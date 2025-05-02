# #3169. 统计无会议的天数 / Count Days Without Meetings

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-days-without-meetings/)

---

## 题目（英文原版）

**Description**

You are given a positive integer days representing the total number of days an employee is available for work (starting from day 1). You are also given a 2D array meetings of size n where, meetings[i] = [start_i, end_i] represents the starting and ending days of meeting i (inclusive).
Return the count of days when the employee is available for work but no meetings are scheduled.
Note: The meetings may overlap.

**Examples**

**Example 1:**

```
Input: days = 10, meetings = [[5,7],[1,3],[9,10]]
Output: 2
Explanation:
There is no meeting scheduled on the 4 th and 8 th days.
```

**Example 2:**

```
Input: days = 5, meetings = [[2,4],[1,3]]
Output: 1
Explanation:
There is no meeting scheduled on the 5 th day.
```

**Example 3:**

```
Input: days = 6, meetings = [[1,6]]
Output: 0
Explanation:
Meetings are scheduled for all working days.
```

**Constraints**

- 1 <= days <= 109
- 1 <= meetings.length <= 105
- meetings[i].length == 2
- 1 <= meetings[i][0] <= meetings[i][1] <= days

---

## 题目（中文翻译）

你得到一个正整数 `days`，表示员工可工作的总天数（从第 1 天开始）。同时给定一个大小为 `n` 的二维数组 `meetings`，其中 `meetings[i] = [start_i, end_i]` 表示第 i 场会议的开始天和结束天（**inclusive**，即包含两端）。  
返回员工可工作且没有任何会议安排的天数。

**注意**：会议可能会重叠。

### 示例

#### 示例 1
**Input:** `days = 10, meetings = [[5,7],[1,3],[9,10]]`  
**Output:** `2`  
**Explanation:** 第 4 天和第 8 天没有安排会议。

#### 示例 2
**Input:** `days = 5, meetings = [[2,4],[1,3]]`  
**Output:** `1`  
**Explanation:** 第 5 天没有安排会议。

#### 示例 3
**Input:** `days = 6, meetings = [[1,6]]`  
**Output:** `0`  
**Explanation:** 所有工作日都有会议安排。

### 约束条件
- `1 <= days <= 10^9`
- `1 <= meetings.length <= 10^5`
- `meetings[i].length == 2`
- `1 <= meetings[i][0] <= meetings[i][1] <= days`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一天都拿出来看看，判断这一天有没有会议。如果没有，就把计数器加一。

- **使用的数据结构**：  
  - `days` 天数我们可以用一个长度为 `days` 的列表（相当于一张“日历”），下标 `i` 表示第 `i+1` 天，值 `True/False` 表示当天是否被会议占用了。  
  - “哈希表就像查字典，key 是词，value 是页码”。这里的列表就像一本**一页一页的日历本**，我们把每个有会议的日期在对应页上打上勾。

- **为什么正确**：  
  只要遍历完所有天数，并且对每一天都检查是否在任意一个会议区间内，就一定能找出所有没有会议的天数。  

- **时间/空间复杂度**（大白话）  
  - **时间**：如果我们把每一天都和所有会议逐个比对，最坏情况要做 `days × n` 次比较。这里的 `O(days·n)` 可以想象成“把 1000 天的日历，每天都去翻 100 场会议的记录”，工作量会随天数和会议数一起成倍增长。  
  - **空间**：需要额外的 `days` 长度的列表来记录每一天是否被占用，空间是 `O(days)`，相当于“准备一本和工作天数一样厚的日历本”。

> **注意**：本题的约束 `days ≤ 10⁹`，显然直接开这么大的列表会爆内存。下面的暴力实现只适用于 **演示思路** 或者 `days` 很小的情况（例如在本地调试时），真正提交时必须使用更高效的算法。

#### 代码（Python）

```python
def count_days_without_meetings_bruteforce(days: int, meetings: list[list[int]]) -> int:
    # 用一个布尔列表记录每一天是否有会议，默认 False 表示没有会议
    occupied = [False] * days               # 下标 0 对应第 1 天

    # 把所有会议的日期都标记为 True
    for start, end in meetings:
        # 将区间 [start, end]（包含两端）对应的下标全部设为 True
        for d in range(start - 1, end):     # 注意 Python 下标从 0 开始
            occupied[d] = True

    # 统计没有被标记的天数，即没有会议的天数
    free_days = sum(1 for is_meeting in occupied if not is_meeting)
    return free_days
```

#### 复杂度

- **时间复杂度**：`O(days * n)`  
  解释：每一天（`days`）都要遍历所有会议（`n`），工作量随两者乘积线性增长。

- **空间复杂度**：`O(days)`  
  解释：需要一个长度等于 `days` 的布尔数组来保存每一天的状态。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“逐天检查”** 是慢的根源，因为天数可能高达 `10⁹`，根本不可能把每一天都枚举。  
真正的瓶颈在于 **“把相同的工作重复做很多遍”**——同一个区间内部的每一天我们都检查了 `n` 次。

**优化的关键**：我们不需要关心每一天到底是哪一天，只需要知道 **哪些天被会议覆盖**，以及 **覆盖的总长度**。  
如果把所有会议区间合并成若干不相交的“大区间”，那么：

```
总的被占用天数 = Σ (每个合并后区间的长度)
没有会议的天数 = days - 总的被占用天数
```

于是我们只要完成两件事：

1. **把所有会议区间按起始时间排序**（就像把日程表按时间顺序排好）。
2. **合并重叠或相邻的区间**。  
   - 维护一个“当前合并区间”。  
   - 遍历排好序的会议：
     - 如果下一个会议的起始时间 ≤ 当前区间的结束时间 + 1（相邻也算连续），说明它们可以合并：把当前区间的结束时间取两者的最大值。  
     - 否则，当前区间结束，记下它的长度并开启一个新的合并区间。

**核心数据结构**：  
- **列表**（List）用来存放排序后的会议。  
- **两个整数** `cur_start, cur_end` 记录正在合并的区间。  
  - 这类似于**双指针**的思路：一只指针指向当前区间的左端，另一只指向右端，随时准备伸展。

**类比**：想象你在把一堆重叠的绳子收拢成几根不交叉的绳子，收拢的过程就是“合并区间”。

#### 代码（Python）

```python
def count_days_without_meetings(days: int, meetings: list[list[int]]) -> int:
    """
    返回在 total days 天中，没有任何会议安排的天数。
    思路：先把所有会议区间合并，再用总天数减去被占用的天数。
    """
    if not meetings:
        return days                     # 没有任何会议，全部都是空闲

    # 1️⃣ 按起始时间升序排列（如果起始相同，再按结束时间升序）
    meetings.sort(key=lambda x: (x[0], x[1]))

    # 2️⃣ 合并区间并累计被占用的天数
    occupied = 0                         # 已经被会议占用的天数
    cur_start, cur_end = meetings[0]     # 初始化第一个合并区间

    for start, end in meetings[1:]:
        if start <= cur_end + 1:         # 与当前区间有交叉或相邻，需合并
            # 取更大的结束时间，扩大当前区间
            cur_end = max(cur_end, end)
        else:
            # 当前区间结束，累计长度
            occupied += cur_end - cur_start + 1
            # 开启新区间
            cur_start, cur_end = start, end

    # 别忘了把最后一个区间的长度加进来
    occupied += cur_end - cur_start + 1

    # 3️⃣ 用总天数减去已占用天数即为答案
    free_days = days - occupied
    # 防御性检查：理论上 occupied 不会超过 days，但加个 max 保证非负
    return max(free_days, 0)
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  解释：对 `n` 个会议进行一次排序需要 `O(n log n)`，合并过程是一次线性遍历 `O(n)`，所以整体是 `O(n log n)`。相比暴力的 `O(days·n)`，这里的时间只随会议数的对数增长，和天数 `days` 完全无关。

- **空间复杂度**：`O(1)`（不计输入）  
  解释：只用了常数个额外变量（`cur_start、cur_end、occupied`），没有额外的与 `days` 或 `n` 成正比的存储。排序本身在 Python 中是原地的（使用 Timsort），因此额外空间可以视为常数。

---

## 心得

- **核心技巧**：**区间合并**（Merge Intervals）  
  通过先排序再线性合并，能够把大量重叠区间压缩成少数不相交区间，从而把 “遍历每一天” 的问题转化为 “计算区间长度” 的问题。

- **适用的题型**  
  1. **合并区间**：如 *“Insert Interval”*、*“Merge Intervals”*。  
  2. **区间覆盖计数**：如 *“Maximum Length of Repeated Subarray”*（需要统计不被覆盖的长度）。  
  3. **区间差集**：如 *“Interval List Intersections”*（求两个区间列表的交集或差集）。

- **一句话总结**：**把所有会议先排好序，再把相交的区间合并，剩下的天数就是答案。**  

---

## 反思

- **拿到题目第一反应**：直接想遍历每一天去检查是否有会议，像在日历本上逐日打勾。  
- **最容易踩的坑**  
  - **大范围天数**：`days` 可达 `10⁹`，直接开数组会导致内存炸掉。  
  - **相邻区间**：如 `[1,3]` 与 `[4,5]` 实际上是连续的，合并时要判断 `start <= cur_end + 1`（不要漏掉相邻的情况）。  
  - **全部被占用**：如果所有天都被会议覆盖，答案应为 `0`，而不是负数。  
- **下次遇到同类题**：第一步先 **思考是否可以把“逐点检查”转化为“区间统计”**，如果可以，就立刻考虑 **排序 + 合并** 的套路。