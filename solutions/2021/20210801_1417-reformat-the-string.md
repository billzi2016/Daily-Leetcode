# #1417. 重新格式化字符串 / Reformat The String

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/reformat-the-string/)

---

## 题目（英文原版）

**Description**

You are given an alphanumeric string s. (Alphanumeric string is a string consisting of lowercase English letters and digits).
You have to find a permutation of the string where no letter is followed by another letter and no digit is followed by another digit. That is, no two adjacent characters have the same type.
Return the reformatted string or return an empty string if it is impossible to reformat the string.

**Examples**

**Example 1:**

```
Input: s = "a0b1c2"
Output: "0a1b2c"
Explanation: No two adjacent characters have the same type in "0a1b2c". "a0b1c2", "0a1b2c", "0c2a1b" are also valid permutations.
```

**Example 2:**

```
Input: s = "leetcode"
Output: ""
Explanation: "leetcode" has only characters so we cannot separate them by digits.
```

**Example 3:**

```
Input: s = "1229857369"
Output: ""
Explanation: "1229857369" has only digits so we cannot separate them by characters.
```

**Constraints**

- 1 <= s.length <= 500
- s consists of only lowercase English letters and/or digits.

---

## 题目（中文翻译）

给定一个字母数字字符串 `s`。（字母数字字符串是指仅由小写英文字母和数字组成的字符串）  
请找出 `s` 的一种排列，使得 **任意相邻的两个字符类型不同**——即不存在字母后面紧跟另一个字母，也不存在数字后面紧跟另一个数字。  

返回满足条件的重新排列后的字符串。如果不存在任何可行的排列，则返回空字符串 `""`。

---

### 示例

#### 示例 1
**输入**  
``` 
s = "a0b1c2"
```  
**输出**  
```
"0a1b2c"
```  
**解释**  
在 `"0a1b2c"` 中，没有两个相邻字符属于同一种类型。`"a0b1c2"`、`"0a1b2c"`、`"0c2a1b"` 等也是合法的排列。

#### 示例 2
**输入**  
``` 
s = "leetcode"
```  
**输出**  
```
""
```  
**解释**  
字符串 `"leetcode"` 只包含字母，无法在字母之间插入数字，因此无法满足相邻字符类型不同的要求。

#### 示例 3
**输入**  
``` 
s = "1229857369"
```  
**输出**  
```
""
```  
**解释**  
字符串 `"1229857369"` 只包含数字，同理也无法满足相邻字符类型不同的要求。

---

### 约束

- `1 <= s.length <= 500`
- `s` 仅由小写英文字母和/或数字组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有字符的排列全枚举一遍，检查每一种排列是否满足「相邻字符类型不同」的条件。  
- **使用的数据结构**：`itertools.permutations` 可以一次性生成字符串的全排列，想象成「把所有字母和数字的拼图全部打乱」后一个一个拿出来尝试。  
- **为什么一定能得到答案**：如果题目有合法的重新排列，遍历所有排列必然会碰到它；如果遍历完都没有符合的，那就说明根本不存在。  

当然，这种方法在实际使用时几乎不可行，因为排列的数量会随字符串长度呈阶乘增长（`n!`），即使 `n=10` 也已经是 3,628,800 种可能了。

#### 代码（Python）

```python
import itertools

def reformat_brute(s: str) -> str:
    """
    暴力枚举所有排列，找到第一个满足相邻字符类型不同的返回，
    若遍历完都没有则返回空串。
    """
    # itertools.permutations 会返回一个迭代器，省去一次性把所有排列装进列表的内存开销
    for perm in itertools.permutations(s):
        # 将元组转成字符串，方便后面检查
        candidate = ''.join(perm)

        # 检查相邻字符类型是否不同
        ok = True
        for i in range(1, len(candidate)):
            # str.isdigit() 判断是否是数字，若两者相同则不符合要求
            if candidate[i].isdigit() == candidate[i-1].isdigit():
                ok = False
                break
        if ok:                     # 找到合法排列，直接返回
            return candidate
    return ""                     # 没有任何合法排列
```

#### 复杂度  

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是所有排列的数量，遍历每一种排列时还要检查 `n-1` 对相邻字符，整体是阶乘级别的。  
  - 用大白话说，就是「每多一个字符，可能的排列就会乘以当前字符数」，很快就会爆炸。

- **空间复杂度**：`O(n)`（不计 `itertools` 的内部迭代器开销）  
  - 只需要保存当前遍历到的排列（长度为 `n`），不需要额外的数组。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于「枚举所有排列」——根本不需要这么多尝试，只要把字母和数字交错排列即可。  

**关键观察**  
1. 只要字母数 `L` 与数字数 `D` 的差值不超过 1（`|L - D| ≤ 1`），就一定能把它们交错排成合法字符串。  
   - 想象字母和数字各自排成两条队列，交替取出一个放进结果。  
   - 若两条队列长度相差超过 1，必然会出现「连续取同一队列」的情况，导致相邻字符类型相同。  

2. 当 `L` 与 `D` 不相等时，**多的那一类必须先放**，否则会在最后剩下两个同类字符而无法继续交错。  

**实现步骤**  
- 先遍历一次字符串，分别把所有字母放进列表 `letters`，所有数字放进列表 `digits`。  
  - 这里的列表就像「字母仓库」和「数字仓库」，相当于查字典（哈希表）的过程，只是把相同类型的字符收集起来。  
- 检查 `abs(len(letters) - len(digits))` 是否大于 1，若是则直接返回空串。  
- 确定哪个列表先出（多的那个或任意一个当等长时），用两个指针 `i, j` 分别指向两个列表的当前位置。  
- 按顺序交叉取字符，构造结果字符串 `res`。  

**为什么一定对**  
- 交叉取字符保证了相邻的两位必然来自不同的列表，即类型不同。  
- 当长度相差不超过 1 时，交叉取完后不会出现「某列表提前耗尽」而导致后面只能取同类字符的情况。  

#### 代码（Python）

```python
def reformat(s: str) -> str:
    """
    最优解：先把字母和数字分开，再交叉合并。
    时间 O(n)，空间 O(n)（存放分离后的两个列表）。
    """
    letters = []          # 存放所有字母
    digits  = []          # 存放所有数字

    # 1️⃣ 分离字符
    for ch in s:
        if ch.isdigit():
            digits.append(ch)   # 数字放进 digits 仓库
        else:
            letters.append(ch)  # 字母放进 letters 仓库

    # 2️⃣ 判断是否可以交错
    if abs(len(letters) - len(digits)) > 1:
        return ""               # 差距太大，必然无法满足相邻不同

    # 3️⃣ 决定先出哪类字符
    # 若字母多或两者相等且字母先（任选），则 letters 先；否则 digits 先
    first_is_letter = len(letters) >= len(digits)

    i = j = 0                   # i 指向 letters，j 指向 digits
    res = []                    # 用列表收集字符，最后一次性 join 提高效率

    # 4️⃣ 交叉取字符
    while i < len(letters) or j < len(digits):
        if first_is_letter:
            if i < len(letters):
                res.append(letters[i])
                i += 1
            if j < len(digits):
                res.append(digits[j])
                j += 1
        else:   # 先放数字
            if j < len(digits):
                res.append(digits[j])
                j += 1
            if i < len(letters):
                res.append(letters[i])
                i += 1

    return ''.join(res)         # 把列表拼成最终字符串
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次原字符串进行分离（`O(n)`），随后一次线性合并，同样是 `O(n)`。  
  - 与暴力解的 `O(n! * n)` 相比，简直是「从宇宙级别降到日常级别」。

- **空间复杂度**：`O(n)`  
  - 需要额外存放分离后的字母列表和数字列表（总长度仍是 `n`），以及结果列表。  
  - 用大白话说，就是「把原来的字符重新排个队」而不是「把所有可能的队形都列出来」。

---

## 心得  

- **核心技巧**：先统计并分离不同类型的元素，再根据「数量差 ≤ 1」的条件决定是否可以交错排列。  
- **适用的题型**  
  1. 「交错排列」类题目，如 LeetCode 1417. Reformat The String（本题）。  
  2. 「重新组织字符」类题，如把 `R`、`G`、`B` 三种颜色交错排列的题目。  
  3. 「队列合并」类题，如把两条已排序的链表交叉合并（思路相似）。  
- **一句话总结**：**只要两类字符数量相差不超过 1，就能把「多的那类」先放，再交替取出即可**。

---

## 反思  

- **第一反应**：看到「相邻字符类型不同」立刻想到「交叉」或「交替」的排列方式。  
- **最容易踩的坑**  
  - 忽视长度差为 1 时必须让「多的那类」先出现，否则最后会剩下两个相同类型的字符导致失败。  
  - 边界情况：字符串全是字母或全是数字，此时直接返回空串。  
- **下次遇到同类题**：第一步先**统计每类元素的数量**，判断是否满足「数量差 ≤ 1」的可行性，再决定交叉合并的起始顺序。