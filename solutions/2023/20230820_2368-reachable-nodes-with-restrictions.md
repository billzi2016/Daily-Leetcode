# #2368. 可达节点（受限制） / Reachable Nodes With Restrictions

> 难度：中等 · 标签：Array、Hash Table、Tree、Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/reachable-nodes-with-restrictions/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.
You are given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree. You are also given an integer array restricted which represents restricted nodes.
Return the maximum number of nodes you can reach from node 0 without visiting a restricted node.
Note that node 0 will not be a restricted node.

**Examples**

**Example 1:**

```
Input: n = 7, edges = [[0,1],[1,2],[3,1],[4,0],[0,5],[5,6]], restricted = [4,5]
Output: 4
Explanation: The diagram above shows the tree.
We have that [0,1,2,3] are the only nodes that can be reached from node 0 without visiting a restricted node.
```

**Example 2:**

```
Input: n = 7, edges = [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], restricted = [4,2,1]
Output: 3
Explanation: The diagram above shows the tree.
We have that [0,5,6] are the only nodes that can be reached from node 0 without visiting a restricted node.
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- edges represents a valid tree.
- 1 <= restricted.length < n
- 1 <= restricted[i] < n
- All the values of restricted are unique.

---

## 题目（中文翻译）

有一棵 **无向树（undirected tree）**，包含 `n` 个节点，编号为 `0` 到 `n - 1`，以及 `n - 1` 条边。  
给定长度为 `n - 1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示在树中存在一条连接节点 `a_i` 与节点 `b_i` 的边。另给定整数数组 `restricted`，其中的节点为 **受限制节点（restricted node）**。  
返回从节点 `0` 出发，**不经过任何受限制节点** 时能够到达的最多节点数。  
注意，节点 `0` 本身一定不是受限制节点。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1**  
```text
Input: n = 7, edges = [[0,1],[1,2],[3,1],[4,0],[0,5],[5,6]], restricted = [4,5]
Output: 4
Explanation: 如上图所示，这棵树中只有节点 [0,1,2,3] 可以在不经过受限制节点的情况下从节点 0 到达。
```

**示例 2**  
```text
Input: n = 7, edges = [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], restricted = [4,2,1]
Output: 3
Explanation: 如上图所示，这棵树中只有节点 [0,5,6] 可以在不经过受限制节点的情况下从节点 0 到达。
```

**约束条件**  
- `2 <= n <= 10^5`  
- `edges.length == n - 1`  
- `edges[i].length == 2`  
- `0 <= a_i, b_i < n`  
- `a_i != b_i`  
- `edges` 构成一棵有效的树  
- `1 <= restricted.length < n`  
- `1 <= restricted[i] < n`  
- `restricted` 中的所有值互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把这棵树想象成一张地图，**节点**是城市，**边**是两城之间的直达道路。  
我们从城市 0 出发，只要路上不经过“禁行城市”（`restricted`），就可以到达该城市。  

最直接的想法是 **把所有可能的路径都枚举一遍**，只要路径上出现了禁行城市，就把这条路径丢掉，剩下的路径对应的终点就是可以到达的城市。

- **用到的数据结构**  
  - **邻接表**：把每条无向边 `[a, b]` 放进两个列表 `graph[a]` 与 `graph[b]` 中，类似于查字典，键是城市编号，值是相邻的城市集合。  
  - **递归/栈**：沿着一条路一路往下走，遇到死路就回溯（就像在迷宫里一步步尝试走每条可能的路）。  

- **为什么正确**  
  只要我们把 **所有** 从 0 开始的路径都遍历一遍，就一定会遍历到每一个可以到达的节点。只要在遍历过程中发现路径上出现了受限节点，就立刻终止这条路的继续搜索，保证不会误算受限节点。

- **时间/空间复杂度（大白话解释）**  
  - 树的节点数为 `n`，每条边只能走两次（去一次、回一次），但因为我们在每一次递归返回时都要把已经走过的路径重新遍历一次，最坏情况下会产生 **`O(n²)`** 的时间开销——可以把它想象成在一条长长的链子上，每走一步都要把前面所有已经走过的步数重新算一遍。  
  - 需要保存整棵树的邻接表以及递归栈，额外的空间是 **`O(n)`**（相当于在纸上画一张包含所有城市和道路的地图）。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Set

def reachableNodes_bruteforce(n: int, edges: List[List[int]], restricted: List[int]) -> int:
    # 1. 建立邻接表（类似查字典：城市 -> 相邻城市列表）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    restricted_set: Set[int] = set(restricted)   # 受限城市的集合，查找速度像在字典里找词一样快
    visited: Set[int] = set()                    # 已经到达过的城市，防止重复计数

    def dfs(node: int) -> None:
        """从 node 开始深度优先搜索，遇到受限城市就直接返回"""
        if node in restricted_set:   # 一旦走进禁区，立刻停止这条路
            return
        visited.add(node)            # 记录已经到达的城市
        for nxt in graph[node]:      # 试图往所有相邻的城市走
            if nxt not in visited:   # 防止走回头路（在树里其实不必检查，但这里保持一般性）
                dfs(nxt)             # 继续往下走

    dfs(0)                            # 从城市 0 出发
    return len(visited)               # 访问到的城市数量即为答案
```

#### 复杂度

- **时间复杂度**：`O(n²)`（在最坏情况下，每次递归都会遍历已经走过的路径，类似“重复走回头路”。）  
- **空间复杂度**：`O(n)`（邻接表 + 递归栈 + visited 集合）。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在：  
1. 每次递归都要检查是否已经访问过，而在树这种**无环**结构里，只要记住已经访问的节点，就不需要再次遍历已经走过的路径。  
2. 暴力解把“受限节点”当作普通节点去遍历，然后在进入时才返回，实际上我们可以在 **遍历之前** 把受限节点直接剔除，这样搜索过程根本不会进入这些节点，省掉了很多不必要的函数调用。

**优化思路**：

- 先把所有受限节点放进一个集合 `restricted_set`，在遍历时 **直接跳过**。  
- 使用 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）** 从节点 0 开始，只要相邻节点不在 `restricted_set` 且未被访问过，就加入搜索队列/栈。因为树没有环，这两种遍历方式的时间复杂度都是 `O(n)`。  
- BFS 更直观：一次把所有当前层的可达节点全部取出，层层推进；DFS 用递归或显式栈实现，同样只遍历每条边一次。

**核心算法/数据结构**：

- **哈希集合**（`set`）：用来快速判断一个节点是否受限，查找时间是常数级（就像在字典里找词一样快）。  
- **邻接表**：把树的结构保存下来，查询某个节点的所有邻居是 `O(1)`（直接取列表）。  
- **队列**（`collections.deque`）：BFS 需要先进先出地处理节点。  

**类比**：把树想成一条河流的支流网络，受限节点是被大坝拦住的支流。我们从源头（节点 0）顺流而下，只要遇到大坝就不再继续往下走。整个过程只需要一次顺流遍历，时间线性。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Set

def reachableNodes(n: int, edges: List[List[int]], restricted: List[int]) -> int:
    # 1. 建立邻接表（城市 -> 相邻城市列表）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    restricted_set: Set[int] = set(restricted)   # 受限城市集合，查询快如查字典
    visited: Set[int] = set([0])                 # 已经访问过的城市，先把起点 0 加进去
    q = deque([0])                               # BFS 队列，先放入起点

    while q:
        node = q.popleft()                       # 取出当前要处理的城市
        for nxt in graph[node]:                  # 看它的所有相邻城市
            # 只要相邻城市不在受限集合且没有被访问过，就可以进入
            if nxt not in restricted_set and nxt not in visited:
                visited.add(nxt)                 # 标记为已访问
                q.append(nxt)                    # 加入队列，后面继续扩展

    return len(visited)                          # 访问到的城市数量即为答案
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每条边只会被检查两次（一次从 `node` 向 `nxt`，一次相反方向），相当于只走了一遍树的所有道路。  
  - 与暴力解的 `O(n²)` 相比，省掉了大量重复遍历，真正意义上只用了线性时间。

- **空间复杂度**：`O(n)`  
  - 邻接表保存所有 `n‑1` 条边，需要 `O(n)` 空间。  
  - `visited`、`restricted_set`、以及 BFS 队列最坏情况下也会存 `O(n)` 个节点。  

---

## 心得

- **核心技巧**：在 **图/树的遍历** 过程中 **提前过滤** 不合法的节点（受限节点），并用 **哈希集合** 实现 O(1) 的快速判断。  
- **适用题型**：  
  1. “从起点出发，限制某些节点/边不能经过”的可达性问题（如 LeetCode 1971 `Find if Path Exists in Graph`）。  
  2. “在树/图中统计满足特定条件的子结构”——如“统计不含特定颜色的连通块”。  
- **解题钥匙**：**一次遍历 + 集合过滤**（一次遍历所有节点，遇到受限直接跳过）。

---

## 反思

- **第一反应**：看到“树”“受限节点”“从 0 出发”，自然想到 **图的遍历**（DFS/BFS），并在遍历时判断是否受限。  
- **最容易踩的坑**：  
  - **忘记把受限节点加入集合**，导致在遍历时仍然会进入它们，从而把受限节点计入答案。  
  - **没有去重**：在 DFS 中如果不记录 `visited`，树虽然无环，但递归返回时仍可能重复访问同一节点。  
  - **递归深度**：`n` 可达 `10⁵`，递归深度可能超出 Python 默认栈大小，使用 BFS 或显式栈更安全。  
- **下次类似题的第一步**：先 **把不允许经过的节点/边放进哈希集合**，然后 **用 BFS/DFS 从起点一次遍历**，只要满足 “未访问且不在限制集合” 就继续搜索。这样既简洁又高效。