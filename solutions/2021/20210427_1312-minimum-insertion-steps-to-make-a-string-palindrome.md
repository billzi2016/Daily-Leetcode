# #1312. 使字符串成为回文的最少插入步数 / Minimum Insertion Steps to Make a String Palindrome

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/)

---

## 题目（英文原版）

**Description**

Given a string s. In one step you can insert any character at any index of the string.
Return the minimum number of steps to make s palindrome.
A Palindrome String is one that reads the same backward as well as forward.

**Examples**

**Example 1:**

```
Input: s = "zzazz"
Output: 0
Explanation: The string "zzazz" is already palindrome we do not need any insertions.
```

**Example 2:**

```
Input: s = "mbadm"
Output: 2
Explanation: String can be "mbdadbm" or "mdbabdm".
```

**Example 3:**

```
Input: s = "leetcode"
Output: 5
Explanation: Inserting 5 characters the string becomes "leetcodocteel".
```

**Constraints**

- 1 <= s.length <= 500
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`。在一次操作中，你可以在字符串的任意位置插入任意字符。返回使 `s` 成为回文字符串（Palindrome String）的最少操作次数。

回文字符串（Palindrome String）是指正读和反读完全相同的字符串。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

---

**示例 1**  
``` 
Input: s = "zzazz"
Output: 0
Explanation: The string "zzazz" is already palindrome we do not need any insertions.
```  
解释：字符串 `"zzazz"` 已经是回文，不需要任何插入。

**示例 2**  
``` 
Input: s = "mbadm"
Output: 2
Explanation: String can be "mbdadbm" or "mdbabdm".
```  
解释：可以将字符串构造成 `"mbdadbm"` 或 `"mdbabdm"`，只需插入 2 个字符。

**示例 3**  
``` 
Input: s = "leetcode"
Output: 5
Explanation: Inserting 5 characters the string becomes "leetcodocteel".
```  
解释：插入 5 个字符后，字符串可以变为 `"leetcodocteel"`，此时为回文。

**约束条件**  
- `1 <= s.length <= 500`  
- `s` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**穷举所有可能的插入方式**，看哪一种能最先得到回文。  
可以把这个过程想象成：

- 把原字符串看成一排字母的“拼图”。  
- 每一次插入，就在任意空位插入一块新字母的“拼图”。  
- 只要最终拼出的整排字母正着读和反着读一样，就算成功。

于是我们可以用递归（或回溯）模拟：  
1. 判断当前字符串是否已经是回文（相当于查字典，直接比较首尾）。  
2. 若不是，则在左侧或右侧各插入一个字符，使得两端字符相等，然后继续递归。  
3. 记录下所有递归路径中插入字符的最少次数。

这种方法一定能得到正确答案，因为它把**所有可能的插入序列**都遍历了一遍。  

但是，这里有两个致命的瓶颈：

- 每一步都有 **O(n)** 种插入位置（在每个字符之间都可以插），递归深度最坏是 **O(n)**，所以总的搜索树规模是 **O(nⁿ)**，会爆炸。  
- 判断回文本身是 **O(n)**，在巨大的搜索树里反复做，会让时间更不可接受。

因此，这种暴力方法只能在非常小的输入（比如长度 ≤ 5）时勉强跑得动，实际面对 1 ≤ |s| ≤ 500 的约束根本不可能。

#### 代码（Python）  
```python
def minInsertions_brute(s: str) -> int:
    """暴力递归解法（仅作思路演示，实际会超时）"""

    def is_palindrome(t: str) -> bool:
        # 判断 t 是否回文：从两头向中间比较
        return t == t[::-1]

    from functools import lru_cache

    @lru_cache(None)                     # 记忆化，避免完全重复的子问题
    def dfs(t: str) -> int:
        if is_palindrome(t):              # 已经是回文，不需要再插入
            return 0
        n = len(t)
        best = float('inf')
        # 在每两个字符之间（包括首尾）尝试插入，使两端字符相等
        for i in range(n + 1):            # 插入位置有 n+1 种
            # 插入字符使左侧字符与右侧字符匹配（两种可能）
            # 这里我们只示意一种：在 i 位置插入 t[n-1-i]，实际会尝试所有字符
            # 为了保持思路简洁，这里不展开所有字符的遍历
            # 直接递归求解（会产生指数级递归）
            # 示例：在左边插入 t[-1]，在右边插入 t[0] 等等
            # 下面的实现仅作占位，实际不建议使用
            pass
        return best

    return dfs(s)
```
> **注意**：上述代码中 `pass` 处本应遍历所有可能的字符并递归求解，完整实现会导致指数级时间，已被省略，仅用于说明“暴力思路”。  

#### 复杂度  
- 时间复杂度：**O(2ⁿ)**（指数级）——每一步可能在左、右两侧各插入，递归深度最坏是 n，导致搜索树节点数呈指数增长。  
- 空间复杂度：**O(n)**（递归栈深度）——递归最多会深入 n 层。

> 大白话：如果字符串长 20，2ⁿ 已经是 1 048 576；长度 30 时就已经是 **十亿级**，根本跑不完。

---

### 2. 最优解  

#### 思路  
从暴力解我们知道，**插入的本质是把原串的字符重新排列成回文**，只是不允许删除字符，只能在合适的位置补足缺失的匹配字符。  
所以，**不需要真的去模拟每一次插入**，只要知道已有字符中已经能组成多大的回文子序列（不要求连续），其余的字符就必须通过插入来配对。

> **关键点**：  
> - **最长回文子序列（Longest Palindromic Subsequence，LPS）** 的长度记为 `x`。  
> - 原串长度是 `n`。  
> - 那么我们只需要把剩下的 `n - x` 个字符“配对”，每配对一次需要插入一个字符。  
> - 因此 **最少插入次数 = n - LPS**。

于是问题转化为**求 LPS 长度**。  

##### 如何求 LPS？  
两种常见方法：

1. **把 LPS 看成原串和它的逆串的最长公共子序列（LCS）**。  
   - 把字符串 `s` 逆序得到 `rev = s[::-1]`。  
   - 在 `s` 与 `rev` 中找到最长的公共子序列，这恰好就是 `s` 的最长回文子序列。  
   - 这是一种 **二维动态规划**（DP）做法，时间 O(n²)，空间 O(n²)（或 O(n) 优化）。

2. **直接在同一串上做区间 DP**。  
   - 设 `dp[i][j]` 为子串 `s[i…j]` 的 LPS 长度。  
   - 状态转移：
     - 若 `s[i] == s[j]`，则这两个字符可以放在回文的两端，`dp[i][j] = dp[i+1][j-1] + 2`（注意 `i==j` 时是 1）。
     - 否则只能把左端或右端舍弃，取较大值：`dp[i][j] = max(dp[i+1][j], dp[i][j-1])`。  
   - 初始化：所有长度为 1 的子串 `dp[i][i] = 1`。  
   - 按子串长度从小到大填表。

这里我们采用第二种 **区间 DP**，因为它直接对应“在原串内部找回文子序列”，逻辑更直观。

> **类比**：想象有一排座位（字符），我们要挑选出最多的同学坐成对称的两边。  
> - 若两端同学相同，就把他们配对（+2）。  
> - 若不同，就把左边或右边的同学先暂时“让座”，看哪种选择能留下更多配对（取 max）。

##### 空间优化  
`dp[i][j]` 只依赖 `dp[i+1][j-1]`、`dp[i+1][j]`、`dp[i][j-1]`，可以只保留上一行和当前行，进而把空间降到 **O(n)**。这里先给出完整的二维表实现，随后展示压缩版。

#### 代码（Python）  

**① 区间 DP（二维表）**  
```python
def minInsertions(s: str) -> int:
    """
    动态规划求最长回文子序列长度，进而得到最少插入次数。
    时间复杂度 O(n²)，空间复杂度 O(n²)。
    """
    n = len(s)
    # dp[i][j] 表示子串 s[i..j] 的最长回文子序列长度
    dp = [[0] * n for _ in range(n)]

    # 所有长度为 1 的子串本身就是回文，长度为 1
    for i in range(n):
        dp[i][i] = 1

    # 按子串长度从短到长填表
    for length in range(2, n + 1):          # 子串长度
        for i in range(n - length + 1):     # 左端起点
            j = i + length - 1              # 右端终点
            if s[i] == s[j]:                # 两端字符相等，可配对
                if length == 2:             # 特殊情况：仅两个字符且相等
                    dp[i][j] = 2
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
            else:                           # 两端不相等，舍弃左或右
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    lps_len = dp[0][n - 1]                  # 整个字符串的 LPS 长度
    return n - lps_len                      # 最少插入次数
```

**② 空间压缩版（只用 O(n) 额外空间）**  
```python
def minInsertions_opt(s: str) -> int:
    """
    使用滚动数组把空间降到 O(n)。
    仍然是 O(n²) 时间。
    """
    n = len(s)
    # prev 保存 dp[i+1][*]，curr 保存 dp[i][*]
    prev = [0] * n
    curr = [0] * n

    for i in range(n - 1, -1, -1):          # 从右往左遍历左端
        curr[i] = 1                         # dp[i][i] = 1
        for j in range(i + 1, n):           # 右端从 i+1 向右
            if s[i] == s[j]:
                curr[j] = prev[j - 1] + 2   # dp[i+1][j-1] + 2
            else:
                curr[j] = max(prev[j], curr[j - 1])  # max(dp[i+1][j], dp[i][j-1])
        # 交换角色，准备计算下一行
        prev, curr = curr, [0] * n

    lps_len = prev[n - 1]                   # 最后一次循环后 prev 即为 dp[0][*]
    return n - lps_len
```

> **代码要点注释**：  
> - `dp[i][j]` 只在 `i ≤ j` 时有意义，左上三角可以不管。  
> - `length == 2` 时若两字符相同，直接设为 2，避免访问 `dp[i+1][j-1]` 越界。  
> - 在压缩版里，`prev` 保存的是上一轮（`i+1`）对应的整行，`curr` 正在计算当前行。

#### 复杂度  
- **时间复杂度**：**O(n²)** — 需要遍历所有 `i, j` 组合（约 n²/2 次），每次只做常数操作。  
  - 大白话：如果字符串长 500，最多会算 250 000 次，现代电脑几毫秒就能搞定。  
- **空间复杂度**：  
  - 完整表：**O(n²)**（约 250 000 个整数，约 2 MB，仍在可接受范围）。  
  - 压缩版：**O(n)**（只用两行数组，约 500 个整数）。  
  - 与暴力解相比，空间和时间都从指数级下降到多项式级，足以通过所有测试。

---

## 心得  

- **核心技巧**：把“最少插入使回文”转化为“原串的最长回文子序列”。  
- **适用场景**：  
  1. **删除字符使回文**（最少删除次数 = n - LPS）。  
  2. **求最少编辑次数让两串相同**（编辑距离 DP），思路相似。  
  3. **最长回文子序列本身**的直接求解（如 LeetCode 516）。  
- **一句话总结**：**“先找出已经能配对的字符（LPS），剩下的全靠插入”**。

---

## 反思  

- **第一反应**：直接想“把缺的字符补上”，于是想到暴力枚举所有插入位置。  
- **最容易踩的坑**：  
  - 忘记 **“最长回文子序列”** 与 **“最少插入次数”** 之间的等价关系，导致在实现时仍然在插入层面循环。  
  - DP 边界处理不当（如 `i+1 > j-1`），会出现负索引或未初始化的情况。  
  - 在压缩空间时忘记在每轮循环后重置 `curr`，导致残留旧值干扰计算。  
- **下次类似题**：  
  1. 首先问自己“有没有已经满足需求的子结构”，比如 **最长公共子序列 / 最长回文子序列**。  
  2. 再思考 **“缺失的部分需要多少操作”**，往往可以用 **总长度 - 已有最优子结构长度** 得到答案。  

祝你玩转 DP，轻松写出最优解！