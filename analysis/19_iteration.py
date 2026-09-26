import csv
import hashlib
import os
import sys
from copy import deepcopy


# ============================================================
# ERA OF STRIFE
# BALANCE ITERATION 02
# ============================================================
#
# Цель:
# проверить дополнительное снижение Damage Stone Ogre,
# не изменяя его HP.
#
# Iteration 01:
# HOR_01 Blade Goblin:
#     Damage = 74.81
#
# HOR_02 Stone Ogre:
#     Damage = 91.20
#
# Iteration 02:
# HOR_01 Blade Goblin:
#     сохраняем изменение Iteration 01
#
# HOR_02 Stone Ogre:
#     Damage 91.20 -> 86.64
#
# Это ещё -5% относительно Iteration 01.
#
# HP Stone Ogre НЕ изменяется.
#
# Важно:
# исходный data/unit_balance.csv не изменяется.
# ============================================================


# ============================================================
# 1. PATHS
# ============================================================

SCRIPT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    SCRIPT_DIR
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
)

RESULTS_DIR = os.path.join(
    SCRIPT_DIR,
    "results",
)

ITERATIONS_DIR = os.path.join(
    RESULTS_DIR,
    "iterations",
)

ITERATION_02_DIR = os.path.join(
    ITERATIONS_DIR,
    "iteration_02",
)

os.makedirs(
    ITERATION_02_DIR,
    exist_ok=True,
)


UNIT_BALANCE_FILE = os.path.join(
    DATA_DIR,
    "unit_balance.csv",
)


ITERATION_01_FILE = os.path.join(
    ITERATIONS_DIR,
    "balance_iteration_01.csv",
)


COMBAT_ENGINE_FILE = os.path.join(
    SCRIPT_DIR,
    "combat_engine.py",
)


MATCHUPS_FILE = os.path.join(
    ITERATION_02_DIR,
    "balance_iteration_02_matchups.csv",
)


UNIT_STATS_FILE = os.path.join(
    ITERATION_02_DIR,
    "balance_iteration_02_unit_statistics.csv",
)


UNIT_COMPARISON_FILE = os.path.join(
    ITERATION_02_DIR,
    "balance_iteration_02_unit_comparison.csv",
)


MATCHUP_COMPARISON_FILE = os.path.join(
    ITERATION_02_DIR,
    "balance_iteration_02_matchup_comparison.csv",
)


CHANGES_FILE = os.path.join(
    ITERATION_02_DIR,
    "balance_iteration_02_changes.csv",
)


SUMMARY_FILE = os.path.join(
    ITERATION_02_DIR,
    "balance_iteration_02_summary.csv",
)


# ============================================================
# 2. IMPORT COMBAT ENGINE
# ============================================================

if SCRIPT_DIR not in sys.path:
    sys.path.insert(
        0,
        SCRIPT_DIR,
    )


from combat_engine import (
    simulate_all_matchups,
    calculate_unit_statistics,
)


# ============================================================
# 3. SETTINGS
# ============================================================

TARGET_WIN_RATE = 50.0

STONE_OGRE_ID = "HOR_02"

BLADE_GOBLIN_ID = "HOR_01"


# Iteration 01 values

BLADE_GOBLIN_ITERATION_01_DAMAGE = 74.81

STONE_OGRE_ITERATION_01_DAMAGE = 91.20


# Iteration 02 candidate:
#
# 91.20 * 0.95 = 86.64

STONE_OGRE_ITERATION_02_DAMAGE = round(
    STONE_OGRE_ITERATION_01_DAMAGE
    * 0.95,
    2,
)


# ============================================================
# 4. HELPERS
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


def write_csv(
    path,
    rows,
    fieldnames=None,
):
    if fieldnames is None:
        if not rows:
            raise ValueError(
                f"Невозможно определить поля "
                f"для пустого CSV: {path}"
            )

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

        writer.writerows(
            rows
        )


def to_float(value):
    if value is None:
        return 0.0

    text = str(value).strip()

    if text == "":
        return 0.0

    return float(
        text.replace(",", ".")
    )


def sha256_file(path):
    sha = hashlib.sha256()

    with open(
        path,
        "rb",
    ) as file:

        while True:
            chunk = file.read(
                1024 * 1024
            )

            if not chunk:
                break

            sha.update(
                chunk
            )

    return sha.hexdigest()


def load_units(path):
    rows = read_csv(
        path
    )

    units = {}

    for row in rows:

        unit_id = row[
            "Unit_ID"
        ].strip()

        units[
            unit_id
        ] = row.copy()

    return units


def matchup_key(row):
    return tuple(
        sorted(
            [
                row["Unit_A_ID"],
                row["Unit_B_ID"],
            ]
        )
    )


def result_for_unit(
    matchup,
    unit_id,
):
    if matchup["Result"] == "Draw":
        return "Draw"

    if matchup["Winner_ID"] == unit_id:
        return "Win"

    return "Loss"


def winner_label(
    matchup,
):
    if matchup["Result"] == "Draw":
        return "Draw"

    return matchup[
        "Winner_ID"
    ]


def distance_from_target(
    value,
):
    return abs(
        to_float(value)
        - TARGET_WIN_RATE
    )


# ============================================================
# 5. INPUT VALIDATION
# ============================================================

required_files = [
    UNIT_BALANCE_FILE,
    COMBAT_ENGINE_FILE,
]


for path in required_files:

    if not os.path.isfile(
        path
    ):
        raise FileNotFoundError(
            "Не найден обязательный файл: "
            + path
        )


# ============================================================
# 6. SOURCE INTEGRITY — BEFORE
# ============================================================

source_hash_before = sha256_file(
    UNIT_BALANCE_FILE
)


# ============================================================
# 7. LOAD BASELINE DATA
# ============================================================

baseline_units = load_units(
    UNIT_BALANCE_FILE
)


if STONE_OGRE_ID not in baseline_units:
    raise KeyError(
        f"{STONE_OGRE_ID} отсутствует "
        f"в unit_balance.csv"
    )


if BLADE_GOBLIN_ID not in baseline_units:
    raise KeyError(
        f"{BLADE_GOBLIN_ID} отсутствует "
        f"в unit_balance.csv"
    )


# ============================================================
# 8. BUILD ITERATION 01 STATE
# ============================================================
#
# Здесь НЕ изменяется исходный CSV.
#
# Создаётся независимая копия baseline.
# Затем в памяти воспроизводятся принятые изменения
# Iteration 01.
# ============================================================

iteration_01_units = deepcopy(
    baseline_units
)


iteration_01_units[
    BLADE_GOBLIN_ID
]["Damage"] = str(
    BLADE_GOBLIN_ITERATION_01_DAMAGE
)


iteration_01_units[
    STONE_OGRE_ID
]["Damage"] = str(
    STONE_OGRE_ITERATION_01_DAMAGE
)


# ============================================================
# 9. BUILD ITERATION 02 STATE
# ============================================================

iteration_02_units = deepcopy(
    iteration_01_units
)


iteration_02_units[
    STONE_OGRE_ID
]["Damage"] = str(
    STONE_OGRE_ITERATION_02_DAMAGE
)


# ============================================================
# 10. RECORD CHANGES
# ============================================================

stone_ogre_hp = to_float(
    iteration_02_units[
        STONE_OGRE_ID
    ]["HP"]
)


stone_ogre_attack_interval = to_float(
    iteration_02_units[
        STONE_OGRE_ID
    ]["Attack_Interval"]
)


if stone_ogre_attack_interval > 0:

    dps_before = (
        STONE_OGRE_ITERATION_01_DAMAGE
        / stone_ogre_attack_interval
    )

    dps_after = (
        STONE_OGRE_ITERATION_02_DAMAGE
        / stone_ogre_attack_interval
    )

else:

    dps_before = 0.0
    dps_after = 0.0


changes_rows = [
    {
        "Iteration":
            "Iteration 02",

        "Unit_ID":
            STONE_OGRE_ID,

        "Unit_Name":
            iteration_02_units[
                STONE_OGRE_ID
            ]["Unit_Name"],

        "Parameter":
            "Damage",

        "Before":
            round(
                STONE_OGRE_ITERATION_01_DAMAGE,
                2,
            ),

        "After":
            round(
                STONE_OGRE_ITERATION_02_DAMAGE,
                2,
            ),

        "Absolute_Change":
            round(
                STONE_OGRE_ITERATION_02_DAMAGE
                - STONE_OGRE_ITERATION_01_DAMAGE,
                2,
            ),

        "Percent_Change":
            round(
                (
                    STONE_OGRE_ITERATION_02_DAMAGE
                    / STONE_OGRE_ITERATION_01_DAMAGE
                    - 1
                )
                * 100,
                2,
            ),

        "HP":
            round(
                stone_ogre_hp,
                2,
            ),

        "DPS_Before":
            round(
                dps_before,
                2,
            ),

        "DPS_After":
            round(
                dps_after,
                2,
            ),

        "Hypothesis":
            (
                "Reduce Stone Ogre offensive power "
                "while preserving its tank durability."
            ),
    }
]


write_csv(
    CHANGES_FILE,
    changes_rows,
)


# ============================================================
# 11. SIMULATE ITERATION 01
# ============================================================

iteration_01_matchups = (
    simulate_all_matchups(
        iteration_01_units
    )
)


iteration_01_statistics = (
    calculate_unit_statistics(
        iteration_01_units,
        iteration_01_matchups,
    )
)


# ============================================================
# 12. SIMULATE ITERATION 02
# ============================================================

iteration_02_matchups = (
    simulate_all_matchups(
        iteration_02_units
    )
)


iteration_02_statistics = (
    calculate_unit_statistics(
        iteration_02_units,
        iteration_02_matchups,
    )
)


# ============================================================
# 13. SAVE ITERATION 02 RAW RESULTS
# ============================================================

write_csv(
    MATCHUPS_FILE,
    iteration_02_matchups,
)


write_csv(
    UNIT_STATS_FILE,
    iteration_02_statistics,
)


# ============================================================
# 14. UNIT COMPARISON
# ============================================================

stats_01_by_id = {
    row["Unit_ID"]: row
    for row in iteration_01_statistics
}


stats_02_by_id = {
    row["Unit_ID"]: row
    for row in iteration_02_statistics
}


unit_comparison_rows = []


for unit_id in baseline_units:

    before = stats_01_by_id[
        unit_id
    ]

    after = stats_02_by_id[
        unit_id
    ]

    before_win_rate = to_float(
        before["Win_Rate"]
    )

    after_win_rate = to_float(
        after["Win_Rate"]
    )

    before_score = to_float(
        before["Combat_Score"]
    )

    after_score = to_float(
        after["Combat_Score"]
    )

    distance_before = abs(
        before_score
        - TARGET_WIN_RATE
    )

    distance_after = abs(
        after_score
        - TARGET_WIN_RATE
    )

    distance_change = (
        distance_after
        - distance_before
    )

    if distance_change < 0:
        balance_result = "Improved"

    elif distance_change > 0:
        balance_result = "Worsened"

    else:
        balance_result = "Unchanged"

    unit_comparison_rows.append(
        {
            "Unit_ID":
                unit_id,

            "Unit_Name":
                after["Unit_Name"],

            "Role":
                after["Role"],

            "Is_Direct_Target":
                (
                    "Yes"
                    if unit_id
                    == STONE_OGRE_ID
                    else "No"
                ),

            "Wins_Before":
                before["Wins"],

            "Wins_After":
                after["Wins"],

            "Losses_Before":
                before["Losses"],

            "Losses_After":
                after["Losses"],

            "Draws_Before":
                before["Draws"],

            "Draws_After":
                after["Draws"],

            "Win_Rate_Before":
                round(
                    before_win_rate,
                    2,
                ),

            "Win_Rate_After":
                round(
                    after_win_rate,
                    2,
                ),

            "Win_Rate_Delta":
                round(
                    after_win_rate
                    - before_win_rate,
                    2,
                ),

            "Combat_Score_Before":
                round(
                    before_score,
                    2,
                ),

            "Combat_Score_After":
                round(
                    after_score,
                    2,
                ),

            "Combat_Score_Delta":
                round(
                    after_score
                    - before_score,
                    2,
                ),

            "Distance_From_50_Before":
                round(
                    distance_before,
                    2,
                ),

            "Distance_From_50_After":
                round(
                    distance_after,
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


write_csv(
    UNIT_COMPARISON_FILE,
    unit_comparison_rows,
)


# ============================================================
# 15. MATCHUP COMPARISON
# ============================================================

matchups_01_by_key = {
    matchup_key(row): row
    for row in iteration_01_matchups
}


matchups_02_by_key = {
    matchup_key(row): row
    for row in iteration_02_matchups
}


matchup_comparison_rows = []


for key in sorted(
    matchups_01_by_key.keys()
):

    before = matchups_01_by_key[
        key
    ]

    after = matchups_02_by_key[
        key
    ]

    before_winner = winner_label(
        before
    )

    after_winner = winner_label(
        after
    )

    changed = (
        before_winner
        != after_winner
    )

    contains_stone_ogre = (
        STONE_OGRE_ID
        in key
    )

    if changed and contains_stone_ogre:
        impact_type = "Direct"

    elif changed:
        impact_type = "Indirect"

    else:
        impact_type = "Unchanged"

    matchup_comparison_rows.append(
        {
            "Unit_1_ID":
                key[0],

            "Unit_1_Name":
                iteration_02_units[
                    key[0]
                ]["Unit_Name"],

            "Unit_2_ID":
                key[1],

            "Unit_2_Name":
                iteration_02_units[
                    key[1]
                ]["Unit_Name"],

            "Contains_Direct_Target":
                (
                    "Yes"
                    if contains_stone_ogre
                    else "No"
                ),

            "Winner_Before":
                before_winner,

            "Winner_After":
                after_winner,

            "Result_Changed":
                (
                    "Yes"
                    if changed
                    else "No"
                ),

            "Impact_Type":
                impact_type,

            "Combat_Time_Before":
                before[
                    "Combat_Time"
                ],

            "Combat_Time_After":
                after[
                    "Combat_Time"
                ],

            "Combat_Time_Delta":
                round(
                    to_float(
                        after[
                            "Combat_Time"
                        ]
                    )
                    - to_float(
                        before[
                            "Combat_Time"
                        ]
                    ),
                    6,
                ),
        }
    )


write_csv(
    MATCHUP_COMPARISON_FILE,
    matchup_comparison_rows,
)


# ============================================================
# 16. SUMMARY METRICS
# ============================================================

changed_matchups = [
    row
    for row
    in matchup_comparison_rows
    if row[
        "Result_Changed"
    ] == "Yes"
]


direct_changed_matchups = [
    row
    for row
    in changed_matchups
    if row[
        "Impact_Type"
    ] == "Direct"
]


indirect_changed_matchups = [
    row
    for row
    in changed_matchups
    if row[
        "Impact_Type"
    ] == "Indirect"
]


improved_units = [
    row
    for row
    in unit_comparison_rows
    if row[
        "Balance_Result"
    ] == "Improved"
]


worsened_units = [
    row
    for row
    in unit_comparison_rows
    if row[
        "Balance_Result"
    ] == "Worsened"
]


unchanged_units = [
    row
    for row
    in unit_comparison_rows
    if row[
        "Balance_Result"
    ] == "Unchanged"
]


stone_ogre_before = stats_01_by_id[
    STONE_OGRE_ID
]


stone_ogre_after = stats_02_by_id[
    STONE_OGRE_ID
]


stone_ogre_score_before = to_float(
    stone_ogre_before[
        "Combat_Score"
    ]
)


stone_ogre_score_after = to_float(
    stone_ogre_after[
        "Combat_Score"
    ]
)


stone_ogre_distance_before = abs(
    stone_ogre_score_before
    - TARGET_WIN_RATE
)


stone_ogre_distance_after = abs(
    stone_ogre_score_after
    - TARGET_WIN_RATE
)


average_distance_before = (
    sum(
        abs(
            to_float(
                row[
                    "Combat_Score_Before"
                ]
            )
            - TARGET_WIN_RATE
        )
        for row
        in unit_comparison_rows
    )
    / len(
        unit_comparison_rows
    )
)


average_distance_after = (
    sum(
        abs(
            to_float(
                row[
                    "Combat_Score_After"
                ]
            )
            - TARGET_WIN_RATE
        )
        for row
        in unit_comparison_rows
    )
    / len(
        unit_comparison_rows
    )
)


# ============================================================
# 17. EXPERIMENT INTERPRETATION
# ============================================================

stone_ogre_improved = (
    stone_ogre_distance_after
    < stone_ogre_distance_before
)


if (
    stone_ogre_improved
    and len(
        indirect_changed_matchups
    ) == 0
):

    iteration_result = (
        "Promising"
    )

    recommendation = (
        "Keep Iteration 02 candidate for further validation."
    )


elif stone_ogre_improved:

    iteration_result = (
        "Promising With Side Effects"
    )

    recommendation = (
        "Investigate indirect matchup changes "
        "before accepting Iteration 02."
    )


elif (
    stone_ogre_distance_after
    == stone_ogre_distance_before
):

    iteration_result = (
        "No Meaningful Improvement"
    )

    recommendation = (
        "Damage-only tuning did not move Stone Ogre "
        "closer to the target. "
        "Consider ability-level tuning next."
    )


else:

    iteration_result = (
        "Worsened"
    )

    recommendation = (
        "Reject this candidate and test another "
        "Stone Ogre tuning direction."
    )


# ============================================================
# 18. SUMMARY CSV
# ============================================================

summary_rows = [
    {
        "Metric":
            "Iteration",

        "Value":
            "Iteration 02",
    },

    {
        "Metric":
            "Direct_Target",

        "Value":
            STONE_OGRE_ID,
    },

    {
        "Metric":
            "Parameter",

        "Value":
            "Damage",
    },

    {
        "Metric":
            "Damage_Before",

        "Value":
            round(
                STONE_OGRE_ITERATION_01_DAMAGE,
                2,
            ),
    },

    {
        "Metric":
            "Damage_After",

        "Value":
            round(
                STONE_OGRE_ITERATION_02_DAMAGE,
                2,
            ),
    },

    {
        "Metric":
            "HP",

        "Value":
            round(
                stone_ogre_hp,
                2,
            ),
    },

    {
        "Metric":
            "DPS_Before",

        "Value":
            round(
                dps_before,
                2,
            ),
    },

    {
        "Metric":
            "DPS_After",

        "Value":
            round(
                dps_after,
                2,
            ),
    },

    {
        "Metric":
            "Stone_Ogre_Combat_Score_Before",

        "Value":
            round(
                stone_ogre_score_before,
                2,
            ),
    },

    {
        "Metric":
            "Stone_Ogre_Combat_Score_After",

        "Value":
            round(
                stone_ogre_score_after,
                2,
            ),
    },

    {
        "Metric":
            "Stone_Ogre_Distance_From_50_Before",

        "Value":
            round(
                stone_ogre_distance_before,
                2,
            ),
    },

    {
        "Metric":
            "Stone_Ogre_Distance_From_50_After",

        "Value":
            round(
                stone_ogre_distance_after,
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
                average_distance_after
                - average_distance_before,
                2,
            ),
    },

    {
        "Metric":
            "Iteration_Result",

        "Value":
            iteration_result,
    },

    {
        "Metric":
            "Recommendation",

        "Value":
            recommendation,
    },
]


write_csv(
    SUMMARY_FILE,
    summary_rows,
    fieldnames=[
        "Metric",
        "Value",
    ],
)


# ============================================================
# 19. SOURCE INTEGRITY — AFTER
# ============================================================

source_hash_after = sha256_file(
    UNIT_BALANCE_FILE
)


source_unchanged = (
    source_hash_before
    == source_hash_after
)


if not source_unchanged:

    raise RuntimeError(
        "ОШИБКА: исходный "
        "data/unit_balance.csv был изменён."
    )


# ============================================================
# 20. TERMINAL REPORT
# ============================================================

print()
print(
    "=" * 72
)

print(
    "ERA OF STRIFE — BALANCE ITERATION 02"
)

print(
    "=" * 72
)

print()

print(
    "Hypothesis:"
)

print(
    "Reduce Stone Ogre offensive power "
    "while preserving tank durability."
)

print()

print(
    "Stone Ogre:"
)

print(
    f"  HP: "
    f"{stone_ogre_hp:.2f} "
    f"(unchanged)"
)

print(
    f"  Damage: "
    f"{STONE_OGRE_ITERATION_01_DAMAGE:.2f}"
    f" -> "
    f"{STONE_OGRE_ITERATION_02_DAMAGE:.2f}"
)

print(
    f"  DPS: "
    f"{dps_before:.2f}"
    f" -> "
    f"{dps_after:.2f}"
)

print()

print(
    "Stone Ogre Combat Score:"
)

print(
    f"  Before: "
    f"{stone_ogre_score_before:.2f}%"
)

print(
    f"  After:  "
    f"{stone_ogre_score_after:.2f}%"
)

print()

print(
    "Matchups:"
)

print(
    f"  Total: "
    f"{len(iteration_02_matchups)}"
)

print(
    f"  Changed: "
    f"{len(changed_matchups)}"
)

print(
    f"  Direct changed: "
    f"{len(direct_changed_matchups)}"
)

print(
    f"  Indirect changed: "
    f"{len(indirect_changed_matchups)}"
)

print()

print(
    "Overall balance:"
)

print(
    f"  Average distance from 50% BEFORE: "
    f"{average_distance_before:.2f}"
)

print(
    f"  Average distance from 50% AFTER:  "
    f"{average_distance_after:.2f}"
)

print(
    f"  Delta: "
    f"{average_distance_after - average_distance_before:+.2f}"
)

print()

print(
    f"Iteration result: "
    f"{iteration_result}"
)

print(
    f"Recommendation: "
    f"{recommendation}"
)

print()

print(
    "Generated files:"
)

for path in [
    CHANGES_FILE,
    MATCHUPS_FILE,
    UNIT_STATS_FILE,
    UNIT_COMPARISON_FILE,
    MATCHUP_COMPARISON_FILE,
    SUMMARY_FILE,
]:

    print(
        " ",
        os.path.relpath(
            path,
            PROJECT_ROOT,
        ),
    )

print()

print(
    "SOURCE INTEGRITY"
)

print(
    f"SHA-256 before: "
    f"{source_hash_before}"
)

print(
    f"SHA-256 after:  "
    f"{source_hash_after}"
)

print(
    "Source unchanged:",
    (
        "Yes"
        if source_unchanged
        else "No"
    ),
)

print()

print(
    "=" * 72
)

print(
    "BALANCE ITERATION 02 ЗАВЕРШЕНА"
)

print(
    "=" * 72
)

print()

print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)