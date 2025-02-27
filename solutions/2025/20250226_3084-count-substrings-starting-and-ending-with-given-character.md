# #3084. 统计以给定字符开头和结尾的子串 / Count Substrings Starting and Ending with Given Character

> 难度：中等 · 标签：Math、String、Counting · [LeetCode 链接](https://leetcode.com/problems/count-substrings-starting-and-ending-with-given-character/)

---

## 题目（英文原版）

**Description**

You are given a string s and a character c. Return the total number of substrings of s that start and end with c.

**Examples**

**Example 1:**

```
Input: s = "abada", c = "a"
Output: 6
Explanation: Substrings starting and ending with "a" are: " a bada" , " aba da" , " abada " , "ab a da" , "ab ada " , "abad a " .
```

**Example 2:**

```
Input: s = "zzz", c = "z"
Output: 6
Explanation: There are a total of 6 substrings in s and all start and end with "z" .
```

**Constraints**

- 1 <= s.length <= 105
- s and c consist only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个字符 `c`，返回 `s` 中所有以 `c` 为起始字符且以 `c` 为结束字符的子串（substring）的总数。

**示例 1**  

**示例 2**  

**约束条件**  

- `1 <= s.length <= 10^5`  
- `s` 和 `c` 只包含小写英文字母  

**示例**

**示例 1**  
```
Input: s = "abada", c = "a"
Output: 6
Explanation: 以 "a" 开头并以 "a" 结尾的子串有： "a", "aba", "abada", "ab a da", "ab ada", "abad a"。
```

**示例 2**  
```
Input: s = "zzz", c = "z"
Output: 6
Explanation: s 中共有 6 个子串，且全部以 "z" 开头并以 "z" 结尾。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的子串都枚举出来，逐个检查它们的**首字符**和**尾字符**是否都是给定的字符 `c`。  
- **数据结构**：我们只需要用 Python 的字符串切片 `s[i:j+1]` 来得到子串。可以把字符串想象成一串珠子，枚举子串相当于把一段连续的珠子全部挑出来看。  
- **正确性**：因为我们把每一种起始位置 `i`（0 ≤ i < n）和每一种结束位置 `j`（i ≤ j < n）都遍历了一遍，只要子串的首尾都是 `c`，就一定会被计数，所以答案一定完整。  

#### 代码（Python）

```python
def count_substrings_bruteforce(s: str, c: str) -> int:
    n = len(s)
    ans = 0
    # 枚举所有起始位置 i
    for i in range(n):
        # 枚举所有结束位置 j，j 必须不小于 i
        for j in range(i, n):
            # 只要子串的首字符和尾字符都是 c，就计数
            if s[i] == c and s[j] == c:
                # 这里不必真正切片，只要检查两端字符即可
                ans += 1
    return ans

# 示例
print(count_substrings_bruteforce("abada", "a"))   # 6
print(count_substrings_bruteforce("zzz", "z"))    # 6
```

- 第 4 行的 `for i in range(n)` 相当于把珠子从左到右一个一个挑出来作为子串的左端。  
- 第 6 行的 `for j in range(i, n)` 把右端往右拖，形成所有可能的连续片段。  
- 第 8 行只检查两端字符，避免了不必要的字符串复制，仍然是 **暴力** 的思路。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  这里的 `n` 是字符串长度。因为外层循环 `n` 次，内层平均也要遍历约 `n/2` 次，整体是 **二次方** 的增长。可以把它想象成“每个人都要和每个人握手”，随着人数增多，握手次数会快速飙升。  
- **空间复杂度**：`O(1)`  
  只使用了常数级别的额外变量 `ans、i、j`，不随输入大小变化。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正影响答案的只有字符 `c` 出现的**位置**，而不是子串内部的具体内容。  
- **慢在哪里**：暴力解遍历了所有 `i, j` 对，即使大多数子串的首尾根本不可能都是 `c`，仍然要检查一遍，导致 `O(n²)`。  
- **关键观察**：如果我们知道字符串中字符 `c` 出现了 `m` 次，那么任意两个出现 `c` 的位置（包括同一个位置）都可以唯一确定一个满足条件的子串。  
  - 选择一个出现 `c` 的位置作为子串的左端，记为 `i`。  
  - 再选择一个（可以是同一个）出现 `c` 的位置作为右端，记为 `j`，且 `i ≤ j`。  
  - 这对 `(i, j)` 正好对应一个合法子串。  
- **组合计数**：从 `m` 个位置中选出 **有序** 的一对 `(i, j)`，且允许 `i = j`。这等价于“把 `m` 个球排成一列，任取左端和右端”。数学上，这个数目是  

\[
\frac{m \times (m + 1)}{2}
\]

  解释：先把 `m` 选成左端（有 `m` 种），右端可以是左端所在位置或其右边的任意一个，共有 `m - i` 种，求和得到等差数列求和公式，化简后就是上式。  
- **实现**：只需要一次遍历统计字符 `c` 出现的次数 `m`，随后直接算出答案。

#### 代码（Python）

```python
def count_substrings_optimal(s: str, c: str) -> int:
    """
    统计字符 c 在字符串 s 中出现的次数 m，
    再用组合公式 m * (m + 1) // 2 计算答案。
    """
    m = 0                     # 记录字符 c 出现的次数
    for ch in s:              # 一次遍历，时间 O(n)
        if ch == c:
            m += 1            # 找到一个 c，计数加一

    # 组合计数：从 m 个位置中任选左端和右端（可相同）
    return m * (m + 1) // 2   # 整除避免浮点数

# 示例
print(count_substrings_optimal("abada", "a"))   # 6
print(count_substrings_optimal("zzz", "z"))    # 6
```

- 第 5 行的 `for ch in s` 把字符串当成一串珠子，一颗颗检查是否是目标颜色 `c`。  
- 第 9 行的公式直接给出答案，`//` 是整数除法，确保返回的是整数。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只需一次线性遍历即可得到 `m`，与字符串长度成正比。相当于“一遍走完所有珠子”，没有多余的比较。  
- **空间复杂度**：`O(1)`  
  只用到计数变量 `m`，不随 `n` 增长。

---

## 心得

- **核心技巧**：**计数+组合数学**——先统计满足条件的“关键元素”（这里是字符 `c`），再用组合公式快速求出所有合法子串的数量。  
- **适用的题型**  
  1. “统计以某字符/数字开头或结尾的子数组/子串”  
  2. “给定数组，求所有元素相等的子数组个数”  
  3. “统计出现次数 ≥ k 的字符对数”  
- **解题钥匙**：把问题从“枚举子串”转化为“统计关键位置”，然后用 **组合计数** 一步算完。

---

## 反思

- **第一反应**：直接写两层循环枚举所有子串（暴力解），因为这是最直观的做法。  
- **最容易踩的坑**  
  - 忘记把 `i = j`（长度为 1 的子串）算进去，导致答案少 `m`。  
  - 对大输入使用暴力会超时，需要及时发现可以用计数代替枚举。  
- **下次遇到同类题**：第一步先问自己“**哪些位置是真正决定答案的**”。如果答案只和出现次数有关，就立刻转向 **计数 + 组合** 的思路，而不是继续暴力枚举。