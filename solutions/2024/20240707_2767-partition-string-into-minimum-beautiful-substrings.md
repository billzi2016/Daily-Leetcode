# #2767. **将字符串划分为最少的美丽子字符串** / Partition String Into Minimum Beautiful Substrings

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming、Backtracking · [LeetCode 链接](https://leetcode.com/problems/partition-string-into-minimum-beautiful-substrings/)

---

## 题目（英文原版）

**Description**

Given a binary string s, partition the string into one or more substrings such that each substring is beautiful.
A string is beautiful if:
Return the minimum number of substrings in such partition. If it is impossible to partition the string s into beautiful substrings, return -1.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: s = "1011"
Output: 2
Explanation: We can paritition the given string into ["101", "1"].
- The string "101" does not contain leading zeros and is the binary representation of integer 51 = 5.
- The string "1" does not contain leading zeros and is the binary representation of integer 50 = 1.
It can be shown that 2 is the minimum number of beautiful substrings that s can be partitioned into.
```

**Example 2:**

```
Input: s = "111"
Output: 3
Explanation: We can paritition the given string into ["1", "1", "1"].
- The string "1" does not contain leading zeros and is the binary representation of integer 50 = 1.
It can be shown that 3 is the minimum number of beautiful substrings that s can be partitioned into.
```

**Example 3:**

```
Input: s = "0"
Output: -1
Explanation: We can not partition the given string into beautiful substrings.
```

**Constraints**

- 1 <= s.length <= 15
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个二进制字符串 `s`，将其划分为一个或多个子字符串（substring），要求每个子字符串都是**美丽**的。  
一个字符串如果满足以下条件，则称为**美丽**的：

- 不包含前导零（leading zeros），即如果字符串长度大于 1，则首字符必须为 `'1'`；
- 将其视为二进制数后，其整数值在 `[1, 5]` 区间内（即 `1 ≤ value ≤ 5`）。

返回能够完成上述划分的**最小子字符串数量**。如果无法将 `s` 划分成全部美丽子字符串，则返回 `-1`。  
子字符串是字符串中连续的字符序列。

---

**示例**

**示例 1**

```
输入: s = "1011"
输出: 2
解释: 我们可以将字符串划分为 ["101", "1"]。
- 子串 "101" 不含前导零，二进制表示的整数为 5，属于 [1,5]。
- 子串 "1"   不含前导零，二进制表示的整数为 1，属于 [1,5]。
可以证明，2 是能够划分得到的最小美丽子字符串数量。
```

**示例 2**

```
输入: s = "111"
输出: 3
解释: 我们可以将字符串划分为 ["1", "1", "1"]。
- 每个子串 "1" 都不含前导零，二进制整数为 1，属于 [1,5]。
可以证明，3 是能够划分得到的最小美丽子字符串数量。
```

**示例 3**

```
输入: s = "0"
输出: -1
解释: 无法将该字符串划分成任何美丽子字符串。
```

---

**约束条件**

- `1 <= s.length <= 15`
- `s[i]` 仅为 `'0'` 或 `'1'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的切分方式都枚举出来**，然后在每一种切分里检查每个子串是否「漂亮」，如果全部满足就记下切分得到的子串个数，最后取最小值。

- **枚举切分**：把字符串的每个位置看成「可以在这里切」还是「不切」。长度为 `n` 的字符串一共有 `2^(n‑1)` 种切法（每两个字符之间都有「切」或「不切」两种选择）。我们可以用递归（回溯）逐个尝试。
- **判断「漂亮」**：  
  1. 子串不能有前导零（即如果长度 > 1，首字符必须是 `'1'`），这就像查字典时要先看词的第一个字母是否符合要求。  
  2. 把二进制子串转成十进制整数 `x`，检查 `x` 是否是 5 的幂。判断 5 的幂可以像「把糖果分成 5 颗一堆」一样：只要 `x` 能一直被 5 整除到最后恰好剩 1，就说明它是 5 的幂。  
- **记录最小子串数**：在递归过程中，一旦发现当前切分已经用了 `cnt` 个子串且 `cnt` 已经不小于目前找到的最小答案，就可以提前剪枝，因为继续往下只会让子串数更大。

> **为什么暴力方法一定能得到答案？**  
> 因为我们把「所有可能的切分」都遍历了一遍，答案必然在其中。只要每一次判断「漂亮」的逻辑是正确的，最终得到的最小子串数就是题目要求的最优解。

#### 代码（Python）

```python
def beautiful_substrings_min(s: str) -> int:
    n = len(s)
    INF = float('inf')
    ans = INF                         # 用一个很大的数代表「尚未找到可行解」

    # ---------- 判断一个子串是否是「漂亮」 ----------
    def is_beautiful(sub: str) -> bool:
        # 不能有前导零，且长度必须大于 0
        if len(sub) > 1 and sub[0] == '0':
            return False
        # 把二进制转成十进制
        num = int(sub, 2)
        if num == 0:                   # 0 不是 5 的幂
            return False
        # 检查是否是 5 的幂
        while num % 5 == 0:
            num //= 5
        return num == 1                # 循环结束后恰好剩 1 才算是 5 的幂

    # ---------- 回溯枚举所有切分 ----------
    def dfs(idx: int, cnt: int) -> None:
        """从位置 idx 开始继续切分，已经用了 cnt 个子串"""
        nonlocal ans
        # 剪枝：已经比已知最小答案更差，直接返回
        if cnt >= ans:
            return
        # 所有字符都已经划分完
        if idx == n:
            ans = min(ans, cnt)
            return

        # 尝试把 s[idx:next_idx] 作为下一个子串
        for next_idx in range(idx + 1, n + 1):
            cur = s[idx:next_idx]
            if is_beautiful(cur):
                dfs(next_idx, cnt + 1)   # 继续往后划分

    dfs(0, 0)
    return -1 if ans == INF else ans
```

> 代码要点  
> - `int(sub, 2)` 把二进制直接转成十进制，省去了手动遍历位的过程。  
> - `while num % 5 == 0: num //= 5` 就像不断把糖果「每次取走 5 颗」直到剩不下 5 为止。  
> - `dfs` 中的 `for next_idx` 把「从当前位置往后选一个切点」的所有可能枚举出来。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - 共有 `2^(n‑1)` 种切法，每种切法在最坏情况下要检查 `n` 次子串是否「漂亮」(因为 `is_beautiful` 里会把子串转成整数，时间与子串长度成正比)。  
  - 对于 `n ≤ 15`，`2^15 = 32768`，完全可以接受。  
- **空间复杂度**：`O(n)`  
  - 递归栈的深度最多 `n`，另外存放字符串本身的空间不计入额外空间。

---

### 2. 最优解

#### 思路  

暴力解的「慢点」在于 **大量重复计算**：同一个前缀 `s[i:j]` 可能在不同的递归路径里被检查多次。我们可以把「从位置 i 开始，剩余最少需要多少个漂亮子串」的结果记下来，后面再遇到相同的 `i` 时直接复用——这正是 **动态规划（DP）** 的思想。

**步骤**：

1. **预处理所有「漂亮」子串**  
   - 对每个起点 `i`，枚举所有可能的终点 `j`（`i ≤ j < n`），判断 `s[i:j+1]` 是否漂亮，记录在 `good[i][j]` 中。  
   - 这一步的时间是 `O(n^2)`，因为 `n ≤ 15`，即使每次都做二进制转整数也没问题。

2. **定义 DP 状态**  
   - `dp[i]` 表示「从下标 `i` 开始切分，能够得到的最少子串数」。如果从 `i` 开始根本切不出漂亮子串，则 `dp[i] = INF`。  
   - 目标答案是 `dp[0]`。

3. **状态转移**  
   - 对每个起点 `i`，遍历所有终点 `j ≥ i`，如果 `good[i][j]` 为真（即 `s[i:j+1]` 是漂亮的），那么我们可以把这段当作第一个子串，剩下的部分从 `j+1` 开始。  
   - 于是 `dp[i] = min(dp[i], 1 + dp[j+1])`。这里的 `1` 表示已经使用了一个漂亮子串。  
   - 为了让 `dp[j+1]` 已经算好，我们从右往左（倒序）填表：先算 `dp[n] = 0`（空串不需要子串），再算 `dp[n‑1] … dp[0]`。

4. **返回结果**  
   - 如果 `dp[0]` 仍然是 `INF`，说明没有合法切分，返回 `-1`；否则返回 `dp[0]`。

> **核心数据结构**：  
> - **二维布尔数组 `good`**（类似「字典」但是固定大小的表格），用来快速判断任意子串是否漂亮，避免重复的二进制转整数和除 5 检查。  
> - **一维 DP 数组 `dp`**，记录子问题的最优解。

#### 代码（Python）

```python
def min_beautiful_substrings(s: str) -> int:
    n = len(s)
    INF = 10 ** 9

    # ---------- 1. 预处理所有「漂亮」子串 ----------
    # good[i][j] == True 表示 s[i:j+1] 是漂亮的
    good = [[False] * n for _ in range(n)]

    def is_beautiful(num: int) -> bool:
        """判断十进制整数 num 是否是 5 的幂（不含 0）"""
        if num == 0:
            return False
        while num % 5 == 0:
            num //= 5
        return num == 1

    for i in range(n):
        # 从 i 开始逐步扩展，实时维护二进制数值，避免每次都 `int(sub, 2)`
        val = 0
        for j in range(i, n):
            # 左移一位并加上当前字符，等价于二进制转十进制的累加
            val = (val << 1) + (s[j] == '1')
            # 前导零判定：如果子串长度 > 1 且首字符是 0，则直接跳过
            if i == 0 and s[i] == '0' and j > i:
                continue
            if i != 0 and s[i] == '0':
                continue
            if is_beautiful(val):
                good[i][j] = True

    # ---------- 2. DP: dp[i] = 最少子串数，从 i 开始 ----------
    dp = [INF] * (n + 1)
    dp[n] = 0                     # 空串需要 0 个子串

    # 倒序遍历保证 dp[j+1] 已经计算完
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if good[i][j]:
                dp[i] = min(dp[i], 1 + dp[j + 1])

    return -1 if dp[0] == INF else dp[0]
```

> 代码要点  
> - `val = (val << 1) + (s[j] == '1')` 用位运算实时把二进制子串转成整数，省去 `int(sub, 2)` 的重复开销。  
> - 前导零的判断放在预处理阶段，只要发现子串首位是 `'0'`（且长度大于 1），就不必再检查它是否是 5 的幂。  
> - DP 采用 **倒序** 填表，确保 `dp[j+1]` 已经是最优的。

#### 复杂度  

- **时间复杂度**：`O(n^2)`  
  - 预处理所有子串：`O(n^2)`（每个子串一次二进制累加和一次除 5 检查）。  
  - DP 转移同样遍历所有 `(i, j)` 对，仍是 `O(n^2)`。  
  - 对于 `n ≤ 15`，几百次操作几乎瞬间完成。  
- **空间复杂度**：`O(n^2)`  
  - `good` 表占 `n^2` 个布尔值，`dp` 占 `O(n)`。在本题的规模下完全可以接受。

---

## 心得

- **核心技巧**：  
  1. **前导零过滤 + 5 的幂判定**（通过不断除 5 判断）。  
  2. **子串预处理**（把「是否漂亮」的判定提前做完，变成 O(1) 查询）。  
  3. **动态规划**：把「从左到右的最少切分」转化为「从当前位置的最优子问题」并倒序求解。

- **该技巧适用的题型**  
  - 「把字符串切成满足某种属性的子串」的最少/最多切分问题（如 LeetCode 1400 `String Partition`、LCP 2021 `分割回文子串`）。  
  - 「子串属性预处理」+ DP 的组合题目（如「分割回文子串」需要先算出回文表）。  

- **一句话总结**：  
  *先把「子串好不好」提前算好，再用 DP 把「最少切几段」一步步向左推进，既避免重复检查，又得到最优解。*

---

## 反思

- **第一反应**：看到「二进制」+「5 的幂」会立刻想到「把二进制转十进制后判断是否是 5 的幂」，再想到「枚举所有切点」的暴力搜索。  
- **最容易踩的坑**  
  1. **前导零**：`"0"` 本身不是漂亮的，任何以 `'0'` 开头且长度 > 1 的子串都必须直接判为不合法。  
  2. **整数溢出**：虽然本题长度 ≤ 15，转成整数完全安全，但如果长度更大，需要考虑 Python 的大整数或使用字符串除法。  
  3. **剪枝不当**：在暴力递归里忘记在已经超过当前最优解时提前返回，会导致时间爆炸。  

- **下次遇到同类题**：  
  1. **先判断子串属性是否容易预处理**（如回文、是否是某类数）。  
  2. **把「是否满足」的判定抽离成表格或哈希，以 O(1) 查询**。  
  3. **再用 DP 或记忆化搜索把最少/最多切分的问题解决**。这样思路清晰、代码易调试，也能自然得到最优解。