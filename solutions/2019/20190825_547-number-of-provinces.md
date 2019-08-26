# #547. 省份数量 / Number of Provinces

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/number-of-provinces/)

---

## 题目（英文原版）

**Description**

There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.
A province is a group of directly or indirectly connected cities and no other cities outside of the group.
You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.
Return the total number of provinces.

**Examples**

**Example 1:**

```
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
```

**Example 2:**

```
Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
```

**Constraints**

- 1 <= n <= 200
- n == isConnected.length
- n == isConnected[i].length
- isConnected[i][j] is 1 or 0.
- isConnected[i][i] == 1
- isConnected[i][j] == isConnected[j][i]

---

## 题目（中文翻译）

给定 **n** 个城市。其中一些城市之间有直接的连接，另一些则没有。如果城市 `a` 与城市 `b` 直接相连，且城市 `b` 与城市 `c` 直接相连，那么城市 `a` 与城市 `c` 之间是间接相连的。  

一个 **省份（province）** 是一组直接或间接相连的城市，并且该组之外不存在与之相连的其他城市。  

你将得到一个 `n × n` 的矩阵 `isConnected`，其中 `isConnected[i][j] = 1` 表示第 `i` 个城市和第 `j` 个城市直接相连，`isConnected[i][j] = 0` 表示它们不直接相连。  

请返回省份的总数。

## 示例

### 示例 1

**输入**  
```text
isConnected = [[1,1,0],
               [1,1,0],
               [0,0,1]]
```

**输出**  
```text
2
```

**解释**  
城市 0 与城市 1 直接相连，形成一个省份；城市 2 与其他城市均不相连，形成另一个省份。因此共有 2 个省份。

### 示例 2

**输入**  
```text
isConnected = [[1,0,0],
               [0,1,0],
               [0,0,1]]
```

**输出**  
```text
3
```

**解释**  
每个城市都仅与自身相连，彼此之间没有任何直接或间接的连接，所以每个城市各自构成一个省份，共计 3 个省份。

## 约束条件

- `1 <= n <= 200`
- `n == isConnected.length`
- `n == isConnected[i].length`
- `isConnected[i][j]` 只能取 `0` 或 `1`
- `isConnected[i][i] == 1`（每个城市与自身相连）
- `isConnected[i][j] == isConnected[j][i]`（连接关系是对称的）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题本质上是在 **无向图** 中求连通块的个数。  
- 每个城市是图中的一个节点。  
- `isConnected[i][j] = 1` 表示节点 `i` 与节点 `j` 之间有一条无向边（直接相连）。  

最直接的做法是：从任意未访问过的城市出发，沿着所有可以到达的城市“走遍”，把走过的城市标记为已访问。走完一次后，就得到一个 **省（province）**。再找下一个未访问的城市，重复同样的过程，直到所有城市都被访问。  

这就是 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 的经典思路。可以把 DFS 想象成“在城市之间不停地往前走”，每走到一个新城市，就继续从这座城市出发探索它的邻居，直到走不下去为止。

> **数据结构类比**  
> - **邻接矩阵** `isConnected` 像一本“城市联络簿”，行号和列号是城市编号，格子里的 `1/0` 告诉我们两座城市是否直接相连。  
> - **visited 列表** 像一本“已走访城市的名单”，防止我们重复走同一座城市。

只要我们把所有可以相互到达的城市全部访问完，就一定找到了一个完整的省；剩下的未访问城市必然属于其他省。  

#### 代码（Python）

```python
from typing import List

def findCircleNum(isConnected: List[List[int]]) -> int:
    n = len(isConnected)                 # 城市数量
    visited = [False] * n                # 记录每座城市是否已访问

    def dfs(city: int) -> None:
        """深度优先遍历：把 city 能到达的所有城市都标记为已访问"""
        visited[city] = True
        for neighbor in range(n):        # 遍历所有可能的邻居
            # 如果 neighbor 与 city 直接相连且还没有被访问，就继续递归
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)

    provinces = 0                         # 省的计数器
    for i in range(n):
        if not visited[i]:                # 找到一个新的未访问城市 → 新的省
            provinces += 1
            dfs(i)                        # 把这个省内部的所有城市都访问掉
    return provinces
```

**关键行中文注释** 已写在代码里，直接跑即可。

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 我们会遍历整个 `n × n` 的矩阵（每次 DFS 要检查一行的所有列），所以即使图很稀疏，最坏情况下仍然是 `n²` 次检查。  
  - 用大白话说，就是如果有 200 座城市，最多要检查 40,000 次“这两座城市是否直接相连”。  

- **空间复杂度：** `O(n)`  
  - 主要是 `visited` 数组占用 `n` 的空间，以及递归调用栈最深也不会超过 `n`（最坏情况是一条链式相连的城市）。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈** 在于我们每次都要遍历整行 `isConnected[i]` 来寻找相邻城市。其实，这一步是不可避免的（因为输入本身就是邻接矩阵），但我们可以把“寻找连通块”的过程改写成 **并查集（Union‑Find）**，这样代码更简洁，且在需要频繁合并集合时更高效。

**并查集的核心思想**  
- 把每座城市先看作一个独立的集合（每个集合代表一个省）。  
- 当我们发现 `isConnected[i][j] = 1`（i 与 j 直接相连）时，就把 i 所在的集合和 j 所在的集合 **合并**（union）。  
- 最后，不同集合的根节点（representative）数量就是省的数量。

> **类比**：想象每座城市都有一张“身份证”。相连的城市会把自己的身份证贴在一起，形成一张“大卡片”。所有贴在同一张卡片上的城市，就属于同一个省。并查集帮我们快速找到每张卡片的“领袖”（根），并在需要时把两张卡片粘合在一起。

**路径压缩（Path Compression）** 与 **按秩合并（Union by Rank）**  
- 为了让 `find`（寻找根）操作更快，我们在查询时把沿途的节点直接挂到根上（路径压缩）。  
- 合并时把“小树挂到大树下”，避免树过深（按秩合并）。这两点让并查集的时间几乎是 **近似 O(1)**，整体仍然是 `O(n²)`（因为要检查矩阵），但常数更小，代码更具可读性。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集实现，带路径压缩和按秩合并"""
    def __init__(self, size: int):
        self.parent = list(range(size))   # 初始时每个节点是自己的父亲（根）
        self.rank = [0] * size            # 用来记录树的“秩”（近似深度）

    def find(self, x: int) -> int:
        """寻找 x 所在集合的根节点，并做路径压缩"""
        if self.parent[x] != x:
            # 递归寻找根的同时，把 x 直接挂到根上
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """把 x 和 y 所在的集合合并"""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:          # 已经在同一个集合，无需合并
            return

        # 按秩合并：把秩小的根挂到秩大的根下
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:                         # 秩相等时随便挂一个，并把秩加 1
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def findCircleNum(isConnected: List[List[int]]) -> int:
    n = len(isConnected)
    uf = UnionFind(n)

    # 只遍历上三角矩阵即可（因为 isConnected 对称）
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)       # 把相连的两座城市合并到同一个集合

    # 统计不同根的数量，即为省的个数
    roots = set()
    for i in range(n):
        roots.add(uf.find(i))
    return len(roots)
```

#### 复杂度  

- **时间复杂度：** `O(n² α(n))` ≈ `O(n²)`  
  - `α(n)` 是 Ackermann 函数的反函数，几乎可以看作常数（即使 n=200 也几乎为 1）。  
  - 主要耗时仍是遍历上三角矩阵的 `n²/2` 次检查。  

- **空间复杂度：** `O(n)`  
  - 只用了 `parent`、`rank` 两个长度为 `n` 的数组，以及一个 `set` 用来统计根。  

与暴力 DFS 相比，**并查集的优势** 在于代码结构更清晰，且在需要多次合并/查询的更大规模图时表现更好。

---  

## 心得  

- **核心技巧**：**并查集（Union‑Find）** —— 用来快速管理“属于同一个集合”的元素，尤其适用于“连通块”类问题。  
- **适用的题型**（类似题）  
  1. **Friend Circles**（朋友圈）—— 与本题本质相同，只是描述换成了“朋友关系”。  
  2. **Number of Connected Components in an Undirected Graph**（无向图连通块计数）。  
  3. **Redundant Connection**（冗余连接）—— 需要判断加入一条边后是否会形成环，同样用并查集检测是否已在同一集合。  
- **一句话总结解题钥匙**：把“相连的城市”看成“可以贴在同一张卡片上的城市”，用并查集把卡片合并，卡片的数量就是省的数量。  

---  

## 反思  

- **第一反应**：看到“直接或间接相连”立刻想到图的连通块，脑中自然浮现 DFS/BFS 的搜索过程。  
- **最容易踩的坑**  
  1. **遍历全矩阵导致重复合并**：如果不限制只遍历上三角（`j > i`），会把同一条边处理两次，虽然不影响正确性，但会多余的 `union` 操作。  
  2. **忘记把 `isConnected[i][i]` 视为已连接**：其实对并查集没有影响，因为每个节点本来就是自己的集合。  
  3. **路径压缩写错**：如果在 `find` 中没有返回根节点，后面的 `union` 会出错。  
- **下次遇到同类题的第一步**：先判断是“查询连通性”还是“合并连通性”。如果只需要一次遍历统计连通块，直接用并查集；如果需要在遍历过程中实时输出或搜索路径，考虑 DFS/BFS。  

祝你在算法的旅程中越走越稳，玩转图与并查集！