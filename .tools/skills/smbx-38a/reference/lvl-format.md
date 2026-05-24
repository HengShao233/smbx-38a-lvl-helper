# LVL/WLD/WLS 格式速查（精炼版）

> 完整规范见 `.docs/.smbx38a-docs/smbx-38A File specifications (LVL WLD WLS).md`。
> 本文档仅列出工具实现/AI 阅写所需的最小信息。
>
> **⚠️ 实战补丁**：所有标注 `[踩坑]` 的项是经过引擎实测验证的格式约束，
> 偏离这些约定 → 关卡加载时必报 `run-time error '13' Type Mismatch`。

## 通用规则

- 文件首行：`SMBXFile??`，`??` 为版本号（项目内常见 `65`、`66`、`69`）。
- ASCII 文本，**Non-ASCII 字段 URL 编码**，**脚本 Base64 编码**。
- 每行第一个 token 为 marker（`A`、`B`、`N`、`S`、…），其后字段以 `|` 分隔。
- 子字段用 `,` 或 `/` 分隔。
- **行尾允许追加额外字段**，禁止改动已有字段顺序。
- 空字符串 `""` 视为图层名 `Default`。

## ⚠️ 踩坑总表（必读）

| 序号 | 字段 | 错误 | 正确 |
| --- | --- | --- | --- |
| 1 | 字符串字段 (layer/name/title 等) | 裸字母 `Default`、`OnSober` | **每个字符强制百分号编码** `%44%65%66%61%75%6C%74` |
| 2 | `A` 行字段数（不含 marker） | 4 (`0\|title\|\|,,,`) | **5** (`0\|title\|\|\|,,,`) |
| 3 | `B` 行 `contain` | `contain=0` | **空字符串** |
| 4 | `N` 行 `b` 字段 | `0,0,0,0` (4 个数) | `0,0,0,0,0,0` (**6 个数**) |
| 5 | `N` 行 events/attach | 占位 `0,0,0,0,0,0,0\|0,0` | **空字符串** `\|\|` |
| 6 | `M` 行 | 只声明用到的 section | **必须 21 行** (id=1..21 全声明) |
| 7 | `V` 行字段数 | 2 | **3** (含 scope) |
| 8 | TeaScript 变量名 | `_init`、`my_var` (下划线) | **只允许字母+数字，字母开头** |
| 9 | `E` 行 `el` 字段 | `Win=show/Default=hide` | `0/<show_csv>/<hide_csv>/<toggle_csv>` (**4 段斜杠分隔**) |
| 10 | `E` 行 `ene` (绑定脚本) | `,0/0,0,0,0,0//<script>` (空 apievent) | `,0/0,0,0,0,0/0/<script>` (**apievent 必须 `0`**) |
| 11 | `E` 行 `ene` (无脚本) | `,0/0,0,0,0,0//` (4 段空尾) | `,0/0,0,0,0,0` (**只 2 段**) |
| 12 | **脚本 `v(name)` 引用** | 脚本里直接写 `v(myFlag)` 而 lvl 中无 V 行 | **必须先在 V 行预声明**，引擎不"按需创建"；用 `lvl_var_check.py` 校验 |
| 13 | TeaScript `next` 语法 | `next i` / `next k` | **只能写 `next`** —— 38A 不允许 next 后跟变量名 |
| 14 | TeaScript `procedure` 内 `return` | 单独 `return` 退出 | 用 `if/end if` 包住路径；procedure 内出现 `return` 会被引擎判为 function 缺 return type |
| 15 | TeaScript 内置函数参数数量 | 凭印象写参数（如 NCreate 6 参） | **必须查 `.docs/.teascript-docs/Functions (TeaScript).md`** + 用 SMBX editor 实测；签名因引擎版本而异 |
| 16 | TeaScript "触发用户事件" | 写 `call SET("EventName")` | **没有该 API**；改用 `LSet(layer, type, smoke)` 切图层、或在 `ene/nextevent` 字段链事件 |
| 17 | **嵌入脚本 marker** | 用 `S\|...` 或小写 `Su\|...`（按文档） | **必须用大写 `SU\|...`**（全局脚本 `GSU\|...`）。来源：真实工作关卡 `Artworks/boss 结束 - 回忆通用过场/实现例/main.lvl` 的 12 个脚本行字节级抽样 — 全部是大写 `SU` |
| 18 | **嵌入脚本 body 编码** | 用 UTF-8 字节做 base64 | **必须用系统 ANSI / GBK 字节做 base64**。38A 是 VB6 应用，运行在中文 Windows 上把字符串当 CP936 处理。若用 UTF-8 字节，引擎按 GBK 解读会乱码 + 字符边界错乱（行尾 `\n` 被当成多字节字符的补字节"吞掉"） |
| 19 | **TeaScript 行尾注释** | `id = 134      ' 火球类` (代码后跟注释) | **注释独占一行放在前面**。38A 引擎实测 bug：代码语句 + 行尾 `'` 注释会让引擎报"未声明变量"等假错。Lint 规则 `E014` 已加。 |
| 20 | **TeaScript NCreate 参数数** | 6 参（旧版/wiki 版） | **本仓库目标引擎要求 7 参** `NCreate(ID,X,Y,Xsp,Ysp,Advset,CreationData)`。Lint 规则 `E013` 已收紧到 7。 |
| 21 | **用户数组的存储 marker** | `V\|<arr>\|0\|1`（用 V 行 + scope=1 假装数组） | **必须用 `R` 行**：`R\|<arr1>\|<arr2>\|...`。一行可声明多个数组，每段一个名字（百分号编码 + 命名规约）。脚本里仍用 `call redim(0, arr, len)` + `array(arr(idx))` 访问。**lvl_var_check.py 已识别 R 行**；新建用 `LVLBuilder.add_array('arr1','arr2',...)`。来源：本仓库实测——只有 V 行无 R 行时，引擎报"undeclared variable echoX"。 |
| 22 | **SU 行字段数** | 严格 2 段 `SU\|name\|base64body` | **实测 ≥2 段都合法**。38A editor 在 GUI 编辑保存时常给 SU 行追加第 3 段（某种 base64 元数据，约 14 字节，例如 `AQAAAAAAAAAAAA`）。引擎对 2 段和 3+ 段都接受；`lvl_validate.py` L017 已放宽到 ≥2。 |
| 23 | **每帧脚本的"挂载点"** | 用自定义事件名 `EchoTick`+autostart=1 期望"每帧触发" | 38A **没有"每帧自动事件"**——`autostart=1` 只在 `Level - Start` 那一帧触发**一次**。每帧逻辑必须放在脚本内部用 `do ... call sleep(1) ... loop` 实现。一个 lvl 只允许一个 `Level - Start` 事件，多个长循环脚本要分别挂在 `Level - Start` 和其它 autostart=1 的自定义名字事件上。 |
| 24 | **FXCreate 参数数** | 8 参 | **必须 10 参**：`FXCreate(ID, X, Y, Xsp, Ysp, Frames, AnimationSpeed, Const, Gravity, Advanced)`。Lint 规则 `E013` 已修正为 10。 |
| 25 | **传送门 = 逻辑触发区 + 视觉图形** | 只放 W 行（`b.add_warp(...)`）就完事 | **W 行只是不可见的"按上键即传送"判定区**，**玩家根本看不到它**！必须**额外放门 BGO**（`type_=2` 时）才能让玩家辨认出传送点位置。门是 32×64 (两格高)，BGO 锚点放在 `(warp_x, warp_y - 32)` 让门视觉刚好覆盖玩家踩位 + 上面一格。基于 60 个真实关卡统计，门 BGO 最常用：**id=92 (默认门)**、79、87、158、168。`LVLBuilder.add_warp()` 默认 `with_visual=True, visual_bgo_id=92`，会自动放入口和出口的门 BGO；不想要默认门时传 `with_visual=False`。Lint 规则 `L022` 会对缺门视觉的 door warp 给 warning。 |
| 26 | **NPC 类绑定脚本（npc-N.txt）** | 试图把"每帧每实例"脚本挂在事件 E 行 + autostart=1，期望 SMBX 自动给每个 NPC 实例都跑 | 38A 提供了一个**独立机制**：`<lvl文件名同名目录>/npc-<id>.txt` 是一个 INI 风格的 NPC 配置文件，里面 `scripts=<scriptName>` 行就把该 type 所有实例（含 NCreate 出来的）都绑上**每帧执行**的"类脚本"。**注意：脚本里没有"隐式 with"——必须显式 `selfIdx = sysval(param1)` 拿到当前实例索引，再 `with NPC(selfIdx) ... end with`** 或 `NPC(selfIdx).field` 访问自己。该机制不进 lvl 文件本身，而是与 lvl 同级的同名目录。详见本文件下方"NPC 类绑定脚本"小节。 |
| 27 | **`.field` leading-dot 用法** | 在普通脚本里写 `.x = 100` 期望它指 NPC(1) | 裸点 `.field` 只在 **`with object ... end with` 块内**有效，块内 `.x` 就是 `object.x`。**没有任何"隐式 with"上下文**——任何脚本（包括 NPC 类绑定脚本、事件脚本）都需要先建立 with 块或显式写 `NPC(idx)`/`char(1)`。NPC 类绑定脚本里取自身索引：**`sysval(param1)`**（这是 NextFrame NPC 事件传给脚本的参数，等于当前 NPC 的索引）。 |
| 28 | **SU base64 末尾 `=` padding 被 editor 去掉** | Python `base64.b64decode(b64)` 报 `Incorrect padding` | 38A editor 保存的 SU/GSU base64 会**去掉末尾 `=` 填充**。`b64_decode_script()` / `lvl_validate.py` 已自动补齐到 `len % 4 == 0`。如果你自己写工具：**`raw.rstrip('=') + '=' * ((-len(raw)) % 4)`** 后再 b64decode。 |
| 29 | **`alive` 字段在 NPC 与 Char 上语义相反** | 把 NPC 杀法套到玩家上：`char(1).alive = 0` 想杀玩家（错！） / 或把玩家杀法套到 NPC 上：`NPC(idx).alive = 1` 想销毁 NPC（错！） | **NPC.alive: `0=死`、非 0=活**（符合常识，对应英文 "alive" 字面意义）；**Char.alive: `1=死`、`0=活`**（反直觉，38A 文档原文 "Forcing this value to 1 will kill the player"）。这两条规则相反、极易记错。**最佳实践**：玩家伤害/死亡用 **`call SpEvent(1)` (受伤)** 或 **`call SpEvent(2)` (杀死)**——引擎自动处理大/小/火/狸/海等各形态降级与无敌，比手写 `status -= 1` + `invtime = 100` + 反向 alive 都稳。NPC 销毁仍直接 `NPC(idx).alive = 0`。 |

> 这些规则被合并实现在 `scripts/lvlfile.py`、`scripts/lvl_builder.py`、
> `scripts/lvl_validate.py` 与 `scripts/lvl_var_check.py` 里。
> AI 应**始终用 `LVLBuilder` 高层 API 创建关卡** + **用 `lvl_validate.py` + `lvl_var_check.py` 校验**，绝不要手写 `.lvl` 字段。

## LVL marker 速查

> **字段数定义**：以下"字段数"指 `lvlfile.Entry.fields` 的长度（**不含 marker token**）。

| marker | 含义 | 字段数 | 关键字段（按顺序） |
| --- | --- | --- | --- |
| `A` | Header | 5 | `stars\|title\|onDieFile\|onDieEntrance\|extra(",,,")` |
| `BTNS` | 角色按钮 | 5 | `Mario\|Luigi\|Peach\|Toad\|Link` |
| `P1`/`P2` | 玩家出生点 | 2 | `x\|y` |
| `M` | Section 设置 (×21 必备) | 14 | `id\|x\|y\|w\|h\|underwater\|wrapX\|offexit\|nbX\|nbY\|wrapY\|music\|background\|musicfile` |
| `B` | Block | 10 | `layer\|id\|x\|y\|contain\|slippery\|invisible\|destroyEvt,hitEvt,emptyEvt\|w\|h` |
| `T` | BGO | 4 | `layer\|id\|x\|y` |
| `N` | NPC | 10 | `layer\|id\|x\|y\|b1,b2,b3,b4,b5,b6\|sp\|events\|attach\|generator\|msg` |
| `Q` | Liquid/Env Box | 7 | `layer\|x\|y\|w\|h\|b1..b5\|event` |
| `W` | Warp | 17 | `layer\|x\|y\|ex\|ey\|type\|enterd\|exitd\|sn,msg,hide\|...\|noexit\|wx\|wy\|le\|we\|extra` |
| `L` | Layer | 2 | `name\|status` (name 必须百分号编码) |
| `E` | Event | 11 | `name\|msg\|ea\|el\|elm\|epy\|eps\|eef\|ecn\|evc\|ene` |
| `V` | Variable | 3 | `name\|value\|scope` (scope: 0=local, 1=global) |
| **`R`** | **User Array** | ≥1 | `arr1\|arr2\|...` ✅ **用户数组用 R 行不是 V 行**。每段一个数组名（百分号编码 + 命名规约）。脚本里 `call redim(0, arr, len)` 后 `array(arr(idx))` 访问。 |
| `S` / `Su` | Script (文档版) | 2 | `name\|base64body` ⚠ 真实关卡里**没人用**这两个；某些版本引擎不识别 |
| **`SU`** | Script (实际工作版) | **≥2** | `name\|base64body[\|extra]` ✅ **必须用大写 SU** + body 用 **GBK 字节**做 base64。**实测 SU 行可有第 3 段元数据**（GUI 编辑器保存时追加，约 14 字节 base64；2 段和 3+ 段引擎都接受） |
| `GSU` | Global Script (.wls) | ≥2 | 同上，但写在 .wls 全局 |
| `CT` | 自定义贴图 | 2 | `id\|hash` |
| `CW` | 自定义音效 | ≥1 | `id,filename` (整段一个字段，逗号分隔) |

### NPC `N` 字段细化（最常用）

```
N|layer|id|x|y|b1,b2,b3,b4,b5,b6|sp|events|attach|generator|msg
```
- `b1`：朝向 (1=左, 0=随机, -1=右)
- `b2`：友善 (0/1)
- `b3`：不移动 (0/1)
- `b4`：容器 NPC 类型 (1=npc91, 2=npc96, 3=npc283, 4=npc284, 5=npc300)
- `b5,b6`：保留位（**必须存在，全 0 即可**）
- `sp`：单个数字（special id），无 special 时为 `0`
- `events`：**空字符串**（无事件绑定时）；不要写占位 `0,0,0,0,0,0,0`
- `attach`：**空字符串**（无附加时）；不要写 `0,0`
- `generator`：`0` (无 generator) 或多字段如 `1,30,0,0,0,0,0`
- `msg`：URL 编码（每字符 `%xx`）

### Block `B` 字段

```
B|layer|id|x|y|contain|slippery|invisible|destroyEvt,hitEvt,emptyEvt|w|h
```
- `layer`：空字符串=`Default`，否则**全字符百分号编码**的图层名
- `contain`：**空字符串=无内容**；`1..999`=金币数；`1001..`=NPC id (=1000+npcid)
- 真实关卡形如：`B||457|x|y||0|0||32|32`

### Warp `W` 字段

`type`：0=instant, 1=pipe, 2=door；`enterd/exitd`：1=up, 2=left, 3=down, 4=right。

> ⚠ **重要**：W 行只创建**不可见的传送判定区**——玩家看不到它！
> 必须**单独放门 BGO** 标识传送点，否则玩家会一脸懵不知道为什么这格地面会突然把人送走。
> 具体做法见下方 **"传送门视觉"** 小节。

### 传送门视觉（W 行 + BGO 配合）

W 行 `type_=2`（door）只是**逻辑触发**，没有任何贴图。要让玩家辨认出传送点，
必须额外放一个**门 BGO**：

```
T||92|<warp_x>|<warp_y - 32>          ' 门 BGO 锚点在玩家踩位上方 32px
```

- 门是 **32×64**（一格宽、两格高），BGO 锚点是左上角，所以放在 `(warp_x, warp_y - 32)`
  让门视觉自然立在玩家身后。
- 入口和出口**两端都要放**（玩家传送过去后也得看到自己刚从哪个门进来）。
- 基于 60 个真实关卡统计，门 BGO 最常用 id（按频次）：
  | id | 说明 |
  | --- | --- |
  | **92** | 默认门（最常用，约占 20%） |
  | 79 | 装饰门 / 城堡门 |
  | 87 | 圆拱门 |
  | 158 | 木门 |
  | 168 | 经典门上半（配 169 用作完整组合） |

**LVLBuilder API（已封装）**：
```python
# 默认会在入口和出口都自动放 BGO 92 门
b.add_warp(x=100, y=-200, ex=300, ey=-100, type_=2)

# 想用其他门 BGO（如装饰风格关卡）
b.add_warp(x=100, y=-200, ex=300, ey=-100, type_=2,
           visual_bgo_id=79)

# 只在入口放门，不在出口放（出口已经有自定义装饰）
b.add_warp(..., visual_at_exit=False)

# 完全自己处理视觉
b.add_warp(..., with_visual=False)
b.add_door_visual(x=100, y=-200, bgo_id=92)   # 等价工具
```

`type_=1`（管道）**不**自动放视觉——管道通常是用 4 个 32×32 方块拼成。
`type_=0`（instant）一般是隐形传送，不需要视觉提示。

`lvl_validate.py` 的 **L022** 会对缺门视觉的 door warp 给 warning。



### Event `E` 字段（按 `|` 顺序）

| 子字段 | 内容 | 格式细则 |
| --- | --- | --- |
| `ea` | 自动启动 | `<autostart>,<condition>` 例 `0,` 或 `1,` |
| `el` | 图层显隐 | `<b>/<show_csv>/<hide_csv>/<toggle_csv>` (**4 段**), 默认 `0///`，多图层用逗号分隔，每个图层名百分号编码 |
| `elm` | 图层运动 | `elm1/elm2/...`，每段 `layername,hExpr,vExpr,way` |
| `epy` | 玩家控制 | 12 个 flag 用逗号分隔，默认 `0,0,0,0,0,0,0,0,0,0,0,0` |
| `eps` | section/bg/music | `esection/ebackground/emusic`，默认 `//` |
| `eef` | 效果 | `sound/endgame/...`，默认 `0/0` |
| `ecn` | 生成 NPC | `cn1/cn2/...`，每段 `id,x,y,sx,sy,sp` |
| `evc` | 修改变量 | `vc1/...`，每段 `name,newvalue` |
| `ene` | 触发器/计时器/API/脚本 | **见下** |

#### `ene` 字段精确格式

```
无任何后置动作:    ',0/0,0,0,0,0'           (只 2 段，nextevent/timer)
仅有 nextevent:   '<name>,<delay>/0,0,0,0,0'
绑定脚本:         ',0/0,0,0,0,0/0/<scriptname>'   (4 段，apievent="0" 不能空！)
api+script:       ',0/0,0,0,0,0/<api>/<script>'
```

> **⚠️** 第 3 段 apievent **绝不能写空字符串**——引擎对空串做 `CInt("")` 会触发 type mismatch。
> 不需要 api 时统一写 `0`。

### 脚本 `S`/`Su`/`SU`

```
S|<urlencoded_name>|<base64_of_script_body>
Su|<urlencoded_name>|<base64_of_script_body>
SU|<urlencoded_name>|<base64_of_gbk_script_body>[|<base64_of_meta>]
```

> 注意：
> - **实际工作版必须用大写 `SU`**（参见踩坑表项 17）。
> - body 必须用 **GBK 字节** 做 base64（项 18）。
> - **第 3 段是可选 GUI 元数据**（项 22）；写不写引擎都接受。`LVLBuilder.add_script()` 默认只写 2 段，由 GUI editor 重新保存时会追加第 3 段。

### 用户数组 `R`

```
R|<urlencoded_arr1>|<urlencoded_arr2>|...
```

- 一行声明所有数组；每段一个数组名（强制百分号编码）。
- 名字规约同变量：字母开头、仅字母数字、不含下划线。
- 数组**长度**不写在 R 行里——由脚本运行时 `call redim(0, arrName, length)` 决定。
- 真实关卡示例：`R|%65%63%68%6F%58|%65%63%68%6F%59` = `R|echoX|echoY`。
- **绝不要**用 `V|name|0|1` 假装数组——引擎会报 `undeclared variable`。
- 写法：`LVLBuilder.add_array('echoX', 'echoY')`。
- 脚本里使用：

```teascript
call redim(0, echoX, 90)
array(echoX(0)) = char(1).x      ' 写入
oldX = array(echoX(idx))         ' 读取
```

### NPC 类绑定脚本（关卡同名目录 + `npc-<id>.txt`）

除了"事件 → 脚本"路径外，38A 还有一条**独立的脚本绑定机制**：

```
<level_filename>.lvl              ← 关卡文件
<level_filename>/                 ← 与关卡同名的目录（无扩展名）
    npc-<id>.txt                  ← 该 type NPC 的配置文件 (INI 键值对)
    block-<id>.txt                ← 该 type Block 的配置文件
    ... (其它 NPC/Block 类配置)
```

`npc-<id>.txt` 里可以写：

```ini
gfxwidth=26
gfxheight=46
scripts=FireBall            ; 关键：把 type=<id> 的所有实例 (含 NCreate 出的)
                            ; 都绑上脚本 FireBall (每帧每实例执行)
```

**调用语义**：
- 该 type 的**每个**实例（包括关卡里静态放的 N 行 + 运行时 `NCreate` 出来的）每帧都会自动执行 `scripts=` 指定的脚本一次。
- **不是**"隐式 with"——脚本里没有默认对象。要访问自身必须先取索引：
  ```teascript
  dim selfIdx as integer
  selfIdx = sysval(param1)        ' NextFrame NPC 事件: param1 = 当前 NPC 的 ID
  with NPC(selfIdx)
      .x = .x + 1                 ' 这里才能用 leading-dot
  end with
  ```
- 显式访问其他对象用 `char(1).x`、`NPC(idx).id`、`Block(i).x` 等。
- 这个脚本本体仍写在 lvl 的 `SU|<name>|<base64>` 行；npc-N.txt 的 `scripts=<name>` 只是引用名字。
- **绝不要写 `do ... loop`** —— 引擎已经替你处理了"每帧调用一次"，脚本本体应该是**单帧瞬时逻辑**（线性的一段 if/赋值/call/with）；写循环 + sleep 会让该实例每帧无限等待。

**对比"每帧驱动"的两条路径**：

| 路径 | 文件 | 适用场景 | 自身引用 |
|---|---|---|---|
| **关卡级 do/sleep/loop** | E 行 autostart=1 → 调用 SU 脚本，脚本里写 `do ... call sleep(1) ... loop` | 整关一个 AI 主控、HUD 刷新 | 无"自身"概念，需 `NPC(idx)` / `char(1)` 显式访问 |
| **NPC 类绑定** | `<lvl>/npc-<id>.txt` 的 `scripts=` | 每个该 type NPC 实例独立行为（弹幕、敌人 AI、互动） | `sysval(param1)` = 当前实例索引；用 `with NPC(idx) ... end with` 进入 |

**示例 — 火球碰玩家扣血**（FireBall.tea）：

```teascript
' 类绑定到 NPC 13；引擎每帧每实例调一次本脚本
' alive 字段 38A 中 NPC 与 Char 语义相反, 见下方"alive 字段坑"小节。
' 玩家受伤推荐用 SpEvent，避免依赖反直觉的 char.alive=1。

dim selfIdx as integer
dim px as double, py as double
dim dx as double, dy as double

selfIdx = sysval(param1)   ' 必须显式取自身索引
px = char(1).x
py = char(1).y

with NPC(selfIdx)
    ' AABB 重叠检测（with 块内可用 leading-dot）
    dx = abs((px + 16) - (.x + 8))
    dy = abs((py + 30) - (.y + 8))

    if dx < 24 then
        if dy < 38 then
            if char(1).invtime <= 0 then
                ' SpEvent(1) = Hurts the player；引擎自动:
                '   - 大马里奥 → 降级 + 100 帧无敌
                '   - 小马里奥 → 死亡
                '   - 火/狸/海/熊 → 各自正确转换
                ' 比手动 status -= 1 / alive = 1 都稳。
                call SpEvent(1)
            end if
            .alive = 0                    ' NPC 销毁: NPC.alive = 0 = 死
        end if
    end if
end with
' ⚠ 不要写 do/loop！每帧已被自动调用
```

> **alive 字段坑**（38A 中 NPC 与 Char 语义相反！）：
> - **NPC.alive**: `0 = 死`，非 0 = 活（与英文字面/常识一致）— 销毁 NPC 用 `.alive = 0`
> - **Char.alive**: 文档原文 "Forcing this value to 1 will kill the player"——**1 = 死**（反直觉！）
> 
> 因为这两条规则相反容易记错，**玩家伤害/死亡推荐用 `call SpEvent(<id>)`**：
> | id | 含义 |
> |---|---|
> | 1 | Hurts the player（引擎处理降级 + 无敌 + 形态转换） |
> | 2 | Kills the player（直接杀死） |
> | 3 | Hide HUD |
> | 4 | Show HUD |
> | 7..10 | 给 mushroom / fire flower / leaf / tanooki 到地图道具栏 |
> 
> 杀 NPC 不要用 SpEvent；NPC 直接 `NPC(idx).alive = 0`（或 `.alive = 0` 在 with 块内）即可。

绑定（同关卡目录下）：

```ini
; AI-Example/EchoChamber/npc-13.txt
scripts=FireBall
```

**LVLBuilder API 支持**（一行搞定）：

```python
b.add_npc_class_script(npc_id=13, script_name='FireBall',
                       script_body=open('FireBall.tea').read(),
                       gfxwidth=26, gfxheight=46)
# 等价于：
#   b.add_script('FireBall', open('FireBall.tea').read())
#   写 <lvl>/npc-13.txt 内容 "scripts=FireBall\ngfxwidth=26\ngfxheight=46"
# save() 时会一并保存到 <lvl 同名目录>/npc-13.txt
```

**其他 NPC 事件**（同样用 `sysval(param1)` 取当前 NPC 索引）：

| `npc-<id>.txt` 字段 | NPC 字段（脚本里设） | 触发时机 | param1 | param2 |
|---|---|---|---|---|
| `scripts=<name>` | `nextframeevent` | **每帧每实例** | 当前 NPC 的 ID | 0 |
| - | `touchevent` | 玩家碰到 NPC（每帧持续） | 当前 NPC 的 ID | 玩家 ID（碰撞方向见 sysval doc） |
| - | `deathevent` | NPC 死亡 | 当前 NPC 的 ID | 击杀者玩家 ID |
| - | `activeevent` | NPC 首次出屏激活 | 当前 NPC 的 ID | 0 |
| - | `talkevent` | 玩家与 NPC 对话 | 当前 NPC 的 ID | 玩家 ID |
| - | `grabedevent` | 玩家拿起 NPC | 当前 NPC 的 ID | 玩家 ID |







## WLD marker

| marker | 含义 |
| --- | --- |
| `ws1` | World 头部设置 |
| `ws2` | Credits |
| `ws3` | 附加字符串列表 |
| `ws4` | Save locker |
| `T` | Terrain tile |
| `S` | Scenery |
| `P` | Path |
| `M` | Area |
| `L` | Level entry |
| `WL` | World layer |
| `WE` | World event |

## WLS marker

| marker | 含义 |
| --- | --- |
| `G` | 全局变量 |
| `GS` | 全局脚本（UTF-8） |
| `GSu` | 全局脚本（ASCII） |
| `CW` | 自定义音效条目 |

## 字段编码规则

### 38A 风格的 URL 编码（强制百分号）

**不是** RFC 3986！38A 的 URL 编码**对所有字符都做 `%xx` 处理**，包括字母数字。

```python
# 错误（urllib 标准实现）：
urllib.parse.quote('Default', safe='')  → 'Default'   ❌

# 正确（38A 实际格式）：
def url_encode_38a(s):
    return ''.join(f'%{b:02X}' for ch in s for b in ch.encode('utf-8'))
url_encode_38a('Default')  → '%44%65%66%61%75%6C%74'   ✅
```

`scripts/lvlfile.py` 的 `url_encode_38a()` 函数已实现该规则，AI 直接调用即可。

### Base64 编码

`base64.b64encode/b64decode`，对脚本 body 做处理。

## 编辑安全清单

1. 文件首行不动。
2. 行尾换行符与原文件一致（项目内多 `CRLF`）。
3. 字符串字段一律用 `url_encode_38a` 处理后再写入。
4. 编辑脚本：先 `lvl_scripts extract` → 改 → `lvl_scripts inject`，**永远不要手写 `S|...|<base64>` 行**。
5. 字段数量必须等于规范要求的最小集（不能多不能少，不能改顺序）。
6. **新建关卡禁止手写 lvl 文本**：用 `scripts/lvlfile.py` API 或 `lvl_edit.py` CLI，由库统一处理编码与字段顺序。
7. 改动后 `lvl_validate.py` 必跑：检测踩坑项 1-11。
8. 改动后用 `lvl_parse` round-trip 校验。
