# #2730. 寻找最长半重复子串 / Find the Longest Semi-Repetitive Substring

> 难度：中等 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/find-the-longest-semi-repetitive-substring/)

---

## 题目（英文原版）

**Description**

You are given a digit string s that consists of digits from 0 to 9.
A string is called semi-repetitive if there is at most one adjacent pair of the same digit. For example, "0010", "002020", "0123", "2002", and "54944" are semi-repetitive while the following are not: "00101022" (adjacent same digit pairs are 00 and 22), and "1101234883" (adjacent same digit pairs are 11 and 88).
Return the length of the longest semi-repetitive substring of s.

**Examples**

**Example 1:**

```
Input: s = "52233"
Output: 4
Explanation:
The longest semi-repetitive substring is "5223". Picking the whole string "52233" has two adjacent same digit pairs 22 and 33, but at most one is allowed.
```

**Example 2:**

```
Input: s = "5494"
Output: 4
Explanation:
s is a semi-repetitive string.
```

**Example 3:**

```
Input: s = "1111111"
Output: 2
Explanation:
The longest semi-repetitive substring is "11". Picking the substring "111" has two adjacent same digit pairs, but at most one is allowed.
```

**Constraints**

- 1 <= s.length <= 50
- '0' <= s[i] <= '9'

---

## 题目（中文翻译）

你得到一个只包含字符 `'0'` 到 `'9'` 的数字字符串 `s`。  
如果一个字符串中至多只有 **一个相邻相同数字对**（adjacent pair of the same digit），则称其为 **半重复（semi-repetitive）**。例如，`"0010"`、`"002020"`、`"0123"`、`"2002"`、`"54944"` 都是半重复的，而下面的字符串不是：`"00101022"`（相邻相同数字对有 `00` 和 `22`）以及 `"1101234883"`（相邻相同数字对有 `11` 和 `88`）。  

返回 `s` 中 **最长半重复子串（semi-repetitive substring）** 的长度。

**示例 1**  
```text
Input: s = "52233"
Output: 4
Explanation:
最长的半重复子串是 "5223"。如果取整个字符串 "52233"，会出现两个相邻相同数字对 `22` 和 `33`，而只允许出现至多一个。
```

**示例 2**  
```text
Input: s = "5494"
Output: 4
Explanation:
整个字符串本身就是半重复的。
```

**示例 3**  
```text
Input: s = "1111111"
Output: 2
Explanation:
最长的半重复子串是 "11"。取子串 "111" 会出现两个相邻相同数字对，超过了限制。
```

**约束条件**  
- `1 <= s.length <= 50`  
- `'0' <= s[i] <= '9'`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把所有可能的子串都枚举出来，逐个判断它们是不是 **半重复**（semi‑repetitive），如果是，就把长度和当前的最大值比较，取最大。  

- **枚举子串**：把字符串的左边界 `i` 从 `0` 到 `n‑1`，右边界 `j` 从 `i` 到 `n‑1`，子串就是 `s[i:j+1]`。  
- **判断半重复**：遍历子串，统计相邻相同数字出现的次数，只要次数 ≤ 1 就满足要求。这里可以把 “相邻相同数字” 想象成在一排座位上，两个人坐在相邻的座位上并且是同一个人，最多只能出现一次。  

为什么这种方法一定能得到答案？因为我们把**所有**子串都检查了一遍，答案一定在其中。  

**复杂度分析（大白话）**  
- 外层两个循环枚举左、右边界，最坏情况下会产生 `n·(n+1)/2 ≈ n²/2` 个子串。  
- 对每个子串我们再遍历一次它的长度来统计相邻相同的次数，最坏情况是子串长度也是 `O(n)`。  
- 所以总时间是 `O(n³)`，在本题的约束 `n ≤ 50` 下仍然能跑完（50³ = 125 000，完全可以接受）。  
- 额外空间只用了常数个变量（计数器、指针），所以是 `O(1)`。  

#### 代码（Python）  

```python
def longestSemiRepetitive_bruteforce(s: str) -> int:
    n = len(s)
    ans = 0                       # 记录最长长度

    # 枚举子串的左端点 i
    for i in range(n):
        # 枚举子串的右端点 j（j >= i）
        for j in range(i, n):
            # 判断 s[i:j+1] 是否满足“相邻相同数字对 ≤ 1”
            cnt = 0                # 记录相邻相同的次数
            for k in range(i, j):  # 逐个检查相邻位置
                if s[k] == s[k + 1]:
                    cnt += 1
                    if cnt > 1:    # 已经超过 1，直接退出本子串的检查
                        break
            else:
                # 循环正常结束，说明 cnt ≤ 1，子串合法
                ans = max(ans, j - i + 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 先枚举左、右端点（两层循环），再遍历子串本身。  
  - “`O(n³)`” 可以理解为：如果把所有字符想象成小盒子，最多要检查 50×50×50 ≈ 125 000 次操作，电脑几毫秒就能完成。  
- **空间复杂度**：`O(1)` —— 只用了几个计数器和指针，和输入长度无关。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**瓶颈在于重复遍历同一个字符**。例如，子串 `"52233"` 的右端点从 `3` 移到 `4` 时，我们又要重新统计前面的相邻相同对，实际上只有新加入的字符 `3` 可能会产生新的相邻相同对。  

这正好适合 **滑动窗口（Sliding Window）** 的思路：  
- 用两个指针 `left`、`right` 维护一个窗口 `s[left:right+1]`，保证窗口内部**相邻相同数字对的数量 ≤ 1**。  
- 当窗口合法时，尝试把 `right` 向右扩张（加入新字符）。  
- 如果加入后窗口出现 **第二个** 相邻相同对，就必须收缩窗口的左边界 `left`，直到窗口再次合法。收缩的过程只需要把左指针往右移动，期间如果左侧恰好是之前的相邻相同对的左端字符，则该对会被“丢掉”，计数器 `dup_cnt` 减 1。  

关键点在于 **如何快速知道窗口里有多少个相邻相同对**。我们用一个整数 `dup_cnt` 记录当前窗口中相邻相同的次数。每次右指针移动到 `right`，只要检查 `s[right]` 与 `s[right-1]` 是否相同，就能决定是否要把 `dup_cnt` 加 1。左指针移动时，只需要检查它离开的字符与其右邻字符是否相同，若相同则 `dup_cnt` 减 1。  

整个过程每个字符最多被左指针和右指针各访问一次，时间是线性的 `O(n)`。  

**类比**：把窗口想象成一条可伸缩的绳子，绳子上只能容纳至多一次“相邻相同的结”。当我们往右拉绳子时，如果出现第二个结，就得把左边的绳子往右收紧，直到只剩下一个结为止。  

#### 代码（Python）  

```python
def longestSemiRepetitive_sliding(s: str) -> int:
    n = len(s)
    left = 0               # 窗口左边界
    dup_cnt = 0            # 窗口内相邻相同对的数量
    ans = 0                # 记录最大合法窗口长度

    # right 从 0 扫到 n-1，逐个把字符加入窗口
    for right in range(n):
        # 判断新加入的字符是否和左边的字符相同
        if right > 0 and s[right] == s[right - 1]:
            dup_cnt += 1    # 新的相邻相同对出现

        # 如果窗口中相同对已经超过 1，需要收缩左边界
        while dup_cnt > 1:
            # left 指针要离开的位置是 left，检查它和它右边的字符是否构成相同对
            if left + 1 <= right and s[left] == s[left + 1]:
                dup_cnt -= 1    # 这对相同对随左指针移出窗口
            left += 1          # 收缩窗口左边界

        # 此时窗口合法，更新答案
        ans = max(ans, right - left + 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 每个字符至多进入窗口一次、离开窗口一次。  
  - 与暴力 `O(n³)` 相比，**只需要遍历一次字符串**，即使 `n` 达到 10⁵ 也能轻松应付。  
- **空间复杂度**：`O(1)` —— 只用了几个整数指针和计数器，和输入规模无关。  

---  

## 心得  

- **核心技巧**：滑动窗口 + 计数相邻相同对的数量。  
- **适用的题型**：  
  1. “最多包含 K 个特定元素的最长子数组”——如 LeetCode 424 *Longest Repeating Character Replacement*（最多替换 K 次）  
  2. “子串中满足某种约束的最长长度”——如 LeetCode 3 *Longest Substring Without Repeating Characters*（字符不重复）  
  3. “窗口内满足某种计数条件”——如 LeetCode 1004 *Max Consecutive Ones III*（最多翻转 K 个 0）  
- **一句话总结**：**把“相邻相同对的数量”当作窗口的“血压”，只要不超过上限，就大胆扩张；一旦超标，就收紧左边界让血压恢复。**  

---  

## 反思  

- **第一反应**：看到“最多一个相邻相同对”，自然想到**枚举子串**检查，觉得最安全。  
- **最容易踩的坑**：  
  - **边界条件**：左指针移动时要确保 `left+1` 不越界，否则访问 `s[left+1]` 会出错。  
  - **计数更新**：忘记在左指针移动时把离开的相邻相同对计数减掉，导致 `dup_cnt` 永远不降，窗口永远收不回。  
- **下次遇到同类题**：第一步先问自己“窗口中需要维护什么统计量（次数、和、最大值）”，然后尝试**滑动窗口**，把统计量用变量实时更新，而不是每次重新遍历子串。这样往往能把指数级的暴力降到线性。