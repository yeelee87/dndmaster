#!/usr/bin/env python3
"""
5etools 索引生成器
为所有数据创建快速查找索引
"""

import json
import os
from pathlib import Path
from typing import Dict, List
import re

# 路径配置
WORKSPACE = Path("/Users/sid/.openclaw/workspace")
DATA_SOURCE = WORKSPACE / "5etools-data" / "data"
OUTPUT_DIR = WORKSPACE / "skills" / "dnd-game-master" / "data" / "index"

def ensure_dirs():
    """确保目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_monster_index() -> Dict:
    """生成怪物索引"""
    print("正在生成怪物索引...")
    
    index = {}
    bestiary_dir = DATA_SOURCE / "bestiary"
    
    if not bestiary_dir.exists():
        print(f"[Warning] 怪物目录不存在: {bestiary_dir}")
        return index
    
    # 遍历所有怪物文件
    for json_file in sorted(bestiary_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for monster in data.get("monster", []):
                name = monster.get("name", "").lower()
                if not name:
                    continue
                
                # 提取关键信息用于快速显示
                cr = monster.get("cr", "0")
                if isinstance(cr, dict):
                    cr = cr.get("cr", "0")
                
                index[name] = {
                    "name_en": monster.get("name", ""),
                    "file": f"bestiary/{json_file.name}",
                    "source": monster.get("source", ""),
                    "cr": str(cr),
                    "type": monster.get("type", {}),
                    "size": monster.get("size", [])
                }
                
                # 同时添加原名（首字母大写）
                name_cap = monster.get("name", "").lower()
                if name_cap != name:
                    index[name_cap] = index[name]
                
        except Exception as e:
            print(f"[Error] 处理文件 {json_file.name}: {e}")
    
    print(f"  索引了 {len(index)} 个怪物")
    return index

def generate_spell_index() -> Dict:
    """生成法术索引"""
    print("正在生成法术索引...")
    
    index = {}
    spells_dir = DATA_SOURCE / "spells"
    
    if not spells_dir.exists():
        print(f"[Warning] 法术目录不存在: {spells_dir}")
        return index
    
    school_map = {
        "A": "Abjuration", "C": "Conjuration", "D": "Divination",
        "E": "Enchantment", "V": "Evocation", "I": "Illusion",
        "N": "Necromancy", "T": "Transmutation"
    }
    
    for json_file in sorted(spells_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for spell in data.get("spell", []):
                name = spell.get("name", "").lower()
                if not name:
                    continue
                
                school = school_map.get(spell.get("school", ""), spell.get("school", ""))
                
                index[name] = {
                    "name_en": spell.get("name", ""),
                    "file": json_file.name,
                    "source": spell.get("source", ""),
                    "level": spell.get("level", 0),
                    "school": school,
                    "ritual": spell.get("meta", {}).get("ritual", False)
                }
                
        except Exception as e:
            print(f"[Error] 处理文件 {json_file.name}: {e}")
    
    print(f"  索引了 {len(index)} 个法术")
    return index

def generate_item_index() -> Dict:
    """生成物品索引"""
    print("正在生成物品索引...")
    
    index = {}
    items_file = DATA_SOURCE / "items.json"
    
    if not items_file.exists():
        print(f"[Warning] 物品文件不存在: {items_file}")
        return index
    
    try:
        with open(items_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item in data.get("item", []):
            name = item.get("name", "").lower()
            if not name:
                continue
            
            index[name] = {
                "name_en": item.get("name", ""),
                "source": item.get("source", ""),
                "type": item.get("type", ""),
                "rarity": item.get("rarity", ""),
                "requires_attunement": item.get("reqAttune", False)
            }
            
    except Exception as e:
        print(f"[Error] 处理物品文件: {e}")
    
    print(f"  索引了 {len(index)} 个物品")
    return index

def generate_feat_index() -> Dict:
    """生成专长索引"""
    print("正在生成专长索引...")
    
    index = {}
    feats_file = DATA_SOURCE / "feats.json"
    
    if not feats_file.exists():
        print(f"[Warning] 专长文件不存在: {feats_file}")
        return index
    
    try:
        with open(feats_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for feat in data.get("feat", []):
            name = feat.get("name", "").lower()
            if not name:
                continue
            
            index[name] = {
                "name_en": feat.get("name", ""),
                "source": feat.get("source", ""),
                "has_prerequisite": bool(feat.get("prerequisite", []))
            }
            
    except Exception as e:
        print(f"[Error] 处理专长文件: {e}")
    
    print(f"  索引了 {len(index)} 个专长")
    return index

def generate_condition_index() -> Dict:
    """生成状态条件索引"""
    print("正在生成状态条件索引...")
    
    index = {}
    conditions_file = DATA_SOURCE / "conditionsdiseases.json"
    
    if not conditions_file.exists():
        print(f"[Warning] 状态条件文件不存在: {conditions_file}")
        return index
    
    try:
        with open(conditions_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for condition in data.get("condition", []):
            name = condition.get("name", "").lower()
            if not name:
                continue
            
            # 只保留 PHB 和 XPHB
            source = condition.get("source", "")
            if source not in ["PHB", "XPHB"]:
                continue
            
            index[name] = {
                "name_en": condition.get("name", ""),
                "source": source,
                "page": condition.get("page", 0),
                "srd": condition.get("srd", False)
            }
            
    except Exception as e:
        print(f"[Error] 处理状态条件文件: {e}")
    
    print(f"  索引了 {len(index)} 个状态条件")
    return index

def generate_action_index() -> Dict:
    """生成战斗动作索引"""
    print("正在生成战斗动作索引...")
    
    index = {}
    actions_file = DATA_SOURCE / "actions.json"
    
    if not actions_file.exists():
        print(f"[Warning] 动作文件不存在: {actions_file}")
        return index
    
    try:
        with open(actions_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for action in data.get("action", []):
            name = action.get("name", "").lower()
            if not name:
                continue
            
            index[name] = {
                "name_en": action.get("name", ""),
                "source": action.get("source", ""),
                "time": action.get("time", [])
            }
            
    except Exception as e:
        print(f"[Error] 处理动作文件: {e}")
    
    print(f"  索引了 {len(index)} 个战斗动作")
    return index

def generate_race_index() -> Dict:
    """生成种族索引"""
    print("正在生成种族索引...")
    
    index = {}
    races_file = DATA_SOURCE / "races.json"
    
    if not races_file.exists():
        print(f"[Warning] 种族文件不存在: {races_file}")
        return index
    
    try:
        with open(races_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for race in data.get("race", []):
            name = race.get("name", "").lower()
            if not name:
                continue
            
            index[name] = {
                "name_en": race.get("name", ""),
                "source": race.get("source", ""),
                "size": race.get("size", []),
                "speed": race.get("speed", {})
            }
            
    except Exception as e:
        print(f"[Error] 处理种族文件: {e}")
    
    print(f"  索引了 {len(index)} 个种族")
    return index

def generate_background_index() -> Dict:
    """生成背景索引"""
    print("正在生成背景索引...")
    
    index = {}
    backgrounds_file = DATA_SOURCE / "backgrounds.json"
    
    if not backgrounds_file.exists():
        print(f"[Warning] 背景文件不存在: {backgrounds_file}")
        return index
    
    try:
        with open(backgrounds_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for bg in data.get("background", []):
            name = bg.get("name", "").lower()
            if not name:
                continue
            
            index[name] = {
                "name_en": bg.get("name", ""),
                "source": bg.get("source", ""),
                "skill_proficiencies": bg.get("skillProficiencies", [])
            }
            
    except Exception as e:
        print(f"[Error] 处理背景文件: {e}")
    
    print(f"  索引了 {len(index)} 个背景")
    return index

def generate_class_index() -> Dict:
    """生成职业索引"""
    print("正在生成职业索引...")
    
    index = {}
    class_dir = DATA_SOURCE / "class"
    
    if not class_dir.exists():
        print(f"[Warning] 职业目录不存在: {class_dir}")
        return index
    
    for json_file in sorted(class_dir.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for cls in data.get("class", []):
                name = cls.get("name", "").lower()
                if not name:
                    continue
                
                index[name] = {
                    "name_en": cls.get("name", ""),
                    "file": f"class/{json_file.name}",
                    "source": cls.get("source", ""),
                    "hd": cls.get("hd", {}),
                    "proficiency": cls.get("proficiency", [])
                }
                
                # 同时索引子职
                for subclass in cls.get("subclasses", []):
                    sub_name = subclass.get("name", "").lower()
                    if sub_name:
                        index[sub_name] = {
                            "name_en": subclass.get("name", ""),
                            "parent_class": cls.get("name", ""),
                            "source": subclass.get("source", "")
                        }
                
        except Exception as e:
            print(f"[Error] 处理文件 {json_file.name}: {e}")
    
    print(f"  索引了 {len(index)} 个职业/子职")
    return index

def save_index(name: str, index: Dict):
    """保存索引文件"""
    output_file = OUTPUT_DIR / f"{name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"  已保存: {output_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("5etools 索引生成器")
    print("=" * 60)
    print()
    
    ensure_dirs()
    
    if not DATA_SOURCE.exists():
        print(f"[Error] 数据源不存在: {DATA_SOURCE}")
        print("请先克隆 5etools 数据仓库:")
        print("  git clone --depth 1 https://github.com/5etools-mirror-3/5etools-src.git")
        return
    
    # 生成各类索引
    indexes = {
        "monsters": generate_monster_index(),
        "spells": generate_spell_index(),
        "items": generate_item_index(),
        "feats": generate_feat_index(),
        "conditions": generate_condition_index(),
        "actions": generate_action_index(),
        "races": generate_race_index(),
        "backgrounds": generate_background_index(),
        "classes": generate_class_index()
    }
    
    print()
    print("保存索引文件...")
    for name, idx in indexes.items():
        if idx:
            save_index(name, idx)
    
    print()
    print("=" * 60)
    print("索引生成完成!")
    print("=" * 60)
    
    # 统计信息
    total_entries = sum(len(idx) for idx in indexes.values())
    print(f"\n总计索引条目: {total_entries}")
    print(f"索引文件位置: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
