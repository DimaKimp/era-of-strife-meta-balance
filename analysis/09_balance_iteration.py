import csv
import copy
import os


# ============================================================
# 1. НАСТРОЙКИ
# ============================================================

UNIT_BALANCE_FILE = "data/unit_balance.csv"

RESULTS_DIR = "analysis/results/iterations"

ITERATION_RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01.csv"
)

ITERATION_SUMMARY_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_summary.csv"
)


# ------------------------------------------------------------
# Пороговые значения
# ------------------------------------------------------------
#
# Они нужны только для аналитической оценки результатов
# упрощённой 1v1-модели.
#
# Это НЕ означает, что настоящий игровой баланс обязан
# иметь Win Rate каждого юнита ровно 50%.
# ------------------------------------------------------------

TARGET_WIN_RATE = 50.0
ACCEPTABLE_DEVIATION = 10.0


# ============================================================
# 2. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def to_float(value):
    """
    Преобразует значение из CSV в число float.

    Поддерживает как точку, так и запятую
    в качестве десятичного разделителя.
    """

    if value is None:
        return 0.0

    value = str(value).strip()

    if value == "":
        return 0.0

    return float(value.replace(",", "."))


def round_value(value, digits=2):
    """
    Удобное округление чисел для вывода и CSV.
    """

    return round(float(value), digits)


# ============================================================
# 3. ЗАГРУЗКА ЮНИТОВ
# ============================================================

def load_units(file_path):
    """
    Загружает характеристики юнитов из unit_balance.csv.

    Возвращает словарь:

    {
        "UND_01": {...},
        "UND_02": {...},
        ...
    }
    """

    units = {}

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            unit_id = row["Unit_ID"].strip()

            units[unit_id] = {
                "Unit_ID": unit_id,
                "Unit_Name": row["Unit_Name"].strip(),
                "Faction": row["Faction"].strip(),
                "Role": row["Role"].strip(),
                "Attack_Type": row["Attack_Type"].strip(),

                "HP": to_float(row["HP"]),
                "Damage": to_float(row["Damage"]),
                "Attack_Interval": to_float(
                    row["Attack_Interval"]
                ),
                "DPS": to_float(row["DPS"]),
                "Attack_Range": to_float(
                    row["Attack_Range"]
                ),
                "Move_Speed": to_float(
                    row["Move_Speed"]
                ),
                "Cost": to_float(row["Cost"]),
            }

    return units


# ============================================================
# 4. СОЗДАНИЕ БОЕВОЙ КОПИИ ЮНИТА
# ============================================================

def create_combatant(unit):
    """
    Создаёт независимую копию юнита для симуляции.

    Благодаря этому исходные характеристики
    в unit_balance.csv не изменяются.
    """

    fighter = copy.deepcopy(unit)

    fighter["Max_HP"] = float(unit["HP"])
    fighter["Current_HP"] = float(unit["HP"])

    return fighter


# ============================================================
# 5. УПРОЩЁННАЯ 1v1-СИМУЛЯЦИЯ
# ============================================================

def simulate_combat(unit_a, unit_b):
    """
    Симулирует базовый бой 1v1.

    На текущем этапе учитываются:

    - HP;
    - Damage;
    - Attack Interval;
    - независимое время атак.

    Пока НЕ учитываются:

    - способности;
    - дальность;
    - движение;
    - позиционирование;
    - баффы;
    - дебаффы;
    - командные взаимодействия.

    Возвращает:

    Unit_ID победителя

    либо

    "Draw"
    """

    fighter_a = create_combatant(unit_a)
    fighter_b = create_combatant(unit_b)

    current_time = 0.0

    next_attack_a = fighter_a["Attack_Interval"]
    next_attack_b = fighter_b["Attack_Interval"]

    max_time = 300.0

    epsilon = 0.000001

    while (
        fighter_a["Current_HP"] > 0
        and fighter_b["Current_HP"] > 0
        and current_time <= max_time
    ):

        next_event_time = min(
            next_attack_a,
            next_attack_b
        )

        current_time = next_event_time

        attack_a_now = (
            abs(next_attack_a - current_time)
            < epsilon
        )

        attack_b_now = (
            abs(next_attack_b - current_time)
            < epsilon
        )

        damage_to_a = 0.0
        damage_to_b = 0.0

        # ----------------------------------------------------
        # Сначала определяем обе атаки.
        #
        # Это важно для корректной обработки ситуации,
        # когда юниты атакуют одновременно.
        # ----------------------------------------------------

        if attack_a_now:
            damage_to_b = fighter_a["Damage"]

        if attack_b_now:
            damage_to_a = fighter_b["Damage"]

        # ----------------------------------------------------
        # Затем одновременно применяем рассчитанный урон.
        # ----------------------------------------------------

        fighter_a["Current_HP"] -= damage_to_a
        fighter_b["Current_HP"] -= damage_to_b

        # ----------------------------------------------------
        # Планируем следующие атаки.
        # ----------------------------------------------------

        if attack_a_now:
            next_attack_a += fighter_a["Attack_Interval"]

        if attack_b_now:
            next_attack_b += fighter_b["Attack_Interval"]

    # --------------------------------------------------------
    # Определяем результат боя.
    # --------------------------------------------------------

    a_dead = fighter_a["Current_HP"] <= 0
    b_dead = fighter_b["Current_HP"] <= 0

    if a_dead and b_dead:
        return "Draw"

    if b_dead:
        return fighter_a["Unit_ID"]

    if a_dead:
        return fighter_b["Unit_ID"]

    return "Draw"


# ============================================================
# 6. ПОЛНЫЙ MATCHUP-ТЕСТ
# ============================================================

def run_all_matchups(units):
    """
    Каждый юнит сражается с каждым другим юнитом один раз.

    Сам с собой юнит не сражается.

    Для 12 юнитов каждый юнит получает 11 матчей.
    """

    statistics = {}

    for unit_id, unit in units.items():

        statistics[unit_id] = {
            "Unit_ID": unit_id,
            "Unit_Name": unit["Unit_Name"],
            "Faction": unit["Faction"],
            "Role": unit["Role"],
            "Wins": 0,
            "Losses": 0,
            "Draws": 0,
            "Total_Matches": 0,
        }

    unit_ids = list(units.keys())

    # --------------------------------------------------------
    # Берём только уникальные пары.
    #
    # Например:
    #
    # UND_01 vs UND_02
    #
    # повторно
    #
    # UND_02 vs UND_01
    #
    # уже не запускаем.
    # --------------------------------------------------------

    for i in range(len(unit_ids)):

        for j in range(i + 1, len(unit_ids)):

            unit_a_id = unit_ids[i]
            unit_b_id = unit_ids[j]

            unit_a = units[unit_a_id]
            unit_b = units[unit_b_id]

            result = simulate_combat(
                unit_a,
                unit_b
            )

            statistics[unit_a_id]["Total_Matches"] += 1
            statistics[unit_b_id]["Total_Matches"] += 1

            if result == "Draw":

                statistics[unit_a_id]["Draws"] += 1
                statistics[unit_b_id]["Draws"] += 1

            elif result == unit_a_id:

                statistics[unit_a_id]["Wins"] += 1
                statistics[unit_b_id]["Losses"] += 1

            elif result == unit_b_id:

                statistics[unit_b_id]["Wins"] += 1
                statistics[unit_a_id]["Losses"] += 1

    # --------------------------------------------------------
    # Рассчитываем Win Rate.
    #
    # Ничья считается как половина победы:
    #
    # Win Rate =
    #
    # (Wins + 0.5 * Draws) / Total Matches * 100
    # --------------------------------------------------------

    for unit_id, stats in statistics.items():

        total_matches = stats["Total_Matches"]

        if total_matches > 0:

            win_rate = (
                (
                    stats["Wins"]
                    + 0.5 * stats["Draws"]
                )
                / total_matches
                * 100
            )

        else:
            win_rate = 0.0

        stats["Win_Rate"] = round_value(
            win_rate
        )

    return statistics


# ============================================================
# 7. ОЦЕНКА СОСТОЯНИЯ ЮНИТА
# ============================================================

def get_balance_status(win_rate):
    """
    Преобразует Win Rate в простую аналитическую категорию.

    Категории относятся только к текущей
    упрощённой 1v1-модели.
    """

    deviation = win_rate - TARGET_WIN_RATE

    if abs(deviation) <= ACCEPTABLE_DEVIATION:
        return "Balanced"

    if deviation > ACCEPTABLE_DEVIATION:
        return "High"

    return "Low"


# ============================================================
# 8. ВЫБОР ЮНИТОВ ДЛЯ ПЕРВОЙ ИТЕРАЦИИ
# ============================================================

def select_iteration_targets(
    units,
    baseline_statistics
):
    """
    Выбирает кандидатов для первой тестовой итерации.

    ВАЖНО:

    Мы не меняем все проблемные юниты одновременно.

    Для первой итерации выбираем:

    1) одного юнита с высоким Win Rate;
    2) одного юнита с низким Win Rate.

    Support-юниты не используем как основные цели
    автоматической 1v1-корректировки, потому что
    их настоящая ценность должна оцениваться
    в командном бою.
    """

    eligible_units = []

    for unit_id, stats in baseline_statistics.items():

        role = units[unit_id]["Role"]

        if role == "Support":
            continue

        deviation = abs(
            stats["Win_Rate"]
            - TARGET_WIN_RATE
        )

        eligible_units.append(
            {
                "Unit_ID": unit_id,
                "Win_Rate": stats["Win_Rate"],
                "Deviation": deviation,
            }
        )

    high_candidates = [
        item
        for item in eligible_units
        if item["Win_Rate"]
        > TARGET_WIN_RATE + ACCEPTABLE_DEVIATION
    ]

    low_candidates = [
        item
        for item in eligible_units
        if item["Win_Rate"]
        < TARGET_WIN_RATE - ACCEPTABLE_DEVIATION
    ]

    high_candidates.sort(
        key=lambda item: item["Win_Rate"],
        reverse=True
    )

    low_candidates.sort(
        key=lambda item: item["Win_Rate"]
    )

    targets = []

    if high_candidates:
        targets.append(
            {
                "Unit_ID":
                    high_candidates[0]["Unit_ID"],

                "Direction":
                    "Nerf Candidate",
            }
        )

    if low_candidates:
        targets.append(
            {
                "Unit_ID":
                    low_candidates[0]["Unit_ID"],

                "Direction":
                    "Buff Candidate",
            }
        )

    return targets


# ============================================================
# 9. СОЗДАНИЕ ТЕСТОВОГО ИЗМЕНЕНИЯ
# ============================================================

def apply_test_change(
    units,
    unit_id,
    direction
):
    """
    Создаёт небольшое тестовое изменение Damage.

    Nerf Candidate:
        Damage -5%

    Buff Candidate:
        Damage +5%

    Почему только 5%?

    Потому что первая итерация должна быть небольшой
    и контролируемой.

    Мы хотим увидеть направление изменения,
    а не сразу полностью переделать баланс.

    ВАЖНО:
    изменяется только копия данных в памяти.
    unit_balance.csv не перезаписывается.
    """

    old_damage = units[unit_id]["Damage"]

    if direction == "Nerf Candidate":

        multiplier = 0.95

    elif direction == "Buff Candidate":

        multiplier = 1.05

    else:

        multiplier = 1.0

    new_damage = old_damage * multiplier

    units[unit_id]["Damage"] = new_damage

    # --------------------------------------------------------
    # DPS пересчитываем для согласованности данных.
    #
    # DPS = Damage / Attack Interval
    # --------------------------------------------------------

    attack_interval = units[unit_id][
        "Attack_Interval"
    ]

    if attack_interval > 0:

        units[unit_id]["DPS"] = (
            new_damage / attack_interval
        )

    return {
        "Unit_ID": unit_id,
        "Parameter": "Damage",
        "Old_Value": old_damage,
        "New_Value": new_damage,
        "Change_Percent":
            (multiplier - 1.0) * 100,
    }


# ============================================================
# 10. ЗАПУСК ПЕРВОЙ БАЛАНСНОЙ ИТЕРАЦИИ
# ============================================================

def run_balance_iteration(units):
    """
    Полный цикл:

    1. baseline;
    2. выбор кандидатов;
    3. создание копии;
    4. тестовые изменения;
    5. повторная симуляция;
    6. сравнение Before / After.
    """

    print()
    print("=" * 70)
    print("ЭТАП 1. BASELINE-СИМУЛЯЦИЯ")
    print("=" * 70)

    baseline_statistics = run_all_matchups(
        units
    )

    targets = select_iteration_targets(
        units,
        baseline_statistics
    )

    print()
    print("Выбранные кандидаты:")

    if not targets:
        print(
            "Юниты для первой итерации "
            "не обнаружены."
        )

    for target in targets:

        unit_id = target["Unit_ID"]

        print(
            unit_id,
            "|",
            units[unit_id]["Unit_Name"],
            "|",
            target["Direction"],
            "| Win Rate:",
            baseline_statistics[unit_id][
                "Win_Rate"
            ],
            "%"
        )

    # --------------------------------------------------------
    # КРИТИЧЕСКИ ВАЖНО:
    #
    # создаём глубокую копию.
    #
    # Именно её будем изменять.
    # --------------------------------------------------------

    test_units = copy.deepcopy(units)

    changes = []

    print()
    print("=" * 70)
    print("ЭТАП 2. ТЕСТОВЫЕ ИЗМЕНЕНИЯ")
    print("=" * 70)

    for target in targets:

        unit_id = target["Unit_ID"]
        direction = target["Direction"]

        change = apply_test_change(
            test_units,
            unit_id,
            direction
        )

        changes.append(change)

        print()
        print(
            unit_id,
            "|",
            test_units[unit_id]["Unit_Name"]
        )

        print(
            "Направление:",
            direction
        )

        print(
            "Параметр:",
            change["Parameter"]
        )

        print(
            "До:",
            round_value(
                change["Old_Value"]
            )
        )

        print(
            "После:",
            round_value(
                change["New_Value"]
            )
        )

        print(
            "Изменение:",
            round_value(
                change["Change_Percent"]
            ),
            "%"
        )

    print()
    print("=" * 70)
    print("ЭТАП 3. ПОВТОРНАЯ СИМУЛЯЦИЯ")
    print("=" * 70)

    after_statistics = run_all_matchups(
        test_units
    )

    return (
        baseline_statistics,
        after_statistics,
        targets,
        changes,
        test_units,
    )


# ============================================================
# 11. СРАВНЕНИЕ BEFORE / AFTER
# ============================================================

def compare_results(
    units,
    baseline_statistics,
    after_statistics,
    targets,
    changes
):
    """
    Создаёт итоговую таблицу сравнения
    исходного и тестового состояния.
    """

    target_lookup = {
        target["Unit_ID"]: target["Direction"]
        for target in targets
    }

    change_lookup = {
        change["Unit_ID"]: change
        for change in changes
    }

    rows = []

    for unit_id, unit in units.items():

        before = baseline_statistics[unit_id]
        after = after_statistics[unit_id]

        before_win_rate = before["Win_Rate"]
        after_win_rate = after["Win_Rate"]

        delta = (
            after_win_rate
            - before_win_rate
        )

        before_distance = abs(
            before_win_rate
            - TARGET_WIN_RATE
        )

        after_distance = abs(
            after_win_rate
            - TARGET_WIN_RATE
        )

        distance_change = (
            after_distance
            - before_distance
        )

        if distance_change < 0:
            effect = "Closer to 50%"

        elif distance_change > 0:
            effect = "Further from 50%"

        else:
            effect = "No Win Rate change"

        change = change_lookup.get(
            unit_id
        )

        if change:

            parameter = change["Parameter"]

            old_value = round_value(
                change["Old_Value"]
            )

            new_value = round_value(
                change["New_Value"]
            )

            change_percent = round_value(
                change["Change_Percent"]
            )

        else:

            parameter = ""
            old_value = ""
            new_value = ""
            change_percent = ""

        row = {
            "Unit_ID": unit_id,
            "Unit_Name": unit["Unit_Name"],
            "Faction": unit["Faction"],
            "Role": unit["Role"],

            "Iteration_Target":
                target_lookup.get(
                    unit_id,
                    "No"
                ),

            "Changed_Parameter":
                parameter,

            "Old_Value":
                old_value,

            "New_Value":
                new_value,

            "Parameter_Change_Percent":
                change_percent,

            "Before_Wins":
                before["Wins"],

            "Before_Losses":
                before["Losses"],

            "Before_Draws":
                before["Draws"],

            "Before_Win_Rate":
                before_win_rate,

            "After_Wins":
                after["Wins"],

            "After_Losses":
                after["Losses"],

            "After_Draws":
                after["Draws"],

            "After_Win_Rate":
                after_win_rate,

            "Win_Rate_Delta":
                round_value(delta),

            "Before_Deviation":
                round_value(
                    before_win_rate
                    - TARGET_WIN_RATE
                ),

            "After_Deviation":
                round_value(
                    after_win_rate
                    - TARGET_WIN_RATE
                ),

            "Before_Status":
                get_balance_status(
                    before_win_rate
                ),

            "After_Status":
                get_balance_status(
                    after_win_rate
                ),

            "Iteration_Effect":
                effect,
        }

        rows.append(row)

    return rows


# ============================================================
# 12. ВЫВОД СРАВНЕНИЯ В ТЕРМИНАЛ
# ============================================================

def print_comparison(rows):
    """
    Показывает основные результаты первой итерации.
    """

    print()
    print("=" * 70)
    print("ЭТАП 4. BEFORE VS AFTER")
    print("=" * 70)

    print()

    for row in rows:

        if row["Iteration_Target"] == "No":
            continue

        print(
            row["Unit_ID"],
            "|",
            row["Unit_Name"]
        )

        print(
            "  Роль:",
            row["Role"]
        )

        print(
            "  Тип изменения:",
            row["Iteration_Target"]
        )

        print(
            "  Параметр:",
            row["Changed_Parameter"]
        )

        print(
            "  Значение:",
            row["Old_Value"],
            "->",
            row["New_Value"]
        )

        print(
            "  Win Rate:",
            row["Before_Win_Rate"],
            "%",
            "->",
            row["After_Win_Rate"],
            "%"
        )

        print(
            "  Delta:",
            row["Win_Rate_Delta"],
            "п.п."
        )

        print(
            "  Эффект:",
            row["Iteration_Effect"]
        )

        print()


# ============================================================
# 13. СОХРАНЕНИЕ ПОЛНОГО РЕЗУЛЬТАТА
# ============================================================

def save_iteration_results(
    rows,
    file_path
):
    """
    Сохраняет результаты Before / After
    для всех 12 юнитов.
    """

    if not rows:
        return

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    fieldnames = list(
        rows[0].keys()
    )

    with open(
        file_path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# 14. СОЗДАНИЕ SUMMARY
# ============================================================

def create_summary(rows):
    """
    Создаёт короткую таблицу только по тем юнитам,
    которые были изменены в этой итерации.
    """

    summary = []

    for row in rows:

        if row["Iteration_Target"] == "No":
            continue

        summary.append(
            {
                "Unit_ID":
                    row["Unit_ID"],

                "Unit_Name":
                    row["Unit_Name"],

                "Role":
                    row["Role"],

                "Iteration_Target":
                    row["Iteration_Target"],

                "Changed_Parameter":
                    row["Changed_Parameter"],

                "Old_Value":
                    row["Old_Value"],

                "New_Value":
                    row["New_Value"],

                "Parameter_Change_Percent":
                    row[
                        "Parameter_Change_Percent"
                    ],

                "Before_Win_Rate":
                    row["Before_Win_Rate"],

                "After_Win_Rate":
                    row["After_Win_Rate"],

                "Win_Rate_Delta":
                    row["Win_Rate_Delta"],

                "Before_Status":
                    row["Before_Status"],

                "After_Status":
                    row["After_Status"],

                "Iteration_Effect":
                    row["Iteration_Effect"],
            }
        )

    return summary


def save_summary(
    summary,
    file_path
):
    """
    Сохраняет краткий итог первой итерации.
    """

    if not summary:
        return

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    fieldnames = list(
        summary[0].keys()
    )

    with open(
        file_path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(summary)


# ============================================================
# 15. ПРОВЕРКА, ЧТО ИСХОДНЫЙ БАЛАНС НЕ ИЗМЕНЁН
# ============================================================

def verify_original_data(
    original_units,
    test_units
):
    """
    Показывает, какие параметры существуют только
    в тестовой копии.

    Функция НЕ записывает изменения обратно
    в unit_balance.csv.
    """

    print()
    print("=" * 70)
    print("ПРОВЕРКА БЕЗОПАСНОСТИ ИТЕРАЦИИ")
    print("=" * 70)

    changed_count = 0

    for unit_id in original_units:

        original_damage = (
            original_units[unit_id]["Damage"]
        )

        test_damage = (
            test_units[unit_id]["Damage"]
        )

        if abs(
            original_damage - test_damage
        ) > 0.000001:

            changed_count += 1

            print(
                unit_id,
                "|",
                original_units[unit_id][
                    "Unit_Name"
                ],
                "| original Damage:",
                round_value(
                    original_damage
                ),
                "| test Damage:",
                round_value(
                    test_damage
                )
            )

    print()

    print(
        "Изменено юнитов только в тестовой копии:",
        changed_count
    )

    print(
        "Файл data/unit_balance.csv "
        "НЕ перезаписывался."
    )


# ============================================================
# 16. MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("ERA OF STRIFE")
    print("BALANCE ITERATION 01")
    print("=" * 70)

    # --------------------------------------------------------
    # Загружаем исходный баланс.
    # --------------------------------------------------------

    units = load_units(
        UNIT_BALANCE_FILE
    )

    print()
    print(
        "Загружено юнитов:",
        len(units)
    )

    # --------------------------------------------------------
    # Запускаем первую итерацию.
    # --------------------------------------------------------

    (
        baseline_statistics,
        after_statistics,
        targets,
        changes,
        test_units,
    ) = run_balance_iteration(
        units
    )

    # --------------------------------------------------------
    # Сравниваем результаты.
    # --------------------------------------------------------

    rows = compare_results(
        units,
        baseline_statistics,
        after_statistics,
        targets,
        changes
    )

    print_comparison(rows)

    # --------------------------------------------------------
    # Сохраняем полный результат.
    # --------------------------------------------------------

    save_iteration_results(
        rows,
        ITERATION_RESULTS_FILE
    )

    # --------------------------------------------------------
    # Создаём короткое summary.
    # --------------------------------------------------------

    summary = create_summary(
        rows
    )

    save_summary(
        summary,
        ITERATION_SUMMARY_FILE
    )

    # --------------------------------------------------------
    # Проверяем, что оригинальный баланс
    # остался нетронутым.
    # --------------------------------------------------------

    verify_original_data(
        units,
        test_units
    )

    # --------------------------------------------------------
    # Финальная информация.
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("BALANCE ITERATION 01 ЗАВЕРШЕНА")
    print("=" * 70)

    print()
    print(
        "Полный результат:",
        ITERATION_RESULTS_FILE
    )

    print(
        "Краткий результат:",
        ITERATION_SUMMARY_FILE
    )

    print()

    print(
        "ВАЖНО: изменения являются "
        "тестовыми гипотезами."
    )

    print(
        "Исходный unit_balance.csv "
        "автоматически не изменялся."
    )


# ============================================================
# 17. ЗАПУСК ПРОГРАММЫ
# ============================================================

if __name__ == "__main__":
    main()