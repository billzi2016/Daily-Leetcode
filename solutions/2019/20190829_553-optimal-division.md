# #553. 最优除法 / Optimal Division

> 难度：中等 · 标签：Array、Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/optimal-division/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. The adjacent integers in nums will perform the float division.
However, you can add any number of parenthesis at any position to change the priority of operations. You want to add these parentheses such the value of the expression after the evaluation is maximum.
Return the corresponding expression that has the maximum value in string format.
Note: your expression should not contain redundant parenthesis.

**Examples**

**Example 1:**

```
Input: nums = [1000,100,10,2]
Output: "1000/(100/10/2)"
Explanation: 1000/(100/10/2) = 1000/((100/10)/2) = 200
However, the bold parenthesis in "1000/((100/10)/2)" are redundant since they do not influence the operation priority.
So you should return "1000/(100/10/2)".
Other cases:
1000/(100/10)/2 = 50
1000/(100/(10/2)) = 50
1000/100/10/2 = 0.5
1000/100/(10/2) = 2
```

**Example 2:**

```
Input: nums = [2,3,4]
Output: "2/(3/4)"
Explanation: (2/(3/4)) = 8/3 = 2.667
It can be shown that after trying all possibilities, we cannot get an expression with evaluation greater than 2.667
```

**Constraints**

- 1 <= nums.length <= 10
- 2 <= nums[i] <= 1000
- There is only one optimal division for the given input.

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`。数组中相邻的整数（adjacent integers）将进行浮点除法（float division）。然而，你可以在任意位置添加任意数量的括号（parenthesis）来改变运算的优先级（priority）。目标是添加这些括号，使得表达式（expression）求值后的结果最大（maximum）。返回能够得到最大值的表达式，要求以字符串形式返回。

**注意**：返回的表达式中不能出现影响运算优先级的冗余括号（redundant parenthesis）。

示例 1  
Input: nums = [1000,100,10,2]  
Output: `"1000/(100/10/2)"`  
Explanation: `1000/(100/10/2) = 1000/((100/10)/2) = 200`。然而 `"1000/((100/10)/2)"` 中的加粗括号是冗余的，因为它们不影响运算优先级。因此应返回 `"1000/(100/10/2)"`。其他情况的计算如下：  
- `1000/(100/10)/2 = 50`  
- `1000/(100/(10/2)) = 50`  
- `1000/100/10/2 = 0.5`  
- `1000/100/(10/2) = 2`

示例 2  
Input: nums = [2,3,4]  
Output: `"2/(3/4)"`  
Explanation: `(2/(3/4)) = 8/3 ≈ 2.667`。经全部可能性验证，无法得到大于 `2.667` 的表达式值。

约束条件  
- `1 <= nums.length <= 10`  
- `2 <= nums[i] <= 1000`  
- 对于给定的输入，最优除法的表达式是唯一的。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的加括号方式**，计算每一种表达式的值，取最大的那一个。  

- **数据结构**：我们用**递归树**来模拟“在两个相邻数之间先算哪一步”。递归的每一层都把当前数组划分成左子表达式和右子表达式两部分，分别递归求值，再用除法 `left / right` 合成当前结果。  
- **类比**：想象你在写数学算式，手里有一串数字 `1000 100 10 2`，你可以随意在它们之间画上“先算哪儿”的圈（括号），每画一次圈就相当于把这段算式切成左边和右边两块，左边先算完再除以右边的结果。  
- **正确性**：递归会遍历 **所有合法的二叉树结构**（即所有合法的加括号方式），而每棵二叉树对应唯一一种运算顺序，故一定能找到最大值。  

**时间复杂度**  
- 对长度为 `n` 的数组，合法的二叉树数量是第 `n‑1` 个 Catalan 数，约为 `C_n ≈ 4^n / (n^{3/2}√π)`，随 `n` 指数级增长。  
- 因此暴力搜索的时间复杂度是 **O(Catalan(n)) ≈ O(4^n)**。在本题 `n ≤ 10` 时还能接受（`4^10 ≈ 1,048,576`），但不算优雅。  
- **空间复杂度**：递归深度最多 `n`，每层保存临时字符串和数值，故为 **O(n)**。

#### 代码（Python）

```python
from typing import List, Tuple
import math

def optimal_division_bruteforce(nums: List[int]) -> str:
    """
    暴力递归枚举所有加括号方式，返回取值最大的表达式。
    返回的表达式保证没有冗余括号（在合并时会去掉不必要的层）。
    """
    # 递归函数返回两个信息：最大值对应的表达式, 该表达式的数值
    def dfs(l: int, r: int) -> Tuple[str, float]:
        # 只剩一个数字时，表达式就是它本身，值也就是它
        if l == r:
            return str(nums[l]), float(nums[l])

        best_val = -math.inf
        best_expr = ""

        # 把区间 [l, r] 划分成左子区间 [l, i] 与右子区间 [i+1, r]
        for i in range(l, r):
            left_expr, left_val = dfs(l, i)
            right_expr, right_val = dfs(i + 1, r)

            # 当前运算是 left / right
            cur_val = left_val / right_val

            if cur_val > best_val:
                best_val = cur_val
                # 右边如果是单个数字，就不需要额外的括号
                if i + 1 == r:
                    cur_expr = f"{left_expr}/{right_expr}"
                else:
                    cur_expr = f"{left_expr}/({right_expr})"
                best_expr = cur_expr

        return best_expr, best_val

    expr, _ = dfs(0, len(nums) - 1)
    return expr
```

#### 复杂度

- **时间复杂度**：`O(4^n)`（Catalan 数），因为我们枚举所有可能的二叉树结构。  
  > 大白话：如果数组长度是 10，最坏情况下要检查大约一百万种括号放法，电脑还能接受，但如果长度是 20，时间会炸掉。
- **空间复杂度**：`O(n)`，递归栈深度最多等于数组长度。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于大量重复的子问题：同样的子数组会被多次计算。更重要的是，观察题目要求的 **“最大化结果”**，可以发现一个数学规律：

- 整个表达式的形式是 `a0 / a1 / a2 / … / an-1`，如果不加括号，等价于左结合 `(((a0 / a1) / a2) / …) / an-1`，结果会非常小。  
- 为了让结果尽可能大，需要 **让分母尽可能小**。  
- 分母是 `a1 / a2 / … / an-1`，**把它整体放进一对括号**，并且在这对括号内部采用 **左结合**（即不再添加额外括号），可以让分母的值最小，从而整体最大。

**证明（直观）**  
- 对于任意三个数 `x / y / z`，有两种加括号的方式：
  1. `(x / y) / z = x / (y * z)`  
  2. `x / (y / z) = x * (z / y)`  
  显然第二种把 `z` 提到分子，结果更大。  
- 通过归纳可以得到：只要第一个数单独在最左边，**其余所有数都放在同一个除号的右边**，并且内部保持左结合，就能得到全局最大值。

因此最优表达式的构造非常简单：

- 当 `len(nums) == 1`，直接返回该数字。  
- 当 `len(nums) == 2`，只能写成 `"a0/a1"`。  
- 当 `len(nums) >= 3`，返回 `"a0/(a1/a2/.../an-1)"`，其中内部不加额外括号。

**为什么没有冗余括号**  
- 题目要求“没有冗余括号”。在 `a0/(a1/a2/.../an-1)` 中，内部的除法已经是左结合，去掉任何一层括号都会改变运算顺序（比如 `a0/(a1/a2)/a3` 与 `a0/(a1/a2/a3)` 不等），所以都是必要的。

#### 代码（Python）

```python
from typing import List

def optimalDivision(nums: List[int]) -> str:
    """
    根据数学归纳得到的最优结构，直接构造表达式。
    复杂度为 O(n)。
    """
    n = len(nums)
    # 只有一个数，直接返回
    if n == 1:
        return str(nums[0])

    # 只有两个数，唯一的合法写法
    if n == 2:
        return f"{nums[0]}/{nums[1]}"

    # n >= 3，按照 a0/(a1/a2/.../an-1) 的形式写
    # 把除第一个数外的其余数用 '/' 连接起来
    denominator = "/".join(str(x) for x in nums[1:])
    return f"{nums[0]}/({denominator})"
```

#### 复杂度

- **时间复杂度**：`O(n)`，只需要一次遍历把除第一个数外的其余数拼接成字符串。  
  > 与暴力解的指数级时间相比，线性时间几乎是瞬间完成，即使 `n = 10` 也只需要几微秒。
- **空间复杂度**：`O(n)`，主要是存放生成的字符串（长度与 `n` 成正比）。

---

## 心得

- **核心技巧**：利用除法的“分子/分母”结构，将 **让分母最小化** 作为目标，归纳得到“一左一右，其余全部放在右边的括号里”。  
- **适用的题型**：  
  1. **最大/最小化表达式**（如 “Maximum Value of an Arithmetic Expression”）  
  2. **运算顺序影响结果的题目**（如 “Different Ways to Add Parentheses”）  
  3. **涉及除法或乘法的最优化**（如 “Maximum Product of Three Numbers” 的思路类似）  
- **一句话总结**：**把第一个数单独留下，后面的所有数整体放进一个除号的右侧括号**，即可得到最大值。

---

## 反思

- **第一反应**：看到“加任意括号”立刻想到**递归枚举所有二叉树**，因为这是最直观的完整搜索方式。  
- **最容易踩的坑**：  
  - **冗余括号**：在暴力实现时容易产生多余的 `()`，需要在拼接时判断右子表达式是否只有一个数字。  
  - **除以 0**：虽然题目保证 `nums[i] ≥ 2`，但若改成更通用的输入，需要防止除数为 0。  
  - **浮点误差**：暴力搜索时比较 `float` 值可能产生微小误差，实际实现时更推荐比较分子/分母的有理数或使用 `Fraction`。  
- **下次思路**：面对“加括号求最值”这类问题，先**思考运算符的单调性**（除法是单调递减的），尝试用**数学归纳或贪心**直接构造最优结构，再决定是否需要完整搜索。这样往往能在 O(n) 时间内得到答案。