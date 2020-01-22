# #741. 樱桃采摘 / Cherry Pickup

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/cherry-pickup/)

---

## 题目（英文原版）

**Description**

You are given an n x n grid representing a field of cherries, each cell is one of three possible integers.
Return the maximum number of cherries you can collect by following the rules below:

**Examples**

**Example 1:**

```
Input: grid = [[0,1,-1],[1,0,-1],[1,1,1]]
Output: 5
Explanation: The player started at (0, 0) and went down, down, right right to reach (2, 2).
4 cherries were picked up during this single trip, and the matrix becomes [[0,1,-1],[0,0,-1],[0,0,0]].
Then, the player went left, up, up, left to return home, picking up one more cherry.
The total number of cherries picked up is 5, and this is the maximum possible.
```

**Example 2:**

```
Input: grid = [[1,1,-1],[1,-1,1],[-1,1,1]]
Output: 0
```

**Constraints**

- n == grid.length
- n == grid[i].length
- 1 <= n <= 50
- grid[i][j] is -1, 0, or 1.
- grid[0][0] != -1
- grid[n - 1][n - 1] != -1

---

## 题目（中文翻译）

给定一个 `n × n` 的网格（grid），每个单元格（cell）只能取以下三种整数之一。请按照下面的规则，返回能够采集到的樱桃的最大数量。

**规则**  
- 玩家从左上角 `(0, 0)` 出发，首先只能向右或向下移动，最终到达右下角 `(n‑1, n‑1)`。  
- 在移动过程中，若进入的单元格值为 `1`，则可以采集一颗樱桃，并将该单元格的值改为 `0`（表示樱桃已被采走）。  
- 若单元格值为 `0`，则什么也不做。  
- 若单元格值为 `-1`，表示该单元格是障碍物，玩家不能经过。  
- 到达右下角后，玩家需要原路返回左上角，同样只能向左或向上移动。返回途中也可以采集尚未被采走的樱桃。  
- **注意**：同一颗樱桃只能被采集一次。

求在满足上述所有约束的前提下，玩家能够采集的樱桃的最大总数。

---

## 示例

### 示例 1

**输入**  
``` 
grid = [[0,1,-1],
        [1,0,-1],
        [1,1,1]]
```

**输出**  
```
5
```

**解释**  
玩家从 `(0, 0)` 开始，依次向下、向下、向右、向右到达 `(2, 2)`。在这一次单程中共采集了 4 颗樱桃，矩阵随之变为 `[[0,1,-1],[0,0,-1],[0,0,0]]`。随后玩家向左、向上、向上、向左返回起点，又采集到 1 颗樱桃。总共采集的樱桃数为 5，这是能够达到的最大值。

### 示例 2

**输入**  
```
grid = [[1,1,-1],
        [1,-1,1],
        [-1,1,1]]
```

**输出**  
```
0
```

---

## 约束条件

- `n == grid.length`
- `n == grid[i].length`
- `1 ≤ n ≤ 50`
- `grid[i][j]` 只能是 `-1`、`0` 或 `1`
- `grid[0][0] != -1`（左上角不是障碍物）
- `grid[n‑1][n‑1] != -1`（右下角不是障碍物）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把走一次去（从左上到右下）和回来一次（从右下到左上）**都枚举出来，然后把两次路径上能捡到的樱桃数相加，取最大值。  

- **路径枚举**：一次完整的旅行其实是两条单向路径。我们可以先用深度优先搜索（DFS）把**所有可能的下/右走法**从 `(0,0)` 到 `(n‑1,n‑1)` 列出来；再把每条路径反向（左/上）走回去，检查在返回途中还能捡到多少樱桃。  
- **数据结构类比**：把每条路径看成一条“路线表”。把 `grid` 当作一张地图，`-1` 的格子相当于“水塘”，不能踩；`1` 是“果树”，踩上去可以“摘果”。  
- **为什么正确**：只要遍历到 **所有** 合法的去程和回程组合，就一定能找到最优解。  

显然，这种做法会产生巨大的搜索空间：  
- 去程有 `C(2n‑2, n‑1)` 条（从 `2n‑2` 步里挑 `n‑1` 步向下），  
- 回程同理。两者相乘的数量是指数级的，几乎不可能在 1 s 内算完。

#### 代码（Python）  

```python
from typing import List

def cherryPickup_bruteforce(grid: List[List[int]]) -> int:
    n = len(grid)
    best = 0                     # 全局最大樱桃数

    # ---------- 第一步：枚举所有去程 ----------
    def dfs_go(x, y, path, visited):
        """从 (x,y) 向右/下走到终点，记录走过的坐标列表 path"""
        if x == n - 1 and y == n - 1:          # 到达右下角
            path.append((x, y))
            dfs_back(0, 0, list(path), set(visited))   # 开始回程搜索
            path.pop()
            return
        # 记录当前格子是否已经摘过樱桃（防止回程重复计数）
        visited.add((x, y))
        path.append((x, y))

        # 向右
        if y + 1 < n and grid[x][y + 1] != -1:
            dfs_go(x, y + 1, path, visited)
        # 向下
        if x + 1 < n and grid[x + 1][y] != -1:
            dfs_go(x + 1, y, path, visited)

        path.pop()
        visited.remove((x, y))

    # ---------- 第二步：枚举所有回程 ----------
    def dfs_back(x, y, go_path, visited):
        """从 (x,y) 向左/上走到左上角，计算总樱桃数"""
        nonlocal best
        if x == 0 and y == 0:                     # 回到起点
            # 统计去程和回程的樱桃数（去程已在 visited 中标记）
            total = 0
            for i, j in go_path:
                if grid[i][j] == 1:
                    total += 1
            # 回程再加上未被去程摘过的樱桃
            for i, j in visited:
                if grid[i][j] == 1:
                    total += 1
            best = max(best, total)
            return

        # 向左
        if y - 1 >= 0 and grid[x][y - 1] != -1:
            visited.add((x, y - 1))
            dfs_back(x, y - 1, go_path, visited)
            visited.remove((x, y - 1))
        # 向上
        if x - 1 >= 0 and grid[x - 1][y] != -1:
            visited.add((x - 1, y))
            dfs_back(x - 1, y, go_path, visited)
            visited.remove((x - 1, y))

    # 开始搜索（入口格子一定合法）
    dfs_go(0, 0, [], set())
    return best
```

> **注意**：代码仅作思路演示，实际运行会因为指数级搜索而超时。

#### 复杂度  

- **时间复杂度**：`O(2^{2n})`（指数级），因为每一步都有 2 种选择，且要遍历去程和回程的所有组合。  
  大白话：如果 `n=5`，可能要尝试几千甚至几万条路线；`n=50` 时几乎不可能算完。  
- **空间复杂度**：`O(n)` 用于递归栈和路径记录。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**主要的瓶颈在于两次路径的相互独立枚举**。其实这两条路径可以**同步进行**，把“去”和“回”看成 **两个人同时从左上角走到右下角**，每一步两人都向右或向下（因为回程的左/上在时间轴上等价于去程的右/下）。  

**关键观察**  

1. 两个人走的步数相同。设第 `k` 步时，两人分别在 `(i1, j1)` 与 `(i2, j2)`，则必有 `i1 + j1 = k` 且 `i2 + j2 = k`。  
2. 同一步 `k`，只要记录两个人的行坐标 `i1, i2`（列可以由 `k - i` 推出），状态空间就压缩到 `O(n^2)`。  
3. 当两人落在同一格时，只能摘一次樱桃，否则可以各自摘取格子里的樱桃。  

基于上述，我们构造 **动态规划**（DP）：

- `dp[k][i1][i2]` 表示在第 `k` 步，两人分别位于 `(i1, k-i1)` 与 `(i2, k-i2)` 时，能够收集到的最大樱桃数。  
- 转移时考虑四种前一步的组合（两人各自是从上或左来），取最大值。  
- 若任意当前位置是 `-1`（障碍），该状态不可达，用 `-inf` 表示。  

**压缩维度**  

`k` 的取值范围是 `0 … 2n‑2`，每层只依赖上一层，因此可以只保留二维数组 `dp[i1][i2]`，每次遍历 `k` 时更新它。  

**类比**：想象两只小蜜蜂从花园左上角出发，同时向右下飞行。每一步它们只能向右或向下，且只能落在没有障碍的格子上。我们记录它们的“高度” `i1, i2`，而“水平距离” 自动由步数决定。这样只需要记住两只蜜蜂的高度，就能推算出它们的完整位置。

#### 代码（Python）  

```python
from typing import List
import sys

def cherryPickup(grid: List[List[int]]) -> int:
    n = len(grid)
    # dp[i][j] 表示在当前步数 k 时，两个玩家分别位于第 i 行和第 j 行时的最大樱桃数
    # 初始全部设为 -inf，表示不可达
    dp = [[-sys.maxsize] * n for _ in range(n)]
    dp[0][0] = grid[0][0]                 # 起点只能各在 (0,0)，只能摘一次

    # k 表示已经走的总步数，从 1 到 2n-2（到达右下角的步数）
    for k in range(1, 2 * n - 1):
        # new_dp 用来存放本轮 k 的状态，先全部置为 -inf
        new_dp = [[-sys.maxsize] * n for _ in range(n)]

        # i1, i2 分别是两个人的行坐标，范围是 max(0, k-(n-1)) … min(n-1, k)
        for i1 in range(max(0, k - (n - 1)), min(n, k + 1)):
            j1 = k - i1                     # 列坐标由 k 与 i1 决定
            if j1 >= n or grid[i1][j1] == -1:
                continue                    # 这格子是障碍，直接跳过

            for i2 in range(max(0, k - (n - 1)), min(n, k + 1)):
                j2 = k - i2
                if j2 >= n or grid[i2][j2] == -1:
                    continue

                # 四种可能的上一步来源：
                # (i1-1, i2-1)   两人都从上面下来
                # (i1-1, i2)     第一个从上，第二个从左
                # (i1, i2-1)     第一个从左，第二个从上
                # (i1, i2)       两人都从左边走
                best_prev = max(
                    dp[i1][i2],               # 两人都从左
                    dp[i1 - 1][i2] if i1 > 0 else -sys.maxsize,
                    dp[i1][i2 - 1] if i2 > 0 else -sys.maxsize,
                    dp[i1 - 1][i2 - 1] if i1 > 0 and i2 > 0 else -sys.maxsize,
                )
                if best_prev < 0:            # 前一步不可达
                    continue

                # 当前格子可以获得的樱桃数
                cur = best_prev + grid[i1][j1]
                if i1 != i2:                 # 两人不在同一格子时，第二个人的格子也能摘
                    cur += grid[i2][j2]

                new_dp[i1][i2] = max(new_dp[i1][i2], cur)

        dp = new_dp                         # 进入下一步

    # dp[n-1][n-1] 为两人在终点 (n-1,n-1) 时的最大樱桃数
    return max(dp[n - 1][n - 1], 0)          # 若不可达返回 0
```

> 代码中的 `-sys.maxsize` 相当于负无穷，用来标记“不可能到达”。  
> 最后取 `max(..., 0)` 是因为题目要求如果全程无法走通，返回 `0`。

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层遍历 `k` 共 `2n-1` 次，内部两层 `i1`、`i2` 各至多 `n`，所以大约 `n * n * n` 次操作。  
  - 大白话：如果 `n=50`，大约需要 `50³ = 125,000` 次计算，完全可以在毫秒级完成。  

- **空间复杂度**：`O(n²)`  
  - 只保留当前 `k` 步的二维表 `dp`（大小 `n × n`），相比暴力的指数空间大幅下降。  

---

## 心得  

- **核心技巧**：把“去”和“回”同步成两个人同向行进的 **双人动态规划**，利用“步数相同”这一约束把二维位置压缩成 `O(n²)` 状态。  
- **适用题型**：  
  1. `Cherry Pickup II`（两名机器人从左上角向右下角收集水果）  
  2. `Maximum Sum of 3 Non‑Overlapping Subarrays`（把多个子序列看成多个人走）  
  3. `Two Robots`（两个机器人在同一条路径上收集分数）  
- **一句话总结**：**把往返合并为两人同步前进，利用步数相等的关系进行 DP，既避免重复计数，又把复杂度降到多项式**。

---

## 反思  

- **第一反应**：直接把去程和回程分开暴力枚举，想“一次走完再一次走回”。  
- **最容易踩的坑**：  
  - **障碍格子 `-1`** 必须在每一步检查，否则会出现非法路径。  
  - **同一格子只能摘一次**：忘记去重会导致答案比实际大。  
  - **状态不可达的处理**：若直接用 `0` 初始化，可能把不可达的路径误认为合法，导致错误的最大值。  
- **下次类似题的第一步**：先思考是否可以把“往返”或“多段路径”**同步**成多个人的同向移动，用 **步数相同** 的约束把维度压缩，再设计 DP 转移。