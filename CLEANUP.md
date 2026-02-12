# 清理记录 (Cleanup Log)

## 2026-02-12 清理内容

### 移除的跑团数据

1. **Campaign State** (`data/campaign_state.json`)
   - 重置为默认空状态
   - 移除了：章节进度、地点发现、NPC 相遇记录、任务状态

2. **Config** (`config/active_module.json`)
   - 重置为默认配置
   - 移除了：战役进度、已发现地点、已遇见 NPC

3. **PC Profiles** (`data/pc_profiles/`)
   - 删除了测试角色：
     - `test_character.json`
     - `test_fighter_1.json`
     - `test_final.json`
     - `test_level2.json`
     - `test_sartan_l2.json`
     - `example-fighter.json`
   - 添加了 `TEMPLATE.json` 作为角色创建模板

4. **NPC Profiles** (`data/npc_profiles/`)
   - 保留了 LMOP 模组 NPC（这些是模组内容，不是跑团数据）
   - 添加了 `README.md` 说明

5. **Cache** (`data/cache/`)
   - 添加到 `.gitignore`，不纳入版本控制

### 保留的文件

- 所有模组原文 (`references/modules/`)
- 核心规则文档 (`references/core-rules/`)
- 脚本 (`scripts/`)
- 静态资源 (`assets/`)
- NPC 档案 (`data/npc_profiles/*.json`)

### 新增文件

- `TEMPLATE.json` - 角色卡模板
- `pc_profiles/README.md` - 角色卡使用说明
- `npc_profiles/README.md` - NPC 档案说明
- `.gitattributes` - Git 行尾规范
- 更新 `.gitignore` - 排除运行时生成的文件

## 如何使用清理后的版本

### 1. 创建新角色

复制模板：
```bash
cp data/pc_profiles/TEMPLATE.json data/pc_profiles/你的角色.json
```

编辑文件，填写角色信息。

### 2. 开始新游戏

```
/use dnd-game-master

"开始凡戴尔的失落矿坑模组"
"读取我的角色：pc_profiles/你的角色.json"
```

### 3. 游戏自动保存

游戏进度会自动保存到：
- `data/campaign_state.json`
- `config/active_module.json`

这些文件已被添加到 `.gitignore`，不会被提交到 Git。

## 文件大小

清理前：~48MB（含缓存和跑团数据）
清理后：~48MB（主要是 5etools 数据文件）

如需更小的仓库，可以在 `.gitignore` 中取消注释：
```
# data/5etools/
```
这样可以排除大型数据文件，只保留代码和文档。
