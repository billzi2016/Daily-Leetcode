# #3243. **道路新增查询后的最短距离 I** / Shortest Distance After Road Addition Queries I

> 难度：中等 · 标签：Array、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/)

---

## 题目（英文原版）

**Description**

You are given an integer n and a 2D integer array queries.
There are n cities numbered from 0 to n - 1. Initially, there is a unidirectional road from city i to city i + 1 for all 0 <= i < n - 1.
queries[i] = [ui, vi] represents the addition of a new unidirectional road from city ui to city vi. After each query, you need to find the length of the shortest path from city 0 to city n - 1.
Return an array answer where for each i in the range [0, queries.length - 1], answer[i] is the length of the shortest path from city 0 to city n - 1 after processing the first i + 1 queries.

**Examples**

**Example 1:**

```
Input: n = 5, queries = [[2,4],[0,2],[0,4]]
Output: [3,2,1]
Explanation:

After the addition of the road from 2 to 4, the length of the shortest path from 0 to 4 is 3.

After the addition of the road from 0 to 2, the length of the shortest path from 0 to 4 is 2.

After the addition of the road from 0 to 4, the length of the shortest path from 0 to 4 is 1.
```

**Example 2:**

```
Input: n = 4, queries = [[0,3],[0,2]]
Output: [1,1]
Explanation:

After the addition of the road from 0 to 3, the length of the shortest path from 0 to 3 is 1.

After the addition of the road from 0 to 2, the length of the shortest path remains 1.
```

**Constraints**

- 3 <= n <= 500
- 1 <= queries.length <= 500
- queries[i].length == 2
- 0 <= queries[i][0] < queries[i][1] < n
- 1 < queries[i][1] - queries[i][0]
- There are no repeated roads among the queries.

---

## 题目（中文翻译）

你得到一个整数 `n` 和一个二维整数数组 `queries`。  
城市编号为 `0` 到 `n - 1`。最初，所有满足 `0 <= i < n - 1` 的相邻城市之间都有一条单向道路（unidirectional road），从城市 `i` 指向城市 `i + 1`。  

`queries[i] = [ui, vi]` 表示在城市 `ui` 与城市 `vi` 之间新增一条单向道路（unidirectional road），方向从 `ui` 指向 `vi`。在处理完每条查询后，你需要求出从城市 `0` 到城市 `n - 1` 的最短路径长度。  

返回一个数组 `answer`，其中 `answer[i]` 为处理前 `i + 1` 条查询后，从城市 `0` 到城市 `n - 1` 的最短路径长度。

**示例 1**  
**输入**: `n = 5, queries = [[2,4],[0,2],[0,4]]`  
**输出**: `[3,2,1]`  
**解释**:

- 在新增从 `2` 到 `4` 的道路后，`0 → 1 → 2 → 4` 是最短路径，长度为 `3`。  
- 再新增从 `0` 到 `2` 的道路后，`0 → 2 → 4` 成为最短路径，长度为 `2`。  
- 再新增从 `0` 到 `4` 的道路后，直接走 `0 → 4`，长度为 `1`。

**示例 2**  
**输入**: `n = 4, queries = [[0,3],[0,2]]`  
**输出**: `[1,1]`  
**解释**:

- 在新增从 `0` 到 `3` 的道路后，`0 → 3` 是最短路径，长度为 `1`。  
- 再新增从 `0` 到 `2` 的道路后，最短路径仍为 `0 → 3`，长度保持为 `1`。

**约束条件**

- `3 <= n <= 500`
- `1 <= queries.length <= 500`
- `queries[i].length == 2`
- `0 <= queries[i][0] < queries[i][1] < n`
- `1 < queries[i][1] - queries[i][0]`
- 查询中不会出现重复的道路。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的图很特殊：

* 城市编号从 `0` 到 `n‑1`，**所有道路都是单向且只能从左往右**（`u < v`）。
* 初始时只有 `i → i+1` 这条相邻道路，后面每次查询会再加入一条 `u → v`（同样满足 `u < v`）。

最直接的想法就是 **每次查询后把所有已有的道路都收集起来，跑一次最短路算法**，得到从 `0` 到 `n‑1` 的最短距离，再把答案存进结果数组。

这里可以使用 **BFS**（广度优先搜索）：

* 因为所有道路的权重都是 `1`，BFS 按层次遍历天然就会得到最短路径长度。
* BFS 需要一个“队列”，相当于我们在现实生活中排队买东西，先进去的先出队，层层推进。

> **类比**：把城市想成书的章节，章节之间有顺序的跳转（相邻章节）以及偶尔出现的跨章节跳转。要找最快的读完方式，就像在图里一步一步“走”过去，先走到的章节自然是最少步数。

**为什么正确**  
BFS 在 **无权图**（所有边权相同）中能够保证第一次到达目标节点的路径就是最短的，因为它一次只扩展一步，层层递进，不会跳过更短的可能。

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortest_after_each_query(n: int, queries: List[List[int]]) -> List[int]:
    # 记录所有已经出现的道路，邻接表的形式
    # adjacency[u] = [v1, v2, ...] 表示从 u 可以直接到达哪些城市
    adjacency = [[] for _ in range(n)]
    # 初始化相邻道路 i -> i+1
    for i in range(n - 1):
        adjacency[i].append(i + 1)

    ans = []

    for u, v in queries:                     # 逐个处理查询
        adjacency[u].append(v)               # 加入新道路

        # ---------- BFS 求最短距离 ----------
        dist = [-1] * n                       # -1 表示「未访问」
        q = deque([0])
        dist[0] = 0

        while q:
            cur = q.popleft()
            if cur == n - 1:                 # 已经到达终点，提前结束
                break
            for nxt in adjacency[cur]:       # 遍历所有可达的下一个城市
                if dist[nxt] == -1:          # 只访问一次，防止死循环
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)

        ans.append(dist[n - 1])               # 记录 0 → n-1 的最短步数
        # -------------------------------------

    return ans
```

> **关键行注释**  
> - `adjacency = [[] for _ in range(n)]`：相当于为每座城市准备一本“出发目录”，里面写着可以直接去的城市。  
> - `dist = [-1] * n`：把每座城市的距离初始化为“未知”。  
> - `if dist[nxt] == -1:`：只在第一次遇到城市时才记录距离，避免重复访问（就像只买一次同一种商品）。

#### 复杂度

- **时间复杂度**：`O(Q * (n + E))`  
  - `Q` 为查询数（≤500），`n` 为城市数（≤500），`E` 为当前图的边数。  
  - 在最坏情况下，每次 BFS 要遍历所有城市和所有道路，约等于 `O(n²)`。  
  - **大白话**：每次查询我们都重新走一遍“全城”，所以如果查询很多，时间会像乘法一样叠加。

- **空间复杂度**：`O(n + E)`  
  - 用邻接表存图需要 `n` 个列表，加上所有道路的总数 `E`。  
  - BFS 队列和距离数组各占 `O(n)` 的空间。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次查询都重新跑一次 BFS**，实际上我们并不需要每次都从头搜索。  
观察图的结构可以发现：

1. **所有道路都是向右的**（`u < v`），因此图本身是一个 **有向无环图（DAG）**。  
2. 在 DAG 中，**从起点到任意节点的最短路径只和它左侧（编号更小）的节点有关**，可以用一次 **动态规划（DP）** 按编号顺序一次算完。

我们可以维护一个数组  

```
dist[i] = 当前所有已知道路下，0 → i 的最短步数
```

初始时只有相邻道路，显然 `dist[i] = i`（一步一步走过去）。

当加入一条新道路 `u → v` 时，只会 **让 v 以及 v 右边的城市的最短距离可能变小**，因为：

* 通过这条新路到达 `v` 的距离是 `dist[u] + 1`。  
* 如果 `dist[u] + 1` 小于原来的 `dist[v]`，我们就更新 `dist[v]`。  
* 更新了 `dist[v]` 以后，`v` 的右侧城市 `v+1, v+2 …` 也要检查是否可以受益——因为它们的最短距离可以是 “左边相邻城市的距离 + 1”。这一步类似于 **从左到右一次扫描，像流水线一样把改动向后传递**。

所以每次新增道路的处理只需要：

```
if dist[u] + 1 < dist[v]:
    dist[v] = dist[u] + 1
    for i from v+1 to n-1:
        # 只要左边的相邻城市可以让当前城市更近，就更新
        if dist[i-1] + 1 < dist[i]:
            dist[i] = dist[i-1] + 1
        else:
            break   # 后面的城市已经没有改进的空间，提前结束
```

这段循环最多遍历一次 `v … n-1`，**总时间仍是 O(n) 每条查询**，但没有 BFS 那种“遍历所有边”的开销，常数更小。

> **类比**：把城市想成一排排的邮筒，`dist[i]` 记录把信从左边邮筒送到第 `i` 个邮筒最少要跳几次。加了一根新的快递线 `u → v`，只要看这根线是否让 `v` 更近了，然后把“快递速度提升”的好处顺着右边的邮筒继续传递下去。

#### 代码（Python）

```python
from typing import List

def shortest_after_each_query_opt(n: int, queries: List[List[int]]) -> List[int]:
    # 初始距离：只能一步一步走，0→i 的距离就是 i
    dist = list(range(n))

    ans = []

    for u, v in queries:
        # 新增一条 u → v 的道路
        # 如果通过这条道路可以让 v 更近，就更新
        if dist[u] + 1 < dist[v]:
            dist[v] = dist[u] + 1

            # 把改进向右传播
            for i in range(v + 1, n):
                # 左边相邻城市的最短距离 + 1
                if dist[i - 1] + 1 < dist[i]:
                    dist[i] = dist[i - 1] + 1
                else:
                    # 已经不能再改进，后面的城市也不会受影响
                    break

        # 0 → n-1 的最短距离即为答案
        ans.append(dist[-1])

    return ans
```

> **关键行解释**  
> - `dist = list(range(n))`：相当于默认每个城市只能一步一步走过去。  
> - `if dist[u] + 1 < dist[v]:`：判断新路是否真的“省步”。  
> - `for i in range(v + 1, n):`：把省步的好消息往右边“广播”。  
> - `break`：一旦右侧城市已经不需要再更新，就可以提前结束，省时间。

#### 复杂度

- **时间复杂度**：`O(Q * n)`  
  - 每条查询最多遍历一次从 `v` 到 `n‑1` 的区间，最坏是 `O(n)`。  
  - 与暴力解的 `O(Q * (n+E))` 相比，省去了遍历所有边的开销，实际运行更快。  
  - **大白话**：我们只在“受影响的那段”里搬砖，而不是全城动员。

- **空间复杂度**：`O(n)`  
  - 只需要保存 `dist` 一个长度为 `n` 的数组，外加答案列表。  
  - 不再需要额外的邻接表或 BFS 队列。

---

## 心得

- **核心技巧**：利用 **有向无环图的单调性**，用 **动态规划 + 增量更新** 维护从源点到所有点的最短距离。  
- **适用的题型**  
  1. **单向链路或只向右/左的 DAG**（如“最短路径后续查询”“最长递增子序列动态维护”）。  
  2. **每次只加入边且不会删除**，且 **边的方向固定**（如“道路建设”“任务依赖增量”）。  
  3. **权重相同的图**，可以把 BFS 换成 DP 直接在拓扑序上扫描。  
- **一句话总结**：  
  > “在只能向右的图里，最短距离只会往右传递，新增一条路只要把‘省步’的影响向后扩散即可。”

---

## 反思

- **第一反应**：看到“每次查询后求最短路”，本能想到 **BFS/Dijkstra**，于是写了暴力版。  
- **最容易踩的坑**  
  * **忘记图是单向且无环**：如果误以为是一般有向图，会去写 Dijkstra，复杂度不必要地高。  
  * **更新传播不完整**：仅更新 `dist[v]` 而不向右继续，会导致后面的城市仍使用旧的、非最优距离。  
  * **边界条件**：`u` 或 `v` 可能是 `0`、`n-1`，要确保循环不会越界。  
- **下次类似题的第一步**：  
  > “先检查图的结构（是否是 DAG、是否只有单向递增的边），如果是，就尝试用拓扑序的 DP 维护答案，而不是每次都跑完整的最短路算法。”