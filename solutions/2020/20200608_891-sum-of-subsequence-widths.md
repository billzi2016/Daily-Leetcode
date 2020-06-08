# #891. **子序列宽度之和** / Sum of Subsequence Widths

> 难度：困难 · 标签：Array、Math、Sorting · [LeetCode 链接](https://leetcode.com/problems/sum-of-subsequence-widths/)

---

## 题目（英文原版）

**Description**

The width of a sequence is the difference between the maximum and minimum elements in the sequence.
Given an array of integers nums, return the sum of the widths of all the non-empty subsequences of nums. Since the answer may be very large, return it modulo 109 + 7.
A subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of the remaining elements. For example, [3,6,2,7] is a subsequence of the array [0,3,1,6,2,2,7].

**Examples**

**Example 1:**

```
Input: nums = [2,1,3]
Output: 6
Explanation: The subsequences are [1], [2], [3], [2,1], [2,3], [1,3], [2,1,3].
The corresponding widths are 0, 0, 0, 1, 1, 2, 2.
The sum of these widths is 6.
```

**Example 2:**

```
Input: nums = [2]
Output: 0
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

序列的宽度（width）定义为该序列中最大元素与最小元素的差值。  
给定一个整数数组 `nums`，返回 `nums` 所有非空子序列（subsequence）的宽度之和。由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。

子序列是可以通过删除数组中的任意个（包括零个）元素而不改变剩余元素相对顺序得到的序列。例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的一个子序列。

**示例 1**

```
输入: nums = [2,1,3]
输出: 6
解释: 所有子序列为 [1], [2], [3], [2,1], [2,3], [1,3], [2,1,3]。
对应的宽度分别为 0, 0, 0, 1, 1, 2, 2。
这些宽度的和为 6。
```

**示例 2**

```
输入: nums = [2]
输出: 0
解释: 唯一的非空子序列是 [2]，其宽度为 0。
```

**约束条件**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有非空子序列**，对每个子序列求出最大值和最小值的差（即宽度），然后累加。  
- **子序列**：可以把数组想象成一串珠子，挑选出任意若干颗（可以不挑，也可以挑全部），保持原来的顺序，这就是一个子序列。  
- **枚举方式**：用二进制掩码 `mask`（长度为 `n`）来表示是否选第 `i` 个元素，`mask` 从 `1` 到 `2^n‑1`（排除全 0 的空子序列）。  
- **求宽度**：遍历当前掩码对应的元素，维护当前子序列的最大值 `mx` 和最小值 `mn`，宽度就是 `mx‑mn`。  

这种方法一定能得到正确答案，因为它穷举了题目要求的“所有非空子序列”。  

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def sum_subseq_widths_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    # 用 1 ~ (2^n - 1) 的二进制表示所有非空子序列
    for mask in range(1, 1 << n):
        mn = float('inf')   # 当前子序列的最小值
        mx = -float('inf')  # 当前子序列的最大值
        for i in range(n):
            if mask >> i & 1:          # 第 i 位为 1，说明选了 nums[i]
                val = nums[i]
                if val < mn:
                    mn = val
                if val > mx:
                    mx = val
        ans = (ans + (mx - mn)) % MOD   # 累加宽度，取模防止溢出
    return ans
```

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  - 解释：有 `2^n` 种子序列（因为每个位置可以选或不选），对每种子序列我们要遍历 `n` 次来找最大最小值。对 n=20 以上就会非常慢，根本跑不完。  
- **空间复杂度**：`O(1)`（只用了常数个额外变量）

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**“枚举所有子序列”**，这一步导致指数级的时间。  
观察宽度的定义 `max - min`，如果我们把数组**先排个序**，会出现一个关键现象：

> 在排好序的数组 `a[0] ≤ a[1] ≤ … ≤ a[n‑1]` 中，任意子序列的 **最大值** 必然是它选中的 **最右边的元素**，**最小值** 必然是它选中的 **最左边的元素**。

换句话说，子序列的宽度只和这两个端点有关，中间的其他元素到底选不选并不影响宽度。  

因此我们可以把问题转化为：

> 对于每个位置 `i`，它作为 **最大值** 时，会和左边的某些元素一起构成子序列；同理，它作为 **最小值** 时，也会和右边的某些元素一起构成子序列。统计所有“最大‑最小”配对的贡献即可。

具体步骤：

1. **排序**：把 `nums` 从小到大排好序，记为 `a`。  
2. **组合计数**：  
   - 设 `a[i]` 为当前元素（排好序后第 `i` 个），它**可以作为最大值**的子序列数目是 `2^i`（因为左边的 `i` 个元素每个都可以自由选择是否加入，右边的元素必须不加入，否则会出现更大的最大值）。  
   - 同理，`a[i]` **可以作为最小值**的子序列数目是 `2^{n‑1‑i}`（右边的 `n‑1‑i` 个元素每个自由选择，左边不加入）。  
3. **贡献相减**：每个 `a[i]` 作为最大值时会 **正向** 加到宽度，总贡献 `a[i] * 2^i`；作为最小值时会 **负向** 减去宽度，总贡献 `a[i] * 2^{n‑1‑i}`。所以最终答案是  

\[
\sum_{i=0}^{n-1} a[i] \times (2^i - 2^{n-1-i}) \pmod{10^9+7}
\]

4. **预计算幂**：`2^k (mod MOD)` 可以用一次遍历的方式递推得到，避免每次 `pow` 带来的额外开销。  

> **类比**：把 `2^i` 想象成“左边有 i 把钥匙，每把钥匙可以打开或不打开一道门”，所以一共有 `2^i` 种可能的开门方式——这正对应了左边元素的“选或不选”。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def sum_subseq_widths(nums: List[int]) -> int:
    n = len(nums)
    nums.sort()                     # 第一步：排序

    # 预计算 2^0, 2^1, ..., 2^{n-1}（模 MOD）
    pow2 = [1] * n
    for i in range(1, n):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = 0
    for i, x in enumerate(nums):
        # x 作为最大值的贡献是 x * 2^i
        # x 作为最小值的贡献是 x * 2^{n-1-i}
        contrib = (pow2[i] - pow2[n - 1 - i]) % MOD   # 先算系数，防止负数
        ans = (ans + x * contrib) % MOD              # 加上该元素的总贡献
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，其余遍历和幂次预计算都是线性 `O(n)`。相较于暴力的指数级，这已经是可以接受的规模（`n ≤ 10^5`）。  
- **空间复杂度**：`O(n)`（存放 `pow2` 数组）。如果想进一步节约空间，也可以只保留一个变量滚动计算，但 `O(n)` 已经足够小。

---

## 心得

- **核心技巧**：**排序 + 组合计数**（利用子序列宽度只与端点有关的特性）。  
- **适用的题型**  
  1. “子序列/子集的和/差/最大最小” 类问题（如 *Sum of Subarray Minimums*）。  
  2. 需要统计“每个元素作为最大/最小出现次数”的问题（如 *Number of Subarrays With Bounded Maximum*）。  
  3. 任何可以把“顺序无关”转化为“端点决定” 的组合计数题。  
- **一句话总结**：**把数组排好序后，利用 2 的幂次快速计数每个元素作为最大或最小的子序列数目，累加贡献即可**。

---

## 反思

- **第一反应**：直接想到遍历所有子序列求宽度，写出暴力实现。  
- **最容易踩的坑**  
  - 忘记对结果取模，导致整数溢出。  
  - 在计算 `(2^i - 2^{n-1-i})` 时出现负数，必须在模运算下先加 `MOD` 再取余。  
  - 排序后忘记使用 `int` 类型的幂次，导致时间超限。  
- **下次类似题的第一步**：先**思考是否可以把“子序列的某种属性”拆解为“左/右端点的组合计数”**，如果能，立刻考虑排序 + 幂次计数的套路。