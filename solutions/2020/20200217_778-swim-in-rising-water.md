# #778. 在上升的水中游泳 / Swim in Rising Water

> 难度：困难 · 标签：Array、Binary Search、Depth-First Search、Breadth-First Search、Union Find、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/swim-in-rising-water/)

---

## 题目（英文原版）

**Description**

You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point (i, j).
It starts raining, and water gradually rises over time. At time t, the water level is t, meaning any cell with elevation less than equal to t is submerged or reachable.
You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.
Return the minimum time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left square (0, 0).

**Examples**

**Example 1:**

```
Input: grid = [[0,2],[1,3]]
Output: 3
Explanation:
At time 0, you are in grid location (0, 0).
You cannot go anywhere else because 4-directionally adjacent neighbors have a higher elevation than t = 0.
You cannot reach point (1, 1) until time 3.
When the depth of water is 3, we can swim anywhere inside the grid.
```

**Example 2:**

```
Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
Output: 16
Explanation: The final route is shown.
We need to wait until time 16 so that (0, 0) and (4, 4) are connected.
```

**Constraints**

- n == grid.length
- n == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] < n2
- Each value grid[i][j] is unique.

---

## 题目（中文翻译）

你得到一个 $n \times n$ 的整数矩阵 `grid`，其中 `grid[i][j]` 表示点 $(i, j)$ 的海拔高度。  
现在开始下雨，水位随时间上升。时间为 $t$ 时，水位等于 $t$，即海拔 **小于等于** $t$ 的单元格都会被淹没或可以到达。  
你只能在两个 **四方向相邻**（up, down, left, right）的单元格之间游泳，且必须满足这两个单元格的海拔分别 **不超过** $t$。在水中游泳的距离不受时间限制（可以在零时间内无限远移动），但必须始终保持在矩阵边界内。  

请返回 **最小的时间** $t$，使得你从左上角单元格 $(0, 0)$ 出发能够到达右下角单元格 $(n-1, n-1)$。

---

### 示例

#### 示例 1  
**输入**  
```text
grid = [[0,2],[1,3]]
```  
**输出**  
```text
3
```  
**解释**  
在时间 $0$ 时，你位于单元格 $(0, 0)$。  
由于四方向相邻的邻居海拔都大于 $t = 0$，你无法移动。  
只有当时间达到 $3$ 时，水深为 $3$，此时所有单元格的海拔均不超过水位，才能从 $(0, 0)$ 到达 $(1, 1)$。  

#### 示例 2  
**输入**  
```text
grid = [[0,1,2,3,4],
        [24,23,22,21,5],
        [12,13,14,15,16],
        [11,17,18,19,20],
        [10,9,8,7,6]]
```  
**输出**  
```text
16
```  
**解释**  
最终的路径如图所示。必须等到时间 $16$，水位达到 $16$，左上角 $(0, 0)$ 与右下角 $(4, 4)$ 才会连通。  

---

### 约束条件
- $n = \text{grid.length}$
- $n = \text{grid}[i].\text{length}$
- $1 \le n \le 50$
- $0 \le \text{grid}[i][j] < n^2$
- 矩阵中的每个值都是唯一的。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**“把时间从 0 一点点往后推”，每个时刻 t 检查我们能不能从左上角走到右下角**。  
具体步骤：

1. 记录当前的时间 `t`（从 0 开始），水面高度就是 `t`。  
2. 用**广度优先搜索（BFS）**从 `(0,0)` 开始，只往四个方向走，**前提是相邻格子的高度 ≤ t**（只有低于或等于水位的格子才能踩）。  
3. 如果 BFS 能够到达 `(n‑1,n‑1)`，说明在时间 `t` 我们已经可以到达终点，返回 `t`。  
4. 否则把 `t` 加 1，继续第 2 步。

> **类比**：想象你在雨中站在一个低洼的格子里，雨水慢慢涨高。每升高一点，你就检查一次，看看有没有已经被水淹没、可以走通的道路。

这个方法一定能得到答案，因为**水位最终会升到最高的格子**，届时所有格子都可达，必然能走通。

#### 代码（Python）

```python
from collections import deque

def swimInWater_bruteforce(grid):
    n = len(grid)
    # 水位从 0 开始逐渐升高
    t = 0
    # 四个方向的移动向量
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    while True:
        # 如果起点或终点本身高度 > t，显然此时不可达，直接跳到更大的 t
        if grid[0][0] > t or grid[n-1][n-1] > t:
            t += 1
            continue

        # BFS 队列，存放当前能够到达的格子坐标
        q = deque([(0, 0)])
        visited = [[False]*n for _ in range(n)]
        visited[0][0] = True
        reached = False

        while q:
            x, y = q.popleft()
            if (x, y) == (n-1, n-1):      # 已经到达右下角
                reached = True
                break
            # 向四个方向扩展
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n \
                        and not visited[nx][ny] \
                        and grid[nx][ny] <= t:   # 只有不高于水位的格子才能进入
                    visited[nx][ny] = True
                    q.append((nx, ny))

        if reached:               # 本次 t 能够连通
            return t
        t += 1                     # 否则水位再升高一点，继续尝试
```

> 代码里每一行都有中文注释，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n^2 * maxHeight)`。  
  - `maxHeight` 最坏情况下等于 `n^2-1`（因为所有高度都是唯一的），所以整体是 `O(n^4)`。  
  - 用大白话说，就是**“每升一级水位，就要把整个矩阵遍历一次”**，随着矩阵变大，这种做法会非常慢。

- **空间复杂度**：`O(n^2)`。  
  - 主要是 `visited` 数组和 BFS 队列占的空间，和矩阵大小成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都重新从头搜索**，而我们其实只需要**一次遍历就能找到最小的“最大高度”**。  
这类“在路径上把最大的代价最小化”的问题，**Dijkstra 最短路**的思想恰好可以改造使用：

1. 把每个格子看成图中的一个节点。  
2. 两个相邻格子之间有一条无向边，**边的权重 = 进入该格子的高度**（因为我们只能在水位 ≥ 该格子高度时才能踩上去）。  
3. 从起点 `(0,0)` 开始，**每次优先走高度最小的格子**。这正好对应**最小堆（priority queue）**的作用——像是“每次把最容易通过的道路先挑出来”。  
4. 维护一个变量 `ans`，记录沿当前路径走过的格子里**最高的高度**。当我们把一个格子加入堆时，`ans = max(ans, grid[x][y])`。  
5. 当第一次弹出终点 `(n-1,n-1)` 时，`ans` 就是答案，因为此时我们已经找到了**“把最高高度降到最低”的路径**。

> **类比**：想象你在爬山，山上每块石头都有一个高度标签。你想找一条路径，使得**最高的那块石头尽可能低**。你每次都先挑选当前**最低的石头**往前走，最终到达山顶时，最高石头的高度就是最小可能的。

**关键数据结构**  
- **最小堆（priority queue）**：类似“排队买票”，票价最小的先被叫号。这里我们把“格子高度”当作票价，堆总是把当前可达的**最低高度**弹出来。Python 的 `heapq` 就是最小堆的实现。  
- **并查集（Union Find）** 也可以解决本题（把所有格子按高度从小到大加入并检查起点和终点是否已经连通），但对初学者来说堆+Dijkstra 更直观。

#### 代码（Python）

```python
import heapq

def swimInWater(grid):
    """
    使用 Dijkstra 思想 + 最小堆，求最小的“最大高度”。
    """
    n = len(grid)
    # 四个方向
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    # visited 用来避免重复加入堆
    visited = [[False]*n for _ in range(n)]

    # 堆里存 (当前格子的高度, x, y)
    # 初始时只能站在 (0,0)，所以把它放进去
    heap = [(grid[0][0], 0, 0)]
    visited[0][0] = True

    # ans 记录走到当前格子时，沿途遇到的最高高度
    ans = 0

    while heap:
        height, x, y = heapq.heappop(heap)   # 取出当前可达的最低高度格子
        ans = max(ans, height)               # 更新路径上最高的高度

        # 如果已经到达右下角，答案就是 ans
        if x == n-1 and y == n-1:
            return ans

        # 向四个方向继续扩展
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                visited[nx][ny] = True
                # 把相邻格子加入堆，堆会根据格子高度自动排序
                heapq.heappush(heap, (grid[nx][ny], nx, ny))

    # 按题意一定能到达，这行代码理论上不会执行
    return -1
```

> - `heapq.heappush` / `heapq.heappop` 分别是**往堆里放**和**弹出最小元素**。  
> - `ans = max(ans, height)` 的作用是“记录我们已经走过的最高水位”。当我们第一次拿到终点时，这个 `ans` 正好是**最小的必要水位**。

#### 复杂度

- **时间复杂度**：`O(n^2 log n^2)` → `O(n^2 log n)`。  
  - 每个格子最多被放入堆一次，堆的大小最多 `n^2`，插入和弹出操作都是 `log`（对数）时间。  
  - 用大白话说，就是**“每走一步都要花一点点时间找最小的高度”，但因为我们只走一次全图，所以比暴力快很多”。**

- **空间复杂度**：`O(n^2)`。  
  - `visited` 数组和堆最坏情况下都需要存放所有格子的信息。

---

## 心得

- **核心技巧**：把“在路径上把最高值最小化”转化为**最小化最大边权的路径**，使用**Dijkstra（最小堆）**或**二分搜索 + BFS**都可以。  
- **适用题型**：  
  1. “路径上的最大值最小化” 类题，如 LeetCode 1102（路径上的最大值）  
  2. “在逐渐开放的环境中找最早连通时间” 类题，如 LeetCode 778（水位上升的泳池）  
  3. “在权值为高度/费用的网格里找最低“瓶颈”路径” 类题。  
- **一句话总结**：**“把水位视作费用，用最小堆一次遍历即可得到最小的‘最大费用’”。**

---

## 反思

- **第一反应**：看到“水位随时间升高”，会想到**模拟时间递增**，于是想到暴力的“逐时 BFS”。  
- **最容易踩的坑**：  
  - **忘记把起点的高度计入答案**（`ans` 必须先取 `grid[0][0]`）。  
  - **未标记 visited**，导致同一个格子被多次放入堆，时间复杂度会失控。  
  - **边界条件**：`n = 1` 时直接返回 `grid[0][0]`。  
- **下次遇到同类题**：第一步先思考**“这是一条路径，路径的代价是什么？是最大值还是和？”**，如果是最大值，就考虑**最小堆（Dijkstra）或二分搜索**；如果是和，则直接用普通 Dijkstra。这样可以快速定位最合适的算法。