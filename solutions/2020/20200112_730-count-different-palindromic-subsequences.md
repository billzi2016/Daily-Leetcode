# #730. 不同回文子序列计数 / Count Different Palindromic Subsequences

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-different-palindromic-subsequences/)

---

## 题目（英文原版）

**Description**

Given a string s, return the number of different non-empty palindromic subsequences in s. Since the answer may be very large, return it modulo 109 + 7.
A subsequence of a string is obtained by deleting zero or more characters from the string.
A sequence is palindromic if it is equal to the sequence reversed.
Two sequences a1, a2, ... and b1, b2, ... are different if there is some i for which ai != bi.

**Examples**

**Example 1:**

```
Input: s = "bccb"
Output: 6
Explanation: The 6 different non-empty palindromic subsequences are 'b', 'c', 'bb', 'cc', 'bcb', 'bccb'.
Note that 'bcb' is counted only once, even though it occurs twice.
```

**Example 2:**

```
Input: s = "abcdabcdabcdabcdabcdabcdabcdabcddcbadcbadcbadcbadcbadcbadcbadcba"
Output: 104860361
Explanation: There are 3104860382 different non-empty palindromic subsequences, which is 104860361 modulo 109 + 7.
```

**Constraints**

- 1 <= s.length <= 1000
- s[i] is either 'a', 'b', 'c', or 'd'.

---

## 题目（中文翻译）

给定一个字符串 `s`，返回 `s` 中不同的非空回文子序列（palindromic subsequence）的数量。由于答案可能非常大，请返回其对 $10^9 + 7$ 取模后的结果。

子序列（subsequence）是通过从字符串中删除零个或多个字符得到的序列。

如果一个序列等于其逆序（reversed）序列，则称其为回文（palindromic）。

当且仅当存在某个下标 `i` 使得 `a_i ≠ b_i` 时，序列 `a₁, a₂, …` 与 `b₁, b₂, …` 被视为不同。

**示例 1**

```
Input: s = "bccb"
Output: 6
Explanation: 这 6 个不同的非空回文子序列分别是 'b', 'c', 'bb', 'cc', 'bcb', 'bccb'。注意，虽然 'bcb' 出现了两次，但只计数一次。
```

**示例 2**

```
Input: s = "abcdabcdabcdabcdabcdabcdabcdabcddcbadcbadcbadcbadcbadcbadcbadcba"
Output: 104860361
Explanation: 共有 3104860382 个不同的非空回文子序列，取模 $10^9 + 7$ 后得到 104860361。
```

**约束条件**

- $1 \leq s.length \leq 1000$
- $s[i]$ 仅为字符 `'a'`, `'b'`, `'c'` 或 `'d'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串的所有**子序列**都枚举出来，挑出其中是回文的，再把相同的序列去重计数。

- **子序列**：把原字符串的若干字符（可以不连续）挑出来，保持原来的相对顺序。  
  想象把每个字符看成一本书的页码，挑选页码的过程就像在**查字典**：我们可以任选几页（可以不选），但选出来的页码顺序不能改变。

- **回文**：序列正着读和倒着读一样。  
  比如 `"bcb"`，正读是 `b c b`，倒读也是 `b c b`。

- **去重**：因为不同的挑选方式可能得到相同的序列，需要用集合（类似装字典的抽屉）把它们合在一起，只算一次。

**为什么能得到正确答案**  
只要把**所有可能的子序列**都列举出来，就不会漏掉任何合法的回文子序列。再把重复的删掉，剩下的就是题目要求的“不同的非空回文子序列”。

**时间/空间分析（大白话）**  

- 枚举子序列的方式是二进制计数：每个字符有“选”或“不选”两种状态，长度为 `n` 的字符串一共有 `2ⁿ` 种组合。  
  所以时间复杂度是 **O(2ⁿ·n)**（每个组合要检查一次是不是回文，检查需要 O(n)）。  
  当 `n=30` 时 `2ⁿ` 已经是十亿级，根本跑不完，更别说 `n` 最高可以到 1000。

- 我们需要把所有找到的回文序列放进集合去重，最坏情况下集合里会有 `2ⁿ` 条记录，空间复杂度也是 **O(2ⁿ)**。

显然，这个办法只能在极小的输入上玩玩，根本不适合正式提交。

#### 代码（Python）

```python
from typing import Set

MOD = 10**9 + 7

def count_palindromes_bruteforce(s: str) -> int:
    n = len(s)
    seen: Set[str] = set()                     # 用集合自动去重

    # 递归枚举所有子序列
    def dfs(idx: int, path: list):
        if idx == n:
            if path:                           # 非空序列
                cand = ''.join(path)
                if cand == cand[::-1]:        # 判断回文（正着倒着一样）
                    seen.add(cand)
            return
        # 不选 s[idx]
        dfs(idx + 1, path)
        # 选 s[idx]
        path.append(s[idx])
        dfs(idx + 1, path)
        path.pop()                             # 恢复现场

    dfs(0, [])
    return len(seen) % MOD
```

> 关键行解释  
> - `seen: Set[str] = set()`：类似字典的抽屉，放进去的相同字符串只会出现一次。  
> - `cand == cand[::-1]`：Python 的切片技巧，`[::-1]` 把字符串倒过来，判断是否相等即是回文。  
> - `len(seen) % MOD`：最后把答案取模，防止数字太大。

#### 复杂度

- **时间复杂度**：`O(2ⁿ·n)`  
  解释：每个字符有两种状态（选/不选），所以有 `2ⁿ` 种组合；每次组合要把字符拼成字符串并检查回文，需要 O(n) 时间。

- **空间复杂度**：`O(2ⁿ)`  
  解释：最坏情况下所有子序列都是回文（比如全部字符相同），集合里会保存 `2ⁿ` 条记录。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有子序列**。我们需要直接统计不同的回文子序列，而不是把它们一一列举。  
这里可以使用**动态规划（DP）**：把大问题拆成子区间的答案，利用已经算好的子区间结果快速得到更大区间的答案。

**核心想法**  

设 `dp[i][j]` 为子串 `s[i..j]`（含两端）的**不同回文子序列个数**（包括空串）。  
我们从左到右、从短到长填表格。

- **情况 1：两端字符不相同**  
  `s[i] != s[j]` 时，区间 `[i, j]` 的回文子序列要么不使用左端字符，要么不使用右端字符。  
  所以  
  ```
  dp[i][j] = dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]
  ```
  这里 `- dp[i+1][j-1]` 是因为左端和右端都不使用的子序列被加了两次，需要减掉一次。

- **情况 2：两端字符相同**（记作 `c = s[i] = s[j]`）  
  这时可以在子序列两端再各加一个 `c`，形成新的回文。  
  关键是要看在 `i` 与 `j` 之间是否还有 `c`：

  1. **区间内部没有 `c`**  
     那么新出现的回文只有两种：单字符 `c` 和 `"c...c"`（两端直接相连），共 **2** 种。  
     ```
     dp[i][j] = 2 * dp[i+1][j-1] + 2
     ```

  2. **区间内部恰好有一个 `c`**（即 `i` 与 `j` 之间只出现一次 `c`）  
     新的回文形式只有 **1** 种（`"c...c"`），因为单字符 `c` 已经算过了。  
     ```
     dp[i][j] = 2 * dp[i+1][j-1] + 1
     ```

  3. **区间内部出现了两个或以上的 `c`**  
     为了避免重复计数，需要减掉区间 `(l+1, r-1)` 中已经算过的回文（`l`、`r` 分别是 `i` 右边第一个 `c`，`j` 左边最后一个 `c`）。  
     ```
     dp[i][j] = 2 * dp[i+1][j-1] - dp[l+1][r-1]
     ```

**如何快速得到 `l`、`r`**  
因为字符种类只有 `'a'~'d'` 四个，我们可以预处理两个二维数组：

- `next_pos[i][ch]`：从位置 `i` 开始向右，第一个出现字符 `ch` 的下标（若不存在记为 `n`）。  
- `prev_pos[i][ch]`：从位置 `i` 向左，第一个出现字符 `ch` 的下标（若不存在记为 `-1`）。

这样在 O(1) 时间内就能得到 `l`、`r`。

**整体步骤**  

1. 预处理 `next_pos`、`prev_pos`（时间 O(4·n)）。  
2. 初始化 `dp[i][i] = 1`（单个字符本身是回文）。  
3. 按长度从 2 到 n 填表。  
4. 最终答案是 `dp[0][n-1] - 1`（减去空串），再取模。

**为什么是最优**  
- 只遍历了所有 **O(n²)** 的子区间，每个子区间的计算是 O(1)。  
- 没有枚举子序列，也没有使用指数级的递归，时间复杂度降到 **O(n²)**，空间 **O(n²)**（可以进一步压缩到 O(n) 但对本题不必）。  
- 只利用了字符种类固定为 4 的特性，使得“去重”一步可以用常数时间完成。

#### 代码（Python）

```python
MOD = 10**9 + 7

def count_palindromes_dp(s: str) -> int:
    n = len(s)
    # 1. 预处理 next_pos 与 prev_pos
    # next_pos[i][c] = 从 i 开始（含 i）向右第一个字符 c 的下标
    # prev_pos[i][c] = 从 i 开始（含 i）向左第一个字符 c 的下标
    next_pos = [[n] * 4 for _ in range(n + 1)]
    prev_pos = [[-1] * 4 for _ in range(n)]

    # 从左到右填 prev_pos
    last = [-1] * 4
    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')          # 把 'a'~'d' 映射到 0~3
        last[idx] = i
        for c in range(4):
            prev_pos[i][c] = last[c]

    # 从右到左填 next_pos
    nxt = [n] * 4
    for i in range(n - 1, -1, -1):
        idx = ord(s[i]) - ord('a')
        nxt[idx] = i
        for c in range(4):
            next_pos[i][c] = nxt[c]

    # 2. DP 表
    dp = [[0] * n for _ in range(n)]

    # 长度为 1 的子串：只有一种回文（自身）
    for i in range(n):
        dp[i][i] = 1

    # 按子串长度递增
    for length in range(2, n + 1):          # length = 子串长度
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] != s[j]:
                # 情况 1：两端不同
                dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]) % MOD
            else:
                # 情况 2：两端相同
                ch = ord(s[i]) - ord('a')
                # 在 (i, j) 区间内部，找最左和最右的相同字符
                l = next_pos[i + 1][ch]      # i 右边第一个 ch
                r = prev_pos[j - 1][ch]      # j 左边最后一个 ch

                if l > r:                    # 区间内部没有 ch
                    dp[i][j] = (2 * dp[i + 1][j - 1] + 2) % MOD
                elif l == r:                 # 只出现一次 ch
                    dp[i][j] = (2 * dp[i + 1][j - 1] + 1) % MOD
                else:                        # 至少出现两次
                    dp[i][j] = (2 * dp[i + 1][j - 1] - dp[l + 1][r - 1]) % MOD

            # Python 取模时可能出现负数，统一加 MOD 再取模
            dp[i][j] = (dp[i][j] + MOD) % MOD

    # 减去空串
    return (dp[0][n - 1] - 1) % MOD
```

> 关键行解释  
> - `next_pos` / `prev_pos`：把字符的 **“在字典里找页码”** 过程变成常数时间查询。  
> - `if l > r`：表示在 `i` 与 `j` 之间根本没有相同字符，直接用公式 `2*dp + 2`。  
> - `dp[i][j] = (dp[i][j] + MOD) % MOD`：防止中间计算出现负数（因为有减法），保证结果始终在 `[0, MOD)` 之间。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们遍历所有 `n·(n+1)/2` 个子区间，每个子区间只做常数次加减乘运算（利用预处理的 `next/prev`），所以总体是平方级别。相较于暴力的指数级 `2ⁿ`，快得多。

- **空间复杂度**：`O(n²)`（`dp` 表） + `O(n·4)`（`next_pos`、`prev_pos`）≈ `O(n²)`  
  解释：`dp` 用来记忆化子区间的答案，需要 `n²` 个整数；其余辅助数组只占线性空间。

---

## 心得

- **核心技巧**：利用**区间动态规划**结合**前缀/后缀字符位置**（`next/prev`）来消除重复计数。  
- **适用的题型**：  
  1. “不同的子序列/子串计数”类（如 LeetCode 940、1150）。  
  2. “区间回文计数”或“区间不同字符计数”类（如 1132、1316）。  
- **一句话总结解题钥匙**：把“把所有子序列都枚举”转化为“把所有子区间的答案合并”，并用字符的最左/最右出现位置来避免重复计数。

---

## 反思

- **第一反应**：直接想把所有子序列列举出来检查回文，结果马上发现 **爆炸的时间复杂度**。  
- **最容易踩的坑**  
  - **负数取模**：在公式 `2*dp - dp[l+1][r-1]` 中可能出现负数，需要加 `MOD` 再取模。  
  - **边界条件**：`l`、`r` 超出区间时（如 `l > r`），要特别处理，否则会访问非法下标。  
  - **空串**：DP 表默认计数包括空串，最后答案要记得减去 1。  
- **下次类似题的第一步**：先思考 **“能否把大问题拆成子区间的子问题”**，并检查是否有 **固定字符种类**、**位置预处理** 等可以帮助快速去重的手段。