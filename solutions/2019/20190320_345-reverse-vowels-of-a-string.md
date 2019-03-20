# #345. 翻转字符串中的元音字母 / Reverse Vowels of a String

> 难度：简单 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/reverse-vowels-of-a-string/)

---

## 题目（英文原版）

**Description**

Given a string s, reverse only all the vowels in the string and return it.
The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower and upper cases, more than once.

**Examples**

**Example 1:**

```
Input: s = "IceCreAm"
Output: "AceCreIm"
Explanation:
The vowels in s are ['I', 'e', 'e', 'A'] . On reversing the vowels, s becomes "AceCreIm" .
```

**Example 2:**

```
Input: s = "leetcode"
Output: "leotcede"
```

**Constraints**

- 1 <= s.length <= 3 * 105
- s consist of printable ASCII characters.

---

## 题目（中文翻译）

给定一个字符串 `s`，仅翻转其中所有的元音字母（vowels），并返回处理后的字符串。  
元音字母包括 `'a'、'e'、'i'、'o'、'u'`，且大小写均可出现，可能出现多次。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  
**示例 1**  
``` 
Input: s = "IceCreAm"
Output: "AceCreIm"
Explanation:
s 中的元音字母为 ['I', 'e', 'e', 'A']。在翻转这些元音字母后，s 变为 "AceCreIm"。
```

**示例 2**  
``` 
Input: s = "leetcode"
Output: "leotcede"
```

**约束条件**  
- `1 <= s.length <= 3 * 10^5`  
- `s` 由可打印的 ASCII 字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：先把字符串里所有的元音字符（a、e、i、o、u，大小写都算）全部找出来，放进一个列表；  
然后把这个列表反转；  
最后再遍历原字符串，把遇到的元音依次替换成反转后列表中的字符。

> **类比**：把字符串想象成一本书，元音就是书里所有的红色标记。我们先把所有红色标记摘下来（放进盒子），把盒子倒置，再把标记按倒置的顺序贴回去。

这个方法一定能得到正确答案，因为我们没有改变元音的相对顺序——只把顺序整体倒转了。

#### 代码（Python）

```python
def reverseVowels_brute(s: str) -> str:
    # 1. 先找出所有元音，保存顺序
    vowels = {'a', 'e', 'i', 'o', 'u',
              'A', 'E', 'I', 'O', 'U'}          # 元音集合，查找像查字典一样 O(1)
    vowel_chars = [ch for ch in s if ch in vowels]   # 把所有元音收集到列表

    # 2. 把元音列表反转
    vowel_chars.reverse()          # 原地反转，等价于 vowel_chars = vowel_chars[::-1]

    # 3. 再遍历原字符串，用反转后的元音替换
    res = []                        # 用列表收集结果，最后再 join 成字符串
    idx = 0                         # 记录当前应该取哪一个反转后的元音
    for ch in s:
        if ch in vowels:            # 遇到元音就用反转后的元音替换
            res.append(vowel_chars[idx])
            idx += 1
        else:                       # 不是元音保持原样
            res.append(ch)
    return ''.join(res)             # 把列表拼成最终字符串
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  我们遍历了三次字符串（一次收集元音、一次反转列表、一次生成结果），每次都是线性操作。这里的 `n` 就是字符串的长度。  
  大白话：如果字符串有 1000 个字符，程序大概会做 3 × 1000 次“检查/复制”，这在量级上仍然是“跟字符数成正比”。

- **空间复杂度**：`O(n)`  
  需要额外的列表保存所有元音（最坏情况所有字符都是元音），以及结果列表。  

---

### 2. 最优解

#### 思路  

暴力解已经是 `O(n)` 时间了，看起来已经很快。但它用了额外的 `O(n)` 空间来存元音列表。我们可以**在原地**完成逆序，只使用常数级的额外空间。

思路如下：

1. 使用 **双指针**：左指针 `i` 从字符串左侧向右移动，右指针 `j` 从右侧向左移动。  
2. 每次让 `i` 找到下一个元音，`j` 找到上一个元音。  
3. 当两指针都指向元音时，直接交换这两个字符。  
4. 交换后，`i` 向右走一步，`j` 向左走一步，继续循环，直到 `i >= j` 为止。

> **类比**：把字符串看成一条走道，两个人站在走道两端，只在看到红色标记（元音）时才互相递交手中的标记，然后继续往前走。

这样我们只遍历一次字符串（每个字符最多被检查两次），不需要额外的列表，空间降到 `O(1)`。

#### 代码（Python）

```python
def reverseVowels_opt(s: str) -> str:
    vowels = {'a', 'e', 'i', 'o', 'u',
              'A', 'E', 'I', 'O', 'U'}          # 同样用集合做 O(1) 判断

    # 为了能够原地修改，先把字符串转成列表（字符串在 Python 中是不可变的）
    chars = list(s)

    i, j = 0, len(chars) - 1                     # 左右指针初始化
    while i < j:
        # 左指针向右找下一个元音
        while i < j and chars[i] not in vowels:
            i += 1
        # 右指针向左找上一个元音
        while i < j and chars[j] not in vowels:
            j -= 1

        if i < j:                                 # 两指针都指到元音，交换
            chars[i], chars[j] = chars[j], chars[i]
            i += 1
            j -= 1

    return ''.join(chars)                         # 把列表拼回字符串
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  每个字符最多被左指针或右指针检查一次，整体仍然是线性。相比暴力解，实际运行更快，因为省掉了列表的额外遍历和反转操作。

- **空间复杂度**：`O(1)`（不计输出字符串本身）  
  只用了常数个额外变量 `i、j、vowels`。我们把字符串转成列表是必须的，因为 Python 字符串不可原地修改，但这相当于输出空间，算作 `O(n)` 必要的返回值。

---

## 心得

- **核心技巧**：双指针（Two Pointers）在需要**从两端同时处理**的数据时非常有用，能够在 O(1) 额外空间下完成逆序、配对等操作。  
- **适用题型**：
  1. “移动零”（Move Zeroes）——把所有 0 移到数组末尾。  
  2. “判断回文字符串（只考虑字母和数字）”——用双指针从两端比较字符。  
  3. “删除有序数组中的重复元素”——双指针维护写指针和读指针。  
- **解题钥匙**：**“从两头往中间逼近，只在满足条件时才动手”**。

## 反思

- **第一反应**：先把所有元音收集起来再倒序，想到用列表保存，代码写得比较直观。  
- **最容易踩的坑**：
  - 忽略大小写导致漏掉大写元音。  
  - 当字符串全是非元音时，双指针循环可能出现死循环，需要在 while 条件里同时检查 `i < j`。  
  - Python 中字符串不可变，直接交换会报错，需要先转成列表。  
- **下次类似题的第一步**：先判断**是否可以用双指针**（或其他线性遍历的“从两端”技巧）把问题转化为“在两端寻找满足条件的元素”。这样就能快速锁定 O(n) 时间、O(1) 空间的最优解。