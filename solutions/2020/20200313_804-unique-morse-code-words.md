# #804. 唯一的摩尔斯密码单词 / Unique Morse Code Words

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/unique-morse-code-words/)

---

## 题目（英文原版）

**Description**

International Morse Code defines a standard encoding where each letter is mapped to a series of dots and dashes, as follows:
For convenience, the full table for the 26 letters of the English alphabet is given below:
Given an array of strings words where each word can be written as a concatenation of the Morse code of each letter.
Return the number of different transformations among all words we have.

**Examples**

**Example 1:**

```
[".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]
```

**Example 2:**

```
Input: words = ["gin","zen","gig","msg"]
Output: 2
Explanation: The transformation of each word is:
"gin" -> "--...-."
"zen" -> "--...-."
"gig" -> "--...--."
"msg" -> "--...--."
There are 2 different transformations: "--...-." and "--...--.".
```

**Example 3:**

```
Input: words = ["a"]
Output: 1
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 12
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

国际摩尔斯密码（Morse Code）定义了一套标准编码，每个字母对应一串点（.）和划（-），如下所示：  
为方便起见，下面给出英文字母表 26 个字母对应的完整映射表。  

给定一个字符串数组 `words`，其中每个单词可以表示为其每个字母对应的摩尔斯密码的拼接。  
返回所有单词转换后得到的不同摩尔斯密码序列的数量。

**示例 1**  

（此处省略具体内容，仅作占位）

**示例 2**  

```text
Input: words = ["gin","zen","gig","msg"]
Output: 2
Explanation: 每个单词的转换结果为：
"gin" -> "--...-."
"zen" -> "--...-."
"gig" -> "--...--."
"msg" -> "--...--."
共有 2 种不同的转换结果："--...-." 和 "--...--."。
```

**示例 3**  

```text
Input: words = ["a"]
Output: 1
```

**约束条件**  

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 12`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **把每个字母的摩斯密码存进表**。  
   可以用一个 **列表**（下标 0 对应 `'a'`，下标 1 对应 `'b'` …）来保存 26 条映射。  
   这相当于一本「查字典」：把字母当成词，摩斯码就是对应的页码。

2. **遍历每个单词**，把它的每个字符转换成摩斯码，再把这些小段拼接成一个完整的字符串。  
   就像把每个字母的“拼图块”拼成整幅图。

3. **把得到的完整摩斯码放进集合**（Hash Set）。  
   集合的特性是“不会出现重复”，所以把所有单词的转换放进去后，集合的大小就是不同变形的数量。  
   哈希表在这里好比「不重复的邮筒」：每次投递信件，如果已经有相同内容的信件，就会被自动合并。

因为题目本身的规模非常小（最多 100 个单词、每个单词最长 12 个字母），直接按照上面的步骤做就能在毫秒级完成。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
from typing import List

class Solution:
    def uniqueMorseRepresentations(self, words: List[str]) -> int:
        # 1. 摩斯码表，顺序对应 a~z
        morse_table = [
            ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---",
            "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-",
            "..-", "...-", ".--", "-..-", "-.--", "--.."
        ]

        # 2. 用集合记录出现过的完整摩斯码
        transformations = set()

        for word in words:                     # 遍历每个单词
            morse_word = []                     # 用列表收集每个字母的摩斯码
            for ch in word:                     # 遍历单词里的每个字符
                index = ord(ch) - ord('a')      # 计算字符在字母表中的下标（0~25）
                morse_word.append(morse_table[index])  # 取对应的摩斯码
            # 将列表拼成字符串，例如 ['--', '...'] -> '--...'
            transformations.add(''.join(morse_word))

        # 集合的大小就是不同的变形数量
        return len(transformations)
```

#### 复杂度  

- **时间复杂度：O(N·L)**  
  - `N` 是单词数量（≤100），`L` 是单词的最大长度（≤12）。  
  - 我们对每个字符都做一次「查表」和「拼接」操作，所以整体是线性的。  
  - 用大白话说，就是「看多少字符，就花多少时间」。

- **空间复杂度：O(N·L)**（最坏情况）  
  - 需要存放每个单词对应的完整摩斯码，最坏情况下每个单词的变形都不相同，集合里会有 `N` 条长度约 `L` 的字符串。  
  - 这相当于「把所有拼好的图都贴在墙上」需要的空间。

---

### 2. 最优解

#### 思路  

其实在本题的约束下，**暴力解已经是最优的**，因为我们已经达到了线性时间 `O(N·L)`，不可能再低于遍历所有字符的下界。  
不过可以从「怎么把代码写得更简洁、易懂」的角度做一点点改进：

1. **利用 Python 的字典推导式**一次性构造字母→摩斯码的映射，这样不必记住下标计算。  
   把字母看成「钥匙」，摩斯码看成「对应的值」，这正是哈希表（字典）的典型用法。

2. **使用集合推导式**直接生成所有变形，省去显式的 `add` 步骤。  
   类比「一次性把所有信件投递到不重复的邮筒里」。

这样做的本质仍然是 **遍历每个字符一次**，时间复杂度不变，但代码更紧凑，思路更「函数式」——对初学者来说可以帮助养成好习惯。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
from typing import List

class Solution:
    def uniqueMorseRepresentations(self, words: List[str]) -> int:
        # 1. 把 26 条映射一次性放进字典（哈希表）
        morse_codes = [
            ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---",
            "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-",
            "..-", "...-", ".--", "-..-", "-.--", "--.."
        ]
        morse_dict = {chr(ord('a') + i): code for i, code in enumerate(morse_codes)}

        # 2. 用集合推导式直接得到所有不同的变形
        transformations = {
            ''.join(morse_dict[ch] for ch in word)   # 把单词的每个字母转换后拼接
            for word in words
        }

        return len(transformations)
```

#### 复杂度  

- **时间复杂度：O(N·L)**  
  与暴力解相同，因为每个字符仍然只能被访问一次。  
  这里的「最优」体现在「没有多余的循环或临时变量」。

- **空间复杂度：O(N·L)**  
  仍然需要保存所有不同的摩斯码字符串。  
  与暴力解的空间需求一致，只是实现方式更紧凑。

---

## 心得

- **核心技巧**：把字符映射成另一种表示（这里是摩斯码）后，用 **哈希集合** 去重。  
- **适用场景**：  
  1. **字符串规范化后去重**（如去除标点、大小写统一后统计不同单词）。  
  2. **数字或坐标的唯一化**（把坐标 `(x, y)` 转成字符串 `"x#y"` 放进集合）。  
  3. **自定义编码**（如把颜色代码转成十六进制后统计不同颜色）。  
- **一句话总结**：**把每个对象映射成唯一的“钥匙”，用集合自动去重**。

---

## 反思

- **第一反应**：把字母表和摩斯码对应起来，逐字符转换，再用 `set` 去重。  
- **最容易踩的坑**：  
  - **下标错误**：`ord(ch) - ord('a')` 必须确保 `ch` 是小写字母，否则会出现负数或越界。  
  - **集合误用**：把列表直接放进集合会报错，因为列表不可哈希；必须先把摩斯码拼成字符串（或使用元组）。  
  - **忘记返回集合大小**：直接返回集合本身会得到错误的类型。  
- **下次思路**：遇到「把每个元素转换后统计不同数量」的题目时，第一步就想到 **「映射 + 哈希集合」**，再根据具体需求决定是否需要额外的数据结构（如计数器）。