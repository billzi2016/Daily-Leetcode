# #1662. 检查两个字符串数组是否等价 / Check If Two String Arrays are Equivalent

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent/)

---

## 题目（英文原版）

**Description**

Given two string arrays word1 and word2, return true if the two arrays represent the same string, and false otherwise.
A string is represented by an array if the array elements concatenated in order forms the string.

**Examples**

**Example 1:**

```
Input: word1 = ["ab", "c"], word2 = ["a", "bc"]
Output: true
Explanation:
word1 represents string "ab" + "c" -> "abc"
word2 represents string "a" + "bc" -> "abc"
The strings are the same, so return true.
```

**Example 2:**

```
Input: word1 = ["a", "cb"], word2 = ["ab", "c"]
Output: false
```

**Example 3:**

```
Input: word1  = ["abc", "d", "defg"], word2 = ["abcddefg"]
Output: true
```

**Constraints**

- 1 <= word1.length, word2.length <= 103
- 1 <= word1[i].length, word2[i].length <= 103
- 1 <= sum(word1[i].length), sum(word2[i].length) <= 103
- word1[i] and word2[i] consist of lowercase letters.

---

## 题目（中文翻译）

给定两个字符串数组 `word1` 和 `word2`，如果这两个数组表示相同的字符串则返回 `true`，否则返回 `false`。  
一个字符串由数组表示，当且仅当把数组中的元素按顺序连接后得到该字符串。

**示例 1**  
**输入**: `word1 = ["ab", "c"]`, `word2 = ["a", "bc"]`  
**输出**: `true`  
**解释**:  
`word1` 表示的字符串为 `"ab" + "c"` → `"abc"`  
`word2` 表示的字符串为 `"a" + "bc"` → `"abc"`  
两个字符串相同，返回 `true`。

**示例 2**  
**输入**: `word1 = ["a", "cb"]`, `word2 = ["ab", "c"]`  
**输出**: `false`

**示例 3**  
**输入**: `word1 = ["abc", "d", "defg"]`, `word2 = ["abcddefg"]`  
**输出**: `true`

**约束条件**  
- `1 <= word1.length, word2.length <= 10^3`  
- `1 <= word1[i].length, word2[i].length <= 10^3`  
- `1 <= sum(word1[i].length), sum(word2[i].length) <= 10^3`  
- `word1[i]` 和 `word2[i]` 仅由小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把两个数组里的所有单词一次性拼成完整的字符串，再直接比较这两个字符串是否相等。  

- **使用的数据结构**：  
  - `list`（数组）存放每个单词，类似我们平时把单词写在纸条上。  
  - `str`（字符串）相当于把所有纸条依次粘在一起形成的一行文字，像把一本书的每页内容顺序连在一起。  
- **为什么正确**：  
  题目要求“数组表示的字符串”是把数组中的元素**按顺序**连接起来得到的完整字符串。如果我们真的把它们全部连接起来，得到的就是题目所说的“表示的字符串”。两个数组表示同一个字符串，就等价于这两个拼好的字符串相等。  
- **复杂度分析（大白话）**：  
  - **时间**：我们需要遍历所有单词里的每个字符一次，字符总数记作 `N`（`N` ≤ 1000），所以时间是 `O(N)`，也就是“和字符个数成正比”。  
  - **空间**：拼接后会产生两个新字符串，长度分别是 `len1`、`len2`，最坏情况下需要额外存 `O(N)` 的空间，也就是“和字符个数一样多的额外内存”。  

#### 代码（Python）

```python
def array_strings_are_equal(word1, word2):
    """
    暴力解：把两个数组全部拼接成字符串再比较
    """
    # 把 word1 中的所有单词拼成一个完整的字符串
    s1 = "".join(word1)          # "".join(...) 相当于把列表里的单词依次粘在一起
    # 把 word2 中的所有单词拼成一个完整的字符串
    s2 = "".join(word2)

    # 直接比较两个完整的字符串是否相等
    return s1 == s2
```

#### 复杂度

- **时间复杂度**：`O(N)` —— 需要遍历所有字符一次。  
- **空间复杂度**：`O(N)` —— 需要额外存放两个拼接后的完整字符串。  

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们创建了两个完整的字符串，导致额外的 `O(N)` 空间。如果只需要判断是否相等，其实不必把所有字符一次性写出来，只要同步地“逐字符”比较即可。  

**一步步的优化思路**：

1. **同步遍历**：把两个数组想象成两条装有字符的输送带，分别从左到右输送字符。我们用两个指针 `i1, i2` 分别指向当前正在比较的字符所在的单词，以及在该单词内部的下标 `j1, j2`。  
2. **逐字符比较**：每次比较 `word1[i1][j1]` 与 `word2[i2][j2]`。如果不相等直接返回 `False`。  
3. **移动指针**：比较完后把两个指针都向前移动一个字符；如果某个单词已经走完，就把对应的 `i` 加 1，`j` 重置为 0，继续看下一个单词。  
4. **结束条件**：当两个数组都走完（`i1 == len(word1)` 且 `i2 == len(word2)`）时，说明所有字符都匹配，返回 `True`。如果其中一个提前走完而另一个还有字符，则返回 `False`。  

**核心技巧**：**双指针**（Two‑Pointer）遍历。它像两个人分别在两条路上走，随时对齐比较当前的步子，避免一次性把所有东西搬到手里。

#### 代码（Python）

```python
def array_strings_are_equal(word1, word2):
    """
    最优解：双指针逐字符比较，省去额外的拼接字符串
    """
    i1 = i2 = 0          # 分别指向 word1、word2 当前所在的单词下标
    j1 = j2 = 0          # 分别指向当前单词内部的字符下标

    while i1 < len(word1) and i2 < len(word2):
        # 取出当前要比较的两个字符
        c1 = word1[i1][j1]
        c2 = word2[i2][j2]

        # 若字符不同，直接返回 False
        if c1 != c2:
            return False

        # 移动指针：各自向后走一个字符
        j1 += 1
        j2 += 1

        # 如果当前单词已经遍历完，换到下一个单词
        if j1 == len(word1[i1]):   # word1[i1] 已经读完
            i1 += 1
            j1 = 0                 # 重置字符下标

        if j2 == len(word2[i2]):   # word2[i2] 已经读完
            i2 += 1
            j2 = 0

    # 循环结束后，只有两种可能：
    # 1. 两个数组都恰好遍历完 -> 完全相等
    # 2. 其中一个还有剩余字符 -> 不相等
    return i1 == len(word1) and i2 == len(word2)
```

#### 复杂度

- **时间复杂度**：`O(N)` —— 每个字符最多被访问一次，和字符总数成正比。相当于“和暴力解一样快”。  
- **空间复杂度**：`O(1)` —— 只用了常数个指针变量，不会随输入规模增长而增加额外内存。相比暴力解省掉了 `O(N)` 的额外空间。

---

## 心得

- **核心技巧**：双指针逐字符比较（不额外构造完整字符串）。  
- **适用的题型**：  
  1. 两个字符串/数组是否相等（如 LeetCode 244. Shortest Word Distance II 的双指针版）。  
  2. 判断两个迭代器/流是否产生相同序列（如合并两个有序链表时的同步遍历）。  
- **一句话总结解题钥匙**：**“不必一次性搬走全部东西，边走边比较即可”。**

---

## 反思

- **第一反应**：直接把两个数组拼接成字符串再比较，代码最简洁。  
- **最容易踩的坑**：  
  - 忽视空数组或单词长度为 0 的情况（本题约束中不出现，但在实际面试中要防范）。  
  - 双指针实现时忘记在单词结束后把字符下标重置为 0，导致 IndexError。  
- **下次类似题的第一步**：先思考“是否真的需要完整的中间结果”，如果只需要比较，尝试用 **同步遍历 + 双指针** 的方式省空间。