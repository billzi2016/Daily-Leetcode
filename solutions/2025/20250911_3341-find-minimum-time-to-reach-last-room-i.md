# #3341. 寻找到达最后一个房间的最小时间 I / Find Minimum Time to Reach Last Room I

> 难度：中等 · 标签：Array、Graph、Heap (Priority Queue)、Matrix、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/find-minimum-time-to-reach-last-room-i/)

---

## 题目（英文原版）

**Description**

There is a dungeon with n x m rooms arranged as a grid.
You are given a 2D array moveTime of size n x m, where moveTime[i][j] represents the minimum time in seconds after which the room opens and can be moved to. You start from the room (0, 0) at time t = 0 and can move to an adjacent room. Moving between adjacent rooms takes exactly one second.
Return the minimum time to reach the room (n - 1, m - 1).
Two rooms are adjacent if they share a common wall, either horizontally or vertically.

**Examples**

**Example 1:**

```
Input: moveTime = [[0,4],[4,4]]
Output: 6
Explanation:
The minimum time required is 6 seconds.
```

**Example 2:**

```
Input: moveTime = [[0,0,0],[0,0,0]]
Output: 3
Explanation:
The minimum time required is 3 seconds.
```

**Example 3:**

```
Input: moveTime = [[0,1],[1,2]]
Output: 3
```

**Constraints**

- 2 <= n == moveTime.length <= 50
- 2 <= m == moveTime[i].length <= 50
- 0 <= moveTime[i][j] <= 109

---

## 题目（中文翻译）

**描述**  
有一个由 `n × m` 个房间组成的地牢（dungeon），这些房间以网格（grid）的形式排列。  
给定一个大小为 `n × m` 的二维数组 `moveTime`，其中 `moveTime[i][j]` 表示房间在 **最小时间**（以秒为单位）后才会打开并且可以进入。  
你从房间 `(0, 0)` 开始，初始时间 `t = 0`，并且可以移动到相邻房间（adjacent room）。在相邻房间之间移动恰好需要 **1 秒**。  
返回到达房间 `(n - 1, m - 1)` 的 **最小时间**。  

两个房间是相邻的，如果它们共享同一面墙，且方向为水平或垂直。

**示例**  

示例 1:  
```text
Input: moveTime = [[0,4],[4,4]]
Output: 6
Explanation:
最小所需时间为 6 秒。
```

示例 2:  
```text
Input: moveTime = [[0,0,0],[0,0,0]]
Output: 3
Explanation:
最小所需时间为 3 秒。
```

示例 3:  
```text
Input: moveTime = [[0,1],[1,2]]
Output: 3
```

**约束条件**  
- `2 ≤ n == moveTime.length ≤ 50`  
- `2 ≤ m == moveTime[i].length ≤ 50`  
- `0 ≤ moveTime[i][j] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的走法**，把从左上角走到右下角的每一条路径都算一遍，然后取最小的耗时。  
- **数据结构**：我们可以用**递归+回溯**来遍历路径，或者用**深度优先搜索（DFS）**的栈来模拟。  
- **生活化类比**：想象你在一个迷宫里，每走一步都要记录走了多久。你把所有可能的走法都画在纸上，最后挑出耗时最短的一条。  
- **正确性**：因为我们把**所有**合法路径都考虑到了，必然会包含最优路径，所以答案一定正确。  

> **为什么要遍历所有路径？**  
> 这里的限制条件是每个房间只能在 `moveTime[i][j]` 秒以后进入，而移动本身固定消耗 1 秒。只要我们在遍历时对每一步都计算“当前时间 + 1 与该房间开放时间的最大值”，就能得到这条路径的实际耗时。

#### 代码（Python）

```python
from typing import List

def minTime_bruteforce(moveTime: List[List[int]]) -> int:
    n, m = len(moveTime), len(moveTime[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # 四个方向

    best = float('inf')          # 记录全局最小时间

    def dfs(x: int, y: int, cur_time: int, visited: List[List[bool]]):
        nonlocal best
        # 已经到达终点
        if x == n - 1 and y == m - 1:
            best = min(best, cur_time)
            return
        # 剪枝：如果当前已经超过已知最小值，就不必继续搜索
        if cur_time >= best:
            return

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 判断是否越界或已经访问（防止死循环）
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
                # 进入相邻房间需要 1 秒，且必须等到该房间开放
                arrive = max(cur_time + 1, moveTime[nx][ny])
                visited[nx][ny] = True
                dfs(nx, ny, arrive, visited)
                visited[nx][ny] = False   # 回溯

    visited = [[False] * m for _ in range(n)]
    visited[0][0] = True
    # 起点的开放时间一定是 0（题目保证），所以初始时间为 0
    dfs(0, 0, 0, visited)
    return best
```

> **关键行中文注释**  
> - `arrive = max(cur_time + 1, moveTime[nx][ny])`：先走 1 秒，再等到房间开放。  
> - `if cur_time >= best: return`：如果已经比当前最优更慢，就直接剪掉这条分支，省时间。

#### 复杂度

- **时间复杂度**：`O(4^(n*m))`（指数级）  
  > 解释：每一步都有最多 4 条分支，最多走 `n*m` 步，所以搜索树的规模是 `4` 的 `n*m` 次方。对初学者来说可以想象成“每走一步都要翻 4 张卡片”，卡片数会非常爆炸，实际根本跑不完。

- **空间复杂度**：`O(n*m)`  
  > 解释：递归栈深度最多 `n*m`，以及 `visited` 数组占用同样大小的格子。

> **结论**：暴力解虽然思路最直观，却在中等规模（如 50×50）时完全不可行，需要更聪明的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**核心难点在于“每一步的实际到达时间取决于之前的路径”**，这正是**最短路**问题的典型特征。  
- **慢在哪里？**  
  - 暴力枚举所有路径导致指数级时间。  
  - 实际上我们只关心“从起点到每个格子的最早到达时间”，不需要记住完整路径。  

- **优化思路**  
  1. 把每个格子看成图中的一个节点。  
  2. 两个相邻格子之间有一条有向边，权重不是固定的 1，而是**`max(cur_time + 1, moveTime[neighbor])`**，即：从当前时间出发，走过去最少需要的时间。  
  3. 这正好可以使用**Dijkstra 最短路算法**（因为所有边的权重都是非负的）。  
  4. 为了高效挑选“当前最早到达的未处理节点”，我们使用**优先队列（最小堆）**。  

- **核心概念解释**  
  - **图**：把格子当成城市，把可以走的通道当成道路。  
  - **节点的最短距离**：从起点出发，最快能到达这个城市的时间。  
  - **优先队列（最小堆）**：像排队买票，时间最早的那个人会先被服务。这里我们把“当前已知的最早到达时间”放进去，堆顶永远是最小的。

- **算法步骤**  
  1. 初始化 `dist[i][j] = INF`，表示尚未得到最短时间。  
  2. `dist[0][0] = 0`，把起点加入堆 `heap = [(0, 0, 0)]`（(时间, x, y)）。  
  3. 循环取出堆顶 `(t, x, y)`：  
     - 如果 `(x, y)` 已经是终点，直接返回 `t`（因为 Dijkstra 保证第一次弹出的终点时间即为最短）。  
     - 否则遍历四个相邻格子 `(nx, ny)`：  
       - 计算进入该格子所需的实际时间 `nt = max(t + 1, moveTime[nx][ny])`。  
       - 如果 `nt < dist[nx][ny]`，说明找到更快的路径，更新 `dist` 并把 `(nt, nx, ny)` 推入堆。  
  4. 循环结束后，`dist[n-1][m-1]` 即为答案（理论上一定能到达）。

- **类比帮助理解**  
  想象你在城市里开车，路口有红绿灯（对应 `moveTime`），你到达路口时如果灯是红的，需要等到它变绿才能继续前进。Dijkstra 就像 GPS，它每次选择“当前离起点最近、且已经算好最短时间的路口”，然后继续往外扩展。

#### 代码（Python）

```python
import heapq
from typing import List

def minTime_dijkstra(moveTime: List[List[int]]) -> int:
    n, m = len(moveTime), len(moveTime[0])
    INF = 10**18
    # 最早到达每个格子的时间，初始为无限大
    dist = [[INF] * m for _ in range(n)]
    dist[0][0] = 0                     # 起点时间为 0

    # (已经走的时间, x, y) 放入最小堆
    heap = [(0, 0, 0)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while heap:
        cur_t, x, y = heapq.heappop(heap)

        # 如果弹出的时间已经不是最优的，直接跳过
        if cur_t != dist[x][y]:
            continue

        # 到达终点，直接返回
        if x == n - 1 and y == m - 1:
            return cur_t

        # 扩展四个方向
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                # 走过去需要 1 秒，若到达时房间尚未开放则必须等到它开放
                nxt_t = max(cur_t + 1, moveTime[nx][ny])
                if nxt_t < dist[nx][ny]:
                    dist[nx][ny] = nxt_t
                    heapq.heappush(heap, (nxt_t, nx, ny))

    # 根据题目约束，必定能到达，这行代码理论上不会被执行
    return dist[n-1][m-1]
```

> **关键行中文注释**  
> - `nxt_t = max(cur_t + 1, moveTime[nx][ny])`：先走 1 秒，再等到房间打开。  
> - `if cur_t != dist[x][y]: continue`：堆里可能会有“过时的”记录，直接丢弃，保证每个格子只用最短的时间继续扩展。  
> - `if x == n - 1 and y == m - 1: return cur_t`：第一次弹出终点时的时间就是最短答案，省去遍历剩余节点。

#### 复杂度

- **时间复杂度**：`O(n * m * log(n * m))`  
  > 解释：每个格子最多进入堆一次（或几次，但总的 push/pop 操作不超过 `4 * n * m`），堆的大小最多是 `n*m`，每次弹出或插入的代价是 `log(n*m)`。对 50×50 的网格来说，大约只需要几千次操作，完全可以在毫秒级跑完。

- **空间复杂度**：`O(n * m)`  
  > 解释：`dist` 数组和堆同时最多存储所有格子的信息，约占网格大小的两倍，仍然是线性空间。

> 与暴力解相比，时间从指数级降到了 **多项式级**（几乎线性），是可接受的最优解。

---

## 心得

- **核心技巧**：把“每一步要等到房间开放”转化为**带权图的最短路径**，使用 **Dijkstra + 最小堆** 求解。  
- **适用的题型**  
  1. **带有等待时间的网格最短路**（例如 LeetCode 1915 “Maximum Cost Deletion” 中的类似约束）。  
  2. **时间窗约束的路径问题**（如“在公交站等车”类题目）。  
  3. **带有动态权重的图搜索**（比如每条边的费用随时间变化）。  
- **一句话总结**：把“最早能进入的时间 = max(上一格时间+1, 当前格开放时间)”视作边权，交给 Dijkstra 完全搞定。

---

## 反思

- **第一反应**：直接想遍历所有路径或用 BFS 逐层搜索，却忽略了每个格子进入时间的**非均匀**特性，导致普通 BFS 不能直接使用。  
- **最容易踩的坑**  
  - **忘记取最大值**：`cur_time + 1` 与 `moveTime[nx][ny]` 必须取 `max`，否则会提前进入未开放的房间。  
  - **重复入堆导致的“过时记录”**：没有在弹出时检查 `cur_t != dist[x][y]`，会导致错误的答案或性能下降。  
  - **边界条件**：起点 `moveTime[0][0]` 可能不是 0（题目一般保证为 0），如果不是，需要先 `max(0, moveTime[0][0])`。  
- **下次遇到同类题**：第一步先思考“是否可以把每一步的代价抽象为图的边权”，如果能，用 **最短路（Dijkstra / SPFA / BFS+0-1）** 来求解，而不是盲目暴力搜索。