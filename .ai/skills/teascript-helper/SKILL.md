---
name: teascript-helper
description: SMBX 38A 的 TeaScript 脚本开发助手。提供语法速查、代码模板、静态 lint、把 .tea 嵌入 lvl 文件、绑定 Event→Script、运行时一键回归测试（lint + inject + reload + trigger + screenshot）。当用户需要写、读、修改、调试、回归 TeaScript 代码（关卡内嵌脚本 / 全局脚本）时使用。
license: project-internal
---

# TeaScript 开发助手 Skill

为 AI 提供 SMBX 38A 中 **TeaScript** 脚本的全流程开发工作流。它**与 `smbx-38a` skill 互补**：

| 职责 | skill |
| --- | --- |
| 解析/编辑 lvl 文件结构、IPC、引擎控制、截图 | `smbx-38a` |
| **写、查、改、嵌入、测试 TeaScript 代码** | **`teascript-helper`（本 skill）** |

## 何时使用

- 写新的 TeaScript（关卡内 `S`/`Su` 脚本，全局 `GS`/`GSu` 脚本）
- 读懂现有脚本并 refactor
- 检查脚本语法/常见错误（`/`/`mod` 除零、未声明 `dim`、`script` 块缺 `end script` 等）
- 把独立 `.tea` 文件嵌入到 lvl 里，无需打开 SMBX editor
- 创建 / 改写 / 绑定 Event → Script 关联（`E` 行的 `ene` 子字段）
- 一键回归：lint → 嵌入 → 引擎重载 → 触发事件 → 抓状态 + 截图

## 与 `smbx-38a` 的协作

本 skill 直接 **import 自 `smbx-38a` 的 `lvlfile.py` 与 `engine_control.py`**（同一个项目里两个 skill 协同）。
- 文件读写仍走 `lvlfile.SMBXFile`，保证 round-trip 无损。
- 引擎控制委托 `engine_control` CLI（启动 / reload / trigger / state / screenshot / editor 会话）。

## 目录结构

```
.ai/skills/teascript-helper/
├── SKILL.md                       # 入口（本文件）
├── README.md
├── reference/
│   ├── syntax-cheatsheet.md       # TeaScript 语法速查（精炼版）
│   ├── builtin-functions.md       # 内置函数清单（含签名）
│   ├── autorun-events.md          # 自动事件名 + sysval 参数
│   └── snippets.md                # 常用代码片段
├── templates/                     # AI 起手即可复制的模板
│   ├── event_script.tea
│   ├── procedure.tea
│   ├── function.tea
│   ├── iterator_loop.tea
│   └── global_script.tea
├── scripts/
│   ├── teascript_lint.py          # 静态 lint（语法 + 规约 + 引用检查）
│   ├── teascript_format.py        # 规整化格式
│   ├── teascript_inject.py        # 直接把 .tea 嵌入为 lvl 的 S/Su
│   ├── teascript_event.py         # 创建 Event 并绑定 Script
│   ├── teascript_test.py          # 一键回归（lint + inject + 启动/重载 + trigger + screenshot）
│   └── selftest.py
└── examples/workflow.md
```

## 工作流速查

### A. 写一段新脚本

1. 复制模板：`templates/event_script.tea` 或 `templates/procedure.tea`。
2. 用普通 `read_file/replace_in_file` 编辑。
3. lint：
   ```bash
   python .ai/skills/teascript-helper/scripts/teascript_lint.py path/to/my.tea
   ```
4. （可选）格式化：
   ```bash
   python .ai/skills/teascript-helper/scripts/teascript_format.py path/to/my.tea -o path/to/my.tea
   ```

### B. 嵌入 lvl

```bash
# 直接添加为 lvl 的 S 行（UTF-8 嵌入脚本）
python .ai/skills/teascript-helper/scripts/teascript_inject.py \
    path/to/level.lvl --tea path/to/my.tea --name "MyScript" \
    -o path/to/level.modified.lvl

# 把脚本绑定到一个事件（创建事件并把 ene/scriptname 指向 MyScript）
python .ai/skills/teascript-helper/scripts/teascript_event.py \
    path/to/level.modified.lvl --event "OnMyTrigger" --script "MyScript" \
    --autostart 1 -o path/to/level.modified.lvl
```

### C. 一键回归

```bash
python .ai/skills/teascript-helper/scripts/teascript_test.py \
    --lvl path/to/level.lvl \
    --tea path/to/my.tea \
    --name "MyScript" \
    --event "OnMyTrigger" \
    --smbx "C:/SMBX38A/smbx.exe" \
    --screenshot ".cache/snap.png"
```
该命令会：
1. **lint** 你的 `.tea`；如失败立即返回。
2. **注入** 到 lvl 的副本 `*.modified.lvl`。
3. （可选）创建/绑定事件。
4. **reload** 引擎加载关卡。
5. **trigger** 指定事件。
6. **state** 抓对象数与变量。
7. **screenshot** 抓窗口图像。

## 行动准则（给 AI 的硬约束）

1. **写脚本前必查**：`reference/syntax-cheatsheet.md` 和 `reference/builtin-functions.md`，避免凭直觉写 VB / JS 风格代码。TeaScript 的注释是 `'`，不是 `//`。
2. **任何 `script ... end script` 块必须放在脚本文件末尾**（语言规约）。
3. **每帧逻辑的标准范式**：38A **没有"每帧自动事件"**——`autostart=1` 仅触发一次。每帧逻辑必须用：
   ```teascript
   ' 一次性初始化（dim 在 do 外）
   dim i as integer
   ' ...
   do
       ' 每帧执行的代码
       call sleep(1)        ' ⚠ 必不可少
   loop
   ```
   一个 lvl 只允许一个 `Level - Start`，多个长循环挂不同 autostart=1 事件名。详见 `reference/snippets.md` 第 13 节。
4. **避免无 `sleep`/`exit` 的 `do ... loop` 死循环**，会冻结游戏。**记住 `do ... loop` 内必须有 `call sleep(1)` 或 `exit do`**。
5. **不要除以 0 / mod 0**，会直接 crash。
6. **`dim` 类型与全局脚本兼容**：`long`/`single`/`double` 在 1.4.4 全局脚本中有 bug；老版本游戏写全局脚本请用 `byte`/`integer`（1.4.5 已修复）。
7. **嵌入到 lvl 时，名字遵守变量命名规范**（字母数字、字母开头、不含空格、**不含下划线**）。
8. **用户数组用 R 行声明**（不是 V 行）：`b.add_array('arr1','arr2',...)`；脚本里 `call redim(0, arr, len)` 后用 `array(arr(idx))` 访问。详见 `reference/snippets.md` 第 14 节。
9. **改完必跑** `teascript_lint.py` + `lvl_validate.py` + `lvl_var_check.py`，再向用户汇报。
10. **运行时验证不要假设引擎能自动启动**：`session.py run` 在很多环境下因为 SMBX 进程已经以 editor 模式运行 / IPC 上线慢 / 路径不一致而失败。**默认假设无法自动启动测试模式**，构建 + 静态校验通过后**直接交给用户手测**，不要反复尝试自动启动浪费时间。能用的命令是 `session.py open-editor` 让用户用编辑器打开后自己 F1。


## 快速参考链接

- 语法权威文档：`.docs/.teascript-docs/TeaScript Syntax.md`
- 自动事件清单：`.docs/.teascript-docs/Autorun Events.md`
- Sysval：`.docs/.teascript-docs/Sysval (TeaScript).md`
- 内置函数：`.docs/.teascript-docs/Functions (TeaScript).md`
- 编辑器函数：`.docs/.teascript-docs/Editor Functions.md`
- 文件格式：`.docs/.smbx38a-docs/smbx-38A File specifications (LVL WLD WLS).md`
