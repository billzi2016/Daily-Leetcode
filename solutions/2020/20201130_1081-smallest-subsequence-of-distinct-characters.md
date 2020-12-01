# #1081. 不同字符的最小子序列 / Smallest Subsequence of Distinct Characters

> 难度：中等 · 标签：String、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/)

---

## 题目（英文原版）

**Description**

Given a string s, return the lexicographically smallest subsequence of s that contains all the distinct characters of s exactly once.

**Examples**

**Example 1:**

```
Input: s = "bcabc"
Output: "abc"
```

**Example 2:**

```
Input: s = "cbacdcbc"
Output: "acdb"
```

**Constraints**

- 1 <= s.length <= 1000
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，返回 `s` 中包含所有不同字符且每个字符恰好出现一次的词典序最小的子序列（subsequence）。

**示例 1**  
输入: `s = "bcabc"`  
输出: `"abc"`

**示例 2**  
输入: `s = "cbacdcbc"`  
输出: `"acdb"`

**约束条件**  
- `1 <= s.length <= 1000`  
- `s` 只由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串 `s` 的所有**子序列**都枚举出来，挑出满足下面两个条件的子序列：

1. 只出现一次的字符集合正好是 `s` 中出现的所有不同字符（即每个字符出现 **恰好一次**）。
2. 在所有满足条件的子序列里，字典序（lexicographically）最小的那个就是答案。

> **子序列**可以类比为“从一串珠子中挑选若干颗，挑选的顺序必须保持原来的先后”。  
> **字典序最小**就像在字典里查单词，先比较第一个字母，谁更靠前就更小；如果第一个相同，再比较第二个，以此类推。

实现时可以用 **位掩码**（bit‑mask）或 `set` 来记录已经挑选的字符集合，用 **递归**或**二进制枚举**遍历所有子序列。

因为要遍历 **所有子序列**，而一个长度为 `n` 的字符串有 `2ⁿ` 种子序列（每个字符保留或丢弃），所以时间会非常大。

#### 代码（Python）

```python
from itertools import combinations

def smallestSubsequence_bruteforce(s: str) -> str:
    # 所有不同字符的集合（目标集合）
    distinct = set(s)

    best = None                     # 保存目前找到的最小字典序子序列

    # 用二进制枚举所有子序列（这里用 combinations 只演示思路，实际仍是指数级）
    for r in range(len(distinct), len(s) + 1):      # 子序列长度至少要等于不同字符数
        for idxs in combinations(range(len(s)), r):
            subseq = ''.join(s[i] for i in idxs)    # 按原顺序拼接得到子序列
            if set(subseq) == distinct and len(subseq) == len(distinct):
                # 只保留恰好出现一次的情况
                if best is None or subseq < best:  # 比较字典序
                    best = subseq
    return best
```

> **关键行解释**  
> - `distinct = set(s)`：把字符串里出现的不同字符收集起来，就像把字典里所有词的“页码”记下来。  
> - `combinations(range(len(s)), r)`：枚举所有长度为 `r` 的下标组合，相当于把珠子挑选出来的所有方式。  
> - `if set(subseq) == distinct and len(subseq) == len(distinct)`：确保每个字符只出现一次。  

#### 复杂度

- **时间复杂度**：`O(2ⁿ)`（指数级）  
  这里的 `2ⁿ` 代表“所有子序列的数量”。比如 `n=20` 时，子序列已经有 **1,048,576** 种，远远超出实际可接受的范围。  
- **空间复杂度**：`O(n)`（递归/组合过程中保存下标列表）  
  只需要额外保存当前子序列的字符或下标，最多 `n` 个。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **遍历所有子序列**。我们其实不需要穷举，只要在遍历原字符串一次的过程中，**贪心**地决定每个字符是否应该加入答案，并且保持答案的字典序最小。

核心观察：

1. **每个字符只出现一次**，所以我们只需要把每个不同字符挑选一次，顺序要尽量小。
2. 对于字符 `c`，如果它后面还有出现的机会（即 **还有未遍历的 `c`**），我们可以暂时把它“踢出”答案，让更小的字符提前进入。
3. 为了快速判断“后面还有没有 `c`”，只需要预先记录每个字符最后一次出现的位置 `last_pos[char]`。
4. 为了在构造答案时能够**弹出**已经放进答案但后面还能重新加入的字符，使用 **单调递增栈**（Monotonic Stack）非常合适。栈顶保持的是当前答案的最后一个字符，栈内字符从下到上字典序递增。

具体步骤：

- **统计每个字符的最后出现下标** `last`.  
  这相当于“这颗珠子最后一次出现在哪儿”，如果我们已经把它丢掉，后面还能再捡到。
- **遍历字符串**，维护两个集合：  
  - `in_stack`（已在答案栈中）相当于“已经放进篮子里的珠子”。  
  - `stack` 本身保存答案的字符顺序。
- 对每个字符 `c`：
  1. 如果 `c` 已经在 `stack` 中，直接跳过（因为我们只能出现一次）。
  2. 否则，**尝试弹出**栈顶字符 `top`，只要满足两个条件就弹出：
     - `top > c`（`c` 更小，想让它排在前面，类似把大字母换成小字母）。
     - `i < last[top]`（栈顶字符在后面还有出现的机会，弹出去后还能再补回来）。
  3. 将 `c` 推入栈，并标记 `in_stack[c] = True`。

遍历结束后，栈中字符的顺序就是字典序最小且包含所有不同字符一次的子序列。

> **类比**：把栈想象成一个“可变的排队队伍”。如果前面的小朋友（字符）比后面的大朋友更想排在前面，而且大朋友还有机会再来排队，我们就让大朋友先让位（弹出），让小朋友先进入。

#### 代码（Python）

```python
def smallestSubsequence(s: str) -> str:
    """
    使用单调栈的贪心算法，时间 O(n)，空间 O(1)（因为字符集合只有 26 种）。
    """
    # 1. 记录每个字符最后出现的位置
    last = {ch: i for i, ch in enumerate(s)}   # 例：{'b':4, 'c':5, 'a':2}
    
    stack = []               # 单调递增栈，保存答案字符
    in_stack = set()         # 记录字符是否已经在栈中

    # 2. 依次遍历每个字符
    for i, ch in enumerate(s):
        # 已经在答案里就跳过
        if ch in in_stack:
            continue

        # 3. 尝试弹出栈顶，使答案字典序更小
        while stack and ch < stack[-1] and i < last[stack[-1]]:
            removed = stack.pop()          # 弹出
            in_stack.remove(removed)       # 同步更新集合
            # 这里可以想象把“大朋友”让回了原来的位置

        # 4. 将当前字符压入栈
        stack.append(ch)
        in_stack.add(ch)

    # 栈中字符即为所求子序列
    return ''.join(stack)
```

> **关键行解释**  
> - `last = {ch: i for i, ch in enumerate(s)}`：记录每个字符**最后一次**出现的下标，等价于“这颗珠子最后一次出现的时间”。  
> - `while stack and ch < stack[-1] and i < last[stack[-1]]:`：只要栈顶字符比当前字符大且后面还能再出现，就把它弹出来，让更小的字符抢前排。  
> - `in_stack` 用来**快速判断**字符是否已经在答案里，避免重复加入。

#### 复杂度

- **时间复杂度**：`O(n)`（线性）  
  每个字符最多被压入栈一次、弹出栈一次，整个过程相当于遍历两遍字符串。相比暴力的 `2ⁿ`，这就像把“所有可能的排列”压缩成“一趟扫荡”。  
- **空间复杂度**：`O(1)`（常数）  
  额外使用的空间只和字符种类有关（这里是 26 个小写英文字母），与字符串长度 `n` 无关。

---

## 心得

- **核心技巧**：**单调栈 + 贪心**，通过“只要后面还能补回来，就把大字符让位给更小字符”。  
- **适用题型**：  
  1. `Remove Duplicate Letters`（LeetCode 316）——本题的变形。  
  2. `Monotone Increasing Subsequence`（类似的单调栈题目）。  
  3. `Lexicographically Smallest Subsequence`（需要保持相对顺序的字典序最小化）。  
- **一句话总结**：**“只要后面还能补齐，就把当前的‘大’字符弹出，让更小的字符抢先”。**

---

## 反思

- **第一反应**：直接想到枚举所有子序列，然后筛选——这是一种“先把所有可能列出来再挑选”的直觉。  
- **最容易踩的坑**：  
  - 忘记记录每个字符的 **最后出现位置**，导致弹出后再也找不到该字符。  
  - 没有使用 `in_stack` 判断字符是否已在答案中，导致同一个字符被多次加入，破坏“一次出现”要求。  
  - 对于只出现一次的字符，弹出条件必须严格检查 `i < last[top]`，否则会把它提前弹出导致缺失。  
- **下次遇到同类题**：第一步先 **统计每个字符的出现次数或最后位置**，再决定是否可以“让位”。这一步往往决定能否使用单调栈的贪心策略。