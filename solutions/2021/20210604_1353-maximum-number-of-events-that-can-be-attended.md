# #1353. 最大可参加的事件数量 / Maximum Number of Events That Can Be Attended

> 难度：中等 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/)

---

## 题目（英文原版）

**Description**

You are given an array of events where events[i] = [startDayi, endDayi]. Every event i starts at startDayi and ends at endDayi.
You can attend an event i at any day d where startDayi <= d <= endDayi. You can only attend one event at any time d.
Return the maximum number of events you can attend.

**Examples**

**Example 1:**

```
Input: events = [[1,2],[2,3],[3,4]]
Output: 3
Explanation: You can attend all the three events.
One way to attend them all is as shown.
Attend the first event on day 1.
Attend the second event on day 2.
Attend the third event on day 3.
```

**Example 2:**

```
Input: events= [[1,2],[2,3],[3,4],[1,2]]
Output: 4
```

**Constraints**

- 1 <= events.length <= 105
- events[i].length == 2
- 1 <= startDayi <= endDayi <= 105

---

## 题目（中文翻译）

给定一个二维数组 `events`，其中 `events[i] = [startDay_i, endDay_i]` 表示第 `i` 场事件的开始天 `startDay_i` 和结束天 `endDay_i`。  
你可以在任意满足 `startDay_i ≤ d ≤ endDay_i` 的天 `d` 参加第 `i` 场事件。**同一时间只能参加一场事件**。  
返回你能够参加的事件的最大数量。

## 示例

### 示例 1
**输入**  
```
events = [[1,2],[2,3],[3,4]]
```
**输出**  
```
3
```
**解释**  
你可以参加全部三场事件。以下是一种可行的安排方式：  
- 第一天参加第一场事件。  
- 第二天参加第二场事件。  
- 第三天参加第三场事件。

### 示例 2
**输入**  
```
events = [[1,2],[2,3],[3,4],[1,2]]
```
**输出**  
```
4
```

## 约束条件
- `1 <= events.length <= 10^5`
- `events[i].length == 2`
- `1 <= startDay_i <= endDay_i <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：把时间线从 **第 1 天** 开始，一天一天往后走。  
- 当来到某一天 `d` 时，查看所有 **还没有参加** 的活动，找出那些 **`start ≤ d ≤ end`** 的活动。  
- 如果找到至少一个，就随便挑一个参加（比如挑第一个），把这天标记为已占用，然后把这场活动从列表中移除。  
- 没有可参加的活动就直接跳到下一天。  

> **类比**：把所有活动想成一本字典，`start`、`end` 就是每个单词的“出现范围”。我们每天只挑一本字典里当前仍在范围内的单词来读，读完后把它从字典里划掉。

这个办法一定能得到一个可行的安排，因为我们始终遵守“一天只能参加一场活动”的规则。只不过它**没有考虑**怎样挑选才会让后面的活动有更多机会。

**为什么正确**：只要我们在每一天都尽量安排一场还能参加的活动，就不会浪费任何一天的空闲时间。只要不违反题目约束，这样的安排一定能得到 **某个** 可参加的活动集合。  

#### 代码（Python）  
```python
from typing import List

def max_events_bruteforce(events: List[List[int]]) -> int:
    # 按照结束时间排序，方便后面挑选
    events = sorted(events, key=lambda x: x[1])
    # 记录每一天是否已经被占用，最大天数不超过 10^5
    max_day = max(e[1] for e in events)
    occupied = [False] * (max_day + 1)          # index 0 不使用
    attended = 0

    for start, end in events:
        # 在活动的时间区间里找第一天没有被占用的日子
        for day in range(start, end + 1):
            if not occupied[day]:
                occupied[day] = True            # 这一天被占用了
                attended += 1
                break                           # 这场活动已经参加，结束内部循环
    return attended
```

#### 复杂度  
- **时间复杂度**：`O(N * D)`，其中 `N` 为活动数量，`D` 为最大天数（最坏情况下每个活动的时间区间都很长，需要遍历整个区间）。如果 `D≈10^5`，在 `N≈10^5` 时会非常慢，等价于 **10^10** 次操作，几乎不可接受。  
- **空间复杂度**：`O(D)` 用来保存每一天是否被占用的布尔数组。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈** 在于每次都要线性遍历活动的全部可选天数。我们需要一种方式，让“在某一天挑最早结束的活动”这一操作变得 **快速**。  

**关键观察**：  
- 当我们决定在第 `d` 天参加哪场活动时，**只要**当天还有活动可选，**优先参加结束时间最早的那场** 能最大化后面天数的可选空间（贪心原理）。  
- 为了在每一天快速获取“最早结束的活动”，可以使用 **最小堆（优先队列）**，把所有当前**已经开始**但**还未结束**的活动的结束时间放进去，堆顶就是最小的结束时间。  

**具体步骤**  

1. **按开始时间升序排序** 所有活动。这样我们可以在遍历天数时，顺序把当天刚开始的活动加入堆中。  
2. 用变量 `day` 从 **最早的开始日** 开始逐天递增。  
3. **加入新活动**：把所有 `start == day` 的活动的结束时间 `end` 推入最小堆。  
4. **移除失效活动**：堆顶的结束时间如果已经小于 `day`（意味着这场活动已经错过），就把它弹出。  
5. **参加一场活动**：如果堆非空，弹出堆顶（最早结束的活动），把 `day` 标记为已占用，计数 `ans += 1`。  
6. `day` 加 1，继续循环，直到所有活动都处理完且堆为空。  

**类比**：  
- 把每天想象成一条流水线。  
- “已经开始但未结束的活动”是待加工的原料，放在一个**最小堆**的托盘里，托盘最上面永远是**最早到期**的原料。我们每走一步，就取走最上面的原料加工（参加），保证不会因为错过期限而浪费。  

#### 代码（Python）  
```python
import heapq
from typing import List

def max_events(events: List[List[int]]) -> int:
    """
    贪心 + 最小堆
    1. 按 start 排序
    2. day 从最小的 start 开始遍历
    3. 每天把所有 start==day 的 end 加入堆
    4. 弹出已经过期的 (end < day) 项
    5. 若堆非空，弹出堆顶参加该活动
    """
    # 1. 按开始时间升序；若相同，结束时间也升序（方便后面统一处理）
    events.sort(key=lambda x: (x[0], x[1]))

    min_heap = []          # 存放活动的结束时间
    i = 0                  # events 的指针
    n = len(events)
    ans = 0
    # day 取最小的可能开始日到最大可能结束日之间
    day = 1
    # 为了避免遍历到无意义的空白天，直接把 day 初始化为最早的 start
    if n:
        day = events[0][0]

    while i < n or min_heap:
        # 2. 把所有在当前 day 开始的活动放入堆
        while i < n and events[i][0] == day:
            heapq.heappush(min_heap, events[i][1])   # 只需要结束时间
            i += 1

        # 3. 移除已经错过的活动（结束时间 < 当前 day）
        while min_heap and min_heap[0] < day:
            heapq.heappop(min_heap)

        # 4. 若还有可参加的活动，参加结束时间最早的那场
        if min_heap:
            heapq.heappop(min_heap)   # 参加该活动
            ans += 1
            day += 1                 # 下一天继续
        else:
            # 堆空且还有未处理的活动，直接跳到下一个活动的开始日
            if i < n:
                day = events[i][0]

    return ans
```

#### 复杂度  
- **时间复杂度**：`O(N log N)`  
  - 排序需要 `O(N log N)`。  
  - 每个活动的结束时间至多进堆一次、出堆一次，堆操作是 `log N`，共 `2N` 次，仍是 `O(N log N)`。  
  - 与暴力解相比，**不再随天数线性增长**，即使天数达到 `10^5`，时间仍保持在 `N log N` 级别。  
- **空间复杂度**：`O(N)`  
  - 最坏情况下所有活动的结束时间都在同一天或相邻天，堆里会同时存放 `N` 条记录。  

---

## 心得  

- **核心技巧**：**贪心 + 最小堆**，在每一天优先参加结束时间最早的活动，以保留后续天数的选择空间。  
- **适用的题型**  
  1. “安排尽可能多的任务/会议”类（如 LeetCode 2529 `Maximum Number of Events That Can Be Attended II`、面试题 “最多会议数”）。  
  2. “在时间区间里选点，使得点数最多”类（如 “Maximum Number of Non‑Overlapping Intervals”。）  
  3. “带期限的任务调度”类（如 “Course Schedule III”。）  
- **一句话总结**：**每一天只参加最早结束的活动**，用最小堆快速找出它。

---

## 反思  

- **第一反应**：看到“每个活动都有一个可参加的时间段”，自然想到**遍历每一天**，看能否安排。于是想到暴力的“逐天挑活动”。  
- **最容易踩的坑**  
  1. **天数跨度大**：如果直接用 `for day in range(1, max_day+1)`，会导致 `O(N * max_day)` 的超时。  
  2. **忘记弹出已过期的活动**：堆里可能残留结束时间已经小于当前 `day` 的活动，若不清理会错误地计数。  
  3. **跳过空白天**：当堆空且还有未处理的活动时，需要把 `day` 直接跳到下一个活动的 `start`，否则会出现大量无意义的循环。  
- **下次类似题的第一步**：先**把所有区间按左端点排序**，思考“在当前时刻能做什么”，然后**用合适的数据结构（堆、集合）维护“可选的右端点”，贪心地取最优的”。