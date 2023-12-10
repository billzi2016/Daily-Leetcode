# #2507. 最小值：用质因数之和替换后 / Smallest Value After Replacing With Sum of Prime Factors

> 难度：中等 · 标签：Math、Simulation、Number Theory · [LeetCode 链接](https://leetcode.com/problems/smallest-value-after-replacing-with-sum-of-prime-factors/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n.
Continuously replace n with the sum of its prime factors.
Return the smallest value n will take on.

**Examples**

**Example 1:**

```
Input: n = 15
Output: 5
Explanation: Initially, n = 15.
15 = 3 * 5, so replace n with 3 + 5 = 8.
8 = 2 * 2 * 2, so replace n with 2 + 2 + 2 = 6.
6 = 2 * 3, so replace n with 2 + 3 = 5.
5 is the smallest value n will take on.
```

**Example 2:**

```
Input: n = 3
Output: 3
Explanation: Initially, n = 3.
3 is the smallest value n will take on.
```

**Constraints**

- 2 <= n <= 105

---

## 题目（中文翻译）

给定一个正整数 `n`。  
不断地将 `n` 替换为其质因数（prime factors）之和。  
返回 `n` 在整个过程中能够达到的最小值。

**示例 1**  
输入: `n = 15`  
输出: `5`  
解释: 初始时 `n = 15`。  
`15 = 3 * 5`，因此将 `n` 替换为 `3 + 5 = 8`。  
`8 = 2 * 2 * 2`，因此将 `n` 替换为 `2 + 2 + 2 = 6`。  
`6 = 2 * 3`，因此将 `n` 替换为 `2 + 3 = 5`。  
`5` 是 `n` 能达到的最小值。

**示例 2**  
输入: `n = 3`  
输出: `3`  
解释: 初始时 `n = 3`。  
`3` 已经是 `n` 能达到的最小值。

**约束条件**  
- `2 <= n <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**不断把 n 分解成质因数，再把这些因数相加**，得到的新数继续这么做，直到数不再变化为止。  
- **质因数**：把一个整数写成若干个质数相乘的形式，例如 `12 = 2 × 2 × 3`，质因数就是 `2,2,3`。  
- **实现**：对当前的 `n`，用**试除法**（从 2 开始往上找能整除的数）把它完全分解，记录每个因数出现的次数，把所有因数加起来得到 `next_n`。  
- **为什么一定会停下来**：每次用“因数之和”代替 `n`，得到的数一定 **不大于** 原来的 `n`，而且当 `n` 本身是质数时，因数只有它自己，和仍是 `n`，于是进入固定点。  

> 类比：把 `n` 看成一本字典，找出所有页码（质因数），然后把这些页码相加得到新的一页。只要页码不是唯一的（不是质数），新页码一定更靠前。

#### 代码（Python）  

```python
def prime_factor_sum(x: int) -> int:
    """返回 x 的所有质因数之和（含重复）"""
    s = 0
    d = 2                         # 从最小的质数 2 开始试除
    while d * d <= x:             # 只需要检查到 sqrt(x)
        while x % d == 0:         # 能整除就一直除下去
            s += d                # 记录一次因数 d
            x //= d
        d += 1 if d == 2 else 2   # 2 之后只检查奇数，稍微加速
    if x > 1:                     # 循环结束后若剩余的 x > 1，则它本身是质数
        s += x
    return s


def smallest_value_bruteforce(n: int) -> int:
    """暴力模拟：不断用质因数之和替换 n，直到不再变化"""
    while True:
        nxt = prime_factor_sum(n)
        if nxt == n:               # 已经是质数，停止
            break
        n = nxt
    return n
```

#### 复杂度  

- **时间复杂度**：`O( sqrt(n) * k )`  
  - 对每一次替换，我们都要用试除法遍历到 `√n`（最坏情况），这一步是 `O(√n)`。  
  - 由于每次替换都会让数变小，最多只会进行 `k` 次（`k` 与 `log n` 同阶），所以整体大约是 `O( √n · log n )`。  
  - 用大白话说，就是“每一步都要把数拆开，最慢要检查到它的平方根”，所以在最坏情况下会稍慢一些。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，不随 `n` 大小增长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每一步都要重新做一次试除**，即“找质因数”。  
如果我们提前把 **每个数的最小质因数**（Smallest Prime Factor，简称 SPF）算好，那么分解一个数只需要不断用 SPF 把它除下去，时间几乎是 `O(log n)`。  

**步骤**  

1. **预处理：线性筛（或普通埃拉托斯特尼筛）**  
   - 建立一个长度为 `MAX = 10⁵`（题目上限）的数组 `spf`，`spf[i]` 保存 `i` 的最小质因数。  
   - 只需要一次 `O(MAX log log MAX)` 的时间（几乎线性），之后查询任意 `i` 的最小质因数是 `O(1)`。  

2. **利用 SPF 快速求质因数之和**  
   - 对当前 `n`，循环：`p = spf[n]`（最小质因数），把 `p` 加到和里，`n //= p`，直到 `n == 1`。  
   - 这样每除一次，`n` 至少除以 2，最多除 `log₂ n` 次。  

3. **模拟过程**  
   - 同暴力解一样，不断把 `n` 换成“质因数之和”，直到不再变化（即 `n` 为质数）。  
   - 由于每一步的因数分解已经非常快，整体时间几乎只受 **模拟次数** 的影响，而模拟次数最多约 `log n`（每次都显著变小），因此整体是 **线性** 的 `O(MAX)`（主要是筛的代价）。  

> 类比：把 `spf` 看成一本“质数字典”，字典里每个数字对应它的“最近的质数邻居”。查字典的速度是 `O(1)`，所以拆数变得非常快。

#### 代码（Python）  

```python
def build_spf(limit: int) -> list[int]:
    """使用埃拉托斯特尼筛生成 0..limit 的最小质因数数组"""
    spf = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if spf[i] == 0:               # i 是质数
            spf[i] = i                # 质数的最小质因数就是它自己
            # 把 i 的倍数的最小质因数设为 i（如果还没被设过）
            for j in range(i * i, limit + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    return spf


def prime_factor_sum_fast(x: int, spf: list[int]) -> int:
    """利用最小质因数表，快速求 x 的质因数之和（含重复）"""
    s = 0
    while x > 1:
        p = spf[x]          # 当前最小质因数
        s += p
        x //= p
    return s


def smallest_value_optimal(n: int) -> int:
    """最优解：先预处理 SPF，再高效模拟"""
    MAX = 100_000                # 题目给的上限
    spf = build_spf(MAX)         # O(MAX log log MAX) 预处理

    while True:
        nxt = prime_factor_sum_fast(n, spf)
        if nxt == n:              # 已经是质数，停止
            break
        n = nxt
    return n
```

> 代码说明（每行中文注释已在函数内部给出），`build_spf` 只会在第一次调用时运行一次，之后的因数求和全部是 `O(log n)`。

#### 复杂度  

- **时间复杂度**：`O(MAX log log MAX + log n)`  
  - 预处理筛 `spf` 用 `O(MAX log log MAX)`，`MAX = 10⁵`，在实际运行中几乎可以视为常数。  
  - 每一次求“质因数之和”只需要 `O(log n)`（因为每除一次至少除以 2），而模拟的次数也在 `O(log n)` 之内。  
  - 综合来看，整个算法在题目范围内几乎是线性的 `O(MAX)`，远快于暴力的 `O(√n·log n)`。  

- **空间复杂度**：`O(MAX)`  
  - 需要保存长度为 `MAX+1` 的 `spf` 数组，大约 10⁵ 个整数，约 0.4 MB，符合限制。  

---

## 心得  

- **核心技巧**：利用**最小质因数表（SPF）**把“分解质因数”这一步从 `√n` 降到 `log n`。  
- **适用的题型**  
  1. 需要频繁求**某数的所有质因数**（如求因数之和、因子计数等）的题目。  
  2. 需要**快速判断质数**或**分解多个数**的情形（如离线质因数分解、欧拉函数求值等）。  
- **一句话总结**：先把“质因数”这本字典做好，后面查找就快得像翻页。  

---

## 反思  

- **第一反应**：直接写一个循环，用试除法不停分解，看到题目说“n 会逐渐变小”，就想直接模拟。  
- **最容易踩的坑**  
  - **忘记处理 n 为 1 的情况**（虽然约束 `n≥2`，但在分解过程中会出现 `x=1`，此时循环要结束）。  
  - **边界条件**：`n` 本身是质数时，应该直接返回，不再继续循环。  
  - **效率误区**：虽然 n 会快速变小，但如果每一步都用 `O(√n)` 的试除法，最坏情况下仍会超时。  
- **下次遇到同类题**：第一步想到“是否需要多次因数分解”。如果答案是“是”，立刻考虑 **预处理最小质因数**（或其他类似的筛法）来把每次分解的代价降到 `log` 级。