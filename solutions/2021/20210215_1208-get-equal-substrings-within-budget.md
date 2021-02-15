# #1208. 在预算内获取相等子字符串 / Get Equal Substrings Within Budget

> 难度：中等 · 标签：String、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/get-equal-substrings-within-budget/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t of the same length and an integer maxCost.
You want to change s to t. Changing the ith character of s to ith character of t costs |s[i] - t[i]| (i.e., the absolute difference between the ASCII values of the characters).
Return the maximum length of a substring of s that can be changed to be the same as the corresponding substring of t with a cost less than or equal to maxCost. If there is no substring from s that can be changed to its corresponding substring from t, return 0.

**Examples**

**Example 1:**

```
Input: s = "abcd", t = "bcdf", maxCost = 3
Output: 3
Explanation: "abc" of s can change to "bcd".
That costs 3, so the maximum length is 3.
```

**Example 2:**

```
Input: s = "abcd", t = "cdef", maxCost = 3
Output: 1
Explanation: Each character in s costs 2 to change to character in t,  so the maximum length is 1.
```

**Example 3:**

```
Input: s = "abcd", t = "acde", maxCost = 0
Output: 1
Explanation: You cannot make any change, so the maximum length is 1.
```

**Constraints**

- 1 <= s.length <= 105
- t.length == s.length
- 0 <= maxCost <= 106
- s and t consist of only lowercase English letters.

---

## 题目（中文翻译）

给定两个长度相同的字符串 `s` 和 `t`，以及一个整数 `maxCost`。  
你希望把 `s` 改成 `t`。将 `s` 的第 `i` 个字符改成 `t` 的第 `i` 个字符的费用为 `|s[i] - t[i]|`（即两个字符的 ASCII 值的绝对差）。  
返回可以在费用不超过 `maxCost` 的前提下，将 `s` 的某个子字符串（substring）改成与 `t` 对应子字符串相同的**最大长度**。如果不存在这样子字符串，返回 `0`。

**示例 1**  
```text
Input: s = "abcd", t = "bcdf", maxCost = 3
Output: 3
Explanation: 将 `s` 的 `"abc"` 改成 `t` 的 `"bcd"`，费用为 3，故最大长度为 3。
```

**示例 2**  
```text
Input: s = "abcd", t = "cdef", maxCost = 3
Output: 1
Explanation: `s` 中的每个字符改成 `t` 中对应字符的费用都是 2，最多只能改动一个字符，故最大长度为 1。
```

**示例 3**  
```text
Input: s = "abcd", t = "acde", maxCost = 0
Output: 1
Explanation: 费用为 0 时不能进行任何修改，但单个字符本身已经相同，故最大长度为 1。
```

**约束条件**  
- `1 <= s.length <= 10^5`  
- `t.length == s.length`  
- `0 <= maxCost <= 10^6`  
- `s` 和 `t` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是枚举所有可能的子串，逐个计算把 `s` 中对应的子串改成 `t` 中子串的费用，看费用是否 ≤ `maxCost`，符合条件的就记录长度的最大值。

- **枚举子串**：可以用两层循环，外层固定左端点 `l`，内层把右端点 `r` 从 `l` 向右扩展。  
- **计算费用**：对每个新加入的字符 `i`，费用是 `abs(ord(s[i]) - ord(t[i]))`，把它累加到当前窗口的总费用中。  
- **检查预算**：如果累计费用已经超过 `maxCost`，这条子串就不合法，直接停止扩展右端点，继续下一个左端点。

> **生活化类比**：把字符串看成一排排的房子，每栋房子有不同的颜色（字符）。我们想把一段连续的房子改成另一段颜色相同的房子，改每栋房子需要花钱（费用）。暴力法就是把每一段可能的房子都去试一遍，看花的钱够不够。

这种做法一定能得到正确答案，因为我们把**所有**子串都检查了一遍。

#### 代码（Python）

```python
def equalSubstring_bruteforce(s: str, t: str, maxCost: int) -> int:
    n = len(s)
    ans = 0                         # 记录找到的最长合法长度
    # 枚举左端点
    for left in range(n):
        cost = 0                     # 当前窗口的总费用
        # 右端点不断往右扩展
        for right in range(left, n):
            # 计算新增字符的费用
            cost += abs(ord(s[right]) - ord(t[right]))
            # 一旦超过预算，就不可能再继续往右扩展了
            if cost > maxCost:
                break
            # 合法子串，更新答案
            ans = max(ans, right - left + 1)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环 `n` 次，内层最坏情况下也要遍历 `n` 次，所以总操作数大约是 `n × n`。  
  - 用大白话说，假设字符串长度是 10,000，暴力法大概要做 100,000,000 次“加法+比较”，对电脑来说已经有点慢了。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和输入规模无关。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算费用**：每次左端点左移时，窗口内部已经算过的费用会被重新累计，导致二次甚至多次遍历同一个字符。

我们可以把窗口的左端点和右端点一起“滑动”，让每个字符**只进一次窗口、只出一次窗口**，这就是**滑动窗口（Sliding Window）**技巧。

核心步骤如下：

1. **先算差值数组**  
   把每个位置的改动费用预先算好，存进数组 `diff[i] = abs(ord(s[i]) - ord(t[i]))`。这一步相当于把每栋房子的改造费用记在纸上，后面只需要查表。

2. **维护一个可变窗口**  
   - 用指针 `left` 标记窗口左端，`right` 标记右端（遍历时 `right` 只会向右移动）。  
   - `curCost` 保存窗口内所有 `diff` 的和，即当前子串的改造费用。  
   - 每次把 `right` 向右推进一格，把对应的 `diff[right]` 加到 `curCost`。  
   - 如果 `curCost` 超过 `maxCost`，说明窗口太宽了，需要把左端 `left` 往右收缩，直到费用 ≤ `maxCost`。收缩时把 `diff[left]` 从 `curCost` 中减去，然后 `left += 1`。  

3. **记录最长合法长度**  
   每次窗口合法（费用 ≤ `maxCost`）时，用 `right - left + 1` 更新答案。

> **类比**：把窗口想象成一根可伸缩的尺子，左端和右端分别是尺子的两端。我们不断把右端往右拉，尺子内部的“重量”是费用总和；当重量超过背包容量 `maxCost` 时，就把左端往右推，把最左边的重量扔掉，保持背包不超重。尺子每一次合法的长度，就是我们要的答案。

#### 代码（Python）

```python
def equalSubstring(s: str, t: str, maxCost: int) -> int:
    n = len(s)
    # 1. 预处理：把每个字符的改动费用算出来，存进 diff 数组
    diff = [abs(ord(s[i]) - ord(t[i])) for i in range(n)]

    left = 0          # 窗口左端指针
    curCost = 0       # 当前窗口的费用总和
    ans = 0           # 记录最长合法子串长度

    # 2. 右端指针从左到右遍历
    for right in range(n):
        curCost += diff[right]          # 把新加入的字符费用加进来

        # 3. 如果费用超出预算，就把左端往右收缩
        while curCost > maxCost:
            curCost -= diff[left]       # 移出左端字符的费用
            left += 1                   # 左端指针右移

        # 4. 此时窗口合法，更新答案
        ans = max(ans, right - left + 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个字符最多被右指针加入一次，又最多被左指针移出一次，整体只遍历了一遍。  
  - 用大白话说，字符串长度是 100,000，只需要做 100,000 次“加法+比较+可能的减法”，非常快。

- **空间复杂度**：`O(n)`（也可以写成 `O(1)`）  
  - 这里用了额外的 `diff` 数组来保存费用，大小与字符串等长，即 `O(n)`。如果在遍历时直接计算 `abs(ord(s[i]) - ord(t[i]))`，就可以省掉这块额外空间，做到 `O(1)`。

---

## 心得

- **核心技巧**：滑动窗口（Sliding Window）+ 前缀和思想。  
- **适用的题型**  
  1. 「最长子数组和 ≤ K」类问题（如 LeetCode 1004 *Max Consecutive Ones III*）。  
  2. 「最短子数组满足条件」类问题（如 LeetCode 209 *Minimum Size Subarray Sum*）。  
- **解题钥匙**：把「要找的子串」看成「一段连续的区间」，用两个指针维护这段区间的“费用”或“和”，让左指针在预算超限时自动收缩。

---

## 反思

- **第一反应**：看到“子串”和“费用上限”，自然想到枚举所有子串——这就是暴力思路。  
- **最容易踩的坑**  
  - 忘记在左指针收缩时同步减去对应的费用，导致窗口费用一直累加，答案错误。  
  - 忽略 `maxCost = 0` 的特殊情况，仍然可以得到长度 1（因为相同字符的费用为 0）。  
  - 对于极长的字符串（10⁵），暴力 `O(n²)` 会超时，需要及时切换到线性滑动窗口。  
- **下次遇到同类题**：第一步先**把每个元素的“代价”算出来**，然后**用双指针/滑动窗口**尝试在 O(n) 时间内维护一个满足“总代价 ≤ 限制”的区间。这样就能把大多数“在子数组/子串上限制和/费用”类问题快速解决。