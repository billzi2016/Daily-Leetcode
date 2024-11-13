# #2937. 使三个字符串相等 / Make Three Strings Equal

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/make-three-strings-equal/)

---

## 题目（英文原版）

**Description**

You are given three strings: s1, s2, and s3. In one operation you can choose one of these strings and delete its rightmost character. Note that you cannot completely empty a string.
Return the minimum number of operations required to make the strings equal. If it is impossible to make them equal, return -1.

**Examples**

**Example 1:**

```
Input: s1 = "abc", s2 = "abb", s3 = "ab"
Output: 2
Explanation: Deleting the rightmost character from both s1 and s2 will result in three equal strings.
```

**Example 2:**

```
Input: s1 = "dac", s2 = "bac", s3 = "cac"
Output: -1
Explanation: Since the first letters of s1 and s2 differ, they cannot be made equal.
```

**Constraints**

- 1 <= s1.length, s2.length, s3.length <= 100
- s1, s2 and s3 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定三个字符串（string）：`s1`、`s2` 和 `s3`。在一次操作（operation）中，你可以选择其中的任意一个字符串并删除它最右侧的字符。注意，**不能**将字符串删除至空字符串。返回使这三个字符串相等所需的最少操作次数。如果无法使它们相等，返回 `-1`。

**示例 1**  
**输入**: `s1 = "abc"`, `s2 = "abb"`, `s3 = "ab"`  
**输出**: `2`  
**解释**: 删除 `s1` 和 `s2` 的最右侧字符后，三个字符串均相等。

**示例 2**  
**输入**: `s1 = "dac"`, `s2 = "bac"`, `s3 = "cac"`  
**输出**: `-1`  
**解释**: 因为 `s1` 和 `s2` 的首字符不同，无法使它们相等。

**约束条件**  
- `1 <= s1.length, s2.length, s3.length <= 100`  
- `s1、s2 和 s3` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把三条字符串都削到同一个长度**，只要削到的长度对应的前缀相同，三条字符串就相等了。  
我们可以枚举所有可能的“目标长度” `len_target`（从 1 到三条字符串最短的长度），  
- 对每个 `len_target`，取三条字符串的前 `len_target` 个字符，判断这三个前缀是否完全相同。  
- 如果相同，就可以把每条字符串删掉多余的字符，使它们都只剩下这个前缀。  
- 需要的操作次数 = `(len(s1)-len_target) + (len(s2)-len_target) + (len(s3)-len_target)`。  

因为我们是从 **最小长度** 开始枚举的，一旦找到第一个可行的 `len_target`，它一定是 **最长公共前缀的长度**，此时的操作次数最少。  

> **类比**：把三根不同长度的绳子裁成同样长度的绳子，只能从右边剪掉。我们先找出三根绳子都能保留下来的最长公共部分（前缀），然后把多余的部分全部剪掉。

如果遍历完所有 `len_target` 都没有找到相同的前缀，说明三条字符串在最左边的字符就已经不相同，根本无法通过只删右边字符来让它们相等，返回 `-1`。

#### 代码（Python）

```python
def min_operations_bruteforce(s1: str, s2: str, s3: str) -> int:
    # 三条字符串的最短长度，目标长度不可能超过它
    min_len = min(len(s1), len(s2), len(s3))

    # 从最长可能的公共前缀开始检查（从 min_len 倒着遍历更直观）
    for target_len in range(min_len, 0, -1):
        # 取每条字符串的前 target_len 个字符
        pre1 = s1[:target_len]
        pre2 = s2[:target_len]
        pre3 = s3[:target_len]

        # 判断这三个前缀是否完全相同
        if pre1 == pre2 == pre3:
            # 计算需要删除的字符数（每删掉一个字符算一次操作）
            ops = (len(s1) - target_len) + (len(s2) - target_len) + (len(s3) - target_len)
            return ops

    # 没有任何公共前缀（连第一个字符都不同），返回 -1
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（这里的 `n` 代表三条字符串最短的长度）。  
  - 外层循环遍历所有可能的目标长度 `O(n)`，  
  - 内层的切片 `s[:target_len]` 实际上会复制 `target_len` 长度的子串，最坏情况下总共会产生 `1 + 2 + … + n = O(n²)` 次字符拷贝。  
  - 对于本题的约束（`n ≤ 100`），`O(n²)` 完全可以接受。

- **空间复杂度**：`O(n)`。  
  - 每次循环我们会生成三个前缀子串，长度最多为 `n`，因此额外空间随 `n` 线性增长。  

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次都要复制前缀子串，导致 `O(n²)` 的时间。  
实际上我们只需要找到 **最长公共前缀（Longest Common Prefix, LCP）** 的长度，随后直接用公式算出操作次数即可。

**一步步推导**：

1. **从左到右逐字符比较**  
   - 同时遍历三条字符串的每个位置 `i`（从 `0` 开始），比较 `s1[i]、s2[i]、s3[i]` 是否全部相等。  
   - 如果相等，说明这个字符可以保留下来，继续往右检查。  
   - 第一次出现不相等的地方，就说明公共前缀到此为止，长度为 `i`。  

2. **特殊情况**  
   - 如果在检查到最短字符串的末尾仍然全部相等，则公共前缀长度等于最短字符串的长度。  
   - 如果一开始就不相等（即 `i == 0`），说明没有公共前缀，题目要求返回 `-1`。  

3. **算操作次数**  
   - 已知最长公共前缀长度 `lcp_len`，每条字符串需要删除的字符数就是 `len(si) - lcp_len`。  
   - 三条相加即为最少的操作次数。  

> **类比**：把三根绳子对齐在左边，从左往右逐段检查颜色是否相同，只要颜色相同就可以保留。遇到第一段颜色不一样，就停下来，左边保留下来的那段就是最长公共前缀。  

#### 代码（Python）

```python
def min_operations_optimal(s1: str, s2: str, s3: str) -> int:
    # 找到三条字符串的最短长度，比较只能进行到这里
    min_len = min(len(s1), len(s2), len(s3))

    # 计算最长公共前缀的长度
    lcp_len = 0
    while lcp_len < min_len and s1[lcp_len] == s2[lcp_len] == s3[lcp_len]:
        lcp_len += 1

    # 如果没有公共前缀（lcp_len == 0），按照题意返回 -1
    if lcp_len == 0:
        return -1

    # 公式直接算出最少的删除次数
    return (len(s1) - lcp_len) + (len(s2) - lcp_len) + (len(s3) - lcp_len)
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 只遍历一次，最多检查到最短字符串的长度 `n`，每次比较三个字符是常数时间。  
  - 相比暴力的 `O(n²)`，大幅提升。

- **空间复杂度**：`O(1)`。  
  - 只使用了若干整数变量，没有额外随输入规模增长的存储。

---

## 心得

- **核心技巧**：**最长公共前缀（LCP）** 的概念与线性遍历。  
- **适用的题型**：  
  1. “使两字符串相等，只能删除后缀” 类似题（如 *Make Two Strings Equal*）。  
  2. “找出多个字符串的公共前缀” 的变体（如 LeetCode 14 *Longest Common Prefix*）。  
- **解题钥匙**：**只要比较左边的字符，右边的字符永远可以被删掉**——所以问题归结为找左边的最长相同部分。

---

## 反思

- **第一反应**：想到“把多余的字符都删掉”，于是自然会去枚举所有可能的目标长度。  
- **最容易踩的坑**：  
  - 忘记题目要求**不能把字符串删空**，所以公共前缀长度为 `0` 时必须返回 `-1`。  
  - 在实现暴力解时，切片复制会导致不必要的时间浪费。  
- **下次遇到同类题**：第一步先**找最长公共前缀**，再用 **总长度 - 3 × 前缀长度** 直接算答案。这样既简洁又高效。