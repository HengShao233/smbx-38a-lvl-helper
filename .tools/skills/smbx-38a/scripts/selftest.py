#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py — skill 的离线能力自检：
- 解析项目内若干 .lvl
- round-trip 字节相等
- 一次空操作 edit + parse 校验
- 截图（仅 Windows）

不会启动 smbx.exe；运行时 IPC 部分不会被测试（因为需要引擎在跑）。
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lvlfile import SMBXFile, assert_round_trip


PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))


def find_sample_lvls(limit=8):
    """从 Scenes/ 挑若干小文件做 round-trip 测。"""
    candidates = []
    scenes = os.path.join(PROJECT_ROOT, 'Scenes')
    if not os.path.isdir(scenes):
        return candidates
    for root, _, files in os.walk(scenes):
        for f in files:
            if f.lower().endswith('.lvl'):
                p = os.path.join(root, f)
                try:
                    sz = os.path.getsize(p)
                except OSError:
                    continue
                candidates.append((sz, p))
    candidates.sort()
    return [p for _, p in candidates[:limit]]


def test_round_trip():
    lvls = find_sample_lvls(8)
    if not lvls:
        print('  (跳过) 没找到任何 .lvl 样本')
        return True
    for p in lvls:
        rel = os.path.relpath(p, PROJECT_ROOT)
        try:
            assert_round_trip(p)
            print(f'  OK   {rel}  ({os.path.getsize(p)} bytes)')
        except Exception as e:
            print(f'  FAIL {rel}: {e}')
            return False
    return True


def test_summary():
    lvls = find_sample_lvls(2)
    for p in lvls:
        f = SMBXFile.load(p)
        s = f.summary()
        rel = os.path.relpath(p, PROJECT_ROOT)
        print(f'  {rel} -> markers={len(s["marker_count"])} '
              f'npc={s["total_npc"]} blk={s["total_block"]} evt={s["total_event"]}')
    return True


def test_edit_round_trip():
    lvls = find_sample_lvls(1)
    if not lvls:
        print('  (跳过)')
        return True
    p = lvls[0]
    f = SMBXFile.load(p)
    n_blk_before = sum(1 for e in f.entries if e.marker == 'B')
    # 添加再删除
    from lvlfile import Entry
    f.add(Entry(marker='B', fields=['Default', '99999', '12345', '-12345', '', '0', '0', '', '32', '32']))
    f.remove(marker='B', predicate=lambda e: e.get(1) == '99999')
    n_blk_after = sum(1 for e in f.entries if e.marker == 'B')
    if n_blk_before != n_blk_after:
        print(f'  FAIL: block count changed {n_blk_before} -> {n_blk_after}')
        return False
    # round-trip 一次
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, 'out.lvl')
        f.save(out)
        f2 = SMBXFile.load(out)
        if sum(1 for e in f2.entries if e.marker == 'B') != n_blk_after:
            print('  FAIL: parse-after-save mismatch')
            return False
    print(f'  OK   add+remove cycle on {os.path.relpath(p, PROJECT_ROOT)}')
    return True


def test_screenshot():
    if not sys.platform.startswith('win'):
        print('  (跳过) 非 Windows')
        return True
    try:
        from screenshot import _capture, _save_png, get_screen_size
    except Exception as e:
        print(f'  FAIL: import error: {e}')
        return False
    w, h = get_screen_size()
    data = _capture(0, 0, 0, 64, 32)  # 不截整屏，省时
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, 'snap.png')
        _save_png(out, 64, 32, data)
        if not os.path.isfile(out) or os.path.getsize(out) < 50:
            print('  FAIL: png file invalid')
            return False
    print(f'  OK   captured 64x32 from screen ({w}x{h})')
    return True


def main():
    print(f'project root = {PROJECT_ROOT}')
    print('=' * 60)
    tests = [
        ('round-trip on real .lvl files', test_round_trip),
        ('summary',                       test_summary),
        ('edit+remove cycle',             test_edit_round_trip),
        ('screenshot (Win only)',         test_screenshot),
    ]
    failed = 0
    for name, fn in tests:
        print(f'[ {name} ]')
        try:
            ok = fn()
        except Exception as e:
            print(f'  CRASH: {e}')
            ok = False
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
