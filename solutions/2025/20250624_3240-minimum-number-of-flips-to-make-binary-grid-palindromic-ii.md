# #3240. 使二进制网格回文的最少翻转次数 II / Minimum Number of Flips to Make Binary Grid Palindromic II

> 难度：中等 · 标签：Array、Two Pointers、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-ii/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid.
A row or column is considered palindromic if its values read the same forward and backward.
You can flip any number of cells in grid from 0 to 1, or from 1 to 0.
Return the minimum number of cells that need to be flipped to make all rows and columns palindromic, and the total number of 1's in grid divisible by 4.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
Explanation:
```

**Example 2:**

```
Input: grid = [[0,1],[0,1],[0,0]]
Output: 2
Explanation:
```

**Example 3:**

```
Input: grid = [[1],[1]]
Output: 2
Explanation:
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m * n <= 2 * 105
- 0 <= grid[i][j] <= 1

---

## 题目（中文翻译）

给定一个 `m × n` 的二进制矩阵（binary matrix） `grid`。  
如果一行或一列的值正读与反读相同，则称该行或该列为回文（palindromic）。  
你可以将任意数量的单元格（cell）的值从 `0` 翻转（flip）为 `1`，或从 `1` 翻转为 `0`。  
返回使 **所有行和所有列均为回文** 且 **矩阵中 `1` 的总数能被 `4` 整除** 所需的最少翻转次数。

## 示例

### 示例 1
**输入**  
```json
grid = [[1,0,0],
        [0,1,0],
        [0,0,1]]
```
**输出**  
```
3
```
**解释**：

（此处填写解释）

### 示例 2
**输入**  
```json
grid = [[0,1],
        [0,1],
        [0,0]]
```
**输出**  
```
2
```
**解释**：

（此处填写解释）

### 示例 3
**输入**  
```json
grid = [[1],
        [1]]
```
**输出**  
```
2
```
**解释**：

（此处填写解释）

## 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m × n ≤ 2 × 10^5`
- `0 ≤ grid[i][j] ≤ 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个格子都当成可以自由翻转的开关**，枚举所有可能的翻转组合，检查翻完以后每一行、每一列是否都是回文，并且 1 的总数能否被 4 整除。  

- **数据结构**：我们只需要一个二维数组 `grid` 来保存原始的 0/1。  
- **生活化类比**：把每个格子想象成一盏灯，开（1）或关（0）。暴力解相当于把所有灯的开关全摆出来，尝试每一种开关状态（所有灯全开、全关、或任意混合）。  
- **为什么正确**：因为我们枚举了**所有**可能的翻转方式，必然能找到最少翻转次数的那一种。  

显然，这种方法在任何稍大一点的输入上都会超时。  
假设矩阵有 `m·n` 个格子，翻转与否各有两种选择，所有可能的状态数是 `2^(m·n)`。即使 `m·n = 20`（仅 20 格子），也要检查 `2^20 ≈ 10⁶` 种；而题目里 `m·n` 可以达到 `2·10⁵`，根本不可能穷举。

#### 代码（Python）

```python
import itertools
from copy import deepcopy

def min_flips_brute(grid):
    """
    暴力搜索：遍历所有 2^(m*n) 种翻转方式，返回满足条件的最小翻转次数。
    仅用于演示思路，实际数据规模会直接炸掉。
    """
    m, n = len(grid), len(grid[0])
    best = float('inf')

    # 把二维坐标映射成一维序号，方便使用 itertools.product
    cells = [(i, j) for i in range(m) for j in range(n)]

    # product 会产生 (0,1) 的所有组合，0 代表不翻，1 代表翻
    for bits in itertools.product([0, 1], repeat=m * n):
        # 复制一份原始矩阵
        cur = deepcopy(grid)
        flips = 0
        for bit, (x, y) in zip(bits, cells):
            if bit:                      # 需要翻转
                cur[x][y] ^= 1           # 0<->1
                flips += 1

        # 检查每行是否回文
        ok = True
        for row in cur:
            if row != row[::-1]:
                ok = False
                break
        # 检查每列是否回文
        if ok:
            for j in range(n):
                col = [cur[i][j] for i in range(m)]
                if col != col[::-1]:
                    ok = False
                    break

        # 检查 1 的总数是否能被 4 整除
        if ok and sum(sum(r) for r in cur) % 4 == 0:
            best = min(best, flips)

    return best if best != float('inf') else -1
```

> **关键行中文注释**已经写在代码里，帮助你对每一步的意义有清晰认识。

#### 复杂度  

- **时间复杂度**：`O( 2^(m·n) * (m·n) )`  
  - 这里的 `2^(m·n)` 是所有翻转组合的数量，`(m·n)` 是检查每一种组合是否满足回文、统计 1 的过程。  
  - 用大白话说，就是“指数级的增长”，随着格子数稍微多一点，时间就会像滚雪球一样飞快变大，根本不可接受。  
- **空间复杂度**：`O(m·n)`  
  - 需要保存原始矩阵和每一次尝试的拷贝。  

显然，暴力解只能用来帮助我们 **理清问题**，而不是实际求解。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们可以发现 **瓶颈** 在于对每个格子单独考虑。  
其实，**行回文 + 列回文** 对格子的约束是可以成对、成组地表示的。  

考虑一个格子 `(x, y)`，它在行、列的镜像位置分别是：

| 位置 | 坐标 | 解释 |
|------|------|------|
| 原格子 | `(x, y)` | 左上 |
| 同行镜像 | `(x, n-1-y)` | 同一行，左右对称 |
| 同列镜像 | `(m-1-x, y)` | 同一列，上下对称 |
| 对角镜像 | `(m-1-x, n-1-y)` | 同时上下左右对称 |

这四个格子必须 **全部相等**，否则对应的行或列就不是回文。  
于是，**所有格子被划分成若干“对称组”**，每组最多 4 个格子：

1. **普通组（4 格子）**：`(x, y) , (x, n-1-y) , (m-1-x, y) , (m-1-x, n-1-y)`  
   - 当 `x < m/2` 且 `y < n/2` 时出现。  
2. **边缘组（2 格子）**：  
   - 当行数为奇数且 `x == m//2`（中间那一行），但列不在中间时，只有左右镜像 `(mid, y)`、`(mid, n-1-y)`。  
   - 当列数为奇数且 `y == n//2`（中间那一列），但行不在中间时，只有上下镜像 `(x, mid)`、`(m-1-x, mid)`。  
3. **中心格子（1 格子）**：当 `m` 与 `n` 同时为奇数时，唯一的 `(mid, mid)`。

> **类比**：把矩阵想象成一面镜子，四个对称格子就像四面镜子里看到的同一张脸，必须保持一致。

---

#### 2.1 组内最小翻转

对于一个普通的 **4‑格子组**，我们可以把它统一成全 0 或全 1：

- 设组内 1 的个数为 `cnt1`。  
- 统一成 **全 0** 需要翻 `cnt1` 次（把所有 1 翻成 0）。  
- 统一成 **全 1** 需要翻 `4 - cnt1` 次（把所有 0 翻成 1）。

显然，**最小翻转次数** 为 `min(cnt1, 4 - cnt1)`，但这只告诉我们“**最少要翻几次**”，并没有决定最终是 0 还是 1。  

为什么要关心最终是 0 还是 1？因为题目还有 **“全部 1 的个数必须能被 4 整除”** 这一全局约束。  
- 统一成 0 → 该组贡献 `0` 个 1。  
- 统一成 1 → 该组贡献 `4` 个 1。  

同理，**2‑格子组**的两种选择分别贡献 `0` 或 `2` 个 1，**1‑格子组**贡献 `0` 或 `1` 个 1。

于是，**每个组都有两个状态**（选 0 还是选 1），每个状态都有：

- **翻转代价**（前面算出的 `cost0`、`cost1`）  
- **产生的 1 的数量**（`add = size * chosen_value`）

---

#### 2.2 把全局约束变成 “模 4” 动态规划

我们只关心 **总的 1 的个数 mod 4** 是否为 0。  
因为每个组加入的 1 的数量都是 **组大小的整数倍**（1、2、4），所以只需要追踪 **当前总和除以 4 的余数**。

设 `dp[r]` 为 **处理完若干组后，使得总 1 数 %4 = r 时的最小翻转次数**。  
初始时只有一种情况：`dp[0] = 0`（什么也不选，翻转次数 0），其它 `dp` 为无限大 `INF`。

遍历所有组，对每个组尝试两种决定（选 0 或选 1）：

```
new_dp[(r + add) % 4] = min( new_dp[(r + add) % 4],
                            dp[r] + cost )
```

其中 `add` 是该选择带来的 1 的数量（0、size），`cost` 是对应的翻转次数。

因为余数只有 0~3 四种，**DP 表的大小固定为 4**，所以时间复杂度是 **线性**（每个格子只被访问常数次），空间复杂度是 **O(1)**。

---

#### 2.3 完整算法步骤

1. **遍历矩阵**，只遍历左上四分之一（`i < m//2`、`j < n//2`），收集 **4‑格子组**。  
2. **处理奇数行/列的边缘**：  
   - 若 `m` 为奇数，遍历中间行的左半部分得到 **2‑格子组**（左右镜像）。  
   - 若 `n` 为奇数，遍历中间列的上半部分得到 **2‑格子组**（上下镜像）。  
3. **处理中心格子**（若两者均为奇数）。  
4. 对每个组执行 **DP 更新**（上面公式）。  
5. 最终答案即 `dp[0]`（使总 1 数 %4 = 0 的最小翻转次数）。

---

#### 代码（Python）

```python
from typing import List

INF = 10 ** 18   # 足够大的数，表示“不可能”

def minFlips(grid: List[List[int]]) -> int:
    """
    最优解：把矩阵划分为对称组，用大小为 4 的 DP 求最小翻转次数，使
    1 的总数 % 4 == 0 且所有行列都是回文。
    """
    m, n = len(grid), len(grid[0])
    dp = [0, INF, INF, INF]          # dp[r] = 最小翻转次数，使得当前 1 数 %4 == r

    # ---------- 1. 处理普通的 4 格子组 ----------
    for i in range(m // 2):
        for j in range(n // 2):
            cells = [
                grid[i][j],
                grid[i][n - 1 - j],
                grid[m - 1 - i][j],
                grid[m - 1 - i][n - 1 - j],
            ]
            cnt1 = sum(cells)                 # 组内 1 的个数
            size = 4
            # 选 0：全部变成 0，翻 cnt1 次，贡献 0 个 1
            cost0 = cnt1
            add0 = 0
            # 选 1：全部变成 1，翻 (4 - cnt1) 次，贡献 4 个 1
            cost1 = size - cnt1
            add1 = size

            # DP 更新（两种选择各自尝试）
            new_dp = [INF, INF, INF, INF]
            for r in range(4):
                if dp[r] == INF:
                    continue
                # 选 0
                nr = (r + add0) % 4
                new_dp[nr] = min(new_dp[nr], dp[r] + cost0)
                # 选 1
                nr = (r + add1) % 4
                new_dp[nr] = min(new_dp[nr], dp[r] + cost1)
            dp = new_dp

    # ---------- 2. 处理横向的 2 格子组（中间行） ----------
    if m % 2 == 1:          # 有中间那一行
        mid = m // 2
        for j in range(n // 2):
            a = grid[mid][j]
            b = grid[mid][n - 1 - j]
            cnt1 = a + b
            size = 2
            cost0 = cnt1            # 统一成 0
            add0 = 0
            cost1 = size - cnt1     # 统一成 1
            add1 = size

            new_dp = [INF, INF, INF, INF]
            for r in range(4):
                if dp[r] == INF:
                    continue
                nr = (r + add0) % 4
                new_dp[nr] = min(new_dp[nr], dp[r] + cost0)
                nr = (r + add1) % 4
                new_dp[nr] = min(new_dp[nr], dp[r] + cost1)
            dp = new_dp

    # ---------- 3. 处理纵向的 2 格子组（中间列） ----------
    if n % 2 == 1:          # 有中间那一列
        mid = n // 2
        for i in range(m // 2):
            a = grid[i][mid]
            b = grid[m - 1 - i][mid]
            cnt1 = a + b
            size = 2
            cost0 = cnt1
            add0 = 0
            cost1 = size - cnt1
            add1 = size

            new_dp = [INF, INF, INF, INF]
            for r in range(4):
                if dp[r] == INF:
                    continue
                nr = (r + add0) % 4
                new_dp[nr] = min(new_dp[nr], dp[r] + cost0)
                nr = (r + add1) % 4
                new_dp[nr] = min(new_dp[nr], dp[r] + cost1)
            dp = new_dp

    # ---------- 4. 处理唯一的中心格子 ----------
    if m % 2 == 1 and n % 2 == 1:
        mid = m // 2
        cnt1 = grid[mid][mid]          # 0 或 1
        size = 1
        cost0 = cnt1       # 变成 0 需要翻 1 次（若原来是 1）
        add0 = 0
        cost1 = 1 - cnt1   # 变成 1 需要翻 1 次（若原来是 0）
        add1 = 1

        new_dp = [INF, INF, INF, INF]
        for r in range(4):
            if dp[r] == INF:
                continue
            nr = (r + add0) % 4
            new_dp[nr] = min(new_dp[nr], dp[r] + cost0)
            nr = (r + add1) % 4
            new_dp[nr] = min(new_dp[nr], dp[r] + cost1)
        dp = new_dp

    # dp[0] 即为总 1 数 %4 == 0 时的最小翻转次数
    return dp[0] if dp[0] != INF else -1   # -1 表示无解（理论上不会出现）
```

> **代码解读**  
> - 每一次「组」的处理都只更新 `dp` 长度为 4 的数组，时间恒定。  
> - `INF` 用来表示「当前余数不可达」的状态。  
> - 最后返回 `dp[0]`，因为我们只需要 **余数为 0** 的最小翻转次数。

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 我们遍历矩阵一次，收集每个对称组（每个格子只被计入一次），随后对每个组做常数次的 DP 更新。  
  - 用大白话说，就是“**线性**”，不管矩阵多大，只要格子数在上限 `2·10⁵`，代码都跑得很快。  

- **空间复杂度**：`O(1)`（不计输入矩阵本身）  
  - 只用了长度为 4 的 `dp` 数组和若干常数级的临时变量。  
  - 与格子数量无关，内存占用几乎可以忽略不计。

---

## 心得

- **核心技巧**：**把矩阵的对称约束转化为“对称组”**，再用 **模 4 动态规划** 统一处理全局的 “1 的总数能被 4 整除” 条件。  
- **适用场景**：  
  1. **所有行列都必须回文** 的矩阵/字符串题目（如 “Make Binary Grid Palindromic I/II”）。  
  2. **需要满足全局模数约束**（如 “使数组和能被 k 整除”）时，可把局部决策的“贡献值”映射到模数 DP。  
  3. **对称或镜像约束** 的几何/网格类问题（比如 “对称图形最小修改”）。  
- **一句话总结解题钥匙**：  
  > “把全局约束拆成每个对称组的局部选择，用‘余数 DP’ 把每个组的 0/1 决策串起来。”

---

## 反思

- **第一反应**：看到“所有行列都要回文”，本能想到“每个格子都有对应的镜像格子”。于是快速定位到 **4‑格子对称组**。  
- **最容易踩的坑**：  
  1. **忘记处理奇数行/列的边缘组**，导致某些格子没有被约束，答案会错误。  
  2. **忽视中心格子的特殊性**（只有 1 个格子），它的选择会直接改变 1 的总数的奇偶性，从而影响能否满足 “%4 == 0”。  
  3. **DP 更新时写错余数**，比如 `new_mod = (prev_mod + size) % 4` 写成了 `+1`，会导致最终答案偏差。  
- **下次遇到同类题**，第一步应该：  
  > “先把对称/镜像关系画出来，把格子划分成最小的等价组（大小 1/2/4），再思考每个组的两种可能及它们对全局约束的‘贡献’，最后用模数 DP 把所有组连起来求最小代价”。