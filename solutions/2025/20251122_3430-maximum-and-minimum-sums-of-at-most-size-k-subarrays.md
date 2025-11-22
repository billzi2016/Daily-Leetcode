# #3430. 至多 K 长度子数组的最大值与最小值之和 / Maximum and Minimum Sums of at Most Size K Subarrays

> 难度：困难 · 标签：Array、Math、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/maximum-and-minimum-sums-of-at-most-size-k-subarrays/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and a positive integer k. Return the sum of the maximum and minimum elements of all subarrays with at most k elements.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], k = 2
Output: 20
Explanation:
The subarrays of nums with at most 2 elements are:
The output would be 20.
```

**Example 2:**

```
Input: nums = [1,-3,1], k = 2
Output: -6
Explanation:
The subarrays of nums with at most 2 elements are:
The output would be -6.
```

**Constraints**

- 1 <= nums.length <= 80000
- 1 <= k <= nums.length
- -106 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个正整数 `k`。返回所有长度至多为 `k` 的子数组（subarray）中，最大元素与最小元素之和的总和。

### 示例 1
**输入**: `nums = [1,2,3]`, `k = 2`  
**输出**: `20`  
**解释**:  
长度至多为 2 的子数组（subarray）为:
- `[1]` → 最大值 1，最小值 1，和为 2  
- `[2]` → 最大值 2，最小值 2，和为 4  
- `[3]` → 最大值 3，最小值 3，和为 6  
- `[1,2]` → 最大值 2，最小值 1，和为 3  
- `[2,3]` → 最大值 3，最小值 2，和为 5  

所有这些和相加得到 `2 + 4 + 6 + 3 + 5 = 20`。

### 示例 2
**输入**: `nums = [1,-3,1]`, `k = 2`  
**输出**: `-6`  
**解释**:  
长度至多为 2 的子数组（subarray）为:
- `[1]` → 最大值 1，最小值 1，和为 2  
- `[-3]` → 最大值 -3，最小值 -3，和为 -6  
- `[1]` → 最大值 1，最小值 1，和为 2  
- `[1,-3]` → 最大值 1，最小值 -3，和为 -2  
- `[-3,1]` → 最大值 1，最小值 -3，和为 -2  

所有这些和相加得到 `2 + (-6) + 2 + (-2) + (-2) = -6`。

### 约束条件
- `1 <= nums.length <= 80000`
- `1 <= k <= nums.length`
- `-10^6 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有合法子数组**，把每个子数组的最大值和最小值求出来再相加。  

- **枚举子数组**：用两层循环，外层固定左端点 `l`，内层把右端点 `r` 从 `l` 向右移动，只要子数组长度 `r‑l+1 ≤ k` 就停下来。  
- **求最大/最小**：遍历子数组里的每个元素，维护当前的最大值 `mx` 和最小值 `mn`。  
- **累加答案**：把 `mx + mn` 加到全局答案中。

> **类比**：把数组想象成一排排货架，暴力解就像让小明从左到右一个货架一个货架地检查，每检查完一段货架就把这段货架里最高的商品价钱和最低的商品价钱相加。显然这会非常慢，因为每次检查都要重新遍历一遍。

**为什么正确**  
只要把**所有**长度不超过 `k` 的子数组都遍历一遍，并且对每个子数组正确求出最大值和最小值，就一定能得到题目要求的和。  

**复杂度分析**  

- 外层循环 `n` 次，内层最多也会遍历 `k` 次（因为子数组长度受 `k` 限制），每次遍历子数组内部再用 `O(length)` 去找最大最小。最坏情况下长度接近 `k`，于是时间复杂度约为  

  \[
  O\bigl(n \times k \times k\bigr) = O(nk^2)
  \]

  当 `k` 接近 `n`（题目最大 8 万）时，这相当于 `O(n^3)`，根本跑不完。  

- 只用了常数级的额外空间，空间复杂度是 `O(1)`。

> **大白话**：`O(nk^2)` 就像说如果有 10 000 个货架，每次检查要检查 10 000 × 10 000 = 1 亿次，显然不可能在几秒钟内完成。

#### 代码（Python）

```python
def brute(nums, k):
    """暴力解：枚举所有长度 ≤ k 的子数组，累加 max+min"""
    n = len(nums)
    ans = 0
    for left in range(n):                     # 固定左端点
        cur_max = cur_min = nums[left]        # 初始化子数组的 max/min
        for right in range(left, min(n, left + k)):   # 右端点最多向右移动 k-1 步
            # 更新当前子数组的最大值和最小值
            cur_max = max(cur_max, nums[right])
            cur_min = min(cur_min, nums[right])
            ans += cur_max + cur_min          # 累加该子数组的贡献
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * k^2)`（在最坏情况下几乎是 `O(n³)`）  
  *含义*：如果数组长度是 `n`，每次都要检查 `k` 长度的子数组，而每个子数组内部又要再遍历一次。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历子数组**：同一个元素会在很多子数组里被反复比较，导致时间指数级增长。  
我们需要把**每个元素的贡献**直接算出来，而不是在每个子数组里去找它。

**核心想法：**  
- 对于 **最大值**，把每个元素看成“这段区间里最大的那个人”。  
- 用 **单调栈**（Monotonic Stack）找到它左边最近的更大的元素 `prev_greater`，以及右边最近的 **不小于** 它的元素 `next_greater`。  
- 那么在 `prev_greater+1 … next_greater-1` 这段区间里，**只要子数组的左端点在 `prev_greater+1` 右侧，右端点在 `next_greater-1` 左侧**，这个元素就是子数组的最大值。  
- 类似地，用单调栈（这次是递增的）可以得到每个元素作为 **最小值** 的支配区间。

得到支配区间后，问题就变成**计数**：  
> 在长度不超过 `k` 的子数组中，有多少个子数组的左端点与右端点分别落在这两个区间，使得该元素是最大（或最小）？

设  

- `L = i - prev` 为左侧可以选择的长度（左端点可以在 `prev+1 … i` 共 `L` 种）  
- `R = next - i` 为右侧可以选择的长度（右端点可以在 `i … next-1` 共 `R` 种）  

若不限制长度，满足条件的子数组数就是 `L * R`（左侧任选一种，右侧任选一种）。  

**加入长度限制 `≤ k`**：  
子数组长度 = `left_len + right_len - 1`（左端点到 `i` 的距离 + 右端点到 `i` 的距离 - 1，`i` 本身算了一次）。  
我们需要统计满足  

```
left_len ∈ [1, L]
right_len ∈ [1, R]
left_len + right_len ≤ k + 1        (记 S = k + 1)
```

的整数对 `(left_len, right_len)` 的个数。  
这可以用数学公式在 **O(1)** 时间算出：

1. 只考虑 `a = left_len`，`b = right_len`。  
2. 对每个合法的 `a`，合法的 `b` 上限是 `min(R, S - a)`（因为 `b ≤ R` 且 `a + b ≤ S`）。  
3. 把求和拆成两段：  
   - 当 `S - a > R` 时，`b` 的上限是 `R`（不受长度限制的影响）。  
   - 当 `S - a ≤ R` 时，`b` 的上限是 `S - a`（受长度限制的影响）。

设  

```
a_max = min(L, S - 1)                # a 不能大于 S-1，否则 S-a ≤ 0
a0    = max(1, S - R)                # 第一个会受到长度限制的 a
```

- 如果 `a0 > a_max`，说明所有 `a` 都不受长度限制，计数 = `a_max * R`。  
- 否则：

```
cnt = (a0 - 1) * R                                   # 前 a0-1 个 a 完全不受限制
n   = a_max - a0 + 1                                 # 受限制的 a 的个数
cnt += n * S - (a0 + a_max) * n // 2                 # 等差数列求和
```

得到的 `cnt` 正是 **该元素在所有合法子数组中作为最大（或最小）出现的次数**。  
最后把 `cnt * value` 加到答案里，分别求 **最大值贡献** 与 **最小值贡献**，相加即得最终答案。

**为什么单调栈能在 O(n) 求出 `prev` 与 `next`**  
- 单调递减栈（存放 **比当前元素大的** 索引）遍历一次数组，弹出比当前小的元素，当前元素的 **右侧第一个不小于它的元素** 就是栈顶。  
- 同理，遍历一次得到 **左侧最近更大的** 元素。  
- 对最小值只需要把“不大于”改成“不小于”，把递减栈改成递增栈即可。

**整体复杂度**：  
- 两次单调栈遍历 → `O(n)`。  
- 对每个元素做一次常数时间的计数 → `O(n)`。  
- 所以总时间是 `O(n)`，空间 `O(n)`（保存 `prev`、`next` 数组）。

> **类比**：把数组看成一排排小朋友，单调栈帮我们快速找出每个小朋友左边最近比他高（或矮）的小朋友是谁。知道左右最近的“更高的”小朋友后，就能确定在什么范围里，这个小朋友是最高的。然后用数学公式直接算出在这些范围里、长度不超过 `k` 的子数组有多少个，而不必真的去枚举每一个子数组。

#### 代码（Python）

```python
from typing import List

def limited_pair_count(L: int, R: int, k: int) -> int:
    """
    在左侧可选 L 种、右侧可选 R 种的情况下，
    统计满足子数组长度 ≤ k 的 (left_len, right_len) 对数。
    """
    S = k + 1                     # left_len + right_len ≤ S
    a_max = min(L, S - 1)         # left_len 不能大于 S-1
    if a_max <= 0:
        return 0

    a0 = max(1, S - R)            # 第一个会受到长度限制的 left_len

    if a0 > a_max:                # 所有 left_len 都不受限制
        return a_max * R

    # 前 (a0-1) 个 left_len 完全不受限制
    cnt = (a0 - 1) * R

    n = a_max - a0 + 1            # 受限制的 left_len 个数
    # 等差数列求和： Σ_{a=a0}^{a_max} (S - a)
    cnt += n * S - (a0 + a_max) * n // 2
    return cnt


def max_min_sum(nums: List[int], k: int) -> int:
    n = len(nums)

    # ---------- 求每个元素作为最大值的支配区间 ----------
    # prev_greater: 左侧最近严格更大的元素下标，若不存在为 -1
    prev_greater = [-1] * n
    stack = []                     # 单调递减栈，保存下标
    for i, v in enumerate(nums):
        while stack and nums[stack[-1]] <= v:   # 弹出不大于 v 的
            stack.pop()
        prev_greater[i] = stack[-1] if stack else -1
        stack.append(i)

    # next_greater: 右侧最近不小于自己的元素下标，若不存在为 n
    next_greater = [n] * n
    stack.clear()
    for i in range(n - 1, -1, -1):
        v = nums[i]
        while stack and nums[stack[-1]] < v:    # 弹出严格小于 v 的
            stack.pop()
        next_greater[i] = stack[-1] if stack else n
        stack.append(i)

    # ---------- 求每个元素作为最小值的支配区间 ----------
    # prev_less: 左侧最近严格更小的元素下标，若不存在为 -1
    prev_less = [-1] * n
    stack.clear()
    for i, v in enumerate(nums):
        while stack and nums[stack[-1]] >= v:   # 弹出不小于 v 的
            stack.pop()
        prev_less[i] = stack[-1] if stack else -1
        stack.append(i)

    # next_less: 右侧最近不大于自己的元素下标，若不存在为 n
    next_less = [n] * n
    stack.clear()
    for i in range(n - 1, -1, -1):
        v = nums[i]
        while stack and nums[stack[-1]] > v:    # 弹出严格大于 v 的
            stack.pop()
        next_less[i] = stack[-1] if stack else n
        stack.append(i)

    # ---------- 统计贡献 ----------
    ans = 0

    # 最大值贡献
    for i, v in enumerate(nums):
        L = i - prev_greater[i]      # 左侧可选长度
        R = next_greater[i] - i      # 右侧可选长度
        cnt = limited_pair_count(L, R, k)
        ans += v * cnt

    # 最小值贡献
    for i, v in enumerate(nums):
        L = i - prev_less[i]
        R = next_less[i] - i
        cnt = limited_pair_count(L, R, k)
        ans += v * cnt

    return ans


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    # 示例 1
    print(max_min_sum([1, 2, 3], 2))          # 20
    # 示例 2
    print(max_min_sum([1, -3, 1], 2))         # -6
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 两次遍历求最大值支配区间、两次遍历求最小值支配区间，各是线性。  
  - 对每个元素的计数是常数时间。  
  与暴力解的 `O(nk^2)` 相比，速度提升了几个数量级。

- **空间复杂度**：`O(n)`  
  - 需要四个长度为 `n` 的数组来存放 `prev/next` 信息。  
  - 这在 `n ≤ 80 000` 时完全可以接受。

---

## 心得

- **核心技巧**：**单调栈 + 贡献计数**。  
  单调栈帮助我们在 *一次* 扫描里找出每个元素在数组中作为「最大」或「最小」的支配区间；随后用数学计数把「长度 ≤ k」的限制转化为一个简单的等差求和公式，从而得到每个元素的出现次数。

- **适用的题型**  
  1. 求所有子数组（或子序列）中**最大/最小元素的贡献**（如「子数组的最大值之和」）。  
  2. **区间限制**（长度、宽度、距离等）下的贡献统计问题。  
  3. 需要在 **O(n)** 或 **O(n log n)** 求解的「每个元素是极值的子数组个数」类问题。

- **一句话总结**：  
  *把每个元素视为区间的「冠军」——用单调栈找出它的统治范围，再用组合数学算出在长度 ≤ k 的子数组里它到底能登场多少次。*

---

## 反思

- **第一反应**：直接枚举子数组，写出暴力解来验证思路。  
- **最容易踩的坑**  
  - **左右边界的选取**：在求最大值时左侧使用「严格大于」而右侧使用「不小于」是为了防止相等元素被重复计数。  
  - **长度限制的计数公式**：容易把「左长度 + 右长度 - 1」写错，导致多算或少算子数组。  
  - **整数溢出**：在 C/C++ 中需要 `long long`，但在 Python 中整数是无限精度，仍要注意不出现负数的错误计数。  
- **下次类似题目**：第一步想到 **「单调栈 → 支配区间 → 计数」**，把「找极值」和「长度限制」分两步解决。这样可以把原本指数级的枚举转化为线性时间的贡献求和。