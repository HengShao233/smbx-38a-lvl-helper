#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
screenshot.py — Windows 下截取 SMBX 窗口（或全屏 / 任意窗口标题匹配）。

零第三方依赖：直接用 ctypes 调 user32/gdi32，再用 stdlib 的 zlib 编码 PNG。

用法：
    # 截图任意标题匹配 'smbx' 的窗口（不区分大小写，支持子串）
    python screenshot.py --window smbx -o snap.png

    # 截图主显示器全屏
    python screenshot.py --screen -o snap.png

    # 列出所有可见顶层窗口的标题（用于挑选）
    python screenshot.py --list-windows
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
import zlib
from typing import List, Optional, Tuple

if not sys.platform.startswith('win'):
    print('screenshot.py 仅支持 Windows', file=sys.stderr)


def _save_png(path: str, width: int, height: int, bgr_bottom_up: bytes) -> None:
    """从 GetDIBits 拿到的 32 位 BGRA 自下而上数据写为 PNG。
    使用切片批处理（无逐像素循环），快很多。"""
    stride = width * 4
    src = memoryview(bgr_bottom_up)
    # 一次性 BGRA -> RGBA：交换 B/R 通道；alpha 强制 255
    flat = bytearray(src)  # 一次大拷贝
    flat[0::4], flat[2::4] = flat[2::4], flat[0::4]
    flat[3::4] = b'\xff' * (width * height)
    # 翻转行（bottom-up -> top-down）并加 PNG filter byte
    rows = bytearray(height * (stride + 1))
    for y in range(height):
        src_off = (height - 1 - y) * stride
        dst_off = y * (stride + 1)
        rows[dst_off] = 0  # filter
        rows[dst_off + 1:dst_off + 1 + stride] = flat[src_off:src_off + stride]
    compressed = zlib.compress(bytes(rows), 6)

    def chunk(typ: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(typ + data) & 0xffffffff
        return struct.pack('>I', len(data)) + typ + data + struct.pack('>I', crc)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    png = sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    with open(path, 'wb') as fh:
        fh.write(png)


def _capture(hwnd: int, dx: int, dy: int, w: int, h: int) -> bytes:
    """从给定窗口（hwnd=0 表示桌面）+ (dx,dy) 起截 w*h 区域，返回 BGRA bottom-up bytes。"""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

    GetDC = user32.GetDC
    GetDC.argtypes = [wintypes.HWND]; GetDC.restype = ctypes.c_void_p
    ReleaseDC = user32.ReleaseDC
    ReleaseDC.argtypes = [wintypes.HWND, ctypes.c_void_p]; ReleaseDC.restype = ctypes.c_int
    CreateCompatibleDC = gdi32.CreateCompatibleDC
    CreateCompatibleDC.argtypes = [ctypes.c_void_p]; CreateCompatibleDC.restype = ctypes.c_void_p
    CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
    CreateCompatibleBitmap.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    CreateCompatibleBitmap.restype = ctypes.c_void_p
    SelectObject = gdi32.SelectObject
    SelectObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]; SelectObject.restype = ctypes.c_void_p
    BitBlt = gdi32.BitBlt
    BitBlt.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                       ctypes.c_void_p, ctypes.c_int, ctypes.c_int, wintypes.DWORD]
    BitBlt.restype = wintypes.BOOL
    DeleteObject = gdi32.DeleteObject
    DeleteObject.argtypes = [ctypes.c_void_p]; DeleteObject.restype = wintypes.BOOL
    DeleteDC = gdi32.DeleteDC
    DeleteDC.argtypes = [ctypes.c_void_p]; DeleteDC.restype = wintypes.BOOL
    GetDIBits = gdi32.GetDIBits
    GetDIBits.argtypes = [ctypes.c_void_p, ctypes.c_void_p, wintypes.UINT, wintypes.UINT,
                          ctypes.c_void_p, ctypes.c_void_p, wintypes.UINT]
    GetDIBits.restype = ctypes.c_int

    SRCCOPY = 0x00CC0020
    BI_RGB = 0
    DIB_RGB_COLORS = 0

    src_dc = GetDC(hwnd)
    if not src_dc:
        raise RuntimeError('GetDC failed')
    mem_dc = CreateCompatibleDC(src_dc)
    bmp = CreateCompatibleBitmap(src_dc, w, h)
    SelectObject(mem_dc, bmp)
    if not BitBlt(mem_dc, 0, 0, w, h, src_dc, dx, dy, SRCCOPY):
        DeleteObject(bmp); DeleteDC(mem_dc); ReleaseDC(hwnd, src_dc)
        err = ctypes.get_last_error()
        raise RuntimeError(f'BitBlt failed (winerror={err})')

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', wintypes.DWORD), ('biWidth', wintypes.LONG),
            ('biHeight', wintypes.LONG), ('biPlanes', wintypes.WORD),
            ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
            ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', wintypes.LONG),
            ('biYPelsPerMeter', wintypes.LONG), ('biClrUsed', wintypes.DWORD),
            ('biClrImportant', wintypes.DWORD),
        ]

    class BITMAPINFO(ctypes.Structure):
        _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', wintypes.DWORD * 3)]

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = h        # 正：bottom-up
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB
    bmi.bmiHeader.biSizeImage = w * h * 4

    buf = (ctypes.c_ubyte * (w * h * 4))()
    got = GetDIBits(mem_dc, bmp, 0, h, buf, ctypes.byref(bmi), DIB_RGB_COLORS)
    DeleteObject(bmp); DeleteDC(mem_dc); ReleaseDC(hwnd, src_dc)
    if got == 0:
        raise RuntimeError('GetDIBits failed')
    return bytes(buf)


def find_windows_by_title(substr: str) -> List[Tuple[int, str]]:
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    EnumWindows = user32.EnumWindows
    EnumWindows.argtypes = [EnumWindowsProc, wintypes.LPARAM]; EnumWindows.restype = wintypes.BOOL
    GetWindowTextLengthW = user32.GetWindowTextLengthW
    GetWindowTextLengthW.argtypes = [wintypes.HWND]; GetWindowTextLengthW.restype = ctypes.c_int
    GetWindowTextW = user32.GetWindowTextW
    GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    GetWindowTextW.restype = ctypes.c_int
    IsWindowVisible = user32.IsWindowVisible
    IsWindowVisible.argtypes = [wintypes.HWND]; IsWindowVisible.restype = wintypes.BOOL

    results: List[Tuple[int, str]] = []
    needle = substr.lower() if substr else ''

    def _cb(hwnd, lparam):
        if not IsWindowVisible(hwnd):
            return True
        n = GetWindowTextLengthW(hwnd)
        if n <= 0:
            return True
        buf = ctypes.create_unicode_buffer(n + 1)
        GetWindowTextW(hwnd, buf, n + 1)
        title = buf.value
        if needle and needle not in title.lower():
            return True
        results.append((int(hwnd), title))
        return True

    EnumWindows(EnumWindowsProc(_cb), 0)
    return results


def get_window_rect(hwnd: int) -> Tuple[int, int, int, int]:
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetClientRect = user32.GetClientRect
    GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    GetClientRect.restype = wintypes.BOOL
    rect = wintypes.RECT()
    if not GetClientRect(hwnd, ctypes.byref(rect)):
        raise RuntimeError('GetClientRect failed')
    return rect.left, rect.top, rect.right, rect.bottom


def get_screen_size() -> Tuple[int, int]:
    import ctypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def cmd_list(_args):
    for hwnd, title in find_windows_by_title(''):
        print(f'  hwnd={hwnd:>10}  title={title!r}')
    return 0


def cmd_capture(args):
    if args.list_windows:
        return cmd_list(args)

    if args.screen:
        w, h = get_screen_size()
        data = _capture(0, 0, 0, w, h)
        _save_png(args.output, w, h, data)
        print(f'[screenshot] saved screen {w}x{h} -> {args.output}')
        return 0

    if not args.window:
        print('请指定 --window <substr>、--screen 或 --list-windows', file=sys.stderr)
        return 2

    matches = find_windows_by_title(args.window)
    if not matches:
        print(f'[screenshot] 没找到匹配窗口（substr={args.window!r}）', file=sys.stderr)
        return 1
    if len(matches) > 1 and not args.first:
        print('[screenshot] 多个匹配，请缩小 --window 或加 --first：', file=sys.stderr)
        for h, t in matches:
            print(f'  hwnd={h}  title={t!r}', file=sys.stderr)
        return 1
    hwnd, title = matches[0]
    l, t, r, b = get_window_rect(hwnd)
    w, h = r - l, b - t
    if w <= 0 or h <= 0:
        print(f'[screenshot] 窗口尺寸异常 {w}x{h}', file=sys.stderr); return 1
    data = _capture(hwnd, 0, 0, w, h)
    _save_png(args.output, w, h, data)
    print(f'[screenshot] saved {title!r} {w}x{h} -> {args.output}')
    return 0


def main():
    ap = argparse.ArgumentParser(description='Capture SMBX (or any) window to PNG (Windows only).')
    ap.add_argument('--window', help='窗口标题包含的子串（不区分大小写）')
    ap.add_argument('--screen', action='store_true', help='截主屏')
    ap.add_argument('--list-windows', action='store_true', help='列出所有可见顶层窗口')
    ap.add_argument('--first', action='store_true', help='多匹配时取第一个')
    ap.add_argument('-o', '--output', default='screenshot.png')
    args = ap.parse_args()
    return cmd_capture(args)


if __name__ == '__main__':
    sys.exit(main())
