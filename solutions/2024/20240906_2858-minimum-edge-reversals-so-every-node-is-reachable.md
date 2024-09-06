# #2858. **最小边翻转次数使每个节点可达** / Minimum Edge Reversals So Every Node Is Reachable

> 难度：困难 · 标签：Dynamic Programming、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/minimum-edge-reversals-so-every-node-is-reachable/)

---

## 题目（英文原版）

**Description**

There is a simple directed graph with n nodes labeled from 0 to n - 1. The graph would form a tree if its edges were bi-directional.
You are given an integer n and a 2D integer array edges, where edges[i] = [ui, vi] represents a directed edge going from node ui to node vi.
An edge reversal changes the direction of an edge, i.e., a directed edge going from node ui to node vi becomes a directed edge going from node vi to node ui.
For every node i in the range [0, n - 1], your task is to independently calculate the minimum number of edge reversals required so it is possible to reach any other node starting from node i through a sequence of directed edges.
Return an integer array answer, where answer[i] is the  minimum number of edge reversals required so it is possible to reach any other node starting from node i through a sequence of directed edges.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[2,0],[2,1],[1,3]]
Output: [1,1,0,2]
Explanation: The image above shows the graph formed by the edges.
For node 0: after reversing the edge [2,0], it is possible to reach any other node starting from node 0.
So, answer[0] = 1.
For node 1: after reversing the edge [2,1], it is possible to reach any other node starting from node 1.
So, answer[1] = 1.
For node 2: it is already possible to reach any other node starting from node 2.
So, answer[2] = 0.
For node 3: after reversing the edges [1,3] and [2,1], it is possible to reach any other node starting from node 3.
So, answer[3] = 2.
```

**Example 2:**

```
Input: n = 3, edges = [[1,2],[2,0]]
Output: [2,0,1]
Explanation: The image above shows the graph formed by the edges.
For node 0: after reversing the edges [2,0] and [1,2], it is possible to reach any other node starting from node 0.
So, answer[0] = 2.
For node 1: it is already possible to reach any other node starting from node 1.
So, answer[1] = 0.
For node 2: after reversing the edge [1, 2], it is possible to reach any other node starting from node 2.
So, answer[2] = 1.
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ui == edges[i][0] < n
- 0 <= vi == edges[i][1] < n
- ui != vi
- The input is generated such that if the edges were bi-directional, the graph would be a tree.

---

## 题目（中文翻译）

存在一个 **有向图（directed graph）**，有 `n` 个节点，编号为 `0` 到 `n-1`。如果把所有边都视为双向的，则该图会形成一棵树。  
给定整数 `n` 和二维整数数组 `edges`，其中 `edges[i] = [ui, vi]` 表示一条 **有向边（directed edge）** 从节点 `ui` 指向节点 `vi`。  
**边翻转（edge reversal）** 指改变一条边的方向，即原本从 `ui` 指向 `vi` 的有向边会变成从 `vi` 指向 `ui` 的有向边。  

对于区间 `[0, n-1]` 内的每个节点 `i`，请独立计算最少需要多少次 **边翻转**，使得从节点 `i` 出发能够通过一系列有向边到达任意其他节点。  
返回一个整数数组 `answer`，其中 `answer[i]` 为使从节点 `i` 出发能够到达所有其他节点所需的最小 **边翻转**次数。

---

### 示例

**示例 1**

```text
Input: n = 4, edges = [[2,0],[2,1],[1,3]]
Output: [1,1,0,2]
```

**解释**：上图展示了由 `edges` 构成的图。  

- 节点 0：翻转边 `[2,0]` 后，能够从节点 0 到达任意其他节点。因此 `answer[0] = 1`。  
- 节点 1：翻转边 `[2,1]` 后，能够从节点 1 到达任意其他节点。因此 `answer[1] = 1`。  
- 节点 2：已经能够到达所有节点，无需翻转，`answer[2] = 0`。  
- 节点 3：...（已截断）

**示例 2**

```text
Input: n = 3, edges = [[1,2],[2,0]]
Output: [2,0,1]
```

**解释**：上图展示了由 `edges` 构成的图。  

- 节点 0：翻转边 `[2,0]` 与 `[1,2]` 后，能够从节点 0 到达任意其他节点。因此 `answer[0] = 2`。  
- 节点 1：已经能够到达所有节点，无需翻转，`answer[1] = 0`。  
- 节点 2：翻转边 `[1,2]` 后，能够从节点 2 到达任意其他节点。因此 `answer[2] = 1`。  
- ...（已截断）

---

### 约束条件

- `2 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= ui == edges[i][0] < n`
- `0 <= vi == edges[i][1] < n`
- `ui != vi`
- 输入保证：如果把所有边都视为双向的，则该图是一棵树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是：**把一棵有向树（每条边只有一个方向）改造，使得从某个起点能够走到所有其它节点**，并且要找出每个起点最少需要翻转多少条边。  
最直接的想法是**枚举每个节点 i**，然后**尝试所有可能的翻转方案**，检查哪些方案能让 i 能遍历整棵树，取翻转次数最少的那个。

- **枚举方案**：把每条边看成“要不要翻转”。因为有 `n-1` 条边，所有可能的翻转组合是 `2^(n-1)` 种（每条边两种状态），这相当于把每条边放进一个“开关”。  
- **检查可达性**：对每一种开关状态，得到一张新的有向图。我们可以用 **BFS/DFS** 从 i 出发，看能否访问到 `n` 个节点。  
- **统计翻转次数**：把被翻转的边数加起来，更新 i 的最小值。

> **类比**：把图想象成城市的单行道，翻转相当于把单行道改成相反方向。我们要把所有可能的“改道”方案列出来，看看哪种最省钱。

> **为什么正确**：穷举所有可能的翻转方式，必然会包含最优解。只要检查到 i 能遍历全图的方案，就能得到最小翻转次数。

#### 代码（Python）

```python
from collections import defaultdict, deque
from itertools import product
from typing import List

def minReversals_bruteforce(n: int, edges: List[List[int]]) -> List[int]:
    # 把原始有向边保存下来，后面会根据翻转状态重新构图
    original = [(u, v) for u, v in edges]

    ans = [float('inf')] * n          # 最终答案，先设为无穷大

    # 对每一条边枚举是否翻转，2^(n-1) 种组合
    for mask in range(1 << (n - 1)):
        # 根据 mask 生成当前图的邻接表
        g = defaultdict(list)
        rev_cnt = 0                    # 记录本次组合翻转了几条边
        for idx, (u, v) in enumerate(original):
            if mask >> idx & 1:        # 这条边要翻转
                g[v].append(u)         # 方向反过来
                rev_cnt += 1
            else:
                g[u].append(v)         # 保持原方向

        # 对每个起点检查是否能遍历全图
        for start in range(n):
            # BFS 看能否访问到所有节点
            visited = [False] * n
            q = deque([start])
            visited[start] = True
            while q:
                cur = q.popleft()
                for nxt in g[cur]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        q.append(nxt)
            if all(visited):           # 能遍历全图，更新答案
                ans[start] = min(ans[start], rev_cnt)

    return ans
```

> 这段代码可以直接跑，但是 **会超时**（指数级的搜索），只适合作为思路展示。

#### 复杂度

- **时间复杂度**：`O( 2^{n-1} * n * (n + m) )`  
  解释：`2^{n-1}` 是所有翻转组合的数量，外层每个组合我们都要对 `n` 个起点跑一次 BFS，BFS 的复杂度是 `O(n + m)`（这里 `m = n-1`）。显然随着 `n` 增大，计算量爆炸，根本不可行。

- **空间复杂度**：`O(n + m)`  
  解释：邻接表和 BFS 队列需要线性空间，和图的规模成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有翻转方式**。实际上，图本身是一棵 **树**（如果把每条有向边都当成无向边），我们可以利用 **树形 DP + 换根技巧** 在 **线性时间** 求出每个节点的最小翻转次数。

**核心概念**：

1. **把每条有向边标记方向**  
   - 若原始方向是 `u → v`，我们记 `cost(u, v) = 0`（从 u 出发走向 v 不需要翻转），  
   - `cost(v, u) = 1`（如果想从 v 走向 u，需要把这条边翻转一次）。  
   这就像在无向树的每条边上贴了两张“票”，从左到右票价 0，从右到左票价 1。

2. **第一次 DFS：计算 `dp[x]`**  
   以 **节点 0** 为根，`dp[x]` 表示 **从 x 出发只能访问到它的子树**（即以 x 为根的那部分）所需要的最少翻转次数。递推公式：

   ```
   dp[x] = Σ ( dp[child] + cost(x, child) )
   ```

   直观解释：要让 x 能到达它的每个子节点 `child`，首先要保证子树内部已经可以相互到达（这就是 `dp[child]`），然后还要保证 **从 x 能走到 child**，如果原来的边是 child → x，则需要额外翻转 1 次（`cost(x, child)=1`），否则 0 次。

   这一步只需要一次后序遍历（自底向上），时间 `O(n)`。

3. **第二次 DFS：换根得到 `answer[x]`**  
   已知根 0 的答案 `answer[0] = dp[0]`（因为根已经覆盖了整棵树）。现在把根 **移动** 到它的子节点 `y`，要重新计算 `answer[y]`，只需要 **局部调整**：

   ```
   answer[y] = answer[x] - cost(x, y) + cost(y, x)
   ```

   解释：

   - 当根在 `x` 时，`cost(x, y)` 已经计入 `answer[x]`（因为从 x 到 y 需要的翻转次数）。把根搬到 y，**这条边的方向需求反过来**：  
     - 如果原来是 `x → y`（cost(x, y)=0），根在 y 时就要 **翻转这条边**，即加 `cost(y, x)=1`。  
     - 如果原来是 `y → x`（cost(x, y)=1），根在 y 时这条边自然满足，不需要翻转，反而可以把之前多加的 1 去掉，即 `-1`。

   只要沿着树做一次前序遍历，把根从父节点移动到子节点，就能在 **O(1)** 的时间更新子节点的答案。整个过程也是 `O(n)`。

4. **整体流程**  
   - 建图时把每条有向边记成两条**带权**的无向边：`(u, v, 0)` 表示从 u 到 v 不需要翻转，`(v, u, 1)` 表示从 v 到 u 需要翻转一次。  
   - 第一次 DFS 计算 `dp`（后序），得到 `answer[0] = dp[0]`。  
   - 第二次 DFS（前序）使用换根公式填满 `answer` 数组。  

> **类比**：把树想象成一座山，根节点是山顶。第一次爬山时我们记录每条小路向下走是否需要翻转（相当于下坡顺畅，上坡要搬土）。第二次把山顶搬到别的地方，只需要把搬动的那条小路的“搬土量”改个符号，其余路保持不变。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def minReversals(n: int, edges: List[List[int]]) -> List[int]:
    """
    返回 answer[i]：从 i 出发能够到达所有节点所需的最少翻转次数
    """

    # ---------- 建图 ----------
    # 对每条有向边 (u -> v) 添加两条带权无向边
    #   u -> v 的权重 0（不需要翻转）
    #   v -> u 的权重 1（需要翻转一次）
    g = defaultdict(list)          # g[node] = [(neighbor, cost_from_node_to_neighbor), ...]
    for u, v in edges:
        g[u].append((v, 0))        # 原方向，无需翻转
        g[v].append((u, 1))        # 反方向，需要翻转

    # ---------- 第一次 DFS：计算 dp ----------
    dp = [0] * n                    # dp[x] = 子树内部需要的翻转次数
    parent = [-1] * n               # 记录父节点，后面换根要用

    def dfs1(x: int, p: int) -> None:
        parent[x] = p
        for nb, w in g[x]:
            if nb == p:
                continue
            dfs1(nb, x)                     # 先处理子树
            dp[x] += dp[nb] + w             # 子树翻转 + 从 x 到 nb 的额外翻转（w）

    dfs1(0, -1)                     # 任选 0 作为初始根

    # ---------- 第二次 DFS：换根得到 answer ----------
    answer = [0] * n
    answer[0] = dp[0]               # 根 0 的答案已经是 dp[0]

    def dfs2(x: int, p: int) -> None:
        for nb, w in g[x]:
            if nb == p:
                continue
            # 换根公式：
            # answer[nb] = answer[x] - w + (1 - w)
            #   w == 0  => edge x->nb, 需要在 nb 为根时翻转 (+1)
            #   w == 1  => edge nb->x, 在 nb 为根时可以省掉这一次翻转 (-1)
            answer[nb] = answer[x] - w + (1 - w)
            dfs2(nb, x)

    dfs2(0, -1)

    return answer
```

> **代码要点注释**  
- `g[u].append((v, 0))` 表示如果我们站在 `u`，沿着这条边去 `v` 不需要翻转。  
- `dp[x] += dp[nb] + w` 把子树的答案累加，并加上从 `x` 到子节点 `nb` 这条边的“额外代价”。  
- 换根公式 `answer[nb] = answer[x] - w + (1 - w)` 实际上等价于 `answer[nb] = answer[x] + (1 if w==0 else -1)`，直观地把这条边的需求从“需要翻转”变成“需要翻转相反方向”。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次 DFS 遍历每条边一次，第二次 DFS 也遍历每条边一次，总共 `2·(n-1)` 次操作。  
  - 与 `n` 成线性关系，能够轻松处理 `10^5` 规模的输入。

- **空间复杂度**：`O(n)`  
  - 邻接表存储 `2·(n-1)` 条带权边，`dp`、`answer`、`parent` 各占 `O(n)`。  
  - 递归深度最坏为 `n`（树可能是链），在 Python 中可以改成显式栈或使用 `sys.setrecursionlimit` 防止递归层数溢出。

---

## 心得

- **核心技巧**：**树形 DP + 换根（Re‑rooting）**。先在固定根上算出子树内部需要的翻转次数，再通过局部调整把根搬到每个节点，得到全局答案。
- **适用的题型**  
  1. “把所有节点都能到达” 类的最小操作数（如 LeetCode 1466. Reorder Routes to Make All Paths Lead to the City Zero）。  
  2. “每个节点的子树信息” 需要在所有根上求解的题目（如求每个节点的子树大小、子树中颜色数量等）。
- **一句话总结解题钥匙**：**把有向树看成带权无向树，用一次后序 DP 统计子树代价，再用换根技巧把根移动到每个节点，局部更新即可得到答案。**

---

## 反思

- **第一反应**：看到“每个节点都要独立求最少翻转次数”，自然想到“枚举每个节点、枚举每条边的翻转”，于是想到暴力搜索。  
- **最容易踩的坑**  
  - **方向代价写反**：记 `cost(u, v)` 为从 `u` 出发沿这条边是否需要翻转，0 表示已经是 `u → v`，1 表示需要翻转。写反会导致 DP 公式错误。  
  - **换根公式的符号**：`answer[child] = answer[parent] - w + (1-w)` 中的 `-w` 与 `+ (1-w)` 必须对应原始方向，容易写成 `+w - (1-w)`。  
  - **递归深度**：树可能是链状，递归层数达到 `10^5` 会导致 Python RecursionError，需要提前 `sys.setrecursionlimit(2*10**5)` 或改成显式栈。  
- **下次类似题的第一步**：**先判断图是否是树**，如果是，考虑**把有向边转成带权无向边**，并**在一棵固定根的树上做一次 DP**，随后使用**换根技巧**一次性得到所有根的答案。这样即可把指数级的暴力搜索压缩到线性时间。