# #3585. 加权中位节点 / Find Weighted Median Node in Tree

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/find-weighted-median-node-in-tree/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an undirected, weighted tree rooted at node 0 with n nodes numbered from 0 to n - 1. This is represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi, wi] indicates an edge from node ui to vi with weight wi.
The weighted median node is defined as the first node x on the path from ui to vi such that the sum of edge weights from ui to x is greater than or equal to half of the total path weight.
You are given a 2D integer array queries. For each queries[j] = [uj, vj], determine the weighted median node along the path from uj to vj.
Return an array ans, where ans[j] is the node index of the weighted median for queries[j].

**Examples**

**Example 1:**

```
Input: n = 2, edges = [[0,1,7]], queries = [[1,0],[0,1]]
Output: [0,1]
Explanation:
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,2],[2,0,4]], queries = [[0,1],[2,0],[1,2]]
Output: [1,0,2]
E xplanation:
```

**Example 3:**

```
Input: n = 5, edges = [[0,1,2],[0,2,5],[1,3,1],[2,4,3]], queries = [[3,4],[1,2]]
Output: [2,2]
Explanation:

Sum from 1 → 0 = 2 < 3.5 . Sum from 1 → 2 = 2 + 5 = 7 >= 3.5 , median is node 2.
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i] == [ui, vi, wi]
- 0 <= ui, vi < n
- 1 <= wi <= 109
- 1 <= queries.length <= 105
- queries[j] == [uj, vj]
- 0 <= uj, vj < n
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

你得到一个整数 `n`，以及一棵以节点 `0` 为根的无向加权树，树中有 `n` 个节点，编号为 `0` 到 `n - 1`。树由长度为 `n - 1` 的二维数组 `edges` 表示，其中 `edges[i] = [ui, vi, wi]` 表示一条连接节点 `ui` 与 `vi`、权重为 `wi` 的边。

**加权中位节点** 定义为：在节点 `ui` 到 `vi` 的路径上，首次出现的节点 `x`，使得从 `ui` 到 `x` 的边权之和 **大于等于** 整条路径权重的一半。

现在给定一个二维整数数组 `queries`。对于每个 `queries[j] = [uj, vj]`，请找出路径 `uj → vj` 上的加权中位节点。

返回一个数组 `ans`，其中 `ans[j]` 为 `queries[j]` 对应的加权中位节点的索引。

---

### 示例

**示例 1**

```text
Input: n = 2, edges = [[0,1,7]], queries = [[1,0],[0,1]]
Output: [0,1]
Explanation:
路径 1 → 0 的总权重为 7，半径为 3.5。第一个满足累计权重 ≥ 3.5 的节点是 0。
路径 0 → 1 同理，第一个满足条件的节点是 1。
```

**示例 2**

```text
Input: n = 3, edges = [[0,1,2],[2,0,4]], queries = [[0,1],[2,0],[1,2]]
Output: [1,0,2]
Explanation:
- 路径 0 → 1 的总权重为 2，半径为 1。累计到节点 1 时已经达到 2 ≥ 1，所以中位节点是 1。
- 路径 2 → 0 的总权重为 4，半径为 2。累计到节点 0 时达到 4 ≥ 2，所以中位节点是 0。
- 路径 1 → 2 的总权重为 2 + 4 = 6，半径为 3。累计到节点 2 时达到 6 ≥ 3，所以中位节点是 2。
```

**示例 3**

```text
Input: n = 5, edges = [[0,1,2],[0,2,5],[1,3,1],[2,4,3]], queries = [[3,4],[1,2]]
Output: [2,2]
Explanation:
- 路径 3 → 4 的权重序列为 1 (3→1) + 2 (1→0) + 5 (0→2) + 3 (2→4) = 11，半径为 5.5。累计到节点 2 时权重为 1+2+5 = 8 ≥ 5.5，故中位节点为 2。
- 路径 1 → 2 的权重序列为 2 (1→0) + 5 (0→2) = 7，半径为 3.5。累计到节点 2 时权重为 2+5 = 7 ≥ 3.5，故中位节点为 2。
```

---

### 约束条件

- `2 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i] == [ui, vi, wi]`
- `0 <= ui, vi < n`
- `1 <= wi <= 10^9`
- `1 <= queries.length <= 10^5`
- `queries[j] == [uj, vj]`
- `0 <= uj, vj < n`
- 输入保证 `edges` 构成一棵合法的树。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把两点之间的完整路径列出来**，然后从起点 `u` 沿着路径累加边的权重，第一次累计值 ≥ 总路径权重的一半时所在的节点就是答案。

- **数据结构**  
  - **邻接表**：把树的每条带权边存成 `graph[u] = [(v, w), …]`。这相当于一本“城市地图”，每个城市（节点）里记着通往哪些邻居以及路程（权重）。  
  - **DFS / BFS**：用于在树上找到两点的**最近公共祖先**（LCA），相当于在家谱里找两个人最近的共同祖父。得到 LCA 后，我们可以把 `u → v` 的路径拆成 `u → LCA` + `LCA → v` 两段。  

- **为什么正确**  
  1. 树没有环，所以任意两点之间的路径唯一。  
  2. 通过 LCA 把路径拆开后，拼接两段即可得到完整路径。  
  3. 按顺序累计权重，第一次 ≥ `total/2` 的节点必然是题目定义的**加权中位节点**。  

- **复杂度分析（大白话）**  
  - 找 LCA 需要遍历整棵树的深度信息，最坏情况是 **O(n)**（把所有节点都查一遍）。  
  - 把路径上的所有节点收集到列表里，同样是 **O(length_of_path)**，最坏也可能是 **O(n)**（路径可能是根到最深叶子）。  
  - 对每个查询都这么做，**总时间**是 `queries * O(n)`，在最坏情况下会达到 `10^5 * 10^5`，显然会超时。  
  - 额外的空间主要是存路径的列表，最多 **O(n)**（一条最长路径）。  

> **O(n²)** 可以想象成「每个学生（查询）都要把全班（所有节点）排个序」，显然太慢了。

#### 代码（Python）

```python
from collections import defaultdict, deque
import sys
sys.setrecursionlimit(10**6)

def brute_force(n, edges, queries):
    # 1️⃣ 建图（邻接表）
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # 2️⃣ 预处理父节点和深度（帮助找 LCA）
    parent = [-1] * n          # 父节点
    depth  = [0] * n           # 深度（根的深度为 0）
    up_w   = [0] * n           # 从根到当前节点的累计权重

    def dfs(u, p):
        for v, w in graph[u]:
            if v == p:          # 不往回走
                continue
            parent[v] = u
            depth[v]  = depth[u] + 1
            up_w[v]   = up_w[u] + w   # 累计权重
            dfs(v, u)

    dfs(0, -1)   # 树根是 0

    # 3️⃣ 求两点 LCA（暴力向上爬）
    def lca(a, b):
        # 让 a、b 在同一深度
        while depth[a] > depth[b]:
            a = parent[a]
        while depth[b] > depth[a]:
            b = parent[b]
        # 同时向上，直到相遇
        while a != b:
            a = parent[a]
            b = parent[b]
        return a

    # 4️⃣ 处理每个查询
    ans = []
    for u, v in queries:
        # a. 找 LCA，计算整条路径的总权重
        L = lca(u, v)
        total = up_w[u] + up_w[v] - 2 * up_w[L]   # 两端到根的累计减去公共部分

        # b. 把路径展开成列表（从 u 往上到 L，再从 L 往下到 v）
        path = []
        cur = u
        while cur != L:               # u → L（不含 L）
            path.append(cur)
            cur = parent[cur]
        path.append(L)                # 加上 L
        # 收集 L → v（需要反向，因为我们要从 L 往 v 前进）
        stack = []
        cur = v
        while cur != L:
            stack.append(cur)
            cur = parent[cur]
        while stack:
            path.append(stack.pop())   # 逆序加入

        # c. 累加权重，找到第一个累计 ≥ total/2 的节点
        half = total / 2
        cur_sum = 0
        median_node = None
        for i in range(len(path) - 1):
            a, b = path[i], path[i+1]
            # 找到两点之间的权重（因为是无向树，遍历一次就行）
            for nb, w in graph[a]:
                if nb == b:
                    cur_sum += w
                    break
            if cur_sum >= half:
                median_node = b
                break
        ans.append(median_node if median_node is not None else u)  # 防止单点情况
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(Q * n)`，其中 `Q = len(queries)`，每个查询最坏需要遍历整棵树的深度（即 `n`）。  
  - 换句话说，就是 **“每个问题都要把整棵树走一遍”**，在 `n = 10^5`、`Q = 10^5` 时根本跑不完。  
- **空间复杂度**：`O(n)` 用于存图、父指针、深度以及一次展开的路径列表。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**逐条遍历路径**。我们需要一种方式，**在不展开整条路径的前提下**，直接跳到“累计权重第一次 ≥ 一半”的位置。  

关键点有三块：

1. **二分跳（Binary Lifting）**  
   - 想象把树的每个节点向上“搭梯子”。第 0 阶梯子是直接的父亲，第 1 阶梯子是 2 步的祖父，第 2 阶梯子是 4 步的祖父…  
   - 通过 **稀疏表**（`up[k][v]`）我们可以在 `O(log n)` 时间内，让节点一次性跳上 `2^k` 步。  

2. **同时记录累计权重**  
   - 只跳节点不记录路程是不行的。我们再准备一张表 `up_w[k][v]`，表示从 `v` 往上跳 `2^k` 步的 **总权重**。  
   - 这样在一次跳跃的同时，就能把这段路的权重累加到当前和里。  

3. **利用 LCA 把问题拆成两段**  
   - 对查询 `(u, v)`，先求出最近公共祖先 `l`（同样用二分跳的方式 O(log n)）。  
   - 整条路径的总权重 `tot = dist(u, l) + dist(v, l)`，其中 `dist` 可以用 `up_w` 快速求得。  
   - 接下来判断**加权中位点在 u→l 这段还是在 v→l 这段**。  
     - 若在 `u → l`：我们在 `u` 向上跳，保持一个累计和 `cur`，寻找**最后一个**使 `2*cur < tot` 的节点 `x`，答案就是 `parent[x]`（即再往上一步）。  
     - 若在 `v → l`：同理，只是从 `v` 向上跳。  

**如何在 O(log n) 内完成“最后一个满足条件的节点”**？  
- 从最高位（`2^k`）开始尝试跳：如果跳过去后 `2 * (cur + up_w[k][cur_node]) < tot`，说明还没有到达一半，可以**放心跳**，并把累计权重加上这段的 `up_w`。  
- 否则不跳，继续检查更小的位。最终停在**恰好不满足条件**的节点 `x`，答案是它的父亲（或直接是 `x` 本身，视具体实现而定）。  

这样，每个查询只需要 **两次 LCA + 两次二分跳**，整体是 `O(log n)`。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def weighted_median_queries(n, edges, queries):
    LOG = (n).bit_length()          # 能覆盖到 2^LOG > n

    # ---------- 1️⃣ 建图 ----------
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # ---------- 2️⃣ 预处理父指针、深度、累计权重 ----------
    up = [[-1] * n for _ in range(LOG)]      # up[k][v] = 2^k 步的祖父
    up_w = [[0] * n for _ in range(LOG)]     # 对应累计权重
    depth = [0] * n

    def dfs(u, p):
        for v, w in graph[u]:
            if v == p:
                continue
            up[0][v] = u               # 第 0 阶梯子是直接父亲
            up_w[0][v] = w             # 这一步的权重
            depth[v] = depth[u] + 1
            dfs(v, u)

    dfs(0, -1)   # 根节点是 0

    # ---------- 3️⃣ 构造二进制提升表 ----------
    for k in range(1, LOG):
        for v in range(n):
            if up[k-1][v] != -1:
                up[k][v] = up[k-1][up[k-1][v]]
                up_w[k][v] = up_w[k-1][v] + up_w[k-1][up[k-1][v]]
                # 累计权重：先走 2^{k-1} 步，再走另一段 2^{k-1} 步

    # ---------- 4️⃣ 辅助函数 ----------
    def lift(node, dist):
        """把 node 向上跳 dist 步，同时返回累计权重"""
        cur_w = 0
        for k in range(LOG-1, -1, -1):
            if node == -1:
                break
            if (1 << k) <= dist:
                cur_w += up_w[k][node]
                node = up[k][node]
                dist -= (1 << k)
        return node, cur_w

    def lca(a, b):
        """二分跳求最近公共祖先"""
        if depth[a] < depth[b]:
            a, b = b, a
        # 把 a 拉到和 b 同深度
        diff = depth[a] - depth[b]
        a, _ = lift(a, diff)
        if a == b:
            return a
        # 同时向上跳，找到最高不同的祖先
        for k in range(LOG-1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return up[0][a]

    def dist_to_ancestor(node, anc):
        """返回 node 到 anc（一定是 anc 的子树）的累计权重"""
        # 假设 anc 在 node 的祖先链上
        d = depth[node] - depth[anc]
        _, w = lift(node, d)
        return w

    # ---------- 5️⃣ 处理每个查询 ----------
    ans = []
    for u, v in queries:
        L = lca(u, v)                         # 最近公共祖先
        # 整条路径总权重
        total = dist_to_ancestor(u, L) + dist_to_ancestor(v, L)

        # 先尝试在 u -> L 这段寻找
        cur = u
        cur_sum = 0
        # 从高位往低位尝试跳，如果跳过去后仍然 < half，则真的跳
        for k in range(LOG-1, -1, -1):
            if up[k][cur] != -1 and depth[up[k][cur]] >= depth[L]:
                if 2 * (cur_sum + up_w[k][cur]) < total:
                    cur_sum += up_w[k][cur]
                    cur = up[k][cur]

        # 跳完后 cur 仍在满足 “2*sum < total” 的最远节点
        # 若再往上一步会使条件不成立（或已经到 L），答案就是它的父亲
        if cur != L:
            median = up[0][cur]   # 父节点即为加权中位节点
            ans.append(median)
            continue

        # 若没有在 u→L 这段满足（说明中位点在 L→v），同理从 v 出发向上找
        cur = v
        cur_sum = 0
        for k in range(LOG-1, -1, -1):
            if up[k][cur] != -1 and depth[up[k][cur]] >= depth[L]:
                if 2 * (cur_sum + up_w[k][cur]) < total:
                    cur_sum += up_w[k][cur]
                    cur = up[k][cur]

        # 此时 cur 必定在 L 的子树里，答案是它的父亲（或 L 本身）
        median = up[0][cur] if cur != L else L
        ans.append(median)

    return ans
```

> **代码要点说明**  
> 1. `LOG = n.bit_length()` 保证 `2^LOG` 大于等于 `n`，所以表的高度足够。  
> 2. `up_w[k][v]` 存的是 **从 v 向上走 2^k 步的所有边权之和**，相当于把“路程”也一起搬上梯子。  
> 3. `lift` 函数一次性返回 **跳完后的节点 + 累计的权重**，方便在后面的二分跳中使用。  
> 4. 在寻找“最后一个满足 `2*sum < total` 的节点”时，我们从最高位开始尝试跳。如果跳过去仍然满足条件，就“放心跳”。这正是 **二分搜索** 的思想，只是把“搜索空间”换成了树的层次。  

#### 复杂度  

- **时间复杂度**：`O((n + Q) * log n)`  
  - 构建 `up`、`up_w` 表：`O(n log n)`（遍历 `n` 个节点，每层 `log n`）。  
  - 每个查询：一次 LCA (`O(log n)`) + 两次二分跳 (`O(log n)`) → 总计 `O(log n)`。  
  - 与暴力的 `O(Q * n)` 相比，**把每个查询从“遍历整条路径”降到“跳几次”**，在 `n = 10^5`、`Q = 10^5` 时可以轻松跑完。  

- **空间复杂度**：`O(n log n)`  
  - 两张稀疏表 `up`、`up_w` 各占 `n * log n`，深度数组等额外 `O(n)`。  
  - 相当于为每个节点准备了大约 `log2(10^5) ≈ 17` 条“跳梯子”。  

---

## 心得  

- **核心技巧**：**二分跳（Binary Lifting）+ 累计权重**。它把“沿父链逐个移动”压缩成“跳若干步一次”，同时保留每段路的总长度，能够在对数时间内完成距离比较。  
- **适用的题型**（类似思路）  
  1. **Kth ancestor / distance on tree** – 求第 k 代祖先或两点距离。  
  2. **Path queries with monotonic condition** – 如“路径上第一个权值 ≥ X”。  
  3. **Tree version of prefix sum / binary search** – 如“树上路径的第一个满足累计和 >= target 的节点”。  
- **一句话总结**：**把路径上的线性累加转化为二进制跳跃的累加，就能在 O(log n) 内找到加权中位节点。**

---

## 反思  

- **第一反应**：看到“路径上累计权重大于等于一半”，本能想把路径全部列出来再遍历——这正是暴力思路。  
- **最容易踩的坑**  
  1. **忘记把 LCA 本身的权重算两次**：`dist(u, l) + dist(v, l)` 已经把从根到 L 的公共部分减掉，若误加会导致总权重翻倍。  
  2. **二分跳的边界**：跳的目标必须 **不超过 L 的深度**，否则会跳出路径导致错误。  
  3. **权重可能非常大（10^9）**，累加时一定要使用 `int`（Python 自动大整数）或 `long long`，防止溢出。  
- **下次类似题的第一步**：  
  - **先确认能否把“沿父链的线性操作”用二分跳压缩**（即是否需要频繁查询路径上累计信息）。如果是，就立刻构造 `up` 与 **累计权重表**，再在此基础上做二分搜索。