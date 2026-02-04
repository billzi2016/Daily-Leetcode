# #3515. 加权树中的最短路径 / Shortest Path in a Weighted Tree

> 难度：困难 · 标签：Array、Tree、Depth-First Search、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/shortest-path-in-a-weighted-tree/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an undirected, weighted tree rooted at node 1 with n nodes numbered from 1 to n. This is represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi, wi] indicates an undirected edge from node ui to vi with weight wi.
You are also given a 2D integer array queries of length q, where each queries[i] is either:
Return an integer array answer, where answer[i] is the shortest path distance from node 1 to x for the ith query of [2, x].

**Examples**

**Example 1:**

```
Input: n = 2, edges = [[1,2,7]], queries = [[2,2],[1,1,2,4],[2,2]]
Output: [7,4]
Explanation:
```

**Example 2:**

```
Input: n = 3, edges = [[1,2,2],[1,3,4]], queries = [[2,1],[2,3],[1,1,3,7],[2,2],[2,3]]
Output: [0,4,2,7]
Explanation:
```

**Example 3:**

```
Input: n = 4, edges = [[1,2,2],[2,3,1],[3,4,5]], queries = [[2,4],[2,3],[1,2,3,3],[2,2],[2,3]]
Output: [8,3,2,5]
Explanation:
```

**Constraints**

- 1 <= n <= 105
- edges.length == n - 1
- edges[i] == [ui, vi, wi]
- 1 <= ui, vi <= n
- 1 <= wi <= 104
- The input is generated such that edges represents a valid tree.
- 1 <= queries.length == q <= 105
- queries[i].length == 2 or 4

queries[i] == [1, u, v, w'] or,
queries[i] == [2, x]
1 <= u, v, x <= n
(u, v) is always an edge from edges.
1 <= w' <= 104
- queries[i] == [1, u, v, w'] or,
- queries[i] == [2, x]
- 1 <= u, v, x <= n
- (u, v) is always an edge from edges.
- 1 <= w' <= 104

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`，以及一棵以节点 `1` 为根的无向（undirected）、带权（weighted）树，树中共有 `n` 个节点，编号为 `1` 到 `n`。树通过长度为 `n‑1` 的二维数组 `edges` 描述，其中 `edges[i] = [u_i, v_i, w_i]` 表示一条连接节点 `u_i` 与 `v_i`、权重为 `w_i` 的无向边（edge）。  

同时给定一个长度为 `q` 的二维整数数组 `queries`，其中每个 `queries[i]` 为以下两种形式之一：

* **类型 1**：`[1, u, v, w']` —— 将原本权重为 `w` 的边 `(u, v)` 的权重更新为 `w'`。  
* **类型 2**：`[2, x]` —— 查询从根节点 `1` 到节点 `x` 的最短路径距离（shortest path distance）。

返回一个整数数组 `answer`，其中 `answer[i]` 为第 `i` 个 **类型 2** 查询的答案。

---

**示例 1**  
```text
Input: n = 2, edges = [[1,2,7]], queries = [[2,2],[1,1,2,4],[2,2]]
Output: [7,4]
Explanation:
第一次查询 `[2,2]` 要求根到节点 2 的最短路径，初始权重为 7，答案为 7。  
随后执行更新 `[1,1,2,4]`，将边 (1,2) 的权重改为 4。  
第二次查询 `[2,2]` 再次求根到节点 2 的最短路径，得到 4。
```

**示例 2**  
```text
Input: n = 3, edges = [[1,2,2],[1,3,4]], queries = [[2,1],[2,3],[1,1,3,7],[2,2],[2,3]]
Output: [0,4,2,7]
Explanation:
查询 `[2,1]` 的答案是根节点到自身的距离 0。  
查询 `[2,3]` 的答案为路径 1→3，权重 4。  
更新 `[1,1,3,7]` 把边 (1,3) 的权重改为 7。  
随后查询 `[2,2]` 得到 2，查询 `[2,3]` 得到 7。
```

**示例 3**  
```text
Input: n = 4, edges = [[1,2,2],[2,3,1],[3,4,5]], queries = [[2,4],[2,3],[1,2,3,3],[2,2],[2,3]]
Output: [8,3,2,5]
Explanation:
初始情况下，根到 4 的最短路径为 1→2→3→4，权重和为 2+1+5=8。  
根到 3 的最短路径为 1→2→3，权重和为 2+1=3。  
更新 `[1,2,3,3]` 把边 (2,3) 的权重改为 3。  
随后查询 `[2,2]` 得到 2，查询 `[2,3]` 得到 1→2→3 的新权重和 2+3=5。
```

---

**约束条件**  

- `1 <= n <= 10^5`  
- `edges.length == n - 1`  
- `edges[i] == [u_i, v_i, w_i]`  
- `1 <= u_i, v_i <= n`  
- `1 <= w_i <= 10^4`  
- 输入保证 `edges` 构成一棵有效的树（valid tree）。  
- `1 <= queries.length == q <= 10^5`  
- `queries[i].length == 2` 或 `4`  

`queries[i]` 为以下两种形式之一：

1. `[1, u, v, w']` —— 更新边 `(u, v)` 的权重为 `w'`。  
2. `[2, x]` —— 查询根节点 `1` 到节点 `x` 的最短路径距离。

其中：

- `1 <= u, v, x <= n`  
- `(u, v)` 必定是 `edges` 中存在的边。  
- `1 <= w' <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这棵树是 **有根** 的（根节点固定为 1），我们需要两类操作：

1. **修改一条边的权重**  
   输入 `[1, u, v, w']` 表示把原本连通 `u‑v` 的那条边的权重改成 `w'`。  
2. **查询根到某节点的最短路径长度**  
   输入 `[2, x]` 要求返回从根 `1` 到节点 `x` 的距离（因为树里只有唯一一条路径，所以最短路径就是这条唯一路径的权值之和）。

最直接的想法是：**每次修改后，重新遍历一次整棵树，重新算出每个节点到根的距离**。  
- 用 **邻接表**（list of lists）把树存起来。  
- 用一次 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 从根出发，累计路径权重，得到 `dist[i] = 根→i 的距离`。  
- 查询时直接返回 `dist[x]`。

> **类比**：邻接表就像一本“城市地图”，每个城市（节点）后面列出它直接相连的道路（相邻节点）和路程（权重）。DFS/BFS 就像让一个快递员从仓库（根）出发，记下送到每家店（节点）需要走的总路程。

**为什么正确**：树没有环，根到任意节点的路径唯一。只要遍历一次，把路径上所有边的权重加起来，就一定得到正确的距离。

**时间/空间分析**  

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 单次 **更新**（修改一条边）| `O(1)`（只改存的边权）| 只改一个数组里的数，几乎不耗时 |
| **整棵树重新遍历**| `O(n)` | 必须访问所有 `n` 个节点才能重新算出 `dist` |
| **查询**| `O(1)` | 直接读取 `dist[x]` |

因为 **每次更新后都要重新遍历**，若有 `q` 条查询/更新，最坏情况是 `q` 次遍历，时间复杂度 **`O(q·n)`**。  
在最坏的约束 `n, q ≤ 10⁵` 时，这会是 `10¹⁰` 次操作，远远超时。

空间上我们需要保存邻接表（`O(n)`）和 `dist` 数组（`O(n)`），总计 `O(n)`。

---

#### 代码（Python）

```python
from collections import defaultdict, deque

def brute_solution(n, edges, queries):
    # ---------- 建图 ----------
    g = defaultdict(list)          # 邻接表：节点 -> [(邻居, 权重)]
    edge_weight = {}                # (u,v) 有序对 -> 权重，方便更新
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
        edge_weight[tuple(sorted((u, v)))] = w

    # ---------- 计算根到每个节点的距离 ----------
    def recompute_dist():
        dist = [0] * (n + 1)        # 1-indexed，dist[0] 不用
        visited = [False] * (n + 1)
        q = deque([1])
        visited[1] = True
        while q:
            cur = q.popleft()
            for nxt, w in g[cur]:
                if not visited[nxt]:
                    visited[nxt] = True
                    dist[nxt] = dist[cur] + w
                    q.append(nxt)
        return dist

    dist = recompute_dist()
    ans = []

    # ---------- 处理查询 ----------
    for query in queries:
        if query[0] == 1:                     # 更新边权
            _, u, v, w_new = query
            key = tuple(sorted((u, v)))
            w_old = edge_weight[key]          # 旧权重
            if w_old == w_new:                # 权重未变，直接跳过
                continue
            edge_weight[key] = w_new
            # 同时在邻接表里改掉旧权重
            for idx, (node, _) in enumerate(g[u]):
                if node == v:
                    g[u][idx] = (v, w_new)
                    break
            for idx, (node, _) in enumerate(g[v]):
                if node == u:
                    g[v][idx] = (u, w_new)
                    break
            # 重新遍历整棵树，更新所有节点的距离
            dist = recompute_dist()
        else:                                 # 查询根到 x 的距离
            _, x = query
            ans.append(dist[x])
    return ans
```

> 关键行中文注释已在代码中给出，直接拷贝运行即可。

#### 复杂度

- **时间复杂度**：`O(q·n)`  
  每次更新后都要一次 `O(n)` 的遍历，查询是 `O(1)`。  
  用大白话说，就是“每次改动都要把全树重新算一遍”，在最坏情况下会非常慢。
- **空间复杂度**：`O(n)`  
  只用了邻接表、一个保存边权的字典以及 `dist` 数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次修改后都要遍历整棵树”**。  
其实我们可以利用树的 **层次结构**：  
- 当一条 **父子边** 的权重改变时，**只有这条边以下的子树**（即该边的**子树**）受到影响。  
- 对子树里的每个节点，它们到根的距离都要 **统一加上**（或减去）同一个 **增量**（新权重 - 旧权重）。

于是我们只需要 **快速定位** 这条边对应的子树在“树的线性序列”中的区间，并对这个区间做 **区间加** 操作；查询根到某节点的距离则是 **点查询**（取该节点对应位置的当前累计增量） 加上 **初始距离**。

实现步骤如下：

1. **一次 DFS 预处理**  
   - 计算每个节点 **初始到根的距离** `baseDist[i]`（使用原始权重）。  
   - 记录 **欧拉遍历（Euler Tour）** 的 **进入时间 `tin[i]`** 与 **退出时间 `tout[i]`**，并把节点按照进入顺序放进数组 `order`。  
   - 对于任意节点 `x`，它的子树恰好对应 `order[tin[x] … tout[x]]` 这段连续区间。  
   > 类比：把树“摊平”成一本书的章节目录，`tin` 是章节的起始页码，`tout` 是章节的结束页码，整本书的页码就是 `order`。

2. **数据结构：树状数组（Fenwick Tree）或线段树**  
   - 这里使用 **树状数组（Binary Indexed Tree，BIT）**，因为它支持 **区间加、点查询**（两次前缀和技巧）都在 `O(log n)`。  
   - BIT 维护一个 **增量数组 `add[]`**，初始全为 0。每次对某子树做 **加 delta**，就在 `[tin, tout]` 区间做 “区间加”。查询时只需要读取 `add[tin[x]]`（点查询），再加上 `baseDist[x]` 就得到最新的根到 `x` 的距离。

3. **处理两类查询**  

   - **更新 `[1, u, v, w']`**  
     - 首先找出 **哪一个是父节点，哪一个是子节点**。因为树是根向下的，我们可以在 DFS 时保存每个节点的父亲 `parent[i]`。  
     - 假设 `parent[child] == parentNode`（`child` 为子节点），则这条边的旧权重是 `old = edge_weight[(u,v)]`。  
     - 计算增量 `delta = w' - old`。  
     - 把 `delta` 加到 **子节点 `child` 的整棵子树**：`BIT.range_add(tin[child], tout[child], delta)`。  
     - 同时更新 `edge_weight[(u,v)] = w'`（以后可能再次修改）。

   - **查询 `[2, x]`**  
     - `ans = baseDist[x] + BIT.point_query(tin[x])`。  
     - 直接返回即可。

4. **复杂度对比**  
   - 预处理一次 DFS：`O(n)`。  
   - 每次 **更新** 或 **查询**：`O(log n)`（BIT 的单次操作）。  
   - 整体 `O((n+q)·log n)`，在 `10⁵` 规模下轻松跑完。

#### 核心数据结构细讲

- **欧拉遍历（Euler Tour）**  
  把树展开成一个序列。对每个节点记录进入时间 `tin`（第一次访问时的序号）和退出时间 `tout`（离开时的序号）。  
  - **性质**：`x` 的子树节点恰好是 `tin[x] … tout[x]` 这一段连续区间。  
  - 这让我们可以把“子树”转换为“数组区间”，从而使用线段树或 BIT 进行区间操作。

- **树状数组（BIT）**  
  - 支持 **前缀和** 查询 `sum(i)`（`i` 前所有增量的和）`O(log n)`。  
  - 为实现 **区间加**，我们维护两个 BIT，或使用“差分”技巧：  
    - `add(l, delta)` → 在 `l` 位置加 `delta`  
    - `add(r+1, -delta)` → 在 `r+1` 位置减 `delta`  
    - 查询点 `i` 时 `prefix_sum(i)` 就是所有区间加的累计值。  
  - 代码里直接封装成 `range_add(l, r, delta)` 与 `point_query(i)`。

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(300000)

# ---------- BIT（树状数组） ----------
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)          # 1-indexed

    def _add(self, idx, delta):
        """在 idx 位置加 delta（单点更新）"""
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def range_add(self, l, r, delta):
        """对闭区间 [l, r] 加 delta"""
        self._add(l, delta)
        self._add(r + 1, -delta)

    def point_query(self, idx):
        """查询 idx 位置的累计值（前缀和）"""
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx
        return s


# ---------- 主函数 ----------
def shortest_path_weighted_tree(n, edges, queries):
    # 1. 建图 + 保存原始边权
    g = [[] for _ in range(n + 1)]
    edge_weight = {}                     # (min(u,v), max(u,v)) -> weight
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
        edge_weight[(min(u, v), max(u, v))] = w

    # 2. DFS 预处理：tin, tout, parent, baseDist, order
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    parent = [0] * (n + 1)
    baseDist = [0] * (n + 1)            # 初始根到每个节点的距离
    order = []                          # 按进入时间排列的节点序列
    timer = 0

    def dfs(u, p):
        nonlocal timer
        timer += 1
        tin[u] = timer
        order.append(u)
        parent[u] = p
        for v, w in g[u]:
            if v == p:
                continue
            baseDist[v] = baseDist[u] + w
            dfs(v, u)
        tout[u] = timer

    dfs(1, 0)                           # 以根 1 为起点

    # 3. BIT 用于维护子树的增量
    bit = BIT(n)

    # 4. 处理查询
    ans = []
    for q in queries:
        if q[0] == 1:                     # 更新边权
            _, u, v, w_new = q
            key = (min(u, v), max(u, v))
            w_old = edge_weight[key]
            if w_old == w_new:            # 没变直接跳过
                continue
            delta = w_new - w_old
            edge_weight[key] = w_new

            # 判断哪一个是子节点（父子关系一定存在）
            if parent[u] == v:            # v 是 u 的父亲 → u 为子节点
                child = u
            else:                         # u 是 v 的父亲 → v 为子节点
                child = v

            # 对子节点所在的子树区间加 delta
            bit.range_add(tin[child], tout[child], delta)

        else:                             # 查询根到 x 的距离
            _, x = q
            cur = baseDist[x] + bit.point_query(tin[x])
            ans.append(cur)

    return ans
```

> 代码要点已加中文注释，直接复制到 Python 环境即可运行。  

---

#### 复杂度

- **时间复杂度**  
  - 预处理 DFS：`O(n)`  
  - 每条查询（更新或查询）：`O(log n)`  
  - 总计 `O((n + q)·log n)`。  
  与暴力的 `O(q·n)` 相比，**把每次遍历整棵树的成本降到了对数级**，在 `10⁵` 规模下可以在毫秒级完成。

- **空间复杂度**  
  - 图的邻接表、父亲数组、`tin/tout`、`baseDist`、`order`：`O(n)`  
  - BIT：`O(n)`  
  - 总计 `O(n)`，只用了线性额外空间。

---

## 心得

- **核心技巧**：把树通过欧拉遍历 “摊平”，子树对应数组的连续区间；再用 **树状数组**（或线段树）实现 **区间加 + 点查询**。  
- **适用场景**：  
  1. **树上子树加权**（如 “给子树所有节点加一个值”）  
  2. **动态树上路径查询**（配合重链剖分可以做路径上的区间操作）  
  3. **树上区间统计**（如 “子树中某种颜色的节点数量”）  
- **一句话总结解题钥匙**：  
  *“把树的层次结构映射到一维数组，用差分+前缀和快速维护子树的整体变化”。*

---

## 反思

- **第一反应**：看到“根到某节点的最短路径”立刻想到 BFS/DFS，看到“边权可变”就想到每次重新遍历。  
- **最容易踩的坑**  
  1. **判断父子方向错误**：更新时必须找出哪一端是子节点，否则把错误区间加了 delta。  
  2. **欧拉序号的 1‑index 与 BIT 实现不匹配**：BIT 是 1‑based，`tin` 也要从 1 开始，否则会越界或错位。  
  3. **忘记在 BIT 中做区间加的差分**：直接对 `[l, r]` 调 `add` 会导致错误的累计值。  
- **下次类似题目第一步**：先思考 “**有什么结构可以把子树变成连续区间**”，如果有，往往可以用 **BIT/线段树** 把子树操作降到 `O(log n)`。  

祝你编码愉快 🎉