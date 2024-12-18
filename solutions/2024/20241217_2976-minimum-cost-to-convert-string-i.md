# #2976. 将字符串转换的最小成本 I / Minimum Cost to Convert String I

> 难度：中等 · 标签：Array、String、Graph、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-convert-string-i/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed strings source and target, both of length n and consisting of lowercase English letters. You are also given two 0-indexed character arrays original and changed, and an integer array cost, where cost[i] represents the cost of changing the character original[i] to the character changed[i].
You start with the string source. In one operation, you can pick a character x from the string and change it to the character y at a cost of z if there exists any index j such that cost[j] == z, original[j] == x, and changed[j] == y.
Return the minimum cost to convert the string source to the string target using any number of operations. If it is impossible to convert source to target, return -1.
Note that there may exist indices i, j such that original[j] == original[i] and changed[j] == changed[i].

**Examples**

**Example 1:**

```
Input: source = "abcd", target = "acbe", original = ["a","b","c","c","e","d"], changed = ["b","c","b","e","b","e"], cost = [2,5,5,1,2,20]
Output: 28
Explanation: To convert the string "abcd" to string "acbe":
- Change value at index 1 from 'b' to 'c' at a cost of 5.
- Change value at index 2 from 'c' to 'e' at a cost of 1.
- Change value at index 2 from 'e' to 'b' at a cost of 2.
- Change value at index 3 from 'd' to 'e' at a cost of 20.
The total cost incurred is 5 + 1 + 2 + 20 = 28.
It can be shown that this is the minimum possible cost.
```

**Example 2:**

```
Input: source = "aaaa", target = "bbbb", original = ["a","c"], changed = ["c","b"], cost = [1,2]
Output: 12
Explanation: To change the character 'a' to 'b' change the character 'a' to 'c' at a cost of 1, followed by changing the character 'c' to 'b' at a cost of 2, for a total cost of 1 + 2 = 3. To change all occurrences of 'a' to 'b', a total cost of 3 * 4 = 12 is incurred.
```

**Example 3:**

```
Input: source = "abcd", target = "abce", original = ["a"], changed = ["e"], cost = [10000]
Output: -1
Explanation: It is impossible to convert source to target because the value at index 3 cannot be changed from 'd' to 'e'.
```

**Constraints**

- 1 <= source.length == target.length <= 105
- source, target consist of lowercase English letters.
- 1 <= cost.length == original.length == changed.length <= 2000
- original[i], changed[i] are lowercase English letters.
- 1 <= cost[i] <= 106
- original[i] != changed[i]

---

## 题目（中文翻译）

你得到两个下标从 **0** 开始的字符串 `source` 和 `target`，两者长度相等且仅包含小写英文字母。另有两个下标从 **0** 开始的字符数组 `original`、`changed`，以及整数数组 `cost`，其中 `cost[i]` 表示将字符 `original[i]` 改为字符 `changed[i]` 的花费。

从字符串 `source` 开始。一次操作可以选择字符串中的任意字符 `x`，若存在下标 `j` 满足 `cost[j] == z`、`original[j] == x` 且 `changed[j] == y`，则可以将该字符改为 `y`，花费为 `z`。

返回将 `source` 转换为 `target` 所需的最小花费，操作次数不限。如果无法完成转换，返回 **-1**。  
注意，可能存在下标 `i, j` 使得 `original[i] == original[j]` 且 `changed[i] == changed[j]`。

---

### 示例

**示例 1**  
```text
Input: source = "abcd", target = "acbe", original = ["a","b","c","c","e","d"], changed = ["b","c","b","e","b","e"], cost = [2,5,5,1,2,20]
Output: 28
Explanation: 将字符串 "abcd" 转换为 "acbe" 的过程如下：
- 将下标 1 处的字符 'b' 改为 'c'，花费 5。
- 将下标 2 处的字符 'c' 改为 'e'，花费 1。
- 将下标 2 处的字符 'e' 改为 'b'，花费 2。
- 将下标 3 处的字符 'd' 改为 'e'，花费 20。
总费用为 5 + 1 + 2 + 20 = 28。
```

**示例 2**  
```text
Input: source = "aaaa", target = "bbbb", original = ["a","c"], changed = ["c","b"], cost = [1,2]
Output: 12
Explanation: 将字符 'a' 转换为 'b' 的最优路径是先将 'a' 改为 'c'（花费 1），再将 'c' 改为 'b'（花费 2），单个字符的总费用为 1 + 2 = 3。  
因为 `source` 中共有 4 个 'a'，最终总费用为 3 * 4 = 12。
```

**示例 3**  
```text
Input: source = "abcd", target = "abce", original = ["a"], changed = ["e"], cost = [10000]
Output: -1
Explanation: 无法将下标 3 处的字符 'd' 改为 'e'，因此无法完成转换，返回 -1。
```

---

### 约束条件

- $1 \le \text{source.length} = \text{target.length} \le 10^5$
- `source`、`target` 只包含小写英文字母。
- $1 \le \text{cost.length} = \text{original.length} = \text{changed.length} \le 2000$
- `original[i]`、`changed[i]` 为小写英文字母。
- $1 \le \text{cost[i]} \le 10^6$
- `original[i] \ne changed[i]`   (每条转换规则的起始字符与目标字符不同)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每个小写字母看成**图的节点**（总共 26 个），  
如果题目给出 `original[j] = x`、`changed[j] = y`、`cost[j] = z`，就相当于在图中加入一条从 `x` 到 `y` 的**有向边**，权重是 `z`（把它想成从字母 `x` 到字母 `y` 的“邮费”）。  

最直接的做法是：  
* 对于字符串中每一个位置 `i`，我们只关心从 `source[i]` 到 `target[i]` 的最小花费。  
* 对这对字符单独跑一次最短路算法（比如 Dijkstra），得到最小费用 `dist[source[i]][target[i]]`。  
* 把所有位置的费用累加起来就是答案；如果某对字符没有路径，则返回 `-1`。

> **为什么正确**  
> 图的每条边对应一次合法的字符转换，路径的总权重就是一次连续转换的总花费。最短路径自然给出最省钱的转换序列，所以对每个字符对求最短路即可。

> **时间/空间分析（大白话）**  
> - **时间**：字符串长度记作 `n`（最多 10⁵），图中最多有 26 个节点，边的数量最多 `len(original)` ≤ 2000。对每个位置我们都跑一次 Dijkstra，复杂度约为 `O(n * (E log V))`，即 `O(n * 2000 * log 26)`，在最坏情况下会接近 2·10⁸ 次操作，实际会超时。  
> - **空间**：我们只需要保存图的邻接表，最多存 2000 条边，空间是 `O(E)`，即几千个整数，几乎可以忽略不计。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

def minimumCost(source: str, target: str,
                original: list[str], changed: list[str], cost: list[int]) -> int:
    # 1️⃣ 建图：字母 -> 编号 (0~25)
    def idx(ch: str) -> int:
        return ord(ch) - ord('a')

    graph = defaultdict(list)               # adjacency list
    for o, c, w in zip(original, changed, cost):
        u, v = idx(o), idx(c)
        graph[u].append((v, w))              # 有向边 u -> v，费用 w

    # 2️⃣ 暴力：对每个字符对单独跑 Dijkstra
    INF = 10**18
    total = 0

    for s_ch, t_ch in zip(source, target):
        s, t = idx(s_ch), idx(t_ch)
        if s == t:                # 本来就相同，不需要花费
            continue

        # Dijkstra 从 s 出发，找到到 t 的最短距离
        dist = [INF] * 26
        dist[s] = 0
        heap = [(0, s)]           # (当前费用, 节点)
        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:
                continue
            if u == t:            # 找到目标，提前结束
                break
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))

        if dist[t] == INF:        # 没有路径
            return -1
        total += dist[t]

    return total
```

> **关键行中文注释**  
> - `graph[u].append((v, w))`：把“一次可以把字符 u 换成字符 v，花费 w”记进邻接表。  
> - `heapq.heappush(heap, (nd, v))`：把新的候选路径放进小根堆，堆顶永远是当前已知最小费用的节点。  
> - `if u == t: break`：一旦到达目标字符，就可以提前结束搜索，省点时间。

#### 复杂度

- **时间复杂度**：`O(n * (E log V))` ≈ `O(n * 2000 * log 26)`。  
  大白话：如果字符串有 10 万个字符，每个字符都要在 2000 条可能的转换中“找最短路”，算起来会非常慢，类似“一百个人排队买票，每个人都要排 2000 次”。  
- **空间复杂度**：`O(E + V)` ≈ `O(2000 + 26)`，只用来存图和 Dijkstra 的临时数组，几乎可以忽略。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都重新跑最短路**。其实字母的种类只有 26 种，所有可能的 **字符对**（最多 26×26 = 676 种）都可以提前算好，后面只需要 **查表**，时间就降到 `O(n)`。

**步骤**：

1. **建图**：同上，把每条合法转换记成有向边。若同一对字符出现多次，只保留费用最小的那条边（因为我们总想花最少的钱）。
2. **全源最短路**：在只有 26 个节点的图上跑 **Floyd‑Warshall**（三层循环），一次性算出任意 `a → b` 的最小费用 `dist[a][b]`。  
   - Floyd‑Warshall 的核心思想：先假设只能经过前 `k` 个字母作为中转点，然后逐步放宽 `k`，最终得到全部最短路。可以把它想成“先只允许走 1、2、3 号站的公交，再允许 4 号站……”的过程。
3. **求答案**：遍历字符串每个位置 `i`，直接取 `dist[source[i]][target[i]]` 并累加；若某对字符的距离是无穷大（不可达），直接返回 `-1`。

**为什么快**：Floyd‑Warshall 只跟字母种类有关，固定为 `26³ ≈ 17576` 次基本操作，和字符串长度无关。随后对每个字符位置只做一次 **O(1)** 的查表，整体是 `O(n + 26³)`，对 `n=10⁵` 完全没压力。

#### 代码（Python）

```python
def minimumCost(source: str, target: str,
                original: list[str], changed: list[str], cost: list[int]) -> int:
    INF = 10**18
    V = 26                                 # 小写字母个数

    # 0️⃣ 初始化距离矩阵，dist[i][j] 表示 i->j 的最小费用
    dist = [[INF] * V for _ in range(V)]
    for i in range(V):
        dist[i][i] = 0                     # 同字母不需要花费

    # 1️⃣ 建图：保留每对字符的最小直接费用
    def idx(ch: str) -> int:
        return ord(ch) - ord('a')

    for o, c, w in zip(original, changed, cost):
        u, v = idx(o), idx(c)
        if w < dist[u][v]:                 # 只保留最小的那条边
            dist[u][v] = w

    # 2️⃣ Floyd‑Warshall：枚举所有可能的中转字母 k
    for k in range(V):
        for i in range(V):
            if dist[i][k] == INF:          # i->k 不可达，直接跳过
                continue
            for j in range(V):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd

    # 3️⃣ 统计答案
    total = 0
    for s_ch, t_ch in zip(source, target):
        s, t = idx(s_ch), idx(t_ch)
        if dist[s][t] == INF:               # 无法转换
            return -1
        total += dist[s][t]

    return total
```

> **关键行中文注释**  
> - `dist[i][i] = 0`：把同一个字母到自己的距离设为 0，表示不需要任何操作。  
> - `if w < dist[u][v]: dist[u][v] = w`：如果有多条 “a→b” 的边，只保留费用最小的那条。  
> - `if dist[i][k] == INF: continue`：如果 `i` 到 `k` 本来就不可达，就不用再尝试 `i→k→j` 这条路，省时间。  
> - `total += dist[s][t]`：直接把查表得到的最小费用加到答案里。

#### 复杂度

- **时间复杂度**：`O(26³ + n)` ≈ `O(n + 17576)`。  
  大白话：先花几千次“小算术”把所有字母之间的最短费用算好，然后只需要把每个字符对应的费用 “读一遍表” 加起来，整个过程和字符串有多长几乎没有关系。  
- **空间复杂度**：`O(26²)` ≈ `O(676)`，仅存 26×26 的距离矩阵，几百个整数，几乎不占内存。

---

## 心得

- **核心技巧**：把字符转换问题抽象成 **带权有向图**，利用 **Floyd‑Warshall** 预计算所有最短路径。  
- **适用场景**：  
  1. 字符或状态种类固定且不多（如 26 个字母、10 个颜色、5 种状态）时，需要多次查询任意两点的最小代价。  
  2. 费用转换可以组合（多步转换），且每一步都有明确费用。  
  3. 典型题目还有 “Minimum Cost to Convert String II”、 “Find the Minimum Cost to Make Two Strings Equal”等。  
- **一句话总结**：**把所有字符之间的最小转换费用一次算好，后面只需要 O(1) 查表即可**。

---

## 反思

- **第一反应**：看到“把字符换成字符，费用给出”，立刻想到把字符当成图的节点，用最短路求最小费用。  
- **最容易踩的坑**：  
  - 忽略 **多条相同方向的边**，导致使用了不是最小的费用。  
  - 没有把 **同字符不需要操作** 的情况设为 0，导致错误的额外费用。  
  - 在暴力实现中忘记 **提前退出**（当目标已达时），会大幅增加不必要的计算。  
- **下次第一步**：先检查字符种类是否有限且足够小，若是则立即考虑 **全源最短路（Floyd‑Warshall）** 或 **多源 BFS** 预处理，避免对每次查询都重复跑最短路。