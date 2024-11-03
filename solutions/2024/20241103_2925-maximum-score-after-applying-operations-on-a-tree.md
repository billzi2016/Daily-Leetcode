# #2925. **在树上执行操作后的最大分数** / Maximum Score After Applying Operations on a Tree

> 难度：中等 · 标签：Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximum-score-after-applying-operations-on-a-tree/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1, and rooted at node 0. You are given a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
You are also given a 0-indexed integer array values of length n, where values[i] is the value associated with the ith node.
You start with a score of 0. In one operation, you can:
A tree is healthy if the sum of values on the path from the root to any leaf node is different than zero.
Return the maximum score you can obtain after performing these operations on the tree any number of times so that it remains healthy.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[0,2],[0,3],[2,4],[4,5]], values = [5,2,5,2,1,1]
Output: 11
Explanation: We can choose nodes 1, 2, 3, 4, and 5. The value of the root is non-zero. Hence, the sum of values on the path from the root to any leaf is different than zero. Therefore, the tree is healthy and the score is values[1] + values[2] + values[3] + values[4] + values[5] = 11.
It can be shown that 11 is the maximum score obtainable after any number of operations on the tree.
```

**Example 2:**

```
Input: edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [20,10,9,7,4,3,5]
Output: 40
Explanation: We can choose nodes 0, 2, 3, and 4.
- The sum of values on the path from 0 to 4 is equal to 10.
- The sum of values on the path from 0 to 3 is equal to 10.
- The sum of values on the path from 0 to 5 is equal to 3.
- The sum of values on the path from 0 to 6 is equal to 5.
Therefore, the tree is healthy and the score is values[0] + values[2] + values[3] + values[4] = 40.
It can be shown that 40 is the maximum score obtainable after any number of operations on the tree.
```

**Constraints**

- 2 <= n <= 2 * 104
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- values.length == n
- 1 <= values[i] <= 109
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

给定一棵无向树，节点数为 `n`，节点编号为 `0` 到 `n-1`，根节点为 `0`。你会得到一个长度为 `n-1` 的二维整数数组 `edges`，其中 `edges[i] = [ai, bi]` 表示节点 `ai` 与节点 `bi` 之间存在一条边。  
同时给定一个长度为 `n` 的 0 起始整数数组 `values`，其中 `values[i]` 是第 `i` 个节点的值。

你初始得分为 `0`。一次操作可以：

> **树是健康的**：如果从根节点到任意叶子节点的路径上所有节点值之和都不等于 `0`，则该树被称为健康的。

返回在对树执行任意次数的上述操作后，使树保持健康的情况下，你能够获得的最大得分。

---

### 示例

#### 示例 1
```text
Input: edges = [[0,1],[0,2],[0,3],[2,4],[4,5]], values = [5,2,5,2,1,1]
Output: 11
Explanation: 我们可以选择节点 1、2、3、4、5。根节点的值非零。因此，从根节点到任意叶子节点的路径和值都不等于零，树是健康的。得分为 values[1] + values[2] + values[3] + values[4] + values[5] = 11。
可以证明 11 是最大可能得分。
```

#### 示例 2
```text
Input: edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [20,10,9,7,4,3,5]
Output: 40
Explanation: 我们可以选择节点 0、2、3、4。
- 从 0 到 4 的路径和值为 10。
- 从 0 到 3 的路径和值为 10。
- 从 0 到 5 的路径和值为 3。
- 从 0 到 6 的路径和值为 5。
因此，树保持健康，得分为 20 + 9 + 7 + 4 = 40（示例截断）。
```

---

### 约束

- `2 <= n <= 2 * 10^4`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= ai, bi < n`
- `values.length == n`
- `1 <= values[i] <= 10^9`
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把**每一个可能的节点集合**都枚举一遍，检查它是否满足“健康”条件（即从根到任意叶子的选中节点值之和不为 0），再把所有满足条件的集合的价值求和，取最大值。  

- **枚举集合**：可以把每个节点看成一个开关，`0` 表示不选，`1` 表示选。所有开关的排列组合就是 `2ⁿ` 种可能。  
- **检查健康**：对每条根到叶子的路径，累加被选中的节点的 `values`，只要有一条路径的和恰好等于 0，就把这个集合判为不健康。  
- **记录最大分数**：对所有健康的集合，计算选中节点的总和，取最大的那个。  

> **类比**：这就像在超市里把所有商品的买/不买组合全部尝试一遍，看看哪种组合既满足“不能买到价值为 0 的套餐”，又能让总花费最高——显然不切实际。

这个方法之所以**正确**，是因为我们穷举了所有可能的答案，必然能找到最优解。但显然**时间会爆炸**，即使 `n = 20`，`2ⁿ` 也已经是 1 048 576 种组合，远远超过题目允许的 `n ≤ 2·10⁴`。

#### 代码（Python）

```python
from itertools import product
from collections import defaultdict

def brute_force(edges, values):
    n = len(values)
    # 建图（只为了找根到叶子的所有路径）
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 先得到所有根到叶子的路径（DFS）
    paths = []
    def dfs(u, parent, cur_path):
        cur_path.append(u)
        if len(g[u]) == 1 and u != 0:          # 叶子（根的度为1时不算叶子）
            paths.append(list(cur_path))
        else:
            for v in g[u]:
                if v != parent:
                    dfs(v, u, cur_path)
        cur_path.pop()
    dfs(0, -1, [])

    best = 0
    # 枚举 0/1 选取方案，product 会产生 2^n 种元组
    for mask in product([0, 1], repeat=n):
        # 检查每条根到叶子的路径和是否为 0
        healthy = True
        for p in paths:
            s = sum(values[node] for node, take in zip(p, mask) if take)
            if s == 0:
                healthy = False
                break
        if healthy:
            best = max(best, sum(v for v, take in zip(values, mask) if take))
    return best
```

> **注意**：上述代码只能在极小规模（如 `n ≤ 10`）下跑通，主要用于说明“暴力思路”。  

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n)`  
  - `2ⁿ` 是所有可能的选取组合数量。  
  - 对每个组合我们要遍历所有根到叶子的路径，最坏情况下每条路径长度是 `O(n)`。  
  - 用大白话说，就是“每多一个节点，可能的组合就会翻倍”，所以根本跑不完。  
- **空间复杂度**：`O(n)`  
  - 递归栈、图的邻接表以及路径列表都需要线性空间。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**枚举所有子集是不可取的**。我们需要利用树的结构，把问题拆成子树之间的独立子问题。  

关键观察：  

1. **根到叶子的路径只受到沿途节点是否被选的影响**，而子树之间互不干扰——只要每条路径的和不为 0，整个树就健康。  
2. 对于某个节点 `x`，我们有两种“决策”  
   - **不选 `x`**：如果 `x` 不计入分数，那么它下面的每棵子树可以**全部选**（因为根到叶子的路径已经不经过 `x`，只剩子树内部的路径）。这时我们能得到的分数就是所有子树的**总和** `sum[child]`。  
   - **选 `x`**：如果把 `x` 的价值计入分数，那么从根到叶子的每条路径都会经过 `x`，因此子树必须保持“健康”。这时子树只能贡献它们**在保持健康前提下的最大分数**，记作 `dp[child]`。  

于是我们可以用**动态规划**在树上自底向上计算两个数组：  

- `sum[u]`：以 `u` 为根的整棵子树所有节点价值的总和（不管健康与否）。递推式  
  ```text
  sum[u] = values[u] + Σ sum[v]   （v 为 u 的所有子节点）
  ```  
- `dp[u]`：在**保证子树健康**的前提下，以 `u` 为根能够得到的**最大分数**。递推式来源于上面的两种决策  
  ```text
  dp[u] = max( values[u] + Σ dp[v] ,   Σ sum[v] )
  ```  
  - 第一个选项：选 `u`，加上每个子树在健康约束下的最佳得分 `dp[v]`。  
  - 第二个选项：不选 `u`，直接把子树全部拿下，得分是子树的总价值 `sum[v]` 的和。  

**根节点** `0` 的 `dp[0]` 就是答案，因为它已经把整棵树的健康约束考虑进来了。  

#### 为什么是最优的？  

- **局部最优等于全局最优**：对每个子树，`dp` 只在“已知子树内部必须健康”的前提下求最大分数。因为子树之间只有通过父节点这条唯一通路相连，父节点的选与不选已经决定了子树是否需要继续保持健康。  
- **不遗漏任何可能**：两种决策覆盖了所有合法的选择（要么选当前节点，要么不选），而每种决策内部又递归地使用了子树的最优解。  

#### 实现细节  

1. **把无向边转成有根树**：从根 `0` 做一次 DFS，记录父子关系，避免回到父节点。  
2. **后序遍历（子树先算）**：在递归返回时计算 `sum[u]` 与 `dp[u]`。  
3. **防止递归深度爆栈**：`n ≤ 2·10⁴`，Python 默认递归深度 ~ 1000，不够。可以使用 `sys.setrecursionlimit(1<<25)` 或改写为显式栈的迭代 DFS。这里使用递归并手动调大递归上限。  

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(1 << 25)          # 把递归深度上限调高，防止栈溢出

from collections import defaultdict
from typing import List

def maximumScore(edges: List[List[int]], values: List[int]) -> int:
    n = len(values)
    # 1️⃣ 建图（邻接表）
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 2️⃣ 用 DFS 把树变成“有根”结构，同时在后序遍历时计算 sum 与 dp
    sum_sub = [0] * n          # sum_sub[u] = 整个子树的价值总和
    dp = [0] * n               # dp[u] = 在子树健康前提下的最大得分

    def dfs(u: int, parent: int) -> None:
        """后序遍历，先处理所有子节点，再回到 u 计算自己的值"""
        total_sum_children = 0   # Σ sum[child]
        total_dp_children = 0    # Σ dp[child]

        for v in g[u]:
            if v == parent:      # 不回到父亲，防止无限循环
                continue
            dfs(v, u)            # 递归处理子树
            total_sum_children += sum_sub[v]
            total_dp_children += dp[v]

        # ① 计算以 u 为根的子树总价值
        sum_sub[u] = values[u] + total_sum_children

        # ② 计算 dp[u]（两种决策取最大）
        take_u = values[u] + total_dp_children          # 选 u
        not_take_u = total_sum_children                  # 不选 u
        dp[u] = max(take_u, not_take_u)

    dfs(0, -1)                 # 从根 0 开始，-1 表示“没有父节点”

    return dp[0]               # 根的 dp 就是整棵树的最大健康得分
```

**代码要点注释**  

- `sum_sub[u] = values[u] + Σ sum_sub[child]` —— 把子树的总价值往上累。  
- `take_u = values[u] + Σ dp[child]` —— 选当前节点，子树只能贡献已经“健康”的最佳得分。  
- `not_take_u = Σ sum_sub[child]` —— 不选当前节点，子树可以全部拿下，因为根到叶的路径已经不经过 `u`。  
- `dp[u] = max(take_u, not_take_u)` —— 在两种合法方案中挑最大的。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每条边只会在 DFS 中被访问两次（一次进入子节点，一次回到父节点），所以整体是线性时间。  
  - 用大白话说，就是“处理一个节点只需要常数时间”，不管树有多大，都能在几秒钟内跑完。  

- **空间复杂度**：`O(n)`  
  - 邻接表、`sum_sub`、`dp` 各占 `n` 大小的数组，递归栈最深为树的高度，最坏情况下（链状树）也不超过 `n`。  

---

## 心得  

- **核心技巧**：**树形动态规划**（自底向上 DP） + **两种决策的取最大**。  
- **适用的题型**：  
  1. “在树上选点使某种约束成立，求最大/最小权值和”。如 LeetCode 337 *House Robber III*（抢劫二叉树）。  
  2. “在树上删除/保留节点，使每条根到叶的属性满足要求”，比如 “Maximum Product of Splitted Binary Tree”。  
- **一句话总结**：**把每棵子树的“全部拿下”和“在健康约束下的最佳”这两种选择列出来，递归取最大，就是答案。**  

---

## 反思  

- **第一反应**：看到“根到叶路径的和不能为 0”，立刻想到要**枚举所有路径**或**暴力搜索**，但很快意识到树的规模太大，必须用 **DP**。  
- **最容易踩的坑**：  
  - **递归深度**：链状树会导致递归层数达到 `n`，若不调大 `sys.setrecursionlimit` 会出现 `RecursionError`。  
  - **根节点的特殊处理**：根没有父节点，判断叶子时要排除根的度为 1 的情况。  
  - **整数溢出**：`values[i] ≤ 10⁹，n ≤ 2·10⁴`，总和可能达到 `2·10¹³`，在 Python 中无需担心，但在某些语言要使用 64 位整数。  
- **下次思路**：面对“树上选点并满足路径约束”这类问题，第一步就**把问题拆成子树的 DP**，明确“选父节点”和“不选父节点”两种状态，再写出递推式。这样可以直接跳到最优解的雏形，避免在暴力搜索上浪费时间。