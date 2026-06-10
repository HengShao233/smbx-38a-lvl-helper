# 动画接口契约（Animation Contract）

一段动画 = **一个 `.tea` 脚本** + **4 个 `Export Script` 接口**。外部（用户的主循环 / 事件）只通过这 4 个接口使用动画，**不关心内部细节**。

## 1. 四个接口

### `{Name}_Launch(BmpIdOffset As Long, Return Integer)`
- 职责：申请本动画所需的 bmp 资源，并**记录 `BmpIdOffset`** 到头部状态变量。
- 所有 bmp id 一律以 `BmpIdOffset + k` 形式分配（`k` 为本动画内的相对槽位）。
- 应是**幂等**的：若已初始化（`inited <> 0`）则直接返回，避免重复 `BmpNew`（重复申请同 id 会被引擎静默忽略，但仍应短路）。
- 返回值约定：成功返回 `0`（返回值语义可由动画自定，但类型必须 `Integer`）。

### `{Name}_Tick(TimeStamp As Long, Return Integer)`
- 职责：根据 `TimeStamp`（单位：**帧**）计算并施加这一刻所有 bmp 的变换。
- **自动初始化**：进入时若 `inited = 0`，必须先 `Call {Name}_Launch(0)`（即未显式 Launch 时，以 offset 0 自动 Launch）。
- **clamp 规则**：
  - `TimeStamp < 0` → 视作 `0`（停在起始姿态）。
  - `TimeStamp > _Length` → clamp 到 `_Length`（**暂停在结尾**，**绝不**在此调用 `_Finish`）。
- **必须尽量 pure**：同一 `TimeStamp` 多次调用应得到尽量一致的画面（除粒子/随机 spawn 等显式例外）。
- **不得自驱动逐帧**：内部**不得 `call sleep`**（sleep = 自驱动逐帧，违背设计）。`do/loop`、`for/next` **允许**，可用于批量建 bmp / 遍历，但必须有限（带 `exit do` / `loop until/while` 或用 `for`），不得死循环。

### `{Name}_Finish(Return Integer)`
- 职责：释放 `_Launch` / `_Tick` 期间申请的**全部** bmp，并把 `inited` 复位为 0。
- 由外部在动画用毕后显式调用；clamp 到结尾的暂停态**不**自动触发它。

### `{Name}_Length(Return Long)`
- 职责：返回动画总长（帧）。通常直接返回头部「调参区」里的 `len` 变量。

## 2. 调用时序（外部驱动方视角）

```teascript
' —— 外部主循环（由用户编写，挂在 autostart=1 事件上）——
dim t as long = 0
call MyAnim_Launch(100)          ' 显式申请, bmp 占用 100+k；也可省略, 由首个 _Tick 自动 Launch(0)
do
    call MyAnim_Tick(t)          ' 每帧驱动
    if t > MyAnim_Length() then  ' 播完
        exit do
    end if
    t = t + 1
    call sleep(1)                ' ⚠ sleep 在“驱动方”，动画脚本内部绝不出现
loop
call MyAnim_Finish()             ' 释放资源
```

> 注意：上面**带 `sleep` 的每帧主循环**属于**驱动方**（用户的主循环），**绝不在动画脚本里**。动画脚本只实现 4 个纯函数式接口；其内部即便用 `do/loop`（如批量建 bmp）也**不得 `call sleep`**。

## 3. bmp 分配规范

- 在头部用 `Dim {Name}_bmpCnt As Long = N` 声明本动画占用的 bmp 数量。
- 在头部维护一张「bmp 分配表」注释，例如：
  ```teascript
  ' bmp 分配 (相对 BmpIdOffset):
  '   +0 : 飞碟本体  npc-2(3984,0,8,8) 4 帧序列
  '   +1 : 背景白片  npc-1(768,256,1,1)
  ```
- `_Finish` 中若槽位连续，可循环释放：
  ```teascript
  For temp_i = 0 To {Name}_bmpCnt - 1 Step 1
      Call BmpDel({Name}_offset + temp_i)
  Next
  ```
  若槽位不连续，请逐个 `BmpDel` 明确释放。

## 4. 中途按需申请（兼容跳帧）

某些 bmp 不在开场出现，而在动画中段才需要。**正确做法**是用区间判定 + 标志位，而非等值判定：

```teascript
' ✅ 兼容跳帧：只要进入区间且尚未申请, 就申请
If TimeStamp >= 120 And TimeStamp < {Name}_len And {Name}_phase2Inited = 0 Then
    Call BmpNewStoreSrc(...)
    Call BmpNew({Name}_offset + 5)
    {Name}_phase2Inited = 1
End If

' ❌ 错误：等值判定, 跳帧时会漏掉
' If TimeStamp = 120 Then ...
```

无论在哪里申请，`_Finish` 都要负责释放。申请出来的 bmp **可复用**：改 `npc id` 和截取区域即可，不必删了重建。

## 5. 头部状态变量约定（命名建议）

| 变量 | 类型 | 用途 |
| --- | --- | --- |
| `{Name}_len` | `Long` | 动画总长（帧），调参区 |
| `{Name}_bmpCnt` | `Long` | 占用 bmp 数量 |
| `{Name}_offset` | `Long` | 缓存 `BmpIdOffset` |
| `{Name}_inited` | `Long` | 0 未初始化 / 1 已初始化 |
| `temp_*` | 任意 | 临时计算变量，统一头部 dim |

> 每个动画脚本拥有独立的 dim 命名空间，故不同动画间的 `temp_*` 不会互相影响；但同一脚本内 `temp_*` 是跨调用持久的，使用前别假设其初值。
