# #438. 找到字符串中的所有字母异位词 / Find All Anagrams in a String

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/find-all-anagrams-in-a-string/)

---

## 题目（英文原版）

**Description**

Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: s = "cbaebabacd", p = "abc"
Output: [0,6]
Explanation:
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".
```

**Example 2:**

```
Input: s = "abab", p = "ab"
Output: [0,1,2]
Explanation:
The substring with start index = 0 is "ab", which is an anagram of "ab".
The substring with start index = 1 is "ba", which is an anagram of "ab".
The substring with start index = 2 is "ab", which is an anagram of "ab".
```

**Constraints**

- 1 <= s.length, p.length <= 3 * 104
- s and p consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `p`，返回所有 `p` 的字母异位词（anagram）在 `s` 中的起始下标组成的数组。答案可以以任意顺序返回。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**  

**示例 1:**  
```
Input: s = "cbaebabacd", p = "abc"
Output: [0,6]
```
**解释:**  
下标为 `0` 的子串（substring）是 `"cba"`，它是 `"abc"` 的字母异位词。  
下标为 `6` 的子串（substring）是 `"bac"`，它也是 `"abc"` 的字母异位词。

**示例 2:**  
```
Input: s = "abab", p = "ab"
Output: [0,1,2]
```
**解释:**  
下标为 `0` 的子串（substring）是 `"ab"`，它是 `"ab"` 的字母异位词。  
下标为 `1` 的子串（substring）是 `"ba"`，它是 `"ab"` 的字母异位词。  
下标为 `2` 的子串（substring）是 `"ab"`，它是 `"ab"` 的字母异位词。

**约束条件:**  
- `1 <= s.length, p.length <= 3 * 10^4`  
- `s` 和 `p` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把字符串 **s** 中的每一个长度等于 **p** 的子串都拿出来，和 **p** 的字符组成情况逐个比较，看它们是不是同构（即字符出现次数完全相同）。  

- **数据结构**：这里可以用「哈希表」来统计字符出现次数，哈希表就像一本字典，单词（字符）是 *key*，在单词所在页的页码（出现次数）是 *value*。  
- **正确性**：如果两个子串的每个字符出现次数都一样，那么这两个子串必然是彼此的字母异位词（anagram），因为字符种类和数量都匹配。  
- **时间/空间分析**：  
  - 对 **s** 长度为 *n*，**p** 长度为 *m*，我们要检查 **n‑m+1** 个窗口。  
  - 对每个窗口都要遍历 **m** 个字符来统计频次并比较，导致总的时间复杂度是 **O((n‑m+1)·m) ≈ O(n·m)**。  
  - 哈希表只需要存放 26 个英文字母的计数，空间是 **O(1)**（常数级），因为字母表大小固定。

#### 代码（Python）

```python
def findAnagrams_brute(s: str, p: str):
    n, m = len(s), len(p)
    res = []

    # 把 p 的字符计数做成基准哈希表
    def build_counter(st: str):
        counter = {}
        for ch in st:
            counter[ch] = counter.get(ch, 0) + 1
        return counter

    p_counter = build_counter(p)

    # 枚举每一个可能的起始位置
    for i in range(n - m + 1):
        window = s[i:i + m]               # 取出长度为 m 的子串
        if build_counter(window) == p_counter:   # 直接比较两个字典是否相等
            res.append(i)                 # 相等说明是异位词，记录下起始下标

    return res
```

#### 复杂度

- **时间复杂度**：**O(n·m)** —— 想象成「n」个小盒子里每个都要装「m」件东西，整体工作量随两者乘积增长。  
- **空间复杂度**：**O(1)** —— 只用了固定大小的哈希表（26 个字母），不随输入规模增大。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于每次窗口都要重新统计 **m** 个字符的出现次数。我们可以让窗口“滑动”，每次只修改进入窗口和离开窗口的那两个字符的计数，从而把每一步的工作量降到 **O(1)**。这就是 **滑动窗口**（Sliding Window）+ **哈希表** 的经典组合。

关键步骤：

1. **准备工作**  
   - 先统计 **p** 中每个字符的出现次数，记作 `need`。  
   - 再准备一个大小为 26 的数组 `window`（或字典），记录当前窗口内字符的计数。  

2. **窗口移动**  
   - 窗口大小固定为 **len(p)**。  
   - 用两个指针 `left`、`right`，`right` 每右移一步，就把 `s[right]` 加入窗口计数。  
   - 当窗口长度等于 **len(p)** 时，比较 `window` 与 `need` 是否相同（即两者的不同字符计数为 0）。如果相同，就把 `left` 加入答案。  
   - 然后把 `s[left]` 移出窗口，`left` 向右移动一步，继续下一轮。  

3. **相等判定的优化**  
   - 直接比较两个 26 长度的数组会花 **O(26)** 的时间，仍然是常数，但我们可以进一步用一个变量 `diff` 记录两者不相等的字符种类数。  
   - 当 `window[ch]` 与 `need[ch]` 从不相等变为相等时，`diff -= 1`；反之则 `diff += 1`。  
   - 当 `diff == 0` 时，说明窗口正好是一个异位词。  

4. **类比**  
   - 想象你在看一条流水线上的装配盒子，每个盒子里只能装 **m** 件零件。你只需要检查进来的一件和即将出走的一件，而不是每次把盒子里所有零件都重新点数。

#### 代码（Python）

```python
def findAnagrams(s: str, p: str):
    n, m = len(s), len(p)
    if n < m:
        return []

    # 统计 p 中每个字符需要出现的次数（哈希表）
    need = [0] * 26               # 只针对小写字母，索引 0~25 对应 'a'~'z'
    for ch in p:
        need[ord(ch) - ord('a')] += 1

    window = [0] * 26              # 当前窗口的字符计数
    diff = 0                       # 记录 need 与 window 不相等的字符种类数

    # 初始化 diff：先把 need 中非零的字符计入 diff
    for i in range(26):
        if need[i] != 0:
            diff += 1

    res = []
    left = 0

    for right in range(n):
        # 把右边新进来的字符加入窗口
        idx = ord(s[right]) - ord('a')
        window[idx] += 1

        # 如果加入后恰好等于 need，对应字符的 diff 减 1
        if window[idx] == need[idx]:
            diff -= 1
        # 如果加入后超过 need，说明之前已经相等，现在不等了，diff 加 1
        elif window[idx] == need[idx] + 1:
            diff += 1

        # 当窗口大小达到 m 时，开始检查并收缩左边
        if right - left + 1 == m:
            if diff == 0:                 # diff 为 0 表示窗口正好是异位词
                res.append(left)

            # 移出左边的字符，准备收缩窗口
            left_idx = ord(s[left]) - ord('a')
            # 移出前，如果窗口计数恰好等于 need，则 diff 加 1（将要不等了）
            if window[left_idx] == need[left_idx]:
                diff += 1
            # 移出后，如果窗口计数恰好等于 need（说明之前多了一个，现在正好相等），diff 减 1
            elif window[left_idx] == need[left_idx] + 1:
                diff -= 1

            window[left_idx] -= 1
            left += 1

    return res
```

#### 复杂度

- **时间复杂度**：**O(n)** —— 每个字符最多进入窗口一次、离开一次，整个过程线性扫描。相比暴力的 **O(n·m)**，快了很多。  
- **空间复杂度**：**O(1)** —— 只用了固定长度的两个大小为 26 的数组和若干常数变量，和输入规模无关。

## 心得

- 本题核心是 **滑动窗口** + **字符计数（哈希表）**，通过让窗口在字符串上“滑动”，把重复的统计工作消除掉。  
- 这类技巧常用于：  
  1. **最长无重复子串**（滑动窗口 + 集合）  
  2. **最小覆盖子串**（滑动窗口 + 哈希表）  
  3. **子数组和为 K**（滑动窗口 + 前缀和）  
- 一句话总结解题钥匙：**“让窗口保持固定大小，只在两端增删字符，实时维护状态”**。

## 反思

- **第一反应**：直接把每个长度为 `len(p)` 的子串和 `p` 的字符计数比较，想到暴力遍历。  
- **最容易踩的坑**：  
  - 忘记处理 `s` 长度小于 `p` 的情况，会导致负数循环。  
  - 在更新 `diff` 时遗漏「从相等变为不相等」或「从不相等变为相等」的两种情况，导致答案错误。  
  - 字符只限小写英文字母时可以用固定长度数组，否则需要 `defaultdict`。  
- **下次遇到类似题**：第一步先判断是否可以使用「固定窗口大小」的滑动窗口，然后准备「目标计数」和「窗口计数」两套哈希表，利用增删字符的差异来实时判断是否匹配。