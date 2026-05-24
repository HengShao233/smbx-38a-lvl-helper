#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_validate.py — 静态校验 .lvl 文件是否符合 SMBX 38A 引擎的真实加载约束。

捕获可能引发 `run-time error '13' Type Mismatch` 的所有已知格式陷阱：

| 规则码 | 检测点 |
| --- | --- |
| L001  | A 行字段数（必须 5；含尾部 `,,,` 占位） |
| L002  | M 行必须 21 行（id=1..21 全声明） |
| L003  | M 行字段数（14） |
| L004  | B 行 `contain` 字段必须为空字符串而非 0 |
| L005  | B 行字段数（10） |
| L006  | N 行 b 字段必须 6 个数 |
| L007  | N 行 events / attach 字段无值时必须空字符串（不是 "0,..."） |
| L008  | N 行字段数（≥9） |
| L009  | T 行字段数（4） |
| L010  | L 行 layer 名必须强制百分号编码（每字符 %xx） |
| L011  | L 行字段数（2） |
| L012  | E 行字段数（11） |
| L013  | E 行 `el` 字段格式（4 段斜杠分隔，不能是 `KEY=VAL`） |
| L014  | E 行 `ene` 绑定脚本时 apievent 段不能为空（必须 `0`） |
| L015  | V 行字段数（3） |
| L016  | V 行 name 必须百分号编码且仅含字母数字（字母开头） |
| L017  | S/Su 行字段数（≥2；实测 SU 可有第 3 段元数据） |
| L018  | 嵌入脚本中的 user variable 名必须仅含字母数字、字母开头（无下划线） |
| L019  | 字符串字段未做强制百分号编码（含裸 ASCII 字母） |
| L020  | 嵌入脚本 marker 必须是大写 `SU`/`GSU`；body 必须用 GBK 字节 |
| L021  | R 行（用户数组声明）每段名字必须百分号编码 + 合法命名 |
| L022  | type=2 (door) 的 W 行入口 / 出口附近无门 BGO（视觉缺失） — warning |

> 字段数定义：使用 `lvlfile.py` 的 `Entry.fields` 长度（**不含 marker token**）。

CLI:
    python lvl_validate.py path/to/level.lvl
    python lvl_validate.py path/to/level.lvl --json
    python lvl_validate.py path/to/level.lvl --disable L019
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lvlfile import SMBXFile, Entry, url_decode, b64_decode_text  # noqa


@dataclass
class Diag:
    rule: str
    severity: str          # 'error' | 'warning' | 'info'
    line: int              # 1-based
    marker: str
    message: str
    snippet: str = ''

    def to_dict(self):
        return dict(rule=self.rule, severity=self.severity,
                    line=self.line, marker=self.marker,
                    message=self.message, snippet=self.snippet)


PCT_ENCODED_RE = re.compile(r'^(?:%[0-9A-Fa-f]{2})*$')
IDENT_RE = re.compile(r'^[A-Za-z][A-Za-z0-9]*$')


def is_full_pct_encoded(s: str) -> bool:
    """所有字符都形如 %xx 才算合法 38A 字符串字段。空串也算合格。"""
    return s == '' or PCT_ENCODED_RE.match(s) is not None


def lint_file(path: str, disabled: Optional[set] = None) -> List[Diag]:
    disabled = disabled or set()
    diags: List[Diag] = []
    f = SMBXFile.load(path)

    # ---- 全局统计 ----
    m_count = sum(1 for e in f.entries if e.marker == 'M')
    if 'L002' not in disabled and m_count != 21:
        diags.append(Diag('L002', 'error', 0, 'M',
                          f'M (section) 行数={m_count}，必须正好 21 (id=1..21)',
                          ''))

    # ---- 逐行 ----
    for idx, e in enumerate(f.entries):
        ln = idx + 2  # 第 1 行是 SMBXFile?? header
        nfields = len(e.fields)
        m = e.marker

        if m == 'A' and 'L001' not in disabled:
            if nfields != 5:
                diags.append(Diag('L001', 'error', ln, m,
                                  f'A 行应有 5 字段，实际 {nfields}',
                                  e.to_line()[:120]))

        elif m == 'M' and 'L003' not in disabled:
            if nfields != 14:
                diags.append(Diag('L003', 'error', ln, m,
                                  f'M 行应有 14 字段(id..musicfile)，实际 {nfields}',
                                  e.to_line()[:120]))

        elif m == 'B':
            if 'L005' not in disabled and nfields != 10:
                diags.append(Diag('L005', 'error', ln, m,
                                  f'B 行应有 10 字段，实际 {nfields}',
                                  e.to_line()[:120]))
            if 'L004' not in disabled and nfields >= 4:
                contain = e.fields[3]
                if contain == '0':
                    diags.append(Diag('L004', 'error', ln, m,
                                      'B 行 contain 字段写成 "0" 会导致 type mismatch；无内容物应使用空字符串',
                                      e.to_line()[:120]))
            if 'L019' not in disabled and nfields >= 1:
                layer = e.fields[0]
                if not is_full_pct_encoded(layer):
                    diags.append(Diag('L019', 'error', ln, m,
                                      f'B 行 layer 字段未做强制百分号编码: {layer!r}',
                                      e.to_line()[:120]))

        elif m == 'T':
            if 'L009' not in disabled and nfields != 4:
                diags.append(Diag('L009', 'error', ln, m,
                                  f'T (BGO) 行应有 4 字段(layer/id/x/y)，实际 {nfields}',
                                  e.to_line()[:120]))

        elif m == 'N':
            if 'L008' not in disabled and nfields < 9:
                diags.append(Diag('L008', 'error', ln, m,
                                  f'N 行应有 ≥9 字段，实际 {nfields}',
                                  e.to_line()[:120]))
            if 'L006' not in disabled and nfields >= 5:
                b_field = e.fields[4]
                bs = b_field.split(',') if b_field else []
                if len(bs) != 6:
                    diags.append(Diag('L006', 'error', ln, m,
                                      f'N 行 b 字段应有 6 个数 (b1..b6)，实际 {len(bs)} 个: {b_field!r}',
                                      e.to_line()[:120]))
            if 'L007' not in disabled and nfields >= 8:
                events_field = e.fields[6]
                attach_field = e.fields[7]
                if events_field and re.match(r'^[\d,]+$', events_field) and ',' in events_field:
                    parts = events_field.split(',')
                    if all(p == '0' for p in parts):
                        diags.append(Diag('L007', 'warning', ln, m,
                                          f'N 行 events 字段填充全 0 占位（{events_field!r}），无事件绑定时应留空',
                                          e.to_line()[:120]))
                if attach_field == '0,0':
                    diags.append(Diag('L007', 'warning', ln, m,
                                      'N 行 attach 字段写 "0,0" 占位，无附加时应留空',
                                      e.to_line()[:120]))

        elif m == 'L':
            if 'L011' not in disabled and nfields != 2:
                diags.append(Diag('L011', 'error', ln, m,
                                  f'L (Layer) 行应有 2 字段(name/status)，实际 {nfields}',
                                  e.to_line()[:120]))
            if 'L010' not in disabled and nfields >= 1:
                name = e.fields[0]
                if not is_full_pct_encoded(name):
                    diags.append(Diag('L010', 'error', ln, m,
                                      f'L 行 name 必须做强制百分号编码: {name!r}',
                                      e.to_line()[:120]))

        elif m == 'E':
            if 'L012' not in disabled and nfields != 11:
                diags.append(Diag('L012', 'error', ln, m,
                                  f'E (Event) 行应有 11 字段，实际 {nfields}',
                                  e.to_line()[:120]))
            # el 字段
            if 'L013' not in disabled and nfields >= 4:
                el = e.fields[3]
                if el and '=' in el:
                    diags.append(Diag('L013', 'error', ln, m,
                                      f'E 行 el 字段含有 "=" (KV 语法)：{el!r}；正确格式为 b/show/hide/toggle',
                                      e.to_line()[:120]))
                # 应该是 4 段斜杠分隔
                if el and el != '' and el.count('/') < 3:
                    diags.append(Diag('L013', 'error', ln, m,
                                      f'E 行 el 字段斜杠数不足: {el!r}；应为 4 段(b/show/hide/toggle)',
                                      e.to_line()[:120]))
            # ene 字段
            if 'L014' not in disabled and nfields >= 11:
                ene = e.fields[10]
                segs = ene.split('/')
                # 4 段或更多时，第 3 段(apievent)不能为空
                if len(segs) >= 4 and segs[2] == '' and segs[3]:
                    diags.append(Diag('L014', 'error', ln, m,
                                      f'E 行 ene 字段 apievent 段为空且有 scriptname：{ene!r}；apievent 必须为 "0" 或具体数字',
                                      e.to_line()[:120]))

        elif m == 'V':
            if 'L015' not in disabled and nfields != 3:
                diags.append(Diag('L015', 'error', ln, m,
                                  f'V (Variable) 行应有 3 字段(name/value/scope)，实际 {nfields}',
                                  e.to_line()[:120]))
            if 'L016' not in disabled and nfields >= 1:
                name_enc = e.fields[0]
                if not is_full_pct_encoded(name_enc):
                    diags.append(Diag('L016', 'error', ln, m,
                                      f'V 行 name 必须百分号编码: {name_enc!r}',
                                      e.to_line()[:120]))
                else:
                    name = url_decode(name_enc)
                    if not IDENT_RE.match(name):
                        diags.append(Diag('L016', 'error', ln, m,
                                          f'V 行变量名 {name!r} 不合法（必须字母开头、只含字母数字、不含下划线）',
                                          e.to_line()[:120]))

        elif m == 'R':
            # R 行：用户数组声明，一行多个名字。每个名字百分号编码 + 命名规约。
            if 'L021' not in disabled and nfields < 1:
                diags.append(Diag('L021', 'error', ln, m,
                                  'R (Array) 行应至少包含一个数组名',
                                  e.to_line()[:120]))
            if 'L021' not in disabled:
                for i_arr, arr_enc in enumerate(e.fields):
                    if not arr_enc:
                        continue
                    if not is_full_pct_encoded(arr_enc):
                        diags.append(Diag('L021', 'error', ln, m,
                                          f'R 行第 {i_arr+1} 段 {arr_enc!r} 必须百分号编码',
                                          e.to_line()[:120]))
                    else:
                        nm = url_decode(arr_enc)
                        if not IDENT_RE.match(nm):
                            diags.append(Diag('L021', 'error', ln, m,
                                              f'R 行数组名 {nm!r} 不合法（字母开头、仅字母数字、不含下划线）',
                                              e.to_line()[:120]))


        elif m in ('S', 'Su', 'SU', 'GS', 'GSu', 'GSU'):
            # 实测：38A editor 在 GUI 编辑保存时，常给 SU 行附加第 3 段
            # （某种 base64 元数据，引擎接受 2 段 / 3+ 段两种形态）。
            # 因此规则放宽为 ≥2 字段。
            if 'L017' not in disabled and nfields < 2:
                diags.append(Diag('L017', 'error', ln, m,
                                  f'{m} 行应有 ≥2 字段(name/base64body[/extra])，实际 {nfields}',
                                  e.to_line()[:120]))

            if nfields >= 2:
                body_enc = e.fields[1]
                # 先解 base64 拿原始字节
                # ⚠ 38A editor 保存的 SU base64 末尾会去掉 `=` padding，需补齐
                import base64
                try:
                    cleaned = re.sub(r'\s+', '', body_enc).rstrip('=')
                    cleaned = cleaned + '=' * ((-len(cleaned)) % 4)
                    raw_bytes = base64.b64decode(cleaned)
                except Exception:
                    raw_bytes = b''
                has_non_ascii = any(b > 127 for b in raw_bytes)
                # 用于 L018 的脚本字符串：按真实社区实践 GBK 优先尝试
                body = ''
                for enc_name in ('gbk', 'utf-8', 'latin-1'):
                    try:
                        body = raw_bytes.decode(enc_name, errors='strict')
                        break
                    except UnicodeDecodeError:
                        continue
                if not body and raw_bytes:
                    body = raw_bytes.decode('latin-1', errors='replace')

                # ---- L020: marker 必须用大写 SU/GSU，且含非 ASCII 时禁止用 S/GS ----
                if 'L020' not in disabled:
                    if has_non_ascii and m in ('S', 'GS'):
                        diags.append(Diag(
                            'L020', 'error', ln, m,
                            f'{m} 含非 ASCII 字符。38A 引擎对 `S` 路径的处理不稳，'
                            f'应改用大写 `{"SU" if m == "S" else "GSU"}` marker + GBK 字节',
                            e.to_line()[:80]))
                    elif m in ('Su', 'GSu'):
                        # 小写 Su / GSu 在某些版本不被识别为脚本，警告
                        upper = 'SU' if m == 'Su' else 'GSU'
                        diags.append(Diag(
                            'L020', 'warning', ln, m,
                            f'marker `{m}` 是小写形式；38A 实际写入用大写 `{upper}`，'
                            f'某些版本可能不识别小写形式',
                            e.to_line()[:80]))

                # ---- L018: 脚本中变量命名 ----
                if 'L018' not in disabled:
                    bad = set()
                    for var_match in re.finditer(r'\b(?:v|gv|str|gstr)\(\s*([A-Za-z_][A-Za-z_0-9]*)\s*\)',
                                                 body, re.IGNORECASE):
                        name = var_match.group(1)
                        if not IDENT_RE.match(name):
                            bad.add(name)
                    for name in sorted(bad):
                        diags.append(Diag('L018', 'error', ln, m,
                                          f'脚本 {url_decode(e.fields[0])!r} 中 user variable 名 {name!r} 不合法（含下划线）',
                                          ''))

    # ---- L022: door warp 没有视觉门 BGO ----
    if 'L022' not in disabled:
        # 收集所有 BGO 位置 (x,y) -> id
        bgo_positions = {}
        for e2 in f.entries:
            if e2.marker == 'T' and len(e2.fields) >= 4:
                try:
                    bx_, by_ = int(e2.fields[2]), int(e2.fields[3])
                    bgo_positions[(bx_, by_)] = int(e2.fields[1])
                except (ValueError, IndexError):
                    pass
        # 检查每个 type=2 (door) warp
        for idx2, e2 in enumerate(f.entries):
            if e2.marker != 'W' or len(e2.fields) < 6:
                continue
            try:
                wtype = int(e2.fields[5])
            except (ValueError, IndexError):
                continue
            if wtype != 2:
                continue
            try:
                wx_, wy_ = int(e2.fields[1]), int(e2.fields[2])
                ex_, ey_ = int(e2.fields[3]), int(e2.fields[4])
            except (ValueError, IndexError):
                continue
            ln2 = idx2 + 2
            # 在入口 / 出口附近 ±16 x, [-64, +0] y 范围内查 BGO
            def has_door_visual(px: int, py: int) -> bool:
                for dx in (-16, 0, 16):
                    for dy in range(-64, 1, 16):
                        if (px + dx, py + dy) in bgo_positions:
                            return True
                return False
            if not has_door_visual(wx_, wy_):
                diags.append(Diag('L022', 'warning', ln2, 'W',
                                  f'door warp 入口 ({wx_},{wy_}) 附近无 BGO 视觉，'
                                  f'玩家会找不到传送点。建议放门 BGO（id=92 默认门 / 79 / 87 / 158 / 168）',
                                  e2.to_line()[:120]))
            if (ex_, ey_) != (wx_, wy_) and not has_door_visual(ex_, ey_):
                diags.append(Diag('L022', 'warning', ln2, 'W',
                                  f'door warp 出口 ({ex_},{ey_}) 附近无 BGO 视觉，'
                                  f'传送过去后玩家不知道刚从哪进来。建议同样放门 BGO',
                                  e2.to_line()[:120]))

    # 排序
    diags.sort(key=lambda d: (d.line, d.rule))
    return diags



def main():
    ap = argparse.ArgumentParser(description='Validate a .lvl file against SMBX 38A loading rules.')
    ap.add_argument('path')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--disable', action='append', default=[],
                    help='禁用规则码，例 --disable L007')
    ap.add_argument('--no-warnings', action='store_true')
    args = ap.parse_args()

    diags = lint_file(args.path, set(args.disable))
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
            print(f'{args.path}:{d.line}: {tag} [{d.rule}] {d.marker}: {d.message}')
            if d.snippet:
                print(f'    > {d.snippet}')
        print(f'[lvl_validate] {n_err} error(s), {n_warn} warning(s)')

    return 1 if n_err > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
