# #2421. **好路径的数量** / Number of Good Paths

> 难度：困难 · 标签：Array、Hash Table、Tree、Union Find、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/number-of-good-paths/)

---

## 题目（英文原版）

**Description**

There is a tree (i.e. a connected, undirected graph with no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges.
You are given a 0-indexed integer array vals of length n where vals[i] denotes the value of the ith node. You are also given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
A good path is a simple path that satisfies the following conditions:
Return the number of distinct good paths.
Note that a path and its reverse are counted as the same path. For example, 0 -> 1 is considered to be the same as 1 -> 0. A single node is also considered as a valid path.

**Examples**

**Example 1:**

```
Input: vals = [1,3,2,1,3], edges = [[0,1],[0,2],[2,3],[2,4]]
Output: 6
Explanation: There are 5 good paths consisting of a single node.
There is 1 additional good path: 1 -> 0 -> 2 -> 4.
(The reverse path 4 -> 2 -> 0 -> 1 is treated as the same as 1 -> 0 -> 2 -> 4.)
Note that 0 -> 2 -> 3 is not a good path because vals[2] > vals[0].
```

**Example 2:**

```
Input: vals = [1,1,2,2,3], edges = [[0,1],[1,2],[2,3],[2,4]]
Output: 7
Explanation: There are 5 good paths consisting of a single node.
There are 2 additional good paths: 0 -> 1 and 2 -> 3.
```

**Example 3:**

```
Input: vals = [1], edges = []
Output: 1
Explanation: The tree consists of only one node, so there is one good path.
```

**Constraints**

- n == vals.length
- 1 <= n <= 3 * 104
- 0 <= vals[i] <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- edges represents a valid tree.

---

## 题目（中文翻译）

There is a tree（即一棵连通的无向无环图） consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges.  
You are given a 0-indexed integer array `vals` of length n where `vals[i]` denotes the value of the i‑th node. You are also given a 2D integer array `edges` where `edges[i] = [ai, bi]` denotes that there exists an undirected edge connecting nodes `ai` and `bi`.  

A good path（好路径） is a simple path that satisfies the following conditions:  

Return the number of distinct good paths.  
Note that a path and its reverse are counted as the same path. For example, `0 -> 1` is considered to be the same as `1 -> 0`. A single node is also considered as a valid path.

---

### 示例

#### 示例 1
**输入**  
`vals = [1,3,2,1,3]`  
`edges = [[0,1],[0,2],[2,3],[2,4]]`  

**输出**  
`6`  

**解释**  
共有 5 条只包含单个节点的好路径。  
还有 1 条额外的好路径：`1 -> 0 -> 2 -> 4`。  
（反向路径 `4 -> 2 -> 0 -> 1` 与 `1 -> 0 -> 2 -> 4` 被视为相同。）  
需要注意的是 `0 -> 2 -> 3` 不是好路径，因为 `vals[2] > vals[0]`。

#### 示例 2
**输入**  
`vals = [1,1,2,2,3]`  
`edges = [[0,1],[1,2],[2,3],[2,4]]`  

**输出**  
`7`  

**解释**  
共有 5 条只包含单个节点的好路径。  
另外还有 2 条好路径：`0 -> 1` 和 `2 -> 3`。

#### 示例 3
**输入**  
`vals = [1]`  
`edges = []`  

**输出**  
`1`  

**解释**  
这棵树仅包含一个节点，因此只有一条好路径。

---

### 约束条件
- `n == vals.length`
- `1 <= n <= 3 * 10^4`
- `0 <= vals[i] <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= ai, bi < n`
- `ai != bi`
- `edges` 表示一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的路径**，逐一判断它是否满足 “好路径” 的定义。  
因为这是一棵树，任意两个节点之间恰好有唯一一条简单路径。我们可以：

1. 先把树用邻接表保存（`graph[i]` 保存所有和 `i` 相连的节点），这就像把每个城市的所有直达道路列出来，方便随时查找。  
2. 对每一对节点 `(u, v)`（包括 `u == v`），用一次 DFS/BFS 找出它们唯一的路径。  
3. 检查这条路径上所有节点的值是否 **不大于** 起点/终点的最大值，且路径两端的值相等。若满足，则计数 +1。  

> **类比**：把哈希表想成一本字典，`key` 是单词，`value` 是页码；这里的邻接表也是一种“字典”，`key` 是节点编号，`value` 是它的相邻节点列表。

**为什么能得到正确答案**  
树的性质保证了每对节点只有唯一一条路径，遍历所有节点对就不会漏掉任何可能的好路径；再对每条路径做完整的检查，只有符合条件的才计数，故答案必然正确。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def number_of_good_paths_bruteforce(vals: List[int], edges: List[List[int]]) -> int:
    n = len(vals)
    # 建立邻接表
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # 用 BFS 找到两点之间唯一的路径（返回路径上的节点序列）
    def bfs_path(start: int, target: int) -> List[int]:
        q = deque([start])
        parent = {start: -1}
        while q:
            cur = q.popleft()
            if cur == target:
                break
            for nxt in graph[cur]:
                if nxt not in parent:
                    parent[nxt] = cur
                    q.append(nxt)
        # 逆向重建路径
        path = []
        node = target
        while node != -1:
            path.append(node)
            node = parent[node]
        return path[::-1]          # 反转得到从 start 到 target 的顺序

    ans = 0
    # 枚举所有 (u, v) 对，u <= v 保证不重复计数
    for u in range(n):
        for v in range(u, n):
            path = bfs_path(u, v)
            max_val = max(vals[x] for x in path)          # 路径上的最大节点值
            if vals[u] == vals[v] == max_val:             # 两端相等且为最大值
                ans += 1
    return ans
```

> 关键行中文注释已经写在代码里，直接运行即可验证小样例。

#### 复杂度

- **时间复杂度**：`O(n³)`（最坏情况）  
  - 外层两层循环遍历 `O(n²)` 对节点。  
  - 对每对节点进行一次 BFS，遍历整棵树的时间是 `O(n)`。  
  - 因此整体是 `O(n³)`，在 `n=3·10⁴` 时根本跑不完。  
  - 大白话：如果把 `n` 想成“一百”，`n³` 就是“一百万”，明显太慢了。

- **空间复杂度**：`O(n)`  
  - 存邻接表、BFS 队列以及 `parent` 哈希表都和节点数成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要重新遍历整棵树** 来找路径。  
观察题目可以发现：

1. 好路径的两端必须拥有 **相同且是路径上最大的值**。  
2. 如果我们只考虑 **值不大于当前值的节点**，这些节点之间的连通块（connected component）已经确定。  
3. 在同一个连通块里，任意两个值相等且为该块的最大值的节点之间，都必然存在一条满足条件的好路径（因为路径上所有节点值都 ≤ 该最大值）。

因此，我们可以 **从小到大逐步加入节点**，并使用 **并查集（Union‑Find）** 动态维护连通块：

- 先把所有节点按 `vals[i]` 从小到大排序。  
- 依次处理每个 **相同值的节点集合**（例如值为 2 的所有节点）。  
- 对于当前值 `v`，把它的所有 **邻居中值 ≤ v** 的边“打开”，即在并查集中把这两个节点所在的集合合并。此时，所有值 ≤ v 的节点已经形成若干连通块。  
- 接下来统计 **在这些连通块里，值恰好等于 v 的节点有多少**。设在某块中有 `k` 个这样的节点，则这块内部可以形成 `k * (k-1) / 2` 条两端不同的好路径，加上每个节点自身算作一条长度为 0 的好路径（在最终答案里已经计数）。  
- 把所有块的贡献累加，就是答案。

> **并查集类比**：想象每个节点是一本书，书之间可以通过相同主题的目录链接在一起。并查集帮助我们快速判断两本书是否已经在同一本“大书”里（即同一个连通块），合并操作就像把两本书的目录合并成一本更大的目录。

**关键细节**  

- 只在 **当前值** 的节点之间计数，不会把更小值的节点算进去，因为它们的最大值不是当前值。  
- 合并时只考虑 **邻居值 ≤ 当前值**，防止把更大的值提前拉进来破坏“最大值是端点”的条件。  
- 由于树的边数为 `n-1`，每条边最多被检查两次（一次在较小端的处理时，一次在较大端的处理时），整体是线性级别。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

class UnionFind:
    """并查集实现，支持路径压缩和按大小合并"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n                 # 维护每个根节点的集合大小

    def find(self, x: int) -> int:
        # 递归路径压缩
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # 按大小合并，保证树的深度尽可能小
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]


def number_of_good_paths(vals: List[int], edges: List[List[int]]) -> int:
    n = len(vals)
    # 1. 建图（邻接表）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # 2. 按节点值排序，得到值 -> 节点列表 的映射
    nodes_by_val = defaultdict(list)
    for i, v in enumerate(vals):
        nodes_by_val[v].append(i)
    sorted_vals = sorted(nodes_by_val.keys())   # 从小到大

    uf = UnionFind(n)
    ans = 0

    # 3. 逐个值处理
    for v in sorted_vals:
        # 3.1 把所有 “值 <= v” 的邻边都合并进来
        for node in nodes_by_val[v]:
            for nb in graph[node]:
                if vals[nb] <= v:               # 只合并不大于当前值的邻居
                    uf.union(node, nb)

        # 3.2 统计在同一连通块里，值恰好等于 v 的节点数量
        comp_cnt = defaultdict(int)   # root -> 该块中值为 v 的节点数
        for node in nodes_by_val[v]:
            root = uf.find(node)
            comp_cnt[root] += 1

        # 3.3 计算贡献：每个块内部可以形成 C(k,2) 条好路径
        for k in comp_cnt.values():
            ans += k * (k - 1) // 2   # 两端不同的好路径数
        # 单节点路径已经在最终答案里计数一次，稍后整体 +n（下面统一加）

    # 4. 每个节点本身也是一条好路径
    ans += n
    return ans
```

> 代码中的每一步都有中文注释，直接拷贝运行即可通过示例。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 对节点值排序需要 `O(n log n)`。  
  - 之后遍历每条边至多两次（每端各一次），并查集的 `find/union` 近似 `O(α(n))`（α 为极慢增长的阿克曼函数），可以视作常数。  
  - 因此整体是 `O(n log n)`，远快于暴力的 `O(n³)`。  
  - 大白话：如果 `n=30,000`，`n log n` 大约是 `30,000 * 15 ≈ 450,000`，在一秒内轻松跑完。

- **空间复杂度**：`O(n)`  
  - 存邻接表、并查集数组以及若干哈希表，都是和节点数线性相关。

---

## 心得

- **核心技巧**：**按值从小到大逐步并入 + 并查集**，利用“最大值必须在端点”这一限制，把原本需要遍历路径的问题转化为 **连通块计数**。  
- **适用的题型**  
  1. “路径上最大/最小值受限”的树/图题目（如 *Maximum Number of Good Paths*、*Count Paths With Max Value*）。  
  2. 需要统计 **同值节点在同一连通块** 的组合数问题（如 *Number of Islands With Same Height*）。  
- **一句话总结**：**把树拆成“值 ≤ 当前值”的连通块，块内部相同最大值的节点两两相连即构成好路径**。

---

## 反思

- **第一反应**：看到“好路径”涉及“最大值在两端”，立刻想到枚举所有路径并逐条检查。  
- **最容易踩的坑**  
  - **遗漏单节点路径**：记得每个节点本身也是一条合法路径。  
  - **合并边的条件**：只能在 “邻居值 ≤ 当前值” 时才 union，防止把更大的值提前拉进来破坏最大值的要求。  
  - **同一值的批处理**：如果不按批处理，而是逐个节点立即计数，可能会把同一连通块中后加入的节点计入错误的组合数。  
- **下次遇到同类题**：第一步先 **把节点按关键属性（值、权重）排序**，然后 **用并查集维护满足该属性的子图**，最后 **在每个连通块内部统计组合**。这样既能避免重复遍历，又能利用结构化的计数公式得到答案。