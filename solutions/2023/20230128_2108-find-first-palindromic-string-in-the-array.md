# #2108. 数组中第一个回文字符串 / Find First Palindromic String in the Array

> 难度：简单 · 标签：Array、Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/find-first-palindromic-string-in-the-array/)

---

## 题目（英文原版）

**Description**

Given an array of strings words, return the first palindromic string in the array. If there is no such string, return an empty string "".
A string is palindromic if it reads the same forward and backward.

**Examples**

**Example 1:**

```
Input: words = ["abc","car","ada","racecar","cool"]
Output: "ada"
Explanation: The first string that is palindromic is "ada".
Note that "racecar" is also palindromic, but it is not the first.
```

**Example 2:**

```
Input: words = ["notapalindrome","racecar"]
Output: "racecar"
Explanation: The first and only string that is palindromic is "racecar".
```

**Example 3:**

```
Input: words = ["def","ghi"]
Output: ""
Explanation: There are no palindromic strings, so the empty string is returned.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组（array）`words`，返回数组中第一个回文字符串（palindromic）。如果不存在满足条件的字符串，返回空字符串 `""`。  
回文字符串的定义是：正着读和反着读完全相同的字符串。

**示例 1:**  
**示例 2:**  
**示例 3:**  

**约束条件**  
- `1 <= words.length <= 100`  
- `1 <= words[i].length <= 100`  
- `words[i]` 仅由小写英文字母组成。

---

### 示例

#### 示例 1
**输入:**  
```json
words = ["abc","car","ada","racecar","cool"]
```  
**输出:**  
```
"ada"
```  
**解释:** 第一个满足回文条件的字符串是 `"ada"`。  
注意 `"racecar"` 也是回文字符串，但它不是第一个出现的。

#### 示例 2
**输入:**  
```json
words = ["notapalindrome","racecar"]
```  
**输出:**  
```
"racecar"
```  
**解释:** 唯一的回文字符串是 `"racecar"`，因此它既是第一个也是唯一的回文字符串。

#### 示例 3
**输入:**  
```json
words = ["def","ghi"]
```  
**输出:**  
```
""
```  
**解释:** 数组中不存在回文字符串，返回空字符串 `""`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **从左到右遍历数组**，一旦碰到回文字符串就立刻返回。  
判断一个字符串是否是回文，可以把它**反转**后和原串比较——如果相同就是回文。

- **数据结构**：这里只需要遍历列表 `words`，用到的“哈希表”之类的高级结构都不必。  
- **为什么正确**：因为题目要求返回**第一个**回文字符串，遍历顺序正好和题目要求一致，找到的第一个回文必然是答案。  
- **时间/空间复杂度**：  
  - 对每个字符串我们都要做一次“翻转”，翻转的代价是 O(k)，k 为该字符串长度。  
  - 整体上要遍历 `n` 个字符串，平均长度为 `m`，所以时间复杂度是 **O(n·m)**。  
  - 反转会产生一个新字符串，额外占用 O(k) 的空间，但只在检查当前字符串时存在，整体空间复杂度是 **O(m)**（最坏情况下是最长字符串的长度）。

> 大白话解释：如果数组里有 10 条句子，每条平均 5 个字母，那么我们大概要检查 10 × 5 = 50 次字符比较。

#### 代码（Python）

```python
def firstPalindrome(words):
    """
    遍历 words，返回第一个回文字符串；若不存在返回空串
    """
    for w in words:                       # 依次拿到每个字符串
        # 把字符串翻转后与原串比较，== 表示完全相同
        if w == w[::-1]:                  # w[::-1] 是 Python 的切片语法，快速得到逆序字符串
            return w                      # 找到第一个回文，直接返回
    return ""                             # 循环结束仍未找到，返回空串
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - `n` 为数组长度，`m` 为每个字符串的平均长度。  
  - 表示我们可能要检查所有字符一次。
- **空间复杂度**：`O(m)`  
  - 只在检查当前字符串时产生一个长度为 `m` 的临时逆序字符串，其他地方几乎不占额外空间。

---

### 2. 最优解

#### 思路  

从暴力解看，**瓶颈**在于每次判断回文时都要生成一个完整的逆序字符串，这会额外占用 `O(m)` 的空间。我们可以**用双指针**在原字符串上直接比较首尾字符，省掉临时字符串的创建。

- **双指针**：设左指针 `l` 指向字符串开头，右指针 `r` 指向结尾。每次比较 `s[l]` 与 `s[r]`，若相等则 `l += 1, r -= 1`，继续比较；只要出现不相等，就说明不是回文。全部比较完仍相等，则是回文。  
- 这一步的时间仍是 `O(m)`，但空间降到了 **O(1)**（只用几个整数变量）。

整体思路仍是“遍历数组，遇到第一个回文立即返回”。相对于前一种实现，**时间没有下降**（因为必须检查每个字符），但**空间降低**，在严格的内存限制下更友好。

#### 代码（Python）

```python
def is_palindrome(s: str) -> bool:
    """
    使用双指针判断字符串 s 是否为回文，时间 O(len(s))，空间 O(1)
    """
    left, right = 0, len(s) - 1          # 左右指针初始位置
    while left < right:                  # 当左指针还在右指针左侧时继续比较
        if s[left] != s[right]:          # 一旦发现不相等，直接返回 False
            return False
        left += 1                         # 左指针向右移动
        right -= 1                        # 右指针向左移动
    return True                          # 循环结束说明全部匹配，回文

def firstPalindrome(words):
    """
    遍历 words，返回第一个回文字符串；若不存在返回空串
    """
    for w in words:                       # 按顺序检查每个字符串
        if is_palindrome(w):              # 用双指针判断是否回文
            return w                      # 第一个回文直接返回
    return ""                             # 没有回文，返回空串
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - 与暴力解相同，因为每个字符仍然要检查一次。  
  - 与暴力解对比：时间没有提升，因为无论用翻转还是双指针，都必须看完整个字符串才能确认是否回文。
- **空间复杂度**：`O(1)`  
  - 只使用了几个整数变量 `left, right`，不随输入规模增长而增加。  
  - 相比暴力解的 `O(m)`（临时逆序字符串），省去了额外的内存。

---

## 心得

- **核心技巧**：使用 **双指针** 判断回文，省去额外的字符串拷贝。  
- **适用题型**：  
  1. 判断单个字符串是否回文（如 LeetCode 125. Valid Palindrome）  
  2. 判断回文子串或最长回文子串（如 LeetCode 5. Longest Palindromic Substring）  
  3. 需要在数组/链表中找第一个满足回文条件的元素（本题）  
- **一句话总结**：**“先遍历，遇到回文即止；回文判定用双指针，空间 O(1)”。**

---

## 反思

- **第一反应**：直接遍历数组，用 `s == s[::-1]` 检查回文，写完代码就能跑通。  
- **最容易踩的坑**：  
  - 忽略了 **空字符串** 也是回文（但本题约束最短长度为 1）。  
  - 对于极端输入（比如所有字符串都很长）使用 `s[::-1]` 会产生大量临时对象，可能导致内存超限。  
- **下次类似题的第一步**：先确认“**遍历顺序**”是否与题目要求的“第一个”对应，然后决定**回文判定方式**——如果对空间有要求，立刻想到 **双指针**。