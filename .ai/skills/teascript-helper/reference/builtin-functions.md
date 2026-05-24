# TeaScript 内置函数速查

> 完整文档：`.docs/.teascript-docs/Functions (TeaScript).md`
> 此处只给函数名 + 简短说明 + 调用形式，详情请回查权威文档。

## 调用约定

| 形式 | 用法 |
| --- | --- |
| **过程**（无返回值） | `call funcName(args)` |
| **函数**（有返回值） | `x = funcName(args)`，参数包在表达式里 |

---

## 数学 / 转换

| 函数 | 返回 | 说明 |
| --- | --- | --- |
| `abs(x)` | num | 绝对值 |
| `exp(x)` | num | e^x |
| `log(x)` | num | 自然对数 |
| `sgn(x)` | num | 1 / 0 / -1 |
| `int(x)` | num | 向下取整（floor）`int(-2.2) = -3` |
| `fix(x)` | num | 截尾取整 `fix(-2.2) = -2` |
| `sqr(x)` | num | 平方根 |
| `sin/cos/tan/atn(x)` | num | 弧度三角函数 |
| `getangle(x, y)` | num | atan2，结果是 0..1 的角度比 |
| `chr(n) / chrW(n)` | str | ASCII / Unicode 字符 |

## 数组

| 函数 | 说明 |
| --- | --- |
| `redim(type, arr, len)` | 初始化用户数组。`type=0` 是 double 数组。**先 redim 再用！** |

## 音频

| 函数 | 说明 |
| --- | --- |
| `AudioSet(1, ID, Advanced, Filepath)` | 加载音效 |
| `AudioSet(2, ID, Loop, "")`            | 播放音效 |
| `AudioSet(3, ID, 0, "")`               | 停止音效 |
| `AudioSet(5, ID, Volume, "")`          | 设置音量 |
| `AudioSet(11, FadeIn, 0, Filepath)`    | 播放音乐 |
| `AudioSet(12, FadeOut, 0, "")`         | 停止音乐 |

## HUD / UI

| 函数 | 说明 |
| --- | --- |
| `HUDSet(...)` | 配置 HUD 元素，参数较多详见原文 |
| `ShowMsg(msg)` | 显示消息（同游戏内消息框） |
| `SysShowMsg(d1, d2, d3)` | 调试消息（数字） |
| `SysShowInput(prompt)` | 弹窗输入 |

## 文本对象（Text）

| 函数 | 说明 |
| --- | --- |
| `TCreate(id, ...)` | 创建文本对象 |
| `TCreateEx(...)` | 进阶创建（多参数） |
| `TClear(id)` | 销毁文本对象 |
| `TxtCreate(id, ...)` | 文本/动态消息 |
| `BErase(type, id)` | 通用销毁：0=Iterator 1=Text 2=Bitmap 3=Block |

## Bitmap / 图像

| 函数 | 说明 |
| --- | --- |
| `BmpCreate(id, picid, useScreenCoords, isVisible, sx, sy, sw, sh, destx, desty, stretchx, stretchy, centerx, centery, angle, color)` | 创建自定义 bitmap |
| `BErase(2, id)` | 销毁 bitmap |

## 效果 / NPC / Block 操作

| 函数 | 说明 |
| --- | --- |
| `FXCreate(id, x, y, sx, sy, grv, fsp, life)` | 生成特效 |
| `NCreate(id, x, y, ...)`        | 生成 NPC |
| `NCreateGroup(...)`             | 批量生成 NPC |
| `NKill(npcIdx)`                 | 杀死 NPC |
| `BSet(...)`                     | 修改对象配置位（多参，详见 BSet 文档） |
| `LMove(layer, hsp, vsp)` | 图层运动 |
| `LSet(...)`     | 图层属性 |
| `LSpin(layer, ...)` | 图层旋转 |

## 迭代器

| 函数 | 说明 |
| --- | --- |
| `ItrCreate(id, type, ...)` | 创建迭代器 |
| `ItrNext(id)` | 步进 |

详见 `.docs/.teascript-docs/Iterators.md`。

## 输入

| 函数 | 说明 |
| --- | --- |
| `KeyPress(playerIdx, keyCode)` | 检查按键 |

## 控制流 / 时机

| 函数 | 说明 |
| --- | --- |
| `Sleep(frames)` | 暂停脚本 N 帧（`call sleep(60)` ≈ 1 秒） |
| `EXEScript(name)` | 执行另一个脚本（同步，运行完才继续） |
| `SpEvent(...)` | 触发特殊事件 |
| `ScriptID()` | 取当前脚本 id |
| `SCSet(...)` | 配置脚本相关 |
| `Debug(msg)` | 控制台调试 |
| `PlayNote(...)` | 播放音符 |

## 系统变量速查（部分）

只读：`ncount` `bcount` `bgocount` `wcount` `lcount` `ecount` `actncount` `actbcount`
读/写：`score` `coincount` `playerhealth`
其它：`gamemode` `gametime` `lvltimer` `starcount` `starcoincount`
摄像机：`player1scrx` `player1scry` `player2scrx` `player2scry` `scrsplitstyle`
能力：`enablewalljump` `disablejump` `disablespinjump` `disableduck` `disableclimbing` ……
游戏机制：`enablelighting` `enablesmb3statussys` `coinsforextralife` `showhud` `enablepause` `disablesave` ……
事件参数：`param1` `param2` `param3`（事件源给到的参数）
窗口：`gametitle`（只写）

> 完整 ~80 个 sysval 见 `.docs/.teascript-docs/Sysval (TeaScript).md`。
