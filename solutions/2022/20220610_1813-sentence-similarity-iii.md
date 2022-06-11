# #1813. 句子相似性 III / Sentence Similarity III

> 难度：中等 · 标签：Array、Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/sentence-similarity-iii/)

---

## 题目（英文原版）

**Description**

You are given two strings sentence1 and sentence2, each representing a sentence composed of words. A sentence is a list of words that are separated by a single space with no leading or trailing spaces. Each word consists of only uppercase and lowercase English characters.
Two sentences s1 and s2 are considered similar if it is possible to insert an arbitrary sentence (possibly empty) inside one of these sentences such that the two sentences become equal. Note that the inserted sentence must be separated from existing words by spaces.
For example,
Given two sentences sentence1 and sentence2, return true if sentence1 and sentence2 are similar. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: sentence1 = "My name is Haley", sentence2 = "My Haley"
Output: true
Explanation:
sentence2 can be turned to sentence1 by inserting "name is" between "My" and "Haley".
```

**Example 2:**

```
Input: sentence1 = "of", sentence2 = "A lot of words"
Output: false
Explanation:
No single sentence can be inserted inside one of the sentences to make it equal to the other.
```

**Example 3:**

```
Input: sentence1 = "Eating right now", sentence2 = "Eating"
Output: true
Explanation:
sentence2 can be turned to sentence1 by inserting "right now" at the end of the sentence.
```

**Constraints**

- 1 <= sentence1.length, sentence2.length <= 100
- sentence1 and sentence2 consist of lowercase and uppercase English letters and spaces.
- The words in sentence1 and sentence2 are separated by a single space.

---

## 题目（中文翻译）

**题目描述**  
给定两个字符串 `sentence1` 和 `sentence2`，它们分别表示由单词组成的句子（句子是由单个空格分隔的单词序列，且首尾没有多余的空格）。每个单词仅由大小写英文字母构成。  

如果可以在其中一个句子内部（可能为空）插入任意句子，使得两个句子相等，则认为这两个句子 **相似**。插入的句子必须与原有单词之间用空格分隔。

换句话说，若存在一种方式可以在 `sentence1` 或 `sentence2` 中插入若干（也可能为零）单词，使得插入后两句完全相同，则返回 `true`，否则返回 `false`。

---

### 示例

**示例 1**  
```text
Input: sentence1 = "My name is Haley", sentence2 = "My Haley"
Output: true
Explanation:
sentence2 可以通过在 "My" 与 "Haley" 之间插入 "name is" 而变成 sentence1。
```

**示例 2**  
```text
Input: sentence1 = "of", sentence2 = "A lot of words"
Output: false
Explanation:
不存在一个单独的句子可以插入到任意一个原句中，使其等于另一个句子。
```

**示例 3**  
```text
Input: sentence1 = "Eating right now", sentence2 = "Eating"
Output: true
Explanation:
sentence2 可以在句尾插入 "right now" 从而得到 sentence1。
```

---

### 约束条件
- `1 <= sentence1.length, sentence2.length <= 100`
- `sentence1` 和 `sentence2` 只包含大小写英文字母和空格
- `sentence1` 与 `sentence2` 中的单词之间仅有单个空格分隔，且句首句尾没有空格

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两句话拆成单词列表后，枚举所有可能的“插入位置”，看能否让两句完全相同**。  
具体步骤如下：

1. 把 `sentence1`、`sentence2` 按空格分割成 `words1`、`words2`（相当于把一句话拆成一本书的词汇目录）。
2. 假设我们把 **较短的句子** 当作 “基准”，把 **较长的句子** 当作 “可能被插入词的句子”。  
   - 这样我们只需要在较长句子里挑选出一段连续的子串，删掉后看是否和较短句子一模一样。
3. 枚举 **删除子串的起始下标 `i`**（从 0 到 `len(long)-1`）和 **结束下标 `j`**（`i-1` 表示不删任何词），把 `long[i:j+1]` 这段词删除掉，得到新的词列表 `new_long`。
4. 把 `new_long` 与 `short` 逐词比较，若全部相同则返回 `True`，遍历结束仍未匹配则返回 `False`。

> **类比**：把长句子想象成一本书的章节，暴力解相当于把每一本可能的章节（连续的若干页）摘掉，看看剩下的内容是不是正好和另一本书的全部章节相同。

**为什么能得到正确答案**  
因为题目要求“在其中一条句子里插入（或删除）一段连续的词，使两句相等”。我们把插入过程逆向看作“在较长句子里删除一段连续的词”。只要遍历所有可能的删除区间，就一定能覆盖所有合法的插入方式。

#### 代码（Python）

```python
def areSentencesSimilar(sentence1: str, sentence2: str) -> bool:
    # 1️⃣ 把句子拆成单词列表
    w1 = sentence1.split()
    w2 = sentence2.split()

    # 2️⃣ 让 w_short 为较短的列表，w_long 为较长的列表
    if len(w1) <= len(w2):
        short, long = w1, w2
    else:
        short, long = w2, w1

    n, m = len(short), len(long)

    # 3️⃣ 枚举所有可能的删除区间 [i, j]（j < i 表示不删）
    for i in range(m + 1):                # 删除区间的左端点
        for j in range(i - 1, m):         # 删除区间的右端点（i-1 表示空区间）
            # 4️⃣ 把 long 的区间 [i, j] 删除，得到 new_long
            new_long = long[:i] + long[j + 1:]

            # 5️⃣ 如果长度已经不等，直接跳过
            if len(new_long) != n:
                continue

            # 6️⃣ 逐词比较
            if all(new_long[k] == short[k] for k in range(n)):
                return True

    return False
```

- `split()` 把句子按空格切成单词，类似于把一本书拆成章节目录。
- `long[:i] + long[j+1:]` 把第 `i` 到 `j`（含）这段词“删掉”，相当于把书的若干页撕掉。

#### 复杂度

- **时间复杂度**：`O(m² * n)`  
  - `m` 是较长句子的单词数，`n` 是较短句子的单词数。我们要遍历所有 `i, j`（约 `m²/2` 种），每次都要把剩余词列表和 `short` 逐词比较（`O(n)`），所以总体是二次方乘以线性。  
  - 用大白话说，就是“如果句子有 10 个词，最坏情况下要检查大约 100 次，每次检查 5 个词，总共 500 次操作”。
- **空间复杂度**：`O(m)`  
  - 需要保存拆分后的单词列表，以及在循环中产生的 `new_long`（最多 `m` 个词）。

> 由于 `sentence1`、`sentence2` 最长仅 100 个字符，暴力解在实际运行时还能接受，但仍然有更好的办法。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有可能的删除区间**，这导致二次方的时间。  
观察题意可以发现：

> 如果两句可以通过插入一段连续词变得相等，那么它们 **一定拥有相同的前缀**（从左往右）和 **相同的后缀**（从右往左），中间被“插入/删除”的部分正好是两句不相同的那段。

因此，只需要找出 **最长公共前缀** 和 **最长公共后缀**，检查这两段是否 **不重叠**（即没有冲突），即可判断是否相似。

实现步骤：

1. 把两句拆成单词列表 `a`、`b`。
2. 用两个指针 `i`（从左向右）和 `j`（从右向左）：
   - `i` 逐步向右移动，只要 `a[i] == b[i]`，说明前缀相同，就继续。
   - `j` 逐步向左移动，只要 `a[-1-j] == b[-1-j]`（即从尾部比较），说明后缀相同，就继续。
3. 当 `i` 与 `j` **相遇或交叉** 时，说明两句已经完全匹配（或者只差一个空插入），直接返回 `True`。
4. 否则，只要 **前缀长度 + 后缀长度 ≥ 较短句子的总词数**，说明中间的“缺口”可以通过插入一句任意词的方式填补，返回 `True`；否则返回 `False`。

> **类比**：想象两根绳子分别写着单词，从左边同时往右拉（找前缀），从右边同时往左拉（找后缀）。只要两边拉开的总长度已经覆盖了较短绳子的全部内容，剩下的空白部分就可以随意填充——这正是题目允许的“插入任意句子”。

#### 代码（Python）

```python
def areSentencesSimilar(sentence1: str, sentence2: str) -> bool:
    # 1️⃣ 拆词
    a = sentence1.split()
    b = sentence2.split()
    n, m = len(a), len(b)

    # 2️⃣ 让 a 为较短的列表，b 为较长的列表（方便后面比较）
    if n > m:
        a, b = b, a
        n, m = m, n

    # 3️⃣ 找最长公共前缀
    i = 0                     # 从左边开始的指针
    while i < n and a[i] == b[i]:
        i += 1                # 前缀相同，继续右移

    # 4️⃣ 找最长公共后缀
    j = 0                     # 从右边开始的指针
    while j < n - i and a[-1 - j] == b[-1 - j]:
        j += 1                # 后缀相同，继续左移

    # 5️⃣ 判断是否可以通过插入填补中间的空白
    #    前缀 i + 后缀 j 已经覆盖了较短句子的全部单词（i + j >= n）则成立
    return i + j >= n
```

- 第 3 步的 `while i < n and a[i] == b[i]` 找到 **公共前缀** 的长度 `i`。  
- 第 4 步的 `while j < n - i and a[-1 - j] == b[-1 - j]` 找到 **公共后缀** 的长度 `j`。这里的 `n - i` 防止前缀和后缀相交产生重复计数。  
- 第 5 步的判断 `i + j >= n` 就是“前缀+后缀已经覆盖了整个较短句子”。如果覆盖，则中间的缺口可以随意填充，从而满足题目要求。

#### 复杂度

- **时间复杂度**：`O(n)`（其中 `n` 为较短句子的单词数）  
  - 我们只遍历一次前缀和一次后缀，最多走过每个单词一次。相比暴力的二次方，这相当于“把检查次数从 100 次降到了 10 次”。
- **空间复杂度**：`O(1)`（不计输入的拆分列表）  
  - 只用了常数个指针变量 `i、j`，没有额外的数组或哈希表。

---

## 心得

- **核心技巧**：**双指针找最长公共前缀 + 最长公共后缀**，再用长度判断是否可以通过一次“插入”完成匹配。  
- **适用的题型**：
  1. *Sentence Similarity I/II*（判断两个句子是否全等或只允许删除单词）  
  2. *Longest Common Prefix*（在字符串数组中找公共前缀）  
  3. *Valid Palindrome II*（允许删除至多一个字符使回文）  
- **一句话总结**：只要把两句从两端“同步对齐”，看前后相同的部分能否把中间的空白全部覆盖，就是答案。

---

## 反思

- **拿到题目第一反应**：先把两句话拆成单词，然后想“遍历所有可能的插入位置”。这自然导向了暴力解。  
- **最容易踩的坑**：
  - **边界条件**：当两句完全相同或其中一句为空时，需要保证指针不会越界。  
  - **前后缀相交**：如果公共前缀已经占满了较短句子，后缀的比较必须停止（否则会重复计数）。代码中 `while j < n - i` 正是为此防止交叉。  
  - **大小写敏感**：题目说明大小写都视为不同字符，直接比较即可，无需额外处理。  
- **下次遇到同类题**，第一步应该想到**“从两端同步扫描，找出必然相同的部分”，再用**长度或计数**判断剩余部分是否可以通过一次自由操作（插入/删除/替换）完成匹配。这样往往能直接得到 O(n) 的最优解。