#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_edit.py — 在 .lvl/.wld/.wls 中增删改条目（不改脚本内容；脚本用 lvl_scripts.py）。

用法：
    # 1) 添加条目（按 marker 提供命名字段；未列出的字段会按默认值/空填充）
    python lvl_edit.py <file> -o <out> --add N --layer Default --id 1 --x 100 --y -120
    python lvl_edit.py <file> -o <out> --add B --layer Default --id 457 --x 0 --y 0 --w 32 --h 32
    python lvl_edit.py <file> -o <out> --add E --name "MyEvent"     # 仅创建空事件壳，再用 --field 设其它子字段
    python lvl_edit.py <file> -o <out> --add L --name "Foreground" --status 1
    python lvl_edit.py <file> -o <out> --add V --name myVar --value 0
    python lvl_edit.py <file> -o <out> --add T --layer Default --id 1 --x 0 --y 0
    python lvl_edit.py <file> -o <out> --add P1 --x 100 --y -120

    # 2) 删除满足条件
    python lvl_edit.py <file> -o <out> --del N --where "id=1,x<200"

    # 3) 修改字段（按 marker 字段名）
    python lvl_edit.py <file> -o <out> --set N --where "id=1" --field "y=-300"
    python lvl_edit.py <file> -o <out> --set N --where "id=1" --field "y=-300" --field "msg=Hi"

    # 4) 原地修改（默认输出新文件；显式指定 --inplace 才覆盖）
    python lvl_edit.py <file> --inplace --set L --where "name=BG" --field status=0

    # 5) 通过命令组合（一条 CLI 同时执行多步）：
    python lvl_edit.py <file> -o <out> \
        --del N --where "id=1" \
        --add N --layer Default --id 2 --x 100 --y -120

注意：
- 字符串字段（layer/name/title/msg/lik/fn/...）会自动 URL 编码。
- --where 使用与 lvl_query 相同的 OP（= != < <= > >=），多条件用逗号分隔，AND 关系。
- 如不确定 marker 字段顺序，先 `lvl_parse <file> --json --decode-strings` 查看。
"""
import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lvlfile import (SMBXFile, Entry, url_encode, url_decode,
                     LVL_FIELD_NAMES, WLD_FIELD_NAMES, WLS_FIELD_NAMES)


STR_FIELDS_DEFAULT = {  # 这些字段名按 38A 规范是 url-encoded 字符串
    'layer', 'name', 'title', 'msg', 'lik', 'fn', 'n',
    'onDieFile', 'musicfile', 'sp', 'we', 'attach',
}


def get_field_map(kind: str) -> Dict[str, List[str]]:
    return {'lvl': LVL_FIELD_NAMES, 'wld': WLD_FIELD_NAMES, 'wls': WLS_FIELD_NAMES}.get(kind, {})


OP_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(==|!=|<=|>=|<|>|=)\s*(.+)$')


def parse_where(s: str) -> List[Tuple[str, str, str]]:
    if not s:
        return []
    parts = [x.strip() for x in s.split(',') if x.strip()]
    out = []
    for p in parts:
        m = OP_RE.match(p)
        if not m:
            raise ValueError(f'bad --where token: {p!r}')
        k, op, v = m.groups()
        out.append((k, '==' if op == '=' else op, v))
    return out


def evaluate(value: str, op: str, target: str) -> bool:
    try:
        a = float(value); b = float(target)
        if op == '==': return a == b
        if op == '!=': return a != b
        if op == '<':  return a <  b
        if op == '<=': return a <= b
        if op == '>':  return a >  b
        if op == '>=': return a >= b
    except (TypeError, ValueError):
        pass
    if op == '==': return str(value) == str(target)
    if op == '!=': return str(value) != str(target)
    raise ValueError(f'cannot compare strings with {op}')


def make_predicate(field_names: List[str], conds: List[Tuple[str, str, str]]):
    name_to_idx = {n: i for i, n in enumerate(field_names)}

    def pred(e: Entry) -> bool:
        for k, op, v in conds:
            if k in name_to_idx:
                actual = e.get(name_to_idx[k], '')
            elif k.isdigit():
                actual = e.get(int(k), '')
            else:
                return False
            try:
                if not evaluate(actual, op, v):
                    return False
            except ValueError:
                return False
        return True

    return pred


def encode_value(field_name: str, value: str) -> str:
    """对像 layer/name/msg 这种字符串字段做 url 编码。"""
    if value is None:
        return ''
    if field_name in STR_FIELDS_DEFAULT:
        return url_encode(value)
    return str(value)


def build_entry(marker: str, field_names: List[str], named: Dict[str, str]) -> Entry:
    """根据已知字段名构造一行；未列出的字段填空字符串到出现的最大下标。"""
    if not field_names and not named:
        return Entry(marker=marker, fields=[])
    fields: List[str] = ['' for _ in field_names]
    used_names = set()
    for k, v in named.items():
        if k in field_names:
            idx = field_names.index(k)
            fields[idx] = encode_value(k, v)
            used_names.add(k)
        elif k.isdigit():
            i = int(k)
            while i >= len(fields):
                fields.append('')
            fields[i] = '' if v is None else str(v)
        else:
            # 未知字段：忽略
            pass
    # 去除尾部多余空字段，保持简洁；但若用户显式提供且为空，仍保留
    while fields and fields[-1] == '':
        # 仅当没有明确指定该位置时才裁剪
        idx = len(fields) - 1
        if idx < len(field_names) and field_names[idx] in used_names:
            break
        fields.pop()
    return Entry(marker=marker, fields=fields)


def apply_actions(f: SMBXFile, actions: List[dict]) -> None:
    field_map = get_field_map(f.kind)
    for act in actions:
        kind = act['kind']
        marker = act['marker']
        field_names = field_map.get(marker, [])
        if kind == 'add':
            entry = build_entry(marker, field_names, act['named'])
            idx = f.add(entry)
            print(f"[lvl_edit] +{marker} at index {idx}: {entry.to_line()!r}")
        elif kind == 'del':
            conds = act['where']
            pred = make_predicate(field_names, conds)
            n = f.remove(marker=marker, predicate=pred)
            print(f"[lvl_edit] -{marker}: removed {n} entries (where={conds})")
        elif kind == 'set':
            conds = act['where']
            sets = act['sets']
            pred = make_predicate(field_names, conds)
            matched = f.find(marker=marker, predicate=pred)
            for i, e in matched:
                for k, v in sets.items():
                    if k in field_names:
                        e.set(field_names.index(k), encode_value(k, v))
                    elif k.isdigit():
                        e.set(int(k), v)
                    else:
                        print(f"[lvl_edit] WARN: unknown field {k!r} for marker {marker}",
                              file=sys.stderr)
            print(f"[lvl_edit] ~{marker}: updated {len(matched)} entries (where={conds}, set={sets})")
        else:
            raise ValueError(f'unknown action: {kind}')


def parse_field_kv(items: List[str]) -> Dict[str, str]:
    out = {}
    for it in items or []:
        if '=' not in it:
            raise ValueError(f'--field expects key=value, got {it!r}')
        k, _, v = it.partition('=')
        out[k.strip()] = v
    return out


def main():
    # 因为 argparse 不直接支持"多次同一动作但每次绑定不同子参数"，
    # 我们手工分块解析 sys.argv：将命令分割成连续的 action 段。
    args, actions, common = _parse_argv(sys.argv[1:])
    f = SMBXFile.load(args['path'])
    apply_actions(f, actions)

    # 输出
    if args.get('inplace'):
        out = args['path']
    else:
        out = args.get('output')
        if not out:
            base, ext = os.path.splitext(args['path'])
            out = base + '.modified' + ext
    f.save(out)
    print(f"[lvl_edit] saved -> {out}")
    return 0


def _parse_argv(argv: List[str]):
    # 第一个非 flag 视为 path
    if not argv:
        print(__doc__)
        sys.exit(2)
    path = None
    inplace = False
    output = None
    actions = []
    i = 0
    # 全局参数
    while i < len(argv):
        a = argv[i]
        if a in ('-h', '--help'):
            print(__doc__); sys.exit(0)
        if a == '--inplace':
            inplace = True; i += 1; continue
        if a in ('-o', '--output'):
            output = argv[i + 1]; i += 2; continue
        if a in ('--add', '--del', '--set'):
            break
        if path is None and not a.startswith('-'):
            path = a; i += 1; continue
        print(f'unknown global flag: {a}', file=sys.stderr)
        sys.exit(2)
    if path is None:
        print('missing input path', file=sys.stderr); sys.exit(2)
    # 解析每个 action 段
    while i < len(argv):
        a = argv[i]
        if a == '--add':
            marker = argv[i + 1]
            i += 2
            named = {}
            while i < len(argv) and not argv[i].startswith('--'):
                i += 1  # 不应该出现裸值，跳过
            # add 段：消化所有 --<key> <value>
            i = _consume_kv_until_action(argv, i, named)
            actions.append({'kind': 'add', 'marker': marker, 'named': named})
        elif a == '--del':
            marker = argv[i + 1]; i += 2
            where = []
            while i < len(argv) and argv[i] not in ('--add', '--del', '--set'):
                if argv[i] == '--where':
                    where = parse_where(argv[i + 1]); i += 2
                else:
                    print(f'unknown del flag: {argv[i]}', file=sys.stderr); sys.exit(2)
            actions.append({'kind': 'del', 'marker': marker, 'where': where})
        elif a == '--set':
            marker = argv[i + 1]; i += 2
            where = []
            sets = {}
            while i < len(argv) and argv[i] not in ('--add', '--del', '--set'):
                if argv[i] == '--where':
                    where = parse_where(argv[i + 1]); i += 2
                elif argv[i] == '--field':
                    kv = argv[i + 1]
                    if '=' not in kv:
                        print(f'--field expects key=value, got {kv!r}', file=sys.stderr); sys.exit(2)
                    k, _, v = kv.partition('=')
                    sets[k.strip()] = v
                    i += 2
                else:
                    print(f'unknown set flag: {argv[i]}', file=sys.stderr); sys.exit(2)
            actions.append({'kind': 'set', 'marker': marker, 'where': where, 'sets': sets})
        else:
            print(f'expected --add/--del/--set, got {a}', file=sys.stderr); sys.exit(2)
    return ({'path': path, 'inplace': inplace, 'output': output}, actions, None)


def _consume_kv_until_action(argv, i, named):
    """从 i 起消化 `--<key> <value>` 直到遇到下一个 --add/--del/--set 或结束。"""
    while i < len(argv):
        a = argv[i]
        if a in ('--add', '--del', '--set'):
            break
        if not a.startswith('--'):
            print(f'expected --key value, got {a!r}', file=sys.stderr); sys.exit(2)
        key = a[2:]
        if i + 1 >= len(argv):
            print(f'missing value for {a}', file=sys.stderr); sys.exit(2)
        named[key] = argv[i + 1]
        i += 2
    return i


if __name__ == '__main__':
    sys.exit(main())
