import csv
import os


# ============================================================
# 1. ПУТИ К ФАЙЛАМ
# ============================================================

ITERATION_FILE = (
    "analysis/results/iterations/"
    "balance_iteration_01.csv"
)

OUTPUT_DIR = (
    "analysis/results/iterations/"
    "analysis"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_analysis.csv",
)


# ============================================================
# 2. СОЗДАЁМ ПАПКУ ДЛЯ РЕЗУЛЬТАТОВ
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)


print("=" * 70)
print("ERA OF STRIFE — BALANCE ITERATION ANALYSIS")
print("=" * 70)

print()
print("Исходный файл итерации:")
print(ITERATION_FILE)

print()
print("Файл анализа:")
print(OUTPUT_FILE)
# ============================================================
# 3. ЧТЕНИЕ РЕЗУЛЬТАТОВ BALANCE ITERATION 01
# ============================================================

iteration_rows = []

with open(
    ITERATION_FILE,
    "r",
    encoding="utf-8-sig",
    newline="",
) as file:

    reader = csv.DictReader(file)

    print()
    print("=" * 70)
    print("ПРОВЕРКА СТРУКТУРЫ ИСХОДНОГО CSV")
    print("=" * 70)

    print()
    print("Столбцы файла:")

    for column_name in reader.fieldnames:
        print(" -", column_name)

    for row in reader:
        iteration_rows.append(row)


# ============================================================
# 4. ПРОВЕРКА КОЛИЧЕСТВА ЗАГРУЖЕННЫХ ЮНИТОВ
# ============================================================

print()
print("=" * 70)
print("ЗАГРУЗКА ДАННЫХ")
print("=" * 70)

print()
print(
    "Количество загруженных строк:",
    len(iteration_rows),
)

print()
print("Загруженные юниты:")
analysis_results = []
for row in iteration_rows:
    print(
        " -",
        row["Unit_ID"],
        "|",
        row["Unit_Name"],
    )
    # ============================================================
# 5. РАСЧЁТ ЭФФЕКТА BALANCE ITERATION 01
# ============================================================

TARGET_WIN_RATE = 50.0

analysis_rows = []

print()
print("=" * 70)
print("АНАЛИЗ ИЗМЕНЕНИЯ WIN RATE")
print("=" * 70)


for row in iteration_rows:

    # --------------------------------------------------------
    # 5.1. Получаем основные данные юнита
    # --------------------------------------------------------

    unit_id = row["Unit_ID"]
    unit_name = row["Unit_Name"]

    old_win_rate = float(row["Before_Win_Rate"])
    new_win_rate = float(row["After_Win_Rate"])

    # --------------------------------------------------------
    # 5.2. Считаем изменение Win Rate
    # --------------------------------------------------------
   
    win_rate_change = (
        new_win_rate
        - old_win_rate
    )


    # --------------------------------------------------------
    # 5.3. Считаем расстояние от целевого Win Rate = 50%
    # --------------------------------------------------------

    old_distance = abs(
        old_win_rate
        - TARGET_WIN_RATE
    )

    new_distance = abs(
        new_win_rate
        - TARGET_WIN_RATE
    )


    # --------------------------------------------------------
    # 5.4. Считаем изменение расстояния от 50%
    # --------------------------------------------------------

    distance_change = (
        new_distance
        - old_distance
    )


    # --------------------------------------------------------
    # 5.5. Определяем результат итерации
    # --------------------------------------------------------

    if new_distance < old_distance:
        result = "Improved"

    elif new_distance > old_distance:
        result = "Worsened"

    else:
        result = "Unchanged"


    # --------------------------------------------------------
    # 5.6. Проверяем, изменяли ли юнита напрямую
    # --------------------------------------------------------

    iteration_target = row["Iteration_Target"]

    if iteration_target == "Yes":
        change_type = "Direct"

    else:
        change_type = "Indirect"


    # --------------------------------------------------------
    # 5.7. Сохраняем рассчитанные показатели
    # --------------------------------------------------------

    analysis_row = {
        "Unit_ID": unit_id,
        "Unit_Name": unit_name,
        "Change_Type": change_type,
        "Old_Win_Rate": old_win_rate,
        "New_Win_Rate": new_win_rate,
        "Win_Rate_Change": win_rate_change,
        "Old_Distance_From_50": old_distance,
        "New_Distance_From_50": new_distance,
        "Distance_Change": distance_change,
        "Iteration_Result": result,
    }

    analysis_rows.append(analysis_row)


    # --------------------------------------------------------
    # 5.8. Выводим результат в терминал
    # --------------------------------------------------------

    print()
    print(
        unit_id,
        "|",
        unit_name,
    )

    print(
        "  Тип изменения:",
        change_type,
    )

    print(
        "  Win Rate:",
        round(old_win_rate, 2),
        "% ->",
        round(new_win_rate, 2),
        "%",
    )

    print(
        "  Delta Win Rate:",
        round(win_rate_change, 2),
        "п.п.",
    )

    print(
        "  Расстояние от 50%:",
        round(old_distance, 2),
        "п.п. ->",
        round(new_distance, 2),
        "п.п.",
    )

    print(
        "  Результат:",
        result,
    )

    # ============================================================
# 6. АГРЕГИРОВАННЫЙ АНАЛИЗ ИТЕРАЦИИ
# ============================================================

print()
print("=" * 70)
print("ОБЩИЙ РЕЗУЛЬТАТ BALANCE ITERATION 01")
print("=" * 70)


# ------------------------------------------------------------
# 6.1. Считаем количество результатов каждого типа
# ------------------------------------------------------------

improved_count = sum(
    1
    for row in analysis_rows
    if row["Iteration_Result"] == "Improved"
)

worsened_count = sum(
    1
    for row in analysis_rows
    if row["Iteration_Result"] == "Worsened"
)

unchanged_count = sum(
    1
    for row in analysis_rows
    if row["Iteration_Result"] == "Unchanged"
)

total_units = len(analysis_rows)


print()
print("Количество проанализированных юнитов:", total_units)
print("Improved:", improved_count)
print("Worsened:", worsened_count)
print("Unchanged:", unchanged_count)


# ------------------------------------------------------------
# 6.2. Считаем Direct и Indirect изменения
# ------------------------------------------------------------

direct_count = sum(
    1
    for row in analysis_rows
    if row["Change_Type"] == "Direct"
)

indirect_count = sum(
    1
    for row in analysis_rows
    if row["Change_Type"] == "Indirect"
)


print()
print("Типы изменений:")
print("Direct:", direct_count)
print("Indirect:", indirect_count)


# ------------------------------------------------------------
# 6.3. Среднее расстояние Win Rate от целевых 50%
# ------------------------------------------------------------

average_old_distance = sum(
    row["Old_Distance_From_50"]
    for row in analysis_rows
) / total_units

average_new_distance = sum(
    row["New_Distance_From_50"]
    for row in analysis_rows
) / total_units


average_distance_change = (
    average_new_distance
    - average_old_distance
)


print()
print("Среднее расстояние Win Rate от 50%:")
print(
    "До итерации:",
    round(average_old_distance, 2),
    "п.п.",
)

print(
    "После итерации:",
    round(average_new_distance, 2),
    "п.п.",
)

print(
    "Изменение:",
    round(average_distance_change, 2),
    "п.п.",
)


# ------------------------------------------------------------
# 6.4. Определяем общий результат итерации
# ------------------------------------------------------------

if average_new_distance < average_old_distance:
    overall_result = "Improved"

elif average_new_distance > average_old_distance:
    overall_result = "Worsened"

else:
    overall_result = "Unchanged"


print()
print("Общий результат итерации:", overall_result)


# ------------------------------------------------------------
# 6.5. Дополнительная проверка результата
# ------------------------------------------------------------

if improved_count > worsened_count:
    unit_result = "More units improved than worsened"

elif improved_count < worsened_count:
    unit_result = "More units worsened than improved"

else:
    unit_result = "Equal number of improved and worsened units"


print("Результат по количеству юнитов:", unit_result)


# ------------------------------------------------------------
# 6.6. Сохраняем детальный анализ в CSV
# ------------------------------------------------------------

analysis_fieldnames = [
    "Unit_ID",
    "Unit_Name",
    "Change_Type",
    "Old_Win_Rate",
    "New_Win_Rate",
    "Win_Rate_Change",
    "Old_Distance_From_50",
    "New_Distance_From_50",
    "Distance_Change",
    "Iteration_Result",
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=analysis_fieldnames,
    )

    writer.writeheader()
    writer.writerows(analysis_rows)


# ------------------------------------------------------------
# 6.7. Сохраняем сводный результат итерации
# ------------------------------------------------------------

SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "balance_iteration_01_overall_summary.csv",
)

summary_fieldnames = [
    "Total_Units",
    "Improved",
    "Worsened",
    "Unchanged",
    "Direct_Changes",
    "Indirect_Changes",
    "Average_Distance_Before",
    "Average_Distance_After",
    "Average_Distance_Change",
    "Overall_Result",
]

summary_row = {
    "Total_Units": total_units,
    "Improved": improved_count,
    "Worsened": worsened_count,
    "Unchanged": unchanged_count,
    "Direct_Changes": direct_count,
    "Indirect_Changes": indirect_count,
    "Average_Distance_Before": round(
        average_old_distance,
        2,
    ),
    "Average_Distance_After": round(
        average_new_distance,
        2,
    ),
    "Average_Distance_Change": round(
        average_distance_change,
        2,
    ),
    "Overall_Result": overall_result,
}

with open(
    SUMMARY_FILE,
    "w",
    encoding="utf-8-sig",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=summary_fieldnames,
    )

    writer.writeheader()
    writer.writerow(summary_row)


# ------------------------------------------------------------
# 6.8. Финальный вывод
# ------------------------------------------------------------

print()
print("=" * 70)
print("АНАЛИЗ BALANCE ITERATION 01 ЗАВЕРШЁН")
print("=" * 70)

print()
print("Детальный анализ:")
print(OUTPUT_FILE)

print()
print("Сводный анализ:")
print(SUMMARY_FILE)

print()
print(
    "Исходный unit_balance.csv не изменялся."
)