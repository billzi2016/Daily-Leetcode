# #35. 搜索插入位置 / Search Insert Position

> 难度：简单 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/search-insert-position/)

---

## 题目（英文原版）

**Description**

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
You must write an algorithm with O(log n) runtime complexity.

**Examples**

**Example 1:**

```
Input: nums = [1,3,5,6], target = 5
Output: 2
```

**Example 2:**

```
Input: nums = [1,3,5,6], target = 2
Output: 1
```

**Example 3:**

```
Input: nums = [1,3,5,6], target = 7
Output: 4
```

**Constraints**

- 1 <= nums.length <= 104
- -104 <= nums[i] <= 104
- nums contains distinct values sorted in ascending order.
- -104 <= target <= 104

---

## 题目（中文翻译）

**描述**  
给定一个升序排列且元素互不相同的整数数组（sorted array of distinct integers）`nums`，以及一个目标值（target）`target`。如果在数组中找到了目标值，返回其下标（index）；如果未找到，则返回如果将目标值按顺序插入数组后应该所在的下标。  
要求实现的算法时间复杂度为 **O(log n)**。

**示例**  

示例 1  
```
输入: nums = [1,3,5,6], target = 5
输出: 2
```

示例 2  
```
输入: nums = [1,3,5,6], target = 2
输出: 1
```

示例 3  
```
输入: nums = [1,3,5,6], target = 7
输出: 4
```

**约束条件**  

- `1 <= nums.length <= 10^4`  
- `-10^4 <= nums[i] <= 10^4`  
- `nums` 中的值互不相同，且按升序排列。  
- `-10^4 <= target <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从左到右顺序遍历**数组 `nums`，逐个比较元素和 `target` 的大小：

- 如果当前元素正好等于 `target`，直接返回它的下标。
- 如果当前元素已经大于 `target`，说明 `target` 应该插在它的左侧，返回当前下标即可。
- 如果遍历完整个数组都没有出现上述两种情况，说明 `target` 大于所有元素，应该插到数组末尾，返回 `len(nums)`。

这里使用的唯一数据结构是**列表**本身，遍历时就像在排队买票，一人检查一次，找到合适的位置就停下来。

这种做法一定能得到正确答案，因为我们按照数组的升序顺序逐个检查，必然能找到第一个不小于 `target` 的位置（若不存在则在末尾）。

#### 代码（Python）

```python
def searchInsert(nums, target):
    """
    暴力线性扫描
    :param nums: List[int] 已经排好序的数组（不含重复元素）
    :param target: int 需要查找或插入的目标值
    :return: int 目标值所在或应插入的位置下标
    """
    for i, num in enumerate(nums):
        # 如果当前元素已经不小于 target，说明 target 应该在 i 位置
        if num >= target:
            return i
    # 循环结束说明 target 大于所有元素，插到数组末尾
    return len(nums)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  “O(n)” 的意思是最坏情况下要检查 `n` 次，也就是数组长度这么多次。比如 `target` 最大，比所有元素都大时，需要遍历完整个数组。

- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量（循环计数器 `i`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要检查所有元素**，当数组很长（上限 10⁴）时会比较慢。  
题目要求 **O(log n)** 的时间，这正是**二分查找**的时间复杂度。

二分查找的核心思想可以比作**在一本有序的字典里找单词**：

1. 先把字典对折，看中间的单词是比目标大还是小。
2. 如果目标比中间的单词小，就只在左半边继续对折查找；否则只在右半边继续。
3. 这样每一步都把搜索范围缩小一半，最多只需要 `log₂n` 次比较。

对本题而言，我们需要的不是“是否存在”，而是**第一个不小于 target 的位置**。二分查找天然返回的就是这个位置：

- 设 `left = 0, right = len(nums) - 1`（闭区间）。
- 循环条件 `left <= right`，取中点 `mid = (left + right) // 2`。
- 如果 `nums[mid] < target`，说明目标在右侧，`left = mid + 1`。
- 否则（`nums[mid] >= target`），目标在左侧或正好在 `mid`，把 `right = mid - 1`。
- 循环结束时，`left` 正好指向第一个不小于 `target` 的位置（也可能是数组末尾）。

下面的实现使用 **闭区间**（`[left, right]`）写法，逻辑清晰，容易写对。

#### 代码（Python）

```python
def searchInsert(nums, target):
    """
    二分查找：返回第一个不小于 target 的下标
    :param nums: List[int] 已排序且无重复的数组
    :param target: int 目标值
    :return: int 插入位置的下标
    """
    left, right = 0, len(nums) - 1   # 初始化搜索区间为整个数组

    while left <= right:             # 只要区间非空就继续
        mid = (left + right) // 2    # 取中点（整数除法）

        if nums[mid] < target:       # 中点值太小，目标在右侧
            left = mid + 1
        else:                        # 中点值大于等于目标，目标在左侧或就在 mid
            right = mid - 1

    # 循环结束时 left == right + 1，恰好是第一个不小于 target 的位置
    return left
```

#### 复杂度  

- **时间复杂度**：`O(log n)`  
  每一次循环把搜索区间长度减半，最多需要 `log₂n` 次比较。比如 `n = 10⁴`，只需要约 14 次就能定位。

- **空间复杂度**：`O(1)`  
  只用了常数个变量 `left, right, mid`，不随输入规模增长。

---

## 心得

- **核心技巧**：二分查找（Binary Search）——在有序结构中“每次砍掉一半”寻找目标。
- **适用题型**：  
  1. 在有序数组中查找元素位置（如 `Search Insert Position`）。  
  2. 求满足某个单调条件的最左/最右边界（如 “寻找左侧边界” 题目）。  
  3. 在数轴上寻找最小满足条件的数（如 “找出最小的可行解”）。
- **解题钥匙**：**先确认数组有序 → 再用二分把搜索空间快速压缩**。

## 反思

- **第一反应**：看到“已排序”，立刻想到二分查找；若忽视排序会误走暴力路线。
- **最容易踩的坑**：  
  - 循环结束后返回 `left` 而不是 `mid`（`mid` 可能已经失效）。  
  - 边界条件处理不当导致无限循环（如 `mid = (left + right) // 2` 必须使用整数除法）。  
  - 当 `target` 小于所有元素或大于所有元素时，要确保返回 0 或 `len(nums)`，二分实现天然满足。
- **下次第一步**：先判断数组是否有序（题目已保证），然后写出二分框架，明确返回值是“左侧边界”。