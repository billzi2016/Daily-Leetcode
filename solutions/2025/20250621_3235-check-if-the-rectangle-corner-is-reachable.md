# #3235. 检查矩形角点是否可达 / Check if the Rectangle Corner Is Reachable

> 难度：困难 · 标签：Array、Math、Depth-First Search、Breadth-First Search、Union Find、Geometry · [LeetCode 链接](https://leetcode.com/problems/check-if-the-rectangle-corner-is-reachable/)

---

## 题目（英文原版）

**Description**

You are given two positive integers xCorner and yCorner, and a 2D array circles, where circles[i] = [xi, yi, ri] denotes a circle with center at (xi, yi) and radius ri.
There is a rectangle in the coordinate plane with its bottom left corner at the origin and top right corner at the coordinate (xCorner, yCorner). You need to check whether there is a path from the bottom left corner to the top right corner such that the entire path lies inside the rectangle, does not touch or lie inside any circle, and touches the rectangle only at the two corners.
Return true if such a path exists, and false otherwise.

**Examples**

**Example 1:**

```
Input: xCorner = 3, yCorner = 4, circles = [[2,1,1]]
Output: true
Explanation:

The black curve shows a possible path between (0, 0) and (3, 4) .
```

**Example 2:**

```
Input: xCorner = 3, yCorner = 3, circles = [[1,1,2]]
Output: false
Explanation:

No path exists from (0, 0) to (3, 3) .
```

**Example 3:**

```
Input: xCorner = 3, yCorner = 3, circles = [[2,1,1],[1,2,1]]
Output: false
Explanation:

No path exists from (0, 0) to (3, 3) .
```

**Example 4:**

```
Input: xCorner = 4, yCorner = 4, circles = [[5,5,1]]
Output: true
Explanation:
```

**Constraints**

- 3 <= xCorner, yCorner <= 109
- 1 <= circles.length <= 1000
- circles[i].length == 3
- 1 <= xi, yi, ri <= 109

---

## 题目（中文翻译）

你得到两个正整数 `xCorner` 和 `yCorner`，以及一个二维数组 `circles`，其中 `circles[i] = [xi, yi, ri]` 表示一个圆心为 `(xi, yi)`、半径为 `ri` 的圆。

在坐标平面上存在一个矩形，其左下角位于原点 `(0, 0)`，右上角位于 `(xCorner, yCorner)`。请判断是否存在一条从左下角到右上角的路径，使得：

- 整条路径完全位于矩形内部；
- 路径不接触也不位于任何圆内部；
- 路径仅在两个角点与矩形相交。

如果存在满足条件的路径，返回 `true`；否则返回 `false`。

### 示例

**示例 1**  
Input: `xCorner = 3, yCorner = 4, circles = [[2,1,1]]`  
Output: `true`  
Explanation:  
黑色曲线展示了一条可能的路径，连接 `(0, 0)` 与 `(3, 4)`。

**示例 2**  
Input: `xCorner = 3, yCorner = 3, circles = [[1,1,2]]`  
Output: `false`  
Explanation:  
不存在从 `(0, 0)` 到 `(3, 3)` 的路径。

**示例 3**  
Input: `xCorner = 3, yCorner = 3, circles = [[2,1,1],[1,2,1]]`  
Output: `false`  
Explanation:  
不存在从 `(0, 0)` 到 `(3, 3)` 的路径。

**示例 4**  
Input: `xCorner = 4, yCorner = 4, circles = [[5,5,1]]`  
Output: `true`  

### 约束条件
- `3 <= xCorner, yCorner <= 10^9`
- `1 <= circles.length <= 1000`
- `circles[i].length == 3`
- `1 <= xi, yi, ri <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**在矩形里随意画一条线**，只要这条线不进入任何圆且只在两个对角点接触矩形边界，就算成功。  
要实现的话，可以把矩形离散成一个很细的网格（比如每 0.01 单位划一个点），然后用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 从左下角 (0,0) 开始遍历所有可达的格子，只要有格子能到达右上角 (xCorner, yCorner) 就返回 `True`。

- **用到的数据结构**  
  - **网格**：把连续的平面切成很多小格子，像把地图划分成城市块。  
  - **队列/递归栈**：DFS/BFS 用来“走”到相邻格子。  
  - **布尔数组**：记录格子是否已经访问过，防止走回头路。

- **为什么这个方法正确**  
  只要网格足够细，任何合法的连续曲线都能被离散成一串相邻格子。遍历所有不在圆里的格子，就等价于在平面上搜索所有可能的路径。

- **时间/空间复杂度**  
  假设我们把每条边都划分成 `k` 等分，则矩形内部会有大约 `k²` 个格子。  
  - 每个格子最多检查 4 个相邻格子，所以总的遍历次数是 `O(k²)`。  
  - 需要一个 `k × k` 的布尔数组来记访问状态，空间也是 `O(k²)`。  

> **大白话**：如果把矩形想象成一张棋盘，`k` 是每条边的格子数。遍历整张棋盘的时间跟格子总数成正比，格子越多，耗时越久，内存也会随之膨胀。

#### 代码（Python）

```python
from collections import deque
import math

def brute_path(xCorner: int, yCorner: int, circles):
    # 这里把每条边划分成 200 格（经验值），实际题目坐标可达 1e9，显然不可行
    STEP = 200
    dx = xCorner / STEP
    dy = yCorner / STEP

    # 预处理：判断网格点 (i*dx, j*dy) 是否在任意圆内部或边界上
    def safe(i, j):
        x = i * dx
        y = j * dy
        for cx, cy, r in circles:
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:   # 在圆里或恰好在圆上
                return False
        return True

    visited = [[False] * (STEP + 1) for _ in range(STEP + 1)]
    q = deque()
    if safe(0, 0):
        q.append((0, 0))
        visited[0][0] = True

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        i, j = q.popleft()
        if i == STEP and j == STEP:          # 到达右上角
            return True
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni <= STEP and 0 <= nj <= STEP and not visited[ni][nj] and safe(ni, nj):
                visited[ni][nj] = True
                q.append((ni, nj))
    return False
```

> 这段代码只能作为“思想演示”，在真实测试里会因为 `STEP` 必须非常大而超时或内存爆炸。

#### 复杂度

- **时间复杂度**：`O(k² · n)`，其中 `k` 是每条边的划分数，`n` 是圆的个数（每次判断是否安全要遍历所有圆）。  
  > 换句话说，网格越细、圆越多，时间就越长。

- **空间复杂度**：`O(k²)`，需要存储整个网格的访问状态。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“把平面离散化”**——坐标范围可达 `10⁹`，不可能真的把每个点都枚举。  
实际上，这道题只要求判断 **是否存在一条合法路径**，不需要给出路径本身。我们可以把 **“障碍”**（圆）和 **“矩形的四条边”** 看成图中的节点，**相交或相切** 看成节点之间的连边。  

- **关键观察**  
  1. 如果两个圆相交或相切，它们会形成一道“不可穿越的墙”。  
  2. 如果一个圆接触矩形的左边，则左边也被这堵墙“占领”。同理右、上、下四条边。  
  3. 当 **左边** 与 **右边** 在同一个连通块里时，说明有一条连续的障碍把左侧与右侧彻底隔开，左下角不可能绕过去到右上角。  
  4. 同理，**左边** 与 **下边**、**右边** 与 **上边**、**上边** 与 **下边** 成连通也会阻断对角路径。  

  因此，只要判断上述四对边是否在同一个连通分量里，就能得到答案。

- **构造图**  
  - **节点**：`0 … n-1` 表示 `n` 个圆；`n` 表左边，`n+1` 表右边，`n+2` 表下边，`n+3` 表上边。总共 `n+4` 个节点。  
  - **边的判定**  
    - 两个圆 `i`、`j`：若 `dist(center_i, center_j) ≤ ri + rj`（相交或相切）则连边。  
    - 圆 `i` 与左边：若 `xi - ri ≤ 0`（圆触及或穿过 x=0）则连边。右边同理 `xi + ri ≥ xCorner`。  
    - 圆 `i` 与下边：若 `yi - ri ≤ 0`；上边：`yi + ri ≥ yCorner`。  

- **并查集（Union‑Find）**  
  用并查集快速合并相交的节点并查询连通性。并查集的核心操作只有两种：`find(x)` 找根、`union(a,b)` 合并，两者时间几乎是 **O(α(N))**（α 为极慢增长的反阿克曼函数），可以视作常数。

- **判断**  
  计算完所有连边后，检查以下四对是否在同一集合：
  - `left` (`n`) 与 `right` (`n+1`)  
  - `left` (`n`) 与 `bottom` (`n+2`)  
  - `right` (`n+1`) 与 `top` (`n+3`)  
  - `top` (`n+3`) 与 `bottom` (`n+2`)  

  任意一对相连，说明障碍把矩形划成了两块，答案为 `False`；否则返回 `True`。

- **为什么正确**  
  - 任何合法路径必须在 **左下角** 与 **右上角** 之间穿过矩形内部。若左边与右边已经被障碍连成一条“墙”，这条墙把矩形从左到右完全封闭，左下角根本无法跨过去。同理其它三对边的封闭也会导致不可达。  
  - 反之，如果上述四对边均不相连，就不存在把对角两点分开的完整障碍墙，必然可以沿着空隙画出一条曲线（几何拓扑学中的 “Jordan 曲线定理” 简化版），因此答案为 `True`。

- **类比**  
  想象每个圆是一块 **黏土**，把它们放在矩形里。如果黏土块之间相互粘在一起，甚至粘到墙上，它们就形成了一道 **无法跨越的围栏**。我们只要判断这道围栏是否把左下角和右上角隔开即可。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n                     # 用来做按秩合并，提升效率

    def find(self, x: int) -> int:
        # 路径压缩：把查到的每个节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按秩合并，秩小的挂到秩大的下面
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

def is_path_possible(xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
    n = len(circles)
    LEFT, RIGHT, BOTTOM, TOP = n, n + 1, n + 2, n + 3
    uf = UnionFind(n + 4)

    # 1) 圆与圆之间的连边
    for i in range(n):
        xi, yi, ri = circles[i]
        for j in range(i + 1, n):
            xj, yj, rj = circles[j]
            dx = xi - xj
            dy = yi - yj
            # 两圆相交或相切的判定：距离 <= ri + rj
            if dx * dx + dy * dy <= (ri + rj) ** 2:
                uf.union(i, j)

    # 2) 圆与四条边的连边
    for i, (xi, yi, ri) in enumerate(circles):
        if xi - ri <= 0:          # 接触左边 (x = 0)
            uf.union(i, LEFT)
        if xi + ri >= xCorner:   # 接触右边 (x = xCorner)
            uf.union(i, RIGHT)
        if yi - ri <= 0:          # 接触下边 (y = 0)
            uf.union(i, BOTTOM)
        if yi + ri >= yCorner:   # 接触上边 (y = yCorner)
            uf.union(i, TOP)

    # 3) 检查四对边是否已经连通
    blocked = (
        uf.find(LEFT) == uf.find(RIGHT) or
        uf.find(LEFT) == uf.find(BOTTOM) or
        uf.find(RIGHT) == uf.find(TOP) or
        uf.find(TOP) == uf.find(BOTTOM)
    )
    return not blocked
```

**代码要点注释**  

- `UnionFind`：实现并查集，`find` 用路径压缩让后续查询更快，`union` 用按秩合并保持树的高度低。  
- 圆之间的相交判定采用 **勾股定理**：两圆心距离的平方 ≤ (r1+r2)²。  
- 与矩形边的接触判定只需要检查 **坐标 ± 半径** 是否越过对应的边界。  
- 最后四个 `uf.find(...)` 判断是否在同一个连通分量里，若任意一对相等说明被“墙”挡住，返回 `False`。

#### 复杂度

- **时间复杂度**：  
  - 圆之间两两比较 `O(n²)`（`n ≤ 1000`，最多约 10⁶ 次，完全可接受）。  
  - 圆与四条边的判定 `O(n)`。  
  - 并查集的 `find/union` 近似 `O(1)`，所以整体仍是 `O(n²)`。  
  > 与暴力解的 `O(k²·n)` 相比，这里根本不受坐标范围的影响，`k` 被消除了。

- **空间复杂度**：`O(n)` 用于并查集的父指针数组和秩数组，另外存放原始圆数据也只需 `O(n)`。  

  与暴力解的 `O(k²)`（可能达到数十亿）相比，节省了几乎所有内存。

---

## 心得

- **核心技巧**：把几何阻挡问题抽象成 **连通性图**，使用 **并查集（Union‑Find）** 检测是否出现“把矩形四边围成一圈”的障碍。  
- **适用的题型**  
  1. “是否可以从左上角走到右下角”且障碍为圆形/矩形/线段的路径阻断题。  
  2. “平面上若干障碍物是否把两个点分离” 类似的几何分离问题。  
  3. “岛屿是否相连” 或 “墙是否把区域分割” 的离散化模型。  
- **一句话总结**：把所有“会阻挡路径的东西”连成图，判断关键四条边是否被同一连通块连起来——若连通则路被封死，否者必有通路。

---

## 反思

- **第一反应**：把平面离散成网格，用 BFS/DFS 暴力搜索路径。虽然思路直观，却忽视了坐标范围太大导致的不可行性。  
- **最容易踩的坑**  
  1. **坐标溢出**：距离平方可能超过 64 位整数范围，使用 Python 的大整数自然安全，但在其他语言要注意使用 `long long`。  
  2. **圆与边的接触判定**：要用 `≤`（相切也算阻挡），否则会把恰好相切的情况漏掉。  
  3. **漏掉四种“墙”组合**：左‑右、左‑下、右‑上、上‑下，缺少任意一种都会得到错误的 `True`。  
- **下次类似题的第一步**：先思考**“阻挡的本质是什么”**，把几何对象抽象为**节点**，**相交/相切**抽象为**连边**，再用**并查集**或 **BFS** 检查关键连通性。这样可以立刻把大范围坐标转化为 **O(n²)** 的可解规模。