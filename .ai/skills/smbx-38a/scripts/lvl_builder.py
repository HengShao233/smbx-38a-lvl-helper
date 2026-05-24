#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lvl_builder.py — 高层 API：从零生成符合 SMBX 38A 引擎的 .lvl 文件。

⚠️ 本模块是 AI 创建新关卡的**唯一推荐入口**。所有已知会引发
   `run-time error '13' Type Mismatch` 的格式陷阱都被这里的方法封装规避。
   AI 不要绕过本模块手写 lvl 行！

设计原则：
- 默认值都对齐真实工作关卡 (TP.lvl / MiH.lvl / Sad Land.lvl 等的实测值)。
- 字符串字段统一用 url_encode（38A 强制百分号编码）。
- 字段数量、占位符位置严格按规范。

使用：
    from lvl_builder import LVLBuilder
    b = LVLBuilder(title='My Level', p1=(-199900, -200096))
    b.add_section_grid()                                 # 一键铺 21 sections
    b.add_floor(layer='Default', y=-200032,
                x_start=-200000, x_end=-199232, blk_id=457)
    b.add_npc(npc_id=1, x=-199500, y=-200064)
    b.add_layer('Boss')
    b.add_event('Level - Start', autostart=1, script_name='Main')
    b.add_event('OnWin', show_layers=['Win'], hide_layers=['Default'])
    b.add_script('Main', open('main.tea').read())
    b.save('out.lvl')
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lvlfile import (SMBXFile, Entry, url_encode,
                     b64_encode_text, b64_encode_script, pick_script_marker)  # noqa


# 标准 21 sections 占位坐标（与 TP.lvl 风格一致）
DEFAULT_SECTION_COORDS: Tuple[Tuple[int, int], ...] = (
    (-200000, -200600), (-180000, -180600), (-160000, -160600),
    (-140000, -140600), (-120000, -120600), (-100000, -100600),
    (-80000, -80600),   (-60000, -60600),   (-40000, -40600),
    (-20000, -20600),   (0, -600),
    (20000, 19400),     (40000, 39400),     (60000, 59400),
    (80000, 79400),     (100000, 99400),    (120000, 119400),
    (140000, 139400),   (160000, 159400),   (180000, 179400),
    (200000, 199400),
)


def _f(*fields) -> List[str]:
    """把任意类型字段转字符串列表（None → 空串）。"""
    return ['' if v is None else str(v) for v in fields]


def _enc_layer(name: Optional[str]) -> str:
    """layer 字段：Default → 空串；其它 → 强制百分号编码。"""
    if not name or name == 'Default':
        return ''
    return url_encode(name)


@dataclass
class LVLBuilder:
    """SMBX 38A 关卡建造器。"""
    version: int = 69
    title: str = ''
    on_die_file: str = ''
    on_die_entrance: str = ''
    btns: Tuple[str, ...] = ('Mario', 'Luigi', 'Peach', 'Toad', 'Link')
    p1: Tuple[int, int] = (-199900, -200096)
    p2: Optional[Tuple[int, int]] = None
    stars: int = 0
    _entries: List[Entry] = field(default_factory=list)
    _sections_added: bool = False
    _layers_added: set = field(default_factory=set)
    # NPC 类配置 sidecar：{npc_id: {key: value, ...}}
    # save() 时会写到 <lvl_stem>/npc-<id>.txt
    _npc_class_configs: dict = field(default_factory=dict)


    # ---------- 内部 ----------

    def _add(self, marker: str, *fields_) -> Entry:
        e = Entry(marker=marker, fields=_f(*fields_))
        self._entries.append(e)
        return e

    # ---------- Header / Sections ----------

    def add_section_grid(self,
                         coords: Sequence[Tuple[int, int]] = DEFAULT_SECTION_COORDS,
                         w: int = 800, h: int = 600,
                         music: int = 0, background: str = '0,-1') -> None:
        """一次性铺 21 个 section（id=1..21），引擎要求必须全部声明。"""
        if self._sections_added:
            raise RuntimeError('add_section_grid() 已调用过，不可重复')
        if len(coords) != 21:
            raise ValueError('SMBX 38A 要求恰好 21 个 section (id=1..21)')
        for i, (x, y) in enumerate(coords, start=1):
            # M|id|x|y|w|h|underwater|wrapX|offexit|nbX|nbY|wrapY|music|background|musicfile
            self._add('M', i, x, y, w, h, 0, 0, 0, 0, 0, 0, music, background, '')
        self._sections_added = True

    def configure_section(self, sid: int, *,
                          x: Optional[int] = None, y: Optional[int] = None,
                          w: Optional[int] = None, h: Optional[int] = None,
                          underwater: Optional[int] = None,
                          music: Optional[int] = None,
                          background: Optional[str] = None,
                          musicfile: Optional[str] = None) -> None:
        """修改某个已存在 section（id=1..21）的字段。"""
        for e in self._entries:
            if e.marker == 'M' and e.fields and e.fields[0] == str(sid):
                if x is not None: e.fields[1] = str(x)
                if y is not None: e.fields[2] = str(y)
                if w is not None: e.fields[3] = str(w)
                if h is not None: e.fields[4] = str(h)
                if underwater is not None: e.fields[5] = str(underwater)
                if music is not None: e.fields[11] = str(music)
                if background is not None: e.fields[12] = background
                if musicfile is not None:
                    e.fields[13] = url_encode(musicfile)
                return
        raise ValueError(f'section id={sid} 不存在；先调用 add_section_grid()')

    # ---------- Block / BGO / NPC ----------

    def add_block(self, *, blk_id: int, x: int, y: int,
                  layer: str = 'Default',
                  w: int = 32, h: int = 32,
                  contain: int = 0,         # 0=无，金币数 / NPC id+1000
                  slippery: int = 0,
                  invisible: int = 0,
                  destroy_evt: str = '', hit_evt: str = '', empty_evt: str = '') -> None:
        """B|layer|id|x|y|contain|slippery|invisible|destroyEvt,hitEvt,emptyEvt|w|h"""
        # contain 字段：0 必须写空字符串（这是引擎陷阱）
        contain_field = '' if contain == 0 else str(contain)
        events = ''
        if destroy_evt or hit_evt or empty_evt:
            events = ','.join(url_encode(x) for x in (destroy_evt, hit_evt, empty_evt))
        self._add('B', _enc_layer(layer), blk_id, x, y,
                  contain_field, slippery, invisible, events, w, h)

    def add_bgo(self, *, bgo_id: int, x: int, y: int,
                layer: str = 'Default') -> None:
        """T|layer|id|x|y"""
        self._add('T', _enc_layer(layer), bgo_id, x, y)

    def add_npc(self, *, npc_id: int, x: int, y: int,
                layer: str = 'Default',
                facing: int = 0,        # 1=左, 0=随机, -1=右
                friendly: int = 0,
                nomove: int = 0,
                container_type: int = 0,  # b4
                b5: int = 0, b6: int = 0,
                sp: int = 0,
                events_csv: str = '',
                attach: str = '',
                generator: str = '0',
                msg: str = '') -> None:
        """N|layer|id|x|y|b1,b2,b3,b4,b5,b6|sp|events|attach|generator|msg

        ⚠ 关键：b 字段必须 6 个数；events / attach 无值时必须空字符串而非占位 0。
        """
        b_field = f'{facing},{friendly},{nomove},{container_type},{b5},{b6}'
        self._add('N', _enc_layer(layer), npc_id, x, y,
                  b_field, sp, events_csv, attach, generator,
                  url_encode(msg) if msg else '')

    def add_warp(self, *, x: int, y: int, ex: int, ey: int,
                 layer: str = 'Default',
                 type_: int = 2,        # 0=instant 1=pipe 2=door
                 enter_dir: int = 3,    # 1=up 2=left 3=down 4=right
                 exit_dir: int = 1,
                 stars_cfg: str = '0,,1',
                 flags_csv: str = '0,0,0,0,1,0,0,32,0,0,0',
                 lik: str = '',
                 noexit: int = 0,
                 wx: int = 0, wy: int = 0, le: int = 0, we: int = 1,
                 with_visual: bool = True,
                 visual_bgo_id: int = 92,
                 visual_at_entry: bool = True,
                 visual_at_exit: bool = True,
                 visual_layer: Optional[str] = None) -> None:
        """W|layer|x|y|ex|ey|type|enterd|exitd|sn,msg,hide|flags|lik|liid|noexit|wx|wy|le|we

        ⚠ **传送门 = 逻辑触发区 + 视觉图形** —— 是两件事!
        SMBX 的 W 行只是个不可见的"碰到此格按上键就传送"的判定区，
        玩家**完全看不到**它。如果不另放门 BGO / 管道方块，玩家
        会一脸懵 "为什么这格地面会突然把我送走？"。

        本方法默认会在传送门入口和出口处都自动放上门 BGO（type_=2 时）。
        如果不想要默认门，传 `with_visual=False` 自己手动放置。

        参数:
            with_visual: type_=2 (door) 时自动放门 BGO；type_=1 (pipe)
                时本参数无效（管道图形需用方块自行搭），type_=0 (instant)
                则不放视觉。默认 True。
            visual_bgo_id: 门 BGO 的 id。基于本仓库 60 个真实关卡统计：
                92 (默认门)、79、87、158、168 是最常见门 BGO。
            visual_at_entry / visual_at_exit: 是否分别在入口和出口放门。
                如果出口在另一个 section（比如 warp 到 boss 房），
                通常两边都要门。默认两边都放。
            visual_layer: 门 BGO 的图层名。None=用 warp 同图层。
        """
        self._add('W', _enc_layer(layer), x, y, ex, ey,
                  type_, enter_dir, exit_dir,
                  stars_cfg, flags_csv,
                  url_encode(lik) if lik else '',
                  0, noexit, wx, wy, le, we, '')

        # ---- 自动放门 BGO ----
        # 只有 type_=2 (door) 才自动放视觉；管道/instant 由调用方自理
        if with_visual and type_ == 2:
            vlayer = visual_layer or layer
            # 门 BGO 是 32x64（两格高），锚点在左上 → 放在 (warp_x, warp_y - 32)
            # 这样门覆盖 (y - 32) 到 (y + 32) 共 64 像素，正好 warp 那一格
            # 在门下半的位置，玩家踩在门里。
            if visual_at_entry:
                self.add_bgo(bgo_id=visual_bgo_id, x=x, y=y - 32, layer=vlayer)
            if visual_at_exit and (ex, ey) != (x, y):
                self.add_bgo(bgo_id=visual_bgo_id, x=ex, y=ey - 32, layer=vlayer)

    def add_door_visual(self, *, x: int, y: int,
                        bgo_id: int = 92,
                        layer: str = 'Default') -> None:
        """在指定位置放一个标准门 BGO（仅视觉，不带传送逻辑）。

        x/y 应该是玩家踩位置（即 warp 的 (x, y)），方法会把 BGO 放在
        (x, y - 32)，使门视觉自然立在玩家身后。

        当你需要单独造门图形（例如门是装饰、或想让一个门覆盖多个 warp 时）
        使用本方法；常规 add_warp 已默认带门。

        实测最常用门 BGO id 候选（按出现频次排序）：
            92 (默认门), 79, 87, 158, 168, 87
        """
        self.add_bgo(bgo_id=bgo_id, x=x, y=y - 32, layer=layer)


    def add_liquid(self, *, x: int, y: int, w: int, h: int,
                   layer: str = 'Default',
                   liquid_type: int = 4,
                   friction: float = 0.1,
                   max_speed: float = -1, b4: float = 0, b5: float = 0,
                   event: str = '') -> None:
        """Q|layer|x|y|w|h|b1..b5|event"""
        b = f'{liquid_type},{friction},{max_speed},{b4},{b5}'
        self._add('Q', _enc_layer(layer), x, y, w, h, b,
                  url_encode(event) if event else '')

    # ---------- Layer ----------

    def add_layer(self, name: str, status: int = 1) -> None:
        """L|<encoded_name>|status   layer 名必须强制百分号编码。"""
        if name in self._layers_added:
            return
        self._layers_added.add(name)
        self._add('L', url_encode(name), status)

    # ---------- Variable ----------

    def add_variable(self, name: str, value=0, scope: int = 0) -> None:
        """V|<encoded_name>|<value>|<scope>

        ⚠ 关键：name 必须仅含字母数字、字母开头（无下划线）；
           V 行必须 3 字段（不能省 scope）。
           scope: 0=local（关卡内）, 1=global（跨关卡持久；需要 wls 中也有同名 G 行）
           ⚠ V 行**不能用来声明用户数组**——数组用 add_array() 写 R 行。
        """
        import re
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', name):
            raise ValueError(
                f'变量名 {name!r} 不合法：必须字母开头、只含字母数字、不含下划线。'
                ' (TeaScript 命名规约 + 引擎严格校验)'
            )
        self._add('V', url_encode(name), value, scope)

    def add_array(self, *names: str) -> None:
        """R|<arr1>|<arr2>|...   声明一个或多个用户数组。

        ⚠ 38A 的用户数组（user array）**不**用 V 行声明，而是用 R 行。
        所有数组通常写在**同一行 R 行**中，每个名字一段；脚本里用：
            call redim(0, arrName, length)
            array(arrName(idx)) = value
        每个数组名遵循通用变量命名规约（字母开头、仅字母数字、无下划线）。

        典型写法：
            b.add_array('echoX', 'echoY')
        """
        import re
        if not names:
            return
        encoded = []
        for n in names:
            if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', n):
                raise ValueError(
                    f'数组名 {n!r} 不合法：必须字母开头、只含字母数字、不含下划线。'
                )
            encoded.append(url_encode(n))
        # 直接构造一个 R 行；fields 就是 [arr1, arr2, ...]
        self._add('R', *encoded)


    # ---------- Event ----------

    def _build_el(self, b: int, show: Sequence[str], hide: Sequence[str],
                  toggle: Sequence[str]) -> str:
        """el = b/show_csv/hide_csv/toggle_csv (4 段斜杠分隔)。"""
        def csv(layers):
            return ','.join(url_encode(L) for L in layers)
        return f'{b}/{csv(show)}/{csv(hide)}/{csv(toggle)}'

    def _build_ene(self, *,
                   next_event: str = '', next_delay: int = 0,
                   timer_enable: int = 0, timer_count: int = 0,
                   timer_interval: int = 0, timer_type: int = 0,
                   timer_show: int = 0,
                   apievent: int = 0,
                   script_name: str = '') -> str:
        """ene = nextevent/timer[/apievent[/scriptname]]
        ⚠ 关键：绑定脚本时 apievent 段必须写 "0"（不能空），否则 type mismatch！
        """
        nextevent = f'{url_encode(next_event)},{next_delay}'
        timer = f'{timer_enable},{timer_count},{timer_interval},{timer_type},{timer_show}'
        sn = url_encode(script_name) if script_name else ''
        api = str(apievent)
        if sn:
            return f'{nextevent}/{timer}/{api}/{sn}'
        if apievent != 0:
            return f'{nextevent}/{timer}/{api}'
        return f'{nextevent}/{timer}'

    def add_event(self, name: str, *,
                  autostart: int = 0,        # 0=否 1=Level Start 2=条件 3=Call+条件
                  msg: str = '',
                  show_layers: Iterable[str] = (),
                  hide_layers: Iterable[str] = (),
                  toggle_layers: Iterable[str] = (),
                  el_b: int = 0,
                  elm: str = '',
                  epy: str = '0,0,0,0,0,0,0,0,0,0,0,0',
                  eps: str = '//',
                  eef: str = '0/0',
                  ecn: str = '',
                  evc: str = '',
                  next_event: str = '', next_delay: int = 0,
                  apievent: int = 0,
                  script_name: str = '',
                  ) -> None:
        """E|name|msg|ea|el|elm|epy|eps|eef|ecn|evc|ene"""
        el = self._build_el(el_b, list(show_layers), list(hide_layers), list(toggle_layers))
        ene = self._build_ene(next_event=next_event, next_delay=next_delay,
                              apievent=apievent, script_name=script_name)
        self._add('E',
                  url_encode(name), url_encode(msg) if msg else '',
                  f'{autostart},', el, elm, epy, eps, eef, ecn, evc, ene)

    # ---------- Script ----------

    def add_script(self, name: str, body: str,
                   force_marker: Optional[str] = None) -> None:
        """嵌入 TeaScript 脚本到 lvl。

        ⚠ 38A 引擎实测踩坑（基于真实工作关卡 `main.lvl` 字节级抽样）：
            - **Marker 用大写 `SU`**（不是文档说的 `Su`）。lvlfile 默认就这么写。
            - **Body 用系统 ANSI / GBK 字节做 base64**（中文 Windows 上的 38A
              是 VB6 应用，用 CP936 处理字符串）。如果用 UTF-8 字节，引擎按
              GBK 解读会乱码 + 字符边界错乱（行尾 LF 被当成多字节字符的补字节）。

        Args:
            name: 脚本名（必须字母开头、仅字母数字）。
            body: 脚本源码（Python str）。
            force_marker: 强制使用某个 marker（'S'/'Su'/'SU'/'GS'/'GSu'/'GSU'），
                仅在你确定知道引擎能正确解码时使用；正常情况下不传。

        生成行：`SU|<encoded_name>|<base64(gbk bytes)>`
        """
        import re
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', name):
            raise ValueError(
                f'脚本名 {name!r} 不合法：必须字母开头、只含字母数字、不含下划线（TeaScript 命名规约）'
            )
        marker = force_marker if force_marker else pick_script_marker(body)
        # b64_encode_script 默认用 GBK 字节，与 38A 引擎期望一致
        self._add(marker, url_encode(name), b64_encode_script(body))

    # ---------- Custom Texture / Sound ----------

    def add_custom_texture(self, obj_id: int, hash_str: str = '00081') -> None:
        """CT|id|hash —— 自定义贴图占位条目。"""
        self._add('CT', obj_id, hash_str)

    # ---------- NPC 类配置（sidecar npc-<id>.txt） ----------

    def add_npc_class_config(self, npc_id: int, **kv) -> None:
        """写一个 `<lvl_stem>/npc-<id>.txt` 配置（INI 风格键值对）。

        常用键：
            scripts=<scriptName>     ' 把脚本绑成"每帧每实例"类绑定（关键！）
            gfxwidth=<int>           ' 修改该 type NPC 的渲染宽度
            gfxheight=<int>          ' 修改该 type NPC 的渲染高度
            playerblock=1            ' 修改 NPC flag
            ' ... 详见 38A editor 的 NPC 属性编辑器

        多次调用同一 npc_id 会**合并**键值（同名键覆盖）。

        使用：
            b.add_npc_class_config(13, scripts='FireBall')
            b.add_npc_class_config(13, gfxwidth=26, gfxheight=46)
        """
        cfg = self._npc_class_configs.setdefault(int(npc_id), {})
        for k, v in kv.items():
            cfg[str(k)] = '' if v is None else str(v)

    def add_npc_class_script(self, npc_id: int, script_name: str,
                             script_body: Optional[str] = None,
                             **extra_config) -> None:
        """便捷方法：把脚本 `script_name` 类绑定到 type=`npc_id` 的所有 NPC。

        效果（save 时一并完成）：
          1. 在 lvl 文件中嵌入 `SU|<script_name>|<base64>` (如果给了 script_body)
          2. 在 `<lvl_stem>/npc-<id>.txt` 写入 `scripts=<script_name>`
             + 任何额外的 `extra_config` 键值对（如 gfxwidth）

        如果 script_body 为 None，则**只写 sidecar 配置**（你已经手动 add_script 过了）。

        ⚠ 类绑定脚本本体**不要写 `do ... loop`** —— 引擎已每帧自动调用一次。

        ⚠ 脚本里**没有"隐式 with"上下文**——访问当前实例必须显式：
            dim selfIdx as integer
            selfIdx = sysval(param1)     ' 当前 NPC 的索引
            with NPC(selfIdx)
                .x = .x + 1               ' with 块内才能用 leading-dot
            end with

        示例：
            b.add_npc_class_script(13, 'FireBall',
                                   open('FireBall.tea').read(),
                                   gfxwidth=26, gfxheight=46)
        """
        if script_body is not None:
            self.add_script(script_name, script_body)
        self.add_npc_class_config(npc_id, scripts=script_name, **extra_config)




    # ---------- 输出 ----------

    def build(self) -> SMBXFile:
        """组合 header + 所有条目，返回 SMBXFile 对象。"""
        if not self._sections_added:
            self.add_section_grid()  # 自动补 21 sections

        f = SMBXFile(version=self.version, kind='lvl',
                     newline='\r\n', encoding='ascii', entries=[])
        # A | stars | title | onDieFile | onDieEntrance | extra(",,,")
        f.entries.append(Entry(marker='A', fields=_f(
            self.stars, url_encode(self.title),
            url_encode(self.on_die_file), url_encode(self.on_die_entrance),
            ',,,'
        )))
        # BTNS | Mario | Luigi | Peach | Toad | Link
        f.entries.append(Entry(marker='BTNS', fields=list(self.btns)))
        # P1 | x | y
        f.entries.append(Entry(marker='P1', fields=_f(self.p1[0], self.p1[1])))
        if self.p2 is not None:
            f.entries.append(Entry(marker='P2', fields=_f(self.p2[0], self.p2[1])))
        # 其余条目（M/B/T/N/W/Q/L/V/E/S/...）按添加顺序
        f.entries.extend(self._entries)
        return f

    def save(self, out_path: str, validate: bool = True) -> None:
        """保存到指定路径。validate=True 时调用 lvl_validate 自检。

        如果 add_npc_class_config / add_npc_class_script 注册过 NPC 类配置，
        会同时把它们写到 `<out_path 同名目录>/npc-<id>.txt`（sidecar 文件）。
        """
        f = self.build()
        f.save(out_path)

        # ---- 写 NPC 类配置 sidecar 文件 ----
        if self._npc_class_configs:
            stem, _ = os.path.splitext(out_path)
            sidecar_dir = stem  # 与 lvl 同名（无扩展名）的目录
            os.makedirs(sidecar_dir, exist_ok=True)
            for npc_id, cfg in self._npc_class_configs.items():
                sidecar_path = os.path.join(sidecar_dir, f'npc-{npc_id}.txt')
                lines = [f'{k}={v}' for k, v in cfg.items()]
                with open(sidecar_path, 'w', encoding='ascii', newline='\r\n') as fh:
                    fh.write('\n'.join(lines) + '\n')

        if validate:
            from lvl_validate import lint_file
            diags = lint_file(out_path)
            errs = [d for d in diags if d.severity == 'error']
            if errs:
                print(f'[lvl_builder] ⚠ {len(errs)} 个校验错误：')
                for d in errs:
                    print(f'  {out_path}:{d.line}: [{d.rule}] {d.marker}: {d.message}')
                raise RuntimeError(
                    f'输出文件未通过 lvl_validate（{len(errs)} 错误）。请修正后重试。'
                )



__all__ = ['LVLBuilder', 'DEFAULT_SECTION_COORDS']
