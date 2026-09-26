# Era of Strife — Mobile RTS Balance & META Analysis

**Era of Strife** — портфолио-проект по Game Design, Balance Design и Data Analysis для концепта мобильной RTS.

Проект демонстрирует полный цикл работы с игровым балансом: от проектирования фракций, юнитов и способностей до структурирования данных, Python-анализа, combat simulation, проверки Balance Hypotheses и проведения последовательных Balance Iterations.

---

## О проекте

В Era of Strife разработаны:

- **3 фракции**
- **12 юнитов**
- **4 боевые роли**
- **12 уникальных способностей**
- **66 уникальных pairwise matchup**
- Faction Identity и Unit Identity
- Interaction Matrix
- Balance Risks
- deterministic 1v1 combat simulation
- автоматический Balance Analysis
- Before/After comparison
- Reproducibility Check
- Sensitivity Analysis
- Threshold Refinement
- несколько последовательных Balance Iterations

Основной workflow проекта:

**Game Design → Structured Data → Validation → Combat Simulation → Analysis → Balance Hypothesis → Iteration → Comparison → Design Decision**

---

## Фракции

### Undead

**Identity:** Attrition

Основные особенности:

- Recovery
- Debuffs
- Sustained Pressure

Основной игровой акцент:

**Resource & Army Management**

---

### Forest & Dark Elves

**Identity:** Precision

Основные особенности:

- High Mobility
- Long Range
- High Unit Value

Основной игровой акцент:

**Positioning & Micro**

---

### Horde

**Identity:** Brute Force / Pressure

Основные особенности:

- High HP
- Strong Melee
- Crowd Control

Основной игровой акцент:

**Engagement Timing**

---

## Unit Roster

| Faction | Infantry | Tank | Ranged | Support |
|---|---|---|---|---|
| Undead | Skeleton Swordsman | Bone Dragon | Spear Devil | Witch |
| Forest & Dark Elves | Elven Swordsman | Great Forest Bear | Elven Mage | Elven Scholar |
| Horde | Blade Goblin | Stone Ogre | Orc Thrower | Boneclub Troll |

Каждый юнит имеет собственную Unit Identity, Strengths, Weaknesses и уникальную способность.

---

## Ключевые игровые взаимодействия

В проекте отдельно анализируются взаимодействия между способностями и ролями.

Примеры:

- **Reassemble + Death Feast**
- **Cursed Spear + Curse**
- **Guardian Roar + Arcane Shield**
- **Evasive Step vs Knife Barrage**
- **Bone Smash vs Focused Bolt**
- **Curse vs Blood Rush**
- **Stone Skin vs Focused Bolt**

Для систематизации этих взаимодействий используется отдельная **Interaction Matrix**.

---

## Data-Driven Balance

Game Design проекта переводится в структурированные данные.

Основные datasets содержат:

- параметры юнитов;
- параметры способностей;
- Balance Risks;
- Interaction Matrix;
- Combat Scenarios;
- Balance Tests.

Исходные данные отделены от generated results, что позволяет сохранять baseline и сравнивать разные Balance Iterations.

---

## Combat Simulation

Для первоначального количественного анализа разработана deterministic 1v1 combat simulation.

Базовая модель учитывает:

- HP
- Damage
- Attack Interval
- независимое время атак
- одновременные атаки
- Win / Loss / Draw
- Combat Time

Для 12 юнитов анализируется:

**C(12, 2) = 66**

уникальных pairwise matchup.

Текущая simulation намеренно упрощена и используется для controlled numerical experiments, а не как модель реального PvP Win Rate.

---

## Balance Philosophy

Цель проекта — не привести каждый юнит к **50%**.

Era of Strife использует асимметричные фракции, разные роли, counters и synergy.

Поэтому 50% используется как:

**analytical reference point**

а не как обязательный Balance Target.

Основной вопрос анализа:

> Соответствует ли фактическое поведение юнита его Design Intent?

---

## Balance Case Study — Stone Ogre

Одним из основных Balance Cases проекта стал:

**HOR_02 — Stone Ogre**

Unit Identity:

**Heavy Frontline Tank**

Основная сильная сторона:

**Very High Durability**

Baseline analysis показал необходимость уменьшить его offensive pressure.

При этом простое уменьшение HP могло бы ослабить основную идентичность юнита.

Поэтому основным Balance Lever был выбран:

**Damage**

---

## Stone Ogre Balance Iterations

### Baseline

**Damage: 96.00**

**DPS: 60.00**

---

### Iteration 01

**Damage: 96.00 → 91.20**

**DPS: 60.00 → 57.00**

Изменение Damage:

**-5%**

---

### Iteration 02

**Damage: 91.20 → 86.64**

**DPS: 57.00 → 54.15**

**HP: 1760 → 1760**

Изменение Damage:

**-5%**

---

### Cumulative Result

Полная последовательность:

**96.00 → 91.20 → 86.64**

Cumulative Damage Reduction:

**-9.75%**

При этом высокая Durability Stone Ogre была сохранена.

---

## Iteration 02 Result

После Iteration 02:

**Stone Ogre Combat Score**

**95.45 → 90.91**

**Distance From 50**

**45.45 → 40.91**

Количество Changed Matchups:

**1**

Direct Changed Matchups:

**1**

Indirect Changed Matchups:

**0**

---

## Changed Matchup

Единственный Changed Matchup Iteration 02:

**Great Forest Bear vs Stone Ogre**

Before:

**Stone Ogre Win**

After:

**Draw**

Combat Time:

**28.8 sec → 30.4 sec**

Изменение:

**+1.6 sec**

Это соответствует исходной Balance Hypothesis: уменьшить offensive pressure Stone Ogre, сохранив его Tank Durability.

---

## Current Balance Decision

Текущий статус Iteration 02:

**Promising Candidate for Further Validation**

Iteration 02 не рассматривается как Final Production Balance Patch.

Следующий этап должен проверять кандидата в более сложной модели с учётом способностей, Army Composition и других RTS-механик.

---

## Reproducibility

Для проверки deterministic behavior Iteration 01 была повторена:

**5 раз**

Каждый запуск содержал:

**66 matchup**

Итого:

**330 matchup records**

Результат:

| Metric | Result |
|---|---|
| Runs | 5 |
| Matchups Per Run | 66 |
| Byte Identical Files | Yes |
| Unstable Matchups | 0 |
| Changed Row Comparisons | 0 |
| Changed Field Comparisons | 0 |
| Status | Reproducible |

При этом в проекте отдельно учитывается важный принцип:

**Reproducibility ≠ Correctness**

Стабильный analytical pipeline всё равно требует проверки логики, Data Lineage и исходных предположений.

---

## Sensitivity & Threshold Analysis

Для Stone Ogre дополнительно проводился Sensitivity Analysis.

Его задача заключалась в исследовании того, насколько matchup outcomes чувствительны к изменению параметров.

Дополнительно использовался Threshold Refinement для исследования областей перехода:

**Win → Draw → Loss**

Это позволило лучше понять, почему даже небольшие Balance Changes могут изменять конкретные matchup.

---

## Source Data Integrity

Экспериментальные Balance Iterations не должны незаметно изменять baseline.

Для `data/unit_balance.csv` дополнительно проверялась целостность исходных данных.

SHA-256:

`83a937076d861ffe9f5721e9eac6c2a3cd4a08d120d569b8c041cf4722098499`

После Iteration 02:

**Source unchanged: Yes**

---

## Структура проекта

```text
era-of-strife-meta-balance/
│
├── analysis/
│   ├── combat_engine.py
│   ├── 01_validate_data.py
│   ├── 02_explore_balance.py
│   ├── 03_analyze_abilities.py
│   ├── ...
│   └── results/
│
├── data/
│   ├── unit_balance.csv
│   ├── ability_balance.csv
│   ├── balance_risks.csv
│   ├── interaction_matrix.csv
│   ├── balance_tests.csv
│   └── combat_scenarios.csv
│
├── docs/
│   ├── 01_game_design.md
│   ├── 02_balance_methodology.md
│   ├── 03_balance_iterations.md
│   └── 04_final_findings.md
│
├── images/
│
├── spreadsheets/
│
└── README.md