#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anim_lint.py — tea-anim-helper 动画契约静态校验器。

只做**与动画契约相关**的静态检查（专注高频致命问题与动画规约），无需 SMBX 引擎即可运行。

校验规则码：
    AE001  缺少必需的 Export Script 接口 (_Launch/_Tick/_Finish/_Length)
    AE002  接口签名不符合契约 (参数/返回类型)
    AE003  动画名不一致 (4 个接口前缀不统一)
    AE004  动画脚本内出现 call sleep —— 不得自驱动逐帧 (do/loop/for 允许, 但不能 sleep)
    AE005  使用 rnd (应改用 CUMath_Hash 以保证可复现/pure)
    AE006  bmp 申请/释放疑似不配对 (BmpNew 计数 > BmpDel/循环释放)
    AW101  在子过程/接口内部使用 dim (规约要求变量统一在脚本头部 dim)
    AW102  bmp id 疑似硬编码绝对值 (BmpNew(<数字>) 未走 offset)
    AW103  _Tick 内未发现时间归一化 (CUTimeCalcT / CUTimeSetStamp)
    AW104  可执行语句后存在行尾注释 (38A 引擎实测会触发假错; Dim 声明行不计)
    AW105  临时变量未使用 temp_ 前缀 (规约建议)

CLI:
    python anim_lint.py path/to/anim.tea
    python anim_lint.py path/to/anim.tea --json
    python anim_lint.py path/to/anim.tea --disable AW105
    python anim_lint.py path/to/anim.tea --no-warnings
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional


REQUIRED_SUFFIXES = ["Launch", "Tick", "Finish", "Length"]

# 期望签名（大小写不敏感, 空白宽松）
# _Launch(<p> As Long, Return Integer)
# _Tick(<p> As Double, Return Integer)
# _Finish(Return Integer)
# _Length(Return Double)
SIG_PATTERNS = {
    "Launch": re.compile(
        r"^\s*export\s+script\s+(\w+)_launch\s*\(\s*\w+\s+as\s+long\s*,\s*return\s+integer\s*\)\s*$",
        re.I,
    ),
    "Tick": re.compile(
        r"^\s*export\s+script\s+(\w+)_tick\s*\(\s*\w+\s+as\s+double\s*,\s*return\s+integer\s*\)\s*$",
        re.I,
    ),
    "Finish": re.compile(
        r"^\s*export\s+script\s+(\w+)_finish\s*\(\s*return\s+integer\s*\)\s*$",
        re.I,
    ),
    "Length": re.compile(
        r"^\s*export\s+script\s+(\w+)_length\s*\(\s*return\s+double\s*\)\s*$",
        re.I,
    ),
}

# 任意 (export) script 头, 用于定位接口存在性 + 提取名字
ANY_SCRIPT_HEAD = re.compile(r"^\s*(?:export\s+)?script\s+(\w+)\s*\(", re.I)
SCRIPT_END = re.compile(r"^\s*end\s+script\s*$", re.I)

WARN_PREFIX = "AW"


@dataclass
class Finding:
    line: int
    col: int
    code: str
    msg: str

    @property
    def is_warning(self) -> bool:
        return self.code.startswith(WARN_PREFIX)


def _strip_comment(line: str) -> str:
    """去掉 TeaScript 行注释 (' 之后), 不考虑字符串内的引号转义 (启发式)。"""
    out = []
    in_str = False
    for ch in line:
        if ch == '"':
            in_str = not in_str
        if ch == "'" and not in_str:
            break
        out.append(ch)
    return "".join(out)


def _has_trailing_comment(line: str) -> Optional[int]:
    """若代码语句后有行尾注释, 返回 ' 的列号(1-based), 否则 None。整行注释/空白前注释不算。"""
    in_str = False
    seen_code = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_str = not in_str
            seen_code = True
            continue
        if ch == "'" and not in_str:
            # 前面是否有非空白代码
            if seen_code:
                return i + 1
            return None
        if not ch.isspace():
            seen_code = True
    return None


def lint(text: str) -> List[Finding]:
    findings: List[Finding] = []
    raw_lines = text.splitlines()

    # ---------- 接口存在性 + 签名 + 命名一致性 ----------
    found_suffix_line = {}   # suffix -> line no (任意大小写匹配到的 (export) script X_suffix)
    sig_ok = {}              # suffix -> bool
    names = {}               # suffix -> animation name

    suffix_head_re = {
        s: re.compile(r"^\s*(?:export\s+)?script\s+(\w+)_" + s + r"\s*\(", re.I)
        for s in REQUIRED_SUFFIXES
    }

    for i, raw in enumerate(raw_lines, start=1):
        code = _strip_comment(raw)
        for s in REQUIRED_SUFFIXES:
            m = suffix_head_re[s].match(code)
            if m:
                found_suffix_line.setdefault(s, i)
                names.setdefault(s, m.group(1))
                # 校验是否 export + 精确签名
                if SIG_PATTERNS[s].match(code):
                    sig_ok[s] = True
                else:
                    sig_ok.setdefault(s, False)

    for s in REQUIRED_SUFFIXES:
        if s not in found_suffix_line:
            findings.append(
                Finding(0, 0, "AE001",
                        f"缺少必需接口 Export Script <Name>_{s}(...)")
            )
        else:
            if not sig_ok.get(s, False):
                findings.append(
                    Finding(found_suffix_line[s], 1, "AE002",
                            f"接口 _{s} 签名不符契约 (须为 Export Script, "
                            f"且参数/返回类型严格匹配)")
                )

    # 命名一致性
    distinct = set(names.values())
    if len(distinct) > 1:
        findings.append(
            Finding(0, 0, "AE003",
                    f"4 个接口动画名不一致: {sorted(distinct)} —— 应统一前缀")
        )

    # ---------- 逐行规则 ----------
    bmp_new_cnt = 0
    bmp_del_cnt = 0
    has_del_loop = False        # 是否存在 For ... BmpDel 的循环释放
    tick_body_lines: List[str] = []
    in_tick = False
    tick_name = names.get("Tick")

    # 记录当前是否在某个 script 块内部 (用于 dim 位置检查)
    in_script_block = False

    for i, raw in enumerate(raw_lines, start=1):
        code = _strip_comment(raw).rstrip()
        low = code.lower().strip()

        # script 块进出
        if ANY_SCRIPT_HEAD.match(code):
            in_script_block = True
            # 是否进入 _Tick
            if tick_name and re.match(
                r"^\s*(?:export\s+)?script\s+" + re.escape(tick_name) + r"_tick\s*\(",
                code, re.I,
            ):
                in_tick = True
        elif SCRIPT_END.match(code):
            in_script_block = False
            in_tick = False

        # 收集 tick 主体
        if in_tick and not ANY_SCRIPT_HEAD.match(code):
            tick_body_lines.append(low)

        # AE004 自驱动: 仅禁 call sleep (do/loop/for 允许, 用于批量建 bmp / 遍历)
        if re.search(r"\bcall\s+sleep\s*\(", low) or re.search(r"\bsleep\s*\(", low):
            findings.append(
                Finding(i, 1, "AE004",
                        "动画脚本内禁止 sleep (不得自驱动逐帧; do/loop/for 可用但不能 sleep)")
            )

        # AE005 rnd
        if re.search(r"(?<![a-z0-9_])rnd(?![a-z0-9_])", low):
            findings.append(
                Finding(i, 1, "AE005",
                        "禁用 rnd, 请改用 CUMath_Hash(seed) 以保证可复现/pure")
            )

        # bmp 申请/释放计数
        for _m in re.finditer(r"\bbmpnew\s*\(", low):
            bmp_new_cnt += 1
        for _m in re.finditer(r"\bbmpdel\s*\(", low):
            bmp_del_cnt += 1
        if re.search(r"\bfor\b.*\bto\b", low):
            # 粗略: for 循环后续是否出现 bmpdel —— 简化为标记存在 for 且文件含 bmpdel
            pass
        if re.search(r"\bbmpdel\s*\(", low) and re.search(r"step|to|_bmpcnt", text.lower()):
            has_del_loop = True

        # AW101 内部 dim
        if in_script_block and re.match(r"^\s*dim\b", low):
            findings.append(
                Finding(i, 1, "AW101",
                        "子过程/接口内部 dim —— 规约要求变量统一在脚本头部 dim")
            )

        # AW102 硬编码绝对 bmp id
        m = re.search(r"\bbmpnew\s*\(\s*(\d+)\s*\)", low)
        if m:
            findings.append(
                Finding(i, 1, "AW102",
                        f"BmpNew({m.group(1)}) 疑似硬编码绝对 bmp id, "
                        f"应使用 <Name>_offset + k")
            )

        # AW104 行尾注释 (仅可执行语句; Dim 声明行的行尾注释在实践中可用, 模范案例亦如此, 跳过)
        if not re.match(r"^\s*dim\b", low):
            tc = _has_trailing_comment(raw)
            if tc is not None:
                findings.append(
                    Finding(i, tc, "AW104",
                            "可执行语句后跟行尾注释 (38A 实测会触发假错), 请让注释独占一行")
                )

        # AW105 temp 变量前缀 (仅检查头部 dim 的疑似临时变量)
        if not in_script_block:
            dm = re.match(r"^\s*dim\s+(\w+)\s+as\b", low)
            if dm:
                vname = dm.group(1)
                if re.search(r"(temp|tmp)", vname) and not vname.startswith("temp_"):
                    findings.append(
                        Finding(i, 1, "AW105",
                                f"临时变量 '{vname}' 建议用 temp_ 前缀")
                    )

    # AE006 申请/释放配对
    if bmp_new_cnt > 0 and bmp_del_cnt == 0 and not has_del_loop:
        findings.append(
            Finding(0, 0, "AE006",
                    f"检测到 {bmp_new_cnt} 处 BmpNew 但未见 BmpDel —— "
                    f"_Finish 必须释放所申请的 bmp")
        )

    # AW103 _Tick 缺时间归一化
    if "Tick" in found_suffix_line:
        joined = "\n".join(tick_body_lines)
        if "cutimecalct" not in joined and "cutimesetstamp" not in joined:
            findings.append(
                Finding(found_suffix_line["Tick"], 1, "AW103",
                        "_Tick 内未发现 CUTimeCalcT/CUTimeSetStamp 时间归一化 "
                        "(若有意为之可忽略)")
            )

    findings.sort(key=lambda f: (f.line, f.col, f.code))
    return findings


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Lint a tea-anim-helper animation .tea file.")
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--disable", default="", help="逗号分隔的规则码, 例如 --disable AW105,AW104")
    ap.add_argument("--no-warnings", action="store_true")
    args = ap.parse_args(argv)

    try:
        with open(args.path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(f"无法读取文件: {e}", file=sys.stderr)
        return 2

    disabled = {c.strip().upper() for c in args.disable.split(",") if c.strip()}
    findings = [f for f in lint(text) if f.code not in disabled]
    if args.no_warnings:
        findings = [f for f in findings if not f.is_warning]

    errors = [f for f in findings if not f.is_warning]
    warnings = [f for f in findings if f.is_warning]

    if args.json:
        print(json.dumps({
            "path": args.path,
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [asdict(f) for f in findings],
        }, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            loc = f"{f.line}:{f.col}" if f.line else "-"
            kind = "warning" if f.is_warning else "error"
            print(f"{args.path}:{loc}: {kind} {f.code}: {f.msg}")
        print(f"\n== {len(errors)} error(s), {len(warnings)} warning(s) ==")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
