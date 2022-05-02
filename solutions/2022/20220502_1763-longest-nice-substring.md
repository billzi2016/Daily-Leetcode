# #1763. **最长优美子串** / Longest Nice Substring

> 难度：简单 · 标签：Hash Table、String、Divide and Conquer、Bit Manipulation、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-nice-substring/)

---

## 题目（英文原版）

**Description**

A string s is nice if, for every letter of the alphabet that s contains, it appears both in uppercase and lowercase. For example, "abABB" is nice because 'A' and 'a' appear, and 'B' and 'b' appear. However, "abA" is not because 'b' appears, but 'B' does not.
Given a string s, return the longest substring of s that is nice. If there are multiple, return the substring of the earliest occurrence. If there are none, return an empty string.

**Examples**

**Example 1:**

```
Input: s = "YazaAay"
Output: "aAa"
Explanation: "aAa" is a nice string because 'A/a' is the only letter of the alphabet in s, and both 'A' and 'a' appear.
"aAa" is the longest nice substring.
```

**Example 2:**

```
Input: s = "Bb"
Output: "Bb"
Explanation: "Bb" is a nice string because both 'B' and 'b' appear. The whole string is a substring.
```

**Example 3:**

```
Input: s = "c"
Output: ""
Explanation: There are no nice substrings.
```

**Constraints**

- 1 <= s.length <= 100
- s consists of uppercase and lowercase English letters.

---

## 题目（中文翻译）

一个字符串 `s` 被称为优美（nice），当且仅当 `s` 中出现的每一个字母（letter），其大写形式和小写形式都同时出现。例如，`"abABB"` 是优美的，因为 `'A'` 与 `'a'` 都出现，`'B'` 与 `'b'` 也都出现；而 `"abA"` 不是优美的，因为 `'b'` 出现了但 `'B'` 没出现。

给定字符串 `s`，返回 `s` 中最长的优美子串（substring）。如果存在多个长度相同的最长优美子串，返回最先出现的那个。如果不存在优美子串，返回空字符串 `""`。

**示例 1**  
**输入**: `s = "YazaAay"`  
**输出**: `"aAa"`  
**解释**: `"aAa"` 是优美的，因为字母表中唯一出现的字母是 `'A'/'a'`，且两者均出现。`"aAa"` 是最长的优美子串。

**示例 2**  
**输入**: `s = "Bb"`  
**输出**: `"Bb"`  
**解释**: `"Bb"` 是优美的，因为 `'B'` 与 `'b'` 都出现。整个字符串本身就是一个子串。

**示例 3**  
**输入**: `s = "c"`  
**输出**: `""`  
**解释**: 不存在优美子串。

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由大小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把所有可能的子串都枚举出来，逐个检查它是不是 “nice”。**  
- **枚举子串**：双层循环，外层固定子串的左边界 `i`，内层固定右边界 `j`（`i ≤ j`），这样可以得到所有 `O(n²)` 个子串。  
- **检查是否 nice**：对当前子串统计出现过的字母（不区分大小写），并记录它们出现的是大写还是小写。这里可以用 **哈希表**（在 Python 中用 `dict` 或 `set`）来存放信息。把哈希表想象成一本**字典**，键是字母，值是“是否出现大写、是否出现小写”。如果对每个键，两者都有，则说明子串满足 “nice”。  
- **记录最长**：在检查完每个子串后，若它是 nice 且长度比目前保存的最长子串更长，就更新答案。若长度相等则保留最先出现的子串（因为我们是从左到右枚举的）。  

**为什么正确？**  
枚举了所有子串，且每个子串都经过严格的 “nice” 判定，只要把最长的保存下来，就一定得到题目要求的答案。  

**时间/空间复杂度**  
- **时间**：枚举子串需要 `O(n²)` 次（外层 `n`，内层平均 `n/2`），每次检查子串时最坏需要遍历子串本身，长度最多 `n`，于是总时间是 `O(n³)`。在本题 `n ≤ 100`，即使 `O(n³)` 也能跑完。  
- **空间**：检查子串时使用的哈希表最多存放 26 个字母的信息，视作 `O(1)`（常数空间）。  

#### 代码（Python）  

```python
def longestNiceSubstring_bruteforce(s: str) -> str:
    n = len(s)
    best = ""                     # 保存当前找到的最长 nice 子串
    # i 为子串左端点，j 为右端点（包含）
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j+1]        # 当前子串
            # 用两个集合分别记录出现过的大写和小写字母
            lower = set()
            upper = set()
            for ch in sub:
                if ch.islower():
                    lower.add(ch)            # 小写字母加入 lower
                else:
                    upper.add(ch)            # 大写字母加入 upper
            # 判断子串是否 nice：每个出现的字母，要么同时在 lower 和 upper
            nice = True
            for ch in set(sub.lower()):      # 只遍历一次字母表
                if (ch not in lower) or (ch.upper() not in upper):
                    nice = False
                    break
            if nice and len(sub) > len(best):
                best = sub
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 解释：`n` 是字符串长度。外层两层循环产生 `≈ n²` 个子串；对每个子串我们最坏要遍历它一次（`O(n)`），所以乘起来是 `O(n³)`。  
- **空间复杂度**：`O(1)`（常数空间）  
  - 解释：只用了若干个大小固定的集合，最多 26 个字母，不随 `n` 增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **“枚举所有子串”**——大部分子串根本不可能是 nice，浪费了大量时间。  
观察题目可以得到一个关键性质：

> **如果一个字符 `c`（不论大小写）在子串中只出现了单一形式（只有大写或只有小写），那么以 `c` 为界，子串不可能是 nice。**  

换句话说，**只要在当前区间里找到一个“单身字符”，整个区间就一定不合法**，我们可以把它当作分割点，把区间划分成左、右两段，递归地在这两段里寻找最长的 nice 子串。  

这正是 **分治（Divide and Conquer）** 的思路：  

1. **统计整个区间的字符情况**。用两个位掩码（bitmask）或两个集合分别记录出现的大写和小写字母。这里用 **位运算** 更高效：  
   - 设 `lowerMask` 的第 `k` 位为 1，表示字母 `'a'+k` 出现过小写形式。  
   - `upperMask` 同理表示大写形式。  
2. **找出第一个“单身字符”**：遍历 26 个字母，如果某一位在 `lowerMask` 和 `upperMask` 中只出现一次（即 `lowerMask & (1<<k) == 0` 或 `upperMask & (1<<k) == 0`），则该字母对应的字符在区间里不完整。  
3. **若不存在单身字符**，说明整个区间已经是 nice，直接返回。  
4. **若存在**，把区间在该字符出现的位置全部切开（因为该字符可能出现多次），对每个子区间递归求解，取最长的结果。  

**为什么正确？**  
- 任何包含单身字符的子串都不可能是 nice（因为缺少对应的大写/小写），所以切开后不影响答案。  
- 递归的子问题规模严格小于父问题，最终会在没有单身字符的区间停下来，返回合法的 nice 子串。  

**时间复杂度**  
每一层递归会遍历当前区间一次来统计字符（`O(len)`），随后再遍历一次找切分点，整体是线性。最坏情况下，每次只切掉一个字符，递归深度为 `n`，于是总时间仍是 `O(n²)`，但对 `n ≤ 100` 完全足够且在实际数据中往往接近 `O(n)`。  

**空间复杂度**  
递归栈深度最多 `n`，每层保存常数个变量，故 `O(n)`（最坏），但同样是常数级别的额外空间。  

#### 代码（Python）  

```python
def longestNiceSubstring(s: str) -> str:
    """
    分治求最长 nice 子串
    """
    def helper(l: int, r: int) -> str:
        """返回 s[l:r]（左闭右开）区间内的最长 nice 子串"""
        if r - l < 2:               # 长度 < 2 不可能同时出现大小写
            return ""

        # 统计区间内出现的大写、小写，用位掩码（26 位整数）表示
        lower_mask = 0
        upper_mask = 0
        for i in range(l, r):
            ch = s[i]
            if 'a' <= ch <= 'z':
                lower_mask |= 1 << (ord(ch) - ord('a'))
            else:  # 'A' <= ch <= 'Z'
                upper_mask |= 1 << (ord(ch) - ord('A'))

        # 找到第一个“单身字符”所在的位置
        # 如果每个字母的大小写都同时出现，则区间已经是 nice
        for i in range(l, r):
            ch = s[i]
            idx = ord(ch.lower()) - ord('a')
            # 判断该字母是否同时出现大小写
            if not ( (lower_mask >> idx) & 1 and (upper_mask >> idx) & 1 ):
                # 以 i 为分割点，递归左右子区间
                left = helper(l, i)
                right = helper(i + 1, r)
                # 取更长的；若相等返回左边（更早出现）
                return left if len(left) >= len(right) else right

        # 循环结束说明没有单身字符，整个区间本身就是 nice
        return s[l:r]

    return helper(0, len(s))
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（最坏）  
  - 解释：每层递归线性遍历当前子串；最坏情况下每次只能切掉一个字符，递归深度为 `n`，于是总体是 `n + (n‑1) + … + 1 = O(n²)`。在实际随机字符串中，往往会一次切掉多个字符，接近 `O(n)`。  
- **空间复杂度**：`O(n)`（递归栈）  
  - 解释：递归深度最多等于字符串长度 `n`，每层只用常数额外空间。  

---  

## 心得  

- **核心技巧**：**分治 + 位掩码（或哈希表）判断字符是否同时出现大小写**。  
- **适用的题型**：  
  1. “最长子串满足某种对称/配对条件”——如 *Longest Substring with All Unique Characters*（可以用位掩码加滑动窗口）。  
  2. “在字符串中找出满足全/不存在某类字符的子段”——如 *Longest Substring Containing All 3 Characters*。  
  3. “通过分割不合法字符递归求解”——如 *Longest Substring Without Repeating Characters* 的分治版。  
- **一句话总结**：**只要找到“破坏 nice 条件的字符”，把它当作切点，递归求解剩余部分，即可快速得到最长 nice 子串。**  

---  

## 反思  

- **第一反应**：直接想到枚举所有子串并逐一检查——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记处理 **大小写对应** 的关系，只检查出现过的字母而不区分大小写。  
  - 边界情况：字符串长度为 0、1 时直接返回空串。  
  - 在分治实现时，如果只在 **第一个单身字符** 处切割，而不继续在同一字符的后续出现处切割，可能漏掉合法子串。正确做法是递归左右两段，左段不包括该字符，右段从该字符的下一位开始。  
- **下次遇到同类题**，第一步应该：**统计当前区间的字符出现情况，找出“不完整的字符”，并以它们为分割点进行递归或滑动窗口**。这样可以避免无谓的全枚举，显著提升效率。