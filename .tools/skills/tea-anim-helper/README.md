# tea-anim-helper

把**动画需求**（自然语言 / 需求模板）转化为**单个 tick 驱动型 TeaScript 动画脚本**的 AI skill。产物对外只暴露 4 个接口：`_Launch` / `_Tick` / `_Finish` / `_Length`，内部复用 bmp_utils & cumath_utils 工具函数集。本 skill **自包含**：工具函数集源码副本、模板、范例、静态校验器均在内，不依赖 skill 外部文件。

完整指引见 [`SKILL.md`](SKILL.md)。

## 一分钟上手

> 📁 中间产物（骨架/草稿/调试副本/校验输出）一律放 `.cache/` 目录，由 gitignore 规则 `**/.cache/` 排除，不提交版本库；仅最终成品移出。

```bash
# 1) 生成骨架 (示例: 全屏遮罩 npc-1 裁剪 128x128, 时长 60 帧)
python .tools/skills/tea-anim-helper/scripts/anim_scaffold.py \
  --name MyAnim --length 60 --bmp "0=npc-1(0,0,128,128)" \
  -o .cache/MyAnim.tea

# 2) 在 _Tick 内补全“面向时间的变化”(缩放/位移/透明/帧...) —— 见 cookbook 配方

# 3) 静态校验 (无需引擎)
python .tools/skills/tea-anim-helper/scripts/anim_lint.py .cache/MyAnim.tea

# 4) 交付 .tea (嵌入关卡 / 引擎测试属关卡侧流程, 不在本 skill 范围)
```

## 设计要点

- **tick 驱动**：动画脚本内**禁止 `call sleep`**（自驱动逐帧）；`do/loop`、`for/next` 允许（批量建 bmp / 遍历），但须有限不死循环。由外部按帧调用 `_Tick(timestamp)`。
- **尽量 pure**：相同 `timestamp` 尽量相同输出；随机用 `CUMath_Hash` 而非 `rnd`。
- **单脚本**：一段动画 = 一个 `.tea`，对外仅 4 个 `Export Script`。
- **bmp 相对偏移**：所有 bmp id = `BmpIdOffset + k`，避免多动画并存撞车。
- **头部 dim + temp_ 前缀 + 调参区**：方便人工微调（38A 不宜在子过程内 dim）。

## 文件

| 路径 | 用途 |
| --- | --- |
| `SKILL.md` | 入口：何时使用 / 契约 / SOP / 硬约束 |
| `reference/requirement-template.md` | 用户需求模板规范 + 引导追问 |
| `reference/animation-contract.md` | 4 接口契约 + BmpIdOffset / tick / clamp 语义 |
| `reference/common-utils-cookbook.md` | bmp_utils & cumath_utils 速查 + 配方 |
| `reference/authoring-conventions.md` | 头部 dim / temp_ / 调参区 / 分镜 / 语法红线 |
| `reference/common-utils/*.smt` | 工具函数集完整源码副本（自包含，备查） |
| `templates/animation.tea` | 标准骨架（直接复制改） |
| `examples/starfield.tea` | 自包含范例：do-loop 批量建 bmp + tick 演出 |
| `scripts/anim_lint.py` | 动画契约静态校验 |
| `scripts/anim_scaffold.py` | 从模板 DSL 生成骨架 |
