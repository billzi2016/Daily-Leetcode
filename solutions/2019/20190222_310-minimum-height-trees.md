# #310. 最小高度树 / Minimum Height Trees

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/minimum-height-trees/)

---

## 题目（英文原版）

**Description**

A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.
Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [ai, bi] indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you select a node x as the root, the result tree has height h. Among all possible rooted trees, those with minimum height (i.e. min(h))  are called minimum height trees (MHTs).
Return a list of all MHTs' root labels. You can return the answer in any order.
The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[1,0],[1,2],[1,3]]
Output: [1]
Explanation: As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.
```

**Example 2:**

```
Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
Output: [3,4]
```

**Constraints**

- 1 <= n <= 2 * 104
- edges.length == n - 1
- 0 <= ai, bi < n
- ai != bi
- All the pairs (ai, bi) are distinct.
- The given input is guaranteed to be a tree and there will be no repeated edges.

---

## 题目（中文翻译）

**描述**  
树是一种无向图，其中任意两个顶点之间恰好有一条路径。换句话说，任何没有简单环（simple cycles）的连通图都是树。  
给定一棵包含 `n` 个节点、标号为 `0` 到 `n - 1` 的树，以及一个长度为 `n - 1` 的边数组 `edges`，其中 `edges[i] = [ai, bi]` 表示节点 `ai` 与节点 `bi` 之间存在一条无向边。你可以任选树中的任意节点作为根。当选择节点 `x` 作为根时，得到的**有根树**（rooted tree）的高度为 `h`。在所有可能的有根树中，拥有最小高度（即 `min(h)`）的那些树称为**最小高度树**（Minimum Height Trees，MHT）。  
返回所有 MHT 的根节点标号列表，答案可以以任意顺序返回。  
有根树的高度定义为根节点到叶子节点之间最长向下路径上的边数。

**示例 1**  
输入: `n = 4, edges = [[1,0],[1,2],[1,3]]`  
输出: `[1]`  
**解释**: 如图所示，当根节点选为标号为 `1` 的节点时，树的高度为 `1`，此时得到唯一的 MHT。

**示例 2**  
输入: `n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`  
输出: `[3,4]`  

**约束条件**  
- `1 <= n <= 2 * 10^4`  
- `edges.length == n - 1`  
- `0 <= ai, bi < n`  
- `ai != bi`  
- 所有 `(ai, bi)` 对均唯一。  
- 给定的输入一定构成一棵树，且不存在重复边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个节点都当作根**，算出它作为根时整棵树的高度，最后把高度最小的节点挑出来。  
实现思路如下：

1. **构建邻接表**（相当于“谁和谁是好朋友”），用 `dict[int, List[int]]` 保存每个节点的相邻节点。  
2. 对于每个节点 `i`（`0 … n-1`）  
   * 以 `i` 为起点，做一次 **广度优先搜索（BFS）**，层层向外遍历，记录遍历到的层数 `level`。  
   * BFS 结束时，`level` 就是以 `i` 为根的树的高度（因为 BFS 按层展开，最后一层的层数恰好是最长路径的边数）。  
3. 把所有节点的高度放进列表，找到最小的那个值 `min_h`，把对应的节点编号全部返回。

> **类比**：把邻接表想成一本“社交名录”，键是人的编号，值是他认识的朋友列表。BFS 就像从某个人开始，先找他的直接朋友（第 1 层），再找朋友的朋友（第 2 层），依此类推，直到把所有人都找完。层数越多，树就“越高”。

**为什么正确**：  
树的定义保证了从根到任意叶子只有唯一一条路径。BFS 按层遍历正好能够得到从根到最远叶子的层数，即树的高度。遍历所有可能的根，取最小高度，自然得到所有 **最小高度树（MHT）** 的根。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def find_min_height_trees_bruteforce(n: int, edges: List[List[int]]) -> List[int]:
    # 1️⃣ 建图：邻接表
    graph = defaultdict(list)          # dict[int, List[int]]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def bfs_height(root: int) -> int:
        """返回以 root 为根的树的高度"""
        visited = [False] * n
        q = deque([root])
        visited[root] = True
        height = -1                     # height = 层数-1，最后返回边数
        while q:
            for _ in range(len(q)):     # 同层节点一起弹出
                node = q.popleft()
                for nb in graph[node]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)
            height += 1                 # 完成一层，height 加 1
        return height

    # 2️⃣ 试每个节点，记录高度
    heights = []
    for i in range(n):
        heights.append(bfs_height(i))

    # 3️⃣ 取最小高度对应的根
    min_h = min(heights)
    return [i for i, h in enumerate(heights) if h == min_h]
```

#### 复杂度

- **时间复杂度**：`O(n * (n + m))`，这里 `m = n-1`（树的边数），相当于 `O(n²)`。  
  *解释*：对每个根都要跑一次 BFS，BFS 本身遍历所有节点和边一次是 `O(n+m)`，根有 `n` 个，所以乘起来是 `n·O(n)`。  
- **空间复杂度**：`O(n + m)` 用于存邻接表和 BFS 队列，约 `O(n)`。  
  *解释*：邻接表保存每条边两次，最多 `2·(n-1)`，再加上 visited 数组、队列等，都是线性空间。

> 暴力解在 `n ≤ 10⁴` 时会超时，因为 `n²` 级别的计算量太大。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于对每个节点都要完整遍历一次整棵树。我们需要 **只遍历一次**，就能得到所有 MHT 的根。  
观察树的结构会发现：

* 树的 **直径**（最长路径）两端的节点一定不是最小高度根。  
* 把树的 **叶子**（度为 1 的节点）不断“剪掉”，剩下的核心会逐渐收缩。  
* 当剩下的节点数不超过 2 时，这些节点就是 **所有可能的根**（即 MHT 的根）。

这就是 **“层层剥洋葱”**（Topological Sort / BFS 剪叶子）的思路：

1. **统计每个节点的度**（有多少条边相连），度为 1 的节点就是叶子。  
2. 把所有叶子放进队列 `leaves`。  
3. **循环**：  
   * 记录本轮叶子数 `size`，如果去掉这些叶子后 **剩余节点 ≤ 2**，说明已经到了中心，直接返回这些剩余节点。  
   * 否则，逐个弹出叶子 `leaf`，把它和唯一的相邻节点 `neighbor` 的连边删掉（即把 `neighbor` 的度减 1）。  
   * 如果 `neighbor` 的度此时变成 1，说明它在下一轮会成为叶子，加入 `new_leaves`。  
4. 用 `new_leaves` 替换 `leaves`，继续下一轮。  
5. 最终剩下的 1 或 2 个节点就是答案。

> **类比**：把树想成一棵真正的树，最外层的枝叶是叶子。我们把最外层的叶子一次一次剪掉，树会越来越“小”。当只剩下树干（最多两根）时，这些树干的根就是最“平衡”的位置，树的高度最小。

**核心概念**  
- **度（Degree）**：一个节点有几条边相连，度为 1 就是叶子。  
- **拓扑排序（Topological Sort）**：这里的“层层剪叶子”其实是一种特殊的拓扑排序，把所有入度为 0（这里是度为 1）的节点一次次弹出。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def find_min_height_trees(n: int, edges: List[List[int]]) -> List[int]:
    if n <= 2:                     # 特殊情况：0、1、2 个节点本身就是答案
        return [i for i in range(n)]

    # 1️⃣ 建图 + 统计度
    graph = defaultdict(set)       # 用 set 方便后续删除
    degree = [0] * n
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
        degree[u] += 1
        degree[v] += 1

    # 2️⃣ 初始叶子（度为 1 的节点）
    leaves = deque([i for i in range(n) if degree[i] == 1])

    remaining_nodes = n
    # 3️⃣ 循环剪叶子
    while remaining_nodes > 2:
        leaves_count = len(leaves)        # 本轮要剪掉的叶子数量
        remaining_nodes -= leaves_count   # 剪掉后剩余节点数
        new_leaves = deque()

        for _ in range(leaves_count):
            leaf = leaves.popleft()
            # leaf 只有一个邻居
            neighbor = graph[leaf].pop()
            graph[neighbor].remove(leaf)   # 删除 leaf 与 neighbor 的连边
            degree[neighbor] -= 1
            if degree[neighbor] == 1:      # 成为新叶子
                new_leaves.append(neighbor)

        leaves = new_leaves                # 准备进入下一轮

    # 4️⃣ 剩下的 1~2 个节点就是所有 MHT 的根
    return list(leaves)
```

#### 复杂度

- **时间复杂度**：`O(n)`。  
  *解释*：每条边只会被访问两次（一次在建图，另一次在剪叶子时删除），所以总操作数与节点数线性相关。  
- **空间复杂度**：`O(n)` 用于存邻接表、度数组和队列。  
  *解释*：邻接表保存每条边两次，度数组和队列都是线性大小。

> 与暴力解相比，时间从 `O(n²)` 降到 `O(n)`，在 `n = 2·10⁴` 时也能轻松跑完。

---

## 心得

- **核心技巧**：**层层剥叶子（BFS 拓扑剪枝）**，把树的直径压缩到中心，找到最多两个根。  
- **适用题型**  
  1. “寻找树的中心” 类题目，如 **寻找图的中心节点**。  
  2. “最小高度树” 之外的 **树的最长路径（直径）** 相关问题。  
  3. **拓扑排序** 中需要逐层删除入度为 0 的节点的场景（如课程表）。  
- **一句话总结解题钥匙**：**把所有叶子一次次“拔掉”，剩下的核心（≤2个）就是最小高度树的根**。

---

## 反思

- **第一反应**：直接枚举每个节点、BFS 计算高度——想到最直观的暴力实现。  
- **最容易踩的坑**  
  * 边界情况：`n <= 2` 时直接返回所有节点，否则会在循环里把所有节点都删光。  
  * 删除边时要同步更新邻接表和度，否则会出现 “度为负” 或 “找不到邻居” 的错误。  
  * 使用 `set` 存邻接表可以 O(1) 删除，若用 `list` 删除会导致额外的 `O(k)` 开销。  
- **下次遇到同类题**：第一步先思考 **“有没有办法一次遍历得到答案？”**，如果是树结构，考虑 **“从外向内逐层收缩”**（叶子剪枝）或 **“双指针从两端收敛”** 的思路。这样往往能把指数级或平方级的暴力转化为线性级的高效解。