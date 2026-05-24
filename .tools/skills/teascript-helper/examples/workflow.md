# teascript-helper 工作流示例

## 0. 准备

```powershell
# 列出已有 skill 工具（健康检查）
python .tools/skills/teascript-helper/scripts/selftest.py
python .tools/skills/smbx-38a/scripts/selftest.py
```

## 1. 写一段新脚本（基于模板）

```powershell
# 复制模板（你自己开发的脚本建议放在 .cache/ 或 Scripts/ 自己的子目录）
Copy-Item .tools/skills/teascript-helper/templates/event_script.tea ".cache/MyScript.tea"

# 用普通编辑器或 IDE 修改 .cache/MyScript.tea
# ...

# lint
python .tools/skills/teascript-helper/scripts/teascript_lint.py .cache/MyScript.tea
```

输出示例：
```
.cache/MyScript.tea:8:1: WARN  [W104] 在 if 块内 dim 在旧版有 bug，建议提到 if 外
[teascript_lint] 0 error(s), 1 warning(s)
```

## 2. 嵌入到关卡

```powershell
python .tools/skills/teascript-helper/scripts/teascript_inject.py `
    Scenes/Entries/TP.lvl `
    --tea .cache/MyScript.tea `
    --name "MyScript" `
    -o .cache/TP.test.lvl
```

## 3. 绑定到事件（让脚本在某事件触发时被调用）

```powershell
# 创建新事件 OnFoo，自动启动（autostart=1 = Level Start 时触发），运行 MyScript
python .tools/skills/teascript-helper/scripts/teascript_event.py `
    .cache/TP.test.lvl `
    --event "OnFoo" --script "MyScript" --autostart 1 `
    -o .cache/TP.test.lvl
```

支持的事件：
- 任意自定义名字（被脚本/对象 `call SET("EventName")` 触发）
- 自动事件名（如 `Level - Start`、`NPC - Death`，详见 [`reference/autorun-events.md`](../reference/autorun-events.md)）

## 4. 一键回归测试

```powershell
python .tools/skills/teascript-helper/scripts/teascript_test.py `
    --lvl Scenes/Entries/TP.lvl `
    --tea .cache/MyScript.tea `
    --name "MyScript" `
    --event "OnFoo" --autostart 1 `
    --smbx "C:/SMBX38A/smbx.exe" `
    --screenshot ".cache/snap.png"
```

完整流程会执行：
1. `teascript_lint.py` 检查 .tea
2. 拷贝 lvl 到 `.cache/<lvl>.test.lvl`
3. `teascript_inject.py` 嵌入脚本
4. `teascript_event.py` 创建/绑定事件
5. `lvl_parse.py --summary` round-trip 校验
6. `session.py run` 启动测试 -> 等 IPC -> 触发事件 -> 抓状态 -> 截图 -> **暂停让你 review** -> 用户回车后由你决定是否 stop

加 `--no-launch` 只到 round-trip 为止；加 `--no-review --auto-stop` 完全无人值守。

## 5. 单元化的 SMBX 会话控制

```powershell
# 当前有没有跑 SMBX？
python .tools/skills/smbx-38a/scripts/session.py status
python .tools/skills/smbx-38a/scripts/session.py list-procs

# 自动找 smbx.exe（看缓存 / 看运行中进程 / 扫常见路径）
python .tools/skills/smbx-38a/scripts/session.py locate

# 启动 editor（用于人工编辑）
python .tools/skills/smbx-38a/scripts/session.py open-editor `
    --editor "C:/SMBX38A/editor.exe" --lvl Scenes/Entries/TP.lvl

# 一键测试（不与 teascript_test.py 联动也行）
python .tools/skills/smbx-38a/scripts/session.py run `
    --lvl .cache/TP.test.lvl `
    --trigger "OnFoo" --state `
    --screenshot ".cache/snap.png"

# 收尾
python .tools/skills/smbx-38a/scripts/session.py stop
```

## 6. 找不到 smbx.exe / editor.exe 时

`session.py` / `engine_control.py` 的输出会清楚告诉你：

```
============================================================
❌ 找不到 SMBX editor 可执行文件。

请按以下任一方式让我能找到它：
  1. 打开 SMBX Editor（让它跑起来），然后重新执行本命令；
     工具会自动从已运行进程读取它的安装路径。
  2. 或者直接传入路径，例如：--editor "C:/SMBX38A/editor.exe"

我会自动把路径缓存起来（保存在 .smbx_editor_path），下次无需重复指定。
============================================================
```

## 7. 故障排查

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| `OpenFileMapping("smbx_memory_block") failed (winerror=2)` | smbx.exe 不在 testing 模式下运行 | 用 `session.py run` 或 `engine_control.py launch` 重新启动 |
| `[teascript_inject] 同名脚本已存在` | lvl 中已有同名 `S` 行 | 不加 `--add-only` 即会覆盖；要保留则换名字 |
| `[lvl_parse] round-trip 失败` | 编辑产生了不合规字段 | 检查 `--field` 是否包含 `|`/`/` 等保留字符 |
| `screenshot 失败 rc=1` | SMBX 窗口标题不含 "smbx" | 用 `--screenshot-window` 指定一个窗口标题子串 |
| lint 误报 W102（未知函数） | 项目里的自定义/全局 script 在另一文件 | `--disable W102` 或忽略（仅 warning） |
