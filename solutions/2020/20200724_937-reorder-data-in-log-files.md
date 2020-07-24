# #937. 重新排列日志文件 / Reorder Data in Log Files

> 难度：中等 · 标签：Array、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/reorder-data-in-log-files/)

---

## 题目（英文原版）

**Description**

You are given an array of logs. Each log is a space-delimited string of words, where the first word is the identifier.
There are two types of logs:
Reorder these logs so that:
Return the final order of the logs.

**Examples**

**Example 1:**

```
Input: logs = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
Output: ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
Explanation:
The letter-log contents are all different, so their ordering is "art can", "art zero", "own kit dig".
The digit-logs have a relative order of "dig1 8 1 5 1", "dig2 3 6".
```

**Example 2:**

```
Input: logs = ["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
Output: ["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]
```

**Constraints**

- 1 <= logs.length <= 100
- 3 <= logs[i].length <= 100
- All the tokens of logs[i] are separated by a single space.
- logs[i] is guaranteed to have an identifier and at least one word after the identifier.

---

## 题目（中文翻译）

给定一个字符串数组 `logs`，其中每条日志都是由空格分隔的若干单词组成，**第一个单词是标识符（identifier）**。  
日志分为两类：

- **字母日志（letter-log）**：标识符后面的所有单词仅包含小写字母 `a‑z`。  
- **数字日志（digit-log）**：标识符后面的所有单词仅包含数字 `0‑9`。

请按以下规则重新排列这些日志，并返回最终的顺序：

1. 所有字母日志必须出现在数字日志之前。  
2. 字母日志之间需要 **先按内容（即标识符之后的单词）字典序排序**，若内容相同则 **按标识符字典序排序**。  
3. 数字日志保持原始相对顺序不变。

**返回** 重新排列后的日志数组。

---

**示例 1**

```text
Input: logs = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
Output: ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
Explanation:
字母日志的内容分别为 "art can"、"art zero"、"own kit dig"，按照字典序排列后顺序为 "art can"、"art zero"、"own kit dig"。  
数字日志保持原来的相对顺序，即 "dig1 8 1 5 1" 在前，"dig2 3 6" 在后。
```

**示例 2**

```text
Input: logs = ["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
Output: ["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]
```

---

**约束条件**

- `1 <= logs.length <= 100`
- `3 <= logs[i].length <= 100`
- `logs[i]` 的所有标记（token）均由单个空格分隔。
- 每条日志必包含一个标识符，且标识符后至少还有一个单词。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **遍历一次**，把所有日志分成两堆  
   - **字母日志（letter‑log）**：内容（标识符后面的部分）全部由字母组成。  
   - **数字日志（digit‑log）**：内容全部由数字组成。  
   把它们分别放进两个列表里。  
   这里的“列表”可以类比成我们平时用的**收纳盒**，一个盒子装字母日志，一个盒子装数字日志。

2. 对字母日志**手动排序**。  
   暴力的做法就是使用**冒泡排序**或**选择排序**——每次比较相邻的两条日志，决定谁应该在前面。  
   - 比较规则：先比较 **内容**（去掉标识符的那部分），内容相同再比较 **标识符**。  
   - 这一步可以想象成把所有字母日志排成一行，然后不断让“较大的”日志往后移动，直到所有日志都按顺序站好。

3. 最后把**排好序的字母日志**放在前面，再把**原始顺序的数字日志**接在后面，得到答案。

> **为什么正确？**  
> - 题目要求：字母日志必须排在数字日志前面，且字母日志之间按照内容字典序（若相同再按标识符），数字日志保持原有相对顺序。  
> - 我们把两类日志完全分开处理，分别满足了这两个要求，所以组合起来的结果必然符合题意。

#### 代码（Python）

```python
from typing import List

def reorderLogFiles_bruteforce(logs: List[str]) -> List[str]:
    # 1. 分离
    letter_logs = []   # 用来装字母日志的收纳盒
    digit_logs = []    # 用来装数字日志的收纳盒
    for log in logs:
        # 第一个空格前是标识符，后面的第一个字符决定日志类型
        identifier, rest = log.split(" ", 1)
        if rest[0].isalpha():          # 只要第一个字符是字母，就认定为字母日志
            letter_logs.append((identifier, rest, log))  # 同时保存完整原始字符串
        else:
            digit_logs.append(log)

    # 2. 暴力排序（冒泡）
    n = len(letter_logs)
    for i in range(n):
        for j in range(0, n - i - 1):
            id1, content1, raw1 = letter_logs[j]
            id2, content2, raw2 = letter_logs[j + 1]
            # 先比较内容，内容相同再比较标识符
            if (content1 > content2) or (content1 == content2 and id1 > id2):
                # 交换位置
                letter_logs[j], letter_logs[j + 1] = letter_logs[j + 1], letter_logs[j]

    # 3. 合并结果，只取原始字符串部分
    ordered_letter = [raw for _, _, raw in letter_logs]
    return ordered_letter + digit_logs
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  冒泡排序在最坏情况下需要比较 `n·(n-1)/2` 次（这里的 `n` 是字母日志的数量），所以时间会随日志数的平方增长。  
  用大白话说，如果日志有 100 条，最坏要比较 5,000 次左右。

- **空间复杂度**：`O(n)`  
  额外用了两个列表来保存字母日志和数字日志，最多保存全部日志的副本（每条日志存一次标识符、内容和原始字符串），随日志数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在排序环节**——我们用了 `O(n²)` 的冒泡排序。  
其实 Python 内置的 `list.sort()`（或 `sorted()`）实现了 **快速排序/归并排序的混合**，平均时间是 `O(n log n)`，并且是 **稳定排序**（相等元素会保持原有相对顺序），这正好满足题目对数字日志“保持原始顺序”的要求。

优化思路：

1. **一次遍历**把日志分成两类（同上），但不必自己实现排序，只把字母日志收集起来。
2. 对字母日志使用 Python 的 **自定义排序键**（`key` 参数），让排序过程自动按照  
   - **内容**（去掉标识符的部分）  
   - **标识符**（若内容相同）  
   的顺序比较。  
   这里的 `key` 就像是给每条日志贴上一个“排序标签”，排序时直接比较标签的大小。
3. 最后把排好序的字母日志和原始顺序的数字日志拼接。

> **核心概念——排序键（key）**  
> 想象我们要把学生按成绩排队，但成绩是隐藏在学生对象里的。我们可以先给每个学生贴一张纸条，上面写上他的成绩（`key`），再让大家按纸条上的数字排队。这样，实际比较的对象就是纸条上的数字，而不是完整的学生信息。

> **为什么稳定排序重要？**  
> 稳定排序保证“相等的”元素（这里指数字日志，因为我们把它们直接放在一个列表里不参与比较）在排序后仍保持原来的相对顺序。若使用不稳定的排序，数字日志可能被打乱顺序，违背题目要求。

#### 代码（Python）

```python
from typing import List

def reorderLogFiles(logs: List[str]) -> List[str]:
    # 1. 分离
    letter_logs = []   # 存放 (content, identifier, 原始日志) 三元组，方便后面排序
    digit_logs = []    # 原始字符串直接保存

    for log in logs:
        identifier, rest = log.split(" ", 1)
        if rest[0].isalpha():                     # 判定为字母日志
            # 为后续排序准备好“键”：先比较 rest（内容），再比较 identifier
            letter_logs.append((rest, identifier, log))
        else:
            digit_logs.append(log)

    # 2. 使用 Python 的稳定排序，按 (content, identifier) 排序
    #   这里的 key=lambda x: (x[0], x[1]) 正好对应题目要求的比较顺序
    letter_logs.sort(key=lambda x: (x[0], x[1]))

    # 3. 组合结果，只取原始日志字符串
    ordered_letter = [log for _, _, log in letter_logs]
    return ordered_letter + digit_logs
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  `n` 为日志总数。主要耗时在对字母日志的排序，Python 的 Timsort（基于归并/插入）在平均情况下是 `n log n`。相较于暴力的 `n²`，大幅提升。

- **空间复杂度**：`O(n)`  
  需要额外的列表保存分离后的日志以及排序时的临时空间（Timsort 会用到额外的 `O(n)` 辅助数组），整体随日志数量线性增长。

---

## 心得

- **核心技巧**：**自定义排序键 + 稳定排序**。  
  通过把“先比较内容、再比较标识符”包装成一个 `(content, identifier)` 的元组，交给语言自带的高效排序器完成工作。

- **适用场景**  
  1. LeetCode 937. Reorder Data in Log Files（本题）  
  2. LeetCode 179. Largest Number（把数字转成字符串后自定义比较规则）  
  3. LeetCode 1636. Sort Array by Increasing Frequency（先统计频次，再按 `(freq, value)` 排序）

- **一句话总结**：  
  “把要比较的规则抽象成一个键，让排序器帮你完成 O(n log n) 的高效排序”。  

---

## 反思

- **第一反应**：先手动把日志分成两类，然后想当然地用 `sorted()` 排序，却忘记了数字日志必须保持原顺序，导致第一次实现不通过。

- **最容易踩的坑**  
  - **判断日志类型**：只检查第一个字符是否是字母/数字即可，别把整个后缀都遍历。  
  - **稳定性**：如果使用不稳定的排序（如某些手写快速排序），数字日志相对顺序可能被打乱。  
  - **空格分割**：`split(" ", 1)` 必须只分一次，防止内容里出现多余空格被错误切割。

- **下次思路**：  
  看到“先分组、再排序、保持某类相对顺序”时，立刻想到 **“稳定排序 + 自定义键”**，先把不同组的元素分别收集，再交给语言自带的排序器处理。这样既简洁又高效。