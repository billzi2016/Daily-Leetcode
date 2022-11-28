# #2030. 字母出现次数限制的最小 K 长度子序列 / Smallest K-Length Subsequence With Occurrences of a Letter

> 难度：困难 · 标签：String、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/smallest-k-length-subsequence-with-occurrences-of-a-letter/)

---

## 题目（英文原版）

**Description**

You are given a string s, an integer k, a letter letter, and an integer repetition.
Return the lexicographically smallest subsequence of s of length k that has the letter letter appear at least repetition times. The test cases are generated so that the letter appears in s at least repetition times.
A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.
A string a is lexicographically smaller than a string b if in the first position where a and b differ, string a has a letter that appears earlier in the alphabet than the corresponding letter in b.

**Examples**

**Example 1:**

```
Input: s = "leet", k = 3, letter = "e", repetition = 1
Output: "eet"
Explanation: There are four subsequences of length 3 that have the letter 'e' appear at least 1 time:
- "lee" (from "leet")
- "let" (from "leet")
- "let" (from "leet")
- "eet" (from "leet")
The lexicographically smallest subsequence among them is "eet".
```

**Example 2:**

```
Input: s = "leetcode", k = 4, letter = "e", repetition = 2
Output: "ecde"
Explanation: "ecde" is the lexicographically smallest subsequence of length 4 that has the letter "e" appear at least 2 times.
```

**Example 3:**

```
Input: s = "bb", k = 2, letter = "b", repetition = 2
Output: "bb"
Explanation: "bb" is the only subsequence of length 2 that has the letter "b" appear at least 2 times.
```

**Constraints**

- 1 <= repetition <= k <= s.length <= 5 * 104
- s consists of lowercase English letters.
- letter is a lowercase English letter, and appears in s at least repetition times.

---

## 题目（中文翻译）

给定一个字符串 `s`、整数 `k`、字符 `letter`，以及整数 `repetition`。返回 `s` 中长度为 `k`、且字符 `letter` 至少出现 `repetition` 次的字典序最小的子序列（subsequence）。测试用例保证 `letter` 在 `s` 中出现次数不少于 `repetition`。

**子序列** 是指可以通过删除原字符串中的若干字符（也可以不删）得到的字符串，且剩余字符的相对顺序保持不变。

如果在第一个不同的位置，字符串 `a` 的字符在字母表中的顺序早于字符串 `b` 的对应字符，则称 `a` 的字典序小于 `b`。

### 示例

#### 示例 1
> **输入**: `s = "leet", k = 3, letter = "e", repetition = 1`  
> **输出**: `"eet"`  
> **解释**: 长度为 3 且字符 `'e'` 至少出现 1 次的子序列有四个：  
> - `"lee"`（来源于 `"leet"`）  
> - `"let"`（来源于 `"leet"`）  
> - `"let"`（来源于 `"leet"`）  
> - `"eet"`（来源于 `"leet"`）  
> 其中字典序最小的是 `"eet"`。

#### 示例 2
> **输入**: `s = "leetcode", k = 4, letter = "e", repetition = 2`  
> **输出**: `"ecde"`  
> **解释**: `"ecde"` 是长度为 4 且字符 `"e"` 至少出现 2 次的子序列中字典序最小的。

#### 示例 3
> **输入**: `s = "bb", k = 2, letter = "b", repetition = 2`  
> **输出**: `"bb"`  
> **解释**: `"bb"` 是唯一满足长度为 2 且字符 `"b"` 至少出现 2 次的子序列。

### 约束条件
- `1 <= repetition <= k <= s.length <= 5 * 10^4`
- `s` 仅由小写英文字母组成。
- `letter` 为小写英文字母，且在 `s` 中出现次数不少于 `repetition`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的**子序列**枚举出来，筛掉长度不是 `k` 或者字母 `letter` 出现次数不足 `repetition` 的，然后在剩下的序列中挑最小的（字典序最靠前的）。

- **子序列**：可以把原字符串想成一排书，选几本书出来保持原来的顺序，这就是子序列。  
- **枚举**：把每个字符都决定“要”或“不要”，相当于二进制的 0/1 选择，总共有 `2^n` 种（`n = len(s)`），显然会爆炸。  

虽然这种方法在概念上最简单，却完全不可行。它之所以**正确**是因为我们遍历了所有合法的子序列，必然会找到字典序最小的那个。但时间上会非常慢。

#### 代码（Python）

```python
import itertools

def smallestSubsequence_bruteforce(s: str, k: int, letter: str, repetition: int) -> str:
    n = len(s)
    best = None                     # 用来保存当前最小的合法序列
    # 产生所有长度为 k 的下标组合
    for idxs in itertools.combinations(range(n), k):
        # 取出对应的字符形成子序列
        sub = ''.join(s[i] for i in idxs)
        # 检查 letter 出现次数是否满足要求
        if sub.count(letter) >= repetition:
            if best is None or sub < best:   # 字典序比较
                best = sub
    return best
```

> **提示**：以上代码只能在非常小的输入（比如 `len(s) ≤ 10`）上跑通，真实数据会直接超时。

#### 复杂度  

- **时间复杂度**：`O(C(n, k) * k)`  
  - `C(n, k)` 是组合数，表示有多少种挑 `k` 个位置的方式，约等于 `n! / (k! (n‑k)!)`。即使 `k` 很小，组合数也会指数级增长。  
  - 对每个组合我们还要拼接字符串并统计 `letter`，这一步是 `O(k)`。  
  - 用大白话说，这种复杂度相当于“尝试所有可能的选法”，根本不可接受。

- **空间复杂度**：`O(k)`  
  - 只保存当前正在检查的子序列和最好的答案，最多 `k` 长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**不停地回溯、重新检查**。我们其实只需要**一次遍历**，并在遍历过程中随时决定保留还是丢弃当前字符，使得最终得到的序列既满足长度 `k`、字母出现次数 `repetition`，又是字典序最小的。  

这类“在遍历中维护最优序列”的问题，常用 **单调栈（Monotonic Stack）** + **贪心** 的思路。下面一步步推导：

1. **我们想要的序列长度是 `k`**，所以在遍历完所有字符后，栈（或列表）里应该恰好有 `k` 个字符。  
2. **字母 `letter` 必须出现至少 `repetition` 次**。设 `need = repetition` 为还需要补齐的 `letter` 个数。  
3. **剩余字符的可用数量**：在遍历时，记住从当前位置到字符串结尾还有多少个 `letter`，以及还有多少个总字符可以选（即 `remaining = len(s) - i`）。这帮助我们判断“即使把栈顶的字符弹掉，后面还能补足需求吗？”  
4. **贪心原则**：如果当前字符 `c` 小于栈顶字符 `stack[-1]`，并且弹掉栈顶后仍然可以在后面补足**总长度**和**letter 出现次数**，我们就把栈顶弹掉。这样可以让左边的字符尽可能小，得到更小的字典序。  
5. **特殊处理 `letter`**：  
   - 当栈顶是 `letter` 时，如果弹掉后导致 `need` 变大（因为少了一个必需的字母），我们必须确认后面还有足够的 `letter` 可以补回。  
   - 当当前字符是 `letter` 时，即使它比栈顶大，也要尽可能保留，以免后面找不到足够的 `letter`。  

实现细节：

- 用 `cnt_letter` 记录从当前位置到末尾还有多少个 `letter`（可以在一次遍历前先统计总数，然后在遍历时递减）。  
- 用 `stack` 存放已经确定的字符。  
- 用 `need` 记录还需要多少个 `letter` 才能满足 `repetition`。  
- 每次决定是否 **push** 当前字符之前，先尝试 **pop** 栈顶满足上述条件。  

下面用生活化的类比帮助理解：

> 想象你在排队买票，每个人手里都有一张卡片（字符）。你希望最后手里留下恰好 `k` 张卡片，且其中至少有 `repetition` 张是特定颜色的 `letter`。排队时，你可以把已经拿到的卡片放回队尾（相当于 `pop`），前提是后面还有足够的卡片可以再拿到，且不会让你最终缺少必需的颜色。这样，你总是把“更小的字母”留在手里，从而得到字典序最小的组合。

#### 代码（Python）

```python
def smallestSubsequence(s: str, k: int, letter: str, repetition: int) -> str:
    n = len(s)
    # 统计从左到右遍历时，后面还能看到多少个 letter
    total_letter = s.count(letter)          # 整个字符串里 letter 的总数
    need = repetition                       # 还需要多少个 letter 才能满足要求
    stack = []                               # 单调栈，保存已经选好的字符
    # 已经遍历过的字符数
    used = 0                                 # stack 的当前长度

    for i, ch in enumerate(s):
        # 当前位置后面还能剩下多少字符可以使用
        remain = n - i - 1                     # 不包括当前字符

        # 如果当前字符是 letter，后面的 total_letter 要减 1（因为我们正在处理它）
        if ch == letter:
            total_letter -= 1

        # 只要栈不空，并且栈顶字符比当前字符大，
        # 且弹掉栈顶后仍然能保证最终长度和 letter 的需求，就弹掉
        while stack:
            top = stack[-1]
            # 判断弹掉后还能否满足总长度 k
            #   已经选的字符数 - 1 + 剩余未遍历字符数 + 1（当前字符） >= k
            #   这里 +1 是因为我们准备把当前字符放进去
            can_fill_len = (used - 1) + remain + 1 >= k

            # 判断弹掉后还能否满足 letter 的需求
            #   如果栈顶是 letter，则弹掉会让 need 增加 1
            #   需要确保后面还有足够的 letter（total_letter）来补足
            if top == letter:
                can_fill_letter = (need + 1) <= total_letter
            else:
                # 栈顶不是必需的 letter，弹掉不影响 need
                can_fill_letter = True

            # 同时满足两个条件才可以弹掉
            if top > ch and can_fill_len and can_fill_letter:
                popped = stack.pop()
                used -= 1
                if popped == letter:
                    need += 1          # 因为弹掉了一个必需的 letter
            else:
                break

        # 决定是否把当前字符加入栈中
        # 1) 仍然需要更多的字符才能凑够 k
        # 2) 或者当前字符是 letter（因为我们必须保证 enough letter）
        # 3) 或者当前字符比栈顶大（此时保留当前字符不会破坏字典序）
        if used < k:
            # 只有在必须保留 letter 时才强制加入
            if ch == letter:
                stack.append(ch)
                used += 1
                need = max(need - 1, 0)   # 已经补齐一个 letter
            else:
                # 若当前字符不是 letter，但我们仍有空间，并且
                # 还需要的 letter 数量已经可以在后面补齐，就可以加入
                if need <= total_letter:   # 仍有足够的 letter 供后面使用
                    stack.append(ch)
                    used += 1
                # 否则直接跳过，等后面的 letter 来补齐
        # 如果已经满了 k，直接跳过后面的字符

    # 栈可能会比 k 长（因为在某些情况下我们多加了字符），只取前 k 个
    return ''.join(stack[:k])
```

> **代码说明**（关键行中文注释）  
> - `total_letter`：记录**剩余**可以使用的 `letter` 数量。遍历时递减。  
> - `need`：还缺多少个 `letter` 才能满足 `repetition`。弹栈时若弹掉了 `letter`，`need` 加一；压栈 `letter` 时，`need` 减一。  
> - `can_fill_len`：弹栈后，**剩余字符 + 已选字符** 是否仍能凑够 `k`。  
> - `can_fill_letter`：弹栈后，**剩余的 `letter`** 是否足够补足 `need`。  
> - `while` 循环实现**单调栈**：只要栈顶比当前字符大且不会破坏约束，就弹掉栈顶，让更小的字符尽早进入答案。  
> - 最后 `stack[:k]` 防止因某些边界情况导致栈稍长，截取前 `k` 即为答案。

#### 复杂度  

- **时间复杂度**：`O(n)`（其中 `n = len(s)`）  
  - 每个字符最多被压栈一次、弹栈一次，整个过程是线性的。  
  - 与暴力解的指数级 `C(n, k)` 相比，快了几个数量级。  
  - 用大白话说，就是“只走一遍字符串”，即使 `n` 达到 5×10⁴ 也能轻松跑完。

- **空间复杂度**：`O(k)`  
  - 栈中最多保存 `k` 个字符（答案的长度），其余变量都是常数级。  
  - 相比暴力解的组合数空间，这已经是最小的了。

---

## 心得

- **核心技巧**：**单调栈 + 贪心**，在遍历时维护一个“尽可能小且合法”的前缀序列。  
- **适用的题型**  
  1. “字典序最小的子序列/子数组” 例如 LeetCode 1081 *Smallest Subsequence of Distinct Characters*。  
  2. “长度受限的最小/最大子序列” 如 316 *Remove Duplicate Letters*（需要去重），以及 402 *Remove K Digits*（数字版）。  
- **解题钥匙**：**只要在保证还能完成目标的前提下，尽可能把“更大的”字符弹掉**。

---

## 反思

- **第一反应**：先想到枚举所有子序列，感觉思路最直观，却忽视了数据规模。  
- **最容易踩的坑**  
  - **统计剩余 `letter`**：忘记在遍历时实时更新会导致误判能否弹栈。  
  - **边界条件**：`need` 可能为 0（已经满足要求），但仍需要保证后面还有足够的字符凑满 `k`。  
  - **栈可能超长**：在某些实现里会在 `used == k` 时仍继续压入，需要在最后截断。  
- **下次类似题**：第一步先**明确约束**（长度、必需字符数量），再**思考能否用单调栈在一次遍历中同时满足约束并保持字典序最小**。如果能做到，基本就找到了最优解的方向。