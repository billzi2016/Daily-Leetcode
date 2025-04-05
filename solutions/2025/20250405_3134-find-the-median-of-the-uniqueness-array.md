# #3134. 唯一性数组的中位数 / Find the Median of the Uniqueness Array

> 难度：困难 · 标签：Array、Hash Table、Binary Search、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/find-the-median-of-the-uniqueness-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. The uniqueness array of nums is the sorted array that contains the number of distinct elements of all the subarrays of nums. In other words, it is a sorted array consisting of distinct(nums[i..j]), for all 0 <= i <= j < nums.length.
Here, distinct(nums[i..j]) denotes the number of distinct elements in the subarray that starts at index i and ends at index j.
Return the median of the uniqueness array of nums.
Note that the median of an array is defined as the middle element of the array when it is sorted in non-decreasing order. If there are two choices for a median, the smaller of the two values is taken.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3]
Output: 1
Explanation:
The uniqueness array of nums is [distinct(nums[0..0]), distinct(nums[1..1]), distinct(nums[2..2]), distinct(nums[0..1]), distinct(nums[1..2]), distinct(nums[0..2])] which is equal to [1, 1, 1, 2, 2, 3] . The uniqueness array has a median of 1. Therefore, the answer is 1.
```

**Example 2:**

```
Input: nums = [3,4,3,4,5]
Output: 2
Explanation:
The uniqueness array of nums is [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3] . The uniqueness array has a median of 2. Therefore, the answer is 2.
```

**Example 3:**

```
Input: nums = [4,3,5,4]
Output: 2
Explanation:
The uniqueness array of nums is [1, 1, 1, 1, 2, 2, 2, 3, 3, 3] . The uniqueness array has a median of 2. Therefore, the answer is 2.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`。`nums` 的唯一性数组是一个已排序的数组，包含 `nums` 所有子数组的不同元素个数。换句话说，它是由 `distinct(nums[i..j])`（子数组 `nums[i..j]` 中不同元素的数量）组成的已排序数组，遍历所有满足 `0 ≤ i ≤ j < nums.length` 的 `(i, j)`。

返回 `nums` 的唯一性数组的中位数。  

> **中位数** 的定义：将数组按非递减顺序排序后，位于中间位置的元素。如果数组长度为偶数，则取两个中间元素中较小的那个。

**示例 1**  
```text
Input: nums = [1,2,3]
Output: 1
Explanation:
唯一性数组为 [distinct(nums[0..0]), distinct(nums[1..1]), distinct(nums[2..2]), distinct(nums[0..1]), distinct(nums[1..2]), distinct(nums[0..2])]
即 [1, 1, 1, 2, 2, 3]。该数组的中位数为 1，故答案为 1。
```

**示例 2**  
```text
Input: nums = [3,4,3,4,5]
Output: 2
Explanation:
唯一性数组为 [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3]。其中位数为 2，故答案为 2。
```

**示例 3**  
```text
Input: nums = [4,3,5,4]
Output: 2
Explanation:
唯一性数组为 [1, 1, 1, 1, 2, 2, 2, 3, 3, 3]。其中位数为 2，故答案为 2。
```

**约束条件**  
- `1 ≤ nums.length ≤ 10^5`  
- `1 ≤ nums[i] ≤ 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把 **所有子数组** 都列举出来，然后逐个统计子数组里不同元素的个数，最后把这些计数值排好序取中位数。

- **子数组**：`nums[i..j]`（左闭右闭），对应生活中的“从第 i 件物品一直拿到第 j 件”。  
- **统计不同元素**：可以把子数组的元素放进一个 **集合（set）**，集合天然去重，集合的大小就是子数组的 **distinct** 数。集合就像 **字典**，把出现过的单词记下来，只要出现一次就算一次。

为什么一定能得到正确答案？  
因为我们 **没有遗漏** 任何合法的 `(i, j)`，也 **没有多算**，每个子数组只统计一次，它的 distinct 值一定会出现在最终的 “uniqueness array”。把所有值排好序后，取中位数自然就是题目要的答案。

**复杂度分析（大白话）**  
- 外层两层循环遍历 `i`、`j`，相当于 **所有子数组**，子数组的数量是 `n·(n+1)/2 ≈ O(n²)`。  
- 对每个子数组我们要把元素放进集合，最坏要遍历子数组本身的长度，累计下来是 **再乘一个 `n`**，于是总时间是 `O(n³)`。如果在遍历 `i` 时把集合“增量”保存下来（每次只往右扩展），可以把每个子数组的统计降到 `O(1)`，整体时间变成 `O(n²)`，空间最多保存一个集合，`O(n)`。

下面的实现采用 **每个左端点 `i` 重建集合** 的方式，时间 `O(n²)`，空间 `O(n)`。

#### 代码（Python）

```python
from typing import List

def median_of_uniqueness_array_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    uniq_counts = []                     # 用来存所有子数组的 distinct 值

    # i 为子数组左端点
    for i in range(n):
        seen = set()                     # 相当于“字典”，记录出现过的数
        # j 为子数组右端点，一直往右扩展
        for j in range(i, n):
            seen.add(nums[j])            # 加入新元素，集合会自动去重
            uniq_counts.append(len(seen))   # 当前子数组的 distinct 数

    uniq_counts.sort()                   # 排序得到 uniqueness array
    m = len(uniq_counts)
    # 中位数定义：如果长度为偶数，取较小的那个
    return uniq_counts[(m - 1) // 2]

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(median_of_uniqueness_array_bruteforce([1, 2, 3]))          # 1
    print(median_of_uniqueness_array_bruteforce([3, 4, 3, 4, 5]))    # 2
    print(median_of_uniqueness_array_bruteforce([4, 3, 5, 4]))       # 2
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  *含义*：当 `n = 10⁴` 时，大约会执行 1 亿次基本操作，已经很慢了；当 `n = 10⁵`（题目上限）时，根本跑不完。

- **空间复杂度**：`O(n)`  
  只需要一个集合保存当前左端点 `i` 到右端点 `j` 之间出现的不同数字，最多会有 `n` 个不同数字。

---

### 2. 最优解

#### 思路  
暴力解慢的根源在于 **枚举所有子数组**。我们需要一种方式 **不显式列举**，而是 **直接判断** 有多少子数组的 distinct 数 ≤ 某个阈值 `x`。如果能在 `O(n)` 时间内算出这个数量，就可以对答案做二分搜索（binary search），因为：

- 当 `x` 很小（比如 `1`）时，满足 `distinct ≤ x` 的子数组很少；
- 当 `x` 很大（比如 `n`）时，几乎所有子数组都满足；
- 随着 `x` 单调增大，满足条件的子数组数量 **不会减少**（单调性），这正好适合二分。

于是我们把原问题转化为：

> **计数问题**：给定 `x`，统计 **子数组数量** 使得 `distinct(nums[i..j]) ≤ x`。

**如何在 O(n) 内完成计数？**  
使用 **滑动窗口（sliding window）** + **哈希表（freq dict）**：

- 维护一个窗口 `[left, right]`，窗口内的不同元素个数 `cntDistinct`。
- `right` 逐步右移，把新元素加入窗口；如果加入后 `cntDistinct` 超过 `x`，就要把 `left` 往右收缩，直到 `cntDistinct ≤ x` 再继续右移。
- 对每个 `right`，窗口左端 `left` 的位置决定了 **以 `right` 为右端点的合法子数组个数**：`right - left + 1`（因为左端可以是 `left, left+1, …, right`，这些子数组的 distinct 都 ≤ x）。
- 累加所有 `right` 的贡献，即得到满足条件的子数组总数。

这一步类似 “统计子数组的和 ≤ K” 的经典滑动窗口，只是把“和”换成了“不同元素个数”。

**二分搜索答案**  

- `low = 1`（最小可能的 distinct）  
- `high = n`（最大可能的 distinct）  
- 每次取 `mid = (low + high) // 2`，用上面的滑动窗口计数函数 `cnt_subarrays(mid)` 判断：
  - 如果 `cnt_subarrays(mid) >= need`（`need` 为中位数位置的下标 + 1），说明 **中位数 ≤ mid**，把 `high = mid`；
  - 否则说明中位数更大，`low = mid + 1`。  
- `need` 的计算方式：唯一数组长度为 `total = n * (n + 1) // 2`，中位数对应的 **左侧（含自身）** 元素数量最少为 `(total + 1) // 2`。这就是二分判断的阈值。

整个过程的时间复杂度是 **`O(n log n)`**（每次计数 O(n)，二分 log n 次），空间 `O(n)`（哈希表存频率）。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def median_of_uniqueness_array(nums: List[int]) -> int:
    n = len(nums)
    total_sub = n * (n + 1) // 2               # 所有子数组的总数
    need = (total_sub + 1) // 2                # 中位数左侧（含自身）最少要有多少个

    # -------------------------------------------------
    # 计数函数：返回 distinct <= limit 的子数组数量
    # -------------------------------------------------
    def count_le(limit: int) -> int:
        freq = defaultdict(int)               # 哈希表：元素 -> 出现次数
        left = 0
        distinct = 0
        cnt = 0

        for right, val in enumerate(nums):
            # 把右端点加入窗口
            if freq[val] == 0:                 # 之前窗口里没有这个数
                distinct += 1
            freq[val] += 1

            # 若不同元素个数超过 limit，左端收缩
            while distinct > limit:
                left_val = nums[left]
                freq[left_val] -= 1
                if freq[left_val] == 0:        # 完全移出窗口
                    distinct -= 1
                left += 1

            # 此时窗口 [left, right] 合法，所有以 right 为右端点的子数组都合法
            cnt += (right - left + 1)
        return cnt

    # -------------------------------------------------
    # 二分搜索答案
    # -------------------------------------------------
    lo, hi = 1, n          # distinct 的取值范围必然在 [1, n]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= need:   # 中位数不大于 mid
            hi = mid
        else:                       # 中位数更大
            lo = mid + 1
    return lo

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(median_of_uniqueness_array([1, 2, 3]))          # 1
    print(median_of_uniqueness_array([3, 4, 3, 4, 5]))    # 2
    print(median_of_uniqueness_array([4, 3, 5, 4]))       # 2
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  *含义*：对长度为 `10⁵` 的数组，`log n` 约为 `17`，所以整体约 `1.7·10⁶` 次基本操作，轻松跑完。

- **空间复杂度**：`O(n)`（哈希表 `freq` 最多保存 `n` 个不同数字的计数）。  

与暴力解相比，时间从 **平方级** 降到了 **线性乘对数**，在大数据下差距天壤之别。

---

## 心得

- **核心技巧**：  
  1. 把“找中位数”转化为“判断有多少元素 ≤ x”，利用单调性做二分搜索。  
  2. 用 **滑动窗口 + 哈希表** 在线性时间内统计满足 “distinct ≤ x” 的子数组数量。

- **此技巧常见的类似题**：  
  - “子数组中位数” / “子数组第 K 小数” 类问题（LeetCode 2488）。  
  - “最长子数组满足不同元素 ≤ K” （滑动窗口的典型练习）。  
  - “统计子数组和 ≤ K” （两指针/前缀和 + 二分）。

- **一句话总结解题钥匙**：  
  **“把全局排序的中位数问题转化为单调计数，然后用滑动窗口一次遍历完成计数”。**

---

## 反思

- **第一反应**：直接枚举所有子数组，统计 distinct，随后排序取中位数。  
- **最容易踩的坑**：  
  1. **计数溢出**：子数组总数 `n·(n+1)/2` 在 `n=10⁵` 时约 `5·10⁹`，需要用 64 位整数（Python 自动大整数，但在 C++/Java 要注意 long long）。  
  2. **窗口收缩条件**：忘记在 `while distinct > limit` 循环里同步更新 `distinct`，会导致死循环。  
  3. **二分的边界**：中位数定义为“若偶数取较小”，所以判断条件应是 `cnt >= need`（左侧至少 `need` 个），而不是 `> need`。

- **下次遇到同类题**：  
  第一步先 **思考能否把目标值转化为单调函数的阈值**（如 ≤ x），如果可以，就立刻考虑 **二分 + 线性计数**（滑动窗口、前缀和或 BIT/Fenwick）来实现 O(n log n) 的高效解法。