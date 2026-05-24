#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
session.py — SMBX 38A 测试会话与 editor 进程管理。

它把 launch / wait IPC / run tests / screenshot / user review / stop 串成一个高层 SOP。
也提供 SMBX 可执行文件（包括 editor）路径的智能查找：
    1) 先看缓存 (.smbx_path / .smbx_editor_path)
    2) 看用户当前运行中的 smbx*.exe 进程，从其 ImagePath 读取
    3) 检索常见安装目录（C:/SMBX*, D:/SMBX*, %ProgramFiles%/SMBX*, 项目根 SMBX*）
    4) 都找不到 → 退出并打印清晰的指引让用户传 --smbx-path

子命令：
    locate           定位 smbx 可执行（仅打印结果，不启动）
    locate-editor    定位 smbx editor（不区分大小写匹配 *editor*.exe）
    list-procs       列出运行中的 SMBX 系列进程
    open-editor      启动 SMBX Editor（带可选 --lvl）
    run              一键测试会话：launch testing -> wait IPC -> 触发事件 -> screenshot -> review -> stop
    stop             停止由本工具启动的会话（或 taskkill 全部）

CLI 例子：
    python session.py locate
    python session.py list-procs
    python session.py open-editor --editor "C:/SMBX38A/editor.exe" --lvl path/to/level.lvl
    python session.py run --lvl path/to/level.lvl --trigger "OnFoo" --screenshot ".cache/snap.png"
    python session.py stop
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ipc_client import SMBXIPC, IPCError  # noqa
from lvlfile import url_encode  # noqa

CACHE_SMBX = os.path.join(HERE, '.smbx_path')
CACHE_EDITOR = os.path.join(HERE, '.smbx_editor_path')
SESSION_FILE = os.path.join(HERE, '.session.json')

IS_WIN = sys.platform.startswith('win')

# ---- 常见安装路径搜索 ----
COMMON_HINTS = [
    'SMBX38A', 'SMBX-38A', 'SMBX 38A', 'smbx-38a', 'smbx38a',
    'SMBX', 'SMBX2', 'SMBX 2',
]


def _all_drives() -> List[str]:
    if not IS_WIN:
        return ['/']
    drives = []
    for letter in 'CDEFGHIJKLMN':
        p = f'{letter}:\\'
        if os.path.isdir(p):
            drives.append(p)
    return drives


def _find_in_dir(d: str, name_pattern: re.Pattern, max_depth: int = 2) -> List[str]:
    """在 d 下浅扫描匹配 name_pattern 的 exe；最大深度 max_depth。"""
    out: List[str] = []
    if not os.path.isdir(d):
        return out
    base_depth = d.rstrip('\\/').count(os.sep)
    try:
        for root, dirs, files in os.walk(d):
            depth = root.count(os.sep) - base_depth
            if depth > max_depth:
                dirs[:] = []
                continue
            for fn in files:
                if name_pattern.search(fn):
                    out.append(os.path.join(root, fn))
    except (OSError, PermissionError):
        pass
    return out


def find_candidates(kind: str = 'smbx') -> List[str]:
    """
    kind: 'smbx' -> smbx.exe（运行游戏 / testing 模式入口）
          'editor' -> 任何 *editor*.exe 或 *38a*.exe（在 SMBX 38A 中编辑器与运行同一可执行
                       的可能性也存在；返回 .exe 让用户挑）
    """
    pattern = re.compile(r'(?i)^smbx\.exe$|smbx[-_ ]?editor.*\.exe$|38a.*editor.*\.exe$')
    if kind == 'smbx':
        pattern = re.compile(r'(?i)^smbx\.exe$|^smbx[-_ ]?38a\.exe$')

    found: List[str] = []
    seen = set()
    # 1) cache
    cache = CACHE_SMBX if kind == 'smbx' else CACHE_EDITOR
    if os.path.isfile(cache):
        try:
            p = open(cache, encoding='utf-8').read().strip()
            if p and os.path.isfile(p):
                found.append(p); seen.add(p.lower())
        except OSError:
            pass
    # 2) 运行中的进程
    for img in _running_smbx_image_paths():
        if pattern.search(os.path.basename(img)) and img.lower() not in seen:
            found.append(img); seen.add(img.lower())
    # 3) 常见安装路径
    if IS_WIN:
        for drive in _all_drives():
            for hint in COMMON_HINTS:
                d = os.path.join(drive, hint)
                if os.path.isdir(d):
                    for p in _find_in_dir(d, pattern):
                        if p.lower() not in seen:
                            found.append(p); seen.add(p.lower())
    # 4) Program Files
    for env in ('ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432'):
        base = os.environ.get(env)
        if not base:
            continue
        for hint in COMMON_HINTS:
            d = os.path.join(base, hint)
            for p in _find_in_dir(d, pattern):
                if p.lower() not in seen:
                    found.append(p); seen.add(p.lower())
    # 5) 项目根
    proj_root = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
    for hint in COMMON_HINTS + ['']:
        d = os.path.join(proj_root, hint) if hint else proj_root
        for p in _find_in_dir(d, pattern, max_depth=3):
            if p.lower() not in seen:
                found.append(p); seen.add(p.lower())
    return found


def _running_smbx_image_paths() -> List[str]:
    """通过 WMI 拿出当前所有 *smbx*.exe / *editor*.exe 的可执行完整路径。"""
    if not IS_WIN:
        return []
    out: List[str] = []
    # 尝试 WMIC（旧）/ PowerShell Get-CimInstance（新）
    cmds = [
        ['wmic', 'process', 'where',
         "name like 'smbx%.exe' or name like '%editor%.exe'",
         'get', 'ExecutablePath', '/format:list'],
    ]
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
            if r.returncode == 0 and r.stdout:
                for line in r.stdout.splitlines():
                    line = line.strip()
                    if line.lower().startswith('executablepath='):
                        p = line.split('=', 1)[1].strip()
                        if p and os.path.isfile(p):
                            out.append(p)
                if out:
                    return out
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
    # PowerShell fallback
    try:
        ps = ('Get-CimInstance Win32_Process -Filter '
              '"name like \'smbx%%.exe\' or name like \'%%editor%%.exe\'" | '
              'Select-Object -ExpandProperty ExecutablePath')
        r = subprocess.run(['powershell', '-NoProfile', '-Command', ps],
                           capture_output=True, text=True, timeout=4)
        if r.returncode == 0 and r.stdout:
            for line in r.stdout.splitlines():
                p = line.strip()
                if p and os.path.isfile(p):
                    out.append(p)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return out


def list_running() -> List[dict]:
    """返回当前所有 smbx 系进程基本信息。"""
    if not IS_WIN:
        return []
    rows: List[dict] = []
    try:
        ps = ("Get-CimInstance Win32_Process -Filter "
              "\"name like 'smbx%%.exe' or name like '%%editor%%.exe'\" | "
              "Select-Object ProcessId,Name,ExecutablePath,CommandLine | "
              "ConvertTo-Json -Compress")
        r = subprocess.run(['powershell', '-NoProfile', '-Command', ps],
                           capture_output=True, text=True, timeout=4)
        if r.returncode == 0 and r.stdout.strip():
            data = json.loads(r.stdout)
            if isinstance(data, dict):
                data = [data]
            for d in data:
                rows.append({
                    'pid': d.get('ProcessId'),
                    'name': d.get('Name'),
                    'path': d.get('ExecutablePath'),
                    'cmdline': d.get('CommandLine'),
                })
    except Exception:
        pass
    return rows


def cache_path(path: str, kind: str = 'smbx') -> None:
    target = CACHE_SMBX if kind == 'smbx' else CACHE_EDITOR
    try:
        with open(target, 'w', encoding='utf-8') as fh:
            fh.write(path)
    except OSError:
        pass


# ---- 路径解析 + 用户引导 ----
def resolve_path(args_path: Optional[str], kind: str = 'smbx',
                 strict: bool = True) -> str:
    if args_path:
        if not os.path.isfile(args_path):
            raise SystemExit(f'路径不存在：{args_path}')
        cache_path(args_path, kind=kind)
        return args_path

    cands = find_candidates(kind)
    if cands:
        cache_path(cands[0], kind=kind)
        return cands[0]

    if not strict:
        return ''

    # 无法找到 → 打印明确指引
    label = 'SMBX editor 可执行文件' if kind == 'editor' else 'smbx.exe'
    sys.stderr.write(
        '\n' + '=' * 60 + '\n'
        f'❌ 找不到 {label}。\n\n'
        '请按以下任一方式让我能找到它：\n'
        f'  1. 打开 SMBX{" Editor" if kind == "editor" else ""}（让它跑起来），然后重新执行本命令；\n'
        '     工具会自动从已运行进程读取它的安装路径。\n'
        f'  2. 或者直接传入路径，例如：--{ "editor" if kind == "editor" else "smbx" } "C:/SMBX38A/{ "editor.exe" if kind == "editor" else "smbx.exe" }"\n'
        '\n'
        '我会自动把路径缓存起来（保存在 '
        f'{CACHE_EDITOR if kind == "editor" else CACHE_SMBX}），下次无需重复指定。\n'
        + '=' * 60 + '\n')
    raise SystemExit(2)


# ---- 会话生命周期 ----
def _save_session(info: dict) -> None:
    with open(SESSION_FILE, 'w', encoding='utf-8') as fh:
        json.dump(info, fh, ensure_ascii=False, indent=2)


def _load_session() -> Optional[dict]:
    if not os.path.isfile(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return None


def _clear_session() -> None:
    try:
        os.remove(SESSION_FILE)
    except OSError:
        pass


def kill_smbx_all() -> int:
    """taskkill 所有 smbx 系进程；返回杀掉的数量（粗估）。"""
    if not IS_WIN:
        return 0
    cnt = 0
    for image in ('smbx.exe', 'smbx-editor.exe', 'smbx_editor.exe',
                  'smbx38a.exe', 'editor.exe'):
        try:
            r = subprocess.run(['taskkill', '/IM', image, '/F'],
                               capture_output=True, text=True, timeout=3)
            if r.returncode == 0:
                cnt += 1
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    return cnt


def launch_smbx_testing(smbx: str, lvl: str, mode: int, p1: int, p2: int,
                        args_str: Optional[str], cwd: Optional[str] = None
                        ) -> subprocess.Popen:
    cmd = [smbx, lvl, str(mode), str(p1), str(p2)]
    if args_str:
        cmd.append(url_encode(args_str))
    return subprocess.Popen(cmd, cwd=cwd or os.path.dirname(smbx))


def launch_editor(editor: str, lvl: Optional[str] = None,
                  cwd: Optional[str] = None) -> subprocess.Popen:
    cmd = [editor]
    if lvl:
        cmd.append(lvl)
    return subprocess.Popen(cmd, cwd=cwd or os.path.dirname(editor))


def wait_for_ipc(timeout: float = 15.0, poll: float = 0.4) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with SMBXIPC() as ipc:
                msgs = ipc.send_recv('GGI|ON', timeout=0.5, expect_prefix='GGI|ON')
                if msgs:
                    return True
        except IPCError:
            pass
        time.sleep(poll)
    return False


# ---- 子命令 ----
def cmd_locate(args):
    cands = find_candidates('smbx')
    if not cands:
        print('[session] no smbx.exe candidates found.')
        print('Hint: 启动 SMBX 一次或用 --smbx <path> 提供路径。')
        return 1
    for p in cands:
        print(p)
    cache_path(cands[0], kind='smbx')
    return 0


def cmd_locate_editor(args):
    cands = find_candidates('editor')
    if not cands:
        print('[session] no SMBX editor candidates found.')
        print('Hint: 启动一次 SMBX editor 或用 --editor <path> 提供路径。')
        return 1
    for p in cands:
        print(p)
    cache_path(cands[0], kind='editor')
    return 0


def cmd_list_procs(args):
    rows = list_running()
    if not rows:
        print('[session] 当前无 SMBX/Editor 进程。')
        return 1
    for r in rows:
        print(f'  pid={r["pid"]:<6} name={r["name"]:<20} path={r["path"]}')
        if r.get('cmdline'):
            print(f'    cmdline={r["cmdline"]}')
    return 0


def cmd_open_editor(args):
    editor = resolve_path(args.editor, kind='editor')
    proc = launch_editor(editor, lvl=args.lvl)
    print(f'[session] editor launched: pid={proc.pid}, exe={editor}')
    if args.lvl:
        print(f'[session] opened level: {args.lvl}')
    return 0


def _ask_continue(prompt: str, no_pause: bool = False) -> None:
    if no_pause:
        return
    sys.stderr.write('\n' + prompt + '\n按回车继续... ')
    sys.stderr.flush()
    try:
        input('')
    except (EOFError, KeyboardInterrupt):
        pass


def cmd_run(args):
    """一键测试会话。"""
    smbx = resolve_path(args.smbx, kind='smbx')
    if not os.path.isfile(args.lvl):
        raise SystemExit(f'lvl 不存在：{args.lvl}')

    # 1) 关掉旧的（避免端口/共享内存冲突）
    if not args.keep_existing:
        kill_smbx_all()
        time.sleep(0.4)

    # 2) 启动测试
    print(f'[session] launching: {smbx} {args.lvl} mode={args.mode}')
    proc = launch_smbx_testing(smbx, args.lvl, args.mode, args.p1, args.p2, args.args)
    _save_session({
        'pid': proc.pid,
        'smbx': smbx,
        'lvl': os.path.abspath(args.lvl),
        'started_at': time.time(),
    })

    # 3) 等 IPC
    print('[session] waiting for IPC ...')
    if not wait_for_ipc(timeout=args.ipc_timeout):
        sys.stderr.write(f'[session] IPC 在 {args.ipc_timeout}s 内未上线。请检查 smbx.exe 是否真在 testing 模式启动。\n')
        return 1
    print('[session] IPC online.')

    # 4) （可选）触发事件
    if args.trigger:
        with SMBXIPC() as ipc:
            for ev in args.trigger:
                ipc.send_command('SET|' + url_encode(ev), timeout=0.6)
                print(f'[session] triggered event: {ev}')

    # 5) （可选）抓状态
    if args.state:
        with SMBXIPC() as ipc:
            for q, prefix in [('GGI|ON', 'GGI|ON'), ('GGI|LN', 'GGI|LN'),
                              ('GGI|VP', 'GGI|VP')]:
                msgs = ipc.send_recv(q, timeout=0.6, expect_prefix=prefix)
                for m in msgs:
                    print(f'[state] {m}')

    # 6) 截图
    if args.screenshot:
        print(f'[session] screenshot -> {args.screenshot}')
        rc = subprocess.call(
            [sys.executable, os.path.join(HERE, 'screenshot.py'),
             '--window', args.screenshot_window, '--first',
             '-o', args.screenshot])
        if rc != 0:
            sys.stderr.write(f'[session] screenshot 失败 rc={rc}\n')

    # 7) 让用户 review
    if not args.no_review:
        _ask_continue(
            f'[session] 测试关卡 {os.path.basename(args.lvl)} 已启动。\n'
            f'         请在 SMBX 窗口里检查行为是否符合预期。\n'
            f'         {"已抓截图：" + args.screenshot if args.screenshot else ""}\n'
            f'         此进程 pid={proc.pid}。\n')

    # 8) 收尾
    if args.auto_stop:
        kill_smbx_all()
        _clear_session()
        print('[session] stopped.')
    else:
        print(f'[session] 仍在运行：pid={proc.pid}。'
              ' 用 `python session.py stop` 关闭。')
    return 0


def cmd_stop(args):
    info = _load_session()
    if info:
        print(f'[session] stopping session pid={info.get("pid")} '
              f'lvl={info.get("lvl")}')
    n = kill_smbx_all()
    _clear_session()
    print(f'[session] killed {n} image(s); session cleared.')
    return 0


def cmd_status(args):
    info = _load_session()
    if not info:
        print('[session] no active session recorded.')
    else:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    rows = list_running()
    print(f'[session] running smbx-family processes: {len(rows)}')
    for r in rows:
        print(f'  pid={r["pid"]} name={r["name"]} path={r["path"]}')
    return 0


def main():
    ap = argparse.ArgumentParser(description='SMBX session & editor manager.')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('locate', help='定位 smbx.exe')
    p.set_defaults(func=cmd_locate)

    p = sub.add_parser('locate-editor', help='定位 SMBX Editor 可执行')
    p.set_defaults(func=cmd_locate_editor)

    p = sub.add_parser('list-procs', help='列出运行中的 SMBX 系进程')
    p.set_defaults(func=cmd_list_procs)

    p = sub.add_parser('open-editor', help='启动 SMBX Editor')
    p.add_argument('--editor', help='editor 可执行路径（会自动定位）')
    p.add_argument('--lvl', help='打开时同时加载此 lvl')
    p.set_defaults(func=cmd_open_editor)

    p = sub.add_parser('run', help='一键测试会话：launch -> wait -> trigger -> screenshot -> review -> stop')
    p.add_argument('--smbx', help='smbx.exe 路径（自动定位）')
    p.add_argument('--lvl', required=True)
    p.add_argument('--mode', type=int, default=0, help='0=单 1=双 2=对战')
    p.add_argument('--p1', type=int, default=0)
    p.add_argument('--p2', type=int, default=1)
    p.add_argument('--args', help='SMBXArgs|... 可选额外参数（未编码）')
    p.add_argument('--ipc-timeout', type=float, default=15.0)
    p.add_argument('--trigger', action='append', default=[],
                   help='测试期间触发的事件名（可多次）')
    p.add_argument('--state', action='store_true',
                   help='抓 GGI|ON / GGI|LN / GGI|VP 状态')
    p.add_argument('--screenshot', help='截图输出路径（默认不截）')
    p.add_argument('--screenshot-window', default='smbx',
                   help='截图窗口标题子串，默认 smbx')
    p.add_argument('--no-review', action='store_true',
                   help='跳过"等用户回车 review"环节')
    p.add_argument('--auto-stop', action='store_true',
                   help='review 后自动 kill；默认保留进程让用户继续玩')
    p.add_argument('--keep-existing', action='store_true',
                   help='不杀已存在的 smbx 进程')
    p.set_defaults(func=cmd_run)

    p = sub.add_parser('stop', help='停止由本工具启动的会话')
    p.set_defaults(func=cmd_stop)

    p = sub.add_parser('status', help='当前会话状态')
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
