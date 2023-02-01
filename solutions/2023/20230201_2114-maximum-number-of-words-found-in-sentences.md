# #2114. **句子中出现的最大单词数** / Maximum Number of Words Found in Sentences

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-words-found-in-sentences/)

---

## 题目（英文原版）

**Description**

A sentence is a list of words that are separated by a single space with no leading or trailing spaces.
You are given an array of strings sentences, where each sentences[i] represents a single sentence.
Return the maximum number of words that appear in a single sentence.

**Examples**

**Example 1:**

```
Input: sentences = ["alice and bob love leetcode", "i think so too", "this is great thanks very much"]
Output: 6
Explanation: 
- The first sentence, "alice and bob love leetcode", has 5 words in total.
- The second sentence, "i think so too", has 4 words in total.
- The third sentence, "this is great thanks very much", has 6 words in total.
Thus, the maximum number of words in a single sentence comes from the third sentence, which has 6 words.
```

**Example 2:**

```
Input: sentences = ["please wait", "continue to fight", "continue to win"]
Output: 3
Explanation: It is possible that multiple sentences contain the same number of words. 
In this example, the second and third sentences (underlined) have the same number of words.
```

**Constraints**

- 1 <= sentences.length <= 100
- 1 <= sentences[i].length <= 100
- sentences[i] consists only of lowercase English letters and ' ' only.
- sentences[i] does not have leading or trailing spaces.
- All the words in sentences[i] are separated by a single space.

---

## 题目（中文翻译）

一个句子是由单词组成的列表，单词之间用单个空格分隔，且句子首尾没有空格。  
给定一个字符串数组 `sentences`，其中 `sentences[i]` 表示一条完整的句子。  
返回所有句子中单个句子所含单词数的最大值。

**示例 1**

> **Input:** `sentences = ["alice and bob love leetcode", "i think so too", "this is great thanks very much"]`  
> **Output:** `6`  
> **Explanation:**  
> - 第一句 `"alice and bob love leetcode"` 共 5 个单词。  
> - 第二句 `"i think so too"` 共 4 个单词。  
> - 第三句 `"this is great thanks very much"` 共 6 个单词。  
> 因此，单个句子中出现的最大单词数为 **6**。

**示例 2**

> **Input:** `sentences = ["please wait", "continue to fight", "continue to win"]`  
> **Output:** `3`  
> **Explanation:** 可能有多条句子包含相同数量的单词。  
> 在本例中，第二句和第三句（下划线部分）都包含 **3** 个单词。

**约束条件**

- `1 <= sentences.length <= 100`
- `1 <= sentences[i].length <= 100`
- `sentences[i]` 仅由小写英文字母和空格 `' '` 构成
- `sentences[i]` 的首尾没有空格
- `sentences[i]` 中的所有单词均由单个空格分隔

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**一句话里有多少个单词，就等于有多少个空格 + 1**。  
- **数据结构**：这里只需要遍历字符串本身，不需要额外的数据结构。可以把字符串想象成一串珠子，空格就是珠子之间的“分隔符”。每出现一次分隔符，就说明又多了一个单词。  
- **为什么正确**：题目保证  
  1. 句子没有前导或尾随空格；  
  2. 单词之间恰好只有一个空格。  
  在这种严格的格式下，空格的个数必然等于单词数减一。于是 **单词数 = 空格数 + 1**。  
- **时间/空间复杂度**：我们要对每个句子逐字符检查一次，最坏情况下要看完所有字符。  
  - 时间复杂度是 **O(N)**，其中 N 是 `sentences` 中所有字符的总数。  
  - 空间复杂度是 **O(1)**，只用了常数个额外变量（计数器），不随输入规模增长。

#### 代码（Python）  

```python
def mostWordsFound(sentences):
    """
    返回 sentences 中单句出现的最大单词数
    """
    max_cnt = 0                     # 记录目前看到的最大单词数
    for s in sentences:            # 逐个句子遍历
        # 统计句子中的空格个数，空格数 + 1 就是单词数
        space_cnt = 0
        for ch in s:                # 逐字符检查
            if ch == ' ':           # 遇到空格就计数
                space_cnt += 1
        word_cnt = space_cnt + 1    # 单词数 = 空格数 + 1
        max_cnt = max(max_cnt, word_cnt)   # 更新最大值
    return max_cnt
```

#### 复杂度  

- **时间复杂度：O(N)**  
  N 为所有句子字符总数。比如如果有 100 条句子，每条最长 100 个字符，最坏要检查 10,000 次字符。  
- **空间复杂度：O(1)**  
  只用了 `max_cnt、space_cnt、word_cnt` 这几个整数变量，和输入大小无关。

---  

### 2. 最优解  

#### 思路  
从上面的暴力思路可以看到，**核心工作只是统计空格数**。Python 已经为我们提供了非常便利的字符串方法 `split()`，它会把句子按照空格切分成若干子串（单词），并直接返回一个列表。  

- **为什么更快**：`split()` 在底层已经用 C 实现，速度比我们手写的逐字符循环要快得多。对使用者而言，它把“数空格再 +1”这一步合并成“一行代码”。  
- **核心算法**：遍历 `sentences`，对每个句子调用 `len(sentence.split())` 得到单词数，维护最大值即可。  
- **类比**：把 `split()` 想象成一把专门的“剪刀”，一次性把句子切成若干块（单词），我们只需要数数块有多少。

#### 代码（Python）  

```python
def mostWordsFound(sentences):
    """
    使用 str.split() 一行代码搞定单词计数，代码更简洁、运行更快。
    """
    max_cnt = 0
    for s in sentences:
        # split() 会返回所有单词组成的列表，len() 就是单词数
        word_cnt = len(s.split())
        max_cnt = max(max_cnt, word_cnt)   # 维护最大值
    return max_cnt
```

> **技巧提示**：如果你只想要最大值，还可以写成一行表达式  
> `return max(len(s.split()) for s in sentences)`  
> 但为了让初学者更易读，这里保留了循环结构。

#### 复杂度  

- **时间复杂度：O(N)**  
  与暴力解相同，仍需遍历所有字符，只是底层实现更高效。  
- **空间复杂度：O(M)**  
  `split()` 会临时创建一个列表保存所有单词，列表长度等于该句子的单词数。最坏情况下，单个句子长度为 100，单词数最多约 51（因为每两个字符之间至少有一个空格），所以额外空间仍然是 **线性**（相对于单句长度）且非常小。整体来看仍是 O(1) 级别的额外空间（不计入返回值本身）。

---

## 心得  

- **核心技巧**：利用字符串的 `split()` 方法把句子拆分为单词列表，再用 `len()` 计数。  
- **适用的题型**  
  1. 统计句子/段落中单词数量的题目（如 “统计句子中出现最多的单词”）。  
  2. 需要根据分隔符划分子串并统计子串数量的题目（如 “统计 CSV 行中字段个数”。）  
- **一句话总结**：**把“数空格 + 1”交给 `split()`，代码更简洁、速度更快**。

---

## 反思  

- **第一反应**：看到“单词之间用空格分隔”，立刻想到“数空格”。  
- **最容易踩的坑**  
  - 忘记题目保证没有前后空格和多余空格，直接用 `sentence.count(' ') + 1` 仍然是对的，但如果题目放宽限制，这种方法会出错。  
  - 对空字符串的处理：虽然约束保证每句至少有一个字符，但在实际面试中要考虑空句子的情况。  
- **下次遇到同类题**：第一步先 **确认分隔符的规则**（单个空格、多个空格、其它字符），然后决定是手动遍历计数还是直接使用语言提供的分割函数。