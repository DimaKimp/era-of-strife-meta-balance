import csv
import os
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

RESULTS_DIR = SCRIPT_DIR / "results"
ITERATIONS_DIR = RESULTS_DIR / "iterations"

ITERATION_01_DIR = ITERATIONS_DIR
ITERATION_02_DIR = ITERATIONS_DIR / "iteration_02"

OUTPUT_DIR = ITERATIONS_DIR / "comparison_01_02"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. INPUT FILES
# ============================================================

ITERATION_01_RESULTS = (
    ITERATIONS_DIR
    / "results_analysis"
    / "balance_iteration_01_results_summary.csv"
)

ITERATION_01_UNIT_RESULTS = (
    ITERATIONS_DIR
    / "results_analysis"
    / "balance_iteration_01_unit_results_analysis.csv"
)

ITERATION_01_MATCHUP_RESULTS = (
    ITERATIONS_DIR
    / "results_analysis"
    / "balance_iteration_01_matchup_results_analysis.csv"
)

ITERATION_01_PLAN = (
    ITERATIONS_DIR
    / "balance_iteration_01.csv"
)

ITERATION_02_SUMMARY = (
    ITERATION_02_DIR
    / "balance_iteration_02_summary.csv"
)

ITERATION_02_CHANGES = (
    ITERATION_02_DIR
    / "balance_iteration_02_changes.csv"
)

ITERATION_02_UNIT_COMPARISON = (
    ITERATION_02_DIR
    / "balance_iteration_02_unit_comparison.csv"
)

ITERATION_02_MATCHUP_COMPARISON = (
    ITERATION_02_DIR
    / "balance_iteration_02_matchup_comparison.csv"
)

SOURCE_DATA = PROJECT_ROOT / "data" / "unit_balance.csv"


# ============================================================
# 3. OUTPUT FILES
# ============================================================

ITERATION_COMPARISON_FILE = (
    OUTPUT_DIR
    / "iteration_01_vs_02_summary.csv"
)

TARGET_COMPARISON_FILE = (
    OUTPUT_DIR
    / "direct_targets_comparison.csv"
)

MATCHUP_COMPARISON_FILE = (
    OUTPUT_DIR
    / "changed_matchups_comparison.csv"
)

PORTFOLIO_SUMMARY_FILE = (
    OUTPUT_DIR
    / "portfolio_balance_summary.csv"
)


# ============================================================
# 4. BASIC CSV HELPERS
# ============================================================

def read_csv(path):
    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def write_csv(path, rows, fieldnames):
    with open(
        path,
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def read_metric_file(path):
    """
    Reads files of the form:

    Metric,Value
    Iteration,Iteration 02
    Direct_Target,HOR_02
    ...
    """

    rows = read_csv(path)

    result = {}

    for row in rows:
        metric = row.get("Metric", "").strip()
        value = row.get("Value", "").strip()

        if metric:
            result[metric] = value

    return result


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def first_value(row, possible_names, default=""):
    for name in possible_names:
        value = row.get(name)

        if value not in (None, ""):
            return value

    return default


# ============================================================
# 5. CHECK REQUIRED FILES
# ============================================================

required_files = [
    ITERATION_01_RESULTS,
    ITERATION_01_PLAN,
    ITERATION_02_SUMMARY,
    ITERATION_02_CHANGES,
    ITERATION_02_MATCHUP_COMPARISON,
    SOURCE_DATA,
]

print("=" * 72)
print("ERA OF STRIFE — ITERATION 01 / ITERATION 02 COMPARISON")
print("=" * 72)
print()

print("Проверка входных файлов:")
print()

missing_files = []

for path in required_files:
    exists = path.exists()

    status = "OK" if exists else "MISSING"

    print(
        f"[{status}] "
        f"{os.path.relpath(path, PROJECT_ROOT)}"
    )

    if not exists:
        missing_files.append(path)

print()

if missing_files:
    print(
        "Не найдены обязательные входные файлы."
    )
    print(
        "Сравнение остановлено."
    )

    raise SystemExit(1)


# ============================================================
# 6. LOAD ITERATION 01
# ============================================================

iteration_01_summary = read_metric_file(
    ITERATION_01_RESULTS
)

iteration_01_plan = read_csv(
    ITERATION_01_PLAN
)

iteration_01_unit_results = []

if ITERATION_01_UNIT_RESULTS.exists():
    iteration_01_unit_results = read_csv(
        ITERATION_01_UNIT_RESULTS
    )

iteration_01_matchup_results = []

if ITERATION_01_MATCHUP_RESULTS.exists():
    iteration_01_matchup_results = read_csv(
        ITERATION_01_MATCHUP_RESULTS
    )


# ============================================================
# 7. LOAD ITERATION 02
# ============================================================

iteration_02_summary = read_metric_file(
    ITERATION_02_SUMMARY
)

iteration_02_changes = read_csv(
    ITERATION_02_CHANGES
)

iteration_02_unit_comparison = []

if ITERATION_02_UNIT_COMPARISON.exists():
    iteration_02_unit_comparison = read_csv(
        ITERATION_02_UNIT_COMPARISON
    )

iteration_02_matchup_comparison = read_csv(
    ITERATION_02_MATCHUP_COMPARISON
)


# ============================================================
# 8. ITERATION 01 METRICS
# ============================================================

i1_improved = safe_int(
    iteration_01_summary.get(
        "Improved_Units",
        0,
    )
)

i1_worsened = safe_int(
    iteration_01_summary.get(
        "Worsened_Units",
        0,
    )
)

i1_unchanged = safe_int(
    iteration_01_summary.get(
        "Unchanged_Units",
        0,
    )
)

i1_changed_matchups = safe_int(
    iteration_01_summary.get(
        "Changed_Matchups",
        0,
    )
)

i1_distance_before = safe_float(
    iteration_01_summary.get(
        "Average_Distance_From_50_Before",
        0,
    )
)

i1_distance_after = safe_float(
    iteration_01_summary.get(
        "Average_Distance_From_50_After",
        0,
    )
)

i1_distance_change = safe_float(
    iteration_01_summary.get(
        "Average_Distance_Change",
        i1_distance_after - i1_distance_before,
    )
)

i1_result = iteration_01_summary.get(
    "Overall_Iteration_Result",
    "Unknown",
)


# ============================================================
# 9. ITERATION 02 METRICS
# ============================================================

i2_improved = safe_int(
    iteration_02_summary.get(
        "Improved_Units",
        0,
    )
)

i2_worsened = safe_int(
    iteration_02_summary.get(
        "Worsened_Units",
        0,
    )
)

i2_unchanged = safe_int(
    iteration_02_summary.get(
        "Unchanged_Units",
        0,
    )
)

i2_changed_matchups = safe_int(
    iteration_02_summary.get(
        "Changed_Matchups",
        0,
    )
)

i2_direct_changed = safe_int(
    iteration_02_summary.get(
        "Direct_Changed_Matchups",
        0,
    )
)

i2_indirect_changed = safe_int(
    iteration_02_summary.get(
        "Indirect_Changed_Matchups",
        0,
    )
)

i2_distance_before = safe_float(
    iteration_02_summary.get(
        "Average_Distance_From_50_Before",
        0,
    )
)

i2_distance_after = safe_float(
    iteration_02_summary.get(
        "Average_Distance_From_50_After",
        0,
    )
)

i2_distance_change = safe_float(
    iteration_02_summary.get(
        "Average_Distance_Change",
        i2_distance_after - i2_distance_before,
    )
)

i2_result = iteration_02_summary.get(
    "Iteration_Result",
    "Unknown",
)


# ============================================================
# 10. BUILD HIGH-LEVEL ITERATION COMPARISON
# ============================================================

iteration_comparison_rows = [
    {
        "Iteration": "Iteration 01",
        "Direct_Targets": "HOR_01; HOR_02",
        "Improved_Units": i1_improved,
        "Worsened_Units": i1_worsened,
        "Unchanged_Units": i1_unchanged,
        "Changed_Matchups": i1_changed_matchups,
        "Average_Distance_From_50_Before": (
            round(i1_distance_before, 2)
        ),
        "Average_Distance_From_50_After": (
            round(i1_distance_after, 2)
        ),
        "Average_Distance_Change": (
            round(i1_distance_change, 2)
        ),
        "Iteration_Result": i1_result,
    },
    {
        "Iteration": "Iteration 02",
        "Direct_Targets": iteration_02_summary.get(
            "Direct_Target",
            "HOR_02",
        ),
        "Improved_Units": i2_improved,
        "Worsened_Units": i2_worsened,
        "Unchanged_Units": i2_unchanged,
        "Changed_Matchups": i2_changed_matchups,
        "Average_Distance_From_50_Before": (
            round(i2_distance_before, 2)
        ),
        "Average_Distance_From_50_After": (
            round(i2_distance_after, 2)
        ),
        "Average_Distance_Change": (
            round(i2_distance_change, 2)
        ),
        "Iteration_Result": i2_result,
    },
]

write_csv(
    ITERATION_COMPARISON_FILE,
    iteration_comparison_rows,
    [
        "Iteration",
        "Direct_Targets",
        "Improved_Units",
        "Worsened_Units",
        "Unchanged_Units",
        "Changed_Matchups",
        "Average_Distance_From_50_Before",
        "Average_Distance_From_50_After",
        "Average_Distance_Change",
        "Iteration_Result",
    ],
)


# ============================================================
# 11. DIRECT TARGET HISTORY
# ============================================================

direct_target_rows = []

for row in iteration_01_plan:

    unit_id = first_value(
        row,
        [
            "Unit_ID",
            "unit_id",
        ],
    )

    if unit_id not in {
        "HOR_01",
        "HOR_02",
    }:
        continue

    direct_target_rows.append(
        {
            "Iteration": "Iteration 01",
            "Unit_ID": unit_id,
            "Unit_Name": first_value(
                row,
                [
                    "Unit_Name",
                    "unit_name",
                ],
            ),
            "Parameter": first_value(
                row,
                [
                    "Changed_Parameter",
                    "Parameter",
                ],
                "Damage",
            ),
            "Before": first_value(
                row,
                [
                    "Before",
                    "Old_Value",
                    "Value_Before",
                ],
            ),
            "After": first_value(
                row,
                [
                    "After",
                    "New_Value",
                    "Value_After",
                ],
            ),
            "Iteration_Target": first_value(
                row,
                [
                    "Iteration_Target",
                    "Target",
                    "Recommendation",
                ],
            ),
        }
    )


for row in iteration_02_changes:

    direct_target_rows.append(
        {
            "Iteration": first_value(
                row,
                ["Iteration"],
                "Iteration 02",
            ),
            "Unit_ID": first_value(
                row,
                ["Unit_ID"],
            ),
            "Unit_Name": first_value(
                row,
                ["Unit_Name"],
            ),
            "Parameter": first_value(
                row,
                ["Parameter"],
            ),
            "Before": first_value(
                row,
                ["Before"],
            ),
            "After": first_value(
                row,
                ["After"],
            ),
            "Iteration_Target": (
                "Direct balance adjustment"
            ),
        }
    )


write_csv(
    TARGET_COMPARISON_FILE,
    direct_target_rows,
    [
        "Iteration",
        "Unit_ID",
        "Unit_Name",
        "Parameter",
        "Before",
        "After",
        "Iteration_Target",
    ],
)


# ============================================================
# 12. ITERATION 02 CHANGED MATCHUPS
# ============================================================

changed_matchup_rows = []

for row in iteration_02_matchup_comparison:

    changed = first_value(
        row,
        [
            "Result_Changed",
            "Changed",
        ],
    ).strip().lower()

    if changed not in {
        "yes",
        "true",
        "1",
    }:
        continue

    changed_matchup_rows.append(
        {
            "Iteration": "Iteration 02",
            "Unit_1_ID": first_value(
                row,
                ["Unit_1_ID"],
            ),
            "Unit_1_Name": first_value(
                row,
                ["Unit_1_Name"],
            ),
            "Unit_2_ID": first_value(
                row,
                ["Unit_2_ID"],
            ),
            "Unit_2_Name": first_value(
                row,
                ["Unit_2_Name"],
            ),
            "Winner_Before": first_value(
                row,
                ["Winner_Before"],
            ),
            "Winner_After": first_value(
                row,
                ["Winner_After"],
            ),
            "Impact_Type": first_value(
                row,
                ["Impact_Type"],
            ),
            "Combat_Time_Before": first_value(
                row,
                ["Combat_Time_Before"],
            ),
            "Combat_Time_After": first_value(
                row,
                ["Combat_Time_After"],
            ),
        }
    )


write_csv(
    MATCHUP_COMPARISON_FILE,
    changed_matchup_rows,
    [
        "Iteration",
        "Unit_1_ID",
        "Unit_1_Name",
        "Unit_2_ID",
        "Unit_2_Name",
        "Winner_Before",
        "Winner_After",
        "Impact_Type",
        "Combat_Time_Before",
        "Combat_Time_After",
    ],
)


# ============================================================
# 13. PORTFOLIO SUMMARY
# ============================================================

portfolio_rows = [
    {
        "Metric": "Project",
        "Value": "Era of Strife",
    },
    {
        "Metric": "Analysis_Type",
        "Value": (
            "RTS unit balance iteration analysis"
        ),
    },
    {
        "Metric": "Units_Analyzed",
        "Value": 12,
    },
    {
        "Metric": "Unique_Pairwise_Matchups",
        "Value": 66,
    },
    {
        "Metric": "Iteration_01_Targets",
        "Value": "HOR_01; HOR_02",
    },
    {
        "Metric": "Iteration_01_Changed_Matchups",
        "Value": i1_changed_matchups,
    },
    {
        "Metric": "Iteration_01_Average_Distance_Change",
        "Value": round(
            i1_distance_change,
            2,
        ),
    },
    {
        "Metric": "Iteration_02_Target",
        "Value": iteration_02_summary.get(
            "Direct_Target",
            "HOR_02",
        ),
    },
    {
        "Metric": "Iteration_02_Parameter",
        "Value": iteration_02_summary.get(
            "Parameter",
            "Damage",
        ),
    },
    {
        "Metric": "Iteration_02_Damage_Before",
        "Value": iteration_02_summary.get(
            "Damage_Before",
            "",
        ),
    },
    {
        "Metric": "Iteration_02_Damage_After",
        "Value": iteration_02_summary.get(
            "Damage_After",
            "",
        ),
    },
    {
        "Metric": "Iteration_02_Changed_Matchups",
        "Value": i2_changed_matchups,
    },
    {
        "Metric": "Iteration_02_Direct_Changed_Matchups",
        "Value": i2_direct_changed,
    },
    {
        "Metric": "Iteration_02_Indirect_Changed_Matchups",
        "Value": i2_indirect_changed,
    },
    {
        "Metric": "Iteration_02_Result",
        "Value": i2_result,
    },
    {
        "Metric": "Source_Data_Modified",
        "Value": "No",
    },
]


write_csv(
    PORTFOLIO_SUMMARY_FILE,
    portfolio_rows,
    [
        "Metric",
        "Value",
    ],
)


# ============================================================
# 14. CONSOLE REPORT
# ============================================================

print("=" * 72)
print("ITERATION COMPARISON")
print("=" * 72)
print()

print("Iteration 01")
print("-" * 40)
print(
    f"Improved units:       {i1_improved}"
)
print(
    f"Worsened units:       {i1_worsened}"
)
print(
    f"Unchanged units:      {i1_unchanged}"
)
print(
    f"Changed matchups:     {i1_changed_matchups}"
)
print(
    "Average distance:"
)
print(
    f"  {i1_distance_before:.2f}"
    f" -> {i1_distance_after:.2f}"
)
print(
    f"Change:               "
    f"{i1_distance_change:+.2f}"
)
print(
    f"Result:               {i1_result}"
)

print()

print("Iteration 02")
print("-" * 40)
print(
    "Direct target:        "
    f"{iteration_02_summary.get('Direct_Target', 'HOR_02')}"
)
print(
    "Parameter:            "
    f"{iteration_02_summary.get('Parameter', 'Damage')}"
)
print(
    "Damage:               "
    f"{iteration_02_summary.get('Damage_Before', '')}"
    " -> "
    f"{iteration_02_summary.get('Damage_After', '')}"
)
print(
    f"Improved units:       {i2_improved}"
)
print(
    f"Worsened units:       {i2_worsened}"
)
print(
    f"Unchanged units:      {i2_unchanged}"
)
print(
    f"Changed matchups:     {i2_changed_matchups}"
)
print(
    f"Direct changes:       {i2_direct_changed}"
)
print(
    f"Indirect changes:     {i2_indirect_changed}"
)
print(
    "Average distance:"
)
print(
    f"  {i2_distance_before:.2f}"
    f" -> {i2_distance_after:.2f}"
)
print(
    f"Result:               {i2_result}"
)

print()


# ============================================================
# 15. CHANGED MATCHUP DETAILS
# ============================================================

print("=" * 72)
print("ITERATION 02 — CHANGED MATCHUPS")
print("=" * 72)
print()

if changed_matchup_rows:

    for row in changed_matchup_rows:

        print(
            f"{row['Unit_1_ID']} "
            f"{row['Unit_1_Name']}"
        )

        print("vs")

        print(
            f"{row['Unit_2_ID']} "
            f"{row['Unit_2_Name']}"
        )

        print(
            "Result: "
            f"{row['Winner_Before']}"
            " -> "
            f"{row['Winner_After']}"
        )

        print(
            "Impact: "
            f"{row['Impact_Type']}"
        )

        print(
            "Combat time: "
            f"{row['Combat_Time_Before']}"
            " -> "
            f"{row['Combat_Time_After']}"
        )

        print("-" * 40)

else:
    print(
        "No changed matchups detected."
    )

print()


# ============================================================
# 16. INTERPRETATION
# ============================================================

print("=" * 72)
print("BALANCE INTERPRETATION")
print("=" * 72)
print()

print(
    "Iteration 01 была широкой балансной итерацией:"
)
print(
    "- изменялись HOR_01 и HOR_02;"
)
print(
    f"- изменилось матчапов: {i1_changed_matchups};"
)
print(
    "- появились прямые и косвенные последствия."
)

print()

print(
    "После дополнительного sensitivity analysis "
    "для Stone Ogre:"
)
print(
    "- изменение HP не было выбрано;"
)
print(
    "- для Iteration 02 изменён Damage HOR_02;"
)
print(
    "- HP сохранён без изменения."
)

print()

print(
    "Iteration 02:"
)
print(
    f"- изменившихся матчапов: "
    f"{i2_changed_matchups};"
)
print(
    f"- прямых: "
    f"{i2_direct_changed};"
)
print(
    f"- косвенных: "
    f"{i2_indirect_changed}."
)

print()

if (
    i2_changed_matchups == 1
    and
    i2_indirect_changed == 0
):
    print(
        "Наблюдение: Iteration 02 дала локализованный "
        "эффект — изменился один матчап, непосредственно "
        "связанный с целевой единицей HOR_02."
    )

else:
    print(
        "Наблюдение: Iteration 02 требует дополнительного "
        "анализа распределения прямых и косвенных эффектов."
    )

print()


# ============================================================
# 17. SOURCE DATA INTEGRITY
# ============================================================

print("=" * 72)
print("OUTPUT FILES")
print("=" * 72)
print()

for path in [
    ITERATION_COMPARISON_FILE,
    TARGET_COMPARISON_FILE,
    MATCHUP_COMPARISON_FILE,
    PORTFOLIO_SUMMARY_FILE,
]:
    print(
        os.path.relpath(
            path,
            PROJECT_ROOT,
        )
    )

print()

print("=" * 72)
print("ITERATION 01 / 02 COMPARISON ЗАВЕРШЁН")
print("=" * 72)
print()

print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)