# #507. 完全数 / Perfect Number

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/perfect-number/)

---

## 题目（英文原版）

**Description**

A perfect number is a positive integer that is equal to the sum of its positive divisors, excluding the number itself. A divisor of an integer x is an integer that can divide x evenly.
Given an integer n, return true if n is a perfect number, otherwise return false.

**Examples**

**Example 1:**

```
Input: num = 28
Output: true
Explanation: 28 = 1 + 2 + 4 + 7 + 14
1, 2, 4, 7, and 14 are all divisors of 28.
```

**Example 2:**

```
Input: num = 7
Output: false
```

**Constraints**

- 1 <= num <= 108

---

## 题目（中文翻译）

**描述**  
完全数（perfect number）是指一个正整数（positive integer），它等于其所有正因子（positive divisors）的和，且不包括它本身。整数 x 的因子（divisor）是能够整除 x 的整数。

给定一个整数 n，若 n 是完全数则返回 `true`，否则返回 `false`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1:**  
```
Input: num = 28
Output: true
```
**解释:** 28 = 1 + 2 + 4 + 7 + 14  
1、2、4、7、14 都是 28 的因子。

**示例 2:**  
```
Input: num = 7
Output: false
```

**约束条件:**  
- 1 ≤ num ≤ 10⁸   (10^8)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有小于 `n` 的正整数** 都拿去检查，看看它们能否整除 `n`。  
- 如果 `i` 能整除 `n`（`n % i == 0`），说明 `i` 是 `n` 的一个真因子（除去 `n 本身的因子）。  
- 把所有满足条件的 `i` 加起来，最后看和是否等于 `n`。

这里用到的数据结构只有一个 **整数变量**（用来累计因子之和），可以把它想象成「购物车」——每找到一个符合条件的因子，就往车里放一件商品，最后看购物车里的总价是否恰好等于 `n`。

这种做法一定能得到正确答案，因为它把 **所有可能的真因子** 都遍历了一遍，绝不会漏掉。

#### 代码（Python）

```python
def isPerfectNumber_bruteforce(num: int) -> bool:
    # 1. 特殊情况：1 不是完全数，因为它没有真因子（除自身外）
    if num == 1:
        return False

    total = 0                     # 用来累加所有真因子
    # 2. 从 1 遍历到 num-1，逐个检查是否是因子
    for i in range(1, num):
        if num % i == 0:          # i 能整除 num，说明 i 是真因子
            total += i            # 把 i 加到累计和里

    # 3. 累计和等于 num，说明是完全数
    return total == num
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  这里的 `O(n)` 表示「随着输入 `n` 的增大，程序的运行时间大约会线性增长」。因为我们要检查 `1 … n‑1` 共 `n‑1` 次。
- **空间复杂度：** `O(1)`  
  只用了常数个额外变量（`total`、`i`），不随 `n` 的大小改变而增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **遍历了所有 `n‑1` 个数**，但我们并不需要检查这么多。  
观察一个数的因子有配对的特性：如果 `i` 是 `n` 的因子，则 `n / i` 也是 `n` 的因子。  
例如 `28` 的因子 `2` 对应的配对因子是 `28 / 2 = 14`。  

因此，只要遍历到 `√n`（即 `n` 的平方根）即可找到所有因子对：

1. 从 `1` 到 `√n`（包括 `√n`）逐个检查是否整除 `n`。  
2. 若 `i` 能整除 `n`，则 **两个因子** `i` 与 `n // i` 都要加入累计和。  
3. 需要注意的是：  
   - `i` 本身已经是一个真因子，直接加入。  
   - `n // i` 也是真因子，但要排除 `n 本身`（即当 `i == 1` 时，`n // i == n`，不要加）。  
   - 当 `i * i == n`（即 `i` 正好是 `√n`）时，`i` 与 `n // i` 是同一个数，只应加一次。

这样只遍历到 `√n`，时间复杂度从 `O(n)` 降到 **`O(√n)`**，在 `n ≤ 10⁸` 的约束下非常快。

#### 代码（Python）

```python
import math

def isPerfectNumber(num: int) -> bool:
    # 1. 1 不是完全数（没有真因子）
    if num == 1:
        return False

    total = 1                     # 1 永远是真因子，先加进去
    limit = int(math.isqrt(num))  # sqrt(num) 的整数部分（Python 3.8+ 的写法）

    # 2. 从 2 遍历到 sqrt(num)，寻找因子对
    for i in range(2, limit + 1):
        if num % i == 0:          # i 能整除 num
            total += i            # 加上 i 本身
            other = num // i      # 配对因子
            if other != i:        # 防止 i 正好等于 sqrt(num) 时重复计数
                total += other    # 加上配对因子

    # 3. 累计和等于原数，说明是完全数
    return total == num
```

#### 复杂度

- **时间复杂度：** `O(√n)`  
  只遍历到 `√n`，比如 `n = 10⁸` 时，只检查到 `10⁴` 次，运行速度提升约 **100 倍**（因为 `√n` 远小于 `n`）。
- **空间复杂度：** `O(1)`  
  同样只用了常数个变量。

---

## 心得

- **核心技巧**：利用因子配对（`i` 与 `n // i`）只遍历到平方根，可大幅降低时间复杂度。  
- **适用的题型**：  
  1. 判断一个数是否为 **完全数**、**友好数**、**阿姆斯特朗数**（需要枚举因子或位数）  
  2. **求所有约数**、**约数的和**（如 LeetCode 1720 → `numberOfPairs` 之类的变形）  
  3. **判断是否为完全平方数**（同样只需要检查到 `√n`）  
- **一句话总结**：  
  *“因子成对出现，只检查到根号 n，既完整又高效。”*

## 反思

- **第一反应**：直接把所有小于 `n` 的数都遍历一遍求和。  
- **最容易踩的坑**：  
  - 忘记 **排除 `n 本身** 作为因子（否则会导致总和大于 `n`）。  
  - 当 `i * i == n` 时，配对因子和 `i` 是同一个，需要防止重复累加。  
  - `num = 1` 时没有真因子，必须单独返回 `False`。  
- **下次类似题的第一步**：  
  *“先想想因子是否有配对关系，能否只遍历到根号 n？”*