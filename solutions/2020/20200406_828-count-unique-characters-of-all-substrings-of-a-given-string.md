# #828. 统计给定字符串所有子串的唯一字符数 / Count Unique Characters of All Substrings of a Given String

> 难度：困难 · 标签：Hash Table、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/)

---

## 题目（英文原版）

**Description**

Let's define a function countUniqueChars(s) that returns the number of unique characters in s.
Given a string s, return the sum of countUniqueChars(t) where t is a substring of s. The test cases are generated such that the answer fits in a 32-bit integer.
Notice that some substrings can be repeated so in this case you have to count the repeated ones too.

**Examples**

**Example 1:**

```
Input: s = "ABC"
Output: 10
Explanation: All possible substrings are: "A","B","C","AB","BC" and "ABC".
Every substring is composed with only unique letters.
Sum of lengths of all substring is 1 + 1 + 1 + 2 + 2 + 3 = 10
```

**Example 2:**

```
Input: s = "ABA"
Output: 8
Explanation: The same as example 1, except countUniqueChars("ABA") = 1.
```

**Example 3:**

```
Input: s = "LEETCODE"
Output: 92
```

**Constraints**

- 1 <= s.length <= 105
- s consists of uppercase English letters only.

---

## 题目（中文翻译）

定义函数 `countUniqueChars(s)`，返回字符串 `s` 中唯一字符（unique characters）的数量。  
给定一个字符串 `s`，返回所有子串（substring）`t` 的 `countUniqueChars(t)` 之和。测试用例保证答案能够放入 32 位整数。  
注意，某些子串可能会出现多次，此时需要把重复出现的子串也计入。

**示例 1**  
``` 
Input: s = "ABC"
Output: 10
Explanation: 所有可能的子串为："A","B","C","AB","BC" 和 "ABC"。  
每个子串内部的字符都是唯一的。  
所有子串的唯一字符数之和为 1 + 1 + 1 + 2 + 2 + 3 = 10
```

**示例 2**  
``` 
Input: s = "ABA"
Output: 8
Explanation: 与示例 1 相同，只是 `countUniqueChars("ABA") = 1`（因为只有字符 'B' 是唯一的）。
```

**示例 3**  
``` 
Input: s = "LEETCODE"
Output: 92
```

**约束条件**

- `1 <= s.length <= 10^5`
- `s` 仅由大写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的子串都列举出来，然后逐个统计子串里**不重复出现的字符**有多少个，最后把这些数量加在一起。

- **枚举子串**：可以用两层循环，外层决定子串的左端点 `i`，内层决定右端点 `j`（`i ≤ j`），子串即 `s[i:j+1]`。  
- **统计唯一字符**：对每个子串，用一个哈希表（相当于字典）记录字符出现的次数。遍历完子串后，统计出现次数恰好为 `1` 的字符个数，这就是 `countUniqueChars` 的值。  
  - 哈希表就像一本“查字典”，我们把字符当作单词，出现次数当作页码。找不到的就说明该字符在子串里根本没出现。

**为什么正确**  
因为我们把**所有**子串都算了一遍，并且对每个子串都用了**精确**的唯一字符计数方法，所以结果必然等于题目要求的“所有子串的唯一字符数之和”。

**复杂度大白话**  
- 两层循环遍历子串的次数是 `n*(n+1)/2`，大约是 `n²/2`，所以时间复杂度记作 `O(n²)`，意思是当字符串长度翻倍，运行时间大约会增长四倍（因为平方关系）。  
- 对每个子串我们又要遍历一次子串本身来统计字符出现次数，最坏情况下子串长度也是 `O(n)`，于是整体时间变成 `O(n³)`（立方），这在 `n=10⁵` 时根本不可接受。  
- 空间上我们只用了一个哈希表来存当前子串的字符计数，最多存 `26`（大写字母个数）个键值对，算作 `O(1)` 常数空间。

#### 代码（Python）

```python
def uniqueLetterString_bruteforce(s: str) -> int:
    n = len(s)
    total = 0

    # 枚举所有子串的左端点
    for i in range(n):
        # 记录从 i 开始往右的子串中字符出现的次数
        freq = {}
        # 枚举右端点
        for j in range(i, n):
            ch = s[j]
            freq[ch] = freq.get(ch, 0) + 1          # 哈希表：字符 -> 出现次数

            # 统计当前子串唯一字符的个数
            uniq_cnt = sum(1 for v in freq.values() if v == 1)
            total += uniq_cnt                         # 累加到答案

    return total
```

> 关键点已经用中文注释标出，直接复制运行即可得到正确答案（只适用于很短的字符串，长度 > 1000 会超时）。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 两层循环遍历所有子串是 `O(n²)`，每次子串统计唯一字符又要遍历哈希表（最坏 `O(n)`），相乘得到立方级别。  
  - 用大白话说，就是“每增加一个字符，工作量会乘以大约 n”。  
- **空间复杂度**：`O(1)`（哈希表最多 26 条记录，视作常数）  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复统计**：同一个字符会在很多子串里出现多次，我们每次都要重新遍历子串来判断它是否唯一。  
如果能**直接算出每个字符对答案的贡献**，就能把重复工作省掉。

**核心观察**  
对于字符串 `s` 中的某个位置 `i`（字符记作 `c = s[i]`），只要在当前子串里 `c` **恰好出现一次**，它就会为该子串贡献 `1`。  
要让 `c` 在子串 `[l, r]` 中唯一，需要满足：

```
l ≤ i ≤ r          # 子串必须覆盖到位置 i
在子串的左边没有另一个相同字符
在子串的右边没有另一个相同字符
```

换句话说，左边最近的同字符位置记作 `prev`（如果不存在设为 -1），右边最近的同字符位置记作 `next`（如果不存在设为 n）。  
只要子串的左端点 `l` 落在 `(prev, i]`，右端点 `r` 落在 `[i, next)`，`c` 就是唯一的。

- 左端点的合法选择数 = `i - prev`（因为可以是 `prev+1, prev+2, …, i`）  
- 右端点的合法选择数 = `next - i`（因为可以是 `i, i+1, …, next-1`）  

于是，**位置 i 上的字符 `c` 对答案的贡献** 为：

```
contribution_i = (i - prev) * (next - i)
```

把所有位置的贡献加起来，就是所有子串唯一字符数的总和。

**如何快速得到 `prev` 与 `next`**  
遍历一遍字符串，用一个哈希表记录每个字符上一次出现的位置 `prev`。在遍历时我们可以立即得到 `prev`，而 `next` 需要等到后面再算。最简做法是：

1. **第一次遍历**：记录每个字符出现的所有位置（列表）。  
2. 对每个字符的出现列表 `pos = [p0, p1, …, pk]`，在列表两端各加一个哨兵：`-1` 在前，`n` 在后。  
3. 对列表中每个真实位置 `pos[t]`，`prev = pos[t-1]`，`next = pos[t+1]`，计算贡献并累计。

因为字符集只有 26 个大写字母，整个过程只需要 `O(n)` 的时间和 `O(n)` 的额外空间（存位置列表）。

**类比**：把每个字符想成一根**灯泡**，灯泡左边最近的另一根灯泡是它的“左遮光板”，右边最近的灯泡是“右遮光板”。灯泡能够“照亮”的区间就是左遮光板与右遮光板之间的矩形面积——这正是 `(i - prev) * (next - i)`。

#### 代码（Python）

```python
def uniqueLetterString(s: str) -> int:
    """
    O(n) 时间、O(n) 空间的最优解。
    思路：每个字符贡献 = (i - 上一次出现位置) * (下次出现位置 - i)
    """
    n = len(s)
    # 记录每个字符出现的所有下标，使用 26 个列表（因为只有大写字母）
    pos = {chr(ord('A') + i): [] for i in range(26)}
    for idx, ch in enumerate(s):
        pos[ch].append(idx)

    ans = 0
    for ch, lst in pos.items():
        if not lst:               # 该字符根本没出现，直接跳过
            continue
        # 在列表前后各加一个哨兵，方便统一计算边界情况
        lst = [-1] + lst + [n]
        # 现在 lst 的长度至少为 3（-1, 真实位置, n）
        for i in range(1, len(lst) - 1):
            prev = lst[i - 1]      # 左侧最近的相同字符位置
            cur  = lst[i]          # 当前字符所在的位置
            nxt  = lst[i + 1]      # 右侧最近的相同字符位置
            contribution = (cur - prev) * (nxt - cur)
            ans += contribution
    return ans
```

> 代码里每一步都有中文注释，直接运行即可得到答案。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串收集位置（`O(n)`），随后对每个字符的出现列表做一次线性遍历，总长度仍是 `n`，所以整体是线性级别。  
  - 用大白话说，就是“字符数翻倍，运行时间也只会翻倍”，远远快于暴力的立方级别。  
- **空间复杂度**：`O(n)`  
  - 需要保存每个字符出现的下标，总共恰好 `n` 个整数。  
  - 如果只用固定大小的 26 个列表（每个列表内部存下标），空间仍然随 `n` 成线性增长。  

---

## 心得

- **核心技巧**：**字符贡献法**（Contribution of each character），即把全局求和拆解为每个位置独立贡献的求和。  
- **适用题型**：  
  1. “所有子数组/子串的最大/最小值之和”——如 LeetCode 907. Sum of Subarray Minimums。  
  2. “统计子数组/子串中出现次数唯一的元素个数”——本题的变形。  
  3. “子数组/子串中出现次数恰好为 k 的元素个数”——同样可以用出现位置的间距来计数。  
- **一句话总结**：**把“在每个子串里数唯一字符”转化为“每个字符在多少子串里唯一”，从而只遍历一次字符串**。

---

## 反思

- **拿到题目第一反应**：先想到最笨的办法——枚举所有子串，逐个计数。  
- **最容易踩的坑**：  
  - 忽视**边界情况**：字符在字符串最左或最右的出现，需要把 `prev` 当作 `-1`、`next` 当作 `n`，否则会少算一些子串。  
  - **整数溢出**：虽然题目保证答案在 32 位整数范围，但在语言没有自动大整数时要注意乘法可能临时超出。Python 不会有问题。  
  - **忘记加哨兵**：没有在位置列表两端加 `-1`、`n`，会导致第一个或最后一个出现位置的贡献计算错误。  
- **下次遇到同类题**：第一步就思考**“能否把全局求和拆成每个元素的贡献？”**，如果能，就往这条路上找 `prev/next`、单调栈或前缀和等工具。这样往往能把指数级或平方级的暴力直接降到线性级。