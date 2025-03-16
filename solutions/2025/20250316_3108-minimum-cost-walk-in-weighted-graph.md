# #3108. 加权图中的最小成本行走 / Minimum Cost Walk in Weighted Graph

> 难度：困难 · 标签：Array、Bit Manipulation、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-walk-in-weighted-graph/)

---

## 题目（英文原版）

**Description**

There is an undirected weighted graph with n vertices labeled from 0 to n - 1.
You are given the integer n and an array edges, where edges[i] = [ui, vi, wi] indicates that there is an edge between vertices ui and vi with a weight of wi.
A walk on a graph is a sequence of vertices and edges. The walk starts and ends with a vertex, and each edge connects the vertex that comes before it and the vertex that comes after it. It's important to note that a walk may visit the same edge or vertex more than once.
The cost of a walk starting at node u and ending at node v is defined as the bitwise AND of the weights of the edges traversed during the walk. In other words, if the sequence of edge weights encountered during the walk is w0, w1, w2, ..., wk, then the cost is calculated as w0 & w1 & w2 & ... & wk, where & denotes the bitwise AND operator.
You are also given a 2D array query, where query[i] = [si, ti]. For each query, you need to find the minimum cost of the walk starting at vertex si and ending at vertex ti. If there exists no such walk, the answer is -1.
Return the array answer, where answer[i] denotes the minimum cost of a walk for query i.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[0,1,7],[1,3,7],[1,2,1]], query = [[0,3],[3,4]]
Output: [1,-1]
Explanation:
To achieve the cost of 1 in the first query, we need to move on the following edges: 0->1 (weight 7), 1->2 (weight 1), 2->1 (weight 1), 1->3 (weight 7).
In the second query, there is no walk between nodes 3 and 4, so the answer is -1.
Example 2:
```

**Example 2:**

```
Input: n = 3, edges = [[0,2,7],[0,1,15],[1,2,6],[1,2,1]], query = [[1,2]]
Output: [0]
Explanation:
To achieve the cost of 0 in the first query, we need to move on the following edges: 1->2 (weight 1), 2->1 (weight 6), 1->2 (weight 1).
```

**Constraints**

- 2 <= n <= 105
- 0 <= edges.length <= 105
- edges[i].length == 3
- 0 <= ui, vi <= n - 1
- ui != vi
- 0 <= wi <= 105
- 1 <= query.length <= 105
- query[i].length == 2
- 0 <= si, ti <= n - 1
- si != ti

---

## 题目（中文翻译）

存在一张 **无向加权图（undirected weighted graph）**，有 `n` 个顶点，编号从 `0` 到 `n - 1`。  
给定整数 `n` 和数组 `edges`，其中 `edges[i] = [ui, vi, wi]` 表示在顶点 `ui` 和 `vi` 之间有一条权重为 `wi` 的边。

**行走（walk）** 是一系列顶点和边的序列。行走以顶点开始并以顶点结束，每条边连接它前后的两个顶点。需要注意的是，行走可以多次访问同一条边或同一个顶点。

从节点 `u` 开始、在节点 `v` 结束的行走的 **成本（cost）** 定义为该行走经过的所有边权重的 **按位与（bitwise AND）**。即若行走经过的边权重序列为 `w0, w1, w2, ..., wk`，则成本为 `w0 & w1 & w2 & ... & wk`（`&` 为按位与运算符）。

另给定二维数组 `query`，其中 `query[i] = [si, ti]`。对于每个查询，需要找出从顶点 `si` 到顶点 `ti` 的行走的 **最小成本**。如果不存在这样的行走，答案为 `-1`。

返回数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的最小成本。

---

### 示例

**示例 1**

```
输入: n = 5, edges = [[0,1,7],[1,3,7],[1,2,1]], query = [[0,3],[3,4]]
输出: [1,-1]
解释:
- 第一个查询要得到成本 1，需要走以下边: 0->1（权重 7），1->2（权重 1），2->1（权重 1），1->3（权重 7）。
- 第二个查询中，节点 3 与节点 4 之间不存在任何行走，答案为 -1。
```

**示例 2**

```
输入: n = 3, edges = [[0,2,7],[0,1,15],[1,2,6],[1,2,1]], query = [[1,2]]
输出: [0]
解释:
要得到成本 0，需要走以下边: 1->2（权重 1），2->1（权重 6），1->2（权重 1）。
```

---

### 约束条件

- `2 <= n <= 10^5`
- `0 <= edges.length <= 10^5`
- `edges[i].length == 3`
- `0 <= ui, vi <= n - 1`
- `ui != vi`
- `0 <= wi <= 10^5`
- `1 <= query.length <= 10^5`
- `query[i].length == 2`
- `0 <= si, ti <= n - 1`
- `si != ti`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举出来**，然后把每条走法的边权取 `&`（按位与），找出最小的那个。  
可以把这个过程想象成：

- **走迷宫**：从起点 `s` 出发，一步一步往四周走，记录下每一步走过的门的密码（边权）。  
- **把所有密码都写下来**，再把它们一个个用 “按位与” 合在一起，得到这条路的花费。  
- **遍历所有可能的路径**，取最小的花费。

这种做法在概念上很容易理解，因为我们把**所有合法的走法都考虑到了**，自然可以保证找到最小的答案。

**为什么它是对的？**  
只要我们真的把 **所有** 可能的走法都遍历一遍，答案必然在其中——这是一种穷举的保证。

**但是它的效率太差**：

- 图的规模可以到 `10⁵`，路径的数量会呈指数级增长（即使只考虑最短路径也会有 `O(n!)` 种可能）。  
- 对每条路径我们都要做一次 `&` 运算，时间会爆炸。

**时间/空间复杂度**（大白话）：

- **时间**：`O(所有可能走法的数量)`，在最坏情况下几乎是 **无限大**，根本不可接受。  
- **空间**：需要存放所有走法的记录，最坏情况下也会是 **指数级**，同样不可行。

> 这里的 `O(n²)`、`O(2ⁿ)` 等符号只是用来说明“随输入规模快速增长”，实际运行时会直接超时或内存炸掉。

#### 代码（Python）

```python
# 下面的代码只是演示“暴力枚举所有走法”的思路，
# 实际上在 LeetCode 的数据范围下根本跑不完。
# 请不要在正式提交时使用。

from collections import defaultdict, deque

def brute_min_cost(n, edges, queries):
    # 建图（邻接表）
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    def bfs_min_and(s, t):
        # 用 BFS 枚举所有走法（这里仍然会无限循环，需要额外限制步数）
        best = None
        # (当前节点, 当前 AND 值)
        q = deque([(s, (1 << 20) - 1)])   # 初始 AND 为全 1（足够大）
        visited = set()
        while q:
            node, cur = q.popleft()
            if node == t:
                best = cur if best is None else min(best, cur)
                continue
            for nxt, w in g[node]:
                new_and = cur & w
                # 为了演示，这里不做剪枝，直接继续搜索
                q.append((nxt, new_and))
        return -1 if best is None else best

    ans = []
    for s, t in queries:
        ans.append(bfs_min_and(s, t))
    return ans
```

#### 复杂度

- **时间复杂度**：`O(所有可能走法的数量)`，在最坏情况下呈指数级增长，根本不可接受。  
- **空间复杂度**：`O(搜索队列的最大规模)`，同样可能达到指数级。  

> 结论：暴力解只能帮助我们理清问题，却无法在大数据上通过。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现 **枚举所有走法是最慢的瓶颈**。要想快一点，必须 **不去真正走路**，而是直接利用图的结构特性来推导答案。

关键观察：

1. **按位与的单调性**  
   对任意两个整数 `a, b`，有 `a & b ≤ a`（因为 `&` 只能把位从 1 变成 0，不能把 0 变成 1）。  
   换句话说，**加入更多的边权，只会让结果的二进制位数目变少（即数值变小）**。  

2. **可以重复走同一条边**  
   题目允许 **任意次数** 地走同一条边或访问同一个顶点。也就是说，只要我们想把某个边的权值加入到 `AND` 里，**随时都能做到**。  

3. **在同一个连通块里，任意两点都可以互相到达**  
   如果 `s` 与 `t` 在同一个连通分量（connected component），我们可以先走到 **连通块内部任意一条边**，再走回来，最后到达 `t`。  
   因此，**我们可以把连通块里的所有边权都“强行加入”到走法的 `AND` 中**。

综合 1~3，**最小可能的花费** 就是 **该连通块中所有边权的按位与**。因为：

- 加入所有边权得到的 `AND` 是 **最小的**（再加入任何东西都不会让它更小）。
- 只要 `s` 与 `t` 同属一个连通块，就一定能构造出一条包含所有这些边的走法（先走到每条边，再回到目标）。

如果 `s` 与 `t` **不在同一个连通块**，根本不存在任何走法，答案是 `-1`。

于是问题转化为：

> **对于每个连通块，求出其中所有边权的按位与**，并能够快速判断两个点是否在同一个块里。

这正是 **并查集（Disjoint Set Union，DSU）** 的拿手好戏：

- DSU 能在近似 `O(α(n))`（α 为极慢增长的反阿克曼函数）时间内完成 “合并两个集合” 与 “查询两点是否同属一个集合”。  
- 我们只要在合并时维护 **该集合的 `AND` 值**，就能在所有边处理完后得到每个连通块的答案。

**细节实现**：

1. **初始化**  
   - 每个节点自成一个集合，`and_val[i] = ALL_ONES`（全部 1），因为 `x & ALL_ONES = x`。  
   - `ALL_ONES` 取足够大的全 1，例如 `(1 << 20) - 1`，因为 `wi ≤ 10⁵ < 2¹⁷`。

2. **遍历每条边 `[u, v, w]`**  
   - 找到 `u`、`v` 所在的根 `ru, rv`。  
   - **如果 `ru != rv`**（两端原本不在同一个集合）  
     - 合并这两个集合，新的 `AND` 为 `and_val[ru] & and_val[rv] & w`。  
   - **如果 `ru == rv`**（已经在同一个连通块）  
     - 这条额外的边仍然可以让块内的 `AND` 更小，只需 `and_val[ru] &= w`。

3. **处理查询**  
   - 对每个查询 `[s, t]`，若 `find(s) != find(t)` → `-1`。  
   - 否则答案就是 `and_val[find(s)]`（根节点的 `AND`）。

**为什么 DSU 能做到 O(α(n))**：

- **路径压缩**：在 `find` 时把沿途的所有节点直接挂到根上，后面的查询就更快。  
- **按秩合并**（或按大小合并）：总是把小集合挂到大集合下，保证树的深度很小。

#### 代码（Python）

```python
from typing import List

class DSU:
    def __init__(self, n: int, all_ones: int):
        self.parent = list(range(n))
        self.rank = [0] * n          # 按秩合并使用的高度近似值
        self.and_val = [all_ones] * n   # 每个根维护的 “该集合所有边权的 AND”

    def find(self, x: int) -> int:
        """路径压缩查根"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int, w: int):
        """
        合并两个集合，同时把新加入的边权 w 计入 AND。
        这里假设 x、y 已经是根。
        """
        # 先把边权 w 合并进两个集合的 AND
        new_and = self.and_val[x] & self.and_val[y] & w

        # 按秩合并，保证树的深度尽量小
        if self.rank[x] < self.rank[y]:
            x, y = y, x   # 保证 x 的 rank >= y 的 rank
        self.parent[y] = x
        self.and_val[x] = new_and
        if self.rank[x] == self.rank[y]:
            self.rank[x] += 1

    def apply_inside(self, root: int, w: int):
        """边在同一个集合内部时，只需要把 AND 与 w 再取一次"""
        self.and_val[root] &= w


def min_cost_walk(n: int, edges: List[List[int]], query: List[List[int]]) -> List[int]:
    """
    返回每个查询的最小 walk cost，若不存在则为 -1
    """
    # 所有可能的位数 ≤ 17（因为 10^5 < 2^17），这里多留几位安全起见
    ALL_ONES = (1 << 20) - 1

    dsu = DSU(n, ALL_ONES)

    # 逐条处理边
    for u, v, w in edges:
        ru = dsu.find(u)
        rv = dsu.find(v)
        if ru != rv:
            dsu.union(ru, rv, w)
        else:
            # 已经同属一个连通块，直接把 w 合并进去
            dsu.apply_inside(ru, w)

    # 处理查询
    ans = []
    for s, t in query:
        rs = dsu.find(s)
        rt = dsu.find(t)
        if rs != rt:
            ans.append(-1)
        else:
            ans.append(dsu.and_val[rs])
    return ans
```

> 代码中的每一行都加了中文注释，直接复制到本地即可运行。

#### 复杂度

- **时间复杂度**  
  - 每条边一次 `find`（两次）+ 可能一次 `union` → `O(E * α(n))`。  
  - 每个查询一次 `find` → `O(Q * α(n))`。  
  - `α(n)` 是 **反阿克曼函数**，几乎可以视作常数（≤ 5）。  
  - 整体是 `O((E + Q) * α(n))`，在本题约等于线性 `O(E + Q)`，远快于暴力。

- **空间复杂度**  
  - DSU 需要 `parent、rank、and_val` 三个长度为 `n` 的数组 → `O(n)`。  
  - 额外的 `edges` 与 `query` 本身已经是输入，算作 `O(E + Q)`。  
  - 整体 `O(n + E + Q)`，完全符合限制。

> 与暴力解相比，时间从“指数级”降到了“线性”，空间也从“指数级”降到了“线性”，这就是最优解的威力。

---

## 心得

- **核心技巧**：**按位与的单调性 + 连通块的全部边权 AND**。  
  只要把所有能访问的边都“强行加入”到走法里，得到的 AND 就是最小可能值。  

- **适用的题型**（类似思路）  
  1. **最小/最大路径异或**（利用异或的可逆性与前缀异或）。  
  2. **在连通块内部求公共属性**（如最小公共祖先、公共颜色等）。  
  3. **把所有可用资源都“使用一次”来压低结果**（如最小公共位、最小公共因子等）。

- **一句话总结解题钥匙**  
  > “**在同一连通块里，答案等于该块所有边权的按位与**”。  

---

## 反思

- **拿到题目第一反应**  
  看到“走可以重复，费用是 `&`”，立刻想到“把所有能走的边都加进去会把费用压到最低”。于是把问题转化为“连通块内部的所有边权”。  

- **最容易踩的坑**  
  1. **忘记同一个连通块内部的额外边也会影响 AND**。仅在 `union` 时更新会漏掉已经在同一集合的后续边。  
  2. **初始化 AND 时使用全 1 而不是 0**。因为 `x & 0 = 0` 会把答案直接逼成 0，导致错误。  
  3. **位数不够**：如果把 `ALL_ONES` 设得太小（比如 `1<<17`），而实际权值可能用到更高位，就会把本该保留的位错误地清零。  

- **下次遇到同类题，第一步该想到**  
  > “**是否可以把所有可达的元素一次性合并，然后用集合属性（AND、OR、XOR、最大值、最小值等）直接得到答案？**”  

这样思路一旦形成，往往可以把看似复杂的路径问题转化为 **并查集 + 集合属性维护**，实现既简洁又高效的解法。