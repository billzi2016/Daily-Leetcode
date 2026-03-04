# #3547. 图中边值的最大和 / Maximum Sum of Edge Values in a Graph

> 难度：困难 · 标签：Greedy、Depth-First Search、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-edge-values-in-a-graph/)

---

## 题目（英文原版）

**Description**

You are given an undirected connected graph of n nodes, numbered from 0 to n - 1. Each node is connected to at most 2 other nodes.
The graph consists of m edges, represented by a 2D array edges, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi.
You have to assign a unique value from 1 to n to each node. The value of an edge will be the product of the values assigned to the two nodes it connects.
Your score is the sum of the values of all edges in the graph.
Return the maximum score you can achieve.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[0,1],[1,2],[2,3]]
Output: 23
Explanation:
The diagram above illustrates an optimal assignment of values to nodes. The sum of the values of the edges is: (1 * 3) + (3 * 4) + (4 * 2) = 23 .
```

**Example 2:**

```
Input: n = 6, edges = [[0,3],[4,5],[2,0],[1,3],[2,4],[1,5]]
Output: 82
Explanation:
The diagram above illustrates an optimal assignment of values to nodes. The sum of the values of the edges is: (1 * 2) + (2 * 4) + (4 * 6) + (6 * 5) + (5 * 3) + (3 * 1) = 82 .
```

**Constraints**

- 1 <= n <= 5 * 104
- m == edges.length
- 1 <= m <= n
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- There are no repeated edges.
- The graph is connected.
- Each node is connected to at most 2 other nodes.

---

## 题目（中文翻译）

**题目描述**  
给定一个 **无向连通图**，共有 `n` 个节点，编号为 `0` 到 `n-1`。每个节点至多与 **2 条边** 相连。图由 `m` 条边组成，使用二维数组 `edges` 表示，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条边。  
你需要为每个节点分配一个唯一的整数值，取值范围为 `1` 到 `n`（每个值只能使用一次）。一条边的值定义为其两端节点所分配值的 **乘积**（product）。  
你的得分为图中所有边的值之 **和**（sum）。  
返回你能够得到的 **最大得分**。

**示例 1**  
输入: `n = 4`, `edges = [[0,1],[1,2],[2,3]]`  
输出: `23`  
解释:  
下图展示了一种最优的节点取值方案。边的值之和为  
`(1 * 3) + (3 * 4) + (4 * 2) = 23` 。

**示例 2**  
输入: `n = 6`, `edges = [[0,3],[4,5],[2,0],[1,3],[2,4],[1,5]]`  
输出: `82`  
解释:  
下图展示了一种最优的节点取值方案。边的值之和为  
`(1 * 2) + (2 * 4) + (4 * 6) + (6 * 5) + (5 * 3) + (3 * 1) = 82` 。

**约束条件**  
- `1 <= n <= 5 * 10^4`  
- `m == edges.length`  
- `1 <= m <= n`  
- `edges[i].length == 2`  
- `0 <= a_i, b_i < n`  
- `a_i != b_i`  
- 不存在重复的边。  
- 图是连通的。  
- 每个节点至多与 **2 条边** 相连。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **1 到 n 的所有数全排列**，每一种排列都对应一种给节点编号的方式。  
把每条边的两个端点的编号相乘再相加，就得到该排列的得分，遍历所有排列取最大值。

- **数据结构**：  
  - `perm`：长度为 `n` 的列表，存放当前的排列。可以把它想象成 **一本词典**，每一页（下标）记录了对应的单词（编号），我们要把所有单词的顺序全部列举一遍。  
  - `edges`：原题给出的边列表，像是一张**地图**，告诉我们哪些城市（节点）之间有路（边）。

- **为什么正确**：  
  因为我们把 **所有可能的分配方式** 都尝试了一遍，必然能找到得分最高的那一种。

- **时间/空间复杂度**：  
  - **时间**：排列的数量是 `n!`（n 的阶乘），每次要遍历 `m ≤ n` 条边求和，所以时间是 `O(n! * n)`。  
    - `O(n!)` 可以理解为“**把 n 本书排成一排的所有方法**”，当 n=10 时已经是 3,628,800 种，远远超出计算机在一秒内能做的事。  
  - **空间**：只需要存放一条排列和边列表，`O(n)` 的额外空间。

显然，这种暴力方法只能在 `n ≤ 8` 左右的极小规模上跑得动，根本不适合题目给出的 `n ≤ 5·10⁴`。

#### 代码（Python）

```python
import itertools
from typing import List

def maxScore_bruteforce(n: int, edges: List[List[int]]) -> int:
    best = 0
    # 所有 1..n 的排列
    for perm in itertools.permutations(range(1, n + 1)):
        # 计算当前排列的得分
        cur = 0
        for u, v in edges:               # 对每条边
            cur += perm[u] * perm[v]     # 两端点的编号相乘
        best = max(best, cur)            # 维护最大值
    return best
```

> 这段代码可以直接跑通，但只适合演示思路，实际会因为 `n!` 爆炸而超时。

#### 复杂度  

- **时间复杂度**：`O(n! * n)` —— 需要遍历所有排列，每个排列再遍历 `n` 条边。  
- **空间复杂度**：`O(n)` —— 保存当前排列和边列表。  

---

### 2. 最优解  

#### 思路  

**关键观察**：  
- 题目说每个节点至多连 2 条边，而且图是连通的。  
- 这恰好把图限制成 **“路径”**（两端度为 1，内部度为 2）或 **“环”**（所有度为 2）两种形态。  

**为什么暴力慢**：  
- 暴力在 **所有排列** 上做搜索，而我们只需要在 **节点在图中的相对顺序** 上考虑。  
- 对于路径或环，节点的顺序已经唯一（或只有两个方向），只要把 **1..n** 按某种顺序填进去即可。

**一步步推导**  

1. **把图展成一条线（或环）**  
   - 用邻接表记录每个节点的相邻节点（最多两个）。  
   - 找一个度为 1 的节点作为起点；如果没有（说明是环），随便选一个节点。  
   - 从起点沿着未访问的邻居一步步走，记录遍历顺序 `order`。这一步相当于 **把一根绳子顺着图拉直**，得到节点的线性序列。  

2. **怎么填编号才能让相邻乘积最大？**  
   - 边的贡献是两个相邻节点编号的乘积。  
   - 把大的数放在相邻的位置会让乘积更大。  
   - 这正是 **“重排不等式”**（Rearrangement Inequality）的结论：两个同序（均递增或均递减）的序列对应相乘后求和是最大的。  
   - 因此，把 `1,2,…,n` **按递增（或递减）顺序**映射到 `order` 中即可。  

3. **计算答案**  
   - 已经得到每个节点的值 `val[node]`，再次遍历所有边累加 `val[u] * val[v]` 即可得到最大得分。  

**类比帮助理解**  

- 想象你有一串 **珠子**（节点）已经按顺序串好（路径/环），每颗珠子要贴上 **编号贴纸**（1~n）。  
- 两颗相邻珠子之间有一条细线，线的“价值”是两颗珠子贴纸数字的乘积。  
- 为了让整条线的价值最大，你应该把 **大数字贴在相邻的珠子上**，也就是把贴纸从大到小（或小到大）顺序贴过去。  

#### 代码（Python）

```python
from typing import List

def maxScore(n: int, edges: List[List[int]]) -> int:
    # 1️⃣ 建图（邻接表），每个节点最多两个邻居
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 2️⃣ 找到一条完整的遍历顺序（路径或环）
    #   - 若有度为 1 的节点，则它一定是路径的端点
    start = 0
    for i in range(n):
        if len(g[i]) == 1:          # 找到端点
            start = i
            break

    order = []                      # 记录遍历得到的节点序列
    visited = [False] * n
    cur = start
    prev = -1                       # 上一个节点，帮助避免回头

    while not visited[cur]:
        order.append(cur)
        visited[cur] = True
        # 在邻居里找下一个没有被访问过的（最多两个）
        nxt = None
        for nb in g[cur]:
            if nb != prev:          # 不是从哪里来的那个节点
                nxt = nb
                break
        prev, cur = cur, nxt if nxt is not None else cur

    # 3️⃣ 把 1..n 按递增顺序分配到 order 中（递减同理）
    #    这里直接用 1-indexed 的值，省去再建映射表的步骤
    value = [0] * n                 # value[node] = assigned number
    for idx, node in enumerate(order):
        value[node] = idx + 1       # 第 idx 位对应的数字是 idx+1

    # 4️⃣ 计算所有边的贡献
    ans = 0
    for u, v in edges:
        ans += value[u] * value[v]

    return ans
```

> 代码里每一行都写了中文注释，帮助你一步步对照思路。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 建图、遍历节点、遍历边各只需一次线性扫描。  
  - 与暴力的 `O(n!)` 相比，**线性时间**可以轻松处理 `n = 5·10⁴` 的规模。  

- **空间复杂度**：`O(n)`  
  - 邻接表、访问标记、节点顺序等都需要 `n` 大小的数组。  

---

## 心得  

- **核心技巧**：  
  1. 利用 **度数限制** 把图辨认为 **路径或环**。  
  2. 用 **重排不等式** 说明“把大数相邻放”是最优的。  
  3. 用一次 **DFS/线性遍历** 把节点排成序列，再按递增（递减）填数。

- **适用的题型**（类似思路可复用）：  
  - “最大化相邻乘积” 类的路径/环问题。  
  - “给定序列，要求相邻元素乘积之和最大”，常见于 **排列/贪心**。  
  - “度数上限为 2 的图的最优标号” 这类结构化图论题。

- **一句话总结解题钥匙**：  
  **“先把图摊成一条线（或环），再把大数按顺序排在相邻的位置”。**

---

## 反思  

- **第一反应**：看到“每条边的值是两个节点编号的乘积”，立刻想到“遍历所有排列”——这是一种**暴力枚举**的本能想法。  
- **最容易踩的坑**：  
  - 忽视 **度数 ≤ 2** 的限制，以为是一般图，导致思考路径/环的特性时走弯路。  
  - 在环的情况下忘记两端相连，错误地只考虑单向排列。  
  - 计算时使用 0‑based 编号却直接把 `1..n` 当作下标，产生索引错误。  

- **下次遇到同类题**，第一步应该：  
  **“先分析图的结构（路径/环/树），把问题抽象成序列上的最优排列”。** 这样可以快速定位到贪心或 DP 的方向，避免盲目暴力搜索。