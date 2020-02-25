# #785. 判断图是否为二分图 / Is Graph Bipartite?

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/is-graph-bipartite/)

---

## 题目（英文原版）

**Description**

There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to. More formally, for each v in graph[u], there is an undirected edge between node u and node v. The graph has the following properties:
A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge in the graph connects a node in set A and a node in set B.
Return true if and only if it is bipartite.

**Examples**

**Example 1:**

```
Input: graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
Output: false
Explanation: There is no way to partition the nodes into two independent sets such that every edge connects a node in one and a node in the other.
```

**Example 2:**

```
Input: graph = [[1,3],[0,2],[1,3],[0,2]]
Output: true
Explanation: We can partition the nodes into two sets: {0, 2} and {1, 3}.
```

**Constraints**

- graph.length == n
- 1 <= n <= 100
- 0 <= graph[u].length < n
- 0 <= graph[u][i] <= n - 1
- graph[u] does not contain u.
- All the values of graph[u] are unique.
- If graph[u] contains v, then graph[v] contains u.

---

## 题目（中文翻译）

存在一个由 `n` 个节点组成的无向图（undirected graph），节点编号为 `0` 到 `n - 1`。给定一个二维数组 `graph`，其中 `graph[u]` 是与节点 `u` 相邻的节点列表。形式上，对于 `graph[u]` 中的每个 `v`，节点 `u` 与节点 `v` 之间存在一条无向边（undirected edge）。该图满足以下属性：

- 如果一个图的节点可以被划分为两个独立集合（independent set）`A` 和 `B`，且图中的每条边都连接集合 `A` 中的一个节点和集合 `B` 中的一个节点，则该图是二分图（bipartite）。

返回 `true` 当且仅当该图是二分图。

## 示例

### 示例 1
**输入**  
`graph = [[1,2,3],[0,2],[0,1,3],[0,2]]`

**输出**  
`false`

**解释**  
不存在一种划分方式能够把节点分成两个独立集合，使得每条边都连接两个不同集合中的节点。

### 示例 2
**输入**  
`graph = [[1,3],[0,2],[1,3],[0,2]]`

**输出**  
`true`

**解释**  
可以将节点划分为两组：`{0, 2}` 和 `{1, 3}`，满足二分图的定义。

## 约束条件

- `graph.length == n`
- `1 <= n <= 100`
- `0 <= graph[u].length < n`
- `0 <= graph[u][i] <= n - 1`
- `graph[u]` 不包含 `u`
- `graph[u]` 中的所有值互不相同
- 若 `graph[u]` 包含 `v`，则 `graph[v]` 必定包含 `u`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的划分**，看有没有一种划分能够满足“相邻的两个点必须分到不同的集合”。  
把每个节点看成要贴上两种颜色中的一种（比如红色代表集合 A，蓝色代表集合 B），所有节点共有 `2ⁿ` 种贴法（`n` 是节点数）。只要遍历这些贴法，并逐条检查图中的每条无向边的两个端点颜色是否不同，就能得到答案。

- **数据结构**：  
  - 用一个长度为 `n` 的列表 `color` 保存每个节点的颜色，`0` 表示未染色，`1` 表示红，`-1` 表示蓝。  
  - 图本身已经以邻接表的形式给出：`graph[u]` 是节点 `u` 的所有相邻节点。

- **正确性**：  
  - 我们穷举了**所有**可能的颜色分配。只要存在一种合法的分配，使得每条边的两端颜色不同，就会在遍历过程中被发现。反之，如果遍历完所有可能仍未找到合法分配，则图一定不是二分图。

- **时间/空间复杂度**：  
  - 时间复杂度是 `O(2ⁿ * E)`，其中 `E` 为边数。原因是我们要检查 `2ⁿ` 种颜色组合，每种组合都要遍历所有边来验证。  
    - 大白话：如果图有 10 个节点，`2ⁿ` 就是 1024，意味着最多要检查 1024 次，每次都要看所有边，显然会很慢。  
  - 空间复杂度是 `O(n)`，只需要保存颜色数组和递归时的临时变量。

#### 代码（Python）

```python
from typing import List

def isBipartite_bruteforce(graph: List[List[int]]) -> bool:
    n = len(graph)                     # 节点数
    color = [0] * n                    # 0：未染色，1：红，-1：蓝

    # 递归枚举每个节点的颜色
    def dfs(idx: int) -> bool:
        if idx == n:                    # 所有节点都已经染好色，合法
            return True

        # 尝试给当前节点染红或蓝两种颜色
        for c in (1, -1):
            # 检查已染色的相邻节点是否冲突
            conflict = False
            for nb in graph[idx]:
                if color[nb] == c:      # 相邻节点已经是相同颜色，冲突
                    conflict = True
                    break
            if conflict:
                continue                # 这套颜色不行，换另一种尝试

            color[idx] = c              # 给 idx 染上颜色 c
            if dfs(idx + 1):            # 继续往后枚举
                return True
            color[idx] = 0              # 回溯，撤销颜色

        return False                    # 两种颜色都不行，返回失败

    return dfs(0)
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ * E)`  
  - `2ⁿ` 是所有可能的颜色分配数，`E` 是图中边的数量。对每一种分配，我们都要检查所有相邻关系是否满足不同颜色的要求。  
- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的颜色数组和递归栈（最深 `n` 层），不随边数增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**重复检查相同的子结构**：当我们已经确定了某几个节点的颜色后，后面的枚举仍然会把已经确定的冲突再次检查一遍。  
二分图的本质是**能否用两种颜色把整个图涂色，使得每条边的两端颜色不同**。这正好可以用 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）** **一次遍历** 完成：

1. 从任意未染色的节点开始，给它涂上红色（`1`）。  
2. 用 BFS 把它的所有相邻节点涂成蓝色（`-1`），再把蓝色节点的相邻节点涂成红色，层层推进。  
3. 在遍历过程中，如果发现一条边的两端已经被涂了**相同的颜色**，说明出现冲突，图一定不是二分图，直接返回 `False`。  
4. 图可能是**不连通**的（有多个独立的连通块），所以要对每个未染色的节点都启动一次 BFS/DFS。

> **类比**：把图想象成一群人，每个人要分到“红队”或“蓝队”。规则是：**所有朋友必须在不同的队**。我们可以从一个人开始，让他进红队，然后把他的所有朋友安排进蓝队，再把这些蓝队成员的朋友安排进红队……如果在这个过程中出现了“某个人的两个朋友已经在同一个队”，说明规则冲突，无法完成分队。

**核心数据结构**  
- `color` 列表：保存每个节点的颜色（`0` 未染，`1` 红，`-1` 蓝），相当于**哈希表**的“键是节点，值是颜色”。  
- `queue`（BFS 用）或递归栈（DFS 用）：保存待处理的节点。

**为什么是最优的**  
- 每条边和每个节点只会被访问 **一次**，所以时间是线性的 `O(V + E)`（`V` 为节点数，`E` 为边数）。  
- 只用了一个颜色数组，空间是 `O(V)`。

#### 代码（Python）

```python
from collections import deque
from typing import List

def isBipartite(graph: List[List[int]]) -> bool:
    n = len(graph)
    color = [0] * n                     # 0：未染色，1：红，-1：蓝

    # 对每个连通块都做一次 BFS
    for start in range(n):
        if color[start] != 0:           # 已经染过色，说明在之前的 BFS 中处理过
            continue

        # 从 start 节点开始，给它涂红色
        color[start] = 1
        q = deque([start])

        while q:
            node = q.popleft()
            cur_color = color[node]
            next_color = -cur_color      # 相邻节点必须异色

            for nb in graph[node]:
                if color[nb] == 0:       # 还没染色，涂上相反的颜色并加入队列
                    color[nb] = next_color
                    q.append(nb)
                elif color[nb] != next_color:
                    # 已经染色且颜色不符合要求，冲突！不是二分图
                    return False

    return True
```

> **代码要点注释**  
- `color[start] = 1`：把起点标记为红色。  
- `next_color = -cur_color`：红变蓝，蓝变红，利用负号巧妙取反。  
- `elif color[nb] != next_color`：如果相邻节点已经有颜色，但不是我们期望的异色，说明冲突。

#### 复杂度

- **时间复杂度**：`O(V + E)`  
  - 每个节点最多入队一次，每条边在检查时会被访问两次（`u→v` 与 `v→u`），所以整体是线性时间。与暴力解的指数级时间相比，快得多。  
- **空间复杂度**：`O(V)`  
  - 主要是颜色数组 `color` 和 BFS 队列，最坏情况下队列里会同时存放同一层的所有节点，数量不会超过 `V`。

---

## 心得

- **核心技巧**：**二分图的两色涂色**（BFS/DFS）  
- **适用的题型**：  
  1. 判断图是否二分（本题）。  
  2. “可能的 bipartite 关系” 类似的社交网络分组问题。  
  3. “能否把图中的节点分成两组，使得每组内部没有边”——如 `LeetCode 886`（可能的二分图）等。  
- **一句话总结**：**把图当作两支队伍的排队游戏，只要在遍历时始终让相邻的两个玩家站在不同的队，就能快速判断是否可行**。

---

## 反思

- **第一反应**：想到“枚举所有颜色分配”，因为只要有一种合法的分配就行。  
- **最容易踩的坑**：  
  - **图不连通**：只从 0 节点开始遍历会漏掉其他连通块，需要对每个未染色的节点都启动一次搜索。  
  - **颜色冲突的判断**：一定要在相邻节点已经染色的情况下检查颜色是否相同，不能只判断未染色时的情况。  
  - **使用负号取反**：`-cur_color` 只能在颜色只有 `1` 与 `-1` 两种时使用，若使用 `0/1` 需要手动取反。  
- **下次遇到同类题**：**第一步就想到“用 BFS/DFS 给图两色”**，把问题转化为“遍历时保持相邻节点异色”，再检查是否出现冲突。这样就能直接得到线性时间的解法。