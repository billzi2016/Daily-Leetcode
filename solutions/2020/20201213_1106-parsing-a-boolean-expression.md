# #1106. 解析布尔表达式 / Parsing A Boolean Expression

> 难度：困难 · 标签：String、Stack、Recursion · [LeetCode 链接](https://leetcode.com/problems/parsing-a-boolean-expression/)

---

## 题目（英文原版）

**Description**

A boolean expression is an expression that evaluates to either true or false. It can be in one of the following shapes:
Given a string expression that represents a boolean expression, return the evaluation of that expression.
It is guaranteed that the given expression is valid and follows the given rules.

**Examples**

**Example 1:**

```
Input: expression = "&(|(f))"
Output: false
Explanation: 
First, evaluate |(f) --> f. The expression is now "&(f)".
Then, evaluate &(f) --> f. The expression is now "f".
Finally, return false.
```

**Example 2:**

```
Input: expression = "|(f,f,f,t)"
Output: true
Explanation: The evaluation of (false OR false OR false OR true) is true.
```

**Example 3:**

```
Input: expression = "!(&(f,t))"
Output: true
Explanation: 
First, evaluate &(f,t) --> (false AND true) --> false --> f. The expression is now "!(f)".
Then, evaluate !(f) --> NOT false --> true. We return true.
```

**Constraints**

- 1 <= expression.length <= 2 * 104
- expression[i] is one following characters: '(', ')', '&', '|', '!', 't', 'f', and ','.

---

## 题目（中文翻译）

布尔表达式（boolean expression）是一种求值结果为 `true` 或 `false` 的表达式。它可以是以下几种形式之一：

- `t` 表示 **真**（true）  
- `f` 表示 **假**（false）  
- `!(subExpr)` 表示对 `subExpr` 进行 **非**（NOT）运算  
- `&(subExpr1,subExpr2,…)` 表示对所有子表达式进行 **与**（AND）运算  
- `|(subExpr1,subExpr2,…)` 表示对所有子表达式进行 **或**（OR）运算  

给定一个字符串 `expression`，它表示一个合法的布尔表达式，请返回该表达式的求值结果。

保证输入的表达式合法且符合上述规则。

## 示例

**示例 1**  
输入: `expression = "&(|(f))"`  
输出: `false`  
解释:  
1. 先计算 `|(f)` → `f`，表达式变为 `"&(f)"`。  
2. 再计算 `&(f)` → `f`，表达式变为 `"f"`。  
3. 最终返回 `false`。

**示例 2**  
输入: `expression = "|(f,f,f,t)"`  
输出: `true`  
解释: 计算 `(false OR false OR false OR true)` 的结果为 `true`。

**示例 3**  
输入: `expression = "!(&(f,t))"`  
输出: `true`  
解释:  
1. 先计算 `&(f,t)` → `(false AND true)` → `false`，表达式变为 `"!(f)"`。  
2. 再计算 `!(f)` → `NOT false` → `true`，返回 `true`。

## 约束条件

- `1 <= expression.length <= 2 * 10^4`
- `expression[i]` 只会是以下字符之一： `'('`, `')'`, `'&'`, `'|'`, `'!'`, `'t'`, `'f'`, `','`.

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把表达式里最里面的子表达式先算出来，再把结果替换回去**，一直循环，直到整个字符串只剩下 `t` 或 `f`。  

- **数据结构**：我们只需要把字符串当成一根“纸带”，在上面不停地搜索。可以把 “最里面的子表达式” 想象成 **最里层的圆圈**，把它剪下来算出结果后，用 `t` / `f` 把圆圈填回去。  
- **正确性**：题目保证表达式合法且每个子表达式的运算符（`&`、`|`、`!`）都有对应的括号和参数，最里层的子表达式一定只包含布尔常量 `t` / `f`，直接可以得到它的值。把它替换后，原来的表达式等价于新的表达式，所以不断替换下去最终会得到正确答案。  
- **复杂度分析**：  
  - 每一次搜索最里层的 `(` 到 `)` 需要遍历整条字符串，最坏情况是 `O(n)`（`n` 为字符串长度）。  
  - 替换完以后字符串长度会变短，但在最坏情况下我们会进行 **≈ n/2 次** 替换（因为每次至少消掉两个字符 `(`、`)`），于是总时间是 `O(n²)`。  
  - 只用了原字符串和几个临时变量，空间是 `O(1)`（不计输出的字符串本身）。

> **大白话**：把 `O(n²)` 想象成“把一根绳子剪成很多段，每次都要从头数到想剪的地方”。数的次数会随着段数的增加而累计，最终会很慢。

#### 代码（Python）

```python
def parse_bool_expr_bruteforce(expression: str) -> bool:
    # 把表达式复制一份，后面会不断改动
    expr = expression

    # 辅助函数：根据运算符和参数列表计算结果
    def evaluate(op: str, args: list[bool]) -> bool:
        if op == '&':          # 与
            return all(args)
        if op == '|':          # 或
            return any(args)
        if op == '!':          # 非，只有一个参数
            return not args[0]
        raise ValueError('invalid operator')

    # 循环直到只剩下一个字符（t/f）
    while len(expr) > 1:
        # 找到最里层的 '(' 的位置（从左往右，最后一次出现的 '('）
        left = expr.rfind('(')
        # 对应的右括号一定紧跟在后面
        right = expr.find(')', left)

        # 子表达式形如 "op(arg1,arg2,...)"
        sub = expr[left + 1:right]          # 取出 "op(...)" 之间的内容
        op = sub[0]                          # 第一个字符是运算符
        # 参数部分可能为空（比如 "!()" 这种非法情况，但题目保证合法），
        # 用逗号分割得到布尔值列表
        args_str = sub[2:] if len(sub) > 1 else ''
        args = [c == 't' for c in args_str.split(',') if c]  # 过滤空字符串

        # 计算子表达式的布尔值
        val = evaluate(op, args)

        # 用计算得到的结果（t/f）替换掉整个 "(op(...))"
        expr = expr[:left] + ('t' if val else 'f') + expr[right + 1:]

    # 循环结束后 expr 只剩下 't' 或 'f'
    return expr == 't'
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每一次遍历寻找最里层的括号需要 `O(n)`，最坏会进行 `≈ n/2` 次循环，故整体是平方级别。  
- **空间复杂度**：`O(1)`（不计输入字符串本身）  
  - 只用了常数个临时变量来保存子串、布尔列表等。

---

### 2. 最优解

#### 思路  

暴力解的慢点在 **“每次都要从头重新扫描整条字符串”**。如果我们能 **一次遍历就把所有子表达式的值算出来**，就能把时间降到线性 `O(n)`。这正好可以用 **栈（Stack）** 来实现。

**核心想法**：  
- 从左到右读取字符。  
- **遇到数字、`t/f`、`(`、运算符** 时直接压入栈。  
- **遇到 `)`** 时，说明一个子表达式已经完整出现了，栈顶到最近的左括号之间的内容正好是该子表达式的参数。我们弹出这些参数，弹掉左括号，再弹出运算符，立刻计算出结果（`t` 或 `f`），把结果再压回栈。  

这样每个字符只会 **进栈一次、出栈一次**，整体线性。

**为什么能一次搞定**？  
- 栈天然满足“后进先出”，最里层的子表达式一定最先遇到右括号，于是先被计算；它的结果再进入栈，成为外层表达式的一个参数。层层递进，正好对应递归的过程，但我们用显式的栈把递归的调用栈手动管理了。

**类比**：  
- 想象你在厨房烹饪多层料理（先做酱汁，再把酱汁放进主菜里），每完成一层就把它装进碗里，等到所有层都做好，最后把碗里的成品端出来。栈就是那只碗。

**细节**：

1. **压栈的字符**  
   - `'t'`、`'f'`、`'&'`、`'|'`、`'!'`、`'('`、`,`（逗号）都直接压栈。逗号只是一种分隔符，后面弹出参数时会用到它。

2. **弹出并计算**（遇到 `)`）  
   - 初始化一个空列表 `args`。  
   - **循环弹出**：如果栈顶是 `t` 或 `f`，把对应的布尔值加入 `args`，再弹掉。弹完后栈顶会是 `,`，继续弹掉 `,`，直到遇到 `'('`。  
   - 弹掉 `'('`。  
   - 再弹出运算符 `op`（必然是 `&`、`|`、`!`）。  
   - 根据 `op` 计算 `args`（`&` 用 `all`、`|` 用 `any`、`!` 用 `not`）。  
   - 把结果（`'t'` 或 `'f'`）压回栈。

3. **结束**  
   - 读取完全部字符后，栈里只会剩下一个元素 `'t'` 或 `'f'`，直接返回对应的布尔值。

#### 代码（Python）

```python
def parse_bool_expr(expression: str) -> bool:
    """
    使用栈一次遍历求值，时间 O(n)，空间 O(n)（栈的大小最多是表达式长度）。
    """
    stack: list[str] = []          # 用列表当栈，存放字符

    for ch in expression:
        if ch == ')':               # 遇到右括号，开始弹栈计算子表达式
            # 收集当前子表达式的所有参数（布尔值）
            args: list[bool] = []
            while stack and stack[-1] not in ('(', '&', '|', '!'):
                token = stack.pop()
                if token == 't':
                    args.append(True)
                elif token == 'f':
                    args.append(False)
                # token 可能是 ','，直接丢掉
            # 此时栈顶一定是 '('，弹掉它
            stack.pop()  # '('

            # 弹出运算符
            op = stack.pop()

            # 根据运算符计算结果
            if op == '&':
                val = all(args)          # 与：所有参数都为 True
            elif op == '|':
                val = any(args)          # 或：只要有一个 True
            else:  # op == '!'
                # NOT 只会有一个参数，args[0] 就是它的布尔值
                val = not args[0]

            # 把计算结果再压回栈，统一用字符 't' / 'f' 表示
            stack.append('t' if val else 'f')
        elif ch == ',':               # 逗号仅作分隔，直接跳过（或压栈均可，这里不压）
            continue
        else:
            # 其余字符直接入栈：'t','f','&','|','!','('
            stack.append(ch)

    # 循环结束后栈只剩一个元素
    return stack[0] == 't'
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个字符最多进栈一次、出栈一次，所有计算都是常数时间，整体随字符数线性增长。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(n)`  
  - 最坏情况下栈会保存整个表达式的所有字符（例如全部是左括号），所以需要线性空间。不过这已经是最优的，因为我们必须至少保存未完成的运算符和括号。

---

## 心得

- **核心技巧**：利用 **栈** 把递归的“后进先出”特性显式化，一遍遍历完成表达式求值。  
- **适用的题型**：  
  1. **算术表达式求值**（如 LeetCode 224 “Basic Calculator” 系列）  
  2. **括号匹配 / 有效字符串**（如 LeetCode 20 “Valid Parentheses”）  
  3. **中缀转后缀**、**表达式求值** 等需要处理嵌套结构的题目。  
- **一句话总结**：**“遇到右括号就把最近的左括号之间的子表达式算完并压回去”，一次遍历即可完成求值。**

---

## 反思

- **第一反应**：看到一堆括号和 `&|!`，立刻想到递归解析——写一个 `parse()` 函数，遇到 `(` 就递归，遇到 `)` 返回结果。递归思路直观，但在 Python 中递归层数可能很深（表达式长度 2·10⁴），会导致栈溢出。于是转向显式栈的迭代实现。  
- **最容易踩的坑**：  
  1. **处理 NOT 运算符的单参数**——必须保证弹出时只取一个布尔值，否则会误把逗号当成参数。  
  2. **逗号的处理**——可以选择压栈或直接跳过，关键是弹出参数时要把逗号过滤掉。  
  3. **空参数列表**（虽然题目保证合法，但代码要防止 `args` 为空导致 `all([])` / `any([])` 的意外结果）。  
- **下次第一步**：看到“嵌套的括号 + 运算符”，先在脑海里画出“栈”模型——**遇到 `)` 就把最近的 `(` 之间的东西算完**，决定使用栈或单次遍历的方式，而不是直接写递归。这样可以快速定位最优解的方向。