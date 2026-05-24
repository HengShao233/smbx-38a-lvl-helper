#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_scripts.py — 提取 / 列出 / 注入 .lvl/.wls 中嵌入的 TeaScript 脚本。

支持 marker：
    LVL: S (UTF-8) / Su (ASCII)
    WLS: GS (UTF-8) / GSu (ASCII)

用法：
    # 列出脚本
    python lvl_scripts.py list <file>

    # 提取所有脚本到目录（生成每个脚本的 .tea 文件 + index.json）
    python lvl_scripts.py extract <file> -o <out_dir>

    # 把目录里的 .tea 文件按 index.json 写回（生成新 lvl）
    python lvl_scripts.py inject <file> -i <in_dir> -o <out_file>

    # 单个脚本提取（直接打印到 stdout）
    python lvl_scripts.py cat <file> --name "MyScript"

index.json 结构：
[
  {"i": 132, "marker": "S", "name": "MyScript", "filename": "MyScript.tea", "encoding": "utf-8"},
  ...
]

`inject` 时按 index.json 的 marker 与 i 索引精确写回；如果用户新增了文件而未更新 index.json，
默认忽略新增。
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lvlfile import (SMBXFile, url_decode, url_encode,
                     b64_decode_text, b64_encode_text,
                     b64_encode_script, pick_script_marker)


SCRIPT_MARKERS = ('S', 'Su', 'SU', 'GS', 'GSu', 'GSU')


def safe_filename(name: str) -> str:
    bad = '<>:"/\\|?*'
    out = []
    for ch in name:
        if ch in bad or ord(ch) < 32:
            out.append('_')
        else:
            out.append(ch)
    s = ''.join(out).strip().rstrip('.')
    return s or 'unnamed'


def cmd_list(args):
    f = SMBXFile.load(args.path)
    rows = []
    for i, e, name, body in f.iter_scripts():
        rows.append({
            'i': i, 'marker': e.marker, 'name': name,
            'lines': body.count('\n') + (1 if body else 0),
            'chars': len(body),
        })
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(f'[lvl_scripts] {len(rows)} scripts in {args.path}')
        for r in rows:
            print(f"  [{r['i']:>4}] {r['marker']:<3}  name={r['name']!r}  "
                  f"lines={r['lines']}  chars={r['chars']}")
    return 0


def cmd_extract(args):
    f = SMBXFile.load(args.path)
    out_dir = args.output
    os.makedirs(out_dir, exist_ok=True)
    index = []
    for i, e, name, body in f.iter_scripts():
        encoding = 'utf-8' if e.marker in ('S', 'GS') else 'ascii'
        # 文件名：<i>_<safe(name)>.tea，前置 i 保证可恢复 + 防重名
        fn = f"{i:04d}_{safe_filename(name) or 'unnamed'}.tea"
        path = os.path.join(out_dir, fn)
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(body)
        index.append({
            'i': i,
            'marker': e.marker,
            'name': name,
            'filename': fn,
            'encoding': encoding,
        })
    with open(os.path.join(out_dir, 'index.json'), 'w', encoding='utf-8') as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)
    print(f'[lvl_scripts] extracted {len(index)} scripts to {out_dir}')
    for r in index:
        print(f"  [{r['i']:>4}] {r['marker']:<3}  -> {r['filename']}")
    return 0


def cmd_inject(args):
    in_dir = args.input
    src = args.path
    dst = args.output
    if not dst:
        base, ext = os.path.splitext(src)
        dst = base + '.modified' + ext

    idx_path = os.path.join(in_dir, 'index.json')
    if not os.path.isfile(idx_path):
        print(f'[lvl_scripts] ERROR: missing index.json in {in_dir}', file=sys.stderr)
        return 2
    with open(idx_path, 'r', encoding='utf-8') as fh:
        index = json.load(fh)

    f = SMBXFile.load(src)
    n_changed = 0
    for rec in index:
        i = rec['i']
        if i >= len(f.entries):
            print(f'[lvl_scripts] WARN: index {i} out of range', file=sys.stderr)
            continue
        e = f.entries[i]
        if e.marker != rec['marker']:
            print(f'[lvl_scripts] WARN: marker mismatch at i={i}: '
                  f'expected {rec["marker"]}, got {e.marker}', file=sys.stderr)
            continue
        body_path = os.path.join(in_dir, rec['filename'])
        if not os.path.isfile(body_path):
            print(f'[lvl_scripts] WARN: missing body file {body_path}', file=sys.stderr)
            continue
        with open(body_path, 'r', encoding='utf-8', newline='') as fh:
            body = fh.read()
        # ⚠ 38A 引擎期望大写 SU/GSU + GBK 字节。若 body 含非 ASCII，自动升级 marker。
        has_non_ascii = any(ord(ch) > 127 for ch in body)
        if has_non_ascii:
            old = e.marker
            if e.marker.upper().startswith('GS'):
                e.marker = 'GSU'
            else:
                e.marker = 'SU'
            if old != e.marker:
                print(f'[lvl_scripts] auto-upgraded marker {old} -> {e.marker} at i={i} (script contains non-ASCII)')
        # 编码侧统一用 b64_encode_script（默认 GBK 字节，与 38A 引擎期望一致）
        new_b64 = b64_encode_script(body)
        if e.get(1, '') != new_b64:
            e.set(1, new_b64)
            n_changed += 1
    f.save(dst)
    print(f'[lvl_scripts] injected {n_changed} script(s); saved to {dst}')
    return 0


def cmd_cat(args):
    f = SMBXFile.load(args.path)
    target = args.name
    found = []
    for i, e, name, body in f.iter_scripts():
        if name == target or url_encode(name) == target:
            found.append((i, e.marker, body))
    if not found:
        print(f'[lvl_scripts] no script named {target!r}', file=sys.stderr)
        return 1
    if len(found) > 1:
        print(f'[lvl_scripts] WARN: {len(found)} scripts named {target!r}, printing first',
              file=sys.stderr)
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sys.stdout.write(found[0][2])
    return 0


def main():
    ap = argparse.ArgumentParser(description='Manage embedded TeaScript blocks in 38A files.')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('list', help='列出所有嵌入脚本')
    p.add_argument('path')
    p.add_argument('--json', action='store_true')
    p.set_defaults(func=cmd_list)

    p = sub.add_parser('extract', help='把所有脚本解码后导出到目录')
    p.add_argument('path')
    p.add_argument('-o', '--output', required=True, help='输出目录')
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser('inject', help='把目录里的脚本写回到新文件')
    p.add_argument('path', help='原 lvl/wls 文件')
    p.add_argument('-i', '--input', required=True, help='含 index.json 的目录')
    p.add_argument('-o', '--output', help='输出新文件路径；默认 <name>.modified.<ext>')
    p.set_defaults(func=cmd_inject)

    p = sub.add_parser('cat', help='打印指定名字的单个脚本')
    p.add_argument('path')
    p.add_argument('--name', required=True)
    p.set_defaults(func=cmd_cat)

    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
