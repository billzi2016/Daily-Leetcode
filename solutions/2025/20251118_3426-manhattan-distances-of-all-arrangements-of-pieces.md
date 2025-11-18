# #3426. 曼哈顿距离的所有棋子排列之和 / Manhattan Distances of All Arrangements of Pieces

> 难度：困难 · 标签：Math、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/manhattan-distances-of-all-arrangements-of-pieces/)

---

## 题目（英文原版）

**Description**

You are given three integers m, n, and k.
There is a rectangular grid of size m × n containing k identical pieces. Return the sum of Manhattan distances between every pair of pieces over all valid arrangements of pieces.
A valid arrangement is a placement of all k pieces on the grid with at most one piece per cell.
Since the answer may be very large, return it modulo 109 + 7.
The Manhattan Distance between two cells (xi, yi) and (xj, yj) is |xi - xj| + |yi - yj|.

**Examples**

**Example 1:**

```
Input: m = 2, n = 2, k = 2
Output: 8
Explanation:
The valid arrangements of pieces on the board are:

Thus, the total Manhattan distance across all valid arrangements is 1 + 1 + 1 + 1 + 2 + 2 = 8 .
```

**Example 2:**

```
Input: m = 1, n = 4, k = 3
Output: 20
Explanation:
The valid arrangements of pieces on the board are:

The total Manhattan distance between all pairs of pieces across all arrangements is 4 + 6 + 6 + 4 = 20 .
```

**Constraints**

- 1 <= m, n <= 105
- 2 <= m * n <= 105
- 2 <= k <= m * n

---

## 题目（中文翻译）

给定三个整数 `m`、`n` 和 `k`。  
一个大小为 `m × n` 的矩形网格中放置 `k` 个相同的棋子。返回在 **所有合法排列** 中，每一对棋子之间的曼哈顿距离（Manhattan Distance）的总和。  
合法排列指的是将全部 `k` 个棋子放在网格上，且每个格子至多放置一个棋子。  

由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。  

两个单元格 `(xi, yi)` 与 `(xj, yj)` 之间的曼哈顿距离定义为 `|xi - xj| + |yi - yj|`。

---

### 示例

**示例 1**

> **输入**: `m = 2, n = 2, k = 2`  
> **输出**: `8`  
> **解释**:  
> 棋子在棋盘上的合法排列如下:  
> （此处省略具体排列示意图）  
> 因此，所有合法排列中所有棋子对的曼哈顿距离之和为 `1 + 1 + 1 + 1 + 2 + 2 = 8`。

**示例 2**

> **输入**: `m = 1, n = 4, k = 3`  
> **输出**: `20`  
> **解释**:  
> 棋子在棋盘上的合法排列如下:  
> （此处省略具体排列示意图）  
> 所有排列中所有棋子对的曼哈顿距离之和为 `4 + 6 + 6 + 4 = 20`。

---

### 约束

- `1 <= m, n <= 10^5`
- `2 <= m * n <= 10^5`
- `2 <= k <= m * n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有合法的摆放方式都枚举出来**，再把每一种摆放里所有棋子对之间的 Manhattan 距离相加。

- **数据结构**：我们可以把棋盘的每个格子编号（比如从 `0 … m·n‑1`），用一个长度为 `k` 的数组 `pos` 保存这 `k` 个格子的编号。  
  这就像把“棋子所在的格子”写进一本小笔记本里，随时可以翻看。

- **正确性**：遍历 **每一种** 选取 `k` 个格子（不重复）的方式，必然会覆盖题目要求的“所有合法布局”。对每个布局，遍历所有 unordered pair `(i, j)`，累加 `|xi‑xj| + |yi‑yj|`，自然得到答案。

- **时间/空间分析**：  
  - 枚举所有布局相当于在 `N = m·n` 个格子里挑 `k` 个，组合数记作 `C(N, k)`。  
  - 对每一种布局我们还要遍历所有棋子对，数量是 `C(k, 2) = k·(k‑1)/2`。  
  - 所以总时间是 **`O( C(N, k) · k² )`**，这在最坏情况下会是天文数字（比如 `N=10⁵, k≈N/2`），根本跑不完。  
  - 空间只需要保存一个 `k` 长度的数组，`O(k)`，这点倒是没问题。  

> 大白话解释：  
> - `O(C(N, k))` 就像说“我们要把所有可能的拼图方式都列出来”，这本身已经是超大数量。  
> - 再乘上 `k²`（每幅图里要算所有棋子之间的距离），就像在每幅巨大的拼图上再做一次遍历，根本不可能在电脑里跑完。

#### 代码（Python）

```python
import itertools
from math import comb

def brute_force(m: int, n: int, k: int) -> int:
    MOD = 10**9 + 7
    cells = [(i, j) for i in range(m) for j in range(n)]   # 所有格子坐标
    ans = 0

    # 枚举所有挑 k 个格子的方式（组合）
    for combo in itertools.combinations(cells, k):
        # 对每一对棋子求 Manhattan 距离并累加
        for (x1, y1), (x2, y2) in itertools.combinations(combo, 2):
            ans += abs(x1 - x2) + abs(y1 - y2)
            ans %= MOD
    return ans
```

> 这段代码只能在极小的 `m·n`（比如 ≤ 10）上跑通，纯粹是为了说明“最笨的思路”。

#### 复杂度

- **时间复杂度**：`O( C(m·n, k) · k² )` —— 组合数会指数级增长，实际不可接受。  
- **空间复杂度**：`O(k)` —— 只保存当前选中的 `k` 个格子。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**真正的瓶颈**是“枚举所有布局”。我们需要把这一步**完全去掉**，只用**计数**来代替。

> **关键观察**  
> 把两个特定格子 `A`、`B` 固定住，问：有多少合法布局会让这两个格子同时被占据？  
> 只要这两个格子被占，剩下的 `k‑2` 个棋子可以随意放在其余 `N‑2`（`N = m·n`）个空格子里。  
> 因此，这种情况出现的次数恰好是  
> \[
> \binom{N-2}{k-2}
> \]  
> —— 组合数，和格子之间的距离无关。

> 所以**总答案**可以写成  
> \[
> \text{Ans} = \binom{N-2}{k-2}\; \times\; \underbrace{\sum_{\text{所有 unordered 格子对 }(p,q)}\!\! \text{Manhattan}(p,q)}_{\text{仅和格子位置有关}}
> \]

> 接下来只剩下**求所有格子对的 Manhattan 距离之和**，这一步可以利用**分离 x、y 坐标**来求。

---

#### 2.1 计算所有格子对的 Manhattan 距离之和

Manhattan 距离可以拆成两部分：

\[
|x_i-x_j| + |y_i-y_j|
\]

因此总和等于 **行距离之和 + 列距离之和**。

##### 行距离

- 行坐标只有 `0 … m‑1`（共 `m` 行），每一行有 `n` 列格子。  
- 任选两行 `r1 < r2`，它们之间的行距是 `r2 - r1`。  
- 这两行各有 `n` 列格子，所以 **行距会被每一种列的组合重复 `n·n = n²` 次**（因为可以任选第一行的任意列，再任选第二行的任意列）。

于是行距离之和 =  

\[
n^{2}\times \sum_{0\le r_1<r_2<m} (r_2-r_1)
\]

求和公式：

\[
\sum_{0\le r_1<r_2<m} (r_2-r_1)
= \frac{m^{3}-m}{6}
\]

（可以把它想象成把每一行的“距离贡献”累加起来，等价于把 `1,2,…,m‑1` 这些差值各自出现的次数相加，最终得到立方差的简洁表达式）。

所以 **行距离总和** 为  

\[
\boxed{n^{2}\times\frac{m^{3}-m}{6}}
\]

##### 列距离

同理，列距离总和为  

\[
\boxed{m^{2}\times\frac{n^{3}-n}{6}}
\]

##### 合并

\[
\text{pairDistSum}= \frac{n^{2}(m^{3}-m) + m^{2}(n^{3}-n)}{6}
\]

> 这一步只用了常数次算术运算，**与 `m、n` 的大小无关**。

---

#### 2.2 组合数的计算

我们需要 \(\displaystyle \binom{N-2}{k-2}\)（`N = m·n`）。  
`N ≤ 10⁵`，所以可以 **预先计算阶乘** `fac[i] = i! (mod MOD)`，以及它们的逆元 `invFac[i]`，用公式

\[
\binom{a}{b}= \frac{fac[a]}{fac[b]\;fac[a-b]} \pmod{MOD}
\]

逆元可以用费马小定理（`MOD` 为质数 `1e9+7`）求得：

\[
x^{-1}\equiv x^{MOD-2}\pmod{MOD}
\]

预计算一次 `O(N)`，随后每次查询 `O(1)`。

---

#### 2.3 最终公式

\[
\text{Ans}= \binom{N-2}{k-2}\; \times\; \text{pairDistSum}\;\;(\bmod\; MOD)
\]

所有乘法、除法（即乘以逆元）都在模 `MOD` 下完成。

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def mod_pow(a: int, e: int) -> int:
    """快速幂，返回 a^e % MOD"""
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def prepare_factorials(limit: int):
    """预计算 fac[i] = i! % MOD 与其逆元 invFac[i]"""
    fac = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fac[i] = fac[i-1] * i % MOD

    invFac = [1] * (limit + 1)
    invFac[limit] = mod_pow(fac[limit], MOD-2)          # 逆元 = (limit!)^(MOD-2)
    for i in range(limit, 0, -1):
        invFac[i-1] = invFac[i] * i % MOD                # 逆元的递推
    return fac, invFac

def nCr(n: int, r: int, fac, invFac) -> int:
    """返回 C(n, r) % MOD，假设 0 <= r <= n"""
    if r < 0 or r > n:
        return 0
    return fac[n] * invFac[r] % MOD * invFac[n-r] % MOD

def manhattanSum(m: int, n: int, k: int) -> int:
    N = m * n                     # 总格子数
    # 1️⃣ 组合数 C(N-2, k-2)
    fac, invFac = prepare_factorials(N)          # 只需要到 N
    comb = nCr(N-2, k-2, fac, invFac)

    # 2️⃣ 所有格子对的 Manhattan 距离之和（分离行列）
    # 公式里有除以 6，先把分子算好再乘以 6 的模逆元
    inv6 = mod_pow(6, MOD-2)      # 6 的逆元

    term_rows = (n * n) % MOD * ((m * m % MOD) * m % MOD - m) % MOD   # n² * (m³ - m)
    term_cols = (m * m) % MOD * ((n * n % MOD) * n % MOD - n) % MOD   # m² * (n³ - n)
    pairDistSum = (term_rows + term_cols) % MOD * inv6 % MOD          # 除以 6

    # 3️⃣ 最终答案
    ans = comb * pairDistSum % MOD
    return ans
```

> **代码要点注释**  
> - `prepare_factorials` 只在 `N ≤ 10⁵` 时开销 `O(N)`，对本题完全足够。  
> - `inv6` 是常数，等价于 `6⁻¹ (mod MOD)`，用来实现“除以 6”。  
> - 所有乘法均在模 `MOD` 下进行，防止中间结果爆炸。  

---

#### 复杂度

- **时间复杂度**：`O(N)`（只一次性预计算阶乘），后面的公式计算是 `O(1)`。  
  与 `m·n` 成线性关系，最多约 `10⁵` 次运算，轻松跑完。

- **空间复杂度**：`O(N)` 用于保存 `fac` 与 `invFac` 两个长度为 `N+1` 的数组。  
  这也是 `≈ 2·10⁵` 的整数，几百 KB 内存，完全可接受。

- 与暴力解相比：  
  - **时间**从指数级（`C(N,k)·k²`）降到线性 `O(N)`，快了天文倍。  
  - **空间**略增（需要阶乘表），但仍在常数级别。

---

## 心得

- **核心技巧**：把“每对格子出现的次数”用组合数计数，再把 **所有格子对的 Manhattan 距离之和** 分离成行、列两部分求和。  
- **适用题型**  
  1. 需要在 **所有组合** 中统计某种 “对” 的贡献（如求所有子集的 pairwise distance、pairwise xor 等）。  
  2. “把固定元素对的出现次数乘以它们的价值” 的计数问题（例如求所有排列中两元素相邻的次数）。  
- **一句话总结**：**先把“布局”去掉，用组合数计数每对格子出现的次数，再求出所有格子对的 Manhattan 距离总和**。

---

## 反思

- **第一反应**：直接枚举所有摆放方式，逐对计算距离——这在脑中是最自然的想法，却忽略了组合数的威力。  
- **最容易踩的坑**  
  1. **边界**：当 `k = 2` 时，`C(N-2, 0) = 1`，公式仍然成立；要确保组合函数对 `r = 0` 正确返回 1。  
  2. **模运算**：除以 6 必须乘以 6 的模逆元，直接使用整数除法会出错。  
  3. **大数乘法**：`m³`、`n³` 可能超过 64 位整数范围，务必在每一步都 `% MOD`，防止 Python 整数虽能自动扩容但会拖慢速度。  
- **下次类似题目**：第一步先思考 **“每个局部结构（例如一对格子）在所有全局结构中出现了多少次？”**，把全局枚举转化为局部计数，再利用数学求和或前缀/后缀技巧完成求和。这样往往能把暴力的指数级时间压缩到多项式甚至 O(1)。