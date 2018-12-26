# #214. 最短回文串 / Shortest Palindrome

> 难度：困难 · 标签：String、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/shortest-palindrome/)

---

## 题目（英文原版）

**Description**

You are given a string s. You can convert s to a palindrome by adding characters in front of it.
Return the shortest palindrome you can find by performing this transformation.

**Examples**

**Example 1:**

```
Input: s = "aacecaaa"
Output: "aaacecaaa"
```

**Example 2:**

```
Input: s = "abcd"
Output: "dcbabcd"
```

**Constraints**

- 0 <= s.length <= 5 * 104
- s consists of lowercase English letters only.

---

## 题目（中文翻译）

给定一个字符串（string）`s`。你可以通过在其前面添加字符来将 `s` 转换为回文串（palindrome）。返回通过执行此转换能够得到的最短回文串。

**示例 1：**
``` 
Input: s = "aacecaaa"
Output: "aaacecaaa"
```

**示例 2：**
``` 
Input: s = "abcd"
Output: "dcbabcd"
```

**约束条件：**
- `0 <= s.length <= 5 * 10^4`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符一个一个往前拼，直到整个字符串变成回文**。  
我们可以从原串 `s` 的最左侧开始检查，找出最长的“前缀回文”（即从第 `0` 位到第 `i` 位已经是回文的子串）。  
* 如果整个 `s` 本身已经是回文，直接返回 `s`。  
* 否则，设最长前缀回文的长度为 `len_pre`，则 `s[len_pre:]`（剩下的后缀）需要全部倒序挂在最前面，才能得到最短回文。

> **类比**：想象一面镜子只能放在字符串的左边，你先把能直接映出自己的那段（前缀回文）找出来，剩下的部分只能“翻转后”贴到左侧去。

**暴力检查前缀是否回文** 的方式是：对每个可能的前缀 `s[:i+1]`，用双指针从两端向中间比较字符是否相同。找到最长的满足条件的前缀后，按上面的规则拼接即可。

#### 代码（Python）

```python
def shortestPalindrome_brute(s: str) -> str:
    # ---------- 辅助函数：判断子串是否为回文 ----------
    def is_palindrome(sub: str) -> bool:
        left, right = 0, len(sub) - 1
        while left < right:
            if sub[left] != sub[right]:
                return False
            left += 1
            right -= 1
        return True

    n = len(s)
    if n <= 1:                     # 空串或单字符本身就是回文
        return s

    # 从最长前缀开始往短的方向尝试，找到第一个回文前缀
    for i in range(n, 0, -1):      # i 表示前缀长度
        if is_palindrome(s[:i]):   # 检查 s[0:i] 是否回文
            # 把剩余的后缀倒序拼到最前面
            suffix_rev = s[i:][::-1]   # s[i:] 是后缀，[::-1] 翻转
            return suffix_rev + s

    # 理论上不会走到这里，因为 i=1 时一定是回文（单字符）
    return s
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 外层循环最多遍历 `n` 次（尝试每一种前缀长度），  
  - 内层的 `is_palindrome` 最坏要比较 `O(n)` 次字符。  
  - 所以整体是 “n × n”，也就是 `n²`，对应的实际意义是：如果字符串长度是 10,000，算法大概要做 100,000,000 次字符比较，可能会超时。

- **空间复杂度**：`O(1)`（不计返回结果的额外空间）  
  - 只用了几个指针变量，未额外申请与 `n` 相关的数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历前缀检查回文**，导致二次循环。  
我们需要一次遍历就能得到“最长前缀回文的长度”。这正好可以借助 **字符串匹配中的 KMP（Knuth-Morris-Pratt）算法** 的 “前缀函数（next / lps）”。  

**关键观察**  
把原串 `s` 与它的逆序 `rev = s[::-1]` 拼成 `combined = s + "#" + rev`（`#` 是一个不可能出现在 `s` 中的分隔符）。  
在 `combined` 中，**最长的相同前后缀**（即前缀函数的最大值）恰好等于 `s` 的最长回文前缀的长度。原因如下：

1. 前缀 `s[0:len]` 与后缀 `rev[-len:]`（即原串后缀的逆序）相同，说明 `s[0:len]` 正好是回文（正着和倒着一样）。
2. KMP 的前缀函数 `lps[i]` 给出 `combined[0:i]` 的最长相同前后缀长度，遍历完整个 `combined`，最后的 `lps[-1]` 就是我们要的最长回文前缀长度。

得到 `len_pre = lps[-1]` 后，**只需要把 `s[len_pre:]` 的逆序放到最前**，即：

```
answer = rev[:len(s)-len_pre] + s
```

> **类比**：把原串和它的镜像拼在一起，用一根尺子从左到右滑动，尺子每走一步就记录“已经匹配了多长”。尺子最后停下的最长匹配，就是左边那段可以直接成为回文的部分。

#### KMP 前缀函数（从零解释）

- `lps[i]`（Longest Prefix which is also Suffix）表示 **子串 `combined[0..i]`** 的**最长的既是前缀又是后缀**的长度（不包括整个子串本身）。
- 计算时维护两个指针：`i` 正在遍历字符串，`j` 表示当前匹配的前缀长度。
- 当 `combined[i] == combined[j]`，说明可以把匹配长度加一（`j += 1`），并把 `lps[i] = j`。
- 当不相等时，利用已经算好的 `lps[j-1]` 回退 `j`，尝试更短的前缀，直到 `j` 为 `0` 为止。

这样只需一次线性遍历，就得到全部 `lps`，时间 `O(n)`。

#### 代码（Python）

```python
def shortestPalindrome_kmp(s: str) -> str:
    if not s or len(s) == 1:          # 空串或单字符直接返回
        return s

    rev = s[::-1]                     # 逆序字符串
    # 组合字符串，# 充当分隔符，防止跨界匹配
    combined = s + "#" + rev

    # ---------- 计算 KMP 的前缀函数 ----------
    n = len(combined)
    lps = [0] * n                     # lps[i] 初始化为 0
    j = 0                             # 当前匹配的前缀长度

    for i in range(1, n):
        # 当字符不匹配且 j > 0 时，利用 lps 回退
        while j > 0 and combined[i] != combined[j]:
            j = lps[j - 1]            # 回到更短的前缀

        # 若匹配成功，前缀长度加一
        if combined[i] == combined[j]:
            j += 1
            lps[i] = j                # 记录当前位置的最长前后缀长度
        # 若仍不匹配且 j == 0，则 lps[i] 保持 0（默认）

    # lps[-1] 即为 s 的最长回文前缀长度
    len_pre = lps[-1]

    # 把 s 剩余的后缀倒序拼到最前面
    # rev[:len(s)-len_pre] 正好是 s[len_pre:] 的逆序
    return rev[:len(s) - len_pre] + s
```

#### 复杂度

- **时间复杂度**：`O(n)`（线性）  
  - 只遍历了一遍 `combined`（长度约为 `2n+1`），每个字符的比较、指针移动次数都是常数级别。  
  - 与暴力解的 `n²` 相比，**即使 `n=5·10⁴` 也能在毫秒级完成**。

- **空间复杂度**：`O(n)`（线性）  
  - 需要额外存储 `rev`（长度 `n`）和 `lps`（长度约 `2n`），属于与输入规模同阶的额外空间。  
  - 如果只关心返回值，这已经是最优的空间使用方式。

---

## 心得

- **核心技巧**：把“最长回文前缀”转化为“字符串与其逆序的最长相同前后缀”，利用 KMP 前缀函数在 `O(n)` 时间内求解。  
- **适用场景**：  
  1. **构造最短回文**（本题）。  
  2. **字符串循环移位匹配**（如 LeetCode 796 `Rotate String`）。  
  3. **寻找最长回文子串的中心扩展**（虽然实现不同，但相同的“前后缀匹配”思路常出现）。  
- **一句话总结**：**把原串和逆序拼在一起，用 KMP 找最长前后缀，即得到可直接保留的回文前缀**。

---

## 反思

- **第一反应**：直接倒着把所有字符都加到前面，随后想办法去掉多余的字符，结果想到“只加不需要的那部分”。  
- **最容易踩的坑**：  
  - 忘记在拼接时加入不可能出现的分隔符 `#`，导致跨界匹配错误。  
  - 对空串或长度为 1 的字符串未做特判，会让 `lps[-1]` 为 0，仍能得到正确答案，但代码可读性下降。  
  - 误以为 `lps[i]` 必须等于 `i+1` 才算回文前缀，实际只要是最长的前后缀即可。  
- **下次遇到同类题**：**先思考是否能把“回文”转化为“前后缀相等”，再考虑使用 KMP（或滚动哈希）一次遍历求解**。这样可以快速定位瓶颈并选取线性时间的解法。