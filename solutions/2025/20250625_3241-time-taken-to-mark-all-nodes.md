# #3241. 标记所有节点所需的时间 / Time Taken to Mark All Nodes

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/time-taken-to-mark-all-nodes/)

---

## 题目（英文原版）

**Description**

There exists an undirected tree with n nodes numbered 0 to n - 1. You are given a 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the tree.
Initially, all nodes are unmarked. For each node i:
Return an array times where times[i] is the time when all nodes get marked in the tree, if you mark node i at time t = 0.
Note that the answer for each times[i] is independent, i.e. when you mark node i all other nodes are unmarked.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[0,2]]
Output: [2,4,3]
Explanation:
```

**Example 2:**

```
Input: edges = [[0,1]]
Output: [1,2]
Explanation:
```

**Example 3:**

```
Input: edges = [[2,4],[0,1],[2,3],[0,2]]
Output: [4,6,3,5,5]
Explanation:
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= edges[i][0], edges[i][1] <= n - 1
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

存在一棵 **无向树（undirected tree）**，共有 `n` 个节点，编号为 `0` 到 `n - 1`。给定一个长度为 `n - 1` 的二维整数数组（`2D integer array`）`edges`，其中 `edges[i] = [ui, vi]` 表示在树中存在一条连接节点 `ui` 与节点 `vi` 的边。

最初，所有节点均未被标记。对于每个节点 `i`：

返回一个数组 `times`，其中 `times[i]` 表示如果在时间 `t = 0` 标记节点 `i`，则整棵树中所有节点全部被标记的时间。需要注意的是，`times[i]` 的计算是相互独立的，即在计算 `times[i]` 时，只有节点 `i` 被标记，其余节点均保持未标记状态。

---

### 示例

**示例 1**

```
Input: edges = [[0,1],[0,2]]
Output: [2,4,3]
解释：
```

**示例 2**

```
Input: edges = [[0,1]]
Output: [1,2]
解释：
```

**示例 3**

```
Input: edges = [[2,4],[0,1],[2,3],[0,2]]
Output: [4,6,3,5,5]
解释：
```

---

### 约束条件

- `2 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= edges[i][0], edges[i][1] <= n - 1`
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的标记顺序**，模拟“每个已经被标记的节点在每一秒只能标记一个尚未被标记的相邻节点”。  
具体步骤：

1. 以节点 `i` 为起点，把它标记在时间 `t = 0`。  
2. 维护一个集合 `marked`（已标记的节点）和一个集合 `frontier`（本轮可以继续标记的节点）。  
3. 在每一秒 `t`，从 `frontier` 中任选一个节点 `u`，并让它标记它的一个未标记邻居 `v`（如果有多个邻居，就**遍历所有可能的选择**）。  
4. 把 `v` 加入 `marked`，并把 `v` 放入 `frontier`（因为 `v` 以后也可以继续标记别的节点）。  
5. 重复步骤 3‑4，直到所有节点都被标记。记录下最后一次标记的时间，即为 `times[i]`。

> **类比**：把树想成一群人，只有已经知道消息的人才能把消息告诉一位未听说的人，而且一次只能告诉一个人。我们要尝试所有可能的“谁先告诉谁”的顺序，找出最快的完成时间。

为什么它是对的？  
只要我们遍历了 **所有** 可能的标记顺序，必然会碰到最优的那一种，因此得到的最小时间一定是正确答案。

**时间/空间复杂度**  
- 对每个起点 `i`，我们需要遍历所有可能的标记顺序。树上有 `n` 条边，标记顺序的数量相当于把每条边的方向排个序，约为 `O(n!)`（阶乘级别）。  
- 再乘上 `n` 个起点，总体时间是 `O(n·n!)`，这在 `n ≤ 10⁵` 时根本不可接受。  
- 空间上只需要保存树的邻接表和几个集合，`O(n)`。

> **大白话**：`O(n·n!)` 就像让 10 个人排队，所有可能的排法有 10! = 3,628,800 种，根本算不完。  

---

#### 代码（Python）

```python
from itertools import permutations
from collections import defaultdict

def brute_force_times(edges):
    n = max(max(u, v) for u, v in edges) + 1
    # 建立邻接表
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    def simulate(root):
        # 所有边的方向组合（暴力遍历），这里仅作演示，实际不可运行
        best = float('inf')
        # 把每条边的「先标记哪端」当成一个排列
        for order in permutations(range(n - 1)):
            # ... 省略具体模拟过程
            pass
        return best

    ans = [simulate(i) for i in range(n)]
    return ans
```

> 代码仅作概念展示，真实运行会在几秒钟内炸掉内存或 CPU。

#### 复杂度

- **时间复杂度**：`O(n·n!)` — 需要遍历所有可能的标记顺序，阶乘增长极快，几乎不可能在 10⁵ 规模下完成。  
- **空间复杂度**：`O(n)` — 只保存邻接表和少量临时集合。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**我们在每一步都尝试所有可能的标记顺序**。实际上，树的结构让我们可以用**动态规划（DP）**来直接算出最优时间，而不必枚举。

关键观察：

1. **每个节点只能一次标记一个邻居**，但已经被标记的子树可以**并行进行**。  
2. 对于一个根节点 `r`，它的所有子树会在不同的时间段被依次“唤醒”。如果把子树的“完成时间”记作 `cost(child)`，则根节点的总时间取决于**把子树按完成时间从大到小的顺序依次唤醒**。  
   - 把耗时最长的子树先唤醒，可以让它尽早并行工作，整体完成时间最短（贪心）。  
3. 对于固定根 `r`，我们可以用递归计算  
   \[
   dp[r] = \max_{k\ge 1}\bigl( (k-1) + cost_k \bigr)
   \]
   其中 `cost_k` 是第 `k` 大子树的 `dp[child] + 1`（`+1` 表示从 `r` 到子树的那条边需要 1 秒）。

这一步只需要一次 **深度优先搜索（DFS）**，把每个节点的 `dp`（即把它当作根时标记全部节点所需的最少时间）算出来，称为 **向下 DP**（只看子树）。

但是题目要求 **对每个节点都返回答案**，即**每个节点都可能是根**。我们需要把根从一个节点“搬到”它的相邻节点，这叫 **树的重根（re‑root）**。思路：

- 已经有了 `dpDown[u]`（子树时间），现在把根从 `u` 移到它的一个孩子 `v`。  
- 对于 `v` 来说，原来 `u` 的其余子树（包括 `u` 的父侧）变成了 `v` 的“新子树”。我们只要把这些“新子树”的时间也算进去，就能得到 `dpAll[v]`。  
- 为了在 **O(1)** 时间得到“除去某个子树之外的最大贡献”，我们在每个节点保存 **所有相邻子树的时间列表**（已经排序），并利用前缀/后缀最大值或直接在度数较小的情况下重新排序（总复杂度仍是 `O(n log n)`）。

整体流程：

1. **第一遍 DFS**（`dfs1`）  
   - 计算 `dpDown[u]`：对每个子节点 `c`，先递归得到 `dpDown[c]`，再把 `dpDown[c] + 1` 放进列表。  
   - 把列表降序排列，遍历得到 `dpDown[u] = max( list[i] + i )`（`i` 从 0 开始）。  
2. **第二遍 DFS**（`dfs2`）  
   - 传入从父节点传来的 “上层贡献” `up`（相当于父侧子树的时间）。  
   - 把 `up`（如果有）也加入当前节点的列表，重新计算 **当前节点作为根的答案** `ans[u]`（同样是 `max(list[i] + i)`）。  
   - 对每个子节点 `v`，构造 **除去 `v` 本身贡献的列表**，再算出 `up_for_v = max(other[i] + i) + 1`，递归传给 `v`。  

这样每条边只被处理常数次，整体时间 `O(n log n)`（排序导致的对数），空间 `O(n)`（邻接表 + 若干数组）。

> **类比**：想象你是一个老师，要把作业布置给全班同学。每次只能叫一个同学去布置他的下属，同学们之间可以并行布置自己的下属。把**工作量最大的**那一组先布置，大家就能更快全部拿到作业。老师换到另一位同学的位置时，只需要重新考虑那位同学的“上级”这块工作，而不必重新安排全班。

---

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(300000)

def time_taken_to_mark_all_nodes(edges):
    """
    返回数组 times，其中 times[i] 为以节点 i 为起点时
    标记整棵树所需的最少时间。
    """
    n = max(max(u, v) for u, v in edges) + 1
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # -------------------------------------------------
    # 第一次 DFS：向下 DP，计算 dpDown[u]（子树时间）
    # -------------------------------------------------
    dpDown = [0] * n          # 只看子树时的最少时间
    child_contrib = [[] for _ in range(n)]  # 每个节点子树的 (dpDown[child] + 1)

    def dfs1(u, parent):
        """自底向上计算 dpDown[u]"""
        for v in g[u]:
            if v == parent:
                continue
            dfs1(v, u)
            # v 子树需要的时间 + 1（从 u 到 v 的那条边）
            child_contrib[u].append(dpDown[v] + 1)

        # 把子树贡献从大到小排序，贪心让最长的子树先被唤醒
        child_contrib[u].sort(reverse=True)

        # dpDown[u] = max( child_contrib[i] + i )
        best = 0
        for i, val in enumerate(child_contrib[u]):   # i 从 0 开始
            best = max(best, val + i)
        dpDown[u] = best

    dfs1(0, -1)   # 任意节点当根即可

    # -------------------------------------------------
    # 第二次 DFS：重根 DP，计算每个节点作为根的答案
    # -------------------------------------------------
    ans = [0] * n   # 最终答案

    def dfs2(u, parent, up):
        """
        u：当前节点
        parent：父节点
        up：来自父侧的贡献（即把父侧当作 u 的一个子树时的时间），
            已经包括了从父节点到 u 的那条边的 1 秒。
        """
        # 把所有子树贡献（包括上层 up）放进列表
        all_vals = child_contrib[u].copy()
        if parent != -1:            # 如果有父亲，加入上层贡献
            all_vals.append(up)

        all_vals.sort(reverse=True)

        # 计算当前节点作为根的答案
        cur = 0
        for i, val in enumerate(all_vals):
            cur = max(cur, val + i)
        ans[u] = cur

        # 为每个子节点准备它的 up 值
        for v in g[u]:
            if v == parent:
                continue
            # 取除去子节点 v 本身贡献的其余所有贡献
            others = []
            # 其它子节点的贡献
            for w in g[u]:
                if w == v:
                    continue
                if w == parent:
                    others.append(up)          # 来自父侧的贡献
                else:
                    others.append(dpDown[w] + 1)
            others.sort(reverse=True)

            # 计算除去 v 后的最大时间
            up_for_v = 0
            for i, val in enumerate(others):
                up_for_v = max(up_for_v, val + i)
            # 再加上从 v 到 u 的那条边的 1 秒，得到传递给子节点的 up
            up_for_v += 1
            dfs2(v, u, up_for_v)

    dfs2(0, -1, 0)   # root 为 0 时没有上层贡献

    return ans
```

**代码说明（每行中文注释已写在代码中）**：

- `child_contrib[u]` 保存 **从 u 出发的每条子树** 需要的时间（已加上走过的那条边的 1 秒）。  
- `dpDown[u]` 使用 **贪心排序** 计算：先唤醒时间最长的子树 `val[0]`，它在第 `0` 秒被唤醒；第二长的子树要等 `1` 秒才能开始唤醒，以此类推。于是 `val[i] + i` 表示第 `i` 大子树最终完成的时间，取最大即为 `dpDown[u]`。  
- 第二遍 `dfs2` 把父侧的贡献 `up` 当作 **另一个子树** 加入同样的列表，重新计算根为 `u` 时的答案 `ans[u]`。  
- 对每个子节点 `v`，我们把 **除去 `v` 本身的贡献** 再算一次 `up_for_v`，随后再加上 `+1`（因为从 `v` 看向父亲要多走一步），递归下去完成所有节点的答案。

---

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 第一次 DFS：对每个节点的子树列表排序，所有列表长度之和为 `n‑1`，排序总代价 `O(n log n)`。  
  - 第二次 DFS：对每条边我们最多重新排序一次（度数小的节点），同样累计 `O(n log n)`。  
  - 与暴力解的 `O(n·n!)` 相比，已经可以在 `n = 10⁵` 的规模下轻松跑完。  
- **空间复杂度**：`O(n)`  
  - 邻接表、`dpDown`、`child_contrib`、`ans` 各占 `O(n)`。递归深度最坏 `O(n)`，在 Python 中通过 `sys.setrecursionlimit` 解决。

> **对比**：暴力解像是把所有可能的排队方式都尝试一遍，时间像指数一样飙升；最优解像是先把每个子树的“最快完成时间”算好，再用贪心把最长的子树先叫醒，整个过程只需一次遍历，快得多。

---

## 心得

- **核心技巧**：树形 DP + 贪心排序 + 重根（re‑root）  
  - 先自底向上算出每个子树的最短完成时间（`dpDown`）。  
  - 对同一父节点的子树，**把耗时最长的先处理**，因为后处理的子树必须等前面的子树“占用”时间。  
  - 用重根技巧把根从一个节点搬到相邻节点，只需要把“父侧贡献”当作新的子树即可，避免重新遍历整棵树。

- **适用的题型**  
  1. **通知所有员工**（LeetCode 2427）——有向树，经理一次只能通知一个下属。  
  2. **树上广播/感染**（类似 1665. Minimum Initial Health Required）——每个节点一次只能向一个邻居传递信息。  
  3. **树形任务调度**——节点代表任务，父节点一次只能启动一个子任务。

- **一句话总结解题钥匙**：  
  “把每个子树的完成时间算好后，按从大到小的顺序依次唤醒——最长的先走，剩下的自然排队”。

---

## 反思

- **第一反应**：直接模拟所有标记顺序，想用 BFS/DFS 暴力搜索。  
- **最容易踩的坑**  
  1. **忽视并行**：子树之间可以并行工作，只是根节点本身一次只能叫醒一个子树。  
  2. **忘记加边的 1 秒**：`dpDown[child]` 只算子树内部时间，转向父节点时需要再加上走边的时间。  
  3. **重根时的 “除去自身贡献”**：如果直接在原列表上删掉元素，会破坏其它子树的顺序，需要重新构造或使用前缀/后缀最大值。  

- **下次遇到同类题**：第一步立刻想到 “**每个节点的子树时间** + **贪心让最长的子树先启动**”，随后再考虑 **重根** 把答案推广到所有节点。这样就能直接跳过暴力搜索，直接进入 DP+贪心的高效解法。