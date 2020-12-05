# #1092. 最短公共超序列 / Shortest Common Supersequence 

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/shortest-common-supersequence/)

---

## 题目（英文原版）

**Description**

Given two strings str1 and str2, return the shortest string that has both str1 and str2 as subsequences. If there are multiple valid strings, return any of them.
A string s is a subsequence of string t if deleting some number of characters from t (possibly 0) results in the string s.

**Examples**

**Example 1:**

```
Input: str1 = "abac", str2 = "cab"
Output: "cabac"
Explanation: 
str1 = "abac" is a subsequence of "cabac" because we can delete the first "c".
str2 = "cab" is a subsequence of "cabac" because we can delete the last "ac".
The answer provided is the shortest such string that satisfies these properties.
```

**Example 2:**

```
Input: str1 = "aaaaaaaa", str2 = "aaaaaaaa"
Output: "aaaaaaaa"
```

**Constraints**

- 1 <= str1.length, str2.length <= 1000
- str1 and str2 consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `str1` 和 `str2`，返回一个最短的字符串，使得 `str1` 和 `str2` 都是该字符串的子序列（subsequence）。如果存在多个满足条件的最短字符串，返回任意一个即可。  

子序列（subsequence）的定义：如果通过删除字符串 `t` 中任意数量（可能为 0）的字符后得到字符串 `s`，则 `s` 是 `t` 的子序列。

**示例 1**  
**输入**: `str1 = "abac", str2 = "cab"`  
**输出**: `"cabac"`  
**解释**:  
- `str1 = "abac"` 是 `"cabac"` 的子序列，因为我们可以删除第一个字符 `"c"`。  
- `str2 = "cab"` 是 `"cabac"` 的子序列，因为我们可以删除最后的 `"ac"`。  
该答案是满足上述属性的最短字符串。

**示例 2**  
**输入**: `str1 = "aaaaaaaa", str2 = "aaaaaaaa"`  
**输出**: `"aaaaaaaa"`

**约束条件**  
- `1 <= str1.length, str2.length <= 1000`  
- `str1` 和 `str2` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两条字符串都“穿进去”，把所有可能的交叉方式全部枚举出来，挑最短的那一个**。  
可以把这个过程想象成把两根绳子（`str1`、`str2`）交叉编织，任意时刻可以把一根绳子的下一个字符接在结果串的后面，只要最终这两根绳子都完整出现（即它们都是结果的子序列）即可。  

实现上可以用递归：

1. 设指针 `i` 指向 `str1` 当前要放的字符，指针 `j` 指向 `str2` 当前要放的字符。  
2. 若 `i` 已经到达 `str1` 末尾，则只把 `str2[j:]` 直接接在后面；同理 `j` 到末尾时只接 `str1[i:]`。  
3. 否则比较 `str1[i]` 与 `str2[j]`：  
   - 若相等，我们可以一次性把这个字符放进去，同时把 `i`、`j` 都向前移动一位（因为这个字符已经为两条绳子都贡献了一次）。  
   - 若不相等，我们必须在结果中保留两种可能：  
     * 把 `str1[i]` 放进去，然后递归求解 `(i+1, j)`；  
     * 把 `str2[j]` 放进去，然后递归求解 `(i, j+1)`。  
   取两种递归返回的最短字符串即可。  

这就是**完全搜索**（brute force）的思路。它保证一定能找到最短的公共超序列，因为我们枚举了所有合法的拼接方式。

> **类比**：把哈希表想成查字典，`key` 是词，`value` 是页码；这里的递归就像在一棵无限大的“决策树”里走遍每一条可能的路径，最后挑最短的那条。

#### 代码（Python）

```python
def shortest_common_supersequence_bruteforce(str1: str, str2: str) -> str:
    from functools import lru_cache

    @lru_cache(maxsize=None)                 # 记忆化，防止重复计算同一个 (i,j)
    def dfs(i: int, j: int) -> str:
        # 如果一条已经遍历完，只剩另一条未处理的后缀
        if i == len(str1):
            return str2[j:]                  # 直接把剩余的字符接上
        if j == len(str2):
            return str1[i:]

        # 两个当前字符相等，只需要写一次
        if str1[i] == str2[j]:
            return str1[i] + dfs(i + 1, j + 1)

        # 不相等，分别尝试把 str1[i] 或 str2[j] 放进答案
        opt1 = str1[i] + dfs(i + 1, j)        # 先放 str1 的字符
        opt2 = str2[j] + dfs(i, j + 1)        # 先放 str2 的字符

        # 取长度更短的那个；如果相等随便返回一个
        return opt1 if len(opt1) < len(opt2) else opt2

    return dfs(0, 0)
```

> 关键点注释已在代码中，用中文解释每一步的含义。

#### 复杂度

- **时间复杂度**：`O(2^{m+n})`（指数级）  
  大白话：如果两条绳子各有 `m`、`n` 个字符，最坏情况下每一步都要分两路走，树的深度是 `m+n`，所以可能的路径数是 `2^{m+n}`，这远远超过几千甚至几百万，计算机会卡死。

- **空间复杂度**：`O(m+n)`（递归栈深度）  
  只需要保存递归调用的层数，最深不超过两条字符串的总长度。

> 由于指数级时间，暴力解只能用来验证思路或在极小输入下测试，实际提交会超时。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次字符不相等时都要分叉**，导致指数级的搜索树。  
如果我们能够 **提前知道哪些字符是必须共享的，哪些可以省掉一次写入**，就能大幅削减分叉的次数。  

这正是 **最长公共子序列（LCS）** 的用武之地：

- **LCS**：在两条字符串中挑出最长的公共子序列。  
- 为什么 LCS 有帮助？  
  - 这段公共子序列的字符 **可以只写一次**，因为它们在 `str1`、`str2` 中都出现，放在结果里一次就能满足两条子序列的需求。  
  - 其余不在 LCS 中的字符必须各自出现一次（否则对应的原字符串就会缺字符）。  

因此，**最短公共超序列（SCS）的长度 = |str1| + |str2| - |LCS|**。  
构造过程：

1. **先求 LCS** 的长度以及它的具体字符序列。使用动态规划（DP）完成，时间 `O(m·n)`，空间 `O(m·n)`（也可以压缩到 `O(min(m,n))`，但这里为了后续回溯保留完整表格更直观）。  
2. **根据 LCS 重新合并** 两个字符串：  
   - 用两个指针 `i`、`j` 分别遍历 `str1`、`str2`。  
   - 逐字符对比 LCS 中的下一个字符 `c`：  
     * 把 `str1[i]` 中所有在 `c` 之前的字符（即不在 LCS 里）加入答案，并移动 `i`。  
     * 把 `str2[j]` 中所有在 `c` 之前的字符加入答案，并移动 `j`。  
     * 当两边都到达字符 `c` 时，只把 `c` 加一次，然后 `i`、`j` 同时向前一步（跳过 LCS 中的这段）。  
   - 最后把 `i`、`j` 余下的尾部全部加进答案。  

这样我们只在 **LCS 的每个字符出现一次**，其余字符各自出现一次，正好得到最短公共超序列。

> **类比**：把 LCS 想成两条绳子共同的“金链环”。在编织时，金链环只需要挂一次；其余普通链环（不相同的字符）各自挂一次。这样整个链子最短。

#### 代码（Python）

```python
def shortest_common_supersequence(str1: str, str2: str) -> str:
    m, n = len(str1), len(str2)

    # ---------- 1. DP 求 LCS ----------
    # dp[i][j] 表示 str1[:i] 与 str2[:j] 的最长公共子序列长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1      # 两字符相等，长度加 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # 取较大的子问题

    # ---------- 2. 根据 DP 表回溯得到 LCS 本身 ----------
    i, j = m, n
    lcs_chars = []          # 用列表收集 LCS，随后会反转
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            lcs_chars.append(str1[i - 1])   # 当前字符是 LCS 的一部分
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs = ''.join(reversed(lcs_chars))      # 正序的最长公共子序列

    # ---------- 3. 依照 LCS 合并得到最短公共超序列 ----------
    ans = []
    i = j = 0
    for c in lcs:
        # 把 str1 中在 c 之前的字符全部加入答案
        while i < m and str1[i] != c:
            ans.append(str1[i])
            i += 1
        # 把 str2 中在 c 之前的字符全部加入答案
        while j < n and str2[j] != c:
            ans.append(str2[j])
            j += 1
        # 当前字符 c 本身只加一次
        ans.append(c)
        i += 1   # 跳过已匹配的 c
        j += 1

    # 把剩余的尾部字符全部加进去
    ans.append(str1[i:])
    ans.append(str2[j:])

    return ''.join(ans)
```

> 代码中每一段都有中文注释，帮助读者快速定位思路。

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - DP 填表遍历 `m·n` 个格子，每格 O(1) 操作。  
  - 回溯 LCS、合并过程均是线性扫描 `O(m + n)`，不影响主导项。  
  与暴力解的指数级 `O(2^{m+n})` 相比，**快了很多**，即使 `m,n` 达到 1000 也能毫秒级完成。

- **空间复杂度**：`O(m·n)`  
  - 需要保存 DP 表格，大小为 `(m+1)*(n+1)`。  
  - 如果仅关心长度而不需要实际序列，可以把空间压缩到 `O(min(m,n))`，但为了演示回溯，这里保留完整表格，仍然在题目给定的 1000 上限内完全可接受。

---

## 心得

- **核心技巧**：先求最长公共子序列（LCS），再利用 LCS 把两条字符串“有序合并”。  
- **适用的题型**  
  1. **最短公共超序列**（本题）。  
  2. **构造最小的合并字符串**（如把两个序列合并成字典序最小的字符串）。  
  3. **在两条序列中插入最少字符使之相等**（相当于 SCS 的逆向思考）。  
- **一句话总结**：**找出两串共同的最长子序列，只有这部分可以共享一次，其他字符各自出现一次，即得到最短公共超序列。**

---

## 反思

- **第一反应**：把两串交叉拼接、枚举所有可能（暴力搜索）。  
- **最容易踩的坑**  
  - 忘记在 LCS 回溯时同时移动两个指针，导致产生错误的公共子序列。  
  - 合并时忘记把 LCS 之后的剩余字符加入答案，结果会缺字符。  
  - 对于空字符串的边界没有专门处理，会出现 `IndexError`。  
- **下次遇到同类题**：第一步先思考“有没有可以共享的部分？”——若有，往往是 **最长公共子序列 / 最长公共前缀 / 最长公共子数组** 之类的结构；随后再把共享部分“扣除”，把剩余部分直接拼接。这样可以把指数级的暴力搜索压缩到多项式时间。