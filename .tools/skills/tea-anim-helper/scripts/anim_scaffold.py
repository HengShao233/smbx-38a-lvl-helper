#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anim_scaffold.py — 从需求模板 DSL 生成 tea-anim-helper 动画骨架 .tea。

生成的骨架已包含：
  - 头部块注释 (含 bmp 分配表)
  - 调参区 / 内部状态 / 临时变量 (统一头部 dim, temp_ 前缀)
  - _Length / _Launch / _Tick / _Finish 四接口 (签名严格符合契约)
  - _Launch 中按 --bmp 自动生成 BmpNew (相对 BmpIdOffset)
  - _Tick / _Finish 中留好 TODO 与循环释放
生成后请在 _Tick 内补全“面向时间的变化”，并跑 anim_lint.py 静态校验。

bmp DSL (可多次 --bmp)：
    <slot>=npc-<srcId>(<x>,<y>,<w>,<h>)[ anim:frames=N,cols=C[,loopFrom=L][,fps=F][,interval=IX:IY] ]
例：
    --bmp "0=npc-1(0,0,128,128)"
    --bmp "1=npc-2(3984,0,8,8) anim:frames=4,cols=2,fps=12"

用法：
    python anim_scaffold.py --name MyAnim --length 60 \
        --bmp "0=npc-1(0,0,128,128)" -o .cache/MyAnim.tea

注：中间产物（骨架/草稿）建议输出到 .cache/ 目录, 由 gitignore 规则 **/.cache/ 排除。
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class BmpSpec:
    slot: int
    src_id: int
    x: int
    y: int
    w: int
    h: int
    anim: Optional[Dict[str, int]] = None   # frames/cols/loopFrom/fps/ix/iy
    note: str = ""


BMP_RE = re.compile(
    r"^\s*(\d+)\s*=\s*npc-(\d+)\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*(.*)$",
    re.I,
)


def parse_bmp(spec: str) -> BmpSpec:
    m = BMP_RE.match(spec)
    if not m:
        raise ValueError(f"无法解析 --bmp: {spec!r}\n"
                         f"格式: <slot>=npc-<id>(x,y,w,h)[ anim:frames=N,cols=C,...]")
    slot, src, x, y, w, h, rest = m.groups()
    anim = None
    rest = rest.strip()
    am = re.search(r"anim\s*:\s*(.+)$", rest, re.I)
    if am:
        anim = {}
        for kv in am.group(1).split(","):
            kv = kv.strip()
            if not kv:
                continue
            if kv.lower().startswith("interval"):
                iv = kv.split("=", 1)[1]
                ix, iy = iv.split(":")
                anim["ix"] = int(ix)
                anim["iy"] = int(iy)
                continue
            k, v = kv.split("=", 1)
            anim[k.strip().lower()] = int(v)
    return BmpSpec(int(slot), int(src), int(x), int(y), int(w), int(h), anim, rest)


def gen(name: str, length: int, bmps: List[BmpSpec], intent: str) -> str:
    bmps = sorted(bmps, key=lambda b: b.slot)
    bmp_cnt = (max(b.slot for b in bmps) + 1) if bmps else 1

    L: List[str] = []
    ap = L.append

    # ---- 头部块注释 ----
    ap("' =============================================================")
    ap(f"'  Animation: {name}")
    ap("'  ----------------------------------------------------------")
    ap(f"'  创作意图: {intent or '<TODO 一句话描述>'}")
    ap("'  呈现效果: <TODO 分阶段/分镜描述>")
    ap("'  对标/风格: <TODO>")
    ap("'")
    ap("'  接口契约 (tick 驱动, 内部禁止 call sleep; do/loop/for 可用于批量建 bmp):")
    ap(f"'    {name}_Launch(BmpIdOffset As Long, Return Integer)")
    ap(f"'    {name}_Tick(TimeStamp As Long, Return Integer)")
    ap(f"'    {name}_Finish(Return Integer)")
    ap(f"'    {name}_Length(Return Long)")
    ap("'")
    ap("'  依赖: Lib_Bmp (bmp_utils), Lib_Curver (cumath_utils)")
    ap("'        请在关卡早期 call exeScript(Lib_Bmp) / call exeScript(Lib_Curver)")
    ap("'")
    ap("'  bmp 分配 (相对 BmpIdOffset):")
    for b in bmps:
        extra = ""
        if b.anim:
            extra = " [anim " + ",".join(f"{k}={v}" for k, v in b.anim.items()) + "]"
        ap(f"'    +{b.slot} : npc-{b.src_id}({b.x},{b.y},{b.w},{b.h}){extra}")
    ap("' =============================================================")
    ap("")

    # ---- 调参区 ----
    ap("' ===================================== 调参区 (供人工微调)")
    ap(f"Dim {name}_len As Long = {length}        ' 动画总长(帧); 60fps => {length} 帧")
    ap(f"Dim {name}_bmpCnt As Long = {bmp_cnt}        ' 占用 bmp 数量")
    ap("")

    # ---- 内部状态 ----
    ap("' ===================================== 内部状态 (请勿手改)")
    ap(f"Dim {name}_offset As Long = 0")
    ap(f"Dim {name}_inited As Long = 0")
    ap("")

    # ---- 临时变量 ----
    ap("' ===================================== 临时变量 (temp_ 前缀)")
    ap("Dim temp_t As Double = 0")
    ap("Dim temp_a As Double = 0")
    ap("Dim temp_b As Double = 0")
    ap("Dim temp_i As Long = 0")
    ap("")

    # ---- _Length ----
    ap("' ===================================== 接口: 动画长度")
    ap(f"Export Script {name}_Length(Return Long)")
    ap(f"    Return {name}_len")
    ap("End Script")
    ap("")

    # ---- _Launch ----
    ap("' ===================================== 接口: 初始化 (申请 bmp)")
    ap(f"Export Script {name}_Launch(BmpIdOffset As Long, Return Integer)")
    ap(f"    If {name}_inited <> 0 Then")
    ap("        Return 0")
    ap("    End If")
    ap(f"    {name}_offset = BmpIdOffset")
    ap("")
    ap("    Call BmpNewStoreIsUseScreenCoords(1)")
    for b in bmps:
        ap(f"    ' +{b.slot}: npc-{b.src_id}({b.x},{b.y},{b.w},{b.h})")
        ap("    Call BmpNewStorePos(-10000, -10000)")
        ap("    Call BmpNewStoreScale(1, 1)")
        ap(f"    Call BmpNewStoreSrc({b.src_id}, {b.x}, {b.y}, {b.w}, {b.h})")
        ap(f"    Call BmpNew(BmpIdOffset + {b.slot})")
        ap(f"    Bitmap(BmpIdOffset + {b.slot}).zpos = 0.001")
    ap("")
    ap(f"    {name}_inited = 1")
    ap("    Return 0")
    ap("End Script")
    ap("")

    # ---- _Tick ----
    ap("' ===================================== 接口: 驱动 (按帧)")
    ap(f"Export Script {name}_Tick(TimeStamp As Long, Return Integer)")
    ap(f"    If {name}_inited = 0 Then")
    ap(f"        Call {name}_Launch(0)")
    ap("    End If")
    ap("")
    ap("    If TimeStamp < 0 Then")
    ap("        TimeStamp = 0")
    ap(f"    ElseIf TimeStamp > {name}_len Then")
    ap(f"        TimeStamp = {name}_len")
    ap("    End If")
    ap("")
    ap("    ' 归一化时间 t -> [0, 1]")
    ap(f"    Call CUTimeSetStamp(0, {name}_len)")
    ap("    temp_t = CUTimeCalcT(TimeStamp)")
    ap("")
    for b in bmps:
        ap(f"    ' ---- bmp +{b.slot}: TODO 面向时间的变化 ----")
        ap("    Call BmpStoreAnchor(0.5, 0.5)")
        ap(f"    Call BmpPos({name}_offset + {b.slot}, 400, 300)")
        if b.anim:
            frames = b.anim.get("frames", 1)
            cols = b.anim.get("cols", 1)
            loop = b.anim.get("loopfrom", 0)
            ix = b.anim.get("ix", 0)
            iy = b.anim.get("iy", 0)
            fps = b.anim.get("fps", 12)
            step = round(fps / 60.0, 4)
            ap(f"    Call BmpStoreAnimLoop({loop})")
            ap(f"    Call BmpStoreAnimInterval({ix}, {iy})")
            ap(f"    Call BmpStoreAnimInfo({frames}, {cols})")
            ap(f"    Call BmpStoreAnimPos({b.x}, {b.y}, {b.w}, {b.h})")
            ap(f"    Call BmpAnim({name}_offset + {b.slot}, {step} * TimeStamp)")
        else:
            ap(f"    Call BmpScale({name}_offset + {b.slot}, 1, 1)")
            ap(f"    Call BmpAlpha({name}_offset + {b.slot}, temp_t)")
        ap("")
    ap("    Return 0")
    ap("End Script")
    ap("")

    # ---- _Finish ----
    ap("' ===================================== 接口: 结束 (释放 bmp)")
    ap(f"Export Script {name}_Finish(Return Integer)")
    ap(f"    If {name}_inited <> 0 Then")
    ap(f"        For temp_i = 0 To {name}_bmpCnt - 1 Step 1")
    ap(f"            Call BmpDel({name}_offset + temp_i)")
    ap("        Next")
    ap(f"        {name}_inited = 0")
    ap("    End If")
    ap("    Return 0")
    ap("End Script")
    ap("")

    return "\n".join(L)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="从需求模板 DSL 生成动画骨架 .tea (tea-anim-helper)。")
    ap.add_argument("--name", required=True, help="动画名 (字母开头, 字母数字; 用作接口前缀)")
    ap.add_argument("--length", type=int, default=60, help="动画总长(帧), 默认 60")
    ap.add_argument("--bmp", action="append", default=[],
                    help='bmp 规格, 可多次。如 "0=npc-1(0,0,128,128)"')
    ap.add_argument("--intent", default="", help="创作意图(一句话)")
    ap.add_argument("-o", "--output",
                    help="输出 .tea 路径; 缺省打印到 stdout。"
                         "中间产物建议放 .cache/ 目录 (gitignore 规则 **/.cache/ 排除)")
    args = ap.parse_args(argv)

    if not re.match(r"^[A-Za-z]\w*$", args.name):
        print(f"非法动画名: {args.name!r} (须字母开头, 仅字母数字下划线)", file=sys.stderr)
        return 2

    try:
        bmps = [parse_bmp(s) for s in args.bmp]
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    code = gen(args.name, args.length, bmps, args.intent)

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(code)
        print(f"[anim_scaffold] 已生成 {args.output} "
              f"({args.name}, {len(bmps)} bmp, len={args.length})")
        print("下一步: 在 _Tick 内补全变化逻辑, 然后跑 anim_lint.py 静态校验")
    else:
        sys.stdout.write(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
