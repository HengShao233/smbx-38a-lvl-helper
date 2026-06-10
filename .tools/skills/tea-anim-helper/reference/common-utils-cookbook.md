# common-utils 动画向速查 + 配方

> 工具函数集完整源码副本随本 skill 提供：[`./common-utils/bmp_utils.smt`](./common-utils/bmp_utils.smt)（Lib_Bmp）、[`./common-utils/cumath_utils.smt`](./common-utils/cumath_utils.smt)（Lib_Curver）。
> 使用前需由用户在关卡早期 `call exeScript(Lib_Bmp)` / `call exeScript(Lib_Curver)` 导入。本文档只列动画高频 API；需要完整签名请查上述源码副本。

约定：所有角度为**弧度**；颜色分量 `0~255`；alpha 入参 `0~1`；缩放为倍数；屏幕 `800x600`。

---

## A. bmp_utils（bitmap 操作）

### A.1 创建（先 Store 再 New）
`BmpNew*` 采用「先暂存参数，再创建」的两段式：

```teascript
Call BmpNewStoreIsUseScreenCoords(1)        ' 1=屏幕坐标(过场常用) 0=世界坐标
Call BmpNewStorePos(-10000, -10000)         ' 初始放到屏外, 等 _Tick 再摆位
Call BmpNewStoreScale(1, 1)                 ' 初始缩放
Call BmpNewStoreSrc(srcId, sx, sy, sw, sh)  ' 资产id + 截取(x,y,w,h)
Call BmpNew(id)                             ' 真正创建; id 已占用则静默忽略
Bitmap(id).zpos = 0.001                     ' z 序, 越小越靠前(可微调遮挡)
```

- `BmpNewStoreSrcId(srcId)` / `BmpNewStoreSrcOffset(x,y,w,h)` 可分别设置。
- 销毁：`Call BmpDel(id)`。

### A.2 位置 / 缩放 / 旋转（支持锚点）
先设锚点（相对，0~1，`0.5,0.5` 为中心），后续变换都绕锚点：

```teascript
Call BmpStoreAnchor(0.5, 0.5)
Call BmpPos(id, 400, 300)         ' 设位置(锚点对齐到该点)
Call BmpScale(id, sx, sy)         ' 设缩放
Call BmpRotate(id, angle)         ' 设旋转(弧度)
```

读取：`Call BmpGetPos(id)` 后 `BmpGetRetX()/BmpGetRetY()`；`Call BmpGetScale(id)` 后 `BmpGetRetX()/Y()`；`BmpGetRotate(id)`。
也可直接读写底层字段：`Bitmap(id).destx/.desty/.scalex/.scaley/.rotatang/.scrx/.scry/.scrwidth/.scrheight/.zpos/.forecolor/.forecolor_a`。

> ⚠ 用了非零锚点后，**务必通过 `BmpPos/BmpScale/BmpRotate` 修改**，它们内部做了锚点补偿；直接写 `.destx` 会绕过补偿导致位移。

### A.3 透明度 / 颜色
```teascript
Call BmpAlpha(id, a)                         ' a: 0~1
Call BmpCol(id, r, g, b, a)                  ' 直接设色 (a:0~255)
' 双色插值(渐变):
Call BmpStoreCol1(178, 50, 50, 255)
Call BmpStoreCol2(126, 87, 246, 255)
Call BmpColLerp(id, t)                        ' t:0~1 在两色间插值并应用
```

### A.4 帧动画（序列帧图集）
```teascript
Call BmpStoreAnimPos(startX, startY, frameW, frameH)  ' 图集起点 + 单帧宽高
Call BmpStoreAnimInfo(frameCnt, colsPerRow)           ' 总帧数 + 每行帧数
Call BmpStoreAnimInterval(ix, iy)                     ' 帧间像素间隔(无则 0,0)
Call BmpStoreAnimLoop(loopFrames)                     ' 尾循环帧数; <=0 整体循环
Call BmpAnim(id, frameTimeStamp)                      ' 应用第 frameTimeStamp 帧(可>总帧/为负)
```
帧推进：`frameTimeStamp = fps/60 * timestamp`（如 12fps → `0.2 * timestamp`）。

### A.5 偏移动画（UV 滚动）
```teascript
Call BmpStoreOffsetAnimInfo(x0, y0, x1, y1)
Call BmpOffsetAnim(id, t)        ' t 取小数部分, 在 (x0,y0)->(x1,y1) 间滚动采样原点
```

---

## B. cumath_utils（时间 / 缓动 / 曲线 / 数学）

### B.1 时间归一化（动画时间轴核心）
```teascript
Call CUTimeSetStamp(0, len)          ' 设定 [start,end] 帧区间
t = CUTimeCalcT(timestamp)           ' -> [0,1], 自动 clamp
```
分段（多控制点轨迹）：
```teascript
Call CUTimeSetSplit(4)               ' 把 [0,1] 切 4 段
idx = CUTimeCalcSplitIdx(t)          ' 当前第几段
st  = CUTimeCalcSplitT(t)            ' 段内局部 t -> [0,1]
```

### B.2 缓动 Ease（输入输出均 0~1，可串联）
`CUEase_InSine/OutSine/InOutSine`、`InQuad/OutQuad/InOutQuad`、`InCubic/OutCubic/InOutCubic`、`InQuart/OutQuart/InOutQuart`、`InExpo/OutExpo/InOutExpo`、`InCirc/OutCirc/InOutCirc`。
```teascript
t = CUEase_OutCubic(CUTimeCalcT(timestamp))     ' 先归一再缓动
```

### B.3 插值 / 钳制 / 重映射
```teascript
v = CUMath_Lerp(a, b, t)             ' 线性插值
v = CUMath_SinLerp(a, b, theta)      ' 正弦插值
v = CUMath_Clamp01(x)                ' 钳到 [0,1]
v = CUMath_Clamp(a, b, x)            ' 钳到 [a,b]
v = CUMath_Remap01(f, t, x)          ' 把 [f,t] 映射到 [0,1]
v = CUMath_SmoothClamp(a, b, t)      ' smoothstep
v = CUMath_Frac(x)                   ' 小数部分
v = CUMath_Max(a,b) / CUMath_Min(a,b) / CUMath_Avg(a,b)
```

### B.4 贝塞尔曲线（轨迹运动）
```teascript
Call CUSetP0(x0, y0)                 ' 三阶需 P0..P3
Call CUSetP1(x1, y1)
Call CUSetP2(x2, y2)
Call CUSetP3(x3, y3)
px = CUCalcBezier3X(t)               ' t:0~1 -> 曲线坐标
py = CUCalcBezier3Y(t)
Call BmpPos(id, px, py)
' 二阶: CUCalcBezier2X/Y(需 P0..P2); 一阶: CUCalcBezier1X/Y(需 P0,P1)
' 曲线长度: CUCalcBezier3Len() 等(可用于匀速参数化)
```

### B.5 可复现随机（替代 rnd，保证 pure）
```teascript
r = CUMath_Hash(seed)                ' seed:任意数 -> [0,1) 伪随机, 同 seed 同结果
' 例: 给第 i 个粒子稳定随机相位
phase = CUMath_Hash(i * 137 + 7)
```

### B.6 向量
`CUMath_VecRotate(x,y,ang)` / `VecNormal` / `VecAdd` / `VecSub` / `VecMul` 后用 `CUMath_GetVecRetX()/Y()` 取结果；`VecLength`、`Dot`、`Cross`、`Angle`、`Atan2`。

---

## C. 常见配方（直接抄改）

> 以下片段假设头部已有 `{Name}_offset`、`temp_t`、`temp_s` 等，且 `id = {Name}_offset + k`。

### C.1 淡入（0~len 内 alpha 0→1）
```teascript
Call CUTimeSetStamp(0, {Name}_len)
temp_t = CUTimeCalcT(TimeStamp)
Call BmpAlpha(id, temp_t)
```

### C.2 缩放至刚好覆盖全屏（截取宽高 sw×sh）
```teascript
Call BmpStoreAnchor(0.5, 0.5)
Call BmpPos(id, 400, 300)
Call BmpScale(id, 800.0 / sw, 600.0 / sh)   ' 覆盖: 取 max 可保持比例并裁切
```

### C.3 缓动飞入（从上方滑入并回弹缓停）
```teascript
temp_t = CUEase_OutCubic(CUTimeCalcT(TimeStamp))
Call BmpStoreAnchor(0.5, 0.5)
Call BmpPos(id, 400, CUMath_Lerp(-100, 300, temp_t))
```

### C.4 沿贝塞尔曲线运动
```teascript
temp_t = CUTimeCalcT(TimeStamp)
Call CUSetP0(400, -50)
Call CUSetP1(600, 150)
Call CUSetP2(200, 450)
Call CUSetP3(400, 300)
Call BmpStoreAnchor(0.5, 0.5)
Call BmpPos(id, CUCalcBezier3X(temp_t), CUCalcBezier3Y(temp_t))
```

### C.5 持续旋转 + 越转越慢
```teascript
temp_t = CUEase_OutQuad(CUTimeCalcT(TimeStamp))
Call BmpStoreAnchor(0.5, 0.5)
Call BmpRotate(id, CUMath_Lerp(pi * 6, 0, temp_t))
```

### C.6 播放序列帧（12fps 循环）
```teascript
Call BmpStoreAnimLoop(0)
Call BmpStoreAnimInterval(0, 0)
Call BmpStoreAnimInfo(4, 2)                  ' 4 帧, 每行 2
Call BmpStoreAnimPos(128, 128, 128, 128)     ' 图集起点 + 单帧 128x128
Call BmpAnim(id, 0.2 * TimeStamp)            ' 12fps => 0.2
```

### C.7 颜色随时间渐变
```teascript
temp_t = CUTimeCalcT(TimeStamp)
Call BmpStoreCol1(255, 255, 255, 255)
Call BmpStoreCol2(255, 0, 0, 255)
Call BmpColLerp(id, temp_t)
```

### C.8 抖动（屏幕/物体 shake，可复现）
```teascript
temp_s = CUMath_Clamp01(1 - CUTimeCalcT(TimeStamp)) * 8   ' 强度随时间衰减
temp_i = CUMath_Lerp(-1, 1, CUMath_Hash(TimeStamp * 3 + 1)) * temp_s
temp_j = CUMath_Lerp(-1, 1, CUMath_Hash(TimeStamp * 3 + 2)) * temp_s
Call BmpStoreAnchor(0.5, 0.5)
Call BmpPos(id, 400 + temp_i, 300 + temp_j)
```

### C.9 批量创建一组 bmp（`_Launch` 内，for 或 do-loop）
动画内**允许** `for/next`、`do/loop` 用于批量建/遍历 bmp（只是不能 `call sleep`）。常见于粒子、星空、网格等。

```teascript
' for 写法（最常用，循环边界清晰）
For temp_i = 0 To {Name}_bmpCnt - 1 Step 1
    Call BmpNewStorePos(-10000, -10000)
    Call BmpNewStoreScale(0, 0)
    Call BmpNewStoreSrc(MySrcId, 0, 0, 16, 16)
    Call BmpNew({Name}_offset + temp_i)
    Bitmap({Name}_offset + temp_i).zpos = 0.05
Next
```

```teascript
' do-loop 写法（须有限：带 exit do 或 loop until/while；切勿无退出死循环）
temp_i = 0
do
    Call BmpNewStoreSrc(MySrcId, 0, 0, 16, 16)
    Call BmpNew({Name}_offset + temp_i)
    temp_i = temp_i + 1
    if temp_i >= {Name}_bmpCnt then exit do    ' ⚠ 必须有退出, 动画内不能 call sleep
loop
```

### C.10 遍历一组 bmp 做每帧更新（`_Tick` 内）
```teascript
For temp_i = 0 To {Name}_bmpCnt - 1 Step 1
    ' 用 hash 给每个粒子稳定的相位/位置, 保证可复现
    temp_a = CUMath_Hash(temp_i * 131 + 7)            ' [0,1)
    temp_b = CUMath_Frac((TimeStamp * 0.01) + temp_a) ' 随时间循环推进
    Call BmpStoreAnchor(0.5, 0.5)
    Call BmpPos({Name}_offset + temp_i, temp_a * 800, temp_b * 600)
    Call BmpAlpha({Name}_offset + temp_i, CUMath_Clamp01(1 - temp_b))
Next
```
