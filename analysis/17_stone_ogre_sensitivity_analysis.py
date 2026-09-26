from __future__ import annotations

import copy
import csv
import hashlib
import os
import sys
from pathlib import Path
from typing import Any

from combat_engine import simulate_combat


# ============================================================
# ERA OF STRIFE
# 17 — STONE OGRE HP SENSITIVITY ANALYSIS
# ============================================================
#
# Цель:
#
# Исследовать чувствительность результатов HOR_02 Stone Ogre
# к изменению его HP после Balance Iteration 01.
#
# ВАЖНО:
#
# 1. data/unit_balance.csv НЕ изменяется.
# 2. Используется общий analysis/combat_engine.py.
# 3. Все остальные изменения Iteration 01 сохраняются.
# 4. Меняется только HP Stone Ogre.
# 5. Контрольная точка AFTER Iteration 01:
#
#       HOR_02 HP = 1760
#
# 6. Для каждого HP Ogre проводится 11 боёв —
#    по одному против каждого другого юнита.
#
# 7. Дополнительно определяется первый обнаруженный
#    порог изменения каждого matchup.
#
# ============================================================


# ============================================================
# 1. ПУТИ
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

ANALYSIS_DIR = PROJECT_ROOT / "analysis"

RESULTS_DIR = (
    ANALYSIS_DIR
    / "results"
    / "iterations"
)

SENSITIVITY_DIR = (
    RESULTS_DIR
    / "sensitivity"
)

SOURCE_FILE = (
    DATA_DIR
    / "unit_balance.csv"
)

ITERATION_FILE = (
    RESULTS_DIR
    / "balance_iteration_01.csv"
)

DETAILED_RESULTS_FILE = (
    SENSITIVITY_DIR
    / "stone_ogre_hp_sensitivity_results.csv"
)

SUMMARY_FILE = (
    SENSITIVITY_DIR
    / "stone_ogre_hp_sensitivity_summary.csv"
)

THRESHOLDS_FILE = (
    SENSITIVITY_DIR
    / "stone_ogre_hp_thresholds.csv"
)


# ============================================================
# 2. НАСТРОЙКИ АНАЛИЗА
# ============================================================

TARGET_UNIT_ID = "HOR_02"

TARGET_UNIT_NAME = "Stone Ogre"

CONTROL_HP = 1760.0


# Проверяем диапазон от текущего AFTER вниз.
#
# Более мелкий шаг около исходного значения нужен,
# чтобы не пропустить ранний порог переключения matchup.

HP_VALUES = [
    1760.0,
    1750.0,
    1725.0,
    1700.0,
    1675.0,
    1650.0,
    1625.0,
    1600.0,
]


# ============================================================
# 3. СЛУЖЕБНЫЕ ФУНКЦИИ
# ============================================================

def to_float(
    value: Any,
) -> float:
    """
    Безопасно преобразует число из CSV в float.

    Поддерживает:
    10
    10.5
    10,5
    """

    if value is None:
        return 0.0

    value = str(value).strip()

    if value == "":
        return 0.0

    return float(
        value.replace(",", ".")
    )


def normalize_number(
    value: float,
) -> str:
    """
    Красиво записывает число для CSV.

    1760.0 -> 1760
    1675.0 -> 1675
    91.2   -> 91.2
    """

    if float(value).is_integer():
        return str(
            int(value)
        )

    return str(
        round(value, 6)
    )


def file_sha256(
    file_path: Path,
) -> str:
    """
    Рассчитывает SHA-256 файла.

    Используется для доказательства того,
    что data/unit_balance.csv не был изменён.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb",
    ) as file:

        while True:

            chunk = file.read(
                1024 * 1024
            )

            if not chunk:
                break

            sha256.update(
                chunk
            )

    return sha256.hexdigest()


def read_csv(
    file_path: Path,
) -> list[dict[str, str]]:
    """
    Читает CSV в список словарей.
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
    file_path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> None:
    """
    Записывает список словарей в CSV.
    """

    file_path.parent.mkdir(
        parents=True,
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

            writer.writerow(
                row
            )


# ============================================================
# 4. ПРОВЕРКА ВХОДНЫХ ФАЙЛОВ
# ============================================================

if not SOURCE_FILE.exists():

    raise FileNotFoundError(
        "Не найден исходный файл: "
        f"{SOURCE_FILE}"
    )


if not ITERATION_FILE.exists():

    raise FileNotFoundError(
        "Не найден файл Iteration 01: "
        f"{ITERATION_FILE}"
    )


# ============================================================
# 5. SHA-256 ДО АНАЛИЗА
# ============================================================

source_hash_before = file_sha256(
    SOURCE_FILE
)


# ============================================================
# 6. ЗАГРУЗКА BASELINE
# ============================================================

source_rows = read_csv(
    SOURCE_FILE
)


units: dict[
    str,
    dict[str, Any],
] = {}


for row in source_rows:

    unit_id = row[
        "Unit_ID"
    ].strip()

    units[
        unit_id
    ] = row.copy()


if TARGET_UNIT_ID not in units:

    raise ValueError(
        f"Юнит {TARGET_UNIT_ID} "
        "не найден в unit_balance.csv."
    )


# ============================================================
# 7. ЗАГРУЗКА ITERATION 01
# ============================================================

iteration_rows = read_csv(
    ITERATION_FILE
)


# ============================================================
# 8. ПРИМЕНЕНИЕ DIRECT CHANGES ITERATION 01
# ============================================================
#
# Нам нужен именно AFTER Iteration 01.
#
# Поэтому сначала создаём независимую копию baseline,
# затем применяем изменения Iteration 01.
#
# После этого sensitivity test будет менять
# ТОЛЬКО HP HOR_02.
# ============================================================

after_units = copy.deepcopy(
    units
)


def first_value(
    row: dict[str, Any],
    names: list[str],
) -> str:
    """
    Возвращает первое найденное непустое поле.
    """

    for name in names:

        if name not in row:
            continue

        value = str(
            row.get(
                name,
                "",
            )
        ).strip()

        if value != "":
            return value

    return ""


direct_changes_applied = 0


for row in iteration_rows:

    unit_id = first_value(
        row,
        [
            "Unit_ID",
            "Target_Unit_ID",
        ],
    )

    if (
        unit_id == ""
        or unit_id not in after_units
    ):
        continue

    parameter = first_value(
        row,
        [
            "Parameter",
            "Changed_Parameter",
            "Target_Parameter",
        ],
    )

    after_value = first_value(
        row,
        [
            "After_Value",
            "New_Value",
            "After",
        ],
    )

    # --------------------------------------------------------
    # Fallback для структуры Iteration 01,
    # где параметры могут лежать непосредственно
    # в отдельных столбцах.
    # --------------------------------------------------------

    if (
        parameter != ""
        and after_value != ""
    ):

        after_units[
            unit_id
        ][parameter] = after_value

        direct_changes_applied += 1

        continue

    # --------------------------------------------------------
    # Поддержка нашей текущей Iteration 01:
    # Damage / DPS и аналогичные BEFORE/AFTER-поля.
    # --------------------------------------------------------

    possible_parameters = [
        "HP",
        "Damage",
        "Attack_Interval",
        "DPS",
        "Attack_Range",
        "Move_Speed",
        "Cost",
    ]

    for parameter_name in possible_parameters:

        after_column_candidates = [
            f"After_{parameter_name}",
            f"{parameter_name}_After",
            f"New_{parameter_name}",
        ]

        new_value = first_value(
            row,
            after_column_candidates,
        )

        if new_value == "":
            continue

        after_units[
            unit_id
        ][parameter_name] = new_value

        direct_changes_applied += 1


# ============================================================
# 9. КОНТРОЛЬ AFTER STONE OGRE
# ============================================================
#
# HP в Iteration 01 мы не меняли.
#
# Поэтому он должен остаться 1760.
# ============================================================

ogre_after = after_units[
    TARGET_UNIT_ID
]


actual_control_hp = to_float(
    ogre_after["HP"]
)


if actual_control_hp != CONTROL_HP:

    raise ValueError(
        "Контрольный HP Stone Ogre не совпадает "
        "с ожидаемым AFTER Iteration 01.\n"
        f"Ожидалось: {CONTROL_HP}\n"
        f"Получено: {actual_control_hp}"
    )


# ============================================================
# 10. ФУНКЦИЯ ПРЕДСТАВЛЕНИЯ РЕЗУЛЬТАТА
# ============================================================

def result_for_unit(
    combat_result: dict[str, Any],
    unit_id: str,
) -> str:
    """
    Возвращает результат с точки зрения конкретного юнита:

    Win
    Loss
    Draw
    """

    if combat_result[
        "Result"
    ] == "Draw":

        return "Draw"

    if combat_result[
        "Winner_ID"
    ] == unit_id:

        return "Win"

    return "Loss"


def remaining_hp_for_unit(
    combat_result: dict[str, Any],
    unit_id: str,
) -> float:
    """
    Возвращает Remaining HP указанного юнита.
    """

    if (
        combat_result[
            "Unit_A_ID"
        ]
        == unit_id
    ):

        return to_float(
            combat_result[
                "Unit_A_Remaining_HP"
            ]
        )

    return to_float(
        combat_result[
            "Unit_B_Remaining_HP"
        ]
    )


def attacks_for_unit(
    combat_result: dict[str, Any],
    unit_id: str,
) -> int:
    """
    Возвращает число атак указанного юнита.
    """

    if (
        combat_result[
            "Unit_A_ID"
        ]
        == unit_id
    ):

        return int(
            combat_result[
                "Unit_A_Attacks"
            ]
        )

    return int(
        combat_result[
            "Unit_B_Attacks"
        ]
    )


def damage_for_unit(
    combat_result: dict[str, Any],
    unit_id: str,
) -> float:
    """
    Возвращает суммарный нанесённый урон.
    """

    if (
        combat_result[
            "Unit_A_ID"
        ]
        == unit_id
    ):

        return to_float(
            combat_result[
                "Unit_A_Damage_Dealt"
            ]
        )

    return to_float(
        combat_result[
            "Unit_B_Damage_Dealt"
        ]
    )


# ============================================================
# 11. CONTROL MATCHUPS
# ============================================================
#
# Сначала рассчитываем контрольные результаты
# при HP = 1760.
#
# Именно относительно них будут сравниваться
# остальные значения HP.
# ============================================================

control_results: dict[
    str,
    dict[str, Any],
] = {}


control_units = copy.deepcopy(
    after_units
)

control_units[
    TARGET_UNIT_ID
]["HP"] = CONTROL_HP


for opponent_id, opponent in control_units.items():

    if opponent_id == TARGET_UNIT_ID:
        continue

    combat_result = simulate_combat(
        control_units[
            TARGET_UNIT_ID
        ],
        opponent,
    )

    control_results[
        opponent_id
    ] = combat_result


# ============================================================
# 12. SENSITIVITY TEST
# ============================================================

detailed_rows: list[
    dict[str, Any]
] = []


summary_rows: list[
    dict[str, Any]
] = []


# Сохраняем историю результатов каждого matchup.
matchup_history: dict[
    str,
    list[dict[str, Any]],
] = {}


for hp_value in HP_VALUES:

    test_units = copy.deepcopy(
        after_units
    )

    test_units[
        TARGET_UNIT_ID
    ]["HP"] = hp_value

    wins = 0
    losses = 0
    draws = 0

    changed_matchups = 0

    for opponent_id, opponent in test_units.items():

        if opponent_id == TARGET_UNIT_ID:
            continue

        combat_result = simulate_combat(
            test_units[
                TARGET_UNIT_ID
            ],
            opponent,
        )

        ogre_result = result_for_unit(
            combat_result,
            TARGET_UNIT_ID,
        )

        control_result = (
            result_for_unit(
                control_results[
                    opponent_id
                ],
                TARGET_UNIT_ID,
            )
        )

        changed = (
            ogre_result
            != control_result
        )

        if changed:
            changed_matchups += 1

        if ogre_result == "Win":
            wins += 1

        elif ogre_result == "Loss":
            losses += 1

        else:
            draws += 1

        ogre_remaining_hp = (
            remaining_hp_for_unit(
                combat_result,
                TARGET_UNIT_ID,
            )
        )

        opponent_remaining_hp = (
            remaining_hp_for_unit(
                combat_result,
                opponent_id,
            )
        )

        row = {
            "Ogre_HP":
                normalize_number(
                    hp_value
                ),

            "Opponent_ID":
                opponent_id,

            "Opponent_Name":
                opponent[
                    "Unit_Name"
                ],

            "Opponent_Role":
                opponent.get(
                    "Role",
                    "",
                ),

            "Result":
                ogre_result,

            "Winner_ID":
                combat_result[
                    "Winner_ID"
                ],

            "Winner":
                combat_result[
                    "Winner"
                ],

            "Combat_Time":
                combat_result[
                    "Combat_Time"
                ],

            "Ogre_Remaining_HP":
                ogre_remaining_hp,

            "Opponent_Remaining_HP":
                opponent_remaining_hp,

            "Ogre_Attacks":
                attacks_for_unit(
                    combat_result,
                    TARGET_UNIT_ID,
                ),

            "Opponent_Attacks":
                attacks_for_unit(
                    combat_result,
                    opponent_id,
                ),

            "Ogre_Damage_Dealt":
                damage_for_unit(
                    combat_result,
                    TARGET_UNIT_ID,
                ),

            "Opponent_Damage_Dealt":
                damage_for_unit(
                    combat_result,
                    opponent_id,
                ),

            "Control_Result":
                control_result,

            "Result_Changed_From_Control":
                (
                    "Yes"
                    if changed
                    else "No"
                ),
        }

        detailed_rows.append(
            row
        )

        matchup_history.setdefault(
            opponent_id,
            [],
        ).append(
            row
        )

    battles = (
        wins
        + losses
        + draws
    )

    if battles > 0:

        win_rate = (
            wins
            / battles
            * 100.0
        )

        combat_score = (
            (
                wins
                + 0.5 * draws
            )
            / battles
            * 100.0
        )

    else:

        win_rate = 0.0
        combat_score = 0.0

    summary_rows.append(
        {
            "Ogre_HP":
                normalize_number(
                    hp_value
                ),

            "Battles":
                battles,

            "Wins":
                wins,

            "Losses":
                losses,

            "Draws":
                draws,

            "Win_Rate":
                round(
                    win_rate,
                    2,
                ),

            "Combat_Score":
                round(
                    combat_score,
                    2,
                ),

            "Changed_Matchups":
                changed_matchups,

            "Is_Control":
                (
                    "Yes"
                    if hp_value
                    == CONTROL_HP
                    else "No"
                ),
        }
    )


# ============================================================
# 13. ПОИСК ПЕРВОГО ОБНАРУЖЕННОГО ПОРОГА
# ============================================================
#
# Threshold здесь означает:
#
# первое значение HP в нашей тестовой сетке,
# при котором результат отличается от CONTROL.
#
# Это НЕ математически точный порог до 1 HP.
#
# Например:
#
# 1725 -> Win
# 1700 -> Draw
#
# означает, что настоящий порог расположен
# где-то между 1700 и 1725 включительно.
#
# ============================================================

threshold_rows: list[
    dict[str, Any]
] = []


for opponent_id, history in matchup_history.items():

    if not history:
        continue

    control_row = history[0]

    control_result = control_row[
        "Control_Result"
    ]

    first_changed_row = None
    previous_row = None

    for row in history:

        if (
            row[
                "Result_Changed_From_Control"
            ]
            == "Yes"
        ):

            first_changed_row = row
            break

        previous_row = row

    opponent_name = (
        control_row[
            "Opponent_Name"
        ]
    )

    if first_changed_row is None:

        threshold_rows.append(
            {
                "Opponent_ID":
                    opponent_id,

                "Opponent_Name":
                    opponent_name,

                "Control_Result":
                    control_result,

                "First_Changed_HP":
                    "",

                "Changed_Result":
                    "",

                "Last_Unchanged_HP":
                    normalize_number(
                        HP_VALUES[-1]
                    ),

                "Threshold_Interval":
                    (
                        f"Below "
                        f"{normalize_number(HP_VALUES[-1])}"
                        " or not found"
                    ),

                "Threshold_Found":
                    "No",

                "Interpretation":
                    (
                        "No result change was detected "
                        "inside the tested HP range."
                    ),
            }
        )

        continue

    changed_hp = to_float(
        first_changed_row[
            "Ogre_HP"
        ]
    )

    if previous_row is not None:

        unchanged_hp = to_float(
            previous_row[
                "Ogre_HP"
            ]
        )

        threshold_interval = (
            f"{normalize_number(changed_hp)}"
            "–"
            f"{normalize_number(unchanged_hp)}"
        )

        last_unchanged_hp = (
            normalize_number(
                unchanged_hp
            )
        )

    else:

        threshold_interval = (
            normalize_number(
                changed_hp
            )
        )

        last_unchanged_hp = ""

    threshold_rows.append(
        {
            "Opponent_ID":
                opponent_id,

            "Opponent_Name":
                opponent_name,

            "Control_Result":
                control_result,

            "First_Changed_HP":
                normalize_number(
                    changed_hp
                ),

            "Changed_Result":
                first_changed_row[
                    "Result"
                ],

            "Last_Unchanged_HP":
                last_unchanged_hp,

            "Threshold_Interval":
                threshold_interval,

            "Threshold_Found":
                "Yes",

            "Interpretation":
                (
                    "The matchup result changed "
                    "inside the tested Stone Ogre "
                    "HP range."
                ),
        }
    )


# ============================================================
# 14. СОХРАНЕНИЕ CSV
# ============================================================

detailed_fieldnames = [
    "Ogre_HP",
    "Opponent_ID",
    "Opponent_Name",
    "Opponent_Role",
    "Result",
    "Winner_ID",
    "Winner",
    "Combat_Time",
    "Ogre_Remaining_HP",
    "Opponent_Remaining_HP",
    "Ogre_Attacks",
    "Opponent_Attacks",
    "Ogre_Damage_Dealt",
    "Opponent_Damage_Dealt",
    "Control_Result",
    "Result_Changed_From_Control",
]


summary_fieldnames = [
    "Ogre_HP",
    "Battles",
    "Wins",
    "Losses",
    "Draws",
    "Win_Rate",
    "Combat_Score",
    "Changed_Matchups",
    "Is_Control",
]


threshold_fieldnames = [
    "Opponent_ID",
    "Opponent_Name",
    "Control_Result",
    "First_Changed_HP",
    "Changed_Result",
    "Last_Unchanged_HP",
    "Threshold_Interval",
    "Threshold_Found",
    "Interpretation",
]


write_csv(
    DETAILED_RESULTS_FILE,
    detailed_rows,
    detailed_fieldnames,
)


write_csv(
    SUMMARY_FILE,
    summary_rows,
    summary_fieldnames,
)


write_csv(
    THRESHOLDS_FILE,
    threshold_rows,
    threshold_fieldnames,
)


# ============================================================
# 15. SHA-256 ПОСЛЕ АНАЛИЗА
# ============================================================

source_hash_after = file_sha256(
    SOURCE_FILE
)


source_unchanged = (
    source_hash_before
    == source_hash_after
)


if not source_unchanged:

    raise RuntimeError(
        "КРИТИЧЕСКАЯ ОШИБКА: "
        "data/unit_balance.csv изменился "
        "во время sensitivity analysis."
    )


# ============================================================
# 16. КОНСОЛЬНЫЙ ОТЧЁТ
# ============================================================

print()
print(
    "=" * 72
)

print(
    "STONE OGRE HP SENSITIVITY ANALYSIS"
)

print(
    "=" * 72
)

print()

print(
    f"Target: "
    f"{TARGET_UNIT_ID} | "
    f"{TARGET_UNIT_NAME}"
)

print(
    f"Control HP: "
    f"{normalize_number(CONTROL_HP)}"
)

print(
    "Tested HP values: "
    + ", ".join(
        normalize_number(value)
        for value in HP_VALUES
    )
)

print()

print(
    f"Iteration 01 parameter changes "
    f"loaded: {direct_changes_applied}"
)

print()

print(
    "-" * 72
)

print(
    "SUMMARY"
)

print(
    "-" * 72
)


for row in summary_rows:

    print(
        f"HP {row['Ogre_HP']:>4} | "
        f"W: {row['Wins']:>2} | "
        f"L: {row['Losses']:>2} | "
        f"D: {row['Draws']:>2} | "
        f"Win Rate: "
        f"{row['Win_Rate']:>6.2f}% | "
        f"Combat Score: "
        f"{row['Combat_Score']:>6.2f}% | "
        f"Changed: "
        f"{row['Changed_Matchups']}"
    )


print()
print(
    "-" * 72
)

print(
    "DETECTED MATCHUP THRESHOLDS"
)

print(
    "-" * 72
)


found_thresholds = [
    row
    for row in threshold_rows
    if row[
        "Threshold_Found"
    ] == "Yes"
]


if not found_thresholds:

    print(
        "No matchup result thresholds "
        "were detected in the tested range."
    )

else:

    for row in found_thresholds:

        print(
            f"{row['Opponent_ID']} | "
            f"{row['Opponent_Name']} | "
            f"{row['Control_Result']} -> "
            f"{row['Changed_Result']} | "
            f"Threshold interval: "
            f"{row['Threshold_Interval']} HP"
        )


print()
print(
    "-" * 72
)

print(
    "SOURCE INTEGRITY"
)

print(
    "-" * 72
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
    "Source unchanged: "
    + (
        "Yes"
        if source_unchanged
        else "No"
    )
)

print()
print(
    "=" * 72
)

print(
    "STONE OGRE HP SENSITIVITY ANALYSIS ЗАВЕРШЁН"
)

print(
    "=" * 72
)

print()

print(
    "Detailed results:"
)

print(
    os.path.relpath(
        DETAILED_RESULTS_FILE,
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
    "Thresholds:"
)

print(
    os.path.relpath(
        THRESHOLDS_FILE,
        PROJECT_ROOT,
    )
)

print()

print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)