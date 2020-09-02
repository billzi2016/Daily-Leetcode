# #977. 有序数组的平方 / Squares of a Sorted Array

> 难度：简单 · 标签：Array、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/squares-of-a-sorted-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.

**Examples**

**Example 1:**

```
Input: nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: After squaring, the array becomes [16,1,0,9,100].
After sorting, it becomes [0,1,9,16,100].
```

**Example 2:**

```
Input: nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]
```

**Constraints**

- 1 <= nums.length <= 104
- -104 <= nums[i] <= 104
- nums is sorted in non-decreasing order.

---

## 题目（中文翻译）

给定一个按非递减顺序 (non-decreasing order) 排序的整数数组 (integer array) `nums`，返回一个数组，其中包含每个数字的平方，且该数组按非递减顺序 (non-decreasing order) 排序。

**示例 1**  
Input: `nums = [-4,-1,0,3,10]`  
Output: `[0,1,9,16,100]`  
解释：平方后，数组变为 `[16,1,0,9,100]`。排序后，数组变为 `[0,1,9,16,100]`。

**示例 2**  
Input: `nums = [-7,-3,2,3,11]`  
Output: `[4,9,9,49,121]`

**约束条件**  
- `1 <= nums.length <= 10^4`  
- `-10^4 <= nums[i] <= 10^4`  
- `nums` 已按非递减顺序排序。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：  
1. 先把数组里的每个数求平方，得到一个新数组。  
2. 再把这个新数组排序，得到非递减（从小到大）的结果。  

这里用到的**排序**可以类比成把一堆纸条按照大小顺序排好——不管纸条本身是正数还是负数，只要把它们的“大小”（这里是平方后的数值）排好序，就完成了任务。  

这种方法一定能得到正确答案，因为  
- 每个数都被平方一次，保证了“每个数的平方都出现”。  
- 排序保证了“所有平方后的数按照从小到大的顺序排列”。  

#### 代码（Python）  
```python
from typing import List

def sortedSquares(nums: List[int]) -> List[int]:
    # 1. 把每个数平方，得到新的列表
    squares = [x * x for x in nums]          # 列表推导式，遍历 nums 并平方
    # 2. 对平方后的列表进行排序
    squares.sort()                           # 原地排序，时间复杂度 O(n log n)
    return squares
```

#### 复杂度  
- **时间复杂度**：`O(n log n)`  
  - `n` 是数组长度。遍历一次求平方是 `O(n)`，排序是 `O(n log n)`，两者相加仍是 `O(n log n)`。  
  - 用大白话说，就是“比线性快一点点，但比平方慢很多”。  

- **空间复杂度**：`O(n)`  
  - 需要额外的数组 `squares` 来保存每个数的平方，大小和原数组一样。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**排序**是耗时的关键。  
如果我们仔细观察原数组的特性，会发现：

- 原数组是 **非递减** 排序的。  
- 负数的绝对值大，平方后会变成 **大数**；正数越大，平方后也越大。  

因此，最大的平方一定出现在 **数组的两端**（最左边的负数或最右边的正数）。  

**双指针**技巧：  
- 左指针 `l` 从数组最左端（最小的负数）开始，右指针 `r` 从最右端（最大的正数）开始。  
- 比较 `abs(nums[l])` 与 `abs(nums[r])`，把较大的平方放到结果数组的**最右边**（从后往前填）。  
- 放完后对应的指针向中间收拢（如果左边的大，就 `l += 1`；否则 `r -= 1`）。  
- 重复上述过程，直到所有位置都填满。  

这就像把两只手分别抓住一根绳子两端的石头，比较哪只手抓的石头更重，就把重的石头放到箱子最底下（结果数组的最后），然后把那只手的石头放下，继续比较。这样只需要一次线性遍历，就能得到有序的平方数组。

#### 代码（Python）  
```python
from typing import List

def sortedSquares(nums: List[int]) -> List[int]:
    n = len(nums)
    # 结果数组，预先分配好长度，后面从右往左填
    result = [0] * n
    # 双指针，分别指向数组最左和最右
    left, right = 0, n - 1
    # fill_pos 表示当前要填的位置，从数组最右侧开始
    fill_pos = n - 1

    while left <= right:
        left_sq = nums[left] * nums[left]      # 左指针对应的平方
        right_sq = nums[right] * nums[right]   # 右指针对应的平方

        # 把较大的平方放到 result[fill_pos]，然后移动对应的指针
        if left_sq > right_sq:
            result[fill_pos] = left_sq
            left += 1          # 左边已经用掉，向中间靠拢
        else:
            result[fill_pos] = right_sq
            right -= 1         # 右边已经用掉，向中间靠拢

        fill_pos -= 1          # 下一次填到左边一个位置

    return result
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每次比较、写入都是 `O(1)`，所以整体是线性时间。  
  - 相比暴力解的 `O(n log n)`，这就是把“排序的那把刀”直接省掉了。  

- **空间复杂度**：`O(n)`（如果把结果直接写回原数组，可以认为是 `O(1)` 额外空间）  
  - 需要一个同样大小的数组来存放答案，属于输出空间。  

---  

## 心得  

- **核心技巧**：双指针（Two Pointers）利用有序数组的两端特性，一次遍历完成排序。  
- **适用的题型**：  
  1. “有序数组合并”类（如合并两个有序数组得到有序结果）。  
  2. “寻找两数之和的最接近值”类（如两数之和最接近目标）。  
  3. “删除有序数组中的重复元素”类（利用快慢指针）。  
- **一句话总结**：  
  > 当数组已经有序时，最大（或最小）值一定在两端，利用双指针从两端向中间收敛，可把排序的成本降到 `O(n)`。  

---  

## 反思  

- **第一反应**：直接把每个数平方后再排序，最符合直觉。  
- **最容易踩的坑**：  
  - 忘记负数平方后会变大，导致错误地只从左到右遍历。  
  - 边界条件处理不当（如 `left` 与 `right` 重合时仍需比较）。  
  - 结果数组的填充顺序写错，导致倒序。  
- **下次类似题的第一步**：  
  > 先问自己“数组已经排好序了吗？如果是，最大/最小值会出现在两端吗？”——若答案是肯定的，就尝试用双指针或类似的线性技巧来直接构造答案。