# #1175. 质数排列 / Prime Arrangements

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/prime-arrangements/)

---

## 题目（英文原版）

**Description**

Return the number of permutations of 1 to n so that prime numbers are at prime indices (1-indexed.)
(Recall that an integer is prime if and only if it is greater than 1, and cannot be written as a product of two positive integers both smaller than it.)
Since the answer may be large, return the answer modulo 10^9 + 7.

**Examples**

**Example 1:**

```
Input: n = 5
Output: 12
Explanation: For example [1,2,5,4,3] is a valid permutation, but [5,2,3,4,1] is not because the prime number 5 is at index 1.
```

**Example 2:**

```
Input: n = 100
Output: 682289015
```

**Constraints**

- 1 <= n <= 100

---

## 题目（中文翻译）

返回将 `1` 到 `n` 的所有数进行排列（permutations）的方案数，使得所有质数（prime numbers）都位于质数索引（prime indices）上（索引采用 **1** 开始计数）。  
（回想一下，整数若且仅若大于 `1` 且不能写成两个均小于它的正整数的乘积，则称其为质数。）

由于答案可能很大，请返回答案对 `10^9 + 7` 取模后的结果。

## 示例

### 示例 1
**输入**  
```
n = 5
```
**输出**  
```
12
```
**解释**  
例如排列 `[1,2,5,4,3]` 是合法的，而 `[5,2,3,4,1]` 不合法，因为质数 `5` 位于索引 `1`（不是质数索引）。

### 示例 2
**输入**  
```
n = 100
```
**输出**  
```
682289015
```

## 约束条件
- `1 <= n <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的排列都枚举出来**，然后逐个检查：

1. 生成 `1 … n` 的所有排列（可以用 Python 的 `itertools.permutations`）。
2. 对每个排列 `perm`，遍历下标 `i`（从 1 开始计数），如果 `i` 是素数，就要求 `perm[i‑1]` 也必须是素数；如果 `i` 不是素数，则 `perm[i‑1]` 也必须不是素数。
3. 满足全部条件的排列计数即为答案。

> **类比**：把所有可能的座位安排（每个人坐哪个座位）都写下来，然后一个个去检查“素数坐在素数座位上”。这就像把字典的每一页都翻一遍去找特定的词，显然非常慢。

**为什么它是正确的**：  
因为我们没有遗漏任何一种可能的排列，也没有错误地判断，只要检查过程写对了，计数必然是题目要求的答案。

**时间/空间分析**：

- 生成全部排列的数量是 `n!`（阶乘），即 `1·2·3·…·n`。  
  对每个排列我们还要遍历 `n` 个位置检查条件，所以总的**时间复杂度**是 `O(n!·n)`。  
  用大白话说：当 `n=5` 时，`5! = 120`，检查 120·5=600 次；但当 `n=10` 时，`10! ≈ 3.6M`，检查 36M 次，已经很难在几秒内算完；`n=20` 时更是天文数字，根本不可行。

- **空间复杂度**：要存放一条排列需要 `O(n)` 的空间，若一次只处理一条排列（生成器方式），额外空间仍是 `O(n)`。但如果一次性把所有排列放进列表，则需要 `O(n·n!)`，更不可取。

> 对于本题的约束 `1 ≤ n ≤ 100`，暴力解根本跑不完（`100!` 的数量天文级），只能作为思考起点。

#### 代码（Python）

```python
import itertools

def is_prime(x: int) -> bool:
    """判断 x 是否为素数（朴素 O(√x) 检查）"""
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True

def prime_arrangements_bruteforce(n: int) -> int:
    cnt = 0
    # 生成所有排列，perm 是一个元组，例如 (1,2,3,4,5)
    for perm in itertools.permutations(range(1, n + 1)):
        ok = True
        # i 为 1-indexed 的位置
        for i in range(1, n + 1):
            if is_prime(i) != is_prime(perm[i - 1]):   # 素数位置 ↔ 素数元素必须一致
                ok = False
                break
        if ok:
            cnt += 1
    return cnt
```

> 这段代码可以直接跑通小规模的 `n`（比如 `n ≤ 6`），但 **不要在 `n=100` 时运行**，会卡死。

#### 复杂度

- **时间复杂度**：`O(n!·n)` — 需要遍历所有 `n!` 种排列，并对每个排列检查 `n` 次。
- **空间复杂度**：`O(n)` — 只保存当前遍历到的一个排列（如果使用 `itertools.permutations` 的生成器）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的地方在于枚举所有排列**。其实我们根本不需要真的去排列，只要统计有多少种合法的安排方式即可。关键观察如下：

1. **位置和数字的“素数属性”是相互独立的**。  
   - 所有**素数下标**（即 2、3、5、7、11…）只能放**素数**。  
   - 所有**非素数下标**只能放**非素数**（包括 1 和合数）。
2. 设 `p =` 1~`n` 中的素数个数，`c = n - p` 为非素数个数。  
   - 素数下标有 `p` 个位置，需要把 `p` 个素数数字放进去。把 `p` 个不同的东西放进 `p` 个不同的格子，有 **`p!`（p 的阶乘）** 种排列方式。  
   - 同理，非素数下标有 `c` 个位置，需要把 `c` 个非素数数字放进去，也有 **`c!`** 种方式。
3. 两部分互不影响，**总合法排列数 = `p! * c!`**。  
4. 题目要求对 `10^9+7` 取模，直接在计算阶乘时取模即可防止整数爆炸。

> **类比**：想象有两组不同颜色的球（红色代表素数，蓝色代表非素数），还有两组对应颜色的盒子（红盒子只能放红球，蓝盒子只能放蓝球）。只要把每组球随意放进对应颜色的盒子里，红球的放法有 `p!` 种，蓝球的放法有 `c!` 种，整体组合就是两者相乘。

**如何快速求素数个数 `p`**  
- 由于 `n ≤ 100`，直接用**埃拉托斯特尼筛法（Sieve of Eratosthenes）**即可在 `O(n log log n)` 时间得到所有素数。实现非常简单：用一个布尔数组 `is_prime[0…n]`，先全部标记为 `True`（除 0、1 外），从小到大遍历，每次把当前素数的倍数标记为 `False`。

**阶乘取模**  
- 计算 `k! (mod M)` 时，只需要一个循环 `res = res * i % M`，`i` 从 `1` 到 `k`。因为 `M = 10^9+7` 是质数，直接取模不会影响结果的正确性。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def count_primes_upto_n(n: int) -> int:
    """埃拉托斯特尼筛法，返回 1..n 中素数的个数"""
    if n < 2:
        return 0
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            # 把 p 的所有倍数都标记为非素数
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1
    # 统计 True 的数量，即素数个数
    return sum(is_prime)

def factorial_mod(k: int) -> int:
    """计算 k! % MOD"""
    res = 1
    for i in range(2, k + 1):
        res = (res * i) % MOD
    return res

def prime_arrangements(n: int) -> int:
    """最优解：p! * (n-p)! % MOD"""
    prime_cnt = count_primes_upto_n(n)      # p
    composite_cnt = n - prime_cnt           # c
    return (factorial_mod(prime_cnt) * factorial_mod(composite_cnt)) % MOD
```

> 只需要 `O(n log log n)` 的时间（筛法）和 `O(1)` 额外空间（除了 `is_prime` 数组），对所有合法的 `n ≤ 100` 都能在毫秒级返回答案。

#### 复杂度

- **时间复杂度**：`O(n log log n)` — 主要是筛法的复杂度，远远小于暴力的 `n!`。  
  对于 `n = 100`，实际运行时间几乎可以忽略不计。
- **空间复杂度**：`O(n)` — 用了一个长度为 `n+1` 的布尔数组来标记素数。

> 与暴力解相比，时间从“天文级”降到了“线性级”，空间也从可能的 `O(n·n!)` 降到 `O(n)`，是典型的 **从枚举到计数** 的思路转变。

---

## 心得

- **核心技巧**：把“满足条件的排列数”转化为“不同类别的元素在对应类别位置的全排列”，于是答案是若干阶乘的乘积。  
- **适用场景**：  
  1. **分组排列**：如“奇数放在奇数位置，偶数放在偶数位置”。  
  2. **固定位置的元素**：如“字母 A 必须出现在第 1 位，B 必须出现在第 3 位”。  
  3. **组合计数中的独立子问题**：如“把红球放进红盒子，蓝球放进蓝盒子”。
- **一句话总结解题钥匙**：**先把元素和位置按属性划分成独立的组，组内全排列，组间相乘**。

---

## 反思

- **第一反应**：看到“素数必须在素数下标”，立刻想到要遍历所有排列检查——这就是暴力思路的自然起点。
- **最容易踩的坑**  
  - **忘记 1-indexed**：下标是从 1 开始，而 Python 列表是 0-indexed，需要在判断时把 `i+1` 当作位置。  
  - **素数判断的效率**：对每个 `i` 用 O(√i) 检查在 `n=100` 仍然可以，但如果 `n` 更大，最好预处理素数。  
  - **取模时的顺序**：`p! * c!` 可能在乘法前已经非常大，必须在每一步乘法后立刻 `% MOD`，否则会导致整数溢出（在 Python 虽然不溢出，但会极大降低效率）。
- **下次遇到同类题**，第一步应该问自己：“**这些约束是否把元素和位置划分成互不干扰的若干组**？”如果答案是“是”，那么就可以直接用 **计数×阶乘** 的思路，而不是去枚举。