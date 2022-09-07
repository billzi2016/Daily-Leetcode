# #1926. 最近的出口 / Nearest Exit from Entrance in Maze

> 难度：中等 · 标签：Array、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/nearest-exit-from-entrance-in-maze/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix maze (0-indexed) with empty cells (represented as '.') and walls (represented as '+'). You are also given the entrance of the maze, where entrance = [entrancerow, entrancecol] denotes the row and column of the cell you are initially standing at.
In one step, you can move one cell up, down, left, or right. You cannot step into a cell with a wall, and you cannot step outside the maze. Your goal is to find the nearest exit from the entrance. An exit is defined as an empty cell that is at the border of the maze. The entrance does not count as an exit.
Return the number of steps in the shortest path from the entrance to the nearest exit, or -1 if no such path exists.

**Examples**

**Example 1:**

```
Input: maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]
Output: 1
Explanation: There are 3 exits in this maze at [1,0], [0,2], and [2,3].
Initially, you are at the entrance cell [1,2].
- You can reach [1,0] by moving 2 steps left.
- You can reach [0,2] by moving 1 step up.
It is impossible to reach [2,3] from the entrance.
Thus, the nearest exit is [0,2], which is 1 step away.
```

**Example 2:**

```
Input: maze = [["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0]
Output: 2
Explanation: There is 1 exit in this maze at [1,2].
[1,0] does not count as an exit since it is the entrance cell.
Initially, you are at the entrance cell [1,0].
- You can reach [1,2] by moving 2 steps right.
Thus, the nearest exit is [1,2], which is 2 steps away.
```

**Example 3:**

```
Input: maze = [[".","+"]], entrance = [0,0]
Output: -1
Explanation: There are no exits in this maze.
```

**Constraints**

- maze.length == m
- maze[i].length == n
- 1 <= m, n <= 100
- maze[i][j] is either '.' or '+'.
- entrance.length == 2
- 0 <= entrancerow < m
- 0 <= entrancecol < n
- entrance will always be an empty cell.

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m x n` 的矩阵 `maze`（0 索引），矩阵中的空格用 `'.'` 表示，墙壁用 `'+'` 表示。还给定迷宫的入口 `entrance`，其中 `entrance = [entrancerow, entrancecol]` 表示你最初站立的单元格的行号和列号。

一次移动可以向上、下、左、右任意一个方向移动一个单元格。不能移动到墙壁单元格，也不能移动到矩阵之外。你的目标是找到从入口最近的出口。**出口** 定义为位于迷宫边界上的空格单元格，入口本身不算作出口。

返回从入口到最近出口的最短路径的步数；如果不存在这样的路径，返回 `-1`。

**示例 1**  
```text
Input: maze = [["+","+",".","+"],
               [".",".",".","+"],
               ["+","+","+","." ]],
       entrance = [1,2]
Output: 1
Explanation: 本迷宫共有 3 个出口，分别位于 [1,0]、[0,2] 和 [2,3]。  
初始时，你站在入口单元格 [1,2]。  
- 向左移动 2 步可到达 [1,0]。  
- 向上移动 1 步可到达 [0,2]。  
从入口无法到达 [2,3]。  
因此最近的出口是 [0,2]，步数为 **1**。
```

**示例 2**  
```text
Input: maze = [["+","+","+"],
               [".",".","."],
               ["+","+","+"]],
       entrance = [1,0]
Output: 2
Explanation: 该迷宫唯一的出口位于 [1,2]。  
入口单元格 [1,0] 本身不算作出口。  
从入口出发，向右移动 2 步即可到达 [1,2]。  
最近的出口是 [1,2]，步数为 **2**。
```

**示例 3**  
```text
Input: maze = [[".", "+"]],
       entrance = [0,0]
Output: -1
Explanation: 该迷宫没有任何出口。
```

**约束条件**  

- `maze.length == m`
- `maze[i].length == n`
- `1 ≤ m, n ≤ 100`
- `maze[i][j]` 只能是 `'.'` 或 `'+'`
- `entrance.length == 2`
- `0 ≤ entrancerow < m`
- `0 ≤ entrancecol < n`
- `entrance` 必定是一个空格单元格 (`'.'`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都穷举一遍**，找出能到达边界的最短路径。  
可以把迷宫看成一个棋盘，每走一步就往四个方向（上、下、左、 right）尝试一次，直到：

1. 走出迷宫的墙（`+`），这条路就不可行，直接回溯；
2. 走到边界的空格（`.`），记录走了多少步，和当前最小步数比较。

这里使用的核心数据结构是**递归栈**（隐式的函数调用栈）或**显式的深度优先搜索（DFS）**的栈。  
类比：DFS 就像在森林里找宝藏，你每走进一条小路，就把这条路记下来（压栈），走不通了再回头（弹栈）。

**为什么正确**  
DFS 会遍历**所有**从入口出发的可达路径，只要路径能到达边界，就会被检查到；取最小步数自然就是最近的出口。

**时间/空间复杂度**  
- 时间复杂度：在最坏情况下，每个空格都会被访问一次，并且每次访问会尝试四个方向。若迷宫有 `m × n` 个格子，时间复杂度约为 `O(4^{mn})`，实际表现接近 `O(m·n·4)`，但因为会出现大量重复遍历，整体是指数级的，难以接受。  
- 空间复杂度：递归深度最坏是 `m·n`，即 `O(m·n)`（栈空间），加上保存 visited 的布尔矩阵也需要 `O(m·n)`。

> **大白话**：`O(m·n)` 就像说“如果迷宫有 10000 格子，最多会占用 10000 个格子大小的内存”。`O(4^{mn})` 则是说“每走一步都有 4 种选择，步数越多，可能的情况会像指数一样爆炸”。

#### 代码（Python）

```python
from typing import List

def nearestExit_bruteforce(maze: List[List[str]], entrance: List[int]) -> int:
    m, n = len(maze), len(maze[0])
    sr, sc = entrance
    # 记录最小步数，初始为无限大
    best = float('inf')
    # 方向向量：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 深度优先搜索（递归版）
    def dfs(r: int, c: int, steps: int, visited: List[List[bool]]):
        nonlocal best
        # 剪枝：已经比当前最好的答案更差，直接返回
        if steps >= best:
            return
        # 如果走到了边界且不是入口本身，就是一个出口
        if (r != sr or c != sc) and (r == 0 or r == m-1 or c == 0 or c == n-1):
            best = steps          # 更新最小步数
            return
        # 四个方向继续探索
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            # 合法性检查：在矩阵内部、不是墙、且未访问过
            if 0 <= nr < m and 0 <= nc < n and maze[nr][nc] == '.' and not visited[nr][nc]:
                visited[nr][nc] = True
                dfs(nr, nc, steps + 1, visited)
                visited[nr][nc] = False   # 回溯，撤销标记

    # 初始化 visited 矩阵
    visited = [[False] * n for _ in range(m)]
    visited[sr][sc] = True
    dfs(sr, sc, 0, visited)

    return -1 if best == float('inf') else best
```

#### 复杂度

- **时间复杂度**：`O(4^{m·n})`（指数级）——每一步都有 4 条分支，遍历所有可能路径会非常慢。  
- **空间复杂度**：`O(m·n)`——主要是递归栈和 visited 矩阵占用的空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈在于大量重复遍历**。  
我们需要一种**一次遍历就能得到每个格子到入口的最短步数** 的方法，这正是**广度优先搜索（Breadth‑First Search, BFS）** 的特性：

- BFS 按层（step）展开：第一层是所有距离入口 1 步的格子，第二层是距离 2 步的格子……  
- 第一次碰到出口时，必然是最近的出口，因为 BFS 保证了“先到的路径一定是最短的”。

**核心算法**：  
1. 把入口加入队列 `queue`，并标记为已访问。  
2. 循环取出队首 `(r, c, steps)`，检查它的四个相邻格子：  
   - 若相邻格子是墙 `+` 或已经访问过，直接跳过。  
   - 若相邻格子是空格 `.`，判断它是否在边界且不是入口本身：是的话返回 `steps + 1`（因为我们已经走了一步）。  
   - 否则把相邻格子加入队列，步数设为 `steps + 1`，并标记为已访问。  
3. 队列空了仍未找到出口，说明没有可达的出口，返回 `-1`。

**为什么 BFS 能做到最优**  
- 每个格子只会被放入队列一次（因为一旦访问就不再重复），所以总的遍历次数是 `O(m·n)`。  
- 由于 BFS 按层展开，第一次到达的出口必然是最近的，省去了比较所有路径的过程。

**类比**：想象你在一座城市里找最近的地铁站，先把所有离你 1 公里的地方检查一遍，若没有，再检查 2 公里、3 公里……，这就是 BFS 的“逐层扩散”。

#### 代码（Python）

```python
from collections import deque
from typing import List

def nearestExit(maze: List[List[str]], entrance: List[int]) -> int:
    m, n = len(maze), len(maze[0])
    sr, sc = entrance
    # 四个方向
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # visited 用来防止重复进入同一个格子
    visited = [[False] * n for _ in range(m)]
    visited[sr][sc] = True

    # 队列中存 (行, 列, 已走步数)
    q = deque()
    q.append((sr, sc, 0))

    while q:
        r, c, steps = q.popleft()
        # 向四个方向尝试
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            # 越界或是墙直接跳过
            if not (0 <= nr < m and 0 <= nc < n) or maze[nr][nc] == '+':
                continue
            # 已经访问过的也跳过
            if visited[nr][nc]:
                continue
            # 标记已访问
            visited[nr][nc] = True
            # 如果是边界且不是入口本身，找到最近出口
            if nr == 0 or nr == m-1 or nc == 0 or nc == n-1:
                return steps + 1      # 再走一步到达出口
            # 否则继续往队列里放，步数+1
            q.append((nr, nc, steps + 1))

    # 没有任何出口可达
    return -1
```

#### 复杂度

- **时间复杂度**：`O(m·n)` ——每个格子最多被访问一次，四个方向的检查是常数时间。与暴力解相比，指数级的爆炸被降到了线性。  
- **空间复杂度**：`O(m·n)` ——`visited` 矩阵和 BFS 队列最坏情况下会同时存储整个迷宫的格子。

---

## 心得

- **核心技巧**：广度优先搜索（BFS）求最短路径。  
- **适用场景**：  
  1. **迷宫/网格最短路径**（如 `Shortest Path in Binary Matrix`）。  
  2. **棋盘上最少步数到达目标**（如 `Knight Minimum Moves`）。  
  3. **社交网络中最短关系链**（如 `Six Degrees of Separation`）。  
- **一句话总结**：  
  “想要在无权图里找最近的目标，就让 BFS 按层扩散，第一时间碰到的就是答案。”

## 反思

- **第一反应**：看到“最短步数”立刻想到 BFS，然而最初可能会被“只能向四个方向移动”这点误导，以为需要 DP 或回溯。  
- **最容易踩的坑**：  
  - **入口本身不算出口**，所以在判断边界时要排除入口坐标。  
  - **墙体 `+` 不能进入**，忘记检查会导致无限循环或错误的路径计数。  
  - **边界条件**：单行或单列的迷宫，需要正确判断是否真的有出口。  
- **下次遇到同类题**：第一步就问自己“是否是无权图的最短路径？”——如果答案是 Yes，立刻选 BFS，并准备好 `visited` 防止重复。