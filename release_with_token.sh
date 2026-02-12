#!/bin/bash
# GitHub Token 发布脚本

echo "🎲 D&D 5e Game Master Skill - GitHub 发布"
echo "=========================================="
echo ""

# 检查是否有 token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 需要设置 GITHUB_TOKEN 环境变量"
    echo ""
    echo "获取方式："
    echo "1. 访问 https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 勾选 'repo' 权限"
    echo "4. 复制 token"
    echo ""
    echo "然后运行："
    echo "   export GITHUB_TOKEN=你的token"
    echo "   ./release_with_token.sh"
    exit 1
fi

cd /Users/sid/.openclaw/workspace/skills/dnd-game-master

# 配置 Git
git config user.name "OpenClaw Skill Publisher"
git config user.email "skill@openclaw.ai"

# 推送到 GitHub
REPO_URL="https://${GITHUB_TOKEN}@github.com/yeelee87/dndmaster.git"

git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

echo "🚀 推送到 GitHub..."
git push -u origin main --force

echo ""
echo "✅ 发布完成！"
echo "   https://github.com/yeelee87/dndmaster"
