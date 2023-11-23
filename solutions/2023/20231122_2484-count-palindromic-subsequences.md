# #2484. 计数回文子序列 / Count Palindromic Subsequences

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-palindromic-subsequences/)

---

## 题目（英文原版）

**Description**

Given a string of digits s, return the number of palindromic subsequences of s having length 5. Since the answer may be very large, return it modulo 109 + 7.
Note:

**Examples**

**Example 1:**

```
Input: s = "103301"
Output: 2
Explanation: 
There are 6 possible subsequences of length 5: "10330","10331","10301","10301","13301","03301". 
Two of them (both equal to "10301") are palindromic.
```

**Example 2:**

```
Input: s = "0000000"
Output: 21
Explanation: All 21 subsequences are "00000", which is palindromic.
```

**Example 3:**

```
Input: s = "9999900000"
Output: 2
Explanation: The only two palindromic subsequences are "99999" and "00000".
```

**Constraints**

- 1 <= s.length <= 104
- s consists of digits.

---

## 题目（中文翻译）

给定一个只包含数字的字符串 `s`，返回 `s` 中长度为 5 的回文子序列（palindromic subsequence）的数量。由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。

## 示例

### 示例 1
**输入:** `s = "103301"`  
**输出:** `2`  
**解释:**  
长度为 5 的子序列（subsequence）共有 6 种：`"10330"`, `"10331"`, `"10301"`, `"10301"`, `"13301"`, `"03301"`。其中有两条（均为 `"10301"`）是回文的。

### 示例 2
**输入:** `s = "0000000"`  
**输出:** `21`  
**解释:** 所有 21 条子序列都是 `"00000"`，显然是回文的。

### 示例 3
**输入:** `s = "9999900000"`  
**输出:** `2`  
**解释:** 唯一的两条回文子序列分别是 `"99999"` 和 `"00000"`。

## 约束条件

- `1 <= s.length <= 10^4`
- `s` 仅由数字字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是**枚举所有长度为 5 的子序列**，判断它是不是回文。  
- **子序列**可以把原字符串看成一排商品，挑选其中的 5 件（顺序不变），不要求连续。  
- 判断回文就像检查一串数字正着读和倒着读是否相同，长度 5 的回文一定满足 `a b c b a` 的结构。

实现时可以用 5 层循环（或 `itertools.combinations`）遍历所有 5‑元组的下标，然后把对应字符拼成子串，检查是否回文。

> **为什么能得到正确答案**  
> 只要把所有可能的 5‑字符子序列都检查一遍，凡是满足回文条件的都会被计数，漏掉的不会出现，故答案必然正确。

> **复杂度分析（大白话）**  
> - 假设字符串长度为 `n`，从 `n` 个位置里挑 5 个，有 `C(n,5) = n·(n-1)…(n-4)/120` 种组合。  
> - 对每一种组合我们要检查 5 个字符是否回文，时间就是常数。  
> - 因此总时间大约是 **O(n⁵)**，即随着字符串长度的 5 次方增长，计算会非常慢。  
> - 只用到几个临时数组保存下标，空间几乎是 **O(1)**（常数级）。

#### 代码（Python）

```python
from itertools import combinations

MOD = 10**9 + 7

def count_palindromes_bruteforce(s: str) -> int:
    n = len(s)
    ans = 0
    # 枚举所有 5 个下标的组合
    for i1, i2, i3, i4, i5 in combinations(range(n), 5):
        # 把对应字符拼成子串
        sub = s[i1] + s[i2] + s[i3] + s[i4] + s[i5]
        # 判断是否回文（a b c b a）
        if sub[0] == sub[4] and sub[1] == sub[3]:
            ans += 1
    return ans % MOD
```

#### 复杂度

- **时间复杂度**：`O(n⁵)` —— 随着字符串长度的 5 次方增长，实际运行会在 `n≈30` 时就超时。  
- **空间复杂度**：`O(1)` —— 只用了几个整数计数器和一次性组合生成器，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

长度为 5 的回文一定是 **a b c b a**（`c` 为中心字符）。  
如果把中心字符固定下来，左侧需要一个两字符的子序列 **ab**，右侧需要 **ba**，且这两个子序列必须分别出现在中心左边和右边，且顺序保持不变。

> **慢在哪里**  
> 暴力解的瓶颈是 **枚举所有 5‑元组**，组合数随 `n⁵` 暴涨。我们要把“枚举”这一步消掉，只统计**符合条件的配对数量**。

> **关键观察**  
> - 对于每一个位置 `i`（把 `s[i]` 当作中心 `c`），左边所有可能的 **ab** 只和左侧字符有关，右边所有可能的 **ba** 只和右侧字符有关。  
> - 只要知道左侧出现多少次 `ab`，右侧出现多少次 `ba`，它们的乘积就是以 `i` 为中心能够组成的回文数量。  
> - 数字只有 `0~9`，所以 `a`、`b` 只有 10 种可能，**两层循环 10×10=100** 就可以遍历完所有 `(a,b)` 组合。

> **如何快速得到左侧/右侧的 “ab”/“ba” 计数**  
> - **左侧**：从左往右遍历，维护  
>   - `left_one[d]`：左边出现的字符 `d` 的次数。  
>   - `left_pair[a][b]`：左边出现的子序列 `"ab"` 的次数。  
>   - 当看到一个新字符 `x` 时，先把它加入到所有以 `x` 为第二个字符的 pair 中：`left_pair[a][x] += left_one[a]`（因为每个已经出现的 `a` 可以和当前的 `x` 组成一个新的 `"ab"`），再把 `x` 的计数加一。  
> - **右侧**：从右往左遍历，同理维护 `right_one`、`right_pair`，但这里我们需要的顺序是 **先出现的字符是靠近中心的**，所以在倒序遍历时把当前字符当作 **第一个**，即 `right_pair[x][b] += right_one[b]`。  
> - 为了在遍历中心时能够直接取到“中心右侧的 pair”，我们在倒序遍历时把每个位置 `i` **之后**的 `right_pair` 复制保存下来，记为 `suffix_pair[i]`。

> **整体流程**  
> 1. **倒序预处理**：得到 `suffix_pair[i]`，即从 `i+1` 到结尾所有 `"ba"` 子序列的计数。  
> 2. **正序遍历**：把当前位置 `i` 当作中心，使用当前 `left_pair` 与 `suffix_pair[i]` 计算贡献：  
>    `ans += Σ_{a=0..9} Σ_{b=0..9} left_pair[a][b] * suffix_pair[i][b][a]`。  
> 3. 更新 `left_one`、`left_pair`，继续下一个中心。

> **为什么是 O(100·n)**  
> - 每次遍历（正序或倒序）我们只对 10×10 的矩阵做加法，常数是 100。  
> - 这样整体时间是 `O(100·n) = O(n)`，空间只需要保存两套 10×10 的矩阵和 `suffix_pair`（每个位置一个 10×10 矩阵），即 `O(100·n)`，在本题的 `n ≤ 10⁴` 完全可接受。

#### 代码（Python）

```python
MOD = 10**9 + 7
DIG = 10                     # 只有 0~9 十种数字

def count_palindromes_opt(s: str) -> int:
    n = len(s)
    digits = [int(ch) for ch in s]

    # ---------- 1. 倒序预处理，得到每个位置右侧的 pair 矩阵 ----------
    # right_one[d]：右侧已经遍历过的字符 d 的个数
    right_one = [0] * DIG
    # right_pair[x][y] 表示在当前右侧（不包括即将遍历的字符）出现的子序列 "xy"
    right_pair = [[0] * DIG for _ in range(DIG)]
    # suffix_pair[i] 保存 i 之后（即下标 > i）所有 "ba" 的计数
    suffix_pair = [None] * n

    # 从右往左遍历，先保存当前的 right_pair（对应 i 右侧），再把 s[i] 加入 right_one/right_pair
    for i in range(n - 1, -1, -1):
        suffix_pair[i] = [row[:] for row in right_pair]   # 复制一份快照

        cur = digits[i]
        # 当前字符 cur 作为 "b"（靠近中心的字符），与右侧所有已经出现的 a 组成 "ba"
        for a in range(DIG):
            right_pair[cur][a] += right_one[a]
        # 更新单字符计数
        right_one[cur] += 1

    # ---------- 2. 正序遍历，以每个字符为中心计算答案 ----------
    left_one = [0] * DIG
    left_pair = [[0] * DIG for _ in range(DIG)]
    ans = 0

    for i in range(n):
        cur = digits[i]                 # 作为中心字符 c
        # 用左侧的 "ab" 与右侧的 "ba" 配对
        right = suffix_pair[i]          # 右侧的 pair 矩阵
        for a in range(DIG):
            for b in range(DIG):
                ans = (ans + left_pair[a][b] * right[b][a]) % MOD

        # 继续把当前位置加入左侧统计，为后面的中心做准备
        for a in range(DIG):
            left_pair[a][cur] += left_one[a]   # 形成 "ab"，b 为当前字符
        left_one[cur] += 1

    return ans % MOD
```

> **代码要点注释**  
> - `right_pair[cur][a] += right_one[a]`：把所有已经在右侧出现的 `a` 与当前的 `cur` 组合成 `"ba"`（`cur` 靠近中心）。  
> - `suffix_pair[i] = [row[:] for row in right_pair]`：复制当前的 `right_pair`，因为以后遍历时 `right_pair` 会被修改。  
> - 正序遍历时的双层循环 `for a in range(DIG): for b in range(DIG):` 正好对应所有可能的 `(a,b)` 组合，乘积即为以 `i` 为中心能形成的回文数。  

#### 复杂度

- **时间复杂度**：`O(100·n) ≈ O(n)`  
  - 每次遍历（正序或倒序）只对 10×10 的矩阵进行加法，常数约 100。相比暴力的 `n⁵`，快得多。  
- **空间复杂度**：`O(100·n)`  
  - 需要保存每个位置的 `suffix_pair`（每个是 10×10 的整数矩阵），共 `100·n` 个整数。对 `n ≤ 10⁴` 来说大约 1 MB，完全可接受。  

---

## 心得

- **核心技巧**：把长度为 5 的回文拆成 `a b c b a`，利用**中心字符**把问题分割为左侧的两字符子序列与右侧的两字符子序列的计数乘积。  
- **适用的题型**  
  1. 统计固定长度回文子序列（如长度 3、5、7 等）。  
  2. 需要统计满足特定模式 `x y z y x` 的子序列计数。  
  3. “字母/数字配对”类的组合计数（比如 “ab…ba” 的配对计数）。  
- **一句话总结解题钥匙**：**把回文的对称结构拆开，先分别统计左/右两侧的配对出现次数，再把对应配对相乘求和**。

---

## 反思

- **第一反应**：看到“长度 5 的回文”，立刻想到“中心字符 + 两边对称”。于是尝试把问题转化为左侧两字符子序列与右侧两字符子序列的配对计数。  
- **最容易踩的坑**  
  1. **下标边界**：在倒序预处理时必须在保存 `suffix_pair[i]` 之前**不要**把 `s[i]` 加入右侧统计，否则会把中心字符算进右侧。  
  2. **模数运算**：乘积可能非常大，必须在累加到答案时立即取模，防止 Python 整数过大导致慢。  
  3. **计数溢出**：`left_pair[a][b]` 与 `right_pair[b][a]` 本身也可能很大，乘法前最好先转成 `int` 再取模（Python 自动大整数，但仍建议及时 `% MOD`）。  
- **下次类似题目第一步**：**确定对称结构或固定模式，把它拆成若干独立的子问题（如左/右配对、前缀/后缀计数）**，再寻找可以用前缀计数、后缀计数或 DP 合并的方式。