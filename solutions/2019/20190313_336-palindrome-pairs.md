# #336. 回文对 / Palindrome Pairs

> 难度：困难 · 标签：Array、Hash Table、String、Trie · [LeetCode 链接](https://leetcode.com/problems/palindrome-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of unique strings words.
A palindrome pair is a pair of integers (i, j) such that:
Return an array of all the palindrome pairs of words.
You must write an algorithm with O(sum of words[i].length) runtime complexity.

**Examples**

**Example 1:**

```
Input: words = ["abcd","dcba","lls","s","sssll"]
Output: [[0,1],[1,0],[3,2],[2,4]]
Explanation: The palindromes are ["abcddcba","dcbaabcd","slls","llssssll"]
```

**Example 2:**

```
Input: words = ["bat","tab","cat"]
Output: [[0,1],[1,0]]
Explanation: The palindromes are ["battab","tabbat"]
```

**Example 3:**

```
Input: words = ["a",""]
Output: [[0,1],[1,0]]
Explanation: The palindromes are ["a","a"]
```

**Constraints**

- 1 <= words.length <= 5000
- 0 <= words[i].length <= 300
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始、且元素互不相同的字符串数组 `words`。  
如果存在一对整数 `(i, j)`，满足 `i != j` 且 `words[i] + words[j]`（字符串拼接）是回文串（palindrome），则称 `(i, j)` 为一个 **回文对**。  
请返回所有满足条件的回文对 `(i, j)`，返回的答案可以以任意顺序排列。

**要求**  
必须设计出时间复杂度为 `O( Σ words[i].length )` 的算法。

**示例**

*示例 1*  
```
Input: words = ["abcd","dcba","lls","s","sssll"]
Output: [[0,1],[1,0],[3,2],[2,4]]
Explanation: 这些回文串分别是 ["abcddcba","dcbaabcd","slls","llssssll"]
```

*示例 2*  
```
Input: words = ["bat","tab","cat"]
Output: [[0,1],[1,0]]
Explanation: 这些回文串分别是 ["battab","tabbat"]
```

*示例 3*  
```
Input: words = ["a",""]
Output: [[0,1],[1,0]]
Explanation: 这些回文串分别是 ["a","a"]
```

**约束条件**
- `1 <= words.length <= 5000`
- `0 <= words[i].length <= 300`
- `words[i]` 仅由小写英文字母组成，且数组中的字符串互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每两个单词都拼在一起，检查拼好的字符串是不是回文。

- **遍历所有 (i, j) 对**：对 `words` 中的每个下标 `i`，再遍历一次所有下标 `j (j≠i)`，把 `words[i] + words[j]` 拼起来。
- **判断回文**：把拼好的字符串从左往右、从右往左逐字符比较，看到不相同就可以立刻否定。

> **类比**：把每本书的标题想成单词，暴力解就像把每两本书的标题都贴在一起，然后用放大镜逐字检查是不是“前后对称的句子”。  
> **为什么一定对**：只要把所有可能的组合都检查一遍，肯定不会漏掉任何符合条件的配对。

#### 代码（Python）

```python
def palindromePairs_brute(words):
    """
    暴力解法：两层循环遍历所有不同下标组合
    """
    n = len(words)
    res = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue                      # 不能和自己配对
            s = words[i] + words[j]          # 把两个单词拼接
            # 检查 s 是否是回文
            if s == s[::-1]:                 # Python 的切片技巧：逆序字符串
                res.append([i, j])
    return res
```

#### 复杂度

- **时间复杂度**：`O(n²·k)`  
  - `n` 是单词数量，`k` 是每个单词的平均长度。两层循环产生 `n²` 组合，每次拼接后要遍历 `k`（最坏情况是两个最长单词相加）来判断回文。  
  - 用“大白话”说，就是如果有 5000 本书，每本标题 300 个字母，光检查所有配对就要跑 **5000² ≈ 25 百万** 次，每次再看 600 个字母，根本跑不完。

- **空间复杂度**：`O(1)`（不计输出列表）  
  - 只用了常数级别的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查大量不可能的组合**。我们要把“找配对”这件事提前做好准备，让每个单词只检查 **自身的若干切分**，而不是所有别的单词。

关键观察：

1. **回文的构成**  
   假设我们想要 `words[i] + words[j]` 成为回文。把 `words[i]` 当作左边，`words[j]` 当作右边。  
   - 若 `words[i]` 的左半部分是回文，而 `words[i]` 的右半部分的 **逆序** 正好等于某个单词 `words[j]`，则两者拼起来一定是回文。  
   - 同理，若 `words[i]` 的右半部分是回文，而左半部分的逆序是某个单词 `words[j]`，也可以构成回文。

2. **把所有单词的逆序放进哈希表**  
   哈希表（dictionary）就像一本“单词 → 下标” 的字典，查找某个逆序字符串是否存在，只需要 **O(1)** 时间。

3. **遍历每个单词的所有切分**  
   对于单词 `w`，把它切成 `left|right`（包括空串），分别检查两种情况：
   - `left` 是回文 → 如果 `reverse(right)` 在哈希表且不是 `w` 本身，则 `reverse(right) + w` 是回文。
   - `right` 是回文 → 如果 `reverse(left)` 在哈希表且不是 `w` 本身，则 `w + reverse(left)` 是回文。

4. **特殊情况：空串**  
   空串本身是回文。只要数组里出现空串，所有单独是回文的单词（比如 `"a"`、`"aba"`）都可以和空串配对，形成回文。

5. **时间复杂度分析**  
   - 对每个单词，我们遍历它的每一个切分点，最多 `len(w)+1` 次。每次只做 O(1) 的哈希查找和 O(k) 的回文检查（`k` 为切分后子串的长度）。  
   - 所有单词的切分次数之和恰好等于 **所有字符的总数**（记作 `L = Σ|words[i]|`）。因此整体时间是 **O(L)**，满足题目要求。

> **类比**：把每本书的标题倒着写成一本“逆序标题目录”。找配对时，只要把一本书的标题切成左/右两段，检查左段是不是“前半对称”，再去目录里找右段的逆序标题——这样每本书只需要检查自己的几段，而不是所有别的书。

#### 代码（Python）

```python
def palindromePairs(words):
    """
    高效解法：利用哈希表存储每个单词的逆序，遍历每个单词的所有切分点。
    复杂度 O(total length of all words)
    """
    # 1. 建立逆序哈希表：rev_word -> 原下标
    rev_dict = {w[::-1]: i for i, w in enumerate(words)}
    res = []

    # 2. 辅助函数：判断一个字符串是否为回文
    def is_pal(s):
        return s == s[::-1]

    for i, word in enumerate(words):
        n = len(word)
        # 3. 遍历所有切分点（包括空串在两端）
        for cut in range(n + 1):
            left, right = word[:cut], word[cut:]

            # 3.1 left 是回文 → 需要找 reverse(right) 拼在左边
            if is_pal(left):
                rev_right = right[::-1]
                j = rev_dict.get(rev_right)
                # j 必须存在且不是当前单词本身
                if j is not None and j != i:
                    res.append([j, i])   # rev_right + word

            # 3.2 right 是回文 → 需要找 reverse(left) 拼在右边
            # 注意：当 cut == n 时，right 为 ''，此时已经在 3.1 中处理过，避免重复
            if cut != n and is_pal(right):
                rev_left = left[::-1]
                j = rev_dict.get(rev_left)
                if j is not None and j != i:
                    res.append([i, j])   # word + rev_left

    return res
```

> **代码要点解释**  
> - `rev_dict = {w[::-1]: i for i, w in enumerate(words)}`：把每个单词的逆序放进哈希表，像把所有单词的“倒背词典”准备好，一次建表即可。  
> - `for cut in range(n + 1)`：切分点从 `0`（全部在右边）到 `n`（全部在左边），包括空串的情况。  
> - `if is_pal(left): …`：左半段已经是回文，只要右半段的逆序在数组里，就能在左边补上形成整体回文。  
> - `if cut != n and is_pal(right): …`：右半段是回文时，需要在右边补左半段的逆序。`cut != n` 用来避免在 `right=''` 时重复计数（因为空串已经在左半段回文的分支里处理过）。  

#### 复杂度

- **时间复杂度**：`O(L)`（`L = Σ|words[i]|`）  
  - 解释：我们只遍历每个字符常数次（切分、取逆序、回文判断），所以总耗时与所有字符的总数成正比。相比暴力的 `O(n²·k)`，这就像把原来要跑 **上千亿** 步的马拉松，压缩成只跑 **几万** 步的短跑。

- **空间复杂度**：`O(L)`  
  - 需要存储哈希表里每个逆序字符串，总长度同样是所有字符的和。再加上结果列表，额外的临时空间是常数级别的。

---

## 心得

- **核心技巧**：**利用逆序哈希表 + 字符串切分 + 回文子串判定**，把“找配对”从两两比较转化为“在字典里查找”。  
- **适用场景**：  
  1. **Palindrome Pairs**（本题）  
  2. **Valid Palindrome III**（判断最多删除 k 个字符后是否能成为回文）——需要快速判断子串是否回文。  
  3. **Shortest Palindrome**（在字符串前面添加最少字符使其回文）——同样利用前后缀的回文性质与哈希或 KMP。  
- **一句话总结**：**“把每个单词的逆序记下来，只检查自己的左/右半段是否已经是回文，就能在 O(total length) 内找出所有配对。”**

---

## 反思

- **第一反应**：直接双层循环枚举所有下标组合，写出最朴素的检查回文代码。  
- **最容易踩的坑**：  
  - **空串的处理**：空串本身是回文，需要单独考虑它与其他回文单词的配对。  
  - **重复计数**：切分点 `cut = n` 时 `right=''`，若不排除会把同一配对加入两次。  
  - **同一个单词不能配自己**：在查哈希表时必须排除 `j == i` 的情况。  
- **下次类似题的第一步**：**先把可以 O(1) 查找的“逆向信息”放进哈希表或 Trie”，再只对每个元素本身进行线性遍历/切分，避免全局的平方级比较。**