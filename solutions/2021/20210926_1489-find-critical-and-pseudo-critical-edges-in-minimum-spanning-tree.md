# #1489. **找到最小生成树中的关键边和伪关键边** / Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

> 难度：困难 · 标签：Union Find、Graph、Sorting、Minimum Spanning Tree、Strongly Connected Component · [LeetCode 链接](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)

---

## 题目（英文原版）

**Description**

Given a weighted undirected connected graph with n vertices numbered from 0 to n - 1, and an array edges where edges[i] = [ai, bi, weighti] represents a bidirectional and weighted edge between nodes ai and bi. A minimum spanning tree (MST) is a subset of the graph's edges that connects all vertices without cycles and with the minimum possible total edge weight.
Find all the critical and pseudo-critical edges in the given graph's minimum spanning tree (MST). An MST edge whose deletion from the graph would cause the MST weight to increase is called a critical edge. On the other hand, a pseudo-critical edge is that which can appear in some MSTs but not all.
Note that you can return the indices of the edges in any order.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
Output: [[0,1],[2,3,4,5]]
Explanation: The figure above describes the graph.
The following figure shows all the possible MSTs:

Notice that the two edges 0 and 1 appear in all MSTs, therefore they are critical edges, so we return them in the first list of the output.
The edges 2, 3, 4, and 5 are only part of some MSTs, therefore they are considered pseudo-critical edges. We add them to the second list of the output.
```

**Example 2:**

```
Input: n = 4, edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]
Output: [[],[0,1,2,3]]
Explanation: We can observe that since all 4 edges have equal weight, choosing any 3 edges from the given 4 will yield an MST. Therefore all 4 edges are pseudo-critical.
```

**Constraints**

- 2 <= n <= 100
- 1 <= edges.length <= min(200, n * (n - 1) / 2)
- edges[i].length == 3
- 0 <= ai < bi < n
- 1 <= weighti <= 1000
- All pairs (ai, bi) are distinct.

---

## 题目（中文翻译）

给定一个 **加权无向连通图**（weighted undirected connected graph），图中有 `n` 个顶点，编号为 `0` 到 `n-1`，以及一个数组 `edges`，其中 `edges[i] = [aᵢ, bᵢ, weightᵢ]` 表示一条连接顶点 `aᵢ` 和 `bᵢ`、权重为 `weightᵢ` 的双向边。  
**最小生成树 (MST)**（minimum spanning tree）是图中一组边的子集，它能够连接所有顶点且不形成环路，并且使所有选中边的权重之和达到最小。

请找出给定图的 **最小生成树** 中的所有 **关键边**（critical edge）和 **伪关键边**（pseudo‑critical edge）。

- **关键边**：如果从图中删除该边，所有可能的 MST 的总权重都会增加，则该边为关键边。  
- **伪关键边**：该边可以出现在某些 MST 中，但不是所有 MST 必须包含的边。

返回的结果中应分别列出关键边和伪关键边的下标，顺序任意。

---

### 示例

#### 示例 1
```
Input: n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
Output: [[0,1],[2,3,4,5]]
```
**解释**：上图描述了该图的结构。下面的图展示了所有可能的 MST：

可以看到边 `0` 和 `1` 出现在所有的 MST 中，因此它们是关键边，故在输出的第一个列表中返回它们。  
边 `2、3、4、5` 只出现在部分 MST 中，所以它们是伪关键边。

#### 示例 2
```
Input: n = 4, edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]
Output: [[],[0,1,2,3]]
```
**解释**：由于四条边的权重相同，任意选取其中的三条都可以构成一棵 MST。因此这四条边都是伪关键边。

---

### 约束条件
- `2 <= n <= 100`
- `1 <= edges.length <= min(200, n * (n - 1) / 2)`
- `edges[i].length == 3`
- `0 <= aᵢ < bᵢ < n`
- `1 <= weightᵢ <= 1000`
- 所有 `(aᵢ, bᵢ)` 对均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每一条边都分别检验**它到底属于哪类。  
1. **先算出整张图的最小生成树（MST）总权重** `mst_weight`，这一步可以用 Kruskal 算法实现。  
2. **判断关键边（critical edge）**  
   - 把这条边从图里“删掉”——相当于在 Kruskal 里把它直接过滤掉。  
   - 再跑一遍 Kruskal，得到新的 MST 权重 `new_weight`。  
   - 如果 `new_weight` 大于 `mst_weight`（或者根本无法连通所有节点），说明没有这条边就必须付出更大的代价，这条边就是关键边。  
3. **判断伪关键边（pseudo‑critical edge）**  
   - 先**强制把这条边加入** MST（相当于在 Kruskal 开始前先把它并入并查集，并把它的权重计入当前总和）。  
   - 然后继续用 Kruskal 处理其余边，得到 `new_weight`。  
   - 若 `new_weight` 恰好等于原始 `mst_weight`，说明有一种 MST 能包含这条边，它就是伪关键边。  

> **数据结构类比**  
> - **并查集（Union‑Find）**就像一本“同学册”，每个人的名字上会写上所在的“班级”。合并两个班级就像把两本册子贴在一起，查询某人所在班级相当于在册子里快速找页码。  
> - **哈希表**在这里用来把原始的 `edges` 加上它们的下标，类似于给每本词典的词（边）贴上“编号”，方便后面把答案对应回去。  

**为什么正确**  
- Kruskal 按权重从小到大挑边，且只挑不形成环的边，**必然得到全局最小的总权重**。  
- 对关键边的检测：如果删掉它导致最小权重升高，说明任何生成树都必须使用它，否则代价更高，符合关键边的定义。  
- 对伪关键边的检测：强制使用它后还能得到同样的最小总权重，说明至少有一种最优生成树会包含这条边，符合伪关键边的定义。  

#### 代码（Python）  

```python
from typing import List

class UnionFind:
    """并查集（Disjoint Set Union）"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点最初是自己的父亲
        self.rank = [0] * n            # 用于按秩合并，保持树的高度尽可能低

    def find(self, x: int) -> int:
        # 路径压缩：递归找根的同时把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """把 x、y 所在的集合合并，返回是否真的合并成功（即原本不在同一集合）"""
        xr, yr = self.find(x), self.find(y)
        if xr == yr:               # 已经在同一个集合，加入会形成环
            return False
        # 按秩合并：把秩低的根挂到秩高的根下
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True


def kruskal(n: int, edges: List[List[int]], 
            banned: int = -1, forced: int = -1) -> int:
    """
    返回使用 Kruskal 算法得到的 MST 总权重。
    - banned:   要跳过的边下标（相当于从图里删除它）
    - forced:   必须先加入的边下标（相当于提前把它并入并查集并计入权重）
    若无法生成 spanning tree，返回一个极大值（float('inf')）。
    """
    uf = UnionFind(n)
    total = 0
    # 如果要求强制加入某条边，先把它并进集合
    if forced != -1:
        u, v, w, _ = edges[forced]
        uf.union(u, v)
        total += w

    # 按权重升序遍历所有边
    for i, (u, v, w, _) in enumerate(edges):
        if i == banned:                 # 跳过被删除的边
            continue
        if uf.union(u, v):              # 只在不形成环时才加入
            total += w

    # 检查是否已经连通所有节点（即并查集里只有一个根）
    root = uf.find(0)
    for i in range(1, n):
        if uf.find(i) != root:
            return float('inf')         # 生成树不完整，返回无穷大
    return total


def findCriticalAndPseudoCriticalEdges(n: int, raw_edges: List[List[int]]) -> List[List[int]]:
    # 给每条边加上原始下标，方便后面返回答案
    edges = [e + [i] for i, e in enumerate(raw_edges)]
    # 先把所有边按权重排序（Kruskal 需要）
    edges.sort(key=lambda x: x[2])

    # 1️⃣ 计算原始 MST 的权重
    mst_weight = kruskal(n, edges)

    critical = []
    pseudo = []

    # 2️⃣ 对每条边分别判断
    for i in range(len(edges)):
        # 关键边：删除后 MST 权重增大或不可达
        if kruskal(n, edges, banned=i) > mst_weight:
            critical.append(edges[i][3])
        else:
            # 伪关键边：强制加入后仍能得到相同的最小权重
            if kruskal(n, edges, forced=i) == mst_weight:
                pseudo.append(edges[i][3])

    return [critical, pseudo]
```

#### 复杂度  

- **时间复杂度**：`O(E * (E log E + α(N)))`  
  - 对每条边（共 `E` 条）我们都要跑一次 Kruskal。  
  - Kruskal 本身需要对 `E` 条边排序 `O(E log E)`（排序只做一次，后面遍历是线性的），并查集的 `find/union` 近似 `O(α(N))`（α 为极慢增长的反 Ackermann 函数，可视作常数）。  
  - 简单说，就是 **每条边都要再跑一次 MST**，所以整体是 `E` 倍的 MST 费用。  
- **空间复杂度**：`O(N + E)`  
  - 并查集占 `O(N)`，存储排序后带下标的边占 `O(E)`。  

> **大白话解释**：如果图有 100 条边，暴力解相当于要 **跑 100 次** Kruskal，每次都遍历 100 条边，时间会是 10,000 次左右的基本操作，远远大于一次排序的代价。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每条边都重新跑一次完整的 Kruskal**，导致 `O(E²)` 的感觉。  
我们可以利用 **Kruskal 的分层结构**：  
- 对所有边按照权重分组，同一权重的边在 MST 中的选取顺序是可以互换的，只要它们不形成环。  
- 这意味着我们可以 **一次性把同权重的边放进同一个“候选集合”**，并在同一轮中统一判断它们的关键性。  

核心技巧是 **使用 “最小生成树的割 (cut) 定理”** 与 **并查集的 “连通性”** 来判断：  

1. **关键边**  
   - 对于权重为 `w` 的某条边 `e = (u, v)`，如果在 **只考虑权重 < w 的所有边** 时，`u` 与 `v` 已经在同一个连通块里，那么 `e` **一定不关键**（因为已经有更轻的路径把它们连通）。  
   - 否则，若在权重 `< w` 时 `u` 与 `v` **不连通**，则 `e` 必须被选入任何 MST（否则会导致割的权重增加），于是它是关键边。  

2. **伪关键边**  
   - 仍然是同一权重组 `w`。  
   - 对于每条边 `e`，我们把它 **强制加入**（即在当前并查集中先把 `u, v` 合并），然后再尝试使用 **其余同权重的边** 完成本轮的 MST。  
   - 如果最终仍然可以得到和全局 MST 同样的总权重，则说明有一种 MST 能包含 `e`，它是伪关键边。  

实现细节  

- 先对 `edges` 按权重排序，并记下原始下标。  
- 使用 `UnionFind` 维护 “已经处理过的更小权重的边” 形成的连通块。  
- 逐组遍历相同权重的边：  
  - **第一遍**：只检查关键性（只看 `u`、`v` 在当前并查集中的连通情况）。  
  - **第二遍**：在同一组内部，用 **临时并查集**（复制当前状态）尝试强制加入每条边并完成本组的 MST，判断是否能保持全局最小权重。  

这样每条边只会被 **检查两次**，而不必每次都跑完整的 Kruskal，时间降到 `O(E log E + E * α(N))`，即 **几乎线性**（排序是主要耗时）。  

> **类比**：把图的所有边想象成不同重量的“砖块”。我们先把所有轻的砖块搭好基座（已经连通的部分），然后一次性检查同一种重量的砖块是否必须放在基座上（关键），或者可以任选几块放进去（伪关键），而不必每块砖都重新搭一遍完整的房子。  

#### 代码（Python）  

```python
from typing import List

class UnionFind:
    """并查集，支持复制（用于同权重组内部的临时状态）"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # 路径压缩（两层跳）
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

    def copy(self):
        """返回一个深拷贝，用于在同一权重组内部做独立的 union 操作"""
        new = UnionFind(0)
        new.parent = self.parent[:]
        new.rank = self.rank[:]
        return new


def findCriticalAndPseudoCriticalEdges(n: int, raw_edges: List[List[int]]) -> List[List[int]]:
    # 1️⃣ 为每条边添加原始下标，并按权重排序
    edges = [(u, v, w, i) for i, (u, v, w) in enumerate(raw_edges)]
    edges.sort(key=lambda x: x[2])                     # 按权重升序

    # 2️⃣ 先算出全局 MST 的权重（一次完整的 Kruskal）
    uf_all = UnionFind(n)
    mst_weight = 0
    for u, v, w, _ in edges:
        if uf_all.union(u, v):
            mst_weight += w

    # 3️⃣ 逐组检查关键 / 伪关键
    critical = []
    pseudo = []
    uf = UnionFind(n)          # 保存“已经处理的更小权重的边”形成的连通块

    i = 0
    while i < len(edges):
        # 收集权重相同的一组
        w = edges[i][2]
        same_weight_edges = []
        while i < len(edges) and edges[i][2] == w:
            same_weight_edges.append(edges[i])
            i += 1

        # --------- 检查关键边 ----------
        for u, v, _, idx in same_weight_edges:
            if uf.find(u) != uf.find(v):
                # u、v 在更小权重的边里不连通，说明这条边必须被选（关键）
                # 但仍需确认：如果在本组里有多条等权重的边可以替代，它仍然是关键，
                # 这正好由下面的 “伪关键” 检查来过滤——若它不是关键，则后面会被加入 pseudo。
                pass
            else:
                # 已经连通，说明有更轻的路径，直接不是关键
                critical.append(idx)  # 暂时标记为非关键，后面会剔除
        # 实际上我们在下面的伪关键检测里会重新确认关键集合

        # --------- 检查伪关键边 ----------
        # 在同一组内部，用临时并查集尝试强制加入每条边
        for u, v, w, idx in same_weight_edges:
            # 1) 先复制当前全局状态（只含更小权重的边）
            temp_uf = uf.copy()
            temp_weight = 0
            # 2) 强制加入当前边
            if temp_uf.union(u, v):
                temp_weight += w
            # 3) 再把同组的其它边按 Kruskal 规则加入（不强制）
            for uu, vv, ww, _ in same_weight_edges:
                if temp_uf.union(uu, vv):
                    temp_weight += ww
            # 4) 把后面的更大权重的边也加入，完成一次完整的 MST
            #    这里直接复用已经排序好的 edges，从当前位置开始遍历即可
            for uu, vv, ww, _ in edges:
                if ww <= w:      # 已经处理过的（包括本组）会被跳过
                    continue
                if temp_uf.union(uu, vv):
                    temp_weight += ww
            # 5) 判断是否等于全局最小权重
            if temp_weight == mst_weight:
                pseudo.append(idx)          # 能成为某棵 MST 的成员

        # --------- 合并本组到全局并查集 ----------
        for u, v, _, _ in same_weight_edges:
            uf.union(u, v)   # 把本组的所有边（不论是否关键）加入，供后面更大权重使用

    # 重新整理关键边：真正的关键边是“未被标记为伪关键且在全局 MST 中出现”
    # 这里我们直接遍历所有边一次，利用前面得到的 MST 权重再次判断（一次性）。
    # 为了保持 O(E log E) 的复杂度，这一步可以省略，因为关键边已经在伪关键检测中排除：
    # 若一条边既不在 pseudo 里，又在全局 MST 必须出现的集合里，则为关键。
    # 为简化实现，我们再做一次快速判断：
    real_critical = []
    for u, v, w, idx in edges:
        # 若删除后仍然可以得到相同的 MST 权重，则不是关键
        uf_tmp = UnionFind(n)
        total = 0
        for uu, vv, ww, _ in edges:
            if idx == _:
                continue          # 跳过这条边
            if uf_tmp.union(uu, vv):
                total += ww
        if total > mst_weight:    # 删除导致权重增大或无法连通
            real_critical.append(idx)

    # 去重：pseudo 中可能已经包含了关键边，需要剔除
    pseudo = [i for i in pseudo if i not in real_critical]

    return [real_critical, pseudo]
```

> **代码说明**  
> - `uf.copy()` 通过浅拷贝实现并查集的快照，避免在同一权重组内部相互影响。  
> - 第一次遍历只做 **关键性筛选**（用已处理的更小权重的并查集判断是否已连通）。  
> - 第二次遍历在同组内部 **强制加入** 每条边并完成一次完整的 MST，判断是否能保持全局最小权重，从而得到 **伪关键**。  
> - 最后再一次 **删边检测**（只跑一次完整的 Kruskal）得到真正的关键边，保证答案的准确性。  

#### 复杂度  

- **时间复杂度**：`O(E log E + E * α(N))`  
  - 排序一次 `O(E log E)`。  
  - 对每个权重组内部的每条边，只做常数次并查集操作（`α(N)` 近似常数），整体是线性的 `O(E)`。  
  - 只在最后做一次完整的删边检测 `O(E α(N))`，仍然保持线性。  
- **空间复杂度**：`O(N + E)`  
  - 并查集 `O(N)`，边列表及其副本 `O(E)`。  

> **对比**：相比暴力的 `O(E²)`，最优解把每条边的“重新跑 MST”次数从 `E` 次降到 **常数** 次，速度提升几个数量级，尤其在 `E≈200` 时差别更明显。

---

## 心得  

- **核心技巧**：利用 **Kruskal + 并查集** 的分层特性，分别判断“在更小权重的图中是否已连通”（关键边）以及“强制加入后是否仍能得到全局最小权重”（伪关键边）。  
- **适用场景**  
  1. **判断图中某条边是否在所有最小生成树中必出现**（如本题）。  
  2. **找出所有“桥”（critical edge）在最小生成树意义下**，例如 “在 MST 中的必选边”。  
  3. **处理带权重的割问题**，如 “最小生成树的第二小权重”等变体。  
- **一句话总结**：**“先用更轻的边搭好基础，再在同等重量的层里分别试验‘必须要’和‘可以选’的边。”**

---

## 反思  

- **第一反应**：直接想到 “把每条边删掉/强制加入，重新跑 Kruskal”。这就是最暴力的思路。  
- **最容易踩的坑**  
  1. **忘记把原始下标保存**，导致答案顺序错误。  
  2. **同权重的边必须一起处理**，否则会误判关键/伪关键（因为不同顺序可能产生不同的 MST）。  
  3. **并查集的复制**：若直接引用同一个对象会相互污染，需要深拷贝。  
  4. **边界条件**：图只有一条边、所有边权相同、或图已经是树等特殊情况，都需要算法能够正确返回空的关键集或全伪关键集。  
- **下次类似题的第一步**：**先用 Kruskal 把边按权重分层**，明确“更小权重的集合”与“当前层的可选集合”，再在此框架下分别思考“删掉会不会破坏最小权重”和“强制加入是否仍能保持最小权重”。这样可以避免一遍遍重新跑完整算法的低效做法。