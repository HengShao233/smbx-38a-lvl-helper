---
name: smbx-38a
description: SMBX 38A 关卡/世界/世界设置文件 (.lvl/.wld/.wls) 的解析、查询、编辑与运行时引擎控制工具集。当用户需要查看关卡结构、提取/修改 TeaScript 脚本、增删 NPC/方块/事件、设计或回归测试关卡、通过 IPC 操控 SMBX 引擎（重载关卡、触发事件、获取游戏状态、截图自检）时使用。
license: project-internal
---

# SMBX 38A 开发工作流 Skill

本 skill 为 AI 提供一套完整的 SMBX 38A 关卡/世界文件 **离线编辑** + **运行时引擎控制** + **视觉自检** 的工作流能力。

## 何时使用

只要任务涉及以下任何一项，**优先**使用本 skill：

- 读取/解析 `.lvl`、`.wld`、`.wls` 文件结构（NPC、方块、事件、脚本、传送门……）
- 提取 / 修改 / 回写关卡中嵌入的 TeaScript 脚本（`S`、`Su`、`GS`、`GSu`）
- 增删改地图对象（设计或修改地图）
- 通过 IPC 操控正在运行的 `smbx.exe`（仅 level testing 模式下生效）：
  - 创建/放置 Block、BGO、NPC
  - 设置图层显隐、触发事件、显示消息框
  - 查询当前对象数、相机位置、变量值、玩家状态
- **管理 SMBX / Editor 进程会话**（自动定位可执行 / 列进程 / 启动 editor / 启停测试 / 让用户 review）
- 测试/验证/回归 AI 编写的关卡或脚本是否生效
- 对游戏窗口截图，做视觉自检

> 写、检查、嵌入 **TeaScript 代码**请用 `teascript-helper` skill。两者协同工作。

## 关键约束

1. **🚫 严禁手写 `.lvl` 文件文本**——AI 必须**通过本 skill 提供的工具**生成或修改关卡文件。
   - **新建关卡**：只能用 `scripts/lvl_builder.py` 的 `LVLBuilder` 高层 API。
   - **改条目**：只能用 `scripts/lvl_edit.py` CLI 或 `lvlfile.SMBXFile` 库 API。
   - **改脚本**：只能用 `scripts/lvl_scripts.py` 的 extract → 编辑 `.tea` → inject 流程。
   - **写完必校验**：`scripts/lvl_validate.py` 必须 0 errors，否则 SMBX 引擎会报 `run-time error '13' Type Mismatch`。
   - 这些工具内部封装了所有已实测的格式陷阱（详见 `reference/lvl-format.md` 的踩坑总表 11 项）；手写极易触发引擎加载失败。
2. **文件格式严格按 38A 规范**：详见 `reference/lvl-format.md`。
   - 行首是 marker（`A`、`P1`、`B`、`N`、`S` 等），字段以 `|` 分隔，子字段以 `,` 或 `/` 分隔。
   - **字符串字段使用 38A 强制百分号编码**（每个字符 `%xx`，与 RFC 3986 不同）；`lvlfile.url_encode()` 已实现。
   - 脚本字段 Base64 编码。
   - **额外字段允许追加在行尾**，但严禁在中间插入或替换已有字段顺序。
   - 编辑后必须保持原有 `SMBXFile??` 头与文件原编码（一般 ASCII；行尾 CRLF）。
3. **IPC 仅在 level testing 模式下可用**：`smbx.exe <lvl> <mode> <p1> <p2> <args>` 启动后才能连上 `smbx_memory_block` 共享内存。
4. **永不破坏原文件**：所有编辑工具默认 `--inplace` 关闭，需显式指定输出路径，或调用方负责备份。
5. **行尾保持 CRLF/LF 与原文件一致**（项目内 lvl 大多 `CRLF`）。

## 目录结构

```
.tools/skills/smbx-38a/
├── SKILL.md                       # 本文件（入口）
├── README.md                      # 概览与快速上手
├── reference/                     # 给 AI 的速查
│   ├── lvl-format.md              # ⚠ 行 marker / 字段速查表 + 11 项踩坑总表
│   ├── ipc-protocol.md            # 共享内存协议 + 命令清单
│   └── workflow.md                # 推荐 AI 开发 SOP
├── scripts/                       # 可执行 Python 工具
│   ├── lvlfile.py                 # 核心：解析/序列化库（含 38A 强制百分号编码）
│   ├── lvl_builder.py             # ⭐ 高层 API：LVLBuilder（新建关卡用这个）
│   ├── lvl_validate.py            # ⭐ 静态校验：检测 11 项格式陷阱（改完必跑）
│   ├── lvl_var_check.py           # ⭐ 校验脚本里 v(...) 引用都已在 V 行预声明
│   ├── lvl_parse.py               # CLI: 解析为 JSON 摘要
│   ├── lvl_query.py               # CLI: 按条件查询条目
│   ├── lvl_edit.py                # CLI: 增/删/改条目
│   ├── lvl_scripts.py             # CLI: 提取/回写嵌入脚本
│   ├── ipc_client.py              # 库 + CLI: Windows 共享内存 IPC
│   ├── engine_control.py          # CLI: 引擎控制（launch/reload/trigger/状态）
│   ├── session.py                 # CLI: 测试会话 + Editor 进程管理
│   └── screenshot.py              # CLI: 截 SMBX 窗口或全屏
└── examples/
    └── usage_examples.md
```

## 推荐工作流（速查）

> 详见 `reference/workflow.md`。

**A. 看一关有什么**
```bash
python .tools/skills/smbx-38a/scripts/lvl_parse.py "<file.lvl>" --summary
python .tools/skills/smbx-38a/scripts/lvl_query.py "<file.lvl>" --kind N --filter id=283
```

**B. 改脚本**
```bash
# 1) 把所有嵌入脚本导出到 .tea 文件
python .tools/skills/smbx-38a/scripts/lvl_scripts.py extract "<file.lvl>" -o "<dir>"
# 2) 编辑导出的 .tea 文件（AI 直接 read/replace_in_file 即可）
# 3) 回写
python .tools/skills/smbx-38a/scripts/lvl_scripts.py inject "<file.lvl>" -i "<dir>" -o "<file.modified.lvl>"
```

**C. 设计地图（增/删/改 NPC、Block、事件）**
```bash
# 例：在指定坐标加一个 NPC id=1 (Goomba)
python .tools/skills/smbx-38a/scripts/lvl_edit.py "<file.lvl>" \
  --add N --layer Default --id 1 --x 100 --y -200 -o "<file.modified.lvl>"
```

**D. 运行时验证（需先用 SMBX 测试模式启动关卡）**
```bash
# —— 推荐方式：高层会话（自动定位 smbx.exe / 自动等待 IPC / 触发 / 截图 / 让用户 review）
python .tools/skills/smbx-38a/scripts/session.py run \
  --lvl "<file.lvl>" --trigger "MyEvent" --state \
  --screenshot ".cache/snap.png"
# 没有 --smbx？工具会自动从已运行进程或常见路径找；找不到会提示用户。

# —— 低层方式：手动控制每个步骤
python .tools/skills/smbx-38a/scripts/engine_control.py launch \
  --smbx "C:/Path/To/smbx.exe" --lvl "<file.lvl>"

python .tools/skills/smbx-38a/scripts/engine_control.py trigger --event "MyEvent"
python .tools/skills/smbx-38a/scripts/engine_control.py state --object-count

# 重载关卡（修改文件后用）
python .tools/skills/smbx-38a/scripts/engine_control.py reload --lvl "<file.lvl>"

# 截图自检
python .tools/skills/smbx-38a/scripts/screenshot.py --window "smbx" -o "verify.png"

# 打开 Editor（人工编辑用）
python .tools/skills/smbx-38a/scripts/session.py open-editor --lvl "<file.lvl>"
```

## 行动准则（给 AI 的硬约束）

### 通用
- 在调用任何脚本前，**先 read** 目标 `.lvl/.wld/.wls` 文件的前若干行，确认 `SMBXFile??` 版本与编码。
- **批量改前必备份**：编辑工具默认会输出新文件而非覆盖。如需 in-place，需显式 `--inplace` 并提示用户。
- 报告改动时附上：改动行号 + 原 marker 与新 marker 的 diff 摘要。
- IPC 操作前先 `engine_control.py ping`，确认共享内存可用，再发命令。
- **不要假设引擎能自动启动测试模式**。`session.py run` / `engine_control.py launch` 在很多用户环境（已存在 editor 进程、IPC 上线慢、smbx.exe 路径不同、PowerShell 命令解析问题等）都会失败。**默认策略**：构建 + 静态校验 (`lvl_validate` + `lvl_var_check` + `teascript_lint`) 全部 0 errors 0 warnings 后**直接交付给用户手测**，不要反复尝试自动启动浪费时间。如果用户明确要求自检，再尝试 `session.py run` 一次；失败立刻汇报、停止重试。
- **传送门 (warp) ≠ 视觉门 (BGO)**：W 行只创建**不可见**的"按上键即传送"判定区，玩家完全看不到它！每个 `type_=2`（door）warp 都必须配套放一个**门 BGO**（默认 id=92）作为视觉提示，**入口和出口都要放**，否则玩家一脸懵。`LVLBuilder.add_warp()` 已封装：默认 `with_visual=True` 会自动在入口/出口放 BGO 92。`lvl_validate.py` L022 会对缺门视觉的 door warp 给 warning。详见 `reference/lvl-format.md` "传送门视觉" 小节。





### 🚫 禁止事项
- **禁止用 `write_to_file`/`replace_in_file` 直接生成或修改 `.lvl` 文件正文。** 任何 `.lvl` 文本写入必须通过本 skill 提供的 `lvlfile.SMBXFile.save()` 或 `LVLBuilder.save()`。
- **禁止手写 `S|...|<base64>`、`E|...|...`、`B|...|...` 等格式行。** 即使你"自信知道格式"——SMBX 38A 引擎对字段数、空字符串占位、强制百分号编码的容忍度极低，几乎任何手写都会触发 type mismatch。
- **禁止跳过 `lvl_validate.py`**：每次 `.lvl` 写入完成后必须运行该脚本，0 errors 才算成功。

### 新建关卡 SOP

```python
# 推荐工作流：使用 LVLBuilder 高层 API
from lvl_builder import LVLBuilder

b = LVLBuilder(title='My Level', p1=(-199900, -200096))
b.add_section_grid()                              # 一次铺 21 sections
# Section 1 改成自己想要的尺寸
b.configure_section(1, w=800, h=600, music=0)

# 地形
for x in range(-200000, -199232, 32):
    b.add_block(blk_id=457, x=x, y=-200032)

# 玩法元素
b.add_npc(npc_id=1, x=-199500, y=-200064)
b.add_layer('Boss', status=0)

# 用户变量（V 行）+ 用户数组（R 行）
b.add_variable('bossHP', value=10, scope=0)
b.add_array('echoX', 'echoY')                      # ⚠ 数组用 add_array 写 R 行，不要用 V 行假装！

# 事件 ⚠ 38A 没有"每帧自动事件"
# 每帧脚本必须自己写 do ... call sleep(1) ... loop，
# 用 autostart=1 的事件挂上去，触发一次然后永久循环。
b.add_event('Level - Start', autostart=1, script_name='Main')
b.add_event('OnWin', show_layers=['Boss'], hide_layers=['Default'])

# 嵌入脚本 ⚠ 含非 ASCII（中文等）必须用 SU marker
# LVLBuilder.add_script 默认就是 SU，无需手动指定
b.add_script('Main', open('main.tea').read())     # 名字必须字母+数字，字母开头

# 自定义贴图占位（可选，与 TP.lvl 一致）
b.add_custom_texture(1, '00081')

# 保存（自动跑 lvl_validate；失败会抛异常）
b.save('out.lvl')
```

**每帧脚本的标准范式**（写在 main.tea 里）：

```teascript
' 一次性初始化（dim 必须在 do 外）
dim i as integer
v(bossHP) = 10
call redim(0, echoX, 90)
call redim(0, echoY, 90)

' 永久主循环
do
    ' ... 每帧逻辑 ...
    array(echoX(0)) = char(1).x
    
    call sleep(1)        ' 必不可少
loop
```


### 修改现有关卡 SOP

```bash
# 改条目用 lvl_edit
python .tools/skills/smbx-38a/scripts/lvl_edit.py "<lvl>" -o "<out.lvl>" \
  --add N --layer Default --id 1 --x 100 --y -120

# 改脚本用 extract/inject（绝不要手写 S|...|<base64>）
python .tools/skills/smbx-38a/scripts/lvl_scripts.py extract "<lvl>" -o ".cache/scripts"
# 改 .cache/scripts/<name>.tea
python .tools/skills/smbx-38a/scripts/lvl_scripts.py inject "<lvl>" -i ".cache/scripts" -o "<out.lvl>"

# ⭐ 改完必跑两层校验
python .tools/skills/smbx-38a/scripts/lvl_validate.py "<out.lvl>"
python .tools/skills/smbx-38a/scripts/lvl_var_check.py "<out.lvl>"
# 若有 errors，根据 [Lxxx] 规则码对照 reference/lvl-format.md 修复
# lvl_var_check 报缺失变量时可用 --fix 自动补 V 行
```

## 快速参考链接

- 文件格式权威文档：`.docs/.smbx38a-docs/smbx-38A File specifications (LVL WLD WLS).md`
- IPC 命令权威清单：`.docs/.smbx38a-docs/Engine IPC Interface/Cpp-Example/command.txt`
- TeaScript 文档：`.docs/.teascript-docs/`
