# #3619. 统计总值能被 K 整除的岛屿数量 / Count Islands With Total Value Divisible by K

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/count-islands-with-total-value-divisible-by-k/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix grid and a positive integer k. An island is a group of positive integers (representing land) that are 4-directionally connected (horizontally or vertically).
The total value of an island is the sum of the values of all cells in the island.
Return the number of islands with a total value divisible by k.

**Examples**

**Example 1:**

```
Input: grid = [[0,2,1,0,0],[0,5,0,0,5],[0,0,1,0,0],[0,1,4,7,0],[0,2,0,0,8]], k = 5
Output: 2
Explanation:
The grid contains four islands. The islands highlighted in blue have a total value that is divisible by 5, while the islands highlighted in red do not.
```

**Example 2:**

```
Input: grid = [[3,0,3,0], [0,3,0,3], [3,0,3,0]], k = 3
Output: 6
Explanation:
The grid contains six islands, each with a total value that is divisible by 3.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 105
- 0 <= grid[i][j] <= 106
- 1 <= k <= 106

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m x n` 矩阵（matrix）`grid` 和一个正整数（positive integer）`k`。  
岛屿（island）是由正整数（representing land）组成的、在水平方向或垂直方向上四方向相连（4-directionally connected）的单元格（cells）集合。  
一个岛屿的总值（total value）是该岛屿所有单元格的值的求和（sum）。  
返回总值能被 `k` 整除的岛屿数量。

**示例**

*示例 1*  
```text
Input: grid = [[0,2,1,0,0],[0,5,0,0,5],[0,0,1,0,0],[0,1,4,7,0],[0,2,0,0,8]], k = 5
Output: 2
Explanation:
网格中共有四个岛屿。蓝色标记的岛屿其总值能够被 5 整除，而红色标记的岛屿则不行。
```

*示例 2*  
```text
Input: grid = [[3,0,3,0], [0,3,0,3], [3,0,3,0]], k = 3
Output: 6
Explanation:
网格中共有六个岛屿，每个岛屿的总值都能被 3 整除。
```

**约束条件**
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 1000`
- `1 <= m * n <= 10^5`
- `0 <= grid[i][j] <= 10^6`
- `1 <= k <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **遍历每一个格子**，只要它的值大于 `0`（代表陆地），就把它当作一个“新岛屿”的起点。  
2. 从这个起点出发，用**深度优先搜索（DFS）**或**广度优先搜索（BFS）**把所有 4‑方向相连的陆地全部找出来，累加这些格子的数值，得到该岛屿的总价值。  
3. 判断总价值是否能被 `k` 整除，能的话计数 `+1`。  

> **数据结构类比**：  
> - **栈 / 队列**：在搜索过程中我们会把“待处理的格子”放进一个容器，就像把要查的单词放进字典的待查列表。  
> - **visited 标记**：相当于在字典里划掉已经查过的词，防止重复计数。

**为什么这个方法一定能得到正确答案？**  
因为我们对每个未访问的陆地格子都完整地遍历了它所在的连通分量（即一个岛屿），没有遗漏也没有重复计数。只要遍历完所有格子，所有岛屿都会被统计。

**时间/空间复杂度**  
- **时间**：对每个格子我们都可能发起一次搜索，而一次搜索在最坏情况下会遍历整个矩阵（比如全部都是陆地），于是时间复杂度是 **O((m·n)²)**。  
  - 大白话：如果矩阵有 10,000 格子，最坏要检查 100,000,000 次——这在实际运行时会非常慢。  
- **空间**：递归版 DFS 需要调用栈深度最多 `m·n`，或者 BFS 需要一个队列保存最多 `m·n` 个坐标，额外空间是 **O(m·n)**。

#### 代码（Python）

```python
from collections import deque
from typing import List

def count_islands_bruteforce(grid: List[List[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    ans = 0

    # 四个方向向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 对每个格子都尝试一次 BFS（即使已经访问过也会重复）
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:          # 0 表示水，直接跳过
                continue

            # 使用 BFS 收集整个连通块的总价值
            total = 0
            q = deque()
            q.append((i, j))

            # 为了让暴力解“每次都重新搜索”，这里我们不使用全局 visited，
            # 而是把搜索到的格子临时标记为 0（相当于“已经被吃掉”），
            # 搜索结束后再恢复原值，这样后面的循环仍然会再次遍历它们。
            original = grid[i][j]          # 记住起点原始数值
            grid[i][j] = 0                  # 先把起点设为水，防止无限循环

            while q:
                x, y = q.popleft()
                total += original if (x, y) == (i, j) else grid[x][y]  # 加上当前格子的数值

                # 恢复被改成 0 的格子（因为我们在遍历时会把它们改成 0，后面要恢复）
                if (x, y) != (i, j):
                    original = grid[x][y]
                    grid[x][y] = 0

                # 向四个方向扩展
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] != 0:
                        q.append((nx, ny))
                        # 把加入队列的格子标记为已访问（改成 0）
                        grid[nx][ny] = 0

            # 恢复所有被改成 0 的格子（这里为了演示暴力思路，实际代码会更繁琐）
            # ……（略）

            if total % k == 0:
                ans += 1

    return ans
```

> **注意**：上面的实现只是为了展示“每次都重新遍历整个岛屿”的思想，实际写起来会非常麻烦且效率极低。下面我们会给出真正实用的最优解。

#### 复杂度

- **时间复杂度**：`O((m·n)²)`  
  - 解释：如果矩阵有 `N = m·n` 个格子，最坏每次搜索都会遍历 `N` 格子，搜索会被发起 `N` 次，故总操作数约为 `N²`。  
- **空间复杂度**：`O(m·n)`（用于 BFS 队列或递归栈）  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历同一个岛屿**。  
我们只需要在第一次遍历时把岛屿的所有格子标记为“已经访问”，后面再遇到这些格子时直接跳过，这样每个格子只会被处理 **一次**。

实现步骤如下：

1. **准备一个 `visited` 矩阵**（布尔值），大小和 `grid` 一致，初始全为 `False`。  
   - 类比：这就像在查字典时在每个词后面贴一个“已看过”的标签，防止重复阅读。  

2. **遍历整个矩阵**，遇到 `grid[i][j] > 0` 且 `visited[i][j] == False` 时，说明发现了一个新岛屿的入口。  

3. 对该入口进行 **BFS（或 DFS）**：  
   - 使用队列 `deque` 保存待访问的坐标。  
   - 每弹出一个坐标，就把它的数值加入当前岛屿的 **累计和 `total`**。  
   - 将它的四个相邻格子（上下左右）中满足 `grid[nx][ny] > 0` 且未访问的加入队列，并标记为已访问。  

4. BFS 结束后，**判断 `total % k == 0`**，如果成立则答案 `ans += 1`。  

5. 最终遍历结束，返回 `ans`。

**为什么只遍历一次就能得到正确答案？**  
因为 `visited` 把每个陆地格子锁定在它所在的连通块（岛屿）第一次被搜索时完成标记，后续再看到该格子时直接跳过，保证了 **每个格子只被计入一次**，而岛屿的总价值正好是在它所在的那一次 BFS 中完整累加的。

**关键算法/数据结构解释**  

- **BFS（广度优先搜索）**：把“待处理的格子”放进一个**队列**，先处理离入口最近的格子，逐层向外扩散。想象在一块橡皮上滴水，水会先湿润最靠近滴点的区域，然后向四周蔓延，这个过程正好对应 BFS。  
- **队列（deque）**：在 Python 中 `collections.deque` 支持 **O(1)** 的左端弹出和右端追加，非常适合实现 BFS。  
- **visited 矩阵**：类似字典的“查找表”，用 `True/False` 快速判断格子是否已经处理，时间复杂度是 **O(1)**。  

**复杂度分析**  
- 每个格子最多进入队列一次，出队一次，且只检查四个方向，整体是线性时间 **O(m·n)**。  
- 额外的 `visited` 矩阵占用 **O(m·n)** 的空间，队列的最大长度也不会超过 `m·n`，所以空间也是 **O(m·n)**。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def count_islands(grid: List[List[int]], k: int) -> int:
    """
    返回总价值能被 k 整除的岛屿数量
    """
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]   # 记录每个格子是否已访问
    ans = 0

    # 四个方向的移动向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(m):
        for j in range(n):
            # 只在遇到未访问的陆地格子时启动一次 BFS
            if grid[i][j] > 0 and not visited[i][j]:
                total = 0                 # 当前岛屿的数值累计
                q = deque()
                q.append((i, j))
                visited[i][j] = True      # 入口立刻标记为已访问

                while q:
                    x, y = q.popleft()
                    total += grid[x][y]    # 累加当前格子的数值

                    # 向四个方向扩展
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        # 边界检查 + 必须是陆地 + 未访问
                        if 0 <= nx < m and 0 <= ny < n \
                                and grid[nx][ny] > 0 and not visited[nx][ny]:
                            q.append((nx, ny))
                            visited[nx][ny] = True   # 立即标记，防止重复入队

                # BFS 完成后判断总价值是否能被 k 整除
                if total % k == 0:
                    ans += 1

    return ans
```

> **代码要点注释**  
> - `visited[i][j] = True` 必须在把坐标加入队列 **之前** 标记，否则同一个格子可能会被多次加入，导致队列膨胀。  
> - `total += grid[x][y]` 在每次弹出时累计，保证每个格子的值只加一次。  

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 解释：矩阵里每个格子最多被访问一次，四个方向检查常数次，总操作数和格子数量成线性关系。与暴力解相比，从 “平方级” 降到了 “线性级”。  
- **空间复杂度**：`O(m·n)`  
  - 解释：`visited` 矩阵占用 `m·n` 个布尔值，队列最坏也会装满整张地图的格子，都是线性空间。

---

## 心得

- **核心技巧**：**使用 BFS/DFS 把连通块（岛屿）一次遍历完，同时用 `visited` 防止重复搜索**。  
- **适用的题型**（类似思路）：  
  1. “岛屿的最大面积”（LeetCode 695）  
  2. “统计矩阵中不同连通区域的数量”（如 200. Number of Islands）  
  3. “岛屿周长 / 边界长度”等需要一次遍历求和的题目  
- **一句话总结解题钥匙**：**“一次遍历 + 标记已访问” 能把原本指数级的重复搜索压到线性时间。**

---

## 反思

- **第一反应**：看到“4‑方向相连的正整数”立刻想到 **连通分量**，于是想用 **DFS/BFS** 把每个岛屿遍历出来。  
- **最容易踩的坑**：  
  - 忘记对已经访问过的格子做标记，导致同一个岛屿被多次计数（时间爆炸）。  
  - 边界检查写错（比如 `nx < 0` 或 `ny >= n`）会出现 IndexError。  
  - `k` 可能为 1，所有岛屿都满足条件，答案应等于岛屿总数。  
- **下次类似题的第一步**：**先判断是否已经遍历过（visited），再决定是否开启一次完整的 BFS/DFS**。这样可以确保每个连通块只处理一次，效率自然最优。