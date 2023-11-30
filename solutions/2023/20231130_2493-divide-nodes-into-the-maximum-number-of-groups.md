# #2493. **将节点划分为最多组数** / Divide Nodes Into the Maximum Number of Groups

> 难度：困难 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/divide-nodes-into-the-maximum-number-of-groups/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n representing the number of nodes in an undirected graph. The nodes are labeled from 1 to n.
You are also given a 2D integer array edges, where edges[i] = [ai, bi] indicates that there is a bidirectional edge between nodes ai and bi. Notice that the given graph may be disconnected.
Divide the nodes of the graph into m groups (1-indexed) such that:
Return the maximum number of groups (i.e., maximum m) into which you can divide the nodes. Return -1 if it is impossible to group the nodes with the given conditions.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[1,2],[1,4],[1,5],[2,6],[2,3],[4,6]]
Output: 4
Explanation: As shown in the image we:
- Add node 5 to the first group.
- Add node 1 to the second group.
- Add nodes 2 and 4 to the third group.
- Add nodes 3 and 6 to the fourth group.
We can see that every edge is satisfied.
It can be shown that that if we create a fifth group and move any node from the third or fourth group to it, at least on of the edges will not be satisfied.
```

**Example 2:**

```
Input: n = 3, edges = [[1,2],[2,3],[3,1]]
Output: -1
Explanation: If we add node 1 to the first group, node 2 to the second group, and node 3 to the third group to satisfy the first two edges, we can see that the third edge will not be satisfied.
It can be shown that no grouping is possible.
```

**Constraints**

- 1 <= n <= 500
- 1 <= edges.length <= 104
- edges[i].length == 2
- 1 <= ai, bi <= n
- ai != bi
- There is at most one edge between any pair of vertices.

---

## 题目（中文翻译）

给定一个正整数 `n`，表示无向图（undirected graph）中的节点数量，节点编号为 `1` 到 `n`。  
同时给定一个二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条双向边（bidirectional edge）。注意，给定的图可能是非连通的。

请将图中的所有节点划分到 `m` 个组（组编号从 **1** 开始），使得满足题目要求的条件后，`m` 取最大值。  
如果不存在任何满足条件的划分方式，返回 `-1`。

---

### 示例

**示例 1**  
```
Input: n = 6, edges = [[1,2],[1,4],[1,5],[2,6],[2,3],[4,6]]
Output: 4
Explanation: 如图所示，我们可以：
- 将节点 5 放入第 1 组；
- 将节点 1 放入第 2 组；
- 将节点 2 与节点 4 放入第 3 组；
- 将节点 3 与节点 6 放入第 4 组。

可以看到每条边都满足题目要求。  
可以证明，如果再创建第 5 组并把第 3 组或第 4 组中的任意节点移动到第 5 组，都会导致至少一条边不满足条件。（后文省略） 
```

**示例 2**  
```
Input: n = 3, edges = [[1,2],[2,3],[3,1]]
Output: -1
Explanation: 若把节点 1 放入第 1 组、节点 2 放入第 2 组、节点 3 放入第 3 组，则前两条边都满足，但第三条边不满足。  
可以证明不存在任何合法的分组方式。
```

---

### 约束条件

- `1 <= n <= 500`
- `1 <= edges.length <= 10^4`
- `edges[i].length == 2`
- `1 <= a_i, b_i <= n`
- `a_i != b_i`
- 任意一对节点之间至多存在一条边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把题目先想成“给每个节点安排一个整数编号（组号），要求**任意相连的两个节点的组号相差恰好是 1**”。  
如果把组号看成楼层，边就像楼梯，只能上下相邻一层。

最直接的办法是 **枚举所有可能的分配**，检查每一种分配是否满足条件，然后取组数最多的那一种。  
- 数据结构：我们可以把图用**邻接表**存起来，类似于一本“朋友簿”，`adj[u]` 里记录所有和 `u` 直接相连的朋友。  
- 检查合法性：遍历所有边 `(u,v)`，如果 `|group[u] - group[v]| != 1` 就说明这套分配不行。  
- 统计组数：只要找到合法的分配，组数就是 `max(group) - min(group) + 1`（因为组号是连续的）。

这套办法一定能得到答案，因为我们把**所有可能**都穷举了。

> **为什么一定对？**  
> 只要存在一种合法的分配，我们的枚举一定会遍历到它；若所有枚举都不合法，则说明根本不存在满足题意的分配。

**时间/空间复杂度**  
- 枚举所有可能的组号相当于给 `n` 个节点每个都尝试 `n` 种取值，时间是 `O(n^n)`，指数级别，根本不可行。  
- 空间上只需要存图和一份 `group` 数组，`O(n + m)`（`m` 为边数），这点没问题。

> **大白话解释**：  
> 想象你要把 10 个人排成 10 排，每个人可以随意站在任意一排。你把所有 10ⁱ⁰ 种站法都列出来检查，显然根本不可能在电脑里完成。

#### 代码（Python）

```python
# 只演示暴力思路的框架，实际运行会超时
def max_groups_bruteforce(n, edges):
    from itertools import product

    # 建图（邻接表）
    adj = [[] for _ in range(n)]
    for a, b in edges:
        a -= 1; b -= 1          # 0-index
        adj[a].append(b)
        adj[b].append(a)

    best = 0
    # 每个节点的组号从 0 到 n-1（足够大）
    for groups in product(range(n), repeat=n):
        ok = True
        for u in range(n):
            for v in adj[u]:
                if abs(groups[u] - groups[v]) != 1:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            cur = max(groups) - min(groups) + 1
            best = max(best, cur)

    return best if best > 0 else -1
```

#### 复杂度

- **时间复杂度**：`O(n^n)` —— 组合数爆炸，实际不可接受。  
- **空间复杂度**：`O(n + m)` —— 只存图和临时数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键在于如何快速判断是否存在一种合法的编号方式**，以及在存在时**求出最大的组数**。  
观察题目和提示：

1. **若图不是二分图（bipartite）就不可能**。  
   因为如果存在奇环（长度为奇数的闭合路径），必然会出现两相邻节点在同一“颜色”上，导致它们的组号差不可能恰好是 1。  

2. **每个连通块可以单独处理**，因为不同块之间没有边相连，组号互不影响，最终答案是各块答案的**和**。  

3. 对于 **一个连通块**，如果我们把某个节点 `v` 固定在最左侧（组号 1），则  
   - 其它所有节点的组号只能是 `v` 到它们的最短路径长度（即 BFS 深度）。  
   - 只要每条边的两端深度相差恰好是 1，整个块的编号就是合法的。  

   换句话说：**只要把块当作一棵 BFS 树，以某个根 `v` 为起点，所有边都必须跨越相邻层**。  

4. **如何得到最大可能的组数**？  
   - 对块中的每一个节点尝试一次“根”，做一次 BFS，得到每个节点的层次 `dist`。  
   - 检查所有边：如果 `|dist[u] - dist[v]| != 1`，说明以这个根不行。  
   - 若所有边都满足，合法的组数就是 `max(dist) + 1`（因为层次从 0 开始）。  
   - 在该块的所有根中取最大合法组数，即为该块的最优答案。  

5. **复杂度分析**  
   - 块大小最多 `n ≤ 500`，对每个块我们最多枚举 `size` 次根，每次 BFS `O(size + edges_in_block)`，总计 `O(n * (n + m))`，在限制下完全可接受。  

下面把上述思路逐步实现。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def maximumGroups(n: int, edges: List[List[int]]) -> int:
    # 1. 建图（邻接表），并记录每条边供后面检查
    adj = [[] for _ in range(n)]
    for a, b in edges:
        a -= 1; b -= 1          # 统一转成 0-index
        adj[a].append(b)
        adj[b].append(a)

    visited = [False] * n
    total_groups = 0          # 最终答案：各连通块的组数之和

    # 2. 遍历每个连通块
    for start in range(n):
        if visited[start]:
            continue

        # ---- 收集当前块的所有节点 ----
        comp_nodes = []
        q = deque([start])
        visited[start] = True
        while q:
            u = q.popleft()
            comp_nodes.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

        # ---- 对当前块尝试每一个节点作为“左端点” ----
        best_in_comp = 0      # 记录该块的最大合法组数
        for root in comp_nodes:
            # BFS 计算层次（距离）
            dist = [-1] * n
            dist[root] = 0
            bfs = deque([root])
            while bfs:
                u = bfs.popleft()
                for v in adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        bfs.append(v)

            # 检查所有边是否只跨相邻层
            ok = True
            for u in comp_nodes:
                for v in adj[u]:
                    if u < v:               # 只检查一次
                        if abs(dist[u] - dist[v]) != 1:
                            ok = False
                            break
                if not ok:
                    break

            if ok:
                # 合法 -> 组数 = 最大层数 + 1（因为层次从 0 开始）
                groups_here = max(dist[u] for u in comp_nodes) + 1
                best_in_comp = max(best_in_comp, groups_here)

        # 如果没有任何合法的根，说明该块根本无法分组 → 整体返回 -1
        if best_in_comp == 0:          # 说明块里有边但没有合法划分
            return -1

        total_groups += best_in_comp

    return total_groups
```

**代码要点解释（中文注释已在代码中）**：

- `adj`：邻接表，类似于“每个人的好友列表”。  
- `visited`：标记哪些节点已经被放进当前块，防止重复遍历。  
- 对每个块的 `root` 做 BFS，`dist` 即为“从左边第一组出发，走了几步”。  
- `abs(dist[u] - dist[v]) != 1`：如果出现差距不是 1，说明这条边跨了两层或更多层，违背题目要求。  
- `best_in_comp` 记录该块能得到的最大组数；若遍历完所有根仍为 0，说明块内部的结构本身不满足条件（例如出现跨层边），直接返回 `-1`。  
- 最后把每块的最佳组数相加，就是题目要求的最大总组数。

#### 复杂度

- **时间复杂度**：`O(n * (n + m))`  
  - 外层遍历每个节点一次得到连通块。  
  - 对每个块的每个节点都做一次 BFS（`O(size + edges_in_block)`），最坏情况下 `size ≈ n`，`edges_in_block ≤ m`。  
  - 对 `n ≤ 500`、`m ≤ 10⁴` 完全足够。  

  > 与暴力解的指数级别相比，这里只需要几千次循环，跑得飞快。

- **空间复杂度**：`O(n + m)`  
  - `adj`、`visited`、`dist` 等数组共占线性空间。  

  > 只用了几百个整数，内存几乎可以忽略不计。

---

## 心得

- **核心技巧**：把“相邻组号差为 1”转化为 **层次（BFS 距离）** 的约束，只要每条边跨越相邻层即合法。  
- **适用场景**：  
  1. **层次约束图**（如题目要求相邻节点层数相差固定值）。  
  2. **检测图是否可以嵌入一条直线且边只跨相邻点**（类似 “是否是路径图的超图”）。  
  3. **求图的最大直径**，但需额外检查“跨层边”是否存在。  
- **一句话总结解题钥匙**：**把每条边的“相差 1”转化为“只能跨相邻 BFS 层”，遍历所有可能的根找最大层数**。

---

## 反思

- **第一反应**：看到“相邻组号差 1”立刻想到 **BFS 层次**，但一开始忽略了“跨层边”会导致不合法。  
- **最容易踩的坑**：  
  - 忽视图可能是 **不连通** 的，需要对每个连通块单独求解并累加。  
  - 只检查**奇偶性**（二分图）不足以保证合法，因为仍可能出现跨两层的边（如 1‑2‑3‑4 与额外的 1‑4 边）。  
  - 边的检查要避免重复计数（`u < v`），否则会误判。  
- **下次类似题目**：第一步先 **判断二分性**（奇环会直接否），第二步 **尝试以每个节点为根做 BFS**，检查是否所有边只跨相邻层，最后取最大层数。这样思路更系统、不会遗漏特殊结构。