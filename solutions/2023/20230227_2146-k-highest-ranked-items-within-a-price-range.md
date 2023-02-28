# #2146. 价格区间内排名前 K 的商品 / K Highest Ranked Items Within a Price Range

> 难度：中等 · 标签：Array、Breadth-First Search、Sorting、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/k-highest-ranked-items-within-a-price-range/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array grid of size m x n that represents a map of the items in a shop. The integers in the grid represent the following:
It takes 1 step to travel between adjacent grid cells.
You are also given integer arrays pricing and start where pricing = [low, high] and start = [row, col] indicates that you start at the position (row, col) and are interested only in items with a price in the range of [low, high] (inclusive). You are further given an integer k.
You are interested in the positions of the k highest-ranked items whose prices are within the given price range. The rank is determined by the first of these criteria that is different:
Return the k highest-ranked items within the price range sorted by their rank (highest to lowest). If there are fewer than k reachable items within the price range, return all of them.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,0,1],[1,3,0,1],[0,2,5,1]], pricing = [2,5], start = [0,0], k = 3
Output: [[0,1],[1,1],[2,1]]
Explanation: You start at (0,0).
With a price range of [2,5], we can take items from (0,1), (1,1), (2,1) and (2,2).
The ranks of these items are:
- (0,1) with distance 1
- (1,1) with distance 2
- (2,1) with distance 3
- (2,2) with distance 4
Thus, the 3 highest ranked items in the price range are (0,1), (1,1), and (2,1).
```

**Example 2:**

```
Input: grid = [[1,2,0,1],[1,3,3,1],[0,2,5,1]], pricing = [2,3], start = [2,3], k = 2
Output: [[2,1],[1,2]]
Explanation: You start at (2,3).
With a price range of [2,3], we can take items from (0,1), (1,1), (1,2) and (2,1).
The ranks of these items are:
- (2,1) with distance 2, price 2
- (1,2) with distance 2, price 3
- (1,1) with distance 3
- (0,1) with distance 4
Thus, the 2 highest ranked items in the price range are (2,1) and (1,2).
```

**Example 3:**

```
Input: grid = [[1,1,1],[0,0,1],[2,3,4]], pricing = [2,3], start = [0,0], k = 3
Output: [[2,1],[2,0]]
Explanation: You start at (0,0).
With a price range of [2,3], we can take items from (2,0) and (2,1). 
The ranks of these items are: 
- (2,1) with distance 5
- (2,0) with distance 6
Thus, the 2 highest ranked items in the price range are (2,1) and (2,0). 
Note that k = 3 but there are only 2 reachable items within the price range.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- 0 <= grid[i][j] <= 105
- pricing.length == 2
- 2 <= low <= high <= 105
- start.length == 2
- 0 <= row <= m - 1
- 0 <= col <= n - 1
- grid[row][col] > 0
- 1 <= k <= m * n

---

## 题目（中文翻译）

给定一个 **0 索引** 的二维整数数组 `grid`，大小为 `m × n`，它表示商店中商品的布局。`grid` 中的整数含义如下：

- `0` 表示该格子不可通行（没有商品），
- 正整数表示该格子有商品，且其数值即为商品的价格。

在相邻格子之间移动一步的代价为 `1`。

另给定整数数组 `pricing` 和 `start`，其中 `pricing = [low, high]` 表示只关心价格落在区间 **[low, high]**（闭区间）内的商品，`start = [row, col]` 表示起始位置为 `(row, col)`。再给定一个整数 `k`。

你的任务是找出 **价格在给定区间内且可达的** 前 `k` 名商品的位置。商品的排名依据以下顺序逐项比较，直至出现不同项为止：

1. 与起始位置的 **距离（distance）**（即最短路径步数），距离越小排名越高；
2. 商品的 **价格（price）**，价格越低排名越高；
3. 商品所在的 **行号（row）**，行号越小排名越高；
4. 商品所在的 **列号（col）**，列号越小排名越高。

返回这些商品的坐标列表，按照排名从高到低排序。如果可达且满足价格区间的商品不足 `k` 个，返回全部符合条件的商品。

---

### 示例

**示例 1**

```
Input: grid = [[1,2,0,1],
               [1,3,0,1],
               [0,2,5,1]], pricing = [2,5], start = [0,0], k = 3
Output: [[0,1],[1,1],[2,1]]
Explanation: 你从 (0,0) 出发。
在价格区间 [2,5] 内的商品位于 (0,1)、(1,1)、(2,1) 和 (2,2)。
这些商品的排名如下：
- (0,1) 的距离为 1
- (1,1) 的距离为 2
- (2,1) 的距离为 3
- (2,2) 的距离为 4
因此排名前 3 的商品坐标为 [[0,1],[1,1],[2,1]]。
```

**示例 2**

```
Input: grid = [[1,2,0,1],
               [1,3,3,1],
               [0,2,5,1]], pricing = [2,3], start = [2,3], k = 2
Output: [[2,1],[1,2]]
Explanation: 你从 (2,3) 出发。
在价格区间 [2,3] 内的商品位于 (0,1)、(1,1)、(1,2) 和 (2,1)。
这些商品的排名如下：
- (2,1) 距离 2，价格 2
- (1,2) 距离 2，价格 3
- (1,1) 距离 3
- (0,1) 距离 4
因此排名前 2 的商品坐标为 [[2,1],[1,2]]。
```

**示例 3**

```
Input: grid = [[1,1,1],
               [0,0,1],
               [2,3,4]], pricing = [2,3], start = [0,0], k = 3
Output: [[2,1],[2,0]]
Explanation: 你从 (0,0) 出发。
在价格区间 [2,3] 内的商品位于 (2,0) 和 (2,1)。
这些商品的排名如下：
- (2,1) 距离 5
- (2,0) 距离 6
因此排名前 2 的商品坐标为 [[2,1],[2,0]]。
注意 k = 3，但实际可达且符合价格区间的商品只有 2 个。
```

---

### 约束

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 10⁵`
- `1 ≤ m * n ≤ 10⁵`
- `0 ≤ grid[i][j] ≤ 10⁵`
- `pricing.length == 2`
- `2 ≤ low ≤ high ≤ 10⁵`
- `start.length == 2`
- `0 ≤ row ≤ m - 1`
- `0 ≤ col ≤ n - 1`
- `grid[row][col] > 0` （起始位置一定有商品）
- `1 ≤ k ≤ m * n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个格子都当作目标，分别算它到起点的最短步数**，然后挑出价格在 `[low, high]` 区间的格子，再把它们按「距离 → 价格 → 行号 → 列号」的顺序排好，取前 `k` 个。

- **数据结构**  
  - **队列（Queue）**：用来做广度优先搜索（BFS），每次从队首弹出一个坐标，再把它的四个相邻格子加入队尾。可以把队列想象成「排队买饭」的队伍，先进来的先走，保证我们一次遍历的格子距离起点是递增的。  
  - **哈希表 / 集合（set）**：记录已经访问过的格子，防止走回头路。哈希表就像一本「字典」，键是坐标 `(r,c)`，查找是否出现只要一眼就能看到。

- **为什么正确**  
  对每个格子都跑一次 BFS，能够得到 **从起点到该格子的最短路径长度**（因为 BFS 按层次展开，第一次到达某个格子时的步数一定是最小的）。只要把所有符合价格区间的格子收集起来，再按题目给出的四条排序规则排序，就能得到「排名」最靠前的 `k` 个格子。

- **时间 / 空间复杂度（大白话）**  
  - **时间复杂度**：对每个格子（最多 `m·n`）都要跑一次 BFS，单次 BFS 最坏要遍历整个网格 `O(m·n)`，所以总时间是 `O((m·n)²)`。想象一下，网格有 10,000 格子，暴力解要跑 10,000 次遍历，每次又遍历 10,000 格子，耗时非常可怕。  
  - **空间复杂度**：一次 BFS 需要一个 `visited` 集合和一个队列，最多保存 `m·n` 个坐标，空间是 `O(m·n)`。

#### 代码（Python）

```python
from collections import deque

def bfs_distance(grid, start, target):
    """
    暴力版：为单个目标格子算最短距离
    """
    m, n = len(grid), len(grid[0])
    sr, sc = start
    q = deque([(sr, sc, 0)])          # (行, 列, 已走步数)
    visited = {(sr, sc)}             # 已经访问过的格子

    while q:
        r, c, d = q.popleft()
        if (r, c) == target:         # 第一次到达就是最短距离
            return d
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1                         # unreachable

def brute_force(grid, pricing, start, k):
    low, high = pricing
    m, n = len(grid), len(grid[0])
    candidates = []

    # 逐个格子检查是否满足价格区间
    for r in range(m):
        for c in range(n):
            price = grid[r][c]
            if low <= price <= high:               # 价格符合
                dist = bfs_distance(grid, start, (r, c))
                if dist != -1:                     # 能到达
                    candidates.append((dist, price, r, c))

    # 按 (距离, 价格, 行, 列) 排序
    candidates.sort()
    # 只取前 k 个坐标
    return [[r, c] for _, _, r, c in candidates[:k]]
```

#### 复杂度

- **时间复杂度**：`O((m·n)²)` —— 每个格子都要跑一次 BFS，遍历整个网格 `m·n` 次。  
- **空间复杂度**：`O(m·n)` —— 单次 BFS 需要的 visited 集合和队列大小最多是整个网格的格子数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于我们对每个格子都重复做 BFS**。事实上，**一次 BFS 就能得到所有格子到起点的最短距离**，因为 BFS 按层次展开，第一次遍历到的每个格子对应的步数就是它的最短距离。

**步骤如下**：

1. **一次 BFS**  
   - 从 `start` 开始，使用队列逐层向外扩散。  
   - 记录每个被访问格子的距离 `dist`（层数），并把 **满足价格区间** 的格子加入候选列表 `items`。  
   - 由于 BFS 按距离递增访问，`dist` 本身已经是第一条排序依据。

2. **对候选格子排序**  
   - 候选列表中每个元素保存 `(dist, price, row, col)`。  
   - 使用 Python 的 `sort`（基于 Timsort，时间复杂度 `O(N log N)`，`N` 为候选格子数量），一次性完成「距离 → 价格 → 行 → 列」的四重排序。

3. **取前 k**  
   - 排序后直接取前 `k`（如果不足 `k`，返回全部）。

> **如果想进一步节省排序的开销**，可以在遍历过程中维护一个大小为 `k` 的最大堆（`heapq`），只保留当前最好的 `k` 条记录。这样整体时间会是 `O(m·n + N log k)`，对 `k` 很小的情况更快。不过在本题的约束（`m·n ≤ 10⁵`）下，直接排序已经足够快且代码更简洁。

**关键概念解释**  

- **广度优先搜索（BFS）**  
  想象你站在起点，先走一步到所有相邻格子（第一层），再走两步到第二层，依此类推。因为每一步只能往四个方向走，层数自然等于最短步数。  
- **堆（Heap）**  
  堆是一棵满足「父节点总不大于子节点」的完全二叉树（最小堆）或「父节点总不小于子节点」的完全二叉树（最大堆）。在 Python 中用 `heapq` 实现，能在 `O(log size)` 的时间内插入或弹出最值。这里我们把「更差的」记录放进最大堆，当堆大小超过 `k` 时弹出最差的，最终堆里留下的就是最好的 `k` 条记录。

#### 代码（Python）

```python
from collections import deque
import heapq

def bfs_collect(grid, pricing, start):
    """
    单次 BFS 收集所有满足价格区间的格子，并返回 (dist, price, row, col) 列表
    """
    low, high = pricing
    m, n = len(grid), len(grid[0])
    sr, sc = start

    q = deque([(sr, sc, 0)])          # (行, 列, 距离)
    visited = {(sr, sc)}             # 已访问集合
    items = []                        # 候选格子

    while q:
        r, c, d = q.popleft()
        price = grid[r][c]
        # 如果当前格子价格在区间内，加入候选
        if low <= price <= high:
            items.append((d, price, r, c))

        # 向四个方向扩散
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc, d + 1))
    return items

def optimal_solution(grid, pricing, start, k):
    """
    最优解：一次 BFS + 排序（或最大堆）得到前 k 条结果
    """
    items = bfs_collect(grid, pricing, start)

    # 方法一：直接排序
    items.sort()                     # 按 (dist, price, row, col) 自动升序
    return [[r, c] for _, _, r, c in items[:k]]

    # 方法二：使用最大堆，只保留前 k 条（如果想进一步优化）
    # heap = []                       # 存放 (-dist, -price, -row, -col) 取负号让 heapq 成为最大堆
    # for d, price, r, c in items:
    #     heapq.heappush(heap, (-d, -price, -r, -c))
    #     if len(heap) > k:
    #         heapq.heappop(heap)    # 弹出最差的
    # # 把堆里的元素取出来并恢复正号，按要求排序
    # res = [(-dd, -pp, -rr, -cc) for dd, pp, rr, cc in heap]
    # res.sort()
    # return [[r, c] for _, _, r, c in res]

```

#### 复杂度

- **时间复杂度**：  
  - BFS 访问每个可达格子一次，`O(m·n)`。  
  - 对候选格子 `N`（`N ≤ m·n`）排序，`O(N log N)`。  
  - 整体 `O(m·n + N log N)`，在最坏情况下等价于 `O(m·n log (m·n))`。  
  - 与暴力解的 `O((m·n)²)` 相比，**大幅下降**——从「每个格子都跑一次完整遍历」变成「一次遍历全部格子」再加上「一次排序」。
- **空间复杂度**：  
  - `visited`、`queue`、`items` 最多保存 `m·n` 个坐标，`O(m·n)`。  
  - 若使用最大堆，则额外的堆大小最多是 `k`，即 `O(k)`（`k ≤ m·n`），仍在同一数量级。

---

## 心得

- **核心技巧**：一次 **广度优先搜索**（BFS）即可得到所有格子到起点的最短距离，再配合 **排序**（或 **堆**）选出排名前 `k` 的格子。  
- **适用的题型**：  
  1. “在网格中找最近的目标并排序”——如 LeetCode 1499 *Max Value of Equation*（思路相似的排序+扫描）。  
  2. “从起点出发，按距离层次遍历并挑选满足条件的元素”——如 1030 *Matrix Cells in Distance Order*。  
  3. “在图/网格中求最短路径并对路径属性进行二次排序”——如 864 *Shortest Path to Get All Keys*（BFS + 状态压缩）。  
- **一句话总结**：**一次 BFS 把距离全部算出来，随后用排序挑出最好的 k 条记录**，就是这道题的解题钥匙。

---

## 反思

- **第一反应**：看到“距离、价格、行、列”四个排序维度，我立刻想到要先把每个格子的距离算出来，于是想到对每个格子单独跑 BFS——这就是暴力思路。  
- **最容易踩的坑**  
  1. **障碍格子**（值为 `0`）不能通行，必须在 BFS 扩展时跳过。  
  2. **起点本身可能就是符合价格区间的格子**，别忘了把它加入候选。  
  3. **排序的顺序**必须严格遵循「距离 → 价格 → 行 → 列」四个条件，写错顺序会导致答案不对。  
  4. **大数据时的时间限制**：如果仍坚持对每个格子跑 BFS，必然 TLE。  
- **下次类似题的第一步**：先判断“是否可以一次遍历得到所有需要的基础信息”（如距离、层次），如果可以，就用 **一次 BFS/DFS** 把这些信息一次性收集，再在收集结果上做排序或堆操作。这样既保证正确性，又能把时间控制在 `O(N log N)` 甚至 `O(N log k)` 以内。