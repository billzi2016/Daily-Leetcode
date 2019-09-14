# #576. 出界路径 / Out of Boundary Paths

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/out-of-boundary-paths/)

---

## 题目（英文原版）

**Description**

There is an m x n grid with a ball. The ball is initially at the position [startRow, startColumn]. You are allowed to move the ball to one of the four adjacent cells in the grid (possibly out of the grid crossing the grid boundary). You can apply at most maxMove moves to the ball.
Given the five integers m, n, maxMove, startRow, startColumn, return the number of paths to move the ball out of the grid boundary. Since the answer can be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: m = 2, n = 2, maxMove = 2, startRow = 0, startColumn = 0
Output: 6
```

**Example 2:**

```
Input: m = 1, n = 3, maxMove = 3, startRow = 0, startColumn = 1
Output: 12
```

**Constraints**

- 1 <= m, n <= 50
- 0 <= maxMove <= 50
- 0 <= startRow < m
- 0 <= startColumn < n

---

## 题目（中文翻译）

有一个 $m \times n$ 的网格（grid），网格中放有一个球（ball）。球最初位于坐标 `[startRow, startColumn]`。在每一步，你可以将球移动到网格中四个相邻单元格（adjacent cells）中的任意一个，也可能会因此越过网格边界（grid boundary）而离开网格。最多可以对球执行 `maxMove` 次移动。

给定整数 `m, n, maxMove, startRow, startColumn`，返回将球移动出网格边界的路径数量。由于答案可能非常大，请返回结果对 $10^9 + 7$ 取模后的值。

**示例 1**  
输入: `m = 2, n = 2, maxMove = 2, startRow = 0, startColumn = 0`  
输出: `6`

**示例 2**  
输入: `m = 1, n = 3, maxMove = 3, startRow = 0, startColumn = 1`  
输出: `12`

**约束条件**  
- $1 \le m, n \le 50$
- $0 \le maxMove \le 50$
- $0 \le startRow < m$
- $0 \le startColumn < n$

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的走法全部枚举出来。  
- **从起点出发**，每走一步都可以向上、下、左、右四个方向中的任意一个移动。  
- **递归**（或回溯）模拟每一步的选择，当球走到网格外时计数 +1。  
- **终止条件**：已经走了 `maxMove` 步仍未出界，或者已经出界（此时不再继续走下去）。

> **数据结构类比**：  
> 递归的调用栈好比一本“走法日记”。每翻一页（一次函数调用）就记录一次当前所在的格子和已经走的步数，等到这本日记写满（`maxMove` 步）或走出边界，就把这页算作一条合法路径。

这种方法一定能得到正确答案，因为它把**所有**可能的路径都遍历了一遍，凡是能出界的路径都会被计数。

#### 代码（Python）

```python
MOD = 10**9 + 7

def outOfBoundaryPaths_bruteforce(m, n, maxMove, startRow, startColumn):
    # 四个方向的增量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(x, y, moves):
        """返回从 (x, y) 开始、还能走 moves 步时，能出界的路径数"""
        # 已经走完所有步数，却仍在格子里 → 这条路不算
        if moves == 0:
            return 0
        total = 0
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 下一步已经越界，合法路径 +1
            if nx < 0 or nx >= m or ny < 0 or ny >= n:
                total += 1
            else:
                # 仍在格子里，继续递归
                total += dfs(nx, ny, moves - 1)
        return total % MOD   # 防止递归深度产生的大数溢出

    return dfs(startRow, startColumn, maxMove) % MOD
```

#### 复杂度

- **时间复杂度**：`O(4^maxMove)`  
  解释：每一步都有 4 种选择，最多走 `maxMove` 步，所以最坏情况下会产生 `4^maxMove` 条路径。  
  当 `maxMove = 50` 时，这个数字天文般大，根本不可接受。

- **空间复杂度**：`O(maxMove)`（递归栈的深度）  
  只需要保存每一层的函数调用信息，最多 `maxMove` 层。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复计算**：同一个格子在相同剩余步数的状态会被递归很多次。例如，从 (0,0) 走两步到 (1,1) 的路径有多条，但我们只需要知道“在还有 `k` 步时，站在 (i,j) 有多少种走法”。这正是**动态规划（DP）**的核心思想——把子问题的答案记下来，下次直接取用。

**关键点**：

1. **状态定义**  
   `dp[step][i][j]` = 在已经走了 `step` 步、且球仍在格子 `(i, j)` 的情况下，有多少种走法。  
   这里的 `step` 从 0 开始，到 `maxMove`。

2. **状态转移**  
   从上一步的状态向四个方向扩展：
   ```
   dp[step+1][nx][ny] += dp[step][i][j]
   ```
   只要 `(nx, ny)` 仍在网格内部，就把当前的路径数加到下一个 step 对应的格子上。

3. **计数出界**  
   当从 `(i, j)` 向某个方向走一步会越界时，这一步本身就构成一条合法路径。  
   因此在每一步的转移过程中，只要发现目标格子超出边界，就把 `dp[step][i][j]` 累加到答案 `ans` 中。

4. **空间优化**  
   注意到 `dp[step+1]` 只依赖 `dp[step]`，不需要保存所有 `step` 的表。  
   用两个二维数组 `cur`（当前步数）和 `nxt`（下一步）交替更新即可，将空间从 `O(maxMove·m·n)` 降到 `O(m·n)`。

5. **取模**  
   题目要求对 `10^9 + 7` 取模，所有加法操作都要在取模后进行，防止整数溢出。

> **类比**：把每一次“球在格子里还能继续走”看成一次“投票”。`cur[i][j]` 保存了“有多少票（路径）站在 (i,j)”。每走一步，所有票向四周传播；如果票走出了围栏（网格边界），就直接记入最终统计。这样我们只需要一次遍历就能得到答案。

#### 代码（Python）

```python
MOD = 10**9 + 7

def outOfBoundaryPaths_dp(m: int, n: int, maxMove: int,
                          startRow: int, startColumn: int) -> int:
    # 方向向量：下、上、右、左
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # cur[i][j] 表示「当前已经走了 step 步，球在 (i,j) 的路径数」
    cur = [[0] * n for _ in range(m)]
    cur[startRow][startColumn] = 1   # 第 0 步，球只在起点

    ans = 0  # 累计所有走出边界的路径数

    for step in range(1, maxMove + 1):
        # nxt 用来存 step 步后的状态，先全部清零
        nxt = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if cur[i][j] == 0:
                    continue        # 这格子此时没有路径，直接跳过

                for dx, dy in dirs:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < m and 0 <= nj < n:
                        # 仍在格子内，累加到下一步的状态
                        nxt[ni][nj] = (nxt[ni][nj] + cur[i][j]) % MOD
                    else:
                        # 越界了，这一步本身就是一条合法路径
                        ans = (ans + cur[i][j]) % MOD

        # 把 nxt 变成下一轮的 cur，继续向前推进
        cur = nxt

    return ans % MOD
```

#### 复杂度

- **时间复杂度**：`O(maxMove * m * n)`  
  解释：外层循环执行 `maxMove` 次，每次遍历整个 `m × n` 的网格，对每个格子检查四个方向。  
  与暴力的 `4^maxMove` 相比，**线性**地随网格大小和步数增长，完全可以接受（最多 `50 × 50 × 50 = 125,000` 次操作）。

- **空间复杂度**：`O(m * n)`  
  只保留当前步和下一步的两个二维数组，每个数组大小为网格的格子数。相比保存所有步的三维 DP，省了很多内存。

---

## 心得

- **核心技巧**：把“每一步的所有可能位置及其路径数”保存下来，利用**动态规划**避免重复计算。  
- **适用的题型**  
  1. “多少种走法可以到达/离开某个状态”——如《路径数目》《不同路径 II》  
  2. “在限定步数内的状态转移”——如《棋盘上的最短路径》《网格中的最大得分》  
  3. “多维状态的逐步更新”——如《矩阵的最小路径和》《单词搜索 II》
- **一句话总结解题钥匙**：**把“路径计数”放进状态表，用 DP 按步迭代，边走边把出界的计数加到答案**。

---

## 反思

- **第一反应**：看到“最多 50 步、网格最多 50×50”，第一感觉是直接 DFS 会爆炸，于是想到“记忆化搜索”或 DP。  
- **最容易踩的坑**  
  1. **忘记取模**：在累加路径数时容易出现整数溢出，必须每一步都 `% MOD`。  
  2. **边界计数遗漏**：从格子向外走一步算一次出界，不能等到下一轮才计数，否则会少算。  
  3. **初始化错误**：`cur[startRow][startColumn]` 必须是 1（表示第 0 步已经在起点），否则会少算第一步的出界路径。  
- **下次类似题的第一步**：先**明确状态（位置 + 已走步数）**，判断是否可以用 DP 记录“在该状态下有多少种方式”。如果可以，就直接写出状态转移公式，再考虑空间压缩。