# SMBX-38A File Formats Specification

> Source: `smbx-38A File specifications (LVL WLD WLS).pdf`
> Developed by Chinese developer **5438A38A** for use in re-developed SMBX 1.4.x
> (Unofficial implementation of SMBX Engine)

---

## General Notes

- All files are written as **ASCII text**.
- Every header contains a line `SMBXFile??`, where `??` is the version number of the file generator standard (first version `65`, latest `66`).
- Non-ASCII data is encoded with **URI** and **BASE64** formats.
- Every line begins with a marker indicating the element type, followed by parameters in strict order.
- Parameters are separated with `|`.
- Sub-parameters (extra parameters or array elements within a parent parameter cell) are split with `/` or `,`.
- Extra parameters are allowed at the end of every line. They may be **appended** to the end of any parameter chain, but **replacing or inserting** into the middle is not allowed.
- Extra-type entries are also allowed, but they must not use already-used markers.

> **Note:** entries highlighted as "Red entries" in the original PDF were introduced in updated **SMBX66-38A**. They are preserved here verbatim — refer to the original PDF for the visual marking.

---

# 1. LVL File Specification

## 1.1 Data Type Markers

| Marker | Description |
| --- | --- |
| `A` | Level header settings |
| `P1`, `P2` | Player spawn points |
| `M` | Section settings |
| `B` | Blocks |
| `T` | Background objects |
| `N` | Non-playable characters (NPCs) |
| `Q` | Liquid / Environment boxes |
| `W` | Warp entries |
| `L` | Layers |
| `E` | Events |
| `V` | Local level variables |
| `S` | UTF-8 encoded local level scripts |
| `Su` | ASCII-encoded local level scripts |

## 1.2 File Header (line 1)

```
SMBXFile??
```

- `??` = version number

## 1.3 Level Settings — `A`

```
A|param1|param2[|param3|param4]
```

`[]` denotes optional fields.

| Field | Description |
| --- | --- |
| `param1` | Number of stars on this level |
| `param2` | Level title |
| `param3` | Filename — when player dies, the player is sent to this level |
| `param4` | Normal entrance / target warp `[0..WARPMAX]` |

## 1.4 Player Start Points — `P1`, `P2`

```
P1|x1|y1
P2|x2|y2
```

| Field | Description |
| --- | --- |
| `x1`, `y1` | First player position (x, y) |
| `x2`, `y2` | Second player position (x, y) |

## 1.5 Section Properties — `M`

```
M|id|x|y|w|h|b1|b2|b3|b4|b5|b6|music|background|musicfile
```

| Field | Description |
| --- | --- |
| `id` | Section index `[1..SectionMAX]` |
| `x` | Left coordinate `[-left/+right]` |
| `y` | Top coordinate `[-down/+up]` |
| `w` | Section width (clamped: `if (w < 800) w = 800`) |
| `h` | Section height (clamped: `if (h < 600) h = 600`) |
| `b1` | Under water? `0=false`, `!0=true` |
| `b2` | Is x-level wrap? `0=false`, `!0=true` |
| `b3` | Enable off-screen exit? `0=false`, `!0=true` |
| `b4` | No turn back (X): `0=no x-scrolllock`, `1=scrolllock left`, `2=scrolllock right` |
| `b5` | No turn back (Y): `0=no y-scrolllock`, `1=scrolllock up`, `2=scrolllock down` |
| `b6` | Is y-level wrap? `0=false`, `!0=true` |
| `music` | Music number (same as SMBX 1.3) |
| `background` | Background number (same as filename in `background2` folder) |
| `musicfile` | Custom music file `[***urlencode!***]` |

## 1.6 Blocks — `B`

```
B|layer|id|x|y|contain|b1|b2|e1,e2,e3|w|h
```

| Field | Description |
| --- | --- |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `id` | Block ID |
| `x` | Block position X |
| `y` | Block position Y |
| `contain` | Containing NPC number: `[1001..1000+NPCMAX]` = npc-id; `[1..999]` = coin number; `[0]` = nothing |
| `b1` | Slippery? `0=false`, `!0=true` |
| `b2` | Invisible? `0=false`, `!0=true` |
| `e1` | Block destroy event name `[***urlencode!***]` |
| `e2` | Block hit event name `[***urlencode!***]` |
| `e3` | "No more object in layer" event name `[***urlencode!***]` |
| `w` | Width |
| `h` | Height |

## 1.7 Background Objects — `T`

```
T|layer|id|x|y
```

| Field | Description |
| --- | --- |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `id` | Background ID |
| `x` | Background position X |
| `y` | Background position Y |

## 1.8 NPCs — `N`

```
N|layer|id|x|y|b1,b2,b3,b4|sp|e1,e2,e3,e4,e5,e6,e7|a1,a2|c1[,c2,c3,c4,c5,c6,c7]|msg|
```

| Field | Description |
| --- | --- |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `id` | NPC ID |
| `x` | NPC position X |
| `y` | NPC position Y |
| `b1` | `1` = left, `0` = random, `-1` = right |
| `b2` | Friendly NPC |
| `b3` | Don't move NPC |
| `b4` | `1=npc91`, `2=npc96`, `3=npc283`, `4=npc284`, `5=npc300` |
| `sp` | Special option `[***urlencode!***]` |
| `e1` | Death event |
| `e2` | Talk event |
| `e3` | Activate event |
| `e4` | "No more object in layer" event |
| `e5` | Grabbed event |
| `e6` | Next-frame event |
| `e7` | Touch event |
| `a1` | Layer name to attach |
| `a2` | Variable name to send |
| `c1` | Generator enable |
| `c2` | (if `c1 != 0`) Generator period `[1 frame]` |
| `c3` | Generator effect (see formula below) |
| `c4` | Generator direction angle (when `c3 == 0`) |
| `c5` | Batch (when `c3 == 0`, MAX = 32) |
| `c6` | Angle range (when `c3 == 0`) |
| `c7` | Speed (when `c3 == 0`, float) |
| `msg` | NPC talkative message `[***urlencode!***]` |

### Generator effect (`c3`) encoding

```
c3-1: 1=warp, 0=projective, 4=no effect
c3-2: 0=center, 1=up, 2=left, 3=down, 4=right,
      9=up+left, 10=left+down, 11=down+right, 12=right+up

if (c3-2) != 0
    c3 = 4 * (c3-1) + (c3-2)
else
    c3 = 0
```

## 1.9 Liquid / Environment Boxes — `Q`

```
Q|layer|x|y|w|h|b1,b2,b3,b4,b5|event
```

| Field | Description |
| --- | --- |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `x` | Position X |
| `y` | Position Y |
| `w` | Width |
| `h` | Height |
| `b1` | Liquid type (see table below) |
| `b2` | Friction |
| `b3` | Acceleration direction |
| `b4` | Acceleration |
| `b5` | Maximum velocity |
| `event` | Touch event |

### Liquid types (`b1`)

| Value | Type |
| --- | --- |
| 01 | Water (friction = 0.5) |
| 02 | Quicksand (friction = 0.1) |
| 03 | Custom Water |
| 04 | Gravitational Field |
| 05 | Event Once |
| 06 | Event Always |
| 07 | NPC Event Once |
| 08 | NPC Event Always |
| 09 | Click Event |
| 10 | Collision Script |
| 11 | Click Script |
| 12 | Collision Event |
| 13 | Air |

## 1.10 Warps — `W`

```
W|layer|x|y|ex|ey|type|enterd|exitd|sn,msg,hide|locked,noyoshi,canpick,bomb,hidef,anpc,mini,size|lik|liid|noexit|wx|wy|le|we
```

| Field | Description |
| --- | --- |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `x` | Entrance position X |
| `y` | Entrance position Y |
| `ex` | Exit position X |
| `ey` | Exit position Y |
| `type` | `1=pipe`, `2=door`, `0=instant` |
| `enterd` | Entrance direction: `1=up`, `2=left`, `3=down`, `4=right` |
| `exitd` | Exit direction: `1=up`, `2=left`, `3=down`, `4=right` |
| `sn` | Stars required for entry |
| `msg` | Message when stars are insufficient |
| `hide` | Hide the star number for this warp |
| `locked` | Locked |
| `noyoshi` | No Yoshi |
| `canpick` | Allow NPC |
| `bomb` | Need a bomb |
| `hidef` | Hide the entry scene |
| `anpc` | Allow NPC inter-level |
| `mini` | Mini-Only |
| `size` | Warp size (pixels) |
| `lik` | Warp to level filename `[***urlencode!***]` |
| `liid` | Normal entrance / target warp `[0..WARPMAX]` |
| `noexit` | Level entrance |
| `wx` | Warp to X on world map |
| `wy` | Warp to Y on world map |
| `le` | Level exit |
| `we` | Warp event `[***urlencode!***]` |

## 1.11 Layers — `L`

```
L|name|status
```

| Field | Description |
| --- | --- |
| `name` | Layer name `[***urlencode!***]` |
| `status` | Is the layer visible |

## 1.12 Events — `E`

```
E|name|msg|ea|el|elm|epy|eps|eef|ecn|evc|ene
```

| Field | Description |
| --- | --- |
| `name` | Event name `[***urlencode!***]` |
| `msg` | Show message after event start `[***urlencode!***]` |
| `ea` | Auto-start config: `val,syntax` |
| `el` | Layer toggles |
| `elm` | Layer movement commands |
| `epy` | Player control flags |
| `eps` | Section / background / music changes |
| `eef` | Effects |
| `ecn` | NPCs to spawn |
| `evc` | Variable changes |
| `ene` | Trigger / timer / API event / script |

### `ea` — Auto-start

```
ea = val,syntax
```

| Value | Meaning |
| --- | --- |
| `val=0` | Not auto-start |
| `val=1` | Auto-start when level starts |
| `val=2` | Auto-start when all conditions match |
| `val=3` | Start when called and all conditions match |
| `syntax` | Condition expression `[***urlencode!***]` |

### `el` — Layer show/hide/toggle

```
el = b/s1,s2...sn/h1,h2...hn/t1,t2...tn
```

| Field | Description |
| --- | --- |
| `b` | No smoke (`0=false`, `!0=true`) `[***urlencode!***]` |
| `s(n)` | Layers to show |
| `l(n)` | Layers to hide |
| `t(n)` | Layers to toggle |

### `elm` — Layer movement

```
elm = elm1/elm2.../elmn
elm(n) = layername,horizontal_syntax,vertical_syntax,way
```

| Field | Description |
| --- | --- |
| `layername` | Layer name for movement `[***urlencode!***]` |
| `horizontal syntax` | `[***urlencode!***][syntax]` |
| `vertical syntax` | `[***urlencode!***][syntax]` |
| `way` | `0=by speed`, `1=by coordinate` |

### `epy` — Player controls

```
epy = b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12
```

| Field | Description |
| --- | --- |
| `b1` | Enable player controls |
| `b2` | Drop |
| `b3` | Alt run |
| `b4` | Run |
| `b5` | Jump |
| `b6` | Alt jump |
| `b7` | Up |
| `b8` | Down |
| `b9` | Left |
| `b10` | Right |
| `b11` | Start |
| `b12` | Lock keyboard |

### `eps` — Section / background / music edits

```
eps = esection/ebackground/emusic
esection    = es1:es2...esn
ebackground = eb1:eb2...ebn
emusic      = em1:em2...emn
```

#### `es` — Section edit

```
es = id,stype,x,y,w,h,auto,sx,sy
```

| Field | Description |
| --- | --- |
| `id` | Section ID |
| `stype` | `0=don't change`, `1=default`, `2=custom` |
| `x` | Left X for section `id` `[***urlencode!***][syntax]` |
| `y` | Top Y for section `id` `[***urlencode!***][syntax]` |
| `w` | Width for section `id` `[***urlencode!***][syntax]` |
| `h` | Height for section `id` `[***urlencode!***][syntax]` |
| `auto` | Enable autoscroll controls (`0=false`, `!0=true`) |
| `sx` | Move screen horizontal syntax `[***urlencode!***][syntax]` |
| `sy` | Move screen vertical syntax `[***urlencode!***][syntax]` |

#### `eb` — Background edit

```
eb = id,btype,backgroundid
```

| Field | Description |
| --- | --- |
| `id` | Section ID |
| `btype` | `0=don't change`, `1=default`, `2=custom` |
| `backgroundid` | Custom background ID (when `btype=2`) |

#### `em` — Music edit

```
em = id,mtype,musicid,customfile
```

| Field | Description |
| --- | --- |
| `id` | Section ID |
| `mtype` | `0=don't change`, `1=default`, `2=custom` |
| `musicid` | Custom music ID (when `mtype=2`) |
| `customfile` | Custom music filename (when `mtype=3`) `[***urlencode!***]` |

### `eef` — Effects

```
eef = sound/endgame/ce1/ce2.../cen
```

| Field | Description |
| --- | --- |
| `sound` | Play sound number |
| `endgame` | `0=none`, `1=bowser defeat` |
| `ce(n)` | Effect entry: `id,x,y,sx,sy,grv,fsp,life` |

#### `ce(n)` — Effect entry

| Field | Description |
| --- | --- |
| `id` | Effect ID |
| `x` | Effect position X `[***urlencode!***][syntax]` |
| `y` | Effect position Y `[***urlencode!***][syntax]` |
| `sx` | Effect horizontal speed `[***urlencode!***][syntax]` |
| `sy` | Effect vertical speed `[***urlencode!***][syntax]` |
| `grv` | Affected by gravity? (`0=false`, `!0=true`) |
| `fsp` | Frame speed of generated effect |
| `life` | Effect destroyed after this lifetime |

### `ecn` — NPCs to spawn

```
ecn = cn1/cn2.../cnn
cn(n) = id,x,y,sx,sy,sp
```

| Field | Description |
| --- | --- |
| `id` | NPC ID |
| `x` | NPC position X `[***urlencode!***][syntax]` |
| `y` | NPC position Y `[***urlencode!***][syntax]` |
| `sx` | NPC horizontal speed `[***urlencode!***][syntax]` |
| `sy` | NPC vertical speed `[***urlencode!***][syntax]` |
| `sp` | Advanced settings of generated NPC |

### `evc` — Variable changes

```
evc = vc1/vc2.../vcn
vc(n) = name,newvalue
```

| Field | Description |
| --- | --- |
| `name` | Variable name `[***urlencode!***]` |
| `newvalue` | New value `[***urlencode!***][syntax]` |

### `ene` — Next-event / timer / API event / script

```
ene = nextevent/timer/apievent/scriptname
```

#### `nextevent`

```
nextevent = name,delay
```

| Field | Description |
| --- | --- |
| `name` | Trigger event name `[***urlencode!***]` |
| `delay` | Trigger delay `[1 frame]` |

#### `timer`

```
timer = enable,count,interval,type,show
```

| Field | Description |
| --- | --- |
| `enable` | Enable game timer (`0=false`, `!0=true`) |
| `count` | Time left of the game timer |
| `interval` | Time count interval |
| `type` | `0=counting down`, `1=counting up` |
| `show` | Show timer in HUD? (`0=false`, `!0=true`) |

#### `apievent` / `scriptname`

| Field | Description |
| --- | --- |
| `apievent` | The ID of the API event |
| `scriptname` | Script name `[***urlencode!***]` |

## 1.13 Variables — `V`

```
V|name|value
```

| Field | Description |
| --- | --- |
| `name` | Variable name `[***urlencode!***]` |
| `value` | Initial value of the variable |

## 1.14 Scripts — `S`, `Su`

```
S|name|script
Su|name|scriptu
```

| Field | Description |
| --- | --- |
| `name` | Script name `[***urlencode!***]` |
| `script` | Script body `[***base64encode!***][utf-8]` |
| `scriptu` | Script body `[***base64encode!***][ASCII]` |

---

# 2. WLD File Specification

## 2.1 Data Type Markers

| Marker | Description |
| --- | --- |
| `ws1` | World settings header |
| `ws2` | Credits |
| `ws3` | List of additional strings |
| `ws4` | Saving locker setup |
| `T` | Terrain tiles |
| `S` | Sceneries |
| `P` | Paths |
| `M` | Areas — Music boxes, viewports, etc. |
| `L` | Level entrances |
| `WL` | Layers |
| `WE` | Events |

## 2.2 File Header (line 1)

```
SMBXFile??
```

- `??` = version number

## 2.3 World Settings — `ws1` / `ws2` / `ws3` / `ws4`

```
ws1|wn|bp1,bp2,bp3,bp4,bp5|asn|dtp,nwm,rsd,dcp,sc,sm,asg,smb3|sn,mis|acm|sc
ws2|credits
ws3|list
ws4|se|msg
```

### `ws1` — Header

| Field | Description |
| --- | --- |
| `wn` | Episode name `[***urlencode!***]` |
| `bp(n)` | Don't use player `n` as player's character |
| `asn` | Auto-start level filename `[***urlencode!***]` |
| `dtp` | Disable two-player (`0=false`, `!0=true`) |
| `nwm` | No world map (`0=false`, `!0=true`) |
| `rsd` | Restart last level on player's death (`0=false`, `!0=true`) |
| `dcp` | Disable change player (`0=false`, `!0=true`) |
| `sc` (in 4th group) | Save machine code to `.sav` file (`0=false`, `!0=true`) |
| `sm` | Save mode (see below) |
| `asg` | Auto save game (`0=false`, `!0=true`) |
| `smb3` | SMB3 style world map (`0=false`, `!0=true`) |
| `sn` | Star number |
| `mis` | Max item number in world inventory |
| `acm` | Anti-cheat mode (`0=don't allow in list`, `!0=allow in list`) |
| `sc` (last) | Enable save locker (`0=false`, `!0=true`) |

#### `sm` — Save mode values

| Value | Meaning |
| --- | --- |
| `-1` | Restart at auto-start level |
| `0` | Restart at the world map where we saved last time |
| `1` | Restart at the level where we saved last time |

### `ws2` — Credits

```
[1] #DEFT#xxxxxx[***base64encode!***]
    xxxxxx = name1 /n name2 /n ...
[2] #CUST#xxxxxx[***base64encode!***]
    xxxxxx = any string
```

### `ws3` — Additional strings list

```
list = xxxxxx[***base64encode!***]
xxxxxx = string1,string2...stringn
```

### `ws4` — Save locker

| Field | Description |
| --- | --- |
| `se` | Save locker syntax `[***urlencode!***][syntax]` |
| `msg` | Message when save was locked `[***urlencode!***]` |

## 2.4 Tiles — `T`

```
T|id|x|y|layer
```

| Field | Description |
| --- | --- |
| `id` | Tile ID |
| `x` | Tile position X |
| `y` | Tile position Y |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |

## 2.5 Sceneries — `S`

```
S|id|x|y|layer
```

| Field | Description |
| --- | --- |
| `id` | Scenery ID |
| `x` | Scenery position X |
| `y` | Scenery position Y |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |

## 2.6 Paths — `P`

```
P|id|x|y|layer
```

| Field | Description |
| --- | --- |
| `id` | Path ID |
| `x` | Path position X |
| `y` | Path position Y |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |

## 2.7 Areas — `M`

```
M|id|x|y|name|layer|w|h|flag|te,eflag|ie1,ie2,ie3
```

| Field | Description |
| --- | --- |
| `id` | Music ID |
| `x` | Area position X |
| `y` | Area position Y |
| `name` | Custom music name `[***urlencode!***]` |
| `layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `w` | Width |
| `h` | Height |
| `flag` | Area settings (bitwise: `0=False`, `!0=True`) |
| `te` | Touch event `[***urlencode!***]` |
| `eflag` | Touch trigger mode (see below) |
| `ie1` | Hammer Event `[***urlencode!***]` |
| `ie2` | Warp Whistle Event `[***urlencode!***]` |
| `ie3` | Anchor Event `[***urlencode!***]` |

### `flag` — Area settings (bitwise)

| Bit | Meaning |
| --- | --- |
| `b1 = (flag & 1)` | World Music |
| `b2 = (flag & 2)` | Set Viewport |
| `b3 = (flag & 4)` | Ship Route |
| `b4 = (flag & 8)` | Forced Walking |
| `b5 = (flag & 16)` | Item-triggered events |

### `eflag` — Touch trigger mode

| Value | Meaning |
| --- | --- |
| `0` | Triggered every time entering |
| `1` | Triggered on entrance and level completion |
| `2` | Triggered only once |

## 2.8 Levels — `L`

```
L|id|x|y|fn|n|eu\el\ed\er|wx|wy|wlz|bg,pb,av,ls,f,nsc,otl,li,lcm|s|Layer|Lmt
```

| Field | Description |
| --- | --- |
| `id` | Level ID |
| `x` | Level position X |
| `y` | Level position Y |
| `fn` | Level filename `[***urlencode!***]` |
| `n` | Level name `[***urlencode!***]` |
| `eu`, `el`, `ed`, `er` | Exits for up/left/down/right |
| `wx` | Go to world-map position X |
| `wy` | Go to world-map position Y |
| `wlz` | Number of doors to warp |
| `bg` | Big background |
| `pb` | Path background |
| `av` | Always visible |
| `ls` | Is game start point |
| `f` | Forced |
| `nsc` | No star coin count |
| `otl` | Destroy after clear |
| `li` | Level ID |
| `lcm` | Affected by Music Box |
| `s` | Entrance syntax (see below) |
| `Layer` | Layer name (`""` = `"Default"`) `[***urlencode!***]` |
| `Lmt` | Level Movement Command (see below) |

### Exits `eu / el / ed / er`

```
e = c1,c2,c3,c4
exit = (c1 || c2 || c3) && c4
```

| Field | Description |
| --- | --- |
| `c1`, `c2`, `c3` | Level exit type |
| `c4` | Condition expression `[***urlencode!***][syntax]` |

### `s` — Entrance syntax

```
s = ds1/ds2.../dsn
ds = ds1,ds2[***urlencode!***][syntax]
```

| Field | Description |
| --- | --- |
| `ds1` | Condition expression |
| `ds2` | Index |

### `Lmt` — Level Movement Command

```
lmt = NodeInfo\PathInfo
NodeInfo = Node1:Node2:...:NodeN
Node     = x,y,chance
PathInfo = Path1:Path2:...:PathN
Path     = NodeID1,NodeID2
```

## 2.9 Layers — `WL`

```
WL|name|status
```

| Field | Description |
| --- | --- |
| `name` | Layer name `[***urlencode!***]` |
| `status` | Is the layer hidden |

## 2.10 Events — `WE`

```
WE|name|layer|layerm|world|other
```

| Field | Description |
| --- | --- |
| `name` | Event name `[***urlencode!***]` |
| `layer` | Layer toggles: `way/hidelist/showlist/togglelist` |
| `layerm` | Layer movement commands |
| `world` | World event config |
| `other` | Sound / lock / next-event / script / message / warp whistle |

### `layer` — Layer toggles

```
layer = way/hidelist/showlist/togglelist
list  = name1,name2,name3...namen
name [***urlencode!***]
```

```
if (way % 10 == 1) nosmoke = true;
if (way > 10)      object_state = true;
else               layer_state  = true;
```

### `layerm` — Layer movement

```
layerm = movementcommand1\movementcommand2\...\movementcommandn
movementcommand = way,layer,hp,vp,ap
```

| Field | Description |
| --- | --- |
| `way` | `0=speed`, `1=coordinate`, `2=moveto`, `4=spin` |
| `layer` | Layer name `[***urlencode!***]` |
| `hp` | Horizontal parameter `[***urlencode!***]` |
| `vp` | Vertical parameter `[***urlencode!***]` |
| `ap` | Additional parameter `[***urlencode!***]` |

### `world` — World event

```
world = aw/cs,le,inpc,msgc,syntax,msg
```

| Field | Description |
| --- | --- |
| `aw` | Auto-start setting (see below) |
| `cs` | Start when match all conditions (`0=false`, `!0=true`) |
| `le` | `0`=normal event, `1`=level enter/exit event |
| `inpc` | Interrupt the process if `false` returned |
| `msgc` | Show a message if `false` returned |
| `syntax` | Condition expression `[***urlencode!***]` |
| `msg` | Message `[***urlencode!***]` |

#### `aw` — Auto-start

| Value | Meaning |
| --- | --- |
| `0` | Not auto-start |
| `1` | Triggered on loading the world the first time |
| `2` | Triggered every time loading the world |
| `3` | Triggered on level exit |

### `other` — Misc settings

```
other = sd/ld/event,delay/script/msg/wwx,wwy,lockl
```

| Field | Description |
| --- | --- |
| `sd` | Play sound number |
| `ld` | Lock keyboard (frames) |
| `event` | Trigger event name `[***urlencode!***]` |
| `delay` | Trigger delay `[1 frame]` |
| `script` | Script name `[***urlencode!***]` |
| `msg` | Show message after event start `[***urlencode!***]` |
| `wwx` | Warp Whistle map warp X (see note) |
| `wwy` | Warp Whistle map warp Y (see note) |
| `lockl` | `[Level ID]` Affected by Anchor |

> Note: if `wwx == -1 && wwy == -1`, it means **not moving**.

---

# 3. WLS File Specification (World Settings)

## 3.1 Data Type Markers

| Marker | Description |
| --- | --- |
| `G` | Global variables |
| `GS` | Global script (UTF-8 encoded) |
| `GSu` | Global script (ASCII-encoded) |
| `CW` | Custom sounds entries (alternate implementation of `sounds.ini` from PGE / LunaLUA) |

## 3.2 File Header (line 1)

```
SMBXFile??
```

- `??` = version number

## 3.3 Global Variables — `G`

```
G|name|value
```

| Field | Description |
| --- | --- |
| `name` | Variable name `[***urlencode!***]` |
| `value` | Initial value of the variable |

## 3.4 Global Scripts — `GS`, `GSu`

```
GS|name|script
GSu|name|scriptu
```

| Field | Description |
| --- | --- |
| `name` | Script name `[***urlencode!***]` |
| `script` | Script `[***base64encode!***][utf-8]` |
| `scriptu` | Script `[***base64encode!***][ASCII]` |

## 3.5 Custom Sounds — `CW`

```
CW|cdata1|cdata2|...|cdatan
```

```
cdata = sound-id,sound-filename
```

| Field | Description |
| --- | --- |
| `sound-id` | Sound ID |
| `sound-filename` | Sound filename `[***urlencode!***]` |

---

## Appendix: Encoding conventions

- `[***urlencode!***]` — value is URL-encoded (percent-encoding).
- `[***base64encode!***]` — value is Base64-encoded.
- `[syntax]` — value is a TeaScript-style expression evaluated by the engine.
- `""` (empty string) is an alias of `"Default"` for layer names.
