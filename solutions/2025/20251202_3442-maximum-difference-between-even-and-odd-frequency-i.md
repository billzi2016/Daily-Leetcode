# #3442. **偶数频率与奇数频率之差的最大值 I** / Maximum Difference Between Even and Odd Frequency I

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-between-even-and-odd-frequency-i/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters.
Your task is to find the maximum difference diff = freq(a1) - freq(a2) between the frequency of characters a1 and a2 in the string such that:
Return this maximum difference.

**Examples**

**Example 1:**

```
Input: s = "aaaaabbc"
Output: 3
Explanation:
```

**Example 2:**

```
Input: s = "abcabcab"
Output: 1
Explanation:
```

**Constraints**

- 3 <= s.length <= 100
- s consists only of lowercase English letters.
- s contains at least one character with an odd frequency and one with an even frequency.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s`。  
请在所有字符 `a1` 与 `a2`（其中 `a1` 的出现次数为偶数，`a2` 的出现次数为奇数）中，求出频率差的最大值  

\[
\text{diff} = \text{freq}(a1) - \text{freq}(a2)
\]

返回该最大差值。

**示例 1**  
```
Input: s = "aaaaabbc"
Output: 3
解释：
```

**示例 2**  
```
Input: s = "abcabcab"
Output: 1
解释：
```

**约束条件**

- $3 \le \text{s.length} \le 100$
- `s` 仅由小写英文字母组成。
- `s` 至少包含一个出现次数为奇数的字符和一个出现次数为偶数的字符。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一种字符** 的出现次数都算出来，然后**枚举所有两两组合**，挑出满足「一个字符出现次数为奇数，另一个字符出现次数为偶数」的配对，计算 `freq(奇数字符) - freq(偶数字符)`，把所有得到的差值取最大即可。

- **用到的数据结构**：  
  - **哈希表（字典）** 用来统计每个字符出现了多少次。可以把它想象成一本字典，**key** 是单词（这里是字符），**value** 是页码（这里是出现次数）。  
  - **列表** 用来保存所有出现过的字符，方便后面两两配对。

- **为什么正确**：  
  - 我们遍历了所有可能的 `(a1, a2)` 配对，只要 `a1` 的频次是奇数、`a2` 的频次是偶数，就会计算一次差值。因为所有合法配对都被检查过，取最大的那个就是答案。

- **时间/空间复杂度**（大白话）  
  - 设字符串长度为 `n`（最多 100），字符种类不超过 26。  
  - 统计频次需要遍历一次字符串，时间是 **O(n)**。  
  - 枚举所有配对相当于 **两层循环**，最坏情况要检查 `k²` 次（`k` 为出现过的字符种类），这里 `k ≤ 26`，所以时间是 **O(k²)**，在最坏情况下约等于 **O(26²) ≈ O(1)**，但从算法思路角度我们仍把它写成 **O(m²)**（`m` 为字符种类数），这在概念上比线性遍历慢。  
  - 哈希表存放每个字符的计数，需要 **O(k)** 的空间。

#### 代码（Python）

```python
def maxDiff_bruteforce(s: str) -> int:
    # 1️⃣ 统计每个字符出现的次数，用字典（哈希表）保存
    freq = {}
    for ch in s:                     # O(n) 遍历字符串
        freq[ch] = freq.get(ch, 0) + 1

    # 2️⃣ 把所有出现过的字符列成列表，方便后面两两配对
    chars = list(freq.keys())        # 最多 26 个字符

    max_diff = -float('inf')         # 用一个很小的数初始化答案

    # 3️⃣ 两层循环枚举所有配对 (a1, a2)
    for i in range(len(chars)):
        for j in range(len(chars)):
            if i == j:
                continue              # 不能配对同一个字符
            cnt1, cnt2 = freq[chars[i]], freq[chars[j]]
            # 只保留奇数频次 - 偶数频次 的配对
            if cnt1 % 2 == 1 and cnt2 % 2 == 0:
                diff = cnt1 - cnt2
                if diff > max_diff:
                    max_diff = diff

    return max_diff
```

#### 复杂度  

- **时间复杂度**：`O(n + m²)`  
  - `n` 是字符串长度（统计频次），`m` 是出现过的不同字符数（最多 26）。  
  - 大白话：先走一遍字符串，再在最多 26 个字符里找所有配对，配对的次数大约是 26×26=676，算起来几乎可以忽略不计，但在概念上比一次线性遍历要慢。  

- **空间复杂度**：`O(m)`  
  - 只需要存放每个字符的计数，最多 26 条记录。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正决定答案的只有两件事**：

1. **奇数频次字符中出现次数最大的**（记为 `maxOdd`）。  
2. **偶数频次字符中出现次数最小的**（记为 `minEven`）。

因为我们要求的是 `freq(奇) - freq(偶)` 的最大值，显然取最大的奇数频次再减去最小的偶数频次就能得到最优答案。  

所以我们不必枚举所有配对，只要在一次遍历中：

- 统计每个字符的出现次数（哈希表或长度为 26 的数组）。  
- 在遍历完计数后，**一次扫过计数表**，分别维护 `maxOdd` 和 `minEven`。  

这把 **两层循环** 的配对过程省掉了，整体只需要 **线性时间**。

> **核心数据结构**：**数组**（长度 26）来存放每个小写字母的计数。把数组想象成 **26 格的信箱**，每个格子对应一个字母，往里面塞进去的数字就是该字母出现的次数。数组的查找、写入都是 O(1) 的，非常快。

#### 代码（Python）

```python
def maxDiff_optimal(s: str) -> int:
    # 1️⃣ 用长度为 26 的数组统计字符出现次数
    #   下标 0 对应 'a', 1 对应 'b', ... , 25 对应 'z'
    cnt = [0] * 26
    for ch in s:                         # O(n) 遍历字符串
        idx = ord(ch) - ord('a')         # 计算字符对应的数组下标
        cnt[idx] += 1

    # 2️⃣ 初始化 maxOdd 为极小值，minEven 为极大值
    max_odd = -float('inf')
    min_even = float('inf')

    # 3️⃣ 再遍历一次计数数组，挑出 maxOdd 与 minEven
    for c in cnt:
        if c == 0:
            continue                      # 该字母根本没出现，跳过
        if c % 2 == 1:                    # 奇数频次
            if c > max_odd:
                max_odd = c
        else:                             # 偶数频次
            if c < min_even:
                min_even = c

    # 根据题目保证一定会有奇数频次和偶数频次的字符
    return max_odd - min_even
```

#### 复杂度  

- **时间复杂度**：`O(n + 26) = O(n)`  
  - 第一次遍历字符串统计频次是 `O(n)`，第二次遍历固定长度 26 的数组是常数时间。  
  - 大白话：只需要走两遍“路”，第一遍走完所有字符，第二遍只在 26 格小盒子里找最大/最小，整体速度和字符串长度成正比。  

- **空间复杂度**：`O(1)`（常数空间）  
  - 我们只用了一个长度为 26 的整数数组，大小不随输入 `n` 变化。  

---

## 心得  

- **核心技巧**：先把所有字符的出现次数统计出来，再**分别取奇数频次的最大值和偶数频次的最小值**，直接相减即可。  
- **该技巧适用的题型**  
  1. “在某类元素中取最大 / 在另一类元素中取最小” 类的比较题，例如 “Maximum Difference Between Even and Odd Frequency II”。  
  2. “统计频次后做分类处理” 的题目，如 “Find the Most Frequent Even Number”。  
  3. “利用计数数组（或哈希表）实现 O(1) 查询” 的题目，例如 “Count Characters With Maximum Frequency”。  
- **一句话总结解题钥匙**：**先统计，再分类取 extremum（极值）**。  

---

## 反思  

- **第一反应**：看到“奇数频次”和“偶数频次”，我立刻想到要先统计每个字符出现多少次，然后在这上面做筛选。  
- **最容易踩的坑**  
  - **忘记排除未出现的字符**：计数数组里有 0 的格子，它们既不是奇数也不是偶数，需要跳过。  
  - **边界条件**：题目保证至少有一个奇数频次和一个偶数频次的字符，但如果忘记这点，直接返回 `max_odd - min_even` 可能会出现 `inf - inf` 的错误。  
  - **字符映射错误**：`ord(ch) - ord('a')` 必须确保字符都是小写英文字母，否则会越界。  
- **下次遇到同类题，第一步该想到**：**“先用哈希表或计数数组把所有信息收集齐”，再根据题目要求在收集好的信息上做一次或几次遍历，直接得到答案**。