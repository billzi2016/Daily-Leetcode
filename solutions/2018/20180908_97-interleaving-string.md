# #97. 交错字符串 / Interleaving String

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/interleaving-string/)

---

## 题目（英文原版）

**Description**

Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.
An interleaving of two strings s and t is a configuration where s and t are divided into n and m substrings respectively, such that:
Note: a + b is the concatenation of strings a and b.
Follow up: Could you solve it using only O(s2.length) additional memory space?

**Examples**

**Example 1:**

```
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true
Explanation: One way to obtain s3 is:
Split s1 into s1 = "aa" + "bc" + "c", and s2 into s2 = "dbbc" + "a".
Interleaving the two splits, we get "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".
Since s3 can be obtained by interleaving s1 and s2, we return true.
```

**Example 2:**

```
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: false
Explanation: Notice how it is impossible to interleave s2 with any other string to obtain s3.
```

**Example 3:**

```
Input: s1 = "", s2 = "", s3 = ""
Output: true
```

**Constraints**

- 0 <= s1.length, s2.length <= 100
- 0 <= s3.length <= 200
- s1, s2, and s3 consist of lowercase English letters.

---

## 题目（中文翻译）

给定字符串 `s1`、`s2` 和 `s3`，判断 `s3` 是否可以由 `s1` 与 `s2` 的交错（interleaving）形成。  

两个字符串 `s` 与 `t` 的交错是一种配置：将 `s` 与 `t` 分别划分为若干子字符串（substrings），记为 `s = s₁ + s₂ + … + sₙ`、`t = t₁ + t₂ + … + tₘ`，并满足：

- `n` 与 `m` 可以不同；
- 交错后得到的字符串为 `s₁ + t₁ + s₂ + t₂ + …`（即交替地把两侧的子字符串连接（concatenation）起来），其整体顺序保持不变。

如果能够通过上述方式得到 `s3`，则返回 `true`，否则返回 `false`。

**示例 1**  
```
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true
Explanation: 获取 `s3` 的一种方法是：
将 `s1` 划分为 "aa" + "bc" + "c"，将 `s2` 划分为 "dbbc" + "a"。  
交错这两段划分后得到 "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac"。  
因为 `s3` 可以由 `s1` 与 `s2` 的交错得到，所以返回 `true`。
```

**示例 2**  
```
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: false
Explanation: 可以发现没有办法将 `s2` 与任意其他字符串交错得到 `s3`，因此返回 `false`。
```

**示例 3**  
```
Input: s1 = "", s2 = "", s3 = ""
Output: true
```

**约束条件**  

- `0 <= s1.length, s2.length <= 100`
- `0 <= s3.length <= 200`
- `s1、s2、s3` 只包含小写英文字母。

**进阶**：能否只使用 `O(s2.length)` 的额外内存空间来解决此问题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的交叉方式**，把 `s1` 与 `s2` 的字符按照顺序插入到一起，看看能否得到 `s3`。  
我们可以用递归来实现：每次看 `s3` 的当前字符到底是来自 `s1` 还是 `s2`，如果匹配就往下走，否则回溯。

- **使用的数据结构**：递归调用栈（相当于我们手里的一本“记事本”，每翻一页就记录一次选择）。  
- **生活化类比**：把 `s1` 想成一本只写“A”的笔记本，`s2` 想成一本只写“B”的笔记本，`s3` 是一本混合了两本笔记的成品。我们要一步步检查每页（字符）到底是从哪本笔记本抄来的。

**为什么这个方法正确**  
递归会尝试**所有**合法的取字符顺序，只要有一种取法能把 `s3` 完全匹配，就返回 `True`。如果所有取法都失败，则返回 `False`。

#### 代码（Python）

```python
def isInterleave_brute(s1: str, s2: str, s3: str) -> bool:
    # 长度不相等，直接否定
    if len(s1) + len(s2) != len(s3):
        return False

    # 记忆化缓存，防止重复子问题（没有也算是最原始的暴力）
    from functools import lru_cache

    @lru_cache(None)                     # 把已经算过的 (i,j) 结果记下来
    def dfs(i: int, j: int) -> bool:
        """
        i: 已经使用了 s1 前 i 个字符
        j: 已经使用了 s2 前 j 个字符
        """
        # 已经匹配到 s3 的末尾，说明前面的选择全部成功
        if i == len(s1) and j == len(s2):
            return True

        # 当前要匹配的 s3 的位置是 i + j
        k = i + j

        # 尝试从 s1 取字符（如果还有剩余且字符相等）
        if i < len(s1) and s1[i] == s3[k]:
            if dfs(i + 1, j):              # 递归往下走
                return True

        # 尝试从 s2 取字符（如果还有剩余且字符相等）
        if j < len(s2) and s2[j] == s3[k]:
            if dfs(i, j + 1):
                return True

        # 两条路都走不通，返回 False
        return False

    return dfs(0, 0)
```

#### 复杂度

- **时间复杂度**：`O(2^{m+n})`（指数级）  
  大白话：每一步都有两条可能的路（从 `s1` 取或从 `s2` 取），最坏情况下会把所有组合都试一遍，组合数会像翻倍一样快速增长。

- **空间复杂度**：`O(m+n)`（递归栈深度）  
  这里的 `m = len(s1)`，`n = len(s2)`。递归最多会走 `m+n` 层，栈里保存的每层信息占用常数空间。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**重复子问题**是导致指数时间的根本原因。  
在递归过程中，只要知道已经使用了 `s1` 的前 `i` 个字符和 `s2` 的前 `j` 个字符，后面的判断总是一样的。于是我们可以把「是否能匹配」的结果保存下来，避免二次计算，这就是**动态规划（Dynamic Programming, DP）**的核心思想。

**慢在哪里**  
- 暴力解每次都要重新检查相同的 `(i, j)` 状态。  
- 递归栈会占用额外的函数调用开销。

**优化思路**  
1. 建立一个二维布尔表 `dp[i][j]`，表示：**使用 `s1` 前 `i` 个字符和 `s2` 前 `j` 个字符，能否拼出 `s3` 前 `i+j` 个字符**。  
2. 初始化：`dp[0][0] = True`（空串能拼成空串）。  
3. 转移方程：  
   - 如果 `dp[i-1][j]` 为 `True` 且 `s1[i-1] == s3[i+j-1]`，说明可以把 `s1` 的第 `i` 个字符接在已有的交错串后面，`dp[i][j] = True`。  
   - 同理，如果 `dp[i][j-1]` 为 `True` 且 `s2[j-1] == s3[i+j-1]`，也可以把 `s2` 的第 `j` 个字符接在后面。  
4. 最终答案是 `dp[len(s1)][len(s2)]`。

**空间优化**  
注意到 `dp[i][j]` 只和同一行的左侧 `dp[i][j-1]`、上一行的同列 `dp[i-1][j]` 有关。我们可以只保留一行（或一列），滚动更新即可，把空间降到 `O(min(m,n))`。这里演示保留 `s2` 长度的一行。

**核心概念解释**  
- **动态规划**：把大问题拆成小子问题，先求解小的、容易的子问题，然后把答案拼起来得到大问题的答案。  
- **状态**：这里的状态就是「已经用了 `s1` 前多少字符，`s2` 前多少字符」。  
- **转移**：从已有的状态推导出新状态的规则。

#### 代码（Python）

```python
def isInterleave_dp(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)

    # 长度不匹配直接返回 False
    if m + n != len(s3):
        return False

    # 为了使用 O(min(m,n)) 空间，确保 s2 是较短的那个
    if n > m:                     # 交换，让 s2 成为较短的字符串
        s1, s2 = s2, s1
        m, n = n, m

    # dp[j] 表示使用 s1 前 i 个字符和 s2 前 j 个字符是否能匹配 s3 前 i+j 个字符
    dp = [False] * (n + 1)
    dp[0] = True                  # 空空能匹配空

    # 初始化第一行（i = 0，只用 s2）
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    # 开始遍历 s1（外层）和 s2（内层）
    for i in range(1, m + 1):
        # 更新 dp[0]，只用 s1 的情况
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]

        for j in range(1, n + 1):
            # 两个来源：上面 (i-1,j) 或左边 (i,j-1)
            from_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]   # 这里的 dp[j] 仍是上一行的值
            from_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
            dp[j] = from_s1 or from_s2

    return dp[n]
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  大白话：我们需要检查每一对 `(i, j)`，总共 `m*n` 次，和字符个数的乘积成正比。相比暴力的指数级，这已经是线性乘积的快速度了。

- **空间复杂度**：`O(min(m, n))`  
  只用了长度较短的字符串对应的一维数组，省掉了完整的二维表。相当于只需要记住“一行”信息，像只用一本小笔记本记要点。

---

## 心得

- **核心技巧**：把“交错拼接”转化为**二维状态 DP**，并利用**状态转移**判断字符来源。  
- **适用的题型**：  
  1. “是否能从两个序列交错得到目标序列”——如 *Interleaving String*。  
  2. “两个序列的公共子序列长度”——*Longest Common Subsequence*（同样使用二维 DP）。  
  3. “背包类的是否可达问题”——*Partition Equal Subset Sum*（布尔 DP）。  
- **一句话总结**：**把每一步的“来源”记下来，避免重复搜索**。

## 反思

- **第一反应**：看到“交错”二字，我会先想递归穷举，因为它最直观。  
- **最容易踩的坑**：  
  - 忘记先检查 `len(s1) + len(s2) == len(s3)`，导致后面 DP 越界。  
  - 在空间优化版里，更新 `dp[j]` 时必须先使用上一行的值（即 `from_s1` 使用旧的 `dp[j]`），否则会把信息覆盖掉。  
- **下次第一步**：先判断长度是否匹配，再写出**状态定义**（用 `dp[i][j]` 表示什么），再思考转移方程。这样可以快速定位是否可以用 DP，避免盲目递归。