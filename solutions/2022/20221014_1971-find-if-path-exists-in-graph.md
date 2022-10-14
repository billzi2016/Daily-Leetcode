# #1971. 判断图中是否存在路径 / Find if Path Exists in Graph

> 难度：简单 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/find-if-path-exists-in-graph/)

---

## 题目（英文原版）

**Description**

There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1 (inclusive). The edges in the graph are represented as a 2D integer array edges, where each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi. Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.
You want to determine if there is a valid path that exists from vertex source to vertex destination.
Given edges and the integers n, source, and destination, return true if there is a valid path from source to destination, or false otherwise.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
Output: true
Explanation: There are two paths from vertex 0 to vertex 2:
- 0 → 1 → 2
- 0 → 2
```

**Example 2:**

```
Input: n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
Output: false
Explanation: There is no path from vertex 0 to vertex 5.
```

**Constraints**

- 1 <= n <= 2 * 105
- 0 <= edges.length <= 2 * 105
- edges[i].length == 2
- 0 <= ui, vi <= n - 1
- ui != vi
- 0 <= source, destination <= n - 1
- There are no duplicate edges.
- There are no self edges.

---

## 题目（中文翻译）

描述  
存在一个 **双向图（bi-directional graph）**，它有 `n` 个节点（vertex），节点编号从 `0` 到 `n - 1`（含）。图中的边（edge）由二维整数数组 `edges` 表示，其中 `edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间有一条双向边。任意一对节点至多只有一条边，且不存在指向自身的边。

现在需要判断是否存在一条 **有效路径（valid path）** 能从节点 `source` 到达节点 `destination`。  
给定 `edges`、整数 `n`、`source` 与 `destination`，若存在从 `source` 到 `destination` 的有效路径，返回 `true`；否则返回 `false`。

示例  
**示例 1**  
输入: `n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2`  
输出: `true`  
解释: 从节点 `0` 到节点 `2` 有两条路径:  
- `0 → 1 → 2`  
- `0 → 2`

**示例 2**  
输入: `n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5`  
输出: `false`  
解释: 节点 `0` 与节点 `5` 之间不存在路径。

约束条件  
- `1 <= n <= 2 * 10^5`  
- `0 <= edges.length <= 2 * 10^5`  
- `edges[i].length == 2`  
- `0 <= ui, vi <= n - 1`  
- `ui != vi`  
- `0 <= source, destination <= n - 1`  
- 不存在重复的边。  
- 不存在指向自身的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有点和边都写成一个大表格**，然后从 `source` 开始一步步往后走，看看能不能走到 `destination`。  
- **数据结构**：我们可以用 **邻接矩阵**（二维数组）来存储图。把 `n` × `n` 的矩阵想象成一本“城市-城市”对应表，行代表出发城市，列代表目的城市，`matrix[u][v] = 1` 表示两城之间有直达的路。就像查字典时，词（key）对应的解释（value）一样，`u` 是键，`v` 是值。
- **遍历方式**：采用 **深度优先搜索（DFS）**，从 `source` 递归地访问它的所有相邻城市。如果在递归过程中碰到 `destination`，说明有路径；否则继续搜索，直到所有能到达的城市都遍历完。

为什么这个方法一定能得到正确答案？  
因为 DFS 会把 **所有** 能从 `source` 到达的顶点都访问一遍，只要 `destination` 在这套可达集合里，就一定会被找到。

**时间/空间复杂度**  
- 构造邻接矩阵需要 `n²` 的空间，就像在一张 `n` 行 `n` 列的表格里填“有路/没路”。  
- 在最坏情况下（图是完全连通的），DFS 会检查每一条边，每一次递归都要遍历 `n` 列，整体时间是 **O(n²)**。  
- 递归栈的深度最多是 `n`，占用 **O(n)** 的额外空间。

> 大白话解释：  
> - `O(n²)` 就是说，如果有 1000 个点，程序大概会执行 **一百万次**（1000 × 1000）的基本操作。  
> - `O(n)` 则是说，只会使用跟点的数量成正比的额外内存，1000 个点只会占用几千个单元的空间。

#### 代码（Python）

```python
from typing import List

def validPath_bruteforce(n: int, edges: List[List[int]],
                        source: int, destination: int) -> bool:
    # ---------- 建立邻接矩阵 ----------
    # matrix[u][v] == 1 表示 u 和 v 之间有直接的路
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1          # 因为是双向图

    visited = [False] * n        # 记录每个节点是否已经遍历过

    # ---------- 深度优先搜索 ----------
    def dfs(cur: int) -> bool:
        if cur == destination:    # 已经到达目标
            return True
        visited[cur] = True
        # 遍历 cur 的所有相邻节点（矩阵的一整行）
        for nxt in range(n):
            if matrix[cur][nxt] == 1 and not visited[nxt]:
                if dfs(nxt):      # 只要有一条路能通，就返回 True
                    return True
        return False               # 没有任何相邻节点能通向目标

    return dfs(source)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们在最坏情况下会检查每一对顶点（`n * n`）是否相连。
- **空间复杂度**：`O(n²)`（邻接矩阵）+ `O(n)`（递归栈）≈`O(n²)`  
  解释：整个二维表格占用了 `n²` 个格子。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **邻接矩阵**：它把所有不存在的边也占了空间，导致时间和空间都和 `n²` 成正比。  
实际图的规模受 **边的数量** `m = len(edges)` 限制，`m` 最多也只有 `2·10⁵`，远小于 `n²`（`n` 最高到 `2·10⁵`）。因此我们应当 **只存真实存在的边**，这正是 **邻接表**（list of lists）要做的事。

接下来，遍历图的核心仍然是 **DFS** 或 **BFS**，但这次每次只遍历**当前节点的真实邻居**，时间随边的数量线性增长，即 **O(n + m)**。  
如果想进一步简化（只需要判断「是否连通」而不关心路径本身），**并查集（Union Find）** 更快：一次遍历所有边，把相连的点合并到同一个集合，最后检查 `source` 与 `destination` 是否在同一个集合中。并查集的时间复杂度几乎是 **O(α(n))**（α 为极慢增长的阿克曼函数），在本题中可以视作常数。

下面分别给出 **邻接表 + BFS** 的实现（最常见）以及 **并查集** 的实现，帮助你掌握两种思路。

##### 关键概念解释
- **邻接表**：把每个点的所有直接相连的点放进一个小列表里。想象成每个城市都有一本“直达车次表”，只列出真的有车的目的地。
- **BFS（广度优先搜索）**：像在城市里按层层展开的方式寻找目标，先走完离起点最近的所有城市，再往外扩展。使用 **队列**（先进先出）实现。
- **并查集（Union Find）**：把相互可以到达的点“合并”为同一个集合。每个集合有一个代表（根），`find(x)` 能找出 `x` 所属的根，`union(a,b)` 把两个根合并。类似于把同一片区域的土地划为同一块地号。

#### 代码（Python）

**方法一：邻接表 + BFS（推荐）**

```python
from collections import deque
from typing import List

def validPath_bfs(n: int, edges: List[List[int]],
                  source: int, destination: int) -> bool:
    # ---------- 建立邻接表 ----------
    # graph[u] 是所有和 u 直接相连的节点列表
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)          # 双向图

    # ---------- BFS ----------
    visited = [False] * n
    q = deque([source])
    visited[source] = True

    while q:
        cur = q.popleft()
        if cur == destination:      # 直接找到目标
            return True
        # 只遍历当前节点的真实邻居
        for nxt in graph[cur]:
            if not visited[nxt]:
                visited[nxt] = True
                q.append(nxt)       # 把邻居加入队列，待下一层访问
    return False                    # 队列空了仍未找到，说明不连通
```

**方法二：并查集（Union Find）**

```python
from typing import List

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))   # 每个节点最初是自己的根
        self.rank = [0] * size            # 用于按秩合并，保持树的高度低

    def find(self, x: int) -> int:
        # 路径压缩：把沿途的节点直接挂到根上，后续查询更快
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按秩合并：高度低的挂到高度高的下面
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

def validPath_unionfind(n: int, edges: List[List[int]],
                       source: int, destination: int) -> bool:
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)                # 把每条边的两个端点合并到同一个集合
    return uf.find(source) == uf.find(destination)
```

#### 复杂度

- **邻接表 + BFS**  
  - 时间复杂度：`O(n + m)`  
    解释：遍历所有节点一次（`n`）以及所有边一次（`m`），每条边只会被检查两次（一次从 `u`，一次从 `v`）。  
  - 空间复杂度：`O(n + m)`  
    解释：邻接表需要存 `m` 条边的信息，加上 `n` 个节点的列表头指针和 `visited` 数组。

- **并查集**  
  - 时间复杂度：`O(m·α(n))` ≈ `O(m)`（α 为极慢增长的阿克曼函数）  
    解释：每条边执行一次 `union`，每次 `find` 的时间几乎是常数。  
  - 空间复杂度：`O(n)`  
    解释：只需要 `parent` 与 `rank` 两个长度为 `n` 的数组。

> 与暴力解对比：  
> - 暴力解用了 `O(n²)` 的时间和空间，完全是因为把“没有路”的情况也浪费了资源。  
> - 最优解只关注真实的 `m` 条边，时间从 “一百万次” 降到 “几万次”，空间同样从 “一张巨大的表格” 降到 “几百 KB”。在极限数据（`n = 2·10⁵`，`m = 2·10⁵`）下，暴力解根本会 **内存超限**，而最优解轻松通过。

---

## 心得

- **核心技巧**：把图用 **邻接表** 表示，再用 **BFS/DFS** 或 **并查集** 判断连通性。  
- **适用的题型**  
  1. 判断两个节点是否在同一连通分量（如本题）。  
  2. 求图的 **连通分量数量**（LeetCode 323. Number of Connected Components in an Undirected Graph）。  
  3. 判断图中是否存在环（使用并查集或 DFS）。  
- **一句话总结**：**“只存真实边，用遍历或合并集合快速判断连通”**。

---

## 反思

- **第一反应**：看到“bi‑directional graph”和“是否存在路径”，立刻想到 BFS/DFS。  
- **最容易踩的坑**  
  - **边界条件**：`n = 1` 时，`source` 与 `destination` 可能相同，需要直接返回 `True`。  
  - **孤立点**：`edges` 可能为空，所有节点互不相连，需处理这种极端情况。  
  - **递归深度**：使用 DFS 时递归层数可能达到 `n`（`2·10⁵`），会导致 Python 递归深度溢出，推荐改用显式栈或 BFS。  
- **下次类似题的第一步**：**先把图转换成邻接表**（或直接使用并查集），再决定是 **遍历** 还是 **合并集合**。这样可以避免不必要的 `O(n²)` 开销。