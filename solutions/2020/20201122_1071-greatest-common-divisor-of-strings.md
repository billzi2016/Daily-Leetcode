# #1071. 字符串的最大公约数 / Greatest Common Divisor of Strings

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/greatest-common-divisor-of-strings/)

---

## 题目（英文原版）

**Description**

For two strings s and t, we say "t divides s" if and only if s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times).
Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.

**Examples**

**Example 1:**

```
Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"
```

**Example 2:**

```
Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"
```

**Example 3:**

```
Input: str1 = "LEET", str2 = "CODE"
Output: ""
```

**Constraints**

- 1 <= str1.length, str2.length <= 1000
- str1 and str2 consist of English uppercase letters.

---

## 题目（中文翻译）

**题目描述**  
对于两个字符串 `s` 和 `t`，如果且仅如果 `s = t + t + t + … + t + t`（即 `t` 被连续拼接一次或多次），我们称 **“t 能整除 s”**（t divides s）。  
给定两个字符串 `str1` 和 `str2`，返回能够整除 `str1` 与 `str2` 的最长字符串 `x`。

**示例 1**  
输入: `str1 = "ABCABC", str2 = "ABC"`  
输出: `"ABC"`

**示例 2**  
输入: `str1 = "ABABAB", str2 = "ABAB"`  
输出: `"AB"`

**示例 3**  
输入: `str1 = "LEET", str2 = "CODE"`  
输出: `""`

**约束条件**  
- `1 <= str1.length, str2.length <= 1000`  
- `str1` 和 `str2` 仅由英文字母大写字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的公共子串都枚举一遍**，看哪一个既能完整拼出 `str1` 又能完整拼出 `str2`，并且长度最长。

- **子串是什么**？我们只关心 **前缀**（即从字符串开头开始的连续字符），因为如果一个字符串 `x` 能整除 `str1`，那么 `x` 必然是 `str1` 的前缀；同理也必须是 `str2` 的前缀。可以把前缀想象成一本书的“目录”，只有目录里的章节才能被完整重复。
- **枚举方式**：遍历长度 `l = 1 … min(len(str1), len(str2))`，取 `str1[:l]` 作为候选子串 `candidate`，先判断 `candidate` 能否把 `str1` 拼完整（即 `str1` 是否等于 `candidate` 重复若干次），再判断 `candidate` 能否把 `str2` 拼完整。满足两者的就记录下来，最后返回最长的那一个。

> 为什么这个方法一定能找到答案？因为我们把 **所有** 可能的前缀都检查了一遍，真正的最大公约子串肯定在其中。

#### 代码（Python）

```python
def gcd_of_strings_bruteforce(str1: str, str2: str) -> str:
    # 两个字符串的最短长度，枚举的上限
    max_len = min(len(str1), len(str2))
    answer = ""                     # 用来保存目前找到的最长公共子串

    # 从 1 到 max_len 逐个尝试每一种前缀长度
    for l in range(1, max_len + 1):
        candidate = str1[:l]        # 取 str1 的前 l 个字符作为候选子串

        # 判断 candidate 能否完整拼出 str1
        if len(str1) % l != 0:      # 长度不整除直接跳过
            continue
        if candidate * (len(str1) // l) != str1:
            continue

        # 判断 candidate 能否完整拼出 str2
        if len(str2) % l != 0:      # 长度不整除直接跳过
            continue
        if candidate * (len(str2) // l) != str2:
            continue

        # 上面全部通过，说明 candidate 同时整除 str1 与 str2
        answer = candidate          # 因为遍历是从短到长，直接覆盖即可

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - `n = min(len(str1), len(str2))`。我们要枚举 `1…n` 种长度，每一种都要做两次字符串乘法（实际是 `O(len)` 的拼接比较），所以总体是二次方级别。用大白话说，就是如果两个字符串长度都是 1000，最坏情况下要检查大约 1 000 000 次字符比较。
- **空间复杂度**：`O(1)`（不计输出字符串本身）  
  - 只用了常数级别的额外变量 `candidate`、`answer`，没有额外的数组或递归栈。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **大量的重复检查**：我们每次都把整个字符串重新拼接一遍。实际上，这道题可以用 **欧几里得算法**（求整数最大公约数的那套）来直接得到答案，关键观察如下：

1. **若 `str1` 与 `str2` 能共享同一个公共子串 `x`，则把两个字符串拼接起来的顺序必须相同**。  
   - 换句话说，`str1 + str2` 必须等于 `str2 + str1`。  
   - 这类似于把两根棍子拼在一起，如果它们的“基本模块”不一样，顺序换了自然会不匹配。

2. 当上述条件成立时，**最大公共子串的长度一定是两字符串长度的整数最大公约数（gcd）**。  
   - 想象把两根棍子切成最小的相同长度块，这个块的长度就是 `gcd(len1, len2)`。  
   - 因为 `x` 必须同时整除 `len1` 与 `len2`，所以它的长度只能是它们的公约数，而最大的自然是 `gcd`。

3. 因此，只要先检查 `str1 + str2` 与 `str2 + str1` 是否相等（若不相等直接返回空串），再取 `g = gcd(len(str1), len(str2))`，答案就是 `str1[:g]`。

> **欧几里得算法**是求两个整数最大公约数的经典方法：`gcd(a, b) = gcd(b, a % b)`，不断取余直到余数为 0。它的时间复杂度是 `O(log min(a, b))`，在本题中几乎可以忽略不计。

#### 代码（Python）

```python
import math

def gcd_of_strings(str1: str, str2: str) -> str:
    # 关键判断：若两字符串的拼接顺序不相同，则不可能有公共子串
    if str1 + str2 != str2 + str1:
        return ""                     # 直接返回空串

    # 计算两长度的整数最大公约数
    g = math.gcd(len(str1), len(str2))

    # 最大公共子串一定是 str1（或 str2）的前 g 个字符
    return str1[:g]
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 拼接比较 `str1 + str2` 与 `str2 + str1` 需要遍历两遍字符串，总共约 `2 * (len1 + len2)`，即线性时间。与欧几里得求 gcd 的 `O(log n)` 相比，整体仍是线性级别。相比暴力的 `O(n²)`，快了好几倍。
- **空间复杂度**：`O(1)`（不计输出）  
  - 只用了常数级别的变量 `g` 与临时拼接的字符串（Python 在内部会生成新字符串，但相当于 O(n) 的临时空间，仍然不随递归深度增长）。

---

## 心得

- **核心技巧**：利用**欧几里得算法**把“字符串的最大公约数”转化为“长度的最大公约数”，并通过**拼接相等性**判断是否真的存在公共子串。
- **适用场景**：  
  1. 本题的“字符串最大公约数”。  
  2. “循环数组的最小公共周期”问题（比如判断两个旋转序列是否同源）。  
  3. “两数的最小公倍数”类的字符串问题（如求最短能同时由两个字符串重复得到的字符串）。
- **一句话总结**：**把字符串问题抽象成整数的 gcd，先检查拼接一致性，再直接取前缀**。

---

## 反思

- **第一反应**：直接想到枚举所有前缀，写出暴力实现；因为最直观的思路总是“把所有可能都试一遍”。
- **最容易踩的坑**：  
  - 忽略 **长度必须整除** 的前提，导致在检查子串时出现 “ABC” 能整除 “ABCA” 之类的错误。  
  - 在最优解里忘记先判断 `str1 + str2 == str2 + str1`，直接返回前缀会在不匹配的情况下给出错误答案。
- **下次遇到同类题**：第一步先问自己——**“这两个对象是否可以视作同一种基本单元的重复？”**，如果答案是“可能”，就尝试 **“拼接相等性 + gcd 长度”** 的套路。这样往往能立刻把问题从枚举空间压缩到常数/对数级别。