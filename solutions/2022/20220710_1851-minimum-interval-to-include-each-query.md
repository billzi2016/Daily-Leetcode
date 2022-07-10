# #1851. **包含每个查询的最小区间** / Minimum Interval to Include Each Query

> 难度：困难 · 标签：Array、Binary Search、Line Sweep、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-interval-to-include-each-query/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array intervals, where intervals[i] = [lefti, righti] describes the ith interval starting at lefti and ending at righti (inclusive). The size of an interval is defined as the number of integers it contains, or more formally righti - lefti + 1.
You are also given an integer array queries. The answer to the jth query is the size of the smallest interval i such that lefti <= queries[j] <= righti. If no such interval exists, the answer is -1.
Return an array containing the answers to the queries.

**Examples**

**Example 1:**

```
Input: intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]
Output: [3,3,1,4]
Explanation: The queries are processed as follows:
- Query = 2: The interval [2,4] is the smallest interval containing 2. The answer is 4 - 2 + 1 = 3.
- Query = 3: The interval [2,4] is the smallest interval containing 3. The answer is 4 - 2 + 1 = 3.
- Query = 4: The interval [4,4] is the smallest interval containing 4. The answer is 4 - 4 + 1 = 1.
- Query = 5: The interval [3,6] is the smallest interval containing 5. The answer is 6 - 3 + 1 = 4.
```

**Example 2:**

```
Input: intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]
Output: [2,-1,4,6]
Explanation: The queries are processed as follows:
- Query = 2: The interval [2,3] is the smallest interval containing 2. The answer is 3 - 2 + 1 = 2.
- Query = 19: None of the intervals contain 19. The answer is -1.
- Query = 5: The interval [2,5] is the smallest interval containing 5. The answer is 5 - 2 + 1 = 4.
- Query = 22: The interval [20,25] is the smallest interval containing 22. The answer is 25 - 20 + 1 = 6.
```

**Constraints**

- 1 <= intervals.length <= 105
- 1 <= queries.length <= 105
- intervals[i].length == 2
- 1 <= lefti <= righti <= 107
- 1 <= queries[j] <= 107

---

## 题目（中文翻译）

给定一个二维整数数组 `intervals`，其中 `intervals[i] = [left_i, right_i]` 表示第 `i` 个区间（interval）从 `left_i` 开始、在 `right_i` 结束（两端均包含）。区间的大小定义为它包含的整数个数，形式化为 `right_i - left_i + 1`。  

同时给定一个整数数组 `queries`。第 `j` 个查询（query）的答案是满足 `left_i ≤ queries[j] ≤ right_i` 的所有区间中，大小最小的区间的大小。如果不存在这样的区间，答案为 `-1`。  

返回一个数组，数组第 `j` 项即第 `j` 个查询的答案。

---

### 示例

#### 示例 1
> **输入**  
> `intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]`  
> **输出**  
> `[3,3,1,4]`  
> **解释**  
> - 查询 `= 2`：区间 `[2,4]` 是包含 `2` 的最小区间，答案为 `4 - 2 + 1 = 3`。  
> - 查询 `= 3`：区间 `[2,4]` 是包含 `3` 的最小区间，答案为 `4 - 2 + 1 = 3`。  
> - 查询 `= 4`：区间 `[4,4]` 是包含 `4` 的最小区间，答案为 `4 - 4 + 1 = 1`。  
> - 查询 `= 5`：区间 `[3,6]` 是唯一包含 `5` 的区间，答案为 `6 - 3 + 1 = 4`。

#### 示例 2
> **输入**  
> `intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]`  
> **输出**  
> `[2,-1,4,6]`  
> **解释**  
> - 查询 `= 2`：区间 `[2,3]` 是包含 `2` 的最小区间，答案为 `3 - 2 + 1 = 2`。  
> - 查询 `= 19`：没有区间包含 `19`，答案为 `-1`。  
> - 查询 `= 5`：区间 `[2,5]` 是包含 `5` 的最小区间，答案为 `5 - 2 + 1 = 4`。  
> - 查询 `= 22`：区间 `[20,25]` 是唯一包含 `22` 的区间，答案为 `25 - 20 + 1 = 6`。

---

### 约束条件

- `1 ≤ intervals.length ≤ 10^5`
- `1 ≤ queries.length ≤ 10^5`
- `intervals[i].length == 2`
- `1 ≤ left_i ≤ right_i ≤ 10^7`
- `1 ≤ queries[j] ≤ 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个查询 `q`，遍历所有区间 `intervals`，找出既包含 `q` 又最短的那个**。

- **遍历**：就像在超市里逐个检查每件商品是否符合你的需求——虽然慢，但一定能找到答案。  
- **判断是否包含**：区间 `[l, r]` 包含查询 `q` 的条件是 `l ≤ q ≤ r`。  
- **计算区间大小**：大小 = `r - l + 1`（因为左右端点都算在内）。  
- **记录最小值**：在遍历的过程中维护一个变量 `best`，如果当前区间满足条件且大小更小，就把 `best` 更新为它的大小。遍历完后，如果 `best` 仍是初始的“无限大”，说明没有任何区间包含该查询，答案就是 `-1`。

> **为什么这个方法一定正确？**  
> 因为我们把所有可能的区间都检查了一遍，最小的满足条件的区间必然会被找到。

#### 代码（Python）

```python
from typing import List

def minInterval_bruteforce(intervals: List[List[int]], queries: List[int]) -> List[int]:
    ans = []                       # 用来保存每个查询的答案
    for q in queries:              # 逐个处理查询
        best = float('inf')        # 先把最小大小设为无限大
        for l, r in intervals:     # 检查所有区间
            if l <= q <= r:        # 判断区间是否覆盖查询
                size = r - l + 1   # 计算区间大小
                if size < best:   # 找到更小的就更新
                    best = size
        # 遍历完后，若 best 仍是无限大，说明没有覆盖区间
        ans.append(best if best != float('inf') else -1)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N * Q)`（`N` 为区间数，`Q` 为查询数）。  
  大白话：如果区间有 10 万个，查询也有 10 万个，程序需要执行 10 万 × 10 万 = 1 亿元次判断，显然会超时。  
- **空间复杂度**：`O(1)`（不计答案数组本身，只用了常数级的临时变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个查询都要遍历全部区间**。如果我们能让区间**按需进入**、**按需退出**，就可以把每个区间只处理一次。

关键观察：

1. **如果把查询从小到大排序**，那么随着查询值的增大，**已经不可能再包含当前查询的区间也一定不会再包含后面的查询**。  
   > 类比：在电影院排队买票，排在前面的观众离开后，后面的观众不需要再检查前面已经离开的那个人。

2. **把区间也按左端点 `left` 从小到大排序**，当我们处理某个查询 `q` 时，只需要把所有左端点 `≤ q` 的区间“加入”当前的候选集合中。

3. **在候选集合里我们只关心最小的区间大小**。于是可以使用**最小堆（priority queue）**来维护这些候选区间，堆顶始终是当前最小的区间。  
   - 堆中存 `(size, right)`，`size` 用来比较大小，`right` 用来在后面判断该区间是否已经失效（`right < q`）。

4. **离开候选集合**：当查询值 `q` 超过某个区间的右端点 `right` 时，这个区间再也不可能包含后面的查询，需要从堆中弹出。因为堆是按照 `size` 排序的，直接弹出不一定是失效的最小区间，所以我们在每次取堆顶前，循环弹出所有 `right < q` 的区间。

实现步骤：

| 步骤 | 说明 |
|------|------|
|① 对 `queries` 记录原始下标并按值升序排序 | 方便最后把答案恢复到原来的顺序 |
|② 对 `intervals` 按左端点 `left` 升序排序 | 方便“从左到右”依次加入候选集合 |
|③ 初始化一个空的最小堆 `heap`，指针 `i = 0` 指向下一个待加入的区间 | `i` 用来遍历已排序的 `intervals` |
|④ 遍历排好序的查询 `q`（从小到大）<br> a. 把所有 `left ≤ q` 的区间加入堆（`size = r - l + 1`）<br> b. 弹出堆顶中所有已经失效的区间（`right < q`）<br> c. 堆不空 → 堆顶的 `size` 即为答案；堆空 → `-1` | 这样每个区间只会被 **加入一次**、**弹出一次**，整体线性遍历 |
|⑤ 把答案写回到原始下标对应的位置 | 完成所有查询的答案数组 |

#### 代码（Python）

```python
import heapq
from typing import List

def minInterval(intervals: List[List[int]], queries: List[int]) -> List[int]:
    # 1. 把查询保存原始下标并排序
    sorted_queries = sorted([(q, idx) for idx, q in enumerate(queries)], key=lambda x: x[0])

    # 2. 把区间按左端点排序
    intervals.sort(key=lambda x: x[0])

    heap = []                # 最小堆，元素为 (size, right)
    i = 0                    # 指向下一个未加入堆的区间
    n = len(intervals)
    ans = [-1] * len(queries)   # 预先分配答案数组

    for q, idx in sorted_queries:          # 按查询值从小到大遍历
        # a. 把所有 left <= q 的区间加入堆
        while i < n and intervals[i][0] <= q:
            l, r = intervals[i]
            size = r - l + 1
            heapq.heappush(heap, (size, r))   # 按 size 排序，右端点用于后续失效判断
            i += 1

        # b. 弹出已经失效（right < q）的区间
        while heap and heap[0][1] < q:        # 堆顶的 right 小于当前查询，说明不再覆盖
            heapq.heappop(heap)

        # c. 记录答案
        if heap:
            ans[idx] = heap[0][0]            # 堆顶的 size 就是最小区间大小
        else:
            ans[idx] = -1                     # 没有任何区间覆盖当前查询

    return ans
```

> **代码要点解释**  
> - `heapq.heappush(heap, (size, r))`：把区间的大小 `size` 作为堆的主键，右端点 `r` 作为辅助信息。这样堆顶永远是当前最小的区间。  
> - `while heap and heap[0][1] < q:`：只要堆顶的右端点已经小于查询值，就把它弹出，因为它永远不可能再覆盖后面的查询。  
> - `sorted_queries` 中的 `(q, idx)` 让我们在遍历完后还能把答案放回原来的位置。

#### 复杂度  

- **时间复杂度**：`O((N + Q) log N)`  
  - 区间和查询各自排序各需 `O(N log N)`、`O(Q log Q)`。  
  - 主循环中每个区间只 **加入一次**、**弹出一次**，每次堆操作是 `log N`，所以整体是 `O((N+Q) log N)`。  
  - 与暴力解相比，省掉了 `N*Q` 的巨量乘法，真正能在 `10⁵` 规模下跑完。

- **空间复杂度**：`O(N + Q)`  
  - 需要保存排序后的查询数组（`O(Q)`）和最小堆（最坏情况下可能装下所有区间，`O(N)`），以及答案数组。  
  - 相比于只用常数空间，这里多用了线性空间，但在题目限制下完全可接受。

---

## 心得

- **核心技巧**：**排序 + 扫描线（线段扫描） + 最小堆**。先把事件（区间左端、查询点）按坐标排好序，然后随坐标前进动态维护“当前活跃的区间”，堆帮助我们快速得到最小区间大小。  
- **适用的题型**  
  1. “给定若干区间，查询点落在哪个区间里” 类似题目（如 LeetCode 1850）。  
  2. “在平面上求某一点最近的矩形/线段” 这类需要**动态维护最优解**的几何问题。  
- **一句话总结解题钥匙**：*把查询和区间都排好序，用扫描线把区间“打开/关闭”，最小堆随时提供当前最小的有效区间*。

---

## 反思

- **第一反应**：直接想到遍历所有区间，最自然的暴力实现。  
- **最容易踩的坑**  
  1. **忘记弹出已经失效的区间**，导致堆顶仍是一个不包含当前查询的区间，答案错误。  
  2. **没有记录查询的原始下标**，导致输出顺序与输入不一致。  
  3. **堆中只存大小**而不存右端点，弹不出失效区间，必须把 `right` 也一起保存。  
- **下次遇到同类题**：第一步先**对所有“事件”排序**（区间左端、查询点），再思考在扫描过程中如何**增删**状态集合，常用的数据结构是**堆**或**有序集合**。这样可以把“每次遍历全部” 的 `O(N*Q)` 降到 `O((N+Q) log N)`。