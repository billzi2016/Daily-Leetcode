# #3558. 分配边权重的方法数 I / Number of Ways to Assign Edge Weights I

> 难度：中等 · 标签：Math、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-i/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 1 to n, rooted at node 1. The tree is represented by a 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates that there is an edge between nodes ui and vi.
Initially, all edges have a weight of 0. You must assign each edge a weight of either 1 or 2.
The cost of a path between any two nodes u and v is the total weight of all edges in the path connecting them.
Select any one node x at the maximum depth. Return the number of ways to assign edge weights in the path from node 1 to x such that its total cost is odd.
Since the answer may be large, return it modulo 109 + 7.
Note: Ignore all edges not in the path from node 1 to x.

**Examples**

**Example 1:**

```
Input: edges = [[1,2]]
Output: 1
Explanation:
```

**Example 2:**

```
Input: edges = [[1,2],[1,3],[3,4],[3,5]]
Output: 2
Explanation:
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i] == [ui, vi]
- 1 <= ui, vi <= n
- edges represents a valid tree.

---

## 题目（中文翻译）

**描述**

给定一棵无向树（undirected tree），包含 n 个节点，编号为 1 到 n，树的根为节点 1（rooted at node 1）。树通过长度为 `n - 1` 的二维整数数组 `edges` 描述，其中 `edges[i] = [u_i, v_i]` 表示节点 `u_i` 与节点 `v_i` 之间存在一条边。

最初，所有边的权重均为 0。你需要为每条边分配权重 `1` 或 `2`。

任意两个节点 `u` 与 `v` 之间的路径费用（cost）定义为该路径上所有边权重之和。

任选一条 **深度最大的** 节点 `x`（即距离根节点 1 最远的节点），统计在从节点 `1` 到节点 `x` 的路径上分配边权重，使得该路径的总费用为 **奇数** 的所有可能分配方式的数量。

由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

> **注意**：路径 `1 → x` 之外的所有边均不计入本题的计算范围。

---

**示例**

**示例 1**

```text
输入: edges = [[1,2]]
输出: 1
解释：
```

**示例 2**

```text
输入: edges = [[1,2],[1,3],[3,4],[3,5]]
输出: 2
解释：
```

---

**约束条件**

- `2 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i] == [u_i, v_i]`
- `1 <= u_i, v_i <= n`
- `edges` 构成一棵有效的树（valid tree）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **先找出**从根节点 `1` 出发，深度最大的那条路径（记为 `path`），路径上的边数记作 `L`（即该最深节点的深度）。  
2. **枚举**这条路径上每一条边的权重（只能是 `1` 或 `2`），一共会产生 `2^L` 种组合。  
3. 对每一种组合，**求和**得到路径的总费用，判断它是奇数还是偶数，若是奇数就计数。  

> **类比**：把路径想象成一串灯泡，每根灯泡的开关只能是 “亮（1）” 或 “暗（2）”。我们要把所有灯泡的亮暗状态全部列举出来，然后数一数哪种情况下亮的灯泡数量是奇数（因为 `2` 对奇偶没有影响）。

- **为什么正确**：我们把所有可能的权重分配都穷举一遍，凡是满足奇数和的情况必然被计数，漏掉的情况不存在。  
- **时间/空间复杂度**：  
  - 时间：要遍历 `2^L` 种可能，每种都要把 `L` 条边相加，时间复杂度是 `O(L·2^L)`。  
  - 空间：只需要保存路径本身和递归的枚举状态，`O(L)`。  

> **大白话**：如果路径有 10 条边，`2^10 = 1024`，算下来还行；但如果有 30 条边，`2^30 ≈ 10^9`，根本跑不完。于是我们必须寻找更快的方法。

#### 代码（Python）

```python
from collections import defaultdict

MOD = 10**9 + 7

def brute_force(edges):
    # 建图（邻接表），因为是树所以每条边只出现一次
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 1. 用 DFS 找到最深的节点以及从根到它的路径
    max_path = []          # 保存最深路径的节点序列
    visited = set()

    def dfs(node, path):
        nonlocal max_path
        visited.add(node)
        path.append(node)
        # 叶子节点：没有未访问的子节点
        if len(g[node]) == 1 and node != 1:   # 只剩父节点，且不是根
            if len(path) > len(max_path):
                max_path = path.copy()
        for nxt in g[node]:
            if nxt not in visited:
                dfs(nxt, path)
        path.pop()

    dfs(1, [])

    L = len(max_path) - 1          # 边数 = 节点数-1
    ans = 0

    # 2. 枚举 2^L 种权重分配
    for mask in range(1 << L):
        total = 0
        for i in range(L):
            # 第 i 条边的权重：位为 0 -> 1，位为 1 -> 2
            w = 1 if ((mask >> i) & 1) == 0 else 2
            total += w
        if total % 2 == 1:         # 奇数
            ans += 1

    return ans % MOD
```

> **注释**  
> - `mask` 的每一位对应路径上第 `i` 条边的取值。  
> - `total % 2 == 1` 判断路径费用是否为奇数。  

#### 复杂度

- **时间复杂度**：`O(L·2^L)`，随着路径长度指数级增长，实际不可用。  
- **空间复杂度**：`O(L)`，仅存储路径和递归栈。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有 `2^L` 种组合**。我们要思考：到底哪些信息真正决定路径费用的奇偶性？

1. **观察权重的奇偶性**  
   - `1` 是奇数，`2` 是偶数。  
   - 偶数加在一起仍是偶数，奇数加在一起的奇偶性只取决于奇数出现的次数的奇偶性。  
   - 换句话说：**路径费用的奇偶性只和「出现了多少个 `1`」有关**，`2` 的个数不影响奇偶性。

2. **把问题转化为组合计数**  
   - 路径长度为 `L`（即 `L` 条边）。我们需要在这 `L` 条边中选择 **奇数个** 放 `1`，其余放 `2`。  
   - 这正是“在 `L` 个位置里挑出奇数个位置”的计数问题。  
   - 已知：在 `L` 个二进制位里，奇数个 `1` 的组合数等于 `2^{L-1}`（因为总组合数 `2^L`，奇偶各占一半）。

3. **如何得到 `L`（最大深度）**  
   - 用一次 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 从根 `1` 开始遍历整棵树，记录每个节点的深度（根的深度为 `0`）。  
   - 取所有深度的最大值 `max_depth`，这正是从根到最深节点的边数 `L`。

4. **答案**  
   - `ans = 2^{max_depth-1} (mod 1e9+7)`。  
   - 当 `max_depth = 1`（只有一条边）时，`2^{0}=1`，唯一的合法方案是把这条边设为 `1`（奇数）。

> **类比**：把路径看成一排灯泡，只关心「亮灯的数量是奇数」而不在乎「暗灯是亮几次」。在 `L` 盏灯中，亮灯的奇偶分布是均匀的，亮灯奇数的情况恰好占一半，即 `2^{L-1}` 种。

#### 代码（Python）

```python
from collections import defaultdict, deque

MOD = 10**9 + 7

def numberOfWays(edges):
    """
    返回从根 (1) 到最深节点的路径上，权重总和为奇数的赋值方案数
    """
    n = len(edges) + 1                # 节点总数
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 1. BFS 求每个节点的深度（根深度为 0）
    depth = [0] * (n + 1)
    visited = [False] * (n + 1)
    q = deque([1])
    visited[1] = True
    max_depth = 0

    while q:
        cur = q.popleft()
        for nxt in g[cur]:
            if not visited[nxt]:
                visited[nxt] = True
                depth[nxt] = depth[cur] + 1
                max_depth = max(max_depth, depth[nxt])
                q.append(nxt)

    # 2. 计算 2^(max_depth-1) % MOD
    # pow(base, exp, mod) 是 Python 内置的快速幂实现，时间 O(log exp)
    if max_depth == 0:                # 理论上不会出现，因为 n >= 2
        return 0
    ans = pow(2, max_depth - 1, MOD)
    return ans
```

> **关键行解释**  
> - `depth[nxt] = depth[cur] + 1`：子节点的深度等于父节点深度加一。  
> - `max_depth = max(max_depth, depth[nxt])`：实时维护当前已遍历节点的最大深度。  
> - `pow(2, max_depth - 1, MOD)`：利用快速幂计算 `2^{max_depth-1}`，时间仅为 `O(log max_depth)`，足够快。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次树（BFS/DFS），每条边访问两次。  
  - 计算幂使用对数时间 `O(log max_depth)`，相对于 `n` 可以忽略不计。  

- **空间复杂度**：`O(n)`  
  - 保存邻接表和深度数组，需要 `n` 的线性空间。  

> 与暴力解相比，时间从指数级降到了线性级，毫不费力就能处理 `10^5` 规模的树。

---

## 心得

- **核心技巧**：奇偶性只与出现奇数次数的元素有关，利用组合数学把「奇数个 1」的计数直接算出来。  
- **适用题型**：  
  1. **路径权重奇偶**（如本题、"Number of Ways to Assign Edge Weights II"）。  
  2. **子集奇偶计数**（如“Count Number of Nice Subarrays” 中的奇数子数组计数）。  
  3. **二进制位奇偶**（如“Number of Subsets With XOR Equal to K” 中的奇数位计数）。  
- **一句话总结**：**奇偶只看奇数出现的次数，奇数次数的组合数等于总组合数的一半**。

---

## 反思

- **第一反应**：直接遍历最深路径，枚举所有 `1/2` 的组合检查奇偶。  
- **最容易踩的坑**：  
  - 忽略了 **“只关心最深路径”**，把整棵树都算进去会导致错误。  
  - 把 `2` 当作会改变奇偶性，导致计数错误。  
  - 边界：当最深深度为 `1` 时，公式 `2^{0}=1` 必须返回 `1`，不能出现 `0`。  
- **下次遇到同类题**：  
  1. 先判断 **“奇偶/模 2”** 是否只受特定元素影响。  
  2. 把 **计数问题转化为组合公式**（如“奇数个/偶数个”），避免枚举。  
  3. 用一次遍历得到所需的 **长度或规模**（如路径长度、子数组长度），再套公式。