# #3455. 最短匹配子串 / Shortest Matching Substring

> 难度：困难 · 标签：Two Pointers、String、Binary Search、String Matching · [LeetCode 链接](https://leetcode.com/problems/shortest-matching-substring/)

---

## 题目（英文原版）

**Description**

You are given a string s and a pattern string p, where p contains exactly two '*' characters.
The '*' in p matches any sequence of zero or more characters.
Return the length of the shortest substring in s that matches p. If there is no such substring, return -1.

**Examples**

**Example 1:**

```
Input: s = "abaacbaecebce", p = "ba*c*ce"
Output: 8
Explanation:
The shortest matching substring of p in s is " ba e c eb ce " .
```

**Example 2:**

```
Input: s = "baccbaadbc", p = "cc*baa*adb"
Output: -1
Explanation:
There is no matching substring in s .
```

**Example 3:**

```
Input: s = "a", p = "**"
Output: 0
Explanation:
The empty substring is the shortest matching substring.
```

**Example 4:**

```
Input: s = "madlogic", p = "*adlogi*"
Output: 6
Explanation:
The shortest matching substring of p in s is " adlogi " .
```

**Constraints**

- 1 <= s.length <= 105
- 2 <= p.length <= 105
- s contains only lowercase English letters.
- p contains only lowercase English letters and exactly two '*'.

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `s` 和一个模式字符串 `p`，其中 `p` 恰好包含两个 `'*'` 字符。  
`'*'` 可以匹配任意长度（包括零）的字符序列。  
返回 `s` 中能够匹配 `p` 的最短子字符串（substring）的长度。如果不存在满足条件的子字符串，返回 `-1`。

**示例**

**示例 1**  
输入: `s = "abaacbaecebce", p = "ba*c*ce"`  
输出: `8`  
解释:  
匹配 `p` 的最短子字符串是 `"baecebce"`，长度为 8。

**示例 2**  
输入: `s = "baccbaadbc", p = "cc*baa*adb"`  
输出: `-1`  
解释:  
在 `s` 中不存在匹配 `p` 的子字符串。

**示例 3**  
输入: `s = "a", p = "**"`  
输出: `0`  
解释:  
空子字符串（empty substring）是最短的匹配子串。

**示例 4**  
输入: `s = "madlogic", p = "*adlogi*"`  
输出: `6`  
解释:  
匹配 `p` 的最短子字符串是 `"adlogi"`，长度为 6。

**约束条件**  
- `1 <= s.length <= 10^5`  
- `2 <= p.length <= 10^5`  
- `s` 仅由小写英文字母组成。  
- `p` 仅由小写英文字母和恰好两个 `'*'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的子串**，然后检查它是否能匹配模式 `p`。  
- **子串**：在原字符串 `s` 中任选一个左端点 `l` 与右端点 `r`（`0 ≤ l ≤ r ≤ len(s)`），子串即 `s[l:r]`。  
- **匹配**：把模式 `p` 中的两个 `*` 当成 “可以匹配任意长度（包括 0）” 的通配符，用两指针分别在子串和模式上前进，遇到 `*` 时尝试把它匹配成 0、1、2 … 个字符，直到整个模式走完。

> **类比**：把 `*` 想成一本空白的日记本，里面可以写任意数量的字符（甚至不写）。我们只需要尝试所有“写法”，看能否恰好把子串填满这本日记本。

**为什么一定能得到答案**：因为我们把 **所有** 子串都试了一遍，并且对每个子串尝试了 **所有** `*` 的可能长度，只要存在匹配的子串，必然会在枚举过程中被发现。

**时间/空间复杂度**  
- 枚举子串的次数是 `O(n²)`（左端点 * 右端点），每次匹配需要遍历子串和模式，最坏情况是 `O(m)`（`m = len(p)`），于是总时间是 `O(n²·m)`。  
- 只使用常数级别的额外变量，空间是 `O(1)`。

> **大白话**：如果 `s` 长 10⁵，`n²` 大约是 10¹⁰——这比一天的秒数还多，显然不可接受。

#### 代码（Python）

```python
def matches(sub: str, pat: str) -> bool:
    """
    判断子串 sub 是否能匹配模式 pat（其中恰好有两个 *）。
    采用两指针 + 回溯的朴素实现。
    """
    i = j = 0               # i -> sub, j -> pat
    star1 = star2 = -1      # 记录最近一次 * 的位置
    match1 = match2 = 0     # * 对应匹配了多少字符

    while i < len(sub):
        if j < len(pat) and (pat[j] == sub[i] or pat[j] == '*'):
            if pat[j] == '*':
                # 第一次遇到 *，记录位置并尝试匹配 0 个字符
                if star1 == -1:
                    star1, match1 = j, i
                elif star2 == -1:
                    star2, match2 = j, i
                else:
                    # 第三个 *（题目保证不会出现）不处理
                    return False
                j += 1
            else:               # 普通字符匹配成功
                i += 1
                j += 1
        else:
            # 当前字符不匹配，尝试让最近的 * 多匹配一个字符
            if star2 != -1:
                # 用第二个 * 来吃字符
                match2 += 1
                i = match2
                j = star2 + 1
            elif star1 != -1:
                match1 += 1
                i = match1
                j = star1 + 1
            else:
                return False

    # 处理模式剩余的 *（可以匹配空串）
    while j < len(pat) and pat[j] == '*':
        j += 1
    return j == len(pat)


def shortest_match_bruteforce(s: str, p: str) -> int:
    n = len(s)
    best = None
    for l in range(n + 1):                # 左端点可以在最右边的“空位”
        for r in range(l, n + 1):        # 右端点可以等于左端点 → 空子串
            if matches(s[l:r], p):
                length = r - l
                if best is None or length < best:
                    best = length
    return -1 if best is None else best
```

> 代码里每一行都加了中文注释，帮助你一步步跟踪指针的移动。

#### 复杂度

- **时间复杂度**：`O(n²·m)`  
  解释：我们要检查 `≈ n²/2` 个子串，每个子串的匹配过程最坏要遍历整个模式 `m`（`m ≤ 10⁵`），所以整体是 `n²·m`。
- **空间复杂度**：`O(1)`  
  只用了几个整数指针和标记，不会随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于 **枚举所有子串**。其实我们只需要关注 **模式中的固定字符**，`*` 只负责“留出空位”。  
模式 `p` 正好有两个 `*`，我们可以把它拆成 **三段**：

```
p = A * B * C
```

- `A`、`B`、`C` 都是不含 `*` 的普通字符串（可能为空）。
- `*` 只负责在 `A`、`B`、`C` 之间填充任意长度（包括 0）。

要让一个子串 `s[l:r]` 匹配 `p`，必须满足：

1. `A` 出现在 `s` 的 **左端**，即 `s[l : l+|A|] == A`。
2. 在 `A` 之后（可以紧贴也可以有间隔），出现一次 `B`。
3. 在 `B` 之后（同理），出现一次 `C`，并且 `C` 必须 **恰好在子串的右端**。

于是子串的长度只取决于 **三次出现的起始位置**：

```
length = (posC + |C|) - posA
```

> **类比**：把 `A、B、C` 想成三块拼图，`*` 是可以随意拉伸的橡皮带，只要三块拼图按顺序摆好，橡皮带自然会把它们连在一起。我们想让整体尽可能短，只需要把每块拼图往左、往右“靠拢”到最近的合法位置。

**关键步骤**：

1. **找出所有出现位置**  
   使用 **KMP（Knuth-Morris-Pratt）** 或其他线性匹配算法，得到 `A`、`B`、`C` 在 `s` 中的全部起始下标。  
   - 如果某段为空字符串，按照约定它可以匹配 **每一个位置**（包括字符串末尾），即返回 `[0, 1, …, n]`。

2. **利用二分查找**（`bisect`）在已排序的出现列表中快速定位“最近的合法位置”。  
   对每个 `posA`：
   - 在 `B` 的出现列表里找第一个 `posB ≥ posA + |A|`（保证 `B` 出现在 `A` 之后）。
   - 再在 `C` 的出现列表里找第一个 `posC ≥ posB + |B|`。
   - 计算对应的子串长度，取最小值。

3. **时间复杂度分析**  
   - KMP 找所有匹配的时间是 `O(n + |segment|)`，对三段共 `O(n + |p|)`。  
   - 对每个 `posA` 进行两次二分查找，复杂度 `O(log k)`（`k` 为对应段的出现次数）。最坏情况下出现次数是 `O(n)`，于是整体是 `O(n log n)`。  
   - 这已经远远小于暴力的 `O(n²)`，在 `n ≤ 10⁵` 时轻松跑完。

> **为什么比暴力快**：我们不再枚举子串，而是只遍历 **A 的出现位置**（最多 `n` 次），每次通过二分直接定位最近的合法 `B`、`C`，省掉了大量无意义的尝试。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

def kmp_occurrences(text: str, pattern: str) -> List[int]:
    """
    KMP 找出 pattern 在 text 中所有起始下标（左闭右开）。
    若 pattern 为空，返回所有可能的下标 0..len(text)。
    """
    if not pattern:                     # 空模式匹配每个位置
        return list(range(len(text) + 1))

    # 1️⃣ 构造 next（部分匹配表）
    m = len(pattern)
    nxt = [-1] * (m + 1)
    i, j = 0, -1
    while i < m:
        while j != -1 and pattern[i] != pattern[j]:
            j = nxt[j]
        i += 1
        j += 1
        nxt[i] = j

    # 2️⃣ 主匹配过程
    occ = []
    i = j = 0
    n = len(text)
    while i < n:
        while j != -1 and (j == m or pattern[j] != text[i]):
            j = nxt[j]
        i += 1
        j += 1
        if j == m:                      # 找到一次匹配
            occ.append(i - m)           # 记录起始下标
    return occ


def shortest_match_optimal(s: str, p: str) -> int:
    n = len(s)

    # ----- 1️⃣ 把模式拆成 A * B * C -----
    first = p.find('*')
    second = p.find('*', first + 1)
    A = p[:first]
    B = p[first + 1:second]
    C = p[second + 1:]

    # ----- 2️⃣ 找出每段的所有出现位置 -----
    occA = kmp_occurrences(s, A)
    occB = kmp_occurrences(s, B)
    occC = kmp_occurrences(s, C)

    # 如果任意一段在 s 中根本不存在（且不是空串），直接返回 -1
    if not occA or not occB or not occC:
        return -1

    lenA, lenB, lenC = len(A), len(B), len(C)
    ans = None

    # ----- 3️⃣ 枚举 A 的起始位置，二分找最近的 B、C -----
    for posA in occA:
        # B 必须出现在 A 结束之后（可以紧贴）
        minB = posA + lenA
        idxB = bisect_left(occB, minB)
        if idxB == len(occB):
            continue                     # 没有合法的 B
        posB = occB[idxB]

        # C 必须出现在 B 结束之后
        minC = posB + lenB
        idxC = bisect_left(occC, minC)
        if idxC == len(occC):
            continue                     # 没有合法的 C
        posC = occC[idxC]

        # 计算子串长度：从 A 的左端到 C 的右端
        cur_len = (posC + lenC) - posA
        if ans is None or cur_len < ans:
            ans = cur_len

    return -1 if ans is None else ans
```

**代码要点解释**：

- `kmp_occurrences`：使用 KMP 在 `O(n+|pattern|)` 时间返回所有匹配下标。空模式时返回 `0..n`，对应 `*` 可以匹配空串的情况。
- `bisect_left`：二分查找列表中第一个 **不小于** 给定值的元素，正好满足 “必须在前一段结束之后出现” 的要求。
- `posA、posB、posC` 分别是 `A、B、C` 的起始下标，`lenA、lenB、lenC` 用来确保不越界。
- 若任意段找不到合法位置（列表为空），答案直接是 `-1`。

#### 复杂度

- **时间复杂度**：`O(n + |p| + n log n)` → 实际上是 `O(n log n)`，因为 `|p| ≤ 2·10⁵` 与 `n` 同阶。  
  - KMP 三次遍历 `s`：`O(n)`。  
  - 对每个 `A` 出现位置进行两次二分查找：`O(k log n)`，`k ≤ n`。  
  与暴力的 `O(n²·m)` 相比，下降了至少一个数量级，轻松通过 10⁵ 规模的测试。

- **空间复杂度**：`O(n)` 用于保存三段的出现列表（最坏每个列表长度为 `n+1`），额外的辅助数组（KMP 的 `next`）也是 `O(|segment|)`，总体不超过线性空间。

---

## 心得

- **核心技巧**：把仅有两个 `*` 的模式拆成 **三段固定子串**，利用 **KMP**（线性匹配）快速定位所有出现位置，再用 **二分查找** 在有序列表中找最近的合法组合，从而得到最短匹配子串。
- **适用的题型**  
  1. `*`（或 `?`）数量固定、可以把模式分段的字符串匹配题。  
  2. “最短/最长子串满足若干顺序出现的子序列” 类问题（如 “最短子串包含 `a`、`b`、`c` 按顺序”）。  
  3. 多段模式匹配 + 最小化覆盖区间的场景（如 “最小覆盖子数组” 的变形）。
- **解题钥匙**：**把通配符两侧的真实字符提取出来，分别定位它们的出现位置，再在位置序列上做“最近合法配对”。**

---

## 反思

- **第一反应**：看到只有两个 `*`，立刻想到把模式切成三段，然后在原串里找这些段的出现位置。  
- **最容易踩的坑**  
  1. **空段的处理**：`A、B、C` 可能为空，需要把空串视为“匹配每个位置”。忘记这点会导致索引越界或错误的 `-1`。  
  2. **`*` 能匹配空串**：在二分查找时必须使用 “≥” 而不是 “>”，否则会错过 `B` 正好紧跟 `A` 的情况。  
  3. **重复出现的段**：同一段可能在 `s` 中出现很多次，必须用二分快速定位最近合法的那一次，而不是线性遍历全部。  
- **下次类似题的第一步**：**先把模式中的固定子串抽出来**，统计它们在原串的出现位置；随后在这些位置上思考“如何把它们按顺序、尽量靠近地拼接”。这样可以把指数级的枚举压缩到线性或对数级别。