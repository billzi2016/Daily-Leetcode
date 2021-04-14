# #1297. 子字符串的最大出现次数 / Maximum Number of Occurrences of a Substring

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-occurrences-of-a-substring/)

---

## 题目（英文原版）

**Description**

Given a string s, return the maximum number of occurrences of any substring under the following rules:

**Examples**

**Example 1:**

```
Input: s = "aababcaab", maxLetters = 2, minSize = 3, maxSize = 4
Output: 2
Explanation: Substring "aab" has 2 occurrences in the original string.
It satisfies the conditions, 2 unique letters and size 3 (between minSize and maxSize).
```

**Example 2:**

```
Input: s = "aaaa", maxLetters = 1, minSize = 3, maxSize = 3
Output: 2
Explanation: Substring "aaa" occur 2 times in the string. It can overlap.
```

**Constraints**

- 1 <= s.length <= 105
- 1 <= maxLetters <= 26
- 1 <= minSize <= maxSize <= min(26, s.length)
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `s`，返回满足以下规则的任意子字符串（substring）出现次数的最大值：

- 子字符串的长度必须在 `minSize` 与 `maxSize` 之间（两端均可）。
- 子字符串中不同字母的数量不超过 `maxLetters`。

**示例**  

**示例 1**  
输入：`s = "aababcaab", maxLetters = 2, minSize = 3, maxSize = 4`  
输出：`2`  
解释：子字符串 `"aab"` 在原字符串中出现了 2 次。它满足条件：唯一字母数为 2，长度为 3（位于 `minSize` 与 `maxSize` 之间）。

**示例 2**  
输入：`s = "aaaa", maxLetters = 1, minSize = 3, maxSize = 3`  
输出：`2`  
解释：子字符串 `"aaa"` 在字符串中出现了 2 次，且可以重叠。

**约束条件**  

- `1 <= s.length <= 10^5`
- `1 <= maxLetters <= 26`
- `1 <= minSize <= maxSize <= min(26, s.length)`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有满足条件的子串全部枚举出来，然后统计每个子串出现了多少次，最后取最大值。

- **枚举子串**：我们可以遍历字符串的每一个起始位置 `i`，再遍历所有合法的结束位置 `j`（`minSize ≤ j‑i+1 ≤ maxSize`），把 `s[i:j+1]` 当作一个候选子串。  
- **检查条件**：对每个子串统计其中出现的不同字母个数（比如用 `set`），如果不超过 `maxLetters`，说明它符合题意。  
- **计数**：把符合条件的子串放进一个哈希表（字典）里，键是子串本身，值是出现次数。遍历完所有子串后，哈希表里最大的值就是答案。

> **类比**：哈希表就像一本“字典”，我们把每个子串当成“单词”，把它出现的次数当成“页码”。查找、插入、计数都很快，只要我们先把所有单词写进去。

#### 代码（Python）

```python
def maxFreq_bruteforce(s: str, maxLetters: int, minSize: int, maxSize: int) -> int:
    from collections import defaultdict

    freq = defaultdict(int)          # 哈希表：子串 → 出现次数
    n = len(s)

    # 枚举所有起始位置 i
    for i in range(n):
        # 枚举所有合法的结束位置 j
        for j in range(i + minSize - 1, min(i + maxSize, n)):
            sub = s[i:j + 1]          # 当前子串
            # 统计子串中不同字母的个数
            if len(set(sub)) <= maxLetters:
                freq[sub] += 1        # 计数

    # 取出现次数的最大值（如果没有合法子串返回 0）
    return max(freq.values(), default=0)
```

#### 复杂度

- **时间复杂度**：`O(n * L²)`（`L = maxSize`），因为外层遍历 `n` 次，内层最多遍历 `L` 次，每次统计不同字母又要遍历子串长度 `≈ L`。在最坏情况下 `L ≤ 26`，所以大致是 `O(n * 26²)`，但对 `10⁵` 的字符串仍然会超时。  
- **空间复杂度**：`O(m * L)`，`m` 为不同合法子串的数量，最坏情况下每个子串都要存进哈希表，长度最多 `L`（≤26），因此空间随子串数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有长度** 是导致慢的根本原因。观察题目约束：

1. `maxSize ≤ 26`，所以子串最长也只有 26。  
2. **更长的子串出现的次数必然不大于它的前缀**（因为每次滑动窗口至少会失去一个字符），因此如果我们只关心出现次数最多的子串，只需要考虑最短的合法长度 `minSize`。  

基于这两个观察，最优解只需要：

- **固定窗口大小 = minSize**，在字符串上滑动一次。  
- 在滑动窗口过程中，实时维护窗口内不同字母的个数（用一个大小为 26 的计数数组即可），判断是否 ≤ `maxLetters`。  
- 如果合法，就把当前窗口对应的子串计入哈希表，统计出现次数。  
- 最后返回哈希表中最大的计数。

这样我们只遍历一次字符串，窗口内部的更新是 `O(1)`（只增删一个字符），整体复杂度为 `O(n * 26)`，因为判断不同字母个数最多遍历 26 次字母表。

> **类比**：想象我们在跑步时背着一个装满 26 种颜色球的背包，窗口每前进一步，就把左边的球丢掉、把右边的新球装进去。我们只需要随时检查背包里有几种颜色，而不是每次都重新数一遍。

#### 代码（Python）

```python
def maxFreq_optimal(s: str, maxLetters: int, minSize: int, maxSize: int) -> int:
    """
    只考虑长度为 minSize 的子串，使用滑动窗口 + 哈希表计数
    """
    from collections import defaultdict

    n = len(s)
    if n < minSize:
        return 0

    freq = defaultdict(int)          # 子串 → 出现次数
    cnt = [0] * 26                    # 统计窗口内每个字母出现次数
    distinct = 0                      # 窗口内不同字母的个数

    # 初始化第一个窗口 [0, minSize)
    for i in range(minSize):
        idx = ord(s[i]) - ord('a')
        if cnt[idx] == 0:
            distinct += 1
        cnt[idx] += 1

    # 检查第一个窗口是否合法
    if distinct <= maxLetters:
        freq[s[0:minSize]] += 1

    # 开始滑动窗口，左指针 l，右指针 r（新加入字符的下标）
    for l in range(1, n - minSize + 1):
        # 移出左边的字符
        left_char = s[l - 1]
        left_idx = ord(left_char) - ord('a')
        cnt[left_idx] -= 1
        if cnt[left_idx] == 0:
            distinct -= 1

        # 加入右边的字符
        r = l + minSize - 1
        right_char = s[r]
        right_idx = ord(right_char) - ord('a')
        if cnt[right_idx] == 0:
            distinct += 1
        cnt[right_idx] += 1

        # 若窗口合法，计数
        if distinct <= maxLetters:
            sub = s[l:l + minSize]
            freq[sub] += 1

    # 哈希表里最大的出现次数即为答案
    return max(freq.values(), default=0)
```

#### 复杂度

- **时间复杂度**：`O(n * 26)` → 实际上是 `O(n)`，因为 26 是常数。我们只遍历字符串一次，每一步只检查/更新 26 个计数中的常数个。与暴力解的 `O(n * L²)` 相比，快了好几个数量级。  
- **空间复杂度**：`O(k)`，`k` 为不同合法子串的数量（最坏情况下仍然可能是 `O(n)`），加上固定的 26 长度计数数组和哈希表的开销。

---

## 心得

- **核心技巧**：固定最小合法长度，使用 **滑动窗口** + **哈希表** 统计子串出现次数。  
- **适用题型**：  
  1. “给定长度范围，统计出现次数最多的子串” —— 如本题。  
  2. “找出满足某种字符约束的最长/最短子串” —— 常用滑动窗口。  
  3. “统计所有长度为 K 的子串出现次数” —— 直接使用固定窗口。  
- **解题钥匙**：**只关注最短合法长度**，把 “枚举所有子串” 的指数级爆炸降到线性遍历。

---

## 反思

- **第一反应**：直接把所有子串枚举出来，然后逐个检查条件，感觉最直观。  
- **最容易踩的坑**：  
  - 忘记 **子串可以重叠**（如 `"aaaa"` 中的 `"aaa"` 出现两次）。  
  - 没有利用 `maxSize ≤ 26` 的约束，导致时间复杂度爆炸。  
  - 在滑动窗口中忘记在移出字符时更新 `distinct`，导致错误判断合法性。  
- **下次思路**：一看到 “长度上限很小” 或 “子串长度范围固定”，立即考虑 **固定窗口**；若还有 “字母种类 ≤ X” 的限制，就用 **计数数组**（类似哈希表）实时维护不同字符数。这样可以把原本的 “枚举 + 检查” 转化为 “一次遍历 + 常数时间检查”。