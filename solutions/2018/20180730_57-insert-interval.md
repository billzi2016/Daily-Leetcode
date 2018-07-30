# #57. 插入区间 / Insert Interval

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/insert-interval/)

---

## 题目（英文原版）

**Description**

You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.
Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
Return intervals after the insertion.
Note that you don't need to modify intervals in-place. You can make a new array and return it.

**Examples**

**Example 1:**

```
Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]
```

**Example 2:**

```
Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
```

**Constraints**

- 0 <= intervals.length <= 104
- intervals[i].length == 2
- 0 <= starti <= endi <= 105
- intervals is sorted by starti in ascending order.
- newInterval.length == 2
- 0 <= start <= end <= 105

---

## 题目（中文翻译）

给定一个 **不重叠的区间（non-overlapping intervals）** 数组 `intervals`，其中 `intervals[i] = [start_i, end_i]` 表示第 `i` 个区间的起点和终点，且数组已按照 `start_i` **升序排列（sorted in ascending order by start_i）**。同时给定一个区间 `newInterval = [start, end]`，表示另一个区间的起点和终点。

将 `newInterval` 插入到 `intervals` 中，使得插入后仍然 **按 `start_i` 升序排列（sorted in ascending order by start_i）**，并且 **不存在重叠的区间（merge overlapping intervals if necessary）**。返回插入后的区间数组。

> 需要注意的是，你不必原地修改 `intervals`，可以创建一个新数组并返回。

## 示例

### 示例 1
**输入**  
`intervals = [[1,3],[6,9]], newInterval = [2,5]`

**输出**  
`[[1,5],[6,9]]`

### 示例 2
**输入**  
`intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]`

**输出**  
`[[1,2],[3,10],[12,16]]`

**解释**  
新的区间 `[4,8]` 与 `[3,5]、[6,7]、[8,10]` 均有重叠，需要将它们合并。

## 约束条件

- `0 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^5`
- `intervals` 已按 `start_i` **升序排列（sorted by start_i in ascending order）**
- `newInterval.length == 2`
- `0 <= start <= end <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**先把新区间插进去，再把所有区间整体重新合并**。  
具体步骤：

1. **把 newInterval 加到原数组的合适位置**。因为原数组已经按照左端点 `start` 排好序，只要遍历一次找到第一个 `start` 大于 `newInterval[0]` 的位置，就可以用 `list.insert` 把它插进去。这里可以把“找位置”想象成在排好序的书架上找空位，顺序查找就像从左到右逐本检查。

2. **遍历一次完整的区间列表，合并所有重叠的区间**。合并的办法很像把相邻的两块拼图放在一起：如果当前区间的左端点 ≤ 前一个区间的右端点，就说明它们有交集，需要把它们合并成 `[min(prev_start, cur_start), max(prev_end, cur_end)]`，否则就把前一个区间直接加入答案列表。

这样做一定能得到正确答案，因为我们先保证了所有区间都在同一个列表里，然后把所有可能重叠的区间都合并掉，最后的列表自然满足“非重叠且按左端点升序”。

**为什么是对的？**  
- 插入后列表仍然是**全部区间的集合**（包括新加入的），只不过顺序可能不再严格升序。  
- 合并过程遍历一次并把所有相交的区间合并成一个，等价于把所有“重叠的块”压缩成一块，最后剩下的每块之间必然不相交。

#### 代码（Python）

```python
from typing import List

def insert_bruteforce(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    # 1. 把 newInterval 插入到合适的位置（线性搜索）
    inserted = False
    merged = []                     # 最终返回的列表
    for i, cur in enumerate(intervals):
        if not inserted and cur[0] > newInterval[0]:
            merged.append(newInterval)   # 插入新区间
            inserted = True
        merged.append(cur)               # 把原来的区间加进来
    if not inserted:                      # newInterval 比所有区间都靠右
        merged.append(newInterval)

    # 2. 再遍历一次把所有可能的重叠区间合并
    res = []
    for interval in merged:
        # 如果 res 为空或当前区间与上一个区间不相交，直接加入
        if not res or interval[0] > res[-1][1]:
            res.append(interval)
        else:
            # 有交集，合并：左端点取最小，右端点取最大
            res[-1][1] = max(res[-1][1], interval[1])
    return res
```

#### 复杂度

- **时间复杂度**：`O(n)`（两次线性遍历，`n` 为原数组长度）  
  - 大白话：如果有 10,000 条区间，我们最多检查 20,000 次（插入一次 + 合并一次），这仍然是“随输入规模线性增长”，不像 `O(n²)` 那样会出现“几万条数据就卡死”的情况。

- **空间复杂度**：`O(n)`（创建了一个新的列表 `merged`，最坏情况保存了 `n+1` 条区间）  
  - 大白话：我们额外用了和原数组差不多多的空间，和输入规模成正比。

---

### 2. 最优解

#### 思路  

虽然上面的“暴力”已经是线性时间 `O(n)`，但我们可以**在一次遍历中同时完成插入与合并**，省掉一次额外的遍历和额外的列表拷贝。  
核心观察：

- 原数组已经是**有序且不重叠**的区间。  
- 我们只需要把 `newInterval` 按照左端点插入到合适的位置，同时把所有与 `newInterval` 重叠的区间一起合并。  
- 只要遍历一次，**三种情况**可以一次处理完：

  1. **当前区间在 newInterval 左边且不相交**（`interval.end < new.start`）  
     → 直接加入答案，因为它们肯定不会受后面插入的影响。

  2. **当前区间在 newInterval 右边且不相交**（`interval.start > new.end`）  
     → 说明所有需要合并的区间都已经处理完，先把已经合并好的 `newInterval` 加入答案，然后把剩下的区间全部原样加入。

  3. **当前区间与 newInterval 有交集**（两者有重叠）  
     → 把它们合并成一个更大的区间：  
        `new.start = min(new.start, interval.start)`  
        `new.end   = max(new.end,   interval.end)`  
     → 继续遍历，后面的区间可能仍然与这个“扩大的” `newInterval` 重叠。

把这三种情况写成代码，就是**一次遍历完成插入 + 合并**的最优解。

> **类比**：想象把一根绳子（`newInterval`）插进若干已经排好队的绳子（`intervals`）中，如果遇到相邻的绳子可以搭接，就把它们绑在一起形成更长的绳子，直到再也找不到可以搭接的为止。整个过程只需要从左到右检查一次。

#### 代码（Python）

```python
from typing import List

def insert(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    res = []                     # 最终结果
    i = 0
    n = len(intervals)

    # 1️⃣ 把所有在 newInterval 左侧且不相交的区间直接加入结果
    while i < n and intervals[i][1] < newInterval[0]:
        res.append(intervals[i])
        i += 1

    # 2️⃣ 合并所有与 newInterval 有交集的区间
    #    （包括 newInterval 本身，因为它可能会被“扩展”）
    while i < n and intervals[i][0] <= newInterval[1]:
        # 更新 newInterval 为两者的并集
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    # 合并完成后，把合并后的 newInterval 加入结果
    res.append(newInterval)

    # 3️⃣ 把剩余的、全部在 newInterval 右侧且不相交的区间直接加入
    while i < n:
        res.append(intervals[i])
        i += 1

    return res
```

> 关键行中文注释已在代码中标出，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n)`（只遍历一次）  
  - 与暴力解相比，省掉了第二次遍历和一次额外的列表拷贝，真正做到“一趟搞定”。  
  - 大白话：不管有 10,000 条区间，最多检查 10,000 次，速度和输入规模成正比。

- **空间复杂度**：`O(n)`（返回的列表需要存放所有区间）  
  - 这里没有额外的中间列表，唯一的额外空间是答案本身，和输入规模相同。

---

## 心得

- **核心技巧**：**一次遍历 + 分类讨论**（左侧不相交、重叠合并、右侧不相交）。  
- **适用的题型**：
  1. “合并区间”类（LeetCode 56 Merge Intervals）。  
  2. “区间插入/删除”类（如 435 Non-overlapping Intervals）。  
  3. “区间覆盖查询”类（需要对有序区间进行快速定位）。
- **一句话总结解题钥匙**：**先把左侧安全区间输出，再把所有能碰到的区间合并成一个，最后输出右侧安全区间**。

---

## 反思

- **第一反应**：看到“插入+合并”，自然想到“先插再合并”，即暴力解的思路。  
- **最容易踩的坑**：
  - 忘记处理 **空数组**（`intervals = []`）的情况。  
  - 边界条件写错：如 `interval[i][1] < new[0]` 与 `interval[i][0] > new[1]` 的严格/非严格比较会导致漏掉相邻但不重叠的区间。  
  - 合并时忘记更新 `newInterval` 的左端点或右端点，导致后面的区间仍被错误地当作不相交处理。
- **下次类似题的第一步**：**先把所有“肯定不需要合并”的区间挑出来（左侧或右侧），剩下的必然是需要合并的区间**，然后再统一处理。这样可以快速定位瓶颈并避免不必要的遍历。