# #2709. 最大公约数遍历 / Greatest Common Divisor Traversal

> 难度：困难 · 标签：Array、Math、Union Find、Number Theory · [LeetCode 链接](https://leetcode.com/problems/greatest-common-divisor-traversal/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums, and you are allowed to traverse between its indices. You can traverse between index i and index j, i != j, if and only if gcd(nums[i], nums[j]) > 1, where gcd is the greatest common divisor.
Your task is to determine if for every pair of indices i and j in nums, where i < j, there exists a sequence of traversals that can take us from i to j.
Return true if it is possible to traverse between all such pairs of indices, or false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [2,3,6]
Output: true
Explanation: In this example, there are 3 possible pairs of indices: (0, 1), (0, 2), and (1, 2).
To go from index 0 to index 1, we can use the sequence of traversals 0 -> 2 -> 1, where we move from index 0 to index 2 because gcd(nums[0], nums[2]) = gcd(2, 6) = 2 > 1, and then move from index 2 to index 1 because gcd(nums[2], nums[1]) = gcd(6, 3) = 3 > 1.
To go from index 0 to index 2, we can just go directly because gcd(nums[0], nums[2]) = gcd(2, 6) = 2 > 1. Likewise, to go from index 1 to index 2, we can just go directly because gcd(nums[1], nums[2]) = gcd(3, 6) = 3 > 1.
```

**Example 2:**

```
Input: nums = [3,9,5]
Output: false
Explanation: No sequence of traversals can take us from index 0 to index 2 in this example. So, we return false.
```

**Example 3:**

```
Input: nums = [4,3,12,8]
Output: true
Explanation: There are 6 possible pairs of indices to traverse between: (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), and (2, 3). A valid sequence of traversals exists for each pair, so we return true.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

你被给定一个 **0 索引** 的整数数组 `nums`，并且可以在其下标之间进行遍历。只有当 **最大公约数（gcd）** `gcd(nums[i], nums[j]) > 1` 时，才可以在下标 `i` 与下标 `j`（`i != j`）之间进行遍历，其中 `gcd` 表示最大公约数。

你的任务是判断，对于数组中任意下标对 `i` 和 `j`（`i < j`），是否存在一系列遍历，使得我们可以从 `i` 到达 `j`。如果能够在所有满足 `i < j` 的下标对之间都实现遍历，则返回 `true`；否则返回 `false`。

### 示例

**示例 1**  
Input: `nums = [2,3,6]`  
Output: `true`  
Explanation: 在此示例中，共有 3 对下标可以考虑：(0, 1)、(0, 2) 和 (1, 2)。要从下标 0 到下标 1，可以走 `0 -> 2 -> 1` 的遍历路径。因为 `gcd(nums[0], nums[2]) = gcd(2, 6) = 2 > 1`，能够从 0 到 2；随后 `gcd(nums[2], nums[1]) = gcd(6, 3) = 3 > 1`，能够从 2 到 1。

**示例 2**  
Input: `nums = [3,9,5]`  
Output: `false`  
Explanation: 在此示例中，不存在任何遍历路径可以从下标 0 到达下标 2，所以返回 `false`。

**示例 3**  
Input: `nums = [4,3,12,8]`  
Output: `true`  
Explanation: 共有 6 对下标需要遍历：(0, 1)、(0, 2)、(0, 3)、(1, 2)、(1, 3) 和 (2, 3)。每一对下标都存在合法的遍历序列，因此返回 `true`。

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组 `nums` 看成 **图的节点**，如果两个下标 `i`、`j` 满足 `gcd(nums[i], nums[j]) > 1`，就把它们之间连一条 **无向边**。  
这样，题目就等价于：判断这张图是否 **连通**（所有节点是否在同一个连通分量），因为连通分量里任意两点都可以通过若干条边走到一起。

> **类比**：把每个下标想象成城市，`gcd > 1` 的两座城市之间有直达的高速公路。我们要问的是，这些城市能否通过高速公路形成一张“全连通”的地图。

实现步骤：

1. 对每一对不同的下标 `(i, j)` 计算 `gcd(nums[i], nums[j])`。  
2. 若 `gcd > 1`，就在邻接表/邻接矩阵里记录这条边。  
3. 完成所有边的构建后，从任意一个节点（比如 `0`）做 **DFS/BFS**，遍历能到达的所有节点。  
4. 如果遍历后访问的节点数等于数组长度 `n`，说明图连通，返回 `True`；否则返回 `False`。

> **正确性**：只要两点之间的 `gcd` 大于 `1`，题目允许直接跳转；若需要多步跳转，DFS/BFS 正好会把所有可能的跳转路径串起来。只要遍历能覆盖所有节点，说明任意两点都有路径。

#### 代码（Python）

```python
import math
from collections import deque

def can_traverse_bruteforce(nums):
    n = len(nums)
    # 1. 建立邻接表
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            # 计算两数的最大公约数
            if math.gcd(nums[i], nums[j]) > 1:
                graph[i].append(j)   # i 与 j 相连
                graph[j].append(i)   # j 与 i 相连（无向图）

    # 2. BFS 从节点 0 开始遍历
    visited = [False] * n
    q = deque([0])
    visited[0] = True
    while q:
        cur = q.popleft()
        for nb in graph[cur]:
            if not visited[nb]:
                visited[nb] = True
                q.append(nb)

    # 3. 判断是否所有节点都被访问过
    return all(visited)
```

#### 复杂度

- **时间复杂度**：`O(n² * log C)`  
  - `n²` 来自两层循环遍历所有下标对。  
  - `log C`（`C ≤ 10⁵`）是求一次 `gcd` 的复杂度（欧几里得算法的近似），可以把它视作常数。  
  - 用大白话说，就是当数组有 10⁵ 个元素时，这种双重遍历会产生约 10¹⁰ 次比较，根本跑不完。

- **空间复杂度**：`O(n²)`（最坏情况的邻接表）  
  - 每一对满足 `gcd>1` 的下标都会存一条边，最坏情况下（所有数都相同且 >1）会有 `n·(n-1)/2` 条边。  
  - 对于 10⁵ 的数据，这相当于几百 GB 的内存，显然不可行。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“枚举所有下标对”**。我们需要一种方式，**不必两两比较**，而是利用数的 **质因数** 来快速判断哪些下标可以相连。

关键观察：

1. 两个数的 `gcd > 1`，当且仅当它们 **至少共享一个相同的质因数**。  
   - 例如 `6 = 2·3`、`15 = 3·5`，它们都含有质因数 `3`，所以 `gcd(6,15)=3>1`。  
2. 如果我们把 **每个质因数** 看成 “中转站”，所有含有该质因数的下标都可以通过这个中转站相互到达。  
   - 换句话说，**所有拥有相同质因数的节点本质上已经在同一个连通分量**。

于是我们可以把问题转化为 **“把拥有相同质因数的下标合并到同一个集合”**，这正是 **并查集（Union‑Find）** 的擅长场景。

实现步骤：

1. **预处理**：用 **埃拉托斯特尼筛法** 生成 `1 … 10⁵` 的最小质因数（`spf`），这样可以在 `O(log num)` 时间内快速分解任意数的质因数。  
2. 初始化并查集，`parent[i] = i`（每个下标自成一个集合）。  
3. 遍历数组 `nums`，对每个元素 `num = nums[i]`  
   - 用 `spf` 把 `num` 分解出所有 **唯一的质因数**（去重）。  
   - 对于每个质因数 `p`，我们维护一个字典 `prime_to_index`，记录 **第一次出现该质因数的下标**。  
   - 如果 `p` 之前已经出现过下标 `j`，就把 `i` 与 `j` **合并**（`union(i, j)`）。  
   - 否则把 `i` 记为该质因数的代表（`prime_to_index[p] = i`）。  
4. 完成所有合并后，检查所有下标的根是否相同：如果所有 `find(i)` 都等于 `find(0)`，说明整张图连通，返回 `True`；否则返回 `False`。

> **类比**：把每个下标想成城市，把每个质因数想成公交线路。只要两座城市乘坐同一条公交（共享质因数），它们就可以在同一站点换乘，最终形成同一张“交通网络”。并查集负责记录哪些城市已经在同一网络里。

#### 代码（Python）

```python
from math import sqrt
from collections import defaultdict

# ---------- 并查集 ----------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n           # 用于按秩合并，提升效率

    def find(self, x):
        # 路径压缩：递归查根的同时把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:          # 已经在同一集合
            return
        # 按秩合并：把高度小的树挂到高度大的树下
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

# ---------- 生成最小质因数表 ----------
def smallest_prime_factors(limit: int):
    """返回长度为 limit+1 的数组 spf，其中 spf[x] 为 x 的最小质因数"""
    spf = list(range(limit + 1))
    for i in range(2, int(sqrt(limit)) + 1):
        if spf[i] == i:                     # i 是质数
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:             # 只记录第一次（最小）的质因数
                    spf[j] = i
    return spf

# ---------- 主函数 ----------
def can_traverse(nums):
    n = len(nums)
    max_val = max(nums)
    spf = smallest_prime_factors(max_val)   # 预处理质因数表

    uf = UnionFind(n)
    prime_to_index = {}                      # 质因数 -> 第一次出现的下标

    for idx, num in enumerate(nums):
        x = num
        seen_primes = set()                  # 去重，同一个数可能有重复质因数
        while x > 1:
            p = spf[x]                       # 当前最小质因数
            seen_primes.add(p)
            while x % p == 0:                # 去掉所有 p 的幂次
                x //= p

        # 把拥有相同质因数的下标合并
        for p in seen_primes:
            if p in prime_to_index:
                uf.union(idx, prime_to_index[p])
            else:
                prime_to_index[p] = idx

    # 检查所有节点是否同根
    root = uf.find(0)
    return all(uf.find(i) == root for i in range(1, n))
```

#### 复杂度

- **时间复杂度**：`O(n * log A)`（`A = max(nums)`）  
  - 预处理最小质因数表：`O(A log log A)`，对 `A ≤ 10⁵` 来说非常快。  
  - 对每个数分解质因数的复杂度约为 `O(log num)`（因为每除一次最小质因数，数值就会显著变小），整体是 `O(n log A)`。  
  - 并查集的 `find/union` 近乎 `O(1)`（α(n)），几乎不影响总体复杂度。  
  - 与暴力 `O(n²)` 相比，`n` 最高到 `10⁵` 时，这种做法在毫秒级即可完成。

- **空间复杂度**：`O(n + A)`  
  - `O(n)` 用于并查集的 `parent`、`rank`。  
  - `O(A)` 用于最小质因数表（`A ≤ 10⁵`，只占几百 KB）。  
  - 额外的 `prime_to_index` 最多存 `A` 个不同质因数的映射，仍然在同一个量级。

---

## 心得

- **核心技巧**：把 “两个数的 `gcd>1`” 转化为 “它们共享至少一个质因数”，并利用 **并查集** 按质因数把下标合并成连通分量。  
- **适用的题型**  
  1. “数组中是否所有数都能通过 `gcd>1` 互相连通” （本题）。  
  2. “判断图中是否所有节点都在同一连通分量，且边的生成规则基于公共因子” （如 LeetCode 1657. 确定连通性）。  
  3. “基于共享属性（如相同素数、相同字符等）合并集合的题目” （例如 “相同字母的字符串是否能相互转换”）。  
- **一句话总结解题钥匙**：**“共享质因数 ⇒ 同一连通分量，使用并查集快速合并”**。

---

## 反思

- **第一反应**：直接把每对下标的 `gcd` 算一遍，然后做图的遍历。  
- **最容易踩的坑**  
  1. **时间超限**：`n` 达到 `10⁵` 时，两两比较根本跑不完。  
  2. **重复质因数**：在分解质因数时，需要去重，否则同一个数的同一质因数会导致多余的 `union` 操作。  
  3. **特殊数值**：`1` 没有质因数，单独出现时会导致该下标永远孤立，需要在代码里自然处理（`while x>1` 循环本身会跳过 `1`）。  
- **下次遇到同类题**：第一步先思考 “**两个元素何时可以直接连通**”，如果可以抽象为 “共享某类属性”，就立刻考虑 **把属性映射为中转节点 + 并查集**，从而避免枚举所有元素对。