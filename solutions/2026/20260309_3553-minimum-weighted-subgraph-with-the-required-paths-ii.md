# #3553. 最小加权子图满足必经路径 II / Minimum Weighted Subgraph With the Required Paths II

> 难度：困难 · 标签：Array、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-weighted-subgraph-with-the-required-paths-ii/)

---

## 题目（英文原版）

**Description**

You are given an undirected weighted tree with n nodes, numbered from 0 to n - 1. It is represented by a 2D integer array edges of length n - 1, where edges[i] = [ui, vi, wi] indicates that there is an edge between nodes ui and vi with weight wi.​
Additionally, you are given a 2D integer array queries, where queries[j] = [src1j, src2j, destj].
Return an array answer of length equal to queries.length, where answer[j] is the minimum total weight of a subtree such that it is possible to reach destj from both src1j and src2j using edges in this subtree.
A subtree here is any connected subset of nodes and edges of the original tree forming a valid tree.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], queries = [[2,3,4],[0,2,5]]
Output: [12,11]
Explanation:
The blue edges represent one of the subtrees that yield the optimal answer.

answer[0] : The total weight of the selected subtree that ensures a path from src1 = 2 and src2 = 3 to dest = 4 is 3 + 5 + 4 = 12 .
answer[1] : The total weight of the selected subtree that ensures a path from src1 = 0 and src2 = 2 to dest = 5 is 2 + 3 + 6 = 11 .
```

**Example 2:**

```
Input: edges = [[1,0,8],[0,2,7]], queries = [[0,1,2]]
Output: [15]
Explanation:
```

**Constraints**

- 3 <= n <= 105
- edges.length == n - 1
- edges[i].length == 3
- 0 <= ui, vi < n
- 1 <= wi <= 104
- 1 <= queries.length <= 105
- queries[j].length == 3
- 0 <= src1j, src2j, destj < n
- src1j, src2j, and destj are pairwise distinct.
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

你得到一棵 **无向加权树（undirected weighted tree）**，其中有 `n` 个节点，编号为 `0` 到 `n‑1`。树由长度为 `n‑1` 的二维整数数组 `edges` 表示，`edges[i] = [ui, vi, wi]` 表示节点 `ui` 与节点 `vi` 之间存在一条权重为 `wi` 的边。  

此外，还给定一个二维整数数组 `queries`，其中 `queries[j] = [src1j, src2j, destj]`。  

返回一个长度等于 `queries.length` 的数组 `answer`，其中 `answer[j]` 是 **子树（subtree）** 的最小总权重，使得在该子树中能够分别从 `src1j` 和 `src2j` 使用子树内的边到达 `destj`。这里的子树指的是原树的任意 **连通子集（connected subset）** 的节点和边，仍然构成一棵合法的树。  

---

### 示例 1  
**输入**  
```text
edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]],
queries = [[2,3,4],[0,2,5]]
```  

**输出**  
```text
[12,11]
```  

**解释**  
蓝色的边构成了一个能够得到最优答案的子树。  

- `answer[0]`：选取的子树使得从 `src1 = 2` 与 `src2 = 3` 都能够到达 `dest = 4`，其总权重为 `3 + 5 + 4 = 12`。  
- `answer[1]`：选取的子树使得从 `src1 = 0` 与 `src2 = 2` 都能够到达 `dest = 5`，其总权重为 `2 + 3 + 6 = 11`（示例中给出的答案为 11，具体子树如图所示）。  

---

### 示例 2  
**输入**  
```text
edges = [[1,0,8],[0,2,7]],
queries = [[0,1,2]]
```  

**输出**  
```text
[15]
```  

**解释**  
唯一的子树即整棵树，权重为 `8 + 7 = 15`，满足从 `src1 = 0` 与 `src2 = 1` 都能到达 `dest = 2`。  

---

### 约束条件
- `3 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 3`
- `0 <= ui, vi < n`
- `1 <= wi <= 10^4`
- `1 <= queries.length <= 10^5`
- `queries[j].length == 3`
- `0 <= src1j, src2j, destj < n`
- `src1j, src2j, destj` 两两不同
- 输入保证 `edges` 构成一棵合法的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一次询问**，把整棵树都遍历一遍，算出三对节点之间的距离  
`d(src1, src2) , d(src1, dest) , d(src2, dest)`，再套用题目给出的公式  

\[
\text{答案} = \frac{d(src1, src2)+d(src1, dest)+d(src2, dest)}{2}
\]

> **为什么这样可以得到答案？**  
> 在一棵**树**里，任意两点之间的唯一路径必然是最短的。把三条路径合在一起会出现重复的边（公共部分），而恰好这些重复的边的权重会被加了两次。把三条路径的总权重除以 2，就把重复的那一份去掉，得到恰好覆盖这三个节点的最小连通子树（即 **Steiner 树** 在树上的特例）。

**实现细节**  
- 把 `edges` 建成邻接表 `graph[u] = [(v, w), …]`。  
- 对每个查询，分别以 `src1`、`src2`、`dest` 为起点做一次 **DFS/BFS**，得到从该起点到所有节点的距离数组 `dist[]`（因为是树，遍历一次就能得到所有距离）。  
- 用这三组距离直接算出上面的三对距离。  

> **生活化类比**  
> 把树想象成一座城镇的道路网络，`dist[]` 就像是“从某个出发点开车到城镇里每个地点需要的油费”。我们把三个出发点的油费表都算出来，然后按照公式算出最省油的路线。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def minimumWeightedSubgraph_bruteforce(edges: List[List[int]],
                                      queries: List[List[int]]) -> List[int]:
    # ---------- 建图 ----------
    n = max(max(u, v) for u, v, _ in edges) + 1
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # ---------- 求单点到所有节点的距离 ----------
    def bfs(start: int) -> List[int]:
        """树上单点 BFS，返回 start 到每个节点的最短距离（权重和）"""
        dist = [-1] * n
        q = deque([start])
        dist[start] = 0
        while q:
            cur = q.popleft()
            for nxt, w in graph[cur]:
                if dist[nxt] == -1:                # 只访问一次，树上没有环
                    dist[nxt] = dist[cur] + w
                    q.append(nxt)
        return dist

    ans = []
    for src1, src2, dest in queries:
        # 3 次 BFS，分别得到三组距离
        d1 = bfs(src1)          # 到所有点的距离
        d2 = bfs(src2)
        d3 = bfs(dest)

        # 三对节点的距离
        d_ab = d1[src2]         # src1 -> src2
        d_ac = d1[dest]         # src1 -> dest
        d_bc = d2[dest]         # src2 -> dest

        # 公式： (d_ab + d_ac + d_bc) / 2
        ans.append((d_ab + d_ac + d_bc) // 2)

    return ans
```

> **关键行中文注释**  
> - `dist[nxt] = dist[cur] + w` ← 累加边权，得到从起点到 `nxt` 的总油费  
> - `if dist[nxt] == -1` ← 树上只需要遍历一次，防止回头  

#### 复杂度  

- **时间复杂度**：  
  对每个查询我们要跑 **3 次 BFS**，每次遍历全部 `n` 条边 → `O(3·(n‑1)) ≈ O(n)`。  
  总共 `q` 条查询 → `O(q·n)`。  
  用大白话说，就是“每个查询都要把整棵树重新走一遍”，如果 `n` 和 `q` 都是几万，就会很慢。  

- **空间复杂度**：  
  邻接表存 `O(n)` 条边，`dist` 数组每次 `O(n)`，但只保留当前查询的三份 → `O(n)`。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次查询都重新遍历整棵树**。树的结构是不变的，只是我们需要**快速得到两点之间的距离**。  
如果能够在 **预处理阶段** 把所有节点之间的距离信息压缩存下来，查询时只用 `O(log n)` 或 `O(1)` 就能得到两点距离，整体复杂度就会从 `O(q·n)` 降到 `O((n+q)·log n)`。

**核心技巧**：**二进制提升（Binary Lifting） + LCA（最近公共祖先）**  

1. **根树**  
   随便挑一个节点（这里选 `0`）作为根，做一次 DFS/ BFS，记录  
   - `depth[x]`：根到 `x` 的层数（边数）  
   - `distRoot[x]`：根到 `x` 的**权重和**（即从根到 `x` 所有边的权重之和）  
   - `parent[0][x]`：`x` 的直接父节点  

2. **二进制提升表**  
   对每个节点保存它的 `2^k` 级祖先 `parent[k][x]`（`k` 从 0 到 `⌈log2 n⌉`）。  
   递推公式：`parent[k][x] = parent[k‑1][ parent[k‑1][x] ]`  

   这相当于在树上装了一个“跳楼梯的电梯”，可以在 `O(log n)` 步把节点提升到任意更高的祖先。

3. **求 LCA**（最近公共祖先）  
   - 先把两个节点提升到同一深度（使用提升表）。  
   - 再同时向上跳，直到它们的父节点相同，那个父节点就是 LCA。  
   整个过程只需要 `O(log n)` 步。

4. **两点距离公式**  
   已知 `distRoot[x]`（根到 `x` 的权重和）和 `L = LCA(x, y)`，则  

   \[
   d(x, y) = distRoot[x] + distRoot[y] - 2 \times distRoot[L]
   \]

   这就是“从根出发到 x，再回到根，再到 y”，把公共部分（根到 L 的路径）减掉两次。

5. **三点最小子树**  
   对任意三点 `a, b, c`，最小连通子树的权重等于  

   \[
   \frac{d(a, b) + d(b, c) + d(c, a)}{2}
   \]

   这在树上始终成立，因为三条路径的交叉部分恰好被加了两次，除以 2 把重复的那一层去掉。

**综上**：  
- 预处理 `O(n log n)`（DFS + 构造提升表）  
- 每个查询只需要三次 `distance`（每次 `O(log n)`）→总 `O(q log n)`  

> **类比**  
> 想象树是一本层层嵌套的目录（根 → 子文件夹 → …），  
> - `depth` 就是“在目录树里有多少层”。  
> - `parent[k][x]` 像是“直接跳到第 2^k 层上级目录的快捷键”。  
> - LCA 就是“两个文件最近的共同父文件夹”。  
> 有了这些快捷键，找共同父文件夹只需要几次点击，而不必一步一步往上爬。

#### 代码（Python）

```python
from collections import defaultdict, deque
from math import ceil, log2
from typing import List

def minimumWeightedSubgraph(edges: List[List[int]],
                           queries: List[List[int]]) -> List[int]:
    # ---------- 1. 建图 ----------
    n = max(max(u, v) for u, v, _ in edges) + 1
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    LOG = ceil(log2(n)) + 1               # 够大的层数

    # ---------- 2. 预处理：depth、distRoot、parent[0] ----------
    depth = [0] * n
    distRoot = [0] * n                     # 根到每个节点的权重和
    parent = [[-1] * n for _ in range(LOG)]

    # BFS（也可以用 DFS），从根 0 开始
    q = deque([0])
    visited = [False] * n
    visited[0] = True
    while q:
        cur = q.popleft()
        for nxt, w in graph[cur]:
            if not visited[nxt]:
                visited[nxt] = True
                depth[nxt] = depth[cur] + 1
                distRoot[nxt] = distRoot[cur] + w
                parent[0][nxt] = cur          # 直接父亲
                q.append(nxt)

    # ---------- 3. 二进制提升表 ----------
    for k in range(1, LOG):
        for v in range(n):
            if parent[k-1][v] != -1:
                parent[k][v] = parent[k-1][ parent[k-1][v] ]

    # ---------- 4. LCA 与距离 ----------
    def lca(u: int, v: int) -> int:
        """返回 u, v 最近公共祖先，时间 O(log n)"""
        if depth[u] < depth[v]:
            u, v = v, u               # 保证 u 更深

        # 把 u 提升到和 v 同深度
        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = parent[bit][u]
            diff >>= 1
            bit += 1

        if u == v:
            return u

        # 同时向上跳，直到父节点相同
        for k in range(LOG-1, -1, -1):
            if parent[k][u] != -1 and parent[k][u] != parent[k][v]:
                u = parent[k][u]
                v = parent[k][v]

        return parent[0][u]            # 直接父亲即为 LCA

    def distance(u: int, v: int) -> int:
        """两点权重距离"""
        anc = lca(u, v)
        return distRoot[u] + distRoot[v] - 2 * distRoot[anc]

    # ---------- 5. 逐条查询 ----------
    ans = []
    for a, b, c in queries:
        d_ab = distance(a, b)
        d_bc = distance(b, c)
        d_ca = distance(c, a)
        ans.append((d_ab + d_bc + d_ca) // 2)   # 公式除以 2

    return ans
```

> **代码要点中文注释**  
> - `parent[0][nxt] = cur` ← 记录 `nxt` 的直接父节点（树的“上一级目录”）  
> - `if diff & 1: u = parent[bit][u]` ← 用二进制位把深度差一次性跳过去  
> - `for k in range(LOG-1, -1, -1): …` ← 从最高位向下检查，确保一次跳最大距离，保证 `O(log n)`  

#### 复杂度  

- **时间复杂度**  
  - 预处理：`O(n log n)`（一次 BFS + `LOG` 次遍历所有节点构表）  
  - 每个查询：三次 `distance`，每次 `O(log n)` → `O(q log n)`  
  - 总计：`O((n + q)·log n)`。相比暴力的 `O(q·n)`，当 `n、q` 达到 `10⁵` 时提升数十倍，完全可以在 1 秒左右跑完。

- **空间复杂度**  
  - 邻接表 `O(n)`  
  - `parent` 表 `O(n log n)`（每个节点存 `log n` 个祖先）  
  - 其余数组 `O(n)`  
  - 合计 `O(n log n)`，在 `n ≤ 10⁵` 时约几 MB，符合题目限制。

---

## 心得

- **核心技巧**：**二进制提升 + LCA**，让我们在树上可以 **快速求两点距离**。  
- **适用题型**（类似思路）  
  1. “查询两点之间的最短路径权重” （典型 LCA 应用）  
  2. “树上两点距离的 K 次方求和”  
  3. “在树上求两个节点的最近公共祖先”  

> **一句话总结解题钥匙**：  
> 把树根下来，预处理好每个节点的“跳跃祖先”，任意两点距离只用公式 `distRoot[x] + distRoot[y] - 2·distRoot[LCA]` 即可，随后套用三点子树公式即可得到答案。

---

## 反思

- **第一反应**：直接把每条路径都跑一遍，算出三对距离——这就是暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：树的根选哪儿都行，但一定要保证所有节点都被遍历到（`visited` 防止回到父节点）。  
  - **二进制提升表的大小**：`LOG = ceil(log2(n)) + 1` 必须足够大，否则最高层会越界。  
  - **整数除法**：公式除以 2 必须是整除（题目保证权重整数），使用 `//` 防止浮点数。  
- **下次遇到同类题**：第一步就想 “**是否需要快速求 LCA/两点距离**”。如果答案是 Yes，立刻构建二进制提升表或欧拉序 + RMQ；随后把题目要求的“最小连通子树”转化为已知的距离公式即可。