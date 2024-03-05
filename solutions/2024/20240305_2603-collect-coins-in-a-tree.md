# #2603. 收集树中的硬币 / Collect Coins in a Tree

> 难度：困难 · 标签：Array、Tree、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/collect-coins-in-a-tree/)

---

## 题目（英文原版）

**Description**

There exists an undirected and unrooted tree with n nodes indexed from 0 to n - 1. You are given an integer n and a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree. You are also given an array coins of size n where coins[i] can be either 0 or 1, where 1 indicates the presence of a coin in the vertex i.
Initially, you choose to start at any vertex in the tree. Then, you can perform the following operations any number of times:
Find the minimum number of edges you need to go through to collect all the coins and go back to the initial vertex.
Note that if you pass an edge several times, you need to count it into the answer several times.

**Examples**

**Example 1:**

```
Input: coins = [1,0,0,0,0,1], edges = [[0,1],[1,2],[2,3],[3,4],[4,5]]
Output: 2
Explanation: Start at vertex 2, collect the coin at vertex 0, move to vertex 3, collect the coin at vertex 5 then move back to vertex 2.
```

**Example 2:**

```
Input: coins = [0,0,0,1,1,0,0,1], edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[5,6],[5,7]]
Output: 2
Explanation: Start at vertex 0, collect the coins at vertices 4 and 3, move to vertex 2,  collect the coin at vertex 7, then move back to vertex 0.
```

**Constraints**

- n == coins.length
- 1 <= n <= 3 * 104
- 0 <= coins[i] <= 1
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- edges represents a valid tree.

---

## 题目（中文翻译）

存在一棵无向且未根的树（undirected and unrooted tree），有 `n` 个节点，编号为 `0` 到 `n - 1`。  
给定整数 `n` 和一个长度为 `n - 1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间有一条边。  
同时给定大小为 `n` 的数组 `coins`，`coins[i]` 只能是 `0` 或 `1`，`1` 表示节点 `i` 上有一枚硬币。

最初，你可以选择树中的任意一个节点作为起点。之后，你可以任意多次执行以下操作：

* 找到需要经过的最少边数，使得能够收集所有硬币并回到初始节点。

注意，如果一条边被多次经过，则需要在答案中多次计数。

---

### 示例

#### 示例 1
```text
Input: coins = [1,0,0,0,0,1], edges = [[0,1],[1,2],[2,3],[3,4],[4,5]]
Output: 2
Explanation: 从节点 2 开始，先收集节点 0 的硬币，移动到节点 3，收集节点 5 的硬币后再回到节点 2。
```

#### 示例 2
```text
Input: coins = [0,0,0,1,1,0,0,1], edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[5,6],[5,7]]
Output: 2
Explanation: 从节点 0 开始，收集节点 4 和 3 的硬币，随后移动到节点 2，收集节点 7 的硬币，最后回到节点 0。
```

---

### 约束条件
- `n == coins.length`
- `1 <= n <= 3 * 10^4`
- `0 <= coins[i] <= 1`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= a_i, b_i < n`
- `a_i != b_i`
- `edges` 构成一棵有效的树（valid tree）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**“把所有可能的走法都枚举一遍，找最短的那条”**。  
可以把树看成一张地图，树上的每条边就像两座城市之间的道路。  
我们先任选一个起点 `start`，然后在这棵树上随意走动，直到把所有标记为 `1` 的节点（即有硬币的节点）都走到，再回到 `start`。  

- **数据结构**：  
  - **邻接表**（`graph[u]` 保存所有与 `u` 相连的节点）。  
    - 类比：就像一本“城市手册”，每一页（节点 `u`）上列出这座城市能直接到达的其他城市（相邻节点）。  
  - **递归 + 回溯**：在每一步尝试走向每一条相邻的边，记录已经收集到的硬币数量，所有硬币收齐后再返回起点。  

- **为什么正确**：  
  只要遍历 **所有** 合法的走法（包括走回头路、重复经过同一条边的情况），必然会碰到最优的那一条。于是把所有走法的长度都算出来，取最小值，就是答案。

- **复杂度分析（大白话）**：  
  - 树上有 `n` 个节点，最多有 `n‑1` 条边。  
  - 对每一步我们都有 **“往哪走”** 的选择，最坏情况下会把每条边都走 **无限次**（因为可以回头），于是搜索空间呈指数增长，近似 `O(2^n)`。  
  - 空间上除了存图和递归栈外，只需要 `O(n)` 的额外空间。

> 直觉解只能用来**验证思路**或在极小规模（比如 `n ≤ 10`）时做实验，面对 `n ≤ 3·10^4` 的正式数据根本跑不完。

#### 代码（Python）

```python
from collections import defaultdict

def brute_force_min_edges(coins, edges):
    n = len(coins)
    # 1️⃣ 建图：邻接表
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 2️⃣ 统计总硬币数，作为结束条件
    total_coins = sum(coins)

    # 3️⃣ 深度优先搜索 + 回溯
    def dfs(cur, visited, collected, steps):
        """
        cur       : 当前所在的节点
        visited   : 已经遍历过的路径（用于避免无限循环的简单剪枝）
        collected : 已经收集到的硬币数量
        steps     : 已走过的边数（即当前路径的长度）
        """
        # 收集当前节点的硬币（若有）
        if coins[cur] == 1 and cur not in visited:
            collected += 1
        visited.add(cur)

        # 4️⃣ 终止条件：所有硬币都收集完，并且回到起点
        if collected == total_coins and cur == start:
            return steps

        best = float('inf')
        # 5️⃣ 尝试走每一条相邻的边
        for nxt in graph[cur]:
            # 这里我们允许重复经过同一条边，所以不做 visited 检查
            best = min(best, dfs(nxt, visited.copy(), collected, steps + 1))
        return best

    answer = float('inf')
    # 6️⃣ 枚举每个节点作为起点
    for start in range(n):
        answer = min(answer, dfs(start, set(), 0, 0))
    return answer
```

> 代码里每一行都加了中文注释，帮助你对照思路。**注意**：`visited.copy()` 会导致指数级的时间消耗，这正是暴力解慢的根本原因。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）——每次递归都可能分叉，搜索空间随节点数指数增长。  
  > 大白话：如果树有 20 个节点，理论上要尝试的走法可能有几千万甚至上亿，根本跑不完。

- **空间复杂度**：`O(n)`——存图、递归栈以及临时的 `visited` 集合。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **“枚举所有走法”** 完全不可行。  
要想快，我们必须 **直接找出哪些节点真的必须走，哪些可以直接舍弃**。  
下面一步步推导出最优的 **剪枝 + 计数** 方法（也叫 “两轮叶子削减”），思路全程不涉及复杂的搜索，只用 **树的结构** 本身就能得到答案。

---

#### 2.1 第一步：删掉“没有硬币的叶子”

- **叶子**：度为 1 的节点（只连着一条边）。  
- **直观类比**：想象树是一棵长满硬币的树枝，如果一根枝条的最末端（叶子）上没有硬币，那这根枝条永远不需要去碰——无论你从哪儿出发，都不会把它纳入必走路径。  

**操作**：把所有 **度为 1 且 coins[i] == 0** 的节点一次性删除（把它和唯一相连的那条边一起去掉），然后可能会产生新的叶子，继续删除，直到所有剩余的叶子上都有硬币。

- **为什么这样做不影响答案**：  
  - 这些被删掉的节点上没有硬币，且它们是“死路”——走进去只能再走回去，增加的边数只能让答案变大。  
  - 把它们直接去掉，相当于把“无用的路段”提前剪掉，最短路径自然不会包含它们。

---

#### 2.2 第二步：再删掉“叶子 + 它的父节点”

在第一轮剪枝后，树的每个叶子必然都有硬币。  
现在考虑**“如果我们把这棵树的最外层再往里收缩一层，会怎样？”**  
- 把 **每个叶子**（一定有硬币）以及 **它唯一的相邻节点（父节点）** 同时删除。  
- 删除后，原本的父节点的所有子树已经被完全访问（因为子树里所有硬币都在叶子上），所以我们不需要再回到父节点去别的地方。

**结果**：剩下的节点构成了 **“必须遍历的核心”**，记作 `core`。  
- `core` 中的每条边都 **一定会被走两次**（去一次，回来一次），因为它们连接的两端都必须被访问且没有更短的“绕路”。  
- 因此 **答案 = 2 × (core 中的边数)**。

如果 `core` 里只有 0 条边（即所有硬币都在同一个节点或相邻的两个节点），答案自然为 `0`（不需要走任何边）或者 `2`（走一次再回）。

---

#### 2.3 公式化

- 设 `remain` 为第二轮剪枝后剩余的节点数。  
- 在一棵树里，**节点数 = 边数 + 1**，所以 `core 的边数 = remain - 1`。  
- **最终答案**  
  \[
  \text{ans} = 2 \times (remain - 1)
  \]

---

#### 2.4 关键数据结构：**队列 + 度数组**

- **度数组 `deg[i]`**：记录每个节点当前的度（相连的边数），方便判断叶子。  
- **队列**：一次性把所有当前的叶子放进去，逐层弹出进行削减。类似 **BFS**（层序遍历），但这里的层是“叶子层”。

---

#### 2.5 步骤概览

| 步骤 | 操作 | 目的 |
|------|------|------|
| 1 | 计算每个节点的度 `deg`，把所有 `deg==1 && coins[i]==0` 的叶子入队 | 删除“无硬币的叶子”。 |
| 2 | 循环弹出队列：删除该叶子，度减 1，若其唯一邻居变成新的 “无硬币叶子”，继续入队。 | 递归式地把所有无用的枝条全部剪掉。 |
| 3 | 统计剩余节点 `remain`（度 > 0 的节点），若 `remain ≤ 1` 直接返回 0。 | 进入第二轮削减的前置检查。 |
| 4 | 再次把所有 **当前叶子**（此时一定有硬币）入队，进行一次 **“叶子+父节点”** 的批量删除。 | 得到核心 `core`，即必须走的子树。 |
| 5 | 计算 `remain`（删除完第二轮后剩余的节点数），答案 = `2 * (remain - 1)`。 | 直接得到最小走边数。 |

---

#### 代码（Python）

```python
from collections import deque, defaultdict

def collectCoins(coins, edges):
    """
    返回在任意起点出发，收集所有硬币并回到起点所需的最少边数。
    思路：两轮叶子削减 → 只剩核心节点，答案 = 2 * (核心节点数 - 1)
    """
    n = len(coins)
    if n == 1:                     # 只有一个节点，答案一定是 0
        return 0

    # ---------- 1️⃣ 建图 & 计算度 ----------
    graph = defaultdict(list)
    deg = [0] * n
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # ---------- 2️⃣ 第一次削叶子：删除没有硬币的叶子 ----------
    q = deque()
    for i in range(n):
        if deg[i] == 1 and coins[i] == 0:   # 只连一条边且没有硬币
            q.append(i)

    while q:
        leaf = q.popleft()
        deg[leaf] = 0            # 把 leaf 标记为已删除
        # leaf 只有唯一的邻居
        for nb in graph[leaf]:
            if deg[nb] == 0:     # 已经被删除的邻居直接跳过
                continue
            deg[nb] -= 1         # 与 leaf 的这条边被剪掉
            # 如果 nb 现在变成 “没有硬币的叶子”，继续入队
            if deg[nb] == 1 and coins[nb] == 0:
                q.append(nb)

    # ---------- 3️⃣ 统计第一次削减后剩余的节点 ----------
    remain = sum(1 for d in deg if d > 0)
    if remain == 0:               # 所有硬币都被删除了（只有 0 枚硬币的情况）
        return 0

    # ---------- 4️⃣ 第二次削叶子：删除每个叶子以及它的父节点 ----------
    q.clear()
    for i in range(n):
        if deg[i] == 1:           # 现在的所有叶子一定都有硬币
            q.append(i)

    # 记录哪些节点已经在第二轮被删除
    removed = [False] * n
    while q:
        leaf = q.popleft()
        if deg[leaf] == 0:        # 可能已经在本轮被删除
            continue
        # leaf 的唯一邻居（父节点）
        parent = next(nb for nb in graph[leaf] if deg[nb] > 0)
        # 删除 leaf
        deg[leaf] = 0
        removed[leaf] = True
        # 删除 parent（只要它还未被删掉）
        if not removed[parent]:
            deg[parent] = 0
            removed[parent] = True
            # 父节点的其它邻居可能会变成新的叶子，加入队列
            for nb in graph[parent]:
                if deg[nb] == 1 and not removed[nb]:
                    q.append(nb)

    # ---------- 5️⃣ 计算核心节点数 ----------
    core_nodes = sum(1 for d in deg if d > 0)
    # 核心为空或只有一个节点时，不需要走任何边
    if core_nodes <= 1:
        return 0
    # 最小走边数 = 2 * (核心节点数 - 1)
    return 2 * (core_nodes - 1)
```

**代码要点解读**

| 行号 | 关键代码 | 中文解释 |
|------|----------|----------|
| 10‑13 | `graph = defaultdict(list)`、`deg = [0]*n` | 用邻接表存图，用 `deg` 记录每个节点的当前度（相连的边数）。 |
| 16‑19 | `if deg[i] == 1 and coins[i] == 0: q.append(i)` | 把所有 **“没有硬币的叶子”** 放进队列，准备第一次削减。 |
| 22‑29 | `while q: … deg[nb] -= 1 … if deg[nb]==1 and coins[nb]==0: q.append(nb)` | **层层剪枝**：删掉叶子后可能产生新的叶子，继续删。 |
| 33 | `remain = sum(1 for d in deg if d > 0)` | 统计第一次削减后还剩下的节点数。 |
| 38‑40 | `if deg[i] == 1: q.append(i)` | 把 **“当前所有叶子（一定有硬币）”** 加入队列，准备第二轮削减。 |
| 45‑57 | `leaf = q.popleft() … parent = next(nb for nb in graph[leaf] if deg[nb] > 0)` | **一次性删除叶子和它的父节点**，并把父节点的其他邻居可能形成的新叶子加入队列。 |
| 63‑66 | `core_nodes = sum(1 for d in deg if d > 0)`、`return 2 * (core_nodes - 1)` | 计算核心节点数并得到最终答案。 |

---

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每条边至多被访问常数次（第一次削叶子时删一次，第二次削叶子时删一次），所以整体线性。  
  - 大白话：不管树有多大，只要遍历一次节点和一次边，答案马上算出来。

- **空间复杂度**：`O(n)`  
  - 存图的邻接表、度数组、队列等都跟节点数成正比。  

相较于暴力解的指数级时间，最优解把 **“枚举所有走法”** 直接转化为 **“只保留必要的节点”**，实现了线性效率。

---

## 心得

- **核心技巧**：**两轮叶子削减**（先删无硬币叶子，再删叶子+父节点），把原问题转化为 “核心子树的大小”。  
- **适用场景**：  
  1. **树上收集/删除** 类问题（如 “树中删除所有叶子节点”， “树上最小覆盖子树”）。  
  2. **与距离无关，只关节点是否必须访问** 的题目（如 “删除无价值的子树”， “最小树形覆盖”）。  
  3. **树的直径/中心** 相关的变体（因为核心子树的直径往往决定答案的上界）。  
- **一句话总结**：**把所有“不需要走的路”提前剪掉，剩下的才是必须走的核心，答案就是核心的边数乘以 2**。

---

## 反思

- **第一反应**：看到“收集所有硬币并回到起点”，立刻想到遍历所有路径或做旅行商（TSP）式的搜索。  
- **最容易踩的坑**：  
  - **忘记第二轮削叶子**：只删掉没有硬币的叶子会得到 **“最小包含所有硬币的子树”**，但答案不是它的边数两倍，还要再把最外层的叶子‑父节点一起剔除。  
  - **边界条件**：全部硬币在同一个节点或相邻两个节点时，核心节点数 ≤ 1，答案应为 0，而不是负数。  
  - **多次删除导致度数组出错**：在第二轮削除时，需要同步维护 `deg` 与 `removed`，否则会把已经删除的节点误当成新的叶子。  
- **下次遇到类似题**：  
  1. **先判断哪些节点是“必经”**（比如有价值的、必须访问的），  
  2. **用度数或拓扑思想把无价值的叶子层层剔除**，  
  3. **再根据剩余结构直接计数**（边数、直径、深度等），而不是枚举路径。  

这样就能把原本看似“Hard”的树形遍历问题，快速化简为 **线性时间** 的计数题。祝你玩得开心，算法之路越走越顺！