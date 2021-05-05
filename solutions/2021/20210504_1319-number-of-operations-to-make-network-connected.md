# #1319. 使网络连通的最少操作次数 / Number of Operations to Make Network Connected

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)

---

## 题目（英文原版）

**Description**

There are n computers numbered from 0 to n - 1 connected by ethernet cables connections forming a network where connections[i] = [ai, bi] represents a connection between computers ai and bi. Any computer can reach any other computer directly or indirectly through the network.
You are given an initial computer network connections. You can extract certain cables between two directly connected computers, and place them between any pair of disconnected computers to make them directly connected.
Return the minimum number of times you need to do this in order to make all the computers connected. If it is not possible, return -1.

**Examples**

**Example 1:**

```
Input: n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
Explanation: Remove cable between computer 1 and 2 and place between computers 1 and 3.
```

**Example 2:**

```
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2
```

**Example 3:**

```
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
Explanation: There are not enough cables.
```

**Constraints**

- 1 <= n <= 105
- 1 <= connections.length <= min(n * (n - 1) / 2, 105)
- connections[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- There are no repeated connections.
- No two computers are connected by more than one cable.

---

## 题目（中文翻译）

有 `n` 台电脑，编号为 `0` 到 `n-1`，它们通过以太网线缆（ethernet cables）相连形成网络，其中 `connections[i] = [a_i, b_i]` 表示电脑 `a_i` 与电脑 `b_i` 之间的一根连接线。任意电脑都可以直接或间接地通过网络到达其他任意电脑。

给定初始的电脑网络 `connections`。你可以拔掉两台直接相连的电脑之间的某根线缆，然后把这根线缆重新接到任意一对尚未直接相连的电脑之间，使它们直接相连。

返回使所有电脑连通所需的最少操作次数。如果无法实现，返回 `-1`。

### 示例

**示例 1**  
输入: `n = 4, connections = [[0,1],[0,2],[1,2]]`  
输出: `1`  
解释: 拔掉电脑 `1` 与电脑 `2` 之间的线缆，重新接到电脑 `1` 与电脑 `3` 之间。

**示例 2**  
输入: `n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]`  
输出: `2`

**示例 3**  
输入: `n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]`  
输出: `-1`  
解释: 线缆数量不足，无法连通所有电脑。

### 约束条件

- `1 <= n <= 10^5`
- `1 <= connections.length <= min(n * (n - 1) / 2, 10^5)`
- `connections[i].length == 2`
- `0 <= a_i, b_i < n`
- `a_i != b_i`
- 不存在重复的连接。
- 任意两台电脑之间至多只有一根线缆相连。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有电脑都两两检查一遍，看它们能不能直接或间接连通**。  
我们可以把网络看成一张无向图，`connections[i] = [a, b]` 就是一条无向边。  
暴力做法：

1. 先把所有边放进一个邻接表（`list of list`），相当于把每台电脑的“朋友列表”记下来。  
2. 对每一台电脑 `i`，用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 把它能到达的所有电脑标记为已访问。  
3. 统计一共有多少个 **连通块**（即互相之间都能到达，但和其它块不相连的子图）。  
4. 若连通块的数量为 `c`，则我们需要把这些块两两连接起来，最少要 **`c‑1`** 条新线。  
5. 但是我们只能**搬动已有的线**，不能新增。搬动一根线相当于把它从某条边上取下来，再接到两个不同块之间。  
6. 所以，只要原来的线的总数 `len(connections)` **大于等于** `n‑1`（连通 `n` 台电脑最少需要 `n‑1` 条线），就一定能搬动足够的线；否则返回 `-1`。

> **类比**：把电脑想象成城市，线想象成道路。要让所有城市通行，只需要 `城市数‑1` 条道路（最小生成树）。如果道路本身不足，就算再搬也不够。

#### 代码（Python）

```python
from collections import defaultdict, deque

def makeConnected_bruteforce(n: int, connections: list[list[int]]) -> int:
    # 1. 先检查线是否足够
    if len(connections) < n - 1:          # 不够 n-1 条，根本不可能连通
        return -1

    # 2. 建立邻接表（每台电脑的直接相邻电脑列表）
    graph = defaultdict(list)
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)

    visited = [False] * n                 # 记录每台电脑是否已经遍历过
    components = 0                        # 连通块计数

    # 3. 用 BFS（也可以换成 DFS）遍历每个未访问的电脑，标记同一块的所有电脑
    for i in range(n):
        if not visited[i]:
            components += 1               # 发现新块
            q = deque([i])
            visited[i] = True
            while q:
                cur = q.popleft()
                for nb in graph[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)

    # 4. 需要的搬线次数 = 连通块数 - 1
    return components - 1
```

#### 复杂度

- **时间复杂度**：`O(n + m)`，其中 `m = len(connections)`。  
  - “`n`”是遍历所有电脑的代价，  
  - “`m`”是遍历所有线（每条线在邻接表里出现两次）的代价。  
  - 用大白话说，就是“遍历一次电脑表，遍历一次线表”，所以整体是线性时间。

- **空间复杂度**：`O(n + m)`。  
  - 邻接表需要存 `m` 条线的信息，  
  - `visited` 数组需要 `n` 个布尔值。  

---

### 2. 最优解

#### 思路  

暴力解已经是 `O(n+m)`，在本题的约束（`n ≤ 10⁵`、`m ≤ 10⁵`）下已经足够快。  
不过我们可以把 **“找连通块的数量”** 用 **并查集（Union‑Find）** 来实现，代码会更简洁，且不需要显式的邻接表。

**核心瓶颈**：在暴力解里，我们维护了一个完整的邻接表，空间上稍微多一点。如果只想统计连通块数量，实际上只需要 **“把属于同一个集合的电脑合并”**，不必记录每条边的具体邻居。

**并查集**的工作方式：

1. 每台电脑初始时是独立的集合（自己是自己的父节点）。  
2. 对每条线 `[a, b]`，把 `a` 和 `b` 所在的集合**合并**（union）。  
3. 合并后，所有在同一个集合里的电脑互相之间已经可以连通。  
4. 最后，统计有多少个不同的根节点（即有多少个不同的集合），这就是连通块的数量 `c`。  
5. 需要的搬线次数仍是 `c‑1`，前提是线的总数 `m` ≥ `n‑1`。

**并查集的两个关键操作**：

- **find(x)**：找出 `x` 所在集合的根节点，路径压缩（把查找路径上的节点直接挂到根上）可以让后续查询更快。  
- **union(x, y)**：把 `x`、`y` 两个集合合并，常用按秩（或按大小）合并，保持树的高度尽可能小。

> **类比**：把每台电脑想象成一个小岛，线是可以搭桥的材料。每搭一座桥就把两个小岛合并成一个更大的岛。最终我们只关心有多少块大岛。

#### 代码（Python）

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点的父亲，初始指向自己
        self.rank = [0] * n            # 按秩合并时的“高度”估计

    def find(self, x: int) -> int:
        # 路径压缩：递归找根的同时把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        # 合并两个集合，返回是否真的合并了（即根不同）
        rx, ry = self.find(x), self.find(y)
        if rx == ry:                     # 已经在同一个集合，无需合并
            return False
        # 按秩合并：把秩小的根挂到秩大的根下面
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

def makeConnected_unionfind(n: int, connections: list[list[int]]) -> int:
    # 1. 线不足直接返回 -1
    if len(connections) < n - 1:
        return -1

    uf = UnionFind(n)
    extra = 0                # 记录可以被搬动的多余线（已经在同一个集合内的线）

    # 2. 遍历每条线，尝试合并集合
    for a, b in connections:
        if not uf.union(a, b):   # 合并失败说明 a、b 已经连通，这条线是“冗余”的
            extra += 1

    # 3. 统计连通块数量
    roots = {uf.find(i) for i in range(n)}   # 把每个节点的根放进集合，去重后即为块数
    components = len(roots)

    # 4. 需要的搬线数 = components - 1
    #    只要 extra >= components - 1 就能完成（这里 extra 实际上等于 len(connections) - (n - components)）
    #    但因为我们已经在开头检查了 len(connections) >= n-1，必然满足
    return components - 1
```

#### 复杂度

- **时间复杂度**：`O(n + m·α(n))`，其中 `α` 是阿克曼函数的反函数，几乎可以看作常数。  
  - `find`、`union` 近乎 `O(1)`，所以遍历 `m` 条线的代价是线性。  
  - 再遍历 `n` 次求根节点得到块数也是线性。  
  - 与暴力解的 `O(n+m)` 本质相同，但常数更小，且不需要额外的邻接表。

- **空间复杂度**：`O(n)`。  
  - 只保存 `parent`、`rank` 两个长度为 `n` 的数组，省掉了存储所有邻接关系的空间。

---

## 心得

- **核心技巧**：**并查集（Union‑Find）** 用来快速统计连通块的数量，同时可以顺手统计“多余的线”。  
- **适用题型**：  
  1. 判断图是否连通或有多少连通块（如 LeetCode 547、323）。  
  2. “最小生成树”类的题目，需要知道已有的边是否足够（如 1169、1589）。  
  3. 动态连通性问题（离线查询、克鲁斯卡尔算法等）。  
- **一句话总结**：**把所有电脑看成集合，合并已有的线，剩余的集合数减一即为最少搬线次数。**

---

## 反思

- **第一反应**：检查线的总数是否足够 `n‑1`，然后数连通块，想到用 DFS/BFS。  
- **最容易踩的坑**：  
  - 忘记在 `len(connections) < n-1` 时直接返回 `-1`，导致后面计算出现负数或错误。  
  - 统计连通块时遗漏孤立的电脑（没有任何边的节点），必须把所有 `0 … n-1` 都遍历一遍。  
  - 并查集实现时没有路径压缩或按秩合并，导致在极端数据下性能下降。  
- **下次思路**：  
  1. **先检查资源是否足够**（线的数量）。  
  2. **快速统计连通块**——首选并查集，其次是 BFS/DFS。  
  3. **答案 = 块数 - 1**，并确认多余线是否足够（已在第一步保证）。