# #463. 岛屿周长 / Island Perimeter

> 难度：简单 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/island-perimeter/)

---

## 题目（英文原版）

**Description**

You are given row x col grid representing a map where grid[i][j] = 1 represents land and grid[i][j] = 0 represents water.
Grid cells are connected horizontally/vertically (not diagonally). The grid is completely surrounded by water, and there is exactly one island (i.e., one or more connected land cells).
The island doesn't have "lakes", meaning the water inside isn't connected to the water around the island. One cell is a square with side length 1. The grid is rectangular, width and height don't exceed 100. Determine the perimeter of the island.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]
Output: 16
Explanation: The perimeter is the 16 yellow stripes in the image above.
```

**Example 2:**

```
Input: grid = [[1]]
Output: 4
```

**Example 3:**

```
Input: grid = [[1,0]]
Output: 4
```

**Constraints**

- row == grid.length
- col == grid[i].length
- 1 <= row, col <= 100
- grid[i][j] is 0 or 1.
- There is exactly one island in grid.

---

## 题目（中文翻译）

给定一个 `row × col` 的网格（grid），其中 `grid[i][j] = 1` 表示陆地，`grid[i][j] = 0` 表示水域。网格单元格（cell）仅在水平或垂直方向相连（不考虑对角线相连）。整个网格四周被水包围，并且恰好存在一个岛屿（island），即一个或多个相连的陆地单元格。该岛屿内部没有“湖泊”，即岛屿内部的水域不与外部水域相连。每个单元格是边长为 1 的正方形。网格是矩形的，宽度和高度均不超过 100。请计算该岛屿的周长（perimeter）。

**示例 1**  
**输入**: `grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]`  
**输出**: `16`  
**解释**: 周长即图中 16 条黄色边界的总长度。

**示例 2**  
**输入**: `grid = [[1]]`  
**输出**: `4`  

**示例 3**  
**输入**: `grid = [[1,0]]`  
**输出**: `4`  

**约束条件**  
- `row == grid.length`  
- `col == grid[i].length`  
- `1 <= row, col <= 100`  
- `grid[i][j]` 仅为 `0` 或 `1`。  
- 网格中恰好存在一个岛屿。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一块陆地当成一块正方形**，它本身有 4 条边。  
如果这条边的相邻格子是水或者已经超出地图边界，那么这条边就算进岛屿的周长；  
如果相邻格子也是陆地，那么这两块正方形之间会共享一条边，这条边 **不算** 周长。

可以把 “相邻格子是水” 想象成 **在字典里查单词**：  
- 这里的“字典”是四个方向（上、下、左、右）  
- “单词”是相邻格子的坐标  
- “查不到” 就说明相邻格子是水或越界 → 这条边要计入周长  

遍历整个矩阵，对每个为 `1`（陆地）的格子检查它的四个方向即可得到答案。

#### 代码（Python）

```python
from typing import List

def islandPerimeter(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    perimeter = 0                       # 最终的周长

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:          # 只处理陆地格子
                # 四个方向依次检查：上、下、左、右
                # 如果越界或相邻格子是水，就把这条边计入周长
                # 上
                if r == 0 or grid[r-1][c] == 0:
                    perimeter += 1
                # 下
                if r == rows-1 or grid[r+1][c] == 0:
                    perimeter += 1
                # 左
                if c == 0 or grid[r][c-1] == 0:
                    perimeter += 1
                # 右
                if c == cols-1 or grid[r][c+1] == 0:
                    perimeter += 1
    return perimeter
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`（其中 `m` 为行数，`n` 为列数）  
  大白话：我们只需要 **遍历一次** 整个矩阵，对每个格子做常数次（最多 4 次）检查，所以工作量和格子总数成正比。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量来记录行列数和周长，不会随输入大小而增长。

---

### 2. 最优解

#### 思路  

上面的直觉解已经是 **线性时间**，已经很快了。但我们可以把它改写成 **深度优先搜索（DFS）** 的形式，让思路更贴近 “岛屿遍历” 这种常见的图论问题。

**瓶颈在哪？**  
- 其实没有明显的性能瓶颈，因为每个格子只会被检查一次。  
- 但是如果我们把“检查四个方向”写成 **递归遍历**，代码结构会更清晰：只在岛屿内部递归，而不必遍历整张地图。

**核心思想**：  
1. 从任意一块陆地格子出发，用 DFS 把整座岛屿的所有陆地格子走遍。  
2. 对每个访问到的陆地格子，同样检查它的四条边：  
   - 若邻居是水或越界，则这条边贡献 `1` 到周长。  
   - 若邻居也是陆地且未被访问，则继续递归遍历。  

**类比**：想象你站在岛上，每走到一块新的土地，就把四周的“围墙”数一遍；如果前面还有未踏足的土地，就继续前进，直到把整座岛走完。

#### 代码（Python）

```python
from typing import List

def islandPerimeter(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]   # 记录哪些陆地已经遍历过
    perimeter = 0

    # 定义 DFS，返回从 (r, c) 出发能够贡献的周长
    def dfs(r: int, c: int) -> None:
        nonlocal perimeter
        visited[r][c] = True

        # 四个方向的增量
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # 如果越界或是水，则当前格子在该方向有一条外边界
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] == 0:
                perimeter += 1
            # 如果是陆地且还没访问过，继续递归
            elif not visited[nr][nc]:
                dfs(nr, nc)

    # 找到任意一个陆地格子作为入口
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                dfs(i, j)          # 从这里开始遍历整座岛
                return perimeter   # 只会有唯一的一座岛，遍历完直接返回

    return 0  # 按题意不会走到这里
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  只会递归遍历岛屿内部的格子，每个格子最多被访问一次，和暴力解的遍历次数相同。

- **空间复杂度**：`O(m·n)`（最坏情况）  
  需要一个与地图同大小的 `visited` 矩阵来记录访问状态，此外递归栈深度最多等于岛屿格子数。  
  对于本题的最大规模（100×100），这完全在可接受范围内。

---

## 心得

- **核心技巧**：把“每块陆地的四条边”拆成 “若相邻是水或越界则计数”——相当于把几何的“周长”转化为离散格子之间的“相邻关系”。  
- **适用的题型**：  
  1. **岛屿周长**（本题）  
  2. **岛屿数量**（Number of Islands）——同样需要遍历相连的陆地块  
  3. **最大岛屿面积**（Max Area of Island）——DFS/BFS 统计连通块大小  

> **解题钥匙**：把每块格子想成四面小墙，只有面对水或地图边缘的墙才算进总长度。

## 反思

- **第一反应**：看到“岛屿”“周长”，立刻想到“每块陆地四条边”以及“相邻的两块陆地会抵消一条边”。  
- **最容易踩的坑**：  
  - 忘记检查 **上边界**、**左边界**、**下边界**、**右边界**（越界也算水）。  
  - 题目保证只有一座岛，但如果代码没有提前退出，可能会重复计数。  
  - 在 DFS 实现中，如果不使用 `visited`，会产生无限递归（死循环）。  
- **下次思路**：遇到类似“连通块的属性”题目，先问自己  
  1. “每个单元格的局部贡献是什么？”  
  2. “相邻单元格之间会产生怎样的抵消或叠加？”  
  这两个问题往往能直接指向最简洁的 O(m·n) 解法。