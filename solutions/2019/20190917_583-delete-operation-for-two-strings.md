# #583. 删除两个字符串的操作 / Delete Operation for Two Strings

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/delete-operation-for-two-strings/)

---

## 题目（英文原版）

**Description**

Given two strings word1 and word2, return the minimum number of steps required to make word1 and word2 the same.
In one step, you can delete exactly one character in either string.

**Examples**

**Example 1:**

```
Input: word1 = "sea", word2 = "eat"
Output: 2
Explanation: You need one step to make "sea" to "ea" and another step to make "eat" to "ea".
```

**Example 2:**

```
Input: word1 = "leetcode", word2 = "etco"
Output: 4
```

**Constraints**

- 1 <= word1.length, word2.length <= 500
- word1 and word2 consist of only lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`，返回使两字符串相同所需的最少步骤数。  
在一次操作中，你可以在任意一个字符串中删除恰好一个字符。

**示例 1**  
**输入**  
```
word1 = "sea", word2 = "eat"
```  
**输出**  
```
2
```  
**解释**：第一步将 `"sea"` 删除字符得到 `"ea"`，第二步将 `"eat"` 删除字符得到 `"ea"`，共计 2 步。

**示例 2**  
**输入**  
```
word1 = "leetcode", word2 = "etco"
```  
**输出**  
```
4
```  

**约束条件**  
- `1 <= word1.length, word2.length <= 500`
- `word1` 和 `word2` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两串字符都枚举所有可能的删除方式**，然后找出让两串相等的最少删除次数。  
可以把每一次“删除一个字符”想象成在纸上把对应的字母划掉，最后只留下相同的字母序列。  

实现上，可以把 `word1` 的所有子序列（删掉若干字符得到的结果）和 `word2` 的所有子序列逐一比较，找到最长的公共子序列（Longest Common Subsequence，简称 LCS），因为保留下来的字符不需要再删除。  
- **数据结构**：这里用到的“子序列集合”可以想象成一本“字典”，键（key）是子序列的内容，值（value）是需要删除的字符数。  
- **正确性**：如果我们把两串都删到同一个子序列 `s`，那么删掉的字符数分别是 `len(word1)-len(s)` 与 `len(word2)-len(s)`，总步数为两者之和。要使步数最少，显然要让 `s` 尽可能长，也就是 LCS。

#### 代码（Python）

```python
from itertools import combinations

def all_subsequences(s: str):
    """
    生成字符串 s 的所有子序列（保持字符相对顺序）。
    用 itertools.combinations 取不同长度的下标组合，再拼接对应字符。
    """
    n = len(s)
    subs = set()
    # 选取 0~n 个字符的所有组合
    for r in range(n + 1):
        for idxs in combinations(range(n), r):
            # 根据下标顺序拼接字符，得到一个子序列
            subs.add(''.join(s[i] for i in idxs))
    return subs

def min_deletion_bruteforce(word1: str, word2: str) -> int:
    # 生成两串的所有子序列
    subs1 = all_subsequences(word1)
    subs2 = all_subsequences(word2)

    # 找出公共子序列中最长的那个
    longest_common = ''
    for s in subs1:
        if s in subs2 and len(s) > len(longest_common):
            longest_common = s

    # 删除步数 = 两串各自删掉的字符数
    return len(word1) - len(longest_common) + len(word2) - len(longest_common)

# 示例
print(min_deletion_bruteforce("sea", "eat"))       # 2
print(min_deletion_bruteforce("leetcode", "etco")) # 4
```

#### 复杂度  

- **时间复杂度**：`O(2^m + 2^n)`（其中 `m = len(word1)`，`n = len(word2)`）  
  解释：每个字符串的子序列数是 `2^长度`，我们要把两边的子序列全部枚举并放进集合，显然会非常慢。  
- **空间复杂度**：`O(2^m + 2^n)`  
  需要存储所有子序列，同样是指数级的空间。

> 在实际面试或线上评测里，这种暴力方法根本不可接受，只能用来帮助我们**理解**问题本质。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**核心是找最长公共子序列（LCS）**。  
只要知道 LCS 的长度 `L`，答案就等于：

```
删除总步数 = (len(word1) - L) + (len(word2) - L)
           = len(word1) + len(word2) - 2 * L
```

所以我们只要高效求出 LCS 长度即可。

**瓶颈**：暴力枚举子序列是指数级的。  
**优化**：使用**动态规划（Dynamic Programming）**，把“比较前 i 个字符和前 j 个字符的 LCS 长度”这个子问题记下来，避免重复计算。

---

#### 动态规划细节（从零解释）

1. **状态定义**  
   `dp[i][j]` 表示 `word1` 的前 `i` 个字符（即 `word1[:i]`）与 `word2` 的前 `j` 个字符（`word2[:j]`）的 LCS 长度。  
   - `i`、`j` 都从 `0` 开始，`0` 表示空串。

2. **状态转移**  
   - 若 `word1[i-1] == word2[j-1]`（最后一个字符相同），则这两个字符一定可以加入公共子序列，  
     `dp[i][j] = dp[i-1][j-1] + 1`。  
   - 否则，这两个字符不能同时出现在 LCS 中，只能把其中一个抛弃，取两种可能的最大值：  
     `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`。

3. **初始化**  
   当 `i == 0` 或 `j == 0` 时，空串与任意串的公共子序列长度都是 `0`，所以第一行和第一列全部为 `0`。

4. **求答案**  
   计算完所有 `dp[i][j]`，`dp[m][n]`（`m = len(word1)`，`n = len(word2)`）即为两串的 LCS 长度 `L`，随后套用公式得到最少删除步数。

5. **空间优化**（可选）  
   注意到 `dp[i][j]` 只依赖当前行的左边和上一行的同列值，实际上只需要两行滚动数组即可把空间从 `O(mn)` 降到 `O(min(m,n))`。这里先给出完整二维表的实现，随后给出压缩版代码。

#### 代码（Python）

```python
def min_distance(word1: str, word2: str) -> int:
    """
    动态规划求解两串的最长公共子序列长度 L，
    再根据公式返回最少删除步数。
    """
    m, n = len(word1), len(word2)

    # dp[i][j] 表示 word1[:i] 与 word2[:j] 的 LCS 长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填表格
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # 最后字符相同，可把它加入公共子序列
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 取抛弃 word1 最后字符或抛弃 word2 最后字符的较大值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_len = dp[m][n]                     # LCS 的长度
    return m + n - 2 * lcs_len             # 最少删除步数

# 示例
print(min_distance("sea", "eat"))       # 2
print(min_distance("leetcode", "etco")) # 4
```

**空间压缩版（仅用两行）**

```python
def min_distance_optimized(word1: str, word2: str) -> int:
    # 让 word1 为较短的字符串，减少空间占用
    if len(word1) > len(word2):
        word1, word2 = word2, word1
    m, n = len(word1), len(word2)

    prev = [0] * (n + 1)   # 上一行
    cur  = [0] * (n + 1)   # 当前行

    for i in range(1, m + 1):
        cur[0] = 0
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev, cur = cur, prev   # 交换角色，复用列表

    lcs_len = prev[n]
    return m + n - 2 * lcs_len
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`，其中 `m = len(word1)`，`n = len(word2)`。  
  解释：我们遍历了一个 `m × n` 的表格，每个格子只做了常数次比较和赋值。  
- **空间复杂度**：  
  - 完整表格实现：`O(m * n)`（需要存整个 DP 表）。  
  - 空间压缩实现：`O(min(m, n))`，只保留两行，极大降低内存占用。  

相较于暴力的指数级复杂度，DP 把时间从“天文数字”降到了“几千次”——在 500 长度限制下完全可接受。

---

## 心得

- **核心技巧**：把“最少删除使两串相同”转化为“求最长公共子序列”，再用动态规划求解。  
- **适用的题型**：  
  1. **编辑距离（Edit Distance）**——求最少插入/删除/替换，使两串相等。  
  2. **最长回文子序列（Longest Palindromic Subsequence）**——本质上是字符串自身与其逆序的 LCS。  
  3. **最小插入回文**——等价于 `len(s) - LPS`，同样使用 LCS 思路。  
- **一句话总结**：**把删除问题映射到 LCS，DP 是最直接的桥梁。**

---

## 反思

- **第一反应**：看到“删除字符”就想到“把两串删成相同的子序列”，于是自然联想到 LCS。  
- **最容易踩的坑**：  
  - 忽略空串的情况，导致索引越界。  
  - 在计算答案时忘记乘以 2（因为要把两串都删到 LCS），导致答案只算了一边的删除次数。  
  - DP 表的初始化不完整（第一行/列必须为 0），会让后面的转移公式出错。  
- **下次类似题的第一步**：先思考“是否可以把操作转化为子序列的保留/删除”，如果可以，立刻寻找 **最长公共子序列** 或 **最长递增子序列** 之类的子结构，随后用 DP 或贪心实现。