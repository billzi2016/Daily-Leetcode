# #2490. **循环句子** / Circular Sentence

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/circular-sentence/)

---

## 题目（英文原版）

**Description**

A sentence is a list of words that are separated by a single space with no leading or trailing spaces.
Words consist of only uppercase and lowercase English letters. Uppercase and lowercase English letters are considered different.
A sentence is circular if:
For example, "leetcode exercises sound delightful", "eetcode", "leetcode eats soul" are all circular sentences. However, "Leetcode is cool", "happy Leetcode", "Leetcode" and "I like Leetcode" are not circular sentences.
Given a string sentence, return true if it is circular. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: sentence = "leetcode exercises sound delightful"
Output: true
Explanation: The words in sentence are ["leetcode", "exercises", "sound", "delightful"].
- leetcode's last character is equal to exercises's first character.
- exercises's last character is equal to sound's first character.
- sound's last character is equal to delightful's first character.
- delightful's last character is equal to leetcode's first character.
The sentence is circular.
```

**Example 2:**

```
Input: sentence = "eetcode"
Output: true
Explanation: The words in sentence are ["eetcode"].
- eetcode's last character is equal to eetcode's first character.
The sentence is circular.
```

**Example 3:**

```
Input: sentence = "Leetcode is cool"
Output: false
Explanation: The words in sentence are ["Leetcode", "is", "cool"].
- Leetcode's last character is not equal to is's first character.
The sentence is not circular.
```

**Constraints**

- 1 <= sentence.length <= 500
- sentence consist of only lowercase and uppercase English letters and spaces.
- The words in sentence are separated by a single space.
- There are no leading or trailing spaces.

---

## 题目（中文翻译）

句子（sentence）是一串由单个空格分隔的单词（word），且首尾没有空格。  
单词仅由大小写英文字母组成，大小写字母视为不同字符。

如果满足以下全部条件，则该句子是循环的（circular）：

1. 对于句子中的每一对相邻单词，前一个单词的最后一个字符等于后一个单词的第一个字符。  
2. 最后一个单词的最后一个字符等于第一个单词的第一个字符。

例如，以下句子都是循环句子：

- `"leetcode exercises sound delightful"`
- `"eetcode"`
- `"leetcode eats soul"`

而下面的句子不是循环句子：

- `"Leetcode is cool"`
- `"happy Leetcode"`
- `"Leetcode"`
- `"I like Leetcode"`

给定一个字符串 `sentence`，如果它是循环的返回 `true`，否则返回 `false`。

---

**示例 1**

```text
Input: sentence = "leetcode exercises sound delightful"
Output: true
Explanation: 句子中的单词为 ["leetcode", "exercises", "sound", "delightful"]。
- "leetcode" 的最后一个字符等于 "exercises" 的第一个字符。  
- "exercises" 的最后一个字符等于 "sound" 的第一个字符。  
- "sound" 的最后一个字符等于 "delightful" 的第一个字符。  
- "delightful" 的最后一个字符等于 "leetcode" 的第一个字符。  
因此句子是循环的。
```

**示例 2**

```text
Input: sentence = "eetcode"
Output: true
Explanation: 句子中的单词为 ["eetcode"]。
- "eetcode" 的最后一个字符等于它的第一个字符。  
句子是循环的。
```

**示例 3**

```text
Input: sentence = "Leetcode is cool"
Output: false
Explanation: 句子中的单词为 ["Leetcode", "is", "cool"]。
- "Leetcode" 的最后一个字符不等于 "is" 的第一个字符。  
因此句子不是循环的。
```

---

**约束条件**

- `1 <= sentence.length <= 500`
- `sentence` 只包含大小写英文字母和空格。
- 单词之间仅有单个空格分隔。
- 句子首尾没有空格。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把句子拆成单词，然后逐个比较相邻两个单词的**首字母**和**尾字母**是否相等，最后再把**第一个单词的首字母**和**最后一个单词的尾字母**比较一遍。  

- **数据结构**：这里用到的唯一结构是 **列表（list）**，把 `sentence.split(' ')` 的结果存进去。可以把列表想象成一排排装好编号的盒子，盒子里装的是每个单词。  
- **正确性**：如果每一对相邻单词都满足“前一个的最后字符 == 后一个的第一个字符”，而且首尾也满足同样的条件，那么按照题意整句话就是“环形”。  
- **时间/空间复杂度**：  
  - 我们需要遍历所有单词一次，单词数记为 `n`，所以时间是 **O(n)**。这里的 `n` 实际上是句子里单词的个数，而不是字符串长度。  
  - 额外空间只用来存放拆分后的列表，大小也是 `n`，因此空间是 **O(n)**。  
  用大白话说，`O(n)` 就像“随单词数量线性增长”，单词多了，花的时间和空间就成正比增加。

#### 代码（Python）

```python
def isCircularSentence(sentence: str) -> bool:
    # 把句子按照空格拆成单词列表
    words = sentence.split(' ')          # ["leetcode", "exercises", "sound", "delightful"]
    
    # 逐对检查：前一个单词的最后一个字符 与 后一个单词的第一个字符
    for i in range(len(words) - 1):
        if words[i][-1] != words[i + 1][0]:   # -1 取最后一个字符，0 取第一个字符
            return False                     # 只要有一对不相等，直接返回 False
    
    # 最后检查首尾：最后一个单词的最后字符 与 第一个单词的第一个字符
    return words[-1][-1] == words[0][0]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 随着单词数线性增长，遍历一次即可得到答案。  
- **空间复杂度**：`O(n)` — 需要额外的列表来保存所有单词，列表的大小正好是单词数。  

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 **线性时间**，但它用了额外的 `list` 来存单词。如果我们只想 **常数级额外空间**（即 `O(1)`），可以直接在原字符串上一次遍历完成所有检查：

1. **记录第一个字符** `first_char = sentence[0]`，因为它会在最后和最后一个字符比较。  
2. 从左到右扫描字符串，遇到空格 `' '` 时，比较**空格前的字符**（即前一个单词的最后字符）和**空格后的字符**（即下一个单词的首字符）。如果不相等直接返回 `False`。  
3. 循环结束后，**比较最后一个字符** `sentence[-1]` 与 `first_char`，如果相等则整句话是环形。  

这样我们只用了几个临时变量（`first_char`、`i`），不需要额外的列表，空间降到 `O(1)`。核心技巧是**一次遍历**并**在遇到分隔符时即时比较**，类似于在河里捞木头时每捞到一根就立刻检查它是否合适。

#### 代码（Python）

```python
def isCircularSentence(sentence: str) -> bool:
    # 记录句子的第一个字符，稍后要和最后一个字符比较
    first_char = sentence[0]

    # i 从 1 开始遍历，避免和 first_char 重复比较
    i = 1
    while i < len(sentence):
        if sentence[i] == ' ':                     # 遇到空格，说明前后两个单词相邻
            # 前一个单词的最后字符是 i-1，后一个单词的首字符是 i+1
            if sentence[i - 1] != sentence[i + 1]:
                return False                       # 不相等直接返回 False
        i += 1

    # 循环结束后检查句子的首尾字符是否相等
    return sentence[-1] == first_char
```

#### 复杂度

- **时间复杂度**：`O(m)` — 只遍历一次原字符串，`m` 为句子长度（最多 500），与单词数相同数量级。相比暴力解，时间没有增加。  
- **空间复杂度**：`O(1)` — 只用了常数个临时变量，不依赖额外的存储结构。  
  与暴力解相比，空间从 `O(n)` 降到了 `O(1)`，在内存紧张的场景下更有优势。

---

## 心得

- **核心技巧**：一次遍历+即时比较（遇空格即检查前后字符），以及利用**首字符**与**末字符**的对应关系完成环形判定。  
- **适用题型**：  
  1. 需要检查相邻元素关系的字符串题目（如 “判断回文串是否每对字符相等”）。  
  2. 只用一次扫描即可得出结论的 “一次遍历” 类题目（如 “判断数组是否递增”）。  
- **一句话总结**：**把“相邻检查”搬到空格上做，省去拆词的额外空间**。

## 反思

- **第一反应**：看到“单词之间的首尾字符必须相等”，第一时间想到把句子 `split` 成单词列表再逐对比较。  
- **最容易踩的坑**：  
  - 忘记检查**首尾**的对应关系（第一个单词的首字符 vs 最后一个单词的尾字符）。  
  - 当句子只有一个单词时，仍需判断该单词首尾是否相同。  
  - 直接使用 `sentence[i+1]` 时要确保 `i+1` 不越界，最好在遍历时把范围控制好。  
- **下次第一步**：先明确“相邻关系”出现的**分隔符**（本题是空格），思考是否可以在遍历过程中**即时比较**，从而省去额外的数据结构。