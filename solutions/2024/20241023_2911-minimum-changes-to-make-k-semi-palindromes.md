# #2911. 最少修改次数使其成为 K 个半回文 / Minimum Changes to Make K Semi-palindromes

> 难度：困难 · 标签：Two Pointers、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/)

---

## 题目（英文原版）

**Description**

Given a string s and an integer k, partition s into k substrings such that the letter changes needed to make each substring a semi-palindrome are minimized.
Return the minimum number of letter changes required.
A semi-palindrome is a special type of string that can be divided into palindromes based on a repeating pattern. To check if a string is a semi-palindrome:​
Consider the string "abcabc":

**Examples**

**Example 1:**

```
Input: s = "abcac", k = 2
Output: 1
Explanation: Divide s into "ab" and "cac" . "cac" is already semi-palindrome. Change "ab" to "aa" , it becomes semi-palindrome with d = 1 .
```

**Example 2:**

```
Input: s = "abcdef", k = 2
Output: 2
Explanation: Divide s into substrings "abc" and "def" . Each needs one change to become semi-palindrome.
```

**Example 3:**

```
Input: s = "aabbaa", k = 3
Output: 0
Explanation: Divide s into substrings "aa" , "bb" and "aa" . All are already semi-palindromes.
```

**Constraints**

- 2 <= s.length <= 200
- 1 <= k <= s.length / 2
- s contains only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`，将 `s` 划分成 `k` 个子串，使得将每个子串改造成半回文（semi‑palindrome）所需的字母修改次数之和最小。返回所需的最少字母修改次数。

**半回文** 是一种特殊类型的字符串，能够依据某种循环模式被划分为若干回文（palindrome）。判断一个字符串是否为半回文的步骤如下（题目示例中给出了 `"abcabc"` 的说明）：

*（此处应补充半回文的判定规则，原题目描述略去）*

---

### 示例

#### 示例 1
```
Input: s = "abcac", k = 2
Output: 1
Explanation: 将 s 划分为 "ab" 和 "cac"。"cac" 已经是半回文。将 "ab" 改为 "aa"，只需 1 次修改，即可成为半回文。
```

#### 示例 2
```
Input: s = "abcdef", k = 2
Output: 2
Explanation: 将 s 划分为子串 "abc" 和 "def"。每个子串都需要一次修改才能成为半回文。
```

#### 示例 3
```
Input: s = "aabbaa", k = 3
Output: 0
Explanation: 将 s 划分为子串 "aa"、"bb" 和 "aa"。所有子串已经是半回文，修改次数为 0。
```

---

### 约束条件

- `2 <= s.length <= 200`
- `1 <= k <= s.length / 2`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一种可能的划分都枚举出来**，然后逐个检查每段子串需要改多少个字符才能变成「半回文」——这里的「半回文」实际上就是**普通回文**（即正着读、倒着读完全相同的字符串）。  

- **子串变成回文需要的改动**：把子串左右对应位置的字符两两比较，如果不相同就必须改动其中一个，使它们相等。统计所有不相等的对数，就是把该子串变成回文最少需要的改动次数。  
- **枚举划分**：把原字符串 `s` 划分成 `k` 段，等价于在 `len(s)-1` 个可能的切割点里挑选 `k-1` 个。可以用递归或穷举所有切点的组合来实现。  

> **类比**：把「字典」想象成一个查找表，键是「子串的左端点 i」和「右端点 j」，值是「把 s[i…j] 变成回文最少需要的改动数」。先把这个表（即 `cost[i][j]`）算好，后面查表就跟在字典里找页码一样快。

**为什么暴力解一定正确**  
- 每一种合法的划分我们都会算一次改动数，取最小值自然就是答案。  
- 对每个子串的改动数我们也穷举了所有可能的字符对（只能是左↔右对应），所以得到的改动数是最小的。

**复杂度分析（大白话）**  
- **枚举所有划分**：把 `n`（字符串长度）个位置中挑 `k-1` 个切点，组合数是 `C(n-1, k-1)`，在最坏情况下（比如 `k ≈ n/2`）会非常大，几乎是指数级的。  
- **计算每段子串的改动**：每次检查一个子串，需要比较大约 `len/2` 对字符。若把所有子串都重新比较一次，时间会是 `O(n³)`。  

> 用大白话讲，`O(n³)` 就像「把 200 块糖果每次都拿出 200 次再去数」——在本题的约束（`n ≤ 200`）下已经会超时。

#### 代码（Python）

```python
# 暴力解——仅作思路展示，实际会超时
def minChanges_bruteforce(s: str, k: int) -> int:
    n = len(s)

    # 1) 预计算 cost[i][j]：把 s[i..j] 变成回文最少需要的改动数
    cost = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            # 两端向中间收敛，统计不相等的字符对
            cnt = 0
            l, r = i, j
            while l < r:
                if s[l] != s[r]:
                    cnt += 1
                l += 1
                r -= 1
            cost[i][j] = cnt

    # 2) 递归枚举所有切点
    from functools import lru_cache

    @lru_cache(None)
    def dfs(start: int, parts: int) -> int:
        """从 start 开始，剩余需要 parts 段，返回最小改动数"""
        if parts == 1:                # 只剩最后一段，直接使用预计算的 cost
            return cost[start][n - 1]
        best = float('inf')
        # 把当前段切到 i（i 必须保证后面还能划分出 parts-1 段）
        for i in range(start, n - parts + 1):
            cur = cost[start][i] + dfs(i + 1, parts - 1)
            best = min(best, cur)
        return best

    return dfs(0, k)
```

> 关键行注释已在代码里，用中文解释每一步的作用。

#### 复杂度

- **时间复杂度**：`O(C(n-1, k-1) * n)`，在最坏情况下接近指数级，实际会超时。  
- **空间复杂度**：`O(n²)` 用于保存 `cost` 表，另外递归缓存 `O(n·k)`。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**重复计算相同子问题**。我们可以把问题拆成两层 DP：

1. **子串改成回文的代价**  
   - 对任意 `i ≤ j`，只需要比较 `s[i]` 与 `s[j]`、`s[i+1]` 与 `s[j-1]` …… 这一步的代价可以在 `O(1)` 时间内得到，只要我们事先把所有子串的代价算好。  
   - 这一步叫**预处理**，时间 `O(n²)`，空间 `O(n²)`（`n ≤ 200`，完全可以接受）。

2. **把整串划分成 k 段的最小总代价**  
   - 设 `dp[i][p]` 为**把前 i 个字符（即 s[0..i-1]）划分成 p 段**，所需的最小改动数。  
   - 转移方程：  
     ```
     dp[i][p] = min_{t < i} ( dp[t][p-1] + cost[t][i-1] )
     ```
     解释：第 `p` 段的左端点是 `t`，右端点是 `i-1`。前 `p-1` 段的最优代价已经在 `dp[t][p-1]` 中，当前段把 `s[t..i-1]` 变成回文的代价是 `cost[t][i-1]`，两者相加取最小即得到 `dp[i][p]`。  
   - 初始状态：`dp[0][0] = 0`（空串划分成 0 段代价为 0），其余设为无穷大。  
   - 最终答案是 `dp[n][k]`（全部 `n` 个字符划分成 `k` 段）。

> **类比**：想象我们在建造一条路。`cost[t][i-1]` 就是把第 `t` 到 `i-1` 段路面铺平的费用；`dp[t][p-1]` 是已经铺好的前面那段路的最小费用。我们只要把「已经铺好的」和「新铺的一段」的费用相加，挑出最省钱的方案。

**为什么这一步是最优的**  
- 每个子问题只求一次最小值，避免了暴力枚举时的指数级重复。  
- DP 的状态转移完整覆盖了所有合法划分，因为每一次划分都可以看作「把最后一段截出来」的过程。

**时间、空间分析（大白话）**  
- 预处理 `cost`：要比较 `n*(n-1)/2` 对字符，时间约 `n²/2`，也就是「把 200 块糖果两两配对一次」——非常快。  
- 主 DP：外层遍历 `i`（0…n），内层遍历 `p`（1…k），再内层遍历切点 `t`（0…i），总体是 `O(k·n²)`。在最坏情况下 `k ≤ n/2`，所以时间约 `O(n³/2)`，但常数极小，实际运行在 `n=200` 时毫秒级。  
- 空间：`cost` 表 `O(n²)`，`dp` 表 `O(k·n)`，总共也是 `O(n²)`。

#### 代码（Python）

```python
def minChanges(s: str, k: int) -> int:
    """
    把字符串 s 划分成 k 段，使每段变成回文的改动次数之和最小。
    返回最小改动次数。
    """
    n = len(s)

    # ---------- 1. 预处理：cost[i][j] 表示 s[i..j] 变成回文的最小改动数 ----------
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):          # 子串长度从 2 到 n
        for i in range(n - length + 1):
            j = i + length - 1
            # 只看两端是否相等，内部的代价已经在 cost[i+1][j-1] 中
            if s[i] == s[j]:
                cost[i][j] = cost[i + 1][j - 1] if i + 1 <= j - 1 else 0
            else:
                cost[i][j] = (cost[i + 1][j - 1] if i + 1 <= j - 1 else 0) + 1

    # ---------- 2. DP：dp[i][p] = 前 i 个字符划分成 p 段的最小改动数 ----------
    INF = float('inf')
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0                               # 空串划分成 0 段代价为 0

    for i in range(1, n + 1):                  # i 表示前 i 个字符（0-index 下标 i-1）
        for p in range(1, min(k, i) + 1):      # 至少要有 p 个字符才能划分成 p 段
            # 枚举第 p 段的左端点 t（0 ≤ t < i）
            for t in range(p - 1, i):          # t 必须 ≥ p-1，保证前面有足够字符划分成 p-1 段
                cur = dp[t][p - 1] + cost[t][i - 1]
                if cur < dp[i][p]:
                    dp[i][p] = cur

    return dp[n][k]
```

> **关键行中文注释**  
> - `cost[i][j]` 的递推利用了「只看最外层两字符」的思想，内部已经算好的代价直接拿来用，省掉了每次都重新比较的时间。  
> - `dp[t][p-1] + cost[t][i-1]` 正是「前面已经划好 + 最后一段再处理」的转移。

#### 复杂度

- **时间复杂度**：`O(k·n²)`  
  - 预处理 `cost`：`O(n²)`  
  - 主 DP 三层循环：`O(k·n²)`（在本题 `k ≤ n/2`，最坏约 `O(n³/2)`，但常数极小，实际运行毫秒级）  
- **空间复杂度**：`O(n²)`  
  - `cost` 表占 `n²`，`dp` 表占 `k·n ≤ n²/2`，总共仍是 `O(n²)`。

---

## 心得

- **核心技巧**：先**预处理**所有子串变成回文的代价（`cost` 表），再用**二维动态规划**在划分层面做最小化。  
- **此技巧适用的题型**：  
  1. **字符串分割最小代价**（如 LeetCode 1278 “Palindrome Partitioning III”）。  
  2. **把数组/序列划分成若干段使每段满足某种代价最小**（如 “Minimum Cost to Split Array”。）  
  3. **需要先算子区间代价再做区间划分的 DP**（如 “Burst Balloons” 之类的区间 DP）。  
- **一句话总结解题钥匙**：**先把“局部改动代价”算好，再用 DP 把“全局最优划分”拼出来**。

---

## 反思

- **拿到题目第一反应**：先想「把所有切点枚举出来」——也就是暴力搜索。  
- **最容易踩的坑**  
  1. **忘记子串最小改动数的递推**，直接在 DP 循环里每次都重新比较两端字符，导致时间爆炸。  
  2. **边界条件**：`dp` 的初始化必须把 `dp[0][0]=0`，其余设为无穷大；否则会出现「未划分却算了代价」的错误。  
  3. **子串长度为 1 时的代价**：单字符本身已经是回文，代价应为 0，预处理时要特别处理。  
- **下次遇到同类题，第一步该想到**：**“先把每段的代价预处理成表格”，再在这个表格上做 DP”。** 这样可以把指数级的暴力搜索压缩到多项式时间。