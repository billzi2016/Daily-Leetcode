# #3137. 最少操作次数使单词 K 周期 / Minimum Number of Operations to Make Word K-Periodic

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-word-k-periodic/)

---

## 题目（英文原版）

**Description**

You are given a string word of size n, and an integer k such that k divides n.
In one operation, you can pick any two indices i and j, that are divisible by k, then replace the substring of length k starting at i with the substring of length k starting at j. That is, replace the substring word[i..i + k - 1] with the substring word[j..j + k - 1].
Return the minimum number of operations required to make word k-periodic.
We say that word is k-periodic if there is some string s of length k such that word can be obtained by concatenating s an arbitrary number of times. For example, if word == “ababab”, then word is 2-periodic for s = "ab".

**Examples**

**Example 1:**

```
Input: word = "leetcodeleet", k = 4
Output: 1
Explanation:
We can obtain a 4-periodic string by picking i = 4 and j = 0. After this operation, word becomes equal to "leetleetleet".
```

**Example 2:**

```
Input: word = " leetcoleet ", k = 2
Output: 3
Explanation:
We can obtain a 2-periodic string by applying the operations in the table below.
```

**Constraints**

- 1 <= n == word.length <= 105
- 1 <= k <= word.length
- k divides word.length.
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串 `word`，以及一个整数 `k`（满足 `k` 能整除 `n`）。  
一次操作可以选取任意两个下标 `i` 和 `j`，且这两个下标都能被 `k` 整除，然后用下标 `j` 开始的长度为 `k` 的子串（substring）替换下标 `i` 开始的长度为 `k` 的子串。即将 `word[i .. i + k - 1]` 替换为 `word[j .. j + k - 1]`。  

返回将 `word` 变为 **k-周期**（k-periodic）的最少操作次数。

如果存在一个长度为 `k` 的字符串 `s`，使得 `word` 可以通过把 `s` 复制若干次并拼接得到，则称 `word` 为 **k-周期**。例如，`word == "ababab"` 时，`word` 对于 `s = "ab"` 是 2‑周期的。

---

### 示例 1

**输入**  
`word = "leetcodeleet", k = 4`

**输出**  
`1`

**解释**  
我们可以选择 `i = 4`、`j = 0` 进行一次操作。操作后，`word` 变为 `"leetleetleet"`，此时它是 4‑周期的。

---

### 示例 2

**输入**  
`word = "leetcoleet", k = 2`

**输出**  
`3`

**解释**  
通过下表所示的三次操作可以得到一个 2‑周期的字符串。

| 操作 | i | j | 结果 |
|------|---|---|------|
| 1 | 2 | 0 | `le...` |
| 2 | 4 | 2 | `le...` |
| 3 | 6 | 4 | `le...` |

（具体替换过程略）

---

### 约束条件

- `1 <= n == word.length <= 10^5`
- `1 <= k <= word.length`
- `k` 能整除 `word.length`
- `word` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把字符串 `word` 看成若干 **块**（block），每块长度都是 `k`，因为 `k` 能整除 `n`，所以一定可以完整切分。  
比如 `word = "leetcodeleet"`、`k = 4` 时可以切成  

```
[0,3]   "leet"
[4,7]   "code"
[8,11]  "leet"
```

题目允许的操作是：任选两个块 `i`、`j`（块的起始下标必须是 `k` 的整数倍），把块 `i` 的内容全部改成块 `j` 的内容。  
换句话说，一次操作只能 **把一个块改成另一个块**，而且改成的内容必须已经出现在某个块里。

**最直接的想法**是：把每一个块都当成**可能的目标块** `s`，然后逐个检查把其它块改成 `s` 需要几次操作。  
- 把块 `i` 当作目标 `s`，遍历所有块，统计有多少块和 `s` 不同。  
- 这个不同的数量就是把整个字符串变成 `k`‑周期所需的操作次数（因为每个不同块都要单独一次复制）。  
- 对所有块都尝试一次，取最小值即为答案。

> **类比**：想象你在图书馆把若干本相同章节的书整理成同一本的内容。暴力做法就是把每本书都当成“标准版”，逐本检查其它书是否需要重新打印。

**为什么这样一定能得到正确答案**  
- 最终的 `k`‑周期字符串必然由某一个块的内容 `s` 复制而来（因为只能复制已有块）。  
- 我们把每个块都当成可能的 `s`，必然会遍历到真正的 `s`，于是得到的最小操作数就是最优解。

**时间/空间分析**（大白话）  
- 设块的个数为 `m = n / k`。  
- 对每个块（共 `m` 个）我们都要遍历全部 `m` 个块并比较 `k` 个字符。  
- 所以总共要比较 `m × m × k = (n/k)² × k = n² / k` 次字符。  
- 当 `n = 10⁵`、`k = 1` 时，这相当于 `10¹⁰` 次比较，电脑根本跑不完。  
- 只用了常数级的额外空间（几个计数器），空间复杂度是 **O(1)**。

#### 代码（Python）

```python
def min_operations_bruteforce(word: str, k: int) -> int:
    n = len(word)
    m = n // k                     # 块的数量
    blocks = [word[i:i + k] for i in range(0, n, k)]  # 把所有块取出来

    best = m                      # 最坏情况是每块都不相同，需要 m 次操作
    for target in blocks:         # 把每个块都当作可能的目标块 s
        ops = 0
        for b in blocks:          # 检查每个块是否和目标相同
            if b != target:       # 不同的块需要一次复制操作
                ops += 1
        best = min(best, ops)     # 取最小的操作次数
    return best
```

#### 复杂度

- **时间复杂度**：`O(n² / k)`  
  - 把 `n² / k` 想象成“把一张 10 000 × 10 000 的棋盘划分成小格子”，每走一步都要检查整行整列，显然太慢了。
- **空间复杂度**：`O(1)`（不计存放原始字符串的空间）  

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**真正决定操作次数的不是每个块的具体位置，而是每种块出现的次数**。  
如果某个块出现得最多（记为 `maxFreq`），我们就可以把它选为最终的周期字符串 `s`，因为：

- 已经有 `maxFreq` 个块天然就是 `s`，不需要任何操作。  
- 其余 `m - maxFreq` 个块只要各自一次复制，就能全部变成 `s`。  

于是答案直接等于 **块总数减去出现次数最多的块的频率**：

```
answer = m - maxFreq
```

这把 “遍历所有块作为目标” 的二重循环，**降到了只统计一次出现频率**，时间从 `O(n²/k)` 降到 `O(n)`。

**核心数据结构：哈希表（字典）**  
- 哈希表就像 **查字典**：把每个块（key）对应的出现次数（value）记录下来。  
- 查找、插入、更新的时间都可以看成 “一步到位”，即 **O(1)**，所以整体是线性时间。

**步骤**  

1. **切块**：从下标 `0, k, 2k, …` 把 `word` 切成长度为 `k` 的子串。  
2. **统计频率**：用字典 `cnt` 把每个子串出现的次数累计。  
3. **找最大频率**：遍历字典得到 `maxFreq`（也可以在统计时同步更新）。  
4. **计算答案**：`len(cnt)` 实际是块的总数 `m = n/k`，返回 `m - maxFreq`。

> **类比**：把所有块看成 **相同型号的零件**，我们只需要把最多的那种型号保留下来，其他的全部换成这种型号，一次换一个零件即可。

#### 代码（Python）

```python
def min_operations(word: str, k: int) -> int:
    """
    返回把 word 变成 k‑periodic 所需的最少操作次数
    """
    n = len(word)
    m = n // k                     # 块的数量

    freq = {}                      # 哈希表：子串 -> 出现次数
    max_freq = 0                   # 记录出现次数的最大值

    # 依次取每个块并统计
    for i in range(0, n, k):
        block = word[i:i + k]      # 长度恰好为 k 的子串
        # 更新出现次数
        freq[block] = freq.get(block, 0) + 1
        # 同时维护最大频率
        if freq[block] > max_freq:
            max_freq = freq[block]

    # 需要改动的块数 = 总块数 - 出现次数最多的块的数量
    return m - max_freq
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历了一遍字符串，每个字符恰好被读取一次（切块时读取 `k` 次，但所有块共 `n` 个字符）。  
  - 相当于“只需要一次跑完马拉松”，远快于暴力的 “跑来跑去来回跑”。
- **空间复杂度**：`O(m)`（哈希表存放每种块），最坏情况下每个块都不同，`m = n/k ≤ 10⁵`，完全可以接受。  
  - 如果只关心最大频率，可以在统计时不保存全部键值，只保存出现次数最高的那个块，这样空间可以降到 **O(1)**。

---

## 心得

- **核心技巧**：把“把字符串变成 k‑周期”转化为“把所有长度为 k 的块统一成同一个块”，于是只需要统计块的出现频率，答案是 `总块数 - 最高频率`。  
- **适用的题型**  
  1. **把数组/字符串分块后统一**（例如 “最少替换使数组所有子数组相等”）。  
  2. **出现频率最高的元素决定最少修改次数**（如 “最少删除字符使所有字符出现次数相同”）。  
  3. **分段复制操作**（例如 “把字符串分段复制成目标段落”）。
- **一句话总结解题钥匙**：**“把每块当成字典的键，出现最多的键决定最终形态，答案 = 总数 - 最大频次”。**

## 反思

- **第一反应**：看到“把子串复制到别的子串”，第一时间会想到 **模拟每一次复制**，结果往往会写出暴力的双层循环。  
- **最容易踩的坑**  
  - **忽略 `k` 必须整除 `n`**：若忘记这一点，切块时可能出现残余字符导致索引越界。  
  - **把块的下标当成字符下标**：记得块的起始位置必须是 `k` 的整数倍。  
  - **忘记已有块可以直接作为来源**：如果所有块都不相同，仍然只需要 `m-1` 次操作（因为只要保留一个块作为源即可），而不是 `m` 次。  
- **下次遇到同类题**：第一步先 **统计“单位块”出现的频率**，看是否可以直接用 “总数 - 最高频次” 解决，而不是马上去模拟复制过程。这样思路更清晰，代码也更简洁。