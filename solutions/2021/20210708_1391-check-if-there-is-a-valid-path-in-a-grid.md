# #1391. 检查网格中是否存在有效路径 / Check if There is a Valid Path in a Grid

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/check-if-there-is-a-valid-path-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n grid. Each cell of grid represents a street. The street of grid[i][j] can be:
You will initially start at the street of the upper-left cell (0, 0). A valid path in the grid is a path that starts from the upper left cell (0, 0) and ends at the bottom-right cell (m - 1, n - 1). The path should only follow the streets.
Notice that you are not allowed to change any street.
Return true if there is a valid path in the grid or false otherwise.

**Examples**

**Example 1:**

```
Input: grid = [[2,4,3],[6,5,2]]
Output: true
Explanation: As shown you can start at cell (0, 0) and visit all the cells of the grid to reach (m - 1, n - 1).
```

**Example 2:**

```
Input: grid = [[1,2,1],[1,2,1]]
Output: false
Explanation: As shown you the street at cell (0, 0) is not connected with any street of any other cell and you will get stuck at cell (0, 0)
```

**Example 3:**

```
Input: grid = [[1,1,2]]
Output: false
Explanation: You will get stuck at cell (0, 1) and you cannot reach cell (0, 2).
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- 1 <= grid[i][j] <= 6

---

## 题目（中文翻译）

给定一个 `m × n` 的网格。网格中的每个单元格表示一条街道。`grid[i][j]` 所表示的街道类型可以是：

你将从左上角单元格 `(0, 0)` 的街道开始。网格中的有效路径是指从左上角单元格 `(0, 0)` 开始并在右下角单元格 `(m - 1, n - 1)` 结束的路径。路径只能沿着街道前进。

> 注意：你不能更改任何街道。

如果网格中存在有效路径返回 `true`，否则返回 `false`。

---

### 示例 1
**输入**  
```json
grid = [[2,4,3],[6,5,2]]
```
**输出**  
```
true
```
**解释**  
如图所示，你可以从单元格 `(0, 0)` 开始，依次访问所有单元格，最终到达 `(m - 1, n - 1)`。

### 示例 2
**输入**  
```json
grid = [[1,2,1],[1,2,1]]
```
**输出**  
```
false
```
**解释**  
如图所示，单元格 `(0, 0)` 的街道与其他任何单元格的街道都不相连，你会卡在 `(0, 0)`。

### 示例 3
**输入**  
```json
grid = [[1,1,2]]
```
**输出**  
```
false
```
**解释**  
你会在单元格 `(0, 1)` 卡住，无法到达单元格 `(0, 2)`。

---

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 300`
- `1 ≤ grid[i][j] ≤ 6`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每一步都尝试走**，就像在迷宫里随手往四个方向摸索。  
- 我们从左上角 `(0,0)` 开始，记录下已经走过的格子，防止原地打转（相当于在走过的路上贴了“已经踩过”的标记）。  
- 在当前格子里，根据它的街道类型（1~6）列出所有可能的出入口方向，然后检查相邻格子是否也有对应的入口。如果可以，就递归/回溯到那个格子继续探索。  
- 当走到右下角 `(m‑1,n‑1)` 时返回 `True`，如果所有可能的分支都走完仍未到达终点则返回 `False`。  

> **生活类比**：把每个格子想成一间房间，房间的门只能朝特定方向开。我们拿着一把钥匙（DFS 递归栈），从入口房间出发，尝试打开每一扇门进入相邻房间，走不通就回头再试别的门。  

这个方法**一定正确**，因为它穷举了所有合法的走法，只要有一条能到终点，就一定会被找到。  

然而，最坏情况下我们会把每条可能的路径都遍历一遍。网格大小最多是 `300 × 300 = 90,000`，而每个格子最多有 2 条出路（实际上最多 2 条），所以路径数会呈指数增长，时间会爆炸。  

#### 代码（Python）  

```python
from typing import List

# 方向向量：上、下、左、右
DIRS = {
    1: [(0, -1), (0, 1)],      # ─ 左右
    2: [(-1, 0), (1, 0)],      # │ 上下
    3: [(1, 0), (0, -1)],      # ┌ 下左
    4: [(-1, 0), (0, -1)],     # └ 上左
    5: [(1, 0), (0, 1)],       # ┐ 下右
    6: [(-1, 0), (0, 1)],      # ┘ 上右
}

# 逆向映射：从相邻格子进入当前格子需要的方向
OPPOSITE = {
    (0, -1): (0, 1),   # 左进 ↔ 右出
    (0, 1):  (0, -1),
    (-1, 0): (1, 0),   # 上进 ↔ 下出
    (1, 0):  (-1, 0),
}

def hasValidPath_bruteforce(grid: List[List[int]]) -> bool:
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]

    def dfs(x: int, y: int) -> bool:
        # 到达终点直接返回 True
        if x == m - 1 and y == n - 1:
            return True
        visited[x][y] = True
        # 当前格子可以向哪些方向走
        for dx, dy in DIRS[grid[x][y]]:
            nx, ny = x + dx, y + dy
            # 越界或已经访问过直接跳过
            if not (0 <= nx < m and 0 <= ny < n) or visited[nx][ny]:
                continue
            # 检查相邻格子是否有对应的入口
            if OPPOSITE[(dx, dy)] in DIRS[grid[nx][ny]]:
                if dfs(nx, ny):
                    return True
        # 所有方向都走不通，回溯
        return False

    return dfs(0, 0)
```

#### 复杂度  

- **时间复杂度**：`O(2^{m*n})`（指数级）  
  > 大白话：在最坏的迷宫里，可能的走法会像树一样不断分叉，树的高度是格子数 `m*n`，每层最多有 2 条分支，所以总步数会呈指数增长。  
- **空间复杂度**：`O(m*n)`  
  > 用来保存 `visited` 表的二维数组以及递归栈的最大深度（最坏也是 `m*n`）。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**不停地回溯**，实际上我们只需要判断“是否能连通”，不必记录每一条具体路径。  
关键观察：  
1. 每个格子只有**固定的几条通路**（上、下、左、右中的两条），这相当于在网格上构造了一张**无向图**。  
2. 只要相邻两个格子的通路能够**相互匹配**，它们就在图中相连。  
3. 问题就转化为：在这张图里，左上角节点和右下角节点是否在同一个连通分量。  

实现上有两种常见思路：  
- **DFS / BFS**：一次遍历把所有能走到的格子标记出来，最后检查右下角是否被标记。  
- **并查集（Union‑Find）**：把每个格子看成一个集合，遍历网格时把相邻且匹配的格子合并，最后判断两个格子是否属于同一个集合。  

这里使用 **DFS（或 BFS）**，因为实现更直观，且同样可以达到 `O(m*n)` 的线性时间。  

实现细节：  
- 仍然使用前面给出的 `DIRS` 与 `OPPOSITE` 表，帮助判断相邻格子是否能够互通。  
- 用 **队列** 实现 BFS，避免递归深度可能的栈溢出（Python 递归深度默认约 1000，网格最大 90,000 可能会爆栈）。  
- 每访问一个格子就把它加入 `visited`，这样每个格子只会被处理一次，整个过程是一次**遍历**。  

> **类比**：把网格想成一张城市地图，街道只能向特定方向通行。我们从起点出发，像警车的 GPS 那样一次性把所有可以到达的路口都标记出来（BFS），最后只要终点也被标记，就说明有路可以开到终点。  

#### 代码（Python）  

```python
from collections import deque
from typing import List

# 与上文相同的方向表
DIRS = {
    1: [(0, -1), (0, 1)],      # ─ 左右
    2: [(-1, 0), (1, 0)],      # │ 上下
    3: [(1, 0), (0, -1)],      # ┌ 下左
    4: [(-1, 0), (0, -1)],     # └ 上左
    5: [(1, 0), (0, 1)],       # ┐ 下右
    6: [(-1, 0), (0, 1)],      # ┘ 上右
}
OPPOSITE = {
    (0, -1): (0, 1),
    (0, 1):  (0, -1),
    (-1, 0): (1, 0),
    (1, 0):  (-1, 0),
}

def hasValidPath(grid: List[List[int]]) -> bool:
    """BFS 版 O(m*n) 解法"""
    m, n = len(grid), len(grid[0])
    # visited 用来避免重复入队
    visited = [[False] * n for _ in range(m)]
    q = deque()
    q.append((0, 0))
    visited[0][0] = True

    while q:
        x, y = q.popleft()
        # 已经到达终点，直接返回 True
        if x == m - 1 and y == n - 1:
            return True
        # 当前格子所有可以走的方向
        for dx, dy in DIRS[grid[x][y]]:
            nx, ny = x + dx, y + dy
            # 越界或已经访问过直接跳过
            if not (0 <= nx < m and 0 <= ny < n) or visited[nx][ny]:
                continue
            # 检查相邻格子是否有对应的入口
            if OPPOSITE[(dx, dy)] in DIRS[grid[nx][ny]]:
                visited[nx][ny] = True   # 标记已访问
                q.append((nx, ny))       # 加入队列继续扩散

    # BFS 结束仍未到终点，说明不可达
    return False
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  > 每个格子最多检查两条出路，且只会被加入队列一次，整个遍历过程正比于格子总数。  
- **空间复杂度**：`O(m * n)`  
  > `visited` 数组和队列最坏情况下会同时保存整个网格的状态。  

相较于暴力解，时间从指数级降到了线性，几乎可以在瞬间处理最大规模的输入。  

---  

## 心得  

- **核心技巧**：把“街道连通性”抽象为 **图的连通性**，利用 **BFS/DFS**（或并查集）一次遍历即能判断两点是否在同一个连通分量。  
- **适用的题型**：  
  1. “岛屿数量”“最大岛屿面积”等需要判断相邻格子是否相连的网格题。  
  2. “迷宫最短路径”“岛屿的周长”等需要在网格上做搜索的题目。  
- **解题钥匙**：**先把问题转化为图的遍历**，再选择最合适的遍历/并查集实现。  

---  

## 反思  

- **第一反应**：看到每种街道只能向固定方向走，立刻想到“把格子当成节点、方向当成边”，于是想用 DFS 暴力搜索。  
- **最容易踩的坑**：  
  - 忘记检查**相邻格子的入口是否匹配**，只判断当前格子能否向某方向走会导致错误的“伪连通”。  
  - 边界条件：网格只有一行或一列时，仍需正常判断首尾是否相连。  
  - 使用递归时可能会因栈深度超限而报错。  
- **下次第一步**：先**画出街道的方向表**（如上 `DIRS`），确认两格子之间的**双向匹配**条件，然后决定使用 BFS/DFS 还是并查集一次遍历。