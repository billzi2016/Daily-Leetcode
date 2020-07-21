# #934. 最短桥 / Shortest Bridge

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/shortest-bridge/)

---

## 题目（英文原版）

**Description**

You are given an n x n binary matrix grid where 1 represents land and 0 represents water.
An island is a 4-directionally connected group of 1's not connected to any other 1's. There are exactly two islands in grid.
You may change 0's to 1's to connect the two islands to form one island.
Return the smallest number of 0's you must flip to connect the two islands.

**Examples**

**Example 1:**

```
Input: grid = [[0,1],[1,0]]
Output: 1
```

**Example 2:**

```
Input: grid = [[0,1,0],[0,0,0],[0,0,1]]
Output: 2
```

**Example 3:**

```
Input: grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
Output: 1
```

**Constraints**

- n == grid.length == grid[i].length
- 2 <= n <= 100
- grid[i][j] is either 0 or 1.
- There are exactly two islands in grid.

---

## 题目（中文翻译）

给定一个 `n × n` 的二进制矩阵（binary matrix）`grid`，其中 `1` 表示陆地，`0` 表示水域。  
岛屿（island）是由 **四方向连通**（4-directionally）的 `1` 组成的连通块，且不与其他 `1` 相连。矩阵中恰好存在两个岛屿。  

你可以将 `0` 改为 `1`，从而连接这两个岛屿，使其成为同一个岛屿。  
返回为了连接两个岛屿而必须翻转的 `0` 的最少数量。

**示例 1**  
输入: `grid = [[0,1],[1,0]]`  
输出: `1`

**示例 2**  
输入: `grid = [[0,1,0],[0,0,0],[0,0,1]]`  
输出: `2`

**示例 3**  
输入: `grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]`  
输出: `1`

**约束条件**

- `n == grid.length == grid[i].length`
- `2 <= n <= 100`
- `grid[i][j]` 只能是 `0` 或 `1`
- 矩阵中恰好有两个岛屿

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **先把两个岛分别找出来**  
   - 只要相邻的 `1`（上下左右）连在一起，就算同一个岛。  
   - 用「深度优先搜索」DFS 把每个岛的所有陆地格子收集到两个列表 `island1`、`island2` 中。  
   - 这里可以把 DFS 想象成「在地图上画线」，从一个陆地格子出发，不断向四周扩散，把所有能走到的陆地都涂成同一种颜色。

2. **枚举所有可能的桥**  
   - 桥的长度等于两块陆地之间跨过的 `0` 的个数。  
   - 对于任意 `island1` 中的格子 `(x1, y1)` 与 `island2` 中的格子 `(x2, y2)`，它们之间的最短路径（只能走上下左右）长度是 Manhattan 距离 `|x1‑x2| + |y1‑y2|`。  
   - 但是两块陆地本身已经算在距离里了，所以实际要翻的 `0` 的数量是 `distance‑1`。  
   - 把所有配对的距离算一遍，取最小值就是答案。

> **为什么正确？**  
> 因为在只允许上下左右移动的网格里，两块陆地之间的最短路径一定是沿着直线走的 Manhattan 距离；而我们只需要把水格子变成陆地，陆地本身不需要翻转，所以减去 1。

#### 代码（Python）

```python
from typing import List
import sys

def shortestBridge(grid: List[List[int]]) -> int:
    n = len(grid)
    # 四个方向
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # ---------- 第一步：DFS 找出两个岛 ----------
    visited = [[False]*n for _ in range(n)]
    islands = []                     # 最终会得到 [[(x,y), ...], [(x,y), ...]]

    def dfs(x: int, y: int, cur: List[tuple]) -> None:
        """把 (x,y) 所在的岛全部收集进 cur"""
        visited[x][y] = True
        cur.append((x, y))
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == 1:
                dfs(nx, ny, cur)

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and not visited[i][j]:
                cur_island = []
                dfs(i, j, cur_island)
                islands.append(cur_island)
                if len(islands) == 2:   # 题目保证恰好两个岛
                    break
        if len(islands) == 2:
            break

    island1, island2 = islands[0], islands[1]

    # ---------- 第二步：枚举配对，计算最小 Manhattan 距离 ----------
    ans = sys.maxsize
    for x1, y1 in island1:
        for x2, y2 in island2:
            # Manhattan 距离减 1 就是需要翻的 0 的个数
            dist = abs(x1 - x2) + abs(y1 - y2) - 1
            ans = min(ans, dist)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(k1 * k2)`，其中 `k1`、`k2` 分别是两个岛的格子数。最坏情况下每个岛几乎占满整个 `n×n` 矩阵，复杂度接近 `O(n^4)`（因为 `k1,k2 ≈ n^2`），这就是“暴力”之所以慢的原因。  
- **空间复杂度**：`O(n^2)`，主要是 `visited` 数组和保存两个岛所有坐标的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于两岛之间所有配对的距离计算**——我们不必把每一对都算一遍，只要找到最近的那一对即可。  
我们可以把这个过程看成“**从第一个岛向外扩散**”，一步一步把水变成陆地，直到碰到第二个岛。最先碰到的那一次扩散层数，就是最小需要翻转的 `0` 的个数。

实现步骤：

1. **定位并标记第一个岛**（同上，用 DFS）  
   - 把第一个岛的所有格子改成 `2`（或者放进队列），同时把这些格子加入 **多源 BFS 的起点**。  
   - 想象成「把第一个岛的每块陆地都装上了探照灯」，它们一起向四周发射“波纹”。

2. **广度优先搜索（BFS）**  
   - 从所有起点（第一个岛的每块陆地）同时向四周扩散，一层层地把相邻的 `0` 变成 `2` 并记录层数（即已经翻的水的数量）。  
   - 当 BFS 第一次碰到原始值为 `1` 的格子（属于第二个岛）时，当前层数就是答案。  
   - 因为 BFS 按层次进行，第一次到达第二个岛的路径一定是最短的。

3. **为什么 BFS 能得到最短桥**  
   - BFS 的特性是「先到达的节点一定是距离起点最近的」，这里的「距离」指的是需要翻的水格子数。  
   - 多源 BFS 把整个第一个岛视为同一层的起点，相当于从岛的所有边缘同时出发，保证不管桥从哪个边缘建，都能在最短时间内被发现。

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortestBridge(grid: List[List[int]]) -> int:
    n = len(grid)
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # ---------- 第一步：DFS 找到第一个岛并把它的坐标加入队列 ----------
    visited = [[False]*n for _ in range(n)]
    q = deque()                     # BFS 的队列，里面先放第一个岛的所有格子

    def dfs(x: int, y: int) -> None:
        """把 (x,y) 所在的岛全部标记为 2，并加入队列"""
        visited[x][y] = True
        grid[x][y] = 2              # 用 2 表示已经属于第一岛
        q.append((x, y))
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == 1:
                dfs(nx, ny)

    # 找到第一个 1，启动 DFS
    found = False
    for i in range(n):
        if found:
            break
        for j in range(n):
            if grid[i][j] == 1:
                dfs(i, j)
                found = True
                break

    # ---------- 第二步：多源 BFS ----------
    steps = 0                       # 已经翻的 0 的层数
    while q:
        # 本层所有节点一起扩散
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0 <= nx < n and 0 <= ny < n:
                    if grid[nx][ny] == 1:        # 碰到第二个岛
                        return steps
                    if grid[nx][ny] == 0:        # 还是水，继续扩散
                        grid[nx][ny] = 2         # 标记已访问，防止重复加入
                        q.append((nx, ny))
        steps += 1                     # 完成一层，桥长+1
    return -1  # 理论上不会走到这里
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - DFS 只遍历第一个岛的格子，最多 `n²` 次。  
  - BFS 最多把所有 `0` 变成 `2`，同样最多遍历 `n²` 次。  
  - 两个过程加起来仍是线性级别的，远快于暴力的 `O(n⁴)`。

- **空间复杂度**：`O(n²)`。  
  - `visited`、`grid` 本身占 `n²` 空间。  
  - 队列最坏情况下会存储整张矩阵的格子，也就是 `O(n²)`。

---

## 心得

- **核心技巧**：**多源 BFS**（从整个岛的边缘同时向外扩散）+ **DFS 标记岛屿**。  
- **适用的题型**  
  1. “岛屿之间的最短桥”系列（如本题）。  
  2. “最小岛屿面积”或 “岛屿周长” 类题目，需要先标记岛屿再 BFS/DFS。  
  3. “从多个起点到达目标的最短路径”——例如 **01 矩阵** 中的最近 0 距离。  
- **一句话总结解题钥匙**：先把一个岛全部标记好，再用 **层层扩散的 BFS** 找到离它最近的另一块陆地。

---

## 反思

- **第一反应**：看到“最少翻 0 的数量”，自然想到“把所有配对的距离算一遍”。这就是暴力思路。  
- **最容易踩的坑**  
  - 忘记把第一岛的所有格子一次性加入 BFS 队列，导致只从单一点扩散，时间会翻倍。  
  - 在 BFS 中没有标记已经访问的水格子，可能会重复入队，导致无限循环或时间爆炸。  
  - 边界条件：`steps` 初始为 0，返回时要在碰到第二岛的那一层直接返回，而不是 `steps+1`。  
- **下次类似题目第一步**：**先把一个“起始区域”完整标记出来**（DFS/DFS），**再用 BFS 从整个区域向外层层搜索**，这样可以保证最短距离。