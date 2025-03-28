# #3123. **找出最短路径中的边** / Find Edges in Shortest Paths

> 难度：困难 · 标签：Depth-First Search、Breadth-First Search、Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/find-edges-in-shortest-paths/)

---

## 题目（英文原版）

**Description**

You are given an undirected weighted graph of n nodes numbered from 0 to n - 1. The graph consists of m edges represented by a 2D array edges, where edges[i] = [ai, bi, wi] indicates that there is an edge between nodes ai and bi with weight wi.
Consider all the shortest paths from node 0 to node n - 1 in the graph. You need to find a boolean array answer where answer[i] is true if the edge edges[i] is part of at least one shortest path. Otherwise, answer[i] is false.
Return the array answer.
Note that the graph may not be connected.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[0,1,4],[0,2,1],[1,3,2],[1,4,3],[1,5,1],[2,3,1],[3,5,3],[4,5,2]]
Output: [true,true,true,false,true,true,true,false]
Explanation:
The following are all the shortest paths between nodes 0 and 5:
```

**Example 2:**

```
Input: n = 4, edges = [[2,0,1],[0,1,1],[0,3,4],[3,2,2]]
Output: [true,false,false,true]
Explanation:
There is one shortest path between nodes 0 and 3, which is the path 0 -> 2 -> 3 with the sum of weights 1 + 2 = 3 .
```

**Constraints**

- 2 <= n <= 5 * 104
- m == edges.length
- 1 <= m <= min(5 * 104, n * (n - 1) / 2)
- 0 <= ai, bi < n
- ai != bi
- 1 <= wi <= 105
- There are no repeated edges.

---

## 题目（中文翻译）

给定一个 **无向加权图（undirected weighted graph）**，该图有 `n` 个节点，编号为 `0` 到 `n - 1`。图由 `m` 条边组成，存放在二维数组 `edges` 中，其中 `edges[i] = [a_i, b_i, w_i]` 表示在节点 `a_i` 与节点 `b_i` 之间存在一条权重为 `w_i` 的边。

考虑图中从节点 `0` 到节点 `n - 1` 的所有 **最短路径（shortest paths）**。需要返回一个布尔数组 `answer`，其中 `answer[i]` 为 `true` 表示第 `i` 条边 `edges[i]` 至少出现在一条最短路径中；否则为 `false`。

**注意**：图可能不连通。

返回数组 `answer`。

---

### 示例

#### 示例 1
```text
Input: n = 6, edges = [[0,1,4],[0,2,1],[1,3,2],[1,4,3],[1,5,1],[2,3,1],[3,5,3],[4,5,2]]
Output: [true,true,true,false,true,true,true,false]
Explanation:
以下是节点 0 与节点 5 之间的所有最短路径：
```

#### 示例 2
```text
Input: n = 4, edges = [[2,0,1],[0,1,1],[0,3,4],[3,2,2]]
Output: [true,false,false,true]
Explanation:
节点 0 与节点 3 之间唯一的最短路径是 0 → 2 → 3，权重和为 1 + 2 = 3。
```

---

### 约束条件
- `2 <= n <= 5 * 10^4`
- `m == edges.length`
- `1 <= m <= min(5 * 10^4, n * (n - 1) / 2)`
- `0 <= a_i, b_i < n`
- `a_i != b_i`
- `1 <= w_i <= 10^5`
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的路径**，看看哪些路径恰好是从 `0` 到 `n‑1` 的最短路径，然后把路径里出现的每条边标记为 `True`。  
实现上可以：

1. 用 **深度优先搜索（DFS）** 把图的所有路径都遍历出来（每次把已经走过的节点记在 visited 集合里防止死循环）。  
2. 对每条完整的 `0 → n‑1` 路径，计算它的总权重，记录下最小的权重 `best`。  
3. 再次遍历所有 `0 → n‑1` 路径，只要它的权重等于 `best`，就把路径上出现的每条边在答案数组里置为 `True`。

> **类比**：把图想象成城市的路网，DFS 就像是一个旅行者不停地在城市之间徘徊，尝试所有可能的旅行路线，最后挑出花费最少的钱的旅行计划。

> **为什么正确**：只要我们真的把 **所有** 从 `0` 到 `n‑1` 的路径都列举出来，就一定能找到所有最短路径。只要把这些最短路径涉及的边标记出来，答案自然完整。

> **缺点**：路径的数量在最坏情况下是指数级的（比如完全图），即使 `n` 只有 20，路径数也可能达到几万甚至更多。对于本题的约束（`n` 可达 5·10⁴，`m` 也可能是 5·10⁴），暴力遍历根本不可能在时间限制内完成。

#### 代码（Python）

```python
from typing import List

def findEdgesBruteForce(n: int, edges: List[List[int]]) -> List[bool]:
    # 建图：邻接表，保存 (neighbor, weight, edge_index)
    graph = [[] for _ in range(n)]
    for idx, (u, v, w) in enumerate(edges):
        graph[u].append((v, w, idx))
        graph[v].append((u, w, idx))

    all_paths = []          # 存放所有 0 → n-1 的路径，路径用 (total_weight, [edge_idx, ...]) 表示
    visited = [False] * n   # 防止在一次 DFS 中走回头路

    def dfs(u: int, cur_w: int, used_edges: List[int]):
        """深度优先搜索所有路径"""
        if u == n - 1:               # 到达终点，记录一条完整路径
            all_paths.append((cur_w, used_edges.copy()))
            return
        visited[u] = True
        for v, w, e_idx in graph[u]:
            if not visited[v]:       # 只往未访问的节点走，防止环路
                used_edges.append(e_idx)
                dfs(v, cur_w + w, used_edges)
                used_edges.pop()
        visited[u] = False

    dfs(0, 0, [])
    # 1. 找到最小权重
    best = min(w for w, _ in all_paths) if all_paths else float('inf')
    # 2. 标记所有出现在最短路径里的边
    ans = [False] * len(edges)
    for w, e_list in all_paths:
        if w == best:                # 只处理最短路径
            for e in e_list:
                ans[e] = True
    return ans
```

> **注**：上述代码只适用于非常小的输入，主要用来帮助大家“感受”暴力思路，实际提交会超时。

#### 复杂度  

- **时间复杂度**：`O(所有路径的总长度)`，在最坏情况下是指数级的（`O(2^n)`），因为我们要把每条可能的路径都枚举出来。用大白话说，就是“随节点数指数增长”，根本不可接受。  
- **空间复杂度**：`O(递归深度 + 记录的路径数)`，同样可能达到指数级。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点不在于判断某条边是否在“某条”最短路径里，而在于快速得到**从 `0` 出发到每个节点的最短距离**以及**从 `n‑1` 出发到每个节点的最短距离**。有了这两个距离数组，就能在 **O(1)** 的时间内判断一条边是否可能出现在 *至少一条* 最短路径中。

**关键观察**  

设 `dist0[x]` 为从 `0` 到节点 `x` 的最短距离，`distN[x]` 为从 `n‑1` 到节点 `x` 的最短距离（因为图是无向的，这相当于从 `x` 到 `n‑1` 的最短距离）。  
记 `D = dist0[n-1]` 为 **全局最短路径长度**（从 `0` 到 `n‑1` 的最短距离）。

对于一条无向边 `u‑v`（权重 `w`）：

- 如果我们沿着这条边 **从 `u` 到 `v`** 前进，那么一条可能的路径长度为  
  `dist0[u] + w + distN[v]`。  
- 同理，**从 `v` 到 `u`** 前进的路径长度为  
  `dist0[v] + w + distN[u]`。

只要这两种可能的路径中 **有一种** 正好等于全局最短长度 `D`，说明这条边可以作为 *某条* 最短路径的一段。于是判断公式是：

```
edge i belongs to a shortest path  ⇔
dist0[u] + w + distN[v] == D   or   dist0[v] + w + distN[u] == D
```

**如何得到 `dist0` 与 `distN`？**  
- 图的权重均为正数（≥1），所以我们可以使用 **Dijkstra 算法**（最小堆 + 贪心）在 `O(m log n)` 时间内求出单源最短路径。  
- 只需要运行两次 Dijkstra：一次从源点 `0`，一次从目标点 `n‑1`（因为是无向图，倒着跑和正着跑效果相同）。

**整体步骤**  

1. **建图**：用邻接表保存 `(neighbor, weight, edge_index)`，方便后面遍历。  
2. **Dijkstra(0)** → 得到 `dist0`。  
3. **Dijkstra(n‑1)** → 得到 `distN`。  
4. `D = dist0[n-1]`。如果 `D` 为无穷大，说明 `0` 与 `n‑1` 不连通，此时所有答案都是 `False`。  
5. 对每条边 `edges[i] = [u, v, w]`，按照上面的公式检查是否满足等式，若满足则 `answer[i] = True`，否则 `False`。

> **类比**：  
> 想象有两位快递员分别从仓库（0）和收件点（n‑1）出发，沿着最短路线奔跑。某条道路能出现在最短快递路线里，当且仅当两位快递员分别到达这条道路的两端后，再沿这条道路相会，恰好正好用掉整个最短总时长。

#### 代码（Python）

```python
import heapq
from typing import List

def findEdges(n: int, edges: List[List[int]]) -> List[bool]:
    """
    返回一个布尔数组 answer，answer[i] 为 True 表示 edges[i] 至少在
    一条从 0 到 n-1 的最短路径中出现。
    """

    # ---------- 1. 建图 ----------
    # graph[u] = list of (v, weight, edge_index)
    graph = [[] for _ in range(n)]
    for idx, (u, v, w) in enumerate(edges):
        graph[u].append((v, w, idx))
        graph[v].append((u, w, idx))

    # ---------- 2. Dijkstra ----------
    def dijkstra(start: int) -> List[int]:
        """返回从 start 出发到所有节点的最短距离列表"""
        INF = 10**18
        dist = [INF] * n
        dist[start] = 0
        heap = [(0, start)]                # (当前距离, 节点)
        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:               # 过时的条目，直接跳过
                continue
            for v, w, _ in graph[u]:
                nd = d + w                 # 经过边 u‑v 后的新距离
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        return dist

    dist0 = dijkstra(0)          # 从 0 出发的最短距离
    distN = dijkstra(n - 1)      # 从 n-1 出发的最短距离（等价于到 n-1 的距离）

    INF = 10**18
    total_shortest = dist0[n - 1]   # 0 → n-1 的最短路径长度

    # 如果 0 与 n-1 不连通，直接返回全 False
    if total_shortest >= INF:
        return [False] * len(edges)

    # ---------- 3. 检查每条边 ----------
    answer = [False] * len(edges)
    for idx, (u, v, w) in enumerate(edges):
        # 两种可能的方向：u→v 或 v→u
        if dist0[u] + w + distN[v] == total_shortest or \
           dist0[v] + w + distN[u] == total_shortest:
            answer[idx] = True
    return answer
```

> **代码要点**  
> - `heapq` 实现的最小堆保证每次弹出的都是当前未确定的最短距离节点，正是 Dijkstra 的核心。  
> - `if d != dist[u]` 用来跳过已经被更小的距离更新过的“旧”堆元素，避免不必要的遍历。  
> - 两次 Dijkstra 的时间复杂度都是 `O(m log n)`，所以整体是 `O(m log n)`，在本题约束下完全可接受。

#### 复杂度  

- **时间复杂度**：`O(m log n)`  
  - 每次 Dijkstra 需要遍历所有 `m` 条边，并在堆中做 `log n` 的插入/弹出操作。我们运行两遍，所以仍是同量级。用大白话说，就是“边的数量乘以对数级的额外开销”，对 `5·10⁴` 规模的数据毫无压力。  
- **空间复杂度**：`O(n + m)`  
  - 邻接表占 `O(n + m)`，距离数组 `dist0`、`distN` 各占 `O(n)`，堆最坏也只会存 `O(n)` 条记录。整体就是线性空间，和输入规模同级。

---

## 心得

- **核心技巧**：利用 **双向最短路**（从起点和终点各跑一次 Dijkstra）把“是否在最短路径上”转化为简单的等式判断。  
- **适用的题型**  
  1. “判断边/点是否在所有/任意最短路径中”——如 LeetCode 785（判断边是否在任意最短路径上）。  
  2. “在有向图中找所有关键路径/桥”——常用 `distFromStart + edgeWeight + distToEnd == shortest` 判断关键边。  
  3. “求最短路径树的边集合”——同样需要两次单源最短路。  
- **一句话总结**：**最短路径的“拼图”只要把两端的最短距离拼起来，等式成立的边就是答案。**

---

## 反思

- **第一反应**：看到“所有最短路径”，自然想到枚举或 BFS/DFS 找到每条路径，却忽视了图规模巨大，导致思路太慢。  
- **最容易踩的坑**  
  - **图不连通**：`dist0[n-1]` 可能是无穷大，需要提前返回全 `False`。  
  - **整数溢出**：距离可能累计到 `10⁵ * 5·10⁴`，在 Python 中不怕溢出，但在其他语言要用 `long long`。  
  - **双向等式的顺序**：忘记检查两种方向（`u→v` 与 `v→u`），会导致部分合法边被漏掉。  
- **下次类似题的第一步**：**先求出起点和终点的单源最短距离**（常用 Dijkstra），再用这些距离做**等式或不等式判断**，而不是直接枚举路径。这样既直观又高效。