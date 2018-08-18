# #76. 最小覆盖子串 / Minimum Window Substring

> 难度：困难 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/minimum-window-substring/)

---

## 题目（英文原版）

**Description**

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
The testcases will be generated such that the answer is unique.
Follow up: Could you find an algorithm that runs in O(m + n) time?

**Examples**

**Example 1:**

```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
```

**Example 2:**

```
Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.
```

**Example 3:**

```
Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.
```

**Constraints**

- m == s.length
- n == t.length
- 1 <= m, n <= 105
- s and t consist of uppercase and lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定两个字符串 `s` 和 `t`，它们的长度分别为 `m` 和 `n`。返回 `s` 中的最小窗口子串（minimum window substring），使得窗口内包含 `t` 中的每个字符（包括重复字符）。如果不存在满足条件的子串，返回空字符串 `""`。  
测试用例保证答案唯一。

**示例 1**  
**输入**: `s = "ADOBECODEBANC", t = "ABC"`  
**输出**: `"BANC"`  
**解释**: 最小窗口子串 `"BANC"` 包含了字符串 `t` 中的字符 `'A'`、`'B'` 和 `'C'`。

**示例 2**  
**输入**: `s = "a", t = "a"`  
**输出**: `"a"`  
**解释**: 整个字符串 `s` 本身就是最小窗口。

**示例 3**  
**输入**: `s = "a", t = "aa"`  
**输出**: `""`  
**解释**: 必须在窗口中包含 `t` 的两个 `'a'`，但 `s` 中最多只有一个 `'a'`，因此返回空字符串。

**约束条件**  
- `m == s.length`  
- `n == t.length`  
- `1 <= m, n <= 10^5`  
- `s` 和 `t` 只包含大小写英文字母。

**进阶**  
能否设计出时间复杂度为 `O(m + n)` 的算法？

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **s** 的所有可能子串都枚举一遍，检查每个子串里是否包含 **t** 中的所有字符（包括重复次数），如果满足就记录下长度最短的那个。  

- **枚举子串**：可以用两层循环，外层决定子串的左端点 `left`，内层决定右端点 `right`（左闭右闭区间 `[left, right]`）。  
- **检查是否覆盖**：把 **t** 中每个字符出现的次数统计到一个哈希表（类似查字典：键是字符，值是该字符需要出现的次数）。然后遍历子串，把子串里出现的字符也放进另一个哈希表，比较两个表是否“一致”。  
- **为什么正确**：因为我们把 **s** 的每一个子串都检查了一遍，只要有满足条件的子串，就一定会被找到，最短的自然也会被记录。  

> **哈希表的类比**：想象一本词典，查一个单词时先看键（单词本身），再得到对应的页码（这里的页码就是字符出现的次数）。我们把 **t** 看成需要查的单词表，把子串看成实际翻开的页面，只有页面上出现的所有单词次数都不低于词典里的需求，才算“覆盖”。

#### 代码（Python）  

```python
def minWindow_bruteforce(s: str, t: str) -> str:
    from collections import Counter

    need = Counter(t)                     # t 中每个字符需要的次数
    m, n = len(s), len(t)
    best = ""                             # 记录最短合法子串
    best_len = float('inf')               # 初始设为正无穷大

    # 枚举左端点
    for left in range(m):
        # 枚举右端点
        for right in range(left, m):
            window = s[left:right + 1]    # 当前子串
            # 统计子串中字符出现次数
            have = Counter(window)
            # 检查是否每个字符的次数都满足需求
            if all(have[c] >= need[c] for c in need):
                cur_len = right - left + 1
                if cur_len < best_len:    # 找到更短的合法窗口
                    best_len = cur_len
                    best = window
                break                     # 左端点固定后，后面的右端点只会更长，直接跳出内层

    return best
```

#### 复杂度  

- **时间复杂度**：`O(m³)`（大概）  
  - 两层循环枚举所有子串是 `O(m²)`，  
  - 对每个子串我们又要遍历一次子串来统计字符（最坏情况是 `O(m)`），  
  - 所以总体是 `O(m³)`。  
  - **大白话**：如果 **s** 长度是 1000，暴力解大概要做 10⁹ 次操作，几乎不可接受。  
- **空间复杂度**：`O(|Σ|)`，这里 Σ 是字符集合（最多 52 个英文字母），因为我们只存两个计数字典。  

---  

### 2. 最优解  

#### 思路  

暴力解的主要瓶颈是**重复遍历同一个字符**。我们可以用 **滑动窗口**（two‑pointer）技巧，只让左右指针在 **s** 上各走一遍，做到 **O(m + n)** 的线性时间。

1. **先统计 t 中每个字符需要的次数**，用 `need` 哈希表。  
2. 用两个指针 `left`、`right` 维护一个“窗口” `[left, right)`（左闭右开），窗口内部的字符出现次数记录在 `window` 哈希表。  
3. **扩大窗口**：不断右移 `right`，把字符加入 `window`，直到窗口已经“覆盖”了 `t`（即 `window` 中每个字符的次数都不小于 `need`）。这一步相当于在找一个**可行的**窗口。  
4. **收缩窗口**：只要窗口仍然满足覆盖条件，就左移 `left`，尝试把窗口缩小，同时更新最短答案。左移时要把离开的字符从 `window` 中减掉，可能导致窗口不再满足条件，此时停止收缩，回到第 3 步继续扩大。  
5. 整个过程 `right` 只会从左到右遍历一次，`left` 也只会向右移动不回头，所以时间是线性的。

> **滑动窗口的类比**：想象你在一条长走廊上搬箱子，左手和右手各抓住一段箱子形成一个“窗口”。右手不断往前推，装进更多箱子；当手里的箱子已经满足需求（比如装满了指定种类的物品），左手就开始收紧，去掉不必要的箱子，使窗口尽可能短。整个过程只走一遍走廊。

#### 代码（Python）  

```python
def minWindow(s: str, t: str) -> str:
    from collections import Counter, defaultdict

    need = Counter(t)                     # t 中每个字符的需求次数
    required = len(need)                  # 需要满足的不同字符种类数
    formed = 0                            # 当前窗口已经满足的种类数

    window_counts = defaultdict(int)     # 窗口内字符出现次数
    left = 0
    right = 0
    ans = (float('inf'), None, None)      # (窗口长度, 左端点, 右端点)

    while right < len(s):
        # 1) 把右指针指向的字符加入窗口
        char = s[right]
        window_counts[char] += 1

        # 2) 如果加入后恰好满足了该字符的需求，formed 加 1
        if char in need and window_counts[char] == need[char]:
            formed += 1

        # 3) 当窗口已经覆盖所有需求时，尝试收缩左边界
        while left <= right and formed == required:
            # 更新最小答案
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)

            # 移除左指针指向的字符，准备左移
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in need and window_counts[left_char] < need[left_char]:
                formed -= 1          # 失去了一种满足的字符

            left += 1                # 真正左移

        # 4) 继续向右扩张窗口
        right += 1

    # 如果没有找到合法窗口，返回空串
    if ans[0] == float('inf'):
        return ""
    return s[ans[1]: ans[2] + 1]
```

#### 复杂度  

- **时间复杂度**：`O(m + n)`  
  - `right` 指针遍历 **s** 一遍，`left` 指针最多也遍历一次，所以总操作次数与 **s** 长度线性相关；  
  - 统计 **t** 的次数是 `O(n)`，两者相加即 `O(m + n)`。  
  - **大白话**：如果 **s** 长 100,000，算法大概只需要几十万次基本操作，完全可以在毫秒级完成。  
- **空间复杂度**：`O(|Σ|)`，这里 Σ 为字符集合（最多 52 个英文字母），因为我们只维护两个计数字典 `need` 与 `window_counts`。  

---  

## 心得  

- 这道题的核心技巧是 **滑动窗口 + 哈希计数**，通过两个指针把“扩大-收缩”过程串起来。  
- 该技巧常用于**子串覆盖**、**子数组最小/最大长度**等问题，例如：  
  1. **Longest Substring Without Repeating Characters**（最长无重复字符子串）  
  2. **Find All Anagrams in a String**（在字符串中找所有字母异位词）  
  3. **Minimum Size Subarray Sum**（最小长度子数组和）  
- **一句话总结**：把“需要的东西”放进哈希表，用滑动窗口让左右指针在原串上只走一次，就能快速找到最小满足条件的区间。  

## 反思  

- **第一反应**：看到“每个字符都要出现”，自然想到枚举所有子串并逐个检查。  
- **最容易踩的坑**：  
  - **重复字符的计数**：忘记统计字符出现次数，只判断是否出现会导致错误（如 t="AA"）。  
  - **窗口收缩的边界**：在 `formed == required` 时才收缩，收缩时要先更新答案再减去左字符，否则可能错过最小窗口。  
  - **空答案的处理**：如果 s 中根本不包含 t 的全部字符，需要返回空串而不是错误的子串。  
- **下次遇到同类题**，第一步应该先 **统计需求**（构建哈希表），然后 **用滑动窗口尝试覆盖**，并在覆盖成功后 **收缩左边界**，如此即可快速逼近最优解。