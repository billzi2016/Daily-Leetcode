# #3608. 最小时间使得出现 K 连通分量 / Minimum Time for K Connected Components

> 难度：中等 · 标签：Binary Search、Union Find、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-time-for-k-connected-components/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an undirected graph with n nodes labeled from 0 to n - 1. This is represented by a 2D array edges, where edges[i] = [ui, vi, timei] indicates an undirected edge between nodes ui and vi that can be removed at timei.
You are also given an integer k.
Initially, the graph may be connected or disconnected. Your task is to find the minimum time t such that after removing all edges with time <= t, the graph contains at least k connected components.
Return the minimum time t.
A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.

**Examples**

**Example 1:**

```
Input: n = 2, edges = [[0,1,3]], k = 2
Output: 3
Explanation:
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,2],[1,2,4]], k = 3
Output: 4
Explanation:
```

**Example 3:**

```
Input: n = 3, edges = [[0,2,5]], k = 2
Output: 0
Explanation:
```

**Constraints**

- 1 <= n <= 105
- 0 <= edges.length <= 105
- edges[i] = [ui, vi, timei]
- 0 <= ui, vi < n
- ui != vi
- 1 <= timei <= 109
- 1 <= k <= n
- There are no duplicate edges.

---

## 题目（中文翻译）

**描述**  
给定一个整数 `n` 和一张包含 `n` 个节点（编号为 `0` 到 `n - 1`）的无向图（undirected graph），图由二维数组 `edges` 表示，其中 `edges[i] = [ui, vi, timei]` 表示节点 `ui` 与节点 `vi` 之间存在一条无向边，该边可以在时间点 `timei` 被移除。  
同时给定一个整数 `k`。

最初图可能是连通的，也可能是非连通的。请找出最小的时间点 `t`，使得在移除所有 `time ≤ t` 的边之后，图中至少存在 `k` 个连通分量（connected component）。返回该最小时间 `t`。

连通分量的定义：在图的一个子图中，任意两点之间都有路径相通，且该子图的任意顶点都不与子图外的顶点共享边。

**示例**

**示例 1**  
输入: `n = 2, edges = [[0,1,3]], k = 2`  
输出: `3`  
解释:

**示例 2**  
输入: `n = 3, edges = [[0,1,2],[1,2,4]], k = 3`  
输出: `4`  
解释:

**示例 3**  
输入: `n = 3, edges = [[0,2,5]], k = 2`  
输出: `0`  
解释:

**约束条件**  
- `1 <= n <= 10^5`  
- `0 <= edges.length <= 10^5`  
- `edges[i] = [ui, vi, timei]`  
- `0 <= ui, vi < n`  
- `ui != vi`  
- `1 <= timei <= 10^9`  
- `1 <= k <= n`  
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的时间点都枚举一遍**，对每一个时间 `t`：

1. 把所有 `time ≤ t` 的边「删除」——实际上我们只保留 `time > t` 的边。  
2. 用 **并查集（Union‑Find）** 把剩下的边连起来，统计最后有多少个连通分量。  
3. 看这个分量数是否已经 **≥ k**，如果是，记录下 `t`。

> **并查集类比**：想象你有一本词典，单词是 **节点**，词典的“查找”过程就是把两个单词所在的页码（根节点）合并在一起。`find` 找根，`union` 把两本小词典合并成一本大词典。

为什么这一步一定能得到正确答案？

- 对每个 `t`，我们都严格按照「删除所有 `time ≤ t` 的边」的规则重新构造图；
- 并查集能完整地把所有仍在的边连通起来，得到的连通分量数就是题目要求的「当前的组件数」；
- 因此只要遍历所有可能的 `t`，必然能找到最小的满足条件的 `t`。

**时间/空间复杂度**（大白话版）：

- 假设图里有 `m` 条边。我们把 **每一个不同的时间**（最坏情况下是 `m` 个）都跑一遍。每次跑都要遍历所有 `m` 条边去并查集合并一次。于是总共要做 `m × m` 次操作，也就是 **O(m²)**。  
  - 形象点说：如果有 10,000 条边，暴力解大约要进行 100,000,000 次「合并」操作，明显会超时。
- 并查集本身只保存 `n` 个节点的父指针和秩（rank），所以 **O(n)** 的额外空间。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点先自己是根
        self.rank = [0] * n            # 按秩合并，防止树太高
        self.components = n           # 初始时有 n 个独立的组件

    def find(self, x: int) -> int:
        # 路径压缩：把查找路径上的所有节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:                     # 已经在同一个集合，不用再合并
            return
        # 按秩合并，保证树的高度尽量小
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1            # 合并成功，组件数减一

def minTime_bruteforce(n: int, edges: List[List[int]], k: int) -> int:
    # 取所有出现的时间点（包括 0，因为可以在不删任何边时检查）
    times = sorted({0} | {t for _, _, t in edges})
    for t in times:                     # 逐个尝试时间阈值
        uf = UnionFind(n)
        # 只保留 time > t 的边，模拟“删除 time ≤ t 的边”
        for u, v, time in edges:
            if time > t:                # 这条边还在
                uf.union(u, v)
        if uf.components >= k:          # 已经满足 k 个或更多组件
            return t
    return -1   # 根据题意一定会有答案，这行其实不会被执行
```

#### 复杂度

- **时间复杂度**：`O(m²)`  
  - 解释：我们遍历了 `O(m)` 个不同的时间，每一次都要遍历全部 `m` 条边并做并查集合并。
- **空间复杂度**：`O(n)`  
  - 解释：并查集只保存 `n` 个父指针和秩，和时间 `t` 的枚举无关。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于「每一次都重新遍历全部边」。其实，**判断某个阈值 `t` 是否可行** 只需要一次遍历：把 **所有 `time > t` 的边** 加入并查集，统计得到的连通分量数即可。  
这就把「检查」的代价降到了 **O(m)**。

接下来我们要找 **最小的 `t`** 使得组件数 `≥ k`。观察到：

- 随着 `t` **增大**，被删除的边会 **越来越多**，剩下的边会 **越来越少**，连通分量数 **只会单调不减**（拆得越多，组件越多或保持不变）。
- 单调性恰好可以用 **二分搜索**（Binary Search）来快速定位最小满足条件的 `t`。

整体思路：

1. 先把所有边的 `time` 收集起来，得到搜索范围 `[0, max_time]`（`0` 表示「不删任何边」）。
2. 对这个时间区间做二分搜索：
   - 取中点 `mid`，**只遍历一次**所有边，把 `time > mid` 的边加入并查集，得到当前的组件数 `cnt`。
   - 若 `cnt >= k`，说明 `mid` 已经够大，可以尝试更小的时间，于是把右边界收缩到 `mid`。
   - 否则 `mid` 仍然太小，右移左边界到 `mid + 1`。
3. 循环结束时左边界就是最小满足条件的时间。

> **二分搜索类比**：想象你在一本排好序的字典里找第一个出现「至少 k 页」的词。因为词的页码是递增的，你可以每次跳到中间的词检查页数，如果已经够多，就往左找更早的词；不够就往右找更晚的词。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # 路径压缩（两层跳）
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1

def can_split(n: int, edges: List[List[int]], k: int, limit: int) -> bool:
    """
    判断在删除所有 time <= limit 的边后，连通分量是否已经 >= k
    """
    uf = UnionFind(n)
    for u, v, t in edges:
        if t > limit:                # 只保留比 limit 更大的边
            uf.union(u, v)
    return uf.components >= k

def minTime_optimal(n: int, edges: List[List[int]], k: int) -> int:
    # 若一开始（不删任何边）已经满足 k，直接返回 0
    if can_split(n, edges, k, 0):
        return 0

    # 二分搜索的上下界
    lo = 0
    hi = max(t for _, _, t in edges)   # 最大的 time 必然可以把所有边都删掉

    while lo < hi:
        mid = (lo + hi) // 2
        if can_split(n, edges, k, mid):
            hi = mid                     # 还能往左走，收紧右边界
        else:
            lo = mid + 1                 # 还不够，左边界右移
    return lo
```

#### 复杂度

- **时间复杂度**：`O(m log T)`  
  - `log T` 是二分搜索的轮数，`T` 为最大时间值（`≤ 10⁹`），所以最多约 30 次。每一次检查只遍历一次全部 `m` 条边并做并查集合并，故总体是 `m × log T`。  
  - 与暴力的 `O(m²)` 相比，**速度提升了数量级**（例如 `m = 10⁵` 时，`m log T ≈ 3·10⁶`，完全可以在 1 秒内跑完）。
- **空间复杂度**：`O(n)`  
  - 只需存并查集的父指针、秩和组件计数。二分搜索本身只使用常数额外空间。

---

## 心得

- **核心技巧**：**二分搜索 + 并查集**。二分利用了「删除边后组件数单调不减」的性质，并查集快速统计在给定阈值下的连通分量数。
- **适用的题型**  
  1. “在某个阈值下，图的某种属性是否满足”类题目（如最小生成树的最大边权、删边后是否连通等）。  
  2. “满足单调条件的最小/最大值”搜索类题目（如“最小阈值使得图中有 ≥ k 条路径”）。  
  3. 需要在 **动态** 边集合中快速查询连通性时，使用并查集配合 **离线** 或 **二分** 手段（如 “删除/添加边后是否仍连通”）。
- **一句话总结解题钥匙**：**把“检查可行性”压到一次线性遍历，然后在单调的时间轴上二分定位最小满足条件的点**。

---

## 反思

- **第一反应**：直接把每个时间点都模拟一次，求每次的连通分量数——这就是暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：如果一开始就已经有 `k` 个组件，需要返回 `0`（不要忘记这一步的提前检查）。  
  - **时间上界**：二分搜索的右边界必须是 **所有边的最大 time**，否则可能找不到答案。  
  - **并查集的初始化**：每次二分检查都要重新创建一个干净的并查集，否则残留的合并信息会导致错误计数。  
- **下次遇到同类题**：第一步先确认“随着阈值变化，目标属性是否单调”。如果是，就立刻想到 **二分 + 线性检查**（常配合并查集、前缀和、滑动窗口等数据结构）。这样可以把时间复杂度从 `O(m²)` 降到 `O(m log range)`，轻松通过大数据规模的限制。