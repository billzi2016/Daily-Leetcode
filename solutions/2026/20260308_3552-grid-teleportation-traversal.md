# #3552. 网格传送遍历 / Grid Teleportation Traversal

> 难度：中等 · 标签：Array、Hash Table、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/grid-teleportation-traversal/)

---

## 题目（英文原版）

**Description**

You are given a 2D character grid matrix of size m x n, represented as an array of strings, where matrix[i][j] represents the cell at the intersection of the ith row and jth column. Each cell is one of the following:
You start at the top-left cell (0, 0), and your goal is to reach the bottom-right cell (m - 1, n - 1). You can move from the current cell to any adjacent cell (up, down, left, right) as long as the destination cell is within the grid bounds and is not an obstacle.
If you step on a cell containing a portal letter and you haven't used that portal letter before, you may instantly teleport to any other cell in the grid with the same letter. This teleportation does not count as a move, but each portal letter can be used at most once during your journey.
Return the minimum number of moves required to reach the bottom-right cell. If it is not possible to reach the destination, return -1.

**Examples**

**Example 1:**

```
Input: matrix = ["A..",".A.","..."]
Output: 2
Explanation:
```

**Example 2:**

```
Input: matrix = [".#...",".#.#.",".#.#.","...#."]
Output: 13
Explanation:
```

**Constraints**

- 1 <= m == matrix.length <= 103
- 1 <= n == matrix[i].length <= 103
- matrix[i][j] is either '#', '.', or an uppercase English letter.
- matrix[0][0] is not an obstacle.

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的二维字符网格（grid）`matrix`，以字符串数组的形式表示，其中 `matrix[i][j]` 表示第 `i` 行第 `j` 列交叉处的单元格（cell）。每个单元格的内容只能是以下三种之一：

- `'#'` 表示障碍物（obstacle），不可通行；
- `'.'` 表示普通空地；
- 大写英文字母表示传送门字母（portal letter），可以进行瞬移。

你从左上角单元格 `(0, 0)` 开始，目标是到达右下角单元格 `(m‑1, n‑1)`。在移动时，你可以向上、下、左、右四个方向的相邻单元格（adjacent cell）移动，前提是目标单元格在网格范围内且不是障碍物。

如果你踏上了一个含有传送门字母的单元格，并且之前没有使用过该字母的传送门，则可以**瞬间传送**（teleport）到网格中任意其他拥有相同字母的单元格。此传送不计入移动次数，但每个传送门字母在整条路径中最多只能使用一次。

返回到达右下角单元格所需的最少移动次数。如果无法到达目标，返回 `-1`。

**示例 1**  
Input: `matrix = ["A..",".A.","..."]`  
Output: `2`  
解释：

**示例 2**  
Input: `matrix = [".#...",".#.#.",".#.#.","...#."]`  
Output: `13`  
解释：

**约束条件**  
- `1 <= m == matrix.length <= 10^3`  
- `1 <= n == matrix[i].length <= 10^3`  
- `matrix[i][j]` 只能是 `'#'`、`'.'` 或大写英文字母。  
- `matrix[0][0]` 不是障碍物。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有合法的走法都穷举**，直到找到从左上角 `(0,0)` 到右下角 `(m‑1,n‑1)` 的最短路径。  
- **数据结构**：我们可以把格子当成图的节点，用 **队列**（queue）来实现 **广度优先搜索（BFS）**，因为 BFS 天生能找到最短步数。  
- **传送门**：如果当前格子是字母 `A~Z`，我们把**所有同字母的格子**都当成它的邻居，直接加入队列。这里把“同字母的格子”想象成一本词典里所有出现同一个词的页面，查找时要遍历整本词典。  

为什么这个方法一定能得到答案？  
- BFS 按层展开，先访问的都是走 `0` 步、`1` 步、`2` 步…的格子，一旦我们第一次碰到终点，就一定是最少步数。  
- 只要把 **所有可能的移动**（上下左右 + 同字母的任意跳）都加进去，搜索就不会漏掉任何合法路径。  

**时间复杂度**  
- 每取出一个格子，我们要检查四个方向，**以及**如果是字母，还要遍历**所有同字母的格子**。最坏情况是整个矩阵都是同一个字母 `A`，那么每次使用传送门都要遍历 `m·n` 个格子。于是时间复杂度约为 `O((m·n)²)`，即“平方级”。  
- 用大白话说，如果矩阵有 10,000 格子，暴力解大约要检查 100,000,000 次，显然会超时。  

**空间复杂度**  
- 需要一个 `visited` 数组记录是否已经走过，大小为 `m·n`，再加上 BFS 队列最坏也会装下所有格子，故为 `O(m·n)`。

#### 代码（Python）

```python
from collections import deque
from typing import List

def min_moves_bruteforce(matrix: List[str]) -> int:
    m, n = len(matrix), len(matrix[0])
    # 四个方向向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 记录是否访问过，防止死循环
    visited = [[False] * n for _ in range(m)]
    q = deque()
    q.append((0, 0, 0))          # (行, 列, 已走步数)
    visited[0][0] = True

    while q:
        x, y, steps = q.popleft()
        # 到达右下角，返回步数
        if x == m - 1 and y == n - 1:
            return steps

        # 1. 普通四向移动
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n \
               and not visited[nx][ny] \
               and matrix[nx][ny] != '#':
                visited[nx][ny] = True
                q.append((nx, ny, steps + 1))

        # 2. 传送门：遍历所有同字母格子（暴力）
        ch = matrix[x][y]
        if 'A' <= ch <= 'Z':          # 只对字母格子做传送
            for i in range(m):
                for j in range(n):
                    if (i, j) != (x, y) and matrix[i][j] == ch \
                       and not visited[i][j]:
                        visited[i][j] = True
                        # 传送不计步数，所以 steps 不加 1
                        q.append((i, j, steps))

    # BFS 结束仍未到达终点，说明不可达
    return -1
```

#### 复杂度

- **时间复杂度**：`O((m·n)²)`  
  解释：每访问一个格子（共 `m·n` 次），在最坏情况下要遍历整个矩阵找同字母的格子，又是 `m·n`，于是乘起来就是平方级。

- **空间复杂度**：`O(m·n)`  
  解释：`visited` 表和 BFS 队列最多各保存一次整张格子的信息。

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈在 **“每次使用传送门都要遍历整张矩阵”**。  
我们可以把 **同字母的所有格子** 预先收集好，形成一个**字母 → 坐标列表**的映射（类似字典的“查字典”），这样：

1. **预处理**：一次遍历矩阵，把每个出现的字母对应的坐标放进哈希表 `portal_map`。  
   - 这一步的时间是 `O(m·n)`，空间同样是 `O(m·n)`（因为每个格子最多出现一次）。  
2. **BFS 时**：当我们走到字母格子时，直接取出 `portal_map[letter]`，一次性得到所有可以瞬移到的格子。  
3. **一次性使用**：每个字母的传送门只能使用一次。我们在第一次使用完后，把 `portal_map[letter]` 清空（或标记为已用），以后再走到同字母格子时就不会重复遍历，这保证了 **每个格子最多只会被加入队列一次**。  

这样，**所有传送操作的总耗时等同于遍历所有格子一次**，不再出现二次遍历的平方爆炸。

> **类比**：把每个字母看成一本“快捷通道手册”，手册里列出所有对应的页面。我们只打开一次手册，拿走所有页面后把手册扔掉——以后再看到相同的字母，就不需要再翻手册了。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def min_moves(matrix: List[str]) -> int:
    m, n = len(matrix), len(matrix[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 1️⃣ 预处理：收集每个字母对应的所有坐标
    portal_map = defaultdict(list)          # letter -> [(x1,y1), (x2,y2), ...]
    for i in range(m):
        for j in range(n):
            ch = matrix[i][j]
            if 'A' <= ch <= 'Z':
                portal_map[ch].append((i, j))

    # 2️⃣ BFS
    visited = [[False] * n for _ in range(m)]
    q = deque()
    q.append((0, 0, 0))          # (行, 列, 已走步数)
    visited[0][0] = True

    while q:
        x, y, steps = q.popleft()
        if x == m - 1 and y == n - 1:      # 到达终点
            return steps

        # ① 四向普通移动
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n \
               and not visited[nx][ny] \
               and matrix[nx][ny] != '#':
                visited[nx][ny] = True
                q.append((nx, ny, steps + 1))

        # ② 传送门：一次性取出所有同字母格子
        ch = matrix[x][y]
        if 'A' <= ch <= 'Z' and portal_map.get(ch):
            for nx, ny in portal_map[ch]:
                if not visited[nx][ny]:
                    visited[nx][ny] = True
                    # 传送不计步数
                    q.append((nx, ny, steps))
            # 使用完该字母后清空，防止后续再次遍历
            portal_map[ch].clear()

    # BFS 结束仍未到达右下角
    return -1
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 预处理遍历一次矩阵 `O(m·n)`。  
  - BFS 中每个格子最多入队一次，四向检查是常数时间，传送门每个字母只会被展开一次，总共也不超过 `m·n` 次。  
  - 与暴力解相比，**把平方级降到了线性级**，即“遍历一次矩阵就够了”。  

- **空间复杂度**：`O(m·n)`  
  - `visited` 表占 `m·n`。  
  - `portal_map` 最多保存所有字母格子的坐标，合计也不超过 `m·n`。  
  - 与暴力解的空间使用相同，但因为时间更快，整体效率更高。

---

## 心得

- **核心技巧**：把**同类传送点视为一个“超级节点”**，并在第一次使用后“一劳永逸”地清空，避免重复遍历。  
- **适用场景**：  
  1. **字母/颜色/编号相同的格子可以瞬移**（如 LeetCode 1345 “Jump Game IV”）。  
  2. **图中存在“一键到达”类的多对多连通**（如迷宫中的传送门、跳板）。  
  3. **需要最短路径且边权相同** 的问题，通常可以用 BFS 加上类似的预处理。  
- **一句话总结**：**把所有同字母格子预先收集，使用一次后立即删除**，即可在 BFS 中实现 O(1) 的瞬移查询，保证整体线性时间。

---

## 反思

- **第一反应**：看到“可以瞬移到同字母的任意格子”，立刻想到把所有同字母格子当成邻居直接在 BFS 中遍历。  
- **最容易踩的坑**：  
  - **重复展开同一字母**：如果不在使用后清空列表，会导致每次走到该字母格子都重新遍历所有同字母格子，时间会回到平方级。  
  - **障碍格子 `#`**：一定要在四向移动和传送前检查，防止误把障碍当成可达点。  
  - **起点或终点本身是字母**：起点的传送必须在进入 BFS 循环后立即处理，否则会遗漏一次“免费”瞬移。  
- **下次遇到类似题**：**第一步**先**建立字母 → 坐标列表的映射**，并记住“使用一次后清空”。这一步几乎可以把所有“同类瞬移”类问题的时间复杂度从平方级降到线性级。