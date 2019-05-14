# #417. **太平洋大西洋水流** / Pacific Atlantic Water Flow

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/pacific-atlantic-water-flow/)

---

## 题目（英文原版）

**Description**

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.
The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).
The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.
Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.

**Examples**

**Example 1:**

```
Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
Explanation: The following cells can flow to the Pacific and Atlantic oceans, as shown below:
[0,4]: [0,4] -> Pacific Ocean 
       [0,4] -> Atlantic Ocean
[1,3]: [1,3] -> [0,3] -> Pacific Ocean 
       [1,3] -> [1,4] -> Atlantic Ocean
[1,4]: [1,4] -> [1,3] -> [0,3] -> Pacific Ocean 
       [1,4] -> Atlantic Ocean
[2,2]: [2,2] -> [1,2] -> [0,2] -> Pacific Ocean 
       [2,2] -> [2,3] -> [2,4] -> Atlantic Ocean
[3,0]: [3,0] -> Pacific Ocean 
       [3,0] -> [4,0] -> Atlantic Ocean
[3,1]: [3,1] -> [3,0] -> Pacific Ocean 
       [3,1] -> [4,1] -> Atlantic Ocean
[4,0]: [4,0] -> Pacific Ocean 
       [4,0] -> Atlantic Ocean
Note that there are other possible paths for these cells to flow to the Pacific and Atlantic oceans.
```

**Example 2:**

```
Input: heights = [[1]]
Output: [[0,0]]
Explanation: The water can flow from the only cell to the Pacific and Atlantic oceans.
```

**Constraints**

- m == heights.length
- n == heights[r].length
- 1 <= m, n <= 200
- 0 <= heights[r][c] <= 105

---

## 题目（中文翻译）

岛屿是一个 `m × n` 的矩形，左边缘和上边缘与太平洋（Pacific Ocean）相邻，右边缘和下边缘与大西洋（Atlantic Ocean）相邻。  
岛屿被划分为若干正方形单元格。给定一个 `m × n` 的整数矩阵 `heights`，其中 `heights[r][c]` 表示坐标 `(r, c)` 处单元格的海拔高度。

岛屿会下大雨，雨水可以向北、南、东、西四个相邻方向流动，前提是相邻单元格的高度 **小于等于** 当前单元格的高度。雨水还能直接从与海洋相邻的单元格流入对应的海洋。

返回一个二维列表 `result`，其中 `result[i] = [ri, ci]` 表示雨水能够从单元格 `(ri, ci)` 同时流向太平洋和大西洋。

---

### 示例

**示例 1**

```
输入: heights = [[1,2,2,3,5],
                 [3,2,3,4,4],
                 [2,4,5,3,1],
                 [6,7,1,4,5],
                 [5,1,1,2,4]]
输出: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
解释: 以下单元格可以分别流向太平洋和大西洋，如图所示：
[0,4]: [0,4] → 太平洋  
      [0,4] → 大西洋
[1,3]: [1,3] → [0,3] → 太平洋  
      [1,3] → [1,4] → 大西洋
[1,4]: [1,4] → [1,3] → [0,3] → 太平洋  
      [1,4] → 大西洋
[2,2]: [2,2] → [1,2] → [0,2] → 太平洋  
      [2,2] → [2,3] → [2,4] → 大西洋
[3,0]: [3,0] → 太平洋  
      [3,0] → [4,0] → 大西洋
[3,1]: [3,1] → [3,0] → 太平洋  
      [3,1] → [4,1] → 大西洋
[4,0]: [4,0] → 太平洋  
      [4,0] → 大西洋
注意，这些单元格还有其他可能的流向路径。
```

**示例 2**

```
输入: heights = [[1]]
输出: [[0,0]]
解释: 唯一的单元格的水可以同时流向太平洋和大西洋。
```

---

### 约束条件

- `m == heights.length`
- `n == heights[r].length`
- `1 ≤ m, n ≤ 200`
- `0 ≤ heights[r][c] ≤ 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每一个格子都检查**：  
- 从该格子出发，能否沿着高度不升高的方向一直走到左边或上边（即太平洋）？  
- 再检查，能否走到右边或下边（即大西洋）？

这相当于从每个格子做一次 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）**，把能到达的所有格子记下来，只要搜索过程中碰到海岸边（对应的边界）就算成功。

> **类比**：把每个格子想象成一间房子，水是小球只能往不比自己高的房间滚动。我们要从每间房子出发，看看小球能否滚到左/上门口（太平洋）和右/下门口（大西洋）。

**为什么正确**  
DFS/BFS 能遍历所有满足“相邻格子高度 ≤ 当前格子高度”的路径，只要搜索能触及对应的海岸，就说明从该格子有一条合法的水流路径。

**时间/空间复杂度**  
- 对每个格子都要做一次搜索，搜索最坏会遍历整个矩阵 `m × n`。  
- 因此时间复杂度约为 `O(m·n·(m+n))`，可以粗略记成 **O(m²·n + m·n²)**，在最坏情况下接近 **O(m·n·(m+n))**。  
- 每次搜索需要一个 visited 集合来防止重复访问，空间复杂度为 `O(m·n)`（最坏情况下整个矩阵都会被标记）。

> **大白话**：如果矩阵是 200×200，暴力解大概要跑 200·200·(200+200)= 16 000 000 次遍历，已经很慢了。

#### 代码（Python）

```python
from collections import deque
from typing import List

def pacificAtlantic_bruteforce(heights: List[List[int]]) -> List[List[int]]:
    if not heights:
        return []
    m, n = len(heights), len(heights[0])
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # 判断从 (r,c) 能否到达海岸 ocean = 'pacific' / 'atlantic'
    def can_reach(r: int, c: int, ocean: str) -> bool:
        visited = [[False]*n for _ in range(m)]
        stack = [(r, c)]
        visited[r][c] = True

        while stack:
            x, y = stack.pop()
            # 到达对应海岸即成功
            if ocean == 'pacific' and (x == 0 or y == 0):
                return True
            if ocean == 'atlantic' and (x == m-1 or y == n-1):
                return True
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                    # 只能往不比自己高的方向流动
                    if heights[nx][ny] <= heights[x][y]:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
        return False

    res = []
    for i in range(m):
        for j in range(n):
            # 两边都能到达才加入答案
            if can_reach(i, j, 'pacific') and can_reach(i, j, 'atlantic'):
                res.append([i, j])
    return res
```

#### 复杂度

- **时间复杂度**：`O(m·n·(m+n))`  
  解释：每个格子都要进行一次完整的 DFS/BFS，最坏遍历整个矩阵，导致乘积级别的时间。
- **空间复杂度**：`O(m·n)`  
  解释：每次搜索都要保存一个 `visited` 矩阵，大小与原矩阵相同。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **从每个格子向外搜索**，导致大量重复遍历。  
实际上，水的流向是 **从高处向低处**，如果我们把搜索方向 **反过来**，从海岸向内“逆流”会更高效：

1. **从太平洋的边缘（第一行和第一列）出发**，只向**不低于当前格子**的相邻格子扩散。这样遍历得到的所有格子，恰好是**可以把水流向太平洋**的格子集合 `pacific_reachable`。  
2. 同理，从大西洋的边缘（最后一行和最后一列）出发，得到集合 `atlantic_reachable`。  
3. 两个集合的交集即为答案：同时能流向两边的格子。

> **类比**：想象海岸是两座高台，水只能往**不比自己低**的格子爬。我们把水倒着倒进海岸的“喷泉”，喷泉会往能“倒回去”的格子里流。所有被喷泉触及的格子，就是能把水送到海岸的格子。

**核心算法**：**多源 BFS/DFS**（从多个起点同时搜索），使用 **visited** 集合记录每个海岸能到达的格子。  
- BFS 用队列一次性展开层层扩散，代码更直观。  
- 也可以用 DFS 递归实现，这里采用 BFS。

**为什么正确**  
- 逆向搜索保证了只会进入 **高度不低于当前格子的相邻格子**，正好对应原题中“水只能从高到低（或相等）流”。  
- 任意格子如果能在逆向搜索中被访问到，说明从该格子出发沿着 **不升高** 的路径一定能到达对应的海岸。  

**时间/空间分析**  
- 每个格子最多被两次（一次太平洋，一次大西洋）加入队列，整体遍历一次矩阵，时间 `O(m·n)`。  
- 需要两个 `m×n` 的布尔矩阵记录可达性，空间 `O(m·n)`。

#### 代码（Python）

```python
from collections import deque
from typing import List

def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    if not heights:
        return []
    m, n = len(heights), len(heights[0])
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # BFS 从多个起点出发，返回能够到达的格子集合
    def bfs(starts: List[tuple]) -> List[List[bool]]:
        reachable = [[False]*n for _ in range(m)]
        q = deque(starts)
        for x, y in starts:
            reachable[x][y] = True          # 起点默认可达

        while q:
            x, y = q.popleft()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                # 越界直接跳过
                if not (0 <= nx < m and 0 <= ny < n):
                    continue
                # 必须满足逆向流动的条件：相邻格子高度 >= 当前格子高度
                if not reachable[nx][ny] and heights[nx][ny] >= heights[x][y]:
                    reachable[nx][ny] = True
                    q.append((nx, ny))
        return reachable

    # 1️⃣ 太平洋的起点：第一行 + 第一列
    pacific_starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(m)]
    pacific_reachable = bfs(pacific_starts)

    # 2️⃣ 大西洋的起点：最后一行 + 最后一列
    atlantic_starts = [(m-1, c) for c in range(n)] + [(r, n-1) for r in range(m)]
    atlantic_reachable = bfs(atlantic_starts)

    # 3️⃣ 交集即答案
    res = []
    for i in range(m):
        for j in range(n):
            if pacific_reachable[i][j] and atlantic_reachable[i][j]:
                res.append([i, j])
    return res
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  解释：每个格子最多被两次（一次加入太平洋队列，一次加入大西洋队列），整体线性遍历矩阵。
- **空间复杂度**：`O(m·n)`  
  解释：需要两个 `m×n` 的布尔矩阵记录可达性，加上 BFS 队列最坏也会装满整张矩阵。

---

## 心得

- **核心技巧**：**逆向多源搜索**（从海岸向内遍历），把“从每个点出发检查”转化为“从海岸向内标记可达”。  
- **适用题型**  
  1. 多源最短路径或可达性问题（如 LeetCode 417、417 变体）。  
  2. “从边界流向内部”类的矩阵题（如 **岛屿周长**、**陆地海洋分离**）。  
  3. 需要同时满足两个或多个约束的格子筛选（如 **水流向两个湖泊**）。  
- **一句话总结**：把搜索方向倒过来，从所有可能的目标点一起扩散，交集即为答案。

---

## 反思

- **第一反应**：直接对每个格子做 DFS/BFS，检查能否到达两侧海岸。  
- **最容易踩的坑**  
  - 忘记 **高度相等** 也可以流动，导致路径被错误剪掉。  
  - 只检查四个方向时，遗漏了边界格子本身已经是海岸的情况。  
  - BFS/DFS 的 visited 标记写错（比如用全局数组导致两次搜索相互干扰）。  
- **下次遇到同类题**：第一步先问自己“从**目标**出发能否更快遍历吗？”——若答案是“可以”，立刻考虑 **多源逆向搜索**，再把得到的可达集合取交/并得到最终答案。