# #1559. 检测二维网格中的环 / Detect Cycles in 2D Grid

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/detect-cycles-in-2d-grid/)

---

## 题目（英文原版）

**Description**

Given a 2D array of characters grid of size m x n, you need to find if there exists any cycle consisting of the same value in grid.
A cycle is a path of length 4 or more in the grid that starts and ends at the same cell. From a given cell, you can move to one of the cells adjacent to it - in one of the four directions (up, down, left, or right), if it has the same value of the current cell.
Also, you cannot move to the cell that you visited in your last move. For example, the cycle (1, 1) -> (1, 2) -> (1, 1) is invalid because from (1, 2) we visited (1, 1) which was the last visited cell.
Return true if any cycle of the same value exists in grid, otherwise, return false.

**Examples**

**Example 1:**

```
Input: grid = [["a","a","a","a"],["a","b","b","a"],["a","b","b","a"],["a","a","a","a"]]
Output: true
Explanation: There are two valid cycles shown in different colors in the image below:
```

**Example 2:**

```
Input: grid = [["c","c","c","a"],["c","d","c","c"],["c","c","e","c"],["f","c","c","c"]]
Output: true
Explanation: There is only one valid cycle highlighted in the image below:
```

**Example 3:**

```
Input: grid = [["a","b","b"],["b","z","b"],["b","b","a"]]
Output: false
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 500
- grid consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的字符二维数组（2D array）`grid`，请判断网格中是否存在由相同字符组成的环。

**环的定义**  
- 环是一条长度不少于 4 的路径，起点与终点是同一个单元格。  
- 从当前单元格出发，只能向上、下、左、右四个方向的相邻单元格移动，且相邻单元格的字符必须与当前单元格相同。  
- 不能回到上一步刚刚访问过的单元格。例如，路径 `(1, 1) -> (1, 2) -> (1, 1)` 是无效的，因为在从 `(1, 2)` 移动时回到了上一步访问的 `(1, 1)`。

如果网格中存在任意一个满足上述条件的环，返回 `true`；否则返回 `false。

### 示例

#### 示例 1
**输入**  
```json
grid = [["a","a","a","a"],
        ["a","b","b","a"],
        ["a","b","b","a"],
        ["a","a","a","a"]]
```
**输出**  
```
true
```
**解释**  
下图中用不同颜色标记的两个环都是合法的：

#### 示例 2
**输入**  
```json
grid = [["c","c","c","a"],
        ["c","d","c","c"],
        ["c","c","e","c"],
        ["f","c","c","c"]]
```
**输出**  
```
true
```
**解释**  
图中唯一的合法环已用颜色标出：

#### 示例 3
**输入**  
```json
grid = [["a","b","b"],
        ["b","z","b"],
        ["b","b","a"]]
```
**输出**  
```
false
```

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 500`
- `grid` 仅包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每条可能的路径都枚举一遍**，只要找到一条长度 ≥ 4 且起点＝终点、且路径上所有格子的字符都相同，就说明存在环。  
可以这样实现：

1. 从网格中的每个格子 `(i, j)` 作为起点，开启一次深度优先搜索（DFS）。  
2. 在递归过程中把已经走过的格子放进一个 `path` 集合，防止在同一次搜索里走回头路。  
3. 每走一步检查四个相邻格子（上、下、左、右），如果相邻格子字符相同且 **不是上一格**，就继续向前走。  
4. 当我们再次来到起点且路径长度已经 ≥ 4 时，返回 `True` 表示找到环。  

> **类比**：把网格想成一张城市地图，格子是街区，字符相同的街区可以相互通行。暴力解相当于让一位游客从每个街区出发，**不停地在所有可能的道路上兜圈子**，只要有一次走回原点且走了四条以上的路，就算成功。

**为什么能得到正确答案**  
因为我们穷举了**所有**可能的合法路径，只要有环必然会被遍历到，自然返回 `True`；如果所有路径都检查完仍未发现环，则说明不存在。

**时间/空间复杂度**  
- **时间复杂度**：每个格子都可能作为起点，且每次搜索会在最坏情况下遍历所有可能的路径。对于每一步都有至多 4 条分支，路径长度最多是 `m*n`，所以时间复杂度是指数级的，记作 `O(4^{m*n})`（实际会更小，但仍然是**爆炸**的）。用大白话说，就是“**跑得比跑马拉松还快**”。  
- **空间复杂度**：递归栈的深度最多是格子总数 `m*n`，再加上 `path` 集合，需要 `O(m*n)` 的额外空间。

> 暴力解虽然思路最直观，但在 `m,n` 达到 500 时根本不可行。

#### 代码（Python）

```python
from typing import List, Tuple, Set

def has_cycle_bruteforce(grid: List[List[str]]) -> bool:
    m, n = len(grid), len(grid[0])
    # 四个方向向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 判断坐标是否合法
    def in_grid(x: int, y: int) -> bool:
        return 0 <= x < m and 0 <= y < n

    # 深度优先搜索，path 中记录本次搜索走过的格子
    def dfs(x: int, y: int, px: int, py: int,
            start: Tuple[int, int],
            path: Set[Tuple[int, int]]) -> bool:
        # 把当前格子加入路径
        path.add((x, y))

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not in_grid(nx, ny):
                continue
            if grid[nx][ny] != grid[x][y]:      # 必须是相同字符
                continue
            if (nx, ny) == (px, py):            # 不能回到上一步
                continue

            if (nx, ny) == start and len(path) >= 4:
                # 回到起点且路径长度≥4，找到环
                return True

            if (nx, ny) not in path:
                if dfs(nx, ny, x, y, start, path):
                    return True

        # 回溯：离开 (x, y) 时把它从路径里移除
        path.remove((x, y))
        return False

    # 对每个格子都尝试一次搜索
    for i in range(m):
        for j in range(n):
            if dfs(i, j, -1, -1, (i, j), set()):
                return True
    return False
```

#### 复杂度  

- **时间复杂度**：`O(4^{m*n})`（指数级），因为每一步都有 4 条可能的分支，路径会指数级增长。  
- **空间复杂度**：`O(m*n)`，递归栈和 `path` 集合最坏需要存储整个网格的坐标。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历同一个格子**。如果我们已经从某个格子出发探查过它所在的连通块（即所有能够通过相同字符相互到达的格子），再从这些格子重新开始搜索就是在做无用功。  
我们可以把“是否已经检查过”这件事记下来——**用一个全局的 visited 数组**。这样：

1. 仍然对每个格子遍历一次，但只在它**未被访问**时启动一次 DFS。  
2. DFS 过程同样沿四个方向前进，但我们额外记录**上一格的坐标**（即父节点），用来避免把刚走过的格子当作环的一部分（题目禁止“直接回头”）。  
3. 当在 DFS 中遇到一个已经被 `visited` 标记的格子时，说明我们在当前连通块里找到了环，因为：
   - 该格子已经在本次 DFS 的递归栈之外被访问过，意味着我们从起点出发已经走到它；
   - 再次到达它说明有另一条路径回到同一个格子，且长度一定 ≥ 4（因为 DFS 深度 ≥ 1 且我们不允许直接回头）。  
4. 一旦发现环，立刻返回 `True`。如果所有格子都遍历完仍未发现环，返回 `False`。

> **类比**：把网格看成一个由相同字符组成的“城镇”。我们把每个城镇当作一次探险的“区域”。当我们第一次进入某个城镇时，用 **地图**（`visited`）把已经走过的路标记下来。以后再进入同一个城镇，只要看到已经标记的路，就说明有环路（走了两条不同的路回到同一点）。  

**核心算法**：**深度优先搜索 + 父节点记录**（相当于在有向图里做环检测）。  

**为什么它是最优的**  
- 每个格子只会被访问一次，所有相同字符的连通块只会被遍历一次，时间线性于格子总数 `m*n`。  
- 只使用一个 `visited` 数组和递归栈，空间同样是 `O(m*n)`（递归栈最坏深度为连通块大小）。  

#### 代码（Python）

```python
from typing import List

def containsCycle(grid: List[List[str]]) -> bool:
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def in_grid(x: int, y: int) -> bool:
        return 0 <= x < m and 0 <= y < n

    # 深度优先搜索，(px, py) 是当前格子的父节点坐标
    def dfs(x: int, y: int, px: int, py: int) -> bool:
        visited[x][y] = True
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not in_grid(nx, ny):
                continue
            if grid[nx][ny] != grid[x][y]:   # 必须是相同字符
                continue
            if (nx, ny) == (px, py):
                # 直接回到父节点属于“回头”，不算环
                continue
            if visited[nx][ny]:
                # 已经访问过且不是父节点，说明出现环
                return True
            if dfs(nx, ny, x, y):
                return True
        return False

    # 对每个格子尝试一次 DFS（只在未访问时启动）
    for i in range(m):
        for j in range(n):
            if not visited[i][j]:
                if dfs(i, j, -1, -1):   # (-1,-1) 表示没有父节点
                    return True
    return False
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`。每个格子最多被访问一次，四个方向的检查是常数时间。用大白话说，就是“**和格子数量成正比**”。  
- **空间复杂度**：`O(m * n)`。`visited` 表占用 `m*n` 的布尔空间，递归栈最坏深度也可能是 `m*n`（整块字符相同的情况），所以总空间仍是线性级别。

---

## 心得  

- **核心技巧**：在二维网格中利用 **DFS + 父节点（上一步）** 来避免误判“直接回头”，并结合全局 `visited` 防止重复搜索。  
- **该技巧适用的题型**：  
  1. **环检测**（如本题、LeetCode 1559. Detect Cycles in 2D Grid）。  
  2. **连通块计数**（LeetCode 200. Number of Islands）。  
  3. **寻找特定形状的路径**（如“单词搜索” 79. Word Search）。  
- **一句话总结解题钥匙**：**“只在未访问的连通块里做一次 DFS，遇到已访问且不是父节点的格子就说明环了”。**

---

## 反思  

- **第一反应**：看到“环”和“相同字符”，马上想到 **图的环检测**，把网格抽象成图后用 DFS。  
- **最容易踩的坑**：  
  - 忘记 **排除直接回到父节点**，会把长度为 2 的往返路径误判为环。  
  - 对已经访问过的格子直接返回 `False`，会漏掉环，因为环可能在同一个连通块内部的后续路径中出现。  
  - 边界条件：单行或单列的网格根本不可能形成长度≥4的环，需要提前返回 `False`（但代码里自然会处理）。  
- **下次遇到同类题**：第一步先 **把网格看成图**，确认“相邻且字符相同”是连通条件，然后 **在未访问的连通块里做一次 DFS**，记住父节点即可快速判断环。