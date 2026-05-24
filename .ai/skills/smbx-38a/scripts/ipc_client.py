#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ipc_client.py — Windows 共享内存 IPC 客户端，对接 SMBX 38A 的 `smbx_memory_block`。

权威协议见 `reference/ipc-protocol.md`（精炼）与
`.docs/.smbx38a-docs/Engine IPC Interface/Cpp-Example/command.txt`（原文）。

约定：
- 仅在 Windows 平台可用。
- 依赖 SMBX 已通过 `smbx.exe <lvl> <mode> <p1> <p2> <args>` 命令行进入 testing 模式。
- 共享内存名固定 `smbx_memory_block`，总大小 16384 字节：
    BufferA[8192] : 引擎 -> 客户端，本端只读；读取后必须把 Length 清零
    BufferB[8192] : 客户端 -> 引擎，本端只写；引擎收到后清零
  每个 buffer 头 2 字节 = short Length，后 8190 字节 = ASCII data，多命令以 '\n' 分隔。

CLI:
    python ipc_client.py ping
    python ipc_client.py send "GGI|ON"
    python ipc_client.py recv --timeout 1.0
    python ipc_client.py send-recv "GGI|ON" --timeout 0.5
    python ipc_client.py raw       # 进入交互式 REPL（Ctrl+C 退出）
"""
from __future__ import annotations

import argparse
import struct
import sys
import time
from typing import List, Optional

IS_WIN = sys.platform.startswith('win')

BUFFER_SIZE = 8192
SAFE_DATA_SIZE = 8000  # 同 spec 示例
HEADER_LEN = 2         # short
MEM_NAME = 'smbx_memory_block'


class IPCError(RuntimeError):
    pass


class SMBXIPC:
    """对接 smbx_memory_block 的共享内存客户端。

    设计：
    - 每次 read/write 用 `ctypes` 直接操作 mmap 字节。
    - 不开后台线程；调用方通过 poll / send_recv 推动。
    - send_command 会等到 BufferB.Length 变为 0（说明引擎处理完上一条）再写下一批；
      若超过 timeout 仍未空，则抛 IPCError。
    """

    def __init__(self):
        if not IS_WIN:
            raise IPCError('IPC 仅在 Windows 上可用')
        import ctypes
        from ctypes import wintypes
        self._ctypes = ctypes
        self._wintypes = wintypes

        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        OpenFileMappingW = kernel32.OpenFileMappingW
        OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
        OpenFileMappingW.restype = wintypes.HANDLE

        MapViewOfFile = kernel32.MapViewOfFile
        MapViewOfFile.argtypes = [wintypes.HANDLE, wintypes.DWORD,
                                  wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]
        MapViewOfFile.restype = ctypes.c_void_p

        UnmapViewOfFile = kernel32.UnmapViewOfFile
        UnmapViewOfFile.argtypes = [ctypes.c_void_p]
        UnmapViewOfFile.restype = wintypes.BOOL

        CloseHandle = kernel32.CloseHandle
        CloseHandle.argtypes = [wintypes.HANDLE]
        CloseHandle.restype = wintypes.BOOL

        FILE_MAP_ALL_ACCESS = 0x0002 | 0x0004
        h = OpenFileMappingW(FILE_MAP_ALL_ACCESS, False, MEM_NAME)
        if not h:
            err = ctypes.get_last_error()
            raise IPCError(
                f'OpenFileMapping("{MEM_NAME}") failed (winerror={err}). '
                'SMBX 必须已通过测试模式启动；请先 launch 关卡再连。')
        self._h = h
        ptr = MapViewOfFile(h, FILE_MAP_ALL_ACCESS, 0, 0, BUFFER_SIZE * 2)
        if not ptr:
            err = ctypes.get_last_error()
            CloseHandle(h)
            raise IPCError(f'MapViewOfFile failed (winerror={err})')
        self._ptr = ptr
        self._UnmapViewOfFile = UnmapViewOfFile
        self._CloseHandle = CloseHandle

    def close(self):
        if getattr(self, '_ptr', None):
            self._UnmapViewOfFile(self._ptr); self._ptr = None
        if getattr(self, '_h', None):
            self._CloseHandle(self._h); self._h = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    # ---- 低层 ----
    def _read_buf(self, base_off: int, n: int) -> bytes:
        ctypes = self._ctypes
        addr = self._ptr + base_off
        return bytes((ctypes.c_ubyte * n).from_address(addr))

    def _write_buf(self, base_off: int, data: bytes) -> None:
        ctypes = self._ctypes
        addr = self._ptr + base_off
        arr = (ctypes.c_ubyte * len(data)).from_address(addr)
        for i, b in enumerate(data):
            arr[i] = b

    def _read_length(self, base_off: int) -> int:
        return struct.unpack_from('<h', self._read_buf(base_off, HEADER_LEN))[0]

    def _write_length(self, base_off: int, n: int) -> None:
        self._write_buf(base_off, struct.pack('<h', n))

    # ---- 高层 ----
    def poll_messages(self) -> List[str]:
        """读取 BufferA 中的全部消息（按 '\n' 切分），并清零 Length。"""
        n = self._read_length(0)
        if n <= 0 or n > SAFE_DATA_SIZE:
            return []
        data = bytes(self._read_buf(HEADER_LEN, n))
        # 清零（仅 Length 即可；引擎下次写会覆盖 data）
        self._write_length(0, 0)
        try:
            text = data.decode('ascii', errors='replace')
        except Exception:
            text = data.decode('latin-1', errors='replace')
        return [line for line in text.split('\n') if line != '']

    def _wait_send_buffer_empty(self, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._read_length(BUFFER_SIZE) == 0:
                return True
            time.sleep(0.01)
        return self._read_length(BUFFER_SIZE) == 0

    def send_command(self, command: str, timeout: float = 1.0) -> None:
        """发送一条或多条命令（多条用 '\n'）。等待引擎清空发送缓冲。"""
        if '\r' in command:
            command = command.replace('\r', '')
        data = command.encode('ascii', errors='replace')
        if len(data) >= SAFE_DATA_SIZE:
            raise IPCError(f'command too long: {len(data)} >= {SAFE_DATA_SIZE}')
        if not self._wait_send_buffer_empty(timeout):
            raise IPCError('engine has not consumed previous command (timeout)')
        # 写 data 再写 length（先写数据，再 publish length，模拟原子）
        self._write_buf(BUFFER_SIZE + HEADER_LEN, data)
        self._write_length(BUFFER_SIZE, len(data))

    def send_recv(self, command: str, timeout: float = 1.0,
                  expect_prefix: Optional[str] = None) -> List[str]:
        """发送命令并等待回应。
        - 若 expect_prefix 给出，则只返回从该前缀开始的若干消息。
        - 否则只要 timeout 内拿到任何 messages 就返回。
        """
        # 清掉残留
        self.poll_messages()
        self.send_command(command, timeout=timeout)
        deadline = time.monotonic() + timeout
        out: List[str] = []
        while time.monotonic() < deadline:
            msgs = self.poll_messages()
            if msgs:
                out.extend(msgs)
                if expect_prefix is None:
                    return out
                if any(m.startswith(expect_prefix) for m in out):
                    return out
            time.sleep(0.01)
        return out


# ---- CLI ----
def cmd_ping(args):
    try:
        with SMBXIPC() as ipc:
            r = ipc.send_recv('GGI|ON', timeout=args.timeout, expect_prefix='GGI|ON')
            if not r:
                print('[ipc] PING TIMEOUT (no response)'); return 1
            print(f'[ipc] OK, recv {len(r)} message(s):')
            for m in r:
                print('  ' + m)
            return 0
    except IPCError as e:
        print(f'[ipc] {e}', file=sys.stderr); return 2


def cmd_send(args):
    with SMBXIPC() as ipc:
        ipc.send_command(args.command, timeout=args.timeout)
        print(f'[ipc] sent: {args.command!r}')
        return 0


def cmd_recv(args):
    with SMBXIPC() as ipc:
        deadline = time.monotonic() + args.timeout
        out = []
        while time.monotonic() < deadline:
            msgs = ipc.poll_messages()
            if msgs:
                out.extend(msgs)
                if not args.drain:
                    break
            time.sleep(0.02)
        if not out:
            print('[ipc] (no messages)'); return 1
        for m in out:
            print(m)
        return 0


def cmd_send_recv(args):
    with SMBXIPC() as ipc:
        msgs = ipc.send_recv(args.command, timeout=args.timeout,
                             expect_prefix=args.expect)
        if not msgs:
            print('[ipc] (timeout or empty)'); return 1
        for m in msgs:
            print(m)
        return 0


def cmd_repl(args):
    with SMBXIPC() as ipc:
        print('[ipc] interactive mode. Type a command (e.g. GGI|ON), or `quit`.')
        try:
            while True:
                line = input('> ').strip()
                if not line or line.lower() == 'quit':
                    break
                msgs = ipc.send_recv(line, timeout=args.timeout)
                for m in msgs:
                    print('< ' + m)
        except (EOFError, KeyboardInterrupt):
            print()
    return 0


def main():
    ap = argparse.ArgumentParser(description='SMBX 38A shared-memory IPC client (Windows only).')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('ping', help='发送 GGI|ON 探活')
    p.add_argument('--timeout', type=float, default=1.0)
    p.set_defaults(func=cmd_ping)

    p = sub.add_parser('send', help='发送一条原始命令')
    p.add_argument('command')
    p.add_argument('--timeout', type=float, default=1.0)
    p.set_defaults(func=cmd_send)

    p = sub.add_parser('recv', help='收取当前缓冲（默认收完一批）')
    p.add_argument('--timeout', type=float, default=0.5)
    p.add_argument('--drain', action='store_true', help='直到 timeout 才返回')
    p.set_defaults(func=cmd_recv)

    p = sub.add_parser('send-recv', help='发命令并等响应')
    p.add_argument('command')
    p.add_argument('--timeout', type=float, default=1.0)
    p.add_argument('--expect', default=None, help='等待匹配前缀的消息')
    p.set_defaults(func=cmd_send_recv)

    p = sub.add_parser('raw', help='交互式 REPL')
    p.add_argument('--timeout', type=float, default=0.6)
    p.set_defaults(func=cmd_repl)

    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
