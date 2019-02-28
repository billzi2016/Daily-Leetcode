# #318. Maximum Product of Word Lengths / Maximum Product of Word Lengths

> 难度：中等 · 标签：Array、String、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/maximum-product-of-word-lengths/)

---

## 题目（英文原版）

**Description**

Given a string array words, return the maximum value of length(word[i]) * length(word[j]) where the two words do not share common letters. If no such two words exist, return 0.

**Examples**

**Example 1:**

```
Input: words = ["abcw","baz","foo","bar","xtfn","abcdef"]
Output: 16
Explanation: The two words can be "abcw", "xtfn".
```

**Example 2:**

```
Input: words = ["a","ab","abc","d","cd","bcd","abcd"]
Output: 4
Explanation: The two words can be "ab", "cd".
```

**Example 3:**

```
Input: words = ["a","aa","aaa","aaaa"]
Output: 0
Explanation: No such pair of words.
```

**Constraints**

- 2 <= words.length <= 1000
- 1 <= words[i].length <= 1000
- words[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组（string array）`words`，返回 `length(word[i]) * length(word[j])` 的最大值，其中这两个单词 **不共享任何公共字母**（common letters）。如果不存在满足条件的两个单词，返回 `0`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- `2 <= words.length <= 1000`  
- `1 <= words[i].length <= 1000`  
- `words[i]` 仅由小写英文字母组成。

---

### 示例

#### 示例 1
**输入**: `words = ["abcw","baz","foo","bar","xtfn","abcdef"]`  
**输出**: `16`  
**解释**: 可以选取的两个单词是 `"abcw"` 和 `"xtfn"`。

#### 示例 2
**输入**: `words = ["a","ab","abc","d","cd","bcd","abcd"]`  
**输出**: `4`  
**解释**: 可以选取的两个单词是 `"ab"` 和 `"cd"`。

#### 示例 3
**输入**: `words = ["a","aa","aaa","aaaa"]`  
**输出**: `0`  
**解释**: 不存在满足条件的单词对。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把所有单词两两配对，检查它们是否有公共字母，如果没有就算出 `len(word[i]) * len(word[j])`，把最大的乘积记下来。  

- **数据结构**：我们只需要把单词放在一个普通的 Python `list` 里，遍历时用两层 `for` 循环。  
- **公共字母检查**：可以把每个单词的字符放进 `set`（集合）中，集合的交集不为空说明有公共字母。集合就像是“字典”，里面存的只是字母本身，判断是否相交相当于看两个字典里有没有相同的词。  

> 为什么这样一定能得到答案？因为我们枚举了 **所有** 可能的两两组合，只要有满足条件的配对，必定会被遍历到，最大乘积自然会被记录。

#### 代码（Python）

```python
from typing import List

def max_product_brute(words: List[str]) -> int:
    n = len(words)
    max_prod = 0                     # 记录当前找到的最大乘积
    # 两层循环遍历所有 i < j 的组合
    for i in range(n):
        set_i = set(words[i])        # 把第 i 个单词的字符放进集合，方便后面检查
        len_i = len(words[i])
        for j in range(i + 1, n):
            set_j = set(words[j])
            # 如果两个集合没有交集，说明没有公共字母
            if set_i.isdisjoint(set_j):   # isdisjoint == 没有交集
                prod = len_i * len(words[j])
                if prod > max_prod:
                    max_prod = prod
    return max_prod
```

#### 复杂度

- **时间复杂度**：`O(n² * m)`  
  - `n` 是单词数量，外层两层循环产生 `n²/2` 次配对。  
  - 对每对单词我们要把字符放进集合或做交集检查，最坏情况要遍历单词的长度 `m`（单词最长 1000）。  
  - 用大白话说，就是“如果有 1000 个单词，每个单词有 1000 个字母，最坏情况下要做大约 10⁹ 次字符比较”，这在实际运行时会很慢。

- **空间复杂度**：`O(m)`（临时集合的大小）  
  - 每次只存两个人的字符集合，最多占用 `26` 个字母的空间（常数），可以认为是 `O(1)`，但从实现角度看要额外开几个集合，算作 `O(m)`。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **每次比较都要遍历字符**。如果我们能把“字符集合”压缩成一个固定长度的数据结构，比较两单词是否有公共字母就可以在 **常数时间** 完成。

**位运算（Bit Manipulation）** 正好能做到这点。  
- 英文字母只有 26 个。我们可以用一个 32 位的整数的二进制位来表示一个单词出现了哪些字母。  
  - 第 0 位代表 `'a'`，第 1 位代表 `'b'`，... 第 25 位代表 `'z'`。  
  - 如果单词里出现了 `'c'`，就把第 2 位设为 1。  
  - 这样，一个单词就对应了一个 **掩码**（mask），比如 `"abc"` → `0b111`（二进制 111），只占用 3 位。

- 判断两个单词是否有公共字母，只需要把它们的掩码 **与**（`&`）一下。  
  - 如果结果为 0，说明没有共同的 1，也就是没有公共字母。  
  - 这一步是 O(1) 的整数运算，极快。

**步骤**：

1. **预处理**：遍历 `words`，为每个单词计算掩码并记下它的长度。可以把这两个信息放在同一个列表里，形成 `(mask, length)` 的元组。  
2. **双层遍历**：仍然要两两配对，但这次只比较掩码的 **与运算**，如果 `mask_i & mask_j == 0` 就说明可以计算乘积。  
3. 记录最大乘积即可。

> 类比：把每个单词想成一本书的“目录”，目录里只记哪些字母出现过。两本书是否有共同章节，只要看目录的交叉（与运算）是否为空。

#### 代码（Python）

```python
from typing import List

def max_product(words: List[str]) -> int:
    # 第一步：把每个单词转换成二进制掩码 + 记录长度
    masks = []                       # 存放 (mask, length) 元组
    for w in words:
        mask = 0
        for ch in w:                # 把单词里的每个字符对应的位设为 1
            mask |= 1 << (ord(ch) - ord('a'))   # ord('a') = 97
        masks.append((mask, len(w)))   # 保存掩码和长度

    max_prod = 0
    n = len(masks)
    # 第二步：两两配对，使用位与判断是否有公共字母
    for i in range(n):
        mask_i, len_i = masks[i]
        for j in range(i + 1, n):
            mask_j, len_j = masks[j]
            if mask_i & mask_j == 0:          # 位与为 0 → 没有公共字母
                prod = len_i * len_j
                if prod > max_prod:
                    max_prod = prod
    return max_prod
```

#### 复杂度

- **时间复杂度**：`O(n * m + n²)`  
  - `n * m`：预处理阶段遍历每个字符，计算掩码。`m` 是单词平均长度。  
  - `n²`：配对阶段是两层循环，但每次比较只做一次整数 `&`，是 **常数时间**。  
  - 相比暴力解把字符比较放在配对里，这里把它提前做了一遍，整体快了很多。对于 `n ≤ 1000`、`m ≤ 1000`，运行在几毫秒内。

- **空间复杂度**：`O(n)`  
  - 需要为每个单词保存一个整数掩码和长度，共 `n` 条记录。整数本身占用常数空间（4~8 字节），整体随 `n` 线性增长。

---

## 心得

- **核心技巧**：把离散的字符集合压缩成位掩码，用位运算实现 O(1) 的交集检测。  
- **适用题型**：  
  1. “判断两个集合是否有交集” 类的问题（如 `Maximum XOR of Two Numbers in an Array` 的位思路）。  
  2. “子集或子序列的状态压缩” 题目（如 `Count of Good Substrings`、`Subsets with No Adjacent Elements`）。  
- **一句话总结**：把字母集合映射成 26 位的二进制数，利用位与快速判断是否相交，即可把暴力 O(n²·m) 降到 O(n²)。  

---

## 反思

- **第一反应**：直接两层循环遍历所有单词配对，用 `set` 判断是否有公共字母。  
- **最容易踩的坑**：  
  - **时间超限**：如果不进行位压缩，`n` 与 `m` 都是 1000 时会导致 O(10⁹) 的字符比较。  
  - **掩码冲突**：忘记把相同字母对应的位设为 1（使用 `|=` 而不是 `=`），会导致错误的交集判断。  
  - **边界情况**：全部单词都有公共字母，答案应返回 0。  
- **下次第一步**：看到“字符集合不相交”这类描述，立刻想到 **位掩码**（如果字符种类有限），先把集合压缩，再进行配对比较。这样可以把隐藏的 O(m) 计算提前，显著提升效率。