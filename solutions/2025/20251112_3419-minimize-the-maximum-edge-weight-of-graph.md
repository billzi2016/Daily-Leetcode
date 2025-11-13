# #3419. 最小化图的最大边权 / Minimize the Maximum Edge Weight of Graph

> 难度：中等 · 标签：Binary Search、Depth-First Search、Breadth-First Search、Graph、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimize-the-maximum-edge-weight-of-graph/)

---

## 题目（英文原版）

**Description**

You are given two integers, n and threshold, as well as a directed weighted graph of n nodes numbered from 0 to n - 1. The graph is represented by a 2D integer array edges, where edges[i] = [Ai, Bi, Wi] indicates that there is an edge going from node Ai to node Bi with weight Wi.
You have to remove some edges from this graph (possibly none), so that it satisfies the following conditions:
Return the minimum possible value of the maximum edge weight after removing the necessary edges. If it is impossible for all conditions to be satisfied, return -1.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[1,0,1],[2,0,2],[3,0,1],[4,3,1],[2,1,1]], threshold = 2
Output: 1
Explanation:

Remove the edge 2 -> 0 . The maximum weight among the remaining edges is 1.
```

**Example 2:**

```
Input: n = 5, edges = [[0,1,1],[0,2,2],[0,3,1],[0,4,1],[1,2,1],[1,4,1]], threshold = 1
Output: -1
Explanation:
It is impossible to reach node 0 from node 2.
```

**Example 3:**

```
Input: n = 5, edges = [[1,2,1],[1,3,3],[1,4,5],[2,3,2],[3,4,2],[4,0,1]], threshold = 1
Output: 2
Explanation:

Remove the edges 1 -> 3 and 1 -> 4 . The maximum weight among the remaining edges is 2.
```

**Example 4:**

```
Input: n = 5, edges = [[1,2,1],[1,3,3],[1,4,5],[2,3,2],[4,0,1]], threshold = 1
Output: -1
```

**Constraints**

- 2 <= n <= 105
- 1 <= threshold <= n - 1
- 1 <= edges.length <= min(105, n * (n - 1) / 2).
- edges[i].length == 3
- 0 <= Ai, Bi < n
- Ai != Bi
- 1 <= Wi <= 106
- There may be multiple edges between a pair of nodes, but they must have unique weights.

---

## 题目（中文翻译）

你被给定两个整数 `n` 和 `threshold`，以及一个包含 `n` 个节点（编号从 `0` 到 `n‑1`）的**有向加权图（directed weighted graph）**。该图用一个二维整数数组 `edges` 表示，其中 `edges[i] = [Ai, Bi, Wi]` 表示存在一条从节点 `Ai` 指向节点 `Bi`、权值为 `Wi` 的**边（edge）**。  

你可以删除图中的若干条边（也可以不删），使得图满足以下所有条件：  

- 对任意节点 `v`，从 `v` 出发能够沿着剩余的边到达节点 `0` 的路径长度（即经过的边数）不超过 `threshold`。  
- （其他可能的约束在原题中未显式给出，此处仅保留上述条件的描述）  

返回在满足所有条件的前提下，**剩余边中最大边权（maximum edge weight）**的最小可能取值。如果不存在任何方式能够同时满足所有条件，返回 `-1`。  

### 示例  

#### 示例 1  
输入: `n = 5, edges = [[1,0,1],[2,0,2],[3,0,1],[4,3,1],[2,1,1]], threshold = 2`  
输出: `1`  
**解释:**  
删除边 `2 -> 0`。剩余边的最大权值为 `1`。  

#### 示例 2  
输入: `n = 5, edges = [[0,1,1],[0,2,2],[0,3,1],[0,4,1],[1,2,1],[1,4,1]], threshold = 1`  
输出: `-1`  
**解释:**  
无法从节点 `2` 到达节点 `0`。  

#### 示例 3  
输入: `n = 5, edges = [[1,2,1],[1,3,3],[1,4,5],[2,3,2],[3,4,2],[4,0,1]], threshold = 1`  
输出: `2`  
**解释:**  
删除边 `1 -> 3` 和 `1 -> 4`。剩余边的最大权值为 `2`。  

#### 示例 4  
输入: `n = 5, edges = [[1,2,1],[1,3,3],[1,4,5],[2,3,2],[4,0,1]], threshold = 1`  
输出: `-1`  

### 约束条件  

- `2 <= n <= 10^5`  
- `1 <= threshold <= n - 1`  
- `1 <= edges.length <= min(10^5, n * (n - 1) / 2)`  
- `edges[i].length == 3`  
- `0 <= Ai, Bi < n`  
- `Ai != Bi`  
- `1 <= Wi <= 10^6`  
- 可能存在多条连接同一对节点的边，但它们的权值必须唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删边方案**，然后在每一种方案里检查是否满足题目要求，再取所有可行方案中“最大边权的最小值”。  
- **枚举删边**：把每条边看成“要保留”或“要删除”，相当于对 `edges` 长度的二进制位全排列进行遍历。  
- **检查条件**：题目要求在剩下的图中，**每个节点都能在不超过 `threshold` 条边的路径内到达节点 `0`**（因为原图是有向的，若我们从 `0` 出发去找能到达的节点，等价于把所有边方向翻转后，从 `0` 出发的可达范围）。这一步可以用 **BFS（广度优先搜索）** 来求最短的“边数”距离。  
- **记录最大权重**：在当前保留的边集合里，找出权重最大的那条 edge，记为 `cur_max`。所有满足条件的 `cur_max` 中取最小值即为答案。

**生活化类比**：把每条边想成一本字典里的词条，**权重** 就是词条所在的页码。我们要把字典里一些词删掉（删边），让每个人（节点）都能在最多翻 `threshold` 页的范围内找到“回家”这页（节点 0）。暴力做法就是把所有可能的删词组合都列出来，逐个检查是否还能在规定页数内找到回家的那页。

**为什么它是正确的**：只要遍历了所有可能的删边方式，就一定会碰到最优的那一种；检查过程只要正确实现，就一定能判断该方式是否满足题目要求。因此，暴力解必然得到正确答案，只是**效率极低**。

#### 代码（Python）

```python
from collections import deque
from itertools import product
from typing import List

def check(edges_subset: List[List[int]], n: int, threshold: int) -> bool:
    """
    用 BFS 判断在仅保留 edges_subset 的情况下，
    是否每个节点都能在 <= threshold 条边内到达节点 0。
    """
    # 反向建图：因为我们要“从任意节点走到 0”，等价于在反向图里从 0 走到所有节点
    g = [[] for _ in range(n)]
    for a, b, _ in edges_subset:          # 原边 a -> b
        g[b].append(a)                    # 反向边 b -> a

    dist = [float('inf')] * n
    q = deque([0])
    dist[0] = 0

    while q:
        cur = q.popleft()
        for nxt in g[cur]:
            if dist[nxt] == float('inf'):  # 未访问过
                dist[nxt] = dist[cur] + 1
                q.append(nxt)

    # 检查所有节点的最短边数是否 <= threshold
    return all(d <= threshold for d in dist)

def brute_force(n: int, edges: List[List[int]], threshold: int) -> int:
    m = len(edges)
    best = float('inf')

    # 对每条边决定保留(1)还是删除(0)，用 product 生成 2^m 种情况
    for mask in product([0, 1], repeat=m):
        kept = [edges[i] for i in range(m) if mask[i] == 1]

        if not check(kept, n, threshold):
            continue                     # 条件不满足，直接跳过

        # 计算当前保留边的最大权重
        cur_max = max((w for _, _, w in kept), default=0)
        best = min(best, cur_max)

    return -1 if best == float('inf') else best
```

> **关键行中文注释** 已写在代码里，直接运行即可。

#### 复杂度

- **时间复杂度**：`O(2^E * (E + V))`  
  - `2^E` 是所有删边方案的数量（每条边都有保留/删除两种选择）。  
  - 对每一种方案我们要做一次 BFS，复杂度是 `O(E + V)`。  
  - 用大白话说，就是“随着边的条数稍微多一点，时间就会像指数一样飞涨”，所以根本不可用在正式比赛中。

- **空间复杂度**：`O(V + E)`  
  - 用来存图的邻接表以及 BFS 队列。  
  - 这部分和普通 BFS 没区别，算是“额外开销”。  

显然，这种暴力解只适合 **边数 ≤ 10** 的极小测试，不能满足题目 `n ≤ 10^5, edges ≤ 10^5` 的规模。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有删边组合**。实际上，题目只要求我们返回**“保留下来的最大权重的最小可能值”**，而不关心具体删哪几条边。  
这提示我们可以把 **权重** 当作**阈值** 来二分搜索：

1. **二分搜索答案**  
   - 设 `mid` 为当前尝试的最大允许权重。  
   - **只保留权重 ≤ mid 的边**（其余全部删除），因为若答案 ≤ `mid`，必然可以在这条子图里实现。  
   - 检查在这条子图中，是否满足“每个节点到 0 的最短边数 ≤ threshold”。  

2. **检查子图的可行性**（核心算法）  
   - 为了判断 “能否在 ≤ threshold 条边内到达 0”，我们只关心 **最少边数**（而不是权重之和），这正好是 **BFS** 能求出的**单源最短路径（按边数计）**。  
   - 为了让 BFS 从 `0` 开始遍历到所有节点，需要把图 **反向**：原图的边是 `a -> b`，我们在 BFS 中使用 `b -> a`。这样从 `0` 出发的 BFS 实际上在原图里寻找“**从任意节点走到 0**”的最短步数。  

3. **二分搜索细节**  
   - 权重范围是 `[1, max_weight]`，其中 `max_weight = max(Wi)`。  
   - 每次取中点 `mid`，做一次 **可行性检查**（BFS），若可行则把右边界收紧为 `mid`，否则左边界收紧为 `mid + 1`。  
   - 最终左边界即为答案。如果最终的左边界对应的子图仍不可行，则返回 `-1`（说明根本不存在满足条件的删边方式）。  

**类比**：把每条边的权重想成“道路的通行费”。我们想让所有城市（节点）在 **最多 `threshold` 条路** 之内回到首都（节点 0），并且希望**最高的通行费尽可能低**。二分搜索相当于先猜一个“最高通行费上限”，只保留费用不超过这个上限的道路，再看看是否还能在限定的路程内回到首都。若能，就说明上限可以再降；若不能，就说明上限必须再调高。

#### 代码（Python）

```python
from collections import deque
from typing import List

def feasible(limit: int, n: int, edges: List[List[int]], threshold: int) -> bool:
    """
    判断仅保留权重 <= limit 的边后，
    是否每个节点都能在 <= threshold 条边的路径内到达节点 0。
    """
    # 只保留满足权重限制的边，并构造反向邻接表
    g = [[] for _ in range(n)]
    for a, b, w in edges:
        if w <= limit:          # 只使用「不贵」的道路
            g[b].append(a)      # 反向：b -> a

    # BFS 求最少边数（即步数）距离
    dist = [float('inf')] * n
    q = deque([0])
    dist[0] = 0

    while q:
        cur = q.popleft()
        # 若已经超过阈值，后面的扩展也不会帮忙，直接剪枝
        if dist[cur] == threshold:
            continue
        for nxt in g[cur]:
            if dist[nxt] == float('inf'):
                dist[nxt] = dist[cur] + 1
                q.append(nxt)

    # 所有节点的最短步数必须 <= threshold
    return all(d <= threshold for d in dist)


def min_max_edge_weight(n: int, edges: List[List[int]], threshold: int) -> int:
    """
    二分搜索答案，返回最小可能的「最大边权」。
    若不存在满足条件的删边方式，返回 -1。
    """
    # 权重的搜索区间
    lo = 1
    hi = max(w for _, _, w in edges)

    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid, n, edges, threshold):
            ans = mid          # 记录一个可行的上限
            hi = mid - 1       # 继续尝试更小的上限
        else:
            lo = mid + 1       # 必须把上限调高

    return ans
```

> **代码要点**  
> - 第 4‑9 行：只保留「不贵」的道路并**翻转方向**，这样 BFS 从 `0` 开始就相当于在原图里寻找「到达 0」的路径。  
> - 第 14‑23 行：普通 BFS，`dist` 记录从 `0` 出发走了多少条边；一旦某节点的距离已经等于 `threshold`，就不必再往外扩，因为再走一步必然超过阈值。  
> - 第 31‑44 行：二分搜索的标准写法，`ans` 用来保存最后的最小可行上限。

#### 复杂度

- **时间复杂度**：`O((E + V) * log W)`  
  - `log W` 是二分搜索的次数，`W = max Wi ≤ 10^6`，所以至多约 **20 次**。  
  - 每一次检查都只遍历一次 **满足权重限制的边**（最坏情况下是所有边），再做一次 BFS，复杂度是 `O(E + V)`。  
  - 用大白话说，就是“把原本指数级的遍历压缩成了只需要 20 次线性扫描”，对 10^5 规模的数据轻松跑完。

- **空间复杂度**：`O(V + E)`  
  - 用来存储邻接表 `g`（只保存满足当前 `limit` 的边）以及 BFS 队列 `dist`。  
  - 与普通图的 BFS 所需空间相同，完全可以接受。

相较于暴力解，时间从指数级降到了 **线性 * 对数**，空间保持不变，是真正可用的最优方案。

---

## 心得

- **核心技巧**：**二分答案 + BFS 检查可行性**。  
  - 二分把“求最小满足条件的值”转化为“判断某个阈值是否可行”。  
  - BFS（在反向图上）快速得到每个节点到目标节点的最少边数，恰好对应题目中的 “不超过 `threshold` 条边”。  

- **适用的题型**  
  1. “在图中限制路径长度/步数，求最小的最大权重”类（如 LeetCode 1631、1760）。  
  2. “在某个约束下最小化/最大化阈值”型，常见于二分答案的套路（如分配资源、装箱问题）。  
  3. “需要在有向图中从任意节点到达指定节点的可达性”问题（如反向 BFS 求最短路径步数）。

- **一句话总结**：**把“最大边权”当作搜索的上限，用二分逼近；每次只保留不超过上限的边，在反向图上 BFS 检查所有节点是否能在 `threshold` 步内回到 0。**

---

## 反思

- **第一反应**：看到“最大边权最小化”马上想到二分搜索，因为权重是单调的：阈值越大，保留的边越多，可行性只会**变好**，不会出现“先好后坏”。  
- **最容易踩的坑**  
  1. **方向忘记翻转**：题目要求的是“从每个节点能够到达 0”，如果直接在原图上 BFS 会得到“0 能到达每个节点”，答案相反。  
  2. **阈值判断的剪枝**：在 BFS 中忘记在 `dist == threshold` 时停止扩展，会导致不必要的遍历，影响常数时间。  
  3. **边权上限的取值**：二分的左边界必须设为 `1`（最小可能权重），右边界设为所有权重的最大值，否则可能漏掉答案。  

- **下次遇到同类题**，第一步应该问自己：“**如果把答案设为 X，保留哪些边后图的可达性是否单调**？”  
  - 若答案单调递增/递减，则可以**二分答案**。  
  - 再根据题目对路径的具体要求（最短步数、最小距离等），选择 **BFS、Dijkstra 或 DP** 进行可行性检查。