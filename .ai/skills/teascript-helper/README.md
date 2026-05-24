# teascript-helper Skill

为 SMBX 38A 的 **TeaScript** 脚本提供完整开发与回归工作流。

参见 [`SKILL.md`](./SKILL.md)。

## 关键能力

| 能力 | 入口 |
| --- | --- |
| 语法速查（VB6 风格的方言） | [`reference/syntax-cheatsheet.md`](./reference/syntax-cheatsheet.md) |
| 内置函数清单 | [`reference/builtin-functions.md`](./reference/builtin-functions.md) |
| 自动事件名表 | [`reference/autorun-events.md`](./reference/autorun-events.md) |
| 常用代码模板 | [`templates/`](./templates) |
| 静态 lint | [`scripts/teascript_lint.py`](./scripts/teascript_lint.py) |
| 规整化格式 | [`scripts/teascript_format.py`](./scripts/teascript_format.py) |
| 嵌入到 lvl | [`scripts/teascript_inject.py`](./scripts/teascript_inject.py) |
| 创建/绑定事件 | [`scripts/teascript_event.py`](./scripts/teascript_event.py) |
| **一键回归测试** | [`scripts/teascript_test.py`](./scripts/teascript_test.py) |

## 与 `smbx-38a` 协作

本 skill 直接复用同仓库 `.ai/skills/smbx-38a/scripts/` 下的 `lvlfile.py`、`engine_control.py`、`screenshot.py`。
所有 `.tea ↔ .lvl` 的双向流动都走 `lvlfile.SMBXFile`，保证 round-trip 无损。
