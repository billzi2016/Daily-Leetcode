# #2044. 统计最大按位或子集的数量 / Count Number of Maximum Bitwise-OR Subsets

> 难度：中等 · 标签：Array、Backtracking、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, find the maximum possible bitwise OR of a subset of nums and return the number of different non-empty subsets with the maximum bitwise OR.
An array a is a subset of an array b if a can be obtained from b by deleting some (possibly zero) elements of b. Two subsets are considered different if the indices of the elements chosen are different.
The bitwise OR of an array a is equal to a[0] OR a[1] OR ... OR a[a.length - 1] (0-indexed).

**Examples**

**Example 1:**

```
Input: nums = [3,1]
Output: 2
Explanation: The maximum possible bitwise OR of a subset is 3. There are 2 subsets with a bitwise OR of 3:
- [3]
- [3,1]
```

**Example 2:**

```
Input: nums = [2,2,2]
Output: 7
Explanation: All non-empty subsets of [2,2,2] have a bitwise OR of 2. There are 23 - 1 = 7 total subsets.
```

**Example 3:**

```
Input: nums = [3,2,1,5]
Output: 6
Explanation: The maximum possible bitwise OR of a subset is 7. There are 6 subsets with a bitwise OR of 7:
- [3,5]
- [3,1,5]
- [3,2,5]
- [3,2,1,5]
- [2,5]
- [2,1,5]
```

**Constraints**

- 1 <= nums.length <= 16
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`，求子集的按位或（bitwise OR）能够达到的最大值，并返回拥有该最大按位或的不同非空子集的数量。

- 若数组 `a` 可以通过删除数组 `b` 中的若干（可能为零）元素得到，则称 `a` 是数组 `b` 的子集（subset）。
- 当两个子集选取的元素下标不同，则视为不同的子集。
- 数组 `a` 的按位或（bitwise OR）定义为 `a[0] OR a[1] OR ... OR a[a.length - 1]`（下标从 0 开始）。

### 示例

**示例 1**

```
Input: nums = [3,1]
Output: 2
Explanation: 子集的最大按位或为 3。拥有按位或 3 的子集有 2 个：
- [3]
- [3,1]
```

**示例 2**

```
Input: nums = [2,2,2]
Output: 7
Explanation: 所有非空子集的按位或均为 2。共有 2³ - 1 = 7 个子集。
```

**示例 3**

```
Input: nums = [3,2,1,5]
Output: 6
Explanation: 子集的最大按位或为 7。拥有按位或 7 的子集有 6 个：
- [3,5]
- [3,1,5]
- [3,2,5]
- [3,2,1,5]
- [2,5]
- [2,1,5]
```

### 约束条件

- `1 <= nums.length <= 16`
- `1 <= nums[i] <= 10⁵`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有 **非空子集** 都枚举出来，逐个计算它们的按位或（bitwise OR），记录下最大的 OR 值以及有多少子集能够得到这个最大值。

- **枚举子集**：  
  把数组下标看成 0/1 开关，`1` 表示选这个位置的元素，`0` 表示不选。长度为 `n` 的数组一共有 `2ⁿ` 种开关组合（即子集），除去全 `0` 的情况就是所有非空子集。可以用 `for mask in range(1, 1<<n)` 来遍历每一种组合。  

- **按位或**：  
  把选中的元素依次做 `or` 运算。`or` 就像把几本书的关键字合并到一起，只要有一本书里出现了某个关键字，合并后的结果里就一定有这个关键字。  

- **为什么正确**：  
  我们把 **所有** 可能的子集都算了一遍，最大 OR 必然在其中出现，计数也一定完整。没有遗漏，也没有多算。

#### 代码（Python）

```python
from typing import List

def countMaxOrSubsets(nums: List[int]) -> int:
    n = len(nums)
    max_or = 0           # 当前找到的最大 OR
    cnt = 0              # 能达到 max_or 的子集数量

    # 1 << n 表示 2 的 n 次方，即所有子集的总数
    for mask in range(1, 1 << n):          # 从 1 开始，排除全 0（空子集）
        cur_or = 0                         # 本次子集的 OR
        # 遍历每一位，判断该位是否被选中
        for i in range(n):
            if mask >> i & 1:              # 第 i 位为 1，说明选了 nums[i]
                cur_or |= nums[i]          # 把它的二进制合并进来
        # 更新最大 OR 与计数
        if cur_or > max_or:
            max_or = cur_or
            cnt = 1                         # 重新计数
        elif cur_or == max_or:
            cnt += 1                        # 再多找到了一个

    return cnt
```

#### 复杂度

- **时间复杂度**：`O( n * 2ⁿ )`  
  解释：我们要遍历 `2ⁿ‑1`（≈ `2ⁿ`）个子集，每个子集要检查 `n` 位是否被选中并做一次 `or`，所以总操作次数大约是 `n × 2ⁿ`。  
  当 `n = 16` 时，`2ⁿ = 65536`，`n·2ⁿ ≈ 1,000,000`，在 Python 里完全可以接受。

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  只用了几个整数变量，和 `n` 的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每个子集都要从头遍历所有元素来计算 OR。我们可以把“已经算过的 OR 结果”记下来，后面的元素只需要在这些已有的结果上再做一次 `or`，就能得到新子集的 OR。这样可以把 **重复计算** 大幅削减。

这正好对应 **动态规划（DP）** 的思想：  
- 状态 `dp[or_val]` 表示“已经遍历到当前元素时，得到 `or_val` 的子集有多少个”。  
- 初始时只有空子集，`dp[0] = 1`（这里的空子集只用来帮助转移，最终答案不计入空子集）。  
- 对每个新元素 `x`，我们把它加到 **所有已有的子集** 中去，得到的新 OR 为 `old_or | x`。于是 `dp[new_or]` 要加上 `dp[old_or]`（即把旧子集扩展一次）。  
- 为了防止在同一次循环里使用已经更新的 `dp` 产生重复计数，需要把 **当前循环的快照** 保存下来，或使用 `new_dp` 临时字典。

经过全部元素后，`max_or = OR(nums)`（整个数组的按位或一定是所有子集中最大的），答案就是 `dp[max_or]`（去掉空子集的计数后即可）。

> **为什么 `max_or` 就是整个数组的 OR？**  
> 按位或的性质是“只增不减”。把更多的数合并进去，只会把原来缺失的 1 位补上，永远不会把已有的 1 位变回 0。所以把所有元素都合在一起得到的 OR 是所有子集里最大的。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def countMaxOrSubsets(nums: List[int]) -> int:
    # dp: {当前 OR 值 : 该 OR 对应的子集数量}
    dp = defaultdict(int)
    dp[0] = 1                     # 空子集，帮助后面的转移

    for x in nums:                # 逐个加入数组元素
        # 把当前 dp 的快照复制出来，防止本轮更新影响同一轮的计算
        cur_snapshot = list(dp.items())
        for cur_or, cnt in cur_snapshot:
            new_or = cur_or | x   # 把 x 加入子集后得到的新 OR
            dp[new_or] += cnt     # 这些子集数量要累加到 new_or 上

    # 整体数组的 OR，即所有子集可能的最大值
    max_or = 0
    for v in nums:
        max_or |= v

    # dp[max_or] 包含了所有得到 max_or 的子集数量（包括空子集的贡献）
    # 但空子集的 OR 为 0，不会计入 max_or，所以直接返回即可
    return dp[max_or]
```

#### 复杂度

- **时间复杂度**：`O( n * m )`，其中 `m` 是遍历过程中出现的不同 OR 值的个数。  
  - 每个元素会遍历一次当前的 `dp` 条目，条目数最多等于所有可能的 OR 组合数。  
  - 由于每个数最多有 17 位（`nums[i] ≤ 10⁵ < 2¹⁷`），理论上不同的 OR 值不超过 `2¹⁷`，但实际远小于这个上限，且 `n ≤ 16`，所以运行非常快。  
  - 与暴力解的 `n·2ⁿ` 相比，这里只遍历出现过的状态，通常要快几倍。

- **空间复杂度**：`O(m)`，存储所有出现过的 OR 值及其计数。  
  在最坏情况下 `m` 仍然是 `2ⁿ`（比如每个数都是不同的位），但 `n` 只有 16，最多也就是 65536 条记录，属于可接受范围。

---

## 心得

- **核心技巧**：利用 **动态规划 + 位运算**，把“子集枚举”转化为“状态转移”。  
- **适用的题型**  
  1. “子集的和/异或/按位或”等需要统计不同子集结果的题目（如 **Maximum XOR of Two Numbers in an Array**、**Count Subsets With Sum Equals K**）。  
  2. “把所有可能的位掩码合并”类题目（如 **Subsets with Bitwise AND Equal to K**、**Number of Good Subsets**）。  
- **一句话总结**：**把“枚举子集”压缩成“把已有结果再加一个元素”**，既保留完整信息，又避免重复计算。

---

## 反思

- **第一反应**：看到“子集”和“按位或”，立刻想到 **2ⁿ 枚举**，因为数组长度只有 16，直接暴力也能跑。  
- **最容易踩的坑**  
  - **空子集**：在 DP 里要先把空子集计入 `dp[0]=1`，否则后面的转移会少算一种可能。  
  - **计数溢出**：本题答案不会超过 `2ⁿ-1`，但如果题目要求取模，需要在每次加法后取模。  
  - **位数误解**：`nums[i] ≤ 10⁵`，实际最高位是第 17 位，不能随意假设只有 32 位。  
- **下次第一步**：先判断 **“是否可以直接枚举”**（n 是否很小），若不可行则立刻考虑 **状态压缩 DP** 或 **位运算技巧** 来把枚举的指数下降到可接受范围。