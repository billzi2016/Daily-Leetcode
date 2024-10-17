# #2904. 最短且字典序最小的美丽子串 / Shortest and Lexicographically Smallest Beautiful String

> 难度：中等 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/shortest-and-lexicographically-smallest-beautiful-string/)

---

## 题目（英文原版）

**Description**

You are given a binary string s and a positive integer k.
A substring of s is beautiful if the number of 1's in it is exactly k.
Let len be the length of the shortest beautiful substring.
Return the lexicographically smallest beautiful substring of string s with length equal to len. If s doesn't contain a beautiful substring, return an empty string.
A string a is lexicographically larger than a string b (of the same length) if in the first position where a and b differ, a has a character strictly larger than the corresponding character in b.

**Examples**

**Example 1:**

```
Input: s = "100011001", k = 3
Output: "11001"
Explanation: There are 7 beautiful substrings in this example:
1. The substring "100011001".
2. The substring "100011001".
3. The substring "100011001".
4. The substring "100011001".
5. The substring "100011001".
6. The substring "100011001".
7. The substring "100011001".
The length of the shortest beautiful substring is 5.
The lexicographically smallest beautiful substring with length 5 is the substring "11001".
```

**Example 2:**

```
Input: s = "1011", k = 2
Output: "11"
Explanation: There are 3 beautiful substrings in this example:
1. The substring "1011".
2. The substring "1011".
3. The substring "1011".
The length of the shortest beautiful substring is 2.
The lexicographically smallest beautiful substring with length 2 is the substring "11".
```

**Example 3:**

```
Input: s = "000", k = 1
Output: ""
Explanation: There are no beautiful substrings in this example.
```

**Constraints**

- 1 <= s.length <= 100
- 1 <= k <= s.length

---

## 题目（中文翻译）

给定一个二进制字符串 `s` 和一个正整数 `k`。  
如果一个子串（substring）中恰好包含 `k` 个 `1`，则称该子串为 **美丽子串**（beautiful substring）。  
设 `len` 为最短美丽子串的长度。返回 `s` 中长度等于 `len` 的字典序最小的美丽子串。如果 `s` 不包含任何美丽子串，返回空字符串。

**字典序比较**：若两个等长字符串在首次不同的位置上，字符 `a` 的字符严格大于字符 `b` 的字符，则字符串 `a` 的字典序大于字符串 `b`。

---

### 示例

#### 示例 1
```text
Input: s = "100011001", k = 3
Output: "11001"
Explanation: 在此例中共有 7 个美丽子串：
1. 子串 "100011001"
2. 子串 "100011001"
3. 子串 "100011001"
4. 子串 "100011001"
5. 子串 "100011001"
6. 子串 "100011001"
7. 子串 "100011001"
最短美丽子串的长度为 5。
在所有长度为 5 的美丽子串中，字典序最小的是子串 "11001"。
```

#### 示例 2
```text
Input: s = "1011", k = 2
Output: "11"
Explanation: 在此例中共有 3 个美丽子串：
1. 子串 "1011"
2. 子串 "1011"
3. 子串 "1011"
最短美丽子串的长度为 2。
长度为 2 的美丽子串中，字典序最小的是子串 "11"。
```

#### 示例 3
```text
Input: s = "000", k = 1
Output: ""
Explanation: 此例中不存在美丽子串。
```

---

### 约束条件
- `1 <= s.length <= 100`
- `1 <= k <= s.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把所有可能的子串都枚举出来，逐个检查它们是否满足“恰好有 k 个 `1`”。  
- **枚举子串**：双层循环 `i` 为左端点，`j` 为右端点（左闭右闭），共 `O(n²)` 种可能（`n` 是字符串长度）。  
- **统计 `1` 的个数**：对每个子串再遍历一次，计数，时间是 `O(length)`，最坏也是 `O(n)`。  
- **选最短、字典序最小**：在遍历过程中维护当前找到的最短长度 `min_len`，以及同样长度下字典序最小的子串 `answer`。

> **类比**：把字符串想象成一本书的章节，暴力解相当于把每一页都翻一遍、每一段都读一遍，找出满足条件的最短、最“好看”的那段。

只要把所有子串都检查一遍，就一定不会漏掉答案——这就是暴力解的正确性。

#### 代码（Python）

```python
def shortest_beautiful_bruteforce(s: str, k: int) -> str:
    n = len(s)
    min_len = float('inf')          # 当前找到的最短长度
    answer = ""                     # 对应的字典序最小子串

    # i 为左端点，j 为右端点（左闭右闭）
    for i in range(n):
        cnt = 0                     # 统计从 i 到 j 的 1 的个数
        for j in range(i, n):
            if s[j] == '1':
                cnt += 1
            # 当子串恰好有 k 个 1 时，考虑更新答案
            if cnt == k:
                cur_len = j - i + 1
                cur_sub = s[i:j+1]
                if cur_len < min_len:               # 更短的子串
                    min_len = cur_len
                    answer = cur_sub
                elif cur_len == min_len and cur_sub < answer:  # 同长，字典序更小
                    answer = cur_sub
                # 继续向右扩展也只能让长度变长，没必要再检查更大的 j
                break
            # 如果 cnt 已经 > k，后面的子串只会有更多的 1，直接结束内层循环
            if cnt > k:
                break

    return answer if min_len != float('inf') else ""
```

#### 复杂度  

- **时间复杂度**：`O(n³)`（外层 `O(n)` × 内层 `O(n)` × 计数 `O(n)`），在本题 `n ≤ 100` 时仍能跑完。  
  > “`O(n³)`” 可以想象成：先挑左端点（`n` 种），再挑右端点（最多 `n` 种），最后在子串里再走一遍（`n` 步）。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈在于 **重复统计子串中 `1` 的个数**。  
我们可以利用 **滑动窗口**（Two‑Pointer）一次遍历就知道任意区间里有多少个 `1`，从而把时间降到线性 `O(n)`。

**滑动窗口的核心想法**  
- 用两个指针 `left`、`right` 表示当前窗口 `[left, right]`（左闭右闭）。  
- `ones` 记录窗口里 `1` 的数量。  
- `right` 每次向右移动一位，把新字符加进窗口；  
- 当 `ones > k` 时，说明窗口里 `1` 太多，需要把 `left` 向右收缩，直到 `ones ≤ k`。  
- 当 `ones == k` 时，**此时的窗口已经是以当前 `right` 为右端点的最短窗口**（因为左端点已经尽可能往右收到了只剩下 `k` 个 `1`）。记录它的长度和子串；如果发现更短的子串，就更新答案；如果长度相同且字典序更小，也更新。

这样我们只遍历一次字符串，就能得到所有“恰好有 k 个 1 且最短”的窗口，并在过程中挑出字典序最小的那一个。

> **类比**：把窗口想成一根可伸缩的尺子，`right` 是尺子右端的笔，`left` 是左端的笔。我们不断把右端往右推，尺子里出现的 `1` 超过 `k` 时，就把左端往右收，保持尺子里恰好有 `k` 个 `1`。当尺子恰好满足条件时，它的长度就是当前可能的最短答案。

#### 代码（Python）

```python
def shortest_beautiful(s: str, k: int) -> str:
    n = len(s)
    left = 0               # 窗口左端
    ones = 0               # 窗口内 1 的个数
    min_len = float('inf') # 记录最短长度
    answer = ""            # 对应的字典序最小子串

    for right in range(n):                # 右端指针一次遍历整个字符串
        if s[right] == '1':
            ones += 1                     # 把新来的字符计入

        # 如果窗口里 1 太多，左端不断收缩
        while ones > k:
            if s[left] == '1':
                ones -= 1
            left += 1

        # 此时窗口里的 1 恰好等于 k，且 left 已经是最靠右的可能位置
        if ones == k:
            cur_len = right - left + 1
            cur_sub = s[left:right+1]

            if cur_len < min_len:                     # 找到更短的子串
                min_len = cur_len
                answer = cur_sub
            elif cur_len == min_len and cur_sub < answer:  # 同长，字典序更小
                answer = cur_sub

    return answer if min_len != float('inf') else ""
```

#### 复杂度  

- **时间复杂度**：`O(n)`。每个指针 `left`、`right` 只会向右移动最多 `n` 步，整个过程是线性遍历。  
  > “`O(n)`” 可以理解为：我们只走了一遍字符串，像一次快速的扫地，既不回头也不重复。  
- **空间复杂度**：`O(1)`，只用了常数个变量来保存指针、计数和答案。

与暴力解相比，时间从 `O(n³)` 降到了 `O(n)`，在最坏情况下快了好几百倍。

---

## 心得

- **核心技巧**：滑动窗口（Two‑Pointer） + 维护“最短 + 字典序最小”。  
- **适用的题型**  
  1. “子数组/子串恰好满足某种计数条件”的最短长度问题（如 LeetCode 209. Minimum Size Subarray Sum）。  
  2. “在满足条件的所有子串中找字典序最小”这类需要二次比较的题目（如 “最小字母序子串”）。  
  3. 二进制/字符计数类的窗口优化（如 “最长连续 1 的子数组”）。  
- **一句话总结**：  
  “先用滑动窗口一次遍历得到所有**恰好 k 个 1 的最短窗口**，再在这些窗口里挑出字典序最小的那一个。”

---

## 反思

- **第一反应**：把所有子串枚举一遍，直接检查每个子串是否满足条件。  
- **最容易踩的坑**  
  1. **忘记收缩窗口**：在滑动窗口中只移动右指针而不移动左指针，会导致 `ones` 永远不下降，错失答案。  
  2. **字典序比较**：在 Python 中直接用 `<` 比较字符串即可，但要确保只在长度相同的情况下比较，否则会产生错误的结果。  
  3. **特殊情况**：`k` 大于字符串中所有 `1` 的总数时，需要返回空串；代码中用 `min_len` 是否被更新来判断即可。  
- **下次思路**：  
  1. 先判断 “是否存在满足条件的子串”——用前缀和或计数快速判断。  
  2. 一想到“恰好 k 个 1”且要最短，立刻联想到 **滑动窗口**；  
  3. 在窗口满足条件时，**立即记录**（因为此时窗口已经是以当前右端点的最短），再继续滑动。这样既保证最短，又能在同长度时比较字典序。