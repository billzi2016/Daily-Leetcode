# #629. K 逆序对数组 / K Inverse Pairs Array

> 难度：困难 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/k-inverse-pairs-array/)

---

## 题目（英文原版）

**Description**

For an integer array nums, an inverse pair is a pair of integers [i, j] where 0 <= i < j < nums.length and nums[i] > nums[j].
Given two integers n and k, return the number of different arrays consisting of numbers from 1 to n such that there are exactly k inverse pairs. Since the answer can be huge, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 3, k = 0
Output: 1
Explanation: Only the array [1,2,3] which consists of numbers from 1 to 3 has exactly 0 inverse pairs.
```

**Example 2:**

```
Input: n = 3, k = 1
Output: 2
Explanation: The array [1,3,2] and [2,1,3] have exactly 1 inverse pair.
```

**Constraints**

- 1 <= n <= 1000
- 0 <= k <= 1000

---

## 题目（中文翻译）

对于整数数组 `nums`，逆序对（inverse pair）是满足 `0 ≤ i < j < nums.length` 且 `nums[i] > nums[j]` 的整数对 `[i, j]`。

给定两个整数 `n` 和 `k`，返回由数字 `1` 到 `n` 组成的不同数组的数量，使得数组恰好拥有 `k` 个逆序对（inverse pair）。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

### 示例

#### 示例 1
```
输入: n = 3, k = 0
输出: 1
解释: 唯一满足条件的数组是由 1 到 3 的数字组成的 `[1,2,3]`，它恰好有 0 个逆序对。
```

#### 示例 2
```
输入: n = 3, k = 1
输出: 2
解释: 数组 `[1,3,2]` 和 `[2,1,3]` 各恰好有 1 个逆序对。
```

### 约束条件
- `1 ≤ n ≤ 1000`
- `0 ≤ k ≤ 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 **1 到 n 的所有排列** 都枚举出来，逐个统计它们的逆序对数，如果恰好等于 k 就计数。  

- **数据结构**：  
  - 用 Python 的 `itertools.permutations` 生成全排列，想象它像一本“全排列词典”，每一页（即每个元组）都是一种可能的数组。  
  - 统计逆序对时，用两层循环遍历数组的每一对位置 `(i, j)`（`i < j`），如果 `nums[i] > nums[j]` 就把逆序对计数器加一。  

- **正确性**：  
  - 由于我们把 **所有** 合法数组（即所有排列）都检查了一遍，凡是满足“逆序对数恰好为 k”的数组必然会被计数，反之不满足的不会计数。  

- **时间/空间复杂度**：  
  - **时间**：枚举 `n!`（n 的阶乘）个排列，每个排列再用 `O(n²)` 的双层循环统计逆序对。于是总时间是 `O(n! * n²)`。  
    - 大白话：即使 n 只有 8，`8! = 40320`，再乘以 `8² = 64`，已经有几百万次操作；n=10 时更是天文数字，根本跑不完。  
  - **空间**：只需要存放当前遍历的一个排列和计数器，`O(n)` 的额外空间。  

> 这就是“暴力解”——概念最清晰，却因为 **指数级** 的枚举而不可行。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def k_inverse_pairs_bruteforce(n: int, k: int) -> int:
    """暴力枚举所有排列，统计恰好有 k 个逆序对的个数。"""
    cnt = 0
    # itertools.permutations 会一次生成一个排列，类似“全排列词典”翻页
    for perm in itertools.permutations(range(1, n + 1)):
        inv = 0
        # 双层循环统计逆序对：i < j 且 perm[i] > perm[j]
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]:
                    inv += 1
        if inv == k:
            cnt += 1
    return cnt % MOD
```

#### 复杂度

- **时间复杂度**：`O(n! * n²)`  
  - “阶乘”增长非常快，哪怕 n=10 也已经不现实。  
- **空间复杂度**：`O(n)`  
  - 只存当前排列和计数器。

---

### 2. 最优解

#### 思路  

从暴力解出发，**慢点** 在于我们一次性枚举了所有排列。实际上，**构造排列的过程** 本身可以提供递推关系，从而用动态规划把指数级的搜索压缩到多项式时间。

**核心观察**：  
把 `1…(n-1)` 的一个合法排列（逆序对数为 `k'`）放进来，然后把数字 `n` 插入到这条排列的某个位置。  

- 若把 `n` 放在最左侧（下标 0），它比所有已有的 `n-1` 个数都大，不会产生新的逆序对。  
- 若把 `n` 放在最右侧（下标 n-1），它比左边的所有数都小，恰好产生 `n-1` 个新逆序对。  
- 把 `n` 放在中间位置 `pos`（`0 ≤ pos ≤ n-1`），会产生 **`(n-1 - pos)`** 个新逆序对。  

于是，若我们已知 `dp[n-1][x]`（即长度为 `n-1` 的数组恰好有 `x` 个逆序对的种数），则把 `n` 插入可以得到：

```
dp[n][k] = Σ dp[n-1][k - i]   （i = 0 … min(k, n-1)）
```

其中 `i` 表示插入 `n` 产生的逆序对数。  
这就是 **状态转移方程**，但直接套用会导致 `O(n * k * n)`（因为每个 `dp[n][k]` 又要遍历 `i`），仍然太慢。

**前缀和优化**：  
注意到上式是一个 **滑动窗口求和**：  

```
dp[n][k] = dp[n][k-1] + dp[n-1][k] - (k-n >= 0 ? dp[n-1][k-n] : 0)
```

利用前缀和可以把每个 `dp[n][k]` 的计算降到 `O(1)`，整体时间 `O(n * k)`。

**空间优化**：  
`dp[n][*]` 只依赖 `dp[n-1][*]`，可以只保留两行，甚至滚动成一维数组 `dp[k]`（遍历 n 时使用临时数组 `new_dp`）。

**类比**：  
把 `dp[n][k]` 想成“把前 `n` 本书排好后，恰好有 `k` 本书在错位位置的排法”。每加一本新书，只要把它插到不同的位置，就会产生不同数量的错位（逆序对），这正好对应窗口求和的思想。

#### 代码（Python）

```python
MOD = 10**9 + 7

def k_inverse_pairs(n: int, k: int) -> int:
    """
    动态规划 + 前缀和
    dp[i][j] 表示使用 1..i 的数，恰好有 j 个逆序对的排列数。
    只保留一维数组，空间 O(k)。
    """
    # dp_cur 对应 dp[i-1][*]，初始化 i = 0 时只有 dp[0][0] = 1
    dp_cur = [0] * (k + 1)
    dp_cur[0] = 1

    for i in range(1, n + 1):                     # 把第 i 个数加入
        dp_next = [0] * (k + 1)
        # 前缀和变量，用来在 O(1) 时间内得到窗口和
        window_sum = 0
        for j in range(k + 1):
            # 把 dp_cur[j] 加入窗口
            window_sum = (window_sum + dp_cur[j]) % MOD
            # 若窗口大小超过 i（即 i 个数能产生的最大逆序对数），把最左侧的值踢出
            if j - i >= 0:
                window_sum = (window_sum - dp_cur[j - i] + MOD) % MOD
            dp_next[j] = window_sum            # 当前 dp[i][j]
        dp_cur = dp_next                       # 为下一轮做准备
    return dp_cur[k]
```

> **代码要点注释**（已在关键行加中文注释）  
> - `window_sum` 保存 `dp_cur[j] + dp_cur[j-1] + … + dp_cur[j-i+1]`，即上面的滑动窗口。  
> - 当 `j-i >= 0` 时，需要把窗口左边已经超出范围的 `dp_cur[j-i]` 减掉，保持窗口大小不超过 `i`。  
> - 每一次循环都只使用 `O(k)` 的额外空间。

#### 复杂度

- **时间复杂度**：`O(n * k)`  
  - 对每个 `i (1…n)`，我们遍历 `k+1` 个状态，并且每个状态的更新是 `O(1)`（滑动窗口求和）。  
  - 与暴力解的 `O(n! * n²)` 相比，**从指数级降到了多项式级**，即使 `n = 1000, k = 1000` 也能在毫秒级完成。  

- **空间复杂度**：`O(k)`  
  - 只保留当前行和下一行（实际上用 `dp_cur` 与 `dp_next` 两个长度为 `k+1` 的数组），相比原始二维 DP 的 `O(n*k)` 节省了一大块内存。

---

## 心得  

- **核心技巧**：把“把第 n 个数插入已有排列”转化为状态转移，并用 **滑动窗口（前缀和）** 将三重循环降到二重循环。  
- **适用题型**：  
  1. “K Inverse Pairs Array” —— 本题。  
  2. “Number of Permutations with Exactly K Inversions” （同类逆序对计数）。  
  3. “Count Vowels Permutation” —— 也是 DP + 前缀和/滑动窗口的思路。  
- **一句话总结**：**插入法 + 前缀和** 是求逆序对计数的“解题钥匙”。  

---

## 反思  

- **第一反应**：直接想到枚举所有排列，随后发现不可行。  
- **最容易踩的坑**：  
  - **边界条件**：`k` 可能大于 `i*(i-1)/2`（前 `i` 个数最大逆序对），此时 `dp[i][k]` 必须为 0，窗口求和的实现要自动处理（即 `window_sum` 会在 `j` 超出范围时自然为 0）。  
  - **取模负数**：在窗口左移时 `window_sum - dp_cur[...]` 可能出现负数，需要加上 `MOD` 再取模。  
  - **整数溢出**：Python 本身大整数安全，但在取模前要及时 `% MOD`，防止中间值爆炸。  
- **下次类似题目**：第一步先**思考递推**：把大问题拆成“把第 n 个元素放进已有解的方式”，再检查是否可以用**前缀和/滑动窗口**把转移式的求和从 `O(n)` 降到 `O(1)`。