# #2646. **最小化所有旅行的总费用** / Minimize the Total Price of the Trips

> 难度：困难 · 标签：Array、Dynamic Programming、Tree、Depth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/minimize-the-total-price-of-the-trips/)

---

## 题目（英文原版）

**Description**

There exists an undirected and unrooted tree with n nodes indexed from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
Each node has an associated price. You are given an integer array price, where price[i] is the price of the ith node.
The price sum of a given path is the sum of the prices of all nodes lying on that path.
Additionally, you are given a 2D integer array trips, where trips[i] = [starti, endi] indicates that you start the ith trip from the node starti and travel to the node endi by any path you like.
Before performing your first trip, you can choose some non-adjacent nodes and halve the prices.
Return the minimum total price sum to perform all the given trips.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[0,1],[1,2],[1,3]], price = [2,2,10,6], trips = [[0,3],[2,1],[2,3]]
Output: 23
Explanation: The diagram above denotes the tree after rooting it at node 2. The first part shows the initial tree and the second part shows the tree after choosing nodes 0, 2, and 3, and making their price half.
For the 1st trip, we choose path [0,1,3]. The price sum of that path is 1 + 2 + 3 = 6.
For the 2nd trip, we choose path [2,1]. The price sum of that path is 2 + 5 = 7.
For the 3rd trip, we choose path [2,1,3]. The price sum of that path is 5 + 2 + 3 = 10.
The total price sum of all trips is 6 + 7 + 10 = 23.
It can be proven, that 23 is the minimum answer that we can achieve.
```

**Example 2:**

```
Input: n = 2, edges = [[0,1]], price = [2,2], trips = [[0,0]]
Output: 1
Explanation: The diagram above denotes the tree after rooting it at node 0. The first part shows the initial tree and the second part shows the tree after choosing node 0, and making its price half.
For the 1st trip, we choose path [0]. The price sum of that path is 1.
The total price sum of all trips is 1. It can be proven, that 1 is the minimum answer that we can achieve.
```

**Constraints**

- 1 <= n <= 50
- edges.length == n - 1
- 0 <= ai, bi <= n - 1
- edges represents a valid tree.
- price.length == n
- price[i] is an even integer.
- 1 <= price[i] <= 1000
- 1 <= trips.length <= 100
- 0 <= starti, endi <= n - 1

---

## 题目（中文翻译）

存在一棵无向且未指定根的树，包含 `n` 个节点，编号为 `0` 到 `n-1`。给定整数 `n` 和长度为 `n-1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条边（edge）。  

每个节点都有一个对应的费用（price）。数组 `price` 中 `price[i]` 为第 `i` 个节点的费用。  

一条路径的费用和（price sum）是该路径上所有节点费用的总和。  

此外，还给定二维整数数组 `trips`，其中 `trips[i] = [start_i, end_i]` 表示第 `i` 次旅行从节点 `start_i` 出发，沿任意路径前往节点 `end_i`。  

在进行第一次旅行之前，你可以选择若干 **不相邻**（non‑adjacent）的节点，并将这些节点的费用减半。  

返回在所有给定旅行完成后可能的 **最小总费用和**（minimum total price sum）。

---

### 示例

#### 示例 1
```
Input: n = 4, edges = [[0,1],[1,2],[1,3]], price = [2,2,10,6], trips = [[0,3],[2,1],[2,3]]
Output: 23
Explanation: 上图把树以节点 2 为根。左侧展示了原始树，右侧展示了选取节点 0、2、3 并将它们的费用减半后的树。
对于第 1 次旅行，选择路径 [0,1,3]。该路径的费用和为 1 + 2 + 3 = 6。
...
```

#### 示例 2
```
Input: n = 2, edges = [[0,1]], price = [2,2], trips = [[0,0]]
Output: 1
Explanation: 上图把树以节点 0 为根。左侧展示了原始树，右侧展示了选取节点 0 并将其费用减半后的树。
对于第 1 次旅行，选择路径 [0]。该路径的费用和为 1。
所有旅行的总费用和为 1。可以证明，这已经是最小值。
...
```

---

### 约束条件

- `1 <= n <= 50`
- `edges.length == n - 1`
- `0 <= a_i, b_i <= n - 1`
- `edges` 构成一棵合法的树
- `price.length == n`
- `price[i]` 为偶数
- `1 <= price[i] <= 1000`
- `1 <= trips.length <= 100`
- `0 <= start_i, end_i <= n - 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **先算每个节点被访问的次数**  
   - 对每一次出行 `trips[i] = [s, e]`，在树里找一条从 `s` 到 `e` 的路径。  
   - 把路径上所有节点的访问计数 `freq[node]` 加 1。  
   - 因为树只有 `n-1` 条边，`n ≤ 50`，我们可以直接用 **DFS**（深度优先搜索）一次遍历整棵树，找到 `s` 到 `e` 的路径。  
   - 这样对所有出行都做一次 DFS，时间大概是 `O(trips·n)`（每次遍历最多 `n` 个节点）。

2. **枚举所有可以“打半价”的节点集合**  
   - 题目要求**相邻的节点不能同时打半价**（即选的节点必须构成一棵树的**独立集**）。  
   - 最直接的办法是遍历 **所有子集**（`2^n` 种），对每个子集检查是否满足“相邻节点不同时出现”。  
   - 如果合法，就把子集中节点的价格除以 2（因为 `price[i]` 保证是偶数），再算所有出行的总费用：  
     \[
     \text{total} = \sum_{i=0}^{n-1} \text{freq}[i] \times \text{price\_after\_halving}[i]
     \]  
   - 取所有合法子集的最小 `total` 即为答案。

3. **为什么暴力一定能对**  
   - 我们遍历了**所有可能的打半价方案**，并且对每个方案都精确计算了所有出行的费用，所以最小值一定是正确的。

#### 代码（Python）

```python
from itertools import combinations
from collections import defaultdict, deque
from typing import List

# ---------- 辅助：在树上找两点路径 ----------
def find_path(adj: List[List[int]], start: int, end: int) -> List[int]:
    """返回 start -> end 的节点列表（包含两端），使用 BFS 记录父节点"""
    n = len(adj)
    parent = [-1] * n
    q = deque([start])
    parent[start] = start          # 起点的父亲指向自己，方便回溯

    while q:
        cur = q.popleft()
        if cur == end:
            break
        for nb in adj[cur]:
            if parent[nb] == -1:
                parent[nb] = cur
                q.append(nb)

    # 回溯得到路径
    path = []
    node = end
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()
    return path


# ---------- 主函数 ----------
def minimumTotalPrice_bruteforce(n: int, edges: List[List[int]],
                                price: List[int], trips: List[List[int]]) -> int:
    # 建图（邻接表）
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # 1️⃣ 统计每个节点被访问的次数 freq[]
    freq = [0] * n
    for s, e in trips:
        path = find_path(adj, s, e)          # O(n) 的 BFS + 回溯
        for node in path:
            freq[node] += 1

    # 2️⃣ 枚举所有合法的“打半价”子集
    best = float('inf')
    # 为了方便检查相邻冲突，我们先把所有边放进集合
    edge_set = {tuple(sorted(e)) for e in edges}

    # 由于 n ≤ 50，直接遍历 2^n 仍然会超时，但这里仅作教学演示。
    # 实际运行时请把 n 限制到更小的数（比如 ≤ 15）或者直接使用 DP。
    for mask in range(1 << n):
        # 检查相邻节点是否都被选中了
        ok = True
        for a, b in edges:
            if (mask >> a) & 1 and (mask >> b) & 1:
                ok = False
                break
        if not ok:
            continue

        # 计算该方案的总费用
        total = 0
        for i in range(n):
            cur_price = price[i]
            if (mask >> i) & 1:          # 选中 -> 价格减半
                cur_price //= 2
            total += cur_price * freq[i]

        best = min(best, total)

    return best
```

> **关键行注释**  
> - `find_path` 用 BFS 记录每个节点的父亲，然后从终点回溯到起点得到完整路径。  
> - `freq[node] += 1` 把每一次出行经过的节点都累加进访问计数。  
> - `mask` 的第 `i` 位为 1 表示节点 `i` 被选中打半价。  
> - 检查相邻冲突时，只要有一条边两端都被选中，就直接 `break`，因为这已经违背了题目限制。

#### 复杂度  

- **时间复杂度**  
  - 统计访问次数：`O(trips·n)`（每次 BFS 最多遍历 `n` 个节点）。  
  - 枚举子集：`O(2^n·n)`（`2^n` 种子集，每个子集要检查 `n-1` 条边）。  
  - 综合下来是 **指数级**，在最坏情况下 `n=50` 时根本不可行，只能用于理解思路。  
- **空间复杂度**  
  - `O(n)` 的邻接表、访问计数和递归栈。  
  - 额外的 `O(1)` 用于遍历子集的位运算。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **两件事**：

1. **对每次出行都重新遍历整棵树找路径**  
   - 实际上我们只需要知道每个节点被访问了多少次 `freq[i]`，不必每次都走完整条路径。

2. **枚举所有合法的打半价节点集合**  
   - “相邻节点不能同时选” 是**独立集**（Independent Set）问题，在树上可以用**动态规划**在 `O(n)` 时间完成。

下面一步步把这两个瓶颈化解。

---

#### 2.1 统计每个节点的访问次数（freq）

把所有出行看成在树上 **加权** 的路径。  
对一条路径 `[u … v]`，如果我们在 `freq` 上做如下操作：

| 操作 | 目的 |
|------|------|
| `freq[u] += 1` | 起点进入路径一次 |
| `freq[v] += 1` | 终点进入路径一次 |
| `freq[lca] -= 2` | 让 LCA（最近公共祖先）以及它的父亲不再重复计数 |

> **为什么这样就能得到每个节点的最终访问次数？**  
> 把所有出行的增减操作完成后，再从叶子向根 **累计**（后序遍历）每个节点的 `freq` 到它的父亲。  
> 累计的过程相当于把“路径上的 +1”往上推，最终每个节点的 `freq` 就是它在所有路径中出现的次数。

**实现细节**  

1. **先把树根化**（任选一个节点做根，例如 0），用 DFS 记录每个节点的深度 `depth` 与父亲 `up[k][v]`（二进制提升表），这样可以在 `O(log n)` 时间求出任意两点的 LCA。  
2. 对每一条出行 `[s, e]`：  
   - `freq[s] += 1`、`freq[e] += 1`  
   - `l = lca(s, e)`  
   - `freq[l] -= 2`  
3. 最后一次 **后序 DFS**（从根往下遍历子树），把子节点的 `freq` 加到父节点上。此时 `freq[i]` 就是节点 `i` 被访问的总次数。

---

#### 2.2 在树上做“独立集”动态规划

每个节点有两种状态：

| 状态 | 含义 | 对应费用 |
|------|------|----------|
| `0` | 不打半价，费用为 `price[i] * freq[i]` | `full = price[i] * freq[i]` |
| `1` | 打半价，费用为 `(price[i]/2) * freq[i]` | `half = price[i]//2 * freq[i]` |

因为相邻节点 **不能同时为 1**（即不能相邻打半价），我们可以在树上进行 **树形 DP**：

```
dp[v][0] = full(v) + sum( min(dp[child][0], dp[child][1]) )
dp[v][1] = half(v) + sum( dp[child][0] )   # child 必须是 0
```

解释：

- 当 `v` **不打半价**（状态 0）时，子节点可以自行决定是 0 还是 1，取两者的最小值。
- 当 `v` **打半价**（状态 1）时，子节点 **必须** 不打半价（状态 0），否则会出现相邻两点都被选的冲突。

我们用 **后序遍历**（自底向上）计算 `dp`，根节点的答案是 `min(dp[root][0], dp[root][1])`。

---

#### 2.3 完整流程概览  

1. 建树（邻接表），并用一次 DFS 记录 `depth`、`parent`、二进制提升表 `up`。  
2. 初始化 `freq = [0]*n`。  
3. 对每个 `trip`：  
   - 求 `l = lca(s, e)`（`O(log n)`）  
   - `freq[s] += 1; freq[e] += 1; freq[l] -= 2`  
4. 再次 **后序 DFS** 把子节点的 `freq` 累加到父节点，得到每个节点的真实访问次数。  
5. 用相同的后序 DFS 计算 `dp[v][0]`、`dp[v][1]`（每个节点只访问一次）。  
6. 返回 `min(dp[root][0], dp[root][1])`。

**时间复杂度**  

- 构建提升表：`O(n log n)`（`n ≤ 50`，完全可以忽略）。  
- 处理所有出行：`O(trips·log n)`（每次 LCA `log n`）。  
- 两次后序遍历：`O(n)`。  
- **总体**：`O(n log n + trips·log n) ≈ O((n+trips)·log n)`，在本题约 `O(150·log 50)`，几乎瞬间完成。  

**空间复杂度**  

- `O(n log n)` 用于二进制提升表（`log n ≤ 6`），再加 `O(n)` 的邻接表、`freq`、`dp`。  
- 总体 `O(n log n)`，在 `n ≤ 50` 的范围内几乎可以忽略。

---

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

# ------------------------------------------------------------
# 1️⃣ 预处理：建树、深度、父亲、二进制提升（LCA）
# ------------------------------------------------------------
def build_lca(n: int, edges: List[List[int]]):
    LOG = 6                     # 因为 2^6 = 64 > 50
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    parent = [[-1] * n for _ in range(LOG)]   # parent[k][v] = v 的 2^k 祖先
    depth = [0] * n

    def dfs(v: int, p: int):
        parent[0][v] = p
        for nb in adj[v]:
            if nb == p:
                continue
            depth[nb] = depth[v] + 1
            dfs(nb, v)

    dfs(0, 0)                               # 随便把 0 当根

    # 二进制提升表
    for k in range(1, LOG):
        for v in range(n):
            parent[k][v] = parent[k - 1][parent[k - 1][v]]

    def lca(u: int, v: int) -> int:
        """返回 u 与 v 的最近公共祖先（O(log n)）"""
        if depth[u] < depth[v]:
            u, v = v, u
        # 把 u 拉到和 v 同深度
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = parent[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return u
        # 同时跳高，直到父亲相同
        for k in range(LOG - 1, -1, -1):
            if parent[k][u] != parent[k][v]:
                u = parent[k][u]
                v = parent[k][v]
        return parent[0][u]

    return adj, depth, parent, lca


# ------------------------------------------------------------
# 2️⃣ 主函数：统计 freq、树形 DP 求最小费用
# ------------------------------------------------------------
def minimumTotalPrice(n: int, edges: List[List[int]],
                     price: List[int], trips: List[List[int]]) -> int:
    # 预处理 LCA
    adj, depth, parent, lca = build_lca(n, edges)

    # ① 统计每个节点的访问次数（差分 + 后序累加）
    freq = [0] * n
    for s, e in trips:
        freq[s] += 1
        freq[e] += 1
        anc = lca(s, e)
        freq[anc] -= 2                     # 让 LCA 及其父亲不再计数

    # ② 后序遍历把子节点的 freq 加到父亲上
    def dfs_acc(v: int, p: int):
        for nb in adj[v]:
            if nb == p:
                continue
            dfs_acc(nb, v)
            freq[v] += freq[nb]            # 子树的访问次数累计到父节点

    dfs_acc(0, -1)

    # ③ 树形 DP：dp[v][0] = 不打半价，dp[v][1] = 打半价
    dp0 = [0] * n          # 不打半价的最小费用
    dp1 = [0] * n          # 打半价的最小费用

    def dfs_dp(v: int, p: int):
        full = price[v] * freq[v]          # 不打半价的费用
        half = (price[v] // 2) * freq[v]   # 打半价的费用
        sum0, sum1 = 0, 0
        for nb in adj[v]:
            if nb == p:
                continue
            dfs_dp(nb, v)
            # 子节点可以自由选择（取最小）
            sum0 += min(dp0[nb], dp1[nb])
            # 子节点必须是 0（不打半价），因为 v 已经是 1
            sum1 += dp0[nb]

        dp0[v] = full + sum0
        dp1[v] = half + sum1

    dfs_dp(0, -1)

    # ④ 根节点可以选择打或不打，取最小值即为答案
    return min(dp0[0], dp1[0])
```

> **代码要点中文注释**  
> - `build_lca`：先 DFS 建立深度和第一层父亲，然后用「二进制提升」把每个节点的 `2^k` 祖先预先算好，之后的 LCA 查询只需要 `O(log n)`。  
> - `freq` 差分技巧：每条路径只在端点加 1，在 LCA 减 2，后序累计后自然得到每个节点被经过的次数。  
> - `dfs_dp`：后序遍历保证子树已经算好 `dp`，再根据「相邻不能都为 1」的约束进行状态转移。  

#### 复杂度  

- **时间复杂度**  
  - 建树 + LCA 预处理：`O(n log n)`（`n ≤ 50`，几乎是常数）。  
  - 处理所有出行：`O(trips·log n)`（每次 LCA `log n`）。  
  - 两次后序遍历（累计 `freq` + DP）：`O(n)`。  
  - **总体**：`O((n + trips)·log n)`，在本题数据规模下几乎是 **O(n + trips)**，非常快。

- **空间复杂度**  
  - 邻接表、深度、父亲表、提升表、`freq`、`dp` 共 `O(n log n)`，对 `n ≤ 50` 来说只占几百个整数，完全可以接受。

---

## 心得  

- **核心技巧**：  
  1. **树上路径计数的差分 + 后序累加**，把所有出行一次性转化为每个节点的访问次数。  
  2. **树形独立集 DP**（状态为「打半价」或「不打半价」），利用「相邻节点不能同时为 1」的约束在 `O(n)` 内求最优。

- **该技巧适用的题型**（可以类比）  
  1. “Maximum Sum of Non‑Adjacent Nodes in a Tree” —— 树上选取不相邻节点，使权值和最大。  
  2. “Tree Painting / Minimum Cost to Paint a Tree” —— 相邻节点颜色不能相同，求最小涂色费用。  
  3. “Count the Number of Paths Visiting Each Node” —— 用差分+后序累计统计路径经过次数。

- **一句话总结解题钥匙**  
  > **把所有路径的“+1”压缩成节点的访问次数，再在树上用独立集 DP 决定哪些节点要“打半价”。**

---

## 反思  

- **拿到题目第一反应**  
  - “每次出行都要跑一次最短路径，然后把所有可能的打半价组合暴力枚举”。  
  - 立刻想到“树上路径一定唯一”，于是考虑利用 LCA 来优化。

- **最容易踩的坑**  
  1. **差分计数忘记在 LCA 上减 2**，导致 `freq` 统计偏大。  
  2. **DP 状态写反**：`dp[v][1]` 必须把子节点全部设为 `0`，否则会出现相邻两个节点都打半价的非法情况。  
  3. **边界条件**：根节点的父亲在 DFS 中要设为 `-1`（或自身），否则递归会无限循环。  
  4. **价格是偶数**，除以 2 必须使用整数除法 `//`，避免出现浮点数。

- **下次遇到同类题，第一步该想到**  
  > **先把所有“路径相关的计数”用差分 + 后序累计的方式一次性算好，再在树上用 DP 处理相邻约束。**  

这样既能把原本 `O(trips·n)` 的路径遍历降到 `O(trips·log n)`，也能把指数级的子集枚举压缩到线性 DP，轻松 AC。