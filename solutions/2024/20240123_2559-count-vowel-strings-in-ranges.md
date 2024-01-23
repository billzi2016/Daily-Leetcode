# #2559. 区间内元音字符串计数 / Count Vowel Strings in Ranges

> 难度：中等 · 标签：Array、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-vowel-strings-in-ranges/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of strings words and a 2D array of integers queries.
Each query queries[i] = [li, ri] asks us to find the number of strings present at the indices ranging from li to ri (both inclusive) of words that start and end with a vowel.
Return an array ans of size queries.length, where ans[i] is the answer to the ith query.
Note that the vowel letters are 'a', 'e', 'i', 'o', and 'u'.

**Examples**

**Example 1:**

```
Input: words = ["aba","bcb","ece","aa","e"], queries = [[0,2],[1,4],[1,1]]
Output: [2,3,0]
Explanation: The strings starting and ending with a vowel are "aba", "ece", "aa" and "e".
The answer to the query [0,2] is 2 (strings "aba" and "ece").
to query [1,4] is 3 (strings "ece", "aa", "e").
to query [1,1] is 0.
We return [2,3,0].
```

**Example 2:**

```
Input: words = ["a","e","i"], queries = [[0,2],[0,1],[2,2]]
Output: [3,2,1]
Explanation: Every string satisfies the conditions, so we return [3,2,1].
```

**Constraints**

- 1 <= words.length <= 105
- 1 <= words[i].length <= 40
- words[i] consists only of lowercase English letters.
- sum(words[i].length) <= 3 * 105
- 1 <= queries.length <= 105
- 0 <= li <= ri < words.length

---

## 题目（中文翻译）

给定一个 **下标从 0 开始的数组（0-indexed array）** `words`（字符串数组）和一个 **二维整数数组（2D array of integers）** `queries`。

每个查询 `queries[i] = [li, ri]` 要求我们统计在 `words` 中下标范围为 `li` 到 `ri`（两端均包含）的字符串中，**首字符和尾字符都是元音（vowel）** 的数量。

返回一个数组 `ans`，其长度等于 `queries.length`，其中 `ans[i]` 为第 `i` 条查询的答案。

> 注意，元音字符包括 `'a'`, `'e'`, `'i'`, `'o'`, `'u'`。

---

## 示例

### 示例 1

**输入**  
```text
words = ["aba","bcb","ece","aa","e"], queries = [[0,2],[1,4],[1,1]]
```

**输出**  
```text
[2,3,0]
```

**解释**  
首尾都是元音的字符串有 `"aba"`, `"ece"`, `"aa"` 和 `"e"`。  
- 查询 `[0,2]` 的答案是 `2`（字符串 `"aba"` 和 `"ece"`）。  
- 查询 `[1,4]` 的答案是 `3`（字符串 `"ece"`、`"aa"`、`"e"`）。  
- 查询 `[1,1]` 的答案是 `0`。  

返回 `[2,3,0]`。

### 示例 2

**输入**  
```text
words = ["a","e","i"], queries = [[0,2],[0,1],[2,2]]
```

**输出**  
```text
[3,2,1]
```

**解释**  
所有字符串均满足首尾为元音的条件，因此返回 `[3,2,1]`。

---

## 约束条件

- `1 <= words.length <= 10^5`
- `1 <= words[i].length <= 40`
- `words[i]` 只包含小写英文字母。
- `sum(words[i].length) <= 3 * 10^5`
- `1 <= queries.length <= 10^5`
- `0 <= li <= ri < words.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个查询**都把对应区间 `[l, r]` 里的字符串逐个检查：  

1. 判断字符串的第一个字符和最后一个字符是否都是元音 (`a, e, i, o, u`)。  
2. 如果是，就把计数器 `cnt` 加一。  
3. 最后把 `cnt` 作为该查询的答案。

> **类比**：把 `words` 看成一本书的章节，查询 `[l, r]` 就是让你去翻 **第 l 到第 r 章节**，每翻一章就检查开头和结尾的首字母是否是“元音”。这就像在字典里查单词，`set`（集合）相当于字典的“索引页”，可以在 O(1) 时间判断一个字符是否在元音表里。

只要我们能正确判断“首字符是元音且尾字符是元音”，答案就一定是对的，因为我们没有遗漏也没有多计。

#### 代码（Python）

```python
from typing import List

def count_vowel_strings_bruteforce(words: List[str], queries: List[List[int]]) -> List[int]:
    # 把元音放进集合，后面判断时可以 O(1) 查找
    vowels = {'a', 'e', 'i', 'o', 'u'}

    ans = []                         # 用来保存每个查询的答案
    for l, r in queries:             # 逐个处理查询
        cnt = 0                       # 当前区间符合条件的字符串数量
        for i in range(l, r + 1):    # 扫描区间内的每个下标
            w = words[i]
            # 判断首字符和尾字符是否都在 vowels 集合里
            if w[0] in vowels and w[-1] in vowels:
                cnt += 1
        ans.append(cnt)               # 把本次查询的结果加入答案列表
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(Q * N)`（最坏情况是每个查询都遍历整个 `words`，`Q` 是查询数量，`N` 是数组长度）。  
  大白话：如果 `words` 有 10 万条，查询也有 10 万个，程序大概要跑 **10 万 × 10 万 = 1 亿元**次检查，明显会超时。  
- **空间复杂度**：`O(1)`（只用了常数级的额外空间，除了输入本身和返回的答案）。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**瓶颈**在于每个查询都要遍历区间。  
如果我们能够在 **预处理** 阶段把“前缀累计符合条件的字符串数量”记下来，那么查询时只需要**常数时间**就能得到答案。

> **前缀和**的概念：想象你在走楼梯，每走一步就记录一下已经走了多少步。到了第 `i` 步，你只需要把第 `i` 步的累计值减去第 `l-1` 步的累计值，就能得到 `[l, i]` 之间走了多少步。这里的“走了多少步”对应“区间里有多少符合条件的字符串”。  

实现步骤如下：

1. **预处理**  
   - 逐个检查 `words[i]` 的首尾是否都是元音。  
   - 用一个长度为 `n+1` 的数组 `pref` 保存前缀和，`pref[0] = 0`，`pref[i+1] = pref[i] + (1 if words[i] 符合 else 0)`。  
   - 这样 `pref[k]` 表示前 `k` 个字符串（下标 `0 .. k-1`）中符合条件的数量。

2. **回答查询**  
   - 对于查询 `[l, r]`，答案 = `pref[r+1] - pref[l]`。  
   - 只做两次减法，时间是 O(1)。

> **类比**：把 `pref` 想成一本记了“到第几章为止，有多少符合条件的章节”的笔记本。要知道第 `l` 到第 `r` 章节有多少符合，只要看第 `r` 章节的累计数减去第 `l-1` 章节的累计数即可。

#### 代码（Python）

```python
from typing import List

def count_vowel_strings_opt(words: List[str], queries: List[List[int]]) -> List[int]:
    vowels = {'a', 'e', 'i', 'o', 'u'}

    n = len(words)
    # pref[i] 表示 words[0..i-1] 中符合条件的数量，长度为 n+1，pref[0] = 0
    pref = [0] * (n + 1)

    # 预处理前缀和
    for i, w in enumerate(words):
        # 判断当前字符串是否满足“首尾都是元音”
        good = 1 if (w[0] in vowels and w[-1] in vowels) else 0
        pref[i + 1] = pref[i] + good   # 累计到 i 为止的总数

    # 逐个查询，利用前缀和 O(1) 求答案
    ans = []
    for l, r in queries:
        # 区间 [l, r] 的数量 = 前缀和到 r+1 减去前缀和到 l
        ans.append(pref[r + 1] - pref[l])
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N + Q)`。  
  - 预处理遍历一次 `words`：`O(N)`。  
  - 每个查询只做两次减法：`O(1)`，共 `Q` 次，所以 `O(Q)`。  
  与暴力解的 `O(N·Q)` 相比，提升了 **指数级**（从“每次都遍历”到“一次遍历后全都搞定”）。  

- **空间复杂度**：`O(N)`。  
  - 额外使用了一个长度为 `N+1` 的前缀和数组 `pref`。  
  - 这相当于存了一个和原数组等长的整数列表，属于线性空间。  

---

## 心得  

- **核心技巧**：**前缀和（Prefix Sum）**。它把“区间统计”转化为“前缀差”，让区间查询从线性下降到常数时间。  
- **适用的题型**（列举 2~3）  
  1. 区间求和、区间出现次数（如 “Range Sum Query”）。  
  2. 区间内满足某种属性的元素计数（如 “Number of Even Numbers in Range”。）  
  3. 需要快速判断子数组/子串是否满足累计条件的题目（如 “Number of Subarrays with Sum ≥ K”。）  
- **一句话总结解题钥匙**：  
  > 把“每次都遍历”换成“先一次性累加”，查询时只做 “前缀差”。  

---

## 反思  

- **拿到题目第一反应**：直接对每个查询遍历区间，写出最直观的实现。  
- **最容易踩的坑**  
  1. **下标越界**：前缀和数组多开了一位，查询时要使用 `pref[r+1]` 而不是 `pref[r]`。  
  2. **元音判断**：忘记把 `set` 放在函数外部，导致每次检查都重新创建集合，增加不必要的时间。  
  3. **空字符串**：虽然题目保证 `words[i].length ≥ 1`，但如果忘记这一点，直接访问 `w[0]`、`w[-1]` 可能会报错。  
- **下次遇到同类题，第一步该想到**：  
  > “这道题是区间统计吗？如果是，先算前缀和/前缀计数，再用差值回答每个查询。”