# #1324. 垂直打印单词 / Print Words Vertically

> 难度：中等 · 标签：Array、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/print-words-vertically/)

---

## 题目（英文原版）

**Description**

Given a string s. Return all the words vertically in the same order in which they appear in s.
Words are returned as a list of strings, complete with spaces when is necessary. (Trailing spaces are not allowed).
Each word would be put on only one column and that in one column there will be only one word.

**Examples**

**Example 1:**

```
Input: s = "HOW ARE YOU"
Output: ["HAY","ORO","WEU"]
Explanation: Each word is printed vertically. 
 "HAY"
 "ORO"
 "WEU"
```

**Example 2:**

```
Input: s = "TO BE OR NOT TO BE"
Output: ["TBONTB","OEROOE","   T"]
Explanation: Trailing spaces is not allowed. 
"TBONTB"
"OEROOE"
"   T"
```

**Example 3:**

```
Input: s = "CONTEST IS COMING"
Output: ["CIC","OSO","N M","T I","E N","S G","T"]
```

**Constraints**

- 1 <= s.length <= 200
- s contains only upper case English letters.
- It's guaranteed that there is only one space between 2 words.

---

## 题目（中文翻译）

给定一个字符串 **s**，返回所有单词（word）按它们在 **s** 中出现的顺序竖直排列的结果。  
返回的结果是一个字符串列表（list of strings），必要时需要在字符串中补充空格（space），但**不允许出现尾随空格**（trailing spaces）。  
每个单词只占用一列（column），且每列只能出现一个单词。

**示例 1**  
**输入**: `s = "HOW ARE YOU"`  
**输出**: `["HAY","ORO","WEU"]`  
**解释**: 每个单词被竖直打印。  
```
HAY
ORO
WEU
```

**示例 2**  
**输入**: `s = "TO BE OR NOT TO BE"`  
**输出**: `["TBONTB","OEROOE","   T"]`  
**解释**: 不允许出现尾随空格。  
```
TBONTB
OEROOE
   T
```

**示例 3**  
**输入**: `s = "CONTEST IS COMING"`  
**输出**: `["CIC","OSO","N M","T I","E N","S G","T"]`  

**约束条件**  
- `1 <= s.length <= 200`  
- `s` 仅包含大写英文字母。  
- 保证相邻两个单词之间只有一个空格。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把字符串 `s` 按空格切成若干单词，例如 `"HOW ARE YOU"` → `["HOW","ARE","YOU"]`。  
我们把这些单词想象成一张 **表格**，每个单词占一列，列的高度取决于最长单词的长度。  

```
H O W
A R E
Y O U
```

把表格的每一行拼接起来，就是答案。  
实现时可以：

1. 记录所有单词的最大长度 `max_len`（相当于表格的行数）。  
2. 用两层循环：外层遍历 `0 … max_len-1`（行），内层遍历所有单词（列）。  
   - 如果当前单词的第 `i` 个字符存在，就把它加入本行字符串；  
   - 否则加入一个空格 `' '`，占位保持列对齐。  
3. 每行拼完后，用 `rstrip()` 去掉**右侧**的多余空格（题目不允许行尾有空格），再放入结果列表。

> **类比**：  
> 哈希表像一本字典，`key` 是单词，`value` 是对应的行号。这里我们不需要哈希表，只是把单词“排成表格”，再按行读取。

#### 代码（Python）

```python
def printVertically(s: str) -> list[str]:
    # 1. 把句子切成单词
    words = s.split()                       # ["HOW","ARE","YOU"]
    max_len = max(len(w) for w in words)    # 3

    res = []                                 # 用来存放每一行的结果

    # 2. 按行遍历
    for i in range(max_len):                 # i = 0,1,2
        cur = []                             # 暂存本行的字符
        for w in words:                      # 依次处理每一列
            # 如果第 i 个字符存在，就取出来；否则放空格占位
            cur.append(w[i] if i < len(w) else ' ')
        # 把本行字符拼成字符串，并去掉右侧多余的空格
        res.append(''.join(cur).rstrip())
    return res
```

#### 复杂度

- **时间复杂度**：`O(L * n)`  
  - `L` 为最长单词的长度，`n` 为单词个数。  
  - 可以把它想成“表格里有 `L` 行 `n` 列”，我们要遍历每个格子一次。  
- **空间复杂度**：`O(L * n)`（用于存放结果）  
  - 结果本身就是 `L` 行，每行最多 `n` 个字符，所以需要这么多空间。  

---

### 2. 最优解

#### 思路  

暴力解已经是最直接的思路，实际运行时并没有多余的开销。  
唯一可以**进一步简化**的地方是：

- 不必显式地把每行字符先放进列表 `cur`，可以在遍历列的过程中直接往字符串 `row` 追加。  
- 由于 Python 的字符串拼接在循环里效率略低（每次都会创建新对象），我们仍然使用列表收集字符，最后一次性 `join`，这已经是最优的做法。  

因此，**最优解**和暴力解在时间复杂度上是一样的，只是代码更简洁、可读性更好。

实现要点：

1. 仍然先得到单词列表和最长长度 `max_len`。  
2. 使用列表推导式一次性生成每行的字符序列：`[w[i] if i < len(w) else ' ' for w in words]`。  
3. `''.join(...)` 把字符列表变成字符串，再 `rstrip()` 去掉右侧空格。  

#### 代码（Python）

```python
def printVertically(s: str) -> list[str]:
    words = s.split()
    max_len = max(map(len, words))          # 一行代码得到最长单词长度

    # 使用列表推导式一次生成每一行
    return [
        ''.join(w[i] if i < len(w) else ' ' for w in words).rstrip()
        for i in range(max_len)
    ]
```

#### 复杂度

- **时间复杂度**：`O(L * n)`  
  - 与暴力解相同，只是写法更紧凑。  
  - 仍然是遍历“表格的每个格子”。  
- **空间复杂度**：`O(L * n)`  
  - 需要存放返回的 `L` 行字符串。  

---

## 心得

- 这道题考察的核心技巧是 **“按列遍历字符串”**（即把行列概念调换），常用在**矩阵转置**、**竖向打印**等场景。  
- 类似技巧常见于以下题目：  
  1. **LeetCode 443. String Compression**（需要按字符顺序压缩）  
  2. **LeetCode 151. Reverse Words in a String**（把单词倒序）  
  3. **LeetCode 271. Encode and Decode Strings**（需要逐字符处理）  
- **一句话总结解题钥匙**：先确定“最大行数”，再按行逐列收集字符，最后去掉每行右侧的空格。

## 反思

- **第一反应**：把句子拆成单词，想象成表格，然后逐行读取。  
- **最容易踩的坑**：  
  - **忘记去掉行尾空格**，会导致答案不符合 “Trailing spaces are not allowed”。  
  - **单词长度不一**，需要判断当前列是否还有字符，否则补空格。  
  - **极端情况**：只有一个单词或所有单词长度相同，都应能正常输出。  
- **下次遇到同类题**，第一步应该先**找出整体的尺寸（行数/列数）**，再**按行或按列构造答案**，并记得处理好“多余的空格或填充”。