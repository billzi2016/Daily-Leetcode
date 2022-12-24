# #2063. 所有子串的元音数之和 / Vowels of All Substrings

> 难度：中等 · 标签：Math、String、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/vowels-of-all-substrings/)

---

## 题目（英文原版）

**Description**

Given a string word, return the sum of the number of vowels ('a', 'e', 'i', 'o', and 'u') in every substring of word.
A substring is a contiguous (non-empty) sequence of characters within a string.
Note: Due to the large constraints, the answer may not fit in a signed 32-bit integer. Please be careful during the calculations.

**Examples**

**Example 1:**

```
Input: word = "aba"
Output: 6
Explanation: 
All possible substrings are: "a", "ab", "aba", "b", "ba", and "a".
- "b" has 0 vowels in it
- "a", "ab", "ba", and "a" have 1 vowel each
- "aba" has 2 vowels in it
Hence, the total sum of vowels = 0 + 1 + 1 + 1 + 1 + 2 = 6.
```

**Example 2:**

```
Input: word = "abc"
Output: 3
Explanation: 
All possible substrings are: "a", "ab", "abc", "b", "bc", and "c".
- "a", "ab", and "abc" have 1 vowel each
- "b", "bc", and "c" have 0 vowels each
Hence, the total sum of vowels = 1 + 1 + 1 + 0 + 0 + 0 = 3.
```

**Example 3:**

```
Input: word = "ltcd"
Output: 0
Explanation: There are no vowels in any substring of "ltcd".
```

**Constraints**

- 1 <= word.length <= 105
- word consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `word`，返回 `word` 的所有 **子串（substring）** 中元音字符（'a', 'e', 'i', 'o', 'u'）出现次数的总和。  
子串是字符串中连续（且非空）的字符序列。

> **注意**：由于约束较大，答案可能超出有符号 32 位整数的范围，请在计算时注意溢出问题。

### 示例

**示例 1**

```text
Input: word = "aba"
Output: 6
Explanation: 
所有可能的子串为: "a", "ab", "aba", "b", "ba", "a"。
- 子串 "b" 中元音数为 0
- 子串 "a", "ab", "ba", "a" 中各有 1 个元音
- 子串 "aba" 中有 2 个元音
因此元音总数 = 0 + 1 + 1 + 1 + 1 + 2 = 6。
```

**示例 2**

```text
Input: word = "abc"
Output: 3
Explanation: 
所有可能的子串为: "a", "ab", "abc", "b", "bc", "c"。
- 子串 "a", "ab", "abc" 中各有 1 个元音
- 子串 "b", "bc", "c" 中元音数为 0
因此元音总数 = 1 + 1 + 1 + 0 + 0 + 0 = 3。
```

**示例 3**

```text
Input: word = "ltcd"
Output: 0
Explanation: 所有子串中均不含元音，故总和为 0。
```

### 约束

- `1 <= word.length <= 10^5`
- `word` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有 **子串** 列举出来，然后在每个子串里统计元音字符的个数，最后把这些计数相加。

- **子串** 可以看成“一块连续的拼图”。我们可以用两个指针 `i`（子串的左端）和 `j`（子串的右端）遍历所有可能的拼图位置。  
- 判断一个字符是不是元音，就像在 **字典** 里查单词一样：把 `"a e i o u"` 放进集合里，用 `c in vowel_set` 判断。集合的查找在 Python 中是 O(1) 的，类似查字典时直接定位到页码。

这种做法一定能得到正确答案，因为我们没有漏掉任何子串，也没有遗漏任何元音的贡献。

#### 代码（Python）

```python
def vowelCountBrute(word: str) -> int:
    vowels = set('aeiou')          # 把所有元音放进集合，查找 O(1)
    n = len(word)
    total = 0                      # 最终答案

    # i 为子串左端，j 为子串右端（含）
    for i in range(n):
        cnt = 0                    # 记录当前子串里已经出现的元音个数
        for j in range(i, n):
            if word[j] in vowels: # 右端新加入的字符是否是元音
                cnt += 1
            total += cnt          # 把当前子串的元音数累加到答案
    return total
```

> **关键点**  
> - 内层循环每右移一步，只需要判断新增的字符 `word[j]` 是否是元音，之前的统计 `cnt` 可以直接复用，避免每次重新遍历子串。  
> - 这样时间已经从 O(n³) 降到 O(n²)，但仍然无法通过最大长度 10⁵ 的数据。

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - “n²” 表示当字符串长度是 `n` 时，最坏情况下要执行大约 `n × n / 2` 次循环。比如 `n = 10⁵`，则需要约 `10¹⁰` 次操作，显然会超时。  
- **空间复杂度：** `O(1)`  
  - 只用了常数级别的额外变量（集合、计数器），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的耗时在于遍历所有子串**。我们能否不枚举子串，而直接统计每个元音字符会被多少子串“看到”？

**核心观察**  
- 对于下标 `i`（从 0 开始）的字符，如果它是元音，那么它会出现在所有左端 `≤ i`、右端 `≥ i` 的子串里。  
- 左端可以取 `0 … i` 共 `i + 1` 种选择，右端可以取 `i … n‑1` 共 `n - i` 种选择。  
- 因此，这个元音会出现在 **`(i + 1) × (n - i)`** 个子串中，每出现一次就为答案贡献 `1`。

把所有元音的贡献相加，就得到了所有子串里元音的总数。

> **类比**：把每个元音想成一盏灯，它的光照范围是左边可以往左走的步数乘以右边可以往右走的步数。所有灯光的总亮度，就是答案。

**实现步骤**  

1. 预先把元音字符放进集合，方便 O(1) 判断。  
2. 遍历字符串的每个位置 `i`：  
   - 若 `word[i]` 是元音，则 `contrib = (i + 1) * (n - i)`。  
   - 把 `contrib` 加到答案中。  
3. 返回答案（题目提示答案可能超过 32 位整数，Python 的 `int` 自动大数支持，无需额外处理）。

整个过程只需要一次线性遍历。

#### 代码（Python）

```python
def vowelCountOptimal(word: str) -> int:
    vowels = set('aeiou')          # 元音集合，查找 O(1)
    n = len(word)
    ans = 0

    for i, ch in enumerate(word):
        if ch in vowels:           # 当前字符是元音吗？
            # (i+1) 表示左端可以选多少种，(n-i) 表示右端可以选多少种
            ans += (i + 1) * (n - i)
    return ans
```

> **关键行解释**  
> - `enumerate(word)` 同时得到字符下标 `i` 与字符本身 `ch`，方便计算。  
> - `(i + 1) * (n - i)` 直接给出该元音出现的子串数目。

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次字符串，`n` 次判断和加法。相当于“线性增长”，当 `n = 10⁵` 时只需要 `10⁵` 次操作，完全可以接受。  
- **空间复杂度：** `O(1)`  
  - 只用了常数级别的额外变量（集合、计数器），不随 `n` 增长。

---

## 心得

- **核心技巧**：**每个元素贡献计数**（Contribution Counting）。把全局求和转化为“每个元音在多少子串里出现”再求和。  
- **适用场景**：  
  1. **子数组/子串求和**，例如 “所有子数组的最小值之和”。  
  2. **计数某类元素在子结构中的出现次数**，如 “所有子数组中奇数的个数”。  
- **一句话总结**：**把“遍历子结构”换成“统计单点出现的子结构数”，往往能把 O(n²) 降到 O(n)。**

---

## 反思

- **第一反应**：直接枚举所有子串，写两层循环。  
- **最容易踩的坑**：  
  - 忽略了 **大数** 的问题（在 C++/Java 需要 `long long`/`long`），Python 自动处理。  
  - 对下标的计算容易出错，特别是左端和右端的选择数目要记得加 `1`（因为下标从 0 开始）。  
- **下次类似题目**：第一步先问自己 **“一个元素会被多少子结构覆盖？”**，如果能算出闭式公式，就尝试 **贡献计数** 的思路。