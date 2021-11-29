# #1573. **划分字符串的方案数** / Number of Ways to Split a String

> 难度：中等 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-split-a-string/)

---

## 题目（英文原版）

**Description**

Given a binary string s, you can split s into 3 non-empty strings s1, s2, and s3 where s1 + s2 + s3 = s.
Return the number of ways s can be split such that the number of ones is the same in s1, s2, and s3. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "10101"
Output: 4
Explanation: There are four ways to split s in 3 parts where each part contain the same number of letters '1'.
"1|010|1"
"1|01|01"
"10|10|1"
"10|1|01"
```

**Example 2:**

```
Input: s = "1001"
Output: 0
```

**Example 3:**

```
Input: s = "0000"
Output: 3
Explanation: There are three ways to split s in 3 parts.
"0|0|00"
"0|00|0"
"00|0|0"
```

**Constraints**

- 3 <= s.length <= 105
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个二进制字符串（binary string）`s`，你可以将 `s` 划分为 3 个非空字符串 `s1`、`s2` 和 `s3`，满足 `s1 + s2 + s3 = s`。  
返回将 `s` 划分成满足 `s1`、`s2`、`s3` 中 `'1'` 的数量相同的方案数。由于答案可能非常大，请返回 **模** `10^9 + 7` 的结果。

**示例 1**  
```text
Input: s = "10101"
Output: 4
Explanation: 有四种划分方式使得每段包含相同数量的字符 '1'。
"1|010|1"
"1|01|01"
"10|10|1"
"10|1|01"
```

**示例 2**  
```text
Input: s = "1001"
Output: 0
```

**示例 3**  
```text
Input: s = "0000"
Output: 3
Explanation: 有三种划分方式将 `s` 分成 3 段。
"0|0|00"
"0|00|0"
"00|0|0"
```

**约束条件**

- `3 <= s.length <= 10^5`
- `s[i]` 只能是 `'0'` 或 `'1'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串 `s` 的所有可能的切分点都枚举出来，看看每一种切法是否满足“三段 `1` 的个数相等”。  
因为我们要把 `s` 分成 **3** 段，需要选两个切分点 `i`、`j`（`0 < i < j < len(s)`），于是：

```
s1 = s[0 : i]          # 前 i 个字符
s2 = s[i : j]          # i~j-1
s3 = s[j : ]           # j~结束
```

对每一种 `(i, j)`，统计 `s1、s2、s3` 中 `'1'` 的个数是否相同即可。

> **类比**：想象我们在一条长队列里插两根木棍，把队列分成三段，逐段数有多少红衣服的人（`'1'`），看三段人数是否相等。

要快速得到每段 `'1'` 的数量，可以先算一次 **前缀和**（prefix sum）：

```
pre[k] = s[0:k] 中 '1' 的个数，pre[0] = 0
```

有了前缀和后，任意区间 `[l, r)`（左闭右开）的 `'1'` 数为 `pre[r] - pre[l]`，查询是 O(1) 的。

**为什么正确**：我们穷举了所有合法的切点组合，且每次检查都用了准确的 `'1'` 计数，符合题意。

**时间/空间复杂度**：  
- 枚举 `i`、`j` 两层循环，最多 `n·(n-1)/2` 次检查，时间是 **O(n²)**。  
- 前缀和数组占 `n+1` 个整数，空间是 **O(n)**。  
> **大白话**：如果 `n = 10⁵`，O(n²) 就像让 10⁵ × 10⁵ = 10⁰¹⁰ 次小学生做加法，根本跑不完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numWays_bruteforce(s: str) -> int:
    n = len(s)
    # 1️⃣ 先算前缀和，pre[k] 表示前 k 个字符中 '1' 的个数
    pre = [0] * (n + 1)
    for i, ch in enumerate(s, 1):
        pre[i] = pre[i - 1] + (ch == '1')   # ch == '1' 为 True(1) 或 False(0)

    ans = 0
    # 2️⃣ 双层循环枚举切点 i、j
    for i in range(1, n - 1):          # i 不能在最左或最右
        for j in range(i + 1, n):
            cnt1 = pre[i] - pre[0]          # s1 中的 '1'
            cnt2 = pre[j] - pre[i]          # s2 中的 '1'
            cnt3 = pre[n] - pre[j]          # s3 中的 '1'
            if cnt1 == cnt2 == cnt3:
                ans += 1
                if ans >= MOD:               # 防止整数溢出，随时取模
                    ans -= MOD
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  > 对于 `n = 10⁵` 这种规模，计算量大约是 10⁰¹⁰ 次，远超常规机器的处理能力，实际会超时。

- **空间复杂度**：`O(n)`  
  > 只用了一个长度为 `n+1` 的前缀和数组，额外的空间需求随输入线性增长。

---

### 2. 最优解

#### 思路  

从暴力解看出 **瓶颈** 在于枚举所有 `i、j`，导致二次循环。  
观察题目可以发现：

1. 只关心每段 **'1' 的个数**，而不是具体字符。  
2. 若总的 `'1'` 个数记为 `total`，要把它平分成三段，**必须** `total % 3 == 0`。否则根本不可能。

接下来分两种情况讨论：

| 情况 | 说明 |
|------|------|
| **total = 0** | 整个字符串全是 `'0'`，任何切法都满足“每段 `'1'` 数相等（都是 0）”。只要在 `n-1` 个可能的切点中任选两个即可，组合数为 `C(n-1, 2)`。 |
| **total > 0 且 total % 3 == 0** | 设 `k = total / 3` 为每段应有的 `'1'` 数。我们只需要找出 **第 k 个 `'1'` 的位置** 和 **第 2k 个 `'1'` 的位置**，以及它们后面（前面）连续的 `'0'` 有多少。|

**关键观察**：

- 第 1 段 `s1` 必须以第 `k` 个 `'1'` 为结尾（或者更早，只要 `'1'` 数仍为 `k`）。如果第 `k` 个 `'1'` 后面有 `z1` 个连续的 `'0'`，那么 `s1` 的右边界可以在这 `z1+1` 个位置之间任选（包括恰好在第 `k` 个 `'1'` 后面）。
- 同理，第 2 段 `s2` 必须以第 `2k` 个 `'1'` 为结尾，且第 `2k` 个 `'1'` 前面有 `z2` 个连续的 `'0'`（即第 `k` 个 `'1'` 与第 `2k` 个 `'1'` 之间的零）。`s2` 的左边界可以在这 `z2+1` 种位置之间任选。

于是 **合法切法的总数** = `(z1 + 1) * (z2 + 1)`。

> **类比**：想象把三段 `'1'` 看成三根木棍，木棍之间的空白（`'0'`）可以自由伸缩。每段左/右的空白有几种摆放方式，就决定了整体切法的组合数。

**实现步骤**：

1. 统计 `total`（一次遍历）。
2. 若 `total % 3 != 0` → 返回 `0`。  
   若 `total == 0` → 返回组合数 `C(n-1, 2) % MOD`（使用公式 ` (n-1)*(n-2)//2`）。
3. 否则设 `k = total // 3`。再次遍历字符串，记录：
   - 第 `k` 个 `'1'` 出现的位置 `pos1`（下标从 0 开始）。
   - 第 `2k` 个 `'1'` 出现的位置 `pos2`。
4. 计算 `z1 = number of consecutive '0' after pos1`（从 `pos1+1` 开始向右数，直到遇到下一个 `'1'` 或结束）。
   同理 `z2 = number of consecutive '0' before pos2`（从 `pos2-1` 向左数）。
5. 返回 `(z1 + 1) * (z2 + 1) % MOD`。

**时间复杂度**：只需要 **两次线性遍历**，即 `O(n)`。  
**空间复杂度**：只用常数级变量 `O(1)`（不需要额外数组），极其轻量。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numWays(s: str) -> int:
    n = len(s)
    total = s.count('1')                # 统计全部 '1' 的个数，O(n)

    # 1️⃣ total 不能被 3 整除 → 没办法平分
    if total % 3 != 0:
        return 0

    # 2️⃣ 全部都是 '0' 的特殊情况
    if total == 0:
        # 在 n-1 个切点里任选两个，组合数 C(n-1, 2)
        return ((n - 1) * (n - 2) // 2) % MOD

    # 3️⃣ total 能被 3 整除，求每段应有的 '1' 个数
    k = total // 3

    # 第 k 个和第 2k 个 '1' 的下标
    first_k_idx = second_k_idx = -1
    cnt = 0
    for i, ch in enumerate(s):
        if ch == '1':
            cnt += 1
            if cnt == k:
                first_k_idx = i
            elif cnt == 2 * k:
                second_k_idx = i
                break                     # 找到第二个目标后可以提前结束

    # 4️⃣ 统计 first_k_idx 右边连续的 '0' 数量
    zeros_after_first = 0
    i = first_k_idx + 1
    while i < n and s[i] == '0':
        zeros_after_first += 1
        i += 1

    # 5️⃣ 统计 second_k_idx 左边连续的 '0' 数量
    zeros_before_second = 0
    i = second_k_idx - 1
    while i >= 0 and s[i] == '0':
        zeros_before_second += 1
        i -= 1

    # 6️⃣ 组合计数 (z1+1)*(z2+1) 并取模
    ans = (zeros_after_first + 1) * (zeros_before_second + 1)
    return ans % MOD
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  > 只遍历字符串两遍（一次 `count`，一次找 `k`、`2k`），即使 `n = 10⁵` 也毫秒级完成。

- **空间复杂度**：`O(1)`  
  > 只用了若干整数变量，不随 `n` 增长。

> 与暴力解相比，时间从 **平方级** 降到了 **线性级**，在大数据量下立刻从“卡死”变成“瞬间返回”。  

---

## 心得

- **核心技巧**：把“等量划分”转化为“找特定第几位的 1”，再利用相邻 0 的数量计数组合。  
- **适用的题型**  
  1. “把数组/字符串分成 k 段，使每段的和相等”——比如 “Split Array With Same Average”。  
  2. “在二进制/数字序列中找等量子段”——比如 “Number of Ways to Split an Array”。  
  3. “计数满足特定前缀/后缀条件的切法”——比如 “Count Binary Substrings”。  
- **一句话总结解题钥匙**：**先判断是否可能平分（除以 3），再统计分界点两侧的自由零位，用乘法组合计数**。

---

## 反思

- **第一反应**：直接枚举所有切点，写出双层循环检查 `'1'` 个数。  
- **最容易踩的坑**  
  - 忘记对答案取模 `10⁹+7`，导致整数溢出。  
  - 对全零情况处理不当：`total == 0` 时仍需要组合计数，而不是返回 `0`。  
  - 计算 `zeros_after_first`、`zeros_before_second` 时越界或遗漏最后一个 `'0'`。  
- **下次遇到同类题**：第一步先检查 **整体可否平分**（总和是否能被段数整除），再定位 **第一个/第二个/…关键元素** 的位置，最后统计 **关键位置两侧的自由度**（零/空白的数量）乘积得到答案。