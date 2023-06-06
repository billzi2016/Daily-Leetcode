# #2272. 子串的最大方差 / Substring With Largest Variance

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/substring-with-largest-variance/)

---

## 题目（英文原版）

**Description**

The variance of a string is defined as the largest difference between the number of occurrences of any 2 characters present in the string. Note the two characters may or may not be the same.
Given a string s consisting of lowercase English letters only, return the largest variance possible among all substrings of s.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "aababbb"
Output: 3
Explanation:
All possible variances along with their respective substrings are listed below:
- Variance 0 for substrings "a", "aa", "ab", "abab", "aababb", "ba", "b", "bb", and "bbb".
- Variance 1 for substrings "aab", "aba", "abb", "aabab", "ababb", "aababbb", and "bab".
- Variance 2 for substrings "aaba", "ababbb", "abbb", and "babb".
- Variance 3 for substring "babbb".
Since the largest possible variance is 3, we return it.
```

**Example 2:**

```
Input: s = "abcde"
Output: 0
Explanation:
No letter occurs more than once in s, so the variance of every substring is 0.
```

**Constraints**

- 1 <= s.length <= 104
- s consists of lowercase English letters.

---

## 题目（中文翻译）

字符串的方差定义为字符串中任意两字符出现次数的最大差值。注意，这两字符可以相同，也可以不同。  
给定仅由小写英文字母组成的字符串 `s`，返回 `s` 的所有子串（substring）中可能的最大方差。  
子串（substring）是字符串中连续的字符序列。

**示例 1**  
输入: `s = "aababbb"`  
输出: `3`  
解释:  
所有可能的方差及其对应的子串列举如下:  
- 方差 0 的子串有 `"a"`, `"aa"`, `"ab"`, `"abab"`, `"aababb"`, `"ba"`, `"b"`, `"bb"` 和 `"bbb"`。  
- 方差 1 的子串有 `"aab"`, `"aba"`, `"abb"`, `"aabab"`, `"ababb"`, `"aababbb"` 和 `"bab"`。  
- 方差 2 的子串有 `"aaba"`, `"ababbb"`, `"abbb"` 和 `"babb"`。  
- 方差 3 的子串为 `"ba"` …（已截断）

**示例 2**  
输入: `s = "abcde"`  
输出: `0`  
解释:  
`s` 中没有字母出现超过一次，因此每个子串的方差均为 `0`。

**约束条件**  
- `1 <= s.length <= 10^4`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是枚举 **所有子串**，然后在每个子串里统计出现的字符次数，求出最大的两种字符出现次数的差值（即方差），最后取所有子串的最大值。

- **枚举子串**：可以用两个循环 `i`、`j`（`i` 为子串左端，`j` 为右端），每次取 `s[i:j+1]`。
- **统计字符**：因为只涉及小写英文字母（共 26 个），可以用长度为 26 的数组 `cnt` 记录当前子串里每个字符出现的次数。
- **计算方差**：遍历 `cnt` 找出最大值 `max_cnt` 与最小的非零值 `min_cnt`（如果只有一种字符，则方差为 0），`max_cnt - min_cnt` 就是该子串的方差。

> **生活化类比**：把 `cnt` 想象成一本字典，`key` 是字母，`value` 是这本字典里对应字母出现的页码（次数）。我们把子串看成一本小册子，遍历它时不断在字典里加页码，最后找出页码最高的字母和页码最少（但>0）的字母，两者差值就是这本小册子的“字数差”。

**为什么正确**：我们对每一个可能的子串都完整地计算了它的方差，最大值自然就是答案。

#### 代码（Python）

```python
def largestVariance_bruteforce(s: str) -> int:
    n = len(s)
    ans = 0                     # 最终答案
    for i in range(n):          # 左端点
        cnt = [0] * 26          # 记录当前子串的字符出现次数
        for j in range(i, n):   # 右端点，逐步扩展子串
            idx = ord(s[j]) - ord('a')
            cnt[idx] += 1       # 把新加入的字符计数

            # 计算当前子串的方差
            max_cnt = 0
            min_cnt = float('inf')
            for c in cnt:
                if c > 0:               # 只看出现过的字符
                    max_cnt = max(max_cnt, c)
                    min_cnt = min(min_cnt, c)
            if min_cnt == float('inf'):   # 只有一种字符
                cur_var = 0
            else:
                cur_var = max_cnt - min_cnt
            ans = max(ans, cur_var)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n^2 * 26)`  
  两层循环枚举子串是 `O(n^2)`，每次统计方差要遍历 26 个字母，所以整体是 `O(n^2)` 级别。  
  > 大白话：如果字符串长度是 1000，最坏情况要检查大约 1 000 000（千乘千）个子串，每个子串只看 26 次，仍然会很慢。

- **空间复杂度**：`O(26) = O(1)`  
  只用了常数大小的计数数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有子串**，这一步是 `O(n^2)`。我们需要把 “子串” 这层循环去掉，只在 **一次遍历**（或少量遍历）中得到答案。

观察题目提示：

> 如果字符串里只有 **两种不同字符**，把一种记作 `+1`，另一种记作 `-1`，那么子串的方差就等价于 **这段 +1/-1 序列的最大子段和**（Kadane 算法）。

**一步步推导**：

1. **固定字符对**  
   - 设字符 `a`、`b` 为我们关心的两种字符。  
   - 把原字符串映射为一个仅包含 `+1`（对应 `a`）和 `-1`（对应 `b`）的序列，其他字符直接忽略（当作 0，不影响和）。  
   - 在这个序列上，求最大子段和即得到「以 `a` 为主、`b` 为辅」的最大方差。

2. **Kadane 需要两点额外处理**  
   - 方差要求 **两种字符都出现**，单纯的 Kadane 可能会得到全是 `+1`（只有 `a`）的子段，这时方差其实是 0，需要排除。  
   - 当子段里 `b` 的出现次数比 `a` 多时（累计和变负），我们可以把当前子段丢掉，重新开始。但有一种特殊情况：即使累计和为负，只要子段里已经出现过 `b`（即 `-1`），我们仍然可以把 `b` 当成“起始字符”，继续向后寻找更大的和。这相当于在 Kadane 中加入 **“允许一次负数起始”** 的技巧。

3. **遍历所有字符对**  
   - 英文字母只有 26 种，所有两两组合有 `26 * 25 = 650` 种（顺序不同算两种，因为 `a` 为正、`b` 为负 与 `b` 为正、`a` 为负 结果不一样）。  
   - 对每一对字符执行上述 Kadane（两次：一次正向遍历，一次逆向遍历），取最大值。  
   - 逆向遍历是为了捕获 “`b` 在前、`a` 在后” 的情况，因为 Kadane 本身只能保证子段左端是正数（`a`），但实际最优子段可能是先出现很多 `b` 再出现 `a`。

**核心算法**：对每一对字符使用 **改进的 Kadane（最大子段和）**，时间 `O(n)`；共 `O(26^2 * n)`。

> **类比**：把字符 `a` 当成「收入」(+1)，字符 `b` 当成「支出」(-1)。我们想在一段时间里（子串）找到 **净收入最高** 的区间，但前提是这段时间里至少有一次支出（否则净收入最高的区间只是全收入，没有支出，不算有效）。这正是 Kadane 加上「必须出现支出」的限制。

#### 代码（Python）

```python
import string
from typing import List

def largestVariance(s: str) -> int:
    # 统计所有出现过的字符，后面只遍历这些字符的组合即可稍微剪枝
    present = set(s)
    letters = list(present)               # 最多 26 个
    ans = 0

    # 对每一对不同字符 (a, b) 进行两次 Kadane（正向、逆向）
    for a in letters:
        for b in letters:
            if a == b:
                continue

            # ---------- 正向遍历 ----------
            # cur 表示当前子段的累计和，has_b 用来判断子段里是否出现过字符 b
            cur = 0
            has_b = False
            for ch in s:
                if ch == a:
                    cur += 1                # +1 表示收入
                elif ch == b:
                    cur -= 1                # -1 表示支出
                    has_b = True
                else:
                    continue                # 其他字符直接跳过

                # 只在子段已经出现过 b 时才更新答案
                if has_b:
                    ans = max(ans, cur)

                # 如果累计和变成负数，说明前面的子段已经“亏损”，重新开始
                # 但重新开始时必须把 has_b 复位，因为新子段里还没有出现 b
                if cur < 0:
                    cur = 0
                    has_b = False

            # ---------- 逆向遍历 ----------
            # 同理，只是把 a、b 的角色对调（等价于把字符串反向遍历）
            cur = 0
            has_b = False
            for ch in reversed(s):
                if ch == a:
                    cur += 1
                elif ch == b:
                    cur -= 1
                    has_b = True
                else:
                    continue

                if has_b:
                    ans = max(ans, cur)
                if cur < 0:
                    cur = 0
                    has_b = False

    return ans
```

> **代码要点注释**  
- `present` 用来只遍历出现过的字符，稍微提速。  
- `has_b` 标记当前子段是否已经出现过字符 `b`（支出），只有出现过才算合法方差。  
- 当 `cur < 0` 时，我们把子段「清空」重新开始，这正是 Kadane 的核心思想。  
- 逆向遍历是必须的，否则会漏掉 `b` 在左、`a` 在右的最佳子段。

#### 复杂度

- **时间复杂度**：`O(26^2 * n) ≈ O(n)`（常数 26²=676），因为 `n ≤ 10^4`，最多约 `6.8 * 10^6` 次简单运算，完全可以在一秒内跑完。  
  > 与暴力解相比，从 `O(n^2)` 降到了线性级别，提升非常明显。

- **空间复杂度**：`O(1)`（只使用了几个整型变量），不随 `n` 增长。

---

## 心得

- **核心技巧**：把「两种字符的出现次数差」转化为「+1 / -1 序列的最大子段和」，再用 **Kadane（最大子段和）** 求解，并加入「必须出现负数」的约束。
- **该技巧适用的题型**  
  1. **最大子数组差值**：如 “Maximum Subarray Sum with One Deletion”。  
  2. **子串字符平衡**：如 “Find the longest substring containing at most two distinct characters”。  
  3. **字符映射为权值求最值**：如 “Maximum Subarray Sum after mapping characters to numbers”。
- **一句话总结解题钥匙**：**把两字符计数差映射为 +1 / -1 序列，利用改进的 Kadane 求最大子段和**。

---

## 反思

- **第一反应**：直接枚举所有子串并统计字符频次，想当然地认为时间可以接受。  
- **最容易踩的坑**  
  - 忽略 **“两种字符都必须出现”** 的限制，导致答案可能为正却实际上非法。  
  - 只做一次正向 Kadane，遗漏了 **“b 在左、a 在右”** 的情况，需要逆向遍历或在 Kadane 中加入额外的“首字符为负”处理。  
  - 边界情况：字符串全部相同字符时答案应为 0，代码要确保不会因 `has_b` 永远为 `False` 而产生错误的负数答案。
- **下次类似题的第一步**：先 **把问题抽象为数值序列的最值问题**（如最大子段和、前缀和），再决定是否需要枚举字符/状态的组合。这样可以快速定位到 Kadane、前缀和或单调栈等工具，从而避免暴力枚举。