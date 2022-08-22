# #1905. 统计子岛屿 / Count Sub Islands

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/count-sub-islands/)

---

## 题目（英文原版）

**Description**

You are given two m x n binary matrices grid1 and grid2 containing only 0's (representing water) and 1's (representing land). An island is a group of 1's connected 4-directionally (horizontal or vertical). Any cells outside of the grid are considered water cells.
An island in grid2 is considered a sub-island if there is an island in grid1 that contains all the cells that make up this island in grid2.
Return the number of islands in grid2 that are considered sub-islands.

**Examples**

**Example 1:**

```
Input: grid1 = [[1,1,1,0,0],[0,1,1,1,1],[0,0,0,0,0],[1,0,0,0,0],[1,1,0,1,1]], grid2 = [[1,1,1,0,0],[0,0,1,1,1],[0,1,0,0,0],[1,0,1,1,0],[0,1,0,1,0]]
Output: 3
Explanation: In the picture above, the grid on the left is grid1 and the grid on the right is grid2.
The 1s colored red in grid2 are those considered to be part of a sub-island. There are three sub-islands.
```

**Example 2:**

```
Input: grid1 = [[1,0,1,0,1],[1,1,1,1,1],[0,0,0,0,0],[1,1,1,1,1],[1,0,1,0,1]], grid2 = [[0,0,0,0,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,0,1,0],[1,0,0,0,1]]
Output: 2 
Explanation: In the picture above, the grid on the left is grid1 and the grid on the right is grid2.
The 1s colored red in grid2 are those considered to be part of a sub-island. There are two sub-islands.
```

**Constraints**

- m == grid1.length == grid2.length
- n == grid1[i].length == grid2[i].length
- 1 <= m, n <= 500
- grid1[i][j] and grid2[i][j] are either 0 or 1.

---

## 题目（中文翻译）

**题目描述**  
给定两个大小为 `m x n` 的二进制矩阵 `grid1` 和 `grid2`，其中仅包含 `0`（表示水）和 `1`（表示陆地）。岛屿是指由 4 向（上下左右）相连的 `1` 组成的连通块。网格外部的所有单元格均视为水域。  

如果 `grid2` 中的一个岛屿的所有组成单元格，都被 `grid1` 中的同一个岛屿所覆盖，则该岛屿被称为 **子岛屿（sub-island）**。  
返回 `grid2` 中子岛屿的数量。

**示例 1**  
```text
Input: grid1 = [[1,1,1,0,0],
                [0,1,1,1,1],
                [0,0,0,0,0],
                [1,0,0,0,0],
                [1,1,0,1,1]],
       grid2 = [[1,1,1,0,0],
                [0,0,1,1,1],
                [0,1,0,0,0],
                [1,0,1,1,0],
                [0,1,0,1,0]]
Output: 3
Explanation: 上图左侧为 `grid1`，右侧为 `grid2`。  
`grid2` 中用红色标记的 `1` 表示属于子岛屿的单元格，共有三个子岛屿。
```

**示例 2**  
```text
Input: grid1 = [[1,0,1,0,1],
                [1,1,1,1,1],
                [0,0,0,0,0],
                [1,1,1,1,1],
                [1,0,1,0,1]],
       grid2 = [[0,0,0,0,0],
                [1,1,1,1,1],
                [0,1,0,1,0],
                [0,1,0,1,0],
                [1,0,0,0,1]]
Output: 2
Explanation: 上图左侧为 `grid1`，右侧为 `grid2`。  
`grid2` 中用红色标记的 `1` 表示属于子岛屿的单元格，共有两个子岛屿。
```

**约束条件**  
- `m == grid1.length == grid2.length`
- `n == grid1[i].length == grid2[i].length`
- `1 <= m, n <= 500`
- `grid1[i][j]` 和 `grid2[i][j]` 只能是 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **先把 `grid2` 里的每座岛屿找出来**  
   - 岛屿的定义是「上下左右四个方向相连的 `1`」——这正好可以用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 来「淹没」整座岛。  
   - 想象一下把地图放在桌子上，用手指从某个 `1` 出发，顺着上下左右「涂颜色」把所有相连的 `1` 涂成相同的颜色，这个过程就是一次 DFS/BFS。  

2. **判断这座岛是否是子岛**  
   - 在涂的过程中，同时检查对应位置的 `grid1` 是否也是 `1`。  
   - 只要出现一次 `grid2` 为 `1` 而 `grid1` 为 `0`，说明这块陆地在 `grid1` 里是水，整座岛就 **不可能** 完全被 `grid1` 的某座岛包含，直接判为「不是子岛」。  

3. **计数**  
   - 完成一次 DFS 后，如果没有出现上述不匹配，就把计数器 `ans` 加一。  

> **为什么这方法一定对？**  
> - 每一次 DFS 都恰好遍历了一座完整的 `grid2` 岛屿（因为我们只在 `grid2` 为 `1` 且未访问过的格子上启动）。  
> - 只要岛屿内部所有格子在 `grid1` 里也是陆地，这座岛必然被 `grid1` 的某座更大的岛完全覆盖——这正是子岛的定义。  

#### 代码（Python）  

```python
from typing import List

def countSubIslands(grid1: List[List[int]], grid2: List[List[int]]) -> int:
    m, n = len(grid1), len(grid1[0])
    visited = [[False] * n for _ in range(m)]

    # 四个方向的偏移量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(x: int, y: int) -> bool:
        """返回这座岛是否全部在 grid1 里是陆地"""
        stack = [(x, y)]
        visited[x][y] = True
        # 只要有一次对应位置在 grid1 为 0，就不是子岛
        is_sub = grid1[x][y] == 1

        while stack:
            cx, cy = stack.pop()
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                # 越界或已经访问或在 grid2 里不是陆地，直接跳过
                if not (0 <= nx < m and 0 <= ny < n):
                    continue
                if visited[nx][ny] or grid2[nx][ny] == 0:
                    continue
                visited[nx][ny] = True
                # 检查对应的 grid1 是否为陆地
                if grid1[nx][ny] == 0:
                    is_sub = False
                stack.append((nx, ny))
        return is_sub

    ans = 0
    for i in range(m):
        for j in range(n):
            # 只从 grid2 的未访问陆地格子启动 DFS
            if grid2[i][j] == 1 and not visited[i][j]:
                if dfs(i, j):
                    ans += 1
    return ans
```

> **关键行中文注释**  
> - `visited` 用来记录哪些格子已经被「淹没」过，防止重复遍历（类似字典查词，key 是格子坐标，value 是是否已访问）。  
> - `is_sub` 初始值取决于起点格子在 `grid1` 是否为陆地，后面只要出现一次 `0` 就把它设为 `False`。  
> - `stack` 实现了非递归的 DFS，避免 Python 递归深度限制。  

#### 复杂度  

- **时间复杂度：** `O(m·n)`  
  - 每个格子最多被访问一次（进入 `stack` 并弹出），所以整体是线性遍历整个矩阵。  
  - 大白话：如果把地图想象成 `m·n` 块拼图，老师只需要看一遍每块拼图，就能算出答案。  

- **空间复杂度：** `O(m·n)`（`visited` 数组）  
  - 需要额外的布尔矩阵记录访问状态，最坏情况（全是陆地）时占用整个矩阵大小的空间。  

---  

### 2. 最优解  

#### 思路  

暴力解已经是 **线性** 的，已经很快了。但我们仍可以在 **遍历过程中提前剪枝**，让代码更简洁、常数更小。核心思想：

1. **在遍历 `grid2` 时直接把不可能成为子岛的格子“清掉”。**  
   - 如果 `grid2[i][j] == 1` 而 `grid1[i][j] == 0`，这块陆地在 `grid1` 里是水，说明它所在的整座岛肯定不可能是子岛。我们可以把它以及它相连的所有 `grid2` 陆地全部置为 `0`（相当于一次 “抹掉”），这样后面就不会再去检查这座岛。  

2. **再一次遍历剩下的 `grid2`，每次遇到 `1` 就算一座子岛。**  
   - 此时剩下的所有 `1` 必然在对应位置的 `grid1` 也是 `1`，所以每一次 DFS 直接计数即可。  

这样把 **“检查 + 计数”** 两步拆成 **“先剔除不合格的岛”** + **“直接计数剩余岛”**，实现了 **一次遍历 + 一次 DFS** 的时间复杂度，仍是 `O(m·n)`，但只需要一次 `visited` 数组（甚至可以直接在原矩阵上修改），空间可以降到 `O(1)`（不计递归栈）。  

> **核心数据结构**  
> - **DFS（栈）**：仍然是遍历岛屿的工具。  
> - **原地修改**：把 `grid2` 中不符合子岛条件的格子直接改成 `0`，相当于在原地图上“画掉”。  

#### 代码（Python）  

```python
from typing import List

def countSubIslands(grid1: List[List[int]], grid2: List[List[int]]) -> int:
    m, n = len(grid1), len(grid1[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 第一次 DFS：把所有「在 grid1 里是水」的 grid2 陆地全部抹掉
    def erase_invalid(x: int, y: int) -> None:
        stack = [(x, y)]
        grid2[x][y] = 0                     # 直接改为水，表示已经“清除”
        while stack:
            cx, cy = stack.pop()
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < m and 0 <= ny < n and grid2[nx][ny] == 1:
                    # 只要对应的 grid1 也是水，就继续抹掉
                    if grid1[nx][ny] == 0:
                        grid2[nx][ny] = 0
                        stack.append((nx, ny))
                    else:
                        # 这里先不抹掉，等第二遍计数时会遍历
                        pass

    # 第二次 DFS：统计剩余的完整子岛
    def dfs_count(x: int, y: int) -> None:
        stack = [(x, y)]
        grid2[x][y] = 0                     # 访问后直接置零，避免额外 visited
        while stack:
            cx, cy = stack.pop()
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < m and 0 <= ny < n and grid2[nx][ny] == 1:
                    grid2[nx][ny] = 0
                    stack.append((nx, ny))

    # 1️⃣ 抹掉所有不可能的岛屿
    for i in range(m):
        for j in range(n):
            if grid2[i][j] == 1 and grid1[i][j] == 0:
                erase_invalid(i, j)

    # 2️⃣ 计数剩下的子岛
    ans = 0
    for i in range(m):
        for j in range(n):
            if grid2[i][j] == 1:            # 只剩下完全匹配的岛屿
                ans += 1
                dfs_count(i, j)             # 把整座岛抹掉，防止重复计数
    return ans
```

> **代码要点**  
> - `erase_invalid` 只在发现 `grid1` 为水的格子时才把对应的 `grid2` 陆地置零，等价于「把所有不可能的子岛提前删掉」。  
> - `dfs_count` 只负责「计数」并把已计数的岛屿彻底清零，省去了额外的 `visited` 矩阵。  

#### 复杂度  

- **时间复杂度：** `O(m·n)`  
  - 第一次遍历每个格子最多进入一次 `erase_invalid`（只在不匹配的格子上），第二次遍历每个格子最多进入一次 `dfs_count`，合计仍是线性。  

- **空间复杂度：** `O(1)`（不计递归/栈的临时空间）  
  - 直接在 `grid2` 上原地修改，不需要额外的 `visited` 数组。栈的最大深度最多等于岛屿的格子数，最坏情况下为 `m·n`，但这是算法本身的递归/迭代栈，常数级别的额外空间。  

---  

## 心得  

- **核心技巧**：**二维网格的 Flood Fill（DFS/BFS）** + **原地过滤**。  
- **适用的题型**：  
  1. “岛屿计数” 类题（如 LeetCode 200、694）。  
  2. “子结构” 判断类题（如判断子岛、子矩阵是否全为 1）。  
- **一句话总结解题钥匙**：**先把“不合格的区域”剔除，再把剩余的“合格区域”直接计数**。  

---  

## 反思  

- **第一反应**：看到“子岛”这几个字，马上想到 **遍历每座岛屿并逐格比较**。  
- **最容易踩的坑**：  
  - **忘记四方向连通**（只检查上下或左右会漏掉岛屿）。  
  - **边界条件**：遍历时一定要判断 `0 ≤ x < m`、`0 ≤ y < n`，防止数组越界。  
  - **重复计数**：没有做好“已访问”标记会把同一座岛屿算多次。  
- **下次类似题的第一步**：**在遍历前先标记/过滤掉明显不满足条件的格子**（比如“在另一张图里是水”），这样后面的计数过程会更简洁、错误更少。