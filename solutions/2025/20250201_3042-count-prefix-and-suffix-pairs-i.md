# #3042. 计数前缀与后缀配对 I / Count Prefix and Suffix Pairs I

> 难度：简单 · 标签：Array、String、Trie、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/count-prefix-and-suffix-pairs-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string array words.
Let's define a boolean function isPrefixAndSuffix that takes two strings, str1 and str2:
For example, isPrefixAndSuffix("aba", "ababa") is true because "aba" is a prefix of "ababa" and also a suffix, but isPrefixAndSuffix("abc", "abcd") is false.
Return an integer denoting the number of index pairs (i, j) such that i < j, and isPrefixAndSuffix(words[i], words[j]) is true.

**Examples**

**Example 1:**

```
Input: words = ["a","aba","ababa","aa"]
Output: 4
Explanation: In this example, the counted index pairs are:
i = 0 and j = 1 because isPrefixAndSuffix("a", "aba") is true.
i = 0 and j = 2 because isPrefixAndSuffix("a", "ababa") is true.
i = 0 and j = 3 because isPrefixAndSuffix("a", "aa") is true.
i = 1 and j = 2 because isPrefixAndSuffix("aba", "ababa") is true.
Therefore, the answer is 4.
```

**Example 2:**

```
Input: words = ["pa","papa","ma","mama"]
Output: 2
Explanation: In this example, the counted index pairs are:
i = 0 and j = 1 because isPrefixAndSuffix("pa", "papa") is true.
i = 2 and j = 3 because isPrefixAndSuffix("ma", "mama") is true.
Therefore, the answer is 2.
```

**Example 3:**

```
Input: words = ["abab","ab"]
Output: 0
Explanation: In this example, the only valid index pair is i = 0 and j = 1, and isPrefixAndSuffix("abab", "ab") is false.
Therefore, the answer is 0.
```

**Constraints**

- 1 <= words.length <= 50
- 1 <= words[i].length <= 10
- words[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的字符串数组 `words`。  
定义一个布尔函数 `isPrefixAndSuffix(str1, str2)`，判断 `str1` 同时是 `str2` 的前缀（prefix）和后缀（suffix）。例如，`isPrefixAndSuffix("aba", "ababa")` 为 `true`，因为 `"aba"` 既是 `"ababa"` 的前缀也是后缀；而 `isPrefixAndSuffix("abc", "abcd")` 为 `false`。  

返回满足 `i < j` 且 `isPrefixAndSuffix(words[i], words[j])` 为 `true` 的下标对 `(i, j)` 的数量。

**示例**  

*示例 1*  
```text
Input: words = ["a","aba","ababa","aa"]
Output: 4
Explanation: 本例中计数的下标对为：
- i = 0, j = 1 → isPrefixAndSuffix("a", "aba") 为 true
- i = 0, j = 2 → isPrefixAndSuffix("a", "ababa") 为 true
- i = 0, j = 3 → isPrefixAndSuffix("a", "aa") 为 true
- i = 1, j = 2 → isPrefixAndSuffix("aba", "ababa") 为 true
因此答案为 4。
```

*示例 2*  
```text
Input: words = ["pa","papa","ma","mama"]
Output: 2
Explanation: 本例中计数的下标对为：
- i = 0, j = 1 → isPrefixAndSuffix("pa", "papa") 为 true
- i = 2, j = 3 → isPrefixAndSuffix("ma", "mama") 为 true
因此答案为 2。
```

*示例 3*  
```text
Input: words = ["abab","ab"]
Output: 0
Explanation: 本例中唯一可能的下标对是 i = 0, j = 1，但 isPrefixAndSuffix("abab", "ab") 为 false。
因此答案为 0。
```

**约束条件**  
- `1 <= words.length <= 50`  
- `1 <= words[i].length <= 10`  
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有满足 **i < j** 的下标对枚举一遍，然后逐个检查 `words[i]` 是否既是 `words[j]` 的前缀又是后缀。  

- **枚举下标对**：两层循环，外层遍历 `i`，内层遍历 `j`（`j > i`）。  
- **检查前缀**：用 Python 的 `str.startswith`，把 `words[i]` 当作前缀去匹配 `words[j]`。  
- **检查后缀**：用 `str.endswith`，把 `words[i]` 当作后缀去匹配 `words[j]`。  
- **计数**：只要两者都满足，就把答案加一。  

> **类比**：把 `words` 看成一本书的章节目录，想知道「第 i 章节的标题」是否既出现在「第 j 章节标题的开头」又出现在「结尾」。我们把每一对章节标题都拿出来比对一次，最笨但最靠谱。

**为什么一定对？**  
因为我们把 **所有可能的 (i, j) 组合** 都检查了一遍，漏掉的情况不可能出现。只要检查函数实现正确，答案必然正确。

#### 代码（Python）

```python
from typing import List

def count_prefix_suffix_pairs(words: List[str]) -> int:
    n = len(words)
    ans = 0                     # 记录满足条件的下标对数量
    for i in range(n):          # 第一个下标 i
        for j in range(i + 1, n):   # 第二个下标 j，必须大于 i
            # 判断 words[i] 是否是 words[j] 的前缀且后缀
            if words[j].startswith(words[i]) and words[j].endswith(words[i]):
                ans += 1        # 条件满足，计数器加一
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n² * L)`  
  - `n` 为数组长度（最多 50），`L` 为单词最长长度（最多 10）。  
  - 两层循环产生约 `n·(n-1)/2` ≈ `n²/2` 对下标，每对检查前缀/后缀各需要 `O(L)` 的字符比较。  
  - 大白话：如果有 50 条记录，需要比较大约 1 200 对，每次比较最多 10 个字符，算下来仍然很快。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **两层循环**，即使 `L` 很小，`n²` 仍然是二次增长。  
观察题目可以发现：

> 若 `words[i]` 同时是 `words[j]` 的前缀和后缀，则 `words[i]` 必定是 `words[j]` **两端相同的子串**。  

换句话说，**每个单词 `w` 只需要关心它自身的“前后同形子串”。**  

我们可以把所有已经出现过的单词存进哈希表（Python 的 `dict`），键是单词本身，值是出现次数。遍历数组时，对于当前单词 `cur`，枚举它所有 **既是前缀又是后缀** 的子串 `s`（包括 `cur` 本身），只要 `s` 已经在哈希表中出现过，就说明之前的某些下标 `i` 对应的单词正好是 `s`，满足 `isPrefixAndSuffix(s, cur) = true`。把这些出现次数累加到答案中，即可在 **一次遍历** 内完成统计。

**关键点**：  
1. **找出一个单词的所有“前后同形子串”。**  
   - 对于长度为 `m` 的单词 `cur`，只要 `cur[:k] == cur[m-k:]`（即前 `k` 个字符等于后 `k` 个字符），则长度 `k` 的子串既是前缀也是后缀。  
   - `k` 的取值范围是 `1 … m`，所以最多检查 `m` 次（`m ≤ 10`），时间可以忽略不计。  

2. **使用哈希表统计已出现的单词。**  
   - 哈希表的查找/插入都是 `O(1)`，所以整体时间是 `O(n * L)`。  

> **类比**：把已经看到的单词装进一本“词典”。当我们看到新单词 `cur` 时，只要在它的“前后同形子串”里查一查词典里有没有相同的词，就能立刻知道有多少之前的单词可以和它配对，而不需要一一比较。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def count_prefix_suffix_pairs_opt(words: List[str]) -> int:
    """
    O(n * L) 解法
    - 遍历 words，维护出现过的单词计数 hash 表 cnt
    - 对当前单词 cur，枚举所有同时是前缀和后缀的子串 s
    - 累加 cnt[s]（即之前出现过多少次 s）
    - 最后把 cur 加入哈希表，供后面的单词使用
    """
    cnt = defaultdict(int)   # 哈希表：单词 -> 已出现次数
    ans = 0

    for cur in words:                 # 按顺序遍历，每个单词只处理一次
        m = len(cur)

        # 枚举所有长度 k，使得 cur[:k] == cur[m-k:]
        for k in range(1, m + 1):    # k = 1 … m
            prefix = cur[:k]
            suffix = cur[m - k:]
            if prefix == suffix:     # 同时是前缀又是后缀
                ans += cnt[prefix]   # 之前出现过多少个相同的单词

        cnt[cur] += 1                 # 把当前单词加入统计，供后面的单词匹配

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * L)`  
  - 对每个单词只遍历一次，内部最多检查 `L`（≤10）次前后同形子串的相等性。  
  - 与暴力解的 `O(n² * L)` 相比，去掉了二次循环，规模更大时会快很多。  

- **空间复杂度**：`O(n * L)`（实际为 `O(n)`）  
  - 哈希表最多保存 `n` 个不同的单词，每个单词长度至多 `L`，所以总体占用与输入规模相同。  
  - 大白话：我们只额外用了一个“小本子”记下已经见过的单词，大小跟原数组差不多。  

---

## 心得  

- **核心技巧**：**利用哈希表快速统计已出现的前缀/后缀**。  
- **适用的题型**  
  1. “统计子串是前缀且后缀的配对”——比如本题。  
  2. “单词是否是另一单词的子串”类统计（如前缀树/Trie、滚动哈希）。  
  3. “在字符串序列中找出相同前缀/后缀的对”——如 “Count Prefix and Suffix Pairs II”。  
- **一句话总结解题钥匙**：**把“检查每一对”转化为“对每个新元素只检查它自身的特征”，并用哈希表把过去的答案记下来**。

---

## 反思  

- **第一反应**：看到“前缀 & 后缀”，立刻想到暴力两层循环——最安全、最直观的实现。  
- **最容易踩的坑**  
  - **漏掉长度等于整个单词的情况**：`k = len(cur)` 时，前后子串都是完整单词，本身也算是前后同形子串。  
  - **计数顺序**：一定要在把当前单词加入哈希表之前统计，否则会错误地把 `(i,i)` 计入答案。  
  - **空字符串**（题目不出现）或单字符字符串的处理，需要确保循环能够覆盖 `k = 1`。  
- **下次遇到同类题**：第一步先思考“是否可以把两层遍历合并到一次遍历”，并寻找**可以提前预处理或增量维护的结构**（哈希表、Trie、前缀和等）。这样往往能把二次复杂度降到线性。