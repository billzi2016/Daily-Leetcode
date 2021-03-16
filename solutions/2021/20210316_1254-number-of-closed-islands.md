# #1254. 闭合岛屿的数量 / Number of Closed Islands

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/number-of-closed-islands/)

---

## 题目（英文原版）

**Description**

Given a 2D grid consists of 0s (land) and 1s (water).  An island is a maximal 4-directionally connected group of 0s and a closed island is an island totally (all left, top, right, bottom) surrounded by 1s.
Return the number of closed islands.

**Examples**

**Example 1:**

```
Input: grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]
Output: 2
Explanation: 
Islands in gray are closed because they are completely surrounded by water (group of 1s).
```

**Example 2:**

```
Input: grid = [[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]]
Output: 1
```

**Example 3:**

```
Input: grid = [[1,1,1,1,1,1,1],
               [1,0,0,0,0,0,1],
               [1,0,1,1,1,0,1],
               [1,0,1,0,1,0,1],
               [1,0,1,1,1,0,1],
               [1,0,0,0,0,0,1],
               [1,1,1,1,1,1,1]]
Output: 2
```

**Constraints**

- 1 <= grid.length, grid[0].length <= 100
- 0 <= grid[i][j] <=1

---

## 题目（中文翻译）

给定一个由 `0`（陆地）和 `1`（水）组成的二维网格（`grid`）。岛屿（`island`）是由 `0` 构成的最大四向相连（`4-directionally connected`）区域，而闭合岛屿（`closed island`）是指该岛屿在左、上、右、下四个方向上全部被 `1` 包围。返回闭合岛屿的数量。

### 示例

#### 示例 1
**输入**  
```text
grid = [[1,1,1,1,1,1,1,0],
        [1,0,0,0,0,1,1,0],
        [1,0,1,0,1,1,1,0],
        [1,0,0,0,0,1,0,1],
        [1,1,1,1,1,1,1,0]]
```
**输出**  
```text
2
```
**解释**  
灰色区域的岛屿是闭合的，因为它们被水（`1` 的集合）完全包围。

#### 示例 2
**输入**  
```text
grid = [[0,0,1,0,0],
        [0,1,0,1,0],
        [0,1,1,1,0]]
```
**输出**  
```text
1
```

#### 示例 3
**输入**  
```text
grid = [[1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,0,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]]
```
**输出**  
```text
2
```

### 约束条件
- `1 <= grid.length, grid[0].length <= 100`
- `0 <= grid[i][j] <= 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有相邻的 0 看成一块陆地**，只要这块陆地没有碰到矩阵的边界，就说明它被 1 完全包围，是一个 *closed island*。  
实现思路可以分两步：

1. **遍历整个网格**，每遇到一个未访问过的 `0`，就启动一次 **深度优先搜索（DFS）**（或广度优先搜索 BFS），把与之 4‑方向相连的所有 `0` 标记为已访问。  
2. 在搜索的过程中，记录是否碰到了矩阵的四条边（上、下、左、右）。如果搜索结束后没有碰到边界，则说明这块连通的 `0` 组成了一个闭合岛屿，计数器加一。

> **类比**：把 `0` 当成城镇，`1` 当成河流。我们要找的闭合岛屿就像一座被河流完全围住、且没有任何道路通向城镇外部的“孤岛”。DFS 就像派一支搜救队，从某个城镇出发，沿着四条道路（上下左右）把所有相连的城镇找出来，同时检查有没有通向城镇外部的道路（即是否到达矩阵边缘）。

**为什么正确**：  
- 所有相连的 `0` 必然属于同一个岛屿（因为我们只沿四个方向走）。  
- 如果在遍历过程中没有触及边界，说明这块岛屿四周全是 `1`，满足题目 “完全被水包围” 的要求。  

**复杂度分析（大白话）**：  
- 我们会对每个格子最多访问一次（第一次遇到 `0` 时会展开搜索，后面再碰到同一块岛屿的格子时已经被标记为已访问）。所以时间复杂度是 **O(m·n)**，其中 `m`、`n` 分别是矩阵的行数和列数。  
- 额外空间主要是递归栈（DFS）或队列（BFS）保存待访问的格子，最坏情况下会存放整块岛屿的格子数，仍然是 **O(m·n)**（在全部是 `0` 的情况下）。  

#### 代码（Python）

```python
from typing import List

def closedIsland(grid: List[List[int]]) -> int:
    """
    暴力版：遍历每个格子，对未访问的 0 做 DFS，判断是否触及边界
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    # 四个方向的移动向量
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(r: int, c: int) -> bool:
        """
        深度优先搜索，返回该岛屿是否 **没有** 碰到边界
        """
        # 如果走到边界外，说明已经接触到矩阵外部，返回 False（不闭合）
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False

        # 遇到水或已经访问过的格子，直接返回 True（不影响闭合性）
        if grid[r][c] == 1 or visited[r][c]:
            return True

        visited[r][c] = True          # 标记为已访问
        is_closed = True              # 默认该格子所在的岛屿是闭合的

        # 向四个方向继续搜索
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # 如果任意方向返回 False，说明触及边界，整座岛屿都不闭合
            if not dfs(nr, nc):
                is_closed = False

        return is_closed

    closed_cnt = 0
    for i in range(rows):
        for j in range(cols):
            # 找到一个未访问的陆地格子，尝试探索整座岛屿
            if grid[i][j] == 0 and not visited[i][j]:
                if dfs(i, j):          # 如果该岛屿没有触及边界
                    closed_cnt += 1

    return closed_cnt
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` —— 每个格子最多被访问一次。  
- **空间复杂度**：`O(m·n)` —— 递归栈（或显式的 visited 数组）在最坏情况下会占用和网格同等大小的空间。

---  

### 2. 最优解  

#### 思路  

在上面的暴力解中，**瓶颈** 并不在时间，而是 **对每座岛屿都要检查是否碰到边界**。我们可以把这一步“检查是否碰到边界”提前完成：  
1. **先把所有与边界相连的 `0` 都“淹掉”**（把它们变成 `1`），因为这些 `0` 不可能成为闭合岛屿。  
2. 剩下的 `0` 必然是被 `1` 包围的（如果还有未被淹掉的 `0`，它们只能在内部），于是只要 **再次遍历网格，统计剩余连通块的数量** 即可。

这一步的关键是 **从四条边出发，进行一次 BFS/DFS 把所有能到达边界的 `0` 标记掉**。之后的遍历只需要普通的连通块计数，**不再需要每次都判断是否触及边界**，从而代码更简洁，思路更直观。

> **类比**：想象一块土地被围墙（`1`）分割。我们先把所有“漏到外面的”土地（连到边缘的 `0`）用水灌掉，剩下的才是真正被围墙完全包住的“花园”。之后只要数一数还有多少块独立的花园即可。

**核心算法**：**DFS/BFS + 边界预处理**（也可以用并查集实现，但这里用 DFS 更易懂）。  

**复杂度分析**：  
- 第一次从边界开始的搜索最多遍历所有格子一次，第二次遍历统计连通块也最多遍历所有格子一次。总时间仍是 **O(m·n)**。  
- 额外空间只需要一个 `visited`（或直接修改原数组）以及递归栈/队列，最坏也是 **O(m·n)**，但实际使用的空间通常比暴力版更小（因为边界搜索的递归深度受岛屿形状限制）。

#### 代码（Python）

```python
from typing import List

def closedIsland(grid: List[List[int]]) -> int:
    """
    最优解：先把所有连到边界的 0 消除，再统计剩余的闭合岛屿数量
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # ---------- 第一步：从四条边的 0 开始，DFS 把能到达的 0 全部变成 1 ----------
    def dfs_eliminate(r: int, c: int) -> None:
        """把 (r,c) 以及所有相连的 0 改成 1，防止它们被计入闭合岛屿"""
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 1:
            return
        grid[r][c] = 1                     # 直接把它“淹掉”
        for dr, dc in directions:
            dfs_eliminate(r + dr, c + dc)

    # 上下两行
    for col in range(cols):
        dfs_eliminate(0, col)              # 第一行
        dfs_eliminate(rows - 1, col)       # 最后一行
    # 左右两列（去掉已经处理过的四个角，以免重复递归）
    for row in range(1, rows - 1):
        dfs_eliminate(row, 0)              # 第一列
        dfs_eliminate(row, cols - 1)       # 最后一列

    # ---------- 第二步：遍历剩余的 0，统计连通块 ----------
    def dfs_count(r: int, c: int) -> None:
        """把已经确定是闭合岛屿的一块 0 全部标记为 1，防止重复计数"""
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 1:
            return
        grid[r][c] = 1
        for dr, dc in directions:
            dfs_count(r + dr, c + dc)

    closed_cnt = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:            # 只会出现内部的闭合岛屿
                closed_cnt += 1
                dfs_count(i, j)            # 把整块岛屿全部填掉，防止再次计数

    return closed_cnt
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` —— 两次遍历（一次边界消除，一次计数）合在一起仍然是线性时间。  
- **空间复杂度**：`O(m·n)`（递归栈），但因为我们直接在原数组上做标记，额外的 `visited` 数组可以省去，实际使用的额外空间更少。

---  

## 心得  

- **核心技巧**：先把“与边界相连的 0”全部消除，再统计剩余连通块。这个思路把“判断是否闭合”的工作提前到了预处理阶段，使后面的计数变得极其简单。  
- **适用场景**：  
  1. **Closed Islands**（本题）。  
  2. **Number of Enclaves**（LeetCode 1020），同样需要排除与边界相连的陆地。  
  3. **Surrounded Regions**（LeetCode 130），把与边界相连的 `'O'` 变成 `'E'` 再翻转其余 `'O'`。  
- **一句话总结**：**“先把所有‘逃离’的区域清除，再数剩下的岛屿”。**  

## 反思  

- **第一反应**：看到“4‑方向相连的 0”就想到 DFS/BFS，直接在遍历时判断是否碰到边界。  
- **最容易踩的坑**：  
  - 忘记把已经访问过的格子标记，导致无限递归或重复计数。  
  - 边界判断写错（比如只检查左上角或只检查四个方向的一个），会把本该闭合的岛屿误判。  
  - 对于极端情况（全部是 0）需要确保递归深度不会超出 Python 的默认递归限制（可以改用显式栈或 BFS）。  
- **下次类似题目**：第一步先 **“从外向里”** 做一次 Flood Fill，把所有能直接或间接触及边界的区域剔除；随后再 **“从里向外”** 计数剩余的连通块。这样思路更统一，也更不容易漏掉特殊情况。