# Era of Strife — Итоговые выводы

## 1. Общий итог проекта

**Era of Strife** — портфолио-проект по Game Design, Balance Design и Data Analysis для концепта мобильной RTS.

В рамках проекта была создана игровая и аналитическая система, включающая:

- 3 фракции;
- 12 юнитов;
- 4 основные боевые роли;
- индивидуальные способности юнитов;
- Faction Identity;
- Unit Identity;
- Interaction Matrix;
- Balance Risks;
- структурированные balance-данные;
- Python-валидацию данных;
- deterministic combat simulation;
- 66 уникальных pairwise matchup;
- автоматический анализ результатов;
- Balance Iterations;
- Before/After comparison;
- Reproducibility Check;
- Impact Analysis;
- diagnostics;
- Sensitivity Analysis;
- Threshold Refinement;
- сравнение нескольких Balance Iterations.

Главный результат проекта заключается не только в получении конкретных чисел.

Была построена последовательная система работы:

**Game Design → Structured Data → Validation → Simulation → Analysis → Balance Hypothesis → Controlled Change → Re-Simulation → Comparison → Interpretation**

---

# 2. Основной принцип Balance Design

Один из главных выводов проекта:

> Баланс не означает, что каждый юнит должен иметь одинаковые характеристики или одинаково хорошо сражаться против каждого противника.

Era of Strife строится вокруг асимметричного дизайна.

Фракции имеют разные:

- Strengths;
- Weaknesses;
- способы ведения боя;
- Unit Roles;
- способности;
- counters;
- synergy.

Поэтому значение:

**50%**

используется как аналитический reference point, а не как обязательная конечная цель каждого юнита.

---

# 3. Сохранение Faction Identity

В проекте были сформированы три разные игровые идентичности.

### Undead

**Attrition**

Основные особенности:

- Recovery;
- Debuffs;
- Sustained Pressure.

Основной акцент игрока:

**Resource & Army Management**

---

### Forest & Dark Elves

**Precision**

Основные особенности:

- High Mobility;
- Long Range;
- High Unit Value.

Основной акцент игрока:

**Positioning & Micro**

---

### Horde

**Brute Force / Pressure**

Основные особенности:

- High HP;
- Strong Melee;
- Crowd Control.

Основной акцент игрока:

**Engagement Timing**

Следовательно, одинаковые числовые показатели для всех трёх фракций не являются целью проекта.

---

# 4. Unit Identity как ограничение при балансировке

Одним из важнейших принципов проекта стало сохранение Unit Identity.

Если юнит оказывается слишком сильным, это не означает, что необходимо уменьшить его самую большую характеристику.

Сначала необходимо определить:

> Какая характеристика является частью идентичности юнита, а какая создаёт проблемное поведение?

Наиболее подробно этот подход был применён к:

`HOR_02 — Stone Ogre`

Stone Ogre имеет Unit Identity:

**Heavy Frontline Tank**

Его ключевая сильная сторона:

**Very High Durability**

Следовательно, большое количество HP является не случайной характеристикой, а частью Design Intent.

---

# 5. Stone Ogre как основной Balance Case

Stone Ogre стал наиболее подробно исследованным юнитом проекта.

Первоначальный вопрос заключался не просто в том:

> Как сделать Stone Ogre слабее?

Более точный вопрос:

> Как уменьшить чрезмерное offensive pressure Stone Ogre, не разрушив его роль очень устойчивого Tank?

Именно эта постановка задачи определила последующий выбор Balance Lever.

---

# 6. Выбор Damage вместо HP

Для Stone Ogre рассматривалось влияние различных характеристик.

Дополнительно проводился HP Sensitivity Analysis и Threshold Refinement.

Однако исследование HP не означало, что HP обязательно должен быть уменьшен.

Поскольку высокая Durability является частью Unit Identity Stone Ogre, основной Balance Lever был выбран другой:

**Damage**

Таким образом, цель заключалась в следующем:

**уменьшить offensive power**

при сохранении:

**Tank Durability**

---

# 7. Изменение Stone Ogre

Исходный Damage Stone Ogre:

**96.00**

После Iteration 01:

**91.20**

После Iteration 02:

**86.64**

Полная последовательность:

**96.00 → 91.20 → 86.64**

Каждая Iteration применяла:

**-5%**

к текущему значению Damage.

---

# 8. Cumulative Damage Reduction

Два последовательных уменьшения на 5% не равны ровно 10% от первоначального значения.

Расчёт:

**0.95 × 0.95 = 0.9025**

Следовательно, итоговый Damage составляет:

**90.25%**

от первоначального.

Общее уменьшение:

**100% - 90.25% = 9.75%**

Итого:

**Cumulative Damage Reduction = 9.75%**

---

# 9. Stone Ogre в Iteration 02

В Iteration 02 использовались следующие значения:

**Damage Before = 91.20**

**Damage After = 86.64**

**DPS Before = 57.00**

**DPS After = 54.15**

**HP = 1760**

При этом HP намеренно не изменялся.

Это позволяло проверить конкретную Balance Hypothesis:

> Снижение Damage должно уменьшить offensive pressure Stone Ogre при сохранении его высокой Durability.

---

# 10. Изменение Combat Score

Для Stone Ogre в Iteration 02:

**Combat Score Before = 95.45**

**Combat Score After = 90.91**

То есть:

**95.45 → 90.91**

Distance From 50:

**45.45 → 40.91**

Таким образом, аналитическая метрика Direct Target изменилась в предполагаемом направлении.

При этом результат не следует интерпретировать как реальный PvP Win Rate.

`Combat Score` является внутренней диагностической метрикой текущего analytical pipeline.

---

# 11. Changed Matchup Iteration 02

После Iteration 02 изменился один matchup:

`ELF_02 — Great Forest Bear`

против:

`HOR_02 — Stone Ogre`

### Before

**Stone Ogre Win**

### After

**Draw**

Поскольку Stone Ogre являлся Direct Target:

**Impact Type = Direct**

---

# 12. Изменение Combat Time

В том же matchup:

**Combat Time Before = 28.8 sec**

**Combat Time After = 30.4 sec**

Изменение:

**+1.6 sec**

Следовательно, уменьшение Damage не только изменило Winner, но и увеличило продолжительность боя.

Это соответствует исходной Balance Hypothesis об уменьшении offensive pressure Stone Ogre.

---

# 13. Unchanged Matchups также содержат информацию

Большинство matchup Stone Ogre не изменили Winner после Iteration 02.

Однако в нескольких случаях увеличился Combat Time.

Например:

**14.4 → 16.0 sec**

или:

**12.8 → 14.4 sec**

Это показывает важный принцип:

> Unchanged Winner не означает отсутствие эффекта от Balance Change.

Изменение может влиять на:

- Combat Time;
- Remaining HP;
- количество выполненных атак;
- близость matchup к threshold;

ещё до того, как:

**Win**

превратится в:

**Draw**

или:

**Loss**.

---

# 14. Локальный и глобальный эффект

В Iteration 02:

**Stone Ogre Distance From 50**

изменился:

**45.45 → 40.91**

Однако:

**Average Distance From 50**

для всей системы:

**27.27 → 27.27**

Изменение:

**0.00**

Это демонстрирует различие между:

**Local Metric**

и:

**Global Metric**

---

# 15. Почему Global Metric может не измениться

Iteration 02 изменяла один параметр одного юнита из двенадцати.

Поэтому локальное улучшение не обязано заметно изменить агрегированную характеристику всей системы.

Следовательно:

**Local Improvement ≠ Automatic Global Improvement**

Но одновременно:

**Unchanged Global Metric ≠ No Effect**

Для Balance Analysis необходимо использовать оба уровня анализа.

---

# 16. Контролируемые изменения оказались полезнее крупных изменений

Проект показал преимущество небольших Balance Changes.

Изменения около:

**5%**

позволяли:

- наблюдать направление эффекта;
- обнаруживать matchup thresholds;
- уменьшать вероятность масштабных Side Effects;
- сохранять Unit Identity;
- проще связывать причину и результат.

Большой nerf или buff мог бы сразу изменить множество matchup, но сделал бы анализ причин значительно сложнее.

---

# 17. Matchup Thresholds

Sensitivity Analysis показал важность threshold behavior.

Combat simulation работает с отдельными атаками.

Поэтому небольшое изменение параметра иногда позволяет юниту:

- пережить ещё одну атаку;
- выполнить дополнительную собственную атаку;
- изменить итоговый результат боя.

В результате небольшое изменение может привести к:

**Win → Draw**

или:

**Draw → Loss**

Это означает, что связь между изменением характеристики и результатом боя не всегда является линейной.

---

# 18. Значение Sensitivity Analysis

Sensitivity Analysis оказался полезен не только для поиска нового значения параметра.

Он позволил понять:

- насколько устойчив конкретный matchup;
- где находятся transition areas;
- какие результаты чувствительны к небольшим изменениям;
- какие matchup практически не реагируют на изменение параметра.

Таким образом, Sensitivity Analysis используется как инструмент понимания системы, а не только как автоматический способ поиска «правильного числа».

---

# 19. Reproducibility

Для Iteration 01 была выполнена отдельная проверка Reproducibility.

Использовалось:

**5 runs**

по:

**66 matchup**

на каждый запуск.

Всего:

**330 matchup records**

Результат:

- Byte Identical Files: **Yes**
- Unstable Matchups: **0**
- Changed Row Comparisons: **0**
- Changed Field Comparisons: **0**
- Reproducibility Status: **Reproducible**

Это подтверждает deterministic behavior simulation при одинаковых входных данных.

---

# 20. Reproducibility не равна Correctness

Один из наиболее важных аналитических выводов проекта:

> Reproducibility показывает стабильность результата, но сама по себе не доказывает его правильность.

Если deterministic-код содержит ошибку, он способен стабильно воспроизводить один и тот же неправильный результат.

Поэтому кроме Reproducibility необходимы:

- sanity checks;
- diagnostics;
- Data Lineage;
- comparison;
- проверка исходных предположений.

---

# 21. Data Lineage как часть Balance Analysis

Во время работы с Iteration 01 была обнаружена проблема, при которой downstream analysis некорректно сохранял информацию о Direct Targets.

Это могло привести к неправильной классификации:

**Direct Effects**

как:

**Indirect Effects**

После диагностики источник Direct Target information был скорректирован.

Этот случай показал:

> правильная математика недостаточна, если аналитический pipeline неправильно отслеживает происхождение данных.

---

# 22. Расхождение aggregate results Iteration 01

Разные analytical stages сохранили отличающиеся aggregate results для Iteration 01.

Один analysis output показывал:

- Improved Units: **3**
- Worsened Units: **1**
- Changed Matchups: **3**
- Average Distance From 50: **27.28 → 25.76**

Более поздний comparison output показывал:

- Improved Units: **2**
- Worsened Units: **2**
- Changed Matchups: **2**
- Average Distance From 50: **27.27 → 27.27**

Эти результаты не были искусственно объединены или скрыты.

Они рассматриваются как обнаруженная проблема согласованности разных analytical stages.

---

# 23. Что показывает это расхождение

Расхождение демонстрирует необходимость:

- единого source of truth;
- контроля версий generated outputs;
- проверки aggregation logic;
- сохранения Data Lineage;
- regression checks;
- повторной валидации downstream results после изменения pipeline.

Это является не только технической проблемой, но и частью реального Data Analysis workflow.

---

# 24. Source Data Integrity

Исходный файл:

`data/unit_balance.csv`

сохранялся отдельно от экспериментальных результатов.

В ходе Iteration 02 дополнительно проверялся SHA-256.

Hash Before и After:

`83a937076d861ffe9f5721e9eac6c2a3cd4a08d120d569b8c041cf4722098499`

Результат:

**Source unchanged: Yes**

Таким образом, Balance Iteration не перезаписала baseline source data.

---

# 25. Почему Source Data нельзя изменять во время эксперимента

Если baseline автоматически перезаписывается после каждой Iteration, становится сложнее определить:

- какие значения были исходными;
- что изменилось;
- какая Iteration внесла изменение;
- можно ли воспроизвести предыдущий эксперимент;
- можно ли выполнить rollback.

Поэтому в проекте разделяются:

**Source Data**

**Experimental State**

**Generated Results**

---

# 26. Что текущий анализ действительно позволяет утверждать

На основании текущих результатов можно утверждать, что:

1. deterministic 1v1 model способна стабильно воспроизводить одинаковые результаты при одинаковых входных данных;

2. небольшие изменения характеристик способны влиять на отдельные matchup;

3. изменение Damage Stone Ogre влияет не только на Winner, но и на Combat Time;

4. Iteration 02 оказала локальное воздействие;

5. в Iteration 02 был зафиксирован один Direct Changed Matchup;

6. Indirect Changed Matchups для Iteration 02 не были зафиксированы;

7. Stone Ogre Combat Score изменился с **95.45** до **90.91**;

8. Stone Ogre Distance From 50 изменился с **45.45** до **40.91**;

9. HP Stone Ogre сохранился на уровне **1760**;

10. исходный `unit_balance.csv` не был изменён Iteration 02.

---

# 27. Чего текущий анализ не доказывает

Результаты проекта не являются доказательством реального production balance.

Текущая модель не позволяет утверждать:

- реальный PvP Win Rate;
- реальную популярность юнитов;
- реальный META;
- полную сбалансированность фракций;
- баланс Army Composition;
- баланс Economy;
- влияние Player Skill;
- влияние карты;
- влияние Positioning;
- влияние всех способностей в полноценном бою;
- влияние Progression;
- влияние Monetization;
- влияние изменений на Retention.

Для таких выводов потребуются более сложные модели или реальные player data.

---

# 28. Ограничения текущей combat simulation

Текущая базовая 1v1 model учитывает прежде всего:

- HP;
- Damage;
- Attack Interval;
- независимое время атак;
- одновременные атаки.

Она намеренно не моделирует полностью:

- способности;
- Attack Range;
- Move Speed;
- Positioning;
- Pathfinding;
- Terrain;
- Army Composition;
- Target Selection;
- Focus Fire;
- Economy;
- Production;
- Upgrades;
- Player Skill.

Поэтому результаты должны рассматриваться как controlled analytical experiments.

---

# 29. Ограничения Ability Analysis

Для всех 12 юнитов были разработаны способности и основные правила взаимодействия.

В проекте присутствуют, например:

- Reassemble;
- Death Feast;
- Cursed Spear;
- Curse;
- Evasive Step;
- Guardian Roar;
- Focused Bolt;
- Arcane Shield;
- Blood Rush;
- Stone Skin;
- Knife Barrage;
- Bone Smash.

Однако базовая pairwise combat simulation пока не реализует всю сложность этих механик одновременно.

Следовательно, текущий numerical balance является первым уровнем анализа.

---

# 30. Почему 1v1 model всё равно полезна

Несмотря на ограничения, 1v1 simulation позволяет изолировать отдельные параметры.

Например, если между Before и After у Stone Ogre изменяется только Damage, значительно проще определить влияние именно этой характеристики.

Поэтому упрощённая модель полезна для:

- первоначального поиска outliers;
- проверки Balance Hypotheses;
- исследования thresholds;
- Sensitivity Analysis;
- Before/After comparison;
- проверки технической воспроизводимости.

После этого результаты можно проверять в более сложных моделях.

---

# 31. Основной вывод по Stone Ogre

Текущие результаты поддерживают следующую гипотезу:

> Offensive power Stone Ogre можно уменьшать через Damage, не уменьшая напрямую его основную Tank Durability.

Iteration 02 сохранила:

**HP = 1760**

при этом:

**Damage: 91.20 → 86.64**

**DPS: 57.00 → 54.15**

**Combat Score: 95.45 → 90.91**

и изменила:

**Great Forest Bear vs Stone Ogre**

с:

**Stone Ogre Win**

на:

**Draw**

---

# 32. Текущий статус Iteration 02

Iteration 02 имеет статус:

**Promising Candidate for Further Validation**

Это означает:

- кандидат не отклоняется;
- изменение показало ожидаемый локальный эффект;
- Unit Identity Stone Ogre сохраняется;
- необходимы дополнительные уровни проверки.

Iteration 02 не объявляется:

**Final Production Balance Patch**

---

# 33. Почему не следует продолжать nerf автоматически

Тот факт, что Stone Ogre Combat Score всё ещё значительно выше 50, не означает, что Damage необходимо автоматически уменьшать снова.

Это привело бы к ошибочному процессу:

**Score > 50 → Nerf → Score > 50 → Nerf → ...**

Такой подход игнорирует:

- Role;
- Faction Identity;
- counters;
- Army Composition;
- Economy;
- abilities;
- реальную игровую ценность.

Следующий шаг должен увеличивать качество модели, а не просто продолжать уменьшать цифры.

---

# 34. Основные выводы Balance Design

В ходе проекта были сформированы следующие практические принципы.

### 1. Balance является многомерной задачей

Одной метрики недостаточно для описания состояния игры.

### 2. 50% — reference point, а не обязательная цель

Асимметричная RTS предполагает favorable и unfavorable matchup.

### 3. Unit Identity необходимо сохранять

Balance Change не должен уничтожать назначение юнита.

### 4. Balance Lever должен соответствовать проблеме

Если Tank слишком силён из-за offensive pressure, не обязательно уменьшать его HP.

### 5. Небольшие изменения могут пересекать thresholds

Даже небольшой stat change способен изменить Winner.

### 6. Unchanged Winner не означает отсутствие эффекта

Combat Time и другие показатели также содержат полезную информацию.

### 7. Direct и Indirect Effects необходимо разделять

Иначе невозможно корректно оценить Side Effects.

### 8. Local и Global Metrics отвечают на разные вопросы

Улучшение конкретного юнита не обязано менять агрегированный показатель всей системы.

### 9. Reproducibility не равна Correctness

Стабильный результат также требует логической проверки.

### 10. Data Quality является частью Balance Design

Ошибочная классификация или потеря Data Lineage способны привести к неправильному Game Design-решению.

---

# 35. Навыки, продемонстрированные в проекте

Проект демонстрирует работу сразу с несколькими направлениями.

### Game Design

- Faction Design;
- Unit Design;
- Role Design;
- Ability Design;
- Counterplay;
- Interaction Design;
- Balance Risks;
- Unit Identity;
- Faction Identity.

### Google Sheets / Excel

- структурирование balance-данных;
- таблицы юнитов;
- таблицы способностей;
- Interaction Matrix;
- Balance Risks;
- подготовка данных для анализа.

### Python

- чтение CSV;
- Data Validation;
- Data Analysis;
- автоматические расчёты;
- combat simulation;
- matchup analysis;
- Balance Iterations;
- Before/After comparison;
- Reproducibility Check;
- Impact Analysis;
- diagnostics;
- Sensitivity Analysis;
- Threshold Refinement.

### Analytical Thinking

- формулирование гипотез;
- controlled experiments;
- анализ причин и следствий;
- проверка Side Effects;
- поиск thresholds;
- сравнение нескольких Iterations;
- Data Quality Control.

### Documentation

- фиксация Design Intent;
- описание методологии;
- документирование Balance Iterations;
- фиксация ограничений;
- формирование итоговых выводов.

---

# 36. Следующий уровень — Ability-Aware Simulation

Одним из основных направлений дальнейшего развития является интеграция способностей непосредственно в общую combat simulation.

Это позволит количественно исследовать:

- Reassemble + Death Feast;
- Cursed Spear + Curse;
- Blood Rush + Curse;
- Guardian Roar + Arcane Shield;
- Evasive Step vs Knife Barrage;
- Bone Smash vs Focused Bolt;
- Stone Skin timing;
- CC Chain.

После этого можно будет сравнивать не только базовые характеристики юнитов, но и реальную ценность их Ability Kits.

---

# 37. Следующий уровень — Army Composition

RTS-баланс нельзя полностью исследовать только через 1v1.

Следующим важным этапом может стать:

**Army-vs-Army Simulation**

Например:

- 3 Infantry + 1 Tank;
- 2 Ranged + 1 Tank + 1 Support;
- mixed faction compositions;
- разные пропорции ролей.

Это позволит исследовать:

- synergy;
- Focus Fire;
- frontline/backline;
- обязательность отдельных юнитов;
- counter-compositions.

---

# 38. Следующий уровень — META Analysis

После появления Army Composition можно исследовать META.

Например:

- какие составы используются чаще;
- какие составы выигрывают чаще;
- существуют ли обязательные юниты;
- какие counters доступны;
- насколько разнообразны viable compositions;
- как Balance Patch меняет composition diversity.

Это будет значительно ближе к реальной работе с META в мобильной RTS.

---

# 39. Следующий уровень — Economy

Сильный в прямом бою юнит не обязательно является несбалансированным.

Если его стоимость значительно выше, его Combat Power может быть оправдан.

Поэтому дальнейшая модель может включать:

- Unit Cost;
- Training Time;
- Upgrade Cost;
- Upgrade Time;
- Resource Income;
- Population Capacity.

После этого можно рассчитывать:

**Damage per Cost**

**DPS per Cost**

**HP per Cost**

**Combat Value per Cost**

---

# 40. Следующий уровень — SQL и Telemetry

При переходе к более крупному объёму simulated или player data можно использовать SQL.

В базу данных могут сохраняться:

- Match_ID;
- Player_ID;
- Faction;
- Army Composition;
- Unit Usage;
- Winner;
- Match Duration;
- Damage Dealt;
- Units Lost;
- Resources Spent;
- Ability Usage;
- Map;
- Rating;
- Patch Version.

Это позволит выполнять запросы, приближенные к реальной Game Analytics.

---

# 41. Следующий уровень — Dashboards

На основании SQL или подготовленных CSV можно создавать dashboards с показателями:

- Pick Rate;
- Win Rate;
- Usage Rate;
- matchup matrix;
- Faction Performance;
- Unit Performance;
- Patch Before/After;
- Combat Duration;
- composition diversity.

Это позволит быстрее находить потенциальные Balance Problems.

---

# 42. Следующий уровень — Stochastic Simulation

Текущая модель deterministic.

В дальнейшем можно добавить случайность:

- Damage Variance;
- Critical Hits;
- Ability Proc Chance;
- Target Selection;
- Reaction Delay.

После этого можно использовать:

**Monte Carlo Simulation**

Вместо одного боя конкретный matchup можно выполнять, например:

**1 000**

или:

**10 000**

раз.

Тогда результатом будет не один Winner, а распределение результатов.

---

# 43. Следующий уровень — Playtests

Даже сложная simulation не заменяет Playtests.

Численно сбалансированный юнит может ощущаться:

- неприятным;
- слишком простым;
- слишком сложным;
- несправедливым;
- неинтересным.

Поэтому окончательная Balance Validation должна сочетать:

**Data**

и:

**Player Experience**

---

# 44. Итоговый workflow дальнейшего развития

Следующий уровень проекта может выглядеть следующим образом:

**Current Numerical Model**

↓

**Ability-Aware Combat**

↓

**Army Composition**

↓

**Economy**

↓

**Stochastic Simulation**

↓

**SQL / Telemetry**

↓

**Dashboards**

↓

**Playtests**

↓

**META Analysis**

↓

**Next Balance Iteration**

---

# 45. Итоговый вывод

**Era of Strife** демонстрирует подход, при котором Balance Design рассматривается как последовательность проверяемых гипотез.

Проект начинается с:

**Design Intent**

После этого игровые решения преобразуются в:

**Structured Data**

Затем данные проходят:

**Validation**

После чего выполняется:

**Combat Simulation**

Результаты используются для:

**Balance Analysis**

На основании анализа формируется:

**Balance Hypothesis**

После controlled change выполняется:

**Before/After Comparison**

При необходимости добавляются:

**Diagnostics**

**Reproducibility Check**

**Sensitivity Analysis**

**Threshold Refinement**

После этого принимается следующее:

**Design Decision**

Главный принцип проекта можно сформулировать следующим образом:

> Balance Change должен быть проверяемой гипотезой, которую можно измерить, воспроизвести и интерпретировать в контексте Game Design.

Текущий результат Stone Ogre показывает применение этого подхода на практике.

Вместо случайного уменьшения характеристик был выполнен последовательный процесс:

**Problem Detection**

↓

**Damage Nerf**

↓

**Impact Analysis**

↓

**Diagnostics**

↓

**Sensitivity Analysis**

↓

**Threshold Refinement**

↓

**Second Controlled Damage Nerf**

↓

**Iteration Comparison**

↓

**Promising Candidate for Further Validation**

Именно сочетание Game Design, данных, Python и последовательного экспериментального подхода является основным результатом проекта **Era of Strife**.