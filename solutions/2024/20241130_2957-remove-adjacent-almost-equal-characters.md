# #2957. 移除相邻近似相等字符 / Remove Adjacent Almost-Equal Characters

> 难度：中等 · 标签：String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/remove-adjacent-almost-equal-characters/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string word.
In one operation, you can pick any index i of word and change word[i] to any lowercase English letter.
Return the minimum number of operations needed to remove all adjacent almost-equal characters from word.
Two characters a and b are almost-equal if a == b or a and b are adjacent in the alphabet.

**Examples**

**Example 1:**

```
Input: word = "aaaaa"
Output: 2
Explanation: We can change word into "acaca" which does not have any adjacent almost-equal characters.
It can be shown that the minimum number of operations needed to remove all adjacent almost-equal characters from word is 2.
```

**Example 2:**

```
Input: word = "abddez"
Output: 2
Explanation: We can change word into "ybdoez" which does not have any adjacent almost-equal characters.
It can be shown that the minimum number of operations needed to remove all adjacent almost-equal characters from word is 2.
```

**Example 3:**

```
Input: word = "zyxyxyz"
Output: 3
Explanation: We can change word into "zaxaxaz" which does not have any adjacent almost-equal characters. 
It can be shown that the minimum number of operations needed to remove all adjacent almost-equal characters from word is 3.
```

**Constraints**

- 1 <= word.length <= 100
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的字符串 `word`。  
一次操作中，你可以选择 `word` 的任意下标 `i`，并将 `word[i]` 更改为任意小写英文字母（lowercase English letter）。  
返回使 `word` 中不存在相邻近似相等字符（adjacent almost-equal characters）所需的最少操作次数。

**定义**  
两个字符 `a` 和 `b` 若满足以下任意条件，则称它们**近似相等**（almost-equal）：
- `a == b`  
- `a` 与 `b` 在字母表中相邻（例如 `'a'` 与 `'b'`，`'c'` 与 `'b'` 等）。

**示例**

**示例 1**  
```
Input: word = "aaaaa"
Output: 2
Explanation: 我们可以把 word 改成 "acaca"，此时不存在任何相邻近似相等字符。
可以证明，消除所有相邻近似相等字符的最少操作次数为 2。
```

**示例 2**  
```
Input: word = "abddez"
Output: 2
Explanation: 我们可以把 word 改成 "ybdoez"，此时不存在任何相邻近似相等字符。
可以证明，消除所有相邻近似相等字符的最少操作次数为 2。
```

**示例 3**  
```
Input: word = "zyxyxyz"
Output: 3
Explanation: 我们可以把 word 改成 "zaxaxaz"，此时不存在任何相邻近似相等字符。
可以证明，消除所有相邻近似相等字符的最少操作次数为 3。
```

**约束条件**  
- `1 <= word.length <= 100`  
- `word` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个字符都列出来，尝试所有可能的改法**，然后找出改动最少的方案。  
- **数据结构**：我们可以把字符看成 0~25 的数字（`a` → 0，`b` → 1 …），这相当于把字母表装进了一个**数组**，就像查字典时把单词对应到页码一样。  
- **为什么正确**：只要把每个位置选成一个合法的字符（即与左边字符既不相同也不相邻），整个字符串就满足题目要求。遍历所有合法的选法，取最小的改动数，自然就是答案。  
- **复杂度分析**：  
  - 长度为 `n ≤ 100`，每个位置有 26 种可能的字符。若用最粗的枚举方式（`26ⁿ`），显然不可行。  
  - 为了把搜索空间压到可接受范围，我们用**动态规划**：`dp[i][c]` 表示把前 `i+1` 个字符处理好，并且第 `i` 位选成字符 `c`（0~25）时的最少改动次数。状态转移只需要看第 `i‑1` 位的字符 `p`，如果 `c` 与 `p` **不几乎相等**（即 `c != p` 且 `|c‑p| != 1`），就可以合法衔接。  
  - 对每个 `i`，我们要遍历所有 `c`（26 种），并在每个 `c` 中遍历所有合法的前驱 `p`（最多 26 种），所以总时间是 `O(n·26·26)`，约等于 `O( n )`（因为常数 26² 很小）。空间需要保存 `dp` 表，大小为 `n·26`，即 `O(n·26)`。

#### 代码（Python）

```python
from typing import List

def minOperations_bruteforce(word: str) -> int:
    n = len(word)
    # 把字符转成 0~25 的整数，方便比较
    a = [ord(ch) - ord('a') for ch in word]

    INF = 10 ** 9
    # dp[i][c] = 前 i+1 个字符处理完，i 位置为字符 c 时的最少改动次数
    dp: List[List[int]] = [[INF] * 26 for _ in range(n)]

    # 初始化：第 0 位可以任选字符 c
    for c in range(26):
        dp[0][c] = 0 if c == a[0] else 1   # 若和原字符相同则不需要改动

    # 状态转移
    for i in range(1, n):
        for cur in range(26):                 # 当前位选 cur
            cost_cur = 0 if cur == a[i] else 1   # 是否需要改动
            best = INF
            for pre in range(26):                 # 前一位是 pre
                # 判断 pre 与 cur 是否几乎相等
                if cur == pre or abs(cur - pre) == 1:
                    continue                    # 不能相邻
                best = min(best, dp[i-1][pre])
            dp[i][cur] = best + cost_cur

    # 最后一个字符可以是任意合法字符，取最小值即为答案
    return min(dp[-1])
```

#### 复杂度  

- **时间复杂度**：`O(n·26·26)` ≈ `O(n)`，因为 26 是常数。  
  - 大白话：我们遍历字符串一次（`n`），每次都检查所有字母（最多 26）以及它们的前驱（最多 26），所以整体工作量大约是 `n` 乘以 676 次简单比较。  
- **空间复杂度**：`O(n·26)`，即保存一个 `n×26` 的表。  
  - 大白话：想象每个字符位置我们记录 26 种可能的“分数”，总共最多 2600（100×26）个整数，完全可以放在电脑里。

---

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们发现瓶颈在于 **每次都要遍历 26×26 的组合**，虽然在本题的约束下还能接受，但我们可以进一步思考：  

1. **冲突只出现在相邻两个位置**。如果当前位置 `i` 与左边的字符几乎相等（相同或相邻），那么这两个字符 **至少要改动一次**，否则永远无法满足要求。  
2. **我们可以把改动的决定“推迟”到右边**：  
   - 假设已经处理好前 `i‑1` 位，并且我们已经把第 `i‑1` 位确定为一个安全字符 `prev`（可能是原字符，也可能是改过的）。  
   - 当看到第 `i` 位的原字符 `cur` 时，只要 `cur` 与 `prev` **不几乎相等**，我们就可以直接保留 `cur`，不需要任何操作。  
   - 若 `cur` 与 `prev` **几乎相等**，我们 **必须改动** 第 `i` 位（改动第 `i‑1` 位会破已经确定好的前缀，导致更复杂的回溯）。  
   - 改动 `i` 位时，只要挑一个既不几乎相等于 `prev`，也不几乎相等于原来的第 `i+1` 位的字符，就能保证**不会对后面的判断产生新的冲突**。因为字母表只有 26 个字母，而每个字符最多排除 3（自己、左邻、右邻），必定还有剩余字符可以选。  

3. **贪心策略**：从左到右扫描，**只在冲突出现时改动当前字符**，并把它视作“已经安全的字符”。这样每一次改动都是“必要且足够”的，整条链上不会出现多余的改动。  

**为什么贪心最优**  

- **必要性**：如果两个相邻字符几乎相等，至少要改动其中一个，否则冲突永远无法消除。  
- **充分性**：我们总能在冲突的右侧（即当前位置）找到一个合法的替代字符，使得它既不冲突左侧，也不冲突右侧（因为右侧的原字符还未被处理，我们可以把它当作“禁止列表”中的一个元素）。因此改动右侧永远能解决当前冲突而不引入新的冲突。  
- **最小化**：每一次冲突我们只改动一次，且没有任何冲突可以用 **零次** 改动解决，所以改动次数等于冲突出现的次数，已经是理论下界。  

**核心概念**：  
- **几乎相等**：`abs(c1 - c2) <= 1`（包括相同）。  
- **安全字符**：与左边字符不几乎相等，且在后面遍历时可以保证与右边字符不几乎相等。我们不需要真的找出它的具体字母，只要知道它一定能选到即可。  

#### 代码（Python）

```python
def minOperations_greedy(word: str) -> int:
    """
    贪心实现：只在当前位置与前一个已经确定的字符几乎相等时才改动。
    因为总能选到一个既不与左侧也不与右侧几乎相等的字符，
    所以改动次数恰好等于冲突出现的次数。
    """
    n = len(word)
    if n == 0:
        return 0

    ops = 0               # 已经进行的改动次数
    # prev 保存前一个字符“处理后”的实际字母。为了方便比较，
    # 把它记成整数 0~25；如果当前位置已经被改动，我们可以把它设成 -1，
    # 表示一个“安全的虚拟字符”，永远不会与真实字符冲突。
    prev = ord(word[0]) - ord('a')

    for i in range(1, n):
        cur = ord(word[i]) - ord('a')
        # 判断 cur 与 prev 是否几乎相等
        if cur == prev or abs(cur - prev) == 1:
            # 必须改动当前位置
            ops += 1
            # 把 prev 设成一个虚拟字符，保证下一个位置一定不会与它冲突
            prev = -1   # -1 代表“已经改成了一个安全字符”
        else:
            # 不冲突，保持原字符，更新 prev 为当前字符
            prev = cur

    return ops
```

> **关键注释**  
> - `prev = -1` 的作用是**不再限制**后面的字符。因为我们已经假设把当前位置改成了一个既不与左侧也不与右侧几乎相等的字母，这个字母在后续检查时可以视作“永远安全”。  
> - 实际上如果后面还有字符需要判断，它们只会和 `prev`（即 `-1`）比较，`-1` 与任何 0~25 的字符的差值大于 1，条件 `cur == prev or abs(cur - prev) == 1` 永远不成立，等价于冲突已经被消除。

#### 复杂度  

- **时间复杂度**：`O(n)`，只需要一次线性扫描。  
  - 大白话：我们从左到右看每个字母，一次比较、一次可能的计数，工作量跟字符串长度成正比。  
- **空间复杂度**：`O(1)`，只用几个整数保存状态，不随 `n` 增长。  

与暴力 DP 相比，**时间从 `O(n·26·26)` 降到 `O(n)`，空间从 `O(n·26)` 降到常数**，在所有输入规模下都快得多。

---

## 心得  

- **核心技巧**：**贪心消除冲突**——在出现“几乎相等”时必然改动右侧字符，并利用字母表的余量保证改动后不会产生新冲突。  
- **适用的题型**  
  1. “把字符串改造成不出现相邻相同（或相邻字母）”的题目，如 **Remove Adjacent Duplicates**、**Make String Great**。  
  2. 需要最少修改使相邻约束成立的 DP/贪心混合题目，如 **Minimum Number of Steps to Make Two Strings Anagram**（改动局部冲突）。  
- **一句话总结解题钥匙**：**每一次冲突都必须改动一次，且总可以把改动放在右边而不影响后续**。  

---

## 反思  

- **第一反应**：直接想到“遍历所有可能的字符组合”，于是写出 DP 暴力方案。  
- **最容易踩的坑**  
  - 忘记 **相邻字母** 也算冲突，只检查相同字符会导致错误。  
  - 在贪心实现中若不把已改动的位置设成“安全的虚拟字符”，会误把后面的原字符与已经改动的字符再次比较，导致多计数。  
  - 边界情况：字符串长度为 1 时无需任何操作，需要提前返回 0。  
- **下次类似题的第一步**：**先判断相邻位置是否违反约束**，如果违反，就**立刻进行一次改动**（通常是改动右侧），并**记录改动后该位置的状态**，这样可以在一次线性扫描中得到最优解。