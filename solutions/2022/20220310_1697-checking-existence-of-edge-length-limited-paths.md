# #1697. 检查受限边长路径的存在性 / Checking Existence of Edge Length Limited Paths

> 难度：困难 · 标签：Array、Two Pointers、Union Find、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/)

---

## 题目（英文原版）

**Description**

An undirected graph of n nodes is defined by edgeList, where edgeList[i] = [ui, vi, disi] denotes an edge between nodes ui and vi with distance disi. Note that there may be multiple edges between two nodes.
Given an array queries, where queries[j] = [pj, qj, limitj], your task is to determine for each queries[j] whether there is a path between pj and qj such that each edge on the path has a distance strictly less than limitj .
Return a boolean array answer, where answer.length == queries.length and the jth value of answer is true if there is a path for queries[j] is true, and false otherwise.

**Examples**

**Example 1:**

```
Input: n = 3, edgeList = [[0,1,2],[1,2,4],[2,0,8],[1,0,16]], queries = [[0,1,2],[0,2,5]]
Output: [false,true]
Explanation: The above figure shows the given graph. Note that there are two overlapping edges between 0 and 1 with distances 2 and 16.
For the first query, between 0 and 1 there is no path where each distance is less than 2, thus we return false for this query.
For the second query, there is a path (0 -> 1 -> 2) of two edges with distances less than 5, thus we return true for this query.
```

**Example 2:**

```
Input: n = 5, edgeList = [[0,1,10],[1,2,5],[2,3,9],[3,4,13]], queries = [[0,4,14],[1,4,13]]
Output: [true,false]
Explanation: The above figure shows the given graph.
```

**Constraints**

- 2 <= n <= 105
- 1 <= edgeList.length, queries.length <= 105
- edgeList[i].length == 3
- queries[j].length == 3
- 0 <= ui, vi, pj, qj <= n - 1
- ui != vi
- pj != qj
- 1 <= disi, limitj <= 109
- There may be multiple edges between two nodes.

---

## 题目（中文翻译）

给定一个包含 **n** 个节点的无向图（undirected graph），由 `edgeList` 定义，其中 `edgeList[i] = [ui, vi, disi]` 表示节点 `ui` 与节点 `vi` 之间存在一条距离为 `disi` 的边。注意，同一对节点之间可能存在多条边。  

给定数组 `queries`，其中 `queries[j] = [pj, qj, limitj]`，请判断对于每个查询 `queries[j]`，是否存在一条从 `pj` 到 `qj` 的路径，使得路径上的每条边的距离 **严格小于** `limitj`。  

返回一个布尔数组 `answer`，其长度等于 `queries.length`，若第 `j` 条查询存在满足条件的路径，则 `answer[j]` 为 `true`，否则为 `false`。  

### 示例  

#### 示例 1  
**输入**: `n = 3`, `edgeList = [[0,1,2],[1,2,4],[2,0,8],[1,0,16]]`, `queries = [[0,1,2],[0,2,5]]`  
**输出**: `[false,true]`  
**解释**: 上图展示了给定的图。注意节点 0 与节点 1 之间有两条重叠的边，距离分别为 2 和 16。  
- 对于第一个查询，由于不存在一条路径使得所有边的距离都 **小于 2**，因此返回 `false`。  
- 对于第二个查询，存在路径 `0 -> 1 -> 2`，其边的距离分别为 2 和 4，均小于 5，故返回 `true`。  

#### 示例 2  
**输入**: `n = 5`, `edgeList = [[0,1,10],[1,2,5],[2,3,9],[3,4,13]]`, `queries = [[0,4,14],[1,4,13]]`  
**输出**: `[true,false]`  
**解释**: 上图展示了给定的图。  
- 对于查询 `[0,4,14]`，路径 `0 -> 1 -> 2 -> 3 -> 4` 的所有边距离分别为 10、5、9、13，均小于 14，返回 `true`。  
- 对于查询 `[1,4,13]`，任意从 1 到 4 的路径必然包含距离为 13 的边，而该边不满足 “严格小于 13” 的要求，故返回 `false`。  

### 约束条件  
- `2 <= n <= 10^5`  
- `1 <= edgeList.length, queries.length <= 10^5`  
- `edgeList[i].length == 3`  
- `queries[j].length == 3`  
- `0 <= ui, vi, pj, qj <= n - 1`  
- `ui != vi`  
- `pj != qj`  
- `1 <= disi, limitj <= 10^9`  
- 同一对节点之间可能存在多条边。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每个查询单独在图中做一次搜索**（DFS / BFS），只走权值 `< limit` 的边，看能否从 `p` 走到 `q`。  

- **数据结构**：  
  - 把 `edgeList` 组织成邻接表（每个节点保存它的相邻节点和对应的距离），类似于“每个人的通讯录”，里面记的就是“谁认识谁、距离多远”。  
  - 在搜索过程中，用一个 `visited` 集合记录已经走过的节点，防止在图中兜圈子——这就像“走迷宫时不走回头路”。  

- **为什么正确**：  
  - BFS/DFS 会遍历 **所有** 能够只经过权值 `< limit` 的路径，只要有一条能连通 `p` 与 `q`，搜索就会成功返回 `True`。  

- **时间/空间复杂度**：  
  - 对每个查询我们都要遍历一次图，最坏情况下会把所有边都检查一遍。设 `E = len(edgeList)`，`Q = len(queries)`。  
  - **时间**：`O(Q * (V + E))`，其中 `V = n`。如果图很稀疏 `E≈V`，仍然是 `O(Q·V)`；在最坏的密集图（`E≈10⁵`）里，这相当于 **每个查询都要遍历 10⁵ 条边**，会超时。  
  - **空间**：邻接表需要 `O(V + E)`，每次搜索的 `visited` 需要 `O(V)`。  

> 大白话：如果把每个查询想象成一次“请小明从 A 城跑到 B 城，只能走小于 5 公里的路”，小明每次都要重新检查全城的所有路，问 10⁵ 次，那时间肯定不够。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def distanceLimitedPathsExist_bruteforce(
    n: int, edgeList: List[List[int]], queries: List[List[int]]
) -> List[bool]:
    # 1. 把无向图建成邻接表
    graph = defaultdict(list)               # node -> [(neighbor, weight), ...]
    for u, v, w in edgeList:
        graph[u].append((v, w))
        graph[v].append((u, w))

    def bfs(start: int, target: int, limit: int) -> bool:
        """只走权值 < limit 的边，判断 start 能否到达 target"""
        visited = [False] * n
        q = deque([start])
        visited[start] = True
        while q:
            cur = q.popleft()
            if cur == target:
                return True
            for nxt, w in graph[cur]:
                if not visited[nxt] and w < limit:   # 只能走更短的路
                    visited[nxt] = True
                    q.append(nxt)
        return False

    # 2. 对每个查询单独跑一次 BFS
    ans = []
    for p, q, limit in queries:
        ans.append(bfs(p, q, limit))
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(Q * (V + E))`。  
  - `Q` 次查询，每次最坏遍历全部节点和边。  
- **空间复杂度**：`O(V + E)`。  
  - 邻接表存图，`visited` 数组在一次查询结束后会被回收。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于：每次查询都要重新遍历整张图。  
关键观察：

1. **所有查询都已知**，我们可以先把查询按照 `limit` 从小到大排序。  
2. 同理，把所有边也按照 **权值** 从小到大排序。  
3. 当我们处理 **某个查询** 时，只需要把 **权值 < limit** 的所有边“加入”图中，然后判断 `p` 与 `q` 是否已经在同一个连通块。  

这正好可以用 **并查集（Union‑Find）** 来维护连通块：

- 并查集把若干节点合并成集合，`find(x)` 能快速得到 x 所在集合的根，`union(a,b)` 把两个集合合并。  
- 当我们把一条满足 `weight < limit` 的边加入图时，只需要 `union(u, v)`，把两端所在的集合合并。  
- 查询时，只要 `find(p) == find(q)`，说明已经有一条只经过更小权值边的路径存在。  

**实现步骤**：

1. 把 `queries` 加上原始下标，得到 `(p, q, limit, idx)`，按 `limit` 升序排序。  
2. 把 `edgeList` 按 `weight` 升序排序。  
3. 初始化并查集 `parent = [i for i in range(n)]`，`rank`（或 `size`）用于优化。  
4. 用指针 `e = 0` 遍历排序后的边：  
   - 当 `edgeList[e][2] < cur_limit` 时，执行 `union(u, v)` 并把指针右移。  
   - 当指针指向的边已经不满足 `< limit`，停止加入。  
5. 此时所有已经加入的边的权值都 **严格小于** 当前查询的 `limit`，直接比较 `find(p)` 与 `find(q)`。  
6. 把答案写入 `ans[idx]`（使用原始下标恢复顺序）。  

**为什么正确**：

- 对每个查询，我们只加入了 **所有** 权值更小的边（没有遗漏），而且 **只加入一次**（因为查询是从小到大处理，后面的查询只会再加入更多的边）。  
- 并查集保证了只要两点在同一集合，就必然存在一条只经过已加入边的路径，而已加入的边全部满足 `< limit`，因此路径一定满足题目要求。  

**类比**：把所有道路按“宽度”从窄到宽排好，然后一次次打开更宽的道路。每打开一条新道路，就把两边的城市连通起来。询问能否从 A 到 B，只要看它们是否已经被同一条已经打开的道路网络连在一起。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集：支持路径压缩 + 按秩合并"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点最开始自己是根
        self.rank = [0] * n            # 近似树的深度，帮助平衡

    def find(self, x: int) -> int:
        # 递归写法，顺便做路径压缩：把沿途所有节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:                     # 已经在同一个集合
            return
        # 按秩合并：把秩小的挂到秩大的下面
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1           # 秩相同，挂完后根的秩加一

def distanceLimitedPathsExist(
    n: int, edgeList: List[List[int]], queries: List[List[int]]
) -> List[bool]:
    # 1️⃣ 把查询加上原始下标并按 limit 升序排列
    queries_with_idx = [(p, q, limit, i) for i, (p, q, limit) in enumerate(queries)]
    queries_with_idx.sort(key=lambda x: x[2])          # 按 limit 排序

    # 2️⃣ 把所有边按权值升序排列
    edgeList.sort(key=lambda x: x[2])                  # 按 weight 排序

    uf = UnionFind(n)                                 # 初始化并查集
    ans = [False] * len(queries)                      # 预分配答案数组
    e = 0                                             # 边的指针

    # 3️⃣ 逐个处理查询
    for p, q, limit, idx in queries_with_idx:
        # 把所有 weight < limit 的边全部加入并查集
        while e < len(edgeList) and edgeList[e][2] < limit:
            u, v, w = edgeList[e]
            uf.union(u, v)                           # 合并两端所在的集合
            e += 1
        # 此时所有加入的边权值都 < limit，直接判断连通性
        ans[idx] = uf.find(p) == uf.find(q)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O( (E + Q) * α(n) )`  
  - `E = len(edgeList)`, `Q = len(queries)`。  
  - 排序需要 `O(E log E + Q log Q)`，在本题的约束下仍然是主导。  
  - `α(n)` 是 Ackermann 函数的逆，几乎可以认为是常数（≤ 5），所以并查集的 `union`/`find` 可以视作 `O(1)`。  
  - 与暴力解相比，**只遍历一次所有边**，查询时不再需要额外的搜索，速度提升几个数量级。  

- **空间复杂度**：`O(n + E + Q)`  
  - 并查集 `O(n)`，排序后的边和查询各自占 `O(E)`、`O(Q)`，不额外使用递归栈或 visited 数组。  

---

## 心得  

- **核心技巧**：**离线排序 + 并查集**（把所有查询和边都提前排序，然后一次性“增量”构建连通块）。  
- **适用场景**：  
  1. **路径可达性** 类似的 “只要边权 < 某阈值” 的问题（如 LeetCode 1697. 检查路径是否存在）。  
  2. **最小生成树** 相关的离线查询（如 “在 MST 中查询两点的最大边权”）。  
  3. **动态连通性** 的离线版本（如 “在删边/加边序列中查询连通性”）。  
- **一句话总结**：把查询按限制值排好序，边按权值排好序，使用并查集逐步“打开”满足条件的边，连通即为答案。

---

## 反思  

- **第一反应**：直接对每个查询跑 BFS/DFS，没想到可以把所有查询一次性处理。  
- **最容易踩的坑**：  
  - **边的比较应使用 `< limit`（严格小于）**，不小心写成 `<=` 会导致答案错误。  
  - **忘记把查询的原始下标保存**，导致输出顺序与输入不一致。  
  - **并查集路径压缩忘写**，会导致时间超限（尤其在 10⁵ 规模的数据上）。  
- **下次遇到同类题**，第一步就想到：  
  1. **是否可以离线**（把所有查询先排序）？  
  2. **能否用增量结构（并查集、线段树）一次性维护**？  
  3. **把“限制条件”转化为“只加入满足条件的元素”**，再在此基础上回答查询。