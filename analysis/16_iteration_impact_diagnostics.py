import csv
import hashlib
import os
import sys


# ============================================================
# ERA OF STRIFE
# 16 — ITERATION 01 PIPELINE VALIDATOR
# ============================================================
#
# Финальная техническая проверка Iteration 01.
#
# Скрипт НЕ:
# - меняет баланс;
# - запускает новую симуляцию;
# - изменяет data/unit_balance.csv;
# - принимает новый balance decision.
#
# Скрипт проверяет согласованность цепочки:
#
# 09 — Balance Iteration
# 12 — Iteration Combat Simulation
# 13 — Results Analysis
# 14 — Reproducibility Check
# 15 — Impact Analysis
#
# ============================================================


# ============================================================
# 1. КОНСТАНТЫ
# ============================================================

ITERATION = "Iteration 01"

EXPECTED_UNITS = 12
EXPECTED_MATCHUPS = 66
EXPECTED_DIRECT_TARGETS = {"HOR_01", "HOR_02"}

EXPECTED_CHANGED_MATCHUPS = 2
EXPECTED_DIRECT_CHANGED_MATCHUPS = 2
EXPECTED_INDIRECT_CHANGED_MATCHUPS = 0
EXPECTED_SIDE_EFFECTS = 0


# ============================================================
# 2. ПУТИ
# ============================================================

SOURCE_FILE = os.path.join(
    "data",
    "unit_balance.csv",
)

ITERATION_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "balance_iteration_01.csv",
)

COMBAT_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "combat_simulation",
)

COMBAT_RESULTS_FILE = os.path.join(
    COMBAT_DIR,
    "balance_iteration_01_combat_results.csv",
)

COMBAT_MATCHUPS_FILE = os.path.join(
    COMBAT_DIR,
    "balance_iteration_01_matchup_statistics.csv",
)

COMBAT_UNITS_FILE = os.path.join(
    COMBAT_DIR,
    "balance_iteration_01_unit_statistics.csv",
)

RESULTS_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "results_analysis",
)

RESULTS_UNITS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_unit_results_analysis.csv",
)

RESULTS_MATCHUPS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_matchup_results_analysis.csv",
)

RESULTS_SUMMARY_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_results_summary.csv",
)

REPRO_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "reproducibility",
)

REPRO_SUMMARY_FILE = os.path.join(
    REPRO_DIR,
    "balance_iteration_01_reproducibility_summary.csv",
)

IMPACT_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "impact_analysis",
)

IMPACT_DIRECT_FILE = os.path.join(
    IMPACT_DIR,
    "balance_iteration_01_direct_changes.csv",
)

IMPACT_UNITS_FILE = os.path.join(
    IMPACT_DIR,
    "balance_iteration_01_unit_impact.csv",
)

IMPACT_MATCHUPS_FILE = os.path.join(
    IMPACT_DIR,
    "balance_iteration_01_matchup_impact.csv",
)

IMPACT_SIDE_EFFECTS_FILE = os.path.join(
    IMPACT_DIR,
    "balance_iteration_01_side_effects.csv",
)

IMPACT_SUMMARY_FILE = os.path.join(
    IMPACT_DIR,
    "balance_iteration_01_impact_summary.csv",
)

OUTPUT_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "diagnostics",
)

VALIDATION_CHECKS_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_validation_checks.csv",
)

VALIDATION_SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_validation_summary.csv",
)


# ============================================================
# 3. CSV HELPERS
# ============================================================

def read_csv(path):

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def write_csv(path, rows, fieldnames=None):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True,
    )

    if fieldnames is None:

        if not rows:
            return

        fieldnames = list(
            rows[0].keys()
        )

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


def normalize(value):

    if value is None:
        return ""

    return str(value).strip()


def to_int(value):

    text = normalize(value)

    if text == "":
        return 0

    return int(float(text.replace(",", ".")))


def to_float(value):

    text = normalize(value)

    if text == "":
        return 0.0

    return float(text.replace(",", "."))


def metric_map(rows):

    result = {}

    for row in rows:

        metric = normalize(
            row.get("Metric")
        )

        value = normalize(
            row.get("Value")
        )

        if metric:
            result[metric] = value

    return result


def sha256(path):

    digest = hashlib.sha256()

    with open(path, "rb") as file:

        while True:

            chunk = file.read(65536)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# 4. CHECK SYSTEM
# ============================================================

checks = []


def add_check(
    category,
    name,
    expected,
    actual,
    passed,
    severity="Critical",
):

    checks.append(
        {
            "Category": category,
            "Check": name,
            "Expected": str(expected),
            "Actual": str(actual),
            "Status": (
                "PASS"
                if passed
                else "FAIL"
            ),
            "Severity": severity,
        }
    )


# ============================================================
# 5. START
# ============================================================

print()
print("=" * 78)
print("ERA OF STRIFE — ITERATION 01 PIPELINE VALIDATOR")
print("=" * 78)
print()

source_hash_before = None

if os.path.exists(SOURCE_FILE):

    source_hash_before = sha256(
        SOURCE_FILE
    )


# ============================================================
# 6. FILE EXISTENCE
# ============================================================

required_files = [
    SOURCE_FILE,
    ITERATION_FILE,

    COMBAT_RESULTS_FILE,
    COMBAT_MATCHUPS_FILE,
    COMBAT_UNITS_FILE,

    RESULTS_UNITS_FILE,
    RESULTS_MATCHUPS_FILE,
    RESULTS_SUMMARY_FILE,

    REPRO_SUMMARY_FILE,

    IMPACT_DIRECT_FILE,
    IMPACT_UNITS_FILE,
    IMPACT_MATCHUPS_FILE,
    IMPACT_SIDE_EFFECTS_FILE,
    IMPACT_SUMMARY_FILE,
]


missing_files = []


for path in required_files:

    exists = os.path.exists(path)

    add_check(
        "Files",
        f"Exists: {path}",
        "Exists",
        (
            "Exists"
            if exists
            else "Missing"
        ),
        exists,
    )

    if not exists:
        missing_files.append(path)


if missing_files:

    print("ОШИБКА: отсутствуют обязательные файлы.")
    print()

    for path in missing_files:
        print(" -", path)

    write_csv(
        VALIDATION_CHECKS_FILE,
        checks,
    )

    sys.exit(1)


print("[OK] Все обязательные файлы существуют.")


# ============================================================
# 7. LOAD DATA
# ============================================================

iteration_rows = read_csv(
    ITERATION_FILE
)

combat_matchup_rows = read_csv(
    COMBAT_MATCHUPS_FILE
)

combat_unit_rows = read_csv(
    COMBAT_UNITS_FILE
)

results_unit_rows = read_csv(
    RESULTS_UNITS_FILE
)

results_matchup_rows = read_csv(
    RESULTS_MATCHUPS_FILE
)

results_summary = metric_map(
    read_csv(
        RESULTS_SUMMARY_FILE
    )
)

repro_summary = metric_map(
    read_csv(
        REPRO_SUMMARY_FILE
    )
)

impact_direct_rows = read_csv(
    IMPACT_DIRECT_FILE
)

impact_unit_rows = read_csv(
    IMPACT_UNITS_FILE
)

impact_matchup_rows = read_csv(
    IMPACT_MATCHUPS_FILE
)

impact_side_effect_rows = read_csv(
    IMPACT_SIDE_EFFECTS_FILE
)

impact_summary = metric_map(
    read_csv(
        IMPACT_SUMMARY_FILE
    )
)


# ============================================================
# 8. DATASET SIZE CHECKS
# ============================================================

add_check(
    "Dataset",
    "Combat unit count",
    EXPECTED_UNITS,
    len(combat_unit_rows),
    len(combat_unit_rows) == EXPECTED_UNITS,
)

add_check(
    "Dataset",
    "Combat matchup count",
    EXPECTED_MATCHUPS,
    len(combat_matchup_rows),
    len(combat_matchup_rows) == EXPECTED_MATCHUPS,
)

add_check(
    "Dataset",
    "Results unit count",
    EXPECTED_UNITS,
    len(results_unit_rows),
    len(results_unit_rows) == EXPECTED_UNITS,
)

add_check(
    "Dataset",
    "Results matchup count",
    EXPECTED_MATCHUPS,
    len(results_matchup_rows),
    len(results_matchup_rows) == EXPECTED_MATCHUPS,
)

add_check(
    "Dataset",
    "Impact unit count",
    EXPECTED_UNITS,
    len(impact_unit_rows),
    len(impact_unit_rows) == EXPECTED_UNITS,
)

add_check(
    "Dataset",
    "Impact matchup count",
    EXPECTED_MATCHUPS,
    len(impact_matchup_rows),
    len(impact_matchup_rows) == EXPECTED_MATCHUPS,
)


# ============================================================
# 9. ITERATION PLAN
# ============================================================

iteration_targets = set()

for row in iteration_rows:

    unit_id = normalize(
        row.get("Unit_ID")
    )

    parameter = normalize(
        row.get("Changed_Parameter")
    )

    if unit_id and parameter:
        iteration_targets.add(unit_id)


add_check(
    "Iteration Plan",
    "Direct target count",
    2,
    len(iteration_targets),
    len(iteration_targets) == 2,
)

add_check(
    "Iteration Plan",
    "Direct target IDs",
    "; ".join(
        sorted(EXPECTED_DIRECT_TARGETS)
    ),
    "; ".join(
        sorted(iteration_targets)
    ),
    iteration_targets
    == EXPECTED_DIRECT_TARGETS,
)


# ============================================================
# 10. RESULTS ANALYSIS CHECKS
# ============================================================

results_total_units = to_int(
    results_summary.get(
        "Total_Units"
    )
)

results_total_matchups = to_int(
    results_summary.get(
        "Total_Matchups"
    )
)

results_improved = to_int(
    results_summary.get(
        "Improved_Units"
    )
)

results_worsened = to_int(
    results_summary.get(
        "Worsened_Units"
    )
)

results_unchanged = to_int(
    results_summary.get(
        "Unchanged_Units"
    )
)

results_direct_targets = to_int(
    results_summary.get(
        "Direct_Targets"
    )
)

results_direct_improved = to_int(
    results_summary.get(
        "Direct_Improved"
    )
)

results_direct_worsened = to_int(
    results_summary.get(
        "Direct_Worsened"
    )
)

results_changed_matchups = to_int(
    results_summary.get(
        "Changed_Matchups"
    )
)

results_direct_changed = to_int(
    results_summary.get(
        "Direct_Changed_Matchups"
    )
)

results_indirect_changed = to_int(
    results_summary.get(
        "Indirect_Changed_Matchups"
    )
)

results_unchanged_matchups = to_int(
    results_summary.get(
        "Unchanged_Matchups"
    )
)

results_side_effects = to_int(
    results_summary.get(
        "Potential_Side_Effects"
    )
)


add_check(
    "Results Analysis",
    "Total units",
    EXPECTED_UNITS,
    results_total_units,
    results_total_units
    == EXPECTED_UNITS,
)

add_check(
    "Results Analysis",
    "Unit partition",
    EXPECTED_UNITS,
    (
        results_improved
        + results_worsened
        + results_unchanged
    ),
    (
        results_improved
        + results_worsened
        + results_unchanged
    )
    == EXPECTED_UNITS,
)

add_check(
    "Results Analysis",
    "Total matchups",
    EXPECTED_MATCHUPS,
    results_total_matchups,
    results_total_matchups
    == EXPECTED_MATCHUPS,
)

add_check(
    "Results Analysis",
    "Matchup partition",
    EXPECTED_MATCHUPS,
    (
        results_changed_matchups
        + results_unchanged_matchups
    ),
    (
        results_changed_matchups
        + results_unchanged_matchups
    )
    == EXPECTED_MATCHUPS,
)

add_check(
    "Results Analysis",
    "Changed matchup partition",
    results_changed_matchups,
    (
        results_direct_changed
        + results_indirect_changed
    ),
    (
        results_direct_changed
        + results_indirect_changed
    )
    == results_changed_matchups,
)

add_check(
    "Results Analysis",
    "Direct targets",
    2,
    results_direct_targets,
    results_direct_targets == 2,
)

add_check(
    "Results Analysis",
    "Direct improved",
    2,
    results_direct_improved,
    results_direct_improved == 2,
)

add_check(
    "Results Analysis",
    "Direct worsened",
    0,
    results_direct_worsened,
    results_direct_worsened == 0,
)

add_check(
    "Results Analysis",
    "Changed matchups",
    EXPECTED_CHANGED_MATCHUPS,
    results_changed_matchups,
    results_changed_matchups
    == EXPECTED_CHANGED_MATCHUPS,
)

add_check(
    "Results Analysis",
    "Direct changed matchups",
    EXPECTED_DIRECT_CHANGED_MATCHUPS,
    results_direct_changed,
    results_direct_changed
    == EXPECTED_DIRECT_CHANGED_MATCHUPS,
)

add_check(
    "Results Analysis",
    "Indirect changed matchups",
    EXPECTED_INDIRECT_CHANGED_MATCHUPS,
    results_indirect_changed,
    results_indirect_changed
    == EXPECTED_INDIRECT_CHANGED_MATCHUPS,
)

add_check(
    "Results Analysis",
    "Potential side effects",
    EXPECTED_SIDE_EFFECTS,
    results_side_effects,
    results_side_effects
    == EXPECTED_SIDE_EFFECTS,
)


# ============================================================
# 11. REPRODUCIBILITY CHECKS
# ============================================================

repro_runs = to_int(
    repro_summary.get("Runs")
)

repro_units = to_int(
    repro_summary.get(
        "Units_Per_Run"
    )
)

repro_matchups = to_int(
    repro_summary.get(
        "Matchups_Per_Run"
    )
)

logical_identical = normalize(
    repro_summary.get(
        "Logical_Outputs_Identical"
    )
)

unique_signatures = to_int(
    repro_summary.get(
        "Unique_Run_Signatures"
    )
)

unstable_matchups = to_int(
    repro_summary.get(
        "Unstable_Matchups"
    )
)

unstable_units = to_int(
    repro_summary.get(
        "Unstable_Units"
    )
)

canonical_matchup_mismatches = to_int(
    repro_summary.get(
        "Canonical_Matchup_Mismatches"
    )
)

canonical_unit_mismatches = to_int(
    repro_summary.get(
        "Canonical_Unit_Mismatches"
    )
)

source_file_unchanged = normalize(
    repro_summary.get(
        "Source_File_Unchanged"
    )
)

repro_status = normalize(
    repro_summary.get(
        "Reproducibility_Status"
    )
)


repro_checks = [
    (
        "Runs",
        5,
        repro_runs,
        repro_runs == 5,
    ),
    (
        "Units per run",
        EXPECTED_UNITS,
        repro_units,
        repro_units == EXPECTED_UNITS,
    ),
    (
        "Matchups per run",
        EXPECTED_MATCHUPS,
        repro_matchups,
        repro_matchups == EXPECTED_MATCHUPS,
    ),
    (
        "Logical outputs identical",
        "Yes",
        logical_identical,
        logical_identical == "Yes",
    ),
    (
        "Unique run signatures",
        1,
        unique_signatures,
        unique_signatures == 1,
    ),
    (
        "Unstable matchups",
        0,
        unstable_matchups,
        unstable_matchups == 0,
    ),
    (
        "Unstable units",
        0,
        unstable_units,
        unstable_units == 0,
    ),
    (
        "Canonical matchup mismatches",
        0,
        canonical_matchup_mismatches,
        canonical_matchup_mismatches == 0,
    ),
    (
        "Canonical unit mismatches",
        0,
        canonical_unit_mismatches,
        canonical_unit_mismatches == 0,
    ),
    (
        "Source file unchanged",
        "Yes",
        source_file_unchanged,
        source_file_unchanged == "Yes",
    ),
    (
        "Reproducibility status",
        "Reproducible",
        repro_status,
        repro_status == "Reproducible",
    ),
]


for (
    name,
    expected,
    actual,
    passed,
) in repro_checks:

    add_check(
        "Reproducibility",
        name,
        expected,
        actual,
        passed,
    )


# ============================================================
# 12. IMPACT ANALYSIS CHECKS
# ============================================================

impact_direct_targets = to_int(
    impact_summary.get(
        "Direct_Target_Units"
    )
)

impact_direct_changes = to_int(
    impact_summary.get(
        "Direct_Parameter_Changes"
    )
)

impact_total_units = to_int(
    impact_summary.get(
        "Total_Units_Analyzed"
    )
)

impact_improved = to_int(
    impact_summary.get(
        "Improved_Units"
    )
)

impact_worsened = to_int(
    impact_summary.get(
        "Worsened_Units"
    )
)

impact_unchanged = to_int(
    impact_summary.get(
        "Unchanged_Units"
    )
)

impact_direct_improved = to_int(
    impact_summary.get(
        "Direct_Improved"
    )
)

impact_direct_worsened = to_int(
    impact_summary.get(
        "Direct_Worsened"
    )
)

impact_total_matchups = to_int(
    impact_summary.get(
        "Total_Matchups_Analyzed"
    )
)

impact_changed = to_int(
    impact_summary.get(
        "Changed_Matchups"
    )
)

impact_unchanged_matchups = to_int(
    impact_summary.get(
        "Unchanged_Matchups"
    )
)

impact_direct_changed = to_int(
    impact_summary.get(
        "Direct_Changed_Matchups"
    )
)

impact_indirect_changed = to_int(
    impact_summary.get(
        "Indirect_Changed_Matchups"
    )
)

impact_side_effects = to_int(
    impact_summary.get(
        "Potential_Side_Effects"
    )
)

impact_repro_ok = normalize(
    impact_summary.get(
        "Reproducibility_OK"
    )
)

impact_classification_ok = normalize(
    impact_summary.get(
        "Matchup_Classification_Consistent"
    )
)

iteration_effectiveness = normalize(
    impact_summary.get(
        "Iteration_Effectiveness"
    )
)

iteration_readiness = normalize(
    impact_summary.get(
        "Iteration_02_Readiness"
    )
)


impact_checks = [
    (
        "Direct target units",
        2,
        impact_direct_targets,
        impact_direct_targets == 2,
    ),
    (
        "Direct parameter changes",
        2,
        impact_direct_changes,
        impact_direct_changes == 2,
    ),
    (
        "Total units",
        EXPECTED_UNITS,
        impact_total_units,
        impact_total_units == EXPECTED_UNITS,
    ),
    (
        "Unit partition",
        EXPECTED_UNITS,
        (
            impact_improved
            + impact_worsened
            + impact_unchanged
        ),
        (
            impact_improved
            + impact_worsened
            + impact_unchanged
        )
        == EXPECTED_UNITS,
    ),
    (
        "Direct improved",
        2,
        impact_direct_improved,
        impact_direct_improved == 2,
    ),
    (
        "Direct worsened",
        0,
        impact_direct_worsened,
        impact_direct_worsened == 0,
    ),
    (
        "Total matchups",
        EXPECTED_MATCHUPS,
        impact_total_matchups,
        impact_total_matchups == EXPECTED_MATCHUPS,
    ),
    (
        "Matchup partition",
        EXPECTED_MATCHUPS,
        (
            impact_changed
            + impact_unchanged_matchups
        ),
        (
            impact_changed
            + impact_unchanged_matchups
        )
        == EXPECTED_MATCHUPS,
    ),
    (
        "Changed matchups",
        EXPECTED_CHANGED_MATCHUPS,
        impact_changed,
        impact_changed
        == EXPECTED_CHANGED_MATCHUPS,
    ),
    (
        "Direct changed matchups",
        EXPECTED_DIRECT_CHANGED_MATCHUPS,
        impact_direct_changed,
        impact_direct_changed
        == EXPECTED_DIRECT_CHANGED_MATCHUPS,
    ),
    (
        "Indirect changed matchups",
        EXPECTED_INDIRECT_CHANGED_MATCHUPS,
        impact_indirect_changed,
        impact_indirect_changed
        == EXPECTED_INDIRECT_CHANGED_MATCHUPS,
    ),
    (
        "Potential side effects",
        EXPECTED_SIDE_EFFECTS,
        impact_side_effects,
        impact_side_effects
        == EXPECTED_SIDE_EFFECTS,
    ),
    (
        "Reproducibility OK",
        "Yes",
        impact_repro_ok,
        impact_repro_ok == "Yes",
    ),
    (
        "Classification consistent",
        "Yes",
        impact_classification_ok,
        impact_classification_ok == "Yes",
    ),
    (
        "Iteration effectiveness",
        "Successful",
        iteration_effectiveness,
        iteration_effectiveness
        == "Successful",
    ),
    (
        "Iteration 02 readiness",
        "Ready for Next Balance Decision",
        iteration_readiness,
        iteration_readiness
        == "Ready for Next Balance Decision",
    ),
]


for (
    name,
    expected,
    actual,
    passed,
) in impact_checks:

    add_check(
        "Impact Analysis",
        name,
        expected,
        actual,
        passed,
    )


# ============================================================
# 13. CROSS-STAGE CONSISTENCY
# ============================================================

cross_checks = [
    (
        "Direct targets: 13 vs 15",
        results_direct_targets,
        impact_direct_targets,
    ),
    (
        "Improved units: 13 vs 15",
        results_improved,
        impact_improved,
    ),
    (
        "Worsened units: 13 vs 15",
        results_worsened,
        impact_worsened,
    ),
    (
        "Unchanged units: 13 vs 15",
        results_unchanged,
        impact_unchanged,
    ),
    (
        "Direct improved: 13 vs 15",
        results_direct_improved,
        impact_direct_improved,
    ),
    (
        "Direct worsened: 13 vs 15",
        results_direct_worsened,
        impact_direct_worsened,
    ),
    (
        "Changed matchups: 13 vs 15",
        results_changed_matchups,
        impact_changed,
    ),
    (
        "Direct changed: 13 vs 15",
        results_direct_changed,
        impact_direct_changed,
    ),
    (
        "Indirect changed: 13 vs 15",
        results_indirect_changed,
        impact_indirect_changed,
    ),
    (
        "Side effects: 13 vs 15",
        results_side_effects,
        impact_side_effects,
    ),
]


for name, value_13, value_15 in cross_checks:

    add_check(
        "Cross Stage",
        name,
        value_13,
        value_15,
        value_13 == value_15,
    )


# ============================================================
# 14. DIRECT TARGET ID CONSISTENCY
# ============================================================

impact_target_ids = set()

for row in impact_direct_rows:

    unit_id = normalize(
        row.get("Unit_ID")
    )

    if unit_id:
        impact_target_ids.add(unit_id)


add_check(
    "Cross Stage",
    "09 direct targets vs 15 direct targets",
    "; ".join(
        sorted(iteration_targets)
    ),
    "; ".join(
        sorted(impact_target_ids)
    ),
    iteration_targets == impact_target_ids,
)


# ============================================================
# 15. ACTUAL MATCHUP CLASSIFICATION CHECK
# ============================================================

actual_changed = 0
actual_direct_changed = 0
actual_indirect_changed = 0
actual_side_effects = 0


for row in impact_matchup_rows:

    changed = (
        normalize(
            row.get("Result_Changed")
        )
        == "Yes"
    )

    impact_type = normalize(
        row.get("Impact_Type")
    )

    side_effect = (
        normalize(
            row.get(
                "Potential_Side_Effect"
            )
        )
        == "Yes"
    )

    if changed:

        actual_changed += 1

        if impact_type == "Direct":
            actual_direct_changed += 1

        elif impact_type == "Indirect":
            actual_indirect_changed += 1

    if side_effect:
        actual_side_effects += 1


add_check(
    "Actual Rows",
    "Changed matchup rows",
    impact_changed,
    actual_changed,
    impact_changed == actual_changed,
)

add_check(
    "Actual Rows",
    "Direct changed matchup rows",
    impact_direct_changed,
    actual_direct_changed,
    impact_direct_changed
    == actual_direct_changed,
)

add_check(
    "Actual Rows",
    "Indirect changed matchup rows",
    impact_indirect_changed,
    actual_indirect_changed,
    impact_indirect_changed
    == actual_indirect_changed,
)

add_check(
    "Actual Rows",
    "Side-effect rows",
    impact_side_effects,
    actual_side_effects,
    impact_side_effects
    == actual_side_effects,
)

add_check(
    "Actual Rows",
    "Side-effect CSV row count",
    impact_side_effects,
    len(impact_side_effect_rows),
    impact_side_effects
    == len(impact_side_effect_rows),
)


# ============================================================
# 16. AVERAGE DISTANCE CONSISTENCY
# ============================================================

results_distance_before = to_float(
    results_summary.get(
        "Average_Distance_From_50_Before"
    )
)

results_distance_after = to_float(
    results_summary.get(
        "Average_Distance_From_50_After"
    )
)

results_distance_change = to_float(
    results_summary.get(
        "Average_Distance_Change"
    )
)

impact_distance_before = to_float(
    impact_summary.get(
        "Average_Distance_From_50_Before"
    )
)

impact_distance_after = to_float(
    impact_summary.get(
        "Average_Distance_From_50_After"
    )
)

impact_distance_change = to_float(
    impact_summary.get(
        "Average_Distance_Change"
    )
)


add_check(
    "Cross Stage",
    "Average distance BEFORE: 13 vs 15",
    results_distance_before,
    impact_distance_before,
    results_distance_before
    == impact_distance_before,
)

add_check(
    "Cross Stage",
    "Average distance AFTER: 13 vs 15",
    results_distance_after,
    impact_distance_after,
    results_distance_after
    == impact_distance_after,
)

add_check(
    "Cross Stage",
    "Average distance change: 13 vs 15",
    results_distance_change,
    impact_distance_change,
    results_distance_change
    == impact_distance_change,
)


# ============================================================
# 17. SOURCE FILE INTEGRITY
# ============================================================

source_hash_after = sha256(
    SOURCE_FILE
)

source_unchanged_now = (
    source_hash_before
    == source_hash_after
)


add_check(
    "Integrity",
    "unit_balance.csv unchanged during validator",
    source_hash_before,
    source_hash_after,
    source_unchanged_now,
)


# ============================================================
# 18. FINAL COUNTERS
# ============================================================

critical_errors = sum(
    1
    for row in checks
    if (
        row["Status"] == "FAIL"
        and row["Severity"] == "Critical"
    )
)

warnings = sum(
    1
    for row in checks
    if (
        row["Status"] == "FAIL"
        and row["Severity"] == "Warning"
    )
)

passed_checks = sum(
    1
    for row in checks
    if row["Status"] == "PASS"
)

failed_checks = sum(
    1
    for row in checks
    if row["Status"] == "FAIL"
)

total_checks = len(checks)


# ============================================================
# 19. PIPELINE STATUS
# ============================================================

if critical_errors == 0:

    pipeline_integrity = "PASS"
    iteration_status = "Validated"

else:

    pipeline_integrity = "FAIL"
    iteration_status = "Needs Review"


# ============================================================
# 20. SUMMARY
# ============================================================

summary_rows = [
    {
        "Metric": "Iteration",
        "Value": ITERATION,
    },
    {
        "Metric": "Total_Checks",
        "Value": total_checks,
    },
    {
        "Metric": "Passed_Checks",
        "Value": passed_checks,
    },
    {
        "Metric": "Failed_Checks",
        "Value": failed_checks,
    },
    {
        "Metric": "Critical_Errors",
        "Value": critical_errors,
    },
    {
        "Metric": "Warnings",
        "Value": warnings,
    },
    {
        "Metric": "Expected_Units",
        "Value": EXPECTED_UNITS,
    },
    {
        "Metric": "Expected_Matchups",
        "Value": EXPECTED_MATCHUPS,
    },
    {
        "Metric": "Direct_Targets",
        "Value": len(iteration_targets),
    },
    {
        "Metric": "Changed_Matchups",
        "Value": actual_changed,
    },
    {
        "Metric": "Direct_Changed_Matchups",
        "Value": actual_direct_changed,
    },
    {
        "Metric": "Indirect_Changed_Matchups",
        "Value": actual_indirect_changed,
    },
    {
        "Metric": "Potential_Side_Effects",
        "Value": actual_side_effects,
    },
    {
        "Metric": "Reproducibility_Status",
        "Value": repro_status,
    },
    {
        "Metric": "Iteration_Effectiveness",
        "Value": iteration_effectiveness,
    },
    {
        "Metric": "Iteration_02_Readiness",
        "Value": iteration_readiness,
    },
    {
        "Metric": "Source_SHA256_Before",
        "Value": source_hash_before,
    },
    {
        "Metric": "Source_SHA256_After",
        "Value": source_hash_after,
    },
    {
        "Metric": "Pipeline_Integrity",
        "Value": pipeline_integrity,
    },
    {
        "Metric": "Iteration_01_Status",
        "Value": iteration_status,
    },
]


# ============================================================
# 21. SAVE
# ============================================================

write_csv(
    VALIDATION_CHECKS_FILE,
    checks,
)

write_csv(
    VALIDATION_SUMMARY_FILE,
    summary_rows,
)


# ============================================================
# 22. TERMINAL OUTPUT
# ============================================================

print()
print("=" * 78)
print("VALIDATION RESULTS")
print("=" * 78)

print()
print(
    "Total checks:",
    total_checks,
)

print(
    "Passed:",
    passed_checks,
)

print(
    "Failed:",
    failed_checks,
)

print(
    "Critical errors:",
    critical_errors,
)

print(
    "Warnings:",
    warnings,
)

print()
print(
    "Direct targets:",
    "; ".join(
        sorted(iteration_targets)
    ),
)

print(
    "Changed matchups:",
    actual_changed,
)

print(
    "Direct changed matchups:",
    actual_direct_changed,
)

print(
    "Indirect changed matchups:",
    actual_indirect_changed,
)

print(
    "Potential side effects:",
    actual_side_effects,
)

print()
print(
    "Reproducibility:",
    repro_status,
)

print(
    "Iteration effectiveness:",
    iteration_effectiveness,
)

print(
    "Iteration 02 readiness:",
    iteration_readiness,
)

print()
print(
    "Pipeline integrity:",
    pipeline_integrity,
)

print(
    "Iteration 01 status:",
    iteration_status,
)


# ============================================================
# 23. FAILED CHECKS
# ============================================================

if failed_checks > 0:

    print()
    print("=" * 78)
    print("FAILED CHECKS")
    print("=" * 78)

    for row in checks:

        if row["Status"] == "FAIL":

            print()
            print(
                "[FAIL]",
                row["Category"],
                "|",
                row["Check"],
            )

            print(
                "Expected:",
                row["Expected"],
            )

            print(
                "Actual  :",
                row["Actual"],
            )


# ============================================================
# 24. FINAL
# ============================================================

print()
print("=" * 78)
print("ITERATION 01 PIPELINE VALIDATION ЗАВЕРШЕНА")
print("=" * 78)

print()
print("Checks:")
print(
    VALIDATION_CHECKS_FILE
)

print()
print("Summary:")
print(
    VALIDATION_SUMMARY_FILE
)

print()
print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)


if critical_errors > 0:

    sys.exit(1)