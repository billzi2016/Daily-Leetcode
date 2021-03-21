# #1263. 将箱子移动到目标位置的最少推箱次数 / Minimum Moves to Move a Box to Their Target Location

> 难度：困难 · 标签：Array、Breadth-First Search、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-move-a-box-to-their-target-location/)

---

## 题目（英文原版）

**Description**

A storekeeper is a game in which the player pushes boxes around in a warehouse trying to get them to target locations.
The game is represented by an m x n grid of characters grid where each element is a wall, floor, or box.
Your task is to move the box 'B' to the target position 'T' under the following rules:
Return the minimum number of pushes to move the box to the target. If there is no way to reach the target, return -1.

**Examples**

**Example 1:**

```
Input: grid = [["#","#","#","#","#","#"],
               ["#","T","#","#","#","#"],
               ["#",".",".","B",".","#"],
               ["#",".","#","#",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]
Output: 3
Explanation: We return only the number of times the box is pushed.
```

**Example 2:**

```
Input: grid = [["#","#","#","#","#","#"],
               ["#","T","#","#","#","#"],
               ["#",".",".","B",".","#"],
               ["#","#","#","#",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]
Output: -1
```

**Example 3:**

```
Input: grid = [["#","#","#","#","#","#"],
               ["#","T",".",".","#","#"],
               ["#",".","#","B",".","#"],
               ["#",".",".",".",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]
Output: 5
Explanation: push the box down, left, left, up and up.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 20
- grid contains only characters '.', '#', 'S', 'T', or 'B'.
- There is only one character 'S', 'B', and 'T' in the grid.

---

## 题目（中文翻译）

**描述**  
店长（storekeeper）是一款玩家在仓库中推动箱子（box）以将其送达目标位置（target）的游戏。  
游戏场景由一个 `m × n` 的字符网格（grid）表示，网格中的每个元素可能是墙壁（wall）、地板（floor）或箱子（box）。  

你的任务是按照以下规则，将箱子 `'B'` 移动到目标位置 `'T'`：  
- 玩家只能向相邻的四个方向（上、下、左、右）移动。  
- 当玩家站在箱子旁边且箱子前方的格子为空地（`'.'`）时，玩家可以推动箱子向前移动一格。  
- 推动箱子一次算作一次推箱操作（push），玩家的普通移动不计数。  

返回将箱子推到目标位置所需的最少推箱次数。如果无法到达目标，返回 `-1`。

**示例**  

示例 1:
```text
Input: grid = [["#","#","#","#","#","#"],
               ["#","T","#","#","#","#"],
               ["#",".",".","B",".","#"],
               ["#",".","#","#",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]
Output: 3
Explanation: 只统计箱子被推动的次数，共需要 3 次。
```

示例 2:
```text
Input: grid = [["#","#","#","#","#","#"],
               ["#","T","#","#","#","#"],
               ["#",".",".","B",".","#"],
               ["#","#","#","#",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]
Output: -1
```

示例 3:
```text
Input: grid = [["#","#","#","#","#","#"],
               ["#","T",".",".","#","#"],
               ["#",".","#","B",".","#"],
               ["#",".",".",".",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]
Output: 5
Explanation: 推动箱子的顺序为下、左、左、上、上，共 5 次。
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 ≤ m, n ≤ 20`  
- `grid` 只包含字符 `'.'`、`'#'`、`'S'`、`'T'` 或 `'B'`。  
- 网格中恰好只有一个玩家 `'S'`、一个箱子 `'B'` 和一个目标 `'T'`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **“玩家所在位置 + 箱子所在位置”** 当作一个整体状态来搜索。  
我们把每一次 **玩家走一步** 都记作一次状态转移：

1. 玩家可以向四个方向走一步，只要目标格子不是墙 `#`。  
2. 如果玩家想走进箱子所在的格子，而箱子后面还有一个空格（不是墙），那么玩家会把箱子一起推过去，这时 **推箱子次数 +1**。  

把所有可能的 `(player_row, player_col, box_row, box_col)` 放进 **队列**，用 **广度优先搜索（BFS）** 按层遍历，第一次碰到箱子坐标等于目标 `T` 时返回当前的推箱子次数。

> **类比**：  
> - **哈希表**（`visited`）就像一本“走过的记录本”，`key` 是四元组 `(pr, pc, br, bc)`，`value` 是已经走过的次数，防止我们在同样的四元组上兜圈子。  
> - **队列** 像排队等候的队伍，先进去的先出来，保证我们按最少步数层层展开。

**为什么一定能得到答案**  
BFS 按层展开，先访问的状态拥有最少的 **玩家走步数**，而我们在每次 **推箱子** 时额外记录一次 `push_cnt`，所以第一次到达目标箱子位置的记录一定是最少推箱子次数。

**复杂度分析（大白话）**  
- 网格最大 20×20，格子总数 `M = m·n ≤ 400`。  
- 每个状态由玩家位置和箱子位置共同决定，最多有 `M·M`（约 160 000）种组合。  
- 对每个状态我们会尝试 4 个方向，整体时间大约是 `4·M·M` → **O((mn)²)**。  
- 需要把所有状态存进哈希表，空间同样是 **O((mn)²)**。  

> **O((mn)²)** 可以想象成 “把 400 个格子两两配对”，数量级已经不少了，尤其在 Python 中会有明显的慢。

#### 代码（Python）

```python
from collections import deque

def minPushBox(grid):
    m, n = len(grid), len(grid[0])

    # 找到玩家、箱子、目标的坐标
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S': start = (i, j)
            if grid[i][j] == 'B': box   = (i, j)
            if grid[i][j] == 'T': target = (i, j)

    # 四个方向向量
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # visited[(pr, pc, br, bc)] = True 表示这个四元组已经遍历过
    visited = set()
    visited.add((*start, *box))

    # 队列里存 (玩家行, 玩家列, 箱子行, 箱子列, 已经推的次数)
    q = deque()
    q.append((*start, *box, 0))

    while q:
        pr, pc, br, bc, pushes = q.popleft()

        # 如果箱子已经在目标格子，返回推的次数
        if (br, bc) == target:
            return pushes

        # 玩家可以向四个方向尝试走一步
        for dr, dc in dirs:
            npr, npc = pr + dr, pc + dc               # 玩家下一步位置
            if not (0 <= npr < m and 0 <= npc < n):   # 越界
                continue
            if grid[npr][npc] == '#':                 # 墙，不能走
                continue

            # 情况 1：玩家走到空地，箱子不动
            if (npr, npc) != (br, bc):
                state = (npr, npc, br, bc)
                if state not in visited:
                    visited.add(state)
                    q.append((npr, npc, br, bc, pushes))
                continue

            # 情况 2：玩家想往箱子所在格子走，这相当于推箱子
            nbr, nbc = br + dr, bc + dc               # 箱子被推后的位置
            if not (0 <= nbr < m and 0 <= nbc < n):   # 推出边界
                continue
            if grid[nbr][nbc] == '#':                 # 推进墙里
                continue

            state = (npr, npc, nbr, nbc)               # 推完后的新状态
            if state not in visited:
                visited.add(state)
                # 推箱子一次，pushes + 1
                q.append((npr, npc, nbr, nbc, pushes + 1))

    # BFS 结束仍未到达目标，说明不可达
    return -1
```

#### 复杂度  

- **时间复杂度**：`O((m·n)²)`  
  > 想象把 400 格子两两配对，最多有 160 000 种状态，每个状态检查 4 条边。  
- **空间复杂度**：`O((m·n)²)`  
  > 需要把所有四元组放进 `visited` 集合，最坏情况下也要记住这么多状态。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于我们把 **玩家每一步的移动** 也当作搜索的层级，导致状态空间膨胀到 `(玩家位置, 箱子位置)` 的笛卡尔积。  
实际上，**题目只要求统计推箱子的次数**，玩家在两次推之间可以随意走来走去，只要能站到“推箱子所需的那一格”。  

**优化思路**：  
1. **把搜索的粒度提升到“箱子的位置”**。每一次状态转移代表一次 **推箱子**，而不是玩家的普通走步。  
2. 对于当前箱子所在的格子 `B`，我们枚举四个可能的推的方向 `d`（上、下、左、右）。  
   - 推向 `d` 前，需要玩家站在箱子 **相反方向** 的格子 `P = B - d`（即玩家要站在箱子后面）。  
   - 同时箱子被推到的格子 `B' = B + d` 必须是可通行的（不是墙）。  
3. 检查玩家是否能够 **从当前玩家位置**（上一层的状态记录）**走到 `P`**，而不碰到墙或箱子。这个子问题恰好是 **普通的最短路径 BFS**（在固定的障碍格子中寻找玩家能否到达 `P`）。  
4. 若玩家能够到达 `P`，则这一次推是合法的，产生新状态 `(B', P')`，其中 `P'` 实际上就是 **箱子被推后玩家站的位置**（也就是 `B`），因为玩家在推完后会站在箱子原来的格子。  
5. 对所有合法的推，使用 **普通 BFS（或 0‑1 BFS）** 按层展开，层数即为推箱子的次数。  

**核心算法**：  
- **外层 BFS**：在 **箱子坐标** 的状态空间中搜索，每条边的代价都是 `1`（一次推）。  
- **内层 BFS**：判断玩家能否从当前玩家位置走到指定的“准备推的格子”。这一步只涉及 **普通的网格遍历**，不计入推的次数。  

**为什么更快**  
- 外层状态只有 `m·n`（箱子可能所在的格子） ≤ 400，远小于 `(m·n)²`。  
- 每次扩展时只做一次内层 BFS，复杂度为 `O(m·n)`，整体时间 `O((m·n)²)`，但常数更小，实际运行快很多。  

> **类比**：把箱子想成“棋子”，玩家是“指挥官”。我们不在意指挥官每一步的细枝末节，只关心每次把棋子搬动一次的指令是否可行——先让指挥官跑到指令起点，然后下达搬动。

#### 代码（Python）

```python
from collections import deque

def minPushBox(grid):
    m, n = len(grid), len(grid[0])

    # 找到 S、B、T 的坐标
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S': start_player = (i, j)
            if grid[i][j] == 'B': start_box = (i, j)
            if grid[i][j] == 'T': target = (i, j)

    # 四个方向
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # ---------- 辅助函数：玩家是否能从 (sr,sc) 走到 (tr,tc) ----------
    def player_can_reach(sr, sc, tr, tc, box_r, box_c):
        """在箱子固定在 (box_r,box_c) 的情况下，判断玩家能否到达 (tr,tc)"""
        if (tr, tc) == (box_r, box_c):  # 目标格子被箱子占了，显然不可达
            return False
        q = deque()
        q.append((sr, sc))
        seen = {(sr, sc)}
        while q:
            r, c = q.popleft()
            if (r, c) == (tr, tc):
                return True
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n \
                        and (nr, nc) not in seen \
                        and grid[nr][nc] != '#' \
                        and (nr, nc) != (box_r, box_c):
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return False
    # -----------------------------------------------------------------

    # 外层 BFS：状态是 (box_row, box_col, player_row, player_col)
    # 只记录箱子的位置，玩家位置只在每层中用来做起点
    visited = set()
    visited.add((start_box[0], start_box[1], start_player[0], start_player[1]))
    q = deque()
    q.append((start_box[0], start_box[1], start_player[0], start_player[1], 0))

    while q:
        br, bc, pr, pc, pushes = q.popleft()
        if (br, bc) == target:          # 箱子已经到达目标
            return pushes

        # 尝试四个方向推箱子
        for dr, dc in dirs:
            nbr, nbc = br + dr, bc + dc          # 推完后箱子的新位置
            pr_needed, pc_needed = br - dr, bc - dc   # 玩家必须站的位置

            # 检查新位置是否合法
            if not (0 <= nbr < m and 0 <= nbc < n):
                continue                # 推出边界
            if grid[nbr][nbc] == '#':
                continue                # 推进墙里

            # 检查玩家是否能到达准备推的格子
            if not player_can_reach(pr, pc, pr_needed, pc_needed, br, bc):
                continue                # 玩家走不到，不能推

            state = (nbr, nbc, br, bc)  # 推完后玩家站在箱子原来的格子
            if state not in visited:
                visited.add(state)
                q.append((nbr, nbc, br, bc, pushes + 1))

    return -1
```

> **代码要点解释**  
> 1. `player_can_reach` 使用普通 BFS，**不把箱子当障碍**（因为箱子已经固定在 `(box_r, box_c)`），只要不走墙。  
> 2. 外层 BFS 每一次扩展只产生至多 4 条新状态，因为每个方向最多一次合法推。  
> 3. `visited` 同时记录箱子和玩家的位置，防止在同样的箱子位置、玩家不同站点重复搜索（实际可以只记箱子位置，但记录玩家位置更安全，仍然在约束范围内）。

#### 复杂度  

- **时间复杂度**：`O((m·n)²)`  
  - 外层最多遍历 `m·n` 个箱子位置。  
  - 每次扩展要跑一次 **玩家可达性 BFS**，时间 `O(m·n)`。  
  - 所以总体 `O((m·n) * (m·n))`，即 `O((m·n)²)`。  
  - 与暴力解的时间量级相同，但常数更小，实际运行快很多。  

- **空间复杂度**：`O(m·n)`  
  - `visited` 只需要记录箱子+玩家的组合，最多 `≈ (m·n)²`，但在本实现里因为每次推后玩家必站在箱子原位置，实际状态数约为 `m·n`。  
  - BFS 队列和临时 `seen` 集合也都是格子数级别。  

---

## 心得  

- **核心技巧**：**把“只计数的动作”抽象为图的边权**，利用 **BFS（或 0‑1 BFS）** 在状态空间上层层展开，同时把“辅助移动”抽象为子问题的可达性检查。  
- **适用的题型**  
  1. **推箱子类**（Sokoban）——如本题、LeetCode 1263 “Minimum Moves to Move a Box to Their Target Location”。  
  2. **机器人搬运**——需要在网格里搬动物体，计数的是搬运次数而非机器人步数。  
  3. **带权 BFS**——只关心某类特殊操作次数（如翻转、开关）时，可把普通移动视作权重 `0`，特殊操作视作权重 `1`（0‑1 BFS）。  
- **一句话总结解题钥匙**：**把“推箱子”当作唯一的状态转移，玩家的普通走动只用来验证转移是否合法**。

---

## 反思  

- **第一反应**：看到“只计数推的次数”，本能想把玩家每一步都放进搜索，结果导致状态爆炸。  
- **最容易踩的坑**  
  1. **忘记把箱子当障碍**：在判断玩家能否到达准备推的格子时，必须把当前箱子位置视作不可踏入的格子。  
  2. **边界条件**：推箱子后新位置或玩家站位可能超出网格，需要先检查 `0 ≤ r < m, 0 ≤ c < n`。  
  3. **重复状态**：只记录箱子位置可能导致玩家在同一箱子位置但不同站点反复搜索，记得在 `visited` 中加入玩家坐标（或使用更精细的判重策略）。  
- **下次类似题目第一步**：**先把计数的关键动作抽象成图的边**，问自己：“我到底要统计哪一种操作？其他所有动作是否可以在子问题里快速验证？” 这样就能直接构造最小状态空间，避免不必要的暴力搜索。