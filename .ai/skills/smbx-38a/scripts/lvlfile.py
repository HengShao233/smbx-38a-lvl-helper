#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMBX 38A LVL/WLD/WLS 文件解析与序列化核心库。

设计原则：
- 保真：解析后再序列化必须 byte-equal 原文件（round-trip 无损）。
- 宽容：未知 marker、额外尾部字段一律保留。
- 简单：每行表示为一个 `Entry`(marker, fields[list[str]])，按原顺序存于 LVLFile.entries。
- 行尾：自动检测 CRLF / LF；保留原始换行符。
- 编码：默认 ASCII；非 ASCII 字段按 38A 规范是 URL 编码后才进文件，所以原文件仍是 ASCII。
       本库不强制解码，只在 helper 函数里提供 url/base64 编解码。

核心 API:
    f = LVLFile.load(path)
    f.entries           # list[Entry]
    f.find(marker='N', filter_fn=...)
    f.add(entry)        # 追加；或 f.entries.insert(idx, entry)
    f.remove(predicate)
    f.save(path)
    Entry.from_line('B||457|-199680|-200576||0|0||32|32')
    entry.to_line()
"""
from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Tuple
from urllib.parse import quote, unquote

# 规范行首形如 "SMBXFile<digits>"
HEADER_RE = re.compile(r'^SMBXFile(\d+)\s*$')


def url_encode(s: str) -> str:
    """⚠ 38A 风格的强制百分号编码（每个字符都 %xx，含字母数字）。

    这是 SMBX 38A 引擎实际使用的编码方式，与 RFC 3986 不同。
    真实关卡里 `L|%44%65%66%61%75%6C%74|1` 才是合法的（"Default" 全编码），
    若写裸 `L|Default|1`，引擎在解析图层名时会触发 type mismatch。
    """
    if not s:
        return ''
    out = []
    for ch in s:
        for byte in ch.encode('utf-8'):
            out.append(f'%{byte:02X}')
    return ''.join(out)


# 标准 RFC 3986 风格（仅在解码时容忍即可）
def url_encode_minimal(s: str) -> str:
    """RFC 3986 风格的最小编码——AI 慎用。仅在外部对接时使用。"""
    if s is None:
        return ''
    return quote(s, safe='')


def url_decode(s: str) -> str:
    if s is None:
        return ''
    return unquote(s)


def b64_encode_text(s: str, encoding: str = 'utf-8') -> str:
    if s is None:
        return ''
    return base64.b64encode(s.encode(encoding, errors='replace')).decode('ascii')


def b64_decode_text(s: str, encoding: str = 'utf-8') -> str:
    if not s:
        return ''
    # base64 容忍可能的换行/空白
    raw = re.sub(r'\s+', '', s)
    return base64.b64decode(raw).decode(encoding, errors='replace')


# =============================================================
# 脚本嵌入：marker 选择 + 系统 ANSI 编码
# -------------------------------------------------------------
# ⚠ 38A 引擎实测踩坑（基于真实工作关卡的字节级抽样验证）：
#
#   1) Marker 大小写：38A 引擎实际接受的 marker 是 **大写 `SU`**
#      （以及全局脚本的 `GSU`），而非文档里写的 `Su`/`GSu`。
#      虽然 lvlfile 解析时 marker 大小写无关紧要，但**写入时必须用大写 `SU`**，
#      否则某些版本的引擎不会把它当作脚本行加载。
#
#   2) Body 字节编码：38A 是 VB6 应用，运行在中文 Windows 上时把字符串当成
#      **系统 ANSI codepage（中国大陆 = CP936 / GBK）** 处理。引擎读 `SU` 行
#      解 base64 后，**按 GBK 把字节解为 String**。
#      因此写入时必须把脚本源码用 **GBK** 编码成字节再 base64；
#      若用 UTF-8 字节，引擎会按 GBK 解读，造成乱码 + 字符边界错乱
#      （UTF-8 三字节字符被当成 1 个 GBK 双字节 + 1 残字节，残字节"吃掉"行尾 `\n`）。
#
#   3) 真实工作样本：`Artworks/boss 结束 - 回忆通用过场/实现例/main.lvl`
#      含 12 个 `SU` 行，body 全部是 GBK 字节流。
#
# 因此：嵌入脚本的标准做法 = **`SU` marker + GBK base64**。
# =============================================================

# 38A 实际默认编码（中文 Windows 系统的 ANSI codepage）
SCRIPT_BODY_ENCODING = 'gbk'  # 别名：'cp936'


def pick_script_marker(body: str = '', *, global_script: bool = False) -> str:
    """根据上下文选择正确的脚本 marker。

    经实测，38A 引擎实际期望的脚本 marker 是 **大写 SU**（和全局脚本 GSU），
    不是文档里写的 `Su`/`GSu`。本函数始终返回大写形式。

    Args:
        body: 脚本源码（保留参数以便未来扩展，目前不影响选择）。
        global_script: True 表示 .wls 全局脚本（GSU），False 表示 .lvl 本地脚本（SU）。

    Returns:
        marker 字符串：'SU' 或 'GSU'。
    """
    return 'GSU' if global_script else 'SU'


def b64_encode_script(body: str, encoding: str = SCRIPT_BODY_ENCODING) -> str:
    """把脚本源码编成 base64（默认用系统 ANSI / GBK 字节）。

    与 `SU` / `GSU` marker 配合：引擎按 ANSI codepage 解读 base64 字节，
    所以编码侧也必须用同样 codepage。
    若脚本含无法被 GBK 表示的字符（极少见的 emoji 等），会报错；
    可显式传 `encoding='utf-8'` 但要预期引擎读出来是乱码。
    """
    if body is None:
        return ''
    try:
        return base64.b64encode(body.encode(encoding, errors='strict')).decode('ascii')
    except UnicodeEncodeError:
        # 失败时退化到 errors='replace'，并打印告警让调用方知晓
        import sys as _sys
        print(f'[lvlfile] WARN: script body has chars not representable in {encoding!r}; using errors=replace',
              file=_sys.stderr)
        return base64.b64encode(body.encode(encoding, errors='replace')).decode('ascii')


def b64_decode_script(b64: str, marker: str = 'SU') -> str:
    """把 lvl 中的 base64 脚本解回 Python str。

    Args:
        b64: 原始 base64 字符串。
        marker: 行首 marker（'S'/'Su'/'SU'/'GS'/'GSu'/'GSU'），决定首选解码路径：
            - 'S'/'GS'              → UTF-8 优先（按文档）
            - 'Su'/'SU'/'GSu'/'GSU' → ANSI/GBK 优先（按真实社区实践）
        失败时按 utf-8 → gbk → latin-1 顺序回退，确保不抛异常。

    ⚠ 实测踩坑：38A editor 保存的 SU base64 会**去掉末尾 `=` padding**。
       本函数自动补齐到 % 4 == 0；调用方无需处理。
    """
    if not b64:
        return ''
    raw = re.sub(r'\s+', '', b64)
    # 38A editor 会去掉末尾 `=` padding，这里补回；同时容忍多余 `=`。
    raw = raw.rstrip('=')
    pad = (-len(raw)) % 4
    raw = raw + ('=' * pad)
    data = base64.b64decode(raw)
    is_utf8_marker = marker.upper() in ('S', 'GS')
    candidates = (['utf-8', 'gbk', 'latin-1']
                  if is_utf8_marker
                  else ['gbk', 'utf-8', 'latin-1'])
    for enc in candidates:
        try:
            return data.decode(enc, errors='strict')
        except UnicodeDecodeError:
            continue
    return data.decode('latin-1', errors='replace')



@dataclass
class Entry:
    """一行数据：marker + 后续字段（保持原始字符串形态）。"""
    marker: str
    fields: List[str] = field(default_factory=list)
    raw: Optional[str] = None  # 解析时保留原始行（不含换行符），用于 round-trip 校验

    @classmethod
    def from_line(cls, line: str) -> 'Entry':
        # 行可能不含 '|'（如 BTNS|... 也含；但有些 marker 单独一行如 SMBXFile）
        # 这里仅适用于已知是数据行的情形。SMBXFile 行单独处理。
        if '|' not in line:
            return cls(marker=line.strip(), fields=[], raw=line)
        head, _, rest = line.partition('|')
        fields = rest.split('|') if rest != '' else []
        return cls(marker=head, fields=fields, raw=line)

    def to_line(self) -> str:
        if not self.fields:
            return self.marker
        return self.marker + '|' + '|'.join(self.fields)

    # ---- 字段访问 helper ----
    def get(self, idx: int, default: str = '') -> str:
        return self.fields[idx] if 0 <= idx < len(self.fields) else default

    def set(self, idx: int, value: str) -> None:
        # 不允许在中间插入空洞，只能 append 或修改已存在的
        while idx >= len(self.fields):
            self.fields.append('')
        self.fields[idx] = '' if value is None else str(value)

    def get_int(self, idx: int, default: int = 0) -> int:
        try:
            v = self.get(idx, '').strip()
            return int(v) if v != '' else default
        except ValueError:
            try:
                return int(float(v))
            except Exception:
                return default

    def __repr__(self) -> str:
        body = '|'.join(self.fields)
        if len(body) > 80:
            body = body[:77] + '...'
        return f'Entry({self.marker}|{body})'


# 主要 marker 的字段名映射（仅用于美化输出/查询；不强制约束写入格式）
LVL_FIELD_NAMES = {
    'A':  ['stars', 'title', 'onDieFile', 'onDieEntrance'],
    'P1': ['x', 'y'],
    'P2': ['x', 'y'],
    'M':  ['id', 'x', 'y', 'w', 'h', 'underwater', 'wrapX', 'offexit',
           'noTurnBackX', 'noTurnBackY', 'wrapY', 'music', 'background', 'musicfile'],
    'B':  ['layer', 'id', 'x', 'y', 'contain', 'slippery', 'invisible',
           'events', 'w', 'h'],
    'T':  ['layer', 'id', 'x', 'y'],
    'N':  ['layer', 'id', 'x', 'y', 'flags', 'sp', 'events',
           'attach', 'generator', 'msg'],
    'Q':  ['layer', 'x', 'y', 'w', 'h', 'flags', 'event'],
    'W':  ['layer', 'x', 'y', 'ex', 'ey', 'type', 'enterd', 'exitd',
           'starsCfg', 'flags', 'lik', 'liid', 'noexit', 'wx', 'wy', 'le', 'we'],
    'L':  ['name', 'status'],
    'E':  ['name', 'msg', 'ea', 'el', 'elm', 'epy', 'eps', 'eef', 'ecn', 'evc', 'ene'],
    'V':  ['name', 'value'],
    'S':  ['name', 'body_b64'],
    'Su': ['name', 'body_b64_ascii'],
}

WLD_FIELD_NAMES = {
    'ws1': ['wn', 'bp', 'asn', 'flags1', 'starsItems', 'acm', 'sc'],
    'ws2': ['credits'],
    'ws3': ['list'],
    'ws4': ['se', 'msg'],
    'T':   ['id', 'x', 'y', 'layer'],
    'S':   ['id', 'x', 'y', 'layer'],
    'P':   ['id', 'x', 'y', 'layer'],
    'M':   ['id', 'x', 'y', 'name', 'layer', 'w', 'h', 'flag', 'touch', 'itemEvents'],
    'L':   ['id', 'x', 'y', 'fn', 'n', 'exits', 'wx', 'wy', 'wlz', 'flags', 's', 'layer', 'lmt'],
    'WL':  ['name', 'status'],
    'WE':  ['name', 'layer', 'layerm', 'world', 'other'],
}

WLS_FIELD_NAMES = {
    'G':   ['name', 'value'],
    'GS':  ['name', 'body_b64'],
    'GSu': ['name', 'body_b64_ascii'],
    'CW':  ['entries'],
}


@dataclass
class SMBXFile:
    """通用容器：LVL / WLD / WLS 共用。"""
    version: int = 65
    entries: List[Entry] = field(default_factory=list)
    newline: str = '\r\n'
    encoding: str = 'ascii'
    kind: str = 'lvl'  # lvl|wld|wls，决定字段名映射等

    # ---- 加载 / 保存 ----
    @classmethod
    def load(cls, path: str, kind: Optional[str] = None) -> 'SMBXFile':
        with open(path, 'rb') as fh:
            raw = fh.read()
        # 自动检测 BOM 与换行
        encoding = 'utf-8' if raw.startswith(b'\xef\xbb\xbf') else 'ascii'
        try:
            text = raw.decode(encoding)
        except UnicodeDecodeError:
            text = raw.decode('utf-8', errors='replace')
            encoding = 'utf-8'
        if encoding == 'utf-8' and text.startswith('\ufeff'):
            text = text[1:]
        # 检测 newline：第一处 \r\n 或 \n
        nl = '\r\n' if '\r\n' in text[:4096] else '\n'
        # 拆行（保留每行的原始内容；最后空行也保留）
        # 用 split(nl) 而非 splitlines，便于 round-trip
        lines = text.split(nl)
        # 解析 header
        if not lines:
            raise ValueError(f'{path}: empty file')
        m = HEADER_RE.match(lines[0])
        if not m:
            raise ValueError(f'{path}: missing SMBXFile?? header (first line: {lines[0]!r})')
        version = int(m.group(1))
        body_lines = lines[1:]
        # 推断 kind：从扩展名或调用者指定
        if kind is None:
            ext = os.path.splitext(path)[1].lower().lstrip('.')
            kind = ext if ext in ('lvl', 'wld', 'wls') else 'lvl'
        # 转换为 Entry
        entries: List[Entry] = []
        for ln in body_lines:
            if ln == '':
                # 保留空行：用一个 marker='' 的 Entry 代表
                entries.append(Entry(marker='', fields=[], raw=''))
                continue
            entries.append(Entry.from_line(ln))
        return cls(version=version, entries=entries, newline=nl,
                   encoding=encoding, kind=kind)

    def save(self, path: str) -> None:
        out_lines = [f'SMBXFile{self.version}']
        for e in self.entries:
            out_lines.append(e.to_line())
        text = self.newline.join(out_lines)
        # 保留尾随换行（很多 lvl 文件最后无尾随换行，本库 round-trip 时按 entries 末尾 ''
        #  自动还原，因此不要再 append）
        os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
        with open(path, 'wb') as fh:
            fh.write(text.encode(self.encoding, errors='replace'))

    # ---- 别名 ----
    @classmethod
    def load_lvl(cls, path: str) -> 'SMBXFile':
        return cls.load(path, kind='lvl')

    @classmethod
    def load_wld(cls, path: str) -> 'SMBXFile':
        return cls.load(path, kind='wld')

    @classmethod
    def load_wls(cls, path: str) -> 'SMBXFile':
        return cls.load(path, kind='wls')

    # ---- 查询 / 编辑 ----
    def find(self,
             marker: Optional[str] = None,
             predicate: Optional[Callable[[Entry], bool]] = None
             ) -> List[Tuple[int, Entry]]:
        """返回 (index, entry) 列表。"""
        out = []
        for i, e in enumerate(self.entries):
            if marker is not None and e.marker != marker:
                continue
            if predicate is not None and not predicate(e):
                continue
            out.append((i, e))
        return out

    def remove(self,
               marker: Optional[str] = None,
               predicate: Optional[Callable[[Entry], bool]] = None) -> int:
        """删除满足条件的条目，返回删除条数。"""
        keep = []
        n = 0
        for e in self.entries:
            if (marker is None or e.marker == marker) and (predicate is None or predicate(e)):
                n += 1
                continue
            keep.append(e)
        self.entries = keep
        return n

    def add(self, entry: Entry, before_marker: Optional[str] = None) -> int:
        """追加 entry。如果指定 before_marker，会插入到首个该 marker 出现位置之前；
        否则尝试插入到同 marker 块的末尾，否则文件最后。返回插入的 index。"""
        if before_marker:
            for i, e in enumerate(self.entries):
                if e.marker == before_marker:
                    self.entries.insert(i, entry)
                    return i
        # 找同 marker 末尾
        last = -1
        for i, e in enumerate(self.entries):
            if e.marker == entry.marker:
                last = i
        if last >= 0:
            self.entries.insert(last + 1, entry)
            return last + 1
        # 末尾追加（避开末尾空行）
        idx = len(self.entries)
        while idx > 0 and self.entries[idx - 1].marker == '' and not self.entries[idx - 1].fields:
            idx -= 1
        self.entries.insert(idx, entry)
        return idx

    # ---- 脚本相关 helper ----
    SCRIPT_MARKERS = ('S', 'Su', 'SU', 'GS', 'GSu', 'GSU')

    def iter_scripts(self) -> Iterable[Tuple[int, Entry, str, str]]:
        """yield (index, entry, decoded_name, decoded_body) 仅遍历脚本 marker。

        识别大小写两种形式：S/Su/SU/GS/GSu/GSU（38A 实际写入的是大写 SU/GSU）。
        """
        for i, e in enumerate(self.entries):
            if e.marker in self.SCRIPT_MARKERS:
                name = url_decode(e.get(0, ''))
                body_enc = e.get(1, '')
                try:
                    body = b64_decode_script(body_enc, e.marker)
                except Exception as ex:
                    body = f'<<DECODE FAILED: {ex}>>'
                yield i, e, name, body

    def set_script(self, index: int, body: str, *, auto_marker: bool = True) -> None:
        """更新脚本内容；body 默认用系统 ANSI / GBK 字节做 base64（38A 引擎期望的）。

        Args:
            index: entries 中的索引。
            body: 新的脚本源码 (Python str)。
            auto_marker: 若为 True 且 body 含非 ASCII，则把 marker 升级为
                大写 SU / GSU（38A 实际接受的形式）。
        """
        e = self.entries[index]
        if e.marker not in self.SCRIPT_MARKERS:
            raise ValueError(f'entries[{index}] is not a script (marker={e.marker})')
        if auto_marker:
            has_non_ascii = any(ord(ch) > 127 for ch in (body or ''))
            if has_non_ascii:
                # 把所有局部脚本 marker 统一升级到大写 SU；全局脚本升到 GSU
                if e.marker.upper().startswith('GS'):
                    e.marker = 'GSU'
                else:
                    e.marker = 'SU'
        e.set(1, b64_encode_script(body))

    # ---- 摘要 ----
    def summary(self) -> dict:
        from collections import Counter
        marker_count = Counter(e.marker for e in self.entries if e.marker != '')
        # NPC / Block 类型统计
        npc_ids = Counter()
        blk_ids = Counter()
        sections = []
        events = []
        scripts = []
        layers = []
        warps = 0
        for e in self.entries:
            if e.marker == 'N':
                npc_ids[e.get(1, '?')] += 1
            elif e.marker == 'B':
                blk_ids[e.get(1, '?')] += 1
            elif e.marker == 'M' and self.kind == 'lvl':
                sections.append({
                    'id':   e.get_int(0),
                    'x':    e.get_int(1),
                    'y':    e.get_int(2),
                    'w':    e.get_int(3),
                    'h':    e.get_int(4),
                    'music': e.get(11),
                    'bg':   e.get(12),
                })
            elif e.marker == 'E':
                events.append(url_decode(e.get(0, '')))
            elif e.marker in ('S', 'Su', 'SU', 'GS', 'GSu', 'GSU'):
                scripts.append({
                    'kind': e.marker,
                    'name': url_decode(e.get(0, '')),
                    'size_b64': len(e.get(1, '')),
                })
            elif e.marker in ('L', 'WL'):
                layers.append(url_decode(e.get(0, '')))
            elif e.marker == 'W':
                warps += 1
        title = ''
        for e in self.entries:
            if e.marker == 'A':
                title = url_decode(e.get(1, ''))
                break
        return {
            'kind': self.kind,
            'version': self.version,
            'newline': 'CRLF' if self.newline == '\r\n' else 'LF',
            'encoding': self.encoding,
            'title': title,
            'marker_count': dict(marker_count),
            'sections': sections,
            'layers': layers,
            'events': events,
            'scripts': scripts,
            'top_npc_ids': dict(npc_ids.most_common(20)),
            'top_block_ids': dict(blk_ids.most_common(20)),
            'total_npc': sum(npc_ids.values()),
            'total_block': sum(blk_ids.values()),
            'total_warp': warps,
            'total_event': len(events),
            'total_layer': len(layers),
            'total_script': len(scripts),
        }


# 简易 round-trip 自检（被测试脚本调用）
def assert_round_trip(path: str) -> None:
    f = SMBXFile.load(path)
    tmp = path + '.roundtrip.tmp'
    f.save(tmp)
    with open(path, 'rb') as a, open(tmp, 'rb') as b:
        ra, rb = a.read(), b.read()
    os.remove(tmp)
    if ra != rb:
        # 找出第一处差异
        for i, (x, y) in enumerate(zip(ra, rb)):
            if x != y:
                ctx_a = ra[max(0, i - 40):i + 40]
                ctx_b = rb[max(0, i - 40):i + 40]
                raise AssertionError(
                    f'round-trip diff at byte {i} (size {len(ra)} vs {len(rb)}):\n'
                    f'  ORIG: {ctx_a!r}\n   NEW: {ctx_b!r}')
        raise AssertionError(
            f'round-trip size mismatch: orig={len(ra)} new={len(rb)}')


__all__ = [
    'Entry', 'SMBXFile',
    'url_encode', 'url_encode_minimal', 'url_decode',
    'b64_encode_text', 'b64_decode_text',
    'b64_encode_script', 'b64_decode_script', 'pick_script_marker',
    'SCRIPT_BODY_ENCODING',
    'LVL_FIELD_NAMES', 'WLD_FIELD_NAMES', 'WLS_FIELD_NAMES',
    'assert_round_trip',
]
