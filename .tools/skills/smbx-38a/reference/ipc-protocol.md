# SMBX 38A IPC 协议速查

> 权威源：`.docs/.smbx38a-docs/Engine IPC Interface/Cpp-Example/command.txt`
> 仅在 **level testing 模式**（`smbx.exe filepath mode p1 p2 args` 启动）下可用。

## 共享内存布局

- 文件映射名：`smbx_memory_block`（`OpenFileMapping`）
- 总大小：`16384` 字节，分为两块 `8192` 字节缓冲：

```
struct ShareBlock {
    unsigned char BufferA[8192];  // 引擎 -> 客户端（你只能读）
    unsigned char BufferB[8192];  // 客户端 -> 引擎（你只能写）
};

每个 Buffer:
    short  Length;       // 命令长度（字节）
    char   Data[8190];   // 实际命令字节，ASCII，多条用 '\n' 分隔
```

- **读**：从 `BufferA` 读出 `Length` 字节后，**必须把 `BufferA.Length` 清零**。
- **写**：写入 `BufferB.Length + Data`，引擎处理后会把 `BufferB.Length` 清零。
- 多条命令以 `\n` 串接。
- 线程安全：本 skill 的 Python 客户端用 ~15ms 轮询。

## 启动参数（让引擎进入 testing 模式）

```
smbx.exe <filepath> <mode> <p1> <p2> <args>
```
- `mode`：0=单人, 1=双人, 2=对战
- `p1/p2`：玩家角色 id（0=Mario, 1=Luigi, 2=Peach, 3=Toad, 4=Link）
- `args`（URL 编码）：`SMBXArgs|hp,co,sr|p1p,p1i,p2p,p2i|levelname,cppid,cpidn`

## 命令清单

### 创建对象（编辑器场景）

```
CB|<Block Data>     # 创建 Block，数据格式同 LVL 的 B 行（去掉 marker）
CT|<BGO Data>       # 创建 BGO
CN|<NPC Data>       # 创建 NPC
```

### 当前光标对象

```
GB                  # 请求；引擎回复其中之一：
GB|NULL
GB|ERASER
GB|CURSOR
GB|B|<Block Data>
GB|T|<BGO Data>
GB|N|<NPC Data>
```

### 编辑器光标控制

```
SO                  # 关闭编辑模式
SO|CURSOR           # 切到 Cursor
SO|ERASER           # 切到 Eraser
SO|B|<Block Data>   # 进入"放置 Block"模式
SO|T|<BGO Data>
SO|N|<NPC Data>
```

### 图层 / 事件 / 消息

```
SLT|<layer>|<type>|<nosmoke>
    type: 1=Show, 2=Hide, 3=Toggle
    nosmoke: 0=有烟雾, !0=无烟雾
    layer 名 [URL 编码]

SET|<eventName>     # 触发事件
TMG|<msg>           # 显示一个 message box（msg URL 编码）
```

### 玩家

```
PM|<idn>|<pid>|<pr>
    idn: 1=P1, 2=P2
    pid: 0=Mario 1=Luigi 2=Peach 3=Toad 4=Link
    pr : 强化等级
```

### 查询游戏状态（GGI 系列）

```
GGI|PI                              -> GGI|PIT|d1|pid1|pr1[|d2|pid2|pr2]
GGI|ON                              -> GGI|ON|*Block|*BGO|*NPC|*Warp|*Liquid
GGI|LN                              -> GGI|LN|*Layer|*Event
GGI|CP                              -> GGI|CP|x|y         (cursor)
GGI|VP                              -> GGI|VP|x|y[|x2|y2] (camera)
GGI|VV|<varName>                    -> GGI|VV|name|id|val|stringVal
GGI|SS                              # 切换"取对象时是否回包"开关（默认 TRUE）
GGI|GM                              # 切换"游戏退出时是否回包"开关（默认 FALSE）
                                      退出消息：GGI|GM|exitcode|levelname,cid,id|hp,co,sr
GGI|SLN|<layerName>                 # 设置当前编辑图层
GGI|NOPAUSE                         # 窗口失焦不暂停
```

## 编码须知

- 所有命令是 **ASCII**，非 ASCII 字段（图层名、事件名、变量名、消息文本……）需 **URL 编码**。
- 字段分隔符 `|`；多命令分隔符 `\n`。

## 实务建议

1. **先 ping**：发 `GGI|ON`，若 ~200ms 内收到 `GGI|ON|...` 即视为 IPC 健康。
2. **重载关卡**：本协议不直接支持 hot reload。实践方案：
   - 关闭当前进程：`taskkill /IM smbx.exe /F`，再以新 lvl 启动。
   - 或调用 `engine_control.py reload --lvl ...`（封装上述流程）。
3. **回归测试一段脚本**：
   - 离线 inject 修改后的脚本到 lvl
   - reload
   - 用 `SET|<EventName>` 触发该脚本对应事件
   - `GGI|VV|<watchVar>` 查询脚本写入的变量
   - `screenshot.py` 抓窗口图像比对
