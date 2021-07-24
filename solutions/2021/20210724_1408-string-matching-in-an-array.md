# #1408. 数组中的字符串匹配 / String Matching in an Array

> 难度：简单 · 标签：Array、String、String Matching · [LeetCode 链接](https://leetcode.com/problems/string-matching-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an array of string words, return all strings in words that are a substring of another word. You can return the answer in any order.

**Examples**

**Example 1:**

```
Input: words = ["mass","as","hero","superhero"]
Output: ["as","hero"]
Explanation: "as" is substring of "mass" and "hero" is substring of "superhero".
["hero","as"] is also a valid answer.
```

**Example 2:**

```
Input: words = ["leetcode","et","code"]
Output: ["et","code"]
Explanation: "et", "code" are substring of "leetcode".
```

**Example 3:**

```
Input: words = ["blue","green","bu"]
Output: []
Explanation: No string of words is substring of another string.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 30
- words[i] contains only lowercase English letters.
- All the strings of words are unique.

---

## 题目（中文翻译）

给定一个字符串数组（array）`words`，返回 `words` 中所有是另一字符串的子字符串（substring）的字符串。返回结果的顺序不限。

**示例 1**  
**输入**: `words = ["mass","as","hero","superhero"]`  
**输出**: `["as","hero"]`  
**解释**: `"as"` 是 `"mass"` 的子字符串，`"hero"` 是 `"superhero"` 的子字符串。`["hero","as"]` 也是一个有效答案。

**示例 2**  
**输入**: `words = ["leetcode","et","code"]`  
**输出**: `["et","code"]`  
**解释**: `"et"`、`"code"` 均是 `"leetcode"` 的子字符串。

**示例 3**  
**输入**: `words = ["blue","green","bu"]`  
**输出**: `[]`  
**解释**: 没有任何字符串是另一字符串的子字符串。

**约束条件**  
- `1 <= words.length <= 100`  
- `1 <= words[i].length <= 30`  
- `words[i]` 仅由小写英文字母组成。  
- `words` 中的所有字符串互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个单词拿出来，和数组里的其它所有单词逐个比较，看看它是不是别的单词的 **子串**（substring）。  
这里用到的唯一数据结构是 **列表（list）**，它就像我们平时写的“单词本”，把所有单词排成一行。  

判断“a 是 b 的子串”可以直接使用 Python 的 `in` 运算符：  

```python
if a in b:   # a 是 b 的子串
```

> 类比：`in` 就像在一本字典里查单词，字典的每一页对应一个更长的单词，找到了就说明它是子串。

只要遍历完所有 **(i, j)** 组合（i 为当前单词的下标，j 为要比较的另一个单词的下标），只要发现 `words[i] in words[j]` 就把 `words[i]` 加入答案即可。

#### 代码（Python）

```python
def stringMatching(words):
    """
    暴力解：两层循环遍历所有单词组合，检查子串关系
    """
    ans = []                     # 用来存放满足条件的单词
    n = len(words)
    for i in range(n):          # 第一个循环：选出要检查的单词
        for j in range(n):      # 第二个循环：与其它单词比较
            if i == j:
                continue        # 不能和自己比较
            # 如果 words[i] 是 words[j] 的子串，就把它加入答案
            if words[i] in words[j]:
                ans.append(words[i])
                break            # 已经找到匹配，后面不必再比较了
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² * L)`  
  - `n` 是数组长度，最多 100。  
  - `L` 是单词最长长度，最多 30。  
  - 两层循环产生 `n²` 次比较，每次子串检查最坏要遍历 `L` 个字符，所以整体是 `n² * L`。  
  - 用大白话说，就是“先挑每一对单词（大约 n² 次），再把短的单词的每个字符都和长的单词的字符比一次”。

- **空间复杂度**：`O(1)`（不计答案列表）  
  - 只用了常数个额外变量，答案本身是题目要求返回的，不算在额外空间里。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每一次都要遍历整个数组”**。如果我们先把单词按长度从短到长排好序，那么：

1. **短的单词只需要和更长的单词比较**，因为它不可能是更短或同长度单词的子串。  
2. 当我们在遍历时，一旦找到了匹配，就可以立即停止对该短单词的后续比较（因为已经确认它是子串）。  

这样可以把不必要的比较次数削减很多。实现细节如下：

- 把 `words` 按长度升序排序，得到 `sorted_words`。  
- 用两层循环，外层遍历每个 **短** 单词 `short_word`（从前往后），内层从它后面的 **长** 单词 `long_word` 开始比较。  
- 同样使用 `in` 判断子串关系，一旦匹配就把 `short_word` 加入答案并 `break`。

> 类比：想象把所有单词按身高从矮到高排成一排。我们要找“谁是别人的一部分”，只需要让矮的去看高的，而不必让高的去盯着矮的，因为高的本身不可能“藏在”矮的里面。

#### 代码（Python）

```python
def stringMatching(words):
    """
    优化解：先按长度排序，只比较短单词与更长单词的子串关系
    """
    # 1. 按长度升序排列，等价于把矮的排在前面
    sorted_words = sorted(words, key=len)

    ans = []                     # 保存答案
    n = len(sorted_words)

    for i in range(n):          # i 指向当前要检查的“短”单词
        short_word = sorted_words[i]
        # 只需要和后面的、更长的单词比较
        for j in range(i + 1, n):
            long_word = sorted_words[j]
            if short_word in long_word:   # 判断子串
                ans.append(short_word)
                break                     # 已经找到，停止内层循环
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² * L)`（最坏情况仍然是 n² 次比较）  
  - 虽然数量级看起来和暴力解相同，但实际比较的次数明显少于“每对都比较”。在多数随机数据下，短单词往往在很早的长单词就能匹配成功，`break` 会提前退出循环。  
  - 用大白话说，就是“我们把短的单词排在前面，只让它们去盯着后面的长单词，省掉了很多不必要的盯着短的或同长的单词的时间”。

- **空间复杂度**：`O(n)`  
  - 需要额外存放排好序的列表 `sorted_words`，长度为 `n`。答案列表 `ans` 也占 `O(k)`（k 为答案个数），这里算作输出空间。

---

## 心得

- **核心技巧**：**利用长度排序 + 只比较更长的单词**，把“不可能”的比较提前剔除。  
- **适用场景**：  
  1. **子串/子数组** 判断题（如 “找出数组中所有是其他数组子序列的数组”）。  
  2. **包含关系** 检测（如 “给定若干区间，找出被其他区间完全覆盖的区间”）。  
  3. **字符串/数组去重** 场景，常用 **排序 + 单指针** 思路。  
- **一句话总结**：**先把“短的”排前面，只让它们去找“更长的”，就能快速过滤掉无用比较**。

## 反思

- **第一反应**：直接两层循环暴力比较所有单词。  
- **最容易踩的坑**：  
  - 忘记排除 **自身**（`i == j`）导致误判。  
  - 对 **长度相等** 的单词也进行比较会产生冗余（因为相等长度的单词不可能相互包含，除非完全相同，但题目保证唯一）。  
  - 忽视 `break`，会把已经找到的短单词继续和后面的长单词比较，浪费时间。  
- **下次思路**：看到“子串/子集”这类关键词，第一步就想 **把元素按大小（长度）排序**，只在**可能的方向**上做比较，从而把不可能的情况提前剔除。