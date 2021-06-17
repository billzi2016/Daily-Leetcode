# #1368. 网格中至少一条有效路径的最小代价 / Minimum Cost to Make at Least One Valid Path in a Grid

> 难度：困难 · 标签：Array、Breadth-First Search、Graph、Heap (Priority Queue)、Matrix、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/)

---

## 题目（英文原版）

**Description**

Given an m x n grid. Each cell of the grid has a sign pointing to the next cell you should visit if you are currently in this cell. The sign of grid[i][j] can be:
Notice that there could be some signs on the cells of the grid that point outside the grid.
You will initially start at the upper left cell (0, 0). A valid path in the grid is a path that starts from the upper left cell (0, 0) and ends at the bottom-right cell (m - 1, n - 1) following the signs on the grid. The valid path does not have to be the shortest.
You can modify the sign on a cell with cost = 1. You can modify the sign on a cell one time only.
Return the minimum cost to make the grid have at least one valid path.

**Examples**

**Example 1:**

```
Input: grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]
Output: 3
Explanation: You will start at point (0, 0).
The path to (3, 3) is as follows. (0, 0) --> (0, 1) --> (0, 2) --> (0, 3) change the arrow to down with cost = 1 --> (1, 3) --> (1, 2) --> (1, 1) --> (1, 0) change the arrow to down with cost = 1 --> (2, 0) --> (2, 1) --> (2, 2) --> (2, 3) change the arrow to down with cost = 1 --> (3, 3)
The total cost = 3.
```

**Example 2:**

```
Input: grid = [[1,1,3],[3,2,2],[1,1,4]]
Output: 0
Explanation: You can follow the path from (0, 0) to (2, 2).
```

**Example 3:**

```
Input: grid = [[1,2],[4,3]]
Output: 1
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- 1 <= grid[i][j] <= 4

---

## 题目（中文翻译）

给定一个 **m × n** 的网格 `grid`。网格中的每个单元格都有一个指向下一步应访问单元格的标记（sign），如果你当前位于该单元格，则按照标记前进。`grid[i][j]` 的标记可以是以下四种之一：

- `1` → 向右（right）
- `2` → 向左（left）
- `3` → 向下（down）
- `4` → 向上（up）

> 注意，网格中可能存在指向网格外部的标记。

你最初位于左上角单元格 `(0, 0)`。**有效路径** 是一条从左上角 `(0, 0)` 开始、按照网格标记移动并最终到达右下角 `(m‑1, n‑1)` 的路径。该路径不要求是最短的。

你可以修改任意单元格的标记，修改一次的代价为 `1`，且每个单元格只能修改一次。

**返回** 为使网格至少存在一条有效路径所需的最小代价。

---

### 示例

**示例 1**

```text
Input: grid = [[1,1,1,1],
               [2,2,2,2],
               [1,1,1,1],
               [2,2,2,2]]
Output: 3
Explanation:
从 `(0, 0)` 开始，路径如下：
(0, 0) → (0, 1) → (0, 2) → (0, 3)  
将 `(0, 3)` 的标记改为向下，代价 = 1 → (1, 3) → (1, 2) → (1, 1) → (1, 0)  
将 `(1, 0)` 的标记改为向下，代价 = 1 → (2, 0) → (2, 1) → (2, 2) → (2, 3)  
将 `(2, 3)` 的标记改为向下，代价 = 1 → (3, 3)
总代价为 3。
```

**示例 2**

```text
Input: grid = [[1,1,3],
               [3,2,2],
               [1,1,4]]
Output: 0
Explanation:
直接按照标记即可从 `(0, 0)` 到达 `(2, 2)`，无需修改。
```

**示例 3**

```text
Input: grid = [[1,2],
               [4,3]]
Output: 1
Explanation:
只需将任意一个不符合路径的标记修改为正确方向，代价为 1，即可形成有效路径。
```

---

### 约束

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 100`
- `1 ≤ grid[i][j] ≤ 4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举一遍**，记下每条路径需要改动多少次箭头，最后取最小值。  
可以把这个过程想成在一个迷宫里走路：

1. **当前位置** = `(i, j)`。  
2. **两种选择**  
   - **顺着原来的箭头走**，这不需要花钱，费用 `+0`。  
   - **把箭头改成其它方向**（上、下、左、右 四个），这需要付 1 元，费用 `+1`，然后走到选中的相邻格子。  
3. 对新到达的格子继续上述两步，直到走到右下角 `(m‑1, n‑1)`。  
4. 把所有走到终点的路径费用收集，最小的就是答案。

这相当于在每个格子进行**深度优先搜索（DFS）**，把“改动次数”当作路径代价累计。  
因为每个格子都有 4 条可能的出路，搜索树的分支指数级增长——这就是所谓的**暴力**。

> **生活化类比**：把每个格子想成一本字典的页面，页码上画了一个指向下一页的箭头。如果你想翻到指定的页面（终点），最省事的办法是顺着指示走；如果指示不对，你可以花一块钱把箭头改成指向正确的方向，然后继续翻。暴力做法就是把所有可能的改动组合全部试一遍。

**为什么一定能得到正确答案**  
暴力搜索会遍历**所有**合法的走法（包括改动任意次数的情况），因此最小费用一定会被记录下来。

#### 代码（Python）

```python
from typing import List

def minCost_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # 方向对应的坐标增量，顺序与题目中 1:右, 2:左, 3:下, 4:上 相同
    dirs = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    # 四个可能的方向（右、左、下、上）
    all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    best = float('inf')          # 保存全局最小费用
    visited = [[False]*n for _ in range(m)]

    def dfs(i: int, j: int, cost: int):
        nonlocal best
        # 剪枝：已经比当前最小值更大，就不必继续搜索
        if cost >= best:
            return
        # 到达右下角，更新答案
        if i == m-1 and j == n-1:
            best = min(best, cost)
            return
        visited[i][j] = True

        # 1️⃣ 走原来的箭头（费用 0）
        di, dj = dirs[grid[i][j]]
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj]:
            dfs(ni, nj, cost)   # 不加费用

        # 2️⃣ 改成其它方向（费用 1）
        for di, dj in all_dirs:
            if (di, dj) == dirs[grid[i][j]]:   # 已经处理过的方向跳过
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj]:
                dfs(ni, nj, cost + 1)          # 额外付 1 元

        visited[i][j] = False   # 回溯，撤销访问标记

    dfs(0, 0, 0)
    return best
```

> 代码中每一行都加了中文注释，帮助理解。  
> 由于递归会遍历所有可能的改动组合，**在最坏情况下指数级增长**，仅适用于非常小的网格（例如 3×3），用来说明思路即可。

#### 复杂度

- **时间复杂度**：`O(4^{m·n})`（近似指数级）——因为每个格子最多有 4 条分支，搜索树的节点数随格子数量呈指数增长。用大白话说，就是“几乎不可能在合理时间内跑完”，所以这只是概念性的解法。
- **空间复杂度**：`O(m·n)`——递归栈最多占用与网格大小相同的深度，加上 `visited` 数组。

---

### 2. 最优解

#### 思路  

暴力解太慢的根源在于**每次都把所有可能的改动都尝试一次**。实际上，我们只关心**从起点到终点的最小改动次数**，这正是**最短路**问题的本质。  

**关键观察**  

- 每个格子可以看成图中的一个节点。  
- 从 `(i, j)` 出发，它最多只会 **连向四个相邻格子**（上、下、左、右）。  
- 如果相邻格子正好是 **grid[i][j]** 所指的方向，则走这条边不需要改动，**权重 = 0**。  
- 其它三个方向都需要把箭头改成对应方向，**权重 = 1**（改动一次的代价）。  

于是我们得到一个 **带权图**，所有边的权重只有 **0 或 1**。在这种特殊图里，**0‑1 BFS**（使用双端队列）能够在 **O(V+E)** 的时间内求出最短路径。这里 `V = m·n`，`E ≤ 4·m·n`，所以整体是 **线性**。

> **类比**：想象每个格子是一个城市，城市之间有两种道路  
> - 免费道路（权重 0）：正好和指示牌指向的方向一致。  
> - 收费道路（权重 1）：需要先把指示牌改成指向这条路。  
> 我们要找从左上城到右下城的**最省钱的路线**。因为费用只有 0 或 1，使用 **0‑1 BFS** 就像在城镇里先走所有免费道路，只有走不通时才“交钱”走收费道路。

**算法步骤**  

1. **准备**：  
   - `dist[i][j]` 保存到达格子 `(i, j)` 的最小改动次数，初始化为 `inf`，起点为 `0`。  
   - `deque` 用作 0‑1 BFS 的队列。  
2. **弹出**队首 `(i, j)`，遍历四个相邻格子 `(ni, nj)`。  
   - 判断当前方向是否与 `grid[i][j]` 对应。若相同，`w = 0`；否则 `w = 1`。  
   - 若 `dist[i][j] + w < dist[ni][nj]`，说明找到更便宜的到达方式，更新 `dist[ni][nj]`。  
   - 根据 `w` 的取值把 `(ni, nj)` **加入队列**：`w==0` 时放到左边（优先级高），`w==1` 时放到右边。  
3. 循环直到队列空，`dist[m-1][n-1]` 即为答案。

**为什么快**  
- 每个节点最多被放入队列两次（一次以 `0` 权重，一次以 `1` 权重），所以整体是线性时间。  
- 不需要像 Dijkstra 那样维护堆，省掉了 `log` 的开销。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minCost(grid: List[List[int]]) -> int:
    """
    使用 0-1 BFS 求最小改动次数
    """
    m, n = len(grid), len(grid[0])
    # 四个方向对应的增量，顺序与题目定义保持一致
    # 1: 右, 2: 左, 3: 下, 4: 上
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # dist 保存从起点到每个格子的最小费用，初始为无穷大
    INF = 10**9
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0

    dq = deque()
    dq.append((0, 0))               # 起点入队

    while dq:
        i, j = dq.popleft()         # 取出队首
        # 如果已经是终点，可以提前返回（可选优化）
        if i == m - 1 and j == n - 1:
            return dist[i][j]

        for idx, (di, dj) in enumerate(dirs):
            ni, nj = i + di, j + dj
            if not (0 <= ni < m and 0 <= nj < n):
                continue            # 越界直接跳过

            # 判断走这条边是否需要改动箭头
            # grid[i][j] 的取值 1~4 与 idx+1 对应
            w = 0 if grid[i][j] == idx + 1 else 1

            # 若通过当前路径可以得到更小费用，则更新
            if dist[i][j] + w < dist[ni][nj]:
                dist[ni][nj] = dist[i][j] + w
                if w == 0:
                    dq.appendleft((ni, nj))   # 费用为 0，优先处理
                else:
                    dq.append((ni, nj))        # 费用为 1，放到队尾

    # 循环结束后，dist[m-1][n-1] 必然是最小费用
    return dist[m-1][n-1]
```

> 关键行已加中文注释。代码只用了标准库 `collections.deque`，非常易于理解和调试。

#### 复杂度

- **时间复杂度**：`O(m·n)`。每个格子最多被访问两次（一次通过 0 边，一次通过 1 边），所以整体是线性。相比暴力的指数级，这就像从“遍历所有可能的路线”变成了“只走一次最短路”。
- **空间复杂度**：`O(m·n)`。需要存储 `dist` 数组和队列，大小与网格相同。

---

## 心得

- **核心技巧**：把“改动箭头的次数”抽象成 **带权图的最短路**，权重只有 `0` 或 `1`，于是可以使用 **0‑1 BFS**（双端队列）在 O(N) 时间内求解。  
- **适用的题型**  
  1. **网格/棋盘上带有“免费”或“付费”移动** 的最短路（例如 LeetCode 864 “Shortest Path to Get All Keys” 的 0‑1 权重简化版）。  
  2. **需要最小化“改动次数”或“费用次数”** 的问题，如把障碍物变成可通路的最少操作数（LeetCode 2290 “Minimum Obstacle Removal to Reach Corner”）。  
- **一句话总结**：**把改动代价看作 0/1 权重，0‑1 BFS 能在一次遍历中直接给出最小改动次数**。

---

## 反思

- **第一反应**：看到“可以改动箭头，改动一次花 1 元”，立刻想到 **最短路径**，但一开始会把每条路径的改动次数都枚举——这就是暴力思路。  
- **最容易踩的坑**  
  - **越界检查**：有的箭头指向网格外，需要在遍历邻居时先判断坐标合法。  
  - **方向对应关系**：题目中 `1,2,3,4` 分别对应 **右、左、下、上**，如果记错会导致权重判断错误。  
  - **重复访问**：如果不使用 `dist` 数组记录已经得到的最小费用，0‑1 BFS 可能会无限循环。  
- **下次类似题目**：第一步先把 **状态抽象成图的节点**，**边的权重设为是否需要额外操作（0/1）**，随后立刻想到 **0‑1 BFS**（或 Dijkstra）来求最小代价。这样就能避免指数级的搜索，直接得到最优解。