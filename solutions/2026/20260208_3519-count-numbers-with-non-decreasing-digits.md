# #3519. 计数非递减数字 / Count Numbers with Non-Decreasing Digits 

> 难度：困难 · 标签：Math、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-numbers-with-non-decreasing-digits/)

---

## 题目（英文原版）

**Description**

You are given two integers, l and r, represented as strings, and an integer b. Return the count of integers in the inclusive range [l, r] whose digits are in non-decreasing order when represented in base b.
An integer is considered to have non-decreasing digits if, when read from left to right (from the most significant digit to the least significant digit), each digit is greater than or equal to the previous one.
Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: l = "23", r = "28", b = 8
Output: 3
Explanation:
```

**Example 2:**

```
Input: l = "2", r = "7", b = 2
Output: 2
Explanation:
```

**Constraints**

- 1 <= l.length <= r.length <= 100
- 2 <= b <= 10
- l and r consist only of digits.
- The value represented by l is less than or equal to the value represented by r.
- l and r do not contain leading zeros.

---

## 题目（中文翻译）

给定两个以字符串形式表示的整数 `l` 和 `r`，以及一个整数 `b`。返回在闭区间 `[l, r]` 内，数字在 `b` 进制下各位数字从左到右（即从最高位到最低位）呈非递减（non‑decreasing）顺序的整数个数。  

如果从左到右读取时，每一位数字都 **大于或等于** 前一位，则该整数的数字被视为非递减。  

由于答案可能非常大，返回结果对 `10^9 + 7` 取模。

**示例 1**  
Input: `l = "23", r = "28", b = 8`  
Output: `3`  
Explanation: 在十进制区间 `[23, 28]` 内的数字分别为  
`23 → 27₈`、`24 → 30₈`、`25 → 31₈`、`26 → 32₈`、`27 → 33₈`、`28 → 34₈`。  
其中 `27₈ (2 ≤ 7)`、`33₈ (3 ≤ 3)`、`34₈ (3 ≤ 4)` 的位序满足非递减，共计 3 个。

**示例 2**  
Input: `l = "2", r = "7", b = 2`  
Output: `2`  
Explanation: 区间 `[2, 7]` 的二进制表示为  
`2 → 10₂`、`3 → 11₂`、`4 → 100₂`、`5 → 101₂`、`6 → 110₂`、`7 → 111₂`。  
只有 `11₂` 和 `111₂` 的位序是非递减的，所以答案为 2。

**约束条件**  
- `1 <= l.length <= r.length <= 100`  
- `2 <= b <= 10`  
- `l` 和 `r` 仅由数字字符组成。  
- `l` 表示的数值不大于 `r` 表示的数值。  
- `l` 与 `r` 不含前导零。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把区间 `[l, r]` 里所有的整数都枚举出来，逐个检查它们的每一位数字是否满足“非递减”。  
具体步骤：

1. 把字符串 `l`、`r` 转成十进制整数（或者直接用 Python 的大整数），得到 `L`、`R`。  
2. 从 `L` 循环到 `R`（`for x in range(L, R+1)`），对每个 `x`：  
   - 把 `x` 用 **base‑b** 表示成一串数字（相当于把十进制的 `123` 写成二进制、八进制等）。  
   - 从左到右比较相邻的两位，如果后面的位小于前面的位，就说明这不是非递减数，直接抛弃。  
   - 否则计数器 `ans += 1`。  

> **类比**：把哈希表比作一本字典，key 是单词，value 是页码；这里的“把数字转成 base‑b 表示”就像把十进制的“电话号码”翻译成不同语言的读法。

**为什么正确**：因为我们把区间里的每一个数都检查了一遍，只要满足条件就计数，显然不会漏掉也不会多计。

**复杂度**：  
- **时间**：假设区间长度为 `N = R - L + 1`，每个数最多有 `len = max(len(l), len(r)) ≤ 100` 位，检查一次需要 O(len) 的比较，所以总时间是 `O(N * len)`。如果 `N` 很大（比如 `10^100`），这根本不可行。  
- **空间**：只用了常数级别的额外变量，`O(1)`。

> **大白话**：`O(N * len)` 就像我们要在一条很长的路上走 `N` 步，每一步都要检查手里的 100 张卡片，步数太多根本走不完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def to_base_b(num: int, b: int) -> list[int]:
    """把十进制整数转成 base‑b，返回从高位到低位的列表"""
    if num == 0:
        return [0]
    digits = []
    while num:
        digits.append(num % b)      # 取最低位
        num //= b
    return digits[::-1]             # 反转得到高位在前

def is_nondecreasing(digits: list[int]) -> bool:
    """检查列表中的数字是否非递减"""
    for i in range(1, len(digits)):
        if digits[i] < digits[i-1]:
            return False
    return True

def brute_count(l: str, r: str, b: int) -> int:
    L = int(l)          # Python 的大整数可以直接转
    R = int(r)
    ans = 0
    for x in range(L, R + 1):
        d = to_base_b(x, b)
        if is_nondecreasing(d):
            ans += 1
    return ans % MOD
```

> **注意**：上面的实现只能在 `r - l` 很小的测试里跑通，实际提交会 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O(N * len)`，其中 `N = R-L+1`，`len` 为数字的位数。  
  - 含义：如果区间有 1 000 000 个数，每个数检查 100 位，则大约要做 1 亿 次比较，已经很慢了。  
- **空间复杂度**：`O(1)`，只用了几个整数和列表（列表长度不超过 100，算作常数）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **逐个枚举** 区间里的每个数。实际上我们只关心“有多少满足条件”，不需要把它们一个个列出来。  
这类 “计数 + 位约束” 的问题，**数字动态规划（Digit DP）** 是常用且高效的技巧。

**核心思路**：

1. **把问题拆成“前缀计数”**：先求 `f(X)` = ≤ `X` 的非递减数的个数。  
   那么答案 = `f(r) - f(l-1)`（记得模运算）。  
2. **状态定义**  
   - `pos`：当前处理的是第几位（从最高位往低位走）。  
   - `prev`：前一位选了多少（因为后面的位必须 ≥ 前一位），范围 `[0, b-1]`。  
   - `tight`：前缀是否已经和上界 `X` 完全相同。`True` 表示后面的位不能超过 `X` 对应位的数字；`False` 表示已经小于上界，后面可以随意选。  
   - `lead`（leading zero）：是否仍在前导零阶段。前导零不算作真正的数字，它们不影响非递减约束（因为没有前一个真实位），所以在前导零阶段我们可以把 `prev` 当作 `0` 来处理。  

   状态记作 `dp[pos][prev][tight][lead]`，返回从 `pos` 开始往后可以构造的合法数的个数。  

3. **转移**  
   - 当前位可选的最大数字 `up = digit[pos]`（如果 `tight` 为真）否则 `up = b-1`。  
   - 遍历 `d` 从 `0` 到 `up`：  
     - 若仍在前导零且 `d == 0`，则下一个状态仍是前导零，`prev` 保持为 `0`（不产生约束）。  
     - 否则必须满足 `d >= prev`（非递减），否则跳过。  
     - 新的 `tight` 为 `tight and (d == up)`，因为只有当我们选了上界的最大值才仍然受限。  
   - 把子问题的返回值累加到当前状态。  

4. **边界**  
   - 当 `pos == len(digits)`（已经处理完所有位），如果 **已经离开前导零**（即至少选了一个非零位），说明得到了一合法数，返回 `1`；否则返回 `0`（全是零的情况在本题不算，因为 `l`、`r` 没有前导零且 `l ≥ 1`）。  

5. **实现细节**  
   - 使用 `@lru_cache(None)` 进行记忆化，避免重复计算。  
   - 为了计算 `f(l-1)`，需要实现 **大数减一**（在 base‑b 下）。我们可以把 `l` 当作十进制字符串，先转成整数再减一，再转回字符串；因为长度最多 100，Python 大整数足够。  

6. **复杂度分析**  
   - `pos` 最多 100，`prev` 只有 `b ≤ 10` 种可能，`tight`、`lead` 各 2 种。状态总数 `≈ 100 * 10 * 2 * 2 = 4000`，每个状态遍历最多 `b`（≤10）个数字，整体时间 `O(len * b²)`，实际约几千次操作，几乎瞬间完成。  
   - 只用递归栈和缓存，空间 `O(len * b * 2 * 2)`，同样只有几千个整数，属于 `O(len * b)`。

> **类比**：把数字 DP 想成“在走迷宫”。每走一步（处理一位），我们只能往**不下降**的方向前进（因为必须非递减），而且有时会被墙（`tight` 限制）挡住，只有走到终点（处理完所有位）才算一次合法的路径。

#### 代码（Python）

```python
from functools import lru_cache

MOD = 10**9 + 7

def to_digits(num_str: str, b: int) -> list[int]:
    """把十进制字符串表示的数转成 base‑b 的高位在前的列表"""
    # 先把十进制字符串转成整数（Python 支持任意长度）
    n = int(num_str)
    if n == 0:
        return [0]
    digs = []
    while n:
        digs.append(n % b)
        n //= b
    return digs[::-1]                # 高位在前

def count_upto(num_str: str, b: int) -> int:
    """
    返回 ≤ num_str（十进制表示）且在 base‑b 下数字非递减的整数个数（模 MOD）。
    """
    digits = to_digits(num_str, b)   # 上界的每一位
    m = len(digits)

    @lru_cache(None)
    def dfs(pos: int, prev: int, tight: bool, lead: bool) -> int:
        """
        pos   : 当前处理到的位（0 ~ m），左侧已经确定
        prev  : 前一位真实数字（0~b-1），在 lead 为 True 时视作 0
        tight : 前缀是否仍等于上界
        lead  : 是否仍在前导零阶段
        返回从 pos 开始可以构造的合法数的个数
        """
        if pos == m:                     # 走到最右侧，结束
            return 0 if lead else 1    # 全是前导零算无效，其余算 1
        up = digits[pos] if tight else b - 1   # 本位最大可选值
        total = 0
        for d in range(up + 1):         # 枚举本位可以取的数字
            next_lead = lead and d == 0
            # 前导零阶段不需要比较非递减约束
            if not next_lead:
                if d < prev:            # 违反非递减，直接跳过
                    continue
            # 新的 tight 只有在当前仍受限且选了上界的最大值时才为 True
            next_tight = tight and (d == up)
            # 下一个 prev：如果仍在前导零，保持 0；否则使用当前真实数字 d
            next_prev = 0 if next_lead else d
            total += dfs(pos + 1, next_prev, next_tight, next_lead)
        return total % MOD

    return dfs(0, 0, True, True)

def subtract_one(num_str: str) -> str:
    """十进制大整数减一，返回不带前导零的字符串"""
    n = int(num_str)
    return str(n - 1)

def count_non_decreasing(l: str, r: str, b: int) -> int:
    """
    主函数：区间 [l, r]（十进制字符串）在 base‑b 下数字非递减的个数
    """
    cnt_r = count_upto(r, b)
    # 计算 f(l-1)；如果 l == "0"（本题不会出现），直接视为 0
    l_minus = subtract_one(l)
    cnt_l = count_upto(l_minus, b) if int(l) > 0 else 0
    return (cnt_r - cnt_l) % MOD
```

> **运行示例**

```python
print(count_non_decreasing("23", "28", 8))   # 3
print(count_non_decreasing("2", "7", 2))     # 2
```

#### 复杂度  

- **时间复杂度**：`O(len * b²)`，这里 `len ≤ 100`，`b ≤ 10`，大约几千次循环，几乎是常数级别。  
  - 含义：不管区间有多大（甚至 `10^100`），我们只看最高位有多少位以及基数有多大，计算量始终很小。  
- **空间复杂度**：`O(len * b * 2 * 2)`，即 `O(len * b)`，只用来保存递归缓存和调用栈。  

与暴力解相比，时间从“可能需要遍历 10⁹⁹⁹… 个数”降到了“几千次简单的加法”，效率提升天壤之别。

---

## 心得

- **核心技巧**：**数字动态规划（Digit DP）**——把“在某个范围内计数且满足位约束”的问题转化为对每一位的递归计数。  
- **适用题型**  
  1. “统计区间内满足某种位数性质的数”，如 **计数无重复数字的整数**、**计数各位和为特定值的整数**。  
  2. “求区间内满足前缀/后缀限制的数”，例如 **求区间内回文数的个数**。  
  3. **计数满足递增/递减/非递减/非递增的数字**（本题就是非递减）。  
- **一句话总结解题钥匙**：**把“大范围枚举”换成“逐位递归”，用前缀是否已达上界来控制搜索范围**。

---

## 反思

- **第一反应**：看到“区间”和“数字属性”，本能想到直接遍历每个数检查——这正是暴力解的思路。  
- **最容易踩的坑**  
  - **前导零**：在 DP 中需要单独处理，否则会把 `00123` 误认为不合法。  
  - **tight 状态**：忘记在取不到上界时把 `tight` 设为 `False`，会导致后面的位仍被错误限制。  
  - **模运算**：递归返回值累计时要及时 `% MOD`，防止整数溢出（虽然 Python 自动大整数，但仍要符合题目要求）。  
  - **计算 `l-1`**：直接对字符串做减法容易出错，使用 Python 大整数是最安全的做法。  
- **下次遇到同类题**：第一步立刻把问题转化为 “**求 ≤ X 的满足条件的数**”，然后设计 **Digit DP** 的四个维度（位置、前一位、是否受限、是否前导零），再用 `f(r) - f(l-1)` 得到答案。这样可以避免任何暴力枚举的陷阱。