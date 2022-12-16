# #2054. 两个最佳不重叠事件 / Two Best Non-Overlapping Events

> 难度：中等 · 标签：Array、Binary Search、Dynamic Programming、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/two-best-non-overlapping-events/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array of events where events[i] = [startTimei, endTimei, valuei]. The ith event starts at startTimei and ends at endTimei, and if you attend this event, you will receive a value of valuei. You can choose at most two non-overlapping events to attend such that the sum of their values is maximized.
Return this maximum sum.
Note that the start time and end time is inclusive: that is, you cannot attend two events where one of them starts and the other ends at the same time. More specifically, if you attend an event with end time t, the next event must start at or after t + 1.

**Examples**

**Example 1:**

```
Input: events = [[1,3,2],[4,5,2],[2,4,3]]
Output: 4
Explanation: Choose the green events, 0 and 1 for a sum of 2 + 2 = 4.
```

**Example 2:**

```
Input: events = [[1,3,2],[4,5,2],[1,5,5]]
Output: 5
Explanation: Choose event 2 for a sum of 5.
```

**Example 3:**

```
Input: events = [[1,5,3],[1,5,1],[6,6,5]]
Output: 8
Explanation: Choose events 0 and 2 for a sum of 3 + 5 = 8.
```

**Constraints**

- 2 <= events.length <= 105
- events[i].length == 3
- 1 <= startTimei <= endTimei <= 109
- 1 <= valuei <= 106

---

## 题目（中文翻译）

你得到一个 **0 索引** 的二维整数数组（2D integer array）`events`，其中 `events[i] = [startTimeᵢ, endTimeᵢ, valueᵢ]`。第 `i` 场事件在 `startTimeᵢ` 开始，`endTimeᵢ` 结束，如果参加该事件，你将获得 `valueᵢ` 的价值。你最多可以选择 **两场** 非重叠（non-overlapping）事件参加，使它们的价值之和最大。返回这个最大和。

> 注意：开始时间和结束时间均为 **闭区间**，即不能选择两场事件，使其中一场的开始时间恰好等于另一场的结束时间。更具体地说，如果你参加了一场结束时间为 `t` 的事件，那么下一场事件的开始时间必须 **≥ t + 1**。

### 示例

#### 示例 1
```
Input: events = [[1,3,2],[4,5,2],[2,4,3]]
Output: 4
Explanation: 选择第 0 场和第 1 场事件，价值和为 2 + 2 = 4。
```

#### 示例 2
```
Input: events = [[1,3,2],[4,5,2],[1,5,5]]
Output: 5
Explanation: 只参加第 2 场事件，价值为 5。
```

#### 示例 3
```
Input: events = [[1,5,3],[1,5,1],[6,6,5]]
Output: 8
Explanation: 选择第 0 场和第 2 场事件，价值和为 3 + 5 = 8。
```

### 约束条件
- `2 <= events.length <= 10⁵`
- `events[i].length == 3`
- `1 <= startTimeᵢ <= endTimeᵢ <= 10⁹`
- `1 <= valueᵢ <= 10⁶`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的两场活动组合**，然后挑出不冲突且价值和最大的那对。  

- **枚举**：把每个活动当成第一个选的活动 `i`，再把后面的每个活动 `j`（`j ≠ i`）当成第二个选的活动。  
- **判断是否冲突**：如果 `events[i][1]`（第 `i` 场的结束时间）小于 `events[j][0]`（第 `j` 场的开始时间）**且**两者之间没有交叉（结束时间 +1 ≤ 开始时间），则这两场可以一起参加。  
- **记录最大值**：把所有合法组合的价值和算出来，取最大。

> **类比**：把活动想成图书馆的借书时间段，两个借书时间如果有交叉就不能同时借。暴力法就是把所有可能的两本书配对，看看哪些配对不冲突。

这个方法一定能得到正确答案，因为它遍历了**所有**合法的两场组合。

#### 代码（Python）

```python
from typing import List

def maxTwoEvents_brute(events: List[List[int]]) -> int:
    n = len(events)
    ans = 0

    # 暴力枚举两场活动的下标 i, j
    for i in range(n):
        start_i, end_i, val_i = events[i]
        # 只算单场情况（只参加一场也算合法）
        ans = max(ans, val_i)

        for j in range(i + 1, n):
            start_j, end_j, val_j = events[j]

            # 判断两场是否不重叠（结束时间必须严格小于另一场的开始时间）
            if end_i < start_j or end_j < start_i:
                # 两种顺序都可以，取价值大的顺序
                total = val_i + val_j
                ans = max(ans, total)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：我们要把每个活动和后面的所有活动配对，配对次数大约是 `n*(n-1)/2`，这在大多数情况下会随着 `n` 的增长而呈二次方增长。把 `O(n²)` 想象成“如果有 10,000 场活动，需要比较约 100,000,000 次”，显然会超时。  
- **空间复杂度**：`O(1)`  
  解释：只用了常数个额外变量（`ans`、`i`、`j` 等），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历**：每次选第一场活动时，都要再遍历所有后面的活动去找不冲突的最大价值。我们可以把“后面所有不冲突的最大价值”提前算好，随后只用 **一次查找** 就能得到答案。

思路分三步：

1. **按结束时间排序**  
   把所有活动按照 `endTime` 从小到大排列。这样在遍历时，当前活动的“左边”都是已经结束的活动，右边是还未结束的活动。  
2. **前缀最大值数组（prefix_max）**  
   `prefix_max[i]` 记录 **截至第 i 场（按结束时间排序）** 能得到的最大单场价值。  
   - `prefix_max[i] = max(prefix_max[i-1], events[i][2])`  
   - 这样在后面查找时，只要知道“最近的、结束时间 ≤ 某个开始时间 - 1 的活动”下标，就能直接得到该区间的最大价值。  
3. **二分查找**  
   对每一场活动 `cur = [s, e, v]`，我们想找 **在它之前**（即结束时间 ≤ `s-1`）价值最高的那场。因为结束时间已经排好序，使用二分搜索可以 **O(log n)** 找到满足条件的最右侧下标 `idx`。  
   - 若找到了 `idx`，则 `candidate = v + prefix_max[idx]`（当前活动 + 之前的最佳单场）  
   - 同时我们还要比较只参加当前活动本身的价值 `v`。  
   - 记录全局最大即可。  

> **类比**：想象你在排队买电影票，排好序的结束时间就像排好顺序的队伍。你只想找 **离你最近且已经看完的电影**，二分查找就像快速定位那个人的位置，而前缀最大值相当于记录到每个人为止的最高票价，这样你不需要再遍历整个队伍。

整个过程的时间复杂度是 `O(n log n)`（排序 + n 次二分），空间复杂度是 `O(n)`（存前缀最大数组）。

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List

def maxTwoEvents(events: List[List[int]]) -> int:
    """
    O(n log n) 解法：
    1. 按结束时间排序
    2. 预处理前缀最大单场价值
    3. 对每个活动，用二分查找找出左侧不冲突的最大价值
    """
    # 1. 按结束时间升序排列
    events.sort(key=lambda x: x[1])          # x[1] 是 endTime

    # 把结束时间单独抽出来，方便二分
    ends = [e[1] for e in events]

    # 2. 前缀最大值数组，prefix_max[i] 表示 [0..i] 区间的最大价值
    prefix_max = [0] * len(events)
    for i, (_, _, val) in enumerate(events):
        if i == 0:
            prefix_max[i] = val
        else:
            prefix_max[i] = max(prefix_max[i - 1], val)

    ans = 0

    # 3. 枚举每一场活动作为「第二场」或「唯一一场」
    for s, e, v in events:
        # 只参加当前这场
        ans = max(ans, v)

        # 在已排好序的 ends 中，找出最大的下标 idx，使得 ends[idx] < s
        # 因为结束时间是 inclusive，下一场必须在 s 之后的第一个时间点开始
        idx = bisect_right(ends, s - 1) - 1   # -1 把位置转成下标

        if idx >= 0:                          # 找到了可以搭配的前一场
            candidate = v + prefix_max[idx]   # 当前价值 + 左侧最大价值
            ans = max(ans, candidate)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`  
  - 枚举 `n` 次，每次二分查找 `O(log n)` → `n·log n`  
  - 合在一起仍是 `O(n log n)`，比 `O(n²)` 快很多。可以把它想象成“即使有 100,000 场活动，只需要大约 1.7 million 次比较”，在实际机器上毫秒级完成。  
- **空间复杂度**：`O(n)`  
  - 需要存 `ends`（结束时间列表）和 `prefix_max`（前缀最大值），长度都是 `n`。这相当于“多用了和原数据一样多的空间”，但仍然是线性级别，完全可以接受。

---

## 心得

- **核心技巧**：先把活动按结束时间排序 → 用前缀最大值记录左侧最佳单场价值 → 二分查找快速定位不冲突的左侧活动。  
- **适用的题型**  
  1. “最多选 k 场不冲突活动，价值最大”——可以把 DP 扩展到 `k` 层。  
  2. “在区间集合中找两两不相交且价值和最大的两条”——同样使用排序 + 前缀/后缀最大。  
  3. “给定若干区间，求不相交子集的最大权和（最多 m 条）”——典型的**加权区间调度**问题。  
- **一句话总结**：**“排序 + 前缀最大 + 二分”** 是解决 “选不重叠区间的最大价值” 系列题目的钥匙。

---

## 反思

- **第一反应**：看到“最多两场不重叠”，自然想到枚举组合（暴力），因为两的上限让人觉得可以直接遍历。  
- **最容易踩的坑**  
  - **时间冲突判断**：结束时间是 **inclusive**，所以下一场必须在 `end + 1` 才能参加，二分时要用 `s - 1` 而不是 `s`。  
  - **只选一场的情况**：答案可能只需要一场（如示例 2），记得在遍历时也比较单场价值。  
  - **大数范围**：`startTime`、`endTime` 可达 `10^9`，不能用数组下标直接映射，需要二分或哈希。  
- **下次遇到同类题**：第一步就**把区间按结束时间排序**，然后**思考如何用前缀/后缀信息快速得到左侧或右侧的最佳价值**，最后决定是否需要二分、堆或单调队列等辅助结构。