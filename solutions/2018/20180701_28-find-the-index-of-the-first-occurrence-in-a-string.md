# #28. 在字符串中查找首次出现的索引 / Find the Index of the First Occurrence in a String

> 难度：简单 · 标签：Two Pointers、String、String Matching · [LeetCode 链接](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)

---

## 题目（英文原版）

**Description**

Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

**Examples**

**Example 1:**

```
Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
```

**Example 2:**

```
Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.
```

**Constraints**

- 1 <= haystack.length, needle.length <= 104
- haystack and needle consist of only lowercase English characters.

---

## 题目（中文翻译）

**题目描述**  
给定两个字符串 `needle` 和 `haystack`，返回 `needle` 在 `haystack` 中首次出现的索引。如果 `needle` 不在 `haystack` 中，则返回 `-1`。

**示例 1**  
**输入**: `haystack = "sadbutsad", needle = "sad"`  
**输出**: `0`  
**解释**: `"sad"` 在索引 `0` 和 `6` 处出现。首次出现位于索引 `0`，因此返回 `0`。

**示例 2**  
**输入**: `haystack = "leetcode", needle = "leeto"`  
**输出**: `-1`  
**解释**: `"leeto"` 未在 `"leetcode"` 中出现，所以返回 `-1`。

**约束条件**  
- `1 <= haystack.length, needle.length <= 10^4`  
- `haystack` 和 `needle` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **needle**（要找的子串）当成一把钥匙，**haystack**（大字符串）是一排锁。我们把锁从左到右依次尝试插入钥匙，看哪一个位置能够完整匹配。  

实现上可以：

1. 让指针 `i` 从 `0` 遍历到 `len(haystack) - len(needle)`，因为如果 `i` 超过这个范围，剩下的字符根本不够长装下 `needle`。  
2. 对每个 `i`，用另一个指针 `j` 同时遍历 `needle`，逐字符比较 `haystack[i+j]` 与 `needle[j]`。  
3. 如果所有字符都相等，就找到了第一个出现的位置，直接返回 `i`。  
4. 若遍历完所有可能的起始位置仍未匹配成功，返回 `-1`。

> **类比**：哈希表像是一本词典，`key` 是单词，`value` 是页码。这里我们没有使用词典，而是把每个起始位置当作“翻页”，逐页（字符）检查是否是我们要找的那一页。

这种方法一定能得到正确答案，因为它穷举了所有可能的起始位置并且每次都完整检查了一遍。

#### 代码（Python）

```python
def strStr_brute(haystack: str, needle: str) -> int:
    n, m = len(haystack), len(needle)

    # 特殊情况：空字符串按照约定返回 0
    if m == 0:
        return 0

    # i 为可能的起始下标，最多到 n-m
    for i in range(n - m + 1):
        # 假设从 i 开始匹配成功
        match = True
        for j in range(m):
            if haystack[i + j] != needle[j]:
                match = False      # 一旦发现不相等，立刻放弃本次 i
                break
        if match:                 # 所有字符都相等
            return i
    return -1                     # 没有找到任何匹配
```

#### 复杂度  

- **时间复杂度**：`O((n-m+1) * m)`，简写成 `O(n·m)`。  
  > 大白话：如果 `haystack` 长 1000，`needle` 长 100，那么最坏情况下我们要比较 1000‑100+1 ≈ 900 次起始位置，每次都要检查 100 个字符，约等于 90 000 次比较。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（指针 `i、j` 和布尔标记）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次匹配都从头开始比较**。当出现大量相同前缀时，会产生大量重复比较。例如 `haystack = "aaaaaa"`，`needle = "aaaab"`，暴力法会在每个位置都比较前四个 `'a'`，其实这些比较可以“记忆”下来，避免重复。

**KMP（Knuth–Morris–Pratt）算法** 正是为了解决这个问题而设计的。它的核心是：

1. **构造前缀函数（partial‑match table）**  
   对 `needle` 的每个前缀，记录它的最长相等的真前缀和真后缀的长度。  
   - 真前缀：不包括整个字符串本身的前缀。  
   - 真后缀：不包括整个字符串本身的后缀。  
   前缀函数告诉我们，当匹配失败后，指针应该“跳到” `needle` 的哪个位置继续比较，而不是回到开头。

2. **利用前缀函数在主串上滑动**  
   用两个指针 `i`（遍历 `haystack`）和 `j`（遍历 `needle`）。  
   - 若 `haystack[i] == needle[j]`，两指针都右移。  
   - 若不相等且 `j > 0`，把 `j` 直接跳到 `prefix[j‑1]`（即前缀函数告诉的下一个可能匹配位置），而 **`i` 不回退**。  
   - 若不相等且 `j == 0`，只移动 `i`（因为连第一个字符都不匹配）。

这样，每个字符在 `haystack` 和 `needle` 上最多被比较 **两次**，整体时间降到线性 `O(n + m)`。

> **类比**：想象在一本书里找一句话，如果每次只往后翻一页，一旦发现不匹配，就回到书的开头重新找，这就是暴力法。KMP 好比在每页的下方贴了“如果前面这几个字不匹配，应该直接跳到第几页继续找”，省掉了大量无效的翻页。

#### 代码（Python）

```python
def strStr_kmp(haystack: str, needle: str) -> int:
    n, m = len(haystack), len(needle)

    # 空 needle 按约定返回 0
    if m == 0:
        return 0

    # ---------- 1. 计算前缀函数 ----------
    # prefix[i] 表示 needle[0:i]（不含 i）最长相等的真前后缀长度
    prefix = [0] * m
    j = 0  # 当前匹配的长度

    for i in range(1, m):
        # 当字符不匹配时，利用已经算好的 prefix 回溯
        while j > 0 and needle[i] != needle[j]:
            j = prefix[j - 1]
        if needle[i] == needle[j]:
            j += 1
            prefix[i] = j
        # 若仍不匹配，prefix[i] 默认是 0

    # ---------- 2. 在 haystack 上滑动 ----------
    j = 0  # needle 的指针
    for i in range(n):
        # 失配时，利用前缀函数跳转
        while j > 0 and haystack[i] != needle[j]:
            j = prefix[j - 1]
        if haystack[i] == needle[j]:
            j += 1
            # 完全匹配
            if j == m:
                return i - m + 1   # 匹配的起始下标
        # else: j 为 0，继续向后扫描 i

    return -1   # 未找到
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`。  
  > 大白话：不管 `haystack` 多长，最多只遍历一次；`needle` 只需要一次预处理。整体比较次数和两个字符串长度之和成正比。  
- **空间复杂度**：`O(m)`。  
  > 只用了一个长度为 `needle` 的前缀数组来存储中间信息，和 `needle` 长度成正比。

---

## 心得  

- **核心技巧**：利用 **前缀函数**（或称 “部分匹配表”）实现 **KMP**，在失配时不回溯主串，只在模式串内部跳转。  
- **适用的题型**  
  1. 字符串匹配类（如 LeetCode 28 `strStr()`, 3 `Longest Substring Without Repeating Characters` 的滑动窗口思路）。  
  2. 多模式匹配（如 Aho‑Corasick）。  
  3. 在需要寻找重复子结构的 DP 或字符串压缩题目中，也常用前缀函数。  
- **一句话总结**：**“把失配的成本转移到模式串内部”**，这就是 KMP 的解题钥匙。

---

## 反思  

- **第一反应**：直接写双层循环遍历所有起始位置——这就是暴力解。  
- **最容易踩的坑**  
  - 忘记处理 `needle` 为空的情况（LeetCode 规定返回 0）。  
  - 在暴力循环中越界：起始下标只能到 `len(haystack) - len(needle)`。  
  - KMP 实现时，前缀函数的回溯写错导致死循环或错误的匹配位置。  
- **下次遇到同类题**：先判断是否需要 **线性时间**（字符串很长或会多次查询），若是，就立刻想到 **KMP / 前缀函数**；若规模不大，暴力解也可以先写出来验证思路。