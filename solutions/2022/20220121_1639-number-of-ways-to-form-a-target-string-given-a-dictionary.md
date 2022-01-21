# #1639. **给定字典形成目标字符串的方法数** / Number of Ways to Form a Target String Given a Dictionary

> 难度：困难 · 标签：Array、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/)

---

## 题目（英文原版）

**Description**

You are given a list of strings of the same length words and a string target.
Your task is to form target using the given words under the following rules:
Notice that you can use multiple characters from the same string in words provided the conditions above are met.
Return the number of ways to form target from words. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: words = ["acca","bbbb","caca"], target = "aba"
Output: 6
Explanation: There are 6 ways to form target.
"aba" -> index 0 ("acca"), index 1 ("bbbb"), index 3 ("caca")
"aba" -> index 0 ("acca"), index 2 ("bbbb"), index 3 ("caca")
"aba" -> index 0 ("acca"), index 1 ("bbbb"), index 3 ("acca")
"aba" -> index 0 ("acca"), index 2 ("bbbb"), index 3 ("acca")
"aba" -> index 1 ("caca"), index 2 ("bbbb"), index 3 ("acca")
"aba" -> index 1 ("caca"), index 2 ("bbbb"), index 3 ("caca")
```

**Example 2:**

```
Input: words = ["abba","baab"], target = "bab"
Output: 4
Explanation: There are 4 ways to form target.
"bab" -> index 0 ("baab"), index 1 ("baab"), index 2 ("abba")
"bab" -> index 0 ("baab"), index 1 ("baab"), index 3 ("baab")
"bab" -> index 0 ("baab"), index 2 ("baab"), index 3 ("baab")
"bab" -> index 1 ("abba"), index 2 ("baab"), index 3 ("baab")
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 1000
- All strings in words have the same length.
- 1 <= target.length <= 1000
- words[i] and target contain only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `words`，其中所有字符串长度相同，以及一个目标字符串 `target`。  
请按照以下规则使用 `words` 中的字符来构造 `target`：

1. 依次为 `target` 中的每个字符选择一个字符加入构造的字符串。  
2. 对于某个单词（word）中的字符，若选择了下标为 `i` 的字符，则之后在同一单词中只能选择下标大于 `i` 的字符。  
3. 同一个单词可以被多次使用，只要满足规则 2 即可。

返回能够形成 `target` 的不同方式的数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模的结果。

---

### 示例

**示例 1**

```
Input: words = ["acca","bbbb","caca"], target = "aba"
Output: 6
Explanation: 共有 6 种方式可以形成 target。
"aba" -> 选第 0 位字符的 "acca"，第 1 位字符的 "bbbb"，第 3 位字符的 "caca"
"aba" -> 选第 0 位字符的 "acca"，第 2 位字符的 "bbbb"，第 3 位字符的 "caca"
"aba" -> 选第 0 位字符的 "acca"，第 1 位字符的 "bbbb"，第 3 位字符的 "acca"
"aba" -> 选第 0 位字符的 "acca"，第 2 位字符的 "bbbb"，第 3 位字符的 "acca"
"aba" -> 选第 1 位字符的 "caca"，第 2 位字符的 "bbbb"，第 3 位字符的 "caca"
...（其余情况省略）
```

**示例 2**

```
Input: words = ["abba","baab"], target = "bab"
Output: 4
Explanation: 共有 4 种方式可以形成 target。
"bab" -> 选第 0 位字符的 "baab"，第 1 位字符的 "baab"，第 2 位字符的 "abba"
"bab" -> 选第 0 位字符的 "baab"，第 1 位字符的 "baab"，第 3 位字符的 "baab"
"bab" -> 选第 0 位字符的 "baab"，第 2 位字符的 "baab"，第 3 位字符的 "baab"
"bab" -> 选第 1 位字符的 "abba"，第 2 位字符的 "baab"，第 3 位字符的 "baab"
```

---

### 约束条件

- `1 <= words.length <= 1000`
- `1 <= words[i].length <= 1000`
- `words` 中所有字符串的长度相同。
- `1 <= target.length <= 1000`
- `words[i]` 与 `target` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一列** 看成一排字母，然后把目标字符串 `target` 按顺序挑选字符。  
- 假设 `words` 有 `m` 列（所有单词长度相同），我们从左到右依次决定：第 `k` 列要不要选，选了的话选哪个字符。  
- 这相当于在每一列里遍历所有单词的字符，尝试把它们拼成 `target`。  

可以用递归（或深度优先搜索）实现：  

```
dfs(col, pos)   # 当前考虑第 col 列，已经匹配了 target 前 pos 个字符
    if pos == len(target):   # 已经全部匹配成功
        return 1
    if col == m:              # 已经没有列可以用了
        return 0
    # 1）不使用第 col 列，直接跳到下一列
    ans = dfs(col+1, pos)
    # 2）使用第 col 列，遍历所有单词，看有没有字符等于 target[pos]
    for each word w in words:
        if w[col] == target[pos]:
            ans += dfs(col+1, pos+1)
    return ans
```

**为什么正确**  
递归的每一步都枚举了「是否使用第 `col` 列」以及「如果使用，选哪个字符」这两种可能。  
所有合法的挑选顺序都会被遍历一次，最终计数即为答案。

**时间/空间复杂度**  
- 时间复杂度：在最坏情况下，每一列都有 `n`（`words` 的长度）个字符可以选，递归会产生 `O((n+1)^m)` 种状态，指数级爆炸。可以粗略写成 `O(n^m)`，即 **指数时间**。  
- 空间复杂度：递归栈的深度是 `m`，所以是 `O(m)`。

> 大白话：如果单词有 5 列、每列有 3 条可选路径，暴力解要把 `3⁵ = 243` 种组合全部尝试一遍，列数和单词数再大一点，组合数就会像滚雪球一样迅速变得不可想象。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numWays_bruteforce(words, target):
    m = len(words[0])               # 列数
    n = len(words)                  # 单词数
    t_len = len(target)

    # 记忆化搜索，避免重复子问题（仍然很慢，只是演示）
    from functools import lru_cache

    @lru_cache(None)
    def dfs(col, pos):
        # 已经匹配完 target
        if pos == t_len:
            return 1
        # 已经没有列可用了
        if col == m:
            return 0

        # 1）跳过当前列
        ans = dfs(col + 1, pos) % MOD

        # 2）使用当前列：遍历所有单词，看有没有字符等于 target[pos]
        ch = target[pos]
        for w in words:
            if w[col] == ch:                     # 找到可以匹配的字符
                ans = (ans + dfs(col + 1, pos + 1)) % MOD

        return ans

    return dfs(0, 0)
```

#### 复杂度

- **时间复杂度**：`O(n^m)`（指数级），因为每一列都可能有 `n` 条分支。  
- **空间复杂度**：`O(m)`，递归栈深度等于列数。  

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**每一列的具体单词顺序并不重要**，只要知道在第 `i` 列有多少个字符是 `'a'`、多少个是 `'b'` … 就足够决定选哪一个字符的方式数。  
这提示我们先把数据压缩成「**列频率表**」：

- `freq[i][c]` 表示第 `i` 列（0‑based）中字符 `c`（0‑25 对应 `'a'`~`'z'`）出现的次数。  
- 这一步相当于把所有单词排成一个矩阵，然后把每一列当成一本**字典**，查某个字符的页码就像查哈希表一样快速。

有了列频率后，问题变成：

> 在第 `i` 列我们可以**跳过**，也可以**使用**它。如果使用，必须把 `target[pos]` 对应的字符取出来，方式数等于该列中该字符的出现次数。

这正好适合**动态规划**（DP）：

- 设 `dp[j]` 为「使用前 `j` 列（0…j‑1）能够拼出 `target` 前 `i` 个字符的方式数」。
- 对每一列 `col`（从左到右）更新 `dp`，从后向前遍历 `target`，防止本轮更新时干扰还未更新的状态。

转移方程（`i` 为目标字符的下标，从 1 开始计）：

```
dp[i] = dp[i]                         # 不使用第 col 列
       + dp[i-1] * freq[col][ target[i-1] ]   # 使用第 col 列匹配第 i 个字符
```

- `dp[0]` 永远是 1，表示空字符串只有一种拼法。
- 最终答案是 `dp[len(target)]`。

**空间优化**：因为转移只依赖 `i` 与 `i-1`，可以把二维 DP 压成一维数组，遍历 `target` 时从后往前更新。

**为什么快**  
- 预处理频率只需遍历一次所有字符，时间 `O(m * n)`（`m` 列，`n` 单词）。  
- DP 主循环是 `O(m * t_len)`，其中 `t_len` 是目标长度。  
- 两者相乘仍然是线性级别，远远小于指数级暴力。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numWays(words, target):
    """
    最优解：先统计每一列的字符出现次数，再用一维动态规划计算方案数
    """
    m = len(words[0])          # 列数
    n = len(words)             # 单词数
    t_len = len(target)

    # 1️⃣ 统计列频率：freq[col][c] = 第 col 列字符 c 的出现次数
    # 使用二维列表，行数 = 列数，列数 = 26（英文字母）
    freq = [[0] * 26 for _ in range(m)]
    for w in words:
        for col, ch in enumerate(w):
            freq[col][ord(ch) - ord('a')] += 1

    # 2️⃣ DP：dp[i] = 前几列已经拼出 target 前 i 个字符的方式数
    dp = [0] * (t_len + 1)
    dp[0] = 1                 # 空字符串的基准

    # 按列遍历
    for col in range(m):
        # 为了不让本列的更新影响到同一轮次的更小 i，需要倒序遍历 target
        for i in range(t_len, 0, -1):
            ch_idx = ord(target[i - 1]) - ord('a')
            cnt = freq[col][ch_idx]          # 第 col 列中目标字符的出现次数
            if cnt:                           # 如果该列没有这个字符，直接跳过
                dp[i] = (dp[i] + dp[i - 1] * cnt) % MOD

    return dp[t_len]
```

#### 复杂度

- **时间复杂度**：`O(m * n + m * t_len)`  
  - 统计频率 `O(m * n)`（遍历所有字符）。  
  - 动态规划 `O(m * t_len)`（每列遍历目标长度）。  
  两者都是线性级别，远快于暴力的指数时间。  
- **空间复杂度**：`O(m * 26 + t_len)`  
  - `freq` 用 `m × 26` 的整数表（相当于每列的“字典”）。  
  - `dp` 只需要 `t_len + 1` 的一维数组。  

> 与暴力解对比：时间从指数级降到线性级，空间只多了一个 `m × 26` 的小表，完全可以接受。

---

## 心得

- **核心技巧**：把同一列的字符出现次数预处理成频率表，再用**一维动态规划**累计方案数。  
- **适用场景**：  
  1. 多个字符串按列对齐，需要统计“列上”信息的题目（如 LeetCode 1155 `Number of Dice Rolls With Target Sum` 的列频率思路）。  
  2. 需要在固定顺序的“位置”上挑选字符或数字，且每个位置的可选集合可以用计数表示（如 “构造字符串” 类题）。  
  3. 类似的“多行多列”组合计数问题，常用**列统计 + DP**的套路。  
- **解题钥匙**：**先压缩信息，再 DP**。先把重复的、无关的细节（单词顺序）用计数去掉，剩下的状态转移才会简洁高效。

---

## 反思

- **第一反应**：看到“可以从同一列的不同单词取字符”，立刻想到**暴力枚举每一种取法**。  
- **最容易踩的坑**：  
  - 忘记对每列的字符计数取模，导致中间乘法溢出。  
  - DP 更新顺序错误（正向遍历会把本轮新增的 `dp[i]` 再次用于后续的 `i+1`，导致重复计数）。  
  - 忽视目标长度可能大于列数的情况，需要在循环结束后直接返回 0。  
- **下次第一步**：先检查是否可以把“位置上的选择”用**频率/计数**抽象出来，若可以，就立刻建立列频率表，再考虑 DP 或组合数学。这样往往能把指数爆炸的暴力思路直接压缩到多项式时间。