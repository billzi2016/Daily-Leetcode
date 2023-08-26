# #2376. 统计特殊整数 / Count Special Integers

> 难度：困难 · 标签：Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-special-integers/)

---

## 题目（英文原版）

**Description**

We call a positive integer special if all of its digits are distinct.
Given a positive integer n, return the number of special integers that belong to the interval [1, n].

**Examples**

**Example 1:**

```
Input: n = 20
Output: 19
Explanation: All the integers from 1 to 20, except 11, are special. Thus, there are 19 special integers.
```

**Example 2:**

```
Input: n = 5
Output: 5
Explanation: All the integers from 1 to 5 are special.
```

**Example 3:**

```
Input: n = 135
Output: 110
Explanation: There are 110 integers from 1 to 135 that are special.
Some of the integers that are not special are: 22, 114, and 131.
```

**Constraints**

- 1 <= n <= 2 * 109

---

## 题目（中文翻译）

我们称一个**正整数（positive integer）**为**特殊整数（special integer）**，如果它的所有**数字（digit）**互不相同。  
给定一个正整数 `n`，返回区间 `[1, n]`（**闭区间**）内的特殊整数的数量。

**示例 1**  
**输入**: `n = 20`  
**输出**: `19`  
**解释**: 1 到 20 中，除了 `11` 之外的所有整数都是特殊的，因此共有 19 个特殊整数。

**示例 2**  
**输入**: `n = 5`  
**输出**: `5`  
**解释**: 1 到 5 的所有整数都是特殊的。

**示例 3**  
**输入**: `n = 135`  
**输出**: `110`  
**解释**: 在 1 到 135 之间共有 110 个特殊整数。未满足条件的整数示例包括 `22`、`114`、`131`。

**约束条件**  
- `1 <= n <= 2 * 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把 1 … n 每个数都枚举出来，逐个判断它是否满足“所有数字互不相同”。**  
判断一个整数的各位是否唯一可以用 **集合（set）** 来实现：把每个数字的每一位放进集合，若出现重复，集合的大小就会小于位数。

- **集合**好比一本字典，里面只能出现不重复的词条。我们把每一位数字当作词条，放进去后，如果有相同的词条（相同的数字），字典的容量就会变小，说明出现了重复。
- 只要遍历完所有位，集合的大小等于位数，就说明这是一条“特殊整数”。

这个方法**一定正确**，因为我们把所有可能的整数都检查了一遍，凡是符合条件的自然会被计数。

#### 代码（Python）

```python
def countSpecialNumbers_bruteforce(n: int) -> int:
    """暴力枚举 1~n，逐个检查是否各位数字互不相同"""
    ans = 0
    for x in range(1, n + 1):
        seen = set()          # 用 set 来记录出现过的数字，相当于“字典”
        y = x
        ok = True
        while y:
            d = y % 10        # 取最右边一位
            if d in seen:     # 已经出现过，说明有重复
                ok = False
                break
            seen.add(d)       # 把这位数字加入集合
            y //= 10          # 去掉已经检查过的最右位
        if ok:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * log₁₀ n)`  
  对每个数我们要遍历它的所有位数，位数大约是 `log₁₀ n`（比如 n=10⁹，位数只有 10 位），所以整体是 `n` 乘以常数级别的位数。用大白话说，就是“和 n 成正比”，如果 n 很大（题目上限 2·10⁹），这根本跑不完。
- **空间复杂度**：`O(1)`（不计答案本身）  
  只用了常数个变量和一个最多装 10 个元素的集合。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“遍历所有 1…n 的整数”**，当 n 达到 20 亿时根本不可能逐个检查。  
我们需要 **在不枚举每个具体数字的前提下，直接算出符合条件的数量**。这类“在数的范围内计数”问题常用 **数字动态规划（Digit DP）**。

**核心概念**  

1. **把整数看成一串数字**  
   例如 n = 135 可以写成 `[1, 3, 5]`（从高位到低位）。我们从最高位开始往低位“构造”所有可能的数。

2. **状态 (pos, mask, tight, leadZero)**  
   - `pos`：当前正在处理第几位（从左到右），范围 `0 … m`（`m` 为 n 的位数）。  
   - `mask`：一个 10 位的二进制掩码，记录已经使用了哪些数字。第 `d` 位为 1 表示数字 `d` 已经出现过。掩码就像一张“已用数字表”，类似于我们平时在纸上画的“勾选框”。  
   - `tight`（是否受限）：如果前面已经选的数字严格小于 n 对应的前缀，那么后面的位可以随意选 0‑9；否则（前缀相等）本位的取值上限只能是 n 在该位的数字。  
   - `leadZero`（前导零）：在最高位之前我们可以选 0 形成“前导零”，这些 0 不算作实际位，也不算进 `mask`，因为题目只统计正整数。

3. **转移**  
   - 对当前位 `pos`，遍历所有合法的数字 `dig`（0‑9），但要满足：
     - `dig <= limit`，其中 `limit = n[pos]` 当 `tight` 为 True，否则 `limit = 9`。
     - 若 `leadZero` 为 True 且 `dig == 0`，我们仍保持 `leadZero=True`，且不更新 `mask`（仍然是“没有真正的数字出现”）。
     - 否则必须保证 `dig` 没在 `mask` 中出现（`mask & (1 << dig) == 0`），否则会产生重复位，直接跳过。
   - 递归进入下一位，更新 `tight` 为 `tight and dig == limit`，`leadZero` 为 `leadZero and dig == 0`，以及 `mask`（若不是前导零则加入 `dig`）。

4. **结束条件**  
   当 `pos == m`（已经处理完所有位），只要 **不是全是前导零**（即已经选到至少一位非零），我们就算作一个合法的特殊整数，返回 1；否则返回 0。

5. **记忆化**  
   同一 `(pos, mask, tight, leadZero)` 组合会被重复计算，使用 `lru_cache`（或字典）记住结果，避免指数级递归。

**为什么快？**  
- `pos` 最多 10（因为 n ≤ 2·10⁹，最多 10 位）。  
- `mask` 只有 `2⁰ … 2¹⁰`（共 1024）种可能。  
- `tight`、`leadZero` 只有 2 种取值。  
- 所有状态数目约为 `10 * 1024 * 2 * 2 ≈ 40,960`，每个状态的转移最多遍历 10 个数字，整体只有几万次操作，时间几乎是常数级。

#### 代码（Python）

```python
from functools import lru_cache

def countSpecialNumbers(n: int) -> int:
    """
    使用数字 DP 统计区间 [1, n] 内所有各位数字互不相同的整数个数。
    """
    digits = list(map(int, str(n)))          # 将 n 拆成高位到低位的列表，例如 135 -> [1,3,5]
    m = len(digits)                          # 位数

    @lru_cache(maxsize=None)
    def dfs(pos: int, mask: int, tight: bool, leadZero: bool) -> int:
        """
        返回从当前 pos 开始往后可以构造的合法数的个数。
        pos   : 正在处理第 pos 位（0-index），左边已经确定好。
        mask  : 10 位二进制，记录已经使用过的数字。mask 的第 d 位为 1 表示数字 d 已出现。
        tight : 前缀是否已经和 n 的前缀完全相同，若相同则本位的最大取值受 n 限制。
        leadZero : 之前是否全是前导零（即尚未选到任何非零数字），若是则本位选 0 仍保持前导零状态。
        """
        # 已经处理完所有位
        if pos == m:
            # 至少出现过一次非零数字，才算是正整数
            return 0 if leadZero else 1

        limit = digits[pos] if tight else 9     # 本位可以取的最大值
        total = 0

        for dig in range(0, limit + 1):
            next_tight = tight and (dig == limit)
            next_leadZero = leadZero and (dig == 0)

            # 仍然是前导零的话，不把 0 计入 mask
            if next_leadZero:
                total += dfs(pos + 1, mask, next_tight, True)
                continue

            # 检查是否出现重复数字
            if (mask >> dig) & 1:   # 该数字已经使用过
                continue

            # 把当前数字加入 mask
            new_mask = mask | (1 << dig)
            total += dfs(pos + 1, new_mask, next_tight, False)

        return total

    # 从最高位开始搜索，初始 mask 为 0，tight 为 True（必须不超过 n），leadZero 为 True
    return dfs(0, 0, True, True)
```

#### 复杂度

- **时间复杂度**：`O(m * 2^10 * 10)` ≈ `O(10 * 1024 * 10) ≈ 1e5`  
  用大白话说，就是“状态总数只有几万，算起来几乎是瞬间完成”。相较于暴力的 `O(n log n)`，提升巨大。
- **空间复杂度**：`O(m * 2^10)` ≈ `O(10 * 1024) ≈ 1e4`  
  主要是递归栈和记忆化表占用的空间，仍然是常数级别。

---

## 心得

- **核心技巧**：**数字动态规划（Digit DP） + 位掩码（bitmask）**。  
  这两者一起可以在不枚举所有具体整数的情况下，统计满足“各位互不相同”等位数约束的数量。

- **适用题型**（类似思路）  
  1. **统计区间内不含特定数字的数**（如不含 4 的整数）。  
  2. **统计区间内数字和满足某个范围的数**（如各位数字之和 ≤ 20）。  
  3. **统计区间内满足递增/递减位序的数**（如每位数字严格递增）。

- **一句话总结解题钥匙**：  
  “把大区间拆成‘逐位构造’，用掩码记住已经使用的数字，利用 DP 把重复子问题一次算清”。  

---

## 反思

- **第一反应**：直接想到遍历 1…n，检查每个数的位是否重复——这在面试里是最自然的暴力思路，但很快会因为 n 的上限太大而卡住。

- **最容易踩的坑**  
  1. **前导零的处理**：忘记把前导零排除，会把 `0` 当作合法数计入答案。  
  2. **位掩码的更新**：在前导零阶段错误地把 `0` 加入 mask，会导致后续合法的 `0` 被误判为重复。  
  3. **tight 状态的转移**：在 `tight=False` 时仍错误地使用 n 的当前位作为上限，会漏算一些合法数。

- **下次遇到同类题的第一步**：  
  “先把目标数字拆成数组（高位到低位），思考‘逐位决定每一位的取值’是否会产生重复子问题；如果会，就立刻考虑使用记忆化的 Digit DP”。这样可以迅速从暴力跳到高效的状态转移框架。