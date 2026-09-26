import csv
import copy
import os

from combat_engine import (
    calculate_unit_statistics,
    simulate_all_matchups,
    to_float,
)


# ============================================================
# ERA OF STRIFE
# 12 — ITERATION 01 COMBAT SIMULATION
# ============================================================
#
# Назначение:
#
# 1. Загрузить исходный Unit Balance.
# 2. Загрузить Balance Iteration 01.
# 3. Создать независимую AFTER-копию характеристик.
# 4. Применить только изменения Iteration 01.
# 5. Использовать ТОТ ЖЕ combat_engine.py,
#    который используется в 05_combat_simulation.py.
# 6. Рассчитать 66 AFTER-matchup.
# 7. Сохранить AFTER matchup/unit statistics.
#
# ВАЖНО:
#
# В этом файле НЕТ собственной simulate_combat().
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
# Поэтому математическая модель BEFORE и AFTER одинакова.
# ============================================================


# ============================================================
# 1. ПУТИ
# ============================================================

UNIT_BALANCE_FILE = os.path.join(
    "data",
    "unit_balance.csv",
)

ITERATION_FILE = os.path.join(
    "analysis",
    "results",
    "iterations",
    "balance_iteration_01.csv",
)

RESULTS_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "combat_simulation",
)

COMBAT_RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_combat_results.csv",
)

MATCHUP_STATISTICS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_matchup_statistics.csv",
)

UNIT_STATISTICS_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_unit_statistics.csv",
)


# ============================================================
# 2. CSV HELPERS
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


# ============================================================
# 3. ПРОВЕРКА ВХОДНЫХ ФАЙЛОВ
# ============================================================

required_files = [
    UNIT_BALANCE_FILE,
    ITERATION_FILE,
]


for file_path in required_files:

    if not os.path.exists(
        file_path
    ):

        print()
        print("=" * 70)
        print("ОШИБКА")
        print("=" * 70)

        print(
            "Не найден обязательный файл:"
        )

        print(
            file_path
        )

        raise SystemExit


# ============================================================
# 4. ЗАГРУЗКА ДАННЫХ
# ============================================================

print()
print("=" * 70)
print("ERA OF STRIFE — ITERATION 01 COMBAT SIMULATION")
print("=" * 70)

print()
print(
    "Unit Balance:",
    UNIT_BALANCE_FILE,
)

print(
    "Iteration:",
    ITERATION_FILE,
)


unit_rows = read_csv(
    UNIT_BALANCE_FILE
)

iteration_rows = read_csv(
    ITERATION_FILE
)


print()
print(
    "Исходных юнитов:",
    len(unit_rows),
)

print(
    "Строк Iteration 01:",
    len(iteration_rows),
)


# ============================================================
# 5. ПРОВЕРКА UNIT BALANCE
# ============================================================

if not unit_rows:

    print()
    print(
        "ОШИБКА: unit_balance.csv пуст."
    )

    raise SystemExit


required_unit_columns = [
    "Unit_ID",
    "Unit_Name",
    "HP",
    "Damage",
    "Attack_Interval",
]


missing_columns = [
    column
    for column in required_unit_columns
    if column not in unit_rows[0]
]


if missing_columns:

    print()
    print(
        "ОШИБКА: отсутствуют обязательные "
        "столбцы Unit Balance:"
    )

    for column in missing_columns:

        print(
            "-",
            column,
        )

    raise SystemExit


# ============================================================
# 6. СОЗДАНИЕ BEFORE-СЛОВАРЯ
# ============================================================

before_units = {}


for row in unit_rows:

    unit_id = row[
        "Unit_ID"
    ].strip()

    if unit_id == "":

        continue

    if unit_id in before_units:

        print()
        print(
            "ОШИБКА: повторяющийся Unit_ID:",
            unit_id,
        )

        raise SystemExit


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
            "ОШИБКА числовых данных:",
            unit_id,
        )

        raise SystemExit


    if (
        hp <= 0
        or damage <= 0
        or attack_interval <= 0
    ):

        print()
        print(
            "ОШИБКА: некорректные боевые "
            "параметры:",
            unit_id,
        )

        raise SystemExit


    before_units[
        unit_id
    ] = copy.deepcopy(
        row
    )


# ============================================================
# 7. СОЗДАНИЕ НЕЗАВИСИМОГО AFTER
# ============================================================

after_units = copy.deepcopy(
    before_units
)


print()
print(
    "Юнитов BEFORE:",
    len(before_units),
)

print(
    "Юнитов AFTER:",
    len(after_units),
)


# ============================================================
# 8. ОПРЕДЕЛЕНИЕ ИЗМЕНЕНИЙ ITERATION 01
# ============================================================

DIRECT_TARGET_TYPES = {
    "Buff Candidate",
    "Nerf Candidate",
}


def first_value(
    row,
    possible_columns,
):
    """
    Возвращает первое найденное непустое значение
    из нескольких возможных названий столбцов.
    """

    for column in possible_columns:

        if column in row:

            value = str(
                row[column]
            ).strip()

            if value != "":

                return value

    return ""


direct_changes = []


print()
print("=" * 70)
print("ПРИМЕНЕНИЕ ITERATION 01")
print("=" * 70)


for iteration_row in iteration_rows:

    unit_id = first_value(
        iteration_row,
        [
            "Unit_ID",
            "Target_Unit_ID",
        ],
    )

    iteration_target = first_value(
        iteration_row,
        [
            "Iteration_Target",
            "Recommendation",
            "Target_Type",
        ],
    )

    changed_parameter = first_value(
        iteration_row,
        [
            "Changed_Parameter",
            "Parameter",
        ],
    )

    before_value_text = first_value(
        iteration_row,
        [
            "Before_Value",
            "Original_Value",
            "Old_Value",
        ],
    )

    after_value_text = first_value(
        iteration_row,
        [
            "After_Value",
            "New_Value",
            "Proposed_Value",
        ],
    )


    # --------------------------------------------------------
    # Нас интересуют только реальные direct targets.
    # --------------------------------------------------------

    if (
        iteration_target
        not in DIRECT_TARGET_TYPES
    ):

        continue


    if unit_id == "":

        print()
        print(
            "ОШИБКА: direct target без Unit_ID."
        )

        raise SystemExit


    if unit_id not in after_units:

        print()
        print(
            "ОШИБКА: direct target отсутствует "
            "в Unit Balance:",
            unit_id,
        )

        raise SystemExit


    if changed_parameter == "":

        print()
        print(
            "ОШИБКА:",
            unit_id,
            "не содержит Changed_Parameter."
        )

        raise SystemExit


    if changed_parameter not in after_units[
        unit_id
    ]:

        print()
        print(
            "ОШИБКА:",
            unit_id,
            "не содержит параметр",
            changed_parameter,
        )

        raise SystemExit


    if after_value_text == "":

        print()
        print(
            "ОШИБКА:",
            unit_id,
            changed_parameter,
            "не содержит After_Value."
        )

        raise SystemExit


    # --------------------------------------------------------
    # Реальное BEFORE берём непосредственно
    # из исходного Unit Balance.
    # --------------------------------------------------------

    actual_before_value = to_float(
        after_units[
            unit_id
        ][
            changed_parameter
        ]
    )

    expected_before_value = None


    if before_value_text != "":

        expected_before_value = to_float(
            before_value_text
        )


    # --------------------------------------------------------
    # Защита от несогласованных данных.
    #
    # Если iteration-файл утверждает, что BEFORE был
    # одним, а исходный Unit Balance содержит другое,
    # эксперимент нельзя продолжать молча.
    # --------------------------------------------------------

    if (
        expected_before_value is not None
        and abs(
            actual_before_value
            - expected_before_value
        ) > 1e-9
    ):

        print()
        print("=" * 70)
        print("ОШИБКА BEFORE VALUE")
        print("=" * 70)

        print(
            "Unit:",
            unit_id,
        )

        print(
            "Parameter:",
            changed_parameter,
        )

        print(
            "Unit Balance BEFORE:",
            actual_before_value,
        )

        print(
            "Iteration BEFORE:",
            expected_before_value,
        )

        print()
        print(
            "Iteration 01 не применяется, "
            "пока значения не согласованы."
        )

        raise SystemExit


    new_value = to_float(
        after_value_text
    )


    # --------------------------------------------------------
    # Применяем изменение ТОЛЬКО к AFTER.
    # --------------------------------------------------------

    after_units[
        unit_id
    ][
        changed_parameter
    ] = new_value


    direct_changes.append(
        {
            "Unit_ID":
                unit_id,

            "Unit_Name":
                after_units[
                    unit_id
                ][
                    "Unit_Name"
                ],

            "Iteration_Target":
                iteration_target,

            "Changed_Parameter":
                changed_parameter,

            "Before_Value":
                actual_before_value,

            "After_Value":
                new_value,

            "Absolute_Change":
                round(
                    new_value
                    - actual_before_value,
                    6,
                ),

            "Percent_Change":
                round(
                    (
                        (
                            new_value
                            - actual_before_value
                        )
                        / actual_before_value
                        * 100.0
                    ),
                    2,
                )
                if actual_before_value != 0
                else 0.0,
        }
    )


# ============================================================
# 9. ПРОВЕРКА DIRECT TARGETS
# ============================================================

print()


if not direct_changes:

    print(
        "ОШИБКА: не найдено ни одного "
        "direct change."
    )

    raise SystemExit


for change in direct_changes:

    print(
        change["Unit_ID"],
        "|",
        change["Unit_Name"],
        "|",
        change["Iteration_Target"],
        "|",
        change["Changed_Parameter"],
        ":",
        change["Before_Value"],
        "->",
        change["After_Value"],
        "|",
        str(
            change["Percent_Change"]
        ) + "%",
    )


print()
print(
    "Всего direct changes:",
    len(direct_changes),
)


# Для Iteration 01 мы ожидаем именно два изменения:
# HOR_01 и HOR_02.

expected_direct_targets = {
    "HOR_01",
    "HOR_02",
}

actual_direct_targets = {
    row["Unit_ID"]
    for row in direct_changes
}


print(
    "Expected direct targets:",
    "; ".join(
        sorted(
            expected_direct_targets
        )
    ),
)

print(
    "Detected direct targets:",
    "; ".join(
        sorted(
            actual_direct_targets
        )
    ),
)


if (
    actual_direct_targets
    != expected_direct_targets
):

    print()
    print(
        "ОШИБКА: набор direct targets "
        "не соответствует Iteration 01."
    )

    raise SystemExit


print(
    "[OK] Direct targets определены правильно."
)


# ============================================================
# 10. ДОКАЗАТЕЛЬСТВО, ЧТО ОСТАЛЬНЫЕ ЮНИТЫ НЕ ИЗМЕНИЛИСЬ
# ============================================================

print()
print("=" * 70)
print("ПРОВЕРКА ИЗОЛЯЦИИ AFTER")
print("=" * 70)


unexpected_changes = []


for unit_id in before_units:

    before_unit = before_units[
        unit_id
    ]

    after_unit = after_units[
        unit_id
    ]

    all_fields = set(
        before_unit.keys()
    ) | set(
        after_unit.keys()
    )

    for field in all_fields:

        before_value = str(
            before_unit.get(
                field,
                "",
            )
        )

        after_value = str(
            after_unit.get(
                field,
                "",
            )
        )

        if (
            before_value
            != after_value
        ):

            is_expected_change = any(
                change["Unit_ID"] == unit_id
                and change[
                    "Changed_Parameter"
                ] == field
                for change in direct_changes
            )

            if not is_expected_change:

                unexpected_changes.append(
                    {
                        "Unit_ID":
                            unit_id,

                        "Field":
                            field,

                        "Before":
                            before_value,

                        "After":
                            after_value,
                    }
                )


if unexpected_changes:

    print()
    print(
        "ОШИБКА: обнаружены неожиданные "
        "изменения AFTER:"
    )

    for change in unexpected_changes:

        print(
            change
        )

    raise SystemExit


print(
    "[OK] AFTER отличается от BEFORE "
    "только заявленными direct changes."
)


# ============================================================
# 11. ОЖИДАЕМОЕ ЧИСЛО MATCHUP
# ============================================================

unit_count = len(
    after_units
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
print("AFTER SIMULATION")
print("=" * 70)

print()
print(
    "Количество юнитов:",
    unit_count,
)

print(
    "Ожидаемое количество matchup:",
    expected_matchups,
)

print(
    "Combat engine:",
    "analysis/combat_engine.py",
)


# ============================================================
# 12. ЗАПУСК ТОГО ЖЕ COMBAT ENGINE
# ============================================================

matchup_results = simulate_all_matchups(
    after_units
)


print()
print(
    "Рассчитано AFTER matchup:",
    len(matchup_results),
)


if (
    len(matchup_results)
    != expected_matchups
):

    print()
    print(
        "ОШИБКА: неправильное количество "
        "AFTER matchup."
    )

    raise SystemExit


print(
    "[OK] Количество AFTER matchup корректно."
)


# ============================================================
# 13. ПРОВЕРКА УНИКАЛЬНОСТИ
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
            "ОШИБКА: повторный matchup:",
            pair,
        )

        raise SystemExit

    unique_pairs.add(
        pair
    )


print(
    "[OK] Все AFTER matchup уникальны."
)


# ============================================================
# 14. UNIT STATISTICS
# ============================================================

unit_statistics = calculate_unit_statistics(
    after_units,
    matchup_results,
)


if (
    len(unit_statistics)
    != unit_count
):

    print()
    print(
        "ОШИБКА: неправильное количество "
        "unit statistics."
    )

    raise SystemExit


expected_battles_per_unit = (
    unit_count - 1
)


for row in unit_statistics:

    if (
        int(
            row["Battles"]
        )
        != expected_battles_per_unit
    ):

        print()
        print(
            "ОШИБКА:",
            row["Unit_ID"],
            "имеет неправильное "
            "количество боёв.",
        )

        raise SystemExit


print(
    "[OK] Каждый юнит провёл",
    expected_battles_per_unit,
    "AFTER боёв."
)


# ============================================================
# 15. MATCHUP STATISTICS
# ============================================================

matchup_statistics = []


for result in matchup_results:

    if (
        result["Result"]
        == "Draw"
    ):

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
# 16. СОХРАНЕНИЕ AFTER
# ============================================================

write_csv(
    COMBAT_RESULTS_FILE,
    matchup_results,
)

write_csv(
    MATCHUP_STATISTICS_FILE,
    matchup_statistics,
)

write_csv(
    UNIT_STATISTICS_FILE,
    unit_statistics,
)


# ============================================================
# 17. ФУНКЦИЯ ПОИСКА КОНТРОЛЬНОГО MATCHUP
# ============================================================

def find_matchup(
    rows,
    unit_1_id,
    unit_2_id,
):

    target_pair = {
        unit_1_id,
        unit_2_id,
    }

    for row in rows:

        current_pair = {
            row["Unit_1_ID"],
            row["Unit_2_ID"],
        }

        if (
            current_pair
            == target_pair
        ):

            return row

    return None


# ============================================================
# 18. ТРИ КОНТРОЛЬНЫХ MATCHUP
# ============================================================

print()
print("=" * 70)
print("CONTROL MATCHUPS — AFTER")
print("=" * 70)


control_matchups = [
    (
        "ELF_01",
        "ELF_02",
        "Control: neither unit was modified",
    ),
    (
        "ELF_01",
        "HOR_02",
        "Direct: HOR_02 was modified",
    ),
    (
        "UND_01",
        "HOR_01",
        "Direct: HOR_01 was modified",
    ),
]


for (
    unit_1_id,
    unit_2_id,
    explanation,
) in control_matchups:

    row = find_matchup(
        matchup_statistics,
        unit_1_id,
        unit_2_id,
    )

    print()

    print(
        unit_1_id,
        "VS",
        unit_2_id,
    )

    print(
        explanation
    )

    if row is None:

        print(
            "Result: MATCHUP NOT FOUND"
        )

    else:

        print(
            "AFTER result:",
            row["Result"],
        )

        print(
            "Combat time:",
            row["Combat_Time"],
        )


# ============================================================
# 19. СПЕЦИАЛЬНАЯ ПРОВЕРКА ELF_01 VS ELF_02
# ============================================================

control_elf = find_matchup(
    matchup_statistics,
    "ELF_01",
    "ELF_02",
)


print()
print("=" * 70)
print("PIPELINE CONTROL")
print("=" * 70)


if control_elf is None:

    print()
    print(
        "ОШИБКА: ELF_01 vs ELF_02 "
        "не найден."
    )

    raise SystemExit


print()
print(
    "ELF_01 vs ELF_02 AFTER:",
    control_elf["Result"],
)


# Новый canonical BEFORE из 05 уже показал Draw.
# Поскольку ELF_01 и ELF_02 не изменялись,
# AFTER тоже обязан быть Draw.

EXPECTED_CONTROL_RESULT = "Draw"


if (
    control_elf["Result"]
    != EXPECTED_CONTROL_RESULT
):

    print()
    print("=" * 70)
    print("ОШИБКА PIPELINE CONSISTENCY")
    print("=" * 70)

    print(
        "Canonical BEFORE:",
        EXPECTED_CONTROL_RESULT,
    )

    print(
        "AFTER:",
        control_elf["Result"],
    )

    print()
    print(
        "Немодифицированный matchup изменился."
    )

    print(
        "Нужно остановить pipeline "
        "и искать новую причину."
    )

    raise SystemExit


print(
    "[OK] ELF_01 vs ELF_02:"
)

print(
    "BEFORE = Draw"
)

print(
    "AFTER  = Draw"
)

print(
    "Ложный indirect side effect устранён."
)


# ============================================================
# 20. ВЫВОД AFTER UNIT STATISTICS
# ============================================================

print()
print("=" * 70)
print("AFTER UNIT RESULTS")
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
# 21. ИТОГ
# ============================================================

print()
print("=" * 70)
print("ITERATION 01 COMBAT SIMULATION ЗАВЕРШЕНА")
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
    UNIT_STATISTICS_FILE
)

print()

print(
    "Direct changes applied:",
    len(direct_changes),
)

print()

print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)

print()

print(
    "BEFORE и AFTER теперь используют "
    "один combat_engine.py."
)