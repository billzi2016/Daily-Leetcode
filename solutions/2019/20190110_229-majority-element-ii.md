# #229. 出现次数超过 ⌊ n/3 ⌋ 的元素 II / Majority Element II

> 难度：中等 · 标签：Array、Hash Table、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/majority-element-ii/)

---

## 题目（英文原版）

**Description**

Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.
Follow up: Could you solve the problem in linear time and in O(1) space?

**Examples**

**Example 1:**

```
Input: nums = [3,2,3]
Output: [3]
```

**Example 2:**

```
Input: nums = [1]
Output: [1]
```

**Example 3:**

```
Input: nums = [1,2]
Output: [1,2]
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个大小为 n 的整数数组（integer array），找出所有出现次数严格大于 ⌊ n/3 ⌋ 次的元素。

示例 1  
Input: nums = [3,2,3]  
Output: [3]  

示例 2  
Input: nums = [1]  
Output: [1]  

示例 3  
Input: nums = [1,2]  
Output: [1,2]  

约束条件  
- 1 <= nums.length <= 5 * 104  
- -109 <= nums[i] <= 109  

进阶：你能否在 **线性时间（linear time）** 且 **O(1) 空间** 内解决此问题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组里每个数字出现的次数全部统计出来，然后挑出出现次数 > ⌊ n/3 ⌋ 的元素。  

- **用到的数据结构**：哈希表（Python 中的 `dict`）。可以把它想象成一本“词典”，词（`key`）是数组里的数字，页码（`value`）是这个数字出现的次数。查一次词典的代价是 **O(1)**，就像在字典里快速找到单词的解释一样。  
- **为什么正确**：我们把每个数字出现的次数都记下来，遍历一遍哈希表，只要次数大于阈值 `n//3`，就一定满足题目要求。没有遗漏，也不会误选。  
- **时间/空间复杂度**：  
  - 先遍历数组一次统计次数 → **O(n)**（`n` 是数组长度）。  
  - 再遍历哈希表挑选结果 → 最多也是 **O(n)**（哈希表里最多有 `n` 条记录）。  
  - 所以总体时间是 **O(n)**。  
  - 哈希表需要保存每个不同数字的计数，最坏情况下所有数字都不相同，需要 **O(n)** 的额外空间。  
  - 用大白话说，**O(n)** 就是“随数组长度线性增长”，如果数组有 10 万个数，就大概需要 10 万次基本操作和 10 万个存储单元。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def majorityElement(nums: List[int]) -> List[int]:
    # 1️⃣ 统计每个数字出现的次数，类似查字典
    count = defaultdict(int)          # key: 数字，value: 出现次数
    for num in nums:                  # 遍历一次数组
        count[num] += 1               # 出现一次，就把对应的计数加 1

    # 2️⃣ 挑选出现次数 > n//3 的数字
    threshold = len(nums) // 3        # n/3 的整数下取整
    res = []
    for num, freq in count.items():   # 遍历字典的每一项
        if freq > threshold:          # 大于阈值就保留下来
            res.append(num)

    return res
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 只需要遍历两遍数组/字典，操作次数随 `n` 成正比。  
- **空间复杂度**：**O(n)** — 最坏情况下每个元素都不相同，需要把 `n` 条记录存进哈希表。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，统计全部次数虽然简单，但用了 **O(n)** 的额外空间。题目进阶要求 **线性时间 O(n) 且 O(1) 额外空间**，也就是说我们只能用常数个变量来完成。

**关键观察**：

1. **出现次数 > ⌊n/3⌋ 的元素最多有两个**。  
   - 想象把数组划分成 `⌊n/3⌋` 大小的块，每块最多只能容纳一种“多数”。如果有第三种元素也超过 `n/3`，那总长度就会超过 `n`，不可能。所以答案的候选集合最多是 2 个。

2. 这让我们可以 **把问题转化为“找出最多两个候选”**，然后再一次遍历确认它们的真实出现次数。  
   - 这正是 **Boyer‑Moore 投票算法** 的思路，只不过原始算法只能找出出现 > n/2 的“多数”。我们把它扩展到找 **两个** 候选，分别维护它们的计数。

**算法步骤**：

- **第一遍（选出候选）**  
  - 用两个变量 `cand1, cand2` 保存候选数字，`cnt1, cnt2` 保存对应的计数，初始计数都为 0。  
  - 遍历数组 `num`，按以下规则更新：
    1. 如果 `num` 与 `cand1` 相同 → `cnt1 += 1`  
    2. 否则如果 `num` 与 `cand2` 相同 → `cnt2 += 1`  
    3. 否则如果 `cnt1 == 0` → 把 `num` 设为 `cand1`，`cnt1 = 1`  
    4. 否则如果 `cnt2 == 0` → 把 `num` 设为 `cand2`，`cnt2 = 1`  
    5. 否则 → 两个候选都减 1（`cnt1 -= 1; cnt2 -= 1`），相当于“相互抵消”。  
  - 这一步保证如果真的有出现 > n/3 的元素，它一定会保留下来（因为它的出现次数比抵消的次数多）。

- **第二遍（计数验证）**  
  - 重新遍历数组，分别统计 `cand1` 与 `cand2` 的真实出现次数 `cnt1, cnt2`（这里的计数不再用于抵消，只是计数）。  
  - 最后把出现次数 > n//3 的候选加入结果。

**为什么有效**：  
- 抵消的思想可以看成“把不同的数字两两配对”。每配对一次，两个数字的计数各减 1。出现次数最多的数字因为数量多，配对后仍会剩余，最终成为候选。  
- 因为我们只维护两个候选，空间始终是常数级别。

#### 代码（Python）

```python
from typing import List

def majorityElement(nums: List[int]) -> List[int]:
    # ---------- 第一遍：找出最多两个候选 ----------
    cand1 = cand2 = None   # 候选数字
    cnt1 = cnt2 = 0        # 对应的计数

    for num in nums:
        if cand1 == num:               # 与候选1相同，计数加一
            cnt1 += 1
        elif cand2 == num:             # 与候选2相同，计数加一
            cnt2 += 1
        elif cnt1 == 0:                # 候选1的计数为 0，换成当前数字
            cand1, cnt1 = num, 1
        elif cnt2 == 0:                # 候选2的计数为 0，换成当前数字
            cand2, cnt2 = num, 1
        else:                          # 两个候选都不相同，且计数都不为 0，统一抵消一次
            cnt1 -= 1
            cnt2 -= 1

    # ---------- 第二遍：验证候选的真实出现次数 ----------
    cnt1 = cnt2 = 0                    # 重新计数
    for num in nums:
        if num == cand1:
            cnt1 += 1
        elif num == cand2:            # 注意这里用 elif，防止同一个数被两次计数
            cnt2 += 1

    res = []
    n = len(nums)
    if cnt1 > n // 3:
        res.append(cand1)
    if cnt2 > n // 3:
        res.append(cand2)

    return res
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 两次线性遍历，操作次数随数组长度线性增长。相比暴力解，它没有额外的哈希表查找，仍是“一次遍历 + 再一次遍历”。  
- **空间复杂度**：**O(1)** — 只用了固定的几个变量（`cand1, cand2, cnt1, cnt2`），不随 `n` 增长。  

---

## 心得  

- 这道题核心考察 **“多数元素”** 的扩展——理解出现次数的上限（> n/3 最多两个），以及 **Boyer‑Moore 投票算法** 的推广。  
- 该技巧适用于的题型：  
  1. **Majority Element**（出现 > n/2 的元素）  
  2. **Find All Elements Appearing More Than ⌊ n/k ⌋ Times**（通用的 k‑多数）  
  3. **LeetCode 229 – Majority Element II**（本题）  
- 一句话总结解题钥匙：**“先用抵消法找出最多 k‑1 个候选，再用一次计数确认”**。

## 反思  

- **第一反应**：直接想到哈希表统计——最直观但占用 O(n) 额外空间。  
- **最容易踩的坑**：  
  - 忘记答案可能有 **两个** 元素，写成只返回一个会漏掉情况。  
  - 第二遍计数时如果使用 `if` 而不是 `elif`，同一个数字可能被两次计数，导致错误。  
  - 边界情况如 `nums` 长度为 1 或 2 时，候选变量可能保持 `None`，要确保代码能正确处理。  
- **下次遇到同类题**，第一步应该思考 “**出现次数的阈值能容纳多少不同的多数**”，然后 **“用抵消（投票）把不可能的元素剔除，只留下最多 k‑1 个候选”**。这样就能快速定位到 O(1) 空间的最优思路。