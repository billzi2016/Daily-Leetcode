# #1735. 计数构造乘积为指定值的数组方式 / Count Ways to Make Array With Product

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Combinatorics、Number Theory · [LeetCode 链接](https://leetcode.com/problems/count-ways-to-make-array-with-product/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array, queries. For each queries[i], where queries[i] = [ni, ki], find the number of different ways you can place positive integers into an array of size ni such that the product of the integers is ki. As the number of ways may be too large, the answer to the ith query is the number of ways modulo 109 + 7.
Return an integer array answer where answer.length == queries.length, and answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: queries = [[2,6],[5,1],[73,660]]
Output: [4,1,50734910]
Explanation: Each query is independent.
[2,6]: There are 4 ways to fill an array of size 2 that multiply to 6: [1,6], [2,3], [3,2], [6,1].
[5,1]: There is 1 way to fill an array of size 5 that multiply to 1: [1,1,1,1,1].
[73,660]: There are 1050734917 ways to fill an array of size 73 that multiply to 660. 1050734917 modulo 109 + 7 = 50734910.
```

**Example 2:**

```
Input: queries = [[1,1],[2,2],[3,3],[4,4],[5,5]]
Output: [1,2,3,10,5]
```

**Constraints**

- 1 <= queries.length <= 104
- 1 <= ni, ki <= 104

---

## 题目（中文翻译）

给定一个二维整数数组 `queries`。对于每个 `queries[i]`，其中 `queries[i] = [n_i, k_i]`，求有多少种不同的方式可以向一个长度为 `n_i` 的数组中填入正整数，使得这些整数的乘积等于 `k_i`。由于答案可能非常大，返回第 `i` 条查询的答案对 **10^9 + 7** 取模后的结果。

返回一个整数数组 `answer`，其中 `answer.length == queries.length`，且 `answer[i]` 为第 `i` 条查询的答案。

---

### 示例

#### 示例 1
```
输入: queries = [[2,6],[5,1],[73,660]]
输出: [4,1,50734910]
解释:
每个查询相互独立。
- [2,6]：有 4 种方式填满长度为 2 的数组，使乘积为 6，分别是 [1,6], [2,3], [3,2], [6,1]。
- [5,1]：只有 1 种方式填满长度为 5 的数组，使乘积为 1，即 [1,1,1,1,1]。
- [73,660]：有 1 050 734 917 种方式填满长度为 73 的数组，使乘积为 660。  
  1 050 734 917 对 10^9 + 7 取模后得到 50 734 910。
```

#### 示例 2
```
输入: queries = [[1,1],[2,2],[3,3],[4,4],[5,5]]
输出: [1,2,3,10,5]
```

---

### 约束条件

- `1 <= queries.length <= 10^4`
- `1 <= n_i, k_i <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组的每一个位置都**枚举**一次，尝试所有可能的正整数，然后检查这 `n` 个数的乘积是否等于 `k`。  
可以用递归（深度优先搜索）来实现：

1. 当前正在填第 `pos` 位（从 `0` 开始），已经得到的乘积是 `prod`。  
2. 在第 `pos` 位尝试所有正整数 `x`（`x` 必须整除 `k // prod`，否则后面不可能得到 `k`）。  
3. 把 `x` 放进去，递归处理下一位 `pos+1`，乘积更新为 `prod * x`。  
4. 当 `pos == n` 时，检查 `prod == k`，若相等计数 +1。

> **生活化类比**：这相当于在厨房里把 `n` 个碗一个一个装满食材，每次都尝试所有可能的食材种类，最后看看装好的 `n` 碗的总重量是否正好等于目标重量 `k`。

这种方法一定能找到 **所有** 合法的填法，因为我们把每一种可能都遍历了一遍。

#### 代码（Python）

```python
from typing import List

def brute_force_one(n: int, k: int) -> int:
    """只用于演示的暴力解，适用于非常小的 n、k。"""
    ans = 0

    def dfs(pos: int, prod: int) -> None:
        nonlocal ans
        if pos == n:                     # 已经填满 n 个位置
            if prod == k:                # 检查乘积是否恰好等于 k
                ans += 1
            return

        # 剩余位置还能乘以多少数，最多只能是 k // prod
        # 为了保证乘积不超过 k，后面的数必须是 k // prod 的约数
        limit = k // prod
        for x in range(1, limit + 1):
            if k % (prod * x) != 0:      # x 不是合法的因子，剪枝
                continue
            dfs(pos + 1, prod * x)

    dfs(0, 1)
    return ans
```

> **关键行注释**  
> - `if pos == n:`：递归到底部，检查乘积是否正好是 `k`。  
> - `limit = k // prod`：后面所有数的乘积最多只能是 `k / 已有乘积`，否则必然超出。  
> - `if k % (prod * x) != 0:`：如果当前选择的 `x` 让整体乘积已经不可能整除 `k`，就提前返回，称为**剪枝**。

#### 复杂度  

- **时间复杂度**：`O(m^n)`（极其夸张的上界），其中 `m` 是 `k` 的约数个数。  
  - 直观解释：每一位我们都要尝试所有可能的数，最坏情况下每位都有 `m` 种选择，层层相乘就是指数级别。  
- **空间复杂度**：`O(n)`，递归栈的深度等于数组长度 `n`。

> 这已经远远超出题目给出的 `n、k ≤ 10⁴` 的规模，实际只能在非常小的测试里跑通。下面我们来找出瓶颈并优化。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举每个位置的具体数值** 是最慢的环节。  
真正决定答案的不是每个具体数，而是**每个质因子的出现次数**（即指数）如何在 `n` 个位置之间分配。  

**核心观察**：

- 任意正整数都可以唯一分解为若干质因子及其指数。  
  例如 `k = 660 = 2² * 3¹ * 5¹ * 11¹`。  
- 把 `k` 的所有质因子写成指数的形式后，数组的每个位置只需要决定自己拿走哪些指数。  
  设某个质因子 `p` 的指数是 `e`，我们要把这 `e` 个相同的“星星”分配到 `n` 个“盒子”里，每个盒子可以拿 0、1、2 … 个。  
- 这正是经典的**“星星与栏杆”(Stars and Bars)** 组合问题：  
  把 `e` 个相同的物品放进 `n` 个盒子，允许盒子为空，方法数为  

\[
\binom{e + n - 1}{n - 1}
\]

- 不同质因子之间是 **独立** 的（因为它们乘在一起才得到 `k`），所以总的填法数是所有质因子对应的组合数的乘积。

> **类比**：想象你有 `e` 颗相同颜色的糖果，要把它们放进 `n` 只相同的罐子里，每只罐子可以装任意数量（包括 0 颗）。把糖果分配完的方式有多少？答案就是上面的组合数。

**步骤概览**：

1. **质因数分解** `k`（`k ≤ 10⁴`，用试除法即可在 `O(√k)` 完成）。  
2. 对每个出现的指数 `e`，计算组合数 `C(e + n - 1, n - 1)`，取模 `MOD = 10⁹ + 7`。  
3. 把所有组合数相乘（模乘），即为该查询的答案。  

**组合数的快速求法**：

- 组合数公式：  

\[
C(a, b) = \frac{a!}{b! (a-b)!}
\]

- 为了在大量查询中快速得到 `C`，我们**预先**计算所有可能用到的阶乘 `fact[i]` 与其逆元 `inv_fact[i]`（使用费马小定理：`x⁻¹ ≡ x^{MOD-2} (mod MOD)`），这样一次 `O(1)` 就能得到任意组合数。  
- 需要的最大 `a` 为 `max_e + max_n - 1`。  
  - `max_n` ≤ 10⁴（题目限制）。  
  - `max_e` 是所有查询中出现的最大指数之和。因为 `k ≤ 10⁴`，最坏情况是 `k = 2^{13}`，所以 `max_e ≤ 13`。  
  - 为了安全，我们把上界设为 `max_n + 20`（足够大）。

#### 代码（Python）

```python
from typing import List
import math

MOD = 10 ** 9 + 7

# ---------- 预处理：阶乘 & 逆元 ----------
def precompute_factorials(limit: int):
    """返回两个数组：fact[i] = i! % MOD，inv_fact[i] = (i!)^{-1} % MOD"""
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (limit + 1)
    # 费马小定理求逆元：a^{-1} = a^{MOD-2} (mod MOD)
    inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
    for i in range(limit, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    return fact, inv_fact

def comb(a: int, b: int, fact: List[int], inv_fact: List[int]) -> int:
    """返回 C(a, b) % MOD，假设 0 <= b <= a"""
    if b < 0 or b > a:
        return 0
    return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

# ---------- 质因数分解 ----------
def prime_factorization(x: int) -> List[int]:
    """
    返回所有质因子的指数列表，例如 660 -> [2,1,1,1] 对应 2^2,3^1,5^1,11^1
    """
    exponents = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            exponents.append(cnt)
        d += 1 if d == 2 else 2   # 只检查 2 和奇数
    if x > 1:                     # 剩下的必然是质数
        exponents.append(1)
    return exponents

# ---------- 主函数 ----------
def ways_to_fill_array(queries: List[List[int]]) -> List[int]:
    """
    对每个查询 [n, k]，返回满足乘积为 k 的正整数数组填法数（模 1e9+7）。
    """
    # 预估需要的阶乘上界：max_n + max_possible_exponent
    max_n = max(q[0] for q in queries)
    max_k = max(q[1] for q in queries)

    # 计算所有 k 的指数之和的最大值（保守估计为 20）
    # 实际上 max_exponent_sum <= log2(10^4) ≈ 14
    max_exp_sum = 0
    for _, k in queries:
        # 简单统计每个 k 的指数之和
        temp = k
        d = 2
        while d * d <= temp:
            cnt = 0
            while temp % d == 0:
                temp //= d
                cnt += 1
            max_exp_sum = max(max_exp_sum, cnt)
            d += 1 if d == 2 else 2
        if temp > 1:
            max_exp_sum = max(max_exp_sum, 1)

    LIMIT = max_n + max_exp_sum + 5   # 预留一点余量
    fact, inv_fact = precompute_factorials(LIMIT)

    answers = []
    for n, k in queries:
        if k == 1:
            # 1 的质因子列表为空，唯一的填法是全 1
            answers.append(1)
            continue

        exps = prime_factorization(k)   # 获得所有指数
        ways = 1
        for e in exps:
            # 对每个指数 e，计算组合数 C(e + n - 1, n - 1)
            ways = ways * comb(e + n - 1, n - 1, fact, inv_fact) % MOD
        answers.append(ways)

    return answers
```

> **代码要点注释**  
> - `precompute_factorials`：一次性算出所有需要的阶乘和逆元，后面求组合数只要 O(1)。  
> - `prime_factorization`：把 `k` 拆成质因子并记录每个质因子的出现次数（指数）。  
> - `comb`：利用阶乘与逆元求组合数，防止出现除法导致的浮点误差。  
> - 主循环里，对每个指数 `e` 使用 **星星与栏杆** 公式 `C(e + n - 1, n - 1)`，最后把所有质因子的结果相乘。

#### 复杂度  

- **时间复杂度**：  
  - 预处理阶乘 `O(LIMIT)`，`LIMIT ≈ max_n + 20 ≤ 10⁴ + 20`，一次即可。  
  - 对每个查询：  
    - 质因数分解 `O(√k)`（`k ≤ 10⁴`，最多约 100 次循环）。  
    - 对每个指数计算组合数 `O(1)`。  
  - 总体 `O(Q * √k_max + LIMIT)`，其中 `Q = len(queries) ≤ 10⁴`。在最坏情况下约 `10⁴ * 100 = 10⁶` 次基本操作，轻松通过。

- **空间复杂度**：  
  - 阶乘数组 `O(LIMIT)` 大约 `10⁴` 长度的整数列表。  
  - 其他变量均为 O(1)。  
  - 整体 `O(10⁴)`，即几十 KB，远小于限制。

> 与暴力解相比：  
> - 暴力解的时间是指数级（随 `n` 指数增长），根本不可接受。  
> - 最优解把问题转化为**组合计数**，只和 `n` 与 `k` 的质因子个数有关，线性/对数级别，效率高得多。

---

## 心得

- **核心技巧**：把乘积约束转化为**质因子指数的分配**问题，利用“星星与栏杆”计数公式。  
- **适用的题型**  
  1. **把数的乘积固定，求数组/序列的组合数**（如本题）。  
  2. **把整数拆成若干因子（或若干正整数）计数**（如“Number of Ways to Reorder Array”变体）。  
  3. **多项式系数/组合数的乘积计数**（例如“Count Number of Ways to Form a Target String”）。  
- **一句话总结**：  
  > “把乘积约束拆成指数分配，星星与栏杆公式帮你瞬间算出所有可能”。  

---

## 反思

- **第一反应**：看到“数组乘积为 k”，立刻想到**枚举**每个位置的数值。  
- **最容易踩的坑**  
  1. **忽略 1 的情况**：`k = 1` 时没有质因子，需要单独返回 1。  
  2. **组合数取模**：直接使用除法会出错，必须用阶乘的模逆来实现除法。  
  3. **阶乘上界不足**：`e + n - 1` 可能比 `n` 大，需要提前算好足够大的 `LIMIT`。  
  4. **质因数分解的实现细节**：循环步长要跳过偶数以提升效率，且要处理剩余的质数。  

- **下次遇到同类题**，第一步应该思考**是否可以把数值约束转化为离散的“计数分配”**（如指数、位数、颜色等），再寻找对应的**组合计数公式**（星星与栏杆、容斥、排列组合等），而不是直接枚举。这样往往能把指数级别的问题降到多项式甚至常数级别。