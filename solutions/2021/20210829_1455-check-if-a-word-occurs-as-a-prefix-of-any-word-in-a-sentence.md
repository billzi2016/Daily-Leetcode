# #1455. 检查单词是否是句子中任意单词的前缀 / Check If a Word Occurs As a Prefix of Any Word in a Sentence

> 难度：简单 · 标签：Two Pointers、String、String Matching · [LeetCode 链接](https://leetcode.com/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/)

---

## 题目（英文原版）

**Description**

Given a sentence that consists of some words separated by a single space, and a searchWord, check if searchWord is a prefix of any word in sentence.
Return the index of the word in sentence (1-indexed) where searchWord is a prefix of this word. If searchWord is a prefix of more than one word, return the index of the first word (minimum index). If there is no such word return -1.
A prefix of a string s is any leading contiguous substring of s.

**Examples**

**Example 1:**

```
Input: sentence = "i love eating burger", searchWord = "burg"
Output: 4
Explanation: "burg" is prefix of "burger" which is the 4th word in the sentence.
```

**Example 2:**

```
Input: sentence = "this problem is an easy problem", searchWord = "pro"
Output: 2
Explanation: "pro" is prefix of "problem" which is the 2nd and the 6th word in the sentence, but we return 2 as it's the minimal index.
```

**Example 3:**

```
Input: sentence = "i am tired", searchWord = "you"
Output: -1
Explanation: "you" is not a prefix of any word in the sentence.
```

**Constraints**

- 1 <= sentence.length <= 100
- 1 <= searchWord.length <= 10
- sentence consists of lowercase English letters and spaces.
- searchWord consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个由单个空格分隔的句子（sentence），以及一个搜索单词 `searchWord`，判断 `searchWord` 是否是句子中某个单词的前缀（prefix）。  
返回满足条件的单词在句子中的索引（1-indexed）。如果 `searchWord` 是多个单词的前缀，返回最小的索引。如果不存在这样的单词，返回 `-1`。

**前缀（prefix）**：字符串 `s` 的前缀是 `s` 的任意一个连续的前导子串。

## 示例

### 示例 1
**输入**: `sentence = "i love eating burger"`, `searchWord = "burg"`  
**输出**: `4`  
**解释**: `"burg"` 是 `"burger"` 的前缀，而 `"burger"` 是句子中的第 4 个单词。

### 示例 2
**输入**: `sentence = "this problem is an easy problem"`, `searchWord = "pro"`  
**输出**: `2`  
**解释**: `"pro"` 是 `"problem"` 的前缀，出现在第 2 和第 6 个单词，但返回最小的索引 `2`。

### 示例 3
**输入**: `sentence = "i am tired"`, `searchWord = "you"`  
**输出**: `-1`  
**解释**: `"you"` 不是句子中任何单词的前缀。

## 约束条件

- `1 <= sentence.length <= 100`
- `1 <= searchWord.length <= 10`
- `sentence` 只包含小写英文字母和空格。
- `searchWord` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是：

1. **把句子拆成单词**。句子里单词之间只有一个空格，`split(' ')` 就像把一段文字按空格这把“剪刀”切开，得到一个列表。  
2. **逐个单词检查**：把每个单词的开头（即下标 0 开始的子串）和 `searchWord` 比较，看是否相同。这里的“前缀”可以想象成把 `searchWord` 放在单词的门口，如果正好能匹配上门口的那几块砖，那它就是前缀。  
3. **找到第一个匹配的单词就返回它的序号**（题目要求 1‑indexed），如果遍历完都没有匹配，则返回 `-1`。

> **为什么正确**  
> - 拆分得到的每个元素必定是原句子里的完整单词，未遗漏也不多余。  
> - 前缀的定义就是“从第一个字符开始的连续子串”，所以只要比较 `word[:len(searchWord)]` 与 `searchWord` 是否相等，就能完整判断。

> **复杂度分析（大白话）**  
> - **时间**：我们要看每个单词的前 `len(searchWord)` 个字符。设句子总长度为 `N`（包括空格），`searchWord` 长度为 `M`。最坏情况下我们会遍历所有字符一次，所以 **O(N)**。如果把 `N` 看成“句子里所有字符的数量”，那么 O(N) 就是“随字符多少线性增长”。  
> - **空间**：`split` 会产生一个单词列表，额外占用的空间与单词数大致相同，记作 **O(W)**（`W` 为单词数），在最坏情况下 `W ≤ N`，所以可以写成 **O(N)** 的额外空间。

#### 代码（Python）

```python
def is_prefix_of_word(sentence: str, searchWord: str) -> int:
    """
    暴力实现：逐个单词检查是否以 searchWord 为前缀
    """
    # 1. 按空格切分得到所有单词
    words = sentence.split(' ')          # 类似把句子用剪刀切成块

    # 2. 遍历每个单词，i 是 0‑based 下标，题目要 1‑based 所以最后返回 i+1
    for i, word in enumerate(words):
        # 取单词的前 len(searchWord) 个字符，与 searchWord 做比较
        if word[:len(searchWord)] == searchWord:
            return i + 1                 # 找到第一个就返回

    # 3. 全部遍历完都没有匹配，返回 -1
    return -1
```

#### 复杂度

- **时间复杂度**：`O(N)` — 句子里每个字符最多被查看一次。  
- **空间复杂度**：`O(N)` — `split` 产生的单词列表占用的额外空间。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是线性时间，但它**额外创建了一个单词列表**，这在空间上不是最省的。我们可以**边扫描句子边判断**，不需要把句子全部切开：

1. 使用 **双指针**：`i` 指向当前字符在句子中的位置，`j` 记录当前单词的起始位置。  
2. 当遇到空格或句子结束时，`i` 就指向了一个完整单词的结束位置。此时我们只需要比较这个单词的前缀，而不必把整个单词保存下来。  
3. 若匹配成功，立即返回当前单词的序号（用一个计数器 `idx` 记录已经遍历了多少个单词）。  
4. 若遍历完句子仍未找到匹配，则返回 `-1`。

> **核心技巧：双指针 + 在线前缀比较**  
> - **双指针**可以把“遍历 + 记起点”这两件事合二为一，就像在跑步时用一只脚标记起点，另一只脚走到终点再回头检查。  
> - **在线比较**只在必要时（即检查完一个单词时）才取子串进行比较，避免了对每个字符都做 `word[:len]` 的额外切片。

> **为什么更好**  
> - **省空间**：不需要存放所有单词，只用常数级别的变量 (`i, j, idx`)。  
> - **同样线性时间**：每个字符仍然只被访问一次。

> **复杂度分析（大白话）**  
> - **时间**：仍是 `O(N)`，因为我们只把句子从左到右走了一遍。  
> - **空间**：只有几个整数变量，**O(1)**，即“常数空间”，不随句子长度增长。

#### 代码（Python）

```python
def is_prefix_of_word(sentence: str, searchWord: str) -> int:
    """
    最优实现：不使用 split，使用双指针在原字符串上直接判断前缀
    """
    n = len(sentence)
    word_start = 0          # 当前单词的起始下标
    word_index = 1          # 单词的 1-indexed 编号

    i = 0
    while i <= n:           # i == n 时相当于在句子末尾多加一个“虚拟空格”
        # 当 i 到达空格或句子末尾时，说明一个单词结束
        if i == n or sentence[i] == ' ':
            # 只在单词长度 >= searchWord 长度时才比较前缀
            if i - word_start >= len(searchWord):
                # 直接比较切片，不需要额外拷贝整段单词
                if sentence[word_start:word_start + len(searchWord)] == searchWord:
                    return word_index
            # 准备处理下一个单词
            word_start = i + 1
            word_index += 1
        i += 1

    # 没有任何单词匹配前缀
    return -1
```

#### 复杂度

- **时间复杂度**：`O(N)` — 只遍历一次句子。  
- **空间复杂度**：`O(1)` — 只使用了几个整数变量，空间不随输入规模增长。

---

## 心得

- **核心技巧**：**双指针**（或称“滑动窗口”）配合**在线前缀比较**。  
- **适用的题型**：  
  1. “在字符串中查找单词是否为前缀/后缀”——如 LeetCode 1455（检查单词是否为前缀）。  
  2. “统计句子中满足某种模式的单词”——如统计包含特定子串的单词数。  
  3. “在不拆分的情况下遍历分隔符分割的序列”——如 CSV 行解析。  
- **一句话总结**：**“不必把整段文字拆开，边走边检查即可”**。

---

## 反思

- **第一反应**：直接 `split` 再遍历，写出最直观的代码。  
- **最容易踩的坑**：  
  - 忘记题目要求的 **1-indexed** 返回值，容易返回 0‑based。  
  - 当 `searchWord` 长度大于当前单词时直接比较会出错，需要先判断长度。  
  - 句子末尾没有空格时，需要在循环结束后额外处理最后一个单词（在最优解里通过 `i == n` 的 “虚拟空格” 解决）。  
- **下次类似题的第一步**：**先决定是要一次性拆分还是在原字符串上直接遍历**，依据空间要求和题目规模选择最合适的方式。