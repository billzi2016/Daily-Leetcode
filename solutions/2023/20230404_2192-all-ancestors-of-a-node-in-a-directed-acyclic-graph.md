# #2192. **所有节点的祖先（All Ancestors of a Node in a Directed Acyclic Graph）** / All Ancestors of a Node in a Directed Acyclic Graph

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n representing the number of nodes of a Directed Acyclic Graph (DAG). The nodes are numbered from 0 to n - 1 (inclusive).
You are also given a 2D integer array edges, where edges[i] = [fromi, toi] denotes that there is a unidirectional edge from fromi to toi in the graph.
Return a list answer, where answer[i] is the list of ancestors of the ith node, sorted in ascending order.
A node u is an ancestor of another node v if u can reach v via a set of edges.

**Examples**

**Example 1:**

```
Input: n = 8, edgeList = [[0,3],[0,4],[1,3],[2,4],[2,7],[3,5],[3,6],[3,7],[4,6]]
Output: [[],[],[],[0,1],[0,2],[0,1,3],[0,1,2,3,4],[0,1,2,3]]
Explanation:
The above diagram represents the input graph.
- Nodes 0, 1, and 2 do not have any ancestors.
- Node 3 has two ancestors 0 and 1.
- Node 4 has two ancestors 0 and 2.
- Node 5 has three ancestors 0, 1, and 3.
- Node 6 has five ancestors 0, 1, 2, 3, and 4.
- Node 7 has four ancestors 0, 1, 2, and 3.
```

**Example 2:**

```
Input: n = 5, edgeList = [[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
Output: [[],[0],[0,1],[0,1,2],[0,1,2,3]]
Explanation:
The above diagram represents the input graph.
- Node 0 does not have any ancestor.
- Node 1 has one ancestor 0.
- Node 2 has two ancestors 0 and 1.
- Node 3 has three ancestors 0, 1, and 2.
- Node 4 has four ancestors 0, 1, 2, and 3.
```

**Constraints**

- 1 <= n <= 1000
- 0 <= edges.length <= min(2000, n * (n - 1) / 2)
- edges[i].length == 2
- 0 <= fromi, toi <= n - 1
- fromi != toi
- There are no duplicate edges.
- The graph is directed and acyclic.

---

## 题目（中文翻译）

给定一个正整数 `n`，表示有向无环图（Directed Acyclic Graph，DAG）的节点数量。节点编号为 `0` 到 `n - 1`（含）。
同时给定一个二维整数数组 `edges`，其中 `edges[i] = [from_i, to_i]` 表示图中存在一条从 `from_i` 指向 `to_i` 的单向边。

返回一个列表 `answer`，其中 `answer[i]` 为第 `i` 个节点的所有祖先（ancestors）构成的列表，按升序排序。
如果节点 `u` 能通过若干条边到达节点 `v`，则 `u` 是 `v` 的祖先。

---

### 示例

#### 示例 1
**输入**  
`n = 8, edgeList = [[0,3],[0,4],[1,3],[2,4],[2,7],[3,5],[3,6],[3,7],[4,6]]`

**输出**  
`[[],[],[],[0,1],[0,2],[0,1,3],[0,1,2,3,4],[0,1,2,3]]`

**解释**  
上图表示输入的有向无环图。  
- 节点 `0、1、2` 没有任何祖先。  
- 节点 `3` 的祖先有 `0` 与 `1`。  
- 节点 `4` 的祖先有 `0` 与 `2`。  
- 节点 `5` 的祖先有 `0、1、3`。  
- 节点 `6` 的祖先有 `0、1、2、3、4`。  
- 节点 `7` 的祖先有 `0、1、2、3`。  

（示例已截断）

#### 示例 2
**输入**  
`n = 5, edgeList = [[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`

**输出**  
`[[],[0],[0,1],[0,1,2],[0,1,2,3]]`

**解释**  
上图表示输入的有向无环图。  
- 节点 `0` 没有任何祖先。  
- 节点 `1` 的唯一祖先是 `0`。  
- 节点 `2` 的祖先是 `0、1`。  
- 节点 `3` 的祖先是 `0、1、2`。  
- 节点 `4` 的祖先是 `0、1、2、3`。  

---

### 约束条件
- `1 <= n <= 1000`
- `0 <= edges.length <= min(2000, n * (n - 1) / 2)`
- `edges[i].length == 2`
- `0 <= from_i, to_i <= n - 1`
- `from_i != to_i`
- 不存在重复的边。
- 图是有向且无环的。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「对每个节点，都把它的所有祖先找出来」——这正像我们要为每个人查询「谁能把信递到我这里」。  
实现思路：

1. **把图反向**：原来的边 `u → v` 表示 `u` 能到 `v`，反向后得到 `v → u`，这条反向边恰好表示「从 `v` 可以直接走到它的一个祖先 `u`」。  
2. **对每个节点做一次遍历**（DFS 或 BFS）：从该节点出发，沿着反向边走，所有能走到的节点就是它的祖先。  
3. 把遍历得到的祖先集合排序后放进答案数组。

> **类比**：把「查字典」想成「把所有出现过的单词（祖先）记录下来」。这里的哈希表（`set`）就像字典的「词 → 页码」映射，`set` 里存的都是「能找到的词」。

**为什么正确**  
因为在 DAG 中不存在环路，沿着反向边一直往回走一定能遍历到所有能到达该节点的前驱节点——这正是祖先的定义。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Set

def getAncestors_bruteforce(n: int, edges: List[List[int]]) -> List[List[int]]:
    # 1. 建立反向邻接表：rev_adj[v] = [所有指向 v 的节点]
    rev_adj = defaultdict(list)
    for u, v in edges:
        rev_adj[v].append(u)          # 反向边 v -> u

    answer: List[List[int]] = [[] for _ in range(n)]

    # 2. 对每个节点做 BFS，收集所有能到达它的节点
    for node in range(n):
        visited: Set[int] = set()    # 防止重复访问
        q = deque([node])

        while q:
            cur = q.popleft()
            for pre in rev_adj[cur]: # 只往「祖先」方向走
                if pre not in visited:
                    visited.add(pre)
                    q.append(pre)

        # 3. 把集合转成有序列表
        answer[node] = sorted(visited)

    return answer
```

> **关键行中文注释**  
> - `rev_adj[v].append(u)`：把每条原始边翻转，方便「从子节点往上找祖先」。  
> - `visited`：记录已经找到的祖先，防止在宽度搜索中重复加入。  
> - `sorted(visited)`：题目要求返回的祖先列表必须升序。

#### 复杂度

- **时间复杂度**：`O(n * (n + m))`  
  - 对每个节点都要遍历一次图，最坏情况下（每条边都在反向邻接表里），一次 BFS 需要 `O(n + m)`，再乘以 `n`。  
  - 大白话：如果图有 1000 个节点、2000 条边，最差会进行约 `1000 * (1000 + 2000) ≈ 3·10⁶` 次基本操作，仍在可接受范围，但不是最优。

- **空间复杂度**：`O(n + m)`  
  - 反向邻接表占 `O(n + m)`，每次 BFS 需要的 `visited` 集合最多 `O(n)`。  

---

### 2. 最优解

#### 思路  

暴力解的「慢点」在于**重复遍历**：对每个节点都要从头走一遍图，很多子路径会被重复搜索。我们希望把「一次遍历得到的结果」复用到后面的节点。

**核心思路**：利用 **拓扑排序**（Topological Sort）从「源点」向「终点」逐层处理，同时把已经算好的祖先集合「向下传递」。

步骤如下：

1. **正向邻接表** `adj[u] = [所有 v，使 u → v]`，以及每个节点的入度 `indeg[v]`（有多少条边指向它）。  
2. **拓扑排序**：把入度为 0 的节点放进队列，逐个弹出并「更新」其子节点的入度，形成一个从「没有祖先」到「可能有祖先」的顺序。  
3. **维护祖先集合**：为每个节点准备一个 `set`（或位运算的整数）`anc[u]`，保存已知的祖先。  
   - 当我们从拓扑序弹出节点 `u` 时，`anc[u]` 已经完整（因为所有能到达 `u` 的前驱都已经处理完）。  
   - 对每条 `u → v`，把 `u` 本身以及 `u` 的所有祖先全部加入 `anc[v]`：  
     ```
     anc[v] = anc[v] ∪ {u} ∪ anc[u]
     ```
   - 这一步相当于「把父辈的血统传给子辈」。
4. 拓扑序结束后，`anc[i]` 就是节点 `i` 的全部祖先。把每个集合排序后返回。

> **为什么正确**  
> - 拓扑序保证「所有父节点」一定在「子节点」之前处理完；因此在处理 `u → v` 时，`anc[u]` 已经是完整的祖先集合。  
> - 通过 `anc[v] ∪= anc[u] ∪ {u}`，我们把「父亲」以及「父亲的所有祖先」都加入子节点，递归地把所有可达的前驱都收集进去。  

**实现细节**  
- `n ≤ 1000`，使用 Python 的 `set` 完全够。若想更快，可以用 `int` 的位运算（每个节点对应 1 位），但这里保持可读性，仍用 `set`。  
- 最后排序时直接 `sorted(anc[i])`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Set

def getAncestors_optimal(n: int, edges: List[List[int]]) -> List[List[int]]:
    # 1. 正向邻接表 + 入度统计
    adj = defaultdict(list)          # u -> [v1, v2, ...]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    # 2. 拓扑排序（Kahn 算法）
    q = deque([i for i in range(n) if indeg[i] == 0])  # 入度为 0 的源点
    topo: List[int] = []          # 记录拓扑序

    while q:
        u = q.popleft()
        topo.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # 3. 祖先集合，初始都是空集
    anc: List[Set[int]] = [set() for _ in range(n)]

    # 4. 按拓扑序传播祖先信息
    for u in topo:                # 保证所有前驱已经处理完
        for v in adj[u]:
            # 把 u 本身加入 v 的祖先集合
            anc[v].add(u)
            # 再把 u 的所有祖先也全部加入 v
            anc[v].update(anc[u])

    # 5. 把集合转成升序列表
    answer = [sorted(list(s)) for s in anc]
    return answer
```

> **关键行中文注释**  
> - `indeg[v] += 1`：统计每个节点有多少条「入口」边，用来找「根节点」。  
> - `while q:`：Kahn 拓扑排序的核心循环，保证父节点先被弹出。  
> - `anc[v].add(u)` 与 `anc[v].update(anc[u])`：把父节点和父节点的祖先一起「传递」给子节点。  

#### 复杂度

- **时间复杂度**：`O(n + m + n * avg_ancestors)`，在最坏情况下（完全有向无环图）每条边会把一个集合复制一次，集合大小最多 `O(n)`，整体仍然是 `O(n * m)`，但因为 `m ≤ 2000`、`n ≤ 1000`，实际运行远快于暴力的 `O(n·(n+m))`。  
  - 大白话：我们只遍历一次所有边，且每条边只做一次「集合合并」操作，远比每个节点都重新搜索整张图要高效。

- **空间复杂度**：`O(n + m + n²)`（最坏情况下每个节点的祖先集合可能包含所有前面的节点），但这正是答案本身需要的空间，无法再压缩。  
  - 只要 `n = 1000`，`n² = 10⁶` 个整数的存储在现代机器上完全可以接受。

---

## 心得

- **核心技巧**：利用 **拓扑排序** + **集合传播**（或位运算）一次性求出所有节点的可达前驱。  
- **适用场景**  
  1. **所有前驱/后继集合**（如「找每个节点的所有祖先」或「所有子孙」）。  
  2. **在 DAG 上进行 DP**（最长路径、计数路径数等）。  
  3. **传递闭包**（Transitive Closure）的问题，只要节点数不太大，用集合/位集即可高效实现。  
- **一句话总结解题钥匙**：**「先把图排好序，再沿着顺序把父辈的血统逐层传给子辈」**。

---

## 反思

- **第一反应**：把图反向，然后对每个节点跑一次 BFS/DFS，直接把「能走到」的节点收集起来。  
- **最容易踩的坑**  
  1. **忘记去重**：在暴力 BFS 中如果不使用 `visited`，同一个祖先会被重复加入，导致错误的计数和无限循环。  
  2. **拓扑排序失效**：如果图中出现环（虽然题目保证是 DAG），Kahn 算法会卡住，需要检查入度是否全部归零。  
  3. **集合合并顺序**：必须在父节点的祖先集合已经完整的前提下再合并，否则会遗漏间接祖先。  
- **下次类似题的第一步**：**判断是否可以做拓扑排序**（即图是 DAG），如果可以，就考虑「从源点向下传播」或「从终点向上回收」的 DP/集合方法，而不是对每个节点单独搜索。