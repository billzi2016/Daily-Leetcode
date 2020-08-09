# #952. 按公共因子划分的最大连通分量大小 / Largest Component Size by Common Factor

> 难度：困难 · 标签：Array、Hash Table、Math、Union Find、Number Theory · [LeetCode 链接](https://leetcode.com/problems/largest-component-size-by-common-factor/)

---

## 题目（英文原版）

**Description**

You are given an integer array of unique positive integers nums. Consider the following graph:
Return the size of the largest connected component in the graph.

**Examples**

**Example 1:**

```
Input: nums = [4,6,15,35]
Output: 4
```

**Example 2:**

```
Input: nums = [20,50,9,63]
Output: 2
```

**Example 3:**

```
Input: nums = [2,3,6,7,4,12,21,39]
Output: 8
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 1 <= nums[i] <= 105
- All the values of nums are unique.

---

## 题目（中文翻译）

给定一个由 **唯一** 正整数构成的整数数组 `nums`。构造一张无向图（graph）如下：

- 图中有 `n = nums.length` 个节点，每个节点对应数组中的一个元素。
- 如果两个不同的数字 `a` 和 `b` 之间存在 **大于 1 的公共因子**（common factor），则在对应的两个节点之间连一条无向边（edge）。

返回该图中 **最大连通分量**（largest connected component）的节点数量。

### 示例

#### 示例 1
```
Input: nums = [4,6,15,35]
Output: 4
```
**解释**：  
- 4 与 6 共享因子 2，4 与 15 共享因子 1（不计），4 与 35 共享因子 1（不计）。  
- 6 与 15 共享因子 3，6 与 35 共享因子 1（不计）。  
- 15 与 35 共享因子 5。  

因此，所有四个数字形成一个连通分量，大小为 4。

#### 示例 2
```
Input: nums = [20,50,9,63]
Output: 2
```
**解释**：  
- 20 与 50 共享因子 10，连在同一分量，大小为 2。  
- 9 与 63 共享因子 9，形成另一个大小为 2 的分量。  
- 两个分量大小相同，返回最大值 2。

#### 示例 3
```
Input: nums = [2,3,6,7,4,12,21,39]
Output: 8
```
**解释**：  
所有数字之间通过公共因子相连，形成一个包含 8 个节点的连通分量。

### 约束条件
- `1 <= nums.length <= 2 * 10^4`
- `1 <= nums[i] <= 10^5`
- `nums` 中的所有值均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目把数组 `nums` 看成一个无向图的节点：如果两个数的 **最大公约数 (GCD) 大于 1**，它们之间就有一条边。  
要找最大的连通分量大小，其实就是要在这个图里把「能相互到达」的节点归为一组，找出最大的那组。

最直接的做法就是：

1. 对数组里任意两两组合 `(i, j)`（`i < j`），计算它们的 GCD。  
2. 如果 GCD > 1，就在图里连一条边。  
3. 用 **DFS / BFS** 从每个未访问的节点出发，遍历它能到达的所有节点，统计这一次遍历得到的节点数，即为一个连通分量的大小。  
4. 把所有分量的大小取最大值即可。

> **生活化类比**  
> 想象每个数字是一个人，两个能够「握手」的条件是他们的最大公约数大于 1（握手的“语言”是共同的因子）。暴力解法就是把所有人两两配对，看看谁能握手，再把能通过握手链条相连的所有人归为一伙。

**为什么正确**  
如果我们检查了所有可能的两两关系，并且用 DFS 完全遍历了每个连通块，那么每个连通块必然被完整地统计到。因为图的连通性完全由「是否有公共因子」决定，遍历过程不遗漏也不多算。

**时间/空间复杂度**  
- 计算所有两两 GCD 需要 `C(n,2) = n·(n‑1)/2` 次，时间复杂度是 **O(n²)**。  
  - 这里的 O(n²) 可以想象成「如果有 1000 个人，两两配对要检查 1000×999/2 ≈ 500,000 次」。
- DFS/BFS 需要额外的访问标记数组，空间是 **O(n)**。

#### 代码（Python）

```python
import math
from collections import defaultdict, deque

def largestComponentSize(nums):
    n = len(nums)
    # 记录每个节点的邻居列表（无向图的邻接表）
    graph = defaultdict(list)

    # 暴力枚举所有两两组合，建立边
    for i in range(n):
        for j in range(i + 1, n):
            if math.gcd(nums[i], nums[j]) > 1:      # 如果最大公约数大于 1，就连边
                graph[i].append(j)
                graph[j].append(i)

    visited = [False] * n          # 访问标记
    max_size = 0

    # BFS 遍历每个连通块
    for i in range(n):
        if not visited[i]:
            q = deque([i])
            visited[i] = True
            cur_size = 0
            while q:
                cur = q.popleft()
                cur_size += 1
                for nb in graph[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)
            max_size = max(max_size, cur_size)

    return max_size
```

#### 复杂度

- **时间复杂度：O(n²)**  
  需要检查每一对数字的最大公约数，`n` 越大，检查次数呈二次增长。比如 `n = 2000` 时，大约要比较 2,000,000 次。

- **空间复杂度：O(n)**  
  只用了邻接表（最坏情况下每个节点最多连 `n‑1` 条边，但我们只存下标），以及 `visited` 数组和 BFS 队列，都是线性大小。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于「两两比较」——当 `n` 达到 2·10⁴ 时，`n²` 已经不可接受。  
我们需要 **跳过无关的比较**，只在「真正可能相连」的数字之间建立联系。

**关键观察**  
两个数如果有公共因子 `p > 1`，那么它们必定都能被 `p` 整除。于是我们可以把「拥有同一个因子」的所有数字看成一组，而不是直接两两比较。

**一步步推导**  

1. **把每个数字分解质因数**（只需要找出所有**不同的**质因数）。  
   - 例如 `12 = 2²·3`，它的质因数集合是 `{2, 3}`。  
2. 对每个出现的质因数 `p`，把所有包含 `p` 的数字放进同一个「集合」里。  
   - 这正好对应「在图里通过因子 p 连通」的意思。  
3. 「把同一集合的数字合并为同一个连通块」的经典工具是 **并查集（Union‑Find）**。  
   - 并查集可以在近乎 O(1) 的时间内完成「合并」和「查询根节点」操作。  
4. 遍历完所有数字后，每个并查集的根节点对应一个连通块。统计每个根节点出现的次数（即该块的大小），取最大值即为答案。

> **生活化类比**  
> 把每个数字想成一位「爱好者」，他们的「爱好」是自己的质因数。只要两个人的爱好里有相同的因子（比如都喜欢「2」），他们就会加入同一个兴趣小组。我们用「并查集」这本「社团登记簿」快速把同一兴趣小组的成员合并在一起，最后看看最大的社团有多少人。

**并查集简介（零基础解释）**  
- **父指针 (parent)**：每个元素指向一个「代表」元素，代表整个集合的根。  
- **合并 (union)**：把两个集合的根指向同一个根，实现「合并」的效果。  
- **查找根 (find)**：沿着父指针一直往上找，直到找到自己是根的元素。  
- **路径压缩**：在查找的过程中把沿途的节点直接挂到根上，后续查找更快。  
- **按秩合并**：把小集合挂到大集合下面，保持树的高度尽可能小。

**如何高效分解质因数**  
- 题目限制 `nums[i] ≤ 10⁵`，我们可以预先用 **埃拉托斯特尼筛法** 生成 **最小质因数 (spf)** 数组。  
- 用 `spf[x]` 能在 O(log x) 时间里拆出 `x` 的所有不同质因数。

**整体时间复杂度**  
- 构造 `spf`：`O(max(nums) log log max(nums))`（筛法的经典复杂度），这里约为 `O(10⁵)`.
- 对每个数字分解因数并进行并查集合并：每个数字最多分解出 `log nums[i]` 个不同因数，总体约 `O(n log max(nums))`。  
- 最后统计根节点出现次数：`O(n)`。

整体上是 **线性或准线性**，能够轻松通过 2·10⁴ 的数据规模。

#### 代码（Python）

```python
import math
from collections import defaultdict

# ---------- 并查集实现 ----------
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))   # 每个节点的父指针，初始指向自己
        self.rank = [0] * size            # 按秩合并用的高度近似

    def find(self, x):
        # 路径压缩：递归找根的同时把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # 合并两个集合
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return                     # 已经在同一个集合，无需再合并
        # 按秩合并：把低秩的根挂到高秩的根下面
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

# ---------- 生成最小质因数数组 ----------
def smallest_prime_factor(limit):
    """返回长度为 limit+1 的数组 spf，spf[x] 为 x 的最小质因数"""
    spf = list(range(limit + 1))
    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:                 # i 是质数
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:         # 只记录第一次（最小）的因数
                    spf[j] = i
    return spf

# ---------- 主函数 ----------
def largestComponentSize(nums):
    n = len(nums)
    max_val = max(nums)
    spf = smallest_prime_factor(max_val)   # 预处理最小质因数

    uf = UnionFind(n)                      # 为每个数字建立一个并查集节点

    # factor_to_index: 记录每个质因数第一次出现的数字下标
    factor_to_index = {}

    for idx, num in enumerate(nums):
        x = num
        # 提取 num 的所有不同质因数
        while x > 1:
            p = spf[x]                      # 当前的最小质因数
            # 去掉所有相同的 p，防止重复处理同一因数
            while x % p == 0:
                x //= p
            # 如果 p 已经出现过，则把当前数字和第一次出现 p 的数字合并
            if p in factor_to_index:
                uf.union(idx, factor_to_index[p])
            else:
                factor_to_index[p] = idx     # 记录 p 的“代表”下标

    # 统计每个根节点出现的次数，即每个连通块的大小
    count = defaultdict(int)
    for i in range(n):
        root = uf.find(i)
        count[root] += 1

    return max(count.values())
```

#### 复杂度

- **时间复杂度：O(n · log M + M log log M)**  
  - `M = max(nums) ≤ 10⁵`。  
  - `M log log M` 来自筛法生成最小质因数数组。  
  - 对每个数字的因数分解和并查集合并大约是 `log M`（因为一个数的不同质因数个数 ≤ log₂M），整体近似线性。  
  - 与暴力解的 `O(n²)` 相比，这个复杂度随 `n` 增长非常慢，能轻松处理 2·10⁴ 的规模。

- **空间复杂度：O(n + M)**  
  - `O(n)` 用于并查集的父指针、秩数组以及计数哈希表。  
  - `O(M)` 用于最小质因数数组 `spf`（长度约 10⁵）。  
  - 这两块空间都是线性可接受的。

---

## 心得

- **核心技巧**：把「拥有公共因子」的关系转化为「共享同一个质因数」的集合，再用 **并查集** 快速合并。  
- **适用的题型**  
  1. “根据某种共同属性（如相同因子、相同字母、相同坐标）把元素分组”，如 **"Friend Circles"**、**"Number of Connected Components in an Undirected Graph"**。  
  2. “需要找出最大连通块” 的图论题目，尤其是 **稀疏图** 场景。  
  3. “数论 + 并查集” 的组合，如 **"Smallest Prime Factor Union"**、**"Connected Components by Common Divisors"**。  
- **一句话总结解题钥匙**：*把「公共因子」抽象成「同一个质因数」的标签，用并查集把拥有相同标签的数字快速合并，即可在近线性时间得到最大连通块大小*。

---

## 反思

- **第一反应**：看到「最大公约数 > 1」就想到两两比较，直接写出暴力的双层循环。  
- **最容易踩的坑**  
  1. **时间超限**：没有意识到 `n²` 在 2·10⁴ 时会爆炸。  
  2. **重复因子**：在分解质因数时，如果不去重（比如 12 会得到 `2,2,3`），会导致同一因子多次 union，增加不必要的操作。  
  3. **边界条件**：`nums` 里可能只有一个元素，或者所有数互质，此时答案应为 `1`，要确保统计过程不会返回 `0`。  
- **下次类似题的第一步**：先思考「是否可以把两两关系映射为共享某个标签」；如果可以，尝试用 **哈希表 + 并查集** 或 **DFS/BFS** 按标签分组，而不是直接枚举所有对。这样往往能把指数/二次级别的暴力降到线性或准线性。