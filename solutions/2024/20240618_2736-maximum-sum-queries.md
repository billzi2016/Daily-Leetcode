# #2736. 最大和查询 / Maximum Sum Queries

> 难度：困难 · 标签：Array、Binary Search、Stack、Binary Indexed Tree、Segment Tree、Sorting、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-queries/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2, each of length n, and a 1-indexed 2D array queries where queries[i] = [xi, yi].
For the ith query, find the maximum value of nums1[j] + nums2[j] among all indices j (0 <= j < n), where nums1[j] >= xi and nums2[j] >= yi, or -1 if there is no j satisfying the constraints.
Return an array answer where answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: nums1 = [4,3,1,2], nums2 = [2,4,9,5], queries = [[4,1],[1,3],[2,5]]
Output: [6,10,7]
Explanation: 
For the 1st query xi = 4 and yi = 1, we can select index j = 0 since nums1[j] >= 4 and nums2[j] >= 1. The sum nums1[j] + nums2[j] is 6, and we can show that 6 is the maximum we can obtain.

For the 2nd query xi = 1 and yi = 3, we can select index j = 2 since nums1[j] >= 1 and nums2[j] >= 3. The sum nums1[j] + nums2[j] is 10, and we can show that 10 is the maximum we can obtain. 

For the 3rd query xi = 2 and yi = 5, we can select index j = 3 since nums1[j] >= 2 and nums2[j] >= 5. The sum nums1[j] + nums2[j] is 7, and we can show that 7 is the maximum we can obtain.

Therefore, we return [6,10,7].
```

**Example 2:**

```
Input: nums1 = [3,2,5], nums2 = [2,3,4], queries = [[4,4],[3,2],[1,1]]
Output: [9,9,9]
Explanation: For this example, we can use index j = 2 for all the queries since it satisfies the constraints for each query.
```

**Example 3:**

```
Input: nums1 = [2,1], nums2 = [2,3], queries = [[3,3]]
Output: [-1]
Explanation: There is one query in this example with xi = 3 and yi = 3. For every index, j, either nums1[j] < xi or nums2[j] < yi. Hence, there is no solution.
```

**Constraints**

- nums1.length == nums2.length
- n == nums1.length
- 1 <= n <= 105
- 1 <= nums1[i], nums2[i] <= 109
- 1 <= queries.length <= 105
- queries[i].length == 2
- xi == queries[i][1]
- yi == queries[i][2]
- 1 <= xi, yi <= 109

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的整数数组（integer array）`nums1` 和 `nums2`，它们的长度均为 `n`。同时给定一个下标从 **1** 开始的二维数组（2D array）`queries`，其中 `queries[i] = [xi, yi]`。  

对于第 `i` 个查询（query），在满足 `nums1[j] >= xi` 且 `nums2[j] >= yi` 的所有下标 `j`（`0 <= j < n`）中，找到 `nums1[j] + nums2[j]` 的最大值；如果不存在满足条件的下标 `j`，则返回 `-1`。  

返回一个数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的答案。  

---  

## 示例  

### 示例 1  
**输入**  
```
nums1 = [4,3,1,2], nums2 = [2,4,9,5], queries = [[4,1],[1,3],[2,5]]
```  

**输出**  
```
[6,10,7]
```  

**解释**  
- 第 1 个查询 `xi = 4` 且 `yi = 1`，我们可以选择下标 `j = 0`，因为 `nums1[0] >= 4` 且 `nums2[0] >= 1`。此时和 `nums1[0] + nums2[0] = 6`，且可以证明 6 是能够取得的最大值。  
- 第 2 个查询 `xi = 1` 且 `yi = 3`，我们可以选择下标 `j = 2`，因为 `nums1[2] >= 1` 且 `nums2[2] >= 3`。此时和为 `1 + 9 = 10`，这是所有满足条件的下标中最大的。  
- 第 3 个查询 `xi = 2` 且 `yi = 5`，我们可以选择下标 `j = 3`，因为 `nums1[3] >= 2` 且 `nums2[3] >= 5`。此时和为 `2 + 5 = 7`，为最大可能值。  

### 示例 2  
**输入**  
```
nums1 = [3,2,5], nums2 = [2,3,4], queries = [[4,4],[3,2],[1,1]]
```  

**输出**  
```
[9,9,9]
```  

**解释**  
对于所有查询，都可以使用下标 `j = 2`，因为它满足每个查询的约束条件。`nums1[2] + nums2[2] = 5 + 4 = 9`，因此每个查询的答案都是 9。  

### 示例 3  
**输入**  
```
nums1 = [2,1], nums2 = [2,3], queries = [[3,3]]
```  

**输出**  
```
[-1]
```  

**解释**  
唯一的查询 `xi = 3`、`yi = 3`。对于任意下标 `j`，要么 `nums1[j] < 3`，要么 `nums2[j] < 3`，因此不存在满足条件的下标，答案为 `-1`。  

---  

## 约束条件  

- `nums1.length == nums2.length`  
- `n == nums1.length`  
- `1 <= n <= 10^5`  
- `1 <= nums1[i], nums2[i] <= 10^9`  
- `1 <= queries.length <= 10^5`  
- `queries[i].length == 2`  
- `xi == queries[i][0]`  
- `yi == queries[i][1]`  
- `1 <= xi, yi <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每个查询都 **遍历所有下标**，检查下标 `j` 是否同时满足  

```
nums1[j] >= xi   且   nums2[j] >= yi
```

如果满足，就计算 `nums1[j] + nums2[j]`，把最大的那个记下来；如果整个数组都没有满足条件的下标，就返回 `-1`。

> **数据结构类比**  
> - 这里我们只用到了 **普通的数组**，相当于在超市里把所有商品都逐个检查一遍，看看有没有符合 “重量 ≥ xi 且 体积 ≥ yi” 这两个条件的商品。  

> **为什么能得到正确答案**  
> 因为我们没有漏掉任何下标，所有可能的 `j` 都被检查到了，取最大自然就是答案。

#### 代码（Python）

```python
from typing import List

def maximumSumQueries_bruteforce(nums1: List[int], nums2: List[int],
                                queries: List[List[int]]) -> List[int]:
    n = len(nums1)
    ans = []
    for xi, yi in queries:                     # 对每个查询
        best = -1                               # 先假设没有满足的下标
        for j in range(n):                     # 暴力遍历所有下标
            if nums1[j] >= xi and nums2[j] >= yi:   # 同时满足两个阈值
                s = nums1[j] + nums2[j]              # 计算和
                if s > best:                         # 维护最大值
                    best = s
        ans.append(best)                        # 记录本次查询的答案
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * q)`  
  - `n` 是数组长度，`q` 是查询数量。可以把它想象成 “把 10⁵ 件商品都检查 10⁵ 次”，显然会非常慢（约 10¹⁰ 次操作）。
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每个查询都遍历全部下标**。我们需要把“遍历所有下标”这件事 **提前一次性完成**，让每个查询只做 **对数时间** 的查找。

下面一步步推导出一种 **离线 + 单调映射** 的做法（即 **单调栈/单调映射** + **二分查找**）：

1. **把所有下标看成点** `(x = nums1[j], y = nums2[j])`，并记它们的 “价值” `v = x + y`。  
2. 对查询 `(xi, yi)`，我们要求的是 **所有点中** `x ≥ xi 且 y ≥ yi` 的最大 `v`。  
3. 把所有点 **按照 x 从大到小排序**，把查询也 **按照 xi 从大到小排序**。  
   - 这样，当我们处理一个查询 `(xi, yi)` 时，**已经把所有 x ≥ xi 的点加入了数据结构**，只需要在这些点里找满足 `y ≥ yi` 的最大 `v`。  
4. 需要一种能 **快速插入点的 y 与 v**，并且 **在查询时能够在 y ≥ yi 的范围内得到最大 v** 的结构。  
   - 观察：如果我们把点按照 **y 升序** 保存，并且保证 **对应的 v 是严格递减**（即 y 越大，v 越小），那么 **第一个满足 y ≥ yi 的点** 就一定拥有最大的 v。  
   - 这正好是 **单调递减映射**（monotone map）的特性。我们可以用两个平行的列表 `ys`（保存 y）和 `vals`（保存对应的最大 v）来实现。  
5. **插入新点 `(y, v)` 的规则**  
   - 先在 `ys` 中二分找到插入位置 `pos`。  
   - 如果已有相同的 y，保留更大的 v。  
   - 插入后，**向左**删除所有 `y` 更小但 `v` 不大于当前 `v` 的点（因为它们被新点支配）；  
   - **向右**删除所有 `y` 更大但 `v` 也不大于当前 `v` 的点（同理）。这样保持 `ys` 递增、`vals` 递减。  
6. **查询**  
   - 对于 `(xi, yi)`，二分在 `ys` 中找到 **第一个 ≥ yi** 的位置 `idx`。  
   - 如果 `idx` 越界，则说明没有满足 `y ≥ yi` 的点，答案 `-1`；否则答案就是 `vals[idx]`（已经是最大 v）。  

> **类比**  
> 想象我们在一个 **图书馆** 按照 **出版年份（y）** 排书，书的 **价值（v）** 随年份递减。读者只关心 **“出版年份不少于 yi”** 的书，直接拿到最左边那本（年份最早但仍 ≥ yi）就能得到最高价值的书。

> **为什么正确**  
> - 由于我们是 **离线**（先排序后统一处理），在处理查询时 **所有满足 x 条件的点已经全部加入**。  
> - 单调映射保证了 “更大的 y 对应的 v 更小”，所以在满足 `y ≥ yi` 的集合里，**最左边的点拥有最大的 v**，查询只需一次二分。  

#### 代码（Python）

```python
from bisect import bisect_left, bisect_right
from typing import List

def maximumSumQueries(nums1: List[int], nums2: List[int],
                      queries: List[List[int]]) -> List[int]:
    n = len(nums1)

    # 1. 把所有点 (x, y, x+y) 按 x 降序排列
    points = sorted(((nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)),
                    key=lambda t: -t[0])          # -t[0] → 降序

    # 2. 把查询也按 xi 降序排列，同时记下原始下标方便恢复顺序
    indexed_queries = [(xi, yi, idx) for idx, (xi, yi) in enumerate(queries)]
    indexed_queries.sort(key=lambda q: -q[0])          # 按 xi 降序

    # 3. 单调映射：两个平行列表，ys 递增，vals 递减
    ys: List[int] = []      # 已插入点的 y（升序）
    vals: List[int] = []    # 对应的最大 (x+y)，满足 vals 随 ys 增大而严格递减

    ans = [-1] * len(queries)
    p = 0   # points 的指针

    for xi, yi, qidx in indexed_queries:
        # ① 把所有 x >= xi 的点加入单调映射
        while p < n and points[p][0] >= xi:
            _, y, v = points[p]
            # 在 ys 中二分找到插入位置
            pos = bisect_left(ys, y)

            # 处理相同 y 的情况：保留更大的 v
            if pos < len(ys) and ys[pos] == y:
                if v > vals[pos]:
                    vals[pos] = v
                else:
                    # 当前 v 不比已有的大，直接跳过插入
                    p += 1
                    continue
            else:
                # 插入新 (y, v)
                ys.insert(pos, y)
                vals.insert(pos, v)

            # 向左删除被当前点支配的点（y 更小且 v 不大于当前 v）
            i = pos - 1
            while i >= 0 and vals[i] <= v:
                del ys[i]
                del vals[i]
                i -= 1
                pos -= 1          # 删除后当前位置左移

            # 向右删除被当前点支配的点（y 更大且 v 不大于当前 v）
            i = pos + 1
            while i < len(ys) and vals[i] <= v:
                del ys[i]
                del vals[i]
                # i 不变，因为删除后下一个元素会“移到”当前位置

            p += 1

        # ② 在已构建的单调映射中查询 y >= yi 的最大 v
        idx = bisect_left(ys, yi)
        if idx < len(ys):
            ans[qidx] = vals[idx]          # 第一个满足 y >= yi 的点即为最大 v
        else:
            ans[qidx] = -1                  # 没有满足 y 条件的点

    return ans
```

> **代码要点说明**  
> - `points` 按 `x` 降序确保在处理查询 `(xi, yi)` 前，所有 `x >= xi` 的点已经“加入”。  
> - `ys` 与 `vals` 同时保持 **单调递减**（`vals` 随 `ys` 增大而严格递减），这样二分一次即可得到答案。  
> - 插入时的左右删点保证了映射的单调性，防止出现 “更大的 y 但更大的 v”，否则二分找不到最大值。  

#### 复杂度  

- **时间复杂度**：`O((n + q) log n)`  
  - 对每个点和每个查询各做一次二分（`log n`），其余操作是常数级。相比暴力的 `O(n·q)`，把 10⁵×10⁵ 的巨量运算压到约 `2·10⁵·log(10⁵)`（≈ 3·10⁶）次，足够快。  
- **空间复杂度**：`O(n)`（单调映射最坏保存所有点）  
  - 只需要额外的两个列表 `ys`、`vals`，以及排序后的临时数组。

---

## 心得

- **核心技巧**：离线处理 + 单调映射（Monotone Map）+ 二分查找。  
- **适用场景**  
  1. “在二维平面上，查询满足 `x ≥ X` 且 `y ≥ Y` 的最大（或最小）某个值”。  
  2. “先按一个维度排序、扫过去，同时维护另一个维度的单调结构”。  
  3. 类似的 LeetCode 题目如 **“Maximum Width of a Ramp”**、**“Maximum XOR With an Element From Array”**（使用单调栈/映射）等。  
- **一句话总结**：把“所有满足第一个条件的点”一次性加入单调递减映射，查询只需二分一次即可得到答案。

---

## 反思

- **拿到题目第一反应**：直接遍历所有下标，写出暴力解，验证思路。  
- **最容易踩的坑**  
  - **边界条件**：查询的 `yi` 可能比所有已插入的 `y` 都大，此时需要返回 `-1`。  
  - **单调映射的维护**：插入时忘记同时删除左侧和右侧被支配的点，会导致 `vals` 不再递减，二分后得到的并非最大值。  
  - **排序的方向**：一定要把 `x`（或 `xi`）降序排列，否则在处理查询时会遗漏一些满足 `x ≥ xi` 的点。  
- **下次遇到同类题的第一步**：**先把所有元素/查询按一个约束的阈值排序**，再思考用什么单调/堆结构在遍历过程中维护另一个约束的最优值。这样可以把 “双重筛选” 转化为 “一次遍历 + 对数查询”。