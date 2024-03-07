# #2606. **找到最大代价的子串** / Find the Substring With Maximum Cost

> 难度：中等 · 标签：Array、Hash Table、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/find-the-substring-with-maximum-cost/)

---

## 题目（英文原版）

**Description**

You are given a string s, a string chars of distinct characters and an integer array vals of the same length as chars.
The cost of the substring is the sum of the values of each character in the substring. The cost of an empty string is considered 0.
The value of the character is defined in the following way:
Return the maximum cost among all substrings of the string s.

**Examples**

**Example 1:**

```
Input: s = "adaa", chars = "d", vals = [-1000]
Output: 2
Explanation: The value of the characters "a" and "d" is 1 and -1000 respectively.
The substring with the maximum cost is "aa" and its cost is 1 + 1 = 2.
It can be proven that 2 is the maximum cost.
```

**Example 2:**

```
Input: s = "abc", chars = "abc", vals = [-1,-1,-1]
Output: 0
Explanation: The value of the characters "a", "b" and "c" is -1, -1, and -1 respectively.
The substring with the maximum cost is the empty substring "" and its cost is 0.
It can be proven that 0 is the maximum cost.
```

**Constraints**

- 1 <= s.length <= 105
- s consist of lowercase English letters.
- 1 <= chars.length <= 26
- chars consist of distinct lowercase English letters.
- vals.length == chars.length
- -1000 <= vals[i] <= 1000

---

## 题目（中文翻译）

给定一个字符串 `s`，一个由互不相同字符组成的字符串 `chars`，以及一个与 `chars` 等长的整数数组 `vals`。  
子串（substring）的 **代价** 定义为该子串中每个字符的取值之和，空串的代价视为 `0`。  

字符的取值规则如下：

- 若字符出现在 `chars` 中，则其取值为 `vals` 中对应位置的值；
- 否则，该字符的取值为 `1`。

返回 `s` 的所有子串中能够取得的 **最大代价**。

---

### 示例

**示例 1**

```text
Input: s = "adaa", chars = "d", vals = [-1000]
Output: 2
Explanation: 字符 "a" 与 "d" 的取值分别为 1 和 -1000。
代价最大的子串是 "aa"，其代价为 1 + 1 = 2。
可以证明 2 是最大代价。
```

**示例 2**

```text
Input: s = "abc", chars = "abc", vals = [-1,-1,-1]
Output: 0
Explanation: 字符 "a"、"b"、"c" 的取值分别为 -1、-1、-1。
代价最大的子串是空子串 ""，其代价为 0。
可以证明 0 是最大代价。
```

---

### 约束条件

- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成
- `1 <= chars.length <= 26`
- `chars` 中的字符互不相同，且均为小写英文字母
- `vals.length == chars.length`
- `-1000 <= vals[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子串**，算出每个子串的“价值”，取最大值。

- **枚举子串**：两个循环，外层选子串的左端点 `l`，内层选右端点 `r`（`l ≤ r`），子串就是 `s[l…r]`。  
- **计算价值**：遍历子串里的每个字符，查它对应的价值（`chars` 中的字符对应 `vals`，其余字符价值为 `1`），把所有价值相加。  

> 类比：想象你在一本字典里查词，每查到一个词就记下它的页码（价值），最后把这些页码相加。这里的字典就是 **哈希表**（`dict`），`key` 是字符，`value` 是对应的分值。

这个方法一定能得到正确答案，因为我们把**所有可能的子串**都算了一遍，最大值必然在其中。

#### 代码（Python）

```python
def maximumCostSubstring_bruteforce(s: str, chars: str, vals: list[int]) -> int:
    # 1. 建立字符 -> 价值的映射表，默认价值为 1
    value_map = {c: v for c, v in zip(chars, vals)}
    # 2. 暴力枚举所有子串
    n = len(s)
    best = 0                     # 空串的价值是 0
    for l in range(n):
        cur = 0                  # 当前子串从 l 开始的累计价值
        for r in range(l, n):
            # 取字符 s[r] 的价值；若不在映射表里则为 1
            cur += value_map.get(s[r], 1)
            # 更新全局最大值
            if cur > best:
                best = cur
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - 两层循环分别遍历左端点和右端点，最坏情况下要检查 `n·(n+1)/2 ≈ n²/2` 个子串。  
  - 用大白话说，若 `n = 10,000`，则需要约一亿次运算，已经很慢了。
- **空间复杂度**：`O(1)`（不计输入本身的空间）。  
  - 只用了常数级的额外变量和一个大小不超过 26 的哈希表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复累计子串价值**。  
如果我们把原字符串 `s` 中每个字符直接转换成它的数值（`1` 或 `vals[i]`），问题就变成：

> 在一个整数数组 `arr` 中，找到**连续子数组的最大和**。

这正是经典的**最大子段和**（Maximum Subarray Sum）问题，可以用 **Kadane 算法**在一次遍历中求解。

**步骤拆解**：

1. **构造价值数组** `arr`  
   - 用哈希表把 `chars` → `vals` 映射好。  
   - 遍历 `s`，把每个字符映射为对应的整数，得到 `arr[i]`。  
   - 类比：把每个字符想象成一张纸条，上面写着它的“价值”。把所有纸条排成一行，就是 `arr`。

2. **Kadane 算法**  
   - 维护两个变量：  
     - `cur`：以当前位置结尾的子数组的最大和（如果加上当前值后变负，就把它重置为 0，因为空串价值为 0）。  
     - `best`：全局最大和。  
   - 伪代码：  
     ```
     cur = 0
     best = 0
     for x in arr:
         cur = max(0, cur + x)   # 若累计和为负则抛弃，重新开始
         best = max(best, cur)
     ```
   - 这里把 **负数** 当成“要不要继续往下走”的信号；如果累计和跌到负数，说明之前的子串已经把价值拉低了，直接从下一个字符重新开始会更好。

3. **返回结果**  
   - `best` 即为所有子串的最大价值。若所有字符价值都是负数，`best` 仍然是 0，对应空串。

#### 代码（Python）

```python
def maximumCostSubstring(s: str, chars: str, vals: list[int]) -> int:
    # 1. 建立字符 → 价值的映射（哈希表），默认价值为 1
    value_map = {c: v for c, v in zip(chars, vals)}

    # 2. Kadane 算法求最大子段和
    cur = 0          # 当前累计价值（以当前字符结尾的子串）
    best = 0         # 全局最大价值，空串的价值是 0

    for ch in s:
        # 把字符转换成对应的整数价值
        v = value_map.get(ch, 1)
        # 如果累计和为负，就从 0 开始（相当于抛弃之前的子串）
        cur = max(0, cur + v)
        # 更新全局最大值
        best = max(best, cur)

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 只遍历一次字符串 `s`（`n = len(s)`），每次操作都是 O(1)。  
  - 与暴力解的 `O(n²)` 相比，快了 **指数级**，即使 `n = 10⁵` 也能毫秒级完成。

- **空间复杂度**：`O(1)`（哈希表大小 ≤ 26，视为常数）。  
  - 不需要额外的数组，只用了几个整数变量。

---

## 心得

- **核心技巧**：把字符价值映射成整数数组后，使用 **Kadane 最大子段和**求解。  
- **适用题型**  
  1. “最大子数组和”类题目（如 LeetCode 53）。  
  2. “带权字符/数字的最长子串”类题目（如把字符转成正负权值后求最大/最小）。  
  3. “连续子序列的最优值”问题（如股票买卖的最大利润等）。  
- **一句话总结**：**先把问题转化为数值序列的最大子段和，再用 Kadane 一遍扫过去。**

---

## 反思

- **第一反应**：看到“子串的价值求最大”，立刻想到**枚举子串**，因为最直观。  
- **最容易踩的坑**  
  - **默认价值**：忘记把不在 `chars` 中的字符价值设为 `1`。  
  - **空串**：所有价值均为负时，答案应为 `0`（空串），而不是负数，需要在 Kadane 中使用 `max(0, …)`。  
  - **字符映射**：`chars` 与 `vals` 对应时要用哈希表，防止 O(n) 查找导致时间爆炸。  
- **下次类似题**：第一步先**把字符/元素映射成数值**，看能否转化为经典的 **最大子段和 / 最小子段和** 问题，再选用对应的线性算法。