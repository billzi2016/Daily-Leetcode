# #704. 二分查找 / Binary Search

> 难度：简单 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/binary-search/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
You must write an algorithm with O(log n) runtime complexity.

**Examples**

**Example 1:**

```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

**Example 2:**

```
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1
```

**Constraints**

- 1 <= nums.length <= 104
- -104 < nums[i], target < 104
- All the integers in nums are unique.
- nums is sorted in ascending order.

---

## 题目（中文翻译）

给定一个按升序（ascending order）排序的整数数组（array）`nums`，以及一个整数目标值（target），请编写一个函数在 `nums` 中搜索 `target`。如果 `target` 存在，返回其索引（index）；否则返回 `-1`。要求实现的算法的运行时间复杂度（runtime complexity）为 `O(log n)`。

示例 1：

示例 2：

约束条件：

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- `nums` 中的所有整数互不相同。
- `nums` 按升序（ascending order）排序。

示例：

**示例 1**  
输入: `nums = [-1,0,3,5,9,12], target = 9`  
输出: `4`  
解释: `9` 存在于 `nums` 中，其索引为 `4`。

**示例 2**  
输入: `nums = [-1,0,3,5,9,12], target = 2`  
输出: `-1`  
解释: `2` 不存在于 `nums` 中，返回 `-1`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的办法就是把数组从左到右逐个查看，看看哪个位置的元素等于 `target`。  
- **使用的数据结构**：只需要原来的数组 `nums`，不需要额外的结构。可以把数组想象成一本排好序的电话簿，**线性遍历**就像我们一本一本翻页查找某个名字，虽然能找到，但效率不高。  
- **为什么正确**：因为我们把每个元素都检查了一遍，只要有等于 `target` 的，就一定会被发现；如果遍历结束仍未找到，说明数组里根本不存在该数。  

#### 代码（Python）  

```python
def search(nums, target):
    """
    线性遍历实现：逐个检查 nums 中的元素是否等于 target
    """
    for i in range(len(nums)):          # 从下标 0 开始遍历到最后
        if nums[i] == target:           # 找到相等的元素
            return i                    # 返回它的下标
    return -1                           # 循环结束仍未找到，返回 -1
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— “O” 表示数量级，`n` 是数组长度。意思是最坏情况下我们要看 `n` 次（比如目标根本不在数组里），所以时间会随数组大小线性增长。  
- **空间复杂度**：`O(1)` —— 只用了常数级别的额外空间（几个变量），不随 `n` 增长。

---  

### 2. 最优解  

#### 思路  

**慢点在哪儿？**  
线性遍历的瓶颈在于每次只能检查一个元素，必须把所有元素都走一遍。  
**利用数组已排序的特性**：因为 `nums` 是严格递增的，我们可以把搜索范围每次都 **二分**——把区间长度缩小一半，类似在一本有目录的书里查找章节：先看中间的章节标题，大于目标就去左半边，小于目标就去右半边，反复如此，快速定位。  

**核心算法——二分查找**  
1. 维护两个指针 `left`（区间左端）和 `right`（区间右端），初始分别指向数组的第一个和最后一个元素。  
2. 当 `left <= right` 时，取中点 `mid = (left + right) // 2`。  
3. 比较 `nums[mid]` 与 `target`：  
   - 若相等，直接返回 `mid`。  
   - 若 `nums[mid] < target`，说明目标只可能在右半边，把 `left` 移到 `mid + 1`。  
   - 若 `nums[mid] > target`，说明目标只可能在左半边，把 `right` 移到 `mid - 1`。  
4. 循环结束仍未找到，说明数组中没有目标，返回 `-1`。  

**为什么是 O(log n)**  
每一次循环都把搜索区间长度 **除以 2**，所以循环次数大约是 `log₂ n`（对数），即使 `n` 达到 10⁴，循环也只需要约 14 次，极其快速。  

#### 代码（Python）  

```python
def search(nums, target):
    """
    二分查找实现：利用数组已排序的特性，在 O(log n) 时间内定位 target
    """
    left, right = 0, len(nums) - 1      # 初始化搜索区间的左右边界

    while left <= right:                # 只要区间还有元素就继续
        mid = (left + right) // 2       # 取区间中点（向下取整）

        if nums[mid] == target:         # 命中目标，直接返回下标
            return mid

        if nums[mid] < target:          # 中点值太小，目标在右半边
            left = mid + 1              # 排除左半区，包括 mid 本身
        else:                           # 中点值太大，目标在左半边
            right = mid - 1             # 排除右半区，包括 mid 本身

    return -1                           # 循环结束仍未找到，返回 -1
```

#### 复杂度  

- **时间复杂度**：`O(log n)` —— “log” 表示对数，意味着即使数组很大，搜索次数也只会随 **log₂ n** 增长，远快于线性遍历。  
- **空间复杂度**：`O(1)` —— 只用了固定数量的变量 (`left`, `right`, `mid`)，不随 `n` 增长。

## 心得  

- **核心技巧**：二分查找（Binary Search），利用有序结构把搜索范围每次减半。  
- **适用的题型**：  
  1. 在有序数组中查找元素（本题）。  
  2. 寻找有序数组中满足某种单调条件的最左/最右位置（如 “寻找左边界”）。  
  3. 在单调函数的定义域内求解方程的根（如 “山峰数组的峰值”）。  
- **一句话总结**：**把“逐个检查”换成“每次砍掉一半”，就是二分的魔法钥匙。**  

## 反思  

- **第一反应**：看到“已排序”，立刻想到二分查找，因为它是处理有序数据的标配。  
- **最容易踩的坑**：  
  - 边界条件处理不当（比如 `mid` 计算方式、`left/right` 更新时是否越界）。  
  - 忽视了数组可能只有一个元素的特殊情况。  
  - 在 Python 中使用 `//` 整除防止出现浮点数。  
- **下次遇到同类题的第一步**：先确认数据是否具备单调/有序性质，若有，则立刻构思 **“二分”** 的搜索区间或条件。