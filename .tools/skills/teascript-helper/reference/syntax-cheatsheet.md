# TeaScript 语法速查

> 完整文档：`.docs/.teascript-docs/TeaScript Syntax.md`
> 本文档仅留 AI 写代码所需的核心要点。

TeaScript 是 5438A38A 为 SMBX 38A 开发的 **VB6 风格脚本方言**。

## 注释 / 行尾

```teascript
' 这是一行注释（不是 // 也不是 #）
```
- 行尾不需要分号。
- 字符串使用双引号 `"..."`；想写 `"` 用 `chrW(34)`。

## 三类变量

| 类型 | 声明 / 创建 | 读 | 写 | 作用域 |
| --- | --- | --- | --- | --- |
| **User Variable**（推荐） | **必须**在 lvl 的 V 行（或 wls 的 G 行）预声明，引擎不"按需创建" | `val(name)` 或 `v(name)` (double); `str(name)` (string) | `v(name) = ...` / `str(name) = ...` | 关卡内 |
| **Global User Variable** | 同上，勾选 global | `gval(name)` / `gstr(name)` | `gv(name) = ...` / `gstr(name) = ...` | 跨关卡持久 |
| **User Array**（推荐） | **必须**在 lvl 的 **R 行** 预声明（`R\|arr1\|arr2\|...`，**不是 V 行**！）；脚本里先 `call redim(0, arr, len)` 初始化 | `array(arr(i))` (double); `strarray(arr(i))` (string) | `array(arr(i)) = ...` | 同上 |
| **Dim Variable** | `dim x as type [= value]` | 直接写名字 | `x = ...` | 当前 script |

> ⚠ **每次脚本里出现 `v(myFlag)` 之前，必须确认 lvl 中已有 `V|<encoded>|0|0` 行**。
> 用 `python .tools/skills/smbx-38a/scripts/lvl_var_check.py <lvl>` 一键验证，
> 加 `--fix` 会自动补缺失的 V 行。

字符串拼接在 message/TXTCreate 里要用 `&v(name)` / `&gv(name)` / `$val(name)` / `$gvl(name)` 这种特殊前缀。

### Dim 类型清单

| 类型 | 范围 |
| --- | --- |
| `byte`    | -128..127 |
| `integer` | -32768..32767 |
| `long`    | -2^31..2^31-1 |
| `single`  | 单精度浮点 |
| `double`  | 双精度浮点（推荐） |
| `string`  | 字符串 |

> **注意（已在 1.4.5 修复）**：在全局脚本中，老版本不能用 `long/single/double`，请用 `byte/integer`。

## 命名规范

- 不区分大小写
- 不能含空格
- 只能字母+数字
- 必须字母开头
- `script` 名**额外**：不能含数字

## 运算符

数学：`+ - * / \ ^ mod` （`/` 为浮点除，`\` 为整除；`mod` 为模）
字符串：`&`（拼接）
比较：`= <> > < >= <=` 返回 -1（真）或 0（假）。**不能跨类型比较，否则 crash！**
逻辑：`not / and / or / xor / eqv / imp`（仅作用于数字；约定 -1=真 0=假）
位移：`<< >>`

> **真假约定**：-1 = true，0 = false；其它非零数也是 true。

## 控制流

```teascript
' 单行 if
if x > 0 then x = x - 1

' 完整 if
if x > 0 then
    x = x - 1
elseif x < 0 then
    x = x + 1
else
    ' do nothing
end if

' select case
select case sysval(coincount)
    case 0
        v(broke) = -1
    case 1 to 99
        v(broke) = 0
    case is >= 100
        v(broke) = 0
    case else
        ' fallback
end select

' do loop（必须有退出）
do
    if condition then exit do
    call sleep(1)         ' 没有 sleep/exit 会冻结游戏！
loop

' do until / do while
do until x > 10
    x = x + 1
loop

do while x < 10
    x = x + 1
loop

' for
' ⚠ 38A 实测：`next` 后**不能跟变量名**，只能裸写 `next`。
'    `next i` / `next k` 这种 VB6/QBasic 风格写法在 TeaScript 中是语法错误！
for i = 1 to 10
    ' ...
next

for i = 10 to 1 step -1
    ' ...
next

' 跳出 / 继续
exit do          ' 跳出 do 循环
exit for         ' 跳出 for 循环
```

## 函数 / 过程（custom scripts）

```teascript
' 必须放在脚本文件最末尾！
script myFunc(a as double, b as double, return double)
    if a > b then return a
    return b
end script

script myProc(x as double)
    sysval(disablejump) = x
end script

' 调用
dim r as double
r = myFunc(1, 2)
call myProc(-1)

' 让函数全局可见
export script utilFunc(x as double, return double)
    return x * 2
end script
```

## 内置常量与特殊值

| 名 | 含义 |
| --- | --- |
| `pi` | 3.141592654 |
| `e`  | 2.71828182 |
| `rnd` | 每次访问得到 0..1 之间的新随机数 |

## 系统访问

```teascript
sysval(name)                        ' 系统变量（如 ncount, coincount, scrsplitstyle）
sysval(name) = value                ' 部分可写
char(idx).field                     ' 玩家数据：char(1).x, char(1).status
NPC(idx).field                      ' NPC 字段：NPC(i).id, NPC(i).x, NPC(i).hp
Block(idx).field                    ' Block 字段
BGO(idx).field                      ' 背景对象
.field                              ' leading-dot：仅在 `with object ... end with`
                                    ' 块内有效，等价于 object.field。
                                    ' 没有"隐式 with"——任何脚本（包括 NPC 类绑定
                                    ' 脚本、事件脚本）都需要先建 with 块或显式
                                    ' 写 NPC(idx)/char(1)/Block(i)。
                                    ' NPC 类绑定脚本里取自身索引：
                                    '   selfIdx = sysval(param1)
                                    '   with NPC(selfIdx) ... end with
```

> 完整字段表见 `.docs/.teascript-docs/Char (TeaScript).md` / `NPC (TeaScript).md` / 等。

## 常见陷阱

1. **死循环 = 卡死游戏**：必须有 `sleep` 或 `exit do`。
2. **除/模 0 = crash**：`a / 0` `a mod 0` `a \ 0`。
3. **跨类型比较 = crash**：`"abc" = 1` 这种不要写。
4. **`dim` 在 if 块内会 buggy**（patch 31 之前）：`dim` 写在 `if` 外面。
5. **`script` 块必须在文件最末尾**：放中间会出错。
6. **变量名不区分大小写**，但仍建议保持风格一致。
7. **0^0 = 1**（不是 NaN）。
8. **`(-1)^(0.5)` 会报错**；用 `x^(0.5)` 在 dim 后才不会报错。
9. **写引号到字符串**用 `chrW(34)`。
10. **❌ `SET()` 不是 TeaScript 函数**。`SET` / `SLT` / `TMG` 是 IPC 命令（外部调试用），脚本里调用会编译失败。
   触发自定义事件没有简单 API；推荐通过 `LSet(layer, type, smoke)` 直接控制图层、或在事件链中用 `nextevent`。
11. **❌ Procedure 内不能用 `return` 单独退出**。规则：脚本中**有 `return`**就被判为 function（必须声明 return type），**无 `return`**才是 procedure。
   想从 procedure 提前退出，请用 `if/end if` 包住有效路径，让流程自然结束。
12. **TeaScript 用户变量名规约**：仅字母+数字，字母开头，无下划线（与关卡 `V` 行规约一致）。`v(_init)` 这种会被引擎拒绝。
13. **❌ 代码语句后不要跟行尾注释**（38A 实测引擎 bug）。例如：
    ```teascript
    ' 错误：会让引擎在 id 处报"未声明变量"等假错
    id = 134                  ' 火球类直线
    vy = 0
    ```
    正确做法：注释独占一行写在语句之前。
    ```teascript
    ' 火球类直线
    id = 134
    vy = 0
    ```
    建议**所有注释都单独一行**，不要在赋值/`call`/`v(...)` 等语句后面拖注释。Lint 规则 `E014` 已加。
14. **用户数组用 R 行声明，不是 V 行**：
    ```
    R|<urlencoded_arr1>|<urlencoded_arr2>|...
    ```
    一行声明所有数组，每段一个名字。如果用 `V|name|0|1` 假装数组，引擎会报 `undeclared variable`。**新建关卡用 `LVLBuilder.add_array('echoX','echoY')`**（已封装，自动生成 R 行）。详见 `.tools/skills/smbx-38a/reference/lvl-format.md` 踩坑表项 21。
15. **❌ 38A 没有"每帧自动事件"**。`autostart=1` 仅触发**一次**（在 Level Start 那一帧）。每帧逻辑必须用 `do ... call sleep(1) ... loop` 范式实现：
    ```teascript
    ' 标准每帧范式
    ' 一次性初始化（dim 在 do 外）
    dim i as integer
    v(myCounter) = 0
    
    do
        ' 这里是每帧执行的代码
        v(myCounter) = v(myCounter) + 1
        ' ... 业务逻辑 ...
        
        call sleep(1)   ' 必不可少，否则游戏冻结！
    loop
    ```
    一个 lvl 只允许一个 `Level - Start` 事件，多个长循环脚本要分别挂在 `Level - Start` 和其他 `autostart=1` 的自定义事件名上（如 `HUDStart` / `BossStart` 等）。
16. **FXCreate 是 10 参**：`FXCreate(ID, X, Y, Xsp, Ysp, Frames, AnimationSpeed, Const, Gravity, Advanced)`。常见错误：照旧 wiki 写 8 参漏掉 Gravity / Advanced。Lint 规则 `E013` 已校正。
17. **`alive` 字段在 NPC 与 Char 上语义相反**！
    - **NPC.alive**: `0 = 死`，非 0 = 活（与英文字面一致）— 销毁 NPC 用 `NPC(idx).alive = 0`
    - **Char.alive**: `1 = 死`，`0 = 活`（反直觉！38A 文档原文 "Forcing this value to 1 will kill the player"）

    因为相反极易记错，**玩家伤害/死亡推荐用 `call SpEvent(...)`**：

    | id | 含义 |
    |---|---|
    | 1 | Hurts the player（引擎自动降级 + 无敌 + 形态正确转换） |
    | 2 | Kills the player（直接死） |
    | 3 / 4 | Hide / Show HUD |
    | 7..10 | 给 mushroom / fire flower / leaf / tanooki 进地图道具栏 |

    ```teascript
    ' ✅ 推荐 — 让引擎处理一切
    if char(1).invtime <= 0 then
        call SpEvent(1)        ' 受伤
        ' 或 call SpEvent(2)   ' 直接杀
    end if

    ' ❌ 易错 — 自己手写降级 + 反向 alive
    if char(1).status > 1 then
        char(1).status = char(1).status - 1
        char(1).invtime = 100
    else
        char(1).alive = 1      ' 1=死，反直觉，老忘
    end if

    ' ✅ NPC 销毁直接用 alive=0（NPC 这边是常识方向）
    NPC(idx).alive = 0
    ```

## 内置函数签名常错点（重要！）

写脚本前**必查 `reference/builtin-functions.md` 和 `.docs/.teascript-docs/Functions (TeaScript).md`**，
不要凭直觉写参数数量。下表列几个经常被写错的：

| 函数 | 错误写法 | 正确写法 |
| --- | --- | --- |
| `NCreate` | `NCreate(id, x, y, vx, vy, advset)` (6 参) | `NCreate(id, x, y, vx, vy, advset, creationData)` (**7 参**, 本仓库目标引擎要求 7) |
| `FXCreate` | `FXCreate(id, x, y, vx, vy, grv, fsp, life)` (8 参) | `FXCreate(ID, X, Y, Xsp, Ysp, Frames, AnimationSpeed, Const, Gravity, Advanced)` (**10 参**) |
| `LMove`   | `LMove("L", vx, vy)` (3 参) | `LMove("L", vx, vy, type)` (**4 参**, type=0 按速度移动 / 1 按相对位移) |
| `LSet`    | `LSet("L", show)` (2 参) | `LSet("L", type, smoke)` (**3 参**, type 1=show 2=hide 3=toggle 38=alpha) |
| `BSet`    | 参数随意 | `BSet(type, ID, FlagID, p1, p2, p3)` (**6 参**) |
| `AudioSet`| 总忘加 `""` | `AudioSet(2, ID, Loop, "")` 4 参，最后那个空串必给 |

## 自动事件（Autorun Events）

引擎在特定时刻自动调用、与名字精确绑定的事件：

`Level - Start` / `Level - End` / `P Switch - Start` / `P Switch - End` /
`Player - GotHurt` / `Player - GotItem` / `Player - GotNPChurt` / `Player - Swimming` /
`Player - Warping` / `Player - Death` / `NPC - Death` / `NPC - Killed` /
`Timer - Over` / `Starman - Start` / `Starman - End` /
`Megamushroom - Start` / `Megamushroom - End`

详见 [`autorun-events.md`](./autorun-events.md)。

## 事件 ↔ 脚本绑定

在 lvl 文件中，`E|name|...|...|...|ene` 行的 `ene` 子字段（最后一段）形如：
```
ene = nextevent/timer/apievent/scriptname
nextevent = name,delay
timer     = enable,count,interval,type,show
```
若 `scriptname` 为某 `S`/`Su` 的脚本名（URL 编码），事件触发时会运行该脚本。
本 skill 提供 `teascript_event.py` 自动构造该 `E` 行。
