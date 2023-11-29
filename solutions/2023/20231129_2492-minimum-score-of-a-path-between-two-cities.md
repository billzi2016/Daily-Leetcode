# #2492. 两城之间路径的最小分数 / Minimum Score of a Path Between Two Cities

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n representing n cities numbered from 1 to n. You are also given a 2D array roads where roads[i] = [ai, bi, distancei] indicates that there is a bidirectional road between cities ai and bi with a distance equal to distancei. The cities graph is not necessarily connected.
The score of a path between two cities is defined as the minimum distance of a road in this path.
Return the minimum possible score of a path between cities 1 and n.
Note:

**Examples**

**Example 1:**

```
Input: n = 4, roads = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]
Output: 5
Explanation: The path from city 1 to 4 with the minimum score is: 1 -> 2 -> 4. The score of this path is min(9,5) = 5.
It can be shown that no other path has less score.
```

**Example 2:**

```
Input: n = 4, roads = [[1,2,2],[1,3,4],[3,4,7]]
Output: 2
Explanation: The path from city 1 to 4 with the minimum score is: 1 -> 2 -> 1 -> 3 -> 4. The score of this path is min(2,2,4,7) = 2.
```

**Constraints**

- 2 <= n <= 105
- 1 <= roads.length <= 105
- roads[i].length == 3
- 1 <= ai, bi <= n
- ai != bi
- 1 <= distancei <= 104
- There are no repeated edges.
- There is at least one path between 1 and n.

---

## 题目（中文翻译）

给定一个正整数 `n`，表示编号为 `1` 到 `n` 的 `n` 个城市。还给定一个二维数组 `roads`，其中 `roads[i] = [ai, bi, distancei]` 表示城市 `ai` 与城市 `bi` 之间有一条 **双向道路（bidirectional road）**，其长度为 `distancei`。城市之间的图（graph）不一定是连通的。  

一条 **路径（path）** 的分数定义为该路径上所有道路的长度的最小值。求从城市 `1` 到城市 `n` 的所有可能路径中，能够得到的最小分数。  

**示例 1**  
**输入**: `n = 4, roads = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]`  
**输出**: `5`  
**解释**: 分数最小的路径为 `1 -> 2 -> 4`，其分数为 `min(9,5) = 5`。可以证明不存在分数更小的路径。  

**示例 2**  
**输入**: `n = 4, roads = [[1,2,2],[1,3,4],[3,4,7]]`  
**输出**: `2`  
**解释**: 分数最小的路径为 `1 -> 2 -> 1 -> 3 -> 4`，其分数为 `min(2,2,4,7) = 2`。  

**约束条件**  
- `2 <= n <= 10^5`  
- `1 <= roads.length <= 10^5`  
- `roads[i].length == 3`  
- `1 <= ai, bi <= n`  
- `ai != bi`  
- `1 <= distancei <= 10^4`  
- 不存在重复的道路。  
- 必然存在至少一条从城市 `1` 到城市 `n` 的路径。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的路径都枚举出来**，然后对每条路径求出它的「分数」——路径上所有道路长度的最小值，最后取所有路径分数的最小值。

- **数据结构**：我们可以把城市和道路看成**无向图**，用邻接表（`dict[int, List[Tuple[int,int]]]`）来存储。  
  - 类比：邻接表就像一本城市通讯录，键是城市编号，值是这座城市直接相连的（邻居城市，路程）列表。  
- **枚举路径**：用深度优先搜索（DFS）或广度优先搜索（BFS）从城市 `1` 开始遍历，每走一步把当前路径上出现的最小路程记录下来。  
- **终止条件**：当搜索到城市 `n` 时，把当前路径的最小路程与全局答案比较，取更小的那个。  

这种做法**一定能得到正确答案**，因为我们把「所有」合法路径都考虑到了。

但是，它的时间复杂度非常高：  
- 在最坏情况下（图是完全连通的），从 `1` 到 `n` 的路径数量是指数级的（类似“树的所有根到叶子的路径”），搜索会遍历指数级的状态。  
- 即使只做一次普通的 DFS，仍然会遍历每条边一次，得到 **O(V+E)**，但我们还要在每条搜索路径上维护最小值，导致**大量重复计算**。

所以暴力解在 `n`、`roads` 达到 `10⁵` 的规模时根本跑不动。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def minScore_bruteforce(n: int, roads: List[List[int]]) -> int:
    # 建立邻接表
    graph = defaultdict(list)
    for u, v, w in roads:
        graph[u].append((v, w))
        graph[v].append((u, w))

    ans = float('inf')
    visited = [False] * (n + 1)

    def dfs(u: int, cur_min: int) -> None:
        """从 u 出发的 DFS，cur_min 为当前路径上出现的最小路程"""
        nonlocal ans
        if u == n:                     # 到达终点，更新答案
            ans = min(ans, cur_min)
            return
        visited[u] = True
        for v, w in graph[u]:
            if not visited[v]:
                dfs(v, min(cur_min, w))   # 把当前最小值和这条边的长度取较小
        visited[u] = False               # 允许其他路径再次经过 u

    dfs(1, float('inf'))
    return ans
```

> **注意**：这段代码只用于说明「暴力思路」，在大数据范围下会 **超时**（Time Limit Exceeded）。

#### 复杂度

- **时间复杂度**：`O(所有可能路径的数量)`，在最坏情况下是指数级的，实际会远远超出 `10⁵` 的限制。  
- **空间复杂度**：`O(V+E)` 用于存储图，外加递归栈最多 `O(V)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于“遍历所有路径”**。我们要思考：**到底需要遍历多少路径才能得到答案？**  

观察题目定义：

> 路径的分数 = 这条路径上所有道路长度的**最小值**。

换个角度：只要我们能够**找到任意一条从 1 到 n 的路径**，这条路径上最小的那条边的长度，就是答案的一个上界。我们希望把这个上界降到最低。

关键事实：

1. **只要城市 1 与城市 n 在同一个连通分量（connected component）里，** 那么**在这个连通分量的所有边中，最小的边长度一定可以被某条从 1 到 n 的路径“使用”。**  
   - 为什么？因为连通分量里任意两点都有路径相连。设 `e_min` 是该分量中权重最小的那条边，端点为 `a`、`b`。由于 `1` 与 `n` 与 `a`、`b` 都在同一个分量，我们可以先从 `1` 走到 `a`（或 `b`），再走这条最小边 `e_min`，再从另一端走到 `n`。于是这条路径的最小边就是 `e_min` 本身。

2. 因此**答案 = 连通分量（包含 1 和 n）中所有边的最小权重**。我们不需要真正找出具体的路径。

基于上述思路，求解步骤如下：

- **步骤 1：找出与城市 1 连通的所有城市**。可以用 BFS/DFS 或并查集（Union‑Find）实现。  
- **步骤 2：在这些连通的城市内部遍历所有道路，记录出现的最小距离**。这一步只需要一次线性扫描 `roads`，因为每条边我们都可以判断它的两个端点是否都在「1 的连通分量」里。

这两个步骤的时间都是 **线性** 的，完全可以应对 `10⁵` 规模。

下面分别给出 **并查集** 与 **DFS** 两种实现，任选其一即可。这里使用 **并查集**（Union‑Find），因为它写起来简洁且天然支持“快速判断两个节点是否在同一集合”。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集（不带路径压缩的写法更直观，实际已加入路径压缩）"""
    def __init__(self, n: int):
        self.parent = list(range(n + 1))   # parent[i] = i 表示每个节点自成一族

    def find(self, x: int) -> int:
        # 路径压缩：让查找更快
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra   # 随便把一个根指向另一个根即可

def minScore(n: int, roads: List[List[int]]) -> int:
    """
    返回从城市 1 到城市 n 的路径的最小可能分数。
    思路：找出与 1 连通的所有节点所在的连通分量，
          然后在该分量的所有边中取最小的 distance。
    """
    uf = UnionFind(n)

    # 1️⃣ 合并所有相连的城市
    for u, v, _ in roads:
        uf.union(u, v)

    # 2️⃣ 找到 1 所在连通分量的根
    root_of_one = uf.find(1)

    # 3️⃣ 在属于同一连通分量的边中找最小距离
    min_dist = float('inf')
    for u, v, w in roads:
        # 若两端点都在 1 的连通分量里，则这条边可以出现在某条 1->n 路径中
        if uf.find(u) == root_of_one and uf.find(v) == root_of_one:
            min_dist = min(min_dist, w)

    return min_dist
```

**代码要点解释（中文注释已写在关键行）**：

- `UnionFind` 用来快速判断两个城市是否在同一连通分量。  
- 第一次遍历 `roads` 把所有相连的城市合并到同一个集合。  
- `root_of_one = uf.find(1)` 得到城市 `1` 所在集合的根标识。  
- 再遍历一次 `roads`，只要边的两端点的根都等于 `root_of_one`，说明这条边属于「1 能到达的区域」。我们把这条边的距离 `w` 与当前最小值比较，保留最小者。  
- 题目保证 **至少存在一条从 1 到 n 的路径**，所以最终的 `min_dist` 一定会被更新。

#### 复杂度

- **时间复杂度**：`O(E·α(N))`，其中 `E = len(roads)`，`α` 是 Ackermann 函数的反函数，几乎可以看作常数。因此整体是 **线性** 的 `O(E)`。  
  - 与暴力解相比，省掉了指数级的路径枚举，只需要两次遍历边列表。  
- **空间复杂度**：`O(N)` 用于并查集的 `parent` 数组，外加存放 `roads` 本身的空间（题目已提供）。不需要额外的递归栈或队列。

---

## 心得

- **核心技巧**：**利用连通分量的性质，将「路径最小边」转化为「连通分量内部的全局最小边」**。  
- **适用场景**：  
  1. **最小/最大路径分数**（如本题）  
  2. **在同一连通块内找最小/最大权值的边**（如 “Minimum Edge in Path” 类似问题）  
  3. **判断两点是否可达并统计该连通块的某种全局属性**（如 “Maximum Minimum Path” 等）  
- **一句话总结**：只要 1 与 n 在同一连通块，答案就是该块里最小的道路长度。

---

## 反思

- **第一反应**：直接想到 DFS/BFS 枚举路径，想把每条路径的最小边取出来。  
- **最容易踩的坑**：  
  - **误以为要遍历所有路径**，导致时间爆炸。  
  - **忘记处理不连通的城市**：如果直接在所有边上取最小值，可能会把与 1、n 完全无关的孤立边算进去。  
  - **边界条件**：题目保证 1 与 n 至少有一条路径，但如果忘记这点，可能会在找不到连通块时返回 `inf`。  
- **下次遇到同类题**，第一步应该：  
  1. **判断 1 与 n 是否在同一连通块**（DFS/并查集）。  
  2. **在该块内部统计全局最小（或最大）边权**，而不是枚举路径。