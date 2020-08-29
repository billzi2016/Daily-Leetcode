# #973. 距离原点最近的 K 个点 / K Closest Points to Origin

> 难度：中等 · 标签：Array、Math、Divide and Conquer、Geometry、Sorting、Heap (Priority Queue)、Quickselect · [LeetCode 链接](https://leetcode.com/problems/k-closest-points-to-origin/)

---

## 题目（英文原版）

**Description**

Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).
You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

**Examples**

**Example 1:**

```
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].
```

**Example 2:**

```
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.
```

**Constraints**

- 1 <= k <= points.length <= 104
- -104 <= xi, yi <= 104

---

## 题目（中文翻译）

给定一个点数组，其中 `points[i] = [xi, yi]` 表示平面直角坐标系中的一个点 (point)，以及一个整数 `k`，返回离原点 `(0, 0)` 最近的 `k` 个点。

平面上两点之间的距离使用欧几里得距离（Euclidean distance），即  
\[
\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
\]

返回的答案可以是任意顺序。答案在点的集合上是唯一的（除去顺序的不同）。

**示例 1**  

**示例 2**  

**约束条件**  

- `1 <= k <= points.length <= 10^4`
- `-10^4 <= xi, yi <= 10^4`

### 示例

#### 示例 1
**输入**  
``` 
points = [[1,3],[-2,2]], k = 1
```  
**输出**  
```
[[-2,2]]
```  
**解释**  
点 `(1, 3)` 到原点的距离是 `sqrt(10)`。  
点 `(-2, 2)` 到原点的距离是 `sqrt(8)`。  
因为 `sqrt(8) < sqrt(10)`，所以 `(-2, 2)` 更靠近原点。  
我们只需要最近的 `k = 1` 个点，因此答案为 `[[‑2,2]]`。

#### 示例 2
**输入**  
``` 
points = [[3,3],[5,-1],[-2,4]], k = 2
```  
**输出**  
```
[[3,3],[-2,4]]
```  
**解释**  
答案 `[[‑2,4],[3,3]]` 也是被接受的，只要返回任意两个最近的点即可。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 把每个点到原点的距离算出来。  
   - 这里我们用 **欧氏距离的平方**（`x² + y²`），因为只比较大小，根号 `√` 并不会改变顺序，省去一次开根号的计算。  
2. 把所有点按照距离从小到大排个序。  
   - 排序就像把一堆书按照厚度从薄到厚摆放，最薄的自然在前面。  
3. 取排好序的前 `k` 个点返回。

> **为什么正确？**  
> 排序后，距离最小的 `k` 个点一定是离原点最近的 `k` 个点，因为我们把所有点都按照距离排了序。

#### 代码（Python）

```python
from typing import List

def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    # 1. 计算每个点到原点的距离的平方，并把距离与点本身组成一个元组
    #    (dist, [x, y]) 这里 dist = x*x + y*y
    points_with_dist = [(x * x + y * y, [x, y]) for x, y in points]

    # 2. 按照距离（元组的第一个元素）从小到大排序
    points_with_dist.sort(key=lambda item: item[0])

    # 3. 取前 k 个点的坐标部分返回
    return [pt for _, pt in points_with_dist[:k]]
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n` 是点的个数。我们要遍历一次算距离是 `O(n)`，随后对 `n` 个元素进行排序，排序的代价是 `O(n log n)`，整体就是 `O(n log n)`。  
  - 大白话：如果有 1 万个点，排序大概需要 1 万 × log₂(1 万) ≈ 1 万 × 14 次比较，远比 `n²`（一亿次）要少。

- **空间复杂度**：`O(n)`  
  - 需要额外的列表来存放每个点的距离，大小与原数组成正比。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **排序**：我们把所有点都排了序，实际上只需要找出最小的 `k` 个，而不是全部排好序。

**优化思路**：

- **维护一个大小为 `k` 的最大堆（max‑heap）**  
  - 堆是一种特殊的完全二叉树，根节点总是最大的（max‑heap）或最小的（min‑heap）。  
  - 想象成一堆装满了 `k` 本“最重的书”的箱子，箱子顶端（根）总是最重的那本。  
- **遍历所有点**  
  1. 把当前点的距离（平方）加入堆中。  
  2. 如果堆的大小超过 `k`，就把堆顶（即当前堆中**最远**的点）弹出。  
  - 这样堆里始终保留的是已经看到的点中距离最近的 `k` 个。  
- **遍历结束后，堆里剩下的就是答案**。

使用 Python 的 `heapq` 实现 **最小堆**，所以我们把距离取负数来“伪装”成最大堆。

**为什么更快？**  
- 堆的插入和弹出都是 `O(log k)`，而不是 `O(log n)`。  
- 整体遍历 `n` 次，总代价是 `O(n log k)`。当 `k` 远小于 `n` 时，这比 `O(n log n)` 快很多。

#### 代码（Python）

```python
import heapq
from typing import List

def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    # max-heap 用负数实现，堆中保存 ( -dist, [x, y] )
    max_heap = []

    for x, y in points:
        dist = x * x + y * y          # 计算距离的平方
        # 把 (负距离, 点) 加入堆
        heapq.heappush(max_heap, (-dist, [x, y]))
        # 如果堆的大小超过 k，弹出距离最远的点（堆顶的负距离最大，即距离最小的负数）
        if len(max_heap) > k:
            heapq.heappop(max_heap)   # 弹出后堆里只剩下最近的 k 个点

    # 堆中剩下的就是最近的 k 个点，取出坐标部分返回
    return [pt for _, pt in max_heap]
```

#### 复杂度

- **时间复杂度**：`O(n log k)`  
  - 对每个点做一次 `heappush`（`O(log k)`）并可能一次 `heappop`（也是 `O(log k)`），总共 `n` 次操作。  
  - 当 `k` 很小（比如只要前 10 个），`log k` 远小于 `log n`，所以运行更快。

- **空间复杂度**：`O(k)`  
  - 堆里最多只保存 `k` 个元素，和 `k` 成正比。  

---

## 心得

- **核心技巧**：**最大堆（或最小堆）** 用来维护 “前 `k` 小/大的元素”。  
- **适用题型**：  
  1. **Kth Largest Element in an Array**（第 K 大元素）  
  2. **Top K Frequent Words**（出现频率最高的 K 个单词）  
  3. **Find K Smallest Pairs**（找出和最小的 K 对数）  
- **一句话总结**：  
  > “只要想要前 `k` 名，就用大小为 `k` 的堆把其余的都踢出去。”

---

## 反思

- **第一反应**：直接把所有点排序，然后切片。最直接、最安全，但忽视了 `k` 可能远小于 `n` 的事实。  
- **最容易踩的坑**：  
  - **忘记用距离的平方**：直接算根号会增加不必要的计算量。  
  - **堆的方向写反**：Python 只提供最小堆，需要用负数或自定义比较来实现最大堆。  
  - **返回结果的顺序**：题目说答案顺序可以随意，但如果后续要保持特定顺序，需要再排序一次。  
- **下次类似题的第一步**：  
  > “先判断 `k` 与 `n` 的大小关系，若 `k` 远小于 `n`，就考虑用堆或 Quick‑Select；否则直接排序也可以接受。”