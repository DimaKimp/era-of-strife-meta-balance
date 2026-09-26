from __future__ import annotations

import copy
import math
from itertools import combinations
from typing import Any


# ============================================================
# ERA OF STRIFE — SHARED COMBAT ENGINE
# ============================================================
#
# Это единый источник боевой логики для:
#
# - baseline / BEFORE;
# - Balance Iteration / AFTER;
# - последующих balance iterations.
#
# Главное правило:
#
# BEFORE и AFTER ОБЯЗАНЫ использовать одну и ту же
# функцию simulate_combat().
#
# Тогда единственным изменяемым фактором эксперимента
# являются параметры, которые мы действительно меняем
# в Balance Iteration.
# ============================================================


# ------------------------------------------------------------
# Числовые настройки модели
# ------------------------------------------------------------

TIME_ABS_TOLERANCE = 1e-9
MAX_COMBAT_TIME = 300.0


# ============================================================
# 1. ПРЕОБРАЗОВАНИЕ ЧИСЕЛ
# ============================================================

def to_float(value: Any) -> float:
    """
    Безопасно преобразует значение в float.

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


# ============================================================
# 2. СОЗДАНИЕ НЕЗАВИСИМОЙ БОЕВОЙ КОПИИ
# ============================================================

def create_combatant(
    unit: dict[str, Any],
) -> dict[str, Any]:
    """
    Создаёт независимую копию юнита.

    Исходный словарь юнита не изменяется.
    """

    fighter = copy.deepcopy(unit)

    fighter["Max_HP"] = to_float(
        unit["HP"]
    )

    fighter["Current_HP"] = to_float(
        unit["HP"]
    )

    fighter["Damage"] = to_float(
        unit["Damage"]
    )

    fighter["Attack_Interval"] = to_float(
        unit["Attack_Interval"]
    )

    return fighter


# ============================================================
# 3. ПРОВЕРКА СОВПАДЕНИЯ ВРЕМЕНИ
# ============================================================

def same_time(
    value_a: float,
    value_b: float,
) -> bool:
    """
    Проверяет, относятся ли два значения времени
    к одному событию.

    Используется единое правило во ВСЕХ симуляциях.
    """

    return math.isclose(
        value_a,
        value_b,
        rel_tol=0.0,
        abs_tol=TIME_ABS_TOLERANCE,
    )


# ============================================================
# 4. СИМУЛЯЦИЯ ОДНОГО БОЯ
# ============================================================

def simulate_combat(
    unit_a: dict[str, Any],
    unit_b: dict[str, Any],
) -> dict[str, Any]:
    """
    Единая упрощённая 1v1-модель Era of Strife.

    Учитывает:
    - HP;
    - Damage;
    - Attack Interval;
    - независимое время атак;
    - одновременные атаки.

    Пока НЕ учитывает:
    - способности;
    - Attack Range;
    - Move Speed;
    - позиционирование;
    - командные взаимодействия.

    Это намеренное ограничение текущей baseline-модели.
    """

    fighter_a = create_combatant(
        unit_a
    )

    fighter_b = create_combatant(
        unit_b
    )

    current_time = 0.0

    next_attack_a = fighter_a[
        "Attack_Interval"
    ]

    next_attack_b = fighter_b[
        "Attack_Interval"
    ]

    attacks_a = 0
    attacks_b = 0

    damage_dealt_a = 0.0
    damage_dealt_b = 0.0

    while (
        fighter_a["Current_HP"] > 0
        and fighter_b["Current_HP"] > 0
        and current_time <= MAX_COMBAT_TIME
    ):

        next_event_time = min(
            next_attack_a,
            next_attack_b,
        )

        current_time = next_event_time

        # Защита от бесконечного боя.
        if current_time > MAX_COMBAT_TIME:
            break

        attack_a_now = same_time(
            next_attack_a,
            current_time,
        )

        attack_b_now = same_time(
            next_attack_b,
            current_time,
        )

        # ----------------------------------------------------
        # Сначала рассчитываем ОБЕ атаки.
        #
        # Урон применяется только после этого.
        #
        # Поэтому если оба юнита должны атаковать
        # в один момент, возможна взаимная смерть.
        # ----------------------------------------------------

        damage_to_a = 0.0
        damage_to_b = 0.0

        if attack_a_now:

            damage_to_b = fighter_a[
                "Damage"
            ]

            attacks_a += 1

            damage_dealt_a += damage_to_b

        if attack_b_now:

            damage_to_a = fighter_b[
                "Damage"
            ]

            attacks_b += 1

            damage_dealt_b += damage_to_a

        # ----------------------------------------------------
        # Одновременное применение урона
        # ----------------------------------------------------

        fighter_a[
            "Current_HP"
        ] -= damage_to_a

        fighter_b[
            "Current_HP"
        ] -= damage_to_b

        # ----------------------------------------------------
        # Планирование следующих атак
        # ----------------------------------------------------

        if attack_a_now:

            next_attack_a += fighter_a[
                "Attack_Interval"
            ]

        if attack_b_now:

            next_attack_b += fighter_b[
                "Attack_Interval"
            ]

    # ========================================================
    # 5. ОПРЕДЕЛЕНИЕ РЕЗУЛЬТАТА
    # ========================================================

    a_dead = (
        fighter_a["Current_HP"] <= 0
    )

    b_dead = (
        fighter_b["Current_HP"] <= 0
    )

    if a_dead and b_dead:

        result = "Draw"

        winner_id = ""
        winner_name = ""

        loser_id = ""
        loser_name = ""

    elif b_dead:

        result = "Win"

        winner_id = fighter_a[
            "Unit_ID"
        ]

        winner_name = fighter_a[
            "Unit_Name"
        ]

        loser_id = fighter_b[
            "Unit_ID"
        ]

        loser_name = fighter_b[
            "Unit_Name"
        ]

    elif a_dead:

        result = "Win"

        winner_id = fighter_b[
            "Unit_ID"
        ]

        winner_name = fighter_b[
            "Unit_Name"
        ]

        loser_id = fighter_a[
            "Unit_ID"
        ]

        loser_name = fighter_a[
            "Unit_Name"
        ]

    else:

        # Если достигнут MAX_COMBAT_TIME,
        # бой считается ничьёй.
        result = "Draw"

        winner_id = ""
        winner_name = ""

        loser_id = ""
        loser_name = ""

    return {
        "Unit_A_ID":
            fighter_a["Unit_ID"],

        "Unit_A_Name":
            fighter_a["Unit_Name"],

        "Unit_A_Role":
            fighter_a.get(
                "Role",
                "",
            ),

        "Unit_B_ID":
            fighter_b["Unit_ID"],

        "Unit_B_Name":
            fighter_b["Unit_Name"],

        "Unit_B_Role":
            fighter_b.get(
                "Role",
                "",
            ),

        "Result":
            result,

        "Winner_ID":
            winner_id,

        "Winner":
            winner_name,

        "Loser_ID":
            loser_id,

        "Loser":
            loser_name,

        "Combat_Time":
            round(
                current_time,
                6,
            ),

        "Unit_A_Remaining_HP":
            round(
                max(
                    0.0,
                    fighter_a["Current_HP"],
                ),
                6,
            ),

        "Unit_B_Remaining_HP":
            round(
                max(
                    0.0,
                    fighter_b["Current_HP"],
                ),
                6,
            ),

        "Unit_A_Attacks":
            attacks_a,

        "Unit_B_Attacks":
            attacks_b,

        "Unit_A_Damage_Dealt":
            round(
                damage_dealt_a,
                6,
            ),

        "Unit_B_Damage_Dealt":
            round(
                damage_dealt_b,
                6,
            ),
    }


# ============================================================
# 6. СИМУЛЯЦИЯ ВСЕХ УНИКАЛЬНЫХ MATCHUP
# ============================================================

def simulate_all_matchups(
    units: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Запускает каждый уникальный matchup один раз.

    Для 12 юнитов:

        C(12, 2)
        = 12 * 11 / 2
        = 66 matchup.
    """

    results = []

    unit_ids = list(
        units.keys()
    )

    for unit_a_id, unit_b_id in combinations(
        unit_ids,
        2,
    ):

        result = simulate_combat(
            units[unit_a_id],
            units[unit_b_id],
        )

        results.append(
            result
        )

    return results


# ============================================================
# 7. СОЗДАНИЕ СТАТИСТИКИ ЮНИТОВ
# ============================================================

def calculate_unit_statistics(
    units: dict[str, dict[str, Any]],
    matchup_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Рассчитывает Wins / Losses / Draws / Win Rate
    по результатам всех matchup.
    """

    statistics = {}

    for unit_id, unit in units.items():

        statistics[unit_id] = {
            "Unit_ID":
                unit_id,

            "Unit_Name":
                unit["Unit_Name"],

            "Faction":
                unit.get(
                    "Faction",
                    "",
                ),

            "Role":
                unit.get(
                    "Role",
                    "",
                ),

            "Battles":
                0,

            "Wins":
                0,

            "Losses":
                0,

            "Draws":
                0,
        }

    for matchup in matchup_results:

        unit_a_id = matchup[
            "Unit_A_ID"
        ]

        unit_b_id = matchup[
            "Unit_B_ID"
        ]

        statistics[
            unit_a_id
        ]["Battles"] += 1

        statistics[
            unit_b_id
        ]["Battles"] += 1

        if matchup["Result"] == "Draw":

            statistics[
                unit_a_id
            ]["Draws"] += 1

            statistics[
                unit_b_id
            ]["Draws"] += 1

            continue

        winner_id = matchup[
            "Winner_ID"
        ]

        loser_id = matchup[
            "Loser_ID"
        ]

        statistics[
            winner_id
        ]["Wins"] += 1

        statistics[
            loser_id
        ]["Losses"] += 1

    rows = []

    for unit_id, data in statistics.items():

        battles = data["Battles"]

        wins = data["Wins"]
        draws = data["Draws"]

        if battles > 0:

            win_rate = (
                wins
                / battles
                * 100.0
            )

            draw_rate = (
                draws
                / battles
                * 100.0
            )

            # Combat Score:
            #
            # победа = 1
            # ничья = 0.5
            # поражение = 0

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
            draw_rate = 0.0
            combat_score = 0.0

        row = data.copy()

        row["Win_Rate"] = round(
            win_rate,
            2,
        )

        row["Draw_Rate"] = round(
            draw_rate,
            2,
        )

        row["Combat_Score"] = round(
            combat_score,
            2,
        )

        rows.append(
            row
        )

    return rows