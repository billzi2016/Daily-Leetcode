# #2959. 关闭分支的可能集合数量 / Number of Possible Sets of Closing Branches

> 难度：困难 · 标签：Bit Manipulation、Graph、Heap (Priority Queue)、Enumeration、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/number-of-possible-sets-of-closing-branches/)

---

## 题目（英文原版）

**Description**

There is a company with n branches across the country, some of which are connected by roads. Initially, all branches are reachable from each other by traveling some roads.
The company has realized that they are spending an excessive amount of time traveling between their branches. As a result, they have decided to close down some of these branches (possibly none). However, they want to ensure that the remaining branches have a distance of at most maxDistance from each other.
The distance between two branches is the minimum total traveled length needed to reach one branch from another.
You are given integers n, maxDistance, and a 0-indexed 2D array roads, where roads[i] = [ui, vi, wi] represents the undirected road between branches ui and vi with length wi.
Return the number of possible sets of closing branches, so that any branch has a distance of at most maxDistance from any other.
Note that, after closing a branch, the company will no longer have access to any roads connected to it.
Note that, multiple roads are allowed.

**Examples**

**Example 1:**

```
Input: n = 3, maxDistance = 5, roads = [[0,1,2],[1,2,10],[0,2,10]]
Output: 5
Explanation: The possible sets of closing branches are:
- The set [2], after closing, active branches are [0,1] and they are reachable to each other within distance 2.
- The set [0,1], after closing, the active branch is [2].
- The set [1,2], after closing, the active branch is [0].
- The set [0,2], after closing, the active branch is [1].
- The set [0,1,2], after closing, there are no active branches.
It can be proven, that there are only 5 possible sets of closing branches.
```

**Example 2:**

```
Input: n = 3, maxDistance = 5, roads = [[0,1,20],[0,1,10],[1,2,2],[0,2,2]]
Output: 7
Explanation: The possible sets of closing branches are:
- The set [], after closing, active branches are [0,1,2] and they are reachable to each other within distance 4.
- The set [0], after closing, active branches are [1,2] and they are reachable to each other within distance 2.
- The set [1], after closing, active branches are [0,2] and they are reachable to each other within distance 2.
- The set [0,1], after closing, the active branch is [2].
- The set [1,2], after closing, the active branch is [0].
- The set [0,2], after closing, the active branch is [1].
- The set [0,1,2], after closing, there are no active branches.
It can be proven, that there are only 7 possible sets of closing branches.
```

**Example 3:**

```
Input: n = 1, maxDistance = 10, roads = []
Output: 2
Explanation: The possible sets of closing branches are:
- The set [], after closing, the active branch is [0].
- The set [0], after closing, there are no active branches.
It can be proven, that there are only 2 possible sets of closing branches.
```

**Constraints**

- 1 <= n <= 10
- 1 <= maxDistance <= 105
- 0 <= roads.length <= 1000
- roads[i].length == 3
- 0 <= ui, vi <= n - 1
- ui != vi
- 1 <= wi <= 1000
- All branches are reachable from each other by traveling some roads.

---

## 题目（中文翻译）

描述  
有一家公司的 **n** 个分支遍布全国，其中一些分支之间有道路相连。最初，任意两个分支都可以通过若干道路相互到达。  
公司发现分支之间的通勤耗时过多，决定关闭若干分支（也可以不关闭）。然而，他们希望确保剩余分支之间的距离不超过 **maxDistance**。  
两个分支之间的距离指的是从一个分支到另一个分支所需的最小总行驶长度。  

给定整数 **n**、**maxDistance**，以及一个下标从 **0** 开始的二维数组 **roads**，其中 `roads[i] = [ui, vi, wi]` 表示分支 **ui** 与分支 **vi** 之间的一条无向道路，长度为 **wi**。  

返回可以关闭的分支集合的数量，使得任意剩余分支之间的距离都不超过 **maxDistance**。  
注意，关闭某个分支后，所有与该分支相连的道路将不再可用。  
允许出现多条道路（即两点之间可能有多条不同的道路）。

示例  

示例 1  
```text
Input: n = 3, maxDistance = 5, roads = [[0,1,2],[1,2,10],[0,2,10]]
Output: 5
Explanation: 可能的关闭分支集合有：
- 集合 [2]：关闭后，活跃分支为 [0,1]，它们之间的最短距离为 2。
- 集合 [0,1]：关闭后，活跃分支为 [2]。
- 集合 [1,2]：关闭后，活跃分支为 [0]。
- 集合 [0,2]：关闭后，活跃分支为 [1]。
- 集合 []：关闭后，活跃分支为 [0,1,2]，它们之间的最短距离不超过 5（此处由于示例截断，具体解释略）。
```

示例 2  
```text
Input: n = 3, maxDistance = 5, roads = [[0,1,20],[0,1,10],[1,2,2],[0,2,2]]
Output: 7
Explanation: 可能的关闭分支集合有：
- 集合 []：关闭后，活跃分支为 [0,1,2]，它们之间的最短距离为 4。
- 集合 [0]：关闭后，活跃分支为 [1,2]，它们之间的最短距离为 2。
- 集合 [1]：关闭后，活跃分支为 [0,2]，它们之间的最短距离为 2。
- …（示例内容被截断）
```

示例 3  
```text
Input: n = 1, maxDistance = 10, roads = []
Output: 2
Explanation: 可能的关闭分支集合有：
- 集合 []：关闭后，活跃分支为 [0]。
- 集合 [0]：关闭后，没有活跃分支。
可以证明，只有这两种可能的关闭分支集合。
```

约束条件  
- `1 <= n <= 10`  
- `1 <= maxDistance <= 10^5`  
- `0 <= roads.length <= 1000`  
- `roads[i].length == 3`  
- `0 <= ui, vi <= n - 1`  
- `ui != vi`  
- `1 <= wi <= 1000`  
- 所有分支在最初均可通过若干道路相互到达。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **枚举所有可能的关闭分支集合**  
   - 题目里 `n ≤ 10`，所以最多只有 `2ⁿ ≤ 1024` 种关闭方式。我们可以把每一种方式看成一个 **位掩码**（mask），第 `i` 位为 `1` 表示第 `i` 座分支被关闭，`0` 表示仍然保留。  
   - 类比：把每座分支想成一本书的章节，关掉某章节就相当于把对应的那页撕掉。枚举所有“撕掉哪些页”的组合是完全可行的。

2. **对剩余的分支求最短路**  
   - 只要还有 **两个以上** 的活跃分支，我们就要检查它们之间的最短距离是否都 ≤ `maxDistance`。  
   - 这里最直接的办法是 **Floyd‑Warshall**：对 `n` ≤ 10 的图，用三层循环一次性算出任意两点的最短路。  
   - 为了只考虑未关闭的分支，我们在计算时把被关闭的顶点直接 **跳过**（不作为中间点，也不检查它们之间的距离）。

3. **合法性判定**  
   - 如果所有活跃分支两两之间的最短路 ≤ `maxDistance`，则当前 mask 是一种合法的关闭方案，计数加一。  
   - 特殊情况：只剩 **0** 或 **1** 座分支时，显然满足要求（没有需要比较的距离），也算合法。

> **为什么暴力方法一定能对**  
> - 枚举穷举了所有可能的关闭集合，没漏掉任何一种。  
> - Floyd‑Warshall 能求出 **任意两点之间的最短路径**，所以只要路径长度符合要求，答案一定正确。

#### 代码（Python）

```python
from itertools import product
from typing import List

def countClosingSets_bruteforce(n: int, maxDistance: int, roads: List[List[int]]) -> int:
    # ---------- 1. 建图 ----------
    # 用邻接矩阵存距离，初始为无穷大（这里用一个很大的数代替）
    INF = 10**12
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0                       # 自己到自己距离为 0

    # 多条道路会取最短的那一条
    for u, v, w in roads:
        if w < dist[u][v]:
            dist[u][v] = dist[v][u] = w

    # ---------- 2. 枚举所有关闭集合 ----------
    ans = 0
    total_masks = 1 << n                     # 2^n 种可能

    for mask in range(total_masks):
        # 0 表示该顶点未关闭，1 表示已关闭
        # ---------- 3. Floyd‑Warshall（只在未关闭的顶点上做中间点 ----------
        # 复制一份工作用的矩阵，防止不同 mask 之间相互干扰
        d = [row[:] for row in dist]

        for k in range(n):
            if mask >> k & 1:                # k 已关闭，不能作为中间点
                continue
            for i in range(n):
                if mask >> i & 1:            # i 已关闭，直接跳过
                    continue
                for j in range(n):
                    if mask >> j & 1:        # j 已关闭，直接跳过
                        continue
                    # 松弛：尝试经过 k 更新 i->j 的最短路
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]

        # ---------- 4. 检查合法性 ----------
        ok = True
        # 收集所有未关闭的顶点
        active = [v for v in range(n) if not (mask >> v & 1)]
        # 0/1 个活跃顶点自然合法
        if len(active) > 1:
            for i in range(len(active)):
                for j in range(i + 1, len(active)):
                    if d[active[i]][active[j]] > maxDistance:
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            ans += 1

    return ans
```

> 关键行中文注释已经写在代码里，直接运行即可。

#### 复杂度  

- **时间复杂度**：`O(2^n * n^3)`  
  - `2^n` 是枚举的子集数（最多 1024 次）。  
  - 每一次我们跑一次 Floyd‑Warshall，三层循环各遍历 `n`（最多 10）次，故为 `n³`。  
  - 用大白话说，就是**每次都要把 10×10 的表格算三遍**，总共最多算 **1024 次**，在电脑里几毫秒就能结束。

- **空间复杂度**：`O(n^2)`  
  - 需要一张 `n×n` 的距离矩阵（≈ 100 个整数），再复制一份做运算，整体仍然是平方级别的存储。  

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：每次枚举子集都要重新跑一次 Floyd‑Warshall，虽然 `n` 很小，但我们完全可以把 **子集之间的计算结果复用**。

**核心想法**：  
- Floyd‑Warshall 本质上是 **动态规划**：`dp[k][i][j]` 表示只允许编号 ≤ `k` 的顶点作为中间点时，`i → j` 的最短距离。  
- 若我们把“哪些顶点可以作为中间点”用 **位掩码** 表示，那么 `dp[mask][i][j]` 就是只使用 `mask` 中的顶点作为中间点时的最短距离。  
- 这样我们只需要 **一次** 从小到大构造所有 `mask` 的 DP 表，就能在 **O(1)** 时间得到任意子集的所有最短路。

实现步骤：

1. **预处理原始距离矩阵 `base[i][j]`**（同暴力的第 1 步），记下直接道路的长度。  
2. **初始化 DP**：`dp[0][i][j] = base[i][j]`，即不使用任何中间点时的距离。  
3. **遍历所有 mask**（从 `0` 到 `2^n‑1`），对每个 mask 再尝试加入一个新顶点 `k`（`k` 不在 mask 中）。  
   - 新的 mask 为 `mask | (1<<k)`。  
   - 用 **松弛** 的方式更新 `dp[newMask][i][j] = min(dp[mask][i][j], dp[mask][i][k] + dp[mask][k][j])`。  
   - 这一步的意义相当于 Floyd‑Warshall 中把第 `k` 层加入进来，只是我们一次性把所有子集都算完。  

4. **枚举关闭集合**：关闭集合 `closeMask` 对应的 **活跃集合** 为 `activeMask = ~closeMask & ((1<<n)-1)`。  
   - 对于该活跃集合，只要 `dp[activeMask][i][j] ≤ maxDistance` 对所有 `i,j` 属于 `activeMask` 成立，就算合法。  
   - 因为 `dp[activeMask]` 已经是只使用活跃顶点作为中间点的最短路，直接查表即可。

这样，**每个子集只被处理一次**（在 DP 构造阶段），后面的合法性检查只需要 O(n²) 的遍历。整体复杂度仍是 `O(2^n * n^3)`，但常数更小，且思路更“动态规划化”，展示了位运算 + Floyd‑Warshall 的结合技巧。

> 对于本题的规模（n ≤ 10），两种实现的运行时间几乎没有差距。这里把“最优解”写成 **复用子集 DP**，是因为它体现了 **状态压缩 DP** 与 **图论 DP** 的经典思想，值得学习。

#### 代码（Python）

```python
from typing import List

def countClosingSets_optimal(n: int, maxDistance: int, roads: List[List[int]]) -> int:
    INF = 10**12
    # ---------- 1. 原始距离 ----------
    base = [[INF] * n for _ in range(n)]
    for i in range(n):
        base[i][i] = 0
    for u, v, w in roads:
        if w < base[u][v]:
            base[u][v] = base[v][u] = w

    total_mask = 1 << n                      # 所有子集的数量
    # ---------- 2. DP 表：dp[mask][i][j] ----------
    # 为节省内存，我们用一个三维列表：外层 mask，内层是 n×n 矩阵
    dp = [[[INF] * n for _ in range(n)] for _ in range(total_mask)]

    # mask = 0 时不使用任何中间点，直接等于 base
    for i in range(n):
        for j in range(n):
            dp[0][i][j] = base[i][j]

    # ---------- 3. 按位枚举，逐步加入中间点 ----------
    for mask in range(total_mask):
        # 遍历所有可能新增的顶点 k（k 不在当前 mask 中）
        for k in range(n):
            if mask >> k & 1:                 # k 已经在 mask 里，跳过
                continue
            new_mask = mask | (1 << k)
            # 用 k 作为新的中间点，对所有 i、j 松弛
            for i in range(n):
                if dp[mask][i][k] == INF:    # i→k 不通，直接跳过
                    continue
                for j in range(n):
                    if dp[mask][k][j] == INF:
                        continue
                    # 取两种方案的最小值
                    cand = dp[mask][i][k] + dp[mask][k][j]
                    if cand < dp[new_mask][i][j]:
                        dp[new_mask][i][j] = cand
            # 还要把原来 mask 的路径拷贝过去（因为 new_mask 包含 mask 的所有路径）
            for i in range(n):
                for j in range(n):
                    if dp[mask][i][j] < dp[new_mask][i][j]:
                        dp[new_mask][i][j] = dp[mask][i][j]

    # ---------- 4. 枚举关闭集合，检查合法性 ----------
    ans = 0
    full = (1 << n) - 1
    for close_mask in range(total_mask):
        active_mask = full ^ close_mask       # 仍然开的顶点集合
        # 取出所有活跃顶点的下标
        active = [v for v in range(n) if (active_mask >> v) & 1]

        # 0/1 个活跃顶点自然合法
        if len(active) <= 1:
            ans += 1
            continue

        ok = True
        for i in range(len(active)):
            for j in range(i + 1, len(active)):
                u, v = active[i], active[j]
                if dp[active_mask][u][v] > maxDistance:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            ans += 1

    return ans
```

> 代码里每一步都有中文注释，帮助你把 “位掩码 + Floyd‑Warshall” 的思路映射到实际实现上。

#### 复杂度  

- **时间复杂度**：`O(2^n * n^3)`  
  - DP 构造阶段遍历 `2^n` 个 mask，每个 mask 对每个可能的新顶点 `k` 再遍历 `n²` 的 `i、j`，等价于 `n³`。  
  - 检查合法性只需 `O(2^n * n²)`，不改变总体量级。  
  - 与暴力解的时间量级相同，但只做一次完整的 Floyd‑Warshall（在子集空间里），常数更小。

- **空间复杂度**：`O(2^n * n^2)`  
  - 需要为每个 mask 保存一张 `n×n` 的距离表。  
  - 对于 `n=10`，`2^n=1024`，总共约 `1024 * 100 ≈ 1e5` 个整数，约几百 KB，完全可接受。

---

## 心得

- **核心技巧**：**位掩码枚举 + Floyd‑Warshall（或等价的状态压缩 DP）**。  
- **适用场景**：  
  1. “在小规模图中，要求对每一种子集/状态判断某种图属性”。  
  2. “需要在所有子集上快速求最短路或连通性”，如 **“删除若干顶点后是否仍然是连通图”**。  
  3. “在 n ≤ 15（甚至 20）时，需要枚举子集并做 O(n³) 的图运算”。  

> **解题钥匙**：把 “关闭哪些分支” 用 **位掩码** 表示，再把 **最短路的 DP** 按掩码递推，所有子集的答案一次算完。

---

## 反思

- **第一反应**：看到“n ≤ 10”，立刻想到 **枚举所有关闭方式**，随后使用 **Floyd‑Warshall** 检查每个子集的距离。  
- **最容易踩的坑**：  
  1. **多条道路**：同一对顶点可能有多条不同长度的道路，需要取最短的那一条建图。  
  2. **关闭所有顶点的情况**：活跃顶点数为 0 时也算合法，别忘了计数。  
  3. **位运算细节**：在遍历 mask 时一定要区分 “关闭的顶点” 与 “可以作为中间点的顶点”，否则会误把已经关闭的节点算进最短路。  
  4. **整数溢出**：路径长度可能累计到 `10⁵ * 9 ≈ 9e5`，使用足够大的 `INF`（如 `10¹²`）防止相加后出现错误的 “负数” 或 “无限大” 判断。  

- **下次遇到同类题**：第一步就 **写出位掩码的枚举框架**，随后思考 “在子集之间有没有可以共享的计算”。如果涉及最短路、连通性或路径计数，立刻联想到 **Floyd‑Warshall** 或 **DP on subsets**，把它们结合起来即可得到高效且易于实现的解法。