# PC Profiles - 玩家角色卡

此目录存放玩家角色（PC）的人物卡数据。

## 格式

支持以下格式：
- **JSON** (`.json`) - 推荐，结构清晰
- **Excel** (`.xlsx`) - 便于编辑

## 使用方法

1. 复制 `TEMPLATE.json` 创建新角色
2. 填写角色信息
3. 重命名为角色名称（如 `sartan.json`）
4. 在游戏中通过工具读取：`get_character(file_path="pc_profiles/sartan.json")`

## 必需字段

- `name` - 角色名称
- `race` - 种族
- `class` - 职业
- `level` - 等级
- `ability_scores` - 六项属性值
- `hp` - 生命值（max/current）
- `ac` - 护甲等级

## 可选字段

详见 `TEMPLATE.json` 中的完整结构。

## 示例角色

参考 `TEMPLATE.json` 了解完整格式。
