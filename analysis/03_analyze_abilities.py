import pandas as pd
import math

# Загружаем таблицу с параметрами способностей.
ability_balance = pd.read_csv("data/ability_balance.csv")


print("Данные Ability Balance успешно загружены.")
print(f"Количество строк: {len(ability_balance)}")


# Смотрим структуру таблицы и первые строки.
print("\nСтолбцы таблицы:")
print(ability_balance.columns.tolist())

print("\nПервые 10 строк:")
print(ability_balance.head(10))


# Проверяем количество уникальных способностей и юнитов.
ability_count = ability_balance["Ability_ID"].nunique()
unit_count = ability_balance["Unit_ID"].nunique()

print("\nКоличество уникальных способностей:", ability_count)
print("Количество юнитов со способностями:", unit_count)

# Проверяем, есть ли в таблице пропущенные значения.
print("\nКоличество пропущенных значений:")
print(ability_balance.isna().sum())

missing_values_passed = not ability_balance.isna().any().any()

if missing_values_passed:
    print("Missing values validation: PASS")
else:
    print("Missing values validation: FAIL")


# Проверяем, что один Ability_ID не связан с разными юнитами или названиями.
ability_consistency = (
    ability_balance
    .groupby("Ability_ID")
    .agg(
        Unit_ID_count=("Unit_ID", "nunique"),
        Ability_Name_count=("Ability_Name", "nunique"),
        Ability_Type_count=("Ability_Type", "nunique")
    )
)

invalid_abilities = ability_consistency[
    (ability_consistency["Unit_ID_count"] != 1)
    | (ability_consistency["Ability_Name_count"] != 1)
    | (ability_consistency["Ability_Type_count"] != 1)
]

print("\nПроверка целостности Ability_ID:")

if invalid_abilities.empty:
    print("Ability consistency validation: PASS")
else:
    print("Ability consistency validation: FAIL")
    print(invalid_abilities)


# Проверяем, нет ли одного и того же параметра,
# случайно записанного дважды внутри одной способности.
duplicate_parameters = ability_balance.duplicated(
    subset=["Ability_ID", "Parameter"],
    keep=False
)

print("\nПроверка повторяющихся параметров:")

if duplicate_parameters.sum() == 0:
    print("Duplicate parameters validation: PASS")
else:
    print("Duplicate parameters validation: FAIL")
    print(
        ability_balance.loc[
            duplicate_parameters,
            ["Ability_ID", "Ability_Name", "Parameter", "Value", "Unit"]
        ]
    )

# Загружаем список юнитов и проверяем связь Ability_Balance с Unit_Balance.
unit_balance = pd.read_csv("data/unit_balance.csv")

known_unit_ids = set(unit_balance["Unit_ID"])
ability_unit_ids = set(ability_balance["Unit_ID"])

unknown_unit_ids = ability_unit_ids - known_unit_ids
units_without_abilities = known_unit_ids - ability_unit_ids


print("\nПроверка связи Ability_Balance с Unit_Balance:")

if not unknown_unit_ids:
    print("Unknown Unit_ID validation: PASS")
else:
    print("Unknown Unit_ID validation: FAIL")
    print("Неизвестные Unit_ID:", sorted(unknown_unit_ids))


if not units_without_abilities:
    print("Units with abilities validation: PASS")
else:
    print("Units with abilities validation: FAIL")
    print("Юниты без способностей:", sorted(units_without_abilities))

# Проверяем правило текущей версии дизайна:
# каждому юниту должна соответствовать ровно одна уникальная способность.
abilities_per_unit = (
    ability_balance
    .groupby("Unit_ID")["Ability_ID"]
    .nunique()
)

print("\nКоличество способностей у каждого юнита:")
print(abilities_per_unit)


invalid_ability_count = abilities_per_unit[abilities_per_unit != 1]

if invalid_ability_count.empty:
    print("One ability per unit validation: PASS")
else:
    print("One ability per unit validation: FAIL")
    print("Юниты с неправильным количеством способностей:")
    print(invalid_ability_count)

# Преобразуем параметры способностей из длинного формата в широкий.
# Теперь одна строка будет соответствовать одной способности.
ability_wide = (
    ability_balance
    .pivot_table(
        index=[
            "Ability_ID",
            "Unit_ID",
            "Ability_Name",
            "Ability_Type"
        ],
        columns="Parameter",
        values="Value",
        aggfunc="first"
    )
    .reset_index()
)

# Убираем служебное имя оси столбцов после pivot_table.
ability_wide.columns.name = None

print("\nАналитическая таблица способностей:")
print(ability_wide.to_string(index=False))

# Выбираем способности, для которых одновременно известны
# длительность эффекта и время перезарядки.
uptime_analysis = ability_wide.loc[
    ability_wide["Duration"].notna()
    & ability_wide["Cooldown"].notna(),
    [
        "Ability_ID",
        "Unit_ID",
        "Ability_Name",
        "Ability_Type",
        "Duration",
        "Cooldown"
    ]
].copy()

# Рассчитываем теоретическую долю активного времени способности.
uptime_analysis["Uptime_pct"] = (
    uptime_analysis["Duration"]
    / uptime_analysis["Cooldown"]
    * 100
)

print("\nАнализ теоретического uptime способностей:")
print(
    uptime_analysis
    .sort_values("Uptime_pct", ascending=False)
    .round(2)
    .to_string(index=False)
)   

# Рассчитываем теоретическое время между окончанием эффекта
# и следующим возможным использованием способности.
uptime_analysis["Downtime"] = (
    uptime_analysis["Cooldown"]
    - uptime_analysis["Duration"]
)

print("\nUptime и downtime способностей:")
print(
    uptime_analysis[
        [
            "Unit_ID",
            "Ability_Name",
            "Duration",
            "Cooldown",
            "Uptime_pct",
            "Downtime"
        ]
    ]
    .sort_values("Uptime_pct", ascending=False)
    .round(2)
    .to_string(index=False)
)
# Выбираем основные числовые модификаторы боевых характеристик.
# Пока не объединяем их в один показатель силы, потому что эффекты имеют разный смысл.
combat_modifier_columns = [
    "Attack_Speed_Bonus",
    "Attack_Speed_Reduction",
    "Damage_Reduction",
    "Damage_Multiplier"
]

print("\nОсновные боевые модификаторы способностей:")

for modifier in combat_modifier_columns:
    modifier_abilities = ability_wide.loc[
        ability_wide[modifier].notna(),
        [
            "Unit_ID",
            "Ability_Name",
            modifier
        ]
    ]

    print(f"\n{modifier}:")

    if modifier_abilities.empty:
        print("Способности с таким модификатором отсутствуют.")
    else:
        print(
            modifier_abilities
            .round(2)
            .to_string(index=False)
        )
# Проверяем структуру Unit Balance перед объединением таблиц.
print("\nСтолбцы Unit Balance:")
print(unit_balance.columns.tolist())   

# Объединяем способности с базовыми характеристиками их владельцев.
ability_with_units = ability_wide.merge(
    unit_balance[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "HP",
            "Damage",
            "DPS",
            "Cost"
        ]
    ],
    on="Unit_ID",
    how="left"
)

print("\nСпособности после объединения с Unit Balance:")
print(
    ability_with_units[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "Ability_Name",
            "Damage",
            "DPS",
            "Cost"
        ]
    ].to_string(index=False)
)
# Проверяем, что после объединения каждая способность
# получила данные соответствующего юнита.
merge_check_columns = [
    "Unit_Name",
    "Faction",
    "Role",
    "Damage",
    "DPS",
    "Cost"
]

missing_after_merge = ability_with_units[
    merge_check_columns
].isna().any(axis=1)

print("\nПроверка объединения Ability Balance и Unit Balance:")

if not missing_after_merge.any():
    print("Ability + Unit merge validation: PASS")
else:
    print("Ability + Unit merge validation: FAIL")
    print("Строки с отсутствующими данными:")
    print(
        ability_with_units.loc[
            missing_after_merge,
            [
                "Ability_ID",
                "Unit_ID",
                "Ability_Name"
            ] + merge_check_columns
        ].to_string(index=False)
    )

    # Выбираем способности, у которых задан множитель урона.
damage_multiplier_abilities = ability_with_units.loc[
    ability_with_units["Damage_Multiplier"].notna()
].copy()

print("\nСпособности с Damage_Multiplier:")
print(
    damage_multiplier_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Damage",
            "Damage_Multiplier"
        ]
    ].to_string(index=False)
)

# Преобразуем данные, участвующие в расчёте, в числовой формат.
damage_multiplier_abilities["Damage"] = pd.to_numeric(
    damage_multiplier_abilities["Damage"],
    errors="raise"
)

damage_multiplier_abilities["Damage_Multiplier"] = pd.to_numeric(
    damage_multiplier_abilities["Damage_Multiplier"],
    errors="raise"
)
# Рассчитываем фактический урон способности
# на основе базового Damage юнита и множителя способности.
damage_multiplier_abilities["Calculated_Ability_Damage"] = (
    damage_multiplier_abilities["Damage"]
    * damage_multiplier_abilities["Damage_Multiplier"]
)

print("\nРасчёт урона способностей:")
print(
    damage_multiplier_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Damage",
            "Damage_Multiplier",
            "Calculated_Ability_Damage"
        ]
    ].to_string(index=False)
)

# Выбираем способности, у которых урон задаётся отдельно для каждого снаряда.
damage_per_knife_abilities = ability_with_units.loc[
    ability_with_units["Damage_Per_Knife"].notna()
].copy()

print("\nСпособности с Damage_Per_Knife:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Damage",
            "Damage_Per_Knife",
            "Knife_Count",
        ]
    ].to_string(index=False)
)

# Преобразуем параметры Knife Barrage в числовой формат.
damage_per_knife_abilities["Damage"] = pd.to_numeric(
    damage_per_knife_abilities["Damage"],
    errors="raise"
)

damage_per_knife_abilities["Damage_Per_Knife"] = pd.to_numeric(
    damage_per_knife_abilities["Damage_Per_Knife"],
    errors="raise"
)

damage_per_knife_abilities["Knife_Count"] = pd.to_numeric(
    damage_per_knife_abilities["Knife_Count"],
    errors="raise"
)

# Рассчитываем урон одного ножа.
damage_per_knife_abilities["Damage_Per_Projectile"] = (
    damage_per_knife_abilities["Damage"]
    * damage_per_knife_abilities["Damage_Per_Knife"]
)

# Рассчитываем максимальный урон всей серии.
damage_per_knife_abilities["Max_Barrage_Damage"] = (
    damage_per_knife_abilities["Damage_Per_Projectile"]
    * damage_per_knife_abilities["Knife_Count"]
)

print("\nРасчёт урона многоснарядных способностей:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Damage",
            "Damage_Per_Knife",
            "Knife_Count",
            "Damage_Per_Projectile",
            "Max_Barrage_Damage",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# Добавляем интервал между снарядами из таблицы способностей.
damage_per_knife_abilities["Knife_Interval"] = pd.to_numeric(
    damage_per_knife_abilities["Knife_Interval"],
    errors="raise"
)

# Если первый снаряд выпускается сразу,
# между N снарядами существует N - 1 интервалов.
damage_per_knife_abilities["Barrage_Duration"] = (
    (damage_per_knife_abilities["Knife_Count"] - 1)
    * damage_per_knife_abilities["Knife_Interval"]
)

print("\nВремя исполнения многоснарядных способностей:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Knife_Count",
            "Knife_Interval",
            "Barrage_Duration",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# Рассчитываем интенсивность урона только во время самой серии.
# Это Burst DPS, а не обычный DPS юнита.
damage_per_knife_abilities["Burst_DPS"] = (
    damage_per_knife_abilities["Max_Barrage_Damage"]
    / damage_per_knife_abilities["Barrage_Duration"]
)

print("\nBurst-анализ многоснарядных способностей:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "DPS",
            "Max_Barrage_Damage",
            "Barrage_Duration",
            "Burst_DPS",
        ]
    ]
    .round(2)
    .to_string(index=False)
)
# Преобразуем Cooldown в числовой формат.
damage_per_knife_abilities["Cooldown"] = pd.to_numeric(
    damage_per_knife_abilities["Cooldown"],
    errors="raise"
)

# Рассчитываем средний вклад способности в урон
# на полном цикле её перезарядки.
#
# Cooldown Knife Barrage начинается в момент активации,
# поэтому полный цикл равен Cooldown, а не
# Cooldown + Barrage_Duration.
damage_per_knife_abilities["Ability_DPS_Avg"] = (
    damage_per_knife_abilities["Max_Barrage_Damage"]
    / damage_per_knife_abilities["Cooldown"]
)

print("\nДолгосрочный анализ урона способности:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "DPS",
            "Burst_DPS",
            "Cooldown",
            "Ability_DPS_Avg",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# Учитываем потерю обычных атак во время Knife Barrage.

# Attack_Allowed = 0 означает:
# во время способности юнит не может выполнять обычные атаки.
damage_per_knife_abilities["Replaced_Basic_Damage"] = (
    damage_per_knife_abilities["DPS"]
    * damage_per_knife_abilities["Barrage_Duration"]
)

# Считаем чистый дополнительный урон способности.
# Из полного урона Barrage вычитаем тот урон,
# который юнит и так нанёс бы обычными атаками.
damage_per_knife_abilities["Net_Ability_Damage"] = (
    damage_per_knife_abilities["Max_Barrage_Damage"]
    - damage_per_knife_abilities["Replaced_Basic_Damage"]
)

# Переводим чистый дополнительный урон
# в средний дополнительный DPS на полном цикле способности.
damage_per_knife_abilities["Net_Ability_DPS"] = (
    damage_per_knife_abilities["Net_Ability_Damage"]
    / damage_per_knife_abilities["Cooldown"]
)

# Итоговый теоретический DPS:
# обычный DPS + чистый средний вклад способности.
damage_per_knife_abilities["Effective_DPS"] = (
    damage_per_knife_abilities["DPS"]
    + damage_per_knife_abilities["Net_Ability_DPS"]
)

print("\nРеальный вклад Knife Barrage с учётом замещения обычных атак:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "DPS",
            "Barrage_Duration",
            "Replaced_Basic_Damage",
            "Max_Barrage_Damage",
            "Net_Ability_Damage",
            "Net_Ability_DPS",
            "Effective_DPS",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# Читаем правило Attack_Allowed из Ability Balance.

attack_allowed_abilities = ability_with_units.loc[
    ability_with_units["Attack_Allowed"].notna()
].copy()

# Преобразуем значение в число.
attack_allowed_abilities["Attack_Allowed"] = pd.to_numeric(
    attack_allowed_abilities["Attack_Allowed"],
    errors="raise"
)

print("\nПроверка правила Attack_Allowed:")
print(
    attack_allowed_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Attack_Allowed",
        ]
    ]
    .to_string(index=False)
)
print("\nKnife Barrage и правило Attack_Allowed:")
print(
    damage_per_knife_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Attack_Allowed",
        ]
    ].to_string(index=False)
)


# Анализ ограничения движения во время способностей

# Выбираем только способности, для которых явно задано
# правило Movement_Allowed.
movement_allowed_abilities = ability_with_units.loc[
    ability_with_units["Movement_Allowed"].notna()
].copy()

# Преобразуем значение в числовой формат:
# 1 = движение разрешено
# 0 = движение запрещено
movement_allowed_abilities["Movement_Allowed"] = pd.to_numeric(
    movement_allowed_abilities["Movement_Allowed"],
    errors="raise"
)

print("\nПроверка правила Movement_Allowed:")
print(
    movement_allowed_abilities[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Movement_Allowed",
        ]
    ].to_string(index=False)
)


# АНАЛИЗ FOCUSED BOLT

# Выбираем только способность Focused Bolt.
focused_bolt = ability_with_units.loc[
    ability_with_units["Ability_Name"] == "Focused Bolt"
].copy()
print("\nИсходные параметры Focused Bolt:")

focused_bolt_columns = [
    "Ability_ID",
    "Unit_ID",
    "Unit_Name",
    "Ability_Name",
    "Ability_Type",
    "Damage",
    "DPS",
    "Damage_Multiplier",
    "Charge_Time",
    "Cooldown",
    "Cancel_Cooldown",
    "Movement_Allowed",
    "Attack_Allowed",
    "Projectile_Collision",
    "Pierces_Units",
]

print(
    focused_bolt[
        focused_bolt_columns
    ].to_string(index=False)
)

# Расчёт базового урона Focused Bolt


# Преобразуем необходимые параметры в числовой формат.
focused_bolt["Damage"] = pd.to_numeric(
    focused_bolt["Damage"],
    errors="raise"
)

focused_bolt["Damage_Multiplier"] = pd.to_numeric(
    focused_bolt["Damage_Multiplier"],
    errors="raise"
)
# Полный урон способности при успешном попадании.
focused_bolt["Focused_Bolt_Damage"] = (
    focused_bolt["Damage"]
    * focused_bolt["Damage_Multiplier"]
)
print("\nРасчёт урона Focused Bolt:")
print(
    focused_bolt[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Damage",
            "Damage_Multiplier",
            "Focused_Bolt_Damage",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# РЕАЛЬНЫЙ ВКЛАД FOCUSED BOLT

# Во время Charge_Time маг не может выполнять обычные атаки.
# Поэтому сначала рассчитываем, сколько обычного урона
# он мог бы нанести за время подготовки способности.
focused_bolt["Replaced_Basic_Damage"] = (
    focused_bolt["DPS"]
    * focused_bolt["Charge_Time"]
)

# Теперь определяем чистый дополнительный урон способности.
# Из полного урона Focused Bolt вычитаем урон обычных атак,
# который был потерян во время подготовки.
focused_bolt["Net_Ability_Damage"] = (
    focused_bolt["Focused_Bolt_Damage"]
    - focused_bolt["Replaced_Basic_Damage"]
)

print("\nРеальный вклад Focused Bolt с учётом потерянных обычных атак:")
print(
    focused_bolt[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "DPS",
            "Charge_Time",
            "Replaced_Basic_Damage",
            "Focused_Bolt_Damage",
            "Net_Ability_Damage",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# ДОЛГОСРОЧНЫЙ ВКЛАД FOCUSED BOLT


# По нашим правилам Cooldown Focused Bolt начинается
# после успешного завершения двухсекундной подготовки.
# Поэтому полный цикл способности:
# Charge_Time + Cooldown.
focused_bolt["Ability_Cycle"] = (
    focused_bolt["Charge_Time"]
    + focused_bolt["Cooldown"]
)

# Средний дополнительный DPS, который даёт способность
# при успешном использовании по готовности.
focused_bolt["Net_Ability_DPS"] = (
    focused_bolt["Net_Ability_Damage"]
    / focused_bolt["Ability_Cycle"]
)

# Итоговый эффективный DPS:
# обычный DPS + средний дополнительный DPS способности.
focused_bolt["Effective_DPS"] = (
    focused_bolt["DPS"]
    + focused_bolt["Net_Ability_DPS"]
)

# Процентное изменение DPS относительно обычных атак.
focused_bolt["DPS_Increase_Percent"] = (
    (
        focused_bolt["Effective_DPS"]
        / focused_bolt["DPS"]
    )
    - 1
) * 100

print("\nДолгосрочный анализ Focused Bolt:")
print(
    focused_bolt[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "DPS",
            "Charge_Time",
            "Cooldown",
            "Ability_Cycle",
            "Net_Ability_Damage",
            "Net_Ability_DPS",
            "Effective_DPS",
            "DPS_Increase_Percent",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# АНАЛИЗ ПРЕРЫВАНИЯ FOCUSED BOLT


# Focused Bolt можно прервать во время двухсекундной подготовки.
# Чем позже происходит прерывание, тем больше времени маг уже
# потратил без выполнения обычных атак.
#
# Рассматриваем три тестовых сценария:
# Early Interrupt = 0.5 сек.
# Mid Interrupt   = 1.0 сек.
# Late Interrupt  = 1.5 сек.

interrupt_scenarios = pd.DataFrame(
    {
        "Scenario": [
            "Early Interrupt",
            "Mid Interrupt",
            "Late Interrupt",
        ],
        "Interrupt_Time": [
            0.5,
            1.0,
            1.5,
        ],
    }
)

print("\nСценарии прерывания Focused Bolt:")
print(
    interrupt_scenarios.to_string(index=False)
)
# Берём DPS мага непосредственно из таблицы focused_bolt.
# iloc[0] означает: взять первую строку найденной способности.
mage_dps = focused_bolt["DPS"].iloc[0]

# Берём штрафной cooldown после отмены Focused Bolt.
cancel_cooldown = focused_bolt["Cancel_Cooldown"].iloc[0]

# Добавляем эти значения к каждому тестовому сценарию.
interrupt_scenarios["DPS"] = mage_dps
interrupt_scenarios["Cancel_Cooldown"] = cancel_cooldown

# Считаем обычный урон, который маг мог бы нанести
# за время, уже потраченное на неудачный каст.
interrupt_scenarios["Lost_Basic_Damage"] = (
    interrupt_scenarios["DPS"]
    * interrupt_scenarios["Interrupt_Time"]
)

print("\nПотерянный обычный урон при прерывании Focused Bolt:")
print(
    interrupt_scenarios[
        [
            "Scenario",
            "Interrupt_Time",
            "DPS",
            "Cancel_Cooldown",
            "Lost_Basic_Damage",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# ПОЛНАЯ ВРЕМЕННАЯ ЦЕНА ПРЕРВАННОГО FOCUSED BOLT

# После прерывания игрок уже потратил часть времени на зарядку,
# а затем должен дождаться Cancel_Cooldown,
# прежде чем сможет снова попытаться использовать Focused Bolt.
interrupt_scenarios["Failed_Attempt_Window"] = (
    interrupt_scenarios["Interrupt_Time"]
    + interrupt_scenarios["Cancel_Cooldown"]
)

# Насколько позднее прерывание увеличивает временную цену
# по сравнению с ранним прерыванием.
early_window = interrupt_scenarios["Failed_Attempt_Window"].iloc[0]

interrupt_scenarios["Extra_Time_vs_Early"] = (
    interrupt_scenarios["Failed_Attempt_Window"]
    - early_window
)

print("\nПолная временная цена прерванного Focused Bolt:")
print(
    interrupt_scenarios[
        [
            "Scenario",
            "Interrupt_Time",
            "Cancel_Cooldown",
            "Failed_Attempt_Window",
            "Lost_Basic_Damage",
            "Extra_Time_vs_Early",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# EXPECTED VALUE ДЛЯ FOCUSED BOLT


# Создаём три тестовых сценария надёжности способности.
# 0.90 означает, что 90% попыток завершаются успешно.
focused_bolt_ev = pd.DataFrame(
    {
        "Scenario": [
            "High Reliability",
            "Medium Reliability",
            "Low Reliability",
        ],
        "Success_Probability": [
            0.90,
            0.70,
            0.50,
        ],
    }
)

# Берём полный урон успешного Focused Bolt
# из уже рассчитанных данных, а не пишем 330 вручную.
focused_bolt_damage = focused_bolt["Focused_Bolt_Damage"].iloc[0]

focused_bolt_ev["Focused_Bolt_Damage"] = focused_bolt_damage

# Вероятность неудачи является дополнением
# вероятности успеха до 1.
focused_bolt_ev["Failure_Probability"] = (
    1
    - focused_bolt_ev["Success_Probability"]
)

# Ожидаемый урон одной попытки.
#
# Пока используем модель:
# успешный каст -> полный урон;
# неуспешный каст -> 0 урона способности.
focused_bolt_ev["Expected_Ability_Damage"] = (
    focused_bolt_ev["Success_Probability"]
    * focused_bolt_ev["Focused_Bolt_Damage"]
)

print("\nExpected Value Focused Bolt:")
print(
    focused_bolt_ev[
        [
            "Scenario",
            "Success_Probability",
            "Failure_Probability",
            "Focused_Bolt_Damage",
            "Expected_Ability_Damage",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# RISK-ADJUSTED EXPECTED VALUE FOCUSED BOLT


# Для первой модели фиксируем средний сценарий прерывания:
# Mid Interrupt = 1.0 секунда.
mid_interrupt = interrupt_scenarios.loc[
    interrupt_scenarios["Scenario"] == "Mid Interrupt"
].iloc[0]

# Получаем стоимость неудачного каста из уже рассчитанных данных.
# Не записываем 110 вручную.
mid_interrupt_lost_damage = mid_interrupt["Lost_Basic_Damage"]

focused_bolt_ev["Failure_Lost_Basic_Damage"] = (
    mid_interrupt_lost_damage
)

# Средняя ожидаемая стоимость неудачи.
focused_bolt_ev["Expected_Failure_Cost"] = (
    focused_bolt_ev["Failure_Probability"]
    * focused_bolt_ev["Failure_Lost_Basic_Damage"]
)

# Корректируем ожидаемую ценность способности
# на стоимость неудачных применений.
focused_bolt_ev["Risk_Adjusted_Value"] = (
    focused_bolt_ev["Expected_Ability_Damage"]
    - focused_bolt_ev["Expected_Failure_Cost"]
)

print("\nRisk-adjusted Expected Value Focused Bolt:")
print(
    focused_bolt_ev[
        [
            "Scenario",
            "Success_Probability",
            "Failure_Probability",
            "Expected_Ability_Damage",
            "Failure_Lost_Basic_Damage",
            "Expected_Failure_Cost",
            "Risk_Adjusted_Value",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# SENSITIVITY ANALYSIS: RELIABILITY x INTERRUPT TIMING


# Создаём все комбинации:
# каждый сценарий Reliability соединяем
# с каждым сценарием Interrupt Timing.
sensitivity = focused_bolt_ev[
    [
        "Scenario",
        "Success_Probability",
        "Failure_Probability",
        "Focused_Bolt_Damage",
        "Expected_Ability_Damage",
    ]
].merge(
    interrupt_scenarios[
        [
            "Scenario",
            "Interrupt_Time",
            "Lost_Basic_Damage",
        ]
    ],
    how="cross",
    suffixes=("_Reliability", "_Interrupt"),
)

# Ожидаемая цена неудачного применения.
sensitivity["Expected_Failure_Cost"] = (
    sensitivity["Failure_Probability"]
    * sensitivity["Lost_Basic_Damage"]
)

# Итоговая risk-adjusted ценность.
sensitivity["Risk_Adjusted_Value"] = (
    sensitivity["Expected_Ability_Damage"]
    - sensitivity["Expected_Failure_Cost"]
)

print("\nSensitivity Analysis Focused Bolt:")
print(
    sensitivity[
        [
            "Scenario_Reliability",
            "Scenario_Interrupt",
            "Success_Probability",
            "Interrupt_Time",
            "Expected_Ability_Damage",
            "Lost_Basic_Damage",
            "Expected_Failure_Cost",
            "Risk_Adjusted_Value",
        ]
    ]
    .round(2)
    .to_string(index=False)
)



# ------------------------------------------------------------
# 1. Выбираем только способность Arcane Shield
# ------------------------------------------------------------

# В ability_with_units находятся все способности всех юнитов.
# Поэтому сначала отфильтровываем только Arcane Shield.
#
# .copy() создаёт независимую копию выбранных строк.
# Это безопаснее для дальнейших изменений DataFrame.
arcane_shield = ability_with_units.loc[
    ability_with_units["Ability_Name"] == "Arcane Shield"
].copy()


print("\n" + "=" * 60)
print("ANALYSIS: ARCANE SHIELD")
print("=" * 60)


# ------------------------------------------------------------
# 2. Выводим исходные параметры Arcane Shield
# ------------------------------------------------------------

# Не все возможные параметры способностей обязательно существуют
# у Arcane Shield. Поэтому сначала создаём список желаемых столбцов,
# а затем оставляем только реально существующие.
arcane_shield_columns = [
    "Ability_ID",
    "Unit_ID",
    "Unit_Name",
    "Ability_Name",
    "Ability_Type",
    "Shield_Amount",
    "Duration",
    "Cooldown",
    "Max_Stacks",
    "Self_Cast",
]

arcane_shield_columns = [
    column
    for column in arcane_shield_columns
    if column in arcane_shield.columns
]


print("\nИсходные параметры Arcane Shield:")
print(
    arcane_shield[
        arcane_shield_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 3. Подготавливаем HP всех юнитов
# ------------------------------------------------------------

# ability_with_units уже содержит базовые характеристики юнитов,
# потому что выше в программе мы объединили таблицу способностей
# с таблицей Unit Balance.
#
# Нам нужны:
# Unit_ID   — уникальный ID юнита;
# Unit_Name — название;
# Faction   — фракция;
# Role      — игровая роль;
# HP        — базовое здоровье.
#
# В ability_with_units один и тот же юнит может встречаться
# несколько раз, потому что один юнит имеет способность,
# состоящую из нескольких параметров.
#
# Поэтому после выбора нужных столбцов используем
# drop_duplicates(subset="Unit_ID").
#
# В результате каждый юнит останется только один раз.

unit_hp = (
    ability_with_units[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "HP",
        ]
    ]
    .drop_duplicates(subset="Unit_ID")
    .copy()
)


# ------------------------------------------------------------
# 4. Проверяем, что HP является числом
# ------------------------------------------------------------

# pd.to_numeric() преобразует значения столбца HP
# в числовой формат.
#
# errors="raise" означает:
# если Python встретит значение, которое невозможно
# преобразовать в число, программа остановится
# и покажет ошибку.
#
# Для аналитического проекта это полезнее, чем молча
# пропускать неправильные данные.

unit_hp["HP"] = pd.to_numeric(
    unit_hp["HP"],
    errors="raise",
)


# ------------------------------------------------------------
# 5. Выводим HP всех юнитов
# ------------------------------------------------------------

# Сортируем таблицу по HP от большего значения к меньшему.
#
# ascending=False:
# False = сортировка по убыванию.
#
# Таким образом сверху окажутся самые живучие юниты,
# а снизу — самые хрупкие.

print("\nHP юнитов для анализа Arcane Shield:")
print(
    unit_hp
    .sort_values(
        "HP",
        ascending=False
    )
    .to_string(index=False)
)
print(
    unit_hp
    .sort_values(
        "HP",
        ascending=False
    )
    .to_string(index=False)
)
# ------------------------------------------------------------
# 6. Получаем величину щита Arcane Shield
# ------------------------------------------------------------

# В таблице arcane_shield находится одна строка способности
# Arcane Shield после преобразования исходного CSV
# из длинного формата в широкий.
#
# Нам нужен параметр Shield_Amount.
#
# iloc[0] означает:
# взять первую строку DataFrame.
#
# Таким образом мы получаем одно конкретное числовое значение
# щита, которое затем применим к каждому юниту.

shield_amount = pd.to_numeric(
    arcane_shield["Shield_Amount"],
    errors="raise"
).iloc[0]


print("\nВеличина Arcane Shield:")
print(f"Shield Amount = {shield_amount:.2f} HP")


# ------------------------------------------------------------
# 7. Создаём отдельную таблицу для анализа щита
# ------------------------------------------------------------

# Копируем таблицу unit_hp.
#
# Это важно: мы не хотим изменять исходную таблицу unit_hp,
# потому что она может понадобиться нам позже в первоначальном виде.

shield_analysis = unit_hp.copy()


# ------------------------------------------------------------
# 8. Добавляем величину щита каждому юниту
# ------------------------------------------------------------

# Arcane Shield имеет фиксированную величину.
#
# Поэтому каждому юниту записываем одинаковое значение
# Shield_Amount.
#
# Это НЕ означает, что щит одинаково эффективен для всех.
# Именно это мы сейчас и будем проверять.

shield_analysis["Shield_Amount"] = shield_amount


# ------------------------------------------------------------
# 9. Рассчитываем Effective HP
# ------------------------------------------------------------

# Effective HP в данном упрощённом анализе:
#
# Effective_HP = HP + Shield_Amount
#
# Например:
#
# HP = 700
# Shield = 350
#
# Effective_HP = 700 + 350 = 1050
#
# Здесь мы предполагаем, что щит полностью используется,
# то есть противник наносит достаточно урона,
# чтобы полностью снять Arcane Shield.

shield_analysis["Effective_HP"] = (
    shield_analysis["HP"]
    + shield_analysis["Shield_Amount"]
)


# ------------------------------------------------------------
# 10. Рассчитываем относительную ценность щита
# ------------------------------------------------------------

# Абсолютная величина щита для всех одинаковая:
#
# 350 HP.
#
# Но для юнитов с разным количеством здоровья
# эти 350 HP имеют разную относительную ценность.
#
# Формула:
#
# Shield_Relative_Percent =
#     Shield_Amount / HP * 100
#
# Например:
#
# HP = 700
# Shield = 350
#
# 350 / 700 * 100 = 50 %
#
# А для HP = 1600:
#
# 350 / 1600 * 100 = 21.875 %

shield_analysis["Shield_Relative_Percent"] = (
    shield_analysis["Shield_Amount"]
    / shield_analysis["HP"]
    * 100
)


# ------------------------------------------------------------
# 11. Сортируем юнитов по относительной ценности щита
# ------------------------------------------------------------

# Чем выше Shield_Relative_Percent,
# тем большую долю от собственного HP юнита
# добавляет Arcane Shield.
#
# ascending=False означает сортировку
# от самого большого процента к самому маленькому.

shield_analysis = shield_analysis.sort_values(
    "Shield_Relative_Percent",
    ascending=False
)


# ------------------------------------------------------------
# 12. Выводим итоговую таблицу
# ------------------------------------------------------------

print("\nОтносительная ценность Arcane Shield:")
print(
    shield_analysis[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "HP",
            "Shield_Amount",
            "Effective_HP",
            "Shield_Relative_Percent",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 13. Получаем длительность Arcane Shield
# ------------------------------------------------------------

# Shield_Amount показывает максимальное количество урона,
# которое способен поглотить щит.
#
# Но щит существует ограниченное время.
# Поэтому для оценки его реальной эффективности
# нам также нужна Duration.

shield_duration = pd.to_numeric(
    arcane_shield["Duration"],
    errors="raise"
).iloc[0]


print("\n" + "=" * 60)
print("SHIELD UTILIZATION ANALYSIS")
print("=" * 60)

print(f"\nShield Amount = {shield_amount:.2f} HP")
print(f"Shield Duration = {shield_duration:.2f} sec")


# ------------------------------------------------------------
# 14. Создаём сценарии входящего DPS
# ------------------------------------------------------------

# Пока у нас нет реальных результатов большого количества боёв,
# поэтому мы не пытаемся угадать единственное
# "правильное" значение входящего DPS.
#
# Вместо этого используем несколько тестовых сценариев.
#
# Это называется Scenario Analysis:
# мы смотрим, как одна и та же механика ведёт себя
# при разных условиях боя.

shield_pressure_scenarios = pd.DataFrame(
    {
        "Scenario": [
            "Low Pressure",
            "Medium Pressure",
            "High Pressure",
            "Extreme Pressure",
        ],
        "Incoming_DPS": [
            25.0,
            50.0,
            75.0,
            100.0,
        ],
    }
)


print("\nСценарии входящего урона:")
print(
    shield_pressure_scenarios
    .to_string(index=False)
)


# ------------------------------------------------------------
# 15. Рассчитываем потенциальный входящий урон
# ------------------------------------------------------------

# Формула:
#
# Incoming_Damage =
#     Incoming_DPS * Shield_Duration
#
# Например:
#
# Incoming_DPS = 50
# Duration = 6 sec
#
# Incoming_Damage = 50 * 6 = 300
#
# Это означает:
# если цель получает в среднем 50 урона в секунду,
# то за время существования щита в неё потенциально
# войдёт 300 единиц урона.

shield_pressure_scenarios["Shield_Duration"] = shield_duration

shield_pressure_scenarios["Incoming_Damage"] = (
    shield_pressure_scenarios["Incoming_DPS"]
    * shield_pressure_scenarios["Shield_Duration"]
)


# ------------------------------------------------------------
# 16. Добавляем максимальный размер щита
# ------------------------------------------------------------

shield_pressure_scenarios["Shield_Amount"] = shield_amount


# ------------------------------------------------------------
# 17. Рассчитываем реально поглощённый урон
# ------------------------------------------------------------

# Щит не может поглотить больше своего Shield_Amount.
#
# Поэтому:
#
# Absorbed_Damage =
#     min(Incoming_Damage, Shield_Amount)
#
# Пример 1:
#
# Incoming_Damage = 150
# Shield = 350
#
# Absorbed = 150
#
# Щит использован не полностью.
#
# Пример 2:
#
# Incoming_Damage = 600
# Shield = 350
#
# Absorbed = 350
#
# Больше 350 щит поглотить не способен.
#
# clip(upper=shield_amount) ограничивает максимальное
# значение столбца величиной нашего щита.

shield_pressure_scenarios["Absorbed_Damage"] = (
    shield_pressure_scenarios["Incoming_Damage"]
    .clip(upper=shield_amount)
)


# ------------------------------------------------------------
# 18. Рассчитываем неиспользованную часть щита
# ------------------------------------------------------------

# Если щит закончился раньше, чем противник успел
# нанести достаточно урона, часть Shield_Amount пропадает.
#
# Формула:
#
# Wasted_Shield =
#     Shield_Amount - Absorbed_Damage

shield_pressure_scenarios["Wasted_Shield"] = (
    shield_pressure_scenarios["Shield_Amount"]
    - shield_pressure_scenarios["Absorbed_Damage"]
)


# ------------------------------------------------------------
# 19. Рассчитываем Shield Utilization
# ------------------------------------------------------------

# Shield_Utilization_Percent показывает,
# какой процент потенциальной ёмкости щита
# действительно был использован.
#
# Формула:
#
# Shield_Utilization_Percent =
#     Absorbed_Damage / Shield_Amount * 100

shield_pressure_scenarios["Shield_Utilization_Percent"] = (
    shield_pressure_scenarios["Absorbed_Damage"]
    / shield_pressure_scenarios["Shield_Amount"]
    * 100
)


# ------------------------------------------------------------
# 20. Выводим результаты
# ------------------------------------------------------------

print("\nЭффективность использования Arcane Shield:")
print(
    shield_pressure_scenarios[
        [
            "Scenario",
            "Incoming_DPS",
            "Shield_Duration",
            "Incoming_Damage",
            "Shield_Amount",
            "Absorbed_Damage",
            "Wasted_Shield",
            "Shield_Utilization_Percent",
        ]
    ]
    .round(2)
    .to_string(index=False)
)
# ------------------------------------------------------------
# 21. Рассчитываем время, необходимое для полного разрушения щита
# ------------------------------------------------------------

# Формула:
#
# Time_To_Break_Shield =
#     Shield_Amount / Incoming_DPS
#
# Эта величина показывает, сколько секунд потребуется противнику,
# чтобы полностью снять Arcane Shield при постоянном входящем DPS.
#
# Важно:
#
# Time_To_Break_Shield НЕ всегда равно реальному времени жизни щита.
#
# Если:
#
# Time_To_Break_Shield > Shield_Duration
#
# противник не успевает разрушить щит до окончания Duration.
#
# Если:
#
# Time_To_Break_Shield <= Shield_Duration
#
# щит будет полностью разрушен раньше или ровно
# в момент окончания своей длительности.

shield_pressure_scenarios["Time_To_Break_Shield"] = (
    shield_pressure_scenarios["Shield_Amount"]
    / shield_pressure_scenarios["Incoming_DPS"]
)


# ------------------------------------------------------------
# 22. Рассчитываем фактическое время жизни щита
# ------------------------------------------------------------

# Реальное время существования щита ограничено двумя событиями:
#
# 1. противник полностью разрушил щит;
# 2. закончилась Duration способности.
#
# Поэтому:
#
# Effective_Shield_Lifetime =
#     min(Time_To_Break_Shield, Shield_Duration)
#
# Например:
#
# Time to Break = 14 sec
# Duration      = 6 sec
#
# Реальное время жизни:
#
# min(14, 6) = 6 sec
#
# Но:
#
# Time to Break = 3.5 sec
# Duration      = 6 sec
#
# Реальное время:
#
# min(3.5, 6) = 3.5 sec

shield_pressure_scenarios["Effective_Shield_Lifetime"] = (
    shield_pressure_scenarios[
        [
            "Time_To_Break_Shield",
            "Shield_Duration",
        ]
    ]
    .min(axis=1)
)


# ------------------------------------------------------------
# 23. Определяем, был ли щит полностью разрушен
# ------------------------------------------------------------

# Здесь создаём логический столбец:
#
# True  -> щит успели полностью разрушить;
# False -> щит закончился по Duration раньше,
#          чем противник снял все 350 HP.
#
# Это boolean-переменная — то есть значение True/False.

shield_pressure_scenarios["Shield_Fully_Broken"] = (
    shield_pressure_scenarios["Time_To_Break_Shield"]
    <= shield_pressure_scenarios["Shield_Duration"]
)


# ------------------------------------------------------------
# 24. Рассчитываем Breakpoint DPS
# ------------------------------------------------------------

# Breakpoint — это пороговое значение DPS,
# при котором противник снимает ровно весь щит
# ровно за его полную Duration.
#
# Формула:
#
# Breakpoint_DPS =
#     Shield_Amount / Shield_Duration
#
# Для нашего Arcane Shield:
#
# 350 / 6 = 58.333...
#
# Следовательно:
#
# Incoming DPS < 58.33
# -> щит не успевают полностью разрушить.
#
# Incoming DPS = 58.33
# -> щит снимается примерно ровно за 6 секунд.
#
# Incoming DPS > 58.33
# -> щит ломается раньше окончания Duration.

shield_breakpoint_dps = (
    shield_amount
    / shield_duration
)


print("\nBreakpoint Arcane Shield:")
print(
    f"Для полного разрушения {shield_amount:.2f} HP щита "
    f"за {shield_duration:.2f} sec требуется "
    f"{shield_breakpoint_dps:.2f} DPS."
)


# ------------------------------------------------------------
# 25. Выводим анализ времени жизни щита
# ------------------------------------------------------------

print("\nВремя жизни Arcane Shield:")
print(
    shield_pressure_scenarios[
        [
            "Scenario",
            "Incoming_DPS",
            "Time_To_Break_Shield",
            "Shield_Duration",
            "Effective_Shield_Lifetime",
            "Shield_Fully_Broken",
            "Shield_Utilization_Percent",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# Теперь переходим от искусственных сценариев входящего DPS
# к реальным значениям Damage наших юнитов.
#
# Цель:
# проверить, какую часть Arcane Shield снимает
# одна обычная атака каждого боевого юнита.
#
# Это уже более практический баланс-анализ:
#
# например:
# - слабая атака может снять только небольшую часть щита;
# - сильная атака может уничтожить большую его часть;
# - если Damage >= Shield_Amount,
#   одна атака полностью разрушит щит.


# ------------------------------------------------------------
# 26.1. Получаем величину Arcane Shield
# ------------------------------------------------------------

# arcane_shield мы уже создали раньше.
# Берём Shield_Amount из первой строки таблицы способности.
#
# float() превращает значение в обычное число Python.

shield_amount = float(
    arcane_shield["Shield_Amount"].iloc[0]
)

print("\n" + "=" * 60)
print("ARCANE SHIELD VS REAL UNIT ATTACKS")
print("=" * 60)

print(
    f"\nРазмер Arcane Shield: "
    f"{shield_amount:.2f} HP"
)


# ------------------------------------------------------------
# 26.2. Подготавливаем Damage всех юнитов
# ------------------------------------------------------------

# Нам сейчас нужны:
#
# Unit_ID
# Unit_Name
# Faction
# Role
# Damage
#
# Берём их напрямую из unit_balance.
#
# В отличие от ability_with_units,
# здесь каждый юнит представлен одной строкой,
# поэтому дополнительные drop_duplicates()
# нам не нужны.

shield_vs_attacks = unit_balance[
    [
        "Unit_ID",
        "Unit_Name",
        "Faction",
        "Role",
        "Damage",
    ]
].copy()


# ------------------------------------------------------------
# 26.3. Преобразуем Damage в число
# ------------------------------------------------------------

# Даже если CSV выглядит правильно,
# pandas иногда может считать числовой столбец текстом.
#
# Поэтому явно преобразуем Damage.
#
# errors="coerce":
# если встретится некорректное значение,
# оно станет NaN вместо аварийного завершения программы.

shield_vs_attacks["Damage"] = pd.to_numeric(
    shield_vs_attacks["Damage"],
    errors="coerce",
)


# ------------------------------------------------------------
# 26.4. Удаляем строки без Damage
# ------------------------------------------------------------

shield_vs_attacks = shield_vs_attacks.dropna(
    subset=["Damage"]
).copy()


# ------------------------------------------------------------
# 26.5. Сколько урона реально поглотит щит
# ------------------------------------------------------------

# Важно:
#
# щит не может поглотить больше собственного запаса HP.
#
# Например:
#
# Shield = 350
# Attack = 500
#
# щит поглотит только:
#
# 350 HP
#
# а оставшиеся:
#
# 500 - 350 = 150 HP
#
# пройдут дальше в здоровье юнита.
#
# Поэтому используем clip(upper=shield_amount).

shield_vs_attacks["Absorbed_Damage"] = (
    shield_vs_attacks["Damage"]
    .clip(upper=shield_amount)
)


# ------------------------------------------------------------
# 26.6. Считаем урон, который пробивает щит
# ------------------------------------------------------------

# Формула:
#
# Overflow_Damage =
# max(Damage - Shield_Amount, 0)
#
# Если атака слабее щита:
#
# Damage = 100
# Shield = 350
#
# Overflow = 0
#
# Если:
#
# Damage = 500
# Shield = 350
#
# Overflow = 150

shield_vs_attacks["Overflow_Damage"] = (
    shield_vs_attacks["Damage"]
    - shield_amount
).clip(lower=0)


# ------------------------------------------------------------
# 26.7. Остаток щита после одной атаки
# ------------------------------------------------------------

# Формула:
#
# Remaining_Shield =
# max(Shield_Amount - Damage, 0)

shield_vs_attacks["Remaining_Shield"] = (
    shield_amount
    - shield_vs_attacks["Damage"]
).clip(lower=0)


# ------------------------------------------------------------
# 26.8. Какая доля щита была использована
# ------------------------------------------------------------

# Формула:
#
# Shield_Used_Percent =
# Absorbed_Damage / Shield_Amount * 100

shield_vs_attacks["Shield_Used_Percent"] = (
    shield_vs_attacks["Absorbed_Damage"]
    / shield_amount
    * 100
)


# ------------------------------------------------------------
# 26.9. Может ли одна атака полностью разрушить щит
# ------------------------------------------------------------

# Получаем True / False.
#
# True:
# Damage >= Shield
#
# False:
# Damage < Shield

shield_vs_attacks["Breaks_Shield_One_Hit"] = (
    shield_vs_attacks["Damage"]
    >= shield_amount
)


# ------------------------------------------------------------
# 26.10. Сколько таких атак теоретически нужно для щита
# ------------------------------------------------------------

# Здесь нам понадобится ceil().
#
# ceil означает округление ВВЕРХ.
#
# Например:
#
# Shield = 350
# Damage = 100
#
# 350 / 100 = 3.5
#
# Но половины четвёртой атаки в нашем простом
# дискретном анализе недостаточно:
#
# 3 атаки = 300
# щит ещё жив.
#
# 4 атаки = 400
# щит уничтожен.
#
# Поэтому:
#
# ceil(3.5) = 4

shield_vs_attacks["Hits_To_Break_Shield"] = (
    shield_amount
    / shield_vs_attacks["Damage"]
).apply(lambda x: int(-(-x // 1)))


# ------------------------------------------------------------
# 26.11. Сортируем по силе одиночной атаки
# ------------------------------------------------------------

# Сильнейшие атаки выводим сверху.

shield_vs_attacks = shield_vs_attacks.sort_values(
    "Damage",
    ascending=False,
)


# ------------------------------------------------------------
# 26.12. Выводим результат
# ------------------------------------------------------------

print("\nArcane Shield против обычных атак юнитов:")

print(
    shield_vs_attacks[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "Damage",
            "Absorbed_Damage",
            "Overflow_Damage",
            "Remaining_Shield",
            "Shield_Used_Percent",
            "Breaks_Shield_One_Hit",
            "Hits_To_Break_Shield",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


print("\n" + "=" * 60)
print("ARCANE SHIELD VS REAL UNIT DPS")
print("=" * 60)


# ------------------------------------------------------------
# 27.1. Получаем основные параметры Arcane Shield
# ------------------------------------------------------------

shield_amount = float(
    arcane_shield["Shield_Amount"].dropna().iloc[0]
)

shield_duration = float(
    arcane_shield["Duration"].dropna().iloc[0]
)

print(f"\nРазмер Arcane Shield: {shield_amount:.2f} HP")
print(f"Длительность Arcane Shield: {shield_duration:.2f} sec")


# ------------------------------------------------------------
# 27.2. Создаём таблицу DPS всех юнитов
# ------------------------------------------------------------

shield_vs_dps = (
    unit_balance[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "DPS",
        ]
    ]
    .copy()
)


# ------------------------------------------------------------
# 27.3. Преобразуем DPS в числовой формат
# ------------------------------------------------------------

shield_vs_dps["DPS"] = pd.to_numeric(
    shield_vs_dps["DPS"],
    errors="coerce",
)


# Удаляем строки, где DPS отсутствует.
shield_vs_dps = shield_vs_dps.dropna(
    subset=["DPS"]
)


# ------------------------------------------------------------
# 27.4. Рассчитываем время разрушения щита
# ------------------------------------------------------------

# Формула:
#
# Time_To_Break_Shield =
#     Shield_Amount / DPS
#
# Например:
#
# Shield = 350 HP
# DPS = 70
#
# 350 / 70 = 5 sec

shield_vs_dps["Time_To_Break_Shield"] = (
    shield_amount
    / shield_vs_dps["DPS"]
)


# ------------------------------------------------------------
# 27.5. Проверяем, успеет ли юнит уничтожить щит
# до окончания его длительности
# ------------------------------------------------------------

shield_vs_dps["Breaks_Shield_Before_Expire"] = (
    shield_vs_dps["Time_To_Break_Shield"]
    <= shield_duration
)


# ------------------------------------------------------------
# 27.6. Рассчитываем урон, который юнит теоретически
# может нанести за полные 6 секунд существования щита
# ------------------------------------------------------------

# Формула:
#
# Potential_Damage_During_Shield =
#     DPS * Shield_Duration

shield_vs_dps["Potential_Damage_During_Shield"] = (
    shield_vs_dps["DPS"]
    * shield_duration
)


# ------------------------------------------------------------
# 27.7. Рассчитываем фактически поглощённый щитом урон
# ------------------------------------------------------------

# Щит не может поглотить больше собственного размера.
#
# Поэтому:
#
# Absorbed_Damage =
# min(
#     Potential_Damage_During_Shield,
#     Shield_Amount
# )

shield_vs_dps["Absorbed_Damage"] = (
    shield_vs_dps["Potential_Damage_During_Shield"]
    .clip(upper=shield_amount)
)


# ------------------------------------------------------------
# 27.8. Рассчитываем неиспользованную часть щита
# ------------------------------------------------------------

shield_vs_dps["Unused_Shield"] = (
    shield_amount
    - shield_vs_dps["Absorbed_Damage"]
)


# ------------------------------------------------------------
# 27.9. Рассчитываем процент использования щита
# ------------------------------------------------------------

shield_vs_dps["Shield_Utilization_Percent"] = (
    shield_vs_dps["Absorbed_Damage"]
    / shield_amount
    * 100
)


# ------------------------------------------------------------
# 27.10. Рассчитываем фактическое время жизни щита
# ------------------------------------------------------------

# Если противник способен уничтожить щит быстрее 6 секунд,
# фактическое время жизни равно Time_To_Break_Shield.
#
# Если не способен, щит существует все 6 секунд.

shield_vs_dps["Effective_Shield_Lifetime"] = (
    shield_vs_dps["Time_To_Break_Shield"]
    .clip(upper=shield_duration)
)


# ------------------------------------------------------------
# 27.11. Сортируем от самого опасного DPS к наименее опасному
# ------------------------------------------------------------

shield_vs_dps = shield_vs_dps.sort_values(
    "DPS",
    ascending=False,
)


# ------------------------------------------------------------
# 27.12. Выводим результат
# ------------------------------------------------------------

print("\nArcane Shield против DPS юнитов:")

print(
    shield_vs_dps[
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "DPS",
            "Time_To_Break_Shield",
            "Breaks_Shield_Before_Expire",
            "Potential_Damage_During_Shield",
            "Absorbed_Damage",
            "Unused_Shield",
            "Shield_Utilization_Percent",
            "Effective_Shield_Lifetime",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


print("\n" + "=" * 60)
print("ARCANE SHIELD VS BURST ABILITIES")
print("=" * 60)


# ------------------------------------------------------------
# 28.1. Получаем базовый Damage владельцев способностей
# ------------------------------------------------------------

# Нам понадобятся три способности:
#
# Focused Bolt  -> ELF_03
# Knife Barrage -> HOR_03
# Bone Smash    -> HOR_04
#
# В unit_balance уже находятся базовые характеристики
# каждого юнита, включая Damage.

burst_units = (
    unit_balance[
        unit_balance["Unit_ID"].isin(
            [
                "ELF_03",
                "HOR_03",
                "HOR_04",
            ]
        )
    ][
        [
            "Unit_ID",
            "Unit_Name",
            "Faction",
            "Role",
            "Damage",
        ]
    ]
    .copy()
)


# Преобразуем Damage в числовой формат.
burst_units["Damage"] = pd.to_numeric(
    burst_units["Damage"],
    errors="coerce",
)


print("\nБазовый Damage владельцев burst-способностей:")
print(
    burst_units
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 28.2. Получаем параметры Focused Bolt
# ------------------------------------------------------------

focused_bolt_data = ability_with_units[
    ability_with_units["Ability_Name"] == "Focused Bolt"
].copy()


focused_bolt_multiplier = float(
    focused_bolt_data["Damage_Multiplier"]
    .dropna()
    .iloc[0]
)


# Находим базовый Damage Elven Mage.
elven_mage_damage = float(
    burst_units.loc[
        burst_units["Unit_ID"] == "ELF_03",
        "Damage",
    ].iloc[0]
)


# Полный урон Focused Bolt:
#
# Ability Damage =
# Base Damage * Damage Multiplier

focused_bolt_damage = (
    elven_mage_damage
    * focused_bolt_multiplier
)


# ------------------------------------------------------------
# 28.3. Получаем параметры Knife Barrage
# ------------------------------------------------------------

knife_barrage_data = ability_with_units[
    ability_with_units["Ability_Name"] == "Knife Barrage"
].copy()


knife_count = float(
    knife_barrage_data["Knife_Count"]
    .dropna()
    .iloc[0]
)


damage_per_knife = float(
    knife_barrage_data["Damage_Per_Knife"]
    .dropna()
    .iloc[0]
)


# Базовый Damage Orc Thrower.
orc_thrower_damage = float(
    burst_units.loc[
        burst_units["Unit_ID"] == "HOR_03",
        "Damage",
    ].iloc[0]
)


# Урон одного ножа.
knife_damage = (
    orc_thrower_damage
    * damage_per_knife
)


# Полный теоретический урон Knife Barrage.
#
# Total Damage =
# Base Damage
# * Damage Per Knife
# * Knife Count

knife_barrage_damage = (
    knife_damage
    * knife_count
)


# ------------------------------------------------------------
# 28.4. Получаем параметры Bone Smash
# ------------------------------------------------------------

bone_smash_data = ability_with_units[
    ability_with_units["Ability_Name"] == "Bone Smash"
].copy()


bone_smash_multiplier = float(
    bone_smash_data["Damage_Multiplier"]
    .dropna()
    .iloc[0]
)


# Базовый Damage Boneclub Troll.
boneclub_troll_damage = float(
    burst_units.loc[
        burst_units["Unit_ID"] == "HOR_04",
        "Damage",
    ].iloc[0]
)


bone_smash_damage = (
    boneclub_troll_damage
    * bone_smash_multiplier
)


# ------------------------------------------------------------
# 28.5. Создаём общую таблицу burst-способностей
# ------------------------------------------------------------

burst_vs_shield = pd.DataFrame(
    [
        {
            "Unit_ID": "ELF_03",
            "Unit_Name": "Elven Mage",
            "Ability_Name": "Focused Bolt",
            "Ability_Damage": focused_bolt_damage,
        },
        {
            "Unit_ID": "HOR_03",
            "Unit_Name": "Orc Thrower",
            "Ability_Name": "Knife Barrage",
            "Ability_Damage": knife_barrage_damage,
        },
        {
            "Unit_ID": "HOR_04",
            "Unit_Name": "Boneclub Troll",
            "Ability_Name": "Bone Smash",
            "Ability_Damage": bone_smash_damage,
        },
    ]
)


# ------------------------------------------------------------
# 28.6. Рассчитываем, сколько урона поглощает щит
# ------------------------------------------------------------

burst_vs_shield["Absorbed_By_Shield"] = (
    burst_vs_shield["Ability_Damage"]
    .clip(upper=shield_amount)
)


# ------------------------------------------------------------
# 28.7. Рассчитываем урон, прошедший через щит
# ------------------------------------------------------------

# Overflow Damage =
# Ability Damage - Absorbed Damage

burst_vs_shield["Overflow_Damage"] = (
    burst_vs_shield["Ability_Damage"]
    - burst_vs_shield["Absorbed_By_Shield"]
)


# ------------------------------------------------------------
# 28.8. Сколько щита останется после способности
# ------------------------------------------------------------

burst_vs_shield["Remaining_Shield"] = (
    shield_amount
    - burst_vs_shield["Absorbed_By_Shield"]
)


# ------------------------------------------------------------
# 28.9. Проверяем, полностью ли способность разрушает щит
# ------------------------------------------------------------

burst_vs_shield["Breaks_Shield"] = (
    burst_vs_shield["Ability_Damage"]
    >= shield_amount
)


# ------------------------------------------------------------
# 28.10. Считаем процент щита, который использовала атака
# ------------------------------------------------------------

burst_vs_shield["Shield_Used_Percent"] = (
    burst_vs_shield["Absorbed_By_Shield"]
    / shield_amount
    * 100
)


# ------------------------------------------------------------
# 28.11. Сортируем от самой сильной burst-способности
# ------------------------------------------------------------

burst_vs_shield = burst_vs_shield.sort_values(
    "Ability_Damage",
    ascending=False,
)


# ------------------------------------------------------------
# 28.12. Выводим результат
# ------------------------------------------------------------

print(f"\nРазмер Arcane Shield: {shield_amount:.2f} HP")

print("\nBurst-способности против Arcane Shield:")

print(
    burst_vs_shield[
        [
            "Unit_ID",
            "Unit_Name",
            "Ability_Name",
            "Ability_Damage",
            "Absorbed_By_Shield",
            "Overflow_Damage",
            "Remaining_Shield",
            "Breaks_Shield",
            "Shield_Used_Percent",
        ]
    ]
    .round(2)
    .to_string(index=False)
)

print("\n" + "=" * 60)
print("KNIFE BARRAGE HIT-BY-HIT VS ARCANE SHIELD")
print("=" * 60)


# ------------------------------------------------------------
# 29.1. Получаем интервал между ножами
# ------------------------------------------------------------

knife_interval = float(
    knife_barrage_data["Knife_Interval"]
    .dropna()
    .iloc[0]
)


print(f"\nКоличество ножей: {int(knife_count)}")
print(f"Урон одного ножа: {knife_damage:.2f}")
print(f"Интервал между ножами: {knife_interval:.2f} sec")
print(f"Начальный Arcane Shield: {shield_amount:.2f} HP")


# ------------------------------------------------------------
# 29.2. Подготавливаем переменные симуляции
# ------------------------------------------------------------

# В начале способность ещё не нанесла ни одного удара,
# поэтому щит имеет полный запас прочности.

current_shield = shield_amount


# Здесь будем сохранять результат каждого отдельного ножа.
knife_hit_results = []


# ------------------------------------------------------------
# 29.3. Симулируем каждый нож отдельно
# ------------------------------------------------------------

for knife_number in range(1, int(knife_count) + 1):

    # --------------------------------------------------------
    # Определяем время попадания ножа
    # --------------------------------------------------------
    #
    # Первый нож считаем попавшим в момент t = 0.
    #
    # Поэтому:
    #
    # Knife 1 -> 0.0 sec
    # Knife 2 -> 0.2 sec
    # Knife 3 -> 0.4 sec
    # Knife 4 -> 0.6 sec
    # Knife 5 -> 0.8 sec

    hit_time = (
        (knife_number - 1)
        * knife_interval
    )


    # Запоминаем состояние щита ДО попадания.
    shield_before = current_shield


    # --------------------------------------------------------
    # Сколько урона может поглотить щит?
    # --------------------------------------------------------
    #
    # Если щита осталось больше, чем урон ножа,
    # поглощается весь урон.
    #
    # Если щита осталось меньше,
    # поглощается только оставшийся запас щита.

    absorbed_damage = min(
        knife_damage,
        current_shield,
    )


    # --------------------------------------------------------
    # Считаем урон, который прошёл через щит
    # --------------------------------------------------------

    overflow_damage = max(
        knife_damage - absorbed_damage,
        0,
    )


    # --------------------------------------------------------
    # Уменьшаем прочность щита
    # --------------------------------------------------------

    current_shield = max(
        current_shield - absorbed_damage,
        0,
    )


    # --------------------------------------------------------
    # Проверяем, был ли щит уничтожен именно этим ножом
    # --------------------------------------------------------

    shield_broken = (
        shield_before > 0
        and current_shield <= 0
    )


    # --------------------------------------------------------
    # Сохраняем результат этого попадания
    # --------------------------------------------------------

    knife_hit_results.append(
        {
            "Knife_Number": knife_number,
            "Hit_Time": hit_time,
            "Knife_Damage": knife_damage,
            "Shield_Before": shield_before,
            "Absorbed_Damage": absorbed_damage,
            "Overflow_Damage": overflow_damage,
            "Shield_After": current_shield,
            "Shield_Broken": shield_broken,
        }
    )


# ------------------------------------------------------------
# 29.4. Превращаем результаты симуляции в DataFrame
# ------------------------------------------------------------

knife_hit_analysis = pd.DataFrame(
    knife_hit_results
)


# ------------------------------------------------------------
# 29.5. Добавляем накопительный урон
# ------------------------------------------------------------
#
# cumsum() = cumulative sum
#          = накопительная сумма.
#
# Например:
#
# 59.4
# 118.8
# 178.2
# 237.6
# 297.0

knife_hit_analysis["Cumulative_Damage"] = (
    knife_hit_analysis["Knife_Damage"]
    .cumsum()
)


# ------------------------------------------------------------
# 29.6. Добавляем накопительный урон,
# прошедший через щит
# ------------------------------------------------------------

knife_hit_analysis["Cumulative_Overflow"] = (
    knife_hit_analysis["Overflow_Damage"]
    .cumsum()
)


# ------------------------------------------------------------
# 29.7. Выводим пошаговую таблицу
# ------------------------------------------------------------

print("\nПошаговое попадание Knife Barrage:")

print(
    knife_hit_analysis[
        [
            "Knife_Number",
            "Hit_Time",
            "Knife_Damage",
            "Cumulative_Damage",
            "Shield_Before",
            "Absorbed_Damage",
            "Overflow_Damage",
            "Cumulative_Overflow",
            "Shield_After",
            "Shield_Broken",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 29.8. Итог симуляции
# ------------------------------------------------------------

total_barrage_damage = (
    knife_hit_analysis["Knife_Damage"].sum()
)

total_absorbed_damage = (
    knife_hit_analysis["Absorbed_Damage"].sum()
)

total_overflow_damage = (
    knife_hit_analysis["Overflow_Damage"].sum()
)


print("\nИтог Knife Barrage против Arcane Shield:")

print(
    f"Общий урон Knife Barrage: "
    f"{total_barrage_damage:.2f}"
)

print(
    f"Поглощено Arcane Shield: "
    f"{total_absorbed_damage:.2f}"
)

print(
    f"Урон, прошедший через щит: "
    f"{total_overflow_damage:.2f}"
)

print(
    f"Остаток Arcane Shield: "
    f"{current_shield:.2f}"
)


print("\n" + "=" * 60)
print("KNIFE BARRAGE VS DAMAGED ARCANE SHIELD")
print("=" * 60)


# ------------------------------------------------------------
# 30.1. Создаём разные состояния Arcane Shield
# ------------------------------------------------------------
#
# До этого мы всегда предполагали, что Knife Barrage попадает
# в абсолютно новый щит с полными 350 HP.
#
# Теперь проверим более реалистичные ситуации:
# щит мог получить урон ещё ДО начала Knife Barrage.

starting_shield_values = [
    350,
    250,
    200,
    150,
    100,
    50,
]


# ------------------------------------------------------------
# 30.2. Создаём список для результатов сценариев
# ------------------------------------------------------------

damaged_shield_results = []


# ------------------------------------------------------------
# 30.3. Запускаем отдельную симуляцию
# для каждого стартового значения щита
# ------------------------------------------------------------

for starting_shield in starting_shield_values:

    # В начале каждого нового сценария
    # устанавливаем новое стартовое значение щита.
    scenario_shield = float(starting_shield)

    # Сюда будем записывать общий урон,
    # который прошёл непосредственно в HP цели.
    scenario_overflow = 0.0

    # Сколько урона суммарно поглотил щит.
    scenario_absorbed = 0.0

    # Пока щит не разрушен,
    # номер ножа-разрушителя неизвестен.
    breaking_knife = None

    # Время разрушения щита также пока неизвестно.
    break_time = None


    # --------------------------------------------------------
    # 30.4. Симулируем все ножи Knife Barrage
    # --------------------------------------------------------

    for knife_number in range(1, int(knife_count) + 1):

        hit_time = (
            (knife_number - 1)
            * knife_interval
        )

        shield_before_hit = scenario_shield


        # ----------------------------------------------------
        # Определяем, сколько урона способен поглотить щит
        # ----------------------------------------------------

        absorbed = min(
            knife_damage,
            scenario_shield,
        )


        # ----------------------------------------------------
        # Остаток удара проходит в HP цели
        # ----------------------------------------------------

        overflow = max(
            knife_damage - absorbed,
            0,
        )


        # ----------------------------------------------------
        # Обновляем состояние щита
        # ----------------------------------------------------

        scenario_shield = max(
            scenario_shield - absorbed,
            0,
        )


        # Накапливаем результаты.
        scenario_absorbed += absorbed
        scenario_overflow += overflow


        # ----------------------------------------------------
        # Проверяем момент разрушения щита
        # ----------------------------------------------------
        #
        # Нам нужен именно ПЕРВЫЙ нож,
        # который переводит щит из состояния:
        #
        # Shield > 0
        #
        # в:
        #
        # Shield = 0

        if (
            breaking_knife is None
            and shield_before_hit > 0
            and scenario_shield <= 0
        ):
            breaking_knife = knife_number
            break_time = hit_time


    # --------------------------------------------------------
    # 30.5. Определяем, был ли щит разрушен
    # --------------------------------------------------------

    shield_broken = breaking_knife is not None


    # --------------------------------------------------------
    # 30.6. Сколько процентов Barrage прошло в HP
    # --------------------------------------------------------

    overflow_percent = (
        scenario_overflow
        / total_barrage_damage
        * 100
    )


    # --------------------------------------------------------
    # 30.7. Сохраняем результат сценария
    # --------------------------------------------------------

    damaged_shield_results.append(
        {
            "Starting_Shield": starting_shield,
            "Total_Barrage_Damage": total_barrage_damage,
            "Absorbed_Damage": scenario_absorbed,
            "Overflow_Damage": scenario_overflow,
            "Overflow_Percent": overflow_percent,
            "Remaining_Shield": scenario_shield,
            "Shield_Broken": shield_broken,
            "Breaking_Knife": breaking_knife,
            "Break_Time": break_time,
        }
    )


# ------------------------------------------------------------
# 30.8. Создаём DataFrame
# ------------------------------------------------------------

damaged_shield_analysis = pd.DataFrame(
    damaged_shield_results
)


# ------------------------------------------------------------
# 30.9. Выводим таблицу
# ------------------------------------------------------------

print("\nKnife Barrage против разных состояний Arcane Shield:")

print(
    damaged_shield_analysis[
        [
            "Starting_Shield",
            "Total_Barrage_Damage",
            "Absorbed_Damage",
            "Overflow_Damage",
            "Overflow_Percent",
            "Remaining_Shield",
            "Shield_Broken",
            "Breaking_Knife",
            "Break_Time",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 30.10. Находим минимальный протестированный щит,
# который переживает полный Knife Barrage
# ------------------------------------------------------------

surviving_shields = damaged_shield_analysis[
    damaged_shield_analysis["Shield_Broken"] == False
]


if not surviving_shields.empty:

    minimum_surviving_shield = (
        surviving_shields["Starting_Shield"].min()
    )

    print(
        "\nМинимальное из протестированных значений щита, "
        "которое пережило весь Knife Barrage: "
        f"{minimum_surviving_shield:.2f} HP"
    )

else:

    print(
        "\nВсе протестированные значения щита "
        "были разрушены Knife Barrage."
    )


# ------------------------------------------------------------
# 30.11. Теоретический breakpoint
# ------------------------------------------------------------
#
# Полный Knife Barrage наносит:
#
# knife_damage * knife_count
#
# Чтобы поглотить ВЕСЬ Barrage без overflow,
# щит должен иметь как минимум столько же HP.

barrage_shield_breakpoint = total_barrage_damage


print(
    "\nТеоретический размер щита для полного "
    "поглощения Knife Barrage: "
    f"{barrage_shield_breakpoint:.2f} HP"
)

#
# На предыдущих этапах мы анализировали источники урона
# в основном по отдельности.
#
# Теперь построим маленькую последовательность боевых событий.
#
# Цель:
# проверить, как Arcane Shield расходуется,
# если по защищённой цели последовательно наносят урон
# несколько источников.
#
# Это первый небольшой шаг от статического анализа
# к event-based combat simulation.
#
# Event-based simulation = симуляция, в которой бой
# рассматривается как последовательность событий во времени.


print("\n" + "=" * 60)
print("COMBINED DAMAGE VS ARCANE SHIELD")
print("=" * 60)


# ------------------------------------------------------------
# 31.1. Получаем урон обычной атаки Blade Goblin
# ------------------------------------------------------------
#
# unit_balance уже был загружен ранее.
#
# Нам нужна строка HOR_01 — Blade Goblin.
# Затем из неё берём Damage.

goblin_row = unit_balance[
    unit_balance["Unit_ID"] == "HOR_01"
].iloc[0]

goblin_attack_damage = float(
    str(goblin_row["Damage"]).replace(",", ".")
)


print(
    "\nУрон обычной атаки Blade Goblin: "
    f"{goblin_attack_damage:.2f}"
)


# ------------------------------------------------------------
# 31.2. Напоминаем параметры Knife Barrage
# ------------------------------------------------------------
#
# knife_damage, knife_count и knife_interval
# мы уже рассчитали на предыдущем этапе.
#
# Поэтому повторно вручную числа не записываем.
#
# Это важно:
# если позже параметры Knife Barrage изменятся в CSV,
# анализ автоматически использует новые значения.

print(
    "Урон одного ножа Knife Barrage: "
    f"{knife_damage:.2f}"
)

print(
    "Количество ножей: "
    f"{int(knife_count)}"
)

print(
    "Интервал между ножами: "
    f"{knife_interval:.2f} sec"
)


# ------------------------------------------------------------
# 31.3. Создаём список боевых событий
# ------------------------------------------------------------
#
# Каждое событие — словарь.
#
# В нём пока три главные вещи:
#
# Time   — время события;
# Source — кто наносит урон;
# Attack — какой атакой;
# Damage — входящий урон.
#
# Позже такую структуру можно значительно расширить:
#
# Target
# Ability_ID
# Damage_Type
# Status_Effect
# Crit
# и т.д.


combat_events = []


# ------------------------------------------------------------
# 31.4. Первый обычный удар Blade Goblin
# ------------------------------------------------------------

combat_events.append(
    {
        "Time": 0.0,
        "Source": "Blade Goblin",
        "Attack": "Basic Attack",
        "Damage": goblin_attack_damage,
    }
)


# ------------------------------------------------------------
# 31.5. Добавляем Knife Barrage
# ------------------------------------------------------------
#
# Barrage начинается на 0.5 секунды.
#
# Первый нож:
#
# 0.5 sec
#
# Второй:
#
# 0.5 + 0.2 = 0.7
#
# Затем:
#
# 0.9
# 1.1
# 1.3

barrage_start_time = 0.5


for knife_number in range(
    1,
    int(knife_count) + 1,
):

    knife_time = (
        barrage_start_time
        + (knife_number - 1) * knife_interval
    )

    combat_events.append(
        {
            "Time": knife_time,
            "Source": "Orc Thrower",
            "Attack": f"Knife Barrage #{knife_number}",
            "Damage": knife_damage,
        }
    )


# ------------------------------------------------------------
# 31.6. Второй обычный удар Blade Goblin
# ------------------------------------------------------------

combat_events.append(
    {
        "Time": 1.5,
        "Source": "Blade Goblin",
        "Attack": "Basic Attack",
        "Damage": goblin_attack_damage,
    }
)


# ------------------------------------------------------------
# 31.7. Сортируем события по времени
# ------------------------------------------------------------
#
# Сейчас мы сами добавили их почти по порядку.
#
# Но для будущей симуляции нельзя на это рассчитывать.
#
# Поэтому сортировка по Time — полезное правило.

combat_events = sorted(
    combat_events,
    key=lambda event: event["Time"],
)


# ------------------------------------------------------------
# 31.8. Подготавливаем Arcane Shield
# ------------------------------------------------------------

combined_current_shield = float(
    shield_amount
)


# Суммарный входящий урон.

combined_total_damage = 0.0


# Сколько всего поглотил щит.

combined_absorbed_damage = 0.0


# Сколько прошло непосредственно в HP.

combined_overflow_damage = 0.0


# Здесь сохраним подробный combat log.

combined_combat_log = []


# Щит пока не разрушен.

shield_break_time = None
shield_break_event = None


# ------------------------------------------------------------
# 31.9. Обрабатываем события одно за другим
# ------------------------------------------------------------

for event in combat_events:

    event_time = float(
        event["Time"]
    )

    incoming_damage = float(
        event["Damage"]
    )

    shield_before = (
        combined_current_shield
    )


    # --------------------------------------------------------
    # Сколько урона способен принять щит?
    # --------------------------------------------------------
    #
    # Например:
    #
    # Shield = 40
    # Damage = 90
    #
    # щит может поглотить только 40.

    absorbed_damage = min(
        incoming_damage,
        combined_current_shield,
    )


    # --------------------------------------------------------
    # Остаток проходит в HP цели
    # --------------------------------------------------------

    overflow_damage = max(
        incoming_damage - absorbed_damage,
        0,
    )


    # --------------------------------------------------------
    # Уменьшаем Arcane Shield
    # --------------------------------------------------------

    combined_current_shield = max(
        combined_current_shield
        - absorbed_damage,
        0,
    )


    # --------------------------------------------------------
    # Обновляем общие счётчики
    # --------------------------------------------------------

    combined_total_damage += (
        incoming_damage
    )

    combined_absorbed_damage += (
        absorbed_damage
    )

    combined_overflow_damage += (
        overflow_damage
    )


    # --------------------------------------------------------
    # Проверяем:
    # разрушился ли щит ИМЕННО на этом событии?
    # --------------------------------------------------------

    shield_broken_on_event = (
        shield_before > 0
        and combined_current_shield <= 0
    )


    # Первый момент разрушения сохраняем отдельно.

    if (
        shield_broken_on_event
        and shield_break_time is None
    ):

        shield_break_time = event_time
        shield_break_event = (
            f"{event['Source']} — "
            f"{event['Attack']}"
        )


    # --------------------------------------------------------
    # Добавляем строку в combat log
    # --------------------------------------------------------

    combined_combat_log.append(
        {
            "Time": event_time,
            "Source": event["Source"],
            "Attack": event["Attack"],
            "Incoming_Damage": incoming_damage,
            "Shield_Before": shield_before,
            "Absorbed_By_Shield": absorbed_damage,
            "Overflow_Damage": overflow_damage,
            "Shield_After": combined_current_shield,
            "Shield_Broken_On_Event":
                shield_broken_on_event,
        }
    )


# ------------------------------------------------------------
# 31.10. Превращаем combat log в DataFrame
# ------------------------------------------------------------

combined_combat_df = pd.DataFrame(
    combined_combat_log
)


# ------------------------------------------------------------
# 31.11. Выводим combat log
# ------------------------------------------------------------

print("\nПоследовательность боевых событий:")

print(
    combined_combat_df[
        [
            "Time",
            "Source",
            "Attack",
            "Incoming_Damage",
            "Shield_Before",
            "Absorbed_By_Shield",
            "Overflow_Damage",
            "Shield_After",
            "Shield_Broken_On_Event",
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 31.12. Итоговые показатели
# ------------------------------------------------------------

print("\nИтог комбинированной атаки:")

print(
    f"Начальный Arcane Shield: "
    f"{shield_amount:.2f} HP"
)

print(
    f"Общий входящий урон: "
    f"{combined_total_damage:.2f}"
)

print(
    f"Поглощено щитом: "
    f"{combined_absorbed_damage:.2f}"
)

print(
    f"Прошло в HP цели: "
    f"{combined_overflow_damage:.2f}"
)

print(
    f"Остаток Arcane Shield: "
    f"{combined_current_shield:.2f}"
)


# ------------------------------------------------------------
# 31.13. Выводим момент разрушения щита
# ------------------------------------------------------------

if shield_break_time is not None:

    print(
        f"Arcane Shield разрушен на "
        f"{shield_break_time:.2f} sec."
    )

    print(
        "Событие, разрушившее щит: "
        f"{shield_break_event}"
    )

else:

    print(
        "Arcane Shield пережил всю "
        "последовательность атак."
    )


# ------------------------------------------------------------
# 31.14. Проверяем сохранение урона
# ------------------------------------------------------------
#
# Это очень полезная sanity check.
#
# Должно выполняться:
#
# Total Damage
# =
# Absorbed Damage
# +
# Overflow Damage
#
# Если равенство нарушилось,
# значит где-то в симуляции мы потеряли
# или случайно создали урон.

damage_conservation_check = math.isclose(
    combined_total_damage,
    combined_absorbed_damage
    + combined_overflow_damage,
    rel_tol=1e-9,
    abs_tol=1e-9,
)


print(
    "\nПроверка сохранения урона "
    "(Total = Absorbed + Overflow): "
    f"{damage_conservation_check}"
)
print("\n" + "=" * 60)
print("ШАГ 4.8 ЗАВЕРШЁН")
print("=" * 60)
