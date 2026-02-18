# #3530. 有向无环图中有效拓扑序的最大利润 / Maximum Profit from Valid Topological Order in DAG

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Graph、Topological Sort、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-profit-from-valid-topological-order-in-dag/)

---

## 题目（英文原版）

**Description**

You are given a Directed Acyclic Graph (DAG) with n nodes labeled from 0 to n - 1, represented by a 2D array edges, where edges[i] = [ui, vi] indicates a directed edge from node ui to vi. Each node has an associated score given in an array score, where score[i] represents the score of node i.
You must process the nodes in a valid topological order. Each node is assigned a 1-based position in the processing order.
The profit is calculated by summing up the product of each node's score and its position in the ordering.
Return the maximum possible profit achievable with an optimal topological order.
A topological order of a DAG is a linear ordering of its nodes such that for every directed edge u → v, node u comes before v in the ordering.

**Examples**

**Example 1:**

```
Input: n = 2, edges = [[0,1]], score = [2,3]
Output: 8
Explanation:

Node 1 depends on node 0, so a valid order is [0, 1] .
The maximum total profit achievable over all valid topological orders is 2 + 6 = 8 .
```

**Example 2:**

```
Input: n = 3, edges = [[0,1],[0,2]], score = [1,6,3]
Output: 25
Explanation:

Nodes 1 and 2 depend on node 0, so the most optimal valid order is [0, 2, 1] .
The maximum total profit achievable over all valid topological orders is 1 + 6 + 18 = 25 .
```

**Constraints**

- 1 <= n == score.length <= 22
- 1 <= score[i] <= 105
- 0 <= edges.length <= n * (n - 1) / 2
- edges[i] == [ui, vi] denotes a directed edge from ui to vi.
- 0 <= ui, vi < n
- ui != vi
- The input graph is guaranteed to be a DAG.
- There are no duplicate edges.

---

## 题目（中文翻译）

给定一个 **有向无环图（DAG）**，其中有 `n` 个节点，编号为 `0` 到 `n - 1`，图由二维数组 `edges` 表示，`edges[i] = [ui, vi]` 表示一条从节点 `ui` 指向节点 `vi` 的有向边。每个节点都有一个对应的 **分数（score）**，存于数组 `score` 中，`score[i]` 表示节点 `i` 的分数。

你需要按照一个 **有效拓扑序（topological order）** 处理这些节点。处理顺序中的每个节点会被分配一个 **1 基（1‑based）** 的 **位置（position）**。

**利润（profit）** 的计算方式为：所有节点的 `score[i] * position(i)` 的总和。

返回在所有可能的有效拓扑序中可以得到的 **最大利润**。

> **拓扑序**：有向无环图的线性排序，使得对每条有向边 `u → v`，节点 `u` 在排序中出现在节点 `v` 之前。

---

### 示例

#### 示例 1
```
输入: n = 2, edges = [[0,1]], score = [2,3]
输出: 8
解释:
节点 1 依赖于节点 0，因此一种有效的顺序是 [0, 1]。
在该顺序下的利润为 2*1 + 3*2 = 2 + 6 = 8，这是所有有效拓扑序中可以得到的最大利润。
```

#### 示例 2
```
输入: n = 3, edges = [[0,1],[0,2]], score = [1,6,3]
输出: 25
解释:
节点 1 和节点 2 都依赖于节点 0，最优的有效顺序是 [0, 2, 1]。
在该顺序下的利润为 1*1 + 3*2 + 6*3 = 1 + 6 + 18 = 25，这是所有有效拓扑序中可以得到的最大利润。
```

---

### 约束条件
- `1 <= n == score.length <= 22`
- `1 <= score[i] <= 10^5`
- `0 <= edges.length <= n * (n - 1) / 2`
- `edges[i] == [ui, vi]` 表示一条从 `ui` 到 `vi` 的有向边
- `0 <= ui, vi < n`
- `ui != vi`
- 输入的图一定是 **有向无环图（DAG）**
- 不存在重复的边

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有合法的拓扑序都枚举出来**，然后把每一种序列按照题目要求计算利润，取最大值。

- **数据结构**：  
  - `edges` 用邻接表（`list of lists`）存储，类似一本“路线手册”，`u -> v` 表示从城市 `u` 必须先到达再去城市 `v`。  
  - 为了判断当前哪个节点已经没有未完成的前置依赖，我们可以维护一个 **入度数组** `indeg[i]`，它记录还有多少条指向 `i` 的边没有被“移除”。这就像查字典时先看词条是否还有未解释的前置词，`indeg[i]==0` 时才可以“使用”这个词。  

- **枚举方式**：  
  - 采用深度优先搜索（DFS）+回溯。每一步挑选所有当前入度为 0（即没有未完成前置依赖）的节点之一放到序列的下一个位置。  
  - 放入后，要把它指向的所有后继节点的入度减 1（相当于把这条路标记为已走），递归继续。递归结束后记得恢复（回溯），把入度加回来，以便尝试其他选择。  

- **正确性**：  
  - 只要我们每一步只选入度为 0 的节点，就一定不会违背任何前置依赖；递归遍历所有可能的选择，就一定能遍历 **所有** 合法的拓扑序。遍历完后取最大利润即可。

- **时间/空间复杂度**：  
  - 在最坏情况下（完全没有边），每一步都有 `n, n-1, …, 1` 种选择，枚举的序列数是 `n!`（阶乘），这就是暴力的时间复杂度。  
    - `O(n!)` 可以想象成“把 n 本书全排列”。即使 `n=10`，`10! = 3,628,800`，已经非常大，`n=22` 更是不可想象。  
  - 除了递归栈外，只使用了 `O(n + m)` 的邻接表和入度数组（`m` 为边数），空间是线性的。  

#### 代码（Python）

```python
from typing import List

def maxProfit_bruteforce(n: int, edges: List[List[int]], score: List[int]) -> int:
    # 建立邻接表和入度数组
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1

    best = 0                     # 保存全局最大利润
    order = []                   # 当前正在构造的拓扑序

    def dfs(pos: int, cur_profit: int):
        """pos 为已经放好的节点数（也是下一个节点的 1‑based 位置）"""
        nonlocal best
        if pos == n:             # 所有节点都已排好序
            best = max(best, cur_profit)
            return

        # 找出当前所有入度为 0 且未被使用的节点
        for i in range(n):
            if indeg[i] == 0:
                # 选 i 放到第 pos+1 位
                indeg[i] = -1      # 标记为已使用（负数防止再次被选）
                # 把 i 的所有后继节点的入度减 1
                for nb in g[i]:
                    indeg[nb] -= 1

                # 累加利润：score[i] * (pos+1)
                dfs(pos + 1, cur_profit + score[i] * (pos + 1))

                # -------- 回溯 --------
                for nb in g[i]:
                    indeg[nb] += 1
                indeg[i] = 0

    dfs(0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(n!)`  
  - “阶乘”增长非常快，表示所有可能的排列数。对 `n=22` 来说根本不可能在计算机里跑完。  
- **空间复杂度**：`O(n + m)`  
  - 只用了邻接表、入度数组以及递归栈（深度最多 `n`），都是线性空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每一次都要把所有可能的序列完整展开**，导致指数级的时间。  
我们需要一种方式 **“记住已经算过的子问题”，避免重复计算**。这正是**动态规划**要做的事。

观察：

1. **拓扑序的本质**  
   在任意合法序列中，**已经放好的节点集合**（记作 `S`) 决定了后面还能放哪些节点：只有那些所有前驱都已经在 `S` 中的节点才可以被放下一个位置。  

2. **状态表示**  
   - 用 **位掩码（bitmask）** 表示集合 `S`。因为 `n ≤ 22`，`2^22 ≈ 4 million`，完全可以放进内存。  
   - `mask` 的第 `i` 位为 `1` 表示节点 `i` 已经被放进序列（即已经“移除”）。  

3. **可选节点**  
   对于当前 `mask`，若节点 `i` 的所有前驱都已经在 `mask` 中，则 `i` 可以作为下一个放入的节点。  
   - 前驱集合可以在预处理阶段得到：`pre[i]` 为所有直接前驱节点的位掩码。  
   - 判断方式：`(mask & pre[i]) == pre[i]`，即 `mask` 包含了 `pre[i]` 的所有位。  

4. **DP 转移**  
   - `dp[mask]` 表示 **已经放好 `mask` 中的节点，且这些节点恰好占据前 `popcount(mask)`（已放节点数）个位置时能够得到的最大利润**。  
   - `popcount(mask)` 可以用 Python 的 `bit_count()` 快速得到。  
   - 对于每个 `mask`，枚举所有可以新增的节点 `i`（满足上面的前驱条件且 `i` 不在 `mask` 中），得到新状态 `next_mask = mask | (1 << i)`。  
   - 新的利润贡献是 `score[i] * (pos)`，其中 `pos = popcount(mask) + 1`（因为 `i` 将放在第 `pos` 位）。  
   - 更新 `dp[next_mask] = max(dp[next_mask], dp[mask] + score[i] * pos)`。

5. **初始状态 & 结果**  
   - `dp[0] = 0`（没有放任何节点，利润为 0）。  
   - 最终答案是 `dp[(1 << n) - 1]`，即所有节点都已经放完时的最大利润。

6. **为什么是最优**  
   - 每个 `mask` 只会被计算一次，所有可能的子集合（最多 `2^n`）都被遍历。  
   - 转移只在合法的“可选节点”之间进行，保证了拓扑顺序的合法性。  
   - 由于我们在每一步都取最大值，`dp[mask]` 保存的就是 **从空集合走到 `mask` 的所有合法路径中利润最大的那条**。递推到全体集合，自然得到全局最优。

#### 代码（Python）

```python
from typing import List

def maxProfit_optimal(n: int, edges: List[List[int]], score: List[int]) -> int:
    # 1. 预处理：每个节点的前驱集合，用位掩码表示
    pre = [0] * n                     # pre[i] 的第 j 位为 1，表示 j 是 i 的直接前驱
    for u, v in edges:
        pre[v] |= 1 << u

    total_states = 1 << n             # 2^n 种子集合
    dp = [-1] * total_states          # -1 代表尚未到达/不可行
    dp[0] = 0                         # 空集合利润为 0

    for mask in range(total_states):
        if dp[mask] == -1:            # 该子集合不可达，直接跳过
            continue
        # 已经放好的节点数，就是下一位的下标（1‑based）
        pos = mask.bit_count() + 1

        # 2. 枚举可以放入的下一个节点 i
        for i in range(n):
            if mask >> i & 1:         # i 已经在 mask 中，不能再放
                continue
            # 前驱全部已经在 mask 中吗？
            if (mask & pre[i]) == pre[i]:
                next_mask = mask | (1 << i)
                profit = dp[mask] + score[i] * pos
                if profit > dp[next_mask]:
                    dp[next_mask] = profit

    # 3. 所有节点都放完的 mask 为 (1<<n)-1
    return dp[total_states - 1]
```

#### 复杂度

- **时间复杂度**：`O(n * 2^n)`  
  - 我们遍历所有 `2^n` 个子集合（约 4 million），对每个子集合最多检查 `n` 次可能的下一个节点。  
  - 与暴力的 `O(n!)` 相比，`2^n` 的增长要慢得多，`n=22` 时大约只需要几千万次基本操作，完全可以在 1 秒左右跑完。  

- **空间复杂度**：`O(2^n)`  
  - `dp` 数组保存每个子集合的最大利润，需要 `2^n` 个整数。  
  - 额外的 `pre` 数组只占 `O(n)`，整体仍然是指数级但可接受（约 4 MB）。

---

## 心得

- **核心技巧**：**位掩码动态规划（Subset DP）** 与 **拓扑约束的子集可达性判断**。  
- **适用的题型**：  
  1. “在 DAG 中挑选顺序使某个目标最大化”——如本题、**Maximum Score of a Node Sequence**。  
  2. “在有限集合里，状态转移只依赖于子集的包含关系”——如 **Shortest Hamiltonian Path**（旅行商问题的 DP 版），**Maximum XOR Subset**。  
- **解题钥匙**：**把“已经做了哪些决定”抽象成二进制位，用 DP 记忆每个子集合的最优结果**。

---

## 反思

- **第一反应**：看到“拓扑序”和“最大化加权和”，第一时间想到**枚举所有合法序列**（暴力回溯），因为直觉上只要满足前驱关系就行。  
- **最容易踩的坑**：  
  - **前驱判断错误**：忘记只检查**直接前驱**是否已经在集合中，导致非法序列被计入。  
  - **位运算细节**：`(mask & pre[i]) == pre[i]` 必须写对，顺序写反会判断成“mask 包含 pre”。  
  - **溢出/大数**：`score[i] ≤ 10^5`，`position ≤ 22`，乘积最多约 `2.2e6`，累计到 `n=22` 仍在 64 位整数范围，Python 的 `int` 自动大数无需担心。  
- **下次遇到同类题**：第一步先**把每个节点的前驱集合用位掩码保存**，再**考虑 DP 状态为“已经选了哪些节点”**，检查合法扩展节点的条件是否只依赖于子集包含关系。这样就能快速从暴力转向子集 DP。