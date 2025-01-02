# #3007. 最大满足价格和不超过 K 的数 / Maximum Number That Sum of the Prices Is Less Than or Equal to K

> 难度：中等 · 标签：Binary Search、Dynamic Programming、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/)

---

## 题目（英文原版）

**Description**

You are given an integer k and an integer x. The price of a number num is calculated by the count of set bits at positions x, 2x, 3x, etc., in its binary representation, starting from the least significant bit. The following table contains examples of how price is calculated.
The accumulated price of num is the total price of numbers from 1 to num. num is considered cheap if its accumulated price is less than or equal to k.
Return the greatest cheap number.

**Examples**

**Example 1:**

```
Input: k = 9, x = 1
Output: 6
Explanation:
As shown in the table below, 6 is the greatest cheap number.
```

**Example 2:**

```
Input: k = 7, x = 2
Output: 9
Explanation:
As shown in the table below, 9 is the greatest cheap number.
```

**Constraints**

- 1 <= k <= 1015
- 1 <= x <= 8

---

## 题目（中文翻译）

给定整数 `k` 和整数 `x`。一个数 `num` 的价格（price）通过统计其二进制表示（binary representation）中位于第 `x、2x、3x …` 位的置位（set bits）个数来计算，位序从最低有效位（least significant bit）开始计数。下表展示了价格的计算示例。

`num` 的累计价格（accumulated price）是从 `1` 到 `num` 所有数的价格之和。如果累计价格小于等于 `k`，则称该 `num` 为「便宜」的（cheap）数。

**返回最大的便宜数。**

示例 1  
Input: `k = 9, x = 1`  
Output: `6`  
Explanation: 如下表所示，`6` 是最大的便宜数。

示例 2  
Input: `k = 7, x = 2`  
Output: `9`  
Explanation: 如下表所示，`9` 是最大的便宜数。

约束条件  
- `1 <= k <= 10^15`  
- `1 <= x <= 8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从 1 开始逐个枚举**，把每个数的「价格」累加起来，直到累计价格超过 `k` 为止，前一个数就是答案。  

- **「价格」的计算**：把整数的二进制写出来，找出第 `x、2x、3x …` 位（从最低位算起，第一位记为 1），统计这些位上有多少个 `1`，这就是该数的价格。  
- **累计价格**：把所有已经枚举过的数的价格相加。

> **类比**：把每个数想象成一本字典，字典里只保留第 `x、2x、3x …` 页的单词。我们要统计这些页上出现了多少次「单词」`1`，并把所有字典的「单词数」加在一起。

**为什么能得到正确答案**：因为我们严格按照题意「从 1 到 num」逐个累计价格，只要累计价格不超过 `k`，`num` 就是「便宜」的；第一个超过 `k` 的数的前一个必然是最大「便宜」数。

**复杂度分析**  
- 每检查一个数，需要遍历它的所有二进制位（最多 60 位，因为 `k ≤ 10^15`），时间 `O(60)`，常数很小。  
- 若答案本身是 `N`，我们要检查 `1…N`，总时间 `O(N·60)` → 实际上是 **线性** 的 `O(N)`。  
- 只使用了几个整数变量，空间 `O(1)`。

> **大白话**：如果答案是 1 000 000，程序要跑一百万次循环，每次循环只做几次位运算，跑得很慢；而 `k` 最大可以是 10^15，答案可能远大于一百万，线性算法根本不可行。

#### 代码（Python）

```python
def price(num: int, x: int) -> int:
    """返回单个数 num 的价格——统计第 x,2x,3x... 位上 1 的个数"""
    cnt = 0
    pos = x - 1               # 第 x 位的下标（0-index）
    while (1 << pos) <= num:  # 只要该位仍然在 num 的范围内
        if (num >> pos) & 1:   # 该位是否为 1
            cnt += 1
        pos += x               # 跳到下一个感兴趣的位
    return cnt


def cheap_number_bruteforce(k: int, x: int) -> int:
    """暴力枚举，返回最大 cheap number"""
    acc = 0          # 累计价格
    num = 0
    while True:
        num += 1
        acc += price(num, x)   # 累加当前数的价格
        if acc > k:            # 超出预算，前一个数就是答案
            return num - 1
```

#### 复杂度

- **时间复杂度**：`O(N·(log₂N / x))`，其中 `N` 为答案的大小。实际等价于 `O(N)`，在最坏情况下会超时。  
- **空间复杂度**：`O(1)`，只用了常数个整数。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于**逐个枚举**。我们需要一种**一次性**算出「前 `n` 个数的累计价格」的方法，这样就可以在 **二分搜索** 中快速判断「`n` 是否仍然 cheap」。

**关键观察**  

> 对于固定的二进制位 `p`（从 0 开始计数），在区间 `[1, n]` 中，有多少个数在该位上是 `1`？

这是一道经典的「统计区间内第 `p` 位 1 的个数」问题，答案可以用**周期性**求得：

- 以第 `p` 位为例，周期长度为 `2^{p+1}`（比如第 0 位的周期是 `2`，第 1 位是 `4`，……）。  
- 在每一个完整周期里，恰好有 `2^{p}` 个数的该位为 `1`（后半段都是 `1`）。  
- 余下的不满一个周期的部分，如果超过了前半段 `2^{p}`，多出的部分也会贡献 `1`。

用公式写出来：

```
cnt(p, n) = (n+1) // 2^{p+1} * 2^{p}
          + max(0, (n+1) % 2^{p+1} - 2^{p})
```

**把「价格」拆开**  

一个数的价格是「第 x、2x、3x… 位上 1 的个数之和」。  
因此 **累计价格** = 对所有感兴趣的位 `p ∈ {x-1, 2x-1, 3x-1, …}`，把 `cnt(p, n)` 加起来。

这样我们就能在 **`O(number_of_considered_bits)`**（最多 `60 / x ≤ 60`）时间内算出 `price_up_to(n)`，随后用 **二分搜索** 找到最大满足 `price_up_to(n) ≤ k` 的 `n`。

**二分搜索的上界**  

- `price_up_to(n)` 至少是 `n`（因为每个数至少可能在感兴趣的位上出现一次 `1`，但实际更小）。  
- 为了安全，我们可以先 **指数级扩展**：从 `hi = 1` 开始，若 `price_up_to(hi) ≤ k`，把 `hi` 翻倍，直到超出 `k`。这样得到的 `hi` 必然是答案的上界。

**完整步骤**  

1. 实现 `cnt(p, n)`，返回第 `p` 位在 `[1, n]` 中出现 `1` 的次数。  
2. 实现 `price_up_to(n, x)`，把所有 `p = x-1, 2x-1, …` 的 `cnt(p, n)` 累加。  
3. 用指数扩展得到搜索上界 `hi`。  
4. 在 `[lo=0, hi]` 之间二分搜索，保持 `price_up_to(mid) ≤ k`，最终 `lo` 即为答案。

#### 代码（Python）

```python
def count_ones_at_bit(n: int, bit: int) -> int:
    """
    统计在区间 [1, n] 中，第 bit 位（0-index）为 1 的整数个数。
    公式来源于二进制的周期性：每 2^{bit+1} 个数里恰好有 2^{bit} 个 1。
    """
    if n < 0:
        return 0
    period = 1 << (bit + 1)          # 2^{bit+1}
    full_cycles = (n + 1) // period  # 完整周期的个数
    ones = full_cycles * (1 << bit)  # 每个完整周期贡献的 1 的数量
    remainder = (n + 1) % period      # 余下的不满一个周期的长度
    # 余下的部分如果超过前半段，就会多出 remainder - 2^{bit} 个 1
    ones += max(0, remainder - (1 << bit))
    return ones


def accumulated_price(n: int, x: int) -> int:
    """
    计算从 1 到 n 的累计价格。
    只需要统计第 x、2x、3x… 位（下标为 x-1, 2x-1, …）的 1 的总数。
    """
    total = 0
    # 最高可能的位数不超过 60（因为 k ≤ 10^15，答案也不会超过 2^60）
    for bit in range(x - 1, 61, x):   # 步长为 x
        total += count_ones_at_bit(n, bit)
    return total


def max_cheap_number(k: int, x: int) -> int:
    """二分搜索得到最大的 cheap number"""
    # 1. 先找一个上界 hi，使得 accumulated_price(hi) > k
    lo, hi = 0, 1
    while accumulated_price(hi, x) <= k:
        hi <<= 1                      # hi *= 2，指数级增长

    # 2. 标准二分搜索，寻找最大的 lo 满足条件
    while lo < hi:
        mid = (lo + hi + 1) // 2      # 取上中点，防止死循环
        if accumulated_price(mid, x) <= k:
            lo = mid                  # mid 仍然 cheap，向右找更大
        else:
            hi = mid - 1              # mid 超出预算，向左收缩
    return lo
```

#### 复杂度

- **时间复杂度**  
  - 单次 `accumulated_price` 的计算：遍历所有感兴趣的位，最多 `⌈60 / x⌉ ≤ 60` 次，时间 `O(60) ≈ O(1)`。  
  - 二分搜索需要 `O(log answer)` 次检查。答案的规模最多在 `2^60` 量级，`log₂(2^60) = 60`。  
  - 因此整体时间为 **`O(log answer * 60)` ≈ `O(log answer)`**，在本题的约束下几乎瞬间完成。

- **空间复杂度**  
  - 只使用了若干整数变量，**`O(1)`**。

> 与暴力解相比：从 **线性** (`O(N)`) 降到了 **对数** (`O(log N)`) 级别，速度提升数千倍以上，能够轻松处理 `k = 10^15` 的极端输入。

---

## 心得

- **核心技巧**：把「累计价格」拆解为「每一位的 1 的出现次数」的求和，利用二进制的周期性公式快速统计，再配合二分搜索定位答案。
- **适用题型**  
  1. **区间内位计数**（例如 LeetCode 338：Counting Bits、LeetCode 1523：Count Odd Numbers in Interval）。  
  2. **单调性搜索**（例如 LeetCode 162：Find Peak Element、LeetCode 744：Find Smallest Letter Greater Than Target）。
- **一句话总结**：**把复杂的累计求和转化为若干独立位的计数，利用二进制周期性一次算完，再二分定位最大合法值**。

---

## 反思

- **第一反应**：直接从 1 枚举，逐个累加价格。虽然实现最直观，却忽略了 `k` 可能非常大，导致时间爆炸。
- **最容易踩的坑**  
  1. **位下标的偏移**：题目说「第 x、2x、3x 位」是从 **1** 开始计数，而 Python 的位运算是从 **0** 开始，需要记得 `bit = multiple * x - 1`。  
  2. **溢出/大数**：`k` 可达 `10^15`，在计算 `period = 1 << (bit + 1)` 时要确保 `bit` 不超过 Python 整数的安全范围（Python 整数自动大数，安全）。  
  3. **二分边界**：使用上取中点 `(lo + hi + 1) // 2` 防止在 `lo = hi - 1` 时无限循环。
- **下次类似题的第一步**：先思考「能否把累计求和拆成若干独立、可快速求值的子问题」，如果可以，往往意味着可以用**二分搜索**或**前缀和**等技巧把时间降到对数级。