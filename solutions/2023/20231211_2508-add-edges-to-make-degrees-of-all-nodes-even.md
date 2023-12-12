# #2508. 给所有节点添加边使度数为偶数 / Add Edges to Make Degrees of All Nodes Even

> 难度：困难 · 标签：Hash Table、Graph · [LeetCode 链接](https://leetcode.com/problems/add-edges-to-make-degrees-of-all-nodes-even/)

---

## 题目（英文原版）

**Description**

There is an undirected graph consisting of n nodes numbered from 1 to n. You are given the integer n and a 2D array edges where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi. The graph can be disconnected.
You can add at most two additional edges (possibly none) to this graph so that there are no repeated edges and no self-loops.
Return true if it is possible to make the degree of each node in the graph even, otherwise return false.
The degree of a node is the number of edges connected to it.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[1,2],[2,3],[3,4],[4,2],[1,4],[2,5]]
Output: true
Explanation: The above diagram shows a valid way of adding an edge.
Every node in the resulting graph is connected to an even number of edges.
```

**Example 2:**

```
Input: n = 4, edges = [[1,2],[3,4]]
Output: true
Explanation: The above diagram shows a valid way of adding two edges.
```

**Example 3:**

```
Input: n = 4, edges = [[1,2],[1,3],[1,4]]
Output: false
Explanation: It is not possible to obtain a valid graph with adding at most 2 edges.
```

**Constraints**

- 3 <= n <= 105
- 2 <= edges.length <= 105
- edges[i].length == 2
- 1 <= ai, bi <= n
- ai != bi
- There are no repeated edges.

---

## 题目（中文翻译）

有一个 **无向图（undirected graph）**，包含编号为 `1` 到 `n` 的 `n` 个节点。给定整数 `n` 和二维数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条边。该图可能不连通。  

你可以向图中最多再添加两条边（也可以不添加），要求添加的边不能与已有的边重复，也不能是 **自环（self-loop）**。  

返回 `true` 表示可以使图中每个节点的 **度数（degree）**（即与该节点相连的边的数量）都是偶数；否则返回 `false`。  

---

**示例 1**  
**输入**: `n = 5, edges = [[1,2],[2,3],[3,4],[4,2],[1,4],[2,5]]`  
**输出**: `true`  
**解释**: 下图展示了一种合法的添加方式。  
结果图中每个节点的度数都是偶数。

**示例 2**  
**输入**: `n = 4, edges = [[1,2],[3,4]]`  
**输出**: `true`  
**解释**: 下图展示了添加两条边后的合法图。

**示例 3**  
**输入**: `n = 4, edges = [[1,2],[1,3],[1,4]]`  
**输出**: `false`  
**解释**: 最多再添加两条边也无法得到所有节点度数为偶数的合法图。

---

### 约束条件
- `3 <= n <= 10^5`
- `2 <= edges.length <= 10^5`
- `edges[i].length == 2`
- `1 <= a_i, b_i <= n`
- `a_i != b_i`
- 不存在 **重复边（repeated edges）**。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的新增边都穷举一遍**，看有没有一种方式能让每个点的度数（连了多少条边）都是偶数。  
- 首先统计原图每个节点的度数，记下哪些节点是奇数度。  
- 接下来枚举 **0 条、1 条或 2 条** 新增边的所有组合。  
- 对每一种组合，临时把这些边加进去，检查所有节点的度数是否全部为偶数。  

> **类比**：想象你手里有一张城市地图，城市之间已经有路（原有边）。你可以再建最多两条新路（新边），但不能在已经有路的两座城市之间再建第二条路，也不能把路建成环路（自环）。暴力解相当于把所有可能的两条新路的搭配都列出来，逐个试一遍，看看能不能把所有城市的出入口数量都变成偶数。

**为什么一定能得到正确答案？**  
因为我们把**所有合法的新增方案**都尝试了一遍，只要有一种方案满足条件，就一定会在遍历中被发现；如果遍历结束仍未找到，则说明根本不存在这样的方案。

#### 代码（Python）

```python
from itertools import combinations
from collections import defaultdict

def is_possible_bruteforce(n: int, edges):
    # 建立邻接集合，方便判断是否已有边
    adj = [set() for _ in range(n + 1)]
    degree = [0] * (n + 1)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        degree[u] += 1
        degree[v] += 1

    # 所有可能的新增边（不自环且不与已有边重复）
    possible_new_edges = [(i, j) for i in range(1, n + 1)
                          for j in range(i + 1, n + 1) if j not in adj[i]]

    # 0 条边的情况
    if all(d % 2 == 0 for d in degree[1:]):
        return True

    # 1 条边的情况
    for u, v in possible_new_edges:
        degree[u] += 1
        degree[v] += 1
        if all(d % 2 == 0 for d in degree[1:]):
            return True
        degree[u] -= 1   # 恢复原状
        degree[v] -= 1

    # 2 条边的情况（两两组合）
    for (u1, v1), (u2, v2) in combinations(possible_new_edges, 2):
        # 防止出现自环或重复边（两条边完全相同的情况已在 possible_new_edges 排除）
        if len({u1, v1, u2, v2}) < 4 and (u1, v1) != (u2, v2):
            # 这里可能出现两条边共享一个端点的情况，仍然合法
            pass
        # 加边
        degree[u1] += 1; degree[v1] += 1
        degree[u2] += 1; degree[v2] += 1
        if all(d % 2 == 0 for d in degree[1:]):
            return True
        # 恢复
        degree[u1] -= 1; degree[v1] -= 1
        degree[u2] -= 1; degree[v2] -= 1

    return False
```

> 关键行注释  
> - `adj[u].add(v)` / `adj[v].add(u)`: 用集合记录已有的邻居，后面判断“这条边已经存在吗？”时只需要 O(1) 时间。  
> - `possible_new_edges` 列举所有**合法**的新增边（不自环、不重复）。  
> - `all(d % 2 == 0 for d in degree[1:])` 检查每个节点的度数是否都是偶数。  

#### 复杂度  

- **时间复杂度**：  
  - 枚举所有可能的新增边数目为 `C = O(n²)`（因为最多要检查每一对节点）。  
  - 对每种组合（0、1、2 条）都要遍历度数组检查奇偶性，时间大约是 `O(C²)`，最坏情况是 `O(n⁴)`。  
  - 简单来说，暴力解的时间随 `n` 的平方甚至更快增长，**在 n=10⁵ 时根本不可用**。  
- **空间复杂度**：  
  - 只用了邻接集合和度数组，均为 `O(n + m)`，即线性空间。  

> **大白话**：`O(n²)` 可以想象成“把所有可能的两个人配对”。如果再把配对再配对（要加两条边），相当于“把配对的配对全部列出来”，这就像在 10⁵ 个人里找出所有 10¹⁰ 种组合，显然不可能在电脑里跑完。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**关键在于奇数度节点的数量**。  
- 每加一条新边，会让它的 **两个端点的度数都翻转奇偶性**（奇→偶，偶→奇）。  
- 因此，**只能通过改变奇数节点的数量** 来让所有度数变偶。  

下面一步步推导：

1. **奇数度节点的个数**  
   - 记为 `odd_cnt`。  
   - 每条新增边会把两个节点的奇偶性翻转，所以 `odd_cnt` 的变化是 **-2、0、+2**。  
   - 为了最终让所有节点度数为偶数，`odd_cnt` 必须能被 2 整除并最终变为 0。  
   - 因为我们最多只能加 **两条** 边，最多能把 `odd_cnt` 减少 4（每条边最多把两个奇数变偶）。  
   - 所以 **合法的初始 odd_cnt 只能是 0、2、4**。其他情况（如 6、8 …）根本不可能在两条边内全部消除。

2. **分别讨论这三种可能**  

   - **odd_cnt = 0**  
     已经全部偶数，直接返回 `True`。

   - **odd_cnt = 2**（记为 `a`、`b`）  
     - **方案 1**：直接在 `a` 与 `b` 之间加一条边。如果这条边 **不存在**（没有重复边），只需要一条边即可，返回 `True`。  
     - **方案 2**：如果 `a` 与 `b` 已经相连（不能再加），我们可以 **各加一条边**，把 `a`、`b` 分别连到同一个第三个节点 `c`（`c ≠ a,b`），这样两条新边都把奇数度变偶数。条件是：`(a,c)` 与 `(b,c)` 都**不存在**。只要在图中找得到这样一个 `c`，返回 `True`。  
     - 若上述两种方式都找不到合法的 `c`，则返回 `False`。

   - **odd_cnt = 4**（记为 `a,b,c,d`）  
     我们只能加两条边，必须把这四个奇数节点两两配对。  
     - 列举所有 **3 种配对方式**（从 4 个点中挑出两两组合）：  
       1. `(a,b)` 与 `(c,d)`  
       2. `(a,c)` 与 `(b,d)`  
       3. `(a,d)` 与 `(b,c)`  
     - 对每一种配对，检查这两条边是否**都不存在**于原图。只要有一种配对满足条件，就可以在两条新边后让所有节点度数为偶数，返回 `True`。  
     - 若三种配对全部被原有边占用，则返回 `False`。

3. **实现细节**  

   - 为了快速判断两点之间是否已有边，使用 **哈希集合**（Python 中的 `set`），相当于“字典里查词”。  
   - 建图时记录每个节点的度数，顺手得到 `odd_nodes` 列表。  
   - 查找第三个节点 `c`（odd_cnt=2 情况）时，只需遍历 `1…n`，跳过 `a`、`b`，并用集合判断 `(a,c)`、`(b,c)` 是否已存在，最坏 O(n)（一次遍历即可）。  

> **类比**：  
> - **哈希表**就像一本 **电话簿**，你只要知道名字（节点编号），就能在 **常数时间**（几乎立刻）找到对应的电话号码（是否有边）。  
> - **配对**可以想象成把四个人两两牵手，只要没有人已经手牵手（已经有边），就可以再让他们手牵手一次（加新边）。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def isPossible(n: int, edges: List[List[int]]) -> bool:
    # 1. 建图 + 统计度数
    adj = [set() for _ in range(n + 1)]   # 1-indexed
    degree = [0] * (n + 1)

    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        degree[u] += 1
        degree[v] += 1

    # 2. 找出奇数度的节点
    odd = [i for i in range(1, n + 1) if degree[i] % 2 == 1]
    odd_cnt = len(odd)

    # 只能是 0、2、4
    if odd_cnt not in (0, 2, 4):
        return False

    # 3. 情况划分
    if odd_cnt == 0:
        # 已经全部偶数
        return True

    if odd_cnt == 2:
        a, b = odd[0], odd[1]
        # 方案 1：直接连 a、b（若不存在此边）
        if b not in adj[a]:
            return True

        # 方案 2：找第三个节点 c，使 (a,c) 与 (b,c) 都不存在
        for c in range(1, n + 1):
            if c == a or c == b:
                continue
            if (c not in adj[a]) and (c not in adj[b]):
                # 两条新边分别是 (a,c) 与 (b,c)
                return True
        return False

    # odd_cnt == 4
    a, b, c, d = odd  # 取出四个奇数节点

    # 辅助函数：判断两条边是否都不存在
    def both_missing(x1, y1, x2, y2):
        return (y1 not in adj[x1]) and (y2 not in adj[x2])

    # 配对 1： (a,b) 与 (c,d)
    if both_missing(a, b, c, d):
        return True
    # 配对 2： (a,c) 与 (b,d)
    if both_missing(a, c, b, d):
        return True
    # 配对 3： (a,d) 与 (b,c)
    if both_missing(a, d, b, c):
        return True

    return False
```

> 代码要点注释  
> - `adj = [set() for _ in range(n + 1)]`：每个节点的邻居集合，用哈希实现 O(1) 查找。  
> - `odd = [i for i in range(1, n + 1) if degree[i] % 2 == 1]`：收集奇数度节点。  
> - `both_missing`：一次性检查两条潜在新边是否都不在原图中，避免重复代码。  

#### 复杂度  

- **时间复杂度**：  
  - 建图 + 统计度数：`O(n + m)`（`m = len(edges)`）。  
  - `odd_cnt = 2` 时，遍历寻找第三个节点最多 `O(n)`。  
  - `odd_cnt = 4` 时，只检查 3 种配对，都是 O(1)。  
  - 综合来看 **总时间是 O(n + m)**，即线性时间，能够轻松处理 `n, m ≤ 10⁵` 的规模。  

- **空间复杂度**：  
  - 邻接集合占 `O(n + m)`，度数组占 `O(n)`，整体 **O(n + m)**。  

> **对比**：暴力解需要遍历所有可能的两条新边，时间指数级增长；最优解只关注 **奇数度节点**，一步到位，时间只和图的规模线性相关。

---

## 心得  

- **核心技巧**：利用“每条新增边会翻转其两个端点的奇偶性”这一性质，把问题转化为 **奇数度节点的配对**。  
- **适用的题型**：  
  1. “让所有节点度数为偶数”类问题（如 `Even Degrees`、`Make Graph Eulerian`）。  
  2. “在有限步数内使图满足某种奇偶约束”类（如 `Maximum Number of Edges to Add to Make All Degrees Even`、`Check if Adding One Edge Can Make Graph Bipartite`）。  
- **一句话总结**：**只要看奇数度节点的数量与配对可行性，答案立刻可得。**

---

## 反思  

- **第一反应**：看到“最多加两条边”，自然想到**枚举所有可能**，于是想到暴力搜索。  
- **最容易踩的坑**：  
  - 忘记**不能重复边**或**自环**的限制，导致错误的配对判断。  
  - 在 `odd_cnt = 2` 时，只检查直接相连的情况，忽视了“各连同一个第三点”这种两条边的方案。  
  - 对于 `odd_cnt = 4`，配对方式不止一种，需要全部尝试，否则会误判。  
- **下次类似题**，第一步应该先**统计奇数度节点**，并根据**可添加的边数上限**判断**奇数度节点的可能范围**，再针对具体数量进行配对或寻找第三节点的检查。这样思路更清晰、实现更简洁。