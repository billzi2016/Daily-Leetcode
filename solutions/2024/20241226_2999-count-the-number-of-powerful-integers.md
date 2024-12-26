# #2999. **统计强整数的个数** / Count the Number of Powerful Integers

> 难度：困难 · 标签：Math、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-powerful-integers/)

---

## 题目（英文原版）

**Description**

You are given three integers start, finish, and limit. You are also given a 0-indexed string s representing a positive integer.
A positive integer x is called powerful if it ends with s (in other words, s is a suffix of x) and each digit in x is at most limit.
Return the total number of powerful integers in the range [start..finish].
A string x is a suffix of a string y if and only if x is a substring of y that starts from some index (including 0) in y and extends to the index y.length - 1. For example, 25 is a suffix of 5125 whereas 512 is not.

**Examples**

**Example 1:**

```
Input: start = 1, finish = 6000, limit = 4, s = "124"
Output: 5
Explanation: The powerful integers in the range [1..6000] are 124, 1124, 2124, 3124, and, 4124. All these integers have each digit <= 4, and "124" as a suffix. Note that 5124 is not a powerful integer because the first digit is 5 which is greater than 4.
It can be shown that there are only 5 powerful integers in this range.
```

**Example 2:**

```
Input: start = 15, finish = 215, limit = 6, s = "10"
Output: 2
Explanation: The powerful integers in the range [15..215] are 110 and 210. All these integers have each digit <= 6, and "10" as a suffix.
It can be shown that there are only 2 powerful integers in this range.
```

**Example 3:**

```
Input: start = 1000, finish = 2000, limit = 4, s = "3000"
Output: 0
Explanation: All integers in the range [1000..2000] are smaller than 3000, hence "3000" cannot be a suffix of any integer in this range.
```

**Constraints**

- 1 <= start <= finish <= 1015
- 1 <= limit <= 9
- 1 <= s.length <= floor(log10(finish)) + 1
- s only consists of numeric digits which are at most limit.
- s does not have leading zeros.

---

## 题目（中文翻译）

给定三个整数 `start`、`finish` 和 `limit`，以及一个 0 索引的字符串 `s`，它表示一个正整数（positive integer）。  
如果一个正整数 `x` 满足以下两个条件，则称其为**强整数（powerful integer）**：

1. `x` 以 `s` 结尾（即 `s` 是 `x` 的后缀（suffix））。  
2. `x` 的每一位数字都不大于 `limit`。

返回区间 `[start..finish]` 内所有强整数的数量。

**后缀（suffix）**的定义：字符串 `x` 是字符串 `y` 的后缀，当且仅当 `x` 是 `y` 的一个子串，且该子串从某个索引（包括 0）开始一直延伸到索引 `y.length - 1`。例如，`25` 是 `5125` 的后缀，而 `512` 不是。

---

#### 示例

**示例 1**

```
Input: start = 1, finish = 6000, limit = 4, s = "124"
Output: 5
Explanation: 区间 [1..6000] 中的强整数为 124、1124、2124、3124 和 4124。它们的每一位数字都 ≤ 4，并且以 "124" 为后缀。注意 5124 不是强整数，因为第一位数字 5 大于 4。
可以证明该区间内只有这 5 个强整数。
```

**示例 2**

```
Input: start = 15, finish = 215, limit = 6, s = "10"
Output: 2
Explanation: 区间 [15..215] 中的强整数为 110 和 210。它们的每一位数字都 ≤ 6，并且以 "10" 为后缀。
可以证明该区间内只有这 2 个强整数。
```

**示例 3**

```
Input: start = 1000, finish = 2000, limit = 4, s = "3000"
Output: 0
Explanation: 区间 [1000..2000] 内的所有整数都小于 3000，故 "3000" 不可能是任何整数的后缀。
```

---

#### 约束

- `1 <= start <= finish <= 10^15`
- `1 <= limit <= 9`
- `1 <= s.length <= floor(log10(finish)) + 1`
- `s` 仅由不超过 `limit` 的数字字符组成
- `s` 不含前导零

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把区间 `[start .. finish]` 中的每一个整数都枚举一遍，检查它是否满足题目要求：

1. 把整数转成字符串 `t`，判断 `t` 是否以 `s` 结尾（即 `t.endswith(s)`）。  
2. 再遍历 `t` 的每一位，确认所有数字都不大于 `limit`。

如果两个条件都满足，就把计数器 `ans` 加一。

> **类比**：把 `limit` 想成一本字典，字典里只收录了 `0~limit` 这几页。我们要检查每本书（整数）里所有的页码（每一位数字）是否都在这几页里，同时书的最后几页必须正好是 `s`（后缀）。

**为什么正确**  
因为我们对区间里的每个数都做了完整的检查，只有符合定义的才会计入答案，必然得到正确的计数。

**时间/空间复杂度**  
- **时间复杂度**：设区间长度为 `N = finish - start + 1`，每个数的位数最多为 `log10(finish) + 1`（最多 16 位，因为 `finish ≤ 10^15`）。所以总的时间是 `O(N * L)`，其中 `L` 是位数。最坏情况下 `N` 可能接近 `10^15`，显然不可接受。  
  - 用大白话说，`O(N * L)` 就像让小学生把一本有 `N` 页的书每页都读 `L` 次，工作量太大了。  
- **空间复杂度**：只用了常数级的额外变量 `O(1)`，不随输入规模增长。

#### 代码（Python）

```python
def count_powerful_bruteforce(start: int, finish: int, limit: int, s: str) -> int:
    ans = 0
    for x in range(start, finish + 1):
        t = str(x)                     # 把整数转成字符串
        # 条件 1：必须以 s 为后缀
        if not t.endswith(s):
            continue
        # 条件 2：每一位数字都 ≤ limit
        ok = True
        for ch in t:
            if int(ch) > limit:        # 只要出现大于 limit 的数字就不合格
                ok = False
                break
        if ok:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N * L)`，其中 `N = finish - start + 1`，`L = number of digits of finish`（最多 16）。  
  - 意味着当 `N` 很大（如 `10^12`）时，程序会跑非常非常久。  
- **空间复杂度**：`O(1)`，只用了几个整数和字符串变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有数字**。我们需要一种只和数字的“结构”打交道，而不是逐个数字遍历的方法。这里可以使用**数位 DP（Digit DP）**——一种专门用来在 `10` 进制下统计满足某些条件的整数的技巧。

**核心想法**：  
把“在 `[1 .. X]` 中有多少个满足条件的数”写成一个函数 `cnt(X)`，然后答案就是  

```
cnt(finish) - cnt(start - 1)
```

因为 `cnt(finish)` 包含了所有 ≤ `finish` 的数，减去 ≤ `start-1` 的数，就只剩下 `[start .. finish]` 区间。

要实现 `cnt(X)`，我们从左到右（高位到低位）逐位构造数字，并用 DP 记录**当前已经构造了多少位**以及**与 X 的大小关系**：

- `pos`：已经决定了前 `pos` 位（0 表示还没有决定任何位）。  
- `tight`（也写成 `j`）：表示已经构造的前缀是否**严格小于** `X` 的对应前缀。  
  - `tight = 0` → 前缀**完全相同**，后面的位数仍然受到 `X` 的上界限制。  
  - `tight = 1` → 前缀已经**小于** `X`，后面的每一位都可以随意取 `0~limit`（因为再大也不会超过 `X`）。

**后缀要求**  
我们要求整数的最后 `len(s)` 位恰好等于 `s`。在 DP 里，这相当于在构造到倒数第 `len(s)` 位时**强制**把这几位设成 `s`，而不是随意枚举。这样可以把“后缀等于 s”直接嵌进状态转移。

**状态定义**  

```
dp[pos][tight] = 统计所有满足以下条件的数的个数
    - 已经确定了前 pos 位（从最高位开始计数，pos = 0 表示还没确定任何位）
    - 前 pos 位与 X 的关系由 tight 表示（0: 完全相同, 1: 已经小于）
```

**转移**  

1. **如果 pos 已经超过了 X 的总位数**（即全部位都已确定），检查两件事：  
   - 整数是否 **不为 0**（因为题目要求正整数）。  
   - 整数是否 **以 s 为后缀**（这一步已经在构造时保证了）。  
   若满足则返回 `1`，否则返回 `0`。  

2. **普通位**（不在后缀区域）  
   - 允许的数字集合是 `0..limit`。  
   - 对于每个候选数字 `d`：  
     - 若 `tight == 0` 且 `d > digit_X[pos]`，则该选择会让当前数 **大于 X**，不能取。  
     - 新的 `tight2` = `tight` 或者（`tight == 0` 且 `d < digit_X[pos]`），即一旦我们选了比 X 小的数字，后面就可以随意取。  

3. **后缀区域**（倒数 `len(s)` 位）  
   - 必须把这些位固定为 `s` 对应的数字 `s_digit[pos_from_right]`。  
   - 同样检查 `tight` 与 X 的对应位是否冲突（如果 `tight == 0` 且 `s_digit > digit_X[pos]`，则非法）。  
   - `tight` 的更新方式同上。

**记忆化**：因为 `pos` 最多 16，`tight` 只有 2 种，状态总数约 `32`，可以用递归加 `lru_cache`（或手写数组）进行记忆，时间非常快。

**为什么快**  
- 我们只遍历 **每一位**（最多 16 位）和 **两种 tight 状态**，每次最多尝试 `limit+1 ≤ 10` 种数字。整体复杂度是 `O(L * limit * 2)`，即常数级别，几乎瞬间完成。

#### 代码（Python）

```python
from functools import lru_cache

def count_powerful(start: int, finish: int, limit: int, s: str) -> int:
    """
    主函数：返回区间 [start, finish] 中满足条件的整数个数
    """

    # ---------- 计算 cnt(x)：[1 .. x] 中的合法数 ----------
    def cnt(x: int) -> int:
        if x <= 0:               # x 为 0 或负数时没有正整数
            return 0

        digits = list(map(int, str(x)))          # x 的每一位，从高位到低位
        n = len(digits)                          # 位数
        m = len(s)                               # s 的长度
        s_digits = list(map(int, s))             # s 的每一位，同样是高位在前

        @lru_cache(maxsize=None)
        def dp(pos: int, tight: int) -> int:
            """
            pos   : 当前正在决定第 pos 位（0 <= pos <= n）
            tight : 0 表示前缀与 x 完全相同，1 表示已经小于 x
            返回值：从 pos 开始往后填充能得到的合法整数个数
            """
            # 已经处理完所有位
            if pos == n:
                # 这里一定已经满足后缀要求，因为后缀是在递归里强制填的
                return 1  # 成功构造出一个合法数

            # 判断当前位是否属于必须匹配 s 的后缀区域
            # 后缀位的起始位置 = n - m
            if pos >= n - m:               # 进入后缀区域，需要固定为 s 对应的数字
                # 对应的 s 中的下标
                s_idx = pos - (n - m)
                d = s_digits[s_idx]        # 必须写的数字
                # 如果 tight 为 0，需要保证不超过 x 在该位的数字
                if tight == 0 and d > digits[pos]:
                    return 0               # 超出上界，非法
                # 更新 tight：只有在 tight==0 且 d < x[pos] 时才变成 1
                new_tight = tight
                if tight == 0 and d < digits[pos]:
                    new_tight = 1
                # 递归到下一位
                return dp(pos + 1, new_tight)

            # --------- 普通位：可以自由选 0~limit ----------
            total = 0
            up = digits[pos] if tight == 0 else limit   # 当前位的上限
            for d in range(0, limit + 1):
                if d > up:                # 选的数字超过了上界，不能走
                    break
                new_tight = tight
                if tight == 0 and d < digits[pos]:
                    new_tight = 1
                total += dp(pos + 1, new_tight)
            return total

        # dp(0,0) 计算所有合法数，包括 0 本身。我们要排除 0（因为题目要求正整数）。
        # 0 只有在 s = "0" 且 limit >= 0 时才会被计入，这种情况在题目约束下不会出现
        return dp(0, 0)

    # ---------- 通过前缀计数得到答案 ----------
    return cnt(finish) - cnt(start - 1)
```

#### 复杂度

- **时间复杂度**：`O(L * limit * 2)`，其中 `L = number of digits of finish`（最多 16），`limit ≤ 9`。  
  - 用大白话说，就是最多遍历 16 × 10 × 2 ≈ 320 次小循环，几乎可以忽略不计。相比暴力的 `O(N * L)`（可能是天文数字），快了好几个数量级。  
- **空间复杂度**：`O(L * 2)` 用于递归栈和记忆化表（最多 32 个状态），同样是常数级别。

---

## 心得

- **核心技巧**：**数位 DP**（Digit DP）——在十进制的每一位上做动态规划，利用“tight”状态限制不超过上界。  
- **适用的题型**  
  1. 统计满足某种位数限制的整数（如“不含数字 4”或“每位数字之和为奇数”）。  
  2. 求区间 `[L, R]` 中满足“数字出现次数不超过 k 次”等条件的数。  
  3. 本题这种“固定后缀 + 位数上界”的组合约束。  
- **一句话总结**：**把“大范围枚举”转化为“逐位构造 + 状态记忆”，让问题的规模从 `10^15` 降到个位数的 DP 状态。**

---

## 反思

- **第一反应**：直接写循环遍历所有数字，检查后缀和每位大小——这在面对 `10^15` 规模时会立刻卡死。  
- **最容易踩的坑**  
  1. **边界条件**：`cnt(start-1)` 当 `start = 1` 时要返回 0，防止负数导致错误。  
  2. **后缀长度大于整体位数**：如果 `len(s) > len(x)`，直接返回 0。代码里自然会在 DP 的 “pos >= n - m” 判断中返回 0。  
  3. **limit 为 9 时的全局上界**：要记得在非紧状态下上界是 `limit`，而不是 `9`。  
- **下次类似题目第一步**：先思考 **“能否把问题转化为‘在 [1..X] 中计数’”，再考虑使用 **数位 DP**，尤其是当题目涉及“每位数字的范围”“固定前缀/后缀”“不超过某个上限”等条件时。