# #2501. 数组中最长的平方序列 / Longest Square Streak in an Array

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/longest-square-streak-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. A subsequence of nums is called a square streak if:
Return the length of the longest square streak in nums, or return -1 if there is no square streak.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [4,3,6,16,8,2]
Output: 3
Explanation: Choose the subsequence [4,16,2]. After sorting it, it becomes [2,4,16].
- 4 = 2 * 2.
- 16 = 4 * 4.
Therefore, [4,16,2] is a square streak.
It can be shown that every subsequence of length 4 is not a square streak.
```

**Example 2:**

```
Input: nums = [2,3,5,6,7]
Output: -1
Explanation: There is no square streak in nums so return -1.
```

**Constraints**

- 2 <= nums.length <= 105
- 2 <= nums[i] <= 105

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`。如果一个 `nums` 的子序列（subsequence）在排序后满足：对于排序后的相邻元素 `x` 与 `y`，都有 `y = x * x`，则称该子序列为 **平方序列**（square streak）。  

返回 `nums` 中最长的平方序列的长度；如果不存在平方序列，则返回 `-1`。  

子序列是指可以通过删除原数组中的若干（也可以不删除）元素而得到的数组，删除操作不会改变剩余元素的相对顺序。

**示例**

*示例 1*  
```
Input: nums = [4,3,6,16,8,2]
Output: 3
Explanation: 选取子序列 [4,16,2]。排序后得到 [2,4,16]，满足  
- 4 = 2 * 2  
- 16 = 4 * 4  
因此 [4,16,2] 是一个平方序列。可以证明，任意长度为 4 的子序列都不是平方序列。
```

*示例 2*  
```
Input: nums = [2,3,5,6,7]
Output: -1
Explanation: nums 中不存在平方序列，故返回 -1。
```

**约束条件**  
- `2 <= nums.length <= 10^5`  
- `2 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子序列**，检查每一个子序列能否在排序后满足「每个数都是前一个数的平方」的条件。  
- **子序列**：相当于从原数组里挑选若干个元素，保持原来的相对顺序。可以把它想成从一串珠子里挑出几颗，珠子之间的顺序不变。  
- **检查是否为 square streak**：先把挑出来的子序列排序（像把挑好的珠子摆成从小到大的顺序），然后看相邻两个数是否满足 `b = a * a`。  

由于数组长度最多 10⁵，子序列的数量是 2ⁿ（指数级），显然不可行。但先写出这种「最笨」的办法，有助于验证思路的正确性。

#### 代码（Python）

```python
from itertools import combinations
from math import isqrt

def longestSquareStreak_bruteforce(nums):
    n = len(nums)
    best = -1                     # 记录目前找到的最长长度，-1 表示不存在

    # 枚举子序列的长度，从大到小可以提前剪枝
    for length in range(n, 1, -1):
        # 组合会保持原数组的相对顺序
        for idxs in combinations(range(n), length):
            subseq = [nums[i] for i in idxs]
            subseq.sort()         # 排序后检查平方关系

            ok = True
            for i in range(1, length):
                if subseq[i] != subseq[i-1] * subseq[i-1]:
                    ok = False
                    break
            if ok:
                return length    # 找到最长的直接返回
    return -1
```

> 关键点说明  
> - `combinations` 会产生所有长度为 `length` 的下标组合，等价于所有子序列。  
> - 排序后只需要一次线性遍历检查 `b = a*a`。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n log n)`（指数级），因为要枚举所有子序列并对每个子序列排序。  
  - 大白话：如果数组有 20 个数，可能要检查 2⁽²⁰⁾ ≈ 1,048,576 种子序列，远远超出时间限制。  
- **空间复杂度**：`O(n)`，主要是存放临时子序列的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点在于如何快速判断“某个数是否可以接在已有的 square streak 后面”。**  
如果我们已经知道某个数 `x` 能构成长度为 `k` 的 square streak（以 `x` 为最后一个元素），那么只要数组里出现 `x*x`，它就可以把 streak 延长为 `k+1`。这正好是**动态规划**的思路：从小到大遍历所有数，记录以每个数结尾的最长 streak。

实现细节如下：

1. **把所有数放进集合**  
   - 哈希表（Python 的 `set`）就像一本“词典”，查询某个单词是否在里边只需要 O(1) 时间。这里 `key` 是数组的数值，`value` 不需要，只要能快速判断“`y` 是否在数组里”。  

2. **对数组去重并排序**  
   - 只需要考虑每个不同的数一次，排序后从小到大处理可以确保在处理 `y = x*x` 时，`x` 已经算完它的最长 streak。  

3. **动态规划数组 `dp`**  
   - `dp[val]` 表示「以 `val` 为结尾的最长 square streak 长度」。初始值都是 1（单独一个数算作长度 1）。  
   - 对每个 `val`，如果 `val` 能被某个整数的平方得到（即 `root = isqrt(val)` 且 `root*root == val`），并且 `root` 在集合中，则 `dp[val] = dp[root] + 1`。  

4. **答案筛选**  
   - 题目要求「长度至少为 2」的 streak，最后取所有 `dp[val] >= 2` 的最大值。如果没有满足条件的，则返回 `-1`。  

**为什么只需要检查 `sqrt(val)` 而不是所有更小的数？**  
因为 square streak 的定义要求相邻两个数必须是「前一个数的平方」，所以 `val` 的前驱只能唯一是 `sqrt(val)`（若它是整数且在数组里）。这把原本可能的 O(n²) 检查压缩到 O(n)。

#### 代码（Python）

```python
import math
from typing import List

def longestSquareStreak(nums: List[int]) -> int:
    # 1️⃣ 把所有数放进集合，方便 O(1) 判断是否存在
    num_set = set(nums)

    # 2️⃣ 去重并排序，保证从小到大遍历
    uniq = sorted(num_set)

    # 3️⃣ dp 字典：key 是数值，value 是以它结尾的最长 streak 长度
    dp = {}

    max_len = 1  # 记录全局最长长度（至少会有单个元素）

    for val in uniq:
        # 默认长度为 1（自己本身）
        dp[val] = 1

        # 计算整数平方根，判断是否恰好是某个数的平方
        root = int(math.isqrt(val))
        if root * root == val and root in num_set:
            # 如果前驱存在，长度可以延长
            dp[val] = dp[root] + 1

        # 更新全局最大
        if dp[val] > max_len:
            max_len = dp[val]

    # 题目要求 streak 长度必须 ≥ 2
    return max_len if max_len >= 2 else -1
```

> 关键行中文注释  
> - `num_set = set(nums)`：把数组变成“字典”，查询是否存在只要看键在不在。  
> - `uniq = sorted(num_set)`：去重后从小到大遍历，保证前驱已经算好。  
> - `root = int(math.isqrt(val))`：快速算出整数平方根，避免浮点误差。  
> - `if root * root == val and root in num_set:`：只有当 `val` 真正是某个整数的平方且这个整数在数组里时，才可以接在它后面。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `set(nums)` → O(n)  
  - `sorted` → O(n log n)（排序是主要开销）  
  - 主循环遍历每个不同的数一次，内部操作均为 O(1)。  
  - 大白话：即使数组有 100,000 个数，排序大约需要 100,000 × log₂10⁵ ≈ 1.7 百万次比较，完全在 1 秒以内。  

- **空间复杂度**：`O(n)`  
  - 需要存放集合、排序后的列表以及 `dp` 字典，都是线性规模的。  

与暴力解相比，时间从指数级下降到几乎线性，性能提升巨大。

---

## 心得

- **核心技巧**：利用「平方关系的唯一前驱」把问题转化为 **动态规划 + 哈希表**，并配合**排序**确保子问题已经计算完毕。  
- **适用场景**：  
  1. **等比数列 / 等差数列的最长子序列**（如最长斐波那契子序列）。  
  2. **唯一前驱** 的递推关系题目（如「最长除数链」）。  
  3. 需要**快速存在性查询**的 DP 场景，常用 `set`/`dict`。  
- **一句话总结**：只要把「能接在后面」的唯一前驱找出来，用哈希表记住每个数的最长长度，答案自然浮现。

---

## 反思

- **第一反应**：看到「平方」二字，我立刻想到「根」或「前驱」唯一，想到可以用哈希表快速判断是否存在对应的根。  
- **最容易踩的坑**：  
  - 忽略了 **去重**：如果不去重，`dp` 可能会被同一个数多次更新，导致错误的长度。  
  - 使用 `math.sqrt` 产生浮点数误差，导致 `sqrt(val)` 不是整数却被误判。改用 `math.isqrt` 可避免。  
  - 忘记题目要求 **长度至少为 2**，直接返回 `max_len` 会把单个元素算作合法答案。  
- **下次思路**：遇到「每一步只能由唯一前一步得到」的递推关系时，第一步就考虑 **哈希表 + DP**，并先 **排序** 保证前驱已经处理。这样常能把指数级搜索压到线性级。