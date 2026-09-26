import csv


# ============================================================
# НАСТРОЙКИ
# ============================================================

MATCHUP_FILE = "analysis/results/matchup_statistics.csv"

OUTPUT_FILE = "analysis/results/matchup_analysis.csv"


# ============================================================
# ЗАГРУЗКА РЕЗУЛЬТАТОВ МАТЧАПОВ
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


print("=" * 60)
print("АНАЛИЗ МАТЧАПОВ")
print("=" * 60)
print("Файл:", MATCHUP_FILE)
print("Количество матчапов:", len(matchups))


# ============================================================
# ПРОВЕРКА КОЛИЧЕСТВА МАТЧАПОВ
# ============================================================

EXPECTED_UNITS = 12

expected_matchups = (
    EXPECTED_UNITS
    * (EXPECTED_UNITS - 1)
    // 2
)

print()
print("=" * 60)
print("ПРОВЕРКА КОЛИЧЕСТВА МАТЧАПОВ")
print("=" * 60)

print("Ожидаемое количество:", expected_matchups)
print("Фактическое количество:", len(matchups))

if len(matchups) == expected_matchups:
    print("OK: количество матчапов корректно.")
else:
    print("ВНИМАНИЕ: количество матчапов отличается от ожидаемого.")


# ============================================================
# СОЗДАНИЕ СТРУКТУРЫ ДЛЯ СТАТИСТИКИ ЮНИТОВ
# ============================================================

unit_matchups = {}


def create_unit_record(unit_id, unit_name, role):
    if unit_id not in unit_matchups:
        unit_matchups[unit_id] = {
            "Unit_Name": unit_name,
            "Role": role,
            "Wins_Against": [],
            "Losses_Against": [],
            "Draws_Against": []
        }


# ============================================================
# РЕГИСТРАЦИЯ ВСЕХ ЮНИТОВ
# ============================================================

for matchup in matchups:

    create_unit_record(
        matchup["Unit_A_ID"],
        matchup["Unit_A_Name"],
        matchup["Unit_A_Role"]
    )

    create_unit_record(
        matchup["Unit_B_ID"],
        matchup["Unit_B_Name"],
        matchup["Unit_B_Role"]
    )


print()
print("=" * 60)
print("ЗАРЕГИСТРИРОВАННЫЕ ЮНИТЫ")
print("=" * 60)

for unit_id, data in unit_matchups.items():
    print(
        unit_id,
        "|",
        data["Unit_Name"],
        "| Role:",
        data["Role"]
    )

print("Количество уникальных юнитов:", len(unit_matchups))


# ============================================================
# ЗАПОЛНЕНИЕ ПОБЕД, ПОРАЖЕНИЙ И НИЧЬИХ
# ============================================================

for matchup in matchups:

    unit_a_id = matchup["Unit_A_ID"]
    unit_b_id = matchup["Unit_B_ID"]

    unit_a_name = matchup["Unit_A_Name"]
    unit_b_name = matchup["Unit_B_Name"]

    unit_a_role = matchup["Unit_A_Role"]
    unit_b_role = matchup["Unit_B_Role"]

    result = matchup["Result"]
    winner = matchup["Winner"]
    loser = matchup["Loser"]

    if result == "Draw":

        unit_matchups[unit_a_id]["Draws_Against"].append({
            "Unit_ID": unit_b_id,
            "Unit_Name": unit_b_name,
            "Role": unit_b_role
        })

        unit_matchups[unit_b_id]["Draws_Against"].append({
            "Unit_ID": unit_a_id,
            "Unit_Name": unit_a_name,
            "Role": unit_a_role
        })

    else:

        if winner == unit_a_name:

            unit_matchups[unit_a_id]["Wins_Against"].append({
                "Unit_ID": unit_b_id,
                "Unit_Name": unit_b_name,
                "Role": unit_b_role
            })

            unit_matchups[unit_b_id]["Losses_Against"].append({
                "Unit_ID": unit_a_id,
                "Unit_Name": unit_a_name,
                "Role": unit_a_role
            })

        elif winner == unit_b_name:

            unit_matchups[unit_b_id]["Wins_Against"].append({
                "Unit_ID": unit_a_id,
                "Unit_Name": unit_a_name,
                "Role": unit_a_role
            })

            unit_matchups[unit_a_id]["Losses_Against"].append({
                "Unit_ID": unit_b_id,
                "Unit_Name": unit_b_name,
                "Role": unit_b_role
            })

        else:
            print(
                "ВНИМАНИЕ: не удалось определить победителя:",
                unit_a_id,
                "vs",
                unit_b_id
            )


# ============================================================
# РАСЧЁТ АГРЕГИРОВАННОЙ СТАТИСТИКИ
# ============================================================

for unit_id, data in unit_matchups.items():

    wins = len(data["Wins_Against"])
    losses = len(data["Losses_Against"])
    draws = len(data["Draws_Against"])

    battles = wins + losses + draws

    if battles > 0:

        win_rate = wins / battles * 100

        draw_rate = draws / battles * 100

        combat_score = (
            wins
            + 0.5 * draws
        ) / battles * 100

    else:

        win_rate = 0.0
        draw_rate = 0.0
        combat_score = 0.0

    data["Battles"] = battles
    data["Wins"] = wins
    data["Losses"] = losses
    data["Draws"] = draws

    data["Win_Rate"] = win_rate
    data["Draw_Rate"] = draw_rate
    data["Combat_Score"] = combat_score


# ============================================================
# ПРОВЕРКА ЦЕЛОСТНОСТИ СТАТИСТИКИ
# ============================================================

print()
print("=" * 60)
print("ПРОВЕРКА СТАТИСТИКИ")
print("=" * 60)

statistics_ok = True

expected_battles_per_unit = EXPECTED_UNITS - 1

for unit_id, data in unit_matchups.items():

    if data["Battles"] != expected_battles_per_unit:

        statistics_ok = False

        print(
            "ОШИБКА:",
            unit_id,
            data["Unit_Name"],
            "| Battles:",
            data["Battles"],
            "| Expected:",
            expected_battles_per_unit
        )


if statistics_ok:
    print(
        "OK: каждый юнит имеет",
        expected_battles_per_unit,
        "матчапов."
    )


# ============================================================
# ВЫВОД ПОДРОБНОЙ СТАТИСТИКИ
# ============================================================

print()
print("=" * 60)
print("ПОДРОБНЫЙ АНАЛИЗ ЮНИТОВ")
print("=" * 60)


for unit_id, data in unit_matchups.items():

    print()
    print("-" * 60)

    print(
        unit_id,
        "|",
        data["Unit_Name"],
        "|",
        data["Role"]
    )

    print("-" * 60)

    print("Battles:", data["Battles"])
    print("Wins:", data["Wins"])
    print("Losses:", data["Losses"])
    print("Draws:", data["Draws"])

    print(
        "Win Rate:",
        round(data["Win_Rate"], 2),
        "%"
    )

    print(
        "Draw Rate:",
        round(data["Draw_Rate"], 2),
        "%"
    )

    print(
        "Combat Score:",
        round(data["Combat_Score"], 2),
        "%"
    )


    print()
    print("Wins against:")

    if data["Wins_Against"]:

        for opponent in data["Wins_Against"]:
            print(
                "  -",
                opponent["Unit_ID"],
                "|",
                opponent["Unit_Name"],
                "|",
                opponent["Role"]
            )

    else:
        print("  None")


    print()
    print("Losses against:")

    if data["Losses_Against"]:

        for opponent in data["Losses_Against"]:
            print(
                "  -",
                opponent["Unit_ID"],
                "|",
                opponent["Unit_Name"],
                "|",
                opponent["Role"]
            )

    else:
        print("  None")


    print()
    print("Draws against:")

    if data["Draws_Against"]:

        for opponent in data["Draws_Against"]:
            print(
                "  -",
                opponent["Unit_ID"],
                "|",
                opponent["Unit_Name"],
                "|",
                opponent["Role"]
            )

    else:
        print("  None")


# ============================================================
# АНАЛИЗ РЕЗУЛЬТАТОВ ПРОТИВ РОЛЕЙ
# ============================================================

roles = [
    "Infantry",
    "Tank",
    "Ranged",
    "Support"
]


for unit_id, data in unit_matchups.items():

    role_statistics = {}

    for role in roles:

        role_statistics[role] = {
            "Battles": 0,
            "Wins": 0,
            "Losses": 0,
            "Draws": 0
        }


    for opponent in data["Wins_Against"]:

        opponent_role = opponent["Role"]

        role_statistics[opponent_role]["Battles"] += 1
        role_statistics[opponent_role]["Wins"] += 1


    for opponent in data["Losses_Against"]:

        opponent_role = opponent["Role"]

        role_statistics[opponent_role]["Battles"] += 1
        role_statistics[opponent_role]["Losses"] += 1


    for opponent in data["Draws_Against"]:

        opponent_role = opponent["Role"]

        role_statistics[opponent_role]["Battles"] += 1
        role_statistics[opponent_role]["Draws"] += 1


    data["Role_Statistics"] = role_statistics


# ============================================================
# ВЫВОД СТАТИСТИКИ ПРОТИВ РОЛЕЙ
# ============================================================

print()
print("=" * 60)
print("РЕЗУЛЬТАТЫ ПРОТИВ РОЛЕЙ")
print("=" * 60)


for unit_id, data in unit_matchups.items():

    print()
    print(
        unit_id,
        "|",
        data["Unit_Name"]
    )

    for role in roles:

        role_data = data["Role_Statistics"][role]

        battles = role_data["Battles"]

        if battles > 0:

            role_score = (
                role_data["Wins"]
                + 0.5 * role_data["Draws"]
            ) / battles * 100

        else:
            role_score = 0.0

        role_data["Combat_Score"] = role_score

        print(
            "  vs",
            role,
            "| Battles:",
            role_data["Battles"],
            "| Wins:",
            role_data["Wins"],
            "| Losses:",
            role_data["Losses"],
            "| Draws:",
            role_data["Draws"],
            "| Score:",
            round(role_score, 2),
            "%"
        )


# ============================================================
# ПОИСК ПОТЕНЦИАЛЬНО ПРОБЛЕМНЫХ МАТЧАПОВ
# ============================================================

print()
print("=" * 60)
print("ПОТЕНЦИАЛЬНЫЕ ОТКЛОНЕНИЯ")
print("=" * 60)


HIGH_SCORE_THRESHOLD = 80.0
LOW_SCORE_THRESHOLD = 20.0

deviations = []


for unit_id, data in unit_matchups.items():

    combat_score = data["Combat_Score"]

    if combat_score >= HIGH_SCORE_THRESHOLD:

        deviations.append({
            "Unit_ID": unit_id,
            "Unit_Name": data["Unit_Name"],
            "Role": data["Role"],
            "Combat_Score": combat_score,
            "Flag": "High Combat Score"
        })

    elif combat_score <= LOW_SCORE_THRESHOLD:

        deviations.append({
            "Unit_ID": unit_id,
            "Unit_Name": data["Unit_Name"],
            "Role": data["Role"],
            "Combat_Score": combat_score,
            "Flag": "Low Combat Score"
        })


if deviations:

    for deviation in deviations:

        print(
            deviation["Unit_ID"],
            "|",
            deviation["Unit_Name"],
            "| Role:",
            deviation["Role"],
            "| Combat Score:",
            round(deviation["Combat_Score"], 2),
            "%",
            "| Flag:",
            deviation["Flag"]
        )

else:

    print("Потенциальные отклонения не обнаружены.")


# ============================================================
# ПОДГОТОВКА РЕЗУЛЬТАТОВ ДЛЯ CSV
# ============================================================

output_rows = []


for unit_id, data in unit_matchups.items():

    wins_against = "; ".join(
        opponent["Unit_ID"]
        for opponent in data["Wins_Against"]
    )

    losses_against = "; ".join(
        opponent["Unit_ID"]
        for opponent in data["Losses_Against"]
    )

    draws_against = "; ".join(
        opponent["Unit_ID"]
        for opponent in data["Draws_Against"]
    )


    output_rows.append({
        "Unit_ID": unit_id,
        "Unit_Name": data["Unit_Name"],
        "Role": data["Role"],
        "Battles": data["Battles"],
        "Wins": data["Wins"],
        "Losses": data["Losses"],
        "Draws": data["Draws"],
        "Win_Rate": round(data["Win_Rate"], 2),
        "Draw_Rate": round(data["Draw_Rate"], 2),
        "Combat_Score": round(data["Combat_Score"], 2),
        "Wins_Against": wins_against,
        "Losses_Against": losses_against,
        "Draws_Against": draws_against
    })


# ============================================================
# СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
# ============================================================

fieldnames = [
    "Unit_ID",
    "Unit_Name",
    "Role",
    "Battles",
    "Wins",
    "Losses",
    "Draws",
    "Win_Rate",
    "Draw_Rate",
    "Combat_Score",
    "Wins_Against",
    "Losses_Against",
    "Draws_Against"
]


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(output_rows)


print()
print("=" * 60)
print("АНАЛИЗ МАТЧАПОВ ЗАВЕРШЁН")
print("=" * 60)

print("Исходных матчапов:", len(matchups))
print("Проанализировано юнитов:", len(unit_matchups))
print("Обнаружено отклонений:", len(deviations))
print("Результат сохранён:", OUTPUT_FILE)
# ============================================================
# 6.2. АНАЛИЗ ДОМИНИРУЮЩИХ И ПРОБЛЕМНЫХ МАТЧАПОВ
# ============================================================

print()
print("=" * 60)
print("6.2. АНАЛИЗ ДОМИНИРУЮЩИХ И ПРОБЛЕМНЫХ МАТЧАПОВ")
print("=" * 60)

# ------------------------------------------------------------
# ПОИСК ДОМИНИРУЮЩИХ ЮНИТОВ
# ------------------------------------------------------------

DOMINANT_COMBAT_SCORE = 75.0

dominant_units = []

for unit_id, data in unit_matchups.items():

    combat_score = data["Combat_Score"]

    if combat_score >= DOMINANT_COMBAT_SCORE:

        dominant_units.append({
            "Unit_ID": unit_id,
            "Unit_Name": data["Unit_Name"],
            "Role": data["Role"],
            "Combat_Score": combat_score,
            "Wins": data["Wins"],
            "Losses": data["Losses"],
            "Draws": data["Draws"],
            "Wins_Against": data["Wins_Against"]
        })

print()
print("-" * 60)
print("ДОМИНИРУЮЩИЕ ЮНИТЫ")
print("-" * 60)

if dominant_units:

    for unit in dominant_units:

        print(
            unit["Unit_ID"],
            "|",
            unit["Unit_Name"],
            "| Role:",
            unit["Role"],
            "| Combat Score:",
            round(unit["Combat_Score"], 2),
            "%",
            "| W-L-D:",
            f'{unit["Wins"]}-{unit["Losses"]}-{unit["Draws"]}'
        )

else:

    print("Доминирующие юниты не обнаружены.")
  # ------------------------------------------------------------
# ПОИСК ЮНИТОВ С НИЗКОЙ ЭФФЕКТИВНОСТЬЮ
# ------------------------------------------------------------

LOW_COMBAT_SCORE = 30.0

weak_units = []
support_units_for_team_analysis = []

for unit_id, data in unit_matchups.items():

    combat_score = data["Combat_Score"]
    role = data["Role"]

    if role != "Support" and combat_score <= LOW_COMBAT_SCORE:

        weak_units.append({
            "Unit_ID": unit_id,
            "Unit_Name": data["Unit_Name"],
            "Role": role,
            "Combat_Score": combat_score,
            "Wins": data["Wins"],
            "Losses": data["Losses"],
            "Draws": data["Draws"],
            "Losses_Against": data["Losses_Against"]
        })

    elif role == "Support" and combat_score <= LOW_COMBAT_SCORE:

        support_units_for_team_analysis.append({
            "Unit_ID": unit_id,
            "Unit_Name": data["Unit_Name"],
            "Role": role,
            "Combat_Score": combat_score,
            "Wins": data["Wins"],
            "Losses": data["Losses"],
            "Draws": data["Draws"]
        })


print()
print("-" * 60)
print("ЮНИТЫ С НИЗКОЙ 1V1-ЭФФЕКТИВНОСТЬЮ")
print("-" * 60)

if weak_units:

    for unit in weak_units:

        print(
            unit["Unit_ID"],
            "|",
            unit["Unit_Name"],
            "| Role:",
            unit["Role"],
            "| Combat Score:",
            round(unit["Combat_Score"], 2),
            "%",
            "| W-L-D:",
            f'{unit["Wins"]}-{unit["Losses"]}-{unit["Draws"]}'
        )

else:

    print("Проблемные боевые юниты не обнаружены.")


print()
print("-" * 60)
print("SUPPORT-ЮНИТЫ, ТРЕБУЮЩИЕ КОМАНДНОЙ ОЦЕНКИ")
print("-" * 60)

if support_units_for_team_analysis:

    for unit in support_units_for_team_analysis:

        print(
            unit["Unit_ID"],
            "|",
            unit["Unit_Name"],
            "| Combat Score:",
            round(unit["Combat_Score"], 2),
            "%",
            "| W-L-D:",
            f'{unit["Wins"]}-{unit["Losses"]}-{unit["Draws"]}',
            "| Status: Team Analysis Required"
        )

else:

    print("Support-юниты ниже установленного порога не обнаружены.")
# ------------------------------------------------------------
# ДЕТАЛЬНЫЙ АНАЛИЗ МАТЧАПОВ
# ------------------------------------------------------------

print()
print("=" * 60)
print("ДЕТАЛЬНЫЙ MATCHUP PROFILE")
print("=" * 60)

for unit_id, data in unit_matchups.items():

    print()
    print("-" * 60)

    print(
        unit_id,
        "|",
        data["Unit_Name"],
        "| Role:",
        data["Role"]
    )

    print("-" * 60)

    # --------------------------------------------------------
    # ОСНОВНАЯ СТАТИСТИКА ЮНИТА
    # --------------------------------------------------------

    battles = data["Battles"]
    wins = data["Wins"]
    losses = data["Losses"]
    draws = data["Draws"]

    if battles > 0:

        win_percentage = wins / battles * 100
        loss_percentage = losses / battles * 100
        draw_percentage = draws / battles * 100

    else:

        win_percentage = 0.0
        loss_percentage = 0.0
        draw_percentage = 0.0

    print(
        "Battles:",
        battles,
        "| Wins:",
        wins,
        "| Losses:",
        losses,
        "| Draws:",
        draws
    )

    print(
        "Win %:",
        round(win_percentage, 2),
        "| Loss %:",
        round(loss_percentage, 2),
        "| Draw %:",
        round(draw_percentage, 2)
    )

    print(
        "Combat Score:",
        round(data["Combat_Score"], 2),
        "%"
    )

    # --------------------------------------------------------
    # ПРОТИВ КОГО ЮНИТ ПОБЕЖДАЕТ
    # --------------------------------------------------------

    print()

    if data["Wins_Against"]:

        wins_against_text = []

        for opponent in data["Wins_Against"]:

            wins_against_text.append(
                opponent["Unit_ID"]
                + " ("
                + opponent["Unit_Name"]
                + ")"
            )

        print(
            "Wins Against:",
            ", ".join(wins_against_text)
        )

    else:

        print("Wins Against: None")

    # --------------------------------------------------------
    # ПРОТИВ КОГО ЮНИТ ПРОИГРЫВАЕТ
    # --------------------------------------------------------

    if data["Losses_Against"]:

        losses_against_text = []

        for opponent in data["Losses_Against"]:

            losses_against_text.append(
                opponent["Unit_ID"]
                + " ("
                + opponent["Unit_Name"]
                + ")"
            )

        print(
            "Losses Against:",
            ", ".join(losses_against_text)
        )

    else:

        print("Losses Against: None")

    # --------------------------------------------------------
    # С КЕМ ЮНИТ ИГРАЕТ ВНИЧЬЮ
    # --------------------------------------------------------

    if data["Draws_Against"]:

        draws_against_text = []

        for opponent in data["Draws_Against"]:

            draws_against_text.append(
                opponent["Unit_ID"]
                + " ("
                + opponent["Unit_Name"]
                + ")"
            )

        print(
            "Draws Against:",
            ", ".join(draws_against_text)
        )

    else:

        print("Draws Against: None")


# ============================================================
# ИТОГ ЭТАПА 6.2
# ============================================================

print()
print("=" * 60)
print("ЭТАП 6.2 ЗАВЕРШЁН")
print("=" * 60)

print(
    "Всего проанализировано юнитов:",
    len(unit_matchups)
)

print(
    "Доминирующих юнитов:",
    len(dominant_units)
)

print(
    "Боевых юнитов с низкой эффективностью:",
    len(weak_units)
)

print(
    "Support-юнитов для командного анализа:",
    len(support_units_for_team_analysis)
)

print()
print(
    "Детальный анализ матчапов успешно завершён."
)