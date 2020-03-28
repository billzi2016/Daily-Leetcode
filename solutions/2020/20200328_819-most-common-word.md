# #819. 最常出现的单词 / Most Common Word

> 难度：简单 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/most-common-word/)

---

## 题目（英文原版）

**Description**

Given a string paragraph and a string array of the banned words banned, return the most frequent word that is not banned. It is guaranteed there is at least one word that is not banned, and that the answer is unique.
The words in paragraph are case-insensitive and the answer should be returned in lowercase.
Note that words can not contain punctuation symbols.

**Examples**

**Example 1:**

```
Input: paragraph = "Bob hit a ball, the hit BALL flew far after it was hit.", banned = ["hit"]
Output: "ball"
Explanation: 
"hit" occurs 3 times, but it is a banned word.
"ball" occurs twice (and no other word does), so it is the most frequent non-banned word in the paragraph. 
Note that words in the paragraph are not case sensitive,
that punctuation is ignored (even if adjacent to words, such as "ball,"), 
and that "hit" isn't the answer even though it occurs more because it is banned.
```

**Example 2:**

```
Input: paragraph = "a.", banned = []
Output: "a"
```

**Constraints**

- 1 <= paragraph.length <= 1000
- paragraph consists of English letters, space ' ', or one of the symbols: "!?',;.".
- 0 <= banned.length <= 100
- 1 <= banned[i].length <= 10
- banned[i] consists of only lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `paragraph` 和一个禁用词字符串数组 `banned`，返回在 `paragraph` 中出现频率最高且不在禁用词列表中的单词。题目保证至少存在一个不在禁用词列表中的单词，且答案唯一。  
`paragraph` 中的单词不区分大小写，返回的答案应为全小写形式。  
注意，单词中不能包含标点符号。

**示例 1**  
```text
Input: paragraph = "Bob hit a ball, the hit BALL flew far after it was hit.", banned = ["hit"]
Output: "ball"
```
**解释**  
- 单词 `"hit"` 出现了 3 次，但它是禁用词。  
- 单词 `"ball"` 出现了两次（其他单词都没有出现两次），因此它是段落中出现频率最高的非禁用词。  
- `paragraph` 中的单词不区分大小写，标点符号会被忽略（即使紧邻单词，如 `"ball,"`），并且即使 `"hit"` 出现次数更多也不是答案，因为它被列入了禁用词。

**示例 2**  
```text
Input: paragraph = "a.", banned = []
Output: "a"
```

**约束条件**  
- `1 <= paragraph.length <= 1000`  
- `paragraph` 只包含英文字母、空格 `' '`，以及以下符号之一：`!?',;.`  
- `0 <= banned.length <= 100`  
- `1 <= banned[i].length <= 10`  
- `banned[i]` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 把段落 `paragraph` 按照空格切分成一个个“原始”单词（这里的单词可能带有标点，例如 `"ball,"`）。  
2. 对每一个单词，去掉两端的标点并转成小写，得到真正的单词。  
3. 用两层循环遍历所有单词，统计每个单词出现的次数（如果它在 `banned` 列表里就直接跳过）。  
4. 最后挑出出现次数最多的非禁用单词。

> **数据结构类比**：  
> - **哈希表（字典）** 就像一本查字典，单词是“词”，出现次数是对应的“页码”。我们把每次看到的单词记到字典里，遇到相同的词就把页码（计数）加一。  
> - **两层循环** 像是“把所有人都请进教室，让每个人分别点名一次”，时间会很久。

这种做法一定能得到正确答案，因为我们把**所有可能的单词**都枚举了一遍，并且逐个计数。

#### 代码（Python）

```python
import string

def most_common_word_brute(paragraph: str, banned):
    # 1️⃣ 把段落按照空格拆成“原始”单词列表
    raw_words = paragraph.split()
    
    # 2️⃣ 把 banned 列表转成集合，查找更快（像把禁用词装进一本小册子，翻页 O(1)）
    banned_set = set(banned)

    # 3️⃣ 暴力计数：对每个单词都遍历一次，统计出现次数
    max_word = ""
    max_cnt = 0

    for i in range(len(raw_words)):
        # 取出第 i 个原始单词
        w = raw_words[i]
        # 去掉两端的标点（.,!?'等），并全部转成小写
        w = w.strip(string.punctuation).lower()
        if not w or w in banned_set:        # 空字符串或禁用词直接跳过
            continue

        # 统计 w 在整个列表中出现了多少次（第二层循环）
        cnt = 0
        for j in range(len(raw_words)):
            w2 = raw_words[j].strip(string.punctuation).lower()
            if w2 == w:
                cnt += 1

        # 更新最大值
        if cnt > max_cnt:
            max_cnt = cnt
            max_word = w

    return max_word
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：`n` 是段落中单词的数量。外层循环遍历 `n` 次，内层又要遍历 `n` 次去统计出现次数，所以总共是 `n × n`，这在实际里相当于“把所有人都叫两遍”。  
- **空间复杂度**：`O(m)`  
  解释：这里用了一个集合保存禁用词，`m` 是 `banned` 的长度（最多 100），除此之外只用了常数级的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **第二层循环**：每次都要遍历全部单词去统计，这导致 `O(n²)`。  
我们可以把 **“统计出现次数”** 的工作一次性完成，而不是每次都重新算。思路如下：

1. **一次遍历** 整个段落，顺序读取字符。  
   - 遇到字母就累积成当前单词（使用 `list` 或 `str`）。  
   - 遇到空格或标点时，说明一个单词结束，把它加入计数器。  
2. 用 **哈希表（字典）** 直接记录每个单词出现的次数。  
   - 只要单词不在 `banned` 集合里，就在字典里 `cnt[word] += 1`。  
3. 遍历完后，字典里已经保存了所有非禁用单词的出现次数，直接取出现次数最大的键即可。

> **核心技巧解释**  
> - **哈希表**：把每个单词当作“钥匙”，出现次数当作“价值”。查询、插入、更新的时间都是 `O(1)`，所以统计过程是线性的。  
> - **一次遍历**：把“读取字符 → 形成单词 → 计数”这三个步骤连在一起做，就像在流水线上一次完成，不需要再回头。

> **类比**：想象我们在读一本书，同时在旁边的记事本上记录每个单词出现的次数。每看到一个完整的单词，就在记事本上把对应的计数加一，整个过程只需要读一遍书。

#### 代码（Python）

```python
import string
from collections import defaultdict

def most_common_word(paragraph: str, banned):
    # 1️⃣ 把 banned 列表转成集合，查找 O(1)
    banned_set = set(banned)

    # 2️⃣ 用 defaultdict 自动把不存在的键初始化为 0
    freq = defaultdict(int)

    # 3️⃣ 读取字符，构造单词
    word_chars = []                     # 暂存当前单词的字符列表
    for ch in paragraph:
        if ch.isalpha():                # 是字母就加入当前单词
            word_chars.append(ch.lower())
        else:                           # 碰到空格或标点，单词结束
            if word_chars:              # 防止连续的标点产生空单词
                word = ''.join(word_chars)
                if word not in banned_set:
                    freq[word] += 1    # 计数
                word_chars = []        # 重置，准备下一个单词

    # 处理最后一个单词（段落可能不以标点结尾）
    if word_chars:
        word = ''.join(word_chars)
        if word not in banned_set:
            freq[word] += 1

    # 4️⃣ 找出出现次数最多的单词
    # max 函数的 key 参数指定比较的依据，这里是字典的 value（出现次数）
    most_common = max(freq.keys(), key=lambda w: freq[w])
    return most_common
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：`n` 为段落字符数（最长 1000），我们只遍历一次，每个字符的处理都是 `O(1)`。相比暴力的 `O(n²)`，这相当于“只读一遍书”。  
- **空间复杂度**：`O(k)`  
  解释：`k` 为不同单词的数量（最坏情况下每个字符都是单独的单词），我们需要在哈希表里保存每个单词的计数。除此之外只用了常数级的临时变量。

---

## 心得

- **核心技巧**：使用哈希表统计频率 + 一次遍历提取单词（即“分词 + 计数”。）  
- **适用的题型**：  
  1. **字符统计**：如 `Top K Frequent Words`、`Number of Good Pairs`。  
  2. **分词统计**：如 `Word Subsets`、`Sentence Similarity`.  
  3. **出现次数最高的元素**：如 `Majority Element`（虽然思路略有不同）。  
- **一句话总结解题钥匙**：**“一次遍历+哈希表” 能把所有计数工作在 O(n) 内完成。**

---

## 反思

- **第一反应**：先把段落拆成单词，再用两个循环去计数。  
- **最容易踩的坑**  
  1. **标点处理**：直接 `split()` 会把标点留在单词里，需要额外去除。  
  2. **大小写**：题目要求不区分大小写，忘记统一转成小写会导致同一个单词被当成不同词。  
  3. **末尾单词**：段落可能不以标点或空格结束，需要在循环结束后手动处理最后一个累积的单词。  
- **下次遇到同类题**：第一步想到 “**一次扫描并实时更新哈希表**”，把“提取/统计”合并在一次遍历里，而不是先切分再二次遍历。