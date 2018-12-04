# #192. 单词频率 / Word Frequency

> 难度：中等 · 标签：Shell · [LeetCode 链接](https://leetcode.com/problems/word-frequency/)

---

## 题目（英文原版）

**Description**

Write a bash script to calculate the frequency of each word in a text file words.txt.
For simplicity sake, you may assume:
Example:
Assume that words.txt has the following content:
Your script should output the following, sorted by descending frequency:
Note:

**Examples**

**Example 1:**

```
the day is sunny the the
the sunny is is
```

**Example 2:**

```
the 4
is 3
sunny 2
day 1
```

---

## 题目（中文翻译）

编写一个 Bash 脚本，统计文本文件 `words.txt` 中每个单词的出现频次。  
为简化起见，你可以假设：

**示例**  
假设 `words.txt` 的内容如下：

示例 1:
```
the day is sunny the the
the sunny is is
```

你的脚本应按频次从高到低排序输出：

示例 2:
```
the 4
is 3
sunny 2
day 1
```

**注意：**  
- 只需统计单词本身的出现次数，不需要考虑标点或大小写差异。  
- 输出格式为 `单词 频次`，每行一个单词。  
- 结果按频次降序排列，频次相同的单词可以按任意顺序输出。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 把文件 `words.txt` 里的所有单词全部读进一个列表 `words`。  
2. 对列表中的每一个单词 `w`，再遍历一遍整个列表，统计 `w` 出现了多少次。  
3. 把统计结果放到另一个列表 `result`，最后按照出现次数从大到小排序并输出。

这里用到的唯一数据结构是 **列表**（Python 的 `list`），可以把它想象成一排排的书本，顺序固定但查找需要从头到尾翻。  

为什么这个方法能得到正确答案？因为我们对每一个单词都完整地检查了一遍整个文件，保证没有漏掉任何出现的次数。只要实现的循环没有写错，答案必然正确。

不过，这种做法的效率很低：如果文件里有 `n` 个单词，我们需要进行 `n` 次外层循环，每一次外层循环又要遍历 `n` 次内层循环，总共要做 `n × n = n²` 次比较。  

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
# 暴力实现：两层循环统计每个单词出现的次数

def word_frequency_brute(file_path: str):
    # 读取文件并按空格分割成单词列表
    with open(file_path, 'r', encoding='utf-8') as f:
        # strip() 去掉首尾换行，split() 按任意空白字符分割
        words = f.read().strip().split()

    # 用来保存每个单词对应的出现次数，格式是 [(word, count), ...]
    result = []

    # 外层遍历每一个单词
    for i in range(len(words)):
        w = words[i]
        # 如果已经在 result 里统计过，就跳过（避免重复统计）
        if any(w == pair[0] for pair in result):
            continue

        cnt = 0  # 计数器
        # 内层再次遍历整个列表，统计 w 出现的次数
        for j in range(len(words)):
            if words[j] == w:
                cnt += 1

        # 把 (单词, 次数) 加入结果列表
        result.append((w, cnt))

    # 按次数降序排序，次数相同的保持原有相对顺序
    result.sort(key=lambda x: x[1], reverse=True)

    # 输出
    for word, count in result:
        print(f"{word} {count}")


# 示例调用
if __name__ == "__main__":
    word_frequency_brute("words.txt")
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `n` 是文件中单词的总数。两层循环每层都要遍历 `n` 次，所以整体是 `n × n`。  
  - 用大白话说，就是如果文件里有 10,000 个单词，程序要做大约 1 亿 次比较，速度会很慢。

- **空间复杂度**：`O(n)`  
  - 需要存放所有单词的列表 `words`，以及最终的统计结果 `result`（最坏情况每个单词都不重复），所以占用的额外内存和单词数量成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次统计都要遍历整个列表。我们其实不需要重复遍历，只要在第一次看到单词时立刻把它的计数加 1，后面再遇到同一个单词时直接把计数加 1 就行。

这正是 **哈希表**（在 Python 中叫 `dict`）的用武之地：

- 哈希表可以把“单词”映射到“出现次数”。  
- 查找或更新一个键的时间是 **常数级**，也就是 `O(1)`，不随数据规模增长而变慢。  
- 可以把哈希表想象成一本“字典”，每个单词（key）对应一个页码（value），查找某个单词只需要直接翻到对应的页码，而不需要从头到尾遍历。

实现步骤：

1. 读取文件，得到单词列表（这一步和暴力解相同）。  
2. 创建空字典 `freq = {}`。  
3. 遍历单词列表，对每个单词 `w`：  
   - 如果 `w` 已经在字典里，`freq[w] += 1`；  
   - 否则，`freq[w] = 1`（首次出现）。  
4. 把字典的键值对转换成列表并按照出现次数降序排序。  
5. 按要求输出。

整个过程只遍历一次单词列表，时间从 `O(n²)` 降到了 `O(n)`，空间仍然是 `O(n)`（存放字典的大小）。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
# 最优实现：使用哈希表（dict）一次遍历统计频率

def word_frequency_optimal(file_path: str):
    # 读取文件并切分成单词列表
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().strip().split()

    # 哈希表：key 是单词，value 是出现次数
    freq = {}

    # 单次遍历，统计每个单词的次数
    for w in words:
        if w in freq:
            freq[w] += 1      # 已经出现过，次数加一
        else:
            freq[w] = 1       # 第一次出现，次数置为 1

    # 将字典转换为列表，并按次数降序排序
    # sorted 的 key 参数指定按照 value（即出现次数）排序，reverse=True 表示倒序
    sorted_items = sorted(freq.items(), key=lambda item: item[1], reverse=True)

    # 输出结果，格式 "单词 次数"
    for word, count in sorted_items:
        print(f"{word} {count}")


# 示例调用
if __name__ == "__main__":
    word_frequency_optimal("words.txt")
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次单词列表，字典的插入/查询是常数时间。  
  - 与暴力解相比，速度提升了 **指数级**（从 n² 降到 n）。

- **空间复杂度**：`O(n)`  
  - 需要保存所有不同单词及其计数，最坏情况下每个单词都不重复，空间仍然和单词数量成正比。  

---

## 心得

- **核心技巧**：利用哈希表（字典）实现“一遍遍历、一次统计”。  
- **适用的题型**：  
  1. 统计字符出现次数（如 “找出字符串中出现次数最多的字符”）。  
  2. 计数相同元素的对数（如 “两数之和出现次数”）。  
  3. 词频统计相关的文本处理题（如 “Top K Frequent Words”）。  
- **一句话总结**：**“出现频率统计＝哈希表 + 单遍历”。**

## 反思

- **第一反应**：直接想到把文件内容读进来，用两层循环逐个比较，虽然能得到答案，但会很慢。  
- **最容易踩的坑**：  
  - 忽略文件中可能出现的换行、制表符等空白字符，导致分词不完整。  
  - 没有对大小写统一处理（`The` 与 `the` 被视为不同单词）。  
  - 直接使用 `print` 输出时未加排序，导致结果顺序不符合要求。  
- **下次遇到同类题**：第一步先思考“是否可以用哈希表一次遍历完成计数”，如果可以，就直接走最优路径；如果不行，再考虑更复杂的数据结构或多遍遍历的方案。