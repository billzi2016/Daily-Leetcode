# #2129. 标题大小写 / Capitalize the Title

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/capitalize-the-title/)

---

## 题目（英文原版）

**Description**

You are given a string title consisting of one or more words separated by a single space, where each word consists of English letters. Capitalize the string by changing the capitalization of each word such that:
Return the capitalized title.

**Examples**

**Example 1:**

```
Input: title = "capiTalIze tHe titLe"
Output: "Capitalize The Title"
Explanation:
Since all the words have a length of at least 3, the first letter of each word is uppercase, and the remaining letters are lowercase.
```

**Example 2:**

```
Input: title = "First leTTeR of EACH Word"
Output: "First Letter of Each Word"
Explanation:
The word "of" has length 2, so it is all lowercase.
The remaining words have a length of at least 3, so the first letter of each remaining word is uppercase, and the remaining letters are lowercase.
```

**Example 3:**

```
Input: title = "i lOve leetcode"
Output: "i Love Leetcode"
Explanation:
The word "i" has length 1, so it is lowercase.
The remaining words have a length of at least 3, so the first letter of each remaining word is uppercase, and the remaining letters are lowercase.
```

**Constraints**

- 1 <= title.length <= 100
- title consists of words separated by a single space without any leading or trailing spaces.
- Each word consists of uppercase and lowercase English letters and is non-empty.

---

## 题目（中文翻译）

给定一个只包含英文字母且由单个空格分隔的 **字符串 (string)** `title`，其中至少包含一个单词，每个单词仅由字母组成。请按以下规则对每个单词的大小写进行转换，使得整个标题符合要求后返回。

- 若单词长度 **≥ 3**，则将首字母改为 **大写 (uppercase)**，其余字母改为 **小写 (lowercase)**。  
- 若单词长度 **< 3**，则将所有字母全部改为小写。

返回处理后的 **标题 (title)**。

## 示例

### 示例 1
**输入**  
`title = "capiTalIze tHe titLe"`

**输出**  
`"Capitalize The Title"`

**解释**  
所有单词长度均不小于 3，故每个单词的首字母均转为大写，其余字母转为小写。

### 示例 2
**输入**  
`title = "First leTTeR of EACH Word"`

**输出**  
`"First Letter of Each Word"`

**解释**  
单词 `"of"` 长度为 2，需全部转为小写。其余单词长度均 ≥ 3，首字母大写，其余小写。

### 示例 3
**输入**  
`title = "i lOve leetcode"`

**输出**  
`"i Love Leetcode"`

**解释**  
单词 `"i"` 长度为 1，保持小写。其余单词长度均 ≥ 3，首字母大写，其余小写。

## 约束条件

- `1 <= title.length <= 100`
- `title` 仅由单个空格分隔的单词组成，且不存在首尾空格。
- 每个单词均为非空，且仅包含大小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把字符串按空格拆成单词，**逐个**处理每个单词的大小写，再把它们用空格拼回去。  

- **拆分**：使用 `split(' ')` 把 `"capiTalIze tHe titLe"` 变成 `["capiTalIze","tHe","titLe"]`。  
  - 类比：把一串珠子（句子）按颜色（空格）分成若干串（单词），每串单独操作更方便。  
- **处理单词**：  
  - 如果单词长度 **≥ 3**，把首字母大写、其余字母小写。  
  - 如果长度 **< 3**，全部转成小写。  
  - 这里的 “大写” 与 “小写” 可以直接调用 Python 的 `upper()`、`lower()`，就像查字典一样——把字母这本“大词典”里对应的“页码”（大小写）换过去。  
- **合并**：把处理好的单词用空格 `' '` 再次拼接成完整的句子。  

这种做法一定能得到正确答案，因为我们严格按照题目要求对每个单词执行了同样的规则，且没有遗漏任何字符。

#### 代码（Python）

```python
def capitalizeTitle(title: str) -> str:
    # 1️⃣ 把句子拆成单词列表
    words = title.split(' ')          # ["capiTalIze", "tHe", "titLe"]

    # 2️⃣ 逐个处理单词
    for i, w in enumerate(words):
        if len(w) >= 3:               # 长度 ≥ 3 → 首字母大写，其余小写
            # w[0].upper() 把第一个字符转成大写
            # w[1:].lower() 把后面的字符全部转成小写
            words[i] = w[0].upper() + w[1:].lower()
        else:                         # 长度 < 3 → 全部小写
            words[i] = w.lower()

    # 3️⃣ 把处理好的单词重新拼成句子并返回
    return ' '.join(words)             # "Capitalize The Title"
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 这里的 `n` 是字符串的总字符数。我们遍历了一遍 `title`（拆分、逐字符大小写转换、再拼接），每个字符只被处理常数次。  
  - 用大白话说，就是“时间随字符数线性增长”，字符多了花的时间也会相应多，但不会出现指数级、平方级的爆炸。  
- **空间复杂度**：`O(n)`  
  - 需要额外的列表 `words` 来存放拆分后的单词，以及最终返回的拼接结果，这些都和原字符串大小成正比。  

---

### 2. 最优解

#### 思路  

对于这道 **Easy** 题目，暴力解已经是最优的线性解法了，没有更快的“奇技淫巧”。  
唯一可以改进的地方是 **省掉列表的额外拷贝**，直接在遍历原字符串的同时构造结果。思路如下：

1. 用 `split(' ')` 仍然是最方便的方式获取每个单词，**但**我们可以在遍历时直接把处理好的单词加入结果列表，而不再对列表再做一次遍历修改。  
2. 处理单词的规则保持不变（长度 ≥3 → 首字母大写，其余小写；否则全部小写）。  
3. 最后一次性 `join`，得到答案。

这样做的核心仍是 **一次遍历**，时间复杂度仍是 `O(n)`，但省去了对列表的二次写入，常数因子更小。  

> **为什么这样算“最优”？**  
> - 对于字符串处理，`O(n)` 已经是下界（必须看每个字符一次），再进一步只能在 **常数因子** 上优化。  
> - 采用 **生成式（list comprehension）** 或 **生成器表达式** 能让代码更紧凑，也更符合 Pythonic 风格。  

#### 代码（Python）

```python
def capitalizeTitle(title: str) -> str:
    # 用列表生成式一次完成“拆分 → 处理 → 收集”
    processed = [
        # 对每个单词 w，按照长度决定转换方式
        w[0].upper() + w[1:].lower() if len(w) >= 3 else w.lower()
        for w in title.split(' ')
    ]
    # 再一次性拼接成最终字符串
    return ' '.join(processed)
```

> **代码要点注释**（可自行在 IDE 中打开查看）  
> - `title.split(' ')`：把句子切成单词列表。  
> - `w[0].upper() + w[1:].lower()`：首字母大写、其余小写。  
> - `if len(w) >= 3 else w.lower()`：长度小于 3 时全部小写。  
> - `''.join(processed)`：把处理好的单词用空格连起来。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 仍然只遍历一次原始字符（拆分、大小写转换、拼接），没有额外的循环。  
- **空间复杂度**：`O(n)`  
  - 需要保存处理后的单词列表 `processed`，其总长度与输入相同。  

与暴力解相比，**时间相同**，**空间相同**，但实现更简洁、常数因子更小。

---

## 心得

- **核心技巧**：对字符串按空格分词后，根据长度分别使用 `upper()` / `lower()` 完成大小写转换。  
- **适用场景**：  
  1. **标题大小写规范**（如本题、LeetCode 2129 “Capitalizing the Title”）。  
  2. **单词首字母大写**（如 151 “Reverse Words in a String”。）  
  3. **根据长度或其它条件对单词做不同处理**（如 125 “Valid Palindrome” 的预处理）。  
- **一句话总结**：**“先分词，再按规则逐词转换，最后合并”** 是处理这类字符串格式化题的通用钥匙。

---

## 反思

- **第一反应**：看到“单词”“长度”“大小写”，立刻想到先把句子拆成单词，再逐个判断长度并转大小写。  
- **最容易踩的坑**：  
  - 忘记把 **其余字符全部转成小写**（只改首字母会导致 “tHe” → “TH e” 等错误）。  
  - 处理长度为 **1 或 2** 的单词时，直接使用 `lower()`，不要只改首字母。  
  - 输入保证没有前后空格，但如果忘记 `split(' ')` 而用了默认 `split()`（会把多个空格视为一个），在本题不会出错，但要保持对题目约束的尊重。  
- **下次思路**：遇到类似“对每个单词做不同规则的转换”时，第一步就 **“分词 + 循环/生成式”**，然后 **“根据条件决定转换方式”**，最后 **“重新拼接”。这样思路清晰，代码也容易写对。