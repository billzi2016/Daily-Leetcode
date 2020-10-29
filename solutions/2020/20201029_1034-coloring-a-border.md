# #1034. 染色边界 / Coloring A Border

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/coloring-a-border/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid, and three integers row, col, and color. Each value in the grid represents the color of the grid square at that location.
Two squares are called adjacent if they are next to each other in any of the 4 directions.
Two squares belong to the same connected component if they have the same color and they are adjacent.
The border of a connected component is all the squares in the connected component that are either adjacent to (at least) a square not in the component, or on the boundary of the grid (the first or last row or column).
You should color the border of the connected component that contains the square grid[row][col] with color.
Return the final grid.

**Examples**

**Example 1:**

```
Input: grid = [[1,1],[1,2]], row = 0, col = 0, color = 3
Output: [[3,3],[3,2]]
```

**Example 2:**

```
Input: grid = [[1,2,2],[2,3,2]], row = 0, col = 1, color = 3
Output: [[1,3,3],[2,3,3]]
```

**Example 3:**

```
Input: grid = [[1,1,1],[1,1,1],[1,1,1]], row = 1, col = 1, color = 2
Output: [[2,2,2],[2,1,2],[2,2,2]]
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- 1 <= grid[i][j], color <= 1000
- 0 <= row < m
- 0 <= col < n

---

## 题目（中文翻译）

给定一个 `m x n` 整数矩阵（matrix）`grid`，以及三个整数 `row`、`col` 和 `color`。`grid` 中的每个值表示对应格子的颜色。

- 两个格子如果在上下左右四个方向中的任意一个方向相邻（adjacent），则称它们是相邻的。  
- 如果两个格子颜色相同且相邻，则它们属于同一个连通分量（connected component）。  
- 连通分量的边界（border）指的是该连通分量中所有满足以下任意条件的格子：  
  1. 与至少一个不在该连通分量中的格子相邻（adjacent）；  
  2. 或位于矩阵的最外层边界（即第一行、最后一行、第一列或最后一列）。

请将包含格子 `grid[row][col]` 的连通分量的边界全部染成给定的 `color`，并返回最终的矩阵。

## 示例

### 示例 1
**输入**  
```
grid = [[1,1],[1,2]], row = 0, col = 0, color = 3
```
**输出**  
```
[[3,3],[3,2]]
```

### 示例 2
**输入**  
```
grid = [[1,2,2],[2,3,2]], row = 0, col = 1, color = 3
```
**输出**  
```
[[1,3,3],[2,3,3]]
```

### 示例 3
**输入**  
```
grid = [[1,1,1],[1,1,1],[1,1,1]], row = 1, col = 1, color = 2
```
**输出**  
```
[[2,2,2],[2,1,2],[2,2,2]]
```

## 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 50`
- `1 <= grid[i][j], color <= 1000`
- `0 <= row < m`
- `0 <= col < n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个格子都检查一遍**，看它是不是和 `grid[row][col]` 所在的连通块属于同一块儿。  
具体做法：

1. 记下起始格子的颜色 `origin = grid[row][col]`。  
2. 对矩阵里的每个位置 `(i, j)`，如果它的颜色恰好是 `origin`，就**从这里开始一次深度优先搜索**（DFS）或广度优先搜索（BFS），只走颜色相同的格子，看看能否走到起始格子 `(row, col)`。  
3. 能走到的格子就是连通块的一部分。再对这些格子逐个检查：  
   - 如果格子在矩阵边界上（第一行、最后一行、第一列、最后一列），或  
   - 它的四个相邻格子中有任意一个颜色不同（或越界），  
   那么这个格子就是**边界格子**。  
4. 把所有找到的边界格子统一改成 `color`，其余格子保持不变。  

> **类比**：想象你在一张地图上找所有和你所在城市颜色相同的城市，然后逐个走路去看能否回到自己所在的城市。如果能回，就说明它们在同一个“同色连通块”。再把那些靠近不同颜色或边界的城市标记出来。

**为什么正确**：  
- 第 2 步保证了只有和起始格子颜色相同且相互可达的格子才会被认为是同一连通块。  
- 第 3 步正好对应题目对“边界格子”的定义：只要有邻居不是同块或在矩阵外，就是边界。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def colorBorder_bruteforce(grid: List[List[int]],
                          row: int, col: int, color: int) -> List[List[int]]:
    m, n = len(grid), len(grid[0])
    origin = grid[row][col]               # 起始格子的颜色
    border = []                           # 用来保存所有需要染色的格子

    # ---------- 第一步：遍历每个格子 ----------
    for i in range(m):
        for j in range(n):
            if grid[i][j] != origin:      # 颜色不同的直接跳过
                continue

            # ---------- 第二步：从 (i,j) 做一次 BFS 看能否到达 (row,col) ----------
            visited = [[False] * n for _ in range(m)]
            q = deque([(i, j)])
            visited[i][j] = True
            reachable = False

            while q:
                x, y = q.popleft()
                if x == row and y == col:   # 能到达起始格子，说明在同一连通块
                    reachable = True
                    break
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n \
                       and not visited[nx][ny] \
                       and grid[nx][ny] == origin:
                        visited[nx][ny] = True
                        q.append((nx, ny))

            if not reachable:               # 不是同块的格子，直接跳过
                continue

            # ---------- 第三步：判断 (i,j) 是否是边界 ----------
            is_border = False
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = i + dx, j + dy
                # 越界或相邻格子颜色不同，都算边界
                if not (0 <= nx < m and 0 <= ny < n) or grid[nx][ny] != origin:
                    is_border = True
                    break
            if is_border:
                border.append((i, j))

    # ---------- 第四步：统一染色 ----------
    for x, y in border:
        grid[x][y] = color

    return grid
```

#### 复杂度  

- **时间复杂度**：`O((m·n)²)`  
  - 外层遍历所有格子是 `m·n` 次。  
  - 对每个符合颜色的格子，又要跑一次 BFS，最坏情况下会遍历整个矩阵 `m·n`，于是总体是平方级。  
  - 用大白话说，就是如果矩阵是 50×50（最大），大约要跑 2500 × 2500 ≈ 6 250 000 次操作，稍显吃力。  

- **空间复杂度**：`O(m·n)`  
  - 每次 BFS 都要新建一个 `visited` 矩阵，最坏占用整个矩阵的大小。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**重复的 BFS 是性能瓶颈**：我们对每个同色格子都重新遍历整块连通区域，导致大量重复工作。  
其实，只需要**一次遍历**就能把整块连通区域找出来，并顺便判断每个格子是否是边界。

关键点：

1. **一次 DFS（或 BFS）把连通块全部标记**。  
   - 从起始格子 `(row, col)` 出发，只往颜色相同的相邻格子走。  
   - 用 `visited` 数组记录已经走过的格子，防止回头。  

2. **在 DFS 过程中判断是否是边界**。  
   - 对当前格子 `(x, y)`，检查四个方向的相邻格子：  
     - 若相邻格子 **越界**（在矩阵外） → 当前格子必是边界。  
     - 若相邻格子 **颜色不同** 且 **未被访问** → 也说明当前格子是边界。  
   - 如果以上任意一种情况成立，就把 `(x, y)` 加入 `border` 列表。  

3. **遍历结束后统一染色**。  
   - 只改 `border` 中的格子颜色，其他格子保持原样。  

> **类比**：想象你从起点出发，用一根绳子把所有相同颜色、相连的格子“拉住”。拉的过程中，只要发现绳子碰到墙（矩阵边界）或不同颜色的格子，就把这根绳子标记为“边界绳”。最后把所有“边界绳”换上新颜色。  

#### 代码（Python）

```python
from typing import List

def colorBorder(grid: List[List[int]],
               row: int, col: int, color: int) -> List[List[int]]:
    m, n = len(grid), len(grid[0])
    origin = grid[row][col]          # 起始颜色
    visited = [[False] * n for _ in range(m)]
    border = []                      # 保存所有需要染色的格子

    def dfs(x: int, y: int) -> None:
        """深度优先遍历连通块，同时判断 (x,y) 是否为边界"""
        visited[x][y] = True
        is_border = False

        # 四个方向的增量
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            # 1️⃣ 越界 → 当前格子是边界
            if not (0 <= nx < m and 0 <= ny < n):
                is_border = True
                continue
            # 2️⃣ 相邻格子颜色不同 → 当前格子是边界
            if grid[nx][ny] != origin:
                is_border = True
                continue
            # 3️⃣ 相邻格子颜色相同且未访问 → 继续递归
            if not visited[nx][ny]:
                dfs(nx, ny)

        if is_border:
            border.append((x, y))

    # 从起点开始一次完整的 DFS
    dfs(row, col)

    # 把所有边界格子改成目标颜色
    for x, y in border:
        grid[x][y] = color

    return grid
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 每个格子最多被访问一次（进入 `dfs`），所以总操作次数和矩阵大小成线性关系。  
  - 与暴力解相比，从平方级降到了线性级，速度快了很多。  

- **空间复杂度**：`O(m·n)`  
  - `visited` 数组占用 `m·n` 的空间，递归栈最坏也会有 `m·n` 深度（实际一般远小于此）。  
  - 这在题目给出的 50×50 的限制下完全可以接受。

---

## 心得  

- **核心技巧**：一次遍历（DFS/BFS）同时完成连通块的寻找和边界判定。  
- **适用题型**：  
  1. **岛屿/连通块的边界染色**（如本题）。  
  2. **“围绕”类题目**——把被某种颜色包围的区域找出来（如 LeetCode 130. 被围绕的地区）。  
  3. **矩阵中的区域计数**（如 LeetCode 200. 岛屿数量）——只需要一次 DFS/BFS。  
- **一句话总结**：**“一次遍历，边走边标记边界”，是处理同色连通块的通用钥匙。**  

---

## 反思  

- **第一反应**：看到“连通块”和“边界”，自然想到先把整块找出来（DFS/BFS），再单独遍历判断边界。  
- **最容易踩的坑**：  
  - **边界条件**：格子位于矩阵最外层时，四个方向的检查会越界，需要先判断 `0 <= nx < m`、`0 <= ny < n`。  
  - **颜色修改的时机**：如果在 DFS 过程中直接改颜色，后续相邻格子的颜色判断会被破坏，导致错误的连通块划分。正确做法是**先收集所有边界格子**，最后一次性染色。  
  - **递归深度**：在极端情况下（如全是同色的大矩阵），递归深度可能达到 `m·n`，在 Python 中会触发递归深度限制。可以改用显式栈的 BFS，或在实际面试中说明这一点。  
- **下次第一步**：  
  - 确认 **“同色相邻”** 的定义，用 **一次 DFS/BFS** 把连通块全部标记出来；  
  - 在遍历的同时 **判断每个格子是否触及不同颜色或矩阵边缘**，把符合条件的格子加入结果集合。