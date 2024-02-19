# #2586. 统计区间内元音字符串的数量 / Count the Number of Vowel Strings in Range

> 难度：简单 · 标签：Array、String、Counting · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-vowel-strings-in-range/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of string words and two integers left and right.
A string is called a vowel string if it starts with a vowel character and ends with a vowel character where vowel characters are 'a', 'e', 'i', 'o', and 'u'.
Return the number of vowel strings words[i] where i belongs to the inclusive range [left, right].

**Examples**

**Example 1:**

```
Input: words = ["are","amy","u"], left = 0, right = 2
Output: 2
Explanation: 
- "are" is a vowel string because it starts with 'a' and ends with 'e'.
- "amy" is not a vowel string because it does not end with a vowel.
- "u" is a vowel string because it starts with 'u' and ends with 'u'.
The number of vowel strings in the mentioned range is 2.
```

**Example 2:**

```
Input: words = ["hey","aeo","mu","ooo","artro"], left = 1, right = 4
Output: 3
Explanation: 
- "aeo" is a vowel string because it starts with 'a' and ends with 'o'.
- "mu" is not a vowel string because it does not start with a vowel.
- "ooo" is a vowel string because it starts with 'o' and ends with 'o'.
- "artro" is a vowel string because it starts with 'a' and ends with 'o'.
The number of vowel strings in the mentioned range is 3.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 10
- words[i] consists of only lowercase English letters.
- 0 <= left <= right < words.length

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的字符串数组（array）`words`，以及两个整数 `left` 和 `right`。  
如果一个字符串的首字符和尾字符都是元音字符（vowel character），则称其为元音字符串（vowel string），其中元音字符包括 `'a'、'e'、'i'、'o'、'u'`。  
返回下标 `i` 属于闭区间（inclusive range）`[left, right]` 时，`words[i]` 为元音字符串的数量。

**示例 1**  
```text
Input: words = ["are","amy","u"], left = 0, right = 2
Output: 2
Explanation: 
- "are" 是元音字符串，因为它以 'a' 开头并以 'e' 结尾。
- "amy" 不是元音字符串，因为它的结尾不是元音。
- "u" 是元音字符串，因为它以 'u' 开头并以 'u' 结尾。
在给定区间内的元音字符串数量为 2。
```

**示例 2**  
```text
Input: words = ["hey","aeo","mu","ooo","artro"], left = 1, right = 4
Output: 3
Explanation: 
- "aeo" 是元音字符串，因为它以 'a' 开头并以 'o' 结尾。
- "mu" 不是元音字符串，因为它的开头不是元音。
- "ooo" 是元音字符串，因为它以 'o' 开头并以 'o' 结尾。
- "artro" 是元音字符串，因为它以 'a' 开头并以 'o' 结尾。
在给定区间内的元音字符串数量为 3。
```

**约束条件**  
- `1 <= words.length <= 1000`  
- `1 <= words[i].length <= 10`  
- `words[i]` 仅由小写英文字母组成。  
- `0 <= left <= right < words.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是 **把区间 `[left, right]` 里的每个单词都检查一遍**，看它的第一个字符和最后一个字符是否都是元音 (`a, e, i, o, u`)。  

- **用到的数据结构**：  
  - `list`（数组）存放所有单词。  
  - `set`（集合）存放五个元音字母，查找时相当于查字典：`key` 是字符，`value` 是是否在集合里，时间是 **O(1)**。  

- **为什么正确**：  
  只要遍历了区间内的每个单词，并对每个单词做了“首字符是元音 && 尾字符是元音”的判断，计数器加一即可。没有遗漏也没有多算，答案自然正确。  

- **时间/空间复杂度**（大白话解释）：  
  - **时间复杂度** `O(n)`：这里的 `n` 是区间长度 `right - left + 1`。想象你要检查 10 本书的封面和背面，检查每本书只花常数时间，总共花的时间和书的本数成正比。  
  - **空间复杂度** `O(1)`：只用了几个额外的变量（计数器、集合），不随输入规模增大而增多。  

#### 代码（Python）

```python
from typing import List

def vowel_strings(words: List[str], left: int, right: int) -> int:
    """
    统计区间 [left, right] 中，以元音字母开头且结尾的单词数量。
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}          # 元音集合，查找像查字典一样快
    count = 0                                   # 计数器

    # 逐个检查区间内的单词
    for i in range(left, right + 1):            # 包含 right 本身
        word = words[i]
        # 检查首字符和尾字符是否都是元音
        if word[0] in vowels and word[-1] in vowels:
            count += 1                          # 符合条件，计数加一

    return count
```

#### 复杂度  

- **时间复杂度**：`O(right - left + 1)` —— 只和要检查的单词个数有关，最多遍历整个数组（长度 ≤ 1000），所以最坏情况是 `O(n)`。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（集合、计数器），不随 `words` 长度变化。

---  

### 2. 最优解  

#### 思路  

对这道 **单次查询** 的题目，上面的暴力解已经是最优的 `O(n)` 线性时间。  
如果把问题稍微推广：**同一个数组会被多次查询不同的 `[left, right]` 区间**，我们就可以用**前缀和**把每次查询的时间降到 `O(1)`，只在预处理阶段花 `O(n)`。

**核心技巧：前缀和**  

- 先把每个单词是否是“元音串”转换成 `0/1` 的数组 `is_vowel[i]`（1 表示是，0 表示否）。  
- 构造前缀和 `pref[i]`，表示 `words[0..i-1]` 中元音串的数量。  
- 对任意查询 `[l, r]`，答案就是 `pref[r+1] - pref[l]`（左闭右开区间差），只需常数时间。

> 类比：把每本书的封面是否是元音看作“一颗星”，前缀和就是把从第一本到第 `i` 本的星星全部收集起来的总数。要知道第 `l` 到第 `r` 本之间有多少星，只要用“大盒子”里总星数减去“前面盒子”里的星数即可。

#### 代码（Python）

```python
from typing import List

def vowel_strings_prefix(words: List[str], left: int, right: int) -> int:
    """
    使用前缀和实现 O(1) 区间查询。
    适用于会有多次不同区间查询的场景。
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}

    # 1. 将每个单词是否是元音串映射为 0/1
    is_vowel = [1 if w[0] in vowels and w[-1] in vowels else 0 for w in words]

    # 2. 构造前缀和数组，pref[i] 表示前 i 个元素的和（i 为 0..n）
    pref = [0]                     # pref[0] = 0，方便左闭右开区间计算
    for val in is_vowel:
        pref.append(pref[-1] + val)   # 累加得到新的前缀和

    # 3. 区间查询：左闭右闭 => 使用左闭右开差值
    return pref[right + 1] - pref[left]
```

#### 复杂度  

- **时间复杂度**：  
  - 预处理阶段 `O(n)`（遍历一次数组，构造前缀和）。  
  - 单次查询 `O(1)`（只做两次数组取值和一次减法）。  
  与暴力解相比，如果只有一次查询，两者时间相同；若有 `q` 次查询，整体时间从 `O(q·n)` 降到 `O(n + q)`。  

- **空间复杂度**：`O(n)` 用于存放 `is_vowel` 与 `pref` 两个额外数组。若只做一次查询，可直接使用暴力解，省去这部分额外空间。

---  

## 心得  

- **核心技巧**：判断字符是否在集合中（常数时间）+ 前缀和快速区间求和。  
- **适用题型**：  
  1. “区间统计” 类题目，如统计区间内奇数个数、区间内满足某种属性的元素个数。  
  2. “前缀和” 常见于求区间和、区间最大子段和等。  
- **一句话总结解题钥匙**：**把“是否满足条件”抽象成 0/1，再用前缀和把多次区间查询变成 O(1)。**  

---  

## 反思  

- **第一反应**：看到“区间”和“计数”，直接想到遍历区间逐个检查，这是最自然的做法。  
- **最容易踩的坑**：  
  - 忘记 `right` 是 **闭区间**，导致 `range(left, right)` 少检查了最后一个元素。  
  - 当单词长度为 1 时，首字符和尾字符是同一个，需要同时检查，代码 `word[0]` 与 `word[-1]` 已经兼容，但如果写成 `word[1]` 就会越界。  
- **下次遇到同类题**：第一步先判断**是否只需要一次遍历**，若会有多次查询，再考虑**前缀和**或**树状数组**等更高效的数据结构。