#!/usr/bin/env python3
"""
5etools 数据索引和查询系统 (适配已提取数据版本)
- 按需加载，快速查询
- 支持缓存和热数据
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from functools import lru_cache
import hashlib

# 路径配置
WORKSPACE = Path("/Users/sid/.openclaw/workspace")
DATA_SOURCE = WORKSPACE / "5etools-data" / "data"  # 完整数据源（可选）
SKILL_DATA = WORKSPACE / "skills" / "dnd-game-master" / "data"
INDEX_DIR = SKILL_DATA / "index"
CACHE_DIR = SKILL_DATA / "cache"

# 已提取的核心数据文件
EXTRACTED_DATA = SKILL_DATA / "5etools_extracted.json"
LMOP_DATA = SKILL_DATA / "lmop_monsters.json"

# 常见怪物中文名称映射
MONSTER_NAME_CN = {
    # 基础怪物
    "goblin": "地精",
    "goblins": "地精",
    "bugbear": "熊地精",
    "bugbears": "熊地精",
    "wolf": "狼",
    "wolves": "狼",
    "skeleton": "骷髅",
    "skeletons": "骷髅",
    "zombie": "僵尸",
    "zombies": "僵尸",
    "orc": "兽人",
    "orcs": "兽人",
    "bandit": "强盗",
    "bandits": "强盗",
    "scout": "斥候",
    "scouts": "斥候",
    "noble": "贵族",
    "commoner": "平民",
    "commoners": "平民",
    "guard": "守卫",
    "guards": "守卫",
    "thug": "暴徒",
    "thugs": "暴徒",
    "spy": "间谍",
    "spies": "间谍",
    "tribal warrior": "部落战士",
    "veteran": "老兵",
    "cultist": "邪教徒",
    "cultists": "邪教徒",
    "cult fanatic": "邪教狂热者",
    "druid": "德鲁伊",
    "druids": "德鲁伊",
    "priest": "牧师",
    "priests": "牧师",
    "acolyte": "侍僧",
    "acolytes": "侍僧",
    "mage": "法师",
    "mages": "法师",
    "archmage": "大法师",
    "assassin": "刺客",
    "assassins": "刺客",
    "gladiator": "角斗士",
    "knight": "骑士",
    "knights": "骑士",
    "werewolf": "狼人",
    "wererat": "鼠人",
    "ghost": "幽灵",
    "specter": "恶灵",
    "wraith": "怨灵",
    "wraiths": "怨灵",
    "ghoul": "食尸鬼",
    "ghouls": "食尸鬼",
    "spectator": "观察者",
    "owl bear": "枭熊",
    "owlbear": "枭熊",
    "notouch": "诺特奇",
    "grick": "格里克",
    "ochre jelly": "赭冻怪",
    "stirge": "蚊蝠",
    "stirges": "蚊蝠",
    "twig blight": "枯枝怪",
    "twig blights": "枯枝怪",
    "vine blight": "藤蔓怪",
    "needle blight": "针刺怪",
    "awakened shrub": "觉醒灌木",
    "awakened tree": "觉醒树木",
    "giant spider": "巨型蜘蛛",
    "giant wolf spider": "巨型狼蛛",
    "spider": "蜘蛛",
    "rat": "老鼠",
    "rats": "老鼠",
    "raven": "乌鸦",
    "ravens": "乌鸦",
    "rock": "岩石",
    "mule": "骡子",
    "riding horse": "乘用马",
    "draft horse": "挽马",
    "mastiff": "獒犬",
    "mastiffs": "獒犬",
    "poisonous snake": "毒蛇",
    "constrictor snake": "蟒蛇",
    "giant poisonous snake": "巨型毒蛇",
    "giant constrictor snake": "巨型蟒蛇",
    "crocodile": "鳄鱼",
    "giant crocodile": "巨型鳄鱼",
    "boar": "野猪",
    "boars": "野猪",
    "giant boar": "巨型野猪",
    "elk": "麋鹿",
    "giant elk": "巨型麋鹿",
}

class DnDDataManager:
    """D&D 5e 数据管理器"""
    
    def __init__(self):
        self.index = {}
        self.cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self._extracted_data = None
        self._lmop_data = None
        self._load_indexes()
        self._load_extracted_data()
    
    def _load_indexes(self):
        """加载所有索引文件"""
        if INDEX_DIR.exists():
            for idx_file in INDEX_DIR.glob("*.json"):
                with open(idx_file, "r", encoding="utf-8") as f:
                    key = idx_file.stem
                    self.index[key] = json.load(f)
        else:
            print("[Warning] 索引目录不存在")
    
    def _load_extracted_data(self):
        """加载已提取的核心数据"""
        if EXTRACTED_DATA.exists():
            with open(EXTRACTED_DATA, "r", encoding="utf-8") as f:
                self._extracted_data = json.load(f)
        
        if LMOP_DATA.exists():
            with open(LMOP_DATA, "r", encoding="utf-8") as f:
                self._lmop_data = json.load(f)
    
    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        hash_key = hashlib.md5(key.encode()).hexdigest()[:16]
        return CACHE_DIR / f"{hash_key}.json"
    
    def _load_from_cache(self, key: str) -> Optional[Dict]:
        """从缓存加载"""
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    self.cache_hits += 1
                    return json.load(f)
            except:
                pass
        return None
    
    def _save_to_cache(self, key: str, data: Dict):
        """保存到缓存"""
        cache_path = self._get_cache_path(key)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ============ 核心查询方法 ============
    
    def find_monster(self, name: str) -> Optional[Dict]:
        """
        查找怪物
        
        Args:
            name: 怪物名称（英文或中文）
        
        Returns:
            怪物数据字典，未找到返回 None
        """
        name_lower = name.lower()
        cache_key = f"monster:{name_lower}"
        
        # 1. 检查内存缓存
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]
        
        # 2. 检查文件缓存
        cached = self._load_from_cache(cache_key)
        if cached:
            self.cache[cache_key] = cached
            return cached
        
        # 3. 从LMOP数据查找（模组特定怪物）
        self.cache_misses += 1
        if self._lmop_data:
            for monster in self._lmop_data:
                monster_name_en = monster.get("name_en", "").lower()
                monster_name_cn = monster.get("name_cn", "").lower()
                
                # 直接匹配名称
                if monster_name_en == name_lower or monster_name_cn == name_lower:
                    formatted = self._format_lmop_monster(monster)
                    self.cache[cache_key] = formatted
                    self._save_to_cache(cache_key, formatted)
                    return formatted
                
                # 通过中文映射匹配
                cn_name = MONSTER_NAME_CN.get(name_lower)
                if cn_name and monster_name_cn == cn_name.lower():
                    formatted = self._format_lmop_monster(monster)
                    self.cache[cache_key] = formatted
                    self._save_to_cache(cache_key, formatted)
                    return formatted
        
        # 4. 从完整的5etools怪物数据查找
        full_monsters_path = SKILL_DATA / "5etools" / "core" / "monsters" / "monsters.json"
        if full_monsters_path.exists():
            try:
                with open(full_monsters_path, 'r', encoding='utf-8') as f:
                    all_monsters = json.load(f)
                
                for monster in all_monsters:
                    # 匹配怪物名称（英文）
                    if monster.get("name", "").lower() == name_lower:
                        # 转换为统一格式
                        result = self._format_monster_data(monster)
                        self.cache[cache_key] = result
                        self._save_to_cache(cache_key, result)
                        return result
            except Exception as e:
                print(f"⚠️ 读取完整怪物数据失败: {e}")
        
        # 5. 从索引查找（备用）
        idx = self.index.get("monsters", {})
        if name_lower in idx:
            info = idx[name_lower]
            result = {
                "name_en": info.get("name_en", ""),
                "name_cn": info.get("name_cn", ""),
                "cr": info.get("cr", "0"),
                "type": info.get("type", ""),
                "size": info.get("size", ""),
                "source": info.get("source", ""),
                "_note": "完整数据需要从源文件加载"
            }
            self.cache[cache_key] = result
            return result
        
        return None
    
    def _format_monster_data(self, raw_monster: Dict) -> Dict:
        """将原始5etools怪物数据格式化为统一格式"""
        # 解析AC
        ac_data = raw_monster.get("ac", [{}])
        if isinstance(ac_data, list) and len(ac_data) > 0:
            ac = ac_data[0].get("ac", 10) if isinstance(ac_data[0], dict) else ac_data[0]
        else:
            ac = ac_data
        
        # 解析HP
        hp_data = raw_monster.get("hp", {})
        hp_average = hp_data.get("average", 0)
        hp_formula = hp_data.get("formula", "")
        
        # 解析速度
        speed_data = raw_monster.get("speed", {})
        if isinstance(speed_data, dict):
            walk_speed = speed_data.get("walk", 0)
        else:
            walk_speed = speed_data
        
        # 解析属性值
        abilities = raw_monster.get("abilities", {})
        
        # 解析CR
        cr_data = raw_monster.get("cr", "0")
        if isinstance(cr_data, dict):
            cr = cr_data.get("cr", "0")
        else:
            cr = cr_data
        
        # 构建动作列表
        actions_text = raw_monster.get("actions", "")
        
        # 获取中文名称
        name_en = raw_monster.get("name", "")
        name_cn = MONSTER_NAME_CN.get(name_en.lower(), name_en)
        
        return {
            "name_en": name_en,
            "name_cn": name_cn,
            "size": raw_monster.get("size", ""),
            "type": raw_monster.get("type", ""),
            "ac": ac,
            "hp": f"{hp_average} ({hp_formula})",
            "speed": walk_speed,
            "abilities": {
                "str": abilities.get("str", 10),
                "dex": abilities.get("dex", 10),
                "con": abilities.get("con", 10),
                "int": abilities.get("int", 10),
                "wis": abilities.get("wis", 10),
                "cha": abilities.get("cha", 10),
            },
            "cr": str(cr),
            "actions": actions_text,
            "traits": raw_monster.get("traits", ""),
            "source": raw_monster.get("source", ""),
        }
    
    def _format_lmop_monster(self, monster: Dict) -> Dict:
        """格式化LMOP怪物数据，解析5etools格式的动作描述"""
        # 解析动作，将5etools格式转换为可读格式
        actions = monster.get("actions", [])
        formatted_actions = []
        
        for action in actions:
            name = action.get("name", "")
            desc = action.get("description", "")
            
            # 解析5etools格式的攻击描述
            # 例如: "{@atk mw} {@hit 3} to hit, reach 5 ft., one target. {@h}4 ({@damage 1d6 + 1}) bludgeoning damage."
            attack_info = self._parse_action_description(desc)
            
            formatted_actions.append({
                "name": name,
                "description": desc,
                "attack_bonus": attack_info.get("attack_bonus"),
                "damage": attack_info.get("damage"),
                "reach": attack_info.get("reach"),
                "parsed": attack_info.get("parsed_text", "")
            })
        
        # 复制怪物数据并添加格式化后的动作
        result = dict(monster)
        result["formatted_actions"] = formatted_actions
        
        return result
    
    def _parse_action_description(self, desc: str) -> Dict:
        """解析5etools格式的动作描述"""
        import re
        
        result = {
            "attack_bonus": None,
            "damage": None,
            "reach": None,
            "parsed_text": ""
        }
        
        if not desc:
            return result
        
        # 解析攻击加值 {@hit X}
        hit_match = re.search(r'\{@hit\s+(\+?\d+)\}', desc)
        if hit_match:
            result["attack_bonus"] = int(hit_match.group(1))
        
        # 解析伤害 {@damage XdY + Z}
        damage_match = re.search(r'\{@damage\s+([^}]+)\}', desc)
        if damage_match:
            result["damage"] = damage_match.group(1)
        
        # 解析射程 reach X ft.
        reach_match = re.search(r'reach\s+(\d+)\s*ft?', desc)
        if reach_match:
            result["reach"] = f"{reach_match.group(1)}尺"
        
        # 生成人类可读的描述
        parsed = desc
        # 替换5etools标记
        parsed = re.sub(r'\{@atk\s+([^}]+)\}', r'[\1]', parsed)
        parsed = re.sub(r'\{@hit\s+([^}]+)\}', r'命中+\1', parsed)
        parsed = re.sub(r'\{@damage\s+([^}]+)\}', r'\1', parsed)
        parsed = re.sub(r'\{@h\}', '命中时:', parsed)
        parsed = re.sub(r'\{@dc\s+(\d+)\}', r'DC\1', parsed)
        parsed = re.sub(r'\{@condition\s+([^}]+)\}', r'\1', parsed)
        parsed = re.sub(r'\{@spell\s+([^}]+)\}', r'\1', parsed)
        
        result["parsed_text"] = parsed
        
        return result
    
    def find_spell(self, name: str) -> Optional[Dict]:
        """
        查找法术
        
        Args:
            name: 法术名称（英文）
        
        Returns:
            法术数据字典
        """
        name_lower = name.lower()
        cache_key = f"spell:{name_lower}"
        
        # 检查缓存
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]
        
        cached = self._load_from_cache(cache_key)
        if cached:
            self.cache[cache_key] = cached
            return cached
        
        # 从提取的数据查找
        self.cache_misses += 1
        if self._extracted_data:
            for spell in self._extracted_data.get("spells", []):
                if spell.get("name_en", "").lower() == name_lower:
                    self.cache[cache_key] = spell
                    self._save_to_cache(cache_key, spell)
                    return spell
        
        return None
    
    def find_condition(self, name: str) -> Optional[Dict]:
        """查找状态条件"""
        name_lower = name.lower()
        cache_key = f"condition:{name_lower}"
        
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]
        
        cached = self._load_from_cache(cache_key)
        if cached:
            self.cache[cache_key] = cached
            return cached
        
        self.cache_misses += 1
        if self._extracted_data:
            for cond in self._extracted_data.get("conditions", []):
                if (cond.get("name_en", "").lower() == name_lower or
                    cond.get("name_cn", "").lower() == name_lower):
                    self.cache[cache_key] = cond
                    self._save_to_cache(cache_key, cond)
                    return cond
        
        return None
    
    def find_action(self, name: str) -> Optional[Dict]:
        """查找战斗动作"""
        name_lower = name.lower()
        cache_key = f"action:{name_lower}"
        
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]
        
        cached = self._load_from_cache(cache_key)
        if cached:
            self.cache[cache_key] = cached
            return cached
        
        self.cache_misses += 1
        if self._extracted_data:
            for action in self._extracted_data.get("actions", []):
                if (action.get("name_en", "").lower() == name_lower or
                    action.get("name_cn", "").lower() == name_lower):
                    self.cache[cache_key] = action
                    self._save_to_cache(cache_key, action)
                    return action
        
        return None
    
    def find_feat(self, name: str) -> Optional[Dict]:
        """查找专长"""
        name_lower = name.lower()
        cache_key = f"feat:{name_lower}"
        
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]
        
        cached = self._load_from_cache(cache_key)
        if cached:
            self.cache[cache_key] = cached
            return cached
        
        self.cache_misses += 1
        if self._extracted_data:
            for feat in self._extracted_data.get("feats", []):
                if (feat.get("name_en", "").lower() == name_lower or
                    feat.get("name_cn", "").lower() == name_lower):
                    self.cache[cache_key] = feat
                    self._save_to_cache(cache_key, feat)
                    return feat
        
        return None
    
    # ============ 搜索方法 ============
    
    def search_monsters(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索怪物（模糊匹配）
        
        Args:
            query: 搜索关键词
            limit: 返回结果数量上限
        
        Returns:
            匹配的怪物列表
        """
        query_lower = query.lower()
        results = []
        
        # 从LMOP数据搜索
        if self._lmop_data:
            for monster in self._lmop_data:
                if (query_lower in monster.get("name_en", "").lower() or
                    query_lower in monster.get("name_cn", "").lower()):
                    results.append({
                        "name_en": monster.get("name_en", ""),
                        "name_cn": monster.get("name_cn", ""),
                        "cr": monster.get("cr", "0"),
                        "type": monster.get("type", "")
                    })
                    if len(results) >= limit:
                        break
        
        # 从索引搜索
        if len(results) < limit:
            idx = self.index.get("monsters", {})
            for name, info in idx.items():
                if query_lower in name:
                    # 避免重复
                    if not any(r.get("name_en", "").lower() == name for r in results):
                        results.append({
                            "name_en": info.get("name_en", name),
                            "name_cn": info.get("name_cn", ""),
                            "cr": info.get("cr", "0"),
                            "type": info.get("type", "")
                        })
                        if len(results) >= limit:
                            break
        
        return results
    
    def search_spells(self, query: str, level: Optional[int] = None, limit: int = 10) -> List[Dict]:
        """
        搜索法术
        
        Args:
            query: 搜索关键词
            level: 指定环数（可选）
            limit: 返回结果数量上限
        """
        query_lower = query.lower()
        results = []
        
        if self._extracted_data:
            for spell in self._extracted_data.get("spells", []):
                if query_lower in spell.get("name_en", "").lower():
                    if level is not None and spell.get("level") != level:
                        continue
                    results.append({
                        "name_en": spell.get("name_en", ""),
                        "name_cn": spell.get("name_cn", ""),
                        "level": spell.get("level", 0),
                        "school": spell.get("school_cn", "")
                    })
                    if len(results) >= limit:
                        break
        
        return results
    
    def list_spells_by_level(self, level: int) -> List[Dict]:
        """按环数列出法术"""
        results = []
        if self._extracted_data:
            for spell in self._extracted_data.get("spells", []):
                if spell.get("level") == level:
                    results.append(spell)
        return results
    
    def get_all_conditions(self) -> List[Dict]:
        """获取所有状态条件"""
        if self._extracted_data:
            return self._extracted_data.get("conditions", [])
        return []
    
    def get_all_actions(self) -> List[Dict]:
        """获取所有战斗动作"""
        if self._extracted_data:
            return self._extracted_data.get("actions", [])
        return []
    
    # ============ 缓存管理 ============
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "memory_cache_size": len(self.cache),
            "disk_cache_size": len(list(CACHE_DIR.glob("*.json"))) if CACHE_DIR.exists() else 0
        }
    
    def clear_cache(self):
        """清除所有缓存"""
        self.cache.clear()
        if CACHE_DIR.exists():
            for f in CACHE_DIR.glob("*.json"):
                f.unlink()
        print("[Info] 缓存已清除")
    
    def preload_common_data(self):
        """预加载常用数据到内存"""
        common_monsters = ["goblin", "bugbear", "wolf", "zombie"]
        common_spells = ["fireball", "magic missile", "healing word", "shield"]
        
        print("[Info] 预加载常用数据...")
        for name in common_monsters:
            self.find_monster(name)
        for name in common_spells:
            self.find_spell(name)
        print("[Info] 预加载完成")


# ============ 便捷函数 ============

_manager = None

def get_manager() -> DnDDataManager:
    """获取数据管理器单例"""
    global _manager
    if _manager is None:
        _manager = DnDDataManager()
    return _manager

def find_monster(name: str) -> Optional[Dict]:
    """便捷函数：查找怪物"""
    return get_manager().find_monster(name)

def find_spell(name: str) -> Optional[Dict]:
    """便捷函数：查找法术"""
    return get_manager().find_spell(name)

def find_condition(name: str) -> Optional[Dict]:
    """便捷函数：查找状态条件"""
    return get_manager().find_condition(name)

def find_action(name: str) -> Optional[Dict]:
    """便捷函数：查找战斗动作"""
    return get_manager().find_action(name)

def find_feat(name: str) -> Optional[Dict]:
    """便捷函数：查找专长"""
    return get_manager().find_feat(name)

def search_monsters(query: str, limit: int = 10) -> List[Dict]:
    """便捷函数：搜索怪物"""
    return get_manager().search_monsters(query, limit)

def search_spells(query: str, level: Optional[int] = None, limit: int = 10) -> List[Dict]:
    """便捷函数：搜索法术"""
    return get_manager().search_spells(query, level, limit)


if __name__ == "__main__":
    # 测试
    print("=" * 60)
    print("D&D 5e 数据管理器测试")
    print("=" * 60)
    print()
    
    dm = DnDDataManager()
    
    # 测试查找法术
    print("查找法术 'Fireball':")
    spell = find_spell("Fireball")
    if spell:
        print(f"  ✓ 找到: {spell['name_en']} ({spell['name_cn']})")
        print(f"    环数: {spell['level']}, 学派: {spell['school_cn']}")
        print(f"    施法时间: {spell['cast_time']}")
        print(f"    射程: {spell['range']}")
    else:
        print("  ✗ 未找到")
    
    print()
    
    # 测试查找怪物
    print("查找怪物 'Evil Mage':")
    monster = find_monster("Evil Mage")
    if monster:
        print(f"  ✓ 找到: {monster['name_en']} ({monster['name_cn']})")
        print(f"    CR: {monster['cr']}, 类型: {monster['type']}")
        print(f"    AC: {monster['ac']}, HP: {monster['hp']}")
    else:
        print("  ✗ 未找到")
    
    print()
    
    # 测试查找状态
    print("查找状态 'blinded':")
    cond = find_condition("blinded")
    if cond:
        print(f"  ✓ 找到: {cond['name_en']} ({cond['name_cn']})")
        print(f"    来源: {cond['source']} p.{cond['page']}")
    else:
        print("  ✗ 未找到")
    
    print()
    
    # 测试搜索
    print("搜索 'magic':")
    results = search_spells("magic", limit=5)
    for r in results:
        print(f"  - {r['name_en']} ({r['name_cn']}) - {r['level']}环")
    
    print()
    
    # 缓存统计
    print("缓存统计:")
    stats = dm.get_cache_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")
