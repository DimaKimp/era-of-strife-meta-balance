import csv
import os


# ============================================================
# ERA OF STRIFE
# 13 — ITERATION 01 RESULTS ANALYSIS
# ============================================================
#
# Назначение:
#
# Сравнить канонические результаты BEFORE и AFTER.
#
# BEFORE:
#     05_combat_simulation.py
#             ↓
#     combat_engine.py
#
# AFTER:
#     12_iteration_combat_simulation.py
#             ↓
#     combat_engine.py
#
# Поэтому теперь обе стороны эксперимента используют
# одну и ту же математическую модель.
#
# Скрипт:
#
# 1. Проверяет структуру BEFORE и AFTER.
# 2. Проверяет наличие 12 юнитов.
# 3. Проверяет наличие 66 matchup.
# 4. Сопоставляет matchup независимо от порядка юнитов.
# 5. Определяет реально изменившиеся matchup.
# 6. Сравнивает статистику каждого юнита.
# 7. Отдельно анализирует direct targets HOR_01 и HOR_02.
# 8. Проверяет контрольный ELF_01 vs ELF_02.
# 9. Формирует итоговые CSV.
#
# ВАЖНО:
#
# Этот скрипт НЕ изменяет:
#
#     data/unit_balance.csv
#
# и НЕ выполняет новую боевую симуляцию.
#
# Он только анализирует уже созданные результаты.
# ============================================================


# ============================================================
# 1. ПУТИ
# ============================================================

BEFORE_MATCHUP_FILE = os.path.join(
    "analysis",
    "results",
    "matchup_statistics.csv",
)

BEFORE_UNIT_FILE = os.path.join(
    "analysis",
    "results",
    "unit_combat_statistics.csv",
)

AFTER_MATCHUP_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "combat_simulation",
    "balance_iteration_01_matchup_statistics.csv",
)

AFTER_UNIT_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "combat_simulation",
    "balance_iteration_01_unit_statistics.csv",
)

RESULTS_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "results_analysis",
)

UNIT_ANALYSIS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_unit_results_analysis.csv",
)

MATCHUP_ANALYSIS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_matchup_results_analysis.csv",
)

SUMMARY_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_results_summary.csv",
)


# ============================================================
# 2. КОНСТАНТЫ
# ============================================================

EXPECTED_UNITS = 12

EXPECTED_MATCHUPS = (
    EXPECTED_UNITS
    * (
        EXPECTED_UNITS - 1
    )
    // 2
)

TARGET_WIN_RATE = 50.0

DIRECT_TARGETS = {
    "HOR_01",
    "HOR_02",
}


# ============================================================
# 3. CSV HELPERS
# ============================================================

def read_csv(file_path):
    """Читает CSV и возвращает список словарей."""

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def write_csv(
    file_path,
    rows,
):
    """Сохраняет список словарей в CSV."""

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


def to_float(value):
    """Преобразует значение в float."""

    if value is None:

        return 0.0

    text = str(
        value
    ).strip()

    if text == "":

        return 0.0

    return float(
        text.replace(
            ",",
            ".",
        )
    )


def to_int(value):
    """Преобразует числовое значение в int."""

    return int(
        round(
            to_float(
                value
            )
        )
    )


# ============================================================
# 4. ПРОВЕРКА ВХОДНЫХ ФАЙЛОВ
# ============================================================

required_files = [
    BEFORE_MATCHUP_FILE,
    BEFORE_UNIT_FILE,
    AFTER_MATCHUP_FILE,
    AFTER_UNIT_FILE,
]


print()
print("=" * 72)
print("ERA OF STRIFE — ITERATION 01 RESULTS ANALYSIS")
print("=" * 72)


for file_path in required_files:

    if not os.path.exists(
        file_path
    ):

        print()
        print("ОШИБКА")

        print(
            "Не найден обязательный файл:"
        )

        print(
            file_path
        )

        raise SystemExit


print()
print(
    "[OK] Все входные файлы найдены."
)


# ============================================================
# 5. ЗАГРУЗКА
# ============================================================

before_matchups = read_csv(
    BEFORE_MATCHUP_FILE
)

before_units = read_csv(
    BEFORE_UNIT_FILE
)

after_matchups = read_csv(
    AFTER_MATCHUP_FILE
)

after_units = read_csv(
    AFTER_UNIT_FILE
)


print()
print("BEFORE:")
print(
    "  Matchups:",
    len(before_matchups),
)
print(
    "  Units:",
    len(before_units),
)

print()
print("AFTER:")
print(
    "  Matchups:",
    len(after_matchups),
)
print(
    "  Units:",
    len(after_units),
)


# ============================================================
# 6. ПРОВЕРКА РАЗМЕРОВ
# ============================================================

if (
    len(before_matchups)
    != EXPECTED_MATCHUPS
):

    print()
    print(
        "ОШИБКА: BEFORE должен содержать",
        EXPECTED_MATCHUPS,
        "matchup, получено",
        len(before_matchups),
    )

    raise SystemExit


if (
    len(after_matchups)
    != EXPECTED_MATCHUPS
):

    print()
    print(
        "ОШИБКА: AFTER должен содержать",
        EXPECTED_MATCHUPS,
        "matchup, получено",
        len(after_matchups),
    )

    raise SystemExit


if (
    len(before_units)
    != EXPECTED_UNITS
):

    print()
    print(
        "ОШИБКА: BEFORE должен содержать",
        EXPECTED_UNITS,
        "юнитов."
    )

    raise SystemExit


if (
    len(after_units)
    != EXPECTED_UNITS
):

    print()
    print(
        "ОШИБКА: AFTER должен содержать",
        EXPECTED_UNITS,
        "юнитов."
    )

    raise SystemExit


print()
print(
    "[OK] BEFORE = 66 matchup / 12 units."
)

print(
    "[OK] AFTER  = 66 matchup / 12 units."
)


# ============================================================
# 7. КЛЮЧ MATCHUP
# ============================================================

def matchup_key(
    unit_1_id,
    unit_2_id,
):
    """
    Создаёт ключ пары независимо от порядка.

    ELF_01 + HOR_02
    и
    HOR_02 + ELF_01

    считаются одним matchup.
    """

    return tuple(
        sorted(
            [
                unit_1_id,
                unit_2_id,
            ]
        )
    )


# ============================================================
# 8. ПРОВЕРКА УНИКАЛЬНОСТИ MATCHUP
# ============================================================

def build_matchup_map(
    rows,
    label,
):

    result = {}

    for row in rows:

        key = matchup_key(
            row["Unit_1_ID"],
            row["Unit_2_ID"],
        )

        if key in result:

            print()
            print(
                "ОШИБКА:",
                label,
                "содержит повторный matchup:",
                key,
            )

            raise SystemExit

        result[
            key
        ] = row

    return result


before_matchup_map = build_matchup_map(
    before_matchups,
    "BEFORE",
)

after_matchup_map = build_matchup_map(
    after_matchups,
    "AFTER",
)


if (
    set(
        before_matchup_map.keys()
    )
    != set(
        after_matchup_map.keys()
    )
):

    print()
    print(
        "ОШИБКА: набор matchup BEFORE "
        "не совпадает с AFTER."
    )

    raise SystemExit


print(
    "[OK] Наборы matchup BEFORE и AFTER совпадают."
)


# ============================================================
# 9. UNIT MAP
# ============================================================

def build_unit_map(
    rows,
    label,
):

    result = {}

    for row in rows:

        unit_id = row[
            "Unit_ID"
        ]

        if unit_id in result:

            print()
            print(
                "ОШИБКА:",
                label,
                "содержит повторный Unit_ID:",
                unit_id,
            )

            raise SystemExit

        result[
            unit_id
        ] = row

    return result


before_unit_map = build_unit_map(
    before_units,
    "BEFORE",
)

after_unit_map = build_unit_map(
    after_units,
    "AFTER",
)


if (
    set(
        before_unit_map.keys()
    )
    != set(
        after_unit_map.keys()
    )
):

    print()
    print(
        "ОШИБКА: набор юнитов BEFORE "
        "не совпадает с AFTER."
    )

    raise SystemExit


print(
    "[OK] Наборы юнитов BEFORE и AFTER совпадают."
)


# ============================================================
# 10. СРАВНЕНИЕ UNIT STATISTICS
# ============================================================

unit_analysis = []


for unit_id in sorted(
    before_unit_map.keys()
):

    before = before_unit_map[
        unit_id
    ]

    after = after_unit_map[
        unit_id
    ]


    before_win_rate = to_float(
        before["Win_Rate"]
    )

    after_win_rate = to_float(
        after["Win_Rate"]
    )


    before_combat_score = to_float(
        before.get(
            "Combat_Score",
            before_win_rate,
        )
    )

    after_combat_score = to_float(
        after.get(
            "Combat_Score",
            after_win_rate,
        )
    )


    before_distance = abs(
        before_combat_score
        - TARGET_WIN_RATE
    )

    after_distance = abs(
        after_combat_score
        - TARGET_WIN_RATE
    )


    distance_change = (
        after_distance
        - before_distance
    )


    # --------------------------------------------------------
    # Отрицательное Distance_Change = улучшение:
    # юнит приблизился к аналитической цели 50.
    # --------------------------------------------------------

    if distance_change < -1e-9:

        balance_result = "Improved"

    elif distance_change > 1e-9:

        balance_result = "Worsened"

    else:

        balance_result = "Unchanged"


    is_direct_target = (
        unit_id
        in DIRECT_TARGETS
    )


    unit_analysis.append(
        {
            "Unit_ID":
                unit_id,

            "Unit_Name":
                before["Unit_Name"],

            "Faction":
                before.get(
                    "Faction",
                    "",
                ),

            "Role":
                before.get(
                    "Role",
                    "",
                ),

            "Is_Direct_Target":
                (
                    "Yes"
                    if is_direct_target
                    else "No"
                ),

            "Before_Battles":
                to_int(
                    before["Battles"]
                ),

            "After_Battles":
                to_int(
                    after["Battles"]
                ),

            "Before_Wins":
                to_int(
                    before["Wins"]
                ),

            "After_Wins":
                to_int(
                    after["Wins"]
                ),

            "Before_Losses":
                to_int(
                    before["Losses"]
                ),

            "After_Losses":
                to_int(
                    after["Losses"]
                ),

            "Before_Draws":
                to_int(
                    before["Draws"]
                ),

            "After_Draws":
                to_int(
                    after["Draws"]
                ),

            "Before_Win_Rate":
                round(
                    before_win_rate,
                    2,
                ),

            "After_Win_Rate":
                round(
                    after_win_rate,
                    2,
                ),

            "Win_Rate_Change":
                round(
                    after_win_rate
                    - before_win_rate,
                    2,
                ),

            "Before_Combat_Score":
                round(
                    before_combat_score,
                    2,
                ),

            "After_Combat_Score":
                round(
                    after_combat_score,
                    2,
                ),

            "Combat_Score_Change":
                round(
                    after_combat_score
                    - before_combat_score,
                    2,
                ),

            "Distance_From_50_Before":
                round(
                    before_distance,
                    2,
                ),

            "Distance_From_50_After":
                round(
                    after_distance,
                    2,
                ),

            "Distance_Change":
                round(
                    distance_change,
                    2,
                ),

            "Balance_Result":
                balance_result,
        }
    )


# ============================================================
# 11. СРАВНЕНИЕ MATCHUP
# ============================================================

matchup_analysis = []


for key in sorted(
    before_matchup_map.keys()
):

    before = before_matchup_map[
        key
    ]

    after = after_matchup_map[
        key
    ]


    before_result = before[
        "Result"
    ]

    after_result = after[
        "Result"
    ]


    result_changed = (
        before_result
        != after_result
    )


    contains_direct_target = (
        key[0] in DIRECT_TARGETS
        or key[1] in DIRECT_TARGETS
    )


    if not result_changed:

        impact_type = "Unchanged"

    elif contains_direct_target:

        impact_type = "Direct"

    else:

        impact_type = "Indirect"


    if (
        result_changed
        and not contains_direct_target
    ):

        potential_side_effect = "Yes"

    else:

        potential_side_effect = "No"


    matchup_analysis.append(
        {
            "Matchup_Unit_1":
                before["Unit_1_ID"],

            "Matchup_Unit_1_Name":
                before["Unit_1_Name"],

            "Matchup_Unit_2":
                before["Unit_2_ID"],

            "Matchup_Unit_2_Name":
                before["Unit_2_Name"],

            "Before_Result":
                before_result,

            "After_Result":
                after_result,

            "Result_Changed":
                (
                    "Yes"
                    if result_changed
                    else "No"
                ),

            "Contains_Direct_Target":
                (
                    "Yes"
                    if contains_direct_target
                    else "No"
                ),

            "Impact_Type":
                impact_type,

            "Potential_Side_Effect":
                potential_side_effect,

            "Before_Combat_Time":
                before.get(
                    "Combat_Time",
                    "",
                ),

            "After_Combat_Time":
                after.get(
                    "Combat_Time",
                    "",
                ),
        }
    )


# ============================================================
# 12. СЧЁТЧИКИ MATCHUP
# ============================================================

changed_matchups = [
    row
    for row in matchup_analysis
    if row[
        "Result_Changed"
    ] == "Yes"
]


direct_changed_matchups = [
    row
    for row in changed_matchups
    if row[
        "Impact_Type"
    ] == "Direct"
]


indirect_changed_matchups = [
    row
    for row in changed_matchups
    if row[
        "Impact_Type"
    ] == "Indirect"
]


unchanged_matchups = [
    row
    for row in matchup_analysis
    if row[
        "Result_Changed"
    ] == "No"
]


# ============================================================
# 13. КОНТРОЛЬ ELF_01 VS ELF_02
# ============================================================

control_key = matchup_key(
    "ELF_01",
    "ELF_02",
)


control_before = before_matchup_map[
    control_key
][
    "Result"
]

control_after = after_matchup_map[
    control_key
][
    "Result"
]


print()
print("=" * 72)
print("PIPELINE CONTROL — ELF_01 VS ELF_02")
print("=" * 72)

print()
print(
    "BEFORE:",
    control_before,
)

print(
    "AFTER :",
    control_after,
)


if (
    control_before
    != control_after
):

    print()
    print(
        "ОШИБКА: немодифицированный контрольный "
        "matchup изменился."
    )

    raise SystemExit


print(
    "[OK] Контрольный matchup не изменился."
)


# ============================================================
# 14. UNIT COUNTERS
# ============================================================

improved_units = [
    row
    for row in unit_analysis
    if row[
        "Balance_Result"
    ] == "Improved"
]

worsened_units = [
    row
    for row in unit_analysis
    if row[
        "Balance_Result"
    ] == "Worsened"
]

unchanged_units = [
    row
    for row in unit_analysis
    if row[
        "Balance_Result"
    ] == "Unchanged"
]


direct_unit_rows = [
    row
    for row in unit_analysis
    if row[
        "Is_Direct_Target"
    ] == "Yes"
]


direct_improved = [
    row
    for row in direct_unit_rows
    if row[
        "Balance_Result"
    ] == "Improved"
]

direct_worsened = [
    row
    for row in direct_unit_rows
    if row[
        "Balance_Result"
    ] == "Worsened"
]

direct_unchanged = [
    row
    for row in direct_unit_rows
    if row[
        "Balance_Result"
    ] == "Unchanged"
]


# ============================================================
# 15. СРЕДНЕЕ ОТКЛОНЕНИЕ ОТ 50
# ============================================================

average_distance_before = (
    sum(
        row[
            "Distance_From_50_Before"
        ]
        for row in unit_analysis
    )
    / len(
        unit_analysis
    )
)


average_distance_after = (
    sum(
        row[
            "Distance_From_50_After"
        ]
        for row in unit_analysis
    )
    / len(
        unit_analysis
    )
)


average_distance_change = (
    average_distance_after
    - average_distance_before
)


# ============================================================
# 16. ОЦЕНКА ITERATION 01
# ============================================================

#
# Здесь "Successful" — НЕ утверждение,
# что весь игровой баланс идеален.
#
# Это только технический вывод текущего
# упрощённого эксперимента:
#
# - оба direct targets не ухудшились;
# - среднее отклонение от аналитической цели не выросло;
# - отсутствуют unexplained indirect matchup changes.
#

if (
    len(direct_worsened) == 0
    and len(direct_improved) > 0
    and average_distance_change <= 1e-9
    and len(indirect_changed_matchups) == 0
):

    overall_result = "Successful"

elif (
    len(direct_worsened) > 0
    or average_distance_change > 1e-9
):

    overall_result = "Needs Review"

else:

    overall_result = "Mixed"


# ============================================================
# 17. SUMMARY
# ============================================================

summary_rows = [
    {
        "Metric":
            "Iteration",

        "Value":
            "Iteration 01",
    },
    {
        "Metric":
            "Target_Win_Rate",

        "Value":
            TARGET_WIN_RATE,
    },
    {
        "Metric":
            "Total_Units",

        "Value":
            len(
                unit_analysis
            ),
    },
    {
        "Metric":
            "Total_Matchups",

        "Value":
            len(
                matchup_analysis
            ),
    },
    {
        "Metric":
            "Improved_Units",

        "Value":
            len(
                improved_units
            ),
    },
    {
        "Metric":
            "Worsened_Units",

        "Value":
            len(
                worsened_units
            ),
    },
    {
        "Metric":
            "Unchanged_Units",

        "Value":
            len(
                unchanged_units
            ),
    },
    {
        "Metric":
            "Direct_Targets",

        "Value":
            len(
                direct_unit_rows
            ),
    },
    {
        "Metric":
            "Direct_Improved",

        "Value":
            len(
                direct_improved
            ),
    },
    {
        "Metric":
            "Direct_Worsened",

        "Value":
            len(
                direct_worsened
            ),
    },
    {
        "Metric":
            "Direct_Unchanged",

        "Value":
            len(
                direct_unchanged
            ),
    },
    {
        "Metric":
            "Average_Distance_From_50_Before",

        "Value":
            round(
                average_distance_before,
                2,
            ),
    },
    {
        "Metric":
            "Average_Distance_From_50_After",

        "Value":
            round(
                average_distance_after,
                2,
            ),
    },
    {
        "Metric":
            "Average_Distance_Change",

        "Value":
            round(
                average_distance_change,
                2,
            ),
    },
    {
        "Metric":
            "Changed_Matchups",

        "Value":
            len(
                changed_matchups
            ),
    },
    {
        "Metric":
            "Direct_Changed_Matchups",

        "Value":
            len(
                direct_changed_matchups
            ),
    },
    {
        "Metric":
            "Indirect_Changed_Matchups",

        "Value":
            len(
                indirect_changed_matchups
            ),
    },
    {
        "Metric":
            "Unchanged_Matchups",

        "Value":
            len(
                unchanged_matchups
            ),
    },
    {
        "Metric":
            "Potential_Side_Effects",

        "Value":
            len(
                indirect_changed_matchups
            ),
    },
    {
        "Metric":
            "Control_ELF_01_vs_ELF_02_Before",

        "Value":
            control_before,
    },
    {
        "Metric":
            "Control_ELF_01_vs_ELF_02_After",

        "Value":
            control_after,
    },
    {
        "Metric":
            "Overall_Iteration_Result",

        "Value":
            overall_result,
    },
]


# ============================================================
# 18. СОХРАНЕНИЕ
# ============================================================

write_csv(
    UNIT_ANALYSIS_FILE,
    unit_analysis,
)

write_csv(
    MATCHUP_ANALYSIS_FILE,
    matchup_analysis,
)

write_csv(
    SUMMARY_FILE,
    summary_rows,
)


# ============================================================
# 19. ВЫВОД ИЗМЕНИВШИХСЯ MATCHUP
# ============================================================

print()
print("=" * 72)
print("CHANGED MATCHUPS")
print("=" * 72)


if not changed_matchups:

    print()
    print(
        "Изменившихся matchup нет."
    )

else:

    for row in changed_matchups:

        print()

        print(
            row["Matchup_Unit_1"],
            row["Matchup_Unit_1_Name"],
            "VS",
            row["Matchup_Unit_2"],
            row["Matchup_Unit_2_Name"],
        )

        print(
            "BEFORE:",
            row["Before_Result"],
        )

        print(
            "AFTER :",
            row["After_Result"],
        )

        print(
            "Impact:",
            row["Impact_Type"],
        )

        print(
            "Side effect:",
            row["Potential_Side_Effect"],
        )


# ============================================================
# 20. DIRECT TARGET RESULTS
# ============================================================

print()
print("=" * 72)
print("DIRECT TARGET RESULTS")
print("=" * 72)


for row in direct_unit_rows:

    print()

    print(
        row["Unit_ID"],
        "|",
        row["Unit_Name"],
    )

    print(
        "Combat Score:",
        row["Before_Combat_Score"],
        "->",
        row["After_Combat_Score"],
    )

    print(
        "Distance from 50:",
        row["Distance_From_50_Before"],
        "->",
        row["Distance_From_50_After"],
    )

    print(
        "Result:",
        row["Balance_Result"],
    )


# ============================================================
# 21. SUMMARY OUTPUT
# ============================================================

print()
print("=" * 72)
print("ITERATION 01 SUMMARY")
print("=" * 72)

print()
print(
    "Total units:",
    len(
        unit_analysis
    ),
)

print(
    "Total matchups:",
    len(
        matchup_analysis
    ),
)

print()
print(
    "Improved units:",
    len(
        improved_units
    ),
)

print(
    "Worsened units:",
    len(
        worsened_units
    ),
)

print(
    "Unchanged units:",
    len(
        unchanged_units
    ),
)

print()
print(
    "Direct targets:",
    len(
        direct_unit_rows
    ),
)

print(
    "Direct improved:",
    len(
        direct_improved
    ),
)

print(
    "Direct worsened:",
    len(
        direct_worsened
    ),
)

print(
    "Direct unchanged:",
    len(
        direct_unchanged
    ),
)

print()
print(
    "Average distance from 50 BEFORE:",
    round(
        average_distance_before,
        2,
    ),
)

print(
    "Average distance from 50 AFTER :",
    round(
        average_distance_after,
        2,
    ),
)

print(
    "Average distance change:",
    round(
        average_distance_change,
        2,
    ),
)

print()
print(
    "Changed matchups:",
    len(
        changed_matchups
    ),
)

print(
    "Direct changed matchups:",
    len(
        direct_changed_matchups
    ),
)

print(
    "Indirect changed matchups:",
    len(
        indirect_changed_matchups
    ),
)

print(
    "Unchanged matchups:",
    len(
        unchanged_matchups
    ),
)

print(
    "Potential side effects:",
    len(
        indirect_changed_matchups
    ),
)

print()
print(
    "Overall Iteration Result:",
    overall_result,
)


# ============================================================
# 22. ФИНАЛ
# ============================================================

print()
print("=" * 72)
print("ITERATION RESULTS ANALYSIS ЗАВЕРШЁН")
print("=" * 72)

print()
print(
    "Unit analysis:"
)

print(
    UNIT_ANALYSIS_FILE
)

print()
print(
    "Matchup analysis:"
)

print(
    MATCHUP_ANALYSIS_FILE
)

print()
print(
    "Summary:"
)

print(
    SUMMARY_FILE
)

print()
print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)

print()
print(
    "BEFORE и AFTER получены одной "
    "версией combat_engine.py."
)