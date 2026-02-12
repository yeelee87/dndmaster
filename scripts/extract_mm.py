#!/usr/bin/env python3
"""
提取5etools怪物数据，生成完整怪物手册
"""

import json
import re
from pathlib import Path

# 路径
DATA_DIR = Path("/Users/sid/.openclaw/workspace/5etools-data/5etools-src-main/data")
OUTPUT_DIR = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/core-rules")

def clean_text(text):
    """清理5etools标记"""
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
    text = re.sub(r'\{@hit\s+([^}]+)\}', r'+\1', text)
    text = re.sub(r'\{@damage\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@dc\s+([^}]+)\}', r'DC\1', text)
    text = re.sub(r'\{@condition\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@spell\s+([^}]+)\}', r'《\1》', text)
    text = re.sub(r'\{@item\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@action\s+([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@skill\s+([^}]+)\}', r'\1', text)
    
    return text

def parse_entries(entries):
    """解析entries结构"""
    if not entries:
        return ""
    
    if isinstance(entries, str):
        return clean_text(entries)
    
    if isinstance(entries, list):
        result = []
        for entry in entries:
            parsed = parse_entries(entry)
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
            content = parse_entries(entries.get("entries", []))
            if name:
                return f"**{name}**：{content}"
            return content
        
        else:
            content = entries.get("entries", entries.get("items", []))
            return parse_entries(content)
    
    return ""

def format_damage_list(damage_list):
    """格式化伤害抗性/免疫/易伤列表"""
    if not damage_list:
        return []
    result = []
    for item in damage_list:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            # 处理复杂的抗性结构
            if "resist" in item and isinstance(item["resist"], list):
                resist_types = ", ".join(str(r) for r in item["resist"])
                note = item.get("note", "")
                result.append(f"{resist_types} ({note})" if note else resist_types)
            elif "immune" in item and isinstance(item["immune"], list):
                immune_types = ", ".join(str(i) for i in item["immune"])
                note = item.get("note", "")
                result.append(f"{immune_types} ({note})" if note else immune_types)
            else:
                result.append(str(item))
        else:
            result.append(str(item))
    return result

def parse_monster(data):
    """解析怪物数据为易读格式"""
    
    # 基础信息
    name = data.get("name", "未知")
    size_map = {"T": "微型", "S": "小型", "M": "中型", "L": "大型", "H": "巨型", "G": "超巨型"}
    size = size_map.get(data.get("size", ["M"])[0], "中型")
    
    # 类型
    type_info = data.get("type", {})
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
    if tags:
        type_cn += f" ({', '.join(tags)})"
    
    # 阵营
    alignment = data.get("alignment", [])
    align_map = {"L": "守序", "N": "中立", "C": "混乱", "G": "善良", "E": "邪恶", "U": "无阵营", "A": "任意阵营"}
    alignment_str = " ".join([align_map.get(a, a) for a in alignment]) if alignment else "无阵营"
    
    # AC
    ac_data = data.get("ac", [])
    ac_str = ""
    if ac_data and isinstance(ac_data, list):
        if isinstance(ac_data[0], int):
            ac_str = str(ac_data[0])
        elif isinstance(ac_data[0], dict):
            ac_str = str(ac_data[0].get("ac", 10))
            if ac_data[0].get("from"):
                ac_str += f" ({ac_data[0]['from']})"
        elif isinstance(ac_data[0], str):
            ac_str = ac_data[0]
    
    # HP
    hp_data = data.get("hp", {})
    hp_str = f"{hp_data.get('average', 0)} ({hp_data.get('formula', '')})"
    
    # 速度
    speed_data = data.get("speed", {})
    speed_str = ""
    if isinstance(speed_data, dict):
        speeds = []
        if "walk" in speed_data:
            speeds.append(f"行走 {speed_data['walk']}尺")
        if "fly" in speed_data:
            fly_info = speed_data['fly']
            if isinstance(fly_info, dict):
                speeds.append(f"飞行 {fly_info.get('number', 0)}尺")
            else:
                speeds.append(f"飞行 {fly_info}尺")
        if "swim" in speed_data:
            speeds.append(f"游泳 {speed_data['swim']}尺")
        if "climb" in speed_data:
            speeds.append(f"攀爬 {speed_data['climb']}尺")
        if "burrow" in speed_data:
            speeds.append(f"掘地 {speed_data['burrow']}尺")
        speed_str = "，".join(speeds) if speeds else "行走 30尺"
    elif isinstance(speed_data, int):
        speed_str = f"行走 {speed_data}尺"
    
    # 属性值
    abilities = {
        "力量": data.get("str", 10),
        "敏捷": data.get("dex", 10),
        "体质": data.get("con", 10),
        "智力": data.get("int", 10),
        "感知": data.get("wis", 10),
        "魅力": data.get("cha", 10)
    }
    
    # 计算调整值
    def mod(score):
        return (score - 10) // 2
    
    # 豁免
    saves = data.get("save", {})
    
    # 技能
    skills = data.get("skill", {})
    
    # 伤害抗性/免疫/易伤
    resistances = format_damage_list(data.get("resist", []))
    immunities = format_damage_list(data.get("immune", []))
    vulnerabilities = format_damage_list(data.get("vulnerable", []))
    condition_immunities = format_damage_list(data.get("conditionImmune", []))
    
    # 感官
    senses = data.get("senses", [])
    passive = data.get("passive", 10)
    
    # 语言
    languages = data.get("languages", [])
    
    # 挑战等级
    cr = data.get("cr", "0")
    if isinstance(cr, dict):
        cr = cr.get("cr", "0")
    
    # 特性
    traits = []
    for trait in data.get("trait", []):
        trait_name = trait.get("name", "")
        trait_desc = parse_entries(trait.get("entries", []))
        if trait_desc:
            traits.append(f"**{trait_name}**：{trait_desc}")
    
    # 动作
    actions = []
    for action in data.get("action", []):
        action_name = action.get("name", "")
        action_desc = parse_entries(action.get("entries", []))
        if action_desc:
            actions.append(f"**{action_name}**：{action_desc}")
    
    # 反应
    reactions = []
    for reaction in data.get("reaction", []):
        reaction_name = reaction.get("name", "")
        reaction_desc = parse_entries(reaction.get("entries", []))
        if reaction_desc:
            reactions.append(f"**{reaction_name}**：{reaction_desc}")
    
    #  legendary actions
    legendary = []
    for leg in data.get("legendary", []):
        leg_name = leg.get("name", "")
        leg_desc = parse_entries(leg.get("entries", []))
        if leg_desc:
            legendary.append(f"**{leg_name}**：{leg_desc}")
    
    # 生成markdown
    md = f"""### {name}

*{size} {type_cn}，{alignment_str}*

**护甲等级**：{ac_str}  
**生命值**：{hp_str}  
**速度**：{speed_str}  
**挑战等级**：{cr}

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| {abilities['力量']} ({mod(abilities['力量']):+d}) | {abilities['敏捷']} ({mod(abilities['敏捷']):+d}) | {abilities['体质']} ({mod(abilities['体质']):+d}) | {abilities['智力']} ({mod(abilities['智力']):+d}) | {abilities['感知']} ({mod(abilities['感知']):+d}) | {abilities['魅力']} ({mod(abilities['魅力']):+d}) |

"""
    
    if saves:
        save_strs = [f"{k.upper()} {v}" for k, v in saves.items()]
        md += f"**豁免**：{', '.join(save_strs)}  \n"
    
    if skills:
        skill_strs = [f"{k} {v}" for k, v in skills.items()]
        md += f"**技能**：{', '.join(skill_strs)}  \n"
    
    if resistances:
        md += f"**伤害抗性**：{', '.join(resistances)}  \n"
    
    if immunities:
        md += f"**伤害免疫**：{', '.join(immunities)}  \n"
    
    if vulnerabilities:
        md += f"**伤害易伤**：{', '.join(vulnerabilities)}  \n"
    
    if condition_immunities:
        md += f"**状态免疫**：{', '.join(condition_immunities)}  \n"
    
    if senses:
        md += f"**感官**：{', '.join(senses)}  \n"
    
    md += f"**被动感知**：{passive}  \n"
    
    if languages:
        md += f"**语言**：{', '.join(languages)}  \n"
    
    md += "\n"
    
    if traits:
        md += "**特性**：\n\n"
        for trait in traits:
            md += f"{trait}\n\n"
    
    if actions:
        md += "**动作**：\n\n"
        for action in actions:
            md += f"{action}\n\n"
    
    if reactions:
        md += "**反应**：\n\n"
        for reaction in reactions:
            md += f"{reaction}\n\n"
    
    if legendary:
        md += "**传奇动作**：\n\n"
        for leg in legendary:
            md += f"{leg}\n\n"
    
    md += "---\n\n"
    
    return name, md

def extract_core_monsters():
    """提取核心怪物手册数据"""
    
    # 核心怪物手册文件 - 包含MM、DMG、PHB的怪物
    core_files = [
        "bestiary-mm.json",  # 怪物手册
        "bestiary-dmg.json", # DMG怪物
        "bestiary-phb.json", # PHB相关
    ]
    
    monsters = []
    
    for fname in core_files:
        fpath = DATA_DIR / "bestiary" / fname
        if not fpath.exists():
            print(f"跳过: {fname}")
            continue
        
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            print(f"处理 {fname}: {len(data.get('monster', []))} 个怪物")
            
            for monster in data.get("monster", []):
                try:
                    name, md = parse_monster(monster)
                    monsters.append((name, md))
                except Exception as e:
                    print(f"  解析怪物失败: {e}")
                
        except Exception as e:
            print(f"错误处理 {fname}: {e}")
    
    return monsters

def main():
    print("提取核心怪物手册数据...")
    print()
    
    monsters = extract_core_monsters()
    print()
    print(f"总共提取了 {len(monsters)} 个怪物")
    
    # 去重
    seen = {}
    for name, md in monsters:
        if name not in seen:
            seen[name] = md
    monsters = list(seen.items())
    print(f"去重后: {len(monsters)} 个怪物")
    
    # 生成完整怪物手册
    md_content = """# 怪物手册 (Monster Manual)

> 数据来源于5etools，D&D 5e 2014版核心怪物

---

## 目录

"""
    
    # 按字母排序
    monsters.sort(key=lambda x: x[0])
    
    for name, _ in monsters:
        anchor = name.lower().replace(' ', '-').replace("'", '')
        md_content += f"- [{name}](#{anchor})\n"
    
    md_content += "\n---\n\n"
    
    # 添加所有怪物
    for name, md in monsters:
        md_content += md
    
    # 保存
    output_file = OUTPUT_DIR / "mm_2014_full.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print()
    print(f"已保存到: {output_file}")
    print(f"文件大小: {output_file.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
