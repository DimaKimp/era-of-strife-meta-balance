import csv
import os


# ============================================================
# 1. PATHS
# ============================================================

SCRIPT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    SCRIPT_DIR
)

RESULTS_DIR = os.path.join(
    SCRIPT_DIR,
    "results",
)

ITERATIONS_DIR = os.path.join(
    RESULTS_DIR,
    "iterations",
)

SENSITIVITY_DIR = os.path.join(
    ITERATIONS_DIR,
    "sensitivity",
)

SOURCE_FILE = os.path.join(
    SENSITIVITY_DIR,
    "stone_ogre_hp_sensitivity_results.csv",
)

DETAIL_FILE = os.path.join(
    SENSITIVITY_DIR,
    "stone_ogre_hp_threshold_refinement.csv",
)

SUMMARY_FILE = os.path.join(
    SENSITIVITY_DIR,
    "stone_ogre_hp_threshold_refinement_summary.csv",
)


# ============================================================
# 2. SETTINGS
# ============================================================

TESTED_UNIT_ID = "HOR_02"
TESTED_UNIT_NAME = "Stone Ogre"

OPPONENT_ID = "ELF_01"
OPPONENT_NAME = "Elven Swordsman"

HP_STEP = 1


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

def read_csv(file_path):
    """
    Читает CSV-файл и возвращает список словарей.
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


def write_csv(
    file_path,
    rows,
    fieldnames,
):
    """
    Записывает список словарей в CSV-файл.
    """

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
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def safe_float(value):
    """
    Безопасно преобразует значение в float.
    """

    try:
        return float(value)
    except (
        TypeError,
        ValueError,
    ):
        return None


def safe_int(value):
    """
    Безопасно преобразует значение в int.
    """

    number = safe_float(value)

    if number is None:
        return None

    return int(round(number))


def normalize_text(value):
    """
    Приводит текст к удобному виду.
    """

    if value is None:
        return ""

    return str(value).strip()


def get_result(row):
    """
    Получает результат Stone Ogre.

    В sensitivity_results.csv поле Result уже описывает
    результат Stone Ogre:

    Win  - Stone Ogre победил;
    Draw - ничья;
    Loss - Stone Ogre проиграл.
    """

    result = normalize_text(
        row.get("Result")
    )

    if result:
        return result

    control_result = normalize_text(
        row.get("Control_Result")
    )

    return control_result


def result_rank(result):
    """
    Числовой порядок результатов нужен только для удобства:

    Loss = 0
    Draw = 1
    Win  = 2
    """

    ranks = {
        "Loss": 0,
        "Draw": 1,
        "Win": 2,
    }

    return ranks.get(
        result,
        -1,
    )


# ============================================================
# 4. CHECK INPUT FILE
# ============================================================

if not os.path.exists(SOURCE_FILE):
    raise FileNotFoundError(
        "Не найден файл:\n"
        f"{SOURCE_FILE}\n\n"
        "Сначала необходимо выполнить "
        "17_stone_ogre_sensitivity_analysis.py."
    )


# ============================================================
# 5. LOAD SENSITIVITY RESULTS
# ============================================================

all_rows = read_csv(
    SOURCE_FILE
)

if not all_rows:
    raise ValueError(
        "stone_ogre_hp_sensitivity_results.csv пуст."
    )


# ============================================================
# 6. FILTER ELF_01 MATCHUP
# ============================================================

opponent_rows = []

for row in all_rows:

    opponent_id = normalize_text(
        row.get("Opponent_ID")
    )

    if opponent_id != OPPONENT_ID:
        continue

    hp = safe_int(
        row.get("Ogre_HP")
    )

    if hp is None:
        continue

    result = get_result(row)

    if result not in {
        "Win",
        "Draw",
        "Loss",
    }:
        continue

    copied_row = dict(row)

    copied_row["_HP"] = hp
    copied_row["_Result"] = result

    opponent_rows.append(
        copied_row
    )


if not opponent_rows:
    raise ValueError(
        f"В {os.path.basename(SOURCE_FILE)} "
        f"не найдены результаты против {OPPONENT_ID}."
    )


# ============================================================
# 7. SORT BY HP
# ============================================================

opponent_rows.sort(
    key=lambda row: row["_HP"]
)


# ============================================================
# 8. CREATE HP -> RESULT MAP
# ============================================================

coarse_result_by_hp = {}

for row in opponent_rows:

    hp = row["_HP"]
    result = row["_Result"]

    coarse_result_by_hp[hp] = result


coarse_hp_values = sorted(
    coarse_result_by_hp.keys()
)


# ============================================================
# 9. DETECT COARSE TRANSITIONS
# ============================================================

coarse_transitions = []

for index in range(
    1,
    len(coarse_hp_values),
):

    previous_hp = coarse_hp_values[
        index - 1
    ]

    current_hp = coarse_hp_values[
        index
    ]

    previous_result = (
        coarse_result_by_hp[
            previous_hp
        ]
    )

    current_result = (
        coarse_result_by_hp[
            current_hp
        ]
    )

    if previous_result == current_result:
        continue

    transition = {
        "Lower_HP": previous_hp,
        "Lower_Result": previous_result,
        "Upper_HP": current_hp,
        "Upper_Result": current_result,
    }

    coarse_transitions.append(
        transition
    )


# ============================================================
# 10. PRINT COARSE RESULTS
# ============================================================

print()
print(
    "=" * 70
)

print(
    "STONE OGRE HP THRESHOLD REFINEMENT"
)

print(
    "=" * 70
)

print()

print(
    f"Tested unit: "
    f"{TESTED_UNIT_ID} - "
    f"{TESTED_UNIT_NAME}"
)

print(
    f"Opponent: "
    f"{OPPONENT_ID} - "
    f"{OPPONENT_NAME}"
)

print()

print(
    "Coarse sensitivity results:"
)

for hp in sorted(
    coarse_hp_values,
    reverse=True,
):

    print(
        f"HP {hp}: "
        f"{coarse_result_by_hp[hp]}"
    )


print()

print(
    "Detected coarse transitions:"
)

if coarse_transitions:

    for transition in coarse_transitions:

        print(
            f"{transition['Lower_HP']} HP "
            f"({transition['Lower_Result']}) "
            f"-> "
            f"{transition['Upper_HP']} HP "
            f"({transition['Upper_Result']})"
        )

else:

    print(
        "No transitions detected."
    )


# ============================================================
# 11. IMPORTANT NOTE ABOUT REFINEMENT
# ============================================================

"""
В текущем проекте sensitivity_results.csv уже содержит результаты
только для заранее протестированных значений HP.

Поэтому этот скрипт НЕ выдумывает результаты для отсутствующих HP.

Если между 1725 и 1750 в исходном sensitivity-файле нет значений
1726, 1727, ..., 1749, то мы можем честно установить только интервал,
внутри которого находится breakpoint.

Чтобы получить точный breakpoint с шагом 1 HP, нужно реально
прогнать combat simulation для каждого HP внутри интервала.

Ниже поэтому формируются:

1. обнаруженные интервалы переходов;
2. список HP, которые необходимо дополнительно протестировать;
3. максимально точный вывод, который поддерживается текущими данными.
"""


# ============================================================
# 12. BUILD REFINEMENT PLAN
# ============================================================

refinement_rows = []

transition_number = 0

for transition in coarse_transitions:

    transition_number += 1

    lower_hp = transition[
        "Lower_HP"
    ]

    upper_hp = transition[
        "Upper_HP"
    ]

    lower_result = transition[
        "Lower_Result"
    ]

    upper_result = transition[
        "Upper_Result"
    ]

    interval_size = (
        upper_hp - lower_hp
    )

    missing_hp_values = []

    for hp in range(
        lower_hp + HP_STEP,
        upper_hp,
        HP_STEP,
    ):

        if hp not in coarse_result_by_hp:
            missing_hp_values.append(
                hp
            )

    if interval_size <= HP_STEP:

        exact_status = "Exact"

        breakpoint_description = (
            f"Result changes between "
            f"{lower_hp} HP "
            f"({lower_result}) and "
            f"{upper_hp} HP "
            f"({upper_result})."
        )

    else:

        exact_status = (
            "Requires additional simulation"
        )

        breakpoint_description = (
            f"Breakpoint is inside "
            f"{lower_hp}-{upper_hp} HP: "
            f"{lower_result} -> "
            f"{upper_result}."
        )

    refinement_rows.append(
        {
            "Transition_ID":
                transition_number,

            "Tested_Unit_ID":
                TESTED_UNIT_ID,

            "Tested_Unit_Name":
                TESTED_UNIT_NAME,

            "Opponent_ID":
                OPPONENT_ID,

            "Opponent_Name":
                OPPONENT_NAME,

            "Lower_HP":
                lower_hp,

            "Lower_Result":
                lower_result,

            "Upper_HP":
                upper_hp,

            "Upper_Result":
                upper_result,

            "Interval_Size":
                interval_size,

            "HP_Step":
                HP_STEP,

            "Missing_HP_Count":
                len(
                    missing_hp_values
                ),

            "Missing_HP_Values":
                "; ".join(
                    str(hp)
                    for hp
                    in missing_hp_values
                ),

            "Threshold_Status":
                exact_status,

            "Interpretation":
                breakpoint_description,
        }
    )


# ============================================================
# 13. WRITE DETAILED TRANSITION FILE
# ============================================================

detail_fieldnames = [
    "Transition_ID",
    "Tested_Unit_ID",
    "Tested_Unit_Name",
    "Opponent_ID",
    "Opponent_Name",
    "Lower_HP",
    "Lower_Result",
    "Upper_HP",
    "Upper_Result",
    "Interval_Size",
    "HP_Step",
    "Missing_HP_Count",
    "Missing_HP_Values",
    "Threshold_Status",
    "Interpretation",
]

write_csv(
    DETAIL_FILE,
    refinement_rows,
    detail_fieldnames,
)


# ============================================================
# 14. BUILD SUMMARY
# ============================================================

unique_results = sorted(
    {
        coarse_result_by_hp[hp]
        for hp in coarse_hp_values
    },
    key=result_rank,
)


win_hp_values = [
    hp
    for hp in coarse_hp_values
    if coarse_result_by_hp[hp]
    == "Win"
]

draw_hp_values = [
    hp
    for hp in coarse_hp_values
    if coarse_result_by_hp[hp]
    == "Draw"
]

loss_hp_values = [
    hp
    for hp in coarse_hp_values
    if coarse_result_by_hp[hp]
    == "Loss"
]


summary_rows = [
    {
        "Metric": "Tested_Unit_ID",
        "Value": TESTED_UNIT_ID,
    },
    {
        "Metric": "Tested_Unit_Name",
        "Value": TESTED_UNIT_NAME,
    },
    {
        "Metric": "Opponent_ID",
        "Value": OPPONENT_ID,
    },
    {
        "Metric": "Opponent_Name",
        "Value": OPPONENT_NAME,
    },
    {
        "Metric": "Minimum_Tested_HP",
        "Value": min(
            coarse_hp_values
        ),
    },
    {
        "Metric": "Maximum_Tested_HP",
        "Value": max(
            coarse_hp_values
        ),
    },
    {
        "Metric": "Tested_HP_Count",
        "Value": len(
            coarse_hp_values
        ),
    },
    {
        "Metric": "Unique_Results",
        "Value": "; ".join(
            unique_results
        ),
    },
    {
        "Metric": "Transition_Count",
        "Value": len(
            coarse_transitions
        ),
    },
]


if win_hp_values:

    summary_rows.append(
        {
            "Metric":
                "Lowest_Tested_HP_With_Win",

            "Value":
                min(win_hp_values),
        }
    )


if draw_hp_values:

    summary_rows.append(
        {
            "Metric":
                "Lowest_Tested_HP_With_Draw",

            "Value":
                min(draw_hp_values),
        }
    )

    summary_rows.append(
        {
            "Metric":
                "Highest_Tested_HP_With_Draw",

            "Value":
                max(draw_hp_values),
        }
    )


if loss_hp_values:

    summary_rows.append(
        {
            "Metric":
                "Highest_Tested_HP_With_Loss",

            "Value":
                max(loss_hp_values),
        }
    )


# ============================================================
# 15. ADD EACH TRANSITION TO SUMMARY
# ============================================================

for index, transition in enumerate(
    coarse_transitions,
    start=1,
):

    lower_hp = transition[
        "Lower_HP"
    ]

    upper_hp = transition[
        "Upper_HP"
    ]

    lower_result = transition[
        "Lower_Result"
    ]

    upper_result = transition[
        "Upper_Result"
    ]

    summary_rows.append(
        {
            "Metric":
                f"Transition_{index}",

            "Value":
                (
                    f"{lower_hp} HP "
                    f"{lower_result} -> "
                    f"{upper_hp} HP "
                    f"{upper_result}"
                ),
        }
    )

    summary_rows.append(
        {
            "Metric":
                f"Transition_{index}_Interval",

            "Value":
                f"{lower_hp}-{upper_hp}",
        }
    )

    summary_rows.append(
        {
            "Metric":
                f"Transition_{index}_Exact_Threshold_Known",

            "Value":
                (
                    "Yes"
                    if upper_hp - lower_hp
                    <= HP_STEP
                    else "No"
                ),
        }
    )


# ============================================================
# 16. INTERPRETATION
# ============================================================

if len(coarse_transitions) == 0:

    interpretation = (
        "No matchup-result transition was detected "
        "for Elven Swordsman inside the tested "
        "Stone Ogre HP range."
    )

elif len(coarse_transitions) == 1:

    interpretation = (
        "One Stone Ogre HP breakpoint interval "
        "was detected against Elven Swordsman."
    )

else:

    interpretation = (
        f"{len(coarse_transitions)} Stone Ogre HP "
        "breakpoint intervals were detected against "
        "Elven Swordsman. "
        "Additional 1-HP combat simulations are "
        "required to determine exact breakpoints."
    )


summary_rows.append(
    {
        "Metric": "Interpretation",
        "Value": interpretation,
    }
)


# ============================================================
# 17. WRITE SUMMARY
# ============================================================

write_csv(
    SUMMARY_FILE,
    summary_rows,
    [
        "Metric",
        "Value",
    ],
)


# ============================================================
# 18. FINAL CONSOLE OUTPUT
# ============================================================

print()

print(
    "-" * 70
)

print(
    "REFINEMENT RESULT"
)

print(
    "-" * 70
)

print()

print(
    f"Unique results: "
    f"{', '.join(unique_results)}"
)

print(
    f"Transitions detected: "
    f"{len(coarse_transitions)}"
)

print()


for index, transition in enumerate(
    coarse_transitions,
    start=1,
):

    lower_hp = transition[
        "Lower_HP"
    ]

    upper_hp = transition[
        "Upper_HP"
    ]

    lower_result = transition[
        "Lower_Result"
    ]

    upper_result = transition[
        "Upper_Result"
    ]

    print(
        f"Transition {index}:"
    )

    print(
        f"  {lower_hp} HP: "
        f"{lower_result}"
    )

    print(
        f"  {upper_hp} HP: "
        f"{upper_result}"
    )

    print(
        f"  Breakpoint interval: "
        f"{lower_hp}-{upper_hp} HP"
    )

    if (
        upper_hp - lower_hp
        > HP_STEP
    ):

        print(
            "  Exact breakpoint: "
            "requires additional "
            "1-HP simulations"
        )

    else:

        print(
            "  Exact breakpoint interval "
            "has been identified."
        )

    print()


print(
    "-" * 70
)

print(
    "FILES"
)

print(
    "-" * 70
)

print()

print(
    "Detailed results:"
)

print(
    os.path.relpath(
        DETAIL_FILE,
        PROJECT_ROOT,
    )
)

print()

print(
    "Summary:"
)

print(
    os.path.relpath(
        SUMMARY_FILE,
        PROJECT_ROOT,
    )
)

print()

print(
    "=" * 70
)

print(
    "STONE OGRE HP THRESHOLD REFINEMENT ЗАВЕРШЁН"
)

print(
    "=" * 70
)

print()

print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)