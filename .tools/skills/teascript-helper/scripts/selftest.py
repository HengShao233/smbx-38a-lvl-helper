#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py — teascript-helper 离线自检：
- lint 干净模板（0 err / 0 warn）
- lint 故意错误样本（应捕获错误）
- inject + event 后 round-trip 校验

不会启动 smbx.exe；运行时 IPC/截图阶段不在此测试范围。
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
SMBX38A_SCRIPTS = os.path.abspath(os.path.join(HERE, '..', '..', 'smbx-38a', 'scripts'))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))


def run(cmd, **kwargs):
    # Force UTF-8 decoding so non-ASCII (中文、emoji) in tool output don't
    # crash the GBK default codec on zh-CN Windows.
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('errors', 'replace')
    env = kwargs.pop('env', None) or os.environ.copy()
    env.setdefault('PYTHONIOENCODING', 'utf-8')
    return subprocess.run(cmd, capture_output=True, text=True, env=env, **kwargs)


def test_lint_clean():
    rc = []
    for tea in ['event_script.tea', 'function.tea', 'procedure.tea',
                'iterator_loop.tea', 'global_script.tea']:
        p = os.path.join(SKILL_ROOT, 'templates', tea)
        r = run([sys.executable, os.path.join(HERE, 'teascript_lint.py'), p])
        if r.returncode != 0:
            print(f'  FAIL: lint clean failed on {tea}: rc={r.returncode}')
            print(r.stdout[-400:])
            return False
        rc.append(tea)
    print(f'  OK   lint clean on {len(rc)} templates')
    return True


def test_lint_dirty():
    bad = """// wrong comment
dim 1bad as integer = 0
do
    x = x + 1
loop
"""
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'bad.tea')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(bad)
        r = run([sys.executable, os.path.join(HERE, 'teascript_lint.py'), p])
        if r.returncode == 0:
            print('  FAIL: dirty sample passed lint, expected non-zero')
            return False
        for code in ('E001', 'E008', 'W101'):
            if code not in r.stdout:
                print(f'  FAIL: missing rule {code} in lint output')
                print(r.stdout)
                return False
    print('  OK   lint dirty captures E001/E008/W101')
    return True


def test_inject_event_round_trip():
    # 找一个小的 lvl
    sample = None
    scenes = os.path.join(PROJECT_ROOT, 'Scenes')
    for root, _, files in os.walk(scenes):
        for f in files:
            if f.lower().endswith('.lvl'):
                sample = os.path.join(root, f); break
        if sample:
            break
    if not sample:
        print('  (跳过) 找不到 lvl 样本')
        return True

    tea = os.path.join(SKILL_ROOT, 'templates', 'event_script.tea')
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, 'out.lvl')
        shutil.copyfile(sample, out)
        # inject
        r = run([sys.executable, os.path.join(HERE, 'teascript_inject.py'),
                 out, '--tea', tea, '--name', 'TestX', '-o', out])
        if r.returncode != 0:
            print('  FAIL: inject\n' + r.stderr); return False
        # bind event
        r = run([sys.executable, os.path.join(HERE, 'teascript_event.py'),
                 out, '--event', 'TestEvtX', '--script', 'TestX',
                 '--autostart', '1', '-o', out, '--require-script'])
        if r.returncode != 0:
            print('  FAIL: bind event\n' + r.stderr); return False
        # round-trip 校验：再 load 一遍
        sys.path.insert(0, SMBX38A_SCRIPTS)
        try:
            from lvlfile import SMBXFile, url_decode
        finally:
            try:
                sys.path.remove(SMBX38A_SCRIPTS)
            except ValueError:
                pass
        f = SMBXFile.load(out)
        names = [url_decode(e.get(0, '')) for e in f.entries if e.marker == 'E']
        scripts = [url_decode(e.get(0, '')) for e in f.entries if e.marker in ('S', 'Su')]
        if 'TestEvtX' not in names:
            print(f'  FAIL: event not present, got {names}'); return False
        if 'TestX' not in scripts:
            print(f'  FAIL: script not present, got {scripts}'); return False
    print('  OK   inject + bind + reload all in 1 lvl')
    return True


def test_format():
    src = "dim x as integer\t=\t1\n  \n\n"
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 't.tea')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(src)
        r = run([sys.executable, os.path.join(HERE, 'teascript_format.py'),
                 p, '--inplace'])
        if r.returncode != 0:
            print('  FAIL: format'); return False
        with open(p, 'r', encoding='utf-8') as fh:
            text = fh.read()
        if '\t' in text:
            print('  FAIL: tab not expanded'); return False
        if not text.endswith('\n'):
            print('  FAIL: missing trailing newline'); return False
    print('  OK   format expands tabs and trims')
    return True


def main():
    print('=' * 60)
    tests = [
        ('lint clean',   test_lint_clean),
        ('lint dirty',   test_lint_dirty),
        ('inject+event', test_inject_event_round_trip),
        ('format',       test_format),
    ]
    failed = 0
    for name, fn in tests:
        print(f'[ {name} ]')
        try:
            ok = fn()
        except Exception as e:
            print(f'  CRASH: {e}'); ok = False
        if not ok:
            failed += 1
    print('=' * 60)
    if failed:
        print(f'FAILED: {failed} test(s)')
        return 1
    print('All tests passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
