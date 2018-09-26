# #115. 不同的子序列 / Distinct Subsequences

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/distinct-subsequences/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, return the number of distinct subsequences of s which equals t.
The test cases are generated so that the answer fits on a 32-bit signed integer.

**Examples**

**Example 1:**

```
Input: s = "rabbbit", t = "rabbit"
Output: 3
Explanation:
As shown below, there are 3 ways you can generate "rabbit" from s.
rabbbit
rabbbit
rabbbit
```

**Example 2:**

```
Input: s = "babgbag", t = "bag"
Output: 5
Explanation:
As shown below, there are 5 ways you can generate "bag" from s.
babgbag
babgbag
babgbag
babgbag
babgbag
```

**Constraints**

- 1 <= s.length, t.length <= 1000
- s and t consist of English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，返回 `s` 中等于 `t` 的不同子序列（subsequence）的数量。  
测试用例保证答案能够放入 32 位有符号整数中。

**示例 1**  
**输入**: `s = "rabbbit", t = "rabbit"`  
**输出**: `3`  
**解释**: 如下所示，有 3 种方法可以从 `s` 生成 `"rabbit"`。  
```
rabbbit
rabbbit
rabbbit
```

**示例 2**  
**输入**: `s = "babgbag", t = "bag"`  
**输出**: `5`  
**解释**: 如下所示，有 5 种方法可以从 `s` 生成 `"bag"`。  
```
babgbag
babgbag
babgbag
babgbag
babgbag
```

**约束条件**  
- `1 <= s.length, t.length <= 1000`  
- `s` 和 `t` 仅由英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把 `s` 的所有子序列都列举出来**，然后统计有多少子序列恰好等于 `t`。  
- **子序列**可以理解为：从原字符串中挑选若干字符，**保持原来的相对顺序**，但不要求连续。  
- 这就像从一堆书中挑选若干本，挑的顺序必须和书架上的顺序一致，但可以跳过中间的书。

实现上可以用**递归**（或回溯）遍历每一个字符，决定“保留”还是“跳过”。  
- 当遍历完 `s` 时，如果已经匹配完 `t`（即 `t` 的所有字符都被选中了），就算一种合法的子序列。  
- 否则不算。

这种方法一定是**正确的**，因为它穷举了所有可能的挑选方式，必然不会漏掉任何合法解。

**时间/空间复杂度**  
- 对于长度为 `n` 的 `s`，每个字符都有“保留 / 跳过”两种选择，总共会产生 `2^n` 种子序列（指数级）。所以时间复杂度是 **O(2ⁿ)**，这在 `n ≤ 1000` 时根本不可接受。  
- 递归深度最多 `n`，使用的栈空间是 **O(n)**。

#### 代码（Python）

```python
def numDistinct_bruteforce(s: str, t: str) -> int:
    n, m = len(s), len(t)

    def dfs(i: int, j: int) -> int:
        """
        i: 当前在 s 中的下标（从 0 开始）
        j: 当前在 t 中的下标
        返回：从 s[i:] 中挑选，使得能够匹配 t[j:] 的方案数
        """
        # 已经匹配完 t，说明找到一种合法子序列
        if j == m:
            return 1
        # s 已经用完但 t 还没匹配完，说明此路不通
        if i == n:
            return 0

        # 方案1：跳过 s[i]
        cnt = dfs(i + 1, j)

        # 方案2：如果 s[i] 与 t[j] 相等，选取它
        if s[i] == t[j]:
            cnt += dfs(i + 1, j + 1)

        return cnt

    return dfs(0, 0)
```

#### 复杂度

- **时间复杂度**：O(2ⁿ) —— 解释：每个字符都有两条分支（选或不选），所以总的递归树节点数是 2 的 n 次方，随着 `n` 增大会非常快地爆炸。
- **空间复杂度**：O(n) —— 解释：递归栈的最大深度等于 `s` 的长度 `n`，只要保存函数调用的局部变量即可。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈在于大量重复计算**：  
- 当我们在不同的递归路径上，可能会多次进入相同的 `(i, j)` 状态（比如同样的 `s` 剩余部分和同样的 `t` 剩余部分），但每次都重新遍历，造成指数级的时间。

**动态规划（Dynamic Programming，DP）**的核心思想是**把子问题的答案记下来，后面直接使用**，避免重复计算。  
这里的子问题自然是：“使用 `s` 的前 `i` 个字符，能组成 `t` 的前 `j` 个字符的方案数”。记作 `dp[i][j]`。

**状态转移**  
1. **不使用第 i 个字符**：`dp[i-1][j]`（仍然用前 `i-1` 个字符匹配 `t` 的前 `j` 个字符）。  
2. **使用第 i 个字符**：只有当 `s[i-1] == t[j-1]` 时才可能，用 `dp[i-1][j-1]`（前 `i-1` 个字符匹配前 `j-1` 个字符，再把 `s[i-1]` 与 `t[j-1]` 配对）。

于是：
```
dp[i][j] = dp[i-1][j]                     # 跳过 s[i-1]
if s[i-1] == t[j-1]:
    dp[i][j] += dp[i-1][j-1]              # 使用 s[i-1]
```

**边界**  
- 空的 `t`（`j == 0`）可以被任何子序列匹配，只有一种方式：全部“跳过”。所以 `dp[i][0] = 1`。  
- 空的 `s`（`i == 0`）且 `t` 非空时，显然不可能匹配，`dp[0][j] = 0`（`j > 0`）。

**空间优化**  
观察公式，只和 `dp[i-1][*]`（上一行）有关。我们可以用**一维数组** `dp[j]` 逐行更新。为了保证 `dp[j-1]` 仍然是上一行的值，需要**从右向左**遍历 `j`（即大 `j` 先算），防止被本行已经更新的值覆盖。

**类比**  
把 `dp` 想象成一本“配对手册”，`dp[i][j]` 就是“用前 i 本书配对前 j 章节的方案数”。我们一次翻一本书（遍历 `s`），更新手册中所有章节的配对方式。

#### 代码（Python）

```python
def numDistinct(s: str, t: str) -> int:
    n, m = len(s), len(t)

    # dp[j] 表示使用已经遍历过的 s 前缀，匹配 t 前 j 个字符的方案数
    dp = [0] * (m + 1)
    dp[0] = 1                     # 空的 t 只能有一种匹配方式

    for i in range(1, n + 1):     # 遍历 s 的每个字符（从 1 开始，方便对应 s[i-1]）
        # 必须从右往左遍历 j，防止 dp[j-1] 已被本轮更新
        for j in range(m, 0, -1):
            if s[i - 1] == t[j - 1]:
                dp[j] += dp[j - 1]   # 把“使用 s[i-1] 配对 t[j-1]”的方案加进来
        # 注意：dp[0] 始终保持 1，不需要在循环里改动

    return dp[m]                    # 最终答案：使用全部 s 匹配全部 t 的方案数
```

#### 复杂度

- **时间复杂度**：O(n·m) —— 解释：外层遍历 `s`（长度 `n`），内层遍历 `t`（长度 `m`），每次只做 O(1) 的加法。对 `n,m ≤ 1000` 完全可接受。
- **空间复杂度**：O(m) —— 解释：只用了一个长度为 `m+1` 的一维数组，和 `t` 的长度成线性关系，显著节约了原本二维表的 `n·m` 空间。

---

## 心得

- **核心技巧**：把“子序列计数”转化为 **二维/一维动态规划**，利用“是否使用当前字符”两种状态的转移。
- **适用的题型**  
  1. **不同的子序列计数**（如 LeetCode 1155 `Number of Dice Rolls With Target Sum` 的思路类似）。  
  2. **编辑距离/最小操作数**（如 LeetCode 72 `Edit Distance`，同样使用 dp[i][j] 表示前缀匹配）。  
  3. **最长公共子序列**（LeetCode 1143 `Longest Common Subsequence`，状态转移几乎相同，只是取 `max` 而不是 `+`）。

- **一句话总结**：**把“选或不选”写成递推式，用 DP 把指数级的枚举压缩到多项式时间**。

---

## 反思

- **第一反应**：直接想要把所有子序列列举出来，写递归/回溯。  
- **最容易踩的坑**  
  1. **指数爆炸**：暴力递归在 `n=1000` 时根本不可跑。  
  2. **状态转移写错**：忘记 `dp[i][j]` 包含“跳过当前字符”的情况，只写了匹配时的加法，导致计数不完整。  
  3. **一维压缩的遍历顺序**：如果从左往右更新 `dp[j]`，会把本轮已经更新的 `dp[j-1]` 当成上一行的值，导致结果错误。  

- **下次遇到同类题**：第一步先**明确子问题**（前缀匹配多少方案），写出 **递推关系**，然后判断是否可以 **空间压缩**（一维 DP）。这样可以快速从“暴力想法”跳到 “动态规划” 的解法。