# #802. 寻找最终安全状态 / Find Eventual Safe States

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/find-eventual-safe-states/)

---

## 题目（英文原版）

**Description**

There is a directed graph of n nodes with each node labeled from 0 to n - 1. The graph is represented by a 0-indexed 2D integer array graph where graph[i] is an integer array of nodes adjacent to node i, meaning there is an edge from node i to each node in graph[i].
A node is a terminal node if there are no outgoing edges. A node is a safe node if every possible path starting from that node leads to a terminal node (or another safe node).
Return an array containing all the safe nodes of the graph. The answer should be sorted in ascending order.

**Examples**

**Example 1:**

```
Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
Output: [2,4,5,6]
Explanation: The given graph is shown above.
Nodes 5 and 6 are terminal nodes as there are no outgoing edges from either of them.
Every path starting at nodes 2, 4, 5, and 6 all lead to either node 5 or 6.
```

**Example 2:**

```
Input: graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]
Output: [4]
Explanation:
Only node 4 is a terminal node, and every path starting at node 4 leads to node 4.
```

**Constraints**

- n == graph.length
- 1 <= n <= 104
- 0 <= graph[i].length <= n
- 0 <= graph[i][j] <= n - 1
- graph[i] is sorted in a strictly increasing order.
- The graph may contain self-loops.
- The number of edges in the graph will be in the range [1, 4 * 104].

---

## 题目（中文翻译）

**描述**  
给定一个包含 `n` 个节点的有向图（directed graph），节点编号为 `0` 到 `n - 1`。图使用一个 **0 索引** 的二维整数数组 `graph` 表示，其中 `graph[i]` 是与节点 `i` 相邻的节点（adjacent nodes）构成的整数数组，意味着存在一条从节点 `i` 到 `graph[i]` 中每个节点的有向边。

- **终端节点（terminal node）**：没有任何出边的节点。  
- **安全节点（safe node）**：从该节点出发的 **所有可能的路径（path）** 最终都能到达某个终端节点（或另一个安全节点）。

返回一个包含图中所有安全节点的数组，答案需按升序排列。

**示例 1**  
```text
Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
Output: [2,4,5,6]
Explanation: 如上图所示。  
节点 5 和 6 为终端节点，因为它们没有出边。  
从节点 2、4、5、6 出发的每条路径最终都会到达节点 5 或 6，因此这些节点都是安全节点。
```

**示例 2**  
```text
Input: graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]
Output: [4]
Explanation: 只有节点 4 是终端节点，且从节点 4 出发的所有路径都只能到达节点 4 本身，所以它是唯一的安全节点。
```

**约束条件**  
- `n == graph.length`  
- `1 <= n <= 10^4`  
- `0 <= graph[i].length <= n`  
- `0 <= graph[i][j] <= n - 1`  
- `graph[i]` 按严格递增顺序排序。  
- 图中可能包含自环。  
- 图中的边数在 `[1, 4 * 10^4]` 范围内。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每个节点都做一次深度优先搜索**，把所有可能的走法都走一遍，只要出现了环（即在同一条路径上再次访问到已经走过的节点），说明从这个起点可以走进死循环，它就不是安全的；如果所有走法都能顺利走到没有出边的终点节点，则这个节点安全。

- **用到的数据结构**  
  - **栈（或递归）**：DFS 需要记录当前路径上已经访问的节点，类似我们在走迷宫时手里拿的“足迹”。  
  - **集合 `visited`**：保存本次搜索过程中已经走过的节点，防止在同一条路径上重复进入。可以把它想成“已经踩过的格子”。  
  - **列表 `graph`**：题目已经给出的邻接表，像是每个城市的出发航班表。

- **为什么正确**  
  对一个起点 `s`，DFS 会枚举 **所有** 从 `s` 出发的路径。如果其中有一条路径进入环，则必然出现「在当前路径上再次访问同一个节点」的情况，这正是我们用 `visited` 检测到的。只要不存在这种情况，说明 **每条路径都必然走到终点**，于是 `s` 是安全的。

- **复杂度分析（大白话）**  
  - 对每个节点我们都要跑一次完整的 DFS。一次完整的 DFS 在最坏情况下会遍历图中所有的边和节点，记作 `O(V+E)`（V = 节点数，E = 边数）。  
  - 因为我们要对 **每个节点** 都这么做，整体时间就是 `O(V·(V+E))`。可以把它想成「你先检查第 1 个人的所有可能走法，然后检查第 2 个人的所有可能走法……」  
  - 额外空间主要是递归栈和 `visited` 集合，最深会到 `V`，所以是 `O(V)`。

#### 代码（Python）

```python
from typing import List

def eventualSafeNodes_bruteforce(graph: List[List[int]]) -> List[int]:
    n = len(graph)

    # 记录每个节点是否已经判定为安全，避免重复计算
    safe_memo = {}

    # 深度优先搜索，返回该节点是否安全
    def dfs(node: int, path: set) -> bool:
        # 如果已经算过，直接返回缓存结果
        if node in safe_memo:
            return safe_memo[node]

        # 当前路径上再次出现同一个节点 → 环
        if node in path:
            safe_memo[node] = False
            return False

        # 终止节点没有出边，必然安全
        if not graph[node]:
            safe_memo[node] = True
            return True

        # 把当前节点加入本次路径的集合
        path.add(node)

        # 只要有一条出边通向不安全的节点，当前节点就不安全
        for nxt in graph[node]:
            if not dfs(nxt, path):
                safe_memo[node] = False
                path.remove(node)          # 退出前记得把自己踢出路径集合
                return False

        # 所有出边都通向安全节点，当前节点安全
        path.remove(node)
        safe_memo[node] = True
        return True

    res = []
    for i in range(n):
        if dfs(i, set()):
            res.append(i)

    return res
```

> **关键行中文注释**  
> - `if node in path:` 检测环  
> - `if not graph[node]:` 终止节点直接安全  
> - `safe_memo` 用来**记忆化**已经算好的结果，防止重复递归  

#### 复杂度

- **时间复杂度**：`O(V·(V+E))`  
  - “V 次”遍历每个起点，每次 DFS 最坏遍历所有节点和边。  
- **空间复杂度**：`O(V)`  
  - 递归栈最深 `V`，加上 `path` 集合和记忆化表同样最多保存 `V` 条信息。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**重复遍历相同的子图**。实际上，所有**不安全的节点**恰好组成**有环的强连通分量**，而**安全的节点**是 **图的拓扑序的后半段**——它们不会出现在任何环里。我们可以把问题转化为 **“把所有不在环里的节点挑出来”**。

**核心技巧**：**反向拓扑排序（Kahn 算法）**  
1. 把原图的所有边方向反过来，得到 `reverse_graph`。  
   - 在原图中，若 `u → v`，则在反向图中 `v → u`。  
2. 统计每个节点的 **出度**（在原图中的邻接数），记作 `out_degree[i]`。  
3. 把所有 **出度为 0** 的节点（终止节点）放进队列 `q`。这些节点一定安全。  
4. 逐个弹出队列中的节点 `cur`，在 **反向图** 中找到所有指向 `cur` 的前驱 `pre`，把 `pre` 的出度减 1。  
   - 当某个前驱的出度降到 0，说明它所有的后继已经全部是安全的，它自己也安全，加入队列。  
5. 最终 **所有被加入队列的节点** 就是安全节点，按升序返回。

> **为什么这样就能找出所有安全节点？**  
> - 在原图里，一个节点如果还有 **未被确认安全的后继**，它的出度就不会降到 0，说明它仍可能进入环。  
> - 只要一个节点的所有后继都是安全的（即出度已被“消除”），它本身也安全。这样从 **终点向前层层“剥离”**，恰好就是拓扑排序的过程。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def eventualSafeNodes(graph: List[List[int]]) -> List[int]:
    n = len(graph)

    # 1. 建立反向图：reverse_adj[v] 收集所有指向 v 的前驱节点 u
    reverse_adj = [[] for _ in range(n)]
    out_degree = [0] * n               # 记录原图的出度

    for u, neighbors in enumerate(graph):
        out_degree[u] = len(neighbors)  # u 的出度等于它的邻接列表长度
        for v in neighbors:
            reverse_adj[v].append(u)    # v 的前驱加入 reverse_adj

    # 2. 初始队列放所有出度为 0（终止节点）的节点
    q = deque([i for i in range(n) if out_degree[i] == 0])
    safe = []                           # 最终安全节点的列表

    # 3. BFS（类似拓扑排序）逐层剥离
    while q:
        cur = q.popleft()
        safe.append(cur)                # cur 已经确认安全

        # 通过反向图找到所有指向 cur 的前驱 pre
        for pre in reverse_adj[cur]:
            out_degree[pre] -= 1        # 把 cur 从 pre 的后继中“移除”
            if out_degree[pre] == 0:    # 前驱的所有后继都安全了
                q.append(pre)

    # 4. 按题目要求返回升序结果
    return sorted(safe)
```

> **关键行中文注释**  
> - `reverse_adj[v].append(u)`：把“谁指向 v”记下来，方便后续“从安全节点回溯”。  
> - `out_degree[pre] -= 1`：把已经确定安全的后继从前驱的出度中去掉。  
> - `if out_degree[pre] == 0:` 前驱的所有后继都安全 → 前驱也安全。  

#### 复杂度

- **时间复杂度**：`O(V + E)`  
  - 每条边只在建图时遍历一次，又在反向遍历时被处理一次，整体线性。相比暴力的 `O(V·(V+E))` 快了很多。  
- **空间复杂度**：`O(V + E)`  
  - 需要存储反向邻接表和出度数组，大小正好和原图相同。  

---

## 心得

- **核心技巧**：**把“安全节点 = 不在环里”转化为 **反向拓扑排序**，利用出度逐渐归零的过程把安全节点一步步剥离。  
- **适用的题型**  
  1. **找出图中所有的“终端安全点”**（本题）。  
  2. **找出有向图的所有“非环节点”**（如 “所有可以安全结束的课程”）。  
  3. **拓扑排序相关的题目**（如 “课程表 II” 中的可行顺序）。  
- **一句话总结解题钥匙**：**从“没有出路的终点”逆向推进，所有能够把出度压到 0 的节点必然安全**。

---

## 反思

- **第一反应**：看到“所有路径都能到达终点”，立刻想到 **遍历所有路径**，于是写了暴力的 DFS。  
- **最容易踩的坑**  
  - **自环**：`i -> i` 本身就是一个环，需要在 DFS 中检测 `node in path`。  
  - **孤立节点**：没有出边的节点直接安全，别忘了把它们放进初始队列。  
  - **返回结果要排序**：拓扑排序的顺序不一定是升序，需要 `sorted()`。  
- **下次类似题的第一步**：先判断 **是否可以把问题转化为“图中哪些点不在环里”**，若可以，就直接考虑 **逆向拓扑（Kahn）或 Tarjan 强连通分量**，而不是盲目遍历所有路径。