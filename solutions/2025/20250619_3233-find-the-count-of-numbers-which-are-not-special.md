# #3233. 统计非特殊数字的个数 / Find the Count of Numbers Which Are Not Special

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/find-the-count-of-numbers-which-are-not-special/)

---

## 题目（英文原版）

**Description**

You are given 2 positive integers l and r. For any number x, all positive divisors of x except x are called the proper divisors of x.
A number is called special if it has exactly 2 proper divisors. For example:
Return the count of numbers in the range [l, r] that are not special.

**Examples**

**Example 1:**

```
Input: l = 5, r = 7
Output: 3
Explanation:
There are no special numbers in the range [5, 7] .
```

**Example 2:**

```
Input: l = 4, r = 16
Output: 11
Explanation:
The special numbers in the range [4, 16] are 4 and 9.
```

**Constraints**

- 1 <= l <= r <= 109

---

## 题目（中文翻译）

给定两个正整数 `l` 和 `r`。对于任意整数 `x`，除 `x` 本身之外的所有正因子称为 `x` 的**真因子（proper divisors）**。  
如果一个数恰好拥有 **2** 个真因子，则称该数为**特殊数（special）**。  
返回区间 `[l, r]` 内**非特殊数**的个数。

**示例 1**  
**示例 2**  
**约束条件**  

**示例：**  

**示例 1:**  
```
Input: l = 5, r = 7
Output: 3
Explanation:
区间 [5, 7] 中不存在特殊数，所以全部 3 个数都不是特殊数。
```

**示例 2:**  
```
Input: l = 4, r = 16
Output: 11
Explanation:
区间 [4, 16] 中的特殊数为 4 和 9，共 2 个。
因此非特殊数的个数为 16 - 4 + 1 - 2 = 11。
```

**约束条件：**  
- `1 <= l <= r <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把区间 `[l, r]` 中的每一个整数 `x` 都枚举一遍，求出它的所有**真因子**（不包括 `x 本身`），统计它们的个数是否恰好为 2。如果是，就把它记为「特殊数」，最后用区间长度减去特殊数的个数即得到「非特殊数」的数量。

> **真因子**可以类比为一本词典里除去词条本身的所有解释词：我们只关心词条的“其他解释”。  
> **枚举所有因子**相当于把词条的每一页都翻一遍，看看有没有恰好两页是解释。

实现时，对于每个 `x`，我们可以从 `1` 到 `√x` 逐个检查能否整除 `x`。如果 `i` 能整除 `x`，那么 `i` 和 `x//i`（除非相等）都是 `x` 的因子。把 `x` 本身排除后，计数即可。

**为什么这个方法一定正确？**  
因为我们对每个数都完整地列举了它的所有真因子，判断条件「恰好有 2 个真因子」就是题目对「特殊数」的定义，符合题意。

**时间/空间复杂度**  
- 对每个 `x`，我们最多检查 `√x` 次。最坏情况下 `x ≈ r ≤ 10⁹`，所以每个数的检查次数约为 `√10⁹ ≈ 31623`。  
- 区间长度最多为 `r‑l+1 ≤ 10⁹`（理论上），但实际运行时受限于时间，暴力解会超时。  
- **时间复杂度** 大约是 `O((r‑l+1) * √r)`，可以粗略记作 `O(n·√M)`（`n` 为区间长度，`M` 为最大数）。这在最坏情况下会达到数十亿次操作，远远超出常规时间限制。  
- **空间复杂度** 只需要常数级的额外存储 `O(1)`（几个计数器），因为我们不需要额外的数据结构。

#### 代码（Python）

```python
import math

def count_not_special_bruteforce(l: int, r: int) -> int:
    """暴力枚举区间每个数，统计不是特殊数的个数"""
    total = r - l + 1               # 区间总长度
    special_cnt = 0                 # 记录特殊数的个数

    for x in range(l, r + 1):
        proper_divisors = 0         # 真因子计数
        # 只需要检查到 sqrt(x)
        limit = int(math.isqrt(x))
        for d in range(1, limit + 1):
            if x % d == 0:          # d 是因子
                other = x // d
                if d != x:          # d 本身不是 x
                    proper_divisors += 1
                if other != d and other != x:   # 另一个因子且不是 x
                    proper_divisors += 1
            if proper_divisors > 2:  # 已经超过2个，提前结束
                break
        if proper_divisors == 2:    # 正好2个真因子 → 特殊数
            special_cnt += 1

    return total - special_cnt      # 非特殊数 = 总数 - 特殊数
```

#### 复杂度

- **时间复杂度**：`O((r‑l+1) * √r)`  
  → 直观上可以理解为「每个数都要走一遍它的平方根那么多步」；如果 `r` 接近 `10⁹`，每个数要检查约 `3万` 次，乘以区间长度会非常慢。
- **空间复杂度**：`O(1)`  
  → 只用了几个整数计数器，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，瓶颈在于**对每个数都要枚举因子**。我们需要找一种方式，直接判断一个数是否「恰好有 2 个真因子」而不进行因子枚举。

**观察**：  
- 如果一个数 `x` 有 **恰好 2 个真因子**，这两个真因子只能是 `1` 与 `p`（其中 `p` 为某个素数），因为 `1` 必然是所有数的真因子。  
- 那么 `x` 的所有因子只有 `1、p、p²`（其中 `p² = x`），也就是说 `x` 必须是 **素数的平方**。  

> 类比：把 `x` 想成一棵只有根、一个分支、一个叶子的树，根是 `1`，分支是素数 `p`，叶子是 `p²` 本身。只有这样树才只有两条“枝叶”——恰好两个真因子。

因此，**「特殊数」 ⇔ 「某个素数的平方」**。  
于是求区间 `[l, r]` 中「非特殊数」的个数，只需要：

1. 计算区间长度 `total = r - l + 1`。  
2. 统计区间内 **素数的平方**（即 `p²`）的个数 `special_cnt`。  
3. `answer = total - special_cnt`。

**如何快速统计素数的平方落在 `[l, r]` 之间？**  
- `p²` 落在 `[l, r]` 当且仅当 `p` 落在 `[√l, √r]`（向上/向下取整）。  
- 所以我们只需要在区间 `[⌈√l⌉, ⌊√r⌋]` 中找出所有素数，然后计数即可。

**找素数的高效方法——埃拉托斯特尼筛法（Sieve of Eratosthenes）**  
- 这是一种“筛子”思路：先把 `2,3,4,…,N` 都标记为「可能是素数」；然后从最小的未被筛除的数 `p` 开始，把 `p` 的所有倍数（`p*p, p*p+p, …`）标记为「不是素数」。  
- 经过一次遍历后，剩下的未被标记的数就是素数。  
- 对于本题，`N = ⌊√r⌋ ≤ √10⁹ ≈ 31623`，非常小，筛法几乎瞬间完成。

**完整步骤**：

1. 计算 `low = ceil(sqrt(l))`、`high = floor(sqrt(r))`。如果 `low > high`，说明区间内根本没有平方数，直接返回 `total`。  
2. 使用埃拉托斯特尼筛法在 `[2, high]` 范围内生成所有素数。  
3. 遍历筛得的素数列表，统计满足 `low ≤ p ≤ high` 的个数 `special_cnt`。  
4. 返回 `total - special_cnt`。

#### 代码（Python）

```python
import math

def sieve(limit: int) -> list:
    """
    埃拉托斯特尼筛法，返回 ≤ limit 的所有素数
    limit 只会到 31623 左右，空间和时间都很友好
    """
    if limit < 2:
        return []
    # True 表示“可能是素数”，下标 i 对应数字 i
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # 只需遍历到 sqrt(limit)
    for p in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[p]:
            # 把 p 的所有倍数标记为非素数，起始位置从 p*p 开始
            step_start = p * p
            for multiple in range(step_start, limit + 1, p):
                is_prime[multiple] = False

    # 收集所有仍为 True 的下标，即素数
    return [i for i, prime in enumerate(is_prime) if prime]

def count_not_special(l: int, r: int) -> int:
    """返回区间 [l, r] 中不是特殊数的个数（最优解）"""
    total = r - l + 1                     # 区间总数

    # 计算可能的素数范围的平方根边界
    low = math.isqrt(l)
    if low * low < l:                     # 向上取整 sqrt(l)
        low += 1
    high = math.isqrt(r)                  # 向下取整 sqrt(r)

    if low > high:                        # 没有平方数落在区间
        return total

    # 生成所有 ≤ high 的素数
    primes = sieve(high)

    # 统计落在 [low, high] 的素数个数，即特殊数的个数
    special_cnt = sum(1 for p in primes if low <= p <= high)

    return total - special_cnt

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(count_not_special(5, 7))   # 3
    print(count_not_special(4, 16))  # 11
```

**代码要点注释**  
- `math.isqrt` 是整数平方根，避免浮点数误差。  
- `low` 用「向上取整」确保 `low² ≥ l`；`high` 用「向下取整」确保 `high² ≤ r`。  
- `sieve(high)` 只需要到 `high`（即 `√r`），因为更大的素数的平方必然超出 `r`。  
- `sum(1 for p in primes if low <= p <= high)` 直接统计满足区间的素数数量。

#### 复杂度

- **时间复杂度**：`O(√r log log √r)`（筛法的复杂度）  
  - 对 `√r ≤ 31623` 而言，这几乎是常数时间。与暴力解的 `O((r‑l+1)·√r)` 相比，快了几个数量级。  
- **空间复杂度**：`O(√r)` 用于存放 `is_prime` 数组（约 3 万个布尔值），在现代机器上几乎可以忽略不计。

---

## 心得

- **核心技巧**：把「恰好有 2 个真因子」转化为「素数的平方」的判定，从数的性质入手，而不是逐个枚举因子。  
- **适用的题型**  
  1. 判断一个数是否是**完全数**、**半完全数**等，需要利用数的因子结构的特殊形式。  
  2. 统计区间内**形如 `p³`（素数立方）**、**`p·q`（两个不同素数的乘积）**的数。  
  3. 与**平方数**、**立方数**相关的计数题，常常可以把范围映射到根号或三次根的区间，再用筛法找素数。  
- **一句话总结**：特殊数 = 「素数的平方」→只要数根号范围内的素数个数，就能快速得到答案。

---

## 反思

- **第一反应**：直接遍历区间、枚举因子——这在没有观察到「2 个真因子」的结构时是最自然的做法。  
- **最容易踩的坑**  
  1. **边界处理**：`low` 必须向上取整，`high` 必须向下取整，否则会把不在区间的平方数误算进去。  
  2. **整数溢出**：在语言中直接使用 `int(sqrt(x))` 可能产生浮点误差，推荐使用 `math.isqrt`（整数平方根）保证精确。  
  3. **空区间**：当 `l`、`r` 很接近且没有平方数时，需要提前返回 `total`，否则会出现 `low > high` 导致错误计数。  
- **下次遇到同类题**：第一步先思考「这个计数条件在数的因子结构上有什么特殊限制？」如果能把条件映射到「素数」或「幂」上，就可以把区间问题转化为根号/立方根范围的素数计数，随后使用筛法或其他素数生成技巧完成。