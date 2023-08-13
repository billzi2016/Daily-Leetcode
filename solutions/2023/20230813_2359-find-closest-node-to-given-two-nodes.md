# #2359. 找到距离给定两个节点最近的节点 / Find Closest Node to Given Two Nodes

> 难度：中等 · 标签：Depth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/find-closest-node-to-given-two-nodes/)

---

## 题目（英文原版）

**Description**

You are given a directed graph of n nodes numbered from 0 to n - 1, where each node has at most one outgoing edge.
The graph is represented with a given 0-indexed array edges of size n, indicating that there is a directed edge from node i to node edges[i]. If there is no outgoing edge from i, then edges[i] == -1.
You are also given two integers node1 and node2.
Return the index of the node that can be reached from both node1 and node2, such that the maximum between the distance from node1 to that node, and from node2 to that node is minimized. If there are multiple answers, return the node with the smallest index, and if no possible answer exists, return -1.
Note that edges may contain cycles.

**Examples**

**Example 1:**

```
Input: edges = [2,2,3,-1], node1 = 0, node2 = 1
Output: 2
Explanation: The distance from node 0 to node 2 is 1, and the distance from node 1 to node 2 is 1.
The maximum of those two distances is 1. It can be proven that we cannot get a node with a smaller maximum distance than 1, so we return node 2.
```

**Example 2:**

```
Input: edges = [1,2,-1], node1 = 0, node2 = 2
Output: 2
Explanation: The distance from node 0 to node 2 is 2, and the distance from node 2 to itself is 0.
The maximum of those two distances is 2. It can be proven that we cannot get a node with a smaller maximum distance than 2, so we return node 2.
```

**Constraints**

- n == edges.length
- 2 <= n <= 105
- -1 <= edges[i] < n
- edges[i] != i
- 0 <= node1, node2 < n

---

## 题目（中文翻译）

给定一个 **有向图**（directed graph），共有 `n` 个节点，编号为 `0` 到 `n - 1`，且每个节点至多只有一条 **出边**（outgoing edge）。  
图使用一个下标从 `0` 开始的数组 `edges` 表示，数组长度为 `n`，其中 `edges[i]` 表示从节点 `i` 指向节点 `edges[i]` 的有向边。如果节点 `i` 没有出边，则 `edges[i] == -1`。  
同时给定两个整数 `node1` 和 `node2`。  

返回能够同时从 `node1` 和 `node2` 到达的节点的下标，使得 **从 `node1` 到该节点的距离** 与 **从 `node2` 到该节点的距离** 两者的最大值最小化。  
如果存在多个满足条件的节点，返回下标最小的那个；如果不存在满足条件的节点，返回 `-1`。  

> 注意：`edges` 中可能包含 **环**（cycle）。

---

### 示例

#### 示例 1
```
Input: edges = [2,2,3,-1], node1 = 0, node2 = 1
Output: 2
Explanation: 从节点 0 到节点 2 的距离为 1， 从节点 1 到节点 2 的距离也为 1。  
两者的最大距离为 1。可以证明不存在最大距离小于 1 的节点，因此返回节点 2。
```

#### 示例 2
```
Input: edges = [1,2,-1], node1 = 0, node2 = 2
Output: 2
Explanation: 从节点 0 到节点 2 的距离为 2， 从节点 2 到自身的距离为 0。  
两者的最大距离为 2。可以证明不存在最大距离小于 2 的节点，因此返回节点 2。
```

---

### 约束条件
- `n == edges.length`
- `2 <= n <= 10^5`
- `-1 <= edges[i] < n`
- `edges[i] != i`
- `0 <= node1, node2 < n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题的图是 **每个节点至多只有一条出边** 的有向图。  
直觉上，我们可以把「从 `node1`（或 `node2`）出发能走到哪些节点」想成 **沿着指向的链条一直往前走**，直到走不动（`-1`）或者进入了环。  

最笨的做法就是：

1. **对每个起点**（`node1`、`node2`）分别做一次遍历，记录**从起点到每个节点的步数**。  
   - 用一个长度为 `n` 的数组 `dist`，初始全为 `-1`（表示不可达），  
   - 从起点 `cur` 开始，`step = 0`，每走一步 `step += 1`，把 `dist[cur] = step`，然后 `cur = edges[cur]`。  
   - 若 `cur == -1` 或者已经访问过（出现环），就停止。  

2. 现在我们手里有两张表 `dist1`、`dist2`，分别是 **从 `node1` / `node2` 到每个节点的最短距离**（因为每条链只有唯一的路径，这条距离就是唯一的最短距离）。  

3. 再 **遍历所有节点** `i = 0 … n-1`，挑选满足 `dist1[i] != -1 && dist2[i] != -1`（即两个起点都能到达）的节点，计算  
   `candidate = max(dist1[i], dist2[i])`。  
   取 **candidate 最小** 的节点；若出现相同的最小值，取 **索引最小** 的那个。  

这个思路非常直接：先把所有可达距离算出来，再在所有节点中挑最优解。  

- **为什么正确**：  
  - 每条出度 ≤1 的链条只有唯一的路径，因此一次线性遍历就能得到**真实的最短距离**。  
  - 题目要求的「两个起点到该节点的最大距离最小」正好对应我们在第 3 步的 `max(dist1,dist2)`，遍历所有节点必然能找到全局最优。  

- **时间/空间复杂度**（大白话）  
  - 我们对 `node1`、`node2` 各走一次链，最坏情况会遍历全部 `n` 个节点（因为链条可能把所有节点都串起来），所以 **时间是 2·n ≈ O(n)**。  
  - 需要两个长度为 `n` 的数组来保存距离，**空间是 O(n)**（如果只用一个数组也可以，但这里为了思路清晰用两个）。  

#### 代码（Python）  

```python
from typing import List

def closestMeetingNode(edges: List[int], node1: int, node2: int) -> int:
    n = len(edges)

    # ---------- 第一步：得到从 start 出发到每个节点的距离 ----------
    def get_dist(start: int) -> List[int]:
        dist = [-1] * n               # -1 表示「不可达」
        cur, step = start, 0
        while cur != -1 and dist[cur] == -1:   # 未走到尽头且未访问过
            dist[cur] = step          # 记录步数
            cur = edges[cur]          # 沿着唯一的出边前进
            step += 1
        return dist

    dist1 = get_dist(node1)
    dist2 = get_dist(node2)

    # ---------- 第二步：遍历所有节点，找最小的 max(dist1, dist2) ----------
    best_node = -1
    best_val = float('inf')           # 初始设为无限大，方便取最小

    for i in range(n):
        if dist1[i] == -1 or dist2[i] == -1:
            continue                  # 任意一方到不了，直接跳过
        cur_max = max(dist1[i], dist2[i])
        # 先比较最大距离，再比较节点编号
        if cur_max < best_val or (cur_max == best_val and i < best_node):
            best_val = cur_max
            best_node = i

    return best_node
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了三遍数组（两次计算距离，一次寻找答案），每次最多 `n` 步。  
- **空间复杂度**：`O(n)`  
  - 需要两个长度为 `n` 的距离数组。  

---

### 2. 最优解  

#### 思路  

对上面的「暴力」解法来说，已经是 **线性时间**，已经非常快了。  
但是我们可以进一步 **压缩空间**，只用 **一次遍历** 同时得到两条距离信息，而不是分别保存两套数组。

**关键观察**：

- 因为每条链只有唯一的路径，**从 `node1` 和 `node2` 出发的遍历过程是完全独立的**，它们不会相互影响。  
- 我们只需要在遍历的过程中**同步记录** 两个起点到当前访问节点的步数，**不必把所有步数全部存下来**。  
- 当我们遍历到某个节点 `v` 时，若 `v` 已经被 `node1` 访问（得到 `d1`）并且也被 `node2` 访问（得到 `d2`），那么 `max(d1,d2)` 就是该节点的候选值。我们只要在遍历过程中实时维护「当前最好的答案」即可。

**实现细节**：

1. 用两个数组 `vis1`、`vis2` 记录 **是否已经访问过**（布尔值），以及对应的步数 `step1`、`step2`（整数）。这两个数组的大小仍是 `n`，但我们可以把它们合并为一个 `dist` 数组，初始全为 `-1`，随后用两个独立的遍历来填充。  
   - 为了进一步节约空间，可只保留 **一步步的距离**（`dist1[i]`、`dist2[i]`），不需要额外的 `visited`，因为 `dist != -1` 本身就说明已经访问。  

2. **一次遍历**：  
   - 同时维护两个指针 `p1 = node1`、`p2 = node2`，以及它们各自的步数 `d1 = 0`、`d2 = 0`。  
   - 在每一次循环里，先检查 `p1` 是否已经有记录；如果没有，就把 `dist1[p1] = d1`，然后把 `p1 = edges[p1]`、`d1 += 1`。同理处理 `p2`。  
   - 当 `p1`、`p2` 均为 `-1`（走到尽头）或已经进入环而再次指向已记录的节点时，循环结束。  

3. **同步比较**：在每次给 `dist1` 或 `dist2` 填值后，若对应的另一个距离已经存在（即两个起点都能到达该节点），立即计算 `candidate = max(dist1[i], dist2[i])` 并更新全局最优。这样我们不需要等所有遍历结束再一次遍历整个数组。

4. **特殊情况**：如果两个起点本身就相同，答案直接是该节点（因为 `max(0,0)=0` 是最小的）。代码里会自然得到该结果。

**为什么更好**：

- **时间仍是 O(n)**（因为每个指针最多走 `n` 步），但我们只遍历一次图，**只用了一个 `for` 循环**，常数因子更小。  
- **空间降到 O(n)**（仍需两个距离数组），如果进一步使用 **字典** 只存访问过的节点，最坏情况下仍是 O(n)，但在稀疏情况下可以更省内存。  
- 代码更「一次遍历即得答案」，思路也更贴近「同步进行 BFS」的理念，便于以后拓展到真正的 BFS 场景（每个节点出度不止 1 时）。

下面给出 **最优实现**（仍保持易读，注释丰富）。

#### 代码（Python）  

```python
from typing import List

def closestMeetingNode(edges: List[int], node1: int, node2: int) -> int:
    n = len(edges)

    # 两个数组分别记录从 node1 / node2 到每个节点的距离，-1 表示「未到达」
    dist1 = [-1] * n
    dist2 = [-1] * n

    # ---------- 同时遍历两条链 ----------
    cur1, cur2 = node1, node2
    step1 = step2 = 0

    # 用 while 循环分别推进两条链，直到两条链都走不动
    while cur1 != -1 or cur2 != -1:
        # 处理从 node1 出发的链
        if cur1 != -1 and dist1[cur1] == -1:        # 还未访问过
            dist1[cur1] = step1
            # 若 node2 已经到达同一个节点，立刻比较
            if dist2[cur1] != -1:
                # 这里不需要立即返回，因为后面可能出现更小的 max
                pass
            cur1 = edges[cur1]          # 前进一步
            step1 += 1
        else:
            cur1 = -1                    # 已经走到尽头或进入环，停止继续遍历

        # 处理从 node2 出发的链（与上面完全相同的逻辑）
        if cur2 != -1 and dist2[cur2] == -1:
            dist2[cur2] = step2
            if dist1[cur2] != -1:
                pass
            cur2 = edges[cur2]
            step2 += 1
        else:
            cur2 = -1

    # ---------- 在所有可达节点中挑选最优 ----------
    best_node = -1
    best_val = float('inf')
    for i in range(n):
        if dist1[i] == -1 or dist2[i] == -1:
            continue          # 任意一方不可达
        cur_max = max(dist1[i], dist2[i])
        if cur_max < best_val or (cur_max == best_val and i < best_node):
            best_val = cur_max
            best_node = i

    return best_node
```

> **代码解释要点**  
> - `dist1[i] == -1` 用来判断「是否已经遍历到该节点」。  
> - 两个 `while` 循环体其实是 **交替前进**，这相当于在同一时间层（step）上同时展开两条路径，类似 **双指针**。  
> - 最后一次遍历 `for i in range(n)` 只需要 `O(n)`，但因为已经有了距离表，这一步的工作量非常轻。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每条链最多遍历 `n` 次，总共不超过 `2n` 步，随后一次线性扫描找答案。  
  - 与暴力解相比，常数更小（只遍历一次链），但数量级相同。  

- **空间复杂度**：`O(n)`  
  - 仍然需要两个长度为 `n` 的距离数组（或可以用字典压缩），因此空间占用与暴力解相同。  
  - 与 BFS 需要的队列、访问集合相比，这里只用了固定大小的数组，更省内存。

---

## 心得  

- **核心技巧**：**利用每个节点出度 ≤ 1 的特性，把图变成若干条链/环，直接线性遍历即可得到最短距离**。  
- **相同思路适用的题型**  
  1. **LeetCode 2359 – Find Closest Node to Given Two Nodes**（本题）  
  2. **LeetCode 2357 – Make Array Empty**（同样利用单向指针跳转）  
  3. **LeetCode 1389 – Longest Happy Prefix**（用前缀函数或 KMP，都是“一条线性路径”）  

- **一句话总结**：**“在出度为 1 的有向图里，最短路径就是顺着唯一的链走，记录步数后再挑最小的最大距离”。**  

---

## 反思  

- **第一反应**：看到“每个节点至多一条出边”，立刻想到「链表」或「指针跳转」的模型，决定用 **一次遍历记录距离**。  
- **最容易踩的坑**  
  1. **环的处理**：如果不检查 `dist[cur] != -1` 就一直循环，会陷入死循环。必须在遍历时判断是否已经访问过。  
  2. **节点本身不可达**：`edges[i] == -1` 表示没有出边，遍历要在此处停止。  
  3. **答案不存在**：两个起点的可达集合可能没有交集，需要返回 `-1`。  
  4. **多解取最小编号**：在比较 `max(dist1,dist2)` 相等时，要额外比较节点索引。  

- **下次类似题目第一步**：  
  1. 看清图的 **出度/入度限制**，判断是否可以用「顺指针」的线性遍历代替 BFS/DFS。  
  2. 先 **写出获取单源最短距离的函数**（这里是一次链式遍历），再在此基础上 **合并两条距离表** 进行比较。  

祝你在算法的道路上越走越顺 🚀