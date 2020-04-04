# #826. **最大利润分配工作** / Most Profit Assigning Work

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/most-profit-assigning-work/)

---

## 题目（英文原版）

**Description**

You have n jobs and m workers. You are given three arrays: difficulty, profit, and worker where:
Every worker can be assigned at most one job, but one job can be completed multiple times.
Return the maximum profit we can achieve after assigning the workers to the jobs.

**Examples**

**Example 1:**

```
Input: difficulty = [2,4,6,8,10], profit = [10,20,30,40,50], worker = [4,5,6,7]
Output: 100
Explanation: Workers are assigned jobs of difficulty [4,4,6,6] and they get a profit of [20,20,30,30] separately.
```

**Example 2:**

```
Input: difficulty = [85,47,57], profit = [24,66,99], worker = [40,25,25]
Output: 0
```

**Constraints**

- n == difficulty.length
- n == profit.length
- m == worker.length
- 1 <= n, m <= 104
- 1 <= difficulty[i], profit[i], worker[i] <= 105

---

## 题目（中文翻译）

给定 `n` 个工作和 `m` 名工人。你会得到三个数组：**难度（difficulty）**、**利润（profit）** 和 **工人（worker）**，其中：

- 每名工人至多可以被分配到一个工作；
- 同一个工作可以被多名工人完成（即可以被重复分配）。

返回在为工人分配工作后能够获得的最大总利润。

**示例 1**  
**输入**  
```text
difficulty = [2,4,6,8,10], profit = [10,20,30,40,50], worker = [4,5,6,7]
```  
**输出**  
```text
100
```  
**解释**：工人分别被分配到难度为 `[4,4,6,6]` 的工作，获得的利润分别是 `[20,20,30,30]`，总和为 100。

**示例 2**  
**输入**  
```text
difficulty = [85,47,57], profit = [24,66,99], worker = [40,25,25]
```  
**输出**  
```text
0
```  

**约束条件**

- `n == difficulty.length`
- `n == profit.length`
- `m == worker.length`
- `1 <= n, m <= 10^4`
- `1 <= difficulty[i], profit[i], worker[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历每个工人，找出他能做的所有工作中利润最大的那一个**。  
具体步骤如下：

1. 对每个 `worker[i]`（工人的能力），遍历所有 `job`（用 `difficulty[j]` 表示工作难度）  
   - 如果 `difficulty[j] ≤ worker[i]`，说明该工人可以完成这份工作。  
   - 记录这些可做工作的利润 `profit[j]`，取最大值即为该工人的收益。  
2. 把所有工人的收益相加，得到总利润。

> **类比**：把 `difficulty` 看作“门槛”，`profit` 看作“门后奖品”。每个工人手里拿着一把钥匙（能力），只能打开 **等于或小于** 这把钥匙的门。我们让每个工人挑选门后价值最高的奖品。

> **正确性**：因为每个工人只能挑选 **一份** 工作，而我们在所有可选工作中挑了最高利润的，显然不可能再选出更好的组合（不影响其他工人，因为工作可以被重复完成）。

#### 代码（Python）

```python
from typing import List

def maxProfitAssignment_brute(difficulty: List[int],
                             profit: List[int],
                             worker: List[int]) -> int:
    total = 0                         # 累计所有工人的利润
    n = len(difficulty)               # 工作数量

    for w in worker:                  # 遍历每个工人
        best = 0                      # 当前工人能拿到的最大利润，默认 0（可能什么工作都做不了）
        for i in range(n):           # 遍历所有工作
            if difficulty[i] <= w:   # 工作难度不超过工人能力，说明可以做
                if profit[i] > best: # 取更大的利润
                    best = profit[i]
        total += best                 # 把该工人的最佳利润加入总和
    return total
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - `m` 是工人数，`n` 是工作数量。对每个工人我们都要遍历全部工作。  
  - 大白话：如果有 10 000 个工人和 10 000 份工作，最坏情况下要做 1 亿 次比较，明显会超时。

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（`total`、`best`、循环计数器），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“每个工人都遍历所有工作”**，导致 `O(m·n)`。  
我们可以把工作按照难度从小到大排好序，这样 **难度更大的工作一定在后面**，于是可以用 **一次遍历 + 双指针**（或二分查找）把每个工人的最佳利润直接找出来。

核心想法：

1. **把工作配对**  
   - 将 `difficulty[i]` 与 `profit[i]` 组成 `(难度, 利润)` 的元组，放进列表 `jobs`。  
   - 按 **难度升序** 排序。如果两个工作难度相同，保留更大的利润（后面会统一处理）。

2. **预处理最大利润前缀**  
   - 依次遍历排好序的 `jobs`，维护一个变量 `max_profit_sofar`，它始终是 **截至当前难度的最大利润**。  
   - 用 `max_profit[i]` 记录到第 `i` 个工作为止的最大利润。这样对任何给定的难度阈值，都能在 `O(1)` 时间得到“≤该难度的最大利润”。

   > 类比：把每个难度点视为“一条路口”，我们在走路的过程中把“路口的最高奖品”记下来，后面再来查询时直接看记忆表。

3. **为每个工人二分查找**  
   - 把 `worker` 数组也排序（不必保持原顺序，只要累计利润即可）。  
   - 对每个工人的能力 `w`，使用二分查找在 `jobs` 的难度数组中找到 **最右侧** 那个 `difficulty ≤ w` 的位置 `idx`。  
   - 该位置对应的 `max_profit[idx]` 就是该工人能得到的最大利润。

4. **累计答案**  
   - 将所有工人的利润相加即为答案。

**为什么这样更快？**  
- 排序一次 `O(n log n)`（工作）和 `O(m log m)`（工人）。  
- 预处理前缀最大利润是线性 `O(n)`。  
- 对每个工人只做一次二分查找 `O(log n)`，总计 `O(m log n)`。  
- 综合下来时间复杂度是 `O((n+m) log n)`，远小于暴力的 `O(m·n)`。

#### 代码（Python）

```python
from typing import List
import bisect

def maxProfitAssignment(difficulty: List[int],
                        profit: List[int],
                        worker: List[int]) -> int:
    # 1️⃣ 把工作配对并按难度排序
    jobs = sorted(zip(difficulty, profit), key=lambda x: x[0])
    # jobs = [(2,10), (4,20), (6,30), (8,40), (10,50)]

    # 2️⃣ 预处理前缀最大利润
    max_profit = []          # max_profit[i] = 到第 i 个工作为止的最大利润
    cur_max = 0
    for d, p in jobs:
        cur_max = max(cur_max, p)   # 取更大的利润
        max_profit.append(cur_max)

    # 为二分查找准备一个只包含难度的列表
    difficulties = [d for d, _ in jobs]

    # 3️⃣ 为每个工人寻找能做的最高利润
    total = 0
    for w in worker:
        # bisect_right 返回第一个 > w 的位置，下标-1 即为 ≤ w 的最后一个位置
        idx = bisect.bisect_right(difficulties, w) - 1
        if idx >= 0:                     # 至少有一份工作能做
            total += max_profit[idx]     # 累加该工人能得到的最大利润
        # 若 idx < 0，说明工人的能力连最简单的工作都达不到，利润为 0，直接跳过

    return total
```

#### 复杂度  

- **时间复杂度**：`O((n + m) log n)`  
  - `n` 为工作数，`m` 为工人数。  
  - 排序 `O(n log n)` + `O(m log m)`（如果把 `worker` 也排序），随后每个工人二分 `O(log n)`，总计 `O((n+m) log n)`。  
  - 与暴力解的 `O(m·n)` 相比，若 `n,m` 均为 10⁴，最坏情况下从 10⁸ 次降到约 `10⁴·log10⁴ ≈ 1.3×10⁵` 次，提升巨大。

- **空间复杂度**：`O(n)`  
  - 需要额外存储排序后的 `jobs`、`difficulties` 与 `max_profit`，大小均与工作数 `n` 成线性关系。  
  - 这只是把原始数据重新组织，并没有随 `m` 增长的额外空间。

---

## 心得

- **核心技巧**：先对工作按难度排序，再用前缀最大利润 + 二分查找，完成 **“对于每个查询（工人能力），快速得到 ≤阈值的最优值”**。  
- **适用的题型**  
  1. “**查询 ≤ 某值的最大/最小**” 类问题（如 LeetCode 1847 `ClosestRoom`）。  
  2. “**区间最大值**” 需要离线处理的场景（如 1223 `Dice Roll Simulation` 的变体）。  
  3. “**在已排序数组中找最近的满足条件的元素**” （如 33 `Search in Rotated Sorted Array` 的变形）。  
- **一句话总结**：把“求每个工人的最佳工作”转化为“在已排序的工作难度上做一次二分”，并提前记住每个难度对应的最高利润。

---

## 反思

- **第一反应**：看到“每个工人只能做一份工作”，自然想到逐个遍历找最大利润——就是暴力解。  
- **最容易踩的坑**  
  1. **同一难度的工作利润不一定递增**，需要在预处理时取**全局最大**而不是只取当前工作利润。  
  2. **二分查找返回的位置**：`bisect_right` 与 `bisect_left` 的区别要弄清楚，错误的下标会导致越界或选错利润。  
  3. **工人能力低于所有工作难度** 时，`idx` 为 `-1`，一定要判断后再取利润，否则会报错。  
- **下次遇到同类题**：第一步先 **排序 + 预处理前缀最值**，然后把每个“查询”转化为二分/指针扫描，这样时间自然会从指数级下降到对数级。