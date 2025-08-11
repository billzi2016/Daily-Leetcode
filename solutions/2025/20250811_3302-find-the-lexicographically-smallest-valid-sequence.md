# #3302. **找字典序最小的合法序列** / Find the Lexicographically Smallest Valid Sequence

> 难度：中等 · 标签：Two Pointers、String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/find-the-lexicographically-smallest-valid-sequence/)

---

## 题目（英文原版）

**Description**

You are given two strings word1 and word2.
A string x is called almost equal to y if you can change at most one character in x to make it identical to y.
A sequence of indices seq is called valid if:
Return an array of size word2.length representing the lexicographically smallest valid sequence of indices. If no such sequence of indices exists, return an empty array.
Note that the answer must represent the lexicographically smallest array, not the corresponding string formed by those indices.

**Examples**

**Example 1:**

```
Input: word1 = "vbcca", word2 = "abc"
Output: [0,1,2]
Explanation:
The lexicographically smallest valid sequence of indices is [0, 1, 2] :
```

**Example 2:**

```
Input: word1 = "bacdc", word2 = "abc"
Output: [1,2,4]
Explanation:
The lexicographically smallest valid sequence of indices is [1, 2, 4] :
```

**Example 3:**

```
Input: word1 = "aaaaaa", word2 = "aaabc"
Output: []
Explanation:
There is no valid sequence of indices.
```

**Example 4:**

```
Input: word1 = "abc", word2 = "ab"
Output: [0,1]
```

**Constraints**

- 1 <= word2.length < word1.length <= 3 * 105
- word1 and word2 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`。

- 若可以通过修改字符串 `x` 中至多一个字符，使其与字符串 `y` 完全相同，则称 `x` **几乎相等 (almost equal)** 于 `y`。
- 若一个下标序列 `seq` 满足以下条件，则称其为 **合法 (valid)** 的：
  1. `seq` 长度等于 `word2.length`，且下标严格递增（即构成 `word1` 的一个子序列）。
  2. 将 `word1` 中对应下标的字符依次拼接得到的字符串 `t = word1[seq[0]] word1[seq[1]] … word1[seq[m‑1]]`（其中 `m = word2.length`）与 `word2` **几乎相等**。

返回一个大小为 `word2.length` 的数组，表示字典序最小的合法下标序列 `seq`。如果不存在合法序列，返回空数组。

> 注意：答案必须是字典序最小的 **数组**，而不是由这些下标组成的字符串的字典序。

---

### 示例

**示例 1**

```text
Input: word1 = "vbcca", word2 = "abc"
Output: [0,1,2]
Explanation:
字典序最小的合法序列为 [0, 1, 2]，对应的子序列字符串为 "vbc"，与 "abc" 只在第一个字符不同，满足几乎相等。
```

**示例 2**

```text
Input: word1 = "bacdc", word2 = "abc"
Output: [1,2,4]
Explanation:
字典序最小的合法序列为 [1, 2, 4]，对应的子序列字符串为 "acc"，仅在第二个字符不同，满足几乎相等。
```

**示例 3**

```text
Input: word1 = "aaaaaa", word2 = "aaabc"
Output: []
Explanation:
不存在合法序列，因为任何长度为 5 的子序列都是 "aaaaa"，与 "aaabc" 至少有两个字符不同，不满足几乎相等。
```

**示例 4**

```text
Input: word1 = "abc", word2 = "ab"
Output: [0,1]
Explanation:
字典序最小的合法序列为 [0, 1]，对应的子序列字符串为 "ab"，与 "ab" 完全相同，满足几乎相等。
```

---

### 约束

- `1 <= word2.length < word1.length <= 3 * 10^5`
- `word1` 和 `word2` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **word1** 看成一本长长的书，**word2** 看成我们想要抄写的短句。  
我们要在 **word1** 中挑选出 `len(word2)` 个字符（下标严格递增），把它们连起来得到一个新字符串 **s**，要求 **s** 和 **word2** 至多只相差 **一个字符**（可以把这个字符改成想要的即可）。  

暴力实现的思路：

1. 从 **word1** 的第一个字符开始，尝试把它当成 **word2[0]**，再继续往后找 **word2[1]** …  
2. 在挑选的过程中记录已经用了多少次“改字符”的机会（最多一次）。  
3. 当挑选完 `len(word2)` 个字符后，检查是否满足“最多一次改字符”。如果满足，就得到一组合法的下标序列。  
4. 把所有合法序列放进列表，最后挑选字典序最小的那一个。

> **类比**：把 `word1` 想成一本字典，查找每个 `word2` 的字符就像在字典里找对应的页码。暴力法就是把每一种可能的“查找路径”都走一遍。

> **为什么正确**：只要遍历了所有可能的下标组合，肯定不会漏掉任何合法解。于是最小的那个一定在遍历得到的集合里。

> **时间/空间分析**：  
> - 对每一种可能的下标组合都要检查一次。最坏情况下，`word1` 长度是 `n`，`word2` 长度是 `m`，组合数大约是 `C(n, m)`（组合数），随 `n,m` 指数增长。  
> - 每次检查需要遍历 `m` 个字符，整体时间复杂度约为 `O(C(n,m)·m)`，在最坏情况下几乎是 **指数级**，根本跑不完。  
> - 只用到几个指针和临时数组，空间复杂度是 `O(m)`。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def brute_force(word1: str, word2: str) -> List[int]:
    n, m = len(word1), len(word2)
    best = None                     # 用来保存字典序最小的答案

    # 逐一枚举所有长度为 m、下标递增的组合
    for idxs in combinations(range(n), m):
        # 统计与 word2 不同的字符个数
        diff = sum(1 for i, j in zip(idxs, range(m))
                   if word1[i] != word2[j])
        if diff <= 1:                # 至多允许一次改动
            if best is None or list(idxs) < best:
                best = list(idxs)

    return best if best is not None else []
```

> **关键行解释**  
> - `combinations(range(n), m)`：相当于把 **word1** 的每个字符都列出所有可能的取法，类似把字典的所有页码组合列出来。  
> - `diff = sum(1 for i, j in zip(idxs, range(m)) if word1[i] != word2[j])`：统计需要改动的字符数。  
> - `if diff <= 1`：满足“最多一次改字符”的条件。  
> - `list(idxs) < best`：Python 中列表的比较就是字典序比较，直接得到字典序更小的序列。

#### 复杂度  

- **时间复杂度**：`O(C(n,m)·m)`（指数级）——把所有可能的下标组合都枚举一次，远远超出题目给出的 3·10⁵ 规模。  
- **空间复杂度**：`O(m)`——只保存当前组合和最优答案。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举所有组合**，这一步把时间推到了指数级。  
观察题目：我们只需要 **一个** 合法的下标序列，并且要 **字典序最小**。  
这提示我们可以 **从左到右** 贪心地挑选每一个下标：  
- 先找能够放在最左边的字符（下标最小），  
- 再在它右边继续找下一个，以此类推。  

但是在挑选的过程中，需要确保 **后面的字符仍然有办法完成**。  
这正是提示里提供的 `dp` 数组的用处：  

> **dp[i]** = “在 `word1[i:]`（从 i 开始的后缀）中，能够匹配 `word2` 的**最长后缀**的长度”。  

换句话说，`dp[i]` 告诉我们“从 i 开始往后看，最多还能匹配 `word2` 的多少个字符”。  
有了它，我们就能在贪心选取时**提前判断**：如果现在选了下标 `i`，剩下的字符还能否在 `word1[i+1:]` 中匹配完成？

下面分两步说明如何得到 `dp`，以及如何利用它贪心选取下标。

---

#### 2.1 计算 `dp`（后缀匹配长度）

我们从右往左扫描 `word1`，同时把 `word2` 当成倒着匹配的目标。  
设 `m = len(word2)`，`dp[n] = 0`（空后缀能匹配 0 个字符）。  

对每个位置 `i`（从 `n-1` 到 `0`）：

- `dp[i+1]` 已经知道它能匹配的最长后缀长度。  
- 如果 `dp[i+1] < m` 且 `word1[i] == word2[m - dp[i+1] - 1]`，说明 `word1[i]` 正好可以再匹配 **一个** 更长的后缀（把 `word2` 最后一个未匹配的字符补上），于是 `dp[i] = dp[i+1] + 1`。  
- 否则，`word1[i]` 不能再延伸后缀，`dp[i] = dp[i+1]`。

这一步只遍历一次 `word1`，时间 `O(n)`，空间 `O(n)`（也可以把数组压缩成 `O(1)`，但为了后面的查询方便保留完整数组）。

---

#### 2.2 贪心选取下标  

我们从左到右遍历 `word2`（记下标为 `j`），同时维护：

- `pos`：在 `word1` 中当前可选的最左位置（上一轮选取的下一个位置）。  
- `used`：是否已经用了“改字符”的机会（最多一次）。  

对于每个 `j`，我们要找 **最小的 `i ≥ pos`** 满足：

1. **后缀可行性**：`dp[i+1] ≥ (m - j - 1)`，即在 `word1[i+1:]` 中还能匹配剩下的 `m-j-1` 个字符。  
2. **字符匹配**  
   - 若 `word1[i] == word2[j]`，直接使用该下标。  
   - 若不相等且 `used == False`，我们可以把这里当成唯一的改字符位置（使用一次 `used = True`），同样要满足条件 1。  
   - 若不相等且已经用过改字符，则不能选这个 `i`。

因为我们从 `pos` 开始线性扫描，一旦找到符合条件的 `i`，立刻把它加入答案，更新 `pos = i + 1`，继续处理下一个 `j`。  

如果在扫描过程中 `i` 越界（`i == n`）仍未找到合法位置，说明 **不存在** 任意合法序列，直接返回空数组。

这整个过程只遍历 `word1` 一次（每个字符最多被检查两次），时间 `O(n + m)`，空间 `O(n)` 用来存 `dp`，答案数组 `O(m)`。

---

#### 代码（Python）

```python
from typing import List

def smallestValidSequence(word1: str, word2: str) -> List[int]:
    n, m = len(word1), len(word2)
    # ---------- 1. 计算 dp ----------
    dp = [0] * (n + 1)          # dp[n] = 0 已经在初始化里
    for i in range(n - 1, -1, -1):
        # 当前已经匹配的后缀长度是 dp[i+1]
        if dp[i + 1] < m and word1[i] == word2[m - dp[i + 1] - 1]:
            dp[i] = dp[i + 1] + 1          # 再多匹配一个字符
        else:
            dp[i] = dp[i + 1]              # 维持原来的最长后缀长度

    # ---------- 2. 贪心挑选 ----------
    ans: List[int] = []
    pos = 0                # 下一次搜索的起点（上一次选取的下一个位置）
    used = False           # 是否已经用了“改一个字符”的机会

    for j in range(m):                     # j 为 word2 的当前位置
        # 剩余需要匹配的字符数
        need = m - j - 1

        # 在 word1 中从 pos 开始寻找最左的可行下标 i
        while pos < n:
            # ① 检查剩余后缀是否还能完成（dp[pos+1] 必须 >= need）
            if dp[pos + 1] < need:         # 已经不可能完成，直接返回空
                return []

            # ② 看看当前字符能否使用
            if word1[pos] == word2[j]:
                # 完全匹配，直接选
                ans.append(pos)
                pos += 1
                break
            else:
                # 不匹配，看看能否把它当成唯一的改字符位置
                if not used:
                    # 使用一次改字符的机会
                    ans.append(pos)
                    pos += 1
                    used = True
                    break
                # 已经用了改字符，当前字符不能选，只能往后找
            pos += 1
        else:
            # while 循环跑完都没有 break，说明找不到合法 i
            return []

    # 检查是否真的只用了最多一次改字符（安全起见）
    # （这里理论上已经保证，但加一层防御）
    diff = sum(1 for i, ch in zip(ans, word2) if word1[i] != ch)
    if diff > 1:
        return []

    return ans
```

> **代码要点注释**  
> - `dp[i]` 的计算公式对应提示中的递推式。  
> - `need = m - j - 1` 表示“后面还要匹配多少字符”。  
> - `if dp[pos + 1] < need:` 这一步是 **提前剪枝**：如果从 `pos+1` 开始已经不足以完成剩余匹配，说明无论怎么选都不行，直接返回空。  
> - `used` 标记确保“最多改一次”。  

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 计算 `dp` 只遍历一次 `word1`（`O(n)`）。  
  - 贪心选取时 `pos` 只向右移动，总共不超过 `n` 步，加上遍历 `word2`（`O(m)`），合计线性。  
  - 与暴力解的指数级时间相比，快了好几个数量级，完全可以处理 `3·10⁵` 的规模。  

- **空间复杂度**：`O(n)`（`dp` 数组）+ `O(m)`（答案），总计 `O(n)`。  
  - 相比暴力的 `O(m)`，多了一段线性额外空间，但在本题的限制下是完全可以接受的。

---

## 心得  

- **核心技巧**：**后缀匹配 DP + 贪心**。  
  - DP 负责“看远”，提前告诉我们从当前位置往后还能完成多少匹配。  
  - 贪心利用这个信息，始终把每一步的下标选得尽可能左（字典序最小）。  
- **适用的题型**  
  1. **子序列匹配 + 限制改动次数**（如本题）。  
  2. **在字符串中找字典序最小的合法子序列**（如“最小字典序的子序列”类题）。  
  3. **需要提前判断后缀可行性的双指针/贪心问题**（如 “从左到右挑选满足条件的字符”）。
- **一句话总结**：**先用 DP 预计算“还能走多远”，再用贪心把每一步推到最左——这就是字典序最小合法序列的钥匙。**

---

## 反思  

- **第一反应**：看到“几乎相等（最多一次改字符）”和“字典序最小”，自然想到**暴力枚举**所有子序列，然后挑最小的。  
- **最容易踩的坑**  
  1. **忽视后缀不可行性**：只贪心找匹配字符而不检查后面还能否完成，容易在中途卡死导致错误答案。  
  2. **改字符次数控制不严**：在贪心过程中必须明确“是否已经使用了改字符”，否则会误选两个不匹配的位置。  
  3. **边界条件**：`dp` 的下标要多留一个哨兵 (`dp[n]=0`)；在检查 `dp[pos+1]` 时要防止越界。  
- **下次类似题的第一步**：  
  **先把“后面还能完成多少”用 DP/前缀或后缀信息算出来**，再在此基础上进行贪心或双指针的选择。这样可以把“全局可行性”转化为局部的快速判断，避免指数级搜索。