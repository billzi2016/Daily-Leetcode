# #994. 腐烂的橙子 / Rotting Oranges

> 难度：中等 · 标签：Array、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/rotting-oranges/)

---

## 题目（英文原版）

**Description**

You are given an m x n grid where each cell can have one of three values:
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

**Examples**

**Example 1:**

```
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
```

**Example 2:**

```
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.
```

**Example 3:**

```
Input: grid = [[0,2]]
Output: 0
Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2.

---

## 题目（中文翻译）

给定一个 **m × n 网格（grid）**，其中每个单元格的取值只能是以下三种之一：

- `0` 表示空单元格
- `1` 表示新鲜橙子（fresh orange）
- `2` 表示腐烂橙子（rotten orange）

每过 **一分钟（minute）**，所有与腐烂橙子 **4 向相邻（4-directionally）** 的新鲜橙子都会变成腐烂橙子。

返回使得整个网格中不再存在新鲜橙子所需要的最少分钟数。如果无论如何都无法让所有新鲜橙子腐烂，则返回 `-1`。

---

### 示例

**示例 1**  
Input: `grid = [[2,1,1],[1,1,0],[0,1,1]]`  
Output: `4`

**示例 2**  
Input: `grid = [[2,1,1],[0,1,1],[1,0,1]]`  
Output: `-1`  
Explanation: 左下角的橙子（第 2 行，第 0 列）永远不会腐烂，因为腐烂只能在 **4 向相邻** 的方向上传播。

**示例 3**  
Input: `grid = [[0,2]]`  
Output: `0`  
Explanation: 在第 0 分钟时已经不存在新鲜橙子，答案就是 `0`。

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10`
- `grid[i][j]` 只能是 `0`、`1` 或 `2`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟每一分钟的腐烂过程**，一直循环下去，直到：

1. 没有新鲜橙子被腐烂（说明已经全部腐烂），返回经过的分钟数。  
2. 再循环一次仍然没有任何新鲜橙子被腐烂，但还有新鲜橙子残留（说明这些橙子永远不会被腐烂），返回 `-1`。

**用到的数据结构**  
- **二维列表 `grid`**：就是我们手里的棋盘，直接在上面改值。  
- **一个临时列表 `to_rot`**：记录本分钟里哪些新鲜橙子会被腐烂。可以把它想象成“待处理的任务清单”，类似于我们写待办事项时先列出所有要做的事。

**为什么这个方法一定能得到正确答案**  
因为我们严格按照题目描述的“每分钟、四个方向相邻的橙子一起腐烂”来一步步推进，永远不会漏掉任何可能的腐烂路径。只要循环结束时仍有新鲜橙子，那它们一定不在任何腐烂橙子的四邻域里，题目要求的“不可能”情况就出现了。

**时间/空间复杂度的直观解释**  
- **时间复杂度**：每一分钟我们要遍历整个棋盘 `m × n`（最多 10×10=100），而最坏情况下需要腐烂的分钟数也可能是 `m × n`（每次只腐烂一个橙子）。于是总体是 `O((m·n)²)`，可以想象成“把棋盘的每一个格子都检查了很多次”。  
- **空间复杂度**：我们只用了一个额外的列表 `to_rot` 来存放本轮要腐烂的坐标，最多也不会超过棋盘格子数 `m·n`，所以是 `O(m·n)`。

#### 代码（Python）

```python
from typing import List

def orangesRotting_brute(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    minutes = 0                     # 记录已经过去的分钟数

    while True:
        to_rot = []                  # 本轮要变成腐烂的橙子坐标
        # 1️⃣ 扫描整个棋盘，找出所有 4️⃣方向相邻的 fresh(1) 橙子
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:                 # 当前是腐烂橙子
                    for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                            to_rot.append((ni, nj))

        # 2️⃣ 如果本轮没有任何新鲜橙子可以被腐烂，循环结束
        if not to_rot:
            break

        # 3️⃣ 将本轮记录的橙子全部设为腐烂
        for i, j in to_rot:
            grid[i][j] = 2

        minutes += 1                 # 计时器前进一步

    # 循环结束后检查是否还有新鲜橙子
    for row in grid:
        if 1 in row:                 # 仍然存在 fresh orange
            return -1                # 不可能全部腐烂

    return minutes                  # 所有橙子都腐烂，返回耗时
```

#### 复杂度

- **时间复杂度**：`O((m·n)²)` —— 想象一次遍历棋盘需要 `m·n` 步，最坏情况下要进行 `m·n` 次循环，就像“在同一个房间里来回走了 `m·n` 次”。  
- **空间复杂度**：`O(m·n)` —— 只多用了一个存放待腐烂坐标的列表，最多不超过棋盘格子数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于每分钟都要**完整遍历整个棋盘**来寻找腐烂橙子，这会导致二次方的时间复杂度。其实我们不需要每次都重新扫描，**只要把所有已经腐烂的橙子一次性放进队列**，随后按照“层次遍历”（Breadth‑First Search，BFS）的方式一次性扩散即可。

**关键点：多源 BFS**  

- 把所有初始的腐烂橙子（值为 `2` 的格子）一次性加入队列，这相当于把它们都视作“第 0 层”。  
- 每一次从队列里弹出一个位置，就把它的四个相邻的**新鲜**橙子（值为 `1`）标记为腐烂并加入队列。这样加入队列的橙子自然属于**下一层**，也就是 **+1 分钟** 后会腐烂。  
- 使用**层数计数**来记录已经经过了多少分钟：每当我们把当前层的所有元素全部弹出后，分钟数 `minutes` 加一。

**为什么 BFS 能一次遍历完**  
BFS 正好对应“波纹式传播”。腐烂的橙子每分钟向四周扩散一格，等价于从所有源点同时向外展开的波纹。把所有源点放进同一个队列后，BFS 按层次顺序自然模拟了这种同步扩散，**不需要再重复扫描整个棋盘**。

**核心数据结构解释**  

- **队列 `deque`**：先进先出，保证先处理当前分钟的橙子，再处理下一分钟的橙子。可以把它想象成“排队买咖啡”，先来的先服务，后来的等后面。  
- **方向数组 `dirs = [(1,0),(-1,0),(0,1),(0,-1)]`**：帮助我们一次性得到四个相邻格子的坐标，类似于“东、南、西、北四个方向的指南针”。  

**完整步骤**  

1. 遍历棋盘，把所有腐烂橙子坐标加入队列 `q`，并统计新鲜橙子总数 `fresh_cnt`。  
2. 如果一开始就没有新鲜橙子，直接返回 `0`（题目示例 3）。  
3. BFS 循环：  
   - 记录本轮队列大小 `size`（即当前层的橙子数）。  
   - 依次弹出 `size` 次，每弹出一个腐烂橙子，就检查四个方向的格子。  
   - 若相邻格子是新鲜橙子，标记为腐烂（改为 `2`），`fresh_cnt` 减一，并把该坐标加入队列。  
   - 本轮结束后，若队列不为空，说明还有下一层橙子要在下一分钟腐烂，`minutes += 1`。  
4. BFS 结束后，如果 `fresh_cnt` 为 `0`，说明所有新鲜橙子都被腐烂，返回 `minutes`；否则返回 `-1`（有孤立的橙子永远不会被腐烂）。

#### 代码（Python）

```python
from collections import deque
from typing import List

def orangesRotting(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    q = deque()                     # 队列，存放已经腐烂的橙子坐标
    fresh_cnt = 0                   # 记录还剩多少个新鲜橙子

    # 1️⃣ 初始化：把所有腐烂橙子加入队列，同时统计新鲜橙子数量
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:          # 已经腐烂
                q.append((i, j))
            elif grid[i][j] == 1:        # 新鲜橙子
                fresh_cnt += 1

    # 2️⃣ 特殊情况：根本没有新鲜橙子，直接返回 0
    if fresh_cnt == 0:
        return 0

    minutes = 0                     # 已经过去的分钟数
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]   # 四个方向的偏移量

    # 3️⃣ 多源 BFS
    while q:
        size = len(q)               # 当前层的元素个数，代表本分钟要处理的腐烂橙子
        for _ in range(size):
            i, j = q.popleft()      # 取出一个腐烂橙子的位置
            for di, dj in dirs:     # 检查四个方向
                ni, nj = i + di, j + dj
                # 判断是否在棋盘内部且是新鲜橙子
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2        # 立即把它标记为腐烂
                    fresh_cnt -= 1          # 新鲜橙子数量减一
                    q.append((ni, nj))      # 加入队列，等下一分钟继续扩散

        # 本层全部处理完后，如果队列还有元素，说明还有橙子将在下一分钟腐烂
        if q:
            minutes += 1           # 计时器前进一步

    # 4️⃣ BFS 结束，检查是否还有残留的新鲜橙子
    return minutes if fresh_cnt == 0 else -1
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 每个格子至多被访问一次（入队一次、出队一次），相当于“只走了一遍棋盘”。相比暴力解的 `O((m·n)²)`，快了很多。  
- **空间复杂度**：`O(m·n)` —— 最坏情况下所有格子都是腐烂橙子，全部放进队列，需要 `m·n` 的额外空间。实际使用的空间与格子数呈线性关系。

---

## 心得

- **核心技巧**：**多源广度优先搜索（BFS）**，把所有起点一次性放进队列，层层展开，天然符合“每分钟向四周扩散”这种“波纹”式传播。  
- **适用的题型**  
  1. **01 矩阵** 中的最短距离（从 0 到最近的 1 的距离）  
  2. **岛屿的最大面积** 中的连通块遍历（DFS/BFS）  
  3. **墙壁和门**（`Walls and Gates`）—— 从所有门同时 BFS 填充距离  
- **一句话总结解题钥匙**：**把所有“已经发生的事”一次性放进队列，用层次遍历模拟同步扩散**。

---

## 反思

- **第一反应**：看到“每分钟、相邻”就想到**模拟**，于是写了逐分钟遍历的暴力代码。  
- **最容易踩的坑**  
  1. **计时器的递增位置**：必须在当前层全部处理完后才 `minutes += 1`，否则会多算一次。  
  2. **边界条件**：如果一开始就没有新鲜橙子，需要立即返回 `0`（示例 3）。  
  3. **孤立橙子**：有的橙子被 0（空格子）完全隔离，需要在 BFS 结束后检查 `fresh_cnt` 是否为 0。  
- **下次类似题的第一步**：**先定位所有起始点并放进队列**，判断是否可以直接返回（如没有待处理的目标），然后再进行 BFS/DFS。这样可以避免不必要的全局遍历，直接进入高效的层次扩散。