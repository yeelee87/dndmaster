#!/usr/bin/env python3
"""
提取凡戴尔的失落矿坑 (Lost Mine of Phandelver) 怪物数据
"""

import json
from pathlib import Path

DATA_DIR = Path("/Users/sid/.openclaw/workspace/5etools-src-temp/data")
OUTPUT_DIR = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/data")

# LMOP 怪物名称映射
LMOP_MONSTER_MAP = {
    "Goblin": "地精",
    "Hobgoblin": "大地精",
    "Bugbear": "熊地精",
    "Wolf": "狼",
    "Twig Blight": "枯枝怪",
    "Evil Mage": "邪恶法师",
    "Mormesk the Wraith": "幽灵莫梅斯克",
    "Nezznar the Black Spider": "黑蜘蛛涅兹纳尔",
    "Iarno Albrek": "亚尔诺·阿尔布里克",
    "Sildar Hallwinter": "西尔达·哈尔温特",
    "Gundren Rockseeker": "冈德伦·寻石者",
    "King Grol": "格罗尔大王",
    "Snarl": "咆哮",
    "Ripper": "撕裂者",
    "Targor Bloodsword": "血剑塔戈尔",
    "Venomfang": "毒牙"
}

def extract_lmop_monsters():
    """提取 LMOP 模组怪物"""
    print("提取 LMOP 怪物数据...")
    
    with open(DATA_DIR / "bestiary" / "bestiary-lmop.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    monsters = []
    
    for monster in data.get("monster", []):
        name = monster.get("name", "")
        name_cn = LMOP_MONSTER_MAP.get(name, name)
        
        # 基础信息
        size_map = {
            "T": "微型", "S": "小型", "M": "中型",
            "L": "大型", "H": "巨型", "G": "超巨型"
        }
        size = monster.get("size", ["M"])
        size_str = size_map.get(size[0], size[0]) if size else "中型"
        
        # 类型
        type_info = monster.get("type", {})
        if isinstance(type_info, dict):
            type_str = type_info.get("type", "")
            tags = type_info.get("tags", [])
        else:
            type_str = type_info
            tags = []
        
        type_map = {
            "aberration": "异怪", "beast": "野兽", "celestial": "天界生物",
            "construct": "构装生物", "dragon": "龙", "elemental": "元素生物",
            "fey": "精类", "fiend": "邪魔", "giant": "巨人",
            "humanoid": "类人生物", "monstrosity": "怪兽", "ooze": "泥怪",
            "plant": "植物", "undead": "亡灵"
        }
        type_cn = type_map.get(type_str, type_str)
        
        # 阵营
        alignment = monster.get("alignment", [])
        align_map = {
            "L": "守序", "N": "中立", "C": "混乱",
            "G": "善良", "E": "邪恶", "U": "无阵营"
        }
        alignment_str = " ".join(align_map.get(a, a) for a in alignment) if alignment else "无阵营"
        
        # AC
        ac_data = monster.get("ac", [])
        ac_str = ""
        if ac_data and isinstance(ac_data, list):
            if isinstance(ac_data[0], int):
                ac_str = str(ac_data[0])
            elif isinstance(ac_data[0], dict):
                ac_str = str(ac_data[0].get("ac", 10))
        
        # HP
        hp_data = monster.get("hp", {})
        hp_str = f"{hp_data.get('average', 0)} ({hp_data.get('formula', '')})"
        
        # 速度
        speed_data = monster.get("speed", {})
        speed_parts = []
        if isinstance(speed_data, dict):
            if "walk" in speed_data:
                speed_parts.append(f"行走 {speed_data['walk']}尺")
            if "fly" in speed_data:
                speed_parts.append(f"飞行 {speed_data['fly']}尺")
            if "swim" in speed_data:
                speed_parts.append(f"游泳 {speed_data['swim']}尺")
        speed_str = "，".join(speed_parts) if speed_parts else "行走 30尺"
        
        # 属性值
        abilities = {
            "力量": monster.get("str", 10),
            "敏捷": monster.get("dex", 10),
            "体质": monster.get("con", 10),
            "智力": monster.get("int", 10),
            "感知": monster.get("wis", 10),
            "魅力": monster.get("cha", 10)
        }
        
        # 豁免
        saves = monster.get("save", {})
        save_strs = []
        for k, v in saves.items():
            save_strs.append(f"{k.upper()} {v}")
        
        # 技能
        skills = monster.get("skill", {})
        skill_strs = []
        for k, v in skills.items():
            skill_strs.append(f"{k.title()} {v}")
        
        # 伤害抗性/免疫/易伤
        resist = monster.get("resist", [])
        immune = monster.get("immune", [])
        vulnerable = monster.get("vulnerable", [])
        condition_immunity = monster.get("conditionImmune", [])
        
        # 感官
        senses = monster.get("senses", [])
        passive = monster.get("passive", 10)
        
        # 语言
        languages = monster.get("languages", [])
        
        # 挑战等级
        cr = monster.get("cr", "0")
        
        # 特性
        traits = []
        for trait in monster.get("trait", []):
            trait_name = trait.get("name", "")
            trait_entries = trait.get("entries", [])
            trait_desc = "\n".join(str(e) for e in trait_entries)
            traits.append({"name": trait_name, "description": trait_desc})
        
        # 动作
        actions = []
        for action in monster.get("action", []):
            action_name = action.get("name", "")
            action_entries = action.get("entries", [])
            action_desc = "\n".join(str(e) for e in action_entries)
            actions.append({"name": action_name, "description": action_desc})
        
        # 法术施放
        spellcasting = []
        for sc in monster.get("spellcasting", []):
            sc_name = sc.get("name", "")
            sc_header = sc.get("headerEntries", [])
            sc_spells = sc.get("spells", {})
            spellcasting.append({
                "name": sc_name,
                "header": "\n".join(str(e) for e in sc_header),
                "spells": sc_spells
            })
        
        monsters.append({
            "name_en": name,
            "name_cn": name_cn,
            "is_npc": monster.get("isNpc", False),
            "is_named": monster.get("isNamedCreature", False),
            "size": size_str,
            "type": type_cn,
            "tags": tags,
            "alignment": alignment_str,
            "ac": ac_str,
            "hp": hp_str,
            "speed": speed_str,
            "abilities": abilities,
            "saves": save_strs,
            "skills": skill_strs,
            "resistances": resist,
            "immunities": immune,
            "vulnerabilities": vulnerable,
            "condition_immunities": condition_immunity,
            "senses": senses,
            "passive_perception": passive,
            "languages": languages,
            "cr": cr,
            "traits": traits,
            "actions": actions,
            "spellcasting": spellcasting,
            "source": monster.get("source", "")
        })
    
    return monsters

def generate_lmop_markdown(monsters):
    """生成 LMOP 怪物 Markdown"""
    md = """# 凡戴尔的失落矿坑 - 怪物数据

> 本文档包含模组《凡戴尔的失落矿坑》中的所有怪物和NPC数据
> 数据来源: 5etools

---

"""
    
    for m in monsters:
        npc_tag = " [NPC]" if m['is_npc'] else ""
        named_tag = " [有名角色]" if m['is_named'] else ""
        
        md += f"## {m['name_cn']} ({m['name_en']}){npc_tag}{named_tag}\n\n"
        md += f"*{m['size']} {m['type']}{' (' + ','.join(m['tags']) + ')' if m['tags'] else ''}，{m['alignment']}*\n\n"
        
        # 基础数据
        md += f"**AC**: {m['ac']}  \
"
        md += f"**HP**: {m['hp']}  \
"
        md += f"**速度**: {m['speed']}  \
"
        md += f"**CR**: {m['cr']}  \
\n"
        
        # 属性
        md += "### 属性\n\n"
        md += "| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |\n"
        md += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
        abilities = m['abilities']
        md += f"| {abilities['力量']} ({(abilities['力量']-10)//2:+d}) | "
        md += f"{abilities['敏捷']} ({(abilities['敏捷']-10)//2:+d}) | "
        md += f"{abilities['体质']} ({(abilities['体质']-10)//2:+d}) | "
        md += f"{abilities['智力']} ({(abilities['智力']-10)//2:+d}) | "
        md += f"{abilities['感知']} ({(abilities['感知']-10)//2:+d}) | "
        md += f"{abilities['魅力']} ({(abilities['魅力']-10)//2:+d}) |\n\n"
        
        # 其他信息
        if m['saves']:
            md += f"**豁免**: {', '.join(m['saves'])}  \
"
        if m['skills']:
            md += f"**技能**: {', '.join(m['skills'])}  \
"
        if m['resistances']:
            md += f"**抗性**: {', '.join(str(r) for r in m['resistances'])}  \
"
        if m['immunities']:
            md += f"**免疫**: {', '.join(str(i) for i in m['immunities'])}  \
"
        if m['condition_immunities']:
            md += f"**状态免疫**: {', '.join(str(c) for c in m['condition_immunities'])}  \
"
        if m['senses']:
            md += f"**感官**: {', '.join(m['senses'])}  \
"
        md += f"**被动感知**: {m['passive_perception']}  \
"
        if m['languages']:
            md += f"**语言**: {', '.join(m['languages'])}  \
"
        
        md += "\n"
        
        # 特性
        if m['traits']:
            md += "### 特性\n\n"
            for trait in m['traits']:
                md += f"**{trait['name']}**: {trait['description']}\n\n"
        
        # 法术
        if m['spellcasting']:
            md += "### 法术施放\n\n"
            for sc in m['spellcasting']:
                md += f"**{sc['name']}**: {sc['header']}\n\n"
        
        # 动作
        if m['actions']:
            md += "### 动作\n\n"
            for action in m['actions']:
                md += f"**{action['name']}**: {action['description']}\n\n"
        
        md += "---\n\n"
    
    return md

def main():
    print("=" * 50)
    print("LMOP 怪物数据提取")
    print("=" * 50)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    monsters = extract_lmop_monsters()
    print(f"提取了 {len(monsters)} 个怪物/NPC")
    
    # 保存 JSON
    with open(OUTPUT_DIR / "lmop_monsters.json", "w", encoding="utf-8") as f:
        json.dump(monsters, f, ensure_ascii=False, indent=2)
    
    # 保存 Markdown
    md = generate_lmop_markdown(monsters)
    with open(OUTPUT_DIR / "lmop_monsters.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"\n数据已保存到:")
    print(f"  - {OUTPUT_DIR / 'lmop_monsters.json'}")
    print(f"  - {OUTPUT_DIR / 'lmop_monsters.md'}")

if __name__ == "__main__":
    main()
