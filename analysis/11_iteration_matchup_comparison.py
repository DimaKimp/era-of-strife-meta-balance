import csv
import os


# ============================================================
# 1. ПУТИ К ФАЙЛАМ
# ============================================================

UNIT_BALANCE_FILE = "data/unit_balance.csv"

ITERATION_FILE = (
    "analysis/results/iterations/"
    "balance_iteration_01.csv"
)

OUTPUT_DIR = (
    "analysis/results/iterations/"
    "matchup_comparison"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_matchup_comparison.csv",
)


# ============================================================
# 2. СОЗДАЁМ ПАПКУ ДЛЯ РЕЗУЛЬТАТОВ
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)


# ============================================================
# 3. ЗАГРУЗКА CSV
# ============================================================

def load_csv(file_path):
    """
    Загружает CSV-файл и возвращает список строк.

    Каждая строка CSV становится словарём вида:

    {
        "Unit_ID": "...",
        "Unit_Name": "...",
        ...
    }
    """

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


# ============================================================
# 4. ЗАГРУЖАЕМ ДАННЫЕ
# ============================================================

unit_rows = load_csv(
    UNIT_BALANCE_FILE
)

iteration_rows = load_csv(
    ITERATION_FILE
)


# ============================================================
# 5. ПРОВЕРЯЕМ ЗАГРУЗКУ
# ============================================================

print("=" * 70)
print("ERA OF STRIFE — ITERATION MATCHUP COMPARISON")
print("=" * 70)

print()

print(
    "Загружено юнитов из unit_balance.csv:",
    len(unit_rows),
)

print(
    "Загружено строк Iteration 01:",
    len(iteration_rows),
)

print()

print("Юниты Iteration 01:")

for row in iteration_rows:

    print(
        "-",
        row["Unit_ID"],
        "|",
        row["Unit_Name"],
    )


# ============================================================
# 6. ПРЕОБРАЗОВАНИЕ ЧИСЛОВЫХ ПОЛЕЙ
# ============================================================

NUMERIC_FIELDS = [
    "HP",
    "Damage",
    "Attack_Interval",
    "DPS",
    "Cost",
]


def convert_number(value):
    """
    Преобразует строковое числовое значение в float.

    Поддерживаются оба варианта десятичного разделителя:

    0.9
    0,9
    """

    if isinstance(value, (int, float)):
        return float(value)

    normalized_value = (
        str(value)
        .strip()
        .replace(",", ".")
    )

    return float(normalized_value)


def convert_unit_numbers(unit):
    """
    Создаёт копию строки юнита и преобразует
    необходимые числовые поля в float.
    """

    converted_unit = unit.copy()

    for field in NUMERIC_FIELDS:

        if (
            field in converted_unit
            and converted_unit[field] != ""
        ):

            converted_unit[field] = convert_number(
                converted_unit[field]
            )

    return converted_unit


# ============================================================
# 7. СОЗДАЁМ СОСТОЯНИЕ BEFORE
# ============================================================

before_units = {}

for row in unit_rows:

    unit = convert_unit_numbers(row)

    unit_id = unit["Unit_ID"]

    before_units[unit_id] = unit


# ============================================================
# 8. СОЗДАЁМ СОСТОЯНИЕ AFTER
# ============================================================

after_units = {}

for unit_id, unit in before_units.items():

    after_units[unit_id] = unit.copy()


# ============================================================
# 9. ПРИМЕНЯЕМ ИЗМЕНЕНИЯ ITERATION 01
# ============================================================

applied_changes = []

for row in iteration_rows:

    # Изменяем только тех юнитов, которых действительно
    # выбрали кандидатами на Buff или Nerf.
    if row["Iteration_Target"] not in [
        "Buff Candidate",
        "Nerf Candidate",
    ]:
        continue

    unit_id = row["Unit_ID"]

    changed_parameter = row["Changed_Parameter"]

    # Защита от пустого параметра.
    if changed_parameter == "":
        continue

    # Проверяем, существует ли такой юнит.
    if unit_id not in after_units:
        continue

    # Проверяем, существует ли изменяемый параметр.
    if changed_parameter not in after_units[unit_id]:
        continue

    new_value = convert_number(
        row["New_Value"]
    )

    old_value = after_units[unit_id][
        changed_parameter
    ]

    after_units[unit_id][
        changed_parameter
    ] = new_value

    applied_changes.append(
        {
            "Unit_ID": unit_id,
            "Unit_Name": row["Unit_Name"],
            "Iteration_Target": row["Iteration_Target"],
            "Parameter": changed_parameter,
            "Old_Value": old_value,
            "New_Value": new_value,
        }
    )


# ============================================================
# 10. ПЕРЕСЧИТЫВАЕМ ЗАВИСИМЫЕ ХАРАКТЕРИСТИКИ
# ============================================================

for unit in after_units.values():

    if (
        "Damage" in unit
        and "Attack_Interval" in unit
        and unit["Attack_Interval"] != 0
    ):

        unit["DPS"] = (
            unit["Damage"]
            / unit["Attack_Interval"]
        )


# ============================================================
# 11. ПРОВЕРЯЕМ ПРИМЕНЁННЫЕ ИЗМЕНЕНИЯ
# ============================================================

print()
print("=" * 70)
print("ПРИМЕНЁННЫЕ ИЗМЕНЕНИЯ ITERATION 01")
print("=" * 70)

print()

print(
    "Количество прямых изменений:",
    len(applied_changes),
)

for change in applied_changes:

    print()

    print(
        change["Unit_ID"],
        "|",
        change["Unit_Name"],
    )

    print(
        "  Тип:",
        change["Iteration_Target"],
    )

    print(
        "  Параметр:",
        change["Parameter"],
    )

    print(
        "  BEFORE:",
        change["Old_Value"],
    )

    print(
        "  AFTER:",
        change["New_Value"],
    )


# ============================================================
# 12. КОНТРОЛЬНАЯ ПРОВЕРКА DPS
# ============================================================

print()
print("=" * 70)
print("КОНТРОЛЬ DPS")
print("=" * 70)

for change in applied_changes:

    unit_id = change["Unit_ID"]

    print()

    print(
        unit_id,
        "|",
        change["Unit_Name"],
    )

    print(
        "  Damage:",
        before_units[unit_id]["Damage"],
        "->",
        after_units[unit_id]["Damage"],
    )

    print(
        "  DPS:",
        round(
            before_units[unit_id]["DPS"],
            2,
        ),
        "->",
        round(
            after_units[unit_id]["DPS"],
            2,
        ),
    )


# ============================================================
# 13. СОЗДАЁМ MATCHUP COMPARISON
# ============================================================

comparison_rows = []

for row in iteration_rows:

    unit_id = row["Unit_ID"]

    if unit_id not in before_units:
        continue

    if unit_id not in after_units:
        continue

    before_unit = before_units[unit_id]
    after_unit = after_units[unit_id]

    before_damage = before_unit["Damage"]
    after_damage = after_unit["Damage"]

    before_dps = before_unit["DPS"]
    after_dps = after_unit["DPS"]

    damage_change = (
        after_damage
        - before_damage
    )

    dps_change = (
        after_dps
        - before_dps
    )

    if before_damage != 0:

        damage_change_percent = (
            damage_change
            / before_damage
            * 100
        )

    else:

        damage_change_percent = 0.0

    if before_dps != 0:

        dps_change_percent = (
            dps_change
            / before_dps
            * 100
        )

    else:

        dps_change_percent = 0.0

    if row["Iteration_Target"] in [
        "Buff Candidate",
        "Nerf Candidate",
    ]:

        change_type = "Direct"

    else:

        change_type = "Indirect / Unchanged"

    comparison_rows.append(
        {
            "Unit_ID": unit_id,
            "Unit_Name": row["Unit_Name"],
            "Faction": row["Faction"],
            "Role": row["Role"],
            "Iteration_Target": row["Iteration_Target"],
            "Change_Type": change_type,
            "Before_Damage": round(
                before_damage,
                4,
            ),
            "After_Damage": round(
                after_damage,
                4,
            ),
            "Damage_Change": round(
                damage_change,
                4,
            ),
            "Damage_Change_Percent": round(
                damage_change_percent,
                2,
            ),
            "Before_DPS": round(
                before_dps,
                4,
            ),
            "After_DPS": round(
                after_dps,
                4,
            ),
            "DPS_Change": round(
                dps_change,
                4,
            ),
            "DPS_Change_Percent": round(
                dps_change_percent,
                2,
            ),
        }
    )


# ============================================================
# 14. ВЫВОДИМ СРАВНЕНИЕ В ТЕРМИНАЛ
# ============================================================

print()
print("=" * 70)
print("СРАВНЕНИЕ BEFORE / AFTER")
print("=" * 70)

for row in comparison_rows:

    print()

    print(
        row["Unit_ID"],
        "|",
        row["Unit_Name"],
    )

    print(
        "  Iteration Target:",
        row["Iteration_Target"],
    )

    print(
        "  Change Type:",
        row["Change_Type"],
    )

    print(
        "  Damage:",
        row["Before_Damage"],
        "->",
        row["After_Damage"],
    )

    print(
        "  Damage Change:",
        row["Damage_Change"],
        "(",
        row["Damage_Change_Percent"],
        "% )",
    )

    print(
        "  DPS:",
        row["Before_DPS"],
        "->",
        row["After_DPS"],
    )

    print(
        "  DPS Change:",
        row["DPS_Change"],
        "(",
        row["DPS_Change_Percent"],
        "% )",
    )


# ============================================================
# 15. СОХРАНЯЕМ РЕЗУЛЬТАТ В CSV
# ============================================================

FIELDNAMES = [
    "Unit_ID",
    "Unit_Name",
    "Faction",
    "Role",
    "Iteration_Target",
    "Change_Type",
    "Before_Damage",
    "After_Damage",
    "Damage_Change",
    "Damage_Change_Percent",
    "Before_DPS",
    "After_DPS",
    "DPS_Change",
    "DPS_Change_Percent",
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=FIELDNAMES,
    )

    writer.writeheader()

    writer.writerows(
        comparison_rows
    )


# ============================================================
# 16. КРАТКАЯ СВОДКА ПО ITERATION 01
# ============================================================

buff_count = 0
nerf_count = 0
unchanged_count = 0

for row in iteration_rows:

    if row["Iteration_Target"] == "Buff Candidate":

        buff_count += 1

    elif row["Iteration_Target"] == "Nerf Candidate":

        nerf_count += 1

    else:

        unchanged_count += 1


print()
print("=" * 70)
print("СВОДКА ITERATION 01")
print("=" * 70)

print(
    "Buff Candidate:",
    buff_count,
)

print(
    "Nerf Candidate:",
    nerf_count,
)

print(
    "Без прямого изменения:",
    unchanged_count,
)

print(
    "Всего юнитов:",
    len(iteration_rows),
)


# ============================================================
# 17. ЗАВЕРШЕНИЕ
# ============================================================

print()
print("=" * 70)
print("ITERATION MATCHUP COMPARISON ЗАВЕРШЁН")
print("=" * 70)

print()

print("Результат сохранён:")
print(OUTPUT_FILE)

print()

print(
    "Исходный data/unit_balance.csv "
    "не изменялся."
)