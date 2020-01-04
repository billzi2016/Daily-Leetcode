# #720. 字典中最长的单词 / Longest Word in Dictionary

> 难度：中等 · 标签：Array、Hash Table、String、Trie、Sorting · [LeetCode 链接](https://leetcode.com/problems/longest-word-in-dictionary/)

---

## 题目（英文原版）

**Description**

Given an array of strings words representing an English Dictionary, return the longest word in words that can be built one character at a time by other words in words.
If there is more than one possible answer, return the longest word with the smallest lexicographical order. If there is no answer, return the empty string.
Note that the word should be built from left to right with each additional character being added to the end of a previous word.

**Examples**

**Example 1:**

```
Input: words = ["w","wo","wor","worl","world"]
Output: "world"
Explanation: The word "world" can be built one character at a time by "w", "wo", "wor", and "worl".
```

**Example 2:**

```
Input: words = ["a","banana","app","appl","ap","apply","apple"]
Output: "apple"
Explanation: Both "apply" and "apple" can be built from other words in the dictionary. However, "apple" is lexicographically smaller than "apply".
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 30
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `words`，表示一个英文词典（Dictionary），返回 `words` 中可以**一次只添加一个字符**，并且每一步都对应词典中已经存在的单词，最终能够构成的最长单词。  
如果存在多个满足条件的单词，返回字典序（lexicographical order）最小的那个。若不存在符合要求的单词，返回空字符串 `""`。  
需要注意，构造过程必须从左到右进行，即每次在前一个单词的末尾追加一个字符。

**示例 1**  
``` 
Input: words = ["w","wo","wor","worl","world"]
Output: "world"
Explanation: 单词 "world" 可以通过 "w" → "wo" → "wor" → "worl" → "world" 的方式，一次添加一个字符构建完成。
```

**示例 2**  
``` 
Input: words = ["a","banana","app","appl","ap","apply","apple"]
Output: "apple"
Explanation: "apply" 和 "apple" 均可以由词典中的其他单词逐步构建。但在字典序上，"apple" 小于 "apply"，因此返回 "apple"。
```

**约束条件**  
- `1 <= words.length <= 1000`  
- `1 <= words[i].length <= 30`  
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每个单词检查它的所有前缀**（即去掉最后一个字符、再去掉、一直到只剩一个字符），看这些前缀是否都出现在原数组 `words` 中。  

- **使用的数据结构**：把 `words` 放进一个 **哈希表（Set）**，就像把所有单词写进一本字典，查找一个单词是否存在，只需要把它的“词条”丢进去查页码，时间几乎是 **O(1)**。  
- **为什么正确**：题目要求单词能够“一次加一个字符”地从左到右构造，也就是它的每个前缀都必须是字典里已有的单词。只要我们能把每个前缀都找得到，这个单词就满足条件。  
- **复杂度直观解释**：  
  - 对每个单词，我们最多要检查它的 `len(word)`（最多 30）个前缀。  
  - 如果有 `n` 个单词（最多 1000），最坏情况要检查 `n * max_len` 次查找。  
  - 每次查找在哈希表里是常数时间（想象打开字典直接定位页码），所以整体时间是 **O(n·L)**（L 为单词最大长度），在最坏情况下也可以写成 **O(n·L²)**（如果我们在每次检查前缀时都重新遍历字符串），这里我们采用更直观的 **O(n·L²)** 说明暴力的 “二次循环” 本质。  
  - 额外空间只用了存放哈希表的那部分，和原数组大小相同，记作 **O(n)**。

#### 代码（Python）
```python
from typing import List

def longestWord_bruteforce(words: List[str]) -> str:
    # 把所有单词放进集合，像字典一样快速查找
    word_set = set(words)

    best = ""                     # 记录当前找到的最长且字典序最小的单词
    for w in words:               # 逐个检查每个单词
        # 只要前缀都在集合里，这个单词就是候选
        all_prefixes_ok = True
        for i in range(1, len(w)):   # 检查 w[0:i]（不包括全词本身）
            prefix = w[:i]
            if prefix not in word_set:
                all_prefixes_ok = False
                break               # 一旦缺少前缀就不必继续检查

        if all_prefixes_ok:
            # 更新答案：更长的单词或者同长但字典序更小的单词
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w

    return best
```

#### 复杂度
- **时间复杂度**：`O(n * L²)`  
  - `n` 是单词数，`L` 是最长单词长度。  
  - 直观上可以想象：对每个单词我们要遍历它的每个字符（`L` 次），而每次检查前缀又要切片得到子串（`O(L)`），于是乘起来是 `L²`，再乘以 `n`。  
- **空间复杂度**：`O(n)`  
  - 只用了一个集合保存所有单词，大小和输入相同。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **每次都要遍历单词的所有前缀**。如果我们把单词 **按长度从小到大排好序**，就可以 **一次遍历** 完成检查：  

1. **先把所有单词放进集合**（同样是字典的概念）。  
2. **把单词按长度升序、字典序升序排列**。  
   - 长度小的单词一定先出现，只有当它已经在集合里时，才可能帮助构造更长的单词。  
   - 同长度时字典序小的排在前面，保证我们在长度相同的候选中选到字典序最小的。  
3. **从短到长遍历**：  
   - 对于长度为 1 的单词，直接加入候选集合 `valid`（因为没有前缀需要检查）。  
   - 对于长度 > 1 的单词，只要它的 **去掉最后一个字符的前缀** 已经在 `valid` 中，它就可以被加入 `valid`，并可能更新答案。  
   - 这里我们只检查 **一个前缀**（去掉最后一个字符），因为更短的前缀已经在之前的步骤里保证过了。  

这一步相当于 **动态规划**：`valid` 保存了所有已经确认可以“逐字符构造”的单词，后面的更长单词只需要看它的直接前缀是否在 `valid` 中即可。

**为什么比暴力更快**：  
- 每个单词只检查一次（而不是检查所有前缀），时间从 `O(L²)` 降到 `O(L)`。  
- 排序的代价是 `O(n log n)`，在 `n ≤ 1000` 的规模下完全可以接受。  

#### 代码（Python）
```python
from typing import List

def longestWord_optimal(words: List[str]) -> str:
    # 1. 把所有单词放进集合，快速查找
    word_set = set(words)

    # 2. 按长度升序、字典序升序排序
    #    长度小的先来，长度相同的字典序小的先来
    words.sort(key=lambda w: (len(w), w))

    best = ""            # 当前答案
    valid = set()        # 已经确认可以逐字符构造的单词

    for w in words:
        if len(w) == 1:                 # 长度为 1 的单词不需要前缀检查
            valid.add(w)
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
        else:
            # 只检查去掉最后一个字符后的前缀是否已经在 valid 中
            if w[:-1] in valid:
                valid.add(w)
                # 更新答案的条件同上
                if len(w) > len(best) or (len(w) == len(best) and w < best):
                    best = w

    return best
```

#### 复杂度
- **时间复杂度**：`O(n log n + n·L)`  
  - `O(n log n)` 来自排序（把单词排好顺序）。  
  - 遍历一次 `words`，每个单词只做常数次集合查找和切片（切片是 O(L)），所以是 `O(n·L)`。  
  - 与暴力的 `O(n·L²)` 相比，省掉了每个单词内部的二次循环。  
- **空间复杂度**：`O(n)`  
  - 需要额外的集合 `valid` 保存符合条件的单词，最坏情况下会和 `words` 同大小。  

---

## 心得

- **核心技巧**：**把问题转化为“从短到长逐步构造”，并利用哈希表快速判断前缀是否已出现**。这是一种**增量式验证**的思想，常用于“每一步都必须合法”的题目。  
- **适用的题型**  
  1. “最长的可递增子序列”类，需要先排序再逐步构造。  
  2. “单词接龙”或 “字典树（Trie）”相关的逐字符构造问题。  
  3. “最长的连续字符序列”需要先检查相邻元素是否满足条件。  
- **一句话总结解题钥匙**：**先把单词按长度排好，再用集合一步步验证“前缀是否已出现”。**  

---

## 反思

- **第一反应**：看到“每个前缀都要在字典里”，自然想到遍历每个单词的所有前缀，用集合查找。  
- **最容易踩的坑**  
  1. **字典序的处理**：当长度相同有多个符合条件的单词时，需要返回字典序最小的。排序时把字典序作为第二关键字即可。  
  2. **单字符单词的特殊性**：长度为 1 的单词没有前缀，需要单独加入 `valid`。  
  3. **切片的成本**：在暴力实现里频繁切片会导致额外的 `O(L)` 开销，最好只检查一次前缀（如 `w[:-1]`）。  
- **下次类似题的第一步**：先思考“是否可以把问题拆成‘从小到大’的递推”，如果可以，就先排序，然后用集合或哈希表保存已经验证通过的子结构。这样往往能把二次循环降到一次遍历。