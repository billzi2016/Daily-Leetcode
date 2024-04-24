# #2662. **带特殊道路的路径最小费用** / Minimum Cost of a Path With Special Roads

> 难度：中等 · 标签：Array、Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-of-a-path-with-special-roads/)

---

## 题目（英文原版）

**Description**

You are given an array start where start = [startX, startY] represents your initial position (startX, startY) in a 2D space. You are also given the array target where target = [targetX, targetY] represents your target position (targetX, targetY).
The cost of going from a position (x1, y1) to any other position in the space (x2, y2) is |x2 - x1| + |y2 - y1|.
There are also some special roads. You are given a 2D array specialRoads where specialRoads[i] = [x1i, y1i, x2i, y2i, costi] indicates that the ith special road goes in one direction from (x1i, y1i) to (x2i, y2i) with a cost equal to costi. You can use each special road any number of times.
Return the minimum cost required to go from (startX, startY) to (targetX, targetY).

**Examples**

**Example 1:**

```
Input: start = [1,1], target = [4,5], specialRoads = [[1,2,3,3,2],[3,4,4,5,1]]
Output: 5
Explanation:
So the total cost is 1 + 2 + 1 + 1 = 5.
```

**Example 2:**

```
Input: start = [3,2], target = [5,7], specialRoads = [[5,7,3,2,1],[3,2,3,4,4],[3,3,5,5,5],[3,4,5,6,6]]
Output: 7
Explanation:
It is optimal not to use any special edges and go directly from the starting to the ending position with a cost |5 - 3| + |7 - 2| = 7.
Note that the specialRoads[0] is directed from (5,7) to (3,2).
```

**Example 3:**

```
Input: start = [1,1], target = [10,4], specialRoads = [[4,2,1,1,3],[1,2,7,4,4],[10,3,6,1,2],[6,1,1,2,3]]
Output: 8
Explanation:
```

**Constraints**

- start.length == target.length == 2
- 1 <= startX <= targetX <= 105
- 1 <= startY <= targetY <= 105
- 1 <= specialRoads.length <= 200
- specialRoads[i].length == 5
- startX <= x1i, x2i <= targetX
- startY <= y1i, y2i <= targetY
- 1 <= costi <= 105

---

## 题目（中文翻译）

你得到一个数组 `start`，其中 `start = [startX, startY]` 表示你在二维平面上的初始位置 `(startX, startY)`。同样，你还得到数组 `target`，其中 `target = [targetX, targetY]` 表示目标位置 `(targetX, targetY)`。  
从位置 `(x1, y1)` 前往任意位置 `(x2, y2)` 的代价为 `|x2 - x1| + |y2 - y1|`（曼哈顿距离）。

此外，还有一些特殊道路。给定二维数组 `specialRoads`，其中 `specialRoads[i] = [x1i, y1i, x2i, y2i, costi]` 表示第 `i` 条特殊道路只能单向从 `(x1i, y1i)` 通往 `(x2i, y2i)`，使用该道路的代价为 `costi`。每条特殊道路可以使用任意次。

返回从 `(startX, startY)` 到 `(targetX, targetY)` 所需的最小代价。

**示例 1**

```text
Input: start = [1,1], target = [4,5], specialRoads = [[1,2,3,3,2],[3,4,4,5,1]]
Output: 5
Explanation:
所以总费用为 1 + 2 + 1 + 1 = 5。
```

**示例 2**

```text
Input: start = [3,2], target = [5,7], specialRoads = [[5,7,3,2,1],[3,2,3,4,4],[3,3,5,5,5],[3,4,5,6,6]]
Output: 7
Explanation:
最优策略是不使用任何特殊道路，直接从起点走到终点，费用为 |5 - 3| + |7 - 2| = 7。
需要注意的是，specialRoads[0] 的方向是从 (5,7) 指向 (3,2)。
```

**示例 3**

```text
Input: start = [1,1], target = [10,4], specialRoads = [[4,2,1,1,3],[1,2,7,4,4],[10,3,6,1,2],[6,1,1,2,3]]
Output: 8
Explanation:
（此处保留原解释内容的翻译，如有，需要根据原题目补充。）
```

**约束条件**

- `start.length == target.length == 2`
- `1 <= startX <= targetX <= 10^5`
- `1 <= startY <= targetY <= 10^5`
- `1 <= specialRoads.length <= 200`
- `specialRoads[i].length == 5`
- `startX <= x1i, x2i <= targetX`
- `startY <= y1i, y2i <= targetY`
- `1 <= costi <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个二维平面都当成图的**每一个格子**，从起点 `(startX,startY)` 用 BFS/DFS 按曼哈顿距离一步一步扩散，直到走到终点 `(targetX,targetY)`。  
- **数据结构**：把每个坐标点当成图的节点，用**队列**（BFS）或**递归栈**（DFS）来遍历。  
- **生活类比**：把平面想象成一张无限大的棋盘，走一步只能上下左右移动一格，费用就是走的格子数。  

这种方法显然可以得到答案，因为它遍历了所有可能的路径。  

> **为什么正确**  
> - 每一次移动的费用恰好是两点之间的曼哈顿距离 `|x2-x1|+|y2-y1|`，所以把每一步拆成格子移动后，累加的费用就是原题要求的费用。  
> - 只要搜索遍历完所有格子，必然会碰到一条费用最小的路径。

#### 代码（Python）

```python
from collections import deque

def minCostBrute(start, target, specialRoads):
    # 把所有特殊道路映射成字典，方便查询
    # key: (x1,y1) -> list of (x2,y2,cost)  (有向)
    sp = {}
    for x1, y1, x2, y2, c in specialRoads:
        sp.setdefault((x1, y1), []).append((x2, y2, c))

    # BFS 需要一个 visited 集合防止无限循环
    q = deque()
    q.append((start[0], start[1], 0))   # (x, y, 已经花费的费用)
    visited = {(start[0], start[1]): 0} # 记录到达每个格子时的最小费用

    while q:
        x, y, cost = q.popleft()
        # 到达终点，直接返回
        if [x, y] == target:
            return cost

        # 1. 普通走一步（上下左右四个方向）
        for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            # 题目坐标范围在 [1, 10^5]，这里不做边界检查，只要在范围内就加入
            ncost = cost + 1          # 每走一步费用 +1
            if (nx, ny) not in visited or ncost < visited[(nx, ny)]:
                visited[(nx, ny)] = ncost
                q.append((nx, ny, ncost))

        # 2. 使用所有从 (x,y) 出发的特殊道路
        for nx, ny, c in sp.get((x, y), []):
            ncost = cost + c
            if (nx, ny) not in visited or ncost < visited[(nx, ny)]:
                visited[(nx, ny)] = ncost
                q.append((nx, ny, ncost))

    # 按理说永远能到达目标，这里只是防止 IDE 报错
    return -1
```

> **注意**：上述实现把**每个格子**都当成节点，坐标范围最高到 `10^5`，实际运行会出现 **内存爆炸** 和 **超时**，仅作概念说明。

#### 复杂度

- **时间复杂度**：`O( (range)^2 )`，这里的 `range` 是坐标轴的取值范围（最高 10^5），相当于遍历整个平面，几乎是 **指数级** 的慢。  
- **空间复杂度**：`O( (range)^2 )`，需要存储每个格子的最小费用，同样不可接受。

> 大白话：如果把平面看成一张 10 万 × 10 万 的大棋盘，暴力搜索相当于把每一个格子都检查一遍，根本不可能在合理时间内完成。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于我们把 *所有* 坐标都当成节点。其实我们不需要这么细。  
> **关键观察**：  
> 任意两点之间走曼哈顿距离的费用等价于 **直接“飞”** 从一点到另一点的费用。  
> 而题目只在 **特殊道路的起点 / 终点** 以及 **起点、终点** 这几类位置上提供了额外的、可能更便宜的路径。  

**结论**：在最优路径中，**只会经过** 以下几类点：

1. 起点 `start`
2. 目标点 `target`
3. 所有特殊道路的起点 `(x1i, y1i)`
4. 所有特殊道路的终点 `(x2i, y2i)`

把这些点看成图的 **节点**，两两之间可以 **普通步行**，费用就是曼哈顿距离；再加上每条 **有向特殊道路**，费用为题目给出的 `costi`。于是问题转化为：

> 在一个有向加权图中，求从 `start` 到 `target` 的最短路径。

这正是**单源最短路径**的经典模型，适合使用 **Dijkstra 算法**（配合最小堆）求解。

**为什么只需要这些节点？**  
- 若一条最优路径在中间经过了一个“非关键点” `(x, y)`，我们可以把前后两段普通步行合并为一次直接的曼哈顿距离，费用不变甚至更小。  
- 因此任何非关键点都可以被直接删除，最短路径仍然成立。

**核心算法**：  
- **建图**：把所有关键点放进列表 `points`，长度至多 `2 * len(specialRoads) + 2 ≤ 402`。  
- **边的构造**：  
  - 对任意 `i, j`（`i != j`），普通步行的费用 `dist(i,j) = |xi-xj| + |yi-yj|`。  
  - 对每条特殊道路 `i -> j`（起点是 `i`，终点是 `j`），费用是 `costi`（可能比普通距离更小）。  
- **最短路**：使用 Dijkstra，从 `start`（在 `points` 中的下标 0）出发，求到 `target`（下标 1）的最小费用。

**类比**：把每个关键点想象成城市，普通步行相当于 **高速公路**（费用为直线距离），特殊道路相当于 **特快列车**（费用固定且可能更快）。我们要找最省钱的出行方案。

#### 代码（Python）

```python
import heapq
from typing import List, Tuple

def minimumCost(start: List[int], target: List[int],
                specialRoads: List[List[int]]) -> int:
    """
    Dijkstra 求最短路径。
    节点集合 = {start, target} ∪ {所有特殊道路的起点/终点}
    """
    # 1️⃣ 把所有关键点收集起来，去重
    points: List[Tuple[int, int]] = [tuple(start), tuple(target)]
    point_index = {tuple(start): 0, tuple(target): 1}   # 记录每个点的下标

    for x1, y1, x2, y2, _ in specialRoads:
        p1, p2 = (x1, y1), (x2, y2)
        if p1 not in point_index:
            point_index[p1] = len(points)
            points.append(p1)
        if p2 not in point_index:
            point_index[p2] = len(points)
            points.append(p2)

    n = len(points)                     # 节点总数，最多约 402
    # 2️⃣ 为每个节点准备邻接表（列表），先放普通步行的边
    adj = [[] for _ in range(n)]        # adj[u] = [(v, weight), ...]

    # 普通步行：任意两点之间都可以直接走，费用为曼哈顿距离
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            w = abs(xi - xj) + abs(yi - yj)
            adj[i].append((j, w))
            adj[j].append((i, w))        # 步行是双向的

    # 3️⃣ 加入特殊道路（有向）
    for x1, y1, x2, y2, c in specialRoads:
        u = point_index[(x1, y1)]
        v = point_index[(x2, y2)]
        adj[u].append((v, c))            # 只单向，费用为 c

    # 4️⃣ Dijkstra（最小堆）
    INF = 10 ** 18
    dist = [INF] * n
    dist[0] = 0                         # 起点的费用为 0
    heap = [(0, 0)]                     # (当前费用, 节点下标)

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:                # 过期的条目，直接跳过
            continue
        if u == 1:                      # 已经到达目标点，可提前结束
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist[1]                      # 目标点的最小费用
```

**代码要点解释**  

| 行号 | 关键操作 | 中文解释 |
|------|----------|----------|
| 5‑9 | 收集所有关键点并去重 | 用字典 `point_index` 把每个坐标映射到唯一的下标 |
| 13‑20 | 构造普通步行的双向边 | 任意两点之间的费用是曼哈顿距离，放进邻接表 |
| 22‑24 | 加入有向的特殊道路 | 只在起点指向终点，费用为题目给出的 `c` |
| 28‑38 | Dijkstra 主循环 | 用最小堆不断取当前费用最小的节点，松弛相邻边 |
| 39‑40 | 提前返回 | 当弹出的节点是目标点时，最短距离已经确定 |

#### 复杂度

- **时间复杂度**：  
  - 构造普通步行边需要遍历所有节点对，`O(N²)`（`N ≤ 402`）。  
  - Dijkstra 使用最小堆，边数 `E = O(N²)`，所以总时间 `O(E log N) = O(N² log N)`。  
  - 对于本题的约束，这大约是 `402² ≈ 1.6e5` 条边，完全可以在毫秒级完成。  

- **空间复杂度**：  
  - 邻接表存储所有边 `O(N²)`，再加上距离数组 `O(N)`，整体 `O(N²)`。  
  - 这里的 `N` 最多 402，所需内存只有几百 KB，轻松满足限制。

> 与暴力解相比：  
> - 暴力解遍历了坐标平面（`10^10` 级别），根本不可行。  
> - 最优解只关心 **几百个** 关键点，时间从“天文级”降到“毫秒级”。  

---

## 心得

- **核心技巧**：把「只在关键点之间移动」的思想抽象成 **最短路模型**，利用 **Dijkstra** 求解。  
- **适用的题型**（类似思路）  
  1. **LeetCode 658. Find K Closest Elements**（将离散点看成图，求最近点）  
  2. **LeetCode 1499. Max Value of Equation**（把满足约束的点视作图的节点，用单调队列实现最短路）  
  3. **LeetCode 1197. Minimum Knight Moves**（在棋盘上只考虑关键格子，使用 BFS/Dijkstra）  
- **一句话总结解题钥匙**：**只在“起点、终点和特殊道路的端点”之间跳，剩下的都用曼哈顿距离直接连通，转化为最短路问题即可。**

---

## 反思

- **第一反应**：把整个平面当成网格，想用 BFS/DFS 完全遍历。  
- **最容易踩的坑**  
  1. **忘记特殊道路是有向的**，误把它当成双向会得到错误的更小费用。  
  2. **忽视坐标范围**，直接在二维数组上做 BFS 会导致内存/时间炸掉。  
  3. **没有去重关键点**，会导致邻接表出现重复边，影响效率。  
- **下次遇到同类题**：第一步就**列出所有“可能出现的转折点”，把它们视作图的节点，再判断两点之间的直接费用（曼哈顿或欧氏），最后跑最短路算法。这样既能保证正确，又能避免暴力搜索的灾难。