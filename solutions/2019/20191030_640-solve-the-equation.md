# #640. 求解方程 / Solve the Equation

> 难度：中等 · 标签：Math、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/solve-the-equation/)

---

## 题目（英文原版）

**Description**

Solve a given equation and return the value of 'x' in the form of a string "x=#value". The equation contains only '+', '-' operation, the variable 'x' and its coefficient. You should return "No solution" if there is no solution for the equation, or "Infinite solutions" if there are infinite solutions for the equation.
If there is exactly one solution for the equation, we ensure that the value of 'x' is an integer.

**Examples**

**Example 1:**

```
Input: equation = "x+5-3+x=6+x-2"
Output: "x=2"
```

**Example 2:**

```
Input: equation = "x=x"
Output: "Infinite solutions"
```

**Example 3:**

```
Input: equation = "2x=x"
Output: "x=0"
```

**Constraints**

- 3 <= equation.length <= 1000
- equation has exactly one '='.
- equation consists of integers with an absolute value in the range [0, 100] without any leading zeros, and the variable 'x'.
- The input is generated that if there is a single solution, it will be an integer.

---

## 题目（中文翻译）

**描述：**  
求解给定的方程（**equation**），并以字符串 `"x=#value"` 的形式返回变量 **x** 的取值。方程仅包含加号 `'+'`、减号 `'-'` 运算、变量 **x** 以及其系数。若方程无解，返回 `"No solution"`；若存在无限多解，返回 `"Infinite solutions"`。如果方程恰好有唯一解，我们保证 **x** 的值为整数。

**示例：**  

```
Input: equation = "x+5-3+x=6+x-2"
Output: "x=2"
```

```
Input: equation = "x=x"
Output: "Infinite solutions"
```

```
Input: equation = "2x=x"
Output: "x=0"
```

**约束条件：**  
- 3 ≤ equation.length ≤ 1000  
- 方程（equation）恰好包含一个 `'='`  
- 方程仅由绝对值在 `[0, 100]` 范围内且不含前导零的整数和变量 **x** 组成  
- 输入保证若存在唯一解，则该解为整数

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把方程两边都看成**普通的算式**，把 `x` 当成一个普通的整数，然后**枚举**可能的 `x` 值，看看哪一个能让等式成立。

- **枚举范围**：题目保证如果有唯一解，它一定是整数。我们可以把搜索区间设得稍大一点（比如 `[-1000, 1000]`），在这个区间里一定能找到答案（实际测试发现答案几乎总在这个范围内）。  
- **求值方式**：把等式左边和右边的字符串分别解析成算式，然后用 Python 的 `eval`（或自己写一个简单的求值函数）得到数值。  
- **判断**：如果左边的值等于右边的值，就找到了 `x`。如果遍历完所有候选仍未找到，说明方程无解；如果左、右两边在所有 `x` 下都相等，则是「无限解」。

> **类比**：把 `x` 想成一本字典里没有解释的词，我们先把它假设成每本可能的页码（-1000 到 1000），然后逐页查找哪一页能让两句话的意思相同。

**为什么正确**  
枚举法穷举了所有可能的整数解，只要解在我们设定的搜索区间内，就一定能被找到。  

**时间/空间复杂度**  
- **时间**：我们要遍历 `O(R)` 个候选值（`R` 为搜索区间大小），每次都要解析并计算左右两边的表达式，解析的复杂度是 `O(L)`，`L` 为方程字符串长度（ ≤ 1000）。因此总体是 **O(R·L)**。如果 `R = 2001`（-1000~1000），则大约是 `2001·1000 ≈ 2·10⁶` 次基本操作，勉强能跑完。  
- **空间**：只用了常数级别的临时变量，**O(1)**。

#### 代码（Python）

```python
def eval_side(side: str, x: int) -> int:
    """
    计算等式一侧的值。
    side: 只包含数字、'x'、'+'、'-' 的字符串，例如 "x+5-3"
    x:   假设的 x 的取值
    """
    i, n = 0, len(side)
    total = 0          # 累计结果
    sign = 1           # 当前项的符号，+1 表示正，-1 表示负

    while i < n:
        if side[i] == '+':          # 遇到加号，符号设为正
            sign = 1
            i += 1
        elif side[i] == '-':        # 遇到减号，符号设为负
            sign = -1
            i += 1
        else:
            # 读取一个数或系数
            num = 0
            has_num = False
            while i < n and side[i].isdigit():
                num = num * 10 + int(side[i])
                i += 1
                has_num = True

            if i < n and side[i] == 'x':   # 当前项是 x 或 kx
                coeff = num if has_num else 1   # 没有显式系数时默认为 1
                total += sign * coeff * x
                i += 1
            else:                           # 当前项是纯数字
                total += sign * num
    return total


def solve_bruteforce(equation: str) -> str:
    left, right = equation.split('=')

    # 设定一个相对宽松的搜索范围
    for x in range(-1000, 1001):
        if eval_side(left, x) == eval_side(right, x):
            # 找到唯一解，直接返回
            return f"x={x}"

    # 若循环结束仍未返回，说明没有整数解
    # 再检查是否是「无限解」：左、右两边在任意 x 下都相等
    # 只需要把 x 替换成 0 和 1 两个不同的值做比较即可
    if eval_side(left, 0) == eval_side(right, 0) and \
       eval_side(left, 1) == eval_side(right, 1):
        return "Infinite solutions"
    return "No solution"
```

#### 复杂度

- **时间复杂度**：`O(R·L)`，`R` 为枚举范围大小（这里约为 2001），`L` 为方程长度（≤1000）。大白话：我们要「尝试」大约两千次，每次都要「读」一遍字符串，整体工作量大约是两千乘一千次基本操作。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有可能的 x**，这一步完全可以省掉。其实我们不需要真正求出每个 `x` 的值，只要把等式化简到 **ax = b** 的形式，就能直接求解。

1. **把等式左右两侧分别化成 “系数 × x + 常数” 的形式**  
   - 例如 `x+5-3+x` → `2x + 2`（系数 2，常数 2）  
   - 读取字符时，遇到 `x` 时累计 **x 的系数**，遇到普通数字时累计 **常数**。  
   - **符号**（`+` / `-`）决定是加还是减。  

2. **把右侧的项移到左侧**（即把右侧的系数和常数分别取相反数再加到左侧）  
   - 设左侧得到 `(a1, b1)`，右侧得到 `(a2, b2)`，则整体方程等价于  
     ```
     a1*x + b1 = a2*x + b2
     => (a1 - a2) * x = (b2 - b1)
     ```
   - 记 `A = a1 - a2`，`B = b2 - b1`。

3. **判断解的类型**  
   - **A = 0 且 B = 0**：两边完全相同，任意 x 都满足 → `"Infinite solutions"`  
   - **A = 0 且 B ≠ 0**：左边是常数，右边是另一个常数，不相等 → `"No solution"`  
   - **A ≠ 0**：唯一解 `x = B / A`，题目保证 `B` 能被 `A` 整除 → 返回 `"x=#value"`。

> **类比**：把等式看成天平，两边都有砝码（常数）和杠杆（`x`）。我们把右边的砝码和杠杆全部搬到左边，最后只剩下“一边的杠杆乘以系数等于另一边的砝码”。只要杠杆的系数不为零，就能直接算出砝码的重量。

**关键技巧**  
- **一次遍历**：左右两侧可以在同一次遍历中完成，只要记录当前遍历的是左边还是右边。  
- **系数的默认值**：当出现单独的 `x` 时，系数视为 `1`；出现 `-x` 时系数视为 `-1`。  
- **整数运算**：整个过程只用加减乘，不涉及除法（除法只在最后一步求解唯一解时出现，且一定整除）。

#### 代码（Python）

```python
def parse_side(side: str) -> (int, int):
    """
    将等式一侧解析为 (coeff_x, constant)。
    coeff_x : x 的系数之和
    constant: 常数之和
    """
    i, n = 0, len(side)
    coeff = 0      # x 的系数累计
    const = 0      # 常数累计
    sign = 1       # 当前项的符号 (+1 或 -1)

    while i < n:
        if side[i] == '+':          # 符号改为正
            sign = 1
            i += 1
        elif side[i] == '-':        # 符号改为负
            sign = -1
            i += 1
        else:
            # 读取数字（可能为空）
            num = 0
            has_num = False
            while i < n and side[i].isdigit():
                num = num * 10 + int(side[i])
                i += 1
                has_num = True

            if i < n and side[i] == 'x':   # 遇到 x
                # 没有数字时默认系数为 1，例如 "x"、"-x"
                coeff += sign * (num if has_num else 1)
                i += 1
            else:                           # 纯数字
                const += sign * num
    return coeff, const


def solve_optimal(equation: str) -> str:
    left, right = equation.split('=')

    # 解析左右两侧
    a1, b1 = parse_side(left)   # a1*x + b1
    a2, b2 = parse_side(right)  # a2*x + b2

    # 把右侧移到左侧
    A = a1 - a2          # x 的总系数
    B = b2 - b1          # 常数项的差值

    if A == 0:
        if B == 0:
            return "Infinite solutions"
        else:
            return "No solution"
    else:
        # 题目保证整除
        x = B // A
        return f"x={x}"
```

#### 复杂度

- **时间复杂度**：`O(L)`，只遍历一次方程字符串（长度 `L ≤ 1000`），每个字符做常数次操作。相较于暴力的 `O(R·L)`，这里不再有枚举，快得多。  
- **空间复杂度**：`O(1)`，只用了若干整数变量，和输入规模无关。

---

## 心得

- **核心技巧**：把等式两边化为 “系数 × x + 常数” 的线性形式，再通过移项得到 `ax = b`。这是一种**线性方程求解的标准套路**。  
- **适用题型**：  
  1. **一元一次方程求解**（本题）。  
  2. **含有变量的表达式求值**（如 LeetCode 640 “Solve the Equation”）。  
  3. **变量系数求和**（如 “Basic Calculator III” 中的变量处理）。  
- **一句话总结**：**把所有 `x` 项收集到一起，所有常数收集到一起，最后只剩 `ax = b`，直接除即可**。

## 反思

- **第一反应**：看到等式里只有 `+`、`-`、整数和 `x`，立刻想到把它们拆成系数与常数的线性组合。  
- **最容易踩的坑**：  
  - 忘记 `-x` 的系数是 `-1`（而不是 `0`）。  
  - 处理 “没有显式系数的 x” 时遗漏默认系数 `1`。  
  - 错误地把右侧的常数直接相减，而不是先把右侧的常数取反再加到左侧。  
  - 忽视“无限解”和“无解”的判定条件（`A==0` 时的两种情况）。  
- **下次第一步**：**先把等式两边分别解析成 `(coeff_x, constant)`**，这一步把所有后续的推导都变得线性且明确。