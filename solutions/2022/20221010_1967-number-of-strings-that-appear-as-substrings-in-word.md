# #1967. 出现在单词中的子串计数 / Number of Strings That Appear as Substrings in Word

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/)

---

## 题目（英文原版）

**Description**

Given an array of strings patterns and a string word, return the number of strings in patterns that exist as a substring in word.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: patterns = ["a","abc","bc","d"], word = "abc"
Output: 3
Explanation:
- "a" appears as a substring in "abc".
- "abc" appears as a substring in "abc".
- "bc" appears as a substring in "abc".
- "d" does not appear as a substring in "abc".
3 of the strings in patterns appear as a substring in word.
```

**Example 2:**

```
Input: patterns = ["a","b","c"], word = "aaaaabbbbb"
Output: 2
Explanation:
- "a" appears as a substring in "aaaaabbbbb".
- "b" appears as a substring in "aaaaabbbbb".
- "c" does not appear as a substring in "aaaaabbbbb".
2 of the strings in patterns appear as a substring in word.
```

**Example 3:**

```
Input: patterns = ["a","a","a"], word = "ab"
Output: 3
Explanation: Each of the patterns appears as a substring in word "ab".
```

**Constraints**

- 1 <= patterns.length <= 100
- 1 <= patterns[i].length <= 100
- 1 <= word.length <= 100
- patterns[i] and word consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组（array of strings）`patterns` 和一个字符串 `word`，返回 `patterns` 中有多少个字符串在 `word` 中出现过，出现的形式要求是子串（substring）。  
子串是指字符串中连续的字符序列。

## 示例

### 示例 1
**输入**: `patterns = ["a","abc","bc","d"]`, `word = "abc"`  
**输出**: `3`  
**解释**:
- `"a"` 出现在 `"abc"` 中，构成子串。
- `"abc"` 出现在 `"abc"` 中，构成子串。
- `"bc"` 出现在 `"abc"` 中，构成子串。
- `"d"` 未出现在 `"abc"` 中，无法构成子串。  
`patterns` 中有 3 个字符串是 `word` 的子串。

### 示例 2
**输入**: `patterns = ["a","b","c"]`, `word = "aaaaabbbbb"`  
**输出**: `2`  
**解释**:
- `"a"` 出现在 `"aaaaabbbbb"` 中，构成子串。
- `"b"` 出现在 `"aaaaabbbbb"` 中，构成子串。
- `"c"` 未出现在 `"aaaaabbbbb"` 中，无法构成子串。  
`patterns` 中有 2 个字符串是 `word` 的子串。

### 示例 3
**输入**: `patterns = ["a","a","a"]`, `word = "ab"`  
**输出**: `3`  
**解释**: `patterns` 中的每一个 `"a"` 都是 `word` `"ab"` 的子串。

## 约束条件
- `1 <= patterns.length <= 100`
- `1 <= patterns[i].length <= 100`
- `1 <= word.length <= 100`
- `patterns[i]` 和 `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `patterns` 里的每一个字符串都单独拿出来，问问它是不是 `word` 的子串**。  
在 Python 中，判断一个字符串 `p` 是否出现在另一个字符串 `s` 可以直接写成 `p in s`，这相当于在 `s` 里顺序滑动一个窗口，逐个比较，直到找到完全匹配的地方或滑到末尾。

- **使用的数据结构**：这里不需要额外的数据结构，只用到两个普通的字符串。  
  - 把 `in` 操作想象成 **在一本书里查字**：字典的 “词” 就是 `p`，书的内容就是 `word`，我们把词逐页（字符）翻阅，看看能否在某一页完整出现。

- **为什么正确**：如果 `p` 在 `word` 中出现过，那么 `p in word` 会返回 `True`；否则返回 `False`。对所有 `patterns` 逐一检查，计数即可得到答案。

- **时间/空间复杂度**  
  - 对每个 `pattern`（记为 `k`），`in` 操作最坏要遍历 `word` 的全部字符，且每次比较最多要看 `len(pattern)` 个字符。  
    所以单个检查的最坏时间是 `O(|word| * |pattern|)`。  
  - `patterns` 长度记为 `m`，则总体时间是 `O( Σ |word|·|pattern_i| )`，在本题约束（均 ≤ 100）下最多约 `100·100·100 = 10⁶` 步，完全可以接受。  
  - 只用了常数级额外空间，空间复杂度是 `O(1)`。

#### 代码（Python）

```python
def count_substrings_bruteforce(patterns, word):
    """
    暴力解：逐个检查 patterns 中的字符串是否是 word 的子串。
    """
    count = 0                         # 记录出现的次数
    for p in patterns:                # 遍历每一个模式串
        if p in word:                 # Python 的子串检查（相当于在 word 中“找词典”
            count += 1                # 找到了，就把计数加一
    return count
```

#### 复杂度

- **时间复杂度**：`O(m * n * l)`，其中  
  - `m = len(patterns)`（模式串个数），  
  - `n = len(word)`（主串长度），  
  - `l = average length of a pattern`（模式串平均长度）。  
  简单说，就是 **“每个模式串都要在整个单词里找一遍”**。

- **空间复杂度**：`O(1)`，只用了几个计数器和循环变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：我们对每个 `pattern` 都要在 `word` 里重新扫描一遍。  
如果把 `word` 的所有可能子串预先算出来，后面每次检查只需要 **一次哈希查找**，就可以把时间从 “每次遍历 `word`” 降到 “常数时间”。  

**关键步骤**：

1. **枚举 `word` 的所有子串**  
   - `word` 长度记为 `n`（≤ 100），所有子串的起始位置 `i` 在 `[0, n-1]`，结束位置 `j` 在 `[i+1, n]`。  
   - 把每个子串加入 `set_substrings`（集合）。  
   - 集合在 Python 中实现了 **哈希表**，查找 `x in set_substrings` 的时间是 `O(1)`（平均），就像在字典里查词，几乎不费时间。

2. **遍历 `patterns`，直接在集合里查**  
   - 对每个 `p`，如果 `p in set_substrings`，计数加一。

**为什么正确**：  
- 集合里保存了 **所有** 连续的字符序列（即所有子串），所以只要 `p` 是 `word` 的子串，它一定已经在集合中出现过。  
- 反之，如果 `p` 不在集合里，说明 `word` 中根本不存在这样连续的字符序列。

**类比**：  
想象把 `word` 当成一本书，把每一页的所有连续文字（子串）都写进一本**索引卡片盒**（集合）。以后要查某个词是否出现，只需要在卡片盒里抽一张卡片（哈希查找），不必再翻书。

#### 代码（Python）

```python
def count_substrings_optimal(patterns, word):
    """
    最优解：预先把 word 的所有子串放进集合，之后每个 pattern 只做 O(1) 的查找。
    """
    # 1️⃣ 构造所有子串的集合
    substr_set = set()
    n = len(word)
    for i in range(n):                # 子串的左边界
        # 为了避免每次都做 word[i:j] 的切片，可以在内部累加字符
        cur = ''
        for j in range(i, n):         # 子串的右边界（含 j）
            cur += word[j]            # 逐字符扩展子串
            substr_set.add(cur)       # 把当前子串加入集合

    # 2️⃣ 检查每个 pattern 是否在集合中
    count = 0
    for p in patterns:
        if p in substr_set:           # 哈希查找，平均 O(1)
            count += 1
    return count
```

> **小技巧**：因为 `word` 最多只有 100 个字符，子串的总数最多是 `n·(n+1)/2 ≈ 5,000`，放进集合不会占用太多内存（约几百 KB）。

#### 复杂度

- **时间复杂度**：  
  - 枚举子串的双层循环共计 `O(n²)`（`n ≤ 100`），每次 `add` 操作是 `O(1)`。  
  - 检查 `patterns` 为 `O(m)`，因为每次查找是常数时间。  
  - 综合为 `O(n² + m)`，在最坏情况下约 `10⁴` 步，比暴力的 `10⁶` 步快了好几百倍。  

- **空间复杂度**：`O(n²)`，存储所有子串的集合。  
  - 对于 `n = 100`，最多约 5,000 条子串，完全在题目限制范围内。

---

## 心得

- **核心技巧**：**预处理 + 哈希查找**（把所有可能的答案先算出来，后面查询时用 O(1) 的集合/字典）。  
- **适用的题型**  
  1. 判断多个查询字符串是否出现在同一个大字符串中（如 LeetCode 1037、2080）。  
  2. 统计一组单词在一段文本中的出现次数（类似 “单词计数” 题）。  
  3. 检查多个模式是否是同一字符串的子序列/子串（如 “子序列检查” 系列）。  

- **一句话总结**：**把大问题拆成“小问题”，先把“大”一次性算好，再用哈希表把“小”查询降到常数时间**。

---

## 反思

- **第一反应**：看到“子串”二字，马上想到 Python 的 `in` 或 `find`，于是写出了最直接的暴力遍历。  
- **最容易踩的坑**  
  - 忘记考虑 **重复的模式**（题目要求每个出现的模式都计数，即使相同也要算多次）。  
  - 对 **空字符串** 的处理：本题约束没有空串，但如果出现，需要记得空串是任何字符串的子串。  
  - 忽视 **时间限制**：虽然本题规模小，暴力也能 AC，但如果规模扩大（如 `word` 长度 10⁵），暴力就会超时。  

- **下次遇到同类题**，第一步应该想到 **“能否把原字符串的所有子结构一次性预处理出来？”**，如果可以，就立刻用集合/哈希表把后续查询的复杂度压到 O(1)。