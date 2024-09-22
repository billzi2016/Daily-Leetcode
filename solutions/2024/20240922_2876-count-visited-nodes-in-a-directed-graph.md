# #2876. 计数有向图中访问的节点 / Count Visited Nodes in a Directed Graph

> 难度：困难 · 标签：Dynamic Programming、Graph、Memoization · [LeetCode 链接](https://leetcode.com/problems/count-visited-nodes-in-a-directed-graph/)

---

## 题目（英文原版）

**Description**

There is a directed graph consisting of n nodes numbered from 0 to n - 1 and n directed edges.
You are given a 0-indexed array edges where edges[i] indicates that there is an edge from node i to node edges[i].
Consider the following process on the graph:
Return an array answer where answer[i] is the number of different nodes that you will visit if you perform the process starting from node i.

**Examples**

**Example 1:**

```
Input: edges = [1,2,0,0]
Output: [3,3,3,4]
Explanation: We perform the process starting from each node in the following way:
- Starting from node 0, we visit the nodes 0 -> 1 -> 2 -> 0. The number of different nodes we visit is 3.
- Starting from node 1, we visit the nodes 1 -> 2 -> 0 -> 1. The number of different nodes we visit is 3.
- Starting from node 2, we visit the nodes 2 -> 0 -> 1 -> 2. The number of different nodes we visit is 3.
- Starting from node 3, we visit the nodes 3 -> 0 -> 1 -> 2 -> 0. The number of different nodes we visit is 4.
```

**Example 2:**

```
Input: edges = [1,2,3,4,0]
Output: [5,5,5,5,5]
Explanation: Starting from any node we can visit every node in the graph in the process.
```

**Constraints**

- n == edges.length
- 2 <= n <= 105
- 0 <= edges[i] <= n - 1
- edges[i] != i

---

## 题目（中文翻译）

给定一个包含 **n** 个节点（编号为 `0` 到 `n - 1`）且恰好有 **n** 条有向边的有向图。  
你得到一个下标从 **0** 开始的数组 `edges`，其中 `edges[i]` 表示从节点 `i` 指向节点 `edges[i]` 的一条有向边。

考虑在该图上进行如下过程：

- 从起始节点 `i` 开始，访问当前节点并记录下来。  
- 然后沿着当前节点的唯一出边移动到 `edges[current]`，继续访问该节点。  
- 重复上述步骤，直至再次访问到已经访问过的节点为止（即出现第一次重复）。

返回一个数组 `answer`，其中 `answer[i]` 为 **从节点 `i` 开始执行上述过程时能够访问到的不同节点的数量**。

---

### 示例

**示例 1**

```
输入: edges = [1,2,0,0]
输出: [3,3,3,4]
解释:
- 从节点 0 开始，访问顺序为 0 → 1 → 2 → 0，访问到的不同节点数为 3。
- 从节点 1 开始，访问顺序为 1 → 2 → 0 → 1，访问到的不同节点数为 3。
- 从节点 2 开始，访问顺序为 2 → 0 → 1 → 2，访问到的不同节点数为 3。
- 从节点 3 开始，访问顺序为 3 → 0 → 1 → 2 → 0，访问到的不同节点数为 4。
```

**示例 2**

```
输入: edges = [1,2,3,4,0]
输出: [5,5,5,5,5]
解释: 从任意节点出发，都可以遍历图中的所有 5 个节点。
```

---

### 约束

- `n == edges.length`
- `2 <= n <= 10^5`
- `0 <= edges[i] <= n - 1`
- `edges[i] != i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从每个起点一直沿着唯一的出边走下去，直到再次回到已经访问过的节点**，这时就形成了一个环（cycle），停止计数。  
因为每个节点只有一条出边，整个过程就像在 **一条单行道上不断前进**，遇到已经走过的路口就停下来。  

我们可以把已经走过的节点放进一个 `set`（相当于查字典的“记事本”，里面存的是已经出现过的“词”），每走一步就往集合里加。如果新走到的节点已经在集合里，说明出现了环，遍历结束，集合的大小就是答案。

**为什么正确**  
- 题目保证每个节点都有且仅有一条出边，所以从任意起点出发的路径是唯一的，必定会在有限步数内进入环（因为图的节点数是有限的，必然出现重复）。
- 我们把所有出现过的节点都记录下来，最终集合的大小正好等于“不同节点的数量”。  

**时间/空间复杂度**  
- 对每个起点，我们最坏要遍历整个图一次，**时间复杂度是 O(n²)**（n 是节点数），因为会有 `n` 次遍历，每次最坏走 `n` 步。  
- 为每一次遍历都要维护一个 `set`，最多会存 `n` 个节点，**空间复杂度是 O(n)**（不计答案数组本身）。

> 大白话解释：  
> O(n²) 就像我们有 n 本书，每本书都要把所有 n 页都读一遍，显然太慢了。  

#### 代码（Python）

```python
from typing import List

def countVisitedNodes_bruteforce(edges: List[int]) -> List[int]:
    n = len(edges)
    ans = [0] * n                     # 最终答案数组
    for start in range(n):            # 从每个节点出发
        visited = set()               # 记录已经走过的节点
        cur = start
        while cur not in visited:     # 只要没有进环，就继续走
            visited.add(cur)          # 把当前节点加入集合（相当于记事本）
            cur = edges[cur]          # 沿唯一的出边前进
        ans[start] = len(visited)    # 集合大小 = 不同节点数量
    return ans
```

#### 复杂度

- **时间复杂度：O(n²)**  
  对每个起点最多遍历 n 步，n 个起点所以是 n×n。  
- **空间复杂度：O(n)**  
  `visited` 集合最多存 n 个节点，答案数组也需要 O(n) 空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历同一段路径**。  
实际上，**图中每个连通块都有唯一的环**（因为每个节点出度为 1），环外的节点形成若干条“树枝”，这些树枝的方向都是指向环（或指向更靠近环的节点）。  

我们可以把问题分两步：

1. **先算出所有环上节点的答案**。  
   - 如果一个环的长度是 `k`，那么环上每个节点访问的不同节点数恰好是 `k`（因为只能在环内循环）。  
   - 环的长度可以通过 **拓扑剪枝**（把入度为 0 的节点逐层删掉）得到，剩下的未被删掉的节点必然在环上。

2. **再把答案向外传播**（自底向上 DP）。  
   - 对于不在环上的节点 `u`，它唯一的后继是 `v = edges[u]`。  
   - 当 `v` 的答案已经算好时，`u` 的答案就是 `ans[v] + 1`（因为 `u` 先访问自己，再按照 `v` 的路径继续走）。  
   - 这正好是 **记忆化深度优先搜索（DFS + memo）** 的过程：对每个节点递归求答案，如果后继的答案已经在 `memo` 中，就直接使用。

**核心数据结构**  
- **入度数组**：`indeg[i]` 表示指向节点 `i` 的边的数量。相当于“有多少人指着你”。  
- **队列**（或列表）保存所有入度为 0 的节点，用来做拓扑剪枝。  
- **答案数组 `ans`**：保存每个节点的访问数量，未计算的用 `0` 或 `-1` 标记。  
- **递归函数 `dfs(u)`**：返回从 `u` 开始可以访问的不同节点数，内部使用 `ans` 进行记忆化。

**步骤图示（文字版）**  

```
1. 计算每个节点的入度
2. 把所有入度为 0 的节点放进队列，逐个弹出并“删除”它们的出边
   → 这些被删除的节点一定不在环上
3. 剩下的节点全都是环上的节点
   → 对每个环，用一次遍历得到环长 k，所有环上节点的答案设为 k
4. 对所有节点执行 memoized DFS
   → 如果当前节点已经有答案，直接返回
   → 否则 ans[u] = dfs(edges[u]) + 1
```

这样每条边只会被访问常数次，时间线性。

#### 代码（Python）

```python
from typing import List
from collections import deque

def countVisitedNodes(edges: List[int]) -> List[int]:
    n = len(edges)
    indeg = [0] * n                     # 入度数组
    for v in edges:                     # 统计每个节点的入度
        indeg[v] += 1

    # ---------- 1. 拓扑剪枝，找出所有环上的节点 ----------
    q = deque([i for i in range(n) if indeg[i] == 0])  # 入度为 0 的节点
    on_cycle = [True] * n               # 初始都认为在环上，后面会剔除

    while q:                             # 类似“剔除树枝”
        u = q.popleft()
        on_cycle[u] = False              # u 不是环上的节点
        v = edges[u]                     # 唯一的后继
        indeg[v] -= 1                    # 删除 u -> v 这条边
        if indeg[v] == 0:                # 若 v 现在入度为 0，加入队列
            q.append(v)

    # ---------- 2. 计算环上节点的答案 ----------
    ans = [0] * n                        # 最终答案数组，0 表示未计算
    visited = [False] * n                # 记录环遍历时是否已经处理

    for i in range(n):
        if on_cycle[i] and not visited[i]:
            # 从 i 出发顺时针遍历整条环，统计环长
            cur = i
            cycle_nodes = []
            while not visited[cur]:
                visited[cur] = True
                cycle_nodes.append(cur)
                cur = edges[cur]         # 继续沿唯一出边走
            k = len(cycle_nodes)        # 环的长度
            for node in cycle_nodes:
                ans[node] = k            # 环上每个点的答案都是环长

    # ---------- 3. 记忆化 DFS 计算非环节点 ----------
    def dfs(u: int) -> int:
        """返回从 u 开始可以访问的不同节点数"""
        if ans[u] != 0:                 # 已经算好（环上或已递归得到）
            return ans[u]
        # u 不在环上，先递归求后继的答案
        ans[u] = dfs(edges[u]) + 1
        return ans[u]

    for i in range(n):
        if ans[i] == 0:                 # 仍未计算的必然是树枝上的节点
            dfs(i)

    return ans
```

#### 复杂度

- **时间复杂度：O(n)**  
  - 入度统计、拓扑剪枝、环遍历、DFS 每一步都只遍历每条边一次，等价于线性时间。  
  - 与暴力解的 O(n²) 相比，省去了大量重复遍历。

- **空间复杂度：O(n)**  
  - 需要 `indeg、on_cycle、visited、ans` 四个长度为 n 的数组/列表，外加递归栈最深不超过 n（在最坏的链状结构下），整体仍是线性空间。

---

## 心得

- **核心技巧**：利用“每个节点出度为 1” 的特殊性质，把图划分为 **环 + 指向环的树枝**，先求环上答案，再用 **记忆化递归（DP）** 把答案向外传播。  
- **适用的题型**  
  1. *“找环的长度”* 类似题目，例如 LeetCode 142（环形链表 II）  
  2. *“函数图的遍历次数”* 这类每个点指向唯一下一个点的图，如 LeetCode 2360（图中每个点的距离）  
  3. *“求每个节点的最终停留点”*，如 LeetCode 802（找到最终的安全状态）  
- **一句话总结解题钥匙**：**先把环弄清楚，再把树枝的答案递归地“加一”传递过去**。

---

## 反思

- **第一反应**：看到每个节点只有一条出边，就想到“链表”或“函数图”，直接想到暴力遍历。  
- **最容易踩的坑**  
  1. **环的检测**：直接用 visited 集合会导致对同一环多次遍历，时间会爆炸。需要一次性把所有环找出来（拓扑剪枝或快慢指针）。  
  2. **递归深度**：如果递归实现没有记忆化，树枝上每条路径会重复计算，导致指数级时间。  
  3. **边界情况**：`edges[i] != i` 已经保证没有自环，但仍要处理长度为 2 的环、整张图本身就是一个大环等特殊形态。  
- **下次类似题的第一步**：**检查出度是否唯一**，如果是，就先 **找环**（拓扑剪枝/DFS 标记），再 **用 DP 把环外节点的答案递推**。这样可以把复杂度压到线性。