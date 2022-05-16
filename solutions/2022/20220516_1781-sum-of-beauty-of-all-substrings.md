# #1781. 所有子串美丽值之和 / Sum of Beauty of All Substrings

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/sum-of-beauty-of-all-substrings/)

---

## 题目（英文原版）

**Description**

The beauty of a string is the difference in frequencies between the most frequent and least frequent characters.
Given a string s, return the sum of beauty of all of its substrings.

**Examples**

**Example 1:**

```
Input: s = "aabcb"
Output: 5
Explanation: The substrings with non-zero beauty are ["aab","aabc","aabcb","abcb","bcb"], each with beauty equal to 1.
```

**Example 2:**

```
Input: s = "aabcbaa"
Output: 17
```

**Constraints**

- 1 <= s.length <= 500
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

一个字符串的**美丽值（beauty）**定义为出现次数最多的字符的频率与出现次数最少的字符的频率之差。  
给定字符串 `s`，返回其所有子串（substring）的美丽值之和。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1**  
Input: s = "aabcb"  
Output: 5  
Explanation: 美丽值非零的子串有 ["aab","aabc","aabcb","abcb","bcb"]，它们的美丽值均为 1。

**示例 2**  
Input: s = "aabcbaa"  
Output: 17  

**约束条件**  
- 1 ≤ s.length ≤ 500  
- s 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  
1. **枚举所有子串**。长度为 `n` 的字符串一共有 `n·(n+1)/2` 个子串，最外层两层循环（左边界 `i`，右边界 `j`）即可遍历。  
2. **统计子串里每个字母出现的次数**。最朴素的做法是把子串从头到尾走一遍，用一个长度为 26 的数组 `cnt`（下标 0 对应 `'a'`，1 对应 `'b'` ……）记录每个字符的出现次数。  
3. **求出子串的 beauty**：  
   - 找到 `cnt` 中的最大值 `mx`（出现次数最多的字符）。  
   - 找到 `cnt` 中的最小非零值 `mn`（出现次数最少且>0的字符）。  
   - beauty = `mx - mn`。  
4. 把所有子串的 beauty 累加得到答案。  

> **类比**：把 `cnt` 想成一本“字典”，字母是“单词”，出现次数是“页码”。遍历子串时就像在这本字典里查每个单词出现了多少页，最后比较最高页码和最低页码的差值。  

**为什么正确**：我们对每一个可能的子串都严格按照题目定义计算了 beauty，所有子串的 beauty 求和自然就是题目要求的答案。  

**复杂度分析（大白话）**  
- **时间**：外层两层循环产生 `O(n²)` 个子串。对每个子串我们又要再走一遍子串本身，最坏情况子串长度是 `n`，于是总共是 `O(n³)`。可以把 `n³` 想成“把 500×500×500 次的小操作都做一遍”，在最坏情况下会比较慢。  
- **空间**：只用了一个长度为 26 的计数数组，常数级别的空间 `O(1)`（不随 `n` 增长）。  

#### 代码（Python）  

```python
def beauty_of_substrings_bruteforce(s: str) -> int:
    n = len(s)
    ans = 0

    # i 为子串左边界，j 为右边界（包括两端）
    for i in range(n):
        for j in range(i, n):
            cnt = [0] * 26                 # 统计当前子串的字符出现次数
            # 把子串 s[i:j+1] 逐字符计数
            for k in range(i, j + 1):
                idx = ord(s[k]) - ord('a')
                cnt[idx] += 1

            # 计算该子串的 beauty
            mx = max(cnt)                  # 最多出现的次数
            # 只在出现过的字符中找最少次数
            mn = min(c for c in cnt if c > 0)
            ans += mx - mn

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 需要三层循环，最外层两层枚举子串，最内层遍历子串本身。  
- **空间复杂度**：`O(1)` —— 只用了固定大小的计数数组（长度 26），不随输入规模变化。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要重新遍历子串来统计字符频率**。如果我们能够在 **O(1)** 时间内得到任意子串的字符计数，就可以把整体时间降到 `O(n²)`（只保留枚举子串的两层循环）。  

实现这个目标的常用技巧是 **前缀和（prefix sum）**，这里把它应用到字符计数上。  

**前缀计数表的构造**  
- 定义 `pre[i][c]` 为前 `i` 个字符（下标 `[0, i)`）中字符 `c` 出现的次数。  
- `pre[0]` 全部为 0。  
- 对于每个位置 `i`（0‑based），把 `pre[i]` 复制一份得到 `pre[i+1]`，然后把 `s[i]` 对应的计数加 1。  

这样，**任意子串 `[l, r]`（左闭右闭）的字符计数** 可以用两次前缀计数相减得到：  

```
cnt[c] = pre[r+1][c] - pre[l][c]
```

因为我们只需要 **最大频率** 与 **最小非零频率**，不必把 26 个字符的计数全部列出来再遍历，只要在每次求子串时遍历一次 26 长度的数组即可。  

**实现细节**  
1. 先一次遍历构造 `pre`（大小 `(n+1) × 26`），时间 `O(n·26)`。  
2. 双层循环枚举左边界 `l` 与右边界 `r`（`l ≤ r`），对每个子串：  
   - 用 `pre` 直接得到 26 个字符的出现次数（`cnt[c] = pre[r+1][c] - pre[l][c]`）。  
   - 在这 26 个数里找最大值 `mx` 与最小正值 `mn`。  
   - 累加 `mx - mn`（若所有字符出现次数相同或只有一种字符，则 `mx - mn = 0`，可以直接跳过）。  
3. 所有子串遍历完后返回累计和。  

**为什么是最优**：  
- 我们仍然必须检查所有 `O(n²)` 个子串（因为题目要求把每个子串的 beauty 加起来），所以时间下界是 `Ω(n²)`。  
- 通过前缀计数，我们把每个子串的统计时间压到常数（遍历 26 个字母），达到了 `O(n²)`，已经无法再进一步提升。  

**类比**：  
想象你在一本“字典”里记录每一页前面所有字母出现的累计次数（这就是前缀表）。想知道第 3‑5 页（子串）的字母分布，只需要把第 5 页的累计数减去第 2 页的累计数，瞬间得到答案。  

#### 代码（Python）  

```python
def beauty_of_substrings(s: str) -> int:
    n = len(s)
    # 1. 构造前缀计数表，pre[i][c] 表示前 i 个字符中字符 c 的出现次数
    pre = [[0] * 26 for _ in range(n + 1)]
    for i, ch in enumerate(s):
        # 复制上一行的计数
        for c in range(26):
            pre[i + 1][c] = pre[i][c]
        # 当前字符出现次数加一
        idx = ord(ch) - ord('a')
        pre[i + 1][idx] += 1

    ans = 0
    # 2. 枚举所有子串
    for l in range(n):          # 左边界
        for r in range(l, n):   # 右边界
            mx = 0               # 当前子串出现次数的最大值
            mn = float('inf')    # 当前子串出现次数的最小非零值

            # 3. 通过前缀表快速得到 26 个字符的出现次数
            for c in range(26):
                cnt = pre[r + 1][c] - pre[l][c]   # 子串 [l, r] 中字符 c 的次数
                if cnt > 0:                      # 只关心出现过的字符
                    if cnt > mx:
                        mx = cnt
                    if cnt < mn:
                        mn = cnt

            # 如果子串里至少有两种字符，才会产生非零 beauty
            if mx > mn:
                ans += mx - mn

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²·Σ)`，其中 Σ = 26 为字母表大小。实际表现为 `≈ 26·n²`，对 `n ≤ 500` 完全足够。相较于暴力的 `O(n³)`，我们把最耗时的那一层循环（遍历子串本身）省掉了，只保留固定长度 26 的遍历。  
- **空间复杂度**：`O(n·Σ)`，即前缀表占用 `(n+1) × 26` 的整数空间。`n` 最多 500，所需内存约几千个整数，仍是常数级别的可接受范围。  

---

## 心得  

- **核心技巧**：**前缀计数 + 枚举子串**。利用前缀和把子串的字符频率查询从线性降到常数。  
- **适用的题型**：  
  1. “子串中出现次数的最大/最小差值”类（如本题）。  
  2. “统计子串中满足某种频率条件的子串数量” （例如 LeetCode 1358 `Number of Substrings Containing All Three Characters`）。  
  3. “子串的字符种类数 / 出现次数是否相同” 类（如 LeetCode 1371 `Find the Longest Substring Containing Vowels in Sorted Order`）。  
- **一句话总结**：**把“遍历子串再遍历字符”变成“遍历子串一次、字符固定 26 次”，前缀和是关键**。  

---

## 反思  

- **第一反应**：直接写三层循环枚举子串并统计字符，代码能跑通但会超时。  
- **最容易踩的坑**：  
  - **最小频率的定义**：只能在出现过的字符中取最小值，不能把 `0` 计进去，否则会把没有出现的字母误当成最少出现的字符。  
  - **边界条件**：子串只有一种字符时 beauty 为 0，需要判断 `mx > mn` 再累加。  
  - **前缀表的复制**：构造时必须复制上一行的全部 26 项，否则后面的减法会出错。  
- **下次类似题目第一步**：**先想“能否用前缀/累计信息把子串属性 O(1) 取出”，如果可以，就把枚举子串的复杂度降到 `O(n²)`**。这样往往就能从暴力卡住直接跳到可接受的最优解。