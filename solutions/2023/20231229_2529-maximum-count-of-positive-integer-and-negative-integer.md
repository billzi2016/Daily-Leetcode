# #2529. 正整数与负整数的最大计数 / Maximum Count of Positive Integer and Negative Integer

> 难度：简单 · 标签：Array、Binary Search、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-count-of-positive-integer-and-negative-integer/)

---

## 题目（英文原版）

**Description**

Given an array nums sorted in non-decreasing order, return the maximum between the number of positive integers and the number of negative integers.
Note that 0 is neither positive nor negative.
Follow up: Can you solve the problem in O(log(n)) time complexity?

**Examples**

**Example 1:**

```
Input: nums = [-2,-1,-1,1,2,3]
Output: 3
Explanation: There are 3 positive integers and 3 negative integers. The maximum count among them is 3.
```

**Example 2:**

```
Input: nums = [-3,-2,-1,0,0,1,2]
Output: 3
Explanation: There are 2 positive integers and 3 negative integers. The maximum count among them is 3.
```

**Example 3:**

```
Input: nums = [5,20,66,1314]
Output: 4
Explanation: There are 4 positive integers and 0 negative integers. The maximum count among them is 4.
```

**Constraints**

- 1 <= nums.length <= 2000
- -2000 <= nums[i] <= 2000
- nums is sorted in a non-decreasing order.

---

## 题目（中文翻译）

给定一个已按非递减顺序排序的整数数组（array）`nums`，返回正整数（positive integer）的数量与负整数（negative integer）的数量之中的最大值。  
注意，`0` 既不是正数也不是负数。

**示例 1**  
**输入**: `nums = [-2,-1,-1,1,2,3]`  
**输出**: `3`  
**解释**: 正整数有 `3` 个，负整数也有 `3` 个，两者的最大计数为 `3`。

**示例 2**  
**输入**: `nums = [-3,-2,-1,0,0,1,2]`  
**输出**: `3`  
**解释**: 正整数有 `2` 个，负整数有 `3` 个，最大计数为 `3`。

**示例 3**  
**输入**: `nums = [5,20,66,1314]`  
**输出**: `4`  
**解释**: 正整数有 `4` 个，负整数为 `0`，最大计数为 `4`。

**约束条件**  
- `1 <= nums.length <= 2000`  
- `-2000 <= nums[i] <= 2000`  
- `nums` 按非递减顺序排序。

**后续问题**  
你能在 `O(log(n))` 时间复杂度内解决此问题吗？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是一次遍历数组，分别统计 **正数** 和 **负数** 的个数。  
- **数据结构**：只需要两个整数变量 `pos_cnt`、`neg_cnt` 来计数。可以把它想象成在超市里数「红色商品」和「蓝色商品」的数量，手里只拿着两个记数牌就行了。  
- **正确性**：因为题目只要求比较正数和负数的数量，遍历一次就能把每个元素归类到「正」或「负」或「零」——零不计数，最后两者中大的那个就是答案。  

#### 代码（Python）

```python
def maxCount(nums):
    # 用两个计数器分别统计正数和负数的数量
    pos_cnt = 0          # 正数个数
    neg_cnt = 0          # 负数个数

    for x in nums:       # 逐个检查数组里的元素
        if x > 0:        # 大于 0 的就是正数
            pos_cnt += 1
        elif x < 0:      # 小于 0 的就是负数
            neg_cnt += 1
        # 等于 0 的不计数，直接跳过

    # 返回两者的最大值
    return max(pos_cnt, neg_cnt)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  这里的 `n` 是数组长度。遍历一次数组，每个元素只看一次，花的时间和元素个数成正比。可以把 `O(n)` 想象成「走过 n 步」——步数多了自然花的时间多。  
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（两个计数器），不随 `n` 增大而增加内存。

---

### 2. 最优解

#### 思路  

虽然一次遍历已经是 `O(n)`，但题目给出的 **Follow up** 要求 `O(log n)`，这提示我们可以利用 **二分查找**（Binary Search）来加速。  
- **慢在哪里**：在暴力解里，我们把每个元素都检查了一遍。其实我们只关心 **正数出现的起始位置** 与 **负数结束的位置**。因为数组已经排好序（从小到大），负数一定在左边，正数一定在右边，零（如果有）在中间。只要找到这两个分界点，就能直接算出负数和正数的个数。  
- **二分查找**：二分查找的思想是“把区间一分为二”，每次把搜索范围缩小一半，直到找到目标位置。可以把它类比为在一本字典里找单词：先翻到中间的页码，根据字母顺序决定往前还是往后翻，最终快速定位。  

**关键步骤**  
1. **找第一个正数的下标**（即最左侧 `>0` 的位置）。  
   - 用二分查找：如果 `mid` 位置的数大于 0，则可能是答案，也要继续往左找；否则（≤0）说明正数在右边。  
2. **找最后一个负数的下标**（即最右侧 `<0` 的位置）。  
   - 同理，如果 `mid` 位置的数小于 0，则可能是答案，也要往右找；否则（≥0）说明负数在左边。  
3. 根据下标算出数量  
   - 正数个数 = `len(nums) - first_pos_index`（如果找不到正数，则为 0）。  
   - 负数个数 = `last_neg_index + 1`（如果找不到负数，则为 0）。  
4. 返回两者的最大值。

#### 代码（Python）

```python
def maxCount(nums):
    n = len(nums)

    # ---------- 1. 找第一个正数的下标 ----------
    left, right = 0, n - 1
    first_pos = n          # 默认值 n 表示数组里没有正数
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] > 0:              # 当前是正数，可能是最左侧正数
            first_pos = mid            # 记录下来
            right = mid - 1            # 继续往左查找更早的正数
        else:                           # ≤0，正数一定在右边
            left = mid + 1

    # ---------- 2. 找最后一个负数的下标 ----------
    left, right = 0, n - 1
    last_neg = -1          # 默认值 -1 表示数组里没有负数
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < 0:               # 当前是负数，可能是最右侧负数
            last_neg = mid              # 记录下来
            left = mid + 1             # 继续往右查找更晚的负数
        else:                           # ≥0，负数一定在左边
            right = mid - 1

    # ---------- 3. 计算正负数的数量 ----------
    pos_cnt = n - first_pos if first_pos < n else 0   # 正数个数
    neg_cnt = last_neg + 1 if last_neg >= 0 else 0   # 负数个数

    # ---------- 4. 返回最大值 ----------
    return max(pos_cnt, neg_cnt)
```

#### 复杂度  

- **时间复杂度**：`O(log n)`  
  二分查找每次把搜索区间长度减半，最多进行 `log₂ n` 次比较。可以把它想象成「每走一步都能把剩下的路程减半」，所以即使 `n` 很大，花的时间也很少。  
- **空间复杂度**：`O(1)`  
  只用了固定数量的变量（下标、计数器），不随输入规模增长。

---

## 心得

- **核心技巧**：利用数组的有序性，用二分查找快速定位「正数起点」和「负数终点」。
- **适用的题型**  
  1. 在排好序的数组中找第一个大于/小于某个值的元素（比如 “搜索插入位置”）。  
  2. 统计区间内满足条件的元素个数（比如 “有序数组中的区间和”）。  
- **一句话总结解题钥匙**：**有序 ⇒ 用二分定位边界 ⇒ O(log n) 计数**。

---

## 反思

- **第一反应**：直接遍历计数，觉得已经够快了。  
- **最容易踩的坑**  
  - 没有正数或没有负数时，二分查找的返回值需要特殊处理（如 `first_pos = n`、`last_neg = -1`），否则会算出负数的个数为 `0` 或正数的个数为错误值。  
  - 当数组全为负数或全为正数时，边界条件的判断尤为重要。  
- **下次类似题的第一步**：先检查数组是否已排序；如果是，立刻想到 **二分** 来定位 **阈值/边界**，再根据边界算出所需的计数或范围。