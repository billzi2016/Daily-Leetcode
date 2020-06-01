# #884. 两个句子中的不常见单词 / Uncommon Words from Two Sentences

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/uncommon-words-from-two-sentences/)

---

## 题目（英文原版）

**Description**

A sentence is a string of single-space separated words where each word consists only of lowercase letters.
A word is uncommon if it appears exactly once in one of the sentences, and does not appear in the other sentence.
Given two sentences s1 and s2, return a list of all the uncommon words. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: s1 = "this apple is sweet", s2 = "this apple is sour"
Output: ["sweet","sour"]
Explanation:
The word "sweet" appears only in s1 , while the word "sour" appears only in s2 .
```

**Example 2:**

```
Input: s1 = "apple apple", s2 = "banana"
Output: ["banana"]
```

**Constraints**

- 1 <= s1.length, s2.length <= 200
- s1 and s2 consist of lowercase English letters and spaces.
- s1 and s2 do not have leading or trailing spaces.
- All the words in s1 and s2 are separated by a single space.

---

## 题目（中文翻译）

**题目描述**  
句子（sentence）是由单个空格分隔的单词组成的字符串，且每个单词仅包含小写字母。  
如果一个单词（word）在两个句子中的出现次数恰好为一次，并且只出现在其中的一个句子里，则称其为**不常见**（uncommon）。  
给定两个句子 `s1` 和 `s2`，返回所有不常见单词组成的列表（list）。答案的顺序可以任意。

**示例 1**  
**输入**: `s1 = "this apple is sweet", s2 = "this apple is sour"`  
**输出**: `["sweet","sour"]`  
**解释**:  
单词 `"sweet"` 只出现在 `s1` 中，而单词 `"sour"` 只出现在 `s2` 中。

**示例 2**  
**输入**: `s1 = "apple apple", s2 = "banana"`  
**输出**: `["banana"]`  

**约束条件**  
- `1 <= s1.length, s2.length <= 200`  
- `s1` 和 `s2` 只包含小写英文字母和空格。  
- `s1` 与 `s2` 不含首尾空格。  
- `s1` 和 `s2` 中的所有单词均由单个空格分隔。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两句话的所有单词都列出来，**逐个统计**每个单词出现了多少次，然后挑出只出现一次且只在其中一句出现的单词。  
- **数据结构**：我们可以用 **哈希表（字典）** 来存放「单词 → 出现次数」的映射。哈希表就像一本**查字典**，把单词当作“词条”，对应的出现次数就是“页码”。查询、插入的时间都很快（平均 O(1)），所以非常适合统计频次。  
- **为什么正确**：题目要求“只出现一次且不在另一句话中”。如果我们把两句话的所有单词合并后统计次数，出现一次的单词必然满足这两个条件（因为出现一次意味着它只在某一句出现，另一句里根本没有）。  

#### 代码（Python）

```python
def uncommonFromSentences_brute(s1: str, s2: str):
    # 1️⃣ 把两句话按照空格拆成单词列表
    words = s1.split() + s2.split()          # 例如 ["this","apple","is","sweet","this","apple","is","sour"]

    # 2️⃣ 用字典统计每个单词出现的次数
    freq = {}                                 # 哈希表：单词 -> 次数
    for w in words:                           # 遍历所有单词
        freq[w] = freq.get(w, 0) + 1          # 若不存在则默认 0，再加 1

    # 3️⃣ 只保留出现一次的单词，即为不常见词
    ans = [w for w, cnt in freq.items() if cnt == 1]

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - `n` 为两句话总单词数。遍历一次拆词，遍历一次统计，都是线性时间。  
  - 大白话：如果总共有 1000 个单词，程序大概会跑 1000 步左右，和单词数量成正比。  

- **空间复杂度**：`O(m)`  
  - `m` 为不同单词的数量。字典里要保存每个不同单词一次。  
  - 大白话：如果所有单词都不重复，就要存 1000 条记录；如果全部相同，只需要 1 条记录。  

---

### 2. 最优解  

#### 思路  

暴力解已经是线性时间、线性空间，已经很高效。但我们可以把「统计」和「挑选」这两步合并，让代码更简洁，且 **只遍历一次** 两句话。思路如下：

1. **分别统计** s1、s2 中每个单词的出现次数（各自用哈希表）。  
2. **合并** 两个哈希表的结果：  
   - 如果一个单词只在 s1 出现一次且在 s2 完全不存在 → 加入答案。  
   - 同理，如果只在 s2 出现一次且在 s1 完全不存在 → 加入答案。  
3. 这样我们只需要 **两次遍历**（一次遍历 s1，一次遍历 s2），不需要把所有单词拼成一个大列表再遍历。  

核心数据结构仍是 **哈希表**，但这里用到 **两个** 哈希表来分别记录两句话的频次，思路类似“分治”。  

#### 代码（Python）

```python
def uncommonFromSentences_optimal(s1: str, s2: str):
    # 统计 s1 中每个单词的出现次数
    cnt1 = {}
    for w in s1.split():
        cnt1[w] = cnt1.get(w, 0) + 1

    # 统计 s2 中每个单词的出现次数
    cnt2 = {}
    for w in s2.split():
        cnt2[w] = cnt2.get(w, 0) + 1

    ans = []

    # 只在 s1 出现一次且不在 s2 出现的单词
    for w, c in cnt1.items():
        if c == 1 and w not in cnt2:        # 这里的 "not in" 相当于查字典，看是否有这个词条
            ans.append(w)

    # 只在 s2 出现一次且不在 s1 出现的单词
    for w, c in cnt2.items():
        if c == 1 and w not in cnt1:
            ans.append(w)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`（其中 `n` 为两句话总单词数）  
  - 只遍历了 s1 一遍、s2 一遍以及两次遍历各自的哈希表（哈希表大小 ≤ 单词数），总量仍是线性。  
  - 与暴力解相比，省去了把两个列表合并成一个大列表的额外拷贝，常数因子更小。  

- **空间复杂度**：`O(m1 + m2)`  
  - `m1`、`m2` 分别是 s1、s2 中不同单词的数量。相当于把两句话的不同单词分别存了一遍。  
  - 仍然是线性空间，最坏情况下（所有单词都不同）会是 `O(n)`。  

---

## 心得  

- **核心技巧**：利用哈希表统计频次，再通过“出现一次且另一边不存在”筛选不常见单词。  
- **适用的题型**  
  1. “出现一次的字符/单词”类（如 LeetCode 387 *First Unique Character in a String*）。  
  2. “两个集合的对称差”类（即只在一个集合出现的元素），例如 2445 *Number of Nodes With Value One*（思路类似）。  
- **一句话总结解题钥匙**：**“先把每句话的词频记下来，再把两边的词频交叉检查”。**  

---

## 反思  

- **第一反应**：看到“出现一次且不在另一句”，立刻想到“计数”。于是想用字典把所有单词的出现次数统计出来。  
- **最容易踩的坑**  
  - **空格处理**：直接 `split()` 能正确处理题目保证的单词之间只有一个空格的情况，但若有多余空格会产生空字符串，需要额外过滤。  
  - **重复单词**：如果同一句里出现多次（如 `"apple apple"`），必须确保只把出现一次的单词加入答案。  
  - **返回顺序**：题目说答案顺序任意，不需要额外排序。  
- **下次类似题的第一步**：**先把每个元素的出现次数用哈希表统计**，然后根据“出现次数==1 且不在另一集合”筛选。这样思路统一，代码也更清晰。