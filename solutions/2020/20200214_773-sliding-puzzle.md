# #773. **滑动拼图** / Sliding Puzzle

> 难度：困难 · 标签：Array、Dynamic Programming、Backtracking、Breadth-First Search、Memoization、Matrix · [LeetCode 链接](https://leetcode.com/problems/sliding-puzzle/)

---

## 题目（英文原版）

**Description**

On an 2 x 3 board, there are five tiles labeled from 1 to 5, and an empty square represented by 0. A move consists of choosing 0 and a 4-directionally adjacent number and swapping it.
The state of the board is solved if and only if the board is [[1,2,3],[4,5,0]].
Given the puzzle board board, return the least number of moves required so that the state of the board is solved. If it is impossible for the state of the board to be solved, return -1.

**Examples**

**Example 1:**

```
Input: board = [[1,2,3],[4,0,5]]
Output: 1
Explanation: Swap the 0 and the 5 in one move.
```

**Example 2:**

```
Input: board = [[1,2,3],[5,4,0]]
Output: -1
Explanation: No number of moves will make the board solved.
```

**Example 3:**

```
Input: board = [[4,1,2],[5,0,3]]
Output: 5
Explanation: 5 is the smallest number of moves that solves the board.
An example path:
After move 0: [[4,1,2],[5,0,3]]
After move 1: [[4,1,2],[0,5,3]]
After move 2: [[0,1,2],[4,5,3]]
After move 3: [[1,0,2],[4,5,3]]
After move 4: [[1,2,0],[4,5,3]]
After move 5: [[1,2,3],[4,5,0]]
```

**Constraints**

- board.length == 2
- board[i].length == 3
- 0 <= board[i][j] <= 5
- Each value board[i][j] is unique.

---

## 题目（中文翻译）

在一个 `2 x 3` 的棋盘上，有编号为 `1` 到 `5` 的五块棋子，以及用 `0` 表示的空格。一次移动指的是选择 `0` 与其四向相邻（up, down, left, right）的数字并交换位置。  

当且仅当棋盘的状态为 `[[1,2,3],[4,5,0]]` 时，称该棋盘已解决。  

给定初始棋盘 `board`，返回使棋盘状态达到已解决所需的最少移动次数。如果无论如何都无法将棋盘解决，则返回 `-1`。

---

### 示例

#### 示例 1
**输入:** `board = [[1,2,3],[4,0,5]]`  
**输出:** `1`  
**解释:** 在一次移动中将 `0` 与 `5` 交换。

#### 示例 2
**输入:** `board = [[1,2,3],[5,4,0]]`  
**输出:** `-1`  
**解释:** 无论进行多少次移动，都无法使棋盘达到已解决状态。

#### 示例 3
**输入:** `board = [[4,1,2],[5,0,3]]`  
**输出:** `5`  
**解释:** `5` 是使棋盘解决的最小移动次数。示例路径如下：

- 移动 0 后: `[[4,1,2],[5,0,3]]`
- 移动 1 后: `[[4,1,2],[0,5,3]]`
- 移动 2 后: `[[0,1,2],[4,5,3]]`
- 移动 3 后: `[[1,0,2],[4,5,3]]`
- 移动 4 后: `[[1,2,0],[4,5,3]]`
- 移动 5 后: `[[1,2,3],[4,5,0]]`

---

### 约束条件

- `board.length == 2`
- `board[i].length == 3`
- `0 <= board[i][j] <= 5`
- 每个 `board[i][j]` 的取值唯一。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每一步的所有可能移动都穷举下来**，一直往下走，直到出现目标状态 `[[1,2,3],[4,5,0]]` 为止。  
这相当于在一棵“决策树”里深度优先地走每一条分支——每个节点是一种棋盘布局，孩子节点就是把空格 `0` 与它上下左右相邻的数字交换后得到的新布局。  

- **使用的数据结构**  
  - **列表 `board`**：直接保存 2×3 的棋盘，像是我们手里的一块拼图。  
  - **递归函数**：模拟“走一步”，把当前布局变成下一步的布局，然后继续往下搜索。  
  - **全局变量 `best`**：记录目前找到的最少步数。  

> 类比：把这道题想成在迷宫里找出口，我们每次只能往四个方向走一步，**暴力搜索** 就是把每一条可能的路都走一遍，哪怕会走回头路。

- **为什么一定能得到答案**  
  - 只要把所有合法的移动都尝试到，就不可能漏掉真正的最短路径。只不过搜索过程会非常“啰嗦”，会把很多已经走过的相同布局重复遍历。

- **复杂度分析（大白话）**  
  - 每一步最多有 4 种移动（上、下、左、右），所以深度为 `d` 时，分支数大约是 `4^d`。  
  - 棋盘一共有 6! = 720 种不同的排列（因为数字 0~5 各不相同），最坏情况下我们可能会遍历全部，这已经是 **指数级**（爆炸式）增长。  
  - **时间复杂度**：`O(4^d)`，这里的 `d` 是答案的步数，实际会远大于 `d`，因为会出现大量重复状态。  
  - **空间复杂度**：递归栈的深度是 `d`，所以是 `O(d)`，但如果把所有遍历过的棋盘都保留下来（防止无限循环），空间会变成 `O(4^d)`。

#### 代码（Python）

```python
from copy import deepcopy

# 目标状态，写成一维列表方便比较
TARGET = [1, 2, 3, 4, 5, 0]

# 四个方向的相邻关系（行、列）
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

best = float('inf')          # 当前找到的最少步数（初始为无穷大）

def board_to_list(board):
    """把二维 board 展平成一维列表，方便比较和哈希"""
    return [num for row in board for num in row]

def dfs(board, zero_pos, depth, visited):
    """
    暴力深度优先搜索
    board      : 当前二维棋盘
    zero_pos   : 空格 0 的坐标 (r, c)
    depth      : 已经走了多少步
    visited    : 已经走过的布局集合，防止死循环（这里仅做最基本的去重）
    """
    global best
    # 剪枝：已经走的步数 >= 已知最优，直接返回
    if depth >= best:
        return

    # 如果已经是目标状态，更新最优解
    if board_to_list(board) == TARGET:
        best = depth
        return

    r, c = zero_pos
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 2 and 0 <= nc < 3:          # 保证在棋盘内部
            # 交换 0 与相邻数字
            board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
            state_key = tuple(board_to_list(board))
            if state_key not in visited:         # 简单去重，防止立刻回到上一步
                visited.add(state_key)
                dfs(board, (nr, nc), depth + 1, visited)
                visited.remove(state_key)        # 回溯，撤销这一步的记录
            # 把棋盘恢复成原样（回溯）
            board[r][c], board[nr][nc] = board[nr][nc], board[r][c]

def slidingPuzzle_bruteforce(board):
    """入口函数，返回最少步数或 -1"""
    global best
    best = float('inf')
    # 找到空格 0 的位置
    for i in range(2):
        for j in range(3):
            if board[i][j] == 0:
                zero = (i, j)
    dfs(board, zero, 0, {tuple(board_to_list(board))})
    return -1 if best == float('inf') else best
```

#### 复杂度

- **时间复杂度**：`O(4^d)`（指数级），因为每一步最多有 4 种选择，且会产生大量重复状态。  
- **空间复杂度**：`O(d)`（递归栈深度），如果把所有访问过的状态都保存，则会达到 `O(4^d)`，这在实际运行时会导致内存爆炸。

---

### 2. 最优解

#### 思路  
暴力搜索的主要瓶颈在于 **大量重复遍历**：同一个棋盘布局会被反复走进、走出，导致搜索空间指数级膨胀。  
要想最快得到最少步数，我们可以把搜索过程视为 **在一个无向图里找最短路径**：

- **图的节点**：所有合法的棋盘布局（最多 720 种）。
- **图的边**：两种布局只要能通过一次合法的 `0` 与相邻数字交换得到，就连一条边，边权都是 1。

在无权图里，**广度优先搜索 (BFS)** 能保证第一次碰到目标状态时，就是最短路径长度。  
因此我们只需要：

1. 把棋盘状态压缩成一个**唯一的、可哈希的表示**（如字符串 `"123450"`），这样才能快速判断“是否已经访问过”。  
2. 预先准备好每个位置 `0` 的合法移动方向，避免每次都计算。  
3. 使用 **队列** 按层遍历，记录每层（即每一步）的状态数目，当目标出现时返回当前层数。  

> 类比：把每一种棋盘想成城市的一个站点，站点之间的直达公交线就是一次合法的交换。我们要找的是从起点到终点的 **最少换乘次数**，而 BFS 就是先坐第一层公交、第二层公交……层层递进，最先到达终点的那一次就是答案。

**核心算法**：广度优先搜索（BFS）+ 哈希表（用来去重）  

**关键技巧**：

- **状态编码**：把二维数组展平成一维字符串，例如 `[[1,2,3],[4,0,5]] → "123405"`。字符串在 Python 中是可哈希的，放进 `set` 检查是否访问过非常快。  
- **邻接表**：因为棋盘只有 6 格，直接写出每个位置 `0` 能移动到哪些位置，例如 `0` 在下标 `0`（左上）时只能和下标 `1`、`3` 交换。这样每次展开子节点只需要 O(1) 的时间。  

#### 代码（Python）

```python
from collections import deque

# 目标状态的字符串形式
TARGET = "123450"

# 0 在每个下标（0~5）上可能交换的位置（上、下、左、右）
NEIGHBORS = {
    0: (1, 3),        # 0 在左上角，只能右或下
    1: (0, 2, 4),     # 中上
    2: (1, 5),        # 右上
    3: (0, 4),        # 左下
    4: (1, 3, 5),     # 中下
    5: (2, 4)         # 右下
}

def slidingPuzzle(board):
    """
    BFS 求最少步数
    :param board: List[List[int]] 2x3 棋盘
    :return: int 最少移动次数，若不可达返回 -1
    """
    # 1. 把二维棋盘压成一维字符串，便于哈希与比较
    start = ''.join(str(num) for row in board for num in row)

    if start == TARGET:               # 起点已经是目标
        return 0

    # 2. BFS 队列：存放 (当前状态字符串, 空格 0 的下标)
    zero_idx = start.index('0')
    q = deque([(start, zero_idx)])
    visited = {start}                 # 已访问集合，防止重复

    steps = 0                         # 已经走了多少层（即多少步）

    while q:
        steps += 1                    # 进入新的一层，步数+1
        for _ in range(len(q)):      # 逐层遍历，保证每层的节点步数相同
            cur_state, cur_zero = q.popleft()
            # 3. 枚举所有可能的交换位置
            for nb in NEIGHBORS[cur_zero]:
                # 把字符串转换为列表便于交换字符
                lst = list(cur_state)
                lst[cur_zero], lst[nb] = lst[nb], lst[cur_zero]   # 交换 0 与相邻数字
                nxt_state = ''.join(lst)

                if nxt_state == TARGET:   # 找到目标，返回步数
                    return steps

                if nxt_state not in visited:
                    visited.add(nxt_state)
                    q.append((nxt_state, nb))   # 把新状态和新的 0 位置加入队列

    # BFS 结束仍未找到，说明不可达
    return -1
```

#### 复杂度

- **时间复杂度**：`O(N)`，其中 `N` 是所有可能状态的数量（最多 720），每个状态只会被访问一次，展开邻居的代价是常数。相比暴力的 `4^d`，这是一条 **线性**（对状态空间大小） 的时间。  
- **空间复杂度**：`O(N)`，主要是 `visited` 集合和队列保存的状态，同样最多 720 条记录，属于常数级别（相对于输入规模极小）。

---

## 心得

- **核心技巧**：把“每一步的棋盘”抽象成 **图的节点**，用 **BFS** 在无权图中求最短路径。  
- **该技巧适用的题型**  
  1. 8‑Puzzle / 15‑Puzzle（更大的滑动拼图）  
  2. “打开锁” (`Open the Lock`)——每一次转动相当于图的边  
  3. “迷宫最短路径” 或 “单词接龙”——同样是把状态转移建成图，再 BFS  

- **一句话总结解题钥匙**：**把状态压缩成唯一的哈希值，用 BFS 按层搜索，第一次遇到目标就是最少步数**。

---

## 反思

- **第一反应**：看到“每次只能交换 0 与相邻数字”，立刻想到把每一种棋盘当成节点，用搜索遍历所有可能的布局。  
- **最容易踩的坑**  
  1. **状态去重不彻底**：如果只记录已经访问的二维列表，会因为列表不可哈希导致重复搜索，甚至出现无限循环。  
  2. **忘记更新空格位置**：交换后 `0` 的下标会改变，后续的邻接计算必须使用新的下标。  
  3. **边界条件**：输入已经是目标状态时要直接返回 0，防止 BFS 多跑一层。  
- **下次遇到同类题**：第一步先 **设计状态的唯一编码**（字符串 / 整数），再决定 **使用 BFS（最短路径）还是 DFS（遍历全部）**。如果题目要求最少步数，立刻想到 BFS。