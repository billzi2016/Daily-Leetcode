# #3112. 最小访问消失节点的时间 / Minimum Time to Visit Disappearing Nodes

> 难度：中等 · 标签：Array、Graph、Heap (Priority Queue)、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-visit-disappearing-nodes/)

---

## 题目（英文原版）

**Description**

There is an undirected graph of n nodes. You are given a 2D array edges, where edges[i] = [ui, vi, lengthi] describes an edge between node ui and node vi with a traversal time of lengthi units.
Additionally, you are given an array disappear, where disappear[i] denotes the time when the node i disappears from the graph and you won't be able to visit it.
Note that the graph might be disconnected and might contain multiple edges.
Return the array answer, with answer[i] denoting the minimum units of time required to reach node i from node 0. If node i is unreachable from node 0 then answer[i] is -1.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,1,5]
Output: [0,-1,4]
Explanation:

We are starting our journey from node 0, and our goal is to find the minimum time required to reach each node before it disappears.
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,3,5]
Output: [0,2,3]
Explanation:

We are starting our journey from node 0, and our goal is to find the minimum time required to reach each node before it disappears.
```

**Example 3:**

```
Input: n = 2, edges = [[0,1,1]], disappear = [1,1]
Output: [0,-1]
Explanation:
Exactly when we reach node 1, it disappears.
```

**Constraints**

- 1 <= n <= 5 * 104
- 0 <= edges.length <= 105
- edges[i] == [ui, vi, lengthi]
- 0 <= ui, vi <= n - 1
- 1 <= lengthi <= 105
- disappear.length == n
- 1 <= disappear[i] <= 105

---

## 题目（中文翻译）

给定一个包含 **n** 个节点的无向图。你会得到一个二维数组 `edges`，其中 `edges[i] = [ui, vi, lengthi]` 表示节点 `ui` 与节点 `vi` 之间存在一条边，行走该边需要 `lengthi` 单位时间（traversal time）。  
此外，还会给定一个数组 `disappear`，其中 `disappear[i]` 表示节点 `i` 在图中消失的时间点，之后将无法再访问该节点。  
请注意，图可能是不连通的，也可能包含多条重复的边。  

返回数组 `answer`，其中 `answer[i]` 表示从节点 `0` 出发到达节点 `i` 所需的最小时间（单位时间）。如果节点 `i` 无法从节点 `0` 到达，则 `answer[i] = -1`。

## 示例

### 示例 1
**输入**  
`n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,1,5]`  

**输出**  
`[0,-1,4]`  

**解释**  
我们从节点 `0` 开始出发，目标是找出在每个节点消失之前能够到达该节点的最小时间。

### 示例 2
**输入**  
`n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,3,5]`  

**输出**  
`[0,2,3]`  

**解释**  
同样从节点 `0` 出发，计算在每个节点消失之前能够到达的最小时间。

### 示例 3
**输入**  
`n = 2, edges = [[0,1,1]], disappear = [1,1]`  

**输出**  
`[0,-1]`  

**解释**  
恰好在我们到达节点 `1` 的瞬间，它就已经消失，因而无法访问。

## 约束条件
- `1 <= n <= 5 * 10^4`
- `0 <= edges.length <= 10^5`
- `edges[i] == [ui, vi, lengthi]`
- `0 <= ui, vi <= n - 1`
- `1 <= lengthi <= 10^5`
- `disappear.length == n`
- `1 <= disappear[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的走法**，把每条路走一遍，记录到达每个节点的最短时间，只要这条路在节点消失之前到达，就算合法。  

可以把图想象成城市的道路网络，`length` 就是两座城市之间的行车时间。  
我们从城市 0 出发，拿出一张**白纸**，把每一次“走到哪儿、用了多少时间”都写下来。  
- 用**深度优先搜索（DFS）**把所有路径展开（类似在迷宫里不断往前走，走不通就回头）。  
- 每次走到一个新节点 `v`，计算当前耗时 `t`，如果 `t` **小于** `disappear[v]`，说明还能在它消失前到达，就把 `t` 记下来；否则这条路就不继续往下走了。  

这样遍历完所有路径后，每个节点的最小合法时间就是答案。  

> 这种方法之所以**正确**：  
> - 我们把**所有**可能的走法都考虑到了，因而不会错过任何一条能在消失前到达的路径。  
> - 只要有一条合法路径，我们一定会在遍历时找到它，并把最小的时间保存下来。  

然而，这种“全枚举”会非常慢：  
- 在最坏情况下（图是完全连通的），从起点出发的路径数是指数级的，约为 `O(n!)`。  
- 每次递归都要复制路径信息，空间也会爆炸。  

因此只能作为**思考起点**，帮助我们发现真正的瓶颈——**“每次都要把所有路径都走遍”**。  

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def brute_force(n, edges, disappear):
    # 建立邻接表，存储 (邻居, 边长)
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # 用一个很大的数代表“还没有到达”
    INF = 10**18
    best = [INF] * n          # best[i] 保存到达 i 的最小合法时间
    best[0] = 0               # 起点 0 的到达时间是 0

    def dfs(u, cur_time, visited):
        """从节点 u 出发，当前已经用了 cur_time，visited 记录已经走过的节点"""
        for v, w in graph[u]:
            if v in visited:          # 防止在同一条路径上循环
                continue
            arrive = cur_time + w     # 到达 v 的时间
            if arrive >= disappear[v]:   # 已经晚于 v 消失，不能走这条路
                continue
            # 更新到达 v 的最小时间
            if arrive < best[v]:
                best[v] = arrive
            # 继续向下搜索
            visited.add(v)
            dfs(v, arrive, visited)
            visited.remove(v)

    # 从 0 开始深度优先搜索
    dfs(0, 0, {0})

    # 把无法到达的节点转成 -1
    return [-1 if d == INF else d for d in best]

# ------------------------------------------------------------------
# 示例
print(brute_force(3, [[0,1,2],[1,2,1],[0,2,4]], [1,1,5]))   # [0, -1, 4]
print(brute_force(3, [[0,1,2],[1,2,1],[0,2,4]], [1,3,5]))   # [0, 2, 3]
print(brute_force(2, [[0,1,1]], [1,1]))                     # [0, -1]
```

> **关键注释**  
> - `visited` 类似“字典的查词”，防止在同一条路径里重复访问同一个城市（避免无限循环）。  
> - `arrive >= disappear[v]` 用 **大于等于** 判断，因为“恰好在消失的那一刻”也算已经无法访问。  

#### 复杂度  

- **时间复杂度**：`O(所有可能的路径数)`，在最坏情况下是指数级（约 `O(n!)`），实际会因图的稀疏程度而快一点。  
  - 大白话：想象把所有可能的旅行路线都写在纸上，路线数会像炸弹一样爆炸，根本跑不完。  
- **空间复杂度**：`O(n)` 用于递归栈和 `visited` 集合，保存当前路径上的节点。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**“遍历所有路径”**是瓶颈。  
事实上，我们只关心**最短的到达时间**，而不是每一条可能的路。  
这正好可以使用**单源最短路**的经典算法——**Dijkstra**（迪杰斯特拉）：

1. **核心观察**  
   - 在没有“消失时间”限制时，Dijkstra 能在 `O((V+E) log V)` 时间内求出从起点到所有节点的最短距离。  
   - 现在多了一个约束：只有当 **到达时间 < disappear[node]** 时，这条路径才算合法。  
   - 这意味着我们只要在**松弛（relax）**一条边时，检查新得到的时间是否满足约束；不满足就直接丢掉这条边。  

2. **为什么这样仍然是最优的**  
   - Dijkstra 本身的**贪心性质**保证：当我们把一个节点 `u` 从优先队列（最小堆）中弹出时，`dist[u]` 已经是从起点到 `u` 的**最短合法时间**。  
   - 只要我们在弹出 `u` 之前已经确保 `dist[u] < disappear[u]`（起点自然满足），后续再通过 `u` 去更新邻居时，得到的时间一定是“从起点到邻居的最短合法时间”。  
   - 因此，加入 **“到达前必须小于消失时间”** 的过滤，不会破坏 Dijkstra 的正确性，只会让一些不合法的路径在一开始就被剪掉，进一步加速。  

3. **实现细节**  
   - **邻接表**：`graph[u] = [(v, w), …]`，因为图可能有多条平行边，全部保留。  
   - **最小堆**（`heapq`）：存 `(当前时间, 节点)`，每次弹出时间最小的节点。  
   - **距离数组** `dist` 初始化为无穷大，`dist[0] = 0`。  
   - 当弹出 `(t, u)` 时：  
        - 如果 `t != dist[u]`，说明这条记录是“过时的”，直接跳过（典型的 Dijkstra “懒删”技巧）。  
        - 如果 `t >= disappear[u]`，说明即使已经弹出，这个节点已经在消失的瞬间或之后了，**不再继续扩展**（因为已经不能合法使用它作为中转）。  
   - 对每条相邻边 `(u, v, w)`：  
        - `new_t = t + w`  
        - 若 `new_t < disappear[v]` 且 `new_t < dist[v]`，则更新 `dist[v]` 并压入堆。  

4. **返回答案**  
   - 最后把 `dist[i]` 中仍为无穷大的节点记成 `-1`（不可达），其余保持最短合法时间。  

5. **复杂度分析**（和 Dijkstra 相同）  
   - **时间**：`O((V + E) log V)`，因为每条边最多被松弛一次，堆操作是 `log V`。  
   - **空间**：`O(V + E)` 用于邻接表、距离数组和堆。  

#### 代码（Python）

```python
import heapq
from collections import defaultdict

def minimum_time_to_visit_disappearing_nodes(n, edges, disappear):
    """
    Dijkstra + 消失时间约束
    返回从节点 0 出发，能够在节点消失前到达的最短时间数组
    """
    # 1️⃣ 建图（邻接表）
    graph = defaultdict(list)               # 每个节点对应 [(邻居, 边长), ...]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    INF = 10**18
    dist = [INF] * n                         # dist[i] = 已知的最短合法到达时间
    dist[0] = 0                               # 起点时间是 0

    # 2️⃣ 最小堆，存 (当前累计时间, 节点)
    heap = [(0, 0)]                           # 初始只有起点
    while heap:
        cur_t, u = heapq.heappop(heap)

        # 2.1 已经不是最新的记录，直接跳过
        if cur_t != dist[u]:
            continue

        # 2.2 如果已经晚于 u 的消失时间，u 不能再作为中转点
        if cur_t >= disappear[u]:
            continue

        # 2.3 松弛所有相邻边
        for v, w in graph[u]:
            new_t = cur_t + w                # 到达 v 的时间
            # 只在「新时间 < v 消失时间」且「更优」时才更新
            if new_t < disappear[v] and new_t < dist[v]:
                dist[v] = new_t
                heapq.heappush(heap, (new_t, v))

    # 3️⃣ 把不可达的节点转成 -1
    return [-1 if d == INF else d for d in dist]

# ------------------------------------------------------------------
# 示例
print(minimum_time_to_visit_disappearing_nodes(
    3, [[0,1,2],[1,2,1],[0,2,4]], [1,1,5]))   # [0, -1, 4]

print(minimum_time_to_visit_disappearing_nodes(
    3, [[0,1,2],[1,2,1],[0,2,4]], [1,3,5]))   # [0, 2, 3]

print(minimum_time_to_visit_disappearing_nodes(
    2, [[0,1,1]], [1,1]))                     # [0, -1]
```

> **关键注释**  
> - `heapq` 就像“超市排队的收银台”，每次都会把**最早能到达的城市**挑出来处理。  
> - `if cur_t >= disappear[u]: continue` 相当于“这座城市已经在我们到达的那一刻倒塌，不能再从这里继续旅行”。  
> - `new_t < disappear[v]` 保证我们“在城市 v 还在的时间里”抵达它。  

#### 复杂度  

- **时间复杂度**：`O((n + m) log n)`（`m = len(edges)`）。  
  - 大白话：我们只需要“排队”访问每条道路一次，排队本身是 `log n` 级别的操作，整体快得多。  
- **空间复杂度**：`O(n + m)`。  
  - 需要存图、距离数组以及堆，和输入规模线性相关。  

---

## 心得  

- **核心技巧**：**在 Dijkstra 里加入“到达前必须早于节点消失时间”的过滤**。  
- **适用的题型**（类似约束的最短路）  
  1. **有时间窗的最短路**（如每个节点只能在 `[open, close]` 区间内访问）。  
  2. **路径必须满足燃料/能量上限**（每到达一个节点要检查剩余燃料是否足够）。  
  3. **带有截止日期的任务调度**（如在限定时间内完成所有任务的最小耗时）。  
- **一句话总结解题钥匙**：  
  > **“只要在每次松弛时把合法性检查写进去，Dijkstra 仍然是求最短合法路径的最强武器”。**  

---

## 反思  

- **第一反应**：看到“最短时间”“消失时间”就想到**最短路径**，但一开始忘记了“只能在节点消失前到达”，于是误以为普通 Dijkstra 就够了。  
- **最容易踩的坑**  
  1. **等于消失时间不算**：`arrive == disappear[i]` 仍然视为不可达，需要使用 **严格小于** (`<`) 判断。  
  2. **多条平行边**：不能只保留最短的一条，所有边都要加入图，否则可能错过合法的更快路径。  
  3. **起点本身的消失时间**：若 `disappear[0] == 0`（题目保证 ≥1），但若出现这种情况要直接返回全 `-1`。  
- **下次遇到同类题的第一步**：  
  > **“先写出普通的 Dijkstra 框架，再在松弛阶段加入题目给出的额外时间约束”。**  

祝你在算法的旅途中，像在图中一样，一步一步走向最短且合法的终点！