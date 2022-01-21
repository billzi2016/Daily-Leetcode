# #1638. 相差一个字符的子串计数 / Count Substrings That Differ by One Character

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-substrings-that-differ-by-one-character/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, find the number of ways you can choose a non-empty substring of s and replace a single character by a different character such that the resulting substring is a substring of t. In other words, find the number of substrings in s that differ from some substring in t by exactly one character.
For example, the underlined substrings in "computer" and "computation" only differ by the 'e'/'a', so this is a valid way.
Return the number of substrings that satisfy the condition above.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "aba", t = "baba"
Output: 6
Explanation: The following are the pairs of substrings from s and t that differ by exactly 1 character:
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
The underlined portions are the substrings that are chosen from s and t.
```

**Example 2:**

```
Input: s = "ab", t = "bb"
Output: 3
Explanation: The following are the pairs of substrings from s and t that differ by 1 character:
("ab", "bb")
("ab", "bb")
("ab", "bb")
​​​​The underlined portions are the substrings that are chosen from s and t.
```

**Constraints**

- 1 <= s.length, t.length <= 100
- s and t consist of lowercase English letters only.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，求可以从 `s` 中选择一个非空子串（substring），并将其中恰好一个字符替换为不同的字符，使得得到的子串成为 `t` 的子串（substring）的方案数。换句话说，统计 `s` 中有多少子串与 `t` 中的某个子串恰好相差一个字符。

例如，`"computer"` 与 `"computation"` 中下划线标出的子串仅在字符 `'e'` 与 `'a'` 上不同，因此构成一种合法的方式。

返回满足上述条件的子串对的数量。

子串（substring）是字符串中连续的字符序列。

**示例 1**

```
Input: s = "aba", t = "baba"
Output: 6
Explanation: 以下是 `s` 与 `t` 中相差恰好 1 个字符的子串对：
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
下划线部分标示了从 `s` 和 `t` 中选取的子串。
```

**示例 2**

```
Input: s = "ab", t = "bb"
Output: 3
Explanation: 以下是 `s` 与 `t` 中相差 1 个字符的子串对：
("ab", "bb")
("ab", "bb")
("ab", "bb")
下划线部分标示了从 `s` 和 `t` 中选取的子串。
```

**约束条件**

- `1 <= s.length, t.length <= 100`
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 子串都列举出来，然后两两比较：

1. 先遍历 `s`，取出每一个非空子串 `sub_s`（可以用两层循环得到左、右端点）。  
2. 再遍历 `t`，取出每一个与 `sub_s` 长度相同的子串 `sub_t`。  
3. 对这两个子串逐字符比较，统计不同字符的个数。只有当恰好不同 **1** 个时，计数器 `ans` 加一。

> **类比**：把字符串看成一本书，子串就是书里连续的几页。暴力解相当于把 **每本书的每一段** 都拿出来，和 **另一本文字** 的每段对应起来，手动检查“只错一页”。  
> 哈希表在这里并不需要，用到的唯一数据结构是 **列表**（存放子串）和 **两个循环**。

**为什么正确**：我们把所有可能的「挑选 s 的子串」和「挑选 t 的子串」都枚举了一遍，凡是满足「只差一个字符」的配对都会被统计到，所以答案一定完整。

**时间/空间分析**（大白话）：

- `s` 长度记为 `n`，`t` 长度记为 `m`（均 ≤ 100）。  
- 枚举 `s` 的子串需要 `O(n²)`（左端点 × 右端点），同理 `t` 的子串需要 `O(m²)`。  
- 对每一对长度相同的子串，比较字符最多 `O(L)`（`L` 是子串长度），最坏情况下 `L` 可能是 `min(n,m)`。  
- 综合下来时间复杂度是 `O(n² * m² * min(n,m))`，在最坏情况下约为 `O(100⁵)`，对本题的约束已经会超时。  
- 只用了常数级额外空间，空间复杂度是 `O(1)`。

#### 代码（Python）

```python
def count_substrings_bruteforce(s: str, t: str) -> int:
    n, m = len(s), len(t)
    ans = 0

    # 枚举 s 的所有子串，左端点 i，右端点 i+len-1（左闭右开）
    for i in range(n):
        for j in range(i + 1, n + 1):          # 子串 s[i:j]
            sub_s = s[i:j]
            L = j - i                         # 子串长度

            # 在 t 中找所有同长度的子串
            for p in range(m - L + 1):        # t 的左端点
                sub_t = t[p:p + L]

                # 逐字符统计不同的个数
                diff = 0
                for a, b in zip(sub_s, sub_t):
                    if a != b:
                        diff += 1
                        if diff > 1:          # 早停，超过 1 就不可能了
                            break

                if diff == 1:                  # 正好差 1
                    ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n² * m² * min(n,m))`  
  > 这里的 `O` 只是一种“量级”标记，实际运行时间会随字符串长度的平方甚至更高增长，像 100 × 100 的输入已经会花费不少时间。  
- **空间复杂度**：`O(1)`（只用了几个整数变量）

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复比较**：同样的字符对会被比较很多次。  
我们需要把比较工作“合并”，一次遍历就能把所有可能的匹配信息算出来。核心思路是：

1. **把两个字符串对齐**：想象把 `s` 和 `t` 的字符排成一个网格，`s[i]` 与 `t[j]` 位于交点 `(i, j)`。  
2. **找出每个交点左侧相同的字符数**（即从 `(i-1, j-1)` 往左上走，连续相同的长度），记作 `left[i][j]`。这相当于“左边有多少字符已经匹配”。  
3. **找出每个交点右侧相同的字符数**（从 `(i+1, j+1)` 往右下走），记作 `right[i][j]`。这相当于“右边还能继续匹配多少”。  
4. 对每个 **不相同** 的字符 `s[i] != t[j]`，它可以作为「唯一不同的字符」的中心。  
   - 左侧可以选 `left[i][j] + 1` 种（包括不选左侧，即只取中心）。  
   - 右侧可以选 `right[i][j] + 1` 种（同理）。  
   - 两边独立选择，所以该中心贡献 ` (left[i][j] + 1) * (right[i][j] + 1) ` 种合法子串配对。  
5. 把所有中心的贡献累加，就是答案。

> **类比**：把两条绳子 `s`、`t` 拉直并排，对齐后每个字符位置都是一个“结”。如果结的颜色不一样，它就可以充当「唯一的不同颜色」的节点。左边有多少相同颜色的结、右边有多少相同颜色的结，就决定了可以往左/右延伸多少长度——左右的选择互不影响，乘法自然出现。

**如何高效得到 left / right**：

- `left[i][j]`（后缀相等长度）可以用 **动态规划** 一次遍历得到：  
  `left[i+1][j+1] = left[i][j] + 1` 当 `s[i] == t[j]`，否则 `0`。  
  这相当于「如果当前字符相等，就把左上角的相等长度加一」。  
- `right[i][j]`（前缀相等长度）同理，只是从后往前遍历：  
  `right[i][j] = right[i+1][j+1] + 1` 当 `s[i] == t[j]`，否则 `0`。

这样只需要 **两次 O(n·m)** 的遍历，就能得到所有 `left`、`right`，随后再一次遍历所有格子求和，整体时间是 **O(n·m)**，空间是 **O(n·m)**（或者用两张二维数组，甚至只保留一行实现 O(min(n,m)) 的空间，这里为清晰起见使用完整矩阵）。

#### 代码（Python）

```python
def count_substrings_optimal(s: str, t: str) -> int:
    n, m = len(s), len(t)

    # left[i+1][j+1] 表示 s 前 i 个字符 (0..i-1) 与 t 前 j 个字符 (0..j-1)
    # 的最长公共后缀长度。多加一行/列是为了防止下标越界。
    left = [[0] * (m + 1) for _ in range(n + 1)]

    # 从左上到右下填表
    for i in range(n):
        for j in range(m):
            if s[i] == t[j]:
                left[i + 1][j + 1] = left[i][j] + 1
            # else 默认是 0，保持不变

    # right[i][j] 表示 s 从 i 开始、t 从 j 开始的最长公共前缀长度
    right = [[0] * (m + 1) for _ in range(n + 1)]

    # 从右下往左上填表
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s[i] == t[j]:
                right[i][j] = right[i + 1][j + 1] + 1
            # else 保持 0

    ans = 0
    # 遍历每个格子，找出字符不同的位置
    for i in range(n):
        for j in range(m):
            if s[i] != t[j]:
                # left[i][j] 是左上角相等的长度，right[i+1][j+1] 是右下角相等的长度
                left_len = left[i][j]          # 左侧可以延伸的相同字符数
                right_len = right[i + 1][j + 1]  # 右侧可以延伸的相同字符数
                # +1 表示“可以不延伸”，乘法得到所有组合
                ans += (left_len + 1) * (right_len + 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  > 只需要三次遍历（一次算左后缀，一次算右前缀，一次求和），每次都是 `n*m` 次基本操作。相比暴力的指数级增长，这里随字符串长度线性增长，跑 100 × 100 的数据几乎是瞬间完成。  
- **空间复杂度**：`O(n·m)`  
  > 两张大小为 `(n+1)·(m+1)` 的整数矩阵。对本题的约束（≤ 100）来说，最多只占几千个整数，完全可以接受。若想进一步压缩空间，只保留上一行/列即可做到 `O(min(n,m))`。

---

## 心得  

- **核心技巧**：把「唯一不同字符」视为「中心」，左右两侧分别统计可以继续相等的最长长度，乘积即为该中心贡献的合法子串数。  
- **适用场景**：  
  1. **两个字符串相差恰好一个字符** 的计数（本题）。  
  2. **找出所有只含一个不匹配的子数组**（数值数组的类似问题）。  
  3. **统计两个序列的 “近似相等” 区间**，如 LeetCode 1638（Count Substrings That Differ by One Character）等变形。  
- **一句话总结解题钥匙**：  
  “把唯一的不同字符固定在某个位置，左右各自向外扩展相同字符的最长长度，左右的选择独立相乘即得所有合法子串。”

---

## 反思  

- **第一反应**：直接枚举所有子串，然后逐字符比较——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记 **“左侧/右侧可以不选”**，导致漏算长度为 1 的子串（只包含中心字符）。  
  - 边界处理不当：`left` 与 `right` 的下标偏移容易出错，尤其是 `right[i+1][j+1]` 与 `left[i][j]` 的对应关系。  
  - 对于长度为 0 的子串没有意义，需要排除空子串。  
- **下次遇到同类题**：第一步先 **思考“唯一不同点”可以放在哪”，再 **统计它左/右两侧的相同前缀/后缀**，把乘法组合的思想写下来，再决定是否需要 DP 表来保存这些前缀/后缀长度。这样往往能直接把时间从指数级降到线性级。