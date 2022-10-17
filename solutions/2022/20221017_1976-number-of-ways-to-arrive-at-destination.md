# #1976. 到达终点的路径数 / Number of Ways to Arrive at Destination

> 难度：中等 · 标签：Dynamic Programming、Graph、Topological Sort、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/)

---

## 题目（英文原版）

**Description**

You are in a city that consists of n intersections numbered from 0 to n - 1 with bi-directional roads between some intersections. The inputs are generated such that you can reach any intersection from any other intersection and that there is at most one road between any two intersections.
You are given an integer n and a 2D integer array roads where roads[i] = [ui, vi, timei] means that there is a road between intersections ui and vi that takes timei minutes to travel. You want to know in how many ways you can travel from intersection 0 to intersection n - 1 in the shortest amount of time.
Return the number of ways you can arrive at your destination in the shortest amount of time. Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 7, roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]
Output: 4
Explanation: The shortest amount of time it takes to go from intersection 0 to intersection 6 is 7 minutes.
The four ways to get there in 7 minutes are:
- 0 ➝ 6
- 0 ➝ 4 ➝ 6
- 0 ➝ 1 ➝ 2 ➝ 5 ➝ 6
- 0 ➝ 1 ➝ 3 ➝ 5 ➝ 6
```

**Example 2:**

```
Input: n = 2, roads = [[1,0,10]]
Output: 1
Explanation: There is only one way to go from intersection 0 to intersection 1, and it takes 10 minutes.
```

**Constraints**

- 1 <= n <= 200
- n - 1 <= roads.length <= n * (n - 1) / 2
- roads[i].length == 3
- 0 <= ui, vi <= n - 1
- 1 <= timei <= 109
- ui != vi
- There is at most one road connecting any two intersections.
- You can reach any intersection from any other intersection.

---

## 题目（中文翻译）

你所在的城市由 `n` 个交叉路口组成，编号为 `0` 到 `n-1`，路口之间有双向道路相连。题目保证任意两个路口之间都可达，并且任意两条路口之间至多只有一条道路。

给定整数 `n` 和一个二维整数数组 `roads`，其中 `roads[i] = [ui, vi, timei]` 表示在路口 `ui` 与路口 `vi` 之间有一条道路，行驶该道路需要 `timei` 分钟。请你计算从路口 `0` 到路口 `n-1` 的 **最短时间**（shortest amount of time）内，有多少条不同的路线可以到达。

返回在最短时间内到达目的地的路径数量。由于答案可能很大，请返回 `10^9 + 7` 取模后的结果。

## 示例

### 示例 1
**输入**  
`n = 7`  
`roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]`

**输出**  
`4`

**解释**  
从交叉路口 `0` 到交叉路口 `6` 的最短时间是 **7 分钟**。在 7 分钟内到达的四条路径如下：
- `0 ➝ 6`
- `0 ➝ 4 ➝ 6`
- `0 ➝ 1 ➝ 2 ➝ 5 ➝ 6`
- `0 ➝ 1 ➝ 3 ➝ 5 ➝ 6`

### 示例 2
**输入**  
`n = 2`  
`roads = [[1,0,10]]`

**输出**  
`1`

**解释**  
只有唯一一条路径可以从交叉路口 `0` 到达交叉路口 `1`，耗时 `10` 分钟。

## 约束条件
- `1 <= n <= 200`
- `n - 1 <= roads.length <= n * (n - 1) / 2`
- `roads[i].length == 3`
- `0 <= ui, vi <= n - 1`
- `1 <= timei <= 10^9`
- `ui != vi`
- 任意两条路口之间至多只有一条道路
- 任意路口之间均可相互到达

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的路径**，把每条路径走完后记下它的总耗时，最后挑出最短的时间并统计有多少条路径恰好等于这个时间。

- **数据结构**：  
  - 用 **邻接表**（`dict[int, List[Tuple[int, int]]]`）来存图，类似于城市的公交线路表，`key` 是出发路口，`value` 是「相邻路口 + 所需时间」的列表。  
  - 用 **递归/DFS**（深度优先搜索）把所有可能的路线一次遍历出来，就像在迷宫里把每一条可能的走法都走一遍。

- **为什么正确**：  
  - DFS 会遍历 **每一条从 0 到 n‑1 的可行路径**，所以最短时间一定会被记录下来，随后我们再数一数有多少条路径的时间等于最短时间。

- **时间/空间复杂度**：  
  - 在最坏情况下（比如完全图），从 0 到 n‑1 的路径数可能是指数级的，记作 `O(k)`，其中 `k` 可能接近 `O(2^n)`。  
  - 每条路径我们都要累加一次时间，所以总时间是 **指数级**，对于 `n ≤ 200` 完全不可接受。  
  - 空间主要是递归栈的深度，最多 `O(n)`，再加上邻接表的 `O(E)`（`E` 为道路条数）。

> **大白话**：  
> 设想你要把所有从家到学校的走法写在纸上，可能有几千、几万甚至更多，逐个检查耗时会花掉几天时间，这显然不是好办法。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10000)

def brute_force_ways(n, roads):
    # 建图：邻接表
    graph = defaultdict(list)               # key: 起点，value: [(终点, 时间), ...]
    for u, v, w in roads:
        graph[u].append((v, w))
        graph[v].append((u, w))

    min_time = float('inf')   # 当前发现的最短时间
    count    = 0              # 最短时间的路径数量

    def dfs(u, cur_time, visited):
        """从节点 u 出发，累计已经走的时间 cur_time"""
        nonlocal min_time, count
        if cur_time > min_time:          # 已经比已知最短时间更慢，剪枝
            return
        if u == n - 1:                    # 到达终点
            if cur_time < min_time:
                min_time = cur_time
                count = 1
            elif cur_time == min_time:
                count += 1
            return

        for v, w in graph[u]:
            if v not in visited:         # 防止走回头路（避免无限循环）
                visited.add(v)
                dfs(v, cur_time + w, visited)
                visited.remove(v)

    dfs(0, 0, {0})
    return count, min_time

# ------------------- 示例 -------------------
n = 7
roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],
         [3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]
print(brute_force_ways(n, roads))   # (4, 7)  ← 正确答案是 4 条最短路径，耗时 7
```

> **注意**：这段代码只用于演示「暴力思路」，在实际测评里会因为超时而失效。

#### 复杂度

- **时间复杂度**：`O(k)`，`k` 为所有 0 → n‑1 路径的数量，最坏可达指数级（`≈ O(2^n)`）。  
- **空间复杂度**：`O(n + E)`，其中 `n` 为递归栈深度，`E` 为道路数（邻接表存储）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **遍历所有路径**，而我们只关心 **最短路径的数量**。  
如果先算出从起点 `0` 到每个节点的 **最短距离**，那么只要沿着「距离递增」的边走，就一定是在走「最短路的子路径」。这时图会变成一个 **有向无环图（DAG）**，因为所有合法的「最短路边」都满足 `dist[u] + w = dist[v]`，而 `dist[v] > dist[u]`（权值 `w` 为正数），不可能出现环。

**步骤一：用 Dijkstra 求单源最短距离**  
- `dist[x]` 表示从 `0` 到 `x` 的最短时间。  
- Dijkstra 用「最小堆」挑出当前未确定的最小距离节点，时间复杂度 `O(E log V)`，对本题 `n ≤ 200` 完全够用。

**步骤二：构造只保留「最短路边」的 DAG**  
- 对每条无向道路 `(u, v, w)`，检查  
  - 如果 `dist[u] + w == dist[v]`，则在 DAG 中加入有向边 `u → v`。  
  - 如果 `dist[v] + w == dist[u]`，则加入 `v → u`。  
- 这一步把原来的双向图「剪枝」成只包含「在最短路上可能出现的方向」的有向图。

**步骤三：在 DAG 上做 DP 计数**  
- 设 `ways[x]` 为从 `0` 到 `x` 的最短路径数。显然 `ways[0] = 1`（起点只有一种到达方式）。  
- 按 **拓扑顺序**（即 `dist` 从小到大）遍历节点，对于每条有向边 `u → v`：  
  ```
  ways[v] = (ways[v] + ways[u]) % MOD
  ```
- 这里的拓扑顺序可以直接用已经得到的 `dist` 排序，因为所有合法边都指向更大的 `dist`。

**为什么正确**  
- 所有「合法」的边都是「最短路上」的下一步，任何从 `0` 到 `v` 的最短路径必然是「某条最短路径到 `u`」再加上 `u → v`。  
- DP 按距离递增的顺序累加，保证在计算 `ways[v]` 时，`ways[u]` 已经是完整的最短路径计数。  
- 因为 DAG 没有环，计数过程不会出现重复计数或无限循环。

**类比**  
- 想象城市的所有路口被标上「离家最近的时间」的高度，所有只能往更高的高度走的路段就像是“只能往上爬的楼梯”。我们只需要统计从底层（0）爬到顶层（n‑1）的不同爬法，有多少种爬法就等于答案。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

MOD = 10**9 + 7

def count_shortest_ways(n: int, roads):
    """
    返回从 0 到 n-1 的最短时间路径数（模 1e9+7）
    """
    # ---------- 1. 建图（无向） ----------
    graph = defaultdict(list)          # key: 节点，value: [(相邻节点, 时间), ...]
    for u, v, w in roads:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # ---------- 2. Dijkstra 求最短距离 ----------
    INF = float('inf')
    dist = [INF] * n
    dist[0] = 0
    heap = [(0, 0)]                     # (当前距离, 节点)
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:                # 已经有更小的距离更新过，跳过
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    # ---------- 3. 构造 DAG（只保留最短路边） ----------
    dag = defaultdict(list)            # 有向图：u -> v
    for u, v, w in roads:
        if dist[u] + w == dist[v]:     # u 在前，v 在后
            dag[u].append(v)
        if dist[v] + w == dist[u]:     # v 在前，u 在后
            dag[v].append(u)

    # ---------- 4. DP 计数（按 dist 从小到大拓扑） ----------
    order = sorted(range(n), key=lambda x: dist[x])   # dist 已经是拓扑序
    ways = [0] * n
    ways[0] = 1                         # 起点只有一种到达方式

    for u in order:
        for v in dag[u]:
            ways[v] = (ways[v] + ways[u]) % MOD

    return ways[n - 1]

# ------------------- 示例 -------------------
print(count_shortest_ways(
    7,
    [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],
     [3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]
))  # 输出 4

print(count_shortest_ways(
    2,
    [[1,0,10]]
))  # 输出 1
```

> **代码要点**  
> 1. **堆（heap）** 用来实现 Dijkstra 的「每次挑最小未确定距离」的过程。  
> 2. **dist** 数组相当于「每个路口离家最近的时间」标签。  
> 3. **dag** 只保留「标签严格递增」的有向边，天然形成 DAG。  
> 4. **order** 用 `sorted` 按 `dist` 排序即可得到合法的拓扑顺序，因为所有边都指向更大的 `dist`。

#### 复杂度

- **时间复杂度**：  
  - Dijkstra：`O(E log V)`，`V = n ≤ 200`，`E` 最多 `n*(n-1)/2`。  
  - 构造 DAG：`O(E)`。  
  - DP（遍历 DAG）：`O(V + E)`。  
  - 综合为 `O(E log V)`，在本题规模下几乎是常数时间。  

- **空间复杂度**：  
  - 图的邻接表 `O(V + E)`。  
  - `dist、ways、order` 各 `O(V)`。  
  - 合计 `O(V + E)`，即 `O(n²)` 的上界（因为最密集时 `E ≈ n²/2`）。

> 与暴力解相比，时间从指数级降到了近线性（对 `E` 取对数的略高），空间仍然保持线性。

---

## 心得

- **核心技巧**：先求最短距离（Dijkstra），再在「满足最短距离等式」的边上做 DAG DP 计数。  
- **适用的题型**  
  1. “在最短路径上计数” 类题目（如 LeetCode 1786、1976 等）。  
  2. “限定路径必须满足某种单调性” 的计数问题（如「单调递增路径数」）。  
  3. 任意 **加权有向图** 中求「最短路径数量」的场景，只要权重为正即可使用同样思路。  

- **一句话总结**：  
  > 先把「最短路」抽出来变成有向无环图，再用 DP 累计每条合法边的路径数。

---

## 反思

- **第一反应**：直接想遍历所有路径（暴力）——因为最短路径的概念在脑中先浮现，忽视了「计数」可以在更小的子结构上完成。  
- **最容易踩的坑**  
  - **权重很大**（`≤ 10⁹`），导致用 `int` 累加时可能溢出，需要取模。  
  - **多条等价最短路**：必须在 Dijkstra 结束后再检查 `dist[u] + w == dist[v]`，而不是在搜索过程中直接计数，否则会把非最短路径计进去。  
  - **拓扑顺序**：如果直接用 BFS/DFS 拓扑排序，容易忘记 DAG 已经隐含在 `dist` 的递增顺序里，手写拓扑时要确保不遗漏节点。  

- **下次遇到同类题的第一步**：  
  > “先跑一次单源最短路，得到每个节点的最短距离”。有了这些距离，后面的计数就能在一个天然的 DAG 上完成。