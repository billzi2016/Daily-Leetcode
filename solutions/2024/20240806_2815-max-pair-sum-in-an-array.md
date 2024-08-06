# #2815. 最大数对和 / Max Pair Sum in an Array

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/max-pair-sum-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. You have to find the maximum sum of a pair of numbers from nums such that the largest digit in both numbers is equal.
For example, 2373 is made up of three distinct digits: 2, 3, and 7, where 7 is the largest among them.
Return the maximum sum or -1 if no such pair exists.

**Examples**

**Example 1:**

```
Input: nums = [112,131,411]
Output: -1
Explanation:
Each numbers largest digit in order is [2,3,4].
```

**Example 2:**

```
Input: nums = [2536,1613,3366,162]
Output: 5902
Explanation:
All the numbers have 6 as their largest digit, so the answer is 2536 + 3366 = 5902.
```

**Example 3:**

```
Input: nums = [51,71,17,24,42]
Output: 88
Explanation:
Each number's largest digit in order is [5,7,7,4,4].
So we have only two possible pairs, 71 + 17 = 88 and 24 + 42 = 66.
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`。请找出 `nums` 中一对数字的最大和，使得这两个数字的**最大数字**（largest digit）相等。  
例如，`2373` 由三个不同的数字组成：`2、3、7`，其中 `7` 是最大的数字。  
返回能够得到的最大和；如果不存在满足条件的数对，则返回 `-1`。

## 示例

### 示例 1
**输入**  
`nums = [112,131,411]`  

**输出**  
`-1`  

**解释**  
每个数字的最大数字依次为 `[2,3,4]`，没有两数的最大数字相同。

### 示例 2
**输入**  
`nums = [2536,1613,3366,162]`  

**输出**  
`5902`  

**解释**  
所有数字的最大数字都是 `6`，因此答案为 `2536 + 3366 = 5902`。

### 示例 3
**输入**  
`nums = [51,71,17,24,42]`  

**输出**  
`88`  

**解释**  
每个数字的最大数字依次为 `[5,7,7,4,4]`。  
满足条件的配对只有两组：`71 + 17 = 88` 和 `24 + 42 = 66`，取最大值 `88`。

## 约束条件
- `2 <= nums.length <= 100`
- `1 <= nums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**枚举所有可能的两两组合**，看每一对数字的「最大位数」是否相同，若相同就计算它们的和，最后取最大的那个。  

- **最大位数**：把数字看成一串字符，找出其中最大的那个字符（0~9），这相当于在字典里查找“最大的字母”。  
- **枚举两两组合**：就像我们要从一堆水果里挑出两只苹果来称重，最笨的办法就是把每两只水果都称一遍。  

为什么这样一定能得到答案？因为我们把**所有**合法的配对都检查了一遍，答案肯定在其中。  

**时间/空间分析（大白话）**  
- 我们要检查 `n` 个数的每一对，组合数是 `n*(n-1)/2`，这在数量级上和 `n²` 是同一个层次。可以把它想象成把 `n` 本书两两配对，配对的次数会随书的数量**平方**增长。  
- 额外空间只用来存放每个数的最大位数（或者直接每次算），这和 `n` 成正比，叫 **O(n)**，即“和输入大小差不多”。  

#### 代码（Python）

```python
from typing import List

def max_pair_sum_brute(nums: List[int]) -> int:
    """
    暴力枚举所有两两组合，返回满足条件的最大和。
    若不存在合法配对，返回 -1。
    """
    n = len(nums)
    ans = -1

    # 辅助函数：求一个整数的最大数字（0~9）
    def largest_digit(x: int) -> int:
        # 把整数转成字符串，遍历每个字符取最大值
        max_d = 0
        for ch in str(x):
            d = int(ch)
            if d > max_d:
                max_d = d
        return max_d

    # 枚举所有 i < j 的组合
    for i in range(n):
        for j in range(i + 1, n):
            if largest_digit(nums[i]) == largest_digit(nums[j]):   # 最大位数相等
                cur_sum = nums[i] + nums[j]
                if cur_sum > ans:          # 记录最大的和
                    ans = cur_sum
    return ans
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  `n` 为数组长度。我们用了两层循环，外层 `n` 次，内层最多 `n-1` 次，整体是 `n × (n-1) / 2`，数量级就是 **平方级**，随着 `n` 增大，耗时会快速增长。  

- **空间复杂度：O(1)**（不计输入）  
  只用了常数个临时变量，和 `n` 没有关系。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于“每对都比较”。其实我们只关心每个**最大位数**对应的**最大的两个数**，因为：

- 只要两数的最大位数相同，它们的和只和这两个数的大小有关。  
- 在同一最大位数的集合里，最大的两数的和一定是**最大**的（其他任意两数的和都不可能超过它们）。  

因此我们可以把所有数字**按照它们的最大位数分到 10 个桶**（0~9），每个桶只保留**当前看到的最大和第二大的数**。遍历一次数组即可得到答案。

**核心数据结构：哈希表（字典）**  
- 把“最大位数”当作键（key），对应的值是一个长度为 2 的列表，保存该桶里最大的两个数。  
- 哈希表就像一本查字典的书，**key** 是词条（这里是最大位数），**value** 是我们要的内容（最大两数）。  

**一步步实现**  

1. **遍历数组**，对每个数 `x`  
   - 计算 `mx = largest_digit(x)`（同上）。  
   - 在 `bucket[mx]` 中维护两个最大值：  
     - 若 `x` 大于当前第一大的，`x` 成为第一大，原第一大下沉为第二大。  
     - 否则若 `x` 大于第二大，更新第二大。  
2. **遍历所有桶**，如果某桶里有两个数（即第二大不为 `-inf`），计算它们的和，取最大。  
3. 若所有桶都没有满足条件的配对，返回 `-1`。  

整个过程只需要一次线性遍历，时间 **O(n)**，空间只需要 10 个小桶，**O(1)**（常数空间）。

#### 代码（Python）

```python
from typing import List
import math

def max_pair_sum_opt(nums: List[int]) -> int:
    """
    只遍历一次数组，使用哈希表（字典）把数字按「最大位数」分组，
    每组只保留最大的两个数，最后求最大和。
    """
    # 辅助函数：求整数的最大数字
    def largest_digit(x: int) -> int:
        max_d = 0
        for ch in str(x):
            d = int(ch)
            if d > max_d:
                max_d = d
        return max_d

    # bucket[d] = [largest, second_largest]，初始化为负无穷
    bucket = {d: [-math.inf, -math.inf] for d in range(10)}

    for num in nums:
        d = largest_digit(num)          # 计算该数的最大位数
        first, second = bucket[d]

        if num > first:                 # 当前数比第一大，还要把第一下沉
            bucket[d][1] = first        # 第二大 = 旧的第一大
            bucket[d][0] = num          # 第一大 = 当前数
        elif num > second:              # 只比第二大大，更新第二大
            bucket[d][1] = num

    ans = -1
    for d in range(10):
        first, second = bucket[d]
        if second != -math.inf:         # 说明该桶里至少有两个数
            cur_sum = first + second
            if cur_sum > ans:
                ans = cur_sum
    return ans
```

#### 复杂度  

- **时间复杂度：O(n)**  
  只遍历一次 `nums`（`n` 次），每次的最大位数计算是常数时间（数字最多 5 位），所以整体是 **线性**，随着 `n` 增大，耗时基本按比例增长。  

- **空间复杂度：O(1)**（不计输入）  
  我们只用了 10 个固定大小的桶（每桶两个整数），和 `n` 没有关系，属于**常数空间**。  

---

## 心得  

- **核心技巧**：**分桶 + 维护局部最大值**。把「最大位数」这个属性抽象成键，把同属性的数放进同一个小容器，只保留对答案有贡献的前两名。  
- **适用题型**：  
  1. “在同一类别里找最大/次大配对” 如 LeetCode 1818 *Minimum Absolute Sum Difference*（需要按值分组取最小差）。  
  2. “同一属性的两数之和最大” 如 “Maximum Sum of Two Non‑Overlapping Subarrays”。  
  3. “按某种特征分组后求最优组合” 如 “Group the People Given the Distance They Are Sitting”。  
- **一句话总结**：**把全局问题拆成若干小组，只在每组里挑出局部最优，就能得到全局最优**。  

---

## 反思  

- **第一反应**：看到“最大位数相同”这句话，我立刻想到**哈希表**把相同属性的数聚在一起。  
- **最容易踩的坑**：  
  - **最大位数的计算**：忘记把数字转成字符串或用取模循环，导致错误的最大位数。  
  - **边界条件**：如果某个最大位数只出现一次，不能构成配对，需要跳过。  
  - **初始化**：第二大数的默认值要设成负无穷或 `None`，否则会误把 `0` 当成合法第二大。  
- **下次类似题**：**先把“相同属性”抽出来，用哈希表分组，然后在每组内部只保留对答案有贡献的前几名**，这一步几乎是所有这类题的通用解法。