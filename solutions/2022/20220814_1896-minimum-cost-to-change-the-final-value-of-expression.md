# #1896. **改变表达式最终值的最小代价** / Minimum Cost to Change the Final Value of Expression

> 难度：困难 · 标签：Math、String、Dynamic Programming、Stack · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-change-the-final-value-of-expression/)

---

## 题目（英文原版）

**Description**

You are given a valid boolean expression as a string expression consisting of the characters '1','0','&' (bitwise AND operator),'|' (bitwise OR operator),'(', and ')'.
Return the minimum cost to change the final value of the expression.
The cost of changing the final value of an expression is the number of operations performed on the expression. The types of operations are described as follows:
Note: '&' does not take precedence over '|' in the order of calculation. Evaluate parentheses first, then in left-to-right order.

**Examples**

**Example 1:**

```
Input: expression = "1&(0|1)"
Output: 1
Explanation: We can turn "1&(0|1)" into "1&(0&1)" by changing the '|' to a '&' using 1 operation.
The new expression evaluates to 0.
```

**Example 2:**

```
Input: expression = "(0&0)&(0&0&0)"
Output: 3
Explanation: We can turn "(0&0)&(0&0&0)" into "(0|1)|(0&0&0)" using 3 operations.
The new expression evaluates to 1.
```

**Example 3:**

```
Input: expression = "(0|(1|0&1))"
Output: 1
Explanation: We can turn "(0|(1|0&1))" into "(0|(0|0&1))" using 1 operation.
The new expression evaluates to 0.
```

**Constraints**

- 1 <= expression.length <= 105
- expression only contains '1','0','&','|','(', and ')'
- All parentheses are properly matched.
- There will be no empty parentheses (i.e: "()" is not a substring of expression).

---

## 题目（中文翻译）

给定一个仅由字符 `'1'`、`'0'`、`'&'`（按位与运算符）、`'|'`（按位或运算符）、`'('` 和 `')'` 组成的合法布尔表达式 `expression`。返回使该表达式的最终求值结果发生改变所需的最小代价。  

改变表达式最终值的代价定义为对表达式进行的操作次数。可进行的操作类型如下：

- 将任意 `'&'` 替换为 `'|'`，或将任意 `'|'` 替换为 `'&'`（每次替换计 1 次操作）。
- 其他字符（`'0'`、`'1'`、括号）不可直接修改。

**注意**：在计算顺序上，`'&'` 并不优先于 `'|'`。先计算括号内的子表达式（subexpression），随后按从左到右的顺序依次计算剩余的运算。

---

### 示例

**示例 1**  
**输入**: `expression = "1&(0|1)"`  
**输出**: `1`  
**解释**: 将 `'|'` 改为 `'&'`，得到 `"1&(0&1)"`，只需 1 次操作。新表达式的计算结果为 `0`。

**示例 2**  
**输入**: `expression = "(0&0)&(0&0&0)"`  
**输出**: `3`  
**解释**: 将表达式改为 `"(0|1)|(0&0&0)"`，共需要 3 次操作。新表达式的计算结果为 `1`。

**示例 3**  
**输入**: `expression = "(0|(1|0&1))"`  
**输出**: `1`  
**解释**: 将内部的 `'|'` 改为 `'&'`，得到 `"(0|(0|0&1))"`，只需 1 次操作。新表达式的计算结果为 `0`。

---

### 约束条件

- `1 <= expression.length <= 10^5`
- `expression` 只包含字符 `'1'`、`'0'`、`'&'`、`'|'`、`'('`、`')'`
- 所有括号均匹配完整
- 不会出现空括号（即子串 `"()"` 不会出现在 `expression` 中）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每一个字符都尝试改一次**，看改完以后表达式的值会不会和原来相反。  
具体做法可以是：

1. 先遍历一遍字符串，记下所有可以改的字符位置（`0、1、&、|` 都可以改成另外一种）。
2. 对每一种“改法”——即把若干个字符翻转——重新计算表达式的值。  
   - 计算表达式时只需要按照题目给出的规则：先算括号，再从左到右顺序计算，`&` 与 `|` 没有优先级。  
3. 找到**最少改动次数**使得最终值和原表达式相反的那种情况。

> **类比**：把这道题想成在一本字典里找单词。暴力解相当于把字典里每一个单词都翻遍一次，看哪一个恰好是目标单词的“反义词”。显然，这种“遍历全书”的做法在字典很大的时候会非常慢。

**为什么暴力一定能得到答案？**  
因为我们把**所有可能的改动方式**都枚举了一遍，必然能覆盖到最优的那一种。只是不现实——如果表达式长度是 `n`，每个字符都有两种状态（改或不改），总共要检查 `2^n` 种组合，随着 `n` 的增长，计算量会指数级爆炸。

#### 代码（Python）

```python
import itertools

def eval_expr(expr: str) -> int:
    """按照题目规定的顺序（先括号，再左到右）计算布尔表达式的值。"""
    # 这里用 Python 的 eval 直接算，实际提交时要自行实现
    # 为了演示暴力思路，这里不展开实现细节
    return eval(expr.replace('&', ' and ').replace('|', ' or '))

def brute_min_cost(expr: str) -> int:
    n = len(expr)
    # 记录可以改的下标（不是 '(' 或 ')'）
    idx = [i for i, ch in enumerate(expr) if ch in '01&|']
    # 逐渐增加改动次数，从 0 到 len(idx) 找第一个可行解
    for k in range(len(idx) + 1):
        # 组合出所有恰好改 k 个字符的方案
        for combo in itertools.combinations(idx, k):
            lst = list(expr)
            for i in combo:                     # 把选中的字符翻转
                lst[i] = {'0': '1', '1': '0', '&': '|', '|': '&'}[lst[i]]
            new_expr = ''.join(lst)
            if eval_expr(new_expr) != eval_expr(expr):
                return k                         # 找到最小改动次数
    return -1  # 理论上不会到这里
```

> **提示**：上面代码只用于说明思路，实际运行会在 `n≈20` 左右就超时。

#### 复杂度  

- **时间复杂度**：`O(2^n)`  
  - `n` 为表达式长度。我们要检查每一种可能的改动组合，组合数是指数级的。  
  - 用大白话说，就是“每增加一个字符，就要把所有已经可能的改法翻一遍”。  
- **空间复杂度**：`O(n)`  
  - 主要是保存表达式副本和递归栈（`itertools` 生成组合时会占用一定空间）。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于每次都要重新计算整个表达式的值，而且要枚举所有改动方式。  
要想更快，需要**把表达式分解成子问题**，让每个子表达式只保存**“把它变成 0 的最小代价”**和**“把它变成 1 的最小代价”**这两个数。这样：

- 只需要一次遍历（线性）就能把所有子表达式的这两种代价算出来。  
- 最终答案就是根表达式（整个字符串）把值翻转的代价。

这正是**动态规划**的思想：把大问题拆成小问题，子问题只需要记住有限的状态。  

**关键数据结构：栈**  
因为表达式里有括号，需要先算完括号里的内容再往外合并。栈可以天然地帮助我们**“遇到 '(' 就进栈，遇到 ')' 就弹出并合并”**。  

下面把整个思路拆成几步解释（每一步都会配上生活化的类比）：

1. **把每个字符映射成“代价对”**  
   - 对于常量 `'0'`：保持不变代价是 `0`，想让它变成 `'1'` 需要改一次，代价是 `1`。  
   - 对于常量 `'1'`：同理，`cost(0)=1`，`cost(1)=0`。  
   - 这一步好比把每本书的**封面颜色**记下来：有的本来是红色（0），如果想要蓝色（1）就得贴上一张贴纸（代价 1）。

2. **定义合并规则**  
   假设左子表达式的代价对是 `(L0, L1)`，右子表达式是 `(R0, R1)`，当前运算符是 `op`（`&` 或 `|`）。  
   - **不改运算符**的情况下，得到 **0** 或 **1** 的最小代价可以用下面的公式算出来（下面会逐行解释）。  
   - **改运算符**（`&`↔`|`）只需要额外付出 `1` 的代价，因为只改一个字符。我们把“改运算符后再合并”的结果也算进去，最后取最小值。  

   具体公式（下面的代码里会写得更直观）：

   - `&` 想得到 `0`：只要左边是 `0` **或** 右边是 `0` 即可。  
     ```text
     cost0 = min( L0 + min(R0, R1),   # 左边已经是0，右边随便取最小代价
                 R0 + min(L0, L1) )   # 右边已经是0，左边随便取最小代价
     ```
   - `&` 想得到 `1`：必须左、右都为 `1`。  
     ```text
     cost1 = L1 + R1
     ```
   - `|` 想得到 `1`：左边是 `1` **或** 右边是 `1`。  
     ```text
     cost1 = min( L1 + min(R0, R1),   # 左边已经是1，右边随便取
                 R1 + min(L0, L1) )
     ```
   - `|` 想得到 `0`：只能左、右都为 `0`。  
     ```text
     cost0 = L0 + R0
     ```

3. **用栈一次遍历整个字符串**  

   - **两个栈**：  
     - `vals` 存放每个子表达式的代价对 `(cost0, cost1)`。  
     - `ops` 存放运算符和左括号 `'('`。  
   - **遍历规则**（左到右）  
     1. 遇到 `'0'`、`'1'` → 把对应的代价对压入 `vals`。  
     2. 遇到 `'('` → 把它压入 `ops`（起到分隔作用）。  
     3. 遇到运算符 `&`、`|` →  
        - 因为题目说 **没有运算符优先级**，左到右顺序执行，所以在压入新运算符前，需要先把 `ops` 栈顶的旧运算符算完（只要栈顶不是 `'('`）。  
        - 这样保证了**先算左边的子表达式**，再把新运算符放进去。  
     4. 遇到 `')'` →  
        - 一直弹出并合并 `ops` 栈顶的运算符，直到弹到对应的 `'('` 为止。  
        - 合并时使用上面第 2 步的**合并规则**，并把得到的新代价对压回 `vals`。  

   - 遍历结束后，`vals` 栈里只会剩下一个代价对——整棵表达式的 `(cost0, cost1)`。  
   - 最后看原表达式的值是 `0` 还是 `1`，返回把它变成相反值的代价即可。  

> **类比**：想象你在拼装乐高城堡。每块乐高（子表达式）都有两种颜色（0 / 1），并且已经记录了把它变成每种颜色的最小“贴纸”数量。运算符 `&`、`|` 就像两块乐高之间的连接器：要让整体颜色为某种，需要根据连接器的规则决定哪块需要贴多少贴纸。栈的作用相当于“先把内部房间装好，再装外层墙”。  

#### 代码（Python）

```python
from typing import List, Tuple

INF = 10 ** 9  # 足够大的数，代表“不可能”

def combine(a: Tuple[int, int], b: Tuple[int, int], op: str) -> Tuple[int, int]:
    """
    把左子表达式 a 与右子表达式 b 用运算符 op 合并。
    a / b 都是 (cost0, cost1)。
    返回合并后的 (cost0, cost1)，已经把“改运算符”这种可能性算进去。
    """
    a0, a1 = a
    b0, b1 = b

    # ---------- 不改运算符 ----------
    if op == '&':
        # 目标 0：左为0或右为0
        keep0 = min(a0 + min(b0, b1), b0 + min(a0, a1))
        # 目标 1：必须两边都是1
        keep1 = a1 + b1
    else:          # op == '|'
        # 目标 1：左为1或右为1
        keep1 = min(a1 + min(b0, b1), b1 + min(a0, a1))
        # 目标 0：必须两边都是0
        keep0 = a0 + b0

    # ---------- 改运算符 ----------
    # 把 & 换成 | 或者把 | 换成 &
    flipped_op = '&' if op == '|' else '|'
    if flipped_op == '&':
        flip0 = min(a0 + min(b0, b1), b0 + min(a0, a1))
        flip1 = a1 + b1
    else:  # flipped_op == '|'
        flip1 = min(a1 + min(b0, b1), b1 + min(a0, a1))
        flip0 = a0 + b0

    # 改运算符要额外付出 1 次操作
    flip0 += 1
    flip1 += 1

    # 取最小代价
    return (min(keep0, flip0), min(keep1, flip1))


def minCostToChangeExpression(expression: str) -> int:
    """
    主函数：返回把 expression 最终值翻转所需的最小操作次数。
    思路：用两个栈模拟表达式求值，同时记录每个子表达式
          变成 0 / 1 的最小代价。
    """
    vals: List[Tuple[int, int]] = []   # 代价对栈
    ops: List[str] = []                # 运算符栈，包含 '('

    # 把字符依次处理
    i = 0
    while i < len(expression):
        ch = expression[i]

        if ch == '0':
            vals.append((0, 1))          # 0 本身代价0，改成1代价1
        elif ch == '1':
            vals.append((1, 0))          # 1 本身代价0，改成0代价1
        elif ch in '&|':
            # 由于没有运算符优先级，左到右顺序执行。
            # 所以在压入新运算符前，先把栈顶已有的运算符算完（只要不是 '('）。
            while ops and ops[-1] != '(':
                right = vals.pop()
                left = vals.pop()
                op = ops.pop()
                vals.append(combine(left, right, op))
            ops.append(ch)
        elif ch == '(':
            ops.append(ch)
        elif ch == ')':
            # 把括号内部的所有运算符全部算完
            while ops and ops[-1] != '(':
                right = vals.pop()
                left = vals.pop()
                op = ops.pop()
                vals.append(combine(left, right, op))
            ops.pop()  # 弹掉 '('
        # 其它字符（如空格）题目里不存在，这里直接跳过
        i += 1

    # 处理剩下的运算符（如果表达式最外层没有括号）
    while ops:
        right = vals.pop()
        left = vals.pop()
        op = ops.pop()
        vals.append(combine(left, right, op))

    # 此时 vals 里只剩下根表达式的代价对
    cost0, cost1 = vals[0]

    # 先求出原表达式的真实值（只要一次遍历就能得到，这里复用上面的过程）
    # 为了代码简洁，这里直接使用 Python eval（实际比赛中要自行实现）
    original = eval(expression.replace('&', ' and ').replace('|', ' or '))
    # 如果原来是 0，答案就是把它变成 1 的最小代价，以此类推
    return cost1 if original == 0 else cost0


# -------------------------------------------------
# 示例测试（可直接运行）
if __name__ == "__main__":
    tests = [
        ("1&(0|1)", 1),
        ("(0&0)&(0&0&0)", 3),
        ("(0|(1|0&1))", 1),
    ]
    for expr, ans in tests:
        print(expr, "=>", minCostToChangeExpression(expr), "(expect", ans, ")")
```

> **代码要点注释**  
- `combine` 函数是**核心**：它把两个子表达式的代价合并，并且把“改运算符”这种额外的选择也算进去。  
- 使用 `INF`（这里用一个很大的整数）可以避免在 `min` 时出现负数或未定义的情况。  
- 整个算法只遍历一次字符串，栈的每个元素最多进出一次，符合线性时间。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - `n` 为表达式的长度。我们只做一次线性扫描，每个字符至多进出栈一次，合并操作是 `O(1)`。  
  - 用大白话说，就是“字符多少，就花多少时间”，没有指数级的爆炸。  
- **空间复杂度**：`O(n)`  
  - 最坏情况下栈里会存放所有字符（比如全是左括号），所以空间与字符串长度同阶。  

---

## 心得  

- **核心技巧**：把每个子表达式抽象成“变成 0 / 1 的最小代价”这两个状态，利用**动态规划 + 栈**一次遍历完成全部计算。  
- **适用的题型**（类似思路）  
  1. **布尔表达式最小翻转代价**（本题的变体）。  
  2. **最小代价使表达式结果为真**（LeetCode 1800 系列）。  
  3. **计算表达式的最小/最大值**（如“加减乘除表达式加括号的最大值”）。  
- **一句话总结解题钥匙**：**把“值”拆成两种可能的代价，并在合并时同时考虑“保持运算符”和“改运算符”两条路线，取最小即可。**

---

## 反思  

- **第一反应**：看到“最小操作次数”马上想到**枚举所有改动**（暴力），因为直觉上改动越少越好。  
- **最容易踩的坑**  
  1. **忽视运算符优先级**——题目特意说明 `&` 与 `|` 没有优先级，必须左到右计算，否则会得到错误的代价。  
  2. **忘记把“改运算符”计入代价**——只算了改数字的情况，导致某些情况下答案偏大。  
  3. **边界情况**：表达式只有单个数字（如 `"0"`），此时直接返回 `1`（把它改成 `1`）即可。  
- **下次类似题目第一步**：先**确定每个最小子结构需要保存哪些状态**（本题是 `cost0`、`cost1`），再思考**如何用栈或递归把子结构组合起来**。这样可以避免一开始就陷入暴力枚举的误区。