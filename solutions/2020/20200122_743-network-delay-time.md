# #743. 网络延迟时间 / Network Delay Time

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/network-delay-time/)

---

## 题目（英文原版）

**Description**

You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.
We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.

**Examples**

**Example 1:**

```
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
```

**Example 2:**

```
Input: times = [[1,2,1]], n = 2, k = 1
Output: 1
```

**Example 3:**

```
Input: times = [[1,2,1]], n = 2, k = 2
Output: -1
```

**Constraints**

- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- times[i].length == 3
- 1 <= ui, vi <= n
- ui != vi
- 0 <= wi <= 100
- All the pairs (ui, vi) are unique. (i.e., no multiple edges.)

---

## 题目（中文翻译）

你会得到一个包含 **n** 个节点的网络，节点编号为 **1 到 n**。同时给定 `times`，它是一个旅行时间列表，表示有向边（directed edges）`times[i] = (ui, vi, wi)`，其中 `ui` 为源节点（source node），`vi` 为目标节点（target node），`wi` 为信号从源节点传播到目标节点所需的时间。  

我们将在给定的节点 **k** 处发送一个信号。返回所有 **n** 个节点收到该信号所需的最短时间。如果不可能让所有节点都收到信号，返回 **-1**。  

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= k <= n <= 100`  
- `1 <= times.length <= 6000`  
- `times[i].length == 3`  
- `1 <= ui, vi <= n`  
- `ui != vi`  
- `0 <= wi <= 100`  
- 所有的 `(ui, vi)` 对唯一（即不存在多条相同的有向边）。  

**示例**  

示例 1:  
```
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
```

示例 2:  
```
Input: times = [[1,2,1]], n = 2, k = 1
Output: 1
```

示例 3:  
```
Input: times = [[1,2,1]], n = 2, k = 2
Output: -1
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每条有向边都当成一条路，穷举所有可能的走法，找出从起点 `k` 到每个节点的最短时间**。  
这类似于我们在地图上找路：如果不使用任何导航工具，而是把所有可能的路线都走一遍，记录下每条路花了多少时间，最后挑出最快的那条。  

实现上可以采用 **深度优先搜索（DFS）**：

1. 从起点 `k` 开始，沿着每一条出发的有向边递归向下走。  
2. 用一个数组 `dist[i]` 记录当前已经找到的 **最小到达时间**（相当于我们手里的一本“时间表”），如果这次走到节点 `i` 用的时间比表里记录的更小，就更新表并继续往下走。  
3. 当所有可能的路径都遍历完后，`dist` 中保存的就是从 `k` 出发到每个节点的最短时间。  
4. 最后取 `dist` 中的最大值（因为要等所有节点都收到信号），如果有节点仍是 `∞`（即不可达），返回 `-1`。

> **数据结构类比**  
> - **邻接表**：想象每个节点是一本小笔记本，里面列出所有从它出发的“路”和对应的“时间”。查一本笔记本就像在字典里找词，`key` 是起点，`value` 是一组（终点，时间）的列表。  
> - **dist 数组**：像是一张“到达时间表”，表格的每一行对应一个城市，记录我们已经知道的最快到达时间。

**为什么这个方法正确？**  
DFS 会把所有可能的路径都走一遍，只要在遍历时每次都保留更短的时间，就不会错过真正的最短路。因为图中没有负权边，路径的时间只会增大，更新的过程等价于“松弛”操作。

**时间/空间复杂度**  
- 时间复杂度：在最坏情况下，每条边都可能被遍历多次，递归深度最多是 `n`，所以时间大约是 **O( n! )**（指数级），实际会更小但仍然非常慢。可以把 `O( n! )` 想象成“把所有可能的出行顺序都尝试一遍”，即使 `n=100` 也根本不可能在电脑里跑完。  
- 空间复杂度：存邻接表需要 `O( n + m )`（`m` 为边数），递归栈最深 `O( n )`，总共是 **O( n + m )**，相当于把所有路线表格和一次爬山的记忆一起放在脑子里。

#### 代码（Python）

```python
from collections import defaultdict
import sys

def network_delay_time_bruteforce(times, n, k):
    # 建立邻接表：每个节点指向的 (neighbor, travel_time) 列表
    graph = defaultdict(list)          # 类似字典，key 是起点，value 是出边列表
    for u, v, w in times:
        graph[u].append((v, w))

    # 用一个很大的数表示“还没到达”
    INF = sys.maxsize
    dist = [INF] * (n + 1)              # 下标从 1 开始，0 位不用
    dist[k] = 0                         # 起点的到达时间是 0

    # 深度优先搜索
    def dfs(node):
        # 对当前节点的每条出边尝试前进
        for nxt, w in graph[node]:
            # 通过 node 到 nxt 的新时间
            new_time = dist[node] + w
            # 如果新时间更短，就更新并继续向下搜索
            if new_time < dist[nxt]:
                dist[nxt] = new_time
                dfs(nxt)

    dfs(k)                              # 从起点开始遍历

    # 计算所有节点的最晚到达时间
    max_time = max(dist[1:])            # 去掉下标 0
    return -1 if max_time == INF else max_time
```

#### 复杂度

- **时间复杂度**：`O(n!)`（指数级）——相当于把所有可能的旅行顺序都试一遍，随着节点数增长，耗时会爆炸。  
- **空间复杂度**：`O(n + m)`——存邻接表和递归栈，需要的内存随节点和边的数量线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历同一条边**。比如从 `k` 到 `A` 有两条不同的路径，DFS 会把它们都算一遍，即使已经知道从 `k` 到 `A` 的最短时间了，后面的搜索仍然会再走一次。我们需要一种“只走一次、每次都保证是当前最短”的策略。

这正是 **Dijkstra 算法** 要解决的问题：  
- **核心思想**：每次挑选**当前已知的、离起点最近的未处理节点**，以它的最短时间为基准，去“松弛”它的所有出边。  
- **为什么这样就快了**：因为一旦一个节点被选出来，它的最短时间已经确定，不会再被后面的路径改写。于是每条边只会被“松弛”一次，整体只需要 `O(m log n)` 的时间。

实现细节（对初学者友好解释）：

1. **邻接表**：同上，用字典存每个节点的出边。  
2. **最小堆（优先队列）**：想象我们有一个装满“候选城市”的小盒子，盒子里总是把**离起点最近的城市**放在最上面，取出来的时间是 `O(log n)`，这比一次遍历所有未处理城市 `O(n)` 要快很多。Python 的 `heapq` 就是这种小盒子。  
3. **dist 数组**：同样记录每个节点的当前最短时间，初始时只有起点是 `0`，其它都是 `∞`。  
4. **循环**：不断从堆里取出时间最小的 `(cur_time, node)`，如果这个时间已经大于 `dist[node]`（说明这个节点已经被更短的路径更新过），就直接跳过。否则，用 `cur_time` 去尝试更新它的所有邻居 `neighbor`，如果 `cur_time + w < dist[neighbor]`，就把新的更短时间写进去，并把 `(new_time, neighbor)` 放进堆里。  
5. **结束**：当堆空了，或者我们已经处理了所有节点，`dist` 就是从 `k` 出发到每个节点的最短时间。再取最大值，判断是否有不可达的节点。

> **类比**  
> - **最小堆**：像是排队买咖啡的窗口，最早到达的人（时间最小）会先被服务。  
> - **松弛**：把新发现的更快路线写进“时间表”，就像在地图上画出一条更短的道路。

#### 代码（Python）

```python
import heapq
from collections import defaultdict
import sys

def network_delay_time(times, n, k):
    # 1. 建图（邻接表）
    graph = defaultdict(list)          # key: 起点，value: (终点, 时间) 列表
    for u, v, w in times:
        graph[u].append((v, w))

    # 2. 初始化距离数组，所有节点的最短时间设为无限大
    INF = sys.maxsize
    dist = [INF] * (n + 1)              # 1-indexed
    dist[k] = 0                         # 起点到自己的时间是 0

    # 3. 最小堆，初始只有起点
    heap = [(0, k)]                     # (当前已知最短时间, 节点)

    while heap:
        cur_time, node = heapq.heappop(heap)   # 取出时间最小的节点
        # 如果取出来的时间已经不是最短的了，直接跳过
        if cur_time > dist[node]:
            continue

        # 4. 松弛所有相邻的边
        for nxt, w in graph[node]:
            new_time = cur_time + w
            # 发现更短的到达时间，更新并放入堆中
            if new_time < dist[nxt]:
                dist[nxt] = new_time
                heapq.heappush(heap, (new_time, nxt))

    # 5. 计算最大最短时间
    max_time = max(dist[1:])            # 去掉下标 0
    return -1 if max_time == INF else max_time
```

#### 复杂度

- **时间复杂度**：`O(m log n)`  
  - `m` 是边的数量，`log n` 来自堆的插入/弹出操作。可以把它想象成“每走一条路只花一点点时间去找下一个最近的城市”，整体随边数线性增长，而不是指数级爆炸。  
  - 与暴力解的 `O(n!)` 相比，速度提升了 **几个数量级**，在本题的约束（`n ≤ 100, m ≤ 6000`）下毫秒即可完成。

- **空间复杂度**：`O(n + m)`  
  - 用邻接表存图需要 `O(m)`，`dist` 数组和堆最多各占 `O(n)`，总共也是线性增长。

---

## 心得

- 这道题核心考察的是 **最短路径**，尤其是 **单源最短路径**（从一个起点到所有其它点的最短距离）。  
- 常用技巧：**Dijkstra 算法 + 最小堆**。当图中不存在负权边时，它是最快且最稳妥的选择。  
- 适用的类似题型  
  1. **LeetCode 743. Network Delay Time**（本题）  
  2. **LeetCode 1514. Path with Maximum Probability**（改为最大概率，仍可用 Dijkstra）  
  3. **LeetCode 1631. Path With Minimum Effort**（最小努力路径，同样用 Dijkstra）  

> **一句话总结解题钥匙**：**“每次都选离起点最近的未确定节点，利用堆把这一步做到对数时间”**。

---

## 反思

- **第一反应**：直接把所有路径枚举（DFS）或把图转成矩阵用 Floyd‑Warshall。  
- **最容易踩的坑**  
  - 忘记把 **不可达节点** 处理成 `-1`，直接返回了最大 `INF`。  
  - 堆里可能会出现“已经有更短记录的旧节点”，需要在弹出时用 `if cur_time > dist[node]: continue` 跳过。  
  - 输入节点是 **1-indexed**，容易写成 0-indexed 导致数组越界。  
- **下次遇到同类题**，第一步应该想到：**“这是一张有向加权图，要求最短传播时间 → 用 Dijkstra（或 BFS+层次遍历）”**，先检查是否有负权边，再决定使用哪种最短路算法。