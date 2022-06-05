# #1805. 字符串中不同整数的数量 / Number of Different Integers in a String

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/number-of-different-integers-in-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string word that consists of digits and lowercase English letters.
You will replace every non-digit character with a space. For example, "a123bc34d8ef34" will become " 123  34 8  34". Notice that you are left with some integers that are separated by at least one space: "123", "34", "8", and "34".
Return the number of different integers after performing the replacement operations on word.
Two integers are considered different if their decimal representations without any leading zeros are different.

**Examples**

**Example 1:**

```
Input: word = "a123bc34d8ef34"
Output: 3
Explanation: The three different integers are "123", "34", and "8". Notice that "34" is only counted once.
```

**Example 2:**

```
Input: word = "leet1234code234"
Output: 2
```

**Example 3:**

```
Input: word = "a1b01c001"
Output: 1
Explanation: The three integers "1", "01", and "001" all represent the same integer because
the leading zeros are ignored when comparing their decimal values.
```

**Constraints**

- 1 <= word.length <= 1000
- word consists of digits and lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含数字和小写英文字母的字符串 `word`。  
你需要将每个非数字字符（non-digit character）替换为空格。  
例如，`"a123bc34d8ef34"` 替换后会得到 `" 123  34 8  34"`。  
注意，此时得到的整数之间至少被一个空格分隔，形成的整数序列为 `"123"`、`"34"`、`"8"` 和 `"34"`。

返回在对 `word` 完成上述替换操作后，不同整数的数量。  
如果两个整数去掉前导零（leading zeros）后的十进制表示相同，则视为相同的整数。

**示例 1**  
```text
Input: word = "a123bc34d8ef34"
Output: 3
Explanation: 不同的整数有 "123"、"34" 和 "8"。注意 "34" 只算一次。
```

**示例 2**  
```text
Input: word = "leet1234code234"
Output: 2
```

**示例 3**  
```text
Input: word = "a1b01c001"
Output: 1
Explanation: 整数 "1"、"01"、"001" 在去掉前导零后都表示相同的整数 1。
```

**约束条件**  
- `1 <= word.length <= 1000`  
- `word` 只由数字和小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把字母换成空格**  
   字母相当于“隔板”，把它们全部换成空格后，原来相邻的数字自然会被空格分开，就像把一段文字中的标点全部换成空格，单词就会被空格隔开一样。  

2. **按照空格把字符串切割**  
   Python 的 `split()` 方法会把连续的空格当成一个分隔符，直接得到所有只包含数字的子串。  

3. **去掉每个数字前面的零**  
   “001” 与 “1” 表示同一个整数，只要把左边的 `0` 删除即可。可以使用 `lstrip('0')`，如果全部是 `0`，把空串再恢复成 `"0"`。  

4. **放进集合去重**  
   集合（Hash Table）就像一本字典，里面只能出现不重复的词条。把处理好的数字字符串全部放进去，集合的大小就是不同整数的个数。  

> **为什么正确**  
> - 替换成空格后，所有数字都会被完整保留下来，且不会出现跨字母的数字。  
> - `split()` 按空格切割恰好得到每个整数的原始表示。  
> - 去掉前导零后得到的才是整数的唯一“标准形式”。  
> - 集合天然去重，统计不同整数就等价于统计不同的标准形式数量。

#### 代码（Python）

```python
def numDifferentIntegers(word: str) -> int:
    # 1️⃣ 把所有非数字字符换成空格
    #   isdigit() 判断字符是否是数字，若不是就换成空格
    transformed = ''.join(ch if ch.isdigit() else ' ' for ch in word)

    # 2️⃣ 按空格切割，得到所有只含数字的子串
    raw_numbers = transformed.split()

    # 3️⃣ 用集合保存去掉前导零后的标准形式
    uniq = set()
    for num in raw_numbers:
        # 去掉左侧的所有 '0'
        stripped = num.lstrip('0')
        # 如果全部是 '0'，lstrip 会得到空串，需要手动恢复成 "0"
        if stripped == '':
            stripped = '0'
        uniq.add(stripped)   # 加入集合，自动去重

    # 4️⃣ 集合大小就是不同整数的个数
    return len(uniq)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历了原字符串一次（`n` 为字符串长度），其余操作（`split`、`lstrip`、加入集合）都是对每个子串做线性工作，总体仍是线性时间。  
  用大白话说，就是“随字符串长度等比例增长”，不会出现 `n²` 那种“每个字符都要和每个字符比较”的情况。

- **空间复杂度**：`O(k)`  
  `k` 为不同整数的个数（最坏情况下每个字符都是数字且互不相同），需要把这些整数放进集合。额外的临时字符串也只和原字符串等长，所以总体是线性空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 `O(n)`，已经是最优时间复杂度了。但我们可以 **在一次遍历中直接完成所有工作**，省掉中间的 `split()` 和临时列表，进一步降低常数因子。

优化思路如下：

1. **一次遍历**  
   - 使用两个指针 `i`（遍历指针）和 `j`（记录当前数字子串的起始位置）。  
   - 当遇到数字时，继续向右移动 `i`，直到遇到非数字为止，此时 `[j, i)` 就是一个完整的数字子串。  

2. **即时去掉前导零**  
   - 在得到子串后，用 `lstrip('0')` 同样去除前导零，若全部是 `0` 再手动补成 `"0"`。  

3. **直接放进集合**  
   - 处理好的标准形式立即加入集合，无需额外的列表保存。  

这样只需要 **一次** 对字符的线性扫描，避免了 `split()` 产生的临时字符串列表，空间上也只保留集合本身。

#### 代码（Python）

```python
def numDifferentIntegers(word: str) -> int:
    uniq = set()          # 用来存放不同整数的标准形式
    n = len(word)
    i = 0                 # 主指针，遍历整个字符串

    while i < n:
        if word[i].isdigit():          # 遇到数字，开始收集一个整数
            j = i                       # 记录整数的起始位置
            while i < n and word[i].isdigit():
                i += 1                  # i 向右移动，直到非数字
            num = word[j:i]            # 提取子串 [j, i)
            # 去掉左侧的所有 0
            stripped = num.lstrip('0')
            if stripped == '':
                stripped = '0'
            uniq.add(stripped)          # 加入集合，自动去重
        else:
            i += 1                      # 当前字符是字母，直接跳过

    return len(uniq)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  仍然是一次线性遍历，每个字符只被访问一次。相比暴力解少了一次 `split()` 的额外遍历，常数更小。

- **空间复杂度**：`O(k)`  
  只存放不同整数的集合，`k` 为不同整数的个数。没有额外的临时列表或字符串数组。

---

## 心得

- **核心技巧**：一次遍历 + 哈希集合（去重） + 前导零规范化。  
- **适用场景**：  
  1. 把混合字符的字符串中抽取出某类子串并去重（如提取所有单词、所有 IP 地址等）。  
  2. 需要对数值字符串进行“标准化”后比较（比如去掉前导零、统一大小写）。  
  3. “把分隔符统一为同一种”再分割的技巧（把字母统一成空格）。  
- **解题钥匙**：**把问题转化为“把每个目标子串规范化后放进集合”**。

## 反思

- **第一反应**：把字母全部换成空格，直接 `split()`，然后用集合去重。  
- **最容易踩的坑**：  
  - 前导零全部被去掉后得到空串，需要手动恢复为 `"0"`。  
  - 连续的字母会产生多个空格，`split()` 会自动合并，但手写遍历时要注意跳过非数字字符。  
- **下次类似题的第一步**：**先确定“分隔符”**（本题是字母），把它们统一处理后再**一次遍历抽取目标子串**，随后**规范化并利用哈希表去重**。