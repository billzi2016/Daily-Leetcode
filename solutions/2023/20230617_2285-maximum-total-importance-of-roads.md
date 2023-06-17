# #2285. 道路的最大总重要性 / Maximum Total Importance of Roads

> 难度：中等 · 标签：Greedy、Graph、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-total-importance-of-roads/)

---

## 题目（英文原版）

**Description**

You are given an integer n denoting the number of cities in a country. The cities are numbered from 0 to n - 1.
You are also given a 2D integer array roads where roads[i] = [ai, bi] denotes that there exists a bidirectional road connecting cities ai and bi.
You need to assign each city with an integer value from 1 to n, where each value can only be used once. The importance of a road is then defined as the sum of the values of the two cities it connects.
Return the maximum total importance of all roads possible after assigning the values optimally.

**Examples**

**Example 1:**

```
Input: n = 5, roads = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]
Output: 43
Explanation: The figure above shows the country and the assigned values of [2,4,5,3,1].
- The road (0,1) has an importance of 2 + 4 = 6.
- The road (1,2) has an importance of 4 + 5 = 9.
- The road (2,3) has an importance of 5 + 3 = 8.
- The road (0,2) has an importance of 2 + 5 = 7.
- The road (1,3) has an importance of 4 + 3 = 7.
- The road (2,4) has an importance of 5 + 1 = 6.
The total importance of all roads is 6 + 9 + 8 + 7 + 7 + 6 = 43.
It can be shown that we cannot obtain a greater total importance than 43.
```

**Example 2:**

```
Input: n = 5, roads = [[0,3],[2,4],[1,3]]
Output: 20
Explanation: The figure above shows the country and the assigned values of [4,3,2,5,1].
- The road (0,3) has an importance of 4 + 5 = 9.
- The road (2,4) has an importance of 2 + 1 = 3.
- The road (1,3) has an importance of 3 + 5 = 8.
The total importance of all roads is 9 + 3 + 8 = 20.
It can be shown that we cannot obtain a greater total importance than 20.
```

**Constraints**

- 2 <= n <= 5 * 104
- 1 <= roads.length <= 5 * 104
- roads[i].length == 2
- 0 <= ai, bi <= n - 1
- ai != bi
- There are no duplicate roads.

---

## 题目（中文翻译）

给定一个整数 `n`，表示一个国家的城市数量，城市编号为 `0` 到 `n - 1`。  
同时给定一个二维整数数组 `roads`，其中 `roads[i] = [a_i, b_i]` 表示存在一条双向道路（bidirectional road）连接城市 `a_i` 和城市 `b_i`。  

你需要为每个城市分配一个唯一的整数值，取值范围为 `1` 到 `n`（每个值只能使用一次）。道路的**重要性**（importance）定义为该道路两端城市分配值的和。  

返回在最优分配下，所有道路重要性的**最大总和**（maximum total importance）。

**示例 1**

```text
Input: n = 5, roads = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]
Output: 43
Explanation: 如图所示，城市的分配值为 [2,4,5,3,1]。
- 道路 (0,1) 的重要性为 2 + 4 = 6。
- 道路 (1,2) 的重要性为 4 + 5 = 9。
- 道路 (2,3) 的重要性为 5 + 3 = 8。
- 道路 (0,2) 的重要性为 2 + 5 = 7。
- 道路 (1,3) 的重要性为 4 + 3 = 7。
- 道路 (2,4) 的重要性为 5 + 1 = 6。
所有道路的重要性之和为 6 + 9 + 8 + 7 + 7 + 6 = 43。
... (已截断)
```

**示例 2**

```text
Input: n = 5, roads = [[0,3],[2,4],[1,3]]
Output: 20
Explanation: 如图所示，城市的分配值为 [4,3,2,5,1]。
- 道路 (0,3) 的重要性为 4 + 5 = 9。
- 道路 (2,4) 的重要性为 2 + 1 = 3。
- 道路 (1,3) 的重要性为 3 + 5 = 8。
所有道路的重要性之和为 9 + 3 + 8 = 20。
可以证明不存在更大的总重要性。
... (已截断)
```

**约束条件**

- `2 <= n <= 5 * 10^4`
- `1 <= roads.length <= 5 * 10^4`
- `roads[i].length == 2`
- `0 <= a_i, b_i <= n - 1`
- `a_i != b_i`
- 不存在重复的道路。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **所有可能的城市编号排列** 都枚举一遍，算出每种排列对应的道路重要度总和，取最大的那个。  

- **数据结构**：我们可以用一个长度为 `n` 的列表 `val` 来存放城市的编号（即 1~n 的一个排列），用 `roads` 本身记录道路。  
- **生活化类比**：把城市想成“学生”，给每个学生发一张编号卡（1~n），每条道路就是两位学生一起完成的作业，作业的分数等于两张卡号的和。我们想把卡号发得最“聪明”，让所有作业的总分最高。最笨的办法就是把所有发卡方式（排列）都尝试一次。  
- **为什么正确**：因为我们穷举了 **所有** 合法的编号分配方式，答案必然在其中，所以取最大值一定得到最优解。  

但是，这种做法在规模稍大的情况下会失效——  

- **排列的数量**是 `n!`（阶乘），即使 `n=10` 也有 3.6 百万种，`n=15` 就是 1.3 万亿！远远超出计算机的承受范围。  

#### 代码（Python）

```python
import itertools
from typing import List

def maximumImportance_bruteforce(n: int, roads: List[List[int]]) -> int:
    # 所有 1~n 的排列
    best = 0
    for perm in itertools.permutations(range(1, n + 1)):
        # perm[i] 表示城市 i 的编号
        total = 0
        for a, b in roads:
            total += perm[a] + perm[b]          # 道路重要度 = 两端城市的编号之和
        best = max(best, total)                 # 记录最大值
    return best
```

> 代码仅供思考，`itertools.permutations` 会在 `n>8` 时几乎卡死。

#### 复杂度  

- **时间复杂度**：`O(n! * m)`（`m` 为道路数量），因为要遍历 `n!` 种排列，每种排列要遍历所有道路求和。  
  - **大白话**：这意味着随着城市数量稍微增加，计算时间会呈“炸弹式”增长，根本不可用。  
- **空间复杂度**：`O(n)`，主要是存放当前排列的列表。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于遍历所有排列**。我们需要找到一种不枚举、直接就能得到最优分配的方法。  

观察道路重要度的公式：

\[
\text{total} = \sum_{(u,v)\in \text{roads}} (value_u + value_v)
\]

把所有道路的贡献展开：

\[
\text{total} = \sum_{i=0}^{n-1} value_i \times deg(i)
\]

其中 `deg(i)` 表示城市 `i` 的 **度**（有多少条道路连到它）。  

- **类比**：把每条道路想成“一根绳子”，每根绳子两头挂着两个城市的编号卡。所有绳子的总分就是每个城市的编号乘以它被几根绳子拉了多少次（度），再把所有城市的贡献相加。  

**关键结论**：要让总分最大，只要把 **大的编号分配给度大的城市**，小的编号分配给度小的城市即可。  

这正是一个典型的 **贪心** 思路：  

1. 先统计每个城市的度 `deg[i]`（可以用数组记录，遍历 `roads` 一遍即可）。  
2. 把城市按照度从大到小排序。  
3. 把编号 `n, n-1, …, 1` 按照同样的顺序分配给排好序的城市。  
4. 最后再遍历所有道路，用分配好的编号求和即可得到最大总重要度。  

> 为什么这种贪心是最优的？  
> 把两个城市 `x, y` 的编号分别设为 `a, b (a>b)`，而它们的度分别是 `dx, dy (dx<dy)`。如果我们把大的编号 `a` 给了度小的城市 `x`，则贡献为 `a*dx + b*dy`。  
> 交换后得到的贡献是 `a*dy + b*dx`。因为 `a>b` 且 `dy>dx`，有  
> `a*dy + b*dx > a*dx + b*dy`，即交换后更大。  
> 这正是 **“大数配大权”** 的原理，说明把大编号放在大度上永远不亏。  

#### 代码（Python）

```python
from typing import List

def maximumImportance(n: int, roads: List[List[int]]) -> int:
    # 1. 统计每个城市的度（有几条路连到它）
    degree = [0] * n
    for u, v in roads:
        degree[u] += 1          # u 多了一条相邻的路
        degree[v] += 1          # v 多了一条相邻的路

    # 2. 按度从大到小排序城市的下标
    #    sorted 返回的是下标列表，例如 [3,0,2,1,4] 表示城市 3 度最大，依次往后
    order = sorted(range(n), key=lambda i: degree[i], reverse=True)

    # 3. 按排序顺序分配最大编号（n, n-1, ... , 1）
    value = [0] * n               # value[i] 最终存放城市 i 的编号
    cur = n                       # 当前最大的可用编号
    for idx in order:
        value[idx] = cur
        cur -= 1

    # 4. 计算所有道路的总重要度
    total = 0
    for u, v in roads:
        total += value[u] + value[v]

    return total
```

> 代码每一步都有中文注释，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n log n + m)`  
  - 统计度需要遍历 `roads` 一次，`O(m)`。  
  - 对 `n` 个城市排序需要 `O(n log n)`（排序的常规复杂度）。  
  - 最后再遍历一次 `roads` 计算总和，`O(m)`。  
  - 与暴力解的 `n!` 相比，指数级的增长被降到了 **线性或对数** 级，能轻松处理 `n, m ≤ 5·10⁴` 的规模。  
- **空间复杂度**：`O(n)`  
  - 额外使用了 `degree`、`order`、`value` 三个长度为 `n` 的数组。  

---

## 心得  

- **核心技巧**：把每条边的贡献拆解为 “城市编号 × 该城市的度”，于是问题转化为 “把大数分配给大权”。这是一种 **贪心 + 排序** 的思路。  
- **适用的题型**  
  1. “Maximum Total Importance of Roads”（本题）  
  2. “Maximum Sum of Scores of Children”——把高分配给拥有更多朋友的孩子。  
  3. “Maximum Profit of Assigning Tasks”——任务的权重（如出现次数）决定先给高报酬的任务。  
- **一句话总结解题钥匙**：**“度大的城市配大的编号”**，即“大数配大权”。  

---

## 反思  

- **第一反应**：看到“每条道路的价值是两端城市编号之和”，马上想到枚举所有编号排列求最大。  
- **最容易踩的坑**  
  - 忽视 **度** 的概念，导致没有看到可以把问题拆成线性求和的形式。  
  - 在实现时忘记把 **编号从 1 开始**，导致结果偏小。  
  - 边界条件：`n` 可能很大，若使用 `itertools.permutations` 或递归暴力会直接超时/内存溢出。  
- **下次遇到同类题**：第一步先 **写出总价值的数学表达式**，看能否把它拆成「每个元素 × 权重」的形式；若能，往往可以用 **排序 + 贪心** 来得到最优解。