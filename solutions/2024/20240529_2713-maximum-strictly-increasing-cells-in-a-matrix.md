# #2713. 矩阵中严格递增的最大单元格数量 / Maximum Strictly Increasing Cells in a Matrix

> 难度：困难 · 标签：Array、Hash Table、Binary Search、Dynamic Programming、Memoization、Sorting、Matrix、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/maximum-strictly-increasing-cells-in-a-matrix/)

---

## 题目（英文原版）

**Description**

Given a 1-indexed m x n integer matrix mat, you can select any cell in the matrix as your starting cell.
From the starting cell, you can move to any other cell in the same row or column, but only if the value of the destination cell is strictly greater than the value of the current cell. You can repeat this process as many times as possible, moving from cell to cell until you can no longer make any moves.
Your task is to find the maximum number of cells that you can visit in the matrix by starting from some cell.
Return an integer denoting the maximum number of cells that can be visited.

**Examples**

**Example 1:**

```
Input: mat = [[3,1],[3,4]]
Output: 2
Explanation: The image shows how we can visit 2 cells starting from row 1, column 2. It can be shown that we cannot visit more than 2 cells no matter where we start from, so the answer is 2.
```

**Example 2:**

```
Input: mat = [[1,1],[1,1]]
Output: 1
Explanation: Since the cells must be strictly increasing, we can only visit one cell in this example.
```

**Example 3:**

```
Input: mat = [[3,1,6],[-9,5,7]]
Output: 4
Explanation: The image above shows how we can visit 4 cells starting from row 2, column 1. It can be shown that we cannot visit more than 4 cells no matter where we start from, so the answer is 4.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- -105 <= mat[i][j] <= 105

---

## 题目（中文翻译）

给定一个 **1-indexed**（从 1 开始索引）的 `m x n` 整数矩阵 `mat`，你可以选择矩阵中的任意单元格作为起始单元格。  
从起始单元格出发，你可以移动到同一行或同一列的任意其他单元格，但前提是目标单元格的数值**严格大于**当前单元格的数值。你可以无限次重复上述操作，在单元格之间移动，直至无法再进行合法移动为止。  

你的任务是找到一种起始单元格，使得能够访问的单元格数量最大。返回一个整数，表示能够访问的最大单元格数。

---

### 示例

#### 示例 1
```
Input: mat = [[3,1],[3,4]]
Output: 2
Explanation: 如图所示，先从第 1 行第 2 列出发可以访问 2 个单元格。可以证明，无论从哪个单元格开始，都无法访问超过 2 个单元格，因此答案为 2。
```

#### 示例 2
```
Input: mat = [[1,1],[1,1]]
Output: 1
Explanation: 由于单元格的数值必须严格递增，在本例中最多只能访问到一个单元格。
```

#### 示例 3
```
Input: mat = [[3,1,6],[-9,5,7]]
Output: 4
Explanation: 如上图所示，从第 2 行第 1 列出发可以访问 4 个单元格。可以证明，无论从哪个单元格开始，都无法访问超过 4 个单元格，因此答案为 4。
```

---

### 约束条件
- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 10^5`
- `1 <= m * n <= 10^5`
- `-10^5 <= mat[i][j] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从每一个格子出发，深度优先遍历所有能够走的路径**，记录走到的格子数的最大值。  
- **行/列的移动**可以看成在一张城市地图上，只能沿着同一条横向或纵向的道路行驶，且只能向「更高的山」前进。  
- 为了避免走回头路，需要在递归时记住已经访问过的格子（就像走迷宫时要标记已经踩过的脚印）。  

这种做法一定能得到正确答案，因为它穷举了**所有合法的走法**，只要有一条更长的路径，就一定会被遍历到。

> **为什么会超时？**  
> 矩阵的格子数上限是 `10⁵`，而每个格子最多可以向所在行或列的其余格子跳。最坏情况下，搜索树的分支指数级增长，导致运行时间远远超过 1 秒的限制。

#### 代码（Python）

```python
from typing import List

def maxIncreasingCells_bruteforce(mat: List[List[int]]) -> int:
    m, n = len(mat), len(mat[0])
    # 方向：同一行左/右， 同一列上/下
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 记忆化搜索：从 (i, j) 出发，最多能访问多少格子
    memo = {}

    def dfs(i: int, j: int, visited: set) -> int:
        """返回以 (i,j) 为起点的最长严格递增路径长度"""
        if (i, j) in memo:
            # 已经算好答案，直接返回（不考虑 visited，原因见下文）
            return memo[(i, j)]

        best = 1                     # 至少能访问自己
        visited.add((i, j))
        for di, dj in dirs:
            # 沿同一行/列一直往前走，直到遇到更大的数
            x, y = i + di, j + dj
            while 0 <= x < m and 0 <= y < n:
                if mat[x][y] > mat[i][j] and (x, y) not in visited:
                    best = max(best, 1 + dfs(x, y, visited))
                # 继续往同方向前进
                x += di
                y += dj
        visited.remove((i, j))
        memo[(i, j)] = best
        return best

    ans = 0
    for i in range(m):
        for j in range(n):
            ans = max(ans, dfs(i, j, set()))
    return ans
```

> **代码要点说明**  
> 1. `while` 循环负责在同一行/列“跳过去”，相当于把「可以直接到达的格子」一次性列举出来。  
> 2. `visited` 用来防止在同一次递归路径中回到已经走过的格子，避免无限循环。  
> 3. `memo`（记忆化）把已经算好的子问题保存下来，防止重复计算——这已经把暴力搜索的时间从指数级降低到了 **每个格子只算一次**，但仍然需要在每个格子里遍历整行/整列，最坏情况是 `O(m·n·(m+n))`，仍然太慢。

#### 复杂度  

- **时间复杂度**：`O(m·n·(m+n))`  
  - 想象每个格子都要检查所在行的 `n` 个格子和所在列的 `m` 个格子，乘起来就是这么多次比较。  
  - 用大白话讲，就是如果矩阵是 1000×100 的话，最坏要做 1000·100·(1000+100) ≈ 1.1 × 10⁸ 次操作，远超 1 秒能跑的量。  
- **空间复杂度**：`O(m·n)`  
  - `memo`、递归栈和 `visited` 都需要保存每个格子的状态，最坏占用和格子数相同的空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出 **“同一行/列的所有更大格子”** 是我们每次需要关注的对象。  
如果我们能在 **遍历一次矩阵的过程中**，随时得到“当前格子所在行/列已经出现的、更小的格子里最长路径是多少”，就可以**直接算出**以当前格子为终点的最长路径，而不必再去遍历整行/整列。

**关键观察**  

1. **只和更小的格子有关**  
   - 因为只能往更大的数走，路径的方向是单调递增的。  
   - 如果我们把所有格子按照数值从小到大排序，处理到某个格子时，**它左边/上边已经处理过的格子一定比它小**，右边/下边的格子一定比它大（或者相等）。  

2. **同数值的格子不能相互转移**  
   - 题目要求“严格递增”，相同数值的格子之间不能走。  
   - 因此在一次遍历中，**必须把相同数值的格子分成一批**，先算出它们的 `dp`（最长路径长度），**等整批结束后再统一更新行/列的记录**。这样就不会出现 “同层次的格子互相利用” 的错误。

3. **只需要维护两张哈希表**  
   - `row_best[r]`：截至目前（已处理的更小格子）**行 r 中可以达到的最长路径**。  
   - `col_best[c]`：截至目前**列 c 中可以达到的最长路径**。  
   - 这两个表相当于“查字典”，key 是行号或列号，value 是当前的最大长度。  

**算法步骤**  

| 步骤 | 说明 |
|------|------|
| 1️⃣ 收集所有格子 | 把每个格子写成 `(value, row, col)` 的三元组，放进列表 `cells`。 |
| 2️⃣ 按值排序 | `cells.sort(key=lambda x: x[0])`，得到从小到大的处理顺序。 |
| 3️⃣ 分组遍历 | 用 `i` 循环遍历 `cells`，每次找出 **值相同的连续子数组**（记为 `group`）。 |
| 4️⃣ 计算本组 dp | 对 `group` 中的每个格子 `(v, r, c)`：<br> `dp = 1 + max(row_best.get(r,0), col_best.get(c,0))` <br>（如果该行/列之前没有更小格子，则取 0）。把 `dp` 暂存到 `tmp` 列表。 |
| 5️⃣ 更新记录 | 组处理完后，再遍历 `group`，把对应的 `dp` 写回 `row_best[r] = max(row_best.get(r,0), dp)`、`col_best[c] = max(col_best.get(c,0), dp)`。 |
| 6️⃣ 维护全局答案 | 在计算 `dp` 的时候，实时更新 `ans = max(ans, dp)`。 |

这样每个格子只被 **看两次**（一次算 dp，一次更新哈希表），且 **不需要遍历整行或整列**，时间主要花在排序上。

> **类比**  
> 想象你在参加一场“爬山接力赛”。每座山峰的海拔就是格子的数值。我们先把所有山峰按海拔从低到高排好队。每当轮到某座山峰时，只需要看“同一条线路上已经跑完的最高分”（行/列的 best），把自己的分数加 1，就得到以它为终点的最佳成绩。等本次海拔相同的山峰全部报完名后，再把它们的成绩写进线路记录，供后面更高的山峰使用。这样每条线路只需要记住当前的最高成绩，一次遍历就能算完全部。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def maxIncreasingCells(mat: List[List[int]]) -> int:
    """
    最优解：排序 + 动态规划（行/列的前缀最大值）
    时间 O(N log N)  空间 O(N)   N = m * n
    """
    m, n = len(mat), len(mat[0])
    cells = []                     # (value, row, col)
    for i in range(m):
        for j in range(n):
            cells.append((mat[i][j], i, j))

    # 1️⃣ 按值从小到大排序
    cells.sort(key=lambda x: x[0])

    # 2️⃣ 哈希表记录“截至目前”每行、每列的最长路径
    row_best = defaultdict(int)   # 行号 -> 最长长度
    col_best = defaultdict(int)   # 列号 -> 最长长度

    ans = 0
    i = 0
    while i < len(cells):
        # 3️⃣ 找出所有值相同的格子，组成一个 batch
        j = i
        while j < len(cells) and cells[j][0] == cells[i][0]:
            j += 1
        batch = cells[i:j]          # 这里的每个元素都是 (v, r, c)

        # 4️⃣ 先算本批次的 dp（不立刻写回 row_best/col_best）
        tmp = []                    # 暂存 (r, c, dp) 供后面统一更新
        for _, r, c in batch:
            # 取当前行、列已知的最大值，加上自己这一步
            dp = 1 + max(row_best[r], col_best[c])
            tmp.append((r, c, dp))
            ans = max(ans, dp)      # 维护全局最大

        # 5️⃣ 统一更新 row_best / col_best
        for r, c, dp in tmp:
            if dp > row_best[r]:
                row_best[r] = dp
            if dp > col_best[c]:
                col_best[c] = dp

        i = j                       # 继续处理下一批

    return ans
```

> **代码要点注释**  
> - `defaultdict(int)` 相当于“查字典”，如果键不存在就返回 0，正好对应“当前行/列还没有更小的格子”。  
> - 第 3 步的 `while` 循环把相同数值的格子划到同一批，确保它们互相之间不产生依赖。  
> - 第 4 步的 `dp = 1 + max(row_best[r], col_best[c])` 就是“把本格子接在已经得到的最长路径后面”。  
> - 只要遍历完所有格子，`ans` 就是答案。

#### 复杂度  

- **时间复杂度**：`O(N log N)`（`N = m·n`）  
  - `cells.sort` 需要 `N log N` 的比较。其余遍历、哈希表的查询与更新都是 `O(1)`，整体线性。  
  - 与暴力解相比，**从“每个格子遍历整行/整列”降到了“一次排序 + 常数次查表”**，速度提升数百倍。  

- **空间复杂度**：`O(N)`  
  - 存储 `cells`（每格一个三元组）以及 `row_best`、`col_best`（最多 `m + n ≤ N` 条记录）。  
  - 用大白话说，就是我们只需要记住原矩阵的全部格子和每行、每列的当前最佳长度，和输入规模同量级。

---

## 心得  

- **核心技巧**：**按值排序 + 行/列的“前缀最大值” DP**（相当于在每条横向或纵向的 “链表” 上维护一个滚动的最大值）。  
- **适用的类似题型**  
  1. **“矩阵中的最长递增路径”**（LeetCode 329）——可以用 DFS+记忆化，也可以在 DAG 上做拓扑 DP。  
  2. **“按照值的大小从小到大依次更新的网格游戏”**（如 LeetCode 1637 “Best Position for a Service Centre” 的变体）。  
  3. **“在一维数组里，按顺序更新区间最大值”**（线段树/单调栈的思路）——本题的行/列哈希表相当于“一维的单调递增记录”。  

- **一句话总结解题钥匙**：  
  > **把所有格子从小到大排队，利用“行‑最大”和“列‑最大”两张字典表，像接力赛一样把每个格子的最佳路径长度向前传递。**

---

## 反思  

- **第一反应**：看到“同一行或同一列可以跳”，立刻想到**图的遍历**（DFS/BFS），于是写了暴力递归。  
- **最容易踩的坑**  
  1. **同值格子互相影响**：如果在遍历时立刻更新 `row_best / col_best`，相同数值的格子会错误地把彼此的 `dp` 当作“更小的格子”，导致路径计数超过实际。必须**分批**处理。  
  2. **负数或极端值**：矩阵元素可以是负数，不能把初始化的最大值设成 `-inf` 再加 1，而是用 `0` 代表“还没有更小的格子”。  
  3. **行列数极不平衡**（例如 1×10⁵），仍需 `O(N log N)` 而不是 `O(m·n·(m+n))`。  

- **下次遇到同类题**：  
  1. **先思考是否存在单调性**（数值只能增大或只能减小）。  
  2. **尝试把所有状态按单调顺序排序**，看能否用“一次遍历 + 哈希/数组维护前缀最优”来转移。  
  3. **检查是否需要分批处理**（相同键值的状态是否会相互影响）。  

这样就能快速从“暴力搜索”跳到 **线性/对数级别** 的高效解法。祝你玩转矩阵与 DP！