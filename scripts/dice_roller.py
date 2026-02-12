#!/usr/bin/env python3
"""
D&D Dice Roller
骰子模拟器
"""

import random
import re
from typing import Tuple, List


def roll_dice(dice_notation: str) -> Tuple[int, str]:
    """
    掷骰子
    
    支持的格式：
    - d20, d12, d10, d8, d6, d4
    - 2d6, 3d8, etc.
    - d20+5, 2d6+3, etc.
    - d20-2, etc.
    
    Returns:
        (结果, 计算描述)
    """
    # 解析骰子表达式
    pattern = r'(\d*)d(\d+)(?:([+-])(\d+))?'
    match = re.match(pattern, dice_notation.lower())
    
    if not match:
        return 0, f"❌ 无效的骰子表达式: {dice_notation}"
    
    num_dice = int(match.group(1)) if match.group(1) else 1
    dice_size = int(match.group(2))
    modifier = int(match.group(4)) if match.group(4) else 0
    modifier_sign = match.group(3) if match.group(3) else "+"
    
    # 掷骰子
    rolls = [random.randint(1, dice_size) for _ in range(num_dice)]
    total = sum(rolls)
    
    # 应用调整值
    if modifier != 0:
        if modifier_sign == "+":
            total += modifier
        else:
            total -= modifier
    
    # 生成描述
    if num_dice == 1:
        roll_str = f"d{dice_size}({rolls[0]})"
    else:
        rolls_str = " + ".join(map(str, rolls))
        roll_str = f"{num_dice}d{dice_size}({rolls_str} = {sum(rolls)})"
    
    if modifier != 0:
        calc = f"🎲 {roll_str} {modifier_sign} {modifier} = **{total}**"
    else:
        calc = f"🎲 {roll_str} = **{total}**"
    
    return total, calc


def roll_with_advantage() -> Tuple[int, str]:
    """优势掷骰（取高）"""
    roll1 = random.randint(1, 20)
    roll2 = random.randint(1, 20)
    result = max(roll1, roll2)
    
    return result, f"🎲 优势: d20({roll1}, {roll2}) 取高 = **{result}**"


def roll_with_disadvantage() -> Tuple[int, str]:
    """劣势掷骰（取低）"""
    roll1 = random.randint(1, 20)
    roll2 = random.randint(1, 20)
    result = min(roll1, roll2)
    
    return result, f"🎲 劣势: d20({roll1}, {roll2}) 取低 = **{result}**"


def roll_stats() -> Tuple[List[int], str]:
    """
    掷六维属性（4d6去掉最低）
    
    Returns:
        (6个属性值列表, 计算描述)
    """
    stats = []
    description_lines = ["【属性掷骰 - 4d6去掉最低】", ""]
    
    ability_names = ["力量", "敏捷", "体质", "智力", "感知", "魅力"]
    
    for ability in ability_names:
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        dropped = rolls[0]
        kept = rolls[1:]
        total = sum(kept)
        stats.append(total)
        
        description_lines.append(
            f"{ability}: 4d6({rolls}) 去掉{dropped} = {kept} = **{total}**"
        )
    
    return stats, "\n".join(description_lines)


def roll_hit_dice(hit_dice: str, con_modifier: int) -> Tuple[int, str]:
    """
    掷生命骰恢复HP
    
    Args:
        hit_dice: 生命骰，如"1d12", "1d8"
        con_modifier: 体质调整值
    
    Returns:
        (恢复的HP, 计算描述)
    """
    hp, calc = roll_dice(hit_dice)
    
    if con_modifier > 0:
        total = hp + con_modifier
        calc += f" + {con_modifier}[体质] = **{total}** HP恢复"
    else:
        total = max(1, hp + con_modifier)  # 最少恢复1 HP
        if con_modifier < 0:
            calc += f" {con_modifier}[体质] = **{total}** HP恢复"
        else:
            calc = calc.replace(f"= **{hp}**", f"= **{total}** HP恢复")
    
    return total, calc


def format_dice_result(expression: str, result: int, calculation: str) -> str:
    """格式化骰子结果输出"""
    return f"{calculation}"


# 快捷函数
def d20(modifier: int = 0) -> Tuple[int, str]:
    """快捷掷d20"""
    if modifier == 0:
        return roll_dice("d20")
    else:
        return roll_dice(f"d20{'+' if modifier > 0 else ''}{modifier}")


def d6(modifier: int = 0) -> Tuple[int, str]:
    """快捷掷d6"""
    if modifier == 0:
        return roll_dice("d6")
    else:
        return roll_dice(f"d6{'+' if modifier > 0 else ''}{modifier}")


def d8(modifier: int = 0) -> Tuple[int, str]:
    """快捷掷d8"""
    if modifier == 0:
        return roll_dice("d8")
    else:
        return roll_dice(f"d8{'+' if modifier > 0 else ''}{modifier}")


# ============ MCP工具入口函数 ============

def roll(dice_expression: str, advantage: bool = False, disadvantage: bool = False) -> dict:
    """
    通用的骰子掷骰函数（供MCP工具调用）
    
    Args:
        dice_expression: 骰子表达式（如"d20+5"、"2d6+3"）
        advantage: 是否有优势（仅对d20有效）
        disadvantage: 是否有劣势（仅对d20有效）
        
    Returns:
        包含结果和计算描述的字典
    """
    # 检查是否是d20且有优势/劣势
    is_d20 = dice_expression.lower().startswith("d20") or "+d20" in dice_expression.lower() or "d20+" in dice_expression.lower()
    
    if is_d20 and (advantage or disadvantage):
        if advantage and disadvantage:
            # 互相抵消
            roll1 = random.randint(1, 20)
            result = roll1
            calc = f"🎲 d20({roll1}) [优势劣势抵消]"
        elif advantage:
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            result = max(roll1, roll2)
            calc = f"🎲 优势: d20({roll1}, {roll2}) 取高 = **{result}**"
        else:  # disadvantage
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            result = min(roll1, roll2)
            calc = f"🎲 劣势: d20({roll1}, {roll2}) 取低 = **{result}**"
        
        # 如果有调整值，需要加上
        modifier_match = re.search(r'([+-]\d+)$', dice_expression)
        if modifier_match:
            modifier = int(modifier_match.group(1))
            final_result = result + modifier
            calc += f" {modifier:+d} = **{final_result}**"
            result = final_result
        
        return {
            "result": result,
            "calculation": calc,
            "dice_expression": dice_expression
        }
    else:
        # 普通掷骰
        result, calc = roll_dice(dice_expression)
        return {
            "result": result,
            "calculation": calc,
            "dice_expression": dice_expression
        }


if __name__ == "__main__":
    print("🎲 D&D 骰子模拟器测试")
    print("=" * 50)
    
    # 测试各种骰子
    print("\n【基础骰子】")
    for dice in ["d20", "d12", "d10", "d8", "d6", "d4"]:
        result, calc = roll_dice(dice)
        print(calc)
    
    print("\n【多骰子】")
    for dice in ["2d6", "3d8", "4d4"]:
        result, calc = roll_dice(dice)
        print(calc)
    
    print("\n【带调整值】")
    for dice in ["d20+5", "2d6+3", "d8-1"]:
        result, calc = roll_dice(dice)
        print(calc)
    
    print("\n【优势/劣势】")
    result, calc = roll_with_advantage()
    print(calc)
    result, calc = roll_with_disadvantage()
    print(calc)
    
    print("\n【属性掷骰】")
    stats, calc = roll_stats()
    print(calc)
    print(f"\n总属性值: {sum(stats)}, 平均值: {sum(stats)/6:.1f}")
    
    print("\n【MCP工具函数测试】")
    result = roll("d20+5", advantage=True)
    print(f"表达式: {result['dice_expression']}")
    print(f"结果: {result['result']}")
    print(f"计算: {result['calculation']}")
