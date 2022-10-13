# #1970. **最后一天仍能穿越** / Last Day Where You Can Still Cross

> 难度：困难 · 标签：Array、Binary Search、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/last-day-where-you-can-still-cross/)

---

## 题目（英文原版）

**Description**

There is a 1-based binary matrix where 0 represents land and 1 represents water. You are given integers row and col representing the number of rows and columns in the matrix, respectively.
Initially on day 0, the entire matrix is land. However, each day a new cell becomes flooded with water. You are given a 1-based 2D array cells, where cells[i] = [ri, ci] represents that on the ith day, the cell on the rith row and cith column (1-based coordinates) will be covered with water (i.e., changed to 1).
You want to find the last day that it is possible to walk from the top to the bottom by only walking on land cells. You can start from any cell in the top row and end at any cell in the bottom row. You can only travel in the four cardinal directions (left, right, up, and down).
Return the last day where it is possible to walk from the top to the bottom by only walking on land cells.

**Examples**

**Example 1:**

```
Input: row = 2, col = 2, cells = [[1,1],[2,1],[1,2],[2,2]]
Output: 2
Explanation: The above image depicts how the matrix changes each day starting from day 0.
The last day where it is possible to cross from top to bottom is on day 2.
```

**Example 2:**

```
Input: row = 2, col = 2, cells = [[1,1],[1,2],[2,1],[2,2]]
Output: 1
Explanation: The above image depicts how the matrix changes each day starting from day 0.
The last day where it is possible to cross from top to bottom is on day 1.
```

**Example 3:**

```
Input: row = 3, col = 3, cells = [[1,2],[2,1],[3,3],[2,2],[1,1],[1,3],[2,3],[3,2],[3,1]]
Output: 3
Explanation: The above image depicts how the matrix changes each day starting from day 0.
The last day where it is possible to cross from top to bottom is on day 3.
```

**Constraints**

- 2 <= row, col <= 2 * 104
- 4 <= row * col <= 2 * 104
- cells.length == row * col
- 1 <= ri <= row
- 1 <= ci <= col
- All the values of cells are unique.

---

## 题目（中文翻译）

有一个 **1 基（1-based）** 的二进制矩阵，其中 `0` 表示陆地（land），`1` 表示水域（water）。给定整数 `row` 和 `col`，分别表示矩阵的行数和列数。  

最初（第 0 天），整个矩阵全是陆地。随后，每一天都会有一个新的单元格被水淹没。给定一个 **1 基（1-based）** 的二维数组 `cells`，其中 `cells[i] = [ri, ci]` 表示第 `i` 天，第 `ri` 行第 `ci` 列的单元格会被覆盖为水（即改为 `1`）。  

你需要找出还能从顶部走到底部的**最后一天**。可以从顶行的任意单元格出发，结束于底行的任意单元格。只能在四个基本方向（左、右、上、下）上移动，并且只能走在陆地单元格上。  

返回能够仅在陆地单元格上从顶部走到底部的**最后一天**。

---

### 示例

#### 示例 1
```text
Input: row = 2, col = 2, cells = [[1,1],[2,1],[1,2],[2,2]]
Output: 2
Explanation: 上图展示了从第 0 天开始矩阵每天的变化。能够从顶部穿越到底部的最后一天是第 2 天。
```

#### 示例 2
```text
Input: row = 2, col = 2, cells = [[1,1],[1,2],[2,1],[2,2]]
Output: 1
Explanation: 上图展示了从第 0 天开始矩阵每天的变化。能够从顶部穿越到底部的最后一天是第 1 天。
```

#### 示例 3
```text
Input: row = 3, col = 3, cells = [[1,2],[2,1],[3,3],[2,2],[1,1],[1,3],[2,3],[3,2],[3,1]]
Output: 3
Explanation: 上图展示了从第 0 天开始矩阵每天的变化。能够从顶部穿越到底部的最后一天是第 3 天。
```

---

### 约束条件

- `2 <= row, col <= 2 * 10^4`
- `4 <= row * col <= 2 * 10^4`
- `cells.length == row * col`
- `1 <= ri <= row`
- `1 <= ci <= col`
- `cells` 中的所有坐标均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **模拟每天的淹没过程**，并在每一天检查能否从上边缘走到下边缘。  
具体步骤：

1. **构造矩阵**：一开始全是陆地（0），每天把 `cells[i]` 对应的坐标改成水（1）。  
2. **路径检测**：遍历矩阵，使用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 从所有上排的陆地格子出发，尝试走到下排的任意陆地格子。  
   - 把矩阵看成图，格子是节点，四个方向的相邻格子之间有边。  
   - BFS 类似于在地图上“顺着陆地走”，只要能碰到下排的陆地，就说明这一天还能通行。  

> **类比**：把矩阵想象成一张城市地图，陆地是道路，水是封闭的道路。我们从城市的最北端（上排）出发，看看能否一路走到最南端（下排）。DFS/BFS 就像是让一支探险队在地图上随意走，碰到终点就成功。

为什么这个方法一定能得到答案？  
因为我们对每一天都做了完整的“是否有通路”检查，最后一次检查成功的那一天，就是题目要求的 **最后可以通行的天数**。

#### 代码（Python）

```python
from collections import deque
from typing import List

def latestDayToCross_bruteforce(row: int, col: int, cells: List[List[int]]) -> int:
    # 1. 初始化全是陆地的矩阵（0 表示陆地，1 表示水）
    grid = [[0] * col for _ in range(row)]

    # 2. 每天把一个格子变成水，并检查是否还能通行
    for day, (r, c) in enumerate(cells, start=1):   # day 从 1 开始计数
        grid[r - 1][c - 1] = 1                       # 变成水（下标要减 1）

        # BFS：从上排所有陆地格子出发
        q = deque()
        visited = [[False] * col for _ in range(row)]

        # 把所有上排的陆地加入队列
        for j in range(col):
            if grid[0][j] == 0:
                q.append((0, j))
                visited[0][j] = True

        # 四个方向的移动向量
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while q:
            x, y = q.popleft()
            # 到达最后一行说明还能通行
            if x == row - 1:
                # 这一天仍然可以走通，继续下一天
                break
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < row and 0 <= ny < col \
                        and not visited[nx][ny] and grid[nx][ny] == 0:
                    visited[nx][ny] = True
                    q.append((nx, ny))
        else:
            # BFS 结束都没到达最后一行，说明这一天已经不能通行
            # 返回前一天的编号（因为 day 从 1 开始，所以答案是 day-1）
            return day - 1

    # 所有天都能通行（理论上不会出现，因为最后一天全被水覆盖）
    return len(cells)
```

#### 复杂度  

- **时间复杂度**：`O(row * col * (row * col))`  
  - 每天都要对整个矩阵进行一次 BFS，最坏情况下 BFS 要遍历所有格子，格子总数是 `row * col`。  
  - 用大白话讲，就是“天数 × 矩阵大小”，如果矩阵有 10⁴ 个格子，天数也是 10⁴，算法大约要跑 10⁸ 次操作，明显太慢。  
- **空间复杂度**：`O(row * col)`  
  - 需要保存整个矩阵和 BFS 的 visited 数组，和矩阵大小是同量级。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每一天都要重新跑一次 BFS，重复检查大量已经“被水封住”的区域。  
我们可以把 **“是否可以通行”** 看成一个 **单调性** 的判断：

- 天数越早，水越少，通行的可能性越大（**单调递增**：早期一定能通，后期可能不能）。
- 天数越晚，水越多，通行的可能性越小。

因此，**二分搜索**（Binary Search）可以用来快速定位“最后还能通行的天数”。  
二分搜索的核心是：**给定一个天数 d，判断在第 d 天的状态下是否还能从上到下**。这一步的判断仍然需要图的连通性检查，但只做一次，而不是每一天都做。

**实现细节**：

1. **二分搜索范围**  
   - 最早可能是第 `0` 天（全是陆地），最晚可能是第 `row*col` 天（全部被水）。  
   - 用左闭右闭 `[lo, hi]` 区间进行搜索。

2. **把第 d 天的矩阵构造出来**  
   - 直接把 `cells[:d]` 对应的格子标记为水。  
   - 为了不每次都重新创建整张矩阵，可以在每次判断时 **新建一个空矩阵** 并把前 `d` 个格子填上水，时间仍然是 `O(d)`，但二分搜索只会调用 `log(row*col)` 次，整体仍然是 `O(N log N)`（N 为格子总数）。

3. **连通性检查**  
   - 同样使用 BFS/DFS，从上排的所有陆地出发，看看能否到达下排。  
   - 这里的 BFS 只会在 **第 d 天的实际陆地** 上遍历，最多遍历 `N` 个格子。

4. **二分搜索过程**  
   - 若第 `mid` 天还能通，则说明答案至少是 `mid`，把左边界左移 `lo = mid + 1`（继续寻找更大的天数）。  
   - 若第 `mid` 天已经不能通，则答案在左侧，右边界右移 `hi = mid - 1`。  
   - 循环结束后，`hi` 正好是最后一次还能通的天数。

> **类比**：把所有天数排成一本厚厚的书，前面章节（早期）讲的是“道路畅通”，后面章节（晚期）讲的是“道路被水淹”。我们想找最后一个“还能走通”的章节，二分搜索就像是用手指快速翻到中间章节，判断是否还能走通，然后决定向前还是向后继续翻。

#### 代码（Python）

```python
from collections import deque
from typing import List

def latestDayToCross(row: int, col: int, cells: List[List[int]]) -> int:
    """
    二分搜索 + BFS 判断能否通行
    返回最后一天仍然可以从上到下
    """
    # 方向向量：下、上、右、左
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # ---------- 判断第 d 天是否还能通 ----------
    def can_cross(day: int) -> bool:
        """
        day 表示已经有 day 块格子被水覆盖（1-indexed 的前 day 天）。
        """
        # 1. 构造第 day 天的网格
        grid = [[0] * col for _ in range(row)]
        for i in range(day):
            r, c = cells[i]
            grid[r - 1][c - 1] = 1          # 标记为水

        # 2. BFS：从上排所有陆地格子开始
        q = deque()
        visited = [[False] * col for _ in range(row)]

        for j in range(col):
            if grid[0][j] == 0:             # 上排陆地可以作为起点
                q.append((0, j))
                visited[0][j] = True

        while q:
            x, y = q.popleft()
            if x == row - 1:                # 到达最后一行说明可以通
                return True
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < row and 0 <= ny < col \
                        and not visited[nx][ny] and grid[nx][ny] == 0:
                    visited[nx][ny] = True
                    q.append((nx, ny))
        return False                        # BFS 结束未到达底部

    # ---------- 二分搜索 ----------
    lo, hi = 1, row * col                     # 天数从 1 到 N
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_cross(mid):                    # 第 mid 天还能通
            ans = mid                         # 记录可能的答案
            lo = mid + 1                      # 继续尝试更大的天数
        else:
            hi = mid - 1                      # 必须往前找
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N log N)`  
  - `N = row * col` 为格子总数。  
  - 二分搜索需要 `log N` 次判断，每次判断要遍历最多 `N` 个格子（构造网格 + BFS）。  
  - 用大白话说，就是“先把天数切成二分，最多检查 20 次左右（因为 N ≤ 2·10⁴），每次检查要走遍所有格子”。相较于暴力的 `O(N²)`，快了几个数量级。

- **空间复杂度**：`O(N)`  
  - 需要保存当前检查的网格和 BFS 的 visited 数组，和矩阵大小相同。  
  - 只使用常数级的额外变量（队列、指针等），不随二分次数增长。

---

## 心得

- **核心技巧**：**二分搜索 + 图的连通性检查**（BFS/DFS）。  
- **适用的题型**  
  1. “在某个阈值下是否满足某种条件”，例如 **“最大化最小路径”**（LeetCode 1102）  
  2. “随着时间/操作的累加，状态单调变化”，例如 **“在加盐后是否还能喝水”**（模拟）  
  3. **“在网格中，随着障碍物增加，是否还能连通两端”**，如本题。  

> **一句话总结解题钥匙**：把“是否还能通”视作单调函数，用二分快速定位最后的可行天数，再用 BFS 检查连通性。

---

## 反思

- **第一反应**：直接模拟每天的变化并每次跑 BFS，想到的都是最直观的 “一步步走”。  
- **最容易踩的坑**  
  1. **下标错误**：题目坐标是 1‑based，需要在代码里减 1。  
  2. **二分边界**：左闭右闭写法容易写错，尤其是返回值应该是 `hi`（或记录的 `ans`）。  
  3. **忘记把已淹没的格子标记为水**：在 `can_cross` 里必须先把前 `day` 天的格子全部设为 1，否则会误判。  
  4. **递归深度**：如果用 DFS 递归实现，深度可能达到 2·10⁴，会导致栈溢出，推荐使用显式栈或 BFS。  

- **下次类似题目第一步**：先判断“是否存在单调性”。如果答案随某个数值单调递增/递减，就可以尝试 **二分搜索** 来降低时间复杂度；随后再选取合适的 **图遍历**（BFS/DFS/Union‑Find）来实现单次判定。