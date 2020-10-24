# #1029. 两个城市调度 / Two City Scheduling

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/two-city-scheduling/)

---

## 题目（英文原版）

**Description**

A company is planning to interview 2n people. Given the array costs where costs[i] = [aCosti, bCosti], the cost of flying the ith person to city a is aCosti, and the cost of flying the ith person to city b is bCosti.
Return the minimum cost to fly every person to a city such that exactly n people arrive in each city.

**Examples**

**Example 1:**

```
Input: costs = [[10,20],[30,200],[400,50],[30,20]]
Output: 110
Explanation: 
The first person goes to city A for a cost of 10.
The second person goes to city A for a cost of 30.
The third person goes to city B for a cost of 50.
The fourth person goes to city B for a cost of 20.

The total minimum cost is 10 + 30 + 50 + 20 = 110 to have half the people interviewing in each city.
```

**Example 2:**

```
Input: costs = [[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]]
Output: 1859
```

**Example 3:**

```
Input: costs = [[515,563],[451,713],[537,709],[343,819],[855,779],[457,60],[650,359],[631,42]]
Output: 3086
```

**Constraints**

- 2 * n == costs.length
- 2 <= costs.length <= 100
- costs.length is even.
- 1 <= aCosti, bCosti <= 1000

---

## 题目（中文翻译）

**描述**  
一家公司计划面试 `2n` 个人。给定数组 `costs`，其中 `costs[i] = [aCost_i, bCost_i]` 表示将第 `i` 个人飞往城市 **A** 的费用为 `aCost_i`，飞往城市 **B** 的费用为 `bCost_i`。  
返回使得每个人都被安排飞往某个城市且恰好有 `n` 个人到达每个城市的最小总费用。

**示例 1**  
```
Input: costs = [[10,20],[30,200],[400,50],[30,20]]
Output: 110
Explanation: 
The first person goes to city A for a cost of 10.
The second person goes to city A for a cost of 30.
The third person goes to city B for a cost of 50.
The fourth person goes to city B for a cost of 20.

The total minimum cost is 10 + 30 + 50 + 20 = 110 to have half the people interviewing in each city.
```

**示例 2**  
```
Input: costs = [[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]]
Output: 1859
```

**示例 3**  
```
Input: costs = [[515,563],[451,713],[537,709],[343,819],[855,779],[457,60],[650,359],[631,42]]
Output: 3086
```

**约束条件**  
- `2 * n == costs.length`
- `2 <= costs.length <= 100`
- `costs.length` 为偶数。
- `1 <= aCost_i, bCost_i <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每个人都枚举一次，决定他去 A 城还是 B 城**，只要满足“恰好有 n 个人去 A，n 个人去 B”，就算出对应的花费，取最小值即可。

实现上可以：

1. 先从 `2n` 个人里挑出 `n` 个人去 A 城（其余的自然去 B 城）。  
   - 这一步相当于在 `2n` 个元素中选 `n` 个的组合，类似“从 10 本书里挑出 5 本”。在编程里可以用 `itertools.combinations` 完成。  
2. 对每一种挑选方式，累计 A 城的费用 `aCost`（选中的人）和 B 城的费用 `bCost`（未选中的人），得到总花费。  
3. 记录所有组合的最小花费，即为答案。

> **类比**：把 `costs` 看成一本词典，`aCost`、`bCost` 是每个词对应的两页内容。暴力解相当于把所有可能的“挑哪页”的方式都列出来，再找出最省纸的那一种。

**为什么正确**：遍历了所有合法的分配方式，必然包含最优的那一种，取最小自然得到最优解。

#### 代码（Python）
```python
from itertools import combinations
from typing import List

def twoCitySchedCost_bruteforce(costs: List[List[int]]) -> int:
    n = len(costs) // 2                     # 每个城市需要的人数
    min_total = float('inf')                # 初始设为无穷大

    # 选出 n 个人去城市 A，剩下的自动去城市 B
    for a_indices in combinations(range(2 * n), n):
        total = 0
        a_set = set(a_indices)              # 为了 O(1) 判断某人是否在 A 城

        for i, (a, b) in enumerate(costs):
            if i in a_set:                  # 去 A 城
                total += a
            else:                           # 去 B 城
                total += b

        min_total = min(min_total, total)   # 维护最小花费

    return min_total
```

#### 复杂度
- **时间复杂度**：`O( C(2n, n) * n )`  
  `C(2n, n)` 是组合数，表示所有挑 `n` 个人的方式，约等于 `≈ 4^n / √(π n)`，随 `n` 指数级增长。每种组合我们遍历 `2n`（即 `n`）个人累加费用，所以整体是指数级的，实际只能用于 `n ≤ 10` 左右的小数据。
- **空间复杂度**：`O(n)`  
  主要是存放当前组合的索引集合 `a_set`，规模为 `n`。除此之外使用的额外空间均为常数。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**枚举所有可能的分配**，这会导致指数级时间。我们需要找出一个“贪心”原则，只做一次决策即可得到最优解。

观察每个人去 A 城和去 B 城的费用差值：

```
diff_i = aCost_i - bCost_i
```

- `diff_i` 为正，说明去 A 城比去 B 城贵（更倾向于送 B）。
- `diff_i` 为负，说明去 A 城更便宜（更倾向于送 A）。

**核心贪心想法**：  
把“更应该去 A 城”的人排在前面，把“更应该去 B 城”的人排在后面。于是：

1. 计算所有人的 `diff = aCost - bCost`。  
2. 按 `diff` **从小到大**（即从最负到最正）排序。  
   - 排在前面的 `n` 个人，说明他们去 A 城能省下最多钱（因为 `aCost` 相对 `bCost` 更低）。  
   - 剩下的 `n` 个人自然去 B 城。  
3. 累加对应的费用，即得到最小总花费。

> **类比**：把每个人看成一张“优惠券”。`diff` 越小（越负），这张券在 A 城的折扣越大，越值得在 A 用。我们把折扣最大的 `n` 张券先用在 A，剩下的用在 B，就能省钱。

**为什么贪心有效**：  
设想已经排好序，若把某个排在前面的、应该去 A 的人换成排在后面的、应该去 B 的人，会让总费用增加（因为前面那个人在 A 更便宜，后面那个人在 B 更便宜）。这正是交换论证的核心，说明排序后前 `n` 去 A、后 `n` 去 B 必然是最优的。

#### 代码（Python）
```python
from typing import List

def twoCitySchedCost(costs: List[List[int]]) -> int:
    # 计算每个人去 A、B 的费用差值
    # diff 越小（越负），说明越应该去 A 城
    diffs = [(a - b, a, b) for a, b in costs]

    # 按 diff 从小到大排序
    diffs.sort(key=lambda x: x[0])

    n = len(costs) // 2
    total = 0

    # 前 n 个人送往 A 城
    for i in range(n):
        total += diffs[i][1]   # aCost

    # 后 n 个人送往 B 城
    for i in range(n, 2 * n):
        total += diffs[i][2]   # bCost

    return total
```

#### 复杂度
- **时间复杂度**：`O(n log n)`  
  主要耗时在对 `2n` 条记录按差值排序，排序的时间是 `n log n`（这里的 `n` 实际是 `2n`，常数不影响量级）。排序后只需线性遍历一次求和，故整体是对数线性级。
- **空间复杂度**：`O(n)`  
  需要额外的列表保存 `(diff, a, b)` 三元组，规模为 `2n`，即 `O(n)`。如果在原数组上就地计算 `diff` 并排序，则可以降到 `O(1)` 额外空间。

---

## 心得

- **核心技巧**：**基于费用差值的贪心排序**。先把“相对更适合去 A 城”的人挑出来，再把其余的人送往 B 城。
- **适用的题型**  
  1. **Two City Scheduling**（本题）  
  2. **Maximum Profit in Job Scheduling**（根据收益差值排序）  
  3. **Assign Cookies**（根据需求大小排序的贪心）  
- **一句话总结解题钥匙**：**用“差值”衡量倾向，排序后直接分配即可**。

---

## 反思

- **第一反应**：直接想到枚举所有可能的分配，因为这样最安全、最直观。  
- **最容易踩的坑**  
  - 忘记 **恰好** `n` 人去每个城市，导致出现不平衡的分配。  
  - 在实现贪心时，误把 `diff = a - b` 按 **降序** 排序，导致前 `n` 人实际上更适合去 B 城，答案会翻倍。  
  - 忽视 `costs` 长度是偶数的前提，直接用 `len(costs)//2` 而不检查，会在非法输入时出错。  
- **下次遇到同类题**：第一步先**计算每个选项的相对优势（差值）**，看能否通过排序一次性决定最优分配；如果不能排序，再考虑 DP 或搜索。