# #931. 最小下降路径和 / Minimum Falling Path Sum

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-falling-path-sum/)

---

## 题目（英文原版）

**Description**

Given an n x n array of integers matrix, return the minimum sum of any falling path through matrix.
A falling path starts at any element in the first row and chooses the element in the next row that is either directly below or diagonally left/right. Specifically, the next element from position (row, col) will be (row + 1, col - 1), (row + 1, col), or (row + 1, col + 1).

**Examples**

**Example 1:**

```
Input: matrix = [[2,1,3],[6,5,4],[7,8,9]]
Output: 13
Explanation: There are two falling paths with a minimum sum as shown.
```

**Example 2:**

```
Input: matrix = [[-19,57],[-40,-5]]
Output: -59
Explanation: The falling path with a minimum sum is shown.
```

**Constraints**

- n == matrix.length == matrix[i].length
- 1 <= n <= 100
- -100 <= matrix[i][j] <= 100

---

## 题目（中文翻译）

给定一个 `n x n` 的整数数组矩阵（matrix），返回任意下降路径（falling path）在矩阵中的最小和。

下降路径可以从第一行的任意元素开始，然后在下一行选择正下方或左/右对角的元素。具体而言，当前位置为 `(row, col)` 时，下一步可以移动到 `(row + 1, col - 1)`、`(row + 1, col)` 或 `(row + 1, col + 1)`。

**示例 1**  
输入: `matrix = [[2,1,3],[6,5,4],[7,8,9]]`  
输出: `13`  
解释: 如图所示，有两条下降路径的和达到最小值。

**示例 2**  
输入: `matrix = [[-19,57],[-40,-5]]`  
输出: `-59`  
解释: 如图所示，给出了最小和的下降路径。

**约束条件**
- `n == matrix.length == matrix[i].length`
- `1 <= n <= 100`
- `-100 <= matrix[i][j] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的「下落路径」都枚举一遍，然后把每条路径的元素和算出来，取最小值。

- **数据结构**：我们只需要用二维列表 `matrix` 本身（相当于一张表格），以及一个一维列表 `path_sum` 暂存当前路径的累计和。可以把 `path_sum` 想成「背包」里装的重量，总是把已经走过的数值加进去。
- **为什么正确**：题目要求「任意从第一行的任意位置出发，向下走，每一步可以向左下、正下、右下」，枚举所有合法的走法自然能得到所有可能的路径，取最小和自然就是答案。
- **时间/空间复杂度**：  
  - 每一行有 `n` 列，下一行可以往左/中/右三条路走。完整的递归树深度是 `n`，每层分叉最多 3，最坏情况下会产生 `3^(n-1)` 条路径（第一行选哪个列已经算在 `n` 里了）。所以时间复杂度是 **指数级**，记作 `O(3^{n})`，这在 `n=100` 时根本不可接受。  
  - 递归过程中我们只需要保存当前走到的行号、列号以及累计和，使用的额外空间是 `O(n)`（递归栈深度最多 `n`）。

#### 代码（Python）

```python
from typing import List

def min_falling_path_sum_brute(matrix: List[List[int]]) -> int:
    n = len(matrix)

    # 深度优先搜索所有路径
    def dfs(row: int, col: int, cur_sum: int) -> int:
        # 到达最后一行，返回这条路径的总和
        if row == n - 1:
            return cur_sum + matrix[row][col]

        # 记录从当前格子往下三种合法走法的最小和
        best = float('inf')
        for dcol in (-1, 0, 1):                 # 左下、正下、右下
            ncol = col + dcol
            if 0 <= ncol < n:                   # 不能走出矩阵边界
                # 递归求子路径的最小和
                candidate = dfs(row + 1, ncol, cur_sum + matrix[row][col])
                best = min(best, candidate)
        return best

    # 从第一行的每一列尝试出发，取最小值
    answer = float('inf')
    for start_col in range(n):
        answer = min(answer, dfs(0, start_col, 0))
    return answer
```

> **代码说明**  
> - `dfs` 是一个递归函数，`row`、`col` 表示当前所在的格子，`cur_sum` 是已经累加的和。  
> - 当走到最后一行时，只需要把最后一个格子的值加进去返回。  
> - `for dcol in (-1, 0, 1)` 用来遍历左下、正下、右下三条可能的路线。  
> - 边界检查 `0 <= ncol < n` 防止「走出矩阵」的错误。

#### 复杂度

- **时间复杂度**：`O(3^{n})` —— 每走一层有最多 3 条分支，深度是 `n`，所以整体是指数级，实际运行会非常慢。  
- **空间复杂度**：`O(n)` —— 递归栈的最大深度是 `n`，再加上一点常数空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**大量的重复计算**是导致慢的根本原因。比如在不同的起点出发时，很多子路径会在中间某一行的同一列相遇，随后它们的后续计算完全相同，却被重复求了一遍。

**动态规划（Dynamic Programming，DP）**的核心思想正是「把子问题的答案记下来，后面需要时直接拿来用」，从而避免重复。

我们可以自底向上（从最后一行往上）或自顶向下（从第一行往下）地填表。这里用 **自底向上**：

1. **状态定义**  
   `dp[i][j]` 表示「从格子 `(i, j)` 出发，走到矩阵底部的最小路径和」。
2. **状态转移**  
   - 从 `(i, j)` 往下只能走到三格：`(i+1, j-1)`、`(i+1, j)`、`(i+1, j+1)`（注意边界）。  
   - 所以 `dp[i][j] = matrix[i][j] + min(dp[i+1][j-1], dp[i+1][j], dp[i+1][j+1])`，取三者中的最小值再加上当前格子的数值。
3. **初始化**  
   最底层的 `dp[n-1][j]` 没有往下走的选择，直接等于 `matrix[n-1][j]` 本身。
4. **答案**  
   题目要求「从第一行的任意列出发」，因此答案是 `min(dp[0][j])`（第一行的最小值）。

**空间优化**  
观察到每一行的 `dp` 只依赖下一行的值，所以不必保存完整的 `n×n` 表，只需要两个一维数组交替使用，甚至可以在原矩阵上直接改写，**原地 DP**。

下面给出两种实现方式：

- **方式 A**：使用额外的 `dp` 矩阵（更直观，适合教学）。
- **方式 B**：在原矩阵上原地更新（节省空间）。

#### 代码（Python）

**方式 A：额外矩阵版**

```python
from typing import List

def min_falling_path_sum_dp(matrix: List[List[int]]) -> int:
    n = len(matrix)
    # dp[i][j] 表示从 (i, j) 到最底层的最小路径和
    dp = [[0] * n for _ in range(n)]

    # 初始化最后一行
    for j in range(n):
        dp[n - 1][j] = matrix[n - 1][j]

    # 自底向上填表
    for i in range(n - 2, -1, -1):               # 从倒数第二行往上遍历
        for j in range(n):
            # 取左下、正下、右下三格的最小值，注意边界
            down_left  = dp[i + 1][j - 1] if j - 1 >= 0 else float('inf')
            down_mid   = dp[i + 1][j]
            down_right = dp[i + 1][j + 1] if j + 1 < n else float('inf')
            dp[i][j] = matrix[i][j] + min(down_left, down_mid, down_right)

    # 第一行的最小值即为答案
    return min(dp[0])
```

**方式 B：原地修改版（空间 O(1)）**

```python
from typing import List

def min_falling_path_sum_dp_inplace(matrix: List[List[int]]) -> int:
    n = len(matrix)

    # 从倒数第二行往上逐行更新
    for i in range(n - 2, -1, -1):
        for j in range(n):
            # 取左下、正下、右下三格的最小值（已被更新为子路径最小和）
            left  = matrix[i + 1][j - 1] if j - 1 >= 0 else float('inf')
            mid   = matrix[i + 1][j]
            right = matrix[i + 1][j + 1] if j + 1 < n else float('inf')
            matrix[i][j] += min(left, mid, right)   # 直接把最小和写回原表

    # 处理完后，第一行已经是「从该位置到底部的最小和」
    return min(matrix[0])
```

> **代码要点**  
> - `float('inf')` 表示「正无穷」，用于把非法的左/右下格子排除在 `min` 之外。  
> - `for i in range(n - 2, -1, -1)` 是「从倒数第二行往上」的写法，`-1` 是 Python 的闭区间写法，确保遍历到第 0 行。  
> - 原地版的好处是只用了常数级额外空间（只需要几个临时变量），适合面试中强调「空间优化」的场景。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 我们遍历了矩阵的每一个格子一次（`n` 行 × `n` 列），每次只做常数次比较和加法。相比暴力的指数级，这已经快得多。  
- **空间复杂度**：  
  - 方式 A：`O(n²)`（额外的 `dp` 矩阵）。  
  - 方式 B：`O(1)`（在原矩阵上就地修改，只用常数级临时变量）。  
  对于本题的 `n ≤ 100`，两者都能轻松通过，但原地版展示了「空间优化」的思路。

---

## 心得

- **核心技巧**：动态规划 + 状态转移（每个格子只依赖下一行的三格）。  
- **适用的题型**  
  1. 任何「从上往下」或「从左往右」只能向相邻几格移动的最小/最大路径问题（如「Minimum Path Sum」）。  
  2. 「棋盘上骑士/国王最短路径」等需要「局部最优决定」的网格 DP。  
  3. 「斜坡上滑雪」之类的「单调栈」或「DP」问题（思路类似，只是转移方式不同）。  
- **一句话总结解题钥匙**：**把“从当前格子往下的最优子路径”记下来，逐行累加，最后在第一行取最小**。

---

## 反思

- **第一反应**：直接想到「遍历所有可能的路径」——暴力搜索。因为对「路径」的概念最直观。  
- **最容易踩的坑**  
  1. **边界处理**：左下或右下可能越界，需要用 `float('inf')` 或额外判断排除。  
  2. **负数**：矩阵里可以有负数，不能用「只取正数」的技巧，必须真正比较大小。  
  3. **原地修改时覆盖**：如果不从底向上更新，会把本应保留的原始值覆盖，导致错误。  
- **下次遇到同类题**：第一步先**画出状态转移图**，明确「每个位置的最优子结构」是什么，再决定是自顶向下递归加记忆化，还是自底向上 DP。这样能快速摆脱暴力思路，直接进入高效解法。