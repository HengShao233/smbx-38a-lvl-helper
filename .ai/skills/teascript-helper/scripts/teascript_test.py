#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teascript_test.py — TeaScript 一键回归测试。

把 lint -> inject -> bind event -> launch testing -> trigger -> screenshot -> review -> stop
串成一个原子流水线。失败任意阶段都会立刻终止，并给出明确指引。

用法（最小）：
    python teascript_test.py \
        --lvl path/to/level.lvl \
        --tea path/to/my.tea \
        --name MyScript \
        --event OnFoo

完整：
    python teascript_test.py \
        --lvl Scenes/Entries/TP.lvl \
        --tea path/to/my.tea \
        --name MyScript \
        --event OnFoo \
        --autostart 1 \
        --output .cache/TP.test.lvl \
        --smbx "C:/SMBX38A/smbx.exe" \
        --screenshot .cache/snap.png \
        --no-review

不需要 review 时加 --no-review；不希望自动 stop 时省略 --auto-stop。
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
SMBX38A_SCRIPTS = os.path.abspath(os.path.join(HERE, '..', '..', 'smbx-38a', 'scripts'))


def step(name: str):
    print('\n' + '-' * 60)
    print(f'>> {name}')
    print('-' * 60)


def run(cmd, **kwargs):
    """运行子命令，错误时抛出。"""
    print('  $ ' + ' '.join(_quote(x) for x in cmd))
    rc = subprocess.call(cmd, **kwargs)
    if rc != 0:
        raise SystemExit(f'  [FAIL] 命令失败（rc={rc}）。已终止流水线。')


def _quote(s: str) -> str:
    if ' ' in s or '"' in s:
        return '"' + s.replace('"', '\\"') + '"'
    return s


def main():
    # Windows 控制台默认 GBK，stdout 强制 UTF-8 以兼容输出
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    ap = argparse.ArgumentParser(description='One-shot regression for a TeaScript change.')
    ap.add_argument('--lvl', required=True, help='原始 lvl 路径')
    ap.add_argument('--tea', required=True, help='.tea 脚本路径')
    ap.add_argument('--name', required=True, help='脚本名（变量命名规范）')
    ap.add_argument('--event', help='事件名（不给则不绑定，仅嵌入脚本）')
    ap.add_argument('--autostart', type=int, choices=[0, 1, 2, 3], default=0)
    ap.add_argument('--output', help='输出 lvl 路径；默认 .cache/<lvl>.test.lvl')
    ap.add_argument('--ascii', action='store_true', help='用 Su（ASCII）嵌入')

    # lint 控制
    ap.add_argument('--no-lint', action='store_true')
    ap.add_argument('--lint-allow-warnings', action='store_true',
                    help='lint warning 不视为失败（默认 warning 不阻塞）')
    ap.add_argument('--lint-disable', action='append', default=[],
                    help='禁用 lint 规则码，可多次')

    # 引擎控制
    ap.add_argument('--smbx', help='smbx.exe 路径（自动定位）')
    ap.add_argument('--no-launch', action='store_true', help='只到 inject 为止，不启动引擎')
    ap.add_argument('--screenshot', help='截图输出路径')
    ap.add_argument('--screenshot-window', default='smbx')
    ap.add_argument('--no-review', action='store_true', help='不等用户回车 review')
    ap.add_argument('--auto-stop', action='store_true', help='review 后自动 kill smbx')
    ap.add_argument('--ipc-timeout', type=float, default=15.0)

    args = ap.parse_args()

    # ---- 路径准备 ----
    if not os.path.isfile(args.lvl):
        raise SystemExit(f'lvl 不存在：{args.lvl}')
    if not os.path.isfile(args.tea):
        raise SystemExit(f'.tea 不存在：{args.tea}')

    if args.output:
        out_lvl = args.output
    else:
        cache_dir = os.path.join(_project_root(), '.cache')
        os.makedirs(cache_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(args.lvl))[0]
        out_lvl = os.path.join(cache_dir, base + '.test.lvl')

    # ---- 1) lint ----
    if not args.no_lint:
        step('1) lint')
        cmd = [sys.executable, os.path.join(HERE, 'teascript_lint.py'), args.tea]
        for d in args.lint_disable:
            cmd += ['--disable', d]
        if args.lint_allow_warnings:
            cmd.append('--no-warnings')
        rc = subprocess.call(cmd)
        if rc != 0:
            raise SystemExit('  [FAIL] lint 不通过。请先修复错误，或用 --no-lint 跳过。')
    else:
        step('1) lint  (skipped)')

    # ---- 2) 拷贝 lvl 到目标，避免污染原文件 ----
    step('2) prepare working lvl')
    shutil.copyfile(args.lvl, out_lvl)
    print(f'  copied: {args.lvl}\n      to: {out_lvl}')

    # ---- 3) inject ----
    step('3) inject script')
    inj = [sys.executable, os.path.join(HERE, 'teascript_inject.py'),
           out_lvl, '--tea', args.tea, '--name', args.name, '-o', out_lvl]
    if args.ascii:
        inj.append('--ascii')
    run(inj)

    # ---- 4) bind event ----
    if args.event:
        step('4) bind event -> script')
        run([sys.executable, os.path.join(HERE, 'teascript_event.py'),
             out_lvl, '--event', args.event, '--script', args.name,
             '--autostart', str(args.autostart), '-o', out_lvl,
             '--require-script'])
    else:
        step('4) bind event  (skipped: --event not provided)')

    # ---- 5) round-trip 校验（用 lvl_parse.py --summary，确保未破坏文件）----
    step('5) round-trip verify')
    rc = subprocess.call([sys.executable,
                          os.path.join(SMBX38A_SCRIPTS, 'lvl_parse.py'),
                          out_lvl, '--summary'])
    if rc != 0:
        raise SystemExit('  [FAIL] round-trip 失败。新 lvl 文件结构异常，已停止流水线。')

    if args.no_launch:
        print('\n[OK] 静态阶段完成。lvl 已保存到：')
        print(f'   {out_lvl}')
        print('因 --no-launch，未启动引擎。')
        return 0

    # ---- 6) launch + trigger + screenshot + review ----
    step('6) launch SMBX testing & verify')
    sess = [sys.executable, os.path.join(SMBX38A_SCRIPTS, 'session.py'), 'run',
            '--lvl', out_lvl,
            '--ipc-timeout', str(args.ipc_timeout)]
    if args.smbx:
        sess += ['--smbx', args.smbx]
    if args.event:
        sess += ['--trigger', args.event]
    sess += ['--state']
    if args.screenshot:
        sess += ['--screenshot', args.screenshot,
                 '--screenshot-window', args.screenshot_window]
    if args.no_review:
        sess.append('--no-review')
    if args.auto_stop:
        sess.append('--auto-stop')

    rc = subprocess.call(sess)
    if rc != 0:
        raise SystemExit(f'  [FAIL] session.run 失败 rc={rc}')

    print('\n[OK] 全流程完成。新 lvl 在：')
    print(f'   {out_lvl}')
    if args.screenshot:
        print(f'   screenshot: {args.screenshot}')
    return 0


def _project_root() -> str:
    return os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))


if __name__ == '__main__':
    sys.exit(main())
