#!/usr/bin/env python3
"""
5etools 数据提取和翻译脚本
用于将 5etools 的 JSON 数据提取并翻译成中文，供 DND skill 使用
"""

import json
import os
import re
from pathlib import Path

# 数据目录
DATA_DIR = Path("/Users/sid/.openclaw/workspace/5etools-src-temp/data")
OUTPUT_DIR = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/data")

# 法术学派映射
SCHOOL_MAP = {
    "A": "防护", "Abjuration": "防护",
    "C": "召唤", "Conjuration": "召唤",
    "D": "预言", "Divination": "预言",
    "E": "惑控", "Enchantment": "惑控",
    "V": "塑能", "Evocation": "塑能",
    "I": "幻术", "Illusion": "幻术",
    "N": "死灵", "Necromancy": "死灵",
    "T": "变化", "Transmutation": "变化"
}

# 属性映射
ABILITY_MAP = {
    "strength": "力量", "str": "力量",
    "dexterity": "敏捷", "dex": "敏捷",
    "constitution": "体质", "con": "体质",
    "intelligence": "智力", "int": "智力",
    "wisdom": "感知", "wis": "感知",
    "charisma": "魅力", "cha": "魅力"
}

# 条件状态映射
CONDITION_MAP = {
    "Blinded": "目盲",
    "Charmed": "魅惑",
    "Deafened": "耳聋",
    "Exhaustion": "力竭",
    "Frightened": "恐慌",
    "Grappled": "被擒抱",
    "Incapacitated": "失能",
    "Invisible": "隐形",
    "Paralyzed": "麻痹",
    "Petrified": "石化",
    "Poisoned": "中毒",
    "Prone": "倒地",
    "Restrained": "束缚",
    "Stunned": "震慑",
    "Unconscious": "昏迷"
}

# 动作名称映射
ACTION_MAP = {
    "Attack": "攻击",
    "Cast a Spell": "施法",
    "Dash": "疾走",
    "Disengage": "撤离",
    "Dodge": "闪避",
    "Help": "协助",
    "Hide": "躲藏",
    "Ready": "预备",
    "Search": "搜索",
    "Use an Object": "使用物品",
    "Grapple": "擒抱",
    "Shove": "推撞",
    "Disarm": "缴械",
    "Mark": "标记",
    "Climb onto a Bigger Creature": "攀爬大型生物",
    "Overrun": "冲越",
    "Tumble": "翻滚",
    "Activate an Item": "激活物品",
    "Mind Blind": "心灵致盲"
}

def clean_text(text):
    """清理文本，移除 5etools 标记"""
    if not text:
        return ""
    
    # 处理列表
    if isinstance(text, list):
        return "\n".join(clean_text(t) for t in text)
    
    if not isinstance(text, str):
        return str(text)
    
    # 移除 {@...} 标记
    text = re.sub(r'\{@\w+\s+([^}|]+)(?:\|[^}]+)?\}', r'\1', text)
    text = re.sub(r'\{@h\}', '命中：', text)
    text = re.sub(r'\{@atk\s+\w+\}', '', text)
    text = re.sub(r'\{@hit\s+([^}]+)\}', r'攻击加值+\1', text)
    text = re.sub(r'\{@damage\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@dc\s+([^}]+)\}', r'DC\1', text)
    text = re.sub(r'\{@d20\}', 'd20', text)
    text = re.sub(r'\{@condition\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@spell\s+([^}]+)\}', r'《\1》', text)
    text = re.sub(r'\{@item\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@action\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@skill\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@sense\s+([^}]+)\}', r'\1', text)
    
    return text

def parse_entries(entries, depth=0):
    """解析 entries 结构，返回文本"""
    if not entries:
        return ""
    
    if isinstance(entries, str):
        return clean_text(entries)
    
    if isinstance(entries, list):
        result = []
        for entry in entries:
            parsed = parse_entries(entry, depth)
            if parsed:
                result.append(parsed)
        return "\n".join(result)
    
    if isinstance(entries, dict):
        etype = entries.get("type", "")
        
        if etype == "list":
            items = entries.get("items", [])
            return "\n".join(f"• {clean_text(item)}" for item in items)
        
        elif etype == "entries":
            name = entries.get("name", "")
            content = parse_entries(entries.get("entries", []), depth + 1)
            if name:
                return f"**{name}**：{content}"
            return content
        
        elif etype == "quote":
            text = clean_text(entries.get("entries", []))
            by = entries.get("by", "")
            return f"> {text}" + (f"\n> —— {by}" if by else "")
        
        elif etype == "table":
            # 简化表格处理
            caption = entries.get("caption", "")
            return f"[表格: {caption}]"
        
        else:
            # 默认处理
            content = entries.get("entries", entries.get("items", []))
            return parse_entries(content, depth)
    
    return ""

def extract_conditions():
    """提取状态条件数据"""
    print("提取状态条件...")
    
    with open(DATA_DIR / "conditionsdiseases.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    conditions = []
    
    for condition in data.get("condition", []):
        # 只保留 PHB 和 XPHB 的基本规则
        source = condition.get("source", "")
        if source not in ["PHB", "XPHB"]:
            continue
        
        name_en = condition.get("name", "")
        name_cn = CONDITION_MAP.get(name_en, name_en)
        
        entries = parse_entries(condition.get("entries", []))
        
        conditions.append({
            "name_en": name_en,
            "name_cn": name_cn,
            "source": source,
            "page": condition.get("page", 0),
            "description": entries
        })
    
    # 去重，保留最新的 (XPHB优先)
    seen = {}
    for c in conditions:
        key = c["name_en"]
        if key not in seen or c["source"] == "XPHB":
            seen[key] = c
    
    return list(seen.values())

def extract_actions():
    """提取战斗动作数据"""
    print("提取战斗动作...")
    
    with open(DATA_DIR / "actions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    actions = []
    
    for action in data.get("action", []):
        source = action.get("source", "")
        # 优先基础规则
        if source not in ["PHB", "XPHB", "DMG"]:
            continue
        
        name_en = action.get("name", "")
        name_cn = ACTION_MAP.get(name_en, name_en)
        
        # 获取时间
        time_info = ""
        time = action.get("time", [])
        if time and isinstance(time, list) and len(time) > 0:
            if isinstance(time[0], dict):
                num = time[0].get("number", 1)
                unit = time[0].get("unit", "action")
                time_info = f"{num} {unit}"
        
        entries = parse_entries(action.get("entries", []))
        
        actions.append({
            "name_en": name_en,
            "name_cn": name_cn,
            "source": source,
            "time": time_info,
            "description": entries
        })
    
    # 去重
    seen = {}
    for a in actions:
        key = a["name_en"]
        if key not in seen or a["source"] == "XPHB":
            seen[key] = a
    
    return list(seen.values())

def extract_spells():
    """提取法术数据 - 只取常用法术作为示例"""
    print("提取法术数据...")
    
    spell_files = ["spells-phb.json", "spells-xphb.json"]
    spells = []
    
    for fname in spell_files:
        fpath = DATA_DIR / "spells" / fname
        if not fpath.exists():
            continue
        
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for spell in data.get("spell", []):
            name = spell.get("name", "")
            level = spell.get("level", 0)
            school = spell.get("school", "")
            
            # 获取施法时间
            cast_time = ""
            time = spell.get("time", [])
            if time and isinstance(time, list):
                t = time[0]
                if isinstance(t, dict):
                    cast_time = f"{t.get('number', 1)} {t.get('unit', 'action')}"
            
            # 获取射程
            range_info = ""
            rng = spell.get("range", {})
            if rng:
                if rng.get("type") == "point":
                    dist = rng.get("distance", {})
                    if dist.get("type") == "self":
                        range_info = "自身"
                    elif dist.get("type") == "touch":
                        range_info = "触及"
                    else:
                        range_info = f"{dist.get('amount', 0)} {dist.get('type', 'feet')}"
                elif rng.get("type") == "radius":
                    dist = rng.get("distance", {})
                    range_info = f"自身（{dist.get('amount', 0)}-{dist.get('type', 'feet')} 半径）"
            
            # 获取成分
            components = spell.get("components", {})
            comp_parts = []
            if components.get("v"):
                comp_parts.append("言语(V)")
            if components.get("s"):
                comp_parts.append("姿势(S)")
            if components.get("m"):
                m = components.get("m")
                if isinstance(m, str):
                    comp_parts.append(f"材料(M): {m}")
                elif isinstance(m, dict):
                    comp_parts.append(f"材料(M): {m.get('text', '')}")
            
            # 获取持续时间
            duration_info = ""
            dur = spell.get("duration", [])
            if dur and isinstance(dur, list):
                d = dur[0]
                if isinstance(d, dict):
                    if d.get("type") == "instant":
                        duration_info = "立即"
                    elif d.get("type") == "timed":
                        du = d.get("duration", {})
                        duration_info = f"{du.get('amount', 0)} {du.get('type', '')}"
                        if d.get("concentration"):
                            duration_info = f"专注，至多 {duration_info}"
            
            # 获取描述
            entries = parse_entries(spell.get("entries", []))
            higher_level = parse_entries(spell.get("entriesHigherLevel", []))
            
            spells.append({
                "name_en": name,
                "name_cn": "",  # 待翻译
                "level": level,
                "school_en": school,
                "school_cn": SCHOOL_MAP.get(school, school),
                "cast_time": cast_time,
                "range": range_info,
                "components": "，".join(comp_parts),
                "duration": duration_info,
                "ritual": spell.get("meta", {}).get("ritual", False),
                "description": entries,
                "higher_level": higher_level,
                "source": spell.get("source", "")
            })
    
    # 去重，优先 XPHB
    seen = {}
    for s in spells:
        key = s["name_en"]
        if key not in seen or s["source"] == "XPHB":
            seen[key] = s
    
    return list(seen.values())

def extract_feats():
    """提取专长数据"""
    print("提取专长数据...")
    
    with open(DATA_DIR / "feats.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    feats = []
    
    for feat in data.get("feat", []):
        source = feat.get("source", "")
        # 优先基础规则
        if source not in ["PHB", "XPHB"]:
            continue
        
        name = feat.get("name", "")
        prerequisite = ""
        
        # 获取先决条件
        prereq = feat.get("prerequisite", [])
        if prereq and isinstance(prereq, list):
            prereq_items = []
            for p in prereq:
                if isinstance(p, dict):
                    if "ability" in p:
                        for a in p["ability"]:
                            if isinstance(a, dict):
                                for k, v in a.items():
                                    prereq_items.append(f"{ABILITY_MAP.get(k, k)} {v}")
                    elif "spellcasting" in p:
                        prereq_items.append("能够施法")
                    elif "proficiency" in p:
                        prof = p["proficiency"]
                        if isinstance(prof, list) and prof:
                            prereq_items.append(f"熟练: {prof[0]}")
            prerequisite = "，".join(prereq_items)
        
        entries = parse_entries(feat.get("entries", []))
        
        feats.append({
            "name_en": name,
            "name_cn": "",
            "prerequisite": prerequisite,
            "description": entries,
            "source": source
        })
    
    # 去重
    seen = {}
    for f in feats:
        key = f["name_en"]
        if key not in seen or f["source"] == "XPHB":
            seen[key] = f
    
    return list(seen.values())

def main():
    """主函数"""
    print("=" * 50)
    print("5etools 数据提取工具")
    print("=" * 50)
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 提取各类数据
    conditions = extract_conditions()
    actions = extract_actions()
    spells = extract_spells()
    feats = extract_feats()
    
    print(f"\n提取完成:")
    print(f"  - 状态条件: {len(conditions)} 个")
    print(f"  - 战斗动作: {len(actions)} 个")
    print(f"  - 法术: {len(spells)} 个")
    print(f"  - 专长: {len(feats)} 个")
    
    # 保存为 JSON
    output_data = {
        "conditions": conditions,
        "actions": actions,
        "spells": spells,
        "feats": feats
    }
    
    output_file = OUTPUT_DIR / "5etools_extracted.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    
    # 同时生成 Markdown 格式的参考文档
    md_content = generate_markdown(conditions, actions, spells, feats)
    md_file = OUTPUT_DIR / "5etools_reference.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"参考文档已保存到: {md_file}")

def generate_markdown(conditions, actions, spells, feats):
    """生成 Markdown 格式的参考文档"""
    md = """# D&D 5e 核心规则参考 (从 5etools 提取)

> 本文档包含 D&D 5e 核心规则的英文原文，供翻译和参考使用。
> 数据来源: https://github.com/5etools-mirror-3/5etools-src/

---

## 目录

1. [状态条件 (Conditions)](#状态条件)
2. [战斗动作 (Actions)](#战斗动作)
3. [法术 (Spells)](#法术)
4. [专长 (Feats)](#专长)

---

## 状态条件

"""
    
    # 添加状态条件
    for c in conditions:
        md += f"""### {c['name_cn']} ({c['name_en']})

**来源**: {c['source']} p.{c['page']}

{c['description']}

---

"""
    
    md += """## 战斗动作

"""
    
    # 添加战斗动作
    for a in actions:
        time_str = f" ({a['time']})" if a['time'] else ""
        md += f"""### {a['name_cn']} ({a['name_en']}){time_str}

**来源**: {a['source']}

{a['description']}

---

"""
    
    md += """## 法术

> 注：法术名称的中文翻译需要进一步校对，以下为原文数据

"""
    
    # 添加法术（按等级分组）
    spells_by_level = {}
    for s in spells:
        level = s['level']
        if level not in spells_by_level:
            spells_by_level[level] = []
        spells_by_level[level].append(s)
    
    for level in sorted(spells_by_level.keys()):
        level_name = "戏法" if level == 0 else f"{level} 环"
        md += f"### {level_name}\n\n"
        
        for s in spells_by_level[level][:20]:  # 每级只取前20个示例
            ritual = " (仪式)" if s['ritual'] else ""
            md += f"""#### {s['name_en']}{ritual}

- **学派**: {s['school_cn']} ({s['school_en']})
- **施法时间**: {s['cast_time']}
- **射程**: {s['range']}
- **成分**: {s['components']}
- **持续时间**: {s['duration']}

{s['description']}

"""
            if s['higher_level']:
                md += f"**升阶**: {s['higher_level']}\n\n"
            md += "---\n\n"
    
    md += """## 专长

"""
    
    # 添加专长
    for f in feats:
        prereq = f"\n**先决条件**: {f['prerequisite']}\n" if f['prerequisite'] else ""
        md += f"""### {f['name_en']}

**来源**: {f['source']}{prereq}

{f['description']}

---

"""
    
    return md

if __name__ == "__main__":
    main()
