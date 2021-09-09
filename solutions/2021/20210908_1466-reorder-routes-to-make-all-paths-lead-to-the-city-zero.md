# #1466. 重新排列道路，使所有路径通向城市 0 / Reorder Routes to Make All Paths Lead to the City Zero

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/)

---

## 题目（英文原版）

**Description**

There are n cities numbered from 0 to n - 1 and n - 1 roads such that there is only one way to travel between two different cities (this network form a tree). Last year, The ministry of transport decided to orient the roads in one direction because they are too narrow.
Roads are represented by connections where connections[i] = [ai, bi] represents a road from city ai to city bi.
This year, there will be a big event in the capital (city 0), and many people want to travel to this city.
Your task consists of reorienting some roads such that each city can visit the city 0. Return the minimum number of edges changed.
It's guaranteed that each city can reach city 0 after reorder.

**Examples**

**Example 1:**

```
Input: n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
Output: 3
Explanation: Change the direction of edges show in red such that each node can reach the node 0 (capital).
```

**Example 2:**

```
Input: n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]
Output: 2
Explanation: Change the direction of edges show in red such that each node can reach the node 0 (capital).
```

**Example 3:**

```
Input: n = 3, connections = [[1,0],[2,0]]
Output: 0
```

**Constraints**

- 2 <= n <= 5 * 104
- connections.length == n - 1
- connections[i].length == 2
- 0 <= ai, bi <= n - 1
- ai != bi

---

## 题目（中文翻译）

给定 **n** 个城市，编号为 `0` 到 `n - 1`，以及恰好 `n - 1` 条道路，使得任意两座不同的城市之间仅有唯一一条路径（该网络构成一棵树）。去年，交通部决定将所有道路定向为单向，因为道路太窄。

道路由 `connections` 表示，其中 `connections[i] = [ai, bi]` 表示一条从城市 `ai` 指向城市 `bi` 的单向道路。

今年，首都（城市 `0`）将举办大型活动，很多人希望前往该城市。你的任务是重新定向部分道路，使得每个城市都能够到达城市 `0`。返回需要改变方向的最少边数。题目保证在重新定向后，每个城市都能到达城市 `0`。

**示例 1**  
**输入**: `n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]`  
**输出**: `3`  
**解释**: 将红色标出的边的方向改为指向城市 `0`，使得所有节点都能够到达节点 `0`（首都）。

**示例 2**  
**输入**: `n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]`  
**输出**: `2`  
**解释**: 将红色标出的边的方向改为指向城市 `0`，使得所有节点都能够到达节点 `0`（首都）。

**示例 3**  
**输入**: `n = 3, connections = [[1,0],[2,0]]`  
**输出**: `0`  

**约束条件**  
- `2 <= n <= 5 * 10^4`  
- `connections.length == n - 1`  
- `connections[i].length == 2`  
- `0 <= ai, bi <= n - 1`  
- `ai != bi`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的原始网络是一棵 **树**（`n` 个城市、`n‑1` 条道路，且任意两座城市之间只有唯一一条路径）。  
每条道路都有固定的方向，例如 `[a, b]` 表示只能 **从 `a` 开车到 `b`**。

> **直觉**：我们想让 **所有城市都能到达 0**。  
> 那么只要找出哪些道路的方向“阻挡了”从某座城市回到 0，就把它们翻转。

最直接的做法是 **对每个城市单独检查**：  
1. 从该城市出发，用 **广度优先搜索（BFS）** 按照原有的有向道路寻找能否到达 0。  
2. 如果找不到，就把 **唯一的那条通往 0 的道路**（因为是树，必有唯一路径）翻转。  
3. 重复上述步骤，直到所有城市都能到达 0。

> **类比**：把道路想成“一条只能单向走的走廊”。我们让每个人从自己的房间出发，沿着走廊走到大礼堂（城市 0）。如果走廊的方向让他走不通，就把这条走廊的门换个方向。

**为什么正确？**  
树的结构保证从任意城市到 0 的路径唯一。只要把这条路径上 **第一个方向错误的道路** 翻转，城市就能顺利到达 0。不断对每个城市这样处理，最终所有城市都会有通往 0 的有向路径。

**时间/空间复杂度**  
- 对每个城市我们都要跑一次 BFS，最坏情况下遍历 **所有 `n‑1` 条边**。  
  所以时间复杂度是 `O(n * n) = O(n²)`。  
  > 大白话：如果城市有 10,000 座，算法大约要检查 10,000 × 10,000 = 1 亿次“走廊”，会很慢。
- 除了存图的邻接表外，只用了常数级别的额外变量，空间是 `O(n)`（存图本身）。

#### 代码（Python）

```python
from collections import defaultdict, deque

def minReorder_bruteforce(n, connections):
    # 建立有向邻接表，edges_set 用来快速判断某条有向边是否原本是 a->b
    graph = defaultdict(list)          # 无向图（只记录相邻节点）
    edges_set = set()                   # 存储原始有向边 (a, b)
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)              # 把树当成无向图，方便遍历唯一路径
        edges_set.add((a, b))

    # 记录已经翻转的边数
    answer = 0

    # 对每个城市 i (i != 0) 检查是否能到达 0
    for i in range(1, n):
        # BFS 找到从 i 到 0 的唯一路径（因为是树）
        parent = {i: None}
        q = deque([i])
        while q:
            cur = q.popleft()
            if cur == 0:
                break
            for nxt in graph[cur]:
                if nxt not in parent:   # 防止回到已经走过的节点
                    parent[nxt] = cur
                    q.append(nxt)

        # 回溯路径，找第一条方向错误的边
        node = 0
        while node != i:
            p = parent[node]           # p -> node 是路径上的一条无向边
            # 如果原来的方向是 p -> node，则说明这条边是“正确的”
            # 否则（原来是 node -> p），说明需要翻转
            if (node, p) in edges_set:
                # 需要翻转一次
                answer += 1
                # 把翻转后的方向加入 edges_set，后面其他城市不需要再翻转
                edges_set.remove((node, p))
                edges_set.add((p, node))
                break                 # 只翻转路径上第一条错误的边即可
            node = p

    return answer
```

> **关键行注释**  
> - `graph` 用来把树当成 **无向** 图，这样我们可以从任意城市走到 0，像在“迷宫里找路”。  
> - `edges_set` 相当于 **字典查词**：键是 `(起点, 终点)`，如果键在集合里说明这条路原本是 **从起点指向终点**。  
> - `parent` 记录 BFS 过程中每个节点的前驱，帮助我们把 **唯一路径** 反向恢复出来。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  > 对每个城市都跑一次 BFS（最坏遍历 `n‑1` 条边），于是总操作次数约为 `n × (n‑1)`。  
- **空间复杂度**：`O(n)`  
  > 除了存图（`O(n)`）外，只用了几个额外的集合和队列，和城市数量呈线性关系。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每个城市都要重新遍历整棵树**，导致 `O(n²)`。  
其实我们只需要 **一次遍历** 就能把所有需要翻转的道路一次性找出来。

**核心观察**  

1. 把所有道路视为 **无向** 的（因为题目保证把方向改对后每座城市都能到达 0）。  
2. 从 **根节点 0** 开始做一次 **深度优先搜索（DFS）**。  
3. 当我们沿着 DFS 边走到一个相邻的城市 `v` 时，有两种情况  
   - 原来的方向是 `0 -> v`（即从父节点指向子节点），这条路 **阻挡** 了 `v` 回到 0，需要 **翻转**。  
   - 原来的方向是 `v -> 0`，则已经是 “子指向父”，不需要翻转。  

4. 对所有子树递归执行同样的检查，**只要在遍历时统计向外的边**，答案就是这些统计的总数。

> **类比**：想象把树倒过来，根在地面，所有枝桠向上。我们站在根（0）往上爬，每爬到一根枝桠，就检查它的方向是“向上”还是“向下”。如果向上（从根指向子），说明这根枝桠的方向是“逆风”，需要调转。

**为什么一次遍历就够了？**  
因为树没有环，**从根出发的唯一路径** 已经覆盖了所有城市。只要在这条唯一路径上看到向外的边，就一定是该城市到根的唯一阻挡点，翻转一次即可。再往下的子树不受已经翻转的边影响，因为我们已经把“方向正确的”边当作已经指向父节点。

#### 代码（Python）

```python
from collections import defaultdict

def minReorder(n, connections):
    # 1. 把有向道路同时存入两种结构
    #    - undirected: 用来遍历整棵树（无向）
    #    - directed_set: 用来快速判断一条无向边原本的方向是否是 from -> to
    undirected = defaultdict(list)
    directed_set = set()               # (from, to) 表示原始方向
    for a, b in connections:
        undirected[a].append(b)
        undirected[b].append(a)
        directed_set.add((a, b))

    # 2. 深度优先搜索
    visited = [False] * n
    ans = 0

    def dfs(node):
        nonlocal ans
        visited[node] = True
        for nxt in undirected[node]:
            if visited[nxt]:
                continue
            # 如果原来的方向是 node -> nxt，则这条边是“向外”的，需要翻转
            if (node, nxt) in directed_set:
                ans += 1
            # 继续向下搜索
            dfs(nxt)

    dfs(0)            # 从首都 0 出发
    return ans
```

> **关键行注释**  
> - `undirected`：把道路当成 **双向通道**，相当于把地图的“单行道”改成“双行道”，方便我们遍历。  
> - `directed_set`：类似 **字典查词**，键 `(a, b)` 告诉我们 “这条路原本是从 a 指向 b”。  
> - `if (node, nxt) in directed_set:`：如果在当前 DFS 边上，方向是 **父指向子**，说明这条路需要调转。  
> - `visited` 防止在树里回到已经走过的节点，避免死循环（虽然树没有环，但因为我们把它当成无向图，需要这一步）。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  > 只遍历了每条边一次（`n‑1` 条），相当于一次 “走遍所有走廊”。  
- **空间复杂度**：`O(n)`  
  > 用邻接表存图、visited 数组以及递归栈，均随城市数量线性增长。

---

## 心得

- **核心技巧**：把有向树 **先当成无向树遍历**，在 DFS/ BFS 过程中判断原始方向是否“指向父节点”。只要统计“指向子节点”的边数，就是最小翻转次数。  
- **适用的题型**  
  1. **把所有节点指向根节点**（如 LeetCode 1466 `Reorder Routes to Make All Paths Lead to the City Zero`）。  
  2. **最小翻转使所有节点可达指定节点**（如 1196 `Network Delay Time` 的变形）。  
  3. **在树上统计满足特定方向的边**（如 1462 `Course Schedule IV` 的拓扑方向统计）。  
- **一句话总结**：**一次从根出发的 DFS，遇到“父指向子”的边就翻转**——这把“遍历+方向检查”变成了线性时间的钥匙。

---

## 反思

- **第一反应**：把每条道路都当成要检查的对象，想要对每个城市单独跑 BFS/DFS，结果是 `O(n²)`，显然不够快。  
- **最容易踩的坑**  
  - 把图误当成 **有向** 的去遍历，会导致遗漏那些原本指向父节点的边，导致计数错误。  
  - 忘记在把道路当成 **无向** 图时使用 `visited` 防止回到已经访问的节点，容易出现无限递归。  
  - 边界情况：`n = 2` 时只有一条道路，代码仍需正常工作。  
- **下次遇到同类题**：**先把结构转成无向树**，**从根节点做一次 DFS/BFS**，**在遍历时直接统计方向错误的边**——这一步往往能立刻把时间复杂度降到 `O(n)`。