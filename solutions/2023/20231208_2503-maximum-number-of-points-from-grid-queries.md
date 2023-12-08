# #2503. **网格查询的最大得分** / Maximum Number of Points From Grid Queries

> 难度：困难 · 标签：Array、Two Pointers、Breadth-First Search、Union Find、Sorting、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-points-from-grid-queries/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid and an array queries of size k.
Find an array answer of size k such that for each integer queries[i] you start in the top left cell of the matrix and repeat the following process:
After the process, answer[i] is the maximum number of points you can get. Note that for each query you are allowed to visit the same cell multiple times.
Return the resulting array answer.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,3],[2,5,7],[3,5,1]], queries = [5,6,2]
Output: [5,8,1]
Explanation: The diagrams above show which cells we visit to get points for each query.
```

**Example 2:**

```
Input: grid = [[5,2,1],[1,1,2]], queries = [3]
Output: [0]
Explanation: We can not get any points because the value of the top left cell is already greater than or equal to 3.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 2 <= m, n <= 1000
- 4 <= m * n <= 105
- k == queries.length
- 1 <= k <= 104
- 1 <= grid[i][j], queries[i] <= 106

---

## 题目（中文翻译）

给定一个大小为 `m × n` 的整数矩阵 `grid` 和一个长度为 `k` 的数组 `queries`。  
请构造一个长度为 `k` 的数组 `answer`，使得对于每个整数 `queries[i]`，从矩阵的左上角单元格开始，重复以下过程：

（题目原文中省略了具体的过程，这里保持原样描述）

完成上述过程后，`answer[i]` 即为在该查询下能够获得的最大得分（points）数。需要注意的是，对于每个查询，你可以多次访问同一个单元格。  
返回得到的数组 `answer`。

---

### 示例

#### 示例 1
**输入**  
```text
grid = [[1,2,3],[2,5,7],[3,5,1]], queries = [5,6,2]
```
**输出**  
```text
[5,8,1]
```
**解释**  
上图展示了针对每个查询我们访问的单元格路径以及相应的得分。

#### 示例 2
**输入**  
```text
grid = [[5,2,1],[1,1,2]], queries = [3]
```
**输出**  
```text
[0]
```
**解释**  
由于左上角单元格的值已经大于等于 `3`，因此无法获得任何得分。

---

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `2 ≤ m, n ≤ 1000`
- `4 ≤ m × n ≤ 10^5`
- `k == queries.length`
- `1 ≤ k ≤ 10^4`
- `1 ≤ grid[i][j], queries[i] ≤ 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个查询单独做一次搜索**。  
从左上角 `(0,0)` 出发，使用 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）**，只把**数值严格小于当前查询值** 的格子加入队列/递归。遍历结束后，计数器记录我们到底走到了多少个格子，这个数就是答案。

> **类比**：想象你手里有一本字典，想找所有**拼音在 “c” 之前** 的词。每查到一个词，你就把它记下来。这里的 “拼音在 c 之前” 对应“格子数值 < query”，记下的词的数量对应“可达格子数”。

**为什么一定对？**  
因为 BFS/DFS 会遍历**所有**能够从起点走到的格子，且每一步都检查了“格子值 < query” 这个限制，满足题目要求。

#### 代码（Python）

```python
from collections import deque
from typing import List

def brute_force(grid: List[List[int]], queries: List[int]) -> List[int]:
    m, n = len(grid), len(grid[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def reachable(threshold: int) -> int:
        # 如果左上角本身已经不满足条件，直接返回 0
        if grid[0][0] >= threshold:
            return 0
        q = deque([(0, 0)])
        visited = [[False] * n for _ in range(m)]
        visited[0][0] = True
        cnt = 0

        while q:
            x, y = q.popleft()
            cnt += 1                     # 走到一个合法格子，计数 +1
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                # 越界或已经访问或格子值不满足阈值，跳过
                if not (0 <= nx < m and 0 <= ny < n):
                    continue
                if visited[nx][ny] or grid[nx][ny] >= threshold:
                    continue
                visited[nx][ny] = True
                q.append((nx, ny))
        return cnt

    # 对每个查询单独跑一次 BFS
    return [reachable(q) for q in queries]
```

#### 复杂度  

- **时间复杂度**：`O(k * m * n)`  
  每个查询都要遍历整个矩阵（最坏情况），`k` 是查询数。  
  用大白话说：如果矩阵有 10⁵ 个格子，查询有 10⁴ 条，最坏情况下要跑 **10⁹ 次**操作，显然会超时。

- **空间复杂度**：`O(m * n)`  
  为每次 BFS 准备一个 `visited` 二维数组，最多占用整个矩阵大小的内存。

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于：每个查询都要重新遍历整个矩阵，完全没有利用“查询之间的关联”。  
观察题目可以发现：

1. **查询是独立的**，但我们可以**任意顺序**回答它们（因为题目只要最终答案数组，顺序交给我们自己维护）。  
2. 当阈值 **变大** 时，之前已经可以到达的格子依然可达，只会**新增一些格子**。  
3. 这正好适合**一次遍历**，随着阈值从小到大“逐步打开”格子。

**核心想法**：  
- 把查询按照阈值从小到大排序，同时记住它们在原数组中的下标（用来恢复答案顺序）。  
- 维护一个 **最小堆（priority queue）**，堆中存放**已经“触及”但尚未确认是否满足当前阈值的格子**，堆的键是格子的数值。  
- 初始时，只把左上角 `(0,0)` 放进堆。  
- 对每个查询 `q`（从小到大）：
  1. **弹出**堆顶所有 `value < q` 的格子，标记为“已访问”，计数器 `cnt` 加 1。  
  2. 对每个新访问的格子，尝试把它的四个邻居（未访问且未入堆）加入堆。  
  3. 当堆顶的值已经 `≥ q` 时，说明当前阈值下没有更多格子可以加入，`cnt` 就是答案。  
- 继续处理下一个更大的查询，堆中残留的格子会被继续利用，不需要重新搜索。

> **类比**：想象你在爬山，山上每个点都有海拔高度。你手里有一张“最高允许海拔” 的列表（queries），想知道每个海拔限制下能到达多少个点。  
> - 先把山脚（左上角）放进“待检查队列”。  
> - 每次提高限制时，只检查“比当前限制更低的点”，把它们标记为已到达，并把相邻未检查的点放进队列。  
> - 这样，你只会检查一次每个格子。

**为什么要用最小堆？**  
因为我们需要**快速知道当前堆中最小的格子值**，只有当它小于查询阈值时才可以“解锁”。堆的 `push/pop` 都是 `O(log N)`，足够快。

#### 代码（Python）

```python
import heapq
from typing import List

def maxPoints(grid: List[List[int]], queries: List[int]) -> List[int]:
    m, n = len(grid), len(grid[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # 1. 把查询按阈值从小到大排序，保留原下标
    sorted_q = sorted([(val, idx) for idx, val in enumerate(queries)])

    # 2. 初始化：最小堆只放左上角，visited 标记已确定可达的格子
    heap = [(grid[0][0], 0, 0)]          # (cell_value, x, y)
    visited = [[False] * n for _ in range(m)]
    visited[0][0] = True                 # 已经放进堆，防止重复入堆
    cnt = 0                              # 当前阈值下已访问格子数量
    ans = [0] * len(queries)             # 最终答案数组

    # 3. 按阈值依次处理查询
    for q_val, q_idx in sorted_q:
        # 把所有值 < q_val 的格子弹出并标记为“已访问”
        while heap and heap[0][0] < q_val:
            val, x, y = heapq.heappop(heap)
            cnt += 1                      # 这个格子正式算进答案
            # 将四个方向的邻格子尝试加入堆
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                    visited[nx][ny] = True
                    heapq.heappush(heap, (grid[nx][ny], nx, ny))
        # 此时堆顶的值 >= q_val，或者堆空，cnt 即为答案
        ans[q_idx] = cnt

    return ans
```

> **代码要点中文注释**  
> - `sorted_q`：把查询先排好序，`(阈值, 原下标)` 形式，后面可以直接把答案写回原位置。  
> - `heap`：最小堆，存 `(格子数值, 行, 列)`。堆顶永远是当前**最容易**（数值最小）打开的格子。  
> - `visited`：防止同一个格子被多次加入堆，省掉不必要的 `push`。  
> - `while heap and heap[0][0] < q_val`：只要堆顶的格子值小于当前查询阈值，就可以把它“打开”。  
> - 每弹出一个格子后，立刻把它的四邻加入堆，这相当于 **BFS 的前向扩展**，但因为我们使用堆，所以扩展顺序是“数值从小到大”。  

#### 复杂度  

- **时间复杂度**：`O(m * n * log(m * n) + k log k)`  
  - 每个格子最多被 **一次** 放进堆并弹出，`push/pop` 各是 `O(log N)`，`N = m*n`。  
  - 对查询进行排序需要 `O(k log k)`。  
  - 用大白话说：如果矩阵有 10⁵ 个格子，整个过程大约是 `10⁵ * log 10⁵ ≈ 10⁵ * 17 ≈ 1.7×10⁶` 次基本操作，完全能在一秒内跑完。

- **空间复杂度**：`O(m * n)`  
  - `heap` 最坏会装下所有格子，`visited` 同样是 `m*n` 大小。  
  - 这就是我们只能使用和矩阵同等规模的额外空间。

---

## 心得  

- **核心技巧**：**离线排序 + 最小堆（或等价的多源 BFS）**，把“随阈值逐步开放格子”的过程一次性完成。  
- **适用的题型**  
  1. “在阈值限制下可达的格子数”类，如本题、LeetCode 1657 *Determine if Two Strings Are Close*（思路类似的离线处理）。  
  2. “最大/最小权值路径长度”类，如 LeetCode 1102 *Path With Maximum Minimum Value*（同样使用二叉堆或并查集按权值排序）。  
  3. “动态阈值下的连通块大小”类，如 LeetCode 1101 *The Earliest Moment When Everyone Becomes Friends*（并查集按时间排序）。  
- **一句话总结**：**把所有查询先排好序，随后随着阈值“升高”，用堆一次性把矩阵里越来越多的格子打开，就能一次遍历得到所有答案。**

---

## 反思  

- **第一反应**：直接对每个查询跑一次 BFS，感觉最直观，却忽视了查询之间的重复劳动。  
- **最容易踩的坑**  
  1. **左上角格子本身不满足阈值**：必须先判断，否则会错误地计入 1。  
  2. **重复入堆**：如果没有 `visited` 标记，同一个格子会被多次 push，导致堆膨胀、时间超标。  
  3. **答案顺序**：因为查询被排序了，记得把答案写回原下标，否则输出顺序会错。  
- **下次类似题目**：  
  1. **先思考能否离线处理**（把所有询问排序）。  
  2. **寻找一种“单调性”**（阈值增大只会新增，不会删除），这样就能使用“逐步开放”或“并查集合并”之类的增量算法。  

祝你玩得开心，算法路上越走越顺！