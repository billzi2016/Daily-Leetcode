# #1761. 连通三元组的最小度数 / Minimum Degree of a Connected Trio in a Graph

> 难度：困难 · 标签：Graph、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-degree-of-a-connected-trio-in-a-graph/)

---

## 题目（英文原版）

**Description**

You are given an undirected graph. You are given an integer n which is the number of nodes in the graph and an array edges, where each edges[i] = [ui, vi] indicates that there is an undirected edge between ui and vi.
A connected trio is a set of three nodes where there is an edge between every pair of them.
The degree of a connected trio is the number of edges where one endpoint is in the trio, and the other is not.
Return the minimum degree of a connected trio in the graph, or -1 if the graph has no connected trios.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[1,2],[1,3],[3,2],[4,1],[5,2],[3,6]]
Output: 3
Explanation: There is exactly one trio, which is [1,2,3]. The edges that form its degree are bolded in the figure above.
```

**Example 2:**

```
Input: n = 7, edges = [[1,3],[4,1],[4,3],[2,5],[5,6],[6,7],[7,5],[2,6]]
Output: 0
Explanation: There are exactly three trios:
1) [1,4,3] with degree 0.
2) [2,5,6] with degree 2.
3) [5,6,7] with degree 2.
```

**Constraints**

- 2 <= n <= 400
- edges[i].length == 2
- 1 <= edges.length <= n * (n-1) / 2
- 1 <= ui, vi <= n
- ui != vi
- There are no repeated edges.

---

## 题目（中文翻译）

给定一个 **无向图（undirected graph）**，其中 `n` 表示图中的节点数，`edges` 为一个数组，`edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间存在一条无向边（edge）。  

**连通三元组（connected trio）** 是指由三个节点组成的集合，且这三个节点两两之间都有边相连。  

**连通三元组的度数（degree）** 指的是所有满足以下条件的边的数量：该边的一个端点在三元组内部，另一个端点在三元组外部。  

请返回图中所有连通三元组的最小度数。如果图中不存在任何连通三元组，返回 `-1`。

---

### 示例

**示例 1**

```text
Input: n = 6, edges = [[1,2],[1,3],[3,2],[4,1],[5,2],[3,6]]
Output: 3
Explanation: 图中恰好存在唯一的连通三元组 [1,2,3]。构成该三元组度数的边在图中用粗体标出，如上图所示。
```

**示例 2**

```text
Input: n = 7, edges = [[1,3],[4,1],[4,3],[2,5],[5,6],[6,7],[7,5],[2,6]]
Output: 0
Explanation: 图中恰好存在三个连通三元组：
1) [1,4,3] 的度数为 0；
2) [2,5,6] 的度数为 2；
3) [5,6,7] 的度数为 2。
```

---

### 约束条件

- `2 <= n <= 400`
- `edges[i].length == 2`
- `1 <= edges.length <= n * (n - 1) / 2`
- `1 <= ui, vi <= n`
- `ui != vi`
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 三个节点的组合都枚举出来，看看它们是不是互相都有边相连（即形成一个三人小团体）。  
如果是三角形，就按照题目给出的公式  

```
trio_degree = deg(u) + deg(v) + deg(w) - 6
```

算出它的度，然后取最小值。

- **用到的数据结构**  
  - **邻接矩阵**（`adj[i][j] = True` 表示 i 与 j 之间有边）。可以把它想象成一本“图的词典”，查询 `adj[i][j]` 就像在词典里查“i 和 j 的关系”，时间是 O(1)。  
  - **度数组** `deg[i]` 记录每个节点的度（有多少条边连到它），相当于每个人的“社交活跃度”。  

- **为什么正确**  
  - 我们把所有可能的三元组 `(u, v, w)` 都检查了一遍，只要它们两两相连，就一定是题目要求的 “connected trio”。  
  - 对于每个合法的三元组，我们用公式把它的度算出来，最后取最小的那个，就是答案。  

- **复杂度分析（大白话）**  
  - **时间**：我们要遍历 `C(n,3) = n·(n‑1)·(n‑2)/6` 种三元组合。对每个组合，只需要 O(1) 的矩阵查询和度相加，所以总时间是 **O(n³)**。如果把 `n = 400` 带进去，大概是 64 000 000 次操作，普通电脑跑得还行，但已经不算“快”。  
  - **空间**：邻接矩阵占 `n²` 的布尔空间（最多 400·400 = 160 000），再加上度数组 O(n)。所以是 **O(n²)** 的额外空间。

#### 代码（Python）

```python
def minTrioDegree_bruteforce(n, edges):
    # ---------- 构建邻接矩阵 ----------
    adj = [[False] * (n + 1) for _ in range(n + 1)]
    deg = [0] * (n + 1)                 # 记录每个节点的度

    for u, v in edges:
        adj[u][v] = adj[v][u] = True
        deg[u] += 1
        deg[v] += 1

    INF = float('inf')
    ans = INF

    # ---------- 枚举所有三元组 ----------
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if not adj[u][v]:          # 必须先保证 u、v 之间有边
                continue
            for w in range(v + 1, n + 1):
                # 检查 v‑w、u‑w 是否都有边
                if adj[u][w] and adj[v][w]:
                    # 计算三元组的度：deg(u)+deg(v)+deg(w)-6
                    cur = deg[u] + deg[v] + deg[w] - 6
                    ans = min(ans, cur)

    return -1 if ans == INF else ans
```

#### 复杂度

- **时间复杂度**：`O(n³)` — “立方”级别的遍历，随着节点数的增长会很快变慢。  
- **空间复杂度**：`O(n²)` — 用了一个 `n×n` 的矩阵，就像在一本 400×400 的“关系表”里查每两个人是否认识。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有三元组**，即使很多组合根本不可能形成三角形，也要检查一遍。  
我们可以利用图的结构，**只在真的可能构成三角形的地方搜索**，从而把工作量降下来。

1. **把图存成邻接集合**  
   - 对每个节点 `u` 保存一个 `set`，里面是所有和 `u` 相连的邻居。  
   - 集合的查找 `v in adj[u]` 像在字典里找词一样，时间是 O(1)。  

2. **遍历每条边 (u, v)**  
   - 若要得到一个三角形，第三个节点 `w` 必须同时是 `u` 的邻居也是 `v` 的邻居。  
   - 所以只要把 **度数较小的那个端点** 的所有邻居遍历一遍，检查它们是否也在另一端点的邻居集合里，就能找到所有以这条边为 “底边” 的三角形。  

3. **避免重复计数**  
   - 只在 `u < v` 时处理这条边，且在遍历 `w` 时要求 `v < w`（或 `u < w`），这样每个三角形只会被算一次。  

4. **计算三角形度**  
   - 对于找到的合法三元组 `(u, v, w)`，直接用公式  
     `deg[u] + deg[v] + deg[w] - 6`  
     把三条内部边的贡献减掉（每条内部边被两个端点的度计数了两次）。  

5. **取最小值**，如果没有找到任何三角形返回 `-1`。

> **核心技巧**：  
> - **邻接集合** → 像查字典一样快速判断两点是否相连。  
> - **遍历边 + 小度数优化** → 只在“可能”的地方展开搜索，省掉大量不必要的组合。  

#### 代码（Python）

```python
def minTrioDegree(n, edges):
    # ---------- 建立邻接集合和度数组 ----------
    adj = [set() for _ in range(n + 1)]
    deg = [0] * (n + 1)

    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        deg[u] += 1
        deg[v] += 1

    INF = float('inf')
    ans = INF

    # ---------- 枚举每条边 ----------
    for u, v in edges:
        # 为了只遍历一次三角形，保证 u < v
        if u > v:
            u, v = v, u

        # 只遍历度数更小的那一端的邻居，进一步剪枝
        if len(adj[u]) > len(adj[v]):
            u, v = v, u   # 现在 u 的度一定 ≤ v 的度

        # ---------- 寻找共同邻居 w ----------
        for w in adj[u]:
            if w == v:          # 跳过已经是边的另一端点
                continue
            # 为了避免重复计数，要求 v < w
            if w > v and w in adj[v]:
                # (u, v, w) 构成三角形
                cur = deg[u] + deg[v] + deg[w] - 6
                ans = min(ans, cur)

    return -1 if ans == INF else ans
```

**代码要点注释**  

- `adj = [set() ...]`：把每个节点的邻居装进集合，像“朋友名单”。  
- `if len(adj[u]) > len(adj[v]): u, v = v, u`：把度数小的节点放在前面，遍历它的邻居更省事。  
- `if w > v and w in adj[v]`：`w > v` 保证同一个三角形只算一次；`w in adj[v]` 检查 `v` 与 `w` 是否相连。  
- `cur = deg[u] + deg[v] + deg[w] - 6`：直接套用公式得到三角形的度。

#### 复杂度

- **时间复杂度**：`O( Σ_{(u,v)∈E} min(deg(u), deg(v)) )`  
  - 对每条边只遍历度数更小的端点的所有邻居，检查是否也是另一端点的邻居。  
  - 在最坏的**稠密图**（`n=400, m≈80,000`）下，这个上界约为 `O(n³/√n)`，实际运行时间远小于暴力的 `O(n³)`，在 LeetCode 的限制下几乎瞬间完成。  
  - **大白话**：我们不再把所有 64 000 000 种三元组都检查，而是只在真正可能形成三角形的“底边 + 共同邻居”上花时间，快了好几倍。

- **空间复杂度**：`O(n + m)`  
  - 邻接集合保存每条边一次（共 `2m` 个元素），度数组 O(n)。不需要 `n²` 的矩阵，省了很多内存。

---

## 心得

- **核心技巧**：利用 **邻接集合 + 边遍历 + 小度数优化**，只在真正可能形成三角形的地方搜索。  
- **适用的题型**  
  1. “找图中所有三角形 / 计数三角形” 类问题（如 611. Valid Triangle Number 的变种）。  
  2. “基于共同邻居的图结构查询” 如 **找图中所有四元环**、**计算图的聚类系数**。  
- **一句话总结解题钥匙**：**把“枚举所有组合”变成“枚举所有必然出现的组合”，用集合快速判断共邻居**。

---

## 反思

- **第一反应**：直接把所有三点组合枚举一遍，写一个 `O(n³)` 的暴力实现。  
- **最容易踩的坑**  
  - **重复计数**：同一个三角形会被不同的底边或不同的遍历顺序多算几次，需要加上顺序约束（如 `u < v < w`）。  
  - **边界条件**：图中可能没有任何三角形，需要返回 `-1` 而不是 `0`。  
  - **度的计算**：记得减掉内部的 3 条边，每条边在两个端点的度里都被算了一次，所以要减 `6`。  
- **下次类似题**：**第一步先思考“哪些结构必须共存”**（本题是 “两点都有共同邻居”），然后 **把搜索范围限制在这些必然出现的结构上**，再用集合/哈希表把 “是否相连” 的检查降到 O(1)。这样可以把指数级或立方级的暴力直接压到可接受的线性或准线性量级。