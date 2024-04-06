# #2642. 设计可计算最短路径的图 / Design Graph With Shortest Path Calculator

> 难度：困难 · 标签：Graph、Design、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/design-graph-with-shortest-path-calculator/)

---

## 题目（英文原版）

**Description**

There is a directed weighted graph that consists of n nodes numbered from 0 to n - 1. The edges of the graph are initially represented by the given array edges where edges[i] = [fromi, toi, edgeCosti] meaning that there is an edge from fromi to toi with the cost edgeCosti.
Implement the Graph class:

**Examples**

**Example 1:**

```
Input
["Graph", "shortestPath", "shortestPath", "addEdge", "shortestPath"]
[[4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]]], [3, 2], [0, 3], [[1, 3, 4]], [0, 3]]
Output
[null, 6, -1, null, 6]

Explanation
Graph g = new Graph(4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]]);
g.shortestPath(3, 2); // return 6. The shortest path from 3 to 2 in the first diagram above is 3 -> 0 -> 1 -> 2 with a total cost of 3 + 2 + 1 = 6.
g.shortestPath(0, 3); // return -1. There is no path from 0 to 3.
g.addEdge([1, 3, 4]); // We add an edge from node 1 to node 3, and we get the second diagram above.
g.shortestPath(0, 3); // return 6. The shortest path from 0 to 3 now is 0 -> 1 -> 3 with a total cost of 2 + 4 = 6.
```

**Constraints**

- 1 <= n <= 100
- 0 <= edges.length <= n * (n - 1)
- edges[i].length == edge.length == 3
- 0 <= fromi, toi, from, to, node1, node2 <= n - 1
- 1 <= edgeCosti, edgeCost <= 106
- There are no repeated edges and no self-loops in the graph at any point.
- At most 100 calls will be made for addEdge.
- At most 100 calls will be made for shortestPath.

---

## 题目（中文翻译）

**描述**  
给定一个由 `n` 个节点（编号为 `0` 到 `n - 1`）组成的有向加权图。图的初始边通过数组 `edges` 给出，其中 `edges[i] = [from_i, to_i, edgeCost_i]` 表示存在一条从 `from_i` 到 `to_i` 的边，权重为 `edgeCost_i`（即边的代价）。

请实现 `Graph` 类，使其能够：

- 在构造函数中初始化节点数 `n` 与初始边 `edges`；
- 支持动态添加新边 `addEdge([from, to, edgeCost])`；
- 计算两节点之间的最短路径 `shortestPath(from, to)`，若不存在路径返回 `-1`。

**约束条件**
- `1 <= n <= 100`
- `0 <= edges.length <= n * (n - 1)`
- `edges[i].length == edge.length == 3`
- `0 <= from_i, to_i, from, to, node1, node2 <= n - 1`
- `1 <= edgeCost_i, edgeCost <= 10^6`
- 图中不存在重复边和自环（self-loop）。
- 最多调用 `addEdge` 100 次。
- 最多调用 `shortestPath` 100 次。

**示例**

```json
Input
["Graph", "shortestPath", "shortestPath", "addEdge", "shortestPath"]
[[4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]]], [3, 2], [0, 3], [[1, 3, 4]], [0, 3]]
Output
[null, 6, -1, null, 6]
```

**解释**  
```java
Graph g = new Graph(4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]]);
g.shortestPath(3, 2); // 返回 6。图中从 3 到 2 的最短路径为 3 -> 0 -> 1 -> 2，总代价为 6。
...
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有节点之间的最短距离一次性算出来**，以后查询 `shortestPath(u, v)` 时只要直接返回预先算好的答案。  
这可以用 **Floyd‑Warshall** 算法实现：

1. 用一个二维数组 `dist[i][j]` 保存从 `i` 到 `j` 的当前最短距离。  
   - 初始时如果有直接边 `i → j`，`dist[i][j] = edgeCost`；否则设为 `∞`（一个很大的数）。  
   - `dist[i][i] = 0`（从自己到自己不花费）。  
2. 三层循环：把每个节点 `k` 当作「中转站」尝试更新 `dist[i][j]`：  
   ```
   for k in range(n):
       for i in range(n):
           for j in range(n):
               dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
   ```
   这相当于「如果走 `i → k → j` 更短，就把距离改成更小的那条路」。

**为什么这个方法能得到正确答案？**  
Floyd‑Warshall 的核心是「动态规划」的思想：在考虑前 `k` 个节点作为中转点时，已经算出了所有只经过这 `k` 个节点的最短路径。把第 `k+1` 个节点加入后，只需要检查一次「是否经过新节点会更短」即可。循环结束后，`dist[i][j]` 就是任意两点的最短距离。

**用到的数据结构**  
- **二维数组**（矩阵）`dist`：可以把它想象成「城市之间的距离表」，行是出发城市，列是目的城市，格子里写的就是最小花费。  
- **∞（无穷大）**：相当于字典里查不到的词，表示「目前还不知道有路可以到达」。

#### 代码（Python）

```python
import math
from typing import List

class Graph:
    def __init__(self, n: int, edges: List[List[int]]):
        """初始化图，直接把所有边写进距离矩阵"""
        self.n = n
        # dist[i][j] 表示 i -> j 的最小费用，初始为无穷大
        self.dist = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            self.dist[i][i] = 0                     # 到自己距离为 0
        for u, v, w in edges:                       # 把已有边写进去
            self.dist[u][v] = w

        # 直接跑一次 Floyd‑Warshall，得到所有点对的最短路
        self._floyd_warshall()

    def _floyd_warshall(self) -> None:
        """核心的三层循环，更新 self.dist"""
        n = self.n
        for k in range(n):               # 中转点
            for i in range(n):           # 起点
                if self.dist[i][k] == math.inf:
                    continue            # i 到 k 还不可达，直接跳过
                for j in range(n):       # 终点
                    # i -> k -> j 是否更短
                    new_cost = self.dist[i][k] + self.dist[k][j]
                    if new_cost < self.dist[i][j]:
                        self.dist[i][j] = new_cost

    def addEdge(self, edge: List[int]) -> None:
        """新增一条有向边，然后重新跑 Floyd‑Warshall"""
        u, v, w = edge
        # 直接把新边放进矩阵（可能比原来的更短）
        if w < self.dist[u][v]:
            self.dist[u][v] = w
        # 因为图结构改变，需要重新计算所有最短路
        self._floyd_warshall()

    def shortestPath(self, src: int, dst: int) -> int:
        """查询 src 到 dst 的最短距离，若不可达返回 -1"""
        ans = self.dist[src][dst]
        return -1 if ans == math.inf else ans
```

> 代码中每一行都加了中文注释，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：  
  - 初始化时一次 Floyd‑Warshall：`O(n³)`。  
  - 每次 `addEdge` 也要重新跑 `O(n³)`（因为我们重新算所有点对）。  
  - `shortestPath` 只做一次数组查找，`O(1)`。  
  - 对于本题的约束（`n ≤ 100`，最多 100 次 `addEdge`），`100 * 100³ = 10⁸` 仍在 Python 能接受的范围内，但并不是最优的做法。  

- **空间复杂度**：`O(n²)`，因为保存了一个 `n × n` 的距离矩阵。可以把它想成「把所有城市之间的距离全部写在一张大表上」——占用的空间随节点数的平方增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次添加新边都要把整个 `n³` 的循环跑一遍。实际上，**我们并不需要每次都重新算所有点对的最短路**，只要在查询时即时计算 **单源最短路径** 就行。  

**核心技巧**：  
- **Dijkstra 算法**（带堆的实现）能够在 `O(E log V)` 时间内求出从单个起点到所有其他节点的最短距离，`E` 为边数，`V` 为节点数。  
- 因为 `shortestPath` 调用次数最多只有 100 次，直接在每次查询时运行一次 Dijkstra 就足够快。  
- `addEdge` 只需要把新边加入邻接表（相当于往「城市的出发列表」里加一条新路线），不需要做任何额外计算。

**为什么 Dijkstra 能比 Floyd‑Warshall 快？**  
- Floyd‑Warshall 每次都要遍历 **所有** 三元组合 `(i, j, k)`，即使图很稀疏（边很少）也要花 `n³` 的时间。  
- Dijkstra 只关注从起点能到达的节点，用**最小堆**（Priority Queue）每次挑出当前已知的最近节点，像“按费用从低到高排队”，只遍历真正需要的边，时间随边的数量线性增长（乘以堆的对数因子）。

**数据结构解释**  

| 数据结构 | 类比 | 作用 |
|----------|------|------|
| **邻接表** `adj[u] = [(v, w), …]` | 每个城市的“公交站牌”，站牌上写着能坐哪条线路（`v`）以及票价（`w`） | 只保存实际存在的路，省空间 |
| **最小堆 / 优先队列** | “费用最小的候选城市排在最前面”，类似超市排队时最先服务费用最少的顾客 | 每次快速取出当前距离最近的未访问节点 |
| **dist 数组** | “从起点到每个城市的当前已知最小花费”，相当于“到各站的最快路线表” | 记录 Dijkstra 过程中的最短距离 |

**一步步推导**  

1. **初始化**：把 `edges` 转成邻接表 `adj`。  
2. **addEdge**：直接在 `adj[from].append((to, cost))`。因为题目保证不出现重复边和自环，直接加入即可。  
3. **shortestPath(src, dst)**：  
   - 创建 `dist = [∞] * n`，`dist[src] = 0`。  
   - 把 `(0, src)` 放进堆 `pq`（费用、节点）。  
   - 循环弹出堆顶 `(d, u)`：  
     - 如果 `u` 已经是 `dst`，直接返回 `d`（最短路径已找到）。  
     - 若弹出的 `d` 大于 `dist[u]`，说明这是一个“旧的”记录，直接跳过。  
     - 遍历 `adj[u]` 的每条出边 `(v, w)`，尝试松弛（relax）：如果 `d + w < dist[v]`，更新 `dist[v]` 并把 `(dist[v], v)` 推入堆。  
   - 循环结束后若 `dist[dst]` 仍是 `∞`，说明不可达，返回 `-1`。  

**图示**（文字版）  
```
src ----5----> A ----2----> dst
 \                         ^
  \---3----> B ----4------/
```
从 `src` 开始，堆里先有 `(0, src)`。弹出后把两条路的费用 `5`、`3` 放进去，堆会先弹出费用更小的 `(3, B)`，继续扩展，最终得到最小费用 `7`（`src->B->dst`）。

#### 代码（Python）

```python
import heapq
from typing import List, Tuple

class Graph:
    def __init__(self, n: int, edges: List[List[int]]):
        """构造函数：建立邻接表"""
        self.n = n
        # adj[u] = list of (v, cost) 表示从 u 出发的所有有向边
        self.adj: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        for u, v, w in edges:
            self.adj[u].append((v, w))

    def addEdge(self, edge: List[int]) -> None:
        """在图中插入一条新有向边"""
        u, v, w = edge
        self.adj[u].append((v, w))          # 直接追加到邻接表

    def shortestPath(self, src: int, dst: int) -> int:
        """使用 Dijkstra 计算 src -> dst 的最短距离，若不可达返回 -1"""
        INF = 10**18                         # 足够大的“无穷大”
        dist = [INF] * self.n
        dist[src] = 0
        # 堆中存 (当前已知最小费用, 节点编号)
        heap = [(0, src)]

        while heap:
            d, u = heapq.heappop(heap)      # 取出费用最小的未确定节点
            if u == dst:                    # 已经到达目标，d 就是最短路
                return d
            if d != dist[u]:                # 旧的记录，直接跳过
                continue

            # 遍历 u 的所有出边，尝试松弛
            for v, w in self.adj[u]:
                nd = d + w                  # 走这条边后的新费用
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))

        # 循环结束仍未到达 dst，说明不可达
        return -1
```

> 代码已完整标注中文注释，可直接复制运行。

#### 复杂度  

- **时间复杂度**：  
  - `addEdge` 只做一次列表追加，`O(1)`。  
  - `shortestPath` 使用 Dijkstra：`O(E log V)`。在最坏情况下（稠密图）`E ≈ V²`，但本题 `V ≤ 100`，`E ≤ 100·99`，所以最多约 `10⁴·log100`，极其快速。  
  - 与暴力解的 `O(n³)` 相比，这里只随 **实际边数** 增长，通常要快很多。

- **空间复杂度**：`O(V + E)`，即邻接表占用的空间。相比 `O(V²)` 的矩阵，省了不少内存，尤其当图稀疏时更明显。

---

## 心得  

- **核心技巧**：**Dijkstra + 堆**（最小优先队列）实现单源最短路径。  
- **适用题型**（类似思路）：  
  1. LeetCode 743. **Network Delay Time** – 需要从单点向所有节点传播最短时间。  
  2. LeetCode 1514. **Path with Maximum Probability** – 用概率取对数后仍可用 Dijkstra。  
  3. LeetCode 787. **Cheapest Flights Within K Stops**（改造版） – 需要限制中转次数的最短路。  
- **一句话总结解题钥匙**：  
  > “每次查询只算一次最短路，用堆把最近的节点挑出来，避免全局的 `n³` 计算。”  

---

## 反思  

- **第一反应**：看到“动态添加边、查询最短路”，立刻想到要维护所有点对的距离，于是想到 Floyd‑Warshall。  
- **最容易踩的坑**：  
  - **边权为正**：Dijkstra 只能在所有权值非负时使用；若出现负权需改用 Bellman‑Ford。  
  - **堆中旧记录**：弹出的 `(d, u)` 可能已经被更新为更小的距离，需要 `if d != dist[u]: continue` 来过滤。  
  - **不可达返回 -1**：不要忘记把 `∞`（未更新）转成题目要求的 `-1`。  
- **下次遇到同类题**：第一步先判断“是需要**单源**最短路还是**全源**最短路”。如果是单源且边权非负，立刻想到 **Dijkstra + 堆**；如果是全源且 `n` 很小，考虑 **Floyd‑Warshall**。  

祝你玩转图算法，玩得开心 🎉