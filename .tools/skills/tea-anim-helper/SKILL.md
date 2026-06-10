---
name: tea-anim-helper
description: SMBX 38A 中基于 bmp/bitmap 的「tick 驱动型」TeaScript 动画的设计与实现助手。当用户用自然语言或需求模板（如 `bmp-2&npc-1(0,0,128,128): 缩放覆盖全屏, 0~1s 透明度 0->1`）描述一段过场/演出/特效动画，需要 AI 产出或修改**单个** `.tea` 动画脚本（暴露 `_Launch/_Tick/_Finish/_Length` 四个接口、复用 bmp_utils & cumath_utils 工具函数集）时使用。
license: project-internal
---

# TeaScript 动画助手 Skill（tea-anim-helper）

为 AI 提供一套把**用户自然语言 / 需求模板**转化为**单个 tick 驱动型 TeaScript 动画脚本**的完整、**自包含**的工作流：从需求收敛、骨架生成、变换实现，到静态校验，全部在本 skill 内闭环。

> 范围：本 skill 只负责**生成 / 修改单个动画 `.tea` 脚本**本身（产物可在关卡中按帧驱动播放）。把脚本嵌入关卡文件、绑定事件、启动引擎跑回归等，属于关卡侧流程，不在本 skill 范围内。

## 何时使用

只要任务涉及以下任何一项，**优先**使用本 skill：

- 用户描述一段**过场动画 / 演出 / 特效**（飞入、缩放、淡入淡出、沿曲线运动、帧动画播放、抖动、旋转、颜色渐变、拖尾 / 粒子……），希望生成可在关卡里播放的脚本。
- 用户给出**需求模板**（形如 `bmp-<id>&npc-<srcId>(x,y,w,h): <时间>内<变化>`），需要落地为动画脚本。
- 修改 / 微调一段已有的 `_Tick` 动画（改时长、改缓动、改轨迹、加分镜……）。
- 需要把多个 bmp 组织成一段随时间变化的演出。

## 运行环境约定（屏幕 / fps）

- 屏幕视口恒定 **800x600**，原点左上角；居中坐标 `(400, 300)`。
- 帧率恒定 **64 fps**，故 `1s = 64 帧`，`timestamp` 单位即**帧**。
- 资产称 npc（`npc-1` = id 为 1 的资产），运行时实例化为 bmp；同一资产可被多个 bmp-id 实例化；对已占用的 bmp-id 再 `BmpNew` 会被静默忽略。

## 核心理念（务必牢记）

1. **tick 驱动，不得自驱动逐帧**：动画脚本**内部禁止 `call sleep`**（一旦 sleep 即变成自驱动的逐帧循环，违背设计）。驱动由外部（用户写的主循环或事件）按帧调用 `_Tick(timestamp)` 完成。
   - `do ... loop` / `for ... next` **是允许的**，常用于**批量创建 / 遍历 bmp**（如一次铺很多粒子）；但因为内部不能 `sleep` 退让，循环必须**有限**（带 `exit do` / `loop until` / `loop while`，或用 `for`），切勿写无退出的死循环，否则会冻结游戏。
2. **尽量 pure**：相同 `timestamp` 应尽量产生相同输出，不依赖外部状态 / 事件。允许少量例外（粒子、随机 spawn），但应使用 `CUMath_Hash(seed)` 这类**可复现伪随机**而非 `rnd`。
3. **单脚本交付**：一段动画只产出**一个** `.tea`，内部可拆多个 `Script` 子过程，但对外只暴露 4 个 `Export Script` 接口。
4. **复用工具函数集**：几乎所有变换都走 `bmp_utils`（BmpNew / BmpScale / BmpRotate / BmpAlpha / BmpAnim…）与 `cumath_utils`（CUTimeCalcT / CUEase_* / CUCalcBezier* / CUMath_*）。AI 不重复造轮子，只需告知用户导入哪些库（`reference/common-utils/` 内附完整源码以备查阅）。
5. **给人留微调空间**：所有可调参数集中在脚本头部「调参区」，注释完备，方便人眼后续微调。

## 对外接口契约（必须严格实现，签名一字不差）

```teascript
' 初始化：申请 bmp 资源，记录 BmpIdOffset。本动画占用的 bmp id 一律相对 BmpIdOffset 分配
Export Script {Name}_Launch(BmpIdOffset As Long, Return Integer)

' 驱动：按帧传入时间戳（帧数）
'   timestamp <= 0 且未 Launch 过  -> 自动 Launch(0)
'   timestamp > _Length           -> 内部 clamp 到 _Length（暂停在结尾，不触发 _Finish）
Export Script {Name}_Tick(TimeStamp As Double, Return Integer)

' 结束：释放本动画申请的所有 bmp 资源
Export Script {Name}_Finish(Return Integer)

' 长度：返回动画总长（帧）
Export Script {Name}_Length(Return Double)
```

完整语义见 [`reference/animation-contract.md`](reference/animation-contract.md)。

## 目录结构

```
.tools/skills/tea-anim-helper/
├── SKILL.md                          # 本文件（入口）
├── README.md                         # 概览与快速上手
├── reference/
│   ├── requirement-template.md       # ⭐ 用户需求模板规范 + 如何引导用户补全
│   ├── animation-contract.md         # ⭐ 4 接口契约 + BmpIdOffset / tick / clamp 语义
│   ├── common-utils-cookbook.md      # bmp_utils & cumath_utils 动画向 API 速查 + 配方
│   ├── authoring-conventions.md      # 头部 dim / temp_ 前缀 / 调参区 / 注释 / 分镜规约
│   └── common-utils/                 # ⭐ 工具函数集完整源码副本（自包含，备查）
│       ├── bmp_utils.smt
│       └── cumath_utils.smt
├── templates/
│   └── animation.tea                 # ⭐ 标准动画骨架（4 接口 + 注释，直接复制改）
├── examples/
│   └── starfield.tea                 # ⭐ 自包含范例：do-loop 批量建 bmp + tick 演出
└── scripts/
    ├── anim_lint.py                  # ⭐ 动画专用静态校验（接口齐全 / 签名 / 禁 sleep / 申请释放配对）
    └── anim_scaffold.py              # 从需求模板 DSL 一键生成 animation.tea 骨架
```

## 推荐工作流（SOP）

> 📁 **中间产物一律放 `.cache/`**：本 skill 生成 / 编辑过程中的所有临时与中间 `.tea`（骨架、草稿、调试副本、校验输出等）都应输出到工作区或就近目录下的 `.cache/` 目录（gitignore 规则 `**/.cache/` 即可整体排除），**不要**散落到关卡目录或仓库根、也不要提交到版本库。只有最终需要交付/嵌入关卡的成品 `.tea` 才移出 `.cache/`。下文命令统一以 `.cache/<name>.tea` 为输出路径示范。

**0. 确认需求（最重要）**
对照 [`reference/requirement-template.md`](reference/requirement-template.md)，确保用户至少说清：
- 每个 bmp 选用哪个 npc 资产、截取区域 `(x,y,w,h)`、是否帧动画图集（帧数 / 排布）；
- 面向时间的**生成**（何时出现）与**变化**（位置 / 缩放 / 旋转 / 透明 / 颜色 / 帧）；
- 动画总时长。

信息不足时，先给出模板请用户补全再开工；或对缺项作合理假设并**明确标注**，继续推进。

**1. 生成骨架**（可选，自动）
```bash
python .tools/skills/tea-anim-helper/scripts/anim_scaffold.py \
  --name MyAnim --length 60 \
  --bmp "0=npc-1(0,0,128,128)" \
  -o .cache/MyAnim.tea
```
或直接复制 `templates/animation.tea` 手工改；批量 bmp 演出可参考 `examples/starfield.tea`。

**2. 实现 `_Tick` 逻辑**
- 头部「调参区」写死时长 / 关键参数；用 `read_file` / `replace_in_file` 编辑。
- 时间归一：`Call CUTimeSetStamp(0, len)` + `t = CUTimeCalcT(timestamp)`。
- 变化：缓动 `CUEase_*`、轨迹 `CUSetP0..3 + CUCalcBezier3*`、帧动画 `BmpStoreAnim* + BmpAnim`、透明 `BmpAlpha`、颜色 `BmpStoreCol1/2 + BmpColLerp`。配方与 API 速查见 [`reference/common-utils-cookbook.md`](reference/common-utils-cookbook.md)，完整签名见 [`reference/common-utils/`](reference/common-utils/) 源码副本。

**3. 静态校验（⭐ 无引擎也能做，必跑）**
```bash
python .tools/skills/tea-anim-helper/scripts/anim_lint.py .cache/MyAnim.tea
```
`anim_lint.py` 0 errors 后再交付。它覆盖：4 接口齐全与签名、禁 `call sleep`（自驱动）、bmp 申请/释放配对、`rnd` 禁用、内部 `dim`、可执行语句行尾注释、`_Tick` 时间归一化等。

> 关于命名：本项目约定（来自需求文档与实践）在 `Dim` 名里使用下划线（`temp_` 前缀、`MyAnim_len`），**这在引擎中是合法的**。「禁止下划线」只针对**用户变量 `v(...)` / 关卡 V 行名**，与动画脚本里的 `Dim` 无关。

## 行动准则（给 AI 的硬约束）

1. **签名一字不差**：4 个 `Export Script` 名为 `{Name}_Launch / _Tick / _Finish / _Length`，参数与返回类型严格如契约。`anim_lint.py` 会校验。
2. **不得自驱动**：动画脚本里**不得出现** `call sleep`。`do/loop`、`for/next` 允许（用于批量建 bmp / 遍历），但必须有限、不得死循环。
3. **bmp 申请与释放配对**：`_Launch` 里 `BmpNew` 的，`_Finish` 里必须 `BmpDel`。中途按需申请的也要在 `_Finish` 释放。中途申请用「区间判定 + 未申请才申请」（`timestamp >= a And timestamp < b`），**不要**写 `timestamp == a`，以兼容跳帧。
4. **bmp id 一律相对 `BmpIdOffset`**：禁止硬编码绝对 bmp id；用 `offset + k`，避免多动画并存时 id 撞车。
5. **变量在脚本头部 dim**：受 38A 引擎缺陷影响，**不在子过程内部 dim**。临时变量用 `temp_` 前缀集中在头部；调参参数紧跟头部注释之后。详见 [`reference/authoring-conventions.md`](reference/authoring-conventions.md)。
6. **优先复用工具函数集**：不要自己实现缓动 / 贝塞尔 / 三角；调 `cumath_utils`。bmp 变换调 `bmp_utils`。需要哪些库，明确告诉用户在关卡早期 `call exeScript(Lib_Bmp)` / `call exeScript(Lib_Curver)` 导入。
7. **可复现随机**：需要随机时用 `CUMath_Hash(seed)`，禁用 `rnd`，保证 pure。
8. **注释完备、留微调空间**：头部写清创作意图 / 效果 / bmp 分配表；关键参数注释；阶段（分镜）用注释分隔。
9. **TeaScript 语法红线**（详见 `reference/authoring-conventions.md` 第 6 节）：注释用 `'`；`next` 后不跟变量名；**可执行语句后不要跟行尾注释**；不除以 0；`Script` 子过程定义放文件末尾区域、主体（dim + Export Script）在前。
10. **改完必跑** `anim_lint.py` 再汇报。
11. **中间产物放 `.cache/`**：骨架/草稿/调试副本/校验输出等一切中间 `.tea` 输出到 `.cache/`（由 `**/.cache/` gitignore 排除），不提交版本库；仅最终成品移出。
