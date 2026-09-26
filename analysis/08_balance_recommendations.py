import csv
import os


# ============================================================
# ERA OF STRIFE
# 08_balance_recommendations.py
#
# Назначение:
# - загрузить результаты предыдущих этапов анализа;
# - определить потенциально проблемные юниты;
# - оценить серьёзность отклонений;
# - сформировать рекомендации для дальнейшего баланс-теста;
# - сохранить итоговый отчёт в CSV.
#
# ВАЖНО:
# Скрипт НЕ изменяет характеристики юнитов автоматически.
# Он только помогает геймдизайнеру определить,
# какие элементы баланса требуют дополнительной проверки.
# ============================================================


# ============================================================
# 1. ПУТИ К ФАЙЛАМ
# ============================================================

UNIT_BALANCE_FILE = "data/unit_balance.csv"

MATCHUP_ANALYSIS_FILE = (
    "analysis/results/matchup_analysis.csv"
)

UNIT_COMBAT_STATISTICS_FILE = (
    "analysis/results/unit_combat_statistics.csv"
)

OUTPUT_DIRECTORY = (
    "analysis/results/recommendations"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIRECTORY,
    "balance_recommendations.csv"
)


# ============================================================
# 2. ПОРОГИ ДЛЯ АНАЛИЗА
# ============================================================
#
# Это аналитические пороги, а не окончательные правила
# игрового баланса.
#
# Мы используем их для первичного поиска отклонений.
#
# 45–55%  -> относительно нейтральная зона
# 55–65%  -> повышенный Win Rate
# >65%    -> сильное отклонение
#
# 35–45%  -> пониженный Win Rate
# <35%    -> сильное отрицательное отклонение
#
# ============================================================

BALANCED_MIN = 45.0
BALANCED_MAX = 55.0

HIGH_WIN_RATE = 55.0
VERY_HIGH_WIN_RATE = 65.0

LOW_WIN_RATE = 45.0
VERY_LOW_WIN_RATE = 35.0


# ============================================================
# 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================


def to_float(value, default=0.0):
    """
    Безопасно преобразует значение в float.

    Поддерживает:
    - обычные числа;
    - строки;
    - десятичную запятую;
    - знак процента;
    - пустые значения.
    """

    if value is None:
        return default

    value = str(value).strip()

    if value == "":
        return default

    value = value.replace("%", "")
    value = value.replace(",", ".")

    try:
        return float(value)

    except ValueError:
        return default


def to_int(value, default=0):
    """
    Безопасно преобразует значение в целое число.
    """

    try:
        return int(float(str(value).replace(",", ".")))

    except (ValueError, TypeError):
        return default


def get_first_existing_value(row, possible_names, default=""):
    """
    Возвращает значение первого существующего столбца.

    Это позволяет скрипту работать даже в случае,
    если в CSV использовались немного разные названия
    столбцов на предыдущих этапах проекта.
    """

    for name in possible_names:

        if name in row:

            value = row[name]

            if value is not None and str(value).strip() != "":
                return value

    return default


# ============================================================
# 4. ЗАГРУЗКА UNIT_BALANCE
# ============================================================


def load_unit_balance(file_path):
    """
    Загружает основные характеристики юнитов.
    """

    units = {}

    if not os.path.exists(file_path):

        print(
            "ПРЕДУПРЕЖДЕНИЕ:",
            file_path,
            "не найден."
        )

        return units

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            unit_id = get_first_existing_value(
                row,
                ["Unit_ID", "unit_id"]
            )

            if unit_id == "":
                continue

            units[unit_id] = {
                "Unit_ID": unit_id,

                "Unit_Name": get_first_existing_value(
                    row,
                    ["Unit_Name", "unit_name"],
                    unit_id
                ),

                "Faction": get_first_existing_value(
                    row,
                    ["Faction", "faction"],
                    "Unknown"
                ),

                "Role": get_first_existing_value(
                    row,
                    ["Role", "role"],
                    "Unknown"
                ),

                "Attack_Type": get_first_existing_value(
                    row,
                    ["Attack_Type", "attack_type"],
                    "Unknown"
                ),

                "HP": to_float(
                    get_first_existing_value(
                        row,
                        ["HP", "hp"],
                        0
                    )
                ),

                "Damage": to_float(
                    get_first_existing_value(
                        row,
                        ["Damage", "damage"],
                        0
                    )
                ),

                "Attack_Interval": to_float(
                    get_first_existing_value(
                        row,
                        [
                            "Attack_Interval",
                            "attack_interval"
                        ],
                        0
                    )
                ),

                "DPS": to_float(
                    get_first_existing_value(
                        row,
                        ["DPS", "dps"],
                        0
                    )
                ),

                "Attack_Range": to_float(
                    get_first_existing_value(
                        row,
                        [
                            "Attack_Range",
                            "attack_range"
                        ],
                        0
                    )
                ),

                "Move_Speed": to_float(
                    get_first_existing_value(
                        row,
                        [
                            "Move_Speed",
                            "move_speed"
                        ],
                        0
                    )
                ),

                "Cost": to_float(
                    get_first_existing_value(
                        row,
                        ["Cost", "cost"],
                        0
                    )
                ),
            }

    return units


# ============================================================
# 5. ЗАГРУЗКА UNIT_COMBAT_STATISTICS
# ============================================================


def load_combat_statistics(file_path):
    """
    Загружает агрегированную статистику 1v1 боёв.
    """

    statistics = {}

    if not os.path.exists(file_path):

        print(
            "ПРЕДУПРЕЖДЕНИЕ:",
            file_path,
            "не найден."
        )

        return statistics

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            unit_id = get_first_existing_value(
                row,
                ["Unit_ID", "unit_id"]
            )

            if unit_id == "":
                continue

            wins = to_int(
                get_first_existing_value(
                    row,
                    ["Wins", "wins"],
                    0
                )
            )

            losses = to_int(
                get_first_existing_value(
                    row,
                    ["Losses", "losses"],
                    0
                )
            )

            draws = to_int(
                get_first_existing_value(
                    row,
                    ["Draws", "draws"],
                    0
                )
            )

            total_matches = wins + losses + draws

            win_rate_raw = get_first_existing_value(
                row,
                [
                    "Win_Rate",
                    "Win Rate",
                    "WinRate",
                    "win_rate"
                ],
                ""
            )

            if win_rate_raw != "":

                win_rate = to_float(win_rate_raw)

            elif total_matches > 0:

                win_rate = (
                    wins
                    / total_matches
                    * 100
                )

            else:

                win_rate = 0.0

            combat_score = to_float(
                get_first_existing_value(
                    row,
                    [
                        "Combat_Score",
                        "Combat Score",
                        "CombatScore",
                        "combat_score"
                    ],
                    0
                )
            )

            statistics[unit_id] = {
                "Wins": wins,
                "Losses": losses,
                "Draws": draws,
                "Total_Matches": total_matches,
                "Win_Rate": win_rate,
                "Combat_Score": combat_score,
            }

    return statistics


# ============================================================
# 6. ЗАГРУЗКА MATCHUP_ANALYSIS
# ============================================================


def load_matchup_analysis(file_path):
    """
    Загружает детальные результаты матчапов.

    Функция используется для дополнительной проверки
    количества благоприятных и неблагоприятных матчапов.
    """

    rows = []

    if not os.path.exists(file_path):

        print(
            "ПРЕДУПРЕЖДЕНИЕ:",
            file_path,
            "не найден."
        )

        return rows

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


# ============================================================
# 7. ПОДСЧЁТ MATCHUP SPREAD
# ============================================================


def calculate_matchup_spread(
    unit_id,
    matchup_rows
):
    """
    Пытается определить распределение матчапов юнита:

    - победные;
    - проигрышные;
    - ничейные.

    Если структура matchup_analysis.csv отличается,
    функция не ломает программу.
    """

    wins = 0
    losses = 0
    draws = 0

    for row in matchup_rows:

        selected_unit = get_first_existing_value(
            row,
            [
                "Unit_ID",
                "Selected_Unit_ID",
                "Source_Unit_ID",
                "unit_id"
            ]
        )

        if selected_unit != unit_id:
            continue

        result = get_first_existing_value(
            row,
            [
                "Result",
                "Matchup_Result",
                "Outcome",
                "result"
            ]
        )

        result = str(result).strip().lower()

        if result in [
            "win",
            "w",
            "1",
            "victory"
        ]:

            wins += 1

        elif result in [
            "loss",
            "l",
            "-1",
            "defeat"
        ]:

            losses += 1

        elif result in [
            "draw",
            "d",
            "0"
        ]:

            draws += 1

    return wins, losses, draws


# ============================================================
# 8. ОПРЕДЕЛЕНИЕ СТАТУСА WIN RATE
# ============================================================


def classify_win_rate(win_rate):
    """
    Определяет общий статус Win Rate.
    """

    if win_rate > VERY_HIGH_WIN_RATE:
        return "Very High"

    if win_rate > HIGH_WIN_RATE:
        return "High"

    if win_rate < VERY_LOW_WIN_RATE:
        return "Very Low"

    if win_rate < LOW_WIN_RATE:
        return "Low"

    return "Balanced"


# ============================================================
# 9. ОПРЕДЕЛЕНИЕ СЕРЬЁЗНОСТИ
# ============================================================


def calculate_severity(win_rate):
    """
    Определяет приоритет дальнейшего исследования.

    Critical:
        очень большое отклонение.

    High:
        заметное отклонение.

    Medium:
        небольшое отклонение.

    Low:
        результат находится около нейтральной зоны.
    """

    deviation = abs(
        win_rate - 50.0
    )

    if deviation >= 30:
        return "Critical"

    if deviation >= 20:
        return "High"

    if deviation >= 10:
        return "Medium"

    return "Low"


# ============================================================
# 10. РАСЧЁТ ОТКЛОНЕНИЯ ОТ 50%
# ============================================================


def calculate_deviation(win_rate):
    """
    Возвращает отклонение Win Rate от условного центра 50%.
    """

    return win_rate - 50.0


# ============================================================
# 11. ФОРМИРОВАНИЕ ВОЗМОЖНЫХ ПРИЧИН
# ============================================================


def generate_possible_causes(
    unit,
    win_rate,
    wins,
    losses
):
    """
    Формирует направления для проверки.

    Это НЕ утверждение о причине дисбаланса.

    Скрипт лишь предлагает параметры,
    которые стоит проверить геймдизайнеру.
    """

    causes = []

    role = unit.get(
        "Role",
        "Unknown"
    )

    if win_rate > BALANCED_MAX:

        causes.append(
            "Favorable 1v1 matchup spread"
        )

        causes.append(
            "HP-to-damage relationship may be too efficient"
        )

        if role == "Tank":

            causes.append(
                "Survivability may be too high for 1v1 combat"
            )

        elif role == "Infantry":

            causes.append(
                "Damage, durability or attack tempo may be too efficient"
            )

        elif role == "Ranged":

            causes.append(
                "Damage output may be too efficient in simplified combat"
            )

        elif role == "Support":

            causes.append(
                "1v1 results may not represent the intended team role"
            )

    elif win_rate < BALANCED_MIN:

        causes.append(
            "Unfavorable 1v1 matchup spread"
        )

        causes.append(
            "HP-to-damage relationship may be inefficient"
        )

        if role == "Tank":

            causes.append(
                "Tank may lack sufficient survivability or pressure"
            )

        elif role == "Infantry":

            causes.append(
                "Damage, durability or attack tempo may be insufficient"
            )

        elif role == "Ranged":

            causes.append(
                "Ranged unit may require positioning advantages not represented in 1v1 simulation"
            )

        elif role == "Support":

            causes.append(
                "Low 1v1 Win Rate may be expected because team utility is not represented"
            )

    else:

        causes.append(
            "No major numerical 1v1 deviation detected"
        )

    if wins > losses * 2 and wins > 0:

        causes.append(
            "Wins substantially exceed losses"
        )

    if losses > wins * 2 and losses > 0:

        causes.append(
            "Losses substantially exceed wins"
        )

    causes.append(
        "Current simulation excludes abilities, movement and positioning"
    )

    return causes


# ============================================================
# 12. ФОРМИРОВАНИЕ РЕКОМЕНДАЦИЙ
# ============================================================


def generate_recommendations(
    unit,
    win_rate,
    severity
):
    """
    Создаёт рекомендации по дальнейшему исследованию.

    ВАЖНО:
    Мы не говорим автоматически:
    "уменьшить Damage на 10%".

    Сначала определяется возможная причина,
    затем проводится дополнительный тест.
    """

    recommendations = []

    role = unit.get(
        "Role",
        "Unknown"
    )

    if win_rate > BALANCED_MAX:

        recommendations.append(
            "Review HP, Damage and Attack Interval"
        )

        recommendations.append(
            "Inspect strongest winning matchups"
        )

        recommendations.append(
            "Compare combat efficiency relative to Cost"
        )

        if role == "Tank":

            recommendations.append(
                "Test whether high survivability is driving the result"
            )

        elif role == "Infantry":

            recommendations.append(
                "Test whether offensive efficiency is too high"
            )

        elif role == "Ranged":

            recommendations.append(
                "Test damage output with realistic positioning"
            )

        elif role == "Support":

            recommendations.append(
                "Do not nerf from 1v1 results alone; test team utility first"
            )

    elif win_rate < BALANCED_MIN:

        recommendations.append(
            "Review HP, Damage and Attack Interval"
        )

        recommendations.append(
            "Inspect most frequent losing matchups"
        )

        recommendations.append(
            "Compare combat efficiency relative to Cost"
        )

        if role == "Tank":

            recommendations.append(
                "Test survivability against sustained and burst damage"
            )

        elif role == "Infantry":

            recommendations.append(
                "Test whether the unit reaches its intended damage window"
            )

        elif role == "Ranged":

            recommendations.append(
                "Test the unit with range and positioning advantages enabled"
            )

        elif role == "Support":

            recommendations.append(
                "Evaluate in team scenarios rather than relying on 1v1 Win Rate"
            )

    else:

        recommendations.append(
            "No immediate numerical rebalance required"
        )

        recommendations.append(
            "Continue testing abilities and team interactions"
        )

    if severity in [
        "Critical",
        "High"
    ]:

        recommendations.append(
            "Prioritize this unit in the next balance iteration"
        )

    recommendations.append(
        "Do not change final values before ability and team-based testing"
    )

    return recommendations


# ============================================================
# 13. ФОРМИРОВАНИЕ ПОЛНОГО АНАЛИЗА ЮНИТА
# ============================================================


def analyze_unit(
    unit_id,
    unit,
    combat_statistics,
    matchup_rows
):
    """
    Объединяет все данные по одному юниту
    в единый аналитический результат.
    """

    stats = combat_statistics.get(
        unit_id,
        {}
    )

    wins = stats.get(
        "Wins",
        0
    )

    losses = stats.get(
        "Losses",
        0
    )

    draws = stats.get(
        "Draws",
        0
    )

    total_matches = stats.get(
        "Total_Matches",
        wins + losses + draws
    )

    win_rate = stats.get(
        "Win_Rate",
        0.0
    )

    combat_score = stats.get(
        "Combat_Score",
        0.0
    )

    status = classify_win_rate(
        win_rate
    )

    severity = calculate_severity(
        win_rate
    )

    deviation = calculate_deviation(
        win_rate
    )

    (
        matchup_wins,
        matchup_losses,
        matchup_draws
    ) = calculate_matchup_spread(
        unit_id,
        matchup_rows
    )

    causes = generate_possible_causes(
        unit,
        win_rate,
        wins,
        losses
    )

    recommendations = generate_recommendations(
        unit,
        win_rate,
        severity
    )

    return {
        "Unit_ID": unit_id,
        "Unit_Name": unit["Unit_Name"],
        "Faction": unit["Faction"],
        "Role": unit["Role"],
        "HP": unit["HP"],
        "Damage": unit["Damage"],
        "Attack_Interval": unit["Attack_Interval"],
        "DPS": unit["DPS"],
        "Cost": unit["Cost"],
        "Wins": wins,
        "Losses": losses,
        "Draws": draws,
        "Total_Matches": total_matches,
        "Win_Rate": win_rate,
        "Win_Rate_Deviation": deviation,
        "Combat_Score": combat_score,
        "Status": status,
        "Severity": severity,
        "Matchup_Wins": matchup_wins,
        "Matchup_Losses": matchup_losses,
        "Matchup_Draws": matchup_draws,
        "Possible_Causes": causes,
        "Recommendations": recommendations,
    }


# ============================================================
# 14. СОХРАНЕНИЕ РЕКОМЕНДАЦИЙ В CSV
# ============================================================


def save_recommendations(
    recommendations,
    file_path
):
    """
    Сохраняет итоговый аналитический отчёт.
    """

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    fieldnames = [
        "Unit_ID",
        "Unit_Name",
        "Faction",
        "Role",
        "HP",
        "Damage",
        "Attack_Interval",
        "DPS",
        "Cost",
        "Wins",
        "Losses",
        "Draws",
        "Total_Matches",
        "Win_Rate",
        "Win_Rate_Deviation",
        "Combat_Score",
        "Status",
        "Severity",
        "Matchup_Wins",
        "Matchup_Losses",
        "Matchup_Draws",
        "Possible_Causes",
        "Recommendations",
    ]

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

        for result in recommendations:

            row = result.copy()

            row["Possible_Causes"] = (
                " | ".join(
                    result["Possible_Causes"]
                )
            )

            row["Recommendations"] = (
                " | ".join(
                    result["Recommendations"]
                )
            )

            writer.writerow(row)


# ============================================================
# 15. ВЫВОД ОТЧЁТА В ТЕРМИНАЛ
# ============================================================


def print_unit_report(result):
    """
    Выводит понятный отчёт по одному юниту.
    """

    print()
    print("=" * 70)

    print(
        "BALANCE REVIEW:",
        result["Unit_ID"],
        "—",
        result["Unit_Name"]
    )

    print("=" * 70)

    print(
        "Faction:",
        result["Faction"]
    )

    print(
        "Role:",
        result["Role"]
    )

    print()

    print(
        "Wins:",
        result["Wins"]
    )

    print(
        "Losses:",
        result["Losses"]
    )

    print(
        "Draws:",
        result["Draws"]
    )

    print(
        "Total Matches:",
        result["Total_Matches"]
    )

    print()

    print(
        "Win Rate:",
        round(
            result["Win_Rate"],
            2
        ),
        "%"
    )

    print(
        "Deviation from 50%:",
        round(
            result["Win_Rate_Deviation"],
            2
        ),
        "percentage points"
    )

    print(
        "Combat Score:",
        round(
            result["Combat_Score"],
            2
        )
    )

    print(
        "Status:",
        result["Status"]
    )

    print(
        "Severity:",
        result["Severity"]
    )

    print()

    print("Current numeric parameters:")

    print(
        "  HP:",
        result["HP"]
    )

    print(
        "  Damage:",
        result["Damage"]
    )

    print(
        "  Attack Interval:",
        result["Attack_Interval"]
    )

    print(
        "  DPS:",
        result["DPS"]
    )

    print(
        "  Cost:",
        result["Cost"]
    )

    print()

    print("Possible causes:")

    for index, cause in enumerate(
        result["Possible_Causes"],
        start=1
    ):

        print(
            f"  {index}. {cause}"
        )

    print()

    print("Recommended investigation:")

    for index, recommendation in enumerate(
        result["Recommendations"],
        start=1
    ):

        print(
            f"  {index}. {recommendation}"
        )


# ============================================================
# 16. ОБЩАЯ СВОДКА
# ============================================================


def print_summary(results):
    """
    Показывает общую картину после анализа всех юнитов.
    """

    critical = []
    high = []
    medium = []
    low = []

    for result in results:

        severity = result["Severity"]

        if severity == "Critical":

            critical.append(result)

        elif severity == "High":

            high.append(result)

        elif severity == "Medium":

            medium.append(result)

        else:

            low.append(result)

    print()
    print()
    print("=" * 70)
    print("ИТОГОВАЯ СВОДКА BALANCE REVIEW")
    print("=" * 70)

    print(
        "Всего проанализировано юнитов:",
        len(results)
    )

    print(
        "Critical:",
        len(critical)
    )

    print(
        "High:",
        len(high)
    )

    print(
        "Medium:",
        len(medium)
    )

    print(
        "Low:",
        len(low)
    )

    print()

    print(
        "Приоритет следующей итерации:"
    )

    priority_units = (
        critical
        + high
        + medium
    )

    if priority_units:

        for result in priority_units:

            print(
                " ",
                result["Unit_ID"],
                "|",
                result["Unit_Name"],
                "| Win Rate:",
                round(
                    result["Win_Rate"],
                    2
                ),
                "%",
                "| Severity:",
                result["Severity"]
            )

    else:

        print(
            "  Сильные отклонения не обнаружены."
        )


# ============================================================
# 17. MAIN
# ============================================================


def main():
    """
    Основная последовательность выполнения анализа.
    """

    print("=" * 70)
    print("ERA OF STRIFE — BALANCE RECOMMENDATION SYSTEM")
    print("=" * 70)

    print()
    print("1. Загрузка характеристик юнитов...")

    units = load_unit_balance(
        UNIT_BALANCE_FILE
    )

    print(
        "   Загружено юнитов:",
        len(units)
    )

    print()
    print("2. Загрузка статистики боёв...")

    combat_statistics = load_combat_statistics(
        UNIT_COMBAT_STATISTICS_FILE
    )

    print(
        "   Загружено записей:",
        len(combat_statistics)
    )

    print()
    print("3. Загрузка анализа матчапов...")

    matchup_rows = load_matchup_analysis(
        MATCHUP_ANALYSIS_FILE
    )

    print(
        "   Загружено строк:",
        len(matchup_rows)
    )

    print()
    print("4. Формирование рекомендаций...")

    results = []

    for unit_id, unit in units.items():

        result = analyze_unit(
            unit_id,
            unit,
            combat_statistics,
            matchup_rows
        )

        results.append(result)

    # Сначала показываем самые серьёзные отклонения.
    severity_order = {
        "Critical": 0,
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    results.sort(
        key=lambda result: (
            severity_order.get(
                result["Severity"],
                99
            ),
            -abs(
                result["Win_Rate_Deviation"]
            )
        )
    )

    for result in results:
        print_unit_report(result)

    save_recommendations(
        results,
        OUTPUT_FILE
    )

    print_summary(
        results
    )

    print()
    print("=" * 70)
    print("АНАЛИЗ УСПЕШНО ЗАВЕРШЁН")
    print("=" * 70)

    print(
        "Файл рекомендаций:",
        OUTPUT_FILE
    )

    print()

    print(
        "ВАЖНО: рекомендации являются направлениями"
    )

    print(
        "для дальнейшего тестирования, а не автоматическими"
    )

    print(
        "решениями по изменению характеристик юнитов."
    )


# ============================================================
# 18. ЗАПУСК ПРОГРАММЫ
# ============================================================


if __name__ == "__main__":
    main()