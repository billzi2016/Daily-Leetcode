# #3375. 使数组元素等于 K 的最少操作次数 / Minimum Operations to Make Array Values Equal to K

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-array-values-equal-to-k/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
An integer h is called valid if all values in the array that are strictly greater than h are identical.
For example, if nums = [10, 8, 10, 8], a valid integer is h = 9 because all nums[i] > 9 are equal to 10, but 5 is not a valid integer.
You are allowed to perform the following operation on nums:
Return the minimum number of operations required to make every element in nums equal to k. If it is impossible to make all elements equal to k, return -1.

**Examples**

**Example 1:**

```
Input: nums = [5,2,5,4,5], k = 2
Output: 2
Explanation:
The operations can be performed in order using valid integers 4 and then 2.
```

**Example 2:**

```
Input: nums = [2,1,2], k = 2
Output: -1
Explanation:
It is impossible to make all the values equal to 2.
```

**Example 3:**

```
Input: nums = [9,7,5,3], k = 1
Output: 4
Explanation:
The operations can be performed using valid integers in the order 7, 5, 3, and 1.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- 1 <= k <= 100

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums` 和一个整数 `k`。  
如果所有严格大于某个整数 `h` 的数组元素值都相同，则称整数 `h` 为**有效整数 (valid integer)**。例如，`nums = [10, 8, 10, 8]` 时，`h = 9` 是有效整数，因为所有 `nums[i] > 9` 的元素都等于 `10`；但 `h = 5` 不是有效整数。  

你可以对 `nums` 执行以下**操作 (operation)**：  
（题目原文未给出具体操作细节，此处保持原样）  

返回使 `nums` 中每个元素都等于 `k` 所需的**最少操作次数**。如果无法使所有元素等于 `k`，返回 `-1`。

**示例**

*示例 1*  
输入: `nums = [5,2,5,4,5]`, `k = 2`  
输出: `2`  
解释:  
可以依次使用有效整数 `4` 和 `2` 完成操作。

*示例 2*  
输入: `nums = [2,1,2]`, `k = 2`  
输出: `-1`  
解释:  
无法使所有值都等于 `2`。

*示例 3*  
输入: `nums = [9,7,5,3]`, `k = 1`  
输出: `4`  
解释:  
可以按顺序使用有效整数 `7、5、3、1` 完成操作。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i] <= 100`  
- `1 <= k <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步一步模拟题目允许的操作**：

1. 先检查数组里有没有比 `k` 小的元素。如果有，说明无论怎么操作都无法把它们提升到 `k`，直接返回 `-1`。  
2. 否则，找出当前数组中 **最大的** 那些数。  
3. 根据题意，只有当「所有大于某个整数 `h` 的元素都相等」时，`h` 才是合法的。于是我们可以把 **所有比最大值大的元素**（其实就是最大值本身）一次性降到 **次大的数**，这相当于一次合法操作。  
4. 重复步骤 2~3，直到所有元素都不大于 `k` 为止。  

把每一次「把最大的数降到次大」记为一次操作，最终的操作次数就是答案。

> **类比**：想象你在整理一排不同高度的积木。你只能一次把最高的那堆积木整体压到第二高的那层，随后再把新的最高层压到更低的层，直到所有积木都达到同一高度 `k`。每压一次，就相当于一次合法操作。

**为什么正确**  
- 只要数组里没有小于 `k` 的数，我们总可以把最高的数降到次高的数（因为次高的数已经满足「所有更高的数相等」的条件），这一步合法且不会破坏以后继续降的可能性。  
- 最终我们把所有大于 `k` 的不同数依次「合并」到 `k`，所以操作次数恰好等于 **大于 `k` 的不同数的个数**。暴力模拟正是把这个过程一步步显式地执行出来。

**复杂度分析（大白话）**  
- 每一次循环我们都要遍历整个数组找最大值和次大值，最坏情况下要循环 `distinct` 次（`distinct` 为不同数的个数），每次遍历是 `O(n)`。于是总时间是 `O(n * distinct)`，在最坏情况下 `distinct` 可能接近 `n`，所以是 `O(n²)`。  
- 只用了原数组和几个临时变量，额外空间是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def minOperations_bruteforce(nums: List[int], k: int) -> int:
    # 1️⃣ 先检查有没有比 k 小的数
    if min(nums) < k:
        return -1                     # 直接返回 -1，说明不可能

    ops = 0                           # 记录操作次数
    while True:
        # 2️⃣ 找出当前数组中最大的数
        cur_max = max(nums)
        if cur_max == k:               # 所有数都已经等于 k，结束循环
            break

        # 3️⃣ 找到次大的数（如果次大不存在，就把它降到 k）
        #   用集合去重后排序，得到所有不同的数
        distinct_vals = sorted(set(nums), reverse=True)
        # distinct_vals[0] == cur_max，第二大的要么是 distinct_vals[1]，
        # 要么如果只有一种数，则直接降到 k
        next_val = distinct_vals[1] if len(distinct_vals) > 1 else k

        # 4️⃣ 把所有等于 cur_max 的位置都改成 next_val（一次合法操作）
        for i in range(len(nums)):
            if nums[i] == cur_max:
                nums[i] = next_val

        ops += 1                       # 计数
    return ops
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每次循环遍历数组找最大/次大，最坏要循环 `n` 次。  
  *大白话*：如果数组有 100 个数，最坏需要 100 × 100 = 10 000 次基本操作，算是比较慢的。
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定操作次数的不是具体的降序过程，而是“大于 `k` 的不同数有多少”。**  
所以我们不必真的去模拟降的过程，只要：

1. **先检查**：如果数组里出现了比 `k` 小的数，说明根本不可能把它们提升到 `k`（题目只允许把更大的数降下来），直接返回 `-1`。  
2. **统计**：把所有大于 `k` 的数放进一个集合（集合天然去重），集合的大小就是不同的大于 `k` 的数的个数，也就是最少需要的操作次数。  

> **类比**：把所有不同颜色的积木按颜色分堆，只有颜色比 `k` 深的需要重新涂色。每一种颜色只需要一次涂色，就能变成目标颜色 `k`。于是答案就是“有几种颜色需要改”。  

这一步只需要一次遍历，时间 `O(n)`，空间 `O(100)`（因为数值范围只有 1~100，用集合存放不超过 100 个元素）。

#### 代码（Python）

```python
from typing import List

def minOperations(nums: List[int], k: int) -> int:
    """
    返回把所有元素变成 k 所需的最少操作次数，
    若不可能则返回 -1。
    """
    # 1️⃣ 检查是否有小于 k 的数
    if any(x < k for x in nums):
        return -1                     # 无法提升，只能降，直接失败

    # 2️⃣ 统计所有大于 k 的不同数
    greater_set = set()
    for x in nums:
        if x > k:
            greater_set.add(x)        # 加入集合会自动去重

    # 3️⃣ 集合的大小就是答案
    return len(greater_set)
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 最多 100，几乎瞬间完成。  
  *大白话*：如果有 100 个数，只检查 100 次就够了，比暴力的 10 000 次快很多。
- **空间复杂度**：`O(m)`，其中 `m` 是不同的“大于 k 的数”的个数，最坏不超过 100（因为数值范围 1~100），实际几乎可以视作 `O(1)` 的常数空间。

---

## 心得

- **核心技巧**：把「操作次数」转化为「大于 `k` 的不同数的个数」，利用集合去重的特性直接计数。  
- **适用的题型**  
  1. “把数组中所有元素变成同一个值，只能降不能升” 类似题（如 LeetCode 2363 “Minimum Replacements to Sort the Array”）。  
  2. “统计满足某种条件的不同元素个数” 的计数题（如 “Distinct Elements in an Array”）。  
  3. “只能对满足某种约束的子集进行操作”的优化题（如 “Maximum Number of Operations to Reduce X to Zero”）。  
- **一句话总结**：**只要数组里没有比目标更小的数，答案就是“大于目标的不同数有几种”。**

---

## 反思

- **第一反应**：看到“只能把更大的数降下来”，第一时间想到了**逐层降**的过程——也就是暴力模拟。  
- **最容易踩的坑**  
  - 忘记检查 **是否存在小于 `k` 的元素**，导致错误返回一个正数。  
  - 误以为每一次降到次大需要多次操作，其实一次即可把同一数值的所有位置一起降。  
  - 把 “不同数的个数” 与 “不同数的出现次数” 混淆，导致多计数。  
- **下次遇到同类题**：第一步先 **判断是否有不可逆的元素（这里是小于 k）**，随后 **直接统计满足条件的不同值**，而不是去模拟整个过程。这样既简洁又高效。