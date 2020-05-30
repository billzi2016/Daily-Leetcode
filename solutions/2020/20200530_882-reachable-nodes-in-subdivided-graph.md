# #882. 细分图中可达节点数 / Reachable Nodes In Subdivided Graph

> 难度：困难 · 标签：Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/reachable-nodes-in-subdivided-graph/)

---

## 题目（英文原版）

**Description**

You are given an undirected graph (the "original graph") with n nodes labeled from 0 to n - 1. You decide to subdivide each edge in the graph into a chain of nodes, with the number of new nodes varying between each edge.
The graph is given as a 2D array of edges where edges[i] = [ui, vi, cnti] indicates that there is an edge between nodes ui and vi in the original graph, and cnti is the total number of new nodes that you will subdivide the edge into. Note that cnti == 0 means you will not subdivide the edge.
To subdivide the edge [ui, vi], replace it with (cnti + 1) new edges and cnti new nodes. The new nodes are x1, x2, ..., xcnti, and the new edges are [ui, x1], [x1, x2], [x2, x3], ..., [xcnti-1, xcnti], [xcnti, vi].
In this new graph, you want to know how many nodes are reachable from the node 0, where a node is reachable if the distance is maxMoves or less.
Given the original graph and maxMoves, return the number of nodes that are reachable from node 0 in the new graph.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,10],[0,2,1],[1,2,2]], maxMoves = 6, n = 3
Output: 13
Explanation: The edge subdivisions are shown in the image above.
The nodes that are reachable are highlighted in yellow.
```

**Example 2:**

```
Input: edges = [[0,1,4],[1,2,6],[0,2,8],[1,3,1]], maxMoves = 10, n = 4
Output: 23
```

**Example 3:**

```
Input: edges = [[1,2,4],[1,4,5],[1,3,1],[2,3,4],[3,4,5]], maxMoves = 17, n = 5
Output: 1
Explanation: Node 0 is disconnected from the rest of the graph, so only node 0 is reachable.
```

**Constraints**

- 0 <= edges.length <= min(n * (n - 1) / 2, 104)
- edges[i].length == 3
- 0 <= ui < vi < n
- There are no multiple edges in the graph.
- 0 <= cnti <= 104
- 0 <= maxMoves <= 109
- 1 <= n <= 3000

---

## 题目（中文翻译）

你得到一个无向图（以下简称**原始图**），该图有 `n` 个节点，编号为 `0` 到 `n-1`。你决定将图中的每条边细分为一条由若干新节点组成的链，每条边细分后新增的节点数可以不同。  

图通过二维数组 `edges` 给出，其中 `edges[i] = [ui, vi, cnti]` 表示原始图中存在一条连接节点 `ui` 与 `vi` 的边，且你计划将这条边细分为 `cnti` 个新节点。若 `cnti == 0` 则表示这条边不进行细分。  

对边 `[ui, vi]` 进行细分时，需要用 `cnti + 1` 条新边和 `cnti` 个新节点来替代原边。新节点记为 `x1, x2, …, xcnti`，新边依次为 `[ui, x1]`, `[x1, x2]`, `[x2, x3]`, …, `[xcnti‑1, xcnti]`, `[xcnti, vi]`。  

在得到的 **新图** 中，若从节点 `0` 出发的最短距离不超过 `maxMoves`，则该节点被认为是**可达**的。给定原始图以及 `maxMoves`，返回新图中从节点 `0` 可达的节点总数。

示例 1:  
示例 2:  
示例 3:  

约束条件：

- `0 <= edges.length <= min(n * (n - 1) / 2, 10^4)`
- `edges[i].length == 3`
- `0 <= ui < vi < n`
- 图中不存在多条相同的边
- `0 <= cnti <= 10^4`
- `0 <= maxMoves <= 10^9`
- `1 <= n <= 3000`

---

### 示例

#### 示例 1
``` 
Input: edges = [[0,1,10],[0,2,1],[1,2,2]], maxMoves = 6, n = 3
Output: 13
Explanation: 上图展示了每条边的细分情况。所有可达的节点在图中用黄色标出。
```

#### 示例 2
``` 
Input: edges = [[0,1,4],[1,2,6],[0,2,8],[1,3,1]], maxMoves = 10, n = 4
Output: 23
```

#### 示例 3
``` 
Input: edges = [[1,2,4],[1,4,5],[1,3,1],[2,3,4],[3,4,5]], maxMoves = 17, n = 5
Output: 1
Explanation: 节点 0 与图的其余部分不相连，因此只有节点 0 是可达的。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有细分后的节点真的全部建出来**，再在这张完整的图上做一次普通的 BFS/DFS，统计距离不超过 `maxMoves` 的节点个数。

- **把每条原始边 `[u, v, cnt]` 展开**  
  - 在 `u` 与 `v` 之间插入 `cnt` 个新节点 `x1 … xcnt`。  
  - 把原来的单条无向边换成 `cnt+1` 条无向边：`u‑x1, x1‑x2, …, xcnt‑v`。  
- **得到的图**  
  - 原始节点数 `n`（最多 3000）  
  - 细分节点数 `∑ cnt`，每条边的 `cnt` 最多 10⁴，边的数量最多 10⁴ → **最坏情况下会有上亿个节点**。  
- **遍历**  
  - 从节点 `0` 开始，用 BFS 按层次展开，记录每个节点到 `0` 的最短距离。  
  - 只要距离 ≤ `maxMoves`，计数即可。

> **生活化类比**：把哈希表想成一本词典，`key` 是单词，`value` 是所在的页码。这里把每条边想成一本“道路手册”，我们把它展开成一条条“小路”，再把所有小路拼在一起，最后在这本巨大的手册里找“能在 `maxMoves` 步以内走到的所有地点”。

**为什么这个方法一定能得到正确答案**  
因为我们没有在算法层面做任何近似：所有细分后的节点都实际存在，普通的 BFS 能找出每个节点的真实最短距离，只要距离 ≤ `maxMoves` 就算作可达。

#### 代码（Python）

```python
from collections import deque, defaultdict

def reachable_nodes_bruteforce(n, edges, maxMoves):
    # 1️⃣ 把每条原始边细分成真实的节点和边
    graph = defaultdict(list)          # adjacency list of the expanded graph
    node_id = n                         # 新节点的编号从 n 开始递增

    for u, v, cnt in edges:
        prev = u
        # 在 u 和 v 之间依次插入 cnt 个新节点
        for _ in range(cnt):
            cur = node_id
            node_id += 1
            graph[prev].append(cur)
            graph[cur].append(prev)
            prev = cur
        # 最后把最后一个新节点（或直接 u）连到 v
        graph[prev].append(v)
        graph[v].append(prev)

    total_nodes = node_id                # 包含原始节点 + 所有细分节点

    # 2️⃣ BFS 求最短距离
    dist = [-1] * total_nodes
    q = deque([0])
    dist[0] = 0
    while q:
        cur = q.popleft()
        for nxt in graph[cur]:
            if dist[nxt] == -1:          # 未访问过
                nd = dist[cur] + 1
                if nd > maxMoves:       # 超出 maxMoves 的就不必继续扩展
                    continue
                dist[nxt] = nd
                q.append(nxt)

    # 3️⃣ 统计可达节点数
    reachable = sum(1 for d in dist if d != -1)
    return reachable
```

> **关键行解释**  
> - `graph[prev].append(cur)` / `graph[cur].append(prev)`：在无向图里把新节点连起来，等价于在字典里查“相邻的页码”。  
> - `if nd > maxMoves: continue`：如果已经超过了最大步数，就不必继续往下走，类似于在词典里找不到对应的页码就停下来。

#### 复杂度  

- **时间复杂度**：`O(V + E)`，其中  
  - `V = n + Σ cnt`（所有原始 + 细分节点）  
  - `E = Σ (cnt + 1)`（每条原始边拆成 `cnt+1` 条）  
  在最坏情况下 `V`、`E` 都可以达到 **上亿**，所以实际会超时/内存溢出。  
- **空间复杂度**：`O(V + E)`，需要把所有细分节点存进邻接表，同样会爆内存。

> **大白话**：`O(n²)` 里的 “n” 不是题目里给的原始节点数，而是 **所有细分后产生的节点数**，它可能非常非常大，导致算法根本跑不完。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**把细分节点全部显式存下来**。其实我们并不需要真的创建这些节点，只要知道：

1. 从原始节点 `u` 到原始节点 `v` 之间的“距离”是多少（因为细分的每条小边都算 1 步）。  
2. 对于每条原始边，**有多少细分节点可以在 `maxMoves` 步之内被到达**。

这两个信息足以算出答案，而不必展开图。于是我们采用 **Dijkstra 最短路**（因为所有边权都是正数）在 **原始图** 上先求出每个原始节点到 `0` 的最短距离。  
- 对于原始边 `[u, v, cnt]`，我们把它的权重设为 `cnt + 1`（走完整条细分链需要的步数）。  
- 用 **优先队列（最小堆）** 实现 Dijkstra，时间 `O(E log V)`，这里的 `V = n ≤ 3000`，`E ≤ 10⁴`，非常轻松。

得到 `dist[u]`（从 `0` 到原始节点 `u` 的最短步数）后：

- **原始节点本身**：如果 `dist[u] ≤ maxMoves`，说明 `u` 可达，计 1。  
- **细分节点**：设从 `u` 端还能继续走 `remain_u = max(0, maxMoves - dist[u])` 步，意味着可以在这条边上向里走 `remain_u` 个细分节点（最多 `cnt`）。同理得到 `remain_v`。  
  - 两端走到的细分节点可能会重叠（比如两端都走到中间），所以 **实际可达的细分节点数** 为  
    ```text
    reachable_on_this_edge = min(cnt, remain_u + remain_v)
    ```
    - `remain_u + remain_v` 表示两端“各自能占领”的节点数之和。  
    - `cnt` 是这条边上总共的细分节点数，不能超过它。

把所有原始节点的可达计数与所有边上可达的细分节点数相加，即为答案。

> **类比**：想象每条原始边是一条长走廊，走廊两头分别是原始节点 `u`、`v`，走廊里有 `cnt` 盏灯（细分节点）。我们先算出从入口 `0` 到每个房间（原始节点）的最短距离，然后看还能在走廊里走多少步，灯就被点亮。两头点亮的灯可能会在中间相遇，所以最终点亮的灯数只能是走廊灯的总数 `cnt` 与两头能走的步数之和的最小值。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

def reachableNodes(n, edges, maxMoves):
    """
    :type n: int
    :type edges: List[List[int]]
    :type maxMoves: int
    :rtype: int
    """
    # 1️⃣ 建立原始图的邻接表，边的权重 = cnt + 1（走完整条细分链需要的步数）
    graph = defaultdict(list)          # node -> list of (neighbor, weight, cnt)
    for u, v, cnt in edges:
        w = cnt + 1                     # 实际步数
        graph[u].append((v, w, cnt))
        graph[v].append((u, w, cnt))

    # 2️⃣ Dijkstra：求每个原始节点到 0 的最短距离
    INF = 10**18
    dist = [INF] * n
    dist[0] = 0
    heap = [(0, 0)]                     # (distance, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:                # 已经有更短的距离
            continue
        for v, w, _ in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    # 3️⃣ 统计可达的原始节点
    ans = sum(1 for d in dist if d <= maxMoves)

    # 4️⃣ 统计每条边上可达的细分节点
    for u, v, cnt in edges:
        # 从 u 端还能往里走多少步
        remain_u = max(0, maxMoves - dist[u])
        # 从 v 端还能往里走多少步
        remain_v = max(0, maxMoves - dist[v])
        # 两端占领的细分节点数之和，最多 cnt
        ans += min(cnt, remain_u + remain_v)

    return ans
```

> **关键行解释**  
> - `w = cnt + 1`：把细分链视作“一条长度为 `cnt+1` 的路”。  
> - `if nd < dist[v]:`：Dijkstra 的核心——如果找到更短的路径，就更新并放进堆。  
> - `remain_u = max(0, maxMoves - dist[u])`：从 `u` 出发还能往前走多少步，负数说明根本到不了 `u`，取 0。  
> - `ans += min(cnt, remain_u + remain_v)`：两端能覆盖的灯数之和，最多不超过这条走廊本身的灯数 `cnt`。

#### 复杂度  

- **时间复杂度**：`O(E log V)`  
  - `E` 为原始边数 ≤ 10⁴，`V = n ≤ 3000`。  
  - 这一步相当于在原始图上跑一次“最快路线”，远比在展开后的亿级图上遍历要快得多。  
- **空间复杂度**：`O(V + E)`  
  - 只保存原始图的邻接表以及 `dist` 数组，最多几千个节点、几万条边，内存轻松可用。

> **对比**：暴力解需要 `O(Σ cnt)` 的时间和空间（可能上亿），而最优解只和原始图规模成正比，几乎瞬间结束。

---

## 心得

- **核心技巧**：把「细分后的大量中间节点」抽象成「边的权重」进行最短路计算，然后再用剩余步数在每条边上“分配”可达的中间节点。  
- **适用的题型**  
  1. **带权图的可达节点计数**（如 LeetCode 882 `Reachable Nodes In Subdivided Graph`）  
  2. **在有额外“内部资源”但不想显式展开的图**（如“在每条道路上放置若干补给站”之类的问题）  
  3. **需要在边上做额外计数的最短路变形**（如“在每条路上最多可经过 k 次”）  
- **一句话总结解题钥匙**：**用 Dijkstra 只在原始节点上求最短距离，再把剩余的步数“洒在边上”算细分节点**。

---

## 反思

- **第一反应**：看到「细分」二字就想到把每条边拆成很多小点，直接建图、BFS。虽然思路直观，却忽视了约束中的 `cnt` 可能非常大，导致不可行。  
- **最容易踩的坑**  
  - **忘记对 `cnt = 0` 的边处理**：仍然要把权重设为 `1`（`cnt+1`），否则 Dijkstra 会把这条边当作不存在。  
  - **双端计数时的重复**：两端分别算的细分节点可能重叠，需要 `min(cnt, remain_u + remain_v)` 防止超过实际数量。  
  - **距离可能超过 `maxMoves`**：`dist[u]` 可能是 `INF`，直接用 `maxMoves - dist[u]` 会产生负数，记得 `max(0, …)`。  
- **下次类似题的第一步**：先判断 **是否真的需要显式展开**，若 “内部结构” 只影响距离或计数，尝试把它压缩为 **权重** 或 **额外的数学关系**，再在原始规模的图上跑经典算法（Dijkstra、BFS、DP 等）。