#!/usr/bin/env python3
"""
LMOP 模组章节管理器
按章节组织模组内容，支持当前章节追踪和回查
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

class LMOPChapterManager:
    """LMOP模组章节管理器"""
    
    # LMOP章节定义
    CHAPTERS = {
        "part1": {
            "name": "第一部分：地精箭矢",
            "name_en": "Part 1: Goblin Arrows",
            "sections": [
                {"id": "ambush", "name": "地精伏击", "level_range": "1级"},
                {"id": "hideout", "name": "克拉摩窝点", "level_range": "1级"}
            ],
            "key_npcs": ["刚铎·寻岩者", "修达·霍温特"],
            "key_locations": ["三猪小径", "克拉摩窝点"],
            "level_range": "1级"
        },
        "part2": {
            "name": "第二部分：凡达林",
            "name_en": "Part 2: Phandalin", 
            "sections": [
                {"id": "town_arrival", "name": "抵达小镇", "level_range": "1-2级"},
                {"id": "town_exploration", "name": "探索小镇", "level_range": "1-2级"},
                {"id": "redbrand_racket", "name": "红标帮威胁", "level_range": "2级"},
                {"id": "tresendar_manor", "name": "崔森德庄园", "level_range": "2级"}
            ],
            "key_npcs": [
                "埃尔马·巴森", "林妮·灰风", "哈宾·维斯特",
                "奎琳·艾德玛夫", "达兰·艾德玛斯", "雷多思",
                "哈利娅·桑顿", "修达·霍温特", "西里尔·阿卡"
            ],
            "key_locations": [
                "石丘旅馆", "巴森补给", "狮盾小贩",
                "镇长办公室", "矿工交易所", "艾德莱夫农场",
                "艾德玛斯果园", "崔森德庄园"
            ],
            "level_range": "1-2级"
        },
        "part3": {
            "name": "第三部分：蜘蛛网",
            "name_en": "Part 3: The Spider's Web",
            "sections": [
                {"id": "old_owl_well", "name": "老 Owl Well", "level_range": "2-3级"},
                {"id": "thundertree", "name": "桑德树废墟", "level_range": "3级"},
                {"id": "wyvern_tor", "name": "飞龙突岩", "level_range": "3级"},
                {"id": "cragmaw_castle", "name": "克拉摩堡", "level_range": "3-4级"}
            ],
            "key_npcs": ["雷多思", "绿龙韦诺弥尔", "内兹纳（黑蜘蛛）"],
            "key_locations": [
                "老 Owl Well", "扭木林", "桑德树废墟",
                "飞龙突岩", "克拉摩堡"
            ],
            "level_range": "2-4级"
        },
        "part4": {
            "name": "第四部分：回声洞",
            "name_en": "Part 4: Wave Echo Cave",
            "sections": [
                {"id": "wave_echo_cave", "name": "回声洞", "level_range": "4-5级"}
            ],
            "key_npcs": ["内兹纳（黑蜘蛛）", "刚铎·寻岩者"],
            "key_locations": ["回声洞", "法术锻造厂"],
            "level_range": "4-5级"
        }
    }
    
    def __init__(self, data_dir: str = None):
        """初始化章节管理器"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.skill_dir = self.data_dir.parent
        self.chapters_dir = self.data_dir / "lmop_chapters"
        self.state_file = self.data_dir / "campaign_state.json"
        self.config_file = self.skill_dir / "config" / "active_module.json"
        
        # 确保目录存在
        self.chapters_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载或初始化战役状态
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载战役状态
        
        根据时间戳选择最新的存档：
        1. 读取 data/campaign_state.json（专用状态文件）
        2. 读取 config/active_module.json 中的 campaign_progress
        3. 比较两者的时间戳，选择最新的有效存档
        4. 如果没有存档，使用默认状态
        """
        state_from_file = None
        state_from_config = None
        
        # 1. 尝试从专用状态文件读取
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    if self._is_valid_state(state):
                        state_from_file = state
            except Exception as e:
                print(f"⚠️ 读取 campaign_state.json 失败: {e}")
        
        # 2. 尝试从配置文件读取
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    progress = config.get("campaign_progress", {})
                    if progress.get("current_chapter"):
                        state_from_config = self._convert_progress_to_state(progress)
            except Exception as e:
                print(f"⚠️ 读取 active_module.json 失败: {e}")
        
        # 3. 比较时间戳，选择最新的存档
        if state_from_file and state_from_config:
            # 获取两个存档的时间戳
            time_file = self._parse_timestamp(state_from_file.get("last_saved"))
            time_config = self._parse_timestamp(state_from_config.get("last_saved"))
            
            if time_file and time_config:
                # 两个都有时间戳，选择更新的
                if time_file >= time_config:
                    print(f"📂 从 campaign_state.json 加载存档 (时间: {state_from_file.get('last_saved')})")
                    return state_from_file
                else:
                    print(f"📂 从 active_module.json 加载存档 (时间: {state_from_config.get('last_saved')})")
                    return state_from_config
            elif time_file:
                # 只有文件有时间戳
                print(f"📂 从 campaign_state.json 加载存档 (时间: {state_from_file.get('last_saved')})")
                return state_from_file
            elif time_config:
                # 只有配置有时间戳
                print(f"📂 从 active_module.json 加载存档 (时间: {state_from_config.get('last_saved')})")
                return state_from_config
            else:
                # 都没有时间戳，默认使用文件
                print("📂 从 campaign_state.json 加载存档 (无时间戳)")
                return state_from_file
        
        # 4. 只有一个存档存在
        if state_from_file:
            print("📂 从 campaign_state.json 加载存档")
            return state_from_file
        if state_from_config:
            print("📂 从 active_module.json 加载存档")
            return state_from_config
        
        # 5. 没有存档，使用默认状态
        print("📂 使用默认初始状态")
        return self._get_default_state()
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """解析时间戳字符串为 datetime 对象"""
        if not timestamp_str:
            return None
        try:
            # 尝试 ISO 格式
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            try:
                # 尝试常见格式
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except:
                return None
    
    def _is_valid_state(self, state: Dict) -> bool:
        """验证状态是否完整有效"""
        required_keys = ["current_chapter", "current_section"]
        return all(key in state for key in required_keys)
    
    def _get_default_state(self) -> Dict:
        """获取默认状态"""
        return {
            "current_chapter": "part2",  # 默认从第二部分开始（新手友好）
            "current_section": "town_exploration",
            "completed_sections": [],
            "discovered_locations": [],
            "met_npcs": [],
            "active_quests": [],
            "completed_quests": [],
            "party_level": 2,
            "session_date": None,
            "last_saved": None  # 默认状态没有时间戳
        }
    
    def _convert_progress_to_state(self, progress: Dict) -> Dict:
        """将 config_manager 的 progress 转换为 state 格式"""
        chapter_map = {
            "goblin_arrows": "part1",
            "phandalin": "part2", 
            "spiders_web": "part3",
            "wave_echo_cave": "part4"
        }
        
        chapter = progress.get("current_chapter", "part2")
        # 转换章节名称
        if chapter in chapter_map:
            chapter = chapter_map[chapter]
        
        return {
            "current_chapter": chapter,
            "current_section": progress.get("current_section", "town_exploration"),
            "completed_sections": progress.get("completed_sections", []),
            "discovered_locations": progress.get("discovered_locations", []),
            "met_npcs": progress.get("met_npcs", []),
            "active_quests": progress.get("active_quests", []),
            "completed_quests": progress.get("completed_quests", []),
            "party_level": progress.get("party_level", 2),
            "session_date": progress.get("session_date"),
            "last_saved": progress.get("last_saved")  # 保留时间戳
        }
    
    def save_state(self):
        """保存战役状态
        
        同时保存到：
        1. data/campaign_state.json（专用状态文件）
        2. config/active_module.json（配置管理器使用的文件）
        
        每次保存都会记录当前时间戳，用于后续选择最新存档
        """
        # 记录当前时间戳
        current_time = datetime.now().isoformat()
        self.state["last_saved"] = current_time
        
        # 1. 保存到专用状态文件
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            print(f"💾 存档已保存到 campaign_state.json (时间: {current_time})")
        except Exception as e:
            print(f"⚠️ 保存 campaign_state.json 失败: {e}")
        
        # 2. 同步到配置文件（保持与 config_manager 兼容）
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # 更新 campaign_progress
            if "campaign_progress" not in config:
                config["campaign_progress"] = {}
            
            progress = config["campaign_progress"]
            progress["current_chapter"] = self.state.get("current_chapter")
            progress["current_section"] = self.state.get("current_section")
            progress["completed_sections"] = self.state.get("completed_sections", [])
            progress["discovered_locations"] = self.state.get("discovered_locations", [])
            progress["met_npcs"] = self.state.get("met_npcs", [])
            progress["active_quests"] = self.state.get("active_quests", [])
            progress["completed_quests"] = self.state.get("completed_quests", [])
            progress["party_level"] = self.state.get("party_level", 2)
            progress["session_date"] = self.state.get("session_date")
            progress["last_saved"] = current_time  # 同时记录时间戳到配置文件
            
            # 确保目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"💾 存档已同步到 active_module.json")
        except Exception as e:
            print(f"⚠️ 同步到 active_module.json 失败: {e}")
    
    def get_current_chapter(self) -> Dict:
        """获取当前章节信息"""
        chapter_id = self.state["current_chapter"]
        return {
            "id": chapter_id,
            **self.CHAPTERS[chapter_id]
        }
    
    def get_chapter(self, chapter_id: str) -> Optional[Dict]:
        """获取指定章节信息"""
        if chapter_id not in self.CHAPTERS:
            return None
        return {
            "id": chapter_id,
            **self.CHAPTERS[chapter_id]
        }
    
    def set_chapter(self, chapter_id: str) -> bool:
        """设置当前章节"""
        if chapter_id not in self.CHAPTERS:
            return False
        
        self.state["current_chapter"] = chapter_id
        # 默认切换到该章节的第一个section
        self.state["current_section"] = self.CHAPTERS[chapter_id]["sections"][0]["id"]
        self.save_state()
        return True
    
    def get_section_content(self, chapter_id: str = None, section_id: str = None) -> Optional[str]:
        """获取章节内容（从拆分的文件加载）"""
        if chapter_id is None:
            chapter_id = self.state["current_chapter"]
        if section_id is None:
            section_id = self.state["current_section"]
        
        content_file = self.chapters_dir / f"{chapter_id}_{section_id}.md"
        
        if not content_file.exists():
            return None
        
        with open(content_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_npcs_in_current_chapter(self) -> List[str]:
        """获取当前章节的关键NPC"""
        chapter = self.get_current_chapter()
        return chapter.get("key_npcs", [])
    
    def get_locations_in_current_chapter(self) -> List[str]:
        """获取当前章节的关键地点"""
        chapter = self.get_current_chapter()
        return chapter.get("key_locations", [])
    
    def mark_location_discovered(self, location: str):
        """标记地点已发现"""
        if location not in self.state["discovered_locations"]:
            self.state["discovered_locations"].append(location)
            self.save_state()
    
    def mark_npc_met(self, npc: str):
        """标记NPC已遇见"""
        if npc not in self.state["met_npcs"]:
            self.state["met_npcs"].append(npc)
            self.save_state()
    
    def add_quest(self, quest_name: str, quest_info: Dict):
        """添加任务"""
        self.state["active_quests"].append({
            "name": quest_name,
            **quest_info
        })
        self.save_state()
    
    def complete_quest(self, quest_name: str):
        """完成任务"""
        for quest in self.state["active_quests"]:
            if quest["name"] == quest_name:
                self.state["active_quests"].remove(quest)
                self.state["completed_quests"].append(quest)
                self.save_state()
                return True
        return False
    
    def get_dm_context(self) -> str:
        """获取DM运行时的上下文信息（仅包含当前和之前章节的相关信息）"""
        chapter = self.get_current_chapter()
        
        context = f"""
# 当前战役状态

## 当前章节：{chapter['name']}
- 等级范围：{chapter['level_range']}
- 当前区域：{self.state['current_section']}

## 本章节关键NPC（可能遇到）
{chr(10).join(['- ' + npc for npc in chapter['key_npcs']])}

## 本章节关键地点
{chr(10).join(['- ' + loc for loc in chapter['key_locations']])}

## 已发现的地点
{chr(10).join(['- ' + loc for loc in self.state['discovered_locations']]) if self.state['discovered_locations'] else '（无）'}

## 已遇见的NPC
{chr(10).join(['- ' + npc for npc in self.state['met_npcs']]) if self.state['met_npcs'] else '（无）'}

## 进行中的任务
"""
        for quest in self.state["active_quests"]:
            context += f"- {quest['name']}\n"
        
        if not self.state["active_quests"]:
            context += "（无）\n"
        
        return context
    
    def list_all_chapters(self) -> List[Dict]:
        """列出所有章节"""
        return [
            {"id": ch_id, **ch_info}
            for ch_id, ch_info in self.CHAPTERS.items()
        ]
    
    def can_access_chapter(self, chapter_id: str) -> bool:
        """检查是否可以访问某章节（只能访问当前和之前的章节）"""
        chapter_order = ["part1", "part2", "part3", "part4"]
        current_idx = chapter_order.index(self.state["current_chapter"])
        target_idx = chapter_order.index(chapter_id)
        return target_idx <= current_idx


if __name__ == "__main__":
    # 测试
    manager = LMOPChapterManager()
    
    print("=== 当前章节 ===")
    chapter = manager.get_current_chapter()
    print(f"章节：{chapter['name']}")
    print(f"NPC：{', '.join(chapter['key_npcs'][:3])}...")
    
    print("\n=== DM上下文 ===")
    print(manager.get_dm_context())
