# #65. 有效数字 / Valid Number

> 难度：困难 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/valid-number/)

---

## 题目（英文原版）

**Description**

Given a string s, return whether s is a valid number.

For example, all the following are valid numbers: "2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7", "+6e-1", "53.5e93", "-123.456e789", while the following are not valid numbers: "abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53".
Formally, a valid number is defined using one of the following definitions:
An integer number is defined with an optional sign '-' or '+' followed by digits.
A decimal number is defined with an optional sign '-' or '+' followed by one of the following definitions:
An exponent is defined with an exponent notation 'e' or 'E' followed by an integer number.
The digits are defined as one or more digits.

**Examples**

**Example 1:**

```
Input: s = "0"
Output: true
```

**Example 2:**

```
Input: s = "e"
Output: false
```

**Example 3:**

```
Input: s = "."
Output: false
```

**Constraints**

- 1 <= s.length <= 20
- s consists of only English letters (both uppercase and lowercase), digits (0-9), plus '+', minus '-', or dot '.'.

---

## 题目（中文翻译）

给定一个字符串 `s`，返回 `s` 是否是一个有效数字。

例如，以下所有字符串都是有效数字：`"2"`、`"0089"`、`"-0.1"`、`"+3.14"`、`"4."`、`"-.9"`、`"2e10"`、`"-90E3"`、`"3e+7"`、`"+6e-1"`、`"53.5e93"`、`"-123.456e789"`，而以下字符串不是有效数字：`"abc"`、`"1a"`、`"1e"`、`"e3"`、`"99e2.5"`、`"--6"`、`"-+3"`、`"95a54e53"`。

形式上，一个**有效数字**需要满足以下任意一种定义：

- **整数（integer）**由可选的符号 `'-'` 或 `'+'`，后跟**数字（digits）**组成。  
- **小数（decimal）**由可选的符号 `'-'` 或 `'+'`，后跟以下任意一种形式：  
  - `digits '.'`（例如 `12.`）  
  - `'.' digits`（例如 `.34`）  
  - `digits '.' digits`（例如 `3.14`）  
- **指数（exponent）**由**指数表示法（exponent notation）**`'e'` 或 `'E'`，后跟**整数（integer）**构成。  
- **数字（digits）**定义为一个或多个数字字符。

**Example 1:**  
**Example 2:**  
**Example 3:**  

**Constraints:**

示例：

**示例 1:**  
Input: s = "0"  
Output: true  

**示例 2:**  
Input: s = "e"  
Output: false  

**示例 3:**  
Input: s = "."  
Output: false  

约束条件：  
- `1 <= s.length <= 20`  
- `s` 仅由英文字母（大小写均可）、数字 `0-9`、加号 `'+'`、减号 `'-'` 或点 `'.'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串交给 Python 自带的 `float()` 函数去尝试转成浮点数，如果能成功则说明它是一个合法的数，否则抛异常说明不合法。  

- **用到的数据结构**：仅仅是字符串本身。可以把 `float()` 看成一个“黑盒机器”，它会把我们写在纸上的“数字”交给内部的“词典”，如果词典里有对应的解释（比如 `"-12.3e+4"`），就能顺利返回数值；否则机器会报错，告诉我们“这根本不是数字”。  
- **为什么正确**：`float()` 的实现已经把所有合法的十进制表示、指数形式、正负号、空格等都处理得很完善。只要字符串满足题目定义，它一定能被成功解析。  
- **时间/空间复杂度**：  
  - **时间**：`float()` 需要一次遍历全部字符来判断合法性，等价于 **O(n)**（`n` 为字符串长度）。  
  - **空间**：只用了常数级别的临时变量，**O(1)**。  

> **大白话解释**：  
> - `O(n)` 就是说如果字符串有 10 个字符，程序大概会检查 10 次；如果有 1000 个字符，就会检查 1000 次，随字符数线性增长。  
> - `O(1)` 表示无论字符串多长，程序占用的额外内存几乎不变，就像只在桌子上放了一个小纸条。

#### 代码（Python）

```python
def isNumber_bruteforce(s: str) -> bool:
    """
    暴力思路：直接尝试把字符串转成 float
    如果成功则说明是合法数字，抛异常则不合法
    """
    try:
        # Python 的 float() 会自动忽略前后空格
        # 这里我们先把字符串两端的空格去掉，防止不必要的错误
        float(s.strip())
        return True
    except ValueError:
        # 转换失败，说明不是合法数字
        return False
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 程序会检查每个字符一次，字符越多，检查时间线性增长。  
- **空间复杂度**：`O(1)` — 只用了几个临时变量，额外占用的内存不随 `n` 增长。  

---

### 2. 最优解  

#### 思路  

虽然直接调用 `float()` 很简洁，但在面试中通常不被接受，因为它把“判断合法”这件事全交给了语言本身。我们需要 **自己** 实现一个判定器。  

**1）先找慢在哪里**  
最笨的实现往往是把所有合法形式列举出来，然后一个一个匹配（比如正则表达式）。正则虽然可以一次性完成，但阅读和调试都不友好，而且在极端情况下（回溯过多）会出现性能问题。  

**2）从字符逐个扫描出发**  
我们可以一次遍历字符串，记录下面几个关键状态：  

| 状态变量 | 含义 | 类比 |
|----------|------|------|
| `num_seen` | 已经出现过数字（0‑9） | 像在字典里已经查到“词条”了 |
| `dot_seen` | 已经出现过小数点 `.` | 只允许出现一次的“标点” |
| `e_seen`   | 已经出现过指数符号 `e`/`E` | 只能出现一次的“章节分隔符” |
| `num_after_e` | 指数符号后是否出现过数字 | 确保 `e` 后面真的跟了整数 |

遍历时遵守下面的规则：  

1. **空格**：题目没有明确说明可以有空格，但 LeetCode 原题允许两端空格。我们先 `strip()` 去掉两端空格，内部不允许出现空格。  
2. **符号 `+`/`-`**：只能出现在开头，或紧跟在 `e/E` 之后。  
3. **数字**：出现后把 `num_seen` 设为 `True`，如果在 `e` 之后出现，也把 `num_after_e` 设为 `True`。  
4. **小数点 `.`**：只能出现一次，且不能在 `e` 之后出现。出现后如果前后都没有数字（例如 `"."` 或 `"+."`）仍算非法。  
5. **指数 `e/E`**：只能出现一次，且必须在出现过数字之后（不能是 `"e"`、`".e"` 之类）。出现后把 `e_seen=True`，并重置 `num_after_e=False`，因为指数后必须再出现数字。  

遍历结束后，合法的条件是：

- 必须出现过数字（`num_seen` 为 `True`），  
- 如果出现了 `e/E`，则指数后也必须出现数字（`num_after_e` 为 `True`），  
- 小数点和指数的出现次数都不超过一次（我们在遍历时已经保证）。

**3）核心算法**：一次线性扫描 + 状态机（Finite State Machine）。  
状态机的好处是 **只看当前字符和几个布尔标记**，不需要回溯或递归，时间就是 `O(n)`，空间是 `O(1)`。

下面用 **类比** 来帮助理解：  
- 把字符串想象成一条河流，**数字** 是河里的水，**小数点**、**指数**、**符号** 是河岸上的桥或闸门。我们从左到右走，记住自己是否已经看到水、是否已经打开过闸门（指数），以及闸门是否已经关闭（不能再出现小数点）。只要一路上闸门、桥的使用规则符合规定，最后我们站在河的尽头就算成功。

#### 代码（Python）

```python
def isNumber_optimal(s: str) -> bool:
    """
    最优思路：一次线性扫描 + 状态机
    只使用几个布尔变量，空间 O(1)，时间 O(n)
    """
    s = s.strip()                     # 去掉首尾空格
    if not s:                         # 空字符串直接返回 False
        return False

    num_seen = False      # 是否出现过数字（0-9）
    dot_seen = False      # 是否出现过小数点 '.'
    e_seen = False        # 是否出现过指数符号 'e' 或 'E'
    num_after_e = True    # 指数后是否出现过数字，初始设为 True 防止没有 e 时影响结果

    for i, ch in enumerate(s):
        if ch.isdigit():                     # 当前字符是数字
            num_seen = True
            if e_seen:                       # 在 e 之后出现数字
                num_after_e = True
        elif ch in ['+', '-']:               # 符号只能在开头或 e 后面
            # 必须是第一个字符，或者紧跟在 e/E 之后
            if i != 0 and s[i - 1] not in ['e', 'E']:
                return False
        elif ch == '.':                      # 小数点
            # 已经出现过小数点或已经出现过 e，非法
            if dot_seen or e_seen:
                return False
            dot_seen = True
        elif ch in ['e', 'E']:               # 指数符号
            # 已经出现过 e，或前面还没有数字，非法
            if e_seen or not num_seen:
                return False
            e_seen = True
            num_after_e = False               # 需要在 e 后面再次出现数字
        else:                                 # 其他字符直接非法
            return False

    # 最后检查：必须出现过数字，且如果出现了 e，e 后也必须有数字
    return num_seen and num_after_e
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历一次字符串，字符越多检查次数线性增长。相较于暴力的 `float()`，我们自己控制了每一步的操作，最坏情况仍是一次遍历。  
- **空间复杂度**：`O(1)` — 只用了固定数量的布尔变量，和字符串长度无关。  

---

## 心得  

- **核心技巧**：**一次遍历的状态机**（记录是否出现数字、小数点、指数以及指数后是否有数字）。  
- **适用的题型**：  
  1. 判断合法的 **IP 地址**（需要记录点的数量、每段是否为数字）。  
  2. 判断合法的 **括号匹配**（使用栈记录状态）。  
  3. 判断合法的 **路径字符串**（如 Unix 路径规范）。  
- **一句话总结解题钥匙**：**只要把合法的“出现顺序”和“出现次数”用布尔变量记录下来，线性扫描即可完成判断**。

---

## 反思  

- **第一反应**：直接想到 `float()`，因为 Python 已经帮我们实现了完整的数字解析。  
- **最容易踩的坑**：  
  - 忘记处理 **指数后必须有数字**（如 `"1e"` 是非法的）。  
  - 小数点只能出现一次且不能在 `e` 之后（如 `"1e.5"`）。  
  - 符号只能在开头或紧跟在 `e/E` 之后（如 `"--6"`、`"+-3"`）。  
  - 两端空格需要先 `strip()`，内部空格直接判非法。  
- **下次遇到同类题**，第一步应该想到 **“把字符串分成几块，每块有什么合法的组成元素”**，然后 **用布尔变量记录每块是否出现**，最后 **一次遍历结束后检查所有必需条件**。这样既直观又高效。