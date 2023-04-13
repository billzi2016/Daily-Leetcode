# #2203. 满足所需路径的最小权重子图 / Minimum Weighted Subgraph With the Required Paths

> 难度：困难 · 标签：Graph、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-weighted-subgraph-with-the-required-paths/)

---

## 题目（英文原版）

**Description**

You are given an integer n denoting the number of nodes of a weighted directed graph. The nodes are numbered from 0 to n - 1.
You are also given a 2D integer array edges where edges[i] = [fromi, toi, weighti] denotes that there exists a directed edge from fromi to toi with weight weighti.
Lastly, you are given three distinct integers src1, src2, and dest denoting three distinct nodes of the graph.
Return the minimum weight of a subgraph of the graph such that it is possible to reach dest from both src1 and src2 via a set of edges of this subgraph. In case such a subgraph does not exist, return -1.
A subgraph is a graph whose vertices and edges are subsets of the original graph. The weight of a subgraph is the sum of weights of its constituent edges.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]], src1 = 0, src2 = 1, dest = 5
Output: 9
Explanation:
The above figure represents the input graph.
The blue edges represent one of the subgraphs that yield the optimal answer.
Note that the subgraph [[1,0,3],[0,5,6]] also yields the optimal answer. It is not possible to get a subgraph with less weight satisfying all the constraints.
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,1],[2,1,1]], src1 = 0, src2 = 1, dest = 2
Output: -1
Explanation:
The above figure represents the input graph.
It can be seen that there does not exist any path from node 1 to node 2, hence there are no subgraphs satisfying all the constraints.
```

**Constraints**

- 3 <= n <= 105
- 0 <= edges.length <= 105
- edges[i].length == 3
- 0 <= fromi, toi, src1, src2, dest <= n - 1
- fromi != toi
- src1, src2, and dest are pairwise distinct.
- 1 <= weight[i] <= 105

---

## 题目（中文翻译）

给定一个整数 `n` 表示一个 **加权有向图**（weighted directed graph）的节点数，节点编号为 `0` 到 `n-1`。  
同时给定一个二维整数数组 `edges`，其中 `edges[i] = [from_i, to_i, weight_i]` 表示存在一条 **有向边**（directed edge）`from_i -> to_i`，其权重为 `weight_i`。  
再给定三个互不相同的整数 `src1`, `src2` 和 `dest`，分别代表图中的三个不同节点。

返回一个子图（subgraph）的最小总权重，使得在该子图中能够分别从 `src1` 和 `src2` 到达 `dest`（即存在两条从 `src1`、`src2` 到 `dest` 的路径，路径仅由子图的边组成）。如果不存在满足条件的子图，返回 `-1`。

**子图**（subgraph）是指其顶点（vertex）和边都是原图的子集。子图的权重定义为其所有构成边的权重之和。

---

## 示例

### 示例 1

**输入**  
`n = 6`  
`edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]]`  
`src1 = 0, src2 = 1, dest = 5`

**输出**  
`9`

**解释**  
上图展示了输入的有向图。蓝色的边构成了一个满足要求且权重最小的子图。  
同样，子图 `[[1,0,3],[0,5,6]]` 也能得到相同的最优答案。不存在权重更小的满足条件的子图。

### 示例 2

**输入**  
`n = 3`  
`edges = [[0,1,1],[2,1,1]]`  
`src1 = 0, src2 = 1, dest = 2`

**输出**  
`-1`

**解释**  
上图展示了输入的有向图。可以看到从节点 `1` 到节点 `2` 没有任何路径，因此不存在满足所有约束条件的子图。

---

## 约束条件

- `3 <= n <= 10^5`
- `0 <= edges.length <= 10^5`
- `edges[i].length == 3`
- `0 <= from_i, to_i, src1, src2, dest <= n - 1`
- `from_i != to_i`
- `src1`, `src2` 与 `dest` 两两互不相同
- `1 <= weight_i <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的路径都算出来**，再挑出满足条件且权值最小的那条（或那几条）路径。  
具体可以这样做：

1. 先求出 **任意两点之间的最短路径**。  
   - 这相当于把图中的每一条路都记在一本“大字典”里，字典的键是 `(起点, 终点)`，值是这两点之间的最短路程。  
   - 在算法里，这一步可以用 **Floyd‑Warshall**（所有点对最短路）实现。把每个节点想象成一本字典的页码，`dist[i][j]` 就是第 `i` 页到第 `j` 页的最短距离。

2. 有了所有点对的最短距离后，遍历每个可能的**会合点** `v`（`0 ≤ v < n`），计算三段路的总权值：
   - `src1 → v` 的最短距离 `dist[src1][v]`
   - `src2 → v` 的最短距离 `dist[src2][v]`
   - `v → dest` 的最短距离 `dist[v][dest]`
   - 三段加起来就是一种合法子图的权值。

3. 取所有 `v` 中的最小值即为答案。如果某段距离不存在（用 `inf` 表示），说明该会合点不可行，直接跳过。

> **为什么暴力解是对的？**  
> 在最优子图里，两条从 `src1`、`src2` 出发的路径一定会在某个节点 `v` 汇合，然后共同走向 `dest`（题目提示）。所以只要把所有可能的 `v` 都尝试一次，必然能找到最优答案。

#### 代码（Python）

```python
import math
from typing import List

def minimumWeightBruteForce(n: int, edges: List[List[int]],
                           src1: int, src2: int, dest: int) -> int:
    # ---------- 1. 建立距离矩阵，初始为无穷大 ----------
    INF = math.inf
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0                     # 到自己距离为 0

    # ---------- 2. 把所有直接边的权重填进去 ----------
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)    # 可能有重边，取最小的

    # ---------- 3. Floyd‑Warshall：求所有点对最短路 ----------
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:          # i 到 k 不可达，跳过
                continue
            for j in range(n):
                if dist[k][j] == INF:      # k 到 j 不可达，跳过
                    continue
                # 通过 k 中转，看看能不能更短
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # ---------- 4. 枚举会合点，找最小总权值 ----------
    ans = INF
    for meet in range(n):
        d1 = dist[src1][meet]
        d2 = dist[src2][meet]
        d3 = dist[meet][dest]
        if d1 == INF or d2 == INF or d3 == INF:
            continue                      # 这条会合点不可行
        ans = min(ans, d1 + d2 + d3)

    return -1 if ans == INF else ans
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 想象 `n` 为 10⁵ 时，`n³` 相当于 **一万亿次** 的循环，根本跑不完。这里的 `O(n³)` 其实是 “立方级别”，比 `O(n²)`（平方）要慢得多，像是跑 1000 km 的马拉松 vs 10 km 的短跑。

- **空间复杂度**：`O(n²)`  
  - 需要保存一个 `n × n` 的二维数组，就像在纸上画一个 `n` 行 `n` 列的格子表，`n=10⁵` 时根本装不下（需要 10¹⁰ 个格子）。

> 暴力解思路清晰，但在本题的约束（`n、edges ≤ 10⁵`）下根本不可行，只能作为“最直观的想法”来帮助我们发现真正的优化点。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道：**最优子图的两条路径一定在某个节点 `v` 汇合**，然后共享同一段到 `dest` 的路径。于是我们只需要找出每个可能的 `v`，以及从 `src1、src2、v` 到 `dest` 的最短距离。

关键是**如何快速得到这些最短距离**？  
这里可以利用 **单源最短路**（Dijkstra）：

1. **从 `src1` 出发**，跑一次 Dijkstra，得到 `dist1[i]` —— 从 `src1` 到所有节点 `i` 的最短距离。  
   - 把图想象成一个城市的道路网络，`src1` 是出发的住宅，`dist1[i]` 就是去每个地点的最短费用。

2. **从 `src2` 出发**，再跑一次 Dijkstra，得到 `dist2[i]`。

3. **从 `dest` 逆向出发**（即在 **反向图** 上跑 Dijkstra），得到 `distDest[i]` —— 从任意节点 `i` 到 `dest` 的最短距离。  
   - 这里的“反向图”相当于把所有道路的方向调转，想象成把公交车的行驶方向倒过来，这样一次搜索就能算出所有点到 `dest` 的最短费用。

4. 有了这三组距离后，枚举每个会合点 `v`，计算  
   `total = dist1[v] + dist2[v] + distDest[v]`。  
   只要这三个值都不是无穷大（即路径可达），`total` 就是一种合法子图的权值。取最小的 `total` 即为答案。

> **为什么只需要三次 Dijkstra 就够了？**  
> Dijkstra 能在 **带权有向图** 中找出 **单点到所有点** 的最短路径，时间是 `O((n + m) log n)`（`m` 为边数）。我们分别从 `src1`、`src2`、`dest`（在反向图上）三次搜索，就把所有需要的最短距离一次性收集齐了。再遍历 `v` 只需要 `O(n)`，整体复杂度远低于暴力解。

#### 代码（Python）

```python
import heapq
from typing import List, Tuple

INF = 10**18                         # 足够大的正整数，表示不可达

def dijkstra(start: int, adj: List[List[Tuple[int, int]]]) -> List[int]:
    """
    单源最短路（带权有向图）
    adj[u] = [(v, w), ...] 表示从 u 到 v 的有向边，权重为 w
    返回数组 dist，其中 dist[i] 为 start -> i 的最短距离（不可达为 INF）
    """
    n = len(adj)
    dist = [INF] * n
    dist[start] = 0
    heap = [(0, start)]               # (当前累计权重, 节点)

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:              # 旧的、已经被更短路径更新的记录，直接跳过
            continue
        for v, w in adj[u]:
            nd = d + w                 # 经过 u -> v 的新距离
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist

def minimumWeight(n: int, edges: List[List[int]],
                  src1: int, src2: int, dest: int) -> int:
    # ---------- 1. 建图 ----------
    forward = [[] for _ in range(n)]   # 正向邻接表
    reverse = [[] for _ in range(n)]   # 反向邻接表（用于从 dest 逆向搜索）
    for u, v, w in edges:
        forward[u].append((v, w))
        reverse[v].append((u, w))      # 把方向反过来存

    # ---------- 2. 三次 Dijkstra ----------
    dist1 = dijkstra(src1, forward)    # src1 -> every node
    dist2 = dijkstra(src2, forward)    # src2 -> every node
    distDest = dijkstra(dest, reverse)  # every node -> dest（在反向图上）

    # ---------- 3. 枚举会合点 ----------
    ans = INF
    for meet in range(n):
        d1, d2, d3 = dist1[meet], dist2[meet], distDest[meet]
        if d1 == INF or d2 == INF or d3 == INF:
            continue                    # 该会合点不可达
        ans = min(ans, d1 + d2 + d3)

    return -1 if ans == INF else ans
```

#### 复杂度

- **时间复杂度**：`O((n + m) log n)`  
  - 每次 Dijkstra 需要遍历所有节点和所有边一次（`n + m`），并且每条边会产生一次堆操作，堆的大小最多是 `n`，每次操作 `log n`。我们执行三次，所以整体仍是同量级的 `O((n + m) log n)`。  
  - 与暴力解的 `O(n³)` 相比，这里是 **对数级别的提升**，在 `n、m ≤ 10⁵` 时轻松跑完。

- **空间复杂度**：`O(n + m)`  
  - 需要存储两套邻接表（正向、反向）以及三条距离数组，每个都和节点或边的数量成线性关系。相比暴力解的 `O(n²)`，这里只用 **几倍于输入大小的内存**，完全可接受。

---

## 心得

- **核心技巧**：**三次单源最短路 + 枚举会合点**。  
  通过把“两条路径在某点汇合”这一结构化信息抽象出来，我们只需要知道从三个起点到所有节点的最短距离，而不必枚举所有可能的子图。

- **适用的题型**  
  1. **两个起点共终点的最小合并路径**（如 LeetCode 1263 `Minimum Sum of Four Digit Number After Splitting Digits` 的变形）  
  2. **从多个来源汇聚到同一目标的最短总费用**（如 “Minimum Cost to Supply Water”）  
  3. **需要在图中找公共前缀/会合点的题目**（如 “Shortest Path with Alternating Colors” 中的变体）

- **一句话总结解题钥匙**：  
  “把复杂的子图选择问题转化为**三次单源最短路**，再在所有可能的会合点上做一次线性扫描。”

---

## 反思

- **第一反应**：看到“子图的权值最小”，本能想把所有边的组合枚举或做全图的最短路（Floyd‑Warshall），但马上意识到规模太大。

- **最容易踩的坑**  
  1. **遗漏反向图**：必须在 **反向图** 上跑 Dijkstra 才能得到“任意节点到 dest”的最短距离。直接从 `dest` 正向跑只能得到 `dest` 到其他节点的距离，方向相反会导致错误。  
  2. **溢出**：累加三段距离时要使用足够大的 `INF`（如 `10**18`），防止 `int` 溢出或误判为可达。  
  3. **重边处理**：同一对节点可能有多条边，建图时要保留所有边（因为 Dijkstra 会自行挑选最小的），不要只保留一条。

- **下次遇到同类题**：第一步先 **抽象出“会合点”或“公共前缀”**，然后判断是否可以通过 **多次单源最短路** 把所有需要的距离一次性算出，再在会合点上线性枚举。这样既能保证正确性，又能把时间复杂度控制在 `O((n+m)log n)`。