# #2232. **通过在表达式中添加括号最小化结果** / Minimize Result by Adding Parentheses to Expression

> 难度：中等 · 标签：String、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimize-result-by-adding-parentheses-to-expression/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string expression of the form "<num1>+<num2>" where <num1> and <num2> represent positive integers.
Add a pair of parentheses to expression such that after the addition of parentheses, expression is a valid mathematical expression and evaluates to the smallest possible value. The left parenthesis must be added to the left of '+' and the right parenthesis must be added to the right of '+'.
Return expression after adding a pair of parentheses such that expression evaluates to the smallest possible value. If there are multiple answers that yield the same result, return any of them.
The input has been generated such that the original value of expression, and the value of expression after adding any pair of parentheses that meets the requirements fits within a signed 32-bit integer.

**Examples**

**Example 1:**

```
Input: expression = "247+38"
Output: "2(47+38)"
Explanation: The expression evaluates to 2 * (47 + 38) = 2 * 85 = 170.
Note that "2(4)7+38" is invalid because the right parenthesis must be to the right of the '+'.
It can be shown that 170 is the smallest possible value.
```

**Example 2:**

```
Input: expression = "12+34"
Output: "1(2+3)4"
Explanation: The expression evaluates to 1 * (2 + 3) * 4 = 1 * 5 * 4 = 20.
```

**Example 3:**

```
Input: expression = "999+999"
Output: "(999+999)"
Explanation: The expression evaluates to 999 + 999 = 1998.
```

**Constraints**

- 3 <= expression.length <= 10
- expression consists of digits from '1' to '9' and '+'.
- expression starts and ends with digits.
- expression contains exactly one '+'.
- The original value of expression, and the value of expression after adding any pair of parentheses that meets the requirements fits within a signed 32-bit integer.

---

## 题目（中文翻译）

你得到一个下标从 0 开始的字符串 `expression`，其形式为 "`<num1>+<num2>`"，其中 `<num1>` 和 `<num2>` 为正整数。  
在 `+` 左侧插入左括号 `(`，在 `+` 右侧插入右括号 `)`，使得添加括号后的表达式仍是合法的数学表达式，并且其计算结果尽可能小。  
返回插入一对括号后的表达式字符串。如果有多种答案得到相同的最小值，返回任意一种即可。  

题目保证：原始表达式的值，以及在满足要求的任意位置插入括号后得到的值，都能放入有符号 32 位整数范围内。

---

### 示例

**示例 1**  
> **输入**: `expression = "247+38"`  
> **输出**: `"2(47+38)"`  
> **解释**: 表达式的值为 `2 * (47 + 38) = 2 * 85 = 170`。  
> 注意 `"2(4)7+38"` 是非法的，因为右括号必须位于 `+` 的右侧。可以证明 170 是可能的最小值。

**示例 2**  
> **输入**: `expression = "12+34"`  
> **输出**: `"1(2+3)4"`  
> **解释**: 表达式的值为 `1 * (2 + 3) * 4 = 1 * 5 * 4 = 20`。

**示例 3**  
> **输入**: `expression = "999+999"`  
> **输出**: `"(999+999)"`  
> **解释**: 表达式的值为 `999 + 999 = 1998`。

---

### 约束条件

- `3 <= expression.length <= 10`
- `expression` 仅由字符 `'1'` 到 `'9'` 和 `'+'` 组成
- `expression` 以数字开头并以数字结尾
- `expression` 恰好包含一个 `'+'`
- 原始表达式的值以及在满足要求的任意位置插入括号后得到的值，都能放入有符号 32 位整数范围内

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一个形如 `"num1+num2"` 的字符串，其中 `num1`、`num2` 均为正整数。我们需要在 `'+'` 左侧的某个位置插入左括号 `'('`，在 `'+'` 右侧的某个位置插入右括号 `')'`，使得整个表达式合法且求值最小。

**把表达式想象成**：

```
a b c + d e f
|---|   |---|
   num1   num2
```

- 左括号可以放在 `num1` 的 **任意数字前**（包括最左边），
- 右括号可以放在 `num2` 的 **任意数字后**（包括最右边）。

加入括号后，表达式的数学形式一定是：

```
A * (B + C) * D
```

- `A` 是左括号左边的所有连续数字（如果没有则视为 1），
- `B` 是左括号右边、`+` 左边的数字（一定非空），
- `C` 是 `+` 右边、右括号左边的数字（一定非空），
- `D` 是右括号右边的所有连续数字（如果没有则视为 1）。

因为字符串长度最多只有 10，**遍历所有可能的左、右括号位置**（即枚举 `i`、`j`），计算 `A*(B+C)*D` 的值，取最小的那一种即可。这就是最直接、最“笨”的办法。

- **数据结构**：只需要用字符串切片（`s[l:r]`）来得到子串，然后 `int()` 转成整数。  
  切片就像我们在纸上用剪刀把一段文字剪下来一样，快速且安全。

- **正确性**：我们穷举了所有合法的 `(i, j)` 组合，必然包含最优解；每一种组合都按照题目要求计算了真实的数值，所以取最小值必然得到答案。

- **时间/空间复杂度**：  
  - 长度记作 `n`（`n ≤ 10`），左括号有 `i` 种可能（`0 … pos-1`），右括号有 `j` 种可能（`pos+1 … n-1`），总共最多 `O(n²)` 次枚举。  
  - 每次枚举只做常数次切片和整数运算，时间仍是 `O(n²)`。  
  - 只用了几个临时字符串和整数，空间是 `O(1)`（不计输入本身）。

#### 代码（Python）

```python
def minResult(expression: str) -> str:
    # 找到唯一的 '+' 的下标
    plus = expression.index('+')
    n = len(expression)

    best_val = float('inf')
    best_expr = ""

    # i 表示左括号插入在 plus 左侧的下标（i 为左括号左边的长度）
    for i in range(0, plus):
        # 左侧乘数 A，如果左括号左边没有数字，用 1 代替
        left_mul = int(expression[:i]) if i > 0 else 1
        # B 是左括号右边、+ 左边的子串
        B = int(expression[i:plus])

        # j 表示右括号插入在 plus 右侧的下标（j 为右括号右边的结束位置）
        for j in range(plus + 1, n + 1):
            # C 是 + 右边、右括号左边的子串
            C = int(expression[plus + 1:j])
            # 右侧乘数 D，如果右括号右边没有数字，用 1 代替
            right_mul = int(expression[j:]) if j < n else 1

            # 计算当前组合的值：A * (B + C) * D
            cur_val = left_mul * (B + C) * right_mul

            if cur_val < best_val:
                best_val = cur_val
                # 重新拼装答案字符串
                # 注意：左括号放在 i 前，右括号放在 j 后
                best_expr = (
                    (expression[:i] if i > 0 else "")
                    + "("
                    + expression[i:j]
                    + ")"
                )
    return best_expr
```

**关键行中文注释**：

- `plus = expression.index('+')` # 找到唯一的加号位置  
- `for i in range(0, plus):` # 枚举左括号左侧可以放的所有位置  
- `left_mul = int(expression[:i]) if i > 0 else 1` # 左乘数 A，若为空则视为 1  
- `B = int(expression[i:plus])` # 左括号右边、加号左边的子串  
- `for j in range(plus + 1, n + 1):` # 枚举右括号右侧可以放的所有位置（包含最右端）  
- `C = int(expression[plus + 1:j])` # 加号右边、右括号左边的子串  
- `right_mul = int(expression[j:]) if j < n else 1` # 右乘数 D，若为空则视为 1  
- `cur_val = left_mul * (B + C) * right_mul` # 计算当前表达式的数值  

#### 复杂度

- **时间复杂度**：`O(n²)`，其中 `n` 为表达式长度（≤10）。  
  实际上最多只有 `9*9 = 81` 次计算，几乎可以忽略不计。  
- **空间复杂度**：`O(1)`，只用了常数个临时变量。

---

### 2. 最优解

#### 思路  

因为 `n ≤ 10`，暴力枚举已经是 **最优** 的时间复杂度（`O(n²)`）了。这里把 “最优解” 解释为 **从暴力思路出发，提炼出一般化的算法框架**，便于读者在更大规模的类似问题中迁移思路。

1. **瓶颈定位**  
   - 暴力解已经遍历了所有合法的 `(左括号位置, 右括号位置)`，没有多余的重复计算。  
   - 只要每次枚举的代价是 `O(1)`，整体复杂度已经是 `O(n²)`，对 `n ≤ 10` 完全足够。

2. **核心概念**  
   - **枚举 + 直接计算**：把问题抽象为“所有可能的切分点”，每一种切分点对应唯一的数学表达式 `A*(B+C)*D`。  
   - **默认乘数为 1**：当左/右乘数不存在时，用 1 替代，等价于不乘。这个技巧在处理“可选”乘数时非常常见，类似于在求积时把空集合看成乘法单位元。

3. **算法步骤**（可直接套用到更长的字符串）  
   - 找到 `'+'` 的位置 `p`。  
   - 双层循环：`i` 从 `0` 到 `p-1`（左括号左边结束位置），`j` 从 `p+1` 到 `n`（右括号右边结束位置）。  
   - 对每对 `(i, j)`，提取四段子串 `A, B, C, D`，转成整数，计算 `value = A * (B + C) * D`。  
   - 记录最小的 `value` 与对应的字符串形式。

4. **为何不需要 DP / 单调栈**  
   - 这里的搜索空间极小，且每一步的子问题（比如 `A`、`B`、`C`、`D`）之间没有重叠子结构可以复用，使用动态规划反而会增加额外的存储与代码复杂度。  
   - 所以最直接的枚举即为最优。

#### 代码（Python）

```python
def minResult(expression: str) -> str:
    plus = expression.index('+')
    n = len(expression)

    best_val = float('inf')
    best_expr = ""

    # 枚举左括号位置 i（左侧乘数 A 的结束位置）
    for i in range(0, plus):
        left = int(expression[:i]) if i > 0 else 1   # A
        B = int(expression[i:plus])                  # B

        # 枚举右括号位置 j（右侧乘数 D 的起始位置）
        for j in range(plus + 1, n + 1):
            C = int(expression[plus + 1:j])          # C
            right = int(expression[j:]) if j < n else 1   # D

            cur = left * (B + C) * right
            if cur < best_val:
                best_val = cur
                # 重新拼装答案，注意括号必须包住 + 两侧的数字
                best_expr = (
                    (expression[:i] if i > 0 else "")
                    + "("
                    + expression[i:j]
                    + ")"
                )
    return best_expr
```

> 这段代码与上面的“暴力解”在实现细节上几乎相同，因为在本题的约束下，两者的时间复杂度相同，已达到最优。

#### 复杂度

- **时间复杂度**：`O(n²)`，对任意长度 `n`（本题 ≤10）都是最好的可行复杂度。  
- **空间复杂度**：`O(1)`，只使用常数级别的额外空间。

---

## 心得

- **核心技巧**：**枚举切分点 + 乘法单位元 (1)**。把“在 + 两边插入括号”抽象为四段乘积 `A*(B+C)*D`，缺失的乘数用 `1` 填补，保证公式统一。
- **适用场景**：  
  1. 需要在固定运算符两侧插入括号或其它符号的最小/最大化问题（如 `"a*b+c*d"` 中插入括号）。  
  2. 需要枚举所有合法分割点并直接计算代价的字符串/数组题目（如 “最小化表达式值” 系列）。  
  3. “插入运算符” 使表达式值最小/最大（如 “Insert Operators” 变形）。
- **一句话总结解题钥匙**：**把所有可能的插入位置全部尝试，缺失的乘数视为 1，直接比较得到最小值**。

---

## 反思

- **第一反应**：看到只有一个 `'+'`，立刻想到把括号放在左、右两侧的不同位置，形成 `A*(B+C)*D` 的结构，于是想到枚举所有位置。
- **最容易踩的坑**：  
  - **忘记乘数为 1 的情况**：左括号最左、右括号最右时，`A` 或 `D` 可能为空，必须当作 `1` 处理，否则会报 `ValueError`。  
  - **下标越界**：右括号的结束位置 `j` 可以等于 `n`（表示右括号放在最末尾），切片时要用 `expression[j:]` 而不是 `expression[j]`。  
  - **字符串拼接错误**：答案必须在 `'+'` 两侧都被括号包住，不能出现类似 `"2(4)7+38"` 这种非法形式。
- **下次类似题的第一步**：先把问题抽象成“把原始序列切成若干段”，确定每段的数学意义（乘、加、乘），再判断是否可以直接枚举所有切分点或需要更高效的技巧（如前缀和、单调栈）。