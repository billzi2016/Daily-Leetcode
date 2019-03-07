# #329. **矩阵中的最长递增路径** / Longest Increasing Path in a Matrix

> 难度：困难 · 标签：Array、Dynamic Programming、Depth-First Search、Breadth-First Search、Graph、Topological Sort、Memoization、Matrix · [LeetCode 链接](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

---

## 题目（英文原版）

**Description**

Given an m x n integers matrix, return the length of the longest increasing path in matrix.
From each cell, you can either move in four directions: left, right, up, or down. You may not move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

**Examples**

**Example 1:**

```
Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
Output: 4
Explanation: The longest increasing path is [1, 2, 6, 9].
```

**Example 2:**

```
Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
Output: 4
Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.
```

**Example 3:**

```
Input: matrix = [[1]]
Output: 1
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- 0 <= matrix[i][j] <= 231 - 1

---

## 题目（中文翻译）

给定一个 *m* × *n* 的整数矩阵，返回矩阵中最长递增路径的长度。

从每个单元格出发，你只能向四个方向移动：左、右、上、下。不能对角移动，也不能移出矩阵边界（即不允许环绕）。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- *m* == matrix.length  
- *n* == matrix[i].length  
- 1 ≤ *m*, *n* ≤ 200  
- 0 ≤ matrix[i][j] ≤ 2³¹ - 1  

**示例**

**示例 1**  
``` 
Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
Output: 4
Explanation: 最长递增路径为 [1, 2, 6, 9]。
```

**示例 2**  
``` 
Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
Output: 4
Explanation: 最长递增路径为 [3, 4, 5, 6]。不允许对角移动。
```

**示例 3**  
``` 
Input: matrix = [[1]]
Output: 1
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个格子当作起点，穷举所有可能的走法**，找出最长的递增路径。  
可以把矩阵想象成一张城市地图，每个格子是一个交叉口，四条路（上下左右）可以通向相邻的交叉口。  
从起点出发，只要相邻格子的数值更大，就可以沿着这条路继续前进。于是我们可以用**深度优先搜索（DFS）**把所有合法的走法全部列举出来，记录走到的格子数目，最后取最大值。

为什么会对？  
- 递增路径的定义非常明确：相邻格子数值严格增大。只要我们在搜索时遵守这个规则，就一定遍历到所有合法路径。  
- 暴力搜索没有剪枝，只要把**“向四个方向继续走”**这件事写成递归函数，就能把所有可能的走法都尝试一遍。

#### 代码（Python）

```python
from typing import List

def longestIncreasingPath_bruteforce(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    m, n = len(matrix), len(matrix[0])
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]   # 四个方向：下、上、右、左

    # 递归搜索，从 (x, y) 开始的最长递增路径长度
    def dfs(x: int, y: int) -> int:
        best = 1                     # 至少包含自己这一个格子
        for dx, dy in dirs:         # 尝试四个方向
            nx, ny = x + dx, y + dy
            # 边界检查 + 必须递增
            if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] > matrix[x][y]:
                length = 1 + dfs(nx, ny)   # 走到下一个格子后继续搜索
                best = max(best, length)   # 取最大长度
        return best

    ans = 0
    for i in range(m):
        for j in range(n):
            ans = max(ans, dfs(i, j))   # 每个格子都当作起点
    return ans
```

> **注意**：这里的 `dfs` 没有任何记忆化（缓存）手段，每次从同一个格子出发都会重新计算所有后续路径，导致大量重复工作。

#### 复杂度  

- **时间复杂度**：`O(4^{m*n})`（理论上每一步都有最多 4 种选择，路径长度最坏可以遍历所有格子），实际会更小一点，但仍然是指数级的，几乎不可接受。  
  - 大白话：如果矩阵是 5×5，搜索的次数会像把 25 块积木每块都随意搭起来一样，几乎要尝遍所有可能的搭法，时间会爆炸。
- **空间复杂度**：`O(m*n)` 用于递归栈的最深层（最坏情况下递归深度等于格子总数），另外还有常数级的临时变量。

> 结论：暴力解思路清晰，但在 200×200 的最大输入时根本跑不完，需要优化。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **大量的重复计算** 是性能瓶颈：  
- 当我们从格子 `A` 走到格子 `B`，再继续往下搜索时，`B` 的后续最长递增路径会被计算很多次。  
- 这正好符合**动态规划（DP）**的思想：把子问题的答案保存下来，下次需要时直接取，用**记忆化搜索（Memoization）**把递归转成“查表”。

把矩阵看成**有向无环图（DAG）**也很有帮助：  
- 每个格子是一个节点。  
- 若相邻格子 `grid[x][y] < grid[nx][ny]`，就从 `grid[x][y]` 指向 `grid[nx][ny]`（因为只能向更大的数走）。  
- 由于数值严格递增，这张图不可能出现环路（环路意味着数值既增又减，矛盾），所以是 DAG。  

在 DAG 上求最长路径的常用方法有两种：

1. **拓扑排序 + 动态规划**（从小到大逐层扩展）。  
2. **DFS + 记忆化**（自底向上递归，缓存每个节点的最长路径长度）。

对初学者来说，**DFS + 记忆化**更直观，只需要在递归函数里加一个 `memo` 表格记录已经算好的结果。下面一步步解释实现细节：

1. **准备工作**  
   - 记录矩阵大小 `m, n`。  
   - 创建同尺寸的二维数组 `memo`，初始化为 0，表示“未计算”。  
   - 定义四个方向的偏移量 `dirs`，方便遍历相邻格子。

2. **DFS 带记忆化**  
   - `dfs(i, j)` 返回 **从 (i, j) 出发的最长递增路径长度**。  
   - 若 `memo[i][j] != 0`，说明已经算过，直接返回缓存值。  
   - 否则遍历四个方向，如果相邻格子数值更大，就递归调用 `dfs`，取所有合法方向的最大值 `max_len`。  
   - 最终 `memo[i][j] = 1 + max_len`（加上自己这一步），返回该值。

3. **遍历所有起点**  
   - 对每个格子调用一次 `dfs(i, j)`，并在过程中不断更新全局最大值 `ans`。  
   - 由于每个格子只会被计算一次（后续直接命中缓存），总时间是线性的。

4. **为什么不需要 visited 标记**  
   - 递增路径保证了数值严格上升，不能回到已经访问过的格子形成环路，所以不需要额外的“已访问”数组来防止死循环。

> **类比**：记忆化就像在做一道数学题时把已经算好的子式写在草稿纸上，后面再需要时直接抄下来，不必重新推导。

#### 代码（Python）

```python
from typing import List

def longestIncreasingPath(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    m, n = len(matrix), len(matrix[0])
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]   # 四个方向
    memo = [[0] * n for _ in range(m)]      # 记忆化表，0 表示“未计算”

    # 带记忆化的深度优先搜索
    def dfs(x: int, y: int) -> int:
        if memo[x][y] != 0:                 # 已经算过，直接返回
            return memo[x][y]

        best = 1                            # 至少包含自己
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 必须在矩阵内部且数值严格递增
            if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] > matrix[x][y]:
                length = 1 + dfs(nx, ny)   # 递归求后续最长路径
                best = max(best, length)   # 取最大

        memo[x][y] = best                    # 把结果写进记忆化表
        return best

    ans = 0
    for i in range(m):
        for j in range(n):
            ans = max(ans, dfs(i, j))        # 每个格子都尝试一次

    return ans
```

> 关键行中文注释已经写在代码里，复制后即可直接运行。

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 每个格子最多被 `dfs` 调用一次，调用内部只检查四个方向，整体是线性时间。  
  - 与暴力解的指数级时间形成鲜明对比：现在即使是 200×200（40,000）个格子也能在毫秒级完成。

- **空间复杂度**：`O(m * n)`  
  - `memo` 表占用 `m*n` 的空间。  
  - 递归栈的深度最坏为最长路径长度，最长不超过 `m*n`，所以整体仍是 `O(m*n)`。  
  - 大白话：我们用了一张和矩阵同等大小的“备忘录”来记住每个格子的答案，额外的空间和矩阵本身大小成正比。

---

## 心得

- **核心技巧**：**DFS + 记忆化（自底向上动态规划）**，把“每个格子向更大格子走”的问题抽象成有向无环图的最长路径。
- **适用的题型**  
  1. 矩阵/网格中的“最长/最短递增（或递减）路径”。  
  2. 任何可以建成 DAG 的问题，例如“单词接龙最长链”“课程表中的最长学习路径”。  
  3. 带约束的递归搜索，子问题会被多次重复求解的情形（如“岛屿最大面积”“山脉路径”等）。
- **一句话总结**：**把递归的子问题结果缓存下来，后面直接查表，时间立马从指数级降到线性。**

---

## 反思

- **第一反应**：直接写一个四方向的 DFS，遍历所有可能的走法，期待能跑通。  
- **最容易踩的坑**  
  1. **忘记记忆化**：导致时间爆炸。  
  2. **边界检查写错**：尤其是 `0 <= nx < m` 与 `0 <= ny < n` 的顺序容易写反。  
  3. **递增条件写成 `>=`**：会产生错误的环路，导致无限递归或错误的路径长度。  
  4. **递归深度过大导致栈溢出**：在 Python 中可以适当提升递归深度或改用显式栈（迭代）实现。  
- **下次遇到同类题**：第一步先**思考是否存在子问题的重叠**（即“同一个格子从不同方向会得到相同的后续路径”），如果有，立刻考虑**记忆化或拓扑排序**来消除重复计算。这样可以把“看起来很慢”的暴力搜索，迅速转化为高效的 DP 解。