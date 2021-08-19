# #1443. 收集树中所有苹果的最少时间 / Minimum Time to Collect All Apples in a Tree

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/)

---

## 题目（英文原版）

**Description**

Given an undirected tree consisting of n vertices numbered from 0 to n-1, which has some apples in their vertices. You spend 1 second to walk over one edge of the tree. Return the minimum time in seconds you have to spend to collect all apples in the tree, starting at vertex 0 and coming back to this vertex.
The edges of the undirected tree are given in the array edges, where edges[i] = [ai, bi] means that exists an edge connecting the vertices ai and bi. Additionally, there is a boolean array hasApple, where hasApple[i] = true means that vertex i has an apple; otherwise, it does not have any apple.

**Examples**

**Example 1:**

```
Input: n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,true,false,true,true,false]
Output: 8 
Explanation: The figure above represents the given tree where red vertices have an apple. One optimal path to collect all apples is shown by the green arrows.
```

**Example 2:**

```
Input: n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,true,false,false,true,false]
Output: 6
Explanation: The figure above represents the given tree where red vertices have an apple. One optimal path to collect all apples is shown by the green arrows.
```

**Example 3:**

```
Input: n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,false,false,false,false,false]
Output: 0
```

**Constraints**

- 1 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai < bi <= n - 1
- hasApple.length == n

---

## 题目（中文翻译）

给定一棵无向树（undirected tree），包含 n 个顶点，编号从 0 到 n‑1，部分顶点上放有苹果。走过树的一条边（edge）需要 1 秒。请返回从顶点 0 出发、收集树中所有苹果并最终回到顶点 0 所需的最少时间（秒）。

无向树的边通过数组 `edges` 给出，其中 `edges[i] = [a_i, b_i]` 表示存在一条连接顶点 `a_i` 和 `b_i` 的边。此外，还有一个布尔数组 `hasApple`，其中 `hasApple[i] = true` 表示顶点 `i` 上有苹果；否则该顶点没有苹果。

**示例 1**  
**输入**: `n = 7`, `edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]]`, `hasApple = [false,false,true,false,true,true,false]`  
**输出**: `8`  
**解释**: 上图展示了给定的树，红色顶点表示有苹果的节点。一条收集所有苹果的最优路径如绿色箭头所示。

**示例 2**  
**输入**: `n = 7`, `edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]]`, `hasApple = [false,false,true,false,false,true,false]`  
**输出**: `6`  
**解释**: 上图展示了给定的树，红色顶点表示有苹果的节点。一条收集所有苹果的最优路径如绿色箭头所示。

**示例 3**  
**输入**: `n = 7`, `edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]]`, `hasApple = [false,false,false,false,false,false,false]`  
**输出**: `0`  

**约束条件**  
- `1 <= n <= 10^5`  
- `edges.length == n - 1`  
- `edges[i].length == 2`  
- `0 <= a_i < b_i <= n - 1`  
- `hasApple.length == n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：把每一个有苹果的节点当成 **一次独立的旅行**。  
从根节点 `0` 出发，走到该节点，再原路返回根节点，所走的每条边都算 **2 秒**（去一次 + 回来一次）。  
把所有有苹果的节点的这种“往返路程”相加，就是答案。

> **类比**：想象你住在城市的中心（根节点），每次去郊区的一个小镇（有苹果的节点）买东西后都要把车开回中心。每条道路你都得走两遍。  

**为什么这个方法能得到一个可行的答案**  
- 每次我们都保证回到根节点，所以所有苹果最终都会被收集完。  
- 只要把所有往返路程累加，肯定能覆盖每个苹果所在的路径。

**为什么它不是最优**  
- 多个苹果可能在同一条道路的同一侧。比如两个苹果分别在 `0-1-2` 和 `0-1-3`，我们会把 `0-1` 这条边算了 **四次**（两次往返），其实只需要走两次（去一次，回来一次）就能把两个苹果一起收集。  
- 也就是说，这种方法会 **重复计数** 共用的边，导致时间被高估。

**时间/空间复杂度**  
- **时间复杂度**：我们需要遍历所有节点一次来判断它是否有苹果，然后对每个有苹果的节点计算从根到它的距离（可以用 BFS/DFS 预处理得到）。最坏情况下每个节点都有苹果，距离的求和相当于遍历 `n` 条边 `n` 次 → **O(n²)**。  
  - “O(n²)” 可以想象成 **“把 n 条路每条都走 n 次”**，当 n 很大时会非常慢。  
- **空间复杂度**：需要保存树的邻接表和一些辅助数组，都是 `O(n)` 的规模。  

#### 代码（Python）  

```python
from collections import deque, defaultdict

def minTime_bruteforce(n: int, edges, hasApple) -> int:
    # 建立邻接表（每个节点都记录它的相邻节点）
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 预处理：用 BFS 求出根节点到每个节点的距离（层数）
    dist = [-1] * n               # dist[i] = 从根 0 到 i 的最短边数
    q = deque([0])
    dist[0] = 0
    while q:
        cur = q.popleft()
        for nxt in graph[cur]:
            if dist[nxt] == -1:   # 只访问一次，防止回到父节点
                dist[nxt] = dist[cur] + 1
                q.append(nxt)

    # 对每个有苹果的节点，累加往返路程 2 * distance
    total = 0
    for i in range(n):
        if hasApple[i]:
            total += 2 * dist[i]   # 去一次 + 回来一次
    return total
```

> 代码里每一行都有中文注释，帮助你快速定位每一步的作用。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：最坏情况下每个节点都有苹果，需要把根到每个节点的距离相加，而每次求距离都要遍历整棵树（这里用了预处理把距离一次性算完，实际复杂度是 `O(n)`，但如果不做预处理、每次都 BFS，则会是 `O(n²)`，这里用来说明暴力思路的“慢”。）  
- **空间复杂度**：`O(n)`  
  - 解释：邻接表、距离数组、队列等都随节点数线性增长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复走同一条边是主要的时间浪费**。  
如果我们能判断某条边 **是否真的需要走**（即这条边的子树里至少有一个苹果），就可以只走必要的边，且每条必要的边只走 **两次**（去一次、回来一次）。  

**关键观察**  
- 对于一条连接父节点 `p` 与子节点 `c` 的边，如果子树 `c`（包括 `c` 本身）里没有苹果，那么这条边 **永远不需要走**。  
- 如果子树里有苹果，则无论有多少个，都只需要 **一次往返**（2 秒），因为我们可以一次性把子树里的所有苹果收集完再回到父节点。

**如何判断子树是否包含苹果**  
- 采用 **深度优先搜索（DFS）** 从根节点向下遍历。  
- 对每个节点，递归检查它的所有子节点，返回一个布尔值 `has_apple_in_subtree` 表示“这棵子树里是否有苹果”。  
- 当子节点的返回值为 `True` 时，说明这条边必须走，于是把 **2** 加到答案中。  

**算法步骤**  
1. 把 `edges` 转成邻接表，方便遍历。  
2. 定义递归函数 `dfs(node, parent)`：  
   - 初始化 `total_time = 0`。  
   - 对每个相邻的子节点 `nei`（排除回到 `parent` 的那条边），递归调用 `dfs(nei, node)`。  
   - 如果子树返回 `True`（有苹果），说明 `node ↔ nei` 这条边必须走，两端各一次，`total_time += 2`。  
   - 最后返回 `total_time > 0 or hasApple[node]`，即“本节点或子树里有苹果”。  
3. 主函数调用 `dfs(0, -1)`，得到的累计时间就是答案。  
4. 特殊情况：如果整棵树没有任何苹果，答案应为 **0**（根本不需要移动）。

**类比**：把树想象成一棵 **水果树**，根是树干，枝桠上挂着苹果。我们要从树干出发，采完所有苹果再回到树干。只要某根枝桠上没有苹果，就不必去剪那根枝桠——省下的时间就是我们要的最优解。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

def minTime(n: int, edges: List[List[int]], hasApple: List[bool]) -> int:
    # 1️⃣ 建立邻接表（无向图）
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 2️⃣ 深度优先搜索，返回子树是否包含苹果
    def dfs(node: int, parent: int) -> bool:
        """遍历 node 的所有子节点，累计必要的时间。
        返回值 True 表示该子树（包括 node 本身）里至少有一个苹果。"""
        # 标记当前子树是否需要走的时间
        need = False   # 当前子树是否有苹果
        for nei in graph[node]:
            if nei == parent:          # 防止回到父节点形成死循环
                continue
            child_has = dfs(nei, node) # 递归检查子节点的子树
            if child_has:              # 子树里有苹果，必须走这条边
                nonlocal ans
                ans += 2               # 去一次 + 回来一次
                need = True            # 当前子树肯定有苹果
        # 最终返回：本节点有苹果 或 子树里有苹果
        return need or hasApple[node]

    ans = 0  # 用来累计所有必走的边的时间（每条边计 2 秒）
    dfs(0, -1)   # 从根节点 0 开始，父节点设为 -1（不存在）
    return ans
```

> **关键行解释**  
- `graph[u].append(v)` / `graph[v].append(u)`：把无向边变成邻接表，像 **字典查词**，`u` 是词，`v` 是对应的页面。  
- `if nei == parent: continue`：防止在树里走回头路，像 **不让你走进已经走过的巷子**。  
- `ans += 2`：发现子树有苹果，就必须 **来回走这条边**，每次 2 秒。  
- `return need or hasApple[node]`：只要子树或自己有苹果，就把 “有苹果” 这个信息往上传。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：每个节点和每条边只被访问一次，等价于 **“走遍整棵树一次”**，所以即使 `n=10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(n)`  
  - 解释：邻接表占 `O(n)`，递归栈最深也可能是 `n`（链状树），因此总空间随节点数线性增长。  

---

## 心得  

- **核心技巧**：**后序 DFS 判断子树是否含苹果**，只保留必须走的边。  
- **适用的题型**  
  1. “收集树上资源” 类问题（例如 LeetCode 1245 `Tree Diameter` 的变体）。  
  2. “最小代价遍历所有需要访问的节点”——如 “最小时间访问所有有需求的城市”。  
  3. “剪枝树的无用分支”——例如 “删除无用子树” 类题目。  
- **一句话总结解题钥匙**：**“只走必经的枝桠，子树里有需求才保留这条边”。**  

---

## 反思  

- **第一反应**：看到“树”“走边”“返回根”，自然会想到“遍历所有有苹果的节点，累加往返距离”。这就是暴力思路。  
- **最容易踩的坑**  
  1. **重复计数**：多颗苹果在同一条路径上时，容易把同一条边算多次。  
  2. **递归结束条件**：忘记排除父节点会导致无限循环或错误的计数。  
  3. **全部没有苹果**：答案应是 `0`，而不是默认返回 `2`（根本不需要出发）。  
- **下次遇到同类题**：第一步先问自己 **“这条边的子树里是否真的需要去？”**，用 DFS 把“需要”信息自底向上汇总，再决定是否走这条边。这样即可直接得到最优解。