# #162. 寻找峰值元素 / Find Peak Element

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/find-peak-element/)

---

## 题目（英文原版）

**Description**

A peak element is an element that is strictly greater than its neighbors.
Given a 0-indexed integer array nums, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks.
You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
You must write an algorithm that runs in O(log n) time.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.
```

**Example 2:**

```
Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.
```

**Constraints**

- 1 <= nums.length <= 1000
- -231 <= nums[i] <= 231 - 1
- nums[i] != nums[i + 1] for all valid i.

---

## 题目（中文翻译）

峰值元素（peak element）是指严格大于其相邻元素的数组成员。  
给定一个 **0 索引** 的整数数组 `nums`，请找到任意一个峰值元素并返回其索引。如果数组中存在多个峰值，返回任意一个峰值的索引即可。

你可以假设 `nums[-1] = nums[n] = -∞`（负无穷）。换言之，数组外部的“邻居”始终被视为比数组内的元素更小。  
要求设计的算法时间复杂度为 **O(log n)**。

**示例 1**

```
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 是一个峰值元素，函数应返回其索引 2。
```

**示例 2**

```
Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: 函数可以返回索引 1（峰值元素为 2），也可以返回索引 5（峰值元素为 6）。
```

**约束条件**

- `1 <= nums.length <= 1000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- 对所有有效的 `i`，都有 `nums[i] != nums[i + 1]`（相邻元素不相等）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组从左到右全部遍历一遍，检查每个元素是否比左右相邻的元素都大。  
- **数据结构**：只需要原始的列表 `nums`，不需要额外的容器。可以把它想象成一排排的楼层号，我们要找出“最高的楼层”，只要挨个看看每层的高度就行了。  
- **正确性**：如果一个位置的值严格大于左边和右边的值（边界处只需要比较内部的那一侧），根据题意它就是峰值。遍历到它时立刻返回即可。  
- **时间/空间复杂度**：我们最多检查每个元素一次，时间是 `O(n)`（n 为数组长度），空间只用了常数级别的变量 `O(1)`，即不随输入规模增长。

> **大白话**：`O(n)` 就是“跟数组的长度成正比”，比如数组有 1000 个元素，就可能要检查 1000 次。`O(1)` 则是“只占很小的固定空间”，不管数组有多大，额外占用的内存几乎不变。

#### 代码（Python）

```python
def findPeakElement(nums):
    """
    暴力遍历寻找峰值
    :param nums: List[int]
    :return: 峰值的下标
    """
    n = len(nums)
    for i in range(n):
        # 左侧是否比左邻居大，左邻居不存在时视为 -∞（即自动满足）
        left_ok = (i == 0) or (nums[i] > nums[i - 1])
        # 右侧是否比右邻居大，右邻居不存在时视为 -∞（即自动满足）
        right_ok = (i == n - 1) or (nums[i] > nums[i + 1])
        if left_ok and right_ok:          # 同时满足左右两侧，则找到峰值
            return i
    # 题目保证一定有峰值，这里理论上永远不会执行到
    return -1
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要检查每个元素一次，最坏情况遍历完整个数组。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量 `n、i`，不随输入大小增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **线性遍历**，每次都要检查完整个数组。题目要求 `O(log n)` 的时间，这正好提示我们可以使用 **二分查找**（Binary Search）——每一步都把搜索区间减半。

二分查找的关键在于**利用相邻元素的大小关系**来决定搜索方向：

1. 取区间中点 `mid`。  
2. 比较 `nums[mid]` 与右邻居 `nums[mid + 1]`（不需要比较左邻居，因为我们只关心“往上走”。）  
   - 如果 `nums[mid] > nums[mid + 1]`，说明 **mid 左侧** 有下降趋势，峰值一定在左半边（包括 `mid` 本身）。  
   - 否则 `nums[mid] < nums[mid + 1]`，说明 **mid 右侧** 正在上升，峰值一定在右半边（排除 `mid`）。  
3. 把搜索区间收缩到对应的半边，继续二分。

为什么这样能保证找到峰值？因为数组两端被视作 `-∞`，必然存在至少一个峰值；二分时我们总是把**可能包含峰值的那一半**留下，最终区间会收缩到唯一的峰值位置。

> **类比**：想象在一条山脉的等高线上走，手里有一个指南针指向更高的方向。每次站在中点，看左边还是右边更高，就往更高的那边走，一半一半地逼近山顶。

#### 代码（Python）

```python
def findPeakElement(nums):
    """
    二分查找实现 O(log n) 的峰值搜索
    :param nums: List[int]
    :return: 峰值的下标
    """
    left, right = 0, len(nums) - 1

    while left < right:                     # 区间长度大于 1 时继续划分
        mid = (left + right) // 2           # 取中点（整数除法向下取整）

        # 如果中点比右邻居大，说明峰值在左半边（包括 mid）
        if nums[mid] > nums[mid + 1]:
            right = mid                     # 收缩右边界到 mid
        else:
            # 否则右邻居更大，峰值一定在右半边（排除 mid）
            left = mid + 1                  # 收缩左边界到 mid+1

    # 循环结束时 left == right，指向唯一的峰值下标
    return left
```

#### 复杂度

- **时间复杂度**：`O(log n)` — 每次循环把搜索区间长度减半，类似二分查找的对数级别。相比暴力的 `O(n)`，速度提升显著。  
- **空间复杂度**：`O(1)` — 只用了几个指针变量 `left、right、mid`，不随数组规模增长。

---

## 心得

- **核心技巧**：利用相邻元素的大小关系进行二分搜索（单向梯度二分）。  
- **适用题型**：  
  1. “寻找局部最小/最大” 类问题（如 LeetCode 154 Find Minimum in Rotated Sorted Array）。  
  2. “单调区间” 或 “山脉数组” 的搜索（如 LeetCode 852 Peak Index in a Mountain Array）。  
- **一句话总结**：**“只要能判断峰值在左还是右，就能用二分把搜索空间快速砍掉一半。”**

## 反思

- **第一反应**：看到“峰值”和“邻居”，自然想到逐个检查——暴力遍历。  
- **最容易踩的坑**：  
  - 边界处理：`mid` 在数组最后一个位置时 `mid+1` 会越界，需要保证循环条件 `left < right`，这样 `mid` 永远不是最右端。  
  - 题目保证相邻元素不相等，但如果忘记这点，比较相等时的处理会导致死循环。  
- **下次思考路径**：遇到“在 O(log n) 时间内定位某个位置”时，第一步就想 **“二分能否利用单调/梯度信息？”**，然后明确比较方向并收缩区间。