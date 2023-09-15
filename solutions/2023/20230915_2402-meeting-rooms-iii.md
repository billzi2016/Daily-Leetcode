# #2402. 会议室 III / Meeting Rooms III

> 难度：困难 · 标签：Array、Hash Table、Sorting、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/meeting-rooms-iii/)

---

## 题目（英文原版）

**Description**

You are given an integer n. There are n rooms numbered from 0 to n - 1.
You are given a 2D integer array meetings where meetings[i] = [starti, endi] means that a meeting will be held during the half-closed time interval [starti, endi). All the values of starti are unique.
Meetings are allocated to rooms in the following manner:
Return the number of the room that held the most meetings. If there are multiple rooms, return the room with the lowest number.
A half-closed interval [a, b) is the interval between a and b including a and not including b.

**Examples**

**Example 1:**

```
Input: n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
Output: 0
Explanation:
- At time 0, both rooms are not being used. The first meeting starts in room 0.
- At time 1, only room 1 is not being used. The second meeting starts in room 1.
- At time 2, both rooms are being used. The third meeting is delayed.
- At time 3, both rooms are being used. The fourth meeting is delayed.
- At time 5, the meeting in room 1 finishes. The third meeting starts in room 1 for the time period [5,10).
- At time 10, the meetings in both rooms finish. The fourth meeting starts in room 0 for the time period [10,11).
Both rooms 0 and 1 held 2 meetings, so we return 0.
```

**Example 2:**

```
Input: n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
Output: 1
Explanation:
- At time 1, all three rooms are not being used. The first meeting starts in room 0.
- At time 2, rooms 1 and 2 are not being used. The second meeting starts in room 1.
- At time 3, only room 2 is not being used. The third meeting starts in room 2.
- At time 4, all three rooms are being used. The fourth meeting is delayed.
- At time 5, the meeting in room 2 finishes. The fourth meeting starts in room 2 for the time period [5,10).
- At time 6, all three rooms are being used. The fifth meeting is delayed.
- At time 10, the meetings in rooms 1 and 2 finish. The fifth meeting starts in room 1 for the time period [10,12).
Room 0 held 1 meeting while rooms 1 and 2 each held 2 meetings, so we return 1.
```

**Constraints**

- 1 <= n <= 100
- 1 <= meetings.length <= 105
- meetings[i].length == 2
- 0 <= starti < endi <= 5 * 105
- All the values of starti are unique.

---

## 题目（中文翻译）

**描述**  
给定一个整数 `n`，有 `n` 个会议室，编号从 `0` 到 `n - 1`。  
再给定一个二维整数数组 `meetings`，其中 `meetings[i] = [starti, endi]` 表示第 `i` 场会议将在半开区间 `[starti, endi)`（包括 `starti` 不包括 `endi`）进行。所有的 `starti` 均唯一。  

会议室的分配规则如下：  

返回召开会议次数最多的会议室编号。如果有多个会议室并列，则返回编号最小的那个。  

**半开区间** `[a, b)` 表示从 `a` 到 `b` 的区间，包含 `a` 而不包含 `b`。  

**示例**  

*示例 1*  
```
输入: n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
输出: 0
解释:
- 时间 0 时，两间会议室均空闲，第一场会议在会议室 0 开始。
- 时间 1 时，只有会议室 1 空闲，第二场会议在会议室 1 开始。
- 时间 2 时，两间会议室均被占用，第三场会议被延迟。
- 时间 3 时，两间会议室均被占用，第四场会议被延迟。
- 时间 5 时，会议室 1 的会议结束，第三场会议此时开始并占用会议室 1。
- 时间 7 时，会议室 1 的会议结束，第四场会议此时开始并占用会议室 1。
- 时间 10 时，会议室 0 的会议结束。  
最终，会议室 0 开办了 2 场会议，会议室 1 开办了 2 场会议。因为编号更小的会议室 0 满足条件，返回 0。
```

*示例 2*  
```
输入: n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
输出: 1
解释:
- 时间 1 时，三间会议室均空闲，第一场会议在会议室 0 开始。
- 时间 2 时，会议室 1、2 空闲，第二场会议在会议室 1 开始。
- 时间 3 时，只有会议室 2 空闲，第三场会议在会议室 2 开始。
- 时间 4 时，三间会议室均被占用，第四场会议被延迟。
- 时间 5 时，会议室 2 的会议结束，第四场会议此时开始并占用会议室 2。
- 时间 6 时，会议室 1 的会议结束，第五场会议此时开始并占用会议室 1。  
最终，会议室 0、1、2 分别开办了 1、2、2 场会议。最多的会议次数为 2，编号最小的会议室是 1，故返回 1。
```

**约束条件**  
- `1 <= n <= 100`  
- `1 <= meetings.length <= 10^5`  
- `meetings[i].length == 2`  
- `0 <= starti < endi <= 5 * 10^5`  
- 所有的 `starti` 均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把每个会议按照 **开始时间** 排序后，逐个处理。  
我们维护一个长度为 `n` 的数组 `end_time[i]`，表示第 `i` 个会议室目前占用到的时间点（如果空闲则为 `0`）。  

处理第 `k` 场会议 `[s, e)` 时：

1. 先遍历所有会议室，找出 **结束时间 ≤ s**（即此时已经空闲）的房间。  
2. 如果有空闲房间，挑 **编号最小** 的那间；  
3. 否则只能等到 **最早结束** 的房间空出来。我们把会议的实际开始时间改为那间房间的 `end_time`，再把它的结束时间设为 `实际开始 + (e‑s)`（会议时长不变，只是被“推迟”了）。  
4. 用 `cnt[i]` 记录每个房间被使用的次数，最后返回使用次数最多且编号最小的房间。

> **类比**：  
> - `end_time` 就像每个教室的“下课铃”，铃响后教室才空出来。  
> - 在找空闲教室时，我们像是 **查字典**：键是教室编号，值是下课铃时间。  

这个办法一定能得到正确答案，因为我们严格按照题目描述的调度规则一步步模拟了会议的安排过程。

#### 代码（Python）  

```python
from typing import List

def mostBooked(n: int, meetings: List[List[int]]) -> int:
    # 1. 按开始时间排序，保证按照时间顺序处理
    meetings.sort(key=lambda x: x[0])

    # 2. 每个房间当前的结束时间，初始都是 0（空闲）
    end_time = [0] * n
    # 3. 统计每个房间被使用的次数
    cnt = [0] * n

    for s, e in meetings:                     # 逐个会议
        duration = e - s                       # 会议时长不变

        # ① 找所有已经空闲的房间（结束时间 ≤ 会议开始时间）
        free_rooms = [i for i in range(n) if end_time[i] <= s]

        if free_rooms:                         # 有空闲房间
            room = min(free_rooms)             # 取编号最小的
            actual_start = s
        else:                                  # 没有空闲房间，需要等最早结束的房间
            # 找结束时间最早的房间（如果有多个，取编号最小的）
            earliest_end = min(end_time)
            # 可能有多个房间同时最早结束，取编号最小的
            room = min(i for i, t in enumerate(end_time) if t == earliest_end)
            actual_start = earliest_end        # 会议被推迟到该时间开始

        # ② 更新该房间的结束时间和使用计数
        end_time[room] = actual_start + duration
        cnt[room] += 1

    # 3. 返回使用次数最多且编号最小的房间
    max_cnt = max(cnt)
    for i, c in enumerate(cnt):
        if c == max_cnt:
            return i
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`（`m = meetings.length`），因为对每场会议我们都要遍历 `n` 个房间寻找空闲或最早结束的房间。  
  - **大白话**：如果有 10 000 场会议、100 间会议室，最坏情况下要检查 1 000 000 次。  

- **空间复杂度**：`O(n)`，只用了两个长度为 `n` 的数组（结束时间和计数），和输入本身不计在内。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次线性扫描所有房间**，导致 `O(m·n)`。  
我们可以把「空闲房间」和「正在使用的房间」分别放进 **最小堆（优先队列）**，这样一次操作只需 `log n` 的代价。

- **空闲房间堆 `free`**：存放当前空闲的房间编号，堆顶永远是编号最小的空闲房间。  
- **占用房间堆 `busy`**：存放元组 `(结束时间, 房间编号)`，堆顶是最早结束的会议（如果有多个，同样取编号最小的，因为 Python 的元组比较会先比较第一个元素，再比较第二个）。  

处理流程（同样先把会议按开始时间排序）：

1. **把已经结束的会议释放**：  
   当 `busy` 堆顶的结束时间 ≤ 当前会议的开始时间 `s` 时，说明这些会议已经结束。我们把对应的房间编号弹出 `busy`，放回 `free` 堆。这样 `free` 堆始终保存“此刻可以直接使用的房间”。  

2. **决定使用哪间房间**  
   - 若 `free` 非空，直接取堆顶（编号最小的空闲房间）。  
   - 否则所有房间都在忙碌，取 `busy` 堆顶（最早结束的会议），把当前会议的开始时间 **推迟** 到该结束时间 `end`，然后使用同一间房间。  

3. **更新状态**  
   - 计算该会议的实际结束时间 `actual_end = actual_start + (e‑s)`。  
   - 把 `(actual_end, room)` 再次压入 `busy` 堆。  
   - `cnt[room] += 1` 记录使用次数。  

这样每场会议只涉及 **堆的 push/pop**（`log n`），不再遍历所有房间。

> **类比**：  
> - `free` 堆像是 **空闲车位的停车场入口**，车子进去时总是先占最靠近入口的车位（编号最小）。  
> - `busy` 堆像是 **计时器队列**，最先报时的计时器先释放车位。  

#### 代码（Python）  

```python
import heapq
from typing import List

def mostBooked(n: int, meetings: List[List[int]]) -> int:
    # 1. 按开始时间排序
    meetings.sort(key=lambda x: x[0])

    # 2. 空闲房间堆（只存编号），初始时所有房间都是空闲的
    free = list(range(n))
    heapq.heapify(free)

    # 3. 正在占用的房间堆，存 (结束时间, 房间编号)
    busy = []               # 为空时表示没有正在进行的会议

    # 4. 记录每个房间被使用的次数
    cnt = [0] * n

    for s, e in meetings:
        duration = e - s

        # ① 释放所有在当前会议开始前已经结束的房间
        while busy and busy[0][0] <= s:
            end_time, room = heapq.heappop(busy)   # 取出最早结束的会议
            heapq.heappush(free, room)             # 该房间变为可用

        # ② 决定使用哪间房间
        if free:                                    # 有空闲房间
            room = heapq.heappop(free)              # 取编号最小的空闲房间
            actual_start = s
        else:                                       # 没有空闲房间，需要等最早结束的会议
            end_time, room = heapq.heappop(busy)    # 取最早结束的房间
            actual_start = end_time                 # 会议被推迟到该时间开始

        # ③ 更新该房间的结束时间、使用计数并重新放入 busy 堆
        actual_end = actual_start + duration
        heapq.heappush(busy, (actual_end, room))
        cnt[room] += 1

    # 4. 找出使用次数最多且编号最小的房间
    max_cnt = max(cnt)
    for i, c in enumerate(cnt):
        if c == max_cnt:
            return i
```

#### 复杂度  

- **时间复杂度**：`O(m log n)`  
  - 每场会议最多进行两次堆操作（`push`/`pop`），堆的大小不超过 `n`，所以每次操作是 `log n`。  
  - 与暴力解相比，从 `O(m·n)` 降到了 `O(m·log n)`，在 `n` 较大（比如 100）且会议很多（10⁵）时提升非常明显。  

- **空间复杂度**：`O(n)`  
  - `free`、`busy` 两个堆以及计数数组 `cnt` 都是与房间数 `n` 成正比。  

---  

## 心得  

- **核心技巧**：使用 **两个最小堆** 分别管理空闲房间和正在进行的会议，做到“随时可以得到最小编号的空闲房间”或“最早结束的房间”。  
- **适用的题型**：  
  1. “会议室分配” 系列（如 *Meeting Rooms II*、*Meeting Rooms III*）。  
  2. “任务调度” 类问题，需要在资源有限的情况下选择最早可用的资源（如 *Car Pooling*、*Minimum Number of Platforms*）。  
  3. “有序事件处理” 场景，常用堆维护“下一个要发生的事件”。  
- **一句话总结**：**把“空闲/忙碌”状态抽象成最小堆，随时取最小的即可高效模拟调度**。  

---  

## 反思  

- **第一反应**：看到“如果没有空闲房间，就等最早结束的房间”，立刻想到用 **优先队列**（堆）来快速获取最早结束的会议。  
- **最容易踩的坑**：  
  1. **会议被推迟后仍需占用原来的房间**——不能把它重新放进空闲堆，否则会出现“同一时间两个会议占同一房间”。  
  2. **开始时间相同的会议**：题目保证 `start` 唯一，但如果忘记排序会导致顺序错误。  
  3. **堆中存储的元组顺序**：要把 `(结束时间, 房间编号)` 作为键，这样当结束时间相同会自动比较房间编号，保证“编号最小”原则。  
- **下次遇到同类题**：第一步先 **把所有资源（房间）放进一个“空闲”最小堆**，然后 **按时间顺序遍历事件**，用第二个堆维护“正在使用的资源”。这样几乎所有涉及“最早可用资源” 的调度问题都能快速上手。