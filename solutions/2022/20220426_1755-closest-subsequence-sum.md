# #1755. 最接近的子序列和 / Closest Subsequence Sum

> 难度：困难 · 标签：Array、Two Pointers、Dynamic Programming、Bit Manipulation、Sorting、Bitmask · [LeetCode 链接](https://leetcode.com/problems/closest-subsequence-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer goal.
You want to choose a subsequence of nums such that the sum of its elements is the closest possible to goal. That is, if the sum of the subsequence's elements is sum, then you want to minimize the absolute difference abs(sum - goal).
Return the minimum possible value of abs(sum - goal).
Note that a subsequence of an array is an array formed by removing some elements (possibly all or none) of the original array.

**Examples**

**Example 1:**

```
Input: nums = [5,-7,3,5], goal = 6
Output: 0
Explanation: Choose the whole array as a subsequence, with a sum of 6.
This is equal to the goal, so the absolute difference is 0.
```

**Example 2:**

```
Input: nums = [7,-9,15,-2], goal = -5
Output: 1
Explanation: Choose the subsequence [7,-9,-2], with a sum of -4.
The absolute difference is abs(-4 - (-5)) = abs(1) = 1, which is the minimum.
```

**Example 3:**

```
Input: nums = [1,2,3], goal = -7
Output: 7
```

**Constraints**

- 1 <= nums.length <= 40
- -107 <= nums[i] <= 107
- -109 <= goal <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `goal`。  
你需要从 `nums` 中选择一个子序列（subsequence），使得该子序列中所有元素的和 `sum` 与 `goal` 的距离尽可能小。也就是说，要最小化绝对差 `abs(sum - goal)`。  
返回可能的最小 `abs(sum - goal)` 值。  

**子序列** 是指通过删除原数组中的任意若干元素（可以全部删除，也可以一个也不删）得到的数组。

### 示例

#### 示例 1
输入: `nums = [5,-7,3,5]`, `goal = 6`  
输出: `0`  
解释: 选择整个数组作为子序列，和为 `6`。这正好等于 `goal`，所以绝对差为 `0`。

#### 示例 2
输入: `nums = [7,-9,15,-2]`, `goal = -5`  
输出: `1`  
解释: 选择子序列 `[7,-9,-2]`，其和为 `-4`。  
绝对差为 `abs(-4 - (-5)) = abs(1) = 1`，这是可以得到的最小值。

#### 示例 3
输入: `nums = [1,2,3]`, `goal = -7`  
输出: `7`

### 约束条件

- `1 <= nums.length <= 40`
- `-10^7 <= nums[i] <= 10^7`
- `-10^9 <= goal <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的子序列都列举出来，算出它们的和，再找和 `goal` 最接近的那个**。  

- **子序列** = 任意挑选（或不挑选）原数组中的元素，顺序不变。  
- 对于长度为 `n` 的数组，每个元素都有“挑”或“不挑”两种状态，所以一共有 `2ⁿ` 种子序列（包括空序列）。  
- 我们可以把每个子序列看成一个二进制掩码（bitmask），第 `i` 位是 1 表示取第 `i` 个数，0 表示不取。  

> **类比**：把 `bitmask` 想成一本字典的页码，页码上写着“这本书里第几章要读”。遍历所有页码，就等价于遍历所有子序列。

**为什么这个方法一定能得到答案**  
因为我们没有遗漏任何一种取法，遍历完所有 `2ⁿ` 种组合后，肯定能找到使 `|sum-goal|` 最小的那一个。

**时间/空间分析（大白话）**  

- **时间**：每种子序列我们都要把选中的元素相加，最坏情况下要遍历 `n` 个数。于是总共要做 `2ⁿ × n` 次加法，记作 **O( n·2ⁿ )**。  
  - `O` 符号可以理解为“数量级”。比如 `n=20` 时，`2ⁿ≈1,048,576`，乘以 `n` 仍然是几百万次，电脑还能接受；但 `n=40` 时，`2⁴⁰≈1.1 兆`，已经不可行了。  
- **空间**：只需要保存几个整数（当前的和、最小差值），不随 `n` 增长，记作 **O(1)**。

#### 代码（Python）

```python
from typing import List

def minAbsDifference_bruteforce(nums: List[int], goal: int) -> int:
    """
    暴力枚举所有子序列，返回最小的 |sum - goal|
    """
    n = len(nums)
    ans = float('inf')                     # 当前找到的最小差值，初始设为无限大

    # 0 ~ (1<<n)-1 每一个整数的二进制位代表一种取法
    for mask in range(1 << n):             # 1<<n 等价于 2**n
        cur_sum = 0
        for i in range(n):
            if mask >> i & 1:              # 第 i 位是 1 吗？如果是，就把 nums[i] 加进去
                cur_sum += nums[i]
        diff = abs(cur_sum - goal)         # 计算当前子序列与目标的距离
        if diff < ans:                     # 维护最小值
            ans = diff
            if ans == 0:                    # 已经找到 0，无法再更小，直接退出
                return 0
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n·2ⁿ)`  
  - 解释：我们要遍历 `2ⁿ` 种子序列，每种子序列最多检查 `n` 个元素。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，和数组长度无关。  

---

### 2. 最优解  

#### 思路  

**暴力太慢的根源**  
- `2ⁿ` 的增长速度极快。题目里 `n` 最多 40，`2⁴⁰` 已经是 **1 万亿**，根本不可能全部枚举。

**关键优化思路：分而治之（Meet‑in‑the‑Middle）**  
把数组从中间劈成两半，每半最多 20 个元素。  
- 对 **左半部分**，枚举所有子序列，记录每种子序列的和，得到一个数组 `left_sums`（长度 `2^{n/2}`）。  
- 对 **右半部分**，同样枚举得到 `right_sums`。  

现在我们想要找两个子序列（一个来自左，一個来自右）的和最接近 `goal`。  
设左边选了和 `x`，右边选了和 `y`，则总和为 `x + y`。我们希望 `|x + y - goal|` 最小。  

**转化为一次二分查找**  
- 把 `left_sums` **排序**（因为二分查找要求有序）。  
- 遍历每一个 `y`（右半的子序列和），我们希望在 `left_sums` 中找到最接近 `goal - y` 的 `x`。  
  - 这正好是“在已排序的数组里找最接近某个值”的典型二分搜索。  
  - 用 `bisect_left` 找到第一个 `≥ target` 的位置，同时检查它左边的元素，这两个候选就能得到最小差值。  

**为什么只检查这两个位置**  
因为数组是有序的，目标值左边的所有数都更小，右边的所有数都更大，离目标最近的必然是左边的最大数或右边的最小数（即 `bisect` 返回的位置和它前一个位置）。

**复杂度直观解释**  
- 每半最多 20 个数，子序列数量是 `2^{20} ≈ 1,048,576`，可以轻松在内存中保存。  
- 排序 `left_sums` 用 `O(2^{n/2} log 2^{n/2})`，二分搜索对每个 `y` 只要 `O(log 2^{n/2})`。  
- 整体时间大约是 `O(2^{n/2} log 2^{n/2})`，远远快于 `O(2ⁿ)`。  
- 额外空间主要是保存两个子序列和的列表，都是 `O(2^{n/2})`。

#### 代码（Python）

```python
from typing import List
import bisect

def minAbsDifference(nums: List[int], goal: int) -> int:
    """
    Meet-in-the-Middle（分而治之）求最小 |sum - goal|
    """
    n = len(nums)
    mid = n // 2                     # 把数组分成左/右两段
    left = nums[:mid]
    right = nums[mid:]

    # ---------- 1. 枚举左半部分的所有子序列和 ----------
    left_sums = []
    for mask in range(1 << len(left)):          # 2^{len(left)} 种取法
        cur = 0
        for i in range(len(left)):
            if mask >> i & 1:                    # 第 i 位为 1，则取该元素
                cur += left[i]
        left_sums.append(cur)

    left_sums.sort()                             # 为二分查找准备

    # ---------- 2. 枚举右半部分，配合左半进行二分 ----------
    ans = float('inf')
    for mask in range(1 << len(right)):
        cur = 0
        for i in range(len(right)):
            if mask >> i & 1:
                cur += right[i]

        # 目标是让 left_sum + cur 最接近 goal → left_sum 接近 goal - cur
        target = goal - cur
        idx = bisect.bisect_left(left_sums, target)   # 第一个 >= target 的位置

        # 检查 idx（如果在范围内）和 idx-1（如果在范围内）两种可能
        if idx < len(left_sums):
            ans = min(ans, abs(left_sums[idx] + cur - goal))
        if idx > 0:
            ans = min(ans, abs(left_sums[idx - 1] + cur - goal))

        if ans == 0:                     # 已经找到完美匹配，提前结束
            return 0

    return ans
```

#### 复杂度  

- **时间复杂度**：`O( 2^{n/2} * log 2^{n/2} )`  
  - 解释：左半部分产生 `2^{n/2}` 个和并排序（`log` 是排序的额外开销），右半部分遍历同样数量的子序列，对每个子序列在左边做一次二分（`log`），总体仍是指数级但指数只有原来的一半。  
  - 与暴力的 `O(n·2ⁿ)` 相比，指数从 `2⁴⁰` 降到约 `2²⁰`，快了 **千倍以上**，在实际运行中毫秒级完成。  

- **空间复杂度**：`O( 2^{n/2} )`  
  - 需要存储左半部分的所有子序列和（约一百万个整数），约占几 MB，完全可以放进内存。  

---

## 心得  

- **核心技巧**：**Meet-in-the-Middle（分而治之） + 二分查找**。  
- **适用场景**：  
  1. 子集和类问题，数组长度在 30~40 左右，需要比 `2ⁿ` 更快的枚举（如 LeetCode 1725、1593）。  
  2. “找两组数的和最接近目标” 的变形（如两数之和的最近距离）。  
  3. 任何需要在指数级搜索空间中“把规模减半再组合”的问题。  
- **一句话总结**：把大集合拆成两半，各自列出所有可能的“局部和”，再用有序结构快速配对，就是把 `2ⁿ` 的搜索压缩到 `2^{n/2}`。  

---

## 反思  

- **第一反应**：直接想遍历所有子序列，写出暴力解。  
- **最容易踩的坑**：  
  - **边界**：空子序列（和为 0）也必须考虑，否则在全负数或全正数的情况下可能漏掉最优解。  
  - **整数溢出**：Python 的整数不溢出，但在其他语言要注意使用 64 位。  
  - **二分搜索的细节**：`bisect_left` 可能返回 `0` 或 `len`，访问 `left_sums[idx-1]` 前一定要检查 `idx > 0`，防止越界。  
- **下次遇到同类题**：第一步先判断 `n` 是否在 30~40 左右，若是就立刻想到 **“把数组一分为二，分别枚举子集和”**，再准备排序 + 二分配对的步骤。这样可以从一开始就走在最优解的道路上。