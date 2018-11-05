# #154. 寻找旋转排序数组中的最小值 II / Find Minimum in Rotated Sorted Array II

> 难度：困难 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)

---

## 题目（英文原版）

**Description**

Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,4,4,5,6,7] might become:
Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].
Given the sorted rotated array nums that may contain duplicates, return the minimum element of this array.
You must decrease the overall operation steps as much as possible.
Follow up: This problem is similar to Find Minimum in Rotated Sorted Array, but nums may contain duplicates. Would this affect the runtime complexity? How and why?

**Examples**

**Example 1:**

```
Input: nums = [1,3,5]
Output: 1
```

**Example 2:**

```
Input: nums = [2,2,2,0,1]
Output: 0
```

**Constraints**

- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- nums is sorted and rotated between 1 and n times.

---

## 题目（中文翻译）

假设一个长度为 `n`、按升序排序的数组被旋转了 1 到 `n` 次。例如，数组 `nums = [0,1,4,4,5,6,7]` 可能会变成：

> 注意，旋转数组 `[a[0], a[1], a[2], ..., a[n-1]]` 一次后得到 `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`。

给定可能包含重复元素（duplicates）的 **旋转排序数组（rotated sorted array）** `nums`，返回该数组中的最小元素。要求尽可能降低整体的操作步数。

**示例 1**  

**示例 2**  

**约束条件**  

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- `nums` 已排序且被旋转了 1 到 `n` 次

**进阶**：本题与 “寻找旋转排序数组中的最小值”（Find Minimum in Rotated Sorted Array）相似，但 `nums` 可能包含重复元素。这会影响运行时间复杂度吗？为什么？  

**示例**  

**示例 1**  
```
Input: nums = [1,3,5]
Output: 1
```

**示例 2**  
```
Input: nums = [2,2,2,0,1]
Output: 0
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把数组从头到尾全部遍历一遍，找出最小的那个数。  

- **使用的数据结构**：只需要一个普通的 Python 列表 `nums`（它本身就是题目给出的数组），以及一个变量 `min_val` 用来记录当前看到的最小值。可以把 `min_val` 想象成“记事本”，每遍历一个元素，就把它和记事本里的数字比一下，记事本里存的永远是最小的那个。  

- **为什么正确**：因为题目只要求返回数组里的最小元素，而遍历所有元素并比较大小一定能找到全局最小值。  

- **时间/空间复杂度**：  
  - **时间复杂度**是 `O(n)`，这里的 `n` 是数组长度。大白话说，就是“随数组长度线性增长”。如果数组有 1000 个元素，就要检查 1000 次。  
  - **空间复杂度**是 `O(1)`，因为只用了常数个额外变量（记事本 `min_val`），不随 `n` 增长。  

#### 代码（Python）  
```python
def findMin(nums):
    """
    暴力遍历法：找出数组中的最小值
    """
    # 先把第一个元素当作最小值
    min_val = nums[0]          # 记事本里先写下第一个数

    # 从第二个元素开始逐个比较
    for i in range(1, len(nums)):
        if nums[i] < min_val:  # 如果当前数更小，就把记事本更新
            min_val = nums[i]

    return min_val
```

#### 复杂度  
- **时间复杂度**：`O(n)` —— 随着数组长度线性增长，遍历一次即可得到答案。  
- **空间复杂度**：`O(1)` —— 只用了固定的几个变量，和数组大小无关。  

---  

### 2. 最优解  

#### 思路  
虽然暴力遍历已经是 `O(n)`，但题目要求“**尽可能减少整体操作步骤**”，并且提示使用二分查找（Binary Search）。我们可以把“找最小值”看成“在有序数组中定位转折点”。  

**一步步推导**  

1. **观察有序旋转数组的特性**  
   - 旋转前数组是严格递增的（或相等的）。  
   - 旋转后，数组被分成两段：左段整体 **不小于** 右段的所有元素。  
   - 最小元素一定是**右段的第一个**，也就是**左段最后一个元素的后面**。  

2. **二分查找的核心思想**  
   - 设 `left`、`right` 为当前搜索区间的左右端点，`mid = (left + right) // 2`。  
   - 比较 `nums[mid]` 与 `nums[right]`（或 `nums[left]`），根据大小决定“最小值在左边还是右边”。  

3. **遇到相等元素的情况**  
   - 当 `nums[mid] == nums[right]` 时，我们无法判断最小值到底在左边还是右边，因为相等的元素可能出现在两段中。  
   - 退而求其次，**把右指针左移一位** `right -= 1`，相当于“丢掉一个毫无信息价值的重复”。这一步仍然保持 **正确性**（最小值一定在剩下的区间），但最坏情况会退化到线性扫描（所有元素相同），这也是题目所说的“会影响运行时间”。  

4. **循环结束**  
   - 当 `left == right` 时，搜索区间缩小到唯一一个元素，这个元素就是最小值。  

**类比**：把数组想象成一条环形跑道，最小值是跑道上最低的那段。我们站在跑道的任意一点（`right`），向左看（`mid`），如果左边的高度比右边高，说明最低点在左侧；如果左边更低，最低点在右侧。当两侧高度相同（重复元素）时，我们只能往左走一步尝试。  

#### 代码（Python）  
```python
def findMin(nums):
    """
    二分查找（含重复元素）的最小值
    """
    left, right = 0, len(nums) - 1

    while left < right:                     # 当区间还有两个或以上元素时继续
        mid = (left + right) // 2           # 取中间位置

        if nums[mid] > nums[right]:
            # 中间元素更大，说明最小值一定在右半边（mid 右侧）
            left = mid + 1                  # 把搜索区间左移到 mid+1
        elif nums[mid] < nums[right]:
            # 中间元素更小，说明最小值在左半边（包括 mid 本身）
            right = mid                     # 收缩右边界到 mid
        else:
            # nums[mid] == nums[right]，无法判断方向
            # 丢掉 right 位置的重复元素，区间仍然包含最小值
            right -= 1

    # 循环结束时 left == right，指向最小值
    return nums[left]
```

#### 复杂度  
- **时间复杂度**：  
  - 平均情况 `O(log n)`，因为每次循环都能把搜索区间缩小约一半。  
  - 最坏情况 `O(n)`，当数组中大量重复且 `nums[mid] == nums[right]` 时，只能线性地把右指针左移。  
  - 大白话：大多数时候比暴力快很多（比如 1000 个元素只需要 ~10 次比较），但最坏情况下仍然和暴力一样慢。  

- **空间复杂度**：`O(1)`，只用了固定的几个指针变量 `left、right、mid`，不随数组长度增长。  

---  

## 心得  

- **核心技巧**：在有序且可能被旋转的数组中，二分查找可以通过比较中间元素与右端点（或左端点）的大小来判断最小值所在的半区；遇到重复元素时，必须通过线性收缩来保守处理。  
- **适用的题型**：  
  1. **Find Minimum in Rotated Sorted Array**（无重复）——二分直接判断方向。  
  2. **Search in Rotated Sorted Array**（查找某个目标值）——同样利用区间的有序性。  
  3. **Find Peak Element**（寻找峰值）——二分通过比较左右邻居决定搜索方向。  
- **一句话总结解题钥匙**：**“比较中间值与区间端点，利用有序性缩小搜索范围；遇到相等则保守收缩”。**  

---  

## 反思  

- **第一反应**：直接遍历找最小值，觉得最简单。  
- **最容易踩的坑**：  
  - **重复元素**导致 `nums[mid] == nums[right]`，如果不加处理会陷入无限循环。  
  - **边界条件**：当 `left == right` 时要及时返回，否则会多余的循环。  
  - **负数或全相同**的数组也要兼容，不能假设最小值一定在中间左侧。  
- **下次遇到同类题的第一步**：先判断数组是否完全有序（`nums[left] < nums[right]`），如果是直接返回 `nums[left]`；否则使用二分思路，通过比较 `mid` 与 `right`（或 `left`）的大小来决定搜索方向。