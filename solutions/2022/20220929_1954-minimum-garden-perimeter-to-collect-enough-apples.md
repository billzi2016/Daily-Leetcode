# #1954. 收集足够苹果的最小花园周长 / Minimum Garden Perimeter to Collect Enough Apples

> 难度：中等 · 标签：Math、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-garden-perimeter-to-collect-enough-apples/)

---

## 题目（英文原版）

**Description**

In a garden represented as an infinite 2D grid, there is an apple tree planted at every integer coordinate. The apple tree planted at an integer coordinate (i, j) has |i| + |j| apples growing on it.
You will buy an axis-aligned square plot of land that is centered at (0, 0).
Given an integer neededApples, return the minimum perimeter of a plot such that at least neededApples apples are inside or on the perimeter of that plot.
The value of |x| is defined as:

**Examples**

**Example 1:**

```
Input: neededApples = 1
Output: 8
Explanation: A square plot of side length 1 does not contain any apples.
However, a square plot of side length 2 has 12 apples inside (as depicted in the image above).
The perimeter is 2 * 4 = 8.
```

**Example 2:**

```
Input: neededApples = 13
Output: 16
```

**Example 3:**

```
Input: neededApples = 1000000000
Output: 5040
```

**Constraints**

- 1 <= neededApples <= 1015

---

## 题目（中文翻译）

在一个由无限二维网格（infinite 2D grid）构成的花园中，每个整数坐标点上都种有一棵苹果树。坐标为 \((i, j)\) 的苹果树上长有 \(|i| + |j|\) 个苹果。

你需要购买一块以 \((0, 0)\) 为中心、边与坐标轴平行的正方形土地（axis‑aligned square plot）。给定整数 `neededApples`，返回能够使该正方形内部或其边界上至少包含 `neededApples` 个苹果的最小周长（perimeter）。

\[
|x| = \begin{cases}
x & \text{if } x \ge 0 \\
-x & \text{if } x < 0
\end{cases}
\]

---

### 示例

#### 示例 1
**输入:** `neededApples = 1`  
**输出:** `8`  
**解释:** 边长为 1 的正方形不包含任何苹果。  
然而，边长为 2 的正方形内部（包括边界）共有 12 个苹果（如上图所示）。  
该正方形的周长为 \(2 \times 4 = 8\)。

#### 示例 2
**输入:** `neededApples = 13`  
**输出:** `16`

#### 示例 3
**输入:** `neededApples = 1000000000`  
**输出:** `5040`

---

### 约束条件
- \(1 \le \text{neededApples} \le 10^{15}\)

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把花园想象成一个无限大的棋盘，每个格子里都有一棵苹果树，坐标是整数 `(i, j)`，这棵树上长的苹果数等于 **曼哈顿距离** `|i| + |j|`（离原点越远，树上苹果越多）。  

我们要买一个**轴对齐、中心在原点**的正方形地块。  
如果正方形的半边长记为 `r`（即正方形的左、右、上、下边界分别是 `-r`、`+r`），  
- 正方形的**边长**是 `2·r`，  
- **周长**是 `8·r`（因为四条边各 `2·r`），  
- 正方形内部（包括边界）所有格子坐标满足 `max(|i|,|j|) ≤ r`。

我们只要把 `r` 从 `0` 开始逐渐增大，**每次都把正方形里所有格子的苹果数加起来**，看是否已经达到 `neededApples`。  
- 这里用到的“遍历所有格子”相当于**双层循环**，就像在纸上把每个格子都点一下，数一数苹果多少。  
- 只要苹果总数 ≥ `neededApples`，当前的 `r` 就是答案，周长 `8·r` 即为最小周长。

> **为什么这个方法一定对？**  
> 因为我们是**从小到大**检查所有可能的正方形，必然会在第一个满足需求的正方形处停下来，而后面的正方形只会更大（周长更长），所以得到的周长一定是最小的。

#### 代码（Python）

```python
def min_perimeter_bruteforce(neededApples: int) -> int:
    r = 0                     # 正方形的半边长，初始为 0
    while True:
        # 计算半边长为 r 的正方形里所有苹果的总数
        # 公式推导见后面的最优解，这里直接使用公式
        total = 2 * (2 * r + 1) * r * (r + 1)   # = 2 * (2r+1) * r * (r+1)
        if total >= neededApples:
            return 8 * r        # 周长 = 8 * r
        r += 1                  # 继续扩大正方形
```

> **关键行解释**  
> - `total = 2 * (2 * r + 1) * r * (r + 1)`：直接套用已知的求和公式，避免在循环里再套两层 `for`。  
> - `if total >= neededApples:`：一旦苹果够了，就返回当前周长。  

#### 复杂度  

- **时间复杂度**：`O(r)`，其中 `r` 是答案对应的半边长。  
  - 直观上可以把 `O(r)` 想成“我们最多要检查多少次正方形”。  
  - 当 `neededApples = 10^15` 时，`r` 大约是 `10^5`，所以最坏会循环十万次。  
- **空间复杂度**：`O(1)`，只用了常数个变量。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于我们把 `r` 一个一个递增，**每次都要重新计算** `total`，虽然公式本身是 O(1)，但 `r` 的上界可能达到 `10^5`，在最坏情况下仍会进行十万次循环。  

要把这个过程再快一点，我们可以**二分搜索**（Binary Search）`r`。  
二分搜索的核心思想是：

1. **单调性**：当 `r` 增大时，正方形包含的格子变多，苹果总数 `total(r)` 只会**不减**（实际上是严格递增）。  
2. 因此 `total(r) ≥ neededApples` 形成一个**阈值**：左边的 `r` 都不够，右边的 `r` 都够。  
3. 我们只要在可能的 `r` 范围内不断取中点 `mid`，检查 `total(mid)` 是否够，如果够则把右边界收紧，否则把左边界收紧，最终收敛到最小满足条件的 `r`。

**关键一步是求出 `total(r)` 的闭式公式**，这样每次检查只需要 O(1) 时间。下面推导这个公式：

- 正方形内部所有点满足 `-r ≤ i ≤ r`、`-r ≤ j ≤ r`。  
- 苹果数 = `|i| + |j|`，所以总和可以拆成两部分：  
  ```
  Σ|i| (对所有 i,j) + Σ|j| (对所有 i,j)
  = (2r+1) * Σ|i|  + (2r+1) * Σ|j|
  ```
  因为对每个固定的 `i`，`j` 有 `2r+1` 种取值，同理对 `j` 也是。  
- `Σ|i|`（i 从 -r 到 r） = `2 * (1 + 2 + … + r)` = `r(r+1)`（因为正负对称，0 的贡献为 0）。  
- 把它代入得到  
  ```
  total(r) = 2 * (2r + 1) * r * (r + 1)
  ```
  这正是暴力代码里用的公式。

**二分搜索的边界**：

- **左边界** `lo = 0`（最小可能的半边长）。  
- **右边界** `hi` 需要足够大，使得 `total(hi) ≥ neededApples`。  
  由于 `total(r) ≈ 4r³`（最高次项），我们可以粗略取 `hi = 1`，然后**指数级扩张**（`hi *= 2`）直到满足条件，这只会进行不到 30 次（因为 `2³⁰` 已经大于 `10⁹`），或者直接用 `hi = 10⁶`（安全上界）。  

二分结束后，`lo`（或 `hi`）就是最小满足条件的 `r`，答案周长 `8 * r`。

#### 代码（Python）

```python
def min_perimeter(neededApples: int) -> int:
    """
    二分搜索最小的半边长 r，使得正方形内部的苹果总数 >= neededApples。
    返回最小周长 8 * r。
    """
    # ---------- 1. 辅助函数：计算半边长为 r 的正方形内苹果总数 ----------
    def apples(r: int) -> int:
        # total = 2 * (2r + 1) * r * (r + 1)
        return 2 * (2 * r + 1) * r * (r + 1)

    # ---------- 2. 确定二分搜索的右边界 ----------
    lo, hi = 0, 1
    while apples(hi) < neededApples:   # 逐步扩大 hi，直到足够大
        hi <<= 1                       # hi *= 2，左移一位相当于乘 2

    # ---------- 3. 标准二分搜索 ----------
    while lo < hi:
        mid = (lo + hi) // 2
        if apples(mid) >= neededApples:
            hi = mid      # mid 已经够了，右边界收紧
        else:
            lo = mid + 1  # 不够，左边界右移

    # 循环结束时 lo == hi 为最小满足条件的 r
    return 8 * lo          # 周长 = 8 * r
```

> **关键行解释**  
> - `apples(r)`：一次性算出总苹果数，时间 O(1)。  
> - `while apples(hi) < neededApples: hi <<= 1`：指数扩张右边界，最多 30 次就能覆盖 `10^15` 级别的需求。  
> - 二分循环 `while lo < hi:`：每次都把搜索区间砍掉一半，最终只需要 `log2(hi)` 次检查（约 20~30 次），远快于线性遍历。  

#### 复杂度  

- **时间复杂度**：`O(log R)`，其中 `R` 是答案对应的半边长。  
  - 直观上可以把 `log R` 想成“把可能的范围不断二分，最多只需要几次检查”。  
  - 对于最大输入 `neededApples = 10^15`，`R` 约为 `10^5`，`log2(10^5) ≈ 17`，所以只会执行不到二十次循环。  
- **空间复杂度**：`O(1)`，只用了常数个变量（`lo、hi、mid` 等）。  

相比暴力的 `O(R)`（约十万次循环），二分搜索把时间压缩到了 **十几次**，提升巨大。

---

## 心得  

- **核心技巧**：**利用单调性进行二分搜索**，以及**把求和转化为闭式公式**。  
- **适用的题型**  
  1. “在某个范围内找最小/最大满足条件的整数”，如 “最小体积满足容量” 等。  
  2. “把二维/一维累计求和转化为公式”，如 “求曼哈顿距离之和的最大值” 等。  
- **一句话总结解题钥匙**：**先把问题抽象成“单调函数”，再用二分快速定位最小满足阈值**。

---

## 反思  

- **第一反应**：看到“每棵树的苹果数是 |i|+|j|”，立刻想到**遍历坐标求和**，于是写出暴力循环。  
- **最容易踩的坑**  
  - **边界条件**：`r = 0` 时正方形没有内部格子，苹果数为 0，需要确保循环从 0 开始。  
  - **整数溢出**：`apples(r)` 中涉及 `r³`，在 Python 中整数自动大数不会溢出，但在其他语言要使用 64 位或大整数。  
  - **右边界的选取**：如果直接把 `hi` 设得太小，二分可能永远找不到满足条件的 `r`，导致死循环。  
- **下次类似题目第一步**：**先检查是否存在单调关系**（例如随半径增大总量只增不减），**再尝试写出闭式或递推公式**，最后决定是否需要二分或其他对数级算法。