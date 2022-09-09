# #1928. 最小费用在限定时间内到达目的地 / Minimum Cost to Reach Destination in Time

> 难度：困难 · 标签：Array、Dynamic Programming、Graph · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-reach-destination-in-time/)

---

## 题目（英文原版）

**Description**

There is a country of n cities numbered from 0 to n - 1 where all the cities are connected by bi-directional roads. The roads are represented as a 2D integer array edges where edges[i] = [xi, yi, timei] denotes a road between cities xi and yi that takes timei minutes to travel. There may be multiple roads of differing travel times connecting the same two cities, but no road connects a city to itself.
Each time you pass through a city, you must pay a passing fee. This is represented as a 0-indexed integer array passingFees of length n where passingFees[j] is the amount of dollars you must pay when you pass through city j.
In the beginning, you are at city 0 and want to reach city n - 1 in maxTime minutes or less. The cost of your journey is the summation of passing fees for each city that you passed through at some moment of your journey (including the source and destination cities).
Given maxTime, edges, and passingFees, return the minimum cost to complete your journey, or -1 if you cannot complete it within maxTime minutes.

**Examples**

**Example 1:**

```
Input: maxTime = 30, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]
Output: 11
Explanation: The path to take is 0 -> 1 -> 2 -> 5, which takes 30 minutes and has $11 worth of passing fees.
```

**Example 2:**

```
Input: maxTime = 29, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]
Output: 48
Explanation: The path to take is 0 -> 3 -> 4 -> 5, which takes 26 minutes and has $48 worth of passing fees.
You cannot take path 0 -> 1 -> 2 -> 5 since it would take too long.
```

**Example 3:**

```
Input: maxTime = 25, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]
Output: -1
Explanation: There is no way to reach city 5 from city 0 within 25 minutes.
```

**Constraints**

- 1 <= maxTime <= 1000
- n == passingFees.length
- 2 <= n <= 1000
- n - 1 <= edges.length <= 1000
- 0 <= xi, yi <= n - 1
- 1 <= timei <= 1000
- 1 <= passingFees[j] <= 1000
- The graph may contain multiple edges between two nodes.
- The graph does not contain self loops.

---

## 题目（中文翻译）

**描述**  
一个由 `n` 座城市（编号为 `0` 到 `n - 1`）组成的国家，所有城市之间通过双向道路（bi-directional roads）相连。道路由二维整数数组 `edges` 表示，其中 `edges[i] = [xi, yi, timei]` 表示城市 `xi` 与城市 `yi` 之间有一条道路，行驶该道路需要 `timei` 分钟。可能存在多条不同通行时间的道路连接同一对城市，但不存在连接自身的道路。  

每次经过一座城市，都必须支付通行费（passing fee）。通行费由长度为 `n` 的 0 索引整数数组 `passingFees` 给出，`passingFees[j]` 为经过城市 `j` 时需要支付的美元数。  

起点为城市 `0`，目标是 **在不超过 `maxTime` 分钟** 内到达城市 `n - 1`。旅程的费用为旅途中所有经过的城市（包括起点和终点）的通行费之和。  

给定 `maxTime`、`edges` 与 `passingFees`，返回完成旅程的 **最小费用**；若无法在 `maxTime` 分钟内到达，则返回 `-1`。  

**示例**  

**示例 1**  
```text
Input: maxTime = 30, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]
Output: 11
Explanation: 选择路径 0 -> 1 -> 2 -> 5，耗时 30 分钟，总通行费为 $11。
```

**示例 2**  
```text
Input: maxTime = 29, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]
Output: 48
Explanation: 选择路径 0 -> 3 -> 4 -> 5，耗时 26 分钟，总通行费为 $48。路径 0 -> 1 -> 2 -> 5 超时，不能选择。
```

**示例 3**  
```text
Input: maxTime = 25, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]
Output: -1
Explanation: 在 25 分钟内无法从城市 0 到达城市 5。
```

**约束条件**  

- `1 <= maxTime <= 1000`  
- `n == passingFees.length`  
- `2 <= n <= 1000`  
- `n - 1 <= edges.length <= 1000`  
- `0 <= xi, yi <= n - 1`  
- `1 <= timei <= 1000`  
- `1 <= passingFees[j] <= 1000`  
- 图中可能存在多条连接同一对节点的边。  
- 图中不包含自环。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的路线都枚举一遍，只要路线的总耗时 `≤ maxTime`，就算出它的通行费总和，最后取最小值。  

- **枚举方式**：可以用深度优先搜索（DFS）从城市 `0` 出发，沿着每条道路递归走下去。  
- **数据结构类比**：  
  - **递归调用栈** 就像我们在现实中走路时的“脚印”，每走一步就往栈里压一个城市，回溯时再弹出。  
  - **`visited` 数组** 类似于旅行手册里的“已经去过的城市”，防止在同一次搜索路径中无限循环（因为图是无向的，若不限制会在两条相反的路上来回走）。  
- **正确性**：只要把 **所有** 能在规定时间内到达终点的路径都遍历一遍，最小的费用一定会被记录下来。  

> 这里的“暴力”指的是**穷举**，不考虑任何剪枝或优化，时间复杂度会非常高。

#### 代码（Python）

```python
from typing import List

def minCost_bruteforce(maxTime: int,
                       edges: List[List[int]],
                       passingFees: List[int]) -> int:
    n = len(passingFees)

    # 把无向图转成邻接表，方便遍历
    graph = [[] for _ in range(n)]
    for u, v, t in edges:
        graph[u].append((v, t))   # (相邻城市, 所需时间)
        graph[v].append((u, t))

    best = float('inf')          # 记录全局最小费用

    def dfs(cur: int, spent_time: int, spent_fee: int, visited: List[bool]):
        nonlocal best
        # 剪枝：已经超过时间上限，直接返回
        if spent_time > maxTime:
            return
        # 剪枝：已经找到更好的解，直接返回
        if spent_fee >= best:
            return
        # 到达目的地
        if cur == n - 1:
            best = min(best, spent_fee)
            return

        # 继续向相邻城市探索
        for nxt, t in graph[cur]:
            if not visited[nxt]:          # 防止在同一路径里原地回环
                visited[nxt] = True
                dfs(nxt,
                    spent_time + t,
                    spent_fee + passingFees[nxt],
                    visited)
                visited[nxt] = False        # 回溯

    # 初始状态：在城市 0，已经支付了 passingFees[0]
    visited = [False] * n
    visited[0] = True
    dfs(0, 0, passingFees[0], visited)

    return -1 if best == float('inf') else best
```

> 关键行解释（中文注释已写在代码里）  
> - `if spent_time > maxTime: return` → 超时直接剪枝。  
> - `if spent_fee >= best: return` → 已经不可能更优，提前结束。  
> - `visited[nxt] = True/False` → 记录/撤销本次路径的访问状态，实现回溯。

#### 复杂度  

- **时间复杂度**：`O( branching_factor ^ depth )`，在最坏情况下相当于 **指数级**。  
  - `branching_factor`≈每个城市的平均出度，`depth`≈在 `maxTime` 限制下最多能走的边数。  
  - 用大白话说，就是“走到最后可能要尝试几千、几万、甚至更多种不同的路线”，根本不可能在 1 秒内跑完。  
- **空间复杂度**：`O(n)`，递归栈最多保存 `n` 个城市的状态（因为我们用 `visited` 防止在同一路径里重复访问）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **重复遍历** 同一个状态：  
- 同一个城市在相同或更少的已用时间下，可能会被多次搜索。  
- 每条边都会被尝试很多次，导致指数级爆炸。

**优化方向**：把 “城市 + 已用时间” 视为**一个状态**，只要我们已经找到了到达该状态的最小费用，就不必再用更贵的费用去重复探索。  

这正好对应 **最短路**（Shortest Path）问题，只是我们要在 **费用**（cost）上最小化，同时对 **时间**（time）有上限约束。  

一种常见做法是 **在原图上做动态规划 + Dijkstra（或 BFS）**：

1. **状态定义**  
   - `dp[node][t]` = 在恰好用了 `t` 分钟到达 `node` 时的最小费用。  
   - `t` 的取值范围是 `0 … maxTime`（题目保证 `maxTime ≤ 1000`），因此状态空间大小为 `n * (maxTime+1)`，最多约 `10⁶`，可以接受。

2. **状态转移**  
   - 对于任意一条无向边 `(u, v, w)`（`w` 为该路段耗时），如果我们已经在 `t` 分钟时到达 `u`，则可以在 `t + w` 分钟时到达 `v`，费用会增加 `passingFees[v]`。  
   - 公式：  
     ```
     if t + w <= maxTime:
         dp[v][t + w] = min(dp[v][t + w], dp[u][t] + passingFees[v])
     ```
   - 同理也可以从 `v` 到 `u`。

3. **遍历顺序**  
   - 由于转移只会把时间 **增大**（`t + w`），我们可以按时间从小到大遍历（类似动态规划的“时间层”），或者使用 **优先队列**（最小费用优先）来实现 Dijkstra。这里演示使用 **优先队列**，因为它可以在发现更好路径时立即更新，避免遍历所有时间层。

4. **终止条件**  
   - 当弹出状态 `(node, time, cost)` 且 `node == n-1` 时，说明已经找到一条到达终点的路径，且是费用最小的（因为队列是按费用升序弹出的），直接返回 `cost`。  
   - 如果队列耗尽仍未到达终点，则返回 `-1`。

5. **剪枝**  
   - 对每个 `(node, time)` 只保留 **当前已知的最小费用**，如果再次得到更大的费用则直接丢弃。  
   - 这相当于在 `dp` 表里做记忆化，防止无限扩展。

**类比**：把“城市在某个时间点”想象成一座**时空城堡**，每座城堡都有自己的门票（费用）。我们要在费用最少的前提下，使用不超过 `maxTime` 的钥匙（时间）打开这些城堡，最终走到终点城堡。优先队列就像“最便宜的钥匙先用”，保证先尝试最省钱的路线。

#### 代码（Python）

```python
import heapq
from typing import List

def minCost(maxTime: int,
           edges: List[List[int]],
           passingFees: List[int]) -> int:
    n = len(passingFees)

    # 1️⃣ 建图：邻接表，存 (邻居, 所需时间)
    graph = [[] for _ in range(n)]
    for u, v, t in edges:
        graph[u].append((v, t))
        graph[v].append((u, t))

    # 2️⃣ dp[node][time] = 到达该状态的最小费用，初始化为无穷大
    INF = 10 ** 18
    dp = [[INF] * (maxTime + 1) for _ in range(n)]
    dp[0][0] = passingFees[0]               # 起点费用

    # 3️⃣ 优先队列，元素为 (已花费用, 已用时间, 当前城市)
    #    费用最小的状态会最先被弹出
    heap = [(passingFees[0], 0, 0)]

    while heap:
        cost, cur_time, u = heapq.heappop(heap)

        # 如果已经是终点，直接返回（因为这是费用最小的）
        if u == n - 1:
            return cost

        # 若当前状态已经被更好的费用更新，则跳过
        if cost != dp[u][cur_time]:
            continue

        # 4️⃣ 遍历所有相邻道路，尝试前往下一个城市
        for v, w in graph[u]:
            nxt_time = cur_time + w
            if nxt_time > maxTime:          # 超时直接丢弃
                continue
            nxt_cost = cost + passingFees[v]
            # 若发现更小费用，就更新 dp 并压入堆
            if nxt_cost < dp[v][nxt_time]:
                dp[v][nxt_time] = nxt_cost
                heapq.heappush(heap, (nxt_cost, nxt_time, v))

    # 5️⃣ 所有可行路径都遍历完仍未到达终点
    return -1
```

> **代码要点（中文注释已写）**  
> - `dp` 表防止同一个城市在相同时间点被重复扩展。  
> - `heapq`（最小堆）保证每次处理的都是当前费用最小的状态，等价于 **Dijkstra**（但这里的“边权”是费用，而时间是额外的约束）。  
> - 当弹出终点时，直接返回即可，因为没有比它更省钱的路径了。

#### 复杂度  

- **时间复杂度**：`O(E * maxTime * log (n * maxTime))`  
  - 每条边在每个可能的时间点最多被松弛一次（因为 `dp` 只会从 `INF` 降到更小的值一次），共 `E * maxTime` 次。  
  - 每次松弛会向堆中插入一个元素，堆的大小上限是 `n * maxTime`，每次操作的代价是 `log (n * maxTime)`。  
  - 用大白话说：**最多几百万次**轻量级的“挑最便宜的路”，在本题限制（`n ≤ 1000, maxTime ≤ 1000`）下运行毫秒级。

- **空间复杂度**：`O(n * maxTime)`  
  - `dp` 表占用 `n * (maxTime+1)` 个整数，大约 `10⁶`，约几 MB，完全可以接受。  
  - 堆中最多也会有同样数量的状态。

> 与暴力解相比：  
> - **暴力**是指数级的，根本不可用。  
> - **最优解**把搜索空间压到了多项式级（`n * maxTime`），在题目限制下轻松跑完。

---

## 心得  

- **核心技巧**：把“城市+已用时间”视为**状态**，在状态空间上做最短路（Dijkstra）或 DP。  
- **适用场景**：  
  1. **带资源限制的最短路**（如“最少费用且总距离 ≤ D”）。  
  2. **时间/能量/金钱上限的路径问题**（如 LeetCode 1631、1515、1743 等）。  
  3. **多维 DP 转图**（如“带权重的背包路径”）。  
- **一句话总结解题钥匙**：**把“额外约束”（时间）加入到状态定义中，让每个状态只被处理一次**。

---

## 反思  

- **第一反应**：先写 DFS 暴力遍历，想把所有路径都列举出来。  
- **最容易踩的坑**：  
  - **时间上限**：忘记在递归/松弛时检查 `cur_time + w ≤ maxTime`，会导致无限扩展。  
  - **费用重复计数**：每次进入一个城市都要加一次 `passingFees`，包括起点和终点，别漏了。  
  - **多条平行边**：同一对城市可能有多条不同耗时的道路，需要全部加入邻接表，否则会错过更优路径。  
- **下次类似题的第一步**：先**写出状态 `(节点, 资源消耗)`，判断资源消耗的取值范围是否够小（如 ≤ 1000），如果可以，就在这个状态图上跑最短路或 DP。这样就能把“指数爆炸”直接降到可接受的多项式规模。