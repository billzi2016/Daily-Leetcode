# #3418. 机器人可赚取的最大金额 / Maximum Amount of Money Robot Can Earn

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-amount-of-money-robot-can-earn/)

---

## 题目（英文原版）

**Description**

You are given an m x n grid. A robot starts at the top-left corner of the grid (0, 0) and wants to reach the bottom-right corner (m - 1, n - 1). The robot can move either right or down at any point in time.
The grid contains a value coins[i][j] in each cell:
The robot has a special ability to neutralize robbers in at most 2 cells on its path, preventing them from stealing coins in those cells.
Note: The robot's total coins can be negative.
Return the maximum profit the robot can gain on the route.

**Examples**

**Example 1:**

```
Input: coins = [[0,1,-1],[1,-2,3],[2,-3,4]]
Output: 8
Explanation:
An optimal path for maximum coins is:
```

**Example 2:**

```
Input: coins = [[10,10,10],[10,10,10]]
Output: 40
Explanation:
An optimal path for maximum coins is:
```

**Constraints**

- m == coins.length
- n == coins[i].length
- 1 <= m, n <= 500
- -1000 <= coins[i][j] <= 1000

---

## 题目（中文翻译）

你得到一个 `m x n` 的网格（grid）。机器人从网格的左上角 `(0, 0)` 开始，目标是到达右下角 `(m - 1, n - 1)`。机器人在任意时刻只能向右或向下移动。

网格的每个单元格 `coins[i][j]` 中都有一个整数价值，可能为负。

机器人拥有一种特殊能力：在其路径上最多可以中和（neutralize）2 个单元格中的强盗，从而防止这些单元格的金币被偷走。

> 注意：机器人最终获得的总金币数可能为负。

请返回机器人在路径上能够获得的最大收益（maximum profit）。

### 示例

**示例 1**  
输入: `coins = [[0,1,-1],[1,-2,3],[2,-3,4]]`  
输出: `8`  
解释:  
一条能够获得最大金币的最优路径为：

（此处保留原图或路径描述）

**示例 2**  
输入: `coins = [[10,10,10],[10,10,10]]`  
输出: `40`  
解释:  
一条能够获得最大金币的最优路径为：

（此处保留原图或路径描述）

### 约束条件

- `m == coins.length`
- `n == coins[i].length`
- `1 <= m, n <= 500`
- `-1000 <= coins[i][j] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的路径都枚举出来**，在每条路径上挑选最多两格“中立”掉抢劫犯的格子，然后把该路径上剩余格子的金币相加，取最大值。

- **路径的枚举**  
  机器人只能向右或向下走，从左上走到右下恰好要走 `m-1` 次向下和 `n-1` 次向右，总步数固定为 `m+n-2`。把这 `m+n-2` 步中的向下步位置挑出来（或者向右步位置挑出来），就得到一种路径。可以用递归或回溯把所有组合列出来。

- **中立抢劫犯**  
  在遍历到某条路径时，遍历路径上的每个格子，挑选出价值最小的（最不想收）的两格（如果格子数少于两格，就全都中立），把它们的价值视为 0（因为机器人可以让抢劫犯不偷），其余格子照原样相加。

- **为什么正确**  
  这其实是“穷举”所有合法的走法和所有合法的中立选择，必然能找到最优解。只要遍历不遗漏，答案一定在其中。

- **时间/空间复杂度**  
  - 路径的数量是组合数 `C(m+n-2, m-1)`，在最坏情况下约等于 `2^{(m+n)}`（指数级）。每条路径上还要遍历 `m+n-1` 个格子并挑选两格，整体时间复杂度是 **指数级**，几乎不可能在 `m,n ≤ 500` 时跑完。  
  - 空间上只需要保存递归栈和当前路径，最多 `O(m+n)`，即 **线性**。

> **大白话**：如果把每一步想象成一次“抉择”，我们要把所有可能的抉择树全部走遍，这棵树的枝条会非常多，根本不可能在合理时间内走完。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def brute_force(coins: List[List[int]]) -> int:
    m, n = len(coins), len(coins[0])
    total_steps = m + n - 2          # 需要走的总步数（不算起点）

    # 用 0 表示向下，1 表示向右。下面枚举所有向下的步数所在位置的组合
    best = -10**9

    # 生成所有向下的步子位置集合
    for down_pos in combinations(range(total_steps), m - 1):
        path = []                     # 记录路径上所有坐标
        i = j = 0
        path.append((i, j))
        down_set = set(down_pos)
        for step in range(total_steps):
            if step in down_set:      # 向下
                i += 1
            else:                     # 向右
                j += 1
            path.append((i, j))

        # 取出路径上所有格子的价值
        values = [coins[x][y] for x, y in path]

        # 选出最不想收的两格（最小的两数），把它们视为 0
        if len(values) > 2:
            # 找到两格最小值的下标
            min1, min2 = sorted(values)[:2]
            profit = sum(values) - min1 - min2
        else:   # 路径长度 ≤2，直接把所有格子都中立
            profit = 0

        best = max(best, profit)

    return best
```

> 这段代码可以跑通小规模测试（比如 `m,n ≤ 5`），但在正式数据会超时。

#### 复杂度

- **时间复杂度**：`O( C(m+n-2, m-1) * (m+n) )`，即指数级。`C` 表示组合数，随着网格增大会呈指数爆炸。  
  - 大白话：想象你要把所有可能的走法都列出来，数量会像雪花一样快速增多，根本算不过来。

- **空间复杂度**：`O(m+n)`，只存当前路径和递归栈。  
  - 大白话：我们只需要记住“我现在走到哪儿了”，不需要额外的大表格。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**重复计算**：很多不同的路径会在同一个格子上“相遇”，但我们每次都重新遍历整条路径。动态规划（DP）正是用来把**子问题的最优解**保存下来，避免重复。

**核心想法**：  
设 `dp[i][j][k]` 为“从左上角走到格子 `(i,j)`，已经使用了 `k` 次中立（`k = 0,1,2`）时，能够获得的最大利润”。这样，所有从左上到右下的合法走法都可以通过 **向右或向下** 两个方向的转移得到。

转移方程：

```
dp[i][j][k] = max(
    dp[i-1][j][k]   + coins[i][j]                (从上面下来，仍然保持已用的 k)
    dp[i][j-1][k]   + coins[i][j]                (从左边过来，仍然保持已用的 k)
    dp[i-1][j][k-1] + 0   (从上面下来，利用一次中立，把当前格子价值置零)
    dp[i][j-1][k-1] + 0   (从左边过来，利用一次中立)
)
```

- 当 `k = 0` 时，不能使用中立，只能走第一行两项。
- 当 `k > 0` 时，还可以选择把当前格子 **中立**（价值计为 0），这对应转移中的后两项。

**初始化**：

- 起点 `(0,0)`：  
  - `dp[0][0][0] = coins[0][0]`（不使用中立）  
  - `dp[0][0][1] = dp[0][0][2] = 0`（如果在起点就使用中立，把它的价值抵消）

其余格子如果没有合法来源（如上面越界），对应的 `dp` 设为极小值 `-inf`，防止被错误选入最大值。

**答案**：遍历完所有格子后，目标格子 `(m-1,n-1)` 的最大利润是 `max(dp[m-1][n-1][0], dp[m-1][n-1][1], dp[m-1][n-1][2])`。

**为什么只需要 3 层**：机器人最多只能中立 2 格，所以 `k` 的取值只有 `0,1,2`。这让状态空间保持在 `O(m·n·3)`，即线性可接受。

**类比**：  
把 `dp` 想象成一本“账本”，每翻到一个格子，就记下“到这里为止，我已经用了几次抵消，手里最多有多少钱”。以后再到同一个格子，只要看账本里已经记好的最大值，就不必重新算过去的路。

#### 代码（Python）

```python
from typing import List

def maxProfit(coins: List[List[int]]) -> int:
    INF_NEG = -10**9                     # 负无穷的近似值
    m, n = len(coins), len(coins[0])

    # dp[i][j][k]：到达 (i,j) 时已使用 k 次中立，能获得的最大利润
    dp = [[[INF_NEG] * 3 for _ in range(n)] for _ in range(m)]

    # 初始化起点
    dp[0][0][0] = coins[0][0]            # 不使用中立
    dp[0][0][1] = dp[0][0][2] = 0        # 在起点使用中立（价值被抵消）

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:        # 起点已处理
                continue
            for k in range(3):           # k = 0,1,2
                # 从上方来到 (i,j)
                if i > 0:
                    # 不使用中立
                    dp[i][j][k] = max(dp[i][j][k],
                                      dp[i-1][j][k] + coins[i][j])
                    # 使用一次中立（前一个状态必须已经用了 k-1 次）
                    if k > 0:
                        dp[i][j][k] = max(dp[i][j][k],
                                          dp[i-1][j][k-1] + 0)   # 当前格子价值置零

                # 从左方来到 (i,j)
                if j > 0:
                    dp[i][j][k] = max(dp[i][j][k],
                                      dp[i][j-1][k] + coins[i][j])
                    if k > 0:
                        dp[i][j][k] = max(dp[i][j][k],
                                          dp[i][j-1][k-1] + 0)

    # 目标格子取三种使用次数中的最大值
    return max(dp[m-1][n-1])
```

> 这段代码的时间复杂度是 `O(m * n * 3)`，在 `m,n ≤ 500` 时毫秒级即可跑完。

#### 复杂度

- **时间复杂度**：`O(m * n * 3) = O(mn)`。  
  - 大白话：我们只遍历每个格子一次，每次检查 3 种“已经用了几次中立”的情况，整个过程和网格大小成正比，快得像走直线。

- **空间复杂度**：`O(m * n * 3) = O(mn)`。  
  - 大白话：我们需要保存每个格子对应的 3 条信息（用 0、1、2 次中立时的最大收益），这就像在每个格子里贴了 3 张小纸条。

---

## 心得

- **核心技巧**：**二维动态规划 + 额外的“使用次数”维度**。把“最多中立 2 格”抽象成状态维度 `k`，把原本的二维 DP 扩展为三维 DP。
- **适用的题型**  
  1. “在路径上最多做 K 次特殊操作”类，如“路径上最多翻转 K 次障碍”  
  2. “带有限制的最大/最小路径和”，例如“最多删除 K 条边的最长路径”  
  3. “带费用的最短路径”，如“最多使用 K 次优惠券的最短路”  
- **一句话总结解题钥匙**：**把每一次“资源使用”抽象成 DP 的一个维度，状态转移时同时考虑“使用”与“不使用”。**

---

## 反思

- **第一反应**：直接想到“遍历所有路径”，因为从左上到右下的走法看似不多，却忽视了组合数的爆炸。
- **最容易踩的坑**  
  - **初始化**：起点的 `k>0` 状态必须设为 0（使用中立后价值被抵消），否则后面的转移会误以为不合法。  
  - **负数处理**：网格中的值可以为负，不能把默认的 `0` 当作“不可达”。我们用一个足够小的负数 `-inf` 表示“还没到达”。  
  - **边界**：`i-1`、`j-1` 越界时要小心，防止访问非法索引。  
- **下次遇到同类题**：第一步先**抽象出资源/次数的维度**（比如使用次数、剩余跳跃次数），再写出 **二维/三维 DP 状态转移**，最后检查初始化和边界。这样可以避免从暴力搜索一步步回溯的低效路径。