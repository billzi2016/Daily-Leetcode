# #685. 冗余连接 II / Redundant Connection II

> 难度：困难 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/redundant-connection-ii/)

---

## 题目（英文原版）

**Description**

In this problem, a rooted tree is a directed graph such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents.
The given input is a directed graph that started as a rooted tree with n nodes (with distinct values from 1 to n), with one additional directed edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed.
The resulting graph is given as a 2D-array of edges. Each element of edges is a pair [ui, vi] that represents a directed edge connecting nodes ui and vi, where ui is a parent of child vi.
Return an edge that can be removed so that the resulting graph is a rooted tree of n nodes. If there are multiple answers, return the answer that occurs last in the given 2D-array.

**Examples**

**Example 1:**

```
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
```

**Example 2:**

```
Input: edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]
Output: [4,1]
```

**Constraints**

- n == edges.length
- 3 <= n <= 1000
- edges[i].length == 2
- 1 <= ui, vi <= n
- ui != vi

---

## 题目（中文翻译）

在本题中，**根树（rooted tree）**是一种**有向图（directed graph）**，其满足以下条件：

- 恰好有一个节点（**根节点（root）**），其余所有节点都是该根节点的后代（**descendant**）；
- 每个节点只有一个父节点（**parent**），除了根节点没有父节点。

给定的输入是一张**有向图（directed graph）**，最初是一棵包含 n 个节点（节点值为 1 到 n，且互不相同）的根树，随后额外添加了一条**有向边（directed edge）**。这条新增的边连接了两个不同的顶点，且在原图中不存在这条边。

结果图以二维数组 `edges` 的形式给出。`edges` 中的每个元素 `[ui, vi]` 表示一条从父节点 `ui` 指向子节点 `vi` 的**有向边（directed edge）**。

返回可以删除的那条边，使得剩余的图重新成为一棵包含 n 个节点的根树。如果存在多条满足条件的边，返回在 `edges` 中出现最靠后的那条。

**示例 1：**  
**示例 2：**  
**约束条件：**

- `n == edges.length`
- `3 <= n <= 1000`
- `edges[i].length == 2`
- `1 <= ui, vi <= n`
- `ui != vi`

**示例：**

**示例 1:**  
Input: `edges = [[1,2],[1,3],[2,3]]`  
Output: `[2,3]`

**示例 2:**  
Input: `edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]`  
Output: `[4,1]`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一条边都暂时删掉一次，看看剩下的图能不能变成一棵合法的有根树**。  
如果删掉第 `i` 条边后，图满足下面两个条件，就说明这条边是「多余的」：

1. **每个节点最多只有一个父节点**（根节点除外）。  
   - 可以把每个节点的父节点记在一个数组 `parent[ ]` 里，遍历所有剩余的边，如果发现同一个孩子被指向两次，就说明不是树。  
2. **不存在环路**，也就是从根出发能够遍历到所有节点且不回到已经走过的节点。  
   - 用一次深度优先搜索（DFS）或广度优先搜索（BFS）检查是否有环。如果在遍历过程中再次碰到已经访问过的节点，就说明有环。

因为要求「如果有多个答案，返回出现最靠后的那条」，所以我们要**从后往前**尝试删除边，这样第一个成功的就是答案。

> **类比**：把图想成一条条「父子」的指令，删掉一条指令后，检查每个人是否只有一个爸爸（父节点），并且从「老祖宗」出发能顺利把指令传递下去且不走回头路。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def findRedundantDirectedConnection(edges: List[List[int]]) -> List[int]:
    n = len(edges)

    # --------- 逐条尝试删除（从后往前） ----------
    for i in range(n - 1, -1, -1):
        # 把第 i 条边删掉，剩下的边组成 new_edges
        new_edges = edges[:i] + edges[i + 1:]

        # 1) 检查每个节点是否至多只有一个父节点
        parent = [0] * (n + 1)          # parent[v] = u 表示 u -> v
        valid = True
        for u, v in new_edges:
            if parent[v] != 0:          # v 已经有父亲了
                valid = False
                break
            parent[v] = u

        if not valid:                    # 直接进入下一条边的尝试
            continue

        # 2) 检查是否有环且恰好只有一个根节点
        # 找根节点（没有父亲的节点），根应该唯一
        roots = [i for i in range(1, n + 1) if parent[i] == 0]
        if len(roots) != 1:              # 根不唯一，肯定不是树
            continue
        root = roots[0]

        # 建图（邻接表）供 BFS 使用
        graph = defaultdict(list)
        for u, v in new_edges:
            graph[u].append(v)

        # BFS 检查连通且无环
        visited = set()
        q = deque([root])
        while q:
            node = q.popleft()
            if node in visited:          # 再次访问到同一个节点说明有环
                break
            visited.add(node)
            for nb in graph[node]:
                q.append(nb)

        # 如果访问了所有 n 个节点且没有提前退出，则是合法的树
        if len(visited) == n:
            return edges[i]               # 第 i 条就是答案

    # 题目保证一定有答案，理论上不会走到这里
    return []
```

**代码要点注释**（已在代码中用中文标出）  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 条边，每次都要 **一次**遍历所有剩余的 `n‑1` 条边来检查父节点合法性，随后再 **一次** BFS/DFS 检查环和连通性。整体是 `n × n`，即平方级。  
  - 大白话：如果有 1000 条边，最坏要做大约 1,000,000 次「检查」——对初学者来说还是可以跑通的，但不是最优的。

- **空间复杂度**：`O(n)`  
  - 需要 `parent`、`graph`、`visited` 等辅助数组/集合，规模都和节点数成线性关系。  

---

### 2. 最优解  

#### 思路  

暴力解的慢点在于**每次都重新遍历整张图**。  
事实上，这道题只涉及 **两种异常情况**，可以在一次遍历中把它们找出来：

1. **某个节点有两个父节点**（入度为 2）。  
   - 记这两条边为 `candidate1 = [u1, v]`（先出现的）和 `candidate2 = [u2, v]`（后出现的）。  
   - 如果存在这种情况，答案一定在这两条边里。

2. **图中出现环**（有向环）。  
   - 环路的出现说明「多加的那条边」恰好把已经是树的结构闭合成环。

根据上述两点，问题可以分成三种情形：

| 情形 | 解释 | 返回哪条边 |
|------|------|-----------|
| **A**：存在入度为 2 且 **去掉 `candidate2` 后**图 **没有环** | 说明多余的边是 `candidate2`（后出现的那条） | `candidate2` |
| **B**：存在入度为 2 且 **去掉 `candidate2` 后**仍然 **有环** | 环是因为 `candidate1` 与其它边共同构成的，删掉 `candidate1` 才能破环 | `candidate1` |
| **C**：**没有**入度为 2（每个节点最多一个父），但 **有环** | 多余的边就是导致环的那条（在所有环边中最靠后） | 在遍历时检测到的环边 |

> **类比**：把每个人的「父亲」想成一本家谱。  
> - 如果某个人出现了两个父亲，就像家谱里写了两条血缘线，需要挑选掉一条。  
> - 如果家谱里出现了循环（A 是 B 的父，B 又是 C 的父，C 又是 A 的父），说明多写了一条「血缘」导致环，需要把这条血缘删掉。

实现这一步的关键工具是 **并查集（Union‑Find）**，它可以在 **近乎 O(1)** 的时间判断两点是否已经在同一个连通块（即是否已经有路径相连），从而快速检测环。

##### 并查集（Union‑Find）简易解释  

- **集合**：把所有节点看成若干「朋友圈」；同一个圈里的节点彼此可以互相到达。  
- **find(x)**：返回节点 `x` 所在圈的「代表」或「根」，相当于找出这位朋友的「领袖」。  
- **union(x, y)**：把 `x` 圈和 `y` 圈合并，等价于把两位领袖拉在一起，让两圈成员成为同一个大圈。  
- 当我们尝试把一条有向边 `u → v` 加入图时，**如果 `u` 和 `v` 已经在同一个圈里**，说明这条边会把已有的路径闭合成环——这正是我们要找的「多余的」边。

##### 具体步骤  

1. **第一遍遍历**：统计每个节点的入度，记录下出现两次的节点 `v`，以及对应的两条边 `candidate1`（先出现）和 `candidate2`（后出现）。  
2. **第二遍遍历（并查集）**：  
   - 对每条边 `u → v`，如果这条边是 `candidate2`（我们先「假装」把它删掉），直接跳过。  
   - 否则，尝试 `union(u, v)`：  
     - 如果 `find(u) == find(v)`，说明加入这条边会形成环。此时：  
       - 若 **不存在** 入度为 2 的情况（即 `candidate1`/`candidate2` 为空），说明这条产生环的边就是答案（情形 C）。  
       - 若 **存在** 入度为 2，则说明环是因为 `candidate1` 与其他边共同形成的，答案应该是 `candidate1`（情形 B）。  
   - 如果遍历结束都没有检测到环，则说明 **去掉 `candidate2` 后图已经是一棵树**，答案是 `candidate2`（情形 A）。  

整个过程只需要 **两次线性遍历**，时间 `O(n)`，空间 `O(n)`。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集实现（路径压缩 + 按秩合并）"""
    def __init__(self, n: int):
        self.parent = list(range(n + 1))   # parent[i] = i 表示每个节点初始是自己所在的集合
        self.rank = [0] * (n + 1)          # 用来优化合并时的树高

    def find(self, x: int) -> int:
        # 递归找根并压缩路径，使后续查询更快
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """把 x、y 所在集合合并。若已经在同一集合返回 False（说明会产生环），否则返回 True"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:          # 已经连通，加入这条边会形成环
            return False
        # 按秩合并：把高度小的树挂到高度大的树下面
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def findRedundantDirectedConnection(edges: List[List[int]]) -> List[int]:
    n = len(edges)
    parent = [0] * (n + 1)          # 记录每个节点的父节点（若有）
    candidate1 = candidate2 = None # 用来保存入度为 2 时的两条候选边

    # ---------- 第一次遍历：找出是否有节点拥有两个父亲 ----------
    for u, v in edges:
        if parent[v] == 0:          # v 还没有父亲，正常记录
            parent[v] = u
        else:                       # v 已经有父亲了，这里出现了入度为 2
            candidate1 = [parent[v], v]   # 之前的那条边
            candidate2 = [u, v]            # 当前这条边（后出现的）
            break

    # ---------- 第二次遍历：并查集检测环 ----------
    uf = UnionFind(n)
    for u, v in edges:
        # 如果我们已经发现了两父节点的情况，且当前边是 candidate2，则暂时「跳过」它
        if candidate2 and [u, v] == candidate2:
            continue

        # 正常尝试合并，若合并失败说明会形成环
        if not uf.union(u, v):
            # 产生环的原因有两种：
            # 1) 没有两父节点的情况 -> 当前这条边就是多余的（情形 C）
            # 2) 有两父节点 -> 说明环是因为 candidate1 引起的（情形 B）
            return candidate1 if candidate1 else [u, v]

    # 如果遍历完都没有环，说明「去掉 candidate2」后图已经是树（情形 A）
    return candidate2
```

**代码要点注释**（已在代码中用中文解释）  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历两遍 `edges`（每条边处理常数次），并查集的 `find/union` 近似 `O(α(n))`，α 为极慢增长的反 Ackermann 函数，几乎可以看作常数。  
  - 与暴力解的 `O(n²)` 相比，提升明显。  
- **空间复杂度**：`O(n)`  
  - 需要 `parent`、`UnionFind` 的 `parent` 与 `rank` 数组，均与节点数线性相关。  

---

## 心得  

- **核心技巧**：**并查集 + 处理「入度为 2」的特殊情况**。  
- **适用的题型**：  
  1. **Redundant Connection**（无向版）——只需要并查集检测环。  
  2. **Course Schedule II**（检测有向图是否有环）——可以用并查集或 DFS。  
  3. **树的重建/删除边** 系列题目，如「Delete Edge to Make Forest」等。  
- **一句话总结**：  
  > “先把『有两个父亲的孩子』挑出来，再用并查集快速找环，答案必在这两条或唯一环边中”。  

---

## 反思  

- **第一反应**：看到「多余的有向边」就想「把每条边删掉试试看」——这就是暴力思路。  
- **最容易踩的坑**：  
  - **入度为 2** 的节点会导致两条候选边，需要记住「返回出现最晚的那条」的规则。  
  - **并查集** 中必须**先跳过** `candidate2` 再判断环，否则会误判。  
  - 边界情况：如果根节点本身也被错误指向（形成环），但没有两父节点，这时直接返回产生环的那条边。  
- **下次遇到同类题**，第一步应该：  
  1. **统计每个节点的入度**，看是否出现「两个父亲」的情况；  
  2. **使用并查集**（或 DFS）在一次遍历中检测环。  

这样就能在 O(n) 时间内快速定位多余的边，避免暴力的 O(n²) 低效。