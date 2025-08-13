# #3303. 寻找首个几乎相等子串的出现位置 / Find the Occurrence of First Almost Equal Substring

> 难度：困难 · 标签：String、String Matching · [LeetCode 链接](https://leetcode.com/problems/find-the-occurrence-of-first-almost-equal-substring/)

---

## 题目（英文原版）

**Description**

You are given two strings s and pattern.
A string x is called almost equal to y if you can change at most one character in x to make it identical to y.
Return the smallest starting index of a substring in s that is almost equal to pattern. If no such index exists, return -1.

**Examples**

**Example 1:**

```
Input: s = "abcdefg", pattern = "bcdffg"
Output: 1
Explanation:
The substring s[1..6] == "bcdefg" can be converted to "bcdffg" by changing s[4] to "f" .
```

**Example 2:**

```
Input: s = "ababbababa", pattern = "bacaba"
Output: 4
Explanation:
The substring s[4..9] == "bababa" can be converted to "bacaba" by changing s[6] to "c" .
```

**Example 3:**

```
Input: s = "abcd", pattern = "dba"
Output: -1
```

**Example 4:**

```
Input: s = "dde", pattern = "d"
Output: 0
```

**Constraints**

- 1 <= pattern.length < s.length <= 105
- s and pattern consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `pattern`。  
如果可以通过最多修改 `x` 中的一个字符，使其完全相同于 `y`，则称字符串 `x` **几乎相等**（almost equal）于 `y`。  
返回 `s` 中**最小的**起始下标，使得该下标对应的子串（substring）**几乎相等**于 `pattern`。如果不存在这样的下标，返回 `-1`。

### 示例

#### 示例 1
**输入**: `s = "abcdefg", pattern = "bcdffg"`  
**输出**: `1`  
**解释**: 子串 `s[1..6] == "bcdefg"` 只需将 `s[4]` 改为 `'f'` 即可得到 `"bcdffg"`。

#### 示例 2
**输入**: `s = "ababbababa", pattern = "bacaba"`  
**输出**: `4`  
**解释**: 子串 `s[4..9] == "bababa"` 只需将 `s[6]` 改为 `'c'` 即可得到 `"bacaba"`。

#### 示例 3
**输入**: `s = "abcd", pattern = "dba"`  
**输出**: `-1`

#### 示例 4
**输入**: `s = "dde", pattern = "d"`  
**输出**: `0`

### 约束条件
- `1 <= pattern.length < s.length <= 10^5`
- `s` 与 `pattern` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 `s` 中所有长度等于 `pattern` 的子串全部枚举出来，逐个和 `pattern` 对比，统计它们之间不同字符的个数，只要这个数 **≤ 1** 就说明该子串「几乎相等」——此时返回它的左端点下标。  

- **枚举子串**：把滑动窗口的左端点 `i` 从 `0` 移动到 `len(s)-len(pattern)`，窗口大小固定为 `m = len(pattern)`。  
- **逐字符比较**：用一个计数器 `diff` 记录 `s[i+j]` 与 `pattern[j]` 不同的次数，遍历 `j = 0 … m-1`。  
- **判断**：如果遍历结束后 `diff ≤ 1`，说明找到了答案，直接返回 `i`。若全部窗口都没有满足条件，返回 `-1`。  

**为什么正确**  
只要我们把所有可能的子串都检查了一遍，且每次检查的规则（不同字符不超过一个）正好是题目要求的「几乎相等」的定义，那么必然能够找到最左侧的符合条件的下标。  

**时间/空间复杂度**  
- 时间复杂度：外层遍历 `O(n)`（`n = len(s)`），内层比较 `O(m)`（`m = len(pattern)`），总计 `O(n·m)`。在最坏情况下（比如 `n≈10⁵，m≈5·10⁴`），这几乎是不可接受的。  
- 空间复杂度：只用了常数级的额外变量 `diff、i、j`，所以是 `O(1)`。  

> **大白话解释**：  
> `O(n·m)` 就像让 10 万个人每人都读 5 万页书——显然太慢了。我们需要把「读」的次数降下来。

#### 代码（Python）

```python
def first_almost_equal_bruteforce(s: str, pattern: str) -> int:
    n, m = len(s), len(pattern)
    # i 为窗口左端点
    for i in range(n - m + 1):
        diff = 0                     # 记录不同字符的个数
        for j in range(m):
            if s[i + j] != pattern[j]:
                diff += 1
                if diff > 1:        # 超过一个不可能满足条件，提前结束本次比较
                    break
        if diff <= 1:                # 找到答案
            return i
    return -1                        # 没有任何符合条件的子串
```

#### 复杂度  

- **时间复杂度**：`O(n·m)` —— 每个起始位置都要逐字符比较，等价于「n × m 次比较」。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，没有随输入规模增长的额外存储。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于对每个窗口都要重新比较 `m` 次字符。  
如果我们能一次性算出 **“从某个位置开始，能匹配 pattern 前缀的最长长度”**，以及 **“在某个位置结束，能匹配 pattern 后缀的最长长度”**，那么判断一个窗口是否只差一个字符就可以 **O(1)** 完成。

**核心工具**：  
- **Z‑算法**（或叫 Z 函数）可以在 `O(n+m)` 时间内求出「一个字符串的每个位置起始的最长公共前缀长度」。  
- 把 `pattern` 与 `s` 拼接成 `pattern + "#" + s`，跑 Z 算法即可得到 `dp1[i]` —— 从 `s[i]` 开始向右，能匹配 `pattern` 前缀的最长长度。  
- 同理，**反转**两串后再跑一次 Z 算法，可得到 `dp2[i]` —— 从 `s[i]` 向左，能匹配 `pattern` 后缀的最长长度（这里把下标映射回原串）。  

**为什么这样能判断**  
设窗口左端点为 `i`，长度为 `m`，右端点为 `r = i + m - 1`。  
- `dp1[i]` 表示窗口左边从 `i` 开始连续匹配的字符数（即匹配 pattern 前缀的长度）。  
- `dp2[r]` 表示窗口右边从 `r` 往左连续匹配的字符数（即匹配 pattern 后缀的长度）。  

如果这两个匹配段 **覆盖了整个 pattern，除去至多一个字符**，说明窗口只差一个字符。数学上等价于：

```
dp1[i] + dp2[r] >= m - 1
```

（因为 `m` 个字符中最多可以有 1 个不匹配，其余 `m-1` 必须被前缀或后缀匹配覆盖）。

遍历所有合法的 `i`，第一个满足该不等式的即为答案。整个过程只需要两次线性扫描，时间 `O(n+m)`，空间 `O(n+m)`（存储 dp 数组）。

**类比**：  
- `dp1` 像一本词典里「查前缀」的功能，给定一个起始位置，它直接告诉我们能匹配多少个连续的字母。  
- `dp2` 则是「查后缀」的功能，只不过我们把字符串倒着读，得到的仍然是「从某点往左」的连续匹配长度。

#### 代码（Python）

```python
def z_function(s: str):
    """返回字符串 s 的 Z 数组，时间 O(len(s))"""
    n = len(s)
    z = [0] * n
    l, r = 0, 0          # 当前维护的 [l, r] 区间，内部全部与前缀相等
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def first_almost_equal(s: str, pattern: str) -> int:
    n, m = len(s), len(pattern)
    if m > n:                         # 题目保证 m < n，这里防御性写一下
        return -1

    # ---------- 计算 dp1 ----------
    # 把 pattern 与 s 用特殊字符 # 隔开，防止跨界匹配
    combined = pattern + "#" + s
    z = z_function(combined)
    # dp1[i] 对应 combined 中下标 m+1+i 的 Z 值
    dp1 = [0] * n                     # dp1[i] = 从 s[i] 开始匹配的前缀长度
    offset = m + 1
    for i in range(n):
        dp1[i] = min(z[offset + i], m)   # 不能超过 pattern 长度

    # ---------- 计算 dp2 ----------
    rev_s = s[::-1]
    rev_pat = pattern[::-1]
    combined_rev = rev_pat + "#" + rev_s
    z_rev = z_function(combined_rev)
    dp2_rev = [0] * n                 # 在翻转后字符串中的值
    for i in range(n):
        dp2_rev[i] = min(z_rev[offset + i], m)

    # 把翻转坐标映射回原串：原串位置 i 对应翻转后的位置 n-1-i
    dp2 = [0] * n
    for i in range(n):
        dp2[i] = dp2_rev[n - 1 - i]

    # ---------- 滑动窗口检查 ----------
    for i in range(n - m + 1):
        r = i + m - 1
        # 前缀匹配长度 + 后缀匹配长度 至少覆盖 m-1 个字符
        if dp1[i] + dp2[r] >= m - 1:
            return i
    return -1
```

> **代码要点注释**  
> - `z_function`：经典的线性 Z 算法，实现细节里用了 “左端点 l、右端点 r” 来维护已经匹配好的区间，避免重复比较。  
> - `dp1[i]`、`dp2[i]`：分别是前缀匹配和后缀匹配的最长长度，取 `min(..., m)` 是因为即使 Z 值更大，也只能匹配到 pattern 的全部。  
> - 翻转后再映射回原坐标的过程是关键，确保 `dp2[r]` 表示 *从窗口右端向左* 能匹配多少个 pattern 的后缀字符。  

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 两次 Z 算法各 `O(n + m)`，随后一次线性遍历检查窗口 `O(n)`。整体线性，远快于暴力的 `O(n·m)`。  
- **空间复杂度**：`O(n + m)`  
  - 需要保存 `z`、`dp1`、`dp2` 等数组，大小与输入长度同阶。相较于只用常数空间，这是换取线性时间的合理代价。

---

## 心得  

- **核心技巧**：利用 **Z 算法**（或等价的前缀函数）一次性得到所有位置的最长公共前缀/后缀长度，从而把「逐字符比较」压缩到 **O(1)**。  
- **适用题型**  
  1. “最长公共前缀/后缀”类匹配问题（如 LeetCode 1063：**Number of Valid Subarrays** 的前缀/后缀技巧）。  
  2. “最多 k 次不同字符” 的子串搜索（如 “最多 K 次替换后相等的子串”）。  
  3. “循环移位匹配” 或 “最小编辑距离 ≤ 1” 的判定（利用前后缀覆盖）。  
- **一句话总结解题钥匙**：**把“每次比较 m 个字符”变成“预处理一次，后续只用常数时间检查”。**

---

## 反思  

- **第一反应**：直接枚举窗口并逐字符比较——最自然也最容易想到的暴力法。  
- **最容易踩的坑**  
  - **边界条件**：当 `pattern` 长度为 1 时，任何匹配或单字符不匹配都算「几乎相等」；代码必须能正确返回 `0`。  
  - **翻转坐标映射**：容易写错 `dp2` 的下标，导致后缀匹配长度对应错误位置。  
  - **Z 值超过 pattern 长度**：需要 `min(z, m)`，否则会误判。  
- **下次遇到同类题**，第一步应该想到 **“预处理前后缀匹配长度”**（使用 Z、KMP 前缀函数或哈希），而不是直接暴力比较。这样可以把时间从二次方降到线性。