# #1768. 交替合并字符串 / Merge Strings Alternately

> 难度：简单 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/merge-strings-alternately/)

---

## 题目（英文原版）

**Description**

You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. If a string is longer than the other, append the additional letters onto the end of the merged string.
Return the merged string.

**Examples**

**Example 1:**

```
Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
Explanation: The merged string will be merged as so:
word1:  a   b   c
word2:    p   q   r
merged: a p b q c r
```

**Example 2:**

```
Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
Explanation: Notice that as word2 is longer, "rs" is appended to the end.
word1:  a   b 
word2:    p   q   r   s
merged: a p b q   r   s
```

**Example 3:**

```
Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
Explanation: Notice that as word1 is longer, "cd" is appended to the end.
word1:  a   b   c   d
word2:    p   q 
merged: a p b q c   d
```

**Constraints**

- 1 <= word1.length, word2.length <= 100
- word1 and word2 consist of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定两个字符串 `word1` 和 `word2`。按照交替顺序合并这两个字符串，先从 `word1` 的第一个字符开始。如果其中一个字符串比另一个长，则将剩余的字符直接追加到合并后字符串的末尾。返回合并后的字符串。

**示例 1**  
```
Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
Explanation: 合并过程如下所示：
word1:  a   b   c
word2:    p   q   r
merged: a p b q c r
```

**示例 2**  
```
Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
Explanation: 由于 `word2` 更长，剩余的 `"rs"` 被追加到末尾。
word1:  a   b 
word2:    p   q   r   s
merged: a p b q   r   s
```

**示例 3**  
```
Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
Explanation: 由于 `word1` 更长，剩余的 `"cd"` 被追加到末尾。
word1:  a   b   c   d
word2:    p   q 
merged: a p b q c   d
```

**约束条件**  
- `1 <= word1.length, word2.length <= 100`  
- `word1` 和 `word2` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把两条“绳子”交叉编织**。  
- 用两个指针 `i`、`j` 分别指向 `word1`、`word2` 的当前位置。  
- 先取 `word1[i]`，再取 `word2[j]`，交替往结果字符串里拼。  
- 当一条绳子先到头了，就把另一条剩下的所有字符一次性接在后面。

这里把“指针”想象成 **读书时的手指**：左手指着 `word1`，右手指着 `word2`，轮流往纸上写字。

**为什么一定对？**  
因为我们严格按照题目要求的“先 `word1` 再 `word2`，交替取字符”去操作，所有字符都会被完整地、顺序地放进结果里，剩余的字符自然会在最后出现。

**复杂度的“大白话”**  
- **时间复杂度**：如果每次都用 `result += ch`（把字符拼到已有字符串后面），Python 会把原来的字符串复制一遍再加上新字符，**相当于每加一个字符都要搬一次“行李”。**  
  最坏情况下要搬 `1 + 2 + … + n = n·(n+1)/2` 次，时间是 **O(n²)**（n 为两串总长度）。  
- **空间复杂度**：只用一个额外的字符串保存答案，空间是 **O(n)**。

#### 代码（Python）  

```python
def mergeAlternately_bruteforce(word1: str, word2: str) -> str:
    i, j = 0, 0                 # 两个指针分别指向 word1、word2 的开头
    result = ""                 # 最终答案，用字符串直接累加（会产生 O(n²) 的复制）

    # 只要两边都还有字符，就交替取
    while i < len(word1) and j < len(word2):
        result += word1[i]      # 先放 word1 的当前字符
        i += 1                  # 指针往后走一步
        result += word2[j]      # 再放 word2 的当前字符
        j += 1

    # 可能还有剩余的字符没有处理，直接一次性拼上去
    if i < len(word1):          # word1 更长
        result += word1[i:]
    if j < len(word2):          # word2 更长
        result += word2[j:]

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每次 `+=` 都会重新复制已有的字符串，等价于搬运 n² 次“行李”。  
- **空间复杂度**：`O(n)` —— 只额外用了一个存放答案的字符串（长度为 n）。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到 **瓶颈在于不停地创建新字符串**（`result += ch`）。  
Python 中 **列表（list）** 的 `append` 操作是 **摊销 O(1)** 的，也就是说把字符一次放进列表里不会每次都复制全部内容。  
等所有字符都放进列表后，再用一次性 `''.join(list)` 把列表合并成字符串，这一步只遍历一次列表，时间是线性的。

所以最优解的核心是：

1. 用两个指针 `i、j` 交替遍历两串（**双指针**）。  
2. 把每个取到的字符 **追加到列表** `res` 中。  
3. 最后一次性 `''.join(res)` 得到答案。

> **类比**：把字符装进 **背包**（列表）里，背包可以随意往里塞东西而不需要每次都把背包装满再搬走。等背包装好后，一次性倒出所有东西（`join`），既省力又省时。

#### 代码（Python）  

```python
def mergeAlternately_optimal(word1: str, word2: str) -> str:
    i, j = 0, 0                       # 双指针，从两串的开头开始
    res = []                          # 用列表收集字符，append 是 O(1)

    # 交替取字符，直到其中一条“绳子”走完
    while i < len(word1) and j < len(word2):
        res.append(word1[i])          # 先放 word1 的字符
        i += 1
        res.append(word2[j])          # 再放 word2 的字符
        j += 1

    # 把剩余的字符一次性加入列表（如果有的话）
    if i < len(word1):
        res.extend(word1[i:])         # extend 把子串整体加入列表
    if j < len(word2):
        res.extend(word2[j:])

    # 一次性把列表里的字符拼成字符串返回
    return ''.join(res)
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 每个字符只被访问、加入列表一次，`join` 也只遍历一次。  
- **空间复杂度**：`O(n)` —— 需要额外的列表保存所有字符，大小等于答案长度。  
> 与暴力解相比，时间从 **O(n²)** 降到了 **O(n)**，大幅提升了效率。

---

## 心得  

- **核心技巧**：**双指针 + 列表 + 一次性 `join`**。  
- **适用的题型**：  
  1. 两个序列交叉合并（如 “交叉合并两个有序数组”）。  
  2. 按固定模式遍历两个字符串/数组（如 “交叉打印链表节点”）。  
  3. 需要频繁在字符串中插入字符的场景（如 “实现自定义的字符串构造器”）。  
- **一句话总结**：把“每次拼接都搬家”的做法换成“先装进背包，统一倒出”，就能把时间从平方级降到线性级。

---

## 反思  

- **第一反应**：直接写 `result += ch`，因为字符串拼接看起来最直观。  
- **最容易踩的坑**：  
  - 忽略了 Python 字符串不可变导致的 **O(n²)** 时间。  
  - 边界条件：两串长度不同，需要把剩余的子串一次性加到结果后面。  
- **下次类似题的第一步**：先判断是否会出现大量“逐字符拼接”，如果会，就**准备列表/数组**先收集，再一次性 `join`。这样可以避免不必要的性能陷阱。