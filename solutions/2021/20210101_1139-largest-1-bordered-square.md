# #1139. 最大 1 边框正方形 / Largest 1-Bordered Square

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/largest-1-bordered-square/)

---

## 题目（英文原版）

**Description**

Given a 2D grid of 0s and 1s, return the number of elements in the largest square subgrid that has all 1s on its border, or 0 if such a subgrid doesn't exist in the grid.

**Examples**

**Example 1:**

```
Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: 9
```

**Example 2:**

```
Input: grid = [[1,1,0,0]]
Output: 1
```

**Constraints**

- 1 <= grid.length <= 100
- 1 <= grid[0].length <= 100
- grid[i][j] is 0 or 1

---

## 题目（中文翻译）

给定一个由 `0` 和 `1` 构成的二维网格（2D grid），返回具有全部 `1` 边界（border）的最大正方形子网格（subgrid）的元素数量，如果网格中不存在这样的子网格，则返回 `0`。

## 示例

### 示例 1
``` 
Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: 9
```

### 示例 2
``` 
Input: grid = [[1,1,0,0]]
Output: 1
```

## 约束条件

- `1 <= grid.length <= 100`
- `1 <= grid[0].length <= 100`
- `grid[i][j]` 为 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举**所有可能的子正方形，然后检查它的四条边上是否全是 `1`。  

- **枚举子正方形**  
  - 正方形的左上角可以是任意格子 `(i, j)`。  
  - 正方形的边长 `k`（从 `1` 到 `min(m‑i, n‑j)`）决定了右下角的位置。  
- **检查四条边**  
  - 从左上角往右走 `k‑1` 步检查上边；  
  - 从左上角往下走 `k‑1` 步检查左边；  
  - 从右上角往下走 `k‑1` 步检查右边；  
  - 从左下角往右走 `k‑1` 步检查下边。  

> **类比**：把每个正方形想象成一块地，四条边是围墙。我们要把每块地的围墙都检查一遍，确认它们都是“好材料”（即 `1`）。

只要找到一个满足条件的正方形，就记录它的面积 `k*k`，遍历完所有可能后取最大值。如果整个遍历都没有找到符合条件的正方形，答案就是 `0`。

> **为什么正确**：我们穷举了**所有**可能的正方形，且每个正方形的边界检查都是完整的。因此如果答案存在，一定会在枚举过程中被发现。

#### 代码（Python）

```python
from typing import List

def largest1BorderedSquare_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    max_side = 0                     # 记录找到的最大边长

    # 枚举左上角
    for i in range(m):
        for j in range(n):
            # 只要左上角是 1，才可能构成 1‑bordered 正方形
            if grid[i][j] == 0:
                continue
            # 枚举可能的边长（最小为 1，最大不能超出矩阵边界）
            max_len = min(m - i, n - j)
            for k in range(1, max_len + 1):   # k 为边长
                # 检查四条边是否全是 1
                ok = True
                # 上边
                for y in range(j, j + k):
                    if grid[i][y] == 0:
                        ok = False
                        break
                if not ok:
                    continue
                # 下边
                for y in range(j, j + k):
                    if grid[i + k - 1][y] == 0:
                        ok = False
                        break
                if not ok:
                    continue
                # 左边
                for x in range(i, i + k):
                    if grid[x][j] == 0:
                        ok = False
                        break
                if not ok:
                    continue
                # 右边
                for x in range(i, i + k):
                    if grid[x][j + k - 1] == 0:
                        ok = False
                        break

                if ok:                     # 四条边都满足
                    max_side = max(max_side, k)

    return max_side * max_side           # 返回面积
```

#### 复杂度

- **时间复杂度**：`O(m * n * min(m, n)^2)`  
  - 外层两层遍历左上角是 `O(m·n)`。  
  - 对每个左上角，我们尝试所有可能的边长 `k`（最多 `min(m,n)`），每次检查四条边需要 `O(k)`，于是每个左上角的复杂度是 `O(k^2)`，累加后得到 `O(min(m,n)^2)`。  
  - 用大白话讲，就是“先找每块地，再尝试每种可能的大小，再把围墙一格格检查”。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次检查四条边都要逐格遍历”**，这导致时间复杂度出现二次方的 `k`。  
我们可以**预处理**每个格子向左、向上、向右、向下连续的 `1` 的数量，这样在判断某个正方形是否满足 1‑bordered 时，只需要 **O(1)** 的时间即可得到答案。

**核心技巧**：**前缀计数（动态规划）**  
- `left[i][j]`：在位置 `(i, j)` 左侧（包括自身）连续的 `1` 的个数。  
- `up[i][j]`：在位置 `(i, j)` 上方（包括自身）连续的 `1` 的个数。  
- `right[i][j]`：在位置 `(i, j)` 右侧（包括自身）连续的 `1` 的个数。  
- `down[i][j]`：在位置 `(i, j)` 下方（包括自身）连续的 `1` 的个数。

这些表格可以在 **一次遍历**（或两次遍历）中完成：

1. 从左上到右下扫描，得到 `left` 与 `up`。  
2. 从右下到左上扫描，得到 `right` 与 `down`。

得到这四张表后，**判断一个正方形** `(i, j)` 为左上角、边长 `k` 是否是 1‑bordered：

- 上边需要 `left[i][j + k - 1] >= k`（左上角到右上角的连续 1 至少 k）  
- 左边需要 `up[i + k - 1][j] >= k`（左上角到左下角的连续 1 至少 k）  
- 右边需要 `up[i + k - 1][j + k - 1] >= k`  
- 下边需要 `left[i + k - 1][j + k - 1] >= k`

因为每个查询都是 **O(1)**，我们只需要再遍历所有左上角和可能的边长（最多 `min(m,n)`），总时间复杂度变为 **`O(m·n·min(m,n))`**，在最坏情况下仍是 `O(N^3)`（这里 `N` 代表矩阵的最大维度），但因为每次检查是常数时间，实际运行会快很多。进一步的优化是从大到小枚举边长，一旦找到合法正方形即可返回。

> **类比**：想象我们在每块地的每个角落都提前贴了一张“这条线往左/往上/往右/往下还能走多少格都是好材料”的标记。以后只要看标记，就能立刻知道围墙是否完整，而不必一步步去检查。

#### 代码（Python）

```python
from typing import List

def largest1BorderedSquare(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # 四个 DP 表，分别记录向左、向上、向右、向下的连续 1 的长度
    left = [[0] * n for _ in range(m)]
    up   = [[0] * n for _ in range(m)]
    right = [[0] * n for _ in range(m)]
    down  = [[0] * n for _ in range(m)]

    # 1) 从左上到右下，填 left 与 up
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                left[i][j] = (left[i][j-1] + 1) if j > 0 else 1
                up[i][j]   = (up[i-1][j] + 1)   if i > 0 else 1
            # else 默认 0

    # 2) 从右下到左上，填 right 与 down
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            if grid[i][j] == 1:
                right[i][j] = (right[i][j+1] + 1) if j < n-1 else 1
                down[i][j]  = (down[i+1][j] + 1)   if i < m-1 else 1

    max_side = 0                     # 记录找到的最大边长

    # 3) 枚举左上角 (i, j) 与可能的边长 k（从大到小加速）
    for i in range(m):
        for j in range(n):
            # 当前格子必须是 1，才可能是左上角
            if grid[i][j] == 0:
                continue
            # 可能的最大边长受四个方向的限制
            possible = min(left[i][j], up[i][j])
            # 从可能的最大边长往下尝试
            for k in range(possible, 0, -1):
                # 右下角坐标
                x, y = i + k - 1, j + k - 1
                if x >= m or y >= n:
                    continue
                # 检查四条边是否都有足够的连续 1
                if (right[i][y] >= k and    # 上边右端往右
                    down[x][j] >= k and      # 左边下端往下
                    right[x][y] >= k and    # 下边右端往右
                    down[x][y] >= k):       # 右边下端往下
                    max_side = max(max_side, k)
                    break   # 已经是当前左上角能得到的最大 k，停止内层循环

    return max_side * max_side           # 返回面积
```

#### 复杂度

- **时间复杂度**：`O(m·n·min(m,n))`  
  - 预处理四张表各需一次完整遍历，`O(m·n)`。  
  - 主循环对每个格子最多尝试 `min(m,n)` 次（从大到小枚举边长），每次判断四条边是 **O(1)**，所以整体是 `O(m·n·min(m,n))`。  
  - 用大白话说，就是“先把每块地四面墙的‘还能走多远’标记好”，随后只需“看标记”就能快速判断是否合格。
- **空间复杂度**：`O(m·n)`  
  - 四张 DP 表各占 `m·n` 的空间，总共四倍常数因子，仍属于线性空间。

---

## 心得

- **核心技巧**：利用动态规划（前缀计数）把“检查一条边上是否全是 1”从 `O(k)` 降到 `O(1)`，从而把整体复杂度从 `O(m·n·k^2)` 降到 `O(m·n·k)`。
- **适用的题型**  
  1. **最大正方形/矩形的边界满足特定条件**（如 1277. Count Square Submatrices With All Ones）。  
  2. **在矩阵中寻找满足连续 1 条件的子结构**（如 85. Maximal Rectangle、1727. Largest Submatrix With Rearrangements）。  
  3. **需要快速判断某条直线段是否全部为 1** 的问题（如 1504. Count Submatrices With All Ones）。
- **一句话总结**：**把每个格子向四个方向的“连续 1 长度”预先算好，后面只要看表格就能瞬间判断正方形的边界是否完整**。

---

## 反思

- **第一反应**：直接枚举所有正方形并逐格检查四条边——最朴素也最容易想到的办法。
- **最容易踩的坑**  
  - **边界条件**：正方形的右下角可能超出矩阵，需要提前判断 `i + k - 1 < m`、`j + k - 1 < n`。  
  - **单元格为 0** 时直接跳过，以免浪费不必要的检查。  
  - **预处理表的初始化**：边缘格子没有左/上/右/下邻居时要特别处理，否则会出现索引错误。
- **下次遇到同类题**：第一步想到 **“把需要重复查询的信息提前算好（前缀计数 / 前缀和）”**，再在此基础上进行枚举或滑动窗口。这样可以把重复的线性扫描一次性消除，显著提升效率。