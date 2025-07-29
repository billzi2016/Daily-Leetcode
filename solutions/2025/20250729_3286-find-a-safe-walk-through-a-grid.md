# #3286. 在网格中寻找安全路径 / Find a Safe Walk Through a Grid

> 难度：中等 · 标签：Array、Breadth-First Search、Graph、Heap (Priority Queue)、Matrix、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/find-a-safe-walk-through-a-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid and an integer health.
You start on the upper-left corner (0, 0) and would like to get to the lower-right corner (m - 1, n - 1).
You can move up, down, left, or right from one cell to another adjacent cell as long as your health remains positive.
Cells (i, j) with grid[i][j] = 1 are considered unsafe and reduce your health by 1.
Return true if you can reach the final cell with a health value of 1 or more, and false otherwise.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]], health = 1
Output: true
Explanation:
The final cell can be reached safely by walking along the gray cells below.
```

**Example 2:**

```
Input: grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3
Output: false
Explanation:
A minimum of 4 health points is needed to reach the final cell safely.
```

**Example 3:**

```
Input: grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5
Output: true
Explanation:
The final cell can be reached safely by walking along the gray cells below.

Any path that does not go through the cell (1, 1) is unsafe since your health will drop to 0 when reaching the final cell.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- 2 <= m * n
- 1 <= health <= m + n
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

**描述**  
给定一个 `m x n` 二进制矩阵 (binary matrix) `grid` 和一个整数 `health`。  
你从左上角 `(0, 0)` 开始，想要到达右下角 `(m - 1, n - 1)`。  
只要你的生命值保持为正数，就可以向上、向下、向左或向右移动到相邻单元格 (adjacent cell)。  

矩阵中 `grid[i][j] = 1` 的单元格被视为不安全的 (unsafe)，进入此类单元格会使你的生命值减少 `1`。  
如果你能够以 **生命值 ≥ 1** 到达终点单元格，则返回 `true`；否则返回 `false`。

**示例 1**  
```text
Input: grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]], health = 1
Output: true
```
**解释**：  
通过沿下图的灰色单元格行走，可以安全到达终点。

**示例 2**  
```text
Input: grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3
Output: false
```
**解释**：  
安全到达终点至少需要 `4` 点生命值，因此在 `health = 3` 时无法完成。

**示例 3**  
```text
Input: grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5
Output: true
```
**解释**：  
沿下图的灰色单元格行走即可安全到达终点。  
任何不经过单元格 `(1, 1)` 的路径都是不安全的，因为在抵达终点时生命值会降至 `0`。

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 50`  
- `2 <= m * n`  
- `1 <= health <= m + n`  
- `grid[i][j]` 仅为 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举一遍**，只要找到一条从左上角走到右下角且途中血量不掉到 0 以下的路径，就返回 `True`。  
实现上可以使用 **深度优先搜索（DFS）** 或 **普通的宽度优先搜索（BFS）**：

1. 从 `(0,0)` 出发，记录当前剩余血量 `hp`（初始为 `health`）。  
2. 每次可以向上、下、左、右四个方向走一步，只要新坐标在矩阵范围内且 `hp > 0`。  
3. 走进一个格子后，如果 `grid[i][j] == 1`（不安全格子），就把 `hp` 减 1；否则血量不变。  
4. 用一个 `visited` 集合记录已经到达过的 `(i, j, hp)` 状态，防止在同一个格子用相同或更少血量重复搜索，避免无限循环。  
5. 当搜索到右下角且 `hp >= 1` 时，说明找到安全路径，返回 `True`。  
6. 所有搜索分支都耗尽仍未成功，则返回 `False`。

> **类比**：把矩阵想成一张城市地图，`grid[i][j]=1` 的格子像是有“陷阱”的街道，走进去会让你的体力（血量）掉 1。我们要找一条从起点到终点的“体力不掉光”的路线。

**为什么正确**  
只要遍历了所有合法的走法，就一定会覆盖所有可能的路径。如果有一条满足血量要求的路径，搜索必然会在某个分支中发现它；如果没有，则所有分支都被穷尽，返回 `False`。  

**时间/空间复杂度**  
- **时间复杂度**：最坏情况每个格子都可以以不同的血量状态被访问。血量上限为 `health ≤ m+n ≤ 100`（因为 `m,n ≤ 50`），所以状态数最多是 `O(m·n·health)`，但在暴力实现里我们往往不做血量剪枝，只是单纯记 `visited` 为坐标，这会导致 **指数级** 的搜索：`O(4^{(m·n)})`（每一步有最多 4 种选择），实际会超时。  
- **空间复杂度**：递归栈（或队列）最深可能是所有格子数 `m·n`，再加上 `visited` 集合的大小，同样是 **指数级**（最坏 `O(4^{(m·n)})`），在实际运行中会因为剪枝而稍好，但仍然不可接受。

> **大白话**：`O(4^{(m·n)})` 就像在一个十字路口每走一步都有 4 条路可选，走完 100 步就有 `4^100` 种可能——天文数字，电脑根本算不完。

#### 代码（Python）

```python
from collections import deque

def canReach_bruteforce(grid, health):
    """
    暴力 BFS（不做 0-1 权重优化），返回是否存在安全路径
    """
    m, n = len(grid), len(grid[0])
    # 四个方向：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 队列里保存 (i, j, 剩余血量)
    q = deque()
    q.append((0, 0, health))

    # visited 记录已经到达过的 (i, j, hp) 防止循环
    visited = set()
    visited.add((0, 0, health))

    while q:
        i, j, hp = q.popleft()
        # 到达终点且血量仍然 >= 1
        if i == m - 1 and j == n - 1 and hp >= 1:
            return True

        for di, dj in dirs:
            ni, nj = i + di, j + dj
            # 坐标必须在矩阵内部
            if 0 <= ni < m and 0 <= nj < n:
                nhp = hp - grid[ni][nj]   # 若是危险格子 (1) 则血量减 1
                if nhp <= 0:              # 血量不够，不能继续前进
                    continue
                state = (ni, nj, nhp)
                if state not in visited:
                    visited.add(state)
                    q.append(state)
    return False
```

#### 复杂度

- **时间复杂度**：`O(4^{(m·n)})`（指数级），因为每一步最多有 4 条分支，所有路径都要尝试。  
- **空间复杂度**：`O(4^{(m·n)})`，主要是队列和 `visited` 中保存的状态数，同样是指数级。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于我们把每一步都当作等价的代价来搜索，而实际上**格子是否危险决定了血量的消耗**。  
- 走进安全格子 (`grid[i][j] == 0`) **不消耗血量**，相当于“费用为 0”。  
- 走进危险格子 (`grid[i][j] == 1`) **消耗 1 点血量**，相当于“费用为 1”。  

这正好对应 **01 权重最短路** 的场景：图的每条边权只有 `0` 或 `1`。  
在这种情况下，**01 BFS**（使用双端队列）可以在 `O(V + E)` 的时间内得到最小费用路径，而不需要像 Dijkstra 那样使用堆。

**关键点**：

1. 把每个格子视为图的一个节点，四个相邻格子之间有一条有向边。  
2. 边的权重 = 目的格子的 `grid` 值（0 或 1）。  
3. 用 **双端队列 `deque`** 保存待访问的节点：
   - 若边权为 `0`（安全格子），把新节点 **放到队首**（优先处理）。  
   - 若边权为 `1`（危险格子），把新节点 **放到队尾**（稍后处理）。  
4. 维护一个二维数组 `dist[i][j]`，记录从起点到 `(i,j)` 需要消耗的最少血量（即走过的危险格子数）。  
5. 初始化 `dist[0][0] = grid[0][0]`（起点若是危险格子也要扣血），把 `(0,0)` 放入队首。  
6. 取出队首节点 `(i,j)`，尝试四个方向的邻居 `(ni,nj)`，计算新的消耗 `new_cost = dist[i][j] + grid[ni][nj]`。  
   - 若 `new_cost < dist[ni][nj]`，说明找到更省血的方式，就更新 `dist` 并根据权重把节点加入队首或队尾。  
7. BFS 结束后，`dist[m-1][n-1]` 就是到达终点**最少需要扣多少血**。  
8. 最终只要 `health - dist[m-1][n-1] >= 1`（即剩余血量≥1），返回 `True`，否则 `False`。

> **类比**：把每条路想成「是否有陷阱」的标记，走没有陷阱的路我们立刻走（放在队首），走有陷阱的路只能等后面再走（放在队尾）。这样我们总是先尝试“最省血”的路线。

#### 代码（Python）

```python
from collections import deque
from typing import List

def canReach(grid: List[List[int]], health: int) -> bool:
    """
    01 BFS 求从左上到右下最少经过多少个危险格子（即最少扣血量）。
    若最少扣血量 <= health-1，则可以安全到达。
    """
    m, n = len(grid), len(grid[0])
    # 四个方向
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # dist[i][j] 表示到达 (i,j) 最少扣血量（走过多少个 1）
    INF = 10**9
    dist = [[INF] * n for _ in range(m)]

    # 起点需要扣除自身的危险值
    dist[0][0] = grid[0][0]
    dq = deque()
    dq.appendleft((0, 0))   # 权重为 0 时放队首，权重为 1 时放队尾

    while dq:
        i, j = dq.popleft()
        # 若已经到达终点且当前消耗已经不大于已知最优，可提前结束
        if i == m - 1 and j == n - 1:
            # 仍然继续遍历也可以，只是这里提前返回更快
            break
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                # 走到 (ni,nj) 需要额外扣掉它的危险值
                w = grid[ni][nj]          # 0 或 1
                new_cost = dist[i][j] + w
                if new_cost < dist[ni][nj]:
                    dist[ni][nj] = new_cost
                    if w == 0:
                        dq.appendleft((ni, nj))   # 费用为 0，优先处理
                    else:
                        dq.append((ni, nj))        # 费用为 1，稍后处理

    # 最少扣血量
    min_loss = dist[m - 1][n - 1]
    # 需要保证剩余血量 >= 1
    return health - min_loss >= 1
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 每个格子最多被弹出队列一次（因为 0‑1 BFS 保证一旦最短距离确定就不会再更新），四个方向的检查是常数时间。  
  - 与暴力的指数级搜索相比，线性遍历整个矩阵，快得多。  

- **空间复杂度**：`O(m·n)`  
  - `dist` 数组保存每个格子的最小扣血量，大小正好是矩阵本身。  
  - 队列最多也只会同时存放 O(m·n) 个节点。

> 与暴力解相比，时间从 **指数级** 降到 **线性级**，空间也从 **指数级** 降到 **矩阵大小**，因此在所有合法输入下都能轻松通过。

---

## 心得

- **核心技巧**：**01 BFS**（双端队列实现的最短路），适用于**权重只有 0 或 1** 的图。  
- **适用的类似题型**  
  1. “最少翻转 0/1 矩阵中的障碍物”  
  2. “在网格中最少消除障碍物到达终点”  
  3. “最短路径带有 0/1 权重的迷宫”  
- **一句话总结**：把“走危险格子扣血”看成 **边权 1**，把“走安全格子不扣血”看成 **边权 0**，用 01 BFS 把“最省血的路线”直接算出来。

---

## 反思

- **第一反应**：直接用 DFS/BFS 把所有路径遍历一遍，看到血量就剪枝。  
- **最容易踩的坑**  
  - **血量剪枝不够**：只记录坐标而不记录血量会导致错误的剪枝，导致漏掉可行路径。  
  - **起点本身是危险格子**：需要在初始化时把 `grid[0][0]` 的血量消耗算进去。  
  - **边界条件**：矩阵只有一行或一列时，仍需正确处理四个方向的检查。  
- **下次类似题的第一步**：先判断是否可以把每一步的“代价”抽象为 0/1 权重，若可以，就立刻想到 **01 BFS**（或 Dijkstra 的堆实现）来求最小代价。