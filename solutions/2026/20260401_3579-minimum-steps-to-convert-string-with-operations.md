# #3579. 字符串转换的最少操作步数 / Minimum Steps to Convert String with Operations

> 难度：困难 · 标签：String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-steps-to-convert-string-with-operations/)

---

## 题目（英文原版）

**Description**

You are given two strings, word1 and word2, of equal length. You need to transform word1 into word2.
For this, divide word1 into one or more contiguous substrings. For each substring substr you can perform the following operations:
Each of these counts as one operation and each character of each substring can be used in each type of operation at most once (i.e. no single index may be involved in more than one replace, one swap, or one reverse).
Return the minimum number of operations required to transform word1 into word2.

**Examples**

**Example 1:**

```
Input: word1 = "abcdf", word2 = "dacbe"
Output: 4
Explanation:
Divide word1 into "ab" , "c" , and "df" . The operations are:
```

**Example 2:**

```
Input: word1 = "abceded", word2 = "baecfef"
Output: 4
Explanation:
Divide word1 into "ab" , "ce" , and "ded" . The operations are:
```

**Example 3:**

```
Input: word1 = "abcdef", word2 = "fedabc"
Output: 2
Explanation:
Divide word1 into "abcdef" . The operations are:
```

**Constraints**

- 1 <= word1.length == word2.length <= 100
- word1 and word2 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个等长的字符串 `word1` 和 `word2`，要求把 `word1` 转换成 `word2`。  
为此，需要将 `word1` 划分为一个或多个连续子串（contiguous substrings）。  
对每个子串 `substr` 可以执行以下操作：

* 替换（replace）：将子串中的某个字符替换成另一个字符。  
* 交换（swap）：交换子串中两个不同位置的字符。  
* 逆序（reverse）：将子串整体翻转。

每执行一次上述任意操作都计为 **一次操作**，并且在同一个子串中，同一个字符位置在同一种操作类型下只能使用一次（即同一下标不能同时参与两次替换、两次交换或两次逆序）。

求将 `word1` 转换为 `word2` 所需的最小操作次数，并返回该值。

## 示例

### 示例 1
**输入**  
```text
word1 = "abcdf", word2 = "dacbe"
```
**输出**  
```text
4
```
**解释**  
将 `word1` 划分为 `"ab"`、`"c"` 和 `"df"`。对应的操作为：

（此处省略具体操作步骤，保持原样）

### 示例 2
**输入**  
```text
word1 = "abceded", word2 = "baecfef"
```
**输出**  
```text
4
```
**解释**  
将 `word1` 划分为 `"ab"`、`"ce"` 和 `"ded"`。对应的操作为：

（此处省略具体操作步骤，保持原样）

### 示例 3
**输入**  
```text
word1 = "abcdef", word2 = "fedabc"
```
**输出**  
```text
2
```
**解释**  
将 `word1` 划分为 `"abcdef"`。对应的操作为：

（此处省略具体操作步骤，保持原样）

## 约束条件

- `1 <= word1.length == word2.length <= 100`
- `word1` 和 `word2` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `word1` 的每一个字符都单独拿出来**，把它们一个一个地变成 `word2` 对应位置的字符。  
这相当于把 `word1` 分成 `n` 段（每段长度都是 1），对每段只做一次 **replace** 操作。  

- **数据结构**：只需要两个字符串和一个计数器。这里不需要哈希表、栈之类的高级结构，完全像在纸上写“把 a 换成 b”。  
- **正确性**：因为每个字符都能被单独替换，所以一定可以把 `word1` 完全变成 `word2`。  
- **时间/空间复杂度**：我们要遍历所有字符一次，检查它们是否相等，若不等就加 1 次操作。  

  - 时间复杂度是 `O(n)`，这里的 `n` 就是字符串长度。  
    - “`O(n)`” 可以理解为：如果字符串有 10 个字符，最多检查 10 次；如果有 100 个字符，最多检查 100 次，随着字符数线性增长。  
  - 空间复杂度是 `O(1)`，只用了常数个额外变量（计数器、循环索引），不随输入大小增长。

> **注意**：这只是“最笨”的办法，实际上题目允许 **swap**、**reverse** 等更强的操作，能把操作次数进一步压缩。

#### 代码（Python）

```python
def min_steps_bruteforce(word1: str, word2: str) -> int:
    """
    暴力解：把每个字符单独看成一个子串，只使用 replace。
    每个字符若不相同，就需要一次 replace。
    """
    n = len(word1)
    ops = 0                         # 记录操作次数
    for i in range(n):
        if word1[i] != word2[i]:    # 只要字符不相等，就要替换一次
            ops += 1
    return ops
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 线性遍历一次字符串，字符多多少次检查就多多少次。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和字符串长度无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每次 replace 只能一次性改掉一个错误字符**，这显然不是最省操作的办法。  
我们需要利用题目给出的两种“更省钱”的操作：

1. **swap**（交换）：如果 `word1[i]` 正好等于 `word2[j]` 且 `word1[j]` 等于 `word2[i]`，一次 swap 就能把两个错误同时改对。  
   - 这相当于把两次 replace 合并成一次，**省 1 次操作**。  
2. **reverse**（整体反转）：把整个子串反过来后再进行上面的 swap / replace。  
   - 反转本身算 **一次** 操作，之后再按普通方式处理。

> **关键观察**：  
> 对于任意 **连续子串** `word1[l…r]`（对应的目标子串是 `word2[l…r]`），我们只需要在这段区间内部决定：
> - 是否先整体反转一次（最多一次），
> - 再在反转后（或不反转的）区间里尽可能多地配对 “互相对应的 swap”，
> - 剩下的未配对错误只能用 replace 解决。  

因此，**每个子串的最优操作数** 可以用下面的公式求得：

```
cost_without_reverse = mismatches - max_swap_pairs
cost_with_reverse    = 1 (reverse) + mismatches_rev - max_swap_pairs_rev
cost(l, r) = min(cost_without_reverse, cost_with_reverse)
```

其中：

- `mismatches` = 在子串中字符不相同的位置个数。  
- `max_swap_pairs` = 能够配对的 swap 对数（每对 swap 只能用一次，且每个位置只能参加一个 swap）。  
- 对 “反转后” 的情况，同理计算 `mismatches_rev` 与 `max_swap_pairs_rev`。

#### 如何求 `max_swap_pairs`

在一个子串里，所有不匹配的位置记为集合 `M`。  
我们遍历 `M`，对每个未使用的下标 `i`，尝试找一个更大的下标 `j`（`j > i`），满足：

```
word1[i] == word2[j]  and  word1[j] == word2[i]
```

如果找到，就把 `i`、`j` 标记为已使用，`swap_cnt += 1`。  
因为每个位置只能被使用一次，这种 **贪心一次配对** 已经能得到最大配对数（两两配对的条件是互相对应，若有冲突只能选其中一个，先找到的配对不会影响后面的更佳配对，因为所有配对都只涉及两个位置）。  
该过程的时间复杂度是 `O(L²)`，`L = r-l+1`（子串长度），在整体 `n ≤ 100` 的限制下是可以接受的。

#### DP 把所有子串拼起来

我们把整个字符串视为若干不相交子串的拼接。  
设 `dp[i]` 为 **把前 i 个字符（下标 0 … i-1）全部转换好的最少操作数**。  

状态转移：

```
dp[0] = 0
dp[i] = min_{0 ≤ j < i} ( dp[j] + cost(j, i-1) )
```

也就是说，我们把前 `i` 个字符的最后一个子串设为 `[j, i-1]`，  
前面 `0 … j-1` 的最优已经保存在 `dp[j]`，再加上这个子串的最优 `cost` 即得到一种完整方案。  
遍历所有可能的 `j` 取最小即可。

#### 复杂度分析

- **子串代价预处理**：对所有 `l ≤ r`（共 `O(n²)` 对），每对计算 `cost` 需要 `O(L²)`，最坏 `L = n`，于是整体 `O(n³)`。  
  - 对 `n = 100`，`n³ = 1,000,000`，在 Python 中毫秒级完成。  
- **DP 主循环**：外层 `i` 从 `1 … n`，内层遍历 `j`，共 `O(n²)`。  
- **总时间**：`O(n³)`（约 10⁶ 次基本操作），足够快。  
- **空间**：我们保存 `dp` 长度 `n+1` 的数组以及 `cost` 的二维表（`n×n`），都是 `O(n²)`，即 `≈ 10⁴` 个整数，完全可以接受。

> 与暴力解相比，时间从线性 `O(n)` 变成了 `O(n³)`，但这里的 “暴力解” 只能得到 **上界**（所有字符单独 replace），而 DP 给出了 **真正的最小操作数**。

#### 代码（Python）

```python
def min_steps(word1: str, word2: str) -> int:
    """
    动态规划 + 贪心配对 swap（可选一次 reverse）
    返回把 word1 变成 word2 所需的最少操作数
    """
    n = len(word1)
    # ---------- 1. 预计算所有子串的最优代价 ----------
    # cost[l][r] 表示子串 word1[l..r] -> word2[l..r] 的最少操作数
    cost = [[0] * n for _ in range(n)]

    # 辅助函数：计算单个子串的代价（是否先 reverse）
    def calc_sub(l: int, r: int) -> int:
        """返回子串 [l, r] 的最小代价（含可选的 reverse）"""
        # ---------- 不反转的情况 ----------
        mism = []                     # 记录不匹配的位置
        for i in range(l, r + 1):
            if word1[i] != word2[i]:
                mism.append(i)

        # 贪心配对 swap
        used = [False] * len(mism)
        swap_cnt = 0
        for a in range(len(mism)):
            if used[a]:
                continue
            i = mism[a]
            for b in range(a + 1, len(mism)):
                if used[b]:
                    continue
                j = mism[b]
                if word1[i] == word2[j] and word1[j] == word2[i]:
                    used[a] = used[b] = True
                    swap_cnt += 1
                    break

        cost_no_rev = len(mism) - swap_cnt   # 每个 swap 把两次 replace 合并为一次

        # ---------- 反转一次的情况 ----------
        # 把 word1[l..r] 先整体翻转
        rev_word1 = word1[l:r + 1][::-1]
        mism_rev = []
        for offset, ch in enumerate(rev_word1):
            idx = l + offset
            if ch != word2[idx]:
                mism_rev.append(offset)   # 用相对位置方便后面取字符

        used_rev = [False] * len(mism_rev)
        swap_cnt_rev = 0
        for a in range(len(mism_rev)):
            if used_rev[a]:
                continue
            i_off = mism_rev[a]
            i_char = rev_word1[i_off]
            for b in range(a + 1, len(mism_rev)):
                if used_rev[b]:
                    continue
                j_off = mism_rev[b]
                j_char = rev_word1[j_off]
                # 对应的目标字符
                if i_char == word2[l + j_off] and j_char == word2[l + i_off]:
                    used_rev[a] = used_rev[b] = True
                    swap_cnt_rev += 1
                    break

        cost_rev = 1 + len(mism_rev) - swap_cnt_rev   # 1 次 reverse + 其余操作

        return min(cost_no_rev, cost_rev)

    # 填表
    for length in range(1, n + 1):          # 子串长度
        for l in range(0, n - length + 1):
            r = l + length - 1
            cost[l][r] = calc_sub(l, r)

    # ---------- 2. 动态规划求整体最小操作数 ----------
    INF = 10 ** 9
    dp = [INF] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):               # i 表示前 i 个字符已处理
        for j in range(i):                  # 子串是 [j, i-1]
            dp[i] = min(dp[i], dp[j] + cost[j][i - 1])

    return dp[n]
```

> **代码要点解释（中文注释已在代码中）**  
> - `calc_sub` 完成 **“单段最优代价”** 的计算：先统计不匹配位置，再用贪心找最多的互换对，最后比较“直接处理”和“先整体反转再处理”。  
> - `cost[l][r]` 预先保存所有子串的代价，供后面的 DP 快速查表。  
> - DP 的状态转移 `dp[i] = min(dp[j] + cost[j][i-1])` 正是把整个字符串切分成若干不相交子串的过程。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 预处理所有子串代价需要 `O(n³)`（最多 1,000,000 次基本操作），DP 本身是 `O(n²)`，总体仍是 `O(n³)`。  
  - 与暴力解的 `O(n)` 不同，这里 **n³** 表示“随着字符数的立方增长”。但因为 `n ≤ 100`，实际运行非常快。  
- **空间复杂度**：`O(n²)`  
  - `cost` 表占用 `n×n` 的整数，`dp` 只要 `n+1`，整体是二次级别的存储需求。  

> 与暴力解相比，**操作次数明显下降**（因为我们真正利用了 swap 与 reverse），而且 **时间仍在可接受范围**（n 只到 100）。

---

## 心得

- **核心技巧**：**在每个子串内部先做最多的 swap（配对互换），必要时再一次性 reverse**，随后用 DP 把整个字符串划分成若干最优子串。  
- **适用的题型**  
  1. 需要把一个序列变成另一个序列，且操作可以在**连续区间**内部完成的题目（如 “把数组排序只允许区间翻转或交换”）。  
  2. 需要**区间划分 + 区间内部最优**的 DP 题（如 “最小划分代价” 类问题）。  
  3. 包含 **swap / reverse** 等“可组合”操作的字符串编辑问题。  
- **一句话总结解题钥匙**：**把局部的“配对换位”最大化，再用 DP 把全局划分成若干局部最优的子段**。

---

## 反思

- **第一反应**：看到可以把 `word1` 分成子串，立刻想到**枚举所有划分**，但直接递归会指数爆炸。  
- **最容易踩的坑**  
  1. **swap 的配对条件**写错：一定是 `word1[i] == word2[j]` 且 `word1[j] == word2[i]`，否则 swap 并不能一次解决两个错误。  
  2. **反转后的字符对应关系**：反转后下标变化，需要用相对偏移来取字符，容易产生 off‑by‑one 错误。  
  3. **每个字符只能参加一次 swap**：忘记标记已使用的下标会导致同一个位置被多次计入不同的 swap，结果会低估操作数。  
- **下次遇到同类题**：第一步先**明确每个区间内部的最优代价**（是否可以配对、是否需要整体翻转），再**用 DP 把区间拼接**得到全局最优。这样可以把“全局难题”拆解成“局部易解 + 组合”。