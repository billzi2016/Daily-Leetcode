# #2781. **最长有效子串的长度** / Length of the Longest Valid Substring

> 难度：困难 · 标签：Array、Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/length-of-the-longest-valid-substring/)

---

## 题目（英文原版）

**Description**

You are given a string word and an array of strings forbidden.
A string is called valid if none of its substrings are present in forbidden.
Return the length of the longest valid substring of the string word.
A substring is a contiguous sequence of characters in a string, possibly empty.

**Examples**

**Example 1:**

```
Input: word = "cbaaaabc", forbidden = ["aaa","cb"]
Output: 4
Explanation: There are 11 valid substrings in word: "c", "b", "a", "ba", "aa", "bc", "baa", "aab", "ab", "abc" and "aabc". The length of the longest valid substring is 4. 
It can be shown that all other substrings contain either "aaa" or "cb" as a substring.
```

**Example 2:**

```
Input: word = "leetcode", forbidden = ["de","le","e"]
Output: 4
Explanation: There are 11 valid substrings in word: "l", "t", "c", "o", "d", "tc", "co", "od", "tco", "cod", and "tcod". The length of the longest valid substring is 4.
It can be shown that all other substrings contain either "de", "le", or "e" as a substring.
```

**Constraints**

- 1 <= word.length <= 105
- word consists only of lowercase English letters.
- 1 <= forbidden.length <= 105
- 1 <= forbidden[i].length <= 10
- forbidden[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

你得到一个字符串 `word` 和一个字符串数组 `forbidden`。  
如果一个字符串的所有子串（subarray）都不出现在 `forbidden` 中，则称该字符串为**有效**（valid）。  
返回 `word` 中最长的有效子串的长度。  

子串是字符串中连续的字符序列，长度可以为 0。

**示例 1**

```text
Input: word = "cbaaaabc", forbidden = ["aaa","cb"]
Output: 4
```

**解释**：`word` 中共有 11 个有效子串：`"c"`, `"b"`, `"a"`, `"ba"`, `"aa"`, `"bc"`, `"baa"`, `"aab"`, `"ab"`, `"abc"` 和 `"aabc"`。最长的有效子串长度为 4。可以证明，所有其他子串都包含 `"aaa"` 或 `"cb"` 作为子串。

**示例 2**

```text
Input: word = "leetcode", forbidden = ["de","le","e"]
Output: 4
```

**解释**：`word` 中共有 11 个有效子串：`"l"`, `"t"`, `"c"`, `"o"`, `"d"`, `"tc"`, `"co"`, `"od"`, `"tco"`, `"cod"` 和 `"tcod"`。最长的有效子串长度为 4。可以证明，所有其他子串都包含 `"de"`、`"le"` 或 `"e"` 作为子串。

**约束条件**

- `1 <= word.length <= 10^5`
- `word` 仅由小写英文字母组成。
- `1 <= forbidden.length <= 10^5`
- `1 <= forbidden[i].length <= 10`
- `forbidden[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 子串都列举出来，逐个判断它们是否包含禁忌串 `forbidden` 中的任意一个。  
- **枚举子串**：双层循环，外层固定左端点 `l`，内层把右端点 `r` 从 `l` 往后推进，得到子串 `word[l:r+1]`。  
- **检查是否合法**：把 `forbidden` 放进一个 **哈希表**（想象成一本字典，单词是键，出现与否是值），然后遍历 `forbidden` 中的每个字符串，看它是否是当前子串的子序列（即 `sub in word[l:r+1]`）。  
- **记录最长**：只要子串合法，就更新答案 `max_len = max(max_len, r-l+1)`。

> **为什么能得到正确答案？**  
> 我们遍历了所有可能的连续子序列（子串），只要其中有一个不包含禁忌串，就会被计入答案；因为我们取了最大长度，自然得到最长的合法子串。

#### 代码（Python）

```python
def longestValidSubstring_bruteforce(word: str, forbidden: list[str]) -> int:
    # 把 forbidden 放进哈希表，查找 O(1)
    forbid_set = set(forbidden)

    n = len(word)
    max_len = 0

    # 枚举所有左端点 l
    for l in range(n):
        # 枚举所有右端点 r，形成子串 word[l:r+1]
        for r in range(l, n):
            sub = word[l:r + 1]          # 当前子串
            valid = True                 # 假设合法

            # 检查每个禁忌串是否出现在 sub 中
            for f in forbid_set:
                if f in sub:             # Python 的子串检测，实际是 O(len(sub)*len(f))
                    valid = False
                    break               # 只要发现一个禁忌，就不合法

            if valid:
                max_len = max(max_len, r - l + 1)   # 更新最长合法长度

    return max_len
```

> 关键行的中文注释已写在代码里，直接可以运行（不过会超时）。

#### 复杂度

- **时间复杂度**：`O(n² * m)`  
  - `n` 是 `word` 长度，双层循环产生约 `n²/2` 个子串。  
  - `m` 是 `forbidden` 中字符串的数量（最坏情况每个都要检查一次）。  
  - 用大白话说，就是“把 10 万个字符的每一对位置都配对检查，还要把 10 万个禁忌词一个个比对”，显然会慢到炸。

- **空间复杂度**：`O(m)`  
  - 只用了一个哈希表存 `forbidden`，其余变量都是常数级别。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：  
1. **子串枚举** 产生 `O(n²)`，太多。  
2. **每次检查** 需要遍历所有禁忌串，或在子串里做 `in` 操作，时间开销大。

我们需要 **一次遍历** 就能判断当前字符加入后，窗口（即当前合法子串）是否仍合法。  
观察题目限制：

- 每个禁忌串的长度 ≤ **10**（常数）。  
- 只要我们知道 **以当前位置结尾** 的子串中是否出现禁忌串，就能决定窗口左端点 `left` 必须往右移动到哪儿。

**核心想法：滑动窗口 + 哈希表**  

1. 把 `forbidden` 全部放进哈希表 `forbid_set`（查找 O(1)），相当于一本字典，单词是禁忌词，查找时只要看词是否在字典里。  
2. 维护一个左指针 `left`，表示当前合法窗口的左边界（窗口是 `word[left:i+1]`）。  
3. 从左到右遍历字符，设当前索引为 `i`（窗口右边界）。  
   - 因为禁忌串最长只有 10，我们只需要检查 **长度为 1~10**、**以 `i` 结尾** 的子串是否在 `forbid_set`。  
   - 具体做法：对每个可能的长度 `l = 1..10`（且 `i-l+1 >= 0`），取子串 `word[i-l+1 : i+1]`，如果它在 `forbid_set`，说明出现了禁忌串，起始位置是 `i-l+1`。  
   - 为了让窗口不包含这段禁忌串，左指针必须移动到 **禁忌串起始位置的右侧**，即 `left = max(left, i - l + 2)`（`+2` 因为下标从 0 开始，要跳到下一个字符）。  
4. 更新答案 `ans = max(ans, i - left + 1)`。

**为什么只检查到长度 10 就够了？**  
因为所有禁忌串的最长长度就是 10，若一个更长的子串包含禁忌串，那么它的 **结尾** 一定在某个长度 ≤10 的子串里已经检测到。于是只要把窗口左边界往右推到不碰到禁忌串的最左位置，后面的字符继续往右扩展即可。

**类比**：想象我们在一条路上走，路上有若干段 “禁行区”。每次走到新的一米时，往后看最多 10 米，如果发现自己刚进入了禁行区，就立刻把起点往前搬到禁行区的后面，确保整段路程都是安全的。

#### 代码（Python）

```python
def longestValidSubstring(word: str, forbidden: list[str]) -> int:
    # 1. 把所有禁忌串放进哈希表，查找相当于查字典
    forbid_set = set(forbidden)

    n = len(word)
    left = 0          # 当前合法窗口的左端点
    ans = 0
    max_len_forbid = 10   # 根据约束，禁忌串最长不超过 10

    # 2. 右指针 i 从左到右扫描
    for i in range(n):
        # 只需要检查长度 1~10、以 i 结尾的子串
        # Python 切片的左闭右开区间，i-l+1 要 >= 0
        for l in range(1, max_len_forbid + 1):
            if i - l + 1 < 0:   # 超出字符串左边界，停止
                break
            sub = word[i - l + 1 : i + 1]   # 取出长度为 l 的子串
            if sub in forbid_set:          # 发现禁忌串
                # 把左指针搬到禁忌串起始位置的右侧
                # 禁忌串起始下标是 i-l+1，右侧是 i-l+2
                left = max(left, i - l + 2)
                # 因为本次已经发现禁忌，后面更长的 l 不会再是禁忌
                #（更长子串必然包含这个禁忌），可以直接 break
                break

        # 3. 计算当前窗口长度并更新答案
        ans = max(ans, i - left + 1)

    return ans
```

**代码要点**  

- `forbid_set` 是哈希表，查找 `sub in forbid_set` 是 O(1)。  
- 内层循环最多跑 10 次（常数），所以整体是 **线性**。  
- 当检测到禁忌串后立刻 `break`，因为更长的子串一定已经包含了这个禁忌，无需继续检查。

#### 复杂度

- **时间复杂度**：`O(n * L)`，其中 `n = len(word)`，`L = 10`（禁忌串的最大长度）。  
  - 用大白话说，就是“遍历 10 万个字符，每个字符只检查至多 10 次”，约等于 1 百万次操作，跑得很快。  
  - 与暴力的 `O(n²)`（十万的平方是 10⁹）相比，快了几个数量级。

- **空间复杂度**：`O(m)`，`m = len(forbidden)`，用于存放哈希表。  
  - 额外的变量只有几个整数，忽略不计。  
  - 与暴力解相比，空间使用相同，但时间提升巨大。

---

## 心得

- **核心技巧**：**滑动窗口 + 限长子串检查**。  
  通过维护一个左边界，使得窗口始终保持“合法”，并利用禁忌串的长度上限只检查常数次。

- **该技巧适用的题型**  
  1. **最长不含子串的子数组/子串**（如 “Longest Substring Without Repeating Characters”）。  
  2. **带有限制长度的模式匹配**（如 “Maximum Length of a Subarray With Positive Product” 需要检查固定窗口）。  
  3. **禁止出现特定模式的区间**（如 “Maximum Size Subarray Sum Equals k” 中的窗口左移）。

- **一句话总结**：  
  *“只要把窗口左边界推到最近一次出现的禁忌子串的右侧，整个窗口就天然合法。”*

---

## 反思

- **拿到题目第一反应**：直接枚举所有子串检查是否合法（暴力思路），因为最直观的做法就是“把每一种可能都试一遍”。  

- **最容易踩的坑**  
  1. **忘记限制检查长度**：若把 `for l in range(1, n)` 写成遍历所有可能长度，时间会恢复到 `O(n²)`。  
  2. **左指针更新错误**：必须取 `max(left, i - l + 2)`，否则可能把左指针移动到更左的位置，导致仍包含禁忌。  
  3. **边界条件**：当 `i - l + 1 < 0` 时要提前 `break`，防止负下标导致错误的子串。  

- **下次遇到同类题，第一步该想到**：  
  *“禁忌模式的最大长度是常数吗？如果是，就把窗口右移时只检查最近的常数个子串；如果不是，需要考虑 Trie、Aho‑Corasick 等更高级的数据结构。”*