# #3439. 重新安排会议以获得最大空闲时间 I / Reschedule Meetings for Maximum Free Time I

> 难度：中等 · 标签：Array、Greedy、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/reschedule-meetings-for-maximum-free-time-i/)

---

## 题目（英文原版）

**Description**

You are given an integer eventTime denoting the duration of an event, where the event occurs from time t = 0 to time t = eventTime.
You are also given two integer arrays startTime and endTime, each of length n. These represent the start and end time of n non-overlapping meetings, where the ith meeting occurs during the time [startTime[i], endTime[i]].
You can reschedule at most k meetings by moving their start time while maintaining the same duration, to maximize the longest continuous period of free time during the event.
The relative order of all the meetings should stay the same and they should remain non-overlapping.
Return the maximum amount of free time possible after rearranging the meetings.
Note that the meetings can not be rescheduled to a time outside the event.

**Examples**

**Example 1:**

```
Input: eventTime = 5, k = 1, startTime = [1,3], endTime = [2,5]
Output: 2
Explanation:

Reschedule the meeting at [1, 2] to [2, 3] , leaving no meetings during the time [0, 2] .
```

**Example 2:**

```
Input: eventTime = 10, k = 1, startTime = [0,2,9], endTime = [1,4,10]
Output: 6
Explanation:

Reschedule the meeting at [2, 4] to [1, 3] , leaving no meetings during the time [3, 9] .
```

**Example 3:**

```
Input: eventTime = 5, k = 2, startTime = [0,1,2,3,4], endTime = [1,2,3,4,5]
Output: 0
Explanation:
There is no time during the event not occupied by meetings.
```

**Constraints**

- 1 <= eventTime <= 109
- n == startTime.length == endTime.length
- 2 <= n <= 105
- 1 <= k <= n
- 0 <= startTime[i] < endTime[i] <= eventTime
- endTime[i] <= startTime[i + 1] where i lies in the range [0, n - 2].

---

## 题目（中文翻译）

**描述**  
给定一个整数 `eventTime`，表示活动的持续时间，活动从时间 `t = 0` 开始，持续到 `t = eventTime`。  
再给定两个长度均为 `n` 的整数数组 `startTime` 和 `endTime`，分别表示 `n` 场**不重叠的会议（non-overlapping meetings）**的开始时间和结束时间，其中第 `i` 场会议的时间区间为 `[startTime[i], endTime[i]]`。  

你可以**最多**重新安排 `k` 场会议的开始时间，保持每场会议的时长不变，以使活动期间**最长的连续空闲时间**达到最大。  
重新安排后，所有会议的相对顺序必须保持不变，且仍然**不重叠（non-overlapping）**。  
会议的时间不能超出活动的范围 `[0, eventTime]`。  

返回重新安排会议后能够得到的**最大空闲时间**。  

**示例**  

示例 1:  
Input: eventTime = 5, k = 1, startTime = [1,3], endTime = [2,5]  
Output: 2  
Explanation:  
将 `[1, 2]` 这场会议重新安排到 `[2, 3]`，如此在 `[0, 2]` 时间段内没有任何会议，得到最长空闲时间为 2。  

示例 2:  
Input: eventTime = 10, k = 1, startTime = [0,2,9], endTime = [1,4,10]  
Output: 6  
Explanation:  
将 `[2, 4]` 这场会议重新安排到 `[1, 3]`，如此在 `[3, 9]` 时间段内没有会议，得到最长空闲时间为 6。  

示例 3:  
Input: eventTime = 5, k = 2, startTime = [0,1,2,3,4], endTime = [1,2,3,4,5]  
Output: 0  
Explanation:  
整个活动期间均被会议占满，无法得到空闲时间。  

**约束条件**  
- `1 <= eventTime <= 10^9`  
- `n == startTime.length == endTime.length`  
- `2 <= n <= 10^5`  
- `1 <= k <= n`  
- `0 <= startTime[i] < endTime[i] <= eventTime`  
- `endTime[i] <= startTime[i + 1]`（对所有 `0 <= i <= n-2`）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一次可移动的会议都枚举所有可能的移动位置**，然后在每一种安排下计算事件期间最长的连续空闲时间，最后取最大值。

- **数据结构**：我们只需要几个普通的 Python 列表。  
  - `start`、`end` 保存每个会议的起止时间。  
  - `gap` 用来存放相邻会议之间的空档（类似字典里查词的“词条”，这里的“词条”是两个会议之间的距离）。

- **为什么正确**：因为我们把“所有可能的安排”都遍历了一遍，答案必然在其中。只要在每一种合法安排下正确计算空闲时长，就一定能得到全局最优。

- **时间/空间复杂度**：  
  - 对每个会议我们都要尝试把它向左或向右移动到**所有**可能的位置。若有 `n` 场会议，最多要检查 `O(eventTime)`（事件总时长）个位置，整体时间复杂度会是 `O(n * eventTime)`。  
  - `eventTime` 最多可达 `10^9`，这在实际运行中相当于 **十亿次循环**，显然会超时。  
  - 空间上只需要存放原始数组和若干临时变量，`O(n)` 的空间即可。

> **大白话解释**：  
> - `O(n²)` 的意思是“如果把 `n` 当成 10，工作量大约是 10×10=100；如果 `n` 是 100，工作量是 100×100=10 000”。这里的 `O(n * eventTime)` 更可怕，因为 `eventTime` 可能是十亿，意味着即使 `n` 只有 10，工作量也会是 10 × 10⁹ = 10 000 000 000 次——电脑根本跑不完。

#### 代码（Python）

```python
def maxFreeTime_bruteforce(eventTime: int, k: int,
                           startTime: list[int], endTime: list[int]) -> int:
    n = len(startTime)
    # 计算每场会议的时长，后面移动时保持不变
    duration = [endTime[i] - startTime[i] for i in range(n)]

    best = 0                                 # 记录最大的空闲时长
    # 对每一种选取最多 k 场需要移动的会议的组合进行遍历（这里用递归暴力枚举）
    def dfs(idx: int, moved: int, cur_start: list[int]):
        nonlocal best
        if idx == n:                         # 已处理完所有会议
            # 计算当前安排下的最长空闲区间
            prev_end = 0
            max_gap = 0
            for s, e in zip(cur_start, [cur_start[i] + duration[i] for i in range(n)]):
                max_gap = max(max_gap, s - prev_end)   # 前后会议之间的空档
                prev_end = e
            max_gap = max(max_gap, eventTime - prev_end)  # 事件结束后的空档
            best = max(best, max_gap)
            return

        # 情况 1：不移动第 idx 场会议
        dfs(idx + 1, moved, cur_start + [startTime[idx]])

        # 情况 2：如果还有剩余的可移动次数，尝试把它向左/右移动到所有合法位置
        if moved < k:
            # 可以向左移动的最早起点是前一场会议的结束时间（或 0）
            left_limit = cur_start[-1] + duration[idx - 1] if idx > 0 else 0
            # 可以向右移动的最晚起点是后面会议的开始时间（或 eventTime）
            right_limit = startTime[idx + 1] - duration[idx] if idx < n - 1 else eventTime - duration[idx]
            for new_start in range(left_limit, right_limit + 1):
                dfs(idx + 1, moved + 1, cur_start + [new_start])

    dfs(0, 0, [])
    return best
```

> **注释说明**  
> - `duration` 保存每场会议的固定时长，移动时不改变。  
> - `dfs` 用深度优先搜索枚举所有“搬不搬”以及搬到哪个位置的组合。  
> - `left_limit`、`right_limit` 确保移动后仍保持会议不重叠且在事件区间内。  
> - 最后遍历完所有可能后 `best` 就是答案。

#### 复杂度

- **时间复杂度**：`O( C(n, ≤k) * eventTime )`（指数级），实际会因为 `eventTime` 过大而不可接受。  
- **空间复杂度**：`O(n)`，主要是递归栈和临时列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈**在于我们把每个会议都尝试所有可能的起点。其实我们并不需要知道每一次具体怎么移动，只需要知道 **把哪些连续的会议整体向左/向右压缩后，空出的间隙会有多大**。

关键观察：

1. **会议之间的空档（gap）是固定的**。  
   - 设 `gap[i] = startTime[i+1] - endTime[i]`，即第 `i` 场会议结束后到第 `i+1` 场会议开始前的空闲时长。  
   - 只要不移动这两场之间的相对顺序，这些 gap 的值在原始安排里是确定的。

2. **如果我们把一段连续的 `K+1` 场会议整体往左移动（或往右移动），它们之间的 gap 都会被“压缩”掉**，只剩下这段会议左侧的空档和右侧的空档。  
   - 想象把几块书往左挪，书之间的空隙会消失，只留下左边的书架空位和右边的书架空位。  

3. **最多可以移动 `k` 场会议**，而一次“整体移动”会涉及 `K+1` 场会议（因为移动 `K` 场会议会把它们与前后两端的 gap 合并），于是我们只需要在 **所有长度为 `K+1` 的连续会议子数组** 中，找出 **它们内部 gap 的总和** 的最大值。  
   - 这个最大内部 gap，就是我们可以“省掉”的空闲时间。  
   - 原始总空闲时间 = `eventTime - sum(durations)`（所有会议占用的时间）。  
   - 最终答案 = 原始空闲时间 + **最大可省掉的 gap**。

4. **滑动窗口**可以在 `O(n)` 时间内求出每个长度为 `K+1` 子数组的 gap 和。  
   - 窗口左端 `l`，右端 `r = l + K`（因为窗口包含 `K+1` 场会议）。  
   - 当窗口向右滑动一步时，只需要把 `gap[l]` 移出、把 `gap[r]` 加入，总和更新 `O(1)`。

**完整步骤**：

- 预处理出每场会议的时长 `len[i] = endTime[i] - startTime[i]`，以及相邻会议之间的 gap `gap[i]`（长度为 `n-1`）。
- 计算 `totalBusy = sum(len)`，`totalFree = eventTime - totalBusy`（事件里原始的空闲时长）。
- 若 `k >= n`（可以移动所有会议），则可以把所有会议堆到最左侧或最右侧，空闲时长直接等于 `eventTime - totalBusy`（因为没有内部 gap 可以再省），此时答案 = `eventTime - totalBusy`（即 `totalFree`）。
- 使用滑动窗口遍历所有长度为 `k+1` 的会议序列，累计窗口内的 `gap` 总和，记录最大值 `max_gap_inside`。
- 最终答案 = `totalFree + max_gap_inside`。

> **类比**：  
> 把会议想象成一列火车车厢，每节车厢之间有若干空隙（gap）。我们有一次“调车”机会，可以把至多 `k` 节车厢一起往前推，使它们之间的空隙全部消失，只剩下推前后两端的空白。我们想让整个车站（事件）里出现最长的无人轨道（空闲时间），于是只需要找出哪段连续的 `k+1` 节车厢之间的空隙最多，推走它们就能得到最长的空轨。

#### 代码（Python）

```python
def maxFreeTime(eventTime: int, k: int,
                startTime: list[int], endTime: list[int]) -> int:
    n = len(startTime)

    # 1️⃣ 计算每场会议的时长
    durations = [endTime[i] - startTime[i] for i in range(n)]
    total_busy = sum(durations)               # 会议总占用时间
    total_free = eventTime - total_busy        # 事件原始的空闲时间

    # 2️⃣ 计算相邻会议之间的空档（gap），长度为 n-1
    gaps = [startTime[i + 1] - endTime[i] for i in range(n - 1)]

    # 3️⃣ 特殊情况：如果 k >= n，所有会议都可以挤在一起，内部 gap 全部可以消除
    #    此时最大空闲仍是 total_free，因为已经没有内部 gap 可再“省掉”
    if k >= n:
        return total_free

    # 4️⃣ 滑动窗口：窗口长度为 k+1 场会议 → 包含 k 条 gap
    window_len = k + 1               # 会议数
    gap_window_len = window_len - 1  # 对应的 gap 数量

    # 初始化窗口内的 gap 和
    cur_sum = sum(gaps[:gap_window_len]) if gap_window_len > 0 else 0
    max_inside = cur_sum                     # 记录最大的内部 gap 和

    # 窗口左端 l 从 0 移动到 n - window_len
    for l in range(1, n - window_len + 1):
        # 移除左侧离开的 gap
        cur_sum -= gaps[l - 1]
        # 加入新进入的右侧 gap
        cur_sum += gaps[l + gap_window_len - 1]
        # 更新最大值
        if cur_sum > max_inside:
            max_inside = cur_sum

    # 5️⃣ 结果 = 原始空闲 + 能够“省掉”的内部 gap
    return total_free + max_inside
```

> **代码注释**  
> - 第 1 步把每场会议的固定时长算出来，后面移动时不需要再次计算。  
> - 第 2 步把相邻会议之间的空档保存为 `gaps`，这就是我们后面要“压缩”的对象。  
> - 第 4 步的滑动窗口只在 `gaps` 上移动，窗口宽度为 `k`（因为 `k+1` 场会议之间恰好有 `k` 条 gap）。  
> - `max_inside` 保存的是 **可以一次性消除的最大空档总和**。  
> - 最终答案把这部分空档加回原始空闲时间，即得到最长的连续自由时段。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历了一遍 `startTime/endTime` 计算时长和 gap，随后一次线性滑动窗口遍历所有窗口。  
  - 与暴力解的指数级时间相比，快得多。

- **空间复杂度**：`O(n)`（存放 `durations` 与 `gaps` 两个长度为 `n` 的数组）。  
  - 只用了常数级的额外变量，符合题目要求。

---

## 心得

- **核心技巧**：把“最多移动 k 场会议”转化为“在长度为 k+1 的连续会议子序列中，最大化内部空档的和”。这是一种**滑动窗口 + 贪心**的思路。  
- **适用的题型**：  
  1. “在数组中找长度为 K 的子数组，使其和最大”——典型的滑动窗口。  
  2. “把最多 K 次操作用于压缩间隙”——如 **Reschedule Meetings for Maximum Free Time II**（变体）。  
  3. “在不改变相对顺序的前提下，使用 K 次移动合并区间”——比如 **Maximum Consecutive Ones After Flipping K Zeros**（把 0 翻成 1）。
- **一句话总结解题钥匙**：**把可移动的会议整体视作一个整体，用滑动窗口直接统计它们之间可以“省掉”的空隙，总和最大即为答案**。

---

## 反思

- **第一反应**：看到“最多移动 k 场会议”，立刻想到**枚举每场会议的所有可能位置**，这会导致指数级搜索。  
- **最容易踩的坑**：  
  - 忘记**保持会议的相对顺序**，导致窗口内部的会议被重新排列，从而产生非法安排。  
  - 边界条件：`k = n`（可以移动全部会议）时，窗口长度为 `n+1` 超出数组范围，需要单独处理。  
  - 当 `gap_window_len = 0`（即 `k = 0`）时，滑动窗口应直接返回原始空闲时间，防止取 `gaps[:0]` 产生空列表导致错误。  
- **下次类似题的第一步**：先**把“操作次数”映射到“连续子数组的长度”，检查是否可以用**滑动窗口**一次遍历得到所需的最大/最小值**，而不是直接枚举所有操作细节。