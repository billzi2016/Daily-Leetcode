# #1592. 重新排列单词间的空格 / Rearrange Spaces Between Words

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/rearrange-spaces-between-words/)

---

## 题目（英文原版）

**Description**

You are given a string text of words that are placed among some number of spaces. Each word consists of one or more lowercase English letters and are separated by at least one space. It's guaranteed that text contains at least one word.
Rearrange the spaces so that there is an equal number of spaces between every pair of adjacent words and that number is maximized. If you cannot redistribute all the spaces equally, place the extra spaces at the end, meaning the returned string should be the same length as text.
Return the string after rearranging the spaces.

**Examples**

**Example 1:**

```
Input: text = "  this   is  a sentence "
Output: "this   is   a   sentence"
Explanation: There are a total of 9 spaces and 4 words. We can evenly divide the 9 spaces between the words: 9 / (4-1) = 3 spaces.
```

**Example 2:**

```
Input: text = " practice   makes   perfect"
Output: "practice   makes   perfect "
Explanation: There are a total of 7 spaces and 3 words. 7 / (3-1) = 3 spaces plus 1 extra space. We place this extra space at the end of the string.
```

**Constraints**

- 1 <= text.length <= 100
- text consists of lowercase English letters and ' '.
- text contains at least one word.

---

## 题目（中文翻译）

给定一个字符串 `text`，其中包含若干单词，这些单词被若干空格分隔。每个单词由一个或多个小写英文字母组成，且相邻单词之间至少有一个空格。保证 `text` 至少包含一个单词。

请重新分配这些空格，使得相邻单词之间的空格数目相等，并且该空格数目尽可能大。如果无法将所有空格完全平均分配，则将多余的空格放在字符串的末尾，使得返回的字符串长度与原 `text` 长度相同。

返回重新排列空格后的字符串。

## 示例

### 示例 1
**输入**  
`text = "  this   is  a sentence "`  

**输出**  
`"this   is   a   sentence"`  

**解释**  
总共有 9 个空格，单词数为 4。我们可以把 9 个空格均匀地分配到单词之间：`9 / (4-1) = 3` 个空格。

### 示例 2
**输入**  
`text = " practice   makes   perfect"`  

**输出**  
`"practice   makes   perfect "`  

**解释**  
总共有 7 个空格，单词数为 3。`7 / (3-1) = 3` 个空格，剩余 1 个空格放在字符串末尾。

## 约束条件
- `1 <= text.length <= 100`
- `text` 只包含小写英文字母和空格字符 `' '`。
- `text` 至少包含一个单词。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **遍历整个字符串**，顺便统计一共有多少个空格 `total_spaces`，并把出现的每个单词收集到一个列表 `words` 中。  
   - 这里的“单词”可以类比成一本字典里的词条，空格就像是字典的页码间隔。我们只关心词条本身，不在乎它们之间有多少页码（空格）。
2. **把空格重新摆放**。  
   - 先算出相邻单词之间应该放多少个空格 `gap = total_spaces // (len(words)-1)`（如果只有一个单词，这一步会除以 0，后面会单独处理）。  
   - 再算出剩下的“零头”空格 `tail = total_spaces % (len(words)-1)`，这些空格要全部放在最末尾。  
3. **用字符串拼接**把单词和空格一个一个地连起来。  
   - 由于 Python 中字符串是不可变的，每次 `result = result + something` 都会产生一个新字符串，等价于把旧的字符复制一遍再加上新字符。这样在最坏情况下会出现 **O(n²)** 的时间开销（把 n 个字符复制了 n 次）。

> **为什么这样一定能得到正确答案？**  
> 我们先把所有空格数算出来，再平均分配到每两个相邻单词之间，保证了“相邻单词间的空格数相等且最大”。剩余的空格只能放在最末尾，否则会破坏相等的要求。因此只要按上述公式计算，就一定满足题意。

#### 代码（Python）

```python
def reorderSpaces_bruteforce(text: str) -> str:
    # 1. 统计空格数，收集单词
    total_spaces = 0          # 空格总数
    words = []                # 用来存放所有单词
    i = 0
    n = len(text)
    while i < n:
        if text[i] == ' ':
            total_spaces += 1
            i += 1
        else:
            # 遇到字母，开始读取一个完整的单词
            j = i
            while j < n and text[j] != ' ':
                j += 1
            words.append(text[i:j])   # 把单词加入列表
            i = j                     # 继续从 j 位置往后扫描

    # 2. 计算每个间隔应该放多少空格，和尾部的多余空格
    if len(words) == 1:          # 只有一个单词，所有空格都放在末尾
        gap = 0
        tail = total_spaces
    else:
        gap = total_spaces // (len(words) - 1)   # 每两个单词之间的空格数
        tail = total_spaces % (len(words) - 1)   # 剩余的空格

    # 3. 逐个拼接（每次 + 都会生成新字符串，导致 O(n²)）
    result = ""
    for idx, w in enumerate(words):
        result = result + w                # 先加单词
        if idx != len(words) - 1:          # 不是最后一个单词，需要加间隔空格
            result = result + " " * gap    # 加 gap 个空格
    result = result + " " * tail          # 最后加上尾部空格

    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：我们在第 3 步里使用 `result = result + something`，每次拼接都会把已有的字符串全部复制一遍。若字符串长度为 `n`，大约会复制 `1 + 2 + … + n ≈ n²/2` 次，所以是二次时间。
- **空间复杂度**：`O(n)`  
  - 解释：需要存放原始单词列表 `words`（最多占 `n` 个字符）以及最终返回的结果字符串，同样是 `n` 量级的空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于第 3 步的逐字符拼接。我们只需要把所有要拼好的片段先放到一个 **列表** 中，最后一次性用 `''.join(list)` 把它们合并。列表的 `append` 操作是 **O(1)** 的，`join` 在内部只遍历一次字符串，所以整体可以降到线性时间。

优化步骤：

1. **统计空格数 & 收集单词** —— 这一步仍然是一次遍历，时间 `O(n)`，空间 `O(k)`（`k` 为单词数）。
2. **计算间隔空格数** —— 与暴力解相同，只是多了对“只有一个单词”的特判。
3. **构造结果列表**  
   - 把每个单词依次 `append` 到 `parts` 列表。  
   - 如果不是最后一个单词，紧接着 `append` `gap` 个空格（可以直接用 `" " * gap` 生成一个完整的空格块）。  
   - 循环结束后，再 `append` `tail` 个空格。  
4. **一次性合并**：`result = ''.join(parts)`。这一步内部会先算出所有子串的总长度，然后一次性拷贝到新字符串里，时间正比于最终字符串长度 `n`。

> **为什么这样更快？**  
> 列表的 `append` 只在内存里记录指针，不会产生拷贝。真正拷贝只在 `join` 的那一刻完成一次，等价于把所有块拼成一条“流水线”。因此整体时间从二次降到了线性 `O(n)`。

#### 代码（Python）

```python
def reorderSpaces(text: str) -> str:
    """
    最优实现：一次遍历统计 + 列表 + 一次 join
    """
    # 1. 统计空格数，收集所有单词
    total_spaces = text.count(' ')                # 直接使用 count，O(n)
    words = [w for w in text.split() if w]        # split 会把连续空格视为分隔符，得到所有单词

    # 2. 计算每个间隔应该放多少空格，和尾部的多余空格
    if len(words) == 1:                           # 只有一个单词的特殊情况
        gap = 0
        tail = total_spaces
    else:
        gap = total_spaces // (len(words) - 1)    # 平均分配到每两个单词之间
        tail = total_spaces % (len(words) - 1)    # 剩余的空格放在末尾

    # 3. 构造结果的各个片段（使用列表避免频繁拼接）
    parts = []
    for i, w in enumerate(words):
        parts.append(w)                           # 先放单词
        if i != len(words) - 1:                   # 不是最后一个单词，需要加间隔空格
            parts.append(' ' * gap)               # 一次性生成 gap 个空格

    parts.append(' ' * tail)                      # 最后再加上尾部空格

    # 4. 一次性合并为最终字符串
    return ''.join(parts)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：`count`、`split`、遍历 `words`、以及最后的 `join` 都只各自遍历一次字符，总共是线性时间。相比暴力解省去了大量重复拷贝。
- **空间复杂度**：`O(n)`  
  - 解释：需要存放 `words`（所有单词）以及 `parts`（每个单词和空格块），总大小不超过原字符串长度 `n`，属于线性空间。

---

## 心得

- **核心技巧**：一次遍历统计 + 使用列表 + `''.join` 合并，避免在循环里频繁使用 `+` 拼接字符串导致的二次时间。
- **适用场景**：
  1. **字符串重组**（如把句子中的单词逆序、删除多余空格等）。
  2. **大量字符拼接**（如构造 CSV 行、日志拼接等），均推荐使用列表 + `join`。
  3. **分割-重组**（如 LeetCode 151（翻转字符串里的单词））同样可以用此技巧提升效率。
- **一句话总结**：**“先收集，再一次性合并”，是处理大规模字符串拼接的钥匙。**

---

## 反思

- **第一反应**：看到“空格重新分配”，立刻想到先数空格、数单词，再算平均值，然后把空格塞回去。
- **最容易踩的坑**：
  1. **只有一个单词**时除以零的错误，需要单独处理。
  2. **连续空格**会让 `split()` 产生空字符串，需要过滤或直接使用 `text.split()`（它已经会自动忽略空串）。
  3. **返回字符串长度必须与原字符串相同**——忘记把剩余空格放在末尾会导致长度不匹配。
- **下次遇到同类题**：第一步先 **“计数 + 分块”**，把需要的资源（空格、单词）统计清楚；第二步决定 **“如何高效拼接”**（列表 + `join`），而不是在循环里直接 `+`。这样可以快速写出既正确又高效的代码。