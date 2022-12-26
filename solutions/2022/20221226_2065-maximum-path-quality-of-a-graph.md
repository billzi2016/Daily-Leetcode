# #2065. **图的最大路径质量** / Maximum Path Quality of a Graph

> 难度：困难 · 标签：Array、Backtracking、Graph · [LeetCode 链接](https://leetcode.com/problems/maximum-path-quality-of-a-graph/)

---

## 题目（英文原版）

**Description**

There is an undirected graph with n nodes numbered from 0 to n - 1 (inclusive). You are given a 0-indexed integer array values where values[i] is the value of the ith node. You are also given a 0-indexed 2D integer array edges, where each edges[j] = [uj, vj, timej] indicates that there is an undirected edge between the nodes uj and vj, and it takes timej seconds to travel between the two nodes. Finally, you are given an integer maxTime.
A valid path in the graph is any path that starts at node 0, ends at node 0, and takes at most maxTime seconds to complete. You may visit the same node multiple times. The quality of a valid path is the sum of the values of the unique nodes visited in the path (each node's value is added at most once to the sum).
Return the maximum quality of a valid path.
Note: There are at most four edges connected to each node.

**Examples**

**Example 1:**

```
Input: values = [0,32,10,43], edges = [[0,1,10],[1,2,15],[0,3,10]], maxTime = 49
Output: 75
Explanation:
One possible path is 0 -> 1 -> 0 -> 3 -> 0. The total time taken is 10 + 10 + 10 + 10 = 40 <= 49.
The nodes visited are 0, 1, and 3, giving a maximal path quality of 0 + 32 + 43 = 75.
```

**Example 2:**

```
Input: values = [5,10,15,20], edges = [[0,1,10],[1,2,10],[0,3,10]], maxTime = 30
Output: 25
Explanation:
One possible path is 0 -> 3 -> 0. The total time taken is 10 + 10 = 20 <= 30.
The nodes visited are 0 and 3, giving a maximal path quality of 5 + 20 = 25.
```

**Example 3:**

```
Input: values = [1,2,3,4], edges = [[0,1,10],[1,2,11],[2,3,12],[1,3,13]], maxTime = 50
Output: 7
Explanation:
One possible path is 0 -> 1 -> 3 -> 1 -> 0. The total time taken is 10 + 13 + 13 + 10 = 46 <= 50.
The nodes visited are 0, 1, and 3, giving a maximal path quality of 1 + 2 + 4 = 7.
```

**Constraints**

- n == values.length
- 1 <= n <= 1000
- 0 <= values[i] <= 108
- 0 <= edges.length <= 2000
- edges[j].length == 3
- 0 <= uj < vj <= n - 1
- 10 <= timej, maxTime <= 100
- All the pairs [uj, vj] are unique.
- There are at most four edges connected to each node.
- The graph may not be connected.

---

## 题目（中文翻译）

给定一个无向图，图中有编号为 `0` 到 `n-1`（含）的 `n` 个节点。  
另有一个 **0 索引** 的整数数组 `values`，其中 `values[i]` 表示第 `i` 个节点的价值。  
再给定一个 **0 索引** 的二维整数数组 `edges`，其中 `edges[j] = [uj, vj, timej]` 表示节点 `uj` 与节点 `vj` 之间存在一条无向边，且在这条边上行走需要 `timej` 秒。  
最后给出一个整数 `maxTime`。

一条 **有效路径** 定义为：起点是节点 `0`，终点也是节点 `0`，且整个路径耗时不超过 `maxTime` 秒。路径中可以多次访问同一个节点。  
一条有效路径的 **质量** 为路径上所有 **唯一**（即第一次出现）节点的价值之和——每个节点的价值最多只计入一次。

返回所有有效路径中的最大质量。

> **提示**：每个节点至多有四条相连的边。

---

### 示例

**示例 1**

```text
输入: values = [0,32,10,43], edges = [[0,1,10],[1,2,15],[0,3,10]], maxTime = 49
输出: 75
解释:
一种可能的路径为 0 -> 1 -> 0 -> 3 -> 0。总耗时为 10 + 10 + 10 + 10 = 40 ≤ 49。
访问的节点为 0、1、3，路径质量为 0 + 32 + 43 = 75。
```

**示例 2**

```text
输入: values = [5,10,15,20], edges = [[0,1,10],[1,2,10],[0,3,10]], maxTime = 30
输出: 25
解释:
一种可能的路径为 0 -> 3 -> 0。总耗时为 10 + 10 = 20 ≤ 30。
访问的节点为 0、3，路径质量为 5 + 20 = 25。
```

**示例 3**

```text
输入: values = [1,2,3,4], edges = [[0,1,10],[1,2,11],[2,3,12],[1,3,13]], maxTime = 50
输出: 7
解释:
一种可能的路径为 0 -> 1 -> 3 -> 1 -> 0。总耗时为 10 + 13 + 13 + 10 = 46 ≤ 50。
访问的节点为 0、1、3，路径质量为 1 + 2 + 4 = 7。
```

---

### 约束条件

- `n == values.length`
- `1 ≤ n ≤ 1000`
- `0 ≤ values[i] ≤ 10^8`
- `0 ≤ edges.length ≤ 2000`
- `edges[j].length == 3`
- `0 ≤ uj < vj ≤ n - 1`
- `10 ≤ timej, maxTime ≤ 100`
- 所有 `[uj, vj]` 对均唯一
- 每个节点至多有四条相连的边
- 图可能不是连通的

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的合法路径都枚举一遍**，然后在每条路径上计算质量，取最大值。  

- **路径的定义**：从节点 `0` 出发，最后又回到 `0`，且走的总时间 ≤ `maxTime`。  
- **可以重复走同一个节点**，所以这是一棵 **有向的遍历树**（每走一步都可能分叉），深度受 `maxTime` 限制。  
- **记录已访问的节点**：在遍历的过程中，用一个 `set`（集合）保存已经走过的节点编号。每次走到一个新节点时，把它的价值 `values[node]` 加到当前质量里；如果已经在集合里，则不再重复加。  

> **类比**：把图想成城镇之间的道路，`maxTime` 是你只能花的最多时间。暴力解就像让你把 **所有可能的旅行路线**（在时间限制内）都写下来，再挑出价值最高的那条。

只要我们能把每一步的选择全部列举出来，答案自然就能找到。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Set

def maximalPathQuality(values: List[int], edges: List[List[int]], maxTime: int) -> int:
    # 1️⃣ 建图：邻接表，key 是节点，value 是 (邻居, 所需时间) 的列表
    graph = defaultdict(list)
    for u, v, t in edges:
        graph[u].append((v, t))
        graph[v].append((u, t))

    n = len(values)
    best = 0                       # 记录全局最大质量

    def dfs(node: int, time_used: int, cur_score: int, visited: Set[int]) -> None:
        """深度优先遍历所有合法路径"""
        nonlocal best
        # 每次回到 0，尝试更新答案
        if node == 0:
            best = max(best, cur_score)

        # 超时就不能继续往下走了
        if time_used > maxTime:
            return

        # 2️⃣ 枚举当前节点的所有相邻节点
        for nxt, cost in graph[node]:
            new_time = time_used + cost
            if new_time > maxTime:          # 剪枝：时间已经不够
                continue

            # 判断 nxt 是否是第一次访问
            added = 0
            if nxt not in visited:
                visited.add(nxt)            # 标记为已访问
                added = values[nxt]         # 这一次可以把它的价值加进去

            dfs(nxt, new_time, cur_score + added, visited)

            # 回溯：撤销对 nxt 的访问标记（因为后面的分支仍然需要把它当作未访问）
            if added:
                visited.remove(nxt)

    # 初始状态：已经在 0 位置，已经收集了 values[0]（因为 0 是必经点）
    dfs(0, 0, values[0], {0})
    return best
```

**关键行解释**  

- `graph[u].append((v, t))`：把无向边变成两条有向边，类似在字典里查“从 u 出发能去哪些城镇”。  
- `if node == 0: best = max(best, cur_score)`：只要回到起点，就可以把当前质量当作候选答案。  
- `if new_time > maxTime: continue`：如果这一步已经超时，就不必继续往下搜索（剪枝）。  
- `visited.add(nxt)` / `visited.remove(nxt)`：回溯的核心，确保不同分支之间的“已经访问的节点集合”互不干扰。

#### 复杂度  

- **时间复杂度**：`O(b^d)`（指数级），其中  
  - `b` ≈ 每个节点的平均度数 ≤ 4（因为每个节点至多有四条边），  
  - `d` ≈ `maxTime / min_edge_time`，即在最小耗时的边上能走多少步。  
  换句话说，最坏情况下我们会尝试所有可能的路径，数量随时间限制指数增长。  
- **空间复杂度**：`O(n + d)`  
  - `O(n)` 用于存放图的邻接表，  
  - 递归栈最深为 `d`，再加上 `visited` 集合的大小 ≤ `n`。  

> **大白话**：如果 `maxTime` 是 100，最短边是 10，最多走 10 步；每步有 4 种选择，理论上要检查 4¹⁰ ≈ 1,048,576 条路径。虽然数字不算天文，但在最坏情况下仍会超时。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **盲目遍历所有路径**，即使很多路径已经明显不可能得到更好答案。我们需要 **记忆化**（Memoization）来避免重复计算同样的子问题。

观察可以发现：

1. **状态只和两个因素有关**  
   - 当前所在的节点 `u`  
   - 还剩多少时间 `t`（或者已经用了多少时间）  
   只要这两个信息确定，**从这里出发在剩余时间内能得到的最大质量**是唯一的。  
   已经走过的节点集合不需要放进状态，因为我们只关心**还能再收集到的新增价值**，而已经收集的价值已经在 `cur_score` 中累计。

2. **递归定义**  
   `dp(u, t)` = 在节点 `u`、剩余时间 `t`（即还能再花 `t` 秒）时，**从这里出发最终回到 0** 能得到的最大“额外”质量（不包括已经在 `cur_score` 里累计的部分）。  

   递推式：  
   - 若 `t < 0` → 不合法，返回 `-inf`。  
   - 若 `u == 0` → 已经回到起点，可以选择结束，质量为 `0`（不再收集新价值）。  
   - 对每条相邻边 `(u, v, w)`，如果 `w ≤ t`，我们可以走这条边去 `v`，此时  
     `gain = values[v]`（如果 `v` 之前没被访问过）  
     `dp(u, t) = max(dp(u, t), gain + dp(v, t - w))`  
   为了判断 `v` 是否是“第一次访问”，我们在递归时使用 **全局的 `visited` 集合**，在进入递归前标记、返回后撤销。  

3. **记忆化**  
   用字典 `memo[(u, t)]` 缓存已经算好的 `dp(u, t)`，这样同一个 `(u, t)` 只会计算一次，避免指数级重复。  
   由于 `t` 的取值范围是 `0 … maxTime ≤ 100`，`u` 的取值范围是 `0 … n-1 ≤ 999`，总状态数最多 `1000 * 101 ≈ 1e5`，非常可接受。  

4. **整体流程**  
   - 从 `0` 出发，已收集 `values[0]`，已用时间 `0`。  
   - 调用 `dfs(0, maxTime)`，返回的结果再加上已经收集的 `values[0]` 即为答案。  

> **类比**：把图想成一张地图，`dp(u, t)` 就像是“站在城镇 `u`，手里还有 `t` 天时间，接下来还能赚到的最多金钱”。我们把每个 `(城镇, 剩余时间)` 的最优收益记下来，后面再遇到同样的情况就直接查表，不必重新算。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple, Dict, Set

def maximalPathQuality(values: List[int], edges: List[List[int]], maxTime: int) -> int:
    # 1️⃣ 建图（邻接表）
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    n = len(values)
    memo: Dict[Tuple[int, int], int] = {}   # (node, remaining_time) -> best extra quality
    visited: Set[int] = set()               # 当前递归路径上已经访问过的节点

    def dfs(node: int, remaining: int) -> int:
        """
        返回：在 remaining 秒还能继续走，并且最终必须回到 0 时，
              能再收集到的最大质量（不包括已经在 visited 中的节点价值）。
        """
        if (node, remaining) in memo:               # 记忆化查询
            return memo[(node, remaining)]

        # 如果已经回到起点，可以选择不再继续，质量为 0（因为已经在 cur_score 里算过）
        best_extra = 0 if node == 0 else -float('inf')

        # 枚举所有相邻的边
        for nxt, cost in graph[node]:
            if cost > remaining:                     # 没时间走这条边，直接跳过
                continue

            added = 0
            newly_visited = False
            if nxt not in visited:                  # 第一次踏入 nxt，能收获它的价值
                added = values[nxt]
                visited.add(nxt)
                newly_visited = True

            # 递归求 nxt 位置、剩余时间的最优质量
            candidate = added + dfs(nxt, remaining - cost)
            best_extra = max(best_extra, candidate)

            # 回溯，撤销标记
            if newly_visited:
                visited.remove(nxt)

        memo[(node, remaining)] = best_extra
        return best_extra

    # 初始状态：已经在 0，已经收集了 values[0]，把 0 放进 visited
    visited.add(0)
    answer = values[0] + dfs(0, maxTime)
    return answer
```

**关键行解释**  

- `if (node, remaining) in memo:`：查询缓存，防止同一个子问题被重复求解。  
- `best_extra = 0 if node == 0 else -inf`：只有站在起点时才可以直接“结束”，否则必须继续走（否则质量为负无穷）。  
- `if nxt not in visited:`：只在第一次经过某节点时把它的价值加入 `added`，这正是题目“唯一节点价值只算一次”的要求。  
- `candidate = added + dfs(nxt, remaining - cost)`：当前这一步收获的价值 + 从下一节点继续走的最优价值。  
- `visited.remove(nxt)`：典型的 **回溯**，保证其他分支不受影响。  

#### 复杂度  

- **时间复杂度**：`O(n * maxTime * deg)`  
  - 状态数 `n * (maxTime+1)` ≤ `1000 * 101 ≈ 1e5`。  
  - 对每个状态我们遍历它的所有邻居，度数 `deg ≤ 4`。  
  - 因此总体约为 `4 * 1e5 = 4e5` 次递归调用，远低于暴力的指数级。  
  - **含义**：相当于把“所有可能的路径”压缩成“每个节点在每个剩余时间下的最优结果”，大幅降低计算量。  

- **空间复杂度**：`O(n * maxTime + n)`  
  - `memo` 表占用 `O(n * maxTime)`。  
  - `visited` 集合最多保存 `n` 个节点。  
  - 递归栈深度最多 `maxTime / min_edge_time ≤ 100 / 10 = 10`（实际更小），因此栈空间可以忽略不计。  

> 与暴力解相比，时间从指数级降到线性（相对于 `n * maxTime`），空间稍增但仍在几百 KB 级别，完全可以接受。

---

## 心得  

- **核心技巧**：**记忆化深度优先搜索（DFS + Memo）**，把“当前位置 + 剩余时间”作为状态进行缓存。  
- **适用的题型**  
  1. **受时间/步数限制的图遍历**（如 “Maximum Probability Path” 类似的概率版）。  
  2. **带资源消耗的路径问题**（如 “Minimum Cost to Reach Destination With Fuel”）。  
  3. **需要统计唯一节点价值的回路问题**（如本题）。  
- **一句话总结解题钥匙**：**把“路径枚举”压缩成“状态转移”，用记忆化避免重复子问题**。

---

## 反思  

- **第一反应**：看到“路径必须回到 0，时间 ≤ maxTime”，立刻想到“枚举所有路径”。这在没有注意到 `maxTime ≤ 100`、每个节点度数 ≤ 4 时会导致指数爆炸。  
- **最容易踩的坑**  
  1. **忘记只计一次价值**：在回溯时必须在 `visited` 中正确加入/删除节点，否则会重复计数。  
  2. **剪枝不够**：仅凭 `time_used > maxTime` 剪枝仍会遍历大量不可能的分支。记忆化是关键的“高效剪枝”。  
  3. **边界条件**：当 `node == 0` 时可以直接结束并返回 0；若写成 `return cur_score` 会导致多计一次 `values[0]`。  
- **下次遇到同类题**：第一步先**思考能否把“剩余资源 + 当前所在位置”作为状态**，如果可以，就立刻尝试**记忆化 DFS / DP**，而不是盲目枚举全部路径。这样往往能把难度从 *Hard* 降到 *Medium* 甚至 *Easy*。