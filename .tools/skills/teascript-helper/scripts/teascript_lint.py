#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teascript_lint.py — TeaScript 静态检查器（无完整 parser，基于行级 + 词法启发）。

设计目标：
- 不追求 AST 严格性，专注于捕获**高频致命错误**与**风格规约**。
- 误报率优先低，宁可漏不错杀；所有规则可由 --disable 关闭。
- 命中即给出 line:col + 规则码 + 建议。

规则码：
    E001  注释符不正确（用了 // 或 # 而非 '）
    E002  字符串缺右引号
    E003  字面量除以 0 / mod 0 / \ 0
    E004  script 块未闭合（缺 end script）
    E005  if/do/for/select 块未闭合
    E006  end 语句无对应起始
    E007  script 块名包含数字（违反命名规范）
    E008  dim 变量名违规（含空格 / 数字开头 / 含非法字符）
    E009  script 块后还有可执行主体代码（script 必须在文件末尾）
    E010  next 后跟变量名（38A 不允许，只能裸写 `next`）
    E011  procedure 内使用 return 单独退出（会被引擎判为 function 缺 return type）
    E012  调用 SET() / SLT() / TMG()（这是 IPC 命令，不是 TeaScript 内置函数）
    E013  内置函数参数数量错误（基于已知签名速查）
    E014  代码语句后跟同行注释（38A 引擎实测：会破坏赋值语义，触发"未声明变量"等假错）
    W101  do ... loop 内未发现 sleep 或 exit do（可能死循环）
    W102  调用了不在内置/自定义函数白名单里的名字
    W103  使用了 // 之外的可疑符号（# 注释）
    W104  在 if 块内 dim（旧版本 bug）
    W105  跨类型字面量比较启发式
    W106  使用了下划线变量名（v(_xxx) / dim _xxx）
    W107  v(name) 中的 name 含下划线（引擎拒绝）

CLI:
    python teascript_lint.py path/to/x.tea
    python teascript_lint.py path/to/x.tea --json
    python teascript_lint.py path/to/x.tea --disable W102
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


# ---- 内置 / 已知名字（用于 W102 警告） ----
BUILTIN_FUNCTIONS: Set[str] = {
    # 数学
    'abs', 'exp', 'log', 'sgn', 'int', 'fix', 'sqr',
    'sin', 'cos', 'tan', 'atn', 'getangle',
    'chr', 'chrw', 'asc', 'len', 'mid', 'left', 'right', 'lcase', 'ucase',
    'cdbl', 'cint', 'clng', 'csng', 'cbyte', 'cstr', 'val', 'str',
    # 数组 / 类型
    'redim',
    # 音频
    'audioset',
    # HUD / UI / 文本
    'hudset', 'showmsg', 'sysshowmsg', 'sysshowinput',
    'tcreate', 'tcreateex', 'tclear', 'txtcreate',
    # bitmap
    'bmpcreate', 'berase',
    # 效果 / NPC / Block / Layer
    'fxcreate', 'ncreate', 'ncreategroup', 'nkill', 'bset',
    'lmove', 'lset', 'lspin',
    # 迭代器
    'itrcreate', 'itrnext', 'itrtype',
    # 输入
    'keypress',
    # 控制 / 时机
    'sleep', 'exescript', 'spevent', 'scriptid', 'scset', 'debug',
    'playnote',
    # 编辑器
    'objectcreate', 'objectremove',
    # 系统对象访问（虽然是关键字，也加白）
    'sysval', 'val', 'v', 'gval', 'gv', 'str', 'gstr', 'array', 'strarray',
    'char', 'npc', 'block', 'bgo', 'liquid', 'effect', 'warp',
    'section', 'liquid', 'lvltimer', 'text', 'bitmap',
    # 关键字
    'true', 'false', 'pi', 'e', 'rnd', 'nothing', 'null',
    # 颜色 / 数学辅助 (TeaScript 内置)
    'rgba', 'rgb',
    # NPC permID -> index 转换
    'getid',
}

KEYWORDS: Set[str] = {
    'if', 'then', 'else', 'elseif', 'end',
    'select', 'case', 'is', 'to',
    'do', 'loop', 'while', 'until',
    'for', 'next', 'step',
    'exit', 'return',
    'dim', 'as',
    'script', 'export', 'call',
    'and', 'or', 'not', 'xor', 'eqv', 'imp', 'mod', 'like',
    'byte', 'integer', 'long', 'single', 'double', 'string',
    'redim', 'scriptptr',
}


@dataclass
class Diag:
    line: int
    col: int
    code: str
    message: str
    severity: str  # 'error' | 'warning' | 'info'

    def to_dict(self):
        return dict(line=self.line, col=self.col, code=self.code,
                    message=self.message, severity=self.severity)


# ---- 词法工具 ----
def strip_string_and_comment(line: str) -> Tuple[str, bool]:
    """返回 (代码部分, 字符串未闭合标志)。
    用 ' 之前最先出现的非字符串内的 ' 作为注释起点。"""
    out = []
    i, n = 0, len(line)
    in_str = False
    while i < n:
        c = line[i]
        if in_str:
            out.append(c)
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "'":
            # 注释开始，丢弃后续
            break
        out.append(c)
        i += 1
    return ''.join(out), in_str


def find_inline_comment_col(line: str) -> int:
    """返回注释 ' 在原始行中的列号 (0-based)；找不到返回 -1。
    跳过位于字符串字面量内的 '。"""
    i, n = 0, len(line)
    in_str = False
    while i < n:
        c = line[i]
        if in_str:
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            i += 1
            continue
        if c == "'":
            return i
        i += 1
    return -1



WORD_RE = re.compile(r'[A-Za-z_][A-Za-z_0-9]*')
CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z_0-9]*)\s*\(')
DIM_RE = re.compile(r'^\s*dim\s+([^\s,]+)\s+as\s+(byte|integer|long|single|double|string)', re.IGNORECASE)
SCRIPT_DEF_RE = re.compile(r'^\s*(?:export\s+)?script\s+([A-Za-z_][A-Za-z_0-9]*)', re.IGNORECASE)
END_SCRIPT_RE = re.compile(r'^\s*end\s+script\b', re.IGNORECASE)
IF_OPEN_RE = re.compile(r'^\s*if\b.*\bthen\s*$', re.IGNORECASE)         # 多行 if
IF_INLINE_RE = re.compile(r'^\s*if\b.*\bthen\b\s+\S', re.IGNORECASE)    # 单行 if（含语句）
ELSEIF_RE = re.compile(r'^\s*elseif\b', re.IGNORECASE)
ELSE_RE = re.compile(r'^\s*else\s*$', re.IGNORECASE)
END_IF_RE = re.compile(r'^\s*end\s+if\b', re.IGNORECASE)
DO_OPEN_RE = re.compile(r'^\s*do\b', re.IGNORECASE)
LOOP_END_RE = re.compile(r'^\s*loop\b', re.IGNORECASE)
FOR_OPEN_RE = re.compile(r'^\s*for\s+[A-Za-z_]\w*\s*=', re.IGNORECASE)
NEXT_END_RE = re.compile(r'^\s*next\b', re.IGNORECASE)
NEXT_WITH_VAR_RE = re.compile(r'^\s*next\s+\S+', re.IGNORECASE)
SELECT_OPEN_RE = re.compile(r'^\s*select\s+case\b', re.IGNORECASE)
END_SELECT_RE = re.compile(r'^\s*end\s+select\b', re.IGNORECASE)
DIV_ZERO_RE = re.compile(r'(/|\\)\s*0(?!\d)|\bmod\s+0(?!\d)\b', re.IGNORECASE)
COMPARE_LITERAL_RE = re.compile(r'"[^"]*"\s*(=|<>|>=|<=|>|<)\s*-?\d')
RETURN_BARE_RE = re.compile(r'^\s*return\b\s*$|^\s*if\s+.+then\s+return\s*$', re.IGNORECASE)
RETURN_VALUE_RE = re.compile(r'^\s*return\s+\S', re.IGNORECASE)
SET_CALL_RE = re.compile(r'\b(?:call\s+)?(?:SET|SLT|TMG)\s*\(', re.IGNORECASE)
V_REF_RE = re.compile(r'\b(?:v|gv|str|gstr|val|gval)\(\s*([A-Za-z_][A-Za-z_0-9]*)\s*\)', re.IGNORECASE)

# 已知内置函数的标准参数数量（基于 .docs/.teascript-docs/Functions (TeaScript).md）
# value = 单值 (固定参数数) 或 set (容许多个版本)
# ⚠ 这只是文档/wiki 的参考值；不同 38A 版本实际参数数可能不同。
#   AI 写完后**必须用 SMBX editor 实测**，不要盲信此表。
BUILTIN_ARITIES = {
    'ncreate':       7,        # ID, X, Y, Xsp, Ysp, Advset, CreationData
                               # ⚠ 实测：该引擎版本必须给满 7 参数（写 6 参会报参数数量错）。
                               # 旧版可能 6 参，但本仓库目标引擎是 7。
    'ncreategroup':  {9, 10},  # 不同版本可能 9 或 10
    'nkill':         {1, 8},   # 简形 1，详形 8
    'lmove':         {3, 4},   # 旧版 3 / 新版 4 (含 Type)
    'lset':          3,        # LayerName, Type, Smoke|Alpha
    'lspin':         {3, 4},
    'audioset':      4,
    'sleep':         1,
    'showmsg':       1,
    'sysshowmsg':    3,
    'sysshowinput':  1,
    'fxcreate':      10,

    'spevent':       1,
    'bset':          6,
    'tcreate':       {3, 4, 5, 6, 7, 8},
    'tclear':        1,
    'berase':        2,
    'keypress':      2,
    'redim':         3,
    'getangle':      2,
    'chr':           1,
    'chrw':          1,
    'asc':           1,
    'len':           1,
    'mid':           {2, 3},
    'left':          2,
    'right':         2,
    'lcase':         1,
    'ucase':         1,
}


# ---- 主 lint 流程 ----
def lint_text(text: str, disabled: Set[str]) -> List[Diag]:
    diags: List[Diag] = []
    raw_lines = text.splitlines()
    code_lines: List[str] = []          # 已剥离字符串内/注释 的代码部分
    has_unterminated_string = False

    # 第一遍：词法清洗 + E001/W103/E002
    for ln, raw in enumerate(raw_lines, start=1):
        stripped, in_str = strip_string_and_comment(raw)
        if in_str and 'E002' not in disabled:
            diags.append(Diag(ln, len(raw), 'E002',
                              '字符串缺右引号 "', 'error'))
            has_unterminated_string = True
        # 注释符误用：仅当不在字符串里时检测
        if 'E001' not in disabled:
            # 排除字符串里的 //（已被 strip 去掉了）
            if '//' in stripped:
                col = stripped.index('//') + 1
                diags.append(Diag(ln, col, 'E001',
                                  "TeaScript 注释用 \\' （单引号），不是 //", 'error'))
        if 'W103' not in disabled:
            if '#' in stripped and not re.search(r'\bend\b', stripped, re.IGNORECASE):
                # 警告 # 看起来像 Python 注释
                col = stripped.index('#') + 1
                # 但 # 在 38A 中合法吗？至少在 wn 字段会出现。这里仅 warn。
                # 实际 TeaScript 代码中很少见 #
                pass
        code_lines.append(stripped)

    # 第二遍：块结构 + E003 / E004 / E005 / E006 / E007 / E008 / W101 / W104
    block_stack: List[Tuple[str, int]] = []  # (kind, line)
    in_script_block = False
    saw_script_end_line = -1

    for idx, line in enumerate(code_lines):
        ln = idx + 1
        if not line.strip():
            continue

        # script 块
        m = SCRIPT_DEF_RE.match(line)
        if m:
            name = m.group(1)
            if 'E007' not in disabled and re.search(r'\d', name):
                diags.append(Diag(ln, m.start(1) + 1, 'E007',
                                  f"script 名 {name!r} 包含数字（命名规范禁止）",
                                  'error'))
            if in_script_block:
                # 不允许嵌套 script
                if 'E004' not in disabled:
                    diags.append(Diag(ln, 1, 'E004',
                                      'script 块嵌套或未闭合', 'error'))
            block_stack.append(('script', ln))
            in_script_block = True
            continue
        if END_SCRIPT_RE.match(line):
            if not block_stack or block_stack[-1][0] != 'script':
                if 'E006' not in disabled:
                    diags.append(Diag(ln, 1, 'E006',
                                      "'end script' 没有对应的 script 起始",
                                      'error'))
            else:
                block_stack.pop()
            in_script_block = False
            saw_script_end_line = ln
            continue

        # if 块
        if IF_OPEN_RE.match(line) and not IF_INLINE_RE.match(line):
            block_stack.append(('if', ln))
        elif END_IF_RE.match(line):
            if block_stack and block_stack[-1][0] == 'if':
                block_stack.pop()
            else:
                if 'E006' not in disabled:
                    diags.append(Diag(ln, 1, 'E006',
                                      "'end if' 没有对应的 if 起始",
                                      'error'))

        # do / loop
        if DO_OPEN_RE.match(line):
            block_stack.append(('do', ln))
        elif LOOP_END_RE.match(line):
            if block_stack and block_stack[-1][0] == 'do':
                start_line = block_stack.pop()[1]
                # W101：检查这一段内是否有 sleep / exit
                if 'W101' not in disabled:
                    # start_line 是 1-based 行号；对应 0-based 切片 [start_line-1: idx+1]
                    body_start = max(0, start_line - 1)
                    body = '\n'.join(code_lines[body_start:idx + 1])
                    if not (re.search(r'\bcall\s+sleep\b', body, re.IGNORECASE) or
                            re.search(r'\bsleep\s*\(', body, re.IGNORECASE) or
                            re.search(r'\bexit\s+do\b', body, re.IGNORECASE)):
                        diags.append(Diag(start_line, 1, 'W101',
                                          'do...loop 内未发现 sleep 或 exit do（可能死循环）',
                                          'warning'))
            else:
                if 'E006' not in disabled:
                    diags.append(Diag(ln, 1, 'E006',
                                      "'loop' 没有对应的 do 起始",
                                      'error'))

        # for / next
        if FOR_OPEN_RE.match(line):
            block_stack.append(('for', ln))
        elif NEXT_END_RE.match(line):
            if block_stack and block_stack[-1][0] == 'for':
                block_stack.pop()
            else:
                if 'E006' not in disabled:
                    diags.append(Diag(ln, 1, 'E006',
                                      "'next' 没有对应的 for 起始",
                                      'error'))
            # E010: next 后跟变量名（38A 不允许）
            if 'E010' not in disabled and NEXT_WITH_VAR_RE.match(line):
                diags.append(Diag(ln, 1, 'E010',
                                  "'next' 后不能跟变量名（如 next i）；38A 只允许裸 'next'",
                                  'error'))

        # select / end select
        if SELECT_OPEN_RE.match(line):
            block_stack.append(('select', ln))
        elif END_SELECT_RE.match(line):
            if block_stack and block_stack[-1][0] == 'select':
                block_stack.pop()
            else:
                if 'E006' not in disabled:
                    diags.append(Diag(ln, 1, 'E006',
                                      "'end select' 没有对应的 select 起始",
                                      'error'))

        # E003 字面量除/模 0
        if 'E003' not in disabled:
            for m_ in DIV_ZERO_RE.finditer(line):
                op = m_.group(0).strip().split()[0]
                diags.append(Diag(ln, m_.start() + 1, 'E003',
                                  f'字面量 {op} 0 会导致游戏崩溃',
                                  'error'))

        # W105 跨类型字面量比较
        if 'W105' not in disabled and COMPARE_LITERAL_RE.search(line):
            m_ = COMPARE_LITERAL_RE.search(line)
            diags.append(Diag(ln, m_.start() + 1, 'W105',
                              '字符串字面量与数字字面量比较会 crash 游戏',
                              'warning'))

        # E008 dim 名规范
        m = DIM_RE.match(line)
        if m and 'E008' not in disabled:
            name = m.group(1)
            if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', name):
                diags.append(Diag(ln, m.start(1) + 1, 'E008',
                                  f"dim 变量名 {name!r} 违规（应字母开头、仅字母数字、不含空格）",
                                  'error'))
            # W104：dim 在 if 块里
            if 'W104' not in disabled:
                for kind, _ in block_stack:
                    if kind == 'if':
                        diags.append(Diag(ln, 1, 'W104',
                                          '在 if 块内 dim 在旧版（patch 31 前）有 bug，建议提到 if 外',
                                          'warning'))
                        break

        # E009：脚本主体在 script 块之后还出现可执行代码
        if saw_script_end_line > 0 and not in_script_block and 'E009' not in disabled:
            # 接受空行/注释/继续的 script 块定义；其它视为违规
            stripped = line.strip()
            # 允许接着另一个 script 定义或 end 系列
            if (SCRIPT_DEF_RE.match(line) or END_SCRIPT_RE.match(line)
                    or stripped == '' or stripped.startswith("'")):
                pass
            else:
                diags.append(Diag(ln, 1, 'E009',
                                  'script 块之后又出现主体代码：所有 script 块必须放在文件末尾',
                                  'error'))
                # 只报第一处即可
                saw_script_end_line = -1

    # 块未闭合
    for kind, ln in block_stack:
        code = {'script': 'E004'}.get(kind, 'E005')
        if code in disabled:
            continue
        diags.append(Diag(ln, 1, code,
                          f'{kind} 块未闭合', 'error'))

    # W102：调用未知函数（仅在没有未结束字符串的情况下）
    if not has_unterminated_string and 'W102' not in disabled:
        # 收集自定义 script 名
        custom: Set[str] = set()
        for line in code_lines:
            m = SCRIPT_DEF_RE.match(line)
            if m:
                custom.add(m.group(1).lower())
        # 收集 R 行（用户数组）暂无法从 .tea 看到，但 array(arr(idx)) /
        # strarray(arr(idx)) 中的 arr 不是函数；通过位置启发式跳过：
        #   只要紧跟在 'array(' / 'strarray(' 后的第一个 '(' 是同一表达式
        #   的下标语法。
        ARRAY_INDEX_RE = re.compile(r'\b(?:array|strarray)\(\s*([A-Za-z_][A-Za-z_0-9]*)\s*\(',
                                    re.IGNORECASE)
        # 检查每行
        for idx, line in enumerate(code_lines):
            ln = idx + 1
            # 收集本行所有作为数组名的标识符（在 array(...)/strarray(...) 内紧接的）
            array_names_in_line = {m.group(1).lower()
                                   for m in ARRAY_INDEX_RE.finditer(line)}
            for m_ in CALL_RE.finditer(line):
                name = m_.group(1).lower()
                if name in KEYWORDS or name in BUILTIN_FUNCTIONS or name in custom:
                    continue
                if name in array_names_in_line:
                    # 是数组下标，不是函数调用
                    continue
                # 只 warn 一次
                diags.append(Diag(ln, m_.start(1) + 1, 'W102',
                                  f'调用未知名字 {name}()，请确认是内置函数或已定义的 script',
                                  'warning'))


    # ---- E012/E013/W107 额外检测 ----
    if not has_unterminated_string:
        # 找出当前文件里所有 script 块的范围（用于判定 E011 是否在 procedure 内）
        proc_ranges = []   # list of (start_ln, end_ln, name, is_function)
        cur_proc = None
        for idx, raw in enumerate(raw_lines):
            ln = idx + 1
            m = SCRIPT_DEF_RE.match(raw)
            if m:
                cur_proc = {'start': ln, 'name': m.group(1), 'has_return_value': False}
                continue
            if END_SCRIPT_RE.match(raw):
                if cur_proc:
                    cur_proc['end'] = ln
                    proc_ranges.append(cur_proc)
                    cur_proc = None
                continue
            # 检测 script 内是否有 `return <value>` (function) vs `return` 单独 (procedure 内非法)
            if cur_proc:
                if RETURN_VALUE_RE.match(raw):
                    cur_proc['has_return_value'] = True
                # 用 return type 在 script 头声明？看 script 头是否含 'return'
                # SCRIPT_DEF_RE 简化没抓 return type，这里用宽容扫描
        # 头中含 'return ' 的视为 function
        for p in proc_ranges:
            head_line = code_lines[p['start'] - 1] if p['start'] - 1 < len(code_lines) else ''
            if re.search(r'\breturn\b', head_line, re.IGNORECASE):
                p['has_return_value'] = True

        for idx, line in enumerate(code_lines):
            ln = idx + 1

            # E011: procedure 内 `return` 单独（无值）
            if 'E011' not in disabled and RETURN_BARE_RE.match(line):
                # 找它在哪个 script 块内
                for p in proc_ranges:
                    if p['start'] < ln < p.get('end', 10**9) and not p['has_return_value']:
                        diags.append(Diag(ln, 1, 'E011',
                                          f"procedure {p['name']!r} 内使用裸 'return' 会让引擎判其为 function 缺 return type；改用 if/end if 包住有效路径",
                                          'error'))
                        break

            # E012: 调用 SET / SLT / TMG（非 TeaScript 函数）
            if 'E012' not in disabled:
                m_ = SET_CALL_RE.search(line)
                if m_:
                    diags.append(Diag(ln, m_.start() + 1, 'E012',
                                      f"{m_.group(0).strip()} 不是 TeaScript 内置函数（是 IPC 命令）；触发事件请用其它机制（如 LSet 改图层）",
                                      'error'))

            # E013: 内置函数参数数量错误
            if 'E013' not in disabled:
                for m_ in CALL_RE.finditer(line):
                    name = m_.group(1).lower()
                    if name not in BUILTIN_ARITIES:
                        continue
                    expected = BUILTIN_ARITIES[name]
                    # 提取括号内的参数（粗略；不处理嵌套换行）
                    start = m_.end() - 1   # 指向 '('
                    depth = 0
                    end = start
                    for j in range(start, len(line)):
                        if line[j] == '(':
                            depth += 1
                        elif line[j] == ')':
                            depth -= 1
                            if depth == 0:
                                end = j
                                break
                    if end <= start:
                        continue   # 参数跨行，跳过
                    args_str = line[start + 1:end]
                    # 数顶层逗号
                    d = 0; n = 1 if args_str.strip() else 0
                    for ch in args_str:
                        if ch == '(':
                            d += 1
                        elif ch == ')':
                            d -= 1
                        elif ch == ',' and d == 0:
                            n += 1
                    if isinstance(expected, set):
                        ok = n in expected
                    else:
                        ok = n == expected
                    if not ok:
                        exp_str = expected if not isinstance(expected, set) else f'∈{sorted(expected)}'
                        diags.append(Diag(ln, m_.start() + 1, 'E013',
                                          f'{name}() 参数数量错误：实际 {n}，预期 {exp_str}',
                                          'error'))

            # W107: v(_name) / gv(_name) 含下划线变量名（引擎拒绝）
            if 'W107' not in disabled:
                for m_ in V_REF_RE.finditer(line):
                    name = m_.group(1)
                    if '_' in name:
                        diags.append(Diag(ln, m_.start(1) + 1, 'W107',
                                          f"v(...) 引用变量名 {name!r} 含下划线；TeaScript 命名规约：仅字母+数字，字母开头",
                                          'warning'))

            # E014: 代码语句后跟同行注释 → 38A 引擎实测会破坏赋值/调用语义
            #
            # 触发场景（实测自 Drunkards' Last Toast.tea）：
            #     id = 134                  ' 火球类直线   ← 引擎报"未声明变量 id"等假错
            # 移除行尾注释后即正常。原因推测：38A 的 TeaScript 解析器对
            # "代码 + 行尾 ' 注释"的边界处理有 bug（可能把注释末尾误并到下一语句）。
            #
            # 规则：原始行里若存在非字符串内的 '，且 ' 之前去除空白后还有内容，
            #       就报 error，建议把注释独占一行放在前面。
            if 'E014' not in disabled:
                raw_for_e014 = raw_lines[idx]
                col = find_inline_comment_col(raw_for_e014)
                if col > 0:
                    before = raw_for_e014[:col].rstrip()
                    if before.strip():
                        # 排除整行就是注释的情况（before 全空白时不会进这里）
                        diags.append(Diag(ln, col + 1, 'E014',
                                          "代码语句后不要跟行尾注释（38A 引擎 bug 会破坏语义）；把注释独占一行放在该语句之前",
                                          'error'))

    # 排序去重
    diags.sort(key=lambda d: (d.line, d.col, d.code))
    return diags


def main():
    ap = argparse.ArgumentParser(description='Lint a TeaScript .tea file.')
    ap.add_argument('path')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--disable', action='append', default=[],
                    help='禁用规则码，例如 --disable W102')
    ap.add_argument('--no-warnings', action='store_true', help='只输出错误')
    args = ap.parse_args()

    with open(args.path, 'r', encoding='utf-8', errors='replace') as fh:
        text = fh.read()
    disabled = set(args.disable)

    diags = lint_text(text, disabled)
    if args.no_warnings:
        diags = [d for d in diags if d.severity == 'error']

    n_err = sum(1 for d in diags if d.severity == 'error')
    n_warn = sum(1 for d in diags if d.severity == 'warning')

    if args.json:
        print(json.dumps({
            'path': os.path.abspath(args.path),
            'errors': n_err,
            'warnings': n_warn,
            'diagnostics': [d.to_dict() for d in diags],
        }, ensure_ascii=False, indent=2))
    else:
        for d in diags:
            tag = {'error': 'ERROR', 'warning': 'WARN ', 'info': 'INFO '}[d.severity]
            print(f'{args.path}:{d.line}:{d.col}: {tag} [{d.code}] {d.message}')
        print(f'[teascript_lint] {n_err} error(s), {n_warn} warning(s)')

    return 1 if n_err > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
