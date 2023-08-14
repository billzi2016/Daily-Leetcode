# #2360. **图中最长环** / Longest Cycle in a Graph

> 难度：困难 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/longest-cycle-in-a-graph/)

---

## 题目（英文原版）

**Description**

You are given a directed graph of n nodes numbered from 0 to n - 1, where each node has at most one outgoing edge.
The graph is represented with a given 0-indexed array edges of size n, indicating that there is a directed edge from node i to node edges[i]. If there is no outgoing edge from node i, then edges[i] == -1.
Return the length of the longest cycle in the graph. If no cycle exists, return -1.
A cycle is a path that starts and ends at the same node.

**Examples**

**Example 1:**

```
Input: edges = [3,3,4,2,3]
Output: 3
Explanation: The longest cycle in the graph is the cycle: 2 -> 4 -> 3 -> 2.
The length of this cycle is 3, so 3 is returned.
```

**Example 2:**

```
Input: edges = [2,-1,3,1]
Output: -1
Explanation: There are no cycles in this graph.
```

**Constraints**

- n == edges.length
- 2 <= n <= 105
- -1 <= edges[i] < n
- edges[i] != i

---

## 题目（中文翻译）

你被给定了一个 **有向图（directed graph）**，包含编号为 `0` 到 `n - 1` 的 `n` 个节点，每个节点至多只有一条出边（outgoing edge）。  
图使用一个下标从 `0` 开始的数组 `edges` 表示，`edges` 的长度为 `n`，其中 `edges[i]` 表示从节点 `i` 指向节点 `edges[i]` 的有向边。如果节点 `i` 没有出边，则 `edges[i] == -1`。  

返回图中 **最长环（cycle）** 的长度。如果图中不存在环，返回 `-1`。  
环是指起点与终点相同的路径。

---

### 示例

**示例 1**  
```
Input: edges = [3,3,4,2,3]
Output: 3
Explanation: 图中最长的环是 2 -> 4 -> 3 -> 2。
该环的长度为 3，故返回 3。
```

**示例 2**  
```
Input: edges = [2,-1,3,1]
Output: -1
Explanation: 图中不存在环。
```

---

### 约束条件

- `n == edges.length`
- `2 <= n <= 10^5`
- `-1 <= edges[i] < n`
- `edges[i] != i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出的图是 **每个节点最多只有一条出边** 的有向图。  
我们可以把它想成“一张指向下一位同学的传话纸条”，有的同学手里没有纸条（`-1`），有的同学手里只拿一张纸条指向别的同学。

> **最直接的想法**：从每个节点出发，沿着它的唯一出边一直走下去，直到出现三种情况  
> 1. 走到了 `-1`，说明这条路没有环。  
> 2. 走到了已经在 **本次遍历** 中出现过的节点，这时我们找到了一个环，环的长度就是从第一次出现该节点到现在走的步数。  
> 3. 走到了 **之前已经遍历过**（标记为全局已访问）的节点，这说明这条路已经被别的起点处理过，直接结束即可。

这里需要两个标记集合：  

- `global_visited`（全局已访问）：记录所有已经被任何起点遍历过的节点，防止重复工作。  
- `local_visited`（本次遍历已访问）：记录本次从某个起点走过的节点及它们的步数，用来判断环的出现位置。

> **类比**：`global_visited` 像一本已经写好“已检查”标记的检查表，`local_visited` 像是你在当前这条路上贴的临时标签，帮助你发现自己是否回到了已经走过的地方。

只要把每个节点都当作起点去跑一次，记录下出现的所有环的长度，最后取最大值即可。

#### 代码（Python）

```python
from typing import List

def longestCycle(edges: List[int]) -> int:
    n = len(edges)
    # 全局已访问：已经被任何起点遍历过的节点
    global_visited = [False] * n
    longest = -1                     # 记录最长环的长度，初始为 -1 表示没有环

    for start in range(n):
        if global_visited[start]:
            # 这个节点已经在别的遍历中被处理过，直接跳过
            continue

        # local_visited 用 dict 保存「节点 -> 步数」方便算环的长度
        local_visited = dict()
        cur = start
        step = 0                      # 从 start 出发走了多少步

        while cur != -1 and not global_visited[cur]:
            if cur in local_visited:
                # 环出现！环的长度 = 当前步数 - 第一次到达该节点的步数
                cycle_len = step - local_visited[cur]
                longest = max(longest, cycle_len)
                break

            # 记录本次遍历的路径
            local_visited[cur] = step
            step += 1
            cur = edges[cur]          # 沿唯一的出边继续前进

        # 本次遍历结束后，把走过的所有节点标记为全局已访问
        for node in local_visited:
            global_visited[node] = True

    return longest
```

#### 复杂度

- **时间复杂度：** `O(n²)`（最坏情况）  
  - 解释：如果每次遍历都只能走一步（因为一旦走到已全局访问的节点就停），而我们又要对每个节点都尝试一次，最坏会出现 `1 + 2 + … + n ≈ n²/2` 步。对初学者来说，可以把 `O(n²)` 想成“随 `n` 增大，运行时间会像正方形一样快”。  
- **空间复杂度：** `O(n)`  
  - 解释：我们用了两个长度为 `n` 的布尔数组和一个最多保存 `n` 条记录的字典，都是跟节点数线性相关的。

> 暴力解虽然思路直观，但在 `n` 达到 `10⁵` 时会超时，需要进一步优化。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历**：很多节点会被不同的起点多次踩到，尤其是“树枝”状的结构。  
我们要把 **每个节点只遍历一次**，并且在遍历过程中直接得到环的长度。

两种常见的思路：

1. **拓扑排序（Kahn）**：把所有 **不在环上的节点**（即入度为 0 的节点）逐层删掉，剩下的节点必然全部在环里。删完后剩余的连通块的大小就是环的长度。  
2. **DFS + 时间戳**：在一次深度优先搜索中，用 `visit_time[node]` 记录第一次进入该节点的时间（步数）。当在递归过程中再次碰到已经被本次 DFS 访问过的节点时，`当前时间 - visit_time[node]` 就是环的长度。

这里我们采用 **DFS + 时间戳**，因为实现更直观且只需要一次遍历。

关键点如下：

- **全局状态 `state[node]`**  
  - `0`：未访问  
  - `1`：正在本次 DFS 中（相当于“在递归栈里”）  
  - `2`：本次 DFS 已完成，且不在环中  

- **时间戳 `order[node]`**：记录进入该节点时的全局计数器 `step`，帮助计算环的长度。

遍历每个节点 `i`：

1. 如果 `state[i] != 0`，说明已经处理过，直接跳过。  
2. 否则从 `i` 开始沿唯一出边进行 DFS。  
3. 在递归过程中：
   - 进入一个新节点 `v`，把 `state[v] = 1`，`order[v] = step`，`step += 1`。  
   - 如果 `v` 的出边指向 `-1`，直接结束，标记 `state[v] = 2`。  
   - 如果指向的下一个节点 `next` **未访问**，继续递归。  
   - 如果 `state[next] == 1`（仍在当前递归栈），说明找到了环，环长 = `step - order[next]`。  
   - 如果 `state[next] == 2`，说明 `next` 已经确定不在环里，当前路径也不在环。

4. 递归返回后，把当前节点标记为 `state = 2`（已完成）。

整个过程只会访问每个节点一次，时间线性。

> **类比**：把递归栈想成“一条追踪线”。当你在追踪过程中再次碰到已经在这条线上的点，就说明你绕了个圈回来——这正是环。

#### 代码（Python）

```python
from typing import List

def longestCycle(edges: List[int]) -> int:
    n = len(edges)
    # 0 = 未访问, 1 = 正在本次 DFS（在递归栈里）, 2 = 已处理完毕
    state = [0] * n
    order = [0] * n          # 记录进入节点时的全局步数
    step = 0                 # 全局计数器，随每次进入新节点递增
    longest = -1

    def dfs(node: int):
        """对节点 node 进行深度优先搜索，返回在该路径上找到的最大环长（若有）"""
        nonlocal step, longest
        state[node] = 1               # 标记为“正在访问”
        order[node] = step
        step += 1

        nxt = edges[node]             # 唯一的出边
        if nxt != -1:                  # 如果存在出边
            if state[nxt] == 0:       # 还未访问，继续向下递归
                dfs(nxt)
            elif state[nxt] == 1:     # nxt 仍在当前递归栈，发现环
                cycle_len = step - order[nxt]
                longest = max(longest, cycle_len)
            # state[nxt] == 2 时不做任何事，说明 nxt 已经确定不在环

        state[node] = 2               # 本节点处理完毕，标记为“已完成”

    for i in range(n):
        if state[i] == 0:             # 只从未访问的节点开始 DFS
            dfs(i)

    return longest
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 解释：每个节点恰好进入一次 `dfs`，在递归里只做常数次操作。即使有环，也只会遍历一次环内的节点。对比暴力解的 `O(n²)`，这里的运行时间随 `n` 成线性增长，像“一条直线”。  
- **空间复杂度：** `O(n)`  
  - 解释：递归栈最坏深度可能是 `n`（链状结构），再加上 `state`、`order` 两个长度为 `n` 的数组，都是线性空间。

> 因此，这个方案在 `n ≤ 10⁵` 的限制下完全可以通过。

---

## 心得

- **核心技巧**：**DFS + 时间戳（或递归栈标记）** 用来一次遍历找出有向图中的环，并直接算出环的长度。  
- **适用的题型**：  
  1. “找图中是否存在环” 类似题目（例如 LeetCode 207. Course Schedule）。  
  2. “找环的入口/环的长度” 类似题目（例如 LeetCode 142. Linked List Cycle II）。  
  3. “每个节点只有一条出边” 的特殊图问题（本题、LeetCode 2360. Longest Cycle in a Graph）。  
- **一句话总结**：**把每条路径看成一次“追踪”，只要在追踪过程中再次踩到已经在本次追踪里的节点，就找到了环，环长等于两次踩到的时间差。**

---

## 反思

- **第一反应**：看到“每个节点最多一条出边”，立刻想到可以把图看成 **若干条链 + 若干个环**，于是想从每个节点走一遍。  
- **最容易踩的坑**：  
  - **忘记全局标记**：如果不记录已经处理过的节点，会导致大量重复遍历，时间爆炸。  
  - **环的长度计算错误**：必须用 **当前全局步数 - 第一次进入环中节点的步数**，而不是简单计数。  
  - **递归深度**：在 Python 中递归深度可能超出默认限制，需要自行调整（`sys.setrecursionlimit`），或者改写成显式栈的迭代写法。  
- **下次类似题的第一步**：先判断**是否可以把问题抽象为“每个节点只有唯一下一步”，然后考虑**一次遍历**（拓扑删点或 DFS 标记）来直接得到环的信息，而不是多次重复走。