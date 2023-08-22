# #2370. 最长理想子序列 / Longest Ideal Subsequence

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-ideal-subsequence/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase letters and an integer k. We call a string t ideal if the following conditions are satisfied:
Return the length of the longest ideal string.
A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.
Note that the alphabet order is not cyclic. For example, the absolute difference in the alphabet order of 'a' and 'z' is 25, not 1.

**Examples**

**Example 1:**

```
Input: s = "acfgbd", k = 2
Output: 4
Explanation: The longest ideal string is "acbd". The length of this string is 4, so 4 is returned.
Note that "acfgbd" is not ideal because 'c' and 'f' have a difference of 3 in alphabet order.
```

**Example 2:**

```
Input: s = "abcd", k = 3
Output: 4
Explanation: The longest ideal string is "abcd". The length of this string is 4, so 4 is returned.
```

**Constraints**

- 1 <= s.length <= 105
- 0 <= k <= 25
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写字母的字符串 `s` 和一个整数 `k`。如果一个字符串 `t` 满足以下条件，则称其为 **理想的**（ideal）：

- `t` 是 `s` 的子序列（subsequence），即可以通过删除 `s` 中的若干字符（也可以不删）而得到，且删除后剩余字符的相对顺序保持不变；
- 对于 `t` 中相邻的任意两个字符，其在字母序（alphabet order）上的绝对差值不超过 `k`。

返回最长理想字符串的长度。

> 注意，字母序不是循环的。例如，字符 `'a'` 与 `'z'` 的字母序差值为 `25`，而不是 `1`。

### 示例

**示例 1**  
Input: `s = "acfgbd", k = 2`  
Output: `4`  
Explanation: 最长的理想字符串是 `"acbd"`，其长度为 `4`，因此返回 `4`。  
注意，原字符串 `"acfgbd"` 并非理想的，因为字符 `'c'` 与 `'f'` 的字母序差值为 `3`，超过了 `k`。

**示例 2**  
Input: `s = "abcd", k = 3`  
Output: `4`  
Explanation: 最长的理想字符串是 `"abcd"`，其长度为 `4`，因此返回 `4`。

### 约束条件

- `1 <= s.length <= 10^5`
- `0 <= k <= 25`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子序列**，检查每个子序列是否满足 “相邻字符的字母序号差 ≤ k”。  
如果满足，就记录它的长度，最后取最大的那个。

- **子序列**可以把原字符串的每个字符想成一本书的每一页，**要么选这页，要么不选**，但选的顺序必须保持原来的顺序。  
- 检查是否 “ideal” 就像在看相邻两页的页码差，如果差值 ≤ k 就算合格。

暴力枚举的实现通常用**回溯（DFS）**或**位掩码**：

1. 从左到右遍历字符，决定“选”或“不选”。  
2. 选了之后，记录上一次被选的字符，确保新选的字符和上一次的差 ≤ k。  
3. 当遍历结束时，得到一个合法子序列的长度，更新全局最大值。

虽然思路很清晰，但它会尝试 **2ⁿ** 种选法（n 为字符串长度），对于 n 达到 10⁵ 的题目根本不可行。

#### 代码（Python）

```python
def longestIdeal_subseq_bruteforce(s: str, k: int) -> int:
    n = len(s)
    best = 0                     # 记录全局最长长度

    def dfs(idx: int, prev_char: str, length: int):
        """从位置 idx 开始向后搜索，prev_char 为上一次选的字符（或 None）"""
        nonlocal best
        # 已经遍历完所有字符，更新答案
        if idx == n:
            best = max(best, length)
            return

        # 方案一：不选 s[idx]，直接跳到下一个字符
        dfs(idx + 1, prev_char, length)

        # 方案二：选 s[idx]，前提是满足 ideal 条件
        cur = s[idx]
        if prev_char is None or abs(ord(cur) - ord(prev_char)) <= k:
            dfs(idx + 1, cur, length + 1)

    dfs(0, None, 0)
    return best
```

> **提示**：上述代码只能通过极小的测试用例，`n=20` 左右已经会超时。

#### 复杂度  

- **时间复杂度**：`O(2^n)`  
  每个字符都有“选”或“不选”两种决定，导致指数级的搜索。可以把 `2^n` 想成“翻倍” n 次的结果，n=30 时已经是十亿级别，根本不可接受。

- **空间复杂度**：`O(n)`（递归栈的深度）  
  递归最深会走到字符串末尾，需要保存 n 层调用信息。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**重复计算**：很多子序列的前缀是相同的，我们每次都重新遍历一遍。  
动态规划（DP）正是用来**记住已经算过的子问题答案**，避免重复工作。

**关键观察**：

- 对于位置 `i`（字符 `s[i]`），如果我们已经知道以某个字符 `c` 结尾的最长 ideal 子序列长度 `dp[c]`，那么只要 `|s[i] - c| ≤ k`，我们就可以把 `s[i]` 接在这个子序列后面，得到长度 `dp[c] + 1`。

- 因此，**只需要维护 26 个状态**，分别表示“以字母 `'a' … 'z'` 结尾的最长 ideal 子序列长度”。这 26 个状态可以看成一个**哈希表**（这里用数组更快），就像查字典一样：键是字母，值是当前的最长长度。

**具体步骤**：

1. 初始化一个长度为 26 的数组 `best[0…25] = 0`，`best[i]` 代表以字母 `chr(ord('a')+i)` 结尾的最长 ideal 子序列长度。  
2. 逐字符遍历字符串 `s`（从左到右），设当前字符是 `ch`，对应的下标 `idx = ord(ch) - ord('a')`。  
3. 为了得到以 `ch` 结尾的最长长度，需要查看所有能够和 `ch` “相邻”的字母，即下标在 `[idx-k, idx+k]` 之间（并且在 0~25 范围内）的 `best` 值，取其中的最大值 `mx`。  
4. 当前字符能够形成的长度是 `mx + 1`。把它写回 `best[idx] = max(best[idx], mx + 1)`（因为以后可能还有别的出现再更新）。  
5. 最后答案是 `best` 数组里的最大值。

**为什么只看前后 k 个字母就够？**  
因为 ideal 的定义只限制**相邻字符**的差 ≤ k。若我们已经得到一条以字母 `c` 结尾的理想子序列，那么只要新字符 `ch` 与 `c` 的差 ≤ k，就可以安全接在后面。更远的字母（差 > k）根本不可能直接相连，所以不需要考虑。

**时间复杂度**：遍历 `n` 个字符，每个字符最多检查 `2k+1 ≤ 51`（因为 `k ≤ 25`）个前缀状态，整体是 `O(n·k)`，在最坏情况下仍是 `O(n·25) = O(n)`。

**空间复杂度**：只用到长度为 26 的数组，`O(1)`（常数空间）。

#### 代码（Python）

```python
def longestIdealSubsequence(s: str, k: int) -> int:
    """
    动态规划 + 固定大小哈希表（数组）实现
    best[i] 表示以字母 chr(ord('a') + i) 结尾的最长 ideal 子序列长度
    """
    best = [0] * 26               # 初始化全部为 0
    for ch in s:                  # 从左到右遍历
        idx = ord(ch) - ord('a')  # 当前字符在数组中的下标

        # 在 idx-k … idx+k 之间寻找可以接在前面的最长子序列
        lo = max(0, idx - k)      # 防止下标越界
        hi = min(25, idx + k)

        mx = 0                     # 记录可接的最大长度
        for j in range(lo, hi + 1):
            mx = max(mx, best[j])

        # 把当前字符接在最长的那条序列后面，长度为 mx+1
        # 可能已经有更长的以相同字符结尾的序列，取最大值
        best[idx] = max(best[idx], mx + 1)

    return max(best)               # 整体最长的就是答案
```

> **关键行解释**  
> - `best = [0] * 26`：把 26 本“字典”打开，初始页码都是 0。  
> - `for j in range(lo, hi + 1): mx = max(mx, best[j])`：在字典里查找“相邻”几页的最大长度。  
> - `best[idx] = max(best[idx], mx + 1)`：把新页码写进去，保持最新的最大值。

#### 复杂度  

- **时间复杂度**：`O(n * (2k+1)) = O(n)`  
  解释：每个字符只检查至多 51 次（因为 k≤25），可以把它想成“最多遍历 51 本小书”，即使 n 达到 10⁵，整体仍在几百万次以内，跑得很快。

- **空间复杂度**：`O(1)`（常数 26）  
  只用了一个固定大小的数组，不随输入规模增长。

---

## 心得

- **核心技巧**：**动态规划 + 限定范围的哈希表（数组）**。  
  把“以某个字符结尾的最长子序列长度”记下来，后面的字符只需要在它的“邻近”字符里找最大值。

- **适用的题型**  
  1. “最长递增子序列”类问题（如 LeetCode 300）——只需维护以每个值结尾的最长长度。  
  2. “最长连续子数组”或“相邻差值限制的子序列”类（如 “最长的字母序列”）。  
  3. 需要**按值分桶**（bucket）记录状态的 DP，例如 “最大子序和” 按数值区间划分的变体。

- **一句话总结解题钥匙**：  
  **把“以字母 X 结尾的最优解”抽象成 26 条状态，用局部范围查询快速转移。**

---

## 反思

- **第一反应**：看到“子序列”和“最长”，立刻想到暴力枚举或经典的 LIS（Longest Increasing Subsequence）思路，想把每个字符都当成 DP 的下标。

- **最容易踩的坑**  
  1. **忘记限制字母差值**：直接用普通 LIS 会把任意递增都算进来，结果会错误。  
  2. **边界处理**：`idx-k`、`idx+k` 可能越界，需要用 `max(0, …)`、`min(25, …)` 限制。  
  3. **状态更新顺序**：若在遍历同一个字符时直接覆盖 `best[idx]` 再去查询，会导致同一轮次使用了已经更新的值，产生错误。这里我们先查询完再一次性写回，或使用临时变量 `mx` 保存最大值。

- **下次遇到同类题的第一步**：  
  **先问自己“我能否把答案拆成‘以某个特定值结尾’的子问题’，并且转移只依赖于一个小范围的前驱状态吗？”**  
  若答案是肯定的，就可以尝试用“状态压缩 + 局部查询”来实现 O(n) 的线性解。