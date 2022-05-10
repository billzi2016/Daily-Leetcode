# #1771. 从子序列中构造的最长回文长度 / Maximize Palindrome Length From Subsequences

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximize-palindrome-length-from-subsequences/)

---

## 题目（英文原版）

**Description**

You are given two strings, word1 and word2. You want to construct a string in the following manner:
Return the length of the longest palindrome that can be constructed in the described manner. If no palindromes can be constructed, return 0.
A subsequence of a string s is a string that can be made by deleting some (possibly none) characters from s without changing the order of the remaining characters.
A palindrome is a string that reads the same forward as well as backward.

**Examples**

**Example 1:**

```
Input: word1 = "cacb", word2 = "cbba"
Output: 5
Explanation: Choose "ab" from word1 and "cba" from word2 to make "abcba", which is a palindrome.
```

**Example 2:**

```
Input: word1 = "ab", word2 = "ab"
Output: 3
Explanation: Choose "ab" from word1 and "a" from word2 to make "aba", which is a palindrome.
```

**Example 3:**

```
Input: word1 = "aa", word2 = "bb"
Output: 0
Explanation: You cannot construct a palindrome from the described method, so return 0.
```

**Constraints**

- 1 <= word1.length, word2.length <= 1000
- word1 and word2 consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`。你可以分别从 `word1` 和 `word2` 中选取一个子序列（subsequence），然后按顺序拼接这两个子序列得到一个新字符串。返回能够构造的最长回文（palindrome）的长度。如果无法构造任何回文，返回 `0`。

- **子序列**：可以通过删除原字符串中的若干（也可能不删除）字符而不改变剩余字符相对顺序得到的字符串。  
- **回文**：正读和反读完全相同的字符串。

### 示例

#### 示例 1
**输入**: `word1 = "cacb", word2 = "cbba"`  
**输出**: `5`  
**解释**: 从 `word1` 中选取子序列 `"ab"`，从 `word2` 中选取子序列 `"cba"`，拼接得到 `"abcba"`，它是一个回文，长度为 5。

#### 示例 2
**输入**: `word1 = "ab", word2 = "ab"`  
**输出**: `3`  
**解释**: 从 `word1` 中选取子序列 `"ab"`，从 `word2` 中选取子序列 `"a"`，拼接得到 `"aba"`，它是一个回文，长度为 3。

#### 示例 3
**输入**: `word1 = "aa", word2 = "bb"`  
**输出**: `0`  
**解释**: 无法按照上述方法构造回文，返回 `0`。

### 约束条件

- `1 <= word1.length, word2.length <= 1000`
- `word1` 和 `word2` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是「把两段字符串的每一种子序列都列出来，配对后检查是不是回文」，把能得到的最长回文长度记下来。

- **子序列**：把原字符串看成一本书，随意把几页撕掉，剩下的页码顺序不变，这就是一个子序列。  
- **回文**：正着读和反着读完全一样的字符串，就像「镜子里看到的自己」。
- **暴力枚举**：  
  1. 对 `word1` 的所有子序列进行枚举（相当于把 0/1 开关放在每个字符前，决定保留还是删除），总共有 `2^{|word1|}` 种。  
  2. 同理枚举 `word2` 的子序列，`2^{|word2|}` 种。  
  3. 把每一对子序列拼接起来（先 `word1` 再 `word2`），判断它是不是回文，若是则更新最大长度。  

为什么能得到正确答案？因为我们把 **所有** 合法的选法都尝试了一遍，最优的必然在其中。

#### 代码（Python）

```python
from itertools import product

def all_subsequences(s: str):
    """返回字符串 s 的所有非空子序列（列表形式）"""
    n = len(s)
    subseqs = []
    # 0/1 组合决定每个字符是否保留
    for mask in range(1, 1 << n):          # 0 代表全删，跳过
        cur = []
        for i in range(n):
            if mask >> i & 1:               # 第 i 位是 1，保留字符
                cur.append(s[i])
        subseqs.append(''.join(cur))
    return subseqs

def is_palindrome(st: str) -> bool:
    return st == st[::-1]

def brute(word1: str, word2: str) -> int:
    subs1 = all_subsequences(word1)   # O(2^n)
    subs2 = all_subsequences(word2)   # O(2^m)
    ans = 0
    for a in subs1:                   # 两层循环遍历所有配对
        for b in subs2:
            cand = a + b               # 按要求先 word1 后 word2 拼接
            if is_palindrome(cand):
                ans = max(ans, len(cand))
    return ans
```

> **关键行中文注释**  
> - `for mask in range(1, 1 << n)`: 用二进制的「开关」枚举保留哪些字符。  
> - `cand = a + b`: 把两段子序列拼成最终字符串。  
> - `if is_palindrome(cand)`: 判断是否满足「正读反读相同」的回文条件。

#### 复杂度  

- **时间复杂度**：`O(2^{|word1|} * 2^{|word2|} * L)`，  
  其中 `L` 是拼接后字符串的长度（最多 `|word1|+|word2|`），  
  简单来说就是「指数级」的慢——即使 `|word1|=|word2|=20` 已经不可接受。  
- **空间复杂度**：`O(2^{|word1|} + 2^{|word2|})` 用来存放所有子序列，同样是指数级。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在 **枚举所有子序列**，这一步把每个字符的取舍都单独考虑，导致指数级爆炸。  
观察题目可以发现：

1. **我们只关心最长的回文子序列**（LPS，Longest Palindromic Subsequence），而不是每一种子序列。  
2. **LPS 有经典的动态规划解法**：在一个字符串 `s` 上，`dp[i][j]` 表示区间 `s[i…j]`（两端都包含）内的最长回文子序列长度。  
3. 这里的字符串其实是 `s = word1 + word2` 的**拼接**，因为子序列可以跨两个原字符串。唯一的额外约束是：**回文的左端必须取自 `word1`，右端必须取自 `word2`**（题目要求先选 `word1` 的子序列，再选 `word2` 的子序列拼接）。  

基于这三点，我们可以：

- 先对拼接字符串 `s` 完整地算出 `dp` 表（不考虑“必须跨两段”的限制）。这一步的复杂度是 `O(N^2)`，`N = |word1|+|word2| ≤ 2000`，可以接受。  
- 再在 `dp` 表中挑选所有 **左端索引 i 属于 `word1`（0 ≤ i < n）且右端索引 j 属于 `word2`（n ≤ j < N）** 的区间，取其中最大的 `dp[i][j]`。这一步直接得到答案。  

如果没有任何满足条件的区间，说明根本不存在同时使用两段字符的回文，返回 `0`。

**动态规划细节**（从零解释）：

- **状态** `dp[i][j]`：在子串 `s[i…j]` 中，最长回文子序列的长度。  
- **初始化**：  
  - 当 `i == j` 时，只剩一个字符，显然可以构成长度为 `1` 的回文。  
  - 当 `i > j`（空区间）时，长度为 `0`（在实现中可以用 `0` 填充）。  
- **状态转移**：  
  - 若 `s[i] == s[j]`，则这两个字符可以放在回文的两端，长度 = `dp[i+1][j-1] + 2`。  
  - 若不相等，则不能同时使用这两个字符，只能在 `i` 或 `j` 中「丢掉」一个，取两种情况的最大值：`max(dp[i+1][j], dp[i][j-1])`。  
- **遍历顺序**：因为 `dp[i][j]` 依赖于 `i+1`、`j-1`，我们先算小区间再算大区间。常用的做法是外层遍历左端 `i` 从后往前，内层遍历右端 `j` 从 `i+1` 到末尾。

**为什么这一步比暴力快？**  
动态规划把「每个字符要不要选」的指数级决策压缩成「子区间的最优值」的多项式级递推，只需要记录每个区间的答案一次，避免了重复计算。

#### 代码（Python）

```python
def longestPalindrome(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    s = word1 + word2                # 合并后的完整字符串
    N = n + m

    # dp[i][j] 表示 s[i..j] 区间的最长回文子序列长度
    dp = [[0] * N for _ in range(N)]

    # 单字符区间：长度为 1
    for i in range(N):
        dp[i][i] = 1

    # 按区间长度从短到长填表
    for length in range(2, N + 1):          # length = 子串长度
        for i in range(N - length + 1):
            j = i + length - 1              # 区间右端
            if s[i] == s[j]:
                # 两端相等，可以拼在回文的两头
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                # 取丢掉左端或右端后的最大值
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    # 在所有左端来自 word1、右端来自 word2 的区间里找最大值
    ans = 0
    for i in range(n):               # i 必须在 word1 区间
        for j in range(n, N):        # j 必须在 word2 区间
            ans = max(ans, dp[i][j])

    return ans                       # 若 ans 为 0，说明不存在合法回文
```

> **关键行中文注释**  
> - `dp[i][i] = 1`：单个字符本身就是回文，长度 1。  
> - `if s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2`：把相同的两端放进回文，两边各贡献 1。  
> - `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`：若两端不同，必须舍弃左或右，取更大的那条路。  
> - 最后两层 `for i in range(n)`、`for j in range(n, N)`：只统计「左在 word1、右在 word2」的区间，正好满足「先取 word1 再取 word2」的拼接顺序。

#### 复杂度  

- **时间复杂度**：`O((n+m)^2)`。  
  - 解释：我们遍历所有长度为 `1 … N` 的区间，每个区间只做常数次比较和赋值，整体相当于填一个 `N × N` 的表。对于 `N ≤ 2000`，约 `4 × 10⁶` 次操作，毫秒级即可完成。  
  - 与暴力的指数级 `2^n·2^m` 相比，**从天际跌到地面**，可以轻松通过所有测试用例。  

- **空间复杂度**：`O((n+m)^2)`（存 `dp` 表）。  
  - 解释：我们需要记录每个区间的最优值，表格大小正好是 `N²`。如果想进一步压缩空间，可以只保留前一行/列的状态，降到 `O(N)`，但为了代码可读性这里保持完整表格。  

---

## 心得

- **核心技巧**：**最长回文子序列的动态规划** + **跨段约束的后处理**。  
- **该技巧适用的题型**：  
  1. 在合并后的字符串上求 LPS（如 “Maximum Palindrome Length From Subsequences”）。  
  2. “两个序列的最长公共回文子序列” 类似问题。  
  3. “在一个序列中挑选子序列，使其前后对称” 的变形。  
- **一句话总结解题钥匙**：  
  *把两段字符串拼成一个整体，先用标准 LPS DP 求所有子区间的答案，再在必须跨越两段的区间里挑最大值。*

---

## 反思

- **第一反应**：直接把两段字符串的所有子序列枚举完再检查回文——想当然地把「所有可能」写成代码。  
- **最容易踩的坑**  
  1. **跨段限制**：只要记得答案必须左端在 `word1`、右端在 `word2`，否则会得到仅使用单段字符的更大回文（不符合题意）。  
  2. **空区间**：如果两段都没有共同字符，`dp[i][j]` 仍会返回 1（单字符），但这不满足「两段都要选」的条件，需要在最终统计时过滤。  
  3. **下标错误**：合并后字符串的下标和原来两段的下标不同，容易把 `n`（`word1` 长度）算错。  
- **下次类似题的第一步**：  
  *先把所有涉及的字符放进同一个统一序列，求出该序列的经典 DP（LPS、LCS、最长递增子序列等），再在 DP 结果上加上题目额外的“必须跨越/必须包含”等约束。*