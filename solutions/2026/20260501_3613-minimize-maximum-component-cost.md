# #3613. 最小化最大组件代价 / Minimize Maximum Component Cost

> 难度：中等 · 标签：Binary Search、Sort、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/minimize-maximum-component-cost/)

---

## 题目（英文原版）

**Description**

You are given an undirected connected graph with n nodes labeled from 0 to n - 1 and a 2D integer array edges where edges[i] = [ui, vi, wi] denotes an undirected edge between node ui and node vi with weight wi, and an integer k.
You are allowed to remove any number of edges from the graph such that the resulting graph has at most k connected components.
The cost of a component is defined as the maximum edge weight in that component. If a component has no edges, its cost is 0.
Return the minimum possible value of the maximum cost among all components after such removals.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[0,1,4],[1,2,3],[1,3,2],[3,4,6]], k = 2
Output: 4
Explanation:
```

**Example 2:**

```
Input: n = 4, edges = [[0,1,5],[1,2,5],[2,3,5]], k = 1
Output: 5
Explanation:
```

**Constraints**

- 1 <= n <= 5 * 104
- 0 <= edges.length <= 105
- edges[i].length == 3
- 0 <= ui, vi < n
- 1 <= wi <= 106
- 1 <= k <= n
- The input graph is connected.

---

## 题目（中文翻译）

**题目描述**  
给定一个标号为 `0` 到 `n-1` 的无向连通图，以及一个二维整数数组 `edges`，其中 `edges[i] = [ui, vi, wi]` 表示节点 `ui` 与节点 `vi` 之间的一条权重为 `wi` 的无向边，另给定整数 `k`。  
你可以从图中删除任意数量的边，使得最终图的连通分量（connected components）数目不超过 `k`。  
一个连通分量的代价（cost）定义为该分量中所有边的最大权重。如果一个分量中没有边，则其代价为 `0`。  
返回在上述删除操作后，所有连通分量的最大代价的最小可能值。

**示例**

**示例 1**  
```
Input: n = 5, edges = [[0,1,4],[1,2,3],[1,3,2],[3,4,6]], k = 2
Output: 4
Explanation:
```

**示例 2**  
```
Input: n = 4, edges = [[0,1,5],[1,2,5],[2,3,5]], k = 1
Output: 5
Explanation:
```

**约束条件**  
- $1 \le n \le 5 \times 10^4$
- $0 \le \text{edges.length} \le 10^5$
- $\text{edges}[i].\text{length} = 3$
- $0 \le ui, vi < n$
- $1 \le wi \le 10^6$
- $1 \le k \le n$
- 输入的图是连通的。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的删边方案枚举一遍**，然后在每种方案下计算得到的连通块数以及每个块的最大边权，取所有方案中“最大块成本”最小的那个。  

- **数据结构**  
  - **邻接表**：把图存成 `adj[u] = [(v, w), …]`，类似于我们平时查字典，键是节点，值是它的邻居列表。  
  - **DFS / BFS**：遍历连通块，就像我们在地图上找所有相连的城市。  

- **为什么正确**  
  枚举了**所有**合法的删边方式，必然会覆盖最优解；每一次遍历都能得到真实的连通块和对应的最大边权，所以最终取最小的“最大块成本”一定是答案。

- **复杂度分析（大白话）**  
  - 枚举删边的组合数是 `2^{|edges|}`（每条边保留或删除），这就像把 20 条边的开关全打开关一次要 1,048,576 次，边数稍大就根本不可能跑完。  
  - 对每一种组合，我们都要做一次完整的 DFS，时间是 `O(n + |edges|)`。  
  - 综合下来，时间复杂度是 **指数级**，记作 `O(2^m * (n+m))`（这里的 `m` 是边数），在最坏情况下会远远超出 1 秒的限制。  
  - 空间上只需要保存图和递归栈，`O(n + m)`。

#### 代码（Python）

```python
from itertools import product
from collections import defaultdict, deque

def min_max_component_cost_bruteforce(n, edges, k):
    m = len(edges)
    best = float('inf')

    # edges_idx[i] = (u, v, w)
    for keep_mask in product([0, 1], repeat=m):          # 0 表示删，1 表示保留
        # 只保留最多 k-1 条删边（因为最多 k 个连通块 => 最少 n-k 条保留边）
        # 这里不做剪枝，仅作演示
        adj = defaultdict(list)
        for keep, (u, v, w) in zip(keep_mask, edges):
            if keep:
                adj[u].append((v, w))
                adj[v].append((u, w))

        # 统计连通块及每块的最大边权
        visited = [False] * n
        comps = 0
        max_cost = 0

        for start in range(n):
            if not visited[start]:
                comps += 1
                q = deque([start])
                visited[start] = True
                cur_max = 0
                while q:
                    u = q.popleft()
                    for v, w in adj[u]:
                        cur_max = max(cur_max, w)     # 记录块内最大权重
                        if not visited[v]:
                            visited[v] = True
                            q.append(v)
                max_cost = max(max_cost, cur_max)      # 记录所有块的最大成本

        if comps <= k:
            best = min(best, max_cost)

    return best
```

> **注意**：上述代码只用于解释暴力思路，实际运行会超时。

#### 复杂度

- **时间复杂度**：`O(2^m * (n + m))`，指数级增长，几乎不可能在真实数据上通过。  
  - 大白话：想象每条边都有一个开关，所有开关的组合数就是 2 的边数次方，几乎是“天文数字”。  
- **空间复杂度**：`O(n + m)`，只需要存图和访问标记。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有删边方案是不可行的**。我们需要找到一种“判断是否可行”的方法，然后利用**二分搜索**快速定位答案。

**关键观察**  

1. **如果我们只允许使用权重 ≤ X 的边**，那么所有权重大于 X 的边一定会被删除。此时图会被划分成若干连通块。  
2. 只要这些块的数量 **≤ k**，说明我们可以在 “最大块成本 ≤ X” 的前提下得到不超过 k 个块（因为可以再随意删掉一些 ≤ X 的边，块数只会增大）。  
3. 换句话说，**判断 X 是否可行** = “在只保留 ≤ X 的边时，连通块数是否 ≤ k”。  

**如何快速判断**  

- 将所有边按权重从小到大排序。  
- 使用 **并查集（DSU）**（像是“查字典”，每个节点是词，根节点是词所在的页码），遍历排序后的边，只把 **权重 ≤ X** 的边合并。  
- 合并完后，DSU 中不同根的数量就是连通块数。  

**二分搜索**  

- 权重的取值范围是 `[0, max_edge_weight]`（0 表示不使用任何边，所有单点块成本为 0）。  
- 在这个区间上做二分，每次取中点 `mid`，调用上面的“可行性检查”。  
- 若 `mid` 可行，则说明答案不大于 `mid`，继续在左半区搜索；否则在右半区搜索。  

**完整流程**  

1. 读取所有边，记下最大权重 `max_w`。  
2. 对边按权重升序排序。  
3. 二分搜索 `low = 0, high = max_w`：  
   - `mid = (low + high) // 2`。  
   - 用 DSU 合并所有 `w ≤ mid` 的边，统计根的数量 `components`。  
   - 若 `components ≤ k` → `high = mid`（答案可能更小）。  
   - 否则 `low = mid + 1`。  
4. 循环结束时 `low`（或 `high`）即为最小的“最大块成本”。  

**为什么对 DSU 合并是 O(m α(n))**  

- `α(n)` 是 Ackermann 反函数，几乎可以认为是常数（比如 4），所以 DSU 的合并和查询几乎是 **线性** 的。  

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集（Disjoint Set Union）"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点的“父亲”，一开始指向自己
        self.rank = [0] * n            # 用来平衡树的高度（可选优化）

    def find(self, x: int) -> int:
        # 路径压缩：递归寻找根的同时，把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        # 按秩合并：把低秩的根挂到高秩的根下，保持树矮一点
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1

def min_max_component_cost(n: int, edges: List[List[int]], k: int) -> int:
    """
    二分答案 + DSU
    :param n: 节点数
    :param edges: [[u, v, w], ...]
    :param k: 最多允许的连通块数
    :return: 最小可能的最大块成本
    """
    if not edges:          # 没有边，所有块成本都是 0
        return 0

    # 1️⃣ 按权重升序排序
    edges.sort(key=lambda e: e[2])
    max_w = edges[-1][2]   # 最大权重，二分的上界

    # 2️⃣ 二分搜索答案
    low, high = 0, max_w
    while low < high:
        mid = (low + high) // 2

        # 3️⃣ 用 DSU 合并所有权重 <= mid 的边
        dsu = DSU(n)
        for u, v, w in edges:
            if w > mid:          # 已经超过当前阈值，后面的边更大，直接跳出循环
                break
            dsu.union(u, v)

        # 统计连通块数量：根的不同个数
        roots = set()
        for i in range(n):
            roots.add(dsu.find(i))
        components = len(roots)

        # 4️⃣ 根据块数决定二分区间
        if components <= k:      # 可以在 “最大成本 ≤ mid” 的前提下得到 ≤ k 块
            high = mid           # 继续往左找更小的可能
        else:
            low = mid + 1        # 需要更大的阈值才能把块数降到 ≤ k

    return low
```

> **代码要点**  
> - `edges.sort(key=lambda e: e[2])` 把边的权重从小到大排列，类似把书按照页码从前往后排好，后面遍历时可以“一遇到大于阈值的就停”。  
> - `while low < high` 是经典的 **闭区间二分** 写法，循环结束时 `low == high` 即为答案。  
> - `roots` 集合用来统计 DSU 中有多少不同的根，根的数量就是连通块数。

#### 复杂度

- **时间复杂度**：`O( (n + m) * log W )`  
  - `log W` 是二分的次数，`W` 为最大边权（ ≤ 10⁶），所以最多约 20 次。  
  - 每次二分我们遍历一次已排序的边并做 DSU 合并，复杂度近似 `O(m α(n))`，α(n) 近似常数。  
  - 大白话：我们只需要 **20 次** “把所有边按阈值合并一次”，每次都像扫一次超市的商品条形码，速度很快。

- **空间复杂度**：`O(n + m)`  
  - 存储排序后的边列表 `O(m)`，以及 DSU 的 `parent`、`rank` 数组 `O(n)`。  

---

## 心得

- **核心技巧**：**二分答案 + 并查集**。先把“是否可行”转化为一个单调判定问题（阈值越大，可行性越强），再用二分快速定位最小可行阈值；并查集负责在每次判定时高效统计连通块数。  
- **适用题型**  
  1. “在图上删边/加边，使得某个属性（如最大边权、直径等）最小”——如 **Minimum Score of a Path Between Two Cities**。  
  2. “在数列/区间上满足单调性条件的最小/最大值”，常用二分答案配合前缀和或滑动窗口。  
  3. “把元素划分成若干组，使得每组的某个指标 ≤ X”，如 **Split Array Largest Sum**。  
- **一句话总结解题钥匙**：把“最大成本 ≤ X”变成“只保留 ≤ X 的边”，利用 DSU 检查连通块数是否满足 k，二分寻找最小 X。

---

## 反思

- **第一反应**：看到“最大块成本”和“可以删任意边”，立刻想到 **“把大权重的边都删掉”**，于是想到二分阈值。  
- **最容易踩的坑**  
  - **边权为 0 的情况**：如果 `k = n`，答案应该是 0，需要在二分下界设为 0 而不是最小边权。  
  - **排序后提前退出**：在判定时一旦遇到 `w > mid` 必须立即 `break`，否则会把不该算的边也加入 DSU，导致块数错误。  
  - **并查集的路径压缩**：若忘记 `find` 中的递归压缩，时间会慢到接近 `O(n log n)`，在极限数据下可能超时。  
- **下次类似题的第一步**：先判断是否可以把“目标属性 ≤ X”转化为“只保留满足某单调条件的元素”，如果可以，就立刻构造 **单调判定函数**，准备二分搜索。