# #1377. **t 秒后青蛙的位置** / Frog Position After T Seconds

> 难度：困难 · 标签：Tree、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/frog-position-after-t-seconds/)

---

## 题目（英文原版）

**Description**

Given an undirected tree consisting of n vertices numbered from 1 to n. A frog starts jumping from vertex 1. In one second, the frog jumps from its current vertex to another unvisited vertex if they are directly connected. The frog can not jump back to a visited vertex. In case the frog can jump to several vertices, it jumps randomly to one of them with the same probability. Otherwise, when the frog can not jump to any unvisited vertex, it jumps forever on the same vertex.
The edges of the undirected tree are given in the array edges, where edges[i] = [ai, bi] means that exists an edge connecting the vertices ai and bi.
Return the probability that after t seconds the frog is on the vertex target. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 2, target = 4
Output: 0.16666666666666666 
Explanation: The figure above shows the given graph. The frog starts at vertex 1, jumping with 1/3 probability to the vertex 2 after second 1 and then jumping with 1/2 probability to vertex 4 after second 2. Thus the probability for the frog is on the vertex 4 after 2 seconds is 1/3 * 1/2 = 1/6 = 0.16666666666666666.
```

**Example 2:**

```
Input: n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 1, target = 7
Output: 0.3333333333333333
Explanation: The figure above shows the given graph. The frog starts at vertex 1, jumping with 1/3 = 0.3333333333333333 probability to the vertex 7 after second 1.
```

**Constraints**

- 1 <= n <= 100
- edges.length == n - 1
- edges[i].length == 2
- 1 <= ai, bi <= n
- 1 <= t <= 50
- 1 <= target <= n

---

## 题目（中文翻译）

给定一棵无向树，包含编号为 `1` 到 `n` 的 `n` 个顶点。青蛙从顶点 `1` 开始跳跃。  
在 **1 秒** 内，青蛙会从当前所在的顶点跳到与之直接相连且**未被访问过**的顶点。如果存在多条可选路径，青蛙会以相同的概率随机选择其中一条进行跳跃。  
如果青蛙已经没有未访问的相邻顶点可跳，则它会一直停留在当前顶点，不再移动。  

无向树的边信息存放在数组 `edges` 中，其中 `edges[i] = [a_i, b_i]` 表示顶点 `a_i` 与顶点 `b_i` 之间存在一条边。  

返回青蛙在 **t 秒** 后位于目标顶点 `target` 的概率。答案相对误差在 `10^-5` 以内的解均被视为正确。

---

### 示例

#### 示例 1
```text
Input: n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 2, target = 4
Output: 0.16666666666666666 
```
**解释**：上图展示了给定的树结构。青蛙从顶点 `1` 出发，第一秒以概率 `1/3` 跳到顶点 `2`，第二秒再以概率 `1/2` 跳到顶点 `4`。因此，青蛙在 `2` 秒后位于顶点 `4` 的概率为 `1/3 * 1/2 = 1/6 ≈ 0.16666666666666666`。

#### 示例 2
```text
Input: n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 1, target = 7
Output: 0.3333333333333333
```
**解释**：上图展示了给定的树结构。青蛙从顶点 `1` 出发，第一秒以概率 `1/3 = 0.3333333333333333` 跳到顶点 `7`。

---

### 约束条件
- `1 <= n <= 100`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `1 <= a_i, b_i <= n`
- `1 <= t <= 50`
- `1 <= target <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的跳法全部枚举**，然后把每条路径对应的概率加起来。  
- **数据结构**：用 **邻接表**（list of lists）来存放树的结构。邻接表就像一本“通讯录”，每个节点（人）都有一张“联系人名单”，里面写着它直接相连的节点（朋友）。  
- **遍历方式**：用递归（深度优先搜索）从根节点 `1` 开始，记录已经走过的节点（相当于在“访问过的联系人名单”里打勾），以及已经用了多少秒。  
- **概率计算**：在某个节点 `cur`，如果还有 `k` 条未访问的边可以走，青蛙会等概率选一条，所以这一步的概率是 `1/k`。把它乘到当前路径的累计概率上即可。  

**为什么正确**  
树的每条边只能走一次（因为不能回到已经访问的节点），所以一次完整的遍历恰好对应一次合法的跳跃序列。把所有序列的概率相加，正好得到青蛙在 `t` 秒后位于 `target` 的总概率。

**复杂度分析（大白话）**  
- **时间复杂度**：最坏情况下每一步都有很多未访问的邻居，比如一棵星形树（根节点连 `n‑1` 颗叶子）。如果 `t` 很大，递归会产生 ` (n‑1) × (n‑2) × …` 这么多分支，指数级增长，用 **O(b^t)** 表示（`b` 是平均分支数）。这在实际运行时会非常慢，尤其 `t` 达到 50 时几乎不可行。  
- **空间复杂度**：递归栈的深度最多是 `t`，加上邻接表的存储，需要 **O(n + t)** 的额外空间。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def frogPosition_bruteforce(n: int, edges: List[List[int]],
                           t: int, target: int) -> float:
    # 1. 建立邻接表（通讯录）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    ans = 0.0                     # 最终答案累计到这里

    def dfs(cur: int, time: int, prob: float, visited: set):
        """从 cur 节点出发，已经用了 time 秒，累计概率为 prob"""
        nonlocal ans
        # ① 到达目标且满足停留条件，累计答案
        if cur == target:
            # 如果已经用了 t 秒，或者已经没有可以继续跳的邻居（叶子），
            # 那么青蛙会一直停在这里。
            if time == t or not any(nb not in visited for nb in graph[cur]):
                ans += prob
                # 这里不必继续向下搜索，因为即使继续也不会改变答案
                return

        # ② 时间已用完，仍未到达 target，直接返回
        if time == t:
            return

        # ③ 计算未访问的邻居数量
        unvisited = [nb for nb in graph[cur] if nb not in visited]
        k = len(unvisited)          # 相当于“有几条路可以选”
        if k == 0:                  # 没路可走，只能原地等
            return

        # ④ 对每条可能的路递归搜索
        for nb in unvisited:
            visited.add(nb)                     # 标记这条路已走
            dfs(nb, time + 1, prob * 1.0 / k, visited)
            visited.remove(nb)                  # 恢复现场，供其他分支使用

    # 初始状态：在节点 1，时间 0，概率 1，已经访问了 1
    dfs(1, 0, 1.0, {1})
    return ans
```

> 代码里每一行的中文注释都是在解释“这一步在干嘛”。  
> 运行 `frogPosition_bruteforce` 能得到与官方答案相同的结果，只是会在 `t` 较大时超时。

#### 复杂度

- **时间复杂度**：`O(b^t)`（指数级），其中 `b` 是平均分支数。  
  *大白话*：想象每秒都要掷一次硬币选路，树的分叉很多时，所有可能的“硬币序列”会呈指数增长，算不过来。
- **空间复杂度**：`O(n + t)`，邻接表占 `O(n)`，递归栈最深 `t` 层。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“枚举所有路径”**——其实我们并不需要把每条路径都写出来，只要把 **概率的传播过程** 按照树的结构一次走完即可。  

关键观察：

1. **树没有环**，所以从根出发的每一次跳跃只能往“子树”方向走。我们只需要记住“从哪来”，即父节点，防止回头。  
2. 在某个节点 `cur`，如果还有 `k` 条未访问的子节点，青蛙选每条的概率都是 `1/k`。这意味着 **当前的累计概率 = 父节点的概率 ÷ k**。  
3. 当青蛙 **到达目标** 时，有两种合法的停留情况  
   - 正好用了 `t` 秒（恰好在第 `t` 步到达）  
   - 已经没有未访问的邻居（变成叶子），即使时间还没用完，青蛙也会一直呆在这里。  

基于以上三点，我们可以 **一次 DFS**（或 BFS）把概率从根向下传递，一旦满足停留条件就把概率加入答案。整个过程只遍历每条边一次，时间线性。

**核心算法/数据结构**：

- **深度优先搜索（DFS）**：递归实现，参数包括 `cur`（当前节点）、`time`（已经用了多少秒）和 `prob`（到达当前节点的累计概率）。  
- **邻接表**：仍然用来存树的结构。  
- **父节点记录**：在递归里把 `parent` 传进去，避免回到已经走过的节点。  

下面用一个**生活化的类比**帮助理解：

> 把树想象成一棵**树形电路**，根节点是电源，电流（概率）从上往下流。每次遇到分叉，电流会 **平均分配** 到所有未走过的分支。我们只需要把电流一路“走完”，不必记录每一次电流的具体路径。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def frogPosition(n: int, edges: List[List[int]],
                t: int, target: int) -> float:
    """
    最优解：一次 DFS 传播概率
    """
    # 1️⃣ 建立邻接表（通讯录）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    answer = 0.0

    def dfs(cur: int, parent: int, time: int, prob: float):
        """
        cur      – 当前所在的节点
        parent   – 来自哪条边（防止回头）
        time     – 已经用了多少秒
        prob     – 到达 cur 的累计概率
        """
        nonlocal answer

        # 2️⃣ 是否已经到达 target，且满足停留条件？
        if cur == target:
            # 只要满足「恰好用了 t 秒」或「没有可继续的子节点」即可停下来
            if time == t or len([nb for nb in graph[cur] if nb != parent]) == 0:
                answer = prob          # 找到唯一答案，直接返回
                # 这里可以直接结束搜索，因为在树上同一个节点只能有唯一一条路径到达
                return

        # 3️⃣ 时间用完还没到 target，直接返回
        if time == t:
            return

        # 4️⃣ 计算未访问的子节点数量（不包括父节点）
        children = [nb for nb in graph[cur] if nb != parent]
        k = len(children)

        # 5️⃣ 若没有子节点，青蛙只能原地停留（不会影响答案，因为上面已经处理 target）
        if k == 0:
            return

        # 6️⃣ 向每个子节点递归，概率均分
        for nb in children:
            dfs(nb, cur, time + 1, prob / k)   # prob/k = prob * (1/k)

    # 初始状态：在节点 1，时间 0，概率 1，没有父节点（设为 0）
    dfs(1, 0, 0, 1.0)
    return answer
```

> **关键行解释**  
> - `children = [nb for nb in graph[cur] if nb != parent]`：把“不能回头的父节点”过滤掉，剩下的才是真正的“可选子树”。  
> - `prob / k`：把当前概率平均分给每条可走的边，正好对应题目“等概率随机跳”。  
> - `if cur == target and (time == t or len(children) == 0)`：这一步决定了青蛙是否会“卡在这里”。如果已经是叶子，即使时间没到 `t`，青蛙也会一直呆在这。

#### 复杂度

- **时间复杂度**：`O(n)`，因为每条边只会被访问一次。  
  *大白话*：树上只有 `n‑1` 条路，DFS 把它们走遍一次就完事了，和 `t` 大小无关。
- **空间复杂度**：`O(n)`，主要是递归栈的深度最坏等于树的高度（最坏是链状树时是 `n`），以及邻接表本身。

---

## 心得

- **核心技巧**：在树结构上进行 **概率的递归传播**（DFS），利用“父节点排除法”防止回头。  
- **适用的题型**  
  1. **树上随机游走**（如 LeetCode 1491 – `Average Salary of Employees` 中的概率传播）  
  2. **树的期望值/概率问题**（如 LeetCode 1245 – `Tree Diameter` 的 BFS/DFS 统计）  
  3. **限定步数的遍历**（如 LeetCode 1029 – `Two City Scheduling` 中的组合计数）  
- **一句话总结解题钥匙**：**把“每一步的等概率选择”转化为“当前概率除以可选分支数”，沿树向下递归即可**。

---

## 反思

- **第一反应**：看到“随机跳”“等概率”，立刻想到**枚举所有可能**，于是写了暴力递归。  
- **最容易踩的坑**  
  - **漏掉“停在叶子上”**：当时间还没用完但已无未访问的邻居时，青蛙会一直停留，需要在答案判断里额外处理。  
  - **回头错误**：如果不记录父节点，DFS 会在树上来回走，导致无限递归或错误的概率分配。  
  - **边界条件**：`t = 0` 时只可能在根节点；`target = 1` 时要判断根节点是否已经是叶子。  
- **下次遇到同类题**：第一步先思考 **“概率如何在结构上分配？”**，如果是树或 DAG，往往可以 **一次遍历把概率向下传递**，而不是枚举所有路径。这样既省时又省力。