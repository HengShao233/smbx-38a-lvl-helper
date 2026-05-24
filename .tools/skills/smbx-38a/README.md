# smbx-38a Skill

为 AI 提供 SMBX 38A 完整开发工作流：

| 能力 | 入口 |
| --- | --- |
| **新建关卡（高层 API，强烈推荐）** | `scripts/lvl_builder.py` (`LVLBuilder`) |
| **静态校验关卡（11 项格式陷阱）** | `scripts/lvl_validate.py` |
| 解析 `.lvl/.wld/.wls` | `scripts/lvl_parse.py`、`scripts/lvl_query.py` |
| 编辑条目（NPC/方块/事件等） | `scripts/lvl_edit.py` |
| 提取/回写 TeaScript 脚本 | `scripts/lvl_scripts.py` |
| 通过共享内存 IPC 控制引擎 | `scripts/ipc_client.py`、`scripts/engine_control.py` |
| 测试会话 + Editor 管理（自动定位 / 用户 review） | `scripts/session.py` |
| 窗口截图自检 | `scripts/screenshot.py` |

## 🚫 硬约束

**AI 不得用 `write_to_file`/`replace_in_file` 直接生成 `.lvl` 文件文本。**
所有 `.lvl` 写入必须通过本 skill 的工具：
- 新建关卡 → `LVLBuilder`
- 改条目 → `lvl_edit.py`
- 改脚本 → `lvl_scripts.py extract/inject`
- 写完 → `lvl_validate.py` 必须 0 errors

详细 SOP 与踩坑总表见 [`SKILL.md`](./SKILL.md) 与 [`reference/lvl-format.md`](./reference/lvl-format.md)。

## 依赖

- Python 3.8+（项目已使用）
- Windows（IPC 与截图依赖 Win32 API；离线解析/编辑跨平台可用）
- 标准库即可，无需第三方包（截图使用 PowerShell + .NET，IPC 使用 `ctypes` 调 `kernel32`）
