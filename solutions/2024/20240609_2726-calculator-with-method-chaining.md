# #2726. 链式调用的计算器 / Calculator with Method Chaining

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/calculator-with-method-chaining/)

---

## 题目（英文原版）

**Description**

Design a Calculator class. The class should provide the mathematical operations of addition, subtraction, multiplication, division, and exponentiation. It should also allow consecutive operations to be performed using method chaining. The Calculator class constructor should accept a number which serves as the initial value of result.
Your Calculator class should have the following methods:
Solutions within 10-5 of the actual result are considered correct.

**Examples**

**Example 1:**

```
Input: 
actions = ["Calculator", "add", "subtract", "getResult"], 
values = [10, 5, 7]
Output: 8
Explanation: 
new Calculator(10).add(5).subtract(7).getResult() // 10 + 5 - 7 = 8
```

**Example 2:**

```
Input: 
actions = ["Calculator", "multiply", "power", "getResult"], 
values = [2, 5, 2]
Output: 100
Explanation: 
new Calculator(2).multiply(5).power(2).getResult() // (2 * 5) ^ 2 = 100
```

**Example 3:**

```
Input: 
actions = ["Calculator", "divide", "getResult"], 
values = [20, 0]
Output: "Division by zero is not allowed"
Explanation: 
new Calculator(20).divide(0).getResult() // 20 / 0 

The error should be thrown because we cannot divide by zero.
```

**Constraints**

- actions is a valid JSON array of strings
- values is a valid JSON array of numbers
- 2 <= actions.length <= 2 * 104
- 1 <= values.length <= 2 * 104 - 1
- actions[i] is one of "Calculator", "add", "subtract", "multiply", "divide", "power", and "getResult"
- First action is always "Calculator"
- Last action is always "getResult"

---

## 题目（中文翻译）

设计一个 **Calculator** 类。该类应提供加法（addition）、减法（subtraction）、乘法（multiplication）、除法（division）和指数运算（exponentiation）的数学操作，并且支持通过方法链（method chaining）进行连续操作。**Calculator** 类的构造函数应接受一个数字，作为结果的初始值。

你的 **Calculator** 类需要实现以下方法（具体实现细节请参见题目要求）：

- `add(number)`
- `subtract(number)`
- `multiply(number)`
- `divide(number)`
- `power(number)` // 进行指数运算
- `getResult()`

**注意**：答案在实际结果的 ±10⁻⁵ 范围内均视为正确。

## 示例

### 示例 1
**输入**  
```text
actions = ["Calculator", "add", "subtract", "getResult"]
values = [10, 5, 7]
```
**输出**  
```text
8
```
**解释**  
`new Calculator(10).add(5).subtract(7).getResult()` // 10 + 5 - 7 = 8

### 示例 2
**输入**  
```text
actions = ["Calculator", "multiply", "power", "getResult"]
values = [2, 5, 2]
```
**输出**  
```text
100
```
**解释**  
`new Calculator(2).multiply(5).power(2).getResult()` // (2 * 5) ^ 2 = 100

### 示例 3
**输入**  
```text
actions = ["Calculator", "divide", "getResult"]
values = [20, 0]
```
**输出**  
```text
"Division by zero is not allowed"
```
**解释**  
`new Calculator(20).divide(0).getResult()` // 20 / 0  

由于除数为零，应该抛出错误，因为除零是非法操作。

## 约束条件
- `actions` 是一个合法的 JSON 字符串数组，元素为字符串。
- `values` 是一个合法的 JSON 字符串数组，元素为数字。
- `2 <= actions.length <= 2 * 10⁴`
- `1 <= values.length <= 2 * 10⁴ - 1`
- `actions[i]` 只能是 `"Calculator"`、`"add"`、`"subtract"`、`"multiply"`、`"divide"`、`"power"` 或 `"getResult"`。
- 第一个操作必定是 `"Calculator"`。
- 最后一个操作必定是 `"getResult"`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每一次调用的操作先记下来，等到 `getResult()` 时再一次性把所有操作全部执行一遍。  
- **数据结构**：我们可以用一个普通的 Python 列表 `ops` 来保存“操作 + 参数”。列表就像一本记事本，往后面写（`append`）就相当于把每一步记下来，最后再从头读（遍历）一遍。  
- **为什么正确**：因为题目只要求 **先后顺序** 地对初始值做加、减、乘、除、幂运算，记下顺序后再统一计算，得到的结果必然和一步一步即时计算是一样的。  
- **复杂度直白解释**：  
  - 把每一次调用记录下来是 **O(1)**（常数时间），因为只往列表尾部加一个元素。  
  - 当调用 `getResult()` 时，需要遍历整条记录，最多 `n` 次操作（`n` 为调用次数），所以时间是 **O(n)**，即“和操作次数成正比”。  
  - 额外的空间是存这条记录，需要 `n` 个元素，也就是 **O(n)**。  

> 大白话：如果你把所有步骤写在纸上，最后一次性算出来，算的时间跟步骤数一样多，纸上要写的字数也跟步骤数一样多。

#### 代码（Python）  

```python
class Calculator:
    """
    直觉解：把每一步操作先记下来，等 getResult 时一次性算。
    """
    def __init__(self, init_val: float):
        self.init = init_val          # 初始值，等同于“记事本的第一行”
        self.ops = []                 # 用列表保存后续的每一次操作

    # 以下每个方法只负责把操作记录下来，不立刻算出结果
    def add(self, x: float):
        self.ops.append(('add', x))   # 记下“加 x”
        return self                  # 为了支持链式调用，返回自身

    def subtract(self, x: float):
        self.ops.append(('sub', x))   # 记下“减 x”
        return self

    def multiply(self, x: float):
        self.ops.append(('mul', x))   # 记下“乘 x”
        return self

    def divide(self, x: float):
        self.ops.append(('div', x))   # 记下“除 x”
        return self

    def power(self, x: float):
        self.ops.append(('pow', x))   # 记下“幂 x”
        return self

    def getResult(self):
        """遍历所有记录，依次执行运算并返回最终结果。"""
        result = self.init
        for op, val in self.ops:
            if op == 'add':
                result += val
            elif op == 'sub':
                result -= val
            elif op == 'mul':
                result *= val
            elif op == 'div':
                if val == 0:                     # 除 0 需要报错
                    return "Division by zero is not allowed"
                result /= val
            elif op == 'pow':
                result **= val
        return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - “n” 是调用除 `getResult` 之外的方法的次数。遍历一次列表算所有操作，需要的时间随操作次数线性增长。  
- **空间复杂度**：`O(n)`  
  - 需要额外的列表来存 `n` 条操作记录，列表越长占的内存越多。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，真正的“慢点”不在遍历，而在 **把操作记录下来再算** 这一步。  
- **瓶颈**：每次 `getResult` 都要重新走一遍所有历史操作，等价于把已经算好的结果“抹掉”，重新算一遍。  
- **优化方向**：**即时更新** 结果。也就是说，每执行一次 `add`、`subtract` …，就立刻把结果算出来并保存，而不是等到最后。这样 `getResult` 只需要把已经算好的值直接返回，时间就是 **O(1)**（常数时间）。  
- **核心技巧**：**方法链式返回 `self`**。在面向对象编程里，方法如果返回对象本身，就可以像 `obj.method1().method2()` 这样连续调用。这里我们在每个算术方法里 **先做运算 → 再返回 `self`**。  
- **类比**：想象你在厨房做菜，一步一步往锅里加料并立刻翻炒，最后端出来的菜已经是完成状态；而不是把所有料都倒进碗里，等到客人来时才一次性全部炒。显然前者更省时。  

#### 代码（Python）  

```python
class Calculator:
    """
    最优解：每次调用算术方法时立即更新 result，getResult 只返回 result。
    """
    def __init__(self, init_val: float):
        self.result = float(init_val)   # 当前累计结果，随时保持最新

    def add(self, x: float):
        """result = result + x"""
        self.result += x
        return self                     # 支持链式调用

    def subtract(self, x: float):
        """result = result - x"""
        self.result -= x
        return self

    def multiply(self, x: float):
        """result = result * x"""
        self.result *= x
        return self

    def divide(self, x: float):
        """result = result / x，除 0 时返回错误信息"""
        if x == 0:
            # 为了让整个链式调用仍能结束，直接把错误信息保存进去
            self.result = "Division by zero is not allowed"
        else:
            self.result /= x
        return self

    def power(self, x: float):
        """result = result ** x"""
        # 如果前面已经出现除 0 错误，直接跳过后续运算
        if isinstance(self.result, str):
            return self
        self.result **= x
        return self

    def getResult(self):
        """直接返回当前的 result（已经是最终值）"""
        return self.result
```

#### 复杂度  

- **时间复杂度**：`O(1)`  
  - 每个算术方法只做一次基本运算（加、减、乘、除、幂），不随调用次数增加而变慢。`getResult` 只返回已有的结果，时间恒定。  
- **空间复杂度**：`O(1)`  
  - 只保存一个数字（或错误字符串），不需要额外的列表或数组，内存使用固定不变。  

> 与暴力解对比：我们把“把所有操作记下来再算”这一步的 **O(n)** 迁移到了每一次调用本身，使得最终查询 (`getResult`) 成本几乎为零。

---

## 心得  

- **核心技巧**：**即时更新状态 + 方法返回自身实现链式调用**。  
- **适用题型**：  
  1. 需要连续调用多步操作的“构造器/构建者模式”题目（例如 `StringBuilder`、`QueryBuilder`）。  
  2. 需要在每一步都保持最新状态的 “累计/滚动” 类题目（如累计和、滑动窗口的手写实现）。  
- **一句话总结**：让对象在每一步就把结果算好，并返回自身，就能做到 **O(1) 查询、O(1) 额外空间** 的高效链式计算。  

---

## 反思  

- **第一反应**：把所有操作记录下来，最后一次性计算——因为最容易想到“先记后算”。  
- **最容易踩的坑**：  
  - **除零错误**：必须在 `divide` 时立即检测并返回/保存错误信息，否则会在后续的幂运算中出现异常。  
  - **链式返回忘记**：如果方法没有 `return self`，链式调用会在第一步后报 `'NoneType' object has no attribute ...'`。  
  - **错误传播**：除零后后面的操作应当被“短路”，即不再继续修改结果。  
- **下次思考**：看到“连续调用”或“链式”关键字时，第一步就考虑 **“每一步立即更新内部状态并返回自身”**，而不是先累积再统一处理。这样往往能直接得到最优解。