# #1178. 每个谜题的有效单词数 / Number of Valid Words for Each Puzzle

> 难度：困难 · 标签：Array、Hash Table、String、Bit Manipulation、Trie · [LeetCode 链接](https://leetcode.com/problems/number-of-valid-words-for-each-puzzle/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: words = ["aaaa","asas","able","ability","actt","actor","access"], puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"]
Output: [1,1,3,2,4,0]
Explanation: 
1 valid word for "aboveyz" : "aaaa" 
1 valid word for "abrodyz" : "aaaa"
3 valid words for "abslute" : "aaaa", "asas", "able"
2 valid words for "absoryz" : "aaaa", "asas"
4 valid words for "actresz" : "aaaa", "asas", "actt", "access"
There are no valid words for "gaswxyz" cause none of the words in the list contains letter 'g'.
```

**Example 2:**

```
Input: words = ["apple","pleas","please"], puzzles = ["aelwxyz","aelpxyz","aelpsxy","saelpxy","xaelpsy"]
Output: [0,1,3,2,0]
```

**Constraints**

- 1 <= words.length <= 105
- 4 <= words[i].length <= 50
- 1 <= puzzles.length <= 104
- puzzles[i].length == 7
- words[i] and puzzles[i] consist of lowercase English letters.
- Each puzzles[i] does not contain repeated characters.

---

## 题目（中文翻译）

**描述**  
给定一个字符串数组 `words` 和另一个字符串数组 `puzzles`，请返回一个整数数组 `answer`，其中 `answer[i]` 表示对应 `puzzles[i]`（第 *i* 个谜题）能够匹配的 **有效单词**（valid word）数量。

- **有效单词** 的定义如下：
  1. 单词中必须包含该谜题的第一个字母（即 `puzzles[i][0]`）。
  2. 单词的所有字母必须全部出现在该谜题的七个字母中，即单词的字符集合是谜题字符集合的子集（subset）。

**示例 1**  
```text
Input: words = ["aaaa","asas","able","ability","actt","actor","access"],
       puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"]
Output: [1,1,3,2,4,0]
Explanation: 
1 valid word for "aboveyz" : "aaaa" 
1 valid word for "abrodyz" : "aaaa"
3 valid words for "abslute" : "aaaa", "asas", "able"
2 valid words for "absoryz" : "aaaa", "asas"
4 valid words for "actresz" : "aaaa", "asas", "actt", "actor"
0 valid words for "gaswxyz" : (none)
```

**示例 2**  
```text
Input: words = ["apple","pleas","please"],
       puzzles = ["aelwxyz","aelpxyz","aelpsxy","saelpxy","xaelpsy"]
Output: [0,1,3,2,0]
```

**约束条件**  
- `1 <= words.length <= 10^5`
- `4 <= words[i].length <= 50`
- `1 <= puzzles.length <= 10^4`
- `puzzles[i].length == 7`
- `words[i]` 和 `puzzles[i]` 仅由小写英文字母组成。
- 每个 `puzzles[i]` 中的字符互不重复。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个 `puzzle`（7 个字母）和每个 `word`（长度 4~50）逐一比对，判断该单词是否满足两个条件：

1. **必须包含拼图的第一个字母**（puzzle[0]）。
2. **只能使用拼图里出现的字母**，也就是说 `word` 中的每个字符都必须在 `puzzle` 中出现。

可以把 `puzzle` 看成一本“字母字典”，`puzzle[0]` 是这本字典的“必带关键词”。我们把每个 `word` 逐字符检查，像在字典里逐页翻找，找到所有符合条件的单词计数。

> **类比**：  
> 哈希表就像查字典，`key` 是单词的字母集合，`value` 是出现次数。这里我们不需要哈希表，只是逐个遍历。

**为什么正确**：只要遍历了所有单词并对每个拼图都做了上述两条检查，所有符合要求的单词都会被计入答案，且不会漏掉任何合法单词。

**复杂度分析（大白话）**  

- 对每个拼图，我们要检查所有单词。设 `W = len(words)`，`P = len(puzzles)`。  
- 检查一个单词需要遍历它的字符，最坏长度是 50。  
- 所以总的工作量是 `P * W * 50`，这在最坏情况下约等于 `10⁴ * 10⁵ * 50 = 5×10¹⁰` 次操作，显然会超时。  

时间复杂度记作 **O(P·W·L)**（`L` 为单词最大长度），空间几乎为 **O(1)**（只用了常数级的临时变量）。

#### 代码（Python）

```python
from typing import List

def find_num_of_valid_words_bruteforce(words: List[str], puzzles: List[str]) -> List[int]:
    res = []
    for puzzle in puzzles:
        first = puzzle[0]                     # 必须出现的字母
        cnt = 0
        for w in words:
            # 条件 1：必须包含第一个字母
            if first not in w:
                continue
            # 条件 2：单词里的每个字母都必须在拼图里出现
            ok = True
            for ch in w:
                if ch not in puzzle:          # 只要出现一个不在的字母，就不合法
                    ok = False
                    break
            if ok:
                cnt += 1
        res.append(cnt)
    return res
```

#### 复杂度

- **时间复杂度**：`O(P·W·L)`  
  - `P` 为拼图数量，`W` 为单词数量，`L` 为单词最长长度（≤50）。  
  - 大意就是“每个拼图要遍历所有单词的每个字符”，在数据规模大时会非常慢。

- **空间复杂度**：`O(1)`  
  - 只用了几个临时变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“每个拼图都要遍历全部单词”**。  
观察题目可以发现：

1. **拼图长度固定为 7**，所以每个拼图最多只有 `2⁷ = 128` 种不同的子集（子集指从这 7 个字母中挑出任意若干个字母形成的集合）。
2. 单词只关心 **出现了哪些不同的字母**，顺序和重复次数都不重要。我们可以把每个单词的字母集合压缩成一个 **26 位的二进制掩码**（bit‑mask），比如 `"abc"` → `0b000...0111`。
3. 对于一个拼图 `p`，合法单词的掩码必须满足：
   - 包含拼图的第一个字母（即掩码的对应位为 1）。
   - 只使用拼图里的字母，即 `word_mask` 必须是 `puzzle_mask` 的 **子掩码**（`word_mask & ~puzzle_mask == 0`）。

于是我们可以：

- **预处理**：遍历所有 `words`，把每个单词转换成掩码并记录出现次数（因为不同单词可能得到相同掩码）。这一步只做一次，复杂度 `O(W·L)`。
- 对每个 `puzzle`：
  1. 计算它的完整掩码 `puzzle_mask`（7 位中可能散布在 26 位中）。
  2. 枚举 **所有子掩码**，但只保留那些**包含首字母**的子掩码。子掩码的枚举可以通过 “子集枚举”技巧在 `O(2⁷)`（即 128）时间内完成。
  3. 对每个子掩码 `sub`，如果在预处理的哈希表里出现过，就把对应的计数加到答案中。

> **类比**：  
> - **位掩码**就像一张 26 格的“字母表格”，格子里写 0/1 表示该字母是否出现。  
> - **子掩码枚举**相当于从这张表格里挑出若干格子组成子集合，就像从 7 张卡片里抽任意张。

**子掩码枚举的技巧**（代码中会展示）：

```python
sub = puzzle_mask
while sub:
    # 处理 sub
    sub = (sub - 1) & puzzle_mask   # 产生下一个子掩码
```

这个循环会遍历除 `0` 之外的所有子集，最多 2⁷‑1 次。

#### 代码（Python）

```python
from typing import List
from collections import Counter

def find_num_of_valid_words(words: List[str], puzzles: List[str]) -> List[int]:
    """
    最优解：利用位掩码 + 子集枚举
    """
    # ---------- 1. 预处理所有单词 ----------
    # 把每个单词压缩成 26 位掩码，只保留出现过的字母
    def word_to_mask(w: str) -> int:
        mask = 0
        for ch in set(w):               # set 去重，减少不必要的位操作
            mask |= 1 << (ord(ch) - ord('a'))
        return mask

    word_cnt = Counter()
    for w in words:
        mask = word_to_mask(w)
        # 只保留字母数 ≤ 7 的单词（因为拼图只有 7 个字母，不可能匹配更长的集合）
        if bin(mask).count('1') <= 7:
            word_cnt[mask] += 1

    # ---------- 2. 逐个处理拼图 ----------
    ans = []
    for puzzle in puzzles:
        # 把拼图转成掩码
        puzzle_mask = 0
        for ch in puzzle:
            puzzle_mask |= 1 << (ord(ch) - ord('a'))

        first_bit = 1 << (ord(puzzle[0]) - ord('a'))   # 必须出现的首字母对应的位

        total = 0
        # 子掩码枚举：从 puzzle_mask 开始，不断产生子集
        sub = puzzle_mask
        while sub:
            # 只统计包含首字母的子集
            if sub & first_bit:
                total += word_cnt.get(sub, 0)   # 若该子掩码出现过，则加上出现次数
            # 产生下一个子掩码
            sub = (sub - 1) & puzzle_mask

        ans.append(total)
    return ans
```

> **关键注释解释**  
> - `word_to_mask`：把单词的不同字母映射到 26 位的二进制数，`1` 表示出现，`0` 表示未出现。  
> - `Counter`：相当于“字典”，记录每种掩码出现了多少次。  
> - `bin(mask).count('1') <= 7`：如果一个单词涉及的不同字母超过 7 个，根本不可能匹配任何拼图，直接丢弃，进一步减小哈希表大小。  
> - `sub = (sub - 1) & puzzle_mask`：这是 **子集枚举**的核心，一行代码即可遍历所有子掩码。  

#### 复杂度

- **时间复杂度**：`O(W·L + P·2⁷)`  
  - 预处理所有单词：`W` 为单词数，`L` 为单词最长长度（≤50），即 `O(W·L)`。  
  - 对每个拼图枚举子集：`2⁷ = 128`，所以每个拼图最多只做 128 次哈希查询，整体是 `O(P·128)`，即 `O(P)`（因为 128 是常数）。  
  - 与暴力解相比，时间从 `O(P·W·L)` 降到了 **线性**（`W` 与 `P` 不再相乘），即使在最大约束下也能轻松通过。

- **空间复杂度**：`O(U)`，其中 `U` 为不同单词掩码的数量。最多不超过 `min(W, 2²⁶)`，但实际由于只保留字母数 ≤7 的单词，`U` 通常远小于 `W`（在本题约为几万），属于线性空间。

---

## 心得

- **核心技巧**：**位掩码 + 子集枚举**。把字符集合映射到整数，用位运算做集合包含/子集判断，利用拼图长度固定的特性把搜索空间压到常数级（128）。
- **适用场景**  
  1. **子集匹配** 类似题目，如 *“Number of Valid Words for Each Puzzle”*、*“Maximum XOR With an Element From Array”*（需要子集遍历）。  
  2. **字母集合计数** 如 *“Maximum Length of a Concatenated String with Unique Characters”*（使用位掩码做去重）。  
  3. **固定小规模集合的子集遍历** 如 *“Count Numbers with Unique Digits”*（枚举 10 位数字子集）。
- **一句话总结**：**把字符集合压成整数，枚举所有子集合，用哈希表计数，时间从指数降到常数**。

---

## 反思

- **第一反应**：看到 “每个 puzzle 长度 7，单词很多”，立刻想到“用位掩码把字母集合压缩”。如果没有想到位运算，可能会尝试 Trie、DFS 等更复杂的结构，导致时间爆炸。
- **最容易踩的坑**  
  1. **重复字母**：单词里出现多次同一个字母不应重复计数，使用 `set(w)` 去重。  
  2. **首字母必须出现**：在子集枚举时忘记过滤不含首字母的子集，会把非法单词算进去。  
  3. **子集枚举的起始值**：必须从 `puzzle_mask` 开始而不是 `0`，否则会遗漏包含所有字母的情况。  
  4. **掩码位数**：使用 `1 << (ord(ch)-ord('a'))` 时要确保 `ch` 是小写英文字母，否则会越界。
- **下次类似题**：第一步先 **判断是否可以用位掩码**（集合大小 ≤ 20‑30），然后 **检查是否有固定小规模的子集搜索空间**（如 7、10），再决定是否使用 **子集枚举 + 哈希计数** 的方案。这样可以快速锁定最优思路。