# SMBX 38A NPC List

> 共 **287** 个 NPC 条目。
> 数据源自 SMBX 38A 官方文档 PDF，自动提取并整理为 Markdown。

## 精简属性速查表

| NPC # | NPC Name | NPC type | Is Scenery | hurt to player | NPC Collision | Player Collision | Player Collision top | Block Collision | Gravity enabled | Can be take | Kill On HeadJump | On Jump/take | Kill by shell | Kill on fireball | Freezable by iceball |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 2 | Red Goomna | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 3 | Para Goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 4 | Green Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 5 | Green Koopa's shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV | ✓ | ✓ | ✓ |
| 6 | Red Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 7 | Red Koopa's shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV | ✓ | ✓ | ✓ |
| 8 | Green Piranha plant | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 9 | Mushroom | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | ✓ | ✓ | ✓ |
| 10 | Gold Coin | Bonus | - | - | - | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 11 | Random exit bonus | Exit  | - | - | - | - | - | ✓ | - | ✓ | - | End | - | - | - |
| 12 | Podoboo | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | - | ✓ |
| 13 | Fireball (player) | Bult | - | - | ✓ | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 14 | Fire flower | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 15 | Boom-boom | Boss | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | - | - |
| 16 | Mistary Ball | Exit  | - | - | ✓ | - | - | ✓ | - | ✓ | - | End | - | - | - |
| 17 | Bullet Bill | Enemy | - | ✓ | - | - | - | - | - | - | ✓ | Kill | ✓ | - | ✓ |
| 18 | Banzai Bill | Enemy | - | ✓ | - | - | - | - | - | - | ✓ | Kill | ✓ | - | - |
| 19 | Shy-Guy Red | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 20 | Shy-Guy Blue | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 21 | Bill Blaster | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 22 | Billy Gun | Carry | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 23 | Buzzy beetle | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | - | ✓ |
| 24 | Buzzy's shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV | ✓ | - | ✓ |
| 25 | Violet Ninja | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 26 | Springboard | Carry | - | - | - | - | ✓ | ✓ | ✓ | - | - | Bnc | - | - | - |
| 27 | Blue goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 28 | Red Cheep | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 29 | Hammer bros. | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 30 | Hammer | Bult | - | ✓ | - | - | - | - | ✓ | - | - | - | - | - | - |
| 31 | Big key | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 32 | Blue P switch | Button | - | - | ✓ | ✓ | - | ✓ | ✓ | - | ✓ | PBlk | - | - | - |
| 33 | Yellow coin | Bonus | - | - | - | - | - | ✓ | - | - | - | Take | - | - | - |
| 34 | Racoon leaf | Power | - | - | - | - | - | - | ✓ | ✓ | - | Take | - | - | - |
| 35 | Kuribo's shoe | Trans | - | - | ✓ | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 36 | Spiny | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 37 | Thwomp | Enemy | - | ✓ | ✓ | - | - | ✓ | - | - | - | Hurt | ✓ | - | - |
| 38 | Boo | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | - | - |
| 39 | Birdo | Enemy | - | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | - | - | ✓ | - | - |
| 40 | Birdo's egg | Bult | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | ✓ | - | - |
| 41 | Crystal sphere | Exit  | - | - | ✓ | - | - | ✓ | - | ✓ | - | End | - | - | - |
| 42 | Eerie (Dino ghost) | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | - | - |
| 43 | Boo | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | - | - |
| 44 | Big Boo | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | - | - |
| 45 | Ice Block (Grabbable) | Carry | - | - | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - | - |
| 46 | Red donut block | Mass  | - | - | ✓ | ✓ | ✓ | - | - | - | - | Grav | - | - | - |
| 47 | Lakitu (SMB3) | Enemy | - | ✓ | - | - | - | - | - | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 48 | Lakitu's ball | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 49 | Toothie Pipe | Carry | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 50 | Toothie | Enemy | - | ✓ | - | - | - | - | - | - | - | - | - | - | - |
| 51 | Turned Red Piranha Plant | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | ✓ |
| 52 | Horisontal Red Piranha Plant | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | ✓ |
| 54 | Fighter Fly | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 55 | Blue Beach Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 56 | Clown car | Trans | - | - | - | - | ✓ | ✓ | - | - | - | Mnt | - | - | - |
| 57 | Conveyor | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - | - |
| 58 | Iron Curbstone | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 59 | Yellow goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 60 | Yellow platform | Platf | - | - | - | - | ✓ | ✓ | ✓ | - | - | - | - | - | ✓ |
| 61 | Blue goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 62 | Blue platform | Platf | - | - | - | - | ✓ | ✓ | ✓ | - | - | - | - | - | ✓ |
| 63 | Green goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 64 | Green platform | Platf | - | - | - | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 65 | Red goomba | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 66 | Red platform | Platf | - | - | - | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 67 | Horisontal pipe x4 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 68 | Horisontal pipe x8 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 69 | Vertical pipe x4 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 70 | Vertical pipe x8 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 71 | Big goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 72 | Big green Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 73 | Big green Koopa's shell | Enemy | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV/- | ✓ | ✓ | ✓ |
| 74 | Big red piranha plant | Enemy | - | ✓ | - | - | - | - | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 75 | Jumping Toad | People | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 76 | Green Para-Koopa | Enemy | - | - | ✓ | - | - | ✓ | ✓ | - | - | Chg | - | ✓ | ✓ |
| 77 | Ninja | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 78 | Tractor caterpillars | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 79 | Wood block x2 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 80 | Wood block x4 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 81 | Wood block x4 2 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 82 | Wood block x4 3 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 83 | Wood block x8 | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 84 | Bowser's statue | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 85 | Bowser's statue's fire | Bult | - | ✓ | - | - | - | - | - | - | - | Hurt | - | - | - |
| 86 | Bowser (SMB-3) | Boss | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | - |
| 87 | Bowser's fire | Bult | - | ✓ | - | - | - | - | - | - | - | Hurt | - | - | - |
| 88 | Gold Coin | Bonus | - | - | - | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 89 | Goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 90 | 1up murshroom | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 91 | Herb (have contents) | Carry | - | - | - | - | ✓ | - | - | - | - | - | - | - | - |
| 92 | Vegatable — onions | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 93 | Piranha plant | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | - |
| 94 | Toad | People | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 95 | Green Yoshi | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 96 | Color eggs | Carry | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 97 | Star | Exit  | - | - | - | - | - | - | - | ✓ | - | End | - | - | - |
| 98 | Blue Yoshi | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 99 | Yellow Yoshi | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 100 | Red Yoshi | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 101 | Luigi | People | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 102 | Link | People | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 103 | Red coin | Bonus | - | - | - | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 104 | Wood platform (fall because mass) | Platf | - | - | - | - | ✓ | - | - | - | - | Grav | - | - | - |
| 105 | Thin platform | Mass  | - | - | - | - | ✓ | - | - | - | - | Enabl | - | - | - |
| 107 | Ping Bob-omb | People | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 108 | Yoshi's Fireball | Bult | - | - | - | - | - | - | ✓ | - | - | - | - | - | - |
| 109 | SMW green Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chang | ✓ | ✓ | ✓ |
| 110 | SMW red Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chang | ✓ | ✓ | ✓ |
| 111 | SMW blue Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chang | ✓ | ✓ | ✓ |
| 112 | SMW yellow Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chang | ✓ | ✓ | ✓ |
| 113 | SMW green shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV/- | ✓ | ✓ | ✓ |
| 114 | SMW red shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV/- | ✓ | ✓ | ✓ |
| 115 | SMW blue shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV/- | ✓ | ✓ | ✓ |
| 116 | SMW yellow shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV/- | ✓ | ✓ | ✓ |
| 117 | Green Beach Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 118 | Red Beach Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 119 | Blue Beach Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | Only  | ✓ | ✓ |
| 120 | Yellow Beach Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 121 | SMW green paraKoopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 122 | SMW red paraKoopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 123 | SMW blue paraKoopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 124 | SMW yellow paraKoopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 125 | Tinsuit (jackal) (LoZ) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 126 | Bot blue (LoZ) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 127 | Bot cyan (LoZ) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 128 | Bit (LoZ) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 129 | Twitter | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 130 | Red Snifit | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 131 | Blue Snifit | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 132 | Gray Snifit | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 133 | Snifit's bullet | Bult | - | ✓ | - | - | - | ✓ | ✓ | - | ✓ | Hurt | - | - | - |
| 134 | Mouser's Bomb | Carry | - | - | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | - | - |
| 135 | Bob-omb (SMB2) | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | ✓ | ✓ |
| 136 | Bob-omb (SMB3) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | - | ✓ |
| 137 | Bob-omb kicked (SMB3) | Carry | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 138 | Gold Coin | Bonus | - | - | - | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 139 | Vegetable onions glasses | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 140 | Vegetable turnip | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 141 | Vegetable radish 1 | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 142 | Vegetable green pumpkin | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 143 | Vegetable small carrots | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 144 | Vegetable radish 2 | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 145 | Vegetable radish 3 | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 146 | Vegetable big carrots | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 147 | Random vegetable | Carry | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 148 | Gray Yoshi | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 149 | Purpure Yoshi | People | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 150 | Pink Yoshi | People | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 151 | the «?» plate | People | - | - | - | - | - | ✓ | - | - | - | - | - | - | - |
| 152 | Gold ring | Bonus | - | - | - | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 153 | Poison mushroom | Bonus | - | ✓ | ✓ | - | - | ✓ | ✓ | ✓ | - | Take+ | - | - | - |
| 154 | Mushroom Block 1 | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 155 | Mushroom Block 2 | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 156 | Mushroom Block 3 | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 157 | Mushroom Block 4 | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 158 | Mr. Saturn | Carry | - | - | ✓ | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 160 | Jet wooden platform | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 161 | Red para-Koopa | Enemy | - | - | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 162 | Rex | Enemy | - | - | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 163 | Rex kicked | Enemy | - | - | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 164 | Mega mole | Enemy | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | - | ✓ |
| 165 | Galoomba (SMW) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 166 | Kicked Galoomba (SMW) | Carry | - | - | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | ✓ | ✓ |
| 167 | Para-Galoomba (SMW) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 168 | Bully (SM64) | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Thrw | ✓ | - | ✓ |
| 169 | Tanooki suit | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | ✓ |
| 170 | Hammer suit | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 171 | Hammer (player) | Bult | - | - | - | - | - | - | ✓ | - | - | - | - | - | - |
| 172 | Green shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV | ✓ | ✓ | ✓ |
| 173 | Green Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 174 | Red shell | Carry | - | Move | ✓ | - | - | ✓ | ✓ | - | - | MV | ✓ | ✓ | ✓ |
| 175 | Red Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 176 | Green Para-Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 177 | Red para-Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Chg | ✓ | ✓ | ✓ |
| 178 | Axe | Bonus | - | - | ✓ | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 179 | Circular saw | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | - | - | - |
| 180 | Thwomp | Enemy | - | ✓ | ✓ | - | - | ✓ | - | - | - | Hurt | ✓ | - | - |
| 181 | Bowser's statue | Scene | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 182 | Fire flower | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 183 | Fire flower | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 184 | Red mushroom | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 185 | Red mushroom | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 186 | Life murshroom | Bonus | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 187 | Life murshroom | Bonus | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 188 | Life moon | Bonus | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 189 | Dry Bones | Enemy | - | - | ✓ | - | - | ✓ | ✓ | - | - | Tempo | ✓ | - | ✓ |
| 190 | Skull lava platform | Platf | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | MV/- | - | - | - |
| 191 | Podoboo's shoe | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 192 | Check point | Exit  | - | - | - | - | - | ✓ | - | - | - | Take+ | - | - | - |
| 193 | Lakitu's shoe | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 194 | Kamikaze Koopa | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Throw | - | - | ✓ |
| 195 | Rainbow Shell | Carry | - | - | ✓ | - | - | ✓ | ✓ | - | - | MV | - | - | ✓ |
| 196 | Takeble Star | Speci | - | - | - | - | - | - | - | ✓ | - | Take | - | - | - |
| 197 | Exit point | Exit  | - | - | - | - | - | ✓ | - | ✓ | - | End | - | - | - |
| 198 | Peach | People | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 199 | Blargg | Enemy | - | ✓ | - | - | - | - | - | - | - | - | - | - | - |
| 200 | Bowser (SMB1) | Boss | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | - |
| 201 | Wart | Boss | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | - |
| 202 | Wart's buble | Bult | - | ✓ | - | - | - | - | - | - | - | Hurt | - | - | - |
| 203 | Ripper | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | - | - | - | - | ✓ | - | ✓ |
| 204 | Rocket Ripper | Enemy | - | ✓ | ✓ | - | ✓ | ✓ | - | - | - | - | ✓ | - | ✓ |
| 205 | Zoomer | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 206 | Spark | Enemy | - | - | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | - | ✓ |
| 207 | Spike Top | Enemy | - | - | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | - | ✓ |
| 208 | glass flask | Boss | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | ✓ | ✓ | - |
| 209 | Mother Brain | Boss | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | Hurt | ✓ | - | - |
| 210 | Rinka | Bult | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | - |
| 211 | Rinka block | Scene | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - | - |
| 213 | Green vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 214 | Red vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 215 | Green vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 216 | Yellow vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 217 | Blue vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 218 | Green vines end | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 219 | Yellow vines end | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 220 | Blue vines end | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 221 | Ladder | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 222 | Green vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 223 | Green vines end | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 224 | Green vines | Ladder | ✓ | - | - | - | - | - | - | - | - | - | - | - | - |
| 225 | Red vines head | Ladder | ✓ | - | - | - | - | ✓ | - | - | - | - | - | - | - |
| 226 | Green vines head | Ladder | ✓ | - | - | - | - | ✓ | - | - | - | - | - | - | - |
| 227 | Green vines head | Ladder | ✓ | - | - | - | - | ✓ | - | - | - | - | - | - | - |
| 228 | Ice Yoshi | Trans | - | - | - | - | - | ✓ | ✓ | - | - | Mnt | - | - | - |
| 229 | Green cheep-cheep | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | ✓ | Kill/ | - | ✓ | ✓ |
| 230 | Red cheep-cheep | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | ✓ | Kill/ | - | ✓ | ✓ |
| 231 | Blooper | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 232 | Blurp | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 233 | Green cheep-cheep | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 234 | Fishbone | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | - | Hurt | ✓ | - | ✓ |
| 235 | Blooper | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 236 | Blurp (Yoshi's Story) | Enemy | - | ✓ | ✓ | - | - | Under | ✓ | - | ✓ | Kill/ | ✓ | ✓ | ✓ |
| 237 | Ice cube (Cyan yoshi's) | Carry | - | - | ✓ | - | - | ✓ | ✓ | - | - | - | ✓ | - | - |
| 238 | P switch (stop time) | Button | - | - | ✓ | ✓ | - | ✓ | ✓ | - | ✓ | PBlk | - | - | - |
| 239 | Dynamit switcher | Button | ✓ | - | ✓ | - | - | ✓ | ✓ | - | ✓ | Activ | - | - | - |
| 240 | Stop Watch | Bonus | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 241 | Pow block | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| 242 | Goomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 243 | Paragoomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Chang | ✓ | ✓ | ✓ |
| 244 | Paragoomba | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | Chang | ✓ | ✓ | ✓ |
| 245 | Venus FireTrap | Enemy | - | ✓ | - | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 246 | Venus FireTrap's fireball | Bult | - | ✓ | - | - | - | - | ✓ | - | - | Hurt | ✓ | - | - |
| 247 | Pokey | Enemy | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | ✓ | - | - |
| 248 | Stop Watch (add into item stock) | Bonus | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Add i | - | - | - |
| 249 | Red mushroom | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 250 | Heart | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 251 | Emerald | Bonus | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 252 | Sapphire | Bonus | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 253 | Ruby | Bonus | - | - | - | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 254 | Fairy | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 255 | Locked door | Scene | ✓ | - | ✓ | - | - | ✓ | - | - | - | Kill  | - | - | - |
| 256 | Big Piranha plant | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | - |
| 257 | Turned Big Piranha plant | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | - |
| 258 | Blue coin | Bonus | - | - | - | - | - | ✓ | - | ✓ | - | Take | - | - | - |
| 259 | Roto-Disc | Scene | ✓ | - | - | - | - | - | - | - | - | Hurt | - | - | - |
| 260 | Firebar | Scene | ✓ | ✓ | - | - | - | - | - | - | - | Hurt | - | - | - |
| 261 | Nipper Plant | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | - | ✓ |
| 262 | Mouser | Boss | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - | ✓ | ✓ | - |
| 263 | Ice texture | Carry | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - | - | Unpac | - |
| 264 | Ice flower | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 266 | Link's sword shoot | Bult | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 267 | Larry Koopa | Boss | - | ✓ | - | - | - | ✓ | ✓ | - | ✓ | Kill  | ✓ | ✓ | - |
| 268 | Larry's shell | Boss | - | ✓ | - | - | - | ✓ | ✓ | - | - | - | ✓ | ✓ | - |
| 269 | Larry's Magic ring | Bult | - | ✓ | - | - | - | - | - | - | - | Hurt | - | - | - |
| 270 | Jumping Piranha Plant | Enemy | - | ✓ | - | - | - | - | - | - | - | Hurt | ✓ | ✓ | ✓ |
| 271 | Swooper | Enemy | - | ✓ | - | - | - | - | ✓ | - | ✓ | Kill | ✓ | ✓ | ✓ |
| 272 | Hoopster | Enemy | - | ✓ | - | - | - | - | ✓ | - | - | - | ✓ | - | ✓ |
| 273 | «?» mushroom | Power | - | - | - | - | - | ✓ | ✓ | ✓ | - | Chang | - | - | - |
| 274 | Dragon coin | Bonus | - | - | - | - | - | - | - | ✓ | - | Take | - | - | - |
| 275 | Volcano lotus | Enemy | - | ✓ | ✓ | - | - | ✓ | - | - | - | Hurt | ✓ | - | - |
| 276 | Volcano lotus fire | Bult | - | ✓ | - | - | - | - | ✓ | - | - | Hurt | - | - | - |
| 277 | Ice flower | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 278 | Propeller block | Carry | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 279 | Flame Propeller block | Carry | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 280 | Ludwig von Koopa | Boss | - | ✓ | - | - | - | ✓ | ✓ | - | ✓ | Kill  | ✓ | ✓ | - |
| 281 | Ludwig von Koopa's shell | Boss | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | - | - | ✓ | - |
| 282 | Ludwig von Koopa's fire | Bult | - | ✓ | - | - | - | - | - | - | - | Hurt | - | - | - |
| 283 | Bubble | Conta | - | - | - | - | - | ✓ | - | - | - | Unpac | - | ✓ | - |
| 284 | Lakitu (SMW) | Enemy | - | ✓ | - | - | - | - | ✓ | - | ✓ | Kill | - | ✓ | - |
| 285 | Spiny | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 286 | Spiny egg | Enemy | - | ✓ | ✓ | - | - | ✓ | ✓ | - | - | Hurt | ✓ | ✓ | ✓ |
| 287 | Random PowerUP | Power | - | - | ✓ | - | - | ✓ | ✓ | ✓ | - | Take | - | - | - |
| 288 | Magic Potion | Carry | - | - | - | - | - | ✓ | ✓ | - | - | Chang | - | - | - |
| 289 | Subspace door | Door | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 290 | Airship part | Trans | ✓ | - | - | - | ✓ | - | - | - | - | Mnt | - | - | - |
| 291 | Peach's bomb | Bult | - | - | - | - | - | ✓ | ✓ | - | - | - | - | - | - |
| 292 | Toad's Boomerang | Bult | - | - | - | - | - | - | - | - | - | - | - | - | - |

---

## 完整属性详情（按类型分组）

### Enemy（107个）

#### #1 Goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #2 Red Goomna

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #3 Para Goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #4 Green Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #6 Red Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #8 Green Piranha plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #12 Podoboo

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #17 Bullet Bill

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Edible by Yoshi | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #18 Banzai Bill

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #19 Shy-Guy Red

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #20 Shy-Guy Blue

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #23 Buzzy beetle

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #25 Violet Ninja

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #27 Blue goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #28 Red Cheep

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #29 Hammer bros.

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #36 Spiny

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #37 Thwomp

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #38 Boo

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #39 Birdo

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #42 Eerie (Dino ghost)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can burred | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #43 Boo

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #44 Big Boo

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #47 Lakitu (SMB3)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #48 Lakitu's ball

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #50 Toothie

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| On Jump/take | Nothing |

#### #51 Turned Red Piranha Plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #52 Horisontal Red Piranha Plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #54 Fighter Fly

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #55 Blue Beach Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #59 Yellow goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/toggle yellow switch |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #61 Blue goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/toggle blue switch |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #63 Green goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/toggle green switch |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #65 Red goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/toggle red switch |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #71 Big goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #72 Big green Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #73 Big green Koopa's shell

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Only moving |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start MV/nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #74 Big red piranha plant

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #76 Green Para-Koopa

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #77 Ninja

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Jump on cliff |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #89 Goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #93 Piranha plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #109 SMW green Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC+spawn |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #110 SMW red Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC+spawn |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #111 SMW blue Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit / Yoshi can fly |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC+spawn |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #112 SMW yellow Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC+spawn |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #117 Green Beach Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #118 Red Beach Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #119 Blue Beach Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Only behind |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #120 Yellow Beach Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #121 SMW green paraKoopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #122 SMW red paraKoopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #123 SMW blue paraKoopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit / Yoshi can fly |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #124 SMW yellow paraKoopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #125 Tinsuit (jackal) (LoZ)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #126 Bot blue (LoZ)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #127 Bot cyan (LoZ)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #128 Bit (LoZ)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #129 Twitter

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #130 Red Snifit

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #131 Blue Snifit

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #132 Gray Snifit

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #135 Bob-omb (SMB2)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #136 Bob-omb (SMB3)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |

#### #161 Red para-Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #162 Rex

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #163 Rex kicked

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #164 Mega mole

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #165 Galoomba (SMW)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #167 Para-Galoomba (SMW)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #168 Bully (SM64)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Throw up |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |

#### #173 Green Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #175 Red Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #176 Green Para-Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #177 Red para-Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Kill On SlopeSlide | Yes |
| On Jump/take | ChangeNPC |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #180 Thwomp

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #189 Dry Bones

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Temportary cut down |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #194 Kamikaze Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can't be die | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| On Jump/take | Throw up player |
| Freezable by iceball | Yes |
| Kill by racoon's tail | ChangeNPC |
| Kill by spin/tanooki statue | Yes |

#### #199 Blargg

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Nothing |

#### #203 Ripper

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |

#### #204 Rocket Ripper

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |

#### #205 Zoomer

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #206 Spark

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |

#### #207 Spike Top

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #229 Green cheep-cheep

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/hurt player underwater |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #230 Red cheep-cheep

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/hurt player underwater |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #231 Blooper

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #232 Blurp

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/hurt player underwater |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #233 Green cheep-cheep

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/hurt player underwater |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #234 Fishbone

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #235 Blooper

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #236 Blurp (Yoshi's Story)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Underwater only |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill/hurt player underwater |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #242 Goomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #243 Paragoomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Change characters |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #244 Paragoomba

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Change characters |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #245 Venus FireTrap

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #247 Pokey

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #256 Big Piranha plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #257 Turned Big Piranha plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #261 Nipper Plant

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #270 Jumping Piranha Plant

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #271 Swooper

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #272 Hoopster

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |

#### #275 Volcano lotus

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #284 Lakitu (SMW)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill on fireball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

#### #285 Spiny

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

#### #286 Spiny egg

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Statue only |

### Boss（11个）

#### #15 Boom-boom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill |
| Kill by shell | Yes |
| Kill on hammer | Yes |
| Kill by spin/tanooki statue | Yes |

#### #86 Bowser (SMB-3)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #200 Bowser (SMB1)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #201 Wart

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #208 glass flask

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #209 Mother Brain

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #262 Mouser

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #267 Larry Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill on 3-th jump |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |
| Kill by spin/tanooki statue | Yes |

#### #268 Larry's shell

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

#### #280 Ludwig von Koopa

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Kill on 3-th jump |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |
| Kill by spin/tanooki statue | Yes |

#### #281 Ludwig von Koopa's shell

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill on fireball | Yes |
| Kill on hammer | Yes |

### People（9个）

#### #75 Jumping Toad

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #94 Toad

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #101 Luigi

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #102 Link

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #107 Ping Bob-omb

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #149 Purpure Yoshi

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #150 Pink Yoshi

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #151 the «?» plate

| 属性 | 值 |
|---|---|
| Block Collision | Yes |
| On Jump/take | Nothing |

#### #198 Peach

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

### Power-UP（17个）

#### #9 Mushroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #14 Fire flower

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #34 Racoon leaf

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #90 1up murshroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #169 Tanooki suit

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Freezable by iceball | Yes |
| Kill by racoon's tail | Throw up |

#### #170 Hammer suit

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #182 Fire flower

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #183 Fire flower

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #184 Red mushroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #185 Red mushroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #249 Red mushroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #250 Heart

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #254 Fairy

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #264 Ice flower

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #273 «?» mushroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Change characters |

#### #277 Ice flower

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #287 Random PowerUP

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Can be take | Yes |
| On Jump/take | Take |

### Bonus（18个）

#### #10 Gold Coin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #33 Yellow coin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| On Jump/take | Take |

#### #88 Gold Coin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #103 Red coin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #138 Gold Coin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #152 Gold ring

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #153 Poison mushroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take+Hurt player |
| Kill by racoon's tail | Throw up |

#### #178 Axe

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #186 Life murshroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #187 Life murshroom

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |
| Kill by racoon's tail | Throw up |

#### #188 Life moon

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #240 Stop Watch

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #248 Stop Watch (add into item stock)

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can be take | Yes |
| On Jump/take | Add into item stock |

#### #251 Emerald

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #252 Sapphire

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #253 Ruby

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #258 Blue coin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Take |

#### #274 Dragon coin

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Can be take | Yes |
| On Jump/take | Take |

### Exit point（6个）

#### #11 Random exit bonus

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Level End |

#### #16 Mistary Ball

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Level End |

#### #41 Crystal sphere

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Level End |

#### #97 Star

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Can be take | Yes |
| On Jump/take | Level End |

#### #192 Check point

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Take+save position |

#### #197 Exit point

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Can be take | Yes |
| On Jump/take | Level End |

### Carryble tool（41个）

#### #5 Green Koopa's shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start/stop MV |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #7 Red Koopa's shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start/stop MV |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #22 Billy Gun

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #24 Buzzy's shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Start/stop MV |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #26 Springboard

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| On Jump/take | Bounce player |

#### #31 Big key

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #45 Ice Block (Grabbable)

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #49 Toothie Pipe

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #91 Herb (have contents)

| 属性 | 值 |
|---|---|
| Player Collision top | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #92 Vegatable — onions

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #96 Color eggs

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| On Jump/take | Nothing |

#### #113 SMW green shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start MV/nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #114 SMW red shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start MV/nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #115 SMW blue shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit / Yoshi can fly |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start MV/nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #116 SMW yellow shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start MV/nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #134 Mouser's Bomb

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #137 Bob-omb kicked (SMB3)

| 属性 | 值 |
|---|---|
| hurt to player | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |

#### #139 Vegetable onions glasses

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #140 Vegetable turnip

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #141 Vegetable radish 1

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #142 Vegetable green pumpkin

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #143 Vegetable small carrots

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #144 Vegetable radish 2

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #145 Vegetable radish 3

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #146 Vegetable big carrots

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #147 Random vegetable

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| On Jump/take | Nothing |

#### #154 Mushroom Block 1

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #155 Mushroom Block 2

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #156 Mushroom Block 3

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #157 Mushroom Block 4

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #158 Mr. Saturn

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| clif turn | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill by racoon's tail | Throw up |

#### #166 Kicked Galoomba (SMW)

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by spin/tanooki statue | Yes |

#### #172 Green shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start/stop MV |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #174 Red shell

| 属性 | 值 |
|---|---|
| hurt to player | Only moving |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Shoot fire |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Start/stop MV |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Freezable by iceball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Throw up |
| Kill by spin/tanooki statue | Yes |

#### #195 Rainbow Shell

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Start/stop MV |
| Freezable by iceball | Yes |
| Kill by racoon's tail | Throw up |

#### #237 Ice cube (Cyan yoshi's)

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #241 Pow block

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #263 Ice texture

| 属性 | 值 |
|---|---|
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill on fireball | Unpack NPC |
| Kill by spin/tanooki statue | Yes |

#### #278 Propeller block

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #279 Flame Propeller block

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Nothing |

#### #288 Magic Potion

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| Can by Grab side | Yes |
| Can by Grab top | Yes |
| On Jump/take | Change NPC on fall |

### Transport（11个）

#### #35 Kuribo's shoe

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| On Jump/take | Mount to player |

#### #56 Clown car

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| On Jump/take | Mount to player |

#### #95 Green Yoshi

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #98 Blue Yoshi

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #99 Yellow Yoshi

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #100 Red Yoshi

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #148 Gray Yoshi

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #191 Podoboo's shoe

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| On Jump/take | Mount to player |

#### #193 Lakitu's shoe

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| On Jump/take | Mount to player |

#### #228 Ice Yoshi

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Mount to player |

#### #290 Airship part

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| On Jump/take | Mount to player |

### Bullet（17个）

#### #13 Fireball (player)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #30 Hammer

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #40 Birdo's egg

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab top | Yes |
| On Jump/take | Nothing |
| Kill by shell | Yes |
| Kill on hammer | Yes |

#### #85 Bowser's statue's fire

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| On Jump/take | Hurt player |

#### #87 Bowser's fire

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| On Jump/take | Hurt player |

#### #108 Yoshi's Fireball

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #133 Snifit's bullet

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Hurt player |

#### #171 Hammer (player)

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #202 Wart's buble

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| On Jump/take | Hurt player |

#### #210 Rinka

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |
| Kill on fireball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |

#### #246 Venus FireTrap's fireball

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |
| Kill by shell | Yes |

#### #266 Link's sword shoot

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| On Jump/take | Nothing |

#### #269 Larry's Magic ring

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| On Jump/take | Hurt player |

#### #276 Volcano lotus fire

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |

#### #282 Ludwig von Koopa's fire

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| On Jump/take | Hurt player |

#### #291 Peach's bomb

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #292 Toad's Boomerang

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| On Jump/take | Nothing |

### Button（3个）

#### #32 Blue P switch

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Activate P-block |

#### #238 P switch (stop time)

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Can spit |
| Can by Grab side | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Activate P-block |

#### #239 Dynamit switcher

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Kill On HeadJump | Yes |
| On Jump/take | Activate event |

### Platform（6个）

#### #60 Yellow platform

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |
| Freezable by iceball | Yes |

#### #62 Blue platform

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |
| Freezable by iceball | Yes |

#### #64 Green platform

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #66 Red platform

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #104 Wood platform (fall because mass)

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| On Jump/take | Enable gravity |

#### #190 Skull lava platform

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Start MV/nothing |

### Mass platform（2个）

#### #46 Red donut block

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| On Jump/take | Enable gravity |

#### #105 Thin platform

| 属性 | 值 |
|---|---|
| Can't be die | Yes |
| NPC Collision top | Yes |
| Player Collision top | Yes |
| On Jump/take | Enable gravity if stand |

### Scenery（20个）

#### #21 Bill Blaster

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #57 Conveyor

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| On Jump/take | Nothing |

#### #58 Iron Curbstone

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #67 Horisontal pipe x4

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #68 Horisontal pipe x8

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #69 Vertical pipe x4

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #70 Vertical pipe x8

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #78 Tractor caterpillars

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #79 Wood block x2

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #80 Wood block x4

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #81 Wood block x4 2

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #82 Wood block x4 3

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #83 Wood block x8

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #84 Bowser's statue

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #160 Jet wooden platform

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Is Scenery | Yes |
| Can't be die | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #181 Bowser's statue

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Nothing |

#### #211 Rinka block

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Player Collision | Yes |
| Player Collision top | Yes |
| Block Collision | Yes |
| On Jump/take | Nothing |

#### #255 Locked door

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| NPC Collision | Yes |
| NPC Collision top | Yes |
| Block Collision | Yes |
| On Jump/take | Kill on Key touch |

#### #259 Roto-Disc

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can bubble | Yes |
| Can burred | Yes |
| On Jump/take | Hurt player |

#### #260 Firebar

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| hurt to player | Yes |
| Can bubble | Yes |
| Can burred | Yes |
| On Jump/take | Hurt player |

### Container（1个）

#### #283 Bubble

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| Block Collision | Yes |
| Kill On SlopeSlide | Yes |
| On Jump/take | Unpack NPC on any collision |
| Kill on fireball | Yes |
| Kill on hammer | Yes |
| Kill by racoon's tail | Yes |
| Kill by spin/tanooki statue | Yes |

### Door（1个）

#### #289 Subspace door

| 属性 | 值 |
|---|---|
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| Edible by Yoshi | Yes |
| On Jump/take | Nothing |

### Enemy/Platform（1个）

#### #179 Circular saw

| 属性 | 值 |
|---|---|
| moving itself | Yes |
| hurt to player | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| Gravity enabled | Yes |
| On Jump/take | Hurt player |

### Ladder（15个）

#### #213 Green vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #214 Red vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #215 Green vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #216 Yellow vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #217 Blue vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #218 Green vines end

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #219 Yellow vines end

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #220 Blue vines end

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #221 Ladder

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #222 Green vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #223 Green vines end

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #224 Green vines

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| On Jump/take | Nothing |

#### #225 Red vines head

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| On Jump/take | Nothing |

#### #226 Green vines head

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| On Jump/take | Nothing |

#### #227 Green vines head

| 属性 | 值 |
|---|---|
| Is Scenery | Yes |
| Can't be die | Yes |
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Block Collision | Yes |
| On Jump/take | Nothing |

### Special（1个）

#### #196 Takeble Star

| 属性 | 值 |
|---|---|
| Can bubble | Yes |
| Can egg | Yes |
| Can Lakitu | Yes |
| Can burred | Yes |
| Can be take | Yes |
| On Jump/take | Take |

---

*Source: SMBX 38A documentation. Created by Wohlstand and Veudekato.*

*Auto-converted from PDF by AI.*