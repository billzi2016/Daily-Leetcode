# #3559. 为边分配权重的方案数 II / Number of Ways to Assign Edge Weights II

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-ii/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 1 to n, rooted at node 1. The tree is represented by a 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates that there is an edge between nodes ui and vi.
Initially, all edges have a weight of 0. You must assign each edge a weight of either 1 or 2.
The cost of a path between any two nodes u and v is the total weight of all edges in the path connecting them.
You are given a 2D integer array queries. For each queries[i] = [ui, vi], determine the number of ways to assign weights to edges in the path such that the cost of the path between ui and vi is odd.
Return an array answer, where answer[i] is the number of valid assignments for queries[i].
Since the answer may be large, apply modulo 109 + 7 to each answer[i].
Note: For each query, disregard all edges not in the path between node ui and vi.

**Examples**

**Example 1:**

```
Input: edges = [[1,2]], queries = [[1,1],[1,2]]
Output: [0,1]
Explanation:
```

**Example 2:**

```
Input: edges = [[1,2],[1,3],[3,4],[3,5]], queries = [[1,4],[3,4],[2,5]]
Output: [2,1,4]
Explanation:
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i] == [ui, vi]
- 1 <= queries.length <= 105
- queries[i] == [ui, vi]
- 1 <= ui, vi <= n
- edges represents a valid tree.

---

## 题目（中文翻译）

存在一棵 **无向树（undirected tree）**，共有 `n` 个节点，编号为 `1 ~ n`，根节点为 `1`。树由长度为 `n‑1` 的二维整数数组 `edges` 表示，其中 `edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间有一条边。  

初始时所有边的权重均为 `0`，你需要把每条边的权重重新赋值为 `1` 或 `2`。  

任意两节点 `u` 与 `v` 之间的 **路径（path）** 的代价定义为该路径上所有边权重之和。  

给定二维整数数组 `queries`，其中 `queries[i] = [ui, vi]` 表示一次查询。对于每个查询，需要计算在 **仅考虑 `ui` 与 `vi` 之间的路径上的边** 的情况下，使该路径代价为奇数的权重分配方案数。  

返回数组 `answer`，其中 `answer[i]` 为对应查询 `queries[i]` 的有效方案数。由于答案可能很大，请对每个 `answer[i]` 取模 `10^9 + 7`。  

> **注意**：对每个查询，只考虑位于 `ui` 与 `vi` 路径上的边，其他边不计入本次计算。

---

## 示例

### 示例 1  
**输入**  
```text
edges = [[1,2]]
queries = [[1,1],[1,2]]
```  
**输出**  
```text
[0,1]
```  
**解释**  
- 查询 `[1,1]` 的路径为空，无法得到奇数代价，方案数为 `0`。  
- 查询 `[1,2]` 的路径仅包含一条边，该边权重只能取 `1`（奇数）才能使路径代价为奇数，方案数为 `1`。

### 示例 2  
**输入**  
```text
edges = [[1,2],[1,3],[3,4],[3,5]]
queries = [[1,4],[3,4],[2,5]]
```  
**输出**  
```text
[2,1,4]
```  
**解释**  
- 对于查询 `[1,4]`，路径为 `1‑3‑4`，共有两条边。使总权重为奇数的赋值方式有 `2` 种。  
- 对于查询 `[3,4]`，路径仅为一条边 `3‑4`，只能将该边权重设为 `1`，方案数为 `1`。  
- 对于查询 `[2,5]`，路径为 `2‑1‑3‑5`，包含三条边。使总权重为奇数的赋值方式共有 `4` 种。

---

## 约束条件

- `2 ≤ n ≤ 10^5`
- `edges.length = n - 1`
- `edges[i] = [ui, vi]`
- `1 ≤ queries.length ≤ 10^5`
- `queries[i] = [ui, vi]`
- `1 ≤ ui, vi ≤ n`
- `edges` 构成一棵合法的树  

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一次询问当成一次独立的子树**，把路径上的所有边都列出来，然后枚举这些边的权重（1 或 2），统计总权重为奇数的方案数。

- **数据结构**  
  - **邻接表**：把树存成 `graph[u] = [(v1), (v2), …]`，就像把城市的地图画在一本小册子里，查相邻的城市只需要翻到对应的那一页。  
  - **队列 / 栈**：做一次 BFS/DFS 从 `u` 出发，直到找到 `v`，相当于在地图上一步一步走，记录走过的每条路。

- **为什么正确**  
  - 枚举了**所有**可能的权重分配（每条边都有两种选择），只要把每一种情况的路径总和算出来，奇数的计数自然就是答案。

- **时间 / 空间复杂度**  
  - 对每个查询我们都要 **完整遍历** 一遍路径。最坏情况下路径长达 `n‑1`，所以一次查询是 `O(n)`。  
  - 有 `q` 条查询，整体时间是 `O(n·q)`。  
  - 只需要存图和一次遍历的临时队列，空间 `O(n)`。  
  - 用大白话说：如果树有 10 万个节点，查询也有 10 万条，暴力解相当于 **10 万 × 10 万 次遍历**，根本跑不完。

#### 代码（Python）

```python
from collections import deque
MOD = 10**9 + 7

def brute_force(edges, queries):
    n = len(edges) + 1
    # 建图：邻接表
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def path_length(u, v):
        """返回 u 与 v 之间的边数（路径长度），若 u==v 返回 0"""
        if u == v:
            return 0
        # BFS 找最短路径（树里唯一的路径）
        visited = [False] * (n + 1)
        q = deque([(u, 0)])          # (当前节点, 已走的边数)
        visited[u] = True
        while q:
            cur, d = q.popleft()
            if cur == v:
                return d
            for nxt in graph[cur]:
                if not visited[nxt]:
                    visited[nxt] = True
                    q.append((nxt, d + 1))
        return -1   # 永远不会到这里，树保证连通

    ans = []
    for u, v in queries:
        L = path_length(u, v)          # 路径上的边数
        if L == 0:                     # 同一个点，路径权重为 0（偶数），没有合法方案
            ans.append(0)
        else:
            # 每条边有 2 种取值，奇数个 1 的组合数是 2^{L-1}
            ways = pow(2, L - 1, MOD)
            ans.append(ways)
    return ans
```

> **关键行解释**  
> - `graph[u].append(v)` / `graph[v].append(u)`：把一条路画进地图，两头都能看到。  
> - `pow(2, L - 1, MOD)`：`2^{L-1}` 表示“把 L 条路中任意挑选奇数条装上 1，剩下装上 2”，用 Python 的快速幂直接算模。

#### 复杂度

- **时间复杂度**：`O(n·q)`  
  - 每条查询最坏要遍历 `n` 条边。  
  - 用大白话说，就是“树的规模 × 查询的数量”，会超时。

- **空间复杂度**：`O(n)`  
  - 只存图和一次 BFS 的临时数组，和查询数量无关。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈在于每次都要重新走一遍路径**。树的结构决定了两点之间的距离（边数）可以**提前算好**，查询时只要把这个距离拿出来，用公式直接得到答案。

关键观察：

1. **权重奇偶性**  
   - 权重 1 为 **奇数**，权重 2 为 **偶数**。  
   - 路径总和的奇偶性，只取决于**有多少条边被赋值为 1** 的奇偶性。  
   - 对长度为 `L` 的路径，所有 `2^L` 种赋值中，恰好一半（`2^{L-1}`）会出现奇数个 1（因为把任意一条边的取值翻转，奇偶性就会翻转，形成配对）。  

2. **只需要路径长度**  
   - 只要知道 `L = dist(u, v)`（两点之间的边数），答案就是  
     ```
     if L == 0: 0          # 同一点，和为 0（偶数）
     else:      2^{L-1} (mod 1e9+7)
     ```
   - 所以核心任务是**快速求两点距离**。

3. **利用 LCA（最近公共祖先）**  
   - 在根为 1 的树里，`dist(u, v) = depth[u] + depth[v] - 2 * depth[lca(u, v)]`。  
   - `depth[x]` 是根到 `x` 的边数。  
   - `lca(u, v)` 可以用**二进制提升（binary lifting）**在 `O(log n)` 时间内求出。  
   - 预处理时我们为每个节点保存 `2^k` 级父亲（`up[node][k]`），相当于在树上装了“跳跃楼梯”，一次跳可以跨越 `2^k` 条边。

4. **预计算 2 的幂**  
   - `pow2[i] = 2^i mod MOD`（`i` 到 `n`），这样查询时只需要一次数组访问 `pow2[L-1]`。

**整体流程**  

| 步骤 | 说明 |
|------|------|
| 1️⃣ 建图 + DFS | 从根 1 出发，得到每个节点的深度 `depth`，以及 `up[node][0]`（直接父亲）。 |
| 2️⃣ 二进制提升 | 对每个 `k = 1 … LOG`（`LOG = ceil(log2 n)`），`up[node][k] = up[ up[node][k‑1] ][k‑1]`，相当于把 “跳 2^{k-1} 步的父亲” 再跳一次。 |
| 3️⃣ 预计算 2 的幂 | `pow2[i] = (pow2[i‑1] * 2) % MOD`，`i` 从 1 到 `n`。 |
| 4️⃣ 处理每个查询 | 使用二进制提升求 `lca(u, v)`，算出 `L`，返回 `0`（`L==0`）或 `pow2[L-1]`。 |

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(2 * 10**5)

MOD = 10**9 + 7

def number_of_ways(edges, queries):
    n = len(edges) + 1
    LOG = (n).bit_length()          # 足够大的 2 的幂次，等价于 ceil(log2 n)

    # ---------- 1. 建图 ----------
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # ---------- 2. DFS 求深度和第 0 层父亲 ----------
    depth = [0] * (n + 1)
    up = [[0] * LOG for _ in range(n + 1)]   # up[node][k] = 2^k 级父亲

    def dfs(u, p):
        up[u][0] = p
        for v in graph[u]:
            if v == p:
                continue
            depth[v] = depth[u] + 1
            dfs(v, u)

    dfs(1, 1)    # 根的父亲设为自己，方便后面的跳

    # ---------- 3. 二进制提升 ----------
    for k in range(1, LOG):
        for v in range(1, n + 1):
            up[v][k] = up[ up[v][k-1] ][k-1]

    # ---------- 4. 预计算 2 的幂 ----------
    pow2 = [1] * (n + 1)          # pow2[i] = 2^i (mod MOD)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD

    # ---------- 5. LCA 辅助函数 ----------
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # 把 a 提升到和 b 同深度
        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[a][bit]
            diff >>= 1
            bit += 1
        if a == b:
            return a
        # 同时向上跳，找到第一次不相同的祖先
        for k in range(LOG-1, -1, -1):
            if up[a][k] != up[b][k]:
                a = up[a][k]
                b = up[b][k]
        return up[a][0]

    # ---------- 6. 处理查询 ----------
    ans = []
    for u, v in queries:
        if u == v:
            ans.append(0)                # 路径长度为 0，和为 0（偶数）
            continue
        anc = lca(u, v)
        L = depth[u] + depth[v] - 2 * depth[anc]   # 边数
        ans.append(pow2[L-1])          # 2^{L-1} (mod MOD)
    return ans
```

> **关键行解释**  
> - `LOG = (n).bit_length()`：把 `n` 的二进制位数算出来，保证我们能跳到最高的祖先。  
> - `up[v][k] = up[ up[v][k-1] ][k-1]`：把“先跳 `2^{k-1}` 步再跳 `2^{k-1}` 步”合成“一次跳 `2^k` 步”。  
> - `diff & 1` 与 `bit` 循环：把 `a` 按位向上提升，使它和 `b` 同深度。  
> - `pow2[L-1]`：直接拿预先算好的 `2^{L-1}`，不需要再调用慢速的 `pow`。

#### 复杂度

- **时间复杂度**  
  - 预处理：DFS `O(n)` + 二进制提升 `O(n·log n)`。  
  - 每条查询：LCA `O(log n)`，其余 `O(1)`。  
  - 总体 `O((n + q)·log n)`。  
  - 与暴力解相比，**从每条查询遍历整棵树降到只看几层父亲**，快了几个数量级。

- **空间复杂度**  
  - `graph`、`depth`、`up`、`pow2` 共占 `O(n·log n)`（`up` 表是最大的）。  
  - 对 10⁵ 的规模，`log n ≤ 17`，完全在内存可接受范围内。  

---

## 心得

- **核心技巧**：把“路径权重奇偶性”转化为“路径长度的奇偶性”，进而只需**距离**而不是具体的权重分配。  
- **适用的题型**  
  1. 只关心路径上**奇偶/模 2**属性的题目（如 “路径异或为 1 的方案数”。）  
  2. 需要快速求树上两点**距离或 LCA**的题目（如 “树上查询距离之和”。）  
- **一句话总结解题钥匙**：**奇偶性只看 1 的个数 → 只要路径长度 → 用 LCA 快速算距离**。

---

## 反思

- **第一反应**：看到“每条边只能是 1 或 2”，立刻想到“二进制”。于是想把所有可能枚举出来，却忽略了**奇偶性只与 1 的个数有关**。  
- **最容易踩的坑**  
  - **路径长度为 0**（查询的两个节点相同）时，答案必须是 0，不能直接套公式 `2^{−1}`。  
  - **模运算**：`2^{L-1}` 需要对 `1e9+7` 取模，直接用 `pow` 会超时，预计算幂更快。  
  - **LCA 实现细节**：提升时要先把深度对齐，否则会跳到错误的祖先。  
- **下次遇到类似题**：第一步先思考**“属性到底取决于哪些元素”**（这里是 1 的个数），再判断**是否可以只用距离或层次信息**，最后决定是否需要 LCA、二进制提升等**预处理**手段。