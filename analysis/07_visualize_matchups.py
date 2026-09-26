import csv
import os
import matplotlib.pyplot as plt


# ============================================================
# НАСТРОЙКИ
# ============================================================

# Файл с результатами всех попарных матчапов.
MATCHUP_FILE = "analysis/results/matchup_statistics.csv"

# Файл с агрегированной статистикой юнитов.
UNIT_STATISTICS_FILE = "analysis/results/unit_combat_statistics.csv"

# Папка, в которую будут сохраняться изображения.
OUTPUT_DIR = "analysis/results/visualizations"


# ============================================================
# СОЗДАНИЕ ПАПКИ ДЛЯ РЕЗУЛЬТАТОВ
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# ЗАГРУЗКА MATCHUP_STATISTICS.CSV
# ============================================================

matchups = []

with open(
    MATCHUP_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        matchups.append(row)


print("=" * 70)
print("ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ МАТЧАПОВ")
print("=" * 70)

print("Файл матчапов:", MATCHUP_FILE)
print("Загружено матчапов:", len(matchups))


# ============================================================
# ЗАГРУЗКА СТАТИСТИКИ ЮНИТОВ
# ============================================================

unit_statistics = []

with open(
    UNIT_STATISTICS_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        row["Battles"] = int(row["Battles"])
        row["Wins"] = int(row["Wins"])
        row["Losses"] = int(row["Losses"])
        row["Draws"] = int(row["Draws"])

        row["Win_Rate"] = float(row["Win_Rate"])
        row["Draw_Rate"] = float(row["Draw_Rate"])
        row["Combat_Score"] = float(row["Combat_Score"])

        unit_statistics.append(row)


print(
    "Загружено записей статистики юнитов:",
    len(unit_statistics)
)


# ============================================================
# ФОРМИРОВАНИЕ СПИСКА ЮНИТОВ
# ============================================================

units = {}

for matchup in matchups:

    unit_a_id = matchup["Unit_A_ID"]
    unit_b_id = matchup["Unit_B_ID"]

    if unit_a_id not in units:

        units[unit_a_id] = {
            "Unit_ID": unit_a_id,
            "Unit_Name": matchup["Unit_A_Name"],
            "Role": matchup["Unit_A_Role"]
        }

    if unit_b_id not in units:

        units[unit_b_id] = {
            "Unit_ID": unit_b_id,
            "Unit_Name": matchup["Unit_B_Name"],
            "Role": matchup["Unit_B_Role"]
        }


unit_ids = list(units.keys())


print(
    "Обнаружено уникальных юнитов:",
    len(unit_ids)
)


# ============================================================
# СОЗДАНИЕ ЧИСЛОВОЙ MATCHUP-МАТРИЦЫ
# ============================================================

# Используем следующие значения:
#
#  1  = победа
#  0  = ничья
# -1  = поражение
#
# Диагональ означает бой юнита против самого себя.
# Такие бои не проводились, поэтому используем 0.

matchup_matrix = {}

for unit_a_id in unit_ids:

    matchup_matrix[unit_a_id] = {}

    for unit_b_id in unit_ids:

        matchup_matrix[unit_a_id][unit_b_id] = 0


# ============================================================
# ЗАПОЛНЕНИЕ MATCHUP-МАТРИЦЫ
# ============================================================

for matchup in matchups:

    unit_a_id = matchup["Unit_A_ID"]
    unit_b_id = matchup["Unit_B_ID"]

    result = matchup["Result"]

    if result == "Win":

        matchup_matrix[unit_a_id][unit_b_id] = 1
        matchup_matrix[unit_b_id][unit_a_id] = -1

    elif result == "Loss":

        matchup_matrix[unit_a_id][unit_b_id] = -1
        matchup_matrix[unit_b_id][unit_a_id] = 1

    elif result == "Draw":

        matchup_matrix[unit_a_id][unit_b_id] = 0
        matchup_matrix[unit_b_id][unit_a_id] = 0


# ============================================================
# ПРОВЕРКА МАТРИЦЫ
# ============================================================

print()
print("=" * 70)
print("ПРОВЕРКА MATCHUP-МАТРИЦЫ")
print("=" * 70)

for unit_a_id in unit_ids:

    values = []

    for unit_b_id in unit_ids:
        values.append(
            matchup_matrix[unit_a_id][unit_b_id]
        )

    print(
        unit_a_id,
        "|",
        values
    )


# ============================================================
# ПОДГОТОВКА ДАННЫХ ДЛЯ MATPLOTLIB
# ============================================================

matrix_values = []

for unit_a_id in unit_ids:

    row_values = []

    for unit_b_id in unit_ids:

        row_values.append(
            matchup_matrix[unit_a_id][unit_b_id]
        )

    matrix_values.append(row_values)


# Подписи юнитов.
unit_labels = []

for unit_id in unit_ids:

    label = (
        unit_id
        + "\n"
        + units[unit_id]["Unit_Name"]
    )

    unit_labels.append(label)


# ============================================================
# ГРАФИК №1
# MATCHUP MATRIX
# ============================================================

print()
print("=" * 70)
print("СОЗДАНИЕ MATCHUP MATRIX")
print("=" * 70)


fig, ax = plt.subplots(
    figsize=(16, 13)
)


image = ax.imshow(
    matrix_values,
    vmin=-1,
    vmax=1
)


# Подписи по оси X.
ax.set_xticks(
    range(len(unit_ids))
)

ax.set_xticklabels(
    unit_labels,
    rotation=45,
    ha="right",
    fontsize=8
)


# Подписи по оси Y.
ax.set_yticks(
    range(len(unit_ids))
)

ax.set_yticklabels(
    unit_labels,
    fontsize=8
)


# Названия осей.
ax.set_xlabel(
    "Opponent Unit",
    fontsize=11
)

ax.set_ylabel(
    "Selected Unit",
    fontsize=11
)


# Заголовок.
ax.set_title(
    "Era of Strife — 1v1 Matchup Matrix",
    fontsize=16,
    pad=20
)


# ============================================================
# ТЕКСТ ВНУТРИ ЯЧЕЕК
# ============================================================

for row_index in range(len(unit_ids)):

    for column_index in range(len(unit_ids)):

        if row_index == column_index:

            cell_text = "—"

        else:

            value = matrix_values[row_index][column_index]

            if value == 1:
                cell_text = "W"

            elif value == -1:
                cell_text = "L"

            else:
                cell_text = "D"

        ax.text(
            column_index,
            row_index,
            cell_text,
            ha="center",
            va="center",
            fontsize=9
        )


# ============================================================
# СЕТКА МЕЖДУ ЯЧЕЙКАМИ
# ============================================================

ax.set_xticks(
    [
        x - 0.5
        for x in range(1, len(unit_ids))
    ],
    minor=True
)

ax.set_yticks(
    [
        y - 0.5
        for y in range(1, len(unit_ids))
    ],
    minor=True
)

ax.grid(
    which="minor",
    linewidth=1
)

ax.tick_params(
    which="minor",
    bottom=False,
    left=False
)


# ============================================================
# COLORBAR
# ============================================================

colorbar = fig.colorbar(
    image,
    ax=ax,
    fraction=0.046,
    pad=0.04
)

colorbar.set_ticks(
    [-1, 0, 1]
)

colorbar.set_ticklabels(
    [
        "Loss",
        "Draw",
        "Win"
    ]
)


# ============================================================
# СОХРАНЕНИЕ MATCHUP MATRIX
# ============================================================

plt.tight_layout()


matchup_matrix_file = os.path.join(
    OUTPUT_DIR,
    "matchup_matrix.png"
)


plt.savefig(
    matchup_matrix_file,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "Matchup Matrix сохранена:",
    matchup_matrix_file
)


# ============================================================
# ГРАФИК №2
# COMBAT SCORE
# ============================================================

print()
print("=" * 70)
print("СОЗДАНИЕ ГРАФИКА COMBAT SCORE")
print("=" * 70)


sorted_statistics = sorted(
    unit_statistics,
    key=lambda unit: unit["Combat_Score"],
    reverse=True
)


combat_labels = []

combat_scores = []


for unit in sorted_statistics:

    combat_labels.append(
        unit["Unit_ID"]
        + "\n"
        + unit["Unit_Name"]
    )

    combat_scores.append(
        unit["Combat_Score"]
    )


fig, ax = plt.subplots(
    figsize=(15, 8)
)


bars = ax.bar(
    combat_labels,
    combat_scores
)


ax.set_title(
    "Era of Strife — Unit Combat Score",
    fontsize=16,
    pad=20
)


ax.set_xlabel(
    "Unit",
    fontsize=11
)


ax.set_ylabel(
    "Combat Score (%)",
    fontsize=11
)


ax.set_ylim(
    0,
    110
)


ax.tick_params(
    axis="x",
    rotation=45,
    labelsize=8
)


# ============================================================
# ЧИСЛА НАД СТОЛБЦАМИ
# ============================================================

for bar, score in zip(
    bars,
    combat_scores
):

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{score:.2f}%",
        ha="center",
        va="bottom",
        fontsize=8
    )


# Линия условного нейтрального уровня.
ax.axhline(
    y=50,
    linestyle="--",
    linewidth=1.5
)


plt.tight_layout()


combat_score_file = os.path.join(
    OUTPUT_DIR,
    "unit_combat_score.png"
)


plt.savefig(
    combat_score_file,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "Combat Score график сохранён:",
    combat_score_file
)


# ============================================================
# ГРАФИК №3
# WIN / LOSS / DRAW
# ============================================================

print()
print("=" * 70)
print("СОЗДАНИЕ ГРАФИКА WINS / LOSSES / DRAWS")
print("=" * 70)


wl_labels = []

wins = []
losses = []
draws = []


for unit in unit_statistics:

    wl_labels.append(
        unit["Unit_ID"]
    )

    wins.append(
        unit["Wins"]
    )

    losses.append(
        unit["Losses"]
    )

    draws.append(
        unit["Draws"]
    )


x_positions = list(
    range(len(wl_labels))
)


bar_width = 0.25


fig, ax = plt.subplots(
    figsize=(15, 8)
)


win_positions = [
    x - bar_width
    for x in x_positions
]

draw_positions = x_positions

loss_positions = [
    x + bar_width
    for x in x_positions
]


ax.bar(
    win_positions,
    wins,
    width=bar_width,
    label="Wins"
)


ax.bar(
    draw_positions,
    draws,
    width=bar_width,
    label="Draws"
)


ax.bar(
    loss_positions,
    losses,
    width=bar_width,
    label="Losses"
)


ax.set_xticks(
    x_positions
)

ax.set_xticklabels(
    wl_labels,
    rotation=45,
    ha="right"
)


ax.set_xlabel(
    "Unit",
    fontsize=11
)


ax.set_ylabel(
    "Number of Matchups",
    fontsize=11
)


ax.set_title(
    "Era of Strife — Wins, Draws and Losses by Unit",
    fontsize=16,
    pad=20
)


ax.legend()


plt.tight_layout()


win_loss_draw_file = os.path.join(
    OUTPUT_DIR,
    "unit_win_loss_draw.png"
)


plt.savefig(
    win_loss_draw_file,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "Win/Loss/Draw график сохранён:",
    win_loss_draw_file
)


# ============================================================
# ГРАФИК №4
# WIN RATE
# ============================================================

print()
print("=" * 70)
print("СОЗДАНИЕ ГРАФИКА WIN RATE")
print("=" * 70)


win_rate_statistics = sorted(
    unit_statistics,
    key=lambda unit: unit["Win_Rate"],
    reverse=True
)


win_rate_labels = []

win_rates = []


for unit in win_rate_statistics:

    win_rate_labels.append(
        unit["Unit_ID"]
        + "\n"
        + unit["Unit_Name"]
    )

    win_rates.append(
        unit["Win_Rate"]
    )


fig, ax = plt.subplots(
    figsize=(15, 8)
)


bars = ax.bar(
    win_rate_labels,
    win_rates
)


ax.set_title(
    "Era of Strife — Unit Win Rate",
    fontsize=16,
    pad=20
)


ax.set_xlabel(
    "Unit",
    fontsize=11
)


ax.set_ylabel(
    "Win Rate (%)",
    fontsize=11
)


ax.set_ylim(
    0,
    110
)


ax.tick_params(
    axis="x",
    rotation=45,
    labelsize=8
)


# ============================================================
# ЧИСЛА НАД СТОЛБЦАМИ WIN RATE
# ============================================================

for bar, win_rate in zip(
    bars,
    win_rates
):

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{win_rate:.2f}%",
        ha="center",
        va="bottom",
        fontsize=8
    )


# Условная линия 50%.
ax.axhline(
    y=50,
    linestyle="--",
    linewidth=1.5
)


plt.tight_layout()


win_rate_file = os.path.join(
    OUTPUT_DIR,
    "unit_win_rate.png"
)


plt.savefig(
    win_rate_file,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "Win Rate график сохранён:",
    win_rate_file
)


# ============================================================
# ИТОГ
# ============================================================

print()
print("=" * 70)
print("ВИЗУАЛИЗАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
print("=" * 70)

print(
    "Проанализировано матчапов:",
    len(matchups)
)

print(
    "Проанализировано юнитов:",
    len(unit_ids)
)

print(
    "Создано визуализаций:",
    4
)

print()
print("Созданные файлы:")

print(
    "1.",
    matchup_matrix_file
)

print(
    "2.",
    combat_score_file
)

print(
    "3.",
    win_loss_draw_file
)

print(
    "4.",
    win_rate_file
)