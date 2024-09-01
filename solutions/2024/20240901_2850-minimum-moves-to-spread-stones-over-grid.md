# #2850. 最少移动次数以在网格上分布石子 / Minimum Moves to Spread Stones Over Grid

> 难度：中等 · 标签：Array、Dynamic Programming、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-spread-stones-over-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer matrix grid of size 3 * 3, representing the number of stones in each cell. The grid contains exactly 9 stones, and there can be multiple stones in a single cell.
In one move, you can move a single stone from its current cell to any other cell if the two cells share a side.
Return the minimum number of moves required to place one stone in each cell.

**Examples**

**Example 1:**

```
Input: grid = [[1,1,0],[1,1,1],[1,2,1]]
Output: 3
Explanation: One possible sequence of moves to place one stone in each cell is: 
1- Move one stone from cell (2,1) to cell (2,2).
2- Move one stone from cell (2,2) to cell (1,2).
3- Move one stone from cell (1,2) to cell (0,2).
In total, it takes 3 moves to place one stone in each cell of the grid.
It can be shown that 3 is the minimum number of moves required to place one stone in each cell.
```

**Example 2:**

```
Input: grid = [[1,3,0],[1,0,0],[1,0,3]]
Output: 4
Explanation: One possible sequence of moves to place one stone in each cell is:
1- Move one stone from cell (0,1) to cell (0,2).
2- Move one stone from cell (0,1) to cell (1,1).
3- Move one stone from cell (2,2) to cell (1,2).
4- Move one stone from cell (2,2) to cell (2,1).
In total, it takes 4 moves to place one stone in each cell of the grid.
It can be shown that 4 is the minimum number of moves required to place one stone in each cell.
```

**Constraints**

- grid.length == grid[i].length == 3
- 0 <= grid[i][j] <= 9
- Sum of grid is equal to 9.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的 $3 \times 3$ 整数矩阵 `grid`，`grid[i][j]` 表示该单元格中的石子数量。矩阵中恰好有 9 颗石子，单元格可以容纳多个石子。  
一次移动中，你可以将一颗石子从当前单元格移动到与其共享一条边的任意相邻单元格。  
返回使每个单元格恰好拥有一颗石子所需的最小移动次数。

**示例 1**  
```
Input: grid = [[1,1,0],[1,1,1],[1,2,1]]
Output: 3
Explanation: 一种可能的移动序列如下：
1. 将位于单元格 (2,1) 的一颗石子移动到单元格 (2,2)。
2. 将位于单元格 (2,2) 的一颗石子移动到单元格 (1,2)。
3. 将位于单元格 (1,2) 的一颗石子移动到单元格 (0,2)。
共计 3 次移动即可使每个单元格恰好有一颗石子。可以证明 3 是最小的移动次数。
```

**示例 2**  
```
Input: grid = [[1,3,0],[1,0,0],[1,0,3]]
Output: 4
Explanation: 一种可能的移动序列如下：
1. 将位于单元格 (0,1) 的一颗石子移动到单元格 (0,2)。
2. 将位于单元格 (0,1) 的另一颗石子移动到单元格 (1,1)。
3. 将位于单元格 (2,2) 的一颗石子移动到单元格 (1,2)。
4. 将位于单元格 (2,2) 的另一颗石子移动到单元格 (2,1)。
共计 4 次移动即可使每个单元格恰好有一颗石子。
```

**约束条件**  
- `grid.length == grid[i].length == 3`  
- `0 <= grid[i][j] <= 9`  
- `grid` 中所有元素的和恰好等于 9.

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个棋盘当成一个**状态图**，每一次移动石子都产生一个新状态。  
- **状态**：把 3×3 的矩阵拉平成长度为 9 的数组，例如 `grid = [[1,1,0],[1,1,1],[1,2,1]]` 可以写成 `[1,1,0,1,1,1,1,2,1]`。只要保证这 9 个数之和为 9，就是合法状态。  
- **邻接**：从一个状态出发，任选一个拥有 **≥2** 颗石子的格子 `(r,c)`，把其中一颗石子搬到它的 **上下左右** 四个相邻格子中的任意一个 `(nr,nc)`（只要在棋盘内部），得到一个新状态。一次搬动算 **1 步**。  

把所有状态和它们之间的「一步可达」关系想象成一张大图（类似城市地图），我们要找的就是 **从起始状态到目标状态的最短路径**。  
这正好可以用 **广度优先搜索（BFS）** 来解决——BFS 保证第一次到达目标时所走的步数最少。

> 类比：  
> - 哈希表就像一本电话簿，`key` 是人的姓名，`value` 是电话号码。这里我们用哈希表记录「已经访问过的状态」——防止在地图里走回头路。  
> - 队列（queue）像排队买咖啡的队伍，最先进入的状态最先被展开，保证层层递进。

**为什么正确**  
BFS 按层展开：先遍历所有「0 步」能到达的状态（只有起始状态），再遍历所有「1 步」能到达的状态，依此类推。当我们第一次看到「每个格子恰好 1 颗石子」的状态时，必然是使用最少步数得到的，因为任何更少步数的路径已经在前面的层里检查过了。

**复杂度分析（大白话）**  
- **状态总数**：把 9 颗石子放进 9 格子，每格可以放 0~9 颗，但总数固定为 9。组合数是  
  \[
  \binom{9+9-1}{9}= \binom{17}{9}=24310
  \]  
  所以最多只有约 **2.4 万** 种不同的状态。  
- **每个状态的出度**：最多 9 格子里挑出一格搬走一颗石子，再挑 4 个方向中的一个。最坏情况下大约是 `9 * 4 = 36` 条边。  
- **时间复杂度**：遍历所有状态一次 → **O(状态数 × 出度) ≈ O(2.4w × 36) ≈ O(10⁵)**，在本题完全可以接受。  
- **空间复杂度**：需要存放已经访问过的状态集合和 BFS 队列，最坏也只会保存所有状态 → **O(状态数) ≈ O(2.4w)**。

> 用 O(10⁵) 表示「十万次操作」，这在 Python 里几毫秒就能跑完。

#### 代码（Python）

```python
from collections import deque

def minMoves_bruteforce(grid):
    # ---------- 把二维矩阵压平成一维元组，便于哈希 ----------
    start = tuple(grid[i][j] for i in range(3) for j in range(3))
    target = (1,) * 9                         # 目标状态：每格恰好 1 颗

    # ---------- BFS ----------
    q = deque()
    q.append((start, 0))                      # (当前状态, 已走步数)
    seen = {start}                            # 已访问集合，防止重复

    # 方向向量：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        state, step = q.popleft()
        if state == target:                   # 第一次遇到目标，即最少步数
            return step

        # 把一维恢复成二维坐标，方便遍历相邻格子
        board = [list(state[i*3:(i+1)*3]) for i in range(3)]

        for r in range(3):
            for c in range(3):
                if board[r][c] >= 2:          # 只能从「多余」的格子搬石子
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 3 and 0 <= nc < 3:
                            # ---------- 生成新状态 ----------
                            board[r][c] -= 1
                            board[nr][nc] += 1
                            new_state = tuple(board[i][j] for i in range(3) for j in range(3))
                            # ---------- 入队 ----------
                            if new_state not in seen:
                                seen.add(new_state)
                                q.append((new_state, step + 1))
                            # ---------- 恢复现场 ----------
                            board[r][c] += 1
                            board[nr][nc] -= 1
    return -1   # 按题意不会出现
```

#### 复杂度

- **时间复杂度**：`O(状态总数 × 每状态的出度) ≈ O(10⁵)`  
  > 大约十万次「尝试搬石子」的操作，完全可以在毫秒级完成。

- **空间复杂度**：`O(状态总数) ≈ O(2.4 × 10⁴)`  
  > 只需要存几个十几万的整数，内存占用几百 KB。

---

### 2. 最优解

#### 思路  

虽然 BFS 已经能 AC，但我们可以 **利用题目给出的额外信息**，把问题压缩到只需要考虑 **空格子** 与 **多余石子** 的匹配，直接算出最小步数，而不必遍历所有状态。

1. **观察**  
   - 最终每格恰好 1 颗石子。  
   - 对于一个格子，若当前有 `cnt` 颗石子：  
     - `cnt == 1` → 已经正好，**不需要** 处理。  
     - `cnt > 1` → 多出 `cnt-1` 颗石子，称为 **“多余石子”**。  
     - `cnt == 0` → 没有石子，称为 **“空格子”**。  
   - 因为总石子数是 9，**多余石子数 = 空格子数**。设为 `k`。  
   - 提示说 `k ≤ 4`（最多只有 4 个格子是空的或多余的），所以 `k` 很小。

2. **每一步搬动的代价**  
   - 把一颗石子从格子 `A` 移动到相邻格子 `B`，步数加 1。  
   - 若把石子从 `A` 直接搬到 `C`（不相邻），最少需要走 **曼哈顿距离** `|Ax-Cx| + |Ay-Cy|` 步，因为每走一步只能往上下左右其中一个方向前进一步。  
   - 因此，如果我们决定「哪颗多余石子搬到哪个空格子」，最小步数就是两点的曼哈顿距离。

3. **匹配问题**  
   - 把所有 **多余石子**（把每颗多余石子都看成独立的个体）列成左边集合 `S`，把所有 **空格子** 列成右边集合 `E`。  
   - 对每对 `(s, e)`，计算代价 `cost(s, e) = Manhattan(s, e)`。  
   - 我们要在 `S` 与 `E` 之间找一一对应，使总代价最小，这正是 **最小费用完美匹配**（又叫 **Assignment Problem**）。  
   - 由于 `k ≤ 4`，我们可以直接 **枚举全排列**：把空格子顺序排列，然后让第 `i` 个空格子对应第 `i` 个多余石子，求和；取最小值即可。枚举的次数是 `k!`（最多 4! = 24），非常小。

4. **算法步骤**  

   1. 遍历整个 3×3 棋盘，收集  
      - `extra = []`：若格子有 `cnt > 1`，向列表中加入 `(r, c)` **`cnt-1` 次**（每颗多余石子一个坐标）。  
      - `empty = []`：若格子为 `0`，向列表中加入 `(r, c)`。  
   2. `k = len(extra) = len(empty)`（题目保证相等）。  
   3. 对 `empty` 的所有排列 `perm`（`itertools.permutations`），计算  
      `total = sum( manhattan(extra[i], perm[i]) for i in range(k) )`。  
   4. 最小的 `total` 即为答案。

5. **为什么不需要 BFS**  

   - 每颗石子走的路径只影响它自己到达目标格子的距离，石子之间不会互相阻塞（因为我们可以把石子先搬到中转格子再继续搬，总代价仍等于曼哈顿距离）。  
   - 所以只要把「谁搬到哪里」定下来，最少步数就唯一确定为曼哈顿距离之和。  
   - 这把原本的「状态搜索」压缩成了「小规模匹配」——时间更快，代码更简洁。

#### 代码（Python）

```python
import itertools

def minMoves_optimal(grid):
    extra = []   # 每颗多余石子的坐标，可能出现重复
    empty = []   # 每个空格子的坐标

    # 收集信息
    for r in range(3):
        for c in range(3):
            cnt = grid[r][c]
            if cnt > 1:
                # 多出 cnt-1 颗石子，每颗都单独记一个坐标
                extra.extend([(r, c)] * (cnt - 1))
            elif cnt == 0:
                empty.append((r, c))

    k = len(extra)               # 多余石子数量，也是空格子数量
    if k == 0:                   # 已经全部均匀分布
        return 0

    # 曼哈顿距离函数（两点之间最短的格子步数）
    def manhattan(p, q):
        return abs(p[0] - q[0]) + abs(p[1] - q[1])

    best = float('inf')
    # 对空格子全排列，尝试每一种对应关系
    for perm in itertools.permutations(empty, k):
        total = 0
        for i in range(k):
            total += manhattan(extra[i], perm[i])
            # 提前剪枝：已经超过当前最优，就不必继续累加
            if total >= best:
                break
        best = min(best, total)

    return best
```

#### 复杂度

- **时间复杂度**：  
  - 收集 `extra` 与 `empty`：`O(9)`（常数）。  
  - 枚举所有排列：`k!` 种，每种计算 `k` 次曼哈顿距离 → `O(k! * k)`。  
  - 由于 `k ≤ 4`，最坏是 `4! * 4 = 96` 次基本运算，**可视为 O(1)**（常数级），远快于 BFS。  

- **空间复杂度**：  
  - 只存 `extra`、`empty`、以及一次排列的临时列表，最多 `2k ≤ 8` 个坐标 → **O(k) = O(1)**。  

> 与暴力 BFS 相比，时间从「十万级」降到「百级」，空间也从几万条记录降到几条，效率提升数千倍。

---

## 心得

- **核心技巧**：把「每颗石子搬到空格子」抽象为 **最小费用匹配**，利用 **曼哈顿距离** 直接计步。  
- **适用场景**：  
  1. **网格上多余/缺失元素配对**（如「最小移动次数使棋盘每行每列都满足条件」）。  
  2. **机器人搬运**、**物流调度** 中的「最短总路程」问题。  
  3. **分配任务** 给固定数量的工人，使总耗时最小（同样是 Assignment Problem）。  
- **一句话总结**：**把石子视为独立的“货物”，空格子是“目的地”，最少步数等价于最小总曼哈顿距离的完美匹配**。

---

## 反思

- **第一反应**：直接想到 BFS，想把每一次搬动当成图的边，搜索最短路径。  
- **最容易踩的坑**：  
  - **状态表示错误**：忘记把二维矩阵压平成不可变的元组，导致哈希集合失效。  
  - **边界遗漏**：移动时没有检查是否越界，或者把石子从只有 1 颗的格子搬走导致负数。  
  - **多余石子计数**：把一个格子里多出的多颗石子当成一次搬动，实际上每颗石子都需要单独移动。  
- **下次类似题**：第一步先 **统计“多余”和“缺失”** 的格子数量，若数量很小就考虑 **匹配/排列** 的暴力/枚举方案；若数量大则再回到 BFS/DP 等更通用的搜索方法。