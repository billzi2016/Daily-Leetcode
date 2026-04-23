# #3604. 有向图中到达终点的最小时间 / Minimum Time to Reach Destination in Directed Graph

> 难度：中等 · 标签：Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-reach-destination-in-directed-graph/)

---

## 题目（英文原版）

**Description**

You are given an integer n and a directed graph with n nodes labeled from 0 to n - 1. This is represented by a 2D array edges, where edges[i] = [ui, vi, starti, endi] indicates an edge from node ui to vi that can only be used at any integer time t such that starti <= t <= endi.
You start at node 0 at time 0.
In one unit of time, you can either:
Return the minimum time required to reach node n - 1. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1,0,1],[1,2,2,5]]
Output: 3
Explanation:

The optimal path is:
Hence, the minimum time to reach node 2 is 3.
```

**Example 2:**

```
Input: n = 4, edges = [[0,1,0,3],[1,3,7,8],[0,2,1,5],[2,3,4,7]]
Output: 5
Explanation:

The optimal path is:
Hence, the minimum time to reach node 3 is 5.
```

**Example 3:**

```
Input: n = 3, edges = [[1,0,1,3],[1,2,3,5]]
Output: -1
Explanation:
```

**Constraints**

- 1 <= n <= 105
- 0 <= edges.length <= 105
- edges[i] == [ui, vi, starti, endi]
- 0 <= ui, vi <= n - 1
- ui != vi
- 0 <= starti <= endi <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n` 和一个包含 `n` 个节点（编号为 `0` 到 `n‑1`）的有向图（directed graph）。图由二维数组 `edges` 表示，其中 `edges[i] = [ui, vi, starti, endi]` 表示一条从节点 `ui` 到节点 `vi` 的有向边（edge），该边只能在整数时间 `t` 满足 `starti ≤ t ≤ endi` 时使用。  

你在时间 `0` 时位于节点 `0`。在每一个时间单位内，你可以：

* …（题目原文此处省略）  

返回到达节点 `n‑1` 所需的最小时间。如果无法到达，返回 `-1`。  

**示例**  

*示例 1*  
```
Input: n = 3, edges = [[0,1,0,1],[1,2,2,5]]
Output: 3
```
**解释**：  
最优路径为：  
因此，达到节点 `2` 的最小时间为 `3`。  

*示例 2*  
```
Input: n = 4, edges = [[0,1,0,3],[1,3,7,8],[0,2,1,5],[2,3,4,7]]
Output: 5
```
**解释**：  
最优路径为：  
因此，达到节点 `3` 的最小时间为 `5`。  

*示例 3*  
```
Input: n = 3, edges = [[1,0,1,3],[1,2,3,5]]
Output: -1
```
**解释**：  
没有任何可行的路径能够在给定的时间窗口内从节点 `0` 到达节点 `2`，所以返回 `-1`。  

**约束条件**  

- `1 ≤ n ≤ 10^5`  
- `0 ≤ edges.length ≤ 10^5`  
- `edges[i] == [ui, vi, starti, endi]`  
- `0 ≤ ui, vi ≤ n‑1`，且 `ui ≠ vi`  
- `0 ≤ starti ≤ endi ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举一遍**，找出能够到达 `n-1` 的最早时间。  
可以把这个过程想象成：

- **时钟**：从 `t = 0` 开始，每走一步时间 +1。
- **地图**：每条有向边都有一段“开放时间窗口” `[start, end]`，只有当时钟指向的时间落在这个窗口里，才能走这条路。
- **状态**：当前所在的节点 + 当前的时间，称为一个“状态”。  
  从一个状态出发，尝试所有满足 `t ≤ end` 的出边：
  - 若 `t < start`，只能**等到 `start` 再出发**（相当于在原地等），随后再走这条边，抵达下一个节点的时间就是 `start + 1`。
  - 若 `start ≤ t ≤ end`，可以立刻走，抵达时间为 `t + 1`。

暴力做法就是把 **所有状态** 用 BFS（层序遍历）或 DFS（递归）搜索一遍，记录到达每个节点的最早时间，最后看 `n-1` 能否被访问。

> **为什么这个方法能得到正确答案？**  
> 因为我们没有剪枝，所有合法的“等‑走‑等‑走”序列都被尝试了一遍，最早到达终点的那条路径必然会被遍历到。

> **复杂度怎么解释？**  
> - `n` 是节点数，`m` 是边数。  
> - 每个状态包含节点 + 时间，时间最多可以取到 `10^9`（题目上界），理论上状态数是 **无限** 的。  
> - 即使我们只考虑每条边最多一次（不等候），也要把每条边的所有可能出发时间都尝试一次，时间维度让搜索呈指数级增长。  
> - 用大白话说，就是 **“每走一步都要翻遍所有可能的时间”，会慢到不可接受**。

#### 代码（Python）

```python
from collections import deque

def minimum_time_bruteforce(n, edges):
    # 把边按起点分组，方便遍历
    adj = [[] for _ in range(n)]
    for u, v, s, e in edges:
        adj[u].append((v, s, e))

    # BFS 队列里存 (node, current_time)
    q = deque()
    q.append((0, 0))
    # 记录每个节点已经访问过的最早时间，防止无限循环
    visited = [float('inf')] * n
    visited[0] = 0

    while q:
        u, t = q.popleft()
        if u == n - 1:          # 已经到达终点，返回当前时间
            return t
        for v, start, end in adj[u]:
            if t > end:         # 当前时间已经超过这条边的可用窗口，直接跳过
                continue
            # 等待至窗口开始时间（如果需要的话）
            depart = max(t, start)
            arrive = depart + 1   # 行驶一次花 1 单位时间
            if arrive < visited[v]:
                visited[v] = arrive
                q.append((v, arrive))
    return -1
```

> 代码里每一次弹出队列的状态都要遍历所有相邻边，**最坏情况下会遍历 `O(n * max_time)`**，显然不符合题目规模。

#### 复杂度

- **时间复杂度**：`O(状态数 × 出边数)`，在最坏情况下接近 `O(10^9 × m)`，实际会超时。  
  大白话：相当于“每秒钟都要检查所有道路”，根本不可能在合理时间内跑完。

- **空间复杂度**：`O(n)` 用来存放每个节点的最早到达时间 + BFS 队列。  

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈在于时间维度的无限扩展**。  
关键观察：

1. **每条边的可用窗口是一个闭区间** `[start, end]`，而且 **只要我们在窗口内到达该节点，就一定可以立刻出发**（或等到窗口起点）。  
2. 对于同一个节点，只需要记住 **“最早能够到达的时间”**，后面更晚到达的情况永远不会产生更好的答案。  
3. 这正好和 **单源最短路（Dijkstra）** 的思想相吻合：我们把 **“当前最小的已知到达时间”** 当作距离，使用最小堆（优先队列）每次扩展最早到达的节点。

**如何把时间窗口融合进 Dijkstra？**  

- 状态仍然是 `(node, cur_time)`，但我们只在堆中保存**每个节点的最早到达时间**，不必枚举所有可能的等待时间。  
- 当我们从节点 `u`、当前时间 `t`（已经是最早到达 `u` 的时间）尝试使用一条边 `[u, v, start, end]` 时：
  - 若 `t > end`，这条边已经失效，直接跳过。
  - 否则我们可以**等到 `max(t, start)` 再出发**，因为如果 `t` 在窗口内直接走更快，如果 `t` 在窗口前必须等到 `start`。
  - 出发后花 1 单位时间到达 `v`，到达时间 `new_time = max(t, start) + 1`。
- 如果 `new_time` 小于之前记录的 `v` 的最早到达时间，就更新并把 `(v, new_time)` 放入堆。

> **类比**：想象每个节点是一个“公交站”，每条边是“一趟只有特定发车时间段的巴士”。我们站在某站的最早时间 `t`，要乘坐巴士就要等到它的**首班车** `start`（如果已经错过则无法乘坐），上车后再花 1 分钟到达下一站。

**为什么 Dijkstra 能工作？**  

- 边的“权重”其实是 **`max(t, start) + 1 - t`**，它始终是非负的（因为 `max(t,start) ≥ t`），满足 Dijkstra 对非负权重的要求。  
- 堆每次弹出的都是**当前所有未确定节点中最早的到达时间**，因此一旦某节点被弹出，它的最早时间已经是全局最优，不会再被更短的路径改写，这正是 Dijkstra 的核心证明。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

def minimum_time(n: int, edges):
    """
    使用 Dijkstra（最短路）求解在有时间窗口的有向图中从 0 到 n-1 的最小到达时间。
    若不可达返回 -1。
    """
    # 按出发点把边收集起来，方便遍历
    graph = defaultdict(list)          # graph[u] = [(v, start, end), ...]
    for u, v, start, end in edges:
        graph[u].append((v, start, end))

    # dist[i] 表示到达节点 i 的最早时间，初始为正无穷
    INF = 10**18
    dist = [INF] * n
    dist[0] = 0                         # 起点时间为 0

    # 最小堆，元素为 (当前已知最早时间, 节点编号)
    heap = [(0, 0)]                     # 从 0 开始

    while heap:
        cur_time, u = heapq.heappop(heap)

        # 如果弹出的时间已经不是最早的，说明已经被更好的路径更新，直接跳过
        if cur_time != dist[u]:
            continue

        # 已经到达终点，最早时间即为答案（因为 Dijkstra 保证最先弹出的是最优解）
        if u == n - 1:
            return cur_time

        # 遍历 u 的所有出边
        for v, start, end in graph.get(u, []):
            if cur_time > end:          # 当前时间已经超过这条边的可用窗口，永远无法使用
                continue

            # 等待至窗口开始时间（若已在窗口内则不需要等待）
            depart = max(cur_time, start)
            arrive = depart + 1         # 行驶一步花 1 时间单位

            # 如果这条路让 v 更早到达，则更新并放入堆
            if arrive < dist[v]:
                dist[v] = arrive
                heapq.heappush(heap, (arrive, v))

    # 循环结束仍未到达终点，说明不可达
    return -1
```

> 关键行解释  
> - `if cur_time > end: continue` —— 边已经失效，直接丢掉。  
> - `depart = max(cur_time, start)` —— “等到巴士首班车”。  
> - `arrive = depart + 1` —— 上车后花 1 单位时间到达下一站。  
> - `if arrive < dist[v]:` —— 只在找到更早到达时间时才更新，保持 Dijkstra 的最小化特性。

#### 复杂度

- **时间复杂度**：`O((n + m) log n)`  
  - 每条边最多被检查一次（`for v, start, end in graph[u]`），  
  - 每次更新距离时会向堆中插入一个元素，堆的大小至多 `n`，插入/弹出代价 `log n`。  
  - 用大白话说，就是“遍历所有站点和所有巴士一次，每次排队找最早的站点只需要几秒钟的时间”。

- **空间复杂度**：`O(n + m)`  
  - `graph` 保存所有边，需要 `O(m)`，  
  - `dist`、堆等额外数组/结构各占 `O(n)`。  
  - 与暴力解的 `O(10^9)` 时间空间相比，完全可接受。

---

## 心得

- **核心技巧**：在最短路算法中加入**时间窗口约束**，把“等候”转化为边的有效出发时间 `max(cur_time, start)`。
- **适用题型**：
  1. 带有**开放时间段**的交通网络（如公交、火车时刻表）求最早到达时间。  
  2. **时间限制的任务调度**，如在特定时间窗口内才能执行的操作。  
  3. 需要**等待**才能使用资源的图论问题（如动态道路、开关灯的最短路径）。
- **一句话总结**：**把“等”看作边的额外权重，使用 Dijkstra 在 (节点, 最早到达时间) 上搜索**。

---

## 反思

- **第一反应**：直接把时间当成第二维度暴力搜索，忘记了 Dijkstra 对非负权重的强大剪枝能力。  
- **最容易踩的坑**  
  - 忘记判断 `cur_time > end`，导致使用已经失效的边产生错误的负向等待。  
  - 误以为可以直接把 `start` 当作权重，而忽略了 **当前时间** 可能已经在窗口内部，需要 `max(cur_time, start)`。  
  - 边界情况：起点 `0` 本身可能没有出边，或所有边的 `start` 都大于 `0`，此时需要在原点“等待”。  
- **下次类似题**：**第一步先思考“是否可以把时间窗口转化为普通的边权重？”** 若答案是“可以”，立刻联想到 **Dijkstra + 堆**，否则考虑 BFS/DP 等其他思路。