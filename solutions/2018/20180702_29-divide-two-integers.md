# #29. 两个整数相除 / Divide Two Integers

> 难度：中等 · 标签：Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/divide-two-integers/)

---

## 题目（英文原版）

**Description**

Given two integers dividend and divisor, divide two integers without using multiplication, division, and mod operator.
The integer division should truncate toward zero, which means losing its fractional part. For example, 8.345 would be truncated to 8, and -2.7335 would be truncated to -2.
Return the quotient after dividing dividend by divisor.
Note: Assume we are dealing with an environment that could only store integers within the 32-bit signed integer range: [−231, 231 − 1]. For this problem, if the quotient is strictly greater than 231 - 1, then return 231 - 1, and if the quotient is strictly less than -231, then return -231.

**Examples**

**Example 1:**

```
Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = 3.33333.. which is truncated to 3.
```

**Example 2:**

```
Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7/-3 = -2.33333.. which is truncated to -2.
```

**Constraints**

- -231 <= dividend, divisor <= 231 - 1
- divisor != 0

---

## 题目（中文翻译）

给定两个整数 **dividend**（被除数） 和 **divisor**（除数），在不使用乘法、除法和取模运算符（mod operator）的前提下实现整数相除。整数除法应向零方向截断，即去掉小数部分。例如，8.345 会被截断为 8，-2.7335 会被截断为 -2。返回 **dividend** 除以 **divisor** 的商（quotient）。

**注意**：假设运行环境只能存储 32 位有符号整数，范围为 \[−2^31, 2^31 − 1\]。如果计算得到的商严格大于 2^31 − 1，则返回 2^31 − 1；如果商严格小于 −2^31，则返回 −2^31。

### 示例

#### 示例 1
```
Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = 3.33333..，截断后得到 3。
```

#### 示例 2
```
Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7/-3 = -2.33333..，截断后得到 -2。
```

### 约束条件
- \-2^31 ≤ dividend, divisor ≤ 2^31 − 1
- divisor ≠ 0

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **被除数** (`dividend`) 一次一次减去 **除数** (`divisor`) ，每减一次计数器 `quotient` 加 1（或 -1，取决于符号），直到被除数的绝对值小于除数的绝对值为止。  

- **数据结构**：只需要几个整数变量（`dividend`, `divisor`, `quotient`），不需要额外的容器。可以把它想象成“把一块巧克力（被除数）一块块（除数的大小）分给小朋友”，每分完一块就记一个小票（计数器）。
- **正确性**：因为每次减去的都是除数的大小，减的次数恰好等于商的整数部分（向 0 截断），所以最后计数器的值就是我们要的答案。
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(|quotient|)**，也就是被除数除以除数的结果有多大，就要循环多少次。最坏情况下 `dividend = 2³¹‑1`、`divisor = 1`，循环次数接近 `2³¹`，这在实际运行中几乎不可接受。  
  - 空间复杂度是 **O(1)**，只用了常数个变量。

> **大白话**：  
> - `O(n)` 就像你要走 n 步路，每走一步都要花一点时间。这里的 n 是商的大小，商如果很大，你就要走很多很多步。  
> - `O(1)` 就是装东西的背包大小固定，不会随输入增大而变大。

#### 代码（Python）

```python
def divide_brute(dividend: int, divisor: int) -> int:
    # 处理溢出边界
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    # 特殊情况：除数为 1 或 -1 可以直接返回（避免循环太久）
    if divisor == 1:
        return min(max(dividend, INT_MIN), INT_MAX)
    if divisor == -1:
        # 注意 -INT_MIN 会超过 32 位整数范围，需要裁剪
        return min(max(-dividend, INT_MIN), INT_MAX)

    # 记录结果的符号，正数为 1，负数为 -1
    sign = 1 if (dividend >= 0) == (divisor >= 0) else -1

    # 使用绝对值进行运算，避免负数的减法混乱
    a = abs(dividend)
    b = abs(divisor)

    quotient = 0
    # 只要被除数还能减去除数，就继续
    while a >= b:
        a -= b               # 把除数从被除数中“减走”
        quotient += 1        # 计数器加一

    # 加上符号
    quotient = sign * quotient

    # 再次裁剪到 32 位范围
    return min(max(quotient, INT_MIN), INT_MAX)
```

#### 复杂度  

- **时间复杂度**：`O(|quotient|)` —— 需要减多少次除数，就要循环多少次。最坏情况下接近 `2³¹` 次，几乎不可接受。  
- **空间复杂度**：`O(1)` —— 只用了常数个整数变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **一次只减去一个除数**，如果除数很小（比如 1），循环次数会非常多。我们可以把“每次减去一个除数”升级为“每次减去 **多个** 除数”，类似 **“指数级”** 的减法。

核心想法：

1. **把除数不断左移（乘以 2）**，直到它的值超过被除数的绝对值。左移相当于 `除数 * 2、除数 * 4、除数 * 8 …`，这一步只用了位运算（`<<`），不涉及乘法。  
   - 类比：把一袋糖果（除数）先装进一个盒子里，再把盒子装进更大的盒子，直到装不下为止。每一次装的盒子都比上一次大一倍，速度非常快。

2. 当找到了最大的 “左移后仍不超过被除数” 的那一层后，就可以把这层对应的 **倍数** 加到答案里，同时把被除数减去这层对应的值。随后继续在剩余的被除数上重复上述过程（从最高位往低位遍历），这就是 **“二分”** 的思想。

3. 最后恢复符号并裁剪到 32 位整数范围。

**为什么只用位运算**：  
- `x << k` 等价于 `x * (2^k)`，但不使用 `*`，符合题目要求。  
- 同理，`x >> k` 等价于 `x // (2^k)`（整数除法），同样不违背限制。

**步骤细化**（伪代码）：

```
sign = (dividend > 0) == (divisor > 0) ? 1 : -1
a = abs(dividend)
b = abs(divisor)
quotient = 0

while a >= b:
    temp = b          # 当前可以减去的“倍数”
    multiple = 1      # 这一次对应的商的增量
    # 把 temp 左移，尽可能接近 a，但不能超过
    while a >= (temp << 1):
        temp <<= 1
        multiple <<= 1
    a -= temp          # 把这部分“扣掉”
    quotient += multiple
```

**关键点**：

- `temp << 1` 相当于 `temp * 2`，判断 `a >= temp*2` 确保下一次左移仍合法。  
- `multiple` 同步左移，记录这一次我们实际加了多少个除数（比如 `8`、`4`、`2`、`1`），最后累加到 `quotient`。  
- 循环结束时 `a < b`，剩余的 `a` 已经不足以再除一次，直接结束。

这样每一次外层 `while` 循环都把 `a` 减少了 **至少一半**（因为我们用了最大的 `2^k * b`），所以总的循环次数是 **O(log |quotient|)**，极大提升效率。

#### 代码（Python）

```python
def divide(dividend: int, divisor: int) -> int:
    """
    使用位运算实现除法，时间 O(log|quotient|)，空间 O(1)。
    """
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    # 处理特殊情况：除数为 1 或 -1
    if divisor == 1:
        return min(max(dividend, INT_MIN), INT_MAX)
    if divisor == -1:
        # -INT_MIN 会溢出，需要裁剪
        return min(max(-dividend, INT_MIN), INT_MAX)

    # 记录结果的符号
    sign = 1 if (dividend >= 0) == (divisor >= 0) else -1

    # 使用绝对值进行位运算
    a = abs(dividend)
    b = abs(divisor)

    quotient = 0

    # 主循环：只要被除数还不小于除数，就继续“找最高位”
    while a >= b:
        temp = b          # 当前可以减去的“倍数”（从 b 开始）
        multiple = 1      # 对应的商的增量

        # 将 temp 左移，使其尽可能接近 a（但不超过）
        # 相当于找最大的 2^k * b <= a
        while a >= (temp << 1):
            temp <<= 1          # temp *= 2
            multiple <<= 1      # multiple *= 2

        a -= temp                # 把这部分从被除数中扣掉
        quotient += multiple     # 商增加对应的倍数

    # 恢复符号
    quotient = quotient if sign > 0 else -quotient

    # 裁剪到 32 位有符号整数范围
    return min(max(quotient, INT_MIN), INT_MAX)
```

#### 复杂度  

- **时间复杂度**：`O(log |quotient|)` —— 每一次外层循环把剩余的被除数至少减半，类似二分查找的对数级别。对比暴力的 `O(|quotient|)`，快了很多。  
- **空间复杂度**：`O(1)` —— 只用了常数个整数变量，没有额外的数据结构。

---

## 心得

- **核心技巧**：**位移（左移）模拟乘以 2**，配合 **二分思想** 把除法转化为 “找最大 2 的幂次倍数” 的过程。  
- **适用的题型**：  
  1. **整数除法**（本题）  
  2. **乘法实现**（如 `multiply`，通过位移与加法实现）  
  3. **幂运算**（如 `pow(x, n)`，使用快速幂）  
- **一句话总结**：**把大块一次减掉，利用二进制的“倍增”特性把除法变成对数级别的减法**。

---

## 反思

- **第一反应**：直接用循环减法（暴力）实现，代码最直观，但会超时。  
- **最容易踩的坑**：  
  - **符号处理**：正负号必须在全部运算结束后统一加上，否则在取绝对值时会出现错误。  
  - **溢出边界**：`-2³¹` 的相反数在 32 位整数里没有对应正数，需要在返回前做裁剪。  
  - **左移时的越界**：`temp << 1` 可能产生超过 Python 整数范围的值（Python 整数是无限长的），但在逻辑上我们只要判断 `a >= temp << 1` 即可，实际不会导致错误，只是要注意不要无限左移导致死循环。  
- **下次思路**：一看到 “不能用乘除” 且涉及 **大数相除**，第一步就想到 **“利用二进制位移做指数级的减法”**（即“二分/倍增”），随后再处理符号与边界。