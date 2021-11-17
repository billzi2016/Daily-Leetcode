# #1557. 最少顶点数以到达所有节点 / Minimum Number of Vertices to Reach All Nodes

> 难度：中等 · 标签：Graph · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/)

---

## 题目（英文原版）

**Description**

Given a directed acyclic graph, with n vertices numbered from 0 to n-1, and an array edges where edges[i] = [fromi, toi] represents a directed edge from node fromi to node toi.
Find the smallest set of vertices from which all nodes in the graph are reachable. It's guaranteed that a unique solution exists.
Notice that you can return the vertices in any order.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
Output: [0,3]
Explanation: It's not possible to reach all the nodes from a single vertex. From 0 we can reach [0,1,2,5]. From 3 we can reach [3,4,2,5]. So we output [0,3].
```

**Example 2:**

```
Input: n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
Output: [0,2,3]
Explanation: Notice that vertices 0, 3 and 2 are not reachable from any other node, so we must include them. Also any of these vertices can reach nodes 1 and 4.
```

**Constraints**

- 2 <= n <= 10^5
- 1 <= edges.length <= min(10^5, n * (n - 1) / 2)
- edges[i].length == 2
- 0 <= fromi, toi < n
- All pairs (fromi, toi) are distinct.

---

## 题目（中文翻译）

**题目描述**  
给定一个有向无环图（directed acyclic graph，DAG），图中有 `n` 个顶点，编号为 `0` 到 `n-1`，以及一个数组 `edges`，其中 `edges[i] = [from_i, to_i]` 表示一条从顶点 `from_i` 指向顶点 `to_i` 的有向边（directed edge）。  
请找出最小的顶点集合，使得从该集合中的每个顶点出发，都能到达（reach）图中的所有节点。题目保证唯一解。  
返回的顶点集合顺序任意。

**示例 1**  

**示例 2**  

**约束条件**  

- `2 <= n <= 10^5`  
- `1 <= edges.length <= min(10^5, n * (n - 1) / 2)`  
- `edges[i].length == 2`  
- `0 <= from_i, to_i < n`  
- 所有 `(from_i, to_i)` 对均不相同。

**示例**  

*示例 1*  
```
Input: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
Output: [0,3]
Explanation: 仅凭单个顶点无法到达所有节点。  
从顶点 0 可以到达 [0,1,2,5]；  
从顶点 3 可以到达 [3,4,2,5]。  
因此返回 [0,3]。
```

*示例 2*  
```
Input: n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
Output: [0,2,3]
Explanation: 注意到顶点 0、2、3 没有任何其他节点能够到达它们，所以必须将它们全部包含在答案中。  
此外，这些顶点中的任意一个都可以到达节点 1 和 4。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的起始集合都枚举一遍**，然后检查每个集合能否把图里的所有节点都遍历到，最后挑出最小的那个。  
具体步骤如下：

1. **枚举子集**  
   - 把 `0 … n-1` 这 `n` 个节点看成一个集合，所有子集的数量是 `2ⁿ`（比如 3 个节点就有 `000,001,010,011,100,101,110,111` 这 8 种组合）。  
   - 对每一种组合（即一种可能的起始集合），我们把它当成起点，一起做一次**多源 BFS/DFS**，看能否遍历到图中每一个节点。

2. **检查是否覆盖所有节点**  
   - 从子集里的所有起点出发，使用 BFS（或 DFS）把能够到达的节点全部标记。  
   - 最后把标记数组和 `0 … n-1` 对比，只要有任意一个节点没有被标记，就说明这个子集不行。

3. **记录最小的可行子集**  
   - 在所有可行的子集中，挑选节点数最少的那一个（如果有多个，随便返回一个）。

> **生活化类比**：想象你有一把钥匙，每把钥匙只能打开特定的门。暴力解相当于把所有钥匙的组合都尝试一次，看看哪一组合能打开所有的门。显然，钥匙越多，组合数就会指数级增长，效率极低。

> **为什么正确**：因为我们枚举了**所有**可能的起始集合，必然会包含最优解；只要检查过程没有错误，就一定能找到最小的可行集合。

#### 代码（Python）

```python
from itertools import combinations
from collections import deque
from typing import List

def brute_minimum_vertices(n: int, edges: List[List[int]]) -> List[int]:
    # 建立邻接表，方便遍历
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    # 所有节点的集合，用于快速比较是否全部被访问到
    all_nodes = set(range(n))

    # 从子集大小 1 开始枚举，直到找到第一个可行解
    for size in range(1, n + 1):
        # 组合函数会返回所有 size 长度的子集
        for subset in combinations(range(n), size):
            # 多源 BFS
            visited = set()
            dq = deque(subset)          # 把子集里的每个节点都放进队列作为起点
            visited.update(subset)

            while dq:
                cur = dq.popleft()
                for nxt in graph[cur]:
                    if nxt not in visited:
                        visited.add(nxt)
                        dq.append(nxt)

            # 检查是否已经遍历到所有节点
            if visited == all_nodes:
                return list(subset)     # 第一个找到的即是最小的

    # 根据题目保证一定有解，这行理论上不会被执行
    return []
```

> 关键行中文注释已经写在代码里，直接复制跑即可。

#### 复杂度

- **时间复杂度**：`O(2^n * (n + m))`  
  - `2^n` 来自子集的枚举（指数级），每次枚举都要做一次 BFS，遍历所有节点和边，复杂度是 `O(n + m)`（`m` 为边数）。  
  - 用大白话说，就是“节点越多，时间会翻几倍”，在 `n = 30` 以后几乎不可能跑完。

- **空间复杂度**：`O(n + m)`  
  - 需要存图的邻接表 `O(n + m)`，以及 BFS 用的队列和访问集合 `O(n)`。

> 暴力解虽然思路最直观，但在实际面试或线上评测里根本用不了，只能当作“理论上最完整的搜索”来帮助我们发现真正的瓶颈。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有子集是最大的性能瓶颈**。我们需要找一种 **一次遍历** 就能直接判断哪些节点必须被选入答案。观察题目可以得到以下关键结论：

1. **入度为 0 的节点只能自己到达**  
   - “入度”指的是有多少条边指向该节点。若一个节点没有任何入边（入度 = 0），就没有别的节点可以先到达它。唯一的办法是**把它本身放进起始集合**。  
   - 类比：把每个节点想成一本书，入度是指向这本书的引用次数。如果没有任何引用，只有自己（作者）才能拿到它。

2. **入度不为 0 的节点一定可以被其它节点覆盖**  
   - 若节点 `v` 至少有一条入边 `u → v`，只要我们把 `u` 放进答案集合，`v` 就能被 `u` 通过这条边到达。  
   - 这并不意味着我们必须把所有入边的起点都选进来，只要 **每个有入边的节点** 至少有 **一个** 起点被选，就能覆盖它。

3. **唯一最小解就是所有入度为 0 的节点集合**  
   - 把所有入度为 0 的节点全部加入答案，显然可以覆盖整个图（因为每条有向边的终点都有入边，它们都能被前面的某个入度为 0 的节点递归到）。  
   - 设想如果我们把某个入度为 0 的节点 **去掉**，它就再也没有任何来源可以到达，只会导致答案不完整。因此 **必须** 把它们全部保留下来。  
   - 另一方面，任何入度不为 0 的节点 **可以不选**，因为它们已经有来源可以到达。于是，这个集合是 **唯一最小** 的。

> **核心数据结构**：**入度数组**（大小为 `n` 的整数列表）。我们只需要一次遍历所有边，就能统计每个节点的入度。

#### 代码（Python）

```python
from typing import List

def minimum_vertices_to_reach_all_nodes(n: int, edges: List[List[int]]) -> List[int]:
    """
    返回所有入度为 0 的节点，即最小的起始集合。
    """
    # 1. 初始化入度数组，全部设为 0
    indegree = [0] * n

    # 2. 遍历每条有向边，统计终点的入度
    for u, v in edges:
        indegree[v] += 1          # v 收到一条来自 u 的入边

    # 3. 入度为 0 的节点必然是答案
    answer = [i for i in range(n) if indegree[i] == 0]

    return answer
```

> 关键行中文注释已经写在代码里，直接复制跑即可。

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - 只遍历了一遍节点（`n`）和边（`m`），每一步都是常数时间操作。  
  - 与暴力解相比，**从指数级降到了线性级**，即“节点增多，时间只会按比例增长”，在 `10⁵` 规模的数据下也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 只用了一个大小为 `n` 的入度数组来记录每个节点的入度，另外还有返回答案的列表（最坏情况下也只会存 `n` 个元素）。  
  - 与暴力解的 `O(n + m)` 相比，省去了邻接表和 BFS 队列的额外开销。

> 与暴力解对比：  
> - 暴力解需要 **枚举子集**（指数级）+ **多源 BFS**（线性），时间上几乎不可能接受。  
> - 最优解只要 **一次遍历**，即可得到唯一最小解，实用性极高。

---

## 心得

- **核心技巧**：**入度统计**（统计每个节点有多少条进入的边）。  
- **适用题型**：  
  1. “找出所有 **源节点**（没有入边的节点）”——例如 LeetCode 1462 *Course Schedule IV* 中的前置课程分析。  
  2. “最小的起始集合覆盖所有节点”——例如 1557 *Minimum Number of Vertices to Reach All Nodes*（本题）。  
  3. “判断是否存在唯一的拓扑序列”——入度为 0 的节点数目在每一步的唯一性决定了拓扑序是否唯一。

- **一句话总结解题钥匙**：**“入度为 0 的节点必须自己出发，其他节点都可以被它们‘接管’”。**

---

## 反思

- **第一反应**：看到“有向无环图（DAG）”和“最小覆盖集合”，我第一时间想到 **集合覆盖**（NP 难），于是构造了暴力的子集枚举方案。  
- **最容易踩的坑**：  
  - **忘记统计所有节点的入度**：如果只遍历了出现的终点，可能会遗漏完全没有出边也没有入边的孤立节点。  
  - **误以为入度为 0 的节点一定是唯一解**，但需要证明它们**必须**在答案中，否则会出现不可达的节点。  
  - **边界条件**：`n = 2`、`edges = []`（虽然题目保证至少有一条边，但实际写代码时要防止空列表导致错误）。  

- **下次遇到同类题的第一步**：**先统计每个节点的入度**，把所有入度为 0 的节点直接列出来——这往往就是答案的雏形。随后再思考是否需要进一步处理（比如在有环图中要考虑强连通分量），但在 DAG 场景下，入度为 0 已经足够。