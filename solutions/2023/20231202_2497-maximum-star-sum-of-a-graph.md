# #2497. 最大星和 / Maximum Star Sum of a Graph

> 难度：中等 · 标签：Array、Greedy、Graph、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-star-sum-of-a-graph/)

---

## 题目（英文原版）

**Description**

There is an undirected graph consisting of n nodes numbered from 0 to n - 1. You are given a 0-indexed integer array vals of length n where vals[i] denotes the value of the ith node.
You are also given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
A star graph is a subgraph of the given graph having a center node containing 0 or more neighbors. In other words, it is a subset of edges of the given graph such that there exists a common node for all edges.
The image below shows star graphs with 3 and 4 neighbors respectively, centered at the blue node.
The star sum is the sum of the values of all the nodes present in the star graph.
Given an integer k, return the maximum star sum of a star graph containing at most k edges.

**Examples**

**Example 1:**

```
Input: vals = [1,2,3,4,10,-10,-20], edges = [[0,1],[1,2],[1,3],[3,4],[3,5],[3,6]], k = 2
Output: 16
Explanation: The above diagram represents the input graph.
The star graph with the maximum star sum is denoted by blue. It is centered at 3 and includes its neighbors 1 and 4.
It can be shown it is not possible to get a star graph with a sum greater than 16.
```

**Example 2:**

```
Input: vals = [-5], edges = [], k = 0
Output: -5
Explanation: There is only one possible star graph, which is node 0 itself.
Hence, we return -5.
```

**Constraints**

- n == vals.length
- 1 <= n <= 105
- -104 <= vals[i] <= 104
- 0 <= edges.length <= min(n * (n - 1) / 2, 105)
- edges[i].length == 2
- 0 <= ai, bi <= n - 1
- ai != bi
- 0 <= k <= n - 1

---

## 题目（中文翻译）

描述  
给定一个无向图，包含 n 个节点，编号为 0 到 n‑1。还有一个长度为 n 的整数数组 `vals`（0 索引），其中 `vals[i]` 表示第 i 个节点的值。  
另外给定一个二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条无向边。

星形图（star graph）是原图的一个子图，它由一个中心节点以及若干（0 条或更多）邻居节点组成。换句话说，星形图是原图中一组边的子集，这些边都有同一个公共节点（即中心节点）。  

星形和（star sum）是星形图中所有节点值的总和。  
给定整数 `k`，返回 **至多** 包含 `k` 条边的星形图的最大星形和。

示例  

示例 1  
输入: `vals = [1,2,3,4,10,-10,-20]`, `edges = [[0,1],[1,2],[1,3],[3,4],[3,5],[3,6]]`, `k = 2`  
输出: `16`  
解释: 上图展示了输入的图。  
星形图的最大星形和如蓝色部分所示。它以节点 3 为中心，选取了它的邻居节点 1 和 4。  
可以证明不存在星形图的和大于 16。

示例 2  
输入: `vals = [-5]`, `edges = []`, `k = 0`  
输出: `-5`  
解释: 唯一可能的星形图就是节点 0 本身，因此返回 -5。

约束条件  
- `n == vals.length`  
- `1 <= n <= 10^5`  
- `-10^4 <= vals[i] <= 10^4`  
- `0 <= edges.length <= min(n * (n - 1) / 2, 10^5)`  
- `edges[i].length == 2`  
- `0 <= a_i, b_i <= n - 1`  
- `a_i != b_i`  
- `0 <= k <= n - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每个节点当作星形的中心**，然后把它的所有相邻节点（邻居）列出来，**枚举所有可能的子集**，挑出子集大小 ≤ k（即最多 k 条边）的那几个邻居，算出中心节点 + 这些邻居的值之和，取所有中心的最大值。

- **数据结构**：  
  - **邻接表**（`list of lists`）就像一本“社交名录”，下标是人的编号，里面的列表存放他的所有朋友。  
  - **子集**可以用 `itertools.combinations` 生成，就像把朋友们排成一排，挑出若干个人来一起参加聚会。

- **为什么正确**：  
  我们把 **每一种合法的星形**（中心 + 任意 ≤ k 条边）都枚举一遍，求出它们的星和。最大值自然就是答案。

- **时间/空间复杂度**：  
  - 对于度为 `d` 的节点，需要检查 `C(d,0)+C(d,1)+…+C(d,k)` 种子集。最坏情况下 `d` 可能接近 `n`，而 `k` 也可能接近 `n`，于是复杂度会爆炸到 **指数级**，记作 `O( Σ C(d_i, ≤k) ) ≈ O(2^n)`。  
  - 空间上只需要保存邻接表和临时的子集，都是 `O(n+m)`，其中 `m` 是边数。

> 大白话：`O(2^n)` 意味着如果节点有 20 个，就已经需要检查超过一百万种组合；节点 30 个时，组合数就接近十亿，根本跑不完。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def maxStarSum_bruteforce(vals: List[int], edges: List[List[int]], k: int) -> int:
    n = len(vals)
    # 建立邻接表：下标 i 的列表保存 i 的所有邻居
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    best = -10**9  # 题目保证至少有一个节点，初始化为很小的数

    # 对每个节点尝试所有合法的邻居子集
    for center in range(n):
        neighbors = g[center]
        # 先算只保留中心本身的星和（不选任何邻居）
        best = max(best, vals[center])

        # 枚举子集大小 1~k
        for sz in range(1, min(k, len(neighbors)) + 1):
            for comb in combinations(neighbors, sz):
                cur = vals[center] + sum(vals[v] for v in comb)
                best = max(best, cur)
    return best
```

> 这段代码可以跑通 **非常小** 的数据（比如 n ≤ 15），但在正式测评里会因为超时而被判为错误。

#### 复杂度

- **时间复杂度**：`O( Σ_{i=0}^{n-1} Σ_{s=0}^{k} C(deg(i), s) )`，在最坏情况下约等于 `O(2^n)`，指数级增长，几乎不可能在 10⁵ 规模的数据上跑完。  
- **空间复杂度**：`O(n + m)`，只存邻接表和少量临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于 **枚举所有邻居子集**。其实我们并不需要穷举，原因很简单：

1. **我们可以随时停下来**：星形的边数上限是 `k`，但**不必恰好用满 k 条**。如果某个邻居的值是负的，加入它只会让总和更小，我们完全可以不选它。  
2. **只关心“最大的”邻居**：要让星和最大，就应该挑 **值最大的邻居**（因为每条边的贡献就是邻居的 `vals`），而且最多挑 `k` 条。

于是，对于每个中心节点：

- 把它的所有邻居的 `vals` **取出来**。  
- **只保留正数**（负数直接丢掉，因为可以不选）。  
- **挑出最大的至多 k 个**。这一步可以通过 **排序**（降序）或 **维护大小为 k 的最小堆** 完成。  
- 计算 `center_val + sum(chosen_neighbors)`，更新全局最大。

> 类比：把每个人的朋友看成“礼物”，价值越高的礼物越值得带到聚会。我们最多只能带 `k` 件礼物，但如果某件礼物是破烂（价值负），我们宁愿不带。

**核心算法 / 数据结构**  

- **邻接表**：快速得到每个节点的所有邻居。  
- **排序或堆**：在每个邻接列表中挑出前 `k` 大的正值。  
  - 对于 `deg` 很小的节点，直接排序 (`O(deg log deg)`) 更简单。  
  - 对于 `deg` 很大的节点，使用大小为 `k` 的最小堆可以把时间降到 `O(deg log k)`。本题 `n,m ≤ 10⁵`，直接排序已经足够快。

**步骤细化**  

1. 构造邻接表 `g`（`O(n+m)`）。  
2. 初始化答案 `ans = max(vals)`，因为即使没有边，单独一个节点也是合法的星形。  
3. 对每个节点 `i`：  
   - 收集 `vals[neighbor]`（只要 > 0）。  
   - 若收集的正值数量大于 `k`，只保留最大的 `k` 个（排序后切片或堆）。  
   - 计算 `candidate = vals[i] + sum(top_k_vals)`。  
   - `ans = max(ans, candidate)`。  
4. 返回 `ans`。

#### 代码（Python）

```python
from typing import List
import heapq

def maxStarSum(vals: List[int], edges: List[List[int]], k: int) -> int:
    n = len(vals)
    # 1️⃣ 建邻接表
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 2️⃣ 最少也可以只选中心本身
    ans = max(vals)                     # 单节点星形的最大值

    # 3️⃣ 对每个中心尝试选 k 个最有价值的正邻居
    for i in range(n):
        # 收集所有正价值的邻居
        pos_vals = [vals[v] for v in g[i] if vals[v] > 0]

        if not pos_vals:                     # 没有正邻居，直接跳过
            continue

        # 只需要前 k 大的正值
        if len(pos_vals) > k:
            # 方法一：排序（代码更直观）
            pos_vals.sort(reverse=True)      # 降序
            top_k = pos_vals[:k]
            # 方法二：如果想省点时间，可以改成最小堆
            # top_k = heapq.nlargest(k, pos_vals)
        else:
            top_k = pos_vals                  # 全部都可以用

        candidate = vals[i] + sum(top_k)     # 中心 + 选中的邻居
        ans = max(ans, candidate)

    return ans
```

> **关键行中文注释** 已经写在代码里，帮助初学者快速定位每一步的作用。

#### 复杂度

- **时间复杂度**  
  - 建图：`O(n + m)`。  
  - 对每个节点：遍历其邻居一次得到正值 → `O(m)`（所有邻居只遍历一次）。  
  - 对每个节点的正值列表进行排序：如果总正值数量记为 `P`，排序代价为 `Σ O(d_i log d_i)`，其中 `d_i` 是第 `i` 个节点的正邻居数。  
  - 在最坏情况下 `P ≤ m`，所以总体时间是 `O(m log m)`，在本题的约束（`m ≤ 10⁵`）下完全可接受。  
  - 若使用 `heapq.nlargest(k, …)`，每个节点的代价是 `O(d_i log k)`，整体降为 `O(m log k)`，在 `k` 很小的情况下更快。

- **空间复杂度**  
  - 邻接表 `O(n + m)`。  
  - 额外的正值列表在每次循环中最多保存一个节点的邻居，最多 `O(max degree)`，总计仍是 `O(n + m)`。  
  - 整体是线性空间，符合 10⁵ 规模的要求。

> 与暴力解对比：  
> - 暴力解的时间是指数级 `O(2^n)`，根本不可能在大数据上跑完。  
> - 最优解只需要 `O(m log m)`（或 `O(m log k)`），在 10⁵ 规模下几乎是瞬间完成。

---

## 心得

- **核心技巧**：**只取正值的前 k 大邻居**。这是一种 **贪心 + 局部排序** 的思路：在每个局部子问题（以某节点为中心）中，只保留对目标（最大星和）有贡献的“最好”几个元素。  
- **适用的题型**（类似思路）  
  1. **Maximum Sum of a Subset with Size Constraint**（如 LeetCode 1343 “Maximum Sum of a Subset With No Adjacent Elements” 需要挑最大的不相邻元素）。  
  2. **Maximum Beauty of a Garden**（挑出价值最高的 k 条边/点）。  
  3. **Maximum Points From Grid with K Moves**（在每一步只挑最有价值的 k 条路径）。  
- **一句话总结解题钥匙**：**“只要不选负的，就选最大的 k 个”。**

---

## 反思

- **拿到题目第一反应**：先把每个节点的所有邻居枚举组合，像暴力搜索那样“一次性算完”。  
- **最容易踩的坑**  
  - **负数邻居**：忘记可以直接不选，导致把所有邻居都硬塞进星形，答案被错误地压低。  
  - **k = 0**：特殊情况——星形只能是单个节点，代码里要确保不会因为切片 `[:0]` 而出错。  
  - **孤立节点**：没有任何邻居时，答案只能是该节点本身的值。  
- **下次遇到同类题，第一步该想到**：**“是否可以只挑‘价值最大的若干个’而不必枚举所有组合？”**——这往往暗示可以用排序、堆或贪心来把指数级搜索降到线性或对数级。