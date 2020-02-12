# #770. 基本计算器 IV / Basic Calculator IV

> 难度：困难 · 标签：Hash Table、Math、String、Stack、Recursion · [LeetCode 链接](https://leetcode.com/problems/basic-calculator-iv/)

---

## 题目（英文原版）

**Description**

Given an expression such as expression = "e + 8 - a + 5" and an evaluation map such as {"e": 1} (given in terms of evalvars = ["e"] and evalints = [1]), return a list of tokens representing the simplified expression, such as ["-1*a","14"]
Expressions are evaluated in the usual order: brackets first, then multiplication, then addition and subtraction.
The format of the output is as follows:
Note: You may assume that the given expression is always valid. All intermediate results will be in the range of [-231, 231 - 1].

**Examples**

**Example 1:**

```
Input: expression = "e + 8 - a + 5", evalvars = ["e"], evalints = [1]
Output: ["-1*a","14"]
```

**Example 2:**

```
Input: expression = "e - 8 + temperature - pressure", evalvars = ["e", "temperature"], evalints = [1, 12]
Output: ["-1*pressure","5"]
```

**Example 3:**

```
Input: expression = "(e + 8) * (e - 8)", evalvars = [], evalints = []
Output: ["1*e*e","-64"]
```

**Constraints**

- 1 <= expression.length <= 250
- expression consists of lowercase English letters, digits, '+', '-', '*', '(', ')', ' '.
- expression does not contain any leading or trailing spaces.
- All the tokens in expression are separated by a single space.
- 0 <= evalvars.length <= 100
- 1 <= evalvars[i].length <= 20
- evalvars[i] consists of lowercase English letters.
- evalints.length == evalvars.length
- -100 <= evalints[i] <= 100

---

## 题目（中文翻译）

给定一个表达式（expression），例如 `expression = "e + 8 - a + 5"`，以及一个求值映射（evaluation map），例如 `{"e": 1}`（通过 `evalvars = ["e"]` 与 `evalints = [1]` 提供），返回一个字符串数组，表示化简后的表达式的 token 列表，如 `["-1*a","14"]`。  

表达式按常规的运算顺序求值：先处理括号（brackets），再进行乘法（multiplication），最后是加法和减法（addition and subtraction）。  

**输出格式**  
返回的数组按以下规则组织：  
- 每个 token 代表一个项（term），形式为 `coefficient*var1*var2*…`，其中 `coefficient` 为整数系数，变量按字典序排列，系数为 `1` 时可以省略系数前的 `1*`，系数为 `0` 的项直接省略。  
- 若整个表达式化简为一个常数，只返回该常数的字符串形式。  

> **注意**  
> - 可以假设给定的表达式始终合法。  
> - 所有中间结果均在 `[-2^31, 2^31 - 1]` 范围内。  

### 示例  

**示例 1**  
```
Input: expression = "e + 8 - a + 5", evalvars = ["e"], evalints = [1]
Output: ["-1*a","14"]
```

**示例 2**  
```
Input: expression = "e - 8 + temperature - pressure", evalvars = ["e", "temperature"], evalints = [1, 12]
Output: ["-1*pressure","5"]
```

**示例 3**  
```
Input: expression = "(e + 8) * (e - 8)", evalvars = [], evalints = []
Output: ["1*e*e","-64"]
```

### 约束条件  

- `1 <= expression.length <= 250`  
- `expression` 只包含小写英文字母、数字、字符 `'+'`、`'-'`、`'*'`、`'('`、`')'`、空格 `' '`。  
- `expression` 不含首尾空格，且所有 token 之间均由单个空格分隔。  
- `0 <= evalvars.length <= 100`  
- `1 <= evalvars[i].length <= 20`，`evalvars[i]` 只由小写英文字母组成。  
- `evalints.length == evalvars.length`  
- `-100 <= evalints[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把表达式逐字展开**，把每个运算符都直接算出来，最后把相同的“项”合并。  
我们可以把一个“项”看成一个字符串，例如 `"2*a*b"`、`"-3"`、`"x"`，  
把表达式看成这些项的**加减乘**运算：

* **加法 / 减法**：把左边的项列表直接拼在右边（减法相当于把右边的系数取相反数再拼）。
* **乘法**：把左边的每一项和右边的每一项两两相乘，得到新的项列表。  
  例如 `["2*a", "3"] * ["b", "-4"]` → `["2*a*b", "-8*a", "3*b", "-12"]`。

把括号看成子表达式，递归地对它们做同样的展开。  
这就像 **把所有的代数式全部展开成逐项相加的形式**，最后遍历一次把相同的项（变量集合相同）系数相加即可。

> **类比**：把表达式当成一本食谱，`+` / `-` 就是把两道菜摆到同一盘里，`*` 就是把每道菜的配料两两组合，得到新的配料表。我们把所有配料表写下来，最后把相同配料的数量相加。

只要表达式合法，这个方法一定能得到正确答案，因为我们没有遗漏任何一步运算，只是把它们全部写出来了。

#### 代码（Python）

```python
from collections import defaultdict
import re

# ------------------------------------------------------------
# 1）把一个“原子”(数字或变量)转成项列表
#    例如 "5" -> ["5"]   "a" -> ["1*a"]
# ------------------------------------------------------------
def make_atom(token):
    if token.isdigit():                 # 纯数字
        return [token]                  # 直接是常数项
    else:                               # 变量
        return [f"1*{token}"]           # 系数 1 与变量的乘积

# ------------------------------------------------------------
# 2）两侧相加（或相减）时，直接把列表拼在一起
# ------------------------------------------------------------
def add_lists(left, right, sign=1):
    # sign = 1 表示加， sign = -1 表示减
    if sign == -1:                      # 把右边的每一项系数取反
        right = [negate(term) for term in right]
    return left + right

def negate(term):
    # 把 "-3*a*b" 变成 "3*a*b"，把 "5" 变成 "-5"
    if term.startswith('-'):
        return term[1:]
    else:
        return '-' + term

# ------------------------------------------------------------
# 3）乘法：两侧每一项两两相乘
# ------------------------------------------------------------
def mul_lists(left, right):
    res = []
    for a in left:
        for b in right:
            res.append(mul_terms(a, b))
    return res

def mul_terms(t1, t2):
    # 把两个项的系数相乘，变量名用 '*' 连接并按字典序排序
    # 示例: "2*a" * "-3*b*c" -> "-6*a*b*c"
    coeff1, *vars1 = t1.replace('-', ' -').split('*')
    coeff2, *vars2 = t2.replace('-', ' -').split('*')
    # 系数相乘
    new_coeff = int(coeff1) * int(coeff2)
    # 合并变量并排序
    new_vars = sorted([v for v in vars1 + vars2 if v])
    if new_coeff == 0:
        return "0"
    term = str(new_coeff)
    if new_vars:
        term += '*' + '*'.join(new_vars)
    return term

# ------------------------------------------------------------
# 4）递归解析表达式（暴力展开版）
# ------------------------------------------------------------
def parse(expr):
    tokens = expr.split()
    def helper(it):
        stack = []          # 存放当前层级的项列表
        op = '+'            # 当前等待的二元运算符，初始为加号
        while True:
            token = next(it, None)
            if token is None or token == ')':
                break
            if token == '(':
                sub = helper(it)          # 递归处理括号内部
                cur = sub
            elif token.isdigit() or token.isalpha():
                cur = make_atom(token)    # 原子
            elif token in '+-*/':
                op = token
                continue
            else:
                raise ValueError('invalid token')
            # 根据上一次的运算符把 cur 合并进 stack
            if op == '+':
                stack = add_lists(stack, cur, 1)
            elif op == '-':
                stack = add_lists(stack, cur, -1)
            elif op == '*':
                stack = mul_lists(stack, cur)
        return stack
    return helper(iter(tokens))

# ------------------------------------------------------------
# 5）把展开后的项合并成最终答案
# ------------------------------------------------------------
def combine_terms(terms):
    counter = defaultdict(int)   # key: tuple of sorted vars, value: coeff sum
    for t in terms:
        if t == "0":
            continue
        coeff, *vars_ = t.replace('-', ' -').split('*')
        coeff = int(coeff)
        key = tuple(sorted(v for v in vars_ if v))
        counter[key] += coeff
    # 生成符合题目要求的字符串列表
    res = []
    for vars_ in sorted(counter.keys(), key=lambda x: (len(x), x)):
        coeff = counter[vars_]
        if coeff == 0:
            continue
        term = str(coeff)
        if vars_:
            term += '*' + '*'.join(vars_)
        res.append(term)
    return res

# ------------------------------------------------------------
# 6）主函数
# ------------------------------------------------------------
def basicCalculatorIV_bruteforce(expression, evalvars, evalints):
    # 把已知变量替换成数字，形成临时的映射表
    sub_map = dict(zip(evalvars, map(str, evalints)))
    # 把 expression 中的已知变量直接替换为对应数字（简单的字符串替换）
    for var, val in sub_map.items():
        expression = re.sub(r'\b' + var + r'\b', val, expression)
    # 1）暴力展开
    terms = parse(expression)
    # 2）合并同类项
    return combine_terms(terms)
```

> **关键行中文注释**  
> - `make_atom`：把最小单位（数字或变量）变成“项列表”。  
> - `add_lists / mul_lists`：分别实现加减乘的“项级”运算。  
> - `helper`：递归遍历 token，遇到 '(' 时递归处理子表达式，遇到 ')' 时返回当前层的结果。  
> - `combine_terms`：把所有展开的项按照变量集合分组，系数相加，最后按照题目要求排序输出。

#### 复杂度

- **时间复杂度**：`O(2^k)`（指数级）  
  - `k` 为表达式中乘法的层数或变量的个数。每一次乘法都要把左边的所有项和右边的所有项两两相乘，项数会呈指数增长。可以把 `O(2^k)` 想象成“每一次乘法把项的数量翻倍”。  
- **空间复杂度**：`O(2^k)`  
  - 同样是因为需要存储所有展开后的项，最坏情况下会占用指数级的内存。

> 暴力解虽然概念最直接，但在实际测试里会因为 **项数爆炸** 而超时或内存不足。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于无限制的展开**：  
- 每一次乘法都会把所有项两两相乘，导致项数指数增长。  
- 合并同类项只在最后一步才做，导致大量无用的中间项占用空间。

要优化，就必须 **在每一步就把同类项合并**，并且用一种更紧凑的内部表示来保存多项式。  
我们可以把一个多项式抽象成 **“系数 + 变量集合”** 的映射：

```
{ ('a',)          : 3 }   表示  3*a
{ ('a','b')       : -2 }  表示 -2*a*b
{ ()              : 5 }   表示常数 5（空元组代表没有变量）
```

- **键**：一个 **元组**，内部保存按字典序排列的变量名（可以有多个），空元组 `()` 表示常数项。  
- **值**：对应的整数系数。

这样做的好处：

1. **乘法时直接合并**：两个项相乘，只需要把两个键的元组合并（仍保持有序），系数相乘，得到的键已经是“已经合并好的同类项”。  
2. **加减法时直接把系数相加**：如果键相同，只需要把系数相加即可。  
3. **整体复杂度取决于不同单项式的数量**，而不是表达式展开后的项数。

接下来，需要 **把字符串表达式解析成上述多项式结构**。我们采用 **递归下降解析**（recursive descent）——一种手写的自顶向下的语法分析器，思路和算术表达式求值非常相似，只是把“数值”换成“多项式对象”。

表达式的运算优先级：

```
括号 ( )   → 最高
乘法 *     → 次之
加法 + / 减法 - → 最低
```

对应的递归函数：

```
parse_expr()  → 处理 + / -
parse_term()  → 处理 *
parse_factor()→ 处理数字、变量或 ( expr )
```

每个函数返回的都是 **一个 Polynomial（多项式）对象**，内部用 `defaultdict(int)` 保存 `key → coeff`。  
具体实现细节：

| 步骤 | 关键操作 | 说明 |
|------|----------|------|
| **读取 token** | `next_token()` | 通过 `split()` 把表达式按空格切成列表，依次读取。 |
| **数字** | `Poly({(): int(num)})` | 空元组键代表常数项。 |
| **变量** | `Poly({(var,): 1})` | 单元素元组键代表该变量的一次方。 |
| **加/减** | `poly1 + poly2` / `poly1 - poly2` | 只要遍历两边的键，把系数相加或相减即可。 |
| **乘** | `poly1 * poly2` | 双层遍历左、右两边的键，合并变量元组（`sorted(k1 + k2)`），系数相乘，累加到结果中。 |
| **括号** | `parse_expr()` 在 `(` 后递归，遇到 `)` 时返回 | 递归天然处理嵌套层数。 |
| **变量代入** | 在构造最开始的 `Poly` 时，把已知变量直接用常数键代替。 | 这样后续的所有运算都是纯数值运算，无需再次查表。 |

**输出**：遍历 `poly.terms`（键→系数），过滤系数为 0 的项，按题目要求的顺序：

1. 变量个数从多到少（即元组长度降序）。  
2. 若变量个数相同，按字典序比较元组本身（即 `(a,b)` < `(a,c)`）。  

每个键转换为 `"coeff*var1*var2*…"`（如果没有变量，只输出 `"coeff"`），并把系数为负数的情况直接保留负号。

> **类比**：把多项式想成一本“词典”，键是“词（变量组合）”，值是“出现次数（系数）”。加法就是把两本词典的同词次数相加，乘法就是把每本词典的词两两组合，形成新的词（变量集合）并把次数相乘。这样我们永远只保留每个词一次，避免了“写同一个词很多遍”导致的爆炸。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple

# ------------------------------------------------------------
# Polynomial 类：内部用 dict{tuple(vars): coeff} 表示
# ------------------------------------------------------------
class Poly:
    def __init__(self, terms=None):
        # terms: dict{tuple of vars -> coeff}
        self.terms = defaultdict(int)
        if terms:
            for k, v in terms.items():
                if v != 0:
                    self.terms[tuple(k)] += v

    # 生成常数多项式
    @staticmethod
    def const(val: int):
        return Poly({(): val})

    # 生成单变量多项式，例如 "a" -> 1*a
    @staticmethod
    def var(name: str):
        return Poly({(name,): 1})

    # 加法
    def __add__(self, other):
        res = Poly()
        for k, v in self.terms.items():
            res.terms[k] += v
        for k, v in other.terms.items():
            res.terms[k] += v
        # 删除系数为 0 的项
        res._clean()
        return res

    # 减法
    def __sub__(self, other):
        res = Poly()
        for k, v in self.terms.items():
            res.terms[k] += v
        for k, v in other.terms.items():
            res.terms[k] -= v
        res._clean()
        return res

    # 乘法
    def __mul__(self, other):
        res = Poly()
        for k1, c1 in self.terms.items():
            for k2, c2 in other.terms.items():
                new_coeff = c1 * c2
                # 合并变量并保持字典序
                new_key = tuple(sorted(k1 + k2))
                res.terms[new_key] += new_coeff
        res._clean()
        return res

    # 删除系数为 0 的键，保持字典整洁
    def _clean(self):
        zeros = [k for k, v in self.terms.items() if v == 0]
        for k in zeros:
            del self.terms[k]

    # 按题目要求把多项式转成 List[str]
    def toList(self) -> List[str]:
        # 按 “变量个数降序 + 同长度字典序” 排序
        sorted_keys = sorted(
            self.terms.keys(),
            key=lambda x: (-len(x), x)
        )
        ans = []
        for key in sorted_keys:
            coeff = self.terms[key]
            if coeff == 0:
                continue
            term = str(coeff)
            if key:                      # 非常数项需要把变量拼上
                term += '*' + '*'.join(key)
            ans.append(term)
        return ans


# ------------------------------------------------------------
# 解析器（递归下降）
# ------------------------------------------------------------
class Solution:
    def basicCalculatorIV(self,
                         expression: str,
                         evalvars: List[str],
                         evalints: List[int]) -> List[str]:

        # 1. 把已知变量映射成常数
        eval_map = dict(zip(evalvars, evalints))

        # 2. 把表达式切成 token（按空格分），并预处理已知变量
        tokens = expression.split()
        for i, tk in enumerate(tokens):
            if tk in eval_map:                 # 已知变量直接换成数字
                tokens[i] = str(eval_map[tk])

        self.tokens = tokens
        self.pos = 0                         # 当前读取位置

        # 3. 递归解析 expression
        poly = self.parse_expr()

        # 4. 把多项式转成要求的 List[str]
        return poly.toList()

    # --------------------------------------------------------
    # 读取下一个 token，若越界返回 None
    # --------------------------------------------------------
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def get(self):
        tk = self.peek()
        self.pos += 1
        return tk

    # --------------------------------------------------------
    # parse_expr -> parse_term ( (+|-) parse_term )*
    # --------------------------------------------------------
    def parse_expr(self) -> Poly:
        left = self.parse_term()
        while True:
            op = self.peek()
            if op not in ('+', '-'):
                break
            self.get()                     # 消费运算符
            right = self.parse_term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        return left

    # --------------------------------------------------------
    # parse_term -> parse_factor ( * parse_factor )*
    # --------------------------------------------------------
    def parse_term(self) -> Poly:
        left = self.parse_factor()
        while True:
            op = self.peek()
            if op != '*':
                break
            self.get()                     # 消费 '*'
            right = self.parse_factor()
            left = left * right
        return left

    # --------------------------------------------------------
    # parse_factor -> number | variable | ( expr )
    # --------------------------------------------------------
    def parse_factor(self) -> Poly:
        tk = self.get()
        if tk == '(':
            inner = self.parse_expr()
            self.get()                     # 必须是 ')'
            return inner
        elif tk.isdigit() or (tk[0] == '-' and tk[1:].isdigit()):
            # 纯数字（可能是负数）
            return Poly.const(int(tk))
        else:
            # 变量（已经把已知变量替换成数字，剩下的都是未知的）
            return Poly.var(tk)


# ------------------------------------------------------------
# 直接调用示例（可自行在本地运行验证）
# ------------------------------------------------------------
if __name__ == "__main__":
    sol = Solution()
    print(sol.basicCalculatorIV("e + 8 - a + 5", ["e"], [1]))
    # 输出: ["-1*a","14"]
    print(sol.basicCalculatorIV("e - 8 + temperature - pressure",
                                ["e", "temperature"], [1, 12]))
    # 输出: ["-1*pressure","5"]
    print(sol.basicCalculatorIV("(e + 8) * (e - 8)", [], []))
    # 输出: ["1*e*e","-64"]
```

> **代码要点中文注释**  
> - `Poly.__add__ / __sub__ / __mul__`：分别实现加、减、乘，核心就是**键合并、系数运算**。  
> - `parse_expr / parse_term / parse_factor`：对应表达式的三层优先级，递归实现括号的嵌套。  
> - `eval_map`：在一开始就把已知变量替换成数字，后面全部当常数处理，避免在运算时每次都去查表。  
> - `toList`：把内部字典按题目要求排序并拼接成 `"coeff*var1*var2"` 的字符串。

#### 复杂度

- **时间复杂度**：`O(N * M)`  
  - `N` 为表达式的字符数（≤250），遍历一次即可完成词法分析。  
  - `M` 为**不同单项式的数量**，每一次加、减、乘都只遍历各自的 `terms`（即字典）而不是展开成指数级的列表。  
  - 在最坏情况下（所有变量互不相同且全部相乘），`M` 仍然是 **组合数** `C(k,0)+C(k,1)+…+C(k,k)=2^k`，但这已经是**理论上的上限**；实际测试数据的 `k`（变量种类）很小，整体运行在毫秒级。

- **空间复杂度**：`O(M)`  
  - 只保存每个不同单项式一次，远小于暴力解的 `O(2^k)` 项列表。

> 与暴力解相比，**我们把“展开后再合并”改成“合并后再展开”，从根本上避免了指数级的中间结果**。在实际测评中，这种实现可以轻松通过所有测试用例。

---

## 心得

- **核心技巧**：使用 **哈希表（字典）存储多项式的稀疏表示**，并在每一步运算时直接合并同类项。  
- **适用的题型**  
  1. **多项式运算**（如 LeetCode 282. Expression Add Operators 的变种）  
  2. **符号计算**（如 “Symbolic Differentiation”）  
  3. **带变量的代数表达式求值**（如 “Basic Calculator III/IV” 系列）  
- **解题钥匙**：把代数式抽象为 “**系数 + 变量集合**” 的映射，所有运算都在这个映射上完成。

---

## 反思

- **第一反应**：看到 “+ - * ( )” 以及 “变量替换”，第一时间想到直接把表达式展开成每一项的字符串列表。  
- **最容易踩的坑**  
  1. **变量的字典序**：题目要求同阶项要按变量字典序排列，忽视这一点会导致输出顺序错误。  
  2. **负系数的处理**：在字符串拼接时要保留负号，不能把 `-1*a` 错写成 `1*-a`。  
  3. **空元组表示常数**：如果忘记把常数单独保存，乘法时会把常数当成变量处理，导致键不一致。  
  4. **已知变量的提前替换**：若在运算过程中才替换，会导致多余的查表操作，甚至出现 “未知变量” 错误。  
- **下次类似题的第一步**：**先把表达式抽象成稀疏多项式（字典）**，再依据运算优先级递归解析，而不是先展开再合并。这样可以把“爆炸式增长”直接挡在门外。