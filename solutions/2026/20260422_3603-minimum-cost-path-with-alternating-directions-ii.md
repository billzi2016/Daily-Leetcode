# #3603. 交替方向的最小费用路径 II / Minimum Cost Path with Alternating Directions II

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-path-with-alternating-directions-ii/)

---

## 题目（英文原版）

**Description**

You are given two integers m and n representing the number of rows and columns of a grid, respectively.
The cost to enter cell (i, j) is defined as (i + 1) * (j + 1).
You are also given a 2D integer array waitCost where waitCost[i][j] defines the cost to wait on that cell.
The path will always begin by entering cell (0, 0) on move 1 and paying the entrance cost.
At each step, you follow an alternating pattern:
Return the minimum total cost required to reach (m - 1, n - 1).

**Examples**

**Example 1:**

```
Input: m = 1, n = 2, waitCost = [[1,2]]
Output: 3
Explanation:
The optimal path is:
Thus, the total cost is 1 + 2 = 3 .
```

**Example 2:**

```
Input: m = 2, n = 2, waitCost = [[3,5],[2,4]]
Output: 9
Explanation:
The optimal path is:
Thus, the total cost is 1 + 2 + 2 + 4 = 9 .
```

**Example 3:**

```
Input: m = 2, n = 3, waitCost = [[6,1,4],[3,2,5]]
Output: 16
Explanation:
The optimal path is:
Thus, the total cost is 1 + 2 + 1 + 4 + 2 + 6 = 16 .
```

**Constraints**

- 1 <= m, n <= 105
- 2 <= m * n <= 105
- waitCost.length == m
- waitCost[0].length == n
- 0 <= waitCost[i][j] <= 105

---

## 题目（中文翻译）

给定两个整数 `m` 和 `n`，分别表示网格的行数和列数。  
进入单元格 `(i, j)` 的费用定义为 `(i + 1) * (j + 1)`。  
同时给定一个二维整数数组 `waitCost`，其中 `waitCost[i][j]` 表示在该单元格上等待的费用。  
路径总是从第 1 步进入单元格 `(0, 0)` 并支付进入费用开始。  
在每一步，你都遵循交替的移动模式：  

返回到达 `(m - 1, n - 1)` 所需的最小总费用。

### 示例 1
**输入:** `m = 1, n = 2, waitCost = [[1,2]]`  
**输出:** `3`  
**解释:**  
最佳路径为:  
因此，总费用为 `1 + 2 = 3` 。

### 示例 2
**输入:** `m = 2, n = 2, waitCost = [[3,5],[2,4]]`  
**输出:** `9`  
**解释:**  
最佳路径为:  
因此，总费用为 `1 + 2 + 2 + 4 = 9` 。

### 示例 3
**输入:** `m = 2, n = 3, waitCost = [[6,1,4],[3,2,5]]`  
**输出:** `16`  
**解释:**  
最佳路径为:  
因此，总费用为 `1 + 2 + 1 + 4 + 2 + 6 = 16` 。

### 约束条件
- `1 <= m, n <= 10^5`
- `2 <= m * n <= 10^5`
- `waitCost.length == m`
- `waitCost[0].length == n`
- `0 <= waitCost[i][j] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的走法都枚举一遍**，计算每条路径的花费，最后取最小值。  

- **走法**：从左上角 `(0,0)` 出发，只能向右或向下走（因为只能到达右下角），每走一步就进入一个新格子。  
- **花费**：进入格子 `(i,j)` 必须付 **入口费** `(i+1)*(j+1)`；除去起点 `(0,0)` 和终点 `(m‑1,n‑1)`，每到达一次格子还要付 **等待费** `waitCost[i][j]`。  
- **数据结构**：我们只需要用 **递归栈**（或显式的 `list`）来保存当前走到的格子序列，类似于在纸上写下“我现在在第几行第几列”。递归栈就像一本 **笔记本**，每翻一页就记录一次移动。  

**为什么正确**：只要把**所有**合法路径都遍历完，必然会碰到最优那条；把每条路径的费用算出来，取最小值自然就是答案。  

**复杂度**：  
- 设网格有 `m` 行 `n` 列，总共需要走 `m‑1 + n‑1` 步。每一步都有两种选择（右或下），所以路径数是 `C(m+n‑2, m‑1)`，呈指数级增长。  
- **时间复杂度**：`O(2^{m+n})`（实际是组合数，但在大多数情况下可以近似为指数），即“几乎不可能在合理时间内跑完”。  
- **空间复杂度**：递归深度最多 `m+n`，即 `O(m+n)`，相当于记录当前走到哪儿。  

显然，这种暴力方法只能用于非常小的输入，不能通过题目给出的上限 `m·n ≤ 10⁵`。  

#### 代码（Python）  

```python
def minCost_bruteforce(m, n, waitCost):
    # 入口费函数
    def entry(i, j):
        return (i + 1) * (j + 1)

    best = float('inf')                     # 当前找到的最小费用

    def dfs(i, j, cur):
        """从 (i,j) 出发，已累计费用 cur，尝试所有后续路径"""
        nonlocal best
        # 已经比当前最优更大，剪枝
        if cur >= best:
            return
        # 到达终点
        if i == m - 1 and j == n - 1:
            best = min(best, cur)           # 更新最小值
            return
        # 向右走
        if j + 1 < n:
            nxt = cur + entry(i, j + 1) + waitCost[i][j + 1]
            dfs(i, j + 1, nxt)
        # 向下走
        if i + 1 < m:
            nxt = cur + entry(i + 1, j) + waitCost[i + 1][j]
            dfs(i + 1, j, nxt)

    # 起点只付入口费，不付等待费
    dfs(0, 0, entry(0, 0))
    return best
```

> 关键行注释已用中文标明。该函数只适合 `m·n` 极小的情况，实际提交会超时。

#### 复杂度  

- **时间复杂度**：`O(2^{m+n})`（指数级），因为每一步都有两种选择，路径数呈指数增长。  
- **空间复杂度**：`O(m+n)`，递归栈深度最多走完所有格子。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **“穷举所有路径”** 是最慢的环节。  
实际上，这道题满足**最优子结构**：  
- 到达格子 `(i,j)` 的最小费用，只与 **左边格子 `(i, j‑1)`** 或 **上边格子 `(i‑1, j)`** 的最小费用有关。  
- 因为只能向右或向下走，路径只能从左或上方进入当前格子。  

这正好可以用 **动态规划（Dynamic Programming, DP）** 来把指数级的搜索压缩成线性时间。  

**状态定义**  
`dp[i][j]` 表示**走到格子 `(i,j)` 时累计的总费用**（已经包括入口费和该格子的等待费）。  

**状态转移**  
- 若从左边进入：费用为 `dp[i][j‑1] + entry(i,j) + waitCost[i][j]`  
- 若从上边进入：费用为 `dp[i‑1][j] + entry(i,j) + waitCost[i][j]`  

取两者最小，即  

```
dp[i][j] = min(dp[i‑1][j], dp[i][j‑1]) + entry(i,j) + waitCost[i][j]
```

**初始化**  
- 起点 `(0,0)` 只需要付入口费，不需要等待费：`dp[0][0] = entry(0,0)`  
- 第一行只能从左边来，第一列只能从上边来，按上述公式累加即可。  

**答案**  
终点 `(m‑1,n‑1)` 在 DP 里已经算进了等待费，但题目说**终点不需要等待**。因此最终答案要 **减去** `waitCost[m‑1][n‑1]`：  

```
answer = dp[m‑1][n‑1] - waitCost[m‑1][n‑1]
```

**空间优化**  
`dp[i][j]` 只依赖本行的左侧和上一行的同列。我们可以只保留 **一行**（长度为 `n`）的 DP 值，遍历完一行后再覆盖，这把空间从 `O(m·n)` 降到 `O(n)`，甚至如果 `m < n`，可以把列数最小的那一维当作 DP 数组，从而保证最小的空间占用。  

**类比**：  
想象我们在 **爬楼梯**，每一步只能往前或往右走。我们把每层楼的最小花费记下来，只需要记住前面两层的花费，而不必记住所有层的历史，这就是“只保留最近的记忆”。  

#### 代码（Python）  

```python
def minCost(m: int, n: int, waitCost):
    """
    动态规划求最小费用
    :param m: 行数
    :param n: 列数
    :param waitCost: m x n 的等待费用矩阵
    :return: 最小总费用（终点不计等待费）
    """
    # 入口费函数
    def entry(i, j):
        return (i + 1) * (j + 1)

    # 只保留当前行的 dp 值，长度为 n
    dp = [0] * n

    for i in range(m):
        for j in range(n):
            # 计算当前格子的入口费 + 等待费（起点除外稍后处理）
            cur = entry(i, j) + waitCost[i][j]

            if i == 0 and j == 0:                # 起点，只付入口费
                dp[j] = entry(0, 0)
                continue

            # 来自上方的费用（如果 i>0，dp[j] 仍是上一行的值）
            from_up = dp[j] if i > 0 else float('inf')
            # 来自左方的费用（如果 j>0，dp[j-1] 已经是本行左侧的值）
            from_left = dp[j - 1] if j > 0 else float('inf')

            # 取最小的前驱，加上当前格子的费用
            dp[j] = min(from_up, from_left) + cur

    # 终点已经算进了等待费，需要减掉
    return dp[-1] - waitCost[m - 1][n - 1]
```

> 关键行已加中文注释，代码可直接运行。  

#### 复杂度  

- **时间复杂度**：`O(m·n)`，因为每个格子只计算一次最小值。对比暴力的指数级，这就像从“爬山”变成了“坐电梯”。  
- **空间复杂度**：`O(n)`（或 `O(min(m,n))`），只保存一行 DP，显著降低内存占用。  

---

## 心得  

- **核心技巧**：**动态规划 + 空间压缩**，把“所有路径的最小值”转化为“每个格子的局部最优”。  
- **适用场景**：  
  1. 只允许向右/下（或左/上）移动的网格最短路径问题。  
  2. 带有额外格子费用（如入口费、等待费）的路径最小化。  
  3. “最小路径和”类问题（LeetCode 64、119、1514 等）。  
- **解题钥匙**：**找出状态转移的递推式**，并注意边界（起点、终点是否计费）。

---

## 反思  

- **第一反应**：看到“入口费 + 等待费”，立刻想到**把费用累加到每一步**，于是想到**DFS 暴力**。  
- **最容易踩的坑**：  
  - 忘记 **终点不需要等待费**，导致答案偏大。  
  - 边界处理不严谨：第一行只能从左来，第一列只能从上来，若直接使用 `dp[i‑1][j]`、`dp[i][j‑1]` 会出现数组越界。  
  - 大矩阵时忘记空间压缩，`O(m·n)` 的二维 DP 可能会超出内存限制。  
- **下次类似题的第一步**：先**画出网格，明确每一步只能从哪儿来**，写出**入口费 + 额外费用**的递推公式，然后决定是用 **二维 DP** 还是 **一维滚动数组**。