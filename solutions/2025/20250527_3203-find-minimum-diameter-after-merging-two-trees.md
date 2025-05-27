# #3203. 合并两棵树后最小直径 / Find Minimum Diameter After Merging Two Trees

> 难度：困难 · 标签：Tree、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/find-minimum-diameter-after-merging-two-trees/)

---

## 题目（英文原版）

**Description**

There exist two undirected trees with n and m nodes, numbered from 0 to n - 1 and from 0 to m - 1, respectively. You are given two 2D integer arrays edges1 and edges2 of lengths n - 1 and m - 1, respectively, where edges1[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the first tree and edges2[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the second tree.
You must connect one node from the first tree with another node from the second tree with an edge.
Return the minimum possible diameter of the resulting tree.
The diameter of a tree is the length of the longest path between any two nodes in the tree.

**Examples**

**Example 1:**

```
Input: edges1 = [[0,1],[0,2],[0,3]], edges2 = [[0,1]]
Output: 3
Explanation:
We can obtain a tree of diameter 3 by connecting node 0 from the first tree with any node from the second tree.
```

**Example 2:**

```
Input: edges1 = [[0,1],[0,2],[0,3],[2,4],[2,5],[3,6],[2,7]], edges2 = [[0,1],[0,2],[0,3],[2,4],[2,5],[3,6],[2,7]]
Output: 5
Explanation:
We can obtain a tree of diameter 5 by connecting node 0 from the first tree with node 0 from the second tree.
```

**Constraints**

- 1 <= n, m <= 105
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

存在两棵无向树（undirected tree），第一棵有 `n` 个节点（node），编号为 `0` 到 `n-1`，第二棵有 `m` 个节点，编号为 `0` 到 `m-1`。  
给定两个二维整数数组 `edges1` 和 `edges2`，长度分别为 `n-1` 和 `m-1`，其中 `edges1[i] = [a_i, b_i]` 表示在第一棵树中节点 `a_i` 与节点 `b_i` 之间存在一条边（edge），`edges2[i] = [u_i, v_i]` 表示在第二棵树中节点 `u_i` 与节点 `v_i` 之间存在一条边。  

你需要在第一棵树的某个节点与第二棵树的某个节点之间添加一条边，使两棵树合并为一棵树。  
返回合并后得到的树的 **最小可能直径**（minimum possible diameter）。  

树的直径（diameter）定义为树中任意两个节点之间最长路径（longest path）的长度。

**Example 1:**  
**Example 2:**  
**Constraints:**  

- `1 <= n, m <= 10^5`  
- `edges1.length == n - 1`  
- `edges2.length == m - 1`  
- `edges1[i].length == edges2[i].length == 2`  
- `edges1[i] = [a_i, b_i]`，`0 <= a_i, b_i < n`  
- `edges2[i] = [u_i, v_i]`，`0 <= u_i, v_i < m`  
- 输入保证 `edges1` 与 `edges2` 均构成合法的树。

---

### 示例

#### 示例 1
**输入:**  
```json
edges1 = [[0,1],[0,2],[0,3]], edges2 = [[0,1]]
```
**输出:**  
```
3
```
**解释:**  
将第一棵树的节点 `0` 与第二棵树的任意节点相连，即可得到直径为 `3` 的树。

#### 示例 2
**输入:**  
```json
edges1 = [[0,1],[0,2],[0,3],[2,4],[2,5],[3,6],[2,7]],
edges2 = [[0,1],[0,2],[0,3],[2,4],[2,5],[3,6],[2,7]]
```
**输出:**  
```
5
```
**解释:**  
将第一棵树的节点 `0` 与第二棵树的节点 `0` 相连，即可得到直径为 `5` 的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把两棵树的每一对节点都尝试连一次**，然后计算合并后树的直径，取最小值。

- **遍历所有可能的连接**  
  第一本树有 `n` 个节点，第二本树有 `m` 个节点，所有可能的连边有 `n × m` 条。我们可以用两层循环枚举 `(a, b)`，其中 `a` 来自第一棵树，`b` 来自第二棵树。

- **计算合并后树的直径**  
  合并后得到的是一棵新的无环连通图（仍然是树），直径就是**最长的两点之间的最短路径**。最直观的做法是对整棵新树做一次 **BFS/DFS** 找到最远点，再从该点再 BFS 一遍得到直径。

- **为什么暴力解一定正确**  
  我们把**所有可能**的连法都算了一遍，最小的那个自然就是答案。没有遗漏，也没有近似。

- **时间/空间复杂度的大白话**  
  - 时间复杂度：我们要枚举 `n·m` 条边，每条边都要跑两遍 BFS（每次遍历所有 `n+m` 个节点），于是总共要做 `O(n·m·(n+m))` 次基本操作。  
    用大白话说，就是如果两棵树各有 10⁵ 个节点，计算量会是 10⁵·10⁵·2·10⁵ ≈ 10¹⁵，根本不可能在几秒内算完。  
  - 空间复杂度：每次 BFS 需要保存 `n+m` 个节点的距离数组，`O(n+m)`，这部分还能接受。

#### 代码（Python）

```python
from collections import deque
from typing import List

def bfs(start: int, adj: List[List[int]]) -> List[int]:
    """返回 start 到所有节点的最短距离（层数），使用队列实现 BFS"""
    n = len(adj)
    dist = [-1] * n
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:                # 还没访问过
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def tree_diameter(adj: List[List[int]]) -> int:
    """求单棵树的直径，先随便找一个点，再找最远点，最后再 BFS 一遍"""
    # 第一次 BFS，随便从 0 开始
    d1 = bfs(0, adj)
    far = d1.index(max(d1))                 # 最远的节点
    # 第二次 BFS，从最远点出发
    d2 = bfs(far, adj)
    return max(d2)                          # 这就是直径

def min_diameter_bruteforce(edges1: List[List[int]], edges2: List[List[int]]) -> int:
    # 建图
    n, m = len(edges1) + 1, len(edges2) + 1
    g1 = [[] for _ in range(n)]
    g2 = [[] for _ in range(m)]
    for u, v in edges1:
        g1[u].append(v); g1[v].append(u)
    for u, v in edges2:
        g2[u].append(v); g2[v].append(u)

    # 原始两棵树的直径（不变的部分）
    d1 = tree_diameter(g1)
    d2 = tree_diameter(g2)

    ans = float('inf')
    # 枚举所有可能的连接 (a, b)
    for a in range(n):
        for b in range(m):
            # 把两棵树合并成一棵大树：把 g2 的节点编号整体平移 m
            N = n + m
            g = [[] for _ in range(N)]
            # 复制第一棵树
            for u in range(n):
                for v in g1[u]:
                    g[u].append(v)
            # 复制第二棵树（节点编号 + n）
            for u in range(m):
                for v in g2[u]:
                    g[u + n].append(v + n)
            # 加上新加的那条边
            g[a].append(b + n)
            g[b + n].append(a)

            # 计算合并后树的直径
            cur = tree_diameter(g)
            ans = min(ans, cur)

    return ans
```

> **提示**：上述代码仅用于说明思路，**在真正的 LeetCode 环境里会因为超时而失效**。

#### 复杂度

- **时间复杂度**：`O(n·m·(n+m))`  
  解释：`n·m` 是所有可能的连法，`(n+m)` 是每次 BFS 要遍历的节点数，乘起来就是总工作量。  
  用大白话讲，就是“先把两棵树的每一对节点都尝试一次，再把每次尝试都跑遍整棵树”，显然太慢了。

- **空间复杂度**：`O(n+m)`  
  解释：每次 BFS 需要保存一个长度为 `n+m` 的距离数组，其他额外空间是常数级别的。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于枚举所有 `n·m` 条可能的连边。事实上，**并不是每一对节点都值得尝试**，我们可以用树的结构特性把搜索范围压到常数级。

**关键观察**（提示里已经给出）：

> 把节点 `a`（在树 1）和节点 `b`（在树 2）相连后，新树的直径等于下面三者的最大值  
> 1. 树 1 本身的直径 `D1`（不受连接方式影响）  
> 2. 树 2 本身的直径 `D2`（同理）  
> 3. `dist1[a] + dist2[b] + 1`，其中 `dist1[a]` 是 **从 a 出发能到达的最远节点的距离**（即 a 的“最远距离”），`dist2[b]` 同理，`+1` 是新加的那条边。

所以我们只需要**让第三项尽可能小**，因为前两项是固定的。

---

#### 2.1 为什么最优的 `a`、`b` 必须是各自树的“中心”

- 对于一棵树，**最远距离最小的节点**叫做**树的中心**。  
- 中心的最远距离等于 `⌈D/2⌉`（直径除以 2 向上取整），直观上可以想象：把树的最长路径（直径）画成一条直线，中心就是这条线的中点（如果长度是偶数则唯一一个中点，奇数则有两个相邻的中点）。

如果我们把 `a` 放在树 1 的中心，那么 `dist1[a] = ⌈D1/2⌉` 已经是**所有节点中最小的最远距离**；同理，把 `b` 放在树 2 的中心可以让 `dist2[b] = ⌈D2/2⌉` 最小。

于是 **最小的可能第三项** 为  

```
⌈D1/2⌉ + ⌈D2/2⌉ + 1
```

---

#### 2.2 直接得到答案的公式

新树的直径 = 三个值的最大值：

```
answer = max( D1,
              D2,
              ⌈D1/2⌉ + ⌈D2/2⌉ + 1 )
```

只要我们能快速求出两棵树的直径 `D1`、`D2`，答案就算出来了。

---

#### 2.3 如何在 O(N) 时间内求树的直径

经典的 **两次 BFS/DFS** 方法：

1. 任意选一个节点 `x`，做一次 BFS，找到离 `x` 最远的节点 `u`。  
2. 再从 `u` 出发做一次 BFS，得到每个节点到 `u` 的距离，同时记录最远的节点 `v`，`dist(u, v)` 就是树的直径 `D`。

这两次遍历只会触碰每条边两次，时间 `O(N)`，空间 `O(N)`（存距离数组）。

如果我们还想知道每个节点的 **最远距离**（即 `dist[node] = max(dist_u[node], dist_v[node])`），只需要把第二次 BFS 得到的 `dist_u` 再跑一次 BFS 从 `v` 出发得到 `dist_v`，然后对每个节点取最大值即可。但在本题里我们只需要 `⌈D/2⌉`，直接用公式即可，无需逐点计算。

---

#### 代码（Python）

```python
from collections import deque
from typing import List

def bfs(start: int, adj: List[List[int]]) -> List[int]:
    """返回 start 到所有节点的最短距离（层数）"""
    n = len(adj)
    dist = [-1] * n
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def tree_diameter(adj: List[List[int]]) -> int:
    """两次 BFS 求树的直径（返回长度）"""
    # 第一次 BFS：随便选 0
    d1 = bfs(0, adj)
    far = d1.index(max(d1))          # 最远的节点 u
    # 第二次 BFS：从 u 出发
    d2 = bfs(far, adj)
    return max(d2)                   # 这就是直径

def minDiameterAfterMerging(edges1: List[List[int]], edges2: List[List[int]]) -> int:
    # 建图
    n = len(edges1) + 1
    m = len(edges2) + 1
    g1 = [[] for _ in range(n)]
    g2 = [[] for _ in range(m)]
    for u, v in edges1:
        g1[u].append(v); g1[v].append(u)
    for u, v in edges2:
        g2[u].append(v); g2[v].append(u)

    # 1️⃣ 求两棵树的直径
    D1 = tree_diameter(g1)
    D2 = tree_diameter(g2)

    # 2️⃣ 计算中心的最远距离 = ceil(D/2)
    #   Python 整数除法向上取整可以写成 (D + 1) // 2
    center1 = (D1 + 1) // 2
    center2 = (D2 + 1) // 2

    # 3️⃣ 依据公式得到答案
    ans = max(D1, D2, center1 + center2 + 1)
    return ans
```

> **代码说明**  
> - `bfs` 用队列实现，时间复杂度 `O(N)`，空间 `O(N)`。  
> - `tree_diameter` 只返回直径长度，内部已经完成两次 BFS。  
> - `center1`、`center2` 使用 `(D+1)//2` 实现向上取整，等价于 `ceil(D/2)`。  
> - 最后 `max` 取三者中的最大值，就是题目要求的 **最小可能直径**。

---

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  解释：我们对每棵树各做两次 BFS，遍历的边数正好是两棵树的边数之和 ` (n-1) + (m-1) ≈ n+m`。所有操作都是线性的，远快于暴力的 `O(n·m·(n+m))`。

- **空间复杂度**：`O(n + m)`  
  解释：需要存储两棵树的邻接表以及 BFS 时的距离数组，大小正比于节点总数 `n+m`。

---

## 心得

- **核心技巧**：  
  利用树的“中心”概念把**最远距离最小化**，从而把原本指数级的枚举压到常数时间。核心公式是  

  ```
  answer = max( D1, D2, ceil(D1/2) + ceil(D2/2) + 1 )
  ```

- **该技巧适用的题型**（类似题）  
  1. 两棵树合并后求最小直径（本题）。  
  2. 给定一棵树，向其中添加一条边使直径最小化。  
  3. 多棵树两两连通后，求整体直径的最优连接方式。

- **一句话总结解题钥匙**  
  **“把两棵树的中心相连”，因为中心的最远距离最小，能够让跨树的最长路径最短。**

---

## 反思

- **第一反应**：看到“连接两棵树”，自然想到枚举所有可能的连边，随后想到每次都重新计算直径——这就是暴力思路。

- **最容易踩的坑**  
  1. **忽略直径的固定部分**：`D1`、`D2` 与选择的节点无关，若不先把它们固定下来，容易在公式推导时混淆。  
  2. **中心的定义**：中心不一定是唯一的（奇数长度的直径会有两个中心），但它们的最远距离都是 `ceil(D/2)`，这一点必须记清。  
  3. **向上取整**：`ceil(D/2)` 在代码里要写成 `(D + 1) // 2`，否则会出现错误的结果。

- **下次遇到同类题，第一步该想到什么**  
  **先把“树的直径”及其“中心”算出来**，因为很多涉及跨树路径最短化的问题，都可以归结为在中心之间建立连接。只要明确这一步，后面的推导往往就水到渠成。