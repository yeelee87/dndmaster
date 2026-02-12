#!/usr/bin/env python3
"""
模组分离工具 v2
更精确地将LMOP模组分离为玩家版和DM版

标记规则：
- 【玩家朗读文本】>>...<< 格式，玩家听到的描述
- 【DM操作指南】如何运行遭遇、检定DC、战术指导
- 【DM专属信息】怪物位置、陷阱、秘密、扮演提示
"""

import re

def separate_module_v2(input_file, output_player, output_dm):
    """分离模组内容为玩家版和DM版"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    player_sections = []
    dm_sections = []
    
    current_player_block = []
    current_dm_block = []
    
    in_player_box = False
    in_dm_only_section = False
    
    # DM专属内容关键词（更精确）
    dm_only_patterns = [
        r'^如果你正在使用',  # 条件说明
        r'^任何.*检定的角色',  # 检定DC
        r'^成功通过DC',  # DC信息
        r'^如果角色.*会发现',  # 隐藏发现
        r'^如果陷阱未被发现',  # 陷阱机制
        r'^在极不可能的情况下',  # 失败情况
        r'^角色们可能找不到',  # 备选方案
        r'查阅附录',  # 数据卡引用
        r'^四只\*\*.*躲在',  # 怪物隐藏位置
        r'当.*被击败时',  # 战斗发展
        r'如果.*被俘虏',  # 俘虏规则
        r'如果.*击败',  # 失败情况
        r'几天后.*信使',  # 背景信息（玩家不应直接知道）
        r'盘踞在此的',  # 背景设定
        r'奉.*之命',  # 幕后命令
        r'几天前.*来自',  # 时间线背景
    ]
    
    # 朗读文本（玩家可见）
    player_box_patterns = [
        r'^>>',  # 框开始/结束
        r'^在无冬城中',  # 冒险引子
        r'^你们已经在',  # 场景描述
        r'^鞍囊已被',  # 发现
        r'^夕阳的余晖',  # 环境
        r'^你们站在',  # 位置
        r'^你们听到',  # 声音
        r'^空气中弥漫着',  # 氛围
    ]
    
    for i, line in enumerate(lines):
        original_line = line
        stripped = line.strip()
        
        # 检测 >> 框内文本
        if stripped.startswith('>>'):
            if stripped == '>>':
                in_player_box = not in_player_box
                current_player_block.append(original_line)
                current_dm_block.append(original_line)
                continue
            else:
                # 单行框内文本
                current_player_block.append(original_line)
                current_dm_block.append(original_line)
                continue
        
        if in_player_box:
            current_player_block.append(original_line)
            current_dm_block.append(original_line)
            continue
        
        # 空行 - 保留在两个版本中
        if not stripped:
            current_player_block.append(original_line)
            current_dm_block.append(original_line)
            continue
        
        # 标题 - 保留在两个版本中作为导航
        if stripped.startswith('#'):
            current_player_block.append(original_line)
            current_dm_block.append(original_line)
            continue
        
        # 检测是否为DM专属内容
        is_dm_only = False
        for pattern in dm_only_patterns:
            if re.search(pattern, stripped):
                is_dm_only = True
                break
        
        # 侧边栏（> 开头）- 通常是DM参考
        if stripped.startswith('> ') or stripped.startswith('>'):
            is_dm_only = True
        
        # 怪物数据卡格式
        if re.search(r'AC\s*\d+.*HP\s*\d+', stripped):
            is_dm_only = True
        
        # 扮演提示（DM专属）
        if '扮演' in stripped and ('DM' in stripped or '地下城主' in stripped or '如何' in stripped):
            is_dm_only = True
        
        # 战术/发展/宝藏/经验值 部分标题
        if stripped in ['**发展**', '**宝藏**', '**奖励经验值**', '**战术**', '**扮演**']:
            is_dm_only = True
        
        # 通用特征中的环境机制（DM需要知道）
        if stripped.startswith('***') and any(x in stripped for x in ['天花板', '光线', '瓦砾', '声音', '石笋', '溪流']):
            # 这些环境描述可以部分给玩家，但机制说明是DM的
            pass
        
        if is_dm_only:
            # DM专属 - 只加入DM版
            current_dm_block.append(original_line)
            # 玩家版加入占位符或省略
        else:
            # 共享内容
            current_player_block.append(original_line)
            current_dm_block.append(original_line)
    
    # 写入文件
    with open(output_player, 'w', encoding='utf-8') as f:
        f.write('# 凡戴尔的失落矿坑 - 玩家可见内容\n\n')
        f.write('> **使用说明**：此版本包含玩家可以直接看到和听到的内容。\n')
        f.write('> DM应将此版本中的朗读文本（>>...<<框内）朗读给玩家。\n\n')
        f.write('---\n\n')
        f.write('\n'.join(current_player_block))
    
    with open(output_dm, 'w', encoding='utf-8') as f:
        f.write('# 凡戴尔的失落矿坑 - DM完整操作手册\n\n')
        f.write('> **使用说明**：此版本包含完整的DM操作指南、检定DC、怪物数据、\n')
        f.write('> 隐藏信息、战术提示等DM专属内容。\n\n')
        f.write('---\n\n')
        f.write('\n'.join(current_dm_block))
    
    print(f"✅ 已生成玩家版: {output_player}")
    print(f"   行数: {len(current_player_block)}")
    print(f"✅ 已生成DM版: {output_dm}")
    print(f"   行数: {len(current_dm_block)}")

if __name__ == '__main__':
    input_file = '/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/Lost Mine of Phandelver_Chn.md'
    output_player = '/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/lost-mine-player.md'
    output_dm = '/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/lost-mine-dm.md'
    
    separate_module_v2(input_file, output_player, output_dm)
