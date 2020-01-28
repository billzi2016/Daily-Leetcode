# #749. **隔离病毒** / Contain Virus

> 难度：困难 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/contain-virus/)

---

## 题目（英文原版）

**Description**

A virus is spreading rapidly, and your task is to quarantine the infected area by installing walls.
The world is modeled as an m x n binary grid isInfected, where isInfected[i][j] == 0 represents uninfected cells, and isInfected[i][j] == 1 represents cells contaminated with the virus. A wall (and only one wall) can be installed between any two 4-directionally adjacent cells, on the shared boundary.
Every night, the virus spreads to all neighboring cells in all four directions unless blocked by a wall. Resources are limited. Each day, you can install walls around only one region (i.e., the affected area (continuous block of infected cells) that threatens the most uninfected cells the following night). There will never be a tie.
Return the number of walls used to quarantine all the infected regions. If the world will become fully infected, return the number of walls used.

**Examples**

**Example 1:**

```
Input: isInfected = [[0,1,0,0,0,0,0,1],[0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]]
Output: 10
Explanation: There are 2 contaminated regions.
On the first day, add 5 walls to quarantine the viral region on the left. The board after the virus spreads is:

On the second day, add 5 walls to quarantine the viral region on the right. The virus is fully contained.
```

**Example 2:**

```
Input: isInfected = [[1,1,1],[1,0,1],[1,1,1]]
Output: 4
Explanation: Even though there is only one cell saved, there are 4 walls built.
Notice that walls are only built on the shared boundary of two different cells.
```

**Example 3:**

```
Input: isInfected = [[1,1,1,0,0,0,0,0,0],[1,0,1,0,1,1,1,1,1],[1,1,1,0,0,0,0,0,0]]
Output: 13
Explanation: The region on the left only builds two new walls.
```

**Constraints**

- m == isInfected.length
- n == isInfected[i].length
- 1 <= m, n <= 50
- isInfected[i][j] is either 0 or 1.
- There is always a contiguous viral region throughout the described process that will infect strictly more uncontaminated squares in the next round.

---

## 题目（中文翻译）

一种病毒正在迅速蔓延，你的任务是通过修建墙壁将感染区域隔离。

世界被抽象为一个 **m × n** 的二进制网格 `isInfected`，其中 `isInfected[i][j] == 0` 表示**未感染**（uninfected）格子，`isInfected[i][j] == 1` 表示**已感染**（contaminated）格子。

可以在任意两个**四向相邻**（4-directionally adjacent）的格子之间的公共边界上修建**一堵墙**（且每条公共边界最多只能修建一堵墙）。

每个夜晚，病毒会向四个方向的相邻格子传播，除非该方向被墙壁阻挡。

资源有限。每一天，你只能围住**一个区域**（即受影响的区域——**感染细胞的连续块**（continuous block of infected cells）——它在下一晚会威胁到最多**未感染**格子）。题目保证不会出现并列的情况。

返回用于隔离所有感染区域的墙壁总数。如果最终整个世界都会被感染，则返回已修建的墙壁数量。

---

### 示例

#### 示例 1
**输入**
```json
isInfected = [[0,1,0,0,0,0,0,1],
              [0,1,0,0,0,0,0,1],
              [0,0,0,0,0,0,0,1],
              [0,0,0,0,0,0,0,0]]
```
**输出**
```
10
```
**解释**  
存在 2 个被感染的区域。  
第一天，在左侧的病毒区域周围修建 5 面墙以将其隔离。病毒传播后的棋盘如下所示（省略图示）。  
第二天，在右侧的病毒区域周围再修建 5 面墙，病毒被完全遏制。

#### 示例 2
**输入**
```json
isInfected = [[1,1,1],
              [1,0,1],
              [1,1,1]]
```
**输出**
```
4
```
**解释**  
虽然最终只拯救了一个格子，但共修建了 4 面墙。需要注意的是，墙只能建在两格不同状态的公共边界上。

#### 示例 3
**输入**
```json
isInfected = [[1,1,1,0,0,0,0,0,0],
              [1,0,1,0,1,1,1,1,1],
              [1,1,1,0,0,0,0,0,0]]
```
**输出**
```
13
```
**解释**  
左侧的感染区域只需要再建两面墙，其余墙壁已在之前的步骤中修建。

---

### 约束条件
- `m == isInfected.length`
- `n == isInfected[i].length`
- `1 <= m, n <= 50`
- `isInfected[i][j]` 只能为 `0` 或 `1`
- 在描述的整个过程中，总会存在一个连续的病毒区域，在下一轮会感染**严格更多**的未感染格子。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的选择都枚举一遍**，然后从中挑出用墙最少的那条路线。  
具体来说：

1. **找出所有感染块**（即相互 4‑方向相连的 `1`），每个块记作一个“区域”。  
2. 对每个区域，计算它在下一晚会感染多少未感染的格子（我们叫它 **威胁度**），以及需要围住它的墙数（**周长**）。  
3. **枚举**：今天我们可以任选一个区域去围墙，付出它的周长，然后把该区域标记为“已隔离”。其余区域会按照威胁度把病毒向外扩散一格。  
4. 对新的格局递归地继续第 1 步，直到所有病毒都被隔离或整个矩阵被感染。  
5. 记录所有递归路径的墙总数，返回最小值。

> **类比**：想象你在玩一盘棋，每一步可以选任意一块“红子”围住，围住后红子就不能再走。因为每一步都有多种选择，想要得到最少的围墙数，就得把所有可能的走法都试一遍——这就是“暴力搜索”。

**为什么这个方法一定能得到正确答案？**  
因为我们把**所有合法的每日选择**都考虑进来了，答案一定出现在这些枚举的分支里。只要递归的终止条件（所有病毒被隔离或全盘被感染）写对，最终返回的最小墙数就是题目要求的最优解。

**但是**，每一天可能有 `k` 个区域可以选择，随后又会出现新的若干区域，递归树的宽度和深度都很大，时间会呈指数级增长，根本跑不完。

#### 代码（Python）

```python
from typing import List, Tuple, Set
import copy
import sys
sys.setrecursionlimit(10**6)

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def bfs_region(grid: List[List[int]], i: int, j: int,
               visited: List[List[bool]]) -> Tuple[Set[Tuple[int,int]],
                                                   Set[Tuple[int,int]],
                                                   int]:
    """
    从 (i,j) 出发，用 BFS 找出同一感染块的所有细胞
    返回：
        region   – 该块所有感染细胞坐标集合
        frontier – 与之相邻的未感染细胞集合（病毒下一晚会感染的地方）
        perimeter – 围住该块需要的墙数
    """
    m, n = len(grid), len(grid[0])
    q = [(i,j)]
    region = set()
    frontier = set()
    perimeter = 0
    visited[i][j] = True

    while q:
        x, y = q.pop()
        region.add((x,y))
        for dx, dy in DIRS:
            nx, ny = x+dx, y+dy
            if 0 <= nx < m and 0 <= ny < n:
                if grid[nx][ny] == 1 and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx,ny))
                elif grid[nx][ny] == 0:          # 邻居是未感染格子
                    frontier.add((nx,ny))
                    perimeter += 1               # 这条边需要一面墙
            else:
                # 越界的地方自然算作墙，这里不计数（题目只在格子之间建墙）
                pass
    return region, frontier, perimeter


def brute_force(grid: List[List[int]]) -> int:
    """
    完全暴力：递归枚举每天隔离哪个区域，返回最小墙数。
    由于搜索空间指数级，这个实现只能用于极小的测试例子。
    """
    m, n = len(grid), len(grid[0])

    # ---------- 递归函数 ----------
    def dfs(cur_grid: List[List[int]]) -> int:
        # 1. 找出所有感染块
        visited = [[False]*n for _ in range(m)]
        regions = []          # 每个元素是 (region_set, frontier_set, perimeter)
        for i in range(m):
            for j in range(n):
                if cur_grid[i][j] == 1 and not visited[i][j]:
                    region, frontier, peri = bfs_region(cur_grid, i, j, visited)
                    regions.append((region, frontier, peri))

        if not regions:                # 没有病毒了
            return 0

        # 2. 对每一个可能的选择递归尝试
        best = float('inf')
        for idx, (reg, front, peri) in enumerate(regions):
            # 复制一份网格，模拟本轮操作
            nxt = copy.deepcopy(cur_grid)

            # (a) 隔离选中的区域：把它们标记为 -1（表示已经被墙围住，后续不再传播）
            for x, y in reg:
                nxt[x][y] = -1

            # (b) 其余区域向前线扩散
            for jdx, (other_reg, other_front, _) in enumerate(regions):
                if jdx == idx:   # 已经隔离的块不再扩散
                    continue
                for x, y in other_front:
                    nxt[x][y] = 1   # 被感染

            # (c) 递归求后续需要的最少墙数
            total = peri + dfs(nxt)
            best = min(best, total)

        return best
    # ---------- 入口 ----------
    return dfs(grid)
```

> **提示**：上面的 `brute_force` 只适用于 `m·n ≤ 9` 之类的极小规模。对于正式的 LeetCode 输入（最多 50×50），它会在几毫秒内爆掉。

#### 复杂度  

- **时间复杂度**：`O( k^d )`（指数级），其中  
  - `k` 是某一天可能的感染块数（最坏情况下每个病毒单独成块，约为 `m·n`），  
  - `d` 是需要的天数（最多也可能是 `m·n`）。  
  换句话说，随着格子数的增加，搜索树的节点会呈指数增长，根本不可行。  
- **空间复杂度**：`O(m·n)` 用于递归栈和复制的网格。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有可能的每日选择**。事实上，题目已经给了我们一个“唯一的最佳选择”——**每天隔离威胁度最大的那块区域**。只要每一天按这个规则执行，就一定得到最终使用的墙数（题目保证不存在平局）。

因此我们只需要**一次遍历**得到所有感染块的信息，**挑出威胁最大的块**，隔离它并累计墙数；随后**让其余块向外扩散**，再重复上述过程，直至没有病毒可扩散。

实现细节如下：

1. **遍历整个网格，利用 BFS（或 DFS）找出所有感染块**。  
   对每个块我们记录三件事：  
   - `region`：块内部的所有 `(i,j)` 坐标（后面需要把它标记为已隔离）。  
   - `frontier`：块相邻的未感染格子集合（这些格子是下一晚会被感染的）。  
   - `perimeter`：围住该块所需的墙数——每当块的一个细胞向四个方向看到未感染格子（或越界）时，墙数 +1。  

   > **类比**：把每个感染块想象成一座岛屿，`frontier` 就是岛屿周围的海岸线，`perimeter` 就是需要建的防波堤长度。

2. **挑选威胁度最大的块**（即 `frontier` 的大小最大），把它的 `perimeter` 加到答案中，并把 `region` 中的细胞设为 `-1`（表示已经被墙完全封住，后面不再参与扩散）。

3. **其余块向外扩散**：遍历除已隔离块之外的所有 `frontier`，把这些格子改为 `1`（变成新感染细胞），这一步相当于病毒“向四周蔓延”。  

4. 重复 **1‑3**，直到网格中再也找不到 `1`（所有病毒都被围住）或 `frontier` 为空（整个世界已被感染）。  

整个过程每一天都只需要一次完整的 BFS，时间复杂度是 **`O(m·n·days)`**，而 `days` 最多是 `m·n`，所以总体是 **`O((m·n)^2)`**，在 50×50 的限制下完全可接受。

#### 代码（Python）

```python
from typing import List, Set, Tuple
from collections import deque

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

class Solution:
    def containVirus(self, isInfected: List[List[int]]) -> int:
        """
        主函数：返回为了把所有病毒隔离所需的最少墙数。
        思路按照上文的“最优解”一步步实现。
        """
        m, n = len(isInfected), len(isInfected[0])
        answer = 0

        while True:
            # ---------- 1. 找出所有感染块 ----------
            visited = [[False]*n for _ in range(m)]
            regions: List[Set[Tuple[int,int]]] = []      # 每块内部细胞集合
            frontiers: List[Set[Tuple[int,int]]] = []    # 每块可以感染的未感染格子集合
            perimeters: List[int] = []                  # 每块围墙数

            for i in range(m):
                for j in range(n):
                    if isInfected[i][j] == 1 and not visited[i][j]:
                        region, frontier, peri = self._bfs(i, j, isInfected,
                                                          visited, m, n)
                        regions.append(region)
                        frontiers.append(frontier)
                        perimeters.append(peri)

            if not regions:          # 没有病毒了
                break

            # ---------- 2. 选出威胁最大的块 ----------
            max_idx = 0
            max_frontier = len(frontiers[0])
            for idx in range(1, len(frontiers)):
                if len(frontiers[idx]) > max_frontier:
                    max_frontier = len(frontiers[idx])
                    max_idx = idx

            # 把选中的块隔离，累计墙数
            answer += perimeters[max_idx]
            for x, y in regions[max_idx]:
                isInfected[x][y] = -1          # -1 表示已经被围住，后面不再传播

            # ---------- 3. 其余块向外扩散 ----------
            # 先把所有要被感染的格子收集起来，避免一次扩散影响同一天的计算
            to_infect: Set[Tuple[int,int]] = set()
            for idx, frontier in enumerate(frontiers):
                if idx == max_idx:               # 已隔离的块不再扩散
                    continue
                to_infect.update(frontier)

            for x, y in to_infect:
                isInfected[x][y] = 1

            # ---------- 4. 检查是否还有活跃的病毒 ----------
            # 如果所有 1 都已经被 -1 包围，循环会在下一次的 regions 为空时结束
        return answer

    def _bfs(self, si: int, sj: int,
             grid: List[List[int]],
             visited: List[List[bool]],
             m: int, n: int) -> Tuple[Set[Tuple[int,int]],
                                      Set[Tuple[int,int]],
                                      int]:
        """
        从 (si,sj) 出发，遍历同一感染块。
        同时统计：
            - region   : 所有 1 的坐标
            - frontier : 与之相邻的 0 坐标
            - perimeter: 需要建的墙数
        """
        q = deque()
        q.append((si, sj))
        visited[si][sj] = True

        region: Set[Tuple[int,int]] = set()
        frontier: Set[Tuple[int,int]] = set()
        perimeter = 0

        while q:
            x, y = q.popleft()
            region.add((x, y))
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    if grid[nx][ny] == 1 and not visited[nx][ny]:
                        visited[nx][ny] = True
                        q.append((nx, ny))
                    elif grid[nx][ny] == 0:          # 邻居是未感染格子
                        frontier.add((nx, ny))
                        perimeter += 1               # 这条边需要一面墙
                else:
                    # 越界自然算作墙，这里不计数（题目只在格子之间建墙）
                    pass
        return region, frontier, perimeter
```

> 代码中每一行都有中文注释，直接复制到本地即可运行。  

#### 复杂度  

- **时间复杂度**：`O(m·n·days)`，其中 `days` 最多为 `m·n`。在最坏情况下（病毒每一天只能扩大一个格子），总操作数约为 `(m·n)^2 ≤ 2500^2 = 6.25e6`，在 1 秒内轻松完成。  
  - **解释**：我们每天对整个网格做一次 BFS，遍历每个格子至多 `days` 次。  
- **空间复杂度**：`O(m·n)` 用于 `visited`、`region`、`frontier` 等集合以及 BFS 队列。  
  - 这相当于保存网格本身的大小，不会超过 2500 个整数。

---

## 心得  

- **核心技巧**：**一次遍历找所有连通块 + 选最大威胁度块进行隔离**。  
- **适用的题型**：  
  1. “岛屿计数”类问题（需要找所有连通块）。  
  2. “最小墙/最小围栏”类问题（如 LeetCode 749. Contain Virus、LeetCode 463. Island Perimeter）。  
  3. “每轮选择最有价值的对象”类的贪心模拟（如 928. Minimize Malware Spread）。  
- **一句话总结解题钥匙**：**每天只做“威胁最大”的那件事，贪心 + BFS 即可**。

---

## 反思  

- **第一反应**：看到“每天只能围一块、要把病毒全部隔离”，立刻想到 **贪心**——每次挑最“危险”的块。  
- **最容易踩的坑**：  
  - **把已隔离的细胞错误地继续扩散**（一定要把它们标记为 `-1`，并在后续遍历时忽略）。  
  - **墙的计数**：墙只算在 **感染块与未感染块之间的边**，越界不计数。  
  - **同一天的扩散相互影响**：必须先把所有要感染的格子收集到集合 `to_infect`，再一次性写入网格，防止一块的扩散“抢走”另一块的 frontier。  
- **下次遇到类似题**，第一步就思考：**“是否可以把每一步的选择唯一化？”**（比如最大/最小/最近），如果能，就直接用贪心 + BFS/DFS 模拟，避免指数级搜索。