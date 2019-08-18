# #537. **复数乘法** / Complex Number Multiplication

> 难度：中等 · 标签：Math、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/complex-number-multiplication/)

---

## 题目（英文原版）

**Description**

A complex number can be represented as a string on the form "real+imaginaryi" where:
Given two complex numbers num1 and num2 as strings, return a string of the complex number that represents their multiplications.

**Examples**

**Example 1:**

```
Input: num1 = "1+1i", num2 = "1+1i"
Output: "0+2i"
Explanation: (1 + i) * (1 + i) = 1 + i2 + 2 * i = 2i, and you need convert it to the form of 0+2i.
```

**Example 2:**

```
Input: num1 = "1+-1i", num2 = "1+-1i"
Output: "0+-2i"
Explanation: (1 - i) * (1 - i) = 1 + i2 - 2 * i = -2i, and you need convert it to the form of 0+-2i.
```

**Constraints**

- num1 and num2 are valid complex numbers.

---

## 题目（中文翻译）

描述  
复数（complex number）可以用形如 `"real+imaginaryi"` 的字符串表示，其中 `real` 为实部，`imaginary` 为虚部。  
给定两个复数 `num1` 和 `num2`（均为字符串），返回它们相乘后的复数，同样以字符串形式表示。

示例  

**示例 1**  
输入: `num1 = "1+1i", num2 = "1+1i"`  
输出: `"0+2i"`  
解释: \((1 + i) \times (1 + i) = 1 + i^2 + 2i = 2i\)，需要将结果转换为 `0+2i` 的形式。

**示例 2**  
输入: `num1 = "1+-1i", num2 = "1+-1i"`  
输出: `"0+-2i"`  
解释: \((1 - i) \times (1 - i) = 1 + i^2 - 2i = -2i\)，需要将结果转换为 `0+-2i` 的形式。

约束条件  
- `num1` 和 `num2` 均为有效的复数字符串。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心是把形如 `"a+bi"` 的字符串拆解成实部 `a` 与虚部 `b`，然后按照复数乘法公式  

\[
(a+bi)\times(c+di)= (ac-bd) + (ad+bc)i
\]

计算出新的实部与虚部，再拼成 `"real+imaginaryi"` 的字符串返回。

- **拆解字符串**：可以把 `+` 当作分隔符，把后面的 `i` 去掉，剩下的就是实部和虚部。这里把 `+` 当作分割符有点像在字典里查词：键（`+`）把整个句子切成两段，左边是实部，右边是虚部（带 `i`）。
- **转换为整数**：拆出来的两个子串用 `int()` 转成整数，方便后面做算术运算。
- **复数乘法**：直接套用上面的公式，得到新的实部 `real = a*c - b*d` 与虚部 `imag = a*d + b*c`。
- **拼接结果**：把 `real`、`imag` 和字符 `i` 按照题目要求的格式拼起来，得到最终的字符串。

这个思路看起来最直接、最“笨”，因为我们几乎没有做任何优化，只是一步步把文字变成数字、算出答案、再变回文字。

#### 代码（Python）

```python
def complexNumberMultiply(num1: str, num2: str) -> str:
    # ---------- 把 "a+bi" 拆成 a 和 b ----------
    # 先把末尾的 'i' 去掉
    num1 = num1.rstrip('i')
    num2 = num2.rstrip('i')
    # 再用 '+' 分割，得到实部和虚部的字符串
    a_str, b_str = num1.split('+')
    c_str, d_str = num2.split('+')
    # 把字符串转成整数，准备计算
    a, b = int(a_str), int(b_str)
    c, d = int(c_str), int(d_str)

    # ---------- 复数乘法 ----------
    real = a * c - b * d          # 实部：ac - bd
    imag = a * d + b * c          # 虚部：ad + bc

    # ---------- 拼接成目标格式 ----------
    return f"{real}+{imag}i"
```

> **代码要点**  
> - `rstrip('i')` 类似把单词 “apple” 里的字母 “e” 删掉，只保留核心部分。  
> - `split('+')` 把字符串在 `+` 这根“刀”处切开，得到两段。  
> - `f"{real}+{imag}i"` 用 f‑string 把数值直接嵌入到指定的文字模板里。

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做了常数次的字符串切割、整数转换和四次乘法、两次加法、一次减法。无论输入多长（题目保证是合法的复数），操作次数都不变。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量和短暂的字符串切片，额外占用的内存不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解来看，真正的“慢点”其实并不存在——所有操作都是常数时间的。  
但如果把“暴力”定义为**先把字符串完整解析成 `complex` 对象、再利用 Python 自带的复数运算**，那就会产生额外的对象创建与内部实现开销。我们可以直接**手写公式**，省去不必要的中间步骤，这就是“最优解”。  

优化步骤：

1. **一次性解析**：一次性把两个复数的实部、虚部都提取出来，避免多次切割。  
2. **直接套公式**：使用 `ac - bd` 与 `ad + bc` 计算，避免使用 Python 的 `complex` 类型（内部实现会有额外的浮点数转换）。  
3. **一次拼接**：直接用 f‑string 把结果拼好返回。

核心算法仍是 **复数乘法的代数公式**，这里不涉及动态规划、双指针等高级技巧，只是对数学公式的直接实现。下面用 **“配对乘法”** 的类比来帮助理解：想象有两对数 `(a, b)` 与 `(c, d)`，我们把它们分别放进两列，按列相乘再做加减，得到最终的配对结果。

#### 代码（Python）

```python
def complexNumberMultiply(num1: str, num2: str) -> str:
    # ---------- 同时解析两个复数 ----------
    # "a+bi" -> a, b   "c+di" -> c, d
    a, b = map(int, num1[:-1].split('+'))   # 去掉末尾的 'i' 再分割
    c, d = map(int, num2[:-1].split('+'))

    # ---------- 直接套公式 ----------
    real = a * c - b * d          # 实部
    imag = a * d + b * c          # 虚部

    # ---------- 返回结果 ----------
    return f"{real}+{imag}i"
```

> **代码要点**  
> - `num1[:-1]` 用切片一次性去掉最后的 `'i'`，比 `rstrip` 更直观。  
> - `map(int, ...)` 把分割得到的两个字符串一次性转成整数，省去手动 `int()` 两次的代码。  
> - 其余步骤与暴力解相同，只是写法更简洁、常数因子更小。

#### 复杂度

- **时间复杂度**：`O(1)` —— 仍然是常数次的字符串切割、整数转换和四次乘法。相比暴力解省去了额外的对象创建，实际运行更快。  
- **空间复杂度**：`O(1)` —— 只用了四个整数变量，额外空间不随输入增长。

---

## 心得

- **核心技巧**：把复数的字符串表示拆解为整数，利用复数乘法公式 `ac - bd` 与 `ad + bc` 直接求解。  
- **适用的题型**：  
  1. **字符串 + 数学**：如 “字符串转整数并做运算” (`String to Integer (atoi)`)。  
  2. **数值公式直接实现**：如 “两个分数相乘/相除” (`Fraction Multiplication`)。  
  3. **自定义数结构运算**：如 “矩阵乘法的字符串版”。  
- **一句话总结解题钥匙**：**先把字符拆成数字，再把数学公式写进代码**。

---

## 反思

- **第一反应**：看到 `"a+bi"` 这种形式，第一时间会想到把 `+` 当作分隔符，把 `i` 去掉，然后把剩下的两段转成整数。  
- **最容易踩的坑**：  
  - 忘记去掉末尾的 `'i'`，导致 `int('3i')` 报错。  
  - 负号的处理不当，例如 `"1+-1i"` 中的 `+` 与 `-` 连在一起，需要确保 `split('+')` 能得到 `'-1'`（Python 的 `split` 正好可以做到）。  
  - 结果拼接时忘记在虚部后面加 `'i'`。  
- **下次类似题的第一步**：**先把输入的“特殊格式”统一转成最容易操作的数值（整数或浮点数）**，再把数学公式写出来。这样可以把“字符串处理”和“数值运算”这两块任务清晰分离，避免混乱。