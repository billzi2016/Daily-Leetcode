# #1876. 长度为三且字符互不相同的子串 / Substrings of Size Three with Distinct Characters

> 难度：简单 · 标签：Hash Table、String、Sliding Window、Counting · [LeetCode 链接](https://leetcode.com/problems/substrings-of-size-three-with-distinct-characters/)

---

## 题目（英文原版）

**Description**

A string is good if there are no repeated characters.
Given a string s​​​​​, return the number of good substrings of length three in s​​​​​​.
Note that if there are multiple occurrences of the same substring, every occurrence should be counted.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: s = "xyzzaz"
Output: 1
Explanation: There are 4 substrings of size 3: "xyz", "yzz", "zza", and "zaz". 
The only good substring of length 3 is "xyz".
```

**Example 2:**

```
Input: s = "aababcabc"
Output: 4
Explanation: There are 7 substrings of size 3: "aab", "aba", "bab", "abc", "bca", "cab", and "abc".
The good substrings are "abc", "bca", "cab", and "abc".
```

**Constraints**

- 1 <= s.length <= 100
- s​​​​​​ consists of lowercase English letters.

---

## 题目（中文翻译）

如果一个字符串中不存在重复字符，则称该字符串为 好字符串（good string）。  
给定一个字符串 `s`，返回 `s` 中长度为 3 的 好子串（good substring）的数量。  
注意，即使相同的子串出现多次，也要分别计数。  

子串（substring）是字符串中字符的连续序列。

**示例 1**

```text
Input: s = "xyzzaz"
Output: 1
解释：共有 4 个长度为 3 的子串："xyz"、"yzz"、"zza"、"zaz"。唯一满足条件的好子串是 "xyz"。
```

**示例 2**

```text
Input: s = "aababcabc"
Output: 4
解释：共有 7 个长度为 3 的子串："aab"、"aba"、"bab"、"abc"、"bca"、"cab"、"abc"。满足条件的好子串为 "abc"、"bca"、"cab"、以及再次出现的 "abc"。
```

**约束条件**

- `1 <= s.length <= 100`
- `s` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把字符串里所有长度为 3 的子串全部枚举出来，逐个检查这三个字符是否全不相同。  

- **数据结构**：我们只需要遍历字符串，用 **切片** `s[i:i+3]` 取出子串。  
- **判重**：判断三个字符是否互不相同，可以把它们放进 **集合（set）**，集合会自动去重。如果集合的大小是 3，说明三个字符全不相同。这里集合就像一本字典，放进去的每个字符只会保留一份，最后看有几页（元素）就能知道是否有重复。  

为什么这个方法一定对？因为题目要求的“好子串”正好是长度 3 且字符互不相同的子串，而我们把所有可能的长度 3 子串都检查了一遍，符合条件的自然就被统计进来了。  

**时间/空间复杂度**  
- 时间复杂度：外层遍历字符串一次，长度为 n （最多 100），每次检查集合大小是 **O(1)**（因为集合里最多只有 3 个元素）。整体是 **O(n)**。  
- 空间复杂度：每次只创建一个最多装 3 个字符的集合，常数级别的空间，记作 **O(1)**。  

> 大白话解释：  
> - **O(n)** 就是说，处理的工作量跟字符串长度成正比，长度长一点，就多检查几次。  
> - **O(1)** 表示不管字符串多长，我们用的额外内存几乎不变，始终很小。  

#### 代码（Python）

```python
def countGoodSubstrings(s: str) -> int:
    n = len(s)
    ans = 0                     # 记录满足条件的子串个数

    # 枚举所有长度为 3 的子串，左端点 i 从 0 到 n-3
    for i in range(n - 2):
        sub = s[i:i + 3]        # 直接切片得到子串，例如 "xyz"
        # 把子串的字符放进集合，集合会自动去重
        if len(set(sub)) == 3:  # 如果集合大小是 3，说明三个字符全不相同
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 只遍历一次字符串，n 是字符串长度。  
- **空间复杂度**：**O(1)** — 只用了常数大小的集合（最多 3 个字符），不随 n 增长。  

---  

### 2. 最优解  

#### 思路  

虽然上面的暴力解已经是 **O(n)**，在本题的约束（n ≤ 100）下已经足够快，但我们仍然可以从“滑动窗口”的角度来思考，使代码更具通用性，尤其在以后遇到更大规模的类似题目时，滑动窗口的思想会让我们自然想到 **只看一次** 而不是每次都重新创建集合。  

**慢在哪里？**  
- 暴力解在每次检查子串时都会重新创建一个集合，即使相邻的两个子串只差一个字符，这一步仍然重复了很多工作。  

**优化思路**  
- 采用 **固定长度为 3 的滑动窗口**。窗口左边界从 0 开始，右边界一直保持在左边界+2。每次窗口向右移动一步，只需要比较新加入的字符和窗口中已有的两个字符是否相同。  
- 具体实现：直接检查 `s[i]`, `s[i+1]`, `s[i+2]` 三个字符是否两两不同。因为窗口大小固定为 3，直接比较三个字符的关系就可以了，不需要额外的数据结构。  

**核心技巧**：**双指针 / 滑动窗口**。把一段连续的子串想象成一块可以在字符串上“滑动”的小木板，每次只移动一步，检查窗口内的内容是否符合要求。  

**类比**：想象你在走走廊，每次只能看到前面三盏灯的颜色，只要这三盏灯颜色全不相同，你就记一个分数。你不需要每次都重新数灯的颜色，只要把眼睛顺着走廊往前挪一格，重新观察这三盏灯就行了。  

#### 代码（Python）

```python
def countGoodSubstrings(s: str) -> int:
    n = len(s)
    ans = 0

    # i 表示窗口左端点，窗口长度固定为 3，右端点为 i+2
    for i in range(n - 2):
        a, b, c = s[i], s[i + 1], s[i + 2]   # 直接取出三个字符
        # 判断三两两是否不同：a!=b 且 a!=c 且 b!=c
        if a != b and a != c and b != c:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 仍然只遍历一次字符串，每次只做常数次比较（3 次不等式判断）。相比暴力解省掉了集合的创建与哈希操作。  
- **空间复杂度**：**O(1)** — 只用了几个临时变量 `a, b, c`，不随 n 增长。  

> 与暴力解对比：时间上没有数量级的提升（都是 O(n)），但常数因子更小，代码更简洁，且思路更容易推广到更长窗口或更复杂的“窗口内统计”问题。  

---  

## 心得  

- **核心技巧**：滑动窗口（固定长度） + 两两比较字符是否相同。  
- **适用的题型**：  
  1. “长度为 k 的子串中字符全部唯一” 类问题（如 LeetCode 1100 系列）。  
  2. “窗口内满足某种计数条件” 的子数组/子串计数（如 “最长无重复字符子串”）。  
  3. “固定窗口大小的模式匹配” （比如判断每三个字符是否形成某种合法组合）。  
- **一句话总结解题钥匙**：**把“检查子串是否好”转化为“窗口内的元素两两不等”，用最少的比较一次搞定**。  

---  

## 反思  

- **第一反应**：直接想到枚举所有长度为 3 的子串，用集合去重。  
- **最容易踩的坑**：  
  - 忘记字符串长度可能小于 3，需要提前返回 0。  
  - 在使用集合时误把整个子串当作集合元素，导致判断错误。  
  - 处理边界时 `range(len(s)-2)` 必须写对，防止索引越界。  
- **下次类似题的第一步**：先确定窗口大小（本题是 3），再思考窗口内部的“好”条件能否用 **常数次比较** 或 **计数数组** 直接判断，避免不必要的数据结构。