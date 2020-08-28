# #972. 等价有理数 / Equal Rational Numbers

> 难度：困难 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/equal-rational-numbers/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, each of which represents a non-negative rational number, return true if and only if they represent the same number. The strings may use parentheses to denote the repeating part of the rational number.
A rational number can be represented using up to three parts: <IntegerPart>, <NonRepeatingPart>, and a <RepeatingPart>. The number will be represented in one of the following three ways:
The repeating portion of a decimal expansion is conventionally denoted within a pair of round brackets. For example:

**Examples**

**Example 1:**

```
Input: s = "0.(52)", t = "0.5(25)"
Output: true
Explanation: Because "0.(52)" represents 0.52525252..., and "0.5(25)" represents 0.52525252525..... , the strings represent the same number.
```

**Example 2:**

```
Input: s = "0.1666(6)", t = "0.166(66)"
Output: true
```

**Example 3:**

```
Input: s = "0.9(9)", t = "1."
Output: true
Explanation: "0.9(9)" represents 0.999999999... repeated forever, which equals 1.  [See this link for an explanation.]
"1." represents the number 1, which is formed correctly: (IntegerPart) = "1" and (NonRepeatingPart) = "".
```

**Constraints**

- Each part consists only of digits.
- The <IntegerPart> does not have leading zeros (except for the zero itself).
- 1 <= <IntegerPart>.length <= 4
- 0 <= <NonRepeatingPart>.length <= 4
- 1 <= <RepeatingPart>.length <= 4

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，它们分别表示一个非负有理数（non-negative rational number），如果且仅如果这两个字符串表示的是同一个数，则返回 `true`。字符串可以使用圆括号来标记有理数的小数部分的循环段（RepeatingPart）。

一个有理数（rational number）可以由最多三个部分组成：**整数部分（IntegerPart）**、**非循环部分（NonRepeatingPart）** 和 **循环部分（RepeatingPart）**。该数的表示方式必定属于以下三种之一：

- `<IntegerPart>`
- `<IntegerPart>.<NonRepeatingPart>`
- `<IntegerPart>.<NonRepeatingPart>(<RepeatingPart>)`

小数展开式中的循环段通常用一对圆括号括起。例如：

*（示例略）*

## 约束条件

- 每个部分仅由数字组成。
- `<IntegerPart>` 不含前导零（零本身例外）。
- `1 <= <IntegerPart>.length <= 4`
- `0 <= <NonRepeatingPart>.length <= 4`
- `1 <= <RepeatingPart>.length <= 4`

## 示例

### 示例 1
**输入:**  
`s = "0.(52)", t = "0.5(25)"`  

**输出:**  
`true`  

**解释:**  
`"0.(52)"` 表示 `0.52525252…`，而 `"0.5(25)"` 表示 `0.52525252525…`，两者表示相同的数。

### 示例 2
**输入:**  
`s = "0.1666(6)", t = "0.166(66)"`  

**输出:**  
`true`  

### 示例 3
**输入:**  
`s = "0.9(9)", t = "1."`  

**输出:**  
`true`  

**解释:**  
`"0.9(9)"` 表示 `0.999999999…`（无限循环），等于 `1`。  
`"1."` 表示数字 `1`，其组成正确：`(IntegerPart) = "1"` 且 `(NonRepeatingPart) = ""`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把两个小数都**展开成普通的十进制字符串**，然后直接比较这两个字符串是否相同。  
展开的步骤可以这么想：

1. 先把整数部分和小数点前的非循环部分写出来（就像写在纸上的普通小数）。  
2. 如果有“()”括起来的循环部分，就把它不断重复，直到得到足够长的字符串。  
3. 为了避免无限循环，我们只需要把循环部分重复 **若干次**（比如 20~30 位），因为题目中每段最多只有 4 位，最多的循环周期是 `10⁴‑1 = 9999`，只要展开到 20 位就已经可以把两数的差距显现出来了。  
4. 把得到的两段字符串去掉多余的尾随 `0`（如 `0.5000` → `0.5`）和尾随 `9`（如 `0.999…` → `1`），再直接比较是否相等。

> **类比**：把“(52)”看成一本书的章节，需要一直翻下去才能看到完整内容。暴力解相当于把这本书的前几页都抄下来，然后比较两本书的前几页是否一模一样。

**为什么这个方法正确？**  
因为如果两个有理数相等，它们的无限小数展开必然在任意长度的前缀上都相同。只要我们展开的长度足够大（大于循环节的最小公倍数），就能捕捉到所有可能的不同点。  

**时间/空间复杂度**  
- **时间**：我们把每个字符串最多展开 `O(L)` 位（这里的 `L` 取一个常数，比如 30），所以整体是 **O(L)**，在本题的约束下可以视作 **O(1)**。  
- **空间**：需要存放展开后的两个字符串，同样是 **O(L)**（常数级别）。  

#### 代码（Python）

```python
import math

def expand(num: str, max_len: int = 30) -> str:
    """
    把 s 形式的有理数展开成普通十进制字符串，长度不超过 max_len
    """
    # 1️⃣ 找整数部分、非循环部分、循环部分
    if '(' in num:                     # 有循环节
        left, repeat = num.split('(')
        repeat = repeat.rstrip(')')    # 去掉右括号
    else:
        left, repeat = num, ''         # 没有循环节

    if '.' in left:                    # 有小数点
        integer, non_repeat = left.split('.')
    else:                               # 整数
        integer, non_repeat = left, ''

    # 2️⃣ 先把整数部分和非循环部分写出来
    res = integer + '.' + non_repeat

    # 3️⃣ 把循环节不断重复，直到达到 max_len 位
    while len(res) - len(integer) - 1 < max_len:   # 已经写了多少位小数
        if not repeat:               # 没有循环节，直接结束
            break
        res += repeat                # 再加一轮循环节

    # 4️⃣ 截断到 max_len 位小数（不够也行）
    if '.' in res:
        integer_part, fraction_part = res.split('.')
        fraction_part = fraction_part[:max_len]
        res = integer_part + '.' + fraction_part
    else:
        res = res[:max_len]

    # 5️⃣ 去掉无意义的尾随 0 / 9（0.5000 → 0.5，0.999 → 1）
    #    这里用一个小技巧：如果小数点后全是 9，就进位到整数部分
    if '.' in res:
        int_part, frac = res.split('.')
        # 去掉尾随 0
        frac = frac.rstrip('0')
        # 去掉尾随 9 并进位
        if set(frac) == {'9'} or (frac and frac[-1] == '9' and set(frac[-1:]) == {'9'}):
            # 全部是 9，整体进位
            if frac == '' or set(frac) == {'9'}:
                int_part = str(int(int_part) + 1)
                frac = ''
        # 合成最终结果
        res = int_part if frac == '' else int_part + '.' + frac
    return res


def isEqual(s: str, t: str) -> bool:
    """
    暴力解：把两数展开成普通十进制，再比较
    """
    return expand(s) == expand(t)


# ---- 简单测试 ----
print(isEqual("0.(52)", "0.5(25)"))   # True
print(isEqual("0.1666(6)", "0.166(66)"))  # True
print(isEqual("0.9(9)", "1."))       # True
```

#### 复杂度  

- **时间复杂度**：`O(L)`，`L` 为我们展开的最大位数（常数 30），所以可以看作 **O(1)**。  
- **空间复杂度**：`O(L)`，存放展开后的两个字符串，同样是常数级别。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于“把无限循环的十进制写出来”。虽然对本题的限制够用，但在**更大的输入**或**更严格的时间要求**下，这种“写字”方式并不高效。  

要从根本上比较两个有理数，我们可以把它们**转换成最简分数**（分子 / 分母），然后只比较两个分数是否相等。  

**关键点**：

1. **把小数拆成三部分**  
   - 整数部分 `I`  
   - 非循环小数部分 `N`（可能为空）  
   - 循环小数部分 `R`（可能为空）  

2. **利用数学公式**把这三部分直接写成分数。  

   - **没有循环节** (`R` 为空)  
     \[
     value = I + \frac{N}{10^{|N|}}
     \]
     分母是 `10^{len(N)}`，分子是 `I * den + int(N)`。

   - **有循环节** (`R` 非空)  
     把 `N` 与 `R` 拼在一起得到整数 `a = int(N+R)`，把仅 `N` 的整数部分记为 `b = int(N)`（若 `N` 为空则 `b=0`）。  
     循环小数的值等于  
     \[
     \frac{a-b}{10^{|N|}\bigl(10^{|R|}-1\bigr)}
     \]
     整体分数为  
     \[
     \frac{I \times den + (a-b)}{den},
     \qquad
     den = 10^{|N|}\bigl(10^{|R|}-1\bigr)
     \]

3. **约分**  
   用 **最大公约数（gcd）** 把分子、分母同时除以 `gcd(num, den)`，得到最简分数。

4. **比较**  
   两个数相等当且仅当它们的最简分子相同且分母相同。

> **类比**：把“无限循环的小数”想象成一杯混合饮料，整数部分是已经倒好的水，非循环部分是加进去的糖，循环部分是不断往里倒的糖粉。我们只要把所有成分的比例算清楚（分数），再把比例化简，就能直接判断两杯饮料是否完全相同，而不必一直倒下去看它们的味道。

**为什么最优解正确？**  
数学上，任意有理数都有唯一的最简分数表示。我们用的公式正是把给定的循环小数精确转化为分数的推导过程，所以得到的最简分数必然相同当且仅当原始小数相等。

**时间/空间复杂度**  

- **时间**：只遍历一次字符串，做常数次整数运算，时间是 **O(L)**（`L` 为字符串长度），在本题最多 12 位，几乎是 **O(1)**。  
- **空间**：只保存几个整数和短字符串，空间是 **O(1)**。

#### 代码（Python）

```python
import math
from typing import Tuple

def to_fraction(s: str) -> Tuple[int, int]:
    """
    把形如 "123.45(67)" 的有理数转成最简分数 (numerator, denominator)
    """
    # ---------- 1️⃣ 拆分三部分 ----------
    # 先找循环节
    if '(' in s:
        left, repeat = s.split('(')
        repeat = repeat.rstrip(')')          # 循环部分
    else:
        left, repeat = s, ''                # 没有循环节

    # 再找小数点
    if '.' in left:
        integer, non_repeat = left.split('.')
    else:
        integer, non_repeat = left, ''      # 整数

    # ---------- 2️⃣ 转成分数 ----------
    I = int(integer)                         # 整数部分
    N = non_repeat                           # 非循环部分字符串
    R = repeat                               # 循环部分字符串

    lenN = len(N)
    lenR = len(R)

    if lenR == 0:                            # 没有循环节
        den = 10 ** lenN
        num = I * den + (int(N) if N else 0)
    else:                                    # 有循环节
        # a = int(N+R) , b = int(N)
        a = int(N + R) if (N + R) else 0
        b = int(N) if N else 0
        den = (10 ** lenN) * (10 ** lenR - 1)
        num = I * den + (a - b)

    # ---------- 3️⃣ 约分 ----------
    g = math.gcd(num, den)
    num //= g
    den //= g
    return num, den


def isEqual(s: str, t: str) -> bool:
    """最优解：把两数化为最简分数后直接比较"""
    return to_fraction(s) == to_fraction(t)


# ---- 简单测试 ----
print(isEqual("0.(52)", "0.5(25)"))   # True
print(isEqual("0.1666(6)", "0.166(66)"))  # True
print(isEqual("0.9(9)", "1."))       # True
```

#### 复杂度  

- **时间复杂度**：`O(L)`，只遍历一次输入字符串并做常数次整数运算。  
- **空间复杂度**：`O(1)`，只使用了若干整数变量和极短的子串。  

---

## 心得  

- **核心技巧**：把带循环小数的有理数转化为**最简分数**（分子/分母），利用**最大公约数**约分后直接比较。  
- **适用的题型**（类似技巧）  
  1. “判断两个有理数是否相等” 类似题目，如 LeetCode *Fraction Addition and Subtraction*。  
  2. “把循环小数转成分数” 的数学题。  
  3. “比较两个分数大小” 的整数运算题。  
- **一句话总结解题钥匙**：**把无限循环的十进制“压缩”成唯一的最简分数，再比较分子和分母是否相同**。  

---

## 反思  

- **第一反应**：看到“()”表示循环，第一想法是直接把循环部分展开成很多位再比较——这就是暴力解。  
- **最容易踩的坑**  
  - **尾随 9 的进位**：`0.9(9)` 实际等于 `1`，如果只看展开的字符串会误判。  
  - **空的非循环或循环部分**：如 `"1."`、`"0.(0)"` 必须正确处理空字符串对应的整数 `0`。  
  - **整数部分可能没有小数点**：如 `"123"` 也属于合法输入。  
- **下次遇到同类题**，第一步应该先**把输入拆成整数、非循环、小循环三块**，然后**用数学公式直接求分数**，而不是盲目展开。这样既严谨又高效。