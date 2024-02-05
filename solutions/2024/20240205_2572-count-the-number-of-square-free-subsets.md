# #2572. 统计平方自由子集的数量 / Count the Number of Square-Free Subsets

> 难度：中等 · 标签：Array、Math、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-square-free-subsets/)

---

## 题目（英文原版）

**Description**

You are given a positive integer 0-indexed array nums.
A subset of the array nums is square-free if the product of its elements is a square-free integer.
A square-free integer is an integer that is divisible by no square number other than 1.
Return the number of square-free non-empty subsets of the array nums. Since the answer may be too large, return it modulo 109 + 7.
A non-empty subset of nums is an array that can be obtained by deleting some (possibly none but not all) elements from nums. Two subsets are different if and only if the chosen indices to delete are different.

**Examples**

**Example 1:**

```
Input: nums = [3,4,4,5]
Output: 3
Explanation: There are 3 square-free subsets in this example:
- The subset consisting of the 0th element [3]. The product of its elements is 3, which is a square-free integer.
- The subset consisting of the 3rd element [5]. The product of its elements is 5, which is a square-free integer.
- The subset consisting of 0th and 3rd elements [3,5]. The product of its elements is 15, which is a square-free integer.
It can be proven that there are no more than 3 square-free subsets in the given array.
```

**Example 2:**

```
Input: nums = [1]
Output: 1
Explanation: There is 1 square-free subset in this example:
- The subset consisting of the 0th element [1]. The product of its elements is 1, which is a square-free integer.
It can be proven that there is no more than 1 square-free subset in the given array.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 30

---

## 题目（中文翻译）

你得到一个正整数的 **0 索引数组** `nums`。  
如果一个子集（subset）的所有元素的乘积是 **平方自由整数**（square‑free integer），则称该子集为 **平方自由子集**（square‑free subset）。  

**平方自由整数** 是指除了 1 之外不被任何平方数整除的整数。  

请返回数组 `nums` 中 **非空**（non‑empty）平方自由子集的数量。由于答案可能非常大，请返回其对 $10^9 + 7$ 取模后的结果。

**非空子集** 是指可以通过删除 `nums` 中若干（可能为零但不能全部）元素得到的数组。只有当删除的下标集合不同，两个子集才视为不同。

### 示例

**示例 1**

```
Input: nums = [3,4,4,5]
Output: 3
Explanation: 本例中有 3 个平方自由子集：
- 只包含第 0 个元素的子集 [3]，其元素乘积为 3，是平方自由整数；
- 只包含第 3 个元素的子集 [5]，其元素乘积为 5，是平方自由整数；
- 包含第 0 和第 3 个元素的子集 [3,5]，其元素乘积为 15，是平方自由整数。
```

**示例 2**

```
Input: nums = [1]
Output: 1
Explanation: 本例中只有 1 个平方自由子集：
- 只包含第 0 个元素的子集 [1]，其元素乘积为 1，是平方自由整数。
可以证明，对于给定的数组，最多只能有 1 个平方自由子集。
```

### 约束

- $1 \le \text{nums.length} \le 1000$
- $1 \le \text{nums}[i] \le 30$

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组的所有**非空子集**枚举出来，逐个计算子集里元素的乘积，判断这个乘积是否是「无平方因子」的（square‑free）数。  

- **枚举子集**：可以把每个位置看成「要不要选」的开关，`0` 表示不选，`1` 表示选。长度为 `n` 的数组就有 `2ⁿ` 种开关组合（除去全 `0` 的情况即空集）。  
- **乘积**：把子集里所有选中的数相乘。  
- **判断 square‑free**：把乘积进行质因数分解，如果任意质因数的指数大于 `1`（即出现了 `p²`），则说明乘积包含平方因子，不符合要求。  

> **类比**：把 `nums` 想象成一篮子水果，每个水果上贴有编号（数字）。我们要挑选若干水果（子集），把它们的编号相乘，检查结果里有没有「同一种水果出现两次以上」的情况（这对应质因数出现两次以上），如果没有，就算合格。

**为什么正确**：我们遍历了所有可能的子集，并对每个子集做了完整的检查，只要符合条件就计数，最终得到的计数自然就是答案。

#### 代码（Python）

```python
import math
from itertools import combinations

MOD = 10**9 + 7

def is_square_free(x: int) -> bool:
    """判断整数 x 是否为 square‑free（没有平方因子 >1）"""
    # 只需要检查到 sqrt(x) 即可
    i = 2
    while i * i <= x:
        cnt = 0
        while x % i == 0:
            x //= i
            cnt += 1
            if cnt > 1:          # 出现了 i 的平方因子
                return False
        i += 1
    return True                # 没有出现指数 ≥2 的质因数

def count_square_free_subsets_bruteforce(nums):
    n = len(nums)
    ans = 0
    # 用二进制枚举所有非空子集
    for mask in range(1, 1 << n):          # 1~2ⁿ-1，排除全 0（空集）
        prod = 1
        for i in range(n):
            if mask >> i & 1:              # 第 i 位为 1，说明选了 nums[i]
                prod *= nums[i]
        if is_square_free(prod):
            ans = (ans + 1) % MOD
    return ans
```

> 关键行解释  
> - `for mask in range(1, 1 << n)`: 把每一种「选或不选」的组合当作二进制数遍历。  
> - `if mask >> i & 1`: 检查第 `i` 位是否为 `1`，即是否选了第 `i` 个元素。  
> - `is_square_free(prod)`: 判断乘积是否满足「没有平方因子」的条件。  

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 是子集的数量（每个元素都有「选」或「不选」两种可能）。  
  - 对每个子集我们最多要遍历 `n` 次来计算乘积并检查平方因子。  
  - 用大白话说，就是「数组有 20 个元素时，子集有 1,048,576 种，算起来会很慢」。

- **空间复杂度**：`O(1)`（不计输出的变量）  
  - 只用了常数级别的额外变量（`prod`、`mask` 等），没有随 `n` 增长的额外存储。

> 由于 `n ≤ 1000`，`2^n` 远远超出计算机的承受范围，暴力解在本题根本不可行，只能用来帮助我们理清「子集」和「square‑free」的概念。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有子集**。我们需要一种方式 **直接在「状态」层面计数**，而不是一个子集一个子集地遍历。  

观察题目限制：

| 条件 | 含义 |
|------|------|
| `1 ≤ nums[i] ≤ 30` | 每个数最大只有 30，质因数只有前 10 个质数（2,3,5,7,11,13,17,19,23,29）。 |
| `len(nums) ≤ 1000` | 元素很多，但每个元素的「信息」很小（只关心它的质因数是否出现）。 |

**关键点**：如果两个数的质因数集合 **有交集**，把它们放进同一个子集会导致某个质因数的指数 ≥ 2，从而出现平方因子，不合法。换句话说，合法子集对应的 **质因数集合** 必须是两两不相交的。

于是我们可以把每个数 **压缩成一个 10 位的二进制掩码**（bitmask）：

- 第 `k` 位为 `1` 表示该数的质因数中包含第 `k` 个质数（`2,3,…,29`）。  
- 如果某个数本身就包含了 **平方因子**（比如 `4 = 2²`、`9 = 3²`、`12 = 2²·3`），则它 **永远不能** 被放入任何合法子集（因为它已经把某个质数的指数提升到 2），只能被「舍弃」。

这样，**合法子集** 就等价于 **挑选若干个互不冲突的掩码**，并把它们的掩码做按位或（`|`）后仍然保持每个位最多出现一次。

这正好可以用 **动态规划 + 位掩码** 来实现：

- `dp[mask]` 表示「已经处理完前面若干个元素，当前子集的质因数集合恰好是 `mask`」的子集数量。  
- 初始时 `dp[0] = 1`（空子集的质因数集合为空）。  
- 对于数组中的每个数 `x`（忽略掉含平方因子的数），计算它的掩码 `m`。  
  - 若 `mask & m != 0`，说明 `mask` 已经用了 `x` 的某个质因数，**不能** 再把 `x` 加进去。  
  - 否则，可以把 `x` 加入到所有不冲突的状态中：`dp[mask | m] += dp[mask]`。  

**特殊处理 `1`**：`1` 没有质因数，加入 `1` 不会改变掩码。因此每出现一次 `1`，所有已有的合法子集都可以 **选择是否再乘一个 `1`**，相当于把答案乘以 `2^{cnt1}`（`cnt1` 为 `1` 的出现次数），最后再减去空集。

#### 步骤细化

1. **预处理**  
   - 列出前 10 个质数并记录它们的下标。  
   - 对每个 `num`，判断是否含有平方因子。若有，直接跳过。否则计算它的掩码 `mask(num)`。  
   - 统计 `1` 的出现次数 `cnt1`，因为 `1` 的掩码是 `0`，我们单独记。

2. **DP 迭代**  
   - 创建长度为 `2^10 = 1024` 的数组 `dp`，`dp[0] = 1`。  
   - 对每个非 `1` 且无平方因子的数的掩码 `m`：  
     - 从大到小遍历 `mask`（从 `1023` 到 `0`），防止同一次迭代中把新加入的状态再次使用。  
     - 若 `mask & m == 0`，则 `dp[mask | m] = (dp[mask | m] + dp[mask]) % MOD`。

3. **统计答案**  
   - 所有非空子集对应的掩码 `mask != 0`，把它们的计数相加得到 `ans`。  
   - 把 `1` 的贡献乘进去：`ans = ans * pow(2, cnt1, MOD) % MOD`。  
   - 最后 **减去空集**（因为我们在 DP 中把空集计入了 `dp[0]`）：`ans = (ans - 1 + MOD) % MOD`。

> **为什么要倒序遍历 mask**  
> 假设我们正处理一个数的掩码 `m`，如果正向遍历 `mask`，当我们把 `dp[mask]` 加到 `dp[mask|m]` 时，`dp[mask|m]` 已经在本轮循环中可能被后面的 `mask` 再次使用，导致同一个数被算进多次。倒序遍历保证每个数只会被加一次。

#### 代码（Python）

```python
MOD = 10**9 + 7

# 前 10 个 <=30 的质数，按顺序编号 0~9
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
prime_to_idx = {p: i for i, p in enumerate(PRIMES)}

def mask_of(num: int) -> int:
    """
    返回 num 对应的 10 位掩码。
    若 num 含有平方因子（如 4、12），返回 -1 表示不可用。
    """
    mask = 0
    for p in PRIMES:
        if p * p > num:          # 剩下的因子只可能是 1 或本身（质数）
            break
        cnt = 0
        while num % p == 0:
            num //= p
            cnt += 1
        if cnt > 1:              # 出现了 p 的平方因子
            return -1
        if cnt == 1:             # 只出现一次，记录在 mask 中
            mask |= 1 << prime_to_idx[p]
    # 处理剩余的质因数（如果还有且不是 1）
    if num > 1:                  # 这里的 num 必然是质数且只出现一次
        # 该质数一定在 PRIMES 中（因为 num <= 30）
        idx = prime_to_idx[num]
        mask |= 1 << idx
    return mask

def count_square_free_subsets(nums):
    cnt_one = 0                 # 记录 1 的个数
    masks = []                  # 其余合法数的掩码列表

    for x in nums:
        if x == 1:
            cnt_one += 1
            continue
        m = mask_of(x)
        if m != -1:             # -1 表示含平方因子，直接丢弃
            masks.append(m)

    # dp[mask] = 当前已选数的质因数集合恰为 mask 的子集数目
    dp = [0] * (1 << len(PRIMES))   # 2^10 = 1024
    dp[0] = 1                       # 空子集

    for m in masks:
        # 为防止同一轮中重复使用新状态，倒序遍历
        for mask in range((1 << len(PRIMES)) - 1, -1, -1):
            if dp[mask] == 0:
                continue
            if mask & m:            # 与已有质因数冲突，不能加入
                continue
            new_mask = mask | m
            dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD

    # 所有非空子集的数量（mask != 0）
    ans = sum(dp[1:]) % MOD

    # 每个 1 可以任选是否加入，等价于乘以 2^cnt_one
    if cnt_one:
        ans = ans * pow(2, cnt_one, MOD) % MOD

    # 最终答案不包括空集（dp[0] 只算了空集）
    return ans % MOD
```

> 关键行解释  
> - `mask_of`：把一个数拆成质因数并生成二进制掩码，若出现平方因子立即返回 `-1`。  
> - `dp[0] = 1`：空子集算作一种「状态」，后面会把它乘以 `2^{cnt_one}` 再减去空集得到最终答案。  
> - `for mask in range(..., -1, -1)`：倒序遍历保证每个数只使用一次。  
> - `ans = sum(dp[1:])`：把所有非空掩码对应的计数加起来。  
> - `pow(2, cnt_one, MOD)`：快速求 `2^cnt_one mod MOD`，对应把每个 `1` 加入或不加入的两种选择。

#### 复杂度

- **时间复杂度**：`O(n * 2^P)`，其中 `P = 10`（30 以内的质数个数），`2^P = 1024`。  
  - 对每个元素我们只做一次掩码计算（`O(P)`），随后遍历所有 `1024` 种掩码状态。  
  - 用大白话说，就是「即使数组有 1000 个数，也只会跑大约 1 000 000 次循环，完全可以在毫秒级完成」。

- **空间复杂度**：`O(2^P)`，即 `1024` 的整数数组 `dp`。  
  - 与 `n` 无关，常数级别的额外空间。

> 与暴力解相比，时间从指数级（`2^n`）降到了 **线性 × 常数**（`n * 1024`），大幅提升。

---

## 心得

- **核心技巧**：**位掩码 + 动态规划**，把「质因数不冲突」的约束转化为「二进制位不相交」的状态转移。  
- **适用题型**（类似思路）  
  1. **Count the Number of Good Subsets**（LeetCode 1994）  
  2. **Maximum Subset Product with No Common Prime Factors**（变体）  
  3. **Maximum Size Subset With No Repeating Prime Factors**（自定义）  
- **一句话总结解题钥匙**：**把每个数压成「哪些质数出现」的二进制标签，用 DP 按位合并，确保标签不冲突**。

---

## 反思

- **第一反应**：直接枚举子集检查乘积是否 square‑free。虽然思路最直观，却忽视了 `n` 可达 1000，导致不可行。  
- **最容易踩的坑**  
  - **遗漏平方因子**：比如 `4 = 2²`、`12 = 2²·3`，这些数本身已经不合法，必须在预处理阶段直接丢掉。  
  - **`1` 的特殊处理**：`1` 没有质因数，加入后不改变掩码，需要单独计数并在最后乘以 `2^{cnt1}`。  
  - **状态重复计数**：DP 更新时必须倒序遍历，否则同一轮会把同一个数算进多次。  
- **下次遇到同类题**：第一步先**抽象出「冲突」的概念（如质因数冲突、位冲突），看能否用**位掩码**把冲突映射为「位与不为 0」，再考虑**DP/子集枚举**在「状态空间」上做动态规划。这样往往能把指数爆炸的问题压缩到 `2^{(小常数)}` 级别。