# #2846. 树上最小边权平衡查询 / Minimum Edge Weight Equilibrium Queries in a Tree

> 难度：困难 · 标签：Array、Tree、Graph、Strongly Connected Component · [LeetCode 链接](https://leetcode.com/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ui, vi, wi] indicates that there is an edge between nodes ui and vi with weight wi in the tree.
You are also given a 2D integer array queries of length m, where queries[i] = [ai, bi]. For each query, find the minimum number of operations required to make the weight of every edge on the path from ai to bi equal. In one operation, you can choose any edge of the tree and change its weight to any value.
Note that:
Return an array answer of length m where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: n = 7, edges = [[0,1,1],[1,2,1],[2,3,1],[3,4,2],[4,5,2],[5,6,2]], queries = [[0,3],[3,6],[2,6],[0,6]]
Output: [0,0,1,3]
Explanation: In the first query, all the edges in the path from 0 to 3 have a weight of 1. Hence, the answer is 0.
In the second query, all the edges in the path from 3 to 6 have a weight of 2. Hence, the answer is 0.
In the third query, we change the weight of edge [2,3] to 2. After this operation, all the edges in the path from 2 to 6 have a weight of 2. Hence, the answer is 1.
In the fourth query, we change the weights of edges [0,1], [1,2] and [2,3] to 2. After these operations, all the edges in the path from 0 to 6 have a weight of 2. Hence, the answer is 3.
For each queries[i], it can be shown that answer[i] is the minimum number of operations needed to equalize all the edge weights in the path from ai to bi.
```

**Example 2:**

```
Input: n = 8, edges = [[1,2,6],[1,3,4],[2,4,6],[2,5,3],[3,6,6],[3,0,8],[7,0,2]], queries = [[4,6],[0,4],[6,5],[7,4]]
Output: [1,2,2,3]
Explanation: In the first query, we change the weight of edge [1,3] to 6. After this operation, all the edges in the path from 4 to 6 have a weight of 6. Hence, the answer is 1.
In the second query, we change the weight of edges [0,3] and [3,1] to 6. After these operations, all the edges in the path from 0 to 4 have a weight of 6. Hence, the answer is 2.
In the third query, we change the weight of edges [1,3] and [5,2] to 6. After these operations, all the edges in the path from 6 to 5 have a weight of 6. Hence, the answer is 2.
In the fourth query, we change the weights of edges [0,7], [0,3] and [1,3] to 6. After these operations, all the edges in the path from 7 to 4 have a weight of 6. Hence, the answer is 3.
For each queries[i], it can be shown that answer[i] is the minimum number of operations needed to equalize all the edge weights in the path from ai to bi.
```

**Constraints**

- 1 <= n <= 104
- edges.length == n - 1
- edges[i].length == 3
- 0 <= ui, vi < n
- 1 <= wi <= 26
- The input is generated such that edges represents a valid tree.
- 1 <= queries.length == m <= 2 * 104
- queries[i].length == 2
- 0 <= ai, bi < n

---

## 题目（中文翻译）

给定一棵无向树，节点编号为 `0` 到 `n - 1`。  
你会得到整数 `n` 和一个长度为 `n - 1` 的二维整数数组 `edges`，其中 `edges[i] = [ui, vi, wi]` 表示在节点 `ui` 与 `vi` 之间存在一条权重为 `wi` 的边（edge）。  
同时，还会得到长度为 `m` 的二维整数数组 `queries`，其中 `queries[i] = [ai, bi]` 表示一次查询。

对于每个查询，求使路径上所有边的权重相等所需的最少操作次数。一次操作可以任选树中的任意一条边，将其权重改为任意值。

返回长度为 `m` 的数组 `answer`，其中 `answer[i]` 为第 `i` 条查询的答案。

---

### 示例

**示例 1**

```
Input: n = 7, edges = [[0,1,1],[1,2,1],[2,3,1],[3,4,2],[4,5,2],[5,6,2]],
       queries = [[0,3],[3,6],[2,6],[0,6]]
Output: [0,0,1,3]
Explanation:
- 第一次查询，路径 `0 → 3` 上的所有边权均为 `1`，因此答案为 `0`。
- 第二次查询，路径 `3 → 6` 上的所有边权均为 `2`，因此答案为 `0`。
- 第三次查询，需要将边 `[2,3]` 的权重改为 `2`（或将其他边改为 `1`），只需一次操作，答案为 `1`。
- 第四次查询，路径 `0 → 6` 上的边权分别为 `1,1,1,2,2,2`。最少需要把其中的三条权重改为同一值，答案为 `3`。
```

**示例 2**

```
Input: n = 8, edges = [[1,2,6],[1,3,4],[2,4,6],[2,5,3],[3,6,6],[3,0,8],[7,0,2]],
       queries = [[4,6],[0,4],[6,5],[7,4]]
Output: [1,2,2,3]
Explanation:
- 第一次查询，将边 `[1,3]` 的权重改为 `6`，此后路径 `4 → 6` 上的所有边权均为 `6`，答案为 `1`。
- 第二次查询，需要把边 `[0,3]` 和 `[1,3]` 的权重都改为 `6`，共计 `2` 次操作，答案为 `2`。
- 第三次查询，同理需要 `2` 次操作，使路径 `6 → 5` 上的所有边权相等，答案为 `2`。
- 第四次查询，最少需要 `3` 次操作才能使路径 `7 → 4` 上的边权统一，答案为 `3`。
```

---

### 约束条件

- `1 <= n <= 10^4`
- `edges.length == n - 1`
- `edges[i].length == 3`
- `0 <= ui, vi < n`
- `1 <= wi <= 26`
- 输入保证 `edges` 构成一棵合法的树（tree）。
- `1 <= queries.length == m <= 2 * 10^4`
- `queries[i].length == 2`
- `0 <= ai, bi < n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把每一次查询的路径全部枚举出来**，然后统计这条路径上每一种边权出现了多少次，取出现次数最多的那种边权 `maxFreq`，把其余的边全部改成这个权值即可。  

- **数据结构**  
  - **邻接表**：把树存成 `graph[u] = [(v, w), …]`。这就像我们把每条路（边）和路的宽度（权值）记在一本“城市地图”里。  
  - **DFS / BFS**：用一次深度优先搜索（或广度优先搜索）从 `a` 出发找到 `b`，顺便把经过的边权收集到列表里。想象我们从家走到朋友家，一路上记下每条路的宽度。  
  - **计数数组**：因为权值只在 `[1, 26]` 之间，开一个长度 `27` 的数组 `cnt[w]`，下标 `w` 直接对应权值 `w` 的出现次数。数组就像字典的“查字典”，直接把词（权值）对应到页码（出现次数）。  

- **正确性**  
  只要把路径上所有边都改成同一个权值，最终的权值一定是**出现次数最多的那个**（因为改的次数最少）。遍历所有可能的权值并取最小的改动次数，必然得到最优答案。  

- **复杂度分析（大白话）**  
  - 对每个查询我们都要 **遍历一次路径**。最坏情况下路径长达 `n‑1`（树是一条链），所以一次查询的时间是 `O(n)`。  
  - 有 `m` 条查询，总时间是 `O(m·n)`。如果 `n = 10⁴，m = 2·10⁴`，最坏会是 `2·10⁸` 次操作，明显会超时。  
  - 额外空间只需要保存邻接表 (`O(n)`) 和计数数组 (`O(1)`，因为权值上限是常数 26），所以是 `O(n)`。  

#### 代码（Python）  

```python
from collections import defaultdict, deque
from typing import List

def brute_min_operations(n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
    # ---------- 建图 ----------
    graph = defaultdict(list)                     # 邻接表：node -> [(neighbor, weight), ...]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # ---------- 求单条查询的答案 ----------
    def path_weights(a: int, b: int) -> List[int]:
        """返回从 a 到 b 路径上所有边的权值（顺序无关紧要）"""
        parent = {a: (-1, -1)}                    # node -> (prev_node, weight_from_prev)
        q = deque([a])
        while q:
            cur = q.popleft()
            if cur == b:                          # 找到目标，结束 BFS
                break
            for nxt, w in graph[cur]:
                if nxt not in parent:             # 未访问过
                    parent[nxt] = (cur, w)
                    q.append(nxt)

        # 逆向回溯得到路径上的权值
        weights = []
        node = b
        while node != a:
            prev, w = parent[node]
            weights.append(w)
            node = prev
        return weights

    ans = []
    for a, b in queries:
        wlist = path_weights(a, b)                # 暴力取出路径权值
        # 统计每个权值出现次数，权值范围只有 1~26
        cnt = [0] * 27
        for w in wlist:
            cnt[w] += 1
        max_freq = max(cnt)                       # 出现最多的权值次数
        # 需要改的边数 = 路径总长度 - 已经相同的最大次数
        ans.append(len(wlist) - max_freq)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - “一次查询遍历整条路径” → 最差 `n` 条边；`m` 次查询累加。  
  - 用大白话说，就是“每次都把整棵树走一遍”。  

- **空间复杂度**：`O(n)`  
  - 邻接表存 `n‑1` 条边，额外的 `parent`、`cnt` 等都是常数级或与节点数线性相关。  



---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要重新遍历路径**。如果我们事先把**从根到任意节点的边权信息**记下来，那么两点之间的路径信息就可以**通过数学公式**瞬间算出来，而不必再走一遍。

**核心工具**  

1. **把树随意选一个根**（比如 0），把每个节点视为“从根出发的子树”。  
2. **前缀频率** `freq[node][w]`：从根到 `node`（包括根到 `node` 这条路上）每种权值 `w` 出现了多少次。  
   - 想象我们在根出发的旅途中，每看到一种路宽度，就在对应的“记事本”上打一个勾。  
3. **二分倍增（Binary Lifting）** 求 **最近公共祖先（LCA）**。  
   - LCA 就像两个人从不同城市出发，想找最近的共同祖辈（最近的交叉点）。  
   - 通过预处理 `up[k][v]`（第 `2^k` 级父亲）和 `depth[v]`，我们可以在 `O(log n)` 时间内找出任意两点的 LCA。  

**路径频率公式**  

对任意权值 `w`，路径 `a → b` 上出现的次数 =  

```
freq[a][w] + freq[b][w] - 2 * freq[lca][w]
```

因为 `freq[lca][w]` 包含了从根到 LCA 的所有边，而这段在 `a` 和 `b` 的路径中被算了两次，需要减掉两次。  

**求答案的步骤**  

1. 预处理一次：  
   - `depth`、`up`（二分父亲表）  
   - `freq[node]`（长度 27 的数组）  
2. 对每个查询 `(a, b)`：  
   - 用二分倍增得到 `l = LCA(a, b)`（`O(log n)`）  
   - 计算路径长度 `dist = depth[a] + depth[b] - 2*depth[l]`（即边数）  
   - 对所有可能的权值 `w = 1..26`，用公式算出现次数，取最大值 `maxFreq`  
   - 答案 = `dist - maxFreq`（其余的边都要改）  

因为权值只有 26 种，遍历它们是常数时间。整体每条查询的复杂度是 `O(log n)`，整体 `O((n+m)·log n)`，在题目限制下轻松 AC。

#### 代码（Python）  

```python
from collections import defaultdict, deque
from typing import List

LOG = 15          # 因为 n <= 1e4，2^14 = 16384 > 1e4，取 15 足够

def min_operations(n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
    # ---------- 1. 建图 ----------
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # ---------- 2. 预处理：depth、up、freq ----------
    depth = [0] * n                     # depth[root] = 0
    up = [[-1] * n for _ in range(LOG)]  # up[k][v] = 2^k 父亲
    freq = [[0] * 27 for _ in range(n)]   # freq[v][w] = 从根到 v，权值 w 出现次数

    root = 0
    stack = [(root, -1, 0)]            # (node, parent, edge_weight_from_parent)
    while stack:
        node, parent, w = stack.pop()
        up[0][node] = parent           # 直接父亲
        if parent != -1:
            depth[node] = depth[parent] + 1
            # 继承父亲的频率数组，再加上本条进来的边权
            freq[node] = freq[parent][:]   # 复制一份
            freq[node][w] += 1
        else:
            # 根节点没有进来的边
            freq[node] = [0] * 27

        for nxt, nw in graph[node]:
            if nxt == parent:
                continue
            stack.append((nxt, node, nw))

    # 二进制提升表
    for k in range(1, LOG):
        for v in range(n):
            if up[k-1][v] != -1:
                up[k][v] = up[k-1][up[k-1][v]]

    # ---------- 3. LCA  ----------
    def lca(a: int, b: int) -> int:
        if depth[a] < depth[b]:
            a, b = b, a
        # 把 a 提升到和 b 同深度
        diff = depth[a] - depth[b]
        for k in range(LOG):
            if diff >> k & 1:
                a = up[k][a]

        if a == b:
            return a

        # 同时向上跳，找到第一条不同的边
        for k in reversed(range(LOG)):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return up[0][a]   # 父亲就是 LCA

    # ---------- 4. 处理每个查询 ----------
    ans = []
    for a, b in queries:
        anc = lca(a, b)
        # 路径边数（长度）
        dist = depth[a] + depth[b] - 2 * depth[anc]

        # 统计每种权值在路径上的出现次数
        max_freq = 0
        for w in range(1, 27):
            cnt = freq[a][w] + freq[b][w] - 2 * freq[anc][w]
            if cnt > max_freq:
                max_freq = cnt

        ans.append(dist - max_freq)   # 需要改的边数
    return ans
```

> **代码要点解释**  
> 1. **`freq[node] = freq[parent][:]`**：复制父亲的频率数组，相当于在“记事本”上把之前的勾全部搬过去，然后再在对应的权值上再加一勾。  
> 2. **二分提升**：`up[k][v]` 表示节点 `v` 往上走 `2^k` 步后所在的节点。这样可以在 `O(log n)` 时间把两个节点提升到同一深度，再一起向上找公共祖先。  
> 3. **`dist`**：因为树中每条边权都算作一次操作的对象，路径长度即为需要检查的边数。  

#### 复杂度  

- **时间复杂度**  
  - 预处理：`O(n·log n)`（二分表） + `O(n·W)`（复制频率数组，`W=26` 为常数） → 实际是 `O(n·log n)`。  
  - 每条查询：`O(log n)`（求 LCA） + `O(W)`（遍历 26 种权值） → `O(log n)`。  
  - 总计：`O((n + m)·log n)`。  
  - 用大白话说，就是“先把树的所有信息记好，之后每次只看几秒钟”。  

- **空间复杂度**  
  - `up` 表：`LOG·n` 大约 `15·10⁴ ≈ 1.5×10⁵`，属于 `O(n·log n)`。  
  - `freq` 表：`n·27`，也是 `O(n)`（因为 27 是常数）。  
  - 其余邻接表等也是 `O(n)`。  
  - 合计 `O(n·log n)` 的内存，完全在题目限制范围内。  



---  



## 心得  

- **核心技巧**：利用 **前缀频率 + LCA** 把路径上的信息压缩到两个点的属性上，避免每次都遍历路径。  
- **适用的题型**（类似思路）：  
  1. “路径上颜色出现次数最多” / “路径上节点值的众数” 类问题。  
  2. “两点之间权值之和 / 最大权值” 等需要快速求路径聚合的信息。  
  3. “树上区间查询” 之类的离线或在线方案（如树状数组+Euler Tour）。  
- **一句话总结解题钥匙**：**把“路径上所有边的信息”转化为“根到两点的前缀信息的线性组合”，配合 LCA 把查询压到 `O(log n)`**。  



---  



## 反思  

- **第一反应**：看到“把路径上所有边改成相同权值”，第一时间想到**枚举路径、统计出现次数**，于是写出了暴力解。  
- **最容易踩的坑**  
  1. **忘记减掉 LCA 那条边的两次计数**，导致频率公式写成 `freq[a]+freq[b]-freq[lca]`（少了一个 `*2`）。  
  2. **根节点的频率数组初始化**：根没有入边，需要全 0，否则会误计。  
  3. **二分提升的层数**：`LOG` 取值不够大导致数组越界。  
- **下次遇到同类题的第一步**：**先思考能否把路径信息写成“前缀-前缀”形式**，如果可以，就立刻考虑 LCA + 前缀统计；如果不行，再回头考虑暴力或 Heavy‑Light 分解等更高级的方案。