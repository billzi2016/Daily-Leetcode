# #2812. 寻找网格中的最安全路径 / Find the Safest Path in a Grid

> 难度：中等 · 标签：Array、Binary Search、Breadth-First Search、Union Find、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-the-safest-path-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D matrix grid of size n x n, where (r, c) represents:
You are initially positioned at cell (0, 0). In one move, you can move to any adjacent cell in the grid, including cells containing thieves.
The safeness factor of a path on the grid is defined as the minimum manhattan distance from any cell in the path to any thief in the grid.
Return the maximum safeness factor of all paths leading to cell (n - 1, n - 1).
An adjacent cell of cell (r, c), is one of the cells (r, c + 1), (r, c - 1), (r + 1, c) and (r - 1, c) if it exists.
The Manhattan distance between two cells (a, b) and (x, y) is equal to |a - x| + |b - y|, where |val| denotes the absolute value of val.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,0],[0,0,0],[0,0,1]]
Output: 0
Explanation: All paths from (0, 0) to (n - 1, n - 1) go through the thieves in cells (0, 0) and (n - 1, n - 1).
```

**Example 2:**

```
Input: grid = [[0,0,1],[0,0,0],[0,0,0]]
Output: 2
Explanation: The path depicted in the picture above has a safeness factor of 2 since:
- The closest cell of the path to the thief at cell (0, 2) is cell (0, 0). The distance between them is | 0 - 0 | + | 0 - 2 | = 2.
It can be shown that there are no other paths with a higher safeness factor.
```

**Example 3:**

```
Input: grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]
Output: 2
Explanation: The path depicted in the picture above has a safeness factor of 2 since:
- The closest cell of the path to the thief at cell (0, 3) is cell (1, 2). The distance between them is | 0 - 1 | + | 3 - 2 | = 2.
- The closest cell of the path to the thief at cell (3, 0) is cell (3, 2). The distance between them is | 3 - 3 | + | 0 - 2 | = 2.
It can be shown that there are no other paths with a higher safeness factor.
```

**Constraints**

- 1 <= grid.length == n <= 400
- grid[i].length == n
- grid[i][j] is either 0 or 1.
- There is at least one thief in the grid.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的 **n × n** 大小的二维矩阵（2D matrix）`grid`，其中 `grid[r][c]` 表示单元格 \((r, c)\) 的状态：
- `0` 表示该单元格为空地；
- `1` 表示该单元格有小偷（thief）。

初始时你位于单元格 \((0, 0)\)。一次移动可以前往网格中的任意**相邻单元格**（adjacent cell），包括含有小偷的单元格。  
单元格 \((r, c)\) 的相邻单元格指存在的四个方向中的任意一个：\((r, c+1)\)、\((r, c-1)\)、\((r+1, c)\) 和 \((r-1, c)\)。

路径（path）在网格上的 **安全系数**（safeness factor）定义为：路径上所有单元格到网格中任意小偷的 **曼哈顿距离**（Manhattan distance）的最小值。  
两单元格 \((a, b)\) 与 \((x, y)\) 之间的曼哈顿距离等于 \(|a-x| + |b-y|\)，其中 \(|val|\) 表示绝对值。

返回所有从 \((0, 0)\) 到达单元格 \((n-1, n-1)\) 的路径中，能够得到的 **最大安全系数**。

---

## 示例

### 示例 1
```text
Input: grid = [[1,0,0],[0,0,0],[0,0,1]]
Output: 0
Explanation: 所有从 (0, 0) 到 (n-1, n-1) 的路径都会经过小偷所在的单元格 (0, 0) 和 (n-1, n-1)，因此安全系数为 0。
```

### 示例 2
```text
Input: grid = [[0,0,1],[0,0,0],[0,0,0]]
Output: 2
Explanation: 如图所示的路径的安全系数为 2，因为：
- 该路径中离小偷 (0, 2) 最近的单元格是 (0, 0)。两者的距离为 |0-0| + |0-2| = 2。
可以证明不存在安全系数更高的路径。
```

### 示例 3
```text
Input: grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]
Output: 2
Explanation: 如图所示的路径的安全系数为 2，因为：
- 该路径中离小偷 (0, 3) 最近的单元格是 (1, 2)。距离为 |0-1| + |3-2| = 2。
- 该路径中离小偷 (3, 0) 最近的单元格是 (3, 2)。距离为 |3-3| + |0-2| = 2。
```

---

## 约束条件

- \(1 \leq \text{grid.length} = n \leq 400\)
- \(\text{grid}[i].\text{length} = n\)
- \(\text{grid}[i][j]\) 只能是 `0` 或 `1`
- 网格中至少存在一个小偷（即至少有一个 `1`）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的路径都枚举一遍**，然后计算每条路径的安全系数（路径上离最近小偷的最小曼哈顿距离），最后取最大值。

- **枚举路径**：从左上角 `(0,0)` 出发，每一步可以向上/下/左/右四个方向移动，只要没有走出矩阵边界就继续。递归（DFS）遍历所有可能的走法，直到到达右下角 `(n‑1,n‑1)`。
- **安全系数**：遍历路径上的每个格子，计算它到所有小偷格子的曼哈顿距离，取最小值。路径的安全系数就是这些最小值中的最小值（即“路径上最危险的那一步”）。
- **取最大**：把所有路径的安全系数保存在一个变量里，最后返回最大的那个。

> **类比**：把整个网格想象成一张城市地图，格子是街区，小偷是警局。我们要找一条从家到公司的路，使得路上**最靠近警局的那段**距离尽可能远——也就是“最安全的路”。暴力做法就是把每一条可能的路都走一遍，看看哪条路的最小距离最大。

这个方法**一定能得到正确答案**，因为它遍历了所有合法路径，必然包含最优路径。

#### 代码（Python）

```python
from typing import List

def maxSafenessFactor_bruteforce(grid: List[List[int]]) -> int:
    n = len(grid)
    thieves = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 1]

    # 计算格子 (x, y) 到最近小偷的曼哈顿距离
    def dist_to_nearest_thief(x: int, y: int) -> int:
        return min(abs(x - tx) + abs(y - ty) for tx, ty in thieves)

    best = -1                     # 记录目前找到的最大安全系数
    visited = [[False] * n for _ in range(n)]

    # 深度优先搜索，枚举所有路径
    def dfs(x: int, y: int, cur_min: int) -> None:
        nonlocal best
        # 到达终点，更新答案
        if x == n - 1 and y == n - 1:
            best = max(best, cur_min)
            return

        # 四个方向的移动
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                visited[nx][ny] = True
                # 该格子到最近小偷的距离
                d = dist_to_nearest_thief(nx, ny)
                # 路径上最小的距离要随时更新
                dfs(nx, ny, min(cur_min, d))
                visited[nx][ny] = False

    # 起点本身的安全系数
    start_dist = dist_to_nearest_thief(0, 0)
    visited[0][0] = True
    dfs(0, 0, start_dist)
    return best
```

> **注释**  
> - `thieves` 保存所有小偷的位置，后面会遍历求最近距离。  
> - `dist_to_nearest_thief` 就像在“字典”里查每个格子对应的最近小偷距离。  
> - `cur_min` 记录当前已经走过的路径上最小的安全距离，递归时不断取 `min`。  

#### 复杂度

- **时间复杂度**：`O(4^{n^2})`（极端情况）  
  - 我们实际上在每个格子都有 4 条可能的移动方向，遍历所有路径的数量呈指数级增长。对于 `n=400` 完全不可接受。这里用大白话解释：时间像“树的枝杈”一样快速增长，几乎不可能在电脑里跑完。
- **空间复杂度**：`O(n^2)`  
  - 递归栈深度最坏是 `n^2`（走遍所有格子），再加上 `visited` 数组占用 `n^2` 空间。

> 暴力解虽然思路最直观，但在本题的约束（`n ≤ 400`）下根本跑不完，需要寻找更快的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**两大瓶颈**：

1. **遍历所有路径**：路径数量指数级，无法接受。  
2. **每次访问格子都要遍历所有小偷求距离**：如果小偷很多，这一步本身也是 `O(k)`（`k` 为小偷数量）。

我们可以把这两件事拆开来优化：

1. **先一次性算出每个格子到最近小偷的距离**。这可以用**多源 BFS**（一次性从所有小偷同时出发）在 `O(n^2)` 时间完成。把得到的距离记在 `dist[x][y]` 中。  
   - 类比：把所有警局（小偷）都打开广播，让它们把“我在这里，距离 0”这条信息向四周扩散，第一时间到达的格子就记录了离最近警局的距离。  
2. **在已知每格安全值的情况下，找一条从左上到右下、使最小安全值最大的路径**。这其实是**“最大最小路径”**（widest path）问题，常用的解法有两种：
   - **二分查找 + BFS**：假设答案是 `v`，把所有安全值 < `v` 的格子视为墙壁，只在剩余格子上做普通 BFS 看能否连通起点和终点。因为安全值是整数，范围在 `[0, 2n]`（曼哈顿距离最大不超过 `2*(n-1)`），二分可以在 `log(2n)` 次内定位答案。  
   - **最大堆（优先队列）+ 类似 Dijkstra**：每次优先走安全值最高的格子，维护到每个格子的“当前路径的最小安全值”。这等价于在图上找“宽度最大的路径”。时间 `O(n^2 log n)`，实现也相对直接。

下面我们采用**二分查找 + BFS**的思路，因为它把两个核心概念（多源 BFS、二分判定）分开讲，比较容易让初学者理解。

**步骤概览**：

1. **多源 BFS**  
   - 把所有小偷坐标放进队列，距离初始化为 `0`。  
   - 从队列里弹出一个格子，向四邻域扩散，如果邻居还没有距离，就把它的距离设为 `当前距离 + 1`，并加入队列。  
   - 结束后，`dist[x][y]` 就是格子 `(x,y)` 到最近小偷的曼哈顿距离。

2. **二分搜索安全系数**  
   - 设 `low = 0`，`high = max(dist)`（最大的安全值）。  
   - 每次取 `mid = (low + high + 1)//2`（向上取整），检查 **是否存在一条只经过 `dist >= mid` 的格子** 的路径。  
   - 检查方式：普通 BFS/DFS，只在满足 `dist >= mid` 的格子上前进。如果能够到达右下角，说明安全系数可以至少是 `mid`，把 `low = mid`；否则把 `high = mid - 1`。  
   - 循环结束后，`low` 即为最大安全系数。

**为什么二分能工作**：  
如果 `v` 可行（存在安全系数≥`v` 的路径），那么任何更小的 `v' < v` 也一定可行，因为放宽限制会让更多格子可走；相反，如果 `v` 不可行，所有更大的 `v' > v` 也一定不可行。这正好满足二分的“单调性”前提。

#### 代码（Python）

```python
from collections import deque
from typing import List

def maxSafenessFactor(grid: List[List[int]]) -> int:
    n = len(grid)

    # ---------- 1. 多源 BFS，计算每个格子到最近小偷的距离 ----------
    dist = [[-1] * n for _ in range(n)]          # -1 表示未访问
    q = deque()

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:                 # 小偷所在格子
                dist[i][j] = 0
                q.append((i, j))

    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1   # 距离+1 继续向外扩散
                q.append((nx, ny))

    # ---------- 2. 二分查找安全系数 ----------
    # 能否在安全阈值 >= v 的格子上走通的判定函数
    def can_reach(v: int) -> bool:
        if dist[0][0] < v or dist[n-1][n-1] < v:
            return False                         # 起点或终点本身不满足阈值
        visited = [[False] * n for _ in range(n)]
        dq = deque()
        dq.append((0,0))
        visited[0][0] = True

        while dq:
            x, y = dq.popleft()
            if x == n-1 and y == n-1:
                return True                      # 成功到达右下角
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n \
                        and not visited[nx][ny] \
                        and dist[nx][ny] >= v:
                    visited[nx][ny] = True
                    dq.append((nx, ny))
        return False

    low, high = 0, max(max(row) for row in dist)   # 最大可能安全系数
    while low < high:
        mid = (low + high + 1) // 2                # 向上取整，防止死循环
        if can_reach(mid):
            low = mid                               # mid 可行，尝试更大
        else:
            high = mid - 1                          # mid 不行，减小上界
    return low
```

**代码要点解释**  

- `dist` 数组相当于“每个格子到最近警局的距离表”。多源 BFS 把所有警局的信号一次性扩散，时间只和格子数 `n²` 成正比。  
- `can_reach(v)` 把安全阈值 `v` 当作“墙壁”，只在 `dist >= v` 的格子上走普通 BFS，判断起点能否连通终点。  
- 二分的循环里使用了 **向上取整** `(low + high + 1)//2`，这样当 `low` 与 `high` 相邻时仍能收敛。  

#### 复杂度

- **时间复杂度**：`O(n² log n)`  
  - 多源 BFS：`O(n²)`（每个格子访问一次）。  
  - 二分循环：`log(maxDist)` 次，每次 `can_reach` 进行一次普通 BFS，最坏也遍历全部格子 `O(n²)`。`maxDist` ≤ `2*(n-1)`，所以 `log` 项约等于 `log n`。整体是 `O(n² log n)`，在 `n ≤ 400` 时轻松跑完。  
- **空间复杂度**：`O(n²)`  
  - `dist`、`visited`、队列等均需要存储整个网格的信息。  

> 与暴力解相比，**时间从指数级降到了多项式级**（`n² log n`），大幅提升了可行性。

---

## 心得

- **核心技巧**：先把每个格子到最近小偷的距离算出来（多源 BFS），再在这张“安全值图”上寻找 **最大最小路径**（二分 + BFS 或最大堆）。
- **适用题型**：  
  1. “在矩阵中寻找安全/高海拔/低温的路径”——如 LeetCode 1102 *Path With Maximum Minimum Value*。  
  2. “在图中最大化最小边权”——如 “宽度优先路径”（widest path）或 “最小瓶颈路径”。  
  3. “多源最短距离”——如 “逃离鬼屋” 类题目，需要一次性从多个起点 BFS。
- **一句话总结**：**把“离危险的距离”先算好，然后在这张“安全地图”上用二分或堆找最宽的通路**。

---

## 反思

- **第一反应**：直接枚举所有路径（DFS）求最大安全系数，忽略了路径数量的爆炸式增长。  
- **最容易踩的坑**：  
  - **距离计算重复**：每访问一个格子都遍历所有小偷，导致 `O(k·n²)` 的额外开销。  
  - **二分的单调性**：忘记检查起点或终点本身是否满足阈值，会导致错误的 `True/False` 判定。  
  - **边界条件**：`n = 1` 时起点就是终点，答案应直接是 `dist[0][0]`（即 0 或 1），代码要能处理。  
- **下次类似题目**：第一步先**把所有“源点”一起跑 BFS，得到每个位置的“距离/代价”表；第二步再**在这个表上做二分 + 可达性检查**（或最大堆），而不是直接枚举路径。这样思路更清晰，效率也更高。