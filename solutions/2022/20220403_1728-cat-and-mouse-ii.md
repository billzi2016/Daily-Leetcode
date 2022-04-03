# #1728. 猫和老鼠 II / Cat and Mouse II

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Graph、Topological Sort、Memoization、Matrix、Game Theory · [LeetCode 链接](https://leetcode.com/problems/cat-and-mouse-ii/)

---

## 题目（英文原版）

**Description**

A game is played by a cat and a mouse named Cat and Mouse.
The environment is represented by a grid of size rows x cols, where each element is a wall, floor, player (Cat, Mouse), or food.
Mouse and Cat play according to the following rules:
The game can end in 4 ways:
Given a rows x cols matrix grid and two integers catJump and mouseJump, return true if Mouse can win the game if both Cat and Mouse play optimally, otherwise return false.

**Examples**

**Example 1:**

```
Input: grid = ["####F","#C...","M...."], catJump = 1, mouseJump = 2
Output: true
Explanation: Cat cannot catch Mouse on its turn nor can it get the food before Mouse.
```

**Example 2:**

```
Input: grid = ["M.C...F"], catJump = 1, mouseJump = 4
Output: true
```

**Example 3:**

```
Input: grid = ["M.C...F"], catJump = 1, mouseJump = 3
Output: false
```

**Constraints**

- rows == grid.length
- cols = grid[i].length
- 1 <= rows, cols <= 8
- grid[i][j] consist only of characters 'C', 'M', 'F', '.', and '#'.
- There is only one of each character 'C', 'M', and 'F' in grid.
- 1 <= catJump, mouseJump <= 8

---

## 题目（中文翻译）

**描述**  
一只猫和一只老鼠在一个由 `rows x cols` 的网格（grid）中进行游戏。网格中的每个格子可能是墙壁（wall）、空地（floor）、玩家（Cat、Mouse）或食物（food）。  

猫和老鼠轮流行动，老鼠先手。每一回合，当前玩家可以向上、下、左、右四个方向中的任意一个移动，最多移动 `catJump`（对于猫）或 `mouseJump`（对于老鼠）格。玩家可以选择在途中任意格子停下，且移动路径上不能经过墙壁（`#`）。玩家也可以选择不移动。

游戏可能以以下四种方式结束：

1. **老鼠先到达食物** → 老鼠获胜。  
2. **猫在自己的回合捕捉到老鼠**（两者位于同一格子） → 猫获胜。  
3. **猫先到达食物** → 猫获胜。  
4. **游戏进行的回合数超过 1000** → 猫获胜（视为平局，判定为猫胜）。

给定网格 `grid`、整数 `catJump` 与 `mouseJump`，如果在双方都采用最优策略的前提下老鼠能够获胜，返回 `true`；否则返回 `false`。

**示例**

> 示例 1  
> 输入: `grid = ["####F","#C...","M...."]`, `catJump = 1`, `mouseJump = 2`  
> 输出: `true`  
> 解释: 猫在其回合无法捕捉到老鼠，也无法在老鼠之前拿到食物。

> 示例 2  
> 输入: `grid = ["M.C...F"]`, `catJump = 1`, `mouseJump = 4`  
> 输出: `true`  

> 示例 3  
> 输入: `grid = ["M.C...F"]`, `catJump = 1`, `mouseJump = 3`  
> 输出: `false`  

**约束条件**

- `rows == grid.length`  
- `cols = grid[i].length`  
- `1 <= rows, cols <= 8`  
- `grid[i][j]` 仅包含字符 `'C'`（猫）、`'M'`（老鼠）、`'F'`（食物）、`'.'`（空地）和 `'#'`（墙壁）  
- 网格中恰好各出现一次 `'C'`、`'M'` 和 `'F'`  
- `1 <= catJump, mouseJump <= 8`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

这是一盘**两人零和游戏**（Cat 与 Mouse 轮流行动），我们想判断在双方都「最聪明」的情况下，Mouse 能否一定赢。  
最直接的想法是 **枚举所有可能的走法**，把每一种局面都当成一棵「决策树」：

1. **状态（state）**  
   - 猫所在的格子 `(cr, cc)`  
   - 老鼠所在的格子 `(mr, mc)`  
   - 轮到谁走：`turn = 0` 表示 Mouse，`turn = 1` 表示 Cat  

   这就像在棋盘上放了两个棋子，再记一下现在是谁的回合。  

2. **递归**  
   - 如果当前状态已经是**终止状态**（鼠到食物、猫抓到鼠、猫先到食物、或超过 1000 步——题目里用 1000 步限制防止无限循环），直接返回结果。  
   - 否则，依据 `turn` 生成**所有合法的下一步**（向上下左右每个方向最多跳 `mouseJump` 或 `catJump` 步，途中不能穿墙 `#`，也可以选择不动）。  
   - 对每一种下一步递归求值。  
   - **取最优**：  
     - `turn == 0`（Mouse）希望至少有 **一种** 下一步可以让自己赢（返回 `True`），否则输。  
     - `turn == 1`（Cat）希望 **所有** 下一步都让 Mouse 输（返回 `False`），只要有一步可以让 Mouse 输，Cat 就会选这一步。  

3. **防止无限递归**  
   - 用一个 `visited` 集合记住已经遍历过的状态 `(cr, cc, mr, mc, turn)`，如果再次进入同样的状态直接返回 `False`（相当于「这条路走不通」）。  

> **生活化类比**：  
> 想象你在一张格子地图上玩「追逐游戏」。每一步你可以往前走几格（跳数），墙壁是阻挡。你想知道如果你是老鼠，能否一定抢先到达食物而不被猫抓住。暴力递归就像把「所有可能的走法」都画成一张大树，逐层往下看有没有一条通向胜利的路径。

**为什么这个方法正确？**  
因为我们枚举了 **每一种** 合法的行动，并且在每一步都遵循「双方都最优」的假设：  
- 老鼠只要有一条必胜路线就会选这条。  
- 猫则会挑选让老鼠必输的路线。  
递归的返回值正好对应「在该状态下，老鼠是否能必胜」。

**时间/空间复杂度**（大白话）  
- 状态数最多是 `rows * cols`（猫的位置） × `rows * cols`（老鼠的位置） × `2`（轮到谁） ≤ `8*8*8*8*2 = 8192`。  
- 暴力递归会对每个状态 **尝试所有跳数**，每次最多向四个方向走 `jump` 步，最坏情况是 `4 * jump` 种选择。  
- 因此时间复杂度约为 `O(states * (catJump+mouseJump) * 4)`，在最坏的 8×8、jump=8 时大约是 **几万次**，但由于递归会产生大量重复子问题，实际会呈指数级爆炸，超过 1 秒就会超时。  
- 空间方面，递归栈深度最多是状态数，约 `O(states)`，即几千个栈帧。

> 用大白话说：**暴力解像是把所有可能的棋谱都写下来，然后一条条检查**，看起来思路清晰，但会写出几千页纸，效率太低。

#### 代码（Python）

```python
from typing import List, Tuple, Set

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def canMouseWin_bruteforce(grid: List[str], catJump: int, mouseJump: int) -> bool:
    rows, cols = len(grid), len(grid[0])

    # 找到初始位置
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'M':
                mouse_start = (r, c)
            if grid[r][c] == 'C':
                cat_start = (r, c)
            if grid[r][c] == 'F':
                food = (r, c)

    # 判断 (r,c) 是否是墙
    def is_wall(r: int, c: int) -> bool:
        return grid[r][c] == '#'

    # 生成所有合法的下一步
    def next_positions(pos: Tuple[int, int], jump: int) -> List[Tuple[int, int]]:
        r0, c0 = pos
        res = [(r0, c0)]                     # 可以选择不动
        for dr, dc in DIRS:
            for step in range(1, jump + 1):
                nr, nc = r0 + dr * step, c0 + dc * step
                if not (0 <= nr < rows and 0 <= nc < cols):   # 越界
                    break
                if is_wall(nr, nc):                           # 碰到墙，后面的格子也不可达
                    break
                res.append((nr, nc))
        return res

    # 递归 + 记忆化 + 防止无限循环
    from functools import lru_cache

    @lru_cache(None)
    def dfs(cr: int, cc: int, mr: int, mc: int, turn: int, steps: int) -> bool:
        """
        返回在当前局面下，Mouse 是否必胜。
        turn == 0 -> Mouse 走； turn == 1 -> Cat 走
        steps 用来限制最多 1000 步（题目给的安全上限）
        """
        # 终止条件
        if (mr, mc) == food:          # Mouse 已经到食物
            return True
        if (cr, cc) == food:          # Cat 抢先到食物
            return False
        if (cr, cc) == (mr, mc):      # Cat 抓到 Mouse
            return False
        if steps >= 1000:             # 防止无限循环（题目硬限制）
            return False

        if turn == 0:  # Mouse 回合
            for nr, nc in next_positions((mr, mc), mouseJump):
                if dfs(cr, cc, nr, nc, 1, steps + 1):
                    return True          # 找到一条必胜路径
            return False                 # 所有选择都输
        else:          # Cat 回合
            for nr, nc in next_positions((cr, cc), catJump):
                if not dfs(nr, nc, mr, mc, 0, steps + 1):
                    return False         # Cat 能让 Mouse 输，故 Mouse 输
            return True                  # 猫所有选择都让 Mouse 赢，Mouse 赢

    return dfs(cat_start[0], cat_start[1],
               mouse_start[0], mouse_start[1],
               0, 0)   # 从 Mouse 的回合开始

# -------------------------------------------------
# 示例测试
if __name__ == "__main__":
    g1 = ["####F", "#C...", "M...."]
    print(canMouseWin_bruteforce(g1, 1, 2))   # True
```

#### 复杂度  

- **时间复杂度**：`O( (R*C)^2 * (catJump+mouseJump) * 4 )`（指数级，实际会超时）  
  - 解释：每个状态会尝试所有可能的跳步，子状态之间大量重复，导致递归树呈指数增长。  
- **空间复杂度**：`O( (R*C)^2 )`（递归栈 + 记忆化表）  
  - 解释：最多需要记住每一种「猫位置 × 老鼠位置 × 回合」的结果，大约几千个条目。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于 **大量重复子问题**：同一个局面会被不同的走法反复算。  
我们可以把**所有局面**看成图中的节点，**合法的走法**看成有向边。  
在 **博弈论** 中，这类「谁能必胜」的判定可以用 **“逆向拓扑”**（retrograde analysis）来完成：

1. **状态定义**  
   - 同暴力解：`(cat_r, cat_c, mouse_r, mouse_c, turn)`。  
   - 用整数 `0/1` 表示 `turn`（0 = Mouse，1 = Cat）。

2. **终止状态（已知胜负）**  
   - Mouse 已在食物格 → **Mouse 赢**（标记为 `WIN`）。  
   - Cat 已在食物格、或 Cat 与 Mouse 同格 → **Mouse 输**（标记为 `LOSE`）。  
   - 这些状态不需要再展开。

3. **出度 / 入度**  
   - 对每个状态，**出度** = 它可以走到的合法下一状态数量。  
   - **入度** = 有多少其他状态可以一步到达当前状态（逆向边）。  

4. **逆向 BFS（拓扑）**  
   - 把所有已知的 `WIN/LOSE` 状态放进队列。  
   - **弹出一个状态** `s`，检查所有**前驱** `p`（即能够一步转向 `s` 的状态）。  
   - 根据 `p` 的回合来决定 `p` 的标记：  
     - **如果 `p` 是 Mouse 的回合**，只要有 **一个** 后继是 `WIN`，Mouse 就会选这步，使 `p` 成为 `WIN`。  
     - **如果 `p` 是 Cat 的回合**，只有当 **所有** 后继都是 `WIN`（对 Mouse 来说是输）时，`p` 才会被标记为 `LOSE`（即 Mouse 输）。  
   - 为了判断「所有后继」是否已经是 `WIN`，我们使用 **出度计数**：每当一个后继被确认是 `WIN`，就把 `p` 的 `remaining_outdegree` 减 1；当计数降到 0，说明所有后继都是 `WIN`，于是 `p` 成为 `LOSE`。  
   - 这个过程类似 **拓扑排序**：我们一次“消除”确定好的节点，逐步向前推进。

5. **结束**  
   - 当队列为空时，所有可达状态都已经被标记为 `WIN` 或 `LOSE`。  
   - 初始状态（题目给的猫、鼠位置，且 Mouse 先手）如果是 `WIN`，说明 Mouse 必胜，返回 `True`；否则返回 `False`。  

6. **为何有效**  
   - 逆向分析从「已知的必输/必赢」出发，利用 **必然最优** 的假设（每个人都挑对自己最有利的动作），逐层推断出更早的局面结果。  
   - 与递归记忆化相比，它一次遍历每个状态和每条边，避免了重复计算，时间上是 **线性的**（相对于状态图的规模）。

7. **关键数据结构**  

| 名称 | 作用 | 类比 |
|------|------|------|
| `status[(cr,cc,mr,mc,turn)]` | 记录每个状态是 `UNKNOWN / WIN / LOSE` | 像一本「胜负手册」里给每个局面贴标签 |
| `outdeg[(cr,cc,mr,mc,turn)]` | 该状态还能走多少步（未确定的后继数） | 像每个棋子还有多少「可能的下一步」 |
| `queue` | BFS 队列，存放已经确定结果的状态 | 像「已知答案」的通知板，随时传播给前驱 |

8. **实现细节**  
   - 由于 `rows, cols ≤ 8`，总状态数 ≤ `8*8*8*8*2 = 8192`，完全可以一次性遍历并存入数组。  
   - 为了快速得到前驱，需要 **反向枚举**：对每个状态，遍历它所有合法的「下一步」，把当前状态加入那一步的前驱列表。  
   - 另外题目要求最多 1000 步才能判定平局；在逆向分析里，这相当于**把所有超过 1000 步的状态视为 LOSE**（因为如果游戏走得太久，Mouse 也算输），但实际实现中不必显式计数，只要把 **所有未被标记的状态** 视为「可能循环」而最终归为 `LOSE`（因为在最优对局中不会出现无限循环）。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List, Tuple

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def canMouseWin(grid: List[str], catJump: int, mouseJump: int) -> bool:
    R, C = len(grid), len(grid[0])

    # ------------------- 1. 读取初始位置 -------------------
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'M':
                mouse_start = (r, c)
            elif grid[r][c] == 'C':
                cat_start = (r, c)
            elif grid[r][c] == 'F':
                food = (r, c)

    # ------------------- 2. 辅助函数 -------------------
    def inside(r: int, c: int) -> bool:
        return 0 <= r < R and 0 <= c < C and grid[r][c] != '#'

    # 给定位置和对应的跳数，返回所有可以到达的格子（包括原地不动）
    def moves(pos: Tuple[int, int], jump: int) -> List[Tuple[int, int]]:
        r0, c0 = pos
        res = [(r0, c0)]                     # 可以选择停在原地
        for dr, dc in DIRS:
            for step in range(1, jump + 1):
                nr, nc = r0 + dr * step, c0 + dc * step
                if not inside(nr, nc):
                    break                 # 越界或撞墙，方向停止
                res.append((nr, nc))
        return res

    # ------------------- 3. 状态编码 -------------------
    # 使用整数编码把 (cr, cc, mr, mc, turn) 映射到唯一的 id
    def encode(cr, cc, mr, mc, turn):
        return (((cr * C + cc) * (R * C) + (mr * C + mc)) << 1) | turn

    total_states = (R * C) * (R * C) * 2
    UNKNOWN, WIN, LOSE = 0, 1, 2

    status = [UNKNOWN] * total_states          # 0:未知, 1:Mouse赢, 2:Mouse输
    outdeg = [0] * total_states                # 该状态的合法后继数
    # 前驱列表：state_id -> [prev_state_id, ...]
    prev = defaultdict(list)

    # ------------------- 4. 遍历所有可能的状态，构图 -------------------
    for cr in range(R):
        for cc in range(C):
            if grid[cr][cc] == '#': continue
            for mr in range(R):
                for mc in range(C):
                    if grid[mr][mc] == '#': continue
                    for turn in (0, 1):       # 0 Mouse, 1 Cat
                        sid = encode(cr, cc, mr, mc, turn)

                        # 终止状态直接标记
                        if (mr, mc) == food:            # Mouse 已到食物
                            status[sid] = WIN
                            continue
                        if (cr, cc) == food:            # Cat 抢到食物
                            status[sid] = LOSE
                            continue
                        if (cr, cc) == (mr, mc):        # 猫抓到鼠
                            status[sid] = LOSE
                            continue

                        # 计算合法后继（下一步的状态）
                        cur_moves = moves((mr, mc), mouseJump) if turn == 0 else moves((cr, cc), catJump)
                        outdeg[sid] = len(cur_moves)    # 出度计数

                        for nr, nc in cur_moves:
                            if turn == 0:                # Mouse 走 -> 猫保持不变，换成 Cat 回合
                                nxt = encode(cr, cc, nr, nc, 1)
                            else:                       # Cat 走 -> Mouse 不变，换成 Mouse 回合
                                nxt = encode(nr, nc, mr, mc, 0)
                            # 建立逆向边：nxt 的前驱是 sid
                            prev[nxt].append(sid)

    # ------------------- 5. 初始化队列（已知胜负） -------------------
    q = deque()
    for sid, st in enumerate(status):
        if st != UNKNOWN:
            q.append(sid)               # 已知 WIN/LOSE 的状态进入队列

    # ------------------- 6. 逆向拓扑 BFS -------------------
    while q:
        cur = q.popleft()
        cur_state = status[cur]

        for pre in prev[cur]:          # 所有能走到 cur 的前驱
            if status[pre] != UNKNOWN:
                continue               # 已经决定过，跳过

            turn = pre & 1             # 0 Mouse, 1 Cat（因为我们把 turn 放在最低位）
            if turn == 0:              # 前驱是 Mouse 的回合
                # Mouse 只要能找到一个后继是 WIN，自己就是 WIN
                if cur_state == WIN:
                    status[pre] = WIN
                    q.append(pre)
                else:                  # 当前后继是 LOSE，Mouse 仍需寻找其他可能的 WIN
                    outdeg[pre] -= 1
                    if outdeg[pre] == 0:   # 所有后继都是 LOSE → Mouse 输
                        status[pre] = LOSE
                        q.append(pre)
            else:                      # 前驱是 Cat 的回合
                # Cat 只要能让 Mouse 输（即后继是 LOSE），就会选这条
                if cur_state == LOSE:
                    status[pre] = LOSE
                    q.append(pre)
                else:                  # 当前后继是 WIN，Cat 仍需找其他能让 Mouse 输的
                    outdeg[pre] -= 1
                    if outdeg[pre] == 0:   # 所有后继都是 WIN → 对 Mouse 来说是输
                        status[pre] = WIN
                        q.append(pre)

    # ------------------- 7. 查询初始状态 -------------------
    start_id = encode(cat_start[0], cat_start[1],
                      mouse_start[0], mouse_start[1],
                      0)                     # Mouse 先手
    return status[start_id] == WIN

# -------------------------------------------------
# 示例测试
if __name__ == "__main__":
    g1 = ["####F", "#C...", "M...."]
    print(canMouseWin(g1, 1, 2))   # True

    g2 = ["M.C...F"]
    print(canMouseWin(g2, 1, 4))   # True

    g3 = ["M.C...F"]
    print(canMouseWin(g3, 1, 3))   # False
```

#### 复杂度  

- **时间复杂度**：`O( (R*C)^2 * (catJump+mouseJump) )`  
  - 解释：我们遍历每一种可能的状态（最多约 8k），对每个状态枚举所有合法的走法（每方向最多 `jump` 步），总工作量与状态数线性相关，远远快于指数级的递归。  
- **空间复杂度**：`O( (R*C)^2 )`  
  - 解释：需要保存 `status`、`outdeg` 两个大小为状态数的数组，以及逆向边的列表 `prev`（每条边最多出现一次），总体约几千个整数，轻松放进内存。

---

## 心得  

- **核心技巧**：**逆向拓扑（retrograde analysis） + 状态图 + 出度计数**。  
  把「谁能必胜」的判断从「往前搜索」改成「从已知的必输/必赢状态往回推」，一次遍历即可得到所有局面的结果。  

- **适用的题型**  
  1. **棋盘/格子游戏** 中的「先手必胜」判定，如 LeetCode 913 *猫鼠游戏*。  
  2. **Nim、取石子** 等 **博弈论** 题目，常用**状态 DP + 逆向 BFS**。  
  3. **带有回合限制** 的「逃脱/追捕」类问题（如「逃离迷宫」）  

- **一句话总结解题钥匙**：  
  > **先把所有「显然赢」或「显然输」的局面标记出来，再逆向传播，让每个状态都知道「对手会怎样选」从而判定自己是赢还是输。**

---

## 反思  

- **第一反应**：直接写递归暴力搜索，想把所有可能的走法都列举出来。  
- **最容易踩的坑**  
  1. **无限循环**：游戏可能在没有人达到终止条件时一直循环，需要在模型里加入「步数上限」或通过逆向分析把未被标记的状态视为输。  
  2. **状态重复**：没有记忆化会导致指数级爆炸。  
  3. **前驱构造错误**：逆向边必须对应「上一回合」的玩家位置不变，容易写反。  
  4. **出度计数**：忘记在处理 `WIN`/`LOSE` 时更新前驱的 `outdeg`，导致无法正确判断「所有后继都是 X」的情况。  

- **下次遇到同类题**，第一步应该：  
  > **先把所有「已经确定输赢」的局面列出来（比如到达终点、被抓住等），把它们放进队列，随后用逆向 BFS 按「谁的回合」逐层推断其余状态的胜负。**  

这样既能避免递归的重复计算，又能在合理的时间内得到答案。祝你玩得开心！