# #2304. 网格中的最小路径费用 / Minimum Path Cost in a Grid

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-path-cost-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n integer matrix grid consisting of distinct integers from 0 to m * n - 1. You can move in this matrix from a cell to any other cell in the next row. That is, if you are in cell (x, y) such that x < m - 1, you can move to any of the cells (x + 1, 0), (x + 1, 1), ..., (x + 1, n - 1). Note that it is not possible to move from cells in the last row.
Each possible move has a cost given by a 0-indexed 2D array moveCost of size (m * n) x n, where moveCost[i][j] is the cost of moving from a cell with value i to a cell in column j of the next row. The cost of moving from cells in the last row of grid can be ignored.
The cost of a path in grid is the sum of all values of cells visited plus the sum of costs of all the moves made. Return the minimum cost of a path that starts from any cell in the first row and ends at any cell in the last row.

**Examples**

**Example 1:**

```
Input: grid = [[5,3],[4,0],[2,1]], moveCost = [[9,8],[1,5],[10,12],[18,6],[2,4],[14,3]]
Output: 17
Explanation: The path with the minimum possible cost is the path 5 -> 0 -> 1.
- The sum of the values of cells visited is 5 + 0 + 1 = 6.
- The cost of moving from 5 to 0 is 3.
- The cost of moving from 0 to 1 is 8.
So the total cost of the path is 6 + 3 + 8 = 17.
```

**Example 2:**

```
Input: grid = [[5,1,2],[4,0,3]], moveCost = [[12,10,15],[20,23,8],[21,7,1],[8,1,13],[9,10,25],[5,3,2]]
Output: 6
Explanation: The path with the minimum possible cost is the path 2 -> 3.
- The sum of the values of cells visited is 2 + 3 = 5.
- The cost of moving from 2 to 3 is 1.
So the total cost of this path is 5 + 1 = 6.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 2 <= m, n <= 50
- grid consists of distinct integers from 0 to m * n - 1.
- moveCost.length == m * n
- moveCost[i].length == n
- 1 <= moveCost[i][j] <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的 `m × n` 整数矩阵 `grid`，其中的整数互不相同，取值范围为 `0` 到 `m * n - 1`。在该矩阵中，你可以从当前单元格移动到下一行的任意单元格。也就是说，如果你位于单元格 `(x, y)` 且 `x < m - 1`，则可以移动到 `(x + 1, 0)`, `(x + 1, 1)`, …, `(x + 1, n - 1)` 中的任意一个。注意，最后一行的单元格无法再向下移动。

每一次可能的移动都有一个费用，由下标从 0 开始的二维数组 `moveCost` 给出，尺寸为 `(m * n) × n`，其中 `moveCost[i][j]` 表示**从值为 `i` 的单元格移动到下一行第 `j` 列单元格的费用**。最后一行的移动费用可以忽略。

一条路径的费用等于所有访问过的单元格的值之和，加上所有移动费用之和。返回从第一行的任意单元格开始、在最后一行的任意单元格结束的路径的**最小费用**。

---

**示例 1**  
``` 
Input: grid = [[5,3],[4,0],[2,1]], moveCost = [[9,8],[1,5],[10,12],[18,6],[2,4],[14,3]]
Output: 17
Explanation: 最小费用的路径是 5 -> 0 -> 1。
- 访问的单元格值之和为 5 + 0 + 1 = 6。
- 从 5 移动到 0 的费用为 3。
- 从 0 移动到 1 的费用为 8。
因此路径的总费用为 6 + 3 + 8 = 17。
```

**示例 2**  
``` 
Input: grid = [[5,1,2],[4,0,3]], moveCost = [[12,10,15],[20,23,8],[21,7,1],[8,1,13],[9,10,25],[5,3,2]]
Output: 6
Explanation: 最小费用的路径是 2 -> 3。
- 访问的单元格值之和为 2 + 3 = 5。
- 从 2 移动到 3 的费用为 1。
所以路径的总费用为 5 + 1 = 6。
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `2 <= m, n <= 50`  
- `grid` 中的整数互不相同，取值范围为 `0` 到 `m * n - 1`。  
- `moveCost.length == m * n`  
- `moveCost[i].length == n`  
- `1 <= moveCost[i][j] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的路径枚举一遍，算出每条路径的花费，最后取最小值。  

- **路径的定义**：从第一行的任意一个格子出发，每一步只能往下一行的任意格子跳。  
- **遍历方式**：可以用深度优先搜索（DFS）或递归，把当前所在的格子坐标 `(r, c)` 记下来，然后尝试跳到下一行的每一个列 `next_c`，递归求子路径的最小花费。  
- **用到的数据结构**：  
  - **列表（list）**：存放 `grid` 与 `moveCost`，类似一本“字典”，`moveCost[i][j]` 就是查“词 i 在第 j 列的页码”。  
  - **递归栈**：系统会自动为每一次函数调用分配一个栈帧，像是把每一步的选择压进“记事本”。  

**为什么正确**：因为我们把**所有**合法的跳法都穷举了，最小的那条自然会被找到。只要递归终止条件（到达最后一行）处理得当，答案必然包含在搜索空间里。

**时间/空间复杂度**（大白话版）  
- 每一行有 `n` 列，必须从每个格子跳到下一行的 **所有** `n` 列。  
- 第 1 行有 `n` 种起点，第 2 行会产生 `n * n` 种路径，第 3 行 `n * n * n`，以此类推。  
- 所以总的路径数是 `n^(m-1)`（`m` 行要跳 `m-1` 次），每条路径要把格子值和移动费用加起来，整体时间复杂度是 **O(n^(m-1))**。  
  - 举个例子：如果 `m=5, n=5`，就要检查 `5^4 = 625` 条路径，规模稍大时就会爆炸。  
- 递归深度最多是 `m`（行数），因此额外的空间复杂度是 **O(m)**（栈空间）。  

> **提示**：暴力解只能用来验证思路或在极小的测试数据上跑通，实际提交会超时。

#### 代码（Python）

```python
from typing import List

def minPathCost_bruteforce(grid: List[List[int]], moveCost: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    ans = float('inf')                     # 用来保存全局最小值

    # dfs(row, col, cur_cost)   cur_cost 包含已经走过的格子值和移动费用
    def dfs(r: int, c: int, cur_cost: int):
        nonlocal ans
        cur_cost += grid[r][c]             # 加上当前格子的值

        # 到达最后一行，更新答案
        if r == m - 1:
            ans = min(ans, cur_cost)
            return

        # 试遍所有下一行的列
        for nxt_c in range(n):
            # 移动费用：从当前格子值 grid[r][c] 到下一行列 nxt_c
            add = moveCost[grid[r][c]][nxt_c]
            dfs(r + 1, nxt_c, cur_cost + add)

    # 从第一行的每个格子开始搜索
    for start_c in range(n):
        dfs(0, start_c, 0)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n^(m-1))`  
  - 解释：每行要尝试 `n` 种跳法，除最后一行外要跳 `m-1` 次，指数级增长。  
- **空间复杂度**：`O(m)`（递归栈深度）  
  - 解释：最多保存 `m` 层函数调用信息，和 `n`、`moveCost` 的大小无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复计算** 是主要的性能瓶颈：同一个格子在不同的路径中会被多次访问，且每次都要重新算一次“从这里到终点的最小费用”。  
我们可以把“从第一行到达每个格子时的最小花费” **记下来**，后面的行只需要参考这些已经算好的最小值，而不必再次遍历所有前面的路径。  

这正是 **动态规划（Dynamic Programming, DP）** 的典型思路：  

1. **状态定义**  
   - `dp[r][c]` = **到达第 `r` 行第 `c` 列的格子时，已付的最小总费用**（包括走过的格子值和移动费用）。  

2. **状态转移**  
   - 要到达 `(r, c)`，只能从上一行的任意列 `k` 跳过来。  
   - 从 `(r-1, k)` 跳到 `(r, c)` 的费用为  
     `dp[r-1][k] + moveCost[grid[r-1][k]][c] + grid[r][c]`  
   - 因此  
     `dp[r][c] = min_{k=0..n-1} ( dp[r-1][k] + moveCost[grid[r-1][k]][c] ) + grid[r][c]`  

3. **初始状态**  
   - 第一行不需要移动费用，直接把格子值记进去：  
     `dp[0][c] = grid[0][c]`  

4. **答案**  
   - 最后一行任意列都可以结束，取最小值：`min(dp[m-1])`  

5. **空间优化**（可选）  
   - 计算第 `r` 行只依赖第 `r-1` 行，所以可以只保留两行数组，甚至只保留一行并在循环里更新。这里为了代码简洁使用两行。  

**关键概念解释**  
- **动态规划**：把大问题拆成子问题，先解决小的子问题（第一行），再一步步往下推。就像爬楼梯，每一步只需要知道上一步的最少花费。  
- **前缀最小**：如果 `n` 较大，直接在每个 `c` 上遍历所有 `k` 会是 `O(m * n^2)`，已经可以接受（`m,n ≤ 50`），不需要更高级的优化。  

#### 代码（Python）

```python
from typing import List

def minPathCost(grid: List[List[int]], moveCost: List[List[int]]) -> int:
    """
    动态规划实现：dp[r][c] 表示到达 (r, c) 时的最小累计费用
    """
    m, n = len(grid), len(grid[0])

    # 第 0 行的费用就是格子本身的值
    dp_prev = [grid[0][c] for c in range(n)]

    # 从第 1 行开始向下计算
    for r in range(1, m):
        dp_cur = [float('inf')] * n          # 本行的结果先设为无穷大
        for c in range(n):                   # 目标列
            # 考虑所有可能的上一列 k
            for k in range(n):
                # 从 (r-1, k) 跳到 (r, c) 的费用
                cost = dp_prev[k] + moveCost[grid[r-1][k]][c]
                if cost < dp_cur[c]:
                    dp_cur[c] = cost
            # 加上当前格子的值
            dp_cur[c] += grid[r][c]
        dp_prev = dp_cur                      # 为下一行准备

    # 最后一行的最小值即为答案
    return min(dp_prev)
```

#### 复杂度  

- **时间复杂度**：`O(m * n^2)`  
  - 解释：外层遍历 `m-1` 行，每行内部两层循环各遍历 `n` 列，等价于 `m * n * n`。在最坏情况下 `50 * 50 * 50 = 125,000` 次运算，完全可以在毫秒级跑完。相比暴力的指数级 `n^(m-1)`，提升巨大。  
- **空间复杂度**：`O(n)`（只保留前一行的 `dp`）  
  - 解释：我们只用两个长度为 `n` 的列表来存放当前行和上一行的最小费用，省去了完整的 `m*n` 表。

---

## 心得  

- **核心技巧**：**动态规划** —— 把“到达每个格子的最小费用”保存下来，避免重复计算。  
- **适用题型**（类似思路可直接套用）：  
  1. **Minimum Path Sum**（只上下左右移动的网格最小路径和）。  
  2. **Minimum Falling Path Sum**（每行只能向左下、正下、右下移动）。  
  3. **Cherry Pickup II**（从两只小鸟分别走到底部的最大樱桃收集）。  
- **解题钥匙**：**把大问题拆成“到达每一格的最小费用”子问题，逐行递推**。

---

## 反思  

- **第一反应**：看到“任意列都可以跳”，立刻想到“枚举所有路径”。这会导致指数级爆炸。  
- **最容易踩的坑**：  
  - **忘记把当前格子的值加进 dp**（只加了 moveCost）。  
  - **移动费用的索引**：`moveCost` 的行索引是格子 **值**，而不是行号，需要 `grid[r-1][k]` 作为索引。  
  - **边界**：`m,n ≥ 2`，但代码仍需处理只有两行的情况（循环仍然有效）。  
- **下次遇到同类题**，第一步应该：**明确状态定义（到达每个位置的最小/最大代价）并写出转移方程**，再判断是否需要空间优化。这样可以直接进入 DP 而不是盲目枚举。