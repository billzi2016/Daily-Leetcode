# #3275. 第 k 最近障碍查询 / K-th Nearest Obstacle Queries

> 难度：中等 · 标签：Array、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/k-th-nearest-obstacle-queries/)

---

## 题目（英文原版）

**Description**

There is an infinite 2D plane.
You are given a positive integer k. You are also given a 2D array queries, which contains the following queries:
After each query, you need to find the distance of the kth nearest obstacle from the origin.
Return an integer array results where results[i] denotes the kth nearest obstacle after query i, or results[i] == -1 if there are less than k obstacles.
Note that initially there are no obstacles anywhere.
The distance of an obstacle at coordinate (x, y) from the origin is given by |x| + |y|.

**Examples**

**Example 1:**

```
Input: queries = [[1,2],[3,4],[2,3],[-3,0]], k = 2
Output: [-1,7,5,3]
Explanation:
```

**Example 2:**

```
Input: queries = [[5,5],[4,4],[3,3]], k = 1
Output: [10,8,6]
Explanation:
```

**Constraints**

- 1 <= queries.length <= 2 * 105
- All queries[i] are unique.
- -109 <= queries[i][0], queries[i][1] <= 109
- 1 <= k <= 105

---

## 题目（中文翻译）

在一个无限的二维平面（2D plane）上，你需要处理一系列查询。给定一个正整数 k，以及一个二维数组（2D array）`queries`，其中每个元素表示一次查询的坐标。

- 初始时平面上没有任何障碍物（obstacle）。
- 每执行一次查询，你需要在对应坐标处**添加**一个障碍物。
- 在添加完该障碍物后，求原点（origin）到第 k 近的障碍物的距离。如果当前平面上的障碍物数量少于 k，则返回 -1。

障碍物在坐标 (x, y) 处到原点的距离定义为 **曼哈顿距离**：`|x| + |y|`。

返回一个整数数组 `results`，其中 `results[i]` 表示第 i 次查询后第 k 最近障碍物的距离，或在障碍物不足 k 个时为 -1。

---

### 示例

**示例 1**

```
输入: queries = [[1,2],[3,4],[2,3],[-3,0]], k = 2
输出: [-1,7,5,3]
解释：
```

**示例 2**

```
输入: queries = [[5,5],[4,4],[3,3]], k = 1
输出: [10,8,6]
解释：
```

---

### 约束条件

- `1 <= queries.length <= 2 * 10^5`
- 所有 `queries[i]` 均唯一。
- `-10^9 <= queries[i][0], queries[i][1] <= 10^9`
- `1 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次查询都当成一次“插入障碍物”，随后把所有已经出现的障碍物的距离（`|x| + |y|`）全部列出来，排序后取第 `k` 小的那个。  

- **用到的数据结构**：  
  - **列表（List）**：用来存放已经出现的障碍物的距离。可以把它想象成一本“距离手册”，每次把新障碍物的距离写进去。  
  - **排序**：把手册里的距离从小到大排好序，类似把书按字母顺序排好，这样第 `k` 小的距离就直接在第 `k` 位上。

- **为什么正确**：  
  只要把所有障碍物的真实距离都列出来并且按照从小到大排好顺序，第 `k` 小的距离必然就是离原点第 `k` 近的障碍物的距离。即使后面再加入更多障碍物，只要重新排序，答案仍然是第 `k` 小的那个。

- **时间/空间复杂度**：  
  - 每插入一次障碍物后都要**排序**全部已有距离，排序的时间复杂度是 `O(n log n)`（`n` 为当前障碍物数），这里的 `log n` 可以理解为“把 `n` 本书按照字母顺序排好需要的层层比较”。  
  - 因此总的时间复杂度是 `O(m² log m)`（`m = queries.length`），因为第 `i` 次查询要排 `i` 条记录，累加下来约等于 `m²`。  
  - 额外的空间只需要保存所有距离，`O(m)`。

#### 代码（Python）

```python
from typing import List

def kthNearestObstacles_bruteforce(queries: List[List[int]], k: int) -> List[int]:
    # 保存已经出现的障碍物距离
    distances: List[int] = []
    # 最终答案
    ans: List[int] = []

    for x, y in queries:
        # 计算新障碍物到原点的曼哈顿距离
        d = abs(x) + abs(y)          # |x| + |y|
        distances.append(d)          # 把距离写进“手册”

        # 把所有距离从小到大排好序
        distances.sort()             # O(len(distances) * log len(distances))

        # 判断是否已经有足够的障碍物
        if len(distances) < k:
            ans.append(-1)           # 不足 k 个，答案为 -1
        else:
            ans.append(distances[k-1])   # 第 k 小的距离（列表是 0 索引）

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m² log m)`  
  - 想象把 1、2、3 … m 本书一次一次放进书架并每次重新排好序，整体工作量大约是 `m²`（平方）级别，再乘上 `log m` 的比较次数。

- **空间复杂度**：`O(m)`  
  - 只需要保存所有出现过的距离，最多和查询次数一样多。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要把所有距离重新排序**，这一步非常耗时。  
观察题目要求的其实只是 **第 k 小的距离**，而不是完整的排序结果。只要我们能够随时拿到当前第 `k` 小的距离，就不需要对全部数据进行排序。

**关键观察**（提示里已经暗示）：

- 当障碍物的数量已经超过 `k` 时，**第 k+1 小的障碍物永远不可能成为答案**。因为答案只关心第 `k` 小，更多的、更远的障碍物对答案没有影响。  
- 因此我们只需要维护 **当前最小的 k 个距离**，其余更大的距离可以直接丢掉。

**如何维护这 k 个最小距离？**  
使用 **最大堆（max‑heap）**（在 Python 中用负数实现的最小堆）：

- 堆里保存 **当前 k 个最小距离**，但堆顶保存的是这 k 个里 **最大的**（即第 k 小的距离）。  
- 当新障碍物的距离 `d` 小于堆顶（第 k 小）时，说明 `d` 应该进入前 `k` 小的集合：弹出堆顶（把原来的第 k 小踢出），把 `d` 插入堆中。  
- 当 `d` 大于等于堆顶时，直接丢掉，因为它一定不是前 `k` 小的一员。

这样：

- **查询答案**：如果堆的大小小于 `k`，说明目前障碍物不足 `k` 个，答案是 `-1`；否则堆顶（取负后）就是第 `k` 小的距离。  
- **每次操作**只涉及堆的 `push` / `pop`，时间是 `O(log k)`，远远快于 `O(n log n)`。

**最大堆的实现细节**（Python 的 `heapq` 只能实现最小堆）：

- 把每个距离取负数放进堆，负数越大（即原距离越小）在堆顶。  
- 取答案时，需要把负数再取负回来。

#### 代码（Python）

```python
import heapq
from typing import List

def kthNearestObstacles(queries: List[List[int]], k: int) -> List[int]:
    """
    使用最大堆（通过负数实现）维护当前最小的 k 个距离。
    """
    # max‑heap，实际存的是负距离
    max_heap: List[int] = []          # heap[0] 保存的是 -第k小的距离
    ans: List[int] = []

    for x, y in queries:
        d = abs(x) + abs(y)            # 当前障碍物到原点的曼哈顿距离

        if len(max_heap) < k:
            # 堆还没有满 k，直接放进去
            heapq.heappush(max_heap, -d)   # 放负数，形成“最大堆”
        else:
            # 堆已经满 k，堆顶是当前的第 k 小（负数最小）
            if d < -max_heap[0]:            # 如果新距离更小
                heapq.heappushpop(max_heap, -d)   # 弹出最大的（即第k小），再放进新距离

        # 计算本次查询的答案
        if len(max_heap) < k:
            ans.append(-1)               # 障碍物不足 k 个
        else:
            ans.append(-max_heap[0])     # 取负得到第 k 小的距离

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m log k)`  
  - 每次查询只做一次堆的 `push` / `pushpop`，每次操作的代价是 `log k`（对数），可以理解为“把新书放进只装 `k` 本书的书架，需要比较 `log k` 次”。相比暴力的 `O(m² log m)`，提升巨大。

- **空间复杂度**：`O(k)`  
  - 堆里最多只保存 `k` 条记录，和 `k` 成正比。

---

## 心得

- **核心技巧**：**维护固定大小的最大堆（或最小堆）来实时获取第 k 小/大的元素**。  
- **适用的题型**（类似思路）：
  1. “滑动窗口第 K 小/大元素”  
  2. “动态流（stream）中第 K 大元素” (`LeetCode 703`）  
  3. “Kth Largest Element in a Matrix” (`LeetCode 378`)  

- **一句话总结**：**只保留对答案有影响的前 k 条记录，用堆快速维护第 k 小的距离**。

---

## 反思

- **第一反应**：看到“每次查询后求第 k 最近的障碍物”，立刻想到把所有距离收集后排序。  
- **最容易踩的坑**：  
  - 忘记处理 “障碍物少于 k 个” 的情况，需要返回 `-1`。  
  - 堆的实现细节：Python 只有最小堆，需要把距离取负才能模拟最大堆，否则堆顶会是最小距离，导致逻辑相反。  
  - `k` 可能非常大（`10⁵`），如果直接用 `list.sort()` 会导致超时或内存爆炸。  

- **下次遇到同类题**，第一步应该问自己：“我真的需要完整排序吗？我只关心第 k 小（大）”，如果答案是否定的，就立刻考虑 **堆** 或 **计数排序/桶排序** 等只保留必要元素的结构。