# #2719. 整数计数 / Count of Integers

> 难度：困难 · 标签：Math、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-of-integers/)

---

## 题目（英文原版）

**Description**

You are given two numeric strings num1 and num2 and two integers max_sum and min_sum. We denote an integer x to be good if:
Return the number of good integers. Since the answer may be large, return it modulo 109 + 7.
Note that digit_sum(x) denotes the sum of the digits of x.

**Examples**

**Example 1:**

```
Input: num1 = "1", num2 = "12", min_sum = 1, max_sum = 8
Output: 11
Explanation: There are 11 integers whose sum of digits lies between 1 and 8 are 1,2,3,4,5,6,7,8,10,11, and 12. Thus, we return 11.
```

**Example 2:**

```
Input: num1 = "1", num2 = "5", min_sum = 1, max_sum = 5
Output: 5
Explanation: The 5 integers whose sum of digits lies between 1 and 5 are 1,2,3,4, and 5. Thus, we return 5.
```

**Constraints**

- 1 <= num1 <= num2 <= 1022
- 1 <= min_sum <= max_sum <= 400

---

## 题目（中文翻译）

给定两个数字字符串 `num1` 和 `num2`，以及两个整数 `max_sum` 和 `min_sum`。我们称整数 `x` 为**好整数**，如果满足以下条件：

- `num1` ≤ `x` ≤ `num2`（这里的比较是按数值大小进行的）；
- `min_sum` ≤ `digit_sum(x)` ≤ `max_sum`，其中 `digit_sum(x)` 表示 `x` 的各位数字之和。

返回好整数的数量。由于答案可能很大，请返回结果对 `10^9 + 7` 取模后的值。

---

**示例 1**

```text
Input: num1 = "1", num2 = "12", min_sum = 1, max_sum = 8
Output: 11
Explanation: 符合条件的整数有 1,2,3,4,5,6,7,8,10,11,12，共 11 个。因此返回 11。
```

**示例 2**

```text
Input: num1 = "1", num2 = "5", min_sum = 1, max_sum = 5
Output: 5
Explanation: 符合条件的整数有 1,2,3,4,5，共 5 个。因此返回 5。
```

**约束条件**

- `1 ≤ num1 ≤ num2 ≤ 10^22`
- `1 ≤ min_sum ≤ max_sum ≤ 400`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把区间 `[num1, num2]` 里所有整数都列出来，逐个求它们的**数字和**（把每一位相加），然后判断这个和是否落在 `[min_sum, max_sum]` 之间，满足的就计数。

- **数据结构**：我们只需要一个普通的 `int` 变量来累计答案。  
  - 求数字和时可以把整数转成字符串，再把每个字符 `'0'~'9'` 减去 `'0'` 得到对应的数字，就像我们查字典时把词（字符）对应到页码（数字）一样简单。

- **正确性**：因为我们遍历了区间里的**每一个**整数，且对每个整数都做了“数字和是否在合法区间”这一唯一判断，所以计数的结果必然等于题目要求的答案。

- **复杂度分析**  
  - 假设区间长度为 `N = int(num2) - int(num1) + 1`，每个整数的位数最多 `L`（`L ≤ 22`），求数字和的时间是 `O(L)`。  
  - 整体时间就是 `O(N * L)`，在最坏情况下 `N` 可能是 `10^22`（因为 `num2` 最多 22 位），显然不可接受。  
  - 空间上只用了常数个变量，`O(1)`。

> **大白话解释**：`O(N * L)` 可以想象成“有 `N` 堆东西，每堆要翻 `L` 页才能找到答案”。如果 `N` 超过一万亿，这种“翻页”方式根本做不完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def digit_sum(x: int) -> int:
    """返回整数 x 的各位数字之和"""
    s = 0
    while x:
        s += x % 10      # 取最低位
        x //= 10         # 去掉最低位
    return s

def brute_force(num1: str, num2: str, min_sum: int, max_sum: int) -> int:
    lo = int(num1)          # 把字符串转换成整数
    hi = int(num2)
    ans = 0
    for x in range(lo, hi + 1):
        if min_sum <= digit_sum(x) <= max_sum:
            ans += 1
    return ans % MOD
```

#### 复杂度

- **时间复杂度**：`O(N * L)`，`N` 为区间大小，`L` 为数字的位数。  
  - 当 `N` 很大（比如 `10^12`）时，时间会爆炸，根本跑不完。
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐个枚举**区间内的每个整数。我们需要一种方法，**一次性**算出 “所有 ≤ 某个上界的整数” 中满足数字和条件的个数，然后用前缀差得到区间答案。

这正是**数位 DP（Digit DP）**的典型应用场景。  
数位 DP 的核心思想是：从高位到低位逐位构造数字，同时记录“已经形成的数字和”。因为每一位只会取 `0~9`，所以状态空间是有限的，可以用记忆化递归（或 DP 表）枚举。

**步骤概览**

1. **把问题转化为前缀计数**  
   定义 `f(n, L, R)` 为 **从 0 到 n（含 n）** 的所有整数中，数字和落在 `[L, R]` 的个数。  
   那么答案 = `f(num2, min_sum, max_sum) - f(num1-1, min_sum, max_sum)`（注意取模）。

2. **实现 `f`**  
   - 把上界 `n` 写成字符串 `s`，长度记为 `len(s)`。  
   - 使用递归 `dfs(pos, cur_sum, tight)`：
     - `pos`：当前正在处理的位（从左到右，`0` 表示最高位）。  
     - `cur_sum`：到目前为止已经累加的数字和。  
     - `tight`：是否仍然受上界限制。`tight = True` 表示前面的位已经和上界完全相同，当前位的取值不能超过 `s[pos]`；否则可以随意取 `0~9`。  
   - 递归的**终止条件**是 `pos == len(s)`，此时已经构造完所有位，检查 `cur_sum` 是否在 `[L, R]` 区间，返回 `1` 或 `0`。

3. **记忆化**  
   - 由于 `pos ≤ 22`，`cur_sum ≤ 400`，`tight` 只有两种取值，整个状态空间只有 `22 * 401 * 2 ≈ 17k`，完全可以用字典或二维数组缓存，避免重复计算。

4. **取模**  
   - 题目要求答案模 `10^9+7`，在每次加法时都取模即可。

> **为什么比暴力快**  
> 暴力是对每个具体的整数做一次 “求和” 操作，而数位 DP 把相同前缀的数字合并在一起，只遍历 **状态** 而不是 **数**。状态的数量是 **位数 × 目标和上限**，与区间大小无关，所以即使 `num2` 有 22 位、区间宽度是 `10^22`，我们仍然只需要几万次计算。

#### 代码（Python）

```python
MOD = 10**9 + 7

def count_upto(num: str, min_sum: int, max_sum: int) -> int:
    """
    统计 0~num（含）之间，数字和在 [min_sum, max_sum] 区间的整数个数
    """
    digits = list(map(int, num))          # 把每位数字拆成列表，方便索引
    n = len(digits)

    # memo[(pos, cur_sum, tight)] = 计数
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(pos: int, cur_sum: int, tight: bool) -> int:
        """
        pos    : 当前处理的位（0 为最高位）
        cur_sum: 已经累计的数字和
        tight : 前缀是否仍然等于上界 num 的前缀
        """
        # 剪枝：如果已经超过 max_sum，就不可能满足条件，直接返回 0
        if cur_sum > max_sum:
            return 0

        # 到达最右侧，检查累计的数字和是否在合法区间
        if pos == n:
            return 1 if min_sum <= cur_sum <= max_sum else 0

        # 本位能够取的最大数字
        limit = digits[pos] if tight else 9

        total = 0
        for d in range(limit + 1):          # 枚举本位可以放的数字
            next_tight = tight and (d == limit)   # 仍然受限当且仅当当前取到上界
            total += dfs(pos + 1, cur_sum + d, next_tight)
            if total >= MOD:               # 防止中间值溢出，及时取模
                total -= MOD
        return total

    return dfs(0, 0, True) % MOD


def count_range(num1: str, num2: str, min_sum: int, max_sum: int) -> int:
    """
    主函数：返回区间 [num1, num2] 中，数字和在 [min_sum, max_sum] 的整数个数
    """
    # 计算 0~num2 的前缀计数
    cnt2 = count_upto(num2, min_sum, max_sum)

    # 计算 0~(num1-1) 的前缀计数
    # 为了得到 num1-1，需要把 num1 当作大整数减 1
    # 这里用 Python 的大整数直接处理
    num1_minus_one = str(int(num1) - 1) if int(num1) > 0 else "0"
    cnt1 = count_upto(num1_minus_one, min_sum, max_sum)

    ans = (cnt2 - cnt1) % MOD
    return ans
```

> **代码说明**  
> - `dfs` 用 `@lru_cache` 自动记忆化，等价于手写的 `dp[pos][cur_sum][tight]` 表。  
> - `limit` 表示当前位能取的最大值：如果前缀已经严格小于上界，就可以随意取 `0~9`（`tight=False`），否则只能取到上界对应的那一位数字。  
> - 为了防止递归深度过大，Python 默认递归深度足够（`22`），无需额外处理。  
> - `count_range` 里先算 `num2`，再算 `num1-1`，两者相减即得区间答案，最后再取模。

#### 复杂度

- **时间复杂度**：`O(L * max_sum * 10)`  
  - `L` 为数字位数（最多 22），`max_sum ≤ 400`，每个状态最多枚举 10 种下一位的取值。  
  - 实际运行次数约为 `22 * 401 * 10 ≈ 88,220`，非常快。  
  - 与区间宽度 `num2 - num1` 完全无关，明显优于暴力的 `O(N * L)`。

- **空间复杂度**：`O(L * max_sum * 2)`（记忆化表的大小）  
  - 大约 `22 * 401 * 2 ≈ 17,684` 个整数，几 KB 级别的内存。

---

## 心得

- **核心技巧**：**数位 DP（Digit DP）**——把“在某个区间内计数”转化为“在上界以内计数”，再利用位置信息和数字和的累计来做动态规划。  
- **适用的题型**  
  1. “统计区间 `[L, R]` 中满足某种位数属性的整数”，例如 **“计数数字和为 K 的整数”**、**“计数不含连续相同数字的整数”**。  
  2. “求区间内满足某种数位约束的整数个数”，如 **“数字中出现的 4 和 7 的个数相等”**、**“数的每位都不小于前一位（递增数）”**。  
- **一句话总结解题钥匙**：  
  > 把“大范围枚举”压缩成“**状态枚举**”，用 DP 记录“已经走到第几位、累计了多少、是否仍受上界约束”，一次遍历即可得到全部答案。

---

## 反思

- **第一反应**：看到“区间、数字和、模 1e9+7”立刻想到“遍历所有数”。但随后意识到区间上界可能非常大（22 位），直接枚举根本不可行。  
- **最容易踩的坑**  
  1. **边界处理**：`num1` 为最小值时，需要计算 `num1-1`，如果直接 `int(num1)-1` 产生负数会导致错误，需要特殊处理（如上代码的 `if int(num1) > 0 else "0"`）。  
  2. **状态剪枝**：如果不在递归入口判断 `cur_sum > max_sum`，会产生大量无效状态，导致运行时间增加。  
  3. **取模**：递归返回值在累计时必须及时 `% MOD`，否则中间结果可能超过 Python 整数的默认范围（虽然 Python 整数不溢出，但会拖慢性能）。  
- **下次遇到同类题的第一步**：  
  > 先判断是否可以把 “区间计数” 转化为 “前缀计数” 的差，然后思考 **“每一位的取值如何受上界限制”**，这几乎总能指向数位 DP 的解法。