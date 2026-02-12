#!/usr/bin/env python3
"""
5etools 完整数据归档脚本
将5etools所有数据分类整理并固化到skill中
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# 路径配置
SOURCE_DIR = Path("/Users/sid/.openclaw/workspace/5etools-data/5etools-src-main/data")
OUTPUT_DIR = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/data/5etools")

def ensure_dirs():
    """确保目录结构存在"""
    dirs = [
        "core/rules",
        "core/monsters", 
        "core/spells",
        "core/items",
        "core/characters",
        "modules/lmop",
        "indexes"
    ]
    for d in dirs:
        (OUTPUT_DIR / d).mkdir(parents=True, exist_ok=True)

def clean_text(text) -> str:
    """清理5etools标记"""
    if not text:
        return ""
    if isinstance(text, list):
        return "\n".join(clean_text(t) for t in text)
    if not isinstance(text, str):
        return str(text)
    
    # 清理各种5etools标记
    text = re.sub(r'\{@\w+\s+([^}|]+)(?:\|[^}]+)?\}', r'\1', text)
    text = re.sub(r'\{@h\}', '命中：', text)
    text = re.sub(r'\{@atk\s+\w+\}', '', text)
    text = re.sub(r'\{@hit\s+([^}]+)\}', r'+\1', text)
    text = re.sub(r'\{@damage\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@dc\s+([^}]+)\}', r'DC\1', text)
    text = re.sub(r'\{@d20\}', 'd20', text)
    text = re.sub(r'\{@condition\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@spell\s+([^}]+)\}', r'《\1》', text)
    text = re.sub(r'\{@item\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@action\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@skill\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@sense\s+([^}]+)\}', r'\1', text)
    
    return text.strip()

def parse_entries(entries) -> str:
    """解析entries结构"""
    if not entries:
        return ""
    if isinstance(entries, str):
        return clean_text(entries)
    if isinstance(entries, list):
        return "\n".join(parse_entries(e) for e in entries)
    if isinstance(entries, dict):
        etype = entries.get("type", "")
        if etype == "list":
            items = entries.get("items", [])
            return "\n".join(f"• {clean_text(item)}" for item in items)
        elif etype == "entries":
            name = entries.get("name", "")
            content = parse_entries(entries.get("entries", []))
            return f"**{name}**：{content}" if name else content
        elif etype == "table":
            return f"[表格: {entries.get('caption', '')}]"
        else:
            return parse_entries(entries.get("entries", []))
    return ""

# ============ 核心规则数据 ============

def extract_conditions() -> List[Dict]:
    """提取状态条件"""
    with open(SOURCE_DIR / "conditionsdiseases.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    conditions = []
    condition_names = {
        "Blinded": "目盲", "Charmed": "魅惑", "Deafened": "耳聋",
        "Exhaustion": "力竭", "Frightened": "恐慌", "Grappled": "被擒抱",
        "Incapacitated": "失能", "Invisible": "隐形", "Paralyzed": "麻痹",
        "Petrified": "石化", "Poisoned": "中毒", "Prone": "倒地",
        "Restrained": "束缚", "Stunned": "震慑", "Unconscious": "昏迷"
    }
    
    for cond in data.get("condition", []):
        if cond.get("source") not in ["PHB", "XPHB"]:
            continue
        name_en = cond.get("name", "")
        conditions.append({
            "name_en": name_en,
            "name_cn": condition_names.get(name_en, name_en),
            "source": cond.get("source", ""),
            "page": cond.get("page", 0),
            "description": parse_entries(cond.get("entries", []))
        })
    
    # 去重
    seen = {}
    for c in conditions:
        if c["name_en"] not in seen or c["source"] == "XPHB":
            seen[c["name_en"]] = c
    
    return list(seen.values())

def extract_actions() -> List[Dict]:
    """提取战斗动作"""
    with open(SOURCE_DIR / "actions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    actions = []
    action_names = {
        "Attack": "攻击", "Cast a Spell": "施法", "Dash": "疾走",
        "Disengage": "撤离", "Dodge": "闪避", "Help": "协助",
        "Hide": "躲藏", "Ready": "预备", "Search": "搜索",
        "Use an Object": "使用物品", "Grapple": "擒抱", "Shove": "推撞",
        "Disarm": "缴械", "Mark": "标记"
    }
    
    for action in data.get("action", []):
        if action.get("source") not in ["PHB", "XPHB", "DMG"]:
            continue
        name_en = action.get("name", "")
        actions.append({
            "name_en": name_en,
            "name_cn": action_names.get(name_en, name_en),
            "source": action.get("source", ""),
            "time": action.get("time", []),
            "description": parse_entries(action.get("entries", []))
        })
    
    return actions

def extract_spells() -> List[Dict]:
    """提取法术"""
    spells = []
    school_map = {
        "A": "防护", "C": "召唤", "D": "预言", "E": "惑控",
        "V": "塑能", "I": "幻术", "N": "死灵", "T": "变化"
    }
    
    # 读取所有法术文件
    spells_dir = SOURCE_DIR / "spells"
    for json_file in sorted(spells_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for spell in data.get("spell", []):
                # 获取成分
                comp = spell.get("components", {})
                comp_parts = []
                if comp.get("v"): comp_parts.append("V")
                if comp.get("s"): comp_parts.append("S")
                if comp.get("m"):
                    m = comp["m"]
                    if isinstance(m, str):
                        comp_parts.append(f"M({m})")
                    elif isinstance(m, dict):
                        comp_parts.append(f"M({m.get('text', '')})")
                
                spells.append({
                    "name_en": spell.get("name", ""),
                    "level": spell.get("level", 0),
                    "school": school_map.get(spell.get("school", ""), spell.get("school", "")),
                    "cast_time": spell.get("time", []),
                    "range": spell.get("range", {}),
                    "components": ", ".join(comp_parts),
                    "duration": spell.get("duration", []),
                    "ritual": spell.get("meta", {}).get("ritual", False),
                    "description": parse_entries(spell.get("entries", [])),
                    "higher_level": parse_entries(spell.get("entriesHigherLevel", [])),
                    "source": spell.get("source", "")
                })
        except Exception as e:
            print(f"  错误处理 {json_file.name}: {e}")
    
    # 去重，优先XPHB
    seen = {}
    for s in spells:
        key = s["name_en"]
        if key not in seen or s["source"] == "XPHB":
            seen[key] = s
    
    return list(seen.values())

def extract_feats() -> List[Dict]:
    """提取专长"""
    with open(SOURCE_DIR / "feats.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    feats = []
    for feat in data.get("feat", []):
        if feat.get("source") not in ["PHB", "XPHB"]:
            continue
        
        # 解析先决条件
        prereq = feat.get("prerequisite", [])
        prereq_str = ""
        if prereq:
            prereq_parts = []
            for p in prereq:
                if isinstance(p, dict):
                    if "ability" in p:
                        for a in p["ability"]:
                            if isinstance(a, dict):
                                for k, v in a.items():
                                    prereq_parts.append(f"{k} {v}")
                    elif "spellcasting" in p:
                        prereq_parts.append("能够施法")
            prereq_str = ", ".join(prereq_parts)
        
        feats.append({
            "name_en": feat.get("name", ""),
            "prerequisite": prereq_str,
            "description": parse_entries(feat.get("entries", [])),
            "source": feat.get("source", "")
        })
    
    return feats

def extract_races() -> List[Dict]:
    """提取种族"""
    with open(SOURCE_DIR / "races.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    races = []
    for race in data.get("race", []):
        races.append({
            "name": race.get("name", ""),
            "source": race.get("source", ""),
            "size": race.get("size", []),
            "speed": race.get("speed", {}),
            "ability": race.get("ability", {}),
            "entries": parse_entries(race.get("entries", []))
        })
    
    return races

def extract_backgrounds() -> List[Dict]:
    """提取背景"""
    with open(SOURCE_DIR / "backgrounds.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    backgrounds = []
    for bg in data.get("background", []):
        backgrounds.append({
            "name": bg.get("name", ""),
            "source": bg.get("source", ""),
            "skill_proficiencies": bg.get("skillProficiencies", []),
            "entries": parse_entries(bg.get("entries", []))
        })
    
    return backgrounds

def extract_classes() -> List[Dict]:
    """提取职业"""
    classes = []
    class_dir = SOURCE_DIR / "class"
    
    for json_file in sorted(class_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for cls in data.get("class", []):
                classes.append({
                    "name": cls.get("name", ""),
                    "source": cls.get("source", ""),
                    "hd": cls.get("hd", {}),
                    "proficiency": cls.get("proficiency", []),
                    "spellcasting": cls.get("spellcastingAbility", ""),
                    "entries": parse_entries(cls.get("entries", []))
                })
        except Exception as e:
            print(f"  错误处理 {json_file.name}: {e}")
    
    return classes

# ============ 怪物数据 ============

def extract_monsters() -> List[Dict]:
    """提取所有怪物"""
    monsters = []
    bestiary_dir = SOURCE_DIR / "bestiary"
    
    for json_file in sorted(bestiary_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for monster in data.get("monster", []):
                # 基础信息
                size_map = {"T": "微型", "S": "小型", "M": "中型", "L": "大型", "H": "巨型", "G": "超巨型"}
                size = size_map.get(monster.get("size", ["M"])[0], "中型")
                
                # 类型
                type_info = monster.get("type", {})
                if isinstance(type_info, dict):
                    type_str = type_info.get("type", "")
                else:
                    type_str = type_info
                type_map = {
                    "aberration": "异怪", "beast": "野兽", "celestial": "天界生物",
                    "construct": "构装生物", "dragon": "龙", "elemental": "元素生物",
                    "fey": "精类", "fiend": "邪魔", "giant": "巨人",
                    "humanoid": "类人生物", "monstrosity": "怪兽", "ooze": "泥怪",
                    "plant": "植物", "undead": "亡灵"
                }
                type_cn = type_map.get(type_str, type_str)
                
                # CR
                cr = monster.get("cr", "0")
                if isinstance(cr, dict):
                    cr = cr.get("cr", "0")
                
                monsters.append({
                    "name": monster.get("name", ""),
                    "source": monster.get("source", ""),
                    "size": size,
                    "type": type_cn,
                    "ac": monster.get("ac", []),
                    "hp": monster.get("hp", {}),
                    "speed": monster.get("speed", {}),
                    "abilities": {
                        "str": monster.get("str", 10),
                        "dex": monster.get("dex", 10),
                        "con": monster.get("con", 10),
                        "int": monster.get("int", 10),
                        "wis": monster.get("wis", 10),
                        "cha": monster.get("cha", 10)
                    },
                    "cr": str(cr),
                    "traits": parse_entries(monster.get("trait", [])),
                    "actions": parse_entries(monster.get("action", [])),
                    "legendary": parse_entries(monster.get("legendary", []))
                })
        except Exception as e:
            print(f"  错误处理 {json_file.name}: {e}")
    
    return monsters

# ============ 物品数据 ============

def extract_items() -> List[Dict]:
    """提取物品装备"""
    with open(SOURCE_DIR / "items.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = []
    for item in data.get("item", []):
        items.append({
            "name": item.get("name", ""),
            "source": item.get("source", ""),
            "type": item.get("type", ""),
            "rarity": item.get("rarity", ""),
            "requires_attunement": item.get("reqAttune", False),
            "value": item.get("value", ""),
            "weight": item.get("weight", 0),
            "entries": parse_entries(item.get("entries", []))
        })
    
    return items

# ============ 保存数据 ============

def save_json(data: List[Dict], filename: str):
    """保存JSON文件"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  保存: {filepath} ({len(data)} 条记录)")

def generate_index():
    """生成索引文件"""
    index = {
        "version": "5etools-2024",
        "categories": {
            "conditions": {"file": "core/rules/conditions.json", "count": len(extract_conditions())},
            "actions": {"file": "core/rules/actions.json", "count": len(extract_actions())},
            "spells": {"file": "core/spells/spells.json", "count": len(extract_spells())},
            "feats": {"file": "core/characters/feats.json", "count": len(extract_feats())},
            "races": {"file": "core/characters/races.json", "count": len(extract_races())},
            "backgrounds": {"file": "core/characters/backgrounds.json", "count": len(extract_backgrounds())},
            "classes": {"file": "core/characters/classes.json", "count": len(extract_classes())},
            "monsters": {"file": "core/monsters/monsters.json", "count": len(extract_monsters())},
            "items": {"file": "core/items/items.json", "count": len(extract_items())}
        }
    }
    
    with open(OUTPUT_DIR / "indexes/master_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\n生成索引: {OUTPUT_DIR / 'indexes/master_index.json'}")

def main():
    print("=" * 60)
    print("5etools 完整数据归档")
    print("=" * 60)
    print()
    
    ensure_dirs()
    
    # 核心规则
    print("【核心规则数据】")
    save_json(extract_conditions(), "core/rules/conditions.json")
    save_json(extract_actions(), "core/rules/actions.json")
    save_json(extract_spells(), "core/spells/spells.json")
    save_json(extract_feats(), "core/characters/feats.json")
    save_json(extract_races(), "core/characters/races.json")
    save_json(extract_backgrounds(), "core/characters/backgrounds.json")
    save_json(extract_classes(), "core/characters/classes.json")
    
    # 怪物和物品
    print("\n【怪物和物品数据】")
    save_json(extract_monsters(), "core/monsters/monsters.json")
    save_json(extract_items(), "core/items/items.json")
    
    # 生成索引
    print("\n【生成索引】")
    generate_index()
    
    print()
    print("=" * 60)
    print("归档完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
