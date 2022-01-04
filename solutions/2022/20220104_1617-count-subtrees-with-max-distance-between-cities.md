# #1617. 统计子树中城市间最大距离 / Count Subtrees With Max Distance Between Cities

> 难度：困难 · 标签：Dynamic Programming、Bit Manipulation、Tree、Enumeration、Bitmask · [LeetCode 链接](https://leetcode.com/problems/count-subtrees-with-max-distance-between-cities/)

---

## 题目（英文原版）

**Description**

There are n cities numbered from 1 to n. You are given an array edges of size n-1, where edges[i] = [ui, vi] represents a bidirectional edge between cities ui and vi. There exists a unique path between each pair of cities. In other words, the cities form a tree.
A subtree is a subset of cities where every city is reachable from every other city in the subset, where the path between each pair passes through only the cities from the subset. Two subtrees are different if there is a city in one subtree that is not present in the other.
For each d from 1 to n-1, find the number of subtrees in which the maximum distance between any two cities in the subtree is equal to d.
Return an array of size n-1 where the dth element (1-indexed) is the number of subtrees in which the maximum distance between any two cities is equal to d.
Notice that the distance between the two cities is the number of edges in the path between them.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[1,2],[2,3],[2,4]]
Output: [3,4,0]
Explanation:
The subtrees with subsets {1,2}, {2,3} and {2,4} have a max distance of 1.
The subtrees with subsets {1,2,3}, {1,2,4}, {2,3,4} and {1,2,3,4} have a max distance of 2.
No subtree has two nodes where the max distance between them is 3.
```

**Example 2:**

```
Input: n = 2, edges = [[1,2]]
Output: [1]
```

**Example 3:**

```
Input: n = 3, edges = [[1,2],[2,3]]
Output: [2,1]
```

**Constraints**

- 2 <= n <= 15
- edges.length == n-1
- edges[i].length == 2
- 1 <= ui, vi <= n
- All pairs (ui, vi) are distinct.

---

## 题目（中文翻译）

给定 $n$ 个城市，编号为 1 到 $n$。你会得到一个大小为 $n-1$ 的数组 `edges`，其中 `edges[i] = [u_i, v_i]` 表示城市 `u_i` 和城市 `v_i` 之间有一条双向边（edge）。任意两座城市之间恰好存在唯一的一条路径，也就是说，这些城市构成了一棵树（tree）。

子树（subtree）是指一个城市子集，使得子集中任意两座城市之间都能相互到达，且它们之间的路径仅经过子集中的城市。若两个子树中存在某座城市只出现在其中一个子树，则这两个子树视为不同。

对于每个 $d$（$1 \le d \le n-1$），求满足子树中任意两座城市的最大距离（即路径上的边数）恰好等于 $d$ 的子树的数量。

返回一个大小为 $n-1$ 的数组，其中第 $d$ 个元素（下标从 1 开始）即为最大距离等于 $d$ 的子树数量。

> 注意：两座城市之间的距离定义为它们之间路径上的边的条数。

### 示例

**示例 1**

```
输入: n = 4, edges = [[1,2],[2,3],[2,4]]
输出: [3,4,0]
解释:
- 子树 {1,2}、{2,3}、{2,4} 的最大距离均为 1。
- 子树 {1,2,3}、{1,2,4}、{2,3,4}、{1,2,3,4} 的最大距离均为 2。
- 没有子树的最大距离为 3。
```

**示例 2**

```
输入: n = 2, edges = [[1,2]]
输出: [1]
解释:
唯一的子树 {1,2} 的最大距离为 1。
```

**示例 3**

```
输入: n = 3, edges = [[1,2],[2,3]]
输出: [2,1]
解释:
- 子树 {1,2}、{2,3} 的最大距离为 1。
- 子树 {1,2,3} 的最大距离为 2。
```

### 约束条件

- $2 \le n \le 15$
- `edges.length == n-1`
- `edges[i].length == 2`
- $1 \le u_i, v_i \le n$
- 所有的 $(u_i, v_i)$ 对均不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

因为 `n ≤ 15`，所有城市的子集最多只有 `2^15 = 32768` 种。  
我们可以**枚举每一种子集**（用一个二进制掩码 `mask` 表示），然后判断：

1. **这是不是一个合法的子树**  
   - 子树的定义：子集里的每个城市都能互相到达，且走的路径只能经过子集里的城市。  
   - 把子集看成一张只保留子集内部边的“小图”。如果从子集中任意一个城市出发，沿着这张小图走，能走到的城市数恰好等于子集的大小（即 `mask` 中 `1` 的个数），说明这张小图是连通的，也就是合法的子树。  
   - 检查连通性可以用 **BFS / DFS**，就像在现实中从一座城出发，沿着只在子集里出现的道路走，看能否走遍所有选中的城。

2. **求出这棵子树的直径（最大距离）**  
   - 直径是子树中任意两点之间最远的距离（边的条数）。  
   - 在树里求直径的常用技巧是“**两次 BFS**”：
     1. 任意选一个节点 `s`，做一次 BFS，找到离 `s` 最远的节点 `a`。  
     2. 再从 `a` 出发 BFS，得到的最远距离就是整棵树的直径。  
   - 这里我们只在子集内部的边上走，同样可以得到子树的直径。

3. **把子树计入答案**  
   - 直径得到后，`ans[diameter] += 1`（注意答案数组是 1‑indexed，`ans[1]` 对应距离为 1 的子树数）。

把所有 `mask` 都跑完，就得到每个可能的最大距离对应的子树数量。

---

#### 代码（Python）

```python
from collections import deque
from typing import List

def countSubgraphsForEachDiameter(n: int, edges: List[List[int]]) -> List[int]:
    # 把无向树转成邻接表，方便遍历
    g = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1          # 变成 0-index
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # ans[d] 统计直径恰好等于 d 的子树个数，d 的取值范围是 1~n-1
    ans = [0] * (n - 1)

    # ---------- 1. 枚举所有非空子集 ----------
    for mask in range(1, 1 << n):               # 1~2^n-1
        # 取子集里任意一个点做起点
        start = (mask & -mask).bit_length() - 1   # 最低位 1 所在的下标

        # ---------- 2. 检查连通性 ----------
        # BFS 只走子集内部的边
        q = deque([start])
        seen = 0                                 # 已访问的子集节点数（用 bitmask 计数）
        visited_mask = 0
        while q:
            cur = q.popleft()
            visited_mask |= 1 << cur
            for nb in g[cur]:
                if (mask >> nb) & 1 and not (visited_mask >> nb) & 1:
                    q.append(nb)

        if visited_mask != mask:                 # 不是连通的，直接跳过
            continue

        # ---------- 3. 计算子树直径 ----------
        # 第一次 BFS：找最远节点 a
        def bfs(src: int) -> (int, int):
            dq = deque([src])
            dist = [-1] * n
            dist[src] = 0
            far_node, far_dist = src, 0
            while dq:
                u = dq.popleft()
                for v in g[u]:
                    if (mask >> v) & 1 and dist[v] == -1:   # 只在子集内部走
                        dist[v] = dist[u] + 1
                        dq.append(v)
                        if dist[v] > far_dist:
                            far_dist = dist[v]
                            far_node = v
            return far_node, far_dist

        a, _ = bfs(start)            # 任意点 -> 最远点 a
        _, diam = bfs(a)             # a -> 再找最远点，得到直径

        # ---------- 4. 计入答案 ----------
        if diam > 0:                  # 直径为 0 的情况只会出现在只有一个节点的子树，题目要求 d ≥ 1
            ans[diam - 1] += 1

    return ans
```

> **代码要点注释**  
> - `mask & -mask` 取出最低位的 `1`，再用 `bit_length()` 得到对应的城市编号（0‑index）。这相当于“从子集中随手挑一个城”。  
> - `visited_mask` 用 **位运算** 记录已经走过的城市，省去额外的 `visited` 数组。  
> - `bfs` 函数内部的 `dist` 数组只在子集内部更新，保证不会走出子树。

---

#### 复杂度

- **时间复杂度**：`O( 2^n * n )`  
  - 枚举子集有 `2^n` 种。  
  - 对每个合法子集我们会跑两次 BFS，最坏情况下每次遍历所有 `n` 条边（因为 `n ≤ 15`，边数≈节点数），所以每个子集的代价是 `O(n)`。  
  - 用大白话说：如果 `n = 15`，最多约 `32768 * 15 ≈ 5×10^5` 次基本操作，完全可以在毫秒级跑完。

- **空间复杂度**：`O(n)`  
  - 主要是邻接表 `g`、BFS 队列和 `dist` 数组，都是和节点数线性相关的。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个子集都要重新跑两次 BFS**，虽然对 `n ≤ 15` 已经足够快，但我们可以把“求直径”这一步 **提前算好**，让每个子集只需要 *查表* 就能得到答案。  

核心思路是 **树上 DP + 位掩码**：

1. **根树**  
   - 任意选一个节点作为根（比如 0），把树变成“父子关系”。  
   - 这样每条边都会指向子节点，便于自底向上合并子树信息。

2. **状态定义**  
   - `dp[v][mask] = (size, height, diam)`：以节点 `v` 为根、包含的节点集合恰好是 `mask`（`mask` 只在 `v` 的子树范围内）的子树信息。  
   - `size`：子树节点数（其实等于 `mask` 中 `1` 的个数），  
   - `height`：从根 `v` 出发到子树中最远节点的距离，  
   - `diam`：该子树的直径（最大距离）。  

3. **初始化**  
   - 只包含根节点本身的子集 `mask = 1 << v`，此时 `size = 1`，`height = 0`，`diam = 0`。

4. **子树合并（背包合并）**  
   - 对于每个节点 `v`，遍历它的子节点 `c`。  
   - 子节点已经算好了 `dp[c][submask]`（自底向上），我们要把子节点的子集 **并入** `v` 的子集。  
   - 合并过程类似 **0/1 背包**：  
     - 对于当前已经得到的 `mask1`（只含 `v` 和已经处理过的子节点），以及子节点的 `submask`（只含 `c` 那颗子树），  
     - 新的子集是 `new_mask = mask1 | submask`。  
     - 新的 `height` 是 `max(old_height, submask_height + 1)`（因为从 `v` 到子节点的路径要多走一条边）。  
     - 新的 `diam` 是 `max(old_diam, submask_diam, old_height + submask_height + 1)`，后者对应“跨两个子树的最长路径”。  

5. **统计答案**  
   - 合并完所有节点后，每个 `dp[v][mask]`（`mask` 包含 `v`）对应的 `diam` 就是这棵以 `v` 为根的子树的直径。  
   - 把 `diam` 加到答案数组 `ans[diam]` 中即可。  
   - 注意同一子集可能会在不同根 `v` 出现多次，但 **每个合法子树只会在唯一的最小编号节点作为根** 时出现一次（因为我们只把子集的根限定为子集中编号最小的节点），这样避免了重复计数。

6. **为什么快**  
   - 每条边只参与一次合并，合并时遍历的子集数目是子树大小的子集数，整体复杂度是 `O(n * 2^n)`。  
   - 对 `n = 15`，`n * 2^n = 15 * 32768 ≈ 5×10^5`，与暴力解相当，但**不再进行 BFS**，常数更小，思路也更具普适性（适用于稍大 `n` 的场景）。

下面把关键概念用生活化的类比解释：

- **位掩码**：把每座城市想成一本字典的页码，`1` 表示这页被选进子集，`0` 表示未选。  
- **DP 合并**：就像在做拼图，把左边已经拼好的图块（`mask1`）和右边的一个小图块（`submask`）拼在一起，拼好后要重新算一次“最长的边线”（直径）。  
- **背包**：每次决定“要不要把这块小图块放进来”，放进去会让整体的高度和最长边线发生变化。

---

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple

def countSubgraphsForEachDiameter_opt(n: int, edges: List[List[int]]) -> List[int]:
    # ---------- 1. 建树（邻接表） ----------
    g = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # ---------- 2. 把树根在 0 ----------
    parent = [-1] * n
    order = []                 # DFS 序列（自底向上遍历顺序）
    stack = [0]
    parent[0] = 0
    while stack:
        v = stack.pop()
        order.append(v)
        for nb in g[v]:
            if nb == parent[v]:
                continue
            parent[nb] = v
            stack.append(nb)
    order.reverse()            # 现在是叶子到根的顺序

    # ---------- 3. DP 表：dp[v] 是一个 dict，key = mask, value = (height, diam) ----------
    # mask 只在以 v 为根的子树范围内使用，省去 size（size = popcount(mask)）
    dp = [defaultdict(lambda: (-1, -1)) for _ in range(n)]

    for v in order:
        # 只包含自身的子集
        base_mask = 1 << v
        dp[v][base_mask] = (0, 0)          # height = 0, diam = 0

        # 依次合并子节点的信息
        for c in g[v]:
            if parent[c] != v:               # 只处理子节点
                continue
            cur = dp[v].copy()               # 先保存已经合并好的状态
            for mask1, (h1, d1) in cur.items():
                for mask2, (h2, d2) in dp[c].items():
                    # 两个子集必须不相交（因为 mask2 只在 c 的子树里，mask1 已经不包含 c 的节点）
                    new_mask = mask1 | mask2
                    # 新的高度：从 v 出发最远的路径，要么保持原来的，要么经过 c
                    new_h = max(h1, h2 + 1)
                    # 新的直径：三者取最大
                    # 1) 以前的直径 d1
                    # 2) 子节点内部的直径 d2
                    # 3) 跨子树的最长路径 = h1 + h2 + 1（从一侧最远点经过 v 到另一侧最远点）
                    cross = h1 + h2 + 1
                    new_d = max(d1, d2, cross)
                    # 更新 dp[v][new_mask]（取最好的 height/diam 组合）
                    old_h, old_d = dp[v].get(new_mask, (-1, -1))
                    # 对同一个 mask，可能有不同的合并顺序得到不同的 (height, diam)。
                    # 我们只需要保持 height 最大、diam 最大的那一套即可。
                    if new_h > old_h or (new_h == old_h and new_d > old_d):
                        dp[v][new_mask] = (new_h, new_d)

    # ---------- 4. 统计答案 ----------
    ans = [0] * (n - 1)               # ans[d-1] 统计直径为 d 的子树数
    # 为了避免同一子树被不同根重复计数，只统计「根是子集中编号最小的节点」的情况。
    # 这可以通过遍历所有 dp[v]，并只把 mask 中最小位等于 v 的贡献计入。
    for v in range(n):
        for mask, (_, diam) in dp[v].items():
            if diam == 0:               # 只含一个节点的子树直径为 0，不计入答案（题目要求 d ≥ 1）
                continue
            # 检查 mask 中最小的 1 是否正好是 v
            if (mask & -mask) == (1 << v):
                ans[diam - 1] += 1

    return ans
```

> **代码要点注释**  
> - `order.reverse()` 让我们先处理叶子节点，再向上合并，类似“先把小块拼好，再拼大块”。  
> - `dp[v]` 用 `defaultdict` 保存 **仅在 v 子树范围内** 的子集信息，键是位掩码，值是 `(height, diam)`。  
> - 合并时 `cross = h1 + h2 + 1` 对应“从左边最远的点，穿过根 v，走到右边最远的点”，这正是跨两个子树的最长路径。  
> - 最后统计时，只把 **最小编号节点为根** 的子集计入，防止重复计数。最小位检测 `mask & -mask` 与 `1 << v` 是否相同即可实现。

---

#### 复杂度

- **时间复杂度**：`O(n * 2^n)`  
  - 每个节点 `v` 只会与它的子节点做一次「背包」合并。合并时遍历的状态数目恰好是子树的子集数，总体相当于对所有子集遍历一次，乘以 `n`（每层递归一次）。  
  - 对 `n = 15`，约 `5×10^5` 次状态转移，远低于 1 秒。

- **空间复杂度**：`O(n * 2^n)`（最坏情况）  
  - 每个节点的 `dp` 可能保存它子树所有子集的 `(height, diam)`，总数不超过 `n * 2^n`。  
  - 由于 `n` 很小，这在内存上也完全可以接受（约几 MB）。

---

## 心得

- **核心技巧**：**位掩码 + 树形 DP**（子树合并），把“求直径”提前做成状态转移，使得每个子集只需要一次查表即可得到答案。  
- **适用题型**  
  1. “枚举子集并判断连通性” 的树形问题（如 LeetCode 1617 本题）。  
  2. “在树上做背包” 的组合计数问题（如 “Maximum Sum of a Subtree With Constraints” 等）。  
  3. “求子树属性（高度、直径、最大权值等）” 的 DP 合并类问题。  
- **一句话总结解题钥匙**：**把子树的“结构信息” (高度、直径) 用 DP 存下来，合并时只更新这两个数字，就能在指数级子集里快速得到答案。**

---

## 反思

- **第一反应**：看到 “n ≤ 15” 就想到 **位掩码枚举**，随后担心如何快速判断子集是否连通以及怎么求直径。  
- **最容易踩的坑**  
  1. **连通性判断遗漏**：只检查子集内部的边数不够，还必须确保所有选中的节点真的在同一个连通块。  
  2. **直径为 0 的子树**（只有单个节点）不应计入答案，因为题目要求 `d ≥ 1`。  
  3. **重复计数**：同一子树在不同根节点时会出现多次，需要通过“最小编号节点是根”或其他唯一化手段去重。  
- **下次类似题目第一步**：**先判断是否可以用位掩码遍历所有子集**（看 `n` 是否足够小），然后**确定子集合法性的快速判定方式**（连通性、树形约束），最后再考虑**是否能把需要的属性（高度、直径等）提前 DP 计算**，避免对每个子集重新跑图遍历。