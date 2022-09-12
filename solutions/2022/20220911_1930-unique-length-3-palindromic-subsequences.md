# #1930. 唯一的长度为3的回文子序列 / Unique Length-3 Palindromic Subsequences

> 难度：中等 · 标签：Hash Table、String、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/unique-length-3-palindromic-subsequences/)

---

## 题目（英文原版）

**Description**

Given a string s, return the number of unique palindromes of length three that are a subsequence of s.
Note that even if there are multiple ways to obtain the same subsequence, it is still only counted once.
A palindrome is a string that reads the same forwards and backwards.
A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

**Examples**

**Example 1:**

```
Input: s = "aabca"
Output: 3
Explanation: The 3 palindromic subsequences of length 3 are:
- "aba" (subsequence of "aabca")
- "aaa" (subsequence of "aabca")
- "aca" (subsequence of "aabca")
```

**Example 2:**

```
Input: s = "adc"
Output: 0
Explanation: There are no palindromic subsequences of length 3 in "adc".
```

**Example 3:**

```
Input: s = "bbcbaba"
Output: 4
Explanation: The 4 palindromic subsequences of length 3 are:
- "bbb" (subsequence of "bbcbaba")
- "bcb" (subsequence of "bbcbaba")
- "bab" (subsequence of "bbcbaba")
- "aba" (subsequence of "bbcbaba")
```

**Constraints**

- 3 <= s.length <= 105
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，返回 `s` 中作为子序列（subsequence）出现的、长度为 3 的唯一回文（palindrome）数量。  
即使同一个子序列可以通过多种方式得到，也只计一次。

**回文（palindrome）** 是指正读和倒读完全相同的字符串。  
**子序列（subsequence）** 是在不改变剩余字符相对顺序的前提下，删除原字符串中的若干字符（可以不删）得到的新字符串。

### 示例

#### 示例 1
输入: `s = "aabca"`  
输出: `3`  
解释: 长度为 3 的回文子序列共有 3 个：
- `"aba"`（`"aabca"` 的子序列）
- `"aaa"`（`"aabca"` 的子序列）
- `"aca"`（`"aabca"` 的子序列）

#### 示例 2
输入: `s = "adc"`  
输出: `0`  
解释: `"adc"` 中不存在长度为 3 的回文子序列。

#### 示例 3
输入: `s = "bbcbaba"`  
输出: `4`  
解释: 长度为 3 的回文子序列共有 4 个：
- `"bbb"`（`"bbcbaba"` 的子序列）
- `"bcb"`（`"bbcbaba"` 的子序列）
- `"bab"`（`"bbcbaba"` 的子序列）
- `"aba"`（`"bbcbaba"` 的子序列）

### 约束条件
- `3 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把所有可能的长度为 3 的子序列枚举出来，检查它们是不是回文（前后字符相同），再用集合去重。  

- **枚举子序列**：遍历下标 `i < j < k`，把 `s[i] + s[j] + s[k]` 拼成一个三字符的字符串。  
- **回文判断**：只要 `s[i] == s[k]`（首尾相同），中间字符可以随意。  
- **去重**：把满足条件的子序列放进 `set`，集合天然会把相同的字符串合并，只计一次。  

> **类比**：把字符串想成一排小球，暴力解就像把每三个球挑出来检查颜色，挑完所有组合后再把颜色相同的“三球串”放进盒子里去重。  

**为什么正确**：  
- 所有长度为 3 的子序列都被遍历到了（因为我们遍历了所有合法的下标三元组）。  
- 只要首尾相同，必然是回文；不满足首尾相同的直接丢掉。  

**复杂度分析（大白话）**：  
- **时间**：我们要检查每一种 `i, j, k` 的组合。下标总数是 `n`，组合数大约是 `n³/6`，即 **O(n³)**。想象把所有三球组合都列出来，数量会非常大。  
- **空间**：除了存放答案的集合外，只用了常数级别的额外变量。集合里最多有 `26*26 = 676` 种不同的回文（因为首尾只能是 26 个字母中的一种，中心也是 26 种），所以空间是 **O(1)**（常数级）  

#### 代码（Python）  

```python
def countPalindromicSubsequence_bruteforce(s: str) -> int:
    n = len(s)
    seen = set()                     # 用来去重的集合
    for i in range(n):               # 第一个字符的位置
        for j in range(i + 1, n):    # 第二个字符的位置
            for k in range(j + 1, n):# 第三个字符的位置
                if s[i] == s[k]:     # 首尾相同才是回文
                    seen.add(s[i] + s[j] + s[k])
    return len(seen)
```

> 关键行中文注释已写在代码里，直接复制跑就行。  

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 随着字符串长度增长，检查的组合数会呈立方增长。  
- **空间复杂度**：`O(1)` —— 最多只会保存 676 条不同的回文，视作常数空间。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **三层循环**，我们需要把检查的次数从 `n³` 降到 **线性**（`O(n)`）或 **线性乘常数**（`O(26·n)`）。  

观察回文的结构：长度为 3 的回文一定是形如 **`a ? a`**（首尾相同，中间可以是任意字符）。  
所以，只要我们知道 **在某个位置左边出现了哪些字符**，以及 **在右边出现了哪些字符**，就可以直接判断是否能形成 `a ? a`。  

具体步骤：

1. **前缀出现表** `left[i][c]`：在下标 `i` 之前（不包括 `i`）字符 `c`（0‑25）出现过多少次。  
   - 只需要记录是否出现过，布尔值即可，用 `int` 位掩码也可以。  
2. **后缀出现表** `right[i][c]`：在下标 `i` 之后（不包括 `i`）字符 `c` 出现过多少次。  
   - 同样只关心“出现过没”。  

有了这两个表，遍历一次字符串的每个位置 `j`（作为回文的中间字符），  
- 设 `mid = s[j]`。  
- 看左边有没有字符 `a`（`a` 可以是 26 个字母中的任意一个）出现，右边有没有同样的字符 `a` 出现。  
- 只要左、右各出现一次，就能构造出回文 `a mid a`。  

因为字母表只有 26 种，遍历所有 `a` 的成本是常数。  

**实现细节**  

- 用 **位掩码**（整数的二进制位）来压缩 26 个布尔值，省空间也省时间。  
  - `mask_left` 在遍历时不断 `|= 1 << (ord(s[i]) - ord('a'))`。  
  - `mask_right` 先一次性统计全部字符出现的位掩码，然后在遍历时把当前字符对应的位从 `mask_right` 中移除。  
- 对每个中间位置 `j`，用 `mask_left & mask_right` 得到左、右都出现的字符集合。  
  - 统计这个交集中有多少个位为 1，即有多少不同的字符 `a` 能形成回文。  
  - 直接把计数累加到答案中。  

**为什么正确**：  
- 对每个中间字符 `mid`，我们枚举所有可能的首尾字符 `a`。  
- 只要左侧出现过 `a` 且右侧出现过 `a`，必然能挑选出一个左边的 `a`、中间的 `mid`、右边的 `a`，形成合法的子序列。  
- 由于我们对每个 `a` 只计数一次（交集的位只会出现一次），自然实现了“唯一计数”。  

**复杂度分析（大白话）**：  
- **时间**：我们只遍历字符串一次（`O(n)`），每次只检查 26 次（常数），所以整体是 **O(n)**。  
- **空间**：只用了几个整数保存位掩码，空间是 **O(1)**。  

#### 代码（Python）  

```python
def countPalindromicSubsequence(s: str) -> int:
    """
    返回长度为 3 的不同回文子序列个数
    思路：使用左侧/右侧出现字符的位掩码，线性扫描
    """
    n = len(s)
    # 右侧出现的字符集合，初始时把所有字符都加入
    mask_right = 0
    for ch in s:
        mask_right |= 1 << (ord(ch) - ord('a'))

    mask_left = 0          # 左侧出现的字符集合，开始为空
    ans = 0                # 最终答案

    for j, ch in enumerate(s):
        # 当前字符不再算作右侧，先把它从右侧掩码中移除
        mask_right &= ~(1 << (ord(ch) - ord('a')))

        # left & right 得到两侧都出现过的字符集合
        common = mask_left & mask_right

        # 统计 common 中有多少个位为 1（即有多少不同的字符 a）
        # Python 的 bit_count() 能直接返回二进制中 1 的个数（Python3.8+ 可用 bin(...).count('1')）
        ans += common.bit_count()

        # 把当前字符加入左侧集合，为后面的中间字符做准备
        mask_left |= 1 << (ord(ch) - ord('a'))

    return ans
```

> **关键行解释**  
> - `mask_right |= 1 << idx`：把字符对应的位设为 1，表示“右侧出现”。  
> - `mask_right &= ~(... )`：把当前位置的字符从右侧集合中剔除，因为它已经不在“右边”了。  
> - `common = mask_left & mask_right`：只保留左、右都出现的字符。  
> - `common.bit_count()`：统计有多少种不同的字符可以作为首尾。  

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，内部操作是常数。  
- **空间复杂度**：`O(1)` —— 使用固定个数的整数（位掩码），不随 `n` 增长。  

---  

## 心得  

- **核心技巧**：利用字符出现的**前缀/后缀信息**以及**位掩码**快速判断左、右两侧是否都有某个字符。  
- **适用题型**：  
  1. “统计唯一子序列/子串” 类问题（如 “Unique Substrings of Length K”）。  
  2. “左右两端满足某种关系” 的字符串题（如 “Count Good Triplets”）。  
  3. 需要快速判断字符集合交集的场景（如 “Maximum Subarray with Minimum Deletions”）。  
- **一句话总结解题钥匙**：**把“左侧出现什么”和“右侧出现什么”预处理成位掩码，交集的位数就是可构成的不同回文数**。  

---  

## 反思  

- **第一反应**：看到“长度 3 的回文子序列”，立刻想到枚举所有三元组，写出暴力代码。  
- **最容易踩的坑**：  
  - 忘记去重，导致同一个回文被计多次。  
  - 只检查 `s[i] == s[k]` 而忽略了 `j` 必须在 `i` 与 `k` 之间（但遍历三层循环自然保证了顺序）。  
  - 在位掩码实现时，忘记在遍历时把当前字符从右侧集合中剔除，会把同一字符算两次。  
- **下次遇到类似题**，第一步应**先思考字符的出现位置（左/右）能否用前缀/后缀信息压缩**，而不是直接暴力枚举。这样往往能把指数级的复杂度降到线性级。