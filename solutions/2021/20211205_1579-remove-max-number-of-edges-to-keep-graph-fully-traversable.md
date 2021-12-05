# #1579. 删除最多的边以保持图的可完全遍历性 / Remove Max Number of Edges to Keep Graph Fully Traversable

> 难度：困难 · 标签：Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/)

---

## 题目（英文原版）

**Description**

Alice and Bob have an undirected graph of n nodes and three types of edges:
Given an array edges where edges[i] = [typei, ui, vi] represents a bidirectional edge of type typei between nodes ui and vi, find the maximum number of edges you can remove so that after removing the edges, the graph can still be fully traversed by both Alice and Bob. The graph is fully traversed by Alice and Bob if starting from any node, they can reach all other nodes.
Return the maximum number of edges you can remove, or return -1 if Alice and Bob cannot fully traverse the graph.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]
Output: 2
Explanation: If we remove the 2 edges [1,1,2] and [1,1,3]. The graph will still be fully traversable by Alice and Bob. Removing any additional edge will not make it so. So the maximum number of edges we can remove is 2.
```

**Example 2:**

```
Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]
Output: 0
Explanation: Notice that removing any edge will not make the graph fully traversable by Alice and Bob.
```

**Example 3:**

```
Input: n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]
Output: -1
Explanation: In the current graph, Alice cannot reach node 4 from the other nodes. Likewise, Bob cannot reach 1. Therefore it's impossible to make the graph fully traversable.
```

**Constraints**

- 1 <= n <= 105
- 1 <= edges.length <= min(105, 3 * n * (n - 1) / 2)
- edges[i].length == 3
- 1 <= typei <= 3
- 1 <= ui < vi <= n
- All tuples (typei, ui, vi) are distinct.

---

## 题目（中文翻译）

Alice 和 Bob 拥有一个 **无向图**（undirected graph），图中有 `n` 个节点，且存在三种类型的边：

给定数组 `edges`，其中 `edges[i] = [type_i, u_i, v_i]` 表示一条 **双向边**（bidirectional edge），类型为 `type_i`，连接节点 `u_i` 与 `v_i`。请找出最多可以删除多少条边，使得在删除这些边之后，**Alice 和 Bob 都仍然能够完全遍历图**（fully traversed）。  
如果从任意节点出发，Alice（或 Bob）都能够到达所有其他节点，则称该图对 Alice（或 Bob）是 **完全遍历**（fully traversable）的。  
返回可以删除的最大边数；如果无论如何都无法使 Alice 和 Bob 同时完全遍历图，则返回 `-1`。

## 示例

### 示例 1
**输入**  
```
n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]
```
**输出**  
```
2
```
**解释**  
如果删除边 `[1,1,2]` 和 `[1,1,3]`，图仍然可以被 Alice 和 Bob 完全遍历。再删除任意一条边就会破坏这种可遍历性。因此，最多可以删除的边数是 `2`。

### 示例 2
**输入**  
```
n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]
```
**输出**  
```
0
```
**解释**  
任意删除一条边都会导致 Alice 或 Bob 无法完全遍历图，所以最多只能删除 `0` 条边。

### 示例 3
**输入**  
```
n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]
```
**输出**  
```
-1
```
**解释**  
在当前图中，Alice 无法从其他节点到达节点 `4`，同理 Bob 也无法到达节点 `1`。因此不可能使图对两人都完全遍历，返回 `-1`。

## 约束条件
- `1 <= n <= 10^5`
- `1 <= edges.length <= min(10^5, 3 * n * (n - 1) / 2)`
- `edges[i].length == 3`
- `1 <= type_i <= 3`
- `1 <= u_i < v_i <= n`
- 所有三元组 `(type_i, u_i, v_i)` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一条边都尝试删掉一次**，然后检查删完以后 Alice 和 Bob 能否仍然遍历整个图。  
具体步骤：

1. 先把原始的 `edges` 复制一份 `edges_copy`。  
2. 对于 `edges_copy` 中的每一条边 `e`  
   * 把 `e` 从列表里暂时删掉（相当于“移除”这条边）。  
   * 用 **DFS / BFS** 分别在只保留 Alice 能使用的边（type 1 + type 3）和只保留 Bob 能使用的边（type 2 + type 3）上做一次遍历，判断图是否仍然是连通的（从任意节点都能走到所有节点）。  
   * 如果两个人都还能遍历完整图，就把这条边记为“可删”。否则这条边必须留下。  
3. 最后把所有“可删”的边数相加，就是可以删除的最大数量。  

> **类比**：把图想成一座城市的道路网络，想把一些路段封闭。我们逐条把路段封闭后，派两支救援队（Alice、Bob）去检查能否仍然从任意出发点到达所有地点。如果两支队伍都能走通，说明这条路段可以安全封闭。

这个方法之所以 **正确**，是因为我们枚举了所有可能的单条删除情况，并且每次都用完整的连通性检查验证。只要某条边真的可以被删除，它一定会在我们枚举时被标记为可删。

不过它 **没有考虑** 同时删除多条边的组合，只是统计每条单独删掉是否安全。实际上，若两条边分别单独删掉都安全，但一起删可能导致不连通，这种情况在本题中不会出现（因为我们只需要“最大可删数”，只要每条单独删安全，全部删掉也是安全），但遍历所有子集的完整暴力仍然是指数级的。

#### 代码（Python）

```python
from collections import defaultdict, deque
from copy import deepcopy
from typing import List

def bfs(start: int, adj: dict, n: int) -> bool:
    """从 start 出发，用 BFS 看能否遍历到所有 n 个节点"""
    visited = [False] * (n + 1)
    q = deque([start])
    visited[start] = True
    cnt = 1                     # 已访问节点数
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                cnt += 1
                q.append(v)
    return cnt == n             # 所有节点都被访问到说明连通

def can_traverse(edges: List[List[int]], n: int, person_type: int) -> bool:
    """
    检查某个人（person_type = 1 表示 Alice，只能用 type1+type3；
                    person_type = 2 表示 Bob，只能用 type2+type3）是否能遍历全图
    """
    adj = defaultdict(list)
    for t, u, v in edges:
        if t == 3 or t == person_type:   # 该人可以使用的边
            adj[u].append(v)
            adj[v].append(u)
    # 任意选一个节点（这里选 1），如果 n==0 则直接返回 True
    return bfs(1, adj, n)

def max_num_edges_to_remove_bruteforce(n: int, edges: List[List[int]]) -> int:
    total = len(edges)
    removable = 0

    # 逐条尝试删除
    for i in range(total):
        # 复制一份边列表并删除第 i 条
        new_edges = edges[:i] + edges[i+1:]

        # 检查 Alice 和 Bob 是否仍然能遍历全图
        if can_traverse(new_edges, n, 1) and can_traverse(new_edges, n, 2):
            removable += 1          # 这条边可以安全删除
        # 否则必须保留，继续检查下一条

    return removable
```

> **运行说明**：  
> - `bfs` 用来判断一个子图是否连通。  
> - `can_traverse` 根据人的类型挑选可用的边，构造邻接表后调用 `bfs`。  
> - 主函数 `max_num_edges_to_remove_bruteforce` 逐条尝试删除并计数。

#### 复杂度  

- **时间复杂度**：  
  对每条边我们都要重新做两次 BFS（一次检查 Alice，一次检查 Bob）。  
  BFS 的复杂度是 `O(n + m)`，其中 `m` 是当前剩余边数。  
  因此整体是 `O(m * (n + m))`，在最坏情况下约等于 `O(m²)`。  
  用大白话说，就是“如果边很多，时间会像平方一样迅速增长”，对 `10⁵` 级别的数据根本跑不完。

- **空间复杂度**：  
  需要存储邻接表和访问数组，大小为 `O(n + m)`。  
  这在本题的规模下是可以接受的，但配合上面的时间复杂度，整体仍然不可行。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**每次都重新遍历整个图**，而我们其实可以**一次性把所有必须保留的边找出来**，剩下的自然就是可以删除的边。  

关键观察：

1. **类型 3 的边**（Alice & Bob 都能用）是最有价值的。  
   - 如果我们把一条类型 3 的边加入两个人的网络，它可以同时帮助 Alice 和 Bob 连接两个连通块。  
   - 因此**先处理所有类型 3 的边**，尽可能让两个人的图都变得更连通。

2. 处理完类型 3 后，**分别用类型 1（只给 Alice）和类型 2（只给 Bob）补齐各自的连通性**。  
   - 对每个人来说，最终要形成一棵**生成树**（spanning tree），即 `n‑1` 条边就可以把 `n` 个节点全部连通。  
   - 这棵树里已经包含了所有被使用的类型 3 边，剩下的缺口只能用各自专属的边来填。

3. 判断是否可行：  
   - 当我们完成所有合并后，如果 **Alice 的并查集** 还有多于 1 个连通块，说明她仍然无法遍历全图；同理 Bob 也是。  
   - 这时返回 `-1`。

4. 计算答案：  
   - 所有 **被使用的边**（无论是哪种类型）数量记为 `used`。  
   - 最大可删除的边数 = `total_edges - used`。  

> **并查集（Disjoint Set Union, DSU）类比**：  
> 想象每个节点是一张卡片，卡片上写着它所属的“部落”。  
> - `find(x)` 就是查找 x 所在的部落（根卡片）。  
> - `union(x, y)` 就是把两个不同部落合并成一个更大的部落。  
> 使用路径压缩（把查找路径上的卡片直接指向根部落）和按秩合并（把小部落挂到大部落下）可以让这两个操作几乎是常数时间。

**步骤细化**：

| 步骤 | 说明 |
|------|------|
| 1️⃣ 初始化 | 为 Alice 和 Bob 各自创建一个 DSU，初始时每个节点自成一个集合。 |
| 2️⃣ 处理 type = 3 边 | 遍历所有 type = 3 的边，尝试把 `u`、`v` 合并到 **两个人** 的 DSU 中。<br>如果 `u` 与 `v` 已经在同一个集合里（即已经连通），这条边是**冗余**的，可以直接计为可删除。 |
| 3️⃣ 处理 type = 1 边 | 只在 Alice 的 DSU 上尝试合并。若 `u`、`v` 已经连通，这条边也是冗余的。 |
| 4️⃣ 处理 type = 2 边 | 同理，只在 Bob 的 DSU 上尝试合并。 |
| 5️⃣ 检查连通性 | 判断 Alice 和 Bob 的 DSU 中根的数量是否都为 1（即 `components == 1`）。若不是，返回 `-1`。 |
| 6️⃣ 计算答案 | `ans = total_edges - used_edges`（其中 `used_edges` 是在合并过程中实际成功加入的边数）。 |

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集（Disjoint Set Union）实现"""
    def __init__(self, n: int):
        self.parent = list(range(n + 1))   # 每个节点的父节点，初始指向自己
        self.rank = [0] * (n + 1)          # 按秩合并时使用的深度近似
        self.components = n               # 当前连通块数量

    def find(self, x: int) -> int:
        """路径压缩：查找根节点，同时把沿途的节点直接挂到根上"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压缩路径
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """尝试合并两个集合，返回是否真的合并成功（即原本不连通）"""
        xr, yr = self.find(x), self.find(y)
        if xr == yr:                     # 已经在同一个集合，合并无效
            return False

        # 按秩合并：把秩小的根挂到秩大的根下
        if self.rank[xr] < self.rank[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        if self.rank[xr] == self.rank[yr]:
            self.rank[xr] += 1
        self.components -= 1             # 连通块数量减一
        return True

def max_num_edges_to_remove(n: int, edges: List[List[int]]) -> int:
    """
    返回可以删除的最大边数，若两人都无法遍历全图则返回 -1
    """
    # 1️⃣ 为 Alice 和 Bob 各建一个 DSU
    dsu_alice = DSU(n)
    dsu_bob   = DSU(n)

    used = 0          # 实际被保留下来的边数

    # 2️⃣ 先处理 type = 3 的公共边
    for t, u, v in edges:
        if t == 3:
            # 只要任意一方能把 u、v 合并成功，就算这条边被使用
            merged_alice = dsu_alice.union(u, v)
            merged_bob   = dsu_bob.union(u, v)
            if merged_alice or merged_bob:
                used += 1               # 这条边对至少一方有帮助，计为必选
            # 若两者都已经连通，则这条边是冗余的，直接算作可删除（不计入 used）

    # 3️⃣ 处理只给 Alice 的边（type = 1）
    for t, u, v in edges:
        if t == 1:
            if dsu_alice.union(u, v):   # 成功合并说明这条边是必要的
                used += 1

    # 4️⃣ 处理只给 Bob 的边（type = 2）
    for t, u, v in edges:
        if t == 2:
            if dsu_bob.union(u, v):
                used += 1

    # 5️⃣ 检查两个人是否都已经连通整个图
    if dsu_alice.components != 1 or dsu_bob.components != 1:
        return -1               # 任意一方还有多个连通块，说明不可行

    # 6️⃣ 计算可删除的最大边数
    return len(edges) - used
```

**代码要点解释**：

- `DSU` 的 `components` 用来实时记录还有多少个连通块，最终判断是否等于 `1`（即全连通）。  
- 处理类型 3 边时，**只要有一方成功合并**（`merged_alice or merged_bob` 为真），我们就把这条边计入 `used`。因为这条公共边对至少一方是必需的，若两者都已经在同一个集合里，这条边就是多余的，直接算作可以删除。  
- 类型 1、2 边只在对应的 DSU 中尝试合并，成功合并则计入 `used`。  
- 最后 `len(edges) - used` 即为**最大可删边数**。

#### 复杂度  

- **时间复杂度**：  
  - 我们只遍历 `edges` 三次，每次的 `union` / `find` 操作的均摊时间复杂度是 **α(n)**，α 是 Ackermann 函数的反函数，几乎可以视作常数。  
  - 因此整体是 `O(m * α(n))`，在实际中可以写成 `O(m)`。  
  - 用大白话说，就是“和边的数量成线性关系”，即使是 `10⁵` 条边也能在毫秒级完成。

- **空间复杂度**：  
  - 两个 DSU 各需要 `O(n)` 的父节点和秩数组，加上常数级的其他变量，总共是 `O(n)`。  
  - 这比暴力解的 `O(n + m)` 更省（因为我们不需要额外的邻接表）。

---

## 心得

- **核心技巧**：使用并查集（Union‑Find）一次性构造两个人的**最小生成树**，先利用公共边（type 3）最大化共享，然后分别补足各自的专属边。  
- **适用题型**：  
  1. “让图保持连通的最少/最多边数” 类题目（如 LeetCode 1579、1659）。  
  2. 多角色或多层次连通性要求的图论问题（如 “两人分别行走的最小桥梁数”）。  
  3. “删除多余边使图成为森林/树”的问题（如 “删边使图成为树形结构”）。  
- **一句话总结解题钥匙**：**先把所有能被两个人共享的资源（type 3）最大化利用，再用各自专属的资源补齐缺口**。

---

## 反思

- **第一反应**：看到“最大删除边数”立即想到“删边”，于是考虑**枚举删除**，这导致了暴力解的出现。  
- **最容易踩的坑**：  
  - 忽视 **type 3 边的双重作用**，只把它当作普通边会导致重复计数或误判不可连通。  
  - 并查集实现时如果忘记路径压缩或按秩合并，时间会退化到接近 `O(n·m)`，在大数据下会超时。  
  - 统计答案时必须用 **总边数 - 实际使用的边数**，而不是直接统计“被标记为可删的边”，否则会遗漏那些在处理 type 3 时被直接跳过的冗余边。  
- **下次遇到同类题**，第一步应该**思考是否存在一种“公共资源”**（如 type 3 边、共享桥梁、公共路径），并尝试**先利用它们**，再分别处理各自的约束，这样往往能把暴力搜索转化为线性或准线性的并查集/贪心过程。