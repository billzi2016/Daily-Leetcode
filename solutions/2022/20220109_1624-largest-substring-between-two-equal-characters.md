# #1624. 两个相等字符之间的最长子字符串 / Largest Substring Between Two Equal Characters

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/largest-substring-between-two-equal-characters/)

---

## 题目（英文原版）

**Description**

Given a string s, return the length of the longest substring between two equal characters, excluding the two characters. If there is no such substring return -1.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "aa"
Output: 0
Explanation: The optimal substring here is an empty substring between the two 'a's.
```

**Example 2:**

```
Input: s = "abca"
Output: 2
Explanation: The optimal substring here is "bc".
```

**Example 3:**

```
Input: s = "cbzxy"
Output: -1
Explanation: There are no characters that appear twice in s.
```

**Constraints**

- 1 <= s.length <= 300
- s contains only lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `s`，返回两个相同字符之间的最长子字符串（substring）的长度，**不包括**这两个字符本身。如果不存在满足条件的子字符串，返回 `-1`。  
子字符串（substring）是字符串中连续的字符序列。

**示例**  

**示例 1**  
```text
Input: s = "aa"
Output: 0
Explanation: 最优的子字符串是位于两个 `'a'` 之间的空子字符串，长度为 0。
```

**示例 2**  
```text
Input: s = "abca"
Output: 2
Explanation: 最优的子字符串是 `"bc"`，长度为 2。
```

**示例 3**  
```text
Input: s = "cbzxy"
Output: -1
Explanation: 字符串中没有出现两次的字符，因此不存在满足条件的子字符串。
```

**约束条件**  

- `1 <= s.length <= 300`
- `s` 仅包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把**所有可能的字符对**都枚举一遍，看看它们之间的子串有多长。  
- **数据结构**：我们只需要遍历字符串本身，用两个循环分别取左边字符的下标 `i` 和右边字符的下标 `j`（`j > i`）。可以把这两个下标想象成 **两个人站在排队的队伍里**，左边的 `i` 先走，右边的 `j` 后走。  
- 对每一对 `(i, j)`，如果 `s[i] == s[j]`，说明这两个字符相等，它们之间的子串长度就是 `j - i - 1`（两字符本身不算）。把所有满足条件的长度取最大值，就是答案。  
- 如果遍历完都没有找到相等的字符对，返回 `-1`。  

**为什么这个方法正确**：因为我们检查了**所有**可能的相等字符对，最大子串必然出现在其中的某一对里，所以取最大就一定是正确的。

#### 代码（Python）  
```python
def maxLengthBetweenEqualCharacters_bruteforce(s: str) -> int:
    n = len(s)
    ans = -1                      # 初始答案设为 -1，表示还未找到合法子串
    # 双层循环枚举所有字符对 (i, j)
    for i in range(n):
        for j in range(i + 1, n):
            if s[i] == s[j]:      # 两字符相等才考虑
                cur_len = j - i - 1   # 两字符之间的长度（不包括两端字符）
                ans = max(ans, cur_len)   # 更新最大值
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n²)`。我们用了两层循环，外层 `n` 次，内层最坏也要遍历 `n` 次，所以总操作次数大约是 `n * n`，即 **平方级**。如果 `n=300`，最坏会有 90 000 次比较，对机器来说还能接受，但不是最优的。  
- **空间复杂度**：`O(1)`。只用了几个整数变量，和输入大小无关。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**真正耗时的地方是重复遍历同一个字符的所有位置**。  
观察题目：我们只关心每个字符的**最左**出现位置和**最右**出现位置，因为这两者之间的距离最大。  
- 如果我们已经知道字符 `'a'` 第一次出现的位置是 `first['a']`，最后一次出现的位置是 `last['a']`，那么 `'a'` 能产生的最长子串长度就是 `last['a'] - first['a'] - 1`。  
- 对所有 26 个小写字母分别做同样的计算，取最大的那个即可。  

**如何一次遍历得到 `first` 和 `last`**：  
- 用两个大小为 26 的数组（或字典）记录每个字符的**首次出现**和**最近一次出现**下标。  
- 当遍历字符串时，若字符 `c` 第一次出现，就把下标写入 `first[c]`；每次看到 `c` 都把下标写入 `last[c]`（于是遍历结束后 `last[c]` 自动变成最右侧位置）。  
- 这里的数组就像 **一本字典**，`key` 是字母，`value` 是下标。  

这样只需要一次线性扫描，时间从 `O(n²)` 降到 `O(n)`，空间只用了固定的 26 个位置（常数级别），非常高效。

#### 代码（Python）  
```python
def maxLengthBetweenEqualCharacters(s: str) -> int:
    # 记录每个字符的最左下标，初始化为 None 表示还没出现
    first_pos = [None] * 26   # 26 个小写字母
    # 记录每个字符的最右下标，初始化为 -1 方便后面比较
    last_pos = [-1] * 26

    for idx, ch in enumerate(s):
        i = ord(ch) - ord('a')   # 把字符映射到 0~25 的数组下标
        if first_pos[i] is None:   # 第一次看到这个字符
            first_pos[i] = idx
        # 每次出现都更新最右下标
        last_pos[i] = idx

    ans = -1
    for i in range(26):
        if first_pos[i] is not None and last_pos[i] > first_pos[i]:
            # 两端字符之间的长度（不包括端点本身）
            cur_len = last_pos[i] - first_pos[i] - 1
            ans = max(ans, cur_len)

    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n)`。只遍历字符串一次，`n` 为字符串长度。对于 `n=300`，最多只做 300 次简单的数组操作。  
- **空间复杂度**：`O(1)`（常数级）。我们只用了长度为 26 的两个列表，无论输入多长，额外空间都不会增长。

---

## 心得  

- **核心技巧**：记录每个字符的最左/最右出现位置（**一次遍历 + 哈希表/数组**）。  
- **适用的题型**：  
  1. “找字母之间的最大距离” 类似题，如 *Maximum Distance Between Two Same Elements*。  
  2. “统计字符出现区间” 的问题，如 *Longest Substring with At Most K Distinct Characters*（需要区间信息）。  
  3. “求两次出现之间的最大间隔” 之类的子串/子数组问题。  
- **一句话总结解题钥匙**：**只关心每个字符的最左和最右位置，最大间隔自然出现**。

---

## 反思  

- **第一反应**：看到“两个相等字符之间的最长子串”，本能会想到**枚举所有字符对**（暴力），因为这样最容易写出正确代码。  
- **最容易踩的坑**：  
  - 忘记 **排除两端字符本身**，导致答案多加了 `+1`。  
  - 当字符只出现一次时，`last - first - 1` 会得到 `-1`，需要确保只在出现至少两次时才更新答案。  
  - 边界情况：字符串长度为 1 或所有字符都不重复时，返回 `-1`。  
- **下次遇到同类题**：第一步先问自己“**我只需要每个字符的最左/最右位置吗？**”，如果答案是“是”，就立刻转向一次遍历的哈希表/数组解法。