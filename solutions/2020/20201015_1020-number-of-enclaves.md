# #1020. 封闭岛屿的数量 / Number of Enclaves

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/number-of-enclaves/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid, where 0 represents a sea cell and 1 represents a land cell.
A move consists of walking from one land cell to another adjacent (4-directionally) land cell or walking off the boundary of the grid.
Return the number of land cells in grid for which we cannot walk off the boundary of the grid in any number of moves.

**Examples**

**Example 1:**

```
Input: grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
Output: 3
Explanation: There are three 1s that are enclosed by 0s, and one 1 that is not enclosed because its on the boundary.
```

**Example 2:**

```
Input: grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
Output: 0
Explanation: All 1s are either on the boundary or can reach the boundary.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 500
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

你得到一个 **m × n** 的二进制矩阵（binary matrix）`grid`，其中 `0` 表示海洋单元格，`1` 表示陆地单元格。  
一次移动可以从一个陆地单元格走到另一个**四方向相邻**（4-directionally）的陆地单元格，或者走出矩阵的边界。  

返回矩阵中所有**无法**通过任意次数的移动走出边界的陆地单元格的数量。

**示例 1**  

**输入**  
``` 
grid = [[0,0,0,0],
        [1,0,1,0],
        [0,1,1,0],
        [0,0,0,0]]
```  

**输出**  
```
3
```  

**解释**  
有三个 `1` 被 `0` 完全包围，而另一个 `1` 位于边界上，因而不是封闭的。

**示例 2**  

**输入**  
``` 
grid = [[0,1,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,0,0]]
```  

**输出**  
```
0
```  

**解释**  
所有的 `1` 要么在边界上，要么可以到达边界。

**约束条件**  

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 500`
- `grid[i][j]` 只能是 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**对每一个陆地格子（值为 1）**，从它出发，尝试走遍所有可能的路径，看看能否走到矩阵的边界。  
- **遍历**：先遍历整个矩阵，找到所有 `1`。  
- **深度优先搜索（DFS）**：从该格子出发，向上、下、左、右四个方向递归搜索，只要遇到 `0`（海）就停下来。  
- **判定**：如果搜索过程中碰到了矩阵的任意一条边（行号为 0 或 `m-1`，列号为 0 或 `n-1`），说明这块陆地可以“逃离”，不算在“被围住的陆地”里。否则，这块陆地就是我们要统计的。

> **类比**：把矩阵想象成一张地图，`1` 是陆地，`0` 是海。我们把每块陆地当成一座小岛，从岛上任意一点出发，沿着相连的陆地“徒步”。如果徒步的过程中能走到地图的边缘（海岸线），说明这座岛是“通向外部”的；否则，它就是“被海水完全包围”的小岛。

**为什么这个方法正确**  
- 对每块陆地都做了完整的可达性搜索，所有能到达边界的路径都会被发现。  
- 只要有一次能到达边界，就说明该陆地不是“封闭的”。没有一次成功则一定被海水围住。

**时间/空间复杂度**  
- 对每个 `1` 都要做一次完整的 DFS，最坏情况下每次搜索会遍历整个矩阵（`m × n`），于是时间复杂度是 **O((m·n)²)**。  
- 递归栈（或显式栈）最深可能到达矩阵的全部格子，需要 **O(m·n)** 的额外空间。

> **大白话解释**：  
> - `O(m·n)` 表示“和矩阵里格子的总数成正比”。如果矩阵是 100×100，就是 10,000；如果是 500×500，就是 250,000。  
> - `O((m·n)²)` 就是“把这个数字再乘以自己一次”。250,000² ≈ 6.25 × 10¹⁰，显然太大了，跑不动。

#### 代码（Python）

```python
from typing import List

def numEnclaves_brute(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # 四个方向的移动向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 辅助函数：从 (x, y) 开始深度优先搜索，返回是否能到达边界
    def dfs(x: int, y: int, visited: set) -> bool:
        # 如果已经走到矩阵边缘，说明可以逃脱
        if x == 0 or x == m - 1 or y == 0 or y == n - 1:
            return True
        visited.add((x, y))
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 只在陆地且未访问过的格子继续搜索
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1 and (nx, ny) not in visited:
                if dfs(nx, ny, visited):
                    return True
        return False

    enclave_cnt = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:                     # 只关心陆地格子
                visited = set()
                if not dfs(i, j, visited):          # 若搜索不到边界，则为封闭陆地
                    enclave_cnt += 1
    return enclave_cnt
```

#### 复杂度  

- **时间复杂度**：`O((m·n)²)` —— 每块陆地都可能遍历整个矩阵。  
- **空间复杂度**：`O(m·n)` —— 递归栈或 `visited` 集合最多存放整个矩阵的格子。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于对每块陆地都重复遍历**。实际上，所有能够**“走出边界”** 的陆地都有一个共同的特征：**它们和矩阵边缘的陆地相连**。  

**核心想法**：  
1. **先把所有在边界上的陆地以及它们能连通的陆地全部标记为“可以逃脱”**。这一步只需要一次遍历 + 一次 BFS/DFS。  
2. **剩下的未标记的陆地就是被围住的**，直接计数即可。

这样我们只做 **一次** 搜索，避免了重复遍历。

**具体步骤**  

| 步骤 | 操作 | 类比 |
|------|------|------|
| 1    | 找到所有位于第一行、最后一行、第一列、最后一列的 `1`（边界陆地） | 把地图四周的“入口”找出来 |
| 2    | 从每个入口出发，用 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）** 把所有相连的陆地标记为 “已访问” | 想象从海岸线出发，顺着陆地一步步走，走到的每块陆地都可以离开地图 |
| 3    | 再遍历整个矩阵，统计那些 **仍然是 1 且未被访问** 的格子数量 | 剩下的陆地就是被海水完全包围的“岛屿” |

**为什么只需要一次搜索**  
- 所有可以逃脱的陆地必定与某个边界陆地相连。只要把所有边界陆地的连通分量一次性遍历完，就把所有“逃脱”可能性全部覆盖了。  
- 其余陆地必然与边界无连通路径，天然符合题意。

**数据结构解释**  

- **队列（Queue）**：在 BFS 中使用，类似排队等候的队伍。我们把要“进一步探索”的格子依次放进去，保证先探索离入口最近的格子。  
- **集合 / 二维布尔数组 visited**：记录哪些格子已经被走过，防止重复遍历。可以把它想成“已经检查过的地图标记”。

#### 代码（Python）

```python
from collections import deque
from typing import List

def numEnclaves(grid: List[List[int]]) -> int:
    """
    最优解：先把所有能从边界到达的陆地标记，再统计剩余的陆地数量。
    """
    m, n = len(grid), len(grid[0])
    # visited 用来标记已经“逃脱”的陆地，初始化为全 False
    visited = [[False] * n for _ in range(m)]
    q = deque()                     # BFS 用的队列

    # 1️⃣ 把所有边界上的陆地加入队列
    for i in range(m):
        for j in (0, n - 1):        # 只看第一列和最后一列
            if grid[i][j] == 1 and not visited[i][j]:
                visited[i][j] = True
                q.append((i, j))
    for j in range(n):
        for i in (0, m - 1):        # 只看第一行和最后一行
            if grid[i][j] == 1 and not visited[i][j]:
                visited[i][j] = True
                q.append((i, j))

    # 方向向量：上、下、左、右
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 2️⃣ BFS：从所有入口同时向内扩散，标记所有可以逃脱的陆地
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 检查新坐标合法且是陆地且未访问过
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))

    # 3️⃣ 统计未被访问的陆地数量，即被围住的陆地
    enclave_cnt = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1 and not visited[i][j]:
                enclave_cnt += 1
    return enclave_cnt
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` —— 每个格子至多被访问两次（一次加入队列，一次出队），所以和矩阵大小成线性关系。  
- **空间复杂度**：`O(m·n)` —— `visited` 数组和 BFS 队列最坏情况下都可能存放整个矩阵的格子。  

> 与暴力解相比，时间从 **平方级** 降到了 **线性级**，在 500×500 的最大输入下也能轻松跑完。

---

## 心得  

- **核心技巧**：**从边界出发的多源 BFS/DFS**（一次性把所有“入口”放进搜索队列）。  
- **适用的题型**：  
  1. “岛屿问题”系列，如 **Number of Islands**、**Surrounded Regions**（围住的地区）  
  2. “连通分量”相关的题目，例如 **Regions Cut By Slashes**、**Pacific Atlantic Water Flow**  
  3. 任意需要判断“是否能到达边界或特定节点”的网格/图问题。  
- **一句话总结解题钥匙**：**把所有可能的起点（这里是边界陆地）一次性加入搜索，让它们“把能逃脱的陆地”全部涂掉，剩下的自然就是被围住的**。

---

## 反思  

- **第一反应**：看到“只能向四个方向走，且要判断能否走出边界”，立刻想到 **DFS**，于是写出逐块搜索的暴力实现。  
- **最容易踩的坑**：  
  - **重复遍历**：对每块陆地都单独搜索会导致时间爆炸。  
  - **边界条件**：忘记把四条边都加入初始队列，导致部分边缘陆地未被标记。  
  - **访问标记**：如果只用 `grid[i][j] = 0` 直接修改原矩阵，需要小心不影响后续计数；使用单独的 `visited` 更安全。  
- **下次遇到同类题**：第一步就思考 **“哪些格子是天然的起点？”**（边界、特殊标记、外部虚拟节点），然后 **从这些起点一起搜索**，把所有可以到达的区域提前剔除，最后再统计剩余符合条件的格子。