import pandas as pd


# Загружаем таблицу баланса юнитов из CSV-файла.
unit_balance = pd.read_csv("data/unit_balance.csv")

print("Первые строки таблицы:")
print(unit_balance.head())

print("\nРазмер таблицы:")
print(unit_balance.shape)

print("\nТипы данных до преобразования:")
print(unit_balance.dtypes)


# Перечисляем столбцы, которые должны содержать числовые значения.
numeric_columns = [
    "HP",
    "Damage",
    "Attack_Interval",
    "DPS",
    "Attack_Range",
    "Move_Speed",
    "Cost",
    "HP_per_Cost",
    "DPS_per_Cost"
]

print("\nУникальные значения в числовых столбцах:")

for column in numeric_columns:
    print(f"\n{column}:")
    print(unit_balance[column].unique())


# Преобразуем значения с десятичной запятой в формат,
# который Python может корректно распознать как число.
print("\nПреобразование числовых столбцов:")

for column in numeric_columns:
    unit_balance[column] = (
        unit_balance[column]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    unit_balance[column] = pd.to_numeric(
        unit_balance[column],
        errors="coerce"
    )


print("\nТипы данных после преобразования:")
print(unit_balance[numeric_columns].dtypes)

print("\nКоличество пропущенных значений:")
print(unit_balance.isna().sum())


# Проверяем, что основные игровые параметры имеют положительные значения.
positive_columns = [
    "HP",
    "Damage",
    "Attack_Interval",
    "DPS",
    "Attack_Range",
    "Move_Speed",
    "Cost"
]

print("\nПроверка положительных значений:")

for column in positive_columns:
    invalid_count = (unit_balance[column] <= 0).sum()
    print(f"{column}: {invalid_count}")


# Независимо пересчитываем DPS по формуле:
# DPS = Damage / Attack_Interval.
unit_balance["Calculated_DPS"] = (
    unit_balance["Damage"] / unit_balance["Attack_Interval"]
)

print("\nПроверка расчета DPS:")
print(
    unit_balance[
        ["Unit_ID", "Unit_Name", "DPS", "Calculated_DPS"]
    ]
)


# Рассчитываем абсолютное расхождение между DPS из таблицы
# и значением, которое Python вычислил самостоятельно.
unit_balance["DPS_Error"] = (
    unit_balance["DPS"] - unit_balance["Calculated_DPS"]
).abs()

print("\nПроверка расхождения DPS:")
print(
    unit_balance[
        ["Unit_ID", "Unit_Name", "DPS", "Calculated_DPS", "DPS_Error"]
    ]
)


# Устанавливаем допустимую погрешность и проверяем каждый DPS.
dps_tolerance = 0.000001

unit_balance["DPS_Check"] = (
    unit_balance["DPS_Error"] <= dps_tolerance
)

print("\nАвтоматическая проверка DPS:")
print(
    unit_balance[
        ["Unit_ID", "Unit_Name", "DPS_Error", "DPS_Check"]
    ]
)


# Если все строки прошли проверку — PASS.
# Если хотя бы одна строка содержит ошибку — FAIL.
dps_validation_passed = unit_balance["DPS_Check"].all()

if dps_validation_passed:
    print("\nDPS validation: PASS")
else:
    print("\nDPS validation: FAIL")

# Проверяем, что каждый Unit_ID встречается только один раз.
duplicate_ids = unit_balance["Unit_ID"].duplicated().sum()

print("\nПроверка уникальности Unit_ID:")
print(f"Количество повторяющихся Unit_ID: {duplicate_ids}")

if duplicate_ids == 0:
    print("Unit_ID validation: PASS")
else:
    print("Unit_ID validation: FAIL")

# Список фракций, которые разрешены в текущей версии проекта.
allowed_factions = [
    "Undead",
    "Forest & Dark Elves",
    "Horde"
]

invalid_factions = ~unit_balance["Faction"].isin(allowed_factions)

print("\nПроверка значений Faction:")

if invalid_factions.sum() == 0:
    print("Faction validation: PASS")
else:
    print("Faction validation: FAIL")
    print(unit_balance.loc[invalid_factions, ["Unit_ID", "Unit_Name", "Faction"]])

# Проверяем, что каждому юниту назначена одна из четырёх допустимых ролей.
allowed_roles = [
    "Infantry",
    "Tank",
    "Ranged",
    "Support"
]

invalid_roles = ~unit_balance["Role"].isin(allowed_roles)

print("\nПроверка значений Role:")

if invalid_roles.sum() == 0:
    print("Role validation: PASS")
else:
    print("Role validation: FAIL")
    print(unit_balance.loc[invalid_roles, ["Unit_ID", "Unit_Name", "Role"]])

# Проверяем допустимые типы базовой атаки.
allowed_attack_types = [
    "Melee",
    "Ranged"
]

invalid_attack_types = ~unit_balance["Attack_Type"].isin(allowed_attack_types)

print("\nПроверка значений Attack_Type:")

if invalid_attack_types.sum() == 0:
    print("Attack_Type validation: PASS")
else:
    print("Attack_Type validation: FAIL")
    print(
        unit_balance.loc[
            invalid_attack_types,
            ["Unit_ID", "Unit_Name", "Attack_Type"]
        ]
    )

# Пересчитываем эффективность здоровья относительно стоимости юнита.
unit_balance["Calculated_HP_per_Cost"] = (
    unit_balance["HP"] / unit_balance["Cost"]
)

unit_balance["HP_per_Cost_Error"] = (
    unit_balance["HP_per_Cost"] - unit_balance["Calculated_HP_per_Cost"]
).abs()

hp_cost_tolerance = 0.000001

unit_balance["HP_per_Cost_Check"] = (
    unit_balance["HP_per_Cost_Error"] <= hp_cost_tolerance
)

print("\nПроверка HP_per_Cost:")
print(
    unit_balance[
        [
            "Unit_ID",
            "Unit_Name",
            "HP_per_Cost",
            "Calculated_HP_per_Cost",
            "HP_per_Cost_Error",
            "HP_per_Cost_Check"
        ]
    ]
)

if unit_balance["HP_per_Cost_Check"].all():
    print("HP_per_Cost validation: PASS")
else:
    print("HP_per_Cost validation: FAIL")

# Пересчитываем эффективность урона относительно стоимости юнита.
unit_balance["Calculated_DPS_per_Cost"] = (
    unit_balance["DPS"] / unit_balance["Cost"]
)

unit_balance["DPS_per_Cost_Error"] = (
    unit_balance["DPS_per_Cost"] - unit_balance["Calculated_DPS_per_Cost"]
).abs()

dps_cost_tolerance = 0.000001

unit_balance["DPS_per_Cost_Check"] = (
    unit_balance["DPS_per_Cost_Error"] <= dps_cost_tolerance
)

print("\nПроверка DPS_per_Cost:")
print(
    unit_balance[
        [
            "Unit_ID",
            "Unit_Name",
            "DPS_per_Cost",
            "Calculated_DPS_per_Cost",
            "DPS_per_Cost_Error",
            "DPS_per_Cost_Check"
        ]
    ]
)

if unit_balance["DPS_per_Cost_Check"].all():
    print("DPS_per_Cost validation: PASS")
else:
    print("DPS_per_Cost validation: FAIL")

# Собираем результаты всех основных проверок в одном месте.
missing_values_passed = unit_balance.isna().sum().sum() == 0

positive_values_passed = all(
    (unit_balance[column] > 0).all()
    for column in positive_columns
)

unit_id_validation_passed = duplicate_ids == 0
faction_validation_passed = invalid_factions.sum() == 0
role_validation_passed = invalid_roles.sum() == 0
attack_type_validation_passed = invalid_attack_types.sum() == 0

dps_validation_passed = unit_balance["DPS_Check"].all()
hp_per_cost_validation_passed = unit_balance["HP_per_Cost_Check"].all()
dps_per_cost_validation_passed = unit_balance["DPS_per_Cost_Check"].all()

# Словарь связывает название проверки с её результатом True/False.
validation_results = {
    "Missing values": missing_values_passed,
    "Positive values": positive_values_passed,
    "Unique Unit_ID": unit_id_validation_passed,
    "Faction": faction_validation_passed,
    "Role": role_validation_passed,
    "Attack_Type": attack_type_validation_passed,
    "DPS": dps_validation_passed,
    "HP_per_Cost": hp_per_cost_validation_passed,
    "DPS_per_Cost": dps_per_cost_validation_passed
}
print("\n" + "=" * 50)
print("UNIT BALANCE VALIDATION SUMMARY")
print("=" * 50)

for check_name, passed in validation_results.items():
    status = "PASS" if passed else "FAIL"
    print(f"{check_name}: {status}")

# Общий PASS возможен только тогда, когда прошли абсолютно все проверки.
all_validations_passed = all(validation_results.values())

print("-" * 50)

if all_validations_passed:
    print("UNIT BALANCE VALIDATION: PASS")
else:
    print("UNIT BALANCE VALIDATION: FAIL")

print("=" * 50)
    