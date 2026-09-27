from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# ============================================================
# Era of Strife — portfolio visualization
# Stone Ogre balance case study
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "results" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "stone_ogre_balance_case.png"


# ============================================================
# Confirmed analysis results
# ============================================================

unit_1 = "Great Forest Bear"
unit_2 = "Stone Ogre"

damage_before = 91.20
damage_after = 86.64

combat_time_before = 28.8
combat_time_after = 30.4

changed_matchups = 1
direct_changed_matchups = 1
indirect_changed_matchups = 0

initial_win_rate = 100.0


# ============================================================
# Calculations
# ============================================================

damage_change_percent = (
    (damage_after - damage_before)
    / damage_before
    * 100
)

combat_time_change = combat_time_after - combat_time_before


# ============================================================
# Figure
# ============================================================

fig = plt.figure(figsize=(16, 10))

ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")


# ============================================================
# Helpers
# ============================================================

def add_card(x, y, width, height, title=None):
    """Create a simple rounded information card."""

    card = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=1.2,
        edgecolor="0.75",
        facecolor="0.97",
    )

    ax.add_patch(card)

    if title:
        ax.text(
            x + width / 2,
            y + height - 0.035,
            title,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )


def add_arrow(x1, y1, x2, y2):
    """Draw an arrow between two points."""

    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops={
            "arrowstyle": "->",
            "linewidth": 2,
        },
    )


# ============================================================
# Header
# ============================================================

ax.text(
    0.5,
    0.955,
    "ERA OF STRIFE",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
)

ax.text(
    0.5,
    0.915,
    "Кейс балансировки — Stone Ogre",
    ha="center",
    va="center",
    fontsize=25,
    fontweight="bold",
)

ax.text(
    0.5,
    0.875,
    "Контролируемая итерация баланса на основе анализа 1v1-матчапов",
    ha="center",
    va="center",
    fontsize=12,
)


# ============================================================
# Step 1 — Problem
# ============================================================

add_card(
    0.08,
    0.675,
    0.22,
    0.145,
    "1. ОБНАРУЖЕННАЯ ПРОБЛЕМА",
)

ax.text(
    0.19,
    0.735,
    "Stone Ogre",
    ha="center",
    fontsize=15,
    fontweight="bold",
)

ax.text(
    0.19,
    0.700,
    f"{initial_win_rate:.0f}% Win Rate*",
    ha="center",
    fontsize=18,
    fontweight="bold",
)


# ============================================================
# Step 2 — Hypothesis
# ============================================================

add_card(
    0.39,
    0.675,
    0.22,
    0.145,
    "2. ГИПОТЕЗА",
)

ax.text(
    0.50,
    0.735,
    "Снизить Damage",
    ha="center",
    fontsize=16,
    fontweight="bold",
)

ax.text(
    0.50,
    0.700,
    "Stone Ogre",
    ha="center",
    fontsize=13,
)


# ============================================================
# Step 3 — Controlled change
# ============================================================

add_card(
    0.70,
    0.675,
    0.22,
    0.145,
    "3. ITERATION 2",
)

ax.text(
    0.81,
    0.746,
    f"{damage_before:.2f}  →  {damage_after:.2f}",
    ha="center",
    fontsize=17,
    fontweight="bold",
)

ax.text(
    0.81,
    0.700,
    f"{damage_change_percent:.1f}% Damage",
    ha="center",
    fontsize=17,
    fontweight="bold",
)


# Arrows between the three steps
add_arrow(0.31, 0.747, 0.38, 0.747)
add_arrow(0.62, 0.747, 0.69, 0.747)


# ============================================================
# Matchup result section
# ============================================================

ax.text(
    0.5,
    0.615,
    "ИЗМЕНЕНИЕ МАТЧАПА",
    ha="center",
    fontsize=13,
    fontweight="bold",
)

ax.text(
    0.5,
    0.580,
    f"{unit_1}  vs  {unit_2}",
    ha="center",
    fontsize=17,
    fontweight="bold",
)


# BEFORE card
add_card(
    0.12,
    0.365,
    0.30,
    0.165,
    "ДО",
)

ax.text(
    0.27,
    0.455,
    "STONE OGRE",
    ha="center",
    fontsize=15,
    fontweight="bold",
)

ax.text(
    0.27,
    0.415,
    "WIN",
    ha="center",
    fontsize=23,
    fontweight="bold",
)

ax.text(
    0.27,
    0.382,
    f"{combat_time_before:.1f} с",
    ha="center",
    fontsize=12,
)


# Arrow
ax.text(
    0.50,
    0.445,
    "→",
    ha="center",
    va="center",
    fontsize=38,
    fontweight="bold",
)


# AFTER card
add_card(
    0.58,
    0.365,
    0.30,
    0.165,
    "ПОСЛЕ",
)

ax.text(
    0.73,
    0.455,
    "DRAW",
    ha="center",
    fontsize=23,
    fontweight="bold",
)

ax.text(
    0.73,
    0.410,
    f"{combat_time_after:.1f} с",
    ha="center",
    fontsize=14,
)

ax.text(
    0.73,
    0.380,
    f"+{combat_time_change:.1f} с",
    ha="center",
    fontsize=11,
)


# ============================================================
# Impact metrics
# ============================================================

ax.text(
    0.5,
    0.315,
    "ВЛИЯНИЕ НА СИСТЕМУ",
    ha="center",
    fontsize=13,
    fontweight="bold",
)


# Direct changes
add_card(
    0.18,
    0.185,
    0.26,
    0.095,
)

ax.text(
    0.31,
    0.240,
    str(direct_changed_matchups),
    ha="center",
    fontsize=25,
    fontweight="bold",
)

ax.text(
    0.31,
    0.205,
    "прямое изменение матчапа",
    ha="center",
    fontsize=11,
)


# Indirect changes
add_card(
    0.56,
    0.185,
    0.26,
    0.095,
)

ax.text(
    0.69,
    0.240,
    str(indirect_changed_matchups),
    ha="center",
    fontsize=25,
    fontweight="bold",
)

ax.text(
    0.69,
    0.205,
    "косвенных изменений",
    ha="center",
    fontsize=11,
)


# ============================================================
# Conclusion
# ============================================================

ax.text(
    0.5,
    0.125,
    "ВЫВОД",
    ha="center",
    fontsize=12,
    fontweight="bold",
)

ax.text(
    0.5,
    0.087,
    (
        "Точечное снижение Damage на 5% изменило один прямой матчап: "
        "победа Stone Ogre сменилась ничьей."
    ),
    ha="center",
    fontsize=11.5,
)

ax.text(
    0.5,
    0.058,
    (
        "Косвенных изменений других матчапов между Iteration 1 и Iteration 2 "
        "не зафиксировано."
    ),
    ha="center",
    fontsize=11.5,
)


# ============================================================
# Footnote
# ============================================================

ax.text(
    0.5,
    0.020,
    (
        "* 100% Win Rate относится к исходной 1v1-модели "
        "и используется как диагностический сигнал, "
        "а не как оценка полной игровой эффективности юнита."
    ),
    ha="center",
    fontsize=8.5,
    style="italic",
)


# ============================================================
# Save
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=200,
    bbox_inches="tight",
    pad_inches=0.15,
)

plt.close()

print(f"Visualization saved to: {OUTPUT_FILE}")