# #2589. 最小完成所有任务的时间 / Minimum Time to Complete All Tasks

> 难度：困难 · 标签：Array、Binary Search、Stack、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-complete-all-tasks/)

---

## 题目（英文原版）

**Description**

There is a computer that can run an unlimited number of tasks at the same time. You are given a 2D integer array tasks where tasks[i] = [starti, endi, durationi] indicates that the ith task should run for a total of durationi seconds (not necessarily continuous) within the inclusive time range [starti, endi].
You may turn on the computer only when it needs to run a task. You can also turn it off if it is idle.
Return the minimum time during which the computer should be turned on to complete all tasks.

**Examples**

**Example 1:**

```
Input: tasks = [[2,3,1],[4,5,1],[1,5,2]]
Output: 2
Explanation: 
- The first task can be run in the inclusive time range [2, 2].
- The second task can be run in the inclusive time range [5, 5].
- The third task can be run in the two inclusive time ranges [2, 2] and [5, 5].
The computer will be on for a total of 2 seconds.
```

**Example 2:**

```
Input: tasks = [[1,3,2],[2,5,3],[5,6,2]]
Output: 4
Explanation: 
- The first task can be run in the inclusive time range [2, 3].
- The second task can be run in the inclusive time ranges [2, 3] and [5, 5].
- The third task can be run in the two inclusive time range [5, 6].
The computer will be on for a total of 4 seconds.
```

**Constraints**

- 1 <= tasks.length <= 2000
- tasks[i].length == 3
- 1 <= starti, endi <= 2000
- 1 <= durationi <= endi - starti + 1

---

## 题目（中文翻译）

描述  
有一台电脑可以同时运行任意数量的任务。给定一个二维整数数组 `tasks`，其中 `tasks[i] = [start_i, end_i, duration_i]` 表示第 `i` 个任务必须在闭区间 `[start_i, end_i]` 内总共运行 `duration_i` 秒（不要求连续）。  

你只能在需要运行任务时打开电脑，空闲时可以关闭电脑。  
返回为了完成所有任务，电脑需要保持打开的最少时间总和。

示例  
示例 1  
输入: `tasks = [[2,3,1],[4,5,1],[1,5,2]]`  
输出: `2`  
解释:  
- 第一个任务可以在闭区间 `[2, 2]` 内运行。  
- 第二个任务可以在闭区间 `[5, 5]` 内运行。  
- 第三个任务可以在两个闭区间 `[2, 2]` 与 `[5, 5]` 内运行。  
电脑总共开启了 2 秒。

示例 2  
输入: `tasks = [[1,3,2],[2,5,3],[5,6,2]]`  
输出: `4`  
解释:  
- 第一个任务可以在闭区间 `[2, 3]` 内运行。  
- 第二个任务可以在闭区间 `[2, 3]` 与 `[5, 5]` 内运行。  
- 第三个任务可以在闭区间 `[5, 6]` 内运行。  
电脑总共开启了 4 秒。

约束条件  
- `1 <= tasks.length <= 2000`  
- `tasks[i].length == 3`  
- `1 <= start_i, end_i <= 2000`  
- `1 <= duration_i <= end_i - start_i + 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把时间轴上每一秒都看成一个**开关**：  
- “开” 表示这秒电脑是打开的，花费 1 秒的开启时间。  
- “关” 表示这秒电脑是关闭的，不计入时间。  

任务 `tasks[i] = [start_i, end_i, duration_i]` 的要求可以翻译成：**在区间 `[start_i, end_i]`（两端都算）里，必须至少有 `duration_i` 秒被标记为“开”。**  

于是我们可以把所有可能的开关组合（每秒是 0 还是 1）全部枚举，检查每个组合是否满足所有任务的要求，记录满足条件的组合中“开” 的总数最小的那个。  

> **类比**：把时间轴想象成一本字典，字典的每一页（秒）要么写上“打开”，要么不写。每个任务就像要求在某几页里出现至少 `duration_i` 次“打开”。我们要找到最少的“打开”页数，使所有任务的要求都被满足。

这种做法显然是**暴力**的：如果时间范围最大是 `T`（本题 `T ≤ 2000`），则有 `2^T` 种开关方式，远远超出计算能力。我们只把它作为教学示例，展示最原始的思考方式。

#### 代码（Python）

```python
from typing import List

def minTime_bruteforce(tasks: List[List[int]]) -> int:
    # 统计所有时间点的最小起点和最大终点
    min_time = min(s for s, _, _ in tasks)
    max_time = max(e for _, e, _ in tasks)

    T = max_time - min_time + 1          # 实际需要考虑的秒数
    best = float('inf')                  # 记录最小的打开时间

    # 使用递归枚举每一秒是开还是关（仅用于极小规模演示）
    def dfs(pos: int, on: List[int]):
        nonlocal best
        # 剪枝：已经超过当前最好的答案，就不必继续搜索
        if len(on) >= best:
            return
        # 所有秒都决定完了，检查是否满足所有任务
        if pos == T:
            # 检查每个任务
            for s, e, d in tasks:
                # 统计在该任务区间内被打开的秒数
                cnt = sum(1 for t in on if s <= t <= e)
                if cnt < d:               # 不满足
                    return
            best = len(on)                # 更新最优解
            return

        # 选“关” —— 不把当前秒加入 on 列表
        dfs(pos + 1, on)

        # 选“开” —— 把当前实际时间点加入 on 列表
        actual_time = min_time + pos
        dfs(pos + 1, on + [actual_time])

    dfs(0, [])
    return best if best != float('inf') else -1   # -1 表示无解（题目保证有解）

# 示例（仅用于验证思路，实际运行会非常慢）
# print(minTime_bruteforce([[2,3,1],[4,5,1],[1,5,2]]))
```

> **注意**：上面的递归会在 `T=10` 左右的情况下才算可接受，`T=2000` 时根本不可运行。这里的代码仅用于帮助大家体会“最笨的办法”。

#### 复杂度  

- **时间复杂度**：`O(2^T * N)`  
  - `2^T` 是所有可能的开关组合数（指数级），`N` 是任务数，用来检查每个组合是否满足所有任务。  
  - 用大白话说，就是“秒数每多 1，可能的情况就会翻一番”，所以在实际数据（最多 2000 秒）下根本不可能跑完。  
- **空间复杂度**：`O(T + N)`  
  - 递归栈深度为 `T`，另外要保存任务列表。  

> 由于暴力解不可行，我们需要寻找更聪明的办法。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以得到几个关键点：

1. **只关心哪些秒被打开**，而不必关心每秒打开的顺序。  
2. **任务之间可以共享打开的秒**，因为电脑可以并行运行任意数量的任务。  
3. 为了让后面的任务也能尽可能使用已有的打开秒，我们应该**把打开的秒安排得越靠后越好**（靠近任务的结束时间），这样它们更有可能落在后续任务的可用区间里。

这就引出了**贪心**思路：

- **先把任务按结束时间 `end` 从小到大排序**。  
  - 这样处理完的任务，其“已打开的秒”一定落在它们各自的区间的最右侧，对后面的任务影响最小。  
- 对每个任务，统计已经在它区间 `[start, end]` 里打开的秒数 `already`。  
- 若 `already >= duration`，说明已经满足，无需再打开新的秒。  
- 否则，需要再打开 `need = duration - already` 秒。**贪心地把这 `need` 秒放在区间的最右侧**，即从 `end` 往左依次检查，如果该秒还没有被打开，就打开它，直到满足 `need` 为止。  

> **类比**：把每个任务想象成一个“收集卡片”的活动，需要在指定的时间段内收集一定数量的卡片。我们把卡片（打开的秒）尽可能放在时间段的末尾，这样后面的活动还能顺手再拿到这些卡片，避免重复收集。

**为什么贪心是正确的？**  

- 设想我们对某个任务在区间 `[start, end]` 内选择了 `need` 秒的集合 `S`，其中有一个秒 `t` 不是最右侧的（即存在 `t' > t` 且 `t'` 仍在区间且未被选）。把 `t` 换成 `t'`，不增加任何额外的打开时间，且不会影响已经处理好的前面任务（因为它们的结束时间 ≤ `end`，而 `t'` 更靠右）。因此，**总有一种最优解把新打开的秒放在最右侧**。  
- 通过对任务按结束时间的顺序处理，后面的任务看到的已打开秒总是“尽可能靠右”，从而最大化共享。  

**实现细节**  

- 题目中时间范围最多到 `2000`，我们可以用一个长度为 `max_end + 1` 的布尔数组 `on[time]` 来标记哪些秒已经打开。  
- 为了快速统计已打开的秒数，可以在遍历每个任务时直接遍历 `[start, end]` 区间检查 `on[t]`，时间复杂度仍然在 `O(N * T)` 范围（`N ≤ 2000, T ≤ 2000`），即最多约 `4·10⁶` 次操作，完全可以接受。  

#### 代码（Python）

```python
from typing import List

def minTime(tasks: List[List[int]]) -> int:
    """
    贪心算法：
    1. 按结束时间升序排序
    2. 用一个布尔数组记录哪些秒已经打开
    3. 对每个任务，统计已打开的秒数，不足时从区间右端往左补齐
    """
    # 1️⃣ 按 end 排序
    tasks.sort(key=lambda x: x[1])          # x[1] 是 end

    max_end = max(e for _, e, _ in tasks)   # 计算时间轴的最大点
    on = [False] * (max_end + 1)            # on[t] = True 表示第 t 秒电脑已打开

    total_on = 0                            # 记录打开的秒数（答案）

    # 2️⃣ 逐个处理任务
    for start, end, dur in tasks:
        # 统计当前区间已经打开的秒数
        already = 0
        for t in range(start, end + 1):
            if on[t]:
                already += 1

        # 若已满足需求，直接进入下一个任务
        if already >= dur:
            continue

        # 需要再打开的秒数
        need = dur - already

        # 3️⃣ 从右往左补齐（贪心：尽可能靠后）
        t = end
        while need > 0 and t >= start:
            if not on[t]:               # 该秒还未被打开，就打开它
                on[t] = True
                total_on += 1
                need -= 1
            t -= 1

        # 题目保证一定有解，这里不再检查 need 是否为 0

    return total_on

# ---------- 示例 ----------
if __name__ == "__main__":
    print(minTime([[2,3,1],[4,5,1],[1,5,2]]))   # 输出 2
    print(minTime([[1,3,2],[2,5,3],[5,6,2]]))   # 输出 4
```

**代码要点解释**  

- `tasks.sort(key=lambda x: x[1])`：把任务按结束时间从小到大排好序。  
- `on = [False] * (max_end + 1)`：用数组模拟“字典”，下标就是时间点，`True` 表示那秒电脑已经打开。  
- `already` 的统计是一次线性扫描，时间很小（最多 2000 次）。  
- `while need > 0 and t >= start:`：从右端往左检查，如果该秒还未打开，就打开并计数，直到满足该任务的 `duration`。  

#### 复杂度  

- **时间复杂度**：`O(N * T)`  
  - `N` 为任务数（≤ 2000），`T` 为时间轴最大长度（≤ 2000）。  
  - 用大白话说，就是“最多遍历 2000 × 2000 = 4 000 000 次”，在现代电脑上几毫秒就能跑完。相比暴力的 `2^T`，这是天壤之别。  
- **空间复杂度**：`O(T)`  
  - 只需要一个长度为 `max_end + 1` 的布尔数组来记录哪些秒被打开。相当于“只用一张纸记下每秒是否打开”，非常省内存。  

---

## 心得  

- **核心技巧**：**贪心 + 按结束时间排序**，把“必须打开的秒”尽可能安排在区间的最右侧，以便后面的任务共享。  
- **适用场景**：  
  1. “区间覆盖最少点” 类题目（如 LeetCode 757 “Set Intersection Size At Least Two”）。  
  2. “任务调度需要最少资源” 类问题（如 “Minimum Number of Arrows to Burst Balloons”）。  
- **一句话总结**：**把每个任务的缺口向右补齐，先处理结束早的任务，所有缺口自然会最小化**。

---

## 反思  

- **第一反应**：看到“在每个区间里需要累计一定秒数”，马上想到“选点集合满足区间需求”，于是想到枚举所有秒的开关。  
- **最容易踩的坑**：  
  - 忘记任务的 **duration** 可能大于 1，需要在同一个区间里选择不止一个秒。  
  - 只在区间左端补齐会导致后面任务无法共享已打开的秒，答案会变大。  
  - 边界条件：`start == end`（区间只有 1 秒）时仍然要检查是否已经打开。  
- **下次类似题**：**第一步先把任务按结束时间排序**，然后思考“把必选的资源放在区间最右侧”，这通常是贪心的关键。