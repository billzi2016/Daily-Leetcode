# #34. 在排序数组中查找元素的首尾位置 / Find First and Last Position of Element in Sorted Array

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.
If target is not found in the array, return [-1, -1].
You must write an algorithm with O(log n) runtime complexity.

**Examples**

**Example 1:**

```
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
```

**Example 2:**

```
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
```

**Example 3:**

```
Input: nums = [], target = 0
Output: [-1,-1]
```

**Constraints**

- 0 <= nums.length <= 105
- -109 <= nums[i] <= 109
- nums is a non-decreasing array.
- -109 <= target <= 109

---

## 题目（中文翻译）

给定一个整数数组（array）`nums`，该数组按非递减顺序（non-decreasing order）排序，找出给定目标值（target）的起始位置和结束位置。  
如果数组中不存在目标值，则返回 `[-1, -1]`。  
要求实现时间复杂度为 `O(log n)` 的算法（algorithm）。

示例 1:  
示例 2:  
示例 3:

约束条件：
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums` 为非递减数组（non-decreasing array）。
- `-10^9 <= target <= 10^9`

示例：
示例 1:
```
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
```

示例 2:
```
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
```

示例 3:
```
Input: nums = [], target = 0
Output: [-1,-1]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组从左到右全部扫描一遍，记录下第一次出现 `target` 的下标和最后一次出现 `target` 的下标。  

- **用到的数据结构**：只需要 Python 的列表（`list`）和两个整数变量。列表相当于我们生活中的排好队的商品货架，左边的商品先摆放，右边的商品后摆放。  
- **为什么正确**：因为我们把每一个元素都检查了一遍，只要出现了 `target`，就一定会被记录；如果整个数组都没有 `target`，最终的记录值仍然保持为 `-1`，符合题目要求。  
- **复杂度分析**：  
  - **时间**：我们必须检查 `n`（数组长度）个元素，最坏情况下每个元素都要看一遍，所以是 **O(n)**。这里的 `O(n)` 可以理解为“随着数组变长，检查的次数几乎和数组长度成正比”。  
  - **空间**：只用了常数个额外变量（两个下标），不随 `n` 增长，所以是 **O(1)**，也就是“几乎不占额外内存”。

#### 代码（Python）

```python
def searchRange(nums, target):
    """
    暴力解：一次遍历数组，记录第一次和最后一次出现 target 的下标。
    """
    first = -1          # 第一次出现的位置，默认 -1 表示未找到
    last = -1           # 最后一次出现的位置，默认 -1

    for i, num in enumerate(nums):   # enumerate 同时拿到下标 i 和元素值 num
        if num == target:            # 找到目标值
            if first == -1:          # 还没有记录过第一次出现
                first = i
            last = i                 # 每次遇到都更新为最新的下标

    return [first, last]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要遍历整个数组，数组有多长，就要看多少次。  
- **空间复杂度**：`O(1)` — 只用了固定的几个变量，和数组大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历整个数组**。题目要求 **O(log n)** 的时间复杂度，这正是二分查找（Binary Search）擅长的场景：在一个**已排序**的序列里快速定位目标。

二分查找的核心是把搜索区间不断“一分为二”，每次只保留可能包含目标的那一半。这里有一点技巧：我们需要分别找出 **左边界**（第一个等于 `target` 的位置）和 **右边界**（最后一个等于 `target` 的位置），所以要进行 **两次** 二分查找：

1. **找左边界**  
   - 目标是“第一个 >= target 的位置”。  
   - 当 `nums[mid]` 小于 `target` 时，说明左边全不可能，区间左移到 `mid + 1`。  
   - 当 `nums[mid]` 大于等于 `target` 时，说明目标可能在左边或正好在 `mid`，所以把右指针收紧到 `mid - 1`，并记录下 `mid` 为候选左边界。

2. **找右边界**  
   - 目标是“最后一个 <= target 的位置”。  
   - 当 `nums[mid]` 大于 `target` 时，右边全不可能，区间右移到 `mid - 1`。  
   - 当 `nums[mid]` 小于等于 `target` 时，说明目标可能在右边或正好在 `mid`，所以把左指针收紧到 `mid + 1`，并记录下 `mid` 为候选右边界。

如果左边界或右边界最终没有找到（即对应的下标超出数组或对应的值不等于 `target`），就返回 `[-1, -1]`。

> **类比**：把数组想象成一本排好序的字典，左边界相当于“找出第一个出现‘target’这个词的页码”，右边界相当于“找出最后一个出现‘target’这个词的页码”。二分查找就像是先打开中间的页码，根据词是否在左半边或右半边，快速缩小范围。

#### 代码（Python）

```python
def searchRange(nums, target):
    """
    最优解：两次二分查找，分别得到左边界和右边界。
    复杂度 O(log n)。
    """

    def find_left():
        """返回第一个 >= target 的下标，如果不存在返回 -1"""
        lo, hi = 0, len(nums) - 1
        left = -1               # 记录候选答案
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1    # 目标只可能在右半边
            else:               # nums[mid] >= target
                hi = mid - 1    # 收紧右边界
                if nums[mid] == target:
                    left = mid  # 记录可能的左边界
        return left

    def find_right():
        """返回最后一个 <= target 的下标，如果不存在返回 -1"""
        lo, hi = 0, len(nums) - 1
        right = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] > target:
                hi = mid - 1    # 目标只可能在左半边
            else:               # nums[mid] <= target
                lo = mid + 1    # 收紧左边界
                if nums[mid] == target:
                    right = mid # 记录可能的右边界
        return right

    left = find_left()
    right = find_right()
    # 如果任意一侧没有找到，说明数组里根本没有 target
    if left == -1 or right == -1:
        return [-1, -1]
    return [left, right]
```

#### 复杂度

- **时间复杂度**：`O(log n)` — 每次二分查找最多只会把搜索区间缩小一半，执行次数约为 `log₂(n)`，大约是“数组长度的对数”。相比暴力的 `O(n)`，当数组很大时快很多。  
- **空间复杂度**：`O(1)` — 只用了若干整数变量，未使用额外的随 `n` 增长的数据结构。

---

## 心得

- **核心技巧**：二分查找（Binary Search）——在有序数组中通过“不断折半”来快速定位目标。  
- **适用的题型**：  
  1. 在有序数组中寻找某个数的出现次数或边界（如本题）。  
  2. 在有序数组中找第一个满足条件的元素（如 “寻找左边界的山峰”）。  
  3. 在单调函数或单调序列中寻找阈值（如 “寻找最小的满足条件的容量”）。  
- **一句话总结解题钥匙**：**把“遍历全体”换成“折半定位”，利用数组的有序性即可达到 O(log n)。**

---

## 反思

- **第一反应**：看到“已排序”二字，我立刻想到二分查找，而不是直接遍历。  
- **最容易踩的坑**：  
  - 忘记分别处理左边界和右边界，导致只返回一个下标。  
  - 循环结束后没有再次检查 `nums[left]` 或 `nums[right]` 是否真的等于 `target`（尤其在目标不存在时会误返回错误下标）。  
  - 边界条件处理不当（空数组、全是相同元素、目标在最左或最右），会导致无限循环或索引越界。  
- **下次类似题的第一步**：先确认数组是否有序，若有序立即考虑 **二分查找**；若需要“第一个/最后一个满足条件”，就把二分的比较方向改为 “>=” 或 “<=”。