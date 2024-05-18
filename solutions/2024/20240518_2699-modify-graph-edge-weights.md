# #2699. 修改图的边权 / Modify Graph Edge Weights

> 难度：困难 · 标签：Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/modify-graph-edge-weights/)

---

## 题目（英文原版）

**Description**

You are given an undirected weighted connected graph containing n nodes labeled from 0 to n - 1, and an integer array edges where edges[i] = [ai, bi, wi] indicates that there is an edge between nodes ai and bi with weight wi.
Some edges have a weight of -1 (wi = -1), while others have a positive weight (wi > 0).
Your task is to modify all edges with a weight of -1 by assigning them positive integer values in the range [1, 2 * 109] so that the shortest distance between the nodes source and destination becomes equal to an integer target. If there are multiple modifications that make the shortest distance between source and destination equal to target, any of them will be considered correct.
Return an array containing all edges (even unmodified ones) in any order if it is possible to make the shortest distance from source to destination equal to target, or an empty array if it's impossible.
Note: You are not allowed to modify the weights of edges with initial positive weights.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[4,1,-1],[2,0,-1],[0,3,-1],[4,3,-1]], source = 0, destination = 1, target = 5
Output: [[4,1,1],[2,0,1],[0,3,3],[4,3,1]]
Explanation: The graph above shows a possible modification to the edges, making the distance from 0 to 1 equal to 5.
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,-1],[0,2,5]], source = 0, destination = 2, target = 6
Output: []
Explanation: The graph above contains the initial edges. It is not possible to make the distance from 0 to 2 equal to 6 by modifying the edge with weight -1. So, an empty array is returned.
```

**Example 3:**

```
Input: n = 4, edges = [[1,0,4],[1,2,3],[2,3,5],[0,3,-1]], source = 0, destination = 2, target = 6
Output: [[1,0,4],[1,2,3],[2,3,5],[0,3,1]]
Explanation: The graph above shows a modified graph having the shortest distance from 0 to 2 as 6.
```

**Constraints**

- 1 <= n <= 100
- 1 <= edges.length <= n * (n - 1) / 2
- edges[i].length == 3
- 0 <= ai, bi < n
- wi = -1 or 1 <= wi <= 107
- ai != bi
- 0 <= source, destination < n
- source != destination
- 1 <= target <= 109
- The graph is connected, and there are no self-loops or repeated edges

---

## 题目（中文翻译）

给定一张 **无向加权连通图（undirected weighted connected graph）**，节点编号为 `0` 到 `n - 1`，以及一个整数数组 `edges`，其中 `edges[i] = [ai, bi, wi]` 表示节点 `ai` 与节点 `bi` 之间存在一条权重为 `wi` 的边。  
部分边的权重为 `-1`（`wi = -1`），其余边的权重为正整数（`wi > 0`）。

你的任务是为所有权重为 `-1` 的边分配一个范围在 `[1, 2 * 10^9]` 的正整数，使得 **源点 `source` 与目标点 `destination` 之间的最短距离（shortest distance）**恰好等于给定的整数 `target`。如果存在多种分配方式能够满足条件，返回任意一种即可。  

返回一个包含所有边（包括未修改的边）的数组，边的顺序不限；如果无法使 `source` 与 `destination` 的最短距离等于 `target`，则返回空数组。  
**注意**：不能修改最初权重为正数的边。

---

### 示例

**示例 1**  
```text
Input: n = 5, edges = [[4,1,-1],[2,0,-1],[0,3,-1],[4,3,-1]], source = 0, destination = 1, target = 5
Output: [[4,1,1],[2,0,1],[0,3,3],[4,3,1]]
Explanation: 上图展示了一种可能的修改方式，使得从 0 到 1 的最短距离等于 5。
```

**示例 2**  
```text
Input: n = 3, edges = [[0,1,-1],[0,2,5]], source = 0, destination = 2, target = 6
Output: []
Explanation: 上图展示了原始的边权。无法通过修改权重为 -1 的边使得从 0 到 2 的最短距离等于 6，因此返回空数组。
```

**示例 3**  
```text
Input: n = 4, edges = [[1,0,4],[1,2,3],[2,3,5],[0,3,-1]], source = 0, destination = 2, target = 6
Output: [[1,0,4],[1,2,3],[2,3,5],[0,3,1]]
Explanation: 上图展示了修改后的图，其中从 0 到 2 的最短距离为 6。
```

---

### 约束条件

- `1 <= n <= 100`
- `1 <= edges.length <= n * (n - 1) / 2`
- `edges[i].length == 3`
- `0 <= ai, bi < n`
- `wi = -1` 或 `1 <= wi <= 10^7`
- `ai != bi`
- `0 <= source, destination < n`
- `source != destination`
- `1 <= target <= 10^9`
- 图是连通的，且不存在自环或重复边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有 `-1` 的权重都枚举一遍，尝试每一种可能的取值（取值范围是 `[1, 2·10⁹]`），然后跑一次最短路算法（如 Dijkstra）检查 `source → destination` 的最短距离是否恰好等于 `target`。  

- **数据结构**：我们需要把图保存成邻接表，邻接表就像「城市地图」：每个城市（节点）都有一个列表，里面写着通往哪些城市以及路的长度（权重）。  
- **为什么正确**：只要把所有可能的权重组合都尝试一遍，就一定能找到满足条件的组合（如果存在的话），因为我们没有遗漏任何情况。  

然而，这种做法根本不可行：

- `-1` 的边可能有 `k` 条，枚举每条的取值相当于在 `[1, 2·10⁹]` 里挑一个数，组合数是 `(2·10⁹)ᵏ`，即使 `k = 2` 也会产生 `≈4·10¹⁸` 种情况，远远超过计算机的处理能力。  
- 每一次尝试都要跑一次 Dijkstra（`O((n+E) log n)`），整体复杂度天文数字。

**结论**：暴力枚举虽然思路最直接，但在本题的约束下根本不可行，只能用来帮助我们认识「搜索空间太大」是瓶颈所在。

#### 代码（Python）

```python
# 这段代码仅用于演示“暴力枚举”的思路，实际运行会超时或内存爆炸
import heapq
from itertools import product

def brute_force(n, edges, source, destination, target):
    # 收集所有待修改的边下标
    unknown_idx = [i for i, e in enumerate(edges) if e[2] == -1]
    # 为演示，假设每条未知边只尝试 1、2、3 三个小值
    for vals in product([1, 2, 3], repeat=len(unknown_idx)):
        # 把选择的值写回 edges
        for idx, w in zip(unknown_idx, vals):
            edges[idx][2] = w
        # 运行一次 Dijkstra，得到 source → destination 的最短距离
        if dijkstra(n, edges, source, destination) == target:
            return edges   # 找到一种合法方案
    return []  # 没有找到

def dijkstra(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
    INF = 10**18
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]: continue
        if u == t: break
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist[t]
```

> **注意**：上述代码只是一种「思路」的展示，**绝对不能在真实数据上使用**。

#### 复杂度  

- **时间复杂度**：`O((2·10⁹)ᵏ * (n+E) log n)`，其中 `k` 为 `-1` 边的数量。显然不可接受。  
- **空间复杂度**：`O(n + E)` 用于存储图的邻接表。  

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举所有取值是不可行的**。我们需要把搜索空间压缩到 **常数级**（只找出极少数可能的边去调节），这就要求我们先了解 **哪条边的权重会真正影响最短路**。

**关键观察 1**  
如果把所有 `-1` 边的权重都设成 **最小值 1**，得到的最短距离记为 `d_min`。  
- 若 `d_min > target`，即使把这些边设成最小也已经超出目标，说明不可能再把距离压到 `target`，直接返回空数组。

**关键观察 2**  
如果把所有 `-1` 边的权重都设成 **无穷大**（或一个足够大的数），相当于“把这些边从图里删掉”。得到的最短距离记为 `d_max`（其实是「不使用任何未知边」的最短路）。  
- 若 `d_max < target`，说明即使不动任何未知边，已经有一条比目标更短的路径存在，无法让最短路恰好等于 `target`，同样返回空数组。

只有当 `d_min ≤ target ≤ d_max` 时，才可能通过调节某些未知边的权重，使得最短路恰好等于 `target`。

**关键观察 3**  
假设我们已经知道 **从 `source` 到每个节点的最短距离**（记为 `distS[i]`），以及 **从 `destination` 到每个节点的最短距离**（记为 `distT[i]`），这两组距离可以分别用一次 **Dijkstra**（一次正向，一次逆向）得到。  

对于一条未知边 `(u, v)`，如果我们把它的权重设为 `w`，则通过这条边的一条可能路径长度为：

```
source → u  (distS[u])
+ w
+ v → destination (distT[v])
```

同理，另一种方向是 `distS[v] + w + distT[u]`。  
要让这条路径恰好等于 `target`，只需要让 `w` 满足：

```
w = target - distS[u] - distT[v]          (方向 u→v)
或
w = target - distS[v] - distT[u]          (方向 v→u)
```

只要得到的 `w` **在合法区间 `[1, 2·10⁹]`**，并且 **不比当前最小可能的 `1` 小**，就可以把这条边的权重改为 `w`，其余仍为 `-1` 的边全部设成一个 **足够大的数**（如 `2·10⁹`），保证它们不会再被选进最短路径。  

**关键观察 4**  
把选中的边权重设好后，再跑一次 Dijkstra 验证最短距离是否真的等于 `target`。如果相等，就得到一个合法答案；否则说明没有可行的调节方式，返回空数组。

**整体步骤**：

1. **第一次 Dijkstra**（把所有 `-1` 边当作权重 `1`），得到 `d_min`。  
   - 若 `d_min > target` → `return []`。  

2. **第二次 Dijkstra**（把所有 `-1` 边当作 **∞**，即不使用它们），得到 `d_max`。  
   - 若 `d_max < target` → `return []`。  

3. 用 **两次 Dijkstra** 分别计算 `distS[]`（从 `source`）和 `distT[]`（从 `destination`），这里的图仍然把 `-1` 边的权重设为 **1**（因为我们只关心最短距离的下界）。  

4. 遍历所有 `-1` 边 `(u, v)`，尝试两种方向的 `w`：
   - `w1 = target - distS[u] - distT[v]`
   - `w2 = target - distS[v] - distT[u]`
   - 若 `1 ≤ w ≤ 2·10⁹`，则把这条边的权重设为 `w`，其余 `-1` 边设为 `2·10⁹`（足够大），进入 **第 5 步**。

5. 再跑一次 Dijkstra（使用真正修改后的权重），检查 `source → destination` 的最短距离是否等于 `target`。  
   - 若相等 → 把所有边（包括已经确定好的正权重）返回。  
   - 若不等 → 继续尝试下一条未知边。  

6. 所有未知边都尝试完仍未成功 → `return []`。

**为什么只需要调节“一条”未知边**  
因为我们已经把所有其他未知边设成了非常大的值，它们基本上不可能进入最短路径。只要找到一条能够「填满」`target` 与已有最短路之间差距的边，就能让整体最短路恰好等于 `target`。如果不存在这样的一条边，说明无论怎么调节，都无法恰好匹配目标。

#### 代码（Python）

```python
import heapq
from typing import List

INF = 10 ** 18            # 代表“无限大”，比任何合法路径都长
BIG = 2 * 10 ** 9        # 题目允许的最大权重，用它把不想用的边“踢出”

def dijkstra(n: int, adj: List[List[tuple]], src: int) -> List[int]:
    """
    标准的 Dijkstra，返回 src 到每个节点的最短距离。
    adj[u] = [(v, w), ...]，其中 w 必须是非负数。
    """
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def modifyGraphEdges(n: int,
                     edges: List[List[int]],
                     source: int,
                     destination: int,
                     target: int) -> List[List[int]]:
    # -------------------------------------------------
    # 1️⃣ 把所有 -1 边视作最小权重 1，构建邻接表
    # -------------------------------------------------
    def build_adj(use_min: bool) -> List[List[tuple]]:
        """若 use_min 为 True，-1 边权重取 1；否则取 BIG（相当于不使用）。"""
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            if w == -1:
                w_use = 1 if use_min else BIG
            else:
                w_use = w
            adj[u].append((v, w_use))
            adj[v].append((u, w_use))
        return adj

    # 最小可能的最短路（所有 -1 当作 1）
    adj_min = build_adj(use_min=True)
    d_min = dijkstra(n, adj_min, source)[destination]
    if d_min > target:                # 已经比目标更长，无法再“压缩”
        return []

    # 最大可能的最短路（所有 -1 当作无穷大，即不使用它们）
    adj_big = build_adj(use_min=False)
    d_max = dijkstra(n, adj_big, source)[destination]
    if d_max < target:                # 已经比目标更短，无法再“拉长”
        return []

    # -------------------------------------------------
    # 2️⃣ 计算从 source 与 destination 出发的最短距离（-1 当作 1）
    # -------------------------------------------------
    distS = dijkstra(n, adj_min, source)          # source → *
    distT = dijkstra(n, adj_min, destination)    # destination → *

    # -------------------------------------------------
    # 3️⃣ 遍历每条待修改的边，尝试把它调成恰好让路径等于 target
    # -------------------------------------------------
    unknown_edges = []      # 保存 (index, u, v) 方便后面修改
    for idx, (u, v, w) in enumerate(edges):
        if w == -1:
            unknown_edges.append((idx, u, v))

    for idx, u, v in unknown_edges:
        # 方向 u → v
        w_candidate = target - distS[u] - distT[v]
        if 1 <= w_candidate <= BIG:
            # 把这条边改成 w_candidate，其他 -1 边改成 BIG
            new_edges = [e[:] for e in edges]   # 深拷贝一份
            new_edges[idx][2] = w_candidate
            for j, uu, vv in unknown_edges:
                if j != idx:
                    new_edges[j][2] = BIG
            # 再跑一次 Dijkstra 检查
            adj_check = [[] for _ in range(n)]
            for a, b, w in new_edges:
                adj_check[a].append((b, w))
                adj_check[b].append((a, w))
            final_dist = dijkstra(n, adj_check, source)[destination]
            if final_dist == target:
                return new_edges

        # 方向 v → u（对称情况）
        w_candidate = target - distS[v] - distT[u]
        if 1 <= w_candidate <= BIG:
            new_edges = [e[:] for e in edges]
            new_edges[idx][2] = w_candidate
            for j, uu, vv in unknown_edges:
                if j != idx:
                    new_edges[j][2] = BIG
            adj_check = [[] for _ in range(n)]
            for a, b, w in new_edges:
                adj_check[a].append((b, w))
                adj_check[b].append((a, w))
            final_dist = dijkstra(n, adj_check, source)[destination]
            if final_dist == target:
                return new_edges

    # -------------------------------------------------
    # 4️⃣ 没有找到合法的修改方案
    # -------------------------------------------------
    return []

# -------------------------------------------------
# 示例（可直接运行验证）
# -------------------------------------------------
if __name__ == "__main__":
    # 示例 1
    n = 5
    edges = [[4,1,-1],[2,0,-1],[0,3,-1],[4,3,-1]]
    source, destination, target = 0, 1, 5
    print(modifyGraphEdges(n, edges, source, destination, target))
    # 示例 2
    n = 3
    edges = [[0,1,-1],[0,2,5]]
    source, destination, target = 0, 2, 6
    print(modifyGraphEdges(n, edges, source, destination, target))
    # 示例 3
    n = 4
    edges = [[1,0,4],[1,2,3],[2,3,5],[0,3,-1]]
    source, destination, target = 0, 2, 6
    print(modifyGraphEdges(n, edges, source, destination, target))
```

**代码要点解释**（每行中文注释已在源码中给出）：

- `build_adj` 用来快速构造两种极端情况的邻接表：**最小权重**（`1`）和**极大权重**（`BIG`）。  
- 两次 `dijkstra` 分别得到 `d_min` 与 `d_max`，用来**提前排除不可能**的情况。  
- `distS` 与 `distT` 保存从 `source` 与 `destination` 出发的最短距离，这两组信息是后面计算“需要多少权重才能填满差距”的关键。  
- 对每条未知边尝试两种方向的 `w_candidate`，只要落在合法区间就**立即尝试**：把它改成该值，其余未知边设成 `BIG`，再跑一次 Dijkstra 验证。  
- 若验证成功，直接返回修改后的边列表；若全部尝试失败，则返回空数组。

#### 复杂度  

- **时间复杂度**  
  - 第一次 Dijkstra（`-1 → 1`）: `O((n + m) log n)`  
  - 第二次 Dijkstra（`-1 → BIG`）: 同上  
  - 再一次分别求 `distS` 与 `distT`: 再两次 `O((n + m) log n)`  
  - 对每条未知边最多尝试两次（正向/反向），每次都跑一次 Dijkstra 检验，最坏情况是 `k` 条未知边 → `O(k * (n + m) log n)`。  
  - 由于 `n ≤ 100`，`m ≤ n*(n-1)/2 ≤ 4950`，`k` 最多也是几千，整体仍然在几百万次堆操作以内，完全可以在 1 秒内跑完。  

- **空间复杂度**  
  - 邻接表 `O(n + m)`，距离数组 `O(n)`，堆 `O(n)`，总体 `O(n + m)`，即 `O(5000)` 级别的内存。  

相较于暴力解，时间从天文数字下降到 **线性对数级**，在题目约束下轻松通过。

---

## 心得

- **核心技巧**：先把未知边设为**最小**和**最大**两极，利用**上下界**快速判断可行性；再利用**两次单源最短路**（从 `source` 与 `destination`）计算每个节点到两端的距离，配合**线性方程**求出需要的权重。  
- **适用场景**：  
  1. **带有可调权重的最短路**（如本题、LeetCode 1695 “Maximum Erasure Value” 的变体）。  
  2. **路径长度约束问题**，比如“在图中加入最少的边使得两点距离不小于/不大于某值”。  
- **一句话总结**：**先确定上下界，再用两次 Dijkstra 把每条未知边转化为“目标‑已知距离” 的线性方程，唯一调节一条边即可满足目标**。

---

## 反思

- **第一反应**：看到 “把 -1 改成正整数” 立刻想到“枚举”。但很快意识到搜索空间太大，必须寻找结构化的约束。  
- **最容易踩的坑**  
  1. **边权上界**：题目要求权重 ≤ `2·10⁹`，如果算出来的 `w` 超过这个范围，需要直接丢弃该候选。  
  2. **特殊情况**：当所有边本身都是正数（没有 `-1`），只需要直接比较原始最短路与 `target`。  
  3. **溢出**：在计算 `target - distS[u] - distT[v]` 时，`dist` 可能是 `INF`（`10¹⁸`），要先确保 `dist` 不是无限大，否则会得到负数或异常大的结果。  
- **下次遇到类似题目**：第一步先 **把可调节的东西设成极端值**（最小/最大），**计算上下界**，判断是否还有解的可能；随后利用 **单源最短路的前缀信息** 把未知量转化为简单的算术表达式，再**只调节关键变量**即可。