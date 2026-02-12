#!/usr/bin/env python3
"""
将提取的5etools数据翻译成中文
使用标准的D&D 5e中文术语
"""

import json
from pathlib import Path

DATA_DIR = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/data")

# 法术名称翻译映射 (常用法术)
SPELL_NAMES = {
    # 戏法 Cantrips
    "Acid Splash": "酸液飞溅",
    "Blade Ward": "剑刃护壁",
    "Booming Blade": "轰鸣之刃",
    "Chill Touch": "寒冷之触",
    "Control Flames": "操控火焰",
    "Create Bonfire": "创造篝火",
    "Dancing Lights": "舞光术",
    "Druidcraft": "德鲁伊伎俩",
    "Eldritch Blast": "魔能爆",
    "Fire Bolt": "火焰箭",
    "Friends": "交友术",
    "Frostbite": "冷冻射线",
    "Green-Flame Blade": "绿焰之刃",
    "Guidance": "神导术",
    "Gust": "突风",
    "Infestation": "虫害",
    "Light": "光亮术",
    "Lightning Lure": "闪电诱引",
    "Mage Hand": "法师之手",
    "Magic Stone": "魔石术",
    "Mending": "修复术",
    "Message": "传讯术",
    "Minor Illusion": "次级幻影",
    "Mold Earth": "塑土术",
    "Poison Spray": "毒气喷射",
    "Prestidigitation": "魔法伎俩",
    "Primal Savagery": "原初蛮性",
    "Produce Flame": "燃火术",
    "Ray of Frost": "冷冻射线",
    "Resistance": "抗性术",
    "Sacred Flame": "圣焰术",
    "Shape Water": "塑水术",
    "Shillelagh": "橡棍术",
    "Shocking Grasp": "电爪",
    "Spare the Dying": "维生术",
    "Sword Burst": "剑刃爆发",
    "Thaumaturgy": "奇术",
    "Thorn Whip": "荆棘之鞭",
    "Thunderclap": "雷鸣爆",
    "Toll the Dead": "丧钟术",
    "True Strike": "克敌机先",
    "Vicious Mockery": "恶言相加",
    
    # 1环 1st Level
    "Absorb Elements": "吸收元素",
    "Alarm": "警报术",
    "Animal Friendship": "动物交友",
    "Armor of Agathys": "阿加西斯之甲",
    "Arms of Hadar": "哈达之臂",
    "Bane": "灾祸术",
    "Bless": "祝福术",
    "Burning Hands": "燃烧之手",
    "Catapult": "弹射术",
    "Cause Fear": "引起恐惧",
    "Charm Person": "魅惑人类",
    "Chromatic Orb": "彩色法球",
    "Color Spray": "七彩喷射",
    "Command": "命令术",
    "Compelled Duel": "强迫对决",
    "Comprehend Languages": "通晓语言",
    "Create or Destroy Water": "造水/枯水术",
    "Cure Wounds": "疗伤术",
    "Detect Evil and Good": "侦测善恶",
    "Detect Magic": "侦测魔法",
    "Detect Poison and Disease": "侦测毒与疾病",
    "Disguise Self": "易容术",
    "Dissonant Whispers": "不谐低语",
    "Divine Favor": "神恩术",
    "Ensnaring Strike": "诱捕打击",
    "Entangle": "纠缠术",
    "Expeditious Retreat": "脚底抹油",
    "Faerie Fire": "妖火",
    "False Life": "虚假生命",
    "Feather Fall": "羽落术",
    "Find Familiar": "寻找魔宠",
    "Fog Cloud": "云雾术",
    "Goodberry": "神莓术",
    "Grease": "油腻术",
    "Guiding Bolt": "曳光弹",
    "Hail of Thorns": "荆棘之雨",
    "Healing Word": "治愈真言",
    "Hellish Rebuke": "地狱叱喝",
    "Heroism": "英雄气概",
    "Hex": "妖术",
    "Hunter's Mark": "猎人印记",
    "Ice Knife": "冰刃术",
    "Identify": "鉴定术",
    "Illusory Script": "幻象手稿",
    "Inflict Wounds": "造成伤",
    "Jump": "跳跃术",
    "Longstrider": "大步奔行",
    "Mage Armor": "法师护甲",
    "Magic Missile": "魔法飞弹",
    "Protection from Evil and Good": "防护善恶",
    "Purify Food and Drink": "净化饮食",
    "Ray of Sickness": "致病射线",
    "Sanctuary": "圣域术",
    "Searing Smite": "灼热斩",
    "Shield": "护盾术",
    "Shield of Faith": "信仰护盾",
    "Silent Image": "无声幻影",
    "Sleep": "睡眠术",
    "Speak with Animals": "动物交谈",
    "Tasha's Hideous Laughter": "塔莎狂笑术",
    "Tenser's Floating Disk": "浮空碟",
    "Thunderous Smite": "雷鸣斩",
    "Thunderwave": "雷鸣波",
    "Unseen Servant": "隐形仆役",
    "Witch Bolt": "巫术箭",
    "Wrathful Smite": "愤怒斩",
    "Zephyr Strike": "和风打击",
    
    # 2环 2nd Level
    "Aganazzar's Scorcher": "阿迦纳萨喷火术",
    "Aid": "援助术",
    "Alter Self": "变身术",
    "Animal Messenger": "动物信使",
    "Arcane Lock": "秘法锁",
    "Augury": "卜筮术",
    "Barkskin": "树肤术",
    "Beast Sense": "野兽感知",
    "Blindness/Deafness": "目盲/耳聋术",
    "Blur": "朦胧术",
    "Branding Smite": "烙印斩",
    "Calm Emotions": "安定心神",
    "Cloud of Daggers": "匕首之云",
    "Continual Flame": "不灭明焰",
    "Cordon of Arrows": "箭矢防线",
    "Crown of Madness": "疯狂冠冕",
    "Darkness": "黑暗术",
    "Darkvision": "黑暗视觉",
    "Detect Thoughts": "侦测思想",
    "Dragon's Breath": "龙息术",
    "Dust of Disappearance": "尘遁术",
    "Earthbind": "地缚术",
    "Enhance Ability": "强化能力",
    "Enlarge/Reduce": "变巨/缩小术",
    "Enthrall": "迷魅术",
    "Find Steed": "寻找坐骑",
    "Find Traps": "寻找陷阱",
    "Flame Blade": "焰刃术",
    "Flaming Sphere": "炽焰法球",
    "Gentle Repose": "遗体防腐",
    "Gust of Wind": "造风术",
    "Healing Spirit": "治愈灵",
    "Heat Metal": "灼热金属",
    "Hold Person": "人类定身术",
    "Invisibility": "隐形术",
    "Knock": "敲击术",
    "Lesser Restoration": "次级复原术",
    "Levitate": "浮空术",
    "Locate Animals or Plants": "定位动植物",
    "Locate Object": "定位物体",
    "Magic Mouth": "魔法 mouth",
    "Magic Weapon": "魔化武器",
    "Maximilian's Earthen Grasp": "马西米利安地之握",
    "Melf's Acid Arrow": "马尔夫强酸箭",
    "Mirror Image": "镜像术",
    "Misty Step": "迷踪步",
    "Moonbeam": "月光束",
    "Nystul's Magic Aura": "尼斯特林魔法灵光",
    "Pass Without Trace": "行动无踪",
    "Phantasmal Force": "幻影之力",
    "Prayer of Healing": "群体治愈真言",
    "Protection from Poison": "防护毒素",
    "Pyrotechnics": "烟火术",
    "Ray of Enfeeblement": "衰弱射线",
    "Rope Trick": "绳索戏法",
    "Scorching Ray": "灼热射线",
    "See Invisibility": "识破隐形",
    "Shadow Blade": "影刃",
    "Shatter": "粉碎音波",
    "Silence": "沉默术",
    "Skywrite": "天书术",
    "Spider Climb": "蛛行术",
    "Spike Growth": "荆棘丛生",
    "Spiritual Weapon": "灵体武器",
    "Suggestion": "暗示术",
    "Warding Wind": "护风术",
    "Web": "蛛网术",
    "Zone of Truth": "诚实之域",
    
    # 3环 3rd Level
    "Animate Dead": "操纵死尸",
    "Aura of Vitality": "活力灵光",
    "Beacon of Hope": "希望信标",
    "Bestow Curse": "降咒",
    "Blinding Smite": "致盲斩",
    "Blink": "闪现术",
    "Call Lightning": "召雷术",
    "Catnap": "猫盹术",
    "Clairvoyance": "鹰眼/锐耳术",
    "Conjure Animals": "召唤动物",
    "Conjure Barrage": "召唤箭雨",
    "Counterspell": "法术反制",
    "Create Food and Water": "造粮/水术",
    "Crusader's Mantle": "十字军斗篷",
    "Daylight": "昼明术",
    "Dispel Magic": "解除魔法",
    "Elemental Weapon": "元素武器",
    "Enemies Abound": "敌群环绕",
    "Erupting Earth": "爆发之地",
    "Fear": "恐惧术",
    "Feign Death": "假死术",
    "Fireball": "火球术",
    "Flame Arrows": "火焰箭",
    "Fly": "飞行术",
    "Gaseous Form": "气化形体",
    "Glyph of Warding": "守护刻文",
    "Haste": "加速术",
    "Hunger of Hadar": "哈达之饥渴",
    "Hypnotic Pattern": "催眠图纹",
    "Leomund's Tiny Hut": "李欧蒙小屋",
    "Life Transference": "生命转移",
    "Lightning Arrow": "闪电箭",
    "Lightning Bolt": "闪电束",
    "Magic Circle": "魔法圈",
    "Major Image": "高等幻影",
    "Mass Healing Word": "群体治愈真言",
    "Melf's Minute Meteors": "马尔夫微流星",
    "Nondetection": "回避侦测",
    "Phantom Steed": "魅影驹",
    "Plant Growth": "植物滋长",
    "Protection from Energy": "防护能量",
    "Remove Curse": "移除诅咒",
    "Revivify": "复生术",
    "Sending": "传讯术",
    "Sleet Storm": "冰雹雨",
    "Slow": "缓慢术",
    "Speak with Dead": "死者交谈",
    "Speak with Plants": "植物交谈",
    "Spirit Guardians": "灵体卫士",
    "Stinking Cloud": "臭云术",
    "Thunder Step": "雷鸣步",
    "Tidal Wave": "潮汐波",
    "Tiny Servant": "微型仆役",
    "Tongues": "巧言术",
    "Vampiric Touch": "吸血鬼之触",
    "Water Breathing": "水下呼吸",
    "Water Walk": "水面行走",
    "Wind Wall": "风墙术",
    
    # 更多法术可以继续添加...
}

# 专长名称翻译
FEAT_NAMES = {
    "Alert": "警觉",
    "Athlete": "运动员",
    "Actor": "演员",
    "Charger": "冲锋者",
    "Crossbow Expert": "弩箭专家",
    "Defensive Duelist": "防守决斗者",
    "Dual Wielder": "双持客",
    "Dungeon Delver": "地城探索者",
    "Durable": "健壮",
    "Elemental Adept": "元素师",
    "Grappler": "擒抱者",
    "Great Weapon Master": "重武器大师",
    "Healer": "医疗者",
    "Heavily Armored": "重甲熟练",
    "Heavy Armor Master": "重甲大师",
    "Inspiring Leader": "激励领袖",
    "Keen Mind": "敏锐心灵",
    "Lightly Armored": "轻甲熟练",
    "Linguist": "语言学家",
    "Lucky": "幸运儿",
    "Mage Slayer": "法师猎手",
    "Magic Initiate": "魔法入门者",
    "Martial Adept": "战技大师",
    "Medium Armor Master": "中甲大师",
    "Mobile": "机敏",
    "Moderately Armored": "中甲熟练",
    "Mounted Combatant": "骑乘战士",
    "Observant": "观察力敏锐",
    "Polearm Master": "长柄武器大师",
    "Resilient": "顽强",
    "Ritual Caster": "仪式施法者",
    "Savage Attacker": "野蛮攻击者",
    "Sentinel": "哨兵",
    "Sharpshooter": "神射手",
    "Shield Master": "盾牌大师",
    "Skilled": "技艺精湛",
    "Skulker": "潜伏者",
    "Spell Sniper": "法术狙击手",
    "Tough": "强健",
    "War Caster": "战地施法者",
    "Weapon Master": "武器大师"
}

def translate_spells(spells):
    """翻译法术名称"""
    for spell in spells:
        name_en = spell['name_en']
        spell['name_cn'] = SPELL_NAMES.get(name_en, name_en)
    return spells

def translate_feats(feats):
    """翻译专长名称"""
    for feat in feats:
        name_en = feat['name_en']
        feat['name_cn'] = FEAT_NAMES.get(name_en, name_en)
    return feats

def generate_cn_markdown(data):
    """生成中文参考文档"""
    md = """# D&D 5e 核心规则参考文档 (中文版)

> 本文档包含 D&D 5e 核心规则的完整中文翻译，数据来源于 5etools

---

## 目录

1. [状态条件](#状态条件)
2. [战斗动作](#战斗动作)
3. [法术列表](#法术列表)
4. [专长列表](#专长列表)

---

## 状态条件

下列状态会影响生物的能力和行动方式。多个同种状态的效果不叠加。

"""
    
    conditions = data.get('conditions', [])
    for c in conditions:
        md += f"""### {c['name_cn']} ({c['name_en']})

**来源**: {c['source']} 第{c['page']}页

{c['description']}

---

"""
    
    md += """## 战斗动作

在战斗中，你可以选择以下动作之一来执行：

"""
    
    actions = data.get('actions', [])
    for a in actions:
        if a['name_en'] in ['Attack', 'Cast a Spell', 'Dash', 'Disengage', 'Dodge', 'Help', 'Hide', 'Ready', 'Search', 'Use an Object']:
            time_str = f" ({a['time']})" if a['time'] else ""
            md += f"""### {a['name_cn']} ({a['name_en']}){time_str}

{a['description']}

---

"""
    
    md += """## 法术列表

"""
    
    spells = data.get('spells', [])
    # 按等级分组
    spells_by_level = {}
    for s in spells:
        level = s['level']
        if level not in spells_by_level:
            spells_by_level[level] = []
        spells_by_level[level].append(s)
    
    for level in sorted(spells_by_level.keys()):
        level_name = "戏法 (Cantrips)" if level == 0 else f"{level} 环法术"
        md += f"### {level_name}\n\n"
        
        for s in spells_by_level[level]:
            ritual = " (仪式)" if s['ritual'] else ""
            md += f"""#### {s['name_cn']} ({s['name_en']}){ritual}

- **学派**: {s['school_cn']}
- **施法时间**: {s['cast_time']}
- **射程**: {s['range']}
- **成分**: {s['components']}
- **持续时间**: {s['duration']}

{s['description']}

"""
            if s['higher_level']:
                md += f"**升阶效果**: {s['higher_level']}\n\n"
        
        md += "---\n\n"
    
    md += """## 专长列表

"""
    
    feats = data.get('feats', [])
    for f in feats:
        prereq = f"\n**先决条件**: {f['prerequisite']}\n" if f['prerequisite'] else ""
        md += f"""### {f['name_cn']} ({f['name_en']})

**来源**: {f['source']}{prereq}

{f['description']}

---

"""
    
    return md

def main():
    print("=" * 50)
    print("翻译 5etools 数据")
    print("=" * 50)
    
    # 读取提取的数据
    with open(DATA_DIR / "5etools_extracted.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 翻译法术和专长
    data['spells'] = translate_spells(data['spells'])
    data['feats'] = translate_feats(data['feats'])
    
    # 保存翻译后的 JSON
    with open(DATA_DIR / "5etools_cn.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"法术: {len(data['spells'])} 个")
    print(f"专长: {len(data['feats'])} 个")
    print(f"状态: {len(data['conditions'])} 个")
    print(f"动作: {len(data['actions'])} 个")
    
    # 生成中文 Markdown
    md = generate_cn_markdown(data)
    with open(DATA_DIR / "5etools_cn.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"\n中文数据已保存:")
    print(f"  - {DATA_DIR / '5etools_cn.json'}")
    print(f"  - {DATA_DIR / '5etools_cn.md'}")

if __name__ == "__main__":
    main()
