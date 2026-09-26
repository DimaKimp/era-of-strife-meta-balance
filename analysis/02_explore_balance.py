import pandas as pd

# Загружаем проверенные данные баланса юнитов.
unit_balance = pd.read_csv("data/unit_balance.csv")

# Преобразуем числовые столбцы из CSV в числа.
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

print("Данные для анализа успешно загружены.")
print(f"Количество юнитов: {len(unit_balance)}")

# Получаем базовую статистику по главным параметрам баланса.
balance_metrics = [
    "HP",
    "DPS",
    "Attack_Range",
    "Move_Speed",
    "Cost",
    "HP_per_Cost",
    "DPS_per_Cost"
]

print("\nОсновная статистика баланса:")
print(
    unit_balance[balance_metrics].describe()
)
# Сравниваем средние параметры юнитов разных ролей.
role_summary = (
    unit_balance
    .groupby("Role")[balance_metrics]
    .mean()
    .round(2)
)

print("\nСредние показатели по ролям:")
print(role_summary)

# Сравниваем средние характеристики трёх фракций.
# Так мы проверяем, отражаются ли задуманные особенности фракций в числах.
faction_summary = (
    unit_balance
    .groupby("Faction")[balance_metrics]
    .mean()
    .round(2)
)

print("\nСредние показатели по фракциям:")
print(faction_summary)

# Сравниваем одинаковые роли между фракциями.
# Это помогает увидеть различия, которые могут скрываться за средними по всей фракции.
faction_role_summary = (
    unit_balance
    .groupby(["Role", "Faction"])[balance_metrics]
    .mean()
    .round(2)
)

print("\nСравнение одинаковых ролей между фракциями:")
print(faction_role_summary)

# Ищем юнитов с минимальными и максимальными значениями характеристик.
# Это помогает быстро находить крайние значения и потенциальные выбросы баланса.
extreme_metrics = [
    "HP",
    "DPS",
    "Attack_Range",
    "Move_Speed",
    "Cost",
    "HP_per_Cost",
    "DPS_per_Cost"
]

print("\nКрайние значения характеристик:")

for metric in extreme_metrics:
    min_value = unit_balance[metric].min()
    max_value = unit_balance[metric].max()

    # Выбираем всех юнитов, которые делят минимальное или максимальное значение.
    min_units = unit_balance.loc[
        unit_balance[metric] == min_value,
        ["Unit_Name", "Faction", "Role", metric]
    ]

    max_units = unit_balance.loc[
        unit_balance[metric] == max_value,
        ["Unit_Name", "Faction", "Role", metric]
    ]

    print(f"\n{metric}:")
    print(f"MIN = {min_value:.2f}")
    print(min_units.to_string(index=False))

    print(f"MAX = {max_value:.2f}")
    print(max_units.to_string(index=False))

    # Сравниваем каждого юнита со средним значением его собственной роли.
# Это помогает искать необычно сильные или слабые характеристики
# не среди всех юнитов сразу, а среди юнитов с похожей игровой функцией.

role_reference = (
    unit_balance
    .groupby("Role")[balance_metrics]
    .mean()
)

print("\n" + "=" * 60)
print("ОТКЛОНЕНИЯ ЮНИТОВ ОТ СРЕДНЕГО ПО ИХ РОЛИ")
print("=" * 60)

for metric in balance_metrics:
    role_average_column = f"{metric}_Role_Avg"
    deviation_column = f"{metric}_vs_Role_pct"

    # Для каждого юнита находим среднее значение его роли.
    unit_balance[role_average_column] = (
        unit_balance["Role"].map(role_reference[metric])
    )

    # Считаем процентное отклонение юнита от среднего по его роли.
    unit_balance[deviation_column] = (
        (
            unit_balance[metric]
            / unit_balance[role_average_column]
        ) - 1
    ) * 100

    print(f"\n{metric}:")
    print(
        unit_balance[
            [
                "Unit_Name",
                "Faction",
                "Role",
                metric,
                role_average_column,
                deviation_column
            ]
        ]
        .sort_values(deviation_column, ascending=False)
        .round(2)
        .to_string(index=False)
    )

    # Выделяем заметные отклонения от среднего значения внутри роли.
# Порог 10% используется как фильтр для дальнейшего анализа,
# а не как автоматический признак дисбаланса.

deviation_threshold = 10

print("\n" + "=" * 60)
print(f"ЗАМЕТНЫЕ ОТКЛОНЕНИЯ ОТ СРЕДНЕГО ПО РОЛИ (>= {deviation_threshold}%)")
print("=" * 60)

for metric in balance_metrics:
    deviation_column = f"{metric}_vs_Role_pct"

    notable_deviations = unit_balance.loc[
        unit_balance[deviation_column].abs() >= deviation_threshold,
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            metric,
            deviation_column
        ]
    ].copy()

    notable_deviations = notable_deviations.sort_values(
        deviation_column,
        ascending=False
    )

    print(f"\n{metric}:")

    if notable_deviations.empty:
        print("Заметных отклонений не обнаружено.")
    else:
        print(
            notable_deviations
            .round(2)
            .to_string(index=False)
        )

# Собираем все заметные отклонения в одну таблицу,
# чтобы сохранить результат анализа в отдельный CSV-файл.

deviation_results = []

for metric in balance_metrics:
    deviation_column = f"{metric}_vs_Role_pct"

    metric_deviations = unit_balance.loc[
        unit_balance[deviation_column].abs() >= deviation_threshold,
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            metric,
            deviation_column
        ]
    ].copy()

    if not metric_deviations.empty:
        # Приводим разные показатели к единой структуре таблицы.
        metric_deviations["Metric"] = metric
        metric_deviations["Value"] = metric_deviations[metric]
        metric_deviations["Deviation_pct"] = (
            metric_deviations[deviation_column]
        )

        metric_deviations = metric_deviations[
            [
                "Unit_ID",
                "Unit_Name",
                "Faction",
                "Role",
                "Metric",
                "Value",
                "Deviation_pct"
            ]
        ]

        deviation_results.append(metric_deviations)


if deviation_results:
    notable_deviations_table = pd.concat(
        deviation_results,
        ignore_index=True
    )

    notable_deviations_table = notable_deviations_table.sort_values(
        "Deviation_pct",
        key=lambda column: column.abs(),
        ascending=False
    )

    notable_deviations_table.to_csv(
        "data/notable_deviations.csv",
        index=False
    )

    print(
        "\nРезультаты сохранены: "
        "data/notable_deviations.csv"
    )
else:
    print("\nЗаметных отклонений для сохранения нет.")

