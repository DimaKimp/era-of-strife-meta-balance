import csv
import copy
import hashlib
import json
import os

from combat_engine import (
    calculate_unit_statistics,
    simulate_all_matchups,
    to_float,
)


# ============================================================
# ERA OF STRIFE
# 14 — REPRODUCIBILITY CHECK
# ============================================================
#
# Цель:
#
# Проверить воспроизводимость нового канонического
# combat pipeline после унификации BEFORE и AFTER.
#
# Проверяем:
#
# 1. Можно ли повторно построить canonical BEFORE
#    непосредственно из data/unit_balance.csv.
#
# 2. Совпадает ли повторно рассчитанный BEFORE
#    с результатом 05_combat_simulation.py.
#
# 3. Дают ли 5 независимых повторных запусков
#    одинаковый результат.
#
# 4. Стабильны ли все 66 matchup.
#
# 5. Стабильна ли статистика всех 12 юнитов.
#
# 6. Не изменяется ли исходный unit_balance.csv.
#
# ВАЖНО:
#
# Reproducible != Correct.
#
# Воспроизводимость означает только:
# одинаковый input + одинаковая модель
# дают одинаковый output.
#
# Корректность самой модели анализируется отдельно.
# ============================================================


# ============================================================
# 1. НАСТРОЙКИ
# ============================================================

RUNS = 5

EXPECTED_UNITS = 12

EXPECTED_MATCHUPS = (
    EXPECTED_UNITS
    * (EXPECTED_UNITS - 1)
    // 2
)


# ============================================================
# 2. ПУТИ
# ============================================================

UNIT_BALANCE_FILE = os.path.join(
    "data",
    "unit_balance.csv",
)

CANONICAL_BEFORE_MATCHUP_FILE = os.path.join(
    "analysis",
    "results",
    "matchup_statistics.csv",
)

CANONICAL_BEFORE_UNIT_FILE = os.path.join(
    "analysis",
    "results",
    "unit_combat_statistics.csv",
)

RESULTS_DIR = os.path.join(
    "analysis",
    "results",
    "iterations",
    "reproducibility",
)

RUNS_DIR = os.path.join(
    RESULTS_DIR,
    "runs",
)

MATCHUP_CHECK_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_reproducibility_matchups.csv",
)

UNIT_CHECK_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_reproducibility_units.csv",
)

SUMMARY_FILE = os.path.join(
    RESULTS_DIR,
    "balance_iteration_01_reproducibility_summary.csv",
)


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
):

    if not rows:

        print(
            "[WARNING] Нет данных:",
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
# 4. FILE HASH
# ============================================================

def file_sha256(file_path):
    """
    SHA-256 позволяет проверить,
    изменился ли файл побайтно.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb",
    ) as file:

        while True:

            chunk = file.read(
                65536
            )

            if not chunk:
                break

            sha256.update(
                chunk
            )

    return sha256.hexdigest()


# ============================================================
# 5. ПРОВЕРКА ВХОДНЫХ ФАЙЛОВ
# ============================================================

required_files = [
    UNIT_BALANCE_FILE,
    CANONICAL_BEFORE_MATCHUP_FILE,
    CANONICAL_BEFORE_UNIT_FILE,
]


print()
print("=" * 72)
print("ERA OF STRIFE — REPRODUCIBILITY CHECK")
print("=" * 72)


for file_path in required_files:

    if not os.path.exists(
        file_path
    ):

        print()
        print(
            "ОШИБКА: не найден файл:"
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
# 6. HASH ИСХОДНОГО UNIT BALANCE ДО ТЕСТА
# ============================================================

source_hash_before = file_sha256(
    UNIT_BALANCE_FILE
)


print()
print(
    "SHA-256 unit_balance.csv BEFORE:"
)

print(
    source_hash_before
)


# ============================================================
# 7. ЗАГРУЗКА UNIT BALANCE
# ============================================================

unit_rows = read_csv(
    UNIT_BALANCE_FILE
)


if (
    len(unit_rows)
    != EXPECTED_UNITS
):

    print()
    print(
        "ОШИБКА: ожидалось",
        EXPECTED_UNITS,
        "юнитов, получено",
        len(unit_rows),
    )

    raise SystemExit


units = {}


for row in unit_rows:

    unit_id = row[
        "Unit_ID"
    ].strip()

    if unit_id == "":

        print()
        print(
            "ОШИБКА: пустой Unit_ID."
        )

        raise SystemExit

    if unit_id in units:

        print()
        print(
            "ОШИБКА: повторный Unit_ID:",
            unit_id,
        )

        raise SystemExit

    # Проверяем минимально необходимые
    # числовые параметры.

    hp = to_float(
        row["HP"]
    )

    damage = to_float(
        row["Damage"]
    )

    attack_interval = to_float(
        row["Attack_Interval"]
    )

    if (
        hp <= 0
        or damage <= 0
        or attack_interval <= 0
    ):

        print()
        print(
            "ОШИБКА боевых параметров:",
            unit_id,
        )

        raise SystemExit

    units[
        unit_id
    ] = copy.deepcopy(
        row
    )


print()
print(
    "[OK] Загружено юнитов:",
    len(units),
)


# ============================================================
# 8. CANONICAL BEFORE ИЗ 05
# ============================================================

canonical_matchups = read_csv(
    CANONICAL_BEFORE_MATCHUP_FILE
)

canonical_units = read_csv(
    CANONICAL_BEFORE_UNIT_FILE
)


if (
    len(canonical_matchups)
    != EXPECTED_MATCHUPS
):

    print()
    print(
        "ОШИБКА: canonical BEFORE содержит "
        "не 66 matchup."
    )

    raise SystemExit


if (
    len(canonical_units)
    != EXPECTED_UNITS
):

    print()
    print(
        "ОШИБКА: canonical BEFORE содержит "
        "не 12 unit statistics."
    )

    raise SystemExit


print(
    "[OK] Canonical BEFORE содержит "
    "66 matchup / 12 units."
)


# ============================================================
# 9. НОРМАЛИЗАЦИЯ MATCHUP
# ============================================================

def matchup_key(row):

    return tuple(
        sorted(
            [
                row["Unit_1_ID"],
                row["Unit_2_ID"],
            ]
        )
    )


def canonical_matchup_map(rows):

    result = {}

    for row in rows:

        key = matchup_key(
            row
        )

        if key in result:

            print()
            print(
                "ОШИБКА: повторный matchup:",
                key,
            )

            raise SystemExit

        result[
            key
        ] = row

    return result


# ============================================================
# 10. ПРЕОБРАЗОВАНИЕ ENGINE RESULTS
# ============================================================

def engine_to_matchup_statistics(
    engine_results,
):

    rows = []

    for result in engine_results:

        if (
            result["Result"]
            == "Draw"
        ):

            matchup_result = "Draw"

        else:

            matchup_result = result[
                "Winner"
            ]

        rows.append(
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

    return rows


# ============================================================
# 11. НОРМАЛИЗАЦИЯ ДЛЯ СРАВНЕНИЯ
# ============================================================

def normalize_value(value):

    if value is None:
        return ""

    return str(
        value
    ).strip()


def compare_rows(
    row_a,
    row_b,
    fields,
):

    differences = []

    for field in fields:

        value_a = normalize_value(
            row_a.get(
                field,
                "",
            )
        )

        value_b = normalize_value(
            row_b.get(
                field,
                "",
            )
        )

        if value_a != value_b:

            differences.append(
                (
                    field,
                    value_a,
                    value_b,
                )
            )

    return differences


# ============================================================
# 12. ПОЛЯ MATCHUP ДЛЯ СРАВНЕНИЯ
# ============================================================

MATCHUP_COMPARE_FIELDS = [
    "Result",
    "Winner_ID",
    "Winner",
    "Combat_Time",
]


UNIT_COMPARE_FIELDS = [
    "Battles",
    "Wins",
    "Losses",
    "Draws",
    "Win_Rate",
    "Draw_Rate",
    "Combat_Score",
]


# ============================================================
# 13. ПОДГОТОВКА CANONICAL MAP
# ============================================================

canonical_matchup_lookup = (
    canonical_matchup_map(
        canonical_matchups
    )
)


canonical_unit_lookup = {
    row["Unit_ID"]: row
    for row in canonical_units
}


# ============================================================
# 14. ПОВТОРНЫЕ ЗАПУСКИ
# ============================================================

os.makedirs(
    RUNS_DIR,
    exist_ok=True,
)


all_run_matchups = []

all_run_units = []

run_signatures = []


print()
print("=" * 72)
print("REPEATED RUNS")
print("=" * 72)


for run_number in range(
    1,
    RUNS + 1,
):

    print()
    print(
        "Run",
        run_number,
        "of",
        RUNS,
    )

    # Каждый запуск получает независимую
    # глубокую копию исходных данных.

    run_units_input = copy.deepcopy(
        units
    )


    engine_results = simulate_all_matchups(
        run_units_input
    )


    if (
        len(engine_results)
        != EXPECTED_MATCHUPS
    ):

        print()
        print(
            "ОШИБКА: Run",
            run_number,
            "создал",
            len(engine_results),
            "matchup вместо",
            EXPECTED_MATCHUPS,
        )

        raise SystemExit


    matchup_rows = (
        engine_to_matchup_statistics(
            engine_results
        )
    )


    unit_statistics = (
        calculate_unit_statistics(
            run_units_input,
            engine_results,
        )
    )


    if (
        len(unit_statistics)
        != EXPECTED_UNITS
    ):

        print()
        print(
            "ОШИБКА: Run",
            run_number,
            "создал неправильное "
            "количество unit statistics."
        )

        raise SystemExit


    # --------------------------------------------------------
    # Сохраняем каждый run отдельно.
    # --------------------------------------------------------

    run_matchup_file = os.path.join(
        RUNS_DIR,
        (
            "baseline_run_"
            + str(
                run_number
            ).zfill(2)
            + "_matchups.csv"
        ),
    )

    run_unit_file = os.path.join(
        RUNS_DIR,
        (
            "baseline_run_"
            + str(
                run_number
            ).zfill(2)
            + "_units.csv"
        ),
    )


    write_csv(
        run_matchup_file,
        matchup_rows,
    )

    write_csv(
        run_unit_file,
        unit_statistics,
    )


    all_run_matchups.append(
        matchup_rows
    )

    all_run_units.append(
        unit_statistics
    )


    # --------------------------------------------------------
    # Создаём логическую сигнатуру результата.
    #
    # Она не зависит от CSV BOM / line endings.
    # --------------------------------------------------------

    normalized_signature_data = []


    run_lookup = canonical_matchup_map(
        matchup_rows
    )


    for key in sorted(
        run_lookup.keys()
    ):

        row = run_lookup[
            key
        ]

        normalized_signature_data.append(
            {
                "Pair":
                    list(
                        key
                    ),

                "Result":
                    row["Result"],

                "Winner_ID":
                    row["Winner_ID"],

                "Combat_Time":
                    normalize_value(
                        row["Combat_Time"]
                    ),
            }
        )


    signature_text = json.dumps(
        normalized_signature_data,
        ensure_ascii=False,
        sort_keys=True,
    )


    signature = hashlib.sha256(
        signature_text.encode(
            "utf-8"
        )
    ).hexdigest()


    run_signatures.append(
        signature
    )


    print(
        "[OK] 66 matchup / 12 units."
    )

    print(
        "Logical SHA-256:",
        signature,
    )


# ============================================================
# 15. ПРОВЕРКА RUN VS CANONICAL BEFORE
# ============================================================

matchup_check_rows = []

unstable_matchups = 0

canonical_mismatches = 0


all_pairs = sorted(
    canonical_matchup_lookup.keys()
)


for pair in all_pairs:

    canonical_row = (
        canonical_matchup_lookup[
            pair
        ]
    )

    run_results = []

    run_winners = []

    run_times = []

    stable = True

    matches_canonical = True


    for run_rows in all_run_matchups:

        run_lookup = (
            canonical_matchup_map(
                run_rows
            )
        )

        run_row = run_lookup[
            pair
        ]


        differences = compare_rows(
            canonical_row,
            run_row,
            MATCHUP_COMPARE_FIELDS,
        )


        if differences:

            matches_canonical = False


        run_results.append(
            normalize_value(
                run_row[
                    "Result"
                ]
            )
        )

        run_winners.append(
            normalize_value(
                run_row[
                    "Winner_ID"
                ]
            )
        )

        run_times.append(
            normalize_value(
                run_row[
                    "Combat_Time"
                ]
            )
        )


    if (
        len(
            set(
                run_results
            )
        ) > 1
        or len(
            set(
                run_winners
            )
        ) > 1
        or len(
            set(
                run_times
            )
        ) > 1
    ):

        stable = False


    if not stable:

        unstable_matchups += 1


    if not matches_canonical:

        canonical_mismatches += 1


    matchup_check_rows.append(
        {
            "Unit_1_ID":
                pair[0],

            "Unit_2_ID":
                pair[1],

            "Canonical_Result":
                canonical_row[
                    "Result"
                ],

            "Run_1_Result":
                run_results[0],

            "Run_2_Result":
                run_results[1],

            "Run_3_Result":
                run_results[2],

            "Run_4_Result":
                run_results[3],

            "Run_5_Result":
                run_results[4],

            "Stable_Across_Runs":
                (
                    "Yes"
                    if stable
                    else "No"
                ),

            "Matches_Canonical_BEFORE":
                (
                    "Yes"
                    if matches_canonical
                    else "No"
                ),
        }
    )


# ============================================================
# 16. ПРОВЕРКА UNIT STATISTICS
# ============================================================

unit_check_rows = []

unstable_units = 0

unit_canonical_mismatches = 0


for unit_id in sorted(
    canonical_unit_lookup.keys()
):

    canonical_row = (
        canonical_unit_lookup[
            unit_id
        ]
    )

    run_rows_for_unit = []


    for run_units_rows in all_run_units:

        lookup = {
            row["Unit_ID"]: row
            for row in run_units_rows
        }

        run_rows_for_unit.append(
            lookup[
                unit_id
            ]
        )


    stable = True

    matches_canonical = True


    reference_run = (
        run_rows_for_unit[0]
    )


    for run_row in run_rows_for_unit:

        if compare_rows(
            reference_run,
            run_row,
            UNIT_COMPARE_FIELDS,
        ):

            stable = False


        if compare_rows(
            canonical_row,
            run_row,
            UNIT_COMPARE_FIELDS,
        ):

            matches_canonical = False


    if not stable:

        unstable_units += 1


    if not matches_canonical:

        unit_canonical_mismatches += 1


    unit_check_rows.append(
        {
            "Unit_ID":
                unit_id,

            "Unit_Name":
                canonical_row[
                    "Unit_Name"
                ],

            "Canonical_Combat_Score":
                canonical_row[
                    "Combat_Score"
                ],

            "Run_1_Combat_Score":
                run_rows_for_unit[
                    0
                ][
                    "Combat_Score"
                ],

            "Run_2_Combat_Score":
                run_rows_for_unit[
                    1
                ][
                    "Combat_Score"
                ],

            "Run_3_Combat_Score":
                run_rows_for_unit[
                    2
                ][
                    "Combat_Score"
                ],

            "Run_4_Combat_Score":
                run_rows_for_unit[
                    3
                ][
                    "Combat_Score"
                ],

            "Run_5_Combat_Score":
                run_rows_for_unit[
                    4
                ][
                    "Combat_Score"
                ],

            "Stable_Across_Runs":
                (
                    "Yes"
                    if stable
                    else "No"
                ),

            "Matches_Canonical_BEFORE":
                (
                    "Yes"
                    if matches_canonical
                    else "No"
                ),
        }
    )


# ============================================================
# 17. ПРОВЕРКА ЛОГИЧЕСКИХ SIGNATURE
# ============================================================

unique_signatures = set(
    run_signatures
)


logical_outputs_identical = (
    len(
        unique_signatures
    )
    == 1
)


# ============================================================
# 18. HASH SOURCE ПОСЛЕ ТЕСТА
# ============================================================

source_hash_after = file_sha256(
    UNIT_BALANCE_FILE
)


source_file_unchanged = (
    source_hash_before
    == source_hash_after
)


# ============================================================
# 19. ОБЩИЙ СТАТУС
# ============================================================

if (
    logical_outputs_identical
    and unstable_matchups == 0
    and unstable_units == 0
    and canonical_mismatches == 0
    and unit_canonical_mismatches == 0
    and source_file_unchanged
):

    reproducibility_status = (
        "Reproducible"
    )

else:

    reproducibility_status = (
        "Needs Investigation"
    )


# ============================================================
# 20. SUMMARY
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
            "Combat_Engine",

        "Value":
            "analysis/combat_engine.py",
    },
    {
        "Metric":
            "Runs",

        "Value":
            RUNS,
    },
    {
        "Metric":
            "Units_Per_Run",

        "Value":
            EXPECTED_UNITS,
    },
    {
        "Metric":
            "Matchups_Per_Run",

        "Value":
            EXPECTED_MATCHUPS,
    },
    {
        "Metric":
            "Logical_Outputs_Identical",

        "Value":
            (
                "Yes"
                if logical_outputs_identical
                else "No"
            ),
    },
    {
        "Metric":
            "Unique_Run_Signatures",

        "Value":
            len(
                unique_signatures
            ),
    },
    {
        "Metric":
            "Unstable_Matchups",

        "Value":
            unstable_matchups,
    },
    {
        "Metric":
            "Unstable_Units",

        "Value":
            unstable_units,
    },
    {
        "Metric":
            "Canonical_Matchup_Mismatches",

        "Value":
            canonical_mismatches,
    },
    {
        "Metric":
            "Canonical_Unit_Mismatches",

        "Value":
            unit_canonical_mismatches,
    },
    {
        "Metric":
            "Source_File_Unchanged",

        "Value":
            (
                "Yes"
                if source_file_unchanged
                else "No"
            ),
    },
    {
        "Metric":
            "Source_SHA256_Before",

        "Value":
            source_hash_before,
    },
    {
        "Metric":
            "Source_SHA256_After",

        "Value":
            source_hash_after,
    },
    {
        "Metric":
            "Reproducibility_Status",

        "Value":
            reproducibility_status,
    },
    {
        "Metric":
            "Interpretation",

        "Value":
            (
                "Repeated runs of the canonical "
                "combat engine produced identical "
                "logical results and matched the "
                "canonical BEFORE."
                if reproducibility_status
                == "Reproducible"
                else
                "At least one reproducibility "
                "check failed and requires "
                "investigation."
            ),
    },
]


# ============================================================
# 21. СОХРАНЕНИЕ
# ============================================================

write_csv(
    MATCHUP_CHECK_FILE,
    matchup_check_rows,
)

write_csv(
    UNIT_CHECK_FILE,
    unit_check_rows,
)

write_csv(
    SUMMARY_FILE,
    summary_rows,
)


# ============================================================
# 22. ВЫВОД
# ============================================================

print()
print("=" * 72)
print("REPRODUCIBILITY RESULTS")
print("=" * 72)

print()
print(
    "Runs:",
    RUNS,
)

print(
    "Matchups per run:",
    EXPECTED_MATCHUPS,
)

print(
    "Units per run:",
    EXPECTED_UNITS,
)

print()
print(
    "Logical outputs identical:",
    (
        "Yes"
        if logical_outputs_identical
        else "No"
    ),
)

print(
    "Unique run signatures:",
    len(
        unique_signatures
    ),
)

print()
print(
    "Unstable matchups:",
    unstable_matchups,
)

print(
    "Unstable units:",
    unstable_units,
)

print()
print(
    "Canonical matchup mismatches:",
    canonical_mismatches,
)

print(
    "Canonical unit mismatches:",
    unit_canonical_mismatches,
)

print()
print(
    "Source file unchanged:",
    (
        "Yes"
        if source_file_unchanged
        else "No"
    ),
)

print()
print(
    "Reproducibility Status:",
    reproducibility_status,
)


# ============================================================
# 23. КОНТРОЛЬНЫЙ MATCHUP
# ============================================================

control_pair = tuple(
    sorted(
        [
            "ELF_01",
            "ELF_02",
        ]
    )
)


control_row = None


for row in matchup_check_rows:

    row_pair = tuple(
        sorted(
            [
                row["Unit_1_ID"],
                row["Unit_2_ID"],
            ]
        )
    )

    if row_pair == control_pair:

        control_row = row
        break


print()
print("=" * 72)
print("CONTROL MATCHUP")
print("=" * 72)


if control_row is None:

    print()
    print(
        "ОШИБКА: ELF_01 vs ELF_02 "
        "не найден."
    )

    raise SystemExit


print()
print(
    "ELF_01 vs ELF_02"
)

print(
    "Canonical:",
    control_row[
        "Canonical_Result"
    ],
)

print(
    "Run 1:",
    control_row[
        "Run_1_Result"
    ],
)

print(
    "Run 2:",
    control_row[
        "Run_2_Result"
    ],
)

print(
    "Run 3:",
    control_row[
        "Run_3_Result"
    ],
)

print(
    "Run 4:",
    control_row[
        "Run_4_Result"
    ],
)

print(
    "Run 5:",
    control_row[
        "Run_5_Result"
    ],
)

print(
    "Stable:",
    control_row[
        "Stable_Across_Runs"
    ],
)

print(
    "Matches canonical:",
    control_row[
        "Matches_Canonical_BEFORE"
    ],
)


# ============================================================
# 24. ФИНАЛ
# ============================================================

print()
print("=" * 72)
print("REPRODUCIBILITY CHECK ЗАВЕРШЁН")
print("=" * 72)

print()
print(
    "Matchup check:"
)

print(
    MATCHUP_CHECK_FILE
)

print()
print(
    "Unit check:"
)

print(
    UNIT_CHECK_FILE
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