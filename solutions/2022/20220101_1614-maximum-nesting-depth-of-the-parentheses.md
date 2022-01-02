# #1614. **括号的最大嵌套深度** / Maximum Nesting Depth of the Parentheses

> 难度：简单 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/)

---

## 题目（英文原版）

**Description**

Given a valid parentheses string s, return the nesting depth of s. The nesting depth is the maximum number of nested parentheses.

**Examples**

**Example 1:**

```
Input: s = "(1+(2*3)+((8)/4))+1"
Output: 3
Explanation:
Digit 8 is inside of 3 nested parentheses in the string.
```

**Example 2:**

```
Input: s = "(1)+((2))+(((3)))"
Output: 3
Explanation:
Digit 3 is inside of 3 nested parentheses in the string.
```

**Example 3:**

```
Input: s = "()(())((()()))"
Output: 3
```

**Constraints**

- 1 <= s.length <= 100
- s consists of digits 0-9 and characters '+', '-', '*', '/', '(', and ')'.
- It is guaranteed that parentheses expression s is a VPS.

---

## 题目（中文翻译）

给定一个有效的括号字符串（valid parentheses string）`s`，返回 `s` 的嵌套深度。嵌套深度指的是括号的最大嵌套层数。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= s.length <= 100`  
- `s` 只包含数字 `0-9` 以及字符 `'+'`, `'-'`, `'*'`, `'/'`, `'('`, `')'`。  
- 已保证括号表达式 `s` 是一个有效的括号字符串（VPS）。

---

### 示例

**示例 1**  
``` 
Input: s = "(1+(2*3)+((8)/4))+1"
Output: 3
Explanation:
数字 8 在字符串中被 3 层括号嵌套。
```

**示例 2**  
``` 
Input: s = "(1)+((2))+(((3)))"
Output: 3
Explanation:
数字 3 在字符串中被 3 层括号嵌套。
```

**示例 3**  
``` 
Input: s = "()(())((()()))"
Output: 3
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对字符串里的每一个字符，都算一遍它左边有多少左括号 `(`，右边有多少右括号 `)`，二者的差就是它所在的层数**。  
把所有字符的层数取最大值，就是答案。

- **用到的数据结构**：只需要遍历字符串，用两个循环；不需要额外的数据结构。可以把“遍历一次算层数”想象成在一排书本里，**每次都重新数一遍左边有几本书**，显然很费时。
- **为什么正确**：层数的定义恰好是“左括号的数量 - 右括号的数量”。我们对每个位置都这么算，必然得到真实的层数，最大层数自然就是嵌套深度。
- **时间/空间复杂度**：  
  - 外层遍历 `n` 次，内层每次又要遍历一次来统计左括号数，最坏情况是 `O(n²)`（比如长度 100 的字符串，100×100 次计数）。  
  - 只用了几个整数变量，空间是 `O(1)`（常数级）。

> **大白话**：`O(n²)` 就像你要在一条长队里，每次都从队首重新数到你所在的位置，队伍越长，数的次数就呈平方增长。

#### 代码（Python）

```python
def maxDepth_bruteforce(s: str) -> int:
    n = len(s)
    max_depth = 0

    # 对每一个字符 i，重新统计它左边的 '(' 个数
    for i in range(n):
        left_cnt = 0          # 左括号计数器
        right_cnt = 0         # 右括号计数器（可以省略，只用 left_cnt - right_cnt）

        # 统计位置 i 前面的所有字符
        for j in range(i + 1):          # 包含 i 本身，这样 '(' 也会被计入
            if s[j] == '(':
                left_cnt += 1
            elif s[j] == ')':
                right_cnt += 1

        # 当前字符的层数 = 左括号数 - 右括号数
        cur_depth = left_cnt - right_cnt
        max_depth = max(max_depth, cur_depth)

    return max_depth
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要两层循环，外层 `n` 次，内层平均也要遍历 `n/2` 次，整体是平方级别。  
- **空间复杂度**：`O(1)` — 只用了常数个整型变量，和输入长度无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于每次都要重新统计左括号的数量**。其实我们可以**一次遍历中实时维护**当前的层数：

1. **左括号 `(` 出现时**，层数 +1。  
2. **右括号 `)` 出现时**，层数 -1（因为对应的左括号已经结束了）。  
3. **遍历过程中记录出现过的最大层数**，这就是答案。

这相当于把“计数”这件事放进了 **栈** 的概念里：每遇到一个左括号，就把它压进栈；右括号弹出栈。栈的大小（即当前层数）随时可以拿来比较。**实际实现时我们不必真的建栈，只要一个整数 `depth` 就够了**——因为我们只关心栈的高度，而不需要保存具体的括号。

> **类比**：想象你在爬楼梯，左括号是“一步向上”，右括号是“一步向下”。只要记住你爬到最高的第几层，就是答案。

#### 代码（Python）

```python
def maxDepth_optimal(s: str) -> int:
    cur_depth = 0   # 当前所在的括号层数
    max_depth = 0   # 迄今为止出现的最大层数

    for ch in s:
        if ch == '(':
            cur_depth += 1          # 左括号，层数加一
            max_depth = max(max_depth, cur_depth)  # 更新最大层数
        elif ch == ')':
            cur_depth -= 1          # 右括号，层数减一
            # 此处不需要更新 max_depth，因为层数只会在 '(' 时增加

    return max_depth
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只需要一次线性遍历，字符数多少就多少次操作。相比 `O(n²)`，速度提升显著。  
- **空间复杂度**：`O(1)` — 只用了两个整数变量，和字符串长度无关。

---

## 心得

- **核心技巧**：**一次遍历实时维护括号深度（相当于栈的高度）**。  
- **适用的题型**  
  1. 判断括号字符串是否合法（使用栈或计数）。  
  2. 计算最小括号插入次数使表达式合法（同样需要计数当前深度）。  
  3. 统计最长有效括号子串的长度（需要栈或 DP）。  
- **解题钥匙**：**把“左括号是进栈、右括号是出栈”这一步抽象成一个整数的增减**，不必真的维护整个栈。

## 反思

- **第一反应**：看到“嵌套深度”，自然想到“数数左括号出现的次数”。  
- **最容易踩的坑**  
  - 忘记在遇到右括号时要 **先** `depth -= 1`（否则可能出现负数）。  
  - 对空字符串或只有括号的情况要保证返回 0（但本题已保证长度 ≥ 1 且是合法表达式）。  
- **下次类似题的第一步**：**先思考是否可以用一个计数器一次遍历得到答案**，如果计数器足够表达需求，就不必使用真正的栈或更复杂的数据结构。