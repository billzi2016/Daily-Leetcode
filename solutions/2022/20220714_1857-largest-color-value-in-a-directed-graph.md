# #1857. 有向图中最大颜色值 / Largest Color Value in a Directed Graph

> 难度：困难 · 标签：Hash Table、Dynamic Programming、Graph、Topological Sort、Memoization、Counting · [LeetCode 链接](https://leetcode.com/problems/largest-color-value-in-a-directed-graph/)

---

## 题目（英文原版）

**Description**

There is a directed graph of n colored nodes and m edges. The nodes are numbered from 0 to n - 1.
You are given a string colors where colors[i] is a lowercase English letter representing the color of the ith node in this graph (0-indexed). You are also given a 2D array edges where edges[j] = [aj, bj] indicates that there is a directed edge from node aj to node bj.
A valid path in the graph is a sequence of nodes x1 -> x2 -> x3 -> ... -> xk such that there is a directed edge from xi to xi+1 for every 1 <= i < k. The color value of the path is the number of nodes that are colored the most frequently occurring color along that path.
Return the largest color value of any valid path in the given graph, or -1 if the graph contains a cycle.

**Examples**

**Example 1:**

```
Input: colors = "abaca", edges = [[0,1],[0,2],[2,3],[3,4]]
Output: 3
Explanation: The path 0 -> 2 -> 3 -> 4 contains 3 nodes that are colored "a" (red in the above image).
```

**Example 2:**

```
Input: colors = "a", edges = [[0,0]]
Output: -1
Explanation: There is a cycle from 0 to 0.
```

**Constraints**

- n == colors.length
- m == edges.length
- 1 <= n <= 105
- 0 <= m <= 105
- colors consists of lowercase English letters.
- 0 <= aj, bj < n

---

## 题目（中文翻译）

给定一个由 **n** 个带颜色的节点和 **m** 条有向边（directed edge）组成的有向图（directed graph），节点编号为 **0** 到 **n‑1**。  
你会得到一个字符串 **colors**，其中 `colors[i]` 是一个小写英文字母，表示第 **i** 个节点的颜色（0‑索引）。同时给出一个二维数组 **edges**，其中 `edges[j] = [a_j, b_j]` 表示存在一条从节点 **a_j** 指向节点 **b_j** 的有向边。

**有效路径（valid path）** 是指一系列节点 `x₁ -> x₂ -> x₃ -> ... -> x_k`，满足对于每个 `1 ≤ i < k`，都有一条从 `x_i` 到 `x_{i+1}` 的有向边。  
该路径的 **颜色值（color value）** 定义为路径上出现次数最多的颜色所对应的节点数量。

返回给定图中任意 **有效路径** 的最大 **颜色值**，如果图中存在环（cycle），则返回 **-1**。

---

### 示例

**示例 1**  
输入: `colors = "abaca", edges = [[0,1],[0,2],[2,3],[3,4]]`  
输出: `3`  
解释: 路径 `0 -> 2 -> 3 -> 4` 包含 **3** 个颜色为 `'a'` 的节点。

**示例 2**  
输入: `colors = "a", edges = [[0,0]]`  
输出: `-1`  
解释: 节点 `0` 到自身形成了一个环。

---

### 约束条件

- `n == colors.length`
- `m == edges.length`
- `1 ≤ n ≤ 10⁵`
- `0 ≤ m ≤ 10⁵`
- `colors` 只包含小写英文字母
- `0 ≤ a_j, b_j < n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的合法路径都列举出来，统计每条路径上出现次数最多的颜色，然后取最大值**。  

- **数据结构**  
  - **邻接表**：把每条有向边 `a -> b` 存进 `graph[a]`，相当于“每个人的朋友列表”。  
  - **路径栈**：在深度优先搜索（DFS）时，用一个栈记录当前走到的节点，像是“我们现在在走哪条路”。  

- **为什么正确**  
  - 我们枚举了图中**每一条**从起点到终点的合法路径，因而不会错过答案。  

- **时间/空间复杂度**  
  - 在最坏情况下，图是一条长链，节点数为 `n`，所有可能的路径数是指数级的（比如 `2^(n-1)`），因为每走一步都可以选择继续往下或停下来。  
  - 用大白话说，**时间复杂度是指数级**，即 `O(2^n)`，这在 `n=10^5` 时根本跑不完。  
  - 空间上我们只需要保存邻接表（`O(n+m)`）和递归栈（最深 `O(n)`），所以 **空间复杂度是线性的** `O(n+m)`。  

> **小结**：暴力解思路简单、容易写，但会超时。下面我们一步步把它优化掉。

#### 代码（Python）

```python
from collections import defaultdict

def largestPathValue_bruteforce(colors: str, edges):
    n = len(colors)
    graph = defaultdict(list)
    for u, v in edges:                # 建立邻接表
        graph[u].append(v)

    best = 0
    visited = [0] * n                  # 0=未访问, 1=正在访问, 2=已完成（用于检测环）

    def dfs(u, counter):
        """从节点 u 开始的所有路径，counter 保存当前路径上每种颜色的计数"""
        nonlocal best
        # 把当前节点的颜色计数加 1
        c_idx = ord(colors[u]) - ord('a')
        counter[c_idx] += 1
        # 更新答案：当前路径上出现最多的颜色次数
        best = max(best, max(counter))

        for v in graph[u]:
            if visited[v] == 1:        # 发现环 → 暴力解不处理环，只是示意
                continue
            dfs(v, counter[:])         # 复制计数器，防止不同分支相互影响

        # 回溯时不必显式减掉计数，因为我们用了复制的 counter

    for i in range(n):
        dfs(i, [0] * 26)                # 每个节点都当起点尝试

    return best
```

> **注意**：这段代码仅用于演示“暴力思路”，在实际测试中会因为 **指数级时间** 而超时。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）——因为会遍历所有可能的路径。  
- **空间复杂度**：`O(n + m)`——邻接表 + 递归栈（最深 `n`）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **两大瓶颈**：

1. **重复计算**：很多路径会共享相同的前缀，例如 `0->2->3` 和 `0->1->2->3` 都会在 `0->2` 这段上重复统计颜色。  
2. **环的检测**：如果图里有环，合法路径根本不存在，需要提前返回 `-1`。

我们可以 **利用拓扑排序**（Topological Sort）把图的节点按 **“先出现后出现”** 的顺序排列，这样每条有向边 `u -> v` 都满足 `u` 在 `v` 前面。拓扑序列天然去掉了环的干扰——如果无法得到完整的拓扑序列，说明图里有环，直接返回 `-1`。

在得到拓扑序列后，**动态规划**（DP）可以帮助我们在一次遍历中把所有路径的信息“合并”。  
我们定义：

```
dp[u][c] = 在以节点 u 为路径终点（即路径的最右侧）时，颜色 c 出现的最大次数
```

- `dp` 的维度是 `n × 26`（因为只有 26 种小写字母）。  
- 初始时，`dp[u][color_of_u] = 1`，其它颜色为 `0`。  

遍历拓扑序列时，对每条边 `u -> v`：

```
对于所有颜色 c：
    dp[v][c] = max(dp[v][c], dp[u][c] + (color_of_v == c))
```

解释：如果我们把 `u` 前面的最优路径（已记录在 `dp[u][c]`）延伸到 `v`，则颜色 `c` 的计数会 **加 1**（如果 `v` 本身也是颜色 `c`），否则保持不变。取最大值即可保证得到 **所有以 v 为终点的路径中，颜色 c 出现的最多次数**。

遍历完所有节点后，答案就是 `dp` 表中所有元素的最大值。

> **核心概念解释**  
> - **拓扑排序**：想象把所有任务排成一条生产线，只有前置任务完成后才能开始后面的任务。我们使用 **Kahn 算法**（基于入度的 BFS）实现。  
> - **入度（indegree）**：一个节点有多少条边指向它，类似“有多少人指着你”。入度为 0 的节点可以最先加工。  
> - **动态规划表**：把每个节点的“状态”记下来，后面的节点只需要查表，不必重新走一遍所有路径。

#### 代码（Python）

```python
from collections import deque, defaultdict

def largestPathValue(colors: str, edges):
    n = len(colors)
    # 1️⃣ 建图 + 计算入度
    graph = [[] for _ in range(n)]          # 邻接表，graph[u] 存放 u 的所有出邻居
    indeg = [0] * n                          # 入度数组
    for u, v in edges:
        graph[u].append(v)
        indeg[v] += 1

    # 2️⃣ 拓扑排序（Kahn 算法）
    q = deque([i for i in range(n) if indeg[i] == 0])  # 所有入度为 0 的节点先入队
    topo = []                                          # 保存拓扑序列
    while q:
        u = q.popleft()
        topo.append(u)
        for v in graph[u]:
            indeg[v] -= 1               # “移除”这条边
            if indeg[v] == 0:           # 入度降为 0，说明 v 可以被处理了
                q.append(v)

    # 3️⃣ 如果拓扑序列没有覆盖所有节点 → 图中有环
    if len(topo) != n:
        return -1

    # 4️⃣ DP 表：dp[u][c] 记录以 u 为终点、颜色 c 的最大出现次数
    dp = [[0] * 26 for _ in range(n)]
    for i in range(n):
        c_idx = ord(colors[i]) - ord('a')
        dp[i][c_idx] = 1                # 只包含自身时，自己的颜色出现一次

    ans = 1                              # 至少会有一个节点

    # 5️⃣ 按拓扑序遍历，更新邻居的 DP 值
    for u in topo:
        for v in graph[u]:
            for c in range(26):
                # 如果 v 的颜色恰好是 c，就在原有计数上 +1
                add = 1 if (ord(colors[v]) - ord('a')) == c else 0
                # 取最大：要么沿着 u 来，要么保持原来的 dp[v][c]
                if dp[v][c] < dp[u][c] + add:
                    dp[v][c] = dp[u][c] + add
                    # 同时更新全局答案
                    if dp[v][c] > ans:
                        ans = dp[v][c]

    return ans
```

**关键行中文注释** 已在代码中给出，帮助你一步步读懂每一步的意义。

#### 复杂度

- **时间复杂度**：`O(n + m + 26·m)`  
  - 拓扑排序遍历所有节点和边是 `O(n + m)`。  
  - 对每条边我们遍历 26 种颜色（常数），所以是 `O(26·m)`，即 `O(m)`。  
  - 合在一起仍然是线性级别 `O(n + m)`，对 `10⁵` 规模的数据完全可接受。  
  - 用大白话说：我们只走了一遍图，而且每次只做了非常少的额外工作（检查 26 种颜色），所以跑得很快。

- **空间复杂度**：`O(n·26 + n + m)`  
  - DP 表占 `n·26`（约 `2.6·10⁶` 的整数，仍然在内存可接受范围）。  
  - 邻接表、入度数组和队列各占 `O(n + m)`。  
  - 总体仍是线性空间。

---

## 心得  

- **核心技巧**：**拓扑排序 + 按颜色的动态规划**。  
- **适用场景**（类似题目）  
  1. *“最长递增路径”*（LeetCode 329）——同样用拓扑排序把 DAG 转成线性顺序，再 DP 求最长。  
  2. *“课程表 III”*（LeetCode 630）——先判断是否有环（拓扑），再在拓扑序上做 DP。  
  3. *“最长的有效字符序列”*（自定义）——在有向无环图上统计某种属性的最大累计值。  

> **一句话总结解题钥匙**：把有向图变成“先后顺序”（拓扑），再在这个顺序上把“局部最优”汇总到“全局最优”（DP）。

---

## 反思  

- **第一反应**：看到“有向图”“路径”“颜色计数”，立刻想到 **DFS 暴力遍历**，因为最直接的思路总是先把所有可能列出来。  
- **最容易踩的坑**  
  1. **环检测**：如果图里有环，路径长度可以无限增长，必须在一开始就判断。  
  2. **计数冲突**：在 DP 更新时忘记给当前节点的颜色额外加 1，会导致答案偏小。  
  3. **大写/小写字母映射**：把字符转成 0~25 的下标时要小心 `ord('a')` 的基准。  
- **下次类似题的第一步**：先 **判断图是否是 DAG**（使用拓扑排序或 DFS 检环），如果是 DAG 再 **在拓扑序上做 DP**，把每个节点的状态向后传播。这样既能避免无限循环，又能一次遍历搞定所有子路径的最优值。