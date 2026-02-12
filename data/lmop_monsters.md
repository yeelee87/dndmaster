# 凡戴尔的失落矿坑 - 怪物数据

> 本文档包含模组《凡戴尔的失落矿坑》中的所有怪物和NPC数据
> 数据来源: 5etools

---

## Ash Zombie (Ash Zombie)

*中型 亡灵，中立 邪恶*

**AC**: 8  **HP**: 22 (3d8 + 9)  **速度**: 行走 20尺  **CR**: 1/4  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 13 (+1) | 6 (-2) | 16 (+3) | 3 (-4) | 6 (-2) | 5 (-3) |

**豁免**: WIS +0  **免疫**: poison  **状态免疫**: poisoned  **感官**: darkvision 60 ft.  **被动感知**: 8  **语言**: understands all languages it spoke in life but can't speak  
### 特性

**Undead Fortitude**: If damage reduces the zombie to 0 hit points, it must make a Constitution saving throw with a DC of 5+the damage taken, unless the damage is radiant or from a critical hit. On a success, the zombie drops to 1 hit point instead.

**Ash Puff**: The first time the zombie takes damage, any living creature within 5 feet of the zombie must succeed on a {@dc 10} Constitution saving throw or gain disadvantage on attack rolls, saving throws, and ability checks for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on it early with a successful save.

### 动作

**Slam**: {@atk mw} {@hit 3} to hit, reach 5 ft., one target. {@h}4 ({@damage 1d6 + 1}) bludgeoning damage.

---

## 邪恶法师 (Evil Mage)

*中型 类人生物 (human)，守序 邪恶*

**AC**: 12  **HP**: 22 (5d8)  **速度**: 行走 30尺  **CR**: 1  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 9 (-1) | 14 (+2) | 11 (+0) | 17 (+3) | 12 (+1) | 11 (+0) |

**豁免**: INT +5, WIS +3  **技能**: Arcana +5, History +5  **被动感知**: 11  **语言**: Common, Draconic, Dwarvish, Elvish  
### 法术施放

**Spellcasting**: The mage is a 4th-level spellcaster that uses Intelligence as its spellcasting ability (spell save {@dc 13}; {@hit 5} to hit with spell attacks). The mage knows the following spells from the wizard's spell list:

### 动作

**Quarterstaff**: {@atk mw} {@hit 1} to hit, reach 5 ft., one target. {@h}3 ({@damage 1d8 - 1}) bludgeoning damage.

---

## 冈德伦·寻石者 (Gundren Rockseeker) [NPC] [有名角色]

*中型 ，无阵营*

**AC**:   **HP**: 0 ()  **速度**: 行走 30尺  **CR**: 0  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) |

**被动感知**: 10  
---

## 幽灵莫梅斯克 (Mormesk the Wraith) [NPC] [有名角色]

*中型 亡灵，中立 邪恶*

**AC**: 13  **HP**: 45 (6d8 + 18)  **速度**: 行走 0尺，飞行 60尺  **CR**: 3  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 6 (-2) | 16 (+3) | 16 (+3) | 12 (+1) | 14 (+2) | 15 (+2) |

**抗性**: acid, cold, fire, lightning, thunder, {'resist': ['bludgeoning', 'piercing', 'slashing'], 'note': "from nonmagical attacks that aren't silvered", 'cond': True}  **免疫**: necrotic, poison  **状态免疫**: charmed, grappled, paralyzed, petrified, poisoned, prone, restrained  **感官**: darkvision 60 ft.  **被动感知**: 12  **语言**: Common, Infernal  
### 特性

**Incorporeal Movement**: The wraith can move through an object or another creature, but can't stop there.

**Sunlight Sensitivity**: While in sunlight, the wraith has disadvantage on attack rolls and on Wisdom ({@skill Perception}) checks that rely on sight.

### 动作

**Life Drain**: {@atk mw} {@hit 5} to hit, reach 5 ft., one creature. {@h}16 ({@damage 3d8 + 3}) necrotic damage, and the target must succeed on a {@dc 13} Constitution saving throw or its hit point maximum is reduced by an amount equal to the damage taken. If this attack reduces the target's hit point maximum to 0, the target dies. This reduction to the target's hit point maximum lasts until the target finishes a long rest.

---

## 黑蜘蛛涅兹纳尔 (Nezznar the Black Spider) [NPC] [有名角色]

*中型 类人生物 (elf)，中立 邪恶*

**AC**: 11  **HP**: 27 (6d8)  **速度**: 行走 30尺  **CR**: 2  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 9 (-1) | 13 (+1) | 10 (+0) | 16 (+3) | 14 (+2) | 13 (+1) |

**豁免**: INT +5, WIS +4  **技能**: Arcana +5, Perception +4, Stealth +3  **感官**: darkvision 120 ft.  **被动感知**: 14  **语言**: Elvish, Undercommon  
### 特性

**Special Equipment**: Nezznar has a {@item spider staff|LMoP}.

**Fey Ancestry**: Nezznar has advantage on saving throws against being {@condition charmed}, and magic can't put him to sleep.

**Sunlight Sensitivity**: Nezznar has disadvantage on attack rolls when he or his target is in sunlight.

### 法术施放

**Innate Spellcasting**: Nezznar can innately cast the following spells, requiring no material components:

**Spellcasting**: Nezznar is a 4th-level spellcaster that uses Intelligence as his spellcasting ability (spell save {@dc 13}; {@hit 5} to hit with spell attacks). Nezznar has the following spells prepared from the wizard's spell list:

### 动作

**Spider Staff**: {@atk mw} {@hit 1} to hit, reach 5 ft., one target. {@h}2 ({@damage 1d6 - 1}) bludgeoning damage plus 3 ({@damage 1d6}) poison damage.

---

## Nundro Rockseeker (Nundro Rockseeker) [NPC] [有名角色]

*中型 ，无阵营*

**AC**:   **HP**: 0 ()  **速度**: 行走 30尺  **CR**: 0  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) |

**被动感知**: 10  
---

## Redbrand Ruffian (Redbrand Ruffian)

*中型 类人生物 (human)，中立 邪恶*

**AC**: 14  **HP**: 16 (3d8 + 3)  **速度**: 行走 30尺  **CR**: 1/2  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 11 (+0) | 14 (+2) | 12 (+1) | 9 (-1) | 9 (-1) | 11 (+0) |

**技能**: Intimidation +2  **被动感知**: 9  **语言**: Common  
### 动作

**Multiattack**: The ruffian makes two melee attacks.

**Shortsword**: {@atk mw} {@hit 4} to hit, reach 5 ft., one target. {@h}5 ({@damage 1d6 + 2}) piercing damage.

---

## 西尔达·哈尔温特 (Sildar Hallwinter) [NPC] [有名角色]

*中型 类人生物 (human)，中立 善良*

**AC**: 16  **HP**: 27 (5d8 + 5)  **速度**: 行走 30尺  **CR**: 1  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 13 (+1) | 10 (+0) | 12 (+1) | 10 (+0) | 11 (+0) | 10 (+0) |

**豁免**: STR +3, CON +3  **技能**: Perception +2  **被动感知**: 12  **语言**: Common  
### 动作

**Multiattack**: Sildar makes two melee attacks.

**Longsword**: {@atk mw} {@hit 3} to hit, reach 5 ft., one target. {@h}5 ({@damage 1d8 + 1}) slashing damage.

**Heavy Crossbow**: {@atk rw} {@hit 2} to hit, range 100/400 ft., one target. {@h}5 ({@damage 1d10}) piercing damage.

---

## 毒牙 (Venomfang) [NPC] [有名角色]

*中型 ，无阵营*

**AC**:   **HP**: 0 ()  **速度**: 行走 30尺  **CR**: 0  
### 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:----:|:----:|:----:|:----:|:----:|:----:|
| 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) | 10 (+0) |

**被动感知**: 10  
---

