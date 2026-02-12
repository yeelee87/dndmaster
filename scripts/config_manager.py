#!/usr/bin/env python3
"""
D&D Game Configuration Manager
游戏配置管理器
管理激活的规则书、模组和设置
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    CONFIG_FILE = "config/active_module.json"
    
    # 支持的规则书
    AVAILABLE_RULEBOOKS = {
        "phb": {
            "name": "玩家手册 (Player's Handbook)",
            "description": "职业、种族、法术、战斗规则",
            "file": "references/core-rules/phb.md"
        },
        "mm": {
            "name": "怪物手册 (Monster Manual)",
            "description": "怪物数据、特殊能力",
            "file": "references/core-rules/mm.md"
        },
        "dmg": {
            "name": "DM指南 (Dungeon Master's Guide)",
            "description": "世界构建、魔法物品、规则裁定",
            "file": "references/core-rules/dmg.md"
        }
    }
    
    # 支持的模组（可扩展）
    AVAILABLE_MODULES = {
        "lost-mine-phandelver": {
            "name": "凡戴尔的失落矿坑 (Lost Mine of Phandelver)",
            "description": "适合1-5级角色的入门模组",
            "file": "references/modules/lost-mine-phandelver.md",
            "level_range": "1-5"
        },
        "dragon-heist": {
            "name": "龙金劫 (Dragon Heist)",
            "description": "城市冒险模组，寻找龙藏宝藏",
            "file": "references/modules/dragon-heist.md",
            "level_range": "1-5"
        },
        "curse-of-strahd": {
            "name": "施特拉德的诅咒 (Curse of Strahd)",
            "description": "哥特式恐怖模组，挑战吸血鬼领主",
            "file": "references/modules/curse-of-strahd.md",
            "level_range": "1-10"
        },
        "custom": {
            "name": "自定义模组",
            "description": "用户提供的自定义模组",
            "file": "references/modules/custom.md",
            "level_range": "任意"
        }
    }
    
    # 人物卡格式
    CHARACTER_FORMATS = {
        "excel": {
            "name": "Excel (.xlsx)",
            "extensions": [".xlsx", ".xls"],
            "description": "标准Excel人物卡表格"
        },
        "json": {
            "name": "JSON",
            "extensions": [".json"],
            "description": "JSON格式角色数据"
        }
    }
    
    def __init__(self, skill_path: str = "."):
        """
        初始化配置管理器
        
        Args:
            skill_path: Skill根目录路径
        """
        self.skill_path = Path(skill_path)
        self.config_path = self.skill_path / self.CONFIG_FILE
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 加载配置失败: {e}，使用默认配置")
        
        return self.get_default_config()
    
    def save_config(self):
        """保存配置文件"""
        try:
            # 确保目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "rulebooks": {
                "phb": True,
                "mm": True,
                "dmg": False
            },
            "active_module": None,
            "character_format": "excel",
            "game_settings": {
                "strict_rules": True,  # 严格遵守规则
                "show_calculations": True,  # 显示计算过程
                "auto_save": True,  # 自动保存进度
                "death_save_required": True  # 需要死亡豁免
            },
            "campaign_progress": {
                "current_module": None,
                "current_chapter": None,
                "completed_encounters": [],
                "party_xp": 0
            },
            "characters": []  # 当前队伍角色列表
        }
    
    def get_active_rulebooks(self) -> List[str]:
        """获取激活的规则书列表"""
        active = []
        for key, enabled in self.config.get("rulebooks", {}).items():
            if enabled and key in self.AVAILABLE_RULEBOOKS:
                active.append(key)
        return active
    
    def get_active_module(self) -> Optional[str]:
        """获取激活的模组"""
        return self.config.get("active_module")
    
    def get_rulebook_info(self, rulebook_key: str) -> Optional[Dict[str, str]]:
        """获取规则书信息"""
        return self.AVAILABLE_RULEBOOKS.get(rulebook_key)
    
    def get_module_info(self, module_key: str) -> Optional[Dict[str, str]]:
        """获取模组信息"""
        return self.AVAILABLE_MODULES.get(module_key)
    
    def set_rulebook(self, rulebook: str, enabled: bool):
        """设置规则书启用状态"""
        if rulebook not in self.AVAILABLE_RULEBOOKS:
            return False
        
        if "rulebooks" not in self.config:
            self.config["rulebooks"] = {}
        
        self.config["rulebooks"][rulebook] = enabled
        return self.save_config()
    
    def set_active_module(self, module: str):
        """设置激活的模组"""
        if module not in self.AVAILABLE_MODULES:
            return False
        
        self.config["active_module"] = module
        self.config["campaign_progress"]["current_module"] = module
        return self.save_config()
    
    def set_character_format(self, format_type: str):
        """设置人物卡格式"""
        if format_type not in self.CHARACTER_FORMATS:
            return False
        
        self.config["character_format"] = format_type
        return self.save_config()
    
    def add_character(self, character_data: Dict[str, Any]):
        """添加角色到队伍"""
        if "characters" not in self.config:
            self.config["characters"] = []
        
        self.config["characters"].append(character_data)
        return self.save_config()
    
    def update_campaign_progress(self, chapter: str, encounter: str = None, xp: int = 0):
        """更新战役进度"""
        progress = self.config.get("campaign_progress", {})
        progress["current_chapter"] = chapter
        
        if encounter:
            completed = progress.get("completed_encounters", [])
            if encounter not in completed:
                completed.append(encounter)
            progress["completed_encounters"] = completed
        
        if xp > 0:
            progress["party_xp"] = progress.get("party_xp", 0) + xp
        
        self.config["campaign_progress"] = progress
        return self.save_config()
    
    def get_setup_prompt(self) -> str:
        """生成配置设置的提示文本"""
        lines = [
            "🎲 【D&D 5e 游戏设置】",
            "",
            "请先选择要使用的规则书和模组：",
            "",
            "📚 【规则书】（可多选）",
        ]
        
        current_rulebooks = self.config.get("rulebooks", {})
        for key, info in self.AVAILABLE_RULEBOOKS.items():
            enabled = current_rulebooks.get(key, False)
            status = "✅" if enabled else "⬜"
            lines.append(f"{status} [{key}] {info['name']} - {info['description']}")
        
        lines.append("")
        lines.append("📖 【模组】（单选）")
        
        current_module = self.get_active_module()
        for key, info in self.AVAILABLE_MODULES.items():
            selected = "🎯" if current_module == key else "⭕"
            lines.append(f"{selected} [{key}] {info['name']} ({info['level_range']}级) - {info['description']}")
        
        lines.append("")
        lines.append("📋 【人物卡格式】")
        current_format = self.config.get("character_format", "excel")
        for key, info in self.CHARACTER_FORMATS.items():
            selected = "✅" if current_format == key else "⭕"
            lines.append(f"{selected} [{key}] {info['name']} - {info['description']}")
        
        lines.append("")
        lines.append("请回复选择的配置，例如：")
        lines.append("`规则书: phb, mm`")
        lines.append("`模组: lost-mine-phandelver`")
        lines.append("`人物卡: excel`")
        
        return "\n".join(lines)
    
    def apply_setup(self, rulebooks: List[str], module: str, character_format: str) -> bool:
        """应用配置设置"""
        # 设置规则书
        for key in self.AVAILABLE_RULEBOOKS.keys():
            self.set_rulebook(key, key in rulebooks)
        
        # 设置模组
        if module:
            self.set_active_module(module)
        
        # 设置人物卡格式
        if character_format:
            self.set_character_format(character_format)
        
        return self.save_config()
    
    def get_reference_files(self) -> List[str]:
        """获取需要加载的参考文件列表"""
        files = []
        
        # 添加激活的规则书
        for rulebook in self.get_active_rulebooks():
            info = self.get_rulebook_info(rulebook)
            if info:
                file_path = self.skill_path / info["file"]
                if file_path.exists():
                    files.append(str(file_path))
        
        # 添加激活的模组
        module = self.get_active_module()
        if module:
            info = self.get_module_info(module)
            if info:
                file_path = self.skill_path / info["file"]
                if file_path.exists():
                    files.append(str(file_path))
        
        return files
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        # 至少需要一个规则书和模组
        has_rulebook = len(self.get_active_rulebooks()) > 0
        has_module = self.get_active_module() is not None
        return has_rulebook and has_module


def parse_setup_response(response: str) -> Dict[str, Any]:
    """
    解析用户配置回复
    
    支持的格式：
    - 规则书: phb, mm
    - 模组: lost-mine-phandelver
    - 人物卡: excel
    """
    result = {
        "rulebooks": [],
        "module": None,
        "character_format": None
    }
    
    lines = response.strip().split("\n")
    
    for line in lines:
        line = line.strip().lower()
        
        if "规则书" in line or "rulebook" in line:
            # 提取规则书
            if ":" in line:
                books = line.split(":")[1].strip()
                result["rulebooks"] = [b.strip() for b in books.split(",")]
        
        elif "模组" in line or "module" in line:
            # 提取模组
            if ":" in line:
                result["module"] = line.split(":")[1].strip()
        
        elif "人物卡" in line or "character" in line:
            # 提取人物卡格式
            if ":" in line:
                result["character_format"] = line.split(":")[1].strip()
    
    return result


if __name__ == "__main__":
    print("⚙️ D&D 配置管理器测试")
    print("=" * 50)
    
    # 创建配置管理器
    config = ConfigManager("/Users/sid/.openclaw/workspace/skills/dnd-game-master")
    
    # 显示当前配置
    print("\n【当前配置】")
    print(f"激活规则书: {config.get_active_rulebooks()}")
    print(f"激活模组: {config.get_active_module()}")
    print(f"人物卡格式: {config.config.get('character_format')}")
    
    # 显示设置提示
    print("\n" + config.get_setup_prompt())
