# #3493. 属性图 / Properties Graph

> 难度：中等 · 标签：Array、Hash Table、Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/properties-graph/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array properties having dimensions n x m and an integer k.
Define a function intersect(a, b) that returns the number of distinct integers common to both arrays a and b.
Construct an undirected graph where each index i corresponds to properties[i]. There is an edge between node i and node j if and only if intersect(properties[i], properties[j]) >= k, where i and j are in the range [0, n - 1] and i != j.
Return the number of connected components in the resulting graph.

**Examples**

**Example 1:**

```
Input: properties = [[1,2],[1,1],[3,4],[4,5],[5,6],[7,7]], k = 1
Output: 3
Explanation:
The graph formed has 3 connected components:
```

**Example 2:**

```
Input: properties = [[1,2,3],[2,3,4],[4,3,5]], k = 2
Output: 1
Explanation:
The graph formed has 1 connected component:
```

**Example 3:**

```
Input: properties = [[1,1],[1,1]], k = 2
Output: 2
Explanation:
intersect(properties[0], properties[1]) = 1 , which is less than k . This means there is no edge between properties[0] and properties[1] in the graph.
```

**Constraints**

- 1 <= n == properties.length <= 100
- 1 <= m == properties[i].length <= 100
- 1 <= properties[i][j] <= 100
- 1 <= k <= m

---

## 题目（中文翻译）

**描述**  
给定一个二维整数数组 `properties`，其维度为 `n × m`，以及一个整数 `k`。  
定义函数 `intersect(a, b)`，返回数组 `a` 与数组 `b` 中 **不同整数**（distinct integers）的公共个数。  
构造一个无向图，使得每个下标 `i` 对应节点 `properties[i]`。若且仅当 `intersect(properties[i], properties[j]) ≥ k` 时，在节点 `i` 与节点 `j` 之间连一条边，其中 `i`、`j` 的取值范围为 `[0, n - 1]` 且 `i ≠ j`。  
返回构造得到的图中的 **连通分量**（connected components）数量。

**示例 1**  
```text
Input: properties = [[1,2],[1,1],[3,4],[4,5],[5,6],[7,7]], k = 1
Output: 3
Explanation:
形成的图有 3 个连通分量：
```

**示例 2**  
```text
Input: properties = [[1,2,3],[2,3,4],[4,3,5]], k = 2
Output: 1
Explanation:
形成的图只有 1 个连通分量：
```

**示例 3**  
```text
Input: properties = [[1,1],[1,1]], k = 2
Output: 2
Explanation:
intersect(properties[0], properties[1]) = 1， 小于 k。因此在图中不存在 `properties[0]` 与 `properties[1]` 之间的边。
```

**约束条件**  
- `1 ≤ n == properties.length ≤ 100`  
- `1 ≤ m == properties[i].length ≤ 100`  
- `1 ≤ properties[i][j] ≤ 100`  
- `1 ≤ k ≤ m`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **两两比较**：把每一行 `properties[i]` 当成图中的一个点。遍历所有 `i < j`，检查这两个数组的交集大小是否 `≥ k`。如果是，就在 `i` 与 `j` 之间连一条无向边。  
2. **统计连通块**：得到完整的邻接表（或邻接矩阵）后，用 **DFS / BFS** 从未访问的节点出发，沿着边把能走到的所有节点标记为已访问，这一次遍历结束后计数器 `components += 1`。把所有节点都遍历完，计数器的值就是连通分量的个数。

> **类比**：把每行数组想象成一本书的目录，`intersect(a,b)` 就是两本目录里共同出现的词的数量。如果共同词 ≥ k，就说这两本书“相识”，在社交网络里画一条线。之后我们只要数一数有多少个互相“相识”但不和别的书相连的“朋友圈”。

**为什么正确**  
- 边的定义完全按照题目要求实现：`intersect ≥ k` 才连边。  
- DFS/BFS 能遍历出所有在同一连通块里的节点，因为在无向图里，连通块恰好是“可以互相到达的点的最大集合”。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def intersect(a: List[int], b: List[int]) -> int:
    """返回两个数组的不同整数交集大小"""
    # 把列表转成集合，相当于查字典：key 是元素，value 是是否出现
    return len(set(a) & set(b))

def count_components(properties: List[List[int]], k: int) -> int:
    n = len(properties)                # 点的数量
    # 1️⃣ 建图：邻接表，用 list of list 保存每个点的邻居
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if intersect(properties[i], properties[j]) >= k:
                adj[i].append(j)
                adj[j].append(i)       # 无向图要双向加入

    # 2️⃣ DFS（这里用 BFS）统计连通块
    visited = [False] * n
    components = 0

    for start in range(n):
        if not visited[start]:
            components += 1            # 发现一个新连通块
            q = deque([start])
            visited[start] = True
            while q:
                cur = q.popleft()
                for nb in adj[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)
    return components
```

#### 复杂度

- **时间复杂度**：  
  - 两两比较需要 `n·(n-1)/2 ≈ O(n²)` 次。每次比较要把两行转成集合再求交集，最坏是 `O(m)`（`m` 为每行长度），所以整体是 `O(n²·m)`。  
  - BFS/DFS 只遍历 `n` 条点和 `O(n²)` 条可能的边，和前面的比较同阶。  
  - **大白话**：如果 `n=100, m=100`，最坏会做大约 `10⁶` 次“把数组装进字典、找共同词”的操作，仍在可接受范围。

- **空间复杂度**：  
  - 邻接表最坏存 `O(n²)` 条边（完全图），再加 `O(n)` 的 visited 数组。  
  - **大白话**：最多要记 10,000 条线段的两端是谁。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次比较都要把两行转成集合再求交集，这在 Python 里会产生大量临时对象。  
我们可以利用题目给出的 **小范围数值**（`1 ≤ value ≤ 100`）把每行的“出现的数字集合”压缩成一个 **位掩码**（bitmask）：

- 把 1~100 的每个可能值对应到 0~99 的二进制位。  
- 如果第 `v` 个数出现在该行，就把第 `v-1` 位设为 `1`。  
- 两行的交集大小 = `bit_count(mask_i & mask_j)`，即 **按位与后统计 1 的个数**。Python 3.8+ 提供 `int.bit_count()`，一次运算即可得到交集大小，**不需要集合**。

这样：

1. **预处理**：遍历所有行，把每行转成位掩码，时间 `O(n·m)`，空间 `O(n)`（每个掩码是一个整数）。
2. **两两合并**：仍然要遍历 `i < j`，但现在每次只做一次按位与和一次 `bit_count`，这在 Python 中是 **常数时间**（底层是机器指令），整体时间降为 `O(n²)`。
3. **并查集（Union‑Find）**：在遍历时如果交集 ≥ k，就把这两个节点合并。并查集的 `union` / `find` 近乎 `O(α(n))`（α 为极慢增长的阿克曼函数），可以看作常数。遍历结束后，集合的根节点数量就是连通块数。

> **类比**：把每行的数字想象成 100 把钥匙中的若干把。把钥匙排成一排，用“有没有这把钥匙”对应一位的开关。两行钥匙的共同数量，只需要看哪几位同时是“开”的，直接数一数就行了。

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集（Disjoint Set Union）"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n          # 用于按秩合并，保持树矮一点

    def find(self, x: int) -> int:
        # 路径压缩：递归后把每个访问过的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        # 按秩合并：高度低的挂到高度高的下面
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1

def to_bitmask(arr: List[int]) -> int:
    """把数组转成 100 位的二进制掩码（去重后再置位）"""
    mask = 0
    for v in set(arr):               # 去重，防止同一个数多次置位
        mask |= 1 << (v - 1)          # 第 v 位对应值 v
    return mask

def number_of_components(properties: List[List[int]], k: int) -> int:
    n = len(properties)
    # 1️⃣ 预处理：每行转成位掩码
    masks = [to_bitmask(row) for row in properties]

    dsu = DSU(n)

    # 2️⃣ 两两比较并合并
    for i in range(n):
        for j in range(i + 1, n):
            common = (masks[i] & masks[j]).bit_count()   # 交集大小
            if common >= k:
                dsu.union(i, j)

    # 3️⃣ 统计不同的根节点数量，即连通块数
    roots = {dsu.find(i) for i in range(n)}
    return len(roots)
```

#### 复杂度

- **时间复杂度**：  
  - 预处理 `O(n·m)`（把每行装进位掩码）。  
  - 两两比较 `O(n²)`（每次只做一次按位与和一次 `bit_count`，视作常数）。  
  - 并查集的 `union/find` 近似 `O(1)`，不影响总体复杂度。  
  - **对比**：相比暴力的 `O(n²·m)`，我们把内部的 `m` 乘子消掉了，尤其当 `m` 接近 100 时提升明显。

- **空间复杂度**：  
  - `masks` 保存 `n` 个整数 → `O(n)`。  
  - 并查集的 `parent`、`rank` 也都是 `O(n)`。  
  - **总计** `O(n)`，远小于暴力解的 `O(n²)` 邻接表。

---

## 心得

- **核心技巧**：把值域有限的集合压成位掩码 + 使用并查集快速合并连通块。  
- **适用场景**：  
  1. **集合交并计数**（如 “两个数组有多少相同元素”）且元素取值范围不大。  
  2. **基于相似度建立图**（如 “相同标签 ≥ k 的用户连边”）需要快速判断相似度。  
  3. **任意需要频繁集合交集大小的图论题**（如 “相同兴趣的社交网络”）。  
- **一句话总结解题钥匙**：**用位掩码把集合压缩成整数，按位与+popcount 直接得到交集大小，再用并查集合并即可**。

---

## 反思

- **第一反应**：看到“交集 ≥ k”，立刻想到集合运算；看到“连通组件”，想到 DFS/BFS 或并查集。于是写了最直观的两层循环 + BFS。  
- **最容易踩的坑**：  
  - **去重**：同一行里出现相同数字多次不应计入交集，需要先 `set` 再位掩码。  
  - **位移范围**：题目保证值 ≤ 100，使用 `1 << (v-1)` 才能对应到第 `v` 位，防止越界。  
  - **k 的取值**：`k` 可能等于 `m`，此时只有完全相同的去重集合才会连边，必须保证 `>= k` 而不是 `> k`。  
- **下次类似题的第一步**：先判断“元素取值范围是否小”。如果是，就立刻考虑 **位掩码 + 位运算** 进行集合运算；否则再考虑普通的 `set` 或 `Counter`。随后决定用 **DFS/BFS** 还是 **并查集** 来统计连通块。