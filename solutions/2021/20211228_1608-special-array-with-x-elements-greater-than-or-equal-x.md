# #1608. 特殊数组（Special Array With X Elements Greater Than or Equal X） / Special Array With X Elements Greater Than or Equal X

> 难度：简单 · 标签：Array、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/special-array-with-x-elements-greater-than-or-equal-x/)

---

## 题目（英文原版）

**Description**

You are given an array nums of non-negative integers. nums is considered special if there exists a number x such that there are exactly x numbers in nums that are greater than or equal to x.
Notice that x does not have to be an element in nums.
Return x if the array is special, otherwise, return -1. It can be proven that if nums is special, the value for x is unique.

**Examples**

**Example 1:**

```
Input: nums = [3,5]
Output: 2
Explanation: There are 2 values (3 and 5) that are greater than or equal to 2.
```

**Example 2:**

```
Input: nums = [0,0]
Output: -1
Explanation: No numbers fit the criteria for x.
If x = 0, there should be 0 numbers >= x, but there are 2.
If x = 1, there should be 1 number >= x, but there are 0.
If x = 2, there should be 2 numbers >= x, but there are 0.
x cannot be greater since there are only 2 numbers in nums.
```

**Example 3:**

```
Input: nums = [0,4,3,0,4]
Output: 3
Explanation: There are 3 values that are greater than or equal to 3.
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定一个由非负整数构成的数组 `nums`。如果存在一个整数 `x`，使得数组中恰好有 `x` 个元素 **大于等于**（greater than or equal to）`x`，则称该数组为 **特殊**（special）的。  
需要注意，`x` 不一定是 `nums` 中的元素。  
如果数组是特殊的，返回对应的 `x`；否则返回 `-1`。可以证明，当数组是特殊时，满足条件的 `x` 是唯一的。

**示例**  

示例 1  
```
Input: nums = [3,5]
Output: 2
Explanation: 有 2 个数（3 和 5）大于等于 2。
```

示例 2  
```
Input: nums = [0,0]
Output: -1
Explanation: 没有数字满足 x 的条件。
- 当 x = 0 时，应该有 0 个数 ≥ x，但实际有 2 个。
- 当 x = 1 时，应该有 1 个数 ≥ x，但实际有 0 个。
- 当 x = 2 时，应该有 2 个数 ≥ x，但实际有 0 个。
- x 不能更大，因为数组中只有 2 个数。
```

示例 3  
```
Input: nums = [0,4,3,0,4]
Output: 3
Explanation: 有 3 个数大于等于 3。
```

**约束条件**  
- `1 <= nums.length <= 100`  
- `0 <= nums[i] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：  
- 先把可能的 `x` 的取值列出来。题目说明 `x` 的范围只能在 **0 到数组长度** 之间（因为不可能有超过数组长度的元素满足 “≥ x”）。  
- 对每一个候选 `x`，遍历整条 `nums`，统计 **有多少个元素 ≥ x**。  
- 如果统计的结果恰好等于 `x`，说明找到了满足条件的 `x`，直接返回它。  
- 如果所有 `x` 都不满足，返回 `-1`。

> **数据结构类比**：遍历 `nums` 统计符合条件的元素，就像在超市里手动数一数有多少件商品的价格 **不低于** 某个阈值。这里不需要额外的结构，直接用一个计数器就行。

> **为什么正确**：我们把所有可能的 `x`（0~n）都穷举检查了，每一种情况下都精确地算出了 “≥ x” 的元素个数。如果有某个 `x` 能让两者相等，它一定会在遍历中被发现；如果没有，那说明根本不存在这样的 `x`，返回 `-1` 正是题目要求的答案。

#### 代码（Python）  
```python
def specialArray(nums):
    n = len(nums)                     # 数组长度，x 的最大可能值
    # 依次尝试所有可能的 x，从 0 到 n
    for x in range(n + 1):
        cnt = 0                        # 统计 ≥ x 的元素个数
        for v in nums:                 # 遍历整个数组
            if v >= x:                 # 如果当前元素满足条件
                cnt += 1
        if cnt == x:                   # 检查是否恰好等于 x
            return x                   # 找到答案，直接返回
    return -1                          # 没有任何 x 满足条件
```

#### 复杂度  
- **时间复杂度：** `O(n²)`。外层循环最多跑 `n+1` 次，内层遍历整个数组 `n` 次，整体是 `n × n` 的量级。用大白话说，就是如果数组有 100 个数，最多要检查 10 000 次。  
- **空间复杂度：** `O(1)`。只用了几个计数变量，和输入规模无关。

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于：**每检查一个 `x` 都要重新遍历一遍数组**。我们可以利用**排序**把这一步省掉。  

1. **先把数组从大到小排好序**。排好序后，所有大于等于某个阈值的元素会集中在左边。  
2. 设排好序后的数组为 `a[0] ≥ a[1] ≥ … ≥ a[n‑1]`。  
   - 对于任意 `k`（1 ≤ k ≤ n），如果 `a[k‑1] ≥ k` 且 `a[k] < k`（这里把 `a[n]` 当作 `-∞` 方便统一写法），那么恰好有 `k` 个元素 ≥ `k`，答案就是 `k`。  
   - 直观解释：从左往右数第 `k` 大的数，如果它 **不小于** `k`，说明前 `k` 个数都 ≥ `k`；再看第 `k+1` 大的数，如果它 **小于** `k`，说明后面的数都 < `k`，于是“恰好有 `k` 个 ≥ `k`”。  
3. 只需要一次遍历检查这些条件即可得到答案。如果遍历完都不满足，则返回 `-1`。  
4. 另外一种等价写法是：遍历已排序数组，记录当前已经看到的元素个数 `i+1`，当 `a[i] >= i+1` 且（`i+1 == n` 或 `a[i+1] < i+1`) 时返回 `i+1`。

> **核心算法/数据结构**：**排序 + 线性扫描**。排序把“≥ x 的计数”转化为“前缀长度”，一次扫描即可判断是否恰好匹配。  
> **类比**：想象把一堆砖块按高度从高到低排好，然后从最高的开始数。如果第 `k` 块砖的高度仍然不低于 `k`，而第 `k+1` 块已经低于 `k`，说明正好有 `k` 块砖高到 `k`，这正是我们要找的 `x`。

#### 代码（Python）  
```python
def specialArray(nums):
    nums.sort(reverse=True)            # 降序排列，大的在前面
    n = len(nums)

    for i, v in enumerate(nums):       # i 为下标，v 为当前元素值
        # 已经看到 i+1 个元素（下标从 0 开始），判断它们是否满足条件
        if v >= i + 1:                  # 前 i+1 个数都 >= i+1
            # 检查第 i+2 个数（如果存在）是否已经 < i+1
            if i == n - 1 or nums[i + 1] < i + 1:
                return i + 1            # 找到唯一的答案
    return -1                           # 没有任何 x 满足条件
```

#### 复杂度  
- **时间复杂度：** `O(n log n)`。排序需要 `n log n`，随后一次线性扫描是 `O(n)`，整体以排序的复杂度为主。对比暴力的 `O(n²)`，这在 `n` 较大时快得多。  
- **空间复杂度：** `O(1)`（如果使用原地排序）。只用了常数级别的额外变量。

---  

## 心得  

- **核心技巧**：把“计数满足某个阈值的元素个数”转化为**排序后前缀长度的比较**，利用有序性一次遍历即可判断。  
- **适用的题型**：  
  1. “有多少元素 ≥ k” 类的阈值统计题（如 **H-指数**）。  
  2. “数组中是否存在满足某种单调关系的下标” 题目（如 **找出固定点**、**最长递增子序列的长度** 的简化版）。  
- **解题钥匙**：**先把数据排好序**，让“≥ x 的计数”变成“前面有多少个”。  

---  

## 反思  

- **第一反应**：看到 “恰好有 x 个数 ≥ x”，立刻想到枚举所有可能的 `x` 并逐个计数——这就是暴力解。  
- **最容易踩的坑**：  
  - 忽略 `x = 0` 的情况，需要检查是否有 **0 个元素 ≥ 0**（只有在数组全为空时才成立）。  
  - 在排序实现时，忘记处理 “最后一个元素” 的边界，导致索引越界。  
  - 误以为 `x` 必须是数组里的某个元素，其实 `x` 可以是任意整数。  
- **下次思路**：遇到 “≥ 阈值的计数” 这类问题，先问自己 **是否可以排序或构造前缀/后缀信息**，把计数转化为位置比较，从而避免重复遍历。