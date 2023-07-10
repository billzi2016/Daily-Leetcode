# #2316. 无向图中不可达节点对的计数 / Count Unreachable Pairs of Nodes in an Undirected Graph

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/)

---

## 题目（英文原版）

**Description**

You are given an integer n. There is an undirected graph with n nodes, numbered from 0 to n - 1. You are given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
Return the number of pairs of different nodes that are unreachable from each other.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1],[0,2],[1,2]]
Output: 0
Explanation: There are no pairs of nodes that are unreachable from each other. Therefore, we return 0.
```

**Example 2:**

```
Input: n = 7, edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]
Output: 14
Explanation: There are 14 pairs of nodes that are unreachable from each other:
[[0,1],[0,3],[0,6],[1,2],[1,3],[1,4],[1,5],[2,3],[2,6],[3,4],[3,5],[3,6],[4,6],[5,6]].
Therefore, we return 14.
```

**Constraints**

- 1 <= n <= 105
- 0 <= edges.length <= 2 * 105
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- There are no repeated edges.

---

## 题目（中文翻译）

**题目描述**  
给定整数 `n`，表示有 `n` 个节点的无向图，节点编号为 `0` 到 `n - 1`。另给定二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条无向边。  
返回不同节点对中互相不可达的对数。

**示例 1**  
**输入**: `n = 3`, `edges = [[0,1],[0,2],[1,2]]`  
**输出**: `0`  
**解释**: 所有节点之间均可达，因此不存在不可达的节点对，返回 `0`。

**示例 2**  
**输入**: `n = 7`, `edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]`  
**输出**: `14`  
**解释**: 共有 14 对节点互相不可达：  
`[[0,1],[0,3],[0,6],[1,2],[1,3],[1,4],[1,5],[2,3],[2,6],[3,4],[3,5],[3,6],[4,6],[5,6]]`。  
因此返回 `14`。

**约束条件**  
- `1 <= n <= 10^5`  
- `0 <= edges.length <= 2 * 10^5`  
- `edges[i].length == 2`  
- `0 <= a_i, b_i < n`  
- `a_i != b_i`  
- 图中不存在重复的边。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**对每一对不同的节点 (i, j)**，检查它们之间是否存在一条路径。  
- 我们可以把图想成城市之间的道路，**遍历**（DFS/BFS）相当于开车从城市 i 出发，沿着所有可能的道路走，看看能否到达城市 j。  
- 如果遍历结束仍没碰到 j，就说明 i 和 j **不可达**，计数 +1。  

为什么这样能得到答案？  
- 题目要求的是“所有不可达的节点对”。只要把每一对都检查一遍，凡是不可达的就记下来，最后的计数自然就是答案。  

**时间/空间分析（大白话）**  
- 节点数记作 `n`，边数记作 `m`。  
- 对每一对 `(i, j)`（一共有 `n·(n‑1)/2 ≈ n²/2` 对），我们都要跑一次 **完整的 BFS/DFS**，最坏情况下要遍历所有节点和所有边，耗时 `O(n + m)`。  
- 所以整体时间是 **`O(n²·(n+m))`**，这在 `n` 达到 10⁵ 时根本不可接受。  
- 空间上我们只需要保存一次遍历时的 visited 数组和邻接表，都是 `O(n + m)`，即 `O(n)` 量级。  

> **O(n²·(n+m))** 的含义：  
> 想象你要把每个人都和所有其他人分别聊一次，每次聊天都要把整张地图重新翻一遍，这显然太费力了。  

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def countPairs_bruteforce(n: int, edges: List[List[int]]) -> int:
    # 建立邻接表：city -> [相邻的城市]
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def bfs(start: int, target: int) -> bool:
        """从 start 出发，看看能否走到 target"""
        if start == target:
            return True
        visited = [False] * n
        q = deque([start])
        visited[start] = True
        while q:
            cur = q.popleft()
            for nxt in graph[cur]:
                if not visited[nxt]:
                    if nxt == target:          # 找到目标，直接返回
                        return True
                    visited[nxt] = True
                    q.append(nxt)
        return False                       # 遍历完都没找到

    ans = 0
    # 对每一对 (i, j) 检查可达性
    for i in range(n):
        for j in range(i + 1, n):
            if not bfs(i, j):   # 不可达则计数
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²·(n+m))`  
  - `n²/2` 对每对节点，各自跑一次 BFS，最坏遍历 `O(n+m)`。  
- **空间复杂度**：`O(n+m)`（邻接表 + BFS 时的 visited 数组）  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于**重复遍历**同一个连通块。  
如果我们先把图划分成若干**连通分量**（connected component），同一个分量里的任意两个节点**一定是可达**的，跨分量的节点则**必然不可达**。  

**关键一步**：**快速求出每个连通分量的大小**。  
常用的两种办法：  

1. **DFS / BFS**：遍历一次图，标记每个节点属于哪个分量。  
2. **并查集（Union Find）**：把相连的节点“合并”到同一个集合中，最后每个集合的大小即为一个连通分量的规模。  

这里选用 **并查集**，因为实现简单且天然支持**路径压缩 + 按大小合并**，可以在几乎线性的时间内完成所有合并操作（`O(α(n))`，α 为极慢增长的阿克曼函数，近似看作常数）。  

**计算答案**  
设连通分量的大小为 `s1, s2, …, sk`，总节点数 `n = s1 + s2 + … + sk`。  
- 任意两点是否不可达，只取决于它们是否来自不同的分量。  
- 不可达对的数量 = **所有不同分量之间的两两乘积之和**  

\[
\text{ans} = \sum_{i<j} s_i \times s_j
\]

这可以用**累计乘法**或**总对数减去内部对数**的方式快速算出：

\[
\text{总对数} = \binom{n}{2} = \frac{n\,(n-1)}{2}
\]
\[
\text{内部可达对数} = \sum_{i} \binom{s_i}{2} = \sum_{i} \frac{s_i\,(s_i-1)}{2}
\]
\[
\text{不可达对数} = \text{总对数} - \text{内部可达对数}
\]

这样只需要遍历一次分量大小数组即可得到答案，**时间线性**，**空间只需 O(n)** 保存父节点和大小。  

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集：维护 n 个元素的若干不相交集合"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 父节点，初始各自为根
        self.size = [1] * n            # 每个根对应集合的规模

    def find(self, x: int) -> int:
        """寻找 x 所在集合的根，并进行路径压缩"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压缩路径
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        """把 a、b 所在的集合合并"""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:          # 已经同根， nothing to do
            return
        # 按大小合并：把小集合挂到大集合下，保持树的高度低
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]   # 更新根 ra 的规模

def countPairs(n: int, edges: List[List[int]]) -> int:
    uf = UnionFind(n)

    # 1️⃣ 合并所有相连的节点
    for a, b in edges:
        uf.union(a, b)

    # 2️⃣ 统计每个连通分量的规模
    # 只统计根节点的 size 即可
    component_sizes = []
    for i in range(n):
        if uf.find(i) == i:               # i 是根
            component_sizes.append(uf.size[i])

    # 3️⃣ 计算不可达对数
    total_pairs = n * (n - 1) // 2       # 所有节点两两组合的总数
    reachable_pairs = 0
    for sz in component_sizes:
        reachable_pairs += sz * (sz - 1) // 2   # 同一分量内部可达的对数

    return total_pairs - reachable_pairs
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - `m = len(edges)`。并查集的每次 `union` / `find` 近似 `O(1)`（α(n)），所以整体线性。  
  - 与暴力解的 `O(n²·…)` 相比，快了几个数量级。  
- **空间复杂度**：`O(n)`  
  - 只保存 `parent`、`size` 两个长度为 `n` 的数组，以及最终的分量大小列表。  

---

## 心得  

- **核心技巧**：**把图划分成连通分量**，再利用组合数学计算跨分量的配对数。  
- **适用场景**（类似题目）  
  1. *Number of Connected Components in an Undirected Graph*（统计连通块数量）  
  2. *Maximum Number of Edges to Remove to Make Graph Fully Disconnected*（让图完全断开的最大删除边数）  
  3. *Count Pairs of Nodes That Are Not Directly Connected*（统计不直接相连的节点对）  

> **解题钥匙**：先找**“同类”**（同一连通分量），再算**“不同类之间的配对”**。  

---

## 反思  

- **第一反应**：想到要遍历每一对节点检查可达性，直接写了两层循环。  
- **最容易踩的坑**  
  - **时间超限**：`n` 可达 10⁵，暴力 `O(n²)` 完全不行。  
  - **并查集实现细节**：忘记路径压缩或按大小合并会导致近似 `O(n·α(n))` 退化为 `O(n·log n)`，仍然可接受但不够“最优”。  
  - **计数时的整数溢出**（在某些语言里）：使用 `long long`（Python 自动大整数）避免。  
- **下次遇到同类题**：第一步立刻**判断是否可以把问题转化为“连通分量 + 组合计数”**，再选用并查集或一次 BFS/DFS 完成分量划分。