# #3373. **连接两棵树后目标节点数量的最大化 II** / Maximize the Number of Target Nodes After Connecting Trees II

> 难度：困难 · 标签：Tree、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximize-the-number-of-target-nodes-after-connecting-trees-ii/)

---

## 题目（英文原版）

**Description**

There exist two undirected trees with n and m nodes, labeled from [0, n - 1] and [0, m - 1], respectively.
You are given two 2D integer arrays edges1 and edges2 of lengths n - 1 and m - 1, respectively, where edges1[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the first tree and edges2[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the second tree.
Node u is target to node v if the number of edges on the path from u to v is even. Note that a node is always target to itself.
Return an array of n integers answer, where answer[i] is the maximum possible number of nodes that are target to node i of the first tree if you had to connect one node from the first tree to another node in the second tree.
Note that queries are independent from each other. That is, for every query you will remove the added edge before proceeding to the next query.

**Examples**

**Example 1:**

```
Input: edges1 = [[0,1],[0,2],[2,3],[2,4]], edges2 = [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]]
Output: [8,7,7,8,8]
Explanation:
```

**Example 2:**

```
Input: edges1 = [[0,1],[0,2],[0,3],[0,4]], edges2 = [[0,1],[1,2],[2,3]]
Output: [3,6,6,6,6]
Explanation:
For every i , connect node i of the first tree with any node of the second tree.
```

**Constraints**

- 2 <= n, m <= 105
- edges1.length == n - 1
- edges2.length == m - 1
- edges1[i].length == edges2[i].length == 2
- edges1[i] = [ai, bi]
- 0 <= ai, bi < n
- edges2[i] = [ui, vi]
- 0 <= ui, vi < m
- The input is generated such that edges1 and edges2 represent valid trees.

---

## 题目（中文翻译）

存在两棵无向树，分别有 `n` 与 `m` 个节点，节点编号为 `[0, n‑1]` 和 `[0, m‑1]`。  
给定两个二维整数数组 `edges1` 与 `edges2`，长度分别为 `n‑1` 与 `m‑1`，其中 `edges1[i] = [a_i, b_i]` 表示第一棵树中存在一条连接节点 `a_i` 与 `b_i` 的边，`edges2[i] = [u_i, v_i]` 表示第二棵树中存在一条连接节点 `u_i` 与 `v_i` 的边。

**目标（target）**：若从节点 `u` 到节点 `v` 的路径上的边数为偶数，则称节点 `u` 是节点 `v` 的目标（target）。注意，一个节点始终是它自己的目标（target）。

返回一个长度为 `n` 的整数数组 `answer`，其中 `answer[i]` 表示在 **必须** 将第一棵树的某个节点与第二棵树的某个节点相连的前提下，能够使第一棵树中节点 `i` 的目标（target）节点数量达到的最大可能值。  

每一次的连接视为一次独立的查询，查询之间互不影响——即在处理下一次查询之前，需要先移除本次添加的边。

---

### 示例

**示例 1**

```text
Input: edges1 = [[0,1],[0,2],[2,3],[2,4]],
       edges2 = [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]]
Output: [8,7,7,8,8]
Explanation:
对每个 i，将第一棵树的节点 i 与第二棵树中的任意节点相连后，计算节点 i 的目标（target）节点数量的最大值。
```

**示例 2**

```text
Input: edges1 = [[0,1],[0,2],[0,3],[0,4]],
       edges2 = [[0,1],[1,2],[2,3]]
Output: [3,6,6,6,6]
Explanation:
对每个 i，将第一棵树的节点 i 与第二棵树的任意节点相连后，得到的最大目标（target）节点数量如上所示。
```

---

### 约束条件

- `2 ≤ n, m ≤ 10^5`
- `edges1.length == n - 1`
- `edges2.length == m - 1`
- `edges1[i].length == edges2[i].length == 2`
- `edges1[i] = [a_i, b_i]`，`0 ≤ a_i, b_i < n`
- `edges2[i] = [u_i, v_i]`，`0 ≤ u_i, v_i < m`
- 输入保证 `edges1` 与 `edges2` 分别构成合法的树。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举** 所有可能的连接方式，然后把两棵树合并成一棵大树，逐个节点去统计有多少目标节点。  

- **枚举连接**：把第一棵树的每个节点 `i` 与第二棵树的每个节点 `j` 连接一次，形成一条新边 `(i, j)`。  
- **统计目标节点**：对合并后的图，任选一个查询节点 `i`，对所有其它节点做一次 **BFS/DFS**，记录从 `i` 到该节点的边数。如果边数是偶数，就算它是目标节点。  
- **取最大值**：对同一个 `i`，遍历所有可能的 `j`，挑出能够得到最多目标节点的那一次，记下来。

> **生活化类比**：把两棵树想成两本词典，词典里的每个单词就是一个节点，词典之间的连线就是我们要“借”来的一本新词典的页码。暴力解相当于把每本词典的每一页都和另一册的每一页配对，然后逐页检查是否满足“偶数页差”。显然，这样的工作量会非常大。

**为什么正确**：因为我们把所有合法的连接都尝试了一遍，必然会找到最优的那一次。

#### 代码（Python）

```python
from collections import deque
from typing import List

def brute_force(edges1: List[List[int]], edges2: List[List[int]]) -> List[int]:
    # 建图
    def build(edges, n):
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        return g

    n = len(edges1) + 1
    m = len(edges2) + 1
    g1 = build(edges1, n)
    g2 = build(edges2, m)

    # 合并两棵树的函数（不改变原图）
    def merge(i, j):
        g = [lst[:] for lst in g1] + [lst[:] for lst in g2]   # 复制两张图
        g.append([])                                          # 为新节点留位（可选）
        # 把第二棵树的编号全部平移 n，让它们不冲突
        for u in range(m):
            for v in g2[u]:
                g[u + n].append(v + n)
        # 添加新边 (i, j+n)
        g[i].append(j + n)
        g[j + n].append(i)
        return g

    # 计算从 start 出发的偶数距离节点个数
    def count_even(g, start):
        N = len(g)
        dist = [-1] * N
        q = deque([start])
        dist[start] = 0
        cnt = 0
        while q:
            u = q.popleft()
            if dist[u] % 2 == 0:          # 偶数距离
                cnt += 1
            for v in g[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return cnt

    ans = [0] * n
    # 对每个 i 枚举所有 j
    for i in range(n):
        best = 0
        for j in range(m):
            g = merge(i, j)               # 合并后得到的大图
            best = max(best, count_even(g, i))
        ans[i] = best
    return ans
```

> **代码说明**  
> - 第 9‑15 行把两棵树的邻接表复制出来，防止在后面的循环里被改动。  
> - 第 24‑31 行是 **BFS**，用 `dist` 记录从起点 `start` 到每个节点的边数，`dist[u] % 2 == 0` 表示距离为偶数，计数。  
> - 第 38‑44 行枚举所有可能的连接 `(i, j)`，取最大值即为答案。

#### 复杂度  

- **时间复杂度**：  
  - 枚举所有连接需要 `O(n·m)` 次。  
  - 每次枚举后都要对整棵合并后的树做一次 BFS，时间是 `O(n+m)`。  
  - 综合下来是 `O(n·m·(n+m))`，在最坏情况下相当于 **立方级**（比如 `n=m=10⁵` 时根本跑不完）。  
  - 大白话：想象有 10 万本书，每本书要和另外 10 万本书的每一页配对，还要把配对完的全部页数再数一遍，显然不可行。

- **空间复杂度**：  
  - 需要存两棵树的邻接表以及合并后的临时图，最多 `O(n+m)`。  
  - 还有 BFS 用的 `dist` 数组，同样是 `O(n+m)`。  

> 暴力解只能用来验证思路或在极小数据上调试，正式提交必然超时。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **两棵树之间唯一的交互** 只出现在我们新加的那条边 `(i, j)`。  
所以我们要找的其实是 **“在这条边两端的距离奇偶性如何决定目标节点数”**，而不必真的把两棵树合并后遍历。

---

#### 2.1 关键观察：距离的奇偶性等价于深度的异同  

任选一棵树，随便选一个根（比如节点 `0`），用 **DFS/BFS** 计算每个节点的深度 `dep[u]`（根的深度为 `0`，相邻节点深度相差 `1`）。  

在树里，**两点之间的路径长度的奇偶性** 正好等于它们深度奇偶性的 **异或**（`dep[u] % 2  XOR  dep[v] % 2`）。  
- 同奇同偶 → 路径长度为 **偶数**。  
- 奇偶不同 → 路径长度为 **奇数**。

> **类比**：把深度的奇偶性想成“黑白棋子”。两颗同色的棋子之间的距离是偶数，两颗异色的距离是奇数。

因此，对于第一棵树的任意节点 `i`：

- 与 `i` **偶数距离** 的节点正好是 **深度奇偶性和 `i` 相同** 的所有节点。  
- 与 `i` **奇数距离** 的节点正好是深度奇偶性和 `i` 不同的节点。

只要我们知道整棵树里 **深度为偶数的节点有多少**，以及 **深度为奇数的节点有多少**，就能在 **O(1)** 时间算出每个 `i` 的偶数目标数量 `even1[i]`。

同理，对第二棵树的每个节点 `j`，我们可以得到它的 **奇数距离节点数** `odd2[j]`（因为后面需要奇数距离的节点）。

---

#### 2.2 目标节点数的公式推导  

把两棵树通过新边 `(i, j)` 连接后，考虑两类目标节点：

1. **仍然在第一棵树内部**  
   - 距离只经过第一棵树的边，奇偶性不受第二棵树的影响。  
   - 目标节点数 = `even1[i]`（即深度和 `i` 同色的节点数）。

2. **跨到第二棵树的节点**  
   - 路径长度 = `dist(i, i) (=0)` + **新边** `1` + `dist(j, y)`（`y` 为第二棵树中的某节点）。  
   - 为了让总长度为偶数，必须满足 `1 + dist(j, y)` 为奇数 → `dist(j, y)` 必须是 **奇数**。  
   - 因此，跨树的目标节点数恰好等于 **从 `j` 出发的奇数距离节点数**，记作 `odd2[j]`。

于是，针对固定的 `i`，我们可以任选 `j`，得到的目标总数是  

```
answer[i] = even1[i] + odd2[j]          (j 为我们选择连接的第二棵树节点)
```

我们想要 **最大** 的目标数，只需让 `odd2[j]` 取到 **第二棵树中最大的奇数距离节点数**。设  

```
maxOdd2 = max_{j in tree2} odd2[j]
```

则最终答案只和 `i` 本身有关：

```
answer[i] = even1[i] + maxOdd2
```

> 这就是提示里给出的公式的完整推导。

---

#### 2.3 如何快速得到 `even1[i]` 与 `odd2[j]`  

1. **一次遍历得到深度奇偶计数**  
   - 对树 1：DFS/BFS 计算 `dep1[u]`，统计 `cntEven1`（深度为偶数的节点数）和 `cntOdd1`。  
   - 对树 2：同理得到 `dep2[v]`、`cntEven2`、`cntOdd2`。

2. **根据节点的深度奇偶性直接算出对应的目标数**  
   - 对树 1 中的节点 `u`：  
     - 若 `dep1[u]` 为偶数 → `even1[u] = cntEven1`（同色节点）  
     - 否则 → `even1[u] = cntOdd1`  
   - 对树 2 中的节点 `v`：  
     - 若 `dep2[v]` 为偶数 → `odd2[v] = cntOdd2`（异色节点）  
     - 否则 → `odd2[v] = cntEven2`

3. **求出 `maxOdd2`**  
   - 只需遍历一次 `odd2` 数组取最大即可。

所有步骤都是 **线性时间**（`O(n+m)`）和 **线性空间**（存邻接表、深度数组）。

---

#### 代码（Python）

```python
from collections import deque
from typing import List

def max_target_nodes(edges1: List[List[int]], edges2: List[List[int]]) -> List[int]:
    """
    返回 answer，其中 answer[i] = (在第一棵树中与 i 偶数距离的节点数)
                                 + (第二棵树中奇数距离节点数的最大值)
    """
    # ---------- 1. 构造邻接表 ----------
    def build_adj(edges, sz):
        g = [[] for _ in range(sz)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        return g

    n = len(edges1) + 1
    m = len(edges2) + 1
    g1 = build_adj(edges1, n)
    g2 = build_adj(edges2, m)

    # ---------- 2. BFS 求深度 ----------
    def bfs_depth(g, sz):
        depth = [-1] * sz
        q = deque([0])          # 任意选 0 为根
        depth[0] = 0
        while q:
            u = q.popleft()
            for v in g[u]:
                if depth[v] == -1:
                    depth[v] = depth[u] + 1
                    q.append(v)
        return depth

    dep1 = bfs_depth(g1, n)
    dep2 = bfs_depth(g2, m)

    # ---------- 3. 统计奇偶节点数 ----------
    cntEven1 = sum(1 for d in dep1 if d % 2 == 0)
    cntOdd1  = n - cntEven1

    cntEven2 = sum(1 for d in dep2 if d % 2 == 0)
    cntOdd2  = m - cntEven2

    # ---------- 4. 计算 each node 的 even / odd 数 ----------
    # 第一棵树：even1[i] = 同色节点数
    even1 = [cntEven1 if d % 2 == 0 else cntOdd1 for d in dep1]

    # 第二棵树：odd2[j] = 异色节点数
    odd2 = [cntOdd2 if d % 2 == 0 else cntEven2 for d in dep2]

    # ---------- 5. 取第二棵树 odd2 的最大值 ----------
    maxOdd2 = max(odd2)

    # ---------- 6. 组合得到答案 ----------
    answer = [e + maxOdd2 for e in even1]
    return answer
```

> **代码要点**  
> - 第 11‑16 行把每棵树的边转成邻接表，后面遍历更方便。  
> - 第 22‑32 行是 **BFS**，一次遍历即可得到每个节点到根的距离（深度）。  
> - 第 35‑42 行统计深度为偶数/奇数的节点总数。  
> - 第 45‑48 行利用 “同色 → 偶数距离，异色 → 奇数距离” 的性质直接得到 `even1` 与 `odd2`。  
> - 第 51 行取 `odd2` 的最大值 `maxOdd2`，这一步对所有 `i` 是相同的。  
> - 第 54 行把两部分相加得到最终答案。

---

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 两次 BFS 各遍历一次对应树的所有节点和边。  
  - 其余的遍历（统计、取最大、生成答案）也是线性。  
  - 与暴力解的 `O(n·m·(n+m))` 相比，简直是 **从立方降到线性**，即使 `n,m` 达到 `10⁵` 也能轻松跑完。

- **空间复杂度**：`O(n + m)`  
  - 需要存两棵树的邻接表、深度数组以及若干计数变量。  
  - 没有额外的递归栈或临时大图，完全符合题目对 10⁵ 规模的内存要求。

> 大白话：我们只需要走两遍森林（每棵树一次），不需要把两棵树拼在一起再走遍，时间和空间都大幅缩减。

---

## 心得  

- **核心技巧**：**奇偶深度转化**——在树里，两点间路径长度的奇偶性等价于它们深度奇偶性的相等/不等。利用这一点可以把“距离是偶数”直接转化为“颜色相同”，从而只需统计全局的奇偶节点数量。  
- **适用场景**  
  1. **树上奇偶距离统计**（如 “判断两点距离是否为奇数/偶数”）。  
  2. **树的染色问题**（把树二分成黑白两色，求同色或异色节点对数）。  
  3. **跨树连接后奇偶路径问题**（本题的变体：连两棵树后求某类路径数量）。  
- **一句话总结解题钥匙**：  
  > “在树里，距离的奇偶性只看节点深度的奇偶性”。只要把深度奇偶性记下来，所有奇偶距离统计都可以 **O(1)** 完成。

---

## 反思  

- **第一反应**：看到“连接两棵树后统计偶数距离”，自然想到 **暴力枚举**，但很快意识到 `n,m ≤ 10⁵`，枚举必超时。  
- **最容易踩的坑**  
  - 忘记 **节点自身** 也算目标（距离 `0` 为偶数），导致 `even1[i]` 少算 1。  
  - 在求 `odd2[j]` 时写反了，使用了同色节点数而不是异色节点数。  
  - BFS/DFS 递归深度过大，建议使用显式栈或 `deque`（如本解法）避免递归栈溢出。  
- **下次遇到同类题**，第一步应该：  
  1. 把 **“路径长度的奇偶性”** 转化为 **“深度奇偶性”**。  
  2. 统计全局的奇偶节点数量，看看是否能直接用 **全局计数** 替代 **逐点遍历**。  

这样往往能把原本的 **指数/立方** 复杂度瞬间压到 **线性**。祝学习愉快！