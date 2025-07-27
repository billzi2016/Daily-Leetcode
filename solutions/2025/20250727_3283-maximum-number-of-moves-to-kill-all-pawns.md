# #3283. **消灭所有兵的最大移动次数** / Maximum Number of Moves to Kill All Pawns

> 难度：困难 · 标签：Array、Math、Bit Manipulation、Breadth-First Search、Game Theory、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-moves-to-kill-all-pawns/)

---

## 题目（英文原版）

**Description**

There is a 50 x 50 chessboard with one knight and some pawns on it. You are given two integers kx and ky where (kx, ky) denotes the position of the knight, and a 2D array positions where positions[i] = [xi, yi] denotes the position of the pawns on the chessboard.
Alice and Bob play a turn-based game, where Alice goes first. In each player's turn:
Alice is trying to maximize the sum of the number of moves made by both players until there are no more pawns on the board, whereas Bob tries to minimize them.
Return the maximum total number of moves made during the game that Alice can achieve, assuming both players play optimally.
Note that in one move, a chess knight has eight possible positions it can move to, as illustrated below. Each move is two cells in a cardinal direction, then one cell in an orthogonal direction.

**Examples**

**Example 1:**

```
Input: kx = 1, ky = 1, positions = [[0,0]]
Output: 4
Explanation:

The knight takes 4 moves to reach the pawn at (0, 0) .
```

**Example 2:**

```
Input: kx = 0, ky = 2, positions = [[1,1],[2,2],[3,3]]
Output: 8
Explanation:
```

**Example 3:**

```
Input: kx = 0, ky = 0, positions = [[1,2],[2,4]]
Output: 3
Explanation:
```

**Constraints**

- 0 <= kx, ky <= 49
- 1 <= positions.length <= 15
- positions[i].length == 2
- 0 <= positions[i][0], positions[i][1] <= 49
- All positions[i] are unique.
- The input is generated such that positions[i] != [kx, ky] for all 0 <= i < positions.length.

---

## 题目（中文翻译）

有一个 50 × 50 的棋盘，上面有一枚骑士（knight）和若干兵（pawn）。给定两个整数 `kx` 和 `ky`，其中 `(kx, ky)` 表示骑士的初始位置；再给定一个二维数组 `positions`，其中 `positions[i] = [xi, yi]` 表示棋盘上第 *i* 个兵的位置。

Alice 和 Bob 进行一个回合制游戏（turn‑based game），Alice 先手。每位玩家的回合规则如下：

- **Alice** 的目标是**最大化**两位玩家在棋盘上所有兵被吃掉之前所走的总移动次数（move）。
- **Bob** 的目标是**最小化**该总移动次数。

返回在双方都采取最优策略的前提下，Alice 能够实现的**最大**总移动次数。

> 注意：在一次移动中，骑士可以跳到八个可能的位置，如下图所示。每次跳跃先沿某个主方向走两格，再沿垂直方向走一格。

---

### 示例

**示例 1**

```
Input: kx = 1, ky = 1, positions = [[0,0]]
Output: 4
Explanation:
骑士需要 4 步才能到达位于 (0, 0) 的兵。
```

**示例 2**

```
Input: kx = 0, ky = 2, positions = [[1,1],[2,2],[3,3]]
Output: 8
Explanation:
（此处解释略）
```

**示例 3**

```
Input: kx = 0, ky = 0, positions = [[1,2],[2,4]]
Output: 3
Explanation:
（此处解释略）
```

---

### 约束条件

- `0 <= kx, ky <= 49`
- `1 <= positions.length <= 15`
- `positions[i].length == 2`
- `0 <= positions[i][0], positions[i][1] <= 49`
- 所有 `positions[i]` 均互不相同。
- 输入保证 `positions[i] != [kx, ky]` 对所有 `0 <= i < positions.length` 成立。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的吃子顺序** 都列举一遍，然后模拟游戏过程：

1. 先把骑士放在起始格子 `(kx, ky)`。  
2. 任选一个兵子作为第一颗被吃掉的目标，计算骑士走到它需要多少步（可以用 BFS 求最短步数）。  
3. 接下来轮到 Bob 走，他会在剩下的兵子中挑选 **使总步数最小** 的那颗。  
4. 再轮到 Alice，她挑选 **使总步数最大** 的那颗……  
5. 当所有兵子都被吃掉时，记录下这条路径的总步数。  

把第 2~4 步遍历所有可能的顺序，就能得到答案。

> **类比**：把每颗兵子想成一张卡片，游戏就是把卡片按一定顺序摘下来。暴力解相当于把所有可能的排列（`n!`）都试一遍，就像把一副扑克牌的每一种洗牌方式都摆出来看一遍。

**为什么它一定能得到正确答案？**  
因为我们把所有合法的游戏进行过程都枚举了，最优的（即 Alice 能逼出的最大总步数）必然出现在枚举集合里。

**复杂度分析**  

- 设兵子数量为 `n（≤15）`。  
- 每一种顺序需要遍历 `n` 次选择，所有顺序的数量是 `n!`（阶乘），随 `n` 指数增长。  
- 对每一步我们都要查询两格之间的最短骑士步数，这可以提前用 BFS 预处理得到 `O(1)` 查询，但预处理本身是 `O(64·64)`（棋盘 50×50，实际常数很小）。  

```
时间复杂度：O(n!)   （n=15 时已经天文数字，根本跑不完）
空间复杂度：O(n²)   （保存每对格子之间的距离，最多 16×16≈256 个数）
```

> **大白话**：`O(n!)` 就好比“把 15 本书全部排成一排的所有可能”。这种数量远远超过一台电脑在一年里能做的运算次数，所以只能当作“思考的起点”，不能直接提交。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **两大瓶颈**：

1. **枚举所有顺序**：`n!` 太大。  
2. **每次都要知道骑士从当前位置到目标格子的最短步数**：虽然可以预处理，但仍需要在递归/状态转移中快速获取。

要想把枚举从 “所有排列” 缩小到 “状态 + 选择”，可以使用 **动态规划 + 位掩码（Bitmask DP）**。  

- **状态**  
  - `mask`：一个二进制数，长度为 `n`，第 `i` 位为 `1` 表示第 `i` 颗兵子 **还没被吃掉**；`0` 表示已经吃掉。  
  - `last`：上一回合骑士停留的格子。因为骑士的移动距离只和起点和终点有关，我们只需要记住上一次吃掉的是哪颗兵子（或者是初始位置）。  
  - `turn`：轮到谁走，`0` 表示 Alice（想让总步数最大），`1` 表示 Bob（想让总步数最小）。  

- **转移**  
  - 当前轮到的玩家要 **在 mask 中挑选一颗还在的兵子 `i`**，骑士从 `last` 走到 `i` 需要 `dist[last][i]` 步。  
  - 吃掉 `i` 后，`mask` 去掉第 `i` 位，`last` 变成 `i`，`turn` 切换。  
  - 如果是 Alice，她会取 **所有可能选择的最大值**（因为她想让总步数尽可能大）；如果是 Bob，则取 **最小值**。  

- **递归式**（伪代码）

```text
dp(mask, last, turn):
    if mask == 0:                 # 没有兵子了
        return 0
    if turn == 0:                 # Alice，max
        best = -∞
        for each i where mask has bit i:
            best = max(best,
                        dist[last][i] + dp(mask ^ (1<<i), i, 1))
        return best
    else:                         # Bob，min
        best = +∞
        for each i where mask has bit i:
            best = min(best,
                        dist[last][i] + dp(mask ^ (1<<i), i, 0))
        return best
```

- **预处理距离**  
  骑士在 50×50 棋盘上每走一步只能跳到 8 个相邻格子。我们可以对 **每一个关键点**（起始位置 + 所有兵子）分别跑一次 BFS，得到它到其它关键点的最短步数。  
  这样 `dist[a][b]` 的查询是 `O(1)`，而 BFS 本身只在 2500 格子上跑，时间几乎可以忽略不计。

- **为什么 DP 能把 `n!` 降到 `2^n·n`？**  
  - `mask` 只记录 **哪些兵子还在**，不关心它们被吃的先后顺序。  
  - 对同一 `mask`，不管是怎么走到这里的，只要 `last` 相同，后面的子问题是完全一样的。  
  - 所以状态总数是 `2^n`（所有子集）× `n+1`（`last` 可能是任意兵子或起始位置）× `2`（轮到谁），即 `O(2^n·n)`，远远小于 `n!`。  

> **类比**：把 “所有排列” 想成“一棵非常宽的树”。DP 把这棵树“合并”成同一层的相同子树，只保留 **子树根部的状态**，大幅剪枝。

#### 代码（Python）

```python
from collections import deque
from functools import lru_cache
from typing import List

# ------------------- 1. 预处理：BFS 求最短骑士步数 -------------------
def bfs(start_x: int, start_y: int) -> List[List[int]]:
    """返回从 (start_x,start_y) 到棋盘每格的最少骑士步数"""
    dirs = [(2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)]
    INF = 10**9
    dist = [[INF] * 50 for _ in range(50)]
    q = deque()
    q.append((start_x, start_y))
    dist[start_x][start_y] = 0
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 50 and 0 <= ny < 50 and dist[nx][ny] == INF:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return dist

# ------------------- 2. 主函数 -------------------
def maxMoves(kx: int, ky: int, positions: List[List[int]]) -> int:
    n = len(positions)
    # 把起始位置也当作“第 n 颗”点，方便统一处理
    points = positions + [[kx, ky]]          # 长度 = n+1，最后一个是起点

    # 预计算每两个关键点之间的最短步数
    # dist_matrix[i][j] = 从 points[i] 到 points[j] 的最少骑士步数
    dist_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dboard = bfs(points[i][0], points[i][1])
        for j in range(n + 1):
            dist_matrix[i][j] = dboard[points[j][0]][points[j][1]]

    FULL_MASK = (1 << n) - 1   # 所有兵子都还在

    @lru_cache(None)
    def dp(mask: int, last: int, turn: int) -> int:
        """
        mask : 还未被吃的兵子集合（bit 为 1 表示在棋盘上）
        last : 上一次骑士所在的关键点编号（0..n-1 为兵子，n 为起始位置）
        turn : 0 -> Alice（想让总步数最大），1 -> Bob（想让总步数最小）
        返回从当前局面开始，两人都最优时的总步数
        """
        if mask == 0:                 # 没有兵子了，游戏结束
            return 0

        if turn == 0:                 # Alice，取最大值
            best = -10**9
            for i in range(n):
                if mask & (1 << i):   # 第 i 颗兵子还在
                    nxt = mask ^ (1 << i)          # 吃掉 i 后的 mask
                    cost = dist_matrix[last][i] + dp(nxt, i, 1)
                    best = max(best, cost)
            return best
        else:                         # Bob，取最小值
            best = 10**9
            for i in range(n):
                if mask & (1 << i):
                    nxt = mask ^ (1 << i)
                    cost = dist_matrix[last][i] + dp(nxt, i, 0)
                    best = min(best, cost)
            return best

    # 初始状态：所有兵子都在，骑士在起点（编号 n），轮到 Alice（turn=0）
    return dp(FULL_MASK, n, 0)

# ------------------- 3. 示例 -------------------
if __name__ == "__main__":
    print(maxMoves(1, 1, [[0, 0]]))                     # 4
    print(maxMoves(0, 2, [[1,1],[2,2],[3,3]]))         # 8
    print(maxMoves(0, 0, [[1,2],[2,4]]))               # 3
```

> **关键注释**  
> - `bfs` 用来一次性算出 **从某一点到全棋盘** 的最短骑士步数，类似 “查字典”——把所有页码一次性记下来，后面查询只需要 `O(1)`。  
> - `dist_matrix` 把每对关键点的距离装进表格，后面 DP 只要 `dist_matrix[last][i]` 就能得到两格之间的步数。  
> - `dp` 使用 `@lru_cache` 实现记忆化搜索，避免对同一 `(mask, last, turn)` 重复计算。  

#### 复杂度

- **预处理**  
  - BFS 在 50×50 的棋盘上进行 `n+1 ≤ 16` 次，每次 `O(2500)`，总计 `O( (n+1)·2500 )`，几乎可以忽略。  
- **状态数量**  
  - `mask` 有 `2^n` 种，`last` 有 `n+1` 种，`turn` 有 2 种 → `O(2^n · n)`（这里的 `n` 取 `n+1`，常数不影响量级）。  
- **每个状态的转移**  
  - 需要遍历当前 `mask` 中的所有 `1` 位，最坏情况是 `n` 次。  
- **总体时间复杂度**  
  ```
  O( n * 2^n )
  ```
  对 `n ≤ 15` 来说，大约是 `15 * 32768 ≈ 5·10^5` 次基本运算，完全可以在毫秒级跑完。  

- **空间复杂度**  
  - `dist_matrix`：`(n+1)²`，最多 `256` 个整数。  
  - DP 缓存表：`O( n * 2^n )` 个条目，每个保存一个整数。  
  ```
  O( n * 2^n )
  ```
  同样在几百 KB 级别，远小于机器内存。

> 与暴力解的 `O(n!)` 相比，`O(n·2^n)` 是指数级的 **巨大** 缩减，真正可以在 LeetCode 上 AC。

---

## 心得

- **核心技巧**：  
  1. **BFS 预处理**——把棋盘上“骑士最短步数”一次性算好，后面查询瞬间完成。  
  2. **位掩码 DP（Min‑Max 版）**——把“所有排列”压缩成 “剩余集合 + 当前所在点 + 谁的回合”。  

- **该技巧适用的题型**（列举 2~3 个类似题）  
  - “旅行商问题”类的 **最小/最大路径**（如 “Minimum Time to Visit All Points”）  
  - “棋子移动 + 多目标收集” 的 **状态压缩 DP**（如 “Collect All Keys”）  
  - “双人对抗的最优策略” 需要 **Min‑Max DP**（如 “Stone Game VII”）  

- **一句话总结解题钥匙**  
  > **把“顺序”压进“集合”里，用 DP + 位掩码在指数时间内枚举所有可能的游戏走向。**

---

## 反思

- **第一反应**：看到“骑士+多个目标+两人轮流”，立刻想到 **枚举所有吃子的顺序**，因为顺序决定了每一步的移动距离。  
- **最容易踩的坑**  
  1. **距离计算错误**：骑士的走法比较特殊，必须用 BFS（或已知公式）得到最短步数，不能用曼哈顿距离等普通距离。  
  2. **状态遗漏**：在 DP 中忘记把 “上一次所在位置” (`last`) 纳入状态，会导致后续距离计算使用错误的起点。  
  3. **回合交替的 Min‑Max**：只写了 “取最大值” 的递归，忘记在 Bob 的回合取最小值，结果会得到错误的总步数。  
- **下次遇到同类题**，第一步应该想到：  
  > **“把所有关键点两两之间的距离先算好”，随后用 “位掩码 + 记忆化递归” 来遍历剩余目标集合，并在递归里根据当前玩家的目标（最大化/最小化）做对应的选择。**