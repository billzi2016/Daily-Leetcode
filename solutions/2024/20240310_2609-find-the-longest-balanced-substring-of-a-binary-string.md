# #2609. 寻找二进制字符串的最长平衡子串 / Find the Longest Balanced Substring of a Binary String

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/find-the-longest-balanced-substring-of-a-binary-string/)

---

## 题目（英文原版）

**Description**

You are given a binary string s consisting only of zeroes and ones.
A substring of s is considered balanced if all zeroes are before ones and the number of zeroes is equal to the number of ones inside the substring. Notice that the empty substring is considered a balanced substring.
Return the length of the longest balanced substring of s.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "01000111"
Output: 6
Explanation: The longest balanced substring is "000111", which has length 6.
```

**Example 2:**

```
Input: s = "00111"
Output: 4
Explanation: The longest balanced substring is "0011", which has length 4.
```

**Example 3:**

```
Input: s = "111"
Output: 0
Explanation: There is no balanced substring except the empty substring, so the answer is 0.
```

**Constraints**

- 1 <= s.length <= 50
- '0' <= s[i] <= '1'

---

## 题目（中文翻译）

给定一个仅由 `0` 和 `1` 组成的二进制字符串 `s`。  
`s` 的子串（**substring**）被认为是平衡的（**balanced**），当且仅当子串中所有的 `0` 都位于所有的 `1` 之前，并且子串中 `0` 的个数等于 `1` 的个数。需要注意，空子串也算作平衡子串。  

返回 `s` 中最长平衡子串的长度。  

子串是字符串中连续的字符序列。

**示例 1**  
**输入:** `s = "01000111"`  
**输出:** `6`  
**解释:** 最长的平衡子串是 `"000111"`，其长度为 `6`。

**示例 2**  
**输入:** `s = "00111"`  
**输出:** `4`  
**解释:** 最长的平衡子串是 `"0011"`，其长度为 `4`。

**示例 3**  
**输入:** `s = "111"`  
**输出:** `0`  
**解释:** 除空子串外不存在平衡子串，答案为 `0`。

**约束条件**  
- `1 <= s.length <= 50`  
- `s[i]` 为 `'0'` 或 `'1'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的子串都枚举出来，逐个检查它是不是 “balanced”。**  
具体做法：

1. 用两层循环，外层 `i` 表示子串的左端点，内层 `j`（`j > i`）表示右端点。  
   这样就能得到所有 `s[i:j]`（Python 切片不含右端点）这种连续的子串。  
2. 对每个子串判断是否满足平衡条件：  
   - 先把子串里的所有字符分成两段，左边全是 `'0'`，右边全是 `'1'`。  
   - 检查左段和右段的长度是否相等。  
   - 这一步可以用 `count('0')` 与 `count('1')` 来实现，或者手动遍历统计。  
3. 如果子串平衡，就更新答案 `ans = max(ans, len(sub))`。

> **类比**：把哈希表想成一本“字典”，`key` 是单词，`value` 是页码。这里我们不需要哈希表，只需要把每个子串“翻开”，逐字检查它是否符合“先零后一且数量相等”的规则。

> **为什么一定对？**  
> 枚举了**所有**可能的子串，检查每一个是否满足题目要求，最大长度自然就是答案。

#### 代码（Python）

```python
def longestBalancedSubstring_bruteforce(s: str) -> int:
    n = len(s)
    ans = 0                      # 记录目前找到的最长平衡子串长度

    # i 为子串左端点（含），j 为右端点（不含），两层遍历得到所有子串
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = s[i:j]         # 当前子串
            # 统计子串中 0 和 1 的个数
            zeros = sub.count('0')
            ones  = sub.count('1')
            # 必须先出现所有 0，后出现所有 1，且数量相等
            # 检查是否满足 “0*1*” 的形式
            if zeros == ones and sub == '0' * zeros + '1' * ones:
                ans = max(ans, j - i)   # 更新最大长度

    return ans
```

#### 复杂度

- **时间复杂度：** `O(n³)`  
  - 两层循环产生 `O(n²)` 个子串。  
  - 对每个子串我们用了 `count`（相当于遍历一次）来统计 `'0'` 与 `'1'`，这又是 `O(n)`，所以总体是 `O(n²·n) = O(n³)`。  
  - 大白话：如果字符串长度是 10，最多要检查 10·10·10 = 1000 次；长度是 50 时，最坏会有 125 000 次操作，已经相当慢了。

- **空间复杂度：** `O(1)`（不计入返回值）  
  - 只用了常数级别的额外变量 `ans、i、j、zeros、ones`，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历同一段字符**。我们其实只需要一次线性扫描就能得到答案。

观察题目要求的 “balanced substring”：

- 必须是 **先全是 `0`，后全是 `1`**，且两段长度相等。  
- 换句话说，子串可以写成 `0…0 1…1`，其中 `0` 的个数 = `1` 的个数 = `k`，子串长度 = `2k`。

因此，只要我们知道 **相邻的两段连续字符的长度**，就能直接算出能组成的最长平衡子串的长度：

```
... 0000 111 ...
      ^   ^
   前一段 0 的长度 = a
   当前段 1 的长度 = b
   能组成的平衡子串长度 = 2 * min(a, b)
```

**核心思路**：

1. **一次遍历**，记录当前字符连续出现的次数 `cnt`，以及上一段字符的次数 `prev_cnt`。  
2. 当字符发生切换（从 `0` → `1` 或 `1` → `0`）时：  
   - 把 `prev_cnt` 更新为上一次的 `cnt`（即上一段的长度）。  
   - 把 `cnt` 重新计数为 1（因为新段已经开始）。  
3. 每次 **进入 `1` 段**（因为平衡子串一定以 `1` 结束）时，用 `2 * min(prev_cnt, cnt)` 更新答案。  
   - 当 `prev_cnt` 小于 `cnt` 时，`prev_cnt` 决定了能配对的 `0` 的数量；反之亦然。  

这样只遍历一次字符串，时间线性。

> **类比**：想象你在排队买票，前面是一队只拿 `0` 的人，后面是一队只拿 `1` 的人。要组成“平衡队伍”，两队人数必须相同，最少的那队决定了可以凑多少人。我们只需要记录每次两队的长度，就能立刻算出最大可能的平衡长度。

#### 代码（Python）

```python
def longestBalancedSubstring(s: str) -> int:
    """
    返回二进制字符串 s 中最长的平衡子串长度。
    思路：一次线性扫描，记录相邻两段连续字符的长度。
    """
    prev_cnt = 0      # 上一段（左边）的字符数量
    cnt = 0           # 当前段的字符数量
    ans = 0           # 当前找到的最长平衡子串长度
    prev_char = ''    # 用来判断是否换段

    for ch in s:
        if ch == prev_char:          # 仍然在同一段，计数加一
            cnt += 1
        else:                        # 段切换了
            # 当新段开始时，上一段的长度就已经确定
            prev_cnt = cnt
            cnt = 1                  # 当前段从 1 开始计数
            prev_char = ch

        # 只有当当前段是 '1' 时，子串才能以 '1' 结束
        if ch == '1':
            # 取两段的较小值，两者配对后长度是 2 * min(...)
            ans = max(ans, 2 * min(prev_cnt, cnt))

    return ans
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 只遍历一次字符串，`n` 是字符串长度。  
  - 大白话：如果 `n = 50`，最多只看 50 次字符，几乎瞬间完成。

- **空间复杂度：** `O(1)`  
  - 只用了几条整数变量（`prev_cnt、cnt、ans、prev_char`），占用的内存不随 `n` 增长。

---

## 心得

- **核心技巧**：**相邻段计数 + 取最小值**。  
  这是一种常见的 “分段统计 + 取 min” 思路，适用于所有要求“左边全 A、右边全 B 且数量相等”的子串问题。

- **相似题型**（可再练习）：
  1. *Longest Substring with Equal Number of 0s and 1s*（不要求顺序，只要求数量相等）——可用前缀和+哈希表。
  2. *Maximum Length of a Subarray With Positive Product*（子数组乘积为正）——需要统计正负数的连续段。
  3. *Longest Well-Formed Parentheses*（有效括号子串）——同样利用“相邻段配对”思路。

- **一句话总结解题钥匙**：**只要知道相邻两段连续字符的长度，就能立刻算出能组成的最长平衡子串**。

---

## 反思

- **第一反应**：看到“子串”“零在前、一在后”“数量相等”，自然想到**枚举所有子串**检查，这就是暴力解的来源。  
- **最容易踩的坑**：  
  - 忽视空子串的合法性（答案可能是 0）。  
  - 在暴力实现时，判断“先零后一”的条件容易写错，例如 `sub == '0'*zeros + '1'*ones` 必须放在 `zeros == ones` 之后，否则会误判 `0010` 为平衡。  
  - 在最优解里，需要特别注意**段切换的时机**：只有当当前字符是 `'1'` 时才计算答案，否则会把 `000`（没有 `'1'`）误算进来。

- **下次遇到同类题**，第一步应**先把字符串划分成连续相同字符的块**，记录每块的长度，然后思考“两块之间能配对的规则”。这一步往往能把时间复杂度从 `O(n²)` 或 `O(n³)` 降到 `O(n)`。