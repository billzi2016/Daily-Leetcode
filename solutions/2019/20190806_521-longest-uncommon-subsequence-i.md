# #521. 最长不公共子序列 I / Longest Uncommon Subsequence I

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/longest-uncommon-subsequence-i/)

---

## 题目（英文原版）

**Description**

Given two strings a and b, return the length of the longest uncommon subsequence between a and b. If no such uncommon subsequence exists, return -1.
An uncommon subsequence between two strings is a string that is a subsequence of exactly one of them.

**Examples**

**Example 1:**

```
Input: a = "aba", b = "cdc"
Output: 3
Explanation: One longest uncommon subsequence is "aba" because "aba" is a subsequence of "aba" but not "cdc".
Note that "cdc" is also a longest uncommon subsequence.
```

**Example 2:**

```
Input: a = "aaa", b = "bbb"
Output: 3
Explanation: The longest uncommon subsequences are "aaa" and "bbb".
```

**Example 3:**

```
Input: a = "aaa", b = "aaa"
Output: -1
Explanation: Every subsequence of string a is also a subsequence of string b. Similarly, every subsequence of string b is also a subsequence of string a. So the answer would be -1.
```

**Constraints**

- 1 <= a.length, b.length <= 100
- a and b consist of lower-case English letters.

---

## 题目（中文翻译）

给定两个字符串 `a` 和 `b`，返回它们之间最长的不公共子序列（uncommon subsequence）的长度。如果不存在这样的不公共子序列，返回 `-1`。  
不公共子序列是指仅是 **其中一个** 字符串的子序列（subsequence），而不是两个字符串同时的子序列。

### 示例

**示例 1**  
```
Input: a = "aba", b = "cdc"
Output: 3
Explanation: 一个最长的不公共子序列是 "aba"，因为 "aba" 是字符串 "aba" 的子序列，但不是字符串 "cdc" 的子序列。
注意，"cdc" 也是一个最长的不公共子序列。
```

**示例 2**  
```
Input: a = "aaa", b = "bbb"
Output: 3
Explanation: 最长的不公共子序列有 "aaa" 和 "bbb"。
```

**示例 3**  
```
Input: a = "aaa", b = "aaa"
Output: -1
Explanation: 字符串 a 的每个子序列同时也是字符串 b 的子序列，反之亦然。因此答案为 -1。
```

### 约束条件

- `1 <= a.length, b.length <= 100`
- `a` 和 `b` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把两个字符串的所有子序列都列出来**，再逐一检查：

1. 生成字符串 `a` 的所有子序列（子序列可以看成“从原串中挑选若干字符，保持顺序不变”）。
2. 同理生成字符串 `b` 的所有子序列。
3. 把两套子序列分别放进集合（集合像字典的抽屉，只会保存不重复的元素）。
4. 对每一个只出现在 `a` 的子序列或只出现在 `b` 的子序列，记录它的长度，取最大的即可。

> **类比**：想象你有两本书，想找一本里出现而另一本里没有的最长句子。最笨的办法就是把每本书的所有句子写下来，再一一比对。

**为什么它是正确的**：  
只要遍历了**全部**子序列，就一定不会漏掉任何可能的“非公共子序列”。于是最大长度一定被找到了。

**时间/空间分析**：

- 对长度为 `n` 的字符串，子序列的数量是 `2^n`（每个字符保留或丢弃两种选择），所以生成子序列的时间是指数级的。
- 同时需要把这些子序列存进集合，最坏情况下也要占用 `2^n` 的空间。

用大白话解释：  
`O(2^n)` 就像“把所有可能的组合都尝遍”，当 `n=10` 时已经要检查 1024 条，`n=20` 时就要检查 1,048,576 条，显然不可接受。

#### 代码（Python）

```python
from itertools import combinations

def all_subsequences(s: str) -> set:
    """返回字符串 s 的所有子序列，使用集合去重"""
    subseqs = set()
    n = len(s)
    # 选取长度从 1 到 n 的所有组合
    for length in range(1, n + 1):
        for idxs in combinations(range(n), length):
            # 按照 idxs 的顺序拼接字符，得到一个子序列
            subseq = ''.join(s[i] for i in idxs)
            subseqs.add(subseq)
    return subseqs

def longest_uncommon_subsequence_bruteforce(a: str, b: str) -> int:
    # 生成两套子序列
    subs_a = all_subsequences(a)
    subs_b = all_subsequences(b)

    max_len = -1
    # 只在 a 中出现的子序列
    for s in subs_a:
        if s not in subs_b:
            max_len = max(max_len, len(s))
    # 只在 b 中出现的子序列
    for s in subs_b:
        if s not in subs_a:
            max_len = max(max_len, len(s))
    return max_len
```

#### 复杂度

- **时间复杂度**：`O(2^n + 2^m)`（`n = len(a)`, `m = len(b)`）——因为要枚举每个字符串的所有子序列，指数级增长。  
- **空间复杂度**：`O(2^n + 2^m)`——要把所有子序列存进集合，同样是指数级的。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的地方在于枚举所有子序列**。我们要思考：有没有办法直接判断最长的“非公共子序列”到底会是哪一个？

观察题目给出的 **Hint**：

- 如果 `a == b`，答案是 `-1`。因为两串完全相同，任意子序列在另一串里都能找到。
- 否则，答案就是较长的那条字符串本身的长度（或者直接取任意一条的长度），因为整条字符串肯定是它自己的子序列，而另一条字符串 **不可能** 包含这整条（因为两串不相等，长度相同的情况下字符必有不同，长度不同的情况下更明显）。

**关键点**：

- 子序列可以是原串的全部字符（即子序列等于原串本身）。  
- 只要两串不相同，**整条字符串本身必然是“只属于自己” 的子序列**，因为另一串里没有完整的那条字符串。  
- 所以最长的非公共子序列一定是较长的那条完整字符串，长度就是 `max(len(a), len(b))`。

> **类比**：两个人各自写了一段话，如果两段文字完全相同，那么找不到只出现一次的词；如果不相同，直接挑选更长的那段话，它肯定只属于自己。

#### 代码（Python）

```python
def longest_uncommon_subsequence(a: str, b: str) -> int:
    """
    最优解：只需要比较两串是否相同。
    - 相同 → 没有非公共子序列，返回 -1
    - 不同 → 较长的那条字符串本身就是答案，返回其长度
    """
    if a == b:
        return -1
    # 两串不相同，答案是较长的那条字符串的长度
    return max(len(a), len(b))
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做常数次比较和取长度操作，和字符串长度无关。相比暴力解的指数级，这就像“瞬间打开门”。
- **空间复杂度**：`O(1)` —— 只使用了极少的临时变量。

---

## 心得

- **核心技巧**：利用“子序列可以等于原串本身”这一事实，把问题转化为**是否存在完整字符串只出现一次**的判断。
- **适用的题型**：
  1. *Longest Uncommon Subsequence II*（需要在多字符串集合中找最长非公共子序列，思路类似但要遍历集合）。
  2. 判断两个集合是否完全相同，若不同则返回较大元素的某种度量（如长度、数值）。
  3. “只出现一次的最长子数组/子串”类问题，常常可以通过整体比较直接得出答案。
- **一句话总结**：**如果两串不相等，较长的那条本身就是最长的非公共子序列**。

## 反思

- **第一反应**：马上想到枚举所有子序列，写出暴力代码；这是一种安全但低效的直觉。
- **最容易踩的坑**：
  - 忘记考虑两串相等的情况，导致返回错误的长度而不是 `-1`。
  - 在实现暴力版时容易遗漏空子序列（题目要求非空），或者产生重复子序列导致错误的集合大小。
- **下次类似题的第一步**：先问自己“是否有可以直接作为答案的完整对象（整条字符串、整个数组）”，如果能直接判断是否唯一，则不必进入繁琐的枚举过程。