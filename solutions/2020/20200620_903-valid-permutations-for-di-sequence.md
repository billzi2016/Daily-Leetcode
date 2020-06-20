# #903. **有效的 DI 序列排列** / Valid Permutations for DI Sequence

> 难度：困难 · 标签：String、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/valid-permutations-for-di-sequence/)

---

## 题目（英文原版）

**Description**

You are given a string s of length n where s[i] is either:
A permutation perm of n + 1 integers of all the integers in the range [0, n] is called a valid permutation if for all valid i:
Return the number of valid permutations perm. Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "DID"
Output: 5
Explanation: The 5 valid permutations of (0, 1, 2, 3) are:
(1, 0, 3, 2)
(2, 0, 3, 1)
(2, 1, 3, 0)
(3, 0, 2, 1)
(3, 1, 2, 0)
```

**Example 2:**

```
Input: s = "D"
Output: 1
```

**Constraints**

- n == s.length
- 1 <= n <= 200
- s[i] is either 'I' or 'D'.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串 `s`，其中 `s[i]` 只能是字符 `'I'`（Increasing）或 `'D'`（Decreasing）。  

一个由区间 `[0, n]` 内所有整数构成的排列 `perm`（permutation）如果满足对所有合法的下标 `i`：

- 当 `s[i] == 'I'` 时，`perm[i] < perm[i+1]`；
- 当 `s[i] == 'D'` 时，`perm[i] > perm[i+1]`；

则称该排列为**有效排列**（valid permutation）。

求满足上述条件的有效排列的数量。由于答案可能非常大，请返回 `answer mod 10^9 + 7` 的结果。

---

### 示例

**示例 1**

```
输入: s = "DID"
输出: 5
解释: 对于整数集合 (0, 1, 2, 3) 的所有排列中，满足条件的有 5 种：
(1, 0, 3, 2)
(2, 0, 3, 1)
(2, 1, 3, 0)
(3, 0, 2, 1)
(3, 1, 2, 0)
```

**示例 2**

```
输入: s = "D"
输出: 1
```

---

### 约束条件

- `n == s.length`
- `1 <= n <= 200`
- `s[i]` 只能是 `'I'` 或 `'D'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **0 ~ n** 的所有 `n+1` 个数全部列举出来，形成所有可能的排列（全排列），然后逐个检查它们是否满足字符序列 `s` 的要求。

- **全排列**可以看成把 `n+1` 本不同颜色的球全部排成一行，顺序有多少种就有多少种排列。  
- 检查过程类似“老师出题，让我们把这些球按照 `I`（Increasing）和 `D`（Decreasing）的提示依次比较相邻两个球的大小”。  
  - 如果 `s[i] == 'I'`，则要求 `perm[i] < perm[i+1]`（前面的球要比后面的球小），  
  - 如果 `s[i] == 'D'`，则要求 `perm[i] > perm[i+1]`（前面的球要比后面的球大）。  

只要所有位置都满足，当前排列就是 **合法的**。

> **为什么这种方法一定能得到答案？**  
> 因为我们枚举了**所有**可能的排列，合法与否只在检查阶段决定，必然不会漏掉任何一个满足条件的排列。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def numPerms_bruteforce(s: str) -> int:
    n = len(s)
    nums = list(range(n + 1))                 # 0 ~ n 的所有整数
    ans = 0

    # itertools.permutations 会产生所有 (n+1)! 种排列
    for perm in itertools.permutations(nums):
        ok = True
        for i, ch in enumerate(s):
            if ch == 'I' and not (perm[i] < perm[i + 1]):   # 需要递增却不满足
                ok = False
                break
            if ch == 'D' and not (perm[i] > perm[i + 1]):   # 需要递减却不满足
                ok = False
                break
        if ok:
            ans += 1
    return ans % MOD
```

> **关键行中文注释**  
> - `itertools.permutations(nums)`：把所有球全排列，像把字典里每个单词的所有字母全排一次。  
> - `if ch == 'I' and not (perm[i] < perm[i + 1])`：如果提示是递增，但当前两个数不满足递增，就立刻淘汰。  

#### 复杂度  

- **时间复杂度**：`O((n+1)!)`  
  - “阶乘”可以理解为：当 `n=3` 时，需要尝试 4! = 24 次；`n=5` 时要尝试 6! = 720 次，随着 `n` 增大，增长非常快（指数级），几乎不可能在合理时间内跑完 `n=200`。  
- **空间复杂度**：`O(n)`  
  - 只需要存放当前的排列（长度 `n+1`），以及常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**，而我们只关心满足 `I/D` 关系的排列数目，不需要真的把每个排列写出来。  
可以把问题转化为**计数**：在第 `i` 步（处理 `s[0..i-1]`）时，有多少种合法的前缀排列可以得到每一种可能的**最后一个数字**。

设 `dp[i][j]` 表示：  
> 前 `i` 个字符（即已经放了 `i` 个数，长度为 `i`）构成的合法排列，且**第 i 个位置**放的是第 `j` 小的剩余数字时，有多少种不同的排列。

- `i` 从 `1` 到 `n+1`（因为我们最终要排 `n+1` 个数）。  
- `j` 从 `0` 到 `i-1`（因为已经用了 `i` 个数，剩下的最小数的序号最多是 `i-1`）。

**状态转移**：

- 如果 `s[i-1] == 'I'`（第 `i-1` 位需要递增），则第 `i-1` 位的数字必须 **小于** 第 `i` 位的数字。  
  - 因此 `dp[i][j]` 可以由所有 **更小的** `k (< j)` 的 `dp[i-1][k]` 累加得到。  
- 如果 `s[i-1] == 'D'`（第 `i-1` 位需要递减），则第 `i-1` 位的数字必须 **大于** 第 `i` 位的数字。  
  - 此时 `dp[i][j]` 可以由所有 **不小于** `k (≥ j)` 的 `dp[i-1][k]` 累加得到。

直接遍历 `k` 会导致 `O(n^3)`，但是我们可以利用 **前缀和**（或后缀和）把每一次求和压到 `O(1)`，整体降到 `O(n^2)`。

- 对于递增情况：  
  `dp[i][j] = prefix[i-1][j-1]`（`prefix[i-1][x]` 为 `dp[i-1][0..x]` 的累计和）。  
- 对于递减情况：  
  `dp[i][j] = (prefix[i-1][i-2] - prefix[i-1][j-1])`，即把大于等于 `j` 的部分相减得到。

**初始化**：`dp[1][0] = 1`，因为只有一个数（0），唯一一种排列。

**答案**：`sum(dp[n+1][j] for j in range(n+1))`，即把最后一步所有可能的结尾数加起来。

> **类比**：把 `dp` 看成“在每一步我们站在一条河边，`j` 表示我们站在第几块石头上”。  
> - `I` 表示我们只能往右走（只能站在更大的石头），  
> - `D` 表示只能往左走（只能站在更小的石头）。  
> 前缀和相当于我们把所有已经走到左边石头的路线一次性算好，省去逐个枚举。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numPerms(s: str) -> int:
    n = len(s)
    # dp[i][j] : 前 i 个字符（即已经放了 i 个数），第 i 个位置是第 j 小的数的方案数
    dp = [[0] * (i + 1) for i in range(n + 2)]   # i 从 1 到 n+1
    dp[1][0] = 1                                 # 只放第一个数，唯一方案

    # 为了快速求前缀和，额外维护 prefix[i][j] = sum_{k=0}^{j} dp[i][k]
    prefix = [[0] * (i + 1) for i in range(n + 2)]
    prefix[1][0] = 1

    for i in range(2, n + 2):            # i 表示已经放了 i 个数
        if s[i - 2] == 'I':              # 前一位要求递增
            # dp[i][j] = prefix[i-1][j-1] （j 为 0 时没有合法前缀，值为 0）
            for j in range(i):
                if j == 0:
                    dp[i][j] = 0
                else:
                    dp[i][j] = prefix[i - 1][j - 1] % MOD
        else:                             # 前一位要求递减
            # dp[i][j] = prefix[i-1][i-2] - prefix[i-1][j-1]
            total = prefix[i - 1][i - 2]   # 前 i-1 行所有 dp 的累计和
            for j in range(i):
                if j == 0:
                    dp[i][j] = total % MOD
                else:
                    dp[i][j] = (total - prefix[i - 1][j - 1]) % MOD

        # 更新本行的前缀和，供下一轮使用
        cur_sum = 0
        for j in range(i):
            cur_sum = (cur_sum + dp[i][j]) % MOD
            prefix[i][j] = cur_sum

    # 最后一行 i = n+1，所有可能的结尾都算进去
    return sum(dp[n + 1]) % MOD
```

> **关键行中文注释**  
> - `dp = [[0] * (i + 1) for i in range(n + 2)]`：创建一个梯形表格，行号 `i` 对应 “已经放了 i 个数”。  
> - `if s[i - 2] == 'I':`：因为 `s` 的下标比 `i` 小 1，需要用 `i-2` 取对应的字符。  
> - `prefix[i - 1][j - 1]`：前缀和帮助我们一次性把所有 “比 j 小的” 状态加起来。  
> - `total = prefix[i - 1][i - 2]`：`i-1` 行所有状态的总和，用来计算 “大于等于 j” 的部分。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层循环：外层遍历 `i = 2 .. n+1`（约 `n` 次），内层遍历 `j = 0 .. i-1`（平均约 `n/2` 次），所以总操作数约为 `n·n/2 = n²/2`。  
  - 相比暴力的阶乘级别，这已经是可以接受的（`n ≤ 200` 时最多约 40,000 次运算）。  
- **空间复杂度**：`O(n²)`  
  - 存储 `dp` 与 `prefix` 两个大小为 `≈ (n+2)·(n+2)/2` 的梯形表格，最多约 20,000 个整数，完全在内存范围内。  
  - 也可以把 `prefix` 合并到 `dp` 中进一步压缩到 `O(n)`，但对本题的约束不必如此复杂。

---

## 心得

- **核心技巧**：**把“满足 I/D 条件的排列计数”转化为动态规划 + 前缀和**。  
- **适用的题型**（类似思路）  
  1. **"Number of Valid Permutations for DI Sequence"**（本题）。  
  2. **LeetCode 903 – Valid Permutations for DI Sequence (same)**。  
  3. **LeetCode 282 – Expression Add Operators**（利用前缀和或 DP 把组合计数化简）。  
- **一句话总结解题钥匙**：  
  *“把每一步只关心最后一个数字的可能性，用前缀和把所有合法前缀一次性加起来，就能在 O(n²) 里算出所有合法排列。”*

---

## 反思

- **第一反应**：直接想枚举全部排列，想把所有可能的序列都写出来检查。  
- **最容易踩的坑**  
  1. **下标对应错误**：`dp` 的行号是已经放了多少个数，而字符 `s` 的下标比它少 1，需要注意 `s[i-2]` 的位置。  
  2. **模运算负数**：在递减转移时做 `total - prefix`，可能出现负数，需要加上 `MOD` 再取模。  
  3. **前缀和边界**：`j == 0` 时没有 “更小的” 前缀，必须单独处理为 0（或直接使用 `total`）。  
- **下次遇到同类题**，第一步应该先**思考状态：‘到目前为止的合法序列最后一个数字是多少’**，再寻找能够用**累计和**一次性合并转移的方式。这样就能迅速从暴力枚举跳到 O(n²) 的 DP 解。