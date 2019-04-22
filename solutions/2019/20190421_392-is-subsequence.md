# #392. 判断子序列 / Is Subsequence

> 难度：简单 · 标签：Two Pointers、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/is-subsequence/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, return true if s is a subsequence of t, or false otherwise.
A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).

**Examples**

**Example 1:**

```
Input: s = "abc", t = "ahbgdc"
Output: true
```

**Example 2:**

```
Input: s = "axc", t = "ahbgdc"
Output: false
```

**Constraints**

- 0 <= s.length <= 100
- 0 <= t.length <= 104
- s and t consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串（string）`s` 和 `t`，如果 `s` 是 `t` 的子序列（subsequence），返回 `true`；否则返回 `false`。  
子序列（subsequence）是指从原字符串中删除若干（可以为零）字符后得到的新字符串，且不改变剩余字符的相对顺序。  
例如，`"ace"` 是 `"abcde"` 的子序列，而 `"aec"` 不是。

**示例 1**

```text
Input: s = "abc", t = "ahbgdc"
Output: true
```

**示例 2**

```text
Input: s = "axc", t = "ahbgdc"
Output: false
```

**约束条件**

- `0 <= s.length <= 100`
- `0 <= t.length <= 10^4`
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把 **t** 当成一本书，把 **s** 当成一段想要找的文字。我们把 **s** 的每一个字符都在 **t** 中去找一次，找到后再往后继续找下一个字符。如果 **t** 的结尾都找不到某个字符，就说明 **s** 不是 **t** 的子序列。

实现上可以用两层循环：

1. 外层遍历 **s** 的每个字符 `c`。  
2. 内层从 **t** 当前搜索位置开始往后找，看看有没有和 `c` 相同的字符。  
   - 找到就把搜索位置往后移一位，继续外层的下一个字符。  
   - 找不到就直接返回 `False`。

这里用到的“搜索位置”相当于在 **t** 里开了一本“指针笔记本”，每次找到字符后把笔记本的指针往后移动，保证后面的字符仍然保持原来的相对顺序——这正是子序列的定义。

**为什么正确**  
因为我们严格按照 **s** 中字符的顺序，在 **t** 中从左到右依次寻找匹配的字符。如果能够顺序匹配完所有字符，说明 **s** 可以通过在 **t** 中删掉若干字符得到；否则不可能。

#### 代码（Python）

```python
def is_subsequence_brute(s: str, t: str) -> bool:
    # 当前在 t 中的搜索起点（相当于指针位置），初始在第 0 位
    start = 0

    # 遍历 s 的每个字符
    for ch in s:
        # 在 t 中从 start 开始找与 ch 相同的字符
        found = False
        while start < len(t):
            if t[start] == ch:          # 找到匹配
                found = True
                start += 1              # 指针往后移，准备找下一个字符
                break
            start += 1                  # 继续向后扫描
        if not found:                   # 本轮遍历没有找到匹配字符
            return False
    return True                         # 所有字符都匹配成功
```

#### 复杂度

- **时间复杂度**：`O(|s| * |t|)`  
  直观解释就是：如果 **s** 长 5，**t** 长 1000，最坏情况下要检查 5 × 1000 = 5000 次字符。这里的 `|x|` 表示字符串的长度。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量（指针、标记），不随输入规模增长而增加内存。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于：每找不到一个字符时，我们仍然会继续在 **t** 中向后遍历，导致 **t** 可能被多次扫描。其实，只需要一次线性扫描即可完成全部匹配：

- 使用 **双指针**（Two Pointers）技巧：  
  - `i` 指向 **s** 的当前字符位置。  
  - `j` 指向 **t** 的当前字符位置。  
- 同时从左到右遍历 **t**（`j` 前进），每当 `t[j] == s[i]` 时，就把 `i` 往前移动一位（表示已经匹配了 **s** 的一个字符）。  
- 当 `i` 移动到 **s** 的末尾（`i == len(s)`）时，说明所有字符都已经匹配成功，直接返回 `True`。  
- 如果 **t** 扫描完仍未把 `i` 推到末尾，则返回 `False`。

这个思路的核心是“**一次遍历**”。我们只需要一次遍历 **t**，在遍历的过程中顺便检查 **s** 是否匹配完。因为每个字符最多被比较一次，时间就从 `O(|s|*|t|)` 降到了 `O(|t|)`，而且在最坏情况下 `|t|` 也是 10⁴，完全可以接受。

**类比**：把 **t** 想象成一条流水线，**s** 的每个字符是要在流水线上“贴标签”的需求。流水线每经过一个位置，就检查这个位置的字符是否正好是当前需求的标签。如果是，就完成一个需求并转向下一个需求。流水线只跑一遍，所有需求都完成了，就说明 **s** 是 **t** 的子序列。

#### 代码（Python）

```python
def is_subsequence(s: str, t: str) -> bool:
    # i 指向 s，j 指向 t
    i, j = 0, 0
    while i < len(s) and j < len(t):
        # 当 t[j] 与 s[i] 相同，说明匹配成功，s 往前走一步
        if s[i] == t[j]:
            i += 1
        # t 总是往前走一步，寻找下一个可能的匹配位置
        j += 1

    # 如果 i 已经走到 s 的末尾，说明全部匹配成功
    return i == len(s)
```

#### 复杂度

- **时间复杂度**：`O(|t|)`  
  只遍历了一遍 **t**，不管 **s** 有多长，最多检查 `|t|` 次字符。相当于把“10 000 次检查”直接对应到实际的字符数，易于理解。

- **空间复杂度**：`O(1)`  
  只用了两个整数指针 `i`、`j`，不随输入长度变化。

---

## 心得

- **核心技巧**：双指针（Two Pointers）一次遍历匹配。  
- **适用题型**：  
  1. 判断两个有序序列是否相互包含（如合并两个有序数组的过程）。  
  2. 判断是否可以通过删除字符得到子序列（本题）。  
  3. 在已排序的数组中查找满足某种条件的元素对（如两数之和的有序版）。  
- **一句话总结**：只要“从左到右一次遍历，两条指针同步前进”，子序列判断瞬间搞定。

---

## 反思

- **第一反应**：看到“子序列”，立刻想到要保持字符相对顺序，于是想到逐个匹配。  
- **最容易踩的坑**：  
  - **空串**：如果 `s` 为空，答案应该是 `True`（空串是任何字符串的子序列）。  
  - **指针越界**：在暴力实现里，需要注意 `start` 超出 `t` 长度时及时停止，否则会 IndexError。  
  - **字符重复**：要确保每次匹配后指针只向前移动一次，防止重复使用同一个字符。  
- **下次思路**：遇到“在两个序列中保持相对顺序”的问题，第一步就想“双指针一次遍历”，再根据具体需求决定是否需要额外的缓存或数据结构。