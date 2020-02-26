# #787. K 次中转以内的最便宜航班 / Cheapest Flights Within K Stops

> 难度：中等 · 标签：Dynamic Programming、Depth-First Search、Breadth-First Search、Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

---

## 题目（英文原版）

**Description**

There are n cities connected by some number of flights. You are given an array flights where flights[i] = [fromi, toi, pricei] indicates that there is a flight from city fromi to city toi with cost pricei.
You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.

**Examples**

**Example 1:**

```
Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
Output: 700
Explanation:
The graph is shown above.
The optimal path with at most 1 stop from city 0 to 3 is marked in red and has cost 100 + 600 = 700.
Note that the path through cities [0,1,2,3] is cheaper but is invalid because it uses 2 stops.
```

**Example 2:**

```
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
Output: 200
Explanation:
The graph is shown above.
The optimal path with at most 1 stop from city 0 to 2 is marked in red and has cost 100 + 100 = 200.
```

**Example 3:**

```
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
Output: 500
Explanation:
The graph is shown above.
The optimal path with no stops from city 0 to 2 is marked in red and has cost 500.
```

**Constraints**

- 1 <= n <= 100
- 0 <= flights.length <= (n * (n - 1) / 2)
- flights[i].length == 3
- 0 <= fromi, toi < n
- fromi != toi
- 1 <= pricei <= 104
- There will not be any multiple flights between two cities.
- 0 <= src, dst, k < n
- src != dst

---

## 题目（中文翻译）

给定 **n** 个城市，它们之间通过若干航班相连。你会得到一个数组 **flights**，其中 `flights[i] = [from_i, to_i, price_i]` 表示存在一条从城市 `from_i` 到城市 `to_i` 的航班，票价为 `price_i`。

同时给定三个整数 **src**、**dst** 和 **k**，返回从 **src** 到 **dst** 的最小花费，且该路线至多经过 **k** 次中转（即最多 **k** 条边）。如果不存在满足条件的路线，返回 **-1**。

---

### 示例

#### 示例 1
> **输入**  
> `n = 4`  
> `flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`  
> `src = 0, dst = 3, k = 1`  
> **输出** `700`  
> **解释**：  
> 如图所示，满足至多 1 次中转的最优路径为 `0 → 1 → 3`（红色标记），费用为 `100 + 600 = 700`。  
> 注意，路径 `0 → 1 → 2 → 3` 虽然更便宜，但使用了 2 次中转，超出限制。

#### 示例 2
> **输入**  
> `n = 3`  
> `flights = [[0,1,100],[1,2,100],[0,2,500]]`  
> `src = 0, dst = 2, k = 1`  
> **输出** `200`  
> **解释**：  
> 如图所示，满足至多 1 次中转的最优路径为 `0 → 1 → 2`（红色标记），费用为 `100 + 100 = 200`。

#### 示例 3
> **输入**  
> `n = 3`  
> `flights = [[0,1,100],[1,2,100],[0,2,500]]`  
> `src = 0, dst = 2, k = 0`  
> **输出** `500`  
> **解释**：  
> 如图所示，**不允许任何中转** 时的唯一可行路径是直接航班 `0 → 2`（红色标记），费用为 `500`。

---

### 约束条件

- `1 <= n <= 100`
- `0 <= flights.length <= n * (n - 1) / 2`
- `flights[i].length == 3`
- `0 <= from_i, to_i < n`
- `from_i != to_i`
- `1 <= price_i <= 10^4`
- 任意两座城市之间至多只有一条航班
- `0 <= src, dst, k < n`
- `src != dst`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有**可能的航线**都枚举出来，只保留满足「至多 `k` 次中转」的路径，最后在这些合法路径中挑最小的花费。

- **数据结构**  
  - **邻接表**：把 `flights` 转成「每个城市 → 可以直接飞往的城市 + 票价」的字典。可以把它想象成一本「城市航线手册」，查某个城市的下一站就像在手册里翻页。  
  - **深度优先搜索（DFS）**：从起点 `src` 进行一次「走迷宫」式的递归搜索，每走一步就记录已经花了多少钱和已经经过了几次中转。  
  - **路径剪枝**：如果当前已经走的中转次数大于 `k`，或者花费已经比目前已知的最小花费更大，就立刻停止这条搜索分支（相当于在迷宫里发现走不通的死胡同就不再往里走了）。

- **为什么正确**  
  只要把所有长度 ≤ `k+1`（因为 `k` 次中转意味着最多 `k+1` 条航班）的路径全部遍历一遍，就一定能找到最便宜的那条。我们在遍历的过程中记录最小费用，遍历结束后得到的就是答案。

- **时间/空间复杂度**  
  - **时间复杂度**：最坏情况下，城市之间几乎是全连通的，DFS 会尝试所有可能的路径。每一步可以有至多 `n-1` 条可选航班，最多走 `k+1` 步，时间复杂度约为 `O((n-1)^{k+1})`，即指数级增长。可以把它想成「每次都有 `n-1` 种选择，选 `k+1` 次」的全部组合数。  
  - **空间复杂度**：递归栈的深度最多是 `k+1`，加上邻接表需要 `O(n + E)`（`E` 为航班数），整体是 `O(n + E + k)`。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def findCheapestPrice_bruteforce(n: int, flights: List[List[int]],
                                 src: int, dst: int, k: int) -> int:
    # 1. 建立邻接表：city -> [(next_city, price), ...]
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    best = float('inf')               # 记录目前找到的最小费用

    def dfs(cur: int, stops: int, cost: int):
        """从 cur 出发，已使用 stops 次中转，累计花费 cost"""
        nonlocal best
        # 剪枝：已超出中转次数或已经比 best 更贵
        if stops > k or cost >= best:
            return
        # 到达目的地，更新 best
        if cur == dst:
            best = min(best, cost)
            return
        # 继续向下搜索
        for nxt, price in graph[cur]:
            dfs(nxt, stops + 1, cost + price)

    dfs(src, -1, 0)   # 第一次出发不算一次中转，所以从 -1 开始计数
    return -1 if best == float('inf') else best
```

#### 复杂度

- **时间复杂度**：`O((n-1)^{k+1})` —— 每一步都有 `n-1` 种选择，最多走 `k+1` 步，类似指数级的「全枚举」。
- **空间复杂度**：`O(n + E + k)` —— 邻接表占 `O(n + E)`，递归栈深度最多 `k+1`，加上一点常数额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复遍历**相同的子路径：比如从城市 `A` 到 `B` 的最小花费在不同的搜索分支里会被重新计算很多次。我们需要一种「记忆」或「一次遍历多次使用」的技巧。

这道题恰好符合**「最短路径」**的模型，只是额外加了「最多 `k` 次中转」的限制。常见的解决思路有两种：

1. **Bellman‑Ford 动态规划**（本题最常用）  
   - 设 `dp[t][i]` 为「恰好经过 `t` 条航班（即 `t-1` 次中转）到达城市 `i` 的最小费用」。
   - 初始时 `dp[0][src] = 0`，其余为 `∞`。  
   - 对每一次「航班数」`t = 1 … k+1`，遍历所有航班 `(u, v, w)`，尝试用 `t-1` 条航班到达 `u` 再乘坐这条航班到 `v`，更新 `dp[t][v]`。  
   - 最终答案是 `min(dp[t][dst])`（`t = 1 … k+1`）中的最小值。  
   - 这里的「记忆」体现在 `dp` 表里，**每条航班只会被考虑 `k+1` 次**，避免指数级爆炸。

2. **带停次数的 Dijkstra（最小堆）**  
   - 传统 Dijkstra 只管「距离最短」而不管「经过多少条边」，这里我们把「已使用的中转次数」也放进堆的状态。  
   - 每弹出一个 `(cost, city, stops)`，如果 `city == dst` 且 `stops <= k`，直接返回 `cost`（因为堆是按费用升序弹出的，第一个满足条件的就是最小费用）。  
   - 对每个邻居 `next`，只要 `stops < k` 就把 `(cost + price, next, stops + 1)` 放入堆。  
   - 为了防止同一个城市被无意义地重复入堆，我们可以维护一个「到达该城市时的最少停次数」的记录，只在更优的（费用更低或停次数更少）情况下才入堆。

下面给出两种实现，读者可以任选其一。两者时间复杂度都是 **`O(k * E)`**（`E` 为航班数），空间复杂度 **`O(n + E)`**，远快于暴力枚举。

---

#### 代码（Python）—— Bellman‑Ford 动态规划

```python
from typing import List
import math

def findCheapestPrice_bellman_ford(n: int, flights: List[List[int]],
                                   src: int, dst: int, k: int) -> int:
    # dp[i] 表示「经过最多 i 条航班」到每个城市的最小费用
    # 只保留上一轮的结果，空间可以压缩到 O(n)
    INF = math.inf
    dp = [INF] * n
    dp[src] = 0                     # 0 条航班到达 src 的费用是 0

    # 我们最多可以使用 k+1 条航班（k 次中转），所以循环 k+1 次
    for i in range(k + 1):
        # 复制上一轮的结果，防止本轮更新影响同一轮的其他航班
        cur = dp[:]
        for u, v, w in flights:
            if dp[u] == INF:       # 之前不可达则跳过
                continue
            # 通过航班 (u->v) 用一条额外的航班到达 v
            if dp[u] + w < cur[v]:
                cur[v] = dp[u] + w
        dp = cur                    # 完成第 i 条航班的松弛

    return -1 if dp[dst] == INF else dp[dst]
```

#### 代码（Python）—— 带停次数的 Dijkstra（最小堆）

```python
import heapq
from collections import defaultdict
from typing import List

def findCheapestPrice_dijkstra(n: int, flights: List[List[int]],
                               src: int, dst: int, k: int) -> int:
    # 1. 建图（邻接表）
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    # 2. 最小堆，元素为 (累计费用, 当前城市, 已使用的中转次数)
    heap = [(0, src, 0)]
    # 记录到达每个城市时最少的中转次数，帮助剪枝
    best_stop = [math.inf] * n
    best_stop[src] = 0

    while heap:
        cost, city, stops = heapq.heappop(heap)
        # 目的地且停次数符合要求，直接返回
        if city == dst:
            return cost
        # 已经用了 k 次中转，不能再往后走
        if stops > k:
            continue
        # 遍历所有可达的下一站
        for nxt, price in graph[city]:
            new_cost = cost + price
            # 只在「费用更低」或「同等费用但停次数更少」时入堆
            if stops + 1 < best_stop[nxt]:
                best_stop[nxt] = stops + 1
                heapq.heappush(heap, (new_cost, nxt, stops + 1))
    return -1
```

#### 复杂度

- **时间复杂度**  
  - Bellman‑Ford：`O((k+1) * E)` —— 每轮遍历所有航班 `E`，共 `k+1` 轮。相当于「最多走 `k+1` 条边」的所有可能组合，只遍历一次。  
  - Dijkstra（堆）同样是 `O((k+1) * E log V)`，其中 `log V` 来自堆的插入/弹出。因为每条边最多被放入堆 `k+1` 次，整体仍然线性可接受。  
  与暴力 `O((n-1)^{k+1})` 相比，**指数下降到线性**，在 `n ≤ 100`、`k ≤ 99` 的范围内毫无压力。

- **空间复杂度**  
  - 两种实现都需要保存图 `O(V + E)`，以及 DP 表或堆/访问记录 `O(V)`，整体 `O(V + E)`。  
  - 这比暴力的递归栈 `O(k)` 更小，且不随路径数量爆炸。

---

## 心得

- **核心技巧**：**在最短路径问题上加入「边数上限」的约束**。常用的做法是 **Bellman‑Ford 的层数限制**（相当于 DP 的「最多使用 `k+1` 条边」）或 **带停次数的 Dijkstra**（把「已使用的中转次数」放进堆的状态）。
- **适用的题型**  
  1. “在最多 `K` 条边/步骤内求最短路” —— 如 LeetCode 787（本题）  
  2. “限制步数的最小费用/最小时间” —— 如 LeetCode 1697（检查子数组是否满足条件）中的「最少步数」思路  
  3. “带有层数限制的图遍历” —— 如 LeetCode 1039（K 距离内的最小值）  
- **一句话总结解题钥匙**：**把「最多 K 次中转」转化为「最多使用 K+1 条边」的层次 DP，或者把「停次数」当作额外维度放进最小堆**。

---

## 反思

- **第一反应**：看到「最多 K 次中转」立即想到 BFS（层序遍历）或 DFS 枚举所有路径。  
- **最容易踩的坑**  
  - **把中转次数和航班条数弄混**：`k` 次中转对应 **最多 `k+1` 条航班**，容易少算或多算一步。  
  - **忘记对起点的特殊处理**：在 BFS/DFS 中起点不算一次中转，递归时需要从 `-1` 开始计数或在第一次出发不增加 `stops`。  
  - **剪枝不严谨导致错误**：比如只用「费用更低」剪枝而不考虑「停次数」时，可能会把更贵但停次数更少的路径错过，从而在后续无法满足 `k` 限制。  
- **下次遇到同类题**：**第一步**先判断是否可以用「层数限制的 DP」或「带额外维度的最小堆」来把「限制次数」纳入状态，而不是直接暴力枚举所有路径。这样思路更清晰，代码也更容易写对。