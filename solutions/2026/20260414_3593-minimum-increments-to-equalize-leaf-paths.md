# #3593. 最小增量使叶子路径得分相等 / Minimum Increments to Equalize Leaf Paths

> 难度：中等 · 标签：Array、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-increments-to-equalize-leaf-paths/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an undirected tree rooted at node 0 with n nodes numbered from 0 to n - 1. This is represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi] indicates an edge from node ui to vi .
Each node i has an associated cost given by cost[i], representing the cost to traverse that node.
The score of a path is defined as the sum of the costs of all nodes along the path.
Your goal is to make the scores of all root-to-leaf paths equal by increasing the cost of any number of nodes by any non-negative amount.
Return the minimum number of nodes whose cost must be increased to make all root-to-leaf path scores equal.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1],[0,2]], cost = [2,1,3]
Output: 1
Explanation:

There are two root-to-leaf paths:
To make all root-to-leaf path scores equal to 5, increase the cost of node 1 by 2. Only one node is increased, so the output is 1.
```

**Example 2:**

```
Input: n = 3, edges = [[0,1],[1,2]], cost = [5,1,4]
Output: 0
Explanation:

There is only one root-to-leaf path:
Path 0 → 1 → 2 has a score of 5 + 1 + 4 = 10 .
Since only one root-to-leaf path exists, all path costs are trivially equal, and the output is 0.
```

**Example 3:**

```
Input: n = 5, edges = [[0,4],[0,1],[1,2],[1,3]], cost = [3,4,1,1,7]
Output: 1
Explanation:

There are three root-to-leaf paths:
To make all root-to-leaf path scores equal to 10, increase the cost of node 1 by 2. Thus, the output is 1.
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i] == [ui, vi]
- 0 <= ui, vi < n
- cost.length == n
- 1 <= cost[i] <= 109
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

你得到一个整数 `n`，以及一棵以节点 `0` 为根的无向树，树中共有 `n` 个节点，编号为 `0` 到 `n - 1`。树由长度为 `n - 1` 的二维数组 `edges` 表示，其中 `edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间有一条边。

每个节点 `i` 关联一个费用 `cost[i]`，表示经过该节点的费用。

一条路径的得分（score）定义为路径上所有节点费用的总和。

你的目标是通过**增加**任意数量节点的费用（可以增加任意非负整数），使所有从根到叶子（leaf）的路径的得分相等。返回必须增加费用的最小节点数量。

**示例 1：**  
**输入：** `n = 3, edges = [[0,1],[0,2]], cost = [2,1,3]`  
**输出：** `1`  
**解释：**  
存在两条根到叶子的路径。若将所有路径的得分统一为 `5`，只需将节点 `1` 的费用增加 `2`。只增加了一个节点的费用，因此答案为 `1`。

**示例 2：**  
**输入：** `n = 3, edges = [[0,1],[1,2]], cost = [5,1,4]`  
**输出：** `0`  
**解释：**  
仅有一条根到叶子的路径：`0 → 1 → 2`，其得分为 `5 + 1 + 4 = 10`。因为只有一条路径，所有路径得分天然相等，故答案为 `0`。

**示例 3：**  
**输入：** `n = 5, edges = [[0,4],[0,1],[1,2],[1,3]], cost = [3,4,1,1,7]`  
**输出：** `1`  
**解释：**  
共有三条根到叶子的路径。若将所有路径的得分统一为 `10`，只需将节点 `1` 的费用增加 `2`。因此答案为 `1`。

**约束条件：**  
- `2 <= n <= 10^5`  
- `edges.length == n - 1`  
- `edges[i] == [ui, vi]`  
- `0 <= ui, vi < n`  
- `cost.length == n`  
- `1 <= cost[i] <= 10^9`  
- 输入保证 `edges` 构成一棵合法的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一条根到叶子的路径都算出它的总分**，记为 `pathSum`。  
找出所有路径中最大的总分 `maxLeafCost`，然后把每条路径的分数都提升到这个最大值。  

提升的方式很自由：可以给路径上任意节点加任意非负的数，只要最终每条路径的和相等即可。  
于是我们可以**逐条路径**地检查：  

1. 计算该路径与 `maxLeafCost` 的差值 `delta = maxLeafCost - pathSum`。  
2. 为了弥补这个差值，随便挑选路径上的几个节点，把它们的成本分别加上一点，累计起来恰好等于 `delta`。  
3. 只要 **只要有一个节点被加过**，这条路径就算“被修改”。  

遍历完所有路径，统计被修改的 **不同节点** 数目，就是答案。

> **类比**：把每条路径想象成一根绳子，绳子的长度就是路径分数。我们想让所有绳子拉到同样的最长长度，只能在绳子上“加厚”若干段（即增节点成本），只要加厚的段数>0，这根绳子就算被动手过。

**为什么能得到正确答案**  
因为我们没有任何约束只能在某些节点上增值——只要把每条路径的缺口 `delta` 用路径上任意节点填满，所有路径最终都会等于 `maxLeafCost`。只要统计的节点集合包含了每条路径上至少一个被加值的节点，就满足题目要求。

**复杂度分析**  
- 需要遍历 **每一条根到叶子的路径**，在最坏情况下（比如一棵链），路径数等于 `n`，每条路径长度也是 `O(n)`，于是总时间是 `O(n²)`。  
- 只用了几个数组来记录路径和、最大值等，空间是 `O(n)`（存图结构）。

> **大白话**：`O(n²)` 就像你让 10 000 个人每人排队 10 000 次——显然会超时。

#### 代码（Python）

```python
# 暴力解：遍历所有根到叶子的路径，统计需要被修改的节点数
from collections import defaultdict, deque

def minIncrements_bruteforce(n, edges, cost):
    # 建图（邻接表）
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 记录所有根到叶子的路径以及路径和
    leaf_sums = []          # 每条路径的总分
    leaf_paths = []         # 每条路径对应的节点列表（用于后面统计修改的节点）

    # BFS/DFS 求每条路径
    stack = [(0, -1, 0, [0])]          # (当前节点, 父节点, 累计和, 当前路径)
    while stack:
        node, parent, cur_sum, path = stack.pop()
        cur_sum += cost[node]
        children = [nbr for nbr in g[node] if nbr != parent]

        # 叶子：没有子节点（根节点的特殊情况除外）
        if not children:
            leaf_sums.append(cur_sum)
            leaf_paths.append(list(path))
        else:
            for nxt in children:
                stack.append((nxt, node, cur_sum, path + [nxt]))

    max_leaf = max(leaf_sums)               # 目标统一的最大路径分数
    changed_nodes = set()                   # 记录被增值的节点

    # 对每条路径，随便把差值加到路径上的第一个节点（只要加就行）
    for path_sum, nodes in zip(leaf_sums, leaf_paths):
        delta = max_leaf - path_sum
        if delta > 0:                       # 需要增值
            # 随便把增值放在路径的第一个节点上
            changed_nodes.add(nodes[0])

    return len(changed_nodes)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：在最坏情况下（比如链式树），我们会遍历 `n` 条路径，每条路径长度也接近 `n`，所以总操作次数大约是 `n × n`。
- **空间复杂度**：`O(n)`  
  解释：主要是存图的邻接表和递归/栈用到的路径列表，和节点数量成线性关系。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**一次遍历了一整条路径**，而实际上我们只关心每条路径需要“补齐”的**缺口**（即 `maxLeafCost - pathSum`），并且同一条路径上所有节点共享这个缺口——如果我们在路径上的**某个公共节点**一次性把缺口全部加上，下面所有子路径的缺口都会被一起解决。

**关键观察**  

1. 设 `leafSum[u]` 为根到节点 `u` 的累计成本（包括 `u` 本身）。  
2. 所有根到叶子的路径中，最大的累计成本记为 `M`（即 `maxLeafCost`）。  
3. 对于每个叶子 `v`，它缺少的分数是 `need[v] = M - leafSum[v]`。  
4. 对于内部节点 `u`，它的所有子树里会出现若干 `need[leaf]`。  
   - 如果我们在 `u` 上增加 `x`，**所有经过 `u` 的路径**的累计成本都会多 `x`，于是它们的缺口都会同时减小 `x`。  
   - 为了让所有子树的缺口最终都为 `0`，我们只需要把 `u` 增加到 **子树中最大的缺口**。也就是说  
     
     ```
     need[u] = max( need[child] )   （后序遍历得到）
     ```

   - 只要 `need[u]` 大于父节点的 `need[parent]`，我们就必须在 `u` 上再增加 `need[u] - need[parent]`，这意味着 **节点 u 必须被计入答案**。  
5. 因此，**需要增加成本的节点恰好是**“`need` 值在树上出现变化的节点”。根的父亲我们假设 `need = 0`。

**算法步骤**  

1. **建树**：用邻接表保存无向树，随后在 DFS 时避免回到父节点。  
2. **一次 DFS 计算 `leafSum`**（从根出发的累计成本）并记录所有叶子的 `need = M - leafSum`。在遍历完所有叶子后得到 `M`（最大叶子累计成本）。  
3. **第二次后序 DFS**（从叶子向上）计算每个节点的 `need[u] = max( need[child] )`。在回溯时把 `need` 传给父节点。  
4. **统计答案**：在后序遍历时，若 `need[u] != need[parent]`（根的父亲的 `need` 设为 `0`），则答案 `ans += 1`。  
5. 返回 `ans`。

> **类比**：想象每条根到叶子的路径是一条水管，`leafSum` 是水管里已经有的水量，`M` 是最高的水位。每根管子还缺的水量就是 `need`。我们可以在管道的交叉点（树的内部节点）加水，一次加的水会同时流向所有下游的管子。于是我们只在“最需要加水的交叉点”下水，次数最少就等于这些交叉点的数量。

**复杂度分析**  

- 两次深度优先遍历，每次遍历每条边一次，时间 `O(n)`。  
- 需要保存邻接表、累计和、`need` 三个长度为 `n` 的数组，空间 `O(n)`。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(2 * 10**5)

def minIncrements(n: int, edges, cost):
    """
    返回最少需要增值的节点数，使所有根到叶子的路径分数相等
    """
    # 1. 建图（邻接表）
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 2. 第一次 DFS：计算从根到每个节点的累计成本 leafSum
    leaf_sum = [0] * n          # leaf_sum[u] = sum(cost) from root to u (inclusive)
    parent = [-1] * n           # 记录父节点，方便后序遍历时判断子节点
    leaves = []                 # 记录所有叶子节点

    def dfs_sum(u, p):
        """前序遍历，填充 leaf_sum、parent，并收集叶子"""
        parent[u] = p
        # 累计成本已经在 leaf_sum[u] 中（父节点已经算好）
        leaf_sum[u] += cost[u]
        children = [v for v in g[u] if v != p]
        if not children:                # 没有子节点 → 叶子
            leaves.append(u)
        for v in children:
            leaf_sum[v] = leaf_sum[u]   # 继承累计成本
            dfs_sum(v, u)

    dfs_sum(0, -1)

    # 3. 求出所有根到叶子的最大累计成本 M
    max_leaf = max(leaf_sum[v] for v in leaves)

    # 4. 为每个叶子计算缺口 need[leaf] = M - leaf_sum[leaf]
    need = [0] * n               # need[u] = 子树中最大的缺口
    for leaf in leaves:
        need[leaf] = max_leaf - leaf_sum[leaf]

    # 5. 第二次后序 DFS：自底向上汇总 need，并统计答案
    ans = 0

    def dfs_need(u):
        """后序遍历，返回子树中最大的 need 值，同时统计答案"""
        nonlocal ans
        max_child_need = 0
        for v in g[u]:
            if v == parent[u]:
                continue
            child_need = dfs_need(v)          # 子树的最大缺口
            max_child_need = max(max_child_need, child_need)

        # 当前节点的 need 是子树中最大的 need
        cur_need = max(need[u], max_child_need)

        # 与父节点的 need 比较，若不同则需要在此节点增值
        # 对根节点而言，父 need 视为 0（因为根没有父亲）
        parent_need = need[parent[u]] if parent[u] != -1 else 0
        if cur_need != parent_need:
            ans += 1

        # 将当前节点的 need 记录回数组，供父节点使用
        need[u] = cur_need
        return cur_need

    dfs_need(0)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：两次 DFS 每条边只访问常数次，和节点数成线性关系。相比暴力的 `O(n²)`，大幅提升，能够轻松处理 `n = 10⁵` 的规模。
- **空间复杂度**：`O(n)`  
  解释：邻接表、`leaf_sum`、`need`、`parent` 等数组均为 `n` 长度，递归栈最深也不超过 `n`。

---

## 心得

- **核心技巧**：在树上**自底向上**计算“子树中最大的缺口”，并利用**缺口变化点即为必须增值的节点**。这是一种典型的“后序 DP + 计数变化”的思路。  
- **适用题型**  
  1. **使所有根到叶子路径满足同一约束**（如路径长度、路径权值相等）——如本题、`Maximum Difference Between Node and Ancestor` 的变形。  
  2. **树形 DP 统计需要“操作”的节点**——如 `Minimum Number of Operations to Make Tree Balanced`、`Tree Pruning` 等。  
- **一句话总结解题钥匙**：**把每条路径的缺口向上“汇聚”，只在缺口值改变的节点动手，节点数最少。**

## 反思

- **第一反应**：直接枚举所有根到叶子的路径，逐条补齐。  
- **最容易踩的坑**  
  - 忘记把根节点也算进可能的增值节点（根的父节点 `need` 视为 `0`）。  
  - 对于只有一条根到叶子路径的树，答案应该是 `0`，而不是误认为需要修改根。  
  - 递归深度可能超过 Python 默认递归限制，需要 `sys.setrecursionlimit` 或改用显式栈。  
- **下次类似题的第一步**：先**算出每条根到叶子路径的目标值（最大/最小）**，然后**自底向上求每个子树的“最大缺口/最小剩余”，用变化点计数**。这样可以避免暴力遍历每条路径，直接得到线性时间解。