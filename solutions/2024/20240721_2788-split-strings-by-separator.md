# #2788. 按分隔符拆分字符串 / Split Strings by Separator

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/split-strings-by-separator/)

---

## 题目（英文原版）

**Description**

Given an array of strings words and a character separator, split each string in words by separator.
Return an array of strings containing the new strings formed after the splits, excluding empty strings.
Notes

**Examples**

**Example 1:**

```
Input: words = ["one.two.three","four.five","six"], separator = "."
Output: ["one","two","three","four","five","six"]
Explanation: In this example we split as follows:

"one.two.three" splits into "one", "two", "three"
"four.five" splits into "four", "five"
"six" splits into "six" 

Hence, the resulting array is ["one","two","three","four","five","six"].
```

**Example 2:**

```
Input: words = ["$easy$","$problem$"], separator = "$"
Output: ["easy","problem"]
Explanation: In this example we split as follows: 

"$easy$" splits into "easy" (excluding empty strings)
"$problem$" splits into "problem" (excluding empty strings)

Hence, the resulting array is ["easy","problem"].
```

**Example 3:**

```
Input: words = ["|||"], separator = "|"
Output: []
Explanation: In this example the resulting split of "|||" will contain only empty strings, so we return an empty array [].
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 20
- characters in words[i] are either lowercase English letters or characters from the string ".,|$#@" (excluding the quotes)
- separator is a character from the string ".,|$#@" (excluding the quotes)

---

## 题目（中文翻译）

给定一个字符串数组（array of strings）`words` 和一个字符（character）`separator`，对 `words` 中的每个字符串按照 `separator` 进行拆分（split）。  
返回一个字符串数组（array of strings），其中包含拆分后得到的新字符串，且 **不** 包含空字符串（empty strings）。

## 示例

### 示例 1  
**输入**: `words = ["one.two.three","four.five","six"], separator = "."`  
**输出**: `["one","two","three","four","five","six"]`  
**解释**: 本例的拆分过程如下  

- `"one.two.three"` 拆分为 `"one"`, `"two"`, `"three"`  
- `"four.five"` 拆分为 `"four"`, `"five"`  
- `"six"` 拆分为 `"six"`  

因此得到的数组为 `["one","two","three","four","five","six"]`。

### 示例 2  
**输入**: `words = ["$easy$","$problem$"], separator = "$"`  
**输出**: `["easy","problem"]`  
**解释**: 本例的拆分过程如下  

- `"$easy$"` 拆分为 `"easy"`（排除空字符串）  
- `"$problem$"` 拆分为 `"problem"`（排除空字符串）  

因此得到的数组为 `["easy","problem"]`。

### 示例 3  
**输入**: `words = ["|||"], separator = "|"`  
**输出**: `[]`  
**解释**: 本例中 `|||` 拆分后只会得到空字符串，所以返回空数组 `[]`。

## 约束条件
- `1 <= words.length <= 100`  
- `1 <= words[i].length <= 20`  
- `words[i]` 中的字符仅为小写英文字母或字符集合 `".,|$#@"`（不含引号）中的任意字符  
- `separator` 为字符集合 `".,|$#@"`（不含引号）中的一个字符

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**把每个单词按给定的分隔符切开**，把得到的子串全部收集起来，再把空串（`""`）去掉。  

- **使用的数据结构**  
  - `list`（列表）：像装东西的盒子，用来依次保存每个原始字符串的切分结果。  
  - `str.split(separator)`：Python 内置的“切刀”。它把字符串看成一串词，用 `separator` 当作刀子在每个出现的位置切断，返回一个子串列表。  
  - `filter` 或列表推导式：把空串过滤掉，就像在字典里查单词时，只把有意义的词挑出来。

- **为什么正确**  
  对每个字符串，`split` 会完整地把它按照分隔符分割，**不会遗漏任何字符**。随后把所有非空子串放进同一个结果列表，即得到题目要求的“所有新字符串”。  

- **时间/空间复杂度**  
  - 对每个字符串我们都遍历一次它的字符（`split` 的内部实现），所以总共遍历 `words` 中所有字符一次，时间是 **O(N)**，这里的 **N** 表示所有字符的总长度。  
  - 额外的空间主要是保存分割后的子串，最坏情况下每个字符都是独立的子串，空间也是 **O(N)**。  

#### 代码（Python）

```python
def splitWordsBySeparator(words, separator):
    """
    把 words 中的每个字符串按 separator 切开，返回所有非空子串组成的列表。
    """
    result = []                       # 用来装最终答案的列表
    for w in words:                   # 逐个处理 words 中的字符串
        parts = w.split(separator)    # Python 的 split，返回切分后的子串列表
        # 过滤掉空字符串 ""，只保留有实际内容的子串
        for p in parts:
            if p:                     # p 非空时为 True
                result.append(p)
    return result
```

#### 复杂度  

- **时间复杂度：O(N)** — 需要遍历所有字符一次。  
- **空间复杂度：O(N)** — 结果列表里要存放所有非空子串，最坏情况下和输入字符数等量。

---

### 2. 最优解

#### 思路  

从暴力解来看，**真正的瓶颈不存在**：  
- `split` 已经是线性时间的最优切分操作。  
- 过滤空串也只需要一次遍历。  

所以 **没有进一步可以加速的地方**，最优解其实和暴力解是同一套实现，只是把代码写得更简洁、直接。我们可以利用列表推导式一次性完成所有步骤，代码更紧凑，思路更清晰。

核心技巧仍是 **字符串切分 + 过滤空串**。下面用一步一步的解释帮助初学者理解：

1. **一次遍历所有字符串**：`for w in words`。  
2. **对每个字符串直接使用 `split`**：得到子串列表。  
3. **把所有子串展平（flatten）到同一个列表**：使用两层循环的列表推导式。  
4. **只保留非空子串**：在推导式里加上 `if part` 条件。

> **类比**：想象你有若干本书（每本书对应一个字符串），每本书里都有章节标题用特殊符号分隔。你要把所有章节标题收集成一本新书，且空标题（只出现分隔符的地方）不要放进去。一次遍历每本书，摘下每个标题，再把标题全部装进新书即可。

#### 代码（Python）

```python
def splitWordsBySeparator(words, separator):
    """
    最简洁的实现：一次遍历、一次切分、一次过滤。
    """
    # 两层列表推导式：
    # - 外层遍历每个原始字符串 w
    # - 内层遍历 w.split(separator) 得到的子串 part
    # - if part 过滤掉空串
    return [part for w in words for part in w.split(separator) if part]
```

#### 复杂度  

- **时间复杂度：O(N)** — 仍然只遍历一次所有字符。  
- **空间复杂度：O(N)** — 结果列表需要存放所有非空子串。  
与暴力解的复杂度相同，只是实现更紧凑，常数因子更小。

---

## 心得

- **核心技巧**：字符串的 `split` 方法 + 过滤空串。  
- **适用的题型**  
  1. 把 CSV、日志等文本按分隔符拆分成字段（如 `split` + `map`）。  
  2. 统计句子中出现的单词或字符（先 `split` 再遍历）。  
  3. 处理路径或 URL 中的段落（如 `path.split('/')`）。  
- **解题钥匙**：**一次遍历 + 原生切分**，不需要额外的数据结构或复杂的算法。

---

## 反思

- **第一反应**：直接想到 Python 的 `str.split`，因为它本身就能完成“按字符切分并返回子串列表”。  
- **最容易踩的坑**  
  - 忘记过滤空串，导致结果里出现 `""`（比如 `"$$".split("$")` 会得到 `['', '', '']`）。  
  - 分隔符是特殊字符（如 `.`、`|`），在正则库里需要转义，但这里使用 `split` 不会有问题。  
- **下次遇到同类题**：第一步想到 **“有没有现成的语言特性可以直接完成切分？”**，如果有，就直接使用并在后面加上必要的过滤。这样既简洁又高效。