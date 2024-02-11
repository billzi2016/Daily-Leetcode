# #2577. 最小访问网格单元的时间 / Minimum Time to Visit a Cell In a Grid

> 难度：困难 · 标签：Array、Breadth-First Search、Graph、Heap (Priority Queue)、Matrix、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-visit-a-cell-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a m x n matrix grid consisting of non-negative integers where grid[row][col] represents the minimum time required to be able to visit the cell (row, col), which means you can visit the cell (row, col) only when the time you visit it is greater than or equal to grid[row][col].
You are standing in the top-left cell of the matrix in the 0th second, and you must move to any adjacent cell in the four directions: up, down, left, and right. Each move you make takes 1 second.
Return the minimum time required in which you can visit the bottom-right cell of the matrix. If you cannot visit the bottom-right cell, then return -1.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,3,2],[5,1,2,5],[4,3,8,6]]
Output: 7
Explanation: One of the paths that we can take is the following:
- at t = 0, we are on the cell (0,0).
- at t = 1, we move to the cell (0,1). It is possible because grid[0][1] <= 1.
- at t = 2, we move to the cell (1,1). It is possible because grid[1][1] <= 2.
- at t = 3, we move to the cell (1,2). It is possible because grid[1][2] <= 3.
- at t = 4, we move to the cell (1,1). It is possible because grid[1][1] <= 4.
- at t = 5, we move to the cell (1,2). It is possible because grid[1][2] <= 5.
- at t = 6, we move to the cell (1,3). It is possible because grid[1][3] <= 6.
- at t = 7, we move to the cell (2,3). It is possible because grid[2][3] <= 7.
The final time is 7. It can be shown that it is the minimum time possible.
```

**Example 2:**

```
Input: grid = [[0,2,4],[3,2,1],[1,0,4]]
Output: -1
Explanation: There is no path from the top left to the bottom-right cell.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 2 <= m, n <= 1000
- 4 <= m * n <= 105
- 0 <= grid[i][j] <= 105
- grid[0][0] == 0

---

## 题目（中文翻译）

给定一个 `m x n` 矩阵 `grid`，其中 `grid[row][col]` 表示访问单元格 `(row, col)` 所需的最小时间，也就是说只有当你访问该单元格的时刻 **≥** `grid[row][col]` 时才可以进入该单元格。  

你从矩阵的左上角单元格 `(0, 0)` 的第 `0` 秒开始，每次可以向四个方向中的任意一个相邻单元格移动：上、下、左、右。每移动一步耗时 `1` 秒。  

返回能够到达矩阵右下角单元格的最小时间。如果无法到达右下角单元格，则返回 `-1`。

**示例 1**  

**输入**  
``` 
grid = [[0,1,3,2],
        [5,1,2,5],
        [4,3,8,6]]
```  

**输出**  
```
7
```  

**解释**  
以下是一条可行路径的时间演示：

- `t = 0` 时，位于单元格 `(0,0)`。  
- `t = 1` 时，移动到单元格 `(0,1)`。因为 `grid[0][1] = 1 ≤ 1`，可以进入。  
- `t = 2` 时，移动到单元格 `(1,1)`。因为 `grid[1][1] = 1 ≤ 2`，可以进入。  
- `t = 3` 时，移动到单元格 `(1,2)`。因为 `grid[1][2] = 2 ≤ 3`，可以进入。  
- `t = 4` 时，移动到单元格 `(0,2)`。因为 `grid[0][2] = 3 ≤ 4`，可以进入。  
- `t = 5` 时，移动到单元格 `(0,3)`。因为 `grid[0][3] = 2 ≤ 5`，可以进入。  
- `t = 6` 时，移动到单元格 `(1,3)`。因为 `grid[1][3] = 5 ≤ 6`，可以进入。  
- `t = 7` 时，移动到单元格 `(2,3)`（右下角），此时满足 `grid[2][3] = 6 ≤ 7`，完成访问。  

因此最小所需时间为 `7`。

**示例 2**  

**输入**  
``` 
grid = [[0,2,4],
        [3,2,1],
        [1,0,4]]
```  

**输出**  
```
-1
```  

**解释**  
不存在从左上角到右下角的可行路径，故返回 `-1`。

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `2 <= m, n <= 1000`
- `4 <= m * n <= 10^5`
- `0 <= grid[i][j] <= 10^5`
- `grid[0][0] == 0`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个网格当成 **棋盘**，我们每走一步就把时间 +1。  
从左上角 `(0,0)` 出发，使用 **广度优先搜索 (BFS)** 按时间层层展开：

1. 当前所在的格子记为 `(x, y)`，当前的时间记为 `t`。  
2. 同时检查四个相邻格子 `(nx, ny)`，如果 `t + 1 >= grid[nx][ny]`（即下个格子的限制已经满足），就把 `(nx, ny, t+1)` 放进队列继续搜索。  
3. 为了防止重复访问，需要记录 **已经到达过的状态**。这里的状态不仅仅是格子坐标，还要记住到达时的时间，因为同一个格子在不同时间可能会有不同的后续选择。于是我们用集合 `visited = {(x, y, t)}`。

如果队列里出现了右下角 `(m‑1, n‑1)`，说明已经找到了通路，返回对应的时间；如果队列耗尽仍未到达，则返回 `-1`。

> **生活化类比**：  
> 想象你在一个只能往前走的迷宫里，每走一步都要花 1 秒。如果前面有一道门需要等到特定时间才会打开，你只能等（继续走别的路再回来），所以我们把“等”也写进了搜索的每一步。

#### 代码（Python）

```python
from collections import deque
from typing import List, Tuple, Set

def minimumTime_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # 队列里保存 (x, y, 当前时间)
    q = deque()
    q.append((0, 0, 0))
    # visited 记录已经遍历过的 (x, y, 时间) 防止无限循环
    visited: Set[Tuple[int, int, int]] = {(0, 0, 0)}
    # 四个方向向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y, t = q.popleft()
        # 到达右下角，返回答案
        if x == m - 1 and y == n - 1:
            return t

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 越界直接跳过
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            nt = t + 1                         # 移动一步后时间+1
            # 只有当下个格子的限制 <= 到达时间时才能进入
            if nt >= grid[nx][ny]:
                state = (nx, ny, nt)
                if state not in visited:
                    visited.add(state)
                    q.append(state)
    # 队列空了仍未到达右下角，说明不可达
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m * n * T)`，其中 `T` 是可能出现的最大时间。最坏情况下我们会把每个格子在每个时间点都放进队列，时间会随 `grid` 中的数值线性增长，实际会非常慢（比如 `T` 可能达到 `10^5`），因此这不是可接受的做法。  
- **空间复杂度**：同样是 `O(m * n * T)`，因为 `visited` 需要保存每个格子在每个时间的访问记录。  

> 用大白话解释：如果把网格想象成一座城堡，暴力 BFS 相当于把城堡里的每一个房间在每一秒都记录一次进出情况，城堡再大、时间再长，记录的条目就会爆炸式增长，导致程序卡死。

---

### 2. 最优解

#### 思路  

暴力 BFS 太慢的根本原因是 **每次只考虑“走一步”**，而没有利用 **路径权值** 的信息。  
这里我们把网格看成一个 **有向加权图**：

- 每个格子是一个节点。  
- 从节点 `A` 到相邻节点 `B` 有一条边，**走这条边的代价**不是固定的 1，而是 **“最早能够到达 B 的时间”**。

为什么会出现这种代价？  
设我们在格子 `A` 的时间是 `t`，想要走向格子 `B`（其限制为 `grid[B]`）：

1. **直接前进**：如果 `t + 1 >= grid[B]`，我们只需要 1 秒就能到达，代价是 `t + 1`。  
2. **需要等待**：如果 `t + 1 < grid[B]`，我们必须等到时间至少为 `grid[B]` 才能进入。  
   - 这里的“等”只能通过 **来回走动** 实现（题目没有说可以原地等待），一次往返需要 2 秒，意味着我们只能把时间 **以 2 为步长** 增加。  
   - 因此到达 `B` 的最早时间是  
     ```text
     next_time = max(grid[B], t + 1)            # 先把时间提升到足够大
     if (next_time - t) % 2 == 1:               # 如果差是奇数，说明只能通过再走一次来回
         next_time += 1                         # 再加 1 秒，使差变成偶数（即多走一次来回）
     ```
   - 这段公式保证我们既满足 `grid[B]` 的限制，又满足只能通过 **偶数秒** 的来回来“等待”。

把每条边的 **代价** 视为「从当前时间出发后，最早能够到达对方的时间」，整个问题就转化为 **单源最短路径**：  
从左上角出发，找出到右下角的最小「到达时间」。

**Dijkstra 算法** 正好可以在加权图中求最短路径，且使用 **优先队列（最小堆）** 可以把每次扩展的代价保持在 `O(log(mn))`。

核心步骤如下：

1. 初始化 `dist` 数组，`dist[x][y]` 表示到达 `(x,y)` 的最小时间，全部设为无穷大，`dist[0][0] = 0`。  
2. 把起点 `(0,0,0)` 放入最小堆。  
3. 每次弹出堆顶 `(t, x, y)`（当前已知的最早到达时间），如果已经不是最优值则跳过。  
4. 对四个相邻格子计算 `next_time`（上面公式），如果 `next_time < dist[nx][ny]`，就更新并把新状态压入堆。  
5. 当弹出的节点是右下角时，即可返回对应的时间；若堆空仍未到达，则返回 `-1`。

> **生活化类比**：  
> 把每个格子想象成一座城市，城市之间有道路。道路的“行驶时间”取决于两座城市的开门时间以及只能“来回绕路”来等的规则。我们使用导航系统（Dijkstra）一次次挑选“当前最快可以到达的城市”，逐步扩展，最终得到到达终点的最短时间。

#### 代码（Python）

```python
import heapq
from typing import List

def minimumTime(grid: List[List[int]]) -> int:
    """
    Dijkstra + 等待奇偶校正
    返回从左上到右下的最小到达时间，若不可达返回 -1
    """
    m, n = len(grid), len(grid[0])
    # 四个方向
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # dist[x][y] 保存到达 (x,y) 的最小时间，初始为无穷大
    INF = 10 ** 18
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0

    # 优先队列，元素为 (当前时间, x, y)
    heap = [(0, 0, 0)]

    while heap:
        t, x, y = heapq.heappop(heap)
        # 如果已经不是最优的时间，直接跳过
        if t != dist[x][y]:
            continue
        # 到达终点，直接返回答案
        if x == m - 1 and y == n - 1:
            return t

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < m and 0 <= ny < n):
                continue

            # 计算走到 (nx, ny) 的最早时间
            # 1. 必须至少比当前时间多 1 秒（因为要走一步）
            # 2. 还要满足网格的限制
            nxt = max(grid[nx][ny], t + 1)

            # 等待只能通过来回走动实现，只能把时间以 2 为步长增加
            # 因此如果 nxt 与 t 的差是奇数，需要再加 1 秒使其成为偶数
            if (nxt - t) % 2 == 1:
                nxt += 1

            # 松弛（更新最短路）
            if nxt < dist[nx][ny]:
                dist[nx][ny] = nxt
                heapq.heappush(heap, (nxt, nx, ny))

    # 堆空仍未到达右下角，说明不可达
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m * n * log(m * n))`  
  - 每个格子最多会被弹出堆一次（因为我们只在发现更小的时间时才会重新入堆），堆操作的代价是 `log(mn)`。  
  - 与暴力解相比，**不再和时间上限成正比**，即使网格很大（`10^5` 个格子），也能在几秒内跑完。  

- **空间复杂度**：`O(m * n)`  
  - 需要存 `dist` 数组以及堆里最多 `mn` 条记录。  
  - 相比暴力解的 `O(m * n * T)`，大幅降低了内存消耗。

---

## 心得  

- **核心技巧**：把“每个格子只能在满足时间限制后才能进入”转化为 **带权图的边权**，并使用 **Dijkstra** 求最短路径。  
- **适用的题型**（类似思路）  
  1. “Minimum Cost to Reach Destination” 系列——网格中每格有进入费用，需要最小化总费用。  
  2. “Path With Minimum Effort”——路径的代价是相邻格子高度差的最大值，使用二分 + BFS 或 Dijkstra。  
  3. “Swim in Rising Water”——水位随时间升高，需要在水位足够时才能进入格子，同样可以用 Dijkstra。  
- **一句话总结解题钥匙**：**把时间限制包装成“最早可达时间”，在图上跑最短路**。

---

## 反思  

- **第一反应**：看到“每走一步需要 1 秒，格子有最小时间限制”，立刻想到 BFS 按层搜索。  
- **最容易踩的坑**  
  1. **忘记等待的奇偶性**：因为只能通过来回走动来“等待”，导致到达时间与当前时间的差必须是偶数。忽略这点会得到错误的答案（时间偏小）。  
  2. **边界条件**：起点 `grid[0][0]` 必须是 0，否则一开始就不可行。  
  3. **大规模输入**：直接把每个时间点都记下来会导致 **内存爆炸**，一定要用 `dist` 只记录最小时间。  
- **下次遇到同类题**：第一步先思考 **“能否把每一步的可行性映射成一条带权边”**，如果可以，就立刻考虑 **Dijkstra / 最短路** 而不是裸 BFS。这样既能保证正确性，又能避免时间/空间超限。