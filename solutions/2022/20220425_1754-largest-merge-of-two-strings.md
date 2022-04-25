# #1754. **最大合并字符串** / Largest Merge Of Two Strings

> 难度：中等 · 标签：Two Pointers、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/largest-merge-of-two-strings/)

---

## 题目（英文原版）

**Description**

You are given two strings word1 and word2. You want to construct a string merge in the following way: while either word1 or word2 are non-empty, choose one of the following options:
Return the lexicographically largest merge you can construct.
A string a is lexicographically larger than a string b (of the same length) if in the first position where a and b differ, a has a character strictly larger than the corresponding character in b. For example, "abcd" is lexicographically larger than "abcc" because the first position they differ is at the fourth character, and d is greater than c.

**Examples**

**Example 1:**

```
Input: word1 = "cabaa", word2 = "bcaaa"
Output: "cbcabaaaaa"
Explanation: One way to get the lexicographically largest merge is:
- Take from word1: merge = "c", word1 = "abaa", word2 = "bcaaa"
- Take from word2: merge = "cb", word1 = "abaa", word2 = "caaa"
- Take from word2: merge = "cbc", word1 = "abaa", word2 = "aaa"
- Take from word1: merge = "cbca", word1 = "baa", word2 = "aaa"
- Take from word1: merge = "cbcab", word1 = "aa", word2 = "aaa"
- Append the remaining 5 a's from word1 and word2 at the end of merge.
```

**Example 2:**

```
Input: word1 = "abcabc", word2 = "abdcaba"
Output: "abdcabcabcaba"
```

**Constraints**

- 1 <= word1.length, word2.length <= 3000
- word1 and word2 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`。你需要按照下面的方式构造一个字符串 `merge`：只要 `word1` 或 `word2` 任意一个非空，就从以下两种操作中任选其一：

1. 取 `word1` 的首字符并将其追加到 `merge`，随后 `word1` 删除该字符；
2. 取 `word2` 的首字符并将其追加到 `merge`，随后 `word2` 删除该字符。

返回你能够构造的 **字典序（lexicographically）** 最大的 `merge`。

若两个等长字符串 `a` 与 `b`，若在它们首次出现不同的字符位置上，`a` 的字符严格大于 `b` 的对应字符，则称 `a` 的字典序大于 `b`。例如，`"abcd"` 的字典序大于 `"abcc"`，因为它们在第四个字符处不同，`d > c`。

---

### 示例

**示例 1**  
```text
Input: word1 = "cabaa", word2 = "bcaaa"
Output: "cbcabaaaaa"
Explanation:
一种得到字典序最大的合并字符串的方法如下：
- 从 word1 取字符：merge = "c",  word1 = "abaa", word2 = "bcaaa"
- 从 word2 取字符：merge = "cb", word1 = "abaa", word2 = "caaa"
- 从 word2 取字符：merge = "cbc", word1 = "abaa", word2 = "aaa"
- 从 word1 取字符：merge = "cbca", word1 = "baa",  word2 = "aaa"
- 从 word1 取字符：merge = "cbcab", word1 = "aa",   word2 = "aaa"
- 从 word1 取字符：merge = "cbcaba", word1 = "a",    word2 = "aaa"
- 从 word2 取字符：merge = "cbcabaa", word1 = "a",    word2 = "aa"
- 从 word2 取字符：merge = "cbcabaaa", word1 = "a",    word2 = "a"
- 从 word1 取字符：merge = "cbcabaaaa", word1 = "",     word2 = "a"
- 从 word2 取字符：merge = "cbcabaaaaa", word1 = "",     word2 = ""
```

**示例 2**  
```text
Input: word1 = "abcabc", word2 = "abdcaba"
Output: "abdcabcabcaba"
```

---

### 约束条件

- `1 <= word1.length, word2.length <= 3000`
- `word1` 与 `word2` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的合并方式**，找出字典序最大的那个。  
- 我们可以把 `word1` 和 `word2` 看成两条“排队的队伍”。每一步从队首取走一个字符放进结果 `merge`，直到两条队伍都空为止。  
- 暴力做法就是把每一种“取走顺序”全部列出来，然后比较得到的完整字符串大小。  

> **类比**：把两本书的章节交叉排成一本新书。暴力方法相当于把所有可能的章节排列组合都写出来，然后挑出最“好看的”那本。

这个方法 **一定能得到正确答案**，因为它遍历了所有合法的合并方式，最大者必然在其中。

但是，它的时间复杂度极高：  
- 两个长度分别为 `n`、`m` 的字符串，一共要做 `C_{n+m}^{n}`（组合数）种取法，随着 `n,m` 增大呈指数增长。  
- 即使我们用递归/回溯实现，最坏情况下也会遍历所有分支，根本不可能在 3000 长度的限制下跑完。

#### 代码（Python）

```python
from functools import lru_cache

def largestMerge_bruteforce(word1: str, word2: str) -> str:
    """暴力递归：尝试所有取字符的顺序，返回字典序最大的合并串"""
    @lru_cache(None)                     # 记忆化搜索，避免重复计算子问题
    def dfs(i: int, j: int) -> str:      # i、j 分别是 word1、word2 已经取走的字符数
        # 两个字符串都已经取完，返回空串
        if i == len(word1) and j == len(word2):
            return ""
        candidates = []
        # 若 word1 还有剩余，可以取下一个字符
        if i < len(word1):
            candidates.append(word1[i] + dfs(i + 1, j))
        # 若 word2 还有剩余，也可以取下一个字符
        if j < len(word2):
            candidates.append(word2[j] + dfs(i, j + 1))
        # 在所有可能的结果中挑出字典序最大的那个
        return max(candidates)

    return dfs(0, 0)

# 示例（仅用于演示，实际 3000 长度会超时）
print(largestMerge_bruteforce("cabaa", "bcaaa"))
```

> **关键行注释**  
> - `@lru_cache(None)`：把已经算过的 `(i,j)` 状态记下来，避免指数级递归。  
> - `candidates.append(word1[i] + dfs(i+1, j))`：把当前字符放到结果最前面，再递归处理剩余部分。  
> - `max(candidates)`：Python 的字符串比较天然是字典序比较，直接取最大即可。

#### 复杂度  

- **时间复杂度**：`O( C_{n+m}^{n} )`（组合数），即指数级别。  
  - 用大白话说，就是“几乎每一步都要分叉”，随着字符串长度稍微大一点，计算时间就会像滚雪球一样快速增长，根本不可接受。  
- **空间复杂度**：`O(n+m)` 用于递归栈 + 记忆化表（最多 `n*m` 条记录），在最坏情况下也会占用大量内存。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到：**每一步我们只需要决定从哪条字符串取字符**，而不必考虑后面所有的取法。  
如果我们能在每一步都做出“最优的局部选择”，并且这个局部最优能保证全局最优（贪心），就能把时间降到线性。

**关键观察**  

1. **如果当前两个字符不相等**，显然应该取较大的那个字符。  
   - 例如 `word1[i] = 'c'`，`word2[j] = 'b'`，把 `'c'` 放在前面一定能让结果字典序更大，因为字典序比较是从左到右的，先出现的大字符会主导比较结果。  

2. **如果当前两个字符相等**，仅凭这一个字符无法决定。我们需要比较**后面的子串**（即从 `i`、`j` 开始的剩余部分）。  
   - 把剩余子串看作两本“待阅读的书”。我们要决定先读哪本，取决于哪本的**后续内容更大**。  
   - 于是可以把问题转化为比较 `word1[i:]` 与 `word2[j:]` 的字典序大小。  

3. **比较子串的实现**  
   - 直接用 Python 的切片比较 `word1[i:] > word2[j:]`，因为字符串比较本身就是字典序比较。  
   - 这一步的时间复杂度是 **O(k)**，其中 `k` 是两子串第一次不同的位置。但在整体算法里，这种比较最多只会进行 **O(n+m)** 次，因为每次比较后至少会移动一个指针，使得已经比较过的字符不再参与后续比较。  

**贪心算法**  

- 用两个指针 `i`、`j` 分别指向 `word1`、`word2` 当前未取字符的位置。  
- 当任一指针未到字符串末尾时：  
  - 若 `word1[i] > word2[j]` → 把 `word1[i]` 加入结果，`i++`。  
  - 若 `word1[i] < word2[j]` → 把 `word2[j]` 加入结果，`j++`。  
  - 若相等 → 比较 `word1[i:]` 与 `word2[j:]` 的整体大小，较大的那一侧取字符。  
- 最后把剩余的字符直接拼接到结果后面即可。  

> **类比**：想象两条河流分别流出不同颜色的灯笼，灯笼从上游依次漂来。我们每次都挑“颜色更亮”（字典序更大）的灯笼放进展示柜；如果颜色相同，就往后看哪条河流后面会出现更亮的灯笼，再决定取哪条河流的当前灯笼。

#### 代码（Python）

```python
def largestMerge(word1: str, word2: str) -> str:
    """贪心双指针实现：一次遍历 O(n+m) 即可得到字典序最大的合并串"""
    i, j = 0, 0               # 分别指向 word1、word2 当前未使用的字符
    merge = []                # 使用列表收集字符，最后 join 成字符串，效率更高

    while i < len(word1) and j < len(word2):
        # 当前字符不相等时，直接取较大的那个
        if word1[i] > word2[j]:
            merge.append(word1[i])
            i += 1
        elif word1[i] < word2[j]:
            merge.append(word2[j])
            j += 1
        else:  # 当前字符相等，需要比较剩余子串的字典序
            # word1[i:] 与 word2[j:] 的比较是 O(k)（k 为首次不同的位置）
            if word1[i:] > word2[j:]:
                merge.append(word1[i])
                i += 1
            else:
                merge.append(word2[j])
                j += 1

    # 其中一个字符串已经全部取完，直接把剩余部分接在后面
    merge.append(word1[i:])   # 若 i 已到末尾，这一步等价于空串
    merge.append(word2[j:])   # 同理

    return ''.join(merge)     # 把列表合并成最终字符串

# ---- 示例 ----
print(largestMerge("cabaa", "bcaaa"))   # 输出: cbcabaaaaa
print(largestMerge("abcabc", "abdcaba"))# 输出: abdcabcabcaba
```

> **关键行注释**  
> - `while i < len(word1) and j < len(word2):`：只要两边都有字符就继续比较。  
> - `if word1[i:] > word2[j:]:`：比较从当前位置到结尾的子串大小，决定“取哪条河流的灯笼”。  
> - `merge.append(word1[i:])`、`merge.append(word2[j:])`：把剩余的整段一次性加入，避免额外的循环。

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 每一步指针至少前进一次，总共最多移动 `n+m` 步。  
  - 字符串切片比较 `word1[i:] > word2[j:]` 在最坏情况下会遍历相同前缀，但每个字符只会被比较一次（因为比较后对应指针会向后移动），所以整体仍是线性。  
- **空间复杂度**：`O(n + m)` 用于存放结果 `merge`（必须要有），额外的辅助空间只有常数级别（指针、临时变量）。

---

## 心得  

- **核心技巧**：**贪心 + 双指针 + 子串字典序比较**。  
- **适用的题型**：  
  1. “构造字典序最大/最小的字符串” 系列（如 LeetCode 1793 *Maximum Score of a Node* 中的类似思路）。  
  2. 两个序列合并、交叉拼接类问题（如 “最小字典序合并”）。  
  3. 需要在每一步做“先手决定”的游戏类问题（如 “石子游戏” 的贪心版本）。  
- **一句话总结**：**每一步都取当前可以放的最大字符；若相等就比较剩余子串的大小，决定从哪条“河流”继续取**。

---

## 反思  

- **第一反应**：直接想到递归/回溯遍历所有可能，没意识到可以用局部比较来直接决定。  
- **最容易踩的坑**：  
  - 当字符相等时忘记比较后续子串，导致得到的合并不是字典序最大的。  
  - 在实现时使用 `word1[i:] >= word2[j:]` 时要注意等号的处理：如果两子串完全相同，取任意一侧都可以，但保持代码一致性更好。  
  - 大量使用 `+` 拼接字符串会导致 **O(n²)** 的时间开销，应该改用列表 `append` 再一次性 `join`。  
- **下次遇到同类题**：**先检查“局部最大字符是否唯一”，若不唯一则把视野扩大到后面的子串比较**，这一步往往就是解题的关键。