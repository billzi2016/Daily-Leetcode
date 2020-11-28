# #1078. 大二元组后出现的单词 / Occurrences After Bigram

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/occurrences-after-bigram/)

---

## 题目（英文原版）

**Description**

Given two strings first and second, consider occurrences in some text of the form "first second third", where second comes immediately after first, and third comes immediately after second.
Return an array of all the words third for each occurrence of "first second third".

**Examples**

**Example 1:**

```
Input: text = "alice is a good girl she is a good student", first = "a", second = "good"
Output: ["girl","student"]
```

**Example 2:**

```
Input: text = "we will we will rock you", first = "we", second = "will"
Output: ["we","rock"]
```

**Constraints**

- 1 <= text.length <= 1000
- text consists of lowercase English letters and spaces.
- All the words in text are separated by a single space.
- 1 <= first.length, second.length <= 10
- first and second consist of lowercase English letters.
- text will not have any leading or trailing spaces.

---

## 题目（中文翻译）

给定两个字符串 `first` 和 `second`，在一段文本 `text` 中，考虑形如 `"first second third"` 的出现，其中 `second` 紧跟在 `first` 之后，`third` 紧跟在 `second` 之后。  
返回一个数组，包含每一次出现 `"first second third"` 时对应的单词 `third`。

**示例 1:**  
**示例 2:**  

**约束条件**

- `1 <= text.length <= 1000`
- `text` 仅由小写英文字母和空格组成。
- `text` 中的所有单词均由单个空格分隔。
- `1 <= first.length, second.length <= 10`
- `first` 和 `second` 仅由小写英文字母组成。
- `text` 不会有前导或尾随空格。

**示例**

示例 1:  
``` 
Input: text = "alice is a good girl she is a good student", first = "a", second = "good"
Output: ["girl","student"]
```

示例 2:  
``` 
Input: text = "we will we will rock you", first = "we", second = "will"
Output: ["we","rock"]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整段文字先切成单词列表，然后把每三个相邻的单词组成一个「三元组」  
`(words[i], words[i+1], words[i+2])`，检查前两个单词是否分别等于 `first` 和 `second`，如果相等，就把第三个单词记下来。  

- **用到的数据结构**：  
  - `list`（列表），把字符串 `text` 按空格分割成若干单词。可以把它想象成「一排排的词卡」。
- **为什么正确**：  
  - 题目要求的「first second third」恰好是连续的三个词。遍历所有连续的三个词，必然能捕获所有满足条件的出现位置，且不会遗漏。
- **时间/空间复杂度**：  
  - 假设文本里有 `n` 个单词。我们会检查每个可能的起始位置 `i`（`0 … n‑3`），每次检查常数次（只比较两个字符串），所以时间复杂度是 **O(n)**。  
  - 额外空间只用来存放切分后的单词列表和答案列表，都是线性大小，故空间复杂度是 **O(n)**。  
  - 大白话：如果文本有 1000 个词，我们最多看 1000‑2≈998 次，每次只做几次“是不是相等”的对比，基本就是一次线性遍历。

#### 代码（Python）

```python
def findOcurrences(text: str, first: str, second: str):
    # 把整段文字按空格切成单词列表
    words = text.split()                     # ["alice", "is", "a", "good", ...]
    ans = []                                 # 用来存放所有符合条件的 third

    # 遍历所有可能的三元组起始下标 i
    for i in range(len(words) - 2):          # -2 保证 i+2 不会越界
        # 判断前两个词是否正好是 first、second
        if words[i] == first and words[i + 1] == second:
            ans.append(words[i + 2])         # 把第三个词加入答案

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次单词列表，`n` 为单词数量。  
- **空间复杂度**：`O(n)` — 需要保存切分后的单词列表（长度为 `n`）和结果列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，瓶颈并不在「比较」本身，而是我们在遍历时每次都要访问 `words[i]`、`words[i+1]`、`words[i+2]`。这已经是线性的最底限了，无法再进一步降低时间复杂度。  
因此「最优」解其实就是**把暴力解写得更简洁、更易读**，仍然是一次遍历。可以使用「滑动窗口」的思想：一次循环里把当前窗口的三个词看成 `first, second, third`，如果前两词匹配，就把第三词收集。滑动窗口的概念可以类比为「在一排词卡上用手指一次滑过三个相邻的卡片」。

核心技巧：一次遍历、同时检查相邻的三个词。

#### 代码（Python）

```python
def findOcurrences(text: str, first: str, second: str):
    words = text.split()
    ans = []

    # 用 i 表示第三个词的下标，i 从 2 开始，这样 i-2,i-1 就是前两个词
    for i in range(2, len(words)):
        if words[i - 2] == first and words[i - 1] == second:
            ans.append(words[i])      # 当前词恰好是满足条件的 third
    return ans
```

> **代码说明**  
> - `i` 从 `2` 开始，使得 `i-2`、`i-1`、`i` 正好是连续的三个词。  
> - 每次只做一次比较（两次相等判断），符合「滑动窗口」的思想。  

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次单词列表，和暴力解的时间相同，但写法更简洁。  
- **空间复杂度**：`O(n)` — 仍然需要保存切分后的单词列表和结果列表。

---

## 心得

- **核心技巧**：一次遍历 + 相邻三元组检查（滑动窗口）。  
- **适用的题型**：  
  1. “找出所有满足某种相邻模式的子串/单词”——如 LeetCode 1071 *Greatest Common Divisor of Strings*（虽是字符串拼接，但同样需要一次遍历）。  
  2. “统计连续出现次数的题目”——如 1108 *Project Employees I*（统计相邻项目）。  
  3. “找出满足前后关系的三元组”——如 1078 *Occurrences After Bigram*（本题）以及 2088 *Find Target Indices After Sorting Array*（需要一次遍历定位目标）。  
- **一句话总结解题钥匙**：把「三个连续词」看成滑动窗口，一次遍历即可全部捕获。

## 反思

- **拿到题目第一反应**：先把字符串切成单词，然后枚举所有相邻的三个词，检查前两个是否匹配。  
- **最容易踩的坑**：  
  - **下标越界**：遍历时一定要保证 `i+2`（或 `i-2`）不超出列表范围。  
  - **空格处理**：题目保证单词之间只有单个空格且没有首尾空格，直接 `split()` 就可以。若没有此保证，需要自行处理多余空格。  
  - **重复计数**：如果出现重叠的三元组（如 `"a a a"`），仍然需要每次都检查，代码中自然会处理。  
- **下次遇到同类题的第一步**：先把输入拆成最小的「基本单元」（这里是单词列表），然后想象一个固定大小的「滑动窗口」在这些基本单元上滑动，检查窗口内部是否满足条件。这样思路清晰，代码也会自然简洁。