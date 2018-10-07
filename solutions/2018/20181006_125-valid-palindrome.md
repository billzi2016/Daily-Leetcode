# #125. 有效回文 / Valid Palindrome

> 难度：简单 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/valid-palindrome/)

---

## 题目（英文原版）

**Description**

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.
Given a string s, return true if it is a palindrome, or false otherwise.

**Examples**

**Example 1:**

```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

**Example 2:**

```
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
```

**Example 3:**

```
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
```

**Constraints**

- 1 <= s.length <= 2 * 105
- s consists only of printable ASCII characters.

---

## 题目（中文翻译）

**描述**  
如果一个短语在将所有大写字母转换为小写字母并去除所有非字母数字字符（non‑alphanumeric characters）后，正读与反读相同，则称其为回文（palindrome）。字母数字字符（alphanumeric characters）包括字母和数字。

给定一个字符串 `s`，如果它是回文则返回 `true`，否则返回 `false`。

**示例 1**  

**示例 2**  

**示例 3**  

**约束**  

**示例**  

**示例 1**  
```text
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" 是一个回文。
```

**示例 2**  
```text
Input: s = "race a car"
Output: false
Explanation: "raceacar" 不是回文。
```

**示例 3**  
```text
Input: s = " "
Output: true
Explanation: 去除非字母数字字符后，s 变成空字符串 ""。空字符串正读和反读相同，因此是回文。
```

**约束条件**  

- `1 <= s.length <= 2 * 10^5`  
- `s` 仅由可打印的 ASCII 字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：先把原字符串 **全部** 处理成只包含字母和数字的小写形式，然后把处理好的字符串正着读、反着读进行比较。  
- **处理字符串**：遍历原字符串，把每个字符判断是否是字母或数字（相当于把“非字母数字”过滤掉），如果是，就把它转成小写后加入新字符串。可以把这一步想象成 **筛选水果**：只挑出苹果和香蕉（字母数字），把它们切成小块（转成小写），装进篮子里（新字符串）。
- **比较**：把新字符串 `t` 与它的逆序 `t[::-1]` 做等号判断。如果相等，则说明正着读和反着读完全相同，即是回文。

这种方法的正确性很直观：我们把所有“干扰因素”（空格、标点、大小写）全部去掉，只剩下真正需要比较的字符，然后直接比较正逆两个序列是否相同。

#### 代码（Python）
```python
def isPalindrome_brute(s: str) -> bool:
    # 1️⃣ 过滤并转小写
    filtered = []                     # 用列表收集字符，最后再合并成字符串
    for ch in s:
        if ch.isalnum():              # isalnum() 相当于“是不是字母或数字”
            filtered.append(ch.lower())
    t = ''.join(filtered)             # 把列表变成连续的字符串

    # 2️⃣ 正反比较
    return t == t[::-1]               # t[::-1] 是字符串的逆序切片
```

#### 复杂度
- **时间复杂度**：`O(n)`  
  这里的 `n` 是原字符串的长度。我们遍历一次字符串做过滤 (`O(n)`)，再一次遍历做逆序比较（`t[::-1]` 也需要 `O(n)`），总体仍是线性时间。用大白话说，就是“随着字符数增加，耗时也线性增长”，没有指数或平方的爆炸。
- **空间复杂度**：`O(n)`  
  需要额外的列表/字符串来保存过滤后的字符，最坏情况下（原字符串全部是字母数字）会和原字符串等长。

---

### 2. 最优解

#### 思路  
从暴力解看，**主要的开销** 在于我们额外创建了一个完整的过滤后字符串 `t`，以及它的逆序副本。其实我们不需要一次性把所有字符都收集好，只要从两端同时向中间“走”，随时跳过不需要的字符，就可以直接比较。

这正是 **双指针**（Two Pointers）技巧的典型用法：

1. **左指针 `i`** 从字符串最左侧向右移动，**右指针 `j`** 从最右侧向左移动。  
2. 每次移动时，先检查当前字符是否是字母或数字：
   - 若不是（比如空格、标点），直接把对应的指针向中间推进，继续检查下一个字符。
   - 若是，则把字符统一转成小写后进行比较。  
3. 如果这两个字符不相等，说明不是回文，直接返回 `False`。  
4. 当左指针 `i` 与右指针 `j` 相遇或交叉时，说明所有需要比较的字符都相等，返回 `True`。

**类比**：把字符串想象成一条走廊，两个人站在走廊的两头，只检查走廊上是否有“合法的砖块”（字母数字），并且每次都拿相对应的砖块比对，若有不一样的就说明走廊不对称。

这种做法的好处是**不需要额外的存储**，只在原字符串上直接读取，空间几乎为常数。

#### 代码（Python）
```python
def isPalindrome(s: str) -> bool:
    i, j = 0, len(s) - 1               # 左右指针初始位置

    while i < j:                       # 当左指针在右指针左侧时继续
        # ① 跳过左侧非字母数字字符
        while i < j and not s[i].isalnum():
            i += 1                      # 左指针向右移动
        # ② 跳过右侧非字母数字字符
        while i < j and not s[j].isalnum():
            j -= 1                      # 右指针向左移动

        # ③ 取出合法字符并统一转成小写后比较
        if s[i].lower() != s[j].lower():
            return False                # 只要有一次不相等，就不是回文

        # ④ 两指针同时向中间收敛，准备比较下一对字符
        i += 1
        j -= 1

    return True                         # 所有合法字符都匹配成功
```

#### 复杂度
- **时间复杂度**：`O(n)`  
  每个字符最多被左指针或右指针检查一次，整体仍是线性时间。相比暴力解，省去了生成逆序字符串的额外遍历，实际常数更小。
- **空间复杂度**：`O(1)`  
  只使用了几个整数指针和常数级的临时变量，不随输入规模增长而增长。可以说几乎不占额外内存。

---

## 心得

- **核心技巧**：双指针（Two Pointers）在字符串/数组的“对称比较”场景中非常高效。  
- **适用题型**：  
  1. 判断回文（如本题、`Valid Palindrome II`）  
  2. 两数之和的有序数组版（`Two Sum II - Input array is sorted`）  
  3. 合并两个有序链表（`Merge Two Sorted Lists`）——都是从两端/头尾共同推进的思路。  
- **一句话总结**：**“只要能从两端同步比较，就能省去额外的存储”。**

---

## 反思

- **第一反应**：先把字符串全部清洗干净，再直接比较正逆序。  
- **最容易踩的坑**：  
  - 忘记对字符做 **大小写统一**（`lower()`），导致 `'A'` 与 `'a'` 被误判。  
  - 忽略空字符串或只剩非字母数字的情况，实际应返回 `True`（空串本身是回文）。  
  - 使用 `isalnum()` 判断时要注意它在 ASCII 之外的字符行为（本题限制 ASCII，可直接使用）。  
- **下次类似题的第一步**：**先想能否用“双指针”从两端同步检查**，如果可以，就立刻尝试把“过滤+比较”合并在一次遍历里。