# #3. 最长不含重复字符的子串 / Longest Substring Without Repeating Characters

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

---

## 题目（英文原版）

**Description**

Given a string s, find the length of the longest substring without duplicate characters.

**Examples**

**Example 1:**

```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

**Example 2:**

```
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**

```
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
```

**Constraints**

- 0 <= s.length <= 5 * 104
- s consists of English letters, digits, symbols and spaces.

---

## 题目（中文翻译）

给定一个字符串 `s`，求不含重复字符的最长子串（substring）的长度。

## 示例

### 示例 1
**输入**  
```text
s = "abcabcbb"
```
**输出**  
```text
3
```
**解释**  
答案是 `"abc"`，其长度为 3。

### 示例 2
**输入**  
```text
s = "bbbbb"
```
**输出**  
```text
1
```
**解释**  
答案是 `"b"`，其长度为 1。

### 示例 3
**输入**  
```text
s = "pwwkew"
```
**输出**  
```text
3
```
**解释**  
答案是 `"wke"`，其长度为 3。需要注意的是，答案必须是子串（substring），`"pwke"` 是子序列（subsequence），而不是子串。

## 约束条件
- `0 <= s.length <= 5 * 10^4`
- `s` 只包含英文字母、数字、符号和空格。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把字符串里所有可能的子串都枚举出来**，然后检查每个子串里有没有重复字符，合法的就记下它的长度，最后取最大的那个。  

- **枚举子串**：可以用两个循环，外层循环决定子串的左端 `i`，内层循环决定右端 `j`（`j` 从 `i` 开始向右扩展）。  
- **检查是否有重复字符**：对每个子串，用一个集合（`set`）把出现的字符收集起来。如果在加入新字符时发现它已经在集合里，说明出现了重复，子串不合法。  
- **为什么正确**：我们遍历了 **所有** 连续的子串，且每个子串都严格检查了是否有重复字符，只要把合法子串的长度取最大，就一定得到答案。  

> **类比**：集合就像一本字典，字典里每个单词对应一个页码（这里的“页码”是字符本身）。查找一个字符是否已经出现，就像在字典里查词一样——如果已经在字典里，就说明重复了。  

#### 代码（Python）  

```python
def length_of_longest_substring_brute(s: str) -> int:
    n = len(s)
    max_len = 0                     # 记录当前找到的最长合法子串长度

    # i 为子串的左边界，范围是 0 ~ n-1
    for i in range(n):
        seen = set()                # 用集合存放当前子串出现的字符
        # j 为子串的右边界（包括 j），从 i 开始向右扩展
        for j in range(i, n):
            if s[j] in seen:        # 如果字符已经出现，子串不合法，停止扩展
                break
            seen.add(s[j])          # 把新字符加入集合
            # 此时子串 s[i:j+1] 合法，更新最大长度
            max_len = max(max_len, j - i + 1)

    return max_len
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环 `n` 次，内层在最坏情况下也会遍历 `n` 次（比如全都是不重复的字符），所以大概是 `n * n`。  
  - 大白话：如果字符串长度是 10,000，暴力解大概要跑 100,000,000 次循环，显然会很慢。  

- **空间复杂度**：`O(min(n, m))`，这里 `m` 是字符集大小（英文字母、数字、符号共 128 左右），集合最多存放当前子串的字符。  
  - 实际上最多只会存 `n` 个字符，最坏 `O(n)`，但因为字符种类有限，实际占用更小。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次左边界 `i` 移动时，都要重新从头检查子串**。我们可以利用 **滑动窗口**（Two‑Pointer）把检查过程“记住”，让左指针和右指针只各走一遍。  

1. **窗口的定义**：用两个指针 `left`、`right` 表示当前无重复字符的子串 `s[left:right]`（左闭右开区间）。  
2. **哈希表记录字符上一次出现的位置**：用字典 `last_index` 保存每个字符最近一次出现的下标。这样当右指针遇到一个已经出现过的字符时，就能快速知道它上次出现的位置。  
3. **遇到重复字符时，左指针要跳过去**：  
   - 假设 `s[right] = 'a'`，而 `'a'` 上一次出现的位置是 `last_index['a'] = 5`，当前 `left` 为 3。  
   - 为了让窗口再次合法，`left` 必须至少移动到 `5 + 1 = 6`（即把上一次的 `'a'` 排除在窗口外）。  
   - 但如果 `left` 已经在 7 了（说明窗口已经不包含那次 `'a'`），就不需要回退，直接取 `max(left, last_index['a'] + 1)`。  
4. **每次右指针前进后，都更新答案**：窗口长度 = `right - left + 1`（因为这里我们把 `right` 当成闭区间），取最大值即可。  

> **类比**：想象你在走廊里搬箱子，每搬一个新箱子（字符）都要检查前面是否已经有同样的箱子。如果有，就把左边的箱子全部搬走，直到同样的箱子不在视线里。字典 `last_index` 就像是墙上贴的“箱子位置表”，帮助你快速定位需要搬走到哪儿。  

#### 代码（Python）  

```python
def length_of_longest_substring(s: str) -> int:
    """
    滑动窗口 + 哈希表（字典）实现 O(n) 时间复杂度
    """
    last_index = {}          # 记录字符最近一次出现的下标
    max_len = 0              # 当前找到的最长合法子串长度
    left = 0                 # 窗口左边界

    # right 逐个遍历字符串的每个字符
    for right, ch in enumerate(s):
        # 如果字符 ch 之前出现过，并且出现位置在当前窗口内
        if ch in last_index and last_index[ch] >= left:
            # 把左边界移动到上一次出现位置的下一位
            left = last_index[ch] + 1

        # 更新字符 ch 的最新出现位置
        last_index[ch] = right

        # 计算当前窗口长度（right 是闭区间，所以 +1）
        cur_len = right - left + 1
        max_len = max(max_len, cur_len)   # 更新答案

    return max_len
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - `right` 指针只向右走一遍，`left` 指针也只会前进（永不后退），所以总的操作次数和字符串长度成正比。  
  - 大白话：如果 `n = 50,000`，只需要大约 50,000 次循环，瞬间就能算完。  

- **空间复杂度**：`O(min(n, m))`（这里 `m` 为字符种类数）  
  - 字典最多保存每个字符最近一次出现的位置，字符种类有限（ASCII 128），所以最坏是 `O(128)`，实际上可以看作 `O(1)` 常数空间。  

---  

## 心得  

- **核心技巧**：滑动窗口（Two‑Pointer）配合哈希表记录字符位置。  
- **适用的题型**：  
  1. 「最长子数组/子串满足某种条件」——如 *Maximum Size Subarray Sum Equals k*、*Longest Subarray with At Most K Distinct Numbers*。  
  2. 「最短子串覆盖全部目标字符」——如 *Minimum Window Substring*。  
  3. 「子数组/子串中不存在重复」——如 *Longest Substring with At Most Two Distinct Characters*。  
- **一句话总结解题钥匙**：**把“窗口”当成一条正在滑动的绳子，遇到冲突时把左端直接拉到冲突点的右侧，整条绳子永远保持合法**。  

## 反思  

- **第一反应**：想到枚举所有子串，逐个检查是否有重复。  
- **最容易踩的坑**：  
  - 忘记在遇到重复字符时把左指针 **取最大**（`max(left, last_index[ch] + 1)`），否则会把已经合法的字符错误地踢出窗口。  
  - 边界条件：空字符串应返回 `0`，单字符返回 `1`。  
- **下次遇到同类题**：第一步先问自己「是否可以用滑动窗口把区间维护为满足条件的最小/最大」；如果答案是“可以”，就立刻准备一个哈希表/计数器来帮助快速判断窗口是否合法。