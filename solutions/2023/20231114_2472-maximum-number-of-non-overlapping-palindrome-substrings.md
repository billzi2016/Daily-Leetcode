# #2472. 最多不重叠回文子串的数量 / Maximum Number of Non-overlapping Palindrome Substrings

> 难度：困难 · 标签：Two Pointers、String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-non-overlapping-palindrome-substrings/)

---

## 题目（英文原版）

**Description**

You are given a string s and a positive integer k.
Select a set of non-overlapping substrings from the string s that satisfy the following conditions:
Return the maximum number of substrings in an optimal selection.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "abaccdbbd", k = 3
Output: 2
Explanation: We can select the substrings underlined in s = "abaccdbbd". Both "aba" and "dbbd" are palindromes and have a length of at least k = 3.
It can be shown that we cannot find a selection with more than two valid substrings.
```

**Example 2:**

```
Input: s = "adbcda", k = 2
Output: 0
Explanation: There is no palindrome substring of length at least 2 in the string.
```

**Constraints**

- 1 <= k <= s.length <= 2000
- s consists of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `s` 和一个正整数 `k`。  
从字符串 `s` 中选取若干个互不重叠的子串（substring），要求满足以下条件：

1. 每个选中的子串必须是回文子串（palindrome substring），即正读和反读相同。  
2. 每个选中的子串长度不少于 `k`。  

返回在满足上述条件的所有可能选取方案中，能够选取的子串最大数量。

> **提示**：子串是字符串中连续的一段字符序列。

**示例**

*示例 1*  
输入：`s = "abaccdbbd"`, `k = 3`  
输出：`2`  
解释：我们可以选取下划线标记的子串 `ab**aba**ccdb**dbbd**`。`"aba"` 和 `"dbbd"` 都是回文且长度至少为 `k = 3`。可以证明不存在包含多于两个满足条件子串的选取方案。

*示例 2*  
输入：`s = "adbcda"`, `k = 2`  
输出：`0`  
解释：字符串中不存在长度至少为 `2` 的回文子串。

**约束条件**  
- `1 <= k <= s.length <= 2000`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有满足条件的回文子串都列举出来**，然后在这些子串中挑选出一组互不重叠且数量最多的子集。

- **枚举子串**：遍历所有 `(左, 右)` 区间，检查 `s[left:right+1]` 是否是回文且长度 `≥ k`。这一步相当于把字符串的每个字符想象成一本书的页码，左指针是“起始页”，右指针是“结束页”。  
- **回溯选子集**：把所有合法子串记在一个列表 `candidates` 中。接下来使用**递归+记忆化**（或普通回溯）尝试把这些子串一个一个加入答案。每加入一个子串，就把后面所有与它重叠的子串剔除，继续递归求最大数量。  

为什么这样可以得到答案？因为我们穷举了**所有可能的选法**，其中必然包含最优解。只是不够高效。

#### 代码（Python）

```python
def max_non_overlapping_bruteforce(s: str, k: int) -> int:
    n = len(s)

    # ---------- 1. 枚举所有合法回文子串 ----------
    def is_pal(l: int, r: int) -> bool:
        """检查 s[l:r+1] 是否为回文（双指针）"""
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    candidates = []                     # 保存 (左, 右) 区间
    for l in range(n):
        for r in range(l + k - 1, n):    # 长度必须 ≥ k
            if is_pal(l, r):
                candidates.append((l, r))

    # ---------- 2. 回溯挑选互不重叠子串 ----------
    from functools import lru_cache

    # 为加速，先把候选子串按左端点排序
    candidates.sort(key=lambda x: x[0])
    m = len(candidates)

    @lru_cache(None)
    def dfs(idx: int, last_end: int) -> int:
        """
        从 candidates[idx:] 开始挑选，要求新子串的左端点 > last_end。
        返回能够得到的最大子串数量。
        """
        if idx == m:
            return 0
        # 跳过当前子串
        best = dfs(idx + 1, last_end)

        l, r = candidates[idx]
        if l > last_end:                     # 与之前选的子串不重叠
            # 选当前子串 + 继续向后选
            best = max(best, 1 + dfs(idx + 1, r))
        return best

    return dfs(0, -1)    # 初始时没有子串，last_end = -1
```

> **关键行中文注释**已经写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：  
  - 枚举所有子串的两层循环是 `O(n²)`（n ≤ 2000），每次检查回文最坏 `O(n)`，所以最坏是 `O(n³)`。  
  - 回溯阶段的状态数是 `候选子串数 × n`，在最坏情况下仍然是指数级（接近 `2^m`），因此整体是 **指数时间**，只能在极小的测试里跑通。  
  - 用大白话说，**“把所有可能的组合都尝遍”**，所以会非常慢。

- **空间复杂度**：  
  - 保存所有合法子串需要 `O(m)`（最坏 `O(n²)`）的额外列表。  
  - 递归记忆化表 `dfs` 用到 `O(m·n)` 的状态，最坏也是 `O(n²)`。  
  - 总体上是 **平方级别的空间**，但仍然不可接受。

> 暴力解帮助我们理解“什么是合法子串，怎样判断是否重叠”，但它太慢，必须优化。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到两件事：

1. **判断回文** 可以提前预处理，避免在每次检查时重新遍历子串。  
2. **选子串的顺序**：如果我们从左到右扫描字符串，遇到一个合法的回文子串，就可以立刻决定是否把它加入答案——只要保证加入后不会影响后面更好的选择。

这正好对应 **“动态规划 + 贪心”** 的思路。我们定义：

- `dp[i]`：考虑字符串前缀 `s[0…i]`（包括第 `i` 个字符）时，能够得到的**最多不重叠回文子串数**。

对于每个位置 `i`，有两种选择：

1. **不选** 以 `i` 结尾的任何回文子串 → `dp[i] = dp[i-1]`。  
2. **选** 某个长度 `≥ k` 的回文子串 `s[j…i]`（`j ≤ i`），则答案可以在 `j-1` 之前的最优解上再加 `1`：  
   `dp[i] = max(dp[i], dp[j-1] + 1)`（当 `j == 0` 时 `dp[j-1]` 视作 `0`）。

关键在于**快速找出所有以 `i` 为右端点、长度 ≥ k 的回文子串**。这可以通过 **中心扩展**（或经典的 `isPal[l][r]` DP）在 `O(n²)` 时间预处理得到：

- 对每个中心（可以是字符或字符间的空隙）向两侧展开，记录所有满足 `len ≥ k` 的回文区间 `(l, r)`。

有了这些信息，我们只需一次遍历 `i = 0 … n-1`，对每个以 `i` 结尾的回文区间更新 `dp[i]`。

> **为什么这里的贪心成立？**  
> 动态规划已经把“在前缀里怎么选”全部考虑完了。`dp[i]` 只依赖于更左侧的 `dp[j-1]`，没有跨越回文子串之间的冲突。因此，每次把能让 `dp[i]` 变大的回文子串加入，实际上就是在做“在已经得到的最优前缀基础上，尽可能多加一个子串”。这正是贪心的本质——**局部最优** 导致**全局最优**，因为状态转移已经保证了最优子结构。

#### 代码（Python）

```python
def max_non_overlapping_palindromes(s: str, k: int) -> int:
    n = len(s)
    # ---------- 1. 预处理所有满足长度 >= k 的回文区间 ----------
    # pal_ends[i] 保存所有左端点 l，使得 s[l…i] 是回文且长度 >= k
    pal_ends = [[] for _ in range(n)]

    # 以每个字符为中心扩展（奇数长度回文）
    for center in range(n):
        l, r = center, center
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 >= k:          # 长度够了才记录
                pal_ends[r].append(l)   # 右端点是 r，左端点是 l
            l -= 1
            r += 1

    # 以两个字符之间的空隙为中心扩展（偶数长度回文）
    for center in range(n - 1):
        l, r = center, center + 1
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 >= k:
                pal_ends[r].append(l)
            l -= 1
            r += 1

    # ---------- 2. 动态规划求最大数量 ----------
    dp = [0] * n               # dp[i] = 前缀 s[0…i] 的答案

    for i in range(n):
        # 情形 1：不选以 i 结尾的回文子串
        dp[i] = dp[i - 1] if i > 0 else 0

        # 情形 2：选一个以 i 结尾的合法回文子串
        for l in pal_ends[i]:
            # dp[l-1] 为左侧前缀的最优解（l==0 时为 0）
            left = dp[l - 1] if l > 0 else 0
            dp[i] = max(dp[i], left + 1)

    return dp[-1]              # 整个字符串的答案
```

> 代码中每一行都配有中文注释，直接复制即可运行。

#### 复杂度

- **时间复杂度**：  
  - 中心扩展遍历所有可能的回文区间，总共 `O(n²)`（每个中心最多向外扩展 `n` 步）。  
  - 动态规划遍历 `i = 0…n-1`，对每个 `i` 只处理它对应的 `pal_ends[i]`，这些列表里所有左端点的总数恰好是前面预处理得到的回文区间数，仍是 `O(n²)`。  
  - 因此整体 **`O(n²)`**，对 `n ≤ 2000` 完全可接受。  
  - 用大白话说，就是“把所有可能的回文子串一次性列出来，然后在它们上面做一次遍历”，不会出现指数级的爆炸。

- **空间复杂度**：  
  - `pal_ends` 保存每个右端点对应的左端点列表，最坏也会存 `O(n²)` 个区间。  
  - `dp` 只需要 `O(n)`。  
  - 所以总体是 **`O(n²)`** 的额外空间。若想进一步压缩空间，可在中心扩展时直接更新 `dp`（不保存所有区间），那空间可降到 `O(n)`，但这里保持可读性更重要。

> 与暴力解相比，时间从指数级降到了多项式级，真正可以在 LeetCode 上 AC。

---

## 心得

- **核心技巧**：**动态规划 + 预处理回文子串**（中心扩展或回文表）。  
- **适用的题型**：  
  1. “划分字符串，使每段满足某种性质”——如 **分割回文子串的最少次数**（LeetCode 132），  
  2. “在字符串中找最多不重叠的满足条件的子串”——如 **最多不重叠的子序列**（LeetCode 1248），  
  3. “统计满足长度/性质约束的子串数量”——如 **最长回文子串**、**回文子串计数**。  
- **一句话总结解题钥匙**：  
  > “先把所有合法的回文区间一次性找出来，再用 DP 在左到右的顺序上把它们‘拼’成最多的非重叠组合。”

---

## 反思

- **第一反应**：看到“非重叠回文子串”，立刻想到“枚举所有回文子串 + 选子集”。这自然导向暴力解。  
- **最容易踩的坑**：  
  - 忘记 **长度 ≥ k** 的限制，导致把短回文也计入，答案会偏大。  
  - 在 DP 中使用 `dp[i-1]` 时没有处理 `i=0` 的边界，容易出现索引错误。  
  - 中心扩展时忘记 **偶数长度** 的情况，只算奇数回文会漏掉如 `"dbbd"` 这类合法子串。  
- **下次遇到同类题**，第一步应该想到：  
  > “先把**所有满足子串属性**（这里是回文且长度≥k）**一次性预处理**，然后用**左到右的 DP**把这些区间拼成最大非重叠集合”。  

这样既能保证正确性，又能把时间复杂度控制在可接受的范围。