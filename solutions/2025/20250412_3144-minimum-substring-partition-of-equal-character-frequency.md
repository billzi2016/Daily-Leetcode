# #3144. 等字符频率的最小子串划分 / Minimum Substring Partition of Equal Character Frequency

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/)

---

## 题目（英文原版）

**Description**

Given a string s, you need to partition it into one or more balanced substrings. For example, if s == "ababcc" then ("abab", "c", "c"), ("ab", "abc", "c"), and ("ababcc") are all valid partitions, but ("a", "bab", "cc"), ("aba", "bc", "c"), and ("ab", "abcc") are not. The unbalanced substrings are bolded.
Return the minimum number of substrings that you can partition s into.
Note: A balanced string is a string where each character in the string occurs the same number of times.

**Examples**

**Example 1:**

```
Input: s = "fabccddg"
Output: 3
Explanation:
We can partition the string s into 3 substrings in one of the following ways: ("fab, "ccdd", "g") , or ("fabc", "cd", "dg") .
```

**Example 2:**

```
Input: s = "abababaccddb"
Output: 2
Explanation:
We can partition the string s into 2 substrings like so: ("abab", "abaccddb") .
```

**Constraints**

- 1 <= s.length <= 1000
- s consists only of English lowercase letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，需要将其划分为一个或多个 **平衡子串**（balanced substring）。  
例如，`s == "ababcc"` 时，划分 `("abab", "c", "c")`、`("ab", "abc", "c")`、`("ababcc")` 都是合法的，而划分 `("a", "bab", "cc")`、`("aba", "bc", "c")`、`("ab", "abcc")` 则不合法（不平衡的子串已用粗体标出）。  
返回能够使 `s` 被划分的子串数量的最小值。  

**平衡字符串**（balanced string）指的是字符串中每个字符出现的次数都相同。

---

### 示例

**示例 1**

```
Input: s = "fabccddg"
Output: 3
Explanation:
我们可以将字符串 s 划分为 3 个子串，例如：("fab", "ccdd", "g")，或 ("fabc", "cd", "dg")。
```

**示例 2**

```
Input: s = "abababaccddb"
Output: 2
Explanation:
我们可以将字符串 s 划分为 2 个子串，例如：("abab", "abaccddb")。
```

---

### 约束条件

- `1 <= s.length <= 1000`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的切分方式都枚举一遍**，只要每个子串都是 “平衡的”，就记下切分的数量，最后取最小值。

- **枚举切分**：可以用递归（或回溯）从字符串左边开始，每次尝试把前缀 `s[l…r]` 当成一个子串，如果它是平衡的，就递归处理剩下的 `s[r+1…]`。  
- **判断平衡**：遍历子串，统计每个字符出现的次数（用一个长度为 26 的数组，类似查字典：字符是“词”，出现次数是“页码”），取出现次数>0 的最小值 `min_cnt` 与最大值 `max_cnt`，只要 `min_cnt == max_cnt` 就说明子串平衡。

> **为什么正确**  
> 递归把 **所有** 合法的切分方式都遍历到了，最小的切分数一定会在其中出现。

- **时间复杂度**：  
  - 枚举所有切分方式的数目是指数级的（每个位置都有“切或不切”两种选择），记作 `O(2^n)`。  
  - 判断一个子串是否平衡要遍历子串本身，最坏 `O(n)`。  
  - 综合下来是 `O(2^n * n)`，对 `n ≤ 1000` 完全不可接受。  
- **空间复杂度**：递归栈深度最坏 `O(n)`，外加字符计数数组 `O(26) ≈ O(1)`。

#### 代码（Python）

```python
def minPartitions_bruteforce(s: str) -> int:
    n = len(s)

    # 判断子串 s[l:r+1] 是否平衡
    def is_balanced(l: int, r: int) -> bool:
        cnt = [0] * 26                     # 统计每个字母出现次数
        for i in range(l, r + 1):
            cnt[ord(s[i]) - ord('a')] += 1
        # 只看出现过的字符
        non_zero = [c for c in cnt if c > 0]
        return min(non_zero) == max(non_zero)

    # dfs(pos) 返回从位置 pos 开始的最小切分数，若不可行返回 INF
    from functools import lru_cache
    INF = 10 ** 9

    @lru_cache(None)
    def dfs(pos: int) -> int:
        if pos == n:               # 已经划完了
            return 0
        best = INF
        # 尝试把 s[pos … end] 作为第一个子串
        for end in range(pos, n):
            if is_balanced(pos, end):
                # 子串合法，递归处理剩下的部分
                best = min(best, 1 + dfs(end + 1))
        return best

    return dfs(0)
```

> **关键行注释**  
> - `cnt = [0] * 26`：像查字典一样，用字符的 ASCII 码做下标。  
> - `non_zero = [c for c in cnt if c > 0]`：只保留出现过的字符，空字符不参与比较。  
> - `dfs`：递归遍历所有切分方式，`lru_cache` 防止重复计算。

#### 复杂度

- **时间复杂度**：`O(2^n * n)`——指数级，实际运行会超时。  
- **空间复杂度**：`O(n)`——递归栈深度 + 记忆化表（最多 `n` 条记录），计数数组常数级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“枚举所有切分方式”** 与 **“每次都重新统计子串字符”**。  
我们可以把这两件事都 **用动态规划** 与 **增量计数** 来优化。

1. **动态规划框架**  
   - 设 `dp[i]` 为前缀 `s[0…i]`（长度为 `i+1`）的最小切分数。  
   - 最终答案是 `dp[n‑1]`。  
   - 转移方程：  
     ```
     dp[i] = min{ dp[j] + 1 | 0 ≤ j < i 且 s[j+1 … i] 平衡 }
     dp[i] = 1            当整个前缀 s[0…i] 本身平衡时（相当于 j = -1）
     ```
   - 这和暴力解里“遍历所有合法切分点”是一致的，只是把子问题的答案保存下来，避免重复计算。

2. **快速判断子串是否平衡**  
   - 对每个右端点 `i`，我们从 `i` 向左遍历 `j = i, i‑1, …, 0`，**实时维护** 一个 26 长度的计数数组 `cnt`（相当于在字典里不断往里加新词）。  
   - 同时记录当前出现字符的 **最大频率** `mx` 与 **最小非零频率** `mn`。  
   - 当 `mx == mn` 时，子串 `s[j…i]` 必然平衡。  
   - 由于每次只往左扩展一个字符，`cnt`、`mx`、`mn` 的更新都是 **O(1)** 的。

3. **整体复杂度**  
   - 外层遍历右端点 `i`，内层最多向左遍历 `i+1` 次，总共 `∑_{i=0}^{n‑1} (i+1) = O(n²)` 次。  
   - 每次更新计数只涉及常数个操作（26 个字母的数组），所以时间是 `O(n²)`，空间只需要 `dp`（`O(n)`）和计数数组（`O(26)≈O(1)`）。

> **类比**：想象我们在看一本书，每翻到新的一页（右端点 `i`），就把这页的单词依次往左“抄”进笔记本（计数数组），同时随手记下出现最频繁和最少的单词数，只要这两个数相等，就说明这段笔记（子串）是“字数均等”的——即平衡。

#### 代码（Python）

```python
def minPartitions_dp(s: str) -> int:
    n = len(s)
    INF = 10 ** 9
    dp = [INF] * n               # dp[i] = 前缀 s[0…i] 的最小切分数

    for i in range(n):           # 右端点 i
        cnt = [0] * 26           # 重新计数，准备向左扩展
        mx = 0                   # 当前出现字符的最大频率
        mn = INF                 # 当前出现字符的最小非零频率
        # 从 i 向左遍历，实时更新 cnt、mx、mn
        for j in range(i, -1, -1):
            idx = ord(s[j]) - ord('a')
            cnt[idx] += 1
            # 更新最大频率
            mx = max(mx, cnt[idx])
            # 更新最小非零频率：只看出现过的字符
            # 这里遍历 26 次也算常数，代码更直观
            cur_min = INF
            for c in cnt:
                if c > 0:
                    cur_min = min(cur_min, c)
            mn = cur_min

            # 判断 s[j…i] 是否平衡
            if mx == mn:                     # 平衡子串
                if j == 0:                   # 整个前缀本身平衡
                    dp[i] = 1
                else:
                    dp[i] = min(dp[i], dp[j-1] + 1)

    return dp[-1]
```

> **关键行注释**  
> - `cnt = [0] * 26`：用数组模拟哈希表，像查字典一样快速定位字符。  
> - `mx = max(mx, cnt[idx])`：记录出现次数最多的字符。  
> - `cur_min` 循环遍历 26 次找最小非零频率，虽然是 `O(26)`，但常数极小，整体仍是 `O(n²)`。  
> - `dp[i] = min(dp[i], dp[j-1] + 1)`：把左侧已经算好的最优切分数加上当前平衡子串，形成新的候选答案。

#### 复杂度

- **时间复杂度**：`O(n²)`（约 1,000,000 次基本操作，完全可以接受）。  
  - 与暴力解相比，去掉了指数级的“全部切分枚举”，只剩下两层循环。  
- **空间复杂度**：`O(n)`（`dp` 数组）+ `O(1)`（计数数组、几个整数），几乎不占内存。

---

## 心得

- **核心技巧**：**动态规划 + 增量计数**。  
  - DP 把“子问题最优解”保存下来，避免重复枚举。  
  - 增量计数让我们在 O(1)（或常数）时间内判断子串是否平衡，而不是每次重新遍历子串。

- **该技巧适用的题型**  
  1. **划分/分段问题**（如 “分割回文子串”）——需要在每个分割点判断子串属性。  
  2. **子数组/子串统计类**（如 “最长子数组满足条件”）——使用滑动窗口或前缀计数快速判断。  
  3. **字符频率约束的分割**（如 “最少子串覆盖所有字符”）——同样用计数数组维护频率。

- **一句话总结**：  
  *把“检查子串是否合格”变成增量操作，再配合 DP 把所有子问题的最优答案拼起来，就是本题的解题钥匙。*

---

## 反思

- **第一反应**：直接回溯枚举所有切分，想把每个子串逐个检查平衡。  
- **最容易踩的坑**  
  1. **平衡的定义**：只要求出现的字符频率相同，未出现的字符不计入比较。  
  2. **边界情况**：单字符字符串本身就是平衡的，需要把 `j == 0` 的情况单独处理（相当于整个前缀是一个合法子串）。  
  3. **计数更新**：在向左扩展时忘记同步更新最小非零频率，导致错误判断。  

- **下次遇到同类题**：第一步先想 **“能否用 DP 把前缀最优解保存下来”**，随后检查 **“子串属性是否可以增量维护（计数、最大/最小、和等）”**，若可以，就把两者结合，往往能把指数级的搜索压到 `O(n²)` 或更低。