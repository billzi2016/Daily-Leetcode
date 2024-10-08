# #2894. 可整除与不可整除数之和的差 / Divisible and Non-divisible Sums Difference

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/divisible-and-non-divisible-sums-difference/)

---

## 题目（英文原版）

**Description**

You are given positive integers n and m.
Define two integers as follows:
Return the integer num1 - num2.

**Examples**

**Example 1:**

```
Input: n = 10, m = 3
Output: 19
Explanation: In the given example:
- Integers in the range [1, 10] that are not divisible by 3 are [1,2,4,5,7,8,10], num1 is the sum of those integers = 37.
- Integers in the range [1, 10] that are divisible by 3 are [3,6,9], num2 is the sum of those integers = 18.
We return 37 - 18 = 19 as the answer.
```

**Example 2:**

```
Input: n = 5, m = 6
Output: 15
Explanation: In the given example:
- Integers in the range [1, 5] that are not divisible by 6 are [1,2,3,4,5], num1 is the sum of those integers = 15.
- Integers in the range [1, 5] that are divisible by 6 are [], num2 is the sum of those integers = 0.
We return 15 - 0 = 15 as the answer.
```

**Example 3:**

```
Input: n = 5, m = 1
Output: -15
Explanation: In the given example:
- Integers in the range [1, 5] that are not divisible by 1 are [], num1 is the sum of those integers = 0.
- Integers in the range [1, 5] that are divisible by 1 are [1,2,3,4,5], num2 is the sum of those integers = 15.
We return 0 - 15 = -15 as the answer.
```

**Constraints**

- 1 <= n, m <= 1000

---

## 题目（中文翻译）

给定正整数 `n` 和 `m`。  
定义两个整数：

- `num1` 为区间 `[1, n]` 中**不被** `m` 整除（not divisible by `m`）的所有整数之和。  
- `num2` 为区间 `[1, n]` 中**能被** `m` 整除（divisible by `m`）的所有整数之和。

返回 `num1 - num2`。

**示例 1**  
输入: `n = 10, m = 3`  
输出: `19`  
解释:  
- 在 `[1, 10]` 中不被 `3` 整除的整数为 `[1,2,4,5,7,8,10]`，`num1` 为这些整数的和 `= 37`。  
- 在 `[1, 10]` 中能被 `3` 整除的整数为 `[3,6,9]`，`num2` 为这些整数的和 `= 18`。  
返回 `37 - 18 = 19`。

**示例 2**  
输入: `n = 5, m = 6`  
输出: `15`  
解释:  
- 在 `[1, 5]` 中不被 `6` 整除的整数为 `[1,2,3,4,5]`，`num1` 为这些整数的和 `= 15`。  
- 在 `[1, 5]` 中能被 `6` 整除的整数为空集合 `[]`，`num2` 为这些整数的和 `= 0`。  
返回 `15 - 0 = 15`。

**示例 3**  
输入: `n = 5, m = 1`  
输出: `-15`  
解释:  
- 在 `[1, 5]` 中不被 `1` 整除的整数为空集合 `[]`，`num1` 为这些整数的和 `= 0`。  
- 在 `[1, 5]` 中能被 `1` 整除的整数为 `[1,2,3,4,5]`，`num2` 为这些整数的和 `= 15`。  
返回 `0 - 15 = -15`。

**约束条件**  
- `1 <= n, m <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把区间 `[1, n]` 的每个整数都枚举一遍，  
- **如果** 这个整数能被 `m` 整除，就把它加到 `num2`（可被整除的和）  
- **否则** 把它加到 `num1`（不可被整除的和）  

想象一下我们在超市挑选商品：  
- “能被 `m` 整除的商品”就像是特价商品，需要单独放进一个篮子；  
- 其它商品放进另一个篮子。遍历完所有商品后，分别把两个篮子的价钱相加，就得到了 `num1` 与 `num2`，最后返回 `num1 - num2`。  

这个方法 **一定正确**，因为我们把所有 `1…n` 的数都完整地分类，一点也不遗漏。  

**复杂度分析（大白话）**  
- **时间**：我们要检查 `n` 次，每次只做一次取模运算和一次加法，时间随 `n` 成正比，用大写的 **O(n)** 表示。比如 `n = 1000` 时会跑 1000 次，`n = 10⁶` 时会跑一百万次。  
- **空间**：只用到几个整数变量（`num1`, `num2`, `i`），不随 `n` 增长，用 **O(1)** 表示，意思是“常数级”，占用的内存几乎不变。  

#### 代码（Python）  

```python
def divisible_non_divisible_difference_bruteforce(n: int, m: int) -> int:
    """暴力枚举法，时间 O(n)，空间 O(1)"""
    num1, num2 = 0, 0               # 分别存放不可整除的和、可整除的和
    for i in range(1, n + 1):       # 从 1 遍历到 n（包括 n）
        if i % m == 0:              # i 能被 m 整除
            num2 += i               # 加到可整除的和里
        else:
            num1 += i               # 加到不可整除的和里
    return num1 - num2              # 按题目要求返回差值
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 随着 `n` 增大，运行时间线性增长。  
- **空间复杂度**：`O(1)` — 只用了固定数量的变量，内存占用不随 `n` 变化。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正耗时的地方** 是把每个数都检查一遍。  
如果我们能直接算出 “所有能被 `m` 整除的数的和”，就不需要遍历。  

**关键观察**：  
- 区间 `[1, n]` 所有整数的总和是一个等差数列，公式是 `n * (n + 1) / 2`。  
- 能被 `m` 整除的数形如 `m, 2m, 3m, …, km`，其中 `k = n // m`（即最多能取多少个 `m` 的倍数）。这也是一个等差数列，首项 `m`，公差 `m`，项数 `k`。它的和等于 `m * (1 + 2 + … + k)`，而 `1 + 2 + … + k = k * (k + 1) / 2`。  
- 题目要求返回 `num1 - num2`，而 `num1`（不可整除的和） = `total_sum - sum_divisible`，所以  

```
answer = (total_sum - sum_divisible) - sum_divisible
        = total_sum - 2 * sum_divisible
```

于是我们只要 **一次常数时间** 计算出 `total_sum` 与 `sum_divisible`，再套公式即可。  

**类比**：  
把所有商品的总价记作 `total_sum`，特价商品的总价记作 `sum_divisible`，普通商品的总价自然是 `total_sum - sum_divisible`。要求的差值就是普通商品价钱减去特价商品价钱，即 `total_sum - 2 * sum_divisible`。  

#### 代码（Python）  

```python
def divisible_non_divisible_difference_optimal(n: int, m: int) -> int:
    """数学公式直接求解，时间 O(1)，空间 O(1)"""
    # 1. 计算 1~n 的总和（等差数列求和公式）
    total_sum = n * (n + 1) // 2   # // 为整数除法，保证结果是整数

    # 2. 计算能被 m 整除的数的个数 k
    k = n // m                     # 最大的倍数，例如 n=10,m=3 时 k=3 (3,6,9)

    # 3. 计算这些倍数的和
    #    1+2+...+k = k*(k+1)//2, 再乘以 m 得到实际的数值和
    sum_divisible = m * k * (k + 1) // 2

    # 4. 按题目要求返回差值
    return total_sum - 2 * sum_divisible
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 只做了几次算术运算，执行时间不随 `n`、`m` 的大小变化。  
- **空间复杂度**：`O(1)` — 只用了常数个变量。  

与暴力解相比，时间从 **线性** 降到了 **常数**，在 `n` 很大时优势尤为明显。  

---  

## 心得  

- **核心技巧**：等差数列求和 + 计数整数倍数  
- **适用的题型**：  
  1. “求 1~n 中能被 k 整除的数的和”  
  2. “求区间内所有数的和减去满足某种条件的子集和”  
  3. “利用数学公式把遍历转化为 O(1) 计算”  
- **一句话总结**：**把“遍历求和”换成“等差数列求和”，直接用公式就能秒算出答案。**  

---  

## 反思  

- **第一反应**：先写一个循环把每个数分类累加——这是最安全的做法。  
- **最容易踩的坑**：  
  - 忘记使用整数除法 `//`，导致结果出现浮点数。  
  - 当 `m = 1` 时，所有数都是可整除的，`num1` 为 0，答案应该是负的总和。  
  - 计算 `k = n // m` 时要确保是向下取整，防止把超出范围的倍数算进去。  
- **下次遇到同类题**：第一步先思考 **是否可以把求和过程用等差数列公式表达**，如果能，就立刻写出 O(1) 解法；如果不行，再回到遍历的暴力思路。