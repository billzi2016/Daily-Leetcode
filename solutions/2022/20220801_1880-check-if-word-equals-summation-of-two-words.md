# #1880. 检查单词是否等于两个单词之和 / Check if Word Equals Summation of Two Words

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/check-if-word-equals-summation-of-two-words/)

---

## 题目（英文原版）

**Description**

The letter value of a letter is its position in the alphabet starting from 0 (i.e. 'a' -> 0, 'b' -> 1, 'c' -> 2, etc.).
The numerical value of some string of lowercase English letters s is the concatenation of the letter values of each letter in s, which is then converted into an integer.
You are given three strings firstWord, secondWord, and targetWord, each consisting of lowercase English letters 'a' through 'j' inclusive.
Return true if the summation of the numerical values of firstWord and secondWord equals the numerical value of targetWord, or false otherwise.

**Examples**

**Example 1:**

```
Input: firstWord = "acb", secondWord = "cba", targetWord = "cdb"
Output: true
Explanation:
The numerical value of firstWord is "acb" -> "021" -> 21.
The numerical value of secondWord is "cba" -> "210" -> 210.
The numerical value of targetWord is "cdb" -> "231" -> 231.
We return true because 21 + 210 == 231.
```

**Example 2:**

```
Input: firstWord = "aaa", secondWord = "a", targetWord = "aab"
Output: false
Explanation: 
The numerical value of firstWord is "aaa" -> "000" -> 0.
The numerical value of secondWord is "a" -> "0" -> 0.
The numerical value of targetWord is "aab" -> "001" -> 1.
We return false because 0 + 0 != 1.
```

**Example 3:**

```
Input: firstWord = "aaa", secondWord = "a", targetWord = "aaaa"
Output: true
Explanation: 
The numerical value of firstWord is "aaa" -> "000" -> 0.
The numerical value of secondWord is "a" -> "0" -> 0.
The numerical value of targetWord is "aaaa" -> "0000" -> 0.
We return true because 0 + 0 == 0.
```

**Constraints**

- 1 <= firstWord.length, secondWord.length, targetWord.length <= 8
- firstWord, secondWord, and targetWord consist of lowercase English letters from 'a' to 'j' inclusive.

---

## 题目（中文翻译）

**描述**  
字母的字母值（letter value）是它在字母表中的位置，从 0 开始计数（即 `'a' -> 0`，`'b' -> 1`，`'c' -> 2`，依此类推）。  
一个仅包含小写英文字母的字符串 `s` 的数值（numerical value）是将 `s` 中每个字母的字母值拼接成一个字符串，然后再将该字符串转换为整数。  

给定三个字符串 `firstWord`、`secondWord` 和 `targetWord`，它们均只包含字符 `'a'` 到 `'j'`（含）。  
如果 `firstWord` 与 `secondWord` 的数值之和等于 `targetWord` 的数值，返回 `true`；否则返回 `false`。  

**示例**  

*示例 1*  
```text
Input: firstWord = "acb", secondWord = "cba", targetWord = "cdb"
Output: true
Explanation:
firstWord 的数值是 "acb" -> "021" -> 21。
secondWord 的数值是 "cba" -> "210" -> 210。
targetWord 的数值是 "cdb" -> "231" -> 231。
因为 21 + 210 == 231，返回 true。
```

*示例 2*  
```text
Input: firstWord = "aaa", secondWord = "a", targetWord = "aab"
Output: false
Explanation:
firstWord 的数值是 "aaa" -> "000" -> 0。
secondWord 的数值是 "a" -> "0" -> 0。
targetWord 的数值是 "aab" -> "001" -> 1。
因为 0 + 0 != 1，返回 false。
```

*示例 3*  
```text
Input: firstWord = "aaa", secondWord = "a", targetWord = "aaaa"
Output: true
Explanation:
firstWord 的数值是 "aaa" -> "000" -> 0。
secondWord 的数值是 "a" -> "0" -> 0。
targetWord 的数值是 "aaaa" -> "0000" -> 0。
因为 0 + 0 == 0，返回 true。
```

**约束条件**  

- `1 <= firstWord.length, secondWord.length, targetWord.length <= 8`
- `firstWord`、`secondWord` 和 `targetWord` 仅由字符 `'a'` 到 `'j'`（含）组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把每个单词的字母逐个换成对应的数字（`'a'→0, 'b'→1 … 'j'→9`），再把这些数字拼成一个字符串，最后把字符串直接交给 Python 的 `int()` 转成整数。  

- **数据结构**：这里只用了最常见的 **字符串**（相当于把每个字母写成一行文字）和 **哈希表**（把字母映射到数字，哈希表就像一本查字典，词是字母，页码是对应的数字）。  
- **正确性**：因为题目要求的“数值”本质上就是把每个字母对应的数字按顺序连接起来形成的十进制数，而 `int()` 正好可以把这种十进制字符串转换为整数，所以这种做法一定能得到题目要求的数值。  
- **时间/空间复杂度**：我们要遍历三个字符串一次，每个字符做 O(1) 的映射和拼接，整体时间是 **O(L)**（L 为三个字符串长度之和，最多 8+8+8=24），空间上额外创建了几个同样长度的临时字符串，空间是 **O(L)**。  
  - 大白话：如果把遍历想象成“一只手从左到右数字母”，每数一个字母就花一点时间，整个过程花的时间正比于字母总数。  
  - O(L) 里的 **O** 表示“数量级”，意思是时间随输入大小线性增长，而不是指数或平方级别的爆炸。

#### 代码（Python）  

```python
def isSumEqual(firstWord: str, secondWord: str, targetWord: str) -> bool:
    # 1. 建立字母 → 数字的映射表（类似查字典）
    char_to_digit = {chr(ord('a') + i): str(i) for i in range(10)}  # 'a'->'0', 'b'->'1', ...

    # 2. 把每个单词转换成对应的数字字符串
    def word_to_number_str(word: str) -> str:
        # 用列表收集每个字符对应的数字，再一次性 join 成字符串，效率更高
        digits = [char_to_digit[ch] for ch in word]
        return ''.join(digits)

    # 3. 再把数字字符串转成整数进行比较
    first_val  = int(word_to_number_str(firstWord))
    second_val = int(word_to_number_str(secondWord))
    target_val = int(word_to_number_str(targetWord))

    # 4. 检查是否相等
    return first_val + second_val == target_val
```

#### 复杂度  

- **时间复杂度**：`O(L)`，遍历每个字符一次。  
- **空间复杂度**：`O(L)`，需要存放临时的数字字符串（最坏 8 位），在本题规模下几乎可以忽略不计。  

---  

### 2. 最优解  

#### 思路  
暴力解已经是 **线性** 的，没有明显的“慢点”。  
不过我们可以把 **临时字符串** 这一步省掉，直接在遍历字符时用数学方式累计数值：

- 把当前的数值乘以 10（相当于在十进制里左移一位），再加上当前字符对应的数字。  
- 这样只需要 **一个整数变量** 来保存结果，省去额外的字符串空间。  

这一步的核心是 **“滚动构造整数”**（rolling construction），在很多需要把字符序列解释为数字的题目中都很有用，比如把二进制字符串转十进制。  

> **类比**：想象你在读一本电话号码，先读到“2”，再读到“1”，这时号码应该是 `2*10 + 1 = 21`，继续读到“3”，号码变成 `21*10 + 3 = 213`，这就是我们在代码里做的事。

#### 代码（Python）  

```python
def isSumEqual(firstWord: str, secondWord: str, targetWord: str) -> bool:
    # 把单词直接转成整数，不产生中间字符串
    def word_to_int(word: str) -> int:
        value = 0
        for ch in word:
            digit = ord(ch) - ord('a')          # 'a'->0, 'b'->1, ...
            value = value * 10 + digit          # 左移一位并加上新数字
        return value

    first_val  = word_to_int(firstWord)
    second_val = word_to_int(secondWord)
    target_val = word_to_int(targetWord)

    return first_val + second_val == target_val
```

#### 复杂度  

- **时间复杂度**：`O(L)`，仍然只遍历一次所有字符。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，没有额外随输入增长的存储。  
- 与暴力解相比，时间没有提升（已经是最优的线性遍历），但**空间从 O(L) 降到 O(1)**，在更大规模的数据里会更节省内存。

---  

## 心得  

- **核心技巧**：把字符映射为数字并利用十进制的“左移+加”方式累计整数。  
- **适用场景**：  
  1. 把仅包含 `'0'~'9'` 的字符串转成整数（如 LeetCode 13. Roman to Integer 的思路）。  
  2. 把二进制/八进制/十六进制字符串转换为十进制整数。  
  3. 需要在遍历字符时即时计算数值的题目（例如“把字母映射为 0~25 并求和”）。  
- **一句话总结**：**“遍历字符，累加：value = value * 10 + digit”** 就是本题的解题钥匙。  

## 反思  

- **第一反应**：把每个字母映射成数字，拼成字符串再 `int()`，因为 Python 已经帮我们把十进制字符串转整数了。  
- **最容易踩的坑**：  
  - 忘记把字符 `'a'` 对应到 **0** 而不是 **1**（题目是从 0 开始计数）。  
  - 对于空字符串（本题不会出现）直接 `int('')` 会报错，需要额外判断。  
- **下次遇到同类题**：第一步先思考 **“如何把字符直接累加成整数”**，看能否在遍历时完成，而不是先造中间字符串再转换。这样往往能直接得到 **O(1) 空间** 的最优实现。