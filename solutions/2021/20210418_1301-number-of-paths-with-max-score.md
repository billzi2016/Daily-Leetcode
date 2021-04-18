# #1301. **最大得分路径数量** / Number of Paths with Max Score

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/number-of-paths-with-max-score/)

---

## 题目（英文原版）

**Description**

You are given a square board of characters. You can move on the board starting at the bottom right square marked with the character 'S'.
You need to reach the top left square marked with the character 'E'. The rest of the squares are labeled either with a numeric character 1, 2, ..., 9 or with an obstacle 'X'. In one move you can go up, left or up-left (diagonally) only if there is no obstacle there.
Return a list of two integers: the first integer is the maximum sum of numeric characters you can collect, and the second is the number of such paths that you can take to get that maximum sum, taken modulo 10^9 + 7.
In case there is no path, return [0, 0].

**Examples**

**Example 1:**

```
Input: board = ["E23","2X2","12S"]
Output: [7,1]
```

**Example 2:**

```
Input: board = ["E12","1X1","21S"]
Output: [4,2]
```

**Example 3:**

```
Input: board = ["E11","XXX","11S"]
Output: [0,0]
```

**Constraints**

- 2 <= board.length == board[i].length <= 100

---

## 题目（中文翻译）

给定一个字符方阵（board），你需要从标记为 `'S'` 的右下角格子出发，在棋盘上移动，最终到达左上角标记为 `'E'` 的格子。其余格子要么标记为数字字符 `1, 2, …, 9`，要么标记为障碍物 `'X'`（obstacle）。每一步只能向上、向左或左上方向（对角线）移动，且目标格子不能是障碍物。

返回一个长度为 2 的整数数组：

- 第一个整数是能够收集的数字字符的最大和（即路径上所有数字字符的总和）。
- 第二个整数是能够得到该最大和的不同路径的数量，结果需对 `10^9 + 7` 取模（modulo）。

如果不存在任何合法路径，则返回 `[0, 0]`。

**示例**

示例 1  
输入: `board = ["E23","2X2","12S"]`  
输出: `[7,1]`

示例 2  
输入: `board = ["E12","1X1","21S"]`  
输出: `[4,2]`

示例 3  
输入: `board = ["E11","XXX","11S"]`  
输出: `[0,0]`

**约束条件**

- `2 <= board.length == board[i].length <= 100`  
- `board[i][j]` 只包含字符 `'E'`、`'S'`、`'X'` 或数字 `'1'`~`'9'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把棋盘想象成一张地图，**S** 是出发点，**E** 是终点。我们只能往「上」`↑`、 「左」`←`、 「左上」`↖` 这三个方向走，且不能走到标记为 **X** 的障碍格子。  

最直接的办法就是**把所有合法的走法都枚举出来**，每走到一个格子就把上面的数字（`'1'~'9'`）加到当前分数里，最后到达 **E** 时比较：

1. 记录目前看到的最高分 `max_score`。  
2. 记录能得到这个最高分的路径数量 `cnt`（如果又出现同样的最高分，就把计数加一）。

这和我们平时在玩「找所有通路」的小游戏一样，只是多了一个「累计分数」的过程。

> **类比**：  
> - **哈希表** 就像一本词典，`key` 是单词，`value` 是对应的解释。这里我们不需要哈希表，只用递归的「调用栈」来保存当前的路径和分数。

因为只能往左、上、左上走，坐标只会**递减**，所以不会出现环路（不会回到已经走过的格子），递归不会无限循环。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def pathsWithMaxScore(board: List[str]) -> List[int]:
    n = len(board)
    # 将字符转换为整数，'S'、'E' 当作 0，'X' 当作 -1（表示不可达）
    grid = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j, ch in enumerate(board[i]):
            if ch == 'X':
                grid[i][j] = -1                # 障碍
            elif ch in 'SE':
                grid[i][j] = 0                 # 起点/终点不计分
            else:
                grid[i][j] = int(ch)           # 数字格子

    # 全局记录最大分数和对应路径数
    max_score = -1
    ways = 0

    # 深度优先搜索（递归）
    def dfs(x: int, y: int, cur: int):
        """从坐标 (x, y) 往左上方向走，cur 为累计分数"""
        nonlocal max_score, ways
        # 到达左上角 (0,0) —— 即 E
        if x == 0 and y == 0:
            if cur > max_score:
                max_score, ways = cur, 1
            elif cur == max_score:
                ways = (ways + 1) % MOD
            return

        # 向上、左、左上三种方向继续搜索
        for dx, dy in [(-1, 0), (0, -1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
                dfs(nx, ny, cur + grid[nx][ny])

    # 起点在右下角 (n-1, n-1) ，起始分数为 0（S 本身不计分）
    dfs(n - 1, n - 1, 0)

    if max_score < 0:          # 没有合法路径
        return [0, 0]
    return [max_score, ways % MOD]
```

> **关键行解释**  
> - `grid[i][j] = -1` 把障碍格子标记为 `-1`，后面只要判断不等于 `-1` 就说明可以走。  
> - `if x == 0 and y == 0:` 当递归到达 **E**（左上角）时，更新全局的最大分数和计数。  
> - `for dx, dy in [(-1, 0), (0, -1), (-1, -1)]:` 这三组偏移量正好对应「上、左、左上」三条合法的移动方向。

#### 复杂度

- **时间复杂度**：`O(3^{2n})`（极端情况下每一步都有 3 条选择，路径长度约为 `2n`），也就是**指数级**。可以把 `O(3^{2n})` 想象成「每走一步都要把三条路都走遍」，随着棋盘大小的增加，计算量会爆炸。  
- **空间复杂度**：`O(2n)`，递归调用栈的深度最多是走完对角线的步数，大约 `2n`（`n ≤ 100`，所以最多 200 层）。

> 暴力解虽然思路最直接，但在 `n=100` 时根本跑不完，这正是我们要寻找「最优解」的原因。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复计算** 是主要的性能瓶颈：同一个格子会被多条路径反复访问，导致大量的冗余工作。  
要消除这种重复，就需要**记住**每个格子**从这里出发能够得到的最佳结果**——这正是**动态规划（Dynamic Programming，DP）**的核心思想。

**步骤拆解**：

1. **把「从 S 往 E」的过程反过来**，改为「从 E 往 S」的过程。  
   - 原题只能往上、左、左上走；如果我们把方向反过来，就只能往下、右、右下走。  
   - 这样我们可以**从左上角 (0,0) 开始**，向右下方填表，最终得到右下角 (n‑1,n‑1) 的答案。

2. **定义 DP 表**  
   - `dp[i][j]`：**从格子 (i,j) 到达终点 E（左上角）时，能够取得的最大分数**（不包括 (i,j) 本身的分数，因为我们在转移时会把它加进去）。  
   - `cnt[i][j]`：**在得到 `dp[i][j]` 这个最大分数的所有路径数**（模 `10^9+7`）。

3. **初始化**  
   - 障碍格子 `X`：设 `dp = -inf`（代表不可达），`cnt = 0`。  
   - 起点 `S`（右下角）和终点 `E`（左上角）本身不计分，值为 `0`。  
   - 其他格子先填 `-inf` / `0`，后面会被更新。

4. **状态转移**（从左上往右下遍历）  
   对每个可达格子 `(i, j)`，我们只能从它的**左、上、左上**三个前驱格子走到这里（因为我们是逆向思考）。  
   ```text
   前驱格子集合 = {(i-1, j), (i, j-1), (i-1, j-1)}
   ```
   - 先找出这三个前驱格子中**最大的 dp 值** `best`（如果全部是 -inf，说明当前格子不可达）。  
   - `dp[i][j] = best + value(i,j)`，其中 `value(i,j)` 是格子本身的数字（`0` 对于 S/E）。  
   - `cnt[i][j]` 为所有能够达到 `best` 的前驱格子的路径数之和（取模）。

5. **答案**  
   - 最终格子是右下角 `(n-1, n-1)`（即 S）。  
   - 如果 `dp[n-1][n-1]` 仍是 `-inf`，说明没有合法路径，返回 `[0,0]`。  
   - 否则返回 `[dp[n-1][n-1], cnt[n-1][n-1] % MOD]`。

> **类比**：  
> - 把 `dp` 看成「每个城镇的最高收入」表，`cnt` 看成「获得这个最高收入的赚钱方法有多少种」。我们从城镇 `E` 出发，逐步向外扩展，类似于「把每个城镇的最佳方案传递给相邻的城镇」。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7
INF = float('-inf')          # 用来表示不可达

def pathsWithMaxScore(board: List[str]) -> List[int]:
    n = len(board)

    # 把字符转成数值，'S'、'E' -> 0，'X' -> -1（障碍），'1'~'9' -> 对应整数
    val = [[0] * n for _ in range(n)]
    for i in range(n):
        for j, ch in enumerate(board[i]):
            if ch == 'X':
                val[i][j] = -1          # 障碍标记
            elif ch in 'SE':
                val[i][j] = 0           # 起点/终点不计分
            else:
                val[i][j] = int(ch)     # 数字格子

    # dp[i][j] = 最大分数，cnt[i][j] = 达到该最大分数的路径数
    dp  = [[INF] * n for _ in range(n)]
    cnt = [[0]   * n for _ in range(n)]

    # 起点是左上角的 'E'
    dp[0][0] = 0
    cnt[0][0] = 1

    # 按行、列顺序遍历（从左上往右下）
    for i in range(n):
        for j in range(n):
            if val[i][j] == -1:        # 障碍格子直接跳过
                continue
            if i == 0 and j == 0:      # 已经初始化过
                continue

            # 看左、上、左上三个前驱格子
            best = INF
            ways = 0
            for pi, pj in ((i-1, j), (i, j-1), (i-1, j-1)):
                if 0 <= pi < n and 0 <= pj < n and dp[pi][pj] != INF:
                    if dp[pi][pj] > best:
                        best = dp[pi][pj]
                        ways = cnt[pi][pj]          # 只保留更大的那条路径数
                    elif dp[pi][pj] == best:
                        ways = (ways + cnt[pi][pj]) % MOD   # 同样最大分数，路径数相加

            if best == INF:          # 前面没有可达格子，当前格子仍不可达
                continue

            dp[i][j] = best + val[i][j]   # 加上当前格子的分数
            cnt[i][j] = ways % MOD

    # 右下角是起点 'S'
    final_score = dp[n-1][n-1]
    final_cnt   = cnt[n-1][n-1] % MOD

    if final_score == INF:      # 没有任何合法路径
        return [0, 0]
    return [final_score, final_cnt]
```

> **关键行解释**  
> - `INF = float('-inf')` 用来表示「这条路根本走不通」。  
> - `best = INF`、`ways = 0`：遍历三个前驱格子时，先找出最大的 `dp` 值 `best`，并累计所有能够达到 `best` 的路径数 `ways`。  
> - `dp[i][j] = best + val[i][j]`：把当前格子的数字加到「从前驱格子得到的最大分数」上。  
> - `cnt[i][j] = ways % MOD`：因为答案要求取模，路径数随时取 `% MOD` 防止整数溢出。

#### 复杂度

- **时间复杂度**：`O(n²)`。我们只遍历了 `n × n` 的格子，每个格子只检查常数（3）个前驱格子。对比暴力的指数级，这里可以在 `n=100` 时毫秒级完成。  
- **空间复杂度**：`O(n²)`。需要两个 `n×n` 的二维数组 `dp` 与 `cnt`，以及一个同样大小的 `val` 辅助表。  

> 与暴力解相比，时间从「指数级」降到了「多项式级」——这正是 DP 的威力。

---

## 心得

- **核心技巧**：**二维动态规划 + 同时维护最大值和对应的计数**。  
- **适用的题型**（类似思路）  
  1. *Maximum Minimum Path*（在矩阵中找路径，使得路径上最小值最大）  
  2. *Cherry Pickup*（在二维网格中两次往返收集樱桃，要求最大数量）  
  3. *Unique Paths III*（在有障碍的网格中计数所有从起点到终点的合法路径）  
- **一句话总结解题钥匙**：**把「从起点到终点」的每一步抽象为「从前驱格子得到的最优结果」并记录有多少条路径能达到这个最优**。

---

## 反思

- **第一反应**：直接写递归暴力搜索，想把所有路径都列举出来。  
- **最容易踩的坑**  
  1. **障碍格子**处理不当，导致访问非法位置产生错误。  
  2. **计数取模**忘记在每一步都 `% MOD`，会导致整数溢出。  
  3. **起点/终点不计分**：若把 `'S'`、`'E'` 当成数字，会多算一次。  
- **下次遇到同类题**，第一步应该先问自己：  
  > 「这道题的状态是否可以从子问题递推得到？」  
  如果答案是「可以」，就立刻构造 DP 表（记录最优值），并思考是否需要 **额外的计数表** 来统计「有多少种方式能达到最优」。这样就能直接跳过指数级的暴力搜索。