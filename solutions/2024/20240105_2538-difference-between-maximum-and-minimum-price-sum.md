# #2538. 最大与最小价格和之差 / Difference Between Maximum and Minimum Price Sum

> 难度：困难 · 标签：Array、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/difference-between-maximum-and-minimum-price-sum/)

---

## 题目（英文原版）

**Description**

There exists an undirected and initially unrooted tree with n nodes indexed from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
Each node has an associated price. You are given an integer array price, where price[i] is the price of the ith node.
The price sum of a given path is the sum of the prices of all nodes lying on that path.
The tree can be rooted at any node root of your choice. The incurred cost after choosing root is the difference between the maximum and minimum price sum amongst all paths starting at root.
Return the maximum possible cost amongst all possible root choices.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[0,1],[1,2],[1,3],[3,4],[3,5]], price = [9,8,7,6,10,5]
Output: 24
Explanation: The diagram above denotes the tree after rooting it at node 2. The first part (colored in red) shows the path with the maximum price sum. The second part (colored in blue) shows the path with the minimum price sum.
- The first path contains nodes [2,1,3,4]: the prices are [7,8,6,10], and the sum of the prices is 31.
- The second path contains the node [2] with the price [7].
The difference between the maximum and minimum price sum is 24. It can be proved that 24 is the maximum cost.
```

**Example 2:**

```
Input: n = 3, edges = [[0,1],[1,2]], price = [1,1,1]
Output: 2
Explanation: The diagram above denotes the tree after rooting it at node 0. The first part (colored in red) shows the path with the maximum price sum. The second part (colored in blue) shows the path with the minimum price sum.
- The first path contains nodes [0,1,2]: the prices are [1,1,1], and the sum of the prices is 3.
- The second path contains node [0] with a price [1].
The difference between the maximum and minimum price sum is 2. It can be proved that 2 is the maximum cost.
```

**Constraints**

- 1 <= n <= 105
- edges.length == n - 1
- 0 <= ai, bi <= n - 1
- edges represents a valid tree.
- price.length == n
- 1 <= price[i] <= 105

---

## 题目（中文翻译）

存在一棵无向且最初未根化的树，节点编号为 `0` 到 `n-1`。给定整数 `n` 和长度为 `n-1` 的二维整数数组 `edges`，其中 `edges[i] = [ai, bi]` 表示树中存在一条连接节点 `ai` 与 `bi` 的边。  

每个节点都有一个对应的价格，给定整数数组 `price`，其中 `price[i]` 为第 `i` 个节点的价格。  

**路径的价格和** 是指该路径上所有节点的价格之和。  

树可以任选一个节点作为根（root）。选定根后，所有**从根出发的路径**中，价格和的最大值与最小值之差即为该根的 **代价**（cost）。  
返回在所有可能的根选择中可以得到的 **最大代价**。

## 示例

### 示例 1  
**输入**  
```
n = 6
edges = [[0,1],[1,2],[1,3],[3,4],[3,5]]
price = [9,8,7,6,10,5]
```
**输出**  
```
24
```
**解释**  
上图展示了以节点 `2` 为根时的树结构。  
- 红色部分表示价格和最大的路径，该路径包含节点 `[2,1,3,4]`，对应的价格为 `[7,8,6,10]`，其和为 `31`。  
- 蓝色部分表示价格和最小的路径（示例中未完整给出），两者之差为 `24`。  

### 示例 2  
**输入**  
```
n = 3
edges = [[0,1],[1,2]]
price = [1,1,1]
```
**输出**  
```
2
```
**解释**  
上图展示了以节点 `0` 为根时的树结构。  
- 红色部分表示价格和最大的路径，路径为 `[0,1,2]`，价格和为 `3`。  
- 蓝色部分表示价格和最小的路径（示例中未完整给出），两者之差为 `2`。  

## 约束条件
- `1 <= n <= 10^5`
- `edges.length == n - 1`
- `0 <= ai, bi <= n - 1`
- `edges` 构成一棵有效的树
- `price.length == n`
- `1 <= price[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个节点都当作根**，然后分别求出：

1. 以该根为起点的所有路径的价格和（因为价格都是正数，最小路径必然是只走根本身，和就是 `price[root]`）。  
2. 在这些路径里找到最大的价格和 `maxSum(root)`。  
3. 费用 `cost(root) = maxSum(root) - price[root]`。  

把所有根的费用取最大值即为答案。

> **数据结构类比**  
> - **邻接表**：把树想成一本“通讯录”，每本子目录记录了某个人（节点）认识的所有朋友（相邻节点）。  
> - **DFS（深度优先遍历）**：像在这本通讯录里“追踪”一条从根出发的“探险路线”，把路上每个人的价格累加。

因为树是无向的，我们先任选一个节点作为临时根（比如 0），用 **DFS** 把整棵树遍历一遍，得到从该根出发的所有路径的价格和。把这个过程对每个可能的根都重复一遍，就能得到答案。

> **为什么正确**  
> 对每一个根我们都枚举了它能到达的所有节点，路径的价格和就是根到这些节点的累计价格。最大路径和一定会在这些枚举的路径中出现，所以 `maxSum(root)` 计算的是根的真实最大路径和。费用公式 `max - min` 中的最小值必然是根本身（所有价格都是正数），所以 `cost(root)` 也是准确的。

#### 代码（Python）

```python
from typing import List
import sys
sys.setrecursionlimit(10 ** 6)

def max_cost_bruteforce(n: int, edges: List[List[int]], price: List[int]) -> int:
    # 建立邻接表（通讯录）
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 对每个节点都当根，求最大路径和
    def dfs(u: int, parent: int, cur_sum: int) -> int:
        """从根 u 开始的 DFS，返回遍历到的最大累计价格和"""
        max_here = cur_sum                # 走到当前节点的累计和
        for v in g[u]:
            if v == parent:               # 不能回到已经走过的节点
                continue
            # 继续向下探索，累计价格加上子节点的 price
            max_here = max(max_here, dfs(v, u, cur_sum + price[v]))
        return max_here

    answer = 0
    for root in range(n):
        # 以 root 为根，根本身的价格就是起始累计和
        max_sum = dfs(root, -1, price[root])
        cost = max_sum - price[root]      # 最小路径和必然是根本身
        answer = max(answer, cost)

    return answer
```

> **关键行中文注释**  
> - `g = [[] for _ in range(n)]` 建立邻接表，相当于为每个人准备一个空的朋友列表。  
> - `if v == parent: continue` 防止在无向图里“来回走”。  
> - `cur_sum + price[v]` 累计路径价格，就像把路过的每个人的价格装进背包。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环遍历 `n` 个根。  
  - 每次 `dfs` 需要遍历整棵树，时间 `O(n)`。  
  - 所以总共 `n × n = n²`。  
  - **大白话**：如果树有 10⁵ 个节点，暴力解大约要跑 10¹⁰ 步，根本跑不完。

- **空间复杂度**：`O(n)`  
  - 递归栈最深会是树的高度，最坏情况下是 `n`。  
  - 邻接表也需要 `O(n)` 的存储空间。

---

### 2. 最优解

#### 思路  

暴力解慢的原因在于**每次都重新遍历整棵树**。我们其实只需要**一次遍历**就能得到每个节点作为根时的最大路径和。

观察：

1. **最小路径和**  
   价格都是正数，根到自身的路径是最短的，和就是 `price[root]`。  
   → 费用 = `maxPathSum(root) - price[root]`。

2. **最大路径和**  
   对于任意根 `r`，最大路径一定是一条从 `r` 出发、一直往下走到某个叶子的路径（叶子＝没有再往下的邻居）。  
   换句话说，**我们只需要知道每个节点到它能到达的最远叶子的价格和**，并且这条路径可以向上、向下或两边都走（因为根可以是树的任何位置）。

3. **把问题转化为“以每个节点为起点，能走到的最大累计价格”**  
   设 `best[u]` 为 **从节点 `u` 出发，沿任意方向能得到的最大价格和**（包括 `u` 本身）。  
   那么答案 = `max_u ( best[u] - price[u] )`。

4. **两次 DP（动态规划）即可求出 `best[u]`**  

   - **第一次 DFS（自底向上）** 计算 `down[u]`：  
     `down[u] = price[u] + max( 0, max_{child} down[child] )`  
     这里的 “child” 是相对于任意选的临时根（比如 0）而言的子节点。  
     `down[u]` 表示**只往子树方向**走时能够得到的最大和。

   - **第二次 DFS（自顶向下）** 计算 `up[u]`：  
     `up[u]` 表示**从 `u` 出发，必须先走到父节点，再往父节点的其他方向**（包括父节点的上层或兄弟子树）时能够得到的最大和。  
     递推公式：

     ```
     # 假设 p 是 u 的父节点
     # sibling_max = 最大的 down 值，来自除 u 之外的兄弟子树
     best_excluding_u = max( up[p], price[p] + sibling_max )
     up[u] = price[u] + best_excluding_u
     ```

     关键在于 **快速得到 sibling_max**。在第一次 DFS 时，我们为每个节点记录 **前两大的子树 down 值**，这样在遍历子节点时即可 O(1) 拿到“除当前子节点外的最大 down”。

5. **合并**  
   对每个节点 `u`，真正的 `best[u] = max(down[u], up[u])`（因为可以选择只往下走，或先往上再转向其他分支）。  
   最终答案 = `max_u ( best[u] - price[u] )`。

> **核心数据结构解释**  
> - **`down[u]`**：像把每个节点的子树装进一个背包，背包里装的价值是从该节点往下能拿到的最多价格。  
> - **`up[u]`**：把根之外的“上层世界”也装进背包，价值是从该节点往上（再可能转向兄弟子树）能拿到的最多价格。  
> - **前两大 `down`**：想象每个父节点有好几个孩子，挑出价值最高的两盒礼物，这样给任意一个孩子时，就能立刻知道“除了这盒礼物，最贵的另一盒是什么”，实现 O(1) 查询。

#### 代码（Python）

```python
from typing import List
import sys
sys.setrecursionlimit(2 * 10 ** 5)

def max_cost_optimal(n: int, edges: List[List[int]], price: List[int]) -> int:
    # ---------- 建图 ----------
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # ---------- 第一次 DFS：计算 down ----------
    down = [0] * n                 # down[u] = 最大向下路径和（包括 u）
    # 记录每个节点子树中最大的两个 down 值，方便后面求 sibling_max
    max1 = [-1] * n                # 最大的 down[child]
    max2 = [-1] * n                # 第二大的 down[child]

    def dfs_down(u: int, parent: int) -> None:
        """自底向上计算 down[u]，并记录前两大子树 down 值"""
        best = 0                   # 不选任何子树时，只保留自身 price
        for v in g[u]:
            if v == parent:
                continue
            dfs_down(v, u)         # 先算出子节点的 down
            # 子节点贡献的路径必须加上 u 本身的 price，故候选值为 down[v]
            if down[v] > best:
                best = down[v]
            # 维护前两大 down
            if down[v] > max1[u]:
                max2[u] = max1[u]
                max1[u] = down[v]
            elif down[v] > max2[u]:
                max2[u] = down[v]
        down[u] = price[u] + best   # price[u] 必须算上

    dfs_down(0, -1)                # 随便选 0 当作临时根

    # ---------- 第二次 DFS：计算 up ----------
    up = [0] * n                    # up[u] = 通过父节点向上/横向能得到的最大路径和（包括 u）

    def dfs_up(u: int, parent: int) -> None:
        """自顶向下计算 up[u]"""
        for v in g[u]:
            if v == parent:
                continue

            # 取除 v 之外的最大 sibling down
            sibling_best = max1[u] if max1[u] != down[v] else max2[u]
            # 如果没有其他兄弟（sibling_best == -1），说明只能靠父节点向上
            candidate_from_parent = up[u]                      # 走到父节点再往上
            if sibling_best != -1:
                # 走到父节点后转向兄弟子树：父节点 price + sibling_best
                candidate_from_parent = max(candidate_from_parent,
                                            price[u] + sibling_best)

            # up[v] 必须包含 v 本身的 price
            up[v] = price[v] + candidate_from_parent
            dfs_up(v, u)

    # 根节点的 up 只能是自身 price（不向上走）
    up[0] = price[0]
    dfs_up(0, -1)

    # ---------- 合并结果 ----------
    answer = 0
    for u in range(n):
        best = max(down[u], up[u])   # 从 u 出发的最大路径和
        cost = best - price[u]       # 减去最小路径（只走自己）
        answer = max(answer, cost)

    return answer
```

> **关键行中文注释**  
> - `max1`、`max2`：记录每个节点子树中最大的两条向下路径和，帮助在 `dfs_up` 时 O(1) 找到“除当前子节点外的最佳兄弟”。  
> - `candidate_from_parent = max(up[u], price[u] + sibling_best)`：从父节点出发，要么继续往上（`up[u]`），要么转向另一条子树（`price[u] + sibling_best`），取较大者。  
> - `up[v] = price[v] + candidate_from_parent`：把父节点的最佳贡献加上当前节点的价格，得到 `v` 的向上/横向最大和。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次 DFS 访问每条边一次，第二次 DFS 也只访问每条边一次。  
  - 所以总共是线性时间，**即使 n 达到 10⁵ 也能轻松跑完**。  
  - **对比暴力**：从 `n²` 降到了 `n`，快了近 `n` 倍。

- **空间复杂度**：`O(n)`  
  - 邻接表、`down`、`up`、`max1`、`max2` 各占 `O(n)`。  
  - 递归栈深度最坏是树的高度，最多 `n`，仍然在可接受范围。

---

## 心得

- **核心技巧**：**树形 DP + 换根（reroot）**。先算出“只往下走”的最优值 `down`，再通过一次自顶向下的传播得到“往上/横向”的最优值 `up`，两者合并即得每个节点作为根时的最大路径和。  
- **适用的题型**  
  1. “求每个节点为根时的最长/最大路径”——如 LeetCode 1245 `树的直径 II`、1239 `最大路径和`（变形）。  
  2. “在树上求每条边/每个节点的最优贡献”——如 2159 `树的最大得分`、2191 `树中最长的路径和`。  
- **一句话总结解题钥匙**：**一次自底向上 + 一次自顶向下的双向 DP，能把所有“根视角”的信息一次性算完**。

---

## 反思

- **第一反应**：把每个节点都枚举为根，分别跑一次 DFS。直觉上能想到，却忽视了树的结构可以让信息共享。  
- **最容易踩的坑**  
  - **忘记加上父节点的价格**：在 `up` 的递推里，`price[parent]` 必须算一次，否则会少算一层。  
  - **处理没有兄弟子树的情况**：`max2` 可能为 `-1`，需要单独判断，否则会把 `-1` 当作合法路径。  
  - **递归深度**：树可能呈链状，递归深度会达到 `n`，需要手动调高递归限制或改用显式栈。  
- **下次类似题目第一步**：先**确定一种方向的 DP（如向下）**，再思考**如何把信息从父节点“搬运”到子节点**（换根或前缀后缀技巧），往往能把 O(n²) 的暴力直接压到 O(n)。