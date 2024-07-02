# #2761. **目标和的质数对** / Prime Pairs With Target Sum

> 难度：中等 · 标签：Array、Math、Enumeration、Number Theory · [LeetCode 链接](https://leetcode.com/problems/prime-pairs-with-target-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer n. We say that two integers x and y form a prime number pair if:
Return the 2D sorted list of prime number pairs [xi, yi]. The list should be sorted in increasing order of xi. If there are no prime number pairs at all, return an empty array.
Note: A prime number is a natural number greater than 1 with only two factors, itself and 1.

**Examples**

**Example 1:**

```
Input: n = 10
Output: [[3,7],[5,5]]
Explanation: In this example, there are two prime pairs that satisfy the criteria. 
These pairs are [3,7] and [5,5], and we return them in the sorted order as described in the problem statement.
```

**Example 2:**

```
Input: n = 2
Output: []
Explanation: We can show that there is no prime number pair that gives a sum of 2, so we return an empty array.
```

**Constraints**

- 1 <= n <= 106

---

## 题目（中文翻译）

给定一个整数 `n`。如果两个整数 `x` 和 `y` 同时满足以下条件，则称它们构成一个质数对（prime number pair）：

- `x` 和 `y` 都是质数（prime），即大于 1 且仅有 1 与其本身两个因子；
- `x + y = n`。

返回所有满足条件的质数对 `[x_i, y_i]` 构成的二维有序列表。列表应按 `x_i` 的递增顺序排序。如果不存在任何质数对，返回空数组。

**示例 1**

> **输入**  
> `n = 10`  
> **输出**  
> `[[3,7],[5,5]]`  
> **解释**  
> 本例中有两组满足条件的质数对：`[3,7]` 与 `[5,5]`，按照题目要求的顺序返回。

**示例 2**

> **输入**  
> `n = 2`  
> **输出**  
> `[]`  
> **解释**  
> 可以证明没有任何质数对的和等于 2，故返回空数组。

**约束条件**

- `1 <= n <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有可能的 `x`（从 2 开始）都枚举一遍，计算对应的 `y = n - x`，然后判断 `x` 和 `y` 是否都是质数。如果是，就把 `[x, y]` 加进答案。  

- **质数判断**：可以用“试除法”。把 `x`（或 `y`）除以 `2,3,4,…,√x`，只要能整除就说明不是质数。  
- **数据结构类比**：这里我们只用到最基本的列表（list），相当于把所有符合条件的配对装进一个“收集盒”。  

为什么正确？因为题目要求的“质数对”定义正是 “两个数都是质数且和为 `n`”。只要把所有 `x` 试一遍，必然能找出所有满足条件的配对。

#### 代码（Python）

```python
import math
from typing import List

def prime_pairs_bruteforce(n: int) -> List[List[int]]:
    """暴力解：逐个尝试 x，使用 trial division 检查质数"""
    def is_prime(num: int) -> bool:
        if num < 2:
            return False
        # 只需要检查到 sqrt(num) 就够了
        limit = int(math.isqrt(num))
        for d in range(2, limit + 1):
            if num % d == 0:          # 能整除说明不是质数
                return False
        return True

    res: List[List[int]] = []
    # x 从 2 到 n-2（因为 y = n - x 也必须 ≥ 2）
    for x in range(2, n - 1):
        y = n - x
        if is_prime(x) and is_prime(y):
            # 为了让结果按 x 升序，只要遍历顺序是递增的就行
            res.append([x, y])
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n * sqrt(n))`  
  - 外层遍历 `x` 大约 `n` 次。  
  - 每次检查质数需要最多 `sqrt(n)` 次除法。  
  - 用大白话说，就是“如果 `n` 是 1,000,000，最多要做大约 1,000,000 × 1,000 = 10⁹ 次小计算”，会比较慢。  
- **空间复杂度**：`O(1)`（不计返回结果）  
  - 只用了几个临时变量，答案列表本身不算额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **质数判定**：每次都要重新做 trial division，重复工作很多。  
我们可以把 **“所有 ≤ n 的质数”** 预先算好，随后在枚举 `x` 时只做 **O(1)** 的查表。

**步骤**  

1. **筛法求质数**（埃拉托斯特尼筛法）  
   - 把 `2 … n` 看成一本“字典”。初始时所有页码都标记为“可能是质数”。  
   - 从最小的未标记数 `p` 开始，把 `p` 的所有倍数（`p*2, p*3, …`）标记为“不是质数”。  
   - 这样一次遍历后，所有仍然未标记的数就是质数。  
   - 这一步的时间是 `O(n log log n)`，空间是 `O(n)`（一个布尔数组）。  
2. **枚举配对**  
   - 只需要遍历 `x` 到 `n // 2`，因为配对 `[x, y]` 与 `[y, x]` 实际上是同一组，只保留 `x ≤ y` 即可。  
   - 对每个 `x`，直接看 `is_prime[x]` 与 `is_prime[n-x]` 两个布尔值，若都为 `True`，说明找到了质数对。  
   - 由于查表是 **O(1)**，整个枚举过程是 `O(n)`。

**类比**：把筛法想象成在超市里一次性把所有“过期商品”挑出来，以后再检查商品是否新鲜时，只需要看标签，而不必重新打开检查。

#### 代码（Python）

```python
from typing import List

def prime_pairs_optimal(n: int) -> List[List[int]]:
    """最优解：先用埃拉托斯特尼筛法预计算质数，再 O(1) 查表"""
    if n < 4:                # 最小可能的质数和是 2+2=4
        return []

    # ---------- 1. sieve ----------
    # is_prime[i] = True 表示 i 是质数
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False   # 0、1 不是质数

    # 只需遍历到 sqrt(n) 即可
    limit = int(n ** 0.5) + 1
    for p in range(2, limit):
        if is_prime[p]:                  # p 仍然是质数
            # 把 p 的所有倍数标记为非质数，从 p*p 开始可以省掉前面的重复标记
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False

    # ---------- 2. 枚举配对 ----------
    res: List[List[int]] = []
    for x in range(2, n // 2 + 1):      # 只遍历到一半，防止重复
        y = n - x
        if is_prime[x] and is_prime[y]:
            res.append([x, y])          # x 已经是递增的，结果自然有序

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n log log n)`  
  - 筛法本身的时间是 `n log log n`，比起 `n * sqrt(n)` 快了几个数量级。  
  - 枚举 `x` 只要 `O(n)`，不影响整体量级。  
  - 用通俗的话说：如果 `n = 1,000,000`，筛法大概只需要几百万次基本操作，几乎在瞬间完成。  
- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n+1` 的布尔数组来存放“是否是质数”。  
  - 与返回的答案相比，这个空间是必须的。

---

## 心得

- **核心技巧**：**埃拉托斯特尼筛法 + 一次线性枚举**。先把所有可能的质数一次性算好，后面再查表就能做到 **O(1)** 判定。
- **适用的题型**  
  1. “两个数的和为给定值，且两数必须满足某种数论性质”（如本题、`Two Sum` 变体）。  
  2. “统计区间内的质数对”或“寻找满足条件的质数三元组”。  
  3. “求满足某种可判定属性的数对/数列”，常常可以先把属性预处理成数组/哈希表。
- **一句话总结**：**“先把所有质数一次性筛出来，再用查表快速配对”。**

---

## 反思

- **第一反应**：直接遍历 `x`，每次用 trial division 判断质数。虽然能跑通小数据，但忽略了 `n` 可达 `10⁶` 的规模。  
- **最容易踩的坑**  
  - **边界条件**：`n < 4` 时没有合法配对，需要提前返回空列表。  
  - **重复配对**：如果遍历到 `n`，会出现 `[3,7]` 与 `[7,3]` 两次，需要限制 `x ≤ y`（即遍历到 `n//2`）。  
  - **筛法细节**：标记倍数时从 `p*p` 开始，否则会重复标记导致不必要的循环。  
- **下次遇到同类题**：第一步先思考 “是否可以把需要频繁判断的属性（如是否为质数）预处理成 O(1) 查询的结构”。如果可以，往往就能把暴力的 `O(n·sqrt(n))` 降到 `O(n log log n)` 甚至更低。