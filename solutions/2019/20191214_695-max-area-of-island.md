# #695. 岛屿的最大面积 / Max Area of Island

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/max-area-of-island/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
The area of an island is the number of cells with a value 1 in the island.
Return the maximum area of an island in grid. If there is no island, return 0.

**Examples**

**Example 1:**

```
Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
Output: 6
Explanation: The answer is not 11, because the island must be connected 4-directionally.
```

**Example 2:**

```
Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

你得到一个 `m x n` 的二进制矩阵（binary matrix） `grid`。岛屿（island）是由值为 `1` 的单元格组成的集合，且这些单元格在水平方向或垂直方向上相连（4‑方向相连）。可以假设矩阵的四条边界之外全是水。

岛屿的面积是该岛屿中值为 `1` 的单元格数量。

返回 `grid` 中岛屿的最大面积。如果不存在岛屿，返回 `0`。

**示例 1**

```
Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],
               [0,0,0,0,0,0,0,1,1,1,0,0,0],
               [0,1,1,0,1,0,0,0,0,0,0,0,0],
               [0,1,0,0,1,1,0,0,1,0,1,0,0],
               [0,1,0,0,1,1,0,0,1,1,1,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0,1,1,1,0,0,0],
               [0,0,0,0,0,0,0,1,1,0,0,0,0]]
Output: 6
Explanation: 答案不是 11，因为岛屿必须是 4‑方向相连的。
```

**示例 2**

```
Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0
```

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 50`
- `grid[i][j]` 只能是 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**“每个 1 都当作起点，去把它所在的岛全部走一遍，算出面积，然后把所有起点的面积取最大”。**  

- **数据结构**：我们仍然在原矩阵 `grid` 上进行遍历。为了“走岛”，常用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）**。可以把 DFS 想成“在迷宫里不停往前走，走到尽头再回头”，BFS 则像“每次向四周扩散一次”。  
- **为什么正确**：只要我们从某个 `grid[i][j] == 1` 开始，沿着上下左右四个方向把所有相连的 `1` 访问到，就恰好遍历了这座岛的全部格子，计数得到的就是这座岛的面积。遍历完所有格子后，最大值自然就是答案。  

**暴力实现的“坑”**在于**每次都重新遍历整座岛**。假设岛有 `k` 个格子，第一次从岛里的某个格子出发会遍历 `k` 次；第二次再从岛里另一个格子出发，又会再次遍历这 `k` 个格子，导致大量重复工作。最坏情况下（所有格子都是陆地），会产生 `O((m·n)²)` 的时间。

#### 代码（Python）

```python
from collections import deque
from typing import List

def maxAreaOfIsland(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    max_area = 0                     # 记录最大岛屿面积

    # 四个方向的移动向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # ---------- 暴力 DFS ----------
    def dfs(i: int, j: int) -> int:
        """从 (i, j) 开始，深度优先遍历连通的 1，返回该岛屿面积"""
        # 越界或遇到水直接返回 0
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
            return 0
        # 把当前格子“标记”为已访问，防止本次递归再次进入
        grid[i][j] = 0
        area = 1                      # 当前格子算 1
        for di, dj in dirs:           # 向四个方向继续搜索
            area += dfs(i + di, j + dj)
        return area

    # 对每一个格子都尝试一次 DFS（即使已经被标记为 0 也会被检查）
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:       # 只对陆地格子启动搜索
                # 这里会把整座岛屿全部改为 0，后面再遇到同一座岛时会直接跳过
                cur_area = dfs(i, j)
                max_area = max(max_area, cur_area)

    return max_area
```

> **注意**：这段代码在每次遍历到 `1` 时都会把整座岛全部“涂成 0”，所以同一座岛只会被计数一次。**这其实已经是最优的**，但如果我们把 “标记为已访问” 的步骤去掉（即每次都重新遍历整座岛），时间复杂度就会退化到 `O((m·n)²)`，这才是真正的暴力写法。这里保留了标记的写法，只是为了让代码仍能跑通。

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 每个格子最多被访问一次（第一次遇到 1 时会被 DFS 抹成 0），所以总的递归/循环次数与格子数成线性关系。  
  - 如果不做“已访问”标记，最坏会是 `O((m·n)²)`，因为每个 `1` 都会重复遍历整座岛屿。  
- **空间复杂度**：`O(m·n)`（递归栈）  
  - 在最坏情况下（全是陆地），DFS 的递归深度会等于格子总数，即占用 `m·n` 的栈空间。使用显式的 BFS 队列时同样会有类似的额外空间。

---

### 2. 最优解

#### 思路  

从暴力解我们已经看到 **“重复遍历同一座岛屿”** 是性能瓶颈。要想更快，只需要**确保每座岛只遍历一次**。实现思路如下：

1. **遍历矩阵**，一旦发现 `grid[i][j] == 1`（未被访问的陆地），说明找到了一个新岛的入口。  
2. **用 DFS（或 BFS）把这座岛的所有格子全部遍历并标记为 0**，同时计数得到该岛的面积。  
3. 把得到的面积与当前最大值比较，更新答案。  

这就是**“一次遍历 + 标记已访问”**的典型做法。这里不需要额外的 `visited` 数组，只要把遍历过的 `1` 改成 `0`（或 `-1`），即可在后续的遍历中直接跳过。

> **核心技巧**：** flood fill（填色）**。想象你手里有一把水彩笔，遇到同一种颜色的相邻格子就把它们全部染成另一种颜色，这样以后再看到旧颜色时就知道已经处理过了。

下面给出两种实现方式：**递归版 DFS**（代码更简洁）和 **显式队列的 BFS**（避免递归深度限制）。两者时间、空间复杂度相同。

#### 代码（Python）

```python
from collections import deque
from typing import List

def maxAreaOfIsland(grid: List[List[int]]) -> int:
    """
    返回 grid 中最大的岛屿面积。如果没有岛屿则返回 0。
    思路：遍历每个格子，遇到未访问的陆地 (1) 时，用 BFS/DFS 把整座岛涂成 0，
    同时累计该岛的格子数，更新最大值。
    """
    m, n = len(grid), len(grid[0])
    max_area = 0
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # ---------- BFS 实现 ----------
    def bfs(sr: int, sc: int) -> int:
        """从 (sr, sc) 开始，用队列把连通的 1 全部遍历，返回岛屿面积"""
        queue = deque()
        queue.append((sr, sc))
        grid[sr][sc] = 0               # 立刻标记为已访问，防止重复入队
        area = 0

        while queue:
            r, c = queue.popleft()
            area += 1                  # 走到一个陆地格子，面积 +1
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # 检查四邻域是否仍是未访问的陆地
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 0   # 标记为已访问
                    queue.append((nr, nc))
        return area

    # ---------- 主循环 ----------
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:         # 发现新岛的入口
                cur = bfs(i, j)         # 计算该岛面积并把它全部“抹掉”
                max_area = max(max_area, cur)

    return max_area
```

> 如果你更喜欢递归写法，只需要把 `bfs` 换成下面的 `dfs`，逻辑完全相同：

```python
def dfs(r: int, c: int) -> int:
    if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
        return 0
    grid[r][c] = 0          # 标记已访问
    area = 1
    for dr, dc in dirs:
        area += dfs(r + dr, c + dc)
    return area
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 每个格子最多被访问一次（第一次遇到 `1` 时被 BFS/DFS 把它改为 `0`），所以整体遍历次数等于格子总数。  
  - 与暴力解相比，省去了重复遍历同一岛屿的开销。  

- **空间复杂度**：`O(min(m·n, 4·max(m, n)))`（取决于实现）  
  - **BFS**：队列中最多同时保存一层的格子数，最坏情况下（比如整张矩阵全是陆地）会接近 `m·n`。  
  - **DFS（递归）**：递归栈深度同样可能达到 `m·n`，但在 Python 中递归层数受限，实际使用时可以改成显式栈或 BFS。  
  - 这里的空间主要是 **额外的**，不包括原始矩阵本身。

---

## 心得

- **核心技巧**：**Flood Fill（填色）+ 访问标记**。只要把每座岛屿遍历一次并在遍历过程中把它“刷掉”，就能在一次线性扫描中求出最大面积。  
- **适用的题型**  
  1. **岛屿类**：`Number of Islands`、`Max Area of Island`、`Island Perimeter`。  
  2. **连通块计数**：`Count Sub Islands`、`Surrounded Regions`（四方向或八方向）。  
  3. **图的遍历**：任何需要统计/搜索连通分量的网格或图问题。  
- **一句话总结**：**“遇到未访问的 1，就从这里开始一次完整的填色，期间把所有 1 都标记掉，最大面积自然是所有填色得到的最大计数。”**

---

## 反思

- **第一反应**：看到“4‑方向相连的 1”就想到“用 DFS/BFS 把岛屿全部走一遍”。  
- **最容易踩的坑**  
  1. **忘记标记已访问**：导致同一座岛屿被多次计数，时间爆炸。  
  2. **越界检查不全**：在四方向扩展时一定要判断 `0 ≤ nr < m`、`0 ≤ nc < n`。  
  3. **递归深度**：在全陆地的极端情况下递归层数会很深，Python 可能报 `RecursionError`，此时改用显式栈或 BFS。  
- **下次类似题的第一步**：**先在纸上画一个小网格，手动做一次“填色”**，确认四方向的连通规则，然后决定用 BFS（安全）还是 DFS（简洁）实现。这样可以快速定位核心思路，避免在实现细节上走弯路。