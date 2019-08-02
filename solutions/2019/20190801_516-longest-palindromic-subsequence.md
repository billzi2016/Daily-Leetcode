# #516. **最长回文子序列** / Longest Palindromic Subsequence

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-palindromic-subsequence/)

---

## 题目（英文原版）

**Description**

Given a string s, find the longest palindromic subsequence's length in s.
A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: s = "bbbab"
Output: 4
Explanation: One possible longest palindromic subsequence is "bbbb".
```

**Example 2:**

```
Input: s = "cbbd"
Output: 2
Explanation: One possible longest palindromic subsequence is "bb".
```

**Constraints**

- 1 <= s.length <= 1000
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，求 `s` 中最长回文子序列（palindromic subsequence）的长度。  
子序列（subsequence）是指可以通过删除原序列中的任意个（包括零个）字符而不改变剩余字符相对顺序得到的序列。

**示例 1**  
**输入**: `s = "bbbab"`  
**输出**: `4`  
**解释**: 一种可能的最长回文子序列是 `"bbbb"`。

**示例 2**  
**输入**: `s = "cbbd"`  
**输出**: `2`  
**解释**: 一种可能的最长回文子序列是 `"bb"`。

**约束条件**  

- `1 <= s.length <= 1000`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的子序列都枚举出来，检查它们是不是回文（正读和反读相同），再取最长的长度。  
- **子序列**：想象把原字符串的字符当成一排书签，你可以随意挑选其中的几本书（可以不挑），只要保持原来的顺序不变。  
- **回文判断**：就像把选出来的单词正着读和反着读是否一样，常用的做法是把它翻转后比较。  

为什么这种方法能得到正确答案？因为我们穷举了**所有**合法的子序列，只要其中有回文子序列，必然会被检查到，取最大长度自然就是答案。

缺点是：  
- 长度为 `n` 的字符串有 `2^n`（每个字符选或不选）种子序列，枚举会指数级爆炸。  
- 对每个子序列我们还要做回文检查，进一步增加工作量。

#### 代码（Python）

```python
import itertools

def longestPalindromeSubseq_bruteforce(s: str) -> int:
    n = len(s)
    max_len = 0                     # 记录目前找到的最长回文子序列长度
    # 1~n 位的子序列都要尝试（0 位子序列长度为 0，直接跳过）
    for length in range(1, n + 1):
        # itertools.combinations 会返回所有 length 长度的下标组合
        for idx_tuple in itertools.combinations(range(n), length):
            # 根据下标把字符拼成子序列
            subseq = ''.join(s[i] for i in idx_tuple)
            # 判断是否为回文：正读和反读相同
            if subseq == subseq[::-1]:
                max_len = max(max_len, length)   # 更新最大长度
    return max_len
```

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 是子序列的总数（指数级），每个子序列最多需要 `O(n)` 的时间来拼接和回文检查。  
  - 用大白话说，就是“随着字符串长度稍微增长，运行时间就会像滚雪球一样飞快变大”。  
- **空间复杂度**：`O(n)`  
  - 主要是保存临时子序列的字符串，最坏情况下长度为 `n`。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **重复计算**：很多子序列在不同的组合里会出现相同的前缀或后缀。  
我们可以利用“子问题最优解组成整体最优解” 的思想，用 **动态规划（DP）** 把问题拆成小块，只计算一次。

**核心观察**  
- 设 `dp[i][j]` 表示子串 `s[i…j]`（左闭右闭区间）内部的**最长回文子序列长度**。  
- 当 `i == j` 时，只剩一个字符，显然回文长度为 1。  
- 当 `s[i] == s[j]` 时，这两个字符可以一起构成回文的两端，答案等于 `dp[i+1][j-1] + 2`（把内部的最优解包在这两个字符之间）。  
- 当 `s[i] != s[j]` 时，这两个字符不可能同时出现在同一个回文子序列的两端，只能把其中一个丢掉，于是答案是 `max(dp[i+1][j], dp[i][j-1])`——即“左边去掉一个字符”或“右边去掉一个字符”两种情况的较大值。

**填表顺序**  
因为 `dp[i][j]` 依赖于 `dp[i+1][j-1]、dp[i+1][j]、dp[i][j-1]`，我们可以从**短子串**往**长子串**推进。  
常见做法是让 `i` 从右向左遍历，`j` 从 `i` 向右遍历，这样在计算 `dp[i][j]` 时，所需的子状态已经算好。

**空间优化**  
观察发现，每一次只会用到 `i+1` 行的数据和当前行的左侧数据。于是可以把二维数组压缩成一维 `dp[j]`，再用一个临时变量保存左上角的旧值。这样空间从 `O(n^2)` 降到 `O(n)`。

下面先给出完整的二维 DP 实现，随后展示压缩到一维的版本（两者时间复杂度相同）。

#### 代码（Python）

```python
def longestPalindromeSubseq_dp(s: str) -> int:
    n = len(s)
    # dp[i][j] 表示 s[i..j] 的最长回文子序列长度
    dp = [[0] * n for _ in range(n)]

    # 所有长度为 1 的子串，回文长度都是 1
    for i in range(n):
        dp[i][i] = 1

    # 子串长度从 2 到 n 逐步扩大
    for length in range(2, n + 1):               # length = 子串的实际长度
        for i in range(n - length + 1):
            j = i + length - 1                    # 子串右端下标
            if s[i] == s[j]:
                if length == 2:                   # 两个字符相等且长度为 2，直接是 "aa"
                    dp[i][j] = 2
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]                           # 整个字符串的答案
```

**空间压缩版（只用 O(n) 额外空间）**

```python
def longestPalindromeSubseq_dp_optimized(s: str) -> int:
    n = len(s)
    dp = [0] * n          # dp[j] 最终会表示 s[i..j] 的答案（i 会在外层循环中变化）

    for i in range(n - 1, -1, -1):   # i 从右往左遍历
        dp[i] = 1                    # 子串长度为 1 时，回文长度为 1
        prev = 0                     # 保存 dp[i+1][j-1] 的旧值，初始为 0
        for j in range(i + 1, n):    # j 向右扩展
            temp = dp[j]             # 先把 dp[i+1][j] 暂存到 temp，供下次循环使用
            if s[i] == s[j]:
                dp[j] = prev + 2      # prev 正好是 dp[i+1][j-1]
            else:
                dp[j] = max(dp[j], dp[j - 1])  # dp[j] 为 dp[i+1][j]，dp[j-1] 为 dp[i][j-1]
            prev = temp              # 更新 prev 为下一轮的左上角值
    return dp[-1]                    # dp[n-1] 对应 dp[0][n-1]
```

#### 复杂度  

- **时间复杂度**：`O(n^2)`  
  - 两层循环分别遍历 `i`（`n` 次）和 `j`（最多 `n` 次），所以总操作次数约为 `n²/2`，即平方级。  
  - 用大白话说，就是“如果字符串长 1000，最多要算大约 1,000,000 次”，在电脑上几毫秒就能完成。  

- **空间复杂度**：  
  - **二维实现**：`O(n^2)`，需要一个 `n×n` 的表格来存所有子问题的答案。  
  - **一维压缩实现**：`O(n)`，只用一个长度为 `n` 的数组，节省了大量内存，尤其在 `n=1000` 时差别明显。  

相较于暴力解的指数级时间，DP 把时间从“天文数字”降到了“可接受的多项式”。

---

## 心得

- **核心技巧**：把“最长回文子序列”转化为区间 DP，利用子问题的最优子结构（`dp[i][j]` 依赖于更小区间的结果）。
- **适用的题型**  
  1. **最长回文子串**（Longest Palindromic Substring）——可以用中心扩展或 DP。  
  2. **编辑距离**（Edit Distance）——同样是区间 DP，求两字符串的最小编辑步数。  
  3. **最长公共子序列**（Longest Common Subsequence）——也是子序列 DP，只是比较两串而非同一串的回文。  
- **一句话总结解题钥匙**：**“把大问题拆成左右端点的子区间，递推构造最优解”。**

---

## 反思

- **第一反应**：看到“子序列”二字，立刻想到“枚举所有子序列”，于是想到暴力解。  
- **最容易踩的坑**  
  1. **下标越界**：`dp[i+1][j-1]` 只在 `i+1 ≤ j-1` 时才有效，需要特殊处理长度为 2 的情况。  
  2. **递推顺序错误**：如果先遍历 `i` 从左到右，会出现依赖尚未计算的状态。必须保证“子区间先算好”。  
  3. **空间压缩时的临时变量**：忘记保存左上角的旧值会导致结果错误。  
- **下次思路**：遇到“最长/最短/最大”这类子序列或子串问题，第一步先问自己“是否存在子区间的最优子结构”，如果答案是“是”，就立刻尝试 DP（先写二维表再考虑压缩）。