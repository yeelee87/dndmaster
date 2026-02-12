#!/bin/bash
# 最终发布脚本 - 清理版本

echo "🎲 D&D 5e Game Master Skill - 发布脚本"
echo "========================================"
echo ""

cd /Users/sid/.openclaw/workspace/skills/dnd-game-master

# 检查 Git 状态
echo "📋 Git 状态检查..."
git status --short

echo ""
echo "📦 准备提交的文件:"
git add -n .

echo ""
echo "✅ 清理完成！以下文件已准备提交:"
echo "   - README.md (项目说明)"
echo "   - LICENSE (MIT许可证)"
echo "   - SKILL.md (主配置)"
echo "   - TEMPLATE.json (角色卡模板)"
echo "   - 脚本和数据文件"
echo ""

read -p "是否执行提交并推送到 GitHub? (y/n): " confirm

if [ "$confirm" = "y" ]; then
    git add .
    git commit -m "Clean release: D&D 5e Game Master Skill v1.0.0

Features:
- Strict D&D 5e 2014 rule compliance
- LMOP module support with full text
- Auto identity switching (DM/Monster/NPC/PC)
- Combat engine with transparent calculations
- Character parser (JSON/Excel)
- Monster/spell data query via 5etools
- Information tier management (anti-spoiler)
- NPC database for LMOP
- PC character template

Cleaned:
- Removed test character files
- Reset campaign state
- Added .gitignore for runtime files
- Added documentation"

    echo ""
    echo "🚀 提交完成！"
    echo ""
    echo "下一步:"
    echo "1. 确保已添加远程仓库:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/openclaw-skill-dnd-game-master.git"
    echo ""
    echo "2. 推送到 GitHub:"
    echo "   git push -u origin main"
    echo ""
else
    echo "❌ 取消提交"
    echo ""
    echo "手动提交命令:"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    echo "  git push origin main"
fi
