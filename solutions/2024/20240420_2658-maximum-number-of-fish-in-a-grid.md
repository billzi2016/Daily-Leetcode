# #2658. 网格中最大鱼的数量 / Maximum Number of Fish in a Grid

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-fish-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D matrix grid of size m x n, where (r, c) represents:
A fisher can start at any water cell (r, c) and can do the following operations any number of times:
Return the maximum number of fish the fisher can catch if he chooses his starting cell optimally, or 0 if no water cell exists.
An adjacent cell of the cell (r, c), is one of the cells (r, c + 1), (r, c - 1), (r + 1, c) or (r - 1, c) if it exists.

**Examples**

**Example 1:**

```
Input: grid = [[0,2,1,0],[4,0,0,3],[1,0,0,4],[0,3,2,0]]
Output: 7
Explanation: The fisher can start at cell (1,3) and collect 3 fish, then move to cell (2,3) and collect 4 fish.
```

**Example 2:**

```
Input: grid = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]]
Output: 1
Explanation: The fisher can start at cells (0,0) or (3,3) and collect a single fish.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- 0 <= grid[i][j] <= 10

---

## 题目（中文翻译）

你被给定一个下标从 **0** 开始的二维矩阵 `grid`，大小为 `m × n`，其中 `grid[r][c]` 表示单元格 `(r, c)` 中的鱼的数量。  
- `grid[r][c] == 0` 表示该单元格是陆地，不能进入。  
- `grid[r][c] > 0` 表示该单元格是水域，且可以捕获对应数量的鱼。

渔夫可以从任意水域单元格 `(r, c)` 开始，并可以任意次数地执行以下操作：

1. **捕获** 当前单元格中的所有鱼（只能捕获一次）。  
2. **移动** 到相邻的水域单元格。相邻单元格指四个方向中的任意一个：`(r, c + 1)`、`(r, c - 1)`、`(r + 1, c)`、`(r - 1, c)`（前提是该单元格存在且为水域）。

渔夫不能重复访问已经捕获过鱼的单元格。

返回渔夫在**最优起始单元格**下能够捕获的**最大鱼的数量**；如果不存在水域单元格，则返回 `0`。

---

### 示例

**示例 1**  
```
输入: grid = [[0,2,1,0],
              [4,0,0,3],
              [1,0,0,4],
              [0,3,2,0]]
输出: 7
解释: 渔夫可以从单元格 (1,3) 开始，捕获 3 条鱼，然后移动到单元格 (2,3) 再捕获 4 条鱼，总计 7 条。
```

**示例 2**  
```
输入: grid = [[1,0,0,0],
              [0,0,0,0],
              [0,0,0,0],
              [0,0,0,1]]
输出: 1
解释: 渔夫可以从单元格 (0,0) 或 (3,3) 开始，只能捕获一条鱼。
```

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 10`
- `0 ≤ grid[i][j] ≤ 10`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题要求在一个 `m × n` 的网格里，找出一块 **相连的水域**（值大于 0 的格子），使得把这块水域里所有格子的鱼加起来的数量最大。  
最直接的想法是：

1. 把每一个有鱼的格子当作 **起点**。  
2. 从这个起点出发，用 **深度优先搜索（DFS）** 把所有可以到达的、同样有鱼的格子遍历一遍，累计它们的鱼数。  
3. 把每一次遍历得到的总鱼数和全局最大值比较，最后得到的就是答案。

> **数据结构类比**：DFS 中用到的 `visited` 集合就像一本“访客登记册”，记录哪些格子已经去过，防止走回头路；栈（递归实现）相当于“探险队的背包”，把待探索的格子压进去，逐个弹出。

为什么这个方法一定对？

- 只要格子之间是上下左右相邻，就可以一步步走过去。DFS 会把 **同一个连通块**（所有相连的有鱼格子）全部遍历完，保证不会漏掉任何一条可能的路径。
- 我们对 **每一个起点** 都做一次完整遍历，必然会覆盖所有连通块。因此最大累计值一定会被找到。

**时间/空间复杂度**（大白话版）  
- 对每个有鱼的格子我们都可能重新跑一次 DFS。最坏情况下网格里每个格子都有鱼（最多 10×10=100），每次 DFS 也会访问最多 100 个格子，所以时间复杂度是 `O(m·n·(m·n))`，即 `O((mn)²)`，这里的 `O` 只是一种“上限”，实际运行会快很多。  
- 递归栈或显式栈最多保存 `mn` 个格子，`visited` 集合同样最多 `mn`，所以空间复杂度是 `O(mn)`。

#### 代码（Python）

```python
from typing import List

def maxFish_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # 四个方向：右、左、下、上
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(r: int, c: int, visited: set) -> int:
        """从 (r,c) 开始，深度优先遍历同一个连通块，返回该块的鱼总数"""
        visited.add((r, c))
        total = grid[r][c]          # 当前格子的鱼

        for dr, dc in dirs:         # 向四个方向尝试移动
            nr, nc = r + dr, c + dc
            # 检查是否在边界内、是否有鱼、且未被访问过
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] > 0 and (nr, nc) not in visited:
                total += dfs(nr, nc, visited)   # 递归累加子块的鱼

        return total

    ans = 0
    # 对每一个可能的起点尝试一次完整的 DFS
    for i in range(m):
        for j in range(n):
            if grid[i][j] > 0:                 # 只有有鱼的格子才可能是起点
                visited = set()
                ans = max(ans, dfs(i, j, visited))

    return ans
```

#### 复杂度

- **时间复杂度**：`O((m·n)²)`  
  解释：最坏情况下我们对每个格子都要遍历整个网格一次，类似“把 100 本书每本都读 100 次”。
- **空间复杂度**：`O(m·n)`  
  解释：递归栈和 `visited` 集合最多保存整个网格的格子数量。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：同一个连通块会被多次重复遍历。比如上图中一个 5 格子组成的块，若我们从块里的每个格子都启动一次 DFS，就会把这 5 格子 **算了 5 次**，浪费了大量时间。

**优化思路**：一次遍历就把每个连通块的鱼总数算出来，并记录下来，后面再遇到同块的格子时直接使用已经得到的结果，避免重复计算。

实现方式有两种，下面选用 **并查集（Union‑Find）**，因为它可以在 **线性时间** 完成：

1. **把每个有鱼的格子视为一个节点**。  
2. 遍历网格，对每个有鱼的格子检查它的 **上方和左方**（只需要检查这两个方向，因为右、下会在以后被检查到），如果相邻格子也有鱼，就把这两个节点 **合并**（union）。  
3. 合并完成后，所有相连的格子会属于同一个 **根节点**（representative）。我们再遍历一次网格，把每个格子的鱼数加到它根节点对应的 **累计和** 中。  
4. 最后遍历所有根节点的累计和，取最大值即为答案。

> **数据结构类比**：并查集像是一张“同学分组表”。最初每个同学（格子）自己一个组，看到两个同学坐在一起就把他们的组 **合并**。`find` 操作就像找 “这个同学现在在哪个大组里”。`union` 就是 “把两个小组合并成一个大组”。  

**为什么正确**：  
- 合并的规则正好对应题目中“相邻的有鱼格子可以相互移动”。因此，同一连通块的所有格子最终会被归到同一个根节点。  
- 把鱼数加到根节点上，就是把整个连通块的鱼数算出来。因为每个格子只会贡献一次鱼数，答案自然是所有块中最大的那一个。

**时间/空间复杂度**（大白话版）  
- 只遍历了 **两次** 网格（一次合并，一次统计），每次都是 `mn` 步，时间复杂度是 `O(m·n)`，相当于“一次性读完所有书”。  
- 并查集需要保存每个格子的父指针和一个额外的 “块的鱼总和” 数组，都是 `mn` 大小，空间复杂度也是 `O(m·n)`。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集实现：支持 find、union 两个基本操作"""
    def __init__(self, size: int):
        self.parent = list(range(size))   # 每个节点的父节点，初始指向自己
        self.rank = [0] * size            # 按秩合并时的高度（可选优化）

    def find(self, x: int) -> int:
        """寻找 x 所在集合的根节点，路径压缩让后续查找更快"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压缩路径
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """把 x、y 两个节点所在的集合合并"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return                       # 已经在同一个集合，不需要再合并
        # 按秩合并：高度低的挂到高度高的下面，保持树的高度尽可能小
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

def maxFish_optimal(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    total_cells = m * n
    uf = UnionFind(total_cells)

    # 方向只检查左、上，防止重复合并
    dirs = [(-1, 0), (0, -1)]

    # 第一次遍历：把相邻的有鱼格子合并到同一个集合
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:          # 没有鱼的格子不参与合并
                continue
            cur_id = r * n + c
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] > 0:
                    neighbor_id = nr * n + nc
                    uf.union(cur_id, neighbor_id)

    # 第二次遍历：统计每个根节点对应的鱼总数
    fish_sum = [0] * total_cells          # fish_sum[root] = 该连通块的鱼数
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:
                continue
            node = r * n + c
            root = uf.find(node)          # 找到所在连通块的根
            fish_sum[root] += grid[r][c]  # 累加鱼数

    # 取最大值，即为答案
    return max(fish_sum) if fish_sum else 0
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  解释：只遍历了两遍网格，每一次都是线性操作。相当于“只读一遍书”，比暴力的“读多遍”快得多。
- **空间复杂度**：`O(m·n)`  
  解释：并查集的父指针、秩数组以及鱼数累计数组都需要和网格同样大小的空间。

---

## 心得

- **核心技巧**：**连通块求和**（使用 DFS/BFS 或并查集）。  
- **适用的题型**：  
  1. “岛屿的最大面积” (Number of Islands, Max Area of Island)  
  2. “最小岛屿的周长” (Island Perimeter)  
  3. “连通分量的最大权值” (Maximum Component Size After Removing One Edge)  
- **一句话总结**：把所有相邻的有价值格子先合并成块，再在块层面做统计，避免重复遍历。

---

## 反思

- **第一反应**：看到“相邻格子可以自由移动”，立刻想到“遍历连通块”。  
- **最容易踩的坑**：  
  - 忘记把 **值为 0** 的格子排除，导致错误地把陆地算进去。  
  - 在 DFS 中没有使用 `visited`，会出现无限递归（死循环）。  
  - 并查集实现时没有路径压缩或按秩合并，会导致时间复杂度退化。  
- **下次类似题的第一步**：先判断“相邻关系”是否构成 **图的连通性**，决定使用 **DFS/BFS** 还是 **并查集** 来一次性统计每个连通块的属性（面积、权值等）。