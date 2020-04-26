# #847. 遍历所有节点的最短路径 / Shortest Path Visiting All Nodes

> 难度：困难 · 标签：Dynamic Programming、Bit Manipulation、Breadth-First Search、Graph、Bitmask · [LeetCode 链接](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)

---

## 题目（英文原版）

**Description**

You have an undirected, connected graph of n nodes labeled from 0 to n - 1. You are given an array graph where graph[i] is a list of all the nodes connected with node i by an edge.
Return the length of the shortest path that visits every node. You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges.

**Examples**

**Example 1:**

```
Input: graph = [[1,2,3],[0],[0],[0]]
Output: 4
Explanation: One possible path is [1,0,2,0,3]
```

**Example 2:**

```
Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
Output: 4
Explanation: One possible path is [0,1,4,2,3]
```

**Constraints**

- n == graph.length
- 1 <= n <= 12
- 0 <= graph[i].length < n
- graph[i] does not contain i.
- If graph[a] contains b, then graph[b] contains a.
- The input graph is always connected.

---

## 题目（中文翻译）

你有一个 **无向图（undirected graph）**，该图是 **连通的（connected）**，共有 `n` 个节点，编号为 `0` 到 `n - 1`。给定一个数组 `graph`，其中 `graph[i]` 是一个列表，包含所有与节点 `i` 通过 **边（edge）** 相连的节点。

返回访问每个节点恰好一次的 **最短路径（shortest path）** 长度。你可以从任意节点开始和结束，节点可以被多次访问，边也可以被重复使用。

**示例 1**

> **输入**: `graph = [[1,2,3],[0],[0],[0]]`  
> **输出**: `4`  
> **解释**: 一条可能的路径是 `[1,0,2,0,3]`。

**示例 2**

> **输入**: `graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]`  
> **输出**: `4`  
> **解释**: 一条可能的路径是 `[0,1,4,2,3]`。

**约束条件**

- `n == graph.length`
- `1 <= n <= 12`
- `0 <= graph[i].length < n`
- `graph[i]` 中不包含 `i` 本身。
- 若 `graph[a]` 包含 `b`，则 `graph[b]` 也包含 `a`。
- 输入的图始终是连通的。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：先把图中每两个节点之间的最短距离算出来（因为图是无权的，用一次 BFS 就能得到），然后在这些距离的基础上枚举**所有可能的访问顺序**，找出走完所有节点的最短路径长度。  

- **图的存储**：用邻接表 `graph[i]` 表示第 `i` 个节点的所有相邻节点。可以把它想象成一本“社交网络通讯录”，每个人（节点）都有一张好友列表（邻居）。
- **全局最短距离**：对每个节点做一次 BFS，得到它到其它所有节点的最短步数。相当于在地图上先测好 **“从 A 到 B 最近要几步”**，就像我们在城市里先查好两点之间的最短驾车里程。
- **遍历所有访问顺序**：把 `n` 个节点的排列全部列出来（`n!` 种），每一种排列代表一种访问顺序。例如 `[2,0,3,1]` 表示先去 2，再去 0，接着 3，最后 1。对每个排列，把相邻两点的最短距离相加，得到这条路径的总长度。所有排列里取最小值，就是答案。

这种方法之所以**正确**，是因为我们把所有可能的走法都穷举了一遍，必然不会漏掉最优解。  

**复杂度大概是**：  
- 计算全局最短距离：`n` 次 BFS，每次 `O(E)`，整体 `O(n·E)`。  
- 枚举排列：`n!` 种，每种需要 `O(n)` 次查表相加。  
- 所以总体时间是 `O(n!·n)`，空间主要是存距离矩阵 `O(n²)`。  

> **大白话**：`O(n!·n)` 就是“先把所有可能的走法列出来（这一步会疯狂增长），然后每个走法再算一次总路程”。当 `n` 只有 12 以下时，`12! ≈ 479M`，已经不可能在合理时间内跑完。

#### 代码（Python）  

```python
from itertools import permutations
from collections import deque
from typing import List

def shortestPathLength_bruteforce(graph: List[List[int]]) -> int:
    n = len(graph)

    # ---------- 1. 预处理：所有点对的最短距离 ----------
    # dist[u][v] 表示 u 到 v 的最短步数
    dist = [[0] * n for _ in range(n)]

    for start in range(n):
        # 标准 BFS 求最短路径
        q = deque([start])
        visited = [-1] * n
        visited[start] = 0          # 到自己的距离是 0
        while q:
            cur = q.popleft()
            for nb in graph[cur]:
                if visited[nb] == -1:
                    visited[nb] = visited[cur] + 1
                    q.append(nb)
        dist[start] = visited       # 保存这一次 BFS 的结果

    # ---------- 2. 枚举所有访问顺序 ----------
    all_nodes = list(range(n))
    best = float('inf')

    # permutations 会生成 n! 种排列
    for order in permutations(all_nodes):
        # 计算该排列的总路径长度
        cur_len = 0
        for i in range(1, n):
            cur_len += dist[order[i - 1]][order[i]]
        best = min(best, cur_len)

    return best
```

> **关键注释**  
> - `dist[start] = visited` 把一次 BFS 的结果保存下来，后面查表只需要 O(1)。  
> - `for order in permutations(all_nodes)` 把所有可能的访问顺序都列出来。  

#### 复杂度  

- **时间复杂度**：`O(n!·n)`  
  - “`n!`” 表示所有排列的数量，随着节点数的增加会像炸弹一样快速增长。  
  - “`·n`” 是每条排列内部累计距离的代价。  
- **空间复杂度**：`O(n²)`  
  - 只需要存储 `n×n` 的距离矩阵，其他都是常数级空间。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**枚举所有排列**——这一步的复杂度是阶乘级别，根本不可接受。  

观察题目：  

1. 我们可以**从任意节点出发**，且**路径可以重复经过已经走过的节点**。  
2. 只要最终「已经访问过的节点集合」等于全部 `n` 个节点，就算成功。  

这两个特性让我们想到**在状态空间上做 BFS**：  
- **状态** = `(当前所在的节点, 已经访问过的节点集合)`。  
- 用 **位掩码（bitmask）** 来表示「已经访问过的集合」：因为 `n ≤ 12`，只需要 12 位就能装下每个节点是否已访问。比如 `mask = 0b0101` 表示节点 0 和 2 已经走过。  
- 从 **所有节点同时作为起点** 开始（多源 BFS），因为起点不固定。每个起点的初始状态是 `(i, 1 << i)`，即只访问了自己。  

**搜索过程**：  
- 每次从队列里弹出一个状态 `(u, mask)`，把它的所有邻居 `v` 作为下一层状态 `(v, mask | (1 << v))` 放进去。  
- `mask | (1 << v)` 的作用是把邻居 `v` 标记为「已访问」。这一步用位运算完成，速度极快。  
- BFS 按层展开，**第一次**碰到 `mask == (1 << n) - 1`（即所有 `n` 位都为 1）时，当前层数就是最短路径长度。因为 BFS 保证先到达的状态对应的路径是最短的。  

**为什么是最优的**：  
- 状态总数 = `n * 2^n`（每个节点对应 2^n 种访问集合），远远小于 `n!`。  
- 每条状态转移只看一次邻居，时间是 `O(E * 2^n)`，在 `n ≤ 12` 时最多约 `12 * 2^12 = 49152` 次操作，完全可以在毫秒级完成。  

**关键概念解释**：  
- **位掩码**：把一组布尔值压进一个整数的每一位。比如第 `i` 位是 1 代表「节点 i 已经被访问」。类似于把 12 本书的借阅情况压进一本小册子，每一页的「✔」或「✘」表示是否已借出。  
- **多源 BFS**：一次性把所有可能的起点都放进队列，这样 BFS 的层数就天然对应「从任意起点出发的最短路径长度」。  

#### 代码（Python）  

```python
from collections import deque
from typing import List

def shortestPathLength(graph: List[List[int]]) -> int:
    n = len(graph)
    # 所有节点都被访问时的目标掩码，例如 n=4 时目标是 0b1111 (=15)
    target_mask = (1 << n) - 1

    # visited[node][mask] 表示状态 (node, mask) 是否已经遍历过
    visited = [[False] * (1 << n) for _ in range(n)]
    q = deque()

    # ---------- 多源 BFS：把每个节点都当作起点 ----------
    for i in range(n):
        mask = 1 << i               # 只访问了节点 i
        visited[i][mask] = True
        q.append((i, mask, 0))      # (当前节点, 已访问掩码, 已走步数)

    # ---------- BFS 主循环 ----------
    while q:
        node, mask, dist = q.popleft()

        # 如果已经访问了全部节点，直接返回当前步数
        if mask == target_mask:
            return dist

        # 把所有邻居尝试加入队列
        for nb in graph[node]:
            next_mask = mask | (1 << nb)   # 把邻居标记为已访问
            if not visited[nb][next_mask]:
                visited[nb][next_mask] = True
                q.append((nb, next_mask, dist + 1))

    # 题目保证图是连通的，理论上不会走到这里
    return -1
```

> **关键注释**  
> - `target_mask = (1 << n) - 1` 把前 `n` 位全部置为 1，表示「全部访问完」的目标。  
> - `visited` 是二维布尔表，防止同一个 `(node, mask)` 重复入队，避免指数级爆炸。  
> - `dist + 1` 代表走了一步，从当前节点移动到邻居。  

#### 复杂度  

- **时间复杂度**：`O(n * 2^n)`  
  - 每个节点最多出现 `2^n` 种不同的访问集合，遍历一次后就不再重复。相当于「最多检查 12 × 4096 = 49,152」个状态，远小于 `n!`。  
- **空间复杂度**：`O(n * 2^n)`  
  - `visited` 表和队列都需要保存所有状态，同样是 `n * 2^n` 个布尔值。  

---

## 心得  

- **核心技巧**：**位掩码 + 多源 BFS**（也可视为状态压缩的宽度优先搜索）。  
- **适用的题型**  
  1. **旅行商问题的变形**：要求最短遍历所有节点但可以重复走（如本题）。  
  2. **带“必须访问集合”限制的最短路**：比如 LeetCode 847（本题）/ 1197（Minimum Knight Moves）中使用位掩码记录已经到达的目标点。  
  3. **状态压缩 DP**：如 “Hamiltonian Path” / “TSP” 这类需要记忆已访问节点集合的动态规划。  
- **一句话总结**：把「已访问的节点集合」压进一个整数，用 BFS 在「节点 × 访问集合」的状态图里层层展开，最先触及全覆盖状态的层数即为答案。  

---

## 反思  

- **第一反应**：想到「枚举所有排列」或「把它当成旅行商问题」去穷举，结果发现时间爆炸。  
- **最容易踩的坑**  
  1. **起点不唯一**：忘记多源 BFS，只从一个节点开始会导致答案偏大。  
  2. **位运算写错**：`mask | (1 << nb)` 必须是“或”，而不是“加”。  
  3. **状态去重不彻底**：只用 `mask` 去重会导致同一集合在不同节点重复搜索，必须同时记录 `node`。  
  4. **忘记目标掩码**：`target_mask = (1 << n) - 1` 必须把前 `n` 位全置 1，别写成 `1 << n`（那只是第 `n` 位为 1）。  
- **下次遇到同类题**：第一步先**把「必须访问的集合」抽象成位掩码**，然后**在图上做 BFS/DP**，把「当前所在节点」也加入状态，保证搜索的完整性与最优性。