# #2920. 收集所有节点硬币后的最大得分 / Maximum Points After Collecting Coins From All Nodes

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Tree、Depth-First Search、Memoization · [LeetCode 链接](https://leetcode.com/problems/maximum-points-after-collecting-coins-from-all-nodes/)

---

## 题目（英文原版）

**Description**

There exists an undirected tree rooted at node 0 with n nodes labeled from 0 to n - 1. You are given a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree. You are also given a 0-indexed array coins of size n where coins[i] indicates the number of coins in the vertex i, and an integer k.
Starting from the root, you have to collect all the coins such that the coins at a node can only be collected if the coins of its ancestors have been already collected.
Coins at nodei can be collected in one of the following ways:
Return the maximum points you can get after collecting the coins from all the tree nodes.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[1,2],[2,3]], coins = [10,10,3,3], k = 5
Output: 11                        
Explanation: 
Collect all the coins from node 0 using the first way. Total points = 10 - 5 = 5.
Collect all the coins from node 1 using the first way. Total points = 5 + (10 - 5) = 10.
Collect all the coins from node 2 using the second way so coins left at node 3 will be floor(3 / 2) = 1. Total points = 10 + floor(3 / 2) = 11.
Collect all the coins from node 3 using the second way. Total points = 11 + floor(1 / 2) = 11.
It can be shown that the maximum points we can get after collecting coins from all the nodes is 11.
```

**Example 2:**

```
Input: edges = [[0,1],[0,2]], coins = [8,4,4], k = 0
Output: 16
Explanation: 
Coins will be collected from all the nodes using the first way. Therefore, total points = (8 - 0) + (4 - 0) + (4 - 0) = 16.
```

**Constraints**

- n == coins.length
- 2 <= n <= 105
- 0 <= coins[i] <= 104
- edges.length == n - 1
- 0 <= edges[i][0], edges[i][1] < n
- 0 <= k <= 104

---

## 题目（中文翻译）

存在一棵以节点 0 为根的无向树，树中共有 `n` 个节点，编号为 `0` 到 `n - 1`。给定长度为 `n - 1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示树中存在一条连接节点 `a_i` 与节点 `b_i` 的边。另给定一个下标从 0 开始的数组 `coins`，大小为 `n`，其中 `coins[i]` 表示节点 `i` 上的硬币数量，以及一个整数 `k`。  

从根节点出发，你需要收集所有硬币，收集规则要求：只有在其所有祖先节点的硬币已经被收集的前提下，才能收集某个节点的硬币。  

节点 `i` 的硬币可以通过以下方式之一进行收集：

*（题目原文中会列出具体的收集方式，这里保持原样）*  

返回在收集完所有树节点的硬币后，你能够获得的最大得分。

**示例 1**  
```text
Input: edges = [[0,1],[1,2],[2,3]], coins = [10,10,3,3], k = 5
Output: 11
Explanation: 
先用第一种方式收集节点 0 的所有硬币。此时得分 = 10 - 5 = 5。  
再用第一种方式收集节点 1 的所有硬币。此时得分 = 5 + (10 - 5) = 10。  
随后用第二种方式收集节点 2 的硬币，使得节点 3 剩余的硬币为 `floor(3 / 2) = 1`。最终得分为 …（后续内容已截断）
```

**示例 2**  
```text
Input: edges = [[0,1],[0,2]], coins = [8,4,4], k = 0
Output: 16
Explanation: 
所有节点的硬币都使用第一种方式收集。因此，总得分 = (8 - 0) + (4 - 0) + (4 - 0) = 16。
```

**约束条件**

- `n == coins.length`
- `2 <= n <= 10^5`
- `0 <= coins[i] <= 10^4`
- `edges.length == n - 1`
- `0 <= edges[i][0], edges[i][1] < n`
- `0 <= k <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这棵树只有两种收集硬币的方式（题目原文省略了描述，这里补全）：  

1. **普通收集**：在当前节点 `x` 直接收集硬币，得到 `coins[x]`，但是要付出代价 `k`，即本节点的得分为 `coins[x] - k`。  
2. **半价收集**：在当前节点 `x` 施加一次「二分」操作，所有**已经受到的二分次数**都会再加 1。二分会把硬币数向下取整除以 2（在程序里等价于右移一位 `>> 1`），此时本节点不需要付 `k`，直接得到 `coins[x] / 2`（向下取整）。  

二分的效果会向下传递给子树：如果在祖先节点已经二分了 `t` 次，那么当前节点实际能够拿到的硬币数就是 `coins[x] >> t`（即 `coins[x] // 2^t`）。

**暴力做法**：  
- 对每个节点决定是「普通收集」还是「二分收集」——二选一。  
- 递归遍历整棵树，计算所有可能的决策组合的总得分，取最大值。  

这相当于在每个节点上做一次 **二叉选择**，整棵树有 `n` 个节点，组合数是 `2^n`，随 `n` 指数增长，根本不可行。

> **生活化类比**：把每个节点想成一本书的章节，普通收集就像直接买下这章节，需要付手续费 `k`；二分收集就像把整本书的内容压缩一半，省下手续费但每页内容也变少。要决定每一章是买原版还是压缩版，组合数会非常巨大。

#### 代码（Python）  

下面的代码仅作演示，**不会在大数据上通过**，仅用于说明暴力思路。  

```python
from collections import defaultdict

def brute_force(edges, coins, k):
    n = len(coins)
    # 建树（邻接表）
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 深度优先遍历，记录父子关系，防止回到父节点
    def dfs(u, parent, halve_cnt):
        """返回从子树 u 开始的最大得分，halve_cnt 表示已被二分的次数"""
        # 两种选择
        # 1）普通收集
        score_normal = (coins[u] >> halve_cnt) - k
        total_normal = score_normal
        for v in g[u]:
            if v == parent:
                continue
            total_normal += dfs(v, u, halve_cnt)   # 子树继续使用相同的二分次数

        # 2）在这里再二分一次
        score_half = (coins[u] >> (halve_cnt + 1))   # 本节点再二分一次，不付 k
        total_half = score_half
        for v in g[u]:
            if v == parent:
                continue
            total_half += dfs(v, u, halve_cnt + 1)   # 子树的二分次数 +1

        return max(total_normal, total_half)

    return dfs(0, -1, 0)

# 示例（仅用于演示，n 很小）
edges = [[0,1],[1,2],[2,3]]
coins = [10,10,3,3]
k = 5
print(brute_force(edges, coins, k))   # 结果是 11（和题目示例一致）
```

> 关键行解释（中文注释已在代码中）：  
> - `coins[u] >> halve_cnt`：把硬币数右移 `halve_cnt` 位，等价于除以 `2^halve_cnt` 并向下取整。  
> - `dfs(v, u, halve_cnt)` 与 `dfs(v, u, halve_cnt + 1)` 分别对应“继续使用相同的二分次数”与“再二分一次”。  

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 每个节点有两种决定，组合数是指数级的。  
- **空间复杂度**：`O(n)` —— 递归栈深度最多 `n`，以及保存邻接表的线性空间。  

显然，这种暴力解只能在 `n ≤ 15` 左右的极小测试里跑通，无法满足题目 `n ≤ 10^5` 的规模。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**唯一的状态**是“当前节点已经被二分了多少次”。  
如果我们把这个信息记下来，就可以避免重复计算——这正是**动态规划**的核心：把大问题拆成子问题，子问题的答案只和**有限的状态**有关。

**状态定义**  
> `dp[x][t]` = 在以节点 `x` 为根的子树里，**祖先已经二分了 `t` 次**（即 `coins[x]` 实际可得为 `coins[x] >> t`），从这棵子树收集全部硬币能够得到的**最大得分**。

**为什么只需要 `t` 这个维度？**  
- 决策只在当前节点：是普通收集还是再二分一次。  
- 子树的所有节点只会受到 **累计的二分次数** 的影响，和之前的选择细节无关。  

**状态转移**（直接套用题目提示）  

```
不二分当前节点（普通收集）：
    gain1 = (coins[x] >> t) - k               # 本节点得分
    child1 = Σ dp[child][t]                    # 子节点继续使用相同的二分次数

二分当前节点（再二分一次）：
    gain2 = (coins[x] >> (t + 1))              # 本节点得分（不付 k）
    child2 = Σ dp[child][t + 1]                # 子节点的二分次数加 1

dp[x][t] = max(gain1 + child1, gain2 + child2)
```

**边界**  
- 当 `t` 已经很大时，`coins[x] >> t` 可能为 `0`，此时继续二分也不会得到正收益。  
- 题目给出的上限 `coins[i] ≤ 10^4`，`2^14 = 16384 > 10^4`，所以 **当 `t ≥ 14` 时，所有节点的硬币数都已经变成 `0`**，此时 `dp[x][t] = 0`（不收也不罚）。这让状态空间从 `O(n·max_t)` 变成了 `O(n·15)`，非常可控。

**计算顺序**  
因为 `dp[x][t]` 需要子树的 `dp`，我们采用 **后序深度优先搜索（DFS）**：先算完子节点，再算父节点。

**整体算法**  

1. 把 `edges` 转成邻接表。  
2. 设 `MAX_T = 15`（足够覆盖所有可能的二分次数）。  
3. 用递归（或显式栈）从根 `0` 开始进行后序遍历。  
4. 对每个节点 `x`，遍历 `t = 0 … MAX_T-1`，按上面的转移公式计算 `dp[x][t]`。  
5. 最终答案为 `dp[0][0]`（根节点没有被二分过）。  

> **生活化类比**：把二分次数想成“折扣券的使用次数”。普通收集就像买东西要付手续费，二分收集相当于在结账时使用一张折扣券（把价钱减半），但使用券会让以后所有商品的折扣继续加深。我们只需要记住已经用了几张券，而不必记每一次具体是在哪个商品上用了。

#### 代码（Python）  

```python
import sys
sys.setrecursionlimit(2 * 10 ** 5)

from collections import defaultdict

def maxPoints(edges, coins, k):
    n = len(coins)
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    MAX_T = 15                     # 2^14 > 10^4, 再往后都是 0
    # dp[x] 将会是一个长度为 MAX_T 的列表，dp[x][t] 对应上面的定义
    dp = [[0] * MAX_T for _ in range(n)]

    def dfs(u, parent):
        """后序遍历，填完 dp[u] 后返回"""
        # 先递归子节点，确保子节点的 dp 已经算好
        for v in g[u]:
            if v == parent:
                continue
            dfs(v, u)

        # 对每一种已经二分的次数 t 计算 dp[u][t]
        for t in range(MAX_T):
            # ---- 方案一：普通收集（付 k）----
            # 本节点得分
            cur_val = (coins[u] >> t) - k
            # 子树继续使用相同的二分次数
            child_sum = 0
            for v in g[u]:
                if v == parent:
                    continue
                child_sum += dp[v][t]
            option1 = cur_val + child_sum

            # ---- 方案二：再二分一次（不付 k）----
            # 如果已经达到上限，进一步二分得到的硬币一定是 0，直接可以跳过
            if t + 1 < MAX_T:
                cur_val2 = (coins[u] >> (t + 1))
                child_sum2 = 0
                for v in g[u]:
                    if v == parent:
                        continue
                    child_sum2 += dp[v][t + 1]
                option2 = cur_val2 + child_sum2
            else:
                # t 已经是最大，继续二分只会得到 0 分，子树同样为 0
                option2 = 0

            dp[u][t] = max(option1, option2)

    dfs(0, -1)
    return dp[0][0]

# ------------------- 示例 -------------------
edges1 = [[0,1],[1,2],[2,3]]
coins1 = [10,10,3,3]
k1 = 5
print(maxPoints(edges1, coins1, k1))   # 11

edges2 = [[0,1],[0,2]]
coins2 = [8,4,4]
k2 = 0
print(maxPoints(edges2, coins2, k2))   # 16
```

> **关键行中文注释**  
> - `coins[u] >> t`：把硬币数右移 `t` 位，等价于除以 `2^t`（向下取整）。  
> - `option1` 与 `option2` 分别对应“普通收集”与“再二分一次”。  
> - `MAX_T = 15` 把状态空间压到常数级别，防止 O(n·logC) 变成 O(n·1e4)。  

#### 复杂度  

- **时间复杂度**：`O(n * MAX_T)` → `O(n * 15) ≈ O(n)`。  
  - 每个节点遍历一次，每个 `t`（最多 15）进行常数次加法/比较。  
- **空间复杂度**：`O(n * MAX_T)` 用于存 `dp`，即约 `15n`，再加上递归栈 `O(n)`，整体仍是线性 `O(n)`。  

相比暴力的指数级别，已经是 **线性** 的解法，能够轻松跑完 `n = 10^5` 的极限数据。

---

## 心得  

- **核心技巧**：**以「已二分次数」为状态的树形动态规划**。  
- **适用场景**：  
  1. 树上有「全局递增/递减」的属性（如乘以 2、除以 2、加 1 等）只和祖先的累计操作次数有关。  
  2. 需要在每个节点做「二选一」决策，而子树的状态只取决于一个小的整数参数。  
  3. 类似题目：  
     - *Maximum Profit of a Tree*（在树上做「加速」或「减速」操作）  
     - *Tree DP with Bitmask*（每条路径的位数累计影响后代）  

- **一句话总结**：  
  > 把「祖先已经用了多少次二分」记下来，用 DP 把树拆成子树独立求解，状态数只到 15，整体线性即可。

---

## 反思  

- **第一反应**：看到「二分」和「祖先影响」立刻想到「位运算」+「树形 DP」。  
- **最容易踩的坑**  
  1. **状态上界**：忘记 `coins[i] ≤ 10^4`，导致把 `t` 的上限设成 `log2(10^4)` 以上，浪费空间。  
  2. **子树累计**：在转移时把子树的 `dp` 加到本节点的得分时，必须注意对应的 `t`（相同或加 1），否则会产生错误的递推。  
  3. **递归深度**：树可能是链状的，递归深度可达 `10^5`，需要 `sys.setrecursionlimit` 或改写成显式栈。  

- **下次类似题**：  
  1. 先**抽象出「累计操作次数」或「累计状态」这个唯一影响子树的参数。  
  2. 判断该参数的最大可能取值（通常是对数级别），从而把 DP 状态压到常数。  
  3. 用后序 DFS 完成子树到父节点的 DP 合并。  

祝你玩转树形 DP，解锁更多高分！