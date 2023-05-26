# #2258. 逃离蔓延的火焰 / Escape the Spreading Fire

> 难度：困难 · 标签：Array、Binary Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/escape-the-spreading-fire/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array grid of size m x n which represents a field. Each cell has one of three values:
You are situated in the top-left cell, (0, 0), and you want to travel to the safehouse at the bottom-right cell, (m - 1, n - 1). Every minute, you may move to an adjacent grass cell. After your move, every fire cell will spread to all adjacent cells that are not walls.
Return the maximum number of minutes that you can stay in your initial position before moving while still safely reaching the safehouse. If this is impossible, return -1. If you can always reach the safehouse regardless of the minutes stayed, return 109.
Note that even if the fire spreads to the safehouse immediately after you have reached it, it will be counted as safely reaching the safehouse.
A cell is adjacent to another cell if the former is directly north, east, south, or west of the latter (i.e., their sides are touching).

**Examples**

**Example 1:**

```
Input: grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]]
Output: 3
Explanation: The figure above shows the scenario where you stay in the initial position for 3 minutes.
You will still be able to safely reach the safehouse.
Staying for more than 3 minutes will not allow you to safely reach the safehouse.
```

**Example 2:**

```
Input: grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]
Output: -1
Explanation: The figure above shows the scenario where you immediately move towards the safehouse.
Fire will spread to any cell you move towards and it is impossible to safely reach the safehouse.
Thus, -1 is returned.
```

**Example 3:**

```
Input: grid = [[0,0,0],[2,2,0],[1,2,0]]
Output: 1000000000
Explanation: The figure above shows the initial grid.
Notice that the fire is contained by walls and you will always be able to safely reach the safehouse.
Thus, 109 is returned.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 2 <= m, n <= 300
- 4 <= m * n <= 2 * 104
- grid[i][j] is either 0, 1, or 2.
- grid[0][0] == grid[m - 1][n - 1] == 0

---

## 题目（中文翻译）

**描述**  
给你一个下标从 0 开始的二维整数数组 `grid`，大小为 `m × n`，它表示一块场地。每个格子（cell）只能是以下三种取值之一：

- `0`：草地（grass），可以通行  
- `1`：墙壁（wall），不可通行，也会阻挡火焰扩散  
- `2`：火源（fire），会随时间向四周扩散  

你起始于左上角格子 `(0, 0)`，目标是到达右下角的安全屋 `(m‑1, n‑1)`。每一分钟，你可以移动到一个相邻的草地格子。**移动结束后**，所有火源格子会向四个方向（上下左右）扩散到所有不是墙壁的相邻格子。

返回你可以在不移动的情况下停留在初始位置的**最大分钟数**，并仍然能够安全到达安全屋。如果根本无法到达，返回 `-1`。如果无论你停留多久都一定能安全到达安全屋，返回 `10^9`。

> 注意：即使火焰在你抵达安全屋的**同一时刻**立即蔓延到安全屋，只要你已经到达，它仍算作安全到达。

两个格子相邻的定义是：其中一个格子位于另一个格子的正北、正东、正南或正西（即四边相接）。

---

### 示例

**示例 1**  
```text
输入: grid = [[0,2,0,0,0,0,0],
              [0,0,0,2,2,1,0],
              [0,2,0,0,1,2,0],
              [0,0,2,2,2,0,2],
              [0,0,0,0,0,0,0]]
输出: 3
解释: 上图展示了你在初始位置停留 3 分钟的情形。此时仍然可以安全到达安全屋。  
停留超过 3 分钟则无法安全到达安全屋。
```

**示例 2**  
```text
输入: grid = [[0,0,0,0],
              [0,1,2,0],
              [0,2,0,0]]
输出: -1
解释: 上图展示了你一开始就朝安全屋移动的情形。火焰会蔓延到你前进的每一个格子，导致无法安全到达安全屋，故返回 -1。
```

**示例 3**  
```text
输入: grid = [[0,0,0],
              [2,2,0],
              [1,2,0]]
输出: 1000000000
解释: 上图展示了初始的场地布局。可以看到火焰被墙壁完全围住，你无论何时出发都一定能够安全到达安全屋。  
因此返回 10^9。
```

---

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `2 ≤ m, n ≤ 300`
- `4 ≤ m × n ≤ 2 × 10^4`
- `grid[i][j]` 只会是 `0、1 或 2`
- `grid[0][0] == grid[m‑1][n‑1] == 0`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把“等几分钟再出发”** 当作枚举变量。  
- 先假设我们在起点 `(0,0)` 原地等待 `t` 分钟（`t` 从 `0` 开始递增）。  
- 等待结束后，从起点出发，用 **广度优先搜索（BFS）** 按最短路径在每一分钟向上下左右四个方向移动。  
- 同时，**模拟火焰的蔓延**：每走一步后，所有已经燃起的格子向四周扩散一次。  

只要在某一次模拟中，**我们能够在火焰到达之前走到右下角安全屋**，说明该 `t` 是可行的。继续尝试更大的 `t`，直到发现不可行为止，返回上一次可行的 `t`。  

> **类比**：  
> - **BFS** 就像在迷宫里一次一次“波纹”向外扩散，先到达的格子一定是最短步数能到达的。  
> - **火焰的蔓延** 也可以看成另一层波纹，只是它会在我们每移动一次后**同步**前进一步。  

这个方法之所以能得到正确答案，是因为我们穷举了所有可能的等待时间，并且每一次都完整模拟了人和火的同步运动，确保没有漏掉任何潜在的安全路径。

**但是**：  
- `t` 最大可能达到 `10^9`（题目给出的上限），直接线性枚举会导致 **时间爆炸**。  
- 每一次 `t` 的检查都要跑一次完整的 BFS，复杂度大约是 `O(m·n)`。  
- 所以整体时间复杂度会是 `O(t_max·m·n)`，在最坏情况下远远超出限制。

#### 代码（Python）

```python
from collections import deque
import copy

def brute_max_wait(grid):
    m, n = len(grid), len(grid[0])
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    # 计算火焰每分钟的扩散状态（上限取 1000，足够小的网格测试用）
    # 实际上这里会一直循环到整个地图被火覆盖或不再有新火
    def simulate_fire():
        fire = [[-1]*n for _ in range(m)]          # -1 表示永远不会被火点燃
        q = deque()
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:               # 初始火源
                    fire[i][j] = 0
                    q.append((i,j))
        t = 0
        while q:
            for _ in range(len(q)):
                x,y = q.popleft()
                for dx,dy in dirs:
                    nx,ny = x+dx, y+dy
                    if 0<=nx<m and 0<=ny<n and grid[nx][ny]!=1 and fire[nx][ny]==-1:
                        fire[nx][ny] = fire[x][y] + 1
                        q.append((nx,ny))
        return fire

    fire_time = simulate_fire()          # fire_time[x][y] = 火到达此格的最早分钟

    # 检查在等 t 分钟后，是否还能安全到达终点
    def can_reach(t):
        # 人的 BFS，状态 (x,y,cur_time)
        q = deque()
        visited = [[False]*n for _ in range(m)]
        if t < fire_time[0][0] or fire_time[0][0]==-1:   # 起点在等 t 分钟后仍未被火燃
            q.append((0,0,t))
            visited[0][0] = True
        else:
            return False

        while q:
            x,y,cur = q.popleft()
            if (x,y) == (m-1,n-1):
                return True
            for dx,dy in dirs:
                nx,ny = x+dx, y+dy
                if 0<=nx<m and 0<=ny<n and not visited[nx][ny] and grid[nx][ny]==0:
                    arrive = cur + 1
                    # 必须保证人到达时，火还没到（或永远不会到）
                    if fire_time[nx][ny]==-1 or arrive < fire_time[nx][ny]:
                        visited[nx][ny] = True
                        q.append((nx,ny,arrive))
        return False

    # 线性枚举等待时间（暴力）
    t = 0
    while True:
        if can_reach(t):
            t += 1
        else:
            return t-1    # 上一个可行的 t
```

> **关键行中文注释** 已在代码中给出。  

#### 复杂度  

- **时间复杂度**：`O(t_max · m·n)`  
  - `t_max` 为我们枚举的最大等待时间（最坏可达 `10^9`），每次检查都需要一次 `O(m·n)` 的 BFS。  
  - 用大白话说，就是“等一分钟再检查一次”，如果要等上千分钟，就要跑上千遍全图搜索，根本跑不完。  

- **空间复杂度**：`O(m·n)`  
  - 需要保存火焰到达时间的二维数组和 BFS 的访问标记。  

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于 **“等多少分钟”** 被线性枚举。  
实际上，**等待时间的取值空间是单调的**：  
- 若在等待 `t` 分钟后能够安全到达终点，那么 **所有 ≤ t 的等待时间也一定安全**（因为我们可以提前出发）。  
- 反之，若 `t` 不行，则所有 > t 也不行。  

这正好满足 **二分查找** 的前提：单调性。我们可以把“最大可等待时间”用二分法快速定位。  

二分查找需要一个 **判定函数** `canReach(t)`，它判断在等待 `t` 分钟后，是否仍然可以从 `(0,0)` 到达 `(m-1,n-1)`。  
如何高效实现这个判定？

> **关键观察**：  
> 对于任意格子 `(x,y)`，我们只关心 **火焰最早到达的时间** `fire[x][y]`。  
> - 如果 `fire[x][y] = -1`，说明火永远到不了（被墙围住）。  
> - 否则，火在 `fire[x][y]` 分钟时进入该格。  

只要我们提前算出所有格子的 `fire` 时间，就可以在判定时 **直接比较** 人到达时间与火的到达时间，而不必每次都重新模拟火的蔓延。  

**如何求 fire 时间？**  
- 多源 BFS（Multi‑source BFS）：把所有初始为 `2`（火源）的格子一次性放入队列，视作第 `0` 分钟已经着火。随后像普通 BFS 那样层层展开，每层对应火蔓延的 1 分钟。  
- 这一步的时间复杂度是 `O(m·n)`，只需做一次。

**判定函数 `canReach(t)`**  
- 从起点出发，使用 BFS 同时记录走到每个格子的时间 `dist[x][y]`（即人走了多少步）。  
- 对每个邻居格子 `(nx,ny)`，只有在满足 `dist[x][y] + 1 < fire[nx][ny]`（若 fire 为 -1 直接通过）时才可以进入。  
- 若 BFS 能够到达右下角，则 `t` 可行。  

**二分搜索的边界**  
- **左边界** `lo = 0`（最少等 0 分钟）。  
- **右边界** `hi = m*n` 或更大。因为每走一步最多需要 `m+n-2` 步，而火蔓延速度相同，最大的安全等待时间不可能超过格子总数的上限。  
- 题目中若 **永远安全**（火被墙完全阻隔），返回 `10^9`。我们可以在求完 `fire` 时间后检查：如果 `fire[m-1][n-1] == -1`（安全屋永不被火覆盖）且 `fire[0][0] == -1`（起点也不被火覆盖），则直接返回 `10^9`。  

**整体流程**  

1. **多源 BFS** 计算 `fire` 时间矩阵。  
2. **特殊情况**：若终点永不被火覆盖且起点也永不被火覆盖 → 返回 `10^9`。  
3. **二分查找** `t`：  
   - 中点 `mid = (lo+hi)//2`。  
   - 调用 `canReach(mid)`（一次 BFS）判断可行性。  
   - 若可行 → `lo = mid + 1`（尝试更久的等待）。  
   - 否则 → `hi = mid - 1`。  
4. 最终答案为 `hi`（最大可等待的分钟数），若 `hi < 0` 则返回 `-1`（根本不可达）。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def maximumMinutes(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    INF = 10**9
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    # ---------- 1. 多源 BFS 计算每个格子被火最早点燃的时间 ----------
    fire_time = [[INF] * n for _ in range(m)]          # INF 表示永远不会被火点燃
    q = deque()
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:                        # 初始火源
                fire_time[i][j] = 0
                q.append((i, j))

    while q:
        x, y = q.popleft()
        cur = fire_time[x][y]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] != 1 and fire_time[nx][ny] == INF:
                fire_time[nx][ny] = cur + 1
                q.append((nx, ny))

    # ---------- 2. 检查是否永远安全 ----------
    # 如果终点永不被火覆盖，则不管等多久都能到达（因为火永远进不来）
    if fire_time[m-1][n-1] == INF:
        return INF

    # ---------- 3. 判定函数：给定等待时间 t，是否还能安全到达 ----------
    def canReach(t: int) -> bool:
        # 人的 BFS，记录到达每个格子的时间（步数）
        q = deque()
        visited = [[False] * n for _ in range(m)]

        # 起点必须在等待 t 分钟后仍未被火点燃
        if t >= fire_time[0][0]:
            return False
        q.append((0, 0, 0))          # (x, y, steps 已经走的步数)
        visited[0][0] = True

        while q:
            x, y, steps = q.popleft()
            # 若已经到达安全屋，直接返回 True
            if (x, y) == (m-1, n-1):
                return True

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < m and 0 <= ny < n):
                    continue
                if visited[nx][ny] or grid[nx][ny] != 0:
                    continue
                arrive = steps + 1                # 人走到该格子的时间（不包括前面的等待 t）
                # 火在 fire_time[nx][ny] 分钟到达；人必须在火之前进入
                if arrive + t < fire_time[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny, steps + 1))
        return False

    # ---------- 4. 二分搜索最大可等待时间 ----------
    lo, hi = 0, m * n          # 上界取 m*n 足够大
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if canReach(mid):
            ans = mid
            lo = mid + 1       # 试更大的等待时间
        else:
            hi = mid - 1

    return ans
```

**代码要点说明**  

- `fire_time` 初始为 `INF`（相当于“永远不会着火”），用 `grid[i][j] != 1` 排除墙体。  
- `canReach(t)` 中 `arrive + t` 表示 **从 0 时刻算起** 人实际到达该格子的全局时间（等待 + 行走）。  
- 二分的右边界取 `m*n`（约 9e4），足够覆盖所有可能的最大等待时间；如果实际最大等待时间更大，说明火永远不威胁到终点，已在第 2 步返回 `10^9`。  

#### 复杂度  

- **时间复杂度**：`O(m·n·log(m·n))`  
  - 多源 BFS 计算 `fire_time`：`O(m·n)`。  
  - 二分查找最多 `log(m·n)` 次，每次内部 BFS 同样是 `O(m·n)`。  
  - 用大白话说，就是“先遍历一次全图得到火的到达时间，然后再用二分把等待时间的范围压缩，每次检查仍需遍历全图一次”。相比暴力的 `O(t_max·m·n)`，这里的 `log` 让时间下降了几个数量级。  

- **空间复杂度**：`O(m·n)`  
  - `fire_time`、`visited`、队列等均是和格子数同阶的二维数组或队列。  

---

## 心得  

- **核心技巧**：**多源 BFS + 二分查找**。先一次性求出“火的最早到达时间”，再利用单调性通过二分快速定位最大安全等待时间。  
- **适用的题型**  
  1. **“最晚出发时间”** 类问题，如 “Maximum Number of Days You Can Wait for the Pandemic to End”。  
  2. **“最早/最晚到达时间”** 与 **障碍扩散** 结合的题目，例如 “Escape the Flood”。  
  3. **路径安全性** 判断，配合 **时间层面的限制**（如 “Fire Escape Routes”）。  
- **一句话总结解题钥匙**：*把“火”视作另一条 BFS，先算出它的时间表，再在这张时间表上二分搜索“最迟出发”。*  

---

## 反思  

- **拿到题目第一反应**：先想 “先模拟火的蔓延，再模拟人走路”，于是想到暴力的逐分钟枚举。  
- **最容易踩的坑**  
  1. **火和人同时移动的顺序**：题目要求“先人移动，再让火蔓延”，实现时要注意把等待时间 `t` 加在人的到达时间上，而不是直接把 `t` 当作火的起始时间。  
  2. **边界条件**：起点或终点被墙围住、火永远到不了某格（`INF`）时的判断必须准确，否则会误判返回 `-1` 或 `10^9`。  
  3. **二分上界**：若直接设为 `10^9`，会导致 `canReach` 中的比较出现整数溢出或不必要的循环。取 `m*n` 这样与网格规模同阶的上界更安全。  
- **下次遇到同类题**：第一步先 **求出所有障碍（火、洪水、毒气）到达每个格子的最早时间**（多源 BFS），随后 **在这张时间表上做二分或直接 BFS 判定**，而不是盲目枚举等待或移动次数。