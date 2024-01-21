# #2556. 至多翻转一个格子使二进制矩阵路径断开 / Disconnect Path in a Binary Matrix by at Most One Flip

> 难度：中等 · 标签：Array、Dynamic Programming、Depth-First Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n binary matrix grid. You can move from a cell (row, col) to any of the cells (row + 1, col) or (row, col + 1) that has the value 1. The matrix is disconnected if there is no path from (0, 0) to (m - 1, n - 1).
You can flip the value of at most one (possibly none) cell. You cannot flip the cells (0, 0) and (m - 1, n - 1).
Return true if it is possible to make the matrix disconnect or false otherwise.
Note that flipping a cell changes its value from 0 to 1 or from 1 to 0.

**Examples**

**Example 1:**

```
Input: grid = [[1,1,1],[1,0,0],[1,1,1]]
Output: true
Explanation: We can change the cell shown in the diagram above. There is no path from (0, 0) to (2, 2) in the resulting grid.
```

**Example 2:**

```
Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: false
Explanation: It is not possible to change at most one cell such that there is not path from (0, 0) to (2, 2).
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 105
- grid[i][j] is either 0 or 1.
- grid[0][0] == grid[m - 1][n - 1] == 1

---

## 题目（中文翻译）

给定一个下标从 0 开始的 `m × n` 二进制矩阵 `grid`。你可以从单元格 `(row, col)` 移动到任意值为 **1** 的相邻单元格 `(row + 1, col)` 或 `(row, col + 1)`。如果不存在从 `(0, 0)` 到 `(m - 1, n - 1)` 的路径，则矩阵被认为是 **断开的**（disconnected）。

你至多可以翻转（flip）一个单元格的值（也可以不翻转），但 **不能** 翻转起点 `(0, 0)` 和终点 `(m - 1, n - 1)`。翻转会把 `0` 变成 `1`，或把 `1` 变成 `0`。

返回 `true` 表示可以通过至多翻转一个单元格使矩阵断开，返回 `false` 表示无法做到。

### 示例

**示例 1**  
``` 
Input: grid = [[1,1,1],[1,0,0],[1,1,1]]
Output: true
Explanation: 我们可以翻转示意图中标出的格子。翻转后从 (0, 0) 到 (2, 2) 不再存在路径。
```

**示例 2**  
``` 
Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: false
Explanation: 无论如何至多翻转一个格子，都无法使得从 (0, 0) 到 (2, 2) 的路径不存在。
```

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 1000`
- `1 <= m * n <= 10^5`
- `grid[i][j]` 仅为 `0` 或 `1`
- `grid[0][0] == grid[m - 1][n - 1] == 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举**所有可以翻转的格子（除掉左上角和右下角），每枚举一次就把它的值取反，然后用 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）** 判断从 `(0,0)` 能否走到 `(m‑1,n‑1)`。  
- **BFS/DFS** 就像在迷宫里找路：我们把每个值为 `1` 的格子当成可以通行的“道路”，从起点一步步往右或往下走，看看能否到达终点。  
- 如果在某次翻转后 **找不到** 这样的一条路，说明翻这个格子就能把矩阵断开，直接返回 `True`。  
- 如果所有格子都尝试完仍然能走通，则返回 `False`。

这种做法一定是对的，因为我们把**所有可能的翻转情况都检查了一遍**，只要有一种能让路径消失，就会被发现。

#### 代码（Python）

```python
from collections import deque
from copy import deepcopy
from typing import List

def can_reach(grid: List[List[int]]) -> bool:
    """普通 BFS，判断是否存在从左上到右下的合法路径"""
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 0 or grid[m-1][n-1] == 0:
        return False
    q = deque([(0, 0)])
    visited = [[False] * n for _ in range(m)]
    visited[0][0] = True
    while q:
        r, c = q.popleft()
        if (r, c) == (m-1, n-1):
            return True
        for nr, nc in ((r+1, c), (r, c+1)):          # 只能向下或向右走
            if nr < m and nc < n and not visited[nr][nc] and grid[nr][nc] == 1:
                visited[nr][nc] = True
                q.append((nr, nc))
    return False

def disconnect_path_bruteforce(grid: List[List[int]]) -> bool:
    """暴力枚举翻转每一个内部格子，检查是否能断开路径"""
    m, n = len(grid), len(grid[0])

    # 先判断原矩阵本身是否已经断开
    if not can_reach(grid):
        return True

    # 枚举所有可以翻转的格子（排除 (0,0) 与 (m-1,n-1)）
    for i in range(m):
        for j in range(n):
            if (i, j) in [(0, 0), (m-1, n-1)]:
                continue
            # 复制一份矩阵，翻转当前格子
            new_grid = deepcopy(grid)
            new_grid[i][j] ^= 1          # 0↔1 的快速翻转
            if not can_reach(new_grid):  # 翻转后不可达，说明成功断开
                return True
    return False
```

#### 复杂度  

- **时间复杂度**：  
  - `can_reach` 需要遍历整个矩阵一次，复杂度是 `O(m·n)`。  
  - 暴力枚举会对每个内部格子（最多 `m·n` 个）都调用一次 `can_reach`，所以总时间是 `O((m·n)²)`。  
  - 用大白话说，就是“如果矩阵有 10⁴ 个格子，最坏情况下要检查 10⁸ 次”，对 10⁵ 规模的矩阵会超时。

- **空间复杂度**：  
  - BFS 用到的 `visited` 数组占 `O(m·n)`，复制矩阵时也需要同样的空间。  
  - 整体是 `O(m·n)`，即随矩阵大小线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次翻转都重新跑一次 BFS**，导致二次遍历。我们需要在 **一次遍历** 中就判断是否存在“必经格子”。  
关键观察：

1. **只能向右或向下走**，所以所有合法路径的长度固定为 `(m‑1)+(n‑1)` 步。  
2. 第 `k` 步（从 0 开始）走到的格子一定满足 `row + col = k`，这是一条**斜对角线**（我们称为 “层” 或 “anti‑diagonal”）。  
3. 如果在某一层上，**至少有两个格子同时在某条合法路径上**，那么我们可以让两条路径在这一步分叉，从而得到两条**互不相交（内部不共享格子）**的路径。  
4. 反之，如果每一层上**至多只有一个**格子在任何合法路径中出现，那么所有路径都会经过同一个格子序列——这条唯一的路径的每个内部格子都是**必经点**，翻掉任意一个（除起点终点）就能断开。

于是问题转化为：

- 找出所有 **既能从起点到达，又能走到终点** 的格子（即在某条合法路径上）。  
- 按 `row + col` 分组，统计每组中符合条件的格子数量。  
- 若出现 **数量 ≥ 2** 的层，说明存在两条互不相交的路径，答案 `False`（无法通过一次翻转断开）。  
- 否则答案 `True`（一定能断开，甚至原本就已经断开）。

实现细节：

1. **正向可达**：从左上角用 DP/BFS 只向右/下走，记 `reach_from_start[i][j]`。  
2. **逆向可达**：从右下角只向左/上走，记 `reach_to_end[i][j]`。这相当于把方向反过来。  
3. 同时满足两者的格子即在某条合法路径上。  

这样只需要 **两次线性遍历**，时间 `O(m·n)`，空间 `O(m·n)`（可以进一步压缩为两行，但这里保持可读性）。

#### 代码（Python）

```python
from typing import List

def disconnect_path(grid: List[List[int]]) -> bool:
    """
    最优解：只遍历两遍矩阵，判断是否存在必经格子。
    若原本已经断开直接返回 True；
    否则若每条 anti‑diagonal 上至多出现一个 “在路径上的格子”，
    说明存在必经格子，翻掉它即可断开，返回 True；
    否则存在两条互不相交的路径，翻一个格子也不能断开，返回 False。
    """
    m, n = len(grid), len(grid[0])

    # ---------- 1. 正向可达（只向右/下） ----------
    reach_from_start = [[False] * n for _ in range(m)]
    if grid[0][0] == 1:
        reach_from_start[0][0] = True
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:               # 墙壁不可走
                continue
            if i > 0 and reach_from_start[i-1][j]:
                reach_from_start[i][j] = True
            if j > 0 and reach_from_start[i][j-1]:
                reach_from_start[i][j] = True

    # 若连通性本来就不存在，直接返回 True
    if not reach_from_start[m-1][n-1]:
        return True

    # ---------- 2. 逆向可达（只向左/上） ----------
    reach_to_end = [[False] * n for _ in range(m)]
    if grid[m-1][n-1] == 1:
        reach_to_end[m-1][n-1] = True
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            if grid[i][j] == 0:
                continue
            if i+1 < m and reach_to_end[i+1][j]:
                reach_to_end[i][j] = True
            if j+1 < n and reach_to_end[i][j+1]:
                reach_to_end[i][j] = True

    # ---------- 3. 统计每条 anti‑diagonal ----------
    # anti_diag_cnt[d] = 在第 d 条对角线上（i+j=d）同时可达的格子数
    max_diag = m + n - 2
    anti_diag_cnt = [0] * (max_diag + 1)

    for i in range(m):
        for j in range(n):
            if reach_from_start[i][j] and reach_to_end[i][j]:
                d = i + j
                anti_diag_cnt[d] += 1
                # 一旦出现两格，说明有两条不相交的路径
                if anti_diag_cnt[d] >= 2:
                    return False   # 不能通过一次翻转断开

    # 若遍历完都没有出现 “≥2”，说明每层最多只有一个必经格子
    # 翻掉任意一个内部必经格子即可断开
    return True
```

#### 复杂度  

- **时间复杂度**：  
  - 正向 DP、逆向 DP、以及一次统计遍历，总共是 **3 次线性扫描**，每次都只访问每个格子一次，故为 `O(m·n)`。  
  - 用大白话说，就是“只要走一遍矩阵，就能得到答案”，即使是最大 `10⁵` 个格子也能在毫秒级完成。

- **空间复杂度**：  
  - 两个布尔矩阵 `reach_from_start`、`reach_to_end` 各占 `O(m·n)`，再加一个长度为 `m+n` 的计数数组，整体仍是 `O(m·n)`。  
  - 如果想进一步压缩空间，可以把两个布尔矩阵改成两行滚动数组，但这里保持代码易读性。

---

## 心得

- **核心技巧**：把“是否存在必经格子”转化为“每条 anti‑diagonal 上的可行格子数量”。只要在同一层出现两个可行格子，就能得到两条内部不相交的路径，单点翻转无法断开。
- **适用的题型**  
  1. **唯一路径 / 必经点** 类题，例如 “判断网格中是否存在唯一的从左上到右下的路径”。  
  2. **路径割点**（Vertex Cut）在 DAG 中的判定，如 “在只能向右下走的网格里，找出所有关键格子”。  
  3. **双路径判定**，比如 “判断是否可以在有向无环图中找到两条不相交的 s‑t 路径”。
- **一句话总结解题钥匙**：**在只能向右下走的网格里，检查每条对角线是否出现多于一个“在任何合法路径上的格子”。**  

---

## 反思

- **第一反应**：直接枚举翻转每个格子，然后跑 BFS/DFS 检查连通性。思路直观但显然会超时。
- **最容易踩的坑**  
  1. **忘记先判断原矩阵是否已经断开**——如果一开始就没有路径，答案应直接返回 `True`。  
  2. **把“两条路径”误认为只要有两条不同的路径**，实际上需要**内部不共享格子**（顶点不相交），否则仍可能被同一个格子卡住。  
  3. **边界条件**：`m`、`n` 为 `1` 时只能有起点即终点，直接返回 `True`（因为题目不允许翻动这两个格子，且本身已经是唯一路径）。  
- **下次遇到同类题的第一步**：先思考**“是否存在唯一必经点”**，尝试用层次（`i+j`）或拓扑序的方式把所有路径的共同点抽象出来，而不是盲目枚举。这样往往能把时间复杂度降到线性。