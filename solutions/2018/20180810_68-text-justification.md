# #68. 文本对齐 / Text Justification

> 难度：困难 · 标签：Array、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/text-justification/)

---

## 题目（英文原版）

**Description**

Given an array of strings words and a width maxWidth, format the text such that each line has exactly maxWidth characters and is fully (left and right) justified.
You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly maxWidth characters.
Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line does not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.
For the last line of text, it should be left-justified, and no extra space is inserted between words.
Note:

**Examples**

**Example 1:**

```
Input: words = ["This", "is", "an", "example", "of", "text", "justification."], maxWidth = 16
Output:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
```

**Example 2:**

```
Input: words = ["What","must","be","acknowledgment","shall","be"], maxWidth = 16
Output:
[
  "What   must   be",
  "acknowledgment  ",
  "shall be        "
]
Explanation: Note that the last line is "shall be    " instead of "shall     be", because the last line must be left-justified instead of fully-justified.
Note that the second line is also left-justified because it contains only one word.
```

**Example 3:**

```
Input: words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"], maxWidth = 20
Output:
[
  "Science  is  what we",
  "understand      well",
  "enough to explain to",
  "a  computer.  Art is",
  "everything  else  we",
  "do                  "
]
```

**Constraints**

- 1 <= words.length <= 300
- 1 <= words[i].length <= 20
- words[i] consists of only English letters and symbols.
- 1 <= maxWidth <= 100
- words[i].length <= maxWidth

---

## 题目（中文翻译）

给定一个字符串数组（`words`）和一个宽度（`maxWidth`），将文本排版，使得每一行恰好有 `maxWidth` 个字符，并且实现完全（左右）对齐。

- 你需要采用贪心算法（greedy approach）来装填单词，即在每一行尽可能多地放入单词。必要时使用额外的空格（`' '`）填充，使得每行恰好为 `maxWidth` 个字符。
- 行内单词之间的空格应尽可能均匀分配。如果某行的空格数无法在单词间平均分配，则左侧的空格槽（empty slots）比右侧的多。
- 最后一行应左对齐（left‑justified），且单词之间不再插入额外的空格。

**示例 1**  

**示例 2**  

**示例 3**  

**约束条件**  

- `1 <= words.length <= 300`
- `1 <= words[i].length <= 20`
- `words[i]` 只包含英文字母和符号。
- `1 <= maxWidth <= 100`
- `words[i].length <= maxWidth`

---

### 示例

#### 示例 1
**输入**  
```json
words = ["This", "is", "an", "example", "of", "text", "justification."]
maxWidth = 16
```
**输出**
```json
[
    "This    is    an",
    "example  of text",
    "justification. "
]
```

#### 示例 2
**输入**  
```json
words = ["What","must","be","acknowledgment","shall","be"]
maxWidth = 16
```
**输出**
```json
[
    "What   must   be",
    "acknowledgment  ",
    "shall be        "
]
```
**解释**：注意最后一行是 `"shall be        "` 而不是 `"shall     be"`，因为最后一行必须左对齐而不是完全对齐。第二行也是左对齐的，因为它只包含一个单词。

#### 示例 3
**输入**  
```json
words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"]
maxWidth = 20
```
**输出**
```json
[
    "Science  is  what we",
    "understand       well",
    "enough to explain to",
    "a  computer.  Art is",
    "everything  else  we",
    "do                  "
]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐行尝试**：  
1. 从左到右遍历单词列表 `words`，把尽可能多的单词放进当前行，直到再放一个单词就会超出 `maxWidth`。  
2. 把这行单词按**等宽**的方式填充空格：先把所有单词用单个空格连接，然后在得到的字符串后面补足剩余的空格，使整行恰好 `maxWidth` 长。  
3. 对每一行都这样处理，最后把所有行拼成答案。

> **类比**：把每行想象成一本书的“行纸”，我们像在排版软件里手动往纸上写字，写满后再用橡皮把剩余的空白补满。

**为什么正确**  
- 题目要求“尽可能多地装单词”，所以只要我们每次把**能放的最多单词**取出来，就满足了贪心的装填规则。  
- 对每行只要把单词间的空格填满到 `maxWidth`，就满足了“左、右对齐”。（最后一行和只含一个单词的行另作处理，后面会说明）

**时间/空间复杂度**  
- 对每一行我们会**重新遍历**该行的所有单词来计算空格数，这在最坏情况下会导致 **二次遍历**：外层遍历所有单词 O(n)，内层对每行的单词再遍历一次，总体是 O(n²)。  
- 额外使用的空间主要是保存结果列表，和每行临时的字符串，都是 O(n)（与输入大小同量级）。

> **大白话**：  
> - O(n²) 就像在课堂上每次都要把已经写好的笔记重新抄一遍，时间会翻倍增长。  
> - O(n) 的空间相当于我们只在桌面上放了一叠纸，纸的数量和原来的笔记本差不多。

#### 代码（Python）

```python
from typing import List

def fullJustify_bruteforce(words: List[str], maxWidth: int) -> List[str]:
    res = []                # 最终返回的每一行
    i = 0                   # 当前处理到的单词下标
    n = len(words)

    while i < n:
        # ① 先找出本行能放的最多单词
        line_len = len(words[i])          # 第一个单词的长度
        j = i + 1                         # j 指向下一个候选单词
        while j < n and line_len + 1 + len(words[j]) <= maxWidth:
            line_len += 1 + len(words[j]) # +1 表示单词之间至少要有一个空格
            j += 1

        # ② 生成本行的字符串
        line_words = words[i:j]           # 本行所有单词
        num_words = len(line_words)

        # 最后一行 或 该行只有一个单词 → 左对齐
        if j == n or num_words == 1:
            line = ' '.join(line_words)               # 单词之间一个空格
            line += ' ' * (maxWidth - len(line))      # 右侧补足空格
        else:
            # 需要均匀分配空格
            total_spaces = maxWidth - sum(map(len, line_words))   # 需要的总空格数
            spaces_between = total_spaces // (num_words - 1)      # 每两个单词间最少的空格数
            extra = total_spaces % (num_words - 1)               # 余下的空格，要从左到右依次加1

            line = ''
            for k in range(num_words - 1):
                line += line_words[k]                 # 加单词
                # 先加基本空格数，再把剩余的空格（如果有）分配到左边的缝隙
                line += ' ' * (spaces_between + (1 if k < extra else 0))
            line += line_words[-1]                    # 最后一个单词后面不再加空格

        res.append(line)
        i = j                                        # 继续处理下一行

    return res
```

#### 复杂度

- **时间复杂度**：O(n²)  
  解释：外层遍历 `n` 个单词，内层在每行重新遍历该行的单词来计算空格，最坏情况下每行可能只有 1~2 个单词，导致整体二次遍历。

- **空间复杂度**：O(n)  
  解释：除了存放答案的列表外，只用了常数级别的临时变量。答案本身的大小与输入单词数成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历本行单词来算空格**。实际上，只要在 **确定本行单词集合** 的同时，直接记录该行单词的总长度，就可以在 O(1) 时间内算出需要的空格数，从而一次遍历完成全部工作。

**核心步骤**：

1. **贪心取词**：和暴力解一样，从左到右尽可能多地取单词，使 `words_len + spaces_needed ≤ maxWidth`。这里 `words_len` 是本行单词的总字符数，`spaces_needed = (num_words-1)`（每两个单词至少要一个空格）。  
2. **一次性计算空格**：  
   - `total_spaces = maxWidth - words_len` 为本行需要的全部空格数。  
   - 若是**最后一行**或**只有一个单词**，直接左对齐：单词之间一个空格，其余空格全放在行尾。  
   - 否则，**均匀分配**：  
     - `space_per_gap = total_spaces // (num_words - 1)` → 每个间隙至少的空格数。  
     - `extra = total_spaces % (num_words - 1)` → 多出的空格，从左到右依次加到前 `extra` 个间隙。  
3. **构造行字符串**：在遍历本行单词时，直接把对应数量的空格拼进去，**不再进行二次遍历**。  

> **类比**：把每行看成一条“装配线”，我们在把零件（单词）装进去的同时，就顺手把螺丝（空格）拧好，不需要装好后再回头去补螺丝。

**为什么是最优**  
- 每个单词只被访问一次（确定所在行时）且在构造行时再次访问一次，总共 **两次**，时间仍是线性 O(n)。  
- 空格分配的数学公式是 O(1) 计算，无需额外循环。  
- 只用了结果列表和若干整数变量，空间仍是 O(n)。

#### 代码（Python）

```python
from typing import List

def fullJustify(words: List[str], maxWidth: int) -> List[str]:
    """
    贪心分行 + O(1) 空格分配
    """
    res = []
    i = 0
    n = len(words)

    while i < n:
        # ---------- 1. 确定本行单词范围 ----------
        line_len = len(words[i])      # 本行单词字符总长度（不含空格）
        j = i + 1                     # 下一候选单词下标
        # 只要再放一个单词后，加上必需的空格数仍 ≤ maxWidth，就继续放
        while j < n and line_len + 1 + len(words[j]) <= maxWidth:
            line_len += 1 + len(words[j])   # +1 为单词之间最少的一个空格
            j += 1

        line_words = words[i:j]      # 本行所有单词
        num_words = len(line_words)

        # ---------- 2. 生成本行 ----------
        # 是否是最后一行或该行只有一个单词
        is_last_line = (j == n)
        if is_last_line or num_words == 1:
            # 左对齐：单词之间一个空格，剩余空格全部在行尾
            line = ' '.join(line_words)
            line += ' ' * (maxWidth - len(line))
        else:
            # 完全对齐：均匀分配空格
            total_spaces = maxWidth - sum(len(w) for w in line_words)   # 需要填的空格总数
            space_per_gap = total_spaces // (num_words - 1)            # 每两个单词之间至少多少空格
            extra = total_spaces % (num_words - 1)                     # 余下的空格，从左到右依次加

            line = ''
            for k in range(num_words - 1):
                line += line_words[k]                     # 加单词
                # 基本空格数 + 可能的额外空格（k < extra 时加 1）
                line += ' ' * (space_per_gap + (1 if k < extra else 0))
            line += line_words[-1]                       # 最后一个单词后不再加空格

        res.append(line)
        i = j                                            # 继续处理下一行

    return res
```

#### 复杂度

- **时间复杂度**：O(n)  
  解释：每个单词只在「确定行」阶段和「构造行」阶段各被访问一次，整体线性增长。相比暴力解的 O(n²)，这里省去了每行的二次遍历。

- **空间复杂度**：O(n)  
  解释：额外使用的空间只包括返回的结果列表（必须的）和若干整数变量，和输入规模同阶。

---

## 心得

- **核心技巧**：**贪心分行 + 计算空格的整数除法**。  
- **适用的题型**  
  1. 文本排版类（如 LeetCode 68 `Text Justification`、71 `Simplify Path` 中的路径拼接思路）。  
  2. 需要在固定宽度/容量内均匀分配资源的题目（如 “把石子均匀放进盒子” 之类的模拟题）。  
- **一句话总结**：**先把“装得最多”，再用“一次算空格”把行对齐**。

---

## 反思

- **第一反应**：把所有单词一次性放进列表，随后再逐行回头补空格。  
- **最容易踩的坑**  
  - **最后一行的左对齐**：忘记单词之间只留一个空格，剩余空格全放右侧。  
  - **只有一个单词的行**：同样需要左对齐，不能除以 `num_words-1`（会除以 0）。  
  - **空格余数分配**：余数应该从左往右分配，左边的缝隙会多一个空格。  
- **下次类似题的第一步**：**先确定每行能放哪些单词**（贪心），随后**立即计算该行需要的空格数**，一次完成对齐。