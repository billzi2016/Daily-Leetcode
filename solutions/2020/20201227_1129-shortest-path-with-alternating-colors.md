# #1129. 交替颜色的最短路径 / Shortest Path with Alternating Colors

> 难度：中等 · 标签：Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/shortest-path-with-alternating-colors/)

---

## 题目（英文原版）

**Description**

You are given an integer n, the number of nodes in a directed graph where the nodes are labeled from 0 to n - 1. Each edge is red or blue in this graph, and there could be self-edges and parallel edges.
You are given two arrays redEdges and blueEdges where:
Return an array answer of length n, where each answer[x] is the length of the shortest path from node 0 to node x such that the edge colors alternate along the path, or -1 if such a path does not exist.

**Examples**

**Example 1:**

```
Input: n = 3, redEdges = [[0,1],[1,2]], blueEdges = []
Output: [0,1,-1]
```

**Example 2:**

```
Input: n = 3, redEdges = [[0,1]], blueEdges = [[2,1]]
Output: [0,1,-1]
```

**Constraints**

- 1 <= n <= 100
- 0 <= redEdges.length, blueEdges.length <= 400
- redEdges[i].length == blueEdges[j].length == 2
- 0 <= ai, bi, uj, vj < n

---

## 题目（中文翻译）

给定一个整数 `n`，表示一个**有向图（directed graph）**的节点数，节点编号为 `0` 到 `n - 1`。图中的每条边要么是红色，要么是蓝色，图中可能存在**自环（self-edges）**和**平行边（parallel edges）**。  

另外给定两个数组 `redEdges` 和 `blueEdges`，分别列出所有红色边和蓝色边，其中 `redEdges[i] = [ui, vi]` 表示一条从节点 `ui` 到节点 `vi` 的红色有向边，`blueEdges[i] = [uj, vj]` 表示一条蓝色有向边。  

返回一个长度为 `n` 的数组 `answer`，其中 `answer[x]` 为从节点 `0` 到节点 `x` 的**最短路径（shortest path）**长度，且路径上相邻两条边的颜色必须交替（即红‑蓝‑红‑… 或蓝‑红‑蓝‑…）。如果不存在满足条件的路径，则对应位置的值为 `-1`。

**示例**

示例 1:  
输入: `n = 3, redEdges = [[0,1],[1,2]], blueEdges = []`  
输出: `[0,1,-1]`

示例 2:  
输入: `n = 3, redEdges = [[0,1]], blueEdges = [[2,1]]`  
输出: `[0,1,-1]`

**约束条件**

- `1 <= n <= 100`
- `0 <= redEdges.length, blueEdges.length <= 400`
- `redEdges[i].length == blueEdges[i].length == 2`
- `0 <= ui, vi, uj, vj < n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的路径**，找出满足「相邻边颜色交替」且长度最短的那条。可以用深度优先搜索（DFS）把从 `0` 出发的每一条路都走一遍：

1. 从当前节点 `u` 出发，遍历它的所有出边。  
2. 只把颜色和上一次走的颜色 **不同** 的边继续往下走（保证交替）。  
3. 把已经走过的节点和已经走过的「颜色」记下来，防止在同一次搜索里出现无限循环（比如自环）。  
4. 当到达目标节点 `x` 时，记录走过的步数，所有搜索结束后取最小值。

> **类比**：想象你在一座城市里走路，红灯和蓝灯分别对应两种道路。你只能在红灯路走完后再换到蓝灯路，反之亦然。暴力解相当于把城市里所有可能的走法都写下来，再挑出最短的那条。

这种做法 **一定能得到正确答案**，因为我们把所有合法路径都遍历了一遍，最短的必然在其中。

#### 代码（Python）

```python
from typing import List

def shortest_alternating_paths_brute(n: int,
                                     redEdges: List[List[int]],
                                     blueEdges: List[List[int]]) -> List[int]:
    # 建立邻接表，分别存红边和蓝边
    red_adj = [[] for _ in range(n)]
    blue_adj = [[] for _ in range(n)]
    for u, v in redEdges:
        red_adj[u].append(v)
    for u, v in blueEdges:
        blue_adj[u].append(v)

    # 保存每个节点的最短距离，初始为无限大（这里用 n+1 表示不可达）
    INF = n + 1
    ans = [INF] * n
    ans[0] = 0   # 0 到 0 的距离显然是 0

    # 用 DFS 暴力搜索所有合法路径
    def dfs(node: int, last_color: str, steps: int, visited: set):
        """
        node: 当前所在的节点
        last_color: 上一条走的边的颜色，'R'、'B' 或 None（起点）
        steps: 已经走了多少步
        visited: 已经访问过的 (node, last_color) 组合，防止在同一次搜索里循环
        """
        # 更新答案表
        if steps < ans[node]:
            ans[node] = steps

        # 根据上一次的颜色决定这一次只能走哪种颜色的边
        if last_color != 'R':          # 不能连续走红边
            for nxt in red_adj[node]:
                state = (nxt, 'R')
                if state not in visited:
                    visited.add(state)
                    dfs(nxt, 'R', steps + 1, visited)
                    visited.remove(state)   # 回溯，恢复 visited

        if last_color != 'B':          # 不能连续走蓝边
            for nxt in blue_adj[node]:
                state = (nxt, 'B')
                if state not in visited:
                    visited.add(state)
                    dfs(nxt, 'B', steps + 1, visited)
                    visited.remove(state)

    # 从起点 0 开始搜索，两种可能的「上一条颜色」都可以视为 None
    dfs(0, None, 0, set())

    # 把仍为 INF 的位置改成 -1 表示不可达
    return [-1 if d == INF else d for d in ans]
```

> **关键点注释**  
> - `red_adj` / `blue_adj`：分别保存红色、蓝色的有向边，像一本分颜色的“字典”。  
> - `visited`：防止在一次 DFS 里走回头路，类似“已经翻到的页码”。  
> - `last_color != 'R'`：只有上一次不是红色，才可以这一次走红色，确保颜色交替。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）。因为我们可能会在每个节点都有两种颜色的选择，最坏情况下会遍历所有长度 ≤ n 的路径，类似二叉树的节点数会指数增长。  
  > 大白话：如果节点很多，路径组合会像树枝一样不断分叉，数量会非常大，几乎不可能在短时间内跑完。

- **空间复杂度**：`O(n)` 用于存储邻接表和递归栈。  
  > 大白话：我们只需要把图的结构和递归过程中的少量信息保存在内存里，和节点数成正比。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**重复遍历相同的状态**。比如从 `0` 经过红边到 `1`，再经过蓝边回到 `0`，这和一开始就在 `0` 的状态是完全一样的，却会被再次搜索。我们只要记住「已经到达某个节点且上一次走的颜色是 X」这个**状态**就可以避免重复。

这正好可以用**广度优先搜索（BFS）**来实现：

1. **状态定义**：`(node, last_color)`。`last_color` 取值 `'R'`（红）或 `'B'`（蓝），表示到达 `node` 时最后一步用了哪种颜色。  
2. **起始层**：从节点 `0` 出发，有两种可能的「上一次颜色」——我们可以把它们视为 `None`，在 BFS 初始化时同时放入 `(0, 'R')` 和 `(0, 'B')`，距离设为 `0`。  
3. **层次遍历**：每次弹出队首状态，查看它能走的下一条边颜色（只能和 `last_color` 不同）。把未访问过的 `(next_node, new_color)` 加入队列，距离+1。  
4. **记录最短距离**：因为 BFS 按层展开，第一次到达某个节点（不管是红还是蓝）一定是最短路径。我们分别维护 `dist_red[i]`、`dist_blue[i]`，最后对每个 `i` 取最小的非负值即为答案。  

> **类比**：把「节点+上一次颜色」想成「城市的某个站台」，站台上有红线和蓝线两条轨道。我们每走一步，就换乘另一种颜色的轨道。BFS 就像公交系统的“层层递进”，先遍历所有乘坐 1 站的情况，再遍历 2 站的，以此类推，保证先到达的就是最短的。

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortestAlternatingPaths(n: int,
                             redEdges: List[List[int]],
                             blueEdges: List[List[int]]) -> List[int]:
    # 1. 建图：分别保存红边和蓝边的邻接表
    red_adj = [[] for _ in range(n)]
    blue_adj = [[] for _ in range(n)]
    for u, v in redEdges:
        red_adj[u].append(v)
    for u, v in blueEdges:
        blue_adj[u].append(v)

    # 2. dist_red[i] / dist_blue[i] 记录到达 i 时最后一步是红/蓝 的最短距离
    INF = float('inf')
    dist_red = [INF] * n
    dist_blue = [INF] * n
    dist_red[0] = dist_blue[0] = 0   # 起点到自身距离为 0

    # 3. BFS 队列里存 (node, last_color)
    #    last_color 用 0 表示红，1 表示蓝（方便放进整数元组）
    q = deque()
    q.append((0, 0))   # 假装前一步是红色，这样下一步只能走蓝边
    q.append((0, 1))   # 假装前一步是蓝色，这样下一步只能走红边

    while q:
        node, last = q.popleft()
        # 根据上一次的颜色决定这一次能走哪种颜色的边
        if last == 0:               # 上一次是红 → 这一次只能走蓝
            for nxt in blue_adj[node]:
                if dist_blue[nxt] == INF:          # 该状态未访问过
                    dist_blue[nxt] = dist_red[node] + 1
                    q.append((nxt, 1))
        else:                       # 上一次是蓝 → 这一次只能走红
            for nxt in red_adj[node]:
                if dist_red[nxt] == INF:
                    dist_red[nxt] = dist_blue[node] + 1
                    q.append((nxt, 0))

    # 4. 合并两种颜色的距离，取最小值；不可达则为 -1
    answer = []
    for i in range(n):
        best = min(dist_red[i], dist_blue[i])
        answer.append(-1 if best == INF else best)
    return answer
```

> **关键行解释**  
> - `dist_red[0] = dist_blue[0] = 0`：起点本身的距离是 0，且可以视为「上一次是红」也可以是「上一次是蓝」。  
> - `if dist_blue[nxt] == INF`：只在第一次到达 `(nxt, 蓝)` 时更新，防止后续再用更长的路径覆盖已经得到的最短距离。  
> - `dist_blue[nxt] = dist_red[node] + 1`：如果当前状态是「上一次红」，那么走蓝边后到达 `nxt` 的距离等于到 `node` 时的红色距离 + 1 步。

#### 复杂度

- **时间复杂度**：`O(n + E)`，其中 `E = len(redEdges) + len(blueEdges)`。  
  - 每个状态 `(node, color)` 最多进入队列一次（因为我们用 `dist_*` 判断是否已访问），所以最多遍历 `2 * n` 次。  
  - 对每个状态我们只遍历对应颜色的出边，总共遍历所有红边一次、所有蓝边一次。  
  > 大白话：我们只走一次所有的路，不会重复走同一段路，和把所有道路都一次性检查完的时间差不多。

- **空间复杂度**：`O(n + E)`。  
  - 邻接表需要存所有边。  
  - `dist_red / dist_blue` 各占 `O(n)`。  
  - BFS 队列最多同时装 `O(n)` 条状态。  
  > 大白话：除去存图的空间外，只用了和节点数量成正比的额外内存。

---

## 心得

- **核心技巧**：**把「颜色」当成状态，使用** **BFS** **在状态空间上搜索**。  
- **适用的题型**  
  1. 「交替颜色的最短路径」系列（如 LeetCode 1129）。  
  2. 「奇偶层次图」或「带限制的最短路径」问题（例如只能走奇数/偶数编号的边）。  
  3. 「带方向或权重限制的 BFS」如「只能在晴天或雨天行驶的道路」等。  
- **一句话总结**：**把「上一次的颜色」加入状态，用 BFS 按层展开，即可一次性得到所有交替路径的最短距离。**

---

## 反思

- **第一反应**：看到「交替颜色」就想到「每走一步必须换一种颜色」，于是直接想用 DFS 把所有路径列举出来。  
- **最容易踩的坑**  
  - **忘记记录颜色状态**：只以节点为状态会导致错误的路径被接受。  
  - **自环和并行边**：需要在邻接表里完整保存所有边，不能把自环直接忽略。  
  - **起点的颜色处理**：`0` 到 `0` 的距离是 `0`，但起点可以视作「上一次是红」也可以是「上一次是蓝」，否则会少走第一步。  
- **下次遇到同类题**：**第一步就把「额外限制」抽象成状态变量**（如颜色、奇偶、是否使用过某条边），然后在 BFS/DFS 中把状态一起放进队列或递归参数。这样既能避免重复搜索，又能保证最短路径。