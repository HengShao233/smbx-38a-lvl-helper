# 常用代码片段

## 1. 显示一个调试消息

```teascript
call sysshowmsg(sysval(coincount), sysval(score), 0)
' 或：
call showmsg("Hello World")
```

## 2. 在事件脚本里访问触发对象

例如 `NPC - Death` 事件脚本：

```teascript
dim idx as integer
idx = sysval(param1)
' 现在 NPC(idx) 是刚死的 NPC
NPC(idx).x = -9999    ' 把它移走（已经死了，象征意义）
```

## 3. 修改玩家状态

```teascript
char(1).id = 1            ' 切换为 Luigi (0=Mario 1=Luigi 2=Peach 3=Toad 4=Link)
char(1).status = 2        ' Power-up 等级
char(1).xsp = 0           ' 速度归零
char(1).x = char(1).x + 32
```

## 4. 计数器 + 阈值触发

```teascript
v(killCount) = v(killCount) + 1
if v(killCount) >= 10 then
    call SET("EventBossSpawn")
    v(killCount) = 0
end if
```

## 5. 安全的循环

```teascript
dim n as integer = 0
do
    n = n + 1
    if n >= 60 then exit do
    call sleep(1)        ' 必不可少：1 帧
loop
```

## 6. 迭代所有 NPC

```teascript
' 简化版（用 sysval 计数 + 索引）
dim i as integer
for i = 1 to sysval(ncount)
    if NPC(i).id = 1 then        ' 是 Goomba
        NPC(i).hp = 0
    end if
next
```

> 大型场景应改用 `ItrCreate` / `ItrNext` 迭代器避免性能问题，详见 `.docs/.teascript-docs/Iterators.md`。

## 7. 自定义函数 / 过程

```teascript
' --- 主体 ---
dim r as double
r = clamp(v(myVar), 0, 100)
v(myVar) = r

' --- 辅助函数（必须放最末尾） ---
script clamp(x as double, lo as double, hi as double, return double)
    if x < lo then return lo
    if x > hi then return hi
    return x
end script
```

## 8. 全局可见的函数

```teascript
export script lerp(a as double, b as double, t as double, return double)
    return a + (b - a) * t
end script
```

## 9. 受伤后做点事

事件名 `Player - GotHurt`：

```teascript
dim p as integer
p = sysval(param1)
char(p).status = 1                  ' 强制变小蘑
call audioset(2, 13, 0, "")        ' 播个音效
```

## 10. 切换图层显隐

事件 `el` 子字段更直观；但脚本里也可以：

```teascript
' 这种属于事件的 el 子字段功能；脚本里没有直接 API。
' 推荐：在 lvl 中用 E|name|...|el|... 字段表达。
' 或：用 SLT IPC 命令在调试时手动切（仅 testing 模式）。
```

## 11. 字符串拼接进消息

```teascript
v(coins) = sysval(coincount)
str(line) = "You have " & val(coins) & " coins!"
call showmsg(str(line))
```

## 12. 限制重复触发（防抖）

```teascript
if v(_lastTrigger) + 30 > sysval(gametime) then exit do
v(_lastTrigger) = sysval(gametime)
' ...do work
```

## 13. 每帧驱动（最关键的范式！）

38A **没有"每帧自动事件"**。任何"每帧执行"逻辑都必须自己写循环：

```teascript
' lvl 中: E|<auto-event-name>|...|...|...|...|...|0,/...|.../...|.../<scriptname>
' 用 autostart=1 的事件挂载本脚本，关卡开始时触发**一次**

' ===== 一次性初始化（dim 必须在 do 外） =====
dim i as integer
dim bossIdx as integer
v(myCounter) = 0

' ===== 每帧主循环 =====
do
    v(myCounter) = v(myCounter) + 1
    
    ' 找 Boss
    bossIdx = 0
    for i = 1 to sysval(ncount)
        if NPC(i).id = 168 then
            bossIdx = i
        end if
    next
    
    if bossIdx = 0 then
        exit do          ' 主控对象消失，退出主循环
    end if
    
    ' ... 业务逻辑 ...
    
    call sleep(1)        ' ⚠ 必不可少：每帧让出 1 帧，否则游戏冻结！
loop
```

**多个并行循环**：一个 lvl 只能有一个 `Level - Start`，所以多个长循环要挂在不同的 autostart=1 事件上：

```text
E|Level - Start | autostart=1 | scriptname=BossAI
E|HUDStart      | autostart=1 | scriptname=BossHUD
E|MusicStart    | autostart=1 | scriptname=MusicLoop
```

(LVLBuilder 写法)：
```python
b.add_event('Level - Start', autostart=1, script_name='BossAI')
b.add_event('HUDStart',      autostart=1, script_name='BossHUD')
b.add_event('MusicStart',    autostart=1, script_name='MusicLoop')
```

## 14. 用户数组（R 行 + redim + array）

⚠ 38A 用户数组必须在 lvl 的 **R 行** 声明（不是 V 行！）：

```
R|<urlencoded_arr1>|<urlencoded_arr2>|...
```

LVLBuilder 一键写法：
```python
b.add_array('echoX', 'echoY')        # 一行声明多个数组
```

脚本里使用：
```teascript
dim i as integer

' 必须先 redim 初始化 ——
'   第 1 个参数 0 = double 数组（目前只支持 0）
'   第 2 个参数是数组名（不带引号，直接写名字）
'   第 3 个参数是长度
call redim(0, echoX, 90)
call redim(0, echoY, 90)

' 写入：
array(echoX(0)) = char(1).x
array(echoY(0)) = char(1).y

' 读取：
v(myX) = array(echoX(5))

' 字符串数组：
' call redim(0, names, 10)
' strarray(names(0)) = "Mario"
' str(out) = strarray(names(0))

' 环形 buffer 范例（每帧覆盖最旧元素）
v(head) = 0
do
    array(echoX(v(head))) = char(1).x
    array(echoY(v(head))) = char(1).y
    v(head) = v(head) + 1
    if v(head) >= 90 then
        v(head) = 0
    end if
    call sleep(1)
loop
```

## 15. NPC 类绑定脚本（每帧每实例 + sysval(param1) + with）

绑在 NPC type 上的脚本，由 `<lvl同名目录>/npc-<id>.txt` 中的 `scripts=<name>` 注册。
**引擎已经替你每帧调一次 + 每实例独立调用**，所以脚本主体**是一段瞬时逻辑，不要写 do/loop**。

```teascript
' 类绑定到 NPC 13；这个脚本每帧、每个 NPC 13 实例都会跑一次
' 注意：没有"隐式 with"，访问自身必须显式取索引

dim selfIdx as integer
selfIdx = sysval(param1)        ' NextFrame NPC 事件: param1 = 当前 NPC 的 ID

with NPC(selfIdx)
    ' with 块内可以用 leading-dot 访问自身字段
    if .y > -180000 then
        .alive = 0              ' 出屏即销毁
    end if
    .xsp = .xsp * 0.99          ' 慢慢减速
end with

' 也可不用 with，直接 NPC(selfIdx).field：
' NPC(selfIdx).xsp = NPC(selfIdx).xsp * 0.99
```

LVLBuilder 一站式注册（嵌脚本 + 写 sidecar）：

```python
b.add_npc_class_script(
    npc_id=13, script_name='FireBall',
    script_body=open('FireBall.tea').read(),
    gfxwidth=26, gfxheight=46     # 任何 npc-N.txt 配置键值都能传
)
```

更多 NPC 事件（同样 `sysval(param1)` 取自身索引）：
- `nextframeevent` (= `npc-N.txt scripts=`) — 每帧每实例
- `touchevent` — 玩家碰到时；param2=玩家ID, param3=碰撞方向
- `deathevent` — 死亡时
- `activeevent` — 首次出屏激活时
- `talkevent` / `grabedevent` — 对话 / 抓取


