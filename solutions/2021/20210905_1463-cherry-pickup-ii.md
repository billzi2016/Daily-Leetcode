# #1463. 樱桃采摘 II / Cherry Pickup II

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/cherry-pickup-ii/)

---

## 题目（英文原版）

**Description**

You are given a rows x cols matrix grid representing a field of cherries where grid[i][j] represents the number of cherries that you can collect from the (i, j) cell.
You have two robots that can collect cherries for you:
Return the maximum number of cherries collection using both robots by following the rules below:

**Examples**

**Example 1:**

```
Input: grid = [[3,1,1],[2,5,1],[1,5,5],[2,1,1]]
Output: 24
Explanation: Path of robot #1 and #2 are described in color green and blue respectively.
Cherries taken by Robot #1, (3 + 2 + 5 + 2) = 12.
Cherries taken by Robot #2, (1 + 5 + 5 + 1) = 12.
Total of cherries: 12 + 12 = 24.
```

**Example 2:**

```
Input: grid = [[1,0,0,0,0,0,1],[2,0,0,0,0,3,0],[2,0,9,0,0,0,0],[0,3,0,5,4,0,0],[1,0,2,3,0,0,6]]
Output: 28
Explanation: Path of robot #1 and #2 are described in color green and blue respectively.
Cherries taken by Robot #1, (1 + 9 + 5 + 2) = 17.
Cherries taken by Robot #2, (1 + 3 + 4 + 3) = 11.
Total of cherries: 17 + 11 = 28.
```

**Constraints**

- rows == grid.length
- cols == grid[i].length
- 2 <= rows, cols <= 70
- 0 <= grid[i][j] <= 100

---

## 题目（中文翻译）

给定一个 `rows × cols` 矩阵 `grid`，表示一片樱桃田，其中 `grid[i][j]` 表示你可以从单元格 `(i, j)` 收集的樱桃数量。  
你有两台机器人可以帮助你收集樱桃：

- 两台机器人同时从矩阵的第一行出发，机器人 #1 初始位于列 `0`，机器人 #2 初始位于列 `cols‑1`。  
- 每一步，两台机器人都会向下一行移动，且每台机器人可以向左、向右或保持在同一列，即从 `(i, j)` 移动到 `(i+1, j‑1)`、`(i+1, j)` 或 `(i+1, j+1)`（前提是目标列在矩阵范围内）。  
- 两台机器人可以独立选择移动方向，但**同一时刻两台机器人不能位于同一个单元格**。如果它们恰好落在同一列，则只会收集该单元格中的樱桃一次。  
- 机器人在经过的每个单元格都会收集该格子的所有樱桃。

返回在遵循上述规则的前提下，两台机器人能够收集的樱桃的 **最大总数**。

## 示例

### 示例 1
**输入**  
``` 
grid = [[3,1,1],
        [2,5,1],
        [1,5,5],
        [2,1,1]]
```  
**输出**  
```
24
```  
**解释**  
机器人 #1（绿色路径）收集的樱桃为 `3 + 2 + 5 + 2 = 12`。  
机器人 #2（蓝色路径）收集的樱桃为 `1 + 5 + 5 + 1 = 12`。  
总计 `12 + 12 = 24`。

### 示例 2
**输入**  
``` 
grid = [[1,0,0,0,0,0,1],
        [2,0,0,0,0,3,0],
        [2,0,9,0,0,0,0],
        [0,3,0,5,4,0,0],
        [1,0,2,3,0,0,6]]
```  
**输出**  
```
28
```  
**解释**  
机器人 #1（绿色路径）收集的樱桃为 `1 + 9 + 5 + 2 = 17`。  
机器人 #2（蓝色路径）收集的樱桃为 `1 + 3 + 4 + 3 = 11`。  
总计 `17 + 11 = 28`。

## 约束条件
- `rows == grid.length`
- `cols == grid[i].length`
- `2 ≤ rows, cols ≤ 70`
- `0 ≤ grid[i][j] ≤ 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把所有可能的机器人移动路径都列举一遍**，然后挑出能收集到最多樱桃的那条。  

- **机器人怎么走**：每一次机器人只能向下一行移动，列号可以保持不变、左移一列或右移一列（共 3 种选择）。  
- **两只机器人**：每一步都有 `3 × 3 = 9` 种组合（因为两只机器人各自有 3 种选择），它们可以独立走，也可以碰到同一个格子。若两只机器人落在同一格子，只算一次樱桃。  
- **数据结构类比**：我们可以把每一次“走一步”看成一次“查询字典”，字典的 **key** 是当前所在的行号、机器人1的列、机器人2的列，**value** 是到达这里已经收集的樱桃总数。这里的字典相当于**记忆化搜索**（Memoization），它的作用类似于“查字典”，帮助我们避免重复计算相同状态。  

因为每一步都有 9 种分支，深度为 `rows`（最多 70），所以总的搜索树规模是 `9^(rows-1)`，这在实际里是天文数字，根本跑不完。但 **思路是对的**：只要把所有合法的路径都遍历一遍，就一定能得到最大值。  

#### 代码（Python）  

```python
from functools import lru_cache
from typing import List

def cherryPickup(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    # @lru_cache 会把已经算过的 (r, c1, c2) 记下来，类似查字典
    @lru_cache(None)
    def dfs(r: int, c1: int, c2: int) -> int:
        # 边界检查：列号超出范围的状态直接返回 -inf（不合法）
        if not (0 <= c1 < cols and 0 <= c2 < cols):
            return -10**9

        # 当前格子能收集的樱桃（如果同格子只算一次）
        cur = grid[r][c1]
        if c1 != c2:               # 两机器人不在同一格子时，加上机器人2的樱桃
            cur += grid[r][c2]

        # 已经到了最后一行，返回当前收集的樱桃数
        if r == rows - 1:
            return cur

        # 下面 9 种移动组合，递归求子问题的最大值
        nxt = 0
        for dc1 in (-1, 0, 1):
            for dc2 in (-1, 0, 1):
                nxt = max(nxt, dfs(r + 1, c1 + dc1, c2 + dc2))
        return cur + nxt

    # 两机器人初始分别在最上面一行的最左和最右列
    return dfs(0, 0, cols - 1)
```

> **关键点注释**  
> - `@lru_cache(None)`：把函数的返回值缓存起来，等价于“记忆化搜索”。  
> - `if not (0 <= c1 < cols and 0 <= c2 < cols)`: 超出边界的状态直接返回一个很小的负数，保证它不会被选为最大值。  
> - `cur = grid[r][c1]; if c1 != c2: cur += grid[r][c2]`: 防止同一格子被双倍计数。  

#### 复杂度  

- **时间复杂度**：`O(9^{rows})`（指数级）。  
  - 大白话：每走到下一行，分支数会乘以 9，行数是 70，9 的 70 次方是一个天文数字，根本跑不完。  
- **空间复杂度**：`O(rows * cols * cols)` 用于缓存（最坏情况下会缓存所有合法状态），大约是 `70 * 70 * 70 ≈ 3.4e5`，在内存上还能接受。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**状态重复**是主要的浪费点：不同的递归路径会到达相同的 `(row, col1, col2)`，只要把这些状态的最优结果记下来，就不必重复计算。  

**瓶颈**在于我们仍然用递归去“遍历”所有分支，虽然用了记忆化，但仍然要遍历 `9` 种转移，导致时间仍是 `O(rows * cols^2 * 9)`，这已经是可接受的（`rows, cols ≤ 70`），但我们可以把它写成**自底向上的动态规划（DP）**，思路更直观，也更容易做空间优化。  

**核心概念——三维 DP**  

- 定义 `dp[i][j][k]` 为：**从第 i 行开始，机器人 1 在列 j，机器人 2 在列 k 时，能够收集到的最大樱桃数**（包括第 i 行本身）。  
- 状态转移：机器人在第 i 行只能向第 i+1 行的相邻列移动（-1、0、+1），因此  

```
dp[i][j][k] = grid[i][j] + (grid[i][k] if j != k else 0) 
              + max( dp[i+1][j+dj][k+dk] )   # dj, dk ∈ {-1,0,1}
```

- 边界：当 `i == rows-1`（最后一行）时，只收集当前格子的樱桃，不再向下移动。  

**类比**：把 `dp` 想象成一个**立体的记事本**，每一页对应一行，每页里有一个二维表格（机器人1列 × 机器人2列），格子里写的是从这里往下的“最优收获”。我们从最后一页往前翻，每翻一页就用下面一页的最优值来填当前页。  

**时间复杂度**  
- 外层遍历 `rows`（最多 70）  
- 内层遍历 `cols × cols`（最多 70×70=4900）  
- 每个状态检查 9 种转移  
- 总体 `O(rows * cols^2 * 9)` ≈ `O(rows * cols^2)`，约 `70 * 4900 ≈ 3.4×10^5` 次运算，完全可以在毫秒级跑完。  

**空间优化**  
- 只需要保存**下一行**的 DP 表格即可，因为转移只依赖 `i+1` 行。  
- 使用两个二维数组交替更新，空间降到 `O(cols^2)`（约 5k），更友好。  

#### 代码（Python）  

```python
from typing import List

def cherryPickup(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    # dp_next 表示第 i+1 行的状态，初始化为最后一行的收获
    dp_next = [[0] * cols for _ in range(cols)]
    for c1 in range(cols):
        for c2 in range(cols):
            # 同一格子只算一次
            dp_next[c1][c2] = grid[rows - 1][c1] + (grid[rows - 1][c2] if c1 != c2 else 0)

    # 自底向上遍历行
    for r in range(rows - 2, -1, -1):          # 从倒数第二行往上走
        dp_cur = [[0] * cols for _ in range(cols)]
        for c1 in range(cols):
            for c2 in range(cols):
                # 当前格子能收集的樱桃（防止重复计数）
                cur = grid[r][c1] + (grid[r][c2] if c1 != c2 else 0)

                # 机器人下一步的 9 种组合，取最大值
                best_next = 0
                for dc1 in (-1, 0, 1):
                    for dc2 in (-1, 0, 1):
                        nc1, nc2 = c1 + dc1, c2 + dc2
                        if 0 <= nc1 < cols and 0 <= nc2 < cols:
                            best_next = max(best_next, dp_next[nc1][nc2])
                dp_cur[c1][c2] = cur + best_next
        dp_next = dp_cur                       # 为上一行准备

    # 初始状态：机器人 1 在左上角 (0,0)，机器人 2 在右上角 (0, cols-1)
    return dp_next[0][cols - 1]
```

> **代码要点**  
> 1. `dp_next` 先用**最后一行**的直接收获初始化。  
> 2. 双层 `for c1 in range(cols)`、`for c2 in range(cols)` 遍历所有列组合。  
> 3. `best_next` 用 9 种合法转移的最大值更新，确保不越界。  
> 4. 每次循环结束后把 `dp_cur` 赋给 `dp_next`，相当于“向上搬了一层”。  

#### 复杂度  

- **时间复杂度**：`O(rows * cols^2)`  
  - 直观解释：我们遍历每一行（最多 70 次），在每行里遍历所有机器人列的组合（最多 70×70=4900），每个组合检查 9 种可能的下一步，总体约 `70 × 4900 × 9 ≈ 3.1×10^6` 次基本操作，几毫秒就能算完。  
- **空间复杂度**：`O(cols^2)`  
  - 只保留当前行和下一行的二维表格（约 5k 整数），相比暴力解的递归栈和全部缓存大幅节省内存。  

---

## 心得  

- **核心技巧**：**二维机器人同步 DP**（三维状态压缩为两维），即把两只机器人的位置一起当作状态来记忆最优子问题。  
- **适用题型**：  
  1. **Cherry Pickup I**（只有一只机器人但需要往返）— 也用 DP 记录行列状态。  
  2. **Maximum Profit in Job Scheduling**（多维状态 DP）— 把多个维度的约束压进状态。  
  3. **Two-Player Game on Grid**（两个人轮流移动）— 常用“双方位置”做 DP。  
- **一句话总结**：**把“两个机器人的位置”一起当作一个状态，用 DP 从下往上填，既避免重复计算，又只用 `O(cols²)` 空间**。  

---

## 反思  

- **第一反应**：看到两只机器人同步移动，立刻想到“枚举所有路径”。这会导致指数级爆炸。  
- **最容易踩的坑**：  
  - **同格子重复计数**：若两机器人恰好落在同一格子，必须只加一次樱桃。忘记会把答案翻倍。  
  - **越界检查**：机器人左移或右移时列号可能超出 `[0, cols-1]`，必须在转移时判断。  
  - **初始化错误**：最后一行的 DP 必须考虑两机器人可能在同一列的情况。  
- **下次类似题的第一步**：先**把状态抽象出来**（本题是行号 + 两列坐标），确认转移只依赖**下一行**或**下一状态**，然后决定是递归记忆化还是自底向上的 DP。这样可以立刻避免指数级搜索，直接进入 DP 方案。