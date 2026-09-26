import csv
import os

from combat_engine import (
    calculate_unit_statistics,
    simulate_all_matchups,
    to_float,
)


# ============================================================
# ERA OF STRIFE
# 05 — BASELINE COMBAT SIMULATION
# ============================================================
#
# Назначение:
#
# 1. Загрузить исходный Unit Balance.
# 2. НЕ изменять исходные характеристики.
# 3. Передать исходных юнитов в единый combat_engine.py.
# 4. Рассчитать все уникальные 1v1 matchup.
# 5. Создать канонический BEFORE для Balance Iteration.
#
# ВАЖНО:
#
# В этом файле НЕТ собственной функции simulate_combat().
#
# Вся боевая математика находится только в:
#
#     analysis/combat_engine.py
#
# Благодаря этому BEFORE и AFTER могут использовать
# абсолютно одну и ту же модель боя.
# ============================================================


# ============================================================
# 1. ПУТИ К ФАЙЛАМ
# ============================================================

UNIT_BALANCE_FILE = os.path.join(
    "data",
    "unit_balance.csv",
)

RESULTS_DIR = os.path.join(
    "analysis",
    "results",
)

MATCHUP_STATISTICS_FILE = os.path.join(
    RESULTS_DIR,
    "matchup_statistics.csv",
)

UNIT_COMBAT_STATISTICS_FILE = os.path.join(
    RESULTS_DIR,
    "unit_combat_statistics.csv",
)

COMBAT_RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "combat_simulation_results.csv",
)


# ============================================================
# 2. ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ЧТЕНИЯ CSV
# ============================================================

def read_csv(file_path):
    """
    Загружает CSV-файл и возвращает список словарей.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


# ============================================================
# 3. ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ СОХРАНЕНИЯ CSV
# ============================================================

def write_csv(
    file_path,
    rows,
):
    """
    Сохраняет список словарей в CSV.

    Названия столбцов автоматически берутся
    из первой строки.
    """

    if not rows:

        print(
            "[WARNING] Нет данных для сохранения:",
            file_path,
        )

        return

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True,
    )

    with open(
        file_path,
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(
                rows[0].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


# ============================================================
# 4. ПРОВЕРКА ИСХОДНОГО ФАЙЛА
# ============================================================

if not os.path.exists(
    UNIT_BALANCE_FILE
):

    print()
    print("=" * 70)
    print("ОШИБКА")
    print("=" * 70)

    print(
        "Не найден файл:",
        UNIT_BALANCE_FILE,
    )

    print()
    print(
        "Запускай скрипт из корня проекта:"
    )

    print(
        "python analysis/05_combat_simulation.py"
    )

    raise SystemExit


# ============================================================
# 5. ЗАГРУЗКА UNIT BALANCE
# ============================================================

print()
print("=" * 70)
print("ERA OF STRIFE — BASELINE COMBAT SIMULATION")
print("=" * 70)

print()
print(
    "Источник данных:",
    UNIT_BALANCE_FILE,
)

unit_rows = read_csv(
    UNIT_BALANCE_FILE
)

print(
    "Загружено строк:",
    len(unit_rows),
)


# ============================================================
# 6. СОЗДАНИЕ СЛОВАРЯ ЮНИТОВ
# ============================================================

units = {}

required_columns = [
    "Unit_ID",
    "Unit_Name",
    "HP",
    "Damage",
    "Attack_Interval",
]


if not unit_rows:

    print()
    print(
        "ОШИБКА: unit_balance.csv пуст."
    )

    raise SystemExit


missing_columns = [
    column
    for column in required_columns
    if column not in unit_rows[0]
]


if missing_columns:

    print()
    print("=" * 70)
    print("ОШИБКА СТРУКТУРЫ UNIT BALANCE")
    print("=" * 70)

    print(
        "Отсутствуют обязательные столбцы:"
    )

    for column in missing_columns:

        print(
            "-",
            column,
        )

    raise SystemExit


for row in unit_rows:

    unit_id = row[
        "Unit_ID"
    ].strip()

    if unit_id == "":

        print()
        print(
            "[WARNING] Найдена строка без Unit_ID."
        )

        print(
            "Строка пропущена."
        )

        continue

    if unit_id in units:

        print()
        print(
            "ОШИБКА: повторяющийся Unit_ID:",
            unit_id,
        )

        raise SystemExit

    # --------------------------------------------------------
    # Проверяем ключевые числовые параметры.
    #
    # Здесь мы ничего НЕ балансируем и НЕ изменяем.
    # Только убеждаемся, что значения пригодны
    # для симуляции.
    # --------------------------------------------------------

    try:

        hp = to_float(
            row["HP"]
        )

        damage = to_float(
            row["Damage"]
        )

        attack_interval = to_float(
            row["Attack_Interval"]
        )

    except ValueError:

        print()
        print(
            "ОШИБКА: невозможно преобразовать "
            "числовые параметры юнита:",
            unit_id,
        )

        raise SystemExit


    if hp <= 0:

        print()
        print(
            "ОШИБКА:",
            unit_id,
            "имеет HP <= 0.",
        )

        raise SystemExit


    if damage <= 0:

        print()
        print(
            "ОШИБКА:",
            unit_id,
            "имеет Damage <= 0.",
        )

        raise SystemExit


    if attack_interval <= 0:

        print()
        print(
            "ОШИБКА:",
            unit_id,
            "имеет Attack_Interval <= 0.",
        )

        raise SystemExit


    units[
        unit_id
    ] = row.copy()


print()
print(
    "Юнитов подготовлено к симуляции:",
    len(units),
)


# ============================================================
# 7. ПРОВЕРКА КОЛИЧЕСТВА ЮНИТОВ
# ============================================================

EXPECTED_UNITS = 12


if len(units) != EXPECTED_UNITS:

    print()
    print(
        "[WARNING] Ожидалось юнитов:",
        EXPECTED_UNITS,
    )

    print(
        "[WARNING] Получено:",
        len(units),
    )


# ============================================================
# 8. РАСЧЁТ ОЖИДАЕМОГО ЧИСЛА MATCHUP
# ============================================================

unit_count = len(
    units
)

expected_matchups = (
    unit_count
    * (
        unit_count - 1
    )
    // 2
)


print()
print("=" * 70)
print("ПАРАМЕТРЫ BASELINE-ТЕСТА")
print("=" * 70)

print(
    "Количество юнитов:",
    unit_count,
)

print(
    "Ожидаемое количество уникальных matchup:",
    expected_matchups,
)

print()
print(
    "Формула:"
)

print(
    "n * (n - 1) / 2"
)

print(
    f"{unit_count} * "
    f"{unit_count - 1} / 2 "
    f"= {expected_matchups}"
)


# ============================================================
# 9. ЗАПУСК ЕДИНОГО COMBAT ENGINE
# ============================================================

print()
print("=" * 70)
print("ЗАПУСК COMBAT ENGINE")
print("=" * 70)

print()
print(
    "Боевая модель:"
)

print(
    "analysis/combat_engine.py"
)

print()
print(
    "Начинаем расчёт всех уникальных matchup..."
)


matchup_results = simulate_all_matchups(
    units
)


print()
print(
    "Рассчитано matchup:",
    len(matchup_results),
)


# ============================================================
# 10. КРИТИЧЕСКАЯ ПРОВЕРКА 66 MATCHUP
# ============================================================

if len(
    matchup_results
) != expected_matchups:

    print()
    print("=" * 70)
    print("ОШИБКА MATCHUP COUNT")
    print("=" * 70)

    print(
        "Ожидалось:",
        expected_matchups,
    )

    print(
        "Получено:",
        len(matchup_results),
    )

    raise SystemExit


print(
    "[OK] Количество matchup соответствует формуле."
)


# ============================================================
# 11. ПРОВЕРКА УНИКАЛЬНОСТИ ПАР
# ============================================================

unique_pairs = set()


for result in matchup_results:

    pair = tuple(
        sorted(
            [
                result["Unit_A_ID"],
                result["Unit_B_ID"],
            ]
        )
    )

    if pair in unique_pairs:

        print()
        print(
            "ОШИБКА: обнаружен повторный matchup:",
            pair,
        )

        raise SystemExit

    unique_pairs.add(
        pair
    )


print(
    "[OK] Все matchup уникальны."
)


# ============================================================
# 12. СТАТИСТИКА ПО ЮНИТАМ
# ============================================================

print()
print("=" * 70)
print("РАСЧЁТ UNIT STATISTICS")
print("=" * 70)


unit_statistics = calculate_unit_statistics(
    units,
    matchup_results,
)


print()
print(
    "Строк статистики юнитов:",
    len(unit_statistics),
)


if len(
    unit_statistics
) != unit_count:

    print()
    print(
        "ОШИБКА: количество строк "
        "unit statistics не совпадает "
        "с количеством юнитов."
    )

    raise SystemExit


print(
    "[OK] Для каждого юнита создана строка статистики."
)


# ============================================================
# 13. ПРОВЕРКА КОЛИЧЕСТВА БОЁВ НА ЮНИТА
# ============================================================

expected_battles_per_unit = (
    unit_count - 1
)


for row in unit_statistics:

    battles = int(
        row["Battles"]
    )

    if battles != expected_battles_per_unit:

        print()
        print(
            "ОШИБКА:",
            row["Unit_ID"],
            "имеет",
            battles,
            "боёв вместо",
            expected_battles_per_unit,
        )

        raise SystemExit


print(
    "[OK] Каждый юнит провёл",
    expected_battles_per_unit,
    "боёв."
)


# ============================================================
# 14. ПРОВЕРКА ОБЩЕГО ЧИСЛА УЧАСТИЙ
# ============================================================

total_unit_battles = sum(
    int(
        row["Battles"]
    )
    for row in unit_statistics
)


expected_total_unit_battles = (
    expected_matchups * 2
)


print()
print(
    "Суммарное количество участий юнитов:",
    total_unit_battles,
)

print(
    "Ожидалось:",
    expected_total_unit_battles,
)


if (
    total_unit_battles
    != expected_total_unit_battles
):

    print()
    print(
        "ОШИБКА: нарушена целостность "
        "matchup statistics."
    )

    raise SystemExit


print(
    "[OK] 66 боёв соответствуют 132 участиям юнитов."
)


# ============================================================
# 15. СОЗДАНИЕ УПРОЩЁННОЙ MATCHUP STATISTICS
# ============================================================

matchup_statistics = []


for result in matchup_results:

    if result[
        "Result"
    ] == "Draw":

        matchup_result = "Draw"

    else:

        matchup_result = result[
            "Winner"
        ]


    matchup_statistics.append(
        {
            "Unit_1_ID":
                result["Unit_A_ID"],

            "Unit_1_Name":
                result["Unit_A_Name"],

            "Unit_2_ID":
                result["Unit_B_ID"],

            "Unit_2_Name":
                result["Unit_B_Name"],

            "Result":
                matchup_result,

            "Winner_ID":
                result["Winner_ID"],

            "Winner":
                result["Winner"],

            "Combat_Time":
                result["Combat_Time"],
        }
    )


# ============================================================
# 16. СОХРАНЕНИЕ ПОЛНЫХ COMBAT RESULTS
# ============================================================

write_csv(
    COMBAT_RESULTS_FILE,
    matchup_results,
)


# ============================================================
# 17. СОХРАНЕНИЕ MATCHUP STATISTICS
# ============================================================

write_csv(
    MATCHUP_STATISTICS_FILE,
    matchup_statistics,
)


# ============================================================
# 18. СОХРАНЕНИЕ UNIT STATISTICS
# ============================================================

write_csv(
    UNIT_COMBAT_STATISTICS_FILE,
    unit_statistics,
)


# ============================================================
# 19. КРАТКИЙ ВЫВОД РЕЗУЛЬТАТОВ
# ============================================================

print()
print("=" * 70)
print("BASELINE RESULTS")
print("=" * 70)


sorted_statistics = sorted(
    unit_statistics,
    key=lambda row: float(
        row["Combat_Score"]
    ),
    reverse=True,
)


for row in sorted_statistics:

    print(
        row["Unit_ID"],
        "|",
        row["Unit_Name"],
        "| Battles:",
        row["Battles"],
        "| W:",
        row["Wins"],
        "| L:",
        row["Losses"],
        "| D:",
        row["Draws"],
        "| Win Rate:",
        str(
            row["Win_Rate"]
        ) + "%",
        "| Combat Score:",
        str(
            row["Combat_Score"]
        ) + "%",
    )


# ============================================================
# 20. ПРОВЕРКА КОНКРЕТНОГО ПОДОЗРИТЕЛЬНОГО MATCHUP
# ============================================================

print()
print("=" * 70)
print("CONTROL MATCHUP")
print("=" * 70)


control_found = False


for row in matchup_statistics:

    pair = {
        row["Unit_1_ID"],
        row["Unit_2_ID"],
    }

    if pair == {
        "ELF_01",
        "ELF_02",
    }:

        control_found = True

        print()
        print(
            "ELF_01 Elven Swordsman"
        )

        print(
            "VS"
        )

        print(
            "ELF_02 Great Forest Bear"
        )

        print()
        print(
            "Canonical BEFORE result:",
            row["Result"],
        )

        print(
            "Combat time:",
            row["Combat_Time"],
        )

        break


if not control_found:

    print()
    print(
        "[WARNING] Контрольный matchup "
        "ELF_01 vs ELF_02 не найден."
    )


# ============================================================
# 21. ИТОГ
# ============================================================

print()
print("=" * 70)
print("BASELINE COMBAT SIMULATION ЗАВЕРШЕНА")
print("=" * 70)

print()

print(
    "Combat results:"
)

print(
    COMBAT_RESULTS_FILE
)

print()

print(
    "Matchup statistics:"
)

print(
    MATCHUP_STATISTICS_FILE
)

print()

print(
    "Unit statistics:"
)

print(
    UNIT_COMBAT_STATISTICS_FILE
)

print()

print(
    "Исходный файл data/unit_balance.csv "
    "не изменялся."
)

print()

print(
    "Этот результат является новым "
    "каноническим BEFORE для Iteration 01."
)