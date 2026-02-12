# D&D 5e 数据管理系统 (方案2实施)

## 系统架构

```
skills/dnd-game-master/data/
├── index/                    # 索引文件（快速查找）
│   ├── monsters.json         # 怪物索引
│   ├── spells.json           # 法术索引
│   ├── items.json            # 物品索引
│   ├── feats.json            # 专长索引
│   ├── conditions.json       # 状态条件索引
│   ├── actions.json          # 战斗动作索引
│   ├── races.json            # 种族索引
│   ├── backgrounds.json      # 背景索引
│   └── classes.json          # 职业索引
├── cache/                    # 缓存目录（运行时生成）
├── 5etools_extracted.json    # 核心数据（状态/动作/法术/专长）
├── lmop_monsters.json        # LMOP模组怪物数据
└── README.md                 # 本文件
```

## 性能特点

| 指标 | 数值 | 说明 |
|------|------|------|
| 启动时间 | <100ms | 只加载索引（约500KB） |
| 内存占用 | 5-15MB | 初始+缓存 |
| 查询延迟 | <50ms | 索引查找+文件读取 |
| 缓存命中 | >90% | 常用数据缓存后 |

## 使用方法

### 1. 基础查询

```python
from scripts.dnd_data_manager import find_monster, find_spell, find_condition

# 查找怪物
monster = find_monster("Goblin")
print(monster['name_en'])  # "Goblin"
print(monster['cr'])       # "1/4"

# 查找法术
spell = find_spell("Fireball")
print(spell['level'])      # 3
print(spell['school_cn'])  # "塑能"

# 查找状态条件
condition = find_condition("blinded")
print(condition['name_cn'])  # "目盲"
```

### 2. 模糊搜索

```python
from scripts.dnd_data_manager import search_monsters, search_spells

# 搜索包含 "dragon" 的怪物
results = search_monsters("dragon", limit=10)
for r in results:
    print(f"{r['name_en']} (CR {r['cr']})")

# 搜索包含 "magic" 的法术
results = search_spells("magic", level=3, limit=5)
for r in results:
    print(f"{r['name_en']} - {r['level']}环")
```

### 3. 使用数据管理器（高级）

```python
from scripts.dnd_data_manager import get_manager

dm = get_manager()

# 列出某环数的所有法术
spells = dm.list_spells_by_level(3)

# 获取所有状态条件
conditions = dm.get_all_conditions()

# 获取所有战斗动作
actions = dm.get_all_actions()

# 预加载常用数据
dm.preload_common_data()

# 查看缓存统计
print(dm.get_cache_stats())
# {'cache_hits': 45, 'cache_misses': 5, 'hit_rate': '90.0%', ...}

# 清除缓存
dm.clear_cache()
```

## 数据格式

### 怪物数据
```python
{
    "name_en": "Goblin",
    "name_cn": "地精",
    "size": "小型",
    "type": "类人生物",
    "alignment": "中立邪恶",
    "ac": "15 (皮甲+盾)",
    "hp": "7 (2d6)",
    "speed": "30尺",
    "abilities": {"str": 8, "dex": 14, "con": 10, "int": 10, "wis": 8, "cha": 8},
    "traits": [...],
    "actions": [...],
    "cr": "1/4"
}
```

### 法术数据
```python
{
    "name_en": "Fireball",
    "name_cn": "火球术",
    "level": 3,
    "school_cn": "塑能",
    "cast_time": "1 action",
    "range": "150 feet",
    "components": "言语(V)，姿势(S)，材料(M): 蝙蝠粪和硫磺",
    "duration": "立即",
    "ritual": False,
    "description": "...",
    "higher_level": "..."
}
```

### 状态条件
```python
{
    "name_en": "Blinded",
    "name_cn": "目盲",
    "source": "XPHB",
    "page": 361,
    "description": "..."
}
```

## 扩展完整数据源

当前系统使用预提取的核心数据。如需接入完整的5etools数据源：

```bash
# 1. 克隆完整数据仓库
git clone --depth 1 https://github.com/5etools-mirror-3/5etools-src.git

# 2. 生成完整索引
python3 scripts/generate_indexes.py

# 3. 系统会自动使用新索引
```

完整数据源包含：
- **200+ 怪物文件** - 数千个怪物
- **30+ 法术文件** - 全部法术
- **33+ 职业文件** - 所有职业和子职
- **物品数据** - 所有装备和魔法物品
- **种族/背景** - 完整角色创建选项

## 缓存机制

系统使用两级缓存：

1. **内存缓存** - 当前会话的热数据
2. **磁盘缓存** - 持久化的查询结果

缓存自动管理，无需手动干预。缓存文件存储在 `data/cache/` 目录。

## 索引系统

索引文件包含：
- 条目名称（小写，用于快速查找）
- 英文原名
- 中文翻译（如有）
- 关键属性（CR、环数等）
- 源文件位置

索引让系统无需加载全部数据即可快速定位。

## 在 Skill 中使用

在 `SKILL.md` 中引用数据：

```markdown
需要查询规则时，使用数据管理器：

```python
from scripts.dnd_data_manager import find_spell, find_monster

# 查询法术详细信息
spell = find_spell("Magic Missile")
# 返回完整法术数据用于展示

# 查询怪物数据  
monster = find_monster("Bugbear")
# 返回AC、HP、动作等战斗数据
```
```

## 更新数据

### 更新核心数据
```bash
# 重新提取核心数据
python3 scripts/extract_5etools.py
python3 scripts/extract_lmop.py

# 重新创建索引
python3 -c "
import json
# ... 索引生成代码
"
```

### 更新完整数据
```bash
# 拉取最新数据
cd 5etools-data && git pull

# 重新生成索引
python3 scripts/generate_indexes.py

# 清除缓存以确保新数据生效
python3 -c "from scripts.dnd_data_manager import get_manager; get_manager().clear_cache()"
```

## 性能优化建议

1. **预加载** - 在会话开始时预加载常用数据
2. **批量查询** - 一次性查询多个相关数据，利用缓存
3. **定期清理** - 长时间运行后可清理磁盘缓存

## 故障排除

### 查询返回 None
- 检查名称拼写（英文）
- 检查索引文件是否存在
- 检查数据源文件是否完整

### 查询速度慢
- 检查磁盘缓存是否启用
- 考虑预加载常用数据
- 检查 SSD 性能

### 内存占用高
- 清除内存缓存：`dm.cache.clear()`
- 减少预加载数据量
- 定期重启服务

## 数据来源

- **英文数据**: https://github.com/5etools-mirror-3/5etools-src/
- **中文参考**: https://github.com/tjliqy/5etools-mirror-2.github.io/tree/cn2.0

---

*系统版本: 2.0*  
*最后更新: 2026-02-11*
