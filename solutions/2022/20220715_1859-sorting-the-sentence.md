# #1859. 排序句子 / Sorting the Sentence

> 难度：简单 · 标签：String、Sorting · [LeetCode 链接](https://leetcode.com/problems/sorting-the-sentence/)

---

## 题目（英文原版）

**Description**

A sentence is a list of words that are separated by a single space with no leading or trailing spaces. Each word consists of lowercase and uppercase English letters.
A sentence can be shuffled by appending the 1-indexed word position to each word then rearranging the words in the sentence.
Given a shuffled sentence s containing no more than 9 words, reconstruct and return the original sentence.

**Examples**

**Example 1:**

```
Input: s = "is2 sentence4 This1 a3"
Output: "This is a sentence"
Explanation: Sort the words in s to their original positions "This1 is2 a3 sentence4", then remove the numbers.
```

**Example 2:**

```
Input: s = "Myself2 Me1 I4 and3"
Output: "Me Myself and I"
Explanation: Sort the words in s to their original positions "Me1 Myself2 and3 I4", then remove the numbers.
```

**Constraints**

- 2 <= s.length <= 200
- s consists of lowercase and uppercase English letters, spaces, and digits from 1 to 9.
- The number of words in s is between 1 and 9.
- The words in s are separated by a single space.
- s contains no leading or trailing spaces.

---

## 题目（中文翻译）

**描述**  
一句话是由单个空格分隔的若干单词组成的字符串，且字符串首尾没有空格。每个单词仅包含小写或大写英文字母。  
可以通过在每个单词后附加其 **1-indexed**（从 1 开始计数）的位置编号，然后重新排列这些带编号的单词，来得到一个 **shuffled**（已打乱顺序）的句子。  
给定一个不超过 9 个单词的已打乱的句子 `s`，请恢复并返回原始句子。

**示例 1**  
**输入**: `s = "is2 sentence4 This1 a3"`  
**输出**: `"This is a sentence"`  
**解释**: 将单词按原始位置排序得到 `"This1 is2 a3 sentence4"`，随后去掉数字。

**示例 2**  
**输入**: `s = "Myself2 Me1 I4 and3"`  
**输出**: `"Me Myself and I"`  
**解释**: 将单词按原始位置排序得到 `"Me1 Myself2 and3 I4"`，随后去掉数字。

**约束条件**  
- `2 <= s.length <= 200`  
- `s` 只包含小写和大写英文字母、空格以及数字 `1` 到 `9`。  
- `s` 中的单词数在 `1` 到 `9` 之间。  
- 单词之间仅有单个空格分隔。  
- `s` 首尾没有空格。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把句子切成一个个单词，然后 **按照数字顺序把它们重新排好**。  
这里可以把每个单词想象成一张贴了标签的卡片，标签上写的是它在原句子里的位置（1、2、3…）。  
我们先把所有卡片收集到一个列表里，再用 **冒泡排序**（或任何你熟悉的 O(n²) 排序）把它们按照标签从小到大排列，最后把每张卡片后面的数字去掉，拼回一句话。

> **为什么这样一定能得到正确答案？**  
> 因为题目保证每个单词的末尾只会出现一次 1~9 之间的数字，且数字恰好表示原句子中该单词的第几位。只要把带数字的单词按照这个数字升序排列，去掉数字后得到的顺序必然就是原句子。

> **时间/空间复杂度大白话**  
> - **时间复杂度 O(n²)**：如果句子里有 n（最多 9）个单词，冒泡排序会比较每一对单词，最坏情况要比较 n·(n-1)/2 次，约等于 n² 次。想象你把所有卡片两两比较、交换，次数会很多。  
> - **空间复杂度 O(n)**：我们需要一个列表来保存切分后的单词，大小正好是单词数 n。

#### 代码（Python）

```python
def sortSentence_bruteforce(s: str) -> str:
    # 1. 把字符串按照空格拆成单词列表
    words = s.split()                     # 例: ["is2", "sentence4", "This1", "a3"]
    
    # 2. 冒泡排序——把带数字的单词按数字从小到大排好序
    n = len(words)
    for i in range(n):
        for j in range(0, n - i - 1):
            # 取每个单词最后一个字符，它就是位置编号（字符 '1'~'9'）
            pos_j = int(words[j][-1])
            pos_j1 = int(words[j + 1][-1])
            if pos_j > pos_j1:            # 如果前面的编号更大，就交换
                words[j], words[j + 1] = words[j + 1], words[j]

    # 3. 去掉每个单词最后的数字
    for k in range(n):
        words[k] = words[k][:-1]           # 只保留除最后一个字符外的部分

    # 4. 用空格把单词拼回一句话
    return " ".join(words)
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 冒泡排序需要两层循环，最坏情况下会比较 `n*(n-1)/2` 次。这里的 `n` 代表单词数（最多 9），所以实际运行很快，但从理论上讲是二次方增长。
- **空间复杂度**：`O(n)` —— 需要额外的列表存放拆分后的单词，列表大小随单词数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解我们已经看到，**瓶颈在排序**——我们用了 O(n²) 的冒泡排序。  
事实上，题目已经把每个单词的位置信息直接写在了单词的最后一个字符上，只要把这些信息取出来，就可以 **一次遍历直接放到正确的位置**，根本不需要比较或交换。

实现思路：

1. **拆词**：和暴力解一样，用空格把句子切成单词列表。  
2. **定位**：遍历每个单词，读取最后一个字符得到位置 `idx`（`int(word[-1])`），因为位置是从 1 开始的，我们把单词（去掉数字后）直接放进长度为 `n` 的结果数组的第 `idx-1` 个位置。  
   - 这里的结果数组相当于一本已经排好序的“笔记本”，我们把每张贴了编号的卡片直接贴到对应页码上。  
3. **拼接**：遍历完后，结果数组已经是原句子的顺序，直接用空格 `join` 成句子返回。

> **为什么一次遍历就能搞定？**  
> 因为每个单词的编号唯一且在 1~n 范围内，我们不需要比较大小，只要把它放到对应的下标就行。相当于把“排好队的学生”直接送到对应的座位上。

> **时间/空间复杂度大白话**  
> - **时间复杂度 O(n)**：只遍历一次单词列表，处理每个单词的时间是常数，整体随单词数线性增长。  
> - **空间复杂度 O(n)**：需要一个同样大小的数组来存放按顺序排列的单词，和单词数成正比。

#### 代码（Python）

```python
def sortSentence(s: str) -> str:
    # 1. 把句子切成单词
    words = s.split()                     # ["Myself2", "Me1", "I4", "and3"]
    n = len(words)

    # 2. 预先准备一个长度为 n 的空列表，用来按顺序存放单词（不带数字）
    ordered = [""] * n                     # ["", "", "", ""]

    # 3. 遍历每个单词，取出位置编号并放到对应下标
    for w in words:
        idx = int(w[-1]) - 1               # 最后一个字符是数字，转成 0‑based 下标
        ordered[idx] = w[:-1]              # 去掉数字，只保留单词本身

    # 4. 把有序的单词列表用空格拼成句子
    return " ".join(ordered)
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只进行一次遍历，`n` 为单词数（最多 9），几乎是瞬间完成。  
- **空间复杂度**：`O(n)` —— 需要额外的列表 `ordered` 来保存按顺序排列的单词，大小随单词数线性增长。

---

## 心得

- **核心技巧**：利用单词末尾的数字直接定位（**一次遍历直接放位**），省去排序的开销。  
- **适用的题型**：  
  1. **带位置信息的重排**（如 “把带编号的字符恢复原序”）。  
  2. **基于下标的线性重建**（如 “把数组中每个元素的目标位置已知，直接写入新数组”）。  
  3. **字符/单词后缀携带信息的题目**（如 “把每个单词后面的字母表示的颜色恢复”）。
- **一句话总结**：**把“编号”当成钥匙，一次遍历直接把卡片送到对应的座位**。

---

## 反思

- **第一反应**：看到每个单词后都有数字，立刻想到把它们 **排序**。  
- **最容易踩的坑**：  
  - 忘记把数字转成整数后再减 1，导致下标越界。  
  - 在去掉数字时误删了单词的最后一个字母（应只切除最后一个字符）。  
  - 忽视输入可能只有一个单词的极端情况。  
- **下次遇到同类题**：第一步先 **确认是否已有位置信息**，如果有，直接 **构造目标数组/字符串**，不要急着排序。