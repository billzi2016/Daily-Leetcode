# #1462. 课程表 IV / Course Schedule IV

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/course-schedule-iv/)

---

## 题目（英文原版）

**Description**

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course ai first if you want to take course bi.
Prerequisites can also be indirect. If course a is a prerequisite of course b, and course b is a prerequisite of course c, then course a is a prerequisite of course c.
You are also given an array queries where queries[j] = [uj, vj]. For the jth query, you should answer whether course uj is a prerequisite of course vj or not.
Return a boolean array answer, where answer[j] is the answer to the jth query.

**Examples**

**Example 1:**

```
Input: numCourses = 2, prerequisites = [[1,0]], queries = [[0,1],[1,0]]
Output: [false,true]
Explanation: The pair [1, 0] indicates that you have to take course 1 before you can take course 0.
Course 0 is not a prerequisite of course 1, but the opposite is true.
```

**Example 2:**

```
Input: numCourses = 2, prerequisites = [], queries = [[1,0],[0,1]]
Output: [false,false]
Explanation: There are no prerequisites, and each course is independent.
```

**Example 3:**

```
Input: numCourses = 3, prerequisites = [[1,2],[1,0],[2,0]], queries = [[1,0],[1,2]]
Output: [true,true]
```

**Constraints**

- 2 <= numCourses <= 100
- 0 <= prerequisites.length <= (numCourses * (numCourses - 1) / 2)
- prerequisites[i].length == 2
- 0 <= ai, bi <= numCourses - 1
- ai != bi
- All the pairs [ai, bi] are unique.
- The prerequisites graph has no cycles.
- 1 <= queries.length <= 104
- 0 <= ui, vi <= numCourses - 1
- ui != vi

---

## 题目（中文翻译）

有 `numCourses` 门课程需要学习，编号为 `0` 到 `numCourses - 1`。给定一个数组 `prerequisites`，其中 `prerequisites[i] = [a_i, b_i]` 表示如果想选修课程 `b_i`，必须先修完课程 `a_i`（先决条件，prerequisite）。  
先决条件也可以是间接的（indirect）：如果课程 `a` 是课程 `b` 的先决条件，且课程 `b` 是课程 `c` 的先决条件，则课程 `a` 也是课程 `c` 的先决条件。

同时给定一个数组 `queries`，其中 `queries[j] = [u_j, v_j]`。对于第 `j` 条查询，需要判断课程 `u_j` 是否是课程 `v_j` 的先决条件。  
返回一个布尔数组 `answer`，其中 `answer[j]` 为第 `j` 条查询的答案。

## 示例

### 示例 1
**输入**: `numCourses = 2`, `prerequisites = [[1,0]]`, `queries = [[0,1],[1,0]]`  
**输出**: `[false,true]`  
**解释**: `[1, 0]` 表示必须先修完课程 1 才能修课程 0。  
课程 0 不是课程 1 的先决条件，但相反的关系成立。

### 示例 2
**输入**: `numCourses = 2`, `prerequisites = []`, `queries = [[1,0],[0,1]]`  
**输出**: `[false,false]`  
**解释**: 没有任何先决条件，每门课程相互独立。

### 示例 3
**输入**: `numCourses = 3`, `prerequisites = [[1,2],[1,0],[2,0]]`, `queries = [[1,0],[1,2]]`  
**输出**: `[true,true]`

## 约束条件
- `2 <= numCourses <= 100`
- `0 <= prerequisites.length <= (numCourses * (numCourses - 1) / 2)`
- `prerequisites[i].length == 2`
- `0 <= a_i, b_i <= numCourses - 1`
- `a_i != b_i`
- 所有 `[a_i, b_i]` 均唯一
- 先决条件图不存在环
- `1 <= queries.length <= 10^4`
- `0 <= u_i, v_i <= numCourses - 1`
- `u_i != v_i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每门课程看成 **图中的节点**，`prerequisites[i] = [a, b]` 表示有一条有向边 `a → b`（必须先修 `a` 才能修 `b`）。  
要判断 “课程 `u` 是否是课程 `v` 的先修课”，其实就是在这张有向无环图里 **判断 `u` 能否走到 `v`**。

最直接的想法是：

1. 对每一个查询 `[u, v]`，从节点 `u` 开始 **深度优先搜索（DFS）或广度优先搜索（BFS）**。  
2. 只要在搜索过程中碰到 `v`，就说明 `u` 是 `v` 的先修课；搜索完都没碰到则说明不是。

> **类比**：把课程图想象成城市地图，`u` → `v` 的路径是否存在就像问“从城市 `u` 能不能坐公交到达城市 `v`”。我们每次都从 `u` 出发，沿着公交线路一步步走，看看能否到达 `v`。

**为什么正确**：DFS/BFS 会遍历 **所有** 从 `u` 能到达的节点，只要 `v` 在其中，就一定存在一条（直接或间接）先修关系。

**复杂度分析**  
- 对每个查询我们都要一次完整的搜索。设课程数为 `n`，先修关系（边）数为 `e`，查询数为 `q`。  
- 单次 BFS/DFS 的时间是 `O(n + e)`（遍历所有相邻节点），最坏情况下会遍历整张图。  
- 所以总时间复杂度是 `O(q·(n + e))`。在本题的约束下（`n ≤ 100`，`q ≤ 10⁴`），这会是 **上万次遍历**，在 Python 中会比较慢。  

空间上，只需要一个 `visited` 数组记录搜索时是否已经访问过，大小为 `O(n)`。

#### 代码（Python）

```python
from collections import deque
from typing import List

def checkIfPrerequisite(numCourses: int,
                        prerequisites: List[List[int]],
                        queries: List[List[int]]) -> List[bool]:
    # 1. 建图：邻接表，edges[a] 保存所有直接后继课程 b
    edges = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        edges[a].append(b)

    def bfs(start: int, target: int) -> bool:
        """从 start 出发，广度优先搜索，看能否到达 target"""
        visited = [False] * numCourses
        dq = deque([start])
        visited[start] = True
        while dq:
            cur = dq.popleft()
            if cur == target:          # 找到目标，说明是先修课
                return True
            for nxt in edges[cur]:     # 遍历所有直接相连的后继
                if not visited[nxt]:
                    visited[nxt] = True
                    dq.append(nxt)
        return False                   # 搜索结束也没见到 target

    # 2. 对每个查询单独跑一次 BFS
    ans = []
    for u, v in queries:
        ans.append(bfs(u, v))
    return ans
```

#### 复杂度

- **时间复杂度**：`O(q·(n + e))`  
  - `q` 是查询数，`n` 是课程数，`e` 是先修关系数。  
  - 大白话：每个问题都要“走遍一次全图”，所以问题越多，时间越长。
- **空间复杂度**：`O(n)`  
  - 只用了一个 `visited` 数组和 BFS 队列，大小随课程数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **对每个查询都要重新搜索**，导致大量重复工作。  
实际上，课程数 `n` 最多只有 100，**所有查询** 都是基于同一张有向无环图。我们可以先把 **图中所有可达关系** 预先算好，后面每个查询只要 O(1) 时间查表即可。

两种常见的预处理方式：

1. **Floyd‑Warshall**：经典的「所有点对最短路」算法，也可以用来求「可达性」矩阵。时间 `O(n³)`，空间 `O(n²)`。
2. **对每个节点 BFS/DFS + 记忆化**：从每个课程 `i` 出发一次 BFS，得到 `i` 能到达的所有课程，填入 `reach[i][j]`。时间 `O(n·(n+e))`，空间同样 `O(n²)`。

因为 `n ≤ 100`，`n³ = 10⁶`，这在 Python 中完全可以接受，而且实现最简洁。下面就用 **Floyd‑Warshall** 来说明。

**核心概念——可达矩阵 `reach`**  
- `reach[i][j] = True` 表示课程 `i` 是课程 `j` 的先修课（可能是直接也可能是间接）。  
- 初始时，只把直接先修关系标记为 `True`。  
- Floyd‑Warshall 的核心思想是：「如果 `i` 能到 `k`，且 `k` 能到 `j`，那么 `i` 也能到 `j`。」这正好对应「先修」的传递性。

**类比**：把 `reach` 想成一本「课程先修手册」，手册里每一行 `i` 列出所有可以通过若干层次（直接或间接）到达的课程。我们先填上直接的几页，然后用「如果第 k 页说 i 能到 k，且第 k 页说 k 能到 j，那第 i 页也应该写上 j」的规则，逐页完善手册。

#### 代码（Python）

```python
from typing import List

def checkIfPrerequisite(numCourses: int,
                        prerequisites: List[List[int]],
                        queries: List[List[int]]) -> List[bool]:
    # 1. 初始化可达矩阵：n x n 的布尔二维数组，默认全 False
    n = numCourses
    reach = [[False] * n for _ in range(n)]

    # 2. 把直接先修关系填进去
    for a, b in prerequisites:
        reach[a][b] = True          # a 是 b 的直接先修课

    # 3. Floyd‑Warshall：三层循环，更新传递可达性
    #    对每一个中间节点 k，尝试用它把 i -> j 的关系“桥接”起来
    for k in range(n):
        for i in range(n):
            if reach[i][k]:         # 先判断 i 能否到 k，省去不必要的内层循环
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True   # i 能通过 k 到达 j

    # 4. 直接回答查询：只要查表 O(1)
    ans = []
    for u, v in queries:
        ans.append(reach[u][v])
    return ans
```

> **代码注释说明**  
> - 第 2 步把「直接先修」写进手册。  
> - 第 3 步的 `if reach[i][k]` 是一个小技巧，避免在 `i` 到 `k` 不通时仍然遍历所有 `j`，可以把常数降下来。  
> - 第 4 步直接读取 `reach[u][v]`，答案立刻得到。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 三层循环每层最多跑 `n`（这里 `n ≤ 100`），总共约 `1,000,000` 次基本操作。  
  - 与暴力解相比，**不再随查询数 `q` 增长**，即使 `q = 10⁴` 也只需要常数时间查询，快得多。

- **空间复杂度**：`O(n²)`  
  - `reach` 矩阵占 `n × n` 的布尔值，最多 10,000 个 `True/False`，在内存里只占几百 KB。

---

## 心得

- **核心技巧**：**利用图的传递闭包（可达矩阵）一次性算出所有先修关系**，查询时直接查表。  
- **适用场景**：  
  1. “判断两点是否有路径”类的查询（如 LeetCode 1971 *Find if Path Exists in Graph*）。  
  2. “传递闭包”或“先后顺序”判断（如 1462 *Course Schedule IV* 本题）。  
  3. 任意需要大量 **点对可达性** 查询的场景（如网络连通性、权限继承等）。
- **一句话总结**：先把所有“先修”关系一次性算好，查询时只要 O(1) 查表——把“跑图”搬进预处理阶段。

---

## 反思

- **第一反应**：看到“先修”这个关键词，立刻想到 **图的遍历**（DFS/BFS），于是想到对每个查询单独搜索。  
- **最容易踩的坑**：  
  - 忽视 **图是有向无环** 的特性，导致写成了普通的 BFS 而没有考虑**传递性**的高效利用。  
  - 在暴力解中忘记对 `visited` 进行重置，导致不同查询相互影响。  
  - 在 Floyd‑Warshall 实现时，如果直接写 `reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])`，容易出现 **逻辑错误**（尤其是顺序错误），最好先检查 `reach[i][k]` 再循环 `j`。
- **下次遇到同类题**：第一步就思考 **是否可以把所有可能的答案一次性预处理**（如可达矩阵、前缀和、DP 表），而不是对每个询问重复计算。这样往往能把复杂度从 “查询数 × 图遍历” 降到 “图一次遍历 + 常数查询”。