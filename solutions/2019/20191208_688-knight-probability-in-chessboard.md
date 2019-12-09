# #688. 棋盘上骑士的存活概率 / Knight Probability in Chessboard

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/knight-probability-in-chessboard/)

---

## 题目（英文原版）

**Description**

On an n x n chessboard, a knight starts at the cell (row, column) and attempts to make exactly k moves. The rows and columns are 0-indexed, so the top-left cell is (0, 0), and the bottom-right cell is (n - 1, n - 1).
A chess knight has eight possible moves it can make, as illustrated below. Each move is two cells in a cardinal direction, then one cell in an orthogonal direction.
Each time the knight is to move, it chooses one of eight possible moves uniformly at random (even if the piece would go off the chessboard) and moves there.
The knight continues moving until it has made exactly k moves or has moved off the chessboard.
Return the probability that the knight remains on the board after it has stopped moving.

**Examples**

**Example 1:**

```
Input: n = 3, k = 2, row = 0, column = 0
Output: 0.06250
Explanation: There are two moves (to (1,2), (2,1)) that will keep the knight on the board.
From each of those positions, there are also two moves that will keep the knight on the board.
The total probability the knight stays on the board is 0.0625.
```

**Example 2:**

```
Input: n = 1, k = 0, row = 0, column = 0
Output: 1.00000
```

**Constraints**

- 1 <= n <= 25
- 0 <= k <= 100
- 0 <= row, column <= n - 1

---

## 题目（中文翻译）

在一个 `n × n` 棋盘（chessboard）上，骑士（knight）从单元格 `(row, column)` 开始，并尝试恰好进行 `k` 步移动。行和列均为 **0-indexed**，因此左上角为 `(0, 0)`，右下角为 `(n - 1, n - 1)`。  

骑士有八种可能的移动方式，如下图所示。每一种移动都是先在主方向（cardinal direction）上走两格，然后在正交方向（orthogonal direction）上走一格。  

每当骑士需要移动时，它会 **均匀随机**（uniformly at random）地选择这八种可能中的一种（即使该移动会导致骑士离开棋盘），并执行该移动。  

骑士会持续移动，直到完成恰好 `k` 步，或是已经离开棋盘为止。  

返回骑士在停止移动后仍然留在棋盘上的概率（probability）。

**示例 1**  

**示例 2**  

**约束条件**  

- `1 <= n <= 25`  
- `0 <= k <= 100`  
- `0 <= row, column <= n - 1`  

**示例**  

**示例 1:**  
```
Input: n = 3, k = 2, row = 0, column = 0
Output: 0.06250
Explanation: 有两种移动（到 `(1,2)`、`(2,1)`）能够让骑士仍在棋盘内。  
从这两个位置出发，各自又有两种移动可以让骑士继续留在棋盘上。  
因此，骑士最终仍在棋盘上的总概率为 `0.0625`。
```

**示例 2:**  
```
Input: n = 1, k = 0, row = 0, column = 0
Output: 1.00000
Explanation: 骑士没有进行任何移动，必然留在棋盘上，概率为 `1`。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟**骑士的每一步。  
- 从起始格子 `(row, column)` 出发，遍历所有可能的走法（共 8 种），递归地往下走 `k` 步。  
- 当走到第 `k` 步时，如果仍然在棋盘内部，就记一次 “成功”。  
- 最后把成功次数除以所有可能的走法总数（`8^k`），得到概率。

> **类比**：把棋盘想成一张城市地图，骑士是游客。每一次出门，游客会随机挑选 8 条“公交线路”中的一条，哪怕这条线路会直接把他送出城外。我们要统计：在恰好坐满 `k` 次公交后，游客还能在城里出现的概率。

**为什么正确**  
递归把每一种走法都枚举了一遍，**没有遗漏**也**没有重复计数**。只要统计所有合法的走法占总走法的比例，就是题目要求的概率。

**时间/空间复杂度**  
- 每一步都有 8 种选择，走 `k` 步就会产生 `8^k` 条路径。  
- 因此时间复杂度是 **O(8^k)**，这在 `k` 甚至只有 10 时已经非常大（`8^10 ≈ 1.07e9`），更别说题目允许 `k` 达到 100。  
- 递归的深度为 `k`，每层保存常数个变量，空间复杂度是 **O(k)**（栈空间）。

> **大白话**：  
> - `O(8^k)` 就像每秒可以吃掉 8 块巧克力，吃 `k` 秒后你得吃掉 `8^k` 块，显然吃不完。  
> - `O(k)` 的空间只是说我们只需要记住 “我已经走了几步”，这点儿开销很小。

#### 代码（Python）

```python
from typing import List

# 骑士的 8 种相对移动方式
moves: List[tuple[int, int]] = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def knightProbability_bruteforce(n: int, k: int, row: int, column: int) -> float:
    """
    暴力递归枚举所有可能路径，返回留在棋盘上的概率。
    """
    def dfs(r: int, c: int, steps: int) -> int:
        # 如果已经走出了棋盘，后面不可能再回到棋盘，直接返回 0 条合法路径
        if not (0 <= r < n and 0 <= c < n):
            return 0
        # 已经走完 k 步，仍然在棋盘内，算一条合法路径
        if steps == 0:
            return 1
        # 递归尝试 8 种走法，累计合法路径数
        total = 0
        for dr, dc in moves:
            total += dfs(r + dr, c + dc, steps - 1)
        return total

    # 所有可能的走法总数是 8^k（每一步都有 8 种选择）
    total_paths = 8 ** k
    # 统计合法路径的数量
    stay_paths = dfs(row, column, k)

    # 概率 = 合法路径 / 所有路径
    return stay_paths / total_paths
```

#### 复杂度

- **时间复杂度**：`O(8^k)`  
  > 解释：每走一步都会产生 8 条新分支，走 `k` 步后总分支数是 `8 × 8 × … × 8 = 8^k`，所以执行的递归调用次数也是这个量级。

- **空间复杂度**：`O(k)`  
  > 解释：递归深度最多是 `k`，每层只保存当前坐标和剩余步数这几个整数，所需的额外空间随 `k` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复计算**。  
举个例子：在 `k=10` 的情况下，骑士可能会多次到达同一个格子 `(2,3)`，但我们会把它后面的所有子路径 **重新算** 多遍。  

**关键观察**  
- 骑士在第 `i` 步所处的格子只和 **前一步** 的格子以及 **一步的移动方式** 有关。  
- 换句话说，如果我们已经知道 “第 `i-1` 步在格子 `(x, y)` 的概率”，就可以 **一次性** 推算出 “第 `i` 步在所有合法格子上的概率”。  

这正是**动态规划（Dynamic Programming，DP）**的典型思路：  
> 把大问题拆成若干子问题，子问题的解只依赖于更小的子问题的解，且每个子问题只求一次。

**实现方式**  
- 用一个二维数组 `dp[r][c]` 表示 “在当前已经走了 `t` 步后，骑士在格子 `(r, c)` 上的概率”。  
- 初始化：`t = 0` 时，骑士只在起始格子，概率为 `1`，其它格子为 `0`。  
- 迭代 `t` 从 `1` 到 `k`：  
  - 对于每个格子 `(r, c)`，它的概率来自 **上一步** 能跳到它的 8 个格子。  
  - 如果上一步的格子是合法的，则把 `dp_prev[prev_r][prev_c] / 8` 累加到 `dp_cur[r][c]`（因为每一步均匀随机选择 8 条路径）。  
- 最后把第 `k` 步所有格子的概率相加，即为骑士仍在棋盘上的总概率。

**为什么只需要两张表**  
在一次迭代里，我们只会用到 `t-1` 步的概率（`dp_prev`），而不需要更早之前的值。所以可以交替使用两张 `n × n` 的矩阵，节省空间。

> **类比**：想象你在玩“传球游戏”。每一轮，你把球从手里传给相邻的 8 个人，每个人再继续传。只要记录每一轮每个人手里有球的概率，就能算出第 `k` 轮球仍在场内的概率，而不必记住每一次传球的全部细节。

#### 代码（Python）

```python
from typing import List

# 骑士的 8 种相对移动方式（与上面相同）
MOVES: List[tuple[int, int]] = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def knightProbability_dp(n: int, k: int, row: int, column: int) -> float:
    """
    动态规划求解骑士在 k 步后仍在棋盘内的概率。
    时间复杂度 O(k * n^2) ，空间复杂度 O(n^2)。
    """
    # dp_prev 表示走了 t-1 步后的概率分布
    dp_prev = [[0.0 for _ in range(n)] for _ in range(n)]
    dp_prev[row][column] = 1.0          # 第 0 步，只有起始格子概率为 1

    for step in range(1, k + 1):
        # dp_cur 用来存储走了 step 步后的概率分布
        dp_cur = [[0.0 for _ in range(n)] for _ in range(n)]

        for r in range(n):
            for c in range(n):
                # 如果上一步在 (r, c) 的概率为 0，下面的循环可以直接跳过
                if dp_prev[r][c] == 0:
                    continue
                # 把当前格子的概率均分给 8 条可能的下一步
                prob_each = dp_prev[r][c] / 8.0
                for dr, dc in MOVES:
                    nr, nc = r + dr, c + dc
                    # 只把概率加到仍在棋盘内的格子
                    if 0 <= nr < n and 0 <= nc < n:
                        dp_cur[nr][nc] += prob_each

        # 完成一步后，准备进入下一轮迭代
        dp_prev = dp_cur

    # k 步结束后，把所有格子的概率相加，就是留在棋盘上的总概率
    total_prob = sum(map(sum, dp_prev))
    return total_prob
```

#### 复杂度

- **时间复杂度**：`O(k * n^2)`  
  > 解释：外层循环跑 `k` 次，每一次我们遍历 `n × n` 的格子，对每个格子检查最多 8 条跳法（常数），所以总体是 `k * n^2`。  
  > 与暴力的 `8^k` 相比，`k * n^2` 即使在最大限制 `k = 100, n = 25` 也只有 `100 * 625 = 62,500` 次基本操作，轻松跑完。

- **空间复杂度**：`O(n^2)`  
  > 解释：我们只保存两张 `n × n` 的概率矩阵（`dp_prev` 与 `dp_cur`），不随 `k` 增长。对于 `n = 25`，矩阵大小只有 625 个浮点数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**动态规划 + 状态转移**（把每一步的概率分布当作状态，利用上一步的状态一次性算出下一步）。  
- **适用的题型**  
  1. “在棋盘/网格上走 k 步，求某种概率或路径计数”——如 *Probability of a Random Walk on a Grid*、*Unique Paths III*。  
  2. “限定步数的最短路径 / 最大分数”——如 *Minimum Path Sum with K moves*、*Maximum Gold Collecting with K steps*。  
  3. “在固定步数内能否到达目标”——如 *Reach a Target Position After K Moves*（类似本题的判定版）。  

- **一句话总结解题钥匙**：  
  > 把“每一步的所有可能”压缩成“当前格子的概率”，用前一步的概率一次性推导后一步，避免重复遍历所有路径。

---

## 反思

- **拿到题目第一反应**：直接写递归/DFS 暴力枚举，先跑通最朴素的思路，再看有没有优化空间。  
- **最容易踩的坑**  
  1. **边界判断**：每一次跳动后要先判断是否仍在棋盘内，忘记这一步会导致数组越界或错误累加概率。  
  2. **除以 8**的时机：概率必须在每一步均匀分配，不能等到最后才除，否则会得到错误的结果。  
  3. **k = 0** 的特殊情况：此时骑士根本不动，答案应当是 `1`（只要起点合法），代码中要保证循环不执行导致返回初始概率。  
- **下次遇到同类题，第一步该想到**：  
  > “这道题的状态只和上一步有关吗？”如果答案是肯定的，就立即考虑用 **动态规划**（或记忆化搜索）把子问题的结果保存下来，避免指数级的重复计算。