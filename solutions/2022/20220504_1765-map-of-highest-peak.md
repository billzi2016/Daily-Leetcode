# #1765. 最高峰地图 / Map of Highest Peak

> 难度：中等 · 标签：Array、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/map-of-highest-peak/)

---

## 题目（英文原版）

**Description**

You are given an integer matrix isWater of size m x n that represents a map of land and water cells.
You must assign each cell a height in a way that follows these rules:
Find an assignment of heights such that the maximum height in the matrix is maximized.
Return an integer matrix height of size m x n where height[i][j] is cell (i, j)'s height. If there are multiple solutions, return any of them.
Note: This question is the same as 542: https://leetcode.com/problems/01-matrix/

**Examples**

**Example 1:**

```
Input: isWater = [[0,1],[0,0]]
Output: [[1,0],[2,1]]
Explanation: The image shows the assigned heights of each cell.
The blue cell is the water cell, and the green cells are the land cells.
```

**Example 2:**

```
Input: isWater = [[0,0,1],[1,0,0],[0,0,0]]
Output: [[1,1,0],[0,1,1],[1,2,2]]
Explanation: A height of 2 is the maximum possible height of any assignment.
Any height assignment that has a maximum height of 2 while still meeting the rules will also be accepted.
```

**Constraints**

- m == isWater.length
- n == isWater[i].length
- 1 <= m, n <= 1000
- isWater[i][j] is 0 or 1.
- There is at least one water cell.

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的整数矩阵 `isWater`，其中 `isWater[i][j]` 为 `0` 表示陆地单元格，为 `1` 表示水单元格。  
你需要为每个单元格分配一个高度，使其满足以下规则：

1. 所有水单元格的高度必须为 `0`。  
2. 任意两个相邻单元格（上下左右四个方向）的高度之差的绝对值不能超过 `1`。  

在满足上述规则的前提下，**找到一种高度分配，使得矩阵中的最大高度尽可能大**。  
返回一个大小为 `m x n` 的整数矩阵 `height`，其中 `height[i][j]` 表示单元格 `(i, j)` 的高度。若存在多种满足条件的解，返回任意一种即可。

---

### 示例

**示例 1**

```text
Input: isWater = [[0,1],[0,0]]
Output: [[1,0],[2,1]]
Explanation: 图中展示了每个单元格分配后的高度。蓝色单元格为水单元格（高度为 0），绿色单元格为陆地单元格。
```

**示例 2**

```text
Input: isWater = [[0,0,1],[1,0,0],[0,0,0]]
Output: [[1,1,0],[0,1,1],[1,2,2]]
Explanation: 高度 `2` 是在满足所有规则的前提下可以达到的最大高度。任何最大高度为 `2` 且仍符合规则的高度分配都将被接受。
```

---

### 约束条件

- `m == isWater.length`
- `n == isWater[i].length`
- `1 <= m, n <= 1000`
- `isWater[i][j]` 为 `0` 或 `1`
- 至少存在一个水单元格

> **提示**：本题与 LeetCode 题目 542（[01 Matrix](https://leetcode.com/problems/01-matrix/)）相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个陆地格子，都去找离它最近的水格子，距离就是它的高度**。  
这相当于“从每个陆地格子出发，向四周扩散，直到碰到第一个水格子”。  
实现上可以：

1. 把所有格子都遍历一遍。  
2. 对于每个格子如果是水（`isWater[i][j] == 1`）就直接记高度 `0`。  
3. 否则从该格子开始 **BFS（广度优先搜索）**，逐层向四个方向扩散，直到第一次遇到水格子。扩散的层数就是最近水格子的距离，也就是该格子的高度。

> **类比**：把矩阵想成一张城市地图，水格子是“消防站”。我们要为每栋建筑（陆地格子）标上“离最近消防站的步数”。暴力做法就是每栋建筑都派一辆救护车去找最近的消防站，显然非常低效。

**为什么正确**  
BFS 按层遍历，第一次碰到水格子时的层数就是最短的曼哈顿距离（只能上下左右走），这恰好满足题目“高度受最近的水格子限制”的要求。

#### 代码（Python）

```python
from collections import deque
from typing import List

def highestPeak_brute(isWater: List[List[int]]) -> List[List[int]]:
    m, n = len(isWater), len(isWater[0])
    # 结果矩阵，先全部填 -1 表示未计算
    height = [[-1] * n for _ in range(m)]

    # 四个方向的移动向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(m):
        for j in range(n):
            # 水格子高度直接为 0
            if isWater[i][j] == 1:
                height[i][j] = 0
                continue

            # 对每个陆地格子做一次 BFS
            q = deque()
            q.append((i, j, 0))               # (行, 列, 当前距离)
            visited = [[False] * n for _ in range(m)]
            visited[i][j] = True

            while q:
                x, y, d = q.popleft()
                # 如果碰到水格子，当前距离 d 就是答案
                if isWater[x][y] == 1:
                    height[i][j] = d
                    break

                # 向四个方向继续搜索
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                        visited[nx][ny] = True
                        q.append((nx, ny, d + 1))

    return height
```

> 关键行解释  
> - `q.append((i, j, 0))`：把起点放进队列，距离从 0 开始计数。  
> - `if isWater[x][y] == 1:`：一旦 BFS 触碰到水格子，就得到最近距离。  
> - `visited` 防止在同一次 BFS 中重复访问同一个格子。

#### 复杂度

- **时间复杂度**：`O(m * n * (m + n))`  
  对每个格子都要跑一次 BFS，最坏情况下 BFS 要遍历整个矩阵（约 `m·n`），所以总共是 `m·n` 次 × `m·n` 步 ≈ `O((m·n)²)`，在本题的约束下会超时。  
  用大白话说，就是如果矩阵是 1000×1000，暴力解要做 1 000 000 次“全图搜索”，根本跑不完。

- **空间复杂度**：`O(m * n)`  
  主要是 `height`、`visited` 两个二维数组以及 BFS 队列的最大规模（最多装满整个矩阵）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：我们对每个陆地格子都单独进行一次 BFS，重复遍历了大量相同的路径。  
其实，所有陆地格子的最近水格子 **可以一次性一起求出来**，只要我们把 **所有水格子当作 BFS 的起点**，同时向外层层扩散。  

这是一种 **多源 BFS（Multi‑Source BFS）**：

1. 把矩阵中所有 `isWater[i][j] == 1` 的格子放进同一个队列 `q`，并把它们的高度设为 `0`。  
2. 进行普通的 BFS：每次弹出队首 `(x, y)`，检查它的四个相邻格子 `(nx, ny)`。  
   - 如果相邻格子还没有被赋值（即高度为 `-1`），说明它是第一次被到达，距离就是 `height[x][y] + 1`。  
   - 把 `(nx, ny)` 加入队列继续向外扩散。  
3. 队列空了以后，所有格子的高度就都已经是 **到最近水格子的最短距离**，且因为是从所有水格子一起出发，得到的最大高度已经是可能的最大值。

> **类比**：把所有消防站（所有水格子）都派出一支救护车，同时向四周展开搜索。每条街道（格子）第一次被救护车到达时，记录下它离最近消防站的步数。这样只需要一次“大规模”搜索，而不是每栋楼都单独去找。

**为什么最优**  
- 每个格子只会被加入队列一次，访问一次，时间线性 `O(m·n)`。  
- BFS 本身天然保证了“先到先得”，所以第一次到达的距离一定是最短距离。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def highestPeak(isWater: List[List[int]]) -> List[List[int]]:
    m, n = len(isWater), len(isWater[0])
    height = [[-1] * n for _ in range(m)]   # -1 表示尚未访问

    q = deque()
    # 1️⃣ 把所有水格子放入队列，高度设为 0
    for i in range(m):
        for j in range(n):
            if isWater[i][j] == 1:
                height[i][j] = 0
                q.append((i, j))

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 2️⃣ 多源 BFS
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 只处理尚未赋值的格子
            if 0 <= nx < m and 0 <= ny < n and height[nx][ny] == -1:
                height[nx][ny] = height[x][y] + 1   # 与父节点距离 +1
                q.append((nx, ny))

    return height
```

> 关键行解释  
> - `height[i][j] = 0`、`q.append((i, j))`：一次性把所有水格子塞进队列，形成多源起点。  
> - `if height[nx][ny] == -1:`：只在第一次碰到时更新高度，确保是最近水格子的距离。  
> - `height[nx][ny] = height[x][y] + 1`：父节点的高度已经是到最近水格子的距离，加 1 即为当前格子的距离。

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  每个格子最多被访问一次，队列的入队和出队总共也是 `m·n` 次。用大白话说，就是矩阵有多大，就跑多少步，线性增长，完全能接受。

- **空间复杂度**：`O(m * n)`  
  需要存放结果矩阵 `height`（`m·n`）和 BFS 队列（最坏情况下也会装满整个矩阵），属于同阶。

---

## 心得

- **核心技巧**：**多源 BFS**。把所有满足同一条件的起点一次性放进队列，层层扩散，能够一次性求出每个位置到最近起点的最短距离。
- **适用的题型**  
  1. 01 矩阵（LeetCode 542）——求每个 1 到最近 0 的距离。  
  2. 岛屿周长/最近陆地（LeetCode 1162）——从所有陆地出发找最近海洋。  
  3. “墙与门”问题（LeetCode 286）——从所有门出发填充距离。
- **一句话总结**：**把所有水格子当作“超级起点”，一次 BFS 同时覆盖全图，就是解这类“最近距离”题的钥匙**。

---

## 反思

- **第一反应**：看到“每个格子高度受最近水格子限制”，立刻想到对每个格子单独搜索最近水格子（即暴力 BFS）。
- **最容易踩的坑**  
  - **忘记多源**：只用了一个水格子做起点，导致得到的高度不是全局最优。  
  - **未标记已访问**：在 BFS 中没有判断 `height[nx][ny] == -1`，会导致同一个格子被重复入队，时间爆炸。  
  - **边界条件**：矩阵可能只有一行或一列，四向移动时一定要检查 `0 <= nx < m`、`0 <= ny < n`。
- **下次遇到同类题**：第一步先 **收集所有“源点”**（水格子、门、0 等），判断是否可以 **一次性多源 BFS**，再决定是否需要额外的 DP 或单调栈等技巧。这样可以快速定位最优解的方向。