# #1759. 同构子串计数 / Count Number of Homogenous Substrings

> 难度：中等 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/count-number-of-homogenous-substrings/)

---

## 题目（英文原版）

**Description**

Given a string s, return the number of homogenous substrings of s. Since the answer may be too large, return it modulo 109 + 7.
A string is homogenous if all the characters of the string are the same.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "abbcccaa"
Output: 13
Explanation: The homogenous substrings are listed as below:
"a"   appears 3 times.
"aa"  appears 1 time.
"b"   appears 2 times.
"bb"  appears 1 time.
"c"   appears 3 times.
"cc"  appears 2 times.
"ccc" appears 1 time.
3 + 1 + 2 + 1 + 3 + 2 + 1 = 13.
```

**Example 2:**

```
Input: s = "xy"
Output: 2
Explanation: The homogenous substrings are "x" and "y".
```

**Example 3:**

```
Input: s = "zzzzz"
Output: 15
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，返回 `s` 中同构子串（homogenous substring）的数量。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

如果一个字符串的所有字符都相同，则该字符串是同构的。  
子串（substring）是字符串中连续的一段字符序列。

## 示例

### 示例 1
**输入**  
`s = "abbcccaa"`

**输出**  
`13`

**解释**  
同构子串如下所示：

- `"a"` 出现 3 次。  
- `"aa"` 出现 1 次。  
- `"b"` 出现 2 次。  
- `"bb"` 出现 1 次。  
- `"c"` 出现 3 次。  
- `"cc"` 出现 2 次。  
- `"ccc"` 出现 1 次。  

`3 + 1 + 2 + 1 + 3 + 2 + 1 = 13`。

### 示例 2
**输入**  
`s = "xy"`

**输出**  
`2`

**解释**  
同构子串为 `"x"` 和 `"y"`。

### 示例 3
**输入**  
`s = "zzzzz"`

**输出**  
`15`

## 约束条件
- `1 <= s.length <= 10^5`
- `s` 仅由小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子串**，检查它是否是“同质的”（所有字符相同），如果是就计数。  
- **数据结构**：我们只需要使用 **字符串本身** 和 **两个循环的下标**。可以把它想象成在一本书里，用两根手指分别指向起始页和结束页，逐页读出来判断内容是否全部相同。  
- **正确性**：因为我们遍历了**所有**连续的字符区间（即所有子串），只要子串满足“所有字符相同”，就一定会被计入答案。没有遗漏，也没有多计。

#### 代码（Python）

```python
def countHomogenous(s: str) -> int:
    MOD = 10**9 + 7          # 题目要求的取模数
    n = len(s)
    ans = 0

    # i 为子串的左端点（包含），j 为右端点（包含）
    for i in range(n):
        # 只要当前字符和前一个相同，就继续往右扩展
        # 否则直接退出内部循环，因为子串已经不再同质
        for j in range(i, n):
            # 判断子串 s[i:j+1] 是否同质
            # 只要发现一个字符不同，就可以提前结束
            if s[j] != s[i]:
                break
            ans += 1          # 这一次扩展得到的子串是同质的
            ans %= MOD        # 防止中间结果溢出

    return ans
```

> **关键行解释**  
> - `if s[j] != s[i]: break`：一旦遇到不同字符，后面的更长子串一定也不同，直接停止内层循环，省点时间。  
> - `ans %= MOD`：因为答案可能非常大，实时取模可以避免整数溢出。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 想象把字符串的每个字符当作起点，向右检查最多 `n` 次，总共大约 `n·(n+1)/2` 次比较。  
  - 对于 `n = 10⁵`，这相当于 10⁹ 次操作，显然会超时。

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（`ans、i、j`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们不断重复检查同一段字符是否相同。实际上，同质子串的数量只和**连续相同字符的段长度**有关。  

**关键观察**  
- 若一段连续相同字符的长度为 `k`（例如 `"aaa"`），则所有同质子串正好是这段内部所有可能的起止组合。  
- 组合数公式：从 `k` 个位置中任选起点和终点，且起点 ≤ 终点，组合数是  

\[
\binom{k+1}{2}= \frac{k(k+1)}{2}
\]

  这就像在一排 `k` 本相同的书中，任选两本（可以是同一本）作为子串的左、右边界。

**优化步骤**  

1. **一次遍历**整个字符串，统计每段连续相同字符的长度 `k`。  
2. 对每段，用公式 `k·(k+1)//2` 直接算出该段贡献的同质子串数量。  
3. 累加所有段的贡献，最后对 `10⁹+7` 取模。

**为什么只需要一次遍历？**  
- 当我们从左到右走时，遇到字符变化（比如 `'a' → 'b'`）就说明前一段已经结束，长度已经完整，立刻可以把它的贡献算进去。这样每个字符只会被访问一次。

#### 代码（Python）

```python
def countHomogenous(s: str) -> int:
    MOD = 10**9 + 7
    ans = 0          # 最终答案
    cur_len = 1      # 当前连续相同字符的长度，至少为 1

    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            # 与前一个字符相同，继续扩大当前段
            cur_len += 1
        else:
            # 段结束，计算贡献
            ans = (ans + cur_len * (cur_len + 1) // 2) % MOD
            cur_len = 1   # 重新开启新段，长度恢复为 1

    # 循环结束后，最后一段可能还没计入
    ans = (ans + cur_len * (cur_len + 1) // 2) % MOD
    return ans
```

> **关键行解释**  
> - `cur_len * (cur_len + 1) // 2`：直接套用组合数公式，得到该段的同质子串数量。  
> - `ans = (ans + …) % MOD`：每次累加后立即取模，防止中间结果超出整数范围。  
> - 循环结束后仍需 **一次** 额外的累计，因为最后一段不会在 `else` 分支里被处理。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，`n` 为字符串长度。相当于走完一条街，只需要一次来回，不会重复检查。

- **空间复杂度**：`O(1)`  
  - 只使用了几个整数变量，和输入规模无关。

---

## 心得

- **核心技巧**：把“同质子串计数”转化为“连续相同字符段的长度”，并用**组合数公式**一次性求和。  
- **适用的题型**  
  1. “子数组/子串的某种特性只与连续相同元素有关”——如 **Count Subarrays With Fixed Bounds**（需要统计连续递增段）。  
  2. “统计满足某种单调/相等条件的子区间”——如 **Number of Subarrays With Bounded Maximum**。  
  3. “统计所有只包含一种字符的子串”——如本题的变体 **Count Binary Substrings**（统计 0/1 交替的子串）。
- **一句话总结**：**把局部“同质”转化为段长度，用 `k·(k+1)/2` 一次算完。**

---

## 反思

- **第一反应**：直接枚举所有子串，检查是否同质——这是一种最自然的暴力思路。  
- **最容易踩的坑**  
  1. **忘记取模**：答案可能非常大，忘记在累计时取模会导致整数溢出或运行超时。  
  2. **边界处理**：循环结束后最后一段的计数容易遗漏，需要额外的累加步骤。  
  3. **长度为 1 的字符串**：`cur_len` 初始化要为 1，防止出现 `0` 长度导致错误的组合数。  
- **下次遇到同类题**，第一步应该问自己：“**这道题的答案是否只和连续相同/递增/递减的段长度有关**？”如果答案是肯定的，就立刻转向 **一次遍历 + 公式求和** 的思路，而不是盲目枚举。