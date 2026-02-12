#!/usr/bin/env python3
"""
将LMOP模组按章节拆分
"""

import re
from pathlib import Path

def split_module():
    """拆分模组为章节文件"""
    
    module_file = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/references/modules/Lost Mine of Phandelver_Chn.md")
    output_dir = Path("/Users/sid/.openclaw/workspace/skills/dnd-game-master/data/lmop_chapters")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 章节标记
    chapter_markers = {
        "part1_ambush": ("# 地精箭矢", "## 克拉摩窝点"),
        "part1_hideout": ("## 克拉摩窝点", "# 凡达林"),
        
        "part2_town": ("# 凡达林", "## 红标帮据点"),
        "part2_redbrand": ("## 红标帮据点", "# 蜘蛛网"),
        
        "part3_overview": ("# 蜘蛛网", "## 老 Owl Well"),
        "part3_old_owl_well": ("## 老 Owl Well", "## 桑德树废墟"),
        "part3_thundertree": ("## 桑德树废墟", "## 飞龙突岩"),
        "part3_wyvern_tor": ("## 飞龙突岩", "## 克拉摩堡"),
        "part3_castle": ("## 克拉摩堡", "# 回声洞"),
        
        "part4_wave_echo": ("# 回声洞", None)
    }
    
    for file_name, (start_marker, end_marker) in chapter_markers.items():
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print(f"警告：未找到 {start_marker}")
            continue
        
        if end_marker:
            end_idx = content.find(end_marker, start_idx + len(start_marker))
            if end_idx == -1:
                end_idx = len(content)
        else:
            end_idx = len(content)
        
        section_content = content[start_idx:end_idx]
        
        output_file = output_dir / f"{file_name}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(section_content)
        
        print(f"✓ 已创建：{file_name}.md ({len(section_content)} 字符)")
    
    print(f"\n完成！章节文件保存在：{output_dir}")

if __name__ == "__main__":
    split_module()
