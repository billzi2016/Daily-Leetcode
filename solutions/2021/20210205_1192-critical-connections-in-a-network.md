# #1192. 网络中的关键连接 / Critical Connections in a Network

> 难度：困难 · 标签：Depth-First Search、Graph、Biconnected Component · [LeetCode 链接](https://leetcode.com/problems/critical-connections-in-a-network/)

---

## 题目（英文原版）

**Description**

There are n servers numbered from 0 to n - 1 connected by undirected server-to-server connections forming a network where connections[i] = [ai, bi] represents a connection between servers ai and bi. Any server can reach other servers directly or indirectly through the network.
A critical connection is a connection that, if removed, will make some servers unable to reach some other server.
Return all critical connections in the network in any order.

**Examples**

**Example 1:**

```
Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
Output: [[1,3]]
Explanation: [[3,1]] is also accepted.
```

**Example 2:**

```
Input: n = 2, connections = [[0,1]]
Output: [[0,1]]
```

**Constraints**

- 2 <= n <= 105
- n - 1 <= connections.length <= 105
- 0 <= ai, bi <= n - 1
- ai != bi
- There are no repeated connections.

---

## 题目（中文翻译）

**描述**  
有 `n` 台服务器，编号从 `0` 到 `n - 1`，它们通过无向的服务器间连接形成一个网络，其中 `connections[i] = [a_i, b_i]` 表示服务器 `a_i` 与服务器 `b_i` 之间存在一条连接。任意服务器都可以直接或间接地通过网络到达其他服务器。  
**关键连接**（critical connection）指的是如果移除该连接，就会导致某些服务器无法再相互到达的连接。  
返回网络中所有的关键连接，顺序任意。

**示例 1**  
```text
Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
Output: [[1,3]]
Explanation: [[3,1]] 也被视为正确答案。
```

**示例 2**  
```text
Input: n = 2, connections = [[0,1]]
Output: [[0,1]]
```

**约束条件**  

- `2 <= n <= 10^5`
- `n - 1 <= connections.length <= 10^5`
- `0 <= a_i, b_i <= n - 1`
- `a_i != b_i`
- 不存在重复的连接。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐条删除**网络中的每一条连接，然后检查网络是否仍然是连通的。  
- **数据结构**：我们把服务器和连接看成**无向图**，用邻接表（`defaultdict(list)`）来存储每个服务器的邻居。邻接表就像一本“朋友名单”，每个人（服务器）都有一张写着所有朋友（相邻服务器）的卡片。  
- **检查连通性**：删除一条边后，从任意一个服务器（例如 0）出发，用 **DFS**（深度优先搜索）或 **BFS**（广度优先搜索）遍历所有能到达的服务器。如果遍历结束后还有服务器没有被访问到，说明这条被删掉的边是**关键连接**。  
- **为什么正确**：关键连接的定义恰好是“删掉它会导致图不再连通”。我们把每一条边都尝试删掉一次，并用遍历验证连通性，必然能找出所有满足条件的边。

#### 代码（Python）

```python
from collections import defaultdict, deque
from copy import deepcopy
from typing import List

def critical_connections_bruteforce(n: int, connections: List[List[int]]) -> List[List[int]]:
    # 建立邻接表
    graph = defaultdict(list)
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)

    def bfs(start: int, g: dict) -> set:
        """从 start 出发，用 BFS 找到所有可达的节点，返回 visited 集合"""
        visited = set([start])
        q = deque([start])
        while q:
            node = q.popleft()
            for nb in g[node]:
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        return visited

    critical = []
    # 逐条尝试删除每一条边
    for a, b in connections:
        # 深拷贝一份图，防止修改原图
        g_copy = deepcopy(graph)
        # 删除当前边 (a,b)
        g_copy[a].remove(b)
        g_copy[b].remove(a)

        # 检查图是否仍然连通
        reachable = bfs(0, g_copy)          # 任意节点都行，这里选 0
        if len(reachable) != n:              # 有服务器不可达 → 关键连接
            critical.append([a, b])

    return critical
```

#### 复杂度  

- **时间复杂度**：`O(E * (V + E))`  
  - 对每条边 `E`（即 `len(connections)`）我们都要重新遍历一次图。遍历一次（BFS/DFS）需要查看所有节点 `V` 和所有边 `E`，所以总共是 `E` 次的 `O(V+E)`。  
  - 用大白话讲，就是如果图有 10 条边、5 个服务器，最坏情况要做 10 × (5 + 10) = 150 次基本操作，规模稍大时会很慢。  
- **空间复杂度**：`O(V + E)`  
  - 需要保存邻接表和 BFS 队列，和原图的大小相同。拷贝图时会再占用一次同样的空间，但这属于常数倍的额外开销。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每删一条边都要重新遍历整个图**，导致时间复杂度是二次的。  
我们需要在一次遍历中**直接判断哪条边是桥（bridge）**——桥正是关键连接的另一种叫法。  

**Tarjan 的桥算法** 能在一次深度优先搜索（DFS）里找出所有桥，核心概念是 **low-link 值**。下面一步步解释：

1. **DFS 编号（发现时间）**  
   - 当我们第一次进入一个节点 `u` 时，给它一个递增的时间戳 `disc[u]`（相当于给它贴上“出生时间”）。  
   - 这个时间戳帮助我们判断两个节点的先后关系。

2. **low[u] 的含义**  
   - `low[u]` 表示从 `u` 出发，沿 **DFS 树的子树**（包括 `u` 本身）能够回到的**最早的时间戳**的节点。  
   - 换句话说，`low[u]` 是子树里可以“往回溯”到的最早祖先的时间。  

3. **桥的判定**  
   - 考虑一条 DFS 树中的树边 `(u, v)`（`u` 是父，`v` 是子）。  
   - 如果 `low[v] > disc[u]`，说明 **从 `v` 以及它的所有后代**，**无法**通过非树边回到 `u` 或 `u` 之前的节点。  
   - 这时，删除 `(u, v)` 会把 `v` 子树与其余部分割裂，**恰好是关键连接**。  

4. **如何更新 low 值**  
   - 对每个相邻节点 `w`：  
     - 如果 `w` 还未被访问，则递归 DFS，随后 `low[u] = min(low[u], low[w])`。  
     - 如果 `w` 已经被访问且 **不是父节点**，说明 `u` 与 `w` 之间有一条**回边**（back edge），可以把 `low[u]` 更新为 `min(low[u], disc[w])`（因为 `w` 的发现时间更早）。  

5. **实现细节**  
   - 为了快速判断一条边是否是桥，我们在遍历时直接把满足 `low[v] > disc[u]` 的 `(u, v)` 加入答案。  
   - 为了避免重复计数，答案统一存成 `[min(u,v), max(u,v)]` 的形式。  

**类比**：想象每个服务器是一座城堡，连接是桥梁。DFS 编号像给每座城堡贴上建造的先后顺序；`low` 值像城堡能通过哪座最早建造的桥返回到更早的城堡。如果从城堡 `v` 出发，**找不到**任何比 `u` 更早的桥可以回去，那么 `u-v` 这座桥就是唯一的“唯一通道”，删除后两边就会孤立——这正是关键连接。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def critical_connections(n: int, connections: List[List[int]]) -> List[List[int]]:
    # 1️⃣ 建立邻接表（朋友名单）
    graph = defaultdict(list)
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)

    # 2️⃣ 初始化数组
    disc = [-1] * n          # 发现时间，-1 表示未访问
    low  = [0] * n           # low-link 值
    time = 0                 # 全局时间戳
    bridges = []             # 保存关键连接

    # 3️⃣ 深度优先搜索
    def dfs(u: int, parent: int):
        nonlocal time
        disc[u] = low[u] = time   # 为 u 贴上时间戳
        time += 1

        for v in graph[u]:
            if v == parent:       # 跳过走回去的那条树边
                continue
            if disc[v] == -1:     # v 还没被访问 → 树边
                dfs(v, u)         # 递归探索子节点
                # 回溯后更新 low[u]
                low[u] = min(low[u], low[v])
                # 判断是否为桥
                if low[v] > disc[u]:
                    bridges.append([u, v])
            else:                 # v 已访问且不是父节点 → 回边
                low[u] = min(low[u], disc[v])

    # 4️⃣ 可能图不是连通的（虽然题目保证连通），遍历所有节点
    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)

    # 5️⃣ 统一返回格式（小的在前）
    return [[min(u, v), max(u, v)] for u, v in bridges]
```

#### 复杂度  

- **时间复杂度**：`O(V + E)`  
  - 我们只进行一次 DFS，遍历每个节点一次、每条边两次（因为是无向图）。用大白话说，就是如果有 100,000 台服务器和 200,000 条连接，算法只需要大约 300,000 次基本操作，远远快于暴力的二次遍历。  
- **空间复杂度**：`O(V + E)`  
  - 需要存储邻接表、`disc`、`low` 以及递归栈（最坏深度 `V`）。这与图本身的大小成正比，属于线性空间。

---

## 心得

- **核心技巧**：Tarjan 桥算法（利用 DFS 的发现时间和 low‑link 值一次遍历找出所有桥）。  
- **适用题型**：  
  1. **Critical Connections in a Network**（本题）  
  2. **Bridges in a Graph**（LeetCode 1192 变体）  
  3. **Critical Connections / 关节点**（寻找割点，思路类似，只是判断 `low[child] >= disc[parent]`）  
- **一句话总结**：把“删边后是否断连”转化为“在一次 DFS 中看子树能否回到更早的祖先”，满足 `low[child] > disc[parent]` 的边即为关键连接。

---

## 反思

- **第一反应**：直接想到“遍历每条边，删掉后再检查连通性”，因为这最符合题目文字描述。  
- **最容易踩的坑**：  
  - **递归深度**：`n` 可达 `10^5`，递归可能触发 Python 的递归深度限制，需要 `sys.setrecursionlimit(10**6)` 或改写为显式栈。  
  - **回边判断**：一定要排除父节点，否则会把树边误当成回边，导致 `low` 计算错误。  
  - **返回格式**：答案中每条边的顺序不要求，但同一条桥可能被记录为 `[u,v]` 或 `[v,u]`，统一成 `[min, max]` 更安全。  
- **下次类似题的第一步**：先判断“是否可以用一次 DFS 把全局属性（如连通性、割点、桥）全部算出来”，若可以，就立刻考虑 **Tarjan** 或 **双指针/前缀和** 等一次遍历的线性算法，而不是先写暴力枚举。