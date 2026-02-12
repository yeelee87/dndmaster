#!/usr/bin/env python3
"""
模组分离工具
将LMOP模组分离为：
- 玩家版 (player)：只包含朗读文本和玩家可见信息
- DM版 (dm)：包含完整的DM操作指南、怪物数据、隐藏信息

使用标记系统：
- [PLAYER] 玩家可见内容
- [DM] DM专属内容
- [SHARED] 双方都需要的内容
"""

import re
import json

def separate_module(input_file, output_player, output_dm):
    """分离模组内容为玩家版和DM版"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    player_lines = []
    dm_lines = []
    
    in_player_box = False  # >>...<< 框内文本
    in_dm_sidebar = False  # > 开头的侧边栏
    in_code_block = False
    
    for line in lines:
        original_line = line
        
        # 检测代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            dm_lines.append(original_line)
            continue
        
        if in_code_block:
            dm_lines.append(original_line)
            continue
        
        # 检测 >> 框内文本（玩家朗读文本）
        if line.strip().startswith('>>') and line.strip().endswith('>>') and len(line.strip()) > 4:
            # 单行框内文本
            player_lines.append(original_line)
            dm_lines.append(original_line)
            continue
        
        if line.strip() == '>>':
            in_player_box = not in_player_box
            player_lines.append(original_line)
            dm_lines.append(original_line)
            continue
        
        if in_player_box:
            # 框内文本 - 玩家可见
            player_lines.append(original_line)
            dm_lines.append(original_line)
            continue
        
        # 检测 > 开头的侧边栏（DM参考）
        if line.strip().startswith('> ') or line.strip().startswith('>#'):
            # DM专属侧边栏
            dm_lines.append(original_line)
            continue
        
        # 检测DM专属关键词
        dm_keywords = [
            '如果你正在使用',
            'DM可以',
            '地下城主',
            '检定以确定',
            '如果角色们',
            '如果玩家',
            '发展',
            '宝藏',
            '奖励经验值',
            '扮演',
            '战术',
            '如果受到威胁',
            '如果生命值降至',
            '秘密',
            '幕后',
            '角色不知道',
            'DM专属',
            '暗门',
            '隐藏',
            '陷阱',
            '数据卡',
        ]
        
        is_dm_content = False
        lower_line = line.lower()
        
        for keyword in dm_keywords:
            if keyword in line or keyword in lower_line:
                is_dm_content = True
                break
        
        # 检测怪物属性（DM专属）
        if re.match(r'^\*\*\w+\*\*\s*\.?\s*AC\s*\d+', line):
            is_dm_content = True
        
        if is_dm_content:
            dm_lines.append(original_line)
        else:
            # 场景描述等共享内容
            player_lines.append(original_line)
            dm_lines.append(original_line)
    
    # 写入玩家版
    with open(output_player, 'w', encoding='utf-8') as f:
        f.write('# 凡戴尔的失落矿坑 - 玩家版\n\n')
        f.write('> **注意**：此版本只包含玩家可直接获得的信息\n\n')
        f.write('\n'.join(player_lines))
    
    # 写入DM版
    with open(output_dm, 'w', encoding='utf-8') as f:
        f.write('# 凡戴尔的失落矿坑 - DM完整版\n\n')
        f.write('> **注意**：此版本包含完整的DM操作指南、怪物数据、隐藏信息\n\n')
        f.write('\n'.join(dm_lines))
    
    print(f"✅ 已生成玩家版: {output_player}")
    print(f"✅ 已生成DM版: {output_dm}")
    print(f"📊 玩家版行数: {len(player_lines)}")
    print(f"📊 DM版行数: {len(dm_lines)}")

if __name__ == '__main__':
    input_file = '/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/Lost Mine of Phandelver_Chn.md'
    output_player = '/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/lost-mine-player.md'
    output_dm = '/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/lost-mine-dm.md'
    
    separate_module(input_file, output_player, output_dm)
