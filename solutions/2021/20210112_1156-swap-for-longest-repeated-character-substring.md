# #1156. Swap For Longest Repeated Character Substring / Swap For Longest Repeated Character Substring

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/swap-for-longest-repeated-character-substring/)

---

## 题目（英文原版）

**Description**

You are given a string text. You can swap two of the characters in the text.
Return the length of the longest substring with repeated characters.

**Examples**

**Example 1:**

```
Input: text = "ababa"
Output: 3
Explanation: We can swap the first 'b' with the last 'a', or the last 'b' with the first 'a'. Then, the longest repeated character substring is "aaa" with length 3.
```

**Example 2:**

```
Input: text = "aaabaaa"
Output: 6
Explanation: Swap 'b' with the last 'a' (or the first 'a'), and we get longest repeated character substring "aaaaaa" with length 6.
```

**Example 3:**

```
Input: text = "aaaaa"
Output: 5
Explanation: No need to swap, longest repeated character substring is "aaaaa" with length is 5.
```

**Constraints**

- 1 <= text.length <= 2 * 104
- text consist of lowercase English characters only.

---

## 题目（中文翻译）

给定一个字符串 `text`，你可以交换其中任意两个字符。  
返回交换后可以得到的 **最长重复字符子串（repeated character substring）** 的长度。

**示例 1**  
**输入**: `text = "ababa"`  
**输出**: `3`  
**解释**: 我们可以把第一个 `'b'` 与最后一个 `'a'` 交换，或者把最后一个 `'b'` 与第一个 `'a'` 交换。此时最长的重复字符子串是 `"aaa"`，长度为 `3`。

**示例 2**  
**输入**: `text = "aaabaaa"`  
**输出**: `6`  
**解释**: 将 `'b'` 与最后一个 `'a'`（或第一个 `'a'`）交换后，得到的最长重复字符子串是 `"aaaaaa"`，长度为 `6`。

**示例 3**  
**输入**: `text = "aaaaa"`  
**输出**: `5`  
**解释**: 不需要交换，最长的重复字符子串就是 `"aaaaa"`，长度为 `5`。

**约束条件**  
- `1 <= text.length <= 2 * 10^4`  
- `text` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的交换都穷举一遍**，然后在每一次得到的新字符串里找出最长的连续相同字符子串。  
- **枚举交换**：字符串长度记为 `n`，我们可以把第 `i` 位和第 `j` 位的字符互换，`i`、`j` 的组合有 `n × n` 种（包括不交换的情况，即 `i == j`）。  
- **求最长重复子串**：遍历一次字符串，用一个计数器记录当前字符连续出现的长度，遇到不同字符就把计数器归零，同时维护全局最大值。  

> **类比**：把哈希表想象成一本字典，键（key）是单词，值（value）是页码。这里我们不需要哈希表，只用最原始的“遍历”来查找答案——就像你把字典从头到尾翻一遍，找出最长的同一页码的连续单词。

**为什么正确**：我们把**所有**可能的交换都尝试了一遍，必然会包含最优的那一次（或者根本不需要交换）。随后对每个得到的字符串都完整地检查了一遍最长的重复子串，所以最终答案一定是正确的。

#### 代码（Python）

```python
def max_rep_substring_bruteforce(text: str) -> int:
    n = len(text)
    best = 0

    # 枚举所有 i、j（包括 i==j 表示不交换）
    for i in range(n):
        for j in range(i, n):
            # 复制一份字符串并交换字符
            lst = list(text)
            lst[i], lst[j] = lst[j], lst[i]
            s = ''.join(lst)

            # 线性扫描求最长连续相同字符子串
            cur = 1
            max_len = 1
            for k in range(1, n):
                if s[k] == s[k - 1]:
                    cur += 1               # 同字符继续计数
                else:
                    max_len = max(max_len, cur)
                    cur = 1                # 重置计数
            max_len = max(max_len, cur)    # 处理最后一段

            best = max(best, max_len)      # 更新全局最优

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举 `i、j`，是 `O(n²)`；  
  - 每一次交换后再遍历一次字符串找最长子串是 `O(n)`。  
  - 所以整体是 `n² × n = n³`。  
  - 用大白话说：如果字符串长 1000，程序大概要跑 **十亿** 次基本操作，明显会超时。

- **空间复杂度**：`O(n)`  
  - 需要把字符串转成列表 `lst`（长度 `n`）进行交换；其余只使用常数级变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都完整遍历整个字符串**。其实我们只需要关注字符的**块（run）**——即连续相同字符形成的区间。  
观察可以发现，最长的可通过一次交换得到的重复子串只能出现在下面两种情况：

1. **单块内部**：直接把同字符块外面的一个相同字符（在别处）换进来，使块的长度+1（但不能超过该字符在整串中的出现次数）。
2. **两块之间被单个不同字符隔开**：例如 `aaa b aaa`，把 `b` 换成 `a`，两块合并成更长的 `a` 块。

因此只要 **记录每个字符块的长度**，并知道 **该字符在整个字符串出现的总次数**，就能在 **O(n)** 时间内算出答案。

实现步骤：

1. **统计每个字符的总出现次数**（哈希表 `cnt`），相当于“字典”，键是字符，值是出现次数。  
2. **跑一遍字符串做 Run‑Length Encoding（RLE）**，把相同字符的连续区间压缩成 `(char, length)` 的列表 `runs`。  
   - 例如 `"aaaba"` → `[('a',3), ('b',1), ('a',1)]`。  
3. **遍历 `runs`**，对每个块 `i`：
   - **情况 1**：如果 `cnt[char] > runs[i].length`，说明还有同字符在别处，可以把它搬进来，长度最多是 `runs[i].length + 1`。  
   - **情况 2**：检查相邻的两块 `i`、`i+2`（中间隔着恰好一个块 `i+1`，且 `i+1` 的长度为 1，且两端字符相同），则可以把中间的字符换成两端的字符，使两块合并。合并后的长度是 `runs[i].length + runs[i+2].length`，但仍受该字符总出现次数的上限 `cnt[char]` 限制（防止超过实际拥有的字符数）。
4. 在遍历过程中维护最大值 `ans`，最后返回 `ans`。

> **类比**：把字符串想象成一排排彩色积木，每块积木是同一种颜色的连续积木。我们可以把别的颜色的积木搬进来，或者把中间唯一的不同颜色积木换成两边的颜色，从而把两块同色积木粘在一起。只要知道每种颜色的积木总数，就能判断最多能粘多长。

#### 代码（Python）

```python
from collections import Counter
from typing import List, Tuple

def max_rep_substring(text: str) -> int:
    n = len(text)
    if n == 0:
        return 0

    # 1. 统计每个字符的总出现次数
    total_cnt = Counter(text)          # 例如 {'a':5, 'b':2}

    # 2. Run‑Length Encoding：把连续相同字符压缩成块
    runs: List[Tuple[str, int]] = []   # 每个元素是 (字符, 长度)
    i = 0
    while i < n:
        j = i
        while j < n and text[j] == text[i]:
            j += 1
        runs.append((text[i], j - i))
        i = j

    # 3. 遍历块，计算两种情况的最大长度
    ans = 0
    m = len(runs)
    for idx, (ch, length) in enumerate(runs):
        # 情况 1：块内部可以再拿进一个相同字符
        # 只能多加 1，且不能超过该字符的总出现次数
        if total_cnt[ch] > length:
            ans = max(ans, length + 1)
        else:
            ans = max(ans, length)          # 已经用尽所有该字符

        # 情况 2：检查 "块‑单字符‑块" 的模式
        # 需要保证中间块长度恰好为 1，且两端字符相同
        if idx + 2 < m:
            ch_next, len_next = runs[idx + 1]
            ch_next_next, len_next_next = runs[idx + 2]
            if ch == ch_next_next and ch_next == ch and len_next == 1:
                # 合并两端块的长度
                merged = length + len_next_next
                # 仍受该字符总数的上限限制
                merged = min(merged, total_cnt[ch])
                ans = max(ans, merged)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 统计字符次数、做 RLE、遍历块各只需要一次线性扫描。  
  - 用大白话说：如果字符串长 20,000，只会走大约 **6 万** 步（3 次遍历），非常快。

- **空间复杂度**：`O(k)`（`k` 为不同字符块的个数）  
  - 最坏情况下每个字符都不相同，块的数量等于 `n`，所以额外空间是 `O(n)`。  
  - 这主要是保存 `runs` 列表和哈希表 `total_cnt`，相当于把原字符串再复制一遍，但仍在可接受范围。

---

## 心得

- **核心技巧**：把字符串压缩成“块”（Run‑Length Encoding），并结合**字符总出现次数**判断是否可以通过一次交换把块扩展或合并。  
- **适用的题型**  
  1. “最长连续相同字符子串，允许最多一次修改/交换” 类题（如 LeetCode 1156、424 等）。  
  2. “在字符序列中合并相同颜色的区间” 这类需要**区间合并**的题目。  
- **一句话总结**：一次交换只可能把**相邻的两块**或**块内部再补一个相同字符**，把问题转化为块的长度比较即可。

---

## 反思

- **第一反应**：直接把所有可能的交换枚举完再检查——最自然但会超时。  
- **最容易踩的坑**  
  - 忘记检查**总字符数的上限**，导致合并后长度超过实际拥有的字符数。  
  - 只考虑“块‑块”合并，而遗漏了“块内部再补一个字符”的情况。  
  - 边界情况：字符串全是同字符时，直接返回长度；或只有一个字符出现一次时，答案只能是 1。  
- **下次遇到同类题**：第一步先**做 Run‑Length Encoding**，看能否把问题抽象为“块之间的关系”，再根据**总出现次数**决定是否可以通过一次操作扩展或合并块。这样即可在 `O(n)` 时间内得到最优解。