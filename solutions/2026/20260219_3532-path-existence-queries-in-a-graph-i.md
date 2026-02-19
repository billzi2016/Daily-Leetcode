# #3532. 图中路径存在性查询 I / Path Existence Queries in a Graph I

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/path-existence-queries-in-a-graph-i/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the number of nodes in a graph, labeled from 0 to n - 1.
You are also given an integer array nums of length n sorted in non-decreasing order, and an integer maxDiff.
An undirected edge exists between nodes i and j if the absolute difference between nums[i] and nums[j] is at most maxDiff (i.e., |nums[i] - nums[j]| <= maxDiff).
You are also given a 2D integer array queries. For each queries[i] = [ui, vi], determine whether there exists a path between nodes ui and vi.
Return a boolean array answer, where answer[i] is true if there exists a path between ui and vi in the ith query and false otherwise.

**Examples**

**Example 1:**

```
Input: n = 2, nums = [1,3], maxDiff = 1, queries = [[0,0],[0,1]]
Output: [true,false]
Explanation:
```

**Example 2:**

```
Input: n = 4, nums = [2,5,6,8], maxDiff = 2, queries = [[0,1],[0,2],[1,3],[2,3]]
Output: [false,false,true,true]
Explanation:
The resulting graph is:
```

**Constraints**

- 1 <= n == nums.length <= 105
- 0 <= nums[i] <= 105
- nums is sorted in non-decreasing order.
- 0 <= maxDiff <= 105
- 1 <= queries.length <= 105
- queries[i] == [ui, vi]
- 0 <= ui, vi < n

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n` 表示图中的节点数，节点编号为 `0` 到 `n - 1`。  
再给定一个长度为 `n` 的整数数组 `nums`（已按非递减顺序排序）以及一个整数 `maxDiff`。  

若两个节点 `i` 与 `j` 的数值差的绝对值不超过 `maxDiff`（即 `|nums[i] - nums[j]| <= maxDiff`），则在它们之间存在一条无向边（undirected edge）。  

此外，还给定一个二维整数数组 `queries`。对于每个 `queries[i] = [ui, vi]`，判断节点 `ui` 与节点 `vi` 之间是否存在一条路径（path）。  

返回一个布尔数组 `answer`，其中 `answer[i]` 为 `true` 表示第 `i` 条查询中 `ui` 与 `vi` 之间存在路径，为 `false` 则表示不存在。

---

### 示例

#### 示例 1
```
Input: n = 2, nums = [1,3], maxDiff = 1, queries = [[0,0],[0,1]]
Output: [true,false]
```
**解释**：  
- 查询 `[0,0]` 的节点是同一个节点，显然存在路径，返回 `true`。  
- 查询 `[0,1]` 的两个节点数值差为 `|1 - 3| = 2 > maxDiff`，没有直接的边也无法通过其他节点连通，返回 `false`。

#### 示例 2
```
Input: n = 4, nums = [2,5,6,8], maxDiff = 2, queries = [[0,1],[0,2],[1,3],[2,3]]
Output: [false,false,true,true]
```
**解释**：  
构造出的图如下所示（仅示意）：

- 节点 `0`（值 `2`）与节点 `1`（值 `5`）的差为 `3 > maxDiff`，不存在边。  
- 节点 `1`（值 `5`）与节点 `2`（值 `6`）的差为 `1 ≤ maxDiff`，存在边。  
- 节点 `2`（值 `6`）与节点 `3`（值 `8`）的差为 `2 ≤ maxDiff`，存在边。  

因此：
- 查询 `[0,1]` 与 `[0,2]` 无法连通，返回 `false`。  
- 查询 `[1,3]` 与 `[2,3]` 可以通过已有的边连通，返回 `true`。

---

### 约束条件
- `1 <= n == nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`
- `nums` 已按非递减顺序排序
- `0 <= maxDiff <= 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i] == [ui, vi]`
- `0 <= ui, vi < n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每个查询 `[u, v]`，在图中从 `u` 开始做一次深度优先搜索（DFS）或广度优先搜索（BFS），看能否走到 `v`**。  

- **图的表示**：  
  - 这里没有显式的边列表，而是“两个节点 `i、j` 之间有边当且仅当 `|nums[i] - nums[j]| ≤ maxDiff`”。  
  - 为了遍历，我们可以在搜索时**遍历所有节点**，把满足条件的节点当成邻居。  
  - 想象一下，`nums` 就像一本有序的字典，**“相差不超过 `maxDiff`”**的两个词条就可以互相“握手”。  

- **为什么这个方法一定能得到正确答案**：  
  - DFS/BFS 会把所有能够通过合法边到达的节点全部遍历完，只要 `v` 被遍历到了，就说明 `u` 与 `v` 在同一个连通块，答案为 `True`。  

- **时间/空间复杂度的大白话解释**：  
  - 对每个查询我们都要检查 **所有** 可能的邻居（最多 `n` 个），所以一次搜索是 `O(n)`。  
  - 有 `q = len(queries)` 条查询，整体时间是 `O(n·q)`，这在 `n、q` 都可能达到 `10⁵` 时会非常慢（相当于 10⁹ 次操作）。  
  - 我们只需要存放 `nums`、访问标记等，空间是 `O(n)`，这部分还算好。  

#### 代码（Python）  

```python
from collections import deque
from typing import List

def brute_force(n: int, nums: List[int], maxDiff: int,
                queries: List[List[int]]) -> List[bool]:
    ans = []

    # 辅助函数：判断两点是否有直接边
    def can_connect(i: int, j: int) -> bool:
        return abs(nums[i] - nums[j]) <= maxDiff

    for u, v in queries:
        if u == v:                     # 同一个点显然连通
            ans.append(True)
            continue

        visited = [False] * n          # 记录哪些点已经遍历过
        q = deque([u])
        visited[u] = True
        found = False

        while q:
            cur = q.popleft()
            # 逐个检查所有节点，看是否可以直接相连
            for nxt in range(n):
                if not visited[nxt] and can_connect(cur, nxt):
                    if nxt == v:       # 找到目标点
                        found = True
                        break
                    visited[nxt] = True
                    q.append(nxt)
            if found:
                break

        ans.append(found)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n · q)`  
  - “每条查询都要遍历 `n` 个节点”。如果把 `n` 想象成 10 万，`q` 也是 10 万，那么这就像让 10 万个人各自跑完 10 万 米——显然太慢了。  
- **空间复杂度**：`O(n)`  
  - 只用了一个 `visited` 数组和队列，和节点数量成正比。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈在于每次都要遍历全部节点去找邻居**。其实，这个图的结构很特殊：

1. **`nums` 已经排好序**。  
2. 两个节点只有在它们对应的数值差 ≤ `maxDiff` 时才相连。  
3. 因此如果我们把相邻的、满足 `nums[i+1] - nums[i] ≤ maxDiff` 的节点全部连在一起，**整个连通块一定是一个连续的区间**（没有跳跃）。  

换句话说，**连通块就是把数组划分成若干段**，每段内部的相邻差都 ≤ `maxDiff`，段与段之间的差 > `maxDiff`，不可能跨段相连。  

于是我们只需要一次线性扫描，把这些段标记出来（每个节点记上所属段的编号），**之后每个查询只要比较两个节点的段编号是否相同**，即可在 `O(1)` 时间得到答案。

实现方式有两种：

- **并查集（Union‑Find）**：遍历相邻的 `(i, i+1)`，如果差 ≤ `maxDiff` 就把它们合并到同一个集合。  
- **直接扫描 + 记录段编号**：用一个数组 `comp[i]`，如果 `nums[i] - nums[i-1] ≤ maxDiff` 则 `comp[i] = comp[i-1]`，否则 `comp[i] = comp[i-1] + 1`。

这里用并查集来演示，因为它是图论中“找连通块”的标准工具，且可以帮助读者熟悉 **路径压缩** 与 **按秩合并**（两大优化手段）。

**并查集的类比**：把每个节点想象成一本书的章节，`parent[x]` 就是 “这本章节所在的卷号”。`find(x)` 相当于“追溯到最外层的卷号”，`union(a,b)` 就是把两本卷号相同的书合并成一本大卷。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集：支持快速合并和查询所在集合编号"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 初始每个节点自成一族
        self.rank = [0] * n            # 按秩合并时用的“高度”

    def find(self, x: int) -> int:
        """找根节点，并顺路压缩路径（把沿途的节点直接挂到根上）"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压缩
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """把 x、y 所在的集合合并"""
        xr, yr = self.find(x), self.find(y)
        if xr == yr:          # 已经在同一个集合，无需再合并
            return
        # 按秩合并：把秩低的挂到秩高的下面，保持树尽量扁平
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1      # 秩相同的合并后高度加 1

def path_existence_queries(n: int, nums: List[int], maxDiff: int,
                           queries: List[List[int]]) -> List[bool]:
    """
    预处理连通块 → O(1) 判定每个查询
    """
    uf = UnionFind(n)

    # 只需要检查相邻的两个节点，因为数组有序，跨越更远的节点必定经过相邻节点
    for i in range(1, n):
        if nums[i] - nums[i - 1] <= maxDiff:   # 两者可以直接连边
            uf.union(i, i - 1)                # 把它们放进同一个集合

    # 处理查询：只要根节点相同，即在同一连通块
    ans = []
    for u, v in queries:
        ans.append(uf.find(u) == uf.find(v))
    return ans
```

> **关键点注释**  
> - 第 10‑14 行：`parent[x]` 就像 “这本书的目录指向哪本卷”。路径压缩让以后查找更快。  
> - 第 19‑32 行：`union` 时把“小树”挂到“大树”下面，保持整体结构扁平，查找接近 `O(1)`。  
> - 第 38‑41 行：只检查相邻的 `i-1` 与 `i`，因为若 `i` 与 `j`（`j>i+1`）满足差 ≤ `maxDiff`，那么中间的每一对相邻也必满足，连通性已经在前面的合并中传递了。  

#### 复杂度  

- **时间复杂度**：`O(n + q·α(n))`，其中 `α` 是阿克曼函数的反函数，几乎可以看作常数。  
  - **解释**：一次线性扫描 `O(n)` 把相邻节点合并；每条查询只做两次 `find`，`find` 的均摊时间是极小的常数。相比暴力的 `O(n·q)`，这相当于把 **“每个人都跑 10 万 米”** 变成 **“只跑一次，之后每次只看一下编号”**，快得多。  
- **空间复杂度**：`O(n)`  
  - 需要存 `parent`、`rank` 两个长度为 `n` 的数组，以及答案数组 `O(q)`（输出本身不可避免）。  

---

## 心得  

- **核心技巧**：**利用数组的有序性把连通块转化为连续区间**，随后用并查集（或线性标号）一次预处理，查询时只比较所属组件编号。  
- **适用的题型**  
  1. **“相邻差值限制”**的连通性问题（如 “Maximum Number of Groups With Limited Difference”）。  
  2. **区间合并**类题目（如 “Number of Connected Components in an Undirected Graph” 中的特殊结构）。  
  3. **离线查询**场景：先把所有“加入边”的操作预处理，再统一回答查询（如 “Queries on Number of Islands”）。  
- **一句话总结解题钥匙**：  
  > **“有序 + 局部相连 ⇒ 整体连通块必是连续段，只要把段编号好，查询就是 O(1) 的等号比较”。**  

---

## 反思  

- **拿到题目第一反应**：直接想到 BFS/DFS，逐条检查能否到达——这是一种很自然的“先把图走通再回答”的思路。  
- **最容易踩的坑**  
  - **忽略有序性**：如果不利用 `nums` 已排好序的事实，就会误以为需要检查所有 `O(n²)` 条边。  
  - **跨越非相邻节点的错误合并**：直接把满足 `|nums[i]-nums[j]| ≤ maxDiff` 的任意 `(i, j)` 合并会导致 `O(n²)` 的遍历。正确做法是只看相邻 `(i-1,i)`。  
  - **边界条件**：`maxDiff = 0` 时只有数值相同的相邻节点会连边，注意不要因为 “相等” 而漏掉 `≤` 的情况。  
- **下次遇到同类题的第一步**：  
  > **先问自己：‘如果把数据排个序，连通块会是怎样的形状？’**  
  若答案是“连续区间”，就立刻考虑一次线性预处理（并查集/标号），把查询转化为 “同段吗？” 的判断。