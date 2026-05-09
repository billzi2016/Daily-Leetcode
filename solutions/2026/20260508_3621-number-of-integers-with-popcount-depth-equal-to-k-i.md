# #3621. Popcount 深度等于 K 的整数个数 I / Number of Integers With Popcount-Depth Equal to K I

> 难度：困难 · 标签：Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/number-of-integers-with-popcount-depth-equal-to-k-i/)

---

## 题目（英文原版）

**Description**

You are given two integers n and k.
For any positive integer x, define the following sequence:
This sequence will eventually reach the value 1.
The popcount-depth of x is defined as the smallest integer d >= 0 such that pd = 1.
For example, if x = 7 (binary representation "111"). Then, the sequence is: 7 → 3 → 2 → 1, so the popcount-depth of 7 is 3.
Your task is to determine the number of integers in the range [1, n] whose popcount-depth is exactly equal to k.
Return the number of such integers.

**Examples**

**Example 1:**

```
Input: n = 4, k = 1
Output: 2
Explanation:
The following integers in the range [1, 4] have popcount-depth exactly equal to 1:
Thus, the answer is 2.
```

**Example 2:**

```
Input: n = 7, k = 2
Output: 3
Explanation:
The following integers in the range [1, 7] have popcount-depth exactly equal to 2:
Thus, the answer is 3.
```

**Constraints**

- 1 <= n <= 1015
- 0 <= k <= 5

---

## 题目（中文翻译）

给定两个整数 `n` 和 `k`。  

对于任意正整数 `x`，定义如下序列：

- 设 `p0 = x`；
- 对于 `i ≥ 0`，令 `p(i+1) = popcount(p(i))`，其中 **popcount** 表示二进制表示中 `1` 的个数。

该序列必然会在某一步达到值 `1`。  

**popcount-depth**（popcount 深度）定义为最小的整数 `d ≥ 0`，使得 `p(d) = 1`。  

例如，`x = 7`（二进制为 `"111"`），序列为 `7 → 3 → 2 → 1`，因此 `7` 的 popcount-depth 为 `3`。  

你的任务是统计区间 `[1, n]` 中 **popcount-depth** 恰好等于 `k` 的整数个数，并返回该数量。

---

### 示例

#### 示例 1
**输入**  
`n = 4, k = 1`

**输出**  
`2`

**解释**  
在区间 `[1, 4]` 中，popcount-depth 正好为 `1` 的整数有 `1`（序列 `1`）和 `2`（序列 `2 → 1`），因此答案为 `2`。

#### 示例 2
**输入**  
`n = 7, k = 2`

**输出**  
`3`

**解释**  
在区间 `[1, 7]` 中，popcount-depth 正好为 `2` 的整数有 `3`（`3 → 1`）、`4`（`4 → 1`）和 `5`（`5 → 2 → 1`），所以答案为 `3`。

---

### 约束条件

- `1 ≤ n ≤ 10^15`
- `0 ≤ k ≤ 5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把区间 `[1, n]` 里的每一个整数都枚举出来，逐个计算它的 **popcount‑depth**（即把整数的二进制中 `1` 的个数一直取 `popcount`，直到得到 `1` 为止，需要的步骤数）。  

- **计算 popcount‑depth**：把整数 `x` 转成二进制，统计 `1` 的个数得到 `p1`，再对 `p1` 统计 `1` 的个数得到 `p2` …… 直到出现 `1` 为止，步骤数就是深度 `d`。  
- **判断是否满足**：如果得到的 `d` 正好等于给定的 `k`，计数器 `ans` 加一。  

> **类比**：把 `popcount` 想成“数字里有多少颗星星”。我们不断把星星的数量再变成星星的数量，直到只剩一颗星星。  

因为我们真的把每个数都算了一遍，这个方法一定是 **正确** 的——只要把所有可能的数都检查一遍，答案自然不可能错。

#### 代码（Python）

```python
def popcount(x: int) -> int:
    """返回 x 的二进制中 1 的个数，相当于数星星"""
    return bin(x).count('1')

def depth(x: int) -> int:
    """返回 x 的 popcount‑depth（步骤数）"""
    d = 0
    while x != 1:
        x = popcount(x)   # 把星星的数量再变成星星的数量
        d += 1
    return d

def brute_force(n: int, k: int) -> int:
    """
    暴力枚举 1..n，统计深度恰好等于 k 的数的个数
    时间复杂度大约是 O(n * log n)（因为每次 popcount 需要遍历二进制位）
    """
    ans = 0
    for x in range(1, n + 1):
        if depth(x) == k:
            ans += 1
    return ans
```

> 这段代码可以直接跑在 Python 解释器里，只要 `n` 不太大（比如 `n ≤ 10^5`）就能在几秒内得到答案。  

#### 复杂度  

- **时间复杂度**：`O(n · log n)`  
  - `n` 表示我们要检查的数字个数。  
  - `log n` 是因为每次 `popcount` 需要遍历该数字的二进制位数（大约是 `log₂ n` 位），而深度最多也只有几层（本题 `k ≤ 5`），所以整体是 `n` 乘以一个很小的常数。  
  - 用“大白话”说，就是如果 `n = 1,000,000`，我们大约要做 **一百万次** 的“数星星”，每次数的位数不超过 20，所以大概是 **两千万次** 基本操作，已经算是“慢”了。  

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的变量 `ans、d、x`，不随 `n` 增长。  

> 暴力解虽然思路最清晰，但当 `n` 大到 `10¹⁵` 时根本不可行——这就是我们需要更聪明的方法的动机。  

---  

### 2. 最优解  

#### 思路  

**瓶颈**：暴力解的时间随 `n` 线性增长，而题目给出的 `n` 上限是 `10¹⁵`（约 50 位二进制），根本不可能逐个枚举。我们需要利用 **“数字的结构”** 来一次性统计满足条件的数字，而不是一个一个数。

**关键观察**  

1. **只和“二进制中 1 的个数”有关**  
   - 对于任意整数 `x`，它的 popcount‑depth 只取决于 `x` 的 **`1` 的个数**（记作 `ones(x)`），而不关心 `1` 在哪一位。  
   - 也就是说，所有二进制中 `1` 的个数相同的数，它们的深度完全相同。  

2. **把问题拆成两步**  
   - **步骤 1**：先统计 `1 ≤ y ≤ n` 中，**恰好有 `j` 个 `1` 的数有多少**（记作 `cnt[j]`）。  
   - **步骤 2**：预先算出每个可能的 `j`（`0 ≤ j ≤ 64`）对应的 popcount‑depth `dep[j]`。答案就是所有 `j` 满足 `dep[j] == k` 的 `cnt[j]` 之和。  

3. **如何快速得到 `cnt[j]`**  
   - 这正是 **“数位 DP（Digit DP）”** 在二进制上的典型用法。我们从最高位向最低位逐位决定是 `0` 还是 `1`，并记录截至目前已经放了多少个 `1`。  
   - 状态定义  
     ```
     dp[pos][ones][tight] = 选到第 pos 位（从最高位往下数）时，
                           已经放了 `ones` 个 1，
                           且 tight = 1 表示前面的位严格等于 n 的前缀，
                           tight = 0 表示已经小于 n，后面的位可以随意取。
     ```  
   - 转移  
     - 如果 `tight == 1`，当前位最多只能取 `n` 的对应位（0 或 1），否则可以随意取 `0/1`。  
     - 把选的 `0/1` 加到 `ones` 中，更新 `tight`（如果选的位小于 n 的位，则后面全部可以随意取，即 `tight` 变 0）。  
   - 结束时 `pos == -1`（所有位都处理完），把 `dp` 的值累加到 `cnt[ones]`。  

4. **深度的预计算**  
   - `j` 的范围最多是二进制位数（`≤ 64`），我们直接对每个 `j` 反复做 `popcount`，直到得到 `1`，记录需要的步数 `dep[j]`。这一步非常快，只需要几次循环。  

5. **整体流程**  

   1. **预处理**：计算 `dep[0..64]`。  
   2. **数位 DP**：得到 `cnt[0..64]`，即 `≤ n` 且 `1` 的个数为 `j` 的数的数量。  
   3. **求答案**：`ans = Σ cnt[j] (dep[j] == k)`。  

**为什么 DP 能快？**  
- 二进制位数最多 60（因为 `2⁶⁰ ≈ 10¹⁸ > 10¹⁵`），`ones` 最多也是 60，`tight` 只有 2 种。状态数约为 `60 × 61 × 2 ≈ 7320`，每个状态只转移两次（放 0 或 1），所以总运算在几万次级别，瞬间完成。  

**类比**：把 `n` 看成一条“限高的楼梯”。我们从最高楼层往下走，每一步可以决定是“踩空（0）”还是“踩实（1）”。只要一开始没有踩到比楼梯更高的层（`tight`），后面随便怎么走都合法。我们只记录一路走下来踩了几块实踏（`1`），最后把所有走法的统计加起来，就是答案。  

#### 代码（Python）

```python
from functools import lru_cache

# -------------------------------------------------
# 1. 预计算每个可能的 1 的个数的 popcount‑depth
# -------------------------------------------------
def compute_depth(limit: int = 64) -> list[int]:
    """
    depth[j] = popcount-depth of the integer j (j <= limit)
    """
    depth = [0] * (limit + 1)
    for j in range(limit + 1):
        d = 0
        x = j
        while x != 1:
            # 统计 x 二进制中 1 的个数
            x = bin(x).count('1')
            d += 1
        depth[j] = d          # 当 j == 1 时，循环一次也会得到 d == 0，符合定义
    return depth

DEP = compute_depth()          # 全局缓存，后面直接查表

# -------------------------------------------------
# 2. 数位 DP：统计 ≤ n 的数中恰好有 j 个 1 的数量
# -------------------------------------------------
def count_by_ones(n: int) -> list[int]:
    """
    返回一个长度为 65 的列表 cnt，cnt[j] 表示 1 ≤ x ≤ n 且
    二进制中恰好有 j 个 1 的数的个数。
    """
    # 把 n 写成二进制的位数组，最高位在前
    bits = list(map(int, bin(n)[2:]))   # 例如 n=13 -> ['1','1','0','1'] -> [1,1,0,1]
    L = len(bits)                       # 位数，最多 60

    @lru_cache(maxsize=None)
    def dp(pos: int, ones: int, tight: int) -> int:
        """
        pos   : 当前处理的位的下标（从 0 开始），0 表示最高位
        ones  : 已经放了多少个 1
        tight : 1 表示前缀和 n 完全相同，0 表示已经小于 n
        返回：从 pos 开始到最低位，合法的组合数
        """
        if pos == L:                     # 已经处理完所有位
            # 此时形成了一个完整的数字，统计它的 1 的个数
            # 注意题目要求的是 1 ≤ x ≤ n，0 不算在内，后面会统一减去
            return 1

        # 当前位 n 上的实际取值（只在 tight 为 1 时受限制）
        limit_bit = bits[pos] if tight else 1

        total = 0
        for dig in (0, 1):
            if dig > limit_bit:          # 不能超过 n 在该位的限制
                continue
            next_tight = tight and (dig == limit_bit)
            total += dp(pos + 1, ones + dig, next_tight)
        return total

    # dp 会返回所有合法数字的总数（包括 0），我们需要把每种 ones 的计数拆出来
    # 为此我们再跑一次遍历，把每个状态的贡献累加到 cnt[ones] 中
    cnt = [0] * (L + 1)                   # 最多 L 个 1

    # 下面用一个显式的递归遍历，把每条路径的 ones 计入 cnt
    def collect(pos: int, ones: int, tight: int):
        if pos == L:
            cnt[ones] += 1                # 完成一个数字
            return
        limit_bit = bits[pos] if tight else 1
        for dig in (0, 1):
            if dig > limit_bit:
                continue
            next_tight = tight and (dig == limit_bit)
            collect(pos + 1, ones + dig, next_tight)

    collect(0, 0, 1)

    # 去掉 0 本身（因为题目范围是 [1, n]），0 的 ones 为 0
    cnt[0] -= 1
    return cnt

# -------------------------------------------------
# 3. 主函数：计算答案
# -------------------------------------------------
def number_of_integers(n: int, k: int) -> int:
    """
    返回区间 [1, n] 中 popcount-depth 恰好等于 k 的整数个数
    """
    # 1) 统计每种 1 的个数出现了多少次
    cnt = count_by_ones(n)          # cnt[j] 对应的是「恰好有 j 个 1」的数量

    # 2) 把深度为 k 的所有 j 累加
    ans = 0
    for j, c in enumerate(cnt):
        if c == 0:
            continue
        if DEP[j] == k:              # DEP 已经预先算好
            ans += c
    return ans

# -------------------------------------------------
# 4. 简单的测试
# -------------------------------------------------
if __name__ == "__main__":
    print(number_of_integers(4, 1))   # 示例 1，输出 2
    print(number_of_integers(7, 2))   # 示例 2，输出 3
```

**代码说明（关键行中文注释）**  

- `compute_depth`：对每个可能的 `j`（最多 64）反复取 `popcount`，记录需要多少次才能变成 `1`。  
- `bits = list(map(int, bin(n)[2:]))`：把 `n` 转成二进制位列表，方便逐位 DP。  
- `dp`（使用 `lru_cache`）是典型的 **记忆化搜索**，避免重复计算同一状态。  
- `collect`：实际把每条合法路径的 `ones` 累计到 `cnt` 中；这里没有使用 `dp` 的返回值来直接统计，是因为我们需要 **每种 `ones` 的分布**。  
- `cnt[0] -= 1`：把数字 `0`（不在题目范围）剔除。  
- 最后遍历 `j`，只把 `DEP[j] == k` 的计数加到答案。  

#### 复杂度  

- **时间复杂度**：`O(L²)`（其中 `L` 为 `n` 的二进制位数，最大约 60）  
  - 状态数约 `L × (L+1) × 2`，每个状态最多转移两次，整体大约几千次操作。  
  - 用“大白话”说，就是 **即使 `n = 10¹⁵`，程序也只跑几万步，几乎瞬间完成**。  

- **空间复杂度**：`O(L²)` 用于缓存 DP 状态（约几千个整数），再加上 `cnt` 数组的 `O(L)`。这在现代计算机上几乎可以忽略不计。  

> 与暴力解相比，时间从 **线性 `n`（甚至上万倍）** 降到了 **与 `n` 位数同阶的常数**，是本题唯一可行的思路。  

---  

## 心得  

- **核心技巧**：**数位 DP（Digit DP）** + **预计算 popcount‑depth**。  
- **适用的题型**（可以在面试或练习中多练）：  
  1. “统计 ≤ N 的二进制/十进制满足某种位数约束的数”——如 *Number of Integers with Even Digit Sum*。  
  2. “求 ≤ N 的数中，`1` 的个数恰好为 `k` 的数量”——如 *Counting Numbers with Fixed Hamming Weight*。  
  3. “利用位运算属性把问题转化为计数”——如 *Count Numbers with Given Number of Set Bits After Repeated Popcount*（本题的变形）。  

- **一句话总结解题钥匙**：  
  > “把原问题拆成‘先统计 1 的个数’，再把每个‘1 的个数’映射到固定的深度”。  

---  

## 反思  

- **第一反应**：看到 `popcount‑depth`，立刻想到要对每个数模拟过程，结果发现 `n` 太大，必须找规律。  
- **最容易踩的坑**：  
  1. **忘记排除 0**：数位 DP 自然会计入 `0`（所有位都取 0），但题目区间是 `[1, n]`，需要手动减掉。  
  2. **`k = 0` 的特殊情况**：只有 `x = 1` 的深度为 0，确保 `DEP[1] = 0`（在预计算时循环会直接得到 0 步）。  
  3. **位数上限**：`n` 最高到 `10¹⁵`，二进制位数约 50，代码里要准备足够的数组（如 `cnt` 长度 `L+1`），防止越界。  

- **下次遇到同类题**：  
  1. **先判断答案是否只和“位的统计量”有关**（如 `1` 的个数、奇偶性、和等）。  
  2. **若是，立刻考虑数位 DP**，把整个范围的计数转化为“在每一位上选 0/1，满足前缀约束”。  
  3. **再把统计结果映射到原问题的判定条件**（本题是 `depth[j] == k`）。  

这样一步步拆解，就能把看似 “Hard” 的题目变成可管理的子问题，顺利写出高效的解法。