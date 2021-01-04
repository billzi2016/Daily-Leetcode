# #1143. 最长公共子序列 / Longest Common Subsequence

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-common-subsequence/)

---

## 题目（英文原版）

**Description**

Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.
A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.
A common subsequence of two strings is a subsequence that is common to both strings.

**Examples**

**Example 1:**

```
Input: text1 = "abcde", text2 = "ace" 
Output: 3  
Explanation: The longest common subsequence is "ace" and its length is 3.
```

**Example 2:**

```
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.
```

**Example 3:**

```
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.
```

**Constraints**

- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters.

---

## 题目（中文翻译）

给定两个字符串 `text1` 和 `text2`，返回它们最长公共子序列（Longest Common Subsequence）的长度。如果不存在公共子序列，则返回 `0`。  
子序列（subsequence）是指从原字符串中删除若干字符（可以不删）后得到的新字符串，且剩余字符的相对顺序保持不变。  
公共子序列（common subsequence）是指同时出现在两个字符串中的子序列。

### 示例

**示例 1**  
```
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: 最长公共子序列是 "ace"，其长度为 3。
```

**示例 2**  
```
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: 最长公共子序列是 "abc"，其长度为 3。
```

**示例 3**  
```
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: 不存在公共子序列，结果为 0。
```

### 约束条件
- `1 <= text1.length, text2.length <= 1000`
- `text1` 和 `text2` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **text1** 的所有子序列枚举出来，再和 **text2** 的所有子序列逐一比对，找出最长的公共子序列。  

- **子序列**：可以把它想成“从一串珠子里挑出若干颗珠子，但挑出来的顺序不能变”。  
- **暴力枚举**：我们可以用递归/回溯把每个字符“要”或“不要”，于是得到 `2^{len(text1)}` 种子序列。  
- **查找公共**：把 **text2** 也枚举出子序列后，用“查字典”的方式（哈希表）判断两者是否相同。  

为什么能得到正确答案？因为我们把 **所有可能的子序列** 都列出来了，答案一定在其中。只不过这种做法会非常慢。

#### 代码（Python）

```python
def all_subsequences(s: str) -> set:
    """返回字符串 s 的所有子序列（不包括空串）"""
    res = set()
    n = len(s)

    def dfs(idx: int, path: list):
        # idx 表示当前处理到 s 的哪个位置
        if idx == n:
            if path:                     # 过滤掉空串
                res.add(''.join(path))
            return
        # ① 选取 s[idx]
        path.append(s[idx])
        dfs(idx + 1, path)
        path.pop()                       # 恢复现场

        # ② 不选取 s[idx]
        dfs(idx + 1, path)

    dfs(0, [])
    return res


def longest_common_subsequence_brute(text1: str, text2: str) -> int:
    # 先把两个字符串的所有子序列列出来
    subs1 = all_subsequences(text1)
    subs2 = all_subsequences(text2)

    # 用集合的交集快速找出公共子序列
    common = subs1 & subs2
    if not common:
        return 0
    # 找最长的那个
    return max(len(seq) for seq in common)


# 示例
print(longest_common_subsequence_brute("abcde", "ace"))   # 3
```

#### 复杂度  

- **时间复杂度**：  
  - 枚举一个长度为 *n* 的字符串的子序列需要遍历 `2^n` 种可能。  
  - 对两个字符串分别枚举后再求交集，总时间大致是 `O(2^{m} + 2^{n})`，其中 *m*、*n* 为两字符串的长度。  
  - 用大白话说，就是“指数级别的慢”，长度 10 以上就几乎不可用。

- **空间复杂度**：  
  - 需要存储所有子序列，最坏情况是 `O(2^{m} + 2^{n})` 个字符串，空间同样是指数级。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复子问题**是导致慢的根本原因。比如在枚举子序列时，同样的前缀会被计算很多次。我们可以把“子问题的答案”记下来，以免重复计算——这正是 **动态规划（DP）** 的核心思想。

**核心状态**  
- 设 `dp[i][j]` 为 **text1 前 i 个字符**（即 `text1[0..i-1]`）和 **text2 前 j 个字符**（即 `text2[0..j-1]`）的最长公共子序列长度。  
- 这里的 “前 i 个字符” 可以想象成“把字符串切成两段，只看左边的那段”。  

**状态转移**  

| 情况 | 说明 | 递推式 |
|------|------|--------|
| `text1[i-1] == text2[j-1]` | 最后一个字符相同，必然可以把它加入公共子序列 | `dp[i][j] = dp[i-1][j-1] + 1` |
| `text1[i-1] != text2[j-1]` | 最后一个字符不同，最长公共子序列只能来源于去掉其中一个字符的子问题 | `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` |

**初始化**  
- 当 `i = 0` 或 `j = 0` 时，表示有一个字符串为空，此时公共子序列长度必为 0。对应的第一行和第一列全部填 0。

**实现细节**  
- 为了方便下标，`dp` 的大小设为 `(len(text1)+1) × (len(text2)+1)`，多出的一行一列用来存放“空字符串”的情况。  
- 最终答案就在 `dp[m][n]`（`m = len(text1)`，`n = len(text2)`）里。

**空间优化**（可选）  
- 观察递推式只会用到 `dp[i-1][*]`（上一行）和当前行的左边值，所以可以把二维数组压缩成 **两行**，甚至 **一行**（滚动数组）来降低空间消耗。这里先给出最直观的二维实现，后面再说明一行版。

#### 代码（Python）

```python
def longest_common_subsequence_dp(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)

    # dp[i][j] 表示 text1[0..i-1] 与 text2[0..j-1] 的 LCS 长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 从 i=1, j=1 开始填表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:          # 最后一个字符相同
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:                                      # 不同，取两种删除方式的最大值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # dp[m][n] 就是答案
    return dp[m][n]


# --- 空间优化版（只用一行） ---
def longest_common_subsequence_dp_optimized(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    # prev 保存上一行，curr 保存当前行
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr                     # 把当前行升格为下一次的上一行
    return prev[n]


# 示例
print(longest_common_subsequence_dp("abcde", "ace"))          # 3
print(longest_common_subsequence_dp_optimized("abc", "def")) # 0
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`，其中 `m = len(text1)`，`n = len(text2)`。  
  - 用大白话说，就是“把两个字符串的长度相乘”，如果两者都是 1000，最多算 1,000,000 次，计算机可以在几毫秒内完成。

- **空间复杂度**：  
  - 普通二维表：`O(m * n)`，需要 `m+1` 行 `n+1` 列的整数表格。  
  - 优化为一行：`O(n)`（只保存上一行），大幅降低内存，尤其当一段字符串很长时效果明显。

---

## 心得

- **核心技巧**：**动态规划**——把“大问题”拆成“子问题”，用表格记忆避免重复计算。  
- **适用的题型**（类似思路）  
  1. **Edit Distance（编辑距离）**：求把一个字符串变成另一个字符串的最少操作数。  
  2. **Maximum Subarray Sum（最大子序和）**的二维版本，如 **Maximum Sum Rectangle**。  
  3. **Distinct Subsequences**：计数有多少种方式可以得到目标子序列。  
- **一句话总结**：**“把两个字符串的每个前缀对应的最长公共子序列长度存下来，逐步填表，就能一次遍历得到答案”。**

---

## 反思

- **第一反应**：想到枚举子序列，写出暴力递归，随后意识到会超时。  
- **最容易踩的坑**  
  - **下标错误**：`dp` 多出一行一列，实际字符下标要减 1（`i-1`、`j-1`）。  
  - **边界初始化**：忘记把第一行、第一列设为 0，会导致访问未定义的值。  
  - **空间误用**：直接在同一行修改会覆盖掉 `dp[i-1][j-1]`，导致错误，使用两行或倒序遍历可以避免。  
- **下次遇到同类题**：第一步先**画状态转移表**，明确 `dp[i][j]` 表示的含义，再写出递推公式；如果表格太大，再考虑空间压缩。