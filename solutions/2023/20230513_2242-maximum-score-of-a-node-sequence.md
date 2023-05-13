# #2242. 节点序列的最大得分 / Maximum Score of a Node Sequence

> 难度：困难 · 标签：Array、Graph、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-score-of-a-node-sequence/)

---

## 题目（英文原版）

**Description**

There is an undirected graph with n nodes, numbered from 0 to n - 1.
You are given a 0-indexed integer array scores of length n where scores[i] denotes the score of node i. You are also given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
A node sequence is valid if it meets the following conditions:
The score of a node sequence is defined as the sum of the scores of the nodes in the sequence.
Return the maximum score of a valid node sequence with a length of 4. If no such sequence exists, return -1.

**Examples**

**Example 1:**

```
Input: scores = [5,2,9,8,4], edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]
Output: 24
Explanation: The figure above shows the graph and the chosen node sequence [0,1,2,3].
The score of the node sequence is 5 + 2 + 9 + 8 = 24.
It can be shown that no other node sequence has a score of more than 24.
Note that the sequences [3,1,2,0] and [1,0,2,3] are also valid and have a score of 24.
The sequence [0,3,2,4] is not valid since no edge connects nodes 0 and 3.
```

**Example 2:**

```
Input: scores = [9,20,6,4,11,12], edges = [[0,3],[5,3],[2,4],[1,3]]
Output: -1
Explanation: The figure above shows the graph.
There are no valid node sequences of length 4, so we return -1.
```

**Constraints**

- n == scores.length
- 4 <= n <= 5 * 104
- 1 <= scores[i] <= 108
- 0 <= edges.length <= 5 * 104
- edges[i].length == 2
- 0 <= ai, bi <= n - 1
- ai != bi
- There are no duplicate edges.

---

## 题目（中文翻译）

有一个 **无向图**（undirected graph），包含 `n` 个节点，编号为 `0` 到 `n‑1`。  
给定一个下标从 `0` 开始的整数数组 `scores`（长度为 `n`），其中 `scores[i]` 表示节点 `i` 的得分。  
同时给定一个二维整数数组 `edges`，`edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条 **无向边**（undirected edge）。

若一个节点序列 `(a, b, c, d)` 同时满足以下条件，则称其为 **有效序列**（valid）：

1. 序列长度恰为 `4`（即包含四个节点）。  
2. 四个节点两两不同。  
3. 相邻节点之间都有边相连，即存在边 `[a, b]`、`[b, c]`、`[c, d]`。

节点序列的 **得分** 定义为序列中四个节点得分的总和，即 `scores[a] + scores[b] + scores[c] + scores[d]`。  

返回所有有效节点序列中可能的 **最大得分**。如果不存在满足条件的序列，返回 `-1`。

---

### 示例

**示例 1**

```text
Input: scores = [5,2,9,8,4], edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]
Output: 24
Explanation: 上图展示了该图以及选取的节点序列 [0,1,2,3]。  
该序列的得分为 5 + 2 + 9 + 8 = 24。  
可以证明没有其他长度为 4 的有效序列的得分超过 24。  
注意序列 [3,1,2,0] 和 [1,0,2,3] 也是有效的，得分同样为 24。
```

**示例 2**

```text
Input: scores = [9,20,6,4,11,12], edges = [[0,3],[5,3],[2,4],[1,3]]
Output: -1
Explanation: 上图展示了该图。  
图中不存在长度为 4 的有效节点序列，因此返回 -1。
```

---

### 约束条件

- `n == scores.length`
- `4 <= n <= 5 * 10^4`
- `1 <= scores[i] <= 10^8`
- `0 <= edges.length <= 5 * 10^4`
- `edges[i].length == 2`
- `0 <= a_i, b_i <= n - 1`
- `a_i != b_i`
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的长度为 4 的节点序列** 都枚举一遍，检查它们是否满足「相邻节点之间都有边」的条件，然后把满足条件的序列的分数相加，取最大值。

- **数据结构**  
  - 用 **邻接矩阵**（二维布尔数组）来判断两点之间是否有边。邻接矩阵就像一本「是否相连」的字典，`matrix[u][v] = True` 表示词 `u` 的定义里出现了词 `v`，查找时只要看一眼就能知道。  
  - `scores` 本身就是一个一维数组，直接存每个节点的得分。

- **正确性**  
  只要遍历到了所有合法的 4‑node 序列，就一定不会漏掉最优解；而每次判断 `matrix[a][b] && matrix[b][c] && matrix[c][d]` 能确保序列中每两个相邻节点都有边，因此满足题目要求。

- **时间/空间复杂度**  
  - **时间**：枚举 4 个不同的节点，需要四层循环，时间是 `O(n^4)`。  
    - `O(n^4)` 可以想象成「如果有 1000 个节点，最坏情况要检查 1000⁴ ≈ 10¹² 次」，这在电脑里几乎不可能跑完。  
  - **空间**：邻接矩阵占 `O(n^2)` 的空间（`n` 最多 5·10⁴，矩阵会有 2.5·10⁹ 条记录，根本装不下），所以这种实现根本不可行。

#### 代码（Python）

```python
def maxScoreBruteForce(scores, edges):
    n = len(scores)
    # 建立邻接矩阵，matrix[u][v] 为 True 表示 u 与 v 直接相连
    matrix = [[False] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = matrix[v][u] = True

    ans = -1
    # 四层循环枚举四个不同的节点 a,b,c,d（顺序很重要）
    for a in range(n):
        for b in range(n):
            if b == a or not matrix[a][b]:
                continue
            for c in range(n):
                if c in (a, b) or not matrix[b][c]:
                    continue
                for d in range(n):
                    if d in (a, b, c) or not matrix[c][d]:
                        continue
                    # 此时 a-b-c-d 构成合法序列
                    cur = scores[a] + scores[b] + scores[c] + scores[d]
                    ans = max(ans, cur)
    return ans
```

> **注意**：上述代码仅作思路展示，实际运行会因 `O(n^4)` 的时间和 `O(n^2)` 的内存而 **超时 / 内存爆炸**。

#### 复杂度

- **时间复杂度**：`O(n^4)` —— 四层循环，每层最多遍历 `n` 次，类似「把 n 本书每本都挑四遍」的工作量，随着 `n` 增大，耗时呈四次方增长，几乎不可能在 1 秒内完成。
- **空间复杂度**：`O(n^2)` —— 邻接矩阵需要 `n×n` 的布尔表，`n=5·10⁴` 时已经超过 2 GB，超出常规在线评测的内存限制。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：

1. **枚举全部四元组**（`O(n^4)`）太慢。  
2. **存邻接矩阵**（`O(n^2)`）占用太多内存。

我们要 **把搜索范围压缩**，只在「可能出现的」组合上做搜索。关键观察来自题目提示：

> 把序列的「中间两个」节点固定（记为 `b`、`c`），它们之间一定有一条边 `b‑c`。其余两个节点分别只能和 `b`、`c` 中的一个相连。

于是我们可以把问题转化为：

> 对每条边 `b‑c`，挑选一个与 `b` 相连且不等于 `c` 的节点 `a`，以及一个与 `c` 相连且不等于 `b` 的节点 `d`，使得 `scores[a] + scores[b] + scores[c] + scores[d]` 最大，并且 `a、b、c、d` 四个节点互不相同。

这一步把 **四元组** 的枚举变成 **边 + 两个邻居** 的枚举。仍然需要在每个节点的邻居里挑选「最高分」的那个，但要避免 **选到同一个节点**（比如 `a` 可能正好是 `d`）。

**如何快速得到「每个节点的最高分邻居」？**

- 对每个节点 `v`，我们只需要记录 **分数最高的前 3（或 4）个相邻节点**。为什么是 3？  
  - 当我们固定 `b‑c` 时，需要为 `b` 选一个 `a`，为 `c` 选一个 `d`。如果 `b` 的最高邻居恰好是 `c`（不可用），我们就要看第二高、第三高……  
  - 最糟的情况是 `b` 与 `c` 各自的前两名都冲突（比如 `b` 的前两名都是 `c` 和某个公共节点），此时我们需要 **第三名** 来确保能找到不冲突的候选。  
  - 因此 **存 3 个** 足够保证在不重复的前提下总能取到一个可行的 `a`（或 `d`），如果仍然冲突则说明该边无法组成合法序列。

**整体步骤**

1. **构建邻接表**（每个节点的所有直接相邻节点列表），类似「朋友列表」。
2. **遍历每个节点的邻居**，把邻居按照分数从高到低排序，只保留前 3 个（如果邻居不足 3 个，就全部保留）。这一步的时间是 `O(m log m)`，其中 `m = edges.length`，因为每条边会被加入两个节点的列表中，排序的代价在 `m` 规模下是可以接受的。
3. **遍历每条边 `b‑c`**（每条边只考虑一次），从 `b` 的「前 3 高分邻居」中挑一个不等于 `c`、不等于 `d` 的节点 `a`，同理从 `c` 的列表中挑 `d`。我们尝试所有合法组合（最多 `3 × 3 = 9` 种），计算分数并取最大。
4. 若遍历完所有边仍未找到合法序列，返回 `-1`。

**为什么时间可以接受？**

- 每条边最多检查 9 种组合，`edges ≤ 5·10⁴`，所以总操作数约为 `9·5·10⁴ ≈ 4.5·10⁵`，远远小于 1 秒可以完成的量级。  
- 存储每个节点的前 3 个邻居只需要 `O(n·3)` 的额外空间，几乎可以忽略不计。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maxScore(scores: List[int], edges: List[List[int]]) -> int:
    n = len(scores)

    # 1️⃣ 建立邻接表：node -> list of (neighbor, neighbor_score)
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append((v, scores[v]))
        adj[v].append((u, scores[u]))

    # 2️⃣ 为每个节点保留分数最高的前 3 个邻居（按照得分降序）
    top3 = {}                     # node -> list of neighbor ids (按得分高到低)
    for node in range(n):
        # 按分数从大到小排序
        neigh = sorted(adj[node], key=lambda x: x[1], reverse=True)
        # 只取前 3 个邻居的 id
        top3[node] = [v for v, _ in neigh[:3]]

    ans = -1

    # 3️⃣ 枚举每条边作为「中间」的 b-c
    for b, c in edges:
        # 为了避免重复计算，统一把 (b,c) 当作有序对
        # 取 b 的候选 a，c 的候选 d
        cand_a = top3[b]
        cand_d = top3[c]

        for a in cand_a:
            if a == c:               # a 不能是 c
                continue
            for d in cand_d:
                if d == b or d == a: # d 不能是 b，也不能和 a 重复
                    continue
                # 此时 a-b-c-d 四节点互不相同且相邻都有边
                cur = scores[a] + scores[b] + scores[c] + scores[d]
                ans = max(ans, cur)

    return ans
```

> **代码说明**  
> - 第 1 步的 `adj` 用列表存「邻居 + 他们的得分」，类似「每个人的朋友名单」并把每个朋友的分数标记在旁边，后面排序时直接用分数比较。  
> - 第 2 步的 `top3` 只保存邻居的 **节点编号**，因为我们只需要在后面取出节点来计算分数。  
> - 第 3 步遍历每条边，只检查最多 9 种组合（3×3），并用 `continue` 跳过冲突的情况。

#### 复杂度

- **时间复杂度**  
  - 建邻接表：`O(m)`（每条边加入两次）。  
  - 为每个节点排序并取前 3：`O(m log m)`（总的邻接条目数是 `2m`，排序每个列表的代价累计为 `O(m log m)`，在本题数据范围内足够快）。  
  - 枚举每条边并检查最多 9 种组合：`O(m)`。  
  - **整体** 为 `O(m log m)`，其中 `m = edges.length ≤ 5·10⁴`。  
    - 与暴力的 `O(n⁴)` 相比，已经把指数级降到了几乎线性级，实际运行只需几毫秒。

- **空间复杂度**  
  - 邻接表存 `2m` 条记录：`O(m)`。  
  - `top3` 只保存每个节点最多 3 个整数：`O(n)`。  
  - **整体** 为 `O(n + m)`，远低于邻接矩阵的 `O(n²)`，在题目限制下完全可以放进内存。

---

## 心得

- **核心技巧**：**对每条边固定中间两点，分别挑选两端的最高分邻居**。本质是把「四元组」的搜索空间压缩到「边 + 常数个候选」的层级。  
- **适用场景**  
  1. 需要在图中找固定长度路径/序列且路径内部必须相邻的情况（如本题的长度 4）。  
  2. “中心‑两侧”结构的优化，如求最大权值的三角形、四边形等，只要把中心固定，外围只取高权值邻居。  
  3. 类似的题目还有 **Maximum Score of a Pair of Nodes**（固定一条边，选两侧最高分节点）或 **Maximum Sum of a Triangle in a Graph**（固定一条边，选两侧最高分形成三角形）。  

- **一句话总结解题钥匙**  
  > **把「中间」固定，外围只保留「最高分」的常数个邻居，就能在 O(m) 级别穷举所有可能的最佳序列。**

---

## 反思

- **第一反应**：看到「长度为 4 的合法序列」就想到直接枚举四个节点，导致想到暴力 `O(n⁴)` 的解法。  
- **最容易踩的坑**  
  1. **重复节点**：在选 `a`、`d` 时忘记排除与 `b、c` 重复的情况，容易得到非法序列。  
  2. **邻居不足**：某些节点的度可能小于 3，代码必须能安全处理列表长度不足的情况（直接取全部）。  
  3. **边的方向**：因为是无向图，遍历 `edges` 时不必两次考虑 `b‑c` 与 `c‑b`，否则会重复计算。  
- **下次类似题的第一步**  
  > **先找出「核心」结构（如一条必出现的边或节点），把问题划分为「核心」+「外围」两部分，再只保留外围的高价值候选**。这样可以把指数级搜索压到常数倍的线性搜索。