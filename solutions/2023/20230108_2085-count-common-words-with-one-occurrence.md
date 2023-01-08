# #2085. 统计出现一次的公共单词 / Count Common Words With One Occurrence

> 难度：简单 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/count-common-words-with-one-occurrence/)

---

## 题目（英文原版）

**Description**

Given two string arrays words1 and words2, return the number of strings that appear exactly once in each of the two arrays.

**Examples**

**Example 1:**

```
Input: words1 = ["leetcode","is","amazing","as","is"], words2 = ["amazing","leetcode","is"]
Output: 2
Explanation:
- "leetcode" appears exactly once in each of the two arrays. We count this string.
- "amazing" appears exactly once in each of the two arrays. We count this string.
- "is" appears in each of the two arrays, but there are 2 occurrences of it in words1. We do not count this string.
- "as" appears once in words1, but does not appear in words2. We do not count this string.
Thus, there are 2 strings that appear exactly once in each of the two arrays.
```

**Example 2:**

```
Input: words1 = ["b","bb","bbb"], words2 = ["a","aa","aaa"]
Output: 0
Explanation: There are no strings that appear in each of the two arrays.
```

**Example 3:**

```
Input: words1 = ["a","ab"], words2 = ["a","a","a","ab"]
Output: 1
Explanation: The only string that appears exactly once in each of the two arrays is "ab".
```

**Constraints**

- 1 <= words1.length, words2.length <= 1000
- 1 <= words1[i].length, words2[j].length <= 30
- words1[i] and words2[j] consists only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串数组 `words1` 和 `words2`，返回在这两个数组中 **各出现一次** 的字符串的数量。

**示例 1：**  
**输入：** `words1 = ["leetcode","is","amazing","as","is"], words2 = ["amazing","leetcode","is"]`  
**输出：** `2`  
**解释：**  
- `"leetcode"` 在两个数组中各出现一次，我们计入该字符串。  
- `"amazing"` 在两个数组中各出现一次，我们计入该字符串。  
- `"is"` 虽然在两个数组中都有出现，但在 `words1` 中出现了两次，因此不计入。  

**示例 2：**  
**输入：** `words1 = ["b","bb","bbb"], words2 = ["a","aa","aaa"]`  
**输出：** `0`  
**解释：** 两个数组中没有任何字符串同时出现一次。  

**示例 3：**  
**输入：** `words1 = ["a","ab"], words2 = ["a","a","a","ab"]`  
**输出：** `1`  
**解释：** 唯一满足条件的字符串是 `"ab"`，它在两个数组中各出现一次。  

**约束条件：**  
- `1 <= words1.length, words2.length <= 1000`  
- `1 <= words1[i].length, words2[j].length <= 30`  
- `words1[i]` 和 `words2[j]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两边的单词一个一个拿出来比较：

1. 对 `words1` 中的每个单词 `w`，统计它在 `words1` 里出现了多少次（遍历 `words1` 计数），同理统计它在 `words2` 里出现了多少次（遍历 `words2` 计数）。  
2. 如果这两个计数都恰好等于 1，就说明 `w` 满足 “在两个数组里各出现一次”，答案加一。  

这里用到的 **哈希表**（在 Python 里叫 `dict`）可以类比为一本字典：**key** 是单词，**value** 是这个单词出现的次数。查一次字典就能立刻得到出现次数，就像在字典里找词条的页码一样快。

这种做法一定能得到正确答案，因为我们把所有可能的单词都检查了一遍，并且只在出现次数恰好为 1 时计数。

#### 代码（Python）

```python
def countWords_bruteforce(words1, words2):
    # 统计 words1 中每个单词出现的次数
    cnt1 = {}
    for w in words1:
        cnt1[w] = cnt1.get(w, 0) + 1   # 如果 w 之前没出现过，就默认 0 再加 1

    # 统计 words2 中每个单词出现的次数
    cnt2 = {}
    for w in words2:
        cnt2[w] = cnt2.get(w, 0) + 1

    ans = 0
    # 对 words1 的每个不同单词都检查一次
    for w in cnt1:
        # 只要两边都恰好出现一次，就计数
        if cnt1[w] == 1 and cnt2.get(w, 0) == 1:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * m)`（伪代码）  
  实际上我们遍历了两遍数组（`len(words1) + len(words2)`），再遍历一次 `cnt1` 的键集合。因为每一步都是线性的，整体是 `O(n + m)`，这里的 `n`、`m` 分别是两个数组的长度。  
  大白话：如果两个数组各有 1000 个单词，程序大概要跑 2000 次左右的简单操作，算得上“快”。

- **空间复杂度**：`O(u1 + u2)`  
  需要额外的哈希表来存每个单词的计数，`u1`、`u2` 分别是两个数组里不同单词的数量。最坏情况下每个单词都不相同，空间就是 `O(n + m)`。

---

### 2. 最优解

#### 思路  

暴力解已经是线性时间了，已经很快。但我们可以把代码写得更简洁、一步到位，避免两次遍历两次哈希表的过程。

**瓶颈**：在暴力解里，我们先分别统计 `words1`、`words2` 的出现次数，然后再遍历 `cnt1` 去检查。其实这一步可以合并：只要我们把两次计数的结果放进同一个哈希表，再一次遍历就能得到答案。

**优化思路**：

1. 用一个哈希表 `freq` 记录 **所有** 单词在两个数组里出现的次数。为了区分是来自第一个数组还是第二个数组，我们可以把计数写成 `freq[w] = (cnt_in_words1, cnt_in_words2)` 的二元组，或者更简单地先统计两次，再一次遍历检查。这里我们采用 **两次计数后一次遍历** 的方式，仍然是 `O(n+m)`，但代码更紧凑。

2. 具体实现：  
   - 第一次遍历 `words1`，把每个单词的计数加到 `freq[w][0]`（即第一个位置）。  
   - 第二次遍历 `words2`，把每个单词的计数加到 `freq[w][1]`（即第二个位置）。  
   - 最后遍历 `freq` 的键，只要两个计数都恰好为 1，就把答案加一。

3. 这里的 **二元组** 可以用 `list` `[c1, c2]` 来存，方便在遍历时直接修改。

**核心数据结构**：哈希表 + 小数组（长度为 2），相当于“字典里装了两格小记事本”，专门用来记录每个单词在两个来源中的出现次数。

#### 代码（Python）

```python
def countWords_optimal(words1, words2):
    # freq[w] = [在 words1 中的次数, 在 words2 中的次数]
    freq = {}

    # 统计 words1
    for w in words1:
        if w not in freq:
            freq[w] = [0, 0]        # 第一次出现时，先创建两格记事本
        freq[w][0] += 1            # 第 0 格记录 words1 的计数

    # 统计 words2
    for w in words2:
        if w not in freq:
            freq[w] = [0, 0]        # 同上，保证每个单词都有两格
        freq[w][1] += 1            # 第 1 格记录 words2 的计数

    # 统计满足“各出现一次”的单词数量
    ans = 0
    for w, (c1, c2) in freq.items():
        if c1 == 1 and c2 == 1:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  只遍历了两遍数组（每个元素一次）再遍历一次哈希表的键。相当于把所有工作压在一次线性扫描里。和暴力解的时间复杂度相同，但常数更小，实际运行更快。

- **空间复杂度**：`O(u)`  
  只需要一个哈希表来保存所有不同单词的信息，`u` 是两个数组中不同单词的总数。与暴力解的空间使用相同，但只用了一个表，代码更简洁。

---

## 心得

- **核心技巧**：利用哈希表一次性统计多来源的出现次数。  
- **适用的题型**：  
  1. “两个数组中出现恰好一次的元素” （如 2089. Find Target Indices With a Constraint）  
  2. “统计出现次数并筛选满足特定条件的元素” （如 2283. 检查数组中是否有重复元素）  
- **一句话总结解题钥匙**：**把所有计数集中到同一个字典里，一遍遍历即可得到答案**。

---

## 反思

- **第一反应**：直接把两个数组分别计数，然后比较对应的计数。  
- **最容易踩的坑**：  
  - 忽略了单词在同一个数组里出现多次的情况（如题目示例中的 `"is"`）。  
  - 在实现时忘记对不存在的键进行初始化，导致 `KeyError`。  
- **下次类似题目第一步**：先思考“怎么把所有信息放进同一个容器（哈希表）”，再决定遍历次数与统计方式。