#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engine_control.py — SMBX 38A 引擎运行时高层控制封装。

子命令一览：
    launch       启动 smbx.exe 进入 testing 模式（命令行参数符合 38A 规范）
    reload       重启 smbx 加载指定 lvl（先 kill 再 launch）
    kill         结束所有 smbx.exe 进程
    ping         IPC ping
    state        查询状态（对象数 / 玩家 / 相机 / 变量）
    trigger      触发事件 (SET)
    layer        显隐图层 (SLT)
    message      显示一个消息框 (TMG)
    create       创建 NPC/Block/BGO（CN/CB/CT）
    cursor       设置编辑器光标 (SO)
    raw          直发原始命令

依赖：
- 仅 Windows
- ipc_client.py 同目录
- smbx.exe 路径需通过 --smbx 参数显式提供（首次使用后可缓存到 .smbx_path）
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ipc_client import SMBXIPC, IPCError  # noqa
from lvlfile import url_encode  # noqa

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.smbx_path')


# ---- smbx.exe 路径管理 ----
def get_smbx_path(args_path: Optional[str]) -> str:
    if args_path:
        if not os.path.isfile(args_path):
            raise SystemExit(f'smbx.exe 不存在：{args_path}')
        # 缓存
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as fh:
                fh.write(args_path)
        except OSError:
            pass
        return args_path
    if os.path.isfile(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as fh:
            p = fh.read().strip()
        if os.path.isfile(p):
            return p
    raise SystemExit(
        '请用 --smbx <path-to-smbx.exe> 指定一次（之后会缓存到 .smbx_path）。')


def kill_smbx() -> None:
    if not sys.platform.startswith('win'):
        return
    try:
        subprocess.run(['taskkill', '/IM', 'smbx.exe', '/F'],
                       check=False, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        pass


def launch_smbx(smbx_path: str, lvl: str, mode: int = 0,
                p1: int = 0, p2: int = 1,
                args_str: Optional[str] = None,
                cwd: Optional[str] = None) -> subprocess.Popen:
    """以 testing 模式启动。args_str 应为 38A 文档中的 SMBXArgs|...|...|... 形式（未编码）；
    本函数自动 url-encode。"""
    if not sys.platform.startswith('win'):
        raise SystemExit('仅 Windows 支持启动 smbx.exe')
    if not os.path.isfile(lvl):
        raise SystemExit(f'lvl 文件不存在：{lvl}')
    cmd = [smbx_path, lvl, str(mode), str(p1), str(p2)]
    if args_str:
        cmd.append(url_encode(args_str))
    print('[engine] launching:', ' '.join(shlex.quote(x) for x in cmd))
    return subprocess.Popen(cmd, cwd=cwd or os.path.dirname(smbx_path))


# ---- 各子命令 ----
def cmd_launch(args):
    smbx = get_smbx_path(args.smbx)
    p = launch_smbx(smbx, args.lvl, args.mode, args.p1, args.p2, args.args)
    if args.wait_ipc:
        # 等 IPC 上线
        deadline = time.monotonic() + args.wait_ipc
        last_err = None
        while time.monotonic() < deadline:
            try:
                with SMBXIPC() as ipc:
                    msgs = ipc.send_recv('GGI|ON', timeout=0.5, expect_prefix='GGI|ON')
                    if msgs:
                        print(f'[engine] IPC online; pid={p.pid}; reply: {msgs[0]}')
                        return 0
            except IPCError as e:
                last_err = e
            time.sleep(0.4)
        print(f'[engine] launched pid={p.pid} but IPC not online within {args.wait_ipc}s; last={last_err}',
              file=sys.stderr)
        return 1
    print(f'[engine] launched pid={p.pid}')
    return 0


def cmd_reload(args):
    smbx = get_smbx_path(args.smbx)
    kill_smbx()
    time.sleep(0.4)
    return cmd_launch(args)


def cmd_kill(args):
    kill_smbx()
    print('[engine] kill smbx.exe done')
    return 0


def cmd_ping(args):
    try:
        with SMBXIPC() as ipc:
            r = ipc.send_recv('GGI|ON', timeout=args.timeout, expect_prefix='GGI|ON')
            if not r:
                print('[engine] no response'); return 1
            print('[engine] ping ok ->', r[0])
            return 0
    except IPCError as e:
        print(f'[engine] {e}', file=sys.stderr); return 2


def _send(ipc: SMBXIPC, cmd: str, timeout: float, expect: Optional[str] = None):
    return ipc.send_recv(cmd, timeout=timeout, expect_prefix=expect)


def cmd_state(args):
    out = {}
    with SMBXIPC() as ipc:
        if args.object_count or args.all:
            r = _send(ipc, 'GGI|ON', args.timeout, 'GGI|ON')
            out['object_count_raw'] = r
            for m in r:
                if m.startswith('GGI|ON|'):
                    parts = m.split('|')[2:]
                    keys = ['block', 'bgo', 'npc', 'warp', 'liquid']
                    out['object_count'] = dict(zip(keys, parts))
        if args.layer_event_count or args.all:
            r = _send(ipc, 'GGI|LN', args.timeout, 'GGI|LN')
            out['layer_event_count_raw'] = r
            for m in r:
                if m.startswith('GGI|LN|'):
                    parts = m.split('|')[2:]
                    out['layer_event_count'] = dict(zip(['layers', 'events'], parts))
        if args.player or args.all:
            r = _send(ipc, 'GGI|PI', args.timeout, 'GGI|PIT')
            out['player_raw'] = r
        if args.camera or args.all:
            r = _send(ipc, 'GGI|VP', args.timeout, 'GGI|VP')
            out['camera_raw'] = r
        if args.cursor or args.all:
            r = _send(ipc, 'GGI|CP', args.timeout, 'GGI|CP')
            out['cursor_raw'] = r
        if args.var:
            cmd = 'GGI|VV|' + url_encode(args.var)
            r = _send(ipc, cmd, args.timeout, 'GGI|VV')
            out[f'var:{args.var}_raw'] = r
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_trigger(args):
    with SMBXIPC() as ipc:
        ipc.send_command('SET|' + url_encode(args.event), timeout=args.timeout)
    print(f'[engine] triggered event: {args.event}')
    return 0


def cmd_layer(args):
    type_map = {'show': 1, 'hide': 2, 'toggle': 3}
    t = type_map.get(args.action.lower())
    if t is None:
        raise SystemExit('action must be one of show/hide/toggle')
    cmd = f'SLT|{url_encode(args.name)}|{t}|{0 if args.smoke else 1}'
    with SMBXIPC() as ipc:
        ipc.send_command(cmd, timeout=args.timeout)
    print(f'[engine] layer {args.action} -> {args.name!r}')
    return 0


def cmd_message(args):
    with SMBXIPC() as ipc:
        ipc.send_command('TMG|' + url_encode(args.text), timeout=args.timeout)
    print(f'[engine] message shown: {args.text!r}')
    return 0


def cmd_create(args):
    """创建对象。data 形式与 LVL 行去掉 marker 后的字段串相同，例如：
        --kind N --data "Default|1|100|-120||0|0|||"
    或者通过命名字段构造（最常用情形）：
        --kind N --layer Default --id 1 --x 100 --y -120
    """
    if args.data:
        body = args.data
    else:
        # 分 marker 拼最小字段串
        if args.kind == 'B':
            body = f"{url_encode(args.layer)}|{args.id}|{args.x}|{args.y}|{args.contain or ''}|0|0||{args.w}|{args.h}"
        elif args.kind == 'T':
            body = f"{url_encode(args.layer)}|{args.id}|{args.x}|{args.y}"
        elif args.kind == 'N':
            body = f"{url_encode(args.layer)}|{args.id}|{args.x}|{args.y}|0,0,0,0||,,,,,,||0|"
        else:
            raise SystemExit('--kind must be one of B/T/N')
    marker_to_cmd = {'B': 'CB', 'T': 'CT', 'N': 'CN'}
    raw = f"{marker_to_cmd[args.kind]}|{body}"
    with SMBXIPC() as ipc:
        ipc.send_command(raw, timeout=args.timeout)
    print(f'[engine] created {args.kind}: {raw}')
    return 0


def cmd_cursor(args):
    map_ = {'off': 'SO', 'cursor': 'SO|CURSOR', 'eraser': 'SO|ERASER'}
    raw = map_.get(args.mode)
    if raw is None:
        raise SystemExit('mode must be off/cursor/eraser')
    with SMBXIPC() as ipc:
        ipc.send_command(raw, timeout=args.timeout)
    print(f'[engine] cursor -> {args.mode}')
    return 0


def cmd_raw(args):
    with SMBXIPC() as ipc:
        msgs = ipc.send_recv(args.command, timeout=args.timeout, expect_prefix=args.expect)
    for m in msgs:
        print(m)
    return 0 if msgs or not args.expect else 1


def main():
    ap = argparse.ArgumentParser(description='SMBX 38A engine controller.')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('launch', help='以 testing 模式启动 smbx.exe')
    p.add_argument('--smbx', help='smbx.exe 路径（首次必填，之后缓存到 .smbx_path）')
    p.add_argument('--lvl', required=True)
    p.add_argument('--mode', type=int, default=0, help='0=单人 1=双人 2=对战')
    p.add_argument('--p1', type=int, default=0)
    p.add_argument('--p2', type=int, default=1)
    p.add_argument('--args', help='SMBXArgs|hp,co,sr|p1p,p1i,p2p,p2i|levelname,cppid,cpidn（未编码）')
    p.add_argument('--wait-ipc', type=float, default=10.0,
                   help='等 IPC 上线的秒数；0=不等')
    p.set_defaults(func=cmd_launch)

    p = sub.add_parser('reload', help='kill 当前 smbx.exe 后重新 launch')
    p.add_argument('--smbx')
    p.add_argument('--lvl', required=True)
    p.add_argument('--mode', type=int, default=0)
    p.add_argument('--p1', type=int, default=0)
    p.add_argument('--p2', type=int, default=1)
    p.add_argument('--args')
    p.add_argument('--wait-ipc', type=float, default=10.0)
    p.set_defaults(func=cmd_reload)

    p = sub.add_parser('kill', help='taskkill /IM smbx.exe /F')
    p.set_defaults(func=cmd_kill)

    p = sub.add_parser('ping')
    p.add_argument('--timeout', type=float, default=1.0)
    p.set_defaults(func=cmd_ping)

    p = sub.add_parser('state', help='查询游戏状态')
    p.add_argument('--object-count', action='store_true')
    p.add_argument('--layer-event-count', action='store_true')
    p.add_argument('--player', action='store_true')
    p.add_argument('--camera', action='store_true')
    p.add_argument('--cursor', action='store_true')
    p.add_argument('--var', help='查询变量名')
    p.add_argument('--all', action='store_true')
    p.add_argument('--timeout', type=float, default=0.8)
    p.set_defaults(func=cmd_state)

    p = sub.add_parser('trigger', help='触发事件 SET|<event>')
    p.add_argument('--event', required=True)
    p.add_argument('--timeout', type=float, default=0.6)
    p.set_defaults(func=cmd_trigger)

    p = sub.add_parser('layer', help='图层显隐 SLT')
    p.add_argument('--name', required=True)
    p.add_argument('--action', required=True, choices=['show', 'hide', 'toggle'])
    p.add_argument('--smoke', action='store_true', help='保留烟雾效果（默认无烟）')
    p.add_argument('--timeout', type=float, default=0.6)
    p.set_defaults(func=cmd_layer)

    p = sub.add_parser('message', help='显示消息框 TMG')
    p.add_argument('--text', required=True)
    p.add_argument('--timeout', type=float, default=0.6)
    p.set_defaults(func=cmd_message)

    p = sub.add_parser('create', help='创建对象 CB/CN/CT')
    p.add_argument('--kind', required=True, choices=['B', 'N', 'T'])
    p.add_argument('--data', help='手写完整数据串（覆盖以下命名字段）')
    p.add_argument('--layer', default='Default')
    p.add_argument('--id', default='1')
    p.add_argument('--x', default='0')
    p.add_argument('--y', default='0')
    p.add_argument('--w', default='32')
    p.add_argument('--h', default='32')
    p.add_argument('--contain', default='')
    p.add_argument('--timeout', type=float, default=0.6)
    p.set_defaults(func=cmd_create)

    p = sub.add_parser('cursor', help='切换编辑器光标 SO')
    p.add_argument('--mode', required=True, choices=['off', 'cursor', 'eraser'])
    p.add_argument('--timeout', type=float, default=0.6)
    p.set_defaults(func=cmd_cursor)

    p = sub.add_parser('raw', help='发送任意原始命令并打印响应')
    p.add_argument('command')
    p.add_argument('--expect', help='期望响应前缀')
    p.add_argument('--timeout', type=float, default=1.0)
    p.set_defaults(func=cmd_raw)

    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
