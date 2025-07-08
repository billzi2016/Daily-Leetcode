# #3258. 计数满足 K 约束的子串 I / Count Substrings That Satisfy K-Constraint I

> 难度：简单 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-substrings-that-satisfy-k-constraint-i/)

---

## 题目（英文原版）

**Description**

You are given a binary string s and an integer k.
A binary string satisfies the k-constraint if either of the following conditions holds:
Return an integer denoting the number of substrings of s that satisfy the k-constraint.

**Examples**

**Example 1:**

```
Input: s = "10101", k = 1
Output: 12
Explanation:
Every substring of s except the substrings "1010" , "10101" , and "0101" satisfies the k-constraint.
```

**Example 2:**

```
Input: s = "1010101", k = 2
Output: 25
Explanation:
Every substring of s except the substrings with a length greater than 5 satisfies the k-constraint.
```

**Example 3:**

```
Input: s = "11111", k = 1
Output: 15
Explanation:
All substrings of s satisfy the k-constraint.
```

**Constraints**

- 1 <= s.length <= 50
- 1 <= k <= s.length
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个二进制字符串 `s` 和一个整数 `k`。  
如果二进制字符串满足下列任意一个条件，则称其满足 **k-约束**（k‑constraint）：

1. 字符串中 `'0'` 的数量不超过 `k`；  
2. 字符串中 `'1'` 的数量不超过 `k`。  

返回 `s` 的子串（substrings）中满足 k‑约束的子串数量。

**示例 1**  
```
Input: s = "10101", k = 1
Output: 12
Explanation:
除了子串 "1010"、"10101" 和 "0101" 之外，s 的所有子串都满足 k‑约束。
```

**示例 2**  
```
Input: s = "1010101", k = 2
Output: 25
Explanation:
除了长度大于 5 的子串之外，s 的所有子串都满足 k‑约束。
（长度为 6 或 7 的子串分别为 "101010"、"010101"、"1010101"，它们的 '0' 与 '1' 数量均超过 2。）
```

**示例 3**  
```
Input: s = "11111", k = 1
Output: 15
Explanation:
所有子串均满足 k‑约束，因为它们的 '0' 数量为 0，满足条件 1。
```

**约束条件**  

- `1 <= s.length <= 50`  
- `1 <= k <= s.length`  
- `s[i]` 只能是 `'0'` 或 `'1'`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的办法是把所有可能的子串枚举出来，逐一检查它们是否满足 **k‑constraint**。  
- **枚举子串**：对每一个左端点 `i`，把右端点 `j` 从 `i` 向右移动，形成子串 `s[i..j]`。这相当于把字符串看成一本书的每一页，然后把每一页的所有可能的起始位置和结束位置都列出来。  
- **检查条件**：统计子串里 `'0'` 的个数 `cnt0` 与 `'1'` 的个数 `cnt1`。只要 `cnt0 ≤ k` **或** `cnt1 ≤ k`，这段子串就算满足 k‑constraint。这里的 **或** 就像字典查词一样，只要找到了符合条件的键（`cnt0` 或 `cnt1` 小于等于 `k`），就可以直接返回对应的页码（即这段子串有效）。  

为什么这能得到正确答案？因为我们把 **所有** 子串都检查了一遍，凡是满足条件的必然被计数，凡是不满足的必然被过滤掉。

**复杂度分析（大白话）**  
- **时间**：外层循环 `i` 有 `n` 次，内层循环 `j` 最多也会遍历 `n` 次，总共大约 `n·n/2` 次检查，记作 **O(n²)**。把 `n=50` 代进去，大概是 2500 次操作，完全可以接受。  
- **空间**：只用了几个计数器（`cnt0、cnt1、ans`），不随 `n` 增长，记作 **O(1)**（常数空间）。  

#### 代码（Python）

```python
def count_substrings_bruteforce(s: str, k: int) -> int:
    n = len(s)
    ans = 0                                 # 最终答案
    for i in range(n):                      # 左端点
        cnt0 = cnt1 = 0                      # 当前子串里 0/1 的个数
        for j in range(i, n):                # 右端点
            if s[j] == '0':
                cnt0 += 1
            else:
                cnt1 += 1
            # 只要 0 的个数 ≤ k 或 1 的个数 ≤ k，就满足 k‑constraint
            if cnt0 <= k or cnt1 <= k:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：**O(n²)** —— 两层循环遍历所有子串，`n` 为字符串长度。  
- **空间复杂度**：**O(1)** —— 只使用了固定数量的整数变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于我们对每个子串都重新统计 `'0'`、`'1'` 的个数，导致二次遍历。  
如果我们在遍历的过程中 **维护** 这两个计数，而不是每次都重新计算，就能把时间降到线性。  

下面把问题拆成三个子问题：

1. **只关心 `'0'` 的个数**：统计满足 `cnt0 ≤ k` 的子串数。  
2. **只关心 `'1'` 的个数**：统计满足 `cnt1 ≤ k` 的子串数。  
3. **两者都满足**：统计满足 `cnt0 ≤ k 且 cnt1 ≤ k` 的子串数（即两次都满足的子串会被前面两步重复计数，需要在最终答案里减去一次）。  

这三个子问题都可以用 **滑动窗口（双指针）** 线性求解。  

**滑动窗口的类比**：把字符串想成一条流水线，窗口 `[left, right]` 表示当前正在“加工”的这段原料。我们让右指针 `right` 不断向前推，窗口里累计的 `'0'`（或 `'1'`）个数随之增加；如果超过了 `k`，就让左指针 `left` 向前移动，直到窗口再次合法。此时，所有以 `right` 为右端点、左端点在 `[left, right]` 之间的子串都是合法的，它们的数量正好是 `right - left + 1`。  

下面分别实现这三个计数：

- **计数仅限制 `'0'`**：窗口中 `'0'` 的个数 ≤ `k`。  
- **计数仅限制 `'1'`**：窗口中 `'1'` 的个数 ≤ `k`（把 `'0'` 换成 `'1'` 同理）。  
- **计数同时限制**：窗口中 `'0'` 与 `'1'` 的个数都 ≤ `k`，只要有一种超过 `k`，就把左指针左移，直到两者都 ≤ `k`。  

最后答案 = `cnt_zero + cnt_one - cnt_both`（减去重复计数的交集）。

**为什么是最优的？**  
- 每个指针只会左移或右移 **一次**，整个过程最多走 `2·n` 步，时间是 **O(n)**。  
- 只用几个计数器，空间仍是 **O(1)**。  

#### 代码（Python）

```python
def count_substrings_opt(s: str, k: int) -> int:
    n = len(s)

    # 统计窗口中 cnt0 <= k 的子串数
    def count_limit(char: str) -> int:
        left = 0
        cnt = 0          # 当前窗口里 char 的个数
        total = 0
        for right in range(n):
            if s[right] == char:
                cnt += 1
            # 超出限制，左指针收缩
            while cnt > k:
                if s[left] == char:
                    cnt -= 1
                left += 1
            # 以 right 为右端点的合法子串数量 = right - left + 1
            total += right - left + 1
        return total

    # 只限制 '0' 或只限制 '1'
    cnt_zero = count_limit('0')
    cnt_one  = count_limit('1')

    # 同时限制 '0' 与 '1'（即两者都 ≤ k）
    left = 0
    cnt0 = cnt1 = 0
    cnt_both = 0
    for right in range(n):
        if s[right] == '0':
            cnt0 += 1
        else:
            cnt1 += 1
        # 任意一种超过 k，都需要收缩左边界
        while cnt0 > k or cnt1 > k:
            if s[left] == '0':
                cnt0 -= 1
            else:
                cnt1 -= 1
            left += 1
        cnt_both += right - left + 1   # 同时满足的子串数

    # 使用容斥原理：A∪B = |A| + |B| - |A∩B|
    return cnt_zero + cnt_one - cnt_both
```

#### 复杂度  

- **时间复杂度**：**O(n)** —— 每个字符最多被左指针和右指针各访问一次。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：**O(1)** —— 只用常数个整数变量。

---

## 心得  

- **核心技巧**：**滑动窗口 + 容斥原理**。滑动窗口负责在线性时间内统计满足单一上限的子串，容斥原理用于合并 “只限制 0” 与 “只限制 1” 两个计数，去掉重复计数的交集。  
- **适用题型**：  
  1. “子数组/子串个数 ≤ K 的限制”——如 “Count Subarrays With Bounded Maximum”。  
  2. “至少/至多出现 K 次字符/数字”——如 “Longest Substring with At Most K Distinct Characters”。  
  3. “满足两个或多个上限的计数”——如本题的 “0、1 同时受限”。  
- **一句话总结**：**把“或”转化为两个单独的“≤k”计数，再用容斥去掉交集，即可在线性时间完成计数。**

---

## 反思  

- **第一反应**：看到“或”条件，立刻想到枚举所有子串并逐个检查——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记 **容斥**，直接把 `cnt_zero + cnt_one` 当作答案，会把两者都满足的子串算两次。  
  - 在实现滑动窗口时，左指针的收缩条件写错（比如只检查 `cnt0 > k`，却忘了 `cnt1 > k`），会导致窗口非法，从而统计错误。  
- **下次类似题**：第一步先问自己 “是否可以把复杂的‘或/且’条件拆成几个单独的上限”，然后判断是否可以用 **滑动窗口** 线性统计每个上限，最后用 **容斥** 合并结果。这样思路清晰、实现稳妥。