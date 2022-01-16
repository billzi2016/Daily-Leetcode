# #1631. 最小努力路径 / Path With Minimum Effort

> 难度：中等 · 标签：Array、Binary Search、Depth-First Search、Breadth-First Search、Union Find、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/path-with-minimum-effort/)

---

## 题目（英文原版）

**Description**

You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.
A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.
Return the minimum effort required to travel from the top-left cell to the bottom-right cell.

**Examples**

**Example 1:**

```
Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
Output: 2
Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
```

**Example 2:**

```
Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
Output: 1
Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
```

**Example 3:**

```
Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
Output: 0
Explanation: This route does not require any effort.
```

**Constraints**

- rows == heights.length
- columns == heights[i].length
- 1 <= rows, columns <= 100
- 1 <= heights[i][j] <= 106

---

## 题目（中文翻译）

**题目描述**  
你是一名准备远足的徒步者。给定 `heights`，一个大小为 `rows x columns` 的二维数组（2D array），其中 `heights[row][col]` 表示单元格 `(row, col)` 的高度。你位于左上角单元格 `(0, 0)`，希望走到右下角单元格 `(rows‑1, columns‑1)`（即 0 索引）。每一步可以向上、下、左、右四个方向移动，目标是找到一条**最小努力**（minimum effort）的路径。

路径的**努力**定义为路径上任意相邻两个单元格高度差的绝对值的**最大值**。返回从左上角走到右下角所需的最小努力。

**示例**

*示例 1*  
```
输入: heights = [[1,2,2],[3,8,2],[5,3,5]]
输出: 2
解释: 路径 [1,3,5,3,5] 的相邻单元格高度差最大为 2，这是比路径 [1,2,2,2,5]（最大差为 3）更优的选择。
```

*示例 2*  
```
输入: heights = [[1,2,3],[3,8,4],[5,3,5]]
输出: 1
解释: 路径 [1,2,3,4,5] 的相邻单元格高度差最大为 1，优于路径 [1,3,5,3,5]。
```

*示例 3*  
```
输入: heights = [[1,2,1,1,1],
                 [1,2,1,2,1],
                 [1,2,1,2,1],
                 [1,2,1,2,1],
                 [1,1,1,2,1]]
输出: 0
解释: 这条路径不需要任何努力（所有相邻高度差均为 0）。
```

**约束条件**
- `rows == heights.length`
- `columns == heights[i].length`
- `1 <= rows, columns <= 100`
- `1 <= heights[i][j] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把整个网格想象成一张 **城市地图**，每个格子是一个城市，相邻的城市之间有一条道路，走这条路的「费用」就是两格子高度差的绝对值。  
我们要从左上角走到右下角，**路径的努力值** 等于这条路上所有费用的最大值。  

最直接的想法是：**把所有可能的走法都枚举一遍**，把每条路径的最大费用算出来，最后取最小的那个。  

- **用到的数据结构**：递归（或显式的栈）实现深度优先搜索（DFS），记录已经走过的格子避免原路返回（相当于在地图上画了「走过的痕迹」）。
- **为什么正确**：DFS 会遍历 **所有** 从起点到终点的合法路径，比较它们的最大费用，自然能找到最小的那个。

> 生活类比：想象你在迷宫里，每走一步都要记录下这一步的难度（高度差），等走到出口后，回头看看这条路上最难的那一步有多难。把所有可能的走法都试一遍，挑出最容易的那条路。

#### 代码（Python）

```python
from typing import List

def minimumEffortPath_bruteforce(heights: List[List[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    # 四个方向：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 用 visited 记录已经走过的格子，防止原路返回形成环
    visited = [[False] * cols for _ in range(rows)]
    ans = float('inf')                 # 当前找到的最小努力值

    def dfs(r: int, c: int, cur_max: int) -> None:
        """
        r, c   : 当前所在的格子坐标
        cur_max: 从起点走到这里为止的最大高度差
        """
        nonlocal ans
        # 到达右下角，更新答案
        if r == rows - 1 and c == cols - 1:
            ans = min(ans, cur_max)
            return

        # 剪枝：如果当前的最大差已经不可能比答案更好，就直接返回
        if cur_max >= ans:
            return

        visited[r][c] = True
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            # 检查是否在网格内部且未访问过
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                # 计算这一步的费用（高度差）
                diff = abs(heights[nr][nc] - heights[r][c])
                dfs(nr, nc, max(cur_max, diff))
        visited[r][c] = False   # 回溯，撤销访问标记

    dfs(0, 0, 0)
    return ans
```

> 关键行中文注释已写在代码里，直接复制运行即可（只适合非常小的矩阵，实际会超时）。

#### 复杂度

- **时间复杂度**：`O(4^{rows*cols})`（指数级）  
  解释：每一步最多有 4 条可选方向，最坏情况下会尝试所有可能的走法，类似于在每个格子上都有 4 条分支，整个搜索树的大小是 4 的 **行×列** 次方，远远超过实际可接受的范围。
- **空间复杂度**：`O(rows*cols)`  
  解释：递归栈深度最多等于格子数，加上 `visited` 数组，需要与网格大小相同的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **遍历所有路径**。  
观察题目可以把每条相邻格子之间的高度差看成 **边的权重**，于是整个网格就是一个带权无向图。我们要求的是从起点到终点的路径，使得路径上 **最大的边权** 最小。

这类「最小化最大值」的问题有一个常用技巧：**二分答案 + 可行性判定**。  
思路如下：

1. **设定一个阈值 `k`**（代表我们容忍的最大努力值）。  
2. **只允许走「费用 ≤ k」的边**，也就是说只在高度差不大于 `k` 的相邻格子之间移动。  
3. 在这种限制下，判断能否从左上角走到右下角。  
   - 这一步可以用 **DFS/BFS**（或者并查集）在 O(rows·cols) 时间完成。  
4. 如果能走通，说明答案 ≤ `k`；否则答案 > `k`。  
5. 对 `k` 进行 **二分搜索**，在 `[0, maxDiff]` 区间内不断收敛，最终得到最小可行的 `k`。

> 类比：想象你在爬山，手里只有一双只能承受 `k` 高度差的鞋子。先假设鞋子能承受的最大高度差是 10，看看能不能走到山顶；如果能，就把鞋子再做得更「软」点（把 `k` 缩小），如果不能，就把鞋子做得更「硬」点（把 `k` 放大）。不断二分，最后找到恰好能让你到达山顶的最小 `k`。

**为什么二分能工作**  
- 当阈值 `k` 足够大时（比如 `10^6`），所有边都可用，显然能走通。  
- 当阈值 `k` 为 0 时，只能走高度完全相同的格子，可能走不通。  
- 随着 `k` 单调增大，可行性只能从「不可」变为「可」，不会再变回「不可」——这正好满足二分的单调性前提。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minimumEffortPath(heights: List[List[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    # 四个方向
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # ---------- 判定函数：在阈值 limit 下是否可达 ----------
    def can_reach(limit: int) -> bool:
        """只走高度差 ≤ limit 的边，判断是否能从 (0,0) 到达 (rows-1, cols-1)。"""
        visited = [[False] * cols for _ in range(rows)]
        q = deque()
        q.append((0, 0))
        visited[0][0] = True

        while q:
            r, c = q.popleft()
            if r == rows - 1 and c == cols - 1:      # 已到终点
                return True
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                    # 计算这一步的高度差
                    diff = abs(heights[nr][nc] - heights[r][c])
                    if diff <= limit:               # 只在阈值内的边才加入队列
                        visited[nr][nc] = True
                        q.append((nr, nc))
        return False

    # ---------- 二分搜索 ----------
    # 最大可能的高度差是整个矩阵中任意相邻格子差的上限，取 10^6 足够大
    lo, hi = 0, 10**6
    answer = hi
    while lo <= hi:
        mid = (lo + hi) // 2               # 试探的阈值
        if can_reach(mid):                 # 能走通，说明答案 ≤ mid
            answer = mid
            hi = mid - 1                   # 往更小的区间搜
        else:                              # 走不通，答案 > mid
            lo = mid + 1
    return answer
```

> 代码解释：
- `can_reach` 用 **BFS**（广度优先搜索）在阈值 `limit` 下遍历所有可达格子，时间 O(rows·cols)。
- 二分循环最多执行 `log2(10^6) ≈ 20` 次，每次调用 `can_reach`，整体时间 O(20·rows·cols) ≈ O(rows·cols·log(maxHeight))。

#### 复杂度

- **时间复杂度**：`O((rows·cols) * log(maxHeightDiff))`  
  - 解释：每次二分检查都要遍历整个网格一次（BFS），二分的次数约为 `log₂(10⁶) ≈ 20`，所以整体是「网格大小」乘以「对数」的量级。相较于暴力的指数级，这已经是可以接受的。
- **空间复杂度**：`O(rows·cols)`  
  - 解释：BFS 需要一个 `visited` 矩阵和队列，最坏情况下会把所有格子都放进去，空间正比于网格的大小。

---

## 心得

- **核心技巧**：**二分答案 + 单次可达性判定**（这里用 BFS）。  
  这是一种常见的「最小化最大值」思路，适用于所有“在阈值限制下能否连通”的问题。

- **该技巧适用的题型**  
  1. **Path With Minimum Effort**（本题）  
  2. **Minimum Maximum Distance to Reach All Buildings**（在阈值下检查所有建筑是否可达）  
  3. **Binary Search on Answer** 系列题目，如 “Kth Smallest Number in Multiplication Table” 中的“在阈值下计数”思路。

- **一句话总结解题钥匙**：  
  *把“求最小最大值”转化为“在给定上限下能否到达”，再用二分快速定位最小可行上限。*

---

## 反思

- **第一反应**：看到“最大绝对差的最小化”，立刻想到 **最短路径**，但普通的 Dijkstra 求的是路径长度之和，而这里要求的是路径上 **单条边的最大权重**，于是想到 **最小化最大边** 的二分技巧。
- **最容易踩的坑**  
  - **阈值上下界**：上界不能直接取 `max(heights)`，而应取可能的最大差值（`10⁶` 或实际相邻格子差的最大值），否则二分可能不收敛。  
  - **判定函数的漏写**：忘记在 BFS 中判断 `diff <= limit`，导致所有边都被走通，二分永远返回 0。  
  - **边界条件**：单行或单列的矩阵，仍然要能正常返回 0（因为起点即终点或只有唯一路径）。
- **下次遇到同类题**，第一步应该：  
  *先思考能否把“最大/最小”约束转化为“阈值可行性”，如果可以，就立刻写出二分 + 检查（DFS/BFS/Union‑Find）框架。*