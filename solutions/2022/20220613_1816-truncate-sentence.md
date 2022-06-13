# #1816. **截断句子** / Truncate Sentence

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/truncate-sentence/)

---

## 题目（英文原版）

**Description**

A sentence is a list of words that are separated by a single space with no leading or trailing spaces. Each of the words consists of only uppercase and lowercase English letters (no punctuation).
You are given a sentence s​​​​​​ and an integer k​​​​​​. You want to truncate s​​​​​​ such that it contains only the first k​​​​​​ words. Return s​​​​​​ after truncating it.

**Examples**

**Example 1:**

```
Input: s = "Hello how are you Contestant", k = 4
Output: "Hello how are you"
Explanation:
The words in s are ["Hello", "how" "are", "you", "Contestant"].
The first 4 words are ["Hello", "how", "are", "you"].
Hence, you should return "Hello how are you".
```

**Example 2:**

```
Input: s = "What is the solution to this problem", k = 4
Output: "What is the solution"
Explanation:
The words in s are ["What", "is" "the", "solution", "to", "this", "problem"].
The first 4 words are ["What", "is", "the", "solution"].
Hence, you should return "What is the solution".
```

**Example 3:**

```
Input: s = "chopper is not a tanuki", k = 5
Output: "chopper is not a tanuki"
```

**Constraints**

- 1 <= s.length <= 500
- k is in the range [1, the number of words in s].
- s consist of only lowercase and uppercase English letters and spaces.
- The words in s are separated by a single space.
- There are no leading or trailing spaces.

---

## 题目（中文翻译）

**描述**  
一句话是由单个空格分隔的单词列表，且句首句尾没有空格。每个单词仅由大小写英文字母组成（不含标点符号）。  
给定一个句子 `s` 和一个整数 `k`，请将 `s` 截断，使其只保留前 `k` 个单词。返回截断后的句子 `s`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= s.length <= 500`
- `k` 的取值范围为 `[1, 句子中的单词数]`
- `s` 仅由大小写英文字母和空格组成
- 单词之间仅有一个空格分隔
- 句子首尾没有空格

**示例**

**示例 1**  
```
Input: s = "Hello how are you Contestant", k = 4
Output: "Hello how are you"
Explanation:
句子 s 中的单词为 ["Hello", "how", "are", "you", "Contestant"]。
前 4 个单词是 ["Hello", "how", "are", "you"]。
因此，应返回 "Hello how are you"。
```

**示例 2**  
```
Input: s = "What is the solution to this problem", k = 4
Output: "What is the solution"
Explanation:
句子 s 中的单词为 ["What", "is", "the", "solution", "to", "this", "problem"]。
前 4 个单词是 ["What", "is", "the", "solution"]。
因此，应返回 "What is the solution"。
```

**示例 3**  
```
Input: s = "chopper is not a tanuki", k = 5
Output: "chopper is not a tanuki"
Explanation:
句子 s 中的单词为 ["chopper", "is", "not", "a", "tanuki"]，共 5 个单词。
由于 k = 5，全部单词都被保留，返回原句。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整句话拆成一个**单词数组**，然后取前 `k` 个单词，再把它们用空格拼回去。  
- **拆分**：`str.split(' ')` 把字符串按空格切割，就像把一本书的句子拆成一本**字典**，每个单词就是字典的 **key**。  
- **取前 k**：数组的切片操作 `words[:k]`，相当于只取字典的前几页。  
- **拼接**：`' '.join(...)` 把这些单词再用空格连起来，恢复成一句话。

这个方法一定能得到正确答案，因为题目本身就要求“取前 k 个单词”，我们恰好把所有单词全部列出来，然后挑出前 k 个。

#### 代码（Python）

```python
def truncateSentence(s: str, k: int) -> str:
    # 1. 把句子按空格拆成单词列表
    words = s.split(' ')               # ["Hello", "how", "are", "you", "Contestant"]
    # 2. 取前 k 个单词
    first_k = words[:k]                # ["Hello", "how", "are", "you"]
    # 3. 用空格把它们重新拼成句子
    return ' '.join(first_k)           # "Hello how are you"
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  这里的 `n` 是字符串的长度。我们遍历一次把字符串拆成单词，又遍历一次把前 `k` 个单词拼回去，都是线性时间。

- **空间复杂度**：`O(n)`  
  `split` 会创建一个长度为单词数的数组，最坏情况下每个字符都是单独的单词（如 `"a b c d"`），所以需要额外的 `O(n)` 空间。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 `O(n)` 时间，但它额外用了一个数组来保存所有单词。我们可以**省掉这个数组**，直接在原字符串上扫描，找到第 `k‑1` 个空格的位置，然后截取子串。这样只需要 **常数级的额外空间**。

1. **遍历字符**：从左到右一次遍历字符串，遇到空格就计数。  
2. **计数到 k‑1**：因为第 `k` 个单词之前恰好有 `k‑1` 个空格。  
3. **截取子串**：当计数到 `k‑1` 时，记下当前空格的下标 `pos`，返回 `s[:pos]`（不包括空格本身）。  
4. **特殊情况**：如果遍历完整个字符串仍未计数到 `k‑1`，说明句子本身就只有 `k` 个或更少单词，直接返回原字符串。

这样我们只用了一个计数器和一个位置变量，空间开销降到 `O(1)`。

#### 代码（Python）

```python
def truncateSentence(s: str, k: int) -> str:
    space_cnt = 0          # 已经遇到的空格数量
    for i, ch in enumerate(s):
        if ch == ' ':      # 遇到空格
            space_cnt += 1
            if space_cnt == k:   # 第 k-1 个空格后，已经完整看到 k 个单词
                return s[:i]     # 截取到空格之前的子串
    # 循环结束仍未达到 k-1 个空格，说明 s 本身就只有 k（或更少）个单词
    return s
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  仍然只遍历一次字符串，`n` 为字符数。相比暴力解没有额外的遍历或操作，时间上是一样的。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量（计数器、下标），不随输入规模增长，是真正的常数空间。

---

## 心得

- **核心技巧**：**一次遍历 + 计数**，在需要“前 k 项”或“第 k 项”时，往往可以通过计数在原数组/字符串上直接定位，避免额外的存储。  
- **适用题型**：  
  1. “前 k 个字符/单词”类截断题（如 LeetCode 1820 `Maximum Number of Accepted Invitations`）。  
  2. “第 k 次出现的字符”类搜索题（如 LeetCode 1688 `Count of Matches in Tournament` 的变形）。  
- **解题钥匙**：**“找第 k‑1 个分隔符的位置”**。

---

## 反思

- **第一反应**：直接把句子 `split` 成数组，再取前 `k`，因为这一步最符合直觉。  
- **最容易踩的坑**：  
  - 忘记处理 **恰好等于 k 个单词** 的情况，直接返回 `s[:i]` 可能会把最后一个单词的空格也截掉。  
  - 对 **空格计数** 的理解不清晰：要记住前 `k` 个单词之间只有 `k‑1` 个空格。  
- **下次类似题的第一步**：先问自己“是否可以只在原字符串上定位第 k‑1 个分隔符”，如果能，就尝试 **一次遍历 + 计数** 的思路，而不是直接构造额外的数据结构。