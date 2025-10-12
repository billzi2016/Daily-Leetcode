# #3378. LCM 图中的连通分量计数 / Count Connected Components in LCM Graph

> 难度：困难 · 标签：Array、Hash Table、Math、Union Find、Number Theory · [LeetCode 链接](https://leetcode.com/problems/count-connected-components-in-lcm-graph/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums of size n and a positive integer threshold.
There is a graph consisting of n nodes with the ith node having a value of nums[i]. Two nodes i and j in the graph are connected via an undirected edge if lcm(nums[i], nums[j]) <= threshold.
Return the number of connected components in this graph.
A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.
The term lcm(a, b) denotes the least common multiple of a and b.

**Examples**

**Example 1:**

```
Input: nums = [2,4,8,3,9], threshold = 5
Output: 4
Explanation:


The four connected components are (2, 4) , (3) , (8) , (9) .
```

**Example 2:**

```
Input: nums = [2,4,8,3,9,12], threshold = 10
Output: 2
Explanation:

The two connected components are (2, 3, 4, 8, 9) , and (12) .
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- All elements of nums are unique.
- 1 <= threshold <= 2 * 105

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums` 和一个正整数 `threshold`。  
构造一个包含 `n` 个节点的无向图，其中第 `i` 个节点的取值为 `nums[i]`。若  
`lcm(nums[i], nums[j]) <= threshold`（`lcm(a, b)` 表示 `a` 与 `b` 的最小公倍数（least common multiple）），则节点 `i` 与节点 `j` 之间存在一条无向边。

返回该图中的连通分量（connected component）的数量。  
连通分量是图的一个子图，子图内任意两个顶点之间都有路径相连，并且子图中的顶点与子图外的顶点之间没有边相连。

---

### 示例

#### 示例 1
**输入**  
```text
nums = [2,4,8,3,9], threshold = 5
```
**输出**  
```text
4
```
**解释**  

四个连通分量分别为 `(2, 4)`、`(3)`、`(8)`、`(9)`。

#### 示例 2
**输入**  
```text
nums = [2,4,8,3,9,12], threshold = 10
```
**输出**  
```text
2
```
**解释**  

两个连通分量分别为 `(2, 3, 4, 8, 9)` 和 `(12)`。

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `nums` 中的所有元素互不相同。
- `1 <= threshold <= 2 * 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 把每个数组下标当成图的一个节点。  
2. 对所有 **两两** 组合 `(i, j)`（`i < j`），计算 `lcm(nums[i], nums[j])`。  
3. 如果 `lcm ≤ threshold`，就在图中连一条无向边。  
4. 最后用 **DFS / BFS** 把图遍历一遍，统计连通块的个数。

> **数据结构类比**：  
> - **哈希表**（`dict`）好比一本“电话号码簿”，`key` 是电话号码（这里是数值），`value` 是对应的下标。查找时只要看一眼就能定位。  
> - **并查集（Union‑Find）**可以想象成一堆小组的“部落”。每次发现两个人可以直接通话，就把他们所在的两个部落合并成一个大部落。  

这个方法之所以 **一定正确**，是因为我们把所有满足题目条件的边都完整地建了出来，随后的连通块统计自然就是答案。

#### 代码（Python）

```python
from math import gcd
from collections import defaultdict, deque

def lcm(a: int, b: int) -> int:
    """最小公倍数 = a * b / gcd(a, b)"""
    return a // gcd(a, b) * b      # 先除再乘，防止中间溢出

def count_components_bruteforce(nums, threshold):
    n = len(nums)
    # 1️⃣ 建图：邻接表
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if lcm(nums[i], nums[j]) <= threshold:
                graph[i].append(j)
                graph[j].append(i)

    # 2️⃣ BFS/DFS 统计连通块
    visited = [False] * n
    components = 0

    for i in range(n):
        if not visited[i]:
            components += 1
            # 用队列做 BFS
            q = deque([i])
            visited[i] = True
            while q:
                cur = q.popleft()
                for nb in graph[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)
    return components
```

> **关键行中文注释**  
> - `lcm` 函数先除后乘，避免 `a*b` 直接超出 Python 整数范围（虽然 Python 整数是大数，但这么写更安全）。  
> - 双层 `for` 循环遍历所有 `i < j`，这就是 **O(n²)** 的核心。  
> - `graph[i].append(j)` 把满足条件的边加入邻接表。  
> - BFS 通过队列 `deque` 把同一个连通块的所有节点一次性遍历完。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “平方” 的意思是：如果有 10,000 个数，算法要检查约 `10,000 × 9,999 / 2 ≈ 5·10⁷` 对组合，数量级会非常大，计算机会明显卡顿。  
- **空间复杂度**：`O(n + m)`，其中 `m` 为满足条件的边数。最坏情况下 `m ≈ n²`，所以空间也可能达到 `O(n²)`。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在 **“遍历所有两两组合”**。我们需要 **跳过不可能相连的配对**，只对 **可能相连的节点** 进行合并。  
关键观察如下：

1. **如果一个数 `a` 大于 `threshold`，它不可能和任何其他数相连**。  
   - 因为 `lcm(a, x) ≥ a > threshold`，条件永远不满足。  
   - 这类节点直接算作独立的连通块。

2. **若 `a` 与 `b` 的最小公倍数 ≤ threshold，则它们一定共享一个公共因子 `d`（`d = gcd(a, b)`），且 `d ≤ threshold`。**  
   - 设 `a = d·a'`、`b = d·b'`（`gcd(a', b') = 1`），  
   - `lcm(a, b) = d·a'·b' ≤ threshold` → `d ≤ threshold`。  
   - 换句话说，只要两个数有 **任意一个 ≤ threshold 的公共因子**，它们就一定会在同一个连通块里（即使它们本身不直接相连，仍能通过该因子对应的“虚拟节点”桥接）。

3. **利用“公共因子”来合并**  
   - 对每个可能的因子 `d = 1 … threshold`，找出 **所有是 `d` 的倍数且出现在 `nums` 中的数**。  
   - 把这些数全部合并到同一个集合（使用并查集 DSU）。  
   - 这样，**所有共享同一个因子 `d` 的数都会被连到一起**，而不必检查每一对。

4. **实现细节**  
   - 使用哈希表 `pos = {value: index}` 把数组值映射到它们在 DSU 中的下标，查询是否出现只需 **O(1)**。  
   - 对每个 `d`，遍历 `d, 2d, 3d, … ≤ threshold`（相当于遍历 `threshold/d` 次），把在 `pos` 中出现的下标收集起来并进行合并。  
   - 由于 `threshold ≤ 2·10⁵`，`∑_{d=1}^{threshold} threshold/d = threshold·H_threshold ≈ threshold·log(threshold)`，约为 `2·10⁵·12 ≈ 2.4·10⁶` 次循环，完全可接受。

> **类比**：  
> 想象每个数都是一块拼图，**因子 `d`** 是一根细绳。所有带有相同绳子标记的拼图块会被绑在一起。只要两块拼图之间有同一根绳子，它们就能“间接”相连，形成一个大块拼图——这正是连通块的意义。

#### 代码（Python）

```python
from math import gcd
from typing import List

class DSU:
    """并查集（Disjoint Set Union）"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size   = [1] * n          # 用于按大小合并

    def find(self, x: int) -> int:
        # 路径压缩：递归寻找根节点，同时把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按大小合并，保证树的深度尽量小
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def countComponents(nums: List[int], threshold: int) -> int:
    n = len(nums)

    # 1️⃣ 把数组值映射到下标，方便 O(1) 判断某个数是否在 nums 中
    pos = {v: i for i, v in enumerate(nums)}

    dsu = DSU(n)

    # 2️⃣ 只遍历 ≤ threshold 的因子
    for d in range(1, threshold + 1):
        first_idx = -1               # 记录第一个出现的下标，后面的都和它合并
        # 遍历 d 的所有倍数 m = d, 2d, 3d, ...
        for m in range(d, threshold + 1, d):
            if m in pos:             # 只有 nums 中出现的才参与合并
                idx = pos[m]
                if first_idx == -1:  # 第一个出现的数，暂存
                    first_idx = idx
                else:
                    dsu.union(first_idx, idx)

    # 3️⃣ 统计连通块个数（包括阈值以上的独立节点）
    roots = set()
    for i in range(n):
        roots.add(dsu.find(i))
    return len(roots)
```

> **关键行中文注释**  
> - `pos = {v: i for i, v in enumerate(nums)}`：把数值快速映射到它在 DSU 中的编号。  
> - `for d in range(1, threshold + 1):`：枚举所有可能的公共因子。  
> - `for m in range(d, threshold + 1, d):`：遍历因子 `d` 的所有倍数，步长为 `d`。  
> - `if m in pos:`：只对实际出现在 `nums` 中的倍数做合并，避免无意义的遍历。  
> - `dsu.union(first_idx, idx)`：把同一个因子 `d` 的所有数合并到同一个集合。  

#### 复杂度  

- **时间复杂度**：`O(threshold · log(threshold) + n·α(n))`  
  - `threshold·log(threshold)` 来自 “遍历所有因子及其倍数”。  
  - `α(n)` 是 **Ackermann 函数的逆**，在实际中几乎可以看作常数（≈4），所以并查集的合并/查找几乎是 O(1)。  
  - 与暴力的 `O(n²)` 相比，**大幅下降**：即使 `n = 10⁵`，`threshold = 2·10⁵`，运行时间也在毫秒级。

- **空间复杂度**：`O(n)`  
  - 只存储 DSU 的 `parent`、`size` 两个数组（各 `n` 长），以及哈希表 `pos`。  
  - 与暴力解可能出现的 `O(n²)` 边表不同，空间使用非常友好。

---

## 心得  

- **核心技巧**：**利用公共因子（≤ threshold）把同一因子下的所有数合并**，这是一种“**从属性到集合**”的思路。  
- **适用题型**（类似思路）  
  1. *Count Connected Components in GCD Graph*（根据 `gcd ≤ threshold` 合并）  
  2. *Number of Connected Components in an Undirected Graph where edges exist if `a % b == 0`*（使用因子合并）  
  3. *Largest Component Size by Common Factor*（LeetCode 952）  

- **一句话总结解题钥匙**：  
  > “只要两个数共享一个 ≤ threshold 的因子，它们必然在同一连通块里——把‘因子’当作桥梁，用并查集合并即可。”

---

## 反思  

- **第一反应**：直接枚举所有数对，计算 `lcm`，觉得实现最直观。  
- **最容易踩的坑**  
  1. **阈值以上的数**：忘记它们永远孤立，导致多余的合并操作或错误计数。  
  2. **遍历因子时的重复检查**：若每次都遍历全部 `nums`，时间会退化到 `O(n·threshold)`，不够快。使用哈希表把检查压到 `O(1)`。  
  3. **整数溢出**：直接 `a*b` 可能超过 64 位，使用 `a // gcd(a, b) * b` 或 Python 大整数防止错误。  

- **下次遇到同类题**，第一步应该思考 **“哪些属性可以把节点快速归类”**（如公共因子、倍数关系、相同余数等），再把这些属性当作“桥梁”，用 **并查集** 或 **BFS/DFS** 把同属性的节点合并。这样即可从 **O(n²)** 降到 **接近线性** 的复杂度。