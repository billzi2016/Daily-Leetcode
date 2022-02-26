# #1684. 统计一致字符串的数量 / Count the Number of Consistent Strings

> 难度：简单 · 标签：Array、Hash Table、String、Bit Manipulation、Counting · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-consistent-strings/)

---

## 题目（英文原版）

**Description**

You are given a string allowed consisting of distinct characters and an array of strings words. A string is consistent if all characters in the string appear in the string allowed.
Return the number of consistent strings in the array words.

**Examples**

**Example 1:**

```
Input: allowed = "ab", words = ["ad","bd","aaab","baa","badab"]
Output: 2
Explanation: Strings "aaab" and "baa" are consistent since they only contain characters 'a' and 'b'.
```

**Example 2:**

```
Input: allowed = "abc", words = ["a","b","c","ab","ac","bc","abc"]
Output: 7
Explanation: All strings are consistent.
```

**Example 3:**

```
Input: allowed = "cad", words = ["cc","acd","b","ba","bac","bad","ac","d"]
Output: 4
Explanation: Strings "cc", "acd", "ac", and "d" are consistent.
```

**Constraints**

- 1 <= words.length <= 104
- 1 <= allowed.length <= 26
- 1 <= words[i].length <= 10
- The characters in allowed are distinct.
- words[i] and allowed contain only lowercase English letters.

---

## 题目（中文翻译）

你得到一个仅包含互不相同字符的字符串 `allowed`，以及一个字符串数组 `words`。如果一个字符串中的所有字符都出现在 `allowed` 中，则称该字符串是一致字符串（consistent string）。  
返回数组 `words` 中一致字符串的数量。

**示例 1**  
**输入**: `allowed = "ab"`, `words = ["ad","bd","aaab","baa","badab"]`  
**输出**: `2`  
**解释**: 字符串 `"aaab"` 和 `"baa"` 是一致的，因为它们只包含字符 `'a'` 和 `'b'`。

**示例 2**  
**输入**: `allowed = "abc"`, `words = ["a","b","c","ab","ac","bc","abc"]`  
**输出**: `7`  
**解释**: 所有字符串都是一致的。

**示例 3**  
**输入**: `allowed = "cad"`, `words = ["cc","acd","b","ba","bac","bad","ac","d"]`  
**输出**: `4`  
**解释**: 字符串 `"cc"`、`"acd"`、`"ac"` 和 `"d"` 是一致的。

**约束条件**
- `1 <= words.length <= 10^4`
- `1 <= allowed.length <= 26`
- `1 <= words[i].length <= 10`
- `allowed` 中的字符互不相同。
- `words[i]` 和 `allowed` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**逐个检查** `words` 里的每个单词，看它的每个字符是否都出现在 `allowed` 里。  
- **数据结构**：我们可以把 `allowed` 放进一个 **集合（set）**，它就像一本“字典”，只要把想查的字母当成“单词”，集合会立刻告诉我们这本字典里有没有这页（`O(1)` 查找）。  
- **正确性**：如果一个单词的所有字符都能在集合里找到，说明它只用了允许的字符，满足题意；只要有一个字符不在集合里，这个单词就不算。  
- **时间/空间分析**：  
  - 对每个单词我们要遍历它的所有字符（最长 10），每次查集合是常数时间。  
  - 假设 `n = len(words)`，则总的遍历次数大约是 `n * avg_len`，最坏情况下是 `n * 10` → **O(n)**（因为常数 10 可以忽略）。  
  - 额外的空间只用了一个集合保存 `allowed`，大小至多 26 → **O(1)**（常数空间）。

> 大白话解释：  
> - **O(n)** 就是说运行时间会随单词数量线性增长，单词多了，时间就多，但每增加一个单词只多一点点检查。  
> - **O(1)** 表示占用的额外内存几乎不随输入变大，最多只装下 26 个字母。

#### 代码（Python）

```python
def countConsistentStrings(allowed: str, words: list[str]) -> int:
    # 把 allowed 的字符放进集合，查找像查字典一样快
    allowed_set = set(allowed)          # {'a', 'b', ...}
    consistent_cnt = 0                  # 统计符合条件的单词数

    for w in words:                     # 逐个单词检查
        # 用 all 判断 w 的每个字符是否都在 allowed_set 中
        if all(ch in allowed_set for ch in w):
            consistent_cnt += 1        # 只要全部都在，就计数

    return consistent_cnt
```

#### 复杂度

- **时间复杂度**：`O(n * m)`，其中 `n = len(words)`，`m` 是单词的最大长度（本题 ≤ 10），可以简化为 `O(n)`。  
  > 意味着如果单词数量翻倍，程序跑的时间大约也会翻倍。
- **空间复杂度**：`O(1)`（只用了一个最多 26 个字符的集合），不随 `words` 长度增长。

---

### 2. 最优解

#### 思路  

暴力解已经是线性时间，已经很快了。但我们还能把 **字符查找** 的常数因子降到更低，甚至做到 **位运算**（bit manipulation）一次性判断整个单词。思路如下：

1. **瓶颈**  
   - 在暴力解里，每检查一个字符都要在集合里做一次 `in` 操作，虽然是 `O(1)`，但仍有一定的函数调用开销。  
   - 当单词很多、字符检查频繁时，累计的开销会略大。

2. **优化**：把允许的字符压缩到 **一个 26 位的整数**（每个位对应一个英文字母），这样一次位运算就能判断一个字符是否被允许。进一步地，把单词的所有字符也压缩成一个整数，只要这两个整数的 **按位与** 等于单词整数本身，就说明单词全部由允许字符组成。

3. **核心技巧——位掩码（bit mask）**  
   - 把 `'a'` 到 `'z'` 映射到 0~25 位。  
   - `mask |= 1 << (ord(ch) - ord('a'))` 把对应位设为 1。  
   - 检查 `word_mask & ~allowed_mask == 0`（或者 `word_mask | allowed_mask == allowed_mask`），即 **没有出现不在 allowed 中的位**。

4. **类比**：想象有 26 把灯，每盏灯代表一个字母。`allowed_mask` 把允许的灯点亮，`word_mask` 把单词里出现的灯点亮。如果点亮的灯全都在已经点亮的允许灯之内，那么这个单词就是合法的。

5. **实现步骤**  
   - 先把 `allowed` 转成 `allowed_mask`。  
   - 对每个单词，构造 `word_mask` 并与 `allowed_mask` 做按位与判断。  
   - 计数即可。

#### 代码（Python）

```python
def countConsistentStrings(allowed: str, words: list[str]) -> int:
    # 1️⃣ 把 allowed 转成 26 位的整数掩码
    allowed_mask = 0
    for ch in allowed:
        # 把对应字母的位置设为 1，例如 'c' -> 第 2 位 (0-indexed)
        allowed_mask |= 1 << (ord(ch) - ord('a'))

    consistent_cnt = 0

    # 2️⃣ 遍历每个单词，构造它的位掩码并判断
    for w in words:
        word_mask = 0
        for ch in w:
            word_mask |= 1 << (ord(ch) - ord('a'))

        # 3️⃣ 检查：word_mask 中出现的位必须全部在 allowed_mask 中
        #   即 (word_mask & ~allowed_mask) 为 0
        if word_mask & ~allowed_mask == 0:
            consistent_cnt += 1

    return consistent_cnt
```

#### 复杂度

- **时间复杂度**：`O(n * m)` 与暴力解相同，只是常数更小（每个字符只做位运算，不再查集合）。  
  > 对于本题的规模，两者几乎一样快，但位运算在大数据时更有优势。
- **空间复杂度**：`O(1)`（仅用了几个整数变量），同样是常数空间。

---

## 心得

- **核心技巧**：利用集合快速判重或利用位掩码一次性判断字符集合的包含关系。  
- **适用题型**：  
  1. “只包含某些字符”的判定（如 **Number of Good Substrings**、**Maximum Length of a Concatenated String with Unique Characters**）。  
  2. “字符集合交并差”问题（如 **Unique Morse Code Words**、**Check If All A's Appear Before All B's**）。  
- **一句话总结解题钥匙**：把“字符出现”映射成**集合**或**位掩码**，一次性检查“是否全部在允许范围”。  

---

## 反思

- **第一反应**：直接遍历每个单词的每个字符，用 `set` 做查找——最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忘记 `allowed` 中的字符是**互不相同**的，直接用集合即可；  
  - 对空字符串或极短单词的判断要完整（本题 `words[i]` 长度 ≥ 1，仍需注意）。  
- **下次遇到同类题**：第一步先把“允许集合”用**集合或位掩码**保存，然后对每个待检查对象做**一次性包含性检查**，而不是逐个字符逐个比较。