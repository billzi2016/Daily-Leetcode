# #3423. 环形数组中相邻元素的最大差值 / Maximum Difference Between Adjacent Elements in a Circular Array

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-between-adjacent-elements-in-a-circular-array/)

---

## 题目（英文原版）

**Description**

Given a circular array nums, find the maximum absolute difference between adjacent elements.
Note: In a circular array, the first and last elements are adjacent.

**Examples**

**Example 1:**

```
Input: nums = [1,2,4]
Output: 3
Explanation:
Because nums is circular, nums[0] and nums[2] are adjacent. They have the maximum absolute difference of |4 - 1| = 3 .
```

**Example 2:**

```
Input: nums = [-5,-10,-5]
Output: 5
Explanation:
The adjacent elements nums[0] and nums[1] have the maximum absolute difference of |-5 - (-10)| = 5 .
```

**Constraints**

- 2 <= nums.length <= 100
- -100 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个环形数组 `nums`，求相邻元素之间的最大绝对差值（absolute difference）。  
**注意**：在环形数组中，首元素与尾元素视为相邻。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**  

**示例 1**  
```
Input: nums = [1,2,4]
Output: 3
```
**解释**：  
因为 `nums` 是环形的，`nums[0]` 与 `nums[2]` 相邻。它们的绝对差值为 `|4 - 1| = 3`，是所有相邻元素中最大的。

**示例 2**  
```
Input: nums = [-5,-10,-5]
Output: 5
```
**解释**：  
相邻的元素 `nums[0]` 与 `nums[1]` 的绝对差值为 `|-5 - (-10)| = 5`，为最大值。

**约束条件**  
- `2 <= nums.length <= 100`  
- `-100 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把数组里每一对相邻的元素都拿出来算一次绝对差，然后把最大的那个记下来。  
- **相邻**：在普通数组里相邻就是下标相差 1 的两个数；因为是**环形**数组，首尾也算相邻（下标 0 和 n‑1）。  
- **数据结构**：只需要遍历一次原数组，用一个普通的整数变量 `max_diff` 保存当前看到的最大差值。这里不需要额外的结构，类似把“查字典”简化成“顺着走”。  

**为什么正确**：  
我们把**所有**可能的相邻对都检查了一遍，最大值必然在这几次比较里出现，漏掉任何一对都不可能得到正确答案。

**复杂度大白话**：  
- 时间复杂度 `O(n)`：我们遍历了 `n` 次（`n` 是数组长度），每次只做常数时间的运算，像排队买票，排几个人就花几分钟。  
- 空间复杂度 `O(1)`：只用了几个变量，跟数组长度无关，就像只带了一把钥匙，不会占用额外的背包空间。  

#### 代码（Python）  

```python
from typing import List

def max_adjacent_difference(nums: List[int]) -> int:
    """
    暴力遍历所有相邻对（包括首尾），返回最大的绝对差。
    """
    n = len(nums)                     # 数组长度
    max_diff = 0                       # 用来记录最大的差值，初始为 0

    # 从下标 1 到 n-1，比较 nums[i] 与 nums[i-1]
    for i in range(1, n):
        diff = abs(nums[i] - nums[i - 1])   # 计算当前相邻两数的绝对差
        if diff > max_diff:                 # 如果更大，就更新答案
            max_diff = diff

    # 环形数组的特殊相邻对：首元素和尾元素
    circular_diff = abs(nums[0] - nums[-1])
    if circular_diff > max_diff:
        max_diff = circular_diff

    return max_diff
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历了一遍数组，`n` 越大，时间就线性增长。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量，和数组大小无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解来看，唯一的“瓶颈”其实是 **没有**，因为我们已经只用了一次线性遍历。  
- **慢在哪里？**：如果把环形的首尾比较单独写在循环外，仍然是 `O(n)`，没有多余的嵌套循环或额外的数据结构。  
- **进一步优化**：可以把首尾的比较合并到循环里，让代码更简洁：把循环范围设为 `0 … n-1`，每次比较 `nums[i]` 与 `nums[(i+1) % n]`（取模实现环形），这样只需要一条 `for` 循环即可。  

核心技巧是 **取模运算**（`% n`）把数组视作环形，这在很多环形题目中都非常有用。可以把它想象成跑步场上的跑道：跑到最后一个格子后再回到起点，永远不掉队。

#### 代码（Python）  

```python
def max_adjacent_difference_opt(nums: List[int]) -> int:
    """
    只用一条循环，利用取模实现环形相邻比较。
    """
    n = len(nums)
    max_diff = 0

    for i in range(n):
        # (i + 1) % n 自动把最后一个元素的下一个指向第一个元素
        diff = abs(nums[i] - nums[(i + 1) % n])
        if diff > max_diff:
            max_diff = diff

    return max_diff
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 仍然是一遍遍历，只是代码更简洁。相比暴力解没有实际加速，只是**常数因子**更小。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量。  

---  

## 心得  

- **核心技巧**：把线性数组看成环形，用取模 `% n` 直接得到“下一个”元素。  
- **适用的题型**：  
  1. 环形数组最大/最小差值（本题）。  
  2. 环形数组中连续子数组的最大和（LeetCode 918）。  
  3. 环形队列的实现（常见在数据结构课程）。  
- **一句话总结**：  
  “环形数组的相邻关系，用 `(i+1) % n` 一句搞定，遍历一次即可得最大差”。  

## 反思  

- **第一反应**：先把普通相邻差算一遍，再记得补上首尾这对。  
- **最容易踩的坑**：忘记了环形特性，只比较了 `0 … n-2` 的相邻对，导致答案缺少首尾差；或者在取模时写成 `(i-1) % n` 导致负数下标错误（Python 负数取模仍然有效，但逻辑上容易混淆）。  
- **下次遇到同类题**：第一步就思考“这是不是环形结构”，如果是，立刻把索引用取模写成统一的相邻访问公式。