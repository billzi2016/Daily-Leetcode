# #1234. 平衡字符串的子串替换 / Replace the Substring for Balanced String

> 难度：中等 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/replace-the-substring-for-balanced-string/)

---

## 题目（英文原版）

**Description**

You are given a string s of length n containing only four kinds of characters: 'Q', 'W', 'E', and 'R'.
A string is said to be balanced if each of its characters appears n / 4 times where n is the length of the string.
Return the minimum length of the substring that can be replaced with any other string of the same length to make s balanced. If s is already balanced, return 0.

**Examples**

**Example 1:**

```
Input: s = "QWER"
Output: 0
Explanation: s is already balanced.
```

**Example 2:**

```
Input: s = "QQWE"
Output: 1
Explanation: We need to replace a 'Q' to 'R', so that "RQWE" (or "QRWE") is balanced.
```

**Example 3:**

```
Input: s = "QQQW"
Output: 2
Explanation: We can replace the first "QQ" to "ER".
```

**Constraints**

- n == s.length
- 4 <= n <= 105
- n is a multiple of 4.
- s contains only 'Q', 'W', 'E', and 'R'.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串 `s`，仅包含四类字符：`'Q'`、`'W'`、`'E'` 和 `'R'`。  
如果字符串中每种字符出现的次数恰好为 `n / 4`（其中 `n` 为字符串的长度），则称该字符串为平衡（balanced）的。  

返回可以替换成任意相同长度字符串的子串（substring）的最小长度，使得 `s` 变为平衡的。如果 `s` 已经平衡，返回 `0`。

### 示例

#### 示例 1
**输入:** `s = "QWER"`  
**输出:** `0`  
**解释:** `s` 已经平衡。

#### 示例 2
**输入:** `s = "QQWE"`  
**输出:** `1`  
**解释:** 我们需要将一个 `'Q'` 替换为 `'R'`，使得 `"RQWE"`（或 `"QRWE"`）平衡。

#### 示例 3
**输入:** `s = "QQQW"`  
**输出:** `2`  
**解释:** 我们可以将前面的 `"QQ"` 替换为 `"ER"`。

### 约束条件
- `n == s.length`
- `4 <= n <= 10^5`
- `n` 为 `4` 的倍数
- `s` 只包含字符 `'Q'`、`'W'`、`'E'`、`'R'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子串**，把每个子串都换成任意长度相同的字符组合，然后检查整体是否平衡。  
- **枚举子串**：用两层循环，外层左指针 `l`（从 0 到 n‑1），内层右指针 `r`（从 `l` 到 n‑1），子串即 `s[l:r+1]`。  
- **换成任意字符**：因为我们只关心能否让整体平衡，只要子串外的字符已经满足「每种字符出现 ≤ n/4」的条件，就一定可以用合适的字符把子串内部填满，使整体恰好等于 n/4。  
- **检查平衡**：统计整个字符串中四种字符的出现次数，判断每种是否 ≤ n/4。

生活化类比：  
- 把字符串想象成四种水果的篮子（Q、W、E、R），我们想让每种水果恰好有相同的数量。暴力解相当于把篮子里的每一段水果全部拿出来，尝试重新装入任意水果，看看是否能达到均衡。

#### 代码（Python）

```python
from collections import Counter

def balancedString_bruteforce(s: str) -> int:
    n = len(s)
    target = n // 4                     # 每种字符理想的数量
    cnt = Counter(s)                    # 整体字符计数

    # 如果一开始已经平衡，直接返回 0
    if all(v <= target for v in cnt.values()):
        return 0

    ans = n  # 最坏情况是整串都要换

    # 暴力枚举所有子串 [l, r]
    for l in range(n):
        # 复制一份计数，用来在右指针移动时动态更新子串内部的字符
        cur_cnt = cnt.copy()
        for r in range(l, n):
            # 把 s[r] 从子串外移到子串内（相当于我们准备把它换掉）
            cur_cnt[s[r]] -= 1

            # 检查子串外的字符是否都 ≤ target
            if all(v <= target for v in cur_cnt.values()):
                ans = min(ans, r - l + 1)   # 更新最小长度
                break                       # 右指针再往右只会更长，直接退出内层

    return ans
```

> 关键行中文注释已经写在代码里，帮助理解每一步在做什么。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环遍历所有子串，最坏情况下要检查 `n*(n+1)/2 ≈ n²/2` 次。大白话：如果字符串长度是 10,000，暴力解大约要跑 100 000 000 次循环，明显太慢。
- **空间复杂度**：`O(1)`（不计输入字符串本身）  
  只用了常数级的计数器（四个字符的计数），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有子串**，导致二次遍历。我们其实只需要找到最短的子串，使得 **子串外的字符已经满足 ≤ n/4**。这正好可以用 **滑动窗口（双指针）** 来完成：

1. **先统计整体字符频率** `cnt`。如果每种字符本来就 ≤ `target`（`n/4`），直接返回 0。
2. **窗口左指针 `left` 固定在 0，右指针 `right` 向右扩张**。窗口内部的字符相当于「我们准备替换的部分」。
3. 每次把 `right` 指向的字符计入窗口（即从整体计数 `cnt` 中减去），相当于「把它移出窗口外」。
4. **检查窗口外的字符**（即 `cnt` 中剩余的计数）是否都 ≤ `target`。如果满足，说明当前窗口可以被替换成合适的字符，使整体平衡，此时尝试收缩窗口左边界 `left`（把左边字符移回窗口外）来寻找更短的合法窗口。
5. **循环结束** 时，记录的最小窗口长度即为答案。

核心概念解释：

- **滑动窗口**：想象一条可伸缩的绳子，左端和右端分别是 `left`、`right`。我们让绳子在字符串上滑动，随时记住绳子内部的字符（待替换），绳子外的字符必须满足「不超过目标数量」的约束。
- **前缀计数**：`cnt` 保存的是「窗口外」的字符频率。每次窗口右移，就把对应字符的计数减 1；左移时再加回去。这样可以在 **O(1)** 时间内判断窗口外是否已满足条件。

#### 代码（Python）

```python
from collections import Counter

def balancedString(s: str) -> int:
    n = len(s)
    target = n // 4                      # 每种字符理想的数量

    # 统计整体字符频率
    cnt = Counter(s)

    # 已经平衡直接返回 0
    if all(v <= target for v in cnt.values()):
        return 0

    left = 0
    ans = n                               # 最坏情况是全串都要换

    # 右指针遍历整个字符串
    for right, ch in enumerate(s):
        cnt[ch] -= 1                       # 把 s[right] 移入窗口（即窗口外计数减 1）

        # 当窗口外的所有字符都 ≤ target 时，窗口合法
        while left <= right and all(v <= target for v in cnt.values()):
            # 记录当前合法窗口长度
            ans = min(ans, right - left + 1)

            # 尝试收缩窗口：把左端字符移出窗口，恢复到窗口外计数
            cnt[s[left]] += 1
            left += 1

    return ans
```

> 关键行的中文注释已经写在代码里，帮助初学者一步步跟进。

#### 复杂度

- **时间复杂度**：`O(n)`  
  左右指针各最多遍历一次字符串，内部的 `while` 循环在整个过程中最多也只会执行 `n` 次（每次左指针右移一次）。大白话：即使字符串有 100 000 个字符，算法只会走大约 200 000 步，速度非常快。
- **空间复杂度**：`O(1)`（常数空间）  
  只用了四个字符的计数器 `cnt`，不随 `n` 增长。

---

## 心得

- **核心技巧**：**滑动窗口** + **字符计数**（相当于前缀和的思想）。  
- **适用的题型**：  
  1. 最小覆盖子串（LeetCode 76）——找最短子串使得窗口内包含所有目标字符。  
  2. 长度最小的子数组使得和 ≥ target（LeetCode 209）——窗口外的约束换成窗口内的约束。  
  3. 替换子串使得所有字符出现次数相等（本题）。  
- **一句话总结解题钥匙**：把「要替换的子串」看成「窗口」，只要窗口外的字符已经不超过目标数量，窗口就合法；于是用双指针让窗口在字符串上滑动，实时维护外部计数即可。

---

## 反思

- **第一反应**：直接想到枚举子串检查平衡，写出暴力实现；但立刻意识到 `n` 可达 `10⁵`，暴力 `O(n²)` 会超时。
- **最容易踩的坑**：  
  1. **边界条件**：字符串本身已经平衡时要提前返回 0。  
  2. **计数的增减顺序**：窗口右移时要先把字符从外部计数中减掉，左移时再加回去，顺序写错会导致判断条件永远不成立。  
  3. **`while` 循环的退出条件**：必须在窗口合法时才收缩，否则会把合法窗口错过。
- **下次遇到同类题**：第一步先 **统计整体频率**，判断是否已经满足要求；随后 **构造滑动窗口**，把「窗口外」的约束转化为「窗口内」的搜索目标，这样往往能把时间复杂度降到线性。