# #2045. 第二短到达目的地的时间 / Second Minimum Time to Reach Destination

> 难度：困难 · 标签：Breadth-First Search、Graph、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/second-minimum-time-to-reach-destination/)

---

## 题目（英文原版）

**Description**

A city is represented as a bi-directional connected graph with n vertices where each vertex is labeled from 1 to n (inclusive). The edges in the graph are represented as a 2D integer array edges, where each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi. Every vertex pair is connected by at most one edge, and no vertex has an edge to itself. The time taken to traverse any edge is time minutes.
Each vertex has a traffic signal which changes its color from green to red and vice versa every change minutes. All signals change at the same time. You can enter a vertex at any time, but can leave a vertex only when the signal is green. You cannot wait at a vertex if the signal is green.
The second minimum value is defined as the smallest value strictly larger than the minimum value.
Given n, edges, time, and change, return the second minimum time it will take to go from vertex 1 to vertex n.
Notes:

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[1,2],[1,3],[1,4],[3,4],[4,5]], time = 3, change = 5
Output: 13
Explanation:
The figure on the left shows the given graph.
The blue path in the figure on the right is the minimum time path.
The time taken is:
- Start at 1, time elapsed=0
- 1 -> 4: 3 minutes, time elapsed=3
- 4 -> 5: 3 minutes, time elapsed=6
Hence the minimum time needed is 6 minutes.

The red path shows the path to get the second minimum time.
- Start at 1, time elapsed=0
- 1 -> 3: 3 minutes, time elapsed=3
- 3 -> 4: 3 minutes, time elapsed=6
- Wait at 4 for 4 minutes, time elapsed=10
- 4 -> 5: 3 minutes, time elapsed=13
Hence the second minimum time is 13 minutes.
```

**Example 2:**

```
Input: n = 2, edges = [[1,2]], time = 3, change = 2
Output: 11
Explanation:
The minimum time path is 1 -> 2 with time = 3 minutes.
The second minimum time path is 1 -> 2 -> 1 -> 2 with time = 11 minutes.
```

**Constraints**

- 2 <= n <= 104
- n - 1 <= edges.length <= min(2 * 104, n * (n - 1) / 2)
- edges[i].length == 2
- 1 <= ui, vi <= n
- ui != vi
- There are no duplicate edges.
- Each vertex can be reached directly or indirectly from every other vertex.
- 1 <= time, change <= 103

---

## 题目（中文翻译）

**描述**  
一座城市可以抽象为一个 **双向连通图**（bidirectional connected graph），图中有 `n` 个顶点（vertex），编号为 `1` 到 `n`（含）。图的边用二维整数数组 `edges` 表示，其中 `edges[i] = [ui, vi]` 表示顶点 `ui` 与顶点 `vi` 之间存在一条 **双向边**（bidirectional edge）。任意一对顶点至多只有一条边，且不存在自环。 traversing 任意一条边所需的时间为 `time` 分钟。

每个顶点都有一个交通信号灯（traffic signal），该信号灯每隔 `change` 分钟会在 **绿灯**（green）和 **红灯**（red）之间切换一次，所有信号灯同时切换。你可以在任意时刻进入一个顶点，但只能在信号灯为绿灯时离开该顶点；如果信号灯为绿灯，你不能在该顶点等待。

**第二最小值**（second minimum value）定义为严格大于最小值的最小值。

给定 `n`、`edges`、`time` 和 `change`，返回从顶点 `1` 到顶点 `n` 所需的 **第二最短时间**（second minimum time）。

---

### 示例

**示例 1**  
```text
Input: n = 5, edges = [[1,2],[1,3],[1,4],[3,4],[4,5]], time = 3, change = 5
Output: 13
Explanation:
左图展示了给定的图。
右图中蓝色路径是最短时间路径，所需时间为：
- 从 1 出发，已用时间 = 0
- 1 → 4：3 分钟，已用时间 = 3
- 4 → 5：3 分钟，已用时间 = 6
因此最短时间为 6 分钟。

红色路径展示了 …（此处原文已截断）  
```

**示例 2**  
```text
Input: n = 2, edges = [[1,2]], time = 3, change = 2
Output: 11
Explanation:
最短时间路径为 1 → 2，耗时 3 分钟。  
第二最短时间路径为 1 → 2 → 1 → 2，耗时 11 分钟。
```

---

### 约束条件
- `2 <= n <= 10^4`
- `n - 1 <= edges.length <= min(2 * 10^4, n * (n - 1) / 2)`
- `edges[i].length == 2`
- `1 <= ui, vi <= n`
- `ui != vi`
- 不存在重复的边。
- 任意两个顶点之间都可以直接或间接到达（图是连通的）。
- `1 <= time, change <= 10^3`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举出来**，记录每一种从 `1` 到 `n` 的走法需要的时间，然后把所有时间排序，取第二小的那个。  

- **枚举走法**：可以用深度优先搜索（DFS）或广度优先搜索（BFS）把从起点出发的每一条路径都走一遍。  
- **记录时间**：每走完一条边就把 `time` 加进去；如果此时信号灯是红灯，还要等到下一次绿灯再出发（等的时间可以用 `mod` 运算算出来）。  
- **取第二小**：把所有得到的总时间放进列表，排序后取下标为 `1` 的元素（下标从 `0` 开始），这就是“第二小”。  

> **类比**：把城市想象成一张大地图，想要找出 **所有** 从 A 城到 B 城的路线，就像把所有可能的旅行路线都写在纸上，再逐一算时间，最后挑出第二快的那条。  

**为什么这种方法是正确的？**  
只要把 **所有** 合法走法都遍历完，必然能够得到所有可能的到达时间，其中最小的就是最短时间，第二小的就是题目要求的第二最短时间。

**复杂度分析（大白话）**  

- **时间复杂度**：  
  - 每条路径的长度最多可能是 `O(n)`（最坏情况下要把所有节点都走一遍再回头），  
  - 而可能的路径数是指数级的（每个节点都有多条出路），所以总体是 **指数级**，记作 `O(2^n)`，在 `n` 达到几千甚至几百时根本不可行。  
- **空间复杂度**：  
  - 需要保存递归栈（或队列）以及所有已经算好的时间，最坏也会是指数级，记作 `O(2^n)`。  

> **结论**：暴力枚举在本题的约束（`n ≤ 10^4`）下根本跑不完，只能用来帮助我们理解问题。

#### 代码（Python）

```python
from collections import defaultdict, deque

def secondMinimum_bruteforce(n, edges, time, change):
    # 建图：邻接表，key 像字典里查词一样，value 是相邻的节点列表
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 用 BFS（层序遍历）把所有路径都枚举出来
    # queue 中保存 (当前节点, 已经走的时间, 已走的路径)
    q = deque()
    q.append((1, 0, [1]))
    all_times = []          # 用来收集所有合法的到达时间

    while q:
        node, cur_t, path = q.popleft()
        # 如果已经到了终点，就把这条路径的总时间保存下来
        if node == n:
            all_times.append(cur_t)
            continue

        # 为防止走无限长的环，这里做了非常粗糙的剪枝：只允许路径长度不超过 2*n
        if len(path) > 2 * n:
            continue

        for nxt in graph[node]:
            # 计算从 cur_t 出发走到 nxt 需要的等待时间
            # 信号灯周期 = 2*change，前 change 分钟绿灯，后 change 分钟红灯
            period = 2 * change
            if (cur_t // change) % 2 == 0:          # 现在是绿灯
                depart = cur_t                     # 立刻出发
            else:                                   # 现在是红灯
                wait = period - (cur_t % period)   # 等到下一个绿灯
                depart = cur_t + wait

            next_t = depart + time                  # 再加上走一条边的固定时间
            q.append((nxt, next_t, path + [nxt]))

    # 把所有时间排个序，第二小的就是答案
    all_times.sort()
    return all_times[1]          # 因为题目保证至少有两条不同的到达时间
```

> **注意**：这段代码只能在非常小的测试里跑通，真正的题目数据会让它直接超时或内存炸掉。

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 指数级增长，等价于“每走一步都有好几条分支，分支数会翻倍”。  
- **空间复杂度**：`O(2^n)` —— 需要保存所有可能的路径和时间，同样是指数级。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈** 出在**枚举所有路径**。实际上我们只需要知道 **到每个节点的前两条最短到达时间**，因为：

- 若已经得到节点 `v` 的最短时间 `d1[v]` 和第二短时间 `d2[v]`，  
- 那么从 `v` 出发继续前进时，只会产生 **不超过两条** 对应的到达时间（分别使用 `d1[v]` 或 `d2[v]` 作为出发时间），  
- 这正好满足我们只关心 **全局的第二短时间** 的需求。

因此我们可以把问题转化为 **“在图上寻找每个节点的两条最短到达时间”**，这正好可以用 **改进的 Dijkstra / BFS** 来实现：

1. **数据结构**  
   - 用 **邻接表** 存图（类似字典里查词）。  
   - 用 **优先队列（最小堆）** 按当前已知的到达时间从小到大弹出节点，这样先处理的总是“更早能到达”的状态。  
   - 对每个节点维护两个变量 `first[node]`、`second[node]`，分别保存最短和第二短到达时间（初始为无穷大）。  

2. **信号灯的等待时间**  
   - 设当前时间为 `t`，信号灯周期 `P = 2 * change`。  
   - 如果 `t % P < change`，说明此时是绿灯，可以立刻离开。  
   - 否则是红灯，需要等 `P - (t % P)` 分钟才会变绿。  
   - 这一步只和当前时间有关，**不需要额外的状态**，直接在计算下一条边的到达时间时加上等待时间即可。  

3. **核心循环**（伪代码）  

```
push (0, 1) into heap          # (当前时间, 当前节点)
while heap not empty:
    cur_time, u = pop smallest
    if second[n] 已经确定且 cur_time > second[n]:  # 已经找到了第二短，后面的更大可以直接跳过
        continue

    for each neighbor v of u:
        depart = cur_time
        if (depart // change) % 2 == 1:          # 红灯，需要等
            depart += (2*change - depart % (2*change))

        arrive = depart + time                     # 走完这条边的时间

        # 更新 v 的第一、第二最短时间
        if arrive < first[v]:
            second[v] = first[v]
            first[v] = arrive
            push (arrive, v)
        elif first[v] < arrive < second[v]:
            second[v] = arrive
            push (arrive, v)
```

4. **为什么只需要两条最短时间**  
   - 对于任意一次“从 `u` 到 `v`”的移动，只会基于 `u` 的 **最早** 或 **次早** 到达时间产生新的到达时间。  
   - 如果我们已经拥有 `v` 的两条最短时间，后续任何更慢的到达时间都不可能成为全局的第二短（因为已经有更快的两条）。  
   - 这就是 **“只保留前两名”** 的剪枝依据，能够把搜索空间压到 `O(E)`（每条边最多被松弛两次）。  

5. **时间/空间复杂度**  

   - 每条边最多被处理 **两次**（一次对应最短时间，一次对应第二短时间），每次操作都是堆的 `push/pop`，时间复杂度为 `O((V + E) log V)`。在本题 `V ≤ 10^4`、`E ≤ 2·10^4`，完全可接受。  
   - 只需要保存 `first`、`second` 两个数组以及邻接表，空间为 `O(V + E)`。  

#### 代码（Python）

```python
import heapq
from collections import defaultdict
from typing import List

def secondMinimum(n: int, edges: List[List[int]], time: int, change: int) -> int:
    """
    使用改进的 Dijkstra（每个节点保留最短和次短两条到达时间）。
    关键点：
    1) 计算离开当前节点的等待时间（红灯要等）。
    2) 对每个节点只维护两条最短时间，避免指数级搜索。
    """

    # ---------- 1. 建图 ----------
    graph = defaultdict(list)          # 类似字典查词，key 是节点，value 是相邻节点列表
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    INF = 10**18
    first = [INF] * (n + 1)   # 第一次最短到达时间
    second = [INF] * (n + 1)  # 第二次最短到达时间
    first[1] = 0

    # ---------- 2. 优先队列 ----------
    # 堆里存 (当前已知的到达时间, 节点编号)
    heap = [(0, 1)]

    # ---------- 3. 主循环 ----------
    while heap:
        cur_t, u = heapq.heappop(heap)

        # 已经得到终点的第二短且当前弹出的时间更大，说明后面的都不可能更小，直接结束
        if u == n and cur_t > second[n]:
            continue

        # 对每一条出边尝试松弛
        for v in graph[u]:
            depart = cur_t
            # ---------- 3.1 计算是否需要等红灯 ----------
            period = 2 * change               # 一个完整的绿-红周期
            if (depart // change) % 2 == 1:   # 现在是红灯，需要等到下一个绿灯
                wait = period - (depart % period)
                depart += wait                # 等待后才离开

            arrive = depart + time             # 走完这条边的时间

            # ---------- 3.2 更新 v 的第一、第二最短时间 ----------
            if arrive < first[v]:
                # 新的最短时间出现，原来的最短变成第二短
                second[v] = first[v]
                first[v] = arrive
                heapq.heappush(heap, (arrive, v))
            elif first[v] < arrive < second[v]:
                # 介于最短和第二短之间的合法时间
                second[v] = arrive
                heapq.heappush(heap, (arrive, v))

    # 第二短时间一定会被填满（题目保证有解）
    return second[n]
```

> **代码要点说明**  
> - 第 10 行的 `graph` 用 `defaultdict(list)`，相当于“查字典”，把每个城市的相邻道路列出来。  
> - 第 24 行的 `period = 2 * change` 表示 **一次完整的绿灯+红灯循环**。  
> - 第 27‑30 行判断当前是否是红灯，如果是则算出还要等多少分钟 `wait`，再把 `depart` 加上等待时间。  
> - 第 38‑45 行只保留 **前两条** 到达时间，超过的直接丢弃，保证搜索规模是线性的。

#### 复杂度  

- **时间复杂度**：`O((V + E) log V)`  
  - 每条边最多被松弛两次（一次对应最短，一次对应次短），每次操作堆的插入/弹出是 `log V`。  
  - 对于本题的最大规模（`V = 10^4, E = 2·10^4`），运行毫秒级即可。  
- **空间复杂度**：`O(V + E)`  
  - `first`、`second` 两个长度为 `V+1` 的数组 + 邻接表（存每条边两次），不随搜索深度增长。  

---

## 心得  

- **核心技巧**：**在最短路问题中只保留每个节点的前两条最短到达时间**（也叫 “第二最短路”），配合 **优先队列**（Dijkstra）即可在 `O((V+E) log V)` 完成。  
- **适用的题型**（类似思路）  
  1. “第二短的路径” (`Second Minimum Path`)  
  2. “K 条最短路径” 中的 `K=2` 情形  
  3. “在有时间窗/信号灯限制的最短路”——需要在每次松弛时加入额外的等待时间计算。  
- **一句话总结解题钥匙**：**只要每个节点记录两次到达时间，使用 Dijkstra 的框架逐层展开，就能在不枚举所有路径的情况下直接得到全局的第二最短时间。**  

---

## 反思  

- **第一反应**：看到“第二最小时间”，本能想到 **枚举所有路径**，因为最直接的办法就是把所有时间列出来再挑第二个。  
- **最容易踩的坑**  
  1. **红灯等待的计算**：忘记 `period = 2*change`，或者把 “绿灯时仍需等” 的情况写错，导致时间不对。  
  2. **重复访问导致无限循环**：如果不限制每个节点只保留两条时间，搜索会像暴力解一样爆炸。  
  3. **边界条件**：起点和终点的信号灯也要遵守同样规则，尤其起点 `time=0` 必须先判断是否绿灯（题目保证 0 时是绿灯）。  
- **下次遇到同类题**：第一步立刻想到 **“对每个节点维护前 K 条最短到达时间”**（这里 K=2），然后在 Dijkstra / BFS 中加入 **状态转移的额外费用**（如等待、费用上限等），这样可以把搜索空间压到线性级别。