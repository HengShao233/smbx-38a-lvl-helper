# 编写规约（Authoring Conventions）

这些规约来自 38A 引擎实践与本 skill 的动画范例，目的是让 AI 产物**稳定、可读、易被人工微调**。

## 1. 变量一律在脚本头部 dim

受 38A 引擎缺陷影响，**在子过程内部 `dim` 局部变量会带来危险和性能问题**。因此：

- **所有变量在脚本头部 `dim`**，子过程内部不再 `dim`。
- 临时计算变量用 **`temp_` 前缀**集中声明，与状态变量区分。
- 调参参数（理论上无其它依赖、供人微调）紧跟头部注释之后声明。

```teascript
' ===================================== 调参区 (供人工微调)
Dim MyAnim_len As Long = 60          ' 总长(帧)
Dim MyAnim_bmpCnt As Long = 1        ' 占用 bmp 数

' ===================================== 内部状态 (勿手改)
Dim MyAnim_offset As Long = 0
Dim MyAnim_inited As Long = 0

' ===================================== 临时变量 (temp_ 前缀)
Dim temp_t As Double = 0
Dim temp_s As Double = 0
Dim temp_i As Long = 0
Dim temp_j As Long = 0
```

> 每个动画脚本有独立 dim 命名空间，故 `temp_*` 不会与别的动画冲突；但同脚本内 `temp_*` 跨调用持久，使用前要自行赋值，别依赖其残留值。

## 2. 文件结构顺序

```
1) 头部块注释（创作意图 / 效果 / 依赖库 / bmp 分配表）
2) Dim 调参区
3) Dim 内部状态
4) Dim 临时变量
5) Export Script _Length
6) Export Script _Launch
7) Export Script _Tick      （可在其中 Call 内部子过程）
8) Export Script _Finish
9) 内部子过程 Script ...（如有，放最后）
```

- 4 个对外接口必须 `Export Script`，签名一字不差。
- 内部可拆分 `Script {Name}_Phase1(...)` 等子过程辅助 `_Tick`，命名以 `{Name}_` 开头避免与其它脚本撞名。

## 3. 头部块注释模板

```teascript
' =============================================================
'  Animation: MyAnim
'  ----------------------------------------------------------
'  创作意图: <一句话>
'  呈现效果: <分阶段描述>
'  对标/风格: <参考 / 风格>
'  依赖: Lib_Bmp (bmp_utils), Lib_Curver (cumath_utils)
'        请在关卡早期 call exeScript(Lib_Bmp) / call exeScript(Lib_Curver)
'  bmp 分配 (相对 BmpIdOffset):
'    +0 : <用途> npc-1(0,0,128,128)
' =============================================================
```

## 4. 分镜（多阶段）写法

把长动画按时间切成阶段，用注释明显分隔，必要时拆子过程。典型做法：在 `_Tick` 里用 `If TimeStamp < t1 ... ElseIf ... Else ...` 把动画切成几大段，每段有自己的 `Init`（按需申请 bmp）与 `Update`（每帧变换）子过程；切段时把局部时间戳归零再传入子过程（如 `Call MyAnim_Phase2(TimeStamp - t1)`）。可参考 `examples/starfield.tea` 的组织方式。

```teascript
' ---- 阶段 1: 飞入 (0 ~ 120) ----
If TimeStamp < 120 Then
    Call MyAnim_Enter(TimeStamp)
' ---- 阶段 2: 停留旋转 (120 ~ len) ----
Else
    Call MyAnim_Idle(TimeStamp - 120)
End If
```

## 5. 数值与可读性

- 时间统一走 `CUTimeCalcT` 归一化，避免散落的魔法帧数；阈值帧数放调参区。
- 缓动 / 曲线 / 插值一律调 `cumath_utils`，不要手写 `t*t*t`。
- 关键调参点写注释说明「调大会怎样 / 调小会怎样」，方便人工试。

## 6. TeaScript 语法红线（动画场景高频）

- 注释用 `'`；**可执行语句后不要跟行尾注释**（会触发引擎假错，注释独占一行）。`Dim` 声明行的行尾注释在实践中可用。
- `For ... Next` 的 `Next` 后**不跟变量名**（裸写 `Next`）。
- `Script` 子过程定义放文件末尾；脚本主体（dim + Export Script）在前。
- 不除以 0 / 不 mod 0。
- **动画脚本内禁止 `call sleep`**（sleep = 自驱动逐帧，违背设计）。`do/loop`、`for/next` **允许**（批量建 bmp / 遍历），但必须有限、不得死循环。
- bmp id 不硬编码绝对值，统一 `offset + k`。
- 需要随机用 `CUMath_Hash`，不用 `rnd`。
- 字符串想写 `"` 用 `chrW(34)`；真假约定 `-1`=真 `0`=假；比较不可跨类型。

## 7. 下划线命名说明（重要）

- **`Dim` 变量名可以含下划线**（引擎支持）。实践中常用 `__bmpId_start`、本规约用 `temp_` 前缀，均正常运行。
- 「禁止下划线」只针对**用户变量 `v(...)` / 关卡 `V` 行名**，与动画脚本里的 `Dim` 无关，不要混淆。
- 静态校验以本 skill 的 `anim_lint.py` 为准（它对下划线 `Dim`、工具函数集调用均不误报）。
