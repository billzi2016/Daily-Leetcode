# #474. 零与一 / Ones and Zeroes

> 难度：中等 · 标签：Array、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/ones-and-zeroes/)

---

## 题目（英文原版）

**Description**

You are given an array of binary strings strs and two integers m and n.
Return the size of the largest subset of strs such that there are at most m 0's and n 1's in the subset.
A set x is a subset of a set y if all elements of x are also elements of y.

**Examples**

**Example 1:**

```
Input: strs = ["10","0001","111001","1","0"], m = 5, n = 3
Output: 4
Explanation: The largest subset with at most 5 0's and 3 1's is {"10", "0001", "1", "0"}, so the answer is 4.
Other valid but smaller subsets include {"0001", "1"} and {"10", "1", "0"}.
{"111001"} is an invalid subset because it contains 4 1's, greater than the maximum of 3.
```

**Example 2:**

```
Input: strs = ["10","0","1"], m = 1, n = 1
Output: 2
Explanation: The largest subset is {"0", "1"}, so the answer is 2.
```

**Constraints**

- 1 <= strs.length <= 600
- 1 <= strs[i].length <= 100
- strs[i] consists only of digits '0' and '1'.
- 1 <= m, n <= 100

---

## 题目（中文翻译）

给定一个二进制字符串（binary strings）数组 `strs`，以及两个整数 `m` 和 `n`。  
返回 `strs` 的最大子集（subset）的大小，使得该子集中至多包含 `m` 个 `0` 和 `n` 个 `1`。  
如果集合 `x` 的所有元素也都是集合 `y` 的元素，则称 `x` 是 `y` 的子集（subset）。

**示例 1**  
**输入**: `strs = ["10","0001","111001","1","0"]`, `m = 5`, `n = 3`  
**输出**: `4`  
**解释**: 最大的满足条件的子集是 `{"10", "0001", "1", "0"}`，因此答案为 `4`。  
其他合法但规模更小的子集包括 `{"0001", "1"}` 和 `{"10", "1", "0"}`。  
`{"111001"}` 不是合法子集，因为它包含 `4` 个 `1`，超过了最大允许的 `3`。

**示例 2**  
**输入**: `strs = ["10","0","1"]`, `m = 1`, `n = 1`  
**输出**: `2`  
**解释**: 最大的子集是 `{"0", "1"}`，因此答案为 `2`。

**约束条件**  
- `1 <= strs.length <= 600`  
- `1 <= strs[i].length <= 100`  
- `strs[i]` 仅由字符 `'0'` 和 `'1'` 组成  
- `1 <= m, n <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**枚举所有可能的子集**，然后统计每个子集里 0 的个数和 1 的个数，挑出满足 “0 不超过 m、1 不超过 n” 的最大子集大小。  

- **数据结构**：  
  - 用 `list` 存放原始字符串数组 `strs`。  
  - 用 `int` 计数 0、1 的个数。  
  - 用 **位掩码（bitmask）** 表示子集的选取情况：如果第 `i` 位是 1，说明把 `strs[i]` 放进子集；如果是 0，则不放。位掩码就像一本**字典**的目录页码，指明我们挑了哪些单词。  

- **为什么正确**：  
  - 枚举了**所有**子集（包括空集），不遗漏任何一种可能。只要子集满足约束条件，就会被计入答案。因此，最大的合法子集一定会在枚举结果里出现。  

- **复杂度分析**：  
  - `strs` 长度记为 `k`（题目上限 600），子集的数量是 `2^k`（每个元素有放或不放两种选择）。  
  - 对每个子集，我们要遍历一次 `k` 个字符串统计 0/1，时间是 `O(k)`。  
  - **总时间**：`O(k * 2^k)`，这在 `k=600` 时几乎不可能跑完（指数级爆炸）。  
  - **空间**：只需要存放原数组和几个计数器，`O(k)`，几乎可以忽略。  

> **大白话**：  
> `O(k * 2^k)` 就好比让 600 个人每人都排队买票，一次只能买一张，所有排队方式加起来的组合数会天文数字，根本不可能在电脑里全部列出来。

#### 代码（Python）  

```python
from typing import List

def max_subset_bruteforce(strs: List[str], m: int, n: int) -> int:
    k = len(strs)
    best = 0                       # 当前找到的最大合法子集大小

    # 预先统计每个字符串里 0、1 的个数，后面直接使用
    cnt = []
    for s in strs:
        zeros = s.count('0')
        ones  = s.count('1')
        cnt.append((zeros, ones))

    # 枚举 0 ~ (2^k - 1) 每一个可能的子集
    for mask in range(1 << k):     # 1 << k == 2**k
        zeros_sum = 0
        ones_sum  = 0
        size = 0

        # 检查第 i 位是否被选中
        for i in range(k):
            if mask & (1 << i):    # 第 i 位是 1 → 选中 strs[i]
                z, o = cnt[i]
                zeros_sum += z
                ones_sum  += o
                size += 1

                # 只要已经超出限制，就可以提前退出本子集的检查
                if zeros_sum > m or ones_sum > n:
                    break

        # 所有字符都检查完且没有超标，更新答案
        if zeros_sum <= m and ones_sum <= n:
            best = max(best, size)

    return best
```

#### 复杂度  

- **时间复杂度**：`O(k * 2^k)`  
  - 解释：对每个子集（`2^k` 种）都要遍历最多 `k` 次字符计数。  
- **空间复杂度**：`O(k)`  
  - 只用了 `cnt` 数组保存每个字符串的 0/1 个数，和若干临时变量。

---

### 2. 最优解  

#### 思路  
暴力解的 **瓶颈** 在于“枚举所有子集”。我们需要 **把问题转化成更小的子问题**，利用已经算好的结果来避免重复计算。  

观察题目：  
- 每个字符串只关心它的 **0 的个数** 与 **1 的个数**。  
- 目标是 **在给定的 0、1 预算（m、n）内**，选出尽可能多的字符串。  

这正好像 **背包问题**（Knapsack）：  
- 每件物品（字符串）有两个“重量”——`zeros` 和 `ones`。  
- 我们的“背包容量”是 `m`（0 的上限）和 `n`（1 的上限）。  
- 每件物品的“价值”是 **1**（选一个字符串就能让答案加 1）。  

背包问题有经典的 **动态规划（DP）** 解法。这里的背包是 **二维** 的，因为有两个容量维度。  

**DP 状态**  
`dp[i][j]` = 在最多使用 `i` 个 0 和 `j` 个 1 时，能够选到的最大字符串数量。  

**状态转移**（从每个字符串出发）  
假设当前字符串需要 `z` 个 0、`o` 个 1。我们可以选择 **不放**（状态不变）或者 **放进去**。如果放进去，容量会相应减少：

```
dp[i][j] = max(dp[i][j], dp[i - z][j - o] + 1)   (前提是 i >= z 且 j >= o)
```

**遍历顺序**  
为了保证每个字符串只被算一次（相当于“0-1 背包”，而不是“完全背包”），**外层循环遍历字符串，内层容量从大到小倒序**。倒序保证本轮更新时不会使用到已经在本轮加入的同一个字符串的结果。

**初始化**  
所有 `dp` 初始为 0，表示什么都不选时的答案。

**答案**  
遍历完所有字符串后，`dp[m][n]` 即为在限制条件下能选的最多字符串数。

#### 代码（Python）  

```python
from typing import List

def findMaxForm(strs: List[str], m: int, n: int) -> int:
    # dp[i][j] 表示在最多 i 个 0、j 个 1 的情况下能选的最大字符串数
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for s in strs:
        zeros = s.count('0')
        ones  = s.count('1')

        # 必须倒序遍历，防止同一个字符串被重复使用（类似 0-1 背包）
        for i in range(m, zeros - 1, -1):          # i 从 m 到 zeros
            for j in range(n, ones - 1, -1):       # j 从 n 到 ones
                # 若把当前字符串放进去，则子问题是剩余 (i-zeros, j-ones)
                # 加 1 表示选了这条字符串
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)

    return dp[m][n]
```

#### 复杂度  

- **时间复杂度**：`O(k * m * n)`  
  - `k = len(strs)`（最多 600），`m, n ≤ 100`。  
  - 每条字符串都遍历一次 `m * n` 的二维表，整体大约是 `600 * 100 * 100 = 6,000,000` 次操作，完全可以在毫秒级完成。  
- **空间复杂度**：`O(m * n)`  
  - 只需要保存一个二维 DP 表，大小为 `(m+1) * (n+1)`，最多 `101 * 101 ≈ 10⁴` 个整数，几乎可以忽略不计。

---

## 心得  

- **核心技巧**：把 “在两个资源限制下选最多物品” 转化为 **二维 0‑1 背包**，使用 **动态规划** 求解。  
- **适用的题型**：  
  1. LeetCode 416 – **Partition Equal Subset Sum**（一维背包）  
  2. LeetCode 474 – **Ones and Zeroes**（本题，二维背包）  
  3. LeetCode 1049 – **Last Stone Weight II**（一维背包）  
- **一句话总结**：  
  > “当每个选项有多个消耗维度时，使用多维背包 DP；把预算当作状态维度，价值设为计数即可。”

---

## 反思  

- **第一反应**：看到 “最多 m 个 0、n 个 1” 就想到背包，因为这本质上是“资源受限的选取”。  
- **最容易踩的坑**：  
  - **倒序遍历**：如果正序遍历会导致同一个字符串被多次计入，答案会比实际大。  
  - **边界条件**：`i - zeros`、`j - ones` 必须 ≥ 0，循环的起点要写成 `range(m, zeros-1, -1)`（而不是 `range(m, -1, -1)`），防止索引负数。  
  - **计数 0/1 的方式**：使用 `s.count('0')`、`s.count('1')`，避免自己写循环出错。  
- **下次类似题的第一步**：  
  - 把每个元素的“消耗”抽象成数字（或向量），确认是否可以建模为 **背包**；随后决定是“一维背包”还是“多维背包”，再写 DP 状态转移。