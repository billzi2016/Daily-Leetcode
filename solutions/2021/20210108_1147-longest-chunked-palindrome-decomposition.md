# #1147. **最长块回文分解** / Longest Chunked Palindrome Decomposition

> 难度：困难 · 标签：Two Pointers、String、Dynamic Programming、Greedy、Rolling Hash、Hash Function · [LeetCode 链接](https://leetcode.com/problems/longest-chunked-palindrome-decomposition/)

---

## 题目（英文原版）

**Description**

You are given a string text. You should split it to k substrings (subtext1, subtext2, ..., subtextk) such that:
Return the largest possible value of k.

**Examples**

**Example 1:**

```
Input: text = "ghiabcdefhelloadamhelloabcdefghi"
Output: 7
Explanation: We can split the string on "(ghi)(abcdef)(hello)(adam)(hello)(abcdef)(ghi)".
```

**Example 2:**

```
Input: text = "merchant"
Output: 1
Explanation: We can split the string on "(merchant)".
```

**Example 3:**

```
Input: text = "antaprezatepzapreanta"
Output: 11
Explanation: We can split the string on "(a)(nt)(a)(pre)(za)(tep)(za)(pre)(a)(nt)(a)".
```

**Constraints**

- 1 <= text.length <= 1000
- text consists only of lowercase English characters.

---

## 题目（中文翻译）

给定一个字符串 `text`，你需要将它划分为 `k` 个子串（subtext1, subtext2, …, subtextk），并满足以下条件：

- 对于任意 `i`（1 ≤ i ≤ k），第 `i` 个子串与第 `k+1-i` 个子串相同，即 `subtext_i == subtext_{k+1-i}`，从而整体形成一个回文块的结构。

返回能够得到的 **最大** `k` 值。

**示例**

**示例 1**  
输入: `text = "ghiabcdefhelloadamhelloabcdefghi"`  
输出: `7`  
解释: 我们可以按如下方式划分字符串  
`(ghi)(abcdef)(hello)(adam)(hello)(abcdef)(ghi)`。

**示例 2**  
输入: `text = "merchant"`  
输出: `1`  
解释: 只能划分为 `(merchant)`。

**示例 3**  
输入: `text = "antaprezatepzapreanta"`  
输出: `11`  
解释: 我们可以按如下方式划分字符串  
`(a)(nt)(a)(pre)(za)(tep)(za)(pre)(a)(nt)(a)`。

**约束条件**

- `1 <= text.length <= 1000`
- `text` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串从两端往里“配对”**。  
我们可以枚举左边的第一个块的长度 `lenL`（从 1 到 `n`），把左块记作 `text[0:lenL]`。  
随后再枚举右边的块的长度 `lenR`（同样从 1 到 `n`），把右块记作 `text[n‑lenR:]`。  

- 如果左块和右块完全相同（`text[0:lenL] == text[n‑lenR:]`），说明这两个块可以组成一对“回文块”。  
- 此时把中间剩余的子串 `text[lenL : n‑lenR]` 再递归地进行同样的配对。  
- 递归返回的块数再加上这对块（+2），得到一种合法的分割方式的块数。  

所有可能的 `lenL`、`lenR` 组合都尝试一遍，取最大值即为答案。  

> **类比**：把字符串想象成一根绳子，两个人从左右两端各抓一段绳子，如果抓到的两段颜色相同，就可以把它们剪下来，剩下的绳子再继续这样剪。我们把所有可能的抓法都试一遍，找到最多能剪几段的方案。

**为什么正确**  
只要我们把每一步的左块和右块配对成功，递归处理的子串仍然满足原题的要求——即要把剩下的部分继续拆成回文块。因此遍历所有可能的配对方式，必然能覆盖所有合法的拆分，取最大值自然就是最优解。

**复杂度分析（大白话）**  
- 对每一层递归，我们要枚举左块长度 `lenL`（最多 `n` 种）和右块长度 `lenR`（同样最多 `n` 种），并且每次比较两个子串需要 `O(n)` 的时间（因为要逐字符比对）。  
- 递归的深度最坏情况下是 `O(n)`（每次只剪掉最短的 1 个字符），于是总时间复杂度大约是 `O(n³)`，在最坏的 1000 长度下已经会很慢。  
- 只使用了递归栈和几个临时字符串，额外空间是 `O(n)`（递归深度）。

#### 代码（Python）

```python
def longestChunkedPalindrome(text: str) -> int:
    n = len(text)

    # 记忆化搜索，避免对同一子串重复计算
    from functools import lru_cache

    @lru_cache(None)
    def dfs(l: int, r: int) -> int:
        """
        计算子串 text[l:r]（左闭右开）能拆成多少块的最大值
        """
        # 子串为空，说明已经全部配对完毕
        if l >= r:
            return 0
        # 子串只有一个字符，最多只能算作一块
        if r - l == 1:
            return 1

        best = 1                     # 至少可以把整个子串算作一块
        # 枚举左块长度
        for lenL in range(1, r - l + 1):
            left = text[l:l + lenL]  # 左块
            # 枚举右块长度
            for lenR in range(1, r - l + 1):
                right = text[r - lenR:r]  # 右块
                if left == right:          # 两块相等，满足回文块的配对要求
                    # 递归处理内部子串，+2 表示这对块
                    inner = dfs(l + lenL, r - lenR) + 2
                    best = max(best, inner)
        return best

    return dfs(0, n)
```

> 关键行注释已在代码中，用中文解释了每一步的意义。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - “`n³`”可以理解为：我们要遍历 `n` 层（递归深度），每层又要尝试 `n × n` 种左右块的组合，而且每次比较两个子串要花 `O(n)` 的时间。整体就是 `n × n × n`，也就是 `n³`。
- **空间复杂度**：`O(n)`  
  - 主要是递归调用栈的深度（最坏 `n`），以及 `lru_cache` 保存的状态数目也在 `O(n²)`（但每个状态只保存一个整数），总体仍然是线性级别。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **大量的子串比较**（`left == right`）上——每次比较都要逐字符扫描，导致 `O(n³)`。  
如果我们能够在 **常数时间** 内判断两个子串是否相等，就可以把整体复杂度大幅降低。

**核心技巧：滚动哈希（Rolling Hash）**  
- 把一个字符串看成 **进制数**，比如把 `'a'…'z'` 映射成 `1…26`，选一个基数 `B`（常取 131、257 等），再选一个大模数 `M`（如 `10⁹+7`）防止溢出。  
- 对字符串的前缀计算哈希值 `pref[i] = (pref[i‑1] * B + code(s[i‑1])) % M`，这样任意子串 `[l, r)` 的哈希可以用公式  
  `hash(l, r) = (pref[r] - pref[l] * powB[r‑l]) % M`  
  在 **O(1)** 时间内得到。  
- 两个子串相等 → 哈希相等（冲突概率极低，实际可以再加双模数或直接再做一次字符比对保证正确性）。

**基于哈希的贪心双指针**  
1. 初始化左指针 `i = 0`、右指针 `j = n‑1`、计数器 `cnt = 0`。  
2. 维护两个滚动哈希：`hashL` 表示从左边开始的当前块的哈希，`hashR` 表示从右边开始的当前块的哈希。  
3. 每次向中间移动一步：  
   - `hashL = hashL * B + code(text[i])`（左块向右扩展）  
   - `hashR = hashR + code(text[j]) * powB[lenR]`（右块向左扩展）  
   - 同时记录左块长度 `lenL` 与右块长度 `lenR`。  
4. 当 `hashL == hashR` 并且 `lenL == lenR` 时，说明左块和右块**完全相同**，可以确定一对块，计数 `cnt += 2`，并把哈希、长度重置，继续处理剩余的中间部分。  
5. 当左指针超过右指针时，说明所有字符都已经配对完毕，若还有未配对的字符（`i == j+1`），说明中间剩下一个块，计数 `cnt += 1`。  

这样只遍历一次字符串，所有哈希运算都是 O(1)，总体 **时间 O(n)**，**空间 O(1)**（只需要几个整数和预计算的幂数组）。

> **类比**：想象两个人从绳子两端分别“抓住”若干颜色相同的珠子，每抓到一颗珠子就把它的颜色编号加入自己的“密码”。当两个人的密码相同且抓的珠子数量相同，就可以把这段珠子剪掉。因为密码的比较是瞬间完成的（哈希），所以整个过程只需要一次遍历。

#### 代码（Python）

```python
def longestChunkedPalindrome(text: str) -> int:
    n = len(text)
    if n == 0:
        return 0

    # 参数选取（常用的基数和模数）
    BASE = 131
    MOD1 = 10**9 + 7
    MOD2 = 10**9 + 9          # 双模数进一步降低冲突概率

    # 预计算幂值 powB[i] = BASE^i % MOD
    pow1 = [1] * (n + 1)
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow1[i] = (pow1[i - 1] * BASE) % MOD1
        pow2[i] = (pow2[i - 1] * BASE) % MOD2

    # 双模数哈希，返回 (h1, h2)
    def char_code(ch: str) -> int:
        return ord(ch) - ord('a') + 1   # a->1, b->2, ...

    i, j = 0, n - 1          # 左右指针
    cnt = 0                  # 已确定的块数
    # 当前左块、右块的哈希以及长度
    left_h1 = left_h2 = 0
    right_h1 = right_h2 = 0
    lenL = lenR = 0

    while i <= j:
        # 向左块添加一个字符
        left_h1 = (left_h1 * BASE + char_code(text[i])) % MOD1
        left_h2 = (left_h2 * BASE + char_code(text[i])) % MOD2
        lenL += 1
        i += 1

        # 向右块添加一个字符（注意顺序是从右往左）
        right_h1 = (right_h1 + char_code(text[j]) * pow1[lenR]) % MOD1
        right_h2 = (right_h2 + char_code(text[j]) * pow2[lenR]) % MOD2
        lenR += 1
        j -= 1

        # 当两边的哈希相等且长度相等，说明找到了一个配对块
        if left_h1 == right_h1 and left_h2 == right_h2 and lenL == lenR:
            cnt += 2            # 这对块各算一块
            # 重置，准备寻找下一对块
            left_h1 = left_h2 = 0
            right_h1 = right_h2 = 0
            lenL = lenR = 0

    # 循环结束后可能还有未配对的中心块（lenL != 0 表示还有残留）
    if lenL != 0:               # 中间剩下的部分算作一块
        cnt += 1

    return cnt
```

**代码要点注释**（已在代码中以中文解释）：

- `BASE`、`MOD1`、`MOD2`：选取的基数和两个模数，用来构造稳健的滚动哈希。  
- `pow1`、`pow2`：预计算 `BASE` 的幂，帮助右侧哈希的 **O(1)** 更新。  
- `left_h*`、`right_h*`：分别维护左块和右块的双模哈希值。  
- `lenL == lenR`：保证左块和右块的长度相同（否则即使哈希相同也不算配对）。  
- `cnt += 2`：每次找到一对相同块，计数加 2；循环结束后若还有残余（中心块），再加 1。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，每一步的哈希更新、比较都是常数时间。相比暴力解的 `n³`，这里可以把 1000 长度的字符串在毫秒级完成。  
- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了若干整数变量和长度为 `n+1` 的幂数组（`O(n)`），如果把幂数组视作常数级别的预处理，则额外空间可以认为是常数。

---

## 心得

- **核心技巧**：利用滚动哈希把子串相等判断降到 **O(1)**，配合 **双指针贪心** 实现线性扫描。  
- **适用的题型**  
  1. “最长回文子串/子序列”类的需要快速比较子串是否相等的题目（如 *Palindrome Partitioning* 的变种）。  
  2. “字符串分块”或 “拆分成相等子串” 的问题（如 *Maximum Number of Non‑Overlapping Substrings*）。  
  3. “判定两段子串相等” 的场景，常用滚动哈希或前缀哈希（如 *Repeated Substring Pattern*、*Find the Duplicate Substring*）。  
- **一句话总结解题钥匙**：**把“比较两个子串是否相同”这一步变成 O(1) 的哈希比较，再用双指针一次遍历完成配对**。

---

## 反思

- **第一反应**：看到“把字符串拆成尽可能多的回文块”，自然想到递归/动态规划的枚举方案——即暴力搜索。  
- **最容易踩的坑**  
  - **哈希冲突**：单模数可能出现误判，需要双模数或在哈希相等时再做一次字符逐一比较。  
  - **长度不匹配**：仅哈希相等不足以说明块相同，必须同时保证左块和右块的长度相等（`lenL == lenR`）。  
  - **中心块的处理**：当左指针刚好越过右指针时，可能还有未配对的字符，这时应计为 **1** 块而不是 **0**。  
- **下次思路**：遇到需要“在两端配对”且**频繁比较子串相等**的题目，第一时间想到 **滚动哈希 + 双指针**，把比较从线性降到常数，从而把整体复杂度压到线性级别。