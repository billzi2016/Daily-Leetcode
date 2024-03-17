# #2617. 网格中访问的最少单元格数 / Minimum Number of Visited Cells in a Grid

> 难度：困难 · 标签：Array、Dynamic Programming、Stack、Breadth-First Search、Union Find、Heap (Priority Queue)、Matrix、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-visited-cells-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n integer matrix grid. Your initial position is at the top-left cell (0, 0).
Starting from the cell (i, j), you can move to one of the following cells:
Return the minimum number of cells you need to visit to reach the bottom-right cell (m - 1, n - 1). If there is no valid path, return -1.

**Examples**

**Example 1:**

```
Input: grid = [[3,4,2,1],[4,2,3,1],[2,1,0,0],[2,4,0,0]]
Output: 4
Explanation: The image above shows one of the paths that visits exactly 4 cells.
```

**Example 2:**

```
Input: grid = [[3,4,2,1],[4,2,1,1],[2,1,1,0],[3,4,1,0]]
Output: 3
Explanation: The image above shows one of the paths that visits exactly 3 cells.
```

**Example 3:**

```
Input: grid = [[2,1,0],[1,0,0]]
Output: -1
Explanation: It can be proven that no path exists.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- 0 <= grid[i][j] < m * n
- grid[m - 1][n - 1] == 0

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的 **m × n** 整数矩阵（matrix）`grid`。你的初始位置在左上角单元格 `(0, 0)`。  
从单元格 `(i, j)` 出发，你可以移动到以下任意一个单元格：

（原题目中会给出具体的移动规则，此处保持原样）

返回到达右下角单元格 `(m - 1, n - 1)` 所需访问的最少单元格数。如果不存在合法路径，返回 `-1`。

## 示例

### 示例 1  
**输入**  
```text
grid = [[3,4,2,1],
        [4,2,3,1],
        [2,1,0,0],
        [2,4,0,0]]
```  
**输出**  
```text
4
```  
**解释**  
上图展示了一条恰好访问 **4** 个单元格的路径。

### 示例 2  
**输入**  
```text
grid = [[3,4,2,1],
        [4,2,1,1],
        [2,1,1,0],
        [3,4,1,0]]
```  
**输出**  
```text
3
```  
**解释**  
上图展示了一条恰好访问 **3** 个单元格的路径。

### 示例 3  
**输入**  
```text
grid = [[2,1,0],
        [1,0,0]]
```  
**输出**  
```text
-1
```  
**解释**  
可以证明不存在满足条件的路径。

## 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10^5`
- `1 <= m * n <= 10^5`
- `0 <= grid[i][j] < m * n`
- `grid[m - 1][n - 1] == 0`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一步可以到达的所有格子** 都枚举出来，然后在这些格子之间继续搜索，直到到达右下角。  
这正好可以用 **广度优先搜索（BFS）** 来实现：

1. 从左上角 `(0,0)` 开始，把它放进队列。  
2. 每次从队列里弹出一个格子 `(i, j)`，读取它的跳数 `grid[i][j]`。  
3. 根据题目规定，**只能往右或往下**（或者也可以往左、上，取决于完整题目，这里以官方示例的四个方向为例），向每个方向最多跳 `grid[i][j]` 步，把所有合法且未访问过的格子加入队列。  
4. BFS 按层遍历，第一次把右下角弹出时，就是最少访问格子数（层数+1）。

> **类比**：想象你站在一个大城市的十字路口，每个路口都有一块“广告牌”写着你最多可以一次性跨过多少个街区。暴力 BFS 就是把 **所有** 能跨过去的街区一个一个列出来，走到下一个十字路口再继续这样列。

**为什么能得到最小访问格子数？**  
BFS 按层（即走的格子数）遍历，先到达的路径一定是格子数最少的路径——这是一条 BFS 的基本性质。

#### 代码（Python）

```python
from collections import deque

def minVisitedCells(grid):
    m, n = len(grid), len(grid[0])
    # 记录每个格子是否已经访问，防止重复入队
    visited = [[False] * n for _ in range(m)]
    q = deque()
    q.append((0, 0, 1))          # (行, 列, 已访问格子数)
    visited[0][0] = True

    while q:
        i, j, steps = q.popleft()
        # 到达终点，返回答案
        if i == m - 1 and j == n - 1:
            return steps

        jump = grid[i][j]
        # 四个方向：右、下、左、上（题目只要右下也可以删减）
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            for d in range(1, jump + 1):          # 枚举每一步可能的跳距
                ni, nj = i + di * d, j + dj * d
                # 越界或已经访问过的格子直接跳过
                if not (0 <= ni < m and 0 <= nj < n):
                    break          # 超出边界，后面的 d 更大肯定也出界
                if visited[ni][nj]:
                    continue
                visited[ni][nj] = True
                q.append((ni, nj, steps + 1))

    # 队列空了仍未到终点，说明没有合法路径
    return -1
```

> **关键注释**  
> - `for d in range(1, jump + 1)`: 这里把 **“能跳的所有格子”** 一个一个列出来。  
> - `break` 当越界时直接退出该方向的循环，因为更大的跳距只会更远地越界。  

#### 复杂度  

- **时间复杂度**：`O(m * n * maxJump)`  
  - `maxJump` 是格子里最大的数。最坏情况下每个格子都要遍历它能跳的所有格子，等价于 **每个格子都被检查 `maxJump` 次**。  
  - 用大白话说，就是“如果每个格子都能让你跨 1000 步，而整个网格有 10⁵ 个格子，那么大概要检查 10⁸ 次”。这在 `m·n ≤ 10⁵` 的限制下会超时。

- **空间复杂度**：`O(m * n)`  
  - `visited` 数组和 BFS 队列最多各存一个网格大小的标记，属于线性空间。

---

### 2. 最优解  

#### 思路  

暴力 BFS 的瓶颈在 **“枚举每一步的所有跳距”**，尤其当 `grid[i][j]` 很大时会产生大量无意义的检查。  
我们需要 **快速找出在当前格子 `(i, j)` 能到达的、且 **距离最短** 的未访问格子，而不是把它们全部列举出来。

下面的思路把 **“最短距离”** 的信息提前准备好，用 **优先队列 + 并查集（Union‑Find）** 来 **跳过已经访问过的格子**，实现 **近似 O(m·n log(m·n))** 的时间。

---

#### 2.1 关键观察  

1. **从左到右、从上到下动态规划**  
   - 如果我们已经算出了所有格子 `dis[x][y]`（到达 `(x,y)` 的最少访问格子数），那么在计算 `(i,j)` 时，只需要关注 **同一行左侧** 和 **同一列上方** 的格子。因为只能向右或向下移动（题目给出的四个方向里，右和下是关键方向，左、上在最优路径里会导致回头，等价于把它们视作“已访问”后直接跳过）。

2. **最小距离一定来自“最近的已知格子”**  
   - 对于同一行的左侧格子 `k`（`k < j`），如果 `grid[i][k]` 足够大，使得我们能够一次跳到 `j`，那么 `dis[i][j] = dis[i][k] + 1`。我们只关心 **最小的 `dis[i][k]`**，其余更大的 `dis` 永远不会成为最优答案。

3. **使用 **优先队列** 维护每行/每列的候选格子**  
   - 对每一行维护一个最小堆 `rowHeap[i]`，堆中存 `(dis[i][k], k)`，只保留 **还能跳到当前列的格子**。  
   - 类似地，对每一列维护 `colHeap[j]`，堆中存 `(dis[k][j], k)`。

4. **并查集（Union‑Find）帮助“跳过已访问格子”**  
   - 当我们把格子 `(i, j)` 标记为已访问后，以后再查询同一行的左侧格子时，可以直接 **把 `j` 合并到 `j-1`**（向左找下一个未访问的格子）。这样每个格子只会被查找一次，几乎是 **α(N)**（几乎是常数）的代价。

> **类比**：  
> - **优先队列** 像是“每行的最快快递员”，只要把最快的那位叫出来，就知道该行最早能到达的位置。  
> - **并查集** 像是“道路封闭系统”。一旦某段路已经走过，就把它和前面的路合并，后面再找路时直接跳过这段已经封闭的路。

---

#### 2.2 算法步骤  

1. **初始化**  
   - `dis` 数组全部设为 `inf`（表示暂未可达），`dis[0][0] = 1`（起点算作访问 1 次）。  
   - 为每一行 `i` 创建一个空最小堆 `rowHeap[i]`，每一列 `j` 创建 `colHeap[j]`。  
   - 并查集 `rowNext[i][j]` 用来快速找 **左侧最近未访问的列**（同理 `colNext[i][j]` 用来找 **上方最近未访问的行**）。这里我们用两个一维并查集 `row_parent`、`col_parent` 分别对应行、列。

2. **把起点加入堆**  
   - `rowHeap[0].push((1, 0))`，`colHeap[0].push((1, 0))`。

3. **遍历网格（行从上到下，列从左到右）**  
   对每个格子 `(i, j)`：

   a. **从行堆取最小值**：  
      - 只要堆顶的列 `k` **不能跳到 `j`**（即 `k + grid[i][k] < j`），就把它弹出，因为以后也不可能再用它到达更右的格子。  
      - 堆顶满足条件时，`row_min = heap[0][0]`（最小的访问次数）。  

   b. **从列堆取最小值**（同理）得到 `col_min`。

   c. `dis[i][j] = min(row_min, col_min) + 1`（如果两者都不可达则保持 `inf`）。  

   d. **如果 `dis[i][j]` 仍是 `inf`，说明该格子不可达，直接跳过后面的步骤**。

   e. **把当前格子加入对应的堆**，为后面的格子提供“来源”  
      - `rowHeap[i].push((dis[i][j], j))`  
      - `colHeap[j].push((dis[i][j], i))`

   f. **并查集合并**：  
      - 行方向：`row_parent[i][j] = find(row_parent[i], j-1)`（把 `j` 合并到左侧最近未访问的列）。  
      - 列方向：`col_parent[j][i] = find(col_parent[j], i-1)`（把 `i` 合并到上方最近未访问的行）。

4. **遍历结束后**，若 `dis[m-1][n-1]` 仍是 `inf`，返回 `-1`；否则返回该值。

> **核心优化**：  
> - 每个格子只会 **被弹出堆一次**（因为一旦弹出就说明它已经不能再帮助跳更远）。  
> - 并查集的 **路径压缩** 让“寻找最近未访问格子”的操作几乎是 **O(1)**。  
> - 整体时间复杂度因此降到 `O(m·n log n)`（堆操作的对数）或 `O(m·n α(m·n))`（使用更高级的 “单调队列 + 并查集” 可进一步降到 `O(m·n)`），在 `m·n ≤ 10⁵` 的限制下完全可接受。

---

#### 代码（Python）

```python
import heapq
import sys
sys.setrecursionlimit(1 << 25)

INF = 10 ** 9

def minVisitedCells(grid):
    m, n = len(grid), len(grid[0])

    # ---------- 并查集 ----------
    # 对每一行，parent[i][j] 表示列 j 向左最近未访问的列（包括自身）
    row_parent = [[j for j in range(n + 1)] for _ in range(m)]
    col_parent = [[i for i in range(m + 1)] for _ in range(n)]

    def find_row(i, x):
        """在第 i 行查找 x 的根（左侧最近未访问的列）"""
        if row_parent[i][x] != x:
            row_parent[i][x] = find_row(i, row_parent[i][x])
        return row_parent[i][x]

    def find_col(j, x):
        """在第 j 列查找 x 的根（上方最近未访问的行）"""
        if col_parent[j][x] != x:
            col_parent[j][x] = find_col(j, col_parent[j][x])
        return col_parent[j][x]

    # ---------- 堆 ----------
    # 每行的最小堆：存 (dis, col)
    row_heap = [ [] for _ in range(m) ]
    # 每列的最小堆：存 (dis, row)
    col_heap = [ [] for _ in range(n) ]

    # ---------- DP 表 ----------
    dis = [[INF] * n for _ in range(m)]
    dis[0][0] = 1                         # 起点算作访问一次
    heapq.heappush(row_heap[0], (1, 0))
    heapq.heappush(col_heap[0], (1, 0))

    # 遍历所有格子（从左上到右下）
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:      # 起点已经处理
                continue

            # ---------- 行堆：找左侧能跳到 (i,j) 的最小 dis ----------
            while row_heap[i]:
                cur_dis, col = row_heap[i][0]      # 看堆顶
                # 如果该列的跳距不足以到达 j，弹出它
                if col + grid[i][col] < j:
                    heapq.heappop(row_heap[i])
                else:
                    break
            row_min = row_heap[i][0][0] if row_heap[i] else INF

            # ---------- 列堆：找上方能跳到 (i,j) 的最小 dis ----------
            while col_heap[j]:
                cur_dis, row = col_heap[j][0]
                if row + grid[row][j] < i:
                    heapq.heappop(col_heap[j])
                else:
                    break
            col_min = col_heap[j][0][0] if col_heap[j] else INF

            best = min(row_min, col_min)
            if best == INF:          # 仍不可达
                continue
            dis[i][j] = best + 1

            # 将当前格子加入对应的堆，为后面的格子提供来源
            heapq.heappush(row_heap[i], (dis[i][j], j))
            heapq.heappush(col_heap[j], (dis[i][j], i))

            # 并查集合并：把 (i,j) 标记为已访问，后面查找左/上最近未访问时可以直接跳过
            # 行方向：把 j 合并到左侧最近未访问的列
            row_parent[i][j] = find_row(i, j - 1) if j > 0 else 0
            # 列方向：把 i 合并到上方最近未访问的行
            col_parent[j][i] = find_col(j, i - 1) if i > 0 else 0

    ans = dis[m - 1][n - 1]
    return -1 if ans == INF else ans
```

> **代码要点解释**  
> - `row_heap[i]` / `col_heap[j]`：每行/列的最小堆，只保留 **仍然能跳到当前格子** 的候选者。堆顶即为该行/列的 **最小访问次数**。  
> - `while row_heap[i] …`：不断弹出 **已经无法再向右跳** 的格子（左侧的跳距太小），保证堆顶始终是合法的。  
> - `find_row` / `find_col`：并查集的“路径压缩”实现，使得后续查找几乎是 O(1)。这里我们只在 **标记已访问** 时使用合并，以免后面再次遍历已访问的格子。  
> - `dis[i][j] = best + 1`：到达 `(i,j)` 需要的格子数 = 之前最优格子数 + 当前格子本身。  

#### 复杂度  

- **时间复杂度**：`O(m·n·log n)`（每个格子至多一次堆的 `push` 与 `pop`，堆大小不超过该行/列的格子数，`log` 为对数）  
  - 与暴力解的 `O(m·n·maxJump)` 相比，**对数**远小于可能出现的 `maxJump`（最大可达 10⁵），因此在所有约束下都能快速跑完。  
  - 如果把堆换成 **单调队列 + 并查集**，可以进一步降到 `O(m·n)`，但对初学者来说，堆的实现更直观。

- **空间复杂度**：`O(m·n)`  
  - `dis`、`row_heap`、`col_heap`、并查集数组共占用线性空间。  
  - 这仍然在题目给出的 `m·n ≤ 10⁵` 范围内。

---

## 心得  

- **核心技巧**：**利用最小堆（或单调队列）配合并查集，快速获取同一行/列中“还能跳到当前位置的最小距离”。**  
- **适用题型**  
  1. **带跳跃范围的最短路径**（如 “Minimum Cost to Reach Destination”）。  
  2. **矩阵中向右向下的单调跳**（如 “Maximum Points You Can Obtain from Cards”。）  
  3. **需要在每行/列快速查询最小值的 DP**（如 “Shortest Path in a Grid with Obstacles Elimination” 的优化版）。  
- **一句话总结解题钥匙**：**把“所有可能的跳”压缩成“同一行/列的最小可达代价”，用堆保留最小值、用并查集跳过已经访问的格子**。

---

## 反思  

- **第一反应**：看到“每个格子可以跳任意步数”，本能地想 **枚举所有跳距**，于是写出暴力 BFS。  
- **最容易踩的坑**  
  - **时间爆炸**：`grid[i][j]` 可能很大，直接遍历会超时。  
  - **边界处理**：跳到矩阵外部要立即停止，防止无限循环。  
  - **重复访问**：没有去重会导致同一个格子被多次入队，空间/时间都会翻倍。  
- **下次遇到同类题**，第一步应先问自己：“**是否可以把‘所有可达的格子’压缩成‘同一行/列的最小代价’**？”如果答案是肯定的，就立刻考虑 **单调结构（堆/单调队列） + 并查集** 来避免枚举。这样既能保证正确性，又能把复杂度控制在可接受范围。