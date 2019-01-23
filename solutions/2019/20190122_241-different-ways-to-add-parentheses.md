# #241. 不同的添加括号方法 / Different Ways to Add Parentheses

> 难度：中等 · 标签：Math、String、Dynamic Programming、Recursion、Memoization · [LeetCode 链接](https://leetcode.com/problems/different-ways-to-add-parentheses/)

---

## 题目（英文原版）

**Description**

Given a string expression of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. You may return the answer in any order.
The test cases are generated such that the output values fit in a 32-bit integer and the number of different results does not exceed 104.

**Examples**

**Example 1:**

```
Input: expression = "2-1-1"
Output: [0,2]
Explanation:
((2-1)-1) = 0 
(2-(1-1)) = 2
```

**Example 2:**

```
Input: expression = "2*3-4*5"
Output: [-34,-14,-10,-10,10]
Explanation:
(2*(3-(4*5))) = -34 
((2*3)-(4*5)) = -14 
((2*(3-4))*5) = -10 
(2*((3-4)*5)) = -10 
(((2*3)-4)*5) = 10
```

**Constraints**

- 1 <= expression.length <= 20
- expression consists of digits and the operator '+', '-', and '*'.
- All the integer values in the input expression are in the range [0, 99].
- The integer values in the input expression do not have a leading '-' or '+' denoting the sign.

---

## 题目（中文翻译）

给定一个仅包含数字和运算符的字符串 `expression`，返回对数字和运算符进行所有可能的分组后计算得到的所有结果。返回的结果顺序可以任意。

测试用例保证所有输出值都能放入 32 位整数中，且不同结果的数量不超过 `10^4`。

**示例 1**  
**输入**: `expression = "2-1-1"`  
**输出**: `[0,2]`  
**解释**:  
- `((2-1)-1) = 0`  
- `(2-(1-1)) = 2`

**示例 2**  
**输入**: `expression = "2*3-4*5"`  
**输出**: `[-34,-14,-10,-10,10]`  
**解释**:  
- `(2*(3-(4*5))) = -34`  
- `((2*3)-(4*5)) = -14`  
- `((2*(3-4))*5) = -10`  
- `(2*((3-4)*5)) = -10`  
- `(((2*3)-4)*5) = 10`

**约束条件**  
- `1 <= expression.length <= 20`  
- `expression` 仅由数字和运算符 `'+'`、`'-'`、`'*'` 组成。  
- 输入表达式中的所有整数均在 `[0, 99]` 范围内。  
- 输入表达式中的整数不含表示符号的前导 `'-'` 或 `'+'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题要求把一个只包含数字和 `+ - *` 三种运算符的表达式，按照 **所有可能的加括号方式** 计算出结果。  
最直接的想法是：**把每一个运算符当作「最后一次计算」的切分点**，把表达式递归地拆成左右两部分，分别求出左边和右边所有可能的值，然后把左值和右值用当前运算符算一次，所有算出来的结果放进集合即可。

- **数据结构**：  
  - **列表** 用来保存每一次递归得到的所有可能结果。  
  - **递归栈**（函数调用本身）帮助我们把大问题拆成小问题。  
  - **字符串** 本身就是输入，遍历它找运算符就像在一串字符中寻找「关键字」——相当于在一本书里找每一个标点符号的位置。

- **为什么正确**：  
  对于任意合法的加括号方式，必然存在一个「最外层」的运算符，它把整个表达式分成左子表达式和右子表达式。递归正好把这种「最外层」的划分全部枚举出来，左子表达式和右子表达式又会继续被枚举，直到子表达式只剩一个数字（递归终止条件）。所以所有合法的括号组合都会被遍历到，得到的结果集合必然完整。

- **时间/空间复杂度**（大白话版）：  
  - **时间**：每遇到一个运算符就要把左、右两边的所有结果两两配对再算一次。假设表达式里有 `n` 个运算符，递归树的规模大约是 **Catalan 数**（一种和二叉树节点数有关的计数），它的增长速度接近 `4^n / (n^{1.5})`，也就是说 **指数级**（非常快）会爆炸。可以把它想成「每多加一个运算符，可能的组合数会翻几倍」。
  - **空间**：递归调用栈的深度最多是 `n`（运算符的个数），每层都要保存一个结果列表，最坏情况下总空间也是 **指数级**，不过主要的空间消耗是递归栈，约 `O(n)`。

#### 代码（Python）

```python
from typing import List

def diff_ways_to_compute(expression: str) -> List[int]:
    """
    暴力递归解法
    对每一个运算符把表达式分成左、右两段，递归求解子段的所有可能结果，
    再用当前运算符把左值和右值组合起来。
    """
    # 1. 如果整个 expression 只是一串数字，直接返回它本身
    if expression.isdigit():               # 只包含 0~9，说明没有运算符
        return [int(expression)]

    results = []                            # 用来收集所有可能的结果

    # 2. 遍历每个字符，找到运算符的位置
    for idx, ch in enumerate(expression):
        if ch in "+-*":                     # 只在运算符处做切分
            # 3. 把左边、右边的子表达式分别递归求解
            left_vals = diff_ways_to_compute(expression[:idx])
            right_vals = diff_ways_to_compute(expression[idx+1:])

            # 4. 把左子结果和右子结果两两配对，算出当前运算符的值
            for l in left_vals:
                for r in right_vals:
                    if ch == '+':
                        results.append(l + r)
                    elif ch == '-':
                        results.append(l - r)
                    else:                  # ch == '*'
                        results.append(l * r)

    return results
```

#### 复杂度

- **时间复杂度**：`O( Catalan(n) ) ≈ O(4^n / n^{1.5})`  
  这里的 `n` 是运算符的个数。可以把它想成「每多一个运算符，可能的组合数会成指数级增长」。
- **空间复杂度**：`O(n)`（递归栈深度）+ 结果列表的大小（指数级）。  
  递归调用本身最多占 `n` 层栈帧，除此之外主要的空间是保存所有结果的列表。

---

### 2. 最优解

#### 思路  

暴力递归的瓶颈在于 **大量重复子问题**：同一个子表达式会被多次递归求值。例如 `"2-1-1"`，左子表达式 `"2-1"` 会被分别在两条不同的递归路径里计算两遍。  
**记忆化**（Memoization）可以把已经算好的子表达式结果缓存起来，下次遇到相同子表达式直接取缓存，避免重复计算。

实现步骤：

1. **维护一个哈希表（字典）** `memo`，键是子表达式字符串，值是该子表达式对应的所有可能结果列表。  
   - 哈希表就像一本「查字典」：词是子表达式，页码是已经算好的结果集合。
2. **在递归入口先检查 `memo`**：如果子表达式已经出现过，直接返回缓存的答案。  
3. **其余逻辑和暴力递归完全相同**：遍历运算符、递归求左右子结果、两两组合。  
4. **递归结束后把本次得到的 `results` 放进 `memo`**，供后续复用。

这样每个不同的子表达式只会被计算 **一次**，而不同子表达式的数量最多是所有不同切分产生的子串，最多为 `O(n^2)`（因为子串的起止位置有 `n*(n+1)/2` 种），因此总体时间从指数级下降到 **多项式级**。

> **为什么仍然是多项式？**  
> 对每个子表达式我们仍然要遍历它内部所有运算符并进行两两配对，配对的次数正好是子表达式内部结果数的乘积。但因为每个子表达式只算一次，整体复杂度是 `O(n^3)`（常见的区间 DP 复杂度），足够快。

#### 代码（Python）

```python
from typing import List, Dict

def diff_ways_to_compute_opt(expression: str) -> List[int]:
    """
    记忆化递归（自顶向下动态规划）实现
    使用 dict memo 把已经算好的子表达式缓存，避免重复计算。
    """
    memo: Dict[str, List[int]] = {}   # 全局缓存

    def helper(expr: str) -> List[int]:
        # 1. 先查缓存
        if expr in memo:
            return memo[expr]

        # 2. 纯数字直接返回
        if expr.isdigit():
            memo[expr] = [int(expr)]
            return memo[expr]

        res: List[int] = []

        # 3. 按运算符切分子问题
        for i, ch in enumerate(expr):
            if ch in "+-*":
                left = helper(expr[:i])          # 左子表达式的所有可能值
                right = helper(expr[i+1:])       # 右子表达式的所有可能值

                # 4. 两两配对计算
                for l in left:
                    for r in right:
                        if ch == '+':
                            res.append(l + r)
                        elif ch == '-':
                            res.append(l - r)
                        else:                    # ch == '*'
                            res.append(l * r)

        # 5. 把本次结果存进缓存
        memo[expr] = res
        return res

    return helper(expression)
```

#### 复杂度

- **时间复杂度**：`O(n^3)`  
  - `n` 为表达式的字符长度（最多 20）。  
  - 解释：一共有 `O(n^2)` 种不同的子表达式（所有区间），对每个子表达式我们遍历其中的运算符（最多 `n` 次），并进行左右结果的两两配对（这一步的总和仍然在 `O(n)` 级别），综合起来是立方级别。相比指数级的暴力递归，已经快得多。

- **空间复杂度**：`O(n^2)`  
  - 缓存 `memo` 最多保存 `O(n^2)` 个子表达式对应的结果列表。  
  - 递归栈的深度仍是 `O(n)`。  
  - 这在本题的约束（`n ≤ 20`）下完全可以接受。

---

## 心得

- **核心技巧**：**区间划分 + 记忆化递归（或自底向上 DP）**。  
  把一个整体问题拆成「左区间」和「右区间」的组合，然后用哈希表把已经算好的子区间结果记住，避免重复计算。

- **适用的题型**  
  1. **不同的二叉树构造**（如 `Unique Binary Search Trees`）  
  2. **矩阵连乘的最小代价**（Matrix Chain Multiplication）  
  3. **不同的布尔表达式求值**（Boolean Parenthesization）  

- **一句话总结解题钥匙**：  
  “把每个运算符视作最后一步的切分点，用记忆化把子表达式的结果缓存，递归即可遍历全部括号方式。”

---

## 反思

- **第一反应**：看到“所有可能的加括号方式”，立刻想到 **递归枚举**，把表达式拆成左、右两块再组合。

- **最容易踩的坑**  
  - **忘记对纯数字的终止判断**，会导致无限递归。  
  - **结果重复**：不同的括号方式可能产生相同的数值，题目并不要求去重，只要把所有出现的结果都收集即可。  
  - **缓存键的选择**：一定要用 **子表达式字符串** 作为键，不能只用区间索引（因为我们是基于字符串切片实现的）。  

- **下次遇到同类题**：第一步先 **判断是否存在大量重复子问题**，如果有，就立刻考虑 **记忆化（或 DP）**；再把问题抽象为 “在每个运算符处切分，左右子问题递归求解”。这样就能把指数级暴力递归压缩到多项式时间。