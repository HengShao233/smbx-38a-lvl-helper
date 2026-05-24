# 使用示例

> 所有命令在 PowerShell 中执行，工作目录 = 项目根 `NeuralWarp-Creator/`。

## 1. 看一关里有什么

```powershell
python .ai/skills/smbx-38a/scripts/lvl_parse.py "Scenes/Entries/TP.lvl" --summary
```

输出（节选）：
```json
{
  "kind": "lvl",
  "version": 69,
  "newline": "CRLF",
  "encoding": "ascii",
  "title": "",
  "marker_count": {"A":1,"BTNS":1,"P1":1,"M":21,"B":34,"T":57,"W":2,"Q":3,"L":3,"E":4,"CT":2,"CW":1},
  "layers": ["Default","Destroyed Blocks","Spawned NPCs"],
  "events": ["Level - Start","P Switch - Start","P Switch - End","Door"],
  "total_block": 34, "total_warp": 2, "total_event": 4
}
```

## 2. 列出所有 NPC id=1 且 x<200 的

```powershell
python .ai/skills/smbx-38a/scripts/lvl_query.py "<file.lvl>" --kind N --filter "id=1" --filter "x<200"
```

## 3. 列出脚本

```powershell
python .ai/skills/smbx-38a/scripts/lvl_scripts.py list "<file.lvl>"
```

## 4. 修改一段嵌入 TeaScript（推荐流程）

```powershell
# 4.1 导出
python .ai/skills/smbx-38a/scripts/lvl_scripts.py extract "<file.lvl>" -o ".cache/scripts/level1"

# 4.2 用普通文件编辑工具改 .cache/scripts/level1/0123_xxx.tea

# 4.3 注入回新文件
python .ai/skills/smbx-38a/scripts/lvl_scripts.py inject "<file.lvl>" `
    -i ".cache/scripts/level1" -o "<file.lvl>.modified.lvl"

# 4.4 round-trip 校验
python .ai/skills/smbx-38a/scripts/lvl_parse.py "<file.lvl>.modified.lvl" --summary
```

## 5. 设计地图（增删改）

```powershell
# 同时增加 NPC + Block，删除指定坐标的旧 Block
python .ai/skills/smbx-38a/scripts/lvl_edit.py "Scenes/Entries/TP.lvl" `
    -o ".cache/test_edit.lvl" `
    --add N --layer Default --id 1 --x 100 --y -120 `
    --add B --layer Default --id 90 --x 0 --y 0 --w 32 --h 32 `
    --del B --where "id=457,x=-199680,y=-200576"
```

输出：
```
[lvl_edit] +N at index 130: 'N|Default|1|100|-120'
[lvl_edit] +B at index 58: 'B|Default|90|0|0|||||32|32'
[lvl_edit] -B: removed 1 entries (where=[('id','==','457'),('x','==','-199680'),('y','==','-200576')])
[lvl_edit] saved -> .cache/test_edit.lvl
```

## 6. 启动测试模式 + IPC 控制

```powershell
# 6.1 启动（首次需要 --smbx 指定路径，会缓存）
python .ai/skills/smbx-38a/scripts/engine_control.py launch `
    --smbx "C:/SMBX38A/smbx.exe" --lvl "Scenes/Entries/TP.lvl" --wait-ipc 8

# 6.2 ping
python .ai/skills/smbx-38a/scripts/engine_control.py ping

# 6.3 抓状态
python .ai/skills/smbx-38a/scripts/engine_control.py state --all

# 6.4 触发事件
python .ai/skills/smbx-38a/scripts/engine_control.py trigger --event "Level - Start"

# 6.5 显隐图层
python .ai/skills/smbx-38a/scripts/engine_control.py layer --name "Default" --action toggle

# 6.6 弹消息
python .ai/skills/smbx-38a/scripts/engine_control.py message --text "Hello from AI"

# 6.7 查变量
python .ai/skills/smbx-38a/scripts/engine_control.py state --var "myVar"

# 6.8 重载（修改了 lvl 后）
python .ai/skills/smbx-38a/scripts/engine_control.py reload --lvl "<file>.modified.lvl"
```

## 7. 截图自检

```powershell
# 截 SMBX 窗口（自动按标题子串匹配）
python .ai/skills/smbx-38a/scripts/screenshot.py --window smbx -o ".cache/snap.png"

# 找不到？先列出所有可见窗口
python .ai/skills/smbx-38a/scripts/screenshot.py --list-windows

# 截整个屏幕
python .ai/skills/smbx-38a/scripts/screenshot.py --screen -o ".cache/screen.png"
```

## 8. 完整闭环示例（AI 修脚本 + 验证）

```powershell
$lvl   = "Scenes/Entries/TP.lvl"
$out   = ".cache/TP.modified.lvl"
$dir   = ".cache/scripts/TP"

# 解析 + 列表
python .ai/skills/smbx-38a/scripts/lvl_parse.py $lvl --summary
python .ai/skills/smbx-38a/scripts/lvl_scripts.py list $lvl

# 抽取脚本，AI 用普通编辑工具改 *.tea，再 inject
python .ai/skills/smbx-38a/scripts/lvl_scripts.py extract $lvl -o $dir
# ...AI edit *.tea ...
python .ai/skills/smbx-38a/scripts/lvl_scripts.py inject $lvl -i $dir -o $out

# round-trip 校验
python .ai/skills/smbx-38a/scripts/lvl_parse.py $out --summary

# 加载到引擎并验证
python .ai/skills/smbx-38a/scripts/engine_control.py reload --lvl $out
python .ai/skills/smbx-38a/scripts/engine_control.py state --all
python .ai/skills/smbx-38a/scripts/screenshot.py --window smbx -o ".cache/snap.png"
```

## 9. 直接调用 IPC 原始命令

```powershell
python .ai/skills/smbx-38a/scripts/ipc_client.py send "GGI|NOPAUSE"
python .ai/skills/smbx-38a/scripts/ipc_client.py send-recv "GGI|ON" --expect "GGI|ON"

# REPL 调试
python .ai/skills/smbx-38a/scripts/ipc_client.py raw
```
