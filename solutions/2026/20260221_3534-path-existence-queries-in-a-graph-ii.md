# #3534. 图中路径存在查询 II / Path Existence Queries in a Graph II

> 难度：困难 · 标签：Array、Binary Search、Greedy、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/path-existence-queries-in-a-graph-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the number of nodes in a graph, labeled from 0 to n - 1.
You are also given an integer array nums of length n and an integer maxDiff.
An undirected edge exists between nodes i and j if the absolute difference between nums[i] and nums[j] is at most maxDiff (i.e., |nums[i] - nums[j]| <= maxDiff).
You are also given a 2D integer array queries. For each queries[i] = [ui, vi], find the minimum distance between nodes ui and vi. If no path exists between the two nodes, return -1 for that query.
Return an array answer, where answer[i] is the result of the ith query.
Note: The edges between the nodes are unweighted.
Thus, the output is [1, 2, -1, 1].

**Examples**

**Example 1:**

```
Input: n = 5, nums = [1,8,3,4,2], maxDiff = 3, queries = [[0,3],[2,4]]
Output: [1,1]
Explanation:
The resulting graph is:

Thus, the output is [1, 1] .
```

**Example 2:**

```
Input: n = 5, nums = [5,3,1,9,10], maxDiff = 2, queries = [[0,1],[0,2],[2,3],[4,3]]
Output: [1,2,-1,1]
Explanation:
The resulting graph is:
```

**Example 3:**

```
Input: n = 3, nums = [3,6,1], maxDiff = 1, queries = [[0,0],[0,1],[1,2]]
Output: [0,-1,-1]
Explanation:
There are no edges between any two nodes because:
Thus, no node can reach any other node, and the output is [0, -1, -1] .
```

**Constraints**

- 1 <= n == nums.length <= 105
- 0 <= nums[i] <= 105
- 0 <= maxDiff <= 105
- 1 <= queries.length <= 105
- queries[i] == [ui, vi]
- 0 <= ui, vi < n

---

## 题目（中文翻译）

你得到一个整数 `n`，表示图（graph）中节点（node）的数量，编号为 `0` 到 `n‑1`。  
同时给定一个长度为 `n` 的整数数组 `nums` 和一个整数 `maxDiff`。  
如果两个节点 `i` 和 `j` 的 `nums[i]` 与 `nums[j]` 之间的绝对差（absolute difference）不超过 `maxDiff`（即 `|nums[i] - nums[j]| <= maxDiff`），则在它们之间存在一条无向（undirected）边（edge）。  
此外，还给定一个二维整数数组 `queries`（查询）。对于每个 `queries[i] = [ui, vi]`，求节点 `ui` 与 `vi` 之间的最小距离（distance）。如果两节点之间不存在路径，则该查询的答案为 `-1`。  
返回一个数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的结果。  
**注意：** 节点之间的边是无权（unweighted）的。

### 示例

#### 示例 1
```text
Input: n = 5, nums = [1,8,3,4,2], maxDiff = 3, queries = [[0,3],[2,4]]
Output: [1,1]
```
**解释：**  
得到的图如下：

因此输出为 `[1, 1]` 。

#### 示例 2
```text
Input: n = 5, nums = [5,3,1,9,10], maxDiff = 2, queries = [[0,1],[0,2],[2,3],[4,3]]
Output: [1,2,-1,1]
```
**解释：**  
得到的图如下：

#### 示例 3
```text
Input: n = 3, nums = [3,6,1], maxDiff = 1, queries = [[0,0],[0,1],[1,2]]
Output: [0,-1,-1]
```
**解释：**  
任意两个节点之间均不存在边，因为：

因此没有节点能够到达其他节点，输出为 `[0, -1, -1]` 。

### 约束条件
- `1 <= n == nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`
- `0 <= maxDiff <= 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i] == [ui, vi]`
- `0 <= ui, vi < n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把图真的画出来**，然后对每个查询用 BFS（广度优先搜索）求最短路径。

- **怎么画图**  
  对所有 `i , j (i ≠ j)` 检查 `|nums[i] - nums[j]| ≤ maxDiff`，如果满足就在 `i` 与 `j` 之间连一条无向边。  
  这相当于在现实生活中“把每个人的身高写在纸上”，只要两个人身高差不超过 `maxDiff`，他们就可以直接握手（连边）。

- **为什么能得到答案**  
  BFS 每次都按照层数扩展：第一层是起点本身，第二层是所有可以 **一步** 到达的节点，第三层是 **两步** 能到达的节点……当 BFS 第一次碰到目标节点时，层数就是最短路径长度。

- **时间/空间复杂度**  
  - **建图**：要检查 `n` 个节点两两之间是否满足条件，最坏情况要比较 `n·(n‑1)/2 ≈ O(n²)` 次。  
  - **每个查询的 BFS**：在最坏情况下需要遍历整张图，也就是 `O(n + m)`，而这里的 `m`（边数）在最坏情况下也是 `O(n²)`，所以每个查询仍然是 `O(n²)`。  
  - **总时间**：`O(n² + q·n²)`，对 `n ≤ 10⁵` 完全不可接受。  
  - **空间**：存邻接表需要 `O(n²)` 的额外空间（每条边都要存），这在内存上也会炸掉。

> **大白话解释**：  
> `O(n²)` 就像把 `n` 本书排成两排，每本书都要和另一排的每本书握手一次。`n = 10⁵` 时，握手次数已经是 10⁹ 次以上，根本跑不完。

#### 代码（Python）

```python
from collections import deque
from typing import List

def brute_force(n: int, nums: List[int], maxDiff: int,
                queries: List[List[int]]) -> List[int]:
    # ---------- 1. 建图 ----------
    # adj[i] 保存所有和 i 直接相连的节点
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(nums[i] - nums[j]) <= maxDiff:
                adj[i].append(j)
                adj[j].append(i)          # 因为是无向图

    # ---------- 2. 对每个查询做 BFS ----------
    def bfs(s: int, t: int) -> int:
        if s == t:                     # 起点就是终点，距离为 0
            return 0
        vis = [False] * n
        q = deque([(s, 0)])            # (当前节点, 已走的步数)
        vis[s] = True
        while q:
            cur, d = q.popleft()
            for nb in adj[cur]:
                if not vis[nb]:
                    if nb == t:        # 第一次碰到目标，层数就是答案
                        return d + 1
                    vis[nb] = True
                    q.append((nb, d + 1))
        return -1                       # BFS 结束仍未到达，说明不可达

    ans = []
    for u, v in queries:
        ans.append(bfs(u, v))
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² + q·n²)`  
  - 建图需要 `n²` 次比较；每个查询的 BFS 最坏也要遍历 `n²` 条边。  
  - 直观上来说，这相当于“每次都把整个图重新走一遍”，显然太慢。

- **空间复杂度**：`O(n²)`  
  - 邻接表里要存每条可能的边，最坏情况下几乎是完整的无向图（每两个节点都有边），所以需要 `n²` 的存储空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“每次都把整张图遍历一次”**。  
观察题目可以发现，**边的存在只跟 `nums` 的大小差有关**，而不跟节点的下标顺序有关。  

> **关键观察**  
> 把所有节点按 `nums[i]` 从小到大排好序，记排好序后的位置为 `pos[i]`（`pos` 是原下标到排好序后下标的映射）。  
> 在排好序的序列里，满足 `|nums[i] - nums[j]| ≤ maxDiff` 的节点 **一定是相邻的一个连续区间**。  
> 换句话说，对排好序的第 `k` 个节点（记作 `k`），它**一步**能到达的所有节点正好是 `[L[k], R[k]]` 这段连续区间。

于是我们把问题转化为：

> 在一个 **只包含区间跳跃的 1 维坐标轴**（排序后的下标）上，求从点 `a` 到点 `b` 最少需要多少次“跳到覆盖区间”。

这正好可以用 **二分跳（binary jumping）**（也叫 **倍增**）来求最少跳数。  
二分跳的核心是预处理 `jump[k][i]` ——**从位置 `i` 出发，恰好跳 `2^k` 步后能覆盖的最左 / 最右下标**。  
随后对每个查询从大到小尝试跳 `2^k` 步，如果跳完后仍未覆盖目标，就真的跳过去并累计步数。这样最多跳 `log n` 次即可得到答案。

下面一步步说明如何构造这些跳表。

---

#### 2.1 计算一步能到达的区间 `[L[i], R[i]]`

因为 `nums` 已经排好序，只需要两个滑动指针：

```
j 向右移动，保持 nums[j] - nums[i] <= maxDiff
左指针 i 向右移动时，左界 L[i] = 当前的左指针位置
右界 R[i] = 当前的右指针位置
```

时间复杂度 `O(n)`。

---

#### 2.2 为二分跳准备 “区间合并” 操作

设 `jump[k][i] = (left, right)` 表示 **从位置 `i` 出发，恰好跳 `2^k` 步后能覆盖的最左 / 最右下标**。

- `jump[0][i]` 就是上一步得到的 `[L[i], R[i]]`。
- 对于 `k > 0`，先得到 `jump[k‑1][i] = (l1, r1)`。再把 **这段区间** `[l1, r1]` 视作“一次大跳的起点集合”，我们需要知道从这整个集合再跳 `2^{k‑1}` 步能覆盖的最左 / 最右位置。  
  这等价于 **对区间 `[l1, r1]` 询问**：所有 `jump[k‑1][*]` 中的左界最小值、右界最大值。

> **如何快速求区间最小左 / 最大右**  
> 使用 **稀疏表（Sparse Table）**，对每一层 `k‑1` 分别构建两张稀疏表：
> - `st_min[k‑1][i]`：在以 `i` 为左端点、长度为 `2^p` 的区间里，左界的最小值。  
> - `st_max[k‑1][i]`：对应的右界最大值。  
> 稀疏表支持 `O(1)` 区间最值查询，构建时间 `O(n log n)`。

于是：

```
left  = min_left_in_range(l1, r1)   # 用稀疏表
right = max_right_in_range(l1, r1)  # 用稀疏表
jump[k][i] = (left, right)
```

递推到 `k = LOG`（`LOG = ceil(log2 n)`），整体预处理时间 `O(n log n)`，空间同样 `O(n log n)`。

---

#### 2.3 回答单个查询

给定原始下标 `u, v`，先转换为排好序后的下标 `pu, pv`（通过 `pos` 数组），保证 `pu ≤ pv`。

我们想找最小的步数 `ans` 使得从 `pu` 出发的 **跳 `ans` 步后覆盖区间** 包含 `pv`。  
采用 **从大到小的二分跳**：

```
cur_left = cur_right = pu      # 目前只在起点
ans = 0
for k from LOG down to 0:
    # 设想如果再跳 2^k 步，新的覆盖区间会是：
    new_left  = min_left_in_range(cur_left, cur_right)   # 使用 jump[k]
    new_right = max_right_in_range(cur_left, cur_right)
    if not (new_left <= pv <= new_right):   # 仍然没有覆盖目标
        cur_left, cur_right = new_left, new_right
        ans += 1 << k
# 循环结束后，目标仍未被覆盖，需要再跳一次
if cur_left <= pv <= cur_right:
    return ans
else:
    return ans + 1
```

如果即使跳 `2^LOG` 步（即整张图的直达范围）仍不包含 `pv`，说明两点 **不在同一个连通分量**，返回 `-1`。  

每个查询最多遍历 `LOG ≈ 17`（因为 `2^17 > 10⁵`）层，时间 `O(log n)`。

---

#### 2.4 总体复杂度

| 步骤               | 时间复杂度               | 空间复杂度               |
|-------------------|------------------------|--------------------------|
| 排序 + 建立 `pos` | `O(n log n)`           | `O(n)`                   |
| 计算一步区间 `L,R`| `O(n)`                 | `O(n)`                   |
| 稀疏表 + 二分跳   | `O(n log n)`           | `O(n log n)`（两张表）  |
| 每个查询           | `O(log n)`（≈17）      | `O(1)`                   |
| **总计**          | `O((n+q) log n)`       | `O(n log n)`             |

相较于暴力的 `O(n²)`，已经把时间降低到几乎线性，能够轻松通过 10⁵ 规模的测试。

---

#### 代码（Python）

```python
import math
from typing import List

def pathExistenceQueries(
    n: int, nums: List[int], maxDiff: int,
    queries: List[List[int]]
) -> List[int]:
    # ---------- 1. 按值排序 ----------
    order = sorted(range(n), key=lambda i: nums[i])   # 按 nums 从小到大排
    pos = [0] * n                                     # 原下标 -> 排序后下标
    for idx, node in enumerate(order):
        pos[node] = idx

    sorted_vals = [nums[i] for i in order]            # 方便后面二指针

    # ---------- 2. 计算一步能到达的区间 L,R ----------
    L = [0] * n
    R = [0] * n
    r = 0
    for i in range(n):
        while r < n and sorted_vals[r] - sorted_vals[i] <= maxDiff:
            r += 1
        # 此时 [i, r-1] 区间都是满足条件的
        L[i] = i
        R[i] = r - 1

    # ---------- 3. 预处理二分跳 ----------
    LOG = math.ceil(math.log2(n)) + 1   # 防止 n 为 1 时 log 为 0
    # jump_left[k][i] / jump_right[k][i] 表示 2^k 步后能到的最左/最右下标
    jump_left = [[0] * n for _ in range(LOG)]
    jump_right = [[0] * n for _ in range(LOG)]

    # k = 0 的情况直接是一步区间
    for i in range(n):
        jump_left[0][i] = L[i]
        jump_right[0][i] = R[i]

    # 为了快速查询区间最小 left / 最大 right，构建两张稀疏表
    # sparse_min[p][i] = min( jump_left[k][i ... i+2^p-1] )
    # sparse_max[p][i] = max( jump_right[k][i ... i+2^p-1] )
    # 这里我们在每一层 k 上单独构建稀疏表，因为后面只会在同一层查询
    # 为简化实现，直接在每层上用「RMQ」的 O(1) 查询（因为 n ≤ 1e5，log n ≈ 17，直接线性遍历也可以接受）
    # 下面用最直接的方式：在每层 k，预处理 prefix 最小/最大，随后区间查询 O(1)。
    # 为了代码简洁，这里用「离线」方式：在递推 jump 时直接遍历区间，因为区间长度最多 n，整体仍是 O(n log n)。

    for k in range(1, LOG):
        # 为当前层 k-1 构建两张「区间查询」的稀疏表
        # 稀疏表的长度为 n，最多 log n 层
        p_log = math.floor(math.log2(n)) + 1
        st_min = [[0] * n for _ in range(p_log)]
        st_max = [[0] * n for _ in range(p_log)]
        # 初始化第 0 层（长度为 1）
        for i in range(n):
            st_min[0][i] = jump_left[k-1][i]
            st_max[0][i] = jump_right[k-1][i]
        # 建立稀疏表
        j = 1
        while (1 << j) <= n:
            length = 1 << (j - 1)
            for i in range(n - (1 << j) + 1):
                st_min[j][i] = min(st_min[j-1][i], st_min[j-1][i + length])
                st_max[j][i] = max(st_max[j-1][i], st_max[j-1][i + length])
            j += 1

        # 辅助函数：在层 k-1 上查询 [l, r] 的最小 left / 最大 right
        def query_min(l: int, r: int) -> int:
            """返回 jump_left[k-1] 在区间 [l, r] 的最小值"""
            length = r - l + 1
            p = length.bit_length() - 1
            return min(st_min[p][l], st_min[p][r - (1 << p) + 1])

        def query_max(l: int, r: int) -> int:
            """返回 jump_right[k-1] 在区间 [l, r] 的最大值"""
            length = r - l + 1
            p = length.bit_length() - 1
            return max(st_max[p][l], st_max[p][r - (1 << p) + 1])

        # 递推当前层的 jump
        for i in range(n):
            l1, r1 = jump_left[k-1][i], jump_right[k-1][i]
            # 再跳 2^{k-1} 步，相当于在 [l1, r1] 区间上查询
            jump_left[k][i] = query_min(l1, r1)
            jump_right[k][i] = query_max(l1, r1)

    # ---------- 4. 处理查询 ----------
    ans = []
    for u, v in queries:
        pu, pv = pos[u], pos[v]
        if pu > pv:
            pu, pv = pv, pu

        # 先判断是否在同一连通分量：看最大的 2^LOG 步能否覆盖
        if not (jump_left[LOG-1][pu] <= pv <= jump_right[LOG-1][pu]):
            ans.append(-1)
            continue

        cur_l = cur_r = pu
        steps = 0
        # 从大到小尝试跳
        for k in range(LOG-1, -1, -1):
            nl = jump_left[k][cur_l]   # 这里我们直接取左端点的跳表
            nr = jump_right[k][cur_r]  # 同理取右端点的跳表
            # 注意：因为在同一层，左端点和右端点的区间可能不同，
            # 为了保证安全，取两者的最左最右再做一次合并
            nl = min(nl, jump_left[k][cur_r])
            nr = max(nr, jump_right[k][cur_l])
            if not (nl <= pv <= nr):
                steps += 1 << k
                cur_l, cur_r = nl, nr

        # 循环结束后，还差一步就能覆盖
        ans.append(steps + 1 if cur_l != pv or cur_r != pv else steps)
    return ans
```

> **代码说明（关键行中文注释）**  
> - `order = sorted(... )`：把节点按 `nums` 的大小排好序。  
> - `while r < n and sorted_vals[r] - sorted_vals[i] <= maxDiff:`：滑动窗口找一步能到达的最右边界。  
> - `jump_left[k][i] / jump_right[k][i]`：记录 2^k 步后能覆盖的最左/最右位置。  
> - `st_min / st_max`：稀疏表，用来在 `O(1)` 时间内查询区间的最小左界和最大右界。  
> - 查询部分的 `if not (jump_left[LOG-1][pu] <= pv <= jump_right[LOG-1][pu]):`：快速判断两点是否在同一个连通分量，若不在直接返回 `-1`。  
> - 主循环 `for k in range(LOG-1, -1, -1):`：从大到小尝试跳，累计步数，最后再加一次得到最小跳数。

---

## 心得

- **核心技巧**：把“值差 ≤ maxDiff 的无向图”转化为 **按值排序后的一维区间跳跃问题**，再用 **二分跳（倍增）+稀疏表** 求最少跳数。  
- **适用的题型**  
  1. “区间可达”类问题，例如 LeetCode **“Minimum Number of Steps to Reach Target”**（区间扩展）  
  2. “基于排序的图连通性”类，例如 **“Graph Connectivity With Threshold”**（阈值构图）  
  3. “多次区间合并后查询最小次数”类，如 **“Shortest Path in a Graph with Edge Weight 0/1”**（0‑1 BFS 的区间化）  
- **一句话总结解题钥匙**：**把图的边缘条件化为连续区间，利用倍增把“多少步能覆盖区间”抽象成区间最值查询**。

---

## 反思

- **第一反应**：看到 “|nums[i] - nums[j]| ≤ maxDiff” 立刻想到 **把所有满足条件的边直接连起来**，于是想用 BFS。  
- **最容易踩的坑**  
  1. **直接建图会爆内存**：`n` 可达 10⁵，完整邻接表是 `O(n²)`，根本不可行。  
  2. **忽视排序后区间的连续性**：如果不把节点按 `nums` 排序，就看不到“一步可达的区间”这一结构。  
  3. **二分跳的区间合并写错**：跳 `2^k` 步时必须对 **整个当前覆盖区间** 再查询最左/最右，否则会低估可达范围。  
- **下次遇到同类题的第一步**：**先检查是否可以把图的连通条件转化为一维区间或有序结构**，如果可以，就考虑 **滑动窗口 + 区间合并 + 倍增** 的思路，而不是直接暴力建图。