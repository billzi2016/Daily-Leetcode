# #2608. 图中最短环 / Shortest Cycle in a Graph

> 难度：困难 · 标签：Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/shortest-cycle-in-a-graph/)

---

## 题目（英文原版）

**Description**

There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1. The edges in the graph are represented by a given 2D integer array edges, where edges[i] = [ui, vi] denotes an edge between vertex ui and vertex vi. Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.
Return the length of the shortest cycle in the graph. If no cycle exists, return -1.
A cycle is a path that starts and ends at the same node, and each edge in the path is used only once.

**Examples**

**Example 1:**

```
Input: n = 7, edges = [[0,1],[1,2],[2,0],[3,4],[4,5],[5,6],[6,3]]
Output: 3
Explanation: The cycle with the smallest length is : 0 -> 1 -> 2 -> 0
```

**Example 2:**

```
Input: n = 4, edges = [[0,1],[0,2]]
Output: -1
Explanation: There are no cycles in this graph.
```

**Constraints**

- 2 <= n <= 1000
- 1 <= edges.length <= 1000
- edges[i].length == 2
- 0 <= ui, vi < n
- ui != vi
- There are no repeated edges.

---

## 题目（中文翻译）

给定一个有 `n` 个节点的双向图（bi-directional graph），节点编号为 `0` 到 `n - 1`。图中的边由二维整数数组 `edges` 表示，`edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间存在一条无向边。任意一对节点至多有一条边，且不存在自环。

返回图中最短环（cycle）的长度。如果图中不存在环，返回 `-1`。  
环是指起点和终点相同的路径（path），并且路径中的每条边只能使用一次。

**示例 1：**  
**输入:** `n = 7, edges = [[0,1],[1,2],[2,0],[3,4],[4,5],[5,6],[6,3]]`  
**输出:** `3`  
**解释:** 最短的环是 `0 -> 1 -> 2 -> 0`，长度为 3。

**示例 2：**  
**输入:** `n = 4, edges = [[0,1],[0,2]]`  
**输出:** `-1`  
**解释:** 该图中不存在环。

**约束条件：**
- `2 <= n <= 1000`
- `1 <= edges.length <= 1000`
- `edges[i].length == 2`
- `0 <= ui, vi < n`
- `ui != vi`
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一条边都单独拿出来检查**，看看它能不能组成一个环。  
具体做法如下：

1. 任选一条边 `u‑v`，暂时把它从图里“踢掉”。  
2. 在剩下的图里，用 **广度优先搜索（BFS）** 求 `u` 到 `v` 的最短路径长度 `dist`。  
   - BFS 就像在城市里找最少换乘的公交路线，一层层往外扩散，先到达的就是最近的。  
3. 如果 `u` 能够走到 `v`（说明 `dist` 有值），那么原来的那条被踢掉的边 `u‑v` 再加上这条最短路径，就形成了一个环，环的长度是 `dist + 1`（多加的那条被踢掉的边）。  
4. 对所有边都这么算，取最小的环长就是答案；如果所有边都找不到路径，则说明图里没有环，返回 `-1`。

> **为什么正确？**  
> 环的定义要求每条边只能用一次。把环中的任意一条边删掉，剩下的必然是一条从环的起点到终点的 **简单路径**（不重复点）。因此，只要我们遍历每条边并检查删掉它后是否还能连通两端，就一定能找到所有可能的环，最短的那个自然就是答案。

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortest_cycle_bruteforce(n: int, edges: List[List[int]]) -> int:
    # 把无向图转成邻接表，邻接表就像“每个人的朋友列表”
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    INF = float('inf')
    ans = INF                         # 用一个很大的数表示“目前还没找到环”

    # ---------- 对每一条边做一次 BFS ----------
    for u, v in edges:
        # 1️⃣ 把这条边暂时删除：在 BFS 里不允许走 u->v 或 v->u
        # 为了不改动原始邻接表，直接在 BFS 时判断
        dist = [-1] * n                # -1 表示“还没被访问”
        q = deque([u])
        dist[u] = 0

        while q:
            cur = q.popleft()
            # 如果已经比当前最小环长更长，就可以提前结束本次 BFS
            if dist[cur] * 2 + 1 >= ans:   # 粗略的上界剪枝
                continue
            for nxt in adj[cur]:
                # 跳过被“踢掉”的那条边
                if (cur == u and nxt == v) or (cur == v and nxt == u):
                    continue
                if dist[nxt] == -1:          # 第一次遇到，记录距离
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)

        # 2️⃣ 检查 u 能否到达 v
        if dist[v] != -1:                    # 能到达，说明形成环
            ans = min(ans, dist[v] + 1)      # 环长 = 最短路径 + 被删的那条边

    return -1 if ans == INF else ans
```

> **关键行中文注释**  
> - `adj = [[] for _ in range(n)]`：为每个顶点准备一个“朋友列表”。  
> - `dist = [-1] * n`：`dist[i]` 记录从起点 `u` 到节点 `i` 的层数（即 BFS 步数），`-1` 表示还没访问。  
> - `if (cur == u and nxt == v) or (cur == v and nxt == u): continue`：这一步把当前检查的那条边“踢掉”。  
> - `ans = min(ans, dist[v] + 1)`：得到一个环的长度，和当前最小值比较取最小。

#### 复杂度

- **时间复杂度**：`O(E * (V + E))`  
  - 对每条边 (`E` 条) 都要跑一次 BFS。一次 BFS 在无向图里最多遍历所有顶点和所有边，时间是 `O(V + E)`。  
  - 对于本题的约束 `V ≤ 1000, E ≤ 1000`，最坏约为 `1000 * (1000 + 1000) = 2·10⁶`，在 Python 里完全可以接受。  
  - **大白话**：想象你把每条路都拔掉一次，然后在剩下的城镇里找最短的“绕行”路线。每次找路都要遍历全部城镇和路，总共要这么做 `E` 次。

- **空间复杂度**：`O(V + E)`  
  - `adj` 存储邻接表，需要 `O(V + E)` 的空间。  
  - BFS 队列和 `dist` 数组各占 `O(V)`。  
  - 这就是我们在地图上画的所有道路和城市的占用空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 **对每条边做一次 BFS**，时间已经是 `O(E·(V+E))`。在本题的规模（`V, E ≤ 1000`）下，这已经是可以接受的最优复杂度——没有更快的通用算法能在所有无向图里找最短环并保证正确性。

不过，我们可以把 **“对每条边”** 的视角换成 **“对每个顶点”**，实现上更简洁且常见的写法：

1. 对每个起点 `s`，执行一次 BFS，记录每个节点的距离 `dist` 与它的父节点 `parent`（从哪儿走进来的）。  
2. 在 BFS 过程中，如果我们从当前节点 `u` 看到了一个已经被访问过的邻居 `v`，且 `v` 不是 `u` 的父节点（即这条边不是我们刚走来的那条），说明我们找到了一个环：  
   - 环的长度 = `dist[u] + dist[v] + 1`（从 `s` 到 `u` 的距离 + 从 `s` 到 `v` 的距离 + 这条横跨的边）。  
3. 对所有起点 `s` 记录最小的环长，即为答案。  
4. 如果遍历完所有起点仍未发现环，则返回 `-1`。

> **为什么这一步比暴力更“优”？**  
> - 实际上两者的时间量级相同，都是 `O(V·(V+E))`，但这里只需要 **一次 BFS** 对每个顶点，而不是每条边。代码更易读，且在实际运行时常常更快（因为 BFS 的遍历次数会少于对每条边都完整遍历一次的情况）。  
> - 关键点在于 **利用 BFS 的层次结构**：当我们在同一层或相邻层之间发现已经访问过的节点时，必然形成最短环。

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortest_cycle_optimal(n: int, edges: List[List[int]]) -> int:
    # 建立邻接表
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    INF = float('inf')
    answer = INF

    # ---------- 以每个顶点为起点做一次 BFS ----------
    for start in range(n):
        dist = [-1] * n          # 到每个节点的层数，-1 表示未访问
        parent = [-1] * n        # 记录 BFS 树的父节点
        q = deque([start])
        dist[start] = 0

        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1:               # 第一次遇到 v
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
                elif parent[u] != v:            # 已经访问过且不是父子关系 → 环
                    # 环长 = 从 start 到 u 的距离 + 从 start 到 v 的距离 + 这条横跨的边
                    cycle_len = dist[u] + dist[v] + 1
                    answer = min(answer, cycle_len)

        # 小优化：如果当前最小环已经是 3（最小可能），可以提前结束
        if answer == 3:
            break

    return -1 if answer == INF else answer
```

> **关键行中文注释**  
> - `parent[v] = u`：记录 `v` 是从哪个节点走进来的，等价于“谁把我拉进了队列”。  
> - `elif parent[u] != v:`：如果当前邻居 `v` 已经被访问，且它不是 `u` 的父节点，说明我们在 BFS 树中找到了一个“横跨的边”，这正是环的入口。  
> - `cycle_len = dist[u] + dist[v] + 1`：把两条树枝的长度相加，再加上横跨的这条边，就是完整环的长度。  
> - `if answer == 3: break`：在无向图里，最短环的长度不可能小于 3（因为不允许自环和重边），一旦找到 3 就可以直接返回。

#### 复杂度

- **时间复杂度**：`O(V * (V + E))`  
  - 对每个顶点 `V` 做一次 BFS，单次 BFS 的遍历代价仍是 `O(V + E)`。  
  - 与暴力解的量级相同，但实际常数更小，代码更简洁。  
  - **大白话**：想象你把每座城市依次当作“起点”，从那里出发一次性探查所有可能的环，找最短的那一个。

- **空间复杂度**：`O(V + E)`  
  - 邻接表、`dist`、`parent`、队列共用 `O(V + E)` 的空间。

---

## 心得

- **核心技巧**：在无向图中，用 **BFS** 同时记录层次 (`dist`) 与父节点 (`parent`)，一旦在同一层或相邻层之间看到已经访问过的节点且不是父子关系，就找到了一个最短环。  
- **适用的题型**  
  1. **最短环**（本题）。  
  2. **判断图中是否存在奇环**（判断二分图）。  
  3. **求无向图中任意两点的最短闭路**（如 “寻找最小闭合路径” 类题）。  
- **一句话总结解题钥匙**：*“在 BFS 树里，非父子相连的两点必构成最短环”。*

---

## 反思

- **第一反应**：看到“最短环”立刻想到“把每条边删掉后找最短路径”，因为环本质上是“路径 + 额外一条边”。  
- **最容易踩的坑**  
  - **遗漏自环/重边**：题目已经保证没有，但如果出现，需要单独处理。  
  - **父子关系判断错误**：在 BFS 中检测环时必须排除“刚走来的那条边”，否则会把树枝本身误判为环。  
  - **边界条件**：图中没有环时要返回 `-1`，而不是默认的 `0` 或 `INF`。  
- **下次类似题的第一步**：先想 **“把环拆成路径 + 一条额外边”**，然后决定是 **对每条边** 还是 **对每个顶点** 用 BFS/DFS 去找最短路径或直接检测环。这样思路清晰、实现也更稳妥。