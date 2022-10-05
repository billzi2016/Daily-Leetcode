# #1960. 最大化两个奇数长度回文子串长度的乘积 / Maximum Product of the Length of Two Palindromic Substrings

> 难度：困难 · 标签：String、Rolling Hash、Hash Function · [LeetCode 链接](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-substrings/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s and are tasked with finding two non-intersecting palindromic substrings of odd length such that the product of their lengths is maximized.
More formally, you want to choose four integers i, j, k, l such that 0 <= i <= j < k <= l < s.length and both the substrings s[i...j] and s[k...l] are palindromes and have odd lengths. s[i...j] denotes a substring from index i to index j inclusive.
Return the maximum possible product of the lengths of the two non-intersecting palindromic substrings.
A palindrome is a string that is the same forward and backward. A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: s = "ababbb"
Output: 9
Explanation: Substrings "aba" and "bbb" are palindromes with odd length. product = 3 * 3 = 9.
```

**Example 2:**

```
Input: s = "zaaaxbbby"
Output: 9
Explanation: Substrings "aaa" and "bbb" are palindromes with odd length. product = 3 * 3 = 9.
```

**Constraints**

- 2 <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

你得到一个 **0-indexed**（从 0 开始计数）字符串 `s`，需要找出两个**不相交**（non‑intersecting）的**奇数长度**（odd length）回文子串（palindrome），使它们长度的乘积最大。

更形式化地说，选择四个整数 `i, j, k, l`，满足  

`0 ≤ i ≤ j < k ≤ l < s.length`，且子串 `s[i...j]` 与 `s[k...l]` 都是回文且长度为奇数。`s[i...j]` 表示从下标 `i` 到下标 `j`（包含两端）的**子串 (substring)**。

返回这两个不相交的奇数长度回文子串长度乘积的**最大可能值**。

**回文**（palindrome）是指正读和反读完全相同的字符串。**子串**（substring）是字符串中连续的一段字符序列。

---

### 示例

**示例 1**  
Input: `s = "ababbb"`  
Output: `9`  
Explanation: 子串 `"aba"` 与 `"bbb"` 均为奇数长度的回文，乘积为 `3 * 3 = 9`。

**示例 2**  
Input: `s = "zaaaxbbby"`  
Output: `9`  
Explanation: 子串 `"aaa"` 与 `"bbb"` 均为奇数长度的回文，乘积为 `3 * 3 = 9`。

---

### 约束条件

- `2 ≤ s.length ≤ 10^5`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的奇数长度子串都枚举出来**，逐个判断它们是否是回文，然后在所有满足“互不相交”的两段回文子串里挑选长度乘积最大的那对。

- **枚举子串**：我们可以用两层循环 `i`（子串左端）和 `j`（子串右端），只保留 `j-i+1` 为奇数的情况。
- **回文判定**：把子串从左往右和从右往左对比，像检查单词是否正着读和倒着读相同一样。可以把它想象成“把字母排成一列，然后从两端往中间走，看到的字母是否一直匹配”。  
- **两段不相交**：如果左段的右端 `j` 小于右段的左端 `k`，说明它们没有交叉，满足题目要求。
- **最大乘积**：遍历所有合法的两段回文，记录 `len1 * len2` 的最大值。

> **为什么能得到正确答案**  
> 暴力法把**所有**可能的奇数回文子串都列举出来，并且检查**每一种**合法的两段组合。只要答案存在，它一定会在遍历过程中被比较到，自然能得到最大乘积。

#### 代码（Python）

```python
def maxProduct(s: str) -> int:
    n = len(s)
    # 保存所有奇数回文子串的信息： (左端, 右端, 长度)
    palins = []

    # ---------- 枚举所有奇数子串 ----------
    for i in range(n):
        # 只需要以 i 为中心向两边展开，奇数长度的回文一定有一个中心字符
        l = r = i
        while l >= 0 and r < n and s[l] == s[r]:
            # 当前子串 s[l..r] 是回文，长度是 r-l+1（必为奇数）
            palins.append((l, r, r - l + 1))
            l -= 1
            r += 1

    # ---------- 两两组合求最大乘积 ----------
    ans = 0
    m = len(palins)
    for a in range(m):
        l1, r1, len1 = palins[a]
        for b in range(a + 1, m):
            l2, r2, len2 = palins[b]
            # 判断两段是否不相交（左段在前，右段在后）
            if r1 < l2 or r2 < l1:
                ans = max(ans, len1 * len2)

    return ans
```

- 第 8~14 行：以每个字符为中心向两边展开，找到所有以该字符为中心的奇数回文子串。  
- 第 19~29 行：两层循环遍历所有回文子串的组合，检查是否不相交并更新最大乘积。

#### 复杂度

- **时间复杂度**：`O(n³)`（最坏情况下）  
  - 枚举所有回文子串本身是 `O(n²)`（每个中心最多展开 `O(n)` 次）。  
  - 再把这些子串两两组合检查，最坏会有 `O(n²)` 个子串，两两比较是 `O(n⁴)`，但实际因为每个中心只能展开一次，整体约为 `O(n³)`。  
  - **大白话**：如果字符串长度是 1000，程序大概要跑 1000³ = 10⁹ 次操作，明显会超时。

- **空间复杂度**：`O(n²)` 用来存所有回文子串的信息。  
  - 每找到一个回文，就把它的左、右、长度保存下来，最坏情况下（如全部字符相同）会有 `≈ n²/2` 条记录。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有回文子串并两两比较**，导致时间爆炸。我们需要：

1. **快速得到每个位置的最长奇数回文半径**（即以该位置为中心的最大回文长度），这一步可以在 `O(n)` 完成。  
2. **把信息压缩为“前缀最优长度”和“后缀最优长度”**，这样只需要一次线性遍历就能求出答案。

下面一步步推导：

##### a. 用 Manacher 算法求奇数回文半径  

Manacher 算法是一种线性时间的“回文检测器”。它的核心思想是**利用已经算好的回文信息，帮助后面的中心快速跳过不必要的比较**。可以把它想象成：

- 你在一条路上检查每个灯塔（字符）能看到的最远的对称灯塔（回文边界），  
- 当你已经知道某段灯塔之间的视野（回文）很大时，后面的灯塔只需要在这段视野内部做少量检查。

实现时我们维护两个变量：

- `center`：当前已知的最右侧回文的中心  
- `right`：该回文的最右端位置  

对于每个新位置 `i`，如果它在 `right` 之内，我们可以直接把它对应的半径设为 `min(radius[mirror], right - i)`，其中 `mirror = 2*center - i` 是 `i` 关于 `center` 的对称位置。随后再**向左右扩展**验证是否还能更长。

得到的 `rad[i]` 表示以 `i` 为中心，能够向左、向右各扩展 `rad[i]` 个字符，奇数回文的完整长度为 `2*rad[i] + 1`。

##### b. 把每个位置的最长回文“投射”到左/右端  

有了 `rad[i]`，我们知道：

- 以 `i` 为中心的最长奇数回文覆盖区间 `[i - rad[i], i + rad[i]]`。

我们希望得到：

- `pref[i]`：**在子串 `s[0..i]`（左边界到 i）里**出现的**最长奇数回文的长度**。  
- `suf[i]`：**在子串 `s[i..n-1]`（i 到右端）里**出现的**最长奇数回文的长度**。

这样答案就可以写成：

```
max_{0 <= i < n-1}  pref[i] * suf[i+1]
```

因为左侧回文全部在 `[0..i]`，右侧回文全部在 `[i+1..n-1]`，两者必然不相交。

如何求 `pref`、`suf`？

- **左扫**（从左到右）：遍历每个中心 `c`，它的回文左端是 `L = c - rad[c]`，右端是 `R = c + rad[c]`。  
  对于所有 `pos` 在 `[L, R]` 之间的 **右端**，这段回文都可以“落在” `pos` 位置。我们只关心 **右端的最大长度**，因此可以用一个变量 `best` 记录当前遍历到的最大回文长度，并在每个位置更新 `pref[pos] = max(pref[pos-1], best)`。

  更直观的做法是：**对每个中心，把它能产生的最大长度写到它的右端位置**，随后一次前缀最大即可。

- **右扫**（从右到左）同理，只是把信息写到左端位置，再做一次后缀最大。

实现细节（左扫）：

```text
pref = [0] * n
for c in range(n):
    length = 2 * rad[c] + 1
    right = c + rad[c]               # 回文的最右端
    pref[right] = max(pref[right], length)
# 前缀最大：把每个位置的值向右传播
for i in range(1, n):
    pref[i] = max(pref[i], pref[i-1])
```

右扫类似，只是把 `length` 写到 `left = c - rad[c]`，然后做后缀最大。

##### c. 计算答案  

遍历一次分割点 `i`（左子串结束在 `i`），答案即 `max(pref[i] * suf[i+1])`。

> **核心技巧**  
> - 用 Manacher 把“所有奇数回文”压缩成 **每个中心的半径**，只需 `O(n)`。  
> - 再把每个中心的回文“投射”到左端/右端，转化为前缀/后缀最大问题，仍是线性时间。  
> - 最终只需要一次线性遍历得到最大乘积。

#### 代码（Python）

```python
def maxProduct(s: str) -> int:
    n = len(s)
    # ---------- 1. Manacher 求奇数回文半径 ----------
    rad = [0] * n               # rad[i] = 能向左/右扩展的字符数
    center = right = -1
    for i in range(n):
        # 如果 i 在已知回文区间内，先给一个保守的半径
        if i <= right:
            mirror = 2 * center - i
            rad[i] = min(rad[mirror], right - i)
        # 向左右扩展，检查字符是否相等
        while i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n and \
              s[i - rad[i] - 1] == s[i + rad[i] + 1]:
            rad[i] += 1
        # 更新最右回文区间
        if i + rad[i] > right:
            center, right = i, i + rad[i]

    # ---------- 2. 前缀最优长度 ----------
    pref = [0] * n          # pref[i] = 在 s[0..i] 中出现的最长奇数回文长度
    for c in range(n):
        length = 2 * rad[c] + 1          # 以 c 为中心的回文完整长度
        right_end = c + rad[c]           # 回文的最右端下标
        # 把这个长度写到最右端位置（可能已经有更大的）
        pref[right_end] = max(pref[right_end], length)

    # 前缀最大：把每个位置的值向右传播，使得 pref[i] = max_{j<=i} pref[j]
    for i in range(1, n):
        pref[i] = max(pref[i], pref[i - 1])

    # ---------- 3. 后缀最优长度 ----------
    suf = [0] * n           # suf[i] = 在 s[i..n-1] 中出现的最长奇数回文长度
    for c in range(n):
        length = 2 * rad[c] + 1
        left_end = c - rad[c]            # 回文的最左端下标
        suf[left_end] = max(suf[left_end], length)

    # 后缀最大：把每个位置的值向左传播，使得 suf[i] = max_{j>=i} suf[j]
    for i in range(n - 2, -1, -1):
        suf[i] = max(suf[i], suf[i + 1])

    # ---------- 4. 计算最大乘积 ----------
    ans = 0
    for i in range(n - 1):
        ans = max(ans, pref[i] * suf[i + 1])

    return ans
```

- 第 5~18 行：Manacher 主循环，`rad[i]` 保存以 `i` 为中心的最大扩展半径。  
- 第 22~28 行：把每个中心对应的回文长度写到它的最右端位置，随后做前缀最大得到 `pref`。  
- 第 31~38 行：同理写到最左端位置并做后缀最大得到 `suf`。  
- 第 41~44 行：遍历所有可能的分割点，求 `pref[i] * suf[i+1]` 的最大值。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - Manacher 本身是线性遍历一次 `O(n)`。  
  - 前缀、后缀最大以及最终遍历分割点各是一次线性扫描，合计仍是 `O(n)`。  
  - **对比暴力**：原来需要几乎 `n³` 次操作，现在只需要和字符串长度成正比的几次遍历，几乎瞬间就能得到答案。

- **空间复杂度**：`O(n)`  
  - 需要保存 `rad`、`pref`、`suf` 三个长度为 `n` 的数组。  
  - 只用了线性额外空间，符合题目 `n ≤ 10⁵` 的限制。

---

## 心得

- **核心技巧**：  
  1. **Manacher**：一次遍历得到所有奇数回文的最大半径。  
  2. **前缀/后缀最大**：把局部信息压缩成全局“左边最优”和“右边最优”，从而把两段回文的组合问题转化为一次线性扫描。

- **适用的题型**（类似思路）  
  - “两个不相交子数组/子串的最大和/乘积”  
  - “在字符串中找两段不重叠的最长回文（或最长相同子串）”  
  - “利用前缀/后缀最值快速求最优分割点”  

- **一句话总结解题钥匙**：  
  > 把“所有回文”压缩成每个中心的半径，用前缀/后缀最大把局部最长长度传播到全局，再一次线性遍历求最大乘积。

---

## 反思

- **第一反应**：直接枚举所有奇数子串并两两比较，代码写起来很直观，但很快发现会超时。  
- **最容易踩的坑**  
  1. **奇数长度限制**：忘记只考虑奇数回文，导致需要额外判断或错误计数。  
  2. **前缀/后缀最大传播顺序**：如果写成 `pref[i] = max(pref[i], pref[i+1])` 会得到错误的“后缀”信息。  
  3. **边界处理**：分割点 `i` 必须在 `0 … n-2`，否则 `suf[i+1]` 越界。  

- **下次遇到同类题**：  
  第一步先思考**是否可以把所有局部信息（如每个中心的回文）压缩成一维数组**，然后**通过前缀/后缀最大或单调栈等手段把信息传播到全局**，最后**只需一次线性遍历得到答案**。这样既能保证正确性，又能避免暴力的时间炸弹。