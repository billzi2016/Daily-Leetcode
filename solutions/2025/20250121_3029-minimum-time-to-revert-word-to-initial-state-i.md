# #3029. 将单词恢复到初始状态的最小时间 I / Minimum Time to Revert Word to Initial State I

> 难度：中等 · 标签：String、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-revert-word-to-initial-state-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string word and an integer k.
At every second, you must perform the following operations:
Note that you do not necessarily need to add the same characters that you removed. However, you must perform both operations at every second.
Return the minimum time greater than zero required for word to revert to its initial state.

**Examples**

**Example 1:**

```
Input: word = "abacaba", k = 3
Output: 2
Explanation: At the 1st second, we remove characters "aba" from the prefix of word, and add characters "bac" to the end of word. Thus, word becomes equal to "cababac".
At the 2nd second, we remove characters "cab" from the prefix of word, and add "aba" to the end of word. Thus, word becomes equal to "abacaba" and reverts to its initial state.
It can be shown that 2 seconds is the minimum time greater than zero required for word to revert to its initial state.
```

**Example 2:**

```
Input: word = "abacaba", k = 4
Output: 1
Explanation: At the 1st second, we remove characters "abac" from the prefix of word, and add characters "caba" to the end of word. Thus, word becomes equal to "abacaba" and reverts to its initial state.
It can be shown that 1 second is the minimum time greater than zero required for word to revert to its initial state.
```

**Example 3:**

```
Input: word = "abcbabcd", k = 2
Output: 4
Explanation: At every second, we will remove the first 2 characters of word, and add the same characters to the end of word.
After 4 seconds, word becomes equal to "abcbabcd" and reverts to its initial state.
It can be shown that 4 seconds is the minimum time greater than zero required for word to revert to its initial state.
```

**Constraints**

- 1 <= word.length <= 50
- 1 <= k <= word.length
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个下标从 0 开始的字符串 `word` 和一个整数 `k`。  
每秒，你必须执行以下操作：  
（题目原文中此处应列出具体的两步操作，保持原样）  

需要注意的是，你加入的字符 **不一定** 要和删除的字符相同，但每秒必须同时完成这两个操作。  
返回使 `word` 恢复到初始状态所需的最小正整数时间。

### 示例

#### 示例 1
```
Input: word = "abacaba", k = 3
Output: 2
```
**解释**：第 1 秒，删除单词前缀 `aba`（前缀 (prefix)），并在单词末尾添加字符 `bac`，此时 `word` 变为 `cababac`。  
第 2 秒，删除前缀 `cab`，并在末尾添加 `aba`，此时 `word` 重新变为 `abacaba`，即恢复到初始状态。

#### 示例 2
```
Input: word = "abacaba", k = 4
Output: 1
```
**解释**：第 1 秒，删除前缀 `abac`，并在末尾添加 `caba`，此时 `word` 立即变为 `abacaba`，恢复到初始状态。  
可以证明，1 秒是使 `word` 恢复到初始状态所需的最小正整数时间。

#### 示例 3
```
Input: word = "abcbabcd", k = 2
Output: 4
```
**解释**：每秒都删除 `word` 的前 2 个字符，并将相同的字符添加到末尾。  
经过 4 秒后，`word` 再次等于 `abcbabcd`，恢复到初始状态。  
可以证明，4 秒是使 `word` 恢复到初始状态所需的最小正整数时间。

### 约束条件
- `1 <= word.length <= 50`
- `1 <= k <= word.length`
- `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**直接模拟**题目描述的每一秒钟的操作，然后检查多少秒后字符串会恢复成原来的样子。

模拟的步骤：

1. 记录当前字符串 `cur`（一开始等于 `word`）。
2. 第 `t` 秒：  
   - 把 `cur` 的前 `k` 个字符删掉。  
   - 随意往 `cur` 末尾再加上 `k` 个字符（因为我们可以自己决定，加上什么字符都行）。  
   - 为了让最后能够回到原始状态，我们把这一步要“补回”的字符设成 **原字符串中被删掉的那段**（这显然是最有利的选择）。
3. 经过一次操作后得到新的 `cur`，继续下一秒。  
4. 每一次操作后检查 `cur` 是否已经等于 `word`，如果相等就返回当前的秒数 `t`。

因为 `word` 最长只有 `50`，我们可以把 **所有可能的秒数 `t = 1 … n`（`n = len(word)`）** 都枚举一遍，只要找到第一 个满足条件的 `t` 即可。

> **为什么这样一定能找到答案？**  
> 每一次我们都把被删掉的前 `k` 个字符原封不动地放到字符串的末尾。这样相当于把原字符串 **循环左移** `k` 位，然后再把左移后产生的缺口用原来被删掉的字符填补。只要经过若干次循环后，左移的总位数恰好使得 **剩余的原始前缀** 与 **已经拼好的后缀** 完全匹配，整个字符串就会恢复原样。遍历所有 `t` 能保证不漏掉任何可能的匹配。

#### 代码（Python）

```python
def minimumTime_bruteforce(word: str, k: int) -> int:
    n = len(word)
    # 枚举可能的秒数 t（最多 n 次就会把所有字符都搬走一次）
    for t in range(1, n + 1):
        shift = (t * k) % n               # 实际左移的位数（循环移位）
        # 剩下的原始部分是 word[shift:]，它的长度是 n - shift
        # 要想恢复，需要这段剩余部分恰好等于 word 的前缀
        if word[shift:] == word[:n - shift]:
            return t
    # 按理说一定会在上面返回，这里只是防止 IDE 报错
    return n
```

> **关键行解释**  
> - `shift = (t * k) % n`：`t` 秒后，原字符串整体左移了多少位（循环移位）。  
> - `word[shift:] == word[:n - shift]`：检查左移后留下的“未被搬走的”那段是否正好等于原字符串的前缀。如果相等，说明把搬走的字符依次补回后就能得到原串。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层枚举 `t` 最多 `n` 次，内层比较两个子串的长度最多 `n`，所以最坏情况是 `n·n`。  
  - 这里的 `n ≤ 50`，所以 `2500` 次比较在实际运行中几乎可以忽略不计。  
- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量，未使用额外的随 `n` 增长的数据结构。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要把整个字符串切片比较**，时间是 `O(n²)`。  
我们可以把问题抽象成**数学等式**，利用**前缀‑后缀相同的长度（border）**以及**模运算**来一次性算出答案。

---

#### 2.1 把问题写成等式

设 `n = len(word)`，`t` 为答案（需要的秒数），`k` 为每秒搬走的字符数。

- 第 `t` 秒后，原字符串整体左移了 `d = (t·k) mod n` 位（循环左移）。
- 左移后**仍然保留下来的原始部分**是 `word[d:]`，长度是 `n-d`。
- 为了让最终字符串等于原始字符串，**这段保留下来的部分必须恰好是原字符串的前缀**，即  

\[
\boxed{word[d:] = word[0:n-d]}
\]

这正是“**前缀 = 后缀**”的定义，长度为 `n-d` 的前后缀相等，我们把这种长度记作 **border**（边界）  
> **border**：既是前缀又是后缀的子串的长度（不包括整个字符串本身）。

于是我们得到两个条件：

1. `B = n - d` 必须是一个 border（`0 ≤ B ≤ n`）。  
2. `d = (t·k) mod n`，即 `t·k ≡ d (mod n)`。  
   把 `d` 用 `B` 表示：`d = n - B`，于是  

\[
t·k \equiv n - B \pmod{n}
\]

只要找到了满足上述同余式的最小正整数 `t`，答案就出来了。

---

#### 2.2 求所有 border 长度  

利用 **KMP（Knuth–Morris–Pratt）** 的前缀函数 `pi[i]` 可以在 `O(n)` 时间得到所有 border 长度。  
`pi[i]` 表示 `word[0..i]` 的最长 border 长度。  
从 `pi[n-1]` 开始不断向前追溯，就能得到 **所有**（从大到小）满足 `prefix == suffix` 的长度。

---

#### 2.3 解线性同余方程  

对每个 border 长度 `B`，我们要解

\[
t·k \equiv (n - B) \pmod{n}
\]

记 `g = gcd(k, n)`。如果 `(n-B) % g != 0`，则 **无解**（因为左边必然是 `g` 的倍数）。  
否则可以把方程化简：

\[
\begin{aligned}
k' &= k / g \\
n' &= n / g \\
c  &= (n - B) / g \\
t·k' &\equiv c \pmod{n'}
\end{aligned}
\]

此时 `k'` 与 `n'` **互质**，可以求出 `k'` 在模 `n'` 下的**逆元** `inv`（使用扩展欧几里得算法），得到最小解

\[
t_0 = (c·inv) \bmod n'
\]

如果 `t_0 == 0`（说明同余式的最小正解是 `n'`），我们取 `t = n'`。  
对所有 border 取最小的 `t` 即为答案。

---

#### 2.4 为什么最优解快？

- **只遍历所有 border**：最多 `n` 个，`n ≤ 50`，几乎可以忽略。  
- **每个 border 只做一次求逆**：扩展欧几里得的时间是 `O(log n)`。  
- 整体时间 `O(n + log n)`，空间 `O(n)`（存前缀函数），远快于 `O(n²)` 的暴力。

---

#### 代码（Python）

```python
from math import gcd
from typing import List

def get_borders(s: str) -> List[int]:
    """
    使用 KMP 前缀函数返回所有 border 长度（不包括整个字符串本身）。
    结果从大到小排列，方便后面直接遍历。
    """
    n = len(s)
    pi = [0] * n
    # 构造前缀函数
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j

    borders = []
    cur = pi[-1]               # 最长的 border 长度
    while cur > 0:
        borders.append(cur)
        cur = pi[cur - 1]       # 继续往短的 border 追溯
    borders.append(0)           # 空 border 也算（对应 d = n）
    borders.sort(reverse=True)  # 从大到小，便于后面直接取最小 t
    return borders

def mod_inverse(a: int, mod: int) -> int:
    """
    返回 a 在模 mod 下的逆元（a 与 mod 必须互质）。
    使用扩展欧几里得算法。
    """
    def egcd(x, y):
        if y == 0:
            return (1, 0, x)
        u, v, g = egcd(y, x % y)
        return (v, u - (x // y) * v, g)

    inv, _, g = egcd(a, mod)
    # 这里保证 g == 1
    return inv % mod

def minimumTime(word: str, k: int) -> int:
    n = len(word)
    borders = get_borders(word)          # 所有可能的 B

    best = float('inf')
    g = gcd(k, n)

    for B in borders:                    # 遍历每个 border 长度
        target = (n - B) % n              # d = n - B
        if target % g != 0:               # 同余式无解，直接跳过
            continue

        # 把方程化简
        k_ = k // g
        n_ = n // g
        c = target // g

        inv = mod_inverse(k_, n_)         # k_ 在模 n_ 下的逆元
        t0 = (c * inv) % n_                # 最小非负解

        t = t0 if t0 != 0 else n_          # 必须是正整数
        best = min(best, t)

    return best
```

> **代码要点注释**  
> - `get_borders`：利用 KMP 前缀函数一次遍历得到所有满足 `prefix == suffix` 的长度。  
> - `mod_inverse`：扩展欧几里得求逆元，时间 `O(log n)`。  
> - 主函数里：对每个 border `B` 先检查 `target % g == 0`（不可解的直接略过），再求最小正整数 `t`，最后取全局最小。

#### 复杂度  

- **时间复杂度**：`O(n + log n)`  
  - 前缀函数 `O(n)`（`n ≤ 50`）。  
  - 对每个 border（最多 `n` 个）求逆元 `O(log n)`。  
- **空间复杂度**：`O(n)`  
  - 存放前缀函数数组以及 border 列表。

---

## 心得

- **核心技巧**：把“每秒左移 `k` 位后仍然保留下来的那段要与原前缀相等”转化为 **前缀‑后缀相同的长度（border）** 与 **模线性同余方程** 的结合。  
- **适用场景**：  
  1. 需要判断字符串经过若干次“循环左移”后是否能恢复原样（如旋转字符串、循环队列）。  
  2. 需要在周期性操作中求最小步数，使得某种“对齐”条件成立（如密码锁转动、环形赛道的同步问题）。  
- **一句话总结**：**找出所有前后缀相同的长度，然后在这些长度上解最小的同余方程**，即可一次算出答案。

---

## 反思

- **拿到题目第一反应**：先想“把每秒的操作写成循环左移”，然后尝试**直接模拟**，因为字符串很短。  
- **最容易踩的坑**：  
  - 忘记 `t` 必须 **大于 0**（题目要求返回正整数），所以即使 `t = 0`（即不做任何操作）也不能返回。  
  - 在暴力实现里，`shift = (t*k) % n` 必须用取模，否则会越界。  
  - 解同余方程时忽视 `gcd(k, n)`，导致除不尽出现错误。  
- **下次类似题的第一步**：**把周期性操作抽象为“循环移位 + 边界匹配”**，先找出所有可能的匹配长度（border），再在这些长度上做模算术求最小步数。这样可以从 O(n²) 直接跳到 O(n)。