import csv
import os


# ============================================================
# ERA OF STRIFE
# 15 — ITERATION 01 IMPACT ANALYSIS
# ============================================================
#
# Назначение:
#
# Провести итоговый impact analysis Iteration 01.
#
# Источники:
#
# 1. balance_iteration_01.csv
#       Что было намеренно изменено.
#
# 2. 13_iteration_results_analysis.py
#       Что фактически изменилось после Iteration 01.
#
# 3. 14_reproducibility_check.py
#       Воспроизводимы ли результаты.
#
# Скрипт отвечает на вопросы:
#
# - Какие юниты были direct targets?
# - Какие параметры действительно изменились?
# - Улучшились ли direct targets?
# - Какие matchup изменились?
# - Являются изменения direct или indirect?
# - Есть ли потенциальные side effects?
# - Воспроизводим ли эксперимент?
# - Можно ли завершить Iteration 01 и перейти
#   к следующему balance decision?
#
# ВАЖНО:
#
# Этот скрипт НЕ выполняет новую симуляцию.
# Он НЕ изменяет data/unit_balance.csv.
#
# ============================================================


# ============================================================
# 1. ПУТИ
# ============================================================

ITERATION_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "balance_iteration_01.csv",
)

UNIT_RESULTS_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "results_analysis",
    "balance_iteration_01_unit_results_analysis.csv",
)

MATCHUP_RESULTS_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "results_analysis",
    "balance_iteration_01_matchup_results_analysis.csv",
)

RESULTS_SUMMARY_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "results_analysis",
    "balance_iteration_01_results_summary.csv",
)

REPRODUCIBILITY_SUMMARY_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "reproducibility",
    "balance_iteration_01_reproducibility_summary.csv",
)

OUTPUT_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "impact_analysis",
)

DIRECT_CHANGES_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_direct_changes.csv",
)

UNIT_IMPACT_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_unit_impact.csv",
)

MATCHUP_IMPACT_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_matchup_impact.csv",
)

SIDE_EFFECTS_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_side_effects.csv",
)

IMPACT_SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_impact_summary.csv",
)


# ============================================================
# 2. КОНСТАНТЫ
# ============================================================

EXPECTED_UNITS = 12

EXPECTED_MATCHUPS = (
    EXPECTED_UNITS
    * (EXPECTED_UNITS - 1)
    // 2
)

TARGET_WIN_RATE = 50.0


# ============================================================
# 3. CSV HELPERS
# ============================================================

def read_csv(file_path):

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
    fieldnames=None,
):

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True,
    )

    if fieldnames is None:

        if not rows:

            return

        fieldnames = list(
            rows[0].keys()
        )

    with open(
        file_path,
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        if rows:

            writer.writerows(
                rows
            )


def to_float(value):

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


def normalize(value):

    if value is None:

        return ""

    return str(
        value
    ).strip()


def metric_map(rows):

    result = {}

    for row in rows:

        metric = normalize(
            row.get(
                "Metric"
            )
        )

        value = normalize(
            row.get(
                "Value"
            )
        )

        if metric:

            result[
                metric
            ] = value

    return result


def first_present(
    row,
    field_names,
):

    for field in field_names:

        if field in row:

            value = normalize(
                row.get(
                    field
                )
            )

            if value != "":

                return value

    return ""


# ============================================================
# 4. START
# ============================================================

print()
print("=" * 76)
print("ERA OF STRIFE — ITERATION 01 IMPACT ANALYSIS")
print("=" * 76)


# ============================================================
# 5. ПРОВЕРКА ФАЙЛОВ
# ============================================================

required_files = [
    ITERATION_FILE,
    UNIT_RESULTS_FILE,
    MATCHUP_RESULTS_FILE,
    RESULTS_SUMMARY_FILE,
    REPRODUCIBILITY_SUMMARY_FILE,
]


for file_path in required_files:

    if not os.path.exists(
        file_path
    ):

        print()
        print(
            "ОШИБКА: не найден обязательный файл:"
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
# 6. ЗАГРУЗКА
# ============================================================

iteration_rows = read_csv(
    ITERATION_FILE
)

unit_rows = read_csv(
    UNIT_RESULTS_FILE
)

matchup_rows = read_csv(
    MATCHUP_RESULTS_FILE
)

results_summary_rows = read_csv(
    RESULTS_SUMMARY_FILE
)

reproducibility_summary_rows = read_csv(
    REPRODUCIBILITY_SUMMARY_FILE
)


results_summary = metric_map(
    results_summary_rows
)

reproducibility_summary = metric_map(
    reproducibility_summary_rows
)


# ============================================================
# 7. ПРОВЕРКА РАЗМЕРОВ
# ============================================================

if len(unit_rows) != EXPECTED_UNITS:

    print()
    print(
        "ОШИБКА: ожидалось",
        EXPECTED_UNITS,
        "unit result rows, получено",
        len(unit_rows),
    )

    raise SystemExit


if len(matchup_rows) != EXPECTED_MATCHUPS:

    print()
    print(
        "ОШИБКА: ожидалось",
        EXPECTED_MATCHUPS,
        "matchup result rows, получено",
        len(matchup_rows),
    )

    raise SystemExit


print(
    "[OK] Results analysis содержит "
    "12 units / 66 matchups."
)


# ============================================================
# 8. DIRECT TARGETS ИЗ ITERATION PLAN
# ============================================================

direct_targets = set()

direct_changes = []


for row in iteration_rows:

    unit_id = first_present(
        row,
        [
            "Unit_ID",
            "Target_Unit_ID",
        ],
    )

    unit_name = first_present(
        row,
        [
            "Unit_Name",
            "Target_Unit_Name",
        ],
    )

    iteration_target = first_present(
        row,
        [
            "Iteration_Target",
            "Recommendation",
            "Action",
        ],
    )

    changed_parameter = first_present(
        row,
        [
            "Changed_Parameter",
            "Parameter",
            "Target_Parameter",
        ],
    )

    before_value = first_present(
        row,
        [
            "Before_Value",
            "Original_Value",
            "Current_Value",
        ],
    )

    after_value = first_present(
        row,
        [
            "After_Value",
            "New_Value",
            "Proposed_Value",
        ],
    )


    # --------------------------------------------------------
    # В нашем Iteration 01 изменение считается direct,
    # если строка содержит Unit_ID и реально описывает
    # изменяемый параметр.
    # --------------------------------------------------------

    if (
        unit_id != ""
        and changed_parameter != ""
    ):

        direct_targets.add(
            unit_id
        )

        direct_changes.append(
            {
                "Unit_ID":
                    unit_id,

                "Unit_Name":
                    unit_name,

                "Iteration_Target":
                    iteration_target,

                "Changed_Parameter":
                    changed_parameter,

                "Before_Value":
                    before_value,

                "After_Value":
                    after_value,
            }
        )


# ============================================================
# 9. КРИТИЧЕСКАЯ ПРОВЕРКА DIRECT TARGETS
# ============================================================

expected_direct_targets = {
    "HOR_01",
    "HOR_02",
}


if direct_targets != expected_direct_targets:

    print()
    print(
        "ОШИБКА: direct targets из iteration plan "
        "не совпадают с ожидаемыми."
    )

    print(
        "Detected:",
        sorted(
            direct_targets
        ),
    )

    print(
        "Expected:",
        sorted(
            expected_direct_targets
        ),
    )

    raise SystemExit


print()
print(
    "[OK] Direct targets:",
    "; ".join(
        sorted(
            direct_targets
        )
    ),
)

print(
    "[OK] Direct parameter changes:",
    len(
        direct_changes
    ),
)


# ============================================================
# 10. UNIT IMPACT
# ============================================================

unit_impact_rows = []


for row in unit_rows:

    unit_id = normalize(
        row[
            "Unit_ID"
        ]
    )

    is_direct = (
        unit_id
        in direct_targets
    )

    balance_result = normalize(
        row[
            "Balance_Result"
        ]
    )


    if is_direct:

        impact_origin = "Direct"

    elif balance_result != "Unchanged":

        impact_origin = "Indirect"

    else:

        impact_origin = "Unchanged"


    unit_impact_rows.append(
        {
            "Unit_ID":
                unit_id,

            "Unit_Name":
                row[
                    "Unit_Name"
                ],

            "Faction":
                row.get(
                    "Faction",
                    "",
                ),

            "Role":
                row.get(
                    "Role",
                    "",
                ),

            "Is_Direct_Target":
                (
                    "Yes"
                    if is_direct
                    else "No"
                ),

            "Impact_Origin":
                impact_origin,

            "Before_Win_Rate":
                row[
                    "Before_Win_Rate"
                ],

            "After_Win_Rate":
                row[
                    "After_Win_Rate"
                ],

            "Win_Rate_Change":
                row[
                    "Win_Rate_Change"
                ],

            "Before_Combat_Score":
                row[
                    "Before_Combat_Score"
                ],

            "After_Combat_Score":
                row[
                    "After_Combat_Score"
                ],

            "Combat_Score_Change":
                row[
                    "Combat_Score_Change"
                ],

            "Distance_From_50_Before":
                row[
                    "Distance_From_50_Before"
                ],

            "Distance_From_50_After":
                row[
                    "Distance_From_50_After"
                ],

            "Distance_Change":
                row[
                    "Distance_Change"
                ],

            "Balance_Result":
                balance_result,
        }
    )


# ============================================================
# 11. MATCHUP IMPACT
# ============================================================

matchup_impact_rows = []

side_effect_rows = []


for row in matchup_rows:

    unit_1 = normalize(
        row[
            "Matchup_Unit_1"
        ]
    )

    unit_2 = normalize(
        row[
            "Matchup_Unit_2"
        ]
    )

    changed = (
        normalize(
            row[
                "Result_Changed"
            ]
        )
        == "Yes"
    )

    contains_direct_target = (
        unit_1 in direct_targets
        or unit_2 in direct_targets
    )


    # --------------------------------------------------------
    # Классификацию считаем заново.
    #
    # Мы не просто доверяем тексту из 13.
    # Это независимая consistency check.
    # --------------------------------------------------------

    if not changed:

        impact_type = "Unchanged"

    elif contains_direct_target:

        impact_type = "Direct"

    else:

        impact_type = "Indirect"


    potential_side_effect = (
        changed
        and not contains_direct_target
    )


    if potential_side_effect:

        priority = "High"

        interpretation = (
            "Matchup changed even though neither "
            "participant was directly modified. "
            "Investigate before the next iteration."
        )

    elif changed:

        priority = "Normal"

        interpretation = (
            "Matchup changed and contains a directly "
            "modified unit. The change is consistent "
            "with a direct balance impact."
        )

    else:

        priority = "None"

        interpretation = (
            "Matchup result remained unchanged."
        )


    impact_row = {
        "Matchup_Unit_1":
            unit_1,

        "Matchup_Unit_1_Name":
            row[
                "Matchup_Unit_1_Name"
            ],

        "Matchup_Unit_2":
            unit_2,

        "Matchup_Unit_2_Name":
            row[
                "Matchup_Unit_2_Name"
            ],

        "Before_Result":
            row[
                "Before_Result"
            ],

        "After_Result":
            row[
                "After_Result"
            ],

        "Result_Changed":
            (
                "Yes"
                if changed
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
            (
                "Yes"
                if potential_side_effect
                else "No"
            ),

        "Investigation_Priority":
            priority,

        "Interpretation":
            interpretation,
    }


    matchup_impact_rows.append(
        impact_row
    )


    if potential_side_effect:

        side_effect_rows.append(
            impact_row.copy()
        )


# ============================================================
# 12. MATCHUP COUNTERS
# ============================================================

changed_matchups = [
    row
    for row in matchup_impact_rows
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
    for row in matchup_impact_rows
    if row[
        "Result_Changed"
    ] == "No"
]


# ============================================================
# 13. UNIT COUNTERS
# ============================================================

improved_units = [
    row
    for row in unit_impact_rows
    if row[
        "Balance_Result"
    ] == "Improved"
]


worsened_units = [
    row
    for row in unit_impact_rows
    if row[
        "Balance_Result"
    ] == "Worsened"
]


unchanged_units = [
    row
    for row in unit_impact_rows
    if row[
        "Balance_Result"
    ] == "Unchanged"
]


direct_unit_rows = [
    row
    for row in unit_impact_rows
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
# 14. CROSS-CHECK С SUMMARY ИЗ 13
# ============================================================

expected_changed = int(
    to_float(
        results_summary.get(
            "Changed_Matchups",
            0,
        )
    )
)

expected_direct_changed = int(
    to_float(
        results_summary.get(
            "Direct_Changed_Matchups",
            0,
        )
    )
)

expected_indirect_changed = int(
    to_float(
        results_summary.get(
            "Indirect_Changed_Matchups",
            0,
        )
    )
)

expected_side_effects = int(
    to_float(
        results_summary.get(
            "Potential_Side_Effects",
            0,
        )
    )
)


classification_consistent = (
    len(changed_matchups)
    == expected_changed
    and len(direct_changed_matchups)
    == expected_direct_changed
    and len(indirect_changed_matchups)
    == expected_indirect_changed
    and len(side_effect_rows)
    == expected_side_effects
)


if not classification_consistent:

    print()
    print(
        "ОШИБКА: classification в Impact Analysis "
        "не совпадает с Results Analysis."
    )

    raise SystemExit


print()
print(
    "[OK] Matchup classification согласована "
    "с Results Analysis."
)


# ============================================================
# 15. REPRODUCIBILITY
# ============================================================

reproducibility_status = (
    reproducibility_summary.get(
        "Reproducibility_Status",
        "Unknown",
    )
)

logical_outputs_identical = (
    reproducibility_summary.get(
        "Logical_Outputs_Identical",
        "Unknown",
    )
)

unstable_matchups = int(
    to_float(
        reproducibility_summary.get(
            "Unstable_Matchups",
            0,
        )
    )
)

unstable_units = int(
    to_float(
        reproducibility_summary.get(
            "Unstable_Units",
            0,
        )
    )
)

canonical_matchup_mismatches = int(
    to_float(
        reproducibility_summary.get(
            "Canonical_Matchup_Mismatches",
            0,
        )
    )
)

canonical_unit_mismatches = int(
    to_float(
        reproducibility_summary.get(
            "Canonical_Unit_Mismatches",
            0,
        )
    )
)


reproducibility_ok = (
    reproducibility_status
    == "Reproducible"
    and logical_outputs_identical
    == "Yes"
    and unstable_matchups == 0
    and unstable_units == 0
    and canonical_matchup_mismatches == 0
    and canonical_unit_mismatches == 0
)


# ============================================================
# 16. AVERAGE DISTANCE
# ============================================================

average_distance_before = to_float(
    results_summary.get(
        "Average_Distance_From_50_Before",
        0,
    )
)

average_distance_after = to_float(
    results_summary.get(
        "Average_Distance_From_50_After",
        0,
    )
)

average_distance_change = to_float(
    results_summary.get(
        "Average_Distance_Change",
        0,
    )
)


# ============================================================
# 17. SIDE EFFECT RISK
# ============================================================

if len(side_effect_rows) == 0:

    side_effect_risk = "Low"

elif len(side_effect_rows) <= 2:

    side_effect_risk = "Medium"

else:

    side_effect_risk = "High"


# ============================================================
# 18. ITERATION EFFECTIVENESS
# ============================================================

#
# "Successful" здесь означает только успешность
# текущей balance iteration в рамках нашей модели.
#
# Это НЕ означает, что вся игра идеально сбалансирована.
#

if (
    len(direct_improved) > 0
    and len(direct_worsened) == 0
    and average_distance_change <= 0
    and len(side_effect_rows) == 0
    and reproducibility_ok
):

    iteration_effectiveness = "Successful"

elif (
    len(direct_worsened) > 0
    or not reproducibility_ok
):

    iteration_effectiveness = "Needs Review"

else:

    iteration_effectiveness = "Mixed"


# ============================================================
# 19. READINESS FOR NEXT ITERATION
# ============================================================

if not reproducibility_ok:

    iteration_02_readiness = (
        "Fix Reproducibility First"
    )

elif len(side_effect_rows) > 0:

    iteration_02_readiness = (
        "Investigate Indirect Effects First"
    )

elif len(direct_worsened) > 0:

    iteration_02_readiness = (
        "Review Direct Changes First"
    )

else:

    iteration_02_readiness = (
        "Ready for Next Balance Decision"
    )


# ============================================================
# 20. IMPACT SUMMARY
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
            "Direct_Target_Units",

        "Value":
            len(
                direct_targets
            ),
    },
    {
        "Metric":
            "Direct_Target_IDs",

        "Value":
            "; ".join(
                sorted(
                    direct_targets
                )
            ),
    },
    {
        "Metric":
            "Direct_Parameter_Changes",

        "Value":
            len(
                direct_changes
            ),
    },
    {
        "Metric":
            "Total_Units_Analyzed",

        "Value":
            len(
                unit_impact_rows
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
            "Total_Matchups_Analyzed",

        "Value":
            len(
                matchup_impact_rows
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
            "Unchanged_Matchups",

        "Value":
            len(
                unchanged_matchups
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
            "Potential_Side_Effects",

        "Value":
            len(
                side_effect_rows
            ),
    },
    {
        "Metric":
            "Side_Effect_Risk",

        "Value":
            side_effect_risk,
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
            "Reproducibility_Status",

        "Value":
            reproducibility_status,
    },
    {
        "Metric":
            "Reproducibility_OK",

        "Value":
            (
                "Yes"
                if reproducibility_ok
                else "No"
            ),
    },
    {
        "Metric":
            "Matchup_Classification_Consistent",

        "Value":
            (
                "Yes"
                if classification_consistent
                else "No"
            ),
    },
    {
        "Metric":
            "Iteration_Effectiveness",

        "Value":
            iteration_effectiveness,
    },
    {
        "Metric":
            "Iteration_02_Readiness",

        "Value":
            iteration_02_readiness,
    },
]


# ============================================================
# 21. СОХРАНЕНИЕ
# ============================================================

write_csv(
    DIRECT_CHANGES_FILE,
    direct_changes,
)


write_csv(
    UNIT_IMPACT_FILE,
    unit_impact_rows,
)


write_csv(
    MATCHUP_IMPACT_FILE,
    matchup_impact_rows,
)


# Даже если side effects = 0,
# сохраняем CSV с заголовками.

side_effect_fields = [
    "Matchup_Unit_1",
    "Matchup_Unit_1_Name",
    "Matchup_Unit_2",
    "Matchup_Unit_2_Name",
    "Before_Result",
    "After_Result",
    "Result_Changed",
    "Contains_Direct_Target",
    "Impact_Type",
    "Potential_Side_Effect",
    "Investigation_Priority",
    "Interpretation",
]


write_csv(
    SIDE_EFFECTS_FILE,
    side_effect_rows,
    fieldnames=side_effect_fields,
)


write_csv(
    IMPACT_SUMMARY_FILE,
    summary_rows,
)


# ============================================================
# 22. DIRECT CHANGES OUTPUT
# ============================================================

print()
print("=" * 76)
print("DIRECT CHANGES")
print("=" * 76)


for row in direct_changes:

    print()

    print(
        row["Unit_ID"],
        "|",
        row["Unit_Name"],
    )

    print(
        "Target:",
        row["Iteration_Target"],
    )

    print(
        "Parameter:",
        row["Changed_Parameter"],
    )

    print(
        "Before:",
        row["Before_Value"],
    )

    print(
        "After :",
        row["After_Value"],
    )


# ============================================================
# 23. DIRECT TARGET RESULTS
# ============================================================

print()
print("=" * 76)
print("DIRECT TARGET IMPACT")
print("=" * 76)


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
        "Balance result:",
        row["Balance_Result"],
    )


# ============================================================
# 24. CHANGED MATCHUPS OUTPUT
# ============================================================

print()
print("=" * 76)
print("CHANGED MATCHUPS")
print("=" * 76)


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
            "Result:",
            row["Before_Result"],
            "->",
            row["After_Result"],
        )

        print(
            "Impact type:",
            row["Impact_Type"],
        )

        print(
            "Potential side effect:",
            row[
                "Potential_Side_Effect"
            ],
        )


# ============================================================
# 25. SUMMARY OUTPUT
# ============================================================

print()
print("=" * 76)
print("ITERATION 01 IMPACT SUMMARY")
print("=" * 76)

print()
print(
    "Direct target units:",
    len(
        direct_targets
    ),
)

print(
    "Direct parameter changes:",
    len(
        direct_changes
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
    "Potential side effects:",
    len(
        side_effect_rows
    ),
)

print(
    "Side effect risk:",
    side_effect_risk,
)

print()
print(
    "Average distance from 50:",
    round(
        average_distance_before,
        2,
    ),
    "->",
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
    "Reproducibility:",
    reproducibility_status,
)

print(
    "Reproducibility OK:",
    (
        "Yes"
        if reproducibility_ok
        else "No"
    ),
)

print(
    "Classification consistent:",
    (
        "Yes"
        if classification_consistent
        else "No"
    ),
)

print()
print(
    "Iteration effectiveness:",
    iteration_effectiveness,
)

print(
    "Iteration 02 readiness:",
    iteration_02_readiness,
)


# ============================================================
# 26. FINAL INTERPRETATION
# ============================================================

print()
print("=" * 76)
print("INTERPRETATION")
print("=" * 76)

print()

if iteration_effectiveness == "Successful":

    print(
        "Iteration 01 достигла поставленных direct "
        "balance objectives в рамках текущей модели."
    )

    print(
        "Оба direct targets улучшились, direct "
        "worsening не обнаружен."
    )

    print(
        "Необъяснённых indirect matchup changes "
        "не обнаружено."
    )

    print(
        "Результаты воспроизводимы."
    )

    print(
        "Это НЕ означает, что общий баланс игры "
        "идеален; вывод относится только к текущей "
        "модели и Iteration 01."
    )

else:

    print(
        "Iteration 01 требует дополнительного "
        "анализа перед следующим balance decision."
    )


# ============================================================
# 27. FINAL
# ============================================================

print()
print("=" * 76)
print("ITERATION IMPACT ANALYSIS ЗАВЕРШЁН")
print("=" * 76)

print()
print(
    "Direct changes:"
)

print(
    DIRECT_CHANGES_FILE
)

print()
print(
    "Unit impact:"
)

print(
    UNIT_IMPACT_FILE
)

print()
print(
    "Matchup impact:"
)

print(
    MATCHUP_IMPACT_FILE
)

print()
print(
    "Side effects:"
)

print(
    SIDE_EFFECTS_FILE
)

print()
print(
    "Impact summary:"
)

print(
    IMPACT_SUMMARY_FILE
)

print()
print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)