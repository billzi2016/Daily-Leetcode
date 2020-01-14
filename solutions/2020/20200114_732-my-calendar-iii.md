# #732. 我的日历 III / My Calendar III

> 难度：困难 · 标签：Binary Search、Design、Segment Tree、Prefix Sum、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/my-calendar-iii/)

---

## 题目（英文原版）

**Description**

A k-booking happens when k events have some non-empty intersection (i.e., there is some time that is common to all k events.)
You are given some events [startTime, endTime), after each given event, return an integer k representing the maximum k-booking between all the previous events.
Implement the MyCalendarThree class:

**Examples**

**Example 1:**

```
Input
["MyCalendarThree", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
Output
[null, 1, 1, 2, 3, 3, 3]

Explanation
MyCalendarThree myCalendarThree = new MyCalendarThree();
myCalendarThree.book(10, 20); // return 1
myCalendarThree.book(50, 60); // return 1
myCalendarThree.book(10, 40); // return 2
myCalendarThree.book(5, 15); // return 3
myCalendarThree.book(5, 10); // return 3
myCalendarThree.book(25, 55); // return 3
```

**Constraints**

- 0 <= startTime < endTime <= 109
- At most 400 calls will be made to book.

---

## 题目（中文翻译）

当 **k‑预订（k-booking）** 发生时，表示有 **k** 个事件存在非空交集（即存在某个时间点同时属于这 **k** 个事件）。

给定一系列事件 `[startTime, endTime)`，在每次添加一个新事件后，返回一个整数 `k`，表示截至目前所有已添加事件中最大的 **k‑预订** 数。

实现 `MyCalendarThree` 类：

```cpp
class MyCalendarThree {
public:
    MyCalendarThree();               // 构造函数
    int book(int startTime, int endTime); // 预订一个新事件，返回当前的最大 k‑预订
};
```

---

### 示例

``` 
输入
["MyCalendarThree", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
输出
[null, 1, 1, 2, 3, 3, 3]

解释
MyCalendarThree myCalendarThree = new MyCalendarThree();
myCalendarThree.book(10, 20); // 返回 1
myCalendarThree.book(50, 60); // 返回 1
myCalendarThree.book(10, 40); // 返回 2
myCalendarThree.book(5, 15);  // 返回 3
myCalendarThree.book(5, 10);  // 返回 3
myCalendarThree.book(25, 55); // 返回 3
```

---

### 约束条件

- `0 <= startTime < endTime <= 10^9`
- 最多调用 `book` 方法 400 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次预约的时间段都保存下来，然后在 **每次** 再次预约时，和已有的所有区间逐个比较，统计在同一时刻被多少个区间覆盖，取最大值即为答案。

- **数据结构**：使用一个 `list` 保存所有已经预约的 `[start, end)` 区间。  
  - 可以把 `list` 想成一本日程本，里面每一页记着一次会议的起止时间。

- **正确性**：  
  对于新加入的区间 `[s, e)`，我们枚举已有的每一个区间 `[s_i, e_i)`，判断它们是否相交（即 `max(s, s_i) < min(e, e_i)`）。若相交，则说明这两个会议在某段时间里是同时进行的，重叠计数加 1。把所有相交的计数加到一起，再加上新加入的这一次预约本身，就得到这一次加入后所有会议的最大重叠数。遍历所有已有区间后，得到的最大值必然就是题目要求的 `k`。

- **复杂度分析**  
  - **时间**：每次 `book` 都要和之前所有区间比较，第一次比较 0 次，第二次比较 1 次，… 第 `n` 次比较 `n‑1` 次。总次数约为 `0 + 1 + … + (n‑1) = n·(n‑1)/2`，用 **大 O** 记就是 **O(n²)**。  
    大白话解释：如果你已经安排了 100 场会议，插入第 101 场时需要检查前面 100 场，整体工作量大约是“平方级”，会随会议数快速增长。
  - **空间**：只需要保存所有区间，空间是 **O(n)**。

#### 代码（Python）

```python
class MyCalendarThree:
    def __init__(self):
        # 保存已经预约的所有区间，像一本日程本
        self.intervals = []          # List[Tuple[int, int]]
        # 记录当前的最大重叠数
        self.max_overlap = 0

    def book(self, start: int, end: int) -> int:
        """
        暴力检查新加入的区间与已有区间的重叠情况
        """
        # 先把新区间加入列表（后面遍历时会一起算进来）
        self.intervals.append((start, end))

        # 统计所有区间的最大重叠数
        cur_max = 0
        # 对每一个区间，统计它与其它区间的重叠次数
        for i, (s1, e1) in enumerate(self.intervals):
            overlap = 1          # 自己本身算一次
            for j in range(i):   # 只和之前的区间比较，避免重复计数
                s2, e2 = self.intervals[j]
                # 两个区间相交的条件：max(start) < min(end)
                if max(s1, s2) < min(e1, e2):
                    overlap += 1
            cur_max = max(cur_max, overlap)

        # 更新全局最大值并返回
        self.max_overlap = max(self.max_overlap, cur_max)
        return self.max_overlap
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - `n` 为已经调用 `book` 的次数。每一次 `book` 需要和之前的所有区间逐一比对，工作量随 `n` 的平方增长。  
- **空间复杂度**：`O(n)`  
  - 只保存所有的区间，随调用次数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有已有区间**。实际上，我们只关心每个时间点上有多少个会议正在进行，而不是每两个区间之间的直接比较。  
如果把每个区间 `[start, end)` 看成两件事：

- 在 `start` 时 **+1**（会议开始，计数增加 1）  
- 在 `end`   时 **-1**（会议结束，计数减少 1）

把所有这些 “加 1 / 减 1” 的时间点按照时间顺序排好，然后从左到右累加这些增量，就能得到每个时刻的 **在进行的会议数**。其中的最大值就是答案。

这就是**差分数组 + 前缀和**的思想。实现上我们使用 **有序映射**（在 Python 中可以用 `dict` + `bisect` 手动维护有序键，或使用 `sortedcontainers.SortedDict`，这里演示手动实现）来记录每个关键时间点的增量：

1. `book(start, end)`：  
   - `delta[start] += 1`  
   - `delta[end]   -= 1`  
   - 把 `start`、`end` 插入有序的时间列表（若已存在则不重复插入）。
2. 计算当前最大重叠数：  
   - 按时间顺序遍历 `times`，累加对应的 `delta`，记录过程中出现的最大累计值。

因为每次插入和遍历都是 **对数时间** 或 **线性时间**（`times` 长度最多是 `2 * n`），整体复杂度是 **O(n log n)**，远快于暴力的 `O(n²)`。

> **核心概念解释**  
> - **有序映射（Ordered Map）**：想象一本记事本，左边写时间，右边写“这时要加几个人”。我们需要能够快速找到某个时间应该写在哪里并保持顺序，这就是有序映射的作用。  
> - **前缀和（Prefix Sum）**：把一本账本里每天的收支（增量）累加起来，得到每一天的总余额（当前进行的会议数）。最大余额就是我们想要的答案。

#### 代码（Python）

```python
import bisect
from collections import defaultdict

class MyCalendarThree:
    def __init__(self):
        # delta[t] 表示在时间 t 发生的增量 (+1 表示会议开始，-1 表示结束)
        self.delta = defaultdict(int)   # Dict[int, int]
        # 有序保存所有出现过的关键时间点，便于后续遍历
        self.times = []                  # List[int]
        # 当前的最大重叠数
        self.max_overlap = 0

    def _add_time(self, t: int) -> None:
        """
        将时间点 t 插入到有序列表 self.times 中（若已存在则不重复插入）。
        使用二分查找保持有序，时间复杂度 O(log m)，m 为列表长度。
        """
        idx = bisect.bisect_left(self.times, t)
        if idx == len(self.times) or self.times[idx] != t:
            self.times.insert(idx, t)   # 插入保持有序

    def book(self, start: int, end: int) -> int:
        """
        1. 在 start 处 +1，end 处 -1（差分数组的思想）。
        2. 把 start、end 加入有序时间列表。
        3. 按时间顺序遍历 delta，累计得到每个时刻的会议数，更新最大值。
        """
        # 记录增量
        self.delta[start] += 1
        self.delta[end]   -= 1

        # 保证时间点有序
        self._add_time(start)
        self._add_time(end)

        # 前缀和遍历，求最大重叠数
        cur = 0
        for t in self.times:
            cur += self.delta[t]          # 累加增量，得到此时进行的会议数
            if cur > self.max_overlap:
                self.max_overlap = cur    # 只会增长，不会下降

        return self.max_overlap
```

> **代码要点注释**  
> - `defaultdict(int)` 自动把不存在的键初始化为 `0`，省去手动检查。  
> - `bisect_left` 在已排好序的列表中定位插入位置，保持 `times` 永远有序。  
> - 累计 `cur` 的过程相当于把所有 “+1 / -1” 按时间顺序记下来，随时知道当前有多少会议在进行。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n` 为已调用 `book` 的次数。每次插入两个时间点使用二分查找 `O(log n)`，遍历所有关键时间点（最多 `2n`）累计前缀和是 `O(n)`。整体随 `n` 线性增长且每一步都有对数因子，远快于 `O(n²)`。  
- **空间复杂度**：`O(n)`  
  - 需要存储每个唯一的时间点及其增量，最多 `2n` 条记录。

---

## 心得

- **核心技巧**：把区间转化为“起点 +1、终点 -1”的差分形式，再使用有序映射 + 前缀和求最大重叠。  
- **适用题型**  
  1. **My Calendar I / II**（检查是否会冲突、最多两次重叠）  
  2. **区间颜色染色**（给每个区间上色，求任意时刻最多几种颜色）  
  3. **线上会议室需求**（求最少会议室数量）  
- **一句话总结**：把每个区间拆成“+1 / -1”事件，时间顺序累加，出现的最高计数就是答案。

---

## 反思

- **第一反应**：看到“最大 k‑booking”，立刻想到“遍历所有区间，两两比较”，于是写出暴力解。  
- **最容易踩的坑**  
  - **闭区间 vs 开区间**：题目使用 `[start, end)`，结束时间不算在区间内；如果忘记这点，在相邻区间如 `[5,10)` 与 `[10,15)` 会误判为重叠。  
  - **时间点的有序维护**：直接用普通 `dict` 会失去顺序，导致前缀和计算错误。  
  - **重复插入时间点**：若在 `times` 中出现重复，会导致累计增量被多算一次，需要在插入前检查是否已存在。  
- **下次思路**：一看到“区间的交叉次数”或“最大同时进行的活动”，第一步就想到“把区间拆成增量事件 + 前缀和”，再选择合适的数据结构（有序映射、线段树）实现。这样可以直接跳过 O(n²) 的暴力比较，快速得到 O(n log n) 或更优的解法。