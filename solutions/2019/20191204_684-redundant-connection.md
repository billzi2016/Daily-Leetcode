# #684. 冗余连接 / Redundant Connection

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/redundant-connection/)

---

## 题目（英文原版）

**Description**

In this problem, a tree is an undirected graph that is connected and has no cycles.
You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.
Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.

**Examples**

**Example 1:**

```
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
```

**Example 2:**

```
Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]
```

**Constraints**

- n == edges.length
- 3 <= n <= 1000
- edges[i].length == 2
- 1 <= ai < bi <= edges.length
- ai != bi
- There are no repeated edges.
- The given graph is connected.

---

## 题目（中文翻译）

在本题中，树（tree）是一个连通且无环的无向图（undirected graph）。  
给定的图最初是一棵有 n 个节点的树，节点编号为 1 到 n，随后额外添加了一条边（edge）。新增的边连接了编号在 1 到 n 之间的两个不同顶点（vertex），且这条边在原图中不存在。图用长度为 n 的数组 `edges` 表示，其中 `edges[i] = [ai, bi]` 表示节点 `ai` 与节点 `bi` 之间存在一条边。

返回可以删除的那条边，使得剩余的图成为包含 n 个节点的树。如果存在多条满足条件的边，返回在输入中出现最靠后的那条。

Example 1:
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]

Example 2:
Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]

约束条件：
- n == edges.length
- 3 <= n <= 1000
- edges[i].length == 2
- 1 <= ai < bi <= edges.length
- ai != bi
- 不存在重复的边
- 给定的图是连通的

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目给出的是 **一个本来是树的无向图**，后来又多加了一条边。  
> 树的特点：节点之间都连通且**没有环**（也就是说，任意两点之间恰好有唯一一条路径）。

所以我们只需要找出 **导致环出现的那条边**，把它删掉后图就会恢复成树。  
最直接的暴力想法是：

1. **枚举每一条边**，假设把它暂时删除。  
2. 用 **DFS（深度优先搜索）或 BFS（广度优先搜索）** 检查剩下的 `n-1` 条边是否还能把所有 `n` 个节点连通且没有环。  
   - 连通：从任意节点出发能遍历到所有节点。  
   - 没有环：在遍历时如果发现已经访问过的节点再被访问，就说明有环。  

如果删除这条边后图仍然是连通且无环，则说明这条边就是多余的。  
因为题目要求 **返回最后出现的答案**，我们只要从左到右枚举，记录每一次符合条件的边，遍历结束时返回记录的最后一条即可。

> **数据结构类比**：  
> - **邻接表**（list of lists）可以想象成“每个人的朋友名单”。我们把每条边当作“朋友关系”。  
> - **哈希集合**（set）像“检查有没有见过某个人”，用于 DFS 中的 “已访问” 标记。  

#### 代码（Python）  

```python
from collections import defaultdict, deque
from typing import List

def findRedundantConnection_bruteforce(edges: List[List[int]]) -> List[int]:
    n = len(edges)                         # 节点数 = 边数
    # ---------- 建立邻接表 ----------
    adj = defaultdict(list)                # 每个节点对应的邻居列表
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # ---------- 检查删除第 i 条边后是否仍是树 ----------
    def is_tree_without_edge(skip_idx: int) -> bool:
        """返回在忽略第 skip_idx 条边的情况下，图是否仍然是连通且无环"""
        visited = set()
        # 从任意节点（这里选 1）开始 BFS
        q = deque([1])
        visited.add(1)

        while q:
            cur = q.popleft()
            for nxt in adj[cur]:
                # 跳过被“删掉”的那条边
                if (cur == edges[skip_idx][0] and nxt == edges[skip_idx][1]) or \
                   (cur == edges[skip_idx][1] and nxt == edges[skip_idx][0]):
                    continue
                if nxt in visited:          # 已经访问过，说明出现环
                    continue               # 环已经被检测到，继续遍历即可
                visited.add(nxt)
                q.append(nxt)

        # 连通性：所有 n 个节点都被访问到了
        return len(visited) == n

    answer = None
    # 从左到右枚举每一条边，记录符合条件的（因为要返回最后出现的）
    for i in range(len(edges)):
        if is_tree_without_edge(i):
            answer = edges[i]               # 记录，后面的会覆盖前面的

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n * (n + m))`，这里 `n` 为节点数（等于 `edges.length`），`m = n-1` 为剩余边数。  
  - 我们对每条边都做一次 BFS，BFS 本身遍历所有节点和边是 `O(n + m)`，所以总共是 `O(n^2)`。  
  - 用大白话说，就是如果有 1000 条边，最坏要做 1000 次遍历，每次遍历大约要看 2000 次（节点+边），大约 2 百万次操作，勉强能跑完，但不是最优的。  

- **空间复杂度**：`O(n + m)` 用于邻接表和 BFS 队列/访问集合，约 `O(n)`。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次都要重新遍历整张图**，导致 `O(n^2)` 的时间。  
我们可以利用 **并查集（Union‑Find）** 把“是否已经在同一个连通分量”这一查询压缩到近乎 `O(1)` 的时间。

**并查集**可以类比为“学校的班级”。  
- 每个学生（节点）一开始都有自己的班级（自己是根）。  
- 当两位学生成为朋友（加一条边）时，我们把他们所在的班级合并。  
- 如果两位学生已经在同一个班级里，却又再加一条朋友关系，这条新关系必然会把已经在同一个集合里的两个人连在一起，形成环。  

具体步骤：

1. 初始化并查集，`parent[i] = i` 表示每个节点自成一组。  
2. 依次遍历 `edges` 中的每条边 `[u, v]`：  
   - 用 `find(u)`、`find(v)` 找到它们各自所在的根（即班级）。  
   - **如果根相同**，说明 `u` 和 `v` 已经在同一个连通分量，加入这条边会产生环，此时这条边就是 **多余的**。  
   - **如果根不同**，说明这条边是安全的，执行 `union(u, v)` 把两个集合合并。  
3. 因为我们要返回 **最后出现的** 多余边，只要遍历顺序保持原来的顺序，**第一个检测到环的边就是答案**（因为后面的边在出现环之前已经被加入，后面的环边一定在后面出现）。  

> **路径压缩**：在 `find` 操作时把沿途的节点直接挂到根节点下，后续查询更快。  
> **按秩合并（union by rank）**：把小树挂到大树下，保持树的高度尽可能小。  

#### 代码（Python）  

```python
from typing import List

class UnionFind:
    """并查集实现（带路径压缩和按秩合并）"""
    def __init__(self, size: int):
        self.parent = list(range(size + 1))   # parent[i] = i，0 位置不使用
        self.rank = [0] * (size + 1)          # 用于按秩合并，记录树的深度

    def find(self, x: int) -> int:
        """返回 x 所在集合的根节点，同时做路径压缩"""
        if self.parent[x] != x:
            # 递归找根的同时，把 x 直接挂到根下
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        合并 x、y 所在的集合。
        返回 True 表示成功合并（原本不在同一个集合），
        返回 False 表示 x、y 已经在同一个集合，合并会形成环。
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:          # 已经同根，加入会造环
            return False

        # 按秩合并：把深度小的根挂到深度大的根下
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:                         # 深度相同，随便挂一个，同时深度加 1
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


def findRedundantConnection(edges: List[List[int]]) -> List[int]:
    n = len(edges)                     # 节点数等于边数
    uf = UnionFind(n)

    for u, v in edges:
        # 如果 union 返回 False，说明 u、v 已经连通，当前这条边多余
        if not uf.union(u, v):
            return [u, v]

    # 题目保证一定有答案，这行理论上不会到达
    return []
```

#### 复杂度  

- **时间复杂度**：`O(n * α(n))`，其中 `α` 为 Ackermann 函数的逆，几乎可以视作常数。  
  - 每条边只做一次 `find`/`union`，每次操作的均摊复杂度是 **近乎 O(1)**，所以整体是线性 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，快了好几个数量级。  

- **空间复杂度**：`O(n)`，用于存放 `parent`、`rank` 两个数组。  

---

## 心得  

- **核心技巧**：**并查集（Union‑Find）** 用来快速判断两点是否已经在同一个连通分量，从而检测环。  
- **适用的题型**：  
  1. **Redundant Connection**（本题）  
  2. **Redundant Connection II**（处理有向图的环）  
  3. **Number of Islands II**（逐步加入陆地并统计连通块）  
- **一句话总结解题钥匙**：  
  “在无向图中，**如果两个节点已经连通，再加一条边必然形成环**，并查集帮你在常数时间内判断连通性。”

---

## 反思  

- **第一反应**：看到“树 + 多余一条边”，马上想到“环”。于是想直接遍历找环，想到 DFS/BFS。  
- **最容易踩的坑**：  
  - 忽略 **返回最后出现的多余边**，如果不按顺序记录，可能返回最先出现的错误答案。  
  - 并查集实现时忘记 **路径压缩** 或 **按秩合并**，导致最坏情况下退化成 `O(n²)`。  
  - 输入节点编号是从 `1` 开始，而数组索引从 `0`，需要在并查集里额外开一个位置或做偏移。  
- **下次遇到同类题**，第一步应该想到：  
  - “这是一张几乎是树的图，是否可以用并查集检测‘已连通再连’的情况？”  

这样从一开始就把时间复杂度压到线性，事半功倍。祝你编码愉快！