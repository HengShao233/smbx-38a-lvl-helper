#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teascript_inject.py — 把 .tea 文件嵌入到 .lvl 或 .wls 作为 S/Su/GS/GSu 行。

用法：
    # 将 my.tea 作为 lvl 的脚本 'MyScript' 嵌入（默认 marker=S, UTF-8）
    python teascript_inject.py path/to/level.lvl --tea my.tea --name MyScript -o out.lvl

    # 替换已存在的同名脚本（默认行为是若同名存在则替换；--add-only 则报错）
    python teascript_inject.py path/to/level.lvl --tea my.tea --name MyScript --add-only -o out.lvl

    # 嵌入 ASCII 模式（Su / GSu）
    python teascript_inject.py path/to/level.lvl --tea my.tea --name MyScript --ascii -o out.lvl

    # 嵌入到 .wls 全局脚本
    python teascript_inject.py path/to/world.wls --tea my.tea --name MyGlobal -o out.wls

    # 删除指定脚本
    python teascript_inject.py path/to/level.lvl --remove --name MyScript -o out.lvl

    # 列出脚本（等价于 smbx-38a/lvl_scripts list）
    python teascript_inject.py path/to/level.lvl --list

依赖：
    复用 ../smbx-38a/scripts/lvlfile.py
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SMBX38A_SCRIPTS = os.path.abspath(os.path.join(HERE, '..', '..', 'smbx-38a', 'scripts'))
sys.path.insert(0, SMBX38A_SCRIPTS)

try:
    from lvlfile import (SMBXFile, Entry, url_encode, url_decode,
                         b64_encode_text, b64_decode_text)
except ImportError as e:
    sys.stderr.write(
        f'[teascript_inject] 找不到 smbx-38a skill 的 lvlfile.py（路径：{SMBX38A_SCRIPTS}）。\n'
        '请确认 smbx-38a skill 与 teascript-helper skill 共存于同一仓库。\n'
        f'原始错误：{e}\n')
    sys.exit(2)


def determine_marker(kind: str, ascii_mode: bool) -> str:
    """根据 lvl/wls 与 ascii 标志选 marker。"""
    if kind == 'wls':
        return 'GSu' if ascii_mode else 'GS'
    return 'Su' if ascii_mode else 'S'


def script_marker_set(kind: str):
    if kind == 'wls':
        return ('GS', 'GSu')
    return ('S', 'Su')


def find_script_by_name(f: SMBXFile, name: str):
    """返回 (idx, entry) or (None, None)。"""
    markers = script_marker_set(f.kind)
    for i, e in enumerate(f.entries):
        if e.marker in markers and url_decode(e.get(0, '')) == name:
            return i, e
    return None, None


def cmd_list(args):
    f = SMBXFile.load(args.path)
    rows = list(f.iter_scripts())
    if not rows:
        print(f'[teascript_inject] no embedded scripts in {args.path}')
        return 0
    print(f'[teascript_inject] {len(rows)} script(s) in {args.path}:')
    for i, e, name, body in rows:
        print(f'  [{i:>4}] {e.marker:<3}  {name!r}  '
              f'lines={body.count(chr(10)) + (1 if body else 0)}  chars={len(body)}')
    return 0


def cmd_remove(args):
    if not args.name:
        sys.stderr.write('--remove 需要 --name\n'); return 2
    f = SMBXFile.load(args.path)
    idx, e = find_script_by_name(f, args.name)
    if idx is None:
        sys.stderr.write(f'未找到名为 {args.name!r} 的脚本\n'); return 1
    del f.entries[idx]
    out = args.output or _default_out(args.path)
    f.save(out)
    print(f'[teascript_inject] removed {args.name!r} (was at index {idx}); saved -> {out}')
    return 0


def cmd_inject(args):
    if not args.tea or not args.name:
        sys.stderr.write('需要 --tea 与 --name\n'); return 2
    if not os.path.isfile(args.tea):
        sys.stderr.write(f'.tea 文件不存在：{args.tea}\n'); return 2

    with open(args.tea, 'r', encoding='utf-8', newline='') as fh:
        body = fh.read()

    f = SMBXFile.load(args.path)
    desired_marker = determine_marker(f.kind, args.ascii)
    encoding = 'ascii' if args.ascii else 'utf-8'
    encoded = b64_encode_text(body, encoding)
    name_enc = url_encode(args.name)

    idx, existing = find_script_by_name(f, args.name)
    if existing is not None:
        if args.add_only:
            sys.stderr.write(f'同名脚本 {args.name!r} 已存在；--add-only 阻止替换\n')
            return 1
        # 保持原来的 marker（除非用户用 --force-marker 强制改）
        if not args.force_marker and existing.marker != desired_marker:
            print(f'[teascript_inject] 注意：保持原 marker {existing.marker}（与 --ascii/--utf8 选项不同）。'
                  f'若要切换 marker 请加 --force-marker。', file=sys.stderr)
            desired_marker = existing.marker
            encoding = 'ascii' if existing.marker in ('Su', 'GSu') else 'utf-8'
            encoded = b64_encode_text(body, encoding)
        f.entries[idx] = Entry(marker=desired_marker, fields=[name_enc, encoded])
        action = 'replaced'
    else:
        new_entry = Entry(marker=desired_marker, fields=[name_enc, encoded])
        # 优先插入到现有 S/Su 块末尾
        new_idx = f.add(new_entry)
        action = 'added'
        idx = new_idx

    out = args.output or _default_out(args.path)
    f.save(out)
    print(f'[teascript_inject] {action} {desired_marker} script {args.name!r} '
          f'(index={idx}, body={len(body)} chars, base64={len(encoded)} chars); saved -> {out}')
    return 0


def _default_out(in_path: str) -> str:
    base, ext = os.path.splitext(in_path)
    return base + '.modified' + ext


def main():
    ap = argparse.ArgumentParser(description='Inject / replace / remove TeaScript blocks in .lvl/.wls.')
    ap.add_argument('path', help='lvl 或 wls 文件')
    ap.add_argument('--tea', help='要嵌入的 .tea 文件路径')
    ap.add_argument('--name', help='脚本名（必须满足变量命名规范）')
    ap.add_argument('-o', '--output', help='输出路径；默认 <name>.modified.<ext>')
    ap.add_argument('--ascii', action='store_true', help='使用 Su/GSu（ASCII 模式）')
    ap.add_argument('--add-only', action='store_true', help='同名存在时报错，不替换')
    ap.add_argument('--force-marker', action='store_true', help='替换时强制更换 marker')
    ap.add_argument('--list', action='store_true', help='仅列出脚本')
    ap.add_argument('--remove', action='store_true', help='删除 --name 指定的脚本')
    args = ap.parse_args()

    if args.list:
        return cmd_list(args)
    if args.remove:
        return cmd_remove(args)
    return cmd_inject(args)


if __name__ == '__main__':
    sys.exit(main())
