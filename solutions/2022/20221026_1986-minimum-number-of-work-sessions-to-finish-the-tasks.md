# #1986. 完成所有任务的最少工作会话数 / Minimum Number of Work Sessions to Finish the Tasks

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-work-sessions-to-finish-the-tasks/)

---

## 题目（英文原版）

**Description**

There are n tasks assigned to you. The task times are represented as an integer array tasks of length n, where the ith task takes tasks[i] hours to finish. A work session is when you work for at most sessionTime consecutive hours and then take a break.
You should finish the given tasks in a way that satisfies the following conditions:
Given tasks and sessionTime, return the minimum number of work sessions needed to finish all the tasks following the conditions above.
The tests are generated such that sessionTime is greater than or equal to the maximum element in tasks[i].

**Examples**

**Example 1:**

```
Input: tasks = [1,2,3], sessionTime = 3
Output: 2
Explanation: You can finish the tasks in two work sessions.
- First work session: finish the first and the second tasks in 1 + 2 = 3 hours.
- Second work session: finish the third task in 3 hours.
```

**Example 2:**

```
Input: tasks = [3,1,3,1,1], sessionTime = 8
Output: 2
Explanation: You can finish the tasks in two work sessions.
- First work session: finish all the tasks except the last one in 3 + 1 + 3 + 1 = 8 hours.
- Second work session: finish the last task in 1 hour.
```

**Example 3:**

```
Input: tasks = [1,2,3,4,5], sessionTime = 15
Output: 1
Explanation: You can finish all the tasks in one work session.
```

**Constraints**

- n == tasks.length
- 1 <= n <= 14
- 1 <= tasks[i] <= 10
- max(tasks[i]) <= sessionTime <= 15

---

## 题目（中文翻译）

**题目描述**

有 `n` 项任务待完成。任务耗时由长度为 `n` 的整数数组 `tasks` 表示，其中第 `i` 项任务需要 `tasks[i]` 小时完成。**工作会话**（work session）指的是你连续工作至多 `sessionTime` 小时后必须休息的一段时间。

你需要安排这些任务，使得满足以下条件：

- 每个任务必须完整地安排在某个工作会话中，且同一会话内的任务总时长不能超过 `sessionTime`。
- 在满足上述条件的前提下，返回完成所有任务所需的**最少工作会话数**。

题目保证 `sessionTime` 大于等于 `tasks` 中的最大元素。

**示例**

**示例 1**

> 输入: `tasks = [1,2,3]`, `sessionTime = 3`  
> 输出: `2`  
> 解释: 你可以用两次工作会话完成所有任务。  
> - 第一次工作会话: 完成第 1、2 项任务，耗时 `1 + 2 = 3` 小时。  
> - 第二次工作会话: 完成第 3 项任务，耗时 `3` 小时。

**示例 2**

> 输入: `tasks = [3,1,3,1,1]`, `sessionTime = 8`  
> 输出: `2`  
> 解释: 你可以用两次工作会话完成所有任务。  
> - 第一次工作会话: 完成除最后一项之外的所有任务，耗时 `3 + 1 + 3 + 1 = 8` 小时。  
> - 第二次工作会话: 完成最后一项任务，耗时 `1` 小时。

**示例 3**

> 输入: `tasks = [1,2,3,4,5]`, `sessionTime = 15`  
> 输出: `1`  
> 解释: 所有任务可以在一次工作会话内完成。

**约束条件**

- `n == tasks.length`
- `1 <= n <= 14`
- `1 <= tasks[i] <= 10`
- `max(tasks[i]) <= sessionTime <= 15`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把任务看成**一堆小盒子**，每个盒子里装的时间是 `tasks[i]`。  
一次工作时段（session）就像一个容量为 `sessionTime` 的背包，**只能装不超过这个容量的盒子**。  
最直接的想法是：

1. 按照任务的顺序，一个任务接一个任务尝试放进当前的工作时段。  
2. 如果放不下，就**开启一个新的时段**，继续往后放。  
3. 把所有可能的“开启新时段的时机”全部枚举一遍，最后取最少的时段数。

这其实就是**回溯（Backtracking）**：在每一步我们有两种选择——  
- 把当前任务放进已有的某个时段（只要不超容量）  
- 开一个新时段专门放它  

因为 `n ≤ 14`，任务数量本身不大，暴力搜索在最坏情况下会尝试 `O(n!)`（全排列）甚至更多，但仍然可以在纸面上写出完整的递归框架，帮助我们理清问题。

> **为什么正确？**  
> 回溯会尝试**所有可能的任务分配方式**。只要我们记录下遍历过程中的最小时段数，最后得到的答案必然是全局最优的。

> **时间/空间复杂度大白话**  
> - **时间复杂度**：每个任务都有可能去“开新时段”或“加入已有时段”。如果已经有 `k` 个时段，那么第 `i` 个任务会有 `k+1` 种选择。最坏情况下，`k` 会随任务数线性增长，导致近似 `O(n!)` 的搜索空间（阶乘增长，几秒钟内跑不完）。  
> - **空间复杂度**：递归栈的深度等于任务数 `n`，再加上存放当前时段剩余时间的数组，都是 `O(n)`，即和任务数成线性关系。

#### 代码（Python）

```python
from typing import List

def min_sessions_bruteforce(tasks: List[int], sessionTime: int) -> int:
    n = len(tasks)
    # 把任务按长度从大到小排序，有助于提前剪枝
    tasks.sort(reverse=True)
    best = n  # 最多不超过 n 个时段（每个任务单独一个时段）

    def dfs(idx: int, sessions: List[int]) -> None:
        """
        idx: 正在安排的任务下标
        sessions: 每个已开启时段已经用了多少时间
        """
        nonlocal best
        # 剪枝：已经用了的时段数 >= 当前最优解，后面不必继续
        if len(sessions) >= best:
            return
        # 所有任务都安排完了，更新最优解
        if idx == n:
            best = len(sessions)
            return

        cur = tasks[idx]
        # 尝试放进已有的每个时段
        for i in range(len(sessions)):
            if sessions[i] + cur <= sessionTime:          # 还能装下
                sessions[i] += cur                         # 放进去
                dfs(idx + 1, sessions)
                sessions[i] -= cur                         # 回溯
        # 也可以开启一个新时段
        sessions.append(cur)
        dfs(idx + 1, sessions)
        sessions.pop()                                    # 回溯

    dfs(0, [])
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n!)`（阶乘级），因为每个任务都有可能产生新的时段，搜索树会非常宽。  
- **空间复杂度**：`O(n)`，递归栈深度 + 保存每个时段已用时间的列表。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于**大量的重复子问题**：  
比如任务 `[1,2,3]`，无论我们先把 `1` 放进第一个时段，还是先把 `2` 放进第一个时段，最后的状态可能会出现**相同的任务集合已被安排**的情况。  

我们可以把“哪些任务已经完成”抽象成一个**位掩码（bitmask）**：

- 用 `n` 位二进制数表示任务是否已完成。  
- 第 `i` 位为 `1` 表示第 `i` 个任务已经安排好，`0` 表示未安排。  

这样，每一种 **已完成任务集合** 就是一个**状态**。  
如果我们能够记住（缓存）每个状态对应的**最少时段数**，就不必再次搜索相同的子问题。  

下面的 DP 思路来自**“子集 DP + 状态压缩”**：

1. `dp[mask] = (sessions, last_time)`  
   - `sessions`：完成 `mask` 所代表的任务集合需要的最少完整时段数（不包括当前进行中的时段）。  
   - `last_time`：在第 `sessions`+1 个时段已经用了多少时间（仍然 ≤ `sessionTime`）。  

2. 初始状态 `dp[0] = (0, 0)`，表示没有任务时不需要任何时段，当前时段已用时间为 0。

3. 对每个 `mask`（从 `0` 到 `2^n-1`），尝试把一个**未完成**的任务 `j` 加进去，得到新状态 `new_mask = mask | (1<<j)`。  
   - 如果 `last_time + tasks[j] ≤ sessionTime`，说明可以把任务 `j` 放进 **当前** 正在进行的时段，`sessions` 不变，`last_time` 增加。  
   - 否则，需要 **开启新时段**：`sessions+1`，`last_time = tasks[j]`（因为新时段只放了这个任务）。  

4. 对每个 `new_mask`，保留 **sessions 最小**、若 sessions 相同则 `last_time 最小** 的方案。  

5. 最终答案是 `dp[(1<<n)-1].sessions + 1`（因为 `sessions` 记录的是“已经结束的完整时段”，我们还需要加上正在进行的最后一个时段）。

> **核心概念解释**  
> - **位掩码**：把一组布尔状态压成一个整数。比如 `101`（二进制）代表任务 0、2 完成，任务 1 未完成。  
> - **状态压缩 DP**：用一个数组 `dp[mask]` 保存每个“子集合”对应的最优解，避免重复计算。  

> **类比**：想象你在搬家，每件行李都有重量，车厢容量固定。你把已经装好的行李记在一张纸上（mask），每次再挑一件未装的行李放进去。如果装不下，就再开一辆新车。记录每种装法需要的车数，就是 DP 在做的事。

#### 代码（Python）

```python
from typing import List

def minSessions(tasks: List[int], sessionTime: int) -> int:
    n = len(tasks)
    # 为了让 DP 更快，先把任务按大小倒序，这样大的任务先尝试放入
    tasks.sort(reverse=True)

    # dp[mask] = (sessions, last_time)
    # 使用大整数 2**n 作为数组大小
    INF = (n + 1, 0)            # 一个足够大的初始值
    dp = [INF] * (1 << n)
    dp[0] = (0, 0)               # 空集合：0 个完整时段，当前时段已用 0

    for mask in range(1 << n):
        sessions, last = dp[mask]
        # 遍历所有未完成的任务
        for i in range(n):
            if not (mask >> i) & 1:          # 第 i 项任务还没做
                new_mask = mask | (1 << i)
                # 情况 1：还能放进当前时段
                if last + tasks[i] <= sessionTime:
                    cand = (sessions, last + tasks[i])
                else:                         # 情况 2：必须开新时段
                    cand = (sessions + 1, tasks[i])
                # 取更优的方案
                if cand[0] < dp[new_mask][0] or (cand[0] == dp[new_mask][0] and cand[1] < dp[new_mask][1]):
                    dp[new_mask] = cand

    full_mask = (1 << n) - 1
    # dp[full_mask].sessions 记录已经结束的完整时段数，最后还有一个正在进行的时段
    return dp[full_mask][0] + 1
```

#### 复杂度  

- **时间复杂度**：`O(n * 2^n)`  
  - 我们遍历所有 `2^n` 种子集（`mask`），对每个子集尝试加入 `n` 个任务中的未完成任务。  
  - 对于 `n ≤ 14`，`2^n` 最多是 `16384`，乘以 `14` 仍然在毫秒级。  

- **空间复杂度**：`O(2^n)`  
  - 只需要保存 `dp` 数组，一共 `2^n` 条记录。  

相比暴力的阶乘级搜索，这里是指数级（`2^n`）且常数很小，跑得快得多。

---

## 心得  

- **核心技巧**：**子集 DP（状态压缩）** + **位掩码**。把“哪些任务已经完成”用二进制表示，利用 DP 记忆化避免重复搜索。  
- **适用的题型**（类似思路）：  
  1. “**最小工作时间划分**”类（比如把若干工作分配到固定时长的机器上）。  
  2. “**分配任务到多台机器**”的最小机器数（LeetCode 1723 `Find Minimum Time to Finish All Jobs`）。  
  3. “**装箱问题**”的变种（如 `Can Partition into K Equal Subsets`）。  
- **一句话总结**：把每一种“已经完成的任务集合”记下来，用 DP 只算一次，就能快速得到最少工作时段数。

---

## 反思  

- **第一反应**：看到“最多 14 个任务，sessionTime ≤ 15”，立刻想到**枚举全部分配**（回溯）或**位掩码 DP**。因为规模太小，暴力可以写出来，但仍然会超时。  
- **最容易踩的坑**：  
  - 忘记 **排序** 大任务在前，可能导致 DP 中出现不必要的状态更新，虽不影响正确性但会让代码更慢。  
  - 在 DP 更新时只比较 `sessions` 而忽略 `last_time`，会导致错误的“最小时段数”被覆盖。  
  - 边界：`dp[0]` 必须是 `(0,0)`，否则最终答案会多算一个时段。  
- **下次遇到同类题**：第一步先**判断是否可以用子集 DP**（即 n ≤ 20 左右、状态可以用位掩码表达），然后**定义状态**（已完成任务集合）和**转移**（把一个未完成任务加入当前或新时段），最后实现 DP 并做好状态比较。这样就能在指数时间内得到最优解。