#!/usr/bin/env python3
"""
D&D 5e Combat Engine
严格遵守规则的战斗计算系统
"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class DamageType(Enum):
    SLASHING = "挥砍"
    PIERCING = "穿刺"
    BLUDGEONING = "钝击"
    FIRE = "火焰"
    COLD = "冷冻"
    LIGHTNING = "闪电"
    ACID = "强酸"
    POISON = "毒素"
    NECROTIC = "死灵"
    RADIANT = "光耀"
    FORCE = "力场"
    PSYCHIC = "心灵"
    THUNDER = "雷鸣"


@dataclass
class Combatant:
    """战斗参与者"""
    name: str
    max_hp: int
    current_hp: int
    ac: int
    initiative_bonus: int
    initiative: int = 0
    is_pc: bool = False
    conditions: List[str] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []
    
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    def is_dying(self) -> bool:
        return self.current_hp == 0 and "死亡" not in self.conditions
    
    def take_damage(self, damage: int) -> str:
        """承受伤害，返回状态描述"""
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            if not self.is_dying():
                self.conditions.append("濒死")
                return f"💀 {self.name} 倒下，进入濒死状态！"
        return f"💥 {self.name} 受到 {damage} 点伤害，剩余 HP: {self.current_hp}/{self.max_hp}"
    
    def heal(self, amount: int) -> str:
        """恢复生命"""
        if "濒死" in self.conditions:
            self.conditions.remove("濒死")
        old_hp = self.current_hp
        self.current_hp = min(self.current_hp + amount, self.max_hp)
        healed = self.current_hp - old_hp
        return f"✨ {self.name} 恢复 {healed} 点 HP，当前: {self.current_hp}/{self.max_hp}"


@dataclass
class AttackResult:
    """攻击结果"""
    attack_roll: int
    attack_bonus: int
    total_attack: int
    target_ac: int
    is_hit: bool
    is_critical: bool
    is_natural_1: bool
    damage_roll: str
    damage_bonus: int
    total_damage: int
    damage_type: DamageType
    calculation_text: str


class CombatEngine:
    """战斗引擎"""
    
    def __init__(self):
        self.combatants: List[Combatant] = []
        self.round = 0
        self.turn_index = 0
        self.initiative_order: List[Combatant] = []
        self.combat_log: List[str] = []
    
    def roll_d20(self, advantage: bool = False, disadvantage: bool = False) -> Tuple[int, str]:
        """
        掷d20，支持优势和劣势
        返回 (结果, 计算描述)
        """
        roll1 = random.randint(1, 20)
        
        if advantage and disadvantage:
            # 互相抵消
            return roll1, f"d20({roll1}) [优势劣势抵消]"
        
        if advantage:
            roll2 = random.randint(1, 20)
            result = max(roll1, roll2)
            return result, f"d20({roll1}, {roll2}) 优势取高 = {result}"
        
        if disadvantage:
            roll2 = random.randint(1, 20)
            result = min(roll1, roll2)
            return result, f"d20({roll1}, {roll2}) 劣势取低 = {result}"
        
        return roll1, f"d20({roll1})"
    
    def roll_damage(self, dice_str: str) -> Tuple[int, str]:
        """
        掷伤害骰
        格式: "2d8", "1d6+3", "d10"
        """
        import re
        
        # 解析骰子表达式
        match = re.match(r'(\d*)d(\d+)(?:([+-])(\d+))?', dice_str)
        if not match:
            return 0, "解析失败"
        
        num_dice = int(match.group(1)) if match.group(1) else 1
        dice_size = int(match.group(2))
        modifier = int(match.group(4)) if match.group(4) else 0
        modifier_sign = match.group(3) if match.group(3) else "+"
        
        rolls = [random.randint(1, dice_size) for _ in range(num_dice)]
        total = sum(rolls)
        
        if modifier != 0:
            if modifier_sign == "+":
                total += modifier
            else:
                total -= modifier
        
        if num_dice == 1:
            roll_str = f"d{dice_size}({rolls[0]})"
        else:
            roll_str = f"{num_dice}d{dice_size}({' + '.join(map(str, rolls))} = {sum(rolls)})"
        
        if modifier != 0:
            calculation = f"{roll_str} {modifier_sign} {modifier} = {total}"
        else:
            calculation = f"{roll_str} = {total}"
        
        return total, calculation
    
    def make_attack(self, attacker: Combatant, target: Combatant, 
                    attack_bonus: int, damage_dice: str, damage_bonus: int,
                    damage_type: DamageType,
                    advantage: bool = False, disadvantage: bool = False,
                    cover: str = None,
                    fighting_style: str = None,
                    is_one_handed: bool = True) -> AttackResult:
        """
        执行攻击
        
        Args:
            attacker: 攻击者
            target: 目标
            attack_bonus: 攻击加值（属性调整+熟练）
            damage_dice: 伤害骰（如"1d8", "2d6"）
            damage_bonus: 伤害加值（属性调整）
            damage_type: 伤害类型
            advantage: 优势
            disadvantage: 劣势
            cover: 掩护类型（"半", "四分之三", "全"）
            fighting_style: 战斗风格（"对决", "双武器", "箭术", "防御", "守护", "重武器"）
            is_one_handed: 是否单手武器（用于对决风格判断）
        """
        # 计算目标AC（考虑掩护）
        target_ac = target.ac
        cover_bonus = 0
        if cover == "半":
            cover_bonus = 2
            target_ac += 2
        elif cover == "四分之三":
            cover_bonus = 5
            target_ac += 5
        elif cover == "全":
            # 完全掩护无法攻击
            return AttackResult(
                0, 0, 0, target_ac, False, False, False,
                "", 0, 0, damage_type,
                "❌ 目标处于完全掩护下，无法攻击！"
            )
        
        # 掷攻击骰
        attack_roll, roll_text = self.roll_d20(advantage, disadvantage)
        
        # 检查自然20（暴击）和自然1（大失败）
        is_critical = attack_roll == 20
        is_natural_1 = attack_roll == 1
        
        # 计算总攻击值
        total_attack = attack_roll + attack_bonus
        
        # 判断命中
        if is_natural_1:
            is_hit = False
        elif is_critical:
            is_hit = True
        else:
            is_hit = total_attack >= target_ac
        
        # 计算伤害
        fighting_style_bonus = 0
        fighting_style_text = ""
        
        # 应用战斗风格加成
        if fighting_style == "对决" and is_one_handed:
            fighting_style_bonus = 2
            fighting_style_text = "+2[对决风格]"
        elif fighting_style == "箭术":
            # 箭术是攻击加值，不是伤害加值
            pass
        
        if is_hit:
            if is_critical:
                # 暴击：伤害骰翻倍
                base_dice = damage_dice
                # 简单处理：如果是"1d8"变成"2d8"
                if damage_dice.startswith("1d"):
                    crit_dice = "2" + damage_dice[1:]
                else:
                    # 复杂情况：解析并翻倍
                    import re
                    match = re.match(r'(\d+)d(\d+)', damage_dice)
                    if match:
                        num = int(match.group(1)) * 2
                        size = match.group(2)
                        crit_dice = f"{num}d{size}"
                    else:
                        crit_dice = damage_dice
                
                damage_total, damage_calc = self.roll_damage(crit_dice)
                damage_total += damage_bonus + fighting_style_bonus
            else:
                damage_total, damage_calc = self.roll_damage(damage_dice)
                damage_total += damage_bonus + fighting_style_bonus
            
            # 应用伤害
            status = target.take_damage(damage_total)
        else:
            damage_total = 0
            damage_calc = "未命中"
            status = ""
        
        # 生成计算文本
        calc_lines = [
            f"【攻击检定】",
            f"{roll_text}",
        ]
        
        if attack_bonus != 0:
            calc_lines.append(f"+ {attack_bonus}[攻击加值]")
        
        if cover_bonus > 0:
            calc_lines.append(f"vs AC {target.ac} + {cover_bonus}[掩护] = {target_ac}")
        else:
            calc_lines.append(f"= {total_attack} vs AC {target_ac}")
        
        if is_natural_1:
            calc_lines.append(f"❌ 自然1！攻击大失败！")
        elif is_critical:
            calc_lines.append(f"💥 自然20！暴击！")
            calc_lines.append(f"")
            calc_lines.append(f"【伤害】")
            calc_lines.append(f"暴击翻倍: {damage_calc}")
            if damage_bonus != 0:
                calc_lines.append(f"+ {damage_bonus}[伤害加值]")
            if fighting_style_bonus > 0:
                calc_lines.append(f"+ {fighting_style_bonus}[{fighting_style}风格]")
            calc_lines.append(f"= {damage_total} {damage_type.value}伤害")
            if status:
                calc_lines.append(f"")
                calc_lines.append(status)
        elif is_hit:
            calc_lines.append(f"✅ 命中！")
            calc_lines.append(f"")
            calc_lines.append(f"【伤害】")
            calc_lines.append(f"{damage_calc}")
            if damage_bonus != 0:
                calc_lines.append(f"+ {damage_bonus}[伤害加值]")
            if fighting_style_bonus > 0:
                calc_lines.append(f"+ {fighting_style_bonus}[{fighting_style}风格]")
            calc_lines.append(f"= {damage_total} {damage_type.value}伤害")
            if status:
                calc_lines.append(f"")
                calc_lines.append(status)
        else:
            calc_lines.append(f"❌ 未命中")
        
        calculation_text = "\n".join(calc_lines)
        
        return AttackResult(
            attack_roll, attack_bonus, total_attack, target_ac,
            is_hit, is_critical, is_natural_1,
            damage_dice, damage_bonus, damage_total, damage_type,
            calculation_text
        )
    
    def roll_initiative(self, combatants: List[Combatant]) -> List[Combatant]:
        """掷先攻并排序"""
        for c in combatants:
            roll, _ = self.roll_d20()
            c.initiative = roll + c.initiative_bonus
        
        # 按先攻排序（高到低）
        sorted_combatants = sorted(combatants, key=lambda x: x.initiative, reverse=True)
        self.initiative_order = sorted_combatants
        self.combatants = combatants
        return sorted_combatants
    
    def start_combat(self, combatants: List[Combatant]) -> str:
        """开始战斗"""
        self.round = 1
        self.turn_index = 0
        
        # 掷先攻
        initiative_order = self.roll_initiative(combatants)
        
        lines = [
            "⚔️ 【战斗开始！】",
            "",
            "【先攻顺序】",
        ]
        
        for i, c in enumerate(initiative_order, 1):
            icon = "🧙" if c.is_pc else "👹"
            lines.append(f"{i}. {icon} {c.name} (先攻 {c.initiative})")
        
        lines.append("")
        lines.append(f"【第 {self.round} 轮】")
        lines.append("")
        
        return "\n".join(lines)
    
    def get_current_turn(self) -> Optional[Combatant]:
        """获取当前回合的角色"""
        if not self.initiative_order:
            return None
        return self.initiative_order[self.turn_index]
    
    def next_turn(self) -> str:
        """进入下一回合"""
        self.turn_index += 1
        
        if self.turn_index >= len(self.initiative_order):
            # 新一轮
            self.round += 1
            self.turn_index = 0
            return f"\n【第 {self.round} 轮】\n"
        
        return ""
    
    def format_combat_status(self) -> str:
        """格式化战斗状态"""
        lines = ["【战场状态】", ""]
        
        for c in self.initiative_order:
            icon = "🧙" if c.is_pc else "👹"
            hp_bar = f"{c.current_hp}/{c.max_hp}"
            
            if c.current_hp <= 0:
                status = "💀 倒地"
            elif c.current_hp <= c.max_hp * 0.25:
                status = "🩸 重伤"
            elif c.current_hp <= c.max_hp * 0.5:
                status = "⚠️ 受伤"
            else:
                status = "✅ 良好"
            
            condition_str = f" [{', '.join(c.conditions)}]" if c.conditions else ""
            
            lines.append(f"{icon} {c.name}: HP {hp_bar} {status}{condition_str}")
        
        return "\n".join(lines)


def saving_throw(dc: int, ability_bonus: int, advantage: bool = False, 
                 disadvantage: bool = False) -> Tuple[bool, str]:
    """
    豁免检定
    
    Args:
        dc: 难度等级
        ability_bonus: 属性加值
        
    Returns:
        (是否成功, 计算描述)
    """
    engine = CombatEngine()
    roll, roll_text = engine.roll_d20(advantage, disadvantage)
    total = roll + ability_bonus
    
    calc = f"豁免检定: {roll_text}"
    if ability_bonus != 0:
        calc += f" + {ability_bonus}[属性]"
    calc += f" = {total} vs DC {dc}"
    
    if roll == 20:
        success = True
        calc += " ✅ 自然20！自动成功！"
    elif roll == 1:
        success = False
        calc += " ❌ 自然1！自动失败！"
    else:
        success = total >= dc
        calc += " ✅ 成功" if success else " ❌ 失败"
    
    return success, calc


def death_saving_throw() -> Tuple[str, int, int]:
    """
    死亡豁免
    
    Returns:
        (结果描述, 成功次数, 失败次数)
    """
    roll = random.randint(1, 20)
    
    if roll == 20:
        return "🎉 自然20！立即恢复1 HP，苏醒！", 3, 0  # 立即成功
    elif roll == 1:
        return "💀 自然1！2次失败！", 0, 2
    elif roll >= 10:
        return f"✅ {roll} - 成功！", 1, 0
    else:
        return f"❌ {roll} - 失败！", 0, 1


def use_second_wind(character_level: int) -> Tuple[int, str]:
    """
    使用回气 (Second Wind)
    
    Args:
        character_level: 角色等级
        
    Returns:
        (恢复的生命值, 计算描述)
    """
    import random
    roll = random.randint(1, 10)
    total = roll + character_level
    
    calc = f"回气: d10({roll}) + {character_level}[等级] = {total} HP"
    
    return total, calc


def trigger_relentless_endurance() -> str:
    """
    触发半兽人种族特性：不屈
    
    Returns:
        描述文本
    """
    return "🔥 不屈触发！HP降至0时改为1，继续战斗！（1次/长休已使用）"


def apply_savage_attacks(base_damage_dice: str) -> str:
    """
    应用半兽人种族特性：凶恶攻击（暴击时额外骰）
    
    Args:
        base_damage_dice: 基础伤害骰，如 "1d12"
        
    Returns:
        额外伤害骰，如 "1d12"
    """
    # 凶恶攻击：额外追加一个伤害骰
    return base_damage_dice


# ============ 便捷函数（供MCP工具调用） ============

def calculate_attack_roll(attacker_bonus: int, target_ac: int, damage_dice: str,
                         advantage: bool = False, disadvantage: bool = False) -> dict:
    """
    计算攻击检定（独立函数，供MCP工具调用）
    
    Args:
        attacker_bonus: 攻击加值（属性调整值+熟练加值）
        target_ac: 目标AC
        damage_dice: 伤害骰表达式（如"1d8+3"、"2d6"）
        advantage: 是否有优势
        disadvantage: 是否有劣势
        
    Returns:
        包含攻击结果的字典
    """
    import random
    import re
    
    engine = CombatEngine()
    
    # 掷攻击骰
    attack_roll, roll_text = engine.roll_d20(advantage, disadvantage)
    
    # 检查自然20和自然1
    is_critical = attack_roll == 20
    is_natural_1 = attack_roll == 1
    
    # 计算总攻击值
    total_attack = attack_roll + attacker_bonus
    
    # 判断命中
    if is_natural_1:
        is_hit = False
    elif is_critical:
        is_hit = True
    else:
        is_hit = total_attack >= target_ac
    
    # 计算伤害
    damage_result = 0
    damage_calc = "未命中"
    
    if is_hit:
        if is_critical:
            # 暴击：伤害骰翻倍
            match = re.match(r'(\d+)d(\d+)(?:([+-])(\d+))?', damage_dice)
            if match:
                num_dice = int(match.group(1))
                dice_size = int(match.group(2))
                modifier = int(match.group(4)) if match.group(4) else 0
                modifier_sign = match.group(3) if match.group(3) else "+"
                
                # 翻倍骰子数量
                crit_rolls = [random.randint(1, dice_size) for _ in range(num_dice * 2)]
                damage_result = sum(crit_rolls)
                if modifier != 0:
                    if modifier_sign == "+":
                        damage_result += modifier
                    else:
                        damage_result -= modifier
                
                damage_calc = f"暴击翻倍: {num_dice * 2}d{dice_size}({crit_rolls})"
                if modifier != 0:
                    damage_calc += f" {modifier_sign} {modifier}"
                damage_calc += f" = {damage_result}"
            else:
                damage_result, damage_calc = engine.roll_damage(damage_dice)
        else:
            damage_result, damage_calc = engine.roll_damage(damage_dice)
    
    # 构建结果
    result = {
        "attack_roll": attack_roll,
        "attack_bonus": attacker_bonus,
        "total_attack": total_attack,
        "target_ac": target_ac,
        "is_hit": is_hit,
        "is_critical": is_critical,
        "is_natural_1": is_natural_1,
        "damage": damage_result,
        "calculation": ""
    }
    
    # 生成计算文本
    calc_lines = [
        f"【攻击检定】",
        f"{roll_text}",
    ]
    
    if attacker_bonus != 0:
        calc_lines.append(f"+ {attacker_bonus}[攻击加值]")
    
    calc_lines.append(f"= {total_attack} vs AC {target_ac}")
    
    if is_natural_1:
        calc_lines.append(f"❌ 自然1！攻击大失败！")
    elif is_critical:
        calc_lines.append(f"💥 自然20！暴击！")
        calc_lines.append(f"")
        calc_lines.append(f"【伤害】")
        calc_lines.append(f"{damage_calc}")
    elif is_hit:
        calc_lines.append(f"✅ 命中！")
        calc_lines.append(f"")
        calc_lines.append(f"【伤害】")
        calc_lines.append(f"{damage_calc}")
    else:
        calc_lines.append(f"❌ 未命中（差{target_ac - total_attack}点）")
    
    result["calculation"] = "\n".join(calc_lines)
    
    return result


if __name__ == "__main__":
    # 测试战斗引擎
    print("🎲 D&D 5e 战斗引擎测试")
    print("=" * 50)
    
    # 创建测试角色 - 萨尔坦（1级战士）
    pc = Combatant("萨尔坦", 12, 12, 16, 1, is_pc=True)
    enemy = Combatant("地精", 7, 7, 15, 2)
    
    # 开始战斗
    engine = CombatEngine()
    print(engine.start_combat([pc, enemy]))
    
    # 测试攻击（带对决风格）
    print("\n【攻击测试 - 对决风格】")
    result = engine.make_attack(
        pc, enemy,
        attack_bonus=5,  # +3力量 +2熟练
        damage_dice="1d12",  # 巨斧
        damage_bonus=3,  # +3力量
        damage_type=DamageType.SLASHING,
        fighting_style="对决",
        is_one_handed=True
    )
    print(result.calculation_text)
    
    # 测试独立攻击计算函数
    print("\n【独立攻击计算函数测试】")
    attack_result = calculate_attack_roll(
        attacker_bonus=5,
        target_ac=15,
        damage_dice="1d8+3",
        advantage=True
    )
    print(attack_result["calculation"])
    
    # 测试回气
    print("\n【回气测试】")
    heal_amount, heal_calc = use_second_wind(1)
    print(heal_calc)
    print(pc.heal(heal_amount))
    
    print("\n" + engine.format_combat_status())
