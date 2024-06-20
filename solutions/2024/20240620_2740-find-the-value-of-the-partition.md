# #2740. 划分的值 / Find the Value of the Partition

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-the-value-of-the-partition/)

---

## 题目（英文原版）

**Description**

You are given a positive integer array nums.
Partition nums into two arrays, nums1 and nums2, such that:
The value of the partition is |max(nums1) - min(nums2)|.
Here, max(nums1) denotes the maximum element of the array nums1, and min(nums2) denotes the minimum element of the array nums2.
Return the integer denoting the value of such partition.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,4]
Output: 1
Explanation: We can partition the array nums into nums1 = [1,2] and nums2 = [3,4].
- The maximum element of the array nums1 is equal to 2.
- The minimum element of the array nums2 is equal to 3.
The value of the partition is |2 - 3| = 1. 
It can be proven that 1 is the minimum value out of all partitions.
```

**Example 2:**

```
Input: nums = [100,1,10]
Output: 9
Explanation: We can partition the array nums into nums1 = [10] and nums2 = [100,1].
- The maximum element of the array nums1 is equal to 10.
- The minimum element of the array nums2 is equal to 1.
The value of the partition is |10 - 1| = 9.
It can be proven that 9 is the minimum value out of all partitions.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个正整数数组 `nums`。  
将 `nums` 划分为两个数组 `nums1` 和 `nums2`，使得：

- 划分的值为 \|max(nums1) - min(nums2)\|，其中 `max(nums1)` 表示数组 `nums1` 的最大元素，`min(nums2)` 表示数组 `nums2` 的最小元素。

返回能够得到的划分值。

**示例 1**  
```
Input: nums = [1,3,2,4]
Output: 1
Explanation: 我们可以将数组 nums 划分为 nums1 = [1,2] 和 nums2 = [3,4]。
- nums1 的最大元素为 2。
- nums2 的最小元素为 3。
划分的值为 |2 - 3| = 1。  
可以证明，在所有划分方案中 1 是最小值。
```

**示例 2**  
```
Input: nums = [100,1,10]
Output: 9
Explanation: 我们可以将数组 nums 划分为 nums1 = [10] 和 nums2 = [100,1]。
- nums1 的最大元素为 10。
- nums2 的最小元素为 1。
划分的值为 |10 - 1| = 9。  
可以证明，在所有划分方案中 9 是最小值。
```

**约束条件**  
- 2 ≤ `nums.length` ≤ 10⁵  
- 1 ≤ `nums[i]` ≤ 10⁹

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的划分**，然后计算每种划分的 `|max(nums1) - min(nums2)|`，取最小值。

- **枚举划分**：把原数组 `nums` 的每一个元素都决定是放进 `nums1` 还是 `nums2`。这相当于对 `n` 个元素做 2 种选择，组合数是 `2^n`，和把每个元素看成 “左边” 或 “右边” 的二进制位一样。  
- **计算值**：对每一种划分，遍历一次数组即可得到 `max(nums1)`（左边最大的）和 `min(nums2)`（右边最小的），再求绝对差。  
- **取最小**：把所有划分得到的差值放进一个变量 `ans`，不断取最小。

> **类比**：把数组想象成一堆彩色球，暴力解就是把每个球贴上 “A” 或 “B” 的标签，尝试所有可能的贴法，然后找出使两堆之间颜色差最小的那一种。

这个方法一定能得到正确答案，因为它遍历了**全部**合法划分。只要我们没有漏掉任何一种情况，答案必然在枚举的结果里。

#### 代码（Python）

```python
from typing import List

def min_partition_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best = float('inf')                     # 用一个很大的数先保存答案

    # 用二进制位表示划分：第 i 位为 0 表示 nums[i] 放进 nums1，1 表示放进 nums2
    for mask in range(1, (1 << n) - 1):     # 需要保证两边都非空，故排除全 0 和全 1
        max1 = -float('inf')                # nums1 的最大值
        min2 = float('inf')                 # nums2 的最小值

        for i in range(n):
            if mask >> i & 1:               # 第 i 位是 1 → 放进 nums2
                min2 = min(min2, nums[i])
            else:                           # 第 i 位是 0 → 放进 nums1
                max1 = max(max1, nums[i])

        # 计算当前划分的值
        cur = abs(max1 - min2)
        best = min(best, cur)                # 保留最小的那个

    return best
```

> **关键注释**  
> - `mask` 从 `1` 到 `2^n-2`，确保 `nums1`、`nums2` 都至少有一个元素。  
> - `max1`、`min2` 分别在遍历时维护，省去再遍历一次数组的开销。  

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  - “`2^n`” 是所有划分的数量，`n` 是每次遍历数组求 `max`/`min` 所需的时间。  
  - 对于 `n=20` 已经是几千万次操作，显然在实际数据（`n ≤ 10^5`）下不可接受。

- **空间复杂度**：`O(1)`（不计输入数组）  
  - 只使用了常数个额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定答案的只有两个数**：  
- `max(nums1)`（左边最大的）  
- `min(nums2)`（右边最小的）

如果我们把数组 **排序**，所有元素都会按从小到大的顺序排列：

```
sorted_nums = [a1, a2, a3, …, an]   （a1 ≤ a2 ≤ … ≤ an）
```

要让 `|max(nums1) - min(nums2)|` 最小，显然应该让这两个数**尽量靠近**。  
在排好序的序列里，两个相邻的数 `ai`、`ai+1` 的差值是 **所有可能的相邻差** 中最小的候选答案。原因如下：

1. **划分必须是把若干元素放左边，若干元素放右边**。  
   假设我们把排好序的数组切成两段：左段 `[a1 … ak]` 放进 `nums1`，右段 `[ak+1 … an]` 放进 `nums2`。  
   那么 `max(nums1) = ak`，`min(nums2) = ak+1`，两者恰好是相邻的两个数。

2. **如果划分不是连续的两段**（即左边、右边的元素交叉），则左边一定会取到比右边更大的某个数，或者右边会取到比左边更小的某个数，导致差值不可能比某个相邻差更小。  
   换句话说，**最优划分一定是一次切割**，而不是把元素随意混在一起。

所以，只要把数组排序，然后遍历一次，找出 **相邻两数的最小差**，就是答案。

> **类比**：把一排排好序的书放在书架上，要把书分成两堆，使左堆最高的书和右堆最矮的书的高度差最小，只需要在书架的某个“缝隙”处断开，差值就是断开处两本书高度的差。

#### 代码（Python）

```python
from typing import List

def min_partition(nums: List[int]) -> int:
    # 1. 先把数组从小到大排好序
    nums.sort()                               # 时间 O(n log n)

    # 2. 在相邻元素之间找最小差值
    ans = float('inf')
    for i in range(len(nums) - 1):
        diff = nums[i + 1] - nums[i]          # 两个相邻数的差（已是非负数）
        if diff < ans:
            ans = diff

    return ans
```

> **关键注释**  
> - `sort()` 相当于把乱七八糟的水果装进盒子后，按照大小顺序排成一条直线。  
> - `diff` 永远是非负的，因为数组已经从小到大排好序了。  

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序是最耗时的步骤，使用快速排序/归并排序等 `n log n` 级别的算法。遍历一次找最小差只需要 `O(n)`。  
  - 与暴力解的 `O(2^n * n)` 相比，下降到了几乎线性的规模，能轻松处理 `10^5` 规模的数据。

- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（取决于 Python `sort` 的实现）  
  - 这里我们在原数组上直接排序，额外空间几乎为常数。

---

## 心得

- **核心技巧**：先把数组排序，再利用相邻元素的差值求最小值。  
- **适用场景**：  
  1. “把数组分成两段，使左段最大与右段最小的差最小” 这类划分问题。  
  2. “在一组数中找最接近的两个数”——如 LeetCode *Minimum Absolute Difference in an Array*。  
  3. “把点分成两侧，使两侧最近点的距离最小”——几何上的最近点划分。  
- **一句话总结**：**排序 + 看相邻差**，往往能把“全局最优”转化为“局部最优”。

---

## 反思

- **第一反应**：看到“max(nums1) / min(nums2)”，我本能地想到**枚举**所有划分，直接求值。  
- **最容易踩的坑**：  
  - 忘记保证 `nums1`、`nums2` 都非空（题目要求划分成两组）。  
  - 误以为需要考虑“交叉划分”，其实最优划分一定是一次切割。  
  - 直接在未排序数组上计算差值，导致错误的答案。  
- **下次类似题的第一步**：**先思考是否可以把数据排序**，因为很多“最大‑最小”类的最小化问题在有序序列中会变得非常直观。只要能把问题转化为“在有序序列中找最小相邻差”，大多数情况下就能得到线性或 `n log n` 的最优解。