# #2365. 任务调度器 II / Task Scheduler II

> 难度：中等 · 标签：Array、Hash Table、Simulation · [LeetCode 链接](https://leetcode.com/problems/task-scheduler-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of positive integers tasks, representing tasks that need to be completed in order, where tasks[i] represents the type of the ith task.
You are also given a positive integer space, which represents the minimum number of days that must pass after the completion of a task before another task of the same type can be performed.
Each day, until all tasks have been completed, you must either:
Return the minimum number of days needed to complete all tasks.

**Examples**

**Example 1:**

```
Input: tasks = [1,2,1,2,3,1], space = 3
Output: 9
Explanation:
One way to complete all tasks in 9 days is as follows:
Day 1: Complete the 0th task.
Day 2: Complete the 1st task.
Day 3: Take a break.
Day 4: Take a break.
Day 5: Complete the 2nd task.
Day 6: Complete the 3rd task.
Day 7: Take a break.
Day 8: Complete the 4th task.
Day 9: Complete the 5th task.
It can be shown that the tasks cannot be completed in less than 9 days.
```

**Example 2:**

```
Input: tasks = [5,8,8,5], space = 2
Output: 6
Explanation:
One way to complete all tasks in 6 days is as follows:
Day 1: Complete the 0th task.
Day 2: Complete the 1st task.
Day 3: Take a break.
Day 4: Take a break.
Day 5: Complete the 2nd task.
Day 6: Complete the 3rd task.
It can be shown that the tasks cannot be completed in less than 6 days.
```

**Constraints**

- 1 <= tasks.length <= 105
- 1 <= tasks[i] <= 109
- 1 <= space <= tasks.length

---

## 题目（中文翻译）

You are given a **0-indexed** array of positive integers `tasks`, representing tasks that need to be completed in order, where `tasks[i]` denotes the **type**（type） of the *i*‑th task.  
You are also given a positive integer `space`, which represents the minimum number of days that must pass after the completion of a task before another task of the same **type**（type） can be performed.  

Each day, until all tasks have been completed, you must either:

* complete the next pending task, **or**
* take a break (i.e., do nothing).

Return the minimum number of days needed to complete all tasks.

---

### 示例

**示例 1**  
```
Input: tasks = [1,2,1,2,3,1], space = 3
Output: 9
Explanation:
一种在 9 天内完成所有任务的方案如下：
Day 1: 完成第 0 个任务。
Day 2: 完成第 1 个任务。
Day 3: 休息。
Day 4: 休息。
Day 5: 完成第 2 个任务。
Day 6: 完成第 3 个任务。
Day 7: 休息。
Day 8: 完成第 4 个任务。
Day 9: 完成第 5 个任务。
可以证明，无法在少于 9 天的时间内完成所有任务。
```

**示例 2**  
```
Input: tasks = [5,8,8,5], space = 2
Output: 6
Explanation:
一种在 6 天内完成所有任务的方案如下：
Day 1: 完成第 0 个任务。
Day 2: 完成第 1 个任务。
Day 3: 休息。
Day 4: 休息。
Day 5: 完成第 2 个任务。
Day 6: 完成第 3 个任务。
可以证明，无法在少于 6 天的时间内完成所有任务。
```

---

### 约束条件

- `1 <= tasks.length <= 10^5`
- `1 <= tasks[i] <= 10^9`
- `1 <= space <= tasks.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是 **按顺序模拟每一天**：

1. 从第 0 天开始，依次查看 `tasks` 中的下一个任务。  
2. 对于当前任务 `t`，如果它是第一次出现，直接在当天完成。  
3. 否则，需要查看上一次完成同类型任务的天数 `last[t]`。  
   - 若 `today - last[t] > space`（已经间隔足够），就可以直接完成。  
   - 否则必须 **休息**（不做任何任务），天数 +1，重新判断同一个任务。  

这个过程就像排队买咖啡：如果前面有人已经点了同一种咖啡，需要等一定时间机器才能再冲同一种，否则只能等（休息）再继续。

> **为什么正确**  
> 我们每一次都严格遵守“同类任务之间至少相隔 `space` 天”的规则，并且 **不提前休息**（只有在必须等待时才休息），所以得到的天数一定是可行的且不会多余。

> **时间/空间复杂度**  
> - 每天我们只检查一次任务，最坏情况下可能要 **插入很多休息天**。  
> - 设总天数为 `D`，每次循环都把 `day` 加 1，循环次数正好是 `D`。  
> - `D` 在最坏情况下等于 `tasks.length + (tasks.length-1) * space`（每两个相同任务之间都要插满 `space` 天），约为 `O(n·space)`，其中 `n = len(tasks)`。  
> - 空间上我们只需要一个哈希表记录每种任务上一次完成的天数，最多存 `n` 种任务，`O(n)`。

#### 代码（Python）
```python
from typing import List

def leastDays_bruteforce(tasks: List[int], space: int) -> int:
    # 记录每种任务最近一次完成的天数，key 类似字典里的“词”，value 类似“页码”
    last_done = {}               # dict[int, int]
    day = 0                      # 当前是第几天（从 0 开始计数，最后返回 day）

    i = 0                        # 正在处理的任务下标
    while i < len(tasks):
        cur = tasks[i]           # 当前任务的类型
        # 上一次完成该类型任务的天数，若从未完成过则设为 -inf
        prev_day = last_done.get(cur, -10**18)

        # 判断是否满足间隔要求
        if day - prev_day > space:   # 已经间隔足够，可以直接完成
            last_done[cur] = day     # 记录本次完成的天数
            i += 1                   # 处理下一个任务
        # 否则必须休息一天，什么也不做
        day += 1                     # 天数前进

    # 循环结束时 day 已经是完成最后一个任务的那一天的索引 + 1
    return day
```

#### 复杂度
- **时间复杂度**：`O(n·space)`（最坏情况会在每两个相同任务之间插入 `space` 天的休息）。  
  > 大白话：如果 `space` 很大，就可能要在任务之间“排队等候”很多天，时间会随 `space` 成线性增长。
- **空间复杂度**：`O(n)`，只用了一个哈希表来记每种任务上一次完成的天数。

---

### 2. 最优解

#### 思路  
暴力解的慢点在 **逐天递增**，即使我们已经知道需要等多少天，也只能一步步走。  
我们可以直接 **算出下一个任务最早可以完成的天数**，跳过中间的休息天。

关键观察：

- 对于每一种任务类型 `t`，只要记录它 **上一次完成的天数** `last[t]`，  
  那么 **下次可以完成的最早天数** 为 `last[t] + space + 1`（因为需要间隔 `space` 天，+1 表示下一个可用的日子）。
- 当我们准备完成第 `i` 个任务 `tasks[i] = t` 时，只要比较当前天数 `day` 与 `last[t] + space + 1`：
  - 若 `day` 已经不早于该值，说明间隔已满足，直接在 `day` 完成任务。
  - 若 `day` 仍然早于该值，需要 **直接跳到** `last[t] + space + 1` 那天完成任务（相当于一次性“休息”若干天）。
- 这样我们每处理一个任务只做 **O(1)** 的工作，整个过程只遍历一次任务数组。

类比：想象每种任务都有一个“冷却计时器”，当计时器结束后才能再次使用。我们不必每秒检查计时器，而是直接把时间快进到计时器结束的那一刻。

#### 代码（Python）
```python
from typing import List

def leastDays_optimal(tasks: List[int], space: int) -> int:
    # 哈希表记录每种任务最近一次完成的天数
    last_done = {}               # dict[int, int]

    day = 0                      # 当前天数（从 0 开始计数）

    for t in tasks:
        # 该任务上一次完成的天数，若从未出现过则设为 -inf
        prev = last_done.get(t, -10**18)

        # 该任务下次可以完成的最早天数
        earliest = prev + space + 1

        # 如果当前天数已经不早于 earliest，就可以直接做；否则把 day 跳到 earliest
        if day < earliest:
            day = earliest        # 一次性“休息”到合适的日子

        # 在 day 这天完成任务 t
        last_done[t] = day
        day += 1                  # 完成任务后，天数前进到下一天

    return day
```

#### 复杂度
- **时间复杂度**：`O(n)`，只遍历一次 `tasks`，每次操作都是哈希表的 O(1) 读取/写入。  
  > 与暴力解相比，我们不再逐天递增，而是一次性跳过不必要的休息天，速度提升了 `space` 倍（在最坏情况下）。
- **空间复杂度**：`O(m)`，其中 `m` 是不同任务类型的数量，最坏 `m ≤ n`，即 `O(n)`。

---

## 心得

- **核心技巧**：利用哈希表记录“上一次完成时间”，并根据 `space` 直接计算**下次可用的最早时间**，实现“跳跃式”模拟。
- **适用的题型**  
  1. **Task Scheduler 系列**（如 LeetCode 621、Task Scheduler II）。  
  2. **带冷却时间的调度/排队问题**（比如“CPU 任务调度”）。  
  3. **需要按顺序处理且受限于上一次出现位置的序列题**（如“最小间隔子数组”）。
- **一句话总结**：**把“等多少天”算出来，一次性快进，而不是每天慢慢等。**

---

## 反思

- **第一反应**：看到 “space 表示同类任务之间必须相隔的天数”，自然想到逐天模拟——最安全但最慢的办法。
- **最容易踩的坑**  
  - **边界条件**：第一次出现的任务没有前置限制，需要把上一次完成时间设为一个极小值（如 `-inf`），否则会误判需要等待。  
  - **`space = 0`** 时，`earliest = prev + 1`，仍然可以直接在同一天后完成下一个任务（因为 `day` 已经加 1），代码必须兼容。  
  - **大数溢出**：`tasks[i]` 最大可达 `10^9`，但我们只在哈希表里存键，不会产生算术溢出；使用 Python 的大整数即可。
- **下次遇到同类题**：第一步先**思考能否直接算出“下次可执行的最早时间”，而不是逐天递增——这往往是突破暴力的关键。