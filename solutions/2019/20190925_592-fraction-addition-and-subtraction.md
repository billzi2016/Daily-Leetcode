# #592. **分数加减** / Fraction Addition and Subtraction

> 难度：中等 · 标签：Math、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/fraction-addition-and-subtraction/)

---

## 题目（英文原版）

**Description**

Given a string expression representing an expression of fraction addition and subtraction, return the calculation result in string format.
The final result should be an irreducible fraction. If your final result is an integer, change it to the format of a fraction that has a denominator 1. So in this case, 2 should be converted to 2/1.

**Examples**

**Example 1:**

```
Input: expression = "-1/2+1/2"
Output: "0/1"
```

**Example 2:**

```
Input: expression = "-1/2+1/2+1/3"
Output: "1/3"
```

**Example 3:**

```
Input: expression = "1/3-1/2"
Output: "-1/6"
```

**Constraints**

- The input string only contains '0' to '9', '/', '+' and '-'. So does the output.
- Each fraction (input and output) has the format ±numerator/denominator. If the first input fraction or the output is positive, then '+' will be omitted.
- The input only contains valid irreducible fractions, where the numerator and denominator of each fraction will always be in the range [1, 10]. If the denominator is 1, it means this fraction is actually an integer in a fraction format defined above.
- The number of given fractions will be in the range [1, 10].
- The numerator and denominator of the final result are guaranteed to be valid and in the range of 32-bit int.

---

## 题目（中文翻译）

给定一个字符串 `expression`，它表示分数的加法和减法表达式，返回计算结果的字符串形式。  
最终结果必须是既约分数 (irreducible fraction)。如果结果是整数，需要将其写成分母为 1 的分数形式，例如 `2` 要转换为 `2/1`。

**示例 1**  
**示例 2**  
**示例 3**

### 示例

**示例 1**  
Input: `expression = "-1/2+1/2"`  
Output: `"0/1"`

**示例 2**  
Input: `expression = "-1/2+1/2+1/3"`  
Output: `"1/3"`

**示例 3**  
Input: `expression = "1/3-1/2"`  
Output: `"-1/6"`

### 约束条件

- 输入字符串仅包含字符 `'0'` 到 `'9'`、`'/'`、`'+'` 与 `'-'`，输出同理。
- 每个分数（输入和输出）均采用 `±numerator/denominator` 的格式。如果首个输入分数或输出为正数，则省略 `'+'` 符号。
- 输入仅包含合法的既约分数 (irreducible fraction)，其中每个分数的分子和分母均在区间 `[1, 10]` 内。若分母为 `1`，则该分数实际上是整数，但仍按上述分数格式表示。
- 给定的分数个数在区间 `[1, 10]` 内。
- 最终结果的分子和分母保证在 32 位整数范围内且合法。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把表达式里所有分数都 **通分**（把它们的分母变成同一个数），然后把分子相加/相减，最后约掉最大公约数得到最简分数。  

- **把所有分母乘起来**：如果有 `a/b + c/d`，我们把分母变成 `b*d`，于是  
  `a/b = a*d / (b*d)`，`c/d = c*b / (b*d)`。  
- **把所有分子累加**：把所有改写后的分子相加（注意正负号），得到一个总分子 `sum_num`，总分母就是所有分母的乘积 `prod_den`。  
- **约分**：用欧几里得算法算出 `gcd(|sum_num|, prod_den)`，然后把分子、分母同时除以这个最大公约数，得到不可约分数。  

> **类比**：把分母乘起来就像把几本不同厚度的书放在一起装订，必须把每本书的页码（分子）都扩展到同样的厚度（相同的分母）才能直接相加。  

这个方法必然能得到正确答案，因为我们把所有分数都写成了等价的“同分母”形式，数学上加减同分母的分数一定等价于原式的运算结果。  

**为什么会慢**  
- 每出现一个新分数，就要把所有已有的分母再次相乘，导致分母指数级增长。  
- 最终分子、分母可能非常大，约分时的欧几里得算法会耗费不少时间。  

#### 代码（Python）

```python
import math

def fractionAddition_bruteforce(expression: str) -> str:
    # 1. 把表达式切成若干个 "符号 + 分子/分母" 的块
    #    这里在每个 '+'、'-' 前面都补上一个标记，方便 split
    #    例如 "-1/2+1/3" -> ["-1/2", "+1/3"]
    tokens = []
    i = 0
    while i < len(expression):
        # 读取符号
        sign = 1
        if expression[i] == '-':
            sign = -1
            i += 1
        elif expression[i] == '+':
            sign = 1
            i += 1
        # 读取分子
        num = 0
        while i < len(expression) and expression[i].isdigit():
            num = num * 10 + int(expression[i])
            i += 1
        num *= sign                      # 加上正负号
        i += 1                           # 跳过 '/' 
        # 读取分母
        den = 0
        while i < len(expression) and expression[i].isdigit():
            den = den * 10 + int(expression[i])
            i += 1
        tokens.append((num, den))        # 保存为 (分子, 分母) 的元组

    # 2. 暴力通分：所有分母直接相乘
    prod_den = 1
    for _, d in tokens:
        prod_den *= d                     # 这里会把分母指数级扩大

    # 3. 把每个分数的分子扩展到同一个分母后相加
    sum_num = 0
    for n, d in tokens:
        sum_num += n * (prod_den // d)   # n/d = n*(prod_den/d) / prod_den

    # 4. 约分
    g = math.gcd(abs(sum_num), prod_den)
    sum_num //= g
    prod_den //= g

    return f"{sum_num}/{prod_den}"
```

#### 复杂度  

- **时间复杂度**：`O(k + n)`，其中 `n` 为分数个数（最多 10），`k` 为表达式长度。  
  但因为我们把所有分母相乘，实际数值会变得非常大，欧几里得求 `gcd` 的次数会随位数增长，等价于 **指数级**（在最坏情况下接近 `O(2^n)`），所以整体上可以说是 **非常慢**。  
- **空间复杂度**：`O(1)`（只用常数个整数），但这些整数的位数可能会非常大，实际占用的内存随分母乘积的大小指数增长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都把所有分母乘起来，导致中间结果爆炸。  
其实我们不需要一次性把所有分母合在一起，只要 **两两相加**，并在每一步都把结果约到最简，就能把数值控制在合理范围。  

**关键点**  

1. **两数相加的通分公式**  
   对于 `a/b` 与 `c/d`（`b, d > 0`），  
   - 先算出 **最小公倍数**（LCM）`l = lcm(b, d) = b // gcd(b, d) * d`。  
   - 把两个分数都扩展到分母 `l`：  
     `a/b = a * (l / b) / l`，`c/d = c * (l / d) / l`。  
   - 相加得到新分子 `new_num = a * (l // b) + c * (l // d)`，新分母就是 `l`。  
   - 最后用 `gcd(|new_num|, l)` 把它们约掉，得到 **最简** 的中间结果。  

   这样做的好处是：  
   - 每一步只涉及两个分母的 LCM，而不是所有分母的乘积。  
   - 约分后，分子、分母的大小被限制在 `O(max_num * max_den)` 的范围内，防止爆炸。  

2. **遍历表达式，逐个累加**  
   - 先把表达式解析成 `(num, den)` 的列表（同上，只是把符号直接算进 `num`）。  
   - 初始化累计结果 `cur_num = 0, cur_den = 1`（相当于 0/1）。  
   - 对每个分数 `(n, d)`，用上面的两数相加公式把它加入累计结果。  

3. **欧几里得算法（gcd）**  
   - 用 `math.gcd`（或手写递归）求最大公约数。  
   - `gcd` 的时间复杂度是 `O(log max(a, b))`，非常快。  

**类比**：把每次加法想象成把两块拼图合在一起，然后把多余的边缘（公约数）裁掉，保持拼图的尺寸尽可能小，这样后面的拼图就不需要处理巨大的尺寸了。  

#### 代码（Python）

```python
import math
from typing import List, Tuple

def fractionAddition(expression: str) -> str:
    """
    逐个解析并累加分数，始终保持结果为最简分数。
    """
    # ---------- 1. 解析表达式 ----------
    fractions: List[Tuple[int, int]] = []   # (numerator, denominator)
    i = 0
    n = len(expression)
    while i < n:
        # 读取符号（如果没有显式的 +，默认是正号）
        sign = 1
        if expression[i] == '+':
            i += 1
        elif expression[i] == '-':
            sign = -1
            i += 1

        # 读取分子
        num = 0
        while i < n and expression[i].isdigit():
            num = num * 10 + int(expression[i])
            i += 1
        num *= sign                # 加上正负号

        i += 1                     # 跳过 '/' 

        # 读取分母
        den = 0
        while i < n and expression[i].isdigit():
            den = den * 10 + int(expression[i])
            i += 1

        fractions.append((num, den))

    # ---------- 2. 逐个累加 ----------
    cur_num, cur_den = 0, 1        # 初始为 0/1

    for n, d in fractions:
        # 计算当前累计分数与新分数的最小公倍数（LCM）
        g = math.gcd(cur_den, d)          # 先算出两个分母的 gcd
        lcm = cur_den // g * d             # lcm = a/gcd * b，防止直接相乘溢出

        # 把两个分数都扩展到相同的分母 lcm
        # 注意：乘法先做除法可以避免中间数过大
        cur_num = cur_num * (lcm // cur_den) + n * (lcm // d)
        cur_den = lcm

        # 约分，使结果保持最简
        g2 = math.gcd(abs(cur_num), cur_den)
        cur_num //= g2
        cur_den //= g2

    return f"{cur_num}/{cur_den}"
```

#### 复杂度  

- **时间复杂度**：`O(k * log M)`  
  - `k` 为分数的个数（最多 10），每次相加需要一次 `gcd`（时间 `O(log M)`，`M` 为当前分子或分母的大小）。  
  - 因为我们每一步都约分，`M` 不会爆炸，整体仍然是 **线性**（相对于分数个数）且非常快。  
- **空间复杂度**：`O(1)`（只用常数个整数来保存累计结果），不随输入规模增长。  

---

## 心得  

- **核心技巧**：**两数相加时使用最小公倍数（LCM）并即时约分**。  
- **适用的题型**：  
  1. **分数加减**（如本题、LeetCode 726 `Number of Atoms` 中的分子计数）。  
  2. **有理数运算**（如“有理数加法”“有理数乘法”）。  
  3. **涉及比例合并的场景**（如“最小公倍数化简”类的数学题）。  
- **一句话总结**：**把每一次加法都先对齐分母、再约分，避免中间数爆炸。**  

---

## 反思  

- **第一反应**：看到“+ / -”和“/”，立刻想到把所有分母乘起来再相加——这是最自然的“通分”思路。  
- **最容易踩的坑**  
  - **符号处理**：表达式可能以 `-` 开头，或者连续出现 `+`、`-`，要把符号正确合并进分子。  
  - **约分遗漏**：如果不在每一步约分，分子/分母会快速膨胀，导致整数溢出或运行慢。  
  - **零分子**：累计结果可能出现 `0`，此时分母应当保持 `1`（返回 `0/1`）。  
- **下次类似题的第一步**：**先把每个分数解析为 (带符号的分子, 正整数分母) 的元组**，然后**用 LCM+即时约分的方式两两合并**，而不是一次性把所有分母相乘。