import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 60)
print("ERA OF STRIFE — AUTOMATED BALANCE TESTS")
print("=" * 60)


# ------------------------------------------------------------
# 1. Загружаем данные, необходимые для тестирования
# ------------------------------------------------------------

balance_tests = pd.read_csv("data/balance_tests.csv")
balance_risks = pd.read_csv("data/balance_risks.csv")
combat_scenarios = pd.read_csv("data/combat_scenarios.csv")


# ------------------------------------------------------------
# 2. Проверяем, что таблицы действительно загрузились
# ------------------------------------------------------------

print("\nBalance Tests:")
print(f"Количество строк: {len(balance_tests)}")
print("Столбцы:")
print(balance_tests.columns.tolist())


print("\nBalance Risks:")
print(f"Количество строк: {len(balance_risks)}")
print("Столбцы:")
print(balance_risks.columns.tolist())


print("\nCombat Scenarios:")
print(f"Количество строк: {len(combat_scenarios)}")
print("Столбцы:")
print(combat_scenarios.columns.tolist())


# ------------------------------------------------------------
# 3. Показываем первые строки каждой таблицы
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ПЕРВЫЕ СТРОКИ BALANCE TESTS")
print("=" * 60)

print(balance_tests.head())


print("\n" + "=" * 60)
print("ПЕРВЫЕ СТРОКИ BALANCE RISKS")
print("=" * 60)

print(balance_risks.head())


print("\n" + "=" * 60)
print("ПЕРВЫЕ СТРОКИ COMBAT SCENARIOS")
print("=" * 60)

print(combat_scenarios.head())
# ============================================================
# 4. ПОДРОБНО ИЗУЧАЕМ СТРУКТУРУ BALANCE_TESTS
# ============================================================

print("\n" + "=" * 60)
print("DETAILED BALANCE TESTS INSPECTION")
print("=" * 60)


# ------------------------------------------------------------
# 4.1. Выводим точные названия всех столбцов
# ------------------------------------------------------------

print("\nСтолбцы balance_tests.csv:")

for column_number, column_name in enumerate(
    balance_tests.columns,
    start=1
):
    print(f"{column_number}. {column_name}")


# ------------------------------------------------------------
# 4.2. Выводим количество строк и столбцов
# ------------------------------------------------------------

rows_count = balance_tests.shape[0]
columns_count = balance_tests.shape[1]

print(
    f"\nРазмер таблицы: "
    f"{rows_count} строк x {columns_count} столбцов"
)


# ------------------------------------------------------------
# 4.3. Проверяем типы данных
# ------------------------------------------------------------

print("\nТипы данных столбцов:")

print(
    balance_tests.dtypes.to_string()
)


# ------------------------------------------------------------
# 4.4. Проверяем пропущенные значения
# ------------------------------------------------------------

missing_values = balance_tests.isna().sum()

print("\nКоличество пропущенных значений:")

print(
    missing_values.to_string()
)


# ------------------------------------------------------------
# 4.5. Выводим всю таблицу без сокращения столбцов
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FULL BALANCE TESTS TABLE")
print("=" * 60)

with pd.option_context(
    "display.max_columns", None,
    "display.width", 250,
    "display.max_colwidth", 60
):
    print(
        balance_tests.to_string(index=False)
    )


print("\n" + "=" * 60)
print("ШАГ 4.2 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 5. РАЗБИРАЕМ BALANCE TESTS ПО ОДНОМУ
# ============================================================

print("\n" + "=" * 60)
print("BALANCE TESTS — ПОСТРОЧНЫЙ РАЗБОР")
print("=" * 60)


# ------------------------------------------------------------
# 5.1. Сначала ещё раз выводим названия столбцов
# ------------------------------------------------------------

print("\nСтруктура balance_tests.csv:\n")

for number, column in enumerate(balance_tests.columns, start=1):
    print(f"{number:>2}. {column}")


# ------------------------------------------------------------
# 5.2. Разбираем каждую строку отдельно
# ------------------------------------------------------------

for row_number, (_, row) in enumerate(
    balance_tests.iterrows(),
    start=1
):
    print("\n" + "-" * 60)
    print(f"ТЕСТ №{row_number}")
    print("-" * 60)

    for column in balance_tests.columns:

        value = row[column]

        # Если ячейка пустая (NaN),
        # выводим понятное обозначение <EMPTY>.
        if pd.isna(value):
            display_value = "<EMPTY>"
        else:
            display_value = value

        print(
            f"{column:<30} : {display_value}"
        )


print("\n" + "=" * 60)
print("ШАГ 4.3 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 6. ПОДГОТОВКА BALANCE_TESTS К АВТОМАТИЧЕСКОМУ АНАЛИЗУ
# ============================================================

print("\n" + "=" * 60)
print("ПОДГОТОВКА BALANCE TESTS К АВТОМАТИЗАЦИИ")
print("=" * 60)


# ------------------------------------------------------------
# 6.1. Создаём рабочую копию таблицы
# ------------------------------------------------------------

tests_clean = balance_tests.copy()


# ------------------------------------------------------------
# 6.2. Удаляем технические столбцы Unnamed
# ------------------------------------------------------------

unnamed_columns = [
    column
    for column in tests_clean.columns
    if str(column).startswith("Unnamed:")
]

if unnamed_columns:
    print("\nНайдены технические столбцы:")
    
    for column in unnamed_columns:
        print(f"- {column}")

    tests_clean = tests_clean.drop(
        columns=unnamed_columns
    )

    print("Технические столбцы удалены из рабочей копии.")
else:
    print("\nТехнические столбцы Unnamed не найдены.")


# ------------------------------------------------------------
# 6.3. Создаём функцию преобразования значений в float
# ------------------------------------------------------------

def parse_number(value):
    """
    Преобразует числовое значение из CSV в float.

    Поддерживает:
    - обычные числа;
    - десятичную запятую;
    - знак процента;
    - пустые значения NaN.

    Примеры:
    '97,5'    -> 97.5
    '-11,76%' -> -11.76
    75        -> 75.0
    NaN       -> None
    """

    # Если значение отсутствует,
    # возвращаем None.
    if pd.isna(value):
        return None

    # Если pandas уже распознал число,
    # просто преобразуем его в float.
    if isinstance(value, (int, float)):
        return float(value)

    # Всё остальное сначала превращаем в строку.
    text = str(value).strip()

    # Удаляем знак процента.
    text = text.replace("%", "")

    # Русскую десятичную запятую
    # заменяем на точку.
    text = text.replace(",", ".")

    # Пытаемся получить число.
    try:
        return float(text)

    # Если значение вообще не является числом,
    # возвращаем None.
    except ValueError:
        return None


# ------------------------------------------------------------
# 6.4. Проверяем функцию на понятных примерах
# ------------------------------------------------------------

number_examples = [
    "97,5",
    "112,5",
    "-11,76%",
    "15,38%",
    75,
    None,
]

print("\nПроверка parse_number():")

for example in number_examples:
    converted = parse_number(example)

    print(
        f"{str(example):>10} -> {converted}"
    )


# ------------------------------------------------------------
# 6.5. Создаём числовые версии важных столбцов
# ------------------------------------------------------------

tests_clean["Old_Value_Num"] = (
    tests_clean["Old_Value"].apply(parse_number)
)

tests_clean["New_Value_Num"] = (
    tests_clean["New_Value"].apply(parse_number)
)

tests_clean["Change_Percent_Num"] = (
    tests_clean["Change_Percent"].apply(parse_number)
)

tests_clean["Value_Num"] = (
    tests_clean["Value"].apply(parse_number)
)


# ------------------------------------------------------------
# 6.6. Проверяем результат преобразования
# ------------------------------------------------------------

print("\nЧисловые значения после очистки:")

print(
    tests_clean[
        [
            "Test_ID",
            "Metric",
            "Old_Value",
            "Old_Value_Num",
            "New_Value",
            "New_Value_Num",
            "Change_Percent",
            "Change_Percent_Num",
            "Value",
            "Value_Num",
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 6.7. Проверяем количество тестов разных типов
# ------------------------------------------------------------

numeric_change_tests = tests_clean[
    tests_clean["Old_Value_Num"].notna()
    & tests_clean["New_Value_Num"].notna()
]

role_benchmark_tests = tests_clean[
    tests_clean["Metric"] == "Role_Benchmark"
]


print("\nКоличество тестов с Old/New Value:")
print(len(numeric_change_tests))

print("\nКоличество Role Benchmark тестов:")
print(len(role_benchmark_tests))


print("\n" + "=" * 60)
print("ШАГ 4.4 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 7. АВТОМАТИЧЕСКАЯ ПРОВЕРКА CHANGE_PERCENT
# ============================================================

print("\n" + "=" * 60)
print("АВТОМАТИЧЕСКАЯ ПРОВЕРКА CHANGE_PERCENT")
print("=" * 60)


# ------------------------------------------------------------
# 7.1. Создаём функцию расчёта процента изменения
# ------------------------------------------------------------

def calculate_change_percent(old_value, new_value):
    """
    Рассчитывает процент изменения:

    ((New - Old) / Old) * 100

    Если одно из значений отсутствует
    или Old_Value равен нулю,
    возвращает None.
    """

    if old_value is None or new_value is None:
        return None

    if pd.isna(old_value) or pd.isna(new_value):
        return None

    if old_value == 0:
        return None

    return (
        (new_value - old_value)
        / old_value
        * 100
    )


# ------------------------------------------------------------
# 7.2. Рассчитываем процент независимо от CSV
# ------------------------------------------------------------

tests_clean["Calculated_Change_Percent"] = (
    tests_clean.apply(
        lambda row: calculate_change_percent(
            row["Old_Value_Num"],
            row["New_Value_Num"],
        ),
        axis=1,
    )
)


# ------------------------------------------------------------
# 7.3. Считаем разницу между записанным
#      и рассчитанным процентом
# ------------------------------------------------------------

tests_clean["Change_Difference"] = (
    tests_clean["Calculated_Change_Percent"]
    - tests_clean["Change_Percent_Num"]
).abs()


# ------------------------------------------------------------
# 7.4. Задаём допустимую погрешность
# ------------------------------------------------------------

change_tolerance = 0.02


# ------------------------------------------------------------
# 7.5. Проверяем совпадение
# ------------------------------------------------------------

def check_change_percent(row):
    """
    True  — записанный процент совпадает с расчётом.
    False — обнаружено расхождение.
    None  — тест не использует Old/New Value.
    """

    calculated = row["Calculated_Change_Percent"]
    recorded = row["Change_Percent_Num"]

    if pd.isna(calculated) or pd.isna(recorded):
        return None

    return abs(calculated - recorded) <= change_tolerance


tests_clean["Change_Percent_Valid"] = (
    tests_clean.apply(
        check_change_percent,
        axis=1,
    )
)


# ------------------------------------------------------------
# 7.6. Выводим проверяемые тесты
# ------------------------------------------------------------

change_validation = tests_clean[
    tests_clean["Calculated_Change_Percent"].notna()
][
    [
        "Test_ID",
        "Metric",
        "Old_Value_Num",
        "New_Value_Num",
        "Change_Percent_Num",
        "Calculated_Change_Percent",
        "Change_Difference",
        "Change_Percent_Valid",
    ]
]


print("\nПроверка процентов изменения:")

print(
    change_validation
    .round(4)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 7.7. Считаем результаты проверки
# ------------------------------------------------------------

valid_change_count = (
    change_validation["Change_Percent_Valid"]
    .eq(True)
    .sum()
)

invalid_change_count = (
    change_validation["Change_Percent_Valid"]
    .eq(False)
    .sum()
)


print("\nКорректных Change_Percent:")
print(valid_change_count)

print("\nНекорректных Change_Percent:")
print(invalid_change_count)


# ------------------------------------------------------------
# 7.8. Отдельно показываем ошибки, если они есть
# ------------------------------------------------------------

invalid_changes = change_validation[
    change_validation["Change_Percent_Valid"] == False
]

if invalid_changes.empty:

    print(
        "\nOK: все записанные Change_Percent "
        "совпадают с независимым расчётом Python."
    )

else:

    print(
        "\nWARNING: обнаружены несовпадения "
        "Change_Percent:"
    )

    print(
        invalid_changes
        .round(4)
        .to_string(index=False)
    )


print("\n" + "=" * 60)
print("ШАГ 4.5 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 8. АВТОМАТИЧЕСКАЯ ОЦЕНКА ЧИСЛОВЫХ BALANCE TESTS
# ============================================================

print("\n" + "=" * 60)
print("АВТОМАТИЧЕСКАЯ ОЦЕНКА ЧИСЛОВЫХ BALANCE TESTS")
print("=" * 60)


# ------------------------------------------------------------
# 8.1. Отбираем только тесты с Old_Value и New_Value
# ------------------------------------------------------------

numeric_tests = tests_clean[
    tests_clean["Old_Value_Num"].notna()
    & tests_clean["New_Value_Num"].notna()
].copy()


print("\nКоличество числовых тестов:")
print(len(numeric_tests))


# ------------------------------------------------------------
# 8.2. Определяем ожидаемое направление изменения
# ------------------------------------------------------------
#
# Здесь важно:
#
# Improved НЕ всегда означает, что число должно увеличиться.
#
# Например:
#
# Blood Rush DPS:
# больше DPS -> усиление способности.
#
# Но HP_per_Cost Skeleton:
# после повышения стоимости показатель уменьшился,
# и это тоже было целевым балансным изменением.
#
# Поэтому направление изменения зависит от конкретного теста.
# ------------------------------------------------------------

expected_directions = {
    "TEST_001": "decrease",
    "TEST_002": "decrease",
    "TEST_003": "increase",
    "TEST_004": "increase",
}


# ------------------------------------------------------------
# 8.3. Функция определяет фактическое направление
# ------------------------------------------------------------

def get_actual_direction(old_value, new_value):
    """
    Определяет направление изменения метрики.

    increase -> значение увеличилось
    decrease -> значение уменьшилось
    unchanged -> значение не изменилось
    """

    if new_value > old_value:
        return "increase"

    if new_value < old_value:
        return "decrease"

    return "unchanged"


numeric_tests["Actual_Direction"] = (
    numeric_tests.apply(
        lambda row: get_actual_direction(
            row["Old_Value_Num"],
            row["New_Value_Num"],
        ),
        axis=1,
    )
)


# ------------------------------------------------------------
# 8.4. Добавляем ожидаемое направление
# ------------------------------------------------------------

numeric_tests["Expected_Direction"] = (
    numeric_tests["Test_ID"]
    .map(expected_directions)
)


# ------------------------------------------------------------
# 8.5. Python самостоятельно проверяет тест
# ------------------------------------------------------------

numeric_tests["Auto_Passed"] = (
    numeric_tests["Actual_Direction"]
    == numeric_tests["Expected_Direction"]
)


# ------------------------------------------------------------
# 8.6. Преобразуем автоматический результат
#      в понятный текст
# ------------------------------------------------------------

numeric_tests["Auto_Result"] = (
    numeric_tests["Auto_Passed"]
    .map(
        {
            True: "Passed",
            False: "Failed",
        }
    )
)


# ------------------------------------------------------------
# 8.7. Выводим результат
# ------------------------------------------------------------

numeric_result_view = numeric_tests[
    [
        "Test_ID",
        "Metric",
        "Old_Value_Num",
        "New_Value_Num",
        "Calculated_Change_Percent",
        "Expected_Direction",
        "Actual_Direction",
        "Auto_Result",
    ]
]


print("\nАвтоматические результаты числовых тестов:")

print(
    numeric_result_view
    .round(4)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 8.8. Считаем Passed / Failed
# ------------------------------------------------------------

auto_passed_count = (
    numeric_tests["Auto_Passed"]
    .eq(True)
    .sum()
)

auto_failed_count = (
    numeric_tests["Auto_Passed"]
    .eq(False)
    .sum()
)


print("\nАвтоматически пройдено тестов:")
print(auto_passed_count)

print("\nАвтоматически провалено тестов:")
print(auto_failed_count)


# ------------------------------------------------------------
# 8.9. Показываем Failed отдельно
# ------------------------------------------------------------

failed_numeric_tests = numeric_tests[
    numeric_tests["Auto_Passed"] == False
]


if failed_numeric_tests.empty:

    print(
        "\nOK: все числовые balance tests "
        "изменились в ожидаемом направлении."
    )

else:

    print(
        "\nWARNING: обнаружены числовые balance tests, "
        "которые изменились не в ожидаемом направлении:"
    )

    print(
        failed_numeric_tests[
            [
                "Test_ID",
                "Metric",
                "Old_Value_Num",
                "New_Value_Num",
                "Expected_Direction",
                "Actual_Direction",
            ]
        ]
        .to_string(index=False)
    )


print("\n" + "=" * 60)
print("ШАГ 4.6 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 9. ПРОВЕРКА ВЕЛИЧИНЫ БАЛАНСНЫХ ИЗМЕНЕНИЙ
# ============================================================

print("\n" + "=" * 60)
print("ПРОВЕРКА ВЕЛИЧИНЫ БАЛАНСНЫХ ИЗМЕНЕНИЙ")
print("=" * 60)


# ------------------------------------------------------------
# 9.1. Задаём допустимый диапазон изменения
# ------------------------------------------------------------
#
# Для текущей balance iteration v0.2 используем
# рабочий sanity-check:
#
# минимум: 5%
# максимум: 25%
#
# Это НЕ универсальное правило для всех игр.
# Это критерий именно нашей текущей итерации.
# ------------------------------------------------------------

min_change_percent = 5.0
max_change_percent = 25.0


print("\nДопустимый диапазон абсолютного изменения:")
print(
    f"{min_change_percent:.2f}% "
    f"- {max_change_percent:.2f}%"
)


# ------------------------------------------------------------
# 9.2. Берём абсолютную величину изменения
# ------------------------------------------------------------
#
# Например:
#
# -11.76% -> 11.76%
# +15.38% -> 15.38%
#
# Здесь нас интересует именно СИЛА изменения,
# а направление мы уже проверили на шаге 4.6.
# ------------------------------------------------------------

numeric_tests["Absolute_Change_Percent"] = (
    numeric_tests["Calculated_Change_Percent"].abs()
)


# ------------------------------------------------------------
# 9.3. Проверяем нижнюю границу
# ------------------------------------------------------------

numeric_tests["Above_Min_Change"] = (
    numeric_tests["Absolute_Change_Percent"]
    >= min_change_percent
)


# ------------------------------------------------------------
# 9.4. Проверяем верхнюю границу
# ------------------------------------------------------------

numeric_tests["Below_Max_Change"] = (
    numeric_tests["Absolute_Change_Percent"]
    <= max_change_percent
)


# ------------------------------------------------------------
# 9.5. Итоговая проверка диапазона
# ------------------------------------------------------------

numeric_tests["Change_Range_Passed"] = (
    numeric_tests["Above_Min_Change"]
    & numeric_tests["Below_Max_Change"]
)


# ------------------------------------------------------------
# 9.6. Создаём текстовый статус
# ------------------------------------------------------------

def get_change_range_status(row):

    change = row["Absolute_Change_Percent"]

    if change < min_change_percent:
        return "Too Small"

    if change > max_change_percent:
        return "Too Large"

    return "Within Range"


numeric_tests["Change_Range_Status"] = (
    numeric_tests.apply(
        get_change_range_status,
        axis=1,
    )
)


# ------------------------------------------------------------
# 9.7. Выводим результаты
# ------------------------------------------------------------

change_range_view = numeric_tests[
    [
        "Test_ID",
        "Metric",
        "Calculated_Change_Percent",
        "Absolute_Change_Percent",
        "Expected_Direction",
        "Actual_Direction",
        "Change_Range_Status",
        "Change_Range_Passed",
    ]
]


print("\nПроверка величины изменений:")

print(
    change_range_view
    .round(4)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 9.8. Считаем результаты
# ------------------------------------------------------------

range_passed_count = (
    numeric_tests["Change_Range_Passed"]
    .eq(True)
    .sum()
)

range_failed_count = (
    numeric_tests["Change_Range_Passed"]
    .eq(False)
    .sum()
)


print("\nИзменений внутри допустимого диапазона:")
print(range_passed_count)

print("\nИзменений вне допустимого диапазона:")
print(range_failed_count)


# ------------------------------------------------------------
# 9.9. Показываем подозрительные изменения отдельно
# ------------------------------------------------------------

out_of_range_tests = numeric_tests[
    numeric_tests["Change_Range_Passed"] == False
]


if out_of_range_tests.empty:

    print(
        "\nOK: величина всех числовых изменений "
        "находится внутри рабочего диапазона."
    )

else:

    print(
        "\nWARNING: обнаружены изменения, "
        "выходящие за рабочий диапазон:"
    )

    print(
        out_of_range_tests[
            [
                "Test_ID",
                "Metric",
                "Calculated_Change_Percent",
                "Change_Range_Status",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )


print("\n" + "=" * 60)
print("ШАГ 4.7 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 10. ИТОГОВЫЙ СТАТУС ЧИСЛОВЫХ BALANCE TESTS
# ============================================================

print("\n" + "=" * 60)
print("ИТОГОВЫЙ СТАТУС ЧИСЛОВЫХ BALANCE TESTS")
print("=" * 60)


# ------------------------------------------------------------
# 10.1. Создаём отдельную таблицу для итоговой проверки
# ------------------------------------------------------------

numeric_test_summary = numeric_tests.copy()


print(
    "\nКоличество числовых тестов для итоговой проверки:"
)
print(len(numeric_test_summary))


# ------------------------------------------------------------
# 10.2. Формируем итоговый автоматический PASS / FAIL
# ------------------------------------------------------------
#
# Для итогового прохождения тест должен одновременно:
#
# 1. измениться в ожидаемом направлении;
# 2. находиться внутри допустимого диапазона изменения.
#
# Auto_Passed:
# True  -> направление изменения правильное;
# False -> направление изменения неправильное.
#
# Change_Range_Passed:
# True  -> величина изменения находится в диапазоне 5–25%;
# False -> изменение слишком маленькое или слишком большое.
#
# Оператор & означает логическое "И".
#
# Поэтому итоговый тест получает PASS только тогда, когда
# ОБЕ проверки одновременно имеют значение True.
# ------------------------------------------------------------

numeric_test_summary["Auto_Status"] = (
    numeric_test_summary["Auto_Passed"]
    & numeric_test_summary["Change_Range_Passed"]
).map(
    {
        True: "PASS",
        False: "FAIL",
    }
)


# ------------------------------------------------------------
# 10.3. Выводим итоговый статус каждого теста
# ------------------------------------------------------------

print("\nАвтоматический статус каждого числового теста:")

print(
    numeric_test_summary[
        [
            "Test_ID",
            "Risk_ID",
            "Version",
            "Unit_ID",
            "Metric",
            "Old_Value_Num",
            "New_Value_Num",
            "Calculated_Change_Percent",
            "Expected_Direction",
            "Actual_Direction",
            "Auto_Passed",
            "Change_Range_Status",
            "Change_Range_Passed",
            "Auto_Status",
        ]
    ]
    .round(4)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 10.4. Подсчитываем итоговое количество PASS / FAIL
# ------------------------------------------------------------

final_passed_count = (
    numeric_test_summary["Auto_Status"]
    .eq("PASS")
    .sum()
)

final_failed_count = (
    numeric_test_summary["Auto_Status"]
    .eq("FAIL")
    .sum()
)


print("\nИтогово пройдено числовых тестов:")
print(final_passed_count)

print("\nИтогово провалено числовых тестов:")
print(final_failed_count)


# ------------------------------------------------------------
# 10.5. Проверяем общий результат
# ------------------------------------------------------------

if final_failed_count == 0:

    print(
        "\nOK: все числовые balance tests прошли "
        "автоматическую итоговую проверку."
    )

else:

    print(
        "\nWARNING: некоторые числовые balance tests "
        "не прошли итоговую автоматическую проверку."
    )


# ------------------------------------------------------------
# 10.6. Отдельно выводим проваленные тесты
# ------------------------------------------------------------

failed_final_tests = numeric_test_summary[
    numeric_test_summary["Auto_Status"] == "FAIL"
]


if failed_final_tests.empty:

    print(
        "\nПроваленных числовых тестов нет."
    )

else:

    print(
        "\nЧисловые тесты со статусом FAIL:"
    )

    print(
        failed_final_tests[
            [
                "Test_ID",
                "Risk_ID",
                "Unit_ID",
                "Metric",
                "Expected_Direction",
                "Actual_Direction",
                "Calculated_Change_Percent",
                "Change_Range_Status",
                "Auto_Status",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )


print("\n" + "=" * 60)
print("ШАГ 4.8 ЗАВЕРШЁН")
print("=" * 60)
# ============================================================
# 11. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ BALANCE TESTS
# ============================================================

print("\n" + "=" * 60)
print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ BALANCE TESTS")
print("=" * 60)


# ------------------------------------------------------------
# 11.1. Подготавливаем каталог для результатов
# ------------------------------------------------------------

results_dir = Path("analysis") / "results"

results_dir.mkdir(
    parents=True,
    exist_ok=True,
)

print(f"\nКаталог для результатов:")
print(results_dir)

print(
    "Каталог существует: "
    f"{results_dir.exists()}"
)
# ------------------------------------------------------------
# 11.2. Сохраняем полные результаты числовых balance tests
# ------------------------------------------------------------

numeric_results_path = (
    results_dir / "numeric_balance_test_results.csv"
)

numeric_test_summary.to_csv(
    numeric_results_path,
    index=False,
    encoding="utf-8-sig",
)

print("\nПолные результаты числовых тестов сохранены:")
print(numeric_results_path)

print(
    "Файл существует: "
    f"{numeric_results_path.exists()}"
)
# ------------------------------------------------------------
# 11.3. Проверяем сохранённый CSV
# ------------------------------------------------------------

saved_numeric_results = pd.read_csv(
    numeric_results_path,
    encoding="utf-8-sig",
)

print("\nПроверка сохранённого файла:")

print(
    "Количество сохранённых строк: "
    f"{len(saved_numeric_results)}"
)

print(
    "Количество сохранённых столбцов: "
    f"{len(saved_numeric_results.columns)}"
)

print("\nСохранённые столбцы:")
print(saved_numeric_results.columns.tolist())

numeric_results_shape_ok = (
    saved_numeric_results.shape
    == numeric_test_summary.shape
)

numeric_results_columns_ok = (
    saved_numeric_results.columns.tolist()
    == numeric_test_summary.columns.tolist()
)

print(
    "\nРазмер таблицы совпадает с исходным результатом: "
    f"{numeric_results_shape_ok}"
)

print(
    "Структура столбцов совпадает с исходным результатом: "
    f"{numeric_results_columns_ok}"
)
# ------------------------------------------------------------
# 11.4. Проверяем целостность данных после сохранения и чтения
# ------------------------------------------------------------

# Метод DataFrame.equals() сравнивает две таблицы целиком:
# - одинаковы ли их размеры;
# - одинаковы ли названия и порядок столбцов;
# - одинаковы ли значения в соответствующих ячейках;
# - NaN в одинаковых позициях считаются совпадающими.
#
# Это удобнее обычного оператора ==, потому что выражение
#
# numeric_test_summary == saved_numeric_results
#
# вернуло бы не один итоговый True / False,
# а целую таблицу логических значений для каждой ячейки.

numeric_results_data_equal = (
    numeric_test_summary.equals(saved_numeric_results)
)

print(
    "\nСодержимое сохранённого файла полностью совпадает "
    "с исходным результатом: "
    f"{numeric_results_data_equal}"
)
# ------------------------------------------------------------
# 11.4.2. Сравниваем типы данных до и после CSV round-trip
# ------------------------------------------------------------

dtype_comparison = pd.DataFrame(
    {
        "Before_Save": numeric_test_summary.dtypes.astype(str),
        "After_Load": saved_numeric_results.dtypes.astype(str),
    }
)

dtype_comparison["Same_Dtype"] = (
    dtype_comparison["Before_Save"]
    == dtype_comparison["After_Load"]
)

print("\nСравнение типов данных до и после сохранения:")
print(dtype_comparison.to_string())

different_dtypes = dtype_comparison[
    ~dtype_comparison["Same_Dtype"]
]

print("\nКоличество столбцов с изменившимся типом данных:")
print(len(different_dtypes))

if different_dtypes.empty:
    print("OK: типы данных всех столбцов совпадают.")
else:
    print("\nСтолбцы с изменившимся типом данных:")
    print(different_dtypes.to_string())
# ------------------------------------------------------------
# 11.4.3. Ищем реальные различия в значениях
# ------------------------------------------------------------

# Сравниваем таблицы по значениям, не требуя полного совпадения
# внутренних pandas dtype.
#
# Для каждой пары ячеек считаем значения одинаковыми, если:
# 1) они равны через оператор ==;
# ИЛИ
# 2) обе ячейки содержат пропущенное значение NaN.

value_equality_mask = (
    numeric_test_summary.eq(saved_numeric_results)
    | (
        numeric_test_summary.isna()
        & saved_numeric_results.isna()
    )
)

# Проверяем, являются ли абсолютно все ячейки одинаковыми.
all_values_equal = value_equality_mask.to_numpy().all()

print(
    "\nВсе значения до и после сохранения совпадают: "
    f"{all_values_equal}"
)

# Считаем количество несовпадающих ячеек.
different_cells_count = (
    ~value_equality_mask
).to_numpy().sum()

print(
    "Количество несовпадающих ячеек: "
    f"{different_cells_count}"
)    
# ------------------------------------------------------------
# 11.4.4. Показываем конкретные несовпадающие ячейки
# ------------------------------------------------------------

difference_mask = ~value_equality_mask

difference_positions = difference_mask.stack()

difference_positions = difference_positions[
    difference_positions
]

print("\nКонкретные несовпадающие ячейки:")

if difference_positions.empty:
    print("Несовпадающих ячеек нет.")
else:
    for row_index, column_name in difference_positions.index:
        before_value = numeric_test_summary.loc[
            row_index,
            column_name,
        ]

        after_value = saved_numeric_results.loc[
            row_index,
            column_name,
        ]

        print(
            f"Строка {row_index}, "
            f"столбец '{column_name}': "
            f"до = {before_value!r}, "
            f"после = {after_value!r}"
        )
# ------------------------------------------------------------
# 11.4.5. Выполняем корректную проверку CSV round-trip
# ------------------------------------------------------------

# Создаём итоговую маску совпадений того же размера,
# что и исходная таблица.
roundtrip_equality_mask = pd.DataFrame(
    True,
    index=numeric_test_summary.index,
    columns=numeric_test_summary.columns,
)

# Проверяем каждый столбец отдельно.
for column_name in numeric_test_summary.columns:

    before_column = numeric_test_summary[column_name]
    after_column = saved_numeric_results[column_name]

    # Если оба столбца числовые, сравниваем значения
    # с небольшим допустимым отклонением.
    if (
        pd.api.types.is_numeric_dtype(before_column)
        and pd.api.types.is_numeric_dtype(after_column)
    ):
        roundtrip_equality_mask[column_name] = np.isclose(
            before_column,
            after_column,
            rtol=1e-12,
            atol=1e-12,
            equal_nan=True,
        )

    # Для остальных данных используем обычное сравнение,
    # отдельно считая NaN в одинаковых позициях совпадением.
    else:
        roundtrip_equality_mask[column_name] = (
            before_column.eq(after_column)
            | (
                before_column.isna()
                & after_column.isna()
            )
        )

roundtrip_values_ok = (
    roundtrip_equality_mask.to_numpy().all()
)

roundtrip_different_cells = (
    ~roundtrip_equality_mask
).to_numpy().sum()

print(
    "\nКорректная проверка значений с учётом "
    "погрешности float:"
)
print(
    "Все значения эквивалентны: "
    f"{roundtrip_values_ok}"
)
print(
    "Количество существенных различий: "
    f"{roundtrip_different_cells}"
) 
# ============================================================
# 11.5. ИТОГОВАЯ ПРОВЕРКА СОХРАНЕНИЯ РЕЗУЛЬТАТОВ
# ============================================================

print("\n" + "=" * 60)
print("ИТОГОВАЯ ПРОВЕРКА СОХРАНЕНИЯ РЕЗУЛЬТАТОВ")
print("=" * 60)

# Собираем все действительно важные проверки.
save_validation_checks = {
    "Results_Directory_Exists": results_dir.exists(),
    "Results_File_Exists": numeric_results_path.exists(),
    "Table_Shape_Preserved": numeric_results_shape_ok,
    "Column_Structure_Preserved": numeric_results_columns_ok,
    "Values_Preserved": roundtrip_values_ok,
}

# Выводим каждую проверку отдельно.
for check_name, passed in save_validation_checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{check_name}: {status}")

# Общий PASS возможен только тогда,
# когда абсолютно все проверки дали True.
all_save_checks_passed = all(save_validation_checks.values())

print("-" * 60)

if all_save_checks_passed:
    print("RESULTS SAVE VALIDATION: PASS")
else:
    print("RESULTS SAVE VALIDATION: FAIL")

print("=" * 60) 
# ============================================================
# 12. ИТОГОВАЯ СВОДКА ЗАПУСКА BALANCE TESTS
# ============================================================

print("\n" + "=" * 60)
print("ИТОГОВАЯ СВОДКА BALANCE TESTS")
print("=" * 60)

# ------------------------------------------------------------
# 12.1. Подсчитываем результаты числовых тестов
# ------------------------------------------------------------

total_numeric_tests = len(numeric_test_summary)

passed_numeric_tests = int(
    numeric_test_summary["Auto_Passed"].sum()
)

failed_numeric_tests = (
    total_numeric_tests - passed_numeric_tests
)

pass_rate = (
    passed_numeric_tests / total_numeric_tests * 100
    if total_numeric_tests > 0
    else 0.0
)

print(f"Всего числовых тестов: {total_numeric_tests}")
print(f"Пройдено: {passed_numeric_tests}")
print(f"Провалено: {failed_numeric_tests}")
print(f"Процент успешного прохождения: {pass_rate:.2f}%")   
# ------------------------------------------------------------
# 12.2. Формируем общий статус запуска
# ------------------------------------------------------------

numeric_tests_passed = (
    failed_numeric_tests == 0
    and total_numeric_tests > 0
)

overall_run_passed = (
    numeric_tests_passed
    and all_save_checks_passed
)

print("\n" + "-" * 60)

print(
    "Статус числовых balance tests: "
    + ("PASS" if numeric_tests_passed else "FAIL")
)

print(
    "Статус сохранения результатов: "
    + ("PASS" if all_save_checks_passed else "FAIL")
)

print("-" * 60)

if overall_run_passed:
    print("OVERALL BALANCE TEST RUN: PASS")
else:
    print("OVERALL BALANCE TEST RUN: FAIL")

print("=" * 60)   
# ------------------------------------------------------------
# 12.3. Выводим краткую сводку по каждому balance test
# ------------------------------------------------------------

print("\nКРАТКАЯ СВОДКА ПО ЧИСЛОВЫМ BALANCE TESTS")
print("-" * 60)

summary_columns = [
    "Test_ID",
    "Risk_ID",
    "Version",
    "Unit_ID",
    "Metric",
    "Calculated_Change_Percent",
    "Auto_Status",
]

print(
    numeric_test_summary[
        summary_columns
    ].round(4).to_string(index=False)
)
# ------------------------------------------------------------
# 12.4. Финальный статус выполнения скрипта
# ------------------------------------------------------------

print("\n" + "=" * 60)

if overall_run_passed:
    print("BALANCE TEST PIPELINE COMPLETED SUCCESSFULLY")
else:
    print("BALANCE TEST PIPELINE COMPLETED WITH FAILURES")

print("=" * 60)