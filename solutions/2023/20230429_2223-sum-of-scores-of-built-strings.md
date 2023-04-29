# #2223. 构造字符串的分数之和 / Sum of Scores of Built Strings

> 难度：困难 · 标签：String、Binary Search、Rolling Hash、Suffix Array、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/sum-of-scores-of-built-strings/)

---

## 题目（英文原版）

**Description**

You are building a string s of length n one character at a time, prepending each new character to the front of the string. The strings are labeled from 1 to n, where the string with length i is labeled si.
The score of si is the length of the longest common prefix between si and sn (Note that s == sn).
Given the final string s, return the sum of the score of every si.

**Examples**

**Example 1:**

```
Input: s = "babab"
Output: 9
Explanation:
For s1 == "b", the longest common prefix is "b" which has a score of 1.
For s2 == "ab", there is no common prefix so the score is 0.
For s3 == "bab", the longest common prefix is "bab" which has a score of 3.
For s4 == "abab", there is no common prefix so the score is 0.
For s5 == "babab", the longest common prefix is "babab" which has a score of 5.
The sum of the scores is 1 + 0 + 3 + 0 + 5 = 9, so we return 9.
```

**Example 2:**

```
Input: s = "azbazbzaz"
Output: 14
Explanation: 
For s2 == "az", the longest common prefix is "az" which has a score of 2.
For s6 == "azbzaz", the longest common prefix is "azb" which has a score of 3.
For s9 == "azbazbzaz", the longest common prefix is "azbazbzaz" which has a score of 9.
For all other si, the score is 0.
The sum of the scores is 2 + 3 + 9 = 14, so we return 14.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

你一次构建一个字符，**在字符串的前面**（prepend）加入新字符，最终得到长度为 `n` 的字符串 `s`。  
这些中间得到的字符串按长度从 `1` 到 `n` 编号，长度为 `i` 的字符串记为 `s_i`。

`s_i` 的分数（score）定义为 `s_i` 与 `s_n`（即最终的完整字符串 `s`）之间**最长公共前缀**（longest common prefix）的长度（注意 `s == s_n`）。

给定最终的字符串 `s`，返回所有 `s_i` 的分数之和。

### 示例

#### 示例 1
```text
Input: s = "babab"
Output: 9
Explanation:
对于 s1 == "b"，最长公共前缀是 "b"，分数为 1。
对于 s2 == "ab"，不存在公共前缀，分数为 0。
对于 s3 == "bab"，最长公共前缀是 "bab"，分数为 3。
对于 s4 == "abab"，不存在公共前缀，分数为 0。
对于 s5 == "babab"，最长公共前缀是 "babab"，分数为 5。
所有分数相加得到 1 + 0 + 3 + 0 + 5 = 9。
```

#### 示例 2
```text
Input: s = "azbazbzaz"
Output: 14
Explanation:
对于 s2 == "az"，最长公共前缀是 "az"，分数为 2。
对于 s6 == "azbzaz"，最长公共前缀是 "azb"，分数为 3。
对于 s9 == "azbazbzaz"，最长公共前缀是 "azbazbzaz"，分数为 9。
其余 s_i 的分数均为 0。
分数之和为 2 + 3 + 9 = 14。
```

### 约束

- `1 <= s.length <= 10^5`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把题目转化一下：  
我们从左到右依次得到 `s1 , s2 , … , sn`，其中 `si` 是原字符串 `s` 的 **后缀**（因为每次都是在前面再加一个字符）。  
`score(si)` 定义为 `si` 与完整字符串 `s` 的最长公共前缀长度。

最直接的想法就是对每个后缀 `si`，把它和 `s` 从第一个字符开始逐字符比较，遇到不同的字符就停下来，比较的字符数就是它的分数。把所有分数加起来就是答案。

> **类比**：想象你有一本书 `s`，把书的最后几页（后缀）拿出来和整本书的开头对比，看能对齐多少页，逐页比对——这就是“暴力”做法。

为什么一定正确？  
因为我们把每个后缀都完整地和 `s` 对齐比较，必然能得到**最长**的公共前缀。

#### 代码（Python）

```python
def sum_of_scores_bruteforce(s: str) -> int:
    n = len(s)
    total = 0                     # 最终答案
    # i 表示后缀的起始位置（0‑based），对应题目中的 si（长度为 n-i）
    for i in range(n):
        cur = 0                    # 当前后缀与 s 的公共前缀长度
        # 从 s[i] 开始向后遍历，与 s[0:] 对比
        while i + cur < n and s[cur] == s[i + cur]:
            cur += 1               # 匹配成功，长度加 1
        total += cur               # 累加该后缀的得分
    return total
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  对每个后缀（最多 `n` 个）都可能遍历到整条字符串（最多 `n` 次），所以最坏情况下是 `n × n` 次比较。  
  大白话：如果字符串长 10 000，最差情况下要比较 100 000 000 次，明显太慢。

- **空间复杂度**：`O(1)`  
  只用了常数个额外变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

**暴力解的瓶颈**在于每次都从头重新比较，很多比较是重复的。  
例如字符串 `ababa…`，比较 `s2` 与 `s` 时已经知道前 2 个字符匹配，比较 `s3` 时前 3 个字符又会重复检查前 2 个字符。

我们需要一种一次扫描就能得到 **每个后缀** 与原串的最长公共前缀长度的方法。  
这正是 **Z‑algorithm**（或称 Z 函数）要解决的问题：

- 对于一个字符串 `t`（这里取 `t = s`），`Z[i]` 表示 `t[i:]`（从第 `i` 位开始的后缀）与 `t` 本身的最长公共前缀长度。  
- 注意：题目中的 `si` 正好是 `s[i-1:]`（因为 `i` 从 1 开始），所以 `score(si) = Z[i-1]`。

因此，只要一次线性时间计算出 `Z` 数组，所有分数即已得到，求和即可。

**Z‑algorithm 核心概念**  
我们维护一个区间 `[L, R]`，保证在这个区间内的字符 **与** 字符串开头完全相同（即 `s[L:R+1]` = prefix）。  
对每个位置 `i`：

1. 如果 `i > R`，说明 `i` 在已匹配区间之外，只能从头开始逐字符比较，得到 `Z[i]` 并可能更新 `[L,R]`。  
2. 如果 `i ≤ R`，则 `i` 落在已匹配区间内，利用已经知道的 `Z[i-L]`（即对应的“镜像位置”）来快速得到一个**下界** `k = min(Z[i-L], R-i+1)`。  
   - 若 `k` 已经把后缀匹配到区间右端，则仍需继续向右比较，得到更大的 `Z[i]` 并可能扩展 `[L,R]`。  
   - 否则 `Z[i] = k`，不必再比较。

整个过程只遍历一次字符串，时间 `O(n)`。

> **类比**：想象你已经在一段文字里找到了一个与开头完全相同的“大块”。当你站在这块里的一点 `i` 时，你可以直接把前面已经匹配好的长度搬过来，省去重复阅读的时间。

#### 代码（Python）

```python
def sum_of_scores(s: str) -> int:
    """
    使用 Z 算法一次线性扫描得到所有后缀与 s 的最长公共前缀长度，
    再求和返回。
    """
    n = len(s)
    Z = [0] * n          # Z[i] 对应后缀 s[i:] 与 s 的公共前缀长度
    l = r = 0            # 当前维护的匹配区间 [l, r]

    for i in range(1, n):   # Z[0] 按定义为 0（不计入答案）
        if i <= r:
            # i 在区间内，直接利用镜像位置的值
            Z[i] = min(r - i + 1, Z[i - l])
        # 无论上面是否已经得到 Z[i]，都要尝试继续向右扩展匹配
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        # 如果扩展后超过了 r，则更新区间
        if i + Z[i] - 1 > r:
            l, r = i, i + Z[i] - 1

    # Z[0] 实际上等于 n（整个字符串与自身的公共前缀），
    # 题目中 si (i=n) 的得分也应该是 n。
    total = n + sum(Z[1:])   # 把 Z[0] 用 n 替代后求和
    return total
```

> **关键行解释**  
- `Z = [0] * n`：创建长度为 `n` 的数组，初始全 0。  
- `if i <= r: Z[i] = min(r - i + 1, Z[i - l])`：利用已有匹配区间得到一个 **下界**，避免重复比较。  
- `while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:`：如果下界已经把区间右端逼到 `r`，继续往右比较，得到真正的 `Z[i]`。  
- `if i + Z[i] - 1 > r:`：更新维护的匹配区间，使后面的计算仍然可以利用它。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  每个字符最多被比较常数次（进入 `while` 循环的次数累计不超过 `2n`），所以整体线性。  
  与暴力的 `O(n²)` 相比，速度提升了 **指数级**（比如 `n=10⁵` 时，暴力不可行，线性算法轻松跑完）。

- **空间复杂度**：`O(n)`  
  需要额外存 `Z` 数组，大小和原字符串相同。若只要求和而不需要单个分数，理论上可以在计算时直接累加，进一步降到 `O(1)`，但 `O(n)` 已经足够小（约 400KB）。

---

## 心得

- **核心技巧**：Z‑algorithm（或等价的前缀函数）一次线性时间求出每个后缀与整体的最长公共前缀。  
- **适用题型**：  
  1. “所有前缀/后缀的匹配长度” 类问题（如 LeetCode 1063 *Number of Valid Subarrays* 中的前缀匹配）。  
  2. “字符串的重复/周期” 统计（如 1312 *Minimum Insertion Steps to Make a String Palindrome* 中的前缀‑后缀比较）。  
  3. “模式匹配的加速” 场景（如 KMP、Z‑algorithm 用于多模式搜索）。  
- **一句话总结解题钥匙**：把每个后缀视作“从某位置开始的子串”，利用 Z‑array 一次性得到它们与原串的最长公共前缀长度，避免重复比较。

---

## 反思

- **第一反应**：看到“后缀”和“最长公共前缀”，立刻想到 **前缀函数** 或 **Z‑algorithm**，因为它们本身就是为这类查询设计的。  
- **最容易踩的坑**：  
  - 忽略了 `s` 本身（`si` 当 `i = n`）的得分应该是 `n`，而 Z‑array 按定义 `Z[0] = 0`，需要手动加上。  
  - 在实现 Z‑algorithm 时忘记在 `i ≤ r` 情况下仍然要尝试 **向右继续匹配**（即 `while` 循环），导致得到的值仅是下界。  
  - 边界条件：空字符串不在约束范围，但若自行测试需防止 `while` 越界。  
- **下次类似题的第一步**：先判断“是否可以把所有查询转化为对同一字符串的前缀/后缀比较”，如果可以，立刻考虑使用 **Z‑array**（或 **KMP 前缀函数**）一次性预处理。这样常常能把原本的 `O(n²)` 降到 `O(n)`。