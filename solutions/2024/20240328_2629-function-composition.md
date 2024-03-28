# #2629. 函数组合 / Function Composition

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/function-composition/)

---

## 题目（英文原版）

**Description**

Given an array of functions [f1, f2, f3, ..., fn], return a new function fn that is the function composition of the array of functions.
The function composition of [f(x), g(x), h(x)] is fn(x) = f(g(h(x))).
The function composition of an empty list of functions is the identity function f(x) = x.
You may assume each function in the array accepts one integer as input and returns one integer as output.

**Examples**

**Example 1:**

```
Input: functions = [x => x + 1, x => x * x, x => 2 * x], x = 4
Output: 65
Explanation:
Evaluating from right to left ...
Starting with x = 4.
2 * (4) = 8
(8) * (8) = 64
(64) + 1 = 65
```

**Example 2:**

```
Input: functions = [x => 10 * x, x => 10 * x, x => 10 * x], x = 1
Output: 1000
Explanation:
Evaluating from right to left ...
10 * (1) = 10
10 * (10) = 100
10 * (100) = 1000
```

**Example 3:**

```
Input: functions = [], x = 42
Output: 42
Explanation:
The composition of zero functions is the identity function
```

**Constraints**

- -1000 <= x <= 1000
- 0 <= functions.length <= 1000
- all functions accept and return a single integer

---

## 题目（中文翻译）

给定一个函数数组 `[f1, f2, f3, ..., fn]`，返回一个新函数 `fn`，它是该数组的函数组合（function composition）。  
函数组合 `[f(x), g(x), h(x)]` 的形式为 `fn(x) = f(g(h(x)))`。  
空函数列表的函数组合是标识函数（identity function）`f(x) = x`。  
你可以假设数组中的每个函数都接受一个整数作为输入，并返回一个整数作为输出。

## 示例

### 示例 1
**输入**: `functions = [x => x + 1, x => x * x, x => 2 * x]`, `x = 4`  
**输出**: `65`  
**解释**:  
从右往左依次计算 …  
- 先从 `x = 4` 开始。  
- `2 * (4) = 8`  
- `(8) * (8) = 64`  
- `(64) + 1 = 65`

### 示例 2
**输入**: `functions = [x => 10 * x, x => 10 * x, x => 10 * x]`, `x = 1`  
**输出**: `1000`  
**解释**:  
从右往左依次计算 …  
- `10 * (1) = 10`  
- `10 * (10) = 100`  
- `10 * (100) = 1000`

### 示例 3
**输入**: `functions = []`, `x = 42`  
**输出**: `42`  
**解释**:  
零个函数的组合即为标识函数。

## 约束条件
- `-1000 <= x <= 1000`
- `0 <= functions.length <= 1000`
- 所有函数均接受且返回单个整数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把函数一个接一个地执行**。  
把题目中的函数列表想象成一条生产线，原材料 `x` 先进入最右边的机器（最里层的函数），加工后交给左边的机器，依次类推，最后得到成品。  

- **使用的数据结构**：普通的 Python 列表 `functions`，它就像一排排机器的编号，顺序很重要。  
- **为什么正确**：函数复合的定义就是 `f(g(h(x)))`，也就是从右往左依次把每个函数的返回值当作下一个函数的输入。只要我们严格按照这个顺序调用，就一定得到正确的结果。  
- **时间/空间复杂度**：  
  - 时间复杂度：我们需要遍历整个函数列表一次，对每个函数都调用一次。若列表长度为 `n`，则总共做 `n` 次函数调用，记作 **O(n)**。这里的 “O(n)” 可以理解为“随着函数个数线性增长”。  
  - 空间复杂度：只用了常数级别的额外变量（比如 `result`），与 `n` 无关，记作 **O(1)**。

#### 代码（Python）

```python
from typing import List, Callable

def compose(functions: List[Callable[[int], int]]) -> Callable[[int], int]:
    """
    返回一个新函数 fn，使得 fn(x) = f1(f2(...(fn(x))...))
    """
    # 如果列表为空，直接返回恒等函数（输入返回自身）
    if not functions:
        return lambda x: x

    # 暴力实现：在调用时依次执行所有函数
    def composed(x: int) -> int:
        result = x                      # 先把原始输入保存下来
        # 从右到左遍历函数列表（即先执行最里层的函数）
        for func in reversed(functions):
            result = func(result)       # 把上一次的结果喂给当前函数
        return result
    return composed
```

#### 复杂度  

- **时间复杂度**：O(n) — 随着函数个数线性增加，每个函数都要调用一次。  
- **空间复杂度**：O(1) — 只用了几个临时变量，不会随 `n` 增长。  

---

### 2. 最优解

#### 思路  

从暴力解来看，**唯一的瓶颈**就是每次调用返回的函数时都要遍历一次列表。如果我们在**生成返回函数的那一刻**就把所有函数“合并”成一个新的函数，那么以后每次调用只需要一次函数调用即可（虽然内部仍然会依次执行原函数，但对使用者来说是一次调用）。

在 Python 中可以利用 `functools.reduce`（相当于把列表“折叠”成一个值）来**一次性构造**这个组合函数：

1. **从右往左折叠**：`reduce` 的默认方向是从左到右，但我们可以把列表反转后再折叠，或者直接使用 `functools.reduce` 的 `lambda acc, f: lambda x: f(acc(x))`。  
2. **空列表的特殊情况**：如果列表为空，`reduce` 会抛异常，这时直接返回恒等函数即可。  

核心概念——**函数组合**（function composition）本身就是一种 **高阶函数**（接受函数并返回函数），我们只需要把它写成一个表达式即可。

#### 代码（Python）

```python
from typing import List, Callable
from functools import reduce

def compose(functions: List[Callable[[int], int]]) -> Callable[[int], int]:
    """
    使用 reduce 把所有函数一次性“合并”成一个新函数。
    """
    # 空列表直接返回恒等函数
    if not functions:
        return lambda x: x

    # 先把函数列表逆序（因为组合要求从右到左），再用 reduce 把它们折叠成一个函数
    # reduce 的 accumulator 初始值是恒等函数 lambda x: x
    composed = reduce(
        lambda acc, f: lambda x: f(acc(x)),   # 把当前函数 f 包装在已有的 acc 之上
        reversed(functions),                 # 逆序遍历，使得最右侧的函数最先执行
        lambda x: x                          # 初始的 acc 是恒等函数
    )
    return composed
```

#### 复杂度  

- **时间复杂度**：O(n) — 生成组合函数时遍历一次列表；后续每次调用 `composed(x)` 仍然会依次执行 `n` 次原函数，**但对外部调用者来说只需一次函数调用**，代码更简洁。  
- **空间复杂度**：O(1) — 只用了常数级别的临时变量（`acc`、`f`），不随 `n` 增长。  

> 与暴力解的时间复杂度相同，但最优解把“遍历列表”这一步提前到了函数生成阶段，使得返回的函数在使用时更像“一次性黑盒”，代码可读性更好。

---

## 心得

- **核心技巧**：高阶函数 & 函数组合（function composition），以及 `functools.reduce` 的折叠思路。  
- **适用的题型**  
  1. 多个单变量函数需要顺序执行的情形（如“函数管道”）。  
  2. 需要把若干操作合并成一次调用的场景（例如对列表的多步转换）。  
  3. 实现“中间件”或“拦截器”链式调用的系统设计题。  
- **一句话总结解题钥匙**：**把“从右到左依次调用”抽象成“把函数一个接一个包进去”，用 `reduce` 把这层包裹一次性完成。**

---

## 反思

- **第一反应**：把所有函数按顺序手动调用，写个循环就行。  
- **最容易踩的坑**  
  - 忘记**从右到左**执行，导致顺序颠倒得到错误结果。  
  - 当函数列表为空时，没有返回恒等函数 `lambda x: x`，会导致 `None` 被当作函数调用而报错。  
  - `reduce` 的初始值如果忘记设成恒等函数，空列表会抛 `TypeError`。  
- **下次类似题的第一步**：先确认**执行顺序**（左→右还是右→左），再决定是直接循环还是用 `reduce` 把步骤“折叠”成一个高阶函数。