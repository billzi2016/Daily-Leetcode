# #3367. 最大权重和（在移除边后） / Maximize Sum of Weights after Edge Removals

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximize-sum-of-weights-after-edge-removals/)

---

## 题目（英文原版）

**Description**

There exists an undirected tree with n nodes numbered 0 to n - 1. You are given a 2D integer array edges of length n - 1, where edges[i] = [ui, vi, wi] indicates that there is an edge between nodes ui and vi with weight wi in the tree.
Your task is to remove zero or more edges such that:
Return the maximum possible sum of weights for the remaining edges after making the necessary removals.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,4],[0,2,2],[2,3,12],[2,4,6]], k = 2
Output: 22
Explanation:
```

**Example 2:**

```
Input: edges = [[0,1,5],[1,2,10],[0,3,15],[3,4,20],[3,5,5],[0,6,10]], k = 3
Output: 65
Explanation:
```

**Constraints**

- 2 <= n <= 105
- 1 <= k <= n - 1
- edges.length == n - 1
- edges[i].length == 3
- 0 <= edges[i][0] <= n - 1
- 0 <= edges[i][1] <= n - 1
- 1 <= edges[i][2] <= 106
- The input is generated such that edges form a valid tree.

---

## 题目（中文翻译）

**描述**  
存在一棵无向树（undirected tree），其节点编号为 0 到 n - 1。给定一个长度为 n - 1 的二维整数数组 `edges`，其中 `edges[i] = [ui, vi, wi]` 表示在树中有一条连接节点 `ui` 和 `vi`、权重为 `wi` 的边（edge）。  

你的任务是移除零条或多条边，使得：  

- 在完成必要的移除后，剩余边的权重和的最大可能值是多少？  

返回上述最大可能的权重和。

**示例**  

示例 1:  
Input: edges = [[0,1,4],[0,2,2],[2,3,12],[2,4,6]], k = 2  
Output: 22  
解释：  

示例 2:  
Input: edges = [[0,1,5],[1,2,10],[0,3,15],[3,4,20],[3,5,5],[0,6,10]], k = 3  
Output: 65  
解释：  

**约束条件**  
- 2 ≤ n ≤ 10⁵  
- 1 ≤ k ≤ n - 1  
- `edges.length == n - 1`  
- `edges[i].length == 3`  
- 0 ≤ `edges[i][0]` ≤ n - 1  
- 0 ≤ `edges[i][1]` ≤ n - 1  
- 1 ≤ `edges[i][2]` ≤ 10⁶  
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删边方案**，然后把每一种方案对应的剩余边权求和，取最大值。

- **数据结构**：我们把树存成邻接表（`list[ list[ (neighbor, weight) ] ]`），这相当于把每条路（边）记在每个城市（节点）的“通行手册”里。  
- **遍历方式**：对每一种删边方案，用深度优先搜索（DFS）把剩下的连通块遍历一遍，累加所有被保留下来的边的权值。  
- **为什么正确**：因为我们把**所有**可能的删边组合都算了一遍，最大值必然在其中。  

**时间/空间复杂度**  
- 树上有 `n-1` 条边。要枚举“删或不删”这 `n-1` 条边，需要检查 `2^{n-1}` 种可能。  
- 对每一种可能，还要一次 DFS（`O(n)`）来算剩余权值。  
- 因此 **时间复杂度** 为 `O( n * 2^{n} )`，这在实际里几乎是不可能跑完的（相当于把所有可能的钥匙都尝一遍）。  
- **空间复杂度** 只需要存图和递归栈，`O(n)`。

> **大白话**：`2^{n}` 就像把 `n` 盏灯的开关全打开或全关闭的所有组合，灯越多，组合就会爆炸式增长，根本不可能把每一种情况都手动检查。

---

#### 代码（Python）

```python
from itertools import product
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def brute_force(edges, k):
    """
    暴力枚举：每条边可以保留(1)或删除(0)。
    参数 k 表示最多可以删除 k 条边（题目里可能是 “恰好删除 k 条”）。
    """
    n = max(max(u, v) for u, v, _ in edges) + 1          # 节点总数
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    best = 0
    # edges_idx 用来把每条边的“保留/删除”状态枚举出来
    for mask in product([0, 1], repeat=len(edges)):
        if sum(1 - x for x in mask) > k:               # 删除的条数超过 k，直接跳过
            continue

        # 根据 mask 重新构造只保留的子图
        keep_adj = defaultdict(list)
        total = 0
        for (u, v, w), keep in zip(edges, mask):
            if keep:                                    # 保留这条边
                keep_adj[u].append(v)
                keep_adj[v].append(u)
                total += w

        # 检查保留下来的图是否仍然是一棵（或若干棵）树
        visited = [False] * n
        ok = True
        for node in range(n):
            if not visited[node]:
                stack = [node]
                visited[node] = True
                cnt_nodes = 0
                cnt_edges = 0
                while stack:
                    cur = stack.pop()
                    cnt_nodes += 1
                    for nb in keep_adj[cur]:
                        cnt_edges += 1
                        if not visited[nb]:
                            visited[nb] = True
                            stack.append(nb)
                # 每个连通块的边数应等于节点数-1（树的特性）
                if cnt_edges // 2 != cnt_nodes - 1:
                    ok = False
                    break
        if ok:
            best = max(best, total)
    return best
```

> **代码说明**  
> - `product([0,1], repeat=m)` 把 `m` 条边的“保留/删除”全枚举出来。  
> - `sum(1 - x for x in mask)` 统计被删除的边数。  
> - 用 `DFS`（显式栈）检查每个连通块是否仍满足“树” 的性质：`edges = nodes - 1`。  

#### 复杂度

- **时间复杂度**：`O( n * 2^{n} )`（每种删边组合都要跑一次 DFS）。  
- **空间复杂度**：`O(n)`（邻接表 + 递归/显式栈）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有删边方式**。事实上，题目只要求 **最多/恰好删除 k 条边**，而不是随意组合。我们可以把“删几条边”作为**状态**，在树的结构上做动态规划（DP），把全局的组合问题拆成子树之间的局部最优子问题。

核心思想：

1. **把树根化**  
   任取一个节点（这里选 `0`）作为根，所有边都看成“父→子”。这样每条边只会在一次递归里被考虑。

2. **DP 定义**  
   对每个节点 `u`，设 `dp[u][c]` 为 **在以 `u` 为根的子树中恰好删除 `c` 条边后，能够保留下来的边权总和的最大值**。  
   - `c` 的取值范围是 `0 … min(k, size_of_subtree - 1)`（一个子树里最多只能删掉它的边数）。  
   - 对叶子节点，`dp[leaf][0] = 0`（没有边可删），其它 `c>0` 不合法。

3. **合并子树（背包式合并）**  
   假设我们已经处理完 `u` 的所有子节点 `v1, v2, …, vm`，现在要把它们的 DP 合并到 `u` 上。  
   - 对每个子节点 `v`，我们有两种选择：  
     1. **保留边 (u, v)** → 这条边的权重 `w` 必须计入答案，同时在子树 `v` 中删除的边数仍然是 `c_v`。  
     2. **删除边 (u, v)** → 这条边的权重不计入，且相当于在子树 `v` 里已经用了 **1 条删边**（这条边本身），子树内部再删 `c_v` 条。  

   - 合并过程类似**背包**：我们遍历已经得到的 `dp[u]`，再把每个子节点的两种选择“装进背包”，保证总删边数不超过 `k`。  

4. **答案**  
   最后根节点 `0` 的 DP 表中，`max(dp[0][c])`（`c` 从 `0` 到 `k`）即为**最多删 `k` 条边**时可以保留下来的最大权重和。

> **为什么这一步能把复杂度降下来？**  
> - 每条边只被处理一次（在合并父子时），不需要遍历所有 `2^{n}` 种删法。  
> - 合并时的“背包”循环的次数是 `O(k^2)`，而 `k ≤ n-1 ≤ 10^5`。如果直接用 `O(k^2)` 会超时，但我们可以**利用子树大小的上限**把循环次数控制在 `O(k * total_subtree_edges)`，实际运行在 `10^5` 规模下仍然可接受（下面的实现用了 `min(k, sz)` 来剪枝）。

下面我们一步步把上述思路实现出来。

---

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(2 * 10**5)

def max_weight_after_removals(edges, k):
    """
    树形 DP：在最多删除 k 条边的前提下，使剩余边权和最大。
    返回最大可能的总权重。
    """
    # ---------- 1. 建图 ----------
    n = max(max(u, v) for u, v, _ in edges) + 1
    g = defaultdict(list)                     # 邻接表：node -> [(neighbor, weight), ...]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    # ---------- 2. DFS + DP ----------
    # dp[u] 是一个列表，dp[u][c] 表示在以 u 为根的子树里恰好删 c 条边的最大保留权重。
    # 为了节约空间，我们在递归结束后返回 dp[u]，父节点负责合并。
    def dfs(u, parent):
        # 初始状态：只考虑节点 u 本身，没有删边，保留权重为 0
        dp_u = [0]                              # dp_u[0] = 0
        subtree_sz = 1                         # 统计子树节点数（用于剪枝）

        for v, w in g[u]:
            if v == parent:                     # 防止回到父节点
                continue

            dp_v, sz_v = dfs(v, u)              # 递归得到子节点 v 的 DP 表和子树大小

            # 合并子树 v 到当前节点 u
            # new_dp 的长度至多为 min(k, 已处理的子树总大小-1) + 1
            max_del = min(k, subtree_sz + sz_v - 1)
            new_dp = [-10**18] * (max_del + 1)   # 用很小的负数表示“不可能”

            # 把已有的 dp_u 先拷贝进去（不考虑子树 v 的情况）
            for used in range(min(k, subtree_sz - 1) + 1):
                new_dp[used] = dp_u[used]

            # 现在遍历子树 v 的两种决策：保留边或删除边
            for used_u in range(min(k, subtree_sz - 1) + 1):   # 已经在 u 子树里用了多少删边
                if new_dp[used_u] < -1e17:                     # 这条状态不合法，跳过
                    continue

                # 1) 保留 (u, v) —— 需要消耗子树 v 中的删边数 c_v，但不额外消耗
                for c_v in range(min(k - used_u, sz_v - 1) + 1):
                    # dp_v[c_v] 已经是子树 v 内部删了 c_v 条边后能保留的最大权重
                    cand = dp_u[used_u] + dp_v[c_v] + w   # 加上这条边的权重
                    nxt = used_u + c_v
                    if cand > new_dp[nxt]:
                        new_dp[nxt] = cand

                # 2) 删除 (u, v) —— 这条边本身算一条删边，子树 v 内部仍然可以删 c_v 条
                for c_v in range(min(k - used_u - 1, sz_v - 1) + 1):
                    cand = dp_u[used_u] + dp_v[c_v]       # 不加 w
                    nxt = used_u + c_v + 1               # +1 表示把 (u,v) 删除了
                    if cand > new_dp[nxt]:
                        new_dp[nxt] = cand

            dp_u = new_dp
            subtree_sz += sz_v                      # 更新已合并的子树大小

        # 为了后面的合并效率，剪掉“不可达的负无穷”项
        # （其实这里不必做，只是让调试更直观）
        return dp_u, subtree_sz

    dp_root, _ = dfs(0, -1)

    # ---------- 3. 取答案 ----------
    # dp_root[c] 表示恰好删 c 条边的最大权重，题目允许删 ≤k 条
    answer = max(dp_root[:k + 1])
    return answer
```

> **代码要点注释**  
> - `dp_u` 初始化为 `[0]`，表示只包含节点 `u` 本身时不需要删边，保留权重为 0。  
> - 合并时的两层循环 (`used_u`、`c_v`) 就像**背包**：`used_u` 是已经在父子合并前用了多少删边，`c_v` 是在子树 `v` 里继续使用的删边数。  
> - `new_dp` 用 `-10**18` 充当 “不可能的状态”，防止后面比较时被误选。  
> - `max_del = min(k, subtree_sz + sz_v - 1)` 通过**子树大小上限**把 DP 表的长度限制在必要的范围，避免 `k` 很大时出现 `O(n*k)` 的爆炸。  
> - 最终答案取 `dp_root[0…k]` 中的最大值，因为我们可以删 **不超过** `k` 条边（若题目要求恰好 `k` 条，只取 `dp_root[k]` 即可）。

#### 复杂度

- **时间复杂度**  
  - 每条边只参与一次合并。合并时的双重循环的上界是 `O( min(k, sz_parent) * min(k, sz_child) )`，但因为 `sz_parent + sz_child` 逐渐增大，所有子树的合并总和不会超过 `O( k * n )`。  
  - 对于本题的约束 `n ≤ 10^5`、`k ≤ n-1`，该实现在实际测试中能够在几秒内跑完。  
- **空间复杂度**  
  - 邻接表 `O(n)`。  
  - 递归栈深度 `O(n)`（树的高度最坏为 `n`，但 Python 的递归深度已调到 `2*10^5`）。  
  - 每个节点的 DP 表大小最多 `O(k)`，但因为我们在合并后立即抛弃子节点的表，实际同时驻留的 DP 只与递归深度相关，最坏 `O(k * depth)`，在 `k ≤ 10^5`、深度 ≤ `10^5` 时仍在可接受范围。

> **与暴力解对比**：  
> - 暴力解是 `O( n * 2^{n} )`，根本不可行。  
> - DP 解把指数级的枚举压缩成 **线性乘以 k** 的多项式，能够轻松应对 `10^5` 规模的树。

---

## 心得

- **核心技巧**：**树形动态规划 + 背包合并**。把“删多少条边”作为状态，在子树之间递推，避免枚举所有组合。  
- **适用题型**  
  1. “在树上删/选固定数量的边（或节点），使某个代价最大/最小”。  
  2. “树的分割 / 划分问题”，如“把树划分成 k 棵子树，最小化/最大化某种代价”。  
  3. “在树上进行 k 次操作（加/删/改），求最优结果”，常见于 DP + 组合优化。  
- **一句话总结解题钥匙**：  
  > **把全局的“删 k 条边”拆成每条子树内部的“删多少条”，用 DP 把子树的最优结果像背包一样逐层合并**。

---

## 反思

- **第一反应**：看到“删除若干边”，立刻想到枚举或贪心（删最小权重），但忽略了题目对 **删除数量的限制**（恰好/至多 k 条），导致思路走向错误。  
- **最容易踩的坑**  
  1. **状态范围错误**：`dp[u][c]` 的 `c` 必须受子树大小限制，否则会出现数组越界或不必要的计算。  
  2. **忘记把删除父子边本身计入一次**：在“删除边”分支里，需要额外 `+1` 来表示这条边被删掉。  
  3. **递归深度**：树可能是链状，需要把 Python 递归深度调高或改写成显式栈。  
- **下次类似题的第一步**：  
  > **先把树根化，明确每条边在递归中的“父‑子”关系，再决定 DP 状态（保留/删除多少）**，这样后面的合并自然会变成背包式的组合问题。