# #2506. 相似字符串对计数 / Count Pairs Of Similar Strings

> 难度：简单 · 标签：Array、Hash Table、String、Bit Manipulation、Counting · [LeetCode 链接](https://leetcode.com/problems/count-pairs-of-similar-strings/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string array words.
Two strings are similar if they consist of the same characters.
Return the number of pairs (i, j) such that 0 <= i < j <= word.length - 1 and the two strings words[i] and words[j] are similar.

**Examples**

**Example 1:**

```
Input: words = ["aba","aabb","abcd","bac","aabc"]
Output: 2
Explanation: There are 2 pairs that satisfy the conditions:
- i = 0 and j = 1 : both words[0] and words[1] only consist of characters 'a' and 'b'. 
- i = 3 and j = 4 : both words[3] and words[4] only consist of characters 'a', 'b', and 'c'.
```

**Example 2:**

```
Input: words = ["aabb","ab","ba"]
Output: 3
Explanation: There are 3 pairs that satisfy the conditions:
- i = 0 and j = 1 : both words[0] and words[1] only consist of characters 'a' and 'b'. 
- i = 0 and j = 2 : both words[0] and words[2] only consist of characters 'a' and 'b'.
- i = 1 and j = 2 : both words[1] and words[2] only consist of characters 'a' and 'b'.
```

**Example 3:**

```
Input: words = ["nba","cba","dba"]
Output: 0
Explanation: Since there does not exist any pair that satisfies the conditions, we return 0.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consist of only lowercase English letters.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的字符串数组 `words`。  
如果两个字符串由完全相同的字符组成，则称它们是**相似**（similar）。  
返回满足 `0 <= i < j <= words.length - 1` 且 `words[i]` 与 `words[j]` 相似的下标对 `(i, j)` 的数量。

## 示例

### 示例 1
**输入**  
`words = ["aba","aabb","abcd","bac","aabc"]`

**输出**  
`2`

**解释**  
满足条件的有 2 对：
- `i = 0` 且 `j = 1`：`words[0]` 和 `words[1]` 只由字符 `'a'` 和 `'b'` 组成。  
- `i = 3` 且 `j = 4`：`words[3]` 和 `words[4]` 只由字符 `'a'`、`'b'`、`'c'` 组成。

### 示例 2
**输入**  
`words = ["aabb","ab","ba"]`

**输出**  
`3`

**解释**  
满足条件的有 3 对：
- `i = 0` 且 `j = 1`：`words[0]` 和 `words[1]` 只由字符 `'a'` 和 `'b'` 组成。  
- `i = 0` 且 `j = 2`：`words[0]` 和 `words[2]` 只由字符 `'a'` 和 `'b'` 组成。  
- `i = 1` 且 `j = 2`：`words[1]` 和 `words[2]` 只由字符 `'a'` 和 `'b'` 组成。

### 示例 3
**输入**  
`words = ["nba","cba","dba"]`

**输出**  
`0`

**解释**  
不存在满足条件的下标对，返回 `0`。

## 约束条件
- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把 **每一对** `(i, j)`（`i < j`）都拿出来比较：  
1. 把 `words[i]` 和 `words[j]` 各自的字符收集进一个集合（`set`），集合就像一本**词典**，把出现过的字母记下来。  
2. 比较这两个集合是否**完全相同**——如果相同，说明这两个单词只由同样的字母组成，算作一对相似的字符串。  

为什么可行？  
- 集合天然去重，只保留出现过的字符。  
- 两个集合相等，等价于“它们的字符种类完全一致”。  

#### 代码（Python）  
```python
from typing import List

def similarPairs_brute(words: List[str]) -> int:
    n = len(words)
    ans = 0

    # 枚举所有 i < j 的组合
    for i in range(n):
        # 把第 i 个单词的字符放进集合，相当于查字典
        set_i = set(words[i])
        for j in range(i + 1, n):
            # 第 j 个单词的字符集合
            set_j = set(words[j])
            # 两个集合相等即为相似
            if set_i == set_j:
                ans += 1
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n² * L)`  
  - `n` 是单词数，`L` 是单词的最大长度。  
  - 需要遍历 `n·(n‑1)/2` 对，每对里要把两个单词的字符放进集合，最多遍历 `L` 次。  
  - 用大白话说，就是“如果有 100 个单词，每个单词 100 个字母，最坏要检查 100×99/2≈5k 对，每对要看 200 次字符”，所以会有几百万次操作。  

- **空间复杂度**：`O(L)`（每次循环里临时的集合最多装 26 个字母，常数级）  

---

### 2. 最优解  

#### 思路  
暴力解慢的地方在于**每次都要重新构造集合**，这相当于在重复做同一件事。  
我们可以把每个单词的字符集合**提前压缩成一个数字**，这样比较就变成比较数字是否相等，时间大幅下降。  

**核心技巧：位掩码（bit mask）**  
- 英文字母只有 26 个，正好对应一个 26 位的二进制数。  
- 设第 `k` 位（`0 ≤ k < 26`）表示字母 `'a'+k` 是否出现。  
- 遍历单词的每个字符 `c`，把对应位设为 1：`mask |= 1 << (ord(c) - ord('a'))`。  
- 最终得到的 `mask` 就唯一代表了该单词的字符集合。  

有了 `mask`，**相似的单词就拥有相同的 mask**。于是我们只需要统计每个 mask 出现了多少次，然后把同一组里两两配对的数量加起来即可。  
配对数量的公式是组合数学里的 “从 `cnt` 个中选 2 个”：`cnt * (cnt - 1) // 2`。

#### 代码（Python）  
```python
from typing import List
from collections import Counter

def similarPairs_opt(words: List[str]) -> int:
    """
    使用位掩码把每个单词的字符集合压缩成整数，
    再利用哈希表统计相同掩码的出现次数，最后求组合数。
    """
    mask_cnt = Counter()          # 哈希表：mask -> 出现次数

    for w in words:
        mask = 0
        for ch in w:
            # 把字符对应的位设为 1，例如 'c' 对应第 2 位
            mask |= 1 << (ord(ch) - ord('a'))
        mask_cnt[mask] += 1       # 同一 mask 的单词归为一类

    ans = 0
    for cnt in mask_cnt.values():
        # 从 cnt 个相同 mask 的单词中任选两两配对
        ans += cnt * (cnt - 1) // 2
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n * L)`  
  - 每个单词只遍历一次字符，计算 mask，随后只做 O(1) 的哈希操作。  
  - 用通俗的话说，如果有 100 个单词，每个 100 字母，总共只要检查 10,000 次字符，比暴力的几百万次要少很多。  

- **空间复杂度**：`O(n)`（哈希表最多保存 `n` 个不同的 mask，实际最多 2⁶⁶ ≈ 67M 种，但受限于 `n ≤ 100`，空间很小）  

---

## 心得  

- **核心技巧**：把字符集合映射为 26 位的二进制掩码（位运算），并利用哈希表计数。  
- **适用场景**：  
  1. 判断两个集合是否相等且集合元素种类有限（如字符、颜色、开关状态）。  
  2. 需要快速比较大量集合相等性的题目，例如 “求相同字母集合的单词对数”。  
  3. “子集/超集”计数类问题，位掩码可以直接做位与/或运算。  
- **一句话总结**：**把集合压成整数，用哈希表计数，配对公式直接算**。  

---

## 反思  

- **第一反应**：看到“相同字符集合”，马上想到用 `set` 来比较，随后想到可以用位运算压缩。  
- **最容易踩的坑**：  
  - 忽略了字符出现次数不影响相似性，只要出现与否即可。  
  - 位掩码必须用 `|=` 而不是 `+=`，否则会产生错误的数值。  
  - 统计配对时要用组合数公式 `cnt * (cnt-1) // 2`，直接把 `cnt` 加进去会少算。  
- **下次思路**：遇到“集合相等”且元素种类固定的题，第一步就想到 **位掩码 + 哈希计数**，再决定是否需要进一步的位运算（交集、并集等）。