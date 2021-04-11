# #1293. 网格中消除障碍的最短路径 / Shortest Path in a Grid with Obstacles Elimination

> 难度：困难 · 标签：Array、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid where each cell is either 0 (empty) or 1 (obstacle). You can move up, down, left, or right from and to an empty cell in one step.
Return the minimum number of steps to walk from the upper left corner (0, 0) to the lower right corner (m - 1, n - 1) given that you can eliminate at most k obstacles. If it is not possible to find such walk return -1.

**Examples**

**Example 1:**

```
Input: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1
Output: 6
Explanation: 
The shortest path without eliminating any obstacle is 10.
The shortest path with one obstacle elimination at position (3,2) is 6. Such path is (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (3,2) -> (4,2).
```

**Example 2:**

```
Input: grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1
Output: -1
Explanation: We need to eliminate at least two obstacles to find such a walk.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 40
- 1 <= k <= m * n
- grid[i][j] is either 0 or 1.
- grid[0][0] == grid[m - 1][n - 1] == 0

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m x n` 的整数矩阵 `grid`（网格），其中每个单元格的值要么是 `0`（空），要么是 `1`（obstacle，障碍）。你可以在一次 `step`（步）中向上、向下、向左或向右移动到相邻的空单元格。  
返回从左上角 `(0, 0)` 到右下角 `(m - 1, n - 1)` 所需的最少步数，前提是你最多可以消除 `k` 个障碍。如果不存在满足条件的路径，返回 `-1`。

**示例**

*示例 1*  
```
输入: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1
输出: 6
解释:
不消除任何障碍的最短路径长度为 10。  
在位置 `(3,2)` 消除一个障碍后，最短路径长度为 6，路径为  
(0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (3,2) -> (4,2)。
```

*示例 2*  
```
输入: grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1
输出: -1
解释: 至少需要消除两个障碍才能找到可行的路径。
```

**约束条件**
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 40`
- `1 <= k <= m * n`
- `grid[i][j]` 只能是 `0` 或 `1`
- `grid[0][0] == grid[m - 1][n - 1] == 0`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的走法都枚举一遍**，只要走到右下角就记录走的步数，最后取最小值。  
可以用递归（深度优先搜索）从起点 `(0,0)` 开始，每一步尝试向上、下、左、右四个方向前进：

1. 若下一格是 `0`（空地），直接走进去。  
2. 若下一格是 `1`（障碍），检查当前还能否再消除障碍（`k` 是否大于 `0`），如果可以，就把它当作空地走进去，同时把 `k` 减 1。  
3. 为了防止走回头路，需要记录已经走过的格子（用 `visited` 集合），走完后要把记录撤销（回溯），这样才能尝试其他分支。  

这相当于把整个网格看成一棵**无限大的树**，每条树枝代表一次移动。只要遍历完整棵树，就一定能找到所有合法路径，从而得到最短的那条。

> **类比**：想象你在一座迷宫里，每次可以把最多 `k` 面墙敲掉。暴力解就是把所有可能的“拆墙+走路”组合都试一遍，就像把所有可能的钥匙（不同的拆墙次数）都插进去尝试打开每一扇门。

**为什么它是正确的**  
因为递归会穷举**每一种**合法的走法（只要不超过 `k` 次拆墙），不遗漏任何可能的路径，最短路径一定会出现在这些遍历的结果里。

**时间/空间复杂度**  
- 时间复杂度：在最坏情况下，每个格子都有 4 条出路，且每走一步都可能选择是否拆墙。于是递归的分支数大约是 `4^(m*n)`，也就是指数级的，**非常慢**。  
- 空间复杂度：递归栈的深度最多是网格格子数 `m*n`，再加上 `visited` 集合的大小，也是 `O(m*n)`。

> **大白话**：`O(4^(m*n))` 就像把一个 5 层楼的每层 4 种选择都列出来，数量会爆炸到天文数字，根本跑不完。

#### 代码（Python）

```python
from typing import List

def shortestPath_bruteforce(grid: List[List[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    # 四个方向向量
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    best = float('inf')          # 记录最短步数

    def dfs(x: int, y: int, remain: int, steps: int, visited: set):
        nonlocal best
        # 已经比当前最优更糟，直接剪枝
        if steps >= best:
            return
        # 到达终点，更新最短步数
        if x == m-1 and y == n-1:
            best = min(best, steps)
            return
        # 遍历四个相邻格子
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in visited:
                # 需要消除障碍吗？
                if grid[nx][ny] == 1:
                    if remain > 0:               # 还能拆墙
                        visited.add((nx, ny))
                        dfs(nx, ny, remain-1, steps+1, visited)
                        visited.remove((nx, ny))
                else:  # 空地直接走
                    visited.add((nx, ny))
                    dfs(nx, ny, remain, steps+1, visited)
                    visited.remove((nx, ny))

    # 起点已经在路径里
    dfs(0, 0, k, 0, {(0, 0)})
    return -1 if best == float('inf') else best
```

#### 复杂度  

- **时间复杂度**：`O(4^(m*n))` —— 递归会尝试每一种可能的走法，步数随网格大小指数增长。  
- **空间复杂度**：`O(m*n)` —— 递归栈深度和 `visited` 集合最多占用全部格子。  

---

### 2. 最优解  

#### 思路  

从暴力解我们已经知道**搜索**是必须的，但**盲目枚举**导致指数级爆炸。  
要想快，就必须利用**“最短路径一定是先到达的那条”**这一特性——这正是**广度优先搜索（BFS）**的核心思想：  

*BFS 每次从起点向外“一层层”扩散，第一次碰到终点的路径一定是最短的。*  

但是这里有一个额外的维度——**还能剩余多少次障碍消除**。  
如果只把坐标 `(x, y)` 当作状态，可能会把“已经用了 2 次消除”和“用了 0 次消除”这两种情况误认为是同一个状态，从而错过更优的路径。  

**关键点**：把 **“当前位置 + 还能剩余的消除次数”** 视为完整的状态，即 `(x, y, remain)`。  
- `x, y`：当前格子坐标。  
- `remain`：从起点走到这里还剩多少次可以消除障碍。  

我们在 BFS 队列中存放这些三元组，并且用一个三维布尔数组 `visited[x][y][remain]` 记录是否已经到达过该状态，防止重复搜索。  

**搜索过程**：

1. 初始化队列 `deque([(0,0,k,0)])`，其中 `0` 是已经走的步数。  
2. 取出队首 `(x,y,remain,steps)`，如果是终点返回 `steps`。  
3. 向四个方向尝试移动：  
   - 若下一个格子是空 (`0`) 并且该状态未访问过，直接入队 `(nx,ny,remain,steps+1)`。  
   - 若是障碍 (`1`) 且 `remain > 0`，则可以消除障碍，入队 `(nx,ny,remain-1,steps+1)`。  
4. 循环直到队列空，若仍未到达终点返回 `-1`。  

> **类比**：想象你在玩一个带有“炸弹”道具的迷宫游戏。每次你在某个格子时，手里还剩多少炸弹决定了以后还能否炸掉墙。于是你记录的不仅是“我在哪”，还有“我手里还有几颗炸弹”。只要把这两件事一起记下来，搜索就不会走回头路。

**为什么 BFS 能保证最短**  
因为每一次出队的节点都是**步数最少**的（队列是先进先出），当我们第一次弹出终点时，已经是所有可能路径中走的步数最少的那条。加入 `remain` 维度并不会改变这一点，只是把“同一个坐标但剩余炸弹不同”视作不同的层级。

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortestPath(grid: List[List[int]], k: int) -> int:
    """
    BFS + 三维 visited，时间 O(m * n * k)，空间 O(m * n * k)
    """
    m, n = len(grid), len(grid[0])
    # 方向向量：下、上、右、左
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # visited[x][y][r] 表示是否已经以“剩余 r 次消除”到达过 (x,y)
    visited = [[[False] * (k+1) for _ in range(n)] for _ in range(m)]
    q = deque()
    # (x, y, remain, steps)
    q.append((0, 0, k, 0))
    visited[0][0][k] = True

    while q:
        x, y, remain, steps = q.popleft()
        # 到达右下角，直接返回步数
        if x == m-1 and y == n-1:
            return steps

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 越界直接跳过
            if not (0 <= nx < m and 0 <= ny < n):
                continue

            nr = remain - grid[nx][ny]   # 如果是障碍，消除一次；空地则不变
            if nr < 0:                    # 已经没有剩余的消除次数
                continue
            # 若该状态未访问过，才入队
            if not visited[nx][ny][nr]:
                visited[nx][ny][nr] = True
                q.append((nx, ny, nr, steps + 1))

    # 队列空了仍未到达终点，说明无解
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m * n * k)`  
  - 每个格子最多会被访问 `k+1` 次（不同的剩余消除次数），每次检查四个方向，整体是线性乘以 `k`。  
  - 与暴力解的指数级相比，这已经是**多项式**时间，能在题目给出的 `m,n ≤ 40`、`k ≤ m*n` 的范围内轻松跑完。  

- **空间复杂度**：`O(m * n * k)`  
  - `visited` 三维数组需要保存每个格子在每种剩余次数下的访问情况，队列最多也会存这么多状态。  

> **对比**：暴力解的 `4^(m*n)` 相当于“天文数字”，最优解的 `m*n*k` 只相当于“几千到几万”，差距天壤之别。

---

## 心得  

- **核心技巧**：在 BFS 中把“还能剩余多少次障碍消除”当作额外的状态维度（**三元组**），并使用三维 `visited` 防止重复。  
- **适用的题型**  
  1. **带有限制资源的最短路**（如 LeetCode 1293 “Shortest Path in a Grid with Obstacles Elimination” 本题）。  
  2. **带有“钥匙/门”或“能量消耗”限制的网格搜索**（如 “Minimum Obstacles to Remove to Reach Corner”）。  
  3. **在图中同时考虑距离和费用的最短路**（如 “Minimum Cost to Reach Destination”），思路相同：把费用作为状态维度。  
- **一句话总结解题钥匙**：**把所有会影响后续选择的因素（坐标 + 资源剩余）一起放进 BFS 的状态中**。

---

## 反思  

- **第一反应**：看到“最短步数”立刻想到 BFS，看到“可以消除至多 k 个障碍”就想到要在状态里记录剩余的消除次数。  
- **最容易踩的坑**  
  1. **只用二维 visited**：会把不同剩余次数的状态误认为相同，导致错误的剪枝，进而得到非最优或错误答案。  
  2. **忘记对障碍格子检查 `remain > 0`**：直接走进去会出现负数剩余次数的非法状态。  
  3. **边界条件**：起点或终点本身是障碍（题目保证为 `0`，但如果忘记检查会出错）。  
- **下次类似题的第一步**：先明确“最短路径” → 用 BFS；再列出**所有会影响后续决策的变量**（如剩余炸弹、钥匙数量、能量等），把它们加入 BFS 的状态。这样即可构造出既保证最短又不遗漏的搜索。