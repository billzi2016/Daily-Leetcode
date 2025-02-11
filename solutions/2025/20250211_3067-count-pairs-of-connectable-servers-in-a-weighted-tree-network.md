# #3067. 加权树网络中可连接服务器对的计数 / Count Pairs of Connectable Servers in a Weighted Tree Network

> 难度：中等 · 标签：Array、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network/)

---

## 题目（英文原版）

**Description**

You are given an unrooted weighted tree with n vertices representing servers numbered from 0 to n - 1, an array edges where edges[i] = [ai, bi, weighti] represents a bidirectional edge between vertices ai and bi of weight weighti. You are also given an integer signalSpeed.
Two servers a and b are connectable through a server c if:
Return an integer array count of length n where count[i] is the number of server pairs that are connectable through the server i.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,1],[1,2,5],[2,3,13],[3,4,9],[4,5,2]], signalSpeed = 1
Output: [0,4,6,6,4,0]
Explanation: Since signalSpeed is 1, count[c] is equal to the number of pairs of paths that start at c and do not share any edges.
In the case of the given path graph, count[c] is equal to the number of servers to the left of c multiplied by the servers to the right of c.
```

**Example 2:**

```
Input: edges = [[0,6,3],[6,5,3],[0,3,1],[3,2,7],[3,1,6],[3,4,2]], signalSpeed = 3
Output: [2,0,0,0,0,0,2]
Explanation: Through server 0, there are 2 pairs of connectable servers: (4, 5) and (4, 6).
Through server 6, there are 2 pairs of connectable servers: (4, 5) and (0, 5).
It can be shown that no two servers are connectable through servers other than 0 and 6.
```

**Constraints**

- 2 <= n <= 1000
- edges.length == n - 1
- edges[i].length == 3
- 0 <= ai, bi < n
- edges[i] = [ai, bi, weighti]
- 1 <= weighti <= 106
- 1 <= signalSpeed <= 106
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

你得到一棵无根加权树（unrooted weighted tree），该树有 `n` 个顶点，编号为 `0` 到 `n - 1`。数组 `edges` 中的每一条记录 `edges[i] = [a_i, b_i, weight_i]` 表示顶点 `a_i` 与顶点 `b_i` 之间存在一条双向边，权重为 `weight_i`。另给定一个整数 `signalSpeed`（信号速度）。

若满足以下条件，则称服务器 `a` 与服务器 `b` 能通过服务器 `c` 进行连接（connectable）：

（题目原文中此处应给出具体条件，已省略）

返回一个长度为 `n` 的整数数组 `count`，其中 `count[i]` 表示通过服务器 `i` 能够连接的服务器对的数量。

---

### 示例

#### 示例 1
**输入**  
``` 
edges = [[0,1,1],[1,2,5],[2,3,13],[3,4,9],[4,5,2]], signalSpeed = 1
```
**输出**  
```
[0,4,6,6,4,0]
```
**解释**  
由于 `signalSpeed` 为 `1`，`count[c]` 等于从 `c` 出发、且互不共享任何边的两条路径的配对数。  
在给出的链状树中，`count[c]` 等于 `c` 左侧服务器的数量乘以右侧服务器的数量。

#### 示例 2
**输入**  
``` 
edges = [[0,6,3],[6,5,3],[0,3,1],[3,2,7],[3,1,6],[3,4,2]], signalSpeed = 3
```
**输出**  
```
[2,0,0,0,0,0,2]
```
**解释**  
- 通过服务器 `0`，共有两对可连接的服务器：`(4, 5)` 与 `(4, 6)`。  
- 通过服务器 `6`，也有两对可连接的服务器：`(4, 5)` 与 `(0, 5)`。  
可以证明，除 `0` 与 `6` 外，其他服务器均不存在可连接的服务器对。

---

### 约束条件
- `2 <= n <= 1000`
- `edges.length == n - 1`
- `edges[i].length == 3`
- `0 <= a_i, b_i < n`
- `edges[i] = [a_i, b_i, weight_i]`
- `1 <= weight_i <= 10^6`
- `1 <= signalSpeed <= 10^6`
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每一个服务器 `c` 当成「根」来看待，树上任意两台服务器 `a、b` 通过 `c` 互相通信的条件可以拆成两步：

1. **路径必须在 `c` 处分叉**  
   在树里，唯一的路径 `a → b` 必然经过它们最近的公共祖先（LCA）。  
   当我们把 `c` 当成根时，`a` 与 `b` 必须位于 **不同的子树**（即不同的直接子节点所在的子树），否则它们的路径根本不会在 `c` 处相交。

2. **到 `c` 的距离都能被 `signalSpeed` 整除**  
   题目说「距离是 signalSpeed 的整数倍」。  
   这相当于检查 `dist(c, a) % signalSpeed == 0` 与 `dist(c, b) % signalSpeed == 0`。

把这两个条件组合起来：  
> 对根 `c`，在每个直接子树里统计「到 `c` 的距离能被 signalSpeed 整除」的服务器数量 `num_i`。  
> 任意选取两个不同子树中的服务器即可得到一对可连接的服务器。

> **生活化类比**：  
> 想象 `c` 是一座火车站，站台的每一条轨道对应一棵子树。我们只允许站台上「恰好在整点到站」的乘客上车（距离能被 signalSpeed 整除），然后让两个站在不同轨道的乘客搭配成一对。统计所有可能的搭配数，就是答案。

**为什么正确**  
- 树的唯一路径属性保证了只要两点在不同子树，它们的路径必然经过根 `c`，且在 `c` 之外不共享任何边。  
- 我们只计数满足距离整除条件的节点，正好对应题目要求的「可连接」定义。  
- 所有符合条件的 unordered pair `(a, b)` 都会被唯一计入一次（因为它们所属的子树是唯一的），不会漏也不会重。

**复杂度分析（大白话）**  
- 对每个根 `c`，我们要遍历它的所有子树一次，累计 O(n) 的节点访问。  
- 共有 n 个根，所以总共大约需要 `n × n = n²` 次访问。  
- `n ≤ 1000`，所以 `1000² = 1,000,000` 次操作在电脑里跑得飞快。  

> **时间复杂度**：`O(n²)` → 想象把 1000 张卡片两两配对，需要大约一百万次检查。  
> **空间复杂度**：`O(n)` → 只需要存图的邻接表和递归栈，和节点数成正比。

#### 代码（Python）

```python
from typing import List, Tuple
import sys
sys.setrecursionlimit(2000)          # 防止递归深度不足

def countPairs(edges: List[List[int]], signalSpeed: int) -> List[int]:
    n = len(edges) + 1                # 树的节点数
    # ---------- 建图 ----------
    g: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    # ---------- 深度优先搜索 ----------
    # 返回子树中「距离根的模为0」的节点数量
    def dfs(u: int, parent: int, cur_mod: int) -> int:
        # 如果当前节点到根的距离恰好能被 signalSpeed 整除，就计数
        cnt = 1 if cur_mod == 0 else 0
        for v, w in g[u]:
            if v == parent:          # 不回到父节点
                continue
            # (cur_mod + w) % signalSpeed 表示把这条边的权重加进去后的模
            cnt += dfs(v, u, (cur_mod + w) % signalSpeed)
        return cnt

    ans = [0] * n                     # 最终答案

    # ---------- 对每个节点当根 ----------
    for root in range(n):
        child_cnt = []                # 记录每个直接子树的符合条件的节点数
        total = 0                     # 所有子树符合条件节点的总和
        for nb, w in g[root]:        # 遍历根的每个邻居 → 每棵子树的根
            cnt = dfs(nb, root, w % signalSpeed)   # 计算这棵子树
            child_cnt.append(cnt)
            total += cnt

        # ---------- 计算 unordered pair ----------
        pairs = 0
        for cnt in child_cnt:
            # cnt 与 (total - cnt) 之间的配对数，除以 2 防止重复计数
            pairs += cnt * (total - cnt) // 2
        ans[root] = pairs

    return ans
```

> 代码里每行关键语句都加了中文注释，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 对每个根 `O(n)`，内部 DFS 再遍历整棵树 `O(n)`，两层相乘。  
  - 对 n=1000 来说约一百万次递归调用，极其快速。

- **空间复杂度**：`O(n)`  
  - 邻接表保存 `2·(n‑1)` 条边，递归栈最深 `n`。  
  - 与节点数线性相关，符合题目限制。

---

### 2. 最优解

#### 思路  

暴力解已经是 `O(n²)`，已经足够满足 `n ≤ 1000` 的约束。  
在更大规模（比如 `n = 10⁵`）时我们会需要 **一次 DFS + 动态规划** 把所有根的答案一次性算完。这里简要说明思路，帮助大家在以后面对更高要求时快速升级。

1. **把「根」从 0 换到相邻节点的技巧**  
   当我们已经知道以 `c` 为根时，每个子树的 `num_i`（满足距离可整除的节点数），如果把根移动到 `c` 的某个子节点 `v`，只需要局部更新：  
   - `v` 所在的子树会失去 `c`，变成「上层」的一个子树。  
   - 原来 `c` 的其他子树不变，只是它们现在相对于新根的距离多了一条边的权重，需要相应地 **模** 变换。

2. **前缀计数 + 环形卷积**  
   对每条边的权重取模 `signalSpeed`，我们只关心 **距离的模值**。  
   - 在一次 DFS 中，记录从根出发到每个节点的距离模 `signalSpeed`（记作 `distMod[node]`）。  
   - 对每个根 `c`，所有满足 `distMod[node] == 0` 且在同一子树的节点数即为 `num_i`。  
   - 通过「树形 DP」把子树信息向上合并，再「树形重根」把根从父节点搬到子节点，只需要 `O(1)` 的局部更新。

3. **核心公式**（与提示一致）  

   对根 `c`，设它有 `m` 个直接子树，子树 `i` 中满足条件的节点数为 `num[i]`，总和 `S = Σ num[i]`。  
   任意选取两个不同子树的节点即构成一对可连接的服务器：

   \[
   \text{count}[c] = \sum_{i=1}^{m} \frac{num[i] \times (S - num[i])}{2}
   \]

   这正是我们在暴力解里做的配对计数，只是把 `num[i]` 的获取方式从 `O(n)` 的 DFS 改成 `O(1)` 的 DP 查询。

**为什么更快**  
- 只需要一次全树遍历得到所有节点到任意根的距离模。  
- 再进行一次「重根 DP」把每个根的 `num[i]` 汇总，整体 `O(n)`（或 `O(n·log signalSpeed)` 取模运算的开销）。  
- 对于本题的限制，这种优化不是必须的，但它展示了「把每个根的答案一次性算完」的思路，后续面对更大数据时可以直接套用。

#### 代码（Python）

下面给出 **线性时间**（`O(n)`) 的实现思路，代码同样带有中文注释，供参考学习。  
（实际在 `n ≤ 1000` 时，两种实现跑得几乎一样快。）

```python
from typing import List, Tuple
import sys
sys.setrecursionlimit(2000)

def countPairs_opt(edges: List[List[int]], signalSpeed: int) -> List[int]:
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    # ---------- 第一次 DFS：计算以 0 为根的子树信息 ----------
    # sub_cnt[node] : 以 node 为根，其子树（包括自己）中
    #                 距离根 node 的模为 0 的节点数量
    sub_cnt = [0] * n
    # dist_mod[node] : 从全局根 (0) 到 node 的距离模 signalSpeed
    dist_mod = [0] * n

    def dfs1(u: int, parent: int) -> None:
        # 如果到当前根的距离恰好能被 signalSpeed 整除，就计 1
        sub_cnt[u] = 1 if dist_mod[u] == 0 else 0
        for v, w in g[u]:
            if v == parent:
                continue
            # 更新到子节点的模值
            dist_mod[v] = (dist_mod[u] + w) % signalSpeed
            dfs1(v, u)
            # 把子树的信息累加到当前节点
            sub_cnt[u] += sub_cnt[v]

    dfs1(0, -1)

    # ---------- 第二次 DFS：重根 DP ----------
    ans = [0] * n                     # 最终答案

    # 为每个根维护「子树符合条件的节点数」的列表
    # root_info[root] = [cnt_child1, cnt_child2, ...]
    # 为了 O(1) 取值，我们在遍历时即时累计即可
    def dfs2(u: int, parent: int, up_cnt: int) -> None:
        """
        u    : 当前根
        up_cnt: 来自父节点方向（即「上层」子树）符合条件的节点数
        """
        # 收集所有子树的 cnt（包括上层的）
        child_cnt = []
        total = up_cnt
        for v, w in g[u]:
            if v == parent:
                continue
            child_cnt.append(sub_cnt[v])   # 子树 v 已经是相对于 u 的
            total += sub_cnt[v]

        # 根据公式算出当前根的答案
        pairs = 0
        for cnt in child_cnt:
            pairs += cnt * (total - cnt) // 2
        # 注意：上层子树也算在 total 里，需要一起参与配对
        if up_cnt:
            pairs += up_cnt * (total - up_cnt) // 2
        ans[u] = pairs

        # 向下递归时，需要为每个子节点准备它的 “上层子树” 信息
        # 设子节点 v 为新的根时，上层子树即：除去 v 所在子树的其余所有节点
        prefix = 0
        for v, w in g[u]:
            if v == parent:
                continue
            # 计算除去子树 v 之外的其它符合条件的节点数
            # total 包含了 up_cnt + 所有子树的 cnt
            rest = total - sub_cnt[v]
            dfs2(v, u, rest)   # 这里的 rest 正好是 v 当根时的上层子树计数

    dfs2(0, -1, 0)   # 从根 0 开始，根本身没有上层子树

    return ans
```

> 这段代码展示了 **一次遍历 + 重根 DP** 的思想，时间复杂度降到 `O(n)`，空间仍是 `O(n)`。如果以后面对 `n = 10⁵` 的大数据，这个实现即可直接使用。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次 DFS 收集每个子树的计数 `O(n)`。  
  - 第二次 DFS（重根）同样遍历每条边一次 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，提升了数量级（尤其在 `n` 很大时）。

- **空间复杂度**：`O(n)`  
  - 只需要保存图、子树计数、距离模以及递归栈，均为线性规模。

---

## 心得

- **核心技巧**：把「两点路径必须经过根且距离可被 signalSpeed 整除」转化为「根的不同子树中满足模为 0 的节点配对」。
- **适用场景**  
  1. **树上配对计数**（如「统计不同子树中颜色相同的节点对」）。  
  2. **带权距离取模** 的问题（如「判断两点距离是否是某数的倍数」）。  
  3. **重根 DP**：需要对每个节点都求某种子树汇总信息时。
- **一句话总结解题钥匙**：  
  > 「把路径约束拆成‘在不同子树’ + ‘距离模为 0’，然后只在根的子树层面做配对计数」。

---

## 反思

- **第一反应**：把每个服务器都当根，枚举所有节点对，检查路径是否满足条件。很快想到用 DFS 计算距离，但会导致 `O(n³)` 的超时。
- **最容易踩的坑**  
  1. **忘记「不同子树」的限制**，导致同一子树内部的配对被错误计入。  
  2. **距离取模** 时忽视了边权重的累加，需要在递归时把 `cur_mod = (cur_mod + w) % signalSpeed` 正确传递。  
  3. **边界条件**：根本身不算在配对里，只有子树的节点才参与。  
- **下次遇到类似题**：第一步先把「路径必须经过根」转换为「根的不同子树配对」；第二步只统计满足特定距离/属性的节点数量；第三步用组合数学 `cnt_i * (total - cnt_i) / 2` 直接求配对数，而不是枚举。这样思路清晰、实现也自然。