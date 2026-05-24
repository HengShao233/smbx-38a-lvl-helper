# AI 在 SMBX 38A 项目里的标准开发工作流

## 一、看懂一关在做什么

```bash
# 1. 摘要
python .ai/skills/smbx-38a/scripts/lvl_parse.py "<lvl>" --summary

# 2. 列脚本名
python .ai/skills/smbx-38a/scripts/lvl_scripts.py list "<lvl>"

# 3. 按条件查（NPC id=283 + 非默认图层）
python .ai/skills/smbx-38a/scripts/lvl_query.py "<lvl>" --kind N --filter id=283

# 4. 拿事件清单
python .ai/skills/smbx-38a/scripts/lvl_query.py "<lvl>" --kind E --fields name
```

## 二、改 TeaScript 脚本（最常见）

> AI 不要直接动 base64！必须 extract → 编辑文本 → inject。

```bash
# 步骤 A：导出全部脚本（生成 <dir>/<scriptname>.tea + index.json）
python .ai/skills/smbx-38a/scripts/lvl_scripts.py extract "<lvl>" -o ".cache/scripts/level1"

# 步骤 B：用普通 read_file/replace_in_file 工具修改 <dir>/<scriptname>.tea

# 步骤 C：回写到新 lvl（默认输出 <lvl>.modified.lvl）
python .ai/skills/smbx-38a/scripts/lvl_scripts.py inject "<lvl>" \
       -i ".cache/scripts/level1" -o "<lvl>.modified.lvl"

# 步骤 D：round-trip 校验（解析新文件，确保结构无破坏）
python .ai/skills/smbx-38a/scripts/lvl_parse.py "<lvl>.modified.lvl" --summary
```

## 三、增/删/改对象（设计地图）

支持 marker：`B`（Block）、`N`（NPC）、`T`（BGO）、`L`（Layer）、`E`（Event）、`V`（Variable）、`W`（Warp）、`Q`（Liquid）。

```bash
# 增加 Block
python .ai/skills/smbx-38a/scripts/lvl_edit.py "<lvl>" -o "<out.lvl>" \
  --add B --layer Default --id 1 --x 320 --y -160 --w 32 --h 32

# 增加 NPC
python .ai/skills/smbx-38a/scripts/lvl_edit.py "<lvl>" -o "<out.lvl>" \
  --add N --layer Default --id 1 --x 100 --y -120

# 删除满足条件的所有 NPC（id=1 且 x<200）
python .ai/skills/smbx-38a/scripts/lvl_edit.py "<lvl>" -o "<out.lvl>" \
  --del N --where "id=1,x<200"

# 修改字段
python .ai/skills/smbx-38a/scripts/lvl_edit.py "<lvl>" -o "<out.lvl>" \
  --set N --where "id=1" --field "y=-300"
```

每次改完都建议：
```bash
python .ai/skills/smbx-38a/scripts/lvl_parse.py "<out.lvl>" --summary
```

## 四、运行时验证（IPC + 截图）

> 仅在 SMBX 处于 level testing 模式时才有 IPC。本 skill 提供完整封装。

```bash
# 1. 启动测试模式（这会调用 smbx.exe 命令行）
python .ai/skills/smbx-38a/scripts/engine_control.py launch \
  --smbx "C:/Path/To/smbx.exe" --lvl "<lvl>" --mode 0 --p1 0 --p2 1

# 2. ping 一下
python .ai/skills/smbx-38a/scripts/engine_control.py ping

# 3. 触发事件
python .ai/skills/smbx-38a/scripts/engine_control.py trigger --event "MyEvent"

# 4. 取游戏状态
python .ai/skills/smbx-38a/scripts/engine_control.py state --object-count
python .ai/skills/smbx-38a/scripts/engine_control.py state --camera
python .ai/skills/smbx-38a/scripts/engine_control.py state --var "myVar"

# 5. 显示一个 messagebox 检查脚本是否还活着
python .ai/skills/smbx-38a/scripts/engine_control.py message --text "ping"

# 6. 修改了 lvl 后，重载
python .ai/skills/smbx-38a/scripts/engine_control.py reload \
  --smbx "C:/Path/To/smbx.exe" --lvl "<lvl>"

# 7. 截图自检
python .ai/skills/smbx-38a/scripts/screenshot.py --window "smbx" -o ".cache/snap.png"
```

## 五、闭环回归 SOP（推荐 AI 默认采用）

```
[读] lvl_parse / lvl_query     -> 形成对当前关卡心智模型
[改] lvl_scripts extract        -> read_file / replace_in_file 改 .tea
     lvl_scripts inject         -> 写入新 lvl
[校] lvl_parse --summary        -> round-trip 验证 + diff
[跑] engine_control reload      -> 把新 lvl 推到引擎
[验] engine_control trigger     -> 触发关键事件
     engine_control state       -> 抓变量 / 计数
     screenshot                 -> 视觉验证
[回] 把改动 + 验证截图汇报给用户
```

## 六、何时不要用本 skill

- 任务只是修改美术资源（`.png/.aseprite`）：直接走美术工具。
- 任务只是改 README 等纯文档：直接 read/replace。
- 不在 Windows 环境且只需文件解析：本 skill 解析/编辑/脚本部分跨平台可用，IPC + 截图仅 Windows。
