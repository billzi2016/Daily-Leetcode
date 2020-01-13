# #731. 我的日历 II / My Calendar II

> 难度：中等 · 标签：Array、Binary Search、Design、Segment Tree、Prefix Sum、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/my-calendar-ii/)

---

## 题目（英文原版）

**Description**

You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a triple booking.
A triple booking happens when three events have some non-empty intersection (i.e., some moment is common to all the three events.).
The event can be represented as a pair of integers startTime and endTime that represents a booking on the half-open interval [startTime, endTime), the range of real numbers x such that startTime <= x < endTime.
Implement the MyCalendarTwo class:

**Examples**

**Example 1:**

```
Input
["MyCalendarTwo", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
Output
[null, true, true, true, false, true, true]

Explanation
MyCalendarTwo myCalendarTwo = new MyCalendarTwo();
myCalendarTwo.book(10, 20); // return True, The event can be booked. 
myCalendarTwo.book(50, 60); // return True, The event can be booked. 
myCalendarTwo.book(10, 40); // return True, The event can be double booked. 
myCalendarTwo.book(5, 15);  // return False, The event cannot be booked, because it would result in a triple booking.
myCalendarTwo.book(5, 10); // return True, The event can be booked, as it does not use time 10 which is already double booked.
myCalendarTwo.book(25, 55); // return True, The event can be booked, as the time in [25, 40) will be double booked with the third event, the time [40, 50) will be single booked, and the time [50, 55) will be double booked with the second event.
```

**Constraints**

- 0 <= start < end <= 109
- At most 1000 calls will be made to book.

---

## 题目（中文翻译）

**描述**  
你正在实现一个用于日程安排的程序。只有在新增的事件不会导致出现**三重预订（triple booking）**时，才能添加该事件。  
当三个事件在某个非空区间上都有交集（即存在某个时刻同时被这三个事件占用）时，就会产生三重预订。  

每个事件用一对整数 `startTime` 和 `endTime` 表示，代表在**半开区间（half-open interval）** `[startTime, endTime)` 上的预订，即满足 `startTime <= x < endTime` 的所有实数 `x`。

实现 `MyCalendarTwo` 类，使其能够判断是否可以成功预订新事件。

**示例**  

```text
输入
["MyCalendarTwo", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
输出
[null, true, true, true, false, true, true]
```

**解释**  
```java
MyCalendarTwo myCalendarTwo = new MyCalendarTwo();
myCalendarTwo.book(10, 20); // 返回 true，事件可以预订。
myCalendarTwo.book(50, 60); // 返回 true，事件可以预订。
myCalendarTwo.book(10, 40); // 返回 true，事件可以双重预订（double booked）。
myCalendarTwo.book(5, 15);  // 返回 false，事件不能预订，因为会导致三重预订。
myCalendarTwo.book(5, 10);  // 返回 true，事件可以预订，因为它不涉及已经双重预订的时刻 10。
myCalendarTwo.book(25, 55); // 返回 true，事件可以预订；区间 [25, 40) 与第三个事件形成双重预订，  
                            // 区间 [40, 50) 为单次预订，区间 [50, 55) 与第二个事件形成双重预订。
```

**约束条件**  

- `0 <= start < end <= 10^9`
- 最多会调用 `book` 方法 1000 次。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把已经成功预定的所有区间全部记下来，每次要加入一个新区间 `[s, e)` 时，**把它和已经存在的每一个区间都比较**，看会不会出现“三重预定”。  

具体做法可以这样想：

1. 把已有的每个区间记在一个普通的 Python `list` 里（就像把所有的约会时间写在一本日记本上）。  
2. 新的区间进来后，先遍历这本日记本，找出所有**与它有交集**的旧区间。  
3. 再把这些交集两两组合，检查它们的交集是否仍然和新区间有交集。  
   - 如果出现这种情况，说明同一时刻已经被 **三个** 区间占用了，必须返回 `False`（预定失败）。  
   - 否则，新区间可以加入日记本，返回 `True`。

> **类比**：把每个约会想象成一张纸条写在时间线上。暴力解就是把所有纸条都摊开，每次新纸条来时，用手去摸每一张旧纸条，看看有没有三层纸叠在同一个位置。

**为什么正确**：  
只要我们检查了所有旧区间的两两交集，并且这些交集与新区间都有交集，就一定找到了一个时刻被三个区间共同覆盖的情况；反之若不存在这种情况，说明任意时刻最多只有两个区间重叠，新区间可以安全加入。

**时间/空间复杂度**：  
- 对每一次 `book`，我们要遍历已有的 `n` 个区间并两两比较，最坏情况要进行 `O(n²)` 次交集判断。  
- 由于会调用 `book` 最多 `1000` 次，整体复杂度是 **O(n³)**（因为每一次 `book` 的 `n` 都在增长）。  
- 只需要把所有区间存起来，额外空间是 `O(n)`。

> **大白话**：`O(n³)` 可以想象成“把 1000 本日记本每本都翻遍三遍”，显然会很慢。

#### 代码（Python）

```python
from typing import List, Tuple

class MyCalendarTwo:
    def __init__(self):
        # 已经成功预定的所有区间，形式为 (start, end)
        self.events: List[Tuple[int, int]] = []

    # 判断两个区间是否有交集，返回交集区间
    def _overlap(self, a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
        start = max(a[0], b[0])
        end   = min(a[1], b[1])
        if start < end:          # 真正的交集（左闭右开）
            return (start, end)
        return None               # 没有交集

    def book(self, start: int, end: int) -> bool:
        new_interval = (start, end)

        # 第一步：找出所有已经和 new_interval 有交集的旧区间
        overlaps = []
        for ev in self.events:
            ov = self._overlap(ev, new_interval)
            if ov:
                overlaps.append(ov)

        # 第二步：在这些交集中，两两比较，看是否还能再和 new_interval 重叠
        # 如果出现，就说明会形成三重预定
        for i in range(len(overlaps)):
            for j in range(i + 1, len(overlaps)):
                if self._overlap(overlaps[i], overlaps[j]):
                    # 这里已经找到了三个区间共同覆盖的时刻
                    return False

        # 没有冲突，加入 events
        self.events.append(new_interval)
        return True
```

#### 复杂度

- **时间复杂度**：`O(n²)`（每次 `book` 要遍历已有区间并两两比较）。  
  - **含义**：如果已经有 1000 条预约，检查一次大约要比对 1000 × 1000 / 2 ≈ 500 000 次，随预约数的增长呈二次方增长。  
- **空间复杂度**：`O(n)`（只存所有已预定的区间）。  
  - **含义**：占用的内存随预约数线性增长，最多存 1000 条记录，几乎可以忽略不计。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **两两比较** 那一步——每次都要遍历所有已有区间的组合。  
我们可以把“已经被双预定的时间段”单独记录下来，这样只需要 **一次遍历** 就能判断是否会出现三重预定。

核心想法：

1. **单预定区间 (`booked`)**：所有已经预定（至少一次）的时间段。  
2. **双预定区间 (`overlaps`)**：已经出现 **两次** 预定的时间段。  
   - 只要新的区间和 `overlaps` 中的任意一个区间有交集，就会产生三重预定，直接返回 `False`。  
3. 如果没有冲突，我们需要把 **新区间与 `booked` 中的交集** 加入 `overlaps`（因为这些交集现在已经是“双预定”了）。  
4. 最后，把新区间本身加入 `booked`，完成一次成功预定。

> **类比**：  
> - 想象有两层透明的胶片分别记录“已经有人预定的时间”和“已经被两个人抢的时间”。  
> - 当新的一层胶片（新预约）要贴上去时，先检查它是否和第二层胶片（双预定）有重叠——如果有，说明已经有两个人占了这块时间，第三个人再来就会“压到三层”，不允许。  
> - 没冲突的话，再把它和第一层胶片（单预定）的交集复制到第二层（因为这块时间现在被两个人占了），最后把整张新胶片贴到第一层。

**为什么正确**：

- `overlaps` 中的每个区间恰好代表**已经被两次预定**的时间段。只要新预约触碰到其中任意一点，就必然会导致**第三次**预定，这正是题目禁止的情况。  
- 把新预约与 `booked` 的交集加入 `overlaps`，是因为这些交集之前只被预定一次，现在又被预定一次，正好变成“双预定”。  
- 其余不与 `booked` 重叠的部分仍然是**单预定**，直接放进 `booked` 即可。

**核心数据结构**：两个列表，分别保存**不相交的区间**（可以自行合并，代码里直接保留为列表）。列表的遍历是 `O(n)`，而不是 `O(n²)`，因此整体时间复杂度下降到 `O(n)`（每次 `book` 只遍历一次已有区间）。

#### 代码（Python）

```python
from typing import List, Tuple

class MyCalendarTwo:
    def __init__(self):
        # 已经被预定至少一次的区间（单预定）
        self.booked: List[Tuple[int, int]] = []
        # 已经被预定两次的区间（双预定）
        self.overlaps: List[Tuple[int, int]] = []

    # 返回两个区间的交集，如果没有交集返回 None
    def _intersection(self, a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int] | None:
        start = max(a[0], b[0])
        end   = min(a[1], b[1])
        if start < end:
            return (start, end)
        return None

    def book(self, start: int, end: int) -> bool:
        new_interval = (start, end)

        # 1️⃣ 检查是否会产生三重预定：新区间与任何双预定区间有交集即失败
        for ov in self.overlaps:
            if self._intersection(new_interval, ov):
                # 与已有的双预定区间重叠 → 必然三重预定
                return False

        # 2️⃣ 将新区间与所有单预定区间的交集记录为“双预定”
        #   这里不能直接修改 self.overlaps，防止遍历过程中产生干扰
        new_overlaps: List[Tuple[int, int]] = []
        for b in self.booked:
            inter = self._intersection(new_interval, b)
            if inter:
                new_overlaps.append(inter)

        # 把本次产生的双预定区间合并到全局的 overlaps 中
        self.overlaps.extend(new_overlaps)

        # 3️⃣ 最后把新区间加入单预定列表，完成预定
        self.booked.append(new_interval)

        return True
```

> **代码说明**  
> - 第 1 步只遍历 `overlaps`（双预定），最坏是 `O(n)`。  
> - 第 2 步遍历 `booked`（单预定），同样是 `O(n)`。  
> - 第 3 步是常数时间的列表追加。  
> - 因此每次调用 `book` 的时间复杂度是 `O(n)`，整体 `O(n²)`（`n` ≤ 1000，仍然很快）。  
> - 空间上我们只保存两组区间，最多各 `O(n)`。

#### 复杂度

- **时间复杂度**：`O(n)`（每次 `book` 只遍历一次已存在的区间列表）。  
  - **含义**：如果已经有 1000 条预约，检查一次只需要比对 1000 次，而不是 1000 × 1000 次，速度提升约 1000 倍。  
- **空间复杂度**：`O(n)`（保存两套区间列表），随预约数线性增长。

---

## 心得

- **核心技巧**：把“已经被两次预定的时间段”单独记录，用**差分/双列表**的思路把冲突检测从**三层循环**降到**两层循环**。  
- **适用的题型**：  
  1. **My Calendar I**（只能出现一次预定）——只需要维护单预定列表。  
  2. **My Calendar III**（要求返回最大重叠次数）——可以使用差分数组或有序映射来统计任意时刻的重叠次数。  
  3. **区间冲突检测**（如会议室安排）——同样可以把“已占用区间”和“已双占区间”分层管理。  
- **一句话总结**：**把“已经双占的时间段”提前保存，一旦新预约触碰到它，就必然是非法的——这就是避免三重预定的钥匙。**

---

## 反思

- **第一反应**：直接把所有已有区间两两组合检查，结果是 `O(n³)`，实现起来也很笨拙。  
- **最容易踩的坑**：  
  - 忽略 **半开区间** `[start, end)` 的特性，导致边界 `end` 与 `start` 产生错误的重叠。  
  - 在更新 `overlaps` 时，直接在遍历中修改列表会导致漏掉部分交集或产生错误的双预定。  
- **下次遇到同类题**：第一步先思考 **“哪些状态已经是危机点（如双预定）”，把它们单独抽出来保存**，再在新操作时只检查这些危机点即可。这样可以把时间复杂度从指数级降低到线性级。