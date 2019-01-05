# #224. 基本计算器 / Basic Calculator

> 难度：困难 · 标签：Math、String、Stack、Recursion · [LeetCode 链接](https://leetcode.com/problems/basic-calculator/)

---

## 题目（英文原版）

**Description**

Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.
Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

**Examples**

**Example 1:**

```
Input: s = "1 + 1"
Output: 2
```

**Example 2:**

```
Input: s = " 2-1 + 2 "
Output: 3
```

**Example 3:**

```
Input: s = "(1+(4+5+2)-3)+(6+8)"
Output: 23
```

**Constraints**

- 1 <= s.length <= 3 * 105
- s consists of digits, '+', '-', '(', ')', and ' '.
- s represents a valid expression.
- '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
- '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
- There will be no two consecutive operators in the input.
- Every number and running calculation will fit in a signed 32-bit integer.

---

## 题目（中文翻译）

给定一个字符串 `s`（string s），它表示一个 **有效表达式**（valid expression），请实现一个 **基本计算器**（basic calculator）来计算该表达式的值，并返回计算结果。  
**注意**：禁止使用任何能够将字符串直接求值的内置函数（built-in function），例如 `eval()`。

### 示例

**示例 1**  
**输入**: `s = "1 + 1"`  
**输出**: `2`

**示例 2**  
**输入**: `s = " 2-1 + 2 "`  
**输出**: `3`

**示例 3**  
**输入**: `s = "(1+(4+5+2)-3)+(6+8)"`  
**输出**: `23`

### 约束条件

- `1 <= s.length <= 3 * 10^5`
- `s` 仅由数字、字符 `'+'`、`'-'`、`'('`、`')'` 和空格组成。
- `s` 表示一个 **有效表达式**（valid expression）。
- `'+'` 不会作为一元运算符使用（即 `"+1"` 与 `"+(2 + 3)"` 均为非法）。
- `'-'` 可以作为一元运算符使用（即 `"-1"` 与 `"-(2 + 3)"` 为合法）。
- 输入中不会出现两个连续的运算符。
- 每个数字及所有中间计算结果均能在有符号 32 位整数范围内表示。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一对括号单独算出来**，把算好的结果再代入原表达式，循环这个过程直到没有括号为止。  

具体步骤：

1. **去掉空格**，因为空格不参与计算，只是让人看得更舒服。  
2. 在当前字符串里**找到最左边的 '('**，再向后找它对应的 ')'（这一步要一次一次遍历，最坏会遍历整串）。  
3. 把这对括号之间的子串递归地交给同样的算法求值（这里会再次去找子串里的 '('，于是会产生大量重复遍历）。  
4. 把子串的结果（一个整数）用 **字符串** 的形式替换掉原来的 "(子串)"，得到一个更短的表达式。  
5. 当表达式里再也没有 '(' 时，剩下的就只有数字、‘+’、‘-’，这时直接从左到右累加即可。

> **类比**：把表达式想象成一本书，先把最里面的章节（最内层的括号）读完、写下结果，然后把这段文字删掉、用结果替换，继续读下一章节，直到整本书读完。

这个方法之所以能得到正确答案，是因为算式的**运算顺序**恰好由括号决定，而我们每次都把最里层的括号先算完，符合数学的先后顺序。

不过，**每找一对括号都要从头遍历一次**，所以时间会呈二次方增长。

#### 代码（Python）

```python
def calculate_brute(s: str) -> int:
    # 1. 去掉所有空格，方便后面处理
    expr = s.replace(' ', '')

    # 2. 递归求值函数
    def eval_expr(sub: str) -> int:
        # 若子串里没有 '('，直接线性计算 + / -
        if '(' not in sub:
            total, num, sign = 0, 0, 1   # sign = 1 表示正，-1 表示负
            i = 0
            while i < len(sub):
                ch = sub[i]
                if ch.isdigit():
                    # 读取完整的数字
                    num = 0
                    while i < len(sub) and sub[i].isdigit():
                        num = num * 10 + int(sub[i])
                        i += 1
                    total += sign * num
                    continue
                elif ch == '+':
                    sign = 1
                else:               # ch == '-'
                    sign = -1
                i += 1
            return total

        # 3. 找到最左侧的 '(' 以及对应的 ')'
        left = sub.find('(')
        # 为了找到匹配的右括号，需要计数 '(' 的出现次数
        cnt = 0
        for right in range(left, len(sub)):
            if sub[right] == '(':
                cnt += 1
            elif sub[right] == ')':
                cnt -= 1
                if cnt == 0:          # 第一次 cnt 归零时即为匹配的 ')'
                    break

        # 4. 递归计算括号内部的值
        inner_val = eval_expr(sub[left + 1:right])

        # 5. 用计算结果替换原来的 "(...)"，得到更短的表达式
        new_expr = sub[:left] + str(inner_val) + sub[right + 1:]

        # 6. 继续递归求值
        return eval_expr(new_expr)

    return eval_expr(expr)
```

> 关键点已用中文注释，代码可以直接运行。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  最坏情况下，每一次寻找匹配括号都要从字符串开头遍历一次，而字符串的长度会逐步减小，但整体仍然是二次级别。可以把 `O(n²)` 想象成“如果有 10,000 个字符，需要大约 100,000,000 次基本操作”，在大数据下会明显慢。

- **空间复杂度**：`O(n)`  
  递归深度最多等于括号的层数，最坏是 `n/2`（每两个字符是一对括号），再加上临时生成的新字符串，总体在同量级 `n`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要重新遍历整个字符串去匹配括号**。如果我们在一次遍历中就把所有信息记录下来，就可以避免重复扫描。

本题只有两种运算符 `+`、`-`，且 **没有乘除的优先级**，所以可以用 **“符号栈 + 结果累计”** 的思路一次遍历完成计算。

核心想法：

1. **用一个整数 `sign` 记录当前数字前面的符号**（`+` → `1`，`-` → `-1`）。  
2. **用 `result` 累计到目前为止的计算结果**。当读到一个完整的数字时，`result += sign * number`。  
3. 遇到左括号 `(` 时，**把当前的 `result` 与 `sign` 入栈**，并把 `result` 重置为 `0`，`sign` 重置为 `1`，相当于进入一个新的子表达式。  
4. 遇到右括号 `)` 时，**弹出栈顶的 `sign` 与之前的 `result`**，把本层的 `result` 先乘以弹出的 `sign`（因为子表达式的整体符号可能是 `-`），再加到弹出的 `result` 上，得到合并后的累计值。  
5. 空格直接跳过。

> **类比**：把计算过程想象成“记账本”。`result` 是当前账本的余额，`sign` 是本次记账的方向（收入或支出）。左括号相当于打开一本新账本，右括号则把新账本的余额结算回上一页。

这个过程只需要一次线性扫描，**每个字符只看一次**，所以时间是 `O(n)`，空间只需要保存括号层数对应的 `result` 与 `sign`（最坏 `O(n)`，但一般远小于 `n`）。

#### 代码（Python）

```python
def calculate(s: str) -> int:
    """
    一遍扫描求值
    思路：使用栈保存遇到 '(' 时的累计结果和符号
    """
    stack = []          # 用来保存 (result, sign) 的元组
    result = 0          # 当前累计的结果
    sign = 1            # 当前数字前的符号，+ 为 1，- 为 -1
    i = 0
    n = len(s)

    while i < n:
        ch = s[i]

        if ch.isdigit():
            # 读取完整的数字（可能有多位）
            num = 0
            while i < n and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            # 计算到累计结果中
            result += sign * num
            # 这里 i 已经指向下一个非数字字符，continue 跳过 i += 1
            continue

        elif ch == '+':
            sign = 1                # 正号
        elif ch == '-':
            sign = -1               # 负号
        elif ch == '(':
            # 把当前的累计结果和符号压栈，进入新层级
            stack.append((result, sign))
            # 重置为新层级的初始状态
            result = 0
            sign = 1
        elif ch == ')':
            # 弹出上层的累计结果和符号
            prev_result, prev_sign = stack.pop()
            # 先把本层的 result 按本层符号(prev_sign) 合并到上层
            result = prev_result + prev_sign * result
        # 空格直接忽略
        i += 1

    return result
```

> 代码每一步都有中文解释，直接复制即可运行。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，`n` 是字符数。可以把它想象成“每个字符只处理一次”，即使是 300,000 长的表达式也只会进行 300,000 次基本操作，速度非常快。

- **空间复杂度**：`O(n)`（最坏）  
  栈的深度等于括号的最大嵌套层数。若表达式全是 `(`，则栈会存 `n/2` 个元素。实际使用时通常远小于 `n`。

---

## 心得

- **核心技巧**：利用**符号栈**（或递归）一次遍历完成带括号的加减运算。  
- **适用场景**：  
  1. 只含 `+`、`-`、括号的表达式求值（如 LeetCode 224）。  
  2. “带括号的前缀/后缀表达式求值”或“简化版的计算器”。  
  3. 需要在一次扫描中处理**嵌套结构**（如括号匹配、表达式求值）的题目。  
- **一句话总结**：**把每一层的累计结果和符号压栈，遇右括号时弹出合并——一次遍历搞定所有层级。**

---

## 反思

- **第一反应**：看到括号就想到递归或栈，先把最里层算出来再向外合并。  
- **最容易踩的坑**：  
  - 负号作为**一元运算**（如 `-(1+2)`）时，需要把它当作子表达式整体的符号保存。  
  - 多位数的读取：如果只读取单个字符会把 `12` 当成 `1` 与 `2`。  
  - 空格的处理：忘记跳过会导致 `int(' ')` 报错。  
- **下次遇到同类题**：第一步先**确认运算符优先级**（本题只有加减），然后决定是“一次遍历 + 栈”还是“多遍历 + 递归”。如果只有加减，优先考虑**符号栈**方案。