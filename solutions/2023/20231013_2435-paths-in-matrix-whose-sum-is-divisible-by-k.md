# #2435. **矩阵路径和能被 K 整除的路径数** / Paths in Matrix Whose Sum Is Divisible by K

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/paths-in-matrix-whose-sum-is-divisible-by-k/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n integer matrix grid and an integer k. You are currently at position (0, 0) and you want to reach position (m - 1, n - 1) moving only down or right.
Return the number of paths where the sum of the elements on the path is divisible by k. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: grid = [[5,2,4],[3,0,5],[0,7,2]], k = 3
Output: 2
Explanation: There are two paths where the sum of the elements on the path is divisible by k.
The first path highlighted in red has a sum of 5 + 2 + 4 + 5 + 2 = 18 which is divisible by 3.
The second path highlighted in blue has a sum of 5 + 3 + 0 + 5 + 2 = 15 which is divisible by 3.
```

**Example 2:**

```
Input: grid = [[0,0]], k = 5
Output: 1
Explanation: The path highlighted in red has a sum of 0 + 0 = 0 which is divisible by 5.
```

**Example 3:**

```
Input: grid = [[7,3,4,9],[2,3,6,2],[2,3,7,0]], k = 1
Output: 10
Explanation: Every integer is divisible by 1 so the sum of the elements on every possible path is divisible by k.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 5 * 104
- 1 <= m * n <= 5 * 104
- 0 <= grid[i][j] <= 100
- 1 <= k <= 50

---

## 题目（中文翻译）

给定一个下标从 0 开始的 `m × n` 整数矩阵（matrix）`grid` 与一个整数 `k`。你当前位于位置 `(0, 0)`，希望仅通过向下或向右移动到达位置 `(m - 1, n - 1)`。  
返回所有路径中，路径上元素之和（sum）能够被 `k` 整除的路径数量。由于答案可能非常大，请返回 `10^9 + 7` 取模（modulo）后的结果。

**示例**

**示例 1**  
```text
Input: grid = [[5,2,4],[3,0,5],[0,7,2]], k = 3
Output: 2
Explanation: 有两条路径满足路径上元素之和能被 k 整除。
第一条用红色标记的路径之和为 5 + 2 + 4 + 5 + 2 = 18，可被 3 整除。
第二条用蓝色标记的路径之和为 5 + 3 + 0 + 5 + 2 = 15，也可被 3 整除。
```

**示例 2**  
```text
Input: grid = [[0,0]], k = 5
Output: 1
Explanation: 唯一的路径（红色标记）之和为 0 + 0 = 0，能够被 5 整除。
```

**示例 3**  
```text
Input: grid = [[7,3,4,9],[2,3,6,2],[2,3,7,0]], k = 1
Output: 10
Explanation: 由于任意整数都能被 1 整除，所有可能的路径之和均满足条件。
```

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 5 * 10^4`
- `1 ≤ m * n ≤ 5 * 10^4`
- `0 ≤ grid[i][j] ≤ 100`
- `1 ≤ k ≤ 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有合法路径**，把每条路径走过的格子里的数字相加，然后判断和是否能被 `k` 整除。  
- **路径的定义**：只能向右或向下走，从左上角 `(0,0)` 到右下角 `(m‑1,n‑1)`。  
- **枚举方式**：可以用深度优先搜索（递归）或回溯把每一步的「向右」或「向下」写成二叉树的分支，遍历整棵树。

> 类比：想象在一张网格纸上，从左上角走到右下角，每走一步都要抉择「向右」还是「向下」，就像在迷宫里不断分叉，所有的分叉组合就是所有可能的路径。

**为什么一定能得到正确答案**  
只要把**所有**合法路径都遍历一遍，就不会漏掉任何一种可能。因此，只要在遍历结束后把满足「路径和 % k == 0」的计数加起来，答案自然正确。

**时间/空间复杂度**  
- 路径总数等价于「从 `m+n-2` 步中挑出 `m-1` 步向下」的组合数，即 `C(m+n-2, m-1)`。这个数随矩阵大小呈指数级增长。  
- **时间复杂度**：`O( C(m+n-2, m-1) )`，可以近似为 `O( 2^{m+n} )`，在最坏情况下会爆炸。  
- **空间复杂度**：递归栈的深度最多 `m+n-2`，即 `O(m+n)`，除此之外只需要常数级的额外空间。

> 大白话：`O(2^{m+n})` 就像把所有可能的走法都列出来，哪怕矩阵只有 20×20，路径数已经超过一千万，根本不可能在电脑里跑完。

#### 代码（Python）

```python
from typing import List

def brute_force(grid: List[List[int]], k: int) -> int:
    MOD = 10**9 + 7
    m, n = len(grid), len(grid[0])
    ans = 0

    def dfs(i: int, j: int, cur_sum: int) -> None:
        """递归遍历所有路径，i,j 为当前所在格子，cur_sum 为到达这里的累计和"""
        nonlocal ans
        cur_sum += grid[i][j]                     # 把当前格子的值加进去

        # 到达右下角，检查是否可被 k 整除
        if i == m - 1 and j == n - 1:
            if cur_sum % k == 0:
                ans = (ans + 1) % MOD
            return

        # 向右走
        if j + 1 < n:
            dfs(i, j + 1, cur_sum)
        # 向下走
        if i + 1 < m:
            dfs(i + 1, j, cur_sum)

    dfs(0, 0, 0)
    return ans
```

> 这段代码只能在非常小的矩阵（如 `2×2`）里跑通，作为「最笨」的思路展示即可。

#### 复杂度

- **时间复杂度**：`O( C(m+n-2, m-1) )`，指数级增长，实际不可接受。  
- **空间复杂度**：`O(m + n)`，递归栈深度。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**：很多不同的路径会在同一个格子上拥有相同的「前缀和的余数」。如果我们把「到达某个格子时，路径和对 `k` 的余数」作为状态记录下来，就可以把相同状态的路径数量合并，从而避免指数级的枚举。

**核心想法：动态规划 + 余数压缩**  

1. **余数是关键**  
   - 题目只关心「和能否被 `k` 整除」，实际数值大小并不重要。  
   - 把每个格子的值先对 `k` 取余（`grid[i][j] % k`），后面只需要在 **余数** 上做加法并再取余。

2. **状态定义**  
   - `dp[i][j][r]`：**到达格子 `(i,j)` 时，路径和除以 `k` 的余数为 `r` 的路径条数**。  
   - `r` 的取值范围是 `0 … k-1`，因为余数永远在这个区间。

3. **状态转移**  
   - 从上方 `(i-1, j)` 或左方 `(i, j-1)` 走到 `(i, j)`，新的余数为  
     `new_r = (old_r + grid[i][j]) % k`。  
   - 因此  
     ```
     dp[i][j][new_r] += dp[i-1][j][old_r]   (if i > 0)
     dp[i][j][new_r] += dp[i][j-1][old_r]   (if j > 0)
     ```
   - 每次加法都要取模 `1e9+7` 防止整数溢出。

4. **初始化**  
   - 起点只有一种路径，余数为 `grid[0][0] % k`：  
     `dp[0][0][grid[0][0] % k] = 1`。

5. **答案**  
   - 目标格子 `(m-1, n-1)` 的余数为 `0` 的计数即为答案：`dp[m-1][n-1][0]`。

6. **空间优化**  
   - 观察到转移只依赖**当前行的左边格子**和**上一行的同列格子**。  
   - 可以把二维 `dp`（`m × n × k`）压缩成 **一行** `dp[col][r]`，遍历矩阵时逐行更新。  
   - 这样空间变为 `O(n * k)`，在 `m·n ≤ 5·10⁴`、`k ≤ 50` 的限制下非常轻量。

> 类比：把每个格子想象成「收银台」，顾客（路径）带着「零钱余数」来到这里。收银台只记下「有多少顾客带着余数 r」而不是每个顾客的具体金额，这样后面再合并时就只需要看余数即可。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def number_of_paths(grid: List[List[int]], k: int) -> int:
    """
    动态规划：dp[col][r] 表示当前遍历到的行中，列为 col、余数为 r 的路径数
    只保留上一行的数据，空间 O(n * k)
    """
    m, n = len(grid), len(grid[0])

    # dp 是一个 n 行，每行 k 个余数计数的二维列表
    dp = [[0] * k for _ in range(n)]

    # 初始化左上角
    first_rem = grid[0][0] % k
    dp[0][first_rem] = 1

    # 先处理第一行（只能从左往右）
    for col in range(1, n):
        cur_val = grid[0][col] % k
        for r in range(k):
            if dp[col - 1][r]:
                new_r = (r + cur_val) % k
                dp[col][new_r] = (dp[col][new_r] + dp[col - 1][r]) % MOD

    # 从第二行开始，逐行向下遍历
    for row in range(1, m):
        # 第一次处理本行的第 0 列，只能从上方下来
        cur_val = grid[row][0] % k
        for r in range(k):
            if dp[0][r]:
                new_r = (r + cur_val) % k
                dp[0][new_r] = (dp[0][new_r] + dp[0][r]) % MOD
        # 注意：这里会把原来的 dp[0][r] 计入自身，等价于 “从上方” 加上 “从左方”（左方不存在）

        # 处理本行其余列，既可以从上方也可以从左方
        for col in range(1, n):
            cur_val = grid[row][col] % k
            # 暂存上方的 dp（因为左边的 dp 在同一次循环里已经被更新）
            up = dp[col][:]          # copy 一份，表示上一行同列的状态
            left = dp[col - 1]       # 已经是本行左侧的状态（已更新）

            # 先把上方的贡献加进来
            for r in range(k):
                if up[r]:
                    new_r = (r + cur_val) % k
                    dp[col][new_r] = (dp[col][new_r] + up[r]) % MOD

            # 再把左侧的贡献加进来
            for r in range(k):
                if left[r]:
                    new_r = (r + cur_val) % k
                    dp[col][new_r] = (dp[col][new_r] + left[r]) % MOD

    # 最右下角的余数为 0 的计数即为答案
    return dp[n - 1][0] % MOD
```

> 代码解释（关键行中文注释）已写在源码里，直接复制即可运行。

#### 复杂度

- **时间复杂度**：`O(m * n * k)`  
  - 每个格子遍历 `k` 个余数两次（来自上、左），总操作数约为 `m·n·k ≤ 5·10⁴·50 = 2.5·10⁶`，在 1 秒内轻松完成。  
  - 与暴力解的指数级 `O(2^{m+n})` 相比，线性乘以 `k` 的增长是可以接受的。

- **空间复杂度**：`O(n * k)`  
  - 只保存当前行的 `n` 列和 `k` 个余数计数，最大约为 `5·10⁴ * 50 = 2.5·10⁶` 个整数（约 20 MB），符合题目限制。

---

## 心得

- **核心技巧**：**把「路径和」压缩成「模 `k` 的余数」并用**三维**动态规划**记录每个余数的路径数**。  
- **适用的题型**（类似思路）  
  1. “路径和可被 `k` 整除” 类似的 **矩阵/网格路径** 计数题。  
  2. “子数组和可被 `k` 整除” 的 **一维前缀和 + 余数计数**（LeetCode 1012）。  
  3. “在图中计数满足某种模约束的路径” 如 **DP + 状态压缩**（如 0‑1 背包的模数版本）。  
- **一句话总结解题钥匙**：  
  > “只关心余数，用 DP 把相同余数的路径合并”。  

---

## 反思

- **第一反应**：直接想到枚举所有路径（DFS），因为题目描述简单，容易想到“走到底算一次”。  
- **最容易踩的坑**  
  1. **忘记对每个格子取余**：直接累加原始数字会导致整数过大且不必要的计算。  
  2. **边界处理**：第一行只能从左边来，第一列只能从上边来，初始化要写对。  
  3. **模运算的顺序**：`(old_r + cur_val) % k` 必须在每次转移时都取模，否则新余数会超出 `[0, k-1]`。  
  4. **答案取模**：题目要求返回 `10⁹+7` 取模的结果，所有加法都要及时 `% MOD`，防止溢出。  
- **下次遇到同类题**：  
  1. **先判断能否用余数压缩**（如果只关心“能被 … 整除”或“满足某模条件”）。  
  2. **设计 DP 状态时，把“余数”放进去**，并检查转移是否只依赖相邻子状态。  
  3. **考虑空间压缩**：是否只需要前一行/前一列的数据。  

祝你玩转动态规划，玩得开心 🚀！