#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_var_check.py — 校验 lvl 内嵌脚本里的 user variable 引用是否都在 V 行预声明。

⚠️ 经实测：38A 引擎对 v(name) 的处理是**严格模式**——脚本里用到的每个 v(name)
   都必须在 lvl 的 V 行声明，否则脚本编译失败。

用法：
    python lvl_var_check.py path/to/level.lvl
    python lvl_var_check.py path/to/level.lvl --fix       # 自动补上缺失的 V 行
    python lvl_var_check.py path/to/level.lvl --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Set

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lvlfile import (SMBXFile, Entry, url_decode, url_encode,  # noqa
                     b64_decode_text, b64_decode_script)


V_REF_RE = re.compile(
    r'\b(?:v|gv|str|gstr|val|gval)\(\s*([A-Za-z_][A-Za-z_0-9]*)\s*\)',
    re.IGNORECASE)
ARRAY_REF_RE = re.compile(
    r'\b(?:array|strarray)\(\s*([A-Za-z_][A-Za-z_0-9]*)',
    re.IGNORECASE)


def collect_declared_vars(f: SMBXFile) -> Set[str]:
    """从 V 行（标量变量）+ R 行（用户数组）收集已声明的名字（小写）。"""
    decl = set()
    for e in f.entries:
        if e.marker == 'V' and e.fields:
            name = url_decode(e.fields[0])
            decl.add(name.lower())
        elif e.marker == 'R' and e.fields:
            # R 行一行声明多个数组：R|arr1|arr2|...
            for fld in e.fields:
                if fld:
                    name = url_decode(fld)
                    decl.add(name.lower())
    return decl



def _strip_comments_and_strings(body: str) -> str:
    """剔除 TeaScript 注释（'..）与字符串字面量内容，避免误抓注释里的 v(...)。
    采用逐行处理；行内出现非字符串里的 ' 之后都视为注释。"""
    out_lines = []
    for raw in body.splitlines():
        buf = []
        in_str = False
        i, n = 0, len(raw)
        while i < n:
            ch = raw[i]
            if in_str:
                if ch == '"':
                    in_str = False
                # 字符串内容用空格替代，保持列对齐
                buf.append(' ')
            else:
                if ch == '"':
                    in_str = True
                    buf.append(' ')
                elif ch == "'":
                    break  # 注释开始，丢弃后续
                else:
                    buf.append(ch)
            i += 1
        out_lines.append(''.join(buf))
    return '\n'.join(out_lines)


def collect_referenced_vars(f: SMBXFile) -> Set[str]:
    """从所有嵌入脚本里收集 v(name) 引用的变量名（小写）。
    自动跳过注释与字符串字面量。"""
    refs = set()
    for e in f.entries:
        if e.marker not in ('S', 'Su', 'SU', 'GS', 'GSu', 'GSU'):
            continue
        if not e.fields or len(e.fields) < 2:
            continue
        body_enc = e.fields[1]
        # 用 b64_decode_script，对 Su/GSu 也按 UTF-8 优先解码（保留中文注释/字符串），
        # 不会被 ASCII codec 替换成 \ufffd 后丢失变量引用周围的上下文。
        try:
            body = b64_decode_script(body_enc, e.marker)
        except Exception:
            continue
        clean = _strip_comments_and_strings(body)
        for m in V_REF_RE.finditer(clean):
            refs.add(m.group(1).lower())
        for m in ARRAY_REF_RE.finditer(clean):
            refs.add(m.group(1).lower())
    return refs


def main():
    ap = argparse.ArgumentParser(description='Validate that all v(name) references in embedded scripts are declared as V rows.')
    ap.add_argument('path')
    ap.add_argument('--fix', action='store_true',
                    help='自动补上缺失的 V 行（输出到 <path>.modified.lvl 或 --output 指定路径）')
    ap.add_argument('-o', '--output')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    f = SMBXFile.load(args.path)
    declared = collect_declared_vars(f)
    referenced = collect_referenced_vars(f)
    missing = sorted(referenced - declared)
    unused = sorted(declared - referenced)
    invalid_names = [n for n in missing if not re.match(r'^[a-z][a-z0-9]*$', n)]

    if args.json:
        print(json.dumps({
            'path': os.path.abspath(args.path),
            'declared': sorted(declared),
            'referenced': sorted(referenced),
            'missing_in_V': missing,
            'unused_V_rows': unused,
            'invalid_names': invalid_names,
        }, ensure_ascii=False, indent=2))
        return 1 if missing else 0

    print(f'[lvl_var_check] {args.path}')
    print(f'  declared (V rows):     {len(declared)}')
    print(f'  referenced (in tea):   {len(referenced)}')
    if missing:
        print(f'  ❌ MISSING (need V row): {missing}')
    if invalid_names:
        print(f'  ❌ INVALID names (含下划线/数字开头): {invalid_names}')
    if unused:
        print(f'  ⚠ unused V rows: {unused}')
    if not missing and not invalid_names:
        print(f'  ✅ all good')

    if args.fix and missing:
        if invalid_names:
            print(f'[lvl_var_check] 拒绝自动修复——{invalid_names!r} 含非法变量名（请先在 .tea 里改名）',
                  file=sys.stderr)
            return 2
        # 在最后一个 V 行后插入；若没有 V 行则插入到 L 行后或文件末尾
        insert_idx = None
        for i, e in enumerate(f.entries):
            if e.marker == 'V':
                insert_idx = i + 1
        if insert_idx is None:
            for i, e in enumerate(f.entries):
                if e.marker == 'L':
                    insert_idx = i + 1
        if insert_idx is None:
            insert_idx = len(f.entries)
        for name in missing:
            new_e = Entry(marker='V', fields=[url_encode(name), '0', '0'])
            f.entries.insert(insert_idx, new_e)
            insert_idx += 1
        out = args.output or _default_out(args.path)
        f.save(out)
        print(f'[lvl_var_check] added {len(missing)} V row(s); saved -> {out}')

    return 1 if missing else 0


def _default_out(in_path):
    base, ext = os.path.splitext(in_path)
    return base + '.modified' + ext


if __name__ == '__main__':
    sys.exit(main())
