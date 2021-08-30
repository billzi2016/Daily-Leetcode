# #1456. 给定长度子串中的元音字母最大数量 / Maximum Number of Vowels in a Substring of Given Length

> 难度：中等 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/)

---

## 题目（英文原版）

**Description**

Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.
Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.

**Examples**

**Example 1:**

```
Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowel letters.
```

**Example 2:**

```
Input: s = "aeiou", k = 2
Output: 2
Explanation: Any substring of length 2 contains 2 vowels.
```

**Example 3:**

```
Input: s = "leetcode", k = 3
Output: 2
Explanation: "lee", "eet" and "ode" contain 2 vowels.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.
- 1 <= k <= s.length

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`，返回 `s` 中所有长度为 `k` 的子串（substring）里元音字母（vowel letters）的最大出现次数。英语中的元音字母为 `'a'、'e'、'i'、'o'、'u'`。

## 示例

### 示例 1
**输入**  
``` 
s = "abciiidef", k = 3
```  
**输出**  
```
3
```  
**解释**  
子串 `"iii"` 包含 3 个元音字母。

### 示例 2
**输入**  
``` 
s = "aeiou", k = 2
```  
**输出**  
```
2
```  
**解释**  
任意长度为 2 的子串都包含 2 个元音字母。

### 示例 3
**输入**  
``` 
s = "leetcode", k = 3
```  
**输出**  
```
2
```  
**解释**  
子串 `"lee"`、`"eet"` 和 `"ode"` 含有 2 个元音字母。

## 约束条件
- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。
- `1 <= k <= s.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把字符串 `s` 的每一个长度为 `k` 的子串都枚举出来，逐个统计子串里有多少元音字母（`a e i o u`），记录下最大的那个计数。

- **使用的数据结构**：  
  - **字符串**本身就像一本书，取其中连续的 `k` 页就是子串。  
  - **计数器**（一个整数）用来记录当前子串里出现了多少次元音，就像在数一本字典里某个单词出现的次数。  

- **为什么正确**：  
  我们遍历了所有可能的长度为 `k` 的子串，真正的答案一定是其中的某一个子串的元音数。只要把每个子串的元音数算出来并取最大值，就一定能得到正确答案。

- **时间/空间复杂度**：  
  - **时间**：我们有 `len(s) - k + 1` 个子串需要检查。对每个子串我们要遍历 `k` 个字符去计数。于是总的操作次数大约是 `(len(s) - k + 1) * k`，在最坏情况下接近 `n * k`（其中 `n = len(s)`），这在大 O 记号里写成 **O(n·k)**。如果 `k` 接近 `n`，时间复杂度就会变成 **O(n²)**，也就是“平方级别”，随着输入长度的增长，耗时会非常快。  
  - **空间**：只用了常数个变量（计数器、最大值等），所以是 **O(1)**，即“常数级别”的额外空间。

#### 代码（Python）

```python
def maxVowels_bruteforce(s: str, k: int) -> int:
    vowels = set('aeiou')               # 元音集合，像字典查词一样 O(1) 判断
    max_cnt = 0                         # 记录出现的最大元音数

    # 枚举所有长度为 k 的子串，左端点从 0 到 len(s)-k
    for left in range(len(s) - k + 1):
        cnt = 0                         # 当前子串的元音计数
        # 统计子串 s[left:left+k] 中的元音数量
        for i in range(left, left + k):
            if s[i] in vowels:          # 判断字符是否是元音
                cnt += 1
        max_cnt = max(max_cnt, cnt)    # 更新全局最大值

    return max_cnt
```

#### 复杂度

- **时间复杂度**：**O(n·k)**（最坏情况约等于 O(n²)），因为对每个起点都要遍历 `k` 个字符。  
- **空间复杂度**：**O(1)**，只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈在于**每次都重新遍历整个窗口**，导致大量重复工作。实际上，当我们把窗口从左向右滑动一格时，窗口里只会有 **一个字符离开**、**一个字符进入**，其它 `k‑1` 个字符保持不变。

**滑动窗口**（Sliding Window）技巧正是用来避免这种重复计数的：

1. **初始化**：先把前 `k` 个字符的元音数算出来，记作 `cnt`，同时把 `max_cnt` 设为 `cnt`。这一步相当于把窗口固定在字符串的最左边。  
2. **移动窗口**：从第 `k` 个字符开始向右遍历（下标 `i`），每次做两件事：  
   - **离开**：窗口左边界的字符 `s[i - k]` 移出，如果它是元音则把 `cnt` 减 1。  
   - **进入**：新加入的字符 `s[i]` 进入窗口，如果它是元音则把 `cnt` 加 1。  
   这样 `cnt` 始终保持为当前窗口（长度恰好是 `k`）里元音的数量。  
3. **更新答案**：每次移动后把 `max_cnt` 和 `cnt` 做比较，保留更大的值。  
4. **返回**：遍历结束后 `max_cnt` 就是所有窗口中元音数的最大值。

**类比**：想象你在看一条长跑道上的跑步者，每次只关心长度为 `k` 的区间里有多少人戴着红帽子。你不需要每次都重新数整段人，只要记住上一段的红帽子数，离开的人如果戴帽子就减 1，进来的人如果戴帽子就加 1，整个过程只需要一次遍历。

#### 代码（Python）

```python
def maxVowels_sliding_window(s: str, k: int) -> int:
    vowels = set('aeiou')               # 元音集合，查找 O(1)
    cnt = 0                             # 当前窗口的元音数
    max_cnt = 0                         # 记录出现的最大元音数

    # 1️⃣ 先统计前 k 个字符的元音数，形成初始窗口
    for i in range(k):
        if s[i] in vowels:
            cnt += 1
    max_cnt = cnt                        # 初始化答案

    # 2️⃣ 从第 k 个字符开始，逐个滑动窗口
    for i in range(k, len(s)):
        # a) 移除窗口最左侧的字符 s[i - k]
        if s[i - k] in vowels:
            cnt -= 1                     # 离开的字符是元音，计数减 1
        # b) 加入窗口最右侧的新字符 s[i]
        if s[i] in vowels:
            cnt += 1                     # 新进来的字符是元音，计数加 1
        # c) 更新最大值
        max_cnt = max(max_cnt, cnt)

    return max_cnt
```

#### 复杂度

- **时间复杂度**：**O(n)**，只遍历字符串一次（`n = len(s)`），每个字符进入或离开窗口时只做 O(1) 的检查和计数。相比暴力的 O(n·k) 大幅提升。  
- **空间复杂度**：**O(1)**，只用了几个整数和一个常数大小的集合（元音集合），不随输入规模增长。

---

## 心得

- **核心技巧**：滑动窗口（Sliding Window）——在固定长度的窗口里维护一个增量信息（这里是元音计数），实现线性时间解法。  
- **适用的题型**：  
  1. “找长度为 k 的子数组/子串的最大/最小和” （如 LeetCode 209. Minimum Size Subarray Sum 的变形）。  
  2. “包含多少种不同字符的最长子串” （如 LeetCode 3. Longest Substring Without Repeating Characters）。  
  3. “子数组/子串中满足某种条件的最大长度” （如 LeetCode 1004. Max Consecutive Ones III）。  
- **一句话总结解题钥匙**：**“窗口只动一步，增量更新，避免全局重新计数”。**

---

## 反思

- **第一反应**：看到“子串长度固定为 k”，立刻想到枚举所有子串并逐个统计，这是最自然的暴力思路。  
- **最容易踩的坑**：  
  - **边界条件**：`k` 可能等于字符串长度，此时只能返回整个字符串的元音数，滑动窗口的循环要防止越界。  
  - **字符判断**：忘记把元音集合写成 `set('aeiou')`，用列表或字符串每次 `in` 仍然是 O(1) 但集合更直观且语义明确。  
  - **忘记初始化答案**：如果只在滑动过程中更新 `max_cnt`，而没有在初始窗口时赋值，可能会错过第一窗口的结果。  
- **下次遇到同类题**：**第一步先思考“窗口里有什么信息需要维护”，再决定是否可以用滑动窗口做增量更新**。如果能够把每次移动的代价降到 O(1)，往往就能把暴力的 O(n·k) 降到 O(n)。