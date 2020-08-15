# #959. **斜线划分的区域** / Regions Cut By Slashes

> 难度：中等 · 标签：Array、Hash Table、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/regions-cut-by-slashes/)

---

## 题目（英文原版）

**Description**

An n x n grid is composed of 1 x 1 squares where each 1 x 1 square consists of a '/', '\', or blank space ' '. These characters divide the square into contiguous regions.
Given the grid grid represented as a string array, return the number of regions.
Note that backslash characters are escaped, so a '\' is represented as '\\'.

**Examples**

**Example 1:**

```
Input: grid = [" /","/ "]
Output: 2
```

**Example 2:**

```
Input: grid = [" /","  "]
Output: 1
```

**Example 3:**

```
Input: grid = ["/\\","\\/"]
Output: 5
Explanation: Recall that because \ characters are escaped, "\\/" refers to \/, and "/\\" refers to /\.
```

**Constraints**

- n == grid.length == grid[i].length
- 1 <= n <= 30
- grid[i][j] is either '/', '\', or ' '.

---

## 题目（中文翻译）

一个 **n × n** 的网格（grid）由若干 **1 × 1** 的小格子组成，每个小格子内部可能包含字符 `'/'`、`'\'`（在字符串中写作 `'\\'`）或空格 `' '`。这些字符会把所在的小格子划分成若干连续的区域。

给定一个由字符串组成的数组 `grid`，返回整个网格被划分后形成的区域总数。

> 注意：反斜杠字符在字符串里需要转义，因此 `'\ '` 实际表示字符 `'\'`，写法为 `'\\'`。

**示例**

- 示例 1  
  **输入**：`grid = [" /","/ "]`  
  **输出**：`2`

- 示例 2  
  **输入**：`grid = [" /","  "]`  
  **输出**：`1`

- 示例 3  
  **输入**：`grid = ["/\\","\\/"]`  
  **输出**：`5`  
  **解释**：由于 `\` 在字符串中被转义，`"\\/"` 实际表示 `\/`，`"/\\"` 实际表示 `/\`，由此产生了 5 个独立的区域。

**约束条件**

- `n == grid.length == grid[i].length`
- `1 ≤ n ≤ 30`
- `grid[i][j]` 只能是 `'/'`、`'\'`（写作 `'\\'`）或空格 `' '`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每个 1×1 的小格子 **放大** 成 3×3 的像素格子。  

- 原本的 `' '`（空格）相当于 3×3 全部是空白，什么也不划分。  
- `'/'` 把左下到右上这条对角线涂黑（把对应的三个像素设为 1），其余像素保持空白。  
- `'\'` 把左上到右下这条对角线涂黑（把对应的三个像素设为 1），其余像素保持空白。  

把所有小格子都这样展开后，整个图变成了 `3n × 3n` 的大矩阵，黑色像素代表“墙”，白色像素代表可以通行的区域。  
此时，求 **连通块**（即相邻的白色像素组成的区域）的数量，就是原题要求的“区域数”。  

这一步可以用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 来遍历所有白色像素，遇到未访问的白色像素就开启一次搜索，计数器 +1。  

> **类比**：把地图放大后，黑线就像河流，白地就是陆地。数一下有多少块陆地，就是答案。

**为什么正确**  
因为我们把每条斜线都精确地用像素“墙”表示了，且放大后的像素之间的相邻关系（上下左右）恰好对应原图中不被斜线阻隔的连通性。于是连通块的数量等价于原题的区域数。

**复杂度分析（大白话）**  
- **时间**：我们遍历 `3n × 3n` 的每个像素一次，最多做一次 DFS/BFS，时间是 `O((3n)²) = O(n²)`（常数 9 可以不计）。  
- **空间**：需要存放放大后的矩阵以及访问标记，大小也是 `O((3n)²) = O(n²)`。  

#### 代码（Python）  

```python
from collections import deque

def regionsBySlashes(grid):
    n = len(grid)
    # 把每个格子放大成 3x3，初始化为全 0（白色）
    N = n * 3
    board = [[0] * N for _ in range(N)]

    # 根据字符在对应的 3x3 小块里填上 “墙”(1)
    for i in range(n):
        for j in range(n):
            ch = grid[i][j]
            r, c = i * 3, j * 3          # 该格子左上角在放大矩阵中的坐标
            if ch == '/':
                board[r + 0][c + 2] = 1  # /
                board[r + 1][c + 1] = 1
                board[r + 2][c + 0] = 1
            elif ch == '\\':            # 注意这里是转义的反斜杠
                board[r + 0][c + 0] = 1  # \
                board[r + 1][c + 1] = 1
                board[r + 2][c + 2] = 1

    # 四个方向：上、下、左、右
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    def bfs(sr, sc):
        """从 (sr,sc) 出发，用 BFS 把同一个连通块的白色像素全部标记为已访问"""
        q = deque()
        q.append((sr, sc))
        board[sr][sc] = 1               # 把白色改为 1，防止重复访问
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # 越界或已经是墙/已访问的直接跳过
                if 0 <= nr < N and 0 <= nc < N and board[nr][nc] == 0:
                    board[nr][nc] = 1   # 标记为已访问
                    q.append((nr, nc))

    regions = 0
    # 遍历整个放大矩阵，找到每个未访问的白色像素，开启一次 BFS
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:        # 仍是白色，说明发现了新区域
                bfs(i, j)
                regions += 1
    return regions
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：虽然我们遍历的是 `3n × 3n` 的矩阵，但常数 9 对大 O 记号没有影响。每个像素最多被访问一次。  

- **空间复杂度**：`O(n²)`  
  解释：需要保存放大后的矩阵（`3n × 3n`）以及 BFS 队列，整体仍是二次级别的空间。  



---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **把每个格子放大 3 倍**，导致空间占用和遍历次数都被放大了 9 倍。  
其实我们并不需要把格子真的放大，只要能够**描述格子内部的连通关系**即可。  

**核心思想**：把每个 1×1 的格子再细分成 **4 个小三角形**（编号 0、1、2、3），如下图所示  

```
   0
 +---+---+   0: 左上三角
 | \ | / |
 +---+---+   1: 右上三角
 | / | \ |
 +---+---+   2: 左下三角
 |   |   |
 +---+---+   3: 右下三角
```

- 若格子里是 `' '`（空格），四个三角形之间都是相通的，直接合并成同一个集合。  
- 若格子里是 `'/'`，则 **0 与 1**、**2 与 3** 被墙隔开（不相通），而 **0 与 3**、**1 与 2** 仍然相通。  
- 若格子里是 `'\'`，则 **0 与 2**、**1 与 3** 被墙隔开，**0 与 1**、**2 与 3** 仍然相通。  

接下来要做的就是 **把相邻格子之间的对应三角形也合并**（因为它们共享一条边）。  
- 上下相邻：当前格子的 **2** 与下方格子的 **0** 合并。  
- 左右相邻：当前格子的 **1** 与右方格子的 **3** 合并。  

所有合并操作完成后，**不同集合的数量** 就是图中不相连的区域数。  

这正好可以用 **并查集（Union‑Find / Disjoint Set Union, DSU）** 来实现。  

并查集的两大操作：  

1. **find(x)**：找出元素 `x` 所在集合的“根”。  
2. **union(x, y)**：把 `x`、`y` 所在的集合合并（根相同即表示已经连通）。  

通过路径压缩和按秩合并，整个过程的时间几乎是 **线性** 的 `O(N)`（这里的 N = 4·n²）。  

> **类比**：把每个小三角形想象成城市的一个小区，斜线就是城墙，城墙把某些小区隔开。并查集帮我们快速判断哪些小区已经在同一个“大城市”里，合并时就像修桥把两个小区连通。  

#### 代码（Python）  

```python
class DSU:
    """并查集实现，带路径压缩和按秩合并"""
    def __init__(self, n):
        self.parent = list(range(n))   # 每个节点起初自己是根
        self.rank   = [0] * n          # 用于按秩（深度）合并

    def find(self, x):
        # 递归寻找根，同时把路径压平，加速后续查询
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # 合并两棵树，返回 True 表示成功合并（即原本不在同一集合）
        fx, fy = self.find(x), self.find(y)
        if fx == fy:
            return False
        # 按秩合并，保证树的深度尽量小
        if self.rank[fx] < self.rank[fy]:
            fx, fy = fy, fx
        self.parent[fy] = fx
        if self.rank[fx] == self.rank[fy]:
            self.rank[fx] += 1
        return True


def regionsBySlashes_opt(grid):
    n = len(grid)
    # 每个格子拆成 4 块，总数 = 4 * n * n
    dsu = DSU(4 * n * n)

    for i in range(n):
        for j in range(n):
            # 当前格子在并查集里的编号基址
            idx = (i * n + j) * 4
            c = grid[i][j]

            # 1️⃣ 同格子内部的连通关系
            if c == ' ':
                # 四块全部相连
                dsu.union(idx + 0, idx + 1)
                dsu.union(idx + 1, idx + 2)
                dsu.union(idx + 2, idx + 3)
            elif c == '/':
                # 0 与 3 相连，1 与 2 相连
                dsu.union(idx + 0, idx + 3)
                dsu.union(idx + 1, idx + 2)
            else:  # c == '\\'
                # 0 与 1 相连，2 与 3 相连
                dsu.union(idx + 0, idx + 1)
                dsu.union(idx + 2, idx + 3)

            # 2️⃣ 与相邻格子的连通关系（只需要向下、向右检查，避免重复）
            # 与下方格子相连：当前格子的 2 与下方格子的 0
            if i + 1 < n:
                down_idx = ((i + 1) * n + j) * 4
                dsu.union(idx + 2, down_idx + 0)

            # 与右侧格子相连：当前格子的 1 与右侧格子的 3
            if j + 1 < n:
                right_idx = (i * n + (j + 1)) * 4
                dsu.union(idx + 1, right_idx + 3)

    # 最终有多少不同的根，就有多少独立的区域
    regions = sum(1 for i in range(4 * n * n) if dsu.find(i) == i)
    return regions
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：我们遍历每个格子一次，进行常数次 `union`/`find`，每次操作几乎是 `α(N)`（反阿克曼函数），在实际中可以视为常数。因此整体是二次级别的线性时间。  

- **空间复杂度**：`O(n²)`  
  解释：并查集需要保存 `4·n²` 个父指针和秩数组，都是与格子数量同阶的线性空间。相比暴力的 `9·n²` 像素矩阵，常数更小。  



---  

## 心得  

- **核心技巧**：把每个格子拆分成固定的子单元（4 个三角形）并利用 **并查集** 合并连通关系，进而把“平面划分”转化为“集合计数”。  
- **适用场景**：  
  1. **岛屿计数**（Number of Islands）——把陆地格子合并后统计连通块。  
  2. **连通分量**（Friend Circles、Surrounded Regions）——同样使用并查集或 DFS 合并。  
  3. **网格划分**（Stone Game VI 中的区域划分、LeetCode 959）——需要把格子内部进一步拆分再合并。  
- **一句话总结解题钥匙**：**把复杂的几何划分抽象为离散的“子块”并用并查集合并相邻子块，最后统计不同根的数量**。  



---  

## 反思  

- **第一反应**：看到斜线把格子切成不规则形状，第一时间想到把格子放大成像素网格，再用 BFS/DFS 直接计数。  
- **最容易踩的坑**：  
  - **字符转义**：题目里 `'\'` 用 `\\` 表示，写代码时一定要记得 `if c == '\\'`。  
  - **相邻合并的方向**：只向下、向右合并即可，若双向合并会导致重复 union，影响效率。  
  - **并查集的路径压缩**：不写会导致时间复杂度退化到近 `O(n³)`（在 Python 里会超时）。  
- **下次类似题的第一步**：先思考能否把“连续空间”离散化为若干**固定小单元**，并判断这些小单元之间的**相邻关系**，再决定使用 DFS/BFS 还是并查集来计数连通块。