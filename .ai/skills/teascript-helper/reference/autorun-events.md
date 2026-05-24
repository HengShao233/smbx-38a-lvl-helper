# Autorun Events 速查

> 来源：`.docs/.teascript-docs/Autorun Events.md`

引擎在特定时机自动调用、按 **精确名字** 绑定的事件。在 lvl 文件里它仍是普通的 `E|` 行，名称必须**完全匹配**下表。

| 事件名 | 触发时机 | param1 | param2 | param3 |
| --- | --- | --- | --- | --- |
| `Level - Start` | 关卡开始（标准事件，不可删/重命名） | 0 | 0 | 0 |
| `Level - End` | 玩家完成关卡（含死亡） | 退出类型（11/12/5/1/2/7/4/8/80/81/6/99/88） | 0 | 0 |
| `P Switch - Start` | P 开关激活 | 通常 0；脚本触发为 2 | 通常 0；脚本触发为 3 | 0 |
| `P Switch - End` | P 开关失效 | 0 | 0 | 0 |
| `Player - GotHurt` | 玩家受伤（不死） | 玩家索引 | 0 | 0 |
| `Player - GotItem` | 拾取道具（修改 status 的） | 玩家索引 | 新 status | 0 |
| `Player - GotNPChurt` | 与伤害 NPC 接触帧（含无敌帧） | 玩家索引 | 0 | 0 |
| `Player - Swimming` | 进入水液体 | 玩家索引 | 0 | 0 |
| `Player - Warping` | 使用传送门 | 玩家索引 | 传送门索引 | 0 |
| `Player - Death` | 玩家死亡 | 玩家索引 | 0 | 0 |
| `NPC - Death` | NPC 任意原因死亡 | NPC 索引 | 0 | 0 |
| `NPC - Killed` | 玩家行为造成的 NPC 死亡 | NPC 索引 | 0 | 0 |
| `Timer - Over` | 倒计时归 0 | 0 | 0 | 0 |
| `Starman - Start` | 拾取超级星 | 玩家索引 | 0 | 0 |
| `Starman - End` | 无敌结束 | 玩家索引 | 0 | 0 |
| `Megamushroom - Start` | 大蘑菇激活 | 玩家索引 | 0 | 0 |
| `Megamushroom - End` | 大蘑菇结束 | 玩家索引 | 0 | 0 |

## 在事件脚本中读取参数

在 TeaScript 中通过 sysval：

```teascript
' 在 NPC - Death 事件脚本里
dim npcIdx as integer
npcIdx = sysval(param1)
' 现在可以用 NPC(npcIdx).field 访问刚死的 NPC
```

## 注意事项

1. 名字必须 **完全一致**（含空格、大小写、连字符前后空格）。
2. `Level - Start` 是 **必备且不可删** 的事件；不要尝试 `--del E --where name=Level - Start`。
3. `Timer - Over` 一旦存在，玩家在倒计时 0 时不会被杀死。
4. 自动事件可以像普通事件一样被脚本 `call SET("EventName")` 触发。
