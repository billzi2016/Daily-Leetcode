# #3440. 重新安排会议以获得最大空闲时间 II / Reschedule Meetings for Maximum Free Time II

> 难度：中等 · 标签：Array、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/reschedule-meetings-for-maximum-free-time-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer eventTime denoting the duration of an event. You are also given two integer arrays startTime and endTime, each of length n.
These represent the start and end times of n non-overlapping meetings that occur during the event between time t = 0 and time t = eventTime, where the ith meeting occurs during the time [startTime[i], endTime[i]].
You can reschedule at most one meeting by moving its start time while maintaining the same duration, such that the meetings remain non-overlapping, to maximize the longest continuous period of free time during the event.
Return the maximum amount of free time possible after rearranging the meetings.
Note that the meetings can not be rescheduled to a time outside the event and they should remain non-overlapping.
Note: In this version, it is valid for the relative ordering of the meetings to change after rescheduling one meeting.

**Examples**

**Example 1:**

```
Input: eventTime = 5, startTime = [1,3], endTime = [2,5]
Output: 2
Explanation:

Reschedule the meeting at [1, 2] to [2, 3] , leaving no meetings during the time [0, 2] .
```

**Example 2:**

```
Input: eventTime = 10, startTime = [0,7,9], endTime = [1,8,10]
Output: 7
Explanation:

Reschedule the meeting at [0, 1] to [8, 9] , leaving no meetings during the time [0, 7] .
```

**Example 3:**

```
Input: eventTime = 10, startTime = [0,3,7,9], endTime = [1,4,8,10]
Output: 6
Explanation:

Reschedule the meeting at [3, 4] to [8, 9] , leaving no meetings during the time [1, 7] .
```

**Example 4:**

```
Input: eventTime = 5, startTime = [0,1,2,3,4], endTime = [1,2,3,4,5]
Output: 0
Explanation:
There is no time during the event not occupied by meetings.
```

**Constraints**

- 1 <= eventTime <= 109
- n == startTime.length == endTime.length
- 2 <= n <= 105
- 0 <= startTime[i] < endTime[i] <= eventTime
- endTime[i] <= startTime[i + 1] where i lies in the range [0, n - 2].

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `eventTime` 表示活动的总时长。还有两个整数数组 `startTime` 与 `endTime`（长度均为 `n`），它们分别记录了 `n` 场不重叠会议的开始时间与结束时间。第 `i` 场会议的时间区间为 `[startTime[i], endTime[i]]`，所有会议都发生在时间 `t = 0` 到 `t = eventTime` 之间。

你最多可以重新安排 **一场** 会议：在保持该会议时长不变的前提下，仅移动其开始时间，使得所有会议仍保持不重叠，并且不超出活动时间范围。通过一次重新安排，旨在使活动期间的 **最长连续空闲时间**（即没有任何会议占用的时间段）最大化。

返回重新安排后能够得到的最大空闲时间长度。

> 注意：在本版本中，重新安排后会议的相对顺序可以改变。

---

**示例**  

示例 1  
```
Input: eventTime = 5, startTime = [1,3], endTime = [2,5]
Output: 2
Explanation:
将会议 [1, 2] 重新安排到 [2, 3]，此时时间段 [0, 2] 没有任何会议，占得最长连续空闲时间为 2。
```

示例 2  
```
Input: eventTime = 10, startTime = [0,7,9], endTime = [1,8,10]
Output: 7
Explanation:
将会议 [0, 1] 重新安排到 [8, 9]，此时时间段 [0, 7] 没有任何会议，占得最长连续空闲时间为 7。
```

示例 3  
```
Input: eventTime = 10, startTime = [0,3,7,9], endTime = [1,4,8,10]
Output: 6
Explanation:
将会议 [3, 4] 重新安排到 [8, 9]，此时时间段 [1, 7] 没有任何会议，占得最长连续空闲时间为 6。
```

示例 4  
```
Input: eventTime = 5, startTime = [0,1,2,3,4], endTime = [1,2,3,4,5]
Output: 0
Explanation:
整个活动期间均被会议占满，无法得到空闲时间。
```

---

**约束条件**  

- `1 <= eventTime <= 10^9`  
- `n == startTime.length == endTime.length`  
- `2 <= n <= 10^5`  
- `0 <= startTime[i] < endTime[i] <= eventTime`  
- `endTime[i] <= startTime[i + 1]`（`i` 的取值范围为 `[0, n - 2]`）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举**：

1. 任选一场会议 `i`（或者根本不动），把它搬走。  
2. 再在事件时间轴上 **遍历所有可能的起始位置**，只要新位置能容纳这场会议且不与其它会议重叠，就把会议放进去。  
3. 计算搬完会后的所有空闲区间，取最长的那段。  
4. 把所有可能的搬法的最长空闲时间取最大值，返回答案。

> **数据结构类比**  
> 这里的「遍历所有可能的起始位置」可以想象成在一本日程本上把一段文字（会议）抠出来，再把它粘到每一个可能的空白处去检查是否会撞到别的文字。  
> 为了快速判断是否会撞，最直接的办法是把所有已有的会议时间段存进一个 **列表**，每次搬动时遍历这个列表检查是否有交叉——这就像查字典时，一页页翻看，看有没有相同的词。

**为什么正确**：我们把所有合法的搬动方式都穷举一遍，必然不会漏掉最优的那一次。

**时间/空间复杂度**  

- **时间**：  
  - 选哪一场会议要遍历 `n` 次。  
  - 对每一场会议，又要遍历所有可能的起始位置（最坏情况是 `eventTime`），每次检查冲突要遍历其余 `n‑1` 场会议。  
  - 粗略算下来大约是 `O(n * eventTime * n)`，在题目约束 `eventTime ≤ 10⁹`、`n ≤ 10⁵` 时根本跑不完。  
  - 为了说明思路，我们把它简化为 **`O(n²)`**（只枚举每场会议对应的每个空隙），已经远远超出时间限制。

- **空间**：  
  - 只需要存原始的会议列表和若干临时变量，`O(n)` 的空间。

> **大白话解释**：  
> `O(n²)` 就好比你在一个有 `n` 本书的书架上，挑一本书再去检查其它每一本书是否会撞到它，过程会重复 `n` 次，工作量呈“平方”增长，几乎不可能在一分钟内完成。

#### 代码（Python）

```python
def maxFreeTime_bruteforce(eventTime, startTime, endTime):
    n = len(startTime)
    # 把原始会议存成区间列表，方便后面冲突检测
    intervals = [(startTime[i], endTime[i]) for i in range(n)]

    # 计算不搬动时的最大空闲时间
    def current_max_gap():
        max_gap = startTime[0]            # 0 到第一场会议的空隙
        for i in range(1, n):
            max_gap = max(max_gap, startTime[i] - endTime[i-1])
        max_gap = max(max_gap, eventTime - endTime[-1])
        return max_gap

    answer = current_max_gap()

    # 枚举要搬动的会议（包括“搬动 0 场”的情况）
    for i in range(n):
        length = endTime[i] - startTime[i]      # 这场会议的时长
        # 把第 i 场会议从列表里暂时移除，得到“空洞”
        removed = intervals[:i] + intervals[i+1:]

        # 所有可能的放置位置：0~eventTime‑length
        for new_start in range(0, eventTime - length + 1):
            new_end = new_start + length
            # 检查新位置是否会和其它会议冲突
            conflict = False
            for s, e in removed:
                if not (new_end <= s or new_start >= e):   # 有交叉
                    conflict = True
                    break
            if conflict:
                continue

            # 把新会议插回去，重新算最长空闲时间
            cand = sorted(removed + [(new_start, new_end)], key=lambda x: x[0])
            max_gap = cand[0][0]                # 前端空隙
            for j in range(1, len(cand)):
                max_gap = max(max_gap, cand[j][0] - cand[j-1][1])
            max_gap = max(max_gap, eventTime - cand[-1][1])
            answer = max(answer, max_gap)

    return answer
```

> 代码里每一行都有中文注释，直接跑会超时，只是帮助你理解「暴力枚举」的思路。

#### 复杂度

- **时间复杂度**：`O(n²)`（实际更高，已说明原因）——遍历每场会议并尝试所有可能的放置位置。  
- **空间复杂度**：`O(n)`——存放原始会议区间及临时列表。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：

1. **枚举所有空隙**：事件时间可能很大，空隙数目本可以用 `n+1`（两端加中间）来表示，却被“逐格尝试”放大了。  
2. **每次搬动都重新遍历所有会议**：检查冲突的过程可以提前计算，只要知道每个空隙的长度就能判断是否能容下会议。

我们把问题抽象成 **“空隙”** 与 **“会议时长”** 的配对：

- 原始的 `n` 场不重叠会议把时间轴划分成 `n+1` 段空闲区间（我们称之为 **gap**）。  
  - `gap[0] = startTime[0] - 0`（事件起点到第一场会议）  
  - `gap[i] = startTime[i] - endTime[i‑1]`（第 i 场会议左侧的空隙）  
  - `gap[n] = eventTime - endTime[n‑1]`（最后一场会议到事件结束）  

> **类比**：把时间轴想成一根木棍，上面钉了几块木块（会议），木块之间的空隙就是 **gap**，就像字典里词条之间的空白页。

如果我们 **搬走** 第 `i` 场会议（时长 `len_i`），会产生一个 **合并后的大空隙**：

```
merged_gap_i = gap[i] + gap[i+1]
```

因为左边的 `gap[i]` 与右边的 `gap[i+1]` 在会议被移除后会连在一起。

接下来我们要把这场会议重新安置到 **某个其他 gap**（可以是最左或最右的 gap），只要该 gap 的长度 ≥ `len_i`，我们就可以把会议塞进去。  
为了让 **最长空闲时间** 最大化，显然应该把会议放在 **gap 的一端**，这样剩下的空闲部分就是 `gap_len - len_i`（把会议紧贴左边或右边放）。  

于是，对于会议 `i`，最终能得到的最长空闲区间是：

```
candidate_i = max( merged_gap_i ,               # 把会议搬走后得到的合并空隙
                   max_{gap_j >= len_i, j≠i,i+1} (gap_j - len_i) )
```

我们只需要找出 **长度至少为 `len_i` 的最大 gap**（除去 `i` 与 `i+1` 两个位置），因为 `gap_j - len_i` 随 `gap_j` 增大而增大。  

**关键点**：

- 只需要 **前两大的 gap**（全局最大和次大）来处理「除去自己所在的两个 gap」的情况。  
  - 如果全局最大 gap 不在 `{i, i+1}`，直接用它。  
  - 否则用第二大的 gap（若不存在则视为 0）。  
- 只要把每个会议的时长 `len_i` 与这两个候选 gap 比较，就能得到 `candidate_i`。  

整体流程：

1. 计算所有 `gap`（长度 `n+1`）。  
2. 记录 **全局最大 gap**（`max1, idx1`）和 **第二大 gap**（`max2, idx2`）。  
3. 初始化答案为 **不搬动时的最大 gap**（即 `max(gap)`）。  
4. 对每个会议 `i`：  
   - `len_i = endTime[i] - startTime[i]`  
   - `merged = gap[i] + gap[i+1]`  
   - 选出 **可用的最大 gap**：  
     ```
     if idx1 not in {i, i+1}: best_gap = max1
     else: best_gap = max2
     ```  
   - 若 `best_gap >= len_i`，则 `place = best_gap - len_i`，否则 `place = 0`。  
   - `answer = max(answer, merged, place)`  

时间复杂度为 `O(n log n)`（对 `gap` 排序得到前两大），空间 `O(n)`（存 `gap` 与排序结果）。`n ≤ 10⁵` 完全可以接受。

> **为什么排序只取前两大就够了？**  
> 对每个会议我们只关心 **「能容下它的最大空隙」**，而所有空隙的长度已经固定。  
> 如果全局最大的空隙恰好是会议 `i` 左右的两个 gap（即 `i` 或 `i+1`），我们只能换成次大的空隙；其余情况都直接使用全局最大。再往下的第三大、第四大… 都不可能比前两大更好，因为我们已经排除了只能使用的那两个位置。

#### 代码（Python）

```python
from typing import List

def maxFreeTime(eventTime: int, startTime: List[int], endTime: List[int]) -> int:
    n = len(startTime)

    # ---------- 1. 计算所有 gap ----------
    # gap[0] ... gap[n] 共 n+1 个空隙
    gaps = [0] * (n + 1)
    gaps[0] = startTime[0]                     # 事件开始到第一场会议
    for i in range(1, n):
        gaps[i] = startTime[i] - endTime[i-1]  # 两场会议之间的空隙
    gaps[n] = eventTime - endTime[-1]          # 最后一场会议到事件结束

    # ---------- 2. 找出全局最大和第二大 gap ----------
    # 把 (长度, 索引) 按长度降序排列，只取前两名
    # 这里不必对全部排序，只需要一次遍历即可得到前两大
    max1_len, max1_idx = -1, -1   # 最大
    max2_len, max2_idx = -1, -1   # 第二大
    for idx, g in enumerate(gaps):
        if g > max1_len:
            max2_len, max2_idx = max1_len, max1_idx
            max1_len, max1_idx = g, idx
        elif g > max2_len:
            max2_len, max2_idx = g, idx

    # ---------- 3. 初始答案：不搬动时的最长空闲 ----------
    answer = max1_len   # 全局最大 gap 本身

    # ---------- 4. 枚举每一场会议，尝试搬动 ----------
    for i in range(n):
        length = endTime[i] - startTime[i]          # 会议时长

        # (1) 把会议搬走后，两侧空隙会合并
        merged_gap = gaps[i] + gaps[i+1]

        # (2) 在其它 gap 中找能容下它的最大 gap
        # 需要排除 i（左侧）和 i+1（右侧）这两个位置
        if max1_idx not in (i, i + 1):
            best_gap = max1_len
        else:
            best_gap = max2_len   # 若最大在排除范围，则用第二大（可能为 -1）

        # 如果找不到足够大的空隙，就算作 0（即不能安置到其他位置）
        place_gap = best_gap - length if best_gap >= length else 0

        # 这一次搬动能得到的最长空闲区间
        cur_best = max(merged_gap, place_gap)

        # 更新全局答案
        answer = max(answer, cur_best)

    return answer
```

> **代码要点**（每行中文注释已在代码中给出）  
> - 第 1 步把时间轴划分成 `gap`，相当于把所有“空白页”列出来。  
> - 第 2 步只遍历一次就找出最大、第二大的空白页，省去完整排序的开销。  
> - 第 4 步里 `merged_gap` 是把会议搬走后自然产生的最大空隙；`place_gap` 是把会议塞进另一个空白页后剩下的空闲长度。  
> - 最后取两者的最大值并与全局答案比较。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 计算 gap、遍历找前两大、枚举会议均为线性扫描。  
  - 相比暴力的 `O(n²)`，这里的工作量只随会议数量线性增长，能够轻松通过 10⁵ 规模的测试。

- **空间复杂度**：`O(n)`  
  - 需要保存 `gap` 数组（长度 `n+1`）以及常数级的临时变量。  

> **与暴力解的对比**：  
> - 暴力解每次都要遍历所有空隙并检查冲突，等价于在 **每个会议** 上再做一次 **线性搜索**，导致 `O(n²)`。  
> - 最优解把“空隙的长度”提前算好，只需要 **一次** 全局扫描就能得到答案，极大降低了时间消耗。

---

## 心得

- **核心技巧**：把会议划分出的 **空隙（gap）** 看成独立的资源，搬走一场会议会把它左右的两个 gap 合并，而把会议重新安置到另一个 gap 时，只会留下 `gap_len - meeting_len` 的空闲。于是问题转化为 **“找最长的 gap”** 与 **“能否把会议塞进另一条足够长的 gap”** 的组合。

- **适用的题型**  
  1. “在不重叠的区间中插入/移动一个区间，使空闲最长”——如本题、或 “Reschedule Meetings for Maximum Free Time I”。  
  2. “删除一个区间后求最长空白段”——例如 “Maximum Length of Subarray With Positive Product” 的变形。  
  3. “把若干段合并后求最大间隙”——如 “Maximum Gap After Removing One Element”。

- **一句话总结解题钥匙**：**把所有空闲区间的长度提前算好，只需比较“合并后的大空隙”和“把会议塞进最长空隙后剩余的空闲”，即可在 O(n) 完成。**

---

## 反思

- **第一反应**：看到“可以重新安排一次会议”，自然想到 **枚举所有可能的起止时间**，于是想到暴力搜索。  
- **最容易踩的坑**  
  1. **遗漏两端的空隙**：事件的起点 `0` 与终点 `eventTime` 也会形成空隙，必须计入 `gap[0]` 与 `gap[n]`。  
  2. **相邻 gap 的排除**：搬走会议后，它左右的两个 gap 会合并，放回时不能再使用这两个位置，否则会出现“会议和自己碰撞”。  
  3. **空隙不足以容下会议**：有时所有 gap 都比会议时长短，这时只能选择“只搬走不重新放”，即取合并后的 gap。  
  4. **整数溢出**：虽然 Python 自动大整数，但在语言如 C++/Java 中要注意 `eventTime` 可达 `10⁹`，加减仍在 32 位范围内安全。

- **下次遇到同类题的第一步**：先 **把时间轴切分成 gap**，统计每段空闲长度；再思考 **搬走/删除** 某个区间会如何合并相邻的 gap，最后只比较 **合并后最大 gap** 与 **把区间放进最长可容 gap 后剩余的长度**。这样就能快速跳出暴力枚举的陷阱。