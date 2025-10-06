# #3372. 连接树 I 后最大化目标节点数量 / Maximize the Number of Target Nodes After Connecting Trees I

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximize-the-number-of-target-nodes-after-connecting-trees-i/)

---

## 题目（英文原版）

**Description**

There exist two undirected trees with n and m nodes, with distinct labels in ranges [0, n - 1] and [0, m - 1], respectively.
You are given two 2D integer arrays edges1 and edges2 of lengths n - 1 and m - 1, respectively, where edges1[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the first tree and edges2[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the second tree. You are also given an integer k.
Node u is target to node v if the number of edges on the path from u to v is less than or equal to k. Note that a node is always target to itself.
Return an array of n integers answer, where answer[i] is the maximum possible number of nodes target to node i of the first tree if you have to connect one node from the first tree to another node in the second tree.
Note that queries are independent from each other. That is, for every query you will remove the added edge before proceeding to the next query.

**Examples**

**Example 1:**

```
Input: edges1 = [[0,1],[0,2],[2,3],[2,4]], edges2 = [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]], k = 2
Output: [9,7,9,8,8]
Explanation:
```

**Example 2:**

```
Input: edges1 = [[0,1],[0,2],[0,3],[0,4]], edges2 = [[0,1],[1,2],[2,3]], k = 1
Output: [6,3,3,3,3]
Explanation:
For every i , connect node i of the first tree with any node of the second tree.
```

**Constraints**

- 2 <= n, m <= 1000
- edges1.length == n - 1
- edges2.length == m - 1
- edges1[i].length == edges2[i].length == 2
- edges1[i] = [ai, bi]
- 0 <= ai, bi < n
- edges2[i] = [ui, vi]
- 0 <= ui, vi < m
- The input is generated such that edges1 and edges2 represent valid trees.
- 0 <= k <= 1000

---

## 题目（中文翻译）

存在两棵无向树（undirected tree），第一棵有 `n` 个节点，第二棵有 `m` 个节点，节点标签分别在区间 `[0, n - 1]` 和 `[0, m - 1]` 内且互不相同。  

给定两个二维整数数组 `edges1` 和 `edges2`，长度分别为 `n - 1` 和 `m - 1`，其中 `edges1[i] = [a_i, b_i]` 表示第一棵树中节点 `a_i` 与节点 `b_i` 之间有一条边，`edges2[i] = [u_i, v_i]` 表示第二棵树中节点 `u_i` 与节点 `v_i` 之间有一条边。另给定整数 `k`。  

如果从节点 `u` 到节点 `v` 的路径（path）上的边数 **不大于** `k`，则称节点 `u` 是节点 `v` 的 **目标**（target）。注意，节点始终是其自身的目标。  

返回一个长度为 `n` 的整数数组 `answer`，其中 `answer[i]` 表示在**必须**将第一棵树的某个节点与第二棵树的某个节点连接（即在两棵树之间新增一条边）后，**第一棵树中节点 `i` 的目标节点数量的最大可能值**。  

注意，**每一次查询相互独立**。也就是说，对于每一次连接后计算得到的结果，你需要在进行下一次查询之前把刚才添加的那条边移除。

---

## 示例

### 示例 1

```text
Input: edges1 = [[0,1],[0,2],[2,3],[2,4]], edges2 = [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]], k = 2
Output: [9,7,9,8,8]
Explanation:
在第一棵树的每个节点 `i` 与第二棵树的任意节点相连后，统计第一棵树中以 `i` 为中心、距离不超过 `k=2` 的节点总数，并取最大值。得到的结果分别为 `[9,7,9,8,8]`。
```

### 示例 2

```text
Input: edges1 = [[0,1],[0,2],[0,3],[0,4]], edges2 = [[0,1],[1,2],[2,3]], k = 1
Output: [6,3,3,3,3]
Explanation:
对于每个 `i`，将第一棵树的节点 `i` 与第二棵树中的任意节点相连后，计算第一棵树中以 `i` 为中心、距离不超过 `k=1` 的节点数的最大可能值。结果为 `[6,3,3,3,3]`。
```

---

## 约束条件

- `2 <= n, m <= 1000`
- `edges1.length == n - 1`
- `edges2.length == m - 1`
- `edges1[i].length == edges2[i].length == 2`
- `edges1[i] = [a_i, b_i]`，`0 <= a_i, b_i < n`
- `edges2[i] = [u_i, v_i]`，`0 <= u_i, v_i < m`
- 输入保证 `edges1` 与 `edges2` 构成合法的树（valid tree）
- `0 <= k <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **枚举** 所有可以添加的边 `(a , b)`，其中 `a` 是第一棵树的任意节点，`b` 是第二棵树的任意节点。  
2. 对于每一条候选边，**把两棵树连在一起**（这时得到一棵 `n+m` 节点的大树）。  
3. 对于当前查询的节点 `i`，**从 `i` 出发做一次 BFS/DFS**，得到它到所有节点的最短距离。  
4. 统计距离 `≤ k` 的节点个数，这就是在这条候选边下 `i` 能“看到”的节点数。  
5. 对所有候选边取最大值，得到 `answer[i]`。  

> **类比**：把每条候选边想成一把“桥”。我们把桥搭好后，就像在一张大地图上走路，走到的格子数不超过 `k` 的格子就算作“可达”。  
> **为什么对的**：我们把所有可能的桥都试了一遍，必然能找到让 `i` 能看到最多节点的那一座桥。  

**复杂度分析（大白话）**  

- 枚举桥的数量是 `n * m`（第一棵树有 `n` 个点，第二棵树有 `m` 个点）。  
- 对每一座桥，我们都要 **从 `i` 做一次 BFS**，遍历整棵新树，时间是 `O(n + m)`。  
- 还要对 **每个 `i`（共 `n` 个）** 重复上述过程。  

所以总时间是  

```
O( n          // 枚举 i
   * n*m      // 枚举桥
   * (n+m) )  // BFS 一次
≈ O(n²·m·(n+m))
```

在最坏情况下（`n=m=1000`）会是 **上百亿次操作**，根本跑不完。  

空间上只需要存图和 BFS 的队列，`O(n+m)`，这点还算可以。

#### 代码（Python）

```python
from collections import deque
from copy import deepcopy
from typing import List

def bfs(start: int, adj: List[List[int]]) -> List[int]:
    """返回 start 到所有点的最短距离（无权图）"""
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

def brute_force(edges1: List[List[int]], edges2: List[List[int]], k: int) -> List[int]:
    n, m = len(edges1) + 1, len(edges2) + 1
    # 原始两棵树的邻接表
    adj1 = [[] for _ in range(n)]
    for a, b in edges1:
        adj1[a].append(b)
        adj1[b].append(a)

    adj2 = [[] for _ in range(m)]
    for u, v in edges2:
        adj2[u].append(v)
        adj2[v].append(u)

    ans = [0] * n

    # 对每个查询节点 i
    for i in range(n):
        best = 0
        # 枚举所有可能的桥 (a, b)
        for a in range(n):
            for b in range(m):
                # 复制两棵树的邻接表并加上新边
                g = deepcopy(adj1) + [[]]          # 这里先占位，后面会合并
                g = [list(nei) for nei in g]        # 防止浅拷贝
                # 把第二棵树的节点编号整体平移 m（因为两棵树的标签不冲突）
                offset = n
                g2 = [list(nei) for nei in adj2]
                for u in range(m):
                    g2[u] = [v + offset for v in g2[u]]
                # 合并两棵树
                g.extend(g2)
                # 加上桥 (a, b+offset)
                g[a].append(b + offset)
                g[b + offset].append(a)

                # BFS 从 i 开始，统计距离 ≤ k 的点数
                d = bfs(i, g)
                cnt = sum(1 for x in d if 0 <= x <= k)
                best = max(best, cnt)

        ans[i] = best
    return ans
```

> **注意**：上述代码仅用于说明思路，实际运行会因深拷贝和 BFS 的次数而超时。

#### 复杂度  

- **时间复杂度**：`O(n²·m·(n+m))`（解释见上文），在本题约为上百亿次，无法接受。  
- **空间复杂度**：`O(n+m)`（存图和 BFS 队列），这部分还算合理。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 出在两点：

1. **枚举所有桥**（`n·m` 条）是多余的。  
2. 对每条桥都 **重新 BFS**，导致 `O(n+m)` 的重复遍历。

我们需要 **把所有桥的影响合并**，只做一次或少量次数的遍历。  

---

#### 2.1 关键观察  

- **同树内部的距离**：在连接两棵树后，任意两个节点如果都在同一棵树里，最短路径仍然是原来的路径。因为唯一的跨树边只能走一次，走回去只会让路径更长。  
  - 因此 **第一棵树内部** `i` 能看到的节点数 **与是否加桥无关**，只和 `i` 本身的 `k`‑范围有关。  
- **跨树的距离**：若要从 `i`（在第一棵树）到达第二棵树的某个节点 `v`，必须走：  
  ```
  i  --(dist(i, a))-->  a  --(1)-->  b  --(dist(b, v))-->  v
  ```
  其中 `(a , b)` 是我们添加的那条桥。  
  所以跨树的总距离是 `dist(i, a) + 1 + dist(b, v)`。  

- 对固定的 `i`，**只关心** 两件事：  
  1. `dist(i, a)` —— `i` 到桥的入口 `a` 在第一棵树里的距离。  
  2. 在第二棵树里，**以 `b` 为中心，半径 `R = k - dist(i, a) - 1`** 能覆盖多少节点。  

> 把 “以 `b` 为中心，半径 `R` 能覆盖多少节点” 看成一种 **“局部视野”**。我们只需要知道，**在第二棵树里，半径为 `R` 时最多能看到多少节点**，不必记是哪棵树的哪一个 `b`。

---

#### 2.2 预处理  

1. **所有节点对之间的距离**  
   - 对每棵树分别做 `n`（或 `m`）次 BFS/DFS，得到  
     `dist1[u][v]`：第一棵树中 `u` 到 `v` 的距离  
     `dist2[p][q]`：第二棵树中 `p` 到 `q` 的距离  
   - 复杂度 `O(n² + m²)`，在 `n,m ≤ 1000` 之内完全可以接受。  

2. **第二棵树的 “最佳视野”**  
   - 对每个中心节点 `b`，统计它在不同半径 `r (0 … k)` 内能覆盖的节点数。  
   - 具体做法：  
     - 建立一个长度为 `k+1` 的数组 `cnt[r]`，遍历所有 `v`，若 `dist2[b][v] = d ≤ k`，则 `cnt[d] += 1`。  
     - 再把 `cnt` 做前缀和，得到 `pref[r] = Σ_{t≤r} cnt[t]`，这就是 “半径 ≤ r 能覆盖的节点数”。  
   - 记录全局最大值 `best2[r] = max_{b} pref[r]`。  
   - 这一步的时间是 `O(m² + m·k)`，`k ≤ 1000`，同样足够快。  

3. **第一棵树内部的可达节点数**  
   - 对每个 `i`，利用 `dist1[i][*]` 直接统计 `cntInside[i] = #{ u | dist1[i][u] ≤ k }`。  
   - 时间 `O(n²)`。  

---

#### 2.3 计算答案  

对每个查询节点 `i`：

```
inside = cntInside[i]                         # 只看第一棵树，固定不变
best_extra = 0
for each node a in 第一棵树:
    d = dist1[i][a]                            # i 到桥入口的距离
    remain = k - d - 1                         # 跨树后还能走的步数
    if remain >= 0:
        best_extra = max(best_extra, best2[remain])
answer[i] = inside + best_extra
```

- `best2[remain]` 已经是“在第二棵树里，任选中心，半径 ≤ remain 时最多能覆盖的节点数”。  
- 因此只要遍历 `a`（`n` 次）即可得到 `i` 的最优跨树贡献。  

整体时间：

- 预处理 `O(n² + m² + m·k)`  
- 主循环 `O(n²)`（每个 `i` 再遍历所有 `a`）  

总计约 `O(n² + m²)`，在 `n,m ≤ 1000` 时最多约 `2·10⁶` 次基本运算，轻松通过。  

空间：

- 两个距离矩阵 `dist1 (n×n)`、`dist2 (m×m)` → 最多约 `2·10⁶` 整数，约 8 MB。  
- 其余数组 `best2、cntInside` 等均为线性大小。  

---

#### 代码（Python）

```python
from collections import deque
from typing import List

def all_pair_dist(n: int, adj: List[List[int]]) -> List[List[int]]:
    """返回 n 个节点的全部最短距离矩阵（无权树）"""
    dist = [[-1] * n for _ in range(n)]

    for s in range(n):
        q = deque([s])
        dist[s][s] = 0
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[s][v] == -1:
                    dist[s][v] = dist[s][u] + 1
                    q.append(v)
    return dist

def max_target_nodes(edges1: List[List[int]],
                    edges2: List[List[int]],
                    k: int) -> List[int]:
    # ---------- 建图 ----------
    n = len(edges1) + 1
    m = len(edges2) + 1

    adj1 = [[] for _ in range(n)]
    for a, b in edges1:
        adj1[a].append(b)
        adj1[b].append(a)

    adj2 = [[] for _ in range(m)]
    for u, v in edges2:
        adj2[u].append(v)
        adj2[v].append(u)

    # ---------- 1. 所有节点间距离 ----------
    dist1 = all_pair_dist(n, adj1)   # n x n
    dist2 = all_pair_dist(m, adj2)   # m x m

    # ---------- 2. 第二棵树的 best2[r] ----------
    # best2[r] = 在第二棵树里，任选中心，半径 <= r 能覆盖的最多节点数
    best2 = [0] * (k + 1)            # r 可能为 0~k
    for center in range(m):
        # cnt[d] 记录恰好距离为 d 的节点数（只统计 d <= k）
        cnt = [0] * (k + 1)
        for v in range(m):
            d = dist2[center][v]
            if d <= k:
                cnt[d] += 1
        # 前缀和得到半径 <= r 的节点数
        pref = 0
        for r in range(k + 1):
            pref += cnt[r]            # <= r 的总数
            if pref > best2[r]:
                best2[r] = pref

    # ---------- 3. 第一棵树内部的可达节点数 ----------
    inside_cnt = [0] * n
    for i in range(n):
        inside_cnt[i] = sum(1 for d in dist1[i] if d != -1 and d <= k)

    # ---------- 4. 计算答案 ----------
    ans = [0] * n
    for i in range(n):
        best_extra = 0
        for a in range(n):
            d = dist1[i][a]               # i -> a 的距离
            remain = k - d - 1            # 跨树后还能走的步数
            if remain >= 0:
                # best2[remain] 已经是第二棵树的最优覆盖数
                if best2[remain] > best_extra:
                    best_extra = best2[remain]
        ans[i] = inside_cnt[i] + best_extra
    return ans
```

> **代码说明**  
- `all_pair_dist` 用 BFS 从每个节点出发，得到完整的距离矩阵。  
- `best2` 的构造把“任选中心”这一步提前做了，后面只要查表即可。  
- 主循环里只遍历 `a`（第一棵树的入口），没有再遍历第二棵树的中心 `b`，把原来 `n·m` 的组合压缩成 `n`。  

#### 复杂度  

- **时间复杂度**：`O(n² + m²)`  
  - 计算两棵树的全距各一次 `O(n²)`、`O(m²)`。  
  - 生成 `best2` 也在 `O(m²)` 范围内。  
  - 主循环 `O(n²)`。整体远小于暴力的 `O(n²·m·(n+m))`。  
- **空间复杂度**：`O(n² + m²)`（距离矩阵） + `O(k)`（`best2`），约几 MB，符合限制。  

---

## 心得  

- **核心技巧**：把跨树距离拆成 “`i` 到桥入口的距离” + “桥本身的 1 条边” + “第二棵树内部的距离”。  
- **关键点**：  
  1. 同一棵树内部的最短路径不受跨树边的影响。  
  2. 对第二棵树，只需要知道 **半径 `r` 时的最大覆盖数**，不必记具体中心。  
- **适用的题型**：  
  1. 两棵（或多棵）图通过少量额外边连接，求最短路或可达节点数。  
  2. “在树上选择根/中心，使得半径 ≤ R 时覆盖最多节点” 类似的 **树的中心/覆盖** 问题。  
- **一句话总结**：把“所有可能的桥”压缩成“从 `i` 的视角看，入口距离决定剩余半径”，只需预处理一次全距和一次“半径最大覆盖”，即可线性求解。  

---

## 反思  

- **第一反应**：直接枚举所有可能的连接边并跑 BFS，想当然地认为数据量不大。  
- **最容易踩的坑**：  
  - 忽视了同树内部距离不受新边影响，导致不必要的重复计算。  
  - 没有把 “第二棵树的最佳覆盖数” 进行汇总，导致仍然是 `O(n·m)` 的枚举。  
  - 边界条件：`k` 可能为 0，此时只能算自身，`remain = k - d - 1` 可能为负，需要提前判断。  
- **下次类似题目**：第一步先 **分析路径结构**（哪部分会受新边影响），把影响因素拆分成若干独立的 “距离+半径” 形式；随后 **预处理所有可能的局部最优**（如本题的 `best2`），最后在每个查询中只做 **O(节点数)** 的遍历。这样可以把指数级的枚举压到多项式时间。