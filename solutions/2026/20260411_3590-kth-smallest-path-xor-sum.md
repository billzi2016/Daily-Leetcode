# #3590. 第 K 小路径异或和 / Kth Smallest Path XOR Sum

> 难度：困难 · 标签：Array、Tree、Depth-First Search、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-path-xor-sum/)

---

## 题目（英文原版）

**Description**

You are given an undirected tree rooted at node 0 with n nodes numbered from 0 to n - 1. Each node i has an integer value vals[i], and its parent is given by par[i].
The path XOR sum from the root to a node u is defined as the bitwise XOR of all vals[i] for nodes i on the path from the root node to node u, inclusive.
You are given a 2D integer array queries, where queries[j] = [uj, kj]. For each query, find the kjth smallest distinct path XOR sum among all nodes in the subtree rooted at uj. If there are fewer than kj distinct path XOR sums in that subtree, the answer is -1.
Return an integer array where the jth element is the answer to the jth query.
In a rooted tree, the subtree of a node v includes v and all nodes whose path to the root passes through v, that is, v and its descendants.

**Examples**

**Example 1:**

```
Input: par = [-1,0,0], vals = [1,1,1], queries = [[0,1],[0,2],[0,3]]
Output: [0,1,-1]
Explanation:

Path XORs:
Subtree of 0 : Subtree rooted at node 0 includes nodes [0, 1, 2] with Path XORs = [1, 0, 0] . The distinct XORs are [0, 1] .
Queries:
Output: [0, 1, -1]
```

**Example 2:**

```
Input: par = [-1,0,1], vals = [5,2,7], queries = [[0,1],[1,2],[1,3],[2,1]]
Output: [0,7,-1,0]
Explanation:

Path XORs:
Subtrees and Distinct Path XORs:
Queries:
Output: [0, 7, -1, 0]
```

**Constraints**

- 1 <= n == vals.length <= 5 * 104
- 0 <= vals[i] <= 105
- par.length == n
- par[0] == -1
- 0 <= par[i] < n for i in [1, n - 1]
- 1 <= queries.length <= 5 * 104
- queries[j] == [uj, kj]
- 0 <= uj < n
- 1 <= kj <= n
- The input is generated such that the parent array par represents a valid tree.

---

## 题目（中文翻译）

你得到一棵以节点 0 为根（rooted at node 0）的无向树（undirected tree），该树有 n 个节点，编号为 0 到 n‑1。每个节点 i 有一个整数值 vals[i]，其父节点由数组 par[i] 给出。

从根节点到某节点 u 的路径异或和（path XOR sum）定义为路径上所有节点 i 的 vals[i] 进行按位异或（bitwise XOR）的结果，路径包括根节点和节点 u 本身。

给定一个二维整数数组 queries，其中 queries[j] = [uj, kj]。对于每个查询，需要在以 uj 为根的子树（subtree）中，找出第 kj 小的 **不同的**（distinct）路径异或和。如果该子树中不同的路径异或和数量少于 kj，答案为 -1。

返回一个整数数组，数组的第 j 个元素即第 j 个查询的答案。

在根树中，节点 v 的子树包括 v 本身以及所有从根到这些节点的路径必经 v 的后代节点。

---

### 示例 1
```text
Input: par = [-1,0,0], vals = [1,1,1], queries = [[0,1],[0,2],[0,3]]
Output: [0,1,-1]
Explanation:
路径异或和：
- 子树 0：以节点 0 为根的子树包含节点 [0,1,2]，对应的路径异或和为 [1,0,0]。不同的异或和为 [0,1]。
查询结果：
- 第 1 小 = 0
- 第 2 小 = 1
- 第 3 小不存在，返回 -1
```

### 示例 2
```text
Input: par = [-1,0,1], vals = [5,2,7], queries = [[0,1],[1,2],[1,3],[2,1]]
Output: [0,7,-1,0]
Explanation:
路径异或和：
- 子树 0：节点 [0,1,2] 的路径异或和为 [5,7,0]，不同的为 [0,5,7]。
- 子树 1：节点 [1,2] 的路径异或和为 [7,0]，不同的为 [0,7]。
- 子树 2：仅包含节点 [2]，路径异或和为 [0]。
查询结果：
- 对子树 0 第 1 小 → 0
- 对子树 1 第 2 小 → 7
- 对子树 1 第 3 小 → 不存在，返回 -1
- 对子树 2 第 1 小 → 0
```

---

### 约束条件
- `1 <= n == vals.length <= 5 * 10^4`
- `0 <= vals[i] <= 10^5`
- `par.length == n`
- `par[0] == -1`
- `0 <= par[i] < n`，对所有 `i` 属于 `[1, n - 1]`
- `1 <= queries.length <= 5 * 10^4`
- `queries[j] == [uj, kj]`
- `0 <= uj < n`
- `1 <= kj <= n`
- 输入保证数组 `par` 构成一棵合法的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每棵子树的所有节点的路径异或值都枚举出来**，然后去重、排序，最后取第 `k` 小。  
实现步骤如下：

1. 先用一次深度优先搜索（DFS）算出 **从根到每个节点的路径 XOR**，记为 `pref[u]`。  
   - 想象把树看成一条条通往每个城市的道路，`pref[u]` 就是把路上所有城市的“密码” `vals[i]` 用异或（XOR）连在一起得到的总密码。  
2. 对每一次查询 `[u, k]`，遍历整棵树，找出所有在 `u` 的子树里的节点 `v`（即 `v` 的祖先链中必然经过 `u`），把它们的 `pref[v]` 收集进一个列表。  
3. 对列表去重（把相同的 XOR 值合并成一个），再排序，最后检查是否至少有 `k` 个不同的值，若有则返回第 `k` 小，否则返回 `-1`。

> **为什么这一步是对的？**  
> - `pref[v]` 正好是题目定义的“根到节点 `v` 的路径 XOR”。  
> - 只要把子树里的所有 `pref` 收集起来，再做去重和排序，就能得到“子树中所有不同的路径 XOR 并按大小排列”。  
> - 第 `k` 小自然就是答案。

#### 代码（Python）

```python
from collections import defaultdict, deque

def kth_smallest_path_xor_brutal(par, vals, queries):
    n = len(vals)
    # 1. 建立邻接表（无向树）
    g = [[] for _ in range(n)]
    for i in range(1, n):
        p = par[i]
        g[p].append(i)
        g[i].append(p)

    # 2. 计算根到每个节点的路径 XOR（pref）
    pref = [0] * n          # pref[u] = XOR from root to u
    parent = [-1] * n
    stack = [(0, 0)]        # (node, xor_sofar)
    while stack:
        u, cur = stack.pop()
        pref[u] = cur ^ vals[u]
        for v in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            stack.append((v, pref[u]))

    # 3. 辅助函数：判断 v 是否在 u 的子树里（利用父指针向上走）
    def in_subtree(v, u):
        # 把树当成有向的（从根往下），只要向上走能碰到 u，就说明在子树里
        while v != -1 and v != u:
            v = parent[v]
        return v == u

    # 4. 逐个处理查询（最暴力的 O(n^2)）
    ans = []
    for u, k in queries:
        values = []
        for v in range(n):
            if in_subtree(v, u):
                values.append(pref[v])
        # 去重、排序
        distinct = sorted(set(values))
        if k <= len(distinct):
            ans.append(distinct[k - 1])
        else:
            ans.append(-1)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * q)`（最坏情况下每个查询都要遍历全部 `n` 个节点），在 `n = 5·10⁴`、`q = 5·10⁴` 时会达到 `2.5·10⁹` 步，显然会超时。  
  - 这里的 `O(n²)` 只是一种形象说法，表示“每次查询都要遍历整棵树”。  
- **空间复杂度**：`O(n)` 用来存 `pref`、`parent`、邻接表等。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在 **每次查询都要重新遍历整棵树**。如果我们能在一次 DFS 过程中 **把每个节点子树的所有路径 XOR 收集好**，那么查询就只需要在对应的集合里直接取第 `k` 小即可。

这正是 **“树上小到大合并（DSU on tree）”** 的典型场景：

1. **预处理**  
   - 同样先用一次 DFS 计算每个节点的 `pref[u]`（根到 `u` 的 XOR）。  
   - 同时把树转成 **有向的**（父 → 子），方便后面的递归。

2. **维护子树集合**  
   - 对每个节点 `u`，我们维护一个 **有序集合**（`SortedList`），里面存放 **子树里所有不同的 `pref`**。  
   - 合并时采用 **“小集合合并到大集合”**（small‑to‑large），即每次把子节点的集合合并到当前节点的集合时，先比较大小，把较小的集合的所有元素逐个插入较大的集合。这样每个元素最多被搬迁 `log n` 次，总体复杂度是 `O(n log n)`。

3. **处理查询**  
   - 在 DFS 进入节点 `u` 并完成 **子树集合的构建** 后，立即遍历挂在 `u` 上的所有查询 `[u, k]`。  
   - 因为集合已经是有序的，只需要直接取 `sorted_list[k-1]`（Python `SortedList` 支持 O(1) 按下标访问）即可得到第 `k` 小。如果集合大小 `< k`，返回 `-1`。

4. **为什么有序集合可以快速取第 k 小？**  
   - `SortedList` 的内部实现是 **分块的平衡二叉搜索树**（类似 B 树），所以插入、删除是 `O(log n)`，而**按下标取值**是 `O(1)`（因为每块里有序且记录了块大小）。这正好满足我们需要“既能快速合并，又能快速查询第 k 小”的要求。

> **类比**：把每个子树的 XOR 集合想象成一本已经排好序的字典。合并两本字典时，把页数少的那本的每一页（每个 XOR）插入页数多的那本，省时省力。查询第 `k` 小就像直接翻到第 `k` 页。

#### 代码（Python）

> 需要安装 `sortedcontainers`（`pip install sortedcontainers`），但在 LeetCode 环境中已经预装。

```python
from collections import defaultdict
from sortedcontainers import SortedList
import sys
sys.setrecursionlimit(1 << 25)

def kth_smallest_path_xor(par, vals, queries):
    n = len(vals)

    # ---------- 1. 建图（有向：父 -> 子） ----------
    children = [[] for _ in range(n)]
    for i in range(1, n):
        p = par[i]
        children[p].append(i)

    # ---------- 2. 计算 pref[u] ----------
    pref = [0] * n
    def dfs_pref(u, cur_xor):
        pref[u] = cur_xor ^ vals[u]
        for v in children[u]:
            dfs_pref(v, pref[u])
    dfs_pref(0, 0)

    # ---------- 3. 把查询挂到对应节点 ----------
    query_at = defaultdict(list)          # node -> list of (k, query_index)
    for idx, (u, k) in enumerate(queries):
        query_at[u].append((k, idx))

    ans = [-1] * len(queries)              # 最终答案数组

    # ---------- 4. DSU on tree（小到大合并） ----------
    def dfs(u):
        """返回一个 SortedList，里面是子树 u 的所有不同 pref"""
        # 先把当前节点自己的 pref 放进去，作为“当前集合”
        big_set = SortedList([pref[u]])

        # 递归处理所有孩子
        for v in children[u]:
            child_set = dfs(v)                     # 子树 v 的集合
            # 小集合合并到大集合
            if len(child_set) > len(big_set):
                big_set, child_set = child_set, big_set   # 交换，让 big_set 更大
            # 把 child_set 的每个元素插入 big_set（自动去重）
            for x in child_set:
                # SortedList 支持二分搜索，判断是否已经存在
                idx = big_set.bisect_left(x)
                if idx == len(big_set) or big_set[idx] != x:
                    big_set.add(x)                 # O(log n)
            # child_set 以后可以被垃圾回收

        # ---------- 5. 处理挂在 u 上的查询 ----------
        for k, qid in query_at[u]:
            if k <= len(big_set):
                ans[qid] = big_set[k - 1]          # 按下标直接取第 k 小
            else:
                ans[qid] = -1

        return big_set

    dfs(0)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n + q log n)`  
  - 每个节点的 `pref` 只计算一次 `O(n)`。  
  - 小到大合并时，每个 XOR 值最多被移动 `log n` 次（因为每次都进入更大的集合），每次插入 `SortedList` 是 `O(log n)`，所以整体是 `O(n log n)`。  
  - 处理查询只需要 `O(1)` 取值或 `O(log n)` 判断长度，总体与 `q` 成线性关系。  
  - 与暴力的 `O(n·q)` 相比，数量级下降了一个 **log**，在 `5·10⁴` 规模下轻松通过。

- **空间复杂度**：`O(n)`  
  - `pref`、`children`、递归栈以及所有集合的元素总数恰好等于树中节点数（每个节点的 XOR 只会出现在它所在的一个集合里），因此整体是线性空间。

---

## 心得

- **核心技巧**：**树上小到大合并（DSU on tree）** + **有序集合（SortedList）**。  
- **适用的题型**  
  1. 在子树上统计不同元素并需要快速查询第 `k` 小/大（如 “Subtree Queries with Distinct Colors”）。  
  2. 在子树上维护前缀和/前缀异或的集合并支持区间统计（如 “Maximum XOR Subtree”）。  
  3. 任意需要在树的子结构上做 **合并并查询** 的问题。

> **一句话总结解题钥匙**：把子树的信息“先收集、再合并、最后查询”，合并时总是把小的集合搬进大的集合，保证整体复杂度只增长 `log` 级。

---

## 反思

- **第一反应**：看到“子树里第 k 小的不同 XOR”，第一想法是把每棵子树都枚举、排序——这就是暴力解。  
- **最容易踩的坑**  
  - **去重**：`SortedList` 本身可以容纳重复值，需要在插入时手动判断是否已经存在，否则第 `k` 小会被重复元素干扰。  
  - **递归深度**：树可能是链状的，深度达 `5·10⁴`，需要 `sys.setrecursionlimit` 或改写为显式栈。  
  - **整数范围**：`vals[i] ≤ 10⁵`，异或结果也在 `2^17` 左右，仍然适合直接存整数。  
- **下次遇到同类题**：第一步就想到 “**把子树的信息在一次 DFS 中就准备好**”，随后决定使用 **小到大合并** 来保持高效。这样可以把“每次查询都遍历子树”的成本压到 **一次遍历** 里。