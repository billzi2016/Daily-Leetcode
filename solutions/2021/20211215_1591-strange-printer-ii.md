# #1591. 奇怪的打印机 II / Strange Printer II

> 难度：困难 · 标签：Array、Graph、Topological Sort、Matrix · [LeetCode 链接](https://leetcode.com/problems/strange-printer-ii/)

---

## 题目（英文原版）

**Description**

There is a strange printer with the following two special requirements:
You are given a m x n matrix targetGrid, where targetGrid[row][col] is the color in the position (row, col) of the grid.
Return true if it is possible to print the matrix targetGrid, otherwise, return false.

**Examples**

**Example 1:**

```
Input: targetGrid = [[1,1,1,1],[1,2,2,1],[1,2,2,1],[1,1,1,1]]
Output: true
```

**Example 2:**

```
Input: targetGrid = [[1,1,1,1],[1,1,3,3],[1,1,3,4],[5,5,1,4]]
Output: true
```

**Example 3:**

```
Input: targetGrid = [[1,2,1],[2,1,2],[1,2,1]]
Output: false
Explanation: It is impossible to form targetGrid because it is not allowed to print the same color in different turns.
```

**Constraints**

- m == targetGrid.length
- n == targetGrid[i].length
- 1 <= m, n <= 60
- 1 <= targetGrid[row][col] <= 60

---

## 题目（中文翻译）

有一台奇怪的打印机，它有以下两个特殊要求：

给定一个 `m x n` 的矩阵 `targetGrid`，其中 `targetGrid[row][col]` 表示网格中坐标 `(row, col)` 处的颜色。  
如果可以打印出矩阵 `targetGrid`，返回 `true`；否则返回 `false`。

示例 1  
示例 2  
示例 3  

约束条件：

- `m == targetGrid.length`
- `n == targetGrid[i].length`
- `1 <= m, n <= 60`
- `1 <= targetGrid[row][col] <= 60`

示例  
**示例 1:**  
```text
Input: targetGrid = [[1,1,1,1],[1,2,2,1],[1,2,2,1],[1,1,1,1]]
Output: true
```

**示例 2:**  
```text
Input: targetGrid = [[1,1,1,1],[1,1,3,3],[1,1,3,4],[5,5,1,4]]
Output: true
```

**示例 3:**  
```text
Input: targetGrid = [[1,2,1],[2,1,2],[1,2,1]]
Output: false
Explanation: 由于不允许在不同的打印回合中使用相同的颜色，因此无法形成 targetGrid。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把打印过程完整地模拟出来**：

1. 先从空白的网格（所有格子都是 `0`）开始。  
2. 每一次“打印”可以任选一种颜色 `c`，再任选一个**矩形**（左上 `(r1,c1)`，右下 `(r2,c2)`），把矩形内部的所有格子都改成 `c`。  
3. 重复第 2 步，直到得到和 `targetGrid` 完全相同的网格。

这跟我们在生活中使用喷漆或画笔的过程很像：先在画布上画一个矩形，后面再在上面覆盖其他颜色的矩形，最终形成目标图案。

**为什么这个方法一定能得到答案（如果答案是 “可以”）**  
只要我们把**每一种颜色出现的所有格子**都一次性打印成一个覆盖它们的矩形，并且按照某个顺序（后打印的会覆盖前面的），最终一定能得到目标网格。因为题目并没有限制每种颜色只能打印一次，也没有限制矩形的大小，只要是矩形就行。

**为什么暴力会超时**  
- 颜色的种类最多 60，所有可能的打印顺序是 `60!`（阶乘），天文数字，根本不可能枚举。  
- 即使把顺序固定，只是枚举矩形的左上右下四个坐标，也要遍历 `O(m^2 * n^2)` 种矩形（每次都要检查是否覆盖正确），再乘以最多 `m*n` 次打印，时间会爆炸。  

**大白话解释复杂度**：  
- **时间复杂度**：`O(k! * m^2 * n^2)`（`k` 是颜色种类数），等价于“每秒只能做几万次的电脑，要跑上几千年的循环”。  
- **空间复杂度**：`O(m*n)`，只需要保存当前的网格。

显然，这种“穷举所有可能”的办法在实际测试里根本跑不完，只能作为思考的起点。

#### 代码（Python）

```python
from copy import deepcopy
from itertools import permutations
from typing import List

def brute_force(target: List[List[int]]) -> bool:
    m, n = len(target), len(target[0])
    colors = sorted({target[i][j] for i in range(m) for j in range(n)})

    # 生成每种颜色的所有可能矩形（左上右下）
    rects = {}
    for c in colors:
        rects[c] = []
        # 为简化，这里只列举**恰好覆盖所有该颜色格子的最小矩形**一种情况
        min_r = min(i for i in range(m) for j in range(n) if target[i][j] == c)
        max_r = max(i for i in range(m) for j in range(n) if target[i][j] == c)
        min_c = min(j for i in range(m) for j in range(n) if target[i][j] == c)
        max_c = max(j for i in range(m) for j in range(n) if target[i][j] == c)
        rects[c].append((min_r, min_c, max_r, max_c))

    # 枚举所有颜色的打印顺序（仅示例，实际会 TLE）
    for order in permutations(colors):
        grid = [[0] * n for _ in range(m)]          # 空白画布
        for col in order:
            # 这里直接取唯一的最小矩形
            r1, c1, r2, c2 = rects[col][0]
            for i in range(r1, r2 + 1):
                for j in range(c1, c2 + 1):
                    grid[i][j] = col               # 用该颜色覆盖
        if grid == target:
            return True
    return False
```

> **注意**：上面的代码只演示“暴力思路”，实际运行会因为 `permutations` 的阶乘爆炸而在很小的输入上就卡死。

#### 复杂度

- **时间复杂度**：`O(k! * m * n)`（`k` 为不同颜色数），`k!` 代表所有可能的打印顺序，随着颜色种类的增加会呈指数级增长。  
- **空间复杂度**：`O(m * n)`，存放当前的网格。

---

### 2. 最优解

#### 思路  

**从暴力的瓶颈出发**：我们想知道“哪种颜色可以最后打印”。如果能一次性判断所有颜色的先后关系，就可以直接检查是否存在冲突（循环依赖），而不必真的去枚举每一步。

**关键观察——逆向思考**  
> 给定最终的 `targetGrid`，如果一种颜色 `c` 是**最后一次被打印**的，那么在它的**最小外接矩形**内部**不应该出现别的颜色**。  
> 因为如果在这个矩形里还有别的颜色 `d`，说明 `d` 必须在 `c` 之后再覆盖进来，这与 `c` 是最后打印冲突。

因此：

1. **统计每种颜色的最小外接矩形**（左上、右下坐标）。这一步只需要一次遍历，类似“在地图上找出每座城市的最北、最南、最东、最西的点”。  
2. 对每种颜色 `c`，遍历它的矩形内部的每个格子。若格子颜色是 `d ≠ c`，说明 `c` 必须**先于** `d` 打印（因为 `d` 最后把这个格子改成了自己的颜色）。于是我们在有向图中加入一条 **c → d** 的边。  
3. 把所有颜色看成图的节点，所有 “先于” 关系看成有向边。只要这张有向图**不存在环**，就可以找到一个合法的打印顺序（拓扑排序）。若出现环，则说明有循环依赖，打印不可能完成。  

**核心算法**：  
- **前缀/后缀遍历**求最小外接矩形（O(m·n)）  
- **构图 + 拓扑排序（Kahn 算法）**（O(C² + m·n)），其中 `C ≤ 60` 是颜色种类数  

**类比**：把每种颜色想象成一块拼图，矩形里出现的其他颜色就像“被压在下面的拼图”。我们要把“压在上面的”先放好，才能把下面的放进去。若出现“相互压在对方上面”的循环，就根本拼不出来。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Tuple

def isPrintable(targetGrid: List[List[int]]) -> bool:
    m, n = len(targetGrid), len(targetGrid[0])

    # 1. 统计每种颜色的最小外接矩形
    # 用字典存储：color -> (min_row, min_col, max_row, max_col)
    rect: dict[int, Tuple[int, int, int, int]] = {}
    for i in range(m):
        for j in range(n):
            col = targetGrid[i][j]
            if col not in rect:
                rect[col] = (i, j, i, j)          # 第一次出现，四个角都在这里
            else:
                min_r, min_c, max_r, max_c = rect[col]
                rect[col] = (min(min_r, i), min(min_c, j),
                             max(max_r, i), max(max_c, j))

    # 2. 根据矩形内部的不同颜色建立有向边
    # graph[u] = {v1, v2, ...} 表示 u 必须在 v 之前打印
    graph = defaultdict(set)
    indegree = defaultdict(int)                 # 统计每个节点的入度

    for color, (r1, c1, r2, c2) in rect.items():
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1):
                other = targetGrid[i][j]
                if other != color:               # 颜色不同，形成依赖
                    if other not in graph[color]:
                        graph[color].add(other)
                        indegree[other] += 1     # other 多了一个前驱

    # 3. 拓扑排序（Kahn）判断是否有环
    # 把所有入度为 0 的颜色先放入队列
    zero_indeg = deque([c for c in rect if indegree[c] == 0])

    visited = 0
    while zero_indeg:
        cur = zero_indeg.popleft()
        visited += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1                 # 删除一条边
            if indegree[nxt] == 0:
                zero_indeg.append(nxt)

    # 如果所有颜色都被访问过，说明图是 DAG（无环），可以打印
    return visited == len(rect)
```

**代码要点解释**：

| 行号 | 中文注释 |
|------|----------|
| 9‑16 | 遍历整个网格，收集每种颜色出现的最左/上/右/下坐标，得到最小外接矩形。 |
| 22‑30 | 对每种颜色的矩形内部逐格检查，若出现不同颜色 `other`，就在有向图中加入 `color → other` 边，并更新 `other` 的入度。 |
| 34‑45 | Kahn 拓扑排序：先把入度为 0（没有前置依赖）的颜色放进队列，弹出后把它指向的边全部删掉，新的入度为 0 的节点继续入队。 |
| 48‑50 | 最终访问的颜色数量等于颜色种类数，说明没有环，返回 `True`；否则返回 `False`。 |

#### 复杂度

- **时间复杂度**：`O(m * n + C²)`  
  - `O(m * n)` 用于一次遍历统计矩形和检查矩形内部（每个格子最多被检查一次）。  
  - `C` 是不同颜色的数量，最多 60，构建图和拓扑排序最多 `C²`（约 3600）次操作，几乎可以忽略不计。  
  - 用大白话说，就是“和网格大小成正比”，最多几千次循环，跑得飞快。

- **空间复杂度**：`O(C + m * n)`  
  - `O(C)` 保存每种颜色的矩形和图的邻接表（最多 60）。  
  - 额外的 `O(m * n)` 用于存放原始网格（LeetCode 已经给出），我们不需要额外的副本。  

相比暴力的指数级时间，最优解只需要线性时间，能够轻松通过所有测试。

---

## 心得

- **核心技巧**：**逆向思考 + 拓扑排序**  
  先从最终图像出发，判断哪些颜色一定在其他颜色之前打印，进而构建有向依赖图，检查是否有环。

- **适用的题型**  
  1. **Strange Printer**（单行版）——同样利用“最后打印的颜色对应的最小连续子串”。  
  2. **Matrix Cascade / Grid Dependency** 系列题目——需要判断矩阵中元素的先后关系。  
  3. **Course Schedule**（课程表）——本质也是检查有向图是否有环的拓扑排序。

- **一句话总结**：  
  “把颜色看成任务，矩形内部的不同颜色就是前置条件，环即是 impossible”。  

---

## 反思

- **第一反应**：看到“打印矩形”就想直接模拟所有可能的打印顺序，结果立刻卡在了组合爆炸上。  
- **最容易踩的坑**  
  - 忽略 **同一种颜色可能出现不止一个矩形** 的情况；但题目保证每种颜色的所有格子在最终图中一定能被一个矩形覆盖（否则根本无法打印），所以只需要取最小外接矩形即可。  
  - 构图时忘记去重导致 **入度统计错误**（同一条边多算），会误判有环。  
  - 边界条件：单行或单列矩阵、只有一种颜色的特殊情况，都必须在代码里能正常跑。  

- **下次遇到同类题的第一步**：  
  “先在最终状态上寻找可以**最后**完成的元素/颜色”，把它们当成**无前置依赖**的节点，构建依赖图，再用拓扑排序判环。这样可以把“枚举所有步骤”的暴力思路直接转化为 **线性** 的图论检查。