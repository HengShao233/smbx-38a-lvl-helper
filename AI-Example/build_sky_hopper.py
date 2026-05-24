#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sky Hopper —— 「天空跳跃者」
=============================

一个简单有趣的平台跳跃关卡。纯正的马里奥式跑跳乐趣！

█ 玩法
  Section 1 (云端平原): 宽阔草地、多层木平台、弹簧弹跳、金币收集
  Section 2 (天顶高峰): 玻璃浮空平台、高空连续跳跃、金币路线挑战

█ TeaScript
  - Welcome: 关卡欢迎语
  - SkyGuide: 每帧检测玩家区域 → 到达 Section 2 时弹出提示

文件输出: AI-Example/SkyHopper.lvl
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(os.path.dirname(HERE), '.tools', 'skills', 'smbx-38a', 'scripts')
sys.path.insert(0, SKILL_DIR)

from lvl_builder import LVLBuilder

# ╔══════════════════════════════════════════════════════════╗
# ║                       常量 / ID                           ║
# ╚══════════════════════════════════════════════════════════╝

# 方块
BLK_GRASS      = 457   # 草地地面
BLK_WOOD       = 188   # 木质平台
BLK_QUESTION   = 90    # 问号方块
BLK_BRICK      = 4     # 砖块
BLK_GLASS_BLUE = 24    # 蓝色玻璃（浮空平台）

# NPC
NPC_GOOMBA    = 1     # 栗子怪
NPC_GREEN_K   = 2     # 绿龟
NPC_COIN      = 33    # 浮动金币
NPC_SPRING    = 27    # 弹簧

# BGO
BGO_BUSH      = 59    # 灌木
BGO_FLOWER    = 60    # 花朵
BGO_TREE      = 71    # 树

# ─── Section 1: 云端平原 ──────────────────────────
S1_X, S1_Y, S1_W, S1_H = -200000, -200600, 1600, 600
S1_GROUND = -200032
S1_LOWER  = -200192
S1_MID    = -200320
P1_X, P1_Y = -199932, -200096

# ─── Section 2: 天顶高峰 ──────────────────────────
S2_X, S2_Y, S2_W, S2_H = -180000, -180600, 1280, 600
S2_GROUND = -180032
S2_RIGHT  = S2_X + S2_W   # -178720
S2_LOW    = -180160
S2_MID    = -180256
S2_HIGH   = -180352

# ╔══════════════════════════════════════════════════════════╗
# ║                       开始构建                            ║
# ╚══════════════════════════════════════════════════════════╝

b = LVLBuilder(title='Sky Hopper', p1=(P1_X, P1_Y))
b.add_section_grid()

b.configure_section(1, w=S1_W, h=S1_H, music=5)   # Overworld 音乐
b.configure_section(2, w=S2_W, h=S2_H, music=5)

# ════════════════════════════════════════════════════════════
# Section 1 — 云端平原
# ════════════════════════════════════════════════════════════

# 地面
for x in range(S1_X, S1_X + S1_W, 32):
    b.add_block(blk_id=BLK_GRASS, x=x, y=S1_GROUND)

# 下层平台 — 三段
for x in range(-199776, -199552, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_LOWER)
for x in range(-199488, -199264, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_LOWER)
for x in range(-199200, -199008, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_LOWER)

# 中层平台 — 两段
for x in range(-199648, -199424, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_MID)
for x in range(-199328, -199136, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_MID)

# 问号方块（含蘑菇）
b.add_block(blk_id=BLK_QUESTION, x=-199712, y=S1_LOWER, contain=1009)
b.add_block(blk_id=BLK_QUESTION, x=-199360, y=S1_LOWER, contain=1009)
b.add_block(blk_id=BLK_QUESTION, x=-199584, y=S1_MID,  contain=1009)

# 砖块
b.add_block(blk_id=BLK_BRICK, x=-199232, y=S1_LOWER)
b.add_block(blk_id=BLK_BRICK, x=-199200, y=S1_LOWER)
b.add_block(blk_id=BLK_BRICK, x=-199264, y=S1_MID)
b.add_block(blk_id=BLK_BRICK, x=-199232, y=S1_MID)

# 弹簧 — 地面 & 平台
b.add_npc(npc_id=NPC_SPRING, x=-199712, y=S1_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199328, y=S1_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199072, y=S1_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199552, y=S1_LOWER - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199264, y=S1_MID - 32)

# 金币 — 平台上方
for dx in [0, 32, 64, 96]:
    b.add_npc(npc_id=NPC_COIN, x=-199776 + dx, y=S1_LOWER - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=-199488 + dx, y=S1_LOWER - 64)
for dx in [0, 32, 64, 96]:
    b.add_npc(npc_id=NPC_COIN, x=-199200 + dx, y=S1_LOWER - 64)
for dx in [0, 32, 64, 96]:
    b.add_npc(npc_id=NPC_COIN, x=-199648 + dx, y=S1_MID - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=-199328 + dx, y=S1_MID - 64)

# 空中散落金币
b.add_npc(npc_id=NPC_COIN, x=-199456, y=S1_GROUND - 64)
b.add_npc(npc_id=NPC_COIN, x=-199424, y=S1_GROUND - 96)
b.add_npc(npc_id=NPC_COIN, x=-199520, y=S1_GROUND - 64)

# 敌人
b.add_npc(npc_id=NPC_GOOMBA,  x=-199584, y=S1_GROUND - 32, facing=-1)
b.add_npc(npc_id=NPC_GOOMBA,  x=-199072, y=S1_GROUND - 32, facing=1)
b.add_npc(npc_id=NPC_GREEN_K, x=-198656, y=S1_GROUND - 32, facing=-1)

# BGO 装饰
b.add_bgo(bgo_id=BGO_BUSH,   x=-199936, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=-199872, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=-199808, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_BUSH,   x=-199008, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_TREE,   x=-198528, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=-198464, y=S1_GROUND)

# 传送门：Section 1 → Section 2
b.add_warp(
    x=S1_X + S1_W - 64, y=S1_GROUND - 32,
    ex=S2_X + 64, ey=S2_GROUND - 32,
    layer='Default',
    type_=2,         # 门
    enter_dir=3,     # 从下方进入
    exit_dir=1,      # 从上方出来
)

# ════════════════════════════════════════════════════════════
# Section 2 — 天顶高峰
# ════════════════════════════════════════════════════════════

# 地面
for x in range(S2_X, S2_RIGHT, 32):
    b.add_block(blk_id=BLK_GRASS, x=x, y=S2_GROUND)

# 浮空玻璃平台 — 阶梯式上升
# 左列：低 → 中
for x in range(S2_X + 128, S2_X + 256, 32):
    b.add_block(blk_id=BLK_GLASS_BLUE, x=x, y=S2_LOW)
# 中左列：中 → 中
for x in range(S2_X + 352, S2_X + 480, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S2_MID)
# 中右列：高
for x in range(S2_X + 576, S2_X + 704, 32):
    b.add_block(blk_id=BLK_GLASS_BLUE, x=x, y=S2_HIGH)
# 右列：最高
for x in range(S2_X + 800, S2_X + 928, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S2_MID)

# 横向连接桥（中层）
for x in range(S2_X + 256, S2_X + 352, 32):
    b.add_block(blk_id=BLK_BRICK, x=x, y=S2_LOW)
for x in range(S2_X + 480, S2_X + 576, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S2_LOW)
for x in range(S2_X + 704, S2_X + 800, 32):
    b.add_block(blk_id=BLK_BRICK, x=x, y=S2_LOW)

# 问号方块
b.add_block(blk_id=BLK_QUESTION, x=S2_X + 192, y=S2_MID,  contain=1009)
b.add_block(blk_id=BLK_QUESTION, x=S2_X + 864, y=S2_MID,  contain=1009)

# 弹簧
b.add_npc(npc_id=NPC_SPRING, x=S2_X + 128, y=S2_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=S2_X + 416, y=S2_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=S2_X + 832, y=S2_GROUND - 32)

# 金币 — 沿平台路线分布
for dx in [0, 32, 64, 96]:
    b.add_npc(npc_id=NPC_COIN, x=S2_X + 128 + dx, y=S2_LOW - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=S2_X + 352 + dx, y=S2_MID - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=S2_X + 576 + dx, y=S2_HIGH - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=S2_X + 800 + dx, y=S2_MID - 64)

# 空中金币弧线
b.add_npc(npc_id=NPC_COIN, x=S2_X + 288, y=S2_GROUND - 64)
b.add_npc(npc_id=NPC_COIN, x=S2_X + 320, y=S2_GROUND - 96)
b.add_npc(npc_id=NPC_COIN, x=S2_X + 544, y=S2_GROUND - 64)
b.add_npc(npc_id=NPC_COIN, x=S2_X + 576, y=S2_GROUND - 96)

# 敌人
b.add_npc(npc_id=NPC_GOOMBA,  x=S2_X + 192, y=S2_GROUND - 32, facing=-1)
b.add_npc(npc_id=NPC_GOOMBA,  x=S2_X + 544, y=S2_GROUND - 32, facing=1)
b.add_npc(npc_id=NPC_GREEN_K, x=S2_X + 896, y=S2_GROUND - 32, facing=-1)

# BGO 装饰
b.add_bgo(bgo_id=BGO_BUSH,   x=S2_X + 48,  y=S2_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=S2_X + 112, y=S2_GROUND)
b.add_bgo(bgo_id=BGO_BUSH,   x=S2_RIGHT - 128, y=S2_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=S2_RIGHT - 64,  y=S2_GROUND)

# ════════════════════════════════════════════════════════════
# 图层
# ════════════════════════════════════════════════════════════
b.add_layer('Default',          status=1)
b.add_layer('Destroyed Blocks', status=1)
b.add_layer('Spawned NPCs',     status=1)

# ════════════════════════════════════════════════════════════
# 变量
# ════════════════════════════════════════════════════════════
b.add_variable('enteredS2', value=0, scope=0)

# ════════════════════════════════════════════════════════════
# 事件
# ════════════════════════════════════════════════════════════
b.add_event('Level - Start', autostart=1, script_name='Welcome')

# SkyGuide: 每帧检测玩家是否到达 Section 2（独立 autostart 事件）
b.add_event('SkyGuideTick', autostart=1, script_name='SkyGuide')

# ════════════════════════════════════════════════════════════
# TeaScript 脚本
# ════════════════════════════════════════════════════════════

# ── Welcome ──
WELCOME = """\
' Sky Hopper — 欢迎来到天空跳跃者！
call ShowMsg("SKY HOPPER")
call ShowMsg("Jump across the clouds! Go right and find the door to the summit!")
"""

# ── SkyGuide (每帧区域检测) ──
SKY_GUIDE = """\
' ============================================================
'  SkyGuide — 区域提示
'  检测玩家进入 Section 2 时弹出提示
'  每帧运行: do / call sleep(1) / loop
' ============================================================
dim px as double

' 玩家已进入 S2 的标志（防止重复弹消息）
v(enteredS2) = 0

do
    px = char(1).x
    if v(enteredS2) = 0 then
        if px > -181000 then
            v(enteredS2) = 1
            call ShowMsg("You reached the Sky Summit! Climb to the top!")
        end if
    end if
    call sleep(1)
loop
"""

b.add_script('Welcome',   WELCOME)
b.add_script('SkyGuide',  SKY_GUIDE)

# ════════════════════════════════════════════════════════════
# 保存
# ════════════════════════════════════════════════════════════
out_path = os.path.join(HERE, 'SkyHopper.lvl')
b.save(out_path)
print(f'[OK] Sky Hopper level saved to: {out_path}')
print('Sections:')
print(f'  S1 (Cloud Plains): ({S1_X}, {S1_Y}) {S1_W}x{S1_H}')
print(f'  S2 (Sky Summit):   ({S2_X}, {S2_Y}) {S2_W}x{S2_H}')
print(f'  Player start:      ({P1_X}, {P1_Y})')
print(f'  Warp:              ({S1_X + S1_W - 64}, {S1_GROUND - 32}) -> ({S2_X + 64}, {S2_GROUND - 32})')
