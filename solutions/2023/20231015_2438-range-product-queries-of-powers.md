# #2438. 幂的区间乘积查询 / Range Product Queries of Powers

> 难度：中等 · 标签：Array、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/range-product-queries-of-powers/)

---

## 题目（英文原版）

**Description**

Given a positive integer n, there exists a 0-indexed array called powers, composed of the minimum number of powers of 2 that sum to n. The array is sorted in non-decreasing order, and there is only one way to form the array.
You are also given a 0-indexed 2D integer array queries, where queries[i] = [lefti, righti]. Each queries[i] represents a query where you have to find the product of all powers[j] with lefti <= j <= righti.
Return an array answers, equal in length to queries, where answers[i] is the answer to the ith query. Since the answer to the ith query may be too large, each answers[i] should be returned modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 15, queries = [[0,1],[2,2],[0,3]]
Output: [2,4,64]
Explanation:
For n = 15, powers = [1,2,4,8]. It can be shown that powers cannot be a smaller size.
Answer to 1st query: powers[0] * powers[1] = 1 * 2 = 2.
Answer to 2nd query: powers[2] = 4.
Answer to 3rd query: powers[0] * powers[1] * powers[2] * powers[3] = 1 * 2 * 4 * 8 = 64.
Each answer modulo 109 + 7 yields the same answer, so [2,4,64] is returned.
```

**Example 2:**

```
Input: n = 2, queries = [[0,0]]
Output: [2]
Explanation:
For n = 2, powers = [2].
The answer to the only query is powers[0] = 2. The answer modulo 109 + 7 is the same, so [2] is returned.
```

**Constraints**

- 1 <= n <= 109
- 1 <= queries.length <= 105
- 0 <= starti <= endi < powers.length

---

## 题目（中文翻译）

给定一个正整数 `n`，存在一个下标从 0 开始的数组 **powers**（powers），该数组由若干个 2 的幂组成，且这些幂的和恰好等于 `n`。数组中的元素按非递减顺序排列，并且形成该数组的方式唯一，且使用的幂的个数最少。

同时，给定一个下标从 0 开始的二维整数数组 **queries**（queries），其中 `queries[i] = [left_i, right_i]`。每个 `queries[i]` 表示一次查询，需要求出 `powers[left_i] * powers[left_i+1] * … * powers[right_i]` 的 **product**（product）。

返回一个数组 **answers**（answers），其长度与 `queries` 相同，`answers[i]` 为第 `i` 条查询的答案。由于答案可能非常大，返回时需要对 `10^9 + 7` 取 **modulo**（modulo）。

**示例 1**  
**输入**: `n = 15, queries = [[0,1],[2,2],[0,3]]`  
**输出**: `[2,4,64]`  
**解释**:  
- 对于 `n = 15`，`powers = [1,2,4,8]`。可以证明不存在更短的 `powers`。  
- 第 1 条查询: `powers[0] * powers[1] = 1 * 2 = 2`.  
- 第 2 条查询: `powers[2] = 4`.  
- 第 3 条查询: `powers[0] * powers[1] * powers[2] * powers[3] = 1 * 2 * 4 * 8 = 64`.  
对 `10^9 + 7` 取模后结果不变，故返回 `[2,4,64]`.

**示例 2**  
**输入**: `n = 2, queries = [[0,0]]`  
**输出**: `[2]`  
**解释**:  
- 对于 `n = 2`，`powers = [2]`.  
- 唯一的查询答案为 `powers[0] = 2`，取模后仍为 `2`，因此返回 `[2]`.

**约束条件**  
- `1 <= n <= 10^9`  
- `1 <= queries.length <= 10^5`  
- `0 <= left_i <= right_i < powers.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把 `n` 拆成最少的 2 的幂**  
   - 这一步等价于把 `n` 的二进制表示里为 `1` 的位取出来。  
   - 例如 `n = 15 = 1111₂`，对应的幂是 `2⁰, 2¹, 2², 2³`，即 `[1,2,4,8]`。  
   - 把这些幂按从小到大排好顺序，就是题目要求的 `powers` 数组。  
   - 这里的 “哈希表像查字典” 类比不太适用，直接把二进制位当成“字典的 key”，对应的 `2^i` 是“页码”。

2. **对每个查询直接遍历求积**  
   - 读取 `left, right`，把 `powers[left] … powers[right]` 逐个相乘，途中每一步都取模 `10⁹+7` 防止溢出。  
   - 由于 `powers` 最多只有 30 项（`n ≤ 10⁹ < 2³⁰`），即使查询多达 `10⁵`，遍历也只会乘最多 30 次，时间仍在可接受范围。

**为什么正确**  
- `powers` 完全由二进制位唯一确定，题目保证它是“最小长度”。  
- 直接相乘得到的就是题目要求的区间乘积，取模后仍然是正确答案（模运算对乘法是封闭的）。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def build_powers(n: int):
    """把 n 拆成最少的 2 的幂，返回升序列表"""
    powers = []
    bit = 0                # 当前检查的是第几位（2^bit）
    while n:
        if n & 1:          # 若当前位为 1，则加入对应的幂
            powers.append(1 << bit)   # 1 << bit == 2**bit
        n >>= 1            # 右移一位，继续检查更高位
        bit += 1
    return powers          # 已经是升序的

def brute_product_queries(n: int, queries):
    """暴力实现：对每个查询直接遍历相乘"""
    powers = build_powers(n)          # O(log n) ≤ 30
    ans = []
    for left, right in queries:
        prod = 1
        for i in range(left, right + 1):
            prod = (prod * powers[i]) % MOD   # 每一步取模防止整数爆炸
        ans.append(prod)
    return ans
```

#### 复杂度

- **时间复杂度**：  
  - 构造 `powers`：`O(log n)`（最多 30 步）。  
  - 每个查询遍历至多 30 项：`O(30) ≈ O(1)`。  
  - 总体 `O(log n + queries·log n)`，在本题的约束下可以看作 `O(queries)`。  
  - 大白话：`O(n²)` 这种“平方级”在这里根本不会出现，因为我们最多只循环 30 次。

- **空间复杂度**：  
  - `powers` 长度 ≤ 30，额外的 `ans` 长度等于查询数。  
  - 总体 `O(log n + queries)`，主要是保存答案的数组。

---

### 2. 最优解

#### 思路  

暴力解已经能跑，但我们仍可以把 **每个查询的时间** 降到 **O(1)**，只需一次前缀乘积预处理。

1. **前缀乘积**  
   - 定义 `pref[i] = (powers[0] * powers[1] * … * powers[i]) mod MOD`。  
   - `pref` 相当于“累积的商品账本”，查询区间 `[l, r]` 的乘积只需要两次查表。

2. **区间乘积的数学公式**  
   - 对普通加法，区间和可以用 `pref[r] - pref[l-1]` 求得。  
   - 对乘法，同理有 `pref[r] = pref[l-1] * product(l..r) (mod MOD)`。  
   - 把等式两边同时乘以 `pref[l-1]` 的 **模逆**（即 `pref[l-1]` 在模 `MOD` 下的倒数），得到  
     `product(l..r) = pref[r] * inv(pref[l-1]) mod MOD`。  

3. **模逆的获取**  
   - `MOD = 10⁹+7` 是质数，依据**费马小定理**：`a^(MOD-1) ≡ 1 (mod MOD)`，于是 `a^(MOD-2) ≡ a⁻¹ (mod MOD)`。  
   - 用快速幂（`pow(a, MOD-2, MOD)`）即可在 `O(log MOD)`（约 30）时间得到逆元。  

4. **特殊情况**  
   - 当 `l == 0` 时，区间乘积就是 `pref[r]`，不需要乘以逆元。

**核心技巧**：前缀乘积 + 模逆 → 区间乘积 O(1) 查询。  
类比：前缀和像是“跑步的累计里程表”，前缀乘积则是“累计的油耗表”，想算某段路的油耗，只要用总油耗除以起点之前的油耗（在模运算里用逆元代替除法）。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def build_powers(n: int):
    """同上，返回升序的 2 的幂列表"""
    powers = []
    bit = 0
    while n:
        if n & 1:
            powers.append(1 << bit)
        n >>= 1
        bit += 1
    return powers

def fast_product_queries(n: int, queries):
    """最优实现：前缀乘积 + 模逆，单次查询 O(1)"""
    powers = build_powers(n)                 # 长度 ≤ 30
    m = len(powers)

    # 1) 计算前缀乘积
    pref = [0] * m
    cur = 1
    for i in range(m):
        cur = (cur * powers[i]) % MOD
        pref[i] = cur                         # pref[i] = product of powers[0..i]

    # 2) 逐个回答查询
    ans = []
    for l, r in queries:
        if l == 0:
            # 区间从头开始，直接取前缀乘积
            ans.append(pref[r])
        else:
            # product = pref[r] * inv(pref[l-1]) % MOD
            inv = pow(pref[l - 1], MOD - 2, MOD)   # 快速幂求逆元
            ans.append((pref[r] * inv) % MOD)
    return ans
```

#### 复杂度

- **时间复杂度**：  
  - 构造 `powers`：`O(log n)`（≤30）。  
  - 前缀乘积：`O(m)`，`m ≤ 30`。  
  - 每个查询：一次 `pow`（`O(log MOD) ≈ 30`）+ 常数操作 → `O(1)` 实际上是常数级。  
  - 总体 `O(log n + m + queries·log MOD)`，在本题约等于 `O(queries)`。  
  - 与暴力相比，**查询从最多 30 次乘法降到了 1 次乘法 + 1 次快速幂**，在查询非常多（如 10⁵）时更稳健。

- **空间复杂度**：  
  - `powers`、`pref` 各占 `O(m)`（≤30）。  
  - `ans` 需要保存 `queries` 条答案，`O(queries)`。  
  - 整体 `O(queries)`，额外常数空间极小。

---

## 心得

- **核心技巧**：把区间乘积转化为前缀乘积 + 模逆（即“除法”在模空间里的实现）。  
- **适用场景**：  
  1. **区间乘积查询**（如本题、LeetCode 1735 “Counting Ways to Make Array With Product”）  
  2. **区间除法查询**（需要同样的前缀乘积 + 逆元）  
  3. **任意可逆运算的区间查询**（如区间乘法、区间幂次）  
- **一句话总结**：**“把区间乘积拆成前缀乘积的比值，用模逆代替除法”。**

---

## 反思

- **第一反应**：看到 “最少的 2 的幂”，立刻想到二进制位；看到 “区间乘积”，想到直接遍历乘。  
- **最容易踩的坑**：  
  - **模运算顺序**：乘法后必须立刻取模，否则整数会爆炸。  
  - **逆元的前置条件**：只有在模数是质数且前缀乘积不为 0 时逆元才存在，这里 `MOD` 为质数，`powers` 全为 2 的幂，乘积永不为 0。  
  - **边界 `l == 0`**：此时没有 `pref[l-1]`，需要单独处理。  
- **下次思路**：一看到“区间**聚合**（和/积/异或）”，第一步就先考虑**前缀/后缀**技巧，判断是否需要逆元或异或特性，再决定是否需要额外的数据结构（如线段树）。这样可以迅速把时间从 `O(k·queries)` 降到 `O(queries)`。