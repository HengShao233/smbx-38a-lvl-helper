#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teascript_event.py — 在 .lvl 中创建/修改事件，并把它绑定到一段 TeaScript。

E 行字段（spec 1.12）:
    E|name|msg|ea|el|elm|epy|eps|eef|ecn|evc|ene

各子字段最简形态：
    name  = url_encode(eventName)
    msg   = (空)
    ea    = "0,"                       不自动启动
    el    = "0///"                     无图层操作
    elm   = (空)
    epy   = "0,0,0,0,0,0,0,0,0,0,0,0"  默认控制
    eps   = "//"                       无 section/bg/music 编辑
    eef   = "0/0"                      无音效/特效
    ecn   = (空)
    evc   = (空)
    ene   = ",0/0,0,0,0,0//<scriptName>"   绑定脚本

支持自动启动：--autostart 0|1|2|3
    0 = 不自动
    1 = level start 时自动
    2 = 满足条件时自动
    3 = 被 call 时检查条件

用法：
    # 创建 / 复用事件 'OnFoo'，绑定到脚本 'MyScript'
    python teascript_event.py path/to/level.lvl --event OnFoo --script MyScript -o out.lvl

    # 让事件在关卡开始时自动触发
    python teascript_event.py path/to/level.lvl --event OnFoo --script MyScript --autostart 1 -o out.lvl

    # 仅查看事件清单
    python teascript_event.py path/to/level.lvl --list

    # 删除事件
    python teascript_event.py path/to/level.lvl --event OnFoo --remove -o out.lvl
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SMBX38A_SCRIPTS = os.path.abspath(os.path.join(HERE, '..', '..', 'smbx-38a', 'scripts'))
sys.path.insert(0, SMBX38A_SCRIPTS)

from lvlfile import SMBXFile, Entry, url_encode, url_decode  # noqa


# Event field index by name
EVENT_FIELDS = ['name', 'msg', 'ea', 'el', 'elm', 'epy', 'eps', 'eef', 'ecn', 'evc', 'ene']

DEFAULT_FIELDS = {
    'name': '',
    'msg':  '',
    'ea':   '0,',
    'el':   '0///',
    'elm':  '',
    'epy':  '0,0,0,0,0,0,0,0,0,0,0,0',
    'eps':  '//',
    'elm':  '',
    'eef':  '0/0',
    'ecn':  '',
    'evc':  '',
    'ene':  ',0/0,0,0,0,0//',
}


def find_event(f: SMBXFile, name: str):
    for i, e in enumerate(f.entries):
        if e.marker == 'E' and url_decode(e.get(0, '')) == name:
            return i, e
    return None, None


def list_events(f: SMBXFile):
    rows = []
    for i, e in enumerate(f.entries):
        if e.marker == 'E':
            ene = e.get(10, '')
            # 解析 ene 末尾 scriptname
            parts = ene.split('/')
            script = parts[3] if len(parts) >= 4 else ''
            rows.append({
                'i': i,
                'name': url_decode(e.get(0, '')),
                'autostart': e.get(2, '').split(',')[0],
                'script': url_decode(script) if script else '',
            })
    return rows


def build_ene(script_name: str, next_event: str = '', next_delay: int = 0,
              timer_enable: int = 0, apievent: int = 0) -> str:
    nextevent = f'{url_encode(next_event)},{next_delay}'
    timer = f'{timer_enable},0,0,0,0'
    api = str(apievent) if apievent else ''
    sn = url_encode(script_name) if script_name else ''
    return f'{nextevent}/{timer}/{api}/{sn}'


def set_ene_script(existing: Entry, script_name: str) -> None:
    """修改已存在 Event 的 ene 字段，仅替换 scriptname 段。"""
    ene = existing.get(10, '')
    parts = ene.split('/')
    while len(parts) < 4:
        parts.append('')
    parts[3] = url_encode(script_name) if script_name else ''
    existing.set(10, '/'.join(parts))


def cmd_list(args):
    f = SMBXFile.load(args.path)
    rows = list_events(f)
    if not rows:
        print(f'[teascript_event] no events in {args.path}')
        return 0
    print(f'[teascript_event] {len(rows)} event(s):')
    for r in rows:
        bind = f' -> script={r["script"]!r}' if r['script'] else ''
        print(f"  [{r['i']:>4}] {r['name']!r}  autostart={r['autostart']}{bind}")
    return 0


def cmd_remove(args):
    f = SMBXFile.load(args.path)
    idx, e = find_event(f, args.event)
    if idx is None:
        sys.stderr.write(f'未找到事件 {args.event!r}\n'); return 1
    if args.event in ('Level - Start', 'P Switch - Start', 'P Switch - End'):
        sys.stderr.write(f'拒绝删除标准事件 {args.event!r}（SMBX64 标准，不可删除）\n'); return 1
    del f.entries[idx]
    out = args.output or _default_out(args.path)
    f.save(out)
    print(f'[teascript_event] removed event {args.event!r} (was at index {idx}); saved -> {out}')
    return 0


def cmd_bind(args):
    f = SMBXFile.load(args.path)
    idx, existing = find_event(f, args.event)
    if existing is None:
        # 检查脚本是否存在（如果给了 --script）
        if args.script and args.require_script:
            from lvlfile import b64_decode_text  # noqa
            found = False
            for i, e in enumerate(f.entries):
                if e.marker in ('S', 'Su') and url_decode(e.get(0, '')) == args.script:
                    found = True; break
            if not found:
                sys.stderr.write(
                    f'警告：脚本 {args.script!r} 在 lvl 中不存在；'
                    '请先用 teascript_inject.py 嵌入。\n')
                return 1

        # 创建新事件
        ene = build_ene(args.script or '')
        fields = [
            url_encode(args.event),                       # name
            '',                                           # msg
            f'{args.autostart},',                         # ea
            '0///',                                       # el
            '',                                           # elm
            '0,0,0,0,0,0,0,0,0,0,0,0',                   # epy
            '//',                                         # eps
            '0/0',                                        # eef
            '',                                           # ecn
            '',                                           # evc
            ene,                                          # ene
        ]
        new_entry = Entry(marker='E', fields=fields)
        new_idx = f.add(new_entry)
        action = f'created at index {new_idx}'
    else:
        # 修改现有事件
        if args.autostart is not None:
            ea = existing.get(2, '0,')
            cond = ea.split(',', 1)[1] if ',' in ea else ''
            existing.set(2, f'{args.autostart},{cond}')
        if args.script is not None:
            set_ene_script(existing, args.script)
        action = f'updated at index {idx}'

    out = args.output or _default_out(args.path)
    f.save(out)
    print(f'[teascript_event] event {args.event!r} {action}; '
          f'script={args.script!r}; autostart={args.autostart}; saved -> {out}')
    return 0


def _default_out(in_path: str) -> str:
    base, ext = os.path.splitext(in_path)
    return base + '.modified' + ext


def main():
    ap = argparse.ArgumentParser(description='Manage events and bind them to TeaScripts.')
    ap.add_argument('path')
    ap.add_argument('--event', help='事件名（精确字符串，自动 URL 编码后写入）')
    ap.add_argument('--script', help='脚本名（必须先用 teascript_inject 嵌入）')
    ap.add_argument('--autostart', type=int, choices=[0, 1, 2, 3], default=0,
                    help='0=否, 1=Level Start, 2=条件满足, 3=Call+条件')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--remove', action='store_true')
    ap.add_argument('-o', '--output')
    ap.add_argument('--require-script', action='store_true',
                    help='创建事件前要求脚本必须已存在于 lvl 中')
    args = ap.parse_args()

    if args.list:
        return cmd_list(args)
    if not args.event:
        sys.stderr.write('需要 --event\n'); return 2
    if args.remove:
        return cmd_remove(args)
    return cmd_bind(args)


if __name__ == '__main__':
    sys.exit(main())
