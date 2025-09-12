# #3342. 到达最后一个房间的最小时间 II / Find Minimum Time to Reach Last Room II

> 难度：中等 · 标签：Array、Graph、Heap (Priority Queue)、Matrix、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/find-minimum-time-to-reach-last-room-ii/)

---

## 题目（英文原版）

**Description**

There is a dungeon with n x m rooms arranged as a grid.
You are given a 2D array moveTime of size n x m, where moveTime[i][j] represents the minimum time in seconds when you can start moving to that room. You start from the room (0, 0) at time t = 0 and can move to an adjacent room. Moving between adjacent rooms takes one second for one move and two seconds for the next, alternating between the two.
Return the minimum time to reach the room (n - 1, m - 1).
Two rooms are adjacent if they share a common wall, either horizontally or vertically.

**Examples**

**Example 1:**

```
Input: moveTime = [[0,4],[4,4]]
Output: 7
Explanation:
The minimum time required is 7 seconds.
```

**Example 2:**

```
Input: moveTime = [[0,0,0,0],[0,0,0,0]]
Output: 6
Explanation:
The minimum time required is 6 seconds.
```

**Example 3:**

```
Input: moveTime = [[0,1],[1,2]]
Output: 4
```

**Constraints**

- 2 <= n == moveTime.length <= 750
- 2 <= m == moveTime[i].length <= 750
- 0 <= moveTime[i][j] <= 109

---

## 题目（中文翻译）

有一个由 `n × m` 个房间组成的地下城，房间按照网格排列。  
给定一个大小为 `n × m` 的二维数组 `moveTime`，其中 `moveTime[i][j]` 表示 **可以开始移动到该房间的最早时间**（单位：秒）。  
你从房间 `(0, 0)` 出发，初始时间 `t = 0`，可以向相邻的房间移动。相邻的房间是指在水平或垂直方向上共享公共墙壁的房间。  
在两次移动之间，移动所需的时间交替变化：第一次移动耗时 **1 秒**，第二次移动耗时 **2 秒**，随后再一次 **1 秒**，再一次 **2 秒**，如此交替。  

返回到达房间 `(n‑1, m‑1)` 的 **最小时间**。

---

## 示例

### 示例 1  
**输入**  
```text
moveTime = [[0,4],[4,4]]
```  
**输出**  
```text
7
```  
**解释**  
最短需要 7 秒即可到达终点。

### 示例 2  
**输入**  
```text
moveTime = [[0,0,0,0],[0,0,0,0]]
```  
**输出**  
```text
6
```  
**解释**  
最短需要 6 秒即可到达终点。

### 示例 3  
**输入**  
```text
moveTime = [[0,1],[1,2]]
```  
**输出**  
```text
4
```  

---

## 约束条件

- `2 ≤ n == moveTime.length ≤ 750`
- `2 ≤ m == moveTime[i].length ≤ 750`
- `0 ≤ moveTime[i][j] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的走法都穷举一遍**，然后把每条走法算出需要的时间，取最小值。  
可以用递归（DFS）或 BFS（层序遍历）来生成从左上角 `(0,0)` 到右下角 `(n‑1,m‑1)` 的每一条路径：

1. 在当前格子记录已经走了多少步（用来判断本次移动是 1 秒还是 2 秒）。  
2. 对四个相邻格子（上、下、左、右）尝试移动：  
   - 先看 `moveTime[next]`，如果当前时间 < `moveTime[next]`，就**等到** `moveTime[next]` 再出发。  
   - 根据步数的奇偶性决定本次移动的耗时（奇数步 1 秒，偶数步 2 秒）。  
   - 把得到的到达时间传给下一层递归。  
3. 当走到终点时，把这条路径的到达时间和全局最小值比较。

> **生活化类比**：  
> 把格子想成城市的十字路口，`moveTime[i][j]` 就像该路口的 **红灯时间**——只有等到红灯结束（时间≥`moveTime`）才能“开车”进入。  
> 步数的奇偶性则像道路的 **限速交替**：第一段路限速 1 秒/段，第二段限速 2 秒/段，交替进行。

**为什么这个方法一定能得到答案？**  
因为我们把 **所有** 合法的走法都枚举了，最短的那条自然会被找出来。只要实现没有遗漏，就不会错过最优解。

**时间/空间复杂度**（大白话）  
- **时间**：每走一步都有最多 4 种选择，最坏情况下会产生 `4^(n*m)` 条路径——相当于把所有可能的走法都写出来，根本不可能在电脑里跑完。  
- **空间**：递归栈的深度最多是格子数 `n*m`，再加上保存路径的临时数组，最坏也要 `O(n*m)` 的空间。

显然，这种 **暴力搜索** 只适合格子数极少（比如 2×2、3×3）的小例子，面对题目给出的 `750×750`，根本不可行。

#### 代码（Python）

```python
from math import inf
from typing import List

def minTime_bruteforce(moveTime: List[List[int]]) -> int:
    n, m = len(moveTime), len(moveTime[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    best = inf                         # 全局最小时间

    def dfs(x: int, y: int, step: int, cur_time: int, visited):
        """递归枚举所有路径，step 为已经走过的步数（从 0 开始）"""
        nonlocal best
        # 已经到达终点，更新答案
        if x == n - 1 and y == m - 1:
            best = min(best, cur_time)
            return
        # 剪枝：如果当前时间已经不可能比 best 更小，直接返回
        if cur_time >= best:
            return

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in visited:
                # 本次移动的耗时：奇数步 1 秒，偶数步 2 秒
                cost = 1 if step % 2 == 0 else 2
                # 必须等到目标格子允许进入的时间
                start = max(cur_time, moveTime[nx][ny])
                arrive = start + cost
                visited.add((nx, ny))
                dfs(nx, ny, step + 1, arrive, visited)
                visited.remove((nx, ny))

    dfs(0, 0, 0, 0, {(0, 0)})
    return best
```

> 这段代码可以在 `n,m ≤ 3` 时跑通，用来验证思路。但在大数据范围会直接卡死。

#### 复杂度  

- **时间复杂度**：`O(4^{n*m})`（指数级），相当于“穷举所有可能的走法”。  
- **空间复杂度**：`O(n*m)`（递归栈 + visited 集合），在最坏情况下要保存整张地图的坐标。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **两个导致慢的因素**：

1. **状态重复**：同一个格子可能会被多次访问，只是到达时走的步数（奇偶性）不同，导致后面的选择完全相同。  
2. **没有利用最短路的贪心特性**：我们每次都随意探索，根本不关心“现在的时间已经是最小的了吗”。

这正好可以用 **最短路算法**（Dijkstra）来改进。  
关键是把 **“步数的奇偶性”** 也放进状态里。我们把每个格子拆成 **两个子状态**：

| 状态 | 含义 |
|------|------|
| `(i, j, 0)` | 已经走了偶数步（下一步的移动耗时是 1 秒） |
| `(i, j, 1)` | 已经走了奇数步（下一步的移动耗时是 2 秒） |

这样，每一次从某个状态出发，**边的权重是确定的**（要么 1，要么 2），并且进入下一个格子时奇偶性会翻转。

**转移公式**（伪代码）：

```
cost = 1 if parity == 0 else 2               # 当前步的耗时
start = max(current_time, moveTime[nx][ny])   # 必须等到目标格子允许进入的时间
arrival = start + cost                        # 到达邻居的时间
next_parity = 1 - parity                       # 奇偶性翻转
```

因为所有边的权重都是正数，**Dijkstra** 能保证第一次弹出终点状态时的时间就是最小值。

**为什么只需要 2 * n * m 个节点就能描述全部情况？**  
每一次移动只会改变奇偶性，且不需要记忆更早的历史信息——只要知道当前的时间和奇偶性，就能唯一确定以后所有可能的花费。因此状态空间是 **线性的**，而不是指数级。

**数据结构类比**：  
- **哈希表**（字典）就像一本**电话簿**，`key` 是“格子 + 奇偶性”，`value` 是当前已知的最短时间。  
- **优先队列（堆）**像**医院的急诊队**，时间最早的患者会最先被叫出来检查（弹出）。

#### 代码（Python）

```python
import heapq
from typing import List

def minimumTime(moveTime: List[List[int]]) -> int:
    """
    Dijkstra + 双状态（奇偶步）求最短到达时间
    """
    n, m = len(moveTime), len(moveTime[0])
    INF = 10 ** 18

    # dist[i][j][p] 表示到达 (i,j) 并且已经走了 p 步（p=0 表示下一步耗时 1，p=1 表示下一步耗时 2）的最小时间
    dist = [[[INF, INF] for _ in range(m)] for _ in range(n)]
    dist[0][0][0] = 0                     # 起点，已走 0 步，下一步耗时 1

    # 小根堆，元素为 (当前时间, x, y, parity)
    heap = [(0, 0, 0, 0)]                 # (time, row, col, parity)

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while heap:
        cur_time, x, y, parity = heapq.heappop(heap)
        # 已经有更好的记录，直接跳过
        if cur_time != dist[x][y][parity]:
            continue

        # 到达终点并且是任意奇偶性时，即可返回（因为 Dijkstra 保证第一次弹出就是最小的）
        if x == n - 1 and y == m - 1:
            return cur_time

        move_cost = 1 if parity == 0 else 2   # 本次移动的耗时

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < n and 0 <= ny < m):
                continue

            # 必须等到目标格子允许进入的时间
            start_time = max(cur_time, moveTime[nx][ny])
            arrive_time = start_time + move_cost
            next_parity = 1 - parity           # 奇偶性翻转

            if arrive_time < dist[nx][ny][next_parity]:
                dist[nx][ny][next_parity] = arrive_time
                heapq.heappush(heap, (arrive_time, nx, ny, next_parity))

    # 理论上不会走到这里，因为一定能到达右下角
    return -1
```

**代码要点（中文注释）**：

- `dist` 用三维列表保存 **两种奇偶状态** 的最短时间。  
- `heap` 是 **优先队列**，每次弹出时间最小的状态，保证“贪心”是安全的。  
- `move_cost` 根据 `parity` 取 1 或 2，**奇偶交替**。  
- `start_time = max(cur_time, moveTime[nx][ny])` 实现 “等红灯” 的等待。  
- 当我们第一次弹出终点 `(n‑1,m‑1,*)` 时，即可返回，因为后面的任何路径都会更慢。

#### 复杂度  

- **时间复杂度**：`O( (n*m) * log(n*m) )`  
  - 图中有 `2 * n * m` 个节点，每个节点最多有 4 条出边。  
  - Dijkstra 用堆实现，每次弹出/插入的代价是 `log(节点数)`，即 `log(n*m)`。  
  - 大白话：即使是最大规模的 750×750（约 560,000 格子），也只会操作约 **一百万** 个状态，几秒内即可算完。  

- **空间复杂度**：`O( n * m )`  
  - `dist` 保存两倍的格子数，堆里最多也只会存同等数量的状态。  
  - 大白话：只需要几百 MB 以下的内存，完全可以在普通电脑上运行。

---

## 心得  

- **核心技巧**：**把“步数奇偶性”作为额外状态**，并在 Dijkstra 中使用它来决定每条边的权重。  
- **适用场景**（类似题目）  
  1. **交替费用的最短路**：如“每走一步费用在 1 与 2 之间交替”。  
  2. **带有时间窗口的网格最短路**：`moveTime` 类似红绿灯的放行时间。  
  3. **需要记忆有限历史信息的路径问题**：例如“上一次是否使用了特殊道具”之类的二元状态。  
- **一句话总结解题钥匙**：  
  > “把所有会影响后续选择的有限信息（这里是奇偶步）加入到状态中，再用 Dijkstra 求最短路。”

---

## 反思  

- **第一反应**：看到“交替 1 秒 / 2 秒”，马上想到**动态规划**，但忽视了 `moveTime` 的时间窗口限制，导致 DP 难以直接写出。  
- **最容易踩的坑**  
  1. **忘记等红灯**：`start_time = max(cur_time, moveTime[ni][nj])` 必不可少，直接用 `cur_time + cost` 会得到错误的更小答案。  
  2. **奇偶状态写反**：起始步数为 0（已走 0 步），下一步应当是 1 秒，而不是 2 秒。  
  3. **终点的奇偶性**：返回答案时不必区分奇偶，只要第一次弹出终点即可。  
- **下次遇到同类题的第一步**：  
  > “先问自己：除了位置之外，还有哪些‘小记忆’会影响后续的移动费用或可行性？把这些记忆加入到状态里，然后用最短路（Dijkstra）来求解。”