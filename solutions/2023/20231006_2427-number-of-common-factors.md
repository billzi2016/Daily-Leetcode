# #2427. 公共因数的个数 / Number of Common Factors

> 难度：简单 · 标签：Math、Enumeration、Number Theory · [LeetCode 链接](https://leetcode.com/problems/number-of-common-factors/)

---

## 题目（英文原版）

**Description**

Given two positive integers a and b, return the number of common factors of a and b.
An integer x is a common factor of a and b if x divides both a and b.

**Examples**

**Example 1:**

```
Input: a = 12, b = 6
Output: 4
Explanation: The common factors of 12 and 6 are 1, 2, 3, 6.
```

**Example 2:**

```
Input: a = 25, b = 30
Output: 2
Explanation: The common factors of 25 and 30 are 1, 5.
```

**Constraints**

- 1 <= a, b <= 1000

---

## 题目（中文翻译）

**描述**  
给定两个正整数（positive integer）`a` 和 `b`，返回它们的公共因数（common factor）的数量。  
如果整数 `x` 能同时整除 `a` 和 `b`，则 `x` 是 `a` 和 `b` 的公共因数。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**

**示例 1**  
```
Input: a = 12, b = 6
Output: 4
Explanation: 12 和 6 的公共因数是 1、2、3、6。
```

**示例 2**  
```
Input: a = 25, b = 30
Output: 2
Explanation: 25 和 30 的公共因数是 1、5。
```

**约束条件**  
- 1 ≤ a, b ≤ 1000

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的因子** 都枚举一遍，然后检查它是否能同时整除 `a` 和 `b`。  
- **枚举范围**：因子一定不会大于两个数中较小的那个（因为比它大的数不可能整除它），所以我们只需要遍历 `1 … min(a, b)`。  
- **数据结构**：这里不需要额外的数据结构，只用一个普通的 `for` 循环和计数器 `cnt`。  
- **生活化类比**：想象你有两本书的章节目录，想找出它们都有的章节编号。最笨的办法就是把 **1 到最小章节数** 逐个翻看，看看每个章节号是否在两本书里都出现过。

只要遍历完所有可能的数字，计数器的值就是公共因子的个数。

#### 代码（Python）

```python
def common_factors_bruteforce(a: int, b: int) -> int:
    """
    暴力枚举 1~min(a,b) 的每个整数，统计同时能整除 a 与 b 的个数
    """
    limit = min(a, b)          # 只需要检查到较小的那个数
    cnt = 0                    # 计数器，记录公共因子的数量
    for x in range(1, limit + 1):
        # 如果 x 同时整除 a 和 b，就说明它是公共因子
        if a % x == 0 and b % x == 0:
            cnt += 1           # 计数器加一
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(min(a, b))`  
  - 这里的 “O” 代表“数量级”。如果 `a`、`b` 最大都是 1000，那么最坏情况下循环 1000 次，时间大约是 **线性** 随着输入增大而增长。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`limit`、`cnt`、`x`），不随输入规模变化，算作常数空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历 1 … min(a, b)**，即使大多数数字根本不可能是公共因子。  
我们可以利用数论中的一个重要定理：

> 两个整数的 **公共因子** 必然是它们 **最大公约数（GCD）** 的因子。

**为什么？**  
设 `d` 同时整除 `a` 和 `b`，则 `d` 必然整除 `a` 与 `b` 的任意线性组合。特别地，`d` 整除 `gcd(a, b)`（因为 `gcd` 本身就是所有能整除 `a` 与 `b` 的数的最大者）。反过来，`gcd(a, b)` 的每个因子显然也能整除 `a` 与 `b`。于是：

> “公共因子个数” = “`gcd(a, b)` 的因子个数”。

所以我们把问题转化为：**求一个数的因子个数**。这一步可以用 **遍历到平方根** 的技巧大幅降低复杂度。

**遍历到平方根的原理**：  
如果 `i` 是 `n` 的因子，那么 `n / i` 也是因子。`i` 与 `n / i` 成对出现，且 `i ≤ sqrt(n)`。因此只需要检查 `1 … √n`，每找到一个因子就算 **两** 个（除非 `i * i == n`，这时只算一个）。

#### 代码（Python）

```python
import math

def common_factors_optimal(a: int, b: int) -> int:
    """
    先求出 a 与 b 的最大公约数 g，
    再统计 g 的因子个数（只遍历到 sqrt(g)）。
    """
    # 1. 计算最大公约数（欧几里得算法）
    def gcd(x: int, y: int) -> int:
        while y:                # 当 y 不为 0 时循环
            x, y = y, x % y     # 余数作为新的 y，继续求
        return x                # 最终的 x 就是 gcd

    g = gcd(a, b)               # 公共因子一定是 g 的因子

    # 2. 统计 g 的因子个数
    cnt = 0
    limit = int(math.isqrt(g))  # sqrt(g) 的整数部分，math.isqrt 是整数开根号
    for i in range(1, limit + 1):
        if g % i == 0:           # i 能整除 g，说明找到了因子
            cnt += 1             # i 本身算一个因子
            if i != g // i:      # 配对的因子不是同一个（避免平方数重复计数）
                cnt += 1         # g // i 也是因子，算第二个
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(log min(a, b) + √g)`  
  - 计算 GCD 使用欧几里得算法，时间是 `O(log min(a, b))`（对数级，非常快）。  
  - 接下来遍历到 `√g`（`g` 是 `gcd(a, b)`），最坏情况下 `g ≤ min(a, b) ≤ 1000`，所以最多检查约 `√1000 ≈ 32` 次，几乎可以忽略不计。  
  - 与暴力解的 `O(min(a, b))`（最多 1000 次）相比，优化后只需几十次循环，速度提升明显。

- **空间复杂度**：`O(1)`  
  - 同样只用了常数个变量，没有额外的数组或递归栈。

---

## 心得

- **核心技巧**：先求最大公约数（GCD），再统计其因子个数。  
- **适用的题型**  
  1. “两个数的公共约数/因子” 类问题（如 LeetCode 2427 `Number of Ways to Reach a Destination` 的数论变体）。  
  2. “求一个数的约数个数” 类问题（如 1028 `Recover a Tree From Preorder Traversal` 中的数论子任务）。  
  3. “判断是否存在满足某种因子关系的数” 类题目（如 1366 `Palindrome Pairs` 中的数值约束）。  
- **一句话总结**：**公共因子 = 最大公约数的因子**，先把问题压缩到一个数上，再用平方根遍历计数。

---

## 反思

- **第一反应**：直接枚举 `1 … min(a, b)`，把每个数都检查一遍。  
- **最容易踩的坑**  
  - 忘记只遍历到较小的数，会导致不必要的计算。  
  - 统计因子时忘记去重，尤其是平方数（如 `g = 36` 时，`6` 只算一次）。  
  - 对 GCD 的实现不熟悉，可能会写出递归版而导致栈溢出（虽然在本题规模下不会出现）。  
- **下次遇到同类题**：第一步先思考“是否能把两个数合并成一个更小的数（如 GCD）”，再决定遍历范围或使用更高效的数论技巧。