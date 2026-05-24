#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teascript_format.py — TeaScript 格式整理（不重排语义）。

规则：
- Tab 替换为 4 空格
- 行尾去除多余空白
- 文件末尾统一一个换行符
- 行尾换行符统一为 LF（嵌入 lvl 后会被 base64 包裹，不影响 lvl 行尾）
- 不改动注释 / 字符串内部内容

用法：
    python teascript_format.py path/to/x.tea            # 输出到 stdout
    python teascript_format.py path/to/x.tea -o out.tea
    python teascript_format.py path/to/x.tea --inplace
    python teascript_format.py --check path/to/x.tea    # 仅检查（不写入）；返回 1 表示需要格式化
"""
import argparse
import os
import sys


def format_text(text: str) -> str:
    # 统一换行
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    out_lines = []
    for line in text.split('\n'):
        # tab -> 4 spaces
        line = line.expandtabs(4)
        # 去除尾随空白
        line = line.rstrip()
        out_lines.append(line)
    # 去除文件尾的多余空行
    while out_lines and out_lines[-1] == '':
        out_lines.pop()
    return '\n'.join(out_lines) + '\n'


def main():
    ap = argparse.ArgumentParser(description='Format TeaScript .tea files.')
    ap.add_argument('path')
    ap.add_argument('-o', '--output', help='输出路径')
    ap.add_argument('--inplace', action='store_true')
    ap.add_argument('--check', action='store_true', help='仅检查；exit 1 = 需要格式化')
    args = ap.parse_args()

    with open(args.path, 'r', encoding='utf-8', errors='replace', newline='') as fh:
        original = fh.read()
    formatted = format_text(original)

    if args.check:
        if formatted != original.replace('\r\n', '\n').replace('\r', '\n'):
            print(f'[teascript_format] {args.path}: needs formatting')
            return 1
        print(f'[teascript_format] {args.path}: OK')
        return 0

    out = args.path if args.inplace else args.output
    if out:
        with open(out, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(formatted)
        print(f'[teascript_format] wrote {out}')
    else:
        try:
            sys.stdout.reconfigure(encoding='utf-8', newline='\n')
        except Exception:
            pass
        sys.stdout.write(formatted)
    return 0


if __name__ == '__main__':
    sys.exit(main())
