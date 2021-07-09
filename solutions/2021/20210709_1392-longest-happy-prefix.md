# #1392. **最长快乐前缀** / Longest Happy Prefix

> 难度：困难 · 标签：String、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/longest-happy-prefix/)

---

## 题目（英文原版）

**Description**

A string is called a happy prefix if is a non-empty prefix which is also a suffix (excluding itself).
Given a string s, return the longest happy prefix of s. Return an empty string "" if no such prefix exists.

**Examples**

**Example 1:**

```
Input: s = "level"
Output: "l"
Explanation: s contains 4 prefix excluding itself ("l", "le", "lev", "leve"), and suffix ("l", "el", "vel", "evel"). The largest prefix which is also suffix is given by "l".
```

**Example 2:**

```
Input: s = "ababab"
Output: "abab"
Explanation: "abab" is the largest prefix which is also suffix. They can overlap in the original string.
```

**Constraints**

- 1 <= s.length <= 105
- s contains only lowercase English letters.

---

## 题目（中文翻译）

一个字符串如果是**非空前缀（prefix）**且同时也是**后缀（suffix）**（不包括整个字符串本身），则称其为**快乐前缀（happy prefix）**。  
给定字符串 `s`，返回 `s` 的最长快乐前缀。如果不存在满足条件的前缀，返回空字符串 `""`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1**  
```
Input: s = "level"
Output: "l"
Explanation: s 有 4 个除自身外的前缀（"l", "le", "lev", "leve"），以及相应的后缀（"l", "el", "vel", "evel"）。其中既是前缀又是后缀的最长字符串为 "l"。
```

**示例 2**  
```
Input: s = "ababab"
Output: "abab"
Explanation: "abab" 是最长的既是前缀又是后缀的字符串。它们在原字符串中可以出现重叠。
```

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：  
1. 从字符串的最长可能前缀开始检查（长度为 `len(s)-1`），往前逐渐缩短。  
2. 对每一个前缀，判断它是否同样出现在字符串的结尾（作为后缀）。  
   - 前缀就像把一根绳子从左边剪下一段，后缀则是从右边剪下一段。我们只要看这两段内容是否完全相同即可。  
3. 第一次遇到相同的前缀/后缀，就是最长的 “happy prefix”。  

为什么正确？  
- 题目要求的前缀必须是 **非空且不等于整个字符串**，所以我们只需要遍历所有合法的前缀长度。  
- 只要找到了一个长度 `L` 的前缀等于后缀，所有更短的前缀自然也会满足（因为它们是前缀的子串），但我们只关心最长的那个，所以从长到短枚举即可。

#### 代码（Python）  
```python
def longest_happy_prefix_brute(s: str) -> str:
    n = len(s)
    # 从最长可能的前缀（长度 n-1）开始往前检查
    for L in range(n - 1, 0, -1):          # L 为前缀的长度
        prefix = s[:L]                     # 前缀：左边的 L 个字符
        suffix = s[-L:]                    # 后缀：右边的 L 个字符
        # 判断两段是否相同
        if prefix == suffix:
            return prefix                  # 找到最长的 happy prefix
    return ""                              # 没有任何符合条件的前缀
```

#### 复杂度  
- **时间复杂度**：`O(n²)`  
  - 外层循环最多遍历 `n-1` 次，内层的字符串切片和比较在最坏情况下要比较 `L`（≈`n`）个字符，整体相当于 `1 + 2 + … + n ≈ n²/2`。  
  - 用大白话说，若字符串长度是 10,000，程序大约要做 100,000,000 次字符比较，速度会很慢。  
- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  - 只用了几个整数变量和两个切片引用，额外占用的内存几乎不变。

---

### 2. 最优解  

#### 思路  
暴力解慢的根源在于**每次都重新比较整段子串**。我们可以把“前缀是否等于后缀”这个判断，转化为“两个子串的哈希值是否相等”，或者使用 **KMP（Knuth–Morris–Pratt）** 的**前缀函数**（也叫 “最长相等前后缀表”）一次性算出所有前缀‑后缀的匹配长度。

这里采用 KMP 思路，因为它只需要线性时间 `O(n)`，而且不涉及哈希冲突的问题。  

**KMP 前缀函数**的定义  
- 对于字符串 `s[0…i]`（长度为 `i+1`），`pi[i]` 表示 **最长的真前缀**（不包括完整字符串本身）同时也是该子串的 **真后缀** 的长度。  
- 例如 `s = "ababa"`，`pi = [0,0,1,2,3]`，说明 `s[:3]="aba"` 的最长相等前后缀长度是 1（即 "a"）。

关键观察  
- 整个字符串 `s` 的 `pi[-1]`（最后一个位置的值）恰好是 **整个字符串的最长相等前后缀** 的长度。  
- 如果 `pi[-1]` 为 0，说明没有任何非空前缀是后缀，直接返回空串。  
- 否则，`s[:pi[-1]]` 就是答案。

**如何线性计算前缀函数**（从零开始解释）  
1. 用两个指针 `i`（当前遍历的位置）和 `j`（当前已匹配的前缀长度）。  
2. 初始 `i = 1, j = 0`（第一个字符没有前缀）。  
3. 若 `s[i] == s[j]`，说明可以把前缀再延长一位：`j += 1`，把 `j` 记入 `pi[i]`，`i += 1`。  
4. 若不相等，说明已经不能继续匹配，需要把 `j` 回退到 `pi[j-1]`（即把已匹配的前缀再压缩成它自己的最长相等前后缀），继续比较。  
5. 当 `j` 退到 0 仍不相等时，说明 `i` 位置的字符本身没有匹配的前缀，`pi[i] = 0`，`i += 1`。  

这个过程每个字符最多被“指针 `i`”访问一次，`j` 也只会向左回退，整体是 `O(n)`。

#### 代码（Python）  
```python
def longest_happy_prefix_kmp(s: str) -> str:
    n = len(s)
    # pi[i] 表示 s[:i+1] 的最长相等前后缀长度
    pi = [0] * n
    j = 0  # 当前已匹配的前缀长度

    # 从第二个字符开始遍历（i=1），因为第一个字符没有真前缀
    for i in range(1, n):
        # 当出现不匹配时，尝试把已匹配的前缀长度 j 缩小
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]      # 回退到上一个可能的匹配长度
        # 如果匹配成功，前缀长度加 1
        if s[i] == s[j]:
            j += 1
            pi[i] = j
        # 若仍不匹配且 j == 0，pi[i] 保持 0（默认值），继续下一位

    # pi[-1] 即为整个字符串的最长相等前后缀长度
    longest_len = pi[-1]
    return s[:longest_len]   # 长度为 0 时自动返回空串
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，内部的 `while` 循环在所有迭代中累计最多也只会向左移动 `j` 不超过 `n` 次。  
  - 用大白话说，长度为 100,000 的字符串只会做大约 200,000 次字符比较，几乎是线性的，跑得非常快。  
- **空间复杂度**：`O(n)`  
  - 需要额外的数组 `pi` 来保存每个位置的前缀长度，大小正好和原字符串等长。  
  - 如果只需要返回结果而不保留整个表，也可以在遍历时只保留最后一个值，进一步压缩到 `O(1)`（这里为了讲解完整性保留数组）。

---

## 心得  

- **核心技巧**：**KMP 前缀函数**（最长相等前后缀），它把“找相同前缀/后缀”转化为一次线性扫描的问题。  
- **适用的题型**  
  1. **寻找字符串的最长重复前后缀**（本题、LeetCode 1477 `Find the Shortest Superstring` 中的子问题）。  
  2. **字符串匹配**：在一个大文本中搜索模式串（经典 KMP 用法）。  
  3. **周期性判断**：判断一个字符串是否由若干次相同子串重复构成（如 LeetCode 459 `Repeated Substring Pattern`）。  
- **一句话总结**：**“把前后缀匹配转化为前缀函数的递推，一次遍历搞定最长 happy prefix”。**

---

## 反思  

- **第一反应**：看到“前缀 = 后缀”，自然想到“枚举所有可能的长度并直接比较”。这就是暴力思路。  
- **最容易踩的坑**  
  1. **遗漏空串的情况**：当没有任何匹配时，需要返回 `""`，而不是 `None` 或报错。  
  2. **前缀不能是整个字符串本身**：一定要把长度上限设为 `n-1`（暴力）或使用 KMP 的“真前缀”。  
  3. **回退过程写错**：在 KMP 中，`while j > 0 and s[i] != s[j]` 必须放在最前面，否则会出现无限循环。  
- **下次遇到同类题**，第一步应该先问自己：“是否可以用前缀函数/后缀数组一次性得到所有前缀‑后缀的匹配信息？” 若答案是肯定的，就直接走 KMP 或 Z‑algorithm 的路线。