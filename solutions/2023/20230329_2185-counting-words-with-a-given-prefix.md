# #2185. **统计具有给定前缀的单词** / Counting Words With a Given Prefix

> 难度：简单 · 标签：Array、String、String Matching · [LeetCode 链接](https://leetcode.com/problems/counting-words-with-a-given-prefix/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words and a string pref.
Return the number of strings in words that contain pref as a prefix.
A prefix of a string s is any leading contiguous substring of s.

**Examples**

**Example 1:**

```
Input: words = ["pay","attention","practice","attend"], pref = "at"
Output: 2
Explanation: The 2 strings that contain "at" as a prefix are: "attention" and "attend".
```

**Example 2:**

```
Input: words = ["leetcode","win","loops","success"], pref = "code"
Output: 0
Explanation: There are no strings that contain "code" as a prefix.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length, pref.length <= 100
- words[i] and pref consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组（array of strings）`words` 和一个字符串 `pref`，返回 `words` 中以 `pref` 作为前缀（prefix）的字符串数量。

字符串 `s` 的前缀是指 `s` 的任意一个**连续的**（contiguous）前导子串（leading substring）。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**

**示例 1:**  
Input: words = ["pay","attention","practice","attend"], pref = "at"  
Output: 2  
Explanation: 以 `"at"` 为前缀的两个字符串是 `"attention"` 和 `"attend"`。

**示例 2:**  
Input: words = ["leetcode","win","loops","success"], pref = "code"  
Output: 0  
Explanation: 没有字符串以 `"code"` 为前缀。

**约束条件**  
- `1 <= words.length <= 100`  
- `1 <= words[i].length, pref.length <= 100`  
- `words[i]` 和 `pref` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 `words` 里每一个单词都拿出来，和给定的前缀 `pref` 比较一下，看看它是不是以 `pref` 开头。如果是，就把计数器 `ans` 加一。  

- **用到的数据结构**：这里只需要一个 **列表**（存放所有单词）和一个 **整数计数器**。列表就像装书的书架，`words[i]` 就是第 `i` 本书的标题；计数器 `ans` 像是记录“符合条件的书有几本”的笔记本。  
- **为什么正确**：题目要求统计所有 **前缀匹配** 的单词，遍历一次列表就能检查每个单词是否满足条件，所有满足的自然都会被计入。  
- **复杂度分析**：  
  - 对每个单词我们都要检查它的前 `len(pref)` 个字符是否相同，这一步的时间是 `O(len(pref))`。  
  - 列表里有 `n = len(words)` 个单词，所以总时间是 `O(n * len(pref))`。在最坏情况下，`len(pref)` 可能和单词本身一样长，记作 `m`，于是时间复杂度可写成 **`O(n·m)`**。  
  - 空间上我们只用了常数个额外变量（计数器、循环变量），所以是 **`O(1)`**，即不随输入规模增长而增长。

> **大白话**：如果把每个单词想象成一根绳子，前缀就是绳子最前面的那段。我们把每根绳子都拉出来，检查最前面的那段是不是和 `pref` 完全一样，检查一次需要花一点时间（绳子长度），所有绳子都检查完就是总时间。

#### 代码（Python）

```python
def prefixCount(words, pref):
    """
    :param words: List[str]   # 所有单词的列表
    :param pref:  str         # 要匹配的前缀
    :return: int              # 符合条件的单词数量
    """
    ans = 0                     # 计数器，初始为 0
    for w in words:             # 遍历每个单词
        # Python 自带的 startswith 相当于“检查前缀”，如果匹配则返回 True
        if w.startswith(pref): # 前缀相同？
            ans += 1           # 计数器加一
    return ans                  # 返回最终计数
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - `n` 是单词数量，`m = len(pref)` 是前缀的长度。每个单词最多要比较 `m` 个字符。
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（`ans`、循环变量），不随 `words` 长度增长。

---

### 2. 最优解

#### 思路  

对于本题的单次查询（只给一次 `pref`），**暴力遍历已经是最优**的时间复杂度了，因为我们必须至少看一遍每个单词才能确定它是否匹配，时间下界是 `Ω(n)`。  
如果出现 **多次查询**（同一批单词要匹配多个前缀），可以考虑构建 **Trie（前缀树）**，在一次构建后每次查询的时间可以降到 `O(len(pref))`。这里仍然演示一下如何使用 Trie，帮助大家了解一种常见的前缀处理技巧。

**核心概念——Trie（前缀树）**  
- 想象把所有单词写在一棵倒立的树里，每条边对应一个字符，从根到某个节点的路径就是一个前缀。  
- 插入单词时，只需要沿着对应字符的边往下走，如果不存在就新建。  
- 查询前缀时，只要沿着前缀的字符走到底，如果能走完就说明有单词以该前缀开头。

下面给出两种实现方式，任选其一即可：

1. **直接遍历**（上面的暴力解）——代码更短，适用于一次查询。  
2. **Trie + 计数**——适用于大量前缀查询的场景。

#### 代码（Python）

```python
# ---------- 方案 1：直接遍历（最简） ----------
def prefixCount_brute(words, pref):
    ans = 0
    for w in words:
        if w.startswith(pref):
            ans += 1
    return ans


# ---------- 方案 2：Trie + 计数 ----------
class TrieNode:
    def __init__(self):
        self.children = {}          # dict: char -> TrieNode
        self.cnt = 0                # 以该节点为前缀的单词数量

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            # 若该字符的子节点不存在则创建
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.cnt += 1          # 经过该节点的单词计数 +1

    def countPrefix(self, pref):
        node = self.root
        for ch in pref:
            if ch not in node.children:
                return 0           # 前缀不存在
            node = node.children[ch]
        return node.cnt           # 该节点记录的就是前缀出现的次数


def prefixCount_trie(words, pref):
    """
    对于大量查询场景更快。
    """
    trie = Trie()
    for w in words:               # 先把所有单词放进 Trie
        trie.insert(w)
    return trie.countPrefix(pref) # 查询一次前缀出现的次数
```

> **关键行中文注释**已经写在代码里，帮助大家快速定位每一步的作用。

#### 复杂度

| 方案 | 时间复杂度 | 空间复杂度 |
|------|------------|------------|
| 直接遍历 | `O(n·m)`（`n` 为单词数，`m = len(pref)`）<br>每个单词最多比较 `m` 个字符 | `O(1)` 只用常数额外空间 |
| Trie | 构建阶段 `O(N·L)`，查询阶段 `O(m)`<br>其中 `N` 为单词数，`L` 为所有单词平均长度 | `O(N·L)` 用于存储整个 Trie（每个字符一个节点） |

- 对于本题只有一次查询，**直接遍历** 更简洁且空间更省；如果你要在同一组单词上做很多前缀查询，**Trie** 能把每次查询的时间降到只和前缀长度 `m` 有关。

---

## 心得

- **核心技巧**：利用字符串的 `startswith`（或手动比较前缀）逐个检查。  
- **适用的题型**：  
  1. 统计以给定前缀开头的单词数量（本题）。  
  2. 判断一个字符串是否是另一个字符串的前缀/后缀。  
  3. 多次前缀查询时使用 **Trie**（前缀树）提升效率。  
- **一句话总结**：**“遍历 + 前缀匹配” 是解决单次前缀计数的最直接钥匙。**  

---

## 反思

- **第一反应**：直接遍历每个单词，用 `startswith` 判断是否匹配。  
- **最容易踩的坑**：  
  - 忘记考虑空字符串的情况（虽然约束里最短为 1）。  
  - 把 “包含前缀” 当成 “出现过一次” 误写为 `in` 判断，会把中间出现的情况算进去。  
  - 对大小写不敏感的题目忘记统一转小写。  
- **下次遇到同类题**：第一步先判断是**单次查询**还是**多次查询**。  
  - 单次查询 → 直接遍历 + `startswith`。  
  - 多次查询 → 考虑构建 Trie 或者把所有单词排序后二分搜索前缀范围。