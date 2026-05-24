#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spring Garden — 弹跳花园 + 疯狂 Boss 战

Section 1: 弹跳花园（弹簧平台收集金币）
Section 2: Boss 竞技场 —— 对抗疯狂大 Boss！

Boss 战设计：
- Boss 是 Boom Boom (NPC 15)，高血量，由 TeaScript 驱动三阶段 AI
- Phase 1 (HP>5): 缓慢追击玩家 + 周期性召唤栗子怪
- Phase 2 (3<=HP<=5): 加速追击 + 弹幕射击（火球） + 召唤更频繁
- Phase 3 (HP<3): 狂暴模式！极速追击 + 密集弹幕 + 连续召唤
- 场地有左右两个弹簧平台帮助躲避
- Boss 死亡后触发胜利事件，显示通关消息
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.join(os.path.dirname(HERE), '.ai', 'skills', 'smbx-38a', 'scripts')
sys.path.insert(0, SKILL_DIR)

from lvl_builder import LVLBuilder

# ─── 常用方块/BGO/NPC ID ───
BLK_STONE    = 186   # 石砖方块（Boss 战地面用）
BLK_WOOD     = 188   # 木质平台方块
BLK_QUESTION = 90    # 问号方块
BLK_BRICK    = 4     # 砖块
BLK_GRASS    = 457   # 草地地面方块
NPC_GOOMBA   = 1     # 栗子怪
NPC_COIN     = 33    # 浮动金币
NPC_SPRING   = 27    # 弹簧
NPC_BOSS     = 15    # Boom Boom (Boss)
NPC_HAMMER   = 29    # 锤子兄弟
BGO_BUSH     = 59    # 灌木装饰
BGO_FLOWER   = 60    # 花朵装饰

# ═══════════════════════════════════════════
# Section 1 — 弹跳花园
# ═══════════════════════════════════════════
S1_X = -200000
S1_Y = -200600
S1_W = 1600
S1_H = 600
S1_GROUND = -200032
P1_X = -199932
P1_Y = -200096
S1_LOWER = -200192
S1_MID   = -200320
S1_HIGH  = -200448

# ═══════════════════════════════════════════
# Section 2 — Boss 竞技场
# ═══════════════════════════════════════════
S2_X = -180000
S2_Y = -180600
S2_W = 1200
S2_H = 600
S2_GROUND = -180032
S2_LEFT   = S2_X          # -180000
S2_RIGHT  = S2_X + S2_W  # -178800
S2_TOP    = S2_Y          # -180600
S2_BOTTOM = S2_Y + S2_H  # -180000

# Boss 战平台 y 坐标
S2_PLAT_Y = -180224   # 两侧弹簧平台
S2_HIGH_Y = -180384   # 顶部小平台

# ─── 开始构建 ───
b = LVLBuilder(title='Spring Garden', p1=(P1_X, P1_Y))

# 1. 铺满 21 个 section
b.add_section_grid()

# 2. 配置 Section 1 & 2
b.configure_section(1, w=S1_W, h=S1_H, music=5)   # Overworld
b.configure_section(2, w=S2_W, h=S2_H, music=17)   # Boss 战音乐

# ═══════════════════════════════════════════
# Section 1 地形
# ═══════════════════════════════════════════

# 地面（中间有浅坑）
pit_start = -199392
pit_end   = -199328
for x in range(S1_X, S1_X + S1_W, 32):
    if pit_start <= x <= pit_end:
        continue
    b.add_block(blk_id=BLK_GRASS, x=x, y=S1_GROUND)

# 低层平台
for x in range(-199744, -199584, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_LOWER)
for x in range(-199264, -199104, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_LOWER)

# 中层平台
for x in range(-199584, -199392, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_MID)

# 高层平台
for x in range(-199520, -199392, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S1_HIGH)

# 问号方块
b.add_block(blk_id=BLK_QUESTION, x=-199808, y=S1_LOWER, contain=1009)
b.add_block(blk_id=BLK_QUESTION, x=-199168, y=S1_LOWER, contain=1009)
b.add_block(blk_id=BLK_QUESTION, x=-199520, y=S1_MID, contain=0)
b.add_block(blk_id=BLK_QUESTION, x=-199456, y=S1_MID, contain=0)

# 砖块
b.add_block(blk_id=BLK_BRICK, x=-199424, y=S1_LOWER)
b.add_block(blk_id=BLK_BRICK, x=-199296, y=S1_LOWER)

# 弹簧
b.add_npc(npc_id=NPC_SPRING, x=-199680, y=S1_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199200, y=S1_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199616, y=S1_LOWER - 32)
b.add_npc(npc_id=NPC_SPRING, x=-199456, y=S1_MID - 32)

# 金币
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=-199744 + dx, y=S1_LOWER - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=-199264 + dx, y=S1_LOWER - 64)
for dx in [0, 32, 64, 96]:
    b.add_npc(npc_id=NPC_COIN, x=-199584 + dx, y=S1_MID - 64)
for dx in [0, 32, 64]:
    b.add_npc(npc_id=NPC_COIN, x=-199520 + dx, y=S1_HIGH - 64)
b.add_npc(npc_id=NPC_COIN, x=-199360, y=S1_GROUND - 64)
b.add_npc(npc_id=NPC_COIN, x=-199360, y=S1_GROUND - 128)

# 敌人
b.add_npc(npc_id=NPC_GOOMBA, x=-199552, y=S1_GROUND - 32, facing=-1)
b.add_npc(npc_id=NPC_GOOMBA, x=-199104, y=S1_GROUND - 32, facing=1)
b.add_npc(npc_id=NPC_GOOMBA, x=-198672, y=S1_GROUND - 32, facing=-1)

# BGO 装饰
b.add_bgo(bgo_id=BGO_BUSH, x=-199936, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=-199872, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_BUSH, x=-198528, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=-198464, y=S1_GROUND)
b.add_bgo(bgo_id=BGO_FLOWER, x=-199040, y=S1_GROUND)

# ═══════════════════════════════════════════
# Section 2 — Boss 竞技场地形
# ═══════════════════════════════════════════

# 完整石砖地面
for x in range(S2_X, S2_RIGHT, 32):
    b.add_block(blk_id=BLK_STONE, x=x, y=S2_GROUND)

# 左右墙壁（防止跑出竞技场）
for y in range(S2_GROUND - 32, S2_TOP - 32, -32):
    b.add_block(blk_id=BLK_STONE, x=S2_X, y=y)
    b.add_block(blk_id=BLK_STONE, x=S2_RIGHT - 32, y=y)

# 顶部围墙
for x in range(S2_X, S2_RIGHT, 32):
    b.add_block(blk_id=BLK_STONE, x=x, y=S2_TOP)

# 左侧弹簧平台 (4 格宽)
for x in range(S2_X + 64, S2_X + 64 + 128, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S2_PLAT_Y)

# 右侧弹簧平台 (4 格宽)
for x in range(S2_RIGHT - 64 - 128, S2_RIGHT - 64, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S2_PLAT_Y)

# 中央高处小平台 (3 格宽)
for x in range(S2_X + S2_W // 2 - 48, S2_X + S2_W // 2 + 48, 32):
    b.add_block(blk_id=BLK_WOOD, x=x, y=S2_HIGH_Y)

# 弹簧（地面左右各一个）
b.add_npc(npc_id=NPC_SPRING, x=S2_X + 96, y=S2_GROUND - 32)
b.add_npc(npc_id=NPC_SPRING, x=S2_RIGHT - 96 - 32, y=S2_GROUND - 32)

# 中央平台上方的恢复蘑菇（隐藏图层 BossReward 中，Boss 死后显示）
b.add_block(blk_id=BLK_QUESTION, x=S2_X + S2_W // 2 - 16, y=S2_PLAT_Y,
            contain=1009, layer='BossReward')

# ─── Boss NPC ───
# Boom Boom (id=15)，放在竞技场中央，放在 Boss 图层上
b.add_npc(npc_id=NPC_BOSS, x=S2_X + S2_W // 2, y=S2_GROUND - 64,
          layer='Boss', friendly=0, nomove=0)

# ─── 传送门：Section 1 → Section 2 ───
# 入口在 Section 1 右侧地面，出口在 Section 2 左侧地面
b.add_warp(
    x=S1_X + S1_W - 64, y=S1_GROUND - 32,
    ex=S2_X + 64, ey=S2_GROUND - 32,
    layer='Default',
    type_=2,        # 门
    enter_dir=3,    # 从下方进入
    exit_dir=1,     # 从上方出来
)

# ═══════════════════════════════════════════
# 图层
# ═══════════════════════════════════════════
b.add_layer('Default', status=1)
b.add_layer('Destroyed Blocks', status=1)
b.add_layer('Spawned NPCs', status=1)
b.add_layer('Boss', status=1)           # Boss 所在图层
b.add_layer('BossReward', status=0)     # Boss 死后奖励（初始隐藏）

# ═══════════════════════════════════════════
# 变量
# ═══════════════════════════════════════════
b.add_variable('coinCount', value=0, scope=0)
b.add_variable('bossHP', value=0, scope=0)
b.add_variable('bossPhase', value=1, scope=0)
b.add_variable('bossTimer', value=0, scope=0)
b.add_variable('bossAlive', value=0, scope=0)
b.add_variable('summonCD', value=0, scope=0)
b.add_variable('bulletCD', value=0, scope=0)

# ═══════════════════════════════════════════
# 事件
# ═══════════════════════════════════════════
b.add_event('Level - Start', autostart=1, script_name='Welcome')
b.add_event('BossDefeated', autostart=0,
            show_layers=['BossReward'],
            hide_layers=['Boss'])

# ═══════════════════════════════════════════
# TeaScript 脚本
# ═══════════════════════════════════════════

# --- 欢迎脚本 ---
welcome_script = """\
' Welcome script for Spring Garden
call ShowMsg("Welcome to Spring Garden! Go right to find the Boss!")
"""

# --- Boss AI 主控脚本 ---
boss_script = """\
' ============================================================
'  Boss AI — 疯狂 Boom Boom
'  三阶段狂暴 Boss 战
' ============================================================

' 所有 dim 必须在 if 块外声明（patch 31 前的 bug）
dim bi as integer
dim bossIdx as integer
dim ni as integer
dim curHP as double
dim bx as double
dim px as double
dim chaseSpeed as double
dim summonInterval as double
dim spawnX as double
dim bulletInterval as double
dim dir as double

' 只在 Boss 首次出现时初始化
if v(bossAlive) = 0 then
    v(bossAlive) = 0
    v(bossHP) = 0
    v(bossPhase) = 1
    v(bossTimer) = 0
    v(summonCD) = 0
    v(bulletCD) = 0
    for bi = 1 to sysval(ncount)
        if NPC(bi).id = 15 then
            NPC(bi).health = 10
            v(bossAlive) = 1
            v(bossHP) = 10
        end if
    next
    call ShowMsg("BOSS: Boom Boom has appeared!")
end if

' ─── 主循环：每帧执行 ───
if v(bossAlive) = 1 then
    bossIdx = 0
    for ni = 1 to sysval(ncount)
        if NPC(ni).id = 15 then
            bossIdx = ni
        end if
    next

    if bossIdx = 0 then
        v(bossAlive) = 0
        call ShowMsg("BOSS DEFEATED! You are the champion!")
        call LSet("BossReward", 1, 0)
        call LSet("Boss", 2, 0)
    else
        ' ─── 更新 Boss HP ───
        curHP = NPC(bossIdx).health
        v(bossHP) = curHP

        ' ─── 阶段判定 ───
        if curHP > 5 then
            v(bossPhase) = 1
        elseif curHP > 2 then
            v(bossPhase) = 2
        else
            v(bossPhase) = 3
        end if

        ' ─── 追击玩家 ───
        bx = NPC(bossIdx).x
        px = char(1).x

        if v(bossPhase) = 1 then
            chaseSpeed = 1.5
        elseif v(bossPhase) = 2 then
            chaseSpeed = 2.5
        else
            chaseSpeed = 4.0
        end if

        if px > bx + 16 then
            NPC(bossIdx).xsp = chaseSpeed
        elseif px < bx - 16 then
            NPC(bossIdx).xsp = -chaseSpeed
        end if

        ' Phase 2+: Boss 随机跳跃
        if v(bossPhase) >= 2 then
            v(bossTimer) = v(bossTimer) + 1
            if v(bossTimer) > 90 then
                if rnd > 0.5 then
                    NPC(bossIdx).ysp = -7
                end if
                v(bossTimer) = 0
            end if
        end if

        ' Phase 3: Boss 疯狂弹跳
        if v(bossPhase) = 3 then
            if NPC(bossIdx).stand = -1 then
                if rnd > 0.85 then
                    NPC(bossIdx).ysp = -9
                end if
            end if
        end if

        ' ─── 召唤小怪 ───
        v(summonCD) = v(summonCD) + 1
        if v(bossPhase) = 1 then
            summonInterval = 300
        elseif v(bossPhase) = 2 then
            summonInterval = 180
        else
            summonInterval = 90
        end if

        if v(summonCD) >= summonInterval then
            v(summonCD) = 0
            spawnX = bx + (rnd - 0.5) * 200
            call NCreate(1, spawnX, NPC(bossIdx).y - 32, 0, 0, 0, 0)
            if v(bossPhase) >= 2 then
                call NCreate(29, spawnX + 64, NPC(bossIdx).y - 32, 0, 0, 0, 0)
            end if
            if v(bossPhase) = 3 then
                call NCreate(1, spawnX - 64, NPC(bossIdx).y - 32, 0, 0, 0, 0)
                call NCreate(1, spawnX + 128, NPC(bossIdx).y - 32, 0, 0, 0, 0)
            end if
        end if

        ' ─── 弹幕射击 (Phase 2+) ───
        if v(bossPhase) >= 2 then
            v(bulletCD) = v(bulletCD) + 1
            if v(bossPhase) = 2 then
                bulletInterval = 45
            else
                bulletInterval = 20
            end if

            if v(bulletCD) >= bulletInterval then
                v(bulletCD) = 0
                if px > bx then
                    dir = 4
                else
                    dir = -4
                end if
                call NCreate(276, bx, NPC(bossIdx).y - 16, dir, -2, 0, 0)

                if v(bossPhase) = 3 then
                    call NCreate(276, bx, NPC(bossIdx).y - 32, dir * 0.7, -4, 0, 0)
                    call NCreate(276, bx, NPC(bossIdx).y, dir * 1.3, -1, 0, 0)
                end if
            end if
        end if

        ' ─── Phase 3 视觉效果：Boss 闪烁红光 ───
        if v(bossPhase) = 3 then
            if sysval(gametime) mod 8 < 4 then
                NPC(bossIdx).forecolor = rgba(255, 0, 0, 200)
            else
                NPC(bossIdx).forecolor = -1
            end if
        else
            NPC(bossIdx).forecolor = -1
        end if
    end if
end if
"""

b.add_script('Welcome', welcome_script)
b.add_script('BossAI', boss_script)

# ─── Boss AI 需要绑定到 Level - Start 以外的事件 ───
# Boss AI 通过每帧事件触发
b.add_event('BossTick', autostart=1, script_name='BossAI')

# ─── 保存 ───
out_path = os.path.join(HERE, 'SpringGarden.lvl')
b.save(out_path)
print(f'Level saved to: {out_path}')
