# #2414. **最长字母连续子串的长度** / Length of the Longest Alphabetical Continuous Substring

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/length-of-the-longest-alphabetical-continuous-substring/)

---

## 题目（英文原版）

**Description**

An alphabetical continuous string is a string consisting of consecutive letters in the alphabet. In other words, it is any substring of the string "abcdefghijklmnopqrstuvwxyz".
Given a string s consisting of lowercase letters only, return the length of the longest alphabetical continuous substring.

**Examples**

**Example 1:**

```
Input: s = "abacaba"
Output: 2
Explanation: There are 4 distinct continuous substrings: "a", "b", "c" and "ab".
"ab" is the longest continuous substring.
```

**Example 2:**

```
Input: s = "abcde"
Output: 5
Explanation: "abcde" is the longest continuous substring.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of only English lowercase letters.

---

## 题目（中文翻译）

字母连续字符串（alphabetical continuous string）是指由字母表中连续字母组成的字符串。换句话说，它是字符串 `"abcdefghijklmnopqrstuvwxyz"` 的任意子串（substring）。

给定仅包含小写字母的字符串 `s`，返回最长字母连续子串的长度。

**示例 1**

```text
Input: s = "abacaba"
Output: 2
```

**解释**：共有 4 种不同的连续子串：`"a"`、`"b"`、`"c"` 和 `"ab"`。其中 `"ab"` 是最长的连续子串。

**示例 2**

```text
Input: s = "abcde"
Output: 5
```

**解释**：`"abcde"` 是最长的连续子串。

**约束条件**

- `1 <= s.length <= 10^5`
- `s` 仅由英文字母小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子串**，检查每个子串是否满足“字母连续”的条件，然后记录最长的长度。

- **枚举子串**：我们可以用两层循环，外层 `i` 表示子串的起始位置，内层 `j` 表示子串的结束位置（`i ≤ j`），这样可以遍历 `s` 的所有 `O(n²)` 个子串。
- **判断连续**：对于一个子串 `s[i…j]`，只要相邻字符的 ASCII 码差等于 1（即 `ord(s[k]) + 1 == ord(s[k+1])`）就说明它们在字母表中相邻。遍历子串内部一次即可判断。
- **记录答案**：如果当前子串是连续的，就把它的长度 `j-i+1` 和目前的最大值比较，取更大的那个。

> **类比**：把字符串想象成一排排小盒子，每个盒子里装着一个字母。暴力解相当于让我们把每一段连续的盒子都挑出来检查一次，看看盒子里的字母是不是顺序递增的——这显然会花很多时间。

#### 代码（Python）

```python
def longestAlphabeticalSubstring_bruteforce(s: str) -> int:
    n = len(s)
    max_len = 1                     # 至少有一个字符的子串
    # 枚举子串的左端点 i
    for i in range(n):
        # 枚举子串的右端点 j
        for j in range(i, n):
            # 检查子串 s[i:j+1] 是否连续
            ok = True
            for k in range(i, j):
                # ord('a') = 97，后一个字符应该比前一个大 1
                if ord(s[k]) + 1 != ord(s[k + 1]):
                    ok = False
                    break
            if ok:
                cur_len = j - i + 1
                if cur_len > max_len:
                    max_len = cur_len
    return max_len
```

> **关键行中文注释**  
> - `for i in range(n)`: 把每个位置当作子串的起点。  
> - `for j in range(i, n)`: 把每个位置当作子串的终点。  
> - `if ord(s[k]) + 1 != ord(s[k + 1])`: 判断相邻字符是否在字母表中相邻。  

#### 复杂度

- **时间复杂度**：`O(n³)`。外层两层循环枚举子串是 `O(n²)`，每次还要在子串内部遍历一次检查连续性，最坏情况下子串长度为 `O(n)`，于是总体是 `O(n³)`。  
  - 大白话：如果字符串长度是 1000，算法大概会做 1000³ ≈ 10⁹ 次比较，明显太慢。
- **空间复杂度**：`O(1)`。只用了常数个额外变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**检查每个子串的过程是重复的**：当我们已经知道 `s[i…j]` 是连续的，那么 `s[i…j+1]` 只需要再检查 `s[j]` 与 `s[j+1]` 是否相邻即可。于是我们可以 **一次遍历**，用滑动窗口的思想实时维护当前正在增长的连续子串长度。

具体步骤：

1. 初始化 `cur_len = 1`（当前连续子串的长度），`max_len = 1`（全局最大）。
2. 从左到右遍历字符串（从第二个字符开始），记下前一个字符 `prev`。
3. 如果 `prev` 与当前字符 `c` 在字母表中相邻（`ord(prev) + 1 == ord(c)`），说明连续子串可以 **继续延长**，`cur_len += 1`。
4. 否则，连续被打断，需要 **重新开始**，把 `cur_len` 重置为 `1`（当前字符自己是一个长度为 1 的连续子串）。
5. 每一步都把 `cur_len` 和 `max_len` 做比较，保留更大的值。
6. 循环结束后，`max_len` 就是答案。

> **类比**：把字符看成排队的小朋友，只有当后面的孩子的名字字母恰好比前面一个大 1 时，才算是“好朋友”。我们只需要记录当前这条好朋友链有多长，一旦链断了，就从新起一条链，整个过程只走一遍队列。

#### 代码（Python）

```python
def longestAlphabeticalSubstring(s: str) -> int:
    """
    一次遍历，实时维护当前连续子串的长度。
    时间 O(n)，空间 O(1)。
    """
    if not s:                     # 防御性检查，虽然题目保证非空
        return 0

    max_len = 1                   # 最长长度，至少有一个字符
    cur_len = 1                   # 当前连续子串的长度

    # 从第二个字符开始遍历
    for i in range(1, len(s)):
        # 前一个字符
        prev = s[i - 1]
        # 当前字符
        cur = s[i]

        # 判断是否在字母表中相邻
        if ord(prev) + 1 == ord(cur):
            cur_len += 1          # 连续，长度加一
        else:
            cur_len = 1           # 断了，重新计数

        # 更新全局最大值
        if cur_len > max_len:
            max_len = cur_len

    return max_len
```

> **关键行中文注释**  
> - `if ord(prev) + 1 == ord(cur)`: 判断两字符是否是字母表中相邻的。  
> - `cur_len += 1`: 当前连续子串继续增长。  
> - `cur_len = 1`: 连续被中断，需要重新开始计数。  

#### 复杂度

- **时间复杂度**：`O(n)`。只遍历一次字符串，`n` 是字符串长度。  
  - 与暴力解相比，从 `O(n³)` 降到了线性，几乎可以在 10⁵ 长度的输入上毫秒级完成。
- **空间复杂度**：`O(1)`。只使用了几个整数变量，和输入大小无关。

---

## 心得

- **核心技巧**：一次遍历 + 实时维护“当前满足条件的子序列长度”。这是一种**滑动窗口/计数型**思路，适用于所有“连续/递增/递减”类子串问题。
- **适用题型**：
  1. *Longest Continuous Increasing Subarray*（最长连续递增子数组）  
  2. *Maximum Consecutive Ones*（最长连续 1 的子序列）  
  3. *Longest Substring with At Most K Distinct Characters*（最多 K 种字符的最长子串）——思路上也会用到滑动窗口，只是窗口的移动方式不同。
- **一句话总结**：**只要能把“是否满足条件”转化为相邻元素之间的简单比较，就可以用一次遍历实时计数，省去所有子串枚举**。

---

## 反思

- **第一反应**：看到“连续字母”立刻想到“检查相邻字符的 ASCII 差”，于是想到暴力枚举所有子串。
- **最容易踩的坑**：
  1. **边界条件**：字符串长度为 1 时，答案应为 1，需要初始化 `max_len` 为 1（而不是 0）。
  2. **字符比较**：不要忘记使用 `ord()` 将字符转成整数比较，否则 `'a' < 'b'` 只能比较字典序，无法直接判断差值是否为 1。
  3. **重置计数**：当连续被打断时必须把 `cur_len` 重置为 **1**（当前字符本身），而不是 0。
- **下次遇到同类题**：第一步想到 **“把问题转化为相邻元素之间的关系”，然后尝试用一次遍历维护当前满足关系的长度或窗口**。这样往往能直接得到 O(n) 的最优解。