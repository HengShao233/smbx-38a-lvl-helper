#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_query.py — 按条件查询 .lvl/.wld/.wls 中的条目。

用法：
    # 列出所有 NPC（id=283）
    python lvl_query.py <file> --kind N --filter id=283

    # 多条件 + 范围（用 < / <= / > / >= / = / !=）
    python lvl_query.py <file> --kind N --filter id=283 --filter "x<200"

    # 输出指定字段（按 LVL_FIELD_NAMES 命名）
    python lvl_query.py <file> --kind E --fields name

    # 列脚本名称
    python lvl_query.py <file> --kind S
    python lvl_query.py <file> --kind Su
    python lvl_query.py <file> --kind GS

    # 输出 JSON
    python lvl_query.py <file> --kind B --json

字段索引：
    LVL: A/P1/P2/M/B/T/N/Q/W/L/E/V/S/Su 见 lvlfile.LVL_FIELD_NAMES
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lvlfile import SMBXFile, LVL_FIELD_NAMES, WLD_FIELD_NAMES, WLS_FIELD_NAMES, url_decode


OP_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(==|!=|<=|>=|<|>|=)\s*(.+)$')


def parse_filter(expr: str):
    """'x<200' -> (key='x', op='<', value='200')"""
    m = OP_RE.match(expr)
    if not m:
        raise ValueError(f'bad filter: {expr!r}')
    key, op, val = m.groups()
    if op == '=':
        op = '=='
    return key, op, val


def evaluate(value: str, op: str, target: str) -> bool:
    # 尝试数值比较
    try:
        a = float(value)
        b = float(target)
        if op == '==': return a == b
        if op == '!=': return a != b
        if op == '<':  return a <  b
        if op == '<=': return a <= b
        if op == '>':  return a >  b
        if op == '>=': return a >= b
    except (TypeError, ValueError):
        pass
    a, b = str(value), str(target)
    if op == '==': return a == b
    if op == '!=': return a != b
    # 字符串比较仅支持等/不等
    raise ValueError(f'op {op} cannot apply to non-numeric values: {value!r} vs {target!r}')


def get_field_map(kind: str):
    return {'lvl': LVL_FIELD_NAMES, 'wld': WLD_FIELD_NAMES, 'wls': WLS_FIELD_NAMES}.get(kind, {})


def main():
    ap = argparse.ArgumentParser(description='Query entries in SMBX 38A files.')
    ap.add_argument('path')
    ap.add_argument('--kind', required=True, help='marker，如 N / B / E / W / S / Su / GS / GSu / L / V / M ...')
    ap.add_argument('--filter', action='append', default=[],
                    help='形如 id=1 / x<200 / name!=Default 的条件，可多次给出，AND 关系')
    ap.add_argument('--fields', help='以逗号分隔的字段名（按已知 marker 字段名映射；未知直接忽略）')
    ap.add_argument('--json', action='store_true', help='输出 JSON')
    ap.add_argument('--limit', type=int, default=0, help='最多输出多少条；0=不限')
    ap.add_argument('--decode', action='store_true', help='对结果做 url-decode（脚本会做 base64 仅露 size）')
    args = ap.parse_args()

    f = SMBXFile.load(args.path)
    field_names = get_field_map(f.kind).get(args.kind, [])
    name_to_idx = {n: i for i, n in enumerate(field_names)}

    # 解析过滤器
    filters = [parse_filter(x) for x in args.filter]

    def predicate(e):
        for key, op, val in filters:
            if key in name_to_idx:
                v = e.get(name_to_idx[key], '')
            elif key.isdigit():
                v = e.get(int(key), '')
            else:
                # 找不到字段：始终不匹配
                return False
            try:
                if not evaluate(v, op, val):
                    return False
            except ValueError:
                return False
        return True

    matches = f.find(marker=args.kind, predicate=predicate)
    if args.limit > 0:
        matches = matches[:args.limit]

    field_filter = None
    if args.fields:
        field_filter = [s.strip() for s in args.fields.split(',') if s.strip()]

    rows = []
    for i, e in matches:
        if args.kind in ('S', 'Su', 'GS', 'GSu'):
            row = {
                'i': i,
                'marker': e.marker,
                'name': url_decode(e.get(0, '')),
                'body_b64_size': len(e.get(1, '')),
            }
        else:
            named = {}
            for j, n in enumerate(field_names):
                if j < len(e.fields):
                    v = e.fields[j]
                    if args.decode and v and (n in ('layer', 'name', 'title', 'msg', 'fn', 'lik')):
                        v = url_decode(v)
                    named[n] = v
            for j in range(len(field_names), len(e.fields)):
                named[f'extra_{j}'] = e.fields[j]
            if field_filter:
                named = {k: v for k, v in named.items() if k in field_filter}
            row = {'i': i, 'marker': e.marker, **named}
        rows.append(row)

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(f'[lvl_query] {args.kind} matches: {len(rows)}')
        for r in rows:
            print('  ' + json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
