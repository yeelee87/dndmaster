# D&D 5e Game Master Skill 🎲

<p align="center">
  <b>A professional D&D 5e Game Master assistant for OpenClaw</b><br>
  <b>OpenClaw 平台的专业 D&D 5e 游戏主持人助手</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/D%26D-5e%202014-blue?style=flat-square" alt="D&D 5e 2014">
  <img src="https://img.shields.io/badge/Module-LMOP-green?style=flat-square" alt="LMOP">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/Platform-OpenClaw-orange?style=flat-square" alt="OpenClaw">
</p>

---

## 🌟 Features | 功能特性

| English | 中文 |
|---------|------|
| **Strict Rule Compliance** - Follows PHB/MM/DMG 2014 exactly | **严格遵守规则** - 严格遵循 PHB/MM/DMG 2014 版规则 |
| **Official Module Support** - Full Lost Mine of Phandelver (LMOP) text | **官方模组支持** - 完整的《凡戴尔的失落矿坑》(LMOP) 模组原文 |
| **Auto Identity Switching** - Seamlessly switches between DM/Monster/NPC/PC | **自动身份切换** - 在 DM/怪物/NPC/PC 间无缝切换 |
| **Transparent Combat** - Shows every dice roll and calculation | **透明战斗计算** - 展示每一次掷骰和计算公式 |
| **Character Parser** - Supports JSON and Excel character sheets | **人物卡解析** - 支持 JSON 和 Excel 格式的人物卡 |
| **Data Query** - Monster and spell lookup via 5etools | **数据查询** - 通过 5etools 查询怪物和法术数据 |
| **Anti-Spoiler** - Information tier management system | **防剧透系统** - 信息层级管理系统 |

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
cd ~/.openclaw/skills
git clone https://github.com/yeelee87/dndmaster.git dnd-game-master
```

Or download the [latest release](https://github.com/yeelee87/dndmaster/releases) and extract.

或下载 [最新版本](https://github.com/yeelee87/dndmaster/releases) 并解压。

### Usage | 使用

Activate the skill in OpenClaw:

在 OpenClaw 中激活 Skill：

```
/use dnd-game-master
```

Start a game | 开始游戏：

```
Start Lost Mine of Phandelver
开始凡戴尔的失落矿坑

Load my character: pc_profiles/mychar.json
加载我的角色: pc_profiles/mychar.json

Begin combat
开始战斗
```

---

## 📁 File Structure | 文件结构

```
dnd-game-master/
├── 📄 SKILL.md                    # Main configuration | 主配置
├── 📚 references/                 # Reference documents | 参考文档
│   ├── core-rules/               # PHB, MM, DMG | 玩家手册、怪物手册、DM指南
│   └── modules/                  # Official modules | 官方模组
│       └── lost-mine-dm.md       # LMOP full text | LMOP 完整原文
├── 🎲 data/                      # Game data | 游戏数据
│   ├── 5etools/                  # 5e SRD data | 5e SRD 数据
│   ├── npc_profiles/             # NPC database | NPC 档案库
│   └── pc_profiles/              # PC templates | PC 角色卡模板
├── 🔧 scripts/                   # Python tools | Python 工具
│   ├── combat_engine.py          # Combat calculator | 战斗计算器
│   ├── character_parser.py       # Character reader | 人物卡解析器
│   └── dnd_data_manager.py       # Data query | 数据查询
├── 🎨 assets/                    # Images & resources | 图片和资源
└── ⚙️ config/                    # Configuration | 配置文件
```

---

## 🎭 Four Identities System | 四身份系统

This skill automatically switches between four identities:

本 Skill 自动在四种身份间切换：

| Identity | Role | Trigger | 身份 | 角色 | 触发条件 |
|----------|------|---------|------|------|----------|
| **DM** | Neutral referee | Default | **DM** | 中立裁判 | 默认 |
| **MONSTER** | Hostile creature | Monster's turn | **怪物** | 敌对生物 | 怪物回合 |
| **NPC** | Game world character | NPC dialogue | **NPC** | 游戏世界角色 | NPC对话 |
| **PC** | Player companion | Player's turn | **PC** | 玩家队友 | 玩家回合 |

---

## 🛠️ MCP Tools | MCP 工具

| Tool | Description | 工具 | 说明 |
|------|-------------|------|------|
| `get_monster` | Query monster stats | 查询怪物数据 |
| `get_spell` | Query spell details | 查询法术详情 |
| `get_character` | Load PC data | 加载角色数据 |
| `calculate_attack` | Combat calculation | 战斗计算 |
| `roll_dice` | Dice roller | 掷骰子 |

---

## 📖 Supported Modules | 支持的模组

- ✅ **Lost Mine of Phandelver** (凡戴尔的失落矿坑) - Complete
- 🔄 **More coming soon...** | 更多模组开发中...

---

## 📝 Character Sheet Template | 人物卡模板

Create a new PC using the template:

使用模板创建新角色：

```bash
cp data/pc_profiles/TEMPLATE.json data/pc_profiles/myhero.json
# Edit with your character info | 编辑你的角色信息
```

See `data/pc_profiles/README.md` for details.

详情见 `data/pc_profiles/README.md`。

---

## 🎮 Example Session | 示例会话

```
User: 开始凡戴尔的失落矿坑
DM: 【场景】你们站在三猪小径上...
     马车前方传来急促的马蹄声...

User: 我拔出武器准备战斗
DM: 【战斗开始】先攻检定：
     萨尔坦 d20+1 = 15
     敌人 d20+2 = 12
     
     你的回合！动作：
     A. 攻击地精
     B. 保护同伴
     C. 其他行动

User: A，攻击地精
DM: 【萨尔坦攻击】
     攻击检定: d20(14) + 5 = 19 vs AC 15 → 命中！
     伤害: d8(6) + 3 = 9 挥砍伤害
     
     地精 HP: 7/7 → 0/7 💀 死亡！
```

---

## 🧩 Core Principles | 核心原则

1. **查阅原文** | Consult original text - Never rely on memory | 绝不凭记忆
2. **使用工具** | Use tools - Query data via MCP | 通过 MCP 查询数据
3. **不剧透** | No spoilers - Strict information tier management | 严格信息层级管理
4. **计算透明** | Transparent calculations - Show every roll | 展示每次掷骰
5. **模组忠实** | Module faithful - No additions or deletions | 不增删模组内容

---

## 📊 Information Tiers | 信息层级

| Tier | Type | Can Share? | 层级 | 类型 | 可分享？ |
|------|------|------------|------|------|----------|
| Tier 1 | Player knowledge | ✅ Yes | 玩家知识 | ✅ 是 |
| Tier 2 | Character knowledge | ✅ Conditional | 角色知识 | ✅ 有条件 |
| Tier 3 | DM only | ❌ Never | DM专属 | ❌ 绝不 |

---

## 🤝 Contributing | 贡献

Contributions welcome! Please read `CONTRIBUTING.md` first.

欢迎贡献！请先阅读 `CONTRIBUTING.md`。

## 📜 License | 许可证

[MIT License](LICENSE) - See file for details.

[MIT 许可证](LICENSE) - 详见文件。

**Note**: D&D 5e rules are copyright © Wizards of the Coast. This project is for educational and personal use only.

**注意**: D&D 5e 规则版权归 Wizards of the Coast 所有。本项目仅供教育和个人学习使用。

---

## 🙏 Acknowledgments | 致谢

- **OpenClaw** - AI tabletop platform
- **5etools** - Open 5e SRD data
- **All D&D players** - For the love of the game

- **威世智** - D&D 5e 规则和模组
- **OpenClaw** - AI 跑团平台
- **5etools** - 开源 5e SRD 数据
- **所有 D&D 玩家** - 对游戏的热爱

---

<p align="center">
  <b>May your rolls be natural 20s! 🎲</b><br>
  <b>愿你的骰子总是自然20！🎲</b>
</p>
