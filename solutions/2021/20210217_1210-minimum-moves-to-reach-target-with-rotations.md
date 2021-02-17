# #1210. 最少移动次数到达目标（含旋转） / Minimum Moves to Reach Target with Rotations

> 难度：困难 · 标签：Array、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-reach-target-with-rotations/)

---

## 题目（英文原版）

**Description**

In an n*n grid, there is a snake that spans 2 cells and starts moving from the top left corner at (0, 0) and (0, 1). The grid has empty cells represented by zeros and blocked cells represented by ones. The snake wants to reach the lower right corner at (n-1, n-2) and (n-1, n-1).
In one move the snake can:
Return the minimum number of moves to reach the target.
If there is no way to reach the target, return -1.

**Examples**

**Example 1:**

```
Input: grid = [[0,0,0,0,0,1],
               [1,1,0,0,1,0],
               [0,0,0,0,1,1],
               [0,0,1,0,1,0],
               [0,1,1,0,0,0],
               [0,1,1,0,0,0]]
Output: 11
Explanation:
One possible solution is [right, right, rotate clockwise, right, down, down, down, down, rotate counterclockwise, right, down].
```

**Example 2:**

```
Input: grid = [[0,0,1,1,1,1],
               [0,0,0,0,1,1],
               [1,1,0,0,0,1],
               [1,1,1,0,0,1],
               [1,1,1,0,0,1],
               [1,1,1,0,0,0]]
Output: 9
```

**Constraints**

- 2 <= n <= 100
- 0 <= grid[i][j] <= 1
- It is guaranteed that the snake starts at empty cells.

---

## 题目（中文翻译）

在一个 **n × n** 的网格中，有一条占据 2 个格子的蛇，初始位置位于左上角的 `(0, 0)` 与 `(0, 1)`。网格中的空格用 `0` 表示，障碍格用 `1` 表示。蛇的目标是到达右下角的 `(n‑1, n‑2)` 与 `(n‑1, n‑1)`。

在一次移动中，蛇可以：

- 向左、向右或向下平移一格（前提是目标格子均为空）。
- 顺时针或逆时针旋转（将蛇从水平姿态变为垂直姿态，或反之），旋转时需要确保旋转后占据的两个格子均为空。

**返回** 达到目标所需的最少移动次数。如果无法到达目标，返回 `-1`。

### 示例

#### 示例 1
```text
Input: grid = [[0,0,0,0,0,1],
               [1,1,0,0,1,0],
               [0,0,0,0,1,1],
               [0,0,1,0,1,0],
               [0,1,1,0,0,0],
               [0,1,1,0,0,0]]
Output: 11
Explanation:
一种可能的路径是 [右, 右, 顺时针旋转, 右, 下, 下, 下, 下, 逆时针旋转, 右, 下]。
```

#### 示例 2
```text
Input: grid = [[0,0,1,1,1,1],
               [0,0,0,0,1,1],
               [1,1,0,0,0,1],
               [1,1,1,0,0,1],
               [1,1,1,0,0,1],
               [1,1,1,0,0,0]]
Output: 9
```

### 约束条件
- `2 <= n <= 100`
- `0 <= grid[i][j] <= 1`
- 保证蛇的起始格子为空 (`0`)。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举一遍**，从起点 `(0,0)-(0,1)` 开始，一步步尝试四种合法操作（向右、向下、顺时针旋转、逆时针旋转），一直走到目标位置 `(n‑1,n‑2)-(n‑1,n‑1)` 为止。  

- **数据结构**：我们可以用一个 **列表** 保存蛇的当前两个格子坐标，例如 `[(x1,y1),(x2,y2)]`。  
- **生活化类比**：把蛇想象成一根可以伸缩的棍子，棍子两头分别占两个格子。每次移动就像在格子里“滑动”或“转向”。  
- **正确性**：只要遍历了**所有**合法的走法，就一定会找到一条最短路径（如果存在的话），因为最短路径必然是某条遍历到的路径。  

但这种做法的**瓶颈**在于：每一步都有最多 4 种选择，深度可能达到 `O(n^2)`（因为最多要走 `2n-2` 步），所以总的尝试次数是 `4^{2n}`，随网格大小指数级增长，根本不可接受。

#### 代码（Python）

```python
from copy import deepcopy

# ------------------------------------------------------------
# 只用于演示暴力思路，实际运行会在 n>4 时超时或内存爆炸
# ------------------------------------------------------------
def min_moves_bruteforce(grid):
    n = len(grid)
    target = ((n-1, n-2), (n-1, n-1))   # 目标位置（水平）

    # 判断两个格子是否都在范围内且为空
    def ok(cell):
        x, y = cell
        return 0 <= x < n and 0 <= y < n and grid[x][y] == 0

    # 所有合法的下一步
    def next_states(state):
        (x1, y1), (x2, y2) = state
        res = []

        # 1. 向右移动（水平时两格都向右，垂直时右上格、右下格一起右移）
        if y2 + 1 < n and ok((x1, y1+1)) and ok((x2, y2+1)):
            res.append(((x1, y1+1), (x2, y2+1)))

        # 2. 向下移动（垂直时两格都向下，水平时左下格、右下格一起下移）
        if x2 + 1 < n and ok((x1+1, y1)) and ok((x2+1, y2)):
            res.append(((x1+1, y1), (x2+1, y2)))

        # 3. 顺时针旋转：水平 → 垂直（左端点为旋转轴）
        if y1 + 1 < n and x1 + 1 < n and ok((x1+1, y1)) and ok((x1+1, y1+1)):
            res.append(((x1, y1), (x1+1, y1)))   # 成垂直

        # 4. 逆时针旋转：垂直 → 水平（上端点为旋转轴）
        if x1 + 1 < n and y1 + 1 < n and ok((x1, y1+1)) and ok((x1+1, y1+1)):
            res.append(((x1, y1), (x1, y1+1)))   # 成水平

        return res

    ans = float('inf')
    visited = set()

    def dfs(state, steps):
        nonlocal ans
        if steps >= ans:                     # 已经不可能更优，剪枝
            return
        if state == target:                  # 到达目标
            ans = min(ans, steps)
            return
        if state in visited:                 # 防止死循环
            return
        visited.add(state)
        for nxt in next_states(state):
            dfs(nxt, steps+1)
        visited.remove(state)

    dfs(((0,0),(0,1)), 0)
    return -1 if ans == float('inf') else ans
```

> **关键行中文注释**  
> - `ok(cell)`: 判断格子是否在棋盘内部且没有障碍。  
> - `next_states(state)`: 根据当前姿态列举四种合法的下一步。  
> - `dfs`: 深度优先搜索，尝试所有走法并记录最小步数。

#### 复杂度

- **时间复杂度**：`O(4^{2n})`（指数级），因为每一步最多有 4 种选择，最坏情况下要走 `2n` 步。  
  - **大白话**：如果网格是 10×10，可能要尝试几千亿次，根本跑不完。  
- **空间复杂度**：`O(2n)`，递归栈的深度最多是走到终点需要的步数（约 `2n`），以及存放当前状态的集合。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**状态空间**并不是无限的：  
- 蛇只占 **两个相邻的格子**。  
- 这两个格子要么在同一行（水平），要么在同一列（垂直）。  

因此我们可以把**“蛇的姿态 + 位置”**看成一个**离散的状态**，并用 **宽度优先搜索（BFS）** 在状态图中寻找最短路径。BFS 的特点是**先遍历离起点最近的所有状态**，所以第一个到达目标的状态必然是最少步数。

**状态表示**  
- 用 `(x, y, ori)` 表示蛇左上端点坐标 `(x, y)`，以及它的方向 `ori`（0 表示水平，1 表示垂直）。  
  - 当 `ori == 0`（水平）时，蛇占 `(x, y)` 与 `(x, y+1)`。  
  - 当 `ori == 1`（垂直）时，蛇占 `(x, y)` 与 `(x+1, y)`。  

**合法转移**（每个状态最多四条边）  

| 当前方向 | 操作 | 需要的空格 | 产生的新状态 |
|---|---|---|---|
| 水平 | 向右 | `(x, y+2)` 必须为空 | `(x, y+1, 0)` |
| 垂直 | 向下 | `(x+2, y)` 必须为空 | `(x+1, y, 1)` |
| 水平 → 垂直（顺时针） | 以左端点为轴旋转 | `(x+1, y)` 与 `(x+1, y+1)` 必须为空 | `(x, y, 1)` |
| 垂直 → 水平（逆时针） | 以上端点为轴旋转 | `(x, y+1)` 与 `(x+1, y+1)` 必须为空 | `(x, y, 0)` |
| 水平 | 向下 | `(x+1, y)` 与 `(x+1, y+1)` 必须为空 | `(x+1, y, 0)` |
| 垂直 | 向右 | `(x, y+1)` 与 `(x+1, y+1)` 必须为空 | `(x, y+1, 1)` |

**BFS 步骤**  

1. **初始化**：队列 `queue` 放入起始状态 `(0,0,0)`，步数 `0`。  
2. **循环**：每次弹出队首状态，检查是否已到达目标 `(n‑1, n‑2, 0)`。  
3. **产生子状态**：按照上表尝试四种移动/旋转，只要对应格子在棋盘内且为 `0`，且该状态未被访问过，就加入队列。  
4. **层级计数**：使用 `for _ in range(len(queue))` 逐层遍历，层数即为走的步数。  

因为每个状态只会被访问一次，且状态总数为 `2 * n * n`（每个格子两种方向），所以 BFS 能在 **线性** 时间内结束。

#### 代码（Python）

```python
from collections import deque

def min_moves(grid):
    """
    BFS 求最少移动次数
    :param grid: List[List[int]] 0 表示空格，1 表示障碍
    :return: 最小步数，若不可达返回 -1
    """
    n = len(grid)
    # 目标状态：蛇水平，左端点在 (n-1, n-2)
    target = (n - 1, n - 2, 0)

    # 判断坐标是否在棋盘且为空
    def empty(x, y):
        return 0 <= x < n and 0 <= y < n and grid[x][y] == 0

    # BFS 队列：每个元素是 (x, y, ori)
    q = deque()
    q.append((0, 0, 0))          # 起点：水平，左端点在左上角
    visited = set()
    visited.add((0, 0, 0))

    steps = 0                    # 已走的步数（层数）

    while q:
        for _ in range(len(q)):  # 同层的状态一起处理
            x, y, ori = q.popleft()
            if (x, y, ori) == target:
                return steps

            # ---------- 向右 ----------
            if ori == 0:  # 水平状态向右需要 (x, y+2) 为空
                if y + 2 < n and empty(x, y + 2):
                    nxt = (x, y + 1, 0)
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)
            else:         # 垂直状态向右需要 (x, y+1) 与 (x+1, y+1) 为空
                if y + 1 < n and empty(x, y + 1) and empty(x + 1, y + 1):
                    nxt = (x, y + 1, 1)
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)

            # ---------- 向下 ----------
            if ori == 1:  # 垂直状态向下需要 (x+2, y) 为空
                if x + 2 < n and empty(x + 2, y):
                    nxt = (x + 1, y, 1)
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)
            else:         # 水平状态向下需要 (x+1, y) 与 (x+1, y+1) 为空
                if x + 1 < n and empty(x + 1, y) and empty(x + 1, y + 1):
                    nxt = (x + 1, y, 0)
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)

            # ---------- 顺时针旋转：水平 → 垂直 ----------
            if ori == 0:
                # 以左端点 (x, y) 为轴，需要 (x+1, y) 与 (x+1, y+1) 为空
                if x + 1 < n and empty(x + 1, y) and empty(x + 1, y + 1):
                    nxt = (x, y, 1)
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)

            # ---------- 逆时针旋转：垂直 → 水平 ----------
            else:
                # 以上端点 (x, y) 为轴，需要 (x, y+1) 与 (x+1, y+1) 为空
                if y + 1 < n and empty(x, y + 1) and empty(x + 1, y + 1):
                    nxt = (x, y, 0)
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)

        steps += 1   # 处理完一层，步数加一

    # BFS 结束仍未到达目标，说明不可达
    return -1
```

> **代码要点中文注释**  
> - `empty(x, y)`: 判断一个格子是否在范围内且没有障碍。  
> - `visited` 集合防止同一个状态被重复加入队列，避免无限循环。  
> - `for _ in range(len(q))` 实现**层序遍历**，保证 `steps` 正好等于走的步数。  
> - 每一种移动/旋转都对应上表的“需要的空格”，只有满足条件才会产生新状态。

#### 复杂度

- **时间复杂度**：`O(n²)`。  
  - 解释：棋盘上最多有 `n·n` 个左端点，每个端点只有两种方向（水平/垂直），所以状态总数不超过 `2·n²`。BFS 每个状态只会被处理一次，且每次只检查常数条边（最多 4 条），因此总体时间与状态数线性相关。  
  - 与暴力解相比，从指数级降到了多项式级，速度快了天差地别。  

- **空间复杂度**：`O(n²)`。  
  - 解释：`visited` 集合和 BFS 队列最坏情况下会同时保存所有状态，同样是 `2·n²` 个条目，属于线性空间。

---

## 心得

- **核心技巧**：把“蛇的当前位置 + 方向”抽象成离散的 **状态**，使用 **宽度优先搜索（BFS）** 在状态图中寻找最短路径。  
- **适用的题型**  
  1. **滑动拼图**（如 15 Puzzle）——状态是拼图的排列。  
  2. **机器人运动**（如 `Robot Room Cleaner`）——状态是机器人的坐标和朝向。  
  3. **棋子翻转**（如 `Open the Lock`）——状态是转盘的数字组合。  
- **一句话总结解题钥匙**：**把“位置 + 方向”看成一个整体状态，用 BFS 按层展开，最先到达的即为最短步数。**

---

## 反思

- **第一反应**：看到“最少移动次数”，自然想到 **最短路径**，于是想到 BFS。  
- **最容易踩的坑**  
  1. **状态定义不完整**：仅记两个格子坐标会导致同一姿态出现多次，浪费时间。必须统一用左上端点 + 方向来唯一表示。  
  2. **旋转条件漏检**：旋转时不仅要保证旋转后的两个格子空，还要保证**旋转中心所在的 2×2 小块**全部为空，否则会穿墙。  
  3. **边界判断**：向右、向下、旋转时要先判断新格子是否越界，否则会访问非法索引导致错误。  
- **下次遇到同类题**：第一步先**抽象状态**（位置 + 额外信息），再判断**状态转移的合法性**，最后用 **BFS** 寻找最短路径。这样可以把很多看似复杂的移动问题统一到图搜索框架中去解决。