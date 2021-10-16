# #1514. 最大概率路径 / Path with Maximum Probability

> 难度：中等 · 标签：Array、Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/path-with-maximum-probability/)

---

## 题目（英文原版）

**Description**

You are given an undirected weighted graph of n nodes (0-indexed), represented by an edge list where edges[i] = [a, b] is an undirected edge connecting the nodes a and b with a probability of success of traversing that edge succProb[i].
Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.
If there is no path from start to end, return 0. Your answer will be accepted if it differs from the correct answer by at most 1e-5.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
Output: 0.25000
Explanation: There are two paths from start to end, one having a probability of success = 0.2 and the other has 0.5 * 0.5 = 0.25.
```

**Example 2:**

```
Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2
Output: 0.30000
```

**Example 3:**

```
Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
Output: 0.00000
Explanation: There is no path between 0 and 2.
```

**Constraints**

- 2 <= n <= 10^4
- 0 <= start, end < n
- start != end
- 0 <= a, b < n
- a != b
- 0 <= succProb.length == edges.length <= 2*10^4
- 0 <= succProb[i] <= 1
- There is at most one edge between every two nodes.

---

## 题目（中文翻译）

给定一个 **无向加权图（undirected weighted graph）**，包含 `n` 个节点（0 起始索引），图通过 **边列表（edge list）** 表示，其中 `edges[i] = [a, b]` 表示节点 `a` 与节点 `b` 之间存在一条无向边，遍历该边的 **成功概率（success probability）** 为 `succProb[i]`。  
给定起点 `start` 和终点 `end`，求从 `start` 到 `end` 的路径，使得该路径的总体成功概率最大，并返回该最大概率的值。  
如果不存在从 `start` 到 `end` 的路径，返回 `0`。只要你的答案与正确答案的差值不超过 `1e-5`，即视为通过。

**示例 1**  
**输入**: `n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2`  
**输出**: `0.25000`  
**解释**: 有两条从 `start` 到 `end` 的路径，一条的成功概率为 `0.2`，另一条的成功概率为 `0.5 * 0.5 = 0.25`，取较大的 `0.25`。

**示例 2**  
**输入**: `n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2`  
**输出**: `0.30000`

**示例 3**  
**输入**: `n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2`  
**输出**: `0.00000`  
**解释**: 节点 `0` 与 `2` 之间不存在路径。

**约束条件**
- `2 <= n <= 10^4`
- `0 <= start, end < n`
- `start != end`
- `0 <= a, b < n`
- `a != b`
- `0 <= succProb.length == edges.length <= 2*10^4`
- `0 <= succProb[i] <= 1`
- 任意两节点之间至多存在一条边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的路径都枚举出来**，然后把每条路径上所有边的成功概率相乘，取最大的那个。  

- **数据结构**：  
  - **邻接表**（把每个节点和它相连的邻居装进一个列表）可以帮助我们“走路”。  
  - **深度优先搜索（DFS）**就像在迷宫里一直往前走，走不通再回头（回溯），把所有能走到终点的路线都记录下来。  
  - 把概率相乘的过程就像把每段路的“成功率”叠加起来，最终得到整条路的成功率。

- **为什么正确**：  
  枚举了**所有**从 `start` 到 `end` 的路径，比较它们的乘积概率，最大值必然就是答案。

- **复杂度分析**：  
  - 时间复杂度：在最坏情况下，图是完全连通的，节点数 `n`，每条边都有两条方向可以走，所有可能的路径数量是指数级的（大约 `O(2^n)`），所以暴力 DFS 会超时。  
  - 空间复杂度：递归栈最多 `n` 层，加上存图的邻接表 `O(n + m)`（`m` 为边数），整体是 `O(n + m)`。

> **大白话**：`O(2^n)` 就像在猜谜游戏里，你要把所有可能的答案列出来，答案数量会像翻倍一样快速增长，几分钟就会变成几千万、几亿，根本算不完。

#### 代码（Python）

```python
from typing import List
import sys

def maxProbability_brute(
    n: int,
    edges: List[List[int]],
    succProb: List[float],
    start: int,
    end: int,
) -> float:
    # 1️⃣ 建立邻接表，邻接表就像每个城市的公交站牌，指明能坐哪路车以及成功率
    graph = [[] for _ in range(n)]
    for (a, b), prob in zip(edges, succProb):
        graph[a].append((b, prob))   # a → b，成功率 prob
        graph[b].append((a, prob))   # b → a，成功率 prob（无向图）

    best = 0.0                     # 记录全局最大概率

    visited = [False] * n          # 防止在同一条路上走回头路

    def dfs(u: int, cur_prob: float) -> None:
        """从节点 u 出发，当前已经走过的路径成功率是 cur_prob"""
        nonlocal best
        if u == end:               # 到达终点，更新答案
            best = max(best, cur_prob)
            return
        visited[u] = True
        for v, p in graph[u]:
            if not visited[v]:
                # 乘上这条边的概率继续往前走
                dfs(v, cur_prob * p)
        visited[u] = False         # 回溯，恢复状态

    dfs(start, 1.0)                # 初始概率是 1（必定在起点）
    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）——遍历所有可能路径，实际会因为图的稀疏程度稍微好一点，但仍然不满足题目规模（`n ≤ 10⁴`）。
- **空间复杂度**：`O(n + m)`——邻接表 + 递归栈（最深 `n` 层）。  

> 暴力解只能帮助我们**理清思路**，但在实际比赛里会直接超时。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于遍历所有路径**。我们其实只需要**找到概率最大的那条路径**，不必把其它低概率的路径全部展开。  

这正好可以用**最短路算法**的思想来处理，只是这里的“距离”不是加法，而是**乘法**（概率相乘）。  
我们把“更大的概率”视为“更小的代价”，于是可以把每条边的代价设为 `-log(p)`（因为 `log(a*b) = log a + log b`），把乘法转成加法，最小化 `-log` 就等价于最大化原始概率。  

不过直接用 `log` 会涉及浮点数的取对数，**也可以不取对数**，只要在 Dijkstra（或更常用的**最大堆**）里把“取最大的概率”当成“取最小的负概率”即可。  

**核心算法**：  
- **Dijkstra + 最大堆**（优先队列）  
  - 每次从堆里取出**当前已知的最大概率的节点**，因为 Dijkstra 保证这一次取出的概率已经是**最优**的。  
  - 用该节点去**松弛**（尝试更新）它的邻居的概率：`newProb = curProb * edgeProb`，如果 `newProb` 更大，就更新并把邻居重新放进堆。  

**为什么对**：  
- Dijkstra 的证明基于“边权非负”。这里我们使用 **概率**（0~1）乘积，等价于 **-log(p)**（非负），所以同样适用。  
- 堆的作用是每次把**最有希望的节点**先处理，避免无意义的遍历，从而把时间降到 `O((n+m) log n)`。

**类比**：  
- 想象有很多条路通往目的地，你每次都先挑**最短（最快）**的那条路走一步，走完后再挑**当前最快**的路继续前进，直到到达终点。这里“最快”对应的是“概率最大”。  

#### 代码（Python）

```python
import heapq
from typing import List

def maxProbability(
    n: int,
    edges: List[List[int]],
    succProb: List[float],
    start: int,
    end: int,
) -> float:
    # 1️⃣ 建图（邻接表），每条边存 (neighbor, probability)
    graph = [[] for _ in range(n)]
    for (a, b), prob in zip(edges, succProb):
        graph[a].append((b, prob))
        graph[b].append((a, prob))

    # 2️⃣ max-heap（Python 的 heapq 是 min-heap，取负数模拟 max-heap）
    # heap 元素是 (-probability, node)
    heap = [(-1.0, start)]          # 起点的概率是 1，取负后 -1.0 进入堆
    best = [0.0] * n                # best[i] 记录已知的最大概率
    best[start] = 1.0

    while heap:
        cur_neg_prob, u = heapq.heappop(heap)
        cur_prob = -cur_neg_prob    # 还原成正数

        # 已经取出的概率不是最新的（因为可能被后面更大的路径更新），直接跳过
        if cur_prob < best[u] - 1e-12:
            continue

        if u == end:                # 提前结束，已经是最大概率
            return cur_prob

        # 3️⃣ 松弛所有相邻边
        for v, edge_p in graph[u]:
            new_prob = cur_prob * edge_p   # 乘上这条边的成功率
            if new_prob > best[v] + 1e-12:
                best[v] = new_prob
                heapq.heappush(heap, (-new_prob, v))

    # 循环结束仍未到达 end，说明不可达
    return 0.0
```

#### 复杂度

- **时间复杂度**：`O((n + m) log n)`  
  - 每条边最多被松弛一次（`m` 次），每次向堆插入或弹出都需要 `log n` 的时间。  
  - 与暴力 `O(2^n)` 相比，**线性乘对数**的复杂度在 `n ≤ 10⁴`、`m ≤ 2·10⁴` 的情况下完全可接受。

- **空间复杂度**：`O(n + m)`  
  - 邻接表存图需要 `O(n + m)`，堆最多会存 `O(n)` 条记录，`best` 数组 `O(n)`。  

> 与暴力解相比，时间从“指数级”下降到“几乎线性”，这就是**算法优化的威力**。

---

## 心得

- **核心技巧**：把“最大乘积路径”转化为 “最短（最小）路径”，利用 **Dijkstra + 最大堆** 求解。  
- **适用场景**：  
  1. **最大概率路径**（本题）  
  2. **最大乘积子数组**（可以取对数后转为最小和）  
  3. **可靠性最高的网络路由**（边权是成功率）  
- **一句话总结**：把“乘积最大”变成“负数最小”，用 Dijkstra 把最有希望的节点先挑出来，一次遍历即可得到答案。

---

## 反思

- **第一反应**：先想到把所有路径枚举（DFS）求最大乘积，直觉对但不够高效。  
- **最容易踩的坑**：  
  - **精度问题**：直接乘概率会产生极小的数，比较时要加上容差（如 `1e-12`）防止因浮点误差导致的错误更新。  
  - **堆的取负**：忘记把概率取负会导致最小堆变成“最小概率”而不是我们想要的“最大概率”。  
  - **提前结束条件**：在弹出 `end` 时直接返回，否则仍会继续遍历，浪费时间。  
- **下次遇到同类题**：第一步先判断**是否可以把乘法转化为加法**（取对数或取负），然后**考虑最短路/最小生成树**等经典图算法，看看能否直接用 Dijkstra、Bellman‑Ford、Prim 等。