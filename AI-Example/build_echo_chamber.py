#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo Chamber —— 「回声大厅」之回响 Boss 战
============================================

一场围绕「时间录制 / 节奏共鸣 / 三相色墙」的全新 Boss 战体验。

█ 核心机制（市面上没见过的组合）

  1. 「回响录制」(Echo Record)
     脚本每帧把玩家的 (x, y) 写入一个长度为 echoLen 的环形 buffer。
     echoLen 帧之后，Boss 会在玩家"过去那一帧"的位置生成一颗回声弹
     —— 也就是说，**玩家自己 N 秒前的轨迹就是 Boss 的弹幕**。
     越熟悉关卡的玩家越要时刻警惕"未来的自己"会被攻击。

  2. 「韵律相位」(Rhythm Phase)
     战斗按 240 帧 (4 秒) 为一小节循环；每小节有 4 拍。
     每一拍的"重音帧"在屏幕上由 BmpCreate 画的节拍条精准提示。
     **玩家在重音帧上踩中 Boss 头部 = 双倍伤害 + 解除 Boss 一帧无敌**。
     不在节拍踩 = 普通伤害但 Boss 立即开始一次反击突进。

  3. 「三相色墙」(Tri-Phase Walls)
     场地左、中、右各有三组色墙（红 / 绿 / 蓝），每 3 秒切换"激活色"。
     **只有当前激活色的墙是实体的，其余两种是穿透的**。
     - Boss 召唤的回声弹会被实体墙吸收（玩家可主动诱导 Boss 攻击撞墙）。
     - 玩家可在合适的相位下穿过墙到达 Boss 后方击败 Boss。

  4. 「自定义 HUD」
     用 `BmpCreate` 在屏幕顶部绘制：
       - 节拍条 (4 拍指示器)
       - 三色相位灯
       - Boss HP 条（红色填充块）

  5. 「回声幻影」
     回声弹本身用 NPC 13（Bullet Bill 子弹），用 forecolor 染成半透明青色。

█ 关卡布局
  Section 1 (训练厅): 介绍机制
  Section 2 (回声大厅): Boss 战竞技场

█ Boss 三阶段
  - Phase 1 (HP > 7): 单弹回放，相位墙 3 秒切换，节拍 4/4
  - Phase 2 (HP 4-7): 双弹回放，相位墙 2 秒切换
  - Phase 3 (HP < 4): "和声"模式 —— 三连音回放，3/4 拍，墙切换 1.5 秒

文件输出: AI-Example/EchoChamber.lvl
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(os.path.dirname(HERE), '.tools', 'skills', 'smbx-38a', 'scripts')
sys.path.insert(0, SKILL_DIR)

from lvl_builder import LVLBuilder

# ╔══════════════════════════════════════════════════════════╗
# ║                       常量 / NPC ID                       ║
# ╚══════════════════════════════════════════════════════════╝

# 方块
BLK_DARK_STONE = 186
BLK_PURPLE     = 274
BLK_LIGHT      = 188
BLK_GLASS_RED   = 22
BLK_GLASS_GREEN = 23
BLK_GLASS_BLUE  = 24

# NPC
NPC_BOSS    = 168     # Bowser Statue
NPC_COIN    = 33      # 金币 (BmpCreate 贴图源)
NPC_BULLET  = 13      # 子弹 (回声弹)
NPC_GOOMBA  = 1
NPC_SPRING  = 27

# BGO
BGO_DARK_BG = 64
BGO_GLOW    = 51

# ─── Section 1: 训练厅 ─────────────────────────────
S1_X, S1_Y, S1_W, S1_H = -200000, -200600, 1600, 600
S1_GROUND = -200032
P1_X, P1_Y = -199932, -200096

# ─── Section 2: Echo Chamber 竞技场 ────────────────
S2_X, S2_Y, S2_W, S2_H = -180000, -180600, 1280, 600
S2_GROUND = -180032
S2_LEFT, S2_RIGHT = S2_X, S2_X + S2_W
S2_TOP, S2_BOTTOM = S2_Y, S2_Y + S2_H

WALL_LEFT_X   = S2_X + 320
WALL_MID_X    = S2_X + 640
WALL_RIGHT_X  = S2_X + 960

BOSS_X = S2_X + S2_W - 128
BOSS_Y = S2_GROUND - 96

# ╔══════════════════════════════════════════════════════════╗
# ║                       开始构建                            ║
# ╚══════════════════════════════════════════════════════════╝

b = LVLBuilder(title='Echo Chamber', p1=(P1_X, P1_Y))
b.add_section_grid()

b.configure_section(1, w=S1_W, h=S1_H, music=5)
b.configure_section(2, w=S2_W, h=S2_H, music=17, background='17,-1')

# ════════════════════════════════════════════════════════════
# Section 1 — 训练厅
# ════════════════════════════════════════════════════════════
for x in range(S1_X, S1_X + S1_W, 32):
    b.add_block(blk_id=BLK_LIGHT, x=x, y=S1_GROUND)
for x in range(S1_X, S1_X + S1_W, 32):
    b.add_block(blk_id=BLK_DARK_STONE, x=x, y=S1_Y)
for y in range(S1_Y, S1_GROUND, 32):
    b.add_block(blk_id=BLK_DARK_STONE, x=S1_X, y=y)
    b.add_block(blk_id=BLK_DARK_STONE, x=S1_X + S1_W - 32, y=y)

DEMO_RED_X   = S1_X + 320
DEMO_GREEN_X = S1_X + 480
DEMO_BLUE_X  = S1_X + 640
for dy in range(0, 256, 32):
    y = S1_GROUND - 32 - dy
    b.add_block(blk_id=BLK_GLASS_RED,   x=DEMO_RED_X,   y=y, layer='WallRed')
    b.add_block(blk_id=BLK_GLASS_GREEN, x=DEMO_GREEN_X, y=y, layer='WallGreen')
    b.add_block(blk_id=BLK_GLASS_BLUE,  x=DEMO_BLUE_X,  y=y, layer='WallBlue')

for x in range(S1_X + 800, S1_X + 1024, 32):
    b.add_block(blk_id=BLK_LIGHT, x=x, y=S1_GROUND - 128)

b.add_warp(
    x=S1_X + S1_W - 96, y=S1_GROUND - 32,
    ex=S2_X + 64, ey=S2_GROUND - 32,
    layer='Default', type_=2, enter_dir=3, exit_dir=1,
)
for dx in range(0, 96, 32):
    b.add_npc(npc_id=NPC_COIN, x=S1_X + 100 + dx, y=S1_GROUND - 64)

# ════════════════════════════════════════════════════════════
# Section 2 — Echo Chamber 竞技场
# ════════════════════════════════════════════════════════════
for x in range(S2_X, S2_RIGHT, 32):
    b.add_block(blk_id=BLK_DARK_STONE, x=x, y=S2_GROUND)
for x in range(S2_X, S2_RIGHT, 32):
    b.add_block(blk_id=BLK_DARK_STONE, x=x, y=S2_TOP)
for y in range(S2_TOP, S2_GROUND, 32):
    b.add_block(blk_id=BLK_DARK_STONE, x=S2_X, y=y)
    b.add_block(blk_id=BLK_DARK_STONE, x=S2_RIGHT - 32, y=y)

BOSS_PLATFORM_Y = S2_GROUND - 64
for x in range(S2_RIGHT - 224, S2_RIGHT - 32, 32):
    b.add_block(blk_id=BLK_DARK_STONE, x=x, y=BOSS_PLATFORM_Y)

def add_phase_wall(x_pos: int, layer_name: str, blk_id: int):
    y_top = S2_TOP + 32
    y_bot = BOSS_PLATFORM_Y + 32
    for y in range(y_top, y_bot, 32):
        b.add_block(blk_id=blk_id, x=x_pos, y=y, layer=layer_name)

add_phase_wall(WALL_LEFT_X,  'WallRed',   BLK_GLASS_RED)
add_phase_wall(WALL_MID_X,   'WallGreen', BLK_GLASS_GREEN)
add_phase_wall(WALL_RIGHT_X, 'WallBlue',  BLK_GLASS_BLUE)

for x in range(WALL_LEFT_X + 64, WALL_LEFT_X + 224, 32):
    b.add_block(blk_id=BLK_LIGHT, x=x, y=S2_GROUND - 160, layer='Platforms')
for x in range(WALL_MID_X + 64, WALL_MID_X + 224, 32):
    b.add_block(blk_id=BLK_LIGHT, x=x, y=S2_GROUND - 192, layer='Platforms')

b.add_npc(npc_id=NPC_SPRING, x=S2_X + 96, y=S2_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=WALL_LEFT_X - 64, y=S2_GROUND - 32)

b.add_npc(
    npc_id=NPC_BOSS, x=BOSS_X, y=BOSS_PLATFORM_Y - 64,
    layer='Boss', friendly=0, nomove=1,
)
b.add_bgo(bgo_id=BGO_GLOW, x=BOSS_X - 16, y=BOSS_PLATFORM_Y - 96, layer='Boss')

# ════════════════════════════════════════════════════════════
# 图层
# ════════════════════════════════════════════════════════════
b.add_layer('Default',          status=1)
b.add_layer('Destroyed Blocks', status=1)
b.add_layer('Spawned NPCs',     status=1)
b.add_layer('Boss',             status=1)
b.add_layer('Platforms',        status=1)
b.add_layer('WallRed',          status=1)
b.add_layer('WallGreen',        status=0)
b.add_layer('WallBlue',         status=0)
b.add_layer('Victory',          status=0)

# ════════════════════════════════════════════════════════════
# 用户变量 (V 行)
# ════════════════════════════════════════════════════════════
b.add_variable('bossHP',      10, scope=0)
b.add_variable('bossPhase',    1, scope=0)
b.add_variable('bossAlive',    1, scope=0)
b.add_variable('bossInv',      0, scope=0)
b.add_variable('beat',         0, scope=0)
b.add_variable('beatTimer',    0, scope=0)
b.add_variable('phaseColor',   0, scope=0)
b.add_variable('phaseTimer',   0, scope=0)
b.add_variable('echoHead',     0, scope=0)
b.add_variable('echoFilled',   0, scope=0)
b.add_variable('frameCount',   0, scope=0)
b.add_variable('comboHits',    0, scope=0)

# ════════════════════════════════════════════════════════════
# 用户数组 (R 行)
# ════════════════════════════════════════════════════════════
# 38A 用户数组用 R 行声明，不能用 V 行假装。
b.add_array('echoX', 'echoY')

# ════════════════════════════════════════════════════════════
# 事件 (E 行)
# ════════════════════════════════════════════════════════════
# 38A 没有"每帧自动事件"。每帧脚本的标准范式：
#     1) 用一个 autostart=1 的事件，在 Level Start 时触发一次
#     2) 脚本内部 do ... call sleep(1) ... loop 永久循环
#
# 一个 lvl 只允许一个 `Level - Start`，所以两个长循环要分别挂在
# `Level - Start` 和另一个 autostart=1 的自定义名字事件上。
b.add_event('Level - Start', autostart=1, script_name='EchoAI')
b.add_event('HUDStart',      autostart=1, script_name='EchoHUD')
b.add_event('BossDefeated',  autostart=0,
            show_layers=['Victory'],
            hide_layers=['Boss', 'WallRed', 'WallGreen', 'WallBlue'])

# ════════════════════════════════════════════════════════════
# 脚本 (SU 行)
# ════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────
# EchoAI — Boss 主控（每帧驱动，含初始化与录制/反伤/相位）
# ──────────────────────────────────────────────────────────
ECHO_AI = """\
' ============================================================
'  EchoAI — 回响 Boss 主控（每帧驱动）
'  入口: Level - Start (autostart=1)
'  范式: do / call sleep(1) / loop
' ============================================================

' ===== 所有 dim 写在循环外 (patch 31 前 bug + 性能) =====
dim echoLen as integer
dim beatFrames as integer
dim phaseFrames as integer
dim invFrames as integer
dim i as integer
dim bi as integer
dim bossIdx as integer
dim curHP as double
dim px as double
dim py as double
dim bx as double
dim by as double
dim readIdx as integer
dim oldX as double
dim oldY as double
dim dirX as double
dim dirY as double
dim mag as double
dim spd as double
dim shotID as integer
dim isHeavyBeat as integer
dim relY as double
dim beatCount as integer

' ===== 一次性初始化 =====
echoLen = 90
beatFrames = 60
phaseFrames = 180
invFrames = 12

v(bossHP) = 10
v(bossPhase) = 1
v(bossAlive) = 1
v(bossInv) = 0
v(beat) = 0
v(beatTimer) = 0
v(phaseColor) = 0
v(phaseTimer) = 0
v(echoHead) = 0
v(echoFilled) = 0
v(frameCount) = 0
v(comboHits) = 0

' 初始化两个用户数组
call redim(0, echoX, echoLen)
call redim(0, echoY, echoLen)

' 找 Boss 并设置初始 HP
for bi = 1 to sysval(ncount)
    if NPC(bi).id = 168 then
        NPC(bi).health = 10
    end if
next

call ShowMsg("ECHO CHAMBER")
call ShowMsg("Your past is your enemy. Step on the beat to strike back.")

' ===== 主循环（永久每帧执行） =====
do
    if v(bossAlive) = 0 then
        ' 战斗结束，但仍需活着循环以保持脚本驻留（也可 exit do 退出）
        call sleep(1)
    else
        v(frameCount) = v(frameCount) + 1

        ' ────── 找 Boss 索引 ──────
        bossIdx = 0
        for i = 1 to sysval(ncount)
            if NPC(i).id = 168 then
                bossIdx = i
            end if
        next

        if bossIdx = 0 then
            v(bossAlive) = 0
            call ShowMsg("ECHO SILENCED. The chamber falls quiet.")
            call LSet("Boss", 2, 0)
            call LSet("WallRed", 2, 0)
            call LSet("WallGreen", 2, 0)
            call LSet("WallBlue", 2, 0)
            call LSet("Victory", 1, 0)
        else
            ' ────── 阶段判定 ──────
            curHP = NPC(bossIdx).health
            v(bossHP) = curHP
            if curHP > 7 then
                v(bossPhase) = 1
                beatFrames = 60
                phaseFrames = 180
                echoLen = 90
            elseif curHP > 4 then
                v(bossPhase) = 2
                beatFrames = 45
                phaseFrames = 120
                echoLen = 75
            else
                v(bossPhase) = 3
                beatFrames = 30
                phaseFrames = 90
                echoLen = 60
            end if

            ' ────── Boss 无敌闪烁 ──────
            if v(bossInv) > 0 then
                v(bossInv) = v(bossInv) - 1
                if v(bossInv) mod 4 < 2 then
                    NPC(bossIdx).forecolor = rgba(255, 255, 0, 220)
                else
                    NPC(bossIdx).forecolor = -1
                end if
            else
                if v(bossPhase) = 3 then
                    NPC(bossIdx).forecolor = rgba(255, 60, 60, 200)
                elseif v(bossPhase) = 2 then
                    NPC(bossIdx).forecolor = rgba(255, 180, 60, 200)
                else
                    NPC(bossIdx).forecolor = -1
                end if
            end if

            ' ────── 玩家位置 ──────
            px = char(1).x
            py = char(1).y
            bx = NPC(bossIdx).x
            by = NPC(bossIdx).y

            ' ────── 录制玩家位置到环形 buffer ──────
            array(echoX(v(echoHead))) = px
            array(echoY(v(echoHead))) = py
            v(echoHead) = v(echoHead) + 1
            if v(echoHead) >= echoLen then
                v(echoHead) = 0
                v(echoFilled) = 1
            end if

            ' ────── 节拍推进 ──────
            v(beatTimer) = v(beatTimer) + 1
            if v(beatTimer) >= beatFrames then
                v(beatTimer) = 0
                if v(bossPhase) = 3 then
                    beatCount = 3
                else
                    beatCount = 4
                end if
                v(beat) = v(beat) + 1
                if v(beat) >= beatCount then
                    v(beat) = 0
                end if
            end if

            ' 重音帧判定: 节拍 0 + 计时 < 8
            isHeavyBeat = 0
            if v(beat) = 0 then
                if v(beatTimer) < 8 then
                    isHeavyBeat = -1
                end if
            end if

            ' ────── 相位墙切换 ──────
            v(phaseTimer) = v(phaseTimer) + 1
            if v(phaseTimer) >= phaseFrames then
                v(phaseTimer) = 0
                v(phaseColor) = v(phaseColor) + 1
                if v(phaseColor) >= 3 then
                    v(phaseColor) = 0
                end if
                if v(phaseColor) = 0 then
                    call LSet("WallRed", 1, 0)
                    call LSet("WallGreen", 2, 0)
                    call LSet("WallBlue", 2, 0)
                elseif v(phaseColor) = 1 then
                    call LSet("WallRed", 2, 0)
                    call LSet("WallGreen", 1, 0)
                    call LSet("WallBlue", 2, 0)
                else
                    call LSet("WallRed", 2, 0)
                    call LSet("WallGreen", 2, 0)
                    call LSet("WallBlue", 1, 0)
                end if
                call AudioSet(2, 12, 0, "")
            end if

            ' ────── 节拍反伤窗口 (重音 + 踩头) ──────
            if isHeavyBeat = -1 then
                if v(bossInv) = 0 then
                    relY = py - by
                    if relY < 0 then
                        if relY > -120 then
                            if abs(px - bx) < 80 then
                                NPC(bossIdx).health = NPC(bossIdx).health - 2
                                v(bossInv) = invFrames * 2
                                v(comboHits) = v(comboHits) + 1
                                ' FXCreate 必须 10 参: id, x, y, sx, sy, frames, animspeed, const, gravity, advanced
                                call FXCreate(75, bx, by - 16, 0, -2, 0, 0, 0, 0, 0)
                                call FXCreate(75, bx + 16, by, 0, -2, 0, 0, 0, 0, 0)
                                call AudioSet(2, 21, 0, "")
                                call ShowMsg("PERFECT BEAT! +2")
                            end if
                        end if
                    end if
                end if
            end if

            ' ────── 回声攻击 (从 buffer 取过去位置) ──────
            if v(echoFilled) = 1 then
                if v(bossPhase) = 1 then
                    if v(frameCount) mod 60 = 0 then
                        readIdx = v(echoHead)
                        oldX = array(echoX(readIdx))
                        oldY = array(echoY(readIdx))
                        dirX = oldX - bx
                        dirY = oldY - by
                        mag = sqr(dirX * dirX + dirY * dirY)
                        if mag > 1 then
                            spd = 5
                            shotID = NCreate(13, bx, by - 16, dirX / mag * spd, dirY / mag * spd, 0, 0)
                        end if
                    end if
                elseif v(bossPhase) = 2 then
                    if v(frameCount) mod 35 = 0 then
                        readIdx = v(echoHead)
                        oldX = array(echoX(readIdx))
                        oldY = array(echoY(readIdx))
                        dirX = oldX - bx
                        dirY = oldY - by
                        mag = sqr(dirX * dirX + dirY * dirY)
                        if mag > 1 then
                            spd = 6
                            shotID = NCreate(13, bx, by - 16, dirX / mag * spd, dirY / mag * spd, 0, 0)
                        end if
                        ' 第二弹: 当前位置
                        dirX = px - bx
                        dirY = py - by
                        mag = sqr(dirX * dirX + dirY * dirY)
                        if mag > 1 then
                            shotID = NCreate(13, bx, by, dirX / mag * spd, dirY / mag * spd, 0, 0)
                        end if
                    end if
                else
                    ' 阶段 3: 三连音
                    if v(frameCount) mod 20 = 0 then
                        readIdx = v(echoHead)
                        oldX = array(echoX(readIdx))
                        oldY = array(echoY(readIdx))
                        dirX = oldX - bx
                        dirY = oldY - by
                        mag = sqr(dirX * dirX + dirY * dirY)
                        if mag > 1 then
                            spd = 7
                            shotID = NCreate(13, bx, by, dirX / mag * spd, dirY / mag * spd, 0, 0)
                            shotID = NCreate(13, bx, by - 24, dirX / mag * spd * 0.8, dirY / mag * spd * 1.2, 0, 0)
                            shotID = NCreate(13, bx, by - 48, dirX / mag * spd * 1.2, dirY / mag * spd * 0.8, 0, 0)
                        end if
                    end if
                    if v(frameCount) mod 240 = 0 then
                        shotID = NCreate(1, bx - 32, by, 0, 0, 0, 0)
                    end if
                end if
            end if

            ' ────── 普通踩头 (非重音) ──────
            if v(bossInv) = 0 then
                if isHeavyBeat = 0 then
                    relY = py - by
                    if relY < 0 then
                        if relY > -56 then
                            if abs(px - bx) < 48 then
                                if char(1).ysp > 0 then
                                    NPC(bossIdx).health = NPC(bossIdx).health - 1
                                    v(bossInv) = invFrames
                                    char(1).ysp = -8
                                    call FXCreate(75, bx, by - 16, 0, -2, 0, 0, 0, 0, 0)
                                end if
                            end if
                        end if
                    end if
                end if
            end if

            ' ────── Boss 死亡判定 ──────
            if NPC(bossIdx).health <= 0 then
                v(bossAlive) = 0
                NPC(bossIdx).health = 0
                call ShowMsg("ECHO SILENCED. Combo: " & val(comboHits))
                call LSet("Boss", 2, 0)
                call LSet("WallRed", 2, 0)
                call LSet("WallGreen", 2, 0)
                call LSet("WallBlue", 2, 0)
                call LSet("Victory", 1, 0)
                call AudioSet(2, 22, 0, "")
            end if
        end if

        ' 每帧 sleep(1) —— 必不可少，否则游戏冻结
        call sleep(1)
    end if
loop
"""

# ──────────────────────────────────────────────────────────
# EchoHUD — 自定义 BmpCreate HUD（每帧驱动）
# ──────────────────────────────────────────────────────────
ECHO_HUD = """\
' ============================================================
'  EchoHUD — 自定义 HUD (每帧驱动)
'  入口: HUDStart (autostart=1)
'  - 100..103: 4 个节拍指示器
'  - 110..112: 三色相位灯
'  - 120/121: Boss HP 背景/填充
' ============================================================

dim k as integer
dim hpRatio as double
dim hpW as double
dim activeBeat as integer
dim activeBeats as integer
dim phaseHL as integer

' ===== 一次性创建所有 Bitmap =====
for k = 0 to 3
    call BmpCreate(100 + k, 33, 1, 1, 0, 0, 16, 16, 240 + k * 56, 24, 1.5, 1.5, 0, 0, 0, rgba(80, 80, 80, 220))
next
call BmpCreate(110, 33, 1, 1, 0, 0, 16, 16, 32, 24, 1.5, 1.5, 0, 0, 0, rgba(255, 60, 60, 255))
call BmpCreate(111, 33, 1, 1, 0, 0, 16, 16, 64, 24, 1.5, 1.5, 0, 0, 0, rgba(60, 80, 60, 100))
call BmpCreate(112, 33, 1, 1, 0, 0, 16, 16, 96, 24, 1.5, 1.5, 0, 0, 0, rgba(60, 60, 80, 100))
call BmpCreate(120, 33, 1, 1, 0, 0, 16, 16, 200, 540, 13.0, 0.6, 0, 0, 0, rgba(40, 40, 40, 220))
call BmpCreate(121, 33, 1, 1, 0, 0, 16, 16, 200, 540, 13.0, 0.6, 0, 0, 0, rgba(220, 40, 40, 240))

' ===== 主循环（每帧刷新 HUD） =====
do
    activeBeat = v(beat)
    if v(bossPhase) = 3 then
        activeBeats = 3
    else
        activeBeats = 4
    end if

    for k = 0 to 3
        if k >= activeBeats then
            Bitmap(100 + k).forecolor = rgba(20, 20, 20, 100)
        elseif k = activeBeat then
            if k = 0 then
                Bitmap(100 + k).forecolor = rgba(255, 230, 80, 255)
            else
                Bitmap(100 + k).forecolor = rgba(180, 180, 180, 230)
            end if
        else
            Bitmap(100 + k).forecolor = rgba(80, 80, 80, 200)
        end if
    next

    phaseHL = v(phaseColor)
    if phaseHL = 0 then
        Bitmap(110).forecolor = rgba(255, 60, 60, 255)
        Bitmap(111).forecolor = rgba(60, 80, 60, 100)
        Bitmap(112).forecolor = rgba(60, 60, 80, 100)
    elseif phaseHL = 1 then
        Bitmap(110).forecolor = rgba(80, 60, 60, 100)
        Bitmap(111).forecolor = rgba(80, 240, 80, 255)
        Bitmap(112).forecolor = rgba(60, 60, 80, 100)
    else
        Bitmap(110).forecolor = rgba(80, 60, 60, 100)
        Bitmap(111).forecolor = rgba(60, 80, 60, 100)
        Bitmap(112).forecolor = rgba(80, 80, 240, 255)
    end if

    hpRatio = v(bossHP) / 10.0
    if hpRatio < 0 then
        hpRatio = 0
    end if
    if hpRatio > 1 then
        hpRatio = 1
    end if
    hpW = 13.0 * hpRatio
    Bitmap(121).scalex = hpW

    if v(bossPhase) = 3 then
        if sysval(gametime) mod 6 < 3 then
            Bitmap(120).forecolor = rgba(80, 0, 0, 240)
        else
            Bitmap(120).forecolor = rgba(40, 40, 40, 220)
        end if
    end if

    call sleep(1)
loop
"""

b.add_script('EchoAI',  ECHO_AI)
b.add_script('EchoHUD', ECHO_HUD)

# ──────────────────────────────────────────────────────────
# FireBall — NPC 13 (子弹/回声弹) 的"类绑定脚本"
# ──────────────────────────────────────────────────────────
# 这是一个**每帧每实例**自动调用的脚本：所有 type=13 的 NPC（含
# EchoAI 用 NCreate(13, ...) 生成的回声弹）每帧都会跑一次本脚本。
#
# 关键差异（vs 关卡级 do/sleep/loop 脚本）:
#   - **不是**隐式上下文：脚本里**没有**默认对象，必须显式获取自身索引
#     当前实例的索引通过 `sysval(param1)` 拿（38A 文档: NextFrame NPC 事件
#     的 param1 = NPC 的 ID/index）。再用 `with NPC(idx) ... end with`
#     或 `NPC(idx).field` 显式访问自身。
#   - **不要写 do/sleep/loop**：引擎已经在替你每帧调一次，写循环反而冻死该实例
#   - 绑定方式: <lvl同名目录>/npc-13.txt 写 "scripts=FireBall"
#     LVLBuilder.add_npc_class_script() 一站式封装了这一切
FIRE_BALL = """\
' ============================================================
'  FireBall — NPC 13 (子弹) 类绑定脚本
'  绑定: <lvl目录>/npc-13.txt -> scripts=FireBall
'  调用: 每帧每实例 (引擎自动调用，**不要写 do/loop**)
'  自身索引: sysval(param1) (NextFrame NPC 事件的 param1 = 当前 NPC 的 ID)
' ============================================================
' alive 字段语义提醒 (38A 中 NPC 与 Char 相反!):
'   NPC.alive  : 0 = 死, 非 0 = 活  (与英文字面一致)
'   Char.alive : 1 = 死, 0 = 活     (反直觉! 见 Char 文档)
' 推荐玩家受伤/死亡用 SpEvent: 1=受伤(自动降级+无敌), 2=死亡
' 这样既不依赖 char.alive 的反直觉值, 又让引擎处理大/小马里奥差异。

dim selfIdx as integer
dim px as double
dim py as double
dim dx as double
dim dy as double

' 关键：拿到当前实例的索引（38A NextFrame 事件 param1 = NPC 的 ID）
selfIdx = sysval(param1)

px = char(1).x
py = char(1).y

' 显式用 with NPC(selfIdx) 进入当前实例的上下文
with NPC(selfIdx)
    ' AABB 重叠：玩家 ~32×60；子弹 ~16×16
    dx = abs((px + 16) - (.x + 8))
    dy = abs((py + 30) - (.y + 8))

    if dx < 24 then
        if dy < 38 then
            if char(1).invtime <= 0 then
                ' 让引擎处理伤害：大马里奥降级、小马里奥死亡、火/狸力等形态
                ' 都自动正确处理；省得手写 status/invtime 还容易踩 alive 反向坑
                call SpEvent(1)
                ' 视觉 + 音效反馈 (FXCreate 必须 10 参)
                call FXCreate(75, .x, .y - 8, 0, -2, 0, 0, 0, 0, 0)
            end if
            ' 自身销毁: NPC.alive = 0 是死亡 (与 Char.alive = 1 才死亡相反!)
            .alive = 0
        end if
    end if
end with
"""

# 一站式：嵌入脚本 + 写 EchoChamber/npc-13.txt 的 scripts=FireBall
b.add_npc_class_script(npc_id=13, script_name='FireBall',
                       script_body=FIRE_BALL)

# ════════════════════════════════════════════════════════════
# 自定义贴图占位（HUD 用 NPC 33 作贴图源）
# ════════════════════════════════════════════════════════════
b.add_custom_texture(33, '00081')

# ════════════════════════════════════════════════════════════
# 保存
# ════════════════════════════════════════════════════════════
out_path = os.path.join(HERE, 'EchoChamber.lvl')
b.save(out_path)
print(f'[OK] Echo Chamber level saved to: {out_path}')
print('Sections:')
print(f'  S1 (Tutorial Hall):  ({S1_X}, {S1_Y}) {S1_W}x{S1_H}')
print(f'  S2 (Echo Chamber):   ({S2_X}, {S2_Y}) {S2_W}x{S2_H}')
print(f'  Boss spawn:          ({BOSS_X}, {BOSS_PLATFORM_Y - 64})')
print(f'  Walls L/M/R x:       {WALL_LEFT_X} / {WALL_MID_X} / {WALL_RIGHT_X}')
