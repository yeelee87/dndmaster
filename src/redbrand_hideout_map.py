#!/usr/bin/env python3
"""
红标帮窝点 - 探索地图系统
支持战争迷雾（Fog of War）和区域标记
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class MapArea:
    """地图区域"""
    id: str
    name: str
    name_en: str
    description: str
    connected_to: List[str]  # 连接的区域ID
    discovered: bool = False
    explored: bool = False  # 完全探索
    notes: str = ""  # DM笔记（陷阱、敌人等）
    visible_features: List[str] = None  # 玩家可见特征
    
    def __post_init__(self):
        if self.visible_features is None:
            self.visible_features = []

@dataclass
class MapEntity:
    """地图上的实体（敌人、物品等）"""
    name: str
    type: str  # enemy, trap, item, npc
    location: str  # 区域ID
    status: str = "active"  # active, defeated, disabled
    description: str = ""
    hidden: bool = True  # 是否隐藏（需要侦查发现）

class RedbrandHideoutMap:
    """红标帮窝点地图管理器"""
    
    # 红标帮窝点23个区域定义
    AREAS = {
        # 入口区域
        "area_1": MapArea(
            id="area_1",
            name="地窖入口",
            name_en="Cellar Entrance",
            description="从庄园废墟下来的石阶，通向地窖。",
            connected_to=["area_2"],
            visible_features=["石阶", "酒桶"]
        ),
        "area_2": MapArea(
            id="area_2",
            name="储藏地窖",
            name_en="Storage Cellar",
            description="堆满酒桶和补给品的地窖房间。",
            connected_to=["area_1", "area_3", "area_4"],
            visible_features=["酒桶", "木箱", "通往西边的门", "通往东边的门"]
        ),
        "area_3": MapArea(
            id="area_3",
            name="腐败储藏室",
            name_en="Tainted storeroom",
            description="堆满变质食物和腐臭物质的储藏室。",
            connected_to=["area_2"],
            visible_features=["腐烂的食物", "恶臭"]
        ),
        
        # 西侧区域
        "area_4": MapArea(
            id="area_4",
            name="大厅",
            name_en="Hallway",
            description="连接各区域的主走廊。",
            connected_to=["area_2", "area_5", "area_6"],
            visible_features=["石墙", "火把"]
        ),
        "area_5": MapArea(
            id="area_5",
            name="兵营",
            name_en="Barracks",
            description="红标帮成员睡觉和休息的地方，有几张简陋的床铺。",
            connected_to=["area_4"],
            visible_features=["床铺", "武器架", "私人物品"]
        ),
        "area_6": MapArea(
            id="area_6",
            name="陷阱走廊",
            name_en="Trapped Hall",
            description="一条看似普通但暗藏陷阱的走廊。",
            connected_to=["area_4", "area_7"],
            visible_features=["石地板", "墙壁上的裂缝"]
        ),
        "area_7": MapArea(
            id="area_7",
            name="秘门房间",
            name_en="Secret Room",
            description="隐藏的房间，有通往更深处的密门。",
            connected_to=["area_6", "area_8"],
            visible_features=["书架", "秘密门（被发现后）"]
        ),
        
        # 中央区域
        "area_8": MapArea(
            id="area_8",
            name="洞穴隧道",
            name_en="Cavern Tunnel",
            description="从庄园后方通入的天然洞穴隧道。",
            connected_to=["area_7", "area_9", "area_10"],
            visible_features=["岩石墙壁", "泥土地面"]
        ),
        "area_9": MapArea(
            id="area_9",
            name="赌博洞穴",
            name_en="Gambling Den",
            description="红标帮成员赌博和消遣的小洞穴。",
            connected_to=["area_8"],
            visible_features=["木箱", "骰子", "酒桶", "烛光"]
        ),
        "area_10": MapArea(
            id="area_10",
            name="裂隙边缘",
            name_en="Crevasse Edge",
            description="洞穴边缘有巨大的裂隙，深不见底。",
            connected_to=["area_8", "area_11"],
            visible_features=["巨大裂隙", "狭窄的岩石桥"]
        ),
        "area_11": MapArea(
            id="area_11",
            name="自然洞穴",
            name_en="Natural Cavern",
            description="未加工的天然洞穴，有钟乳石。",
            connected_to=["area_10", "area_12"],
            visible_features=["钟乳石", "潮湿地面"]
        ),
        
        # 东侧区域
        "area_12": MapArea(
            id="area_12",
            name="墓室",
            name_en="Crypt",
            description="古老的墓室，石棺排列在墙壁旁。",
            connected_to=["area_11", "area_13"],
            visible_features=["石棺", "古老的雕刻"]
        ),
        "area_13": MapArea(
            id="area_13",
            name="奴隶围栏",
            name_en="Slave Pens",
            description="关押囚犯的牢笼区域。",
            connected_to=["area_12", "area_14"],
            visible_features=["铁笼", "锁链", "稻草床铺"]
        ),
        "area_14": MapArea(
            id="area_14",
            name="守卫室",
            name_en="Guard Room",
            description="通往更深处的主要守卫位置。",
            connected_to=["area_13", "area_15", "area_16"],
            visible_features=["桌子", "椅子", "火把"]
        ),
        
        # 北侧区域 - 玻璃杖居所
        "area_15": MapArea(
            id="area_15",
            name="起居室",
            name_en="Living Area",
            description="较为舒适的居住区域，有家具和书籍。",
            connected_to=["area_14", "area_17"],
            visible_features=["桌椅", "书架", "地毯"]
        ),
        "area_16": MapArea(
            id="area_16",
            name="储藏室",
            name_en="Armory",
            description="存放武器和装备的房间。",
            connected_to=["area_14"],
            visible_features=["武器架", "木箱", "护甲"]
        ),
        "area_17": MapArea(
            id="area_17",
            name="卧室",
            name_en="Bedroom",
            description="玻璃杖的私人卧室。",
            connected_to=["area_15", "area_18"],
            visible_features=["床", "衣柜", "书桌"]
        ),
        "area_18": MapArea(
            id="area_18",
            name="研究室",
            name_en="Laboratory",
            description="玻璃杖研究法术的房间，有各种炼金器材。",
            connected_to=["area_17"],
            visible_features=["炼金器材", "书籍", "法器"]
        ),
        
        # 其他连接
        "area_19": MapArea(
            id="area_19",
            name="储藏洞穴",
            name_en="Storage Cave",
            description="堆放杂物的洞穴。",
            connected_to=["area_11"],
            visible_features=["木箱", "桶", "杂物"]
        ),
        "area_20": MapArea(
            id="area_20",
            name="地下河",
            name_en="Underground River",
            description="地下河流经的洞穴，水声回荡。",
            connected_to=["area_11"],
            visible_features=["地下河", "潮湿的岩石"]
        ),
        
        # 补充区域
        "area_21": MapArea(
            id="area_21",
            name="侧室",
            name_en="Side Chamber",
            description="小型的侧室。",
            connected_to=["area_4"],
            visible_features=["石墙", "空房间"]
        ),
        "area_22": MapArea(
            id="area_22",
            name="暗门通道",
            name_en="Secret Passage",
            description="隐藏的通道。",
            connected_to=["area_7"],
            visible_features=["狭窄的通道"]
        ),
        "area_23": MapArea(
            id="area_23",
            name="逃生隧道",
            name_en="Escape Tunnel",
            description="通往庄园外的秘密逃生隧道。",
            connected_to=["area_8"],
            visible_features=["狭窄的隧道", "向上的阶梯"]
        ),
    }
    
    def __init__(self, save_file: str = None):
        """初始化地图"""
        self.areas = {k: v for k, v in self.AREAS.items()}
        self.entities: List[MapEntity] = []
        self.player_location = None
        
        if save_file:
            self.save_file = Path(save_file)
            self.load_state()
        else:
            self.save_file = None
    
    def discover_area(self, area_id: str, notes: str = ""):
        """发现区域"""
        if area_id in self.areas:
            self.areas[area_id].discovered = True
            if notes:
                self.areas[area_id].notes = notes
            self.save_state()
    
    def explore_area(self, area_id: str):
        """完全探索区域"""
        if area_id in self.areas:
            self.areas[area_id].explored = True
            self.save_state()
    
    def get_area_info(self, area_id: str, player_view: bool = False) -> Optional[Dict]:
        """获取区域信息"""
        if area_id not in self.areas:
            return None
        
        area = self.areas[area_id]
        
        if player_view and not area.discovered:
            # 玩家视角：未发现的区域返回阴影
            return {
                "id": area_id,
                "status": "fog_of_war",
                "name": "???",
                "description": "未探索区域"
            }
        
        result = {
            "id": area.id,
            "name": area.name,
            "name_en": area.name_en,
            "description": area.description if not player_view or area.explored else "已发现但未完全探索",
            "discovered": area.discovered,
            "explored": area.explored,
            "connected_to": area.connected_to if not player_view else [],
            "visible_features": area.visible_features if area.discovered else [],
        }
        
        if not player_view and area.notes:
            result["dm_notes"] = area.notes
        
        return result
    
    def get_player_map(self) -> str:
        """生成玩家视角的地图文本描述"""
        lines = ["# 🗺️ 红标帮窝点 - 已探索区域", ""]
        
        discovered_areas = [a for a in self.areas.values() if a.discovered]
        
        if not discovered_areas:
            lines.append("*尚未探索任何区域*")
            return "\n".join(lines)
        
        for area in discovered_areas:
            status = "✅" if area.explored else "👁️"
            lines.append(f"{status} **{area.name}** ({area.name_en})")
            lines.append(f"   {area.description[:50]}...")
            if area.visible_features:
                lines.append(f"   可见：{', '.join(area.visible_features[:3])}")
            lines.append("")
        
        # 添加连接信息
        lines.append("## 连接关系")
        for area in discovered_areas:
            connected = [self.areas[cid].name for cid in area.connected_to 
                        if cid in self.areas and self.areas[cid].discovered]
            if connected:
                lines.append(f"- {area.name} ↔ {', '.join(connected)}")
        
        return "\n".join(lines)
    
    def get_dm_map(self) -> str:
        """生成DM完整地图"""
        lines = ["# 🗺️ 红标帮窝点 - DM完整地图", ""]
        
        for area in self.areas.values():
            status = "✅ 已探索" if area.explored else ("👁️ 已发现" if area.discovered else "⬛ 未探索")
            lines.append(f"{status} **{area.name}** ({area.id})")
            lines.append(f"   {area.description}")
            lines.append(f"   连接：{', '.join(area.connected_to)}")
            if area.notes:
                lines.append(f"   📝 DM笔记：{area.notes}")
            lines.append("")
        
        return "\n".join(lines)
    
    def mark_player_location(self, area_id: str):
        """标记玩家位置"""
        if area_id in self.areas:
            self.player_location = area_id
            self.discover_area(area_id)  # 自动发现当前位置
    
    def save_state(self):
        """保存地图状态"""
        if not self.save_file:
            return
        
        data = {
            "areas": {k: asdict(v) for k, v in self.areas.items()},
            "player_location": self.player_location,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_state(self):
        """加载地图状态"""
        if not self.save_file or not self.save_file.exists():
            return
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 恢复区域状态
            for area_id, area_data in data.get("areas", {}).items():
                if area_id in self.areas:
                    self.areas[area_id].discovered = area_data.get("discovered", False)
                    self.areas[area_id].explored = area_data.get("explored", False)
                    self.areas[area_id].notes = area_data.get("notes", "")
            
            self.player_location = data.get("player_location")
        except Exception as e:
            print(f"加载地图状态失败: {e}")


# 测试
if __name__ == "__main__":
    map_mgr = RedbrandHideoutMap()
    
    # 模拟凯尔的侦查发现
    map_mgr.discover_area("area_8", "从秘密隧道进入的洞穴通道")
    map_mgr.discover_area("area_9", "发现3名红标帮成员在赌博")
    map_mgr.mark_player_location("area_8")
    
    # 查看玩家地图
    print("=== 玩家视角 ===")
    print(map_mgr.get_player_map())
    
    print("\n\n=== DM完整地图 ===")
    print(map_mgr.get_dm_map())
