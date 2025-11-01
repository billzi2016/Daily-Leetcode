# #3405. 计数相邻元素恰好相同 K 次的数组数量 / Count the Number of Arrays with K Matching Adjacent Elements

> 难度：困难 · 标签：Math、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/)

---

## 题目（英文原版）

**Description**

You are given three integers n, m, k. A good array arr of size n is defined as follows:
Return the number of good arrays that can be formed.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 3, m = 2, k = 1
Output: 4
Explanation:
```

**Example 2:**

```
Input: n = 4, m = 2, k = 2
Output: 6
Explanation:
```

**Example 3:**

```
Input: n = 5, m = 2, k = 0
Output: 2
Explanation:
```

**Constraints**

- 1 <= n <= 105
- 1 <= m <= 105
- 0 <= k <= n - 1

---

## 题目（中文翻译）

**描述**  
给定三个整数 `n、m、k`。定义长度为 `n` 的数组 `arr` 为「好数组」当且仅当：

- `arr` 的每个元素均取自区间 `[1, m]`（即 1 ≤ arr[i] ≤ m）；
- 在相邻位置 `i`（0 ≤ i < n‑1）中，恰好有 `k` 个位置满足 `arr[i] == arr[i+1]`（相邻元素相等的次数为 `k`）。

返回可以构造的好数组的数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

**示例**

示例 1  
Input: `n = 3, m = 2, k = 1`  
Output: `4`  
解释：  
（此处省略具体解释，仅保留标题）

示例 2  
Input: `n = 4, m = 2, k = 2`  
Output: `6`  
解释：  
（此处省略具体解释，仅保留标题）

示例 3  
Input: `n = 5, m = 2, k = 0`  
Output: `2`  
解释：  
（此处省略具体解释，仅保留标题）

**约束条件**

- `1 <= n <= 10^5`
- `1 <= m <= 10^5`
- `0 <= k <= n - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的数组枚举出来，逐个检查它们有多少个相邻相等的位置，如果恰好等于 `k` 就计数。  

- **数据结构**：我们只需要一个普通的 Python 列表 `arr` 来存放当前枚举的数组。  
- **生活化类比**：把数组想象成一排颜色的灯泡，每个灯泡可以点亮 `m` 种颜色。暴力做法就是把每一种点灯方式都列出来，然后数数有多少对相邻的灯泡颜色相同。  
- **正确性**：因为我们把 **所有** 可能的数组都遍历了一遍，凡是满足条件的必然会被统计到，所以答案一定是正确的。  

#### 代码（Python）

```python
from itertools import product

MOD = 10**9 + 7

def brute_force(n: int, m: int, k: int) -> int:
    """
    暴力枚举所有长度为 n、取值范围 [1, m] 的数组，
    统计恰好有 k 对相邻相等的数组个数。
    """
    ans = 0
    # product 会生成 m^n 种可能的元组，每个元组就是一种数组取值
    for arr in product(range(1, m + 1), repeat=n):
        # 统计相邻相等的次数
        cnt = sum(1 for i in range(1, n) if arr[i] == arr[i-1])
        if cnt == k:
            ans += 1
    return ans % MOD

# 小规模测试
print(brute_force(3, 2, 1))   # 4
print(brute_force(4, 2, 2))   # 6
print(brute_force(5, 2, 0))   # 2
```

#### 复杂度  

- **时间复杂度**：`O(m^n * n)`  
  - 解释：我们要遍历 `m^n` 种数组，每种数组需要遍历 `n-1` 条相邻边来计数，所以总工作量是指数级的，随着 `n`、`m` 的增大会很快爆炸。  
- **空间复杂度**：`O(n)`  
  - 解释：只需要保存当前枚举的数组（长度 `n`），其余都是常数级的临时变量。

> 由于题目限制 `n,m` 都可以到 `10^5`，暴力根本不可行，只能作为思路的“起点”。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**每个位置的取值只与它左边的元素是否相等有关**，而不需要关心更远的元素。因此我们可以用组合数学直接计数，而不是枚举。

1. **先决定哪些相邻位置相等**  
   - 在 `n-1` 条相邻边（`i = 1 … n-1`）里挑出恰好 `k` 条让它们相等。  
   - 这相当于从 `n-1` 张“卡片”中挑 `k` 张，方法数是二项式系数 `C(n-1, k)`。  
   - 类比：在一排座位中挑出 `k` 把相邻的座位坐在一起的方式。

2. **为每种挑选方式赋值**  
   - 第一个元素 `arr[0]` 可以随意取 `m` 种颜色（相当于字典的“查词”，有 `m` 种可能）。  
   - 对于 **相等的** 边（我们已经挑好的 `k` 条），`arr[i]` 必须和 `arr[i-1]` 相同，**没有自由度**，只能跟随左边的值。  
   - 对于 **不相等的** 边（其余 `n-1-k` 条），`arr[i]` 必须和 `arr[i-1]` 不同。除去左边已经占用的那一种颜色，剩下 `m-1` 种可以选。每条不相等的边互不影响，故有 `(m-1)^{n-1-k}` 种选择。  

3. **把三部分相乘**  
   - 总数 = `m`（第一个位置） × `C(n-1, k)`（挑相等位置） × `(m-1)^{n-1-k}`（不相等位置的自由选择）。  

4. **大数取模**  
   - 题目要求对 `10^9+7` 取模。我们需要快速计算二项式系数和幂次，常用技巧是**预计算阶乘 & 逆元**（利用费马小定理）以及**快速幂**。  

**核心算法解释**  

- **阶乘 & 逆元**：`C(n, r) = fact[n] * inv_fact[r] * inv_fact[n-r] (mod MOD)`。  
  - `fact[i]` 为 `i! mod MOD`，可以线性预计算到 `n`。  
  - `inv_fact[i]` 为 `fact[i]` 的模逆元，同样可以线性预计算（先算 `inv_fact[n]`，再倒推）。  
  - 逆元的概念可以类比为“除法的乘法逆”，因为在模运算里没有直接除法，只能乘以逆元。  

- **快速幂**：计算 `(m-1)^{exp} mod MOD` 用二分幂（每次把指数减半），时间是 `O(log exp)`。  

#### 代码（Python）

```python
MOD = 10**9 + 7

def mod_pow(a: int, e: int) -> int:
    """二分幂：计算 a^e (mod MOD)"""
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

def prepare_factorials(limit: int):
    """预计算 0..limit 的阶乘和逆元"""
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = (fact[i-1] * i) % MOD

    inv_fact = [1] * (limit + 1)
    # 先算最高的逆元：fact[limit]^(MOD-2) 根据费马小定理
    inv_fact[limit] = mod_pow(fact[limit], MOD - 2)
    for i in range(limit, 0, -1):
        inv_fact[i-1] = (inv_fact[i] * i) % MOD   # 逆元的倒推关系

    return fact, inv_fact

def comb(n: int, r: int, fact, inv_fact) -> int:
    """计算 C(n, r) (mod MOD)"""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

def count_arrays(n: int, m: int, k: int) -> int:
    """
    计数满足恰好有 k 对相邻相等的数组数量。
    公式： m * C(n-1, k) * (m-1)^(n-1-k) (mod MOD)
    """
    if k > n - 1:          # 不可能出现这么多相等对
        return 0

    # 预计算到 n-1 即可（因为组合数里最大是 n-1）
    fact, inv_fact = prepare_factorials(n-1)

    choose = comb(n-1, k, fact, inv_fact)                # C(n-1, k)
    diff_pow = mod_pow(m-1, n-1-k)                       # (m-1)^(n-1-k)
    ans = m * choose % MOD
    ans = ans * diff_pow % MOD
    return ans

# ----------------- 示例测试 -----------------
print(count_arrays(3, 2, 1))   # 4
print(count_arrays(4, 2, 2))   # 6
print(count_arrays(5, 2, 0))   # 2
```

#### 复杂度  

- **时间复杂度**：`O(n + log MOD)`  
  - 解释：预计算阶乘需要遍历一次 `0 … n-1`（线性），快速幂是 `O(log (n))`，整体是线性级别，能够轻松处理 `10^5` 的规模。  
  - 与暴力解的 `O(m^n)` 相比，提升了 **指数级**（从指数级降到线性级）。  

- **空间复杂度**：`O(n)`  
  - 解释：存放 `fact`、`inv_fact` 两个长度为 `n` 的数组。除去这两个数组，只用了常数级的额外空间。  

---

## 心得

- **核心技巧**：把“恰好 k 对相邻相等”转化为“在 n‑1 条相邻边中挑出 k 条相等”，随后使用组合数与幂次独立计数。  
- **适用场景**：  
  1. **计数相邻约束** 的排列问题（如“恰好 k 对相邻相同字符”）。  
  2. **固定相等/不等位置** 的序列计数（如“恰好 k 次上坡/下坡”）。  
  3. **颜色涂色类** 需要限制相邻相同数量的题目。  
- **一句话总结**：**先挑相等位置，再分别给相等/不相等位置分配自由度，乘法原理 + 组合数即可得到答案。**

---

## 反思

- **第一反应**：看到“相邻相等的个数恰好为 k”，自然会想到枚举所有数组然后计数——这就是暴力解。  
- **最容易踩的坑**  
  1. **忘记对第一个元素乘 `m`**：第一个位置没有左邻居，它本身也有 `m` 种取值。  
  2. **边界条件**：当 `k = 0` 或 `k = n-1` 时，组合数仍然适用，但要确保 `pow(m-1, …)` 的指数不为负。  
  3. **模运算细节**：组合数需要模逆元，直接用除法会出错。  
- **下次类似题的第一步**：先把“约束的数量”转化为“在多少条边上满足/不满足”，用**选取 + 独立赋值** 的思路写出计数公式，再考虑取模实现。