# #909. 蛇梯棋 / Snakes and Ladders

> 难度：中等 · 标签：Array、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/snakes-and-ladders/)

---

## 题目（英文原版）

**Description**

You are given an n x n integer matrix board where the cells are labeled from 1 to n2 in a Boustrophedon style starting from the bottom left of the board (i.e. board[n - 1][0]) and alternating direction each row.
You start on square 1 of the board. In each move, starting from square curr, do the following:
A board square on row r and column c has a snake or ladder if board[r][c] != -1. The destination of that snake or ladder is board[r][c]. Squares 1 and n2 are not the starting points of any snake or ladder.
Note that you only take a snake or ladder at most once per dice roll. If the destination to a snake or ladder is the start of another snake or ladder, you do not follow the subsequent snake or ladder.
Return the least number of dice rolls required to reach the square n2. If it is not possible to reach the square, return -1.

**Examples**

**Example 1:**

```
Input: board = [[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,35,-1,-1,13,-1],[-1,-1,-1,-1,-1,-1],[-1,15,-1,-1,-1,-1]]
Output: 4
Explanation: 
In the beginning, you start at square 1 (at row 5, column 0).
You decide to move to square 2 and must take the ladder to square 15.
You then decide to move to square 17 and must take the snake to square 13.
You then decide to move to square 14 and must take the ladder to square 35.
You then decide to move to square 36, ending the game.
This is the lowest possible number of moves to reach the last square, so return 4.
```

**Example 2:**

```
Input: board = [[-1,-1],[-1,3]]
Output: 1
```

**Constraints**

- n == board.length == board[i].length
- 2 <= n <= 20
- board[i][j] is either -1 or in the range [1, n2].
- The squares labeled 1 and n2 are not the starting points of any snake or ladder.

---

## 题目（中文翻译）

**描述**  
给定一个 `n × n` 的整数矩阵 `board`，其中格子按照**之字形**（Boustrophedon）从左下角 (`board[n‑1][0]`) 开始依次编号为 `1` 到 `n²`，每一行的方向交替。  
玩家从编号为 `1` 的格子开始。每一次掷骰子，从当前格子 `curr` 按以下规则移动：

- 若格子位于第 `r` 行第 `c` 列且 `board[r][c] != -1`，则该格子上有一条**蛇**（snake）或**梯子**（ladder），其目的地为 `board[r][c]`。格子 `1` 和 `n²` 不会是任何蛇或梯子的起点。
- 在一次掷骰子中最多只能使用一次蛇或梯子。即使蛇/梯子的目的地恰好是另一条蛇或梯子的起点，也**不**继续沿其移动。

返回到达格子 `n²` 所需的最少掷骰子次数；如果无法到达，返回 `-1`。

**示例 1**  

```text
Input: board = [[-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1],
                [-1,-1,-1,-1,-1,-1],
                [-1,35,-1,-1,13,-1],
                [-1,-1,-1,-1,-1,-1],
                [-1,15,-1,-1,-1,-1]]
Output: 4
Explanation:
- 起始时位于格子 1（第 5 行，第 0 列）。
- 决定向前移动到格子 2，必须乘坐梯子到格子 15。
- 接着移动到格子 17，必须沿蛇滑到格子 13。
- 再移动到格子 14，必须乘坐梯子到格子 35。
- 最后移动到格子 36，游戏结束。

这是到达最后一个格子所需的最少步数，故返回 4。
```

**示例 2**  

```text
Input: board = [[-1,-1],
                [-1,3]]
Output: 1
```

**约束条件**  
- `n == board.length == board[i].length`
- `2 ≤ n ≤ 20`
- `board[i][j]` 为 `-1` 或者位于 `[1, n²]` 区间的整数
- 编号为 `1` 和 `n²` 的格子不是任何蛇或梯子的起点。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一次掷骰子看成一次“走一步”**，从起点 `1` 开始，尝试所有可能的掷出点数（1~6），看能否到达终点 `n²`。  
这其实是 **在一个无向图里做最短路径搜索**：

* 每个格子（编号 1 … n²）是图中的一个节点。  
* 从节点 `i` 可以通过一次掷骰子跳到 `i+1 … i+6`（如果超过 `n²` 则不算）。  
* 如果目标格子上有蛇或梯子（`board[r][c] != -1`），我们必须 **立即** 把它搬到对应的目的格子，这相当于在图里把 `i+dx` 与 `board[r][c]` 合并成同一个节点。

因为每一次掷骰子都算 **一步**，我们只需要找 **最少的步数** 能从 1 走到 `n²`。这正好可以用 **广度优先搜索（BFS）** 完成——BFS 会一次遍历所有「一步能到达」的格子，层层向外扩展，第一次碰到终点时的层数就是答案。

> **生活化类比**：  
> 把棋盘想象成一座城市的十字路口，每次掷骰子就是在街上随意走 1~6 步。如果走到的路口有“快速通道”（蛇或梯子），你立刻坐上它直接抵达另一座城市的路口。要找最少的步数，就是要找最短的“换乘”次数。

**为什么正确**：  
BFS 的核心性质是：**先进入队列的节点一定是最短路径**。因为每一次我们只向前推进“一步”，所以当我们第一次把终点 `n²` 加入队列时，恰好是走了最少的骰子次数。

**时间/空间复杂度**（大白话）：

| 项目 | 说明 |
|------|------|
| 时间复杂度 | `O(n² * 6)` ≈ `O(n²)`。我们最多访问每个格子一次，每次遍历最多 6 条边（骰子点数）。对 n=20（最大 400 格子）来说，最多只遍历约 2400 条边，完全够快。 |
| 空间复杂度 | `O(n²)`。需要一个 `visited` 数组记住哪些格子已经走过，还要保存 BFS 队列里最多 `n²` 个格子。 |

#### 代码（Python）

```python
from collections import deque
from typing import List

def snakes_and_ladders(board: List[List[int]]) -> int:
    n = len(board)                     # 棋盘的行列数
    # ---------- 辅助函数：把 1~n² 的编号转成矩阵坐标 ----------
    def id_to_pos(s: int):
        """返回编号 s 在 board 中的 (row, col)"""
        # 行号：从底部往上数，0 表示最后一行
        row = n - 1 - (s - 1) // n
        # 列号：每行的方向交替
        col = (s - 1) % n
        if (n - 1 - row) % 2 == 1:    # 如果是从右往左的那一行，需要反向
            col = n - 1 - col
        return row, col

    # ---------- BFS ----------
    visited = [False] * (n * n + 1)    # 下标从 1 开始，0 位置不使用
    q = deque()
    q.append((1, 0))                    # (当前格子编号, 已用的掷骰子次数)
    visited[1] = True

    while q:
        cur, step = q.popleft()
        if cur == n * n:                # 到达最后一个格子
            return step

        # 掷出 1~6 点
        for dice in range(1, 7):
            nxt = cur + dice
            if nxt > n * n:              # 超出棋盘直接跳过
                continue

            r, c = id_to_pos(nxt)        # 找到对应的坐标
            if board[r][c] != -1:        # 有蛇或梯子，直接搬到目的格子
                nxt = board[r][c]

            if not visited[nxt]:
                visited[nxt] = True
                q.append((nxt, step + 1))

    # BFS 结束仍未到达终点，说明不可达
    return -1
```

#### 复杂度

- **时间复杂度**：`O(n²)` ——我们最多遍历 `n²`（最多 400）个格子，每个格子检查常数 6 条边。
- **空间复杂度**：`O(n²)` ——`visited` 数组和 BFS 队列都需要存储至多 `n²` 个编号。

---

### 2. 最优解

#### 思路  

从暴力解来看，真正的**瓶颈**只在于**坐标转换**——每次从编号到二维坐标的映射如果写得不清晰，会导致代码难懂、容易出错。  
优化的方向其实是**把这一步抽象成一个 O(1) 的函数**，并在 BFS 中**一次性完成**：

1. **预处理**：我们不需要额外的预处理，只要把“编号 → 坐标”封装好，后面每次使用都是常数时间。  
2. **一次 BFS 即可**：因为每一步的搜索空间只有 6 条边，BFS 已经是最短路径的最优算法，无法再把时间复杂度降到更低（`O(n²)` 已经是线性级别）。  
3. **细节优化**：  
   - 使用 `deque` 实现队列，`popleft` 为 O(1)。  
   - 在遍历 dice 时直接跳过已经访问过的格子，避免重复入队。  
   - 当掷出的点数导致的格子已经是终点时，直接返回 `step + 1`，可以稍微提前结束。

核心数据结构仍是 **队列**（BFS）和 **哈希表/数组**（记录访问），但我们把 **坐标映射**的“蛇梯子方向交替”解释得更细致，帮助初学者彻底弄清楚。

> **类比**：  
> 想象你在玩「楼梯与滑梯」的儿童游戏，每次只能前进 1~6 步。只要你每走一步就记下「已经去过的格子」，再也不会重复踩同一个格子——这就是 BFS 的“记忆”。坐标映射就像把「第几步」翻译成「在左边还是右边」的口令，翻译一次就能直接使用。

#### 代码（Python）

```python
from collections import deque
from typing import List

def snakes_and_ladders(board: List[List[int]]) -> int:
    n = len(board)

    # ---------- 坐标映射（一次写好，后面直接调用） ----------
    def id_to_pos(num: int):
        """
        把编号 num (1 ~ n²) 转成 board 的 (row, col)。
        关键点：每行的方向是交替的，奇数行从左到右，偶数行从右到左。
        """
        # 从底往上数的行号（0 表示最底层）
        row = n - 1 - (num - 1) // n
        # 该行在左→右时的列号
        col = (num - 1) % n
        # 如果该行是“右→左”，把列号反转
        if ((n - 1 - row) & 1) == 1:   # 奇数行（从右往左）
            col = n - 1 - col
        return row, col

    # ---------- BFS ----------
    visited = [False] * (n * n + 1)
    q = deque([(1, 0)])          # (格子编号, 已用的掷骰子次数)
    visited[1] = True

    while q:
        cur, step = q.popleft()
        if cur == n * n:
            return step          # 已经到达终点

        for dice in range(1, 7):
            nxt = cur + dice
            if nxt > n * n:
                continue

            r, c = id_to_pos(nxt)
            if board[r][c] != -1:        # 蛇或梯子
                nxt = board[r][c]

            if not visited[nxt]:
                visited[nxt] = True
                # 若 nxt 已经是终点，直接返回 step+1，可提前结束
                if nxt == n * n:
                    return step + 1
                q.append((nxt, step + 1))

    # BFS 完成仍未到达终点，说明不可达
    return -1
```

#### 复杂度

- **时间复杂度**：`O(n²)` ——每个格子只会入队一次，遍历 6 条可能的边，整体仍是线性级别。与暴力解唯一的区别是坐标映射是常数时间、代码更简洁。
- **空间复杂度**：`O(n²)` ——`visited` 与队列的最大规模均为 `n²`。

---

## 心得

- **核心技巧**：**广度优先搜索（BFS）** 用来求最短步数；**坐标映射** 把“一维编号”转成二维矩阵坐标（要注意行方向交替）。
- **适用题型**：
  1. 任何**最少步数**或**最少操作次数**的格子/棋盘问题（如“迷宫最短路径”）。
  2. **跳格子**类游戏（如“跳棋”“跳方块”），每次可以跳固定范围的格子。
  3. **状态空间有限**、每一步转移固定的题目（如“打开锁”）。
- **一句话总结**：**把棋盘抽象成图，用 BFS 按层遍历，第一次碰到终点即是最少掷骰子次数**。

---

## 反思

- **第一反应**：把棋盘想成一个普通的二维数组，直接用双层循环模拟每一步，结果会陷入指数级的搜索——没有意识到这是一张“图”，应该用 BFS。
- **最容易踩的坑**  
  1. **坐标映射错误**：忘记每行的方向交替，会导致蛇/梯子位置错位。  
  2. **重复访问**：不使用 `visited`，同一个格子会被多次加入队列，导致时间爆炸。  
  3. **边界条件**：掷出的点数超过 `n²` 时要直接跳过，否则会出现数组越界。  
  4. **蛇梯子只能使用一次**：抵达目的格子后不再继续检查是否还有另一条蛇/梯子。
- **下次类似题目**的第一步**：先把题目抽象成“每一步的状态转移”，判断是否可以用 BFS（或 DFS、DP）求最短路径；随后实现 **状态 ↔︎ 坐标** 的转换函数，确保不遗漏交替方向的细节。