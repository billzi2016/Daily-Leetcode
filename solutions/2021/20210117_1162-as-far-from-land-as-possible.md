# #1162. 尽可能远离陆地 / As Far from Land as Possible

> 难度：中等 · 标签：Array、Dynamic Programming、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/as-far-from-land-as-possible/)

---

## 题目（英文原版）

**Description**

Given an n x n grid containing only values 0 and 1, where 0 represents water and 1 represents land, find a water cell such that its distance to the nearest land cell is maximized, and return the distance. If no land or water exists in the grid, return -1.
The distance used in this problem is the Manhattan distance: the distance between two cells (x0, y0) and (x1, y1) is |x0 - x1| + |y0 - y1|.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,1],[0,0,0],[1,0,1]]
Output: 2
Explanation: The cell (1, 1) is as far as possible from all the land with distance 2.
```

**Example 2:**

```
Input: grid = [[1,0,0],[0,0,0],[0,0,0]]
Output: 4
Explanation: The cell (2, 2) is as far as possible from all the land with distance 4.
```

**Constraints**

- n == grid.length
- n == grid[i].length
- 1 <= n <= 100
- grid[i][j] is 0 or 1

---

## 题目（中文翻译）

给定一个只包含 0 和 1 的 **n × n** 网格 `grid`，其中 **0** 表示水域，**1** 表示陆地。请找出一个水域单元格，使其到最近的陆地单元格的距离最大，并返回该距离。如果网格中不存在陆地或不存在水域，返回 **-1**。

本题使用的距离为 **曼哈顿距离**（Manhattan distance）：两个单元格 \((x_0, y_0)\) 和 \((x_1, y_1)\) 之间的距离为 \(|x_0 - x_1| + |y_0 - y_1|\)。

## 示例

### 示例 1

**输入**  
`grid = [[1,0,1],[0,0,0],[1,0,1]]`

**输出**  
`2`

**解释**  
单元格 \((1, 1)\) 与所有陆地的最近距离为 2，且它是可能的最大距离。

### 示例 2

**输入**  
`grid = [[1,0,0],[0,0,0],[0,0,0]]`

**输出**  
`4`

**解释**  
单元格 \((2, 2)\) 与所有陆地的最近距离为 4，且它是可能的最大距离。

## 约束条件

- `n == grid.length`
- `n == grid[i].length`
- `1 <= n <= 100`
- `grid[i][j]` 仅为 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个水格子**，把它和**所有陆地格子**的曼哈顿距离算一遍，取最小的那个距离（最近的陆地），然后在所有水格子中挑选出这个最小距离最大的水格子。  

- **用到的数据结构**：  
  - `list`（列表）保存所有陆地格子的坐标。可以把它想象成一本“地图字典”，key 是坐标，value 是“这里是陆地”。  
  - 双层 `for` 循环遍历网格。  

- **为什么正确**：  
  对每个水格子，我们穷举检查它到每块陆地的距离，必然能得到**最近的陆地**的距离。再把所有水格子的最近距离取最大值，就是题目要求的“离最近陆地最远的水格子”。  

- **时间/空间复杂度**：  
  - 设网格大小为 `n × n`，陆地格子数量记为 `L`，水格子数量记为 `W`（显然 `L + W = n²`）。  
  - 对每个水格子我们都要遍历所有陆地格子，最坏情况是 `L ≈ W ≈ n²/2`，于是时间复杂度是 **O(n⁴)**（因为两层外循环遍历水格子，两层内循环遍历陆地格子）。  
    - 大白话：如果 `n=100`，大约要做 10⁸ 次距离计算，跑起来会很慢。  
  - 额外空间只用来保存陆地坐标列表，最多 `n²` 个坐标，**O(n²)** 的空间。

#### 代码（Python）

```python
from typing import List

def maxDistance_bruteforce(grid: List[List[int]]) -> int:
    n = len(grid)
    land = []                       # 保存所有陆地格子的坐标
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:     # 1 表示陆地
                land.append((i, j))

    # 如果全是陆地或全是水，直接返回 -1
    if not land or len(land) == n * n:
        return -1

    max_min_dist = -1               # 记录所有水格子“最近陆地距离”的最大值
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:     # 只处理水格子
                # 计算该水格子到所有陆地的曼哈顿距离，取最小值
                min_dist = min(abs(i - x) + abs(j - y) for x, y in land)
                max_min_dist = max(max_min_dist, min_dist)

    return max_min_dist
```

#### 复杂度

- **时间复杂度**：`O(n⁴)`  
  - “四次方”意味着随着网格边长的增大，运算量会爆炸式增长。  
- **空间复杂度**：`O(n²)`  
  - 需要额外存放所有陆地的坐标，最坏情况下占用整个网格的空间。

---

### 2. 最优解

#### 思路  

**从暴力解出发**，我们发现瓶颈在于**对每个水格子都去遍历所有陆地格子**。如果能一次性把所有陆地的“影响”传播到水格子上，就不需要重复计算了。  

这正好可以用 **多源广度优先搜索（BFS）** 来实现：

1. 把所有陆地格子一次性放进 BFS 的队列（这叫“多源”），相当于从每块陆地同时向四周“扩散”。  
2. 每一次 BFS 的层数（level）就代表离最近陆地的距离。第一次把所有陆地格子标记为距离 `0`，随后向四个方向扩散到相邻的水格子，给它们标记为 `1`，再继续扩散到未访问的水格子标记为 `2` ……  
3. 当 BFS 结束时，**最后一次弹出队列的格子对应的层数，就是离最近陆地最远的水格子距离**。如果 BFS 过程中根本没有水格子被访问（全是陆地或全是水），返回 `-1`。

**关键概念解释**  

- **队列（Queue）**：像排队买票一样，先进去的先出来。BFS 正是利用这种“先入先出”的特性，一层层向外扩散。  
- **层（Level）**：把 BFS 的过程想象成水波纹，从中心向外扩散，一圈圈就是一层。第 `k` 层对应的格子到最近陆地的曼哈顿距离恰好是 `k`。  
- **多源 BFS**：普通 BFS 只从一个起点开始，而这里我们把所有陆地格子当作起点一起放进队列，就相当于从多个水波中心同时扩散，效率大幅提升。

**步骤**：

1. 遍历整个网格，把所有 `1`（陆地）坐标放入 `queue`，并把对应格子标记为已访问（或直接把原始 `grid` 当作距离矩阵，用 `-1` 表示未访问的水格子）。  
2. 记录 `max_dist = -1`。  
3. 当 `queue` 不为空时，弹出当前坐标 `(x, y)`，检查四个方向的相邻格子 `(nx, ny)`：  
   - 若在边界内且未访问（`grid[nx][ny] == 0`），把它的距离设为 `grid[x][y] + 1`，并加入队列。  
   - 同时更新 `max_dist = grid[nx][ny]`（因为 BFS 按层推进，这里得到的距离一定是当前最大的）。  
4. 循环结束后，`max_dist` 即为答案。若 `max_dist` 仍为 `-1`，说明没有水格子或没有陆地，返回 `-1`。

#### 代码（Python）

```python
from collections import deque
from typing import List

def maxDistance(grid: List[List[int]]) -> int:
    n = len(grid)
    q = deque()                     # BFS 队列
    # 1️⃣ 把所有陆地格子放进队列，距离初始化为 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                q.append((i, j))

    # 边界情况：全是陆地或全是水
    if len(q) == 0 or len(q) == n * n:
        return -1

    # 方向向量：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    max_dist = -1

    # 2️⃣ 多源 BFS
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 检查是否在矩阵内部且是未访问的水格子
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
                grid[nx][ny] = grid[x][y] + 1   # 距离 = 前驱格子的距离 + 1
                max_dist = grid[nx][ny]        # 记录最新的最大距离
                q.append((nx, ny))

    # 因为陆地的距离是 0，答案需要减去 0，直接返回 max_dist 即可
    return max_dist
```

> **注意**：这里直接在原始 `grid` 上写入距离，省去了额外的 `dist` 矩阵，空间更节省。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每个格子至多只会被放进队列一次，四个方向的检查常数级别，整体遍历一次矩阵即可。相当于“线性”随格子数量增长。  
  - 与暴力的 `O(n⁴)` 相比，提升了 **n²** 倍，`n=100` 时只需要约 10⁴ 次操作，瞬间完成。

- **空间复杂度**：`O(n²)`（最坏情况下队列里会同时存放整张矩阵的格子）  
  - 与暴力的额外空间相同，但这里的空间是 BFS 队列本身，属于**必要的**辅助空间。

---

## 心得

- **核心技巧**：**多源 BFS**（一次性从所有陆地同时向外扩散），把“寻找最近陆地距离”转化为“层层推进的水波纹”。  
- **适用的题型**：  
  1. **01 矩阵中最近的 0 / 1**（LeetCode 542 - 01 Matrix）  
  2. **岛屿的最大距离**（本题）  
  3. **墙与门**（LeetCode 286 - Walls and Gates）  
- **一句话总结解题钥匙**：**把“从每个水格子找最近陆地”反过来，改为“从所有陆地同步扩散”，用 BFS 自然得到最远距离**。

---

## 反思

- **第一反应**：看到“最大最小距离”，立刻想到遍历所有组合的暴力搜索。  
- **最容易踩的坑**：  
  - 忘记处理全是陆地或全是水的特殊情况，需要提前返回 `-1`。  
  - BFS 时没有把已经访问的格子标记，导致重复入队，时间会爆炸。  
  - 直接在 `grid` 上写距离时要注意原始 `1`（陆地）和 `0`（未访问水）的区别，防止把陆地误当作已经更新的水格子。  
- **下次遇到同类题**：第一步先问自己 **“是否可以把所有目标点一次性放入队列，进行多源 BFS？”** 如果答案是 “可以”，那就直接走 BFS 路线；否则再考虑其他技巧（DP、单调栈等）。