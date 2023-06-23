# #2290. 到达右下角的最少障碍移除次数 / Minimum Obstacle Removal to Reach Corner

> 难度：困难 · 标签：Array、Breadth-First Search、Graph、Heap (Priority Queue)、Matrix、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array grid of size m x n. Each cell has one of two values:
You can move up, down, left, or right from and to an empty cell.
Return the minimum number of obstacles to remove so you can move from the upper left corner (0, 0) to the lower right corner (m - 1, n - 1).

**Examples**

**Example 1:**

```
Input: grid = [[0,1,1],[1,1,0],[1,1,0]]
Output: 2
Explanation: We can remove the obstacles at (0, 1) and (0, 2) to create a path from (0, 0) to (2, 2).
It can be shown that we need to remove at least 2 obstacles, so we return 2.
Note that there may be other ways to remove 2 obstacles to create a path.
```

**Example 2:**

```
Input: grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]
Output: 0
Explanation: We can move from (0, 0) to (2, 4) without removing any obstacles, so we return 0.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 105
- 2 <= m * n <= 105
- grid[i][j] is either 0 or 1.
- grid[0][0] == grid[m - 1][n - 1] == 0

---

## 题目（中文翻译）

给定一个下标从 0 开始的二维整数数组（2D integer array）`grid`，大小为 `m x n`。每个格子只能取两种值：

- `0` 表示空格子（empty cell）；
- `1` 表示障碍物（obstacle）。

你可以向上、向下、向左、向右移动到相邻的空格子。返回为了能够从左上角 `(0, 0)` 移动到右下角 `(m - 1, n - 1)`，最少需要移除多少个障碍物。

---

### 示例

**示例 1**  
输入: `grid = [[0,1,1],[1,1,0],[1,1,0]]`  
输出: `2`  
解释: 我们可以移除 `(0, 1)` 和 `(0, 2)` 处的障碍物，使得从 `(0, 0)` 到 `(2, 2)` 形成一条通路。可以证明至少需要移除 2 个障碍物，因此返回 `2`。  
注意，也可能存在其他移除 2 个障碍物的方案。

**示例 2**  
输入: `grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]`  
输出: `0`  
解释: 我们可以在不移除任何障碍物的情况下，从 `(0, 0)` 移动到 `(2, 4)`，所以返回 `0`。

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10^5`
- `2 <= m * n <= 10^5`
- `grid[i][j]` 只能是 `0` 或 `1`
- `grid[0][0] == grid[m - 1][n - 1] == 0`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的走法都穷举一遍**，找出能从左上角走到右下角的路径，然后在这些路径里挑最少需要拆除障碍物的那条。  
这相当于在二维网格上做一次「全遍历」：

1. 从 `(0,0)` 开始，向上、下、左、右四个方向递归搜索。  
2. 每走到一个格子，就记录已经拆除的障碍数量（如果格子本身是 `1`，就要「拆」一次）。  
3. 当到达终点 `(m-1,n-1)` 时，比较当前的拆除次数和全局最小值，取更小的。  

> **类比**：想象你在一座迷宫里，墙壁（`1`）可以用锤子敲开，但每敲一次都要花时间。暴力解相当于把所有可能的「锤子使用顺序」都尝试一次，找出最省力的那条路。

**为什么它是正确的？**  
因为我们把「所有」合法走法都遍历了一遍，必然会包含最优解所在的那条路径。只要记录每条路径的拆墙次数，取最小值自然就是答案。

#### 代码（Python）

```python
from typing import List

def min_obstacle_removal_brute(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # 用一个全局变量保存最小拆墙次数
    best = [float('inf')]
    # 记录已经访问过的格子，防止原路返回形成死循环
    visited = [[False] * n for _ in range(m)]

    def dfs(x: int, y: int, removed: int) -> None:
        # 已经比当前最优更差，剪枝
        if removed >= best[0]:
            return
        # 到达右下角，更新最优解
        if x == m - 1 and y == n - 1:
            best[0] = min(best[0], removed)
            return
        # 四个方向移动
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                visited[nx][ny] = True
                # 如果下一个格子是障碍，需要额外拆除一次
                dfs(nx, ny, removed + grid[nx][ny])
                visited[nx][ny] = False   # 回溯，恢复现场

    visited[0][0] = True
    dfs(0, 0, 0)
    return best[0]
```

> 关键点注释（已在代码中）：  
> - `visited` 防止在同一次路径里原路返回导致无限递归。  
> - `removed + grid[nx][ny]` 利用 `grid` 中的 `0/1` 直接算出是否需要再拆一次墙。  
> - 当 `removed` 已经不可能比当前最优更小时，提前返回（剪枝），可以稍微降低指数级的搜索量。

#### 复杂度

- **时间复杂度**：`O(4^{m*n})`（指数级）  
  解释：每个格子最多有 4 条出路，最坏情况下会把所有可能的走法都遍历一次，数量随格子数指数增长。即使加上剪枝，也仍然是 **爆炸式** 的。

- **空间复杂度**：`O(m*n)`  
  解释：递归栈深度最坏会到达全部格子数，加上 `visited` 数组，需要与网格大小同量级的额外空间。

> 结论：暴力解只能用来验证思路或在极小的测试数据上跑通，实际题目规模（`m*n ≤ 10^5`）根本不可能用它。

---

### 2. 最优解

#### 思路  

**从暴力解的瓶颈说起**  
暴力解的慢点在于「把所有路径都尝试一遍」——我们并没有利用「拆墙的代价」信息来指引搜索方向。事实上，**每走一步的代价只有两种**：

- 移动到一个空格子（`0`）→ 代价 **0**  
- 移动到一个障碍格子（`1`）→ 代价 **1**（需要拆除一次障碍）

这正好可以把网格看成一张**加权无向图**：

- **节点**：每个格子 `(i, j)`  
- **边**：相邻的四个方向  
- **权重**：从当前格子到相邻格子的权重 = 相邻格子的值 (`0` 或 `1`)

于是我们要找的，就是 **从左上角到右下角的最短路径**（最小累计权重）。  
这类「权重只有 0 或 1」的最短路问题，有两个常用算法：

1. **Dijkstra**（最小堆）——适用于任意非负权重。  
2. **0-1 BFS**（双端队列）——专门针对权重只有 0 / 1 的情况，效率更高，代码更简洁。

下面我们详细解释 **0-1 BFS** 的工作原理，并给出完整实现。

---

##### 0-1 BFS 工作原理（从零开始解释）

1. **队列的特殊使用**  
   - 使用 **双端队列 `deque`**，它既可以在左侧 `appendleft`，也可以在右侧 `append`。  
   - 当我们沿一条 **代价为 0 的边** 前进时，意味着「这一步不增加拆墙次数」，我们希望尽快把这条路径的后续探索放在**前面**，所以把新坐标 **放到左侧**。  
   - 当我们沿一条 **代价为 1 的边** 前进时，需要额外拆墙，这一步相对「更贵」，我们把新坐标 **放到右侧**，让它稍后再处理。

2. **遍历顺序天然保证最小代价**  
   - `deque` 总是先弹出左侧的元素，也就是目前累计代价最小的路径所在的格子。  
   - 类似 Dijkstra 中「每次取最小距离的节点」的过程，只是这里用 `deque` 替代了堆，时间更快（因为只有两种权重）。

3. **记录已经到达每个格子的最小拆墙次数**  
   - 用 `dist[i][j]` 保存从起点到 `(i,j)` 的最小拆墙数。  
   - 当我们准备把一个新格子加入 `deque` 时，先检查是否已经有更小的 `dist`，如果有则跳过（防止重复扩展）。

4. **终止条件**  
   - 当弹出的格子是右下角 `(m-1,n-1)` 时，`dist` 已经是最小值，可以直接返回。

> **类比**：把 `deque` 想成一条“快递线”。免费快递（权重 0）直接放在前面，付费快递（权重 1）排在后面。快递员总是先送最前面的，确保最先送到的就是花费最少的。

---

#### 代码（Python）

```python
from collections import deque
from typing import List

def min_obstacle_removal(grid: List[List[int]]) -> int:
    """
    0-1 BFS 实现
    返回从左上角到右下角最少需要拆除的障碍数量
    """
    m, n = len(grid), len(grid[0])
    # 四个方向向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # dist 用来保存到每个格子的最小拆墙次数，初始化为无穷大
    INF = 10**9
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0

    dq = deque()
    dq.append((0, 0))               # 起点放入队列

    while dq:
        x, y = dq.popleft()         # 取出当前代价最小的格子

        # 已经到达右下角，直接返回答案
        if x == m - 1 and y == n - 1:
            return dist[x][y]

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n:
                # 通过 (nx,ny) 需要额外拆除的墙数
                w = grid[nx][ny]    # 0 或 1
                new_dist = dist[x][y] + w
                if new_dist < dist[nx][ny]:
                    dist[nx][ny] = new_dist
                    # 权重为 0 时放左侧，权重为 1 时放右侧
                    if w == 0:
                        dq.appendleft((nx, ny))
                    else:
                        dq.append((nx, ny))
    # 理论上永远不会走到这里，因为题目保证终点可达
    return -1
```

**代码要点解释（已在代码中加注）**：

- `dist` 相当于「每个格子到起点的最少拆墙次数」的记忆表。  
- `w = grid[nx][ny]` 直接利用格子值作为边权，省去额外的判断。  
- `if new_dist < dist[nx][ny]` 保证只在发现更优路径时才更新并加入队列，防止无限循环。  
- 当 `w == 0` 时使用 `appendleft`，保证零代价的路径先被处理，从而实现 **0‑1 BFS** 的核心思想。

---

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - 解释：每个格子最多被加入 `deque` 两次（一次通过权重 0，一次通过权重 1），总体线性遍历整个网格。相比 Dijkstra 的 `O(E log V)`（这里 `E≈4V`），0‑1 BFS 省去了堆的 `log` 开销。

- **空间复杂度**：`O(m * n)`  
  - 解释：`dist` 数组和 `deque` 最坏情况下都需要存放全部格子的信息，和网格大小同量级。

> 与暴力解对比：时间从指数级降到线性，几乎可以在 10⁵ 规模的网格上瞬间算出答案。

---

## 心得

- **核心技巧**：把「拆障碍」视作 **边的权重**（0 或 1），利用 **0‑1 BFS** 求最短路。  
- **适用场景**  
  1. **最少翻转路径**（如 LeetCode 1499. Max Value of Equation 中的「最少翻转」）  
  2. **最少变更路径**（如 1659. Maximize Grid Happiness 中的「最少更改」）  
  3. **网格中最少穿越障碍**（本题）  
- **一句话总结**：**把“是否需要拆墙”转化为“边的代价”，用 0‑1 BFS 按代价递增的顺序遍历，即可得到最少拆墙次数**。

---

## 反思

- **拿到题目第一反应**：把网格想成图，使用最短路算法。随后注意到权重只有 0/1，立刻想到 0‑1 BFS 可以把堆的 `log` 抹掉。  
- **最容易踩的坑**  
  1. **忘记对起点和终点是空格 (`0`) 的前提**，导致把起点的障碍计入答案。  
  2. **没有使用 `deque.appendleft`**，而是全部 `append`，这会退化成普通 BFS，得到的不是最小拆墙数。  
  3. **没有更新 `dist` 前就加入队列**，会产生重复访问，导致时间复杂度失控。  
- **下次遇到同类题**：第一步先检查「权重只有两种」——如果是，就立刻考虑 **0‑1 BFS**（或双端队列的 Dijkstra 变形），否则才使用普通的 Dijkstra 或 BFS。