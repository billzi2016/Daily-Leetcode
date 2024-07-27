# #2800. 包含三个字符串的最短字符串 / Shortest String That Contains Three Strings

> 难度：中等 · 标签：String、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/shortest-string-that-contains-three-strings/)

---

## 题目（英文原版）

**Description**

If there are multiple such strings, return the lexicographically smallest one.
Return a string denoting the answer to the problem.
Notes

**Examples**

**Example 1:**

```
Input: a = "abc", b = "bca", c = "aaa"
Output: "aaabca"
Explanation:  We show that "aaabca" contains all the given strings: a = ans[2...4], b = ans[3..5], c = ans[0..2]. It can be shown that the length of the resulting string would be at least 6 and "aaabca" is the lexicographically smallest one.
```

**Example 2:**

```
Input: a = "ab", b = "ba", c = "aba"
Output: "aba"
Explanation: We show that the string "aba" contains all the given strings: a = ans[0..1], b = ans[1..2], c = ans[0..2]. Since the length of c is 3, the length of the resulting string would be at least 3. It can be shown that "aba" is the lexicographically smallest one.
```

**Constraints**

- 1 <= a.length, b.length, c.length <= 100
- a, b, c consist only of lowercase English letters.

---

## 题目（中文翻译）

如果存在多个满足条件的字符串，返回字典序（lexicographically）最小的那个。返回一个表示答案的字符串。

**示例 1**  
**输入**: a = "abc", b = "bca", c = "aaa"  
**输出**: "aaabca"  
**解释**: 我们可以看到 `"aaabca"` 包含所有给定的字符串：a = ans[2...4], b = ans[3..5], c = ans[0..2]。可以证明，结果字符串的长度至少为 6，且 `"aaabca"` 是字典序最小的。

**示例 2**  
**输入**: a = "ab", b = "ba", c = "aba"  
**输出**: "aba"  
**解释**: 可以看到字符串 `"aba"` 包含所有给定的字符串：a = ans[0..1], b = ans[1..2], c = ans[0..2]。由于 c 的长度为 3，结果字符串的长度至少为 3，且 `"aba"` 是字典序最小的。

**约束条件**  
- 1 ≤ a.length, b.length, c.length ≤ 100  
- a、b、c 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的字符串都列举出来**，然后挑出既包含 `a`、`b`、`c` 又最短、字典序最小的那个。  
可以这样做：

1. 设答案的长度不超过 `len(a)+len(b)+len(c)`（把三个字符串全部拼在一起的长度一定够），从最小的可能长度 `L = max(len(a),len(b),len(c))` 开始枚举。  
2. 对每个长度 `L`，把所有由小写字母组成的长度为 `L` 的字符串都生成（相当于 `26^L` 种），检查它是否同时包含 `a`、`b`、`c` 这三个子串。  
3. 第一次找到满足条件的字符串，就是长度最小的；如果同一长度有多个，按字典序（字母表顺序）取最小的。

> **类比**：这相当于在一本巨大的字典里查找符合三个“关键词”的词，字典的每一页都是一种可能的拼法。  

**为什么会对**：只要枚举到真正的最短答案，就一定会被检测到，因为我们把所有可能的字符串都遍历了。

**时间/空间分析**：

- 枚举的字符串数是 `26^L`，`L` 甚至可能是 30（因为每个字符串最长 100，最短答案也可能接近 300）。`26^30` 天文数字，根本不可计算。  
- 检查子串是否出现只需要 `O(L)`（利用 Python 的 `in`），但这点不重要，因为枚举本身已经太慢。  

> **大白话**：暴力解的时间复杂度大约是 `O(26^L * L)`，即“每增加一个字符，可能的组合就会乘以 26”。这在现实机器上根本跑不完，等同于让电脑数到宇宙的原子数。

#### 代码（Python）

```python
import itertools

def brute(a: str, b: str, c: str) -> str:
    # 最短可能长度不小于最长的那个字符串
    min_len = max(len(a), len(b), len(c))
    # 最多不超过三个字符串全部相连的长度
    max_len = len(a) + len(b) + len(c)

    for L in range(min_len, max_len + 1):
        # 生成所有长度为 L 的小写字母串（这里用 * 只是示意，实际不可运行）
        for chars in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=L):
            s = ''.join(chars)
            if a in s and b in s and c in s:
                return s   # 第一个找到的就是字典序最小的
    return ""   # 理论上不会到这里
```

> **注意**：上述代码仅作思想演示，实际运行会因 `itertools.product` 的指数爆炸而卡死。

#### 复杂度  

- **时间复杂度**：`O(26^L * L)`，`L` 为答案长度。  
  - 含义：每多加一个字符，可能的组合就会乘以 26，几乎不可能在有限时间内完成。  
- **空间复杂度**：`O(L)`，只存一条正在检查的字符串。  

---

### 2. 最优解

#### 思路  

因为只需要 **三个** 字符串，我们可以利用「**全排列 + 最大重叠**」的思路把搜索空间压到常数级（6 种排列），并在每一种排列里用**贪心**把两个字符串尽可能紧密地粘在一起。

1. **先把“被包含”的字符串去掉**  
   - 如果 `a` 已经是 `b` 的子串，则在最终答案里只需要考虑 `b`（`a` 已经自然出现了）。  
   - 同理检查 `b`、`c`。这一步可以把问题规模进一步缩小。

2. **枚举 3! = 6 种拼接顺序**  
   - 设顺序为 `s1 → s2 → s3`。我们先把 `s1` 当作当前答案，然后把 `s2`「粘」到后面，使得两者的重叠最长；再把 `s3` 同理粘上去。  

3. **如何求两个字符串的最短共存方式（最大重叠）**  
   - 只需要找 `k`（`0 ≤ k ≤ min(len(s1), len(s2))`），使得 `s1` 的后 `k` 个字符恰好等于 `s2` 的前 `k` 个字符。  
   - 把 `s2` 的剩余 `len(s2)-k` 个字符接到 `s1` 末尾，即得到包含两者的最短字符串。  
   - 这一步类似 **拼图**：把两块可以对齐的边缘尽量贴紧。

4. **把三块拼完后得到 6 条候选答案**  
   - 在这 6 条中，挑 **长度最短** 的；若有多条长度相同，挑 **字典序最小** 的。  

> **核心技巧**：  
> - **最大重叠**（Suffix‑Prefix Overlap）把两个字符串“拼”得最紧。  
> - **全排列** 把所有可能的先后顺序穷举，因为只有 3 条字符串，枚举成本是常数。  

#### 代码（Python）

```python
from itertools import permutations

def overlap(s1: str, s2: str) -> int:
    """
    返回 s1 的后缀与 s2 的前缀能够匹配的最大长度 k。
    例如 s1='abca', s2='caa' => k=2，因为 'ca' == 'ca'。
    """
    max_k = min(len(s1), len(s2))
    for k in range(max_k, 0, -1):          # 从大到小尝试，找到最大匹配
        if s1[-k:] == s2[:k]:
            return k
    return 0                                # 完全不匹配

def merge(s1: str, s2: str) -> str:
    """
    把两个字符串合并成最短的、同时包含两者的字符串。
    只在 s1 末尾追加字符（相当于 “在后面粘”）。
    """
    # 如果 s2 已经是 s1 的子串，直接返回 s1
    if s2 in s1:
        return s1
    # 如果 s1 已经是 s2 的子串，返回 s2（因为我们把 s2 放在后面）
    if s1 in s2:
        return s2
    k = overlap(s1, s2)                     # 最大重叠长度
    return s1 + s2[k:]                      # 只把 s2 剩余部分接上去

def shortest_superstring(a: str, b: str, c: str) -> str:
    # 第一步：去掉被其它字符串包含的字符串
    strs = [a, b, c]
    # 只保留“没有被其他字符串完整包含”的
    filtered = []
    for s in strs:
        if not any(s != t and s in t for t in strs):
            filtered.append(s)

    # 如果过滤后只剩一个，直接返回它
    if len(filtered) == 1:
        return filtered[0]

    best = None
    # 枚举所有排列
    for perm in permutations(filtered):
        cur = perm[0]
        cur = merge(cur, perm[1])
        cur = merge(cur, perm[2])
        # 更新答案：先比较长度，再比较字典序
        if (best is None or
            len(cur) < len(best) or
            (len(cur) == len(best) and cur < best)):
            best = cur
    return best
```

> **关键行中文注释** 已写在代码里，帮助理解每一步在做什么。

#### 复杂度  

- **时间复杂度**：  
  - 枚举 6 种排列是常数 `O(1)`。  
  - `overlap` 最坏需要比较 `O(L)`（`L` 为两字符串最短长度），而我们在每次 `merge` 中调用一次。  
  - 合并三次，整体时间 `O(L1 + L2 + L3)`，即 **线性** 与输入长度成正比。  
  - **含义**：即使每个字符串长度都是 100，程序也只跑几千次字符比较，瞬间结束。

- **空间复杂度**：  
  - 只使用了若干临时字符串和常数级的辅助变量，**`O(L)`**（存放当前合并结果）。  
  - 含义：占用的内存随答案长度线性增长，最多约 300 个字符，几乎可以忽略。

---

## 心得

- **核心技巧**：**最大后缀‑前缀重叠** + **全排列枚举**（因为字符串个数极少）。  
- **适用的题型**：  
  1. “最短公共超字符串”（Shortest Common Superstring）——通常会用 DP 或贪心，当字符串数量很少时可以枚举全排列。  
  2. “合并若干单词，使得所有单词都是子串”——同样利用重叠拼接。  
  3. “把若干段 DNA 序列拼成最短基因组”——生物信息学中的类似问题。

- **一句话总结解题钥匙**：**把每两个字符串的重叠最大化，再把所有排列都试一遍，挑最短、字典序最小的**。

---

## 反思

- **拿到题目第一反应**：想到“把三个字符串全部拼起来，然后删掉重复的部分”。于是立刻想到“找重叠”。  
- **最容易踩的坑**  
  1. **忽略子串关系**：如果 `a` 已经是 `b` 的子串，直接把 `a` 当作独立处理会导致不必要的额外字符。  
  2. **只考虑 `s1` → `s2` 的重叠**，忘记枚举不同顺序会漏掉更短的组合。  
  3. **字典序比较**：长度相同的候选答案需要再比较字典序，否则可能得到错误的“最小”答案。  
- **下次遇到同类题**：第一步先 **去除被包含的字符串**，随后 **枚举所有排列**，在每一次合并时 **求最大后缀‑前缀重叠**。这样既保证最短，又保证字典序最小。