# #1627. 阈值图连通性 / Graph Connectivity With Threshold

> 难度：困难 · 标签：Array、Math、Union Find、Number Theory · [LeetCode 链接](https://leetcode.com/problems/graph-connectivity-with-threshold/)

---

## 题目（英文原版）

**Description**

We have n cities labeled from 1 to n. Two different cities with labels x and y are directly connected by a bidirectional road if and only if x and y share a common divisor strictly greater than some threshold. More formally, cities with labels x and y have a road between them if there exists an integer z such that all of the following are true:
Given the two integers, n and threshold, and an array of queries, you must determine for each queries[i] = [ai, bi] if cities ai and bi are connected directly or indirectly. (i.e. there is some path between them).
Return an array answer, where answer.length == queries.length and answer[i] is true if for the ith query, there is a path between ai and bi, or answer[i] is false if there is no path.

**Examples**

**Example 1:**

```
Input: n = 6, threshold = 2, queries = [[1,4],[2,5],[3,6]]
Output: [false,false,true]
Explanation: The divisors for each number:
1:   1
2:   1, 2
3:   1, 3
4:   1, 2, 4
5:   1, 5
6:   1, 2, 3, 6
Using the underlined divisors above the threshold, only cities 3 and 6 share a common divisor, so they are the
only ones directly connected. The result of each query:
[1,4]   1 is not connected to 4
[2,5]   2 is not connected to 5
[3,6]   3 is connected to 6 through path 3--6
```

**Example 2:**

```
Input: n = 6, threshold = 0, queries = [[4,5],[3,4],[3,2],[2,6],[1,3]]
Output: [true,true,true,true,true]
Explanation: The divisors for each number are the same as the previous example. However, since the threshold is 0,
all divisors can be used. Since all numbers share 1 as a divisor, all cities are connected.
```

**Example 3:**

```
Input: n = 5, threshold = 1, queries = [[4,5],[4,5],[3,2],[2,3],[3,4]]
Output: [false,false,false,false,false]
Explanation: Only cities 2 and 4 share a common divisor 2 which is strictly greater than the threshold 1, so they are the only ones directly connected.
Please notice that there can be multiple queries for the same pair of nodes [x, y], and that the query [x, y] is equivalent to the query [y, x].
```

**Constraints**

- 2 <= n <= 104
- 0 <= threshold <= n
- 1 <= queries.length <= 105
- queries[i].length == 2
- 1 <= ai, bi <= cities
- ai != bi

---

## 题目（中文翻译）

我们有 **n** 个城市，编号为 `1` 到 `n`。如果且仅当两个不同城市的编号 `x` 和 `y` 共享一个严格大于给定阈值 `threshold` 的公共约数，则这两个城市之间会有一条双向道路直接相连。更形式化地说，当且仅当存在整数 `z` 满足以下全部条件时，城市 `x` 与城市 `y` 之间存在道路：

- `z` 能整除 `x`（即 `z` 是 `x` 的约数）；
- `z` 能整除 `y`（即 `z` 是 `y` 的约数）；
- `z > threshold`。

给定整数 `n`、`threshold` 与一个查询数组 `queries`，你需要判断每个查询 `queries[i] = [a_i, b_i]` 中的城市 `a_i` 与城市 `b_i` 是否直接或间接相连（即它们之间是否存在一条路径）。返回一个布尔数组 `answer`，其中 `answer.length == queries.length`，且 `answer[i]` 为 `true` 表示第 `i` 个查询的两座城市之间存在路径，为 `false` 表示不存在。

---

### 示例  

**示例 1**  

```
Input: n = 6, threshold = 2, queries = [[1,4],[2,5],[3,6]]
Output: [false,false,true]
Explanation: 每个数字的约数如下：
1:   1
2:   1, 2
3:   1, 3
4:   1, 2, 4
5:   1, 5
6:   1, 2, 3, 6
在阈值 `2` 之上划线标出的约数只有 `3` 与 `6` 共享的约数 `3`，因此只有城市 3 与城市 6 直接相连。各查询结果为：
[1,4] → 1 与 4 不连通  
[2,5] → 2 与 5 不连通  
[3,6] → 3 与 6 连通
```

**示例 2**  

```
Input: n = 6, threshold = 0, queries = [[4,5],[3,4],[3,2],[2,6],[1,3]]
Output: [true,true,true,true,true]
Explanation: 与示例 1 相同的约数表，但阈值为 `0`，因此所有约数（包括 `1`）都可以使用。由于所有数字都至少共享约数 `1`，所以所有城市互相连通。
```

**示例 3**  

```
Input: n = 5, threshold = 1, queries = [[4,5],[4,5],[3,2],[2,3],[3,4]]
Output: [false,false,false,false,false]
Explanation: 唯一满足阈值 `1` 以上的公共约数是 `2`，仅城市 2 与城市 4 共享该约数，因此它们是唯一直接相连的城市。其余任意城市对都不连通。
```

> 请注意，可能会对同一对节点 `[x, y]` 提出多次查询，并且查询 `[x, y]` 与查询 `[y, x]` 等价。

---

### 约束条件  

- `2 <= n <= 10^4`
- `0 <= threshold <= n`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 2`
- `1 <= a_i, b_i <= n`
- `a_i != b_i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有城市当作图的节点**，然后**两两检查**它们是否满足「有一个公共因子 > threshold」的条件，若满足就把这条边加入图中。  
这一步可以这样实现：

1. 对每一对不同的城市 `(x, y)`（`x` 从 `1` 到 `n-1`，`y` 从 `x+1` 到 `n`）  
2. 计算 `x` 和 `y` 的所有因子（可以通过遍历 `1 … sqrt(num)` 来得到）  
3. 看这两个因子集合里是否有交集且交集中的元素大于 `threshold`  
4. 若有，就把 `x`、`y` 用 **并查集（Union‑Find）** 合并，或者直接在邻接表里记一条无向边  

> **哈希表**就像一本“词典”，`key` 是单词（这里可以是城市编号），`value` 是对应的“页码”（这里可以是该城市的因子集合）。我们把每个城市的因子放进哈希表，查找交集时就像在词典里找同一个页码的单词。

**为什么暴力法是正确的？**  
只要我们把**所有**满足条件的边都加进图，图的连通分量自然就是题目要求的“直接或间接可达”。之后对每个查询只要判断两个城市是否在同一个连通分量即可。

**时间/空间复杂度**  
- **遍历所有城市对**：`C(n,2) = n·(n‑1)/2`，大约是 `O(n²)`。  
- **求每个数的因子**：对一个数 `x`，遍历到 `√x`，最坏 `O(√n)`。于是整体是 `O(n²·√n)`，远远超过题目限制（`n ≤ 10⁴`）。  
- **空间**：需要保存每个城市的因子集合，最坏 `O(n·√n)`，以及并查集 `O(n)`。

> **大白话**：`O(n²)` 就相当于“如果你把 10 000 块砖头两两配对检查，需要检查约 5 0000 0000（五十亿）次”，这在电脑里几乎不可能在一秒内跑完。

#### 代码（Python）

```python
import math

def get_factors(x: int) -> set:
    """返回 x 的所有因子（包括 1 和 x 本身）"""
    factors = set()
    i = 1
    while i * i <= x:
        if x % i == 0:
            factors.add(i)
            factors.add(x // i)
        i += 1
    return factors

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))

    def find(self, x):
        # 路径压缩：把查询路径上的所有节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

def brute_force(n, threshold, queries):
    # 1. 预处理每个城市的因子集合
    factors = [set() for _ in range(n + 1)]
    for i in range(1, n + 1):
        factors[i] = get_factors(i)

    uf = UnionFind(n)

    # 2. 两两检查是否有公共因子 > threshold
    for x in range(1, n):
        for y in range(x + 1, n + 1):
            # 只要有一个公共因子大于阈值，就连通
            if any(f > threshold for f in factors[x] & factors[y]):
                uf.union(x, y)

    # 3. 回答查询
    ans = []
    for a, b in queries:
        ans.append(uf.find(a) == uf.find(b))
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²·√n)`（两层城市循环 + 因子求解）。这在最坏情况下会达到上百亿次操作，实际会超时。  
- **空间复杂度**：`O(n·√n)`（存每个城市的因子集合）+ `O(n)`（并查集）。  

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**两两比较**。我们其实不需要逐对检查，而是**利用数的倍数关系**直接把应该连通的城市一次性合并。

**关键观察**  

- 若 `x` 与 `y` 有公共因子 `z > threshold`，那么 `z` 本身必然是一个 **大于阈值的整数**，且 `x`、`y` 都是 `z` 的 **倍数**。  
- 换句话说：**所有大于 `threshold` 的整数 `z`，把它的所有倍数（`z, 2z, 3z, … ≤ n`）看成一组**，这些城市之间一定是连通的（因为它们都共享因子 `z`）。

因此，只要遍历 **所有可能的因子 `z`（即 `threshold+1 … n`）**，把 `z` 的倍数全部用并查集合并，就能一次性完成整个图的构建。

**为什么这样做等价于暴力法？**  
每一条满足条件的边，都必然对应某个公共因子 `z`。我们把所有拥有相同 `z` 的城市合并，等价于把所有这条边「一次性」加进图里。没有遗漏，也没有多余。

**核心数据结构：并查集（Union‑Find）**  
- `find(x)`: 返回 x 所在连通分量的根。  
- `union(a, b)`: 把 a、b 所在的两棵树合并。  
并查集可以在 **近似常数时间**（α(n)，极小的反函数）完成这些操作，特别适合大量“合并-查询”场景。

**实现细节**  

1. 初始化并查集 `parent[1…n]`。  
2. 对每个可能的因子 `z` 从 `threshold+1` 到 `n`：  
   - 计算 `z` 的第一个倍数 `z` 本身。  
   - 依次遍历 `2*z, 3*z, …`，把它们全部 **union** 到 `z`。  
   - 为了减少 `union` 次数，只需要把 **相邻倍数** 合并即可（`z` 与 `2z` 合并，`2z` 与 `3z` 合并，…），因为并查集的传递性会把所有倍数连成一片。  
3. 所有合并完成后，对每个查询 `[a, b]` 检查 `find(a) == find(b)`，即可得到答案。

**类比**：把每个 `z` 想象成“一支队伍”，所有 `z` 的倍数都是这支队伍的成员。我们只要把队伍里的相邻成员拉手（`union`），整支队伍自然就会手拉手形成一个“大团体”。  

#### 代码（Python）

```python
class UnionFind:
    def __init__(self, n):
        # parent[i] 表示 i 的父节点，初始时每个节点自己是根
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)   # 用于按秩合并，保持树矮一点

    def find(self, x):
        # 路径压缩：递归查根的同时把沿途节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按秩合并：把秩小的根挂到秩大的根下
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1


def are_connected(n: int, threshold: int, queries):
    """
    返回一个布尔列表，指示每个查询的两座城市是否连通。
    """
    uf = UnionFind(n)

    # 只遍历大于阈值的因子 z
    for z in range(threshold + 1, n + 1):
        # 第一个倍数是 z 本身，后面的倍数是 2*z, 3*z, ...
        first = z
        # 把所有倍数两两相邻合并
        multiple = 2 * z
        while multiple <= n:
            uf.union(first, multiple)   # 把 z 与它的下一个倍数连起来
            first = multiple
            multiple += z

    # 处理查询
    ans = []
    for a, b in queries:
        ans.append(uf.find(a) == uf.find(b))
    return ans
```

> **代码解释**  
> - `for z in range(threshold + 1, n + 1)`: 从阈值+1 开始遍历可能的公共因子。  
> - `while multiple <= n:`: 只遍历 `z` 的倍数，不会超过 `n`。  
> - `uf.union(first, multiple)`: 把相邻的两个倍数合并，等价于把所有倍数连成一条链。  
> - 查询阶段只用 `find` 判断根是否相同，时间几乎为 **O(1)**。

#### 复杂度

- **时间复杂度**  
  - 合并阶段：对每个 `z`，遍历 `n / z` 个倍数。总次数是  

    \[
    \sum_{z = threshold+1}^{n} \frac{n}{z}
    \le n \cdot \sum_{z=1}^{n} \frac{1}{z}
    = n \cdot H_n
    \]

    其中 `H_n` 是第 `n` 项调和数，约等于 `log n`。所以整体是 **O(n log n)**。  
    对于 `n ≤ 10⁴`，约 `10⁴·log(10⁴) ≈ 1.2×10⁵` 次操作，完全可以接受。  

  - 查询阶段：每个查询只做两次 `find`，几乎是 **O(1)**，共 `O(Q)`（`Q = queries.length ≤ 10⁵`）。  

  - **总时间**：`O(n log n + Q)`。

- **空间复杂度**  
  - 并查集需要 `parent`、`rank` 两个长度为 `n+1` 的数组 → **O(n)**。  
  - 其余只用常数级别的额外空间 → **O(n)** 总空间。  

> 与暴力解相比，**时间从 `O(n²·√n)` 降到了 `O(n log n)`**，空间也大幅降低。

---

## 心得

- **核心技巧**：利用“公共因子 = 大于阈值的整数的倍数”这一数论性质，把图的构建转化为**遍历因子并合并其倍数**，配合并查集快速判连通性。  
- **该技巧适用的题型**  
  1. “给定阈值，两个数若有公共因子 > 阈值则连通”类（本题）。  
  2. “把所有能被同一个数整除的节点合并”——如 LeetCode 1657 *Determine if Two Strings Are Close*（字符出现次数视为因子）。  
  3. “根据质因数或公约数划分连通分量”——如 “Number of Connected Components in an Undirected Graph” 中的数论版。  
- **一句话总结解题钥匙**：**把“共享因子”映射成“同一个因子的所有倍数是一个连通块”，用并查集一次性完成所有合并**。

---

## 反思

- **第一反应**：直接去构造完整的图、两两比较因子——这在思路上是对的，却忽视了规模限制。  
- **最容易踩的坑**  
  - **阈值为 0** 时，所有数都至少共享因子 1，整个图是连通的，记得不要遗漏 `z = 1`（即 `threshold+1 = 1`）。  
  - **倍数遍历的起点**：如果只把 `z` 与 `2z` 合并，而不继续向后合并，仍然能得到同一个连通块，因为并查集会把 `2z`、`3z`…通过链式合并连起来。  
  - **并查集的路径压缩/按秩**：若忘记这两点，`find` 可能退化成线性搜索，导致超时。  
  - **查询顺序**：查询顺序不影响结果，但一定要在所有 `union` 完成后才去 `find`，否则会得到错误的连通信息。  

- **下次遇到同类题**：第一步就问自己——**“有没有一种共同的属性可以把若干节点一次性归类？”**（比如相同的因子、相同的质因数、相同的余数等），然后用 **并查集** 或 **DFS/BFS** 把这些归类一次性完成，避免 O(N²) 的逐对检查。