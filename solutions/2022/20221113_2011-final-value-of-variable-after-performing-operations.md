# #2011. 执行操作后变量的最终值 / Final Value of Variable After Performing Operations

> 难度：简单 · 标签：Array、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/final-value-of-variable-after-performing-operations/)

---

## 题目（英文原版）

**Description**

There is a programming language with only four operations and one variable X:
Initially, the value of X is 0.
Given an array of strings operations containing a list of operations, return the final value of X after performing all the operations.

**Examples**

**Example 1:**

```
Input: operations = ["--X","X++","X++"]
Output: 1
Explanation: The operations are performed as follows:
Initially, X = 0.
--X: X is decremented by 1, X =  0 - 1 = -1.
X++: X is incremented by 1, X = -1 + 1 =  0.
X++: X is incremented by 1, X =  0 + 1 =  1.
```

**Example 2:**

```
Input: operations = ["++X","++X","X++"]
Output: 3
Explanation: The operations are performed as follows:
Initially, X = 0.
++X: X is incremented by 1, X = 0 + 1 = 1.
++X: X is incremented by 1, X = 1 + 1 = 2.
X++: X is incremented by 1, X = 2 + 1 = 3.
```

**Example 3:**

```
Input: operations = ["X++","++X","--X","X--"]
Output: 0
Explanation: The operations are performed as follows:
Initially, X = 0.
X++: X is incremented by 1, X = 0 + 1 = 1.
++X: X is incremented by 1, X = 1 + 1 = 2.
--X: X is decremented by 1, X = 2 - 1 = 1.
X--: X is decremented by 1, X = 1 - 1 = 0.
```

**Constraints**

- 1 <= operations.length <= 100
- operations[i] will be either "++X", "X++", "--X", or "X--".

---

## 题目（中文翻译）

**题目描述**  
有一种编程语言只包含四种操作，并且只有一个变量 `X`：  
- 初始时，`X` 的值为 `0`。  
- 给定一个字符串数组 `operations`，其中每个元素表示一次操作。请在执行完所有操作后，返回 `X` 的最终值。

**示例**

**示例 1**  
输入: `operations = ["--X","X++","X++"]`  
输出: `1`  
解释: 操作执行过程如下:  
- 初始时，`X = 0`。  
- `--X`: `X` 减 1，`X = 0 - 1 = -1`。  
- `X++`: `X` 加 1，`X = -1 + 1 = 0`。  
- `X++`: `X` 加 1，`X = 0 + 1 = 1`。

**示例 2**  
输入: `operations = ["++X","++X","X++"]`  
输出: `3`  
解释: 操作执行过程如下:  
- 初始时，`X = 0`。  
- `++X`: `X` 加 1，`X = 0 + 1 = 1`。  
- `++X`: `X` 加 1，`X = 1 + 1 = 2`。  
- `X++`: `X` 加 1，`X = 2 + 1 = 3`。

**示例 3**  
输入: `operations = ["X++","++X","--X","X--"]`  
输出: `0`  
解释: 操作执行过程如下:  
- 初始时，`X = 0`。  
- `X++`: `X` 加 1，`X = 0 + 1 = 1`。  
- `++X`: `X` 加 1，`X = 1 + 1 = 2`。  
- `--X`: `X` 减 1，`X = 2 - 1 = 1`。  
- `X--`: `X` 减 1，`X = 1 - 1 = 0`。

**约束条件**  
- `1 <= operations.length <= 100`  
- `operations[i]` 只能是 `"++X"`、`"X++"`、`"--X"` 或 `"X--"`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题只要求我们把一串“加一”“减一”的指令依次执行，最后返回变量 **X** 的值。  
最直接的想法就是：

1. 先把 **X** 初始化为 `0`（相当于一张空白的记事本）。
2. 按照数组的顺序遍历每一个字符串 `op`。  
   - 如果 `op` 是 `"++X"` 或者 `"X++"`，说明要把 **X** 加 `1`，就执行 `X += 1`。  
   - 其余两种 `"--X"`、`"X--"` 表示要把 **X** 减 `1`，就执行 `X -= 1`。  
3. 循环结束后，`X` 就是最终答案。

> **类比**：把 `operations` 想成一列排队的顾客，每位顾客要么给你 1 块钱（`++`），要么收走 1 块钱（`--`）。我们只需要把钱数累计起来即可。

为什么这个方法一定对？因为题目没有任何“跳过”或“提前结束”的特殊规则，**每条指令都必须执行一次**，所以只要逐条执行、正确累加增减值，最终得到的就是题目要求的结果。

#### 代码（Python）

```python
def finalValueAfterOperations(operations):
    """
    逐条模拟执行指令，返回 X 的最终值。
    :param operations: List[str]，每个元素是 ++X、X++、--X、X--
    :return: int，X 的最终数值
    """
    x = 0                     # 初始值为 0
    for op in operations:    # 按顺序遍历每条指令
        if op[0] == '+':      # ++X 或 X++，第一个字符是 '+'，说明要加 1
            x += 1
        else:                 # --X 或 X--，第一个字符是 '-'，说明要减 1
            x -= 1
    return x
```

> **关键行解释**  
> - `if op[0] == '+'`：只检查字符串的第一个字符就能区分加法和减法，因为四种合法指令的第一个字符必然是 `'+'` 或 `'-'`，不需要完整比较，写法更简洁。  

#### 复杂度

- **时间复杂度：** `O(n)`（其中 `n = len(operations)`），因为我们只遍历一次数组，每条指令的处理是 `O(1)` 的常数时间。  
  - **大白话**：如果有 100 条指令，就会做 100 次“加 1”或“减 1”，工作量随指令数线性增长。
- **空间复杂度：** `O(1)`，只用了一个整型变量 `x` 来保存当前值，和输入大小无关。

---

### 2. 最优解

#### 思路  

在暴力解中，我们已经是 **线性遍历一次**，时间已经是最优的 `O(n)`，没有更快的办法（必须看每条指令才能知道它是 `+1` 还是 `-1`）。  
不过我们可以把代码写得更简洁、更直观：**只统计加法出现的次数，减法出现的次数，最后用两者的差值**。

- `++` 或 `X++` 出现一次，就相当于 **+1**。  
- `--` 或 `X--` 出现一次，就相当于 **-1**。  

所以：

```
final = (# 加法) - (# 减法)
```

这一步仍然需要遍历一次数组来计数，但不需要在遍历过程中实时更新 `x`，只在遍历结束后做一次减法运算。  
从复杂度角度看，**时间仍是 O(n)，空间仍是 O(1)**，但思路更像“统计”而非“模拟”，对理解“增量/减量”概念更有帮助。

#### 代码（Python）

```python
def finalValueAfterOperations(operations):
    """
    统计 ++ 出现的次数与 -- 出现的次数之差，得到 X 的最终值。
    """
    inc = 0  # 加法计数器
    dec = 0  # 减法计数器

    for op in operations:
        # op 中只要出现 '+'，说明是一次加法
        if '+' in op:
            inc += 1
        else:               # 否则必然是 '--'，是一次减法
            dec += 1

    return inc - dec        # 加法次数减去减法次数，即为最终值
```

> **关键行解释**  
> - `if '+' in op:`：只要字符串里出现 `'+'`（不管是前缀还是后缀），就一定是加法。这样写更直观，也避免了判断字符位置。  
> - `return inc - dec`：把两类指令的计数相减，一步得到答案。

#### 复杂度

- **时间复杂度：** `O(n)`，仍然需要遍历全部指令一次。  
  - 与暴力解相比，工作量相同，只是把“即时加减”改成了“计数后统一计算”。  
- **空间复杂度：** `O(1)`，只用了两个计数器 `inc`、`dec`，占用常数级别的额外空间。

---

## 心得

- **核心技巧**：把“增/减”操作抽象为**计数**，再用计数差得到最终值。  
- **适用的题型**：  
  1. 只涉及两种相反操作的累计题（如“统计正负符号的净值”）。  
  2. “字符串中出现的特定子串计数”类问题（如统计 `"+1"` 与 `"-1"` 的净和）。  
  3. “投票/抵消”类问题（如 LeetCode 1656. Design an Ordered Stream 中的计数思路）。  
- **一句话总结解题钥匙**：**把每一次的增减看成 1 分，最后用加法次数减去减法次数即可得到答案**。

---

## 反思

- **第一反应**：直接写一个循环，遇到 `++` 就 `+1`，遇到 `--` 就 `-1`，这就是最自然的实现。  
- **最容易踩的坑**：  
  - 忽视了四种合法指令的顺序多样性，导致只检查 `op == "++X"` 之类的写法会漏掉 `X++`、`X--`。  
  - 没有考虑空数组的情况（虽然约束里最小长度是 1），但在实际面试中要养成检查边界的习惯。  
- **下次遇到同类题**：第一步先 **确认操作种类是否只有两种相反的**（如 +1 / -1），如果是，就直接 **统计出现次数**，再用差值求解。这样既简洁又不易出错。