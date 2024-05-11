# #2685. 统计完整连通分量的数量 / Count the Number of Complete Components

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-complete-components/)

---

## 题目（英文原版）

**Description**

You are given an integer n. There is an undirected graph with n vertices, numbered from 0 to n - 1. You are given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting vertices ai and bi.
Return the number of complete connected components of the graph.
A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.
A connected component is said to be complete if there exists an edge between every pair of its vertices.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]
Output: 3
Explanation: From the picture above, one can see that all of the components of this graph are complete.
```

**Example 2:**

```
Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]
Output: 1
Explanation: The component containing vertices 0, 1, and 2 is complete since there is an edge between every pair of two vertices. On the other hand, the component containing vertices 3, 4, and 5 is not complete since there is no edge between vertices 4 and 5. Thus, the number of complete components in this graph is 1.
```

**Constraints**

- 1 <= n <= 50
- 0 <= edges.length <= n * (n - 1) / 2
- edges[i].length == 2
- 0 <= ai, bi <= n - 1
- ai != bi
- There are no repeated edges.

---

## 题目（中文翻译）

给定一个整数 `n`，表示有 `n` 个顶点的无向图（undirected graph），顶点编号为 `0` 到 `n - 1`。另给定二维整数数组 `edges`，其中 `edges[i] = [ai, bi]` 表示存在一条连接顶点 `ai` 与 `bi` 的无向边（undirected edge）。  

返回图中 **完整连通分量（complete connected component）** 的数量。  

**连通分量（connected component）** 是图的一个子图（subgraph），其中任意两个顶点之间都有路径（path），且该子图中的顶点不与子图外的顶点相连。  

如果连通分量中的每一对顶点之间都存在边，则称该连通分量为 **完整的（complete）**。  

### 示例

**示例 1**  
输入: `n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]`  
输出: `3`  
解释: 如图所示，图的所有连通分量都是完整的。

**示例 2**  
输入: `n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]`  
输出: `1`  
解释: 包含顶点 `0, 1, 2` 的连通分量是完整的，因为任意两顶点之间都有边。而包含顶点 `3, 4, 5` 的连通分量不是完整的，因为顶点 `4` 与 `5` 之间没有边。因此，该图中完整连通分量的数量为 `1`。

### 约束条件

- `1 <= n <= 50`
- `0 <= edges.length <= n * (n - 1) / 2`
- `edges[i].length == 2`
- `0 <= ai, bi <= n - 1`
- `ai != bi`
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **先把图分成连通块**  
   用 **DFS / BFS**（深度优先/广度优先搜索）遍历图，从未访问的节点出发把所有能走到的节点收集在一起，这就是一个 **连通分量**。  
   *类比*：想象一张城市地图，城市之间有道路。我们从一个城市出发，沿着道路一直走，能到达的所有城市就构成了一个“连通块”。  

2. **判断每个连通块是否“完整”**  
   完整的意思是块里任意两个节点之间都有直接的边。  
   - 先把块里的节点记下来，设块大小为 `m`。  
   - 然后枚举块里所有 **节点对**（`m` 选 `2`），检查这条边是否在原始 `edges` 列表里出现。  
   - 如果所有配对都找到了对应的边，说明该块是完整的。

3. **统计完整块的数量**  

为什么这个方法一定能得对？  
- DFS/BFS 能保证把所有**互相可达**的节点全部找出来（不漏也不多）。  
- 对每个块我们穷举所有可能的边，只有当每一条都真的存在时，才算完整，完全符合题目对“完整连通块”的定义。

**复杂度分析（大白话）**  
- 找连通块：每条边和每个节点只会被遍历一次，时间是 `O(n + E)`（`n` 是节点数，`E` 是边数）。  
- 判断完整性：对大小为 `m` 的块，要检查 `m*(m-1)/2` 条可能的边。最坏情况下，图是一个完整图，`m = n`，于是检查的次数是 `n*(n-1)/2`，即 **约等于 `n²/2`**。  
- 综合下来，最坏时间是 **`O(n² + E)`**，因为 `n ≤ 50`，这在本题的限制里还能跑完，但不是最优的。  

空间方面：  
- 需要保存邻接表（每个节点的相邻节点列表）和访问标记，都是 `O(n + E)`，再加上暂存一个连通块的节点列表，最多 `O(n)`。总体 **`O(n + E)`**。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Set, Tuple

def countCompleteComponents_bruteforce(n: int, edges: List[List[int]]) -> int:
    # ---------- 建图 ----------
    # 用字典把每个节点的邻居装进集合，查询是否有边就像查字典一样快
    graph: defaultdict[int, Set[int]] = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    visited = [False] * n          # 记录节点是否已经被遍历
    complete_cnt = 0               # 计数完整连通块

    # ---------- BFS 找连通块 ----------
    for start in range(n):
        if visited[start]:
            continue

        # 以 start 为起点做一次 BFS，收集整个连通块的所有节点
        q = deque([start])
        visited[start] = True
        component = []              # 当前连通块的节点列表

        while q:
            node = q.popleft()
            component.append(node)
            for nb in graph[node]:
                if not visited[nb]:
                    visited[nb] = True
                    q.append(nb)

        # ---------- 检查是否完整 ----------
        m = len(component)          # 该块的节点数
        is_complete = True
        # 逐对检查边是否存在（穷举所有 m 选 2 对）
        for i in range(m):
            for j in range(i + 1, m):
                a, b = component[i], component[j]
                # 如果 a 的邻居集合里没有 b，说明缺少这条边
                if b not in graph[a]:
                    is_complete = False
                    break
            if not is_complete:
                break

        if is_complete:
            complete_cnt += 1

    return complete_cnt
```

#### 复杂度

- **时间复杂度**：`O(n² + E)`  
  - `n²` 来自对每个连通块里所有节点对的检查。  
  - `E` 是遍历所有边时的开销。  
  - 对于 `n ≤ 50` 的数据，这个量级是可以接受的。

- **空间复杂度**：`O(n + E)`  
  - 邻接表、访问数组以及 BFS 队列都需要这些空间。  

---

### 2. 最优解

#### 思路  

暴力解慢的地方在于**逐对检查每条可能的边**。我们其实不需要真的去枚举这些对，只要知道**该块里到底有多少条边**，就能直接判断它是否完整。

**关键观察**  

- 对于一个大小为 `m` 的连通块，**完整** 的必要且充分条件是  
  `实际边数 == m * (m - 1) / 2`  
  （这正是完全图的边数公式）。  
- 因此，只要能快速得到每个连通块的 **节点数** 和 **边数**，就能在 **O(1)** 时间判断完整性。

**如何快速得到节点数 & 边数？**  
我们可以使用 **并查集（Union‑Find / DSU）**：

1. 初始时每个节点自成一族。  
2. 逐条遍历 `edges`，把两端的节点合并（`union`）。  
   - 合并的过程把属于同一连通块的节点归到同一个根（代表）。  
3. 合并完后，再遍历一遍所有节点，统计每个根对应的 **节点数量**（`size[root]`）。  
4. 再遍历一遍所有边，统计每个根对应的 **边数量**（`edge_cnt[root]`）。  
   - 注意：因为是无向图，`[u, v]` 只算一次，直接把它归到 `find(u)`（或 `find(v)`）即可。  

最后，对每个根检查 `edge_cnt[root] == size[root] * (size[root] - 1) // 2`，满足的根对应的连通块就是完整的。

**为什么 DSU 更快？**  
- 并查集的 `find`、`union` 操作几乎是 **常数时间**（摊销 `α(n)`，α 为阿克曼函数的逆，几乎等于 1）。  
- 我们只遍历 **一次边列表** 来完成合并和计数，整个过程是 **线性** 的 `O(n + E)`，不再有二次枚举。

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集（Union‑Find）实现，带路径压缩和按秩合并"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点的父节点，初始指向自己
        self.rank = [0] * n            # 按秩合并用的高度近似值

    def find(self, x: int) -> int:
        # 递归找根的同时把路径上的节点直接挂到根上（路径压缩）
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        # 把两个根合并，根的秩小的挂到秩大的下面
        rx, ry = self.find(x), self.find(y)
        if rx == ry:                     # 已经在同一个集合
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

def countCompleteComponents_optimal(n: int, edges: List[List[int]]) -> int:
    dsu = DSU(n)

    # 1️⃣ 把所有边的两端合并进同一个集合
    for u, v in edges:
        dsu.union(u, v)

    # 2️⃣ 统计每个根的节点数（size）和边数（edge_cnt）
    size = [0] * n           # size[root] = 该根所在连通块的节点个数
    edge_cnt = [0] * n       # edge_cnt[root] = 该连通块的实际边数

    # 统计节点数
    for node in range(n):
        root = dsu.find(node)
        size[root] += 1

    # 统计边数（每条边只计一次）
    for u, v in edges:
        root = dsu.find(u)   # u 和 v 必在同一根，任选其一即可
        edge_cnt[root] += 1

    # 3️⃣ 判断完整性
    complete = 0
    for root in range(n):
        if size[root] == 0:          # 该根没有对应的节点，跳过（可能是被别的根“抢走”了）
            continue
        # 完整连通块的边数公式：m*(m-1)/2
        if edge_cnt[root] == size[root] * (size[root] - 1) // 2:
            complete += 1

    return complete
```

#### 复杂度

- **时间复杂度**：`O(n + E·α(n))`  
  - `α(n)` 是阿克曼函数的逆，几乎可以视作常数。整体上只遍历了节点一次、边两次，线性时间。  
  - 与暴力解的 `O(n²)` 相比，**快了一个数量级**，尤其当 `n` 较大时优势明显。

- **空间复杂度**：`O(n)`  
  - 并查集的 `parent`、`rank`、`size`、`edge_cnt` 四个长度为 `n` 的数组。  
  - 不需要额外的邻接表或 BFS 队列，空间更紧凑。

---

## 心得

- **核心技巧**：利用 **并查集** 把同一连通块的节点归并，然后通过 **计数公式** `m*(m-1)/2` 判断是否为完全图。  
- **该技巧适用的题型**  
  1. “统计满足某种结构的连通块” 类题（如 “统计连通块中环的数量”）。  
  2. “判断连通块是否满足度数/边数条件” 类题（如 “检查每个连通块是否是树”）。  
  3. “按连通块分类求和” 类题（如 “求每个连通块的最小生成树权值之和”）。  
- **一句话总结解题钥匙**：  
  > **先把同一块的节点归并，再只用两次遍历分别计数节点和边，用完全图的边数公式直接判断**。

---

## 反思

- **第一反应**：看到“连通块”和“完整”，立刻想到先找连通块，再检查每对节点是否都有边——这就是最直观的暴力思路。  
- **最容易踩的坑**  
  - **边数统计重复**：在遍历 `edges` 时，别把同一条无向边算两次。  
  - **孤立节点**：没有任何边的节点也是一个大小为 `1` 的连通块，它自然是完整的（`1*(1-1)/2 = 0` 条边）。  
  - **并查集根的选取**：统计边数时一定要把边归到根节点（`find(u)`），否则同一个块的边会分散到不同根导致判断错误。  
- **下次遇到同类题的第一步**：  
  > **先用 DSU（或 BFS/DFS）把所有连通块划分出来，然后把“属性计数”交给一次线性遍历**，再用相应的数学公式或判定条件快速得出答案。