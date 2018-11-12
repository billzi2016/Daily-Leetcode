# #168. Excel 表格列标题 / Excel Sheet Column Title

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/excel-sheet-column-title/)

---

## 题目（英文原版）

**Description**

Given an integer columnNumber, return its corresponding column title as it appears in an Excel sheet.
For example:

**Examples**

**Example 1:**

```
A -> 1
B -> 2
C -> 3
...
Z -> 26
AA -> 27
AB -> 28 
...
```

**Example 2:**

```
Input: columnNumber = 1
Output: "A"
```

**Example 3:**

```
Input: columnNumber = 28
Output: "AB"
```

**Example 4:**

```
Input: columnNumber = 701
Output: "ZY"
```

**Constraints**

- 1 <= columnNumber <= 231 - 1

---

## 题目（中文翻译）

给定一个整数 **列号（columnNumber）**，返回它在 Excel 表格中对应的 **列标题（column title）**。

## 示例

**示例 1**  
```
A -> 1
B -> 2
C -> 3
...
Z -> 26
AA -> 27
AB -> 28 
...
```

**示例 2**  
**输入**: `columnNumber = 1`  
**输出**: `"A"`

**示例 3**  
**输入**: `columnNumber = 28`  
**输出**: `"AB"`

**示例 4**  
**输入**: `columnNumber = 701`  
**输出**: `"ZY"`

## 约束条件

- `1 <= columnNumber <= 2^31 - 1`   (即 32 位有符号整数的最大正值)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把题目想成“把一个十进制整数，转换成只用 26 个字母（A~Z）表示的进制”。  
最直接的办法是：

1. **不断除以 26**，得到每一位对应的字母。  
2. **把每次得到的字母收集起来**，最后逆序（因为先得到的是最低位）得到答案。

这里用到的唯一数据结构是**列表（list）**，它相当于我们平时的“装东西的盒子”。我们把每一次算出来的字母放进盒子里，最后再把盒子里的东西倒过来读出来。

> 类比：查字典时，键（key）是我们要找的词，值（value）是对应的解释。这里“键”是余数（0~25），对应的“值”是字母 A~Z。

**为什么正确**  
- 在 Excel 的列编号中，`A` 表示 1，`Z` 表示 26，`AA` 表示 27。  
- 把 `columnNumber` 减 1（变成 0~25），再除以 26，就能得到对应的字母索引。  
- 重复这个过程，直到 `columnNumber` 变成 0，所有位的字母就全部算出来了。

**时间/空间复杂度**  
- 每一次循环都把 `columnNumber` 除以 26，循环次数大约是 `log₍₂₆₎(columnNumber)`，即 **O(log n)**（n 为输入大小）。  
- 只用了一个列表保存字母，列表长度同样是 **O(log n)**，其余空间都是常数。

> 大白话：如果数字是 1000，最多只需要跑几次（大约 3~4 次）就能得到答案；不管数字多大，循环次数都不会超过 7（因为 26⁷ > 2³¹），所以非常快。

#### 代码（Python）

```python
def convertToTitle(columnNumber: int) -> str:
    """
    把正整数 columnNumber 转换成 Excel 列标题
    """
    result = []                     # 用列表收集每一位的字符（相当于装字母的盒子）

    while columnNumber > 0:
        columnNumber -= 1           # 先减 1，让 1~26 映射到 0~25，方便取字母
        remainder = columnNumber % 26   # 余数对应字母的索引
        char = chr(ord('A') + remainder)  # 把索引转成字符，例如 0->'A', 25->'Z'
        result.append(char)         # 把字符放进盒子（列表）里
        columnNumber //= 26         # 去掉已经处理的最低位，继续处理高位

    # result 中的字符顺序是从低位到高位，逆序后才是正确的列标题
    return ''.join(reversed(result))
```

#### 复杂度

- **时间复杂度：O(log₍₂₆₎ n)**  
  解释：每次循环把数字除以 26，循环次数等于数字的 26 进制位数。即使 n 最大（2³¹‑1），循环也最多 7 次。

- **空间复杂度：O(log₍₂₆₎ n)**  
  解释：我们用列表保存每一位的字符，列表长度等于循环次数，也就是 26 进制位数。

---

### 2. 最优解

#### 思路  

暴力解已经是最优的时间复杂度 **O(log n)**，因为我们必须至少输出每一位字符，输出本身就需要 `log₍₂₆₎ n` 的时间。  
这里的“优化”主要是 **代码写得更简洁、避免不必要的列表反转**，直接在字符串前面插入字符（利用 Python 的字符串拼接特性）：

1. 同样是 **减 1、取余、除 26** 的循环。  
2. 这次每得到一个字符，直接 **把它加到答案的左边**（`result = char + result`），这样最后得到的字符串已经是正序，不需要再 `reversed`。

> 类比：把盒子里的字母每次都放在最前面，就像在纸上从左到右写字，一遍写完就不需要再翻转。

#### 代码（Python）

```python
def convertToTitle(columnNumber: int) -> str:
    """
    更简洁的实现：直接在左侧累加字符，省去列表和反转步骤
    """
    result = ""                     # 用字符串累计答案（相当于一张空白纸）

    while columnNumber > 0:
        columnNumber -= 1           # 把 1~26 映射到 0~25
        remainder = columnNumber % 26
        char = chr(ord('A') + remainder)  # 余数转字符
        result = char + result      # 把字符写在已有字符串的左边
        columnNumber //= 26

    return result
```

#### 复杂度

- **时间复杂度：O(log₍₂₆₎ n)**  
  与暴力解相同，因为循环次数不变。字符串前置拼接在 Python 中是 **O(1)**（因为每次都会创建新字符串，但字符总数仍是 `log n`，整体仍是线性于输出长度）。

- **空间复杂度：O(log₍₂₆₎ n)**  
  只用了一个字符串保存结果，长度等于输出字符数。

---

## 心得

- **核心技巧**：把 1~26 映射到 0~25（先 `-1`），再用 “除 26 取余” 的方式得到每一位字符。  
- **适用的题型**：  
  1. 任意进制的数值转字符串（比如十进制转二进制、八进制）。  
  2. “数字到字母”映射的题目（如将 1~26 映射为 A~Z 的密码题）。  
- **解题钥匙**：**先减 1 再取余**，把自然数序列对齐到 0 起点的数组索引。

---

## 反思

- **第一反应**：看到“Excel 列号”，立刻想到进制转换，只是进制基数是 26，且字符不是 0~9 而是 A~Z。  
- **最容易踩的坑**：  
  - 忘记 `columnNumber -= 1`，导致 `Z` 后面会出现 `@`（ASCII 65+26），结果错误。  
  - 直接使用 `chr(ord('A') + remainder)` 而不减 1，导致索引偏移。  
  - 边界值 `columnNumber = 26`（应输出 `Z`）和 `columnNumber = 27`（应输出 `AA`）常常混淆。  
- **下次第一步**：先把题目抽象为“把正整数按 26 进制拆分”，记得把 1~26 对齐到 0~25（`-1`），然后循环除 26、取余即可。