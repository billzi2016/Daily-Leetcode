# #63. 不同路径 II / Unique Paths II

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/unique-paths-ii/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.
Return the number of possible unique paths that the robot can take to reach the bottom-right corner.
The testcases are generated so that the answer will be less than or equal to 2 * 109.

**Examples**

**Example 1:**

```
Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
Explanation: There is one obstacle in the middle of the 3x3 grid above.
There are two ways to reach the bottom-right corner:
1. Right -> Right -> Down -> Down
2. Down -> Down -> Right -> Right
```

**Example 2:**

```
Input: obstacleGrid = [[0,1],[0,0]]
Output: 1
```

**Constraints**

- m == obstacleGrid.length
- n == obstacleGrid[i].length
- 1 <= m, n <= 100
- obstacleGrid[i][j] is 0 or 1.

---

## 题目（中文翻译）

给定一个 `m x n` 的整数矩阵 `grid`（整数数组 grid）。机器人最初位于左上角（即 `grid[0][0]`），尝试移动到右下角（即 `grid[m - 1][n - 1]`）。机器人在任意时刻只能向下（down）或向右（right）移动。

在 `grid` 中，障碍物（obstacle）和空格分别用 `1` 和 `0` 标记。机器人所走的路径不能经过任何障碍格子。

返回机器人到达右下角所能走的不同路径（unique paths）的数量。  
测试用例保证答案不超过 `2 * 10^9`。

**示例 1**  
**输入**: `obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]`  
**输出**: `2`  
**解释**: 上述 3×3 网格的中心有一个障碍物。  
有两条路径可以到达右下角：  
1. 右 → 右 → 下 → 下  
2. 下 → 下 → 右 → 右  

**示例 2**  
**输入**: `obstacleGrid = [[0,1],[0,0]]`  
**输出**: `1`

**约束条件**  
- `m == obstacleGrid.length`  
- `n == obstacleGrid[i].length`  
- `1 <= m, n <= 100`  
- `obstacleGrid[i][j]` 只能是 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把机器人所有可能的移动路径枚举出来，然后把走到终点且不碰到障碍物的路径计数。  
- **数据结构**：可以用一个 **二维列表** 来保存网格 (`obstacleGrid`)。  
- **遍历方式**：从左上角出发，递归地向“右”或“下”两条路走下去。递归的过程就像在一棵二叉树里搜索，每个节点对应当前所在的格子，左子树代表向右走，右子树代表向下走。  
- **障碍处理**：一旦走到的格子是 `1`（障碍），立刻把这条分支剪掉，等同于在字典里查不到对应的单词，直接返回 “不存在”。  

这种方法一定能得到正确答案，因为它遍历了**所有**合法路径，只要路径合法就计数一次。  

#### 代码（Python）  
```python
def uniquePathsWithObstacles_brute(obstacleGrid):
    """
    暴力递归：枚举所有右/下的走法，遇到障碍立刻返回 0
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])

    # 如果起点或终点本身就是障碍，直接返回 0
    if obstacleGrid[0][0] == 1 or obstacleGrid[m-1][n-1] == 1:
        return 0

    def dfs(i, j):
        """返回从 (i, j) 到右下角的合法路径数"""
        # 越界或者走到障碍格子，说明这条路不通
        if i >= m or j >= n or obstacleGrid[i][j] == 1:
            return 0
        # 到达终点，算作一条合法路径
        if i == m - 1 and j == n - 1:
            return 1
        # 向右走 + 向下走，两条分支的路径数相加
        return dfs(i, j + 1) + dfs(i + 1, j)

    return dfs(0, 0)
```

#### 复杂度  
- **时间复杂度**：`O(2^{m+n})`（指数级）  
  - 解释：在没有障碍的情况下，每走一步都有“右”或“下”两种选择，最坏情况下需要遍历所有可能的走法，类似二叉树的节点数会随路径长度呈指数增长。  
- **空间复杂度**：`O(m+n)`（递归栈深度）  
  - 解释：递归调用的最大深度等于从左上到右下的步数，即 `m-1 + n-1`，所以占用的栈空间与网格的行列之和线性相关。

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**大量重复计算**：很多不同的路径会在同一个格子相遇，随后走的子路径完全相同，却被重复求解。  
我们可以把“从起点到某个格子有多少条合法路径”这件事**记下来**，以后再需要时直接取用，这就是**动态规划（Dynamic Programming）**的核心思想。  

**步骤**  

1. **状态定义**  
   - 用 `dp[i][j]` 表示“从左上角 (0,0) 到格子 (i,j) 的唯一合法路径数”。  
   - 如果 `obstacleGrid[i][j] == 1`（有障碍），则 `dp[i][j] = 0`，因为根本走不到这里。  

2. **状态转移**  
   - 对于普通格子（没有障碍），机器人只能从上方或左方走过来，所以  
     `dp[i][j] = dp[i-1][j] + dp[i][j-1]`。  
   - 边界上（第一行或第一列）只能从左或上唯一的方向来，同理把不存在的 `dp` 当作 `0`。  

3. **初始化**  
   - 起点 `(0,0)`：如果它本身是障碍，则答案为 `0`，否则 `dp[0][0] = 1`（只有一种“空”路径）。  
   - 第一行和第一列：遍历时若遇到障碍，后面的格子全部设为 `0`（因为再也走不过去了），否则沿用左/上格子的值。  

4. **空间优化（可选）**  
   - 观察到 `dp[i][j]` 只依赖当前行的左边和上一行同列的值，完全可以把二维数组压缩成**一维数组** `dp[j]`，从左到右遍历更新。这样把空间从 `O(mn)` 降到 `O(n)`。  

下面给出**完整的二维 DP** 实现以及**一维压缩版**，两者思路相同，代码里都有详细中文注释。

#### 代码（Python）  

```python
def uniquePathsWithObstacles(obstacleGrid):
    """
    动态规划：dp[i][j] 表示到达 (i,j) 的路径数，障碍格子 dp 为 0
    时间 O(m*n)，空间 O(m*n)（后面会给出 O(n) 的压缩写法）
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])

    # 创建 dp 表，全部初始化为 0
    dp = [[0] * n for _ in range(m)]

    # 起点处理
    dp[0][0] = 0 if obstacleGrid[0][0] == 1 else 1

    # 第一行：只能从左边来
    for j in range(1, n):
        if obstacleGrid[0][j] == 1:          # 碰到障碍，后面的格子都不可达
            dp[0][j] = 0
        else:
            dp[0][j] = dp[0][j-1]            # 继承左边的路径数

    # 第一列：只能从上边来
    for i in range(1, m):
        if obstacleGrid[i][0] == 1:
            dp[i][0] = 0
        else:
            dp[i][0] = dp[i-1][0]            # 继承上面的路径数

    # 剩余格子：状态转移公式 dp[i][j] = dp[i-1][j] + dp[i][j-1]
    for i in range(1, m):
        for j in range(1, n):
            if obstacleGrid[i][j] == 1:      # 障碍格子直接设为 0
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]

    return dp[m-1][n-1]                      # 右下角的值即答案
```

**空间压缩版（只用一行）**  

```python
def uniquePathsWithObstacles_1D(obstacleGrid):
    """
    使用一维 dp，dp[j] 表示当前行第 j 列的路径数
    只需要 O(n) 的额外空间
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [0] * n

    # 初始化第一行的 dp（相当于遍历 i=0 的过程）
    dp[0] = 0 if obstacleGrid[0][0] == 1 else 1
    for j in range(1, n):
        dp[j] = 0 if obstacleGrid[0][j] == 1 else dp[j-1]

    # 从第二行开始逐行更新 dp
    for i in range(1, m):
        # 先处理第 i 行的第 0 列（只能从上面来）
        dp[0] = 0 if obstacleGrid[i][0] == 1 else dp[0]

        for j in range(1, n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0                     # 障碍格子设为 0
            else:
                dp[j] = dp[j] + dp[j-1]       # 上面(dp[j]) + 左边(dp[j-1])

    return dp[-1]                           # 最右下角的路径数
```

#### 复杂度  
- **时间复杂度**：`O(m * n)` — 只遍历网格一次，`m` 行 `n` 列，每个格子做常数次操作。相比暴力的指数级快了很多。  
- **空间复杂度**：  
  - 二维版：`O(m * n)` — 需要额外的 `dp` 表和原始网格同等大小。  
  - 一维压缩版：`O(n)` — 只保留当前行的状态，空间仅随列数线性增长。  

相较于暴力解，时间从“指数级”降到“线性”，空间也从递归栈的 `O(m+n)` 降到 `O(n)`（或 `O(mn)`），是典型的 **动态规划** 优化。

---

## 心得  

- **核心技巧**：动态规划——把“子问题的答案”记下来，避免重复计算。  
- **适用场景**：  
  1. **路径计数类**（如 `Unique Paths`、`Minimum Path Sum`）。  
  2. **背包类**（如 `01 背包`、`零钱兑换`）。  
  3. **区间或子序列类**（如 `最长递增子序列`、`编辑距离`）。  
- **一句话总结**：**“把每个格子能到达的路径数存起来，遇到障碍就把它清零”。**  

---

## 反思  

- **第一反应**：直接想到递归枚举所有右/下的走法。  
- **最容易踩的坑**：  
  - 起点或终点本身是障碍时要直接返回 0。  
  - 初始化第一行/列时，一旦出现障碍，后面的格子都必须设为 0（因为只能往右或往下，障碍后面的格子再也无法到达）。  
  - 处理大数时要注意 Python 的整数不会溢出，但在其他语言里需要用 `long`。  
- **下次类似题的第一步**：先**写出状态 dp 的定义**（到达某个位置的方案数），再**写出转移方程**，最后**考虑边界（起点、第一行/列）**是否需要特殊处理。