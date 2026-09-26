# Era of Strife — Game Design

## 1. О проекте

**Era of Strife** — концепт мобильной RTS, созданный как основа для практического проекта по Game Design, Balance Design и Data Analysis.

В рамках проекта разрабатывается не полноценная коммерческая игра, а структурированная игровая система, на которой можно последовательно изучать:

- проектирование фракций;
- проектирование юнитов;
- создание способностей;
- формирование сильных и слабых сторон;
- взаимодействие игровых механик;
- баланс характеристик;
- анализ matchup;
- поиск потенциальных проблем баланса;
- проведение balance iterations;
- проверку гипотез с помощью Python;
- анализ результатов симуляций.

Основная задача проекта — показать полный путь от первоначальной Game Design-концепции до принятия обоснованных решений по балансу на основании данных.

---

# 2. Основная структура игры

В текущей версии Era of Strife представлены:

- 3 фракции;
- 12 юнитов;
- по 4 юнита в каждой фракции;
- 4 основные боевые роли;
- индивидуальная способность для каждого юнита.

Используются следующие роли:

1. **Infantry**
2. **Tank**
3. **Ranged**
4. **Support**

Каждая фракция получает по одному представителю каждой роли.

Таким образом, структура выглядит следующим образом:

| Faction | Infantry | Tank | Ranged | Support |
|---|---|---|---|---|
| Undead | Skeleton Swordsman | Bone Dragon | Spear Devil | Witch |
| Forest & Dark Elves | Elven Swordsman | Great Forest Bear | Elven Mage | Elven Scholar |
| Horde | Blade Goblin | Stone Ogre | Orc Thrower | Boneclub Troll |

Такое распределение позволяет сравнивать между собой не только отдельные юниты, но и разные подходы фракций к выполнению одинаковых боевых задач.

---

# 3. Принцип асимметричного дизайна

Фракции Era of Strife не должны быть одинаковыми наборами юнитов с разными визуальными моделями.

Каждая фракция должна иметь собственную игровую идентичность.

Это означает, что одинаковая роль может реализовываться разными способами.

Например, Tank одной фракции может делать основной упор на большое количество HP, другой — на защиту союзников, а третьей — на восстановление и длительное нахождение в бою.

Поэтому баланс не означает:

> все юниты должны иметь одинаковые характеристики и одинаково играть против каждого противника.

Вместо этого используется принцип:

> разные фракции должны иметь собственные преимущества, недостатки и способы реализации одинаковых боевых ролей.

---

# 4. Undead

## 4.1. Основная идентичность

**Faction Identity: Attrition**

Основная идея Undead заключается в постепенном истощении противника.

Фракция должна получать преимущество не обязательно за счёт высокого моментального Damage, а благодаря:

- восстановлению;
- повторному использованию ресурсов;
- ослаблению противника;
- продолжительному давлению;
- выгоде от затяжного боя.

### Strengths

- Recovery
- Debuffs
- Sustained Pressure

### Weaknesses

- Low Mobility
- Low Burst Damage

### Основной навык игрока

**Resource & Army Management**

Игрок должен эффективно распоряжаться армией и получать максимальную ценность от затяжных сражений.

---

# 5. UND_01 — Skeleton Swordsman

**Faction:** Undead  
**Role:** Infantry  
**Attack Type:** Melee

### Unit Identity

**Disposable Frontline Infantry**

Skeleton Swordsman является относительно простым frontline-юнитом, который может использоваться для принятия Damage, задержки противника и создания пространства для более ценных юнитов.

### Strength

**Low Replacement Cost**

Потеря отдельного Skeleton Swordsman не должна быть критической для армии.

### Weakness

**Low Individual Durability**

Отдельный Skeleton Swordsman не рассчитан на длительное самостоятельное выживание.

### Ability

**Reassemble**

После смерти Skeleton Swordsman способен один раз восстановиться.

Параметры способности:

- Restore_HP: **35%**
- Delay: **4 sec**
- Max_Uses: **1**
- Trigger: **On Death**
- Target: **Self**

После первой смерти Skeleton Swordsman через 4 секунды возвращается с 35% HP.

После повторной смерти восстановление больше не происходит.

Вторая смерть считается полноценной смертью юнита и может повторно взаимодействовать с механиками, реагирующими на смерть, например с **Death Feast**.

### Design Purpose

Reassemble поддерживает общую идентичность Undead.

Skeleton Swordsman может быть слабее индивидуально, но способен создавать дополнительную ценность за счёт повторного появления на поле боя.

---

# 6. UND_02 — Bone Dragon

**Faction:** Undead  
**Role:** Tank  
**Attack Type:** Melee

### Unit Identity

**Sustained Frontline Tank**

Bone Dragon предназначен для длительного присутствия на frontline.

### Strength

**High Sustain**

Чем дольше продолжается бой и чем больше смертей происходит рядом, тем больше потенциальной ценности может получить Bone Dragon.

### Weakness

**Low Mobility**

Bone Dragon не должен легко менять позицию или быстро реагировать на действия мобильного противника.

### Ability

**Death Feast**

Bone Dragon восстанавливает часть HP, когда рядом погибает юнит.

Параметры:

- Heal_Per_Death: **3% HP**
- Trigger_Radius: **5 tiles**
- Max_Heal_Per_Second: **6% HP/s**
- Trigger: **Nearby Death**
- Target: **Self**

Ограничение Max_Heal_Per_Second необходимо для предотвращения чрезмерного восстановления при массовой одновременной гибели юнитов.

### Важное взаимодействие

Skeleton Swordsman после Reassemble способен умереть второй раз.

Эта смерть также считается полноценной и может снова активировать Death Feast.

Таким образом:

**Reassemble + Death Feast**

образуют намеренную внутреннюю synergy фракции Undead.

При этом такая synergy требует отдельной проверки баланса, поскольку большое количество Skeleton Swordsman потенциально может обеспечить Bone Dragon слишком сильным Sustain.

---

# 7. UND_03 — Spear Devil

**Faction:** Undead  
**Role:** Ranged  
**Attack Type:** Ranged

### Unit Identity

**Sustained Ranged Damage**

Spear Devil предназначен для стабильного нанесения Damage на дистанции.

### Strength

**Consistent Damage**

Юнит должен быть полезен в продолжительном бою.

### Weakness

**Low Burst**

Spear Devil не предназначен для мгновенного уничтожения противника.

### Ability

**Cursed Spear**

После каждого третьего успешного попадания Spear Devil накладывает на противника эффект снижения Damage.

Параметры:

- Trigger: **Every 3 Hits**
- Damage Reduction: **15%**
- Duration: **5 sec**
- Max Stacks: **1**
- Refresh: **Yes**

Эффект не складывается несколько раз.

Повторное срабатывание обновляет Duration.

### Design Purpose

Cursed Spear позволяет Spear Devil усиливать ценность в продолжительном бою.

Чем дольше он способен непрерывно атаковать одну цель, тем больше пользы приносит Debuff.

### Balance Risk

Время срабатывания Cursed Spear напрямую зависит от Attack Speed.

Поэтому способность требует тестирования при разных значениях Attack Speed и Attack Interval.

---

# 8. UND_04 — Witch

**Faction:** Undead  
**Role:** Support  
**Attack Type:** Ranged

### Unit Identity

**Enemy Debuff Support**

Witch специализируется на ослаблении противников.

### Strength

**Strong Debuffs**

Основная ценность Witch создаётся не собственным Damage, а уменьшением эффективности вражеских юнитов.

### Weakness

**Very Low Durability**

Witch должна быть уязвимой при неправильном позиционировании.

### Ability

**Curse**

Параметры:

- Attack Speed Reduction: **20%**
- Duration: **6 sec**
- Cooldown: **12 sec**
- Target: **Single Enemy**

Curse уменьшает базовый Attack Speed противника.

При этом Curse **не влияет** на:

- Move Speed;
- Ability Charge Time;
- Ability Cast Time;
- Cooldown;
- фиксированные внутренние интервалы способностей.

Например, Curse не изменяет фиксированный интервал **0.2 sec** между ножами Knife Barrage.

### Важное правило

В Era of Strife разделяются:

**Attack Speed ≠ Cast Speed ≠ Move Speed ≠ Cooldown**

Это разные параметры и они не должны автоматически влиять друг на друга.

---

# 9. Forest & Dark Elves

## 9.1. Основная идентичность

**Faction Identity: Precision**

Forest & Dark Elves должны получать преимущество благодаря правильному позиционированию и высокой ценности отдельных юнитов.

### Strengths

- High Mobility
- Long Range
- High Unit Value

### Weaknesses

- Low Durability
- High Punishment for Mistakes

### Основной навык игрока

**Positioning & Micro**

Игрок должен правильно выбирать позицию, момент использования способностей и направление движения.

Ошибка должна быть более опасной, чем при игре за более устойчивые фракции.

---

# 10. ELF_01 — Elven Swordsman

**Faction:** Forest & Dark Elves  
**Role:** Infantry  
**Attack Type:** Melee

### Unit Identity

**Mobile Melee Infantry**

Elven Swordsman является мобильным melee-юнитом.

### Strength

**High Mobility**

Юнит способен быстро менять позицию.

### Weakness

**Low Durability**

При неправильном использовании мобильности Elven Swordsman должен быстро терять HP.

### Ability

**Evasive Step**

Параметры:

- Dash Distance: **3 tiles**
- Dash Duration: **0.5 sec**
- Cooldown: **10 sec**
- Invulnerability: **0**
- Active Ability

Во время Evasive Step юнит быстро перемещается на небольшую дистанцию.

Способность не предоставляет Invulnerability.

Elven Swordsman также не может проходить через вражеских юнитов.

### Design Purpose

Evasive Step предназначен для:

- repositioning;
- выхода из опасной зоны;
- сокращения дистанции;
- уклонения от некоторых последовательных атак.

---

# 11. ELF_02 — Great Forest Bear

**Faction:** Forest & Dark Elves  
**Role:** Tank  
**Attack Type:** Melee

### Unit Identity

**Protective Frontline Tank**

Great Forest Bear защищает более уязвимых союзников.

### Strength

**High Durability**

Bear должен выдерживать значительный входящий Damage.

### Weakness

**Limited Damage**

Основная ценность юнита создаётся защитой, а не высоким DPS.

### Ability

**Guardian Roar**

Параметры:

- Taunt Duration: **2.5 sec**
- Radius: **3 tiles**
- Cooldown: **16 sec**
- Target: **Nearby Enemies**

Guardian Roar заставляет ближайших противников временно переключить внимание на Great Forest Bear.

### Design Purpose

Способность позволяет защищать:

- Elven Mage;
- Elven Scholar;
- другие уязвимые юниты.

---

# 12. ELF_03 — Elven Mage

**Faction:** Forest & Dark Elves  
**Role:** Ranged  
**Attack Type:** Ranged

### Unit Identity

**High-Value Ranged Damage**

Elven Mage является ценным источником дальнего Damage.

### Strength

**High Damage & Range**

При правильной защите и позиционировании Mage должен представлять серьёзную угрозу.

### Weakness

**Very Low Durability**

Попадание противника на близкую дистанцию должно быть опасным.

### Ability

**Focused Bolt**

Параметры:

- Charge: **2 sec**
- Damage Multiplier: **2.5**
- Cooldown: **12 sec**
- Cooldown Start: **On Cast Complete**
- Cancel Cooldown: **2 sec**
- Movement Allowed: **0**
- Target: **Single Enemy**

Во время Charge Elven Mage не может двигаться.

Способность может быть прервана Crowd Control.

Если способность успешно завершается, цель получает Damage с множителем **2.5×**.

Если Cast был прерван, применяется отдельный Cancel Cooldown.

### Counterplay

Bone Smash от Boneclub Troll способен прервать Focused Bolt.

Это создаёт намеренное взаимодействие между Ranged Damage и Crowd Control.

---

# 13. ELF_04 — Elven Scholar

**Faction:** Forest & Dark Elves  
**Role:** Support  
**Attack Type:** Ranged

### Unit Identity

**Protective Magic Support**

Elven Scholar специализируется на защите союзников.

### Strength

**Strong Ally Protection**

Основная ценность создаётся предотвращением входящего Damage.

### Weakness

**Low Direct Damage**

Scholar не должен конкурировать с Ranged-юнитами по собственному DPS.

### Ability

**Arcane Shield**

Параметры:

- Shield Amount: **TBD HP**
- Duration: **6 sec**
- Cooldown: **10 sec**
- Max Stacks: **1**
- Self Cast: **1**
- Target: **Single Ally / Self**

Shield может быть применён к союзнику или самому Elven Scholar.

Одновременно на цели может находиться только один такой Shield.

### Balance Risk

Особого внимания требует:

**Arcane Shield + Guardian Roar**

Great Forest Bear уже обладает высокой Durability.

Дополнительный Shield во время Taunt потенциально способен сделать его слишком сложной целью для уничтожения.

---

# 14. Horde

## 14.1. Основная идентичность

**Faction Identity: Brute Force / Pressure**

Horde должна создавать давление за счёт высокой физической силы и прямого столкновения.

### Strengths

- High HP
- Strong Melee
- Crowd Control

### Weaknesses

- Low Mobility
- Limited Range

### Основной навык игрока

**Engagement Timing**

Игроку важно правильно выбирать момент начала боя.

После успешного Engagement Horde должна создавать сильное прямое давление.

---

# 15. HOR_01 — Blade Goblin

**Faction:** Horde  
**Role:** Infantry  
**Attack Type:** Melee

### Unit Identity

**Aggressive Melee Infantry**

Blade Goblin предназначен для быстрого включения в melee-бой и создания раннего давления.

### Strength

**High Melee Damage**

После вступления в melee Blade Goblin способен значительно увеличить атакующую эффективность.

### Weakness

**Low Durability**

Юнит не рассчитан на длительное принятие Damage.

### Ability

**Blood Rush**

Параметры:

- Trigger: **First Melee Hit**
- Attack Speed Bonus: **+30%**
- Duration: **4 sec**
- Cooldown: **12 sec**
- Cooldown Start: **On Activation**
- Target: **Self**

После первого melee-попадания Blade Goblin получает временное увеличение Attack Speed.

### Design Purpose

Blood Rush создаёт короткое окно повышенного давления.

Противник может пытаться:

- пережить это окно;
- отойти;
- использовать Tank;
- направить Blood Rush на менее ценную цель.

---

# 16. HOR_02 — Stone Ogre

**Faction:** Horde  
**Role:** Tank  
**Attack Type:** Melee

### Unit Identity

**Heavy Frontline Tank**

Stone Ogre является тяжёлым frontline-юнитом.

### Strength

**Very High Durability**

Большой запас HP является одной из основных характеристик юнита.

### Weakness

**Very Low Mobility**

Stone Ogre должен испытывать трудности при необходимости быстро менять позицию.

### Ability

**Stone Skin**

Параметры:

- Damage Reduction: **40%**
- Duration: **4 sec**
- Cooldown: **16 sec**
- Cooldown Start: **On Activation**
- Movement Allowed: **0**
- Attack Allowed: **1**
- Early Cancel: **No**

Во время Stone Skin Stone Ogre значительно уменьшает получаемый Damage.

При этом:

- он не может двигаться;
- он продолжает атаковать;
- способность нельзя отменить раньше времени.

На текущем этапе Stone Skin не предоставляет отдельную Knockback Immunity.

### Design Purpose

Stone Skin усиливает роль Stone Ogre как тяжёлой неподвижной frontline-цели.

При правильном использовании способность должна позволять переживать периоды высокого входящего Damage.

---

# 17. HOR_03 — Orc Thrower

**Faction:** Horde  
**Role:** Ranged  
**Attack Type:** Ranged

### Unit Identity

**Short-Range Ranged Pressure**

Orc Thrower создаёт Ranged Pressure, но работает на меньшей дистанции, чем классический дальнобойный юнит Forest & Dark Elves.

### Strength

**High Attack Rate**

Юнит способен часто наносить Damage.

### Weakness

**Short Range**

Для эффективной атаки Orc Thrower должен находиться относительно близко к противнику.

### Ability

**Knife Barrage**

Параметры:

- Knife Count: **5**
- Damage Per Knife: **0.45× Damage**
- Knife Interval: **0.2 sec**
- Cooldown: **10 sec**
- Movement Allowed: **0**
- Target: **Single Enemy**

Максимальный Damage при попадании всех ножей:

**5 × 0.45 = 2.25× Damage**

Knife Barrage не переключается автоматически на новую цель.

Если текущая цель погибает, оставшаяся последовательность прекращается.

Если цель выходит из допустимой Attack Range, способность также прекращается.

### Важное взаимодействие с Curse

Curse уменьшает базовый Attack Speed.

Однако фиксированный:

**Knife Interval = 0.2 sec**

не является базовым Attack Speed.

Поэтому Curse не увеличивает интервал между ножами Knife Barrage.

---

# 18. HOR_04 — Boneclub Troll

**Faction:** Horde  
**Role:** Support  
**Attack Type:** Melee

### Unit Identity

**Crowd Control Support**

Boneclub Troll создаёт ценность через контроль противника.

### Strength

**Strong CC**

Юнит способен нарушать действия и позиционирование противника.

### Weakness

**Low Damage**

Boneclub Troll не предназначен для нанесения высокого DPS.

### Ability

**Bone Smash**

Параметры:

- Damage Multiplier: **0.5**
- Knockback: **2 tiles**
- Stun: **1.5 sec**
- Cooldown: **14 sec**
- Target: **Single Enemy**

Последовательность эффекта:

**Hit → Knockback → Stun**

Во время Stun цель не может:

- двигаться;
- атаковать;
- использовать способности.

Фактическая дистанция Knockback может быть меньше 2 tiles при столкновении с препятствием или другим объектом.

### Важное взаимодействие

Bone Smash способен прервать **Focused Bolt**.

Несколько Boneclub Troll потенциально способны последовательно использовать CC.

Это создаёт Balance Risk, связанный с возможным чрезмерным CC Chain.

---

# 19. Ключевые взаимодействия

В проекте предусмотрены не только отдельные способности, но и взаимодействия между ними.

## Reassemble + Death Feast

Повторная смерть Skeleton Swordsman может снова активировать Death Feast.

Это усиливает Attrition Identity Undead.

---

## Cursed Spear + Curse

Cursed Spear уменьшает Damage противника.

Curse уменьшает Attack Speed.

Если оба эффекта действуют одновременно:

**Damage Multiplier = 0.85**

**Attack Speed Multiplier = 0.80**

При мультипликативной оценке:

**0.85 × 0.80 = 0.68**

То есть потенциальный DPS противника составляет приблизительно:

**68%**

от исходного.

Это соответствует приблизительному снижению DPS на:

**32%**

Такое сочетание является потенциально сильным и требует Balance Testing.

---

# 20. Curse + Blood Rush

Blood Rush:

**+30% Attack Speed**

Curse:

**-20% Attack Speed**

Здесь возникает вопрос о порядке применения модификаторов.

При аддитивном подходе:

**100% + 30% - 20% = 110%**

Итоговый Attack Speed:

**110%**

При мультипликативном подходе:

**1.30 × 0.80 = 1.04**

Итоговый Attack Speed:

**104%**

Разница между:

**110%**

и:

**104%**

может существенно влиять на баланс.

Поэтому правило stacking должно быть единым для всей системы.

---

# 21. Guardian Roar + Arcane Shield

Great Forest Bear способен заставить противников атаковать себя через Guardian Roar.

Elven Scholar способен дополнительно защитить Bear с помощью Arcane Shield.

Таким образом возникает defensive synergy:

**Taunt + Shield**

Потенциальная проблема заключается в том, что противник может быть вынужден атаковать очень устойчивую цель, дополнительно защищённую Shield.

Это взаимодействие требует отдельного Balance Testing.

---

# 22. Evasive Step + Knife Barrage

Evasive Step может использоваться для изменения позиции Elven Swordsman.

Knife Barrage прекращается, если цель выходит из допустимой Attack Range.

Следовательно, Evasive Step потенциально способен выступать как soft counter против Knife Barrage.

Это не гарантированная полная защита, поскольку результат зависит от:

- начальной дистанции;
- Attack Range;
- момента использования Evasive Step;
- момента начала Knife Barrage.

---

# 23. Bone Smash + Focused Bolt

Focused Bolt требует:

**2 sec Charge**

и может быть прерван CC.

Bone Smash накладывает:

**Knockback + Stun**

Следовательно, Boneclub Troll способен сорвать подготовку Focused Bolt.

Это создаёт прямой counterplay между:

**Crowd Control Support**

и:

**High-Value Ranged Damage**

---

# 24. Guardian Roar + Blood Rush

Blood Rush активируется после первого melee-hit Blade Goblin.

Если Great Forest Bear через Guardian Roar заставляет Blade Goblin атаковать себя, часть усиленного окна Blood Rush может быть потрачена на Tank вместо более уязвимой цели.

Таким образом Guardian Roar способен перенаправлять offensive pressure Blade Goblin.

---

# 25. Skeleton Swordsman против Burst Windows

Благодаря своей роли Disposable Frontline Infantry Skeleton Swordsman может использоваться для принятия ценных атак противника.

Например, он потенциально способен принять на себя:

- часть Blood Rush;
- Knife Barrage;
- Bone Smash.

Даже если Skeleton Swordsman погибает, Reassemble позволяет ему вернуться в бой.

Поэтому ценность такого юнита определяется не только его собственным Damage.

---

# 26. Основные Balance Risks

В проекте зафиксирован отдельный список Balance Risks.

## RISK_001 — Debuff Synergy

Связанные юниты:

- UND_03
- UND_04

Проблема:

совместное действие Cursed Spear и Curse может слишком сильно уменьшать DPS противника.

Необходимо проверять:

- итоговое снижение DPS;
- Duration;
- доступность Debuffs;
- влияние на время выживания.

---

## RISK_002 — CC Chain

Связанный юнит:

- HOR_04

Проблема:

несколько Boneclub Troll могут создать слишком длинную последовательность Stun.

Необходимо сравнить:

- 1 Troll;
- 2 Trolls;
- 3 Trolls.

---

## RISK_003 — Defensive Synergy

Связанные юниты:

- ELF_02
- ELF_04

Проблема:

Guardian Roar + Arcane Shield потенциально способны сделать Great Forest Bear слишком сложной целью для уничтожения.

---

## RISK_004 — Sustain Synergy

Связанные юниты:

- UND_01
- UND_02

Проблема:

Reassembled Skeleton Swordsman способен умереть повторно и ещё раз активировать Death Feast.

При большом количестве Skeleton Swordsman это может создать чрезмерный Sustain.

---

## RISK_005 — Debuff Reliability

Связанный юнит:

- UND_03

Проблема:

скорость активации Cursed Spear зависит от Attack Speed.

Изменение Attack Speed может значительно изменить реальную доступность Debuff.

---

## RISK_006 — Modifier Interaction

Связанные юниты:

- UND_04
- HOR_01

Проблема:

Curse и Blood Rush одновременно изменяют Attack Speed в противоположных направлениях.

Для системы необходимо единое правило stacking.

---

# 27. Interaction Matrix

Для отслеживания важных взаимодействий используется отдельная Interaction Matrix.

Она содержит как минимум следующие типы взаимодействий:

1. Stone Skin vs Focused Bolt;
2. Evasive Step vs Knife Barrage;
3. Bone Smash vs Focused Bolt;
4. Guardian Roar vs Blood Rush;
5. Arcane Shield + Guardian Roar;
6. Reassemble + Death Feast;
7. Skeleton Swordsman vs Blood Rush;
8. Skeleton Swordsman vs Knife Barrage;
9. Skeleton Swordsman vs Bone Smash;
10. Cursed Spear + Death Feast;
11. Curse + Death Feast;
12. Cursed Spear vs Focused Bolt;
13. Cursed Spear vs Blood Rush;
14. Curse vs Blood Rush;
15. Curse vs Orc Thrower basic attacks.

Interaction Matrix используется как связующее звено между Game Design и последующим Balance Testing.

---

# 28. Разделение параметров скорости

Одним из важных правил проекта является разделение различных типов скорости.

Необходимо различать:

- Attack Speed;
- Attack Interval;
- Move Speed;
- Cast Time;
- Charge Time;
- Cooldown;
- внутренние интервалы способности.

Например:

**Curse**

влияет на базовый Attack Speed.

Но это не означает автоматическое изменение:

- Move Speed;
- Cooldown;
- Focused Bolt Charge;
- Knife Barrage Knife Interval.

Такое разделение предотвращает неоднозначное поведение игровых механик.

---

# 29. Принцип выбора характеристик для балансировки

При балансировке важно учитывать Unit Identity.

Например, Stone Ogre имеет:

**Very High Durability**

как одну из основных характеристик.

Следовательно, если Stone Ogre оказывается слишком сильным, уменьшение HP не обязательно является первым правильным решением.

Можно исследовать:

- Damage;
- DPS;
- Attack Interval;
- Stone Skin;
- Cooldown;
- продолжительность Stone Skin;
- другие параметры.

Основная идея:

> балансировка должна уменьшать проблемную силу юнита, не уничтожая его основную игровую идентичность.

Именно этот принцип позже использовался при Balance Iterations Stone Ogre.

---

# 30. Текущая модель боя

Для количественного анализа используется упрощённая deterministic 1v1 combat simulation.

В текущем базовом варианте она учитывает:

- HP;
- Damage;
- Attack Interval;
- независимое время атак каждого юнита;
- одновременные атаки;
- Win;
- Loss;
- Draw;
- Combat Time;
- Remaining HP;
- количество выполненных атак.

Оба участника могут атаковать в один момент времени.

Поэтому при совпадении времени атак возможна взаимная смерть и результат:

**Draw**

---

# 31. Ограничения текущей 1v1-модели

Базовая combat simulation намеренно упрощена.

Она пока не моделирует полностью:

- способности;
- Attack Range;
- Move Speed;
- позиционирование;
- путь движения;
- препятствия;
- командные взаимодействия;
- несколько целей;
- выбор цели;
- Focus Fire;
- Army Composition;
- экономику;
- стоимость юнитов;
- время производства;
- Player Skill.

Это не ошибка модели, а сознательное ограничение текущего этапа.

Базовая модель используется для изоляции основных числовых характеристик.

---

# 32. Почему используется упрощённая модель

Если сразу добавить все механики, становится сложнее определить причину конкретного результата.

Например, если одновременно учитывать:

- HP;
- Damage;
- Attack Speed;
- Range;
- Movement;
- Abilities;
- Positioning;
- Economy;

то после изменения результата будет сложнее определить, какой именно фактор его вызвал.

Поэтому проект развивается постепенно.

Сначала исследуются базовые характеристики.

После этого модель может расширяться дополнительными системами.

---

# 33. Принцип контролируемого эксперимента

При Balance Testing используется следующий принцип:

> между Before и After желательно изменять только тот параметр, который относится к проверяемой гипотезе.

Например, если проверяется влияние Damage Stone Ogre, остальные параметры должны оставаться неизменными.

Тогда изменение matchup можно с большей уверенностью связать именно с изменением Damage.

Этот принцип позже используется в Balance Iteration 01 и Balance Iteration 02.

---

# 34. Что означает баланс в Era of Strife

В рамках проекта баланс не определяется как:

**каждый юнит должен иметь Win Rate = 50%**

Такой подход уничтожил бы часть асимметрии.

Вместо этого анализируется совокупность факторов:

- Unit Identity;
- Faction Identity;
- Role;
- matchup;
- сильные стороны;
- слабые стороны;
- прямые counters;
- soft counters;
- synergy;
- Balance Risks;
- Combat Score;
- Win Rate;
- изменение результатов после Balance Iteration.

50% используется как аналитический reference point, но не как абсолютная цель для каждого юнита.

---

# 35. Связь Game Design и Data Analysis

Game Design отвечает на вопрос:

> Как юнит должен работать?

Data Analysis отвечает на вопрос:

> Что происходит с юнитом в текущей модели?

Balance Design соединяет эти два вопроса:

> Соответствует ли фактическое поведение задуманной роли?

Например:

Stone Ogre должен быть очень устойчивым Tank.

Если анализ показывает, что он одновременно:

- чрезвычайно устойчив;
- наносит слишком высокий Damage;
- выигрывает слишком много matchup;

то проблема может заключаться не в самой Durability, а в сочетании Durability и offensive pressure.

В таком случае изменение Damage может быть предпочтительнее изменения HP.

---

# 36. Основная цель Game Design-документа

Этот документ фиксирует исходный Design Intent проекта.

Он нужен для того, чтобы последующий Data Analysis не выполнялся без игрового контекста.

Числовые результаты должны интерпретироваться вместе с тем, каким должен быть конкретный юнит.

Поэтому дальнейшая последовательность проекта выглядит так:

**Game Design**

↓

**Structured Balance Data**

↓

**Combat Simulation**

↓

**Balance Analysis**

↓

**Balance Hypothesis**

↓

**Balance Iteration**

↓

**Comparison**

↓

**Design Decision**

Подробная методология анализа описана в:

`02_balance_methodology.md`

История проведённых изменений описана в:

`03_balance_iterations.md`

Итоговые выводы собраны в:

`04_final_findings.md`