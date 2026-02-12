# 5etools 完整数据归档清单

> 数据提取时间: 2026-02-11
> 数据来源: https://github.com/5etools-mirror-3/5etools-src/
> 总大小: 7.1 MB

---

## 📁 目录结构

```
data/5etools/
├── core/
│   ├── rules/          # 核心规则
│   ├── monsters/       # 怪物数据
│   ├── spells/         # 法术数据
│   ├── items/          # 物品装备
│   └── characters/     # 角色创建
└── indexes/            # 索引文件
```

---

## 📊 数据详情

### 核心规则 (Core Rules)

| 文件 | 大小 | 记录数 | 内容 |
|------|------|--------|------|
| `conditions.json` | 7.7 KB | 15 | 状态条件（目盲、魅惑、力竭等） |
| `actions.json` | 34 KB | 46 | 战斗动作（攻击、疾走、擒抱等） |

**总计**: 61 条核心规则数据

---

### 角色创建 (Characters)

| 文件 | 大小 | 记录数 | 内容 |
|------|------|--------|------|
| `races.json` | 189 KB | 158 | 所有种族及亚种 |
| `classes.json` | 7.4 KB | 42 | 所有职业及子职 |
| `backgrounds.json` | 251 KB | 175 | 所有背景 |
| `feats.json` | 58 KB | 119 | 所有专长 |

**总计**: 494 条角色创建数据

---

### 法术 (Spells)

| 文件 | 大小 | 记录数 | 内容 |
|------|------|--------|------|
| `spells.json` | 681 KB | 557 | 0-9环全部法术 |

**包含**: 戏法、1-9环法术、仪式法术

---

### 怪物 (Monsters)

| 文件 | 大小 | 记录数 | 内容 |
|------|------|--------|------|
| `monsters.json` | 4.2 MB | 4,085 | 所有怪物数据卡 |

**包含**: MM、DMG、模组怪物等

---

### 物品装备 (Items)

| 文件 | 大小 | 记录数 | 内容 |
|------|------|--------|------|
| `items.json` | 1.7 MB | 2,451 | 所有物品装备 |

**包含**: 武器、护甲、魔法物品、药水等

---

## 📈 数据统计

| 类别 | 数量 |
|------|------|
| 状态条件 | 15 |
| 战斗动作 | 46 |
| 法术 | 557 |
| 专长 | 119 |
| 种族 | 158 |
| 背景 | 175 |
| 职业/子职 | 42 |
| 怪物 | 4,085 |
| 物品 | 2,451 |
| **总计** | **7,649** |

---

## 🔍 索引文件

`indexes/master_index.json` - 主索引文件，包含所有数据文件的位置和统计信息

---

## 📝 数据格式

所有数据均为JSON格式，每条记录包含完整的游戏数据，例如：

### 法术示例
```json
{
  "name_en": "Fireball",
  "level": 3,
  "school": "塑能",
  "cast_time": [...],
  "range": {...},
  "components": "V, S, M(蝙蝠粪和硫磺)",
  "duration": [...],
  "ritual": false,
  "description": "...",
  "higher_level": "..."
}
```

### 怪物示例
```json
{
  "name": "Goblin",
  "size": "小型",
  "type": "类人生物",
  "ac": [...],
  "hp": {...},
  "speed": {...},
  "abilities": {...},
  "cr": "1/4",
  "traits": "...",
  "actions": "..."
}
```

---

## 🔄 更新说明

如需更新数据：
1. 重新下载5etools数据仓库
2. 运行 `scripts/archive_5etools.py`
3. 数据将自动重新提取并归档

---

## 📚 关联文件

- **玩家手册**: `references/core-rules/phb_2014.md`
- **怪物手册**: `references/core-rules/mm_2014_full.md`
- **城主指南**: `references/core-rules/dmg_2014.md`
