# #736. 解析 Lisp 表达式 / Parse Lisp Expression

> 难度：困难 · 标签：Hash Table、String、Stack、Recursion · [LeetCode 链接](https://leetcode.com/problems/parse-lisp-expression/)

---

## 题目（英文原版）

**Description**

You are given a string expression representing a Lisp-like expression to return the integer value of.
The syntax for these expressions is given as follows.

**Examples**

**Example 1:**

```
Input: expression = "(let x 2 (mult x (let x 3 y 4 (add x y))))"
Output: 14
Explanation: In the expression (add x y), when checking for the value of the variable x,
we check from the innermost scope to the outermost in the context of the variable we are trying to evaluate.
Since x = 3 is found first, the value of x is 3.
```

**Example 2:**

```
Input: expression = "(let x 3 x 2 x)"
Output: 2
Explanation: Assignment in let statements is processed sequentially.
```

**Example 3:**

```
Input: expression = "(let x 1 y 2 x (add x y) (add x y))"
Output: 5
Explanation: The first (add x y) evaluates as 3, and is assigned to x.
The second (add x y) evaluates as 3+2 = 5.
```

**Constraints**

- 1 <= expression.length <= 2000
- There are no leading or trailing spaces in expression.
- All tokens are separated by a single space in expression.
- The answer and all intermediate calculations of that answer are guaranteed to fit in a 32-bit integer.
- The expression is guaranteed to be legal and evaluate to an integer.

---

## 题目（中文翻译）

## 描述
给定一个字符串 `expression`，表示一个类 Lisp 表达式，返回其计算得到的整数值。  
该类表达式的语法如下：

- `let` 表达式（let）：用于变量绑定，格式为 `(let <var1> <expr1> <var2> <expr2> … <exprN>)`。  
- `add` 表达式（add）：计算两个子表达式的和，格式为 `(add <expr1> <expr2>)`。  
- `mult` 表达式（mult）：计算两个子表达式的乘积，格式为 `(mult <expr1> <expr2>)`。  
- 变量名由小写字母组成，整数可以是正数或负数。  
- 表达式可以嵌套使用。

在 `let` 表达式中，变量的赋值按照出现顺序依次处理，后续的子表达式可以使用已绑定的变量。变量的作用域为 **从最近的 `let` 块向外**，即在查找变量值时会先检查最内层作用域，再逐层向外查找。

## 示例

### 示例 1
```
Input: expression = "(let x 2 (mult x (let x 3 y 4 (add x y))))"
Output: 14
Explanation: 在子表达式 `(add x y)` 中，需要获取变量 `x` 的值。  
查找时从最内层作用域开始，先找到 `x = 3`，因此 `x` 的值为 3。  
整个表达式计算过程为：`(let x 2 (mult 2 (let x 3 y 4 (add 3 4)))) = (mult 2 7) = 14`。
```

### 示例 2
```
Input: expression = "(let x 3 x 2 x)"
Output: 2
Explanation: `let` 语句中的赋值是按顺序依次处理的。  
先将 `x` 绑定为 3，随后又将 `x` 重新绑定为 2，最后返回变量 `x` 的值 2。
```

### 示例 3
```
Input: expression = "(let x 1 y 2 x (add x y) (add x y))"
Output: 5
Explanation: 第一个 `(add x y)` 计算得到 3，并将结果赋给 `x`。  
第二个 `(add x y)` 使用更新后的 `x = 3` 和 `y = 2`，计算得到 5，作为整个表达式的返回值。
```

## 约束条件
- `1 <= expression.length <= 2000`
- `expression` 不含首尾空格。
- `expression` 中的所有标记（token）均由单个空格分隔。
- 最终答案及所有中间计算结果均保证在 32 位整数范围内。
- 给定的表达式合法且一定会计算出一个整数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把整个表达式一次性拆成子串**，再递归求值。  
具体步骤如下：

1. **把表达式按空格和括号分割成 token**  
   - 如果遇到 `'('` 就一直往后读，直到对应的 `')'` 为止，这期间的所有字符都属于同一个 token（比如 `"(add 1 (mult 2 3))"`）。
   - 这样我们得到的 token 要么是整数/变量，要么是完整的子表达式（仍然以 `'('` 开头、以 `')'` 结尾）。

2. **递归求值**  
   - 若 token 以数字或 `'-'` 开头，直接 `int(token)`。
   - 若 token 以字母开头，说明是变量，去当前作用域（一个 `list` 里保存的 `dict`）里查找最近的定义。
   - 若 token 以 `'('` 开头，则根据第一个子 token 判断是哪种运算：
     - `add a b` → 递归求 `a`、`b`，返回和。
     - `mult a b` → 递归求 `a`、`b`，返回积。
     - `let v1 e1 v2 e2 … expr` → 依次求 `e1、e2 …`，把对应的 `v` 放进**新的作用域**（用 `dict` 保存），最后求 `expr`。

3. **作用域的实现**  
   - 用一个 **栈**（`list`）保存若干 `dict`，栈底是全局作用域，栈顶是当前最近的 `let` 块。
   - 查变量时从栈顶向下遍历，找到的第一条记录就是当前值（类似查字典：先在最近的章节找页码，再往前翻）。

**为什么正确**  
- 递归保证每一次都把最内部的子表达式先算完，符合 Lisp 的求值顺序。  
- 作用域栈保证了“内层变量会遮蔽外层同名变量”，正好对应题目中“从内向外查找变量”的要求。

**时间/空间复杂度（大白话）**  
- **时间**：每一次递归都要**重新遍历整个子串**来找 token，最坏情况下会出现 `n` 次递归，每次遍历 `≈ n` 长度的字符串 → `O(n²)`。可以想象为“每次都要把整本书重新翻一遍”。
- **空间**：递归深度最坏是 `n`（所有括号都嵌套），每层保存一个作用域字典 → `O(n)`。

#### 代码（Python）

```python
def evaluate(expression: str) -> int:
    # ---------- 辅助函数：把一个 '(' 开头的子表达式切成 token ----------
    def split_tokens(s: str):
        """返回 s 中最外层的 token 列表（不包括首尾的 '('、')'）"""
        tokens, i, bal = [], 0, 0
        start = 0
        while i < len(s):
            if s[i] == '(':
                bal += 1
            elif s[i] == ')':
                bal -= 1
            elif s[i] == ' ' and bal == 0:   # 空格且不在子括号内部 → 一个 token 结束
                tokens.append(s[start:i])
                start = i + 1
            i += 1
        tokens.append(s[start:i])  # 最后一个 token
        return tokens

    # ---------- 递归求值 ----------
    def dfs(expr: str, scopes: list) -> int:
        # 1) 直接是整数
        if expr[0].isdigit() or expr[0] == '-':
            return int(expr)

        # 2) 直接是变量
        if expr[0].isalpha():
            # 从最近的作用域往外找
            for scope in reversed(scopes):
                if expr in scope:
                    return scope[expr]
            raise ValueError(f"未定义的变量 {expr}")

        # 3) 复合表达式，以 '(' 开头
        # 去掉最外层的 '(' 与 ')'
        inner = expr[1:-1]
        tokens = split_tokens(inner)
        op = tokens[0]   # 第一个 token 必定是操作符

        if op == 'add':
            a = dfs(tokens[1], scopes)
            b = dfs(tokens[2], scopes)
            return a + b
        if op == 'mult':
            a = dfs(tokens[1], scopes)
            b = dfs(tokens[2], scopes)
            return a * b
        # let 表达式
        # 创建一个新的作用域（字典），并压入栈顶
        new_scope = {}
        scopes.append(new_scope)
        # 变量-表达式对是成对出现的，最后一个 token 是返回值
        i = 1
        while i < len(tokens) - 1:
            var = tokens[i]                # 变量名
            val_expr = tokens[i + 1]       # 对应的子表达式
            new_scope[var] = dfs(val_expr, scopes)
            i += 2
        # 最后一个 token 是整个 let 表达式的值
        result = dfs(tokens[-1], scopes)
        scopes.pop()   # 弹出当前作用域
        return result

    # 初始只有全局作用域（空字典）
    return dfs(expression, [{}])
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - “n²” 表示如果表达式长 2000，最坏情况下需要遍历 2000 × 2000 次字符。因为每层递归都要重新扫描整段子串来切 token。

- **空间复杂度**：`O(n)`  
  - 递归深度和作用域栈最多和字符数成正比，最坏会占用约 `n` 个栈帧和字典。

---

### 2. 最优解

#### 思路  
暴力解的主要瓶颈在于 **每一次递归都要重新遍历子串来切 token**，这导致了二次扫描。  
我们可以把表达式视作一条 **字符流**，用一个全局指针 `i` 从左到右一次遍历，**在遍历的过程中直接完成求值**，这样每个字符只看一次。

关键点如下：

| 步骤 | 解释 | 类比 |
|------|------|------|
| **一次遍历 + 指针** | 用 `i` 记录当前读取位置，递归函数 `parse()` 从 `i` 开始读取下一个完整的 token（整数、变量或子表达式），并把 `i` 移到 token 结束后的位置。 | 想象把表达式放在磁带上，指针只会往前走，不会回头。 |
| **作用域栈** | 同样使用 `list[dict]`，但在进入 `let` 时 **直接在栈顶写入**，离开时弹出。由于指针只往前走，作用域的进出恰好对应递归的进出。 | 像在厨房里开设临时的调味料抽屉，使用完后把抽屉收起来。 |
| **读取 token** | - 若当前字符是数字或 `-` → 读取完整整数。<br>- 若是字母 → 读取完整变量名。<br>- 若是 `'('` → 读取操作符后递归求子表达式。 | 类似在句子里识别“单词”和“短语”。 |
| **运算** | `add` 与 `mult` 只需要递归两次得到子值；`let` 需要循环读取 *变量‑表达式* 对，直到只剩最后一个表达式作为返回值。 | `let` 像“先给孩子们发糖，再让他们一起玩”。 |

由于每个字符只被读取一次，时间复杂度降到 **线性 O(n)**，空间仍为 **O(n)**（递归栈 + 作用域栈）。

#### 代码（Python）

```python
def evaluate(expression: str) -> int:
    # ---------- 全局指针 ----------
    i = 0                      # 读取位置，闭包中会被修改

    # ---------- 作用域栈 ----------
    scopes = [{}]              # 第一个字典是全局作用域

    # ---------- 辅助函数：读取下一个 token ----------
    def next_token() -> str:
        nonlocal i
        # 跳过可能出现的空格
        while i < len(expression) and expression[i] == ' ':
            i += 1
        if expression[i] == '(' or expression[i] == ')':
            # 单独的括号也是一个 token
            tok = expression[i]
            i += 1
            return tok
        # 读取连续的字母或数字（包括负号）
        start = i
        while i < len(expression) and expression[i] not in ' ()':
            i += 1
        return expression[start:i]

    # ---------- 主递归函数 ----------
    def parse() -> int:
        nonlocal i
        token = next_token()

        # 1) 整数
        if token[0].isdigit() or token[0] == '-':
            return int(token)

        # 2) 变量
        if token[0].isalpha() and token not in ('add', 'mult', 'let'):
            # 从最近的作用域往外找
            for scope in reversed(scopes):
                if token in scope:
                    return scope[token]
            raise ValueError(f"未定义的变量 {token}")

        # 3) '(' 开头的复合表达式
        # token 必定是 '('，下一个 token 是操作符
        op = next_token()

        if op == 'add':
            a = parse()
            b = parse()
            next_token()               # 读取对应的 ')'
            return a + b

        if op == 'mult':
            a = parse()
            b = parse()
            next_token()               # 读取对应的 ')'
            return a * b

        # let 表达式
        # 为当前 let 创建一个新作用域
        scopes.append({})
        # 读取若干 (var expr) 对，直到只剩一个 expr
        while True:
            # 看下一个 token 是变量名还是 ')'（表示结束）
            peek = expression[i]
            if peek == ')':            # let 结束，最后一个 expr 已经在栈顶
                break
            # 读取可能的变量名
            var = next_token()
            # 若下一个字符是 ')'，说明这是 let 的返回值
            if expression[i] == ')':
                # 把返回值算出来
                val = parse()
                scopes.pop()
                next_token()           # 把结尾的 ')' 吃掉
                return val
            # 否则读取对应的表达式并绑定到变量
            val = parse()
            scopes[-1][var] = val
        # 这里不应该到达，因为上面的循环已经在 ')' 前返回
        raise RuntimeError("Invalid let expression")

    # 入口：整个表达式一定是一个合法的 token
    return parse()
```

> **代码说明**  
> - `next_token()`：一次性读取下一个完整 token（包括独立的 '('、')'），并自动跳过空格。  
> - `parse()`：核心递归函数，根据 token 类型决定是直接返回整数、查变量、还是继续递归处理 `add`、`mult`、`let`。  
> - 作用域通过 `scopes.append({})` 与 `scopes.pop()` 在进入/离开 `let` 时自动管理。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个字符只被 `next_token` 读取一次，递归只在需要时进入子表达式，等价于“一次性读完整本书”。相较于暴力解的二次遍历，快了很多。

- **空间复杂度**：`O(n)`  
  - 递归深度最坏为表达式的嵌套层数（≤字符数），以及每层对应的作用域字典，仍然是线性空间。

---

## 心得

- **核心技巧**：使用**指针 + 单次遍历**的递归解析（相当于手写解释器），配合**作用域栈**实现变量的作用域管理。  
- **适用的题型**：  
  1. 解析类题目，如 `Basic Calculator III`（四则运算带括号）。  
  2. 带有嵌套作用域的语言解释器，如 “实现简易的 Scheme/Lisp 解释器”。  
  3. 需要一次遍历并即时求值的 “前缀/后缀表达式求值”。  
- **一句话总结**：**“把表达式看成字符流，指针只前进，递归自然完成括号配对和作用域管理”。**

---

## 反思

- **第一反应**：把整个字符串切成 token，递归求值——直观但会多次遍历子串。  
- **最容易踩的坑**：  
  - **变量遮蔽**：忘记在退出 `let` 时弹出对应的作用域，会导致外层变量被错误覆盖。  
  - **括号匹配**：手动计数平衡时容易漏掉最后的 `')'`，导致 token 切分错误。  
  - **空格处理**：表达式中空格恰好是分隔符，必须在读取 token 时跳过，否则会把空格当成字符。  
- **下次遇到同类题**：**先把输入看成“指针在走”，写一个 `next_token` 把下一个完整单元读出来，再在递归里根据运算符决定如何继续**。这样既避免重复扫描，又能自然维护作用域。