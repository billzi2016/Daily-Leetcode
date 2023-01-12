# #2089. 排序数组后查找目标索引 / Find Target Indices After Sorting Array

> 难度：简单 · 标签：Array、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-target-indices-after-sorting-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and a target element target.
A target index is an index i such that nums[i] == target.
Return a list of the target indices of nums after sorting nums in non-decreasing order. If there are no target indices, return an empty list. The returned list must be sorted in increasing order.

**Examples**

**Example 1:**

```
Input: nums = [1,2,5,2,3], target = 2
Output: [1,2]
Explanation: After sorting, nums is [1,2,2,3,5].
The indices where nums[i] == 2 are 1 and 2.
```

**Example 2:**

```
Input: nums = [1,2,5,2,3], target = 3
Output: [3]
Explanation: After sorting, nums is [1,2,2,3,5].
The index where nums[i] == 3 is 3.
```

**Example 3:**

```
Input: nums = [1,2,5,2,3], target = 5
Output: [4]
Explanation: After sorting, nums is [1,2,2,3,5].
The index where nums[i] == 5 is 4.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i], target <= 100

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 **nums** 和一个目标元素 **target**。  
**目标索引 (target index)** 定义为满足 `nums[i] == target` 的下标 **i**。  
请在对 **nums** 按非递减顺序（non-decreasing order）进行排序后，返回所有 **目标索引** 的列表。若不存在目标索引，则返回空列表。返回的列表必须按递增顺序排列。

**示例 1**  
**输入**: `nums = [1,2,5,2,3], target = 2`  
**输出**: `[1,2]`  
**解释**: 排序后，`nums` 为 `[1,2,2,3,5]`。`nums[i] == 2` 的下标是 **1** 和 **2**。

**示例 2**  
**输入**: `nums = [1,2,5,2,3], target = 3`  
**输出**: `[3]`  
**解释**: 排序后，`nums` 为 `[1,2,2,3,5]`。`nums[i] == 3` 的下标是 **3**。

**示例 3**  
**输入**: `nums = [1,2,5,2,3], target = 5`  
**输出**: `[4]`  
**解释**: 排序后，`nums` 为 `[1,2,2,3,5]`。`nums[i] == 5` 的下标是 **4**。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i], target <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**先把数组排好序**，再把排好序后的数组里等于 `target` 的下标全部找出来。

- **排序**：把一堆乱糟糟的数字变成从小到大的顺序。Python 的 `sorted()` 函数就像把书按字母顺序排好，查找时更方便。
- **遍历**：从左到右逐个检查每个位置的数是否等于 `target`，相等就把下标记下来。遍历过程类似“顺着排好序的书架逐本查看”，一旦看到目标词就记下它所在的书架编号。

> **为什么正确**  
> 排序后，所有相同的数会聚在一起，遍历一次即可完整捕获所有目标位置。因为题目要求返回的是**排序后**的下标，这一步正好满足需求。

#### 代码（Python）

```python
def targetIndices(nums: list[int], target: int) -> list[int]:
    # 1️⃣ 先把数组排好序，sorted 返回的是一个新列表，不会改动原数组
    sorted_nums = sorted(nums)                # 例： [1,2,5,2,3] -> [1,2,2,3,5]

    # 2️⃣ 再遍历排好序的数组，找出所有等于 target 的位置
    res = []
    for i, v in enumerate(sorted_nums):       # enumerate 同时得到下标 i 和对应的值 v
        if v == target:                       # 如果值等于目标
            res.append(i)                     # 记录下标
    return res
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  排序是最耗时的步骤，常用的比较排序（如快速排序、归并排序）在最坏情况下都需要 `n log n` 次比较。遍历一次是 `O(n)`，相较于排序可以忽略不计。  
  > **大白话**：如果有 1000 个数字，要排好序大概需要 1000 × log₂1000 ≈ 10 000 次“比较”操作，远比一次遍历（1000 次）要多。

- **空间复杂度**：`O(n)`  
  `sorted()` 会创建一个新列表，额外占用和原数组同样大小的空间。返回的结果列表最坏也会占 `O(n)`（所有元素都相同的情况）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在**排序**这一步。因为 `nums` 的长度只有 ≤ 100，`O(n log n)` 已经足够快。但如果想在更大规模的数据上进一步提升效率，可以**利用二分查找**在已经排好序的数组中直接定位目标值的左边界和右边界，从而只需要 `O(log n)` 的时间查找，而不必遍历整个数组。

优化步骤：

1. **排序**：仍然需要一次 `O(n log n)` 的排序（因为题目要求返回的是排序后的下标，不能省掉这一步）。
2. **二分左边界**：在排好序的数组里，用二分查找找出第一个等于 `target` 的位置。二分查找把搜索范围每次都 **砍掉一半**，所以只需要 `log₂ n` 次比较。
3. **二分右边界**：同理，找出最后一个等于 `target` 的位置（或找出第一个大于 `target` 的位置再减一）。
4. **生成答案**：如果左边界不存在（说明数组里根本没有 `target`），直接返回空列表。否则从左边界到右边界依次加入下标即可，仍然是线性（但长度是目标出现的次数，最多 `n`，且这一步本身不可避免）。

核心概念解释：

- **二分查找**：把有序的书架想象成一本字典，想找某个词的起始页码时，我们先打开中间页，判断词在前半部还是后半部，然后只在那一半继续搜索。每次都把范围缩小一半，效率很高。
- **左边界**：第一个等于目标的下标。相当于“目标词第一次出现的页码”。
- **右边界**：最后一个等于目标的下标。相当于“目标词最后一次出现的页码”。

#### 代码（Python）

```python
def targetIndices(nums: list[int], target: int) -> list[int]:
    # 1️⃣ 排序（必须的，因为题目要求返回排序后数组的下标）
    sorted_nums = sorted(nums)

    # ---------- 二分查找左边界 ----------
    left, right = 0, len(sorted_nums) - 1
    left_bound = -1                     # -1 表示未找到
    while left <= right:
        mid = (left + right) // 2
        if sorted_nums[mid] < target:   # 目标在右侧
            left = mid + 1
        else:                           # sorted_nums[mid] >= target
            if sorted_nums[mid] == target:
                left_bound = mid       # 记录可能的左边界
            right = mid - 1            # 继续向左找更早的出现

    # 如果左边界仍是 -1，说明数组里根本没有 target
    if left_bound == -1:
        return []

    # ---------- 二分查找右边界 ----------
    left, right = 0, len(sorted_nums) - 1
    right_bound = -1
    while left <= right:
        mid = (left + right) // 2
        if sorted_nums[mid] > target:   # 目标在左侧
            right = mid - 1
        else:                           # sorted_nums[mid] <= target
            if sorted_nums[mid] == target:
                right_bound = mid      # 记录可能的右边界
            left = mid + 1             # 继续向右找更晚的出现

    # ---------- 生成结果 ----------
    # 从左边界到右边界（两端都包含）依次加入下标
    return list(range(left_bound, right_bound + 1))
```

#### 复杂度

- **时间复杂度**：`O(n log n)`（排序）+ `O(log n)`（两次二分）+ `O(k)`（生成答案），其中 `k` 为目标出现的次数。整体仍是 `O(n log n)`，但相较于暴力解省掉了遍历整个数组的 `O(n)`，在 `target` 很少出现时会更快。
- **空间复杂度**：`O(n)`（排序产生的新列表）+ `O(k)`（返回的下标列表）。额外的辅助空间仍是线性的。

---

## 心得

- **核心技巧**：先排序，再利用二分查找快速定位目标值的左右边界。
- **适用的题型**：
  1. “在有序数组中查找目标的起始和结束位置”（LeetCode 34. Find First and Last Position of Element in Sorted Array）。
  2. “统计有序数组中某个值出现的次数”（LeetCode 395. Longest Subarray With Maximum Bitwise AND）。
- **一句话总结**：排序后，用二分把“找目标出现的第一本书”和“最后一本书”一步到位。

## 反思

- **第一反应**：先把数组排好序，然后一次遍历把等于 `target` 的下标收集起来——这就是最直观的暴力解。
- **最容易踩的坑**：
  - 忘记在返回前检查是否真的找到了 `target`（左边界为 `-1` 时要返回空列表）。
  - 二分查找的循环条件写错（`left <= right` 必须写对，否则可能漏掉边界）。
  - 生成答案时要包含右边界本身（`range(left, right+1)`），否则会少一个下标。
- **下次类似题的第一步**：先判断“数组是否已经有序”。如果已经有序，直接用二分定位左右边界；如果不确定是否有序，先排序再二分。这样能保证既正确又高效。