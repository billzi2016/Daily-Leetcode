# #4. 两个有序数组的中位数 / Median of Two Sorted Arrays

> 难度：困难 · 标签：Array、Binary Search、Divide and Conquer · [LeetCode 链接](https://leetcode.com/problems/median-of-two-sorted-arrays/)

---

## 题目（英文原版）

**Description**

Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
The overall run time complexity should be O(log (m+n)).

**Examples**

**Example 1:**

```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

**Example 2:**

```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

**Constraints**

- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -106 <= nums1[i], nums2[i] <= 106

---

## 题目（中文翻译）

**描述**  
给定两个已排序的数组 `nums1` 和 `nums2`，大小分别为 `m` 和 `n`，返回这两个已排序数组的中位数。  
整体运行时间复杂度应为 `O(log (m+n))`。

**示例 1**  
输入: `nums1 = [1,3]`, `nums2 = [2]`  
输出: `2.00000`  
解释: 合并后的数组为 `[1,2,3]`，其中位数为 `2`。

**示例 2**  
输入: `nums1 = [1,2]`, `nums2 = [3,4]`  
输出: `2.50000`  
解释: 合并后的数组为 `[1,2,3,4]`，其中位数为 `(2 + 3) / 2 = 2.5`。

**约束条件**  
- `nums1.length == m`  
- `nums2.length == n`  
- `0 ≤ m ≤ 1000`  
- `0 ≤ n ≤ 1000`  
- `1 ≤ m + n ≤ 2000`  
- `-10^6 ≤ nums1[i], nums2[i] ≤ 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把两段已经排好序的数组 **全部合并**，得到一个完整的有序数组，然后按照中位数的定义直接取出答案。

- **数据结构**：我们只需要一个普通的 Python 列表（list）来存放合并后的结果。可以把它想象成把两本已经排好顺序的书的页码全部贴在一起，重新排好顺序后再找中间的页码。
- **正确性**：因为原始的 `nums1`、`nums2` 都是升序的，使用 **归并（merge）** 的方式一次遍历两个数组即可得到整体的升序序列。中位数的定义只和整体有序序列的第 `k`（或 `k`、`k+1`）个元素有关，所以只要得到完整序列，就一定能得到正确的中位数。
- **时间/空间复杂度**：  
  - 归并过程需要遍历 `m + n` 个元素，所以时间是 **O(m + n)**。  
  - 合并后产生的新数组也会占用 `m + n` 个位置，所以空间是 **O(m + n)**。  
  - 大白话解释：如果两个数组各有 1000 个数，合并后会有 2000 个数，遍历 2000 次、存 2000 个数，这就是线性时间和线性空间。

#### 代码（Python）

```python
def findMedianSortedArrays(nums1, nums2):
    m, n = len(nums1), len(nums2)
    merged = []                     # 用来存放合并后的有序序列
    i = j = 0                       # 两个指针分别指向 nums1、nums2 的当前位置

    # 归并过程：每次把较小的元素放进 merged
    while i < m and j < n:
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1

    # 把剩余的元素直接接到后面（因为已经是有序的）
    while i < m:
        merged.append(nums1[i])
        i += 1
    while j < n:
        merged.append(nums2[j])
        j += 1

    # 计算中位数
    total = m + n
    if total % 2 == 1:                      # 总长度为奇数，只需要中间那个数
        return float(merged[total // 2])
    else:                                   # 为偶数，需要取中间两个数的平均值
        left = merged[total // 2 - 1]
        right = merged[total // 2]
        return (left + right) / 2.0
```

#### 复杂度

- **时间复杂度**：`O(m + n)` —— 需要一次遍历两个数组的全部元素，和数组长度成正比。  
- **空间复杂度**：`O(m + n)` —— 需要额外的数组来存放合并后的结果，大小等于两个输入数组之和。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“合并整个数组”** 这一步——我们其实并不需要把所有元素都显式地放在一起，只要找到中位数所在的位置即可。  
关键观察：

1. **中位数的本质**  
   - 对于长度为 `L = m + n` 的有序序列，若 `L` 为奇数，则第 `k = L // 2`（0‑based）个元素即为中位数。  
   - 若 `L` 为偶数，则第 `k = L // 2 - 1` 和 `k+1` 两个元素的平均值为中位数。  

2. **把问题转化为 “找第 k 小的数”**  
   找第 `k` 小的数可以用 **二分搜索**（binary search）在两个有序数组上交叉进行。每次比较两个数组中第 `k//2` 个元素，舍掉不可能包含第 `k` 小元素的那一半。这样每一步都把搜索范围至少削减一半，时间就会是 `O(log (m+n))`。

3. **实现细节**  
   - 设 `A`、`B` 为较短的数组和较长的数组（先把较短的放在 `A`），这样在取 `k//2` 时不会越界。  
   - 递归（或循环）结束的几种情况：  
     - `A` 已经空了，直接返回 `B[k-1]`。  
     - `k == 1`，直接返回 `min(A[0], B[0])`。  
   - 每一步比较 `A[i-1]` 与 `B[j-1]`（`i = min(len(A), k//2)`，`j = k - i`），把较小的一段丢掉。

4. **如何得到中位数**  
   - 若总长度为奇数，只需要调用一次 “第 k 小” 的函数。  
   - 若为偶数，分别求第 `k` 小和第 `k+1` 小，两者求平均。

> **类比**：想象两条排好队的学生（分别代表两个数组），我们要找第 `k` 位的学生。每次我们让两队各自选出第 `k/2` 位的学生，比大小后，站在前面的那一队的前 `k/2` 人肯定不可能是第 `k` 位，于是可以让他们直接退出队列，剩下的继续竞争。这样每轮都把人数减半，最后自然找到第 `k` 位。

#### 代码（Python）

```python
def findMedianSortedArrays(nums1, nums2):
    # 为了统一处理，保证 nums1 是较短的数组
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    def get_kth(A, B, k):
        """
        返回两个有序数组 A、B 合并后第 k 小的元素（k 从 1 开始计数）。
        """
        len_a, len_b = len(A), len(B)

        # 基础情形
        if len_a == 0:                # A 为空，直接返回 B 中第 k 小
            return B[k - 1]
        if k == 1:                    # 要找最小的，直接比较首元素
            return min(A[0], B[0])

        # 取出各自的第 i、j 元素进行比较
        i = min(len_a, k // 2)        # 防止越界，i 至少为 1
        j = k - i                     # 保证 i + j = k

        if A[i - 1] <= B[j - 1]:
            # A 前 i 个元素一定不可能是第 k 小，去掉它们
            return get_kth(A[i:], B, k - i)
        else:
            # B 前 j 个元素一定不可能是第 k 小，去掉它们
            return get_kth(A, B[j:], k - j)

    total_len = len(nums1) + len(nums2)
    if total_len % 2 == 1:          # 奇数长度
        median = get_kth(nums1, nums2, total_len // 2 + 1)
        return float(median)
    else:                           # 偶数长度，需要两个中间数的平均值
        left = get_kth(nums1, nums2, total_len // 2)
        right = get_kth(nums1, nums2, total_len // 2 + 1)
        return (left + right) / 2.0
```

> **代码要点解释**  
- 第 4 行把较短的数组放在 `nums1`，这样递归时 `A[i:]` 不会一次切掉太多导致空列表频繁出现。  
- `get_kth` 使用 **递归** 实现，每次递归都把搜索范围至少削减 `k//2`，所以递归深度为 `O(log (m+n))`。  
- `i = min(len_a, k // 2)` 确保即使数组长度不足 `k//2` 也能安全取值。  
- `k` 是 **从 1 开始** 的计数方式，便于与 “第 k 小” 的定义对应。

#### 复杂度

- **时间复杂度**：`O(log (m + n))`  
  - 每一次递归都把 `k` 减少至少一半，类似二分搜索的过程。即使最坏情况也只会进行 `log₂(m+n)` 次比较。  
  - 与暴力解的 `O(m+n)` 相比，这里只需要几次（比如 20 次）就能定位答案，速度提升巨大。
- **空间复杂度**：`O(log (m + n))`（递归栈）  
  - 递归深度为 `log (m+n)`，每层保存少量局部变量。如果改成循环实现，则可以做到 `O(1)` 的额外空间。

---

## 心得

- **核心技巧**：把 “求中位数” 转化为 “求第 k 小”，利用二分划分在两个有序数组上交叉搜索。  
- **适用的题型**  
  1. “寻找两个有序数组的第 k 小元素”（LeetCode 378）  
  2. “在有序矩阵中第 k 小的数”（LeetCode 378 的变形）  
  3. “分割数组使得左右两边的最大最小差最小”（类似的二分划分思路）  
- **一句话总结解题钥匙**：**把“合并”过程压缩到对数级别，只比较关键位置的元素，快速排除不可能的区间**。

---

## 反思

- **第一反应**：直接把两个数组合并再取中位数，想到归并排序的思路。  
- **最容易踩的坑**  
  - 边界条件：一个数组为空、总长度为奇数/偶数的处理。  
  - `k//2` 可能超过当前数组长度，需要用 `min(len, k//2)` 防止越界。  
  - 递归/循环结束条件写错会导致无限递归或返回错误的元素。  
- **下次遇到同类题**：第一步先思考 **“是否真的需要完整合并？”**，如果答案是否定的，就立刻考虑 **二分划分 / “第 k 小”** 的框架。这样可以快速锁定对数时间解法的方向。