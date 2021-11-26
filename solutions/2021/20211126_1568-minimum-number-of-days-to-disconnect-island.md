# #1568. 最少天数使岛屿断连 / Minimum Number of Days to Disconnect Island

> 难度：困难 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix、Strongly Connected Component · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-days-to-disconnect-island/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary grid grid where 1 represents land and 0 represents water. An island is a maximal 4-directionally (horizontal or vertical) connected group of 1's.
The grid is said to be connected if we have exactly one island, otherwise is said disconnected.
In one day, we are allowed to change any single land cell (1) into a water cell (0).
Return the minimum number of days to disconnect the grid.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,1,0],[0,1,1,0],[0,0,0,0]]

Output: 2
Explanation: We need at least 2 days to get a disconnected grid.
Change land grid[1][1] and grid[0][2] to water and get 2 disconnected island.
```

**Example 2:**

```
Input: grid = [[1,1]]
Output: 2
Explanation: Grid of full water is also disconnected ([[1,1]] -> [[0,0]]), 0 islands.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 30
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m × n` 的二进制网格 `grid`，其中 `1` 表示陆地，`0` 表示水域。**岛屿**（island）是指由 `1` 组成的最大四方向（水平或垂直）连通块。  
如果网格中恰好只有一个岛屿，则称网格是**连通的**；否则称为**断连的**。  

在一天内，你可以将任意一个陆地单元格 (`1`) 改为水域单元格 (`0`)。  
返回使网格断连所需的最少天数。

**示例**  

*示例 1*  
```
Input: grid = [[0,1,1,0],[0,1,1,0],[0,0,0,0]]
Output: 2
Explanation: 至少需要 2 天才能使网格断连。将 grid[1][1] 和 grid[0][2] 这两个陆地改为水域后，得到两个不相连的岛屿。
```

*示例 2*  
```
Input: grid = [[1,1]]
Output: 2
Explanation: 将所有陆地改为水域后（[[1,1]] → [[0,0]]），网格中不再有岛屿，属于断连状态。
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 ≤ m, n ≤ 30`  
- `grid[i][j]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一块陆地（值为 1 的格子）都尝试删除一次**，看删掉后地图是否已经不只一个岛屿（即变成「已断开」）。  
如果有哪一次只需要删除 1 块陆地就能让岛屿数量大于 1，答案就是 1 天；  
如果所有单块删除都仍然只剩下 1 个岛屿，说明最少需要 2 天（因为题目已证明不可能需要 3 天以上）。

实现步骤：

1. **统计当前岛屿数量**。用 **DFS（深度优先搜索）** 或 **BFS（广度优先搜索）** 从任意陆地格子出发，沿四个方向（上、下、左、右）遍历相连的 1，把遍历过的格子标记为已访问。遍历完一次即得到一个岛屿。遍历整个网格得到岛屿总数 `cnt`。  
   - 把 DFS 想象成“在陆地上走路”，每走到一个相邻的陆地格子就记下来，走不通的地方就停下来。
2. **如果 `cnt` ≠ 1**，说明本来就已经是「已断开」状态，直接返回 0 天。
3. **尝试单块删除**：遍历网格中的每个 1，临时把它改成 0，重新统计岛屿数量 `cnt2`。  
   - 如果 `cnt2` 为 0（全水）或 ≥ 2，说明删掉这块就能让地图断开，返回 1 天。  
   - 删除后记得把格子恢复为 1，继续尝试下一个格子。
4. 如果所有格子都尝试完仍未出现断开的情况，答案只能是 2 天（因为题目保证最多两天就能断开）。

> **哈希表类比**：这里没有用到哈希表，不过如果你把「每个格子的位置」想象成「字典的 key」，「格子是否是陆地」想象成「字典的 value」也能帮助记忆：我们在「字典」里查找所有值为 1 的键，然后逐个「把键对应的值改成 0」来模拟删除。

#### 代码（Python）

```python
from collections import deque
from copy import deepcopy
from typing import List

def minDays(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # -------------------------------------------------
    # 1）辅助函数：统计当前网格的岛屿数量
    # -------------------------------------------------
    def count_islands(mat: List[List[int]]) -> int:
        visited = [[False] * n for _ in range(m)]
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        islands = 0

        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1 and not visited[i][j]:
                    islands += 1                # 找到一个新岛屿
                    # 用 BFS 把这个岛屿的所有格子都标记为已访问
                    q = deque([(i, j)])
                    visited[i][j] = True
                    while q:
                        x, y = q.popleft()
                        for dx, dy in dirs:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < m and 0 <= ny < n \
                               and mat[nx][ny] == 1 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                q.append((nx, ny))
        return islands

    # -------------------------------------------------
    # 2）先判断原始网格是否已经断开
    # -------------------------------------------------
    if count_islands(grid) != 1:          # 已经是 0 或 ≥2 个岛屿
        return 0

    # -------------------------------------------------
    # 3）尝试删除单块陆地
    # -------------------------------------------------
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                grid[i][j] = 0               # “拔掉”这块陆地
                if count_islands(grid) != 1:  # 断开了（0 或 ≥2）
                    grid[i][j] = 1           # 恢复原状，防止后面代码受影响
                    return 1
                grid[i][j] = 1               # 恢复，继续尝试下一个格子

    # -------------------------------------------------
    # 4）如果单块都不行，答案只能是 2
    # -------------------------------------------------
    return 2
```

> 关键行中文注释已写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：  
  - `count_islands` 本身是 O(m·n)（遍历整个网格一次）。  
  - 暴力方案在最坏情况下会对每个陆地格子都调用一次 `count_islands`，陆地格子数最多也是 m·n。  
  - 所以总体是 **O((m·n)²)**，即“平方级”。如果把 `m·n` 看成总格子数 N，则是 O(N²)。  
  - 大白话：如果网格是 30×30（900 格），最坏要检查 900 次，每次遍历 900 格，约 81 万次操作，仍能接受但不够高效。

- **空间复杂度**：  
  - `visited` 数组占 O(m·n) 的额外空间；递归栈或队列最多也会存 O(m·n) 个坐标。  
  - 因此是 **O(m·n)**，即“和网格大小成正比”。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都重新遍历整张网格** 来判断是否已断开，这导致二次遍历的平方时间。  
我们可以把“是否只需要删除一块陆地就能断开”这个问题转化为 **图论中的割点（Articulation Point）** 判断：

- 把每块陆地看成图的一个节点，四方向相连的陆地之间有无向边。  
- 整张网格如果恰好是 **一个连通分量**（即题目说的“仅有一个岛屿”），我们只需要判断这个连通图里是否存在 **割点**。  
- **割点**：如果把这个节点（陆地）删掉，连通图会被分成 **两个或更多的连通分量**。这正对应“只删掉一块陆地就能让岛屿数变 ≥2”。  

因此最优解的步骤：

1. **先检查是否已经断开**（同暴力解的第一步），如果是直接返回 0。
2. **在仅有一个岛屿的前提下，使用 Tarjan 算法（DFS + 时间戳）找割点**。  
   - 对每个未访问的陆地格子执行一次 DFS，记录 `disc[u]`（节点 u 被首次发现的时间）和 `low[u]`（从 u 或 u 的子树能够追溯到的最早发现时间）。  
   - 对根节点（DFS 的起点），如果它有 **两个或以上的子树**，则根本身是割点。  
   - 对非根节点，如果存在子节点 v，使得 `low[v] >= disc[u]`，则 u 为割点。  
   - 只要找到 **任意一个割点**，说明只需要一天就能断开，返回 1。
3. 如果 **没有割点**，说明即使删掉任意单块陆地，岛屿仍保持连通。根据题目提示，这种情况最多需要 **两天**（比如把两块关键的陆地一次删掉），所以返回 2。

> **单调栈类比**：Tarjan 算法里维护的 `low` 相当于“往回看能追溯到多早”，像在栈里找前一个更小的元素，只是这里的“更小”指的是时间戳更早。  

#### 代码（Python）

```python
from typing import List

def minDays(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # -------------------------------------------------
    # 1）统计岛屿数量（同暴力解的函数，只保留计数）
    # -------------------------------------------------
    def count_islands() -> int:
        visited = [[False]*n for _ in range(m)]
        islands = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and not visited[i][j]:
                    islands += 1
                    stack = [(i,j)]
                    visited[i][j] = True
                    while stack:
                        x, y = stack.pop()
                        for dx, dy in dirs:
                            nx, ny = x+dx, y+dy
                            if 0 <= nx < m and 0 <= ny < n \
                               and grid[nx][ny] == 1 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
        return islands

    # -------------------------------------------------
    # 2）如果已经不是单岛，直接返回 0
    # -------------------------------------------------
    if count_islands() != 1:
        return 0

    # -------------------------------------------------
    # 3）Tarjan 寻找割点
    # -------------------------------------------------
    disc = [[-1]*n for _ in range(m)]   # 发现时间
    low  = [[-1]*n for _ in range(m)]   # 能追溯到的最早时间
    time = 0
    found_articulation = False          # 是否找到割点

    def dfs(x: int, y: int, parent_x: int, parent_y: int) -> None:
        nonlocal time, found_articulation
        time += 1
        disc[x][y] = low[x][y] = time
        child_cnt = 0   # 当前节点的子树数量（用于根节点的判定）

        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if not (0 <= nx < m and 0 <= ny < n) or grid[nx][ny] == 0:
                continue
            if disc[nx][ny] == -1:               # 未访问的子节点
                child_cnt += 1
                dfs(nx, ny, x, y)
                low[x][y] = min(low[x][y], low[nx][ny])

                # 非根节点的割点判定
                if (parent_x, parent_y) != (-1, -1) and low[nx][ny] >= disc[x][y]:
                    found_articulation = True
                # 根节点的割点判定（子树数 >= 2）
                if (parent_x, parent_y) == (-1, -1) and child_cnt >= 2:
                    found_articulation = True
            elif (nx, ny) != (parent_x, parent_y):   # 回边，更新 low
                low[x][y] = min(low[x][y], disc[nx][ny])

    # 找到任意一个陆地作为 DFS 起点
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dfs(i, j, -1, -1)
                break
        if disc[i][j] != -1:
            break

    # -------------------------------------------------
    # 4）根据是否存在割点返回答案
    # -------------------------------------------------
    if found_articulation:
        return 1      # 删除这块割点即可断开
    else:
        return 2      # 没有割点，需要两块陆地
```

> 代码中每一段都加了中文注释，帮助你一步步跟踪算法的执行过程。

#### 复杂度

- **时间复杂度**：  
  - `count_islands` 只执行一次，O(m·n)。  
  - Tarjan 的 DFS 只遍历每个陆地格子一次，且每条边（四方向相连）检查常数次，仍是 **O(m·n)**。  
  - 整体是 **O(m·n)**，即“和网格大小线性相关”。相较于暴力的 O((m·n)²)，提升巨大。

- **空间复杂度**：  
  - `disc`、`low`、递归栈（最深 ≤ m·n）共占 O(m·n)。  
  - 因此是 **O(m·n)**，与输入规模相同的额外空间。

---

## 心得

- **核心技巧**：把“单块删除是否能断开”转化为 **割点（Articulation Point）** 判定。  
- **适用的题型**：  
  1. “最少删除多少条边/节点使图不连通” 类似题（如 LeetCode 1482 – Minimum Number of Days to Make MBTI Groups Disconnected）。  
  2. “找出图中关键节点/桥” 的问题（如 LeetCode 1192 – Critical Connections in a Network）。  
  3. “判断网络是否稳固” 这类网络连通性分析题。  
- **一句话总结解题钥匙**：**把岛屿看成图，利用割点快速判断“一次删掉是否足够”。**

---

## 反思

- **第一反应**：直接想到“枚举每块陆地，删掉后再检查”。这就是暴力思路，易于实现但不够高效。  
- **最容易踩的坑**：  
  - 忘记先判断原始网格是否已经断开，导致错误返回 1。  
  - 在 Tarjan 实现中漏掉根节点的特殊判定（子树数≥2），会把本应是割点的根误判为普通节点。  
  - 边界情况：整个网格全是水（0）或只有一块陆地（1×1），都要返回 2，因为两天后全变水也算断开。  
- **下次遇到同类题**：第一步先 **把问题抽象成图的连通性**，检查是否已有多个连通分量；随后 **思考是否有关键节点/关键边**（割点/桥），如果有，用 Tarjan/DFS 直接判定；若没有，则答案往往是固定的上界（本题是 2 天）。