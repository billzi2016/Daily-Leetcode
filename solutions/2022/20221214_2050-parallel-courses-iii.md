# #2050. 并行课程 III / Parallel Courses III

> 难度：困难 · 标签：Array、Dynamic Programming、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/parallel-courses-iii/)

---

## 题目（英文原版）

**Description**

You are given an integer n, which indicates that there are n courses labeled from 1 to n. You are also given a 2D integer array relations where relations[j] = [prevCoursej, nextCoursej] denotes that course prevCoursej has to be completed before course nextCoursej (prerequisite relationship). Furthermore, you are given a 0-indexed integer array time where time[i] denotes how many months it takes to complete the (i+1)th course.
You must find the minimum number of months needed to complete all the courses following these rules:
Return the minimum number of months needed to complete all the courses.
Note: The test cases are generated such that it is possible to complete every course (i.e., the graph is a directed acyclic graph).

**Examples**

**Example 1:**

```
Input: n = 3, relations = [[1,3],[2,3]], time = [3,2,5]
Output: 8
Explanation: The figure above represents the given graph and the time required to complete each course. 
We start course 1 and course 2 simultaneously at month 0.
Course 1 takes 3 months and course 2 takes 2 months to complete respectively.
Thus, the earliest time we can start course 3 is at month 3, and the total time required is 3 + 5 = 8 months.
```

**Example 2:**

```
Input: n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
Output: 12
Explanation: The figure above represents the given graph and the time required to complete each course.
You can start courses 1, 2, and 3 at month 0.
You can complete them after 1, 2, and 3 months respectively.
Course 4 can be taken only after course 3 is completed, i.e., after 3 months. It is completed after 3 + 4 = 7 months.
Course 5 can be taken only after courses 1, 2, 3, and 4 have been completed, i.e., after max(1,2,3,7) = 7 months.
Thus, the minimum time needed to complete all the courses is 7 + 5 = 12 months.
```

**Constraints**

- 1 <= n <= 5 * 104
- 0 <= relations.length <= min(n * (n - 1) / 2, 5 * 104)
- relations[j].length == 2
- 1 <= prevCoursej, nextCoursej <= n
- prevCoursej != nextCoursej
- All the pairs [prevCoursej, nextCoursej] are unique.
- time.length == n
- 1 <= time[i] <= 104
- The given graph is a directed acyclic graph.

---

## 题目（中文翻译）

**描述**  
给定一个整数 `n`，表示有 `n` 门课程，编号为 `1` 到 `n`。另给定一个二维整数数组 `relations`，其中 `relations[j] = [prevCoursej, nextCoursej]` 表示课程 `prevCoursej` 必须在课程 `nextCoursej` 之前完成（先修关系）。同时，给定一个 **0-indexed** 整数数组 `time`，其中 `time[i]` 表示完成第 `i+1` 门课程需要的月份数。

你需要按照以下规则，计算完成所有课程的最少月份数并返回：

- 同一时间可以并行学习多门没有先修限制的课程。  
- 只有在所有先修课程都完成后，才能开始学习一门课程。

**注意**：测试用例保证所有课程都可以完成（即给定的图是一个有向无环图（DAG））。

---

### 示例

#### 示例 1
```text
输入: n = 3, relations = [[1,3],[2,3]], time = [3,2,5]
输出: 8
解释: 上图展示了给定的课程依赖图以及每门课程所需的时间。
- 在第 0 月，我们同时开始课程 1 和课程 2。
- 课程 1 需要 3 个月完成，课程 2 需要 2 个月完成。
- 因此，课程 3 最早可以在第 3 月开始学习。
- 完成课程 3 还需要 5 个月，所以总时间为 3 + 5 = 8 个月。
```

#### 示例 2
```text
输入: n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
输出: 12
解释: 上图展示了给定的课程依赖图以及每门课程所需的时间。
- 第 0 月可以同时开始课程 1、2、3。
- 课程 1、2、3 分别在第 1、2、3 月完成。
- 课程 4 必须在课程 3 完成后才能开始，即在第 3 月开始，完成时间为第 3+4=7 月。
- 课程 5 必须等到课程 1、2、3、4 都完成后才能开始，最早在第 7 月开始，完成时间为第 7+5=12 月。
- 因此，总共需要 12 个月完成所有课程。
```

---

### 约束条件
- `1 <= n <= 5 * 10^4`
- `0 <= relations.length <= min(n * (n - 1) / 2, 5 * 10^4)`
- `relations[j].length == 2`
- `1 <= prevCoursej, nextCoursej <= n`
- `prevCoursej != nextCoursej`
- 所有 `[prevCoursej, nextCoursej]` 对均唯一。
- `time.length == n`
- `1 <= time[i] <= 10^4`
- 给定的图是有向无环图（DAG）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每一门课程，枚举它所有的前置课程，算出这些前置课程最早能完成的时间，然后把自己的学习时长加进去**。  
可以把课程之间的先修关系想象成一张“任务依赖图”。  
- **节点**：课程本身。  
- **有向边** `prev → next`：表示 `prev` 必须先完成，才能开始 `next`。  

如果我们对一门课程 `i` 递归地去找它的所有前置课程，取这些前置课程的**最晚完成时间**（因为必须等所有前置都完成才能开始），再加上 `time[i]`，就得到 `i` 的最早完成时间。  

这就是“暴力递归”。它之所以**正确**是因为我们严格遵守了先修关系：只有所有前置都结束后才开始当前课程，且我们取的是最晚的前置结束时间（即“最慢的那条路”），所以得到的就是**最早**可能的完成时间。

**为什么会慢**  
- 每次计算一门课程时，都要重新遍历它的所有前置课程。  
- 前置课程之间可能还有自己的前置，导致大量重复计算（子问题被重复求解）。  
- 在最坏情况下，课程之间形成一条长链，递归深度为 `n`，每层都要遍历前面的所有节点，时间呈指数级增长。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)   # 防止递归太深导致错误

def minimumTime_bruteforce(n, relations, time):
    # 建立邻接表：后继列表（这里用前驱列表更方便递归）
    prereq = defaultdict(list)          # key: 课程，value: 所有直接前置课程
    for a, b in relations:
        prereq[b].append(a)

    # 记忆化数组，保存已经算好的最早完成时间，避免重复计算
    memo = {}

    def dfs(course: int) -> int:
        """返回 course 的最早完成时间（包括自己的学习时长）"""
        if course in memo:               # 已经算过直接返回
            return memo[course]
        if not prereq[course]:           # 没有前置课程，可以直接开始
            earliest_start = 0
        else:
            # 所有前置课程的完成时间取最大值，因为必须等最慢的那条路结束
            earliest_start = max(dfs(p) for p in prereq[course])
        # 最早完成时间 = 最早开始时间 + 自己的学习时长
        memo[course] = earliest_start + time[course - 1]
        return memo[course]

    # 对每一门课都算一次，答案是所有课程最晚的完成时间
    ans = max(dfs(i) for i in range(1, n + 1))
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）  
  > 在最坏情况下，每门课都要重新遍历它的所有前置，导致大量重复子问题。  
- **空间复杂度**：`O(n)`  
  > 递归栈深度最坏为 `n`，以及 `memo` 表占用 `O(n)` 空间。

> **大白话**：如果把 `n` 想成 20，`2^20` 已经是一百万次；而 `n` 甚至可能是几万，这种指数级的算法根本跑不完。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复计算**是瓶颈。我们需要把“每门课的最早完成时间”这个子问题只算一次，并且按照**先后顺序**来计算，这正好可以用 **拓扑排序 + 动态规划** 来实现。

**关键观察**  

1. 课程之间的先修关系构成 **有向无环图 (DAG)**。  
2. 在 DAG 中，如果我们按照 **拓扑序**（所有前置课程都在当前课程之前）遍历节点，那么当我们来到某个节点时，它的所有前置课程的最早完成时间已经算好。  
3. 对于课程 `i`，它的**最早开始时间**等于所有直接前置课程的**最晚完成时间**（即 `max(finish[pre])`），再加上自己的学习时长得到 `finish[i]`。这正是一个**动态规划**的转移：  

   \[
   finish[i] = time[i] + \max_{pre \in prereq[i]} finish[pre]
   \]

   如果 `i` 没有前置课程，则 `max` 部分为 `0`，直接可以开始。

**实现步骤**  

| 步骤 | 目的 | 具体做法 |
|------|------|----------|
| 1️⃣ 建图 & 统计入度 | 为后续的拓扑排序准备 | 用邻接表 `graph[pre] → list(next)`，并用 `indegree[next]` 记录每个节点的前置数量 |
| 2️⃣ 初始化队列 | 把所有**可以立刻开始**的课程放进去 | 所有 `indegree == 0` 的课程加入 `queue`，并把它们的 `finish` 设为 `time[i]`（因为可以在第 0 个月直接学习） |
| 3️⃣ 拓扑遍历 | 按拓扑顺序一次处理每门课 | 当从队列弹出 `u` 时，遍历它的所有后继 `v`：<br>① 更新 `v` 的最早开始时间 `earliest[v] = max(earliest[v], finish[u])`<br>② `indegree[v]--`，若降为 0，则 `v` 可以加入队列，`finish[v] = earliest[v] + time[v]` |
| 4️⃣ 取答案 | 所有课程的完成时间中，最晚的那一个就是总耗时 | `answer = max(finish[1:])` |

**为什么快**  

- 每条边只被访问一次，**不再重复计算**前置课程的完成时间。  
- 拓扑排序保证了所有依赖已经就绪，**只需要一次 DP 更新**。  
- 整体复杂度是 **线性的**，即 `O(n + m)`，其中 `m = len(relations)`。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def minimumTime(n: int, relations: List[List[int]], time: List[int]) -> int:
    """
    拓扑排序 + 动态规划 求所有课程的最早完成时间
    :param n: 课程数量，编号 1..n
    :param relations: 前置关系列表，每个元素 [prev, next]
    :param time: time[i] 为第 i+1 门课的学习时长（下标从 0 开始）
    :return: 完成全部课程的最少月份数
    """
    # 1️⃣ 建图 & 入度统计
    graph = defaultdict(list)          # 前置 -> 后继 列表
    indegree = [0] * (n + 1)            # 1-indexed，indegree[i] 为课程 i 的前置数量
    for pre, nxt in relations:
        graph[pre].append(nxt)
        indegree[nxt] += 1

    # 2️⃣ 初始化队列：所有入度为 0 的课程可以立即开始
    q = deque()
    # earliest_start[i] 表示课程 i 能开始的最早月份（不包括自己的学习时长）
    earliest_start = [0] * (n + 1)
    for i in range(1, n + 1):
        if indegree[i] == 0:
            q.append(i)                     # 直接入队
            earliest_start[i] = 0           # 可以在第 0 个月开始

    # 3️⃣ 拓扑遍历并动态规划
    while q:
        u = q.popleft()
        # 课程 u 的完成时间 = 开始时间 + 自己的学习时长
        finish_u = earliest_start[u] + time[u - 1]

        # 把完成时间传递给所有后继课程
        for v in graph[u]:
            # v 的最早开始时间取所有前置的最大完成时间
            earliest_start[v] = max(earliest_start[v], finish_u)
            indegree[v] -= 1               # 前置已处理
            if indegree[v] == 0:           # 所有前置都完成，加入队列
                q.append(v)

    # 4️⃣ 计算答案：所有课程的完成时间中最大的那个
    answer = 0
    for i in range(1, n + 1):
        answer = max(answer, earliest_start[i] + time[i - 1])
    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  > 每个课程和每条先修关系只遍历一次。对比暴力的指数级，这里是线性时间，`n` 最高 5·10⁴，完全可以接受。  
- **空间复杂度**：`O(n + m)`  
  > 需要存储邻接表、入度数组以及最早开始时间数组，均与 `n`、`m` 成正比。

> **对比**：暴力解的时间像是“爬山”，每一步都要回头再走；最优解则是“坐电梯”，一次上升到最高层，直接到达目标。

---

## 心得  

- **核心技巧**：**拓扑排序 + 动态规划**（在 DAG 上计算最长路径）。  
- **适用题型**：  
  1. 课程表类问题（如 *Course Schedule II*、*Parallel Courses*）。  
  2. 任务调度、项目管理中带有先后约束的最早完成时间（如 *Job Scheduling with Dependencies*）。  
  3. 任意需要在有向无环图上求**最长路径**的场景（权值可以是耗时、收益等）。  
- **一句话总结**：把“所有前置完成的最晚时间”当作当前任务的起点，按拓扑顺序一次更新，即可得到全局最短总耗时。

---

## 反思  

- **第一反应**：看到“先修关系”和“最少月份”，自然会想到“先做完所有前置，再做自己”，于是想到递归枚举所有路径。  
- **最容易踩的坑**：  
  - 忘记把 **课程编号从 1 开始** 转成 **列表下标从 0**（导致索引错位）。  
  - 忽略 **并行学习** 的可能性：多个入度为 0 的课程可以同时进行，不能把它们顺序相加。  
  - 在拓扑排序中没有维护 **最早开始时间** 的最大值，导致得到的不是“最慢的那条路”。  
- **下次思路**：遇到带有“先后约束 + 各自耗时”的问题，第一步就要检查是否是 **DAG**，并立刻想到 **拓扑排序 + DP（最长路径）**，而不是直接递归暴力搜索。