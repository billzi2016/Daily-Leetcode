# #130. 被围绕的地区 / Surrounded Regions

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/surrounded-regions/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:
To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.

**Examples**

**Example 1:**

```
Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
Explanation:
In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.
```

**Example 2:**

```
Input: board = [["X"]]
Output: [["X"]]
```

**Constraints**

- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'.

---

## 题目（中文翻译）

给定一个 **m 行 n 列的矩阵** `board`，其中只包含字符 `'X'` 和 `'O'`。请捕获所有被围绕的区域（region）：

- 要捕获一个被围绕的区域，需要在原矩阵上 **就地**（in‑place）将该区域内所有的 `'O'` 替换为 `'X'`。函数无需返回任何值。

---

### 示例

#### 示例 1  
**Input:**  
```python
board = [["X","X","X","X"],
         ["X","O","O","X"],
         ["X","X","O","X"],
         ["X","O","X","X"]]
```

**Output:**  
```python
[["X","X","X","X"],
 ["X","X","X","X"],
 ["X","X","X","X"],
 ["X","O","X","X"]]
```

**Explanation:**  
如上图所示，最下方的 `'O'` 所在的区域没有被捕获，因为它位于矩阵的边缘，无法被完全围住。

#### 示例 2  
**Input:**  
```python
board = [["X"]]
```

**Output:**  
```python
[["X"]]
```

---

### 约束条件

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 200`
- `board[i][j]` 为 `'X'` 或 `'O'`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把每一个 'O' 当作起点，检查它能否走到棋盘的边界**。  
如果从这个 'O' 出发，沿上下左右四个方向一直走，只要碰到边界上的 'O'（或者走到边界外），说明这个 'O' 属于“未被围住”的区域，**不能**被翻成 'X'；否则，它所在的连通块全部被 'X' 包围，就可以全部翻成 'X'。  

- **用到的数据结构**：  
  - **栈 / 队列**：在遍历连通块时，需要暂时保存待访问的格子位置。可以把栈想象成“待检查的房间钥匙”，把队列想象成“排队等候的乘客”。  
  - **visited 集合**（二维布尔数组）：记录哪些格子已经检查过，防止重复遍历。相当于在地图上贴了“已经走过”的标记，避免走回头路。  

- **为什么正确**：  
  - 每个连通块（相邻的 O 形成的区域）要么至少有一个格子接触到棋盘边缘，要么全部被 X 包围。只要我们能判断该块是否触边，就能决定是否翻转。  

- **复杂度分析（大白话）**：  
  - **时间**：我们对每个格子最多访问一次（进栈/队列一次），但在最坏情况下，每次检查一个连通块都要遍历整个棋盘，导致 **O(m·n·k)**，其中 k 是连通块的数量，最坏等价于 **O((m·n)²)**。可以把它想象成“每检查一个房间，都要把整座大楼走一遍”。  
  - **空间**：需要额外的 visited 数组和栈/队列，最坏情况下会装下所有格子，空间是 **O(m·n)**。  

#### 代码（Python）  

```python
from collections import deque
from typing import List

def solve_bruteforce(board: List[List[str]]) -> None:
    """
    暴力解：对每个 'O' 做一次 BFS，判断它的连通块是否能到达边界。
    直接在原数组上修改。
    """
    if not board:
        return

    m, n = len(board), len(board[0])
    visited = [[False] * n for _ in range(m)]   # 记录是否已经检查过

    # 四个方向：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(m):
        for j in range(n):
            # 只对未访问的 'O' 开始 BFS
            if board[i][j] == 'O' and not visited[i][j]:
                # 保存当前连通块的所有坐标
                component = []
                # 是否能触及边缘的标记
                touches_edge = False

                # 使用队列实现 BFS
                q = deque()
                q.append((i, j))
                visited[i][j] = True

                while q:
                    x, y = q.popleft()
                    component.append((x, y))

                    # 若坐标在边缘，则该块不能翻转
                    if x == 0 or x == m - 1 or y == 0 or y == n - 1:
                        touches_edge = True

                    # 向四个方向扩展
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        # 必须在棋盘内且是 'O' 且未访问过
                        if 0 <= nx < m and 0 <= ny < n \
                                and board[nx][ny] == 'O' and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))

                # BFS 结束后，如果整块不触边，就把它全改成 'X'
                if not touches_edge:
                    for x, y in component:
                        board[x][y] = 'X'
```

#### 复杂度  

- **时间复杂度**：**O((m·n)²)**（最坏情况每个 'O' 都要遍历整个棋盘）  
  - 这里的 O(m·n) 表示棋盘上格子的总数。平方的意思是“遍历次数乘以格子数”。  
- **空间复杂度**：**O(m·n)**（额外的 visited 数组和 BFS 队列）  

---  

### 2. 最优解  

#### 思路  

从暴力解我们看到，**瓶颈在于每次都要重新遍历整块区域**。实际上，只要 **一次遍历** 就能把所有 “不该翻转” 的 ‘O’ 标记出来，剩下的直接翻成 ‘X’。  

关键观察：  
- 只有 **与边缘相连的 O** 才是安全的。  
- 只要我们从所有 **边缘的 O** 出发，沿四个方向把它们能 reach 到的所有 O 全部标记为 “安全”，其余的 O 必然被 X 包围。  

实现思路可以有两种常见方式：**DFS/BFS 从边缘扩散** 或 **并查集（Union‑Find）**。这里用 **DFS**（递归或显式栈）来解释，因为它直观且代码简洁。  

步骤如下：  

1. **遍历四条边**（第一行、最后一行、第一列、最后一列），把每个遇到的 `'O'` 当作起点，执行 **深度优先搜索**（DFS），把所有能到达的 `'O'` 改成临时标记（如 `'E'`，表示 “Edge‑connected”）。  
   - 想象把边缘的 O 当作“海岸线”，从海岸线向内渗透，把所有能被海水浸润的格子涂成蓝色。  
2. **第二遍遍历整个棋盘**：  
   - 把仍然是 `'O'` 的格子改成 `'X'`（这些是被围住的）。  
   - 把标记为 `'E'` 的格子恢复成 `'O'`（这些是安全的）。  

这样只需要 **两次线性遍历**，时间就是 **O(m·n)**，空间只用了递归栈（最坏 O(m·n)）或显式栈，满足题目要求。  

**为什么正确**：  
- 所有安全的 O 必然和至少一个边缘 O 连通。我们从每个边缘 O 出发，把所有连通的 O 都标记为安全。  
- 其余没有被标记的 O，必然没有任何通向边缘的路径，换句话说，它们被 X 完全包围。  

#### 代码（Python）  

```python
from typing import List

def solve(board: List[List[str]]) -> None:
    """
    最优解：从四条边的 'O' 出发，用 DFS 把所有能到达的 'O' 标记为 'E'，
    再统一遍历一次完成翻转。
    直接在原 board 上修改，符合题目要求。
    """
    if not board:
        return

    m, n = len(board), len(board[0])

    # 定义四个方向的移动向量
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 深度优先搜索（递归版），把连通的 'O' 改成 'E'
    def dfs(x: int, y: int) -> None:
        # 越界或不是 'O' 时直接返回
        if x < 0 or x >= m or y < 0 or y >= n or board[x][y] != 'O':
            return
        board[x][y] = 'E'               # 标记为 “边缘安全”
        # 继续向四个方向扩散
        for dx, dy in dirs:
            dfs(x + dx, y + dy)

    # 1️⃣ 从四条边的每个格子开始搜索
    for i in range(m):
        # 第一列
        if board[i][0] == 'O':
            dfs(i, 0)
        # 最后一列
        if board[i][n - 1] == 'O':
            dfs(i, n - 1)

    for j in range(n):
        # 第一行
        if board[0][j] == 'O':
            dfs(0, j)
        # 最后一行
        if board[m - 1][j] == 'O':
            dfs(m - 1, j)

    # 2️⃣ 第二遍遍历：翻转并恢复标记
    for i in range(m):
        for j in range(n):
            if board[i][j] == 'O':      # 没被标记，说明被围住
                board[i][j] = 'X'
            elif board[i][j] == 'E':    # 安全的恢复成原来的 'O'
                board[i][j] = 'O'
```

> **提示**：如果担心递归深度超过 Python 默认的递归限制（约 1000），可以改用显式栈实现迭代版 DFS，或者改用 BFS（queue），思路完全相同。

#### 复杂度  

- **时间复杂度**：**O(m·n)**  
  - 我们只遍历了棋盘两次，每个格子最多被访问常数次。相当于“只走一遍棋盘”。  
- **空间复杂度**：**O(m·n)**（递归栈最坏情况下会占用整个棋盘的深度）  
  - 若改为显式栈或 BFS，额外空间仍是 O(m·n) 的队列/栈，但在平均情况下会更小。  

---  

## 心得  

- **核心技巧**：从 **“边缘出发的扩散”**（DFS/BFS）来辨别哪些区域是安全的。  
- **该技巧适用的题型**：  
  1. **岛屿问题**（如 “Number of Islands”，需要从边缘或特定点遍历）  
  2. **捕获区域**（本题）  
  3. **矩阵中的连通块标记**（如 “Walls and Gates”）  
- **一句话总结解题钥匙**：**只要把所有与边界相连的 O 标记出来，剩下的 O 必然被围住，直接翻成 X**。  

---  

## 反思  

- **第一反应**：看到 “被围住的区域” 立刻想到 “找连通块”，于是想对每个 O 做一次遍历检查。  
- **最容易踩的坑**：  
  - **边界条件**：忘记检查四条边的所有格子（包括四个角），导致某些安全的 O 被错误翻转。  
  - **递归深度**：在极端的 200×200 全是 O 的情况下，递归会超过 Python 的默认栈深度，需要改为迭代实现。  
  - **原地修改**：直接把 O 改成 X 再去检查会破坏后续的搜索，需要使用临时标记（如 'E'）来区分已访问的安全 O。  
- **下次遇到同类题**，第一步应该问自己：“**哪些格子是一定安全的？**”，通常答案是“**与边缘或特殊入口相连的格子**”。先把这些安全格子标记或并入同一集合，再统一处理其余格子。