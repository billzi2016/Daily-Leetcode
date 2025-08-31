# #3326. 使数组非递减的最少除法操作次数 / Minimum Division Operations to Make Array Non Decreasing

> 难度：中等 · 标签：Array、Math、Greedy、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimum-division-operations-to-make-array-non-decreasing/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Any positive divisor of a natural number x that is strictly less than x is called a proper divisor of x. For example, 2 is a proper divisor of 4, while 6 is not a proper divisor of 6.
You are allowed to perform an operation any number of times on nums, where in each operation you select any one element from nums and divide it by its greatest proper divisor.
Return the minimum number of operations required to make the array non-decreasing.
If it is not possible to make the array non-decreasing using any number of operations, return -1.

**Examples**

**Example 1:**

```
Input: nums = [25,7]
Output: 1
Explanation:
Using a single operation, 25 gets divided by 5 and nums becomes [5, 7] .
```

**Example 2:**

```
Input: nums = [7,7,6]
Output: -1
```

**Example 3:**

```
Input: nums = [1,1,1,1]
Output: 0
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums`。

如果一个自然数 `x` 的正除数严格小于 `x`，则称其为 `x` 的真因子（proper divisor）。例如，`2` 是 `4` 的真因子，而 `6` 不是 `6` 的真因子。

可以对数组 `nums` 任意次数地执行以下操作：每次选择 `nums` 中的任意一个元素，并将其除以其最大的真因子（greatest proper divisor）。

返回使数组非递减所需的最少操作次数。如果无论进行多少次操作都无法使数组非递减，则返回 `-1`。

示例 1:
```
Input: nums = [25,7]
Output: 1
Explanation:
只需要一次操作，25 被除以 5，数组变为 [5, 7] .
```

示例 2:
```
Input: nums = [7,7,6]
Output: -1
```

示例 3:
```
Input: nums = [1,1,1,1]
Output: 0
```

约束条件：
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个元素都尝试“要不要做一次除法”**，把所有可能的组合枚举出来，看看哪一种可以让数组变成非递减的，并记录下最少用了多少次操作。

- **数据结构**  
  - 使用 **列表** 保存原始数组。  
  - 用 **位掩码**（二进制的 0/1）表示每个位置是否做除法。把 `1` 看成“把这个位置除一次”，`0` 看成“不动”。位掩码就像一本字典的 **钥匙**，每一位对应一个词（数组下标），钥匙的形状（0/1）决定了我们要查哪一页（是否除法）。

- **为什么正确**  
  - 只要遍历了 **所有** 0/1 组合，就一定能覆盖**所有**合法的操作序列。只要其中有一种组合使得最终数组满足 `a[i] ≤ a[i+1]`，我们就能找到答案。

- **复杂度**  
  - 对长度为 `n` 的数组，有 `2ⁿ` 种 0/1 组合。  
  - 每种组合需要 O(n) 的时间检查是否非递减。  
  - **时间复杂度**：`O(n·2ⁿ)`，这在 `n = 10⁵` 时根本不可行。  
  - **空间复杂度**：仅存放原数组和一个位掩码，`O(n)`。

> 大白话：`O(2ⁿ)` 就像把所有可能的钥匙都拿出来排队尝试，钥匙的数量随 `n` 翻倍增长，根本不可能在合理时间里把所有钥匙都试完。

#### 代码（Python）

```python
from itertools import product
from math import gcd

def greatest_proper_divisor(x: int) -> int:
    """返回 x 的最大真因子（小于 x 的最大除数）。"""
    # 暴力找最大因子
    for d in range(int(x ** 0.5), 0, -1):
        if x % d == 0:
            # d 是因子，x//d 也是因子，取较大的那个（但要小于 x）
            return max(d, x // d) if max(d, x // d) != x else min(d, x // d)
    return 1      # x 为 1 时

def brute_min_operations(nums):
    n = len(nums)
    best = float('inf')
    # 0/1 组合，0 表示不除，1 表示除一次
    for mask in product([0, 1], repeat=n):
        cur = []
        ops = 0
        for i, bit in enumerate(mask):
            if bit == 0:
                cur.append(nums[i])
            else:
                # 只对合数有效，质数除以 1 不变
                g = greatest_proper_divisor(nums[i])
                cur.append(nums[i] // g)
                ops += 1
        # 检查是否非递减
        ok = all(cur[i] <= cur[i + 1] for i in range(n - 1))
        if ok:
            best = min(best, ops)
    return -1 if best == float('inf') else best
```

> 这段代码可以直接跑，但只适用于 `n` 很小（比如 `n ≤ 12`）的调试。

#### 复杂度

- **时间复杂度**：`O(n·2ⁿ)` —— 随着 `n` 的增长指数爆炸，几乎不可能在真实数据（`n ≤ 10⁵`）上跑完。
- **空间复杂度**：`O(n)` —— 只存原数组和当前尝试的数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**真正的难点在于每个位置我们只有两种状态**：

1. 保持原值（不做任何操作）  
2. 把它变成 **最小质因数**（因为除以最大真因子等价于把数降到它的最小质因数）

> **关键观察**：  
> 对任意正整数 `x`，最大的真因子是 `x / p`，其中 `p` 是 `x` 的 **最小质因数**（最小的能整除 `x` 的质数）。  
> 把 `x` 除以它的最大真因子得到的结果正好是 `p`。  
> 换句话说，一次操作只能把 **合数**降到它的 **最小质因数**，而质数根本改不了（最大真因子是 1，除以 1 不变）。

所以每个元素 **最多只需要考虑一次** 是否“降到最小质因数”。这把原本指数级的搜索空间压缩到线性的 **“左/右遍历 + 贪心”**。

---

#### 2.1 从右往左贪心

- **为什么从右边开始**  
  非递减要求 `a[i] ≤ a[i+1]`。如果我们从右往左决定 `a[i]` 的最终取值，只需要保证它 **不大于** 已经确定好的 `a[i+1]`（记作 `limit`）。  
  这正好把全局约束转化为局部约束：**当前值必须 ≤ 右侧的 limit**。

- **每一步该怎么选**  
  对当前位置 `x = nums[i]`，我们有两种候选值：

  1. **不动**：`v1 = x`（操作数 0）  
  2. **降一次**（如果 `x` 是合数）：`v2 = spf[x]`（最小质因数，操作数 1）

  我们希望 **尽可能少操作**，所以：

  - 若 `v1 ≤ limit`，直接保留 `x`，操作数不加，`limit = v1`。  
  - 否则若 `v2 ≤ limit`，只能把它降到 `v2`，操作数加 1，`limit = v2`。  
  - 否则两种都不满足，说明无论怎么做都无法让左侧元素 ≤ 右侧元素，**直接返回 -1**。

- **特殊情况**  
  - 当 `x` 是 **质数** 且 `x > limit`，`v2 = x`（因为质数的最小质因数就是它本身），两者都大于 `limit`，只能返回 `-1`。  
  - `x = 1` 的最小质因数也视作 `1`（它本身已经是最小的），同样遵循上述规则。

- **预处理最小质因数**  
  为了在 O(1) 时间得到每个数的最小质因数，先用 **埃拉托斯特尼筛法**（线性或普通版）在 `1 … 10⁶` 区间预计算 `spf[i]`（smallest prime factor）。  
  - 这一步相当于把“每个数的最小质因数”装进一本 **查字典**，下标是数字，值是对应的最小质因数。查询时间是常数。

- **算法伪代码**

```
build spf[1 … MAX]   // 线性筛，O(MAX)

ops = 0
limit = +∞          // 右侧当前可以接受的最大值

for i from n-1 downto 0:
    x = nums[i]
    if x <= limit:
        limit = x                // 不动
    else:
        y = spf[x]                // 最小质因数（若 x 为质数，y == x）
        if y <= limit:
            ops += 1
            limit = y            // 降一次
        else:
            return -1            // 无法满足非递减

return ops
```

- **为什么是最优的**  
  - **贪心证明**：在遍历到 `i` 时，右侧已经确定了一个最小可能的 `limit`（因为我们总是把右侧元素尽可能保持大）。如果当前 `x` 能够直接 ≤ `limit`，不动显然更好，因为不动不增加操作数且不会影响左侧的可行区间。  
  - 若只能通过一次降操作才能满足 `≤ limit`，这已经是唯一可行的选择，且只需要一次操作。再多的操作也没有意义（一次已经把它降到最小质因数，之后再除不再改变）。  
  - 因此每一步的决定都是**局部最优**，而局部最优累加起来就是全局最优。

#### 代码（Python）

```python
from typing import List

def smallest_prime_factors(limit: int) -> List[int]:
    """线性筛：返回长度为 limit+1 的数组 spf，其中 spf[x] 为 x 的最小质因数。"""
    spf = [0] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if spf[i] == 0:          # i 是质数
            spf[i] = i
            primes.append(i)
        # 用已有的质数去筛 i 的倍数
        for p in primes:
            if p * i > limit or p > spf[i]:
                break
            spf[p * i] = p
    spf[1] = 1                  # 特殊处理 1
    return spf

def min_operations(nums: List[int]) -> int:
    if not nums:
        return 0

    max_val = max(nums)
    spf = smallest_prime_factors(max_val)   # 预处理

    ops = 0
    limit = float('inf')      # 右侧当前允许的最大值

    # 从右往左遍历
    for x in reversed(nums):
        if x <= limit:
            # 不需要操作，直接保留
            limit = x
            continue

        # 只能尝试把它降到最小质因数
        y = spf[x]            # 对于质数 y == x
        if y <= limit:
            ops += 1
            limit = y
        else:
            # 两种都大于 limit，无法构成非递减序列
            return -1

    return ops
```

> **代码解释（中文注释）**  
> - `smallest_prime_factors` 使用 **线性筛**，一次遍历即可把每个数的最小质因数算出来，时间和空间都是 `O(max(nums))`。  
> - 主函数里 `limit` 初始为正无穷，代表右侧没有任何限制。  
> - `for x in reversed(nums)` 按照从后往前的顺序检查每个元素。  
> - 如果当前值已经不大于 `limit`，直接保留，`limit` 更新为当前值。  
> - 否则只能把它降到 `spf[x]`（最小质因数），检查是否还能 ≤ `limit`。能的话计数 `ops+=1`，并把 `limit` 更新为降后的值。  
> - 两种情况都不满足，说明无论怎样都无法让左侧元素 ≤ 右侧元素，直接返回 `-1`。  

#### 复杂度

- **时间复杂度**  
  - 线性筛：`O(M)`，其中 `M = max(nums) ≤ 10⁶`。  
  - 主循环：遍历一次数组 `O(n)`。  
  - **总体**：`O(n + M)`，在本题的约束下（`n ≤ 10⁵, M ≤ 10⁶`）非常快。  
  - 与暴力解的 `O(n·2ⁿ)` 相比，指数级的爆炸被降到了线性级。

- **空间复杂度**  
  - `spf` 数组大小 `M+1`，即 `O(M)`（≈ 1 MB 左右）。  
  - 额外变量 `O(1)`。  
  - 总体 `O(M)`，完全符合题目限制。

---

## 心得

- **核心技巧**：  
  - **“一次操作等价于把合数降到最小质因数”** 的数论观察。  
  - **从右往左的贪心**，把全局的非递减约束转化为局部的 “不超过右侧 limit”。  

- **适用的题型**（类似思路）  
  1. **“把数组变成递增/递减，只能对元素做单调削减”** 的题目（如“最小操作次数使数组单调递增”）。  
  2. **“每个数只能变成它的某个固定子值”** 的题目（如只能把数变成它的位数和、或把数变成它的最高位）。  
  3. **“只能一次性把数降到某个最小可行值”** 的数论贪心题（如把数除以最大因子、或把数变成其最小因子）。

- **一句话总结解题钥匙**：  
  > **“一次除法只能把合数降到最小质因数，逆向遍历保证左侧不超过右侧，从而用最少的降操作完成非递减”。**

---

## 反思

- **拿到题目第一反应**  
  - 先想 **枚举所有可能的除法组合**，因为每个元素可以“除”也可以“不除”。  

- **最容易踩的坑**  
  1. **忽视合数 vs 质数的区别**：质数除以最大真因子不改变，必须把这点写清楚，否则会错误地认为可以无限次降低质数。  
  2. **忘记最小质因数的数论等价**：直接去除最大真因子会让实现复杂，理解等价关系后可直接用最小质因数。  
  3. **边界值**：`1` 的最小质因数是 `1`，需要在筛数组里手动设为 `1`，否则会出现 `0` 或错误。  
  4. **数组全部递增的情况**：`limit` 初始为 `inf`，要确保第一步（最右侧元素）总是可以直接保留。  

- **下次遇到同类题，第一步该想到**  
  - **“每个元素的可变范围只有两种（原值或固定的更小值）”，先把这两种值算出来，然后逆向贪心检查是否可以满足单调约束”。**