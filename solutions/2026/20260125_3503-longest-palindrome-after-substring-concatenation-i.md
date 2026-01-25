# #3503. 子串拼接后的最长回文 I / Longest Palindrome After Substring Concatenation I

> 难度：中等 · 标签：Two Pointers、String、Dynamic Programming、Enumeration · [LeetCode 链接](https://leetcode.com/problems/longest-palindrome-after-substring-concatenation-i/)

---

## 题目（英文原版）

**Description**

You are given two strings, s and t.
You can create a new string by selecting a substring from s (possibly empty) and a substring from t (possibly empty), then concatenating them in order.
Return the length of the longest palindrome that can be formed this way.

**Examples**

**Example 1:**

```
Input: s = "a", t = "a"
Output: 2
Explanation:
Concatenating "a" from s and "a" from t results in "aa" , which is a palindrome of length 2.
```

**Example 2:**

```
Input: s = "abc", t = "def"
Output: 1
Explanation:
Since all characters are different, the longest palindrome is any single character, so the answer is 1.
```

**Example 3:**

```
Input: s = "b", t = "aaaa"
Output: 4
Explanation:
Selecting " aaaa " from t is the longest palindrome, so the answer is 4.
```

**Example 4:**

```
Input: s = "abcde", t = "ecdba"
Output: 5
Explanation:
Concatenating "abc" from s and "ba" from t results in "abcba" , which is a palindrome of length 5.
```

**Constraints**

- 1 <= s.length, t.length <= 30
- s and t consist of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定两个字符串 `s` 和 `t`。  
你可以先从 `s` 中选取一个子串（substring）（可以为空），再从 `t` 中选取一个子串（substring）（可以为空），随后按选取的顺序将它们拼接成一个新字符串。  
返回能够得到的最长回文（palindrome）的长度。

**示例 1**  
**输入**: `s = "a", t = "a"`  
**输出**: `2`  
**解释**:  
将 `s` 中的 `"a"` 与 `t` 中的 `"a"` 拼接得到 `"aa"`，它是长度为 2 的回文。

**示例 2**  
**输入**: `s = "abc", t = "def"`  
**输出**: `1`  
**解释**:  
由于所有字符都不同，最长的回文只能是任意单个字符，答案为 1。

**示例 3**  
**输入**: `s = "b", t = "aaaa"`  
**输出**: `4`  
**解释**:  
从 `t` 中选择子串 `"aaaa"`，它本身就是回文，长度为 4。

**示例 4**  
**输入**: `s = "abcde", t = "ecdba"`  
**输出**: `5`  
**解释**:  
将 `s` 中的子串 `"abc"` 与 `t` 中的子串 `"ba"` 拼接得到 `"abcba"`，它是长度为 5 的回文。

**约束条件**  
- `1 <= s.length, t.length <= 30`  
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的选择全部枚举一遍，然后检查得到的字符串是否是回文。  

- **子串**：在字符串里连续的一段字符。  
  - 把 `s` 的所有子串列出来（包括空串），记作 `sub_s`。  
  - 把 `t` 的所有子串列出来（包括空串），记作 `sub_t`。  
- **拼接**：把 `sub_s` 放在前面，`sub_t` 放在后面，得到 `cand = sub_s + sub_t`。  
- **回文检测**：把 `cand` 从左往右读一遍，再从右往左读一遍，如果两遍完全相同，则 `cand` 是回文。  

> **类比**：把“字典”想象成一个装有所有子串的抽屉，抽屉里每一本书都是一种子串。我们把 `s` 的一本书和 `t` 的一本书拼在一起，看看能不能拼出一面“对称的镜子”。如果能，对称的长度就是答案。

因为题目要求 **最长** 的回文长度，我们只要在遍历的过程中保存最大的长度即可。

**为什么正确**  
- 我们遍历了 **所有** 可能的 `sub_s` 与 `sub_t`（包括空串），所以任何合法的拼接方式一定会被检查到。  
- 只要检查到了回文，就更新答案，最后得到的就是最长的回文长度。

**复杂度分析（大白话）**  

- `s` 长度记作 `n`，`t` 长度记作 `m`（均 ≤ 30）。  
- `s` 的子串数是 `n·(n+1)/2`（想象把 `n` 根棍子两两搭配，得到的组合数），同理 `t` 的子串数是 `m·(m+1)/2`。  
- 对每一对子串，我们要把它们拼起来检查回文，检查的时间是拼接后字符串的长度，最多 `n+m`。  

于是总时间是  

```
O( (n²) * (m²) * (n+m) )   ≈   O(n²·m²)      （因为 n,m ≤ 30，常数很小）
```

- **空间**：只保存几个临时字符串，最多 `n+m` 长度，属于 **O(n+m)**，即 **O(1)** 额外空间。

#### 代码（Python）

```python
def longestPalindromeAfterConcat_bruteforce(s: str, t: str) -> int:
    n, m = len(s), len(t)

    # ---------- 生成所有子串（包括空串） ----------
    subs_s = ['']                     # 先放空串
    for i in range(n):
        for j in range(i + 1, n + 1):
            subs_s.append(s[i:j])    # s[i:j] 是左闭右开区间

    subs_t = ['']
    for i in range(m):
        for j in range(i + 1, m + 1):
            subs_t.append(t[i:j])

    # ---------- 暴力检查 ----------
    ans = 0
    for a in subs_s:                  # 遍历 s 的每个子串
        for b in subs_t:              # 遍历 t 的每个子串
            cand = a + b              # 拼接
            # 判断 cand 是否是回文
            if cand == cand[::-1]:    # Python 的切片逆序非常简洁
                ans = max(ans, len(cand))

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²·m²)`  
  - 这里的 `n²` 来自 `s` 所有子串的数量，`m²` 来自 `t` 的子串数量，内部的回文检测是常数级（因为长度 ≤ 60），所以整体是平方乘积。  
- **空间复杂度**：`O(1)`（不计输出列表的存储，实际只用了几个临时字符串）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **两层子串枚举**：  
- `s` 有 `≈ n²/2` 个子串，`t` 也有 `≈ m²/2` 个子串。  
- 两个 `for` 循环的乘积导致 **四次方** 的时间。

观察题目可以发现，**回文的结构非常有规律**：

1. **完全位于单个字符串** 的情况：  
   - 只取 `s`（或只取 `t`）的子串，这相当于求 `s`（或 `t`）的最长回文子串。  
2. **跨越边界的情况**（即左半段取自 `s`，右半段取自 `t`）：  
   - 回文的左半段（从左到右）全部来自 `s` 的 **后缀**，  
   - 回文的右半段（从右到左）全部来自 `t` 的 **前缀**，并且这两段必须互为逆序。  

> **类比**：想象把 `s` 放在左边，`t` 放在右边。要让整个拼接成镜子，左边的镜子边缘（`s` 的后缀）必须正好映射到右边的镜子边缘（`t` 的前缀）的倒影。  

因此跨界回文的核心是：  
> 在 `s` 中找一个后缀 `x`，在 `t` 中找一个前缀 `y`，要求 `x == reverse(y)`。

只要找到了这样一对匹配的子串 `x`（长度 `k`），我们就可以在它们中间再放一个 **任意的回文**（可以来自 `s`、`t`，甚至是空串），于是总长度为  

```
total_len = 2 * k + middle_len
```

其中 `middle_len` 是 **单独在 s 或 t 中能够取得的最长回文子串的长度**（因为我们可以把中间的那段全部选自某一个字符串，空串也是合法的）。

所以问题化简为：

1. 求 `s`、`t` 各自的最长回文子串长度，记作 `best_s`、`best_t`。  
2. 求 `s` 的所有后缀 与 `t` 的所有前缀 的最长公共子串长度（要求前缀逆序后匹配后缀），记作 `k_max`。  
3. 最终答案 = `max(best_s, best_t, 2 * k_max + max(best_s, best_t))`  

其实第 3 步可以写成 `max(best_s, best_t, 2 * k_max + max(best_s, best_t))`，但更直接的写法是：

```
ans = max(best_s, best_t)                     # 只用单个字符串的情况
for each possible matching length k:
    ans = max(ans, 2*k + max(best_s, best_t)) # 跨界加上中间的最长回文
```

**如何高效求匹配长度 `k_max`**  

把 `t` 逆序记作 `rt = t[::-1]`。  
`x == reverse(y)` 等价于 `x` 与 `rt` 的某个子串相等。  
于是我们只要在 `s` 与 `rt` 之间找 **最长公共子串**（连续匹配），但要求 `x` 必须是 `s` 的 **后缀**，`y` 必须是 `t` 的 **前缀**（即 `rt` 的 **后缀**）。  

实现方法：

- 枚举 `s` 中每个位置 `i` 作为后缀的起点（即子串 `s[i:]`）。  
- 同时枚举 `rt` 中每个位置 `j` 作为后缀的起点（对应 `t` 前缀的逆序）。  
- 用两指针向右同时比较字符，只要相等就继续，记录最长的匹配长度。  

因为 `|s|,|t| ≤ 30`，双层循环 `O(n·m)`（最多 900 次）足够快，且每次比较最多 `min(n-i, m-j)` 步，总体仍是 `O(n·m)`。

**步骤汇总**  

1. **预处理**  
   - `best_s` = 长度最长的回文子串（在 `s` 中）。  
   - `best_t` = 长度最长的回文子串（在 `t` 中）。  
   - `rt = t[::-1]`（把 `t` 反转）。  

2. **最长公共后缀**（对应跨界匹配）  
   ```text
   k_max = 0
   for i in range(len(s)):
       for j in range(len(rt)):
           cur = 0
           while i+cur < len(s) and j+cur < len(rt) and s[i+cur] == rt[j+cur]:
               cur += 1
           k_max = max(k_max, cur)
   ```  

3. **答案合并**  
   ```text
   ans = max(best_s, best_t)                # 只用单个字符串
   ans = max(ans, 2*k_max + max(best_s, best_t))  # 跨界 + 最佳中间
   ```

这就是 **O(n·m)** 时间、**O(1)** 额外空间的最优解。

#### 代码（Python）

```python
def longestPalindromeAfterConcat(s: str, t: str) -> int:
    """最优解：时间 O(|s|·|t|)，空间 O(1)"""
    n, m = len(s), len(t)

    # ---------- 1. 单字符串内部的最长回文子串 ----------
    def longest_pal_substring(st: str) -> int:
        """Manacher 或 DP 都可以，这里用中心扩展，O(len²) 但 len≤30，足够快"""
        L = len(st)
        best = 0
        for center in range(L):
            # 奇数长度，以 center 为中心
            l = r = center
            while l >= 0 and r < L and st[l] == st[r]:
                best = max(best, r - l + 1)
                l -= 1
                r += 1
            # 偶数长度，以 center 与 center+1 为中心
            l, r = center, center + 1
            while l >= 0 and r < L and st[l] == st[r]:
                best = max(best, r - l + 1)
                l -= 1
                r += 1
        return best

    best_s = longest_pal_substring(s)
    best_t = longest_pal_substring(t)

    # ---------- 2. 跨界匹配：s 的后缀 与 t 的前缀 ----------
    rt = t[::-1]                     # t 的逆序
    k_max = 0                        # 记录最长匹配长度

    for i in range(n):               # s 后缀的起点
        for j in range(m):           # rt（即 t 前缀逆序）的起点
            cur = 0
            # 同时向右比较字符，只要相等就继续
            while i + cur < n and j + cur < m and s[i + cur] == rt[j + cur]:
                cur += 1
            if cur > k_max:
                k_max = cur

    # ---------- 3. 合并答案 ----------
    ans = max(best_s, best_t)                     # 只取单个字符串的情况
    ans = max(ans, 2 * k_max + max(best_s, best_t))   # 跨界 + 中间的最佳回文

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n·m)`（最多 30·30 = 900 次字符比较）  
  - 单字符串内部的最长回文采用中心扩展，时间 `O(n² + m²)`，在本题规模下仍然是常数级别。  
  - 与暴力的 `O(n²·m²)` 相比，降低了一个数量级，实际运行毫秒级。

- **空间复杂度**：`O(1)`（只使用若干整数变量和少量临时字符串 `rt`，长度 ≤ 30）  

---

## 心得  

- **核心技巧**：把跨字符串的回文拆解为 “后缀 ↔ 前缀 逆序匹配 + 单字符串内部的最长回文”。  
- **适用场景**：  
  1. 两个字符串拼接后要求整体回文（如本题、`Longest Palindrome After Substring Concatenation II`）。  
  2. 需要找 **后缀‑前缀** 匹配的场景（如字符串拼接、前后缀相等的判定）。  
  3. 利用 **逆序** 把“左‑右匹配”转化为普通的公共子串问题。  

- **一句话总结**：  
  “把跨界的回文看成‘左边的后缀 = 右边前缀的逆序’，只要找到最长的这种匹配，再加上单串里最大的回文，就是答案。”

---

## 反思  

- **第一反应**：直接把所有子串枚举完再检查回文，写出来很快，但明显会超时（虽然本题数据小还能跑通）。  
- **最容易踩的坑**：  
  - 忘记把空串也算进去（题目允许“可能为空”）。  
  - 只考虑 `s` 的前缀与 `t` 的后缀匹配，实际上是 **后缀‑前缀**，方向写反会找不到答案。  
  - 中间的回文可以来源于 **任意** 一个字符串，不能只取 `s` 或只取 `t`。  
- **下次思路**：  
  1. 先判断是否可以把问题拆成 “内部回文 + 跨界匹配”。  
  2. 把跨界匹配转化为 **公共子串**（或最长公共后缀）的问题，用逆序技巧简化。  
  3. 再把两部分的最长长度取最大。  

这样一步步抽象、简化，就能从暴力走到最优。