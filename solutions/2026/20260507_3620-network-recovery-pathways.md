# #3620. 网络恢复路径 / Network Recovery Pathways

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Graph、Topological Sort、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/network-recovery-pathways/)

---

## 题目（英文原版）

**Description**

You are given a directed acyclic graph of n nodes numbered from 0 to n − 1. This is represented by a 2D array edges of length m, where edges[i] = [ui, vi, costi] indicates a one‑way communication from node ui to node vi with a recovery cost of costi.
Some nodes may be offline. You are given a boolean array online where online[i] = true means node i is online. Nodes 0 and n − 1 are always online.
A path from 0 to n − 1 is valid if:
For each valid path, define its score as the minimum edge‑cost along that path.
Return the maximum path score (i.e., the largest minimum-edge cost) among all valid paths. If no valid path exists, return -1.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,5],[1,3,10],[0,2,3],[2,3,4]], online = [true,true,true,true], k = 10
Output: 3
Explanation:

The graph has two possible routes from node 0 to node 3:
Path 0 → 1 → 3
Total cost = 5 + 10 = 15 , which exceeds k ( 15 > 10 ), so this path is invalid.
Path 0 → 2 → 3
Total cost = 3 + 4 = 7 <= k , so this path is valid.
The minimum edge‐cost along this path is min(3, 4) = 3 .
There are no other valid paths. Hence, the maximum among all valid path‐scores is 3.
```

**Example 2:**

```
Input: edges = [[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]], online = [true,true,true,false,true], k = 12
Output: 6
Explanation:

Node 3 is offline, so any path passing through 3 is invalid.
Consider the remaining routes from 0 to 4:
Path 0 → 1 → 4
Total cost = 7 + 5 = 12 <= k , so this path is valid.
The minimum edge‐cost along this path is min(7, 5) = 5 .
Path 0 → 2 → 3 → 4
Node 3 is offline, so this path is invalid regardless of cost.
Path 0 → 2 → 4
Total cost = 6 + 6 = 12 <= k , so this path is valid.
The minimum edge‐cost along this path is min(6, 6) = 6 .
Among the two valid paths, their scores are 5 and 6. Therefore, the answer is 6.
```

**Constraints**

- n == online.length
- 2 <= n <= 5 * 104
- 0 <= m == edges.length <= min(105, n * (n - 1) / 2)
- edges[i] = [ui, vi, costi]
- 0 <= ui, vi < n
- ui != vi
- 0 <= costi <= 109
- 0 <= k <= 5 * 1013
- online[i] is either true or false, and both online[0] and online[n − 1] are true.
- The given graph is a directed acyclic graph.

---

## 题目（中文翻译）

**题目描述**  
给定一个包含 `n` 个节点（编号从 `0` 到 `n‑1`）的有向无环图（directed acyclic graph），用长度为 `m` 的二维数组 `edges` 表示，其中 `edges[i] = [ui, vi, costi]` 表示一条从节点 `ui` 到节点 `vi` 的单向通信，恢复成本（recovery cost）为 `costi`。  
某些节点可能处于离线状态。布尔数组 `online` 用于描述节点是否在线：`online[i] = true` 表示节点 `i` 在线，`online[i] = false` 表示离线。节点 `0` 与节点 `n‑1` 必定在线。  

此外，给定一个整数 `k`，表示总成本上限。  

一条从 `0` 到 `n‑1` 的路径（path）满足以下条件即为**有效路径**：  
1. 路径上所有经过的节点均在线（即对应的 `online` 为 `true`）。  
2. 路径上所有边的恢复成本之和不超过 `k`（`∑ cost ≤ k`）。  

对于每条有效路径，定义其**得分**为该路径上 **最小边成本**（minimum edge‑cost），即路径中所有边的恢复成本的最小值。  

返回所有有效路径中**最大路径得分**（即最大化的最小边成本）。如果不存在任何有效路径，返回 `-1`。

---

### 示例

**示例 1**

```text
Input: edges = [[0,1,5],[1,3,10],[0,2,3],[2,3,4]], online = [true,true,true,true], k = 10
Output: 3
Explanation:
图中存在两条从节点 0 到节点 3 的可能路线：

- 路径 0 → 1 → 3  
  总成本 = 5 + 10 = 15 > k，超出上限，因此该路径无效。

- 路径 0 → 2 → 3  
  总成本 = 3 + 4 = 7 ≤ k，满足成本限制，且所有节点均在线。  
  此路径的最小边成本为 min(3, 4) = 3。

所有有效路径中，最大的最小边成本为 **3**，因此返回 3。
```

**示例 2**

```text
Input: edges = [[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]], online = [true,true,true,false,true], k = 12
Output: 6
Explanation:
节点 3 为离线状态，任何经过该节点的路径均视为无效。考虑剩余的从 0 到 4 的路线：

- 路径 0 → 1 → 4  
  总成本 = 7 + 5 = 12 ≤ k，且所有节点在线。  
  最小边成本为 min(7, 5) = 5。

- 路径 0 → 2 → 4  
  总成本 = 6 + 6 = 12 ≤ k，所有节点在线。  
  最小边成本为 min(6, 6) = 6。

在所有有效路径中，最大的最小边成本为 **6**，因此返回 6。
```

---

### 约束条件

- `n == online.length`
- `2 ≤ n ≤ 5 * 10^4`
- `0 ≤ m == edges.length ≤ min(10^5, n * (n - 1) / 2)`
- `edges[i] = [ui, vi, costi]`
- `0 ≤ ui, vi < n`
- `ui != vi`
- `0 ≤ costi ≤ 10^9`
- `0 ≤ k ≤ 5 * 10^13`
- `online[i] 为 true 或 false，且 `online[0]` 与 `online[n‑1]` 必定为 true`
- 给定的图是有向无环图（directed acyclic graph）

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有可能的路径都枚举出来**，然后把每条路径的两件事算好：

1. **路径的总费用**（所有边的 `cost` 之和），看它是否 ≤ `k`。  
2. **路径的得分**——路径上最小的那条边的 `cost`，记为 `minEdge`。  

把所有满足总费用 ≤ `k` 的路径的 `minEdge` 取最大值，就是答案。

> **类比**：想象你在城市里找从家（节点 0）到公司（节点 n‑1）的所有路线。每条路都有若干段道路（边），每段道路都有“宽度”（费用）和“质量”（边的 `cost`)。你先把所有路线列出来，挑出总费用不超预算的，然后在每条路线里找最窄的那段路（最小边），最后选出“最宽的最窄路”。  

**为什么能得到正确答案**  
因为我们把 **所有合法路径** 都检查了一遍，必然不会漏掉最优的那条。

**为什么会超时**  
- 在最坏情况下，DAG 里可能有指数级的路径数量（比如完全二分层的 DAG）。枚举所有路径的时间会是 `O(2^n)`，根本不可接受。  
- 即使只遍历一次图，若每次都做一次完整的 **最短路** 计算（比如 BFS/DFS），时间仍是 `O(n·m)`，在 `n≈5·10⁴、m≈10⁵` 时已经太慢。

#### 代码（Python）  
下面的代码只演示了「枚举所有路径」的思想（**不建议在实际提交中使用**），以帮助大家理解为什么会超时。  

```python
from collections import defaultdict

def brute_max_min_edge(edges, online, k):
    n = len(online)
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))

    best = -1

    def dfs(u, cur_sum, cur_min):
        """深度优先遍历所有路径，u 为当前所在节点"""
        nonlocal best
        if cur_sum > k:                 # 超预算直接剪枝
            return
        if u == n - 1:                  # 到达终点，更新答案
            best = max(best, cur_min)
            return
        for v, w in g[u]:
            if not online[v]:          # 只能经过在线节点
                continue
            dfs(v, cur_sum + w, min(cur_min, w) if cur_min else w)

    # 起点一定在线，初始最小边设为正无穷（这里用 None 代表未定义）
    dfs(0, 0, None)
    return best
```

> **提示**：`dfs` 里用了两层剪枝：  
> - **预算剪枝**：一旦累计费用已经超过 `k`，后面的递归直接返回。  
> - **在线节点剪枝**：离线节点直接不走。  

#### 复杂度  
- **时间复杂度**：最坏情况下会遍历所有可能的路径，指数级 `O(2^n)`（远大于题目限制）。  
- **空间复杂度**：递归栈深度最多 `O(n)`，以及存图的邻接表 `O(n + m)`。

> **大白话**：`O(2^n)` 就像把 20 个人排成队，每个人可以选站或不站，一共有 1,048,576 种组合。n=50 时，这个数字已经是天文数字，根本算不过来。

---

### 2. 最优解  

#### 思路  
从暴力解可以看出，**枚举路径是不可取的**。我们需要一种只遍历 **一次图** 就能判断「是否存在满足条件的路径」的方法。  

**关键观察**  

1. **我们要最大化「路径最小边」**，这正好可以二分搜索（binary search）答案。  
   - 假设我们猜一个值 `mid`，问：**是否存在一条从 0 到 n‑1、只走 `cost ≥ mid` 的边、总费用 ≤ k 的路径？**  
   - 如果答案是 **YES**，说明 `mid` 可以成为答案的下界，继续往更大尝试。  
   - 如果答案是 **NO**，说明 `mid` 太大，需要往小的方向搜索。  

2. **判定子问题**（给定 `mid`）可以转化为**最短路**问题：  
   - 把所有 **边权 < mid** 的边直接删掉（因为它们会把路径的最小边降低到 < mid）。  
   - 在剩下的子图里，找 **从 0 到 n‑1 的最小总费用**。如果最小费用 ≤ k，则 `mid` 可行。  
   - 由于原图是 **DAG**（有向无环图），最短路可以用 **拓扑序 + 动态规划** 在 `O(n + m)` 时间完成，而不需要 Dijkstra 的堆。  

3. **在线节点的限制**：在构造子图时，只保留 `online[i] == True` 的节点。离线节点以及所有经过它的边直接忽略。  

**整体算法**  

1. **预处理**：  
   - 读取 `edges`，建立邻接表 `adj[u] = [(v, w), …]`。  
   - 用 **Kahn 算法**（基于入度）一次性得到 **拓扑序** `topo`（整个图都不变，后面每次检查只在这条顺序上遍历）。  

2. **二分搜索**：  
   - `low = 0`，`high = max(cost_i)`（所有边的最大费用），答案初始 `ans = -1`。  
   - 循环 `while low <= high`：  
     - `mid = (low + high) // 2`。  
     - 调用 `feasible(mid)` 检查子问题。  

3. **可行性检查 `feasible(limit)`**（核心）  
   - `dist[i] = INF`，`dist[0] = 0`（起点费用为 0）。  
   - 按照 **拓扑序** 遍历每个节点 `u`：  
     - 若 `online[u]` 为 `False`，直接跳过（因为已经在构造子图时排除了）。  
     - 对于每条出边 `(v, w)`：  
       - **仅当** `w >= limit` **且** `online[v]` 为 `True` 时才考虑。  
       - 松弛：`dist[v] = min(dist[v], dist[u] + w)`。  
   - 最终如果 `dist[n-1] <= k`，返回 `True`，否则 `False`。  

4. **二分搜索更新**：  
   - 若 `feasible(mid)` 为 `True`：`ans = mid`，`low = mid + 1`（尝试更大）。  
   - 否则：`high = mid - 1`。  

5. 返回 `ans`（若始终不可行，则保持 `-1`）。  

**为什么是最优的**  

- **二分搜索**把原本可能的答案空间（`0 … 10⁹`）压缩到 `log₂(10⁹) ≈ 30` 次检查。  
- 每次检查只遍历一次图（`O(n+m)`），而 **拓扑 DP** 在 DAG 上是线性的，不需要堆结构，常数更小。  
- 整体时间 `O((n+m)·log C)`（`C` 为最大边权），在题目限制 `n ≤ 5·10⁴、m ≤ 10⁵` 下完全可接受。  

#### 代码（Python）  

```python
from collections import deque
from typing import List

INF = 10 ** 20          # 足够大的数，代表“不可达”

def maximumPathScore(edges: List[List[int]], online: List[bool], k: int) -> int:
    """
    返回从 0 到 n-1 的路径中，满足
        1) 只经过 online 为 True 的节点（0 与 n-1 必定在线）
        2) 总费用 <= k
        3) 路径最小边的 cost 最大化
    若不存在合法路径，返回 -1
    """
    n = len(online)

    # ---------- 1. 建图 & 拓扑序 ----------
    adj = [[] for _ in range(n)]          # 正向邻接表
    indeg = [0] * n                       # 入度，用于拓扑排序

    max_cost = 0
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
        max_cost = max(max_cost, w)

    # Kahn 算法得到拓扑序（整个图都是 DAG，拓扑序唯一或不唯一都行）
    q = deque([i for i in range(n) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # ---------- 2. 可行性检查 ----------
    def feasible(limit: int) -> bool:
        """
        限制最小边权 >= limit，判断是否存在总费用 <= k 的路径。
        """
        dist = [INF] * n
        if not online[0]:          # 题目保证 0 在线，这里仅作防御性检查
            return False
        dist[0] = 0

        for u in topo:
            if not online[u]:          # 离线节点直接跳过
                continue
            if dist[u] == INF:         # 当前节点不可达，后续也不可达
                continue
            for v, w in adj[u]:
                if not online[v]:
                    continue
                if w < limit:           # 这条边不满足最小边要求
                    continue
                # 松弛：尝试通过 u 到达 v
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd

        return dist[n - 1] <= k

    # ---------- 3. 二分搜索 ----------
    low, high = 0, max_cost
    ans = -1
    while low <= high:
        mid = (low + high) // 2
        if feasible(mid):
            ans = mid           # mid 可行，尝试更大
            low = mid + 1
        else:
            high = mid - 1      # mid 不可行，缩小范围

    return ans
```

> **代码要点说明**  
> 1. **拓扑序只算一次**：`topo` 在函数外部一次性得到，后续每次 `feasible` 直接遍历即可。  
> 2. **离线节点的处理**：在 `feasible` 里先判断 `online[u]` 与 `online[v]`，把离线节点及其所有出入边直接过滤掉。  
> 3. **边权阈值 `limit`**：只有 `w >= limit` 的边才会被考虑，正好对应二分搜索的“当前猜的最小边”。  
> 4. **距离数组 `dist`** 用 `INF` 表示不可达，防止溢出。  
> 5. **返回值**：若二分搜索始终未找到可行解，`ans` 仍为 `-1`，符合题目要求。

#### 复杂度  

- **时间复杂度**：  
  - 拓扑排序一次 `O(n + m)`。  
  - 二分搜索最多 `log₂(maxCost) ≤ 31` 次。每次检查遍历全部节点和边一次 `O(n + m)`。  
  - **总计** `O((n + m) · log maxCost)`，约等于 `O((n + m)·30)`，在最坏规模下约 `4.5·10⁶` 次基本操作，轻松通过。  

- **空间复杂度**：  
  - 邻接表 `O(n + m)`。  
  - 拓扑序、入度、距离数组等均为 `O(n)`。  
  - **总体** `O(n + m)`，即线性空间。

> 与暴力解相比：  
> - 暴力解的时间是指数级，根本不可用。  
> - 最优解把问题压缩到 **线性遍历 + 对数次二分**，实现了巨大的提升。

---

## 心得  

- **核心技巧**：**二分答案 + DAG 上的最短路（拓扑 DP）**。  
- **适用场景**：  
  1. “最大化最小值” 类型的路径/选取问题（如最大最小容量、最大最小安全系数）。  
  2. 需要在 **单调性**（答案越大约束越强）下判断可行性的题目。  
  3. **有向无环图** 的最短/最长路问题，尤其可以利用拓扑序做 DP。  

- **一句话总结**：  
  *把“最大化最小边”变成“是否存在边权≥阈值的可行路径”，用二分搜索把阈值逼到极限，再用拓扑 DP 检查预算即可。*  

---

## 反思  

- **第一反应**：看到“路径的最小边要最大”，立刻想到二分搜索 + 判定函数。  
- **最容易踩的坑**  
  1. **离线节点**：忘记在判定函数里把离线节点及其所有出入边过滤，导致错误的最短路。  
  2. **预算 k 的限制**：只检查“是否存在路径”，而不考虑总费用，容易得到错误的答案。  
  3. **拓扑序的正确性**：如果图不是 DAG，拓扑排序会失败；但题目保证是 DAG，仍需在代码里做好异常防护（如检测拓扑长度是否等于 n）。  
  4. **二分边界**：`low` 与 `high` 的取值必须覆盖所有可能的最小边，尤其要把 `max(cost)` 设为上界，否则可能错过答案。  

- **下次类似题的第一步**：  
  先判断“答案随阈值单调变化”吗？若是（阈值越大，满足条件的路径越少），立刻考虑 **二分答案**，并思考 **如何在固定阈值下快速判定可行**（DP、Dijkstra、BFS…）。  

祝你玩得开心，算法之路越走越宽！