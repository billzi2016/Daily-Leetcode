# #3543. 最大加权 K 边路径 / Maximum Weighted K-Edge Path

> 难度：中等 · 标签：Hash Table、Dynamic Programming、Graph · [LeetCode 链接](https://leetcode.com/problems/maximum-weighted-k-edge-path/)

---

## 题目（英文原版）

**Description**

You are given an integer n and a Directed Acyclic Graph (DAG) with n nodes labeled from 0 to n - 1. This is represented by a 2D array edges, where edges[i] = [ui, vi, wi] indicates a directed edge from node ui to vi with weight wi.
You are also given two integers, k and t.
Your task is to determine the maximum possible sum of edge weights for any path in the graph such that:
Return the maximum possible sum of weights for such a path. If no such path exists, return -1.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1,1],[1,2,2]], k = 2, t = 4
Output: 3
Explanation:
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,2],[0,2,3]], k = 1, t = 3
Output: 2
Explanation:
```

**Example 3:**

```
Input: n = 3, edges = [[0,1,6],[1,2,8]], k = 1, t = 6
Output: -1
Explanation:
```

**Constraints**

- 1 <= n <= 300
- 0 <= edges.length <= 300
- edges[i] = [ui, vi, wi]
- 0 <= ui, vi < n
- ui != vi
- 1 <= wi <= 10
- 0 <= k <= 300
- 1 <= t <= 600
- The input graph is guaranteed to be a DAG.
- There are no duplicate edges.

---

## 题目（中文翻译）

给定一个整数 `n` 和一个 **有向无环图**（Directed Acyclic Graph，**DAG**），图中有 `n` 个节点，编号为 `0` 到 `n - 1`。图通过一个二维数组 `edges` 表示，其中 `edges[i] = [ui, vi, wi]` 表示一条从节点 `ui` 指向节点 `vi`、权重为 `wi` 的有向边（edge）。

另外给定两个整数 `k` 和 `t`。

你的任务是找到图中满足以下条件的任意路径（path）：

* 路径恰好包含 `k` 条边（edge）；
* 路径上所有边的权重之和 **严格小于** `t`。

返回所有满足条件的路径中边权重之和的最大可能值。如果不存在满足条件的路径，返回 `-1`。

---

### 示例

**示例 1**

> **输入**: `n = 3, edges = [[0,1,1],[1,2,2]], k = 2, t = 4`  
> **输出**: `3`  
> **解释**: 唯一一条包含 2 条边的路径是 `0 -> 1 -> 2`，权重和为 `1 + 2 = 3 < 4`，因此返回 `3`。

**示例 2**

> **输入**: `n = 3, edges = [[0,1,2],[0,2,3]], k = 1, t = 3`  
> **输出**: `2`  
> **解释**: 包含恰好 1 条边的路径有两条，权重分别为 `2` 和 `3`。由于要求权重和 `< 3`，只能选择权重为 `2` 的路径，故返回 `2`。

**示例 3**

> **输入**: `n = 3, edges = [[0,1,6],[1,2,8]], k = 1, t = 6`  
> **输出**: `-1`  
> **解释**: 唯一的两条单边路径权重分别为 `6` 和 `8`，但均不满足 `< 6` 的条件，故返回 `-1`。

---

### 约束条件

- `1 <= n <= 300`
- `0 <= edges.length <= 300`
- `edges[i] = [ui, vi, wi]`
- `0 <= ui, vi < n`
- `ui != vi`
- `1 <= wi <= 10`
- `0 <= k <= 300`
- `1 <= t <= 600`
- 输入保证构成 **有向无环图**（DAG）
- 不存在重复的边（duplicate edges）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的路径都枚举出来**，然后挑出满足条件的那条：

1. 从图中的每个节点出发，用深度优先搜索（DFS）遍历所有长度不超过 `k` 条有向边的路径。  
2. 每走一条边就把它的权重加到当前路径的总和 `sum` 上。  
3. 当走到第 `k` 条边时（恰好用了 `k` 条边），检查 `sum ≤ t` 是否成立，若成立则更新答案 `ans = max(ans, sum)`。  
4. 由于是 **有向无环图（DAG）**，所以在一次搜索过程中不会出现环路导致无限递归，这让暴力搜索在理论上是可行的。

> **类比**：把图想成城市之间的单行道路，DFS 就像让一位旅行者从某个城市出发，记录走过的路程长度和花费的时间，一直走到恰好走了 `k` 条路为止。

**为什么正确**  
- 我们遍历了 **所有** 恰好包含 `k` 条边的路径（不遗漏也不重复），只要路径满足 `sum ≤ t`，就一定会在遍历过程中被检查到。  
- 最后取最大 `sum`，自然得到题目要求的答案。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maximumWeightedKEdgePath_bruteforce(n: int, edges: List[List[int]],
                                      k: int, t: int) -> int:
    # 建立邻接表：node -> [(next, weight), ...]
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    ans = -1                     # 如果没有合法路径，返回 -1

    # 深度优先搜索
    def dfs(node: int, used: int, cur_sum: int):
        nonlocal ans
        # 用了恰好 k 条边，检查是否满足 sum ≤ t
        if used == k:
            if cur_sum <= t:
                ans = max(ans, cur_sum)
            return
        # 仍有剩余的边可以继续走
        for nxt, w in graph[node]:
            # 只在累计权重仍然 ≤ t 时继续，否则剪枝
            if cur_sum + w <= t:
                dfs(nxt, used + 1, cur_sum + w)

    # 从每个节点尝试出发
    for start in range(n):
        dfs(start, 0, 0)

    return ans
```

> **关键行中文注释**  
> - `graph[u].append((v, w))`：把每条有向边加入邻接表，类似把城市的出入口记录下来。  
> - `if cur_sum + w <= t:`：如果再加这条路的花费已经超过上限 `t`，直接不走（剪枝），省下很多不必要的搜索。  
> - `ans = max(ans, cur_sum)`：记录当前合法路径的最大权重和。

#### 复杂度

- **时间复杂度**：`O( n * branching_factor^k )`  
  - 在最坏情况下，每个节点的出度可能是 `O(n)`，DFS 会产生指数级的分支，随着 `k` 增大会爆炸。可以把它想成“每走一步都有很多选择”，所以不是线性或多项式的，而是 **指数** 的。  
- **空间复杂度**：`O(k)`（递归栈深度）+ `O(n + m)`（邻接表），整体仍然是线性，但递归深度最多 `k ≤ 300`，在 Python 中仍然可接受。

> 由于指数级的时间开销，暴力解只能在非常小的 `n、k` 时才会跑得完。接下来我们要找一种 **多项式** 的方法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**搜索的瓶颈在于大量重复的子路径**。  
同一个节点 `v`、相同已经使用的边数 `e`，只要我们已经知道“从起点到 `v` 用 `e` 条边能够得到的最大权重和”，后面所有以 `v` 为起点继续往下走的计算都可以基于这个信息，而不必重新枚举所有前缀路径。

这正是 **动态规划（DP）** 的思路：把“大问题”拆成“子问题”，子问题的答案只会被使用一次并保存下来。

**关键点 1：状态定义**  
- `dp[v][e]`：**在所有以任意起点开始、恰好走了 `e` 条边、且总权重 ≤ t 的路径中，** 以节点 `v` 为终点时能够得到的**最大权重和**。  
- 如果不存在这样的一条路径，记作 `-inf`（不可达）。

**关键点 2：状态转移**  
考虑一条有向边 `u -> v`，权重为 `w`。  
如果我们已经知道 `dp[u][e]`（即从某个起点到 `u` 用 `e` 条边的最大权重），那么把这条边接在后面就得到一条长度 `e+1` 的路径：

```
if dp[u][e] != -inf and dp[u][e] + w <= t:
    dp[v][e+1] = max(dp[v][e+1], dp[u][e] + w)
```

**关键点 3：遍历顺序**  
因为图是 **DAG**，不存在环路。我们可以先对节点做一次 **拓扑排序**，保证所有进入 `v` 的边的起点 `u` 都已经在 `dp` 中计算完毕。这样就可以像“流水线”一样一次遍历所有边。

**关键点 4：初始化**  
- 对所有节点 `v`，`dp[v][0] = 0`，表示“起点就在这里，使用 0 条边，权重和为 0”。  
- 其余 `dp[v][e]` 先设为 `-inf`（不可达）。

**关键点 5：答案提取**  
遍历所有节点，找出 `dp[v][k]` 的最大值（如果仍是 `-inf`，说明不存在恰好 `k` 条边且权重 ≤ t 的路径，返回 `-1`）。

**为什么快**  
- 每条边只会被访问一次，且对每条边我们只遍历 `e = 0 … k-1`。  
- 总的时间复杂度是 `O( E * k )`，这里 `E ≤ 300，k ≤ 300`，最多约 `9e4` 次操作，轻松跑在毫秒级。  
- 空间只需要保存 `n × (k+1)` 的表，最多 `300 × 301 ≈ 9e4` 个整数，约几百 KB。

> **类比**：把每个节点想成一个“仓库”，`dp[v][e]` 记录的是“恰好用了 `e` 辆卡车搬运货物到这里的最大价值”。每次有新的运输路线（边）时，只要检查前一个仓库的记录是否可用，就能快速算出新的记录，而不必重新算所有可能的搬运方案。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def maximumWeightedKEdgePath(n: int, edges: List[List[int]],
                            k: int, t: int) -> int:
    """
    返回恰好使用 k 条边、总权重不超过 t 的路径的最大权重和。
    若不存在满足条件的路径，返回 -1。
    """
    # ---------- 1. 建图 & 拓扑排序 ----------
    graph = defaultdict(list)      # u -> [(v, w), ...]
    indeg = [0] * n                # 入度，用来做拓扑排序

    for u, v, w in edges:
        graph[u].append((v, w))
        indeg[v] += 1

    # Kahn 算法得到拓扑序列
    q = deque([i for i in range(n) if indeg[i] == 0])
    topo = []                      # 拓扑序列
    while q:
        cur = q.popleft()
        topo.append(cur)
        for nxt, _ in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    # ---------- 2. DP 表 ----------
    NEG = -10**9                    # 表示不可达（-inf）
    dp = [[NEG] * (k + 1) for _ in range(n)]
    for v in range(n):
        dp[v][0] = 0                # 0 条边，权重为 0（起点）

    # ---------- 3. 按拓扑序遍历，进行状态转移 ----------
    for u in topo:                  # 保证所有来源已经处理完
        for v, w in graph[u]:
            # 对每个可能的已使用边数 e，尝试再走这条边得到 e+1 条边的路径
            for e in range(k):     # e 从 0 到 k-1
                if dp[u][e] == NEG:          # 前缀不可达，跳过
                    continue
                new_sum = dp[u][e] + w
                if new_sum > t:               # 超出上限，剪枝
                    continue
                # 更新 dp[v][e+1] 为更大的权重和
                if new_sum > dp[v][e + 1]:
                    dp[v][e + 1] = new_sum

    # ---------- 4. 提取答案 ----------
    best = max(dp[v][k] for v in range(n))
    return best if best != NEG else -1
```

> **关键行中文注释**  
> - `indeg[v] += 1`：记录每个节点的入度，用来找出“没有前驱”的起点。  
> - `while q: ...`：Kahn 算法，确保我们在 DP 时“先算好前面的仓库”。  
> - `dp = [[NEG] * (k + 1) for _ in range(n)]`：创建二维表，行是节点，列是已经使用的边数。  
> - `if dp[u][e] == NEG: continue`：如果到 `u` 用 `e` 条边的路径根本不存在，就不必继续。  
> - `if new_sum > t: continue`：如果再加这条边会把总权重超出上限 `t`，直接丢掉（剪枝）。  
> - `best = max(dp[v][k] for v in range(n))`：在所有以任意节点结束、恰好用了 `k` 条边的路径中找最大权重。

#### 复杂度

- **时间复杂度**：`O(E * k)`  
  - 对每条边我们遍历 `k` 次（0~k-1），所以总操作数约为 `edges.length * k`。  
  - 与暴力的指数级不同，这里是 **线性乘以 k**，在题目限制下非常快。  
- **空间复杂度**：`O(n * k)`  
  - DP 表需要 `n × (k+1)` 的整数，最多约 `9×10⁴`，相当于几百 KB，完全可以接受。

> 与暴力解相比，时间从“指数级”降到了“多项式级”，大幅提升了可行性。

---

## 心得

- **核心技巧**：在 DAG 上利用**动态规划 + 拓扑排序**，把“以某节点为终点、使用固定条数的边”作为子问题，逐层推进。  
- **适用场景**：  
  1. **受限路径长度**（恰好/至多 `k` 条边）的最大/最小权重/费用问题。  
  2. **有上限约束**（如总时间、总费用 ≤ T）的路径规划。  
  3. **在 DAG 上的计数或优化 DP**（例如最长路径、最少费用路径等），只要把“状态 = (节点, 已使用的资源量)”写进去即可。  
- **一句话总结**：把“所有可能的路径”压缩成“每个节点、每条边数对应的最优值”，用拓扑序保证子问题先算好，就能线性遍历完成。

---

## 反思

- **第一反应**：直接想 DFS 把所有路径枚举出来。虽然能写出可运行的代码，但很快会发现会超时。  
- **最容易踩的坑**  
  1. **忘记 DAG 的拓扑顺序**：若随意遍历可能导致使用还未计算好的 `dp[u][e]`，得到错误结果。  
  2. **边数与权重的双重约束**：只检查边数或只检查权重都会产生错误答案，需要同时满足 `e == k` **且** `sum ≤ t`。  
  3. **初始化错误**：`dp[v][0]` 必须是 0（表示“起点在这里”，即使不走任何边也算合法），否则所有后续状态都会不可达。  
  4. **剪枝遗漏**：在转移时忘记 `new_sum ≤ t` 的检查，会导致 DP 表里出现非法的大权重，最终返回错误的答案。  
- **下次思路**：看到 “DAG + 限制边数/费用” 这类关键词时，第一步立刻想到 **拓扑 + DP**，把“节点 + 已使用资源”作为状态，然后进行一次线性遍历。这样既能保证正确性，又能避免指数级的搜索。