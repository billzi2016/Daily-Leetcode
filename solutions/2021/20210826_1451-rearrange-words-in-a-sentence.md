# #1451. 重新排列句子中的单词 / Rearrange Words in a Sentence

> 难度：中等 · 标签：String、Sorting · [LeetCode 链接](https://leetcode.com/problems/rearrange-words-in-a-sentence/)

---

## 题目（英文原版）

**Description**

Given a sentence text (A sentence is a string of space-separated words) in the following format:
Your task is to rearrange the words in text such that all words are rearranged in an increasing order of their lengths. If two words have the same length, arrange them in their original order.
Return the new text following the format shown above.

**Examples**

**Example 1:**

```
Input: text = "Leetcode is cool"
Output: "Is cool leetcode"
Explanation: There are 3 words, "Leetcode" of length 8, "is" of length 2 and "cool" of length 4.
Output is ordered by length and the new first word starts with capital letter.
```

**Example 2:**

```
Input: text = "Keep calm and code on"
Output: "On and keep calm code"
Explanation: Output is ordered as follows:
"On" 2 letters.
"and" 3 letters.
"keep" 4 letters in case of tie order by position in original text.
"calm" 4 letters.
"code" 4 letters.
```

**Example 3:**

```
Input: text = "To be or not to be"
Output: "To be or to be not"
```

**Constraints**

- text begins with a capital letter and then contains lowercase letters and single space between words.
- 1 <= text.length <= 10^5

---

## 题目（中文翻译）

给定一个句子（sentence）`text`（句子是由空格分隔的单词组成的字符串），满足以下格式：首字母大写，其余均为小写字母，单词之间仅有一个空格。

你的任务是重新排列 `text` 中的所有单词，使它们按 **长度递增** 的顺序排列。若两个单词长度相同，则保持它们在原句中的相对顺序不变。返回重新排列后的新句子，格式同输入。

**示例 1**  
**输入**: `text = "Leetcode is cool"`  
**输出**: `"Is cool leetcode"`  
**解释**: 句子中有 3 个单词，分别是长度为 8 的 `"Leetcode"`、长度为 2 的 `"is"`、长度为 4 的 `"cool"`。输出按照长度排序，并且新的首单词首字母大写。

**示例 2**  
**输入**: `text = "Keep calm and code on"`  
**输出**: `"On and keep calm code"`  
**解释**: 输出的排序顺序如下：  
- `"On"` → 2 个字母  
- `"and"` → 3 个字母  
- `"keep"` → 4 个字母（长度相同的单词按原句中的位置保持顺序）  
- `"calm"` → 4 个字母  
- `"code"` → 4 个字母  

**示例 3**  
**输入**: `text = "To be or not to be"`  
**输出**: `"To be or to be not"`  

**约束条件**  
- `text` 以大写字母开头，随后全部为小写字母，单词之间仅有单个空格。  
- `1 <= text.length <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把句子拆成单词列表，然后用**两层循环**（比如冒泡排序）把单词按长度从小到大排好。  
- **拆分**：`text.split(' ')` 把句子按空格切开，得到 `["Leetcode", "is", "cool"]`。这一步类似把一本书的句子拆成一张张纸。  
- **排序**：对每一对单词 `i、j`（`i < j`），比较它们的长度。如果前面的单词比后面的长，就把它们交换位置。这里我们把 **位置** 当作“记忆”，所以即使长度相同，也会保持原来的先后顺序。  
- **大小写处理**：原句的第一个单词首字母是大写，后面的都是小写。排好序后，把所有单词先全部转成小写，再把第一个单词的首字母大写即可。  

这种做法之所以 **正确**，是因为冒泡排序会把较大的（这里指“长度更长的”）元素不断“冒”到后面，最终得到一个严格按照长度递增的序列。若两个单词长度相等，冒泡排序的 **稳定性**（相等元素保持原有相对顺序）正好满足题目要求。  

#### 代码（Python）  

```python
def rearrangeWords_brute(text: str) -> str:
    # 1. 把句子拆成单词列表
    words = text.split(' ')                     # ["Leetcode", "is", "cool"]
    
    # 2. 冒泡排序：按长度升序，长度相同保持原顺序（稳定）
    n = len(words)
    for i in range(n):
        for j in range(0, n - i - 1):
            # 如果前面的单词更长，需要交换
            if len(words[j]) > len(words[j + 1]):
                words[j], words[j + 1] = words[j + 1], words[j]

    # 3. 统一转成小写，除第一个单词外都保持小写
    words = [w.lower() for w in words]

    # 4. 把第一个单词的首字母大写
    words[0] = words[0].capitalize()

    # 5. 用空格拼回句子
    return ' '.join(words)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：我们用了两层循环，外层遍历 `n` 次，内层最多遍历 `n-1`、`n-2` … 次，总操作数大约是 `n*(n-1)/2`，这就是常说的 **平方级**，在 `n` 很大时会很慢。  
- **空间复杂度**：`O(n)`  
  解释：需要保存拆开的单词列表，列表本身占用 `n` 个单词的空间，除此之外只用了常数级别的临时变量。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，慢的地方在 **排序** 那一步：我们用了 `O(n²)` 的冒泡排序。  
实际上，**Python 的内置 `sorted` / `list.sort`** 使用的是 **Timsort**，它在最坏情况下是 `O(n log n)`，而且 **是稳定的**（相同键值的元素保持原来的相对顺序），完全符合“长度相同保持原序”的要求。  

优化步骤如下：  

1. **拆词**：同样使用 `split(' ')`。  
2. **统一小写**：先把所有单词转成小写，便于后面统一处理大小写。  
3. **稳定排序**：`sorted(words, key=len)` 按单词长度升序排序。因为 `sorted` 稳定，长度相同的单词会保持原来的相对位置。  
4. **首字母大写**：排序后把第一个单词的首字母改成大写，其余保持小写。  
5. **拼接**：`' '.join(...)` 得到最终句子。  

下面我们把这些步骤逐行写成代码，并在关键行加上中文注释。  

> **什么是“稳定排序”**  
> 想象一排排学生按身高排队，身高相同的同学如果原来站在前面，排好序后仍然站在前面，这就是“稳定”。在本题中，长度相同的单词要保持原来的出现顺序，使用稳定排序即可天然满足。  

#### 代码（Python）  

```python
def rearrangeWords(text: str) -> str:
    # 1. 拆分成单词列表
    words = text.split(' ')                     # ["Leetcode", "is", "cool"]
    
    # 2. 先把所有单词转成小写，统一处理大小写
    words = [w.lower() for w in words]          # ["leetcode", "is", "cool"]
    
    # 3. 稳定排序：按长度升序，长度相同保持原顺序（sorted 本身是稳定的）
    words_sorted = sorted(words, key=len)       # ["is", "cool", "leetcode"]
    
    # 4. 把排好序的第一个单词首字母大写
    words_sorted[0] = words_sorted[0].capitalize()
    
    # 5. 用空格把单词拼回句子
    return ' '.join(words_sorted)
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  解释：`sorted` 的核心是归并/插入相结合的 Timsort，最坏情况下需要 `n log n` 次比较和移动。相较于 `O(n²)`，在 `n` 达到几万甚至上百万时速度提升非常明显。  
- **空间复杂度**：`O(n)`  
  解释：除了原始单词列表外，`sorted` 会额外创建一个新的列表存放排序结果，大小同样是 `n`，加上少量临时变量，仍然是线性空间。  

---

## 心得  

- **核心技巧**：利用 **稳定排序** 按长度排序，同时保持原始相对顺序。  
- **适用的题型**  
  1. “按某个属性排序且相等时保持原序”——比如 **按年龄排序的学生名单**。  
  2. “把字符串或数组按自定义键值重新排列”——比如 **按字典序、出现频率、数值大小** 排序。  
- **一句话总结**：**“用内置稳定排序，关键在于把比较键设为长度”。**  

---

## 反思  

- **第一反应**：看到“按长度升序，长度相同保持原顺序”，立刻想到 **排序**，但要注意 **稳定性**。  
- **最容易踩的坑**  
  - 忘记把所有单词统一转成小写，导致首字母大小写不统一。  
  - 直接使用 `sorted(words, key=len, reverse=False)` 而不处理大小写，导致返回的句子首字母仍是小写。  
  - 对极端输入（只有一个单词）没有特殊处理，导致索引越界。  
- **下次遇到同类题**：第一步先 **拆分并统一格式**（大小写、空格），第二步考虑 **是否需要稳定排序**，再决定使用 **内置排序** 还是手写。