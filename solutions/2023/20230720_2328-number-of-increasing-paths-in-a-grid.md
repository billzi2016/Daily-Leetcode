# #2328. 网格中的递增路径数量 / Number of Increasing Paths in a Grid

> 难度：困难 · 标签：Array、Dynamic Programming、Depth-First Search、Breadth-First Search、Graph、Topological Sort、Memoization、Matrix · [LeetCode 链接](https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid, where you can move from a cell to any adjacent cell in all 4 directions.
Return the number of strictly increasing paths in the grid such that you can start from any cell and end at any cell. Since the answer may be very large, return it modulo 109 + 7.
Two paths are considered different if they do not have exactly the same sequence of visited cells.

**Examples**

**Example 1:**

```
Input: grid = [[1,1],[3,4]]
Output: 8
Explanation: The strictly increasing paths are:
- Paths with length 1: [1], [1], [3], [4].
- Paths with length 2: [1 -> 3], [1 -> 4], [3 -> 4].
- Paths with length 3: [1 -> 3 -> 4].
The total number of paths is 4 + 3 + 1 = 8.
```

**Example 2:**

```
Input: grid = [[1],[2]]
Output: 3
Explanation: The strictly increasing paths are:
- Paths with length 1: [1], [2].
- Paths with length 2: [1 -> 2].
The total number of paths is 2 + 1 = 3.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 105
- 1 <= grid[i][j] <= 105

---

## 题目（中文翻译）

**描述**  
给定一个 `m × n` 的整数矩阵 `grid`（网格），你可以向上下左右四个方向的相邻单元格移动。  
返回网格中 **严格递增路径**（strictly increasing paths）的数量，路径可以从任意单元格开始，也可以在任意单元格结束。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模的结果。  
如果两条路径的访问单元格序列不完全相同，则视为不同的路径。

**示例 1**  
```text
Input: grid = [[1,1],[3,4]]
Output: 8
Explanation: 严格递增路径包括：
- 长度为 1 的路径: [1], [1], [3], [4]。
- 长度为 2 的路径: [1 -> 3], [1 -> 4], [3 -> 4]。
- 长度为 3 的路径: [1 -> 3 -> 4]。
总路径数为 4 + 3 + 1 = 8。
```

**示例 2**  
```text
Input: grid = [[1],[2]]
Output: 3
Explanation: 严格递增路径包括：
- 长度为 1 的路径: [1], [2]。
- 长度为 2 的路径: [1 -> 2]。
总路径数为 2 + 1 = 3。
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 ≤ m, n ≤ 1000`  
- `1 ≤ m * n ≤ 10^5`  
- `1 ≤ grid[i][j] ≤ 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从每个格子出发，深度优先搜索（DFS）所有可能的递增路径**，把每条合法路径计数后求和。  
- **数据结构**：我们只需要一个二维数组 `grid`（相当于一张地图），以及一个四方向的偏移数组 `dirs = [(0,1),(0,-1),(1,0),(-1,0)]`，它像“指南针”，指示可以往哪走。  
- **为什么正确**：DFS 会把每一种走法都尝试一次，只要相邻格子的数值严格变大，就继续前进。遍历完所有起点后，所有合法的递增路径都会被枚举到，自然得到正确答案。  

> **生活化类比**：想象你在一座山脉的格子地图上行走，每一步只能往更高的格子走。暴力解相当于让你从每个格子出发，走遍所有可能的上坡路线，哪怕路线很长、很弯。

#### 代码（Python）

```python
MOD = 10**9 + 7               # 题目要求的取模数

def count_increasing_paths_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    total = 0

    # 深度优先搜索，返回从 (x, y) 开始的所有递增路径数（不含记忆化）
    def dfs(x, y):
        cnt = 1                 # 只走一步（只停在自己这里）算一条合法路径
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] > grid[x][y]:
                cnt = (cnt + dfs(nx, ny)) % MOD
        return cnt

    for i in range(m):
        for j in range(n):
            total = (total + dfs(i, j)) % MOD
    return total
```

> **关键行注释**  
> - `cnt = 1`：路径长度为 1（只包含起点）本身就是一条递增路径。  
> - `if grid[nx][ny] > grid[x][y]`：只能往更大的格子走，保持严格递增。  
> - `cnt = (cnt + dfs(nx, ny)) % MOD`：把从邻居继续走下去得到的所有路径累加进来。

#### 复杂度  

- **时间复杂度**：`O(m * n * 4^L)`（指数级），其中 `L` 是网格中可能的最长递增路径长度。因为每一次递归都要尝试四个方向，且没有任何剪枝或记忆化，搜索树会呈指数增长。  
  - **大白话**：想象每走一步就会分叉成 4 条新路，走 10 步就会有 4ⁱ⁰ 条（约 1,048,576）种走法，显然会炸掉时间限制。  
- **空间复杂度**：`O(L)`，递归栈的深度最多等于最长递增路径的长度 `L`（最坏情况 `m*n`），即最多占用几千层栈帧。

> 暴力解只能用来验证思路或在极小的输入上跑通，实际提交会 TLE（超时）。

---

### 2. 最优解

#### 思路  

从暴力解出发，**慢的地方在于大量重复计算**。  
- 对于两个相邻格子 `A → B`（`grid[B] > grid[A]`），在遍历 `A` 时会递归求 `B` 的所有递增路径；随后在遍历 `B` 时，又会再次递归求 `A` 的路径（如果还有更大的格子可以回到 `A`，虽然值更大导致不会回去，但同样的子问题仍会被多次计算）。  
- **优化目标**：让每个格子只计算一次，然后把结果复用。

这正好符合**动态规划 + 记忆化**（或拓扑排序）的思路：

1. **定义状态**  
   `f(i, j)` 表示**以格子 `(i, j)` 为起点的递增路径总数**（包括长度为 1 的那条路径）。  

2. **状态转移**  
   从 `(i, j)` 可以走向四个更大的相邻格子 `(x, y)`，于是  
   ```
   f(i, j) = 1                                 # 只停在自己这里
           + Σ f(x, y)   （对所有满足 grid[x][y] > grid[i][j] 的邻居）
   ```
   “1” 是必须计数的自己，后面的求和把所有能继续向更大格子走的路径加进来。

3. **递归实现 + 记忆化**  
   用深度优先搜索遍历格子，但在第一次算完 `f(i, j)` 后把结果存入 `dp[i][j]`，后面再需要时直接返回，避免重复递归。

4. **为什么一定能算完**  
   递增路径的值严格变大，**不可能出现环**。因此递归一定会在最大值的格子（只能停下来）终止，整个状态图是一个 **有向无环图（DAG）**，在 DAG 上做记忆化 DP 是安全的。

5. **另一种等价实现：拓扑排序**  
   把所有格子按数值从小到大排序，依次遍历并用前面已经算好的 `f` 更新后继格子。时间上与记忆化 DFS 相同，只是写法不同。

> **类比**：把每个格子想成“山峰”，从低到高的路径只能向更高的山峰走。我们先把所有山峰的高度排好序，从最低的山峰开始统计“从这里出发可以走多少条上坡路线”。一旦算完，就可以直接告诉更高的山峰它们可以从哪些低的山峰“接力”，不必再重新爬低山。

#### 代码（Python）

```python
from functools import lru_cache

MOD = 10**9 + 7
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def countIncreasingPaths(grid):
    """
    使用记忆化 DFS（自底向上 DP）计算答案。
    时间 O(m*n) ，空间 O(m*n)（dp 表 + 递归栈）。
    """
    m, n = len(grid), len(grid[0])

    @lru_cache(None)                     # 自动记忆化：相同坐标只算一次
    def dfs(i, j):
        # 至少有一条路径——只停在自己这里
        total = 1
        for dx, dy in DIRS:
            ni, nj = i + dx, j + dy
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > grid[i][j]:
                total = (total + dfs(ni, nj)) % MOD   # 加上从更大格子继续走的所有路径
        return total

    ans = 0
    for i in range(m):
        for j in range(n):
            ans = (ans + dfs(i, j)) % MOD   # 把每个格子作为起点的路径数累加
    return ans
```

> **关键行解释**  
> - `@lru_cache(None)`：把函数的返回值保存下来，后面再调用同样的 `(i, j)` 时直接返回，避免重复递归。相当于在格子上贴了一张“已经算好的统计表”。  
> - `total = 1`：路径长度为 1（只在自己这格）一定算一条。  
> - `if grid[ni][nj] > grid[i][j]`：只能往更大的格子走，保证严格递增且不产生环。  
> - `ans = (ans + dfs(i, j)) % MOD`：把所有起点的计数加在一起，就是答案。

> **如果不想用装饰器**，也可以手动建立 `dp = [[0]*n for _ in range(m)]`，在 `dfs` 中判断 `dp[i][j] != 0` 再返回。

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 每个格子只会被 `dfs` 计算一次，计算时只检查至多 4 个相邻格子，整体是线性遍历。  
  - 与暴力解相比，从指数级下降到线性级，快了几万倍甚至更多。  

- **空间复杂度**：`O(m * n)`  
  - 记忆化表（`lru_cache` 或手动 `dp`）需要存放每个格子的结果。  
  - 递归栈的最大深度等于网格中递增链的长度，最坏情况下是 `m*n`，但这仍然在题目限制（≤ 10⁵）内可接受。

---

## 心得

- **核心技巧**：把“从某个格子出发的递增路径数”抽象为 DP 状态 `f(i,j)`，利用**严格递增**保证有向无环，进而使用**记忆化 DFS**或**拓扑排序**一次性算完所有状态。  
- **适用的题型**  
  1. **矩阵/网格上的递增/递减路径计数**（如 LeetCode 2328 `Number of Increasing Paths in a Grid`）  
  2. **基于 DAG 的计数问题**（如 “最长递增路径” 329、 “不同路径的数目” 62）  
  3. **需要对每个节点求“从它出发的所有合法子结构”**（如 “在树上统计递增序列” 等）  
- **一句话总结解题钥匙**：  
  > **把每个格子看成“起点”，用 DP 记住它能走出的所有递增路径，利用值的单调性避免环，从而实现一次遍历完成全部计数。**

---

## 反思

- **第一反应**：看到“任意起点、任意终点的递增路径”，立刻想到**深度优先搜索遍历所有路径**，因为递增约束看起来像“只能往更高的山上爬”。  
- **最容易踩的坑**  
  1. **重复计数**：忘记对已经算好的格子做记忆化，会导致指数级时间。  
  2. **模运算位置**：每一步累加后都要取模，否则中间结果会溢出 Python 的整数（虽然 Python 支持大整数，但会极大拖慢速度）。  
  3. **边界条件**：矩阵可能是单行或单列，`dirs` 检查要写完整，防止越界。  
- **下次遇到同类题的第一步**：先**写出 DP 状态 `f(i,j)`**，思考它如何由**更大邻居的状态**转移而来，确认有向无环后再决定使用记忆化 DFS 还是拓扑排序。这样可以一上来就走在最优路线，而不是在暴力搜索的泥潭里打转。