# #1615. 最大网络秩 / Maximal Network Rank

> 难度：中等 · 标签：Graph · [LeetCode 链接](https://leetcode.com/problems/maximal-network-rank/)

---

## 题目（英文原版）

**Description**

There is an infrastructure of n cities with some number of roads connecting these cities. Each roads[i] = [ai, bi] indicates that there is a bidirectional road between cities ai and bi.
The network rank of two different cities is defined as the total number of directly connected roads to either city. If a road is directly connected to both cities, it is only counted once.
The maximal network rank of the infrastructure is the maximum network rank of all pairs of different cities.
Given the integer n and the array roads, return the maximal network rank of the entire infrastructure.

**Examples**

**Example 1:**

```
Input: n = 4, roads = [[0,1],[0,3],[1,2],[1,3]]
Output: 4
Explanation: The network rank of cities 0 and 1 is 4 as there are 4 roads that are connected to either 0 or 1. The road between 0 and 1 is only counted once.
```

**Example 2:**

```
Input: n = 5, roads = [[0,1],[0,3],[1,2],[1,3],[2,3],[2,4]]
Output: 5
Explanation: There are 5 roads that are connected to cities 1 or 2.
```

**Example 3:**

```
Input: n = 8, roads = [[0,1],[1,2],[2,3],[2,4],[5,6],[5,7]]
Output: 5
Explanation: The network rank of 2 and 5 is 5. Notice that all the cities do not have to be connected.
```

**Constraints**

- 2 <= n <= 100
- 0 <= roads.length <= n * (n - 1) / 2
- roads[i].length == 2
- 0 <= ai, bi <= n-1
- ai != bi
- Each pair of cities has at most one road connecting them.

---

## 题目（中文翻译）

有 **n** 个城市的基础设施，其中一些城市之间有道路相连。`roads[i] = [a_i, b_i]` 表示城市 `a_i` 与城市 `b_i` 之间存在一条双向道路（bidirectional road）。

**网络秩（network rank）** 定义为两座不同城市所直接相连的道路总数。如果同一条道路同时连接这两座城市，则只计入一次。

**最大网络秩（maximal network rank）** 是所有不同城市对的网络秩中的最大值。

给定整数 `n` 和数组 `roads`，返回整个基础设施的最大网络秩。

---

### 示例

**示例 1**  
输入: `n = 4, roads = [[0,1],[0,3],[1,2],[1,3]]`  
输出: `4`  
说明: 城市 0 与城市 1 的网络秩为 4，因为有 4 条道路连接到 0 或 1。道路 `[0,1]` 只计入一次。

**示例 2**  
输入: `n = 5, roads = [[0,1],[0,3],[1,2],[1,3],[2,3],[2,4]]`  
输出: `5`  
说明: 有 5 条道路连接到城市 1 或城市 2。

**示例 3**  
输入: `n = 8, roads = [[0,1],[1,2],[2,3],[2,4],[5,6],[5,7]]`  
输出: `5`  
说明: 城市 2 与城市 5 的网络秩为 5。注意，并非所有城市都必须相互连通。

---

### 约束条件

- `2 <= n <= 100`
- `0 <= roads.length <= n * (n - 1) / 2`
- `roads[i].length == 2`
- `0 <= a_i, b_i <= n - 1`
- `a_i != b_i`
- 任意一对城市之间至多只有一条道路相连。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有城市两两配对，逐个算它们的网络秩**，然后取最大值。  
要算两座城市 `i`、`j` 的网络秩，需要知道：

1. 城市 `i` 有多少条直接相连的道路（即 `i` 的**度**，想象成这座城市的“道路出入口”数量）。  
2. 城市 `j` 的度。  
3. 如果 `i` 与 `j` 之间本身也有一条道路，这条道路在上面两步里被算了两次，需要减掉一次。

所以：

```
rank(i, j) = degree[i] + degree[j] - (i 与 j 之间是否有直接道路 ? 1 : 0)
```

**数据结构**  

- `degree`：长度为 `n` 的整数数组，`degree[x]` 记录城市 `x` 的度。可以把它想成一本**城市字典**，键是城市编号，值是这座城市的道路数量。  
- `connected`：一个 `n × n` 的布尔矩阵（或者 `set`），用来**快速判断两座城市是否直接相连**。这就像查字典一样，`connected[i][j] == True` 表示字典里有词 `i-j`，查找是 O(1)。

**为什么一定正确**  

我们遍历了**所有**不同的城市对 `(i, j)`，对每一对都用公式计算了它们的网络秩，并记录了最大值。由于没有遗漏任何可能的配对，最大值必然是整个基础设施的**最大网络秩**。

**复杂度分析（大白话）**  

- 外层两层循环遍历所有城市对，城市数最多 100，配对数约为 `n*(n-1)/2`，即 **大约 n²/2 次**。  
- 每次计算只做几次加减和一次 O(1) 的查表（判断是否有直接道路），所以 **总时间是 O(n²)**。  
- `degree` 用 `n` 个整数，`connected` 用 `n²` 个布尔值，**空间是 O(n²)**，相当于一张 `n × n` 的“是否相连”表。

> **O(n²) 的含义**：如果城市数量翻倍，计算量会大约增长到原来的四倍（因为是平方关系），但在本题的限制（n ≤ 100）下仍然非常快。

#### 代码（Python）

```python
def maximalNetworkRank(n: int, roads: list[list[int]]) -> int:
    # 1. 统计每个城市的度（道路数量）
    degree = [0] * n                     # degree[i] = i 的度
    # 2. 建立是否直接相连的查询表
    connected = [[False] * n for _ in range(n)]

    for a, b in roads:
        degree[a] += 1
        degree[b] += 1
        connected[a][b] = connected[b][a] = True   # 双向道路

    max_rank = 0

    # 3. 暴力枚举所有不同城市对
    for i in range(n):
        for j in range(i + 1, n):        # 只枚举 i < j，避免重复
            # 计算网络秩：度之和 - 直接相连的重复计数
            cur = degree[i] + degree[j] - (1 if connected[i][j] else 0)
            max_rank = max(max_rank, cur)

    return max_rank
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  *解释*：遍历所有城市对（约 n²/2 次），每次只做常数时间的操作。  
- **空间复杂度**：`O(n²)`  
  *解释*：需要一个 `n × n` 的布尔矩阵来存储是否相连。

---

### 2. 最优解

#### 思路  

在本题的约束下（`n ≤ 100`），**暴力 O(n²) 已经足够快**，没有必要再做更复杂的优化。  
不过，为了帮助大家从“慢哪里”出发思考，我们可以把暴力的 **两个核心点** 再提炼一下：

1. **度的统计** 必不可少，任何优化都离不开每座城市的出入口数。  
2. **快速判断是否相连** 是瓶颈所在。若每次都遍历 `roads` 去找 `(i, j)` 是否相连，时间会退化到 `O(n³)`。  
   - 使用哈希表（`set`）或布尔矩阵把“是否相连”查询降到 **O(1)**，这一步把整体复杂度从 `O(n³)` 降到 `O(n²)`，就是本题的关键优化。

因此，“最优解”实际上就是 **在暴力枚举的框架下，加入 O(1) 的相连查询**。这也是多数图论题目常用的技巧：**预处理 adjacency 信息**。

下面给出使用 `set` 的实现（空间略低于矩阵，但思路相同），并在代码里用中文解释每一步。

#### 代码（Python）

```python
def maximalNetworkRank(n: int, roads: list[list[int]]) -> int:
    # 1️⃣ 统计每座城市的度
    degree = [0] * n
    # 2️⃣ 用集合存所有直接道路，便于 O(1) 判断 (i, j) 是否相连
    #    把每条道路规范成 (min, max) 的形式，防止 (a,b) 与 (b,a) 重复
    road_set = set()
    for a, b in roads:
        degree[a] += 1
        degree[b] += 1
        if a > b:
            a, b = b, a
        road_set.add((a, b))

    max_rank = 0

    # 3️⃣ 暴力枚举所有城市对，计算网络秩
    for i in range(n):
        for j in range(i + 1, n):
            # 先把两座城市的度相加
            cur = degree[i] + degree[j]
            # 若它们之间有直接道路，则需要减掉重复计数的 1
            if (i, j) in road_set:
                cur -= 1
            max_rank = max(max_rank, cur)

    return max_rank
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  与暴力解相同，只是把“是否相连”的检查从线性搜索提升到了常数时间，避免了潜在的 `O(n³)`。  
- **空间复杂度**：`O(n + m)`（`m = len(roads)`）  
  - `degree` 用 `O(n)` 空间。  
  - `road_set` 用 `O(m)` 空间，最多 `n·(n-1)/2` 条道路。  
  与矩阵实现的 `O(n²)` 相比稍省空间，但在本题规模下差别不大。

---

## 心得

- **核心技巧**：先统计每个节点的度，再用哈希表（或矩阵）把“是否相连”查询降到 O(1)。  
- **适用场景**：  
  1. **计算两点之间的度和**（如本题、LeetCode 1615）。  
  2. **判断图中是否存在直接边**（如判断两人是否是朋友、社交网络分析）。  
  3. **找最大/最小度数配对**（如“最大度数的两点”类问题）。  
- **解题钥匙**：**预处理 adjacency 信息**——把“是否相连”这件事提前算好，后面查询就能瞬间得到答案。

---

## 反思

- **第一反应**：看到“网络秩”这个定义，我立刻想到“度（degree）”，于是想把每座城市的度先算出来，再两两配对。  
- **最容易踩的坑**：  
  - **重复计数**：两座城市之间如果有直接道路，需要在度之和里减掉一次，否则会把同一条道路算两次。  
  - **相连查询的实现**：如果每次都遍历 `roads` 去找是否相连，时间会爆炸。一定要用集合或矩阵做 O(1) 查询。  
  - **边界情况**：`roads` 可能为空，所有城市的度都是 0，答案应为 0；或者只有一条道路，答案应为 1。  
- **下次遇到同类题**，第一步应该想到：**统计每个节点的度 + 建立快速相连查询**，然后在此基础上遍历所有配对求最大/最小值。