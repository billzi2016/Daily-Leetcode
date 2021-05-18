# #1334. 找阈值距离下邻居最少的城市 / Find the City With the Smallest Number of Neighbors at a Threshold Distance

> 难度：中等 · 标签：Dynamic Programming、Graph、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)

---

## 题目（英文原版）

**Description**

There are n cities numbered from 0 to n-1. Given the array edges where edges[i] = [fromi, toi, weighti] represents a bidirectional and weighted edge between cities fromi and toi, and given the integer distanceThreshold.
Return the city with the smallest number of cities that are reachable through some path and whose distance is at most distanceThreshold, If there are multiple such cities, return the city with the greatest number.
Notice that the distance of a path connecting cities i and j is equal to the sum of the edges' weights along that path.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
Output: 3
Explanation: The figure above describes the graph. 
The neighboring cities at a distanceThreshold = 4 for each city are:
City 0 -> [City 1, City 2] 
City 1 -> [City 0, City 2, City 3] 
City 2 -> [City 0, City 1, City 3] 
City 3 -> [City 1, City 2] 
Cities 0 and 3 have 2 neighboring cities at a distanceThreshold = 4, but we have to return city 3 since it has the greatest number.
```

**Example 2:**

```
Input: n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
Output: 0
Explanation: The figure above describes the graph. 
The neighboring cities at a distanceThreshold = 2 for each city are:
City 0 -> [City 1] 
City 1 -> [City 0, City 4] 
City 2 -> [City 3, City 4] 
City 3 -> [City 2, City 4]
City 4 -> [City 1, City 2, City 3] 
The city 0 has 1 neighboring city at a distanceThreshold = 2.
```

**Constraints**

- 2 <= n <= 100
- 1 <= edges.length <= n * (n - 1) / 2
- edges[i].length == 3
- 0 <= fromi < toi < n
- 1 <= weighti, distanceThreshold <= 10^4
- All pairs (fromi, toi) are distinct.

---

## 题目（中文翻译）

有 `n` 个城市，编号为 `0` 到 `n‑1`。给定数组 `edges`，其中 `edges[i] = [from_i, to_i, weight_i]` 表示城市 `from_i` 与城市 `to_i` 之间的一条**双向加权边**（bidirectional and weighted edge），以及整数 `distanceThreshold`。  

返回在 **阈值距离**（distance threshold）`distanceThreshold` 之内可以通过某条路径到达的城市数量最少的城市编号。如果有多个城市满足该条件，返回编号最大的城市。  

注意，连接城市 `i` 与城市 `j` 的路径的距离等于该路径上所有边的权重之和。

**示例 1**

```text
Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
Output: 3
Explanation: 如上图所示的无向图。  
在 `distanceThreshold = 4` 时，每个城市的可达邻居如下：
- 城市 0 → [城市 1, 城市 2]  
- 城市 1 → [城市 0, 城市 2, 城市 3]  
- 城市 2 → [城市 0, 城市 1, 城市 3]  
- 城市 3 → [城市 1, 城市 2]  

城市 0 和城市 3 各有 2 个邻居，满足最少邻居数；其中编号更大的城市 3 被返回。
```

**示例 2**

```text
Input: n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
Output: 0
Explanation: 如上图所示的无向图。  
在 `distanceThreshold = 2` 时，每个城市的可达邻居如下：
- 城市 0 → [城市 1]  
- 城市 1 → [城市 0, 城市 4]  
- 城市 2 → [城市 3, 城市 4]  
- 城市 3 → [城市 2, 城市 4]  
- 城市 4 → [城市 1, 城市 2, 城市 3]  

城市 0 只有 1 个邻居，是所有城市中邻居数量最少的，故返回 0。
```

**约束条件**

- `2 <= n <= 100`
- `1 <= edges.length <= n * (n - 1) / 2`
- `edges[i].length == 3`
- `0 <= from_i < to_i < n`
- `1 <= weight_i, distanceThreshold <= 10^4`
- 所有 `(from_i, to_i)` 对均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每座城市，都跑一次最短路算法，算出它到其它所有城市的最短距离**。  
- 我们先把 `edges` 组织成 **邻接表**（adjacency list），它就像一本“城市通讯录”，  
  - **键（key）** 是城市编号，  
  - **值（value）** 是该城市直接相连的邻居以及对应的路程。  
  - 这类似于查字典时，先找到词条（城市），再看到它的解释（相连的城市和权重）。  
- 对每个起点城市，使用 **Dijkstra**（单源最短路）遍历整个图，得到从起点到所有城市的最短距离。  
- 再把这些距离和 `distanceThreshold` 对比，统计 **可达的城市数目**（不算自己）。  
- 最后遍历所有城市，挑出 **可达城市最少的那座**；若出现平局，返回编号更大的城市。

> **为什么它一定对？**  
> Dijkstra 能在权重非负的图里找到从起点到所有点的最短路径。因为题目保证所有 `weighti ≥ 1`，所以使用 Dijkstra 完全符合题意。遍历所有起点后，就能得到每对城市之间的最短距离，从而准确判断是否 ≤ `distanceThreshold`。

#### 代码（Python）

```python
import heapq
from typing import List

def findTheCity(n: int, edges: List[List[int]], distanceThreshold: int) -> int:
    # ---------- 建立邻接表 ----------
    # 类比：city_dict[0] = [(1, 3), (2, 5)] 表示 0 城市直接连到 1（距离 3）和 2（距离 5）
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))          # 因为是双向道路

    # ---------- Dijkstra 单源最短路 ----------
    def dijkstra(src: int) -> List[int]:
        INF = 10**9
        dist = [INF] * n
        dist[src] = 0
        heap = [(0, src)]               # (当前累计距离, 城市编号)

        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:            # 已经有更小的距离了，跳过
                continue
            for v, w in adj[u]:
                nd = d + w               # 经过 u 再到 v 的新距离
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        return dist

    # ---------- 统计每座城市的可达邻居数 ----------
    best_city = -1
    best_cnt = n + 1                     # 初始化为一个不可能的最大值

    for city in range(n):
        dists = dijkstra(city)           # 该城市到所有城市的最短距离
        # 可达且不算自己
        cnt = sum(1 for d in dists if d <= distanceThreshold and d != 0)

        # 若当前城市的可达数更少，或相同但编号更大，就更新答案
        if cnt < best_cnt or (cnt == best_cnt and city > best_city):
            best_cnt = cnt
            best_city = city

    return best_city
```

#### 复杂度  

- **时间复杂度**：`O(n * (E log V))`  
  - 对每个城市都跑一次 Dijkstra，`E` 是边数，`V = n`。  
  - `log V` 来自优先队列的操作。  
  - 直观上可以想象：如果有 100 座城市、400 条路，跑 100 次 Dijkstra，大概是 “100 × 400 × log 100” 次基本操作。  

- **空间复杂度**：`O(V + E)`  
  - 邻接表需要存所有城市和道路信息。  
  - 每次 Dijkstra 里还会开一个 `dist` 数组（长度 n）和一个堆，最多同时占用 `O(V)` 的额外空间。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈在于重复计算**：  
- 对每个起点都要跑一次 Dijkstra，虽然每次都得到完整的最短路径表，但实际上我们只需要 **所有城市两两之间的最短距离** 一次即可。  

**核心技巧：** 使用 **Floyd‑Warshall**（全源最短路）一次性算出 `dist[i][j]`，即任意两座城市的最短距离。  

- Floyd‑Warshall 的思想非常直观：  
  1. 先把直接相连的距离放进矩阵 `dist`，其余位置设为“无穷大”。  
  2. 然后逐个尝试把第 `k` 座城市当作 **中转站**，看能否把 `i → j` 的路径变得更短。  
  3. 公式：`dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`。  
- 这就像在做 **“三人帮”** 的传话游戏：先让两个人直接交流（直接边），再让第三个人加入，看能否让信息传递得更快。  

**为什么它更好？**  
- 只需要 **三层循环**，每层最多 `n`（≤ 100）次，总共 `n³` 次基本比较。  
- 对于 `n = 100`，`100³ = 1,000,000`，在电脑里几毫秒就能跑完，远快于 100 次 Dijkstra（每次都要维护堆）。  
- 代码也更简洁，后面只需一次遍历统计可达城市数。

#### 代码（Python）

```python
from typing import List

def findTheCity(n: int, edges: List[List[int]], distanceThreshold: int) -> int:
    INF = 10**9

    # ---------- 1. 初始化距离矩阵 ----------
    # dist[i][j] 表示 i 到 j 的当前已知最短距离，初始时只有直接相连的边是已知的
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0               # 同一个城市到自己距离是 0

    for u, v, w in edges:
        dist[u][v] = w
        dist[v][u] = w               # 双向道路

    # ---------- 2. Floyd‑Warshall：尝试每个城市作为中转站 ----------
    for k in range(n):               # 中转站 k
        for i in range(n):           # 起点 i
            # 如果 i → k 已经不可达，就没有必要继续
            if dist[i][k] == INF:
                continue
            for j in range(n):       # 终点 j
                # 同理，k → j 不可达也跳过
                if dist[k][j] == INF:
                    continue
                # 看看经由 k 的路径是否更短
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # ---------- 3. 统计每座城市的可达邻居数 ----------
    best_city = -1
    best_cnt = n + 1                 # 初始化为不可能的大数

    for i in range(n):
        # 统计距离 ≤ distanceThreshold 且不是自己本身的城市数
        cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)

        # 若当前城市可达数更少，或相同但编号更大，更新答案
        if cnt < best_cnt or (cnt == best_cnt and i > best_city):
            best_cnt = cnt
            best_city = i

    return best_city
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 三层循环各遍历 `n` 次。  
  - 对于 `n = 100`，大约是一百万次比较，几乎可以忽略不计。  
  - 与暴力解的 `O(n * (E log V))` 相比，省去了重复的堆操作，整体更快。

- **空间复杂度**：`O(n²)`  
  - 需要存储 `n × n` 的距离矩阵。  
  - 对于 `n = 100`，矩阵大小仅 10,000 个整数，内存占用极小。

---

## 心得  

- **核心技巧**：**Floyd‑Warshall 全源最短路**。它一次性算出所有城市对之间的最短距离，随后只需 O(n) 的遍历即可得到答案。  
- **适用的题型**（类似思路）：  
  1. “找出图中距离最短的两点” – 需要任意两点最短路径时。  
  2. “判断图中是否存在负环” – Floyd‑Warshall 同时可以检测 `dist[i][i] < 0`。  
  3. “所有城市的最短运输成本” – 多源多汇的最小成本问题。  
- **解题钥匙**：**把“每次都重新算”换成“一次算完所有”。**  

---

## 反思  

- **第一反应**：看到“每座城市的可达城市数”，立刻想到“对每个城市跑一次最短路”。这是一种直观但重复的做法。  
- **最容易踩的坑**：  
  - **边界条件**：城市本身不算在可达邻居里，需要排除 `i == j`。  
  - **阈值比较**：距离恰好等于 `distanceThreshold` 仍然算作可达。  
  - **平局处理**：题目要求“若有多个，返回编号最大的”，一定要在比较时加入 `city > best_city` 的条件。  
- **下次遇到同类题**：第一步先思考 **“是否真的需要对每个起点单独跑算法？”**  
  - 若 **n** 较小（如 ≤ 100），尝试 **Floyd‑Warshall**；  
  - 若 **n** 很大但图稀疏，则考虑 **从每个点跑 Dijkstra**（或多源 Dijkstra + 优化）。