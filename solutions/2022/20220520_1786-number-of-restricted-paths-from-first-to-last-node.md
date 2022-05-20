# #1786. 从第一个节点到最后一个节点的受限路径数量 / Number of Restricted Paths From First to Last Node

> 难度：中等 · 标签：Dynamic Programming、Graph、Topological Sort、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/number-of-restricted-paths-from-first-to-last-node/)

---

## 题目（英文原版）

**Description**

There is an undirected weighted connected graph. You are given a positive integer n which denotes that the graph has n nodes labeled from 1 to n, and an array edges where each edges[i] = [ui, vi, weighti] denotes that there is an edge between nodes ui and vi with weight equal to weighti.
A path from node start to node end is a sequence of nodes [z0, z1, z2, ..., zk] such that z0 = start and zk = end and there is an edge between zi and zi+1 where 0 <= i <= k-1.
The distance of a path is the sum of the weights on the edges of the path. Let distanceToLastNode(x) denote the shortest distance of a path between node n and node x. A restricted path is a path that also satisfies that distanceToLastNode(zi) > distanceToLastNode(zi+1) where 0 <= i <= k-1.
Return the number of restricted paths from node 1 to node n. Since that number may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[1,2,3],[1,3,3],[2,3,1],[1,4,2],[5,2,2],[3,5,1],[5,4,10]]
Output: 3
Explanation: Each circle contains the node number in black and its distanceToLastNode value in blue. The three restricted paths are:
1) 1 --> 2 --> 5
2) 1 --> 2 --> 3 --> 5
3) 1 --> 3 --> 5
```

**Example 2:**

```
Input: n = 7, edges = [[1,3,1],[4,1,2],[7,3,4],[2,5,3],[5,6,1],[6,7,2],[7,5,3],[2,6,4]]
Output: 1
Explanation: Each circle contains the node number in black and its distanceToLastNode value in blue. The only restricted path is 1 --> 3 --> 7.
```

**Constraints**

- 1 <= n <= 2 * 104
- n - 1 <= edges.length <= 4 * 104
- edges[i].length == 3
- 1 <= ui, vi <= n
- ui != vi
- 1 <= weighti <= 105
- There is at most one edge between any two nodes.
- There is at least one path between any two nodes.

---

## 题目（中文翻译）

存在一个 **无向加权连通图**（undirected weighted connected graph）。给定一个正整数 `n`，表示图中有 `n` 个节点，编号为 `1` 到 `n`，以及一个数组 `edges`，其中 `edges[i] = [ui, vi, weighti]` 表示节点 `ui` 与节点 `vi` 之间存在一条权重为 `weighti` 的 **边**（edge）。

从节点 `start` 到节点 `end` 的 **路径**（path）是一系列节点 `[z0, z1, z2, ..., zk]`，满足 `z0 = start`、`zk = end`，并且对于所有 `0 ≤ i ≤ k‑1`，节点 `zi` 与 `zi+1` 之间存在一条 **边**（edge）。

一条路径的 **距离**（distance）是该路径上所有 **边**（edge）权重之和。记 `distanceToLastNode(x)` 为节点 `x` 到节点 `n` 的 **最短距离**（shortest distance）。如果一条路径满足  
`distanceToLastNode(zi) > distanceToLastNode(zi+1)`（对所有 `0 ≤ i ≤ k‑1`），则称其为 **受限路径**（restricted path）。

返回从节点 `1` 到节点 `n` 的 **受限路径**（restricted path）的数量。由于答案可能非常大，请返回 `答案 mod (10^9 + 7)` 的结果。

---

## 示例

### 示例 1
**输入**  
`n = 5, edges = [[1,2,3],[1,3,3],[2,3,1],[1,4,2],[5,2,2],[3,5,1],[5,4,10]]`

**输出**  
`3`

**解释**  
每个圆圈中黑色数字表示节点编号，蓝色数字表示 `distanceToLastNode` 的值。满足受限条件的三条路径为：

1. `1 --> 2 --> 5`
2. `1 --> 2 --> 3 --> 5`
3. `1 --> 3 --> 5`

### 示例 2
**输入**  
`n = 7, edges = [[1,3,1],[4,1,2],[7,3,4],[2,5,3],[5,6,1],[6,7,2],[7,5,3],[2,6,4]]`

**输出**  
`1`

**解释**  
每个圆圈中黑色数字表示节点编号，蓝色数字表示 `distanceToLastNode` 的值。唯一满足受限条件的路径是 `1 --> 3 --> 7`。

---

## 约束条件

- `1 <= n <= 2 * 10^4`
- `n - 1 <= edges.length <= 4 * 10^4`
- `edges[i].length == 3`
- `1 <= ui, vi <= n`
- `ui != vi`
- `1 <= weighti <= 10^5`
- 任意两节点之间至多只有一条 **边**（edge）。
- 任意两节点之间至少存在一条 **路径**（path）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有从 1 到 n 的路径都枚举出来**，然后逐条检查它们是否满足“受限路径”的条件。  
实现步骤可以是：

1. 先把图用邻接表保存，`adj[u]` 保存所有和 `u` 相连的 `(v, w)`（节点 + 边权）。  
2. 用一次普通的 **深度优先搜索（DFS）** 从节点 `1` 开始遍历。每走一步就把当前节点记入路径 `path`，并把已经走过的节点放进 `visited` 集合，防止走回头路（因为题目没有要求路径必须是**简单**的，但如果出现环会导致无限递归）。  
3. 当走到节点 `n` 时，得到一条完整的 `1 → n` 路径。此时再利用 **distanceToLastNode**（即从每个节点到 `n` 的最短距离）来判断：  
   - 对路径中的相邻节点 `zi , zi+1` 检查 `dist[zi] > dist[zi+1]`。  
   - 若全部满足，则计数器 `ans += 1`。  

> **类比**：把邻接表想象成城市的公交站点表，`DFS` 就像是让你从起点不停换乘，直到到达终点。`visited` 相当于“已经去过的站点”，防止你在同一条线路上来回跑。

**为什么正确**：  
- DFS 能遍历 **所有可能的走法**（只要不重复访问同一个节点），因此不会漏掉任何合法路径。  
- 对每条完整路径都进行距离比较，正好对应题目对“受限路径”的定义。

**复杂度分析**（大白话）：

- **时间**：最坏情况下，图是一条完全连通的密集图，DFS 会尝试每一种可能的走法。走法的数量是指数级的，大约是 `O(2^n)`（因为每个节点可以“选或不选”）。再乘上每条路径要检查 `k`（路径长度）次距离大小，整体仍是指数级，根本不可接受。  
- **空间**：递归栈最多保存 `n` 层节点，加上邻接表的存储，空间是 `O(n + m)`，其中 `m` 是边数。  

> **O(2^n) 代表**：当节点数翻倍时，可能的走法会翻 **指数**（几乎是翻了 2 的 n 次方），这在实际运行中会很快把电脑的内存和时间耗尽。

#### 代码（Python）

```python
from collections import defaultdict

MOD = 10**9 + 7

def countRestrictedPaths_bruteforce(n, edges):
    # ---------- 建图 ----------
    adj = defaultdict(list)                     # 邻接表
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    # ---------- 先算出 distanceToLastNode ----------
    # 这里仍然使用 Dijkstra（因为它实现简单），但在暴力解里我们只把它当作“预处理”
    import heapq
    INF = 10**18
    dist = [INF] * (n + 1)
    dist[n] = 0
    heap = [(0, n)]                              # (当前最短距离, 节点)
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))

    # ---------- 深度优先搜索枚举所有路径 ----------
    ans = 0
    visited = set()

    def dfs(u, prev_dist):
        """从 u 出发继续往下走，prev_dist 为前一个节点的 distanceToLastNode"""
        nonlocal ans
        if u == n:                     # 到达终点，算作一条合法路径
            ans = (ans + 1) % MOD
            return
        visited.add(u)
        for v, _ in adj[u]:
            if v in visited:
                continue
            # 受限路径的关键判断：当前节点的距离必须严格大于下一节点的距离
            if dist[u] > dist[v]:
                dfs(v, dist[v])
        visited.remove(u)              # 回溯，允许后面的其他分支使用 u

    dfs(1, dist[1])
    return ans
```

> 代码里每一行都有中文注释，帮助你快速定位作用。  
> **注意**：这段代码在 `n` 达到 10⁴ 时会 **超时**，仅用于演示思路。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）——因为会尝试所有可能的走法。  
- **空间复杂度**：`O(n + m)`——邻接表 + 递归栈。  

---

### 2. 最优解  

#### 思路  

暴力解太慢的根源在于 **“枚举所有路径”**。我们需要 **直接算出有多少条合法路径**，而不是把它们一个一个列出来。  
从提示可以得到两个关键点：

1. **先求出每个节点到 n 的最短距离** `dist[x]`。这一步可以用 **Dijkstra**（单源最短路）一次完成，时间 `O(m log n)`。  
2. **把原来的无向图“方向化”。**  
   - 对每条无向边 `[u, v]`，比较 `dist[u]` 与 `dist[v]`。  
   - 若 `dist[u] > dist[v]`，则只能沿 **u → v** 走（因为受限路径要求距离递减）。  
   - 若 `dist[v] > dist[u]`，则只能沿 **v → u** 走。  
   - 若两者相等，则这条边在受限路径中 **永远用不到**，直接丢弃。  

   这样处理后，所有保留下来的有向边的 **方向都是从距离大的节点指向距离小的节点**，显然不存在环——因为距离严格递减，沿着有向边走不可能回到已经走过的节点。于是我们得到了一张 **有向无环图（DAG）**。  

3. **在这张 DAG 上统计从 1 到 n 的路径数**。  
   - DAG 的经典做法是 **拓扑排序**（或者直接按照 `dist` 从大到小的顺序遍历），然后用 **动态规划** 累计路径数。  
   - 设 `dp[x]` 为 **从节点 x 到 n 的受限路径数**。显然 `dp[n] = 1`（到自己算一条空路径）。  
   - 对于其它节点 `x`，所有可以走的下一跳都是 `y`，满足 `dist[x] > dist[y]` 且有有向边 `x → y`。于是  
     ```
     dp[x] = Σ dp[y]   (对所有 x → y 的边)
     ```
   - 按照 `dist` 从小到大（即从 n 往 1 方向）计算 `dp`，因为 `dp[y]` 已经在计算 `dp[x]` 之前确定。  

4. 最终答案是 `dp[1] mod (1e9+7)`。

> **类比**：  
> - 把 `dist` 想成山的海拔高度。受限路径要求你只能 **往下走**（海拔递减）。  
> - 把原来的无向道路想成山间小径，先把只能往下走的方向标记出来，就得到一条 **只能下坡的单向道路网络**。  
> - 统计从山脚（节点 1）到山顶（节点 n）的所有下坡路线数，这正是 DP 在 DAG 上的典型应用。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

MOD = 10**9 + 7

def countRestrictedPaths(n: int, edges: list[list[int]]) -> int:
    # ---------- 1. 建图（无向） ----------
    graph = defaultdict(list)          # graph[u] = [(v, w), ...]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # ---------- 2. Dijkstra：求每个节点到 n 的最短距离 ----------
    INF = 10**18
    dist = [INF] * (n + 1)
    dist[n] = 0
    heap = [(0, n)]                     # (当前最短距离, 节点)
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue                    # 过时的条目，直接丢弃
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    # ---------- 3. 按距离从大到小的顺序准备 DP ----------
    #   我们不需要显式地把图变成有向图，只要在 DP 时检查方向即可。
    order = sorted(range(1, n + 1), key=lambda x: dist[x])   # dist 小的在前（n 最前）
    dp = [0] * (n + 1)
    dp[n] = 1                         # 到达 n 本身算一条路径

    # ---------- 4. 逆向 DP（从小距离往大距离累加） ----------
    #    对每个节点 u，遍历它的所有邻居 v：
    #       如果 dist[u] > dist[v]（即只能 u -> v），则 dp[u] += dp[v]
    for u in order:                   # 从 n 往 1 方向遍历
        for v, _ in graph[u]:
            if dist[u] > dist[v]:    # 只能沿着距离递减的方向走
                dp[u] = (dp[u] + dp[v]) % MOD

    return dp[1] % MOD
```

> **代码要点解释**  
> 1. **Dijkstra**：使用最小堆（`heapq`），每次弹出当前已知的最短距离节点。时间 `O(m log n)`。  
> 2. **`order` 排序**：因为 `dist` 是严格递减的方向，按照距离从小到大遍历即可保证在计算 `dp[u]` 时，所有可能的后继 `dp[v]` 已经算好。  
> 3. **DP 累加**：只在 `dist[u] > dist[v]` 时累加，天然实现了“有向化”。  

#### 复杂度  

- **时间复杂度**：`O(m log n)`  
  - Dijkstra：`O(m log n)`（堆操作）  
  - 排序节点：`O(n log n)`（但 `n ≤ 2·10⁴`，可以忽略）  
  - DP 遍历所有边一次：`O(m)`  
  综合来看，最耗时的是 Dijkstra，整体是 `O(m log n)`。  
  > **含义**：即使图有 4·10⁴ 条边，算法也只需要几万次堆操作，完全可以在一秒内跑完。  

- **空间复杂度**：`O(n + m)`  
  - 邻接表保存所有边 `O(m)`  
  - `dist`、`dp`、堆等额外数组 `O(n)`  

---

## 心得  

- **核心技巧**：先把 **“距离递减”** 的约束转化为 **有向无环图**（DAG），再用 **DP 在 DAG 上计数**。  
- **适用的题型**  
  1. **“受限路径 / 单调路径”** 类似题目，例如 “Number of Good Paths”。  
  2. **“从源点到终点的有向路径计数”**，如 “Count All Valid Paths in a DAG”。  
  3. **先算最短距离再做 DP** 的组合题，如 “Shortest Path with Alternating Colors”。  
- **一句话总结**：把“只能往距离更小的节点走”这条规则变成有向边，图立刻变成 DAG，DP 一遍就能得到答案。  

---

## 反思  

- **第一反应**：看到“受限路径”这几个字，我立刻想到 **枚举所有路径**，因为对路径的约束好像只能在走的过程中逐个检查。  
- **最容易踩的坑**  
  1. **忘记取模**：答案可能非常大，需要在每次 DP 累加时 `% MOD`。  
  2. **距离相等的边**：如果 `dist[u] == dist[v]`，这条边在受限路径中根本不能使用，必须 **丢弃**，否则会导致错误的环。  
  3. **图的连通性**：虽然题目保证连通，但 Dijkstra 必须从 **节点 n** 开始，而不是随意选一个起点。  
  4. **递归深度**：如果仍用递归实现 DP，深度可能达 `n`，在 Python 中会触发递归深度限制，使用 **迭代**（如本解法的遍历顺序）更安全。  
- **下次遇到同类题**：第一步先 **把约束转化为 DAG**（或其他可以拓扑排序的结构），再 **用 DP 计数**，而不是直接枚举。这样往往能把指数级的搜索压到多项式时间。