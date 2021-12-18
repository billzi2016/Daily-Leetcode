# #1594. 矩阵中的最大非负乘积 / Maximum Non Negative Product in a Matrix

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-non-negative-product-in-a-matrix/)

---

## 题目（英文原版）

**Description**

You are given a m x n matrix grid. Initially, you are located at the top-left corner (0, 0), and in each step, you can only move right or down in the matrix.
Among all possible paths starting from the top-left corner (0, 0) and ending in the bottom-right corner (m - 1, n - 1), find the path with the maximum non-negative product. The product of a path is the product of all integers in the grid cells visited along the path.
Return the maximum non-negative product modulo 109 + 7. If the maximum product is negative, return -1.
Notice that the modulo is performed after getting the maximum product.

**Examples**

**Example 1:**

```
Input: grid = [[-1,-2,-3],[-2,-3,-3],[-3,-3,-2]]
Output: -1
Explanation: It is not possible to get non-negative product in the path from (0, 0) to (2, 2), so return -1.
```

**Example 2:**

```
Input: grid = [[1,-2,1],[1,-2,1],[3,-4,1]]
Output: 8
Explanation: Maximum non-negative product is shown (1 * 1 * -2 * -4 * 1 = 8).
```

**Example 3:**

```
Input: grid = [[1,3],[0,-4]]
Output: 0
Explanation: Maximum non-negative product is shown (1 * 0 * -4 = 0).
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 15
- -4 <= grid[i][j] <= 4

---

## 题目（中文翻译）

你得到一个 `m x n` 的矩阵 `grid`（网格）。一开始位于左上角 `(0, 0)`，每一步只能向右或向下移动。

在所有从左上角 `(0, 0)` 到右下角 `(m - 1, n - 1)` 的可能路径（path）中，找到乘积（product）非负且最大的那条路径。路径的乘积是路径上所有访问到的格子中的整数的乘积。

返回最大非负乘积对 `10^9 + 7` 取模后的结果。如果最大的乘积是负数，则返回 `-1`。注意，取模操作在求得最大乘积之后再进行。

**示例 1**  
**输入**: `grid = [[-1,-2,-3],[-2,-3,-3],[-3,-3,-2]]`  
**输出**: `-1`  
**解释**: 无法得到非负乘积的路径，从 `(0, 0)` 到 `(2, 2)`，因此返回 `-1`。

**示例 2**  
**输入**: `grid = [[1,-2,1],[1,-2,1],[3,-4,1]]`  
**输出**: `8`  
**解释**: 最大非负乘积为 `1 * 1 * -2 * -4 * 1 = 8`。

**示例 3**  
**输入**: `grid = [[1,3],[0,-4]]`  
**输出**: `0`  
**解释**: 最大非负乘积为 `1 * 0 * -4 = 0`。

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 15`  
- `-4 <= grid[i][j] <= 4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有合法路径都枚举出来**，然后把每条路径上所有格子的数相乘，记录下最大的**非负**乘积。  

- **数据结构**：我们只需要一个二维列表 `grid`（题目已经给出）和一个列表 `path` 用来暂存当前走过的格子里的数值。  
- **生活化类比**：把矩阵想象成一张城市地图，左上角是起点，右下角是终点，只能向“右”或“下”走。暴力解就像把所有可能的行走路线都写在纸上，再一个一个算出每条路线的“总费用”（这里是乘积），挑出最大的非负值。  
- **为什么正确**：因为我们真的遍历了**所有**从左上到右下的路径，最大的非负乘积必然在这些遍历的结果里出现，所以答案一定被找到。  

> 注意：矩阵大小上限是 `15 × 15`，路径数为 `C(m+n-2, m-1)`（组合数），在最坏情况下约为 `C(28,14) ≈ 4·10⁷`，对 Python 来说已经很慢了，但对于“暴力思路”演示足够。

#### 代码（Python）

```python
from typing import List

def maxProductPath_bruteforce(grid: List[List[int]]) -> int:
    MOD = 10**9 + 7
    m, n = len(grid), len(grid[0])
    best = -1                     # 记录当前最大的非负乘积

    def dfs(i: int, j: int, prod: int) -> None:
        """深度优先搜索所有路径，i、j 为当前坐标，prod 为到达此格的乘积"""
        nonlocal best
        prod *= grid[i][j]        # 把当前格子的数加入乘积

        # 到达右下角，检查是否为非负并更新答案
        if i == m - 1 and j == n - 1:
            if prod >= 0:
                best = max(best, prod)
            return

        # 只能向右或向下继续
        if i + 1 < m:               # 向下走
            dfs(i + 1, j, prod)
        if j + 1 < n:               # 向右走
            dfs(i, j + 1, prod)

    dfs(0, 0, 1)                    # 从左上角开始，乘积先设为 1（相乘的中性元）
    return best % MOD if best != -1 else -1
```

> **代码要点**  
> - `nonlocal best` 让内部函数能够修改外层变量。  
> - 每进入一个格子就把它的数乘进当前乘积 `prod`。  
> - 到达终点后，只在乘积非负时才更新 `best`。  

#### 复杂度  

- **时间复杂度**：`O(2^{m+n})`（指数级）。  
  - 直观解释：每走一步都有“向右”或“向下”两种选择，路径长度大约是 `m+n-2` 步，所有组合大约是 `2^{m+n}`，所以运行时间会随矩阵尺寸快速增长。  
- **空间复杂度**：`O(m+n)`（递归栈的深度）。  
  - 只需要保存递归调用的路径信息，最深的递归层数是走到右下角的步数，即 `m+n-2`，所以占用的额外内存与矩阵尺寸线性相关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**：很多不同的路径会在同一个格子相交，而我们每次都重新从起点算到这里的乘积。  
要想去掉这些冗余，就需要**把“到达某格子时可以得到的所有乘积信息”保存下来**，后面的路径只需要基于这些已经算好的信息继续前进，这正是**动态规划**的核心思想。

**关键难点**：乘积会出现负数。负数乘以负数会变成正数，负数乘以正数仍是负数。因此，仅仅记录“最大乘积”是不够的，还必须记录“最小乘积”。  

我们在每个格子维护两个数：

| 记号 | 含义 |
|------|------|
| `max_dp[i][j]` | 从起点走到 `(i,j)` 所能得到的 **最大** 乘积 |
| `min_dp[i][j]` | 从起点走到 `(i,j)` 所能得到的 **最小** 乘积（最负的） |

有了这对数值，转移公式非常直观：

- 若当前格子的值 `val` 为正数，则  
  - 最大乘积 = `val * max(previous max)`  
  - 最小乘积 = `val * min(previous min)`
- 若 `val` 为负数，则正负会互换：  
  - 最大乘积 = `val * min(previous min)`（负数 * 负数 = 正数）  
  - 最小乘积 = `val * max(previous max)`（负数 * 正数 = 负数）

`previous` 可以是 **左边** 或 **上边** 两个来源，因为只能向右或向下走。我们把左、上两条路径的 `max`、`min` 分别算出四个候选值，取其中的最大/最小即可。

**边界**：左上角 `(0,0)` 的 `max` 与 `min` 都等于 `grid[0][0]` 本身，因为它是唯一的起点。

**空间优化**：只需要保留前一行的信息即可，使用一维数组 `max_dp`、`min_dp`（长度 `n`）在遍历每一行时逐列更新，空间降到 `O(n)`。

**最终答案**：遍历完最后一个格子 `(m-1,n-1)`，若 `max_dp[-1]` 为负数说明所有路径乘积都是负的，返回 `-1`；否则返回 `max_dp[-1] % MOD`（先取最大乘积再取模，防止负数被错误地模掉）。

#### 代码（Python）

```python
from typing import List

def maxProductPath(grid: List[List[int]]) -> int:
    MOD = 10**9 + 7
    m, n = len(grid), len(grid[0])

    # 初始化第一行的 max/min，随后会逐行覆盖
    max_dp = [0] * n   # 存放当前行每列的最大乘积
    min_dp = [0] * n   # 存放当前行每列的最小乘积

    for i in range(m):
        for j in range(n):
            val = grid[i][j]

            if i == 0 and j == 0:                # 起点
                max_dp[j] = min_dp[j] = val
                continue

            # 记录来自上方和左方的四个候选值
            candidates_max = []
            candidates_min = []

            # 来自上方 (i-1, j)
            if i > 0:
                up_max, up_min = max_dp[j], min_dp[j]   # 上一行同列的值
                if val >= 0:
                    candidates_max.append(up_max * val)
                    candidates_min.append(up_min * val)
                else:                                   # val < 0，正负互换
                    candidates_max.append(up_min * val)
                    candidates_min.append(up_max * val)

            # 来自左方 (i, j-1)
            if j > 0:
                left_max, left_min = max_dp[j-1], min_dp[j-1]   # 当前行左侧的值
                if val >= 0:
                    candidates_max.append(left_max * val)
                    candidates_min.append(left_min * val)
                else:                                          # val < 0
                    candidates_max.append(left_min * val)
                    candidates_min.append(left_max * val)

            # 取最大/最小
            max_dp[j] = max(candidates_max)
            min_dp[j] = min(candidates_min)

    ans = max_dp[-1]
    return ans % MOD if ans >= 0 else -1
```

> **代码要点说明**  
> 1. `candidates_max / candidates_min` 用来收集“从上方或左方到达当前格子后可能的乘积”。  
> 2. 根据 `val` 的正负决定是否要把 **最大** 与 **最小** 互换。  
> 3. `max_dp[j]` 与 `min_dp[j]` 同时被更新，它们在同一次循环中分别保存当前格子 **最大** 与 **最小** 乘积。  
> 4. 最后 `max_dp[-1]` 即右下角的最大乘积。若它是负数，说明没有非负乘积路径，返回 `-1`；否则对 `10⁹+7` 取模后返回。

#### 复杂度  

- **时间复杂度**：`O(m·n)`（线性）。  
  - 直观解释：我们只遍历矩阵一次，对每个格子做常数次的算术运算（最多 4 次乘法 + 取最大/最小），所以总工作量和格子数量成正比。与暴力解的指数级相比，提升非常明显。  
- **空间复杂度**：`O(n)`（一维 DP）。  
  - 只保留当前行以及左侧格子的最大/最小乘积，额外使用的数组长度等于列数 `n`，而不是整个 `m×n` 矩阵。

---

## 心得

- **核心技巧**：在涉及乘积且数值可能为负时，需要同时维护**最大**和**最小**两种状态，利用负数的“翻转”特性实现动态规划。  
- **适用的题型**  
  1. “最大/最小乘积路径”系列（如本题、LeetCode 1520）。  
  2. 包含负数的“一维最大乘积子数组”问题（LeetCode 152）。  
  3. 需要同时记录两种极值的 DP 题目，如“最大/最小得分路径”。  
- **一句话总结解题钥匙**：**负数会把最大和最小互换，记得把两者一起带上 DP**。

## 反思

- **第一反应**：先想“把所有路径都枚举出来算乘积”，这在概念上最直接，但马上意识到会超时。  
- **最容易踩的坑**  
  - 忘记在负数格子时把 **最大** 与 **最小** 互换，导致结果错误。  
  - 没有处理 `0` 的特殊情况：`0` 会把乘积直接变成 `0`，此时最大/最小都应该是 `0`，代码中自然会产生正确的候选值。  
  - 结果取模的时机错误：必须在得到 **最大非负乘积** 后才取模，不能在 DP 过程中就对每一步取模，否则会丢失负数的比较信息。  
- **下次遇到同类题**：第一步先**思考状态转移**——是否只需要最大值，还是需要最小值（或其他极值），再决定 DP 的维度和更新顺序。这样可以直接从暴力思路跳到高效的 DP。