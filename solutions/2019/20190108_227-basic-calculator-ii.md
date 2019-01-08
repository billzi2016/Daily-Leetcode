# #227. 基本计算器 II / Basic Calculator II

> 难度：中等 · 标签：Math、String、Stack · [LeetCode 链接](https://leetcode.com/problems/basic-calculator-ii/)

---

## 题目（英文原版）

**Description**

Given a string s which represents an expression, evaluate this expression and return its value.
The integer division should truncate toward zero.
You may assume that the given expression is always valid. All intermediate results will be in the range of [-231, 231 - 1].
Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

**Examples**

**Example 1:**

```
Input: s = "3+2*2"
Output: 7
```

**Example 2:**

```
Input: s = " 3/2 "
Output: 1
```

**Example 3:**

```
Input: s = " 3+5 / 2 "
Output: 5
```

**Constraints**

- 1 <= s.length <= 3 * 105
- s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
- s represents a valid expression.
- All the integers in the expression are non-negative integers in the range [0, 231 - 1].
- The answer is guaranteed to fit in a 32-bit integer.

---

## 题目（中文翻译）

给定一个字符串 `s`，它表示一个算术表达式（expression），请计算并返回该表达式的值。整数除法应向零截断（truncate toward zero）。  

你可以假设给定的表达式始终合法。所有中间结果都在 `[-2^31, 2^31 - 1]` 范围内。  

**注意**：禁止使用任何内置函数直接求解字符串形式的算术表达式，例如 `eval()`。

**示例 1**  
输入: `s = "3+2*2"`  
输出: `7`

**示例 2**  
输入: `s = " 3/2 "`  
输出: `1`

**示例 3**  
输入: `s = " 3+5 / 2 "`  
输出: `5`

**约束条件**

- `1 <= s.length <= 3 * 10^5`
- `s` 只包含整数和运算符 `'+'`, `'-'`, `'*'`, `'/'`，并可能由若干空格分隔。
- `s` 表示一个合法的表达式。
- 表达式中的所有整数都是非负整数，范围在 `[0, 2^31 - 1]`。
- 计算结果保证能够放入 32 位整数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把表达式先 **拆成数字和运算符** 两个序列，然后按照算术优先级一次算完。  
可以把它想象成 **“先找乘除，再找加减”** 的两遍扫街：

1. **第一次遍历**：把所有空格去掉，得到形如 `3+2*2` 的紧凑字符串。  
2. **第二次遍历**：从左到右扫描，遇到 `*` 或 `/` 就立刻算出结果，**把左边的数字和右边的数字合并成一个新数字**，把旧的两个数字和运算符删掉。  
   这一步相当于“把乘除这条街的店铺关掉，剩下的只剩下加减”。  
3. **第三次遍历**：只剩下 `+`、`-`，从左到右依次累加即可。

> 这里的 **“把左边的数字和右边的数字合并成一个新数字”** 就像把两本书粘在一起，原来的两本书不见了，只剩下一本更厚的书。

这种方法一定能得到正确答案，因为我们严格按照 **先乘除后加减** 的规则一步步执行了所有运算。

不过，每次遇到 `*` 或 `/` 都要 **把列表中对应的元素删除并插入新元素**，这在 Python 的 `list` 中是 **O(n)** 的操作。最坏情况下会进行 `n/2` 次这样的删除/插入，整体时间复杂度会退化到 **O(n²)**，而且需要额外的列表空间来存放所有数字和运算符。

#### 代码（Python）

```python
def calculate_bruteforce(s: str) -> int:
    # 1️⃣ 去掉所有空格，得到紧凑的表达式
    expr = s.replace(' ', '')
    # 2️⃣ 把表达式拆成数字和运算符两列
    nums = []      # 存放整数
    ops = []       # 存放 '+', '-', '*', '/' 四种运算符
    i = 0
    while i < len(expr):
        if expr[i].isdigit():                     # 读取一个完整的整数
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            nums.append(int(expr[i:j]))
            i = j
        else:                                     # 是运算符
            ops.append(expr[i])
            i += 1

    # 3️⃣ 第一次遍历：处理所有乘除
    idx = 0
    while idx < len(ops):
        if ops[idx] in ('*', '/'):
            left = nums[idx]
            right = nums[idx + 1]
            # 根据运算符计算结果（整数除法向 0 截断）
            if ops[idx] == '*':
                cur = left * right
            else:
                # Python 除法向负无穷取整，需要手动向 0 截断
                cur = int(left / right)
            # 用新结果替换左边的数字，删除右边的数字和运算符
            nums[idx] = cur
            del nums[idx + 1]      # 删除右侧数字 → O(n)
            del ops[idx]           # 删除运算符   → O(n)
            # 不移动 idx，继续检查当前位置是否还有乘除
        else:
            idx += 1               # 加减先跳过，留到后面处理

    # 4️⃣ 第二次遍历：只剩加减，直接累加
    result = nums[0]
    for i, op in enumerate(ops):
        if op == '+':
            result += nums[i + 1]
        else:  # '-'
            result -= nums[i + 1]
    return result
```

> 关键行已加中文注释，代码可以直接运行。

#### 复杂度  

- **时间复杂度：O(n²)**  
  - `n` 为表达式长度。每次删除/插入列表元素都要把后面的元素整体左移，最坏会出现 `≈ n/2` 次 O(n) 操作，故整体是二次方级别。  
  - “O(n²)” 可以想象成 **“把一本 100 页的书每页都往后搬一次”**，工作量随页数的平方增长。

- **空间复杂度：O(n)**  
  - 需要额外的两个列表分别存放所有数字和运算符，大小随输入长度线性增长。  
  - “O(n)” 就像 **“搬家时需要和原来一样多的箱子”**。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于频繁的列表删除/插入**。  
其实我们并不需要把整个表达式保存下来，只要在一次遍历中 **实时计算** 就可以。

观察运算符的优先级：

- `*`、`/` 的优先级高，需要立刻和左侧的数字合并。  
- `+`、`-` 的优先级低，可以等到后面统一累加。

利用 **“上一次的乘除结果”** 这个概念：

1. 用一个变量 `prev` 记录最近一次 **已经确定的乘除结果**（或者当前的单个数字）。  
2. 用一个变量 `result` 累计所有已经确定的 **加减** 结果。  
3. 遍历字符串时，遇到数字就把它转成 `cur`。  
4. 遇到运算符（或遍历结束）时，根据前一个运算符 `sign`（初始为 `'+'`）决定如何处理 `cur`：  

   - `sign == '+'` → 把前一个 `prev` 加到 `result`（因为 `prev` 已经不可能再参与乘除），再把 `cur` 设为新的 `prev`。  
   - `sign == '-'` → 同理，把 `prev` 加到 `result`，把 `-cur` 设为新的 `prev`。  
   - `sign == '*'` → `prev = prev * cur`（直接把乘法合并到 `prev`）。  
   - `sign == '/'` → `prev = int(prev / cur)`（除法向 0 截断，同样合并到 `prev`）。

5. 最后遍历结束后，把最后的 `prev` 加到 `result`，得到答案。

> 这里的 **“把乘除合并到 prev”** 可以类比为 **“把两个相邻的盒子粘在一起，等到必须搬运时一次性搬走”**。这样我们只需要 **O(1)** 的额外空间。

这就是 **一遍扫描 + 常数空间** 的解法，时间是 **O(n)**，空间是 **O(1)**（不计输入本身）。

#### 代码（Python）

```python
def calculate(s: str) -> int:
    """
    一遍扫描求值，时间 O(n)，空间 O(1)。
    """
    n = len(s)
    cur = 0            # 当前正在读取的数字
    prev = 0           # 最近一次确定的乘除结果（或单个数字）
    result = 0         # 累计的加减结果
    sign = '+'         # 前一个运算符，默认视作在最左侧有一个 '+'

    i = 0
    while i < n:
        ch = s[i]
        if ch.isdigit():
            # 累积多位数，例如 "123"
            cur = cur * 10 + int(ch)

        # 如果当前字符是运算符或已经是最后一个字符，需要“交代”前面的数字
        if (not ch.isdigit() and ch != ' ') or i == n - 1:
            if sign == '+':
                result += prev      # 把上一次的 prev 加到累计结果
                prev = cur          # 当前数字成为新的 prev
            elif sign == '-':
                result += prev
                prev = -cur
            elif sign == '*':
                prev = prev * cur
            else:  # sign == '/'
                # Python 除法向负无穷取整，题目要求向 0 截断，需要手动转换
                prev = int(prev / cur)

            sign = ch               # 更新运算符，供下一轮使用
            cur = 0                 # 重置当前数字，准备读取下一个

        i += 1

    result += prev                 # 把最后的 prev 加进去
    return result
```

> 代码中每一关键步骤都有中文注释，直接拷贝即可运行。

#### 复杂度  

- **时间复杂度：O(n)**  
  - 只遍历一次字符串，每个字符做 O(1) 的工作。  
  - “O(n)” 类似 **“一次搬走 n 本书”**，工作量随书本数线性增长。

- **空间复杂度：O(1)**  
  - 只使用了固定数量的整数变量（`cur、prev、result、sign`），不随输入规模增长。  
  - “O(1)” 可以想象成 **“只需要一个小盒子来装工具，箱子数量不变”**。

---

## 心得

- **核心技巧**：一次遍历结合“上一次乘除结果” (`prev`) 与累计加减结果 (`result`) 的思路。  
- **适用场景**：  
  1. 只包含 `+ - * /` 且没有括号的算术表达式（如本题）。  
  2. “带优先级的线性表达式”，例如 LeetCode *Basic Calculator I*（只含 `+ -`，可以直接累加）。  
  3. “需要实时合并同优先级运算的流式计算”，如在线编辑器即时求值。  
- **一句话总结**：**“把乘除先合并到一个临时变量，等到加减时一次性收敛”** 就是这道题的解题钥匙。

---

## 反思

- **第一反应**：把字符串直接 `eval()`，或者把所有数字和运算符存进列表后再分两遍处理。  
- **最容易踩的坑**：  
  - 除法的截断规则：Python 的 `//` 会向负无穷取整，需要手动 `int(a / b)` 才能实现“向 0 截断”。  
  - 连续空格或字符串以数字结尾时，忘记在遍历结束后处理最后的 `prev`。  
  - 多位数的读取：`cur = cur * 10 + digit` 必须在遍历数字时持续累积。  
- **下次类似题**：第一步先 **“把所有乘除立即算完并合并到前一个数”**，再统一处理加减——这一步几乎是所有不带括号、只有四则运算的题目的通用模板。