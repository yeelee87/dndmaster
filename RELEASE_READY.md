# D&D Game Master Skill v1.0.0 - 发布就绪

## ✅ 清理完成

此版本已移除所有跑团测试数据，准备好发布到 GitHub。

## 📁 文件结构

```
dnd-game-master/
├── 📄 核心文件
│   ├── SKILL.md              # Skill主配置（必需）
│   ├── README.md             # 项目说明
│   ├── LICENSE               # MIT许可证
│   ├── CHANGELOG.md          # 更新日志
│   ├── CLEANUP.md            # 清理记录
│   ├── GITHUB_PUBLISH.md     # 发布指南
│   ├── MCP_TOOLS_GUIDE.md    # 工具使用指南
│   ├── .gitignore            # Git忽略规则
│   ├── .gitattributes        # Git行尾规范
│   └── release.sh            # 发布脚本
│
├── ⚙️ 配置
│   └── config/
│       └── active_module.json    # 模块配置（已重置）
│
├── 🎲 数据
│   └── data/
│       ├── pc_profiles/      # 玩家角色模板
│       │   ├── README.md
│       │   └── TEMPLATE.json
│       ├── npc_profiles/     # LMOP NPC档案（6个角色）
│       │   ├── README.md
│       │   ├── daran-ederamath.json
│       │   ├── droop.json
│       │   ├── halia-thornton.json
│       │   ├── ian-alkbreck.json
│       │   ├── qelline-alderleaf.json
│       │   └── sildar-hallwinter.json
│       ├── lmop_chapters/    # LMOP模组分段
│       ├── 5etools/          # 5e数据
│       └── campaign_state.json   # 战役状态（已重置）
│
├── 📚 参考资料
│   └── references/
│       ├── core-rules/       # PHB/MM/DMG规则
│       └── modules/          # 官方模组原文
│
├── 🔧 脚本
│   └── scripts/              # Python工具脚本
│       ├── combat_engine.py
│       ├── character_parser.py
│       └── dnd_data_manager.py
│
└── 🎨 资源
    └── assets/               # 图片等资源
```

## 🎯 核心功能

1. **严格遵守 D&D 5e 2014 规则**
   - PHB/MM/DMG 核心规则
   - 每步战斗计算透明展示

2. **LMOP 模组完整支持**
   - 官方模组原文分段
   - NPC 档案和行为指南
   - 信息层级管理（防剧透）

3. **自动身份切换**
   - DM（中立裁判）
   - MONSTER（敌对生物）
   - NPC（游戏世界角色）
   - PC（玩家队友）

4. **工具支持**
   - 怪物数据查询
   - 法术数据查询
   - 战斗计算
   - 人物卡解析

## 🚀 发布步骤

### 1. 在 GitHub 创建仓库

访问：https://github.com/new
- Repository name: `openclaw-skill-dnd-game-master`
- Description: `A professional D&D 5e Game Master skill for OpenClaw`
- Public/Private: 自选
- **不要**勾选 "Add a README"

### 2. 本地初始化并推送

```bash
cd /Users/sid/.openclaw/workspace/skills/dnd-game-master

# 或使用提供的脚本
./release.sh

# 或手动执行:
git init
git add .
git commit -m "v1.0.0: D&D 5e Game Master Skill"
git remote add origin https://github.com/YOUR_USERNAME/openclaw-skill-dnd-game-master.git
git branch -M main
git push -u origin main
```

### 3. 创建 Release

在 GitHub 仓库页面：
1. 点击 **Releases** → **Create a new release**
2. Tag: `v1.0.0`
3. Title: `Initial Release - LMOP Support`
4. 描述主要功能

## 📊 文件大小

- **总大小**: 48MB
- **主要组成**: 5etools 数据文件 (~25MB) + 模组文档 (~22MB)
- **代码**: <1MB

如需更小的仓库，可在 `.gitignore` 中添加：
```
data/5etools/
```

## 📝 使用示例

安装到 OpenClaw：
```bash
cd ~/.openclaw/skills
git clone https://github.com/YOUR_USERNAME/openclaw-skill-dnd-game-master.git dnd-game-master
```

开始游戏：
```
/use dnd-game-master

"开始凡戴尔的失落矿坑"
"创建一个新角色"
```

## 🎉 完成！

现在可以分享给社区了！
