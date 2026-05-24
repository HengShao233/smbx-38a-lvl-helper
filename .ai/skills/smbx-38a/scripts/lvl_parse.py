#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_parse.py — 解析 .lvl/.wld/.wls 文件并输出摘要 / 完整 JSON。

Usage:
    python lvl_parse.py <path>                    # 默认 --summary
    python lvl_parse.py <path> --summary
    python lvl_parse.py <path> --json             # 整文件转 JSON（含每行 marker+fields）
    python lvl_parse.py <path> --json -o out.json
"""
import argparse
import json
import os
import sys

# 让脚本可独立运行
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lvlfile import SMBXFile, LVL_FIELD_NAMES, WLD_FIELD_NAMES, WLS_FIELD_NAMES, url_decode


def main():
    ap = argparse.ArgumentParser(description='Parse SMBX 38A .lvl/.wld/.wls files.')
    ap.add_argument('path')
    ap.add_argument('--summary', action='store_true', help='打印高层摘要（默认）')
    ap.add_argument('--json', action='store_true', help='输出每行的 JSON 表示')
    ap.add_argument('-o', '--output', help='输出路径；不指定则打印到 stdout')
    ap.add_argument('--decode-strings', action='store_true',
                    help='对常见字符串字段做 url-decode（仅用于阅读）')
    args = ap.parse_args()

    if not args.summary and not args.json:
        args.summary = True

    f = SMBXFile.load(args.path)

    if args.summary:
        s = f.summary()
        out = json.dumps(s, ensure_ascii=False, indent=2)
        _emit(out, args.output)
        return 0

    # full json
    name_map = {'lvl': LVL_FIELD_NAMES, 'wld': WLD_FIELD_NAMES, 'wls': WLS_FIELD_NAMES}.get(f.kind, {})
    data = {
        'meta': {
            'path': os.path.abspath(args.path),
            'kind': f.kind, 'version': f.version,
            'newline': 'CRLF' if f.newline == '\r\n' else 'LF',
            'encoding': f.encoding,
        },
        'entries': [],
    }
    for i, e in enumerate(f.entries):
        item = {'i': i, 'marker': e.marker, 'fields': list(e.fields)}
        if args.decode_strings:
            # 给已知 marker 增加可读名字与解码后的 string 字段
            field_names = name_map.get(e.marker)
            if field_names:
                named = {}
                for j, name in enumerate(field_names):
                    if j < len(e.fields):
                        named[name] = e.fields[j]
                item['named'] = named
            # 脚本特殊处理
            if e.marker in ('S', 'Su', 'GS', 'GSu'):
                item['decoded_name'] = url_decode(e.get(0, ''))
        data['entries'].append(item)
    _emit(json.dumps(data, ensure_ascii=False, indent=2), args.output)
    return 0


def _emit(text: str, output: str = None) -> None:
    if output:
        os.makedirs(os.path.dirname(os.path.abspath(output)) or '.', exist_ok=True)
        with open(output, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print(f'[lvl_parse] wrote {output} ({len(text)} chars)')
    else:
        # stdout 用 utf-8
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
        print(text)


if __name__ == '__main__':
    sys.exit(main())
