# #712. 两字符串的最小 ASCII 删除和 / Minimum ASCII Delete Sum for Two Strings

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/)

---

## 题目（英文原版）

**Description**

Given two strings s1 and s2, return the lowest ASCII sum of deleted characters to make two strings equal.

**Examples**

**Example 1:**

```
Input: s1 = "sea", s2 = "eat"
Output: 231
Explanation: Deleting "s" from "sea" adds the ASCII value of "s" (115) to the sum.
Deleting "t" from "eat" adds 116 to the sum.
At the end, both strings are equal, and 115 + 116 = 231 is the minimum sum possible to achieve this.
```

**Example 2:**

```
Input: s1 = "delete", s2 = "leet"
Output: 403
Explanation: Deleting "dee" from "delete" to turn the string into "let",
adds 100[d] + 101[e] + 101[e] to the sum.
Deleting "e" from "leet" adds 101[e] to the sum.
At the end, both strings are equal to "let", and the answer is 100+101+101+101 = 403.
If instead we turned both strings into "lee" or "eet", we would get answers of 433 or 417, which are higher.
```

**Constraints**

- 1 <= s1.length, s2.length <= 1000
- s1 and s2 consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s1` 和 `s2`，返回通过删除字符使两字符串相等所需的 **ASCII 码（ASCII）** 和的最小值。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1:**  
```
Input: s1 = "sea", s2 = "eat"
Output: 231
Explanation: 删除 "sea" 中的字符 "s"，会将字符 "s" 的 ASCII 码值 115 加入总和。  
删除 "eat" 中的字符 "t"，会将字符 "t" 的 ASCII 码值 116 加入总和。  
最终两字符串相等，115 + 116 = 231 是能够达到此目标的最小和。
```

**示例 2:**  
```
Input: s1 = "delete", s2 = "leet"
Output: 403
Explanation: 将 "delete" 删除为 "let"，需要删除字符 "d"、"e"、"e"，其 ASCII 码值分别为 100、101、101，累计 302。  
将 "leet" 删除为 "let"，需要删除字符 "e"，其 ASCII 码值为 101。  
最终两字符串均为 "let"，总和为 100 + 101 + 101 + 101 = 403。  
如果把两字符串都改成 "lee" 或者 "eet"，得到的和分别为 433 或 417，均更大。
```

**约束条件**  
- `1 <= s1.length, s2.length <= 1000`  
- `s1` 和 `s2` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两串每一种可能的删除方式全部枚举**，算出每种情况下被删除字符的 ASCII 和，取最小值。

- **枚举过程**：对 `s1` 的每一个字符，决定是“保留”还是“删除”。同理对 `s2`。  
  把两串删到同样的长度后，再检查剩下的字符序列是否相同。若相同，就算出本次删除的 ASCII 和。  
- **数据结构**：这里其实只需要**递归的调用栈**来记录我们当前在第几位、已经删了哪些字符。可以把它想象成 **一棵遍历所有可能路径的树**，每走一步就决定是“保留”还是“删除”。  
- **为什么正确**：因为我们把**所有可能的删除组合**都遍历了一遍，最小的那个自然就是答案。

> 生活中的类比：想象你有两本书，要把它们删到内容完全相同。暴力做法就是把每页都拆开，尝试把每页留或扔，所有可能的组合都试一遍，最后找出花费（页码对应的费用）最少的那种方式。

#### 代码（Python）

```python
def minimumDeleteSum_bruteforce(s1: str, s2: str) -> int:
    # 递归枚举所有删除方式
    from functools import lru_cache

    @lru_cache(maxsize=None)                     # 记忆化，防止同样状态重复计算
    def dfs(i: int, j: int) -> int:
        # i、j 分别是 s1、s2 当前指针的位置
        # 当任意一个已经遍历完时，只能把剩下的字符全部删掉
        if i == len(s1):
            return sum(ord(ch) for ch in s2[j:])   # 删除 s2 剩余部分的 ASCII 和
        if j == len(s2):
            return sum(ord(ch) for ch in s1[i:])   # 删除 s1 剩余部分的 ASCII 和

        if s1[i] == s2[j]:                         # 当前字符相等，保留，两指针都向前走
            return dfs(i + 1, j + 1)

        # 两种选择：删掉 s1[i] 或删掉 s2[j]，取花费更小的那条路
        delete_s1 = ord(s1[i]) + dfs(i + 1, j)     # 删除 s1[i]，累计其 ASCII 值
        delete_s2 = ord(s2[j]) + dfs(i, j + 1)     # 删除 s2[j]，累计其 ASCII 值
        return min(delete_s1, delete_s2)

    return dfs(0, 0)
```

> **关键行解释**  
> - `@lru_cache`：把已经算过的子问题结果存下来，避免指数级重复计算（相当于给递归装了“记事本”）。  
> - `if s1[i] == s2[j]`：字符相等时直接跳过，等价于“这两个字符已经匹配，无需删除”。  
> - `ord(ch)`：把字符转换为对应的 ASCII 码，题目要求的就是这些数值的和。

#### 复杂度

- **时间复杂度**：最坏情况下每个字符都有“删 / 不删”两种选择，搜索空间是 `2^{|s1|+|s2|}`，呈指数级。即 **指数时间**，在长度 10 左右已经不可接受。  
- **空间复杂度**：递归栈的深度最多 `|s1| + |s2|`，再加上记忆化表保存的状态数 `O(|s1|·|s2|)`（因为每个 `(i,j)` 只会计算一次），总体 **O(|s1|·|s2|)**。

> 大白话：暴力解相当于“把所有可能的路径都走一遍”，所以时间会像“翻山越岭”一样快到不行。  

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**状态只和两个指针的位置有关**：`i` 表示 `s1` 已经处理到哪儿，`j` 表示 `s2` 已经处理到哪儿。  
这正好符合**动态规划（Dynamic Programming，DP）**的使用场景——把大问题拆成子问题，子问题之间有重叠。

**瓶颈**  
- 暴力递归在没有记忆化时会重复计算很多相同的 `(i,j)` 子问题。即使记忆化后，递归本身仍然需要 **函数调用的开销**，而且实现稍显晦涩。  
- 我们可以把递归改写成 **自底向上的 DP 表**，一次性算完所有子问题，既直观又高效。

**核心概念——最长公共子序列（LCS）**  
如果我们把 **不需要删除的字符** 看成两串的公共子序列，那么要删除的字符就是两串的其余部分。  
- 设 `LCS` 为两串的**最长公共子序列**（顺序必须保持），则把两串都压缩成 `LCS` 需要删除的字符即为答案。  
- 删除的 ASCII 总和 = `sum_ascii(s1) + sum_ascii(s2) - 2 * sum_ascii(LCS)`  
  因为 `LCS` 中的字符既保留在 `s1` 也保留在 `s2`，它们的 ASCII 只算一次，剩下的都要被删掉。

**如何求 LCS 的 ASCII 和**  
普通的 LCS 用 `dp[i][j]` 表示 **长度**，这里我们改为 **ASCII 和**。  
- `dp[i][j]` 表示 `s1[:i]`（前 i 个字符）和 `s2[:j]`（前 j 个字符）的 **最大公共子序列的 ASCII 和**。  
- 转移方程：

| 情况 | 说明 | 转移式 |
|------|------|--------|
| `s1[i-1] == s2[j-1]` | 两个字符相同，可以加入公共子序列 | `dp[i][j] = dp[i-1][j-1] + ord(s1[i-1])` |
| `s1[i-1] != s2[j-1]` | 不能同时取两者，取删除较少的那条路（即保留 ASCII 和更大的那条） | `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` |

- 初始化：`dp[0][*] = dp[*][0] = 0`，因为空串和任何串的公共子序列 ASCII 和为 0。

**完整思路**  
1. 预先算出两个字符串的 ASCII 总和 `total = sum(ord(c) for c in s1) + sum(ord(c) for c in s2)`。  
2. 用 DP 求出 `lcs_ascii = dp[m][n]`（`m = len(s1)`, `n = len(s2)`）。  
3. 答案 = `total - 2 * lcs_ascii`。

> 类比：把两串看成两条绳子，想要把它们拉成完全相同的形状，只能保留下 **最长的公共颜色段**（这里的颜色用 ASCII 表示），其余的颜色全部剪掉，花费就是被剪掉颜色的总价值。

#### 代码（Python）

```python
def minimumDeleteSum(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)

    # 1️⃣ 计算两个字符串各自的 ASCII 总和
    total_ascii = sum(ord(c) for c in s1) + sum(ord(c) for c in s2)

    # 2️⃣ 创建 DP 表，dp[i][j] 表示 s1[:i] 与 s2[:j] 的最长公共子序列的 ASCII 和
    #    为了节省空间，只保留上一行和当前行（滚动数组）
    dp_prev = [0] * (n + 1)          # dp[i-1][*]
    dp_cur  = [0] * (n + 1)          # dp[i][*]

    for i in range(1, m + 1):
        dp_cur[0] = 0                # 第 0 列始终为 0（空串的情况）
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # 字符相等，加入公共子序列，累加它的 ASCII 值
                dp_cur[j] = dp_prev[j - 1] + ord(s1[i - 1])
            else:
                # 不相等，取两种可能中 ASCII 和更大的那个
                dp_cur[j] = max(dp_prev[j], dp_cur[j - 1])
        # 本行算完后，切换指针，让 dp_cur 成为下一轮的 dp_prev
        dp_prev, dp_cur = dp_cur, dp_prev

    lcs_ascii = dp_prev[n]          # 最终的最长公共子序列的 ASCII 和

    # 3️⃣ 计算最小删除和
    return total_ascii - 2 * lcs_ascii
```

> **关键行解释**  
> - `dp_prev` / `dp_cur`：只保留两行，空间从 `O(m·n)` 降到 `O(n)`。相当于“只记住上一层楼的状态”。  
> - `if s1[i - 1] == s2[j - 1]`：字符相等时，意味着我们可以把它放进公共子序列，**把它的 ASCII 加到已有的最大和上**。  
> - `max(dp_prev[j], dp_cur[j - 1])`：不相等时，选择把 `s1[i-1]` 删掉（对应 `dp_prev[j]`）还是把 `s2[j-1]` 删掉（对应 `dp_cur[j-1]`），保留 **ASCII 和更大的** 那条路。  

#### 复杂度

- **时间复杂度**：`O(m·n)`，其中 `m = len(s1)`, `n = len(s2)`。因为我们遍历了一个 `m × n` 的表，每个格子只做 O(1) 的计算。  
  > 与暴力解的指数级相比，这就像把“翻山越岭”压缩成了“一张网格图”，只需要一次遍历即可。  
- **空间复杂度**：`O(n)`（滚动数组），原本的完整 DP 表是 `O(m·n)`，但我们只保留当前行和上一行，两行的长度都是 `n+1`。  
  > 如果不使用滚动数组，则空间是 `O(m·n)`，但对本题的 1000 × 1000 限制仍然可以接受。

---

## 心得

- **核心技巧**：把“最小删除代价”转化为“**保留下来的公共子序列的最大 ASCII 和**”，从而利用 **最长公共子序列（LCS）** 的动态规划框架求解。  
- **适用的题型**  
  1. **Minimum Deletion Cost to Make Two Strings Equal**（本题的变体，只是权值不同）。  
  2. **Edit Distance / Levenshtein Distance**（需要插入、删除、替换的最小操作数）。  
  3. **Maximum ASCII Delete Sum for Two Strings**（求保留的 ASCII 和最大值的等价问题）。  
- **一句话总结解题钥匙**：**把“删除最少” ⇔ “保留最多”，用 LCS 计算保留的最大价值**。

---

## 反思

- **第一反应**：直接想到递归枚举所有删除方式，随后担心会超时。  
- **最容易踩的坑**  
  - 忘记把 **ASCII 值** 而不是字符本身计入成本。  
  - 在 DP 转移时误用了 **最小** 而不是 **最大**（因为我们在最大化保留下来的 ASCII）。  
  - 边界条件：`dp[0][*]`、`dp[*][0]` 必须初始化为 0，否则会出现负值或错误累加。  
- **下次类似题目第一步**：先思考“**哪些字符是可以保留下来的**”，把问题转化为 “**最大化保留价值**”，再决定使用 **最长公共子序列** 或 **背包/子序列** 等 DP 模型。