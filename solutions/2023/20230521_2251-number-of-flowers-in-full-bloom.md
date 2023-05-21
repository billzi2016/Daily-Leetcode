# #2251. **全盛花朵的数量** / Number of Flowers in Full Bloom

> 难度：困难 · 标签：Array、Hash Table、Binary Search、Sorting、Prefix Sum、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/number-of-flowers-in-full-bloom/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array flowers, where flowers[i] = [starti, endi] means the ith flower will be in full bloom from starti to endi (inclusive). You are also given a 0-indexed integer array people of size n, where people[i] is the time that the ith person will arrive to see the flowers.
Return an integer array answer of size n, where answer[i] is the number of flowers that are in full bloom when the ith person arrives.

**Examples**

**Example 1:**

```
Input: flowers = [[1,6],[3,7],[9,12],[4,13]], people = [2,3,7,11]
Output: [1,2,2,2]
Explanation: The figure above shows the times when the flowers are in full bloom and when the people arrive.
For each person, we return the number of flowers in full bloom during their arrival.
```

**Example 2:**

```
Input: flowers = [[1,10],[3,3]], people = [3,3,2]
Output: [2,2,1]
Explanation: The figure above shows the times when the flowers are in full bloom and when the people arrive.
For each person, we return the number of flowers in full bloom during their arrival.
```

**Constraints**

- 1 <= flowers.length <= 5 * 104
- flowers[i].length == 2
- 1 <= starti <= endi <= 109
- 1 <= people.length <= 5 * 104
- 1 <= people[i] <= 109

---

## 题目（中文翻译）

你得到一个下标从 0 开始的二维整数数组（2D integer array）`flowers`，其中 `flowers[i] = [starti, endi]` 表示第 `i` 株花从 `starti` 到 `endi`（两端均包含）处于全盛期（full bloom）。同时，你还有一个下标从 0 开始的整数数组（integer array）`people`，长度为 `n`，其中 `people[i]` 为第 `i` 个人到达观赏花朵的时间。

返回一个长度为 `n` 的整数数组 `answer`，其中 `answer[i]` 表示第 `i` 个人到达时正处于全盛期的花的数量。

**示例 1**

```text
Input: flowers = [[1,6],[3,7],[9,12],[4,13]], people = [2,3,7,11]
Output: [1,2,2,2]
Explanation: 上图展示了各花株的全盛时间区间以及人们的到达时间。对每个人，返回其到达时正处于全盛期的花的数量。
```

**示例 2**

```text
Input: flowers = [[1,10],[3,3]], people = [3,3,2]
Output: [2,2,1]
Explanation: 上图展示了各花株的全盛时间区间以及人们的到达时间。对每个人，返回其到达时正处于全盛期的花的数量。
```

**约束条件**

- `1 <= flowers.length <= 5 * 10^4`
- `flowers[i].length == 2`
- `1 <= starti <= endi <= 10^9`
- `1 <= people.length <= 5 * 10^4`
- `1 <= people[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个人，逐个检查所有花的区间**，看该时间是否落在 `[start, end]` 之间。如果在，就计数 +1，最后得到该人的答案。

- **使用的数据结构**：  
  - `flowers` 是一个二维列表，存放每朵花的 `[开始时间, 结束时间]`。可以把它想象成一张“花开时间表”。  
  - `people` 是一个一维列表，存放每个人到达的时间。可以把它看成“观花时间点”。  

- **为什么正确**：  
  对每个时间点 `t`，我们检查所有花的区间是否包含 `t`，如果包含说明此时这朵花正盛开。把所有满足条件的花加起来，就是答案。

- **复杂度分析（大白话）**：  
  - 外层遍历 `people`，假设有 `m` 个人。  
  - 内层遍历 `flowers`，假设有 `n` 朵花。  
  - 每一次检查只需要常数时间（比较两个整数），所以总共要做 `m × n` 次比较。  
  - 用大 O 表示就是 **O(m·n)**，如果 `m`、`n` 都是 5×10⁴，乘积会达到 2.5×10⁹，计算机根本跑不完。  
  - 额外空间只用了答案数组 `answer`，大小为 `m`，即 **O(m)**。

#### 代码（Python）

```python
from typing import List

def fullBloomFlowers_bruteforce(flowers: List[List[int]], people: List[int]) -> List[int]:
    """
    暴力解法：对每个人检查所有花的区间是否包含该时间
    """
    m = len(people)
    answer = [0] * m                # 最终答案，长度等于人数

    # 对每个人的到达时间 t
    for i, t in enumerate(people):
        cnt = 0                      # 统计此时盛开的花的数量
        # 检查每一朵花的 [start, end] 是否包含 t
        for start, end in flowers:
            if start <= t <= end:   # 如果 t 落在区间内
                cnt += 1
        answer[i] = cnt              # 把计数写进答案

    return answer
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 这里的 `m` 是 `people` 的长度，`n` 是 `flowers` 的长度。意思是“每个人都要遍历所有花”，所以运算次数会随两者的乘积线性增长。
- **空间复杂度**：`O(m)`  
  - 只用了一个大小为 `people` 长度的答案数组，除此之外没有额外的显著空间开销。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有花**。我们需要一种方法，**快速得到**：  

1. **已经开花的花的数量**（即开始时间 ≤ t）。  
2. **已经凋谢的花的数量**（即结束时间 < t）。  

因为在时间 `t` 正在盛开的花数 = “已经开花的花数” – “已经凋谢的花数”。  

**关键观察**：  
- 所有花的开始时间和结束时间是**可以独立排序**的。  
- 排序后，我们可以使用**二分查找**（binary search）在 `O(log n)` 时间内，统计 ≤ t（或 < t）的元素个数。  
- 对每个查询时间 `t`，只需要两次二分查找，就能得到答案。

**一步步推导**：

1. 把所有 `start` 收集到列表 `starts`，所有 `end` 收集到列表 `ends`。  
2. 对 `starts`、`ends` 各自**升序排序**。排序一次的代价是 `O(n log n)`，但只做一次。  
3. 对每个 `people[i] = t`：  
   - 使用 `bisect_right(starts, t)`，得到 **≤ t** 的开始时间个数。`bisect_right` 相当于在排好序的字典里查“页码”，返回“最后一个不大于 t 的位置”。  
   - 使用 `bisect_left(ends, t)`，得到 **< t** 的结束时间个数。`bisect_left` 相当于查“第一个不小于 t 的位置”。  
   - 两者相减即为此时盛开的花数。  

**类比**：  
- 想象你有两本排好序的“时间册”：一本记录每朵花的“开花页码”，另一本记录每朵花的“凋谢页码”。要知道某一天有多少花在盛开，只要看这两本册子里，分别有多少页码在这天之前/之前（不包括），相减就得到答案。

#### 代码（Python）

```python
from bisect import bisect_left, bisect_right
from typing import List

def fullBloomFlowers_optimal(flowers: List[List[int]], people: List[int]) -> List[int]:
    """
    最优解：利用排序 + 二分查找
    思路：
    1. 把所有 start 收集到 starts，所有 end 收集到 ends；
    2. 对 starts、ends 各自排序；
    3. 对每个查询时间 t：
         已开花数量 = bisect_right(starts, t)   # ≤ t
         已凋谢数量 = bisect_left(ends, t)      # < t
         正在盛开的花 = 已开花数量 - 已凋谢数量
    """
    # 1. 拆分 start 与 end
    starts = [s for s, _ in flowers]
    ends   = [e for _, e in flowers]

    # 2. 排序（一次性完成）
    starts.sort()      # 小到大排好序的开花时间
    ends.sort()        # 小到大排好序的凋谢时间

    # 3. 对每个人的到达时间进行二分查询
    answer = []
    for t in people:
        # 已经开花的花的数量（包括在 t 时刻开放的花）
        opened = bisect_right(starts, t)   # 找到最右侧的 ≤ t 的位置，返回计数

        # 已经凋谢的花的数量（不包括在 t 时刻凋谢的花，因为结束时间是 inclusive）
        closed = bisect_left(ends, t)      # 找到最左侧的 ≥ t 的位置，返回 < t 的计数

        answer.append(opened - closed)     # 正在盛开的花数

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n log n + m log n)`  
  - `n` 为花的数量，`m` 为查询人数。  
  - 排序 `starts`、`ends` 各自需要 `O(n log n)`（把时间册排好序）。  
  - 对每个查询时间进行两次二分查找，每次 `O(log n)`，共 `m` 次，所以 `O(m log n)`。  
  - 与暴力解相比，时间从 `O(m·n)` 降到了 “对数级” 的 `O(m log n)`，即使 `n、m` 都是 5×10⁴ 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 额外存储了两个长度为 `n` 的列表 `starts`、`ends`，相当于复制了一遍花的时间信息。  
  - 答案数组 `answer` 长度为 `m`，但这属于输出必需空间，不计入额外复杂度。

---

## 心得

- **核心技巧**：把“区间包含关系”转化为 “前缀计数”——即 **已开始的数量 - 已结束的数量**。  
- **适用的题型**（类似技巧）：
  1. **“查询某时刻有多少活动进行中”**（如会议室使用情况、火车站客流等）。  
  2. **“区间覆盖次数”**（如画线段覆盖问题、区间加法的差分数组）。  
  3. **“区间求和或区间最大值”**（利用前缀和或线段树的思路）。  
- **一句话总结解题钥匙**：**把所有起点、终点分别排序，用二分快速统计“之前有多少起点/终点”，相减即得答案**。

---

## 反思

- **拿到题目第一反应**：直接遍历每个人的时间点去检查所有花的区间，想到用两个循环实现。  
- **最容易踩的坑**：  
  - 结束时间是 **闭区间**（inclusive），所以在统计已经凋谢的花时，需要使用 `bisect_left`（统计 `< t`），而不是 `bisect_right`（统计 `≤ t`），否则会把在同一时刻凋谢的花算进去，导致答案偏小。  
  - 忽视了时间范围可能高达 `10⁹`，不能直接用数组下标做差分，需要用排序+二分的方式。  
- **下次遇到同类题**：第一步先**把所有关键点（起点、终点、查询点）抽出来，思考是否可以**排序后利用二分或前缀计数**来快速求解，而不是盲目遍历。这样往往能把暴力的 `O(m·n)` 降到 `O((m+n) log n)`。