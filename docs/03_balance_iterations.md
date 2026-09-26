# Era of Strife — Итерации баланса

## 1. Назначение документа

Этот документ описывает практический процесс Balance Iterations в **Era of Strife**.

Если `02_balance_methodology.md` объясняет общую методологию, то здесь фиксируется реальная последовательность проведённых экспериментов:

**Baseline Analysis → Balance Hypothesis → Iteration 01 → Impact Analysis → Diagnostics → Sensitivity Analysis → Threshold Refinement → Iteration 02 → Iteration Comparison**

Основная задача заключалась не в последовательном изменении характеристик до тех пор, пока каждый юнит не приблизится к 50%.

Вместо этого каждая Iteration должна была отвечать на конкретный вопрос:

> Можно ли исправить обнаруженную проблему контролируемым изменением параметров, сохранив Unit Identity и не создавая непредусмотренных Side Effects?

---

# 2. Baseline Analysis

В проекте представлены:

- 3 фракции;
- 12 юнитов;
- 4 основные боевые роли;
- 66 уникальных pairwise matchup.

Первоначальный Python-анализ использовался для исследования числовых характеристик и результатов combat simulation.

На основании baseline были выделены два основных кандидата для первой Balance Iteration:

- `HOR_01 — Blade Goblin`
- `HOR_02 — Stone Ogre`

Эти юниты представляли разные проблемы, поэтому требовали противоположных изменений.

Blade Goblin рассматривался как:

**Buff Candidate**

Stone Ogre рассматривался как:

**Nerf Candidate**

---

# 3. Iteration 01

## 3.1. Цель

Iteration 01 проверяла следующую гипотезу:

> Небольшие контролируемые изменения Damage у двух выявленных outliers могут улучшить их положение, не вызывая масштабной перестройки всей matchup matrix.

В Iteration 01 использовались два Direct Targets:

- `HOR_01 — Blade Goblin`
- `HOR_02 — Stone Ogre`

---

# 4. Blade Goblin — изменение Iteration 01

Blade Goblin должен выполнять роль:

**Aggressive Melee Infantry**

Его задача — создавать давление после успешного входа в melee-бой.

Baseline-анализ показал необходимость проверить небольшой buff.

Исходный Damage:

**71.25**

После Iteration 01:

**74.81**

Изменение:

**≈ +5%**

Таким образом:

**71.25 → 74.81**

### Balance Hypothesis

> Небольшое увеличение Damage должно повысить offensive pressure Blade Goblin, не изменяя его основную идентичность как агрессивного, но сравнительно уязвимого melee-юнита.

При этом не изменялись основные характеристики, определяющие его роль.

---

# 5. Stone Ogre — изменение Iteration 01

Stone Ogre имеет Unit Identity:

**Heavy Frontline Tank**

Его ключевая сильная сторона:

**Very High Durability**

При этом первоначальный анализ показал необходимость проверить его offensive power.

Baseline Damage:

**96.00**

После Iteration 01:

**91.20**

Расчёт:

**96 × 0.95 = 91.20**

Изменение:

**-5%**

DPS изменился:

**60.00 → 57.00**

### Balance Hypothesis

> Stone Ogre создаёт слишком высокое offensive pressure относительно своей роли Tank. Снижение Damage может уменьшить его offensive power без прямого ослабления Durability.

Поэтому HP на этом этапе не использовался как основной Balance Lever.

---

# 6. Почему изменения были небольшими

Для обоих Direct Targets первоначально использовалась корректировка около 5%.

Это было сделано намеренно.

Слишком большое изменение могло:

- полностью изменить matchup;
- разрушить Unit Identity;
- создать большое количество Side Effects;
- затруднить понимание причин результата.

Небольшой шаг позволяет оценить чувствительность системы до применения более агрессивных изменений.

---

# 7. Unit-Level Results Iteration 01

Один из основных результатов анализа Iteration 01 содержал следующие показатели:

| Metric | Result |
|---|---:|
| Total Units | 12 |
| Improved Units | 3 |
| Worsened Units | 1 |
| Unchanged Units | 8 |
| Direct Targets | 2 |
| Direct Improved | 2 |
| Direct Worsened | 0 |
| Direct Unchanged | 0 |

В рамках этого аналитического этапа оба Direct Targets были классифицированы как:

**Improved**

Это являлось положительным сигналом для исходных Balance Hypotheses.

Однако результат также содержал:

**1 Worsened Unit**

Поэтому проверка не могла ограничиваться только двумя Direct Targets.

---

# 8. Global Metric Iteration 01

В одном из основных аналитических результатов Average Distance From 50 изменился:

**Before: 27.28**

**After: 25.76**

Изменение:

**-1.52**

То есть:

**27.28 → 25.76**

Уменьшение Average Distance From 50 показывает движение общей числовой картины ближе к reference point.

Однако это не означает автоматически:

> игра стала полностью сбалансированной.

Метрика рассматривается вместе с:

- Unit-Level Results;
- Changed Matchups;
- Direct Effects;
- Indirect Effects;
- Design Intent.

На этом этапе итоговый результат Iteration 01 был классифицирован как:

**Successful**

---

# 9. Changed Matchups Iteration 01

Из:

**66 уникальных matchup**

в одном из основных результатов анализа изменились:

**3 matchup**

Не изменились:

**63 matchup**

Доля Changed Matchups:

**3 / 66 × 100 ≈ 4.55%**

Таким образом, изменение затронуло приблизительно:

**4.55%**

pairwise matchup matrix.

Это указывает на сравнительно локализованное воздействие Iteration 01.

---

# 10. ELF_01 vs ELF_02

Один из обнаруженных Changed Matchups:

`ELF_01 — Elven Swordsman`

против:

`ELF_02 — Great Forest Bear`

### Before

**Great Forest Bear Win**

### After

**Draw**

Ни один из этих юнитов не являлся Direct Target Iteration 01.

Следовательно, изменение требовало дополнительного анализа как потенциальный:

**Indirect Effect**

Именно подобные результаты показывают, почему нельзя проверять только Direct Targets.

---

# 11. ELF_01 vs HOR_02

Следующий Changed Matchup:

`ELF_01 — Elven Swordsman`

против:

`HOR_02 — Stone Ogre`

### Before

**Stone Ogre Win**

### After

**Draw**

Stone Ogre являлся Direct Target Iteration 01.

Следовательно, изменение этого matchup непосредственно связано с тестируемым Balance Change и относится к:

**Direct Effect**

Результат показывает, что уменьшение Damage Stone Ogre оказалось достаточным для пересечения конкретного matchup threshold.

---

# 12. UND_01 vs HOR_01

Ещё один Changed Matchup:

`UND_01 — Skeleton Swordsman`

против:

`HOR_01 — Blade Goblin`

### Before

**Skeleton Swordsman Win**

### After

**Blade Goblin Win**

Blade Goblin являлся Direct Target.

Следовательно, изменение относится к:

**Direct Effect**

Небольшой buff Damage оказался достаточным для изменения Winner в этом matchup.

---

# 13. Первоначальная интерпретация Iteration 01

Iteration 01 показала, что небольшие изменения Damage способны пересекать matchup thresholds.

Для Blade Goblin:

**+5% Damage**

изменили как минимум один direct matchup.

Для Stone Ogre:

**-5% Damage**

также изменили direct matchup.

При этом большая часть matchup matrix осталась стабильной.

Это соответствовало идее контролируемого Balance Change.

Однако последующий analysis pipeline выявил проблему классификации, которую необходимо было исследовать до дальнейших выводов.

---

# 14. Reproducibility Check

Чтобы проверить стабильность combat simulation, Iteration 01 была повторена несколько раз при одинаковых условиях.

Количество запусков:

**5**

Количество matchup в одном запуске:

**66**

Общее количество обработанных matchup records:

**66 × 5 = 330**

Результаты:

| Metric | Result |
|---|---|
| Runs | 5 |
| Matchups Per Run | 66 |
| Byte Identical Files | Yes |
| Unstable Matchups | 0 |
| Changed Row Comparisons | 0 |
| Changed Field Comparisons | 0 |
| Reproducibility Status | Reproducible |

Это означает, что simulation при одинаковых входных данных воспроизводила одинаковый результат.

---

# 15. Что доказал Reproducibility Check

Проверка дала основания утверждать:

> различия между baseline и Balance Iteration не возникали из-за случайного поведения deterministic simulation.

Но она **не доказывала**, что каждый этап последующего анализа был логически корректен.

Это различие стало особенно важным на следующем этапе.

---

# 16. Проблема Impact Analysis

После Iteration 01 был выполнен более подробный Impact Analysis.

В одном из downstream-результатов неожиданно появилась классификация:

**Direct Target Units = 0**

Это противоречило структуре Iteration 01, поскольку были явно изменены:

- `HOR_01`
- `HOR_02`

Следовательно, результат потребовал диагностики.

---

# 17. Почему результат был подозрительным

Например, matchup:

`ELF_01 vs HOR_02`

включал Stone Ogre.

Stone Ogre был Direct Target.

Следовательно, изменение этого matchup не должно было автоматически классифицироваться как независимый Indirect Effect.

Аналогично:

`UND_01 vs HOR_01`

включал Blade Goblin, который также был Direct Target.

Это показало, что проблема, вероятно, находилась не в самой combat simulation, а в downstream classification.

---

# 18. Impact Diagnostics

Для исследования проблемы был добавлен отдельный diagnostic stage.

Проверка показала, что ожидаемые Direct Targets действительно существовали:

- `HOR_01`
- `HOR_02`

Однако информация о них неправильно использовалась на одном из последующих этапов analytical pipeline.

Таким образом, проблема относилась к:

**Data Lineage / Classification**

а не к базовой формуле боя.

---

# 19. Исправление Data Lineage

После диагностики логика определения Direct Targets была скорректирована.

Canonical iteration data стала использоваться как основной source of truth для определения намеренно изменённых юнитов.

Это позволило сохранить информацию:

**какие юниты были изменены специально**

при переходе к downstream Impact Analysis.

---

# 20. Главный вывод из диагностической ошибки

Эта ситуация продемонстрировала важный принцип:

> Reproducible result не обязательно является Correct result.

Скрипт может пять раз подряд выдавать абсолютно одинаковый результат.

Но если его классификационная логика неправильна, результат будет:

**стабильно неправильным.**

Поэтому analytical pipeline требует не только автоматических тестов на воспроизводимость, но и проверки логической согласованности результатов.

---

# 21. Почему дальнейшее внимание было направлено на Stone Ogre

После Iteration 01 Stone Ogre остался особенно интересным Balance Candidate.

Его Unit Identity:

**Heavy Frontline Tank**

Основная сила:

**Very High Durability**

Основная слабость:

**Very Low Mobility**

Возник следующий вопрос:

> Как дополнительно уменьшить чрезмерное offensive pressure Stone Ogre, не разрушая его Tank Identity?

Простое значительное уменьшение HP могло бы решить числовую проблему ценой уничтожения основной сильной стороны юнита.

Поэтому потребовалось дополнительное исследование.

---

# 22. Stone Ogre Sensitivity Analysis

Следующим этапом стал Sensitivity Analysis.

Основная задача:

> Исследовать, как изменение отдельных параметров Stone Ogre влияет на matchup outcomes.

В частности, дополнительно исследовалось влияние HP.

При этом задача заключалась **не обязательно в том, чтобы уменьшить HP**.

HP использовался как исследуемая переменная для понимания структуры matchup thresholds.

---

# 23. Какие данные анализировались

Для различных tested values можно было сравнивать:

- Stone Ogre HP;
- Opponent;
- Opponent Role;
- Winner;
- Combat Time;
- Stone Ogre Remaining HP;
- Opponent Remaining HP;
- количество атак Stone Ogre;
- количество атак противника.

Это позволяло увидеть не только:

**Win / Draw / Loss**

но и то, насколько близко конкретный matchup находился к смене результата.

---

# 24. Что искал Sensitivity Analysis

Основные вопросы:

1. Какие matchup практически не реагируют на небольшие изменения HP?
2. Какие matchup находятся около threshold?
3. Где Stone Ogre перестаёт выигрывать?
4. Где Win превращается в Draw?
5. Где Draw превращается в Loss?
6. Насколько сильно меняется Combat Time?
7. Сколько дополнительных атак позволяет выполнить конкретное количество HP?

---

# 25. Threshold Behavior

В deterministic combat model Damage наносится отдельными атаками.

Поэтому результат может меняться скачкообразно.

Например:

**больше HP → Stone Ogre переживает ещё одну атаку**

↓

**Stone Ogre получает возможность выполнить ещё одну собственную атаку**

↓

**Winner изменяется**

Таким образом, даже небольшая разница в HP может иногда вызвать:

**Loss → Draw**

или:

**Draw → Win**

Это называется threshold behavior.

---

# 26. Threshold Refinement

После широкого Sensitivity Analysis был выполнен отдельный Threshold Refinement.

Результаты сохранялись в том числе в:

`analysis/results/iterations/sensitivity/stone_ogre_hp_threshold_refinement.csv`

и:

`analysis/results/iterations/sensitivity/stone_ogre_hp_threshold_refinement_summary.csv`

Целью было более подробно исследовать области, где результат matchup менялся.

---

# 27. Почему HP не стал основным Balance Lever Iteration 02

Sensitivity Analysis помог понять влияние Durability на matchup.

Но с точки зрения Game Design Stone Ogre должен оставаться:

**очень устойчивым Tank.**

Поэтому дальнейшее уменьшение HP не было выбрано в качестве основного решения Iteration 02.

Вместо этого было принято решение продолжить уменьшать:

**offensive power**

через:

**Damage**

Таким образом сохранялась логика:

**Durability остаётся сильной стороной**

при уменьшении:

**offensive pressure**

---

# 28. Переход к Iteration 02

После Iteration 01 и Sensitivity Analysis была сформулирована более узкая гипотеза:

> Дополнительное уменьшение Damage Stone Ogre может улучшить его проблемные matchup, сохранив HP и Tank Identity.

Iteration 02 стала более контролируемым экспериментом.

В ней использовался только один Direct Target:

`HOR_02 — Stone Ogre`

---

# 29. Iteration 02 — изменение Damage

Перед Iteration 02 Stone Ogre имел:

**Damage = 91.20**

Новое значение:

**Damage = 86.64**

Расчёт:

**91.20 × 0.95 = 86.64**

Absolute Change:

**-4.56**

Percentage Change:

**-5%**

Таким образом:

**91.20 → 86.64**

---

# 30. Iteration 02 — изменение DPS

До Iteration 02:

**DPS = 57.00**

После:

**DPS = 54.15**

То есть:

**57.00 → 54.15**

Изменение также составляет:

**-5%**

При этом HP оставался:

**1760**

Это особенно важно для проверяемой Balance Hypothesis.

---

# 31. Balance Hypothesis Iteration 02

Гипотеза была сформулирована следующим образом:

> Reduce Stone Ogre offensive power while preserving its tank durability.

То есть:

- Damage уменьшается;
- DPS уменьшается;
- HP остаётся прежним;
- Durability сохраняется;
- проверяется изменение matchup.

Это делает Iteration 02 более точным controlled experiment.

---

# 32. Cumulative Damage Change Stone Ogre

До Iteration 01:

**Damage = 96.00**

После Iteration 01:

**Damage = 91.20**

После Iteration 02:

**Damage = 86.64**

Полная последовательность:

**96.00 → 91.20 → 86.64**

Каждая Iteration уменьшала текущее значение на:

**5%**

Однако два последовательных `-5%` не равны ровно `-10%` от исходного значения.

---

# 33. Расчёт cumulative change

После первого изменения:

**96 × 0.95 = 91.20**

После второго:

**91.20 × 0.95 = 86.64**

Общий multiplier:

**0.95 × 0.95 = 0.9025**

Следовательно:

**86.64 / 96 = 0.9025**

Финальное значение составляет:

**90.25%**

от первоначального Damage.

Cumulative Damage Reduction:

**100% - 90.25% = 9.75%**

Итого:

**-9.75%**

от первоначального значения.

---

# 34. Combat Score Stone Ogre

В Iteration 02 summary были зафиксированы:

**Stone Ogre Combat Score Before = 95.45**

**Stone Ogre Combat Score After = 90.91**

То есть:

**95.45 → 90.91**

Соответствующий Distance From 50:

**Before = 45.45**

**After = 40.91**

То есть:

**45.45 → 40.91**

Direct Target приблизился к аналитическому reference point.

---

# 35. Как следует интерпретировать Combat Score

`Combat Score` в этом проекте является внутренней аналитической метрикой pipeline.

Его не следует автоматически интерпретировать как реальный PvP Win Rate.

Значение используется для:

- сравнения версий;
- обнаружения outliers;
- оценки направления изменения.

Поэтому результат:

**95.45 → 90.91**

показывает движение метрики, но не доказывает реальный Win Rate Stone Ogre среди игроков.

---

# 36. Iteration 02 — Changed Matchups

Iteration 02 summary зафиксировал:

**Changed Matchups = 1**

Из них:

**Direct Changed Matchups = 1**

**Indirect Changed Matchups = 0**

Таким образом, Iteration 02 оказала значительно более локальное воздействие на matchup outcomes.

---

# 37. Great Forest Bear vs Stone Ogre

Единственным Changed Matchup в Iteration 02 был:

`ELF_02 — Great Forest Bear`

против:

`HOR_02 — Stone Ogre`

### Before

**Stone Ogre Win**

### After

**Draw**

Stone Ogre являлся Direct Target.

Следовательно:

**Impact Type = Direct**

---

# 38. Combat Time в изменившемся matchup

Для:

`Great Forest Bear vs Stone Ogre`

Combat Time изменился:

**Before = 28.8 sec**

**After = 30.4 sec**

Разница:

**30.4 - 28.8 = 1.6 sec**

Таким образом:

**+1.6 sec**

После снижения Damage Stone Ogre бой стал длиннее и изменился:

**Stone Ogre Win → Draw**

Это хороший пример того, как уменьшение offensive power может одновременно влиять на:

- Combat Time;
- matchup result.

---

# 39. Другие matchup Stone Ogre

Большинство остальных matchup Stone Ogre сохранили прежнего Winner.

Например, в доступных результатах:

### ELF_03 vs HOR_02

**HOR_02 Win → HOR_02 Win**

Combat Time:

**14.4 → 16.0 sec**

### ELF_04 vs HOR_02

**HOR_02 Win → HOR_02 Win**

Combat Time:

**12.8 → 14.4 sec**

### HOR_01 vs HOR_02

**HOR_02 Win → HOR_02 Win**

Combat Time:

**16.0 → 17.6 sec**

### HOR_02 vs UND_02

**HOR_02 Win → HOR_02 Win**

Combat Time:

**25.6 → 27.2 sec**

В этих случаях Winner не изменился, но бой стал продолжительнее.

---

# 40. Почему Unchanged Winner всё равно важен

Если:

**Winner Before = Winner After**

это не означает:

**Balance Change не оказал эффекта.**

Увеличение Combat Time показывает, что Stone Ogre требовалось больше времени для победы.

Это соответствует гипотезе:

**уменьшить offensive pressure**

даже если конкретный matchup ещё не пересёк threshold смены Winner.

---

# 41. Unit-Level Results Iteration 02

Iteration 02 summary:

| Metric | Result |
|---|---:|
| Improved Units | 1 |
| Worsened Units | 1 |
| Unchanged Units | 10 |
| Changed Matchups | 1 |
| Direct Changed Matchups | 1 |
| Indirect Changed Matchups | 0 |

Большая часть системы сохранила прежние matchup outcomes.

---

# 42. Global Metric Iteration 02

Average Distance From 50:

**Before = 27.27**

**After = 27.27**

Изменение:

**0.00**

То есть:

**27.27 → 27.27**

Global Metric остался неизменным.

При этом локальная метрика Stone Ogre улучшилась:

**Distance From 50: 45.45 → 40.91**

Это показывает различие между:

**Local Improvement**

и:

**Global Improvement**

---

# 43. Почему неизменный Global Metric не означает отсутствие эффекта

Iteration 02 изменяла только один основной параметр одного Direct Target.

Поэтому ожидать значительного изменения агрегированной метрики всей системы необязательно.

Фактически было зафиксировано:

- уменьшение Stone Ogre Damage;
- уменьшение Stone Ogre DPS;
- уменьшение Stone Ogre Distance From 50;
- увеличение Combat Time в нескольких matchup;
- один Win → Draw;
- 0 Indirect Changed Matchups.

Следовательно, изменение оказало измеримый локальный эффект.

---

# 44. Итоговая классификация Iteration 02

В summary Iteration 02 получила:

**Iteration Result = Promising**

Recommendation:

**Keep Iteration 02 candidate for further validation.**

Это означает, что Iteration 02 не объявляется окончательным Balance Patch.

Она сохраняется как:

**Promising Candidate**

для дальнейшего тестирования.

---

# 45. Почему используется формулировка Promising Candidate

Текущая simulation является упрощённой.

Она не моделирует полностью:

- способности;
- Positioning;
- Attack Range;
- Move Speed;
- Army Composition;
- Economy;
- Player Skill.

Поэтому даже положительный результат 1v1 simulation недостаточен для утверждения:

> Stone Ogre полностью сбалансирован.

Более корректный вывод:

> Текущие результаты поддерживают Balance Hypothesis и позволяют сохранить Iteration 02 как кандидата для следующего этапа тестирования.

---

# 46. Iteration 01 vs Iteration 02

После выполнения второй Iteration был создан отдельный comparison stage.

Он генерировал результаты в:

`analysis/results/iterations/comparison_01_02/`

В том числе:

- `iteration_01_vs_02_summary.csv`
- `direct_targets_comparison.csv`
- `changed_matchups_comparison.csv`
- `portfolio_balance_summary.csv`

Это позволило сравнивать две Iterations в единой структуре.

---

# 47. Различие Iteration 01 и Iteration 02

### Iteration 01

Direct Targets:

- HOR_01
- HOR_02

Изменения:

- Blade Goblin Damage buff;
- Stone Ogre Damage nerf.

### Iteration 02

Direct Target:

- HOR_02

Изменение:

- дополнительный Stone Ogre Damage nerf.

Iteration 02 была более узкой и поэтому легче интерпретировалась с точки зрения причинно-следственной связи.

---

# 48. Важное расхождение aggregate metrics Iteration 01

При сравнении аналитических outputs было обнаружено, что разные stages pipeline сохранили отличающиеся aggregate results для Iteration 01.

Один из результатов Iteration 01 analysis показывал:

- Improved Units: **3**
- Worsened Units: **1**
- Unchanged Units: **8**
- Changed Matchups: **3**
- Average Distance From 50: **27.28 → 25.76**

Однако более поздний Iteration 01 vs Iteration 02 comparison output показывал для Iteration 01:

- Improved Units: **2**
- Worsened Units: **2**
- Unchanged Units: **8**
- Changed Matchups: **2**
- Average Distance From 50: **27.27 → 27.27**

Эти два набора результатов не следует искусственно объединять в одну цифру.

---

# 49. Как интерпретируется расхождение

Расхождение рассматривается как часть analytical history проекта.

Оно показывает необходимость:

- фиксировать source of truth для каждой метрики;
- контролировать версии generated results;
- проверять aggregation logic;
- сохранять Data Lineage;
- не подменять один output другим без объяснения.

До окончательной унификации pipeline эти результаты следует рассматривать как outputs разных analytical stages, а не как взаимозаменяемые значения.

---

# 50. Почему расхождение не нужно скрывать

В аналитическом проекте обнаружение несогласованности является полезным результатом.

Хуже было бы:

- выбрать более красивую цифру;
- удалить неудобный output;
- представить pipeline как полностью согласованный.

Правильный подход:

1. зафиксировать расхождение;
2. определить его источник;
3. выбрать canonical calculation;
4. добавить regression checks;
5. повторно сформировать downstream outputs.

Таким образом проект показывает не только Balance Analysis, но и Data Quality Control.

---

# 51. Source Data Integrity

В ходе Iteration 02 отдельно проверялось, что исходный:

`data/unit_balance.csv`

не изменяется.

SHA-256 Before и After:

`83a937076d861ffe9f5721e9eac6c2a3cd4a08d120d569b8c041cf4722098499`

Hash остался одинаковым.

Результат:

**Source unchanged: Yes**

Следовательно, Iteration 02 не перезаписала baseline source data.

---

# 52. Почему это важно

Balance Iterations должны быть экспериментами поверх baseline, а не необратимыми изменениями исходных данных.

Такой подход позволяет:

- воспроизвести Iteration;
- восстановить baseline;
- сравнить несколько кандидатов;
- проверить результаты;
- откатить Balance Change;
- сохранить историю проекта.

---

# 53. Итог Iteration 01

Iteration 01 показала:

- небольшие изменения Damage способны изменить конкретные matchup;
- оба Direct Targets отреагировали на изменения в основном аналитическом output;
- большая часть matchup matrix осталась стабильной;
- deterministic simulation воспроизводится;
- downstream analysis требует контроля Data Lineage;
- одного Reproducibility Check недостаточно для проверки Correctness.

---

# 54. Итог Stone Ogre Sensitivity Research

Дополнительное исследование Stone Ogre показало важность разделения:

**Unit Identity**

и:

**Problematic Numerical Behavior**

Stone Ogre должен оставаться очень устойчивым Tank.

Поэтому исследование HP не означало автоматического решения:

**уменьшить HP.**

Sensitivity Analysis использовался для понимания системы.

После этого в качестве основного Balance Lever был сохранён:

**Damage**

---

# 55. Итог Iteration 02

Iteration 02 показала:

- Stone Ogre Damage: **91.20 → 86.64**
- Stone Ogre DPS: **57.00 → 54.15**
- Stone Ogre HP: **1760 → 1760**
- Combat Score: **95.45 → 90.91**
- Distance From 50: **45.45 → 40.91**
- Changed Matchups: **1**
- Direct Changed Matchups: **1**
- Indirect Changed Matchups: **0**
- Average Distance From 50: **27.27 → 27.27**
- Iteration Result: **Promising**

Таким образом, Iteration 02 создала измеримый локальный эффект, сохранив Durability Stone Ogre.

---

# 56. Текущий Balance Decision

На текущем этапе Iteration 02 сохраняется как:

**Promising Candidate for Further Validation**

Это не Final Balance Patch.

Перед окончательным решением необходимы дополнительные уровни тестирования.

---

# 57. Следующие возможные эксперименты

Логичным продолжением могут стать:

- более детальный Damage Sensitivity Analysis Stone Ogre;
- ability-aware Stone Skin simulation;
- Army Composition testing;
- squad-vs-squad simulation;
- Faction-level matchup;
- Economy Balance;
- Unit Cost Efficiency;
- stochastic combat;
- Positioning;
- Target Selection;
- Player Skill simulation.

Это позволит перейти от isolated 1v1 analysis к более реалистичной RTS-среде.

---

# 58. Полная история Balance Iterations

Текущую историю можно представить следующим образом:

**Baseline**

↓

**Iteration 01**

Blade Goblin:

**Damage +≈5%**

Stone Ogre:

**Damage -5%**

↓

**Initial Result**

Direct Targets реагируют на изменения.

Небольшая часть matchup matrix изменяется.

↓

**Reproducibility Check**

**5 × 66 matchup**

Результат:

**Reproducible**

↓

**Impact Analysis**

Обнаруживается проблема Direct Target classification.

↓

**Diagnostics**

Проблема связывается с Data Lineage.

↓

**Pipeline Correction**

Direct Target information начинает использовать canonical iteration data.

↓

**Stone Ogre Sensitivity Analysis**

Исследуется влияние HP на matchup behavior.

↓

**Threshold Refinement**

Исследуются области смены:

**Win / Draw / Loss**

↓

**Design Decision**

Не ослаблять основную Durability Stone Ogre без необходимости.

Использовать Damage как основной Balance Lever.

↓

**Iteration 02**

Stone Ogre:

**Damage 91.20 → 86.64**

**DPS 57.00 → 54.15**

**HP = 1760**

↓

**Iteration 02 Result**

Great Forest Bear vs Stone Ogre:

**Stone Ogre Win → Draw**

Changed Matchups:

**1**

Indirect Changed Matchups:

**0**

↓

**Current Status**

**Iteration 02 = Promising Candidate for Further Validation**

---

# 59. Главный вывод

История Iteration 01 и Iteration 02 показывает, что Balance Design — это не последовательность случайных buff и nerf.

Рабочий процесс должен выглядеть следующим образом:

**Problem Detection**

↓

**Balance Hypothesis**

↓

**Controlled Change**

↓

**Simulation**

↓

**Before/After Comparison**

↓

**Impact Analysis**

↓

**Diagnostics**

↓

**Sensitivity Analysis**

↓

**Design Interpretation**

↓

**Next Iteration**

Именно такой подход используется в Era of Strife.

Итоговые выводы по проекту, его ограничения и направления дальнейшего развития собраны в:

`04_final_findings.md`