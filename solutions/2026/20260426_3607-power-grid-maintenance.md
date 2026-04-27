# #3607. 电网维护 / Power Grid Maintenance

> 难度：中等 · 标签：Array、Hash Table、Depth-First Search、Breadth-First Search、Union Find、Graph、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/power-grid-maintenance/)

---

## 题目（英文原版）

**Description**

You are given an integer c representing c power stations, each with a unique identifier id from 1 to c (1‑based indexing).
These stations are interconnected via n bidirectional cables, represented by a 2D array connections, where each element connections[i] = [ui, vi] indicates a connection between station ui and station vi. Stations that are directly or indirectly connected form a power grid.
Initially, all stations are online (operational).
You are also given a 2D array queries, where each query is one of the following two types:
Return an array of integers representing the results of each query of type [1, x] in the order they appear.
Note: The power grid preserves its structure; an offline (non‑operational) node remains part of its grid and taking it offline does not alter connectivity.

**Examples**

**Example 1:**

```
Input: c = 5, connections = [[1,2],[2,3],[3,4],[4,5]], queries = [[1,3],[2,1],[1,1],[2,2],[1,2]]
Output: [3,2,3]
Explanation:
```

**Example 2:**

```
Input: c = 3, connections = [], queries = [[1,1],[2,1],[1,1]]
Output: [1,-1]
Explanation:
```

**Constraints**

- 1 <= c <= 105
- 0 <= n == connections.length <= min(105, c * (c - 1) / 2)
- connections[i].length == 2
- 1 <= ui, vi <= c
- ui != vi
- 1 <= queries.length <= 2 * 105
- queries[i].length == 2
- queries[i][0] is either 1 or 2.
- 1 <= queries[i][1] <= c

---

## 题目（中文翻译）

你得到一个整数 `c`，表示有 `c` 座电站，每座电站都有唯一的标识符 `id`，范围为 `1` 到 `c`（**1‑based indexing**）。  
这些电站通过 `n` 条双向电缆（bidirectional cable）相连，`connections` 为一个二维数组，其中 `connections[i] = [ui, vi]` 表示电站 `ui` 与电站 `vi` 之间有一条连接。直接或间接相连的电站构成一个电网（power grid）。  
初始时，所有电站均在线（operational）。  

另给定一个二维数组 `queries`，每个查询为以下两种类型之一：

* `[1, x]`：返回 `x` 所在电网中当前在线的电站数量。如果 `x` 已离线，则返回 `-1`。  
* `[2, x]`：将电站 `x` 标记为离线（non‑operational）。**注意**：电网的结构保持不变；离线的节点仍然是其所在电网的一部分，离线不会改变连通性。  

请返回一个整数数组，按查询出现的顺序，包含所有类型为 `[1, x]` 的查询结果。  

---

### 示例

#### 示例 1
```
Input: c = 5, connections = [[1,2],[2,3],[3,4],[4,5]], queries = [[1,3],[2,1],[1,1],[2,2],[1,2]]
Output: [3,2,3]
Explanation:
```

#### 示例 2
```
Input: c = 3, connections = [], queries = [[1,1],[2,1],[1,1]]
Output: [1,-1]
Explanation:
```

---

### 约束条件
- `1 <= c <= 10^5`
- `0 <= n == connections.length <= min(10^5, c * (c - 1) / 2)`
- `connections[i].length == 2`
- `1 <= ui, vi <= c`
- `ui != vi`
- `1 <= queries.length <= 2 * 10^5`
- `queries[i].length == 2`
- `queries[i][0]` 只能是 `1` 或 `2`
- `1 <= queries[i][1] <= c`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**每次查询都重新遍历整张图**。  

1. **数据结构**  
   - 用 **邻接表**（list of lists）来存储电站之间的双向电缆。可以把它想象成“一本城市地图”，每个电站对应一页，页上列出和它相连的所有电站。  
   - 用一个长度为 `c+1` 的布尔数组 `online[i]` 标记第 `i` 站是否在线，类似“电站的开关”。  

2. **查询类型**  
   - **类型 2 `[2, x]`**：直接把 `online[x]` 设为 `False`（下线），不需要改动图的结构。  
   - **类型 1 `[1, x]`**：  
     - 先用 **DFS / BFS** 从 `x` 出发，把所有 **直接或间接相连** 的电站（即同一个电网）找出来。  
     - 在这些电站里挑出仍然 **online** 的站点，取编号最小的那个；如果没有在线站点，返回 `-1`。  

3. **为什么正确**  
   - 只要我们遍历到了所有和 `x` 连通的节点，就完整地得到了 `x` 所在的电网。  
   - 再在这部分节点里找最小的在线编号，恰好就是题目要求的答案。  

#### 代码（Python）  

```python
from collections import deque
from typing import List

def powerGridMaintenance_bruteforce(
    c: int, connections: List[List[int]], queries: List[List[int]]
) -> List[int]:
    # 1. 建图（邻接表）
    graph = [[] for _ in range(c + 1)]
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)

    # 2. 记录每个电站是否在线，初始全部为 True
    online = [True] * (c + 1)

    ans = []

    # 3. 逐个处理查询
    for typ, x in queries:
        if typ == 2:                     # 下线电站
            online[x] = False
        else:                            # 查询最小在线电站
            # BFS 找到 x 所在连通分量的所有节点
            visited = [False] * (c + 1)
            q = deque([x])
            visited[x] = True
            component = []               # 记录同一电网的所有站点
            while q:
                cur = q.popleft()
                component.append(cur)
                for nb in graph[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)

            # 在 component 中找最小在线编号
            min_online = float('inf')
            for node in component:
                if online[node]:
                    min_online = min(min_online, node)

            ans.append(min_online if min_online != float('inf') else -1)

    return ans
```

> **关键行解释**  
> - `graph[u].append(v) / graph[v].append(u)`：把电缆视作双向道路，像在地图上画两条相互指向的路。  
> - `while q:` 循环是 BFS，层层展开，就像从起点逐渐探索周围的城市。  
> - `min_online = min(min_online, node)`：在遍历到的电网里挑最小的在线站点。

#### 复杂度  

- **时间复杂度**：`O(Q * (c + n))`，其中 `Q` 为查询总数。最坏情况下，每一次类型 1 查询都要遍历整张图（`c` 个节点 + `n` 条边），所以看起来像 `O(c²)`。  
  - **大白话**：如果有 10 000 条查询，而每次都要走遍 100 000 条路，那时间会非常慢，几乎是“每次都跑马拉松”。  
- **空间复杂度**：`O(c + n)` 用于存图和 `visited` 数组。  

显然，这种做法在 `c、Q` 都可以达到 `10⁵` 时会超时，需要更快的办法。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次查询都要 **重新遍历连通分量**。  
我们要把「同一个电网的成员」**提前算好**，并且在后续查询中 **快速定位**。  

思路分三步：

1. **一次性求出所有连通分量**  
   - 使用 **并查集（Union‑Find）** 或一次 DFS/BFS 把每个电站划分到所属的「电网」里。  
   - 把每个电网用一个 “根节点” `root` 表示，类似“城市的省份代码”。  

2. **为每个电网维护一个可以** **快速取最小在线编号** **的结构**  
   - 这里使用 **最小堆（heap）**。堆的特性是「随时可以拿到最小值」且插入、弹出都是 `O(log n)`。  
   - 对每个根 `root`，准备一个堆 `heap[root]`，把该电网所有电站的编号一次性 **push** 进去。  

3. **处理查询**  
   - **类型 2（下线）**：只需要把 `online[x] = False`。不必在堆里删掉，因为堆不支持高效的任意删除。我们采用 **懒删**：在以后需要取堆顶时，检查堆顶是否已经下线，若是就 `pop` 掉，直到堆顶是在线的或堆空。  
   - **类型 1（查询）**：  
     1. 找到 `x` 所属的根 `root = find(x)`（并查集的 `find` 操作），这一步是 `α(c)`，几乎是 `O(1)`。  
     2. 对 `heap[root]` 做懒删：`while heap and not online[heap[0]]: heappop(heap)`。  
     3. 此时若堆为空，说明该电网没有在线电站，返回 `-1`；否则堆顶就是 **最小在线编号**，直接返回。  

> **核心技巧解释**  
> - **并查集**：想象每个电站都有一张“身份证”，身份证上写着它所在的省份（根）。合并两座相连的电站，就像把两个省份合并成一个更大的省。查根操作 `find(x)` 就是“查看身份证上写的省份”。  
> - **最小堆 + 懒删**：堆像一个“随时可以打开的抽屉”，最小的编号永远放在最上面。下线时不立刻把抽屉里的东西搬走，而是记下来「这件东西已经失效」，等真正需要抽取时再把失效的东西扔掉。这样避免了在堆里找任意位置删除的高开销。  

#### 代码（Python）  

```python
import sys
from collections import defaultdict
import heapq
from typing import List

class UnionFind:
    """并查集（带路径压缩）"""
    def __init__(self, n: int):
        self.parent = list(range(n + 1))

    def find(self, x: int) -> int:
        # 递归写法，带路径压缩
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra      # 把 rb 所在的集合合并到 ra


def powerGridMaintenance_optimal(
    c: int, connections: List[List[int]], queries: List[List[int]]
) -> List[int]:
    # 1️⃣ 先用并查集合并所有相连的电站，得到每个电站的根（所属电网）
    uf = UnionFind(c)
    for u, v in connections:
        uf.union(u, v)

    # 2️⃣ 为每个根准备一个最小堆，装入该电网所有站点的编号
    comp_heap = defaultdict(list)          # root -> min‑heap
    for node in range(1, c + 1):
        root = uf.find(node)
        heapq.heappush(comp_heap[root], node)

    # 3️⃣ 记录每个站点是否在线，初始全部为 True
    online = [True] * (c + 1)

    ans = []

    # 4️⃣ 逐条处理查询
    for typ, x in queries:
        if typ == 2:                        # 下线
            online[x] = False
        else:                               # 查询最小在线编号
            root = uf.find(x)               # 找到所在电网的根
            heap = comp_heap[root]

            # 懒删：弹出已经下线的堆顶
            while heap and not online[heap[0]]:
                heapq.heappop(heap)

            if not heap:                     # 该电网没有在线站点
                ans.append(-1)
            else:
                ans.append(heap[0])          # 堆顶就是最小在线编号

    return ans
```

> **关键行解释**  
> - `uf.union(u, v)`: 把两座相连的电站合并到同一个省份。  
> - `comp_heap[root].push(node)`: 把同一电网的所有站点装进同一个最小堆，最小的编号自然会跑到堆顶。  
> - `while heap and not online[heap[0]]: heappop(heap)`: 懒删——只在真的需要取最小值时才把已经下线的编号清理掉。  

#### 复杂度  

- **时间复杂度**：  
  - 并查集合并所有边 `O(n α(c))`（α 为反 Ackermann 函数，几乎是常数）。  
  - 初始化堆时把每个节点 `push` 一次，总共 `O(c log c)`（每次 `push` 是 `log` 堆大小）。  
  - 处理查询：  
    - 类型 2 只做一次数组赋值 `O(1)`。  
    - 类型 1 需要 `find`（≈`O(1)`） + 可能弹出若干已经下线的堆顶。每个节点最多被弹出一次，整体仍是 `O(c log c)`。  
  - 因此 **总体** 为 `O((c + n) log c)`，在最坏情况下约 `O(10⁵ log 10⁵)`，完全可以在 1 秒左右通过。  

- **空间复杂度**：`O(c + n)`  
  - 并查集 `parent`、在线标记数组 `online`、以及所有堆中共存放 `c` 个编号。  

相较于暴力解，**每一次查询只需要 `O(log c)`**（堆操作），不再重复遍历整张图，速度提升数千倍。

---

## 心得  

- **核心技巧**：  
  1. **一次性划分连通分量**（并查集或 DFS） → 把“同一个电网”的概念固定下来。  
  2. **对每个分量维护可快速取最小值的数据结构**（最小堆 + 懒删）。  

- **该技巧适用的题型**（列举 2‑3 个类似题）：  
  1. “删除节点后查询所在连通块的最小/最大编号”。  
  2. “在动态图中维护每个连通块的最小/最大权值”。  
  3. “离线查询：在多个集合中快速取最小未删除元素”。  

- **一句话总结解题钥匙**：  
  > 先把「同一个集合」固定下来（并查集），再在每个集合里用「堆」保存成员，查询时只在堆顶做懒删即可。

---

## 反思  

- **第一反应**：直接把每次查询当成一次图遍历，想到 BFS/DFS。  
- **最容易踩的坑**  
  1. **下线节点仍然属于原来的电网**：不能在并查集里把它删掉，只需要标记 offline。  
  2. **堆里不能直接删除任意元素**：如果尝试 `heap.remove(x)` 会是 `O(n)`，导致超时。必须用懒删。  
  3. **边界情况**：孤立节点（没有任何连接）也是一个独立的电网，需要单独维护堆。  
- **下次遇到同类题，第一步该想到**：  
  > “是否可以先把所有连通块预处理好”，然后再用**适合快速取极值的结构**（堆、平衡树）在每个块内部维护状态。