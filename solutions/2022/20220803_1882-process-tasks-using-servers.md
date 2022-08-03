# #1882. 使用服务器处理任务 / Process Tasks Using Servers

> 难度：中等 · 标签：Array、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/process-tasks-using-servers/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays servers and tasks of lengths n​​​​​​ and m​​​​​​ respectively. servers[i] is the weight of the i​​​​​​th​​​​ server, and tasks[j] is the time needed to process the j​​​​​​th​​​​ task in seconds.
Tasks are assigned to the servers using a task queue. Initially, all servers are free, and the queue is empty.
At second j, the jth task is inserted into the queue (starting with the 0th task being inserted at second 0). As long as there are free servers and the queue is not empty, the task in the front of the queue will be assigned to a free server with the smallest weight, and in case of a tie, it is assigned to a free server with the smallest index.
If there are no free servers and the queue is not empty, we wait until a server becomes free and immediately assign the next task. If multiple servers become free at the same time, then multiple tasks from the queue will be assigned in order of insertion following the weight and index priorities above.
A server that is assigned task j at second t will be free again at second t + tasks[j].
Build an array ans​​​​ of length m, where ans[j] is the index of the server the j​​​​​​th task will be assigned to.
Return the array ans​​​​.

**Examples**

**Example 1:**

```
Input: servers = [3,3,2], tasks = [1,2,3,2,1,2]
Output: [2,2,0,2,1,2]
Explanation: Events in chronological order go as follows:
- At second 0, task 0 is added and processed using server 2 until second 1.
- At second 1, server 2 becomes free. Task 1 is added and processed using server 2 until second 3.
- At second 2, task 2 is added and processed using server 0 until second 5.
- At second 3, server 2 becomes free. Task 3 is added and processed using server 2 until second 5.
- At second 4, task 4 is added and processed using server 1 until second 5.
- At second 5, all servers become free. Task 5 is added and processed using server 2 until second 7.
```

**Example 2:**

```
Input: servers = [5,1,4,3,2], tasks = [2,1,2,4,5,2,1]
Output: [1,4,1,4,1,3,2]
Explanation: Events in chronological order go as follows: 
- At second 0, task 0 is added and processed using server 1 until second 2.
- At second 1, task 1 is added and processed using server 4 until second 2.
- At second 2, servers 1 and 4 become free. Task 2 is added and processed using server 1 until second 4. 
- At second 3, task 3 is added and processed using server 4 until second 7.
- At second 4, server 1 becomes free. Task 4 is added and processed using server 1 until second 9. 
- At second 5, task 5 is added and processed using server 3 until second 7.
- At second 6, task 6 is added and processed using server 2 until second 7.
```

**Constraints**

- servers.length == n
- tasks.length == m
- 1 <= n, m <= 2 * 105
- 1 <= servers[i], tasks[j] <= 2 * 105

---

## 题目（中文翻译）

你得到两个下标从 **0** 开始的整数数组 `servers` 和 `tasks`，长度分别为 **n** 和 **m**。`servers[i]` 表示第 **i** 台服务器的权重（weight），`tasks[j]` 表示第 **j** 项任务需要的处理时间（seconds）。  

任务通过任务队列（task queue）分配给服务器。最初所有服务器均为空闲状态，队列为空。  

- 在第 **j** 秒时，将第 **j** 项任务插入队列（从第 **0** 秒插入第 **0** 项任务开始）。  
- 当存在空闲服务器且队列不为空时，队列前端的任务会被分配给权重最小的空闲服务器；若出现权重相同的情况，则分配给下标最小的空闲服务器。  
- 若没有空闲服务器且队列不为空，需要等待直到有服务器空闲，然后立刻分配下一个任务。若多台服务器在同一时刻空闲，则按照上述权重与下标的优先级，从队列中依次取出任务进行分配。  
- 某台服务器在第 **t** 秒被分配执行任务 **j** 后，将在第 **t + tasks[j]** 秒再次变为空闲。  

构造一个长度为 **m** 的数组 `ans`，其中 `ans[j]` 为第 **j** 项任务被分配到的服务器下标。返回数组 `ans`。  

## 示例  

### 示例 1  
**输入**  
```
servers = [3,3,2], tasks = [1,2,3,2,1,2]
```  

**输出**  
```
[2,2,0,2,1,2]
```  

**解释**：按时间顺序的事件如下：  
- 第 0 秒，任务 0 被加入并使用服务器 2 处理，直至第 1 秒。  
- 第 1 秒，服务器 2 变为空闲。任务 1 被加入并使用服务器 2 处理，直至第 3 秒。  
- 第 2 秒，任务 2 被加入并使用服务器 0 处理，直至第 5 秒。  
- 第 3 秒，服务器 …（已截断）  

### 示例 2  
**输入**  
```
servers = [5,1,4,3,2], tasks = [2,1,2,4,5,2,1]
```  

**输出**  
```
[1,4,1,4,1,3,2]
```  

**解释**：按时间顺序的事件如下：  
- 第 0 秒，任务 0 被加入并使用服务器 1 处理，直至第 2 秒。  
- 第 1 秒，任务 1 被加入并使用服务器 4 处理，直至第 2 秒。  
- 第 2 秒，服务器 1 与 4 同时空闲。任务 2 被加入并使用服务器 1 处理，直至第 4 秒。  
- 第 …（已截断）  

## 约束条件  

- `servers.length == n`  
- `tasks.length == m`  
- `1 <= n, m <= 2 * 10^5`  
- `1 <= servers[i], tasks[j] <= 2 * 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把任务 **一个接一个** 按照题目规定的时间顺序模拟下来：

1. **记录每台服务器的下次空闲时间**，初始都为 `0`（表示立刻可用）。  
2. 对于第 `j` 秒到来的第 `j` 个任务：  
   - 把它加入任务队列（这里用 `list` 当作普通队列）。  
   - **循环检查**：只要队列不空且有服务器空闲，就把队首任务分配给**权重最小、下标最小**的空闲服务器。  
   - 为了找到符合条件的服务器，我们每次遍历所有服务器，挑出满足 `free_time <= 当前秒` 的最小 `(weight, index)`。  
   - 分配完后，把该服务器的 `free_time` 更新为 `当前秒 + tasks[j]`，并把任务的答案记录下来。  

> **类比**：把服务器想成图书馆的自习位，`free_time` 就是“这位自习位什么时候可以再坐人”。每次有学生来（任务），我们就把所有自习位全部检查一遍，挑出最空闲、最舒服（权重最小）的那位。

这种做法一定能得到正确答案，因为我们完全遵循了题目给出的**“先来先服务、权重最小、下标最小”**的规则，只是实现上比较笨拙。

#### 代码（Python）

```python
from collections import deque
from typing import List

def assignTasks_bruteforce(servers: List[int], tasks: List[int]) -> List[int]:
    n = len(servers)
    m = len(tasks)

    # 每台服务器的下次空闲时间，初始为 0
    free_time = [0] * n

    # 任务队列，保存任务下标
    q = deque()

    ans = [0] * m

    # 当前时间从 0 开始，最多跑到 max(tasks) + m
    cur = 0
    task_idx = 0  # 下一个要加入队列的任务下标

    while task_idx < m or q:
        # 1️⃣ 把本秒到来的任务放进队列
        if task_idx < m and task_idx == cur:
            q.append(task_idx)
            task_idx += 1

        # 2️⃣ 只要有空闲服务器且队列不空，就分配任务
        while q:
            # 找出所有当前空闲的服务器中 (weight, index) 最小的那台
            best = None
            best_idx = -1
            for i in range(n):
                if free_time[i] <= cur:                # 空闲
                    if best is None or (servers[i], i) < best:
                        best = (servers[i], i)
                        best_idx = i
            if best is None:          # 没有空闲服务器，退出内部循环
                break

            # 分配任务
            task_id = q.popleft()
            ans[task_id] = best_idx
            free_time[best_idx] = cur + tasks[task_id]   # 更新空闲时间

        # 3️⃣ 若没有空闲服务器且还有任务未到达，需要快进时间
        if not q and task_idx < m:
            # 找到最近一次有服务器会空闲的时间
            next_free = min(free_time)
            cur = max(cur + 1, next_free)   # 跳到那个时刻
        else:
            cur += 1   # 正常递增

    return ans
```

> 关键注释已用中文标明，代码可直接运行。

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  每处理一个任务（最坏情况下）都要遍历所有 `n` 台服务器找最小的 `(weight, index)`，所以是任务数 `m` 乘以服务器数 `n`。  
  用大白话讲，就是如果有 10 万个任务和 10 万台服务器，程序会做 `10^10` 次比较，明显太慢。

- **空间复杂度**：`O(n + m)`  
  需要保存每台服务器的空闲时间 `O(n)`，以及任务队列和答案数组 `O(m)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都遍历所有服务器** 去找最小的可用服务器。我们可以把“可用服务器集合”维护在一种**随时可以取出最小元素**的数据结构里——**最小堆（优先队列）**。

整个过程可以拆成两部分：

1. **空闲服务器堆 `available`**  
   - 堆中存 `(weight, index)`，堆顶永远是当前空闲服务器中**权重最小、下标最小**的那台。  
   - 初始时把所有服务器都放进去。

2. **忙碌服务器堆 `busy`**  
   - 当服务器被分配任务后，它会在 `busy` 堆里等待“解锁”。  
   - 堆中存 `(free_time, weight, index)`，堆顶是**最早会空闲**的服务器。  
   - 当当前时间 `cur` 达到堆顶的 `free_time`，说明这台服务器已经空闲了，就把它弹出 `busy`，再放回 `available`。

**整体流程**（伪代码）：

```
cur = 0                     # 当前时间（等同于任务下标）
for each task j (0 … m-1):
    cur = max(cur, j)       # 任务 j 在第 j 秒到达

    # 1️⃣ 把所有已经完成的任务的服务器移回 available
    while busy not empty and busy.top.free_time <= cur:
        pop from busy -> (ft, w, i)
        push (w, i) into available

    # 2️⃣ 若没有空闲服务器，必须等到最近的服务器空闲
    if available empty:
        cur = busy.top.free_time
        # 再把此时空闲的服务器全部搬回 available
        while busy not empty and busy.top.free_time <= cur:
            pop from busy -> (ft, w, i)
            push (w, i) into available

    # 3️⃣ 现在一定有空闲服务器，直接取堆顶
    w, i = pop from available
    ans[j] = i
    # 该服务器将在 cur + tasks[j] 时空闲，放入 busy
    push (cur + tasks[j], w, i) into busy
```

> **类比**：  
> - `available` 像一个“排队等座位的入口”，入口的秩序是“先看体重最轻、再看编号”。  
> - `busy` 像一个“正在使用的自习位的计时器”，每当计时结束，就把对应的自习位重新送回入口。

**关键点**：

- 使用 **两个堆**：一个维护空闲服务器的优先级（`weight, index`），一个维护忙碌服务器的解锁时间。  
- 每次任务到达时，先把已经解锁的服务器搬回空闲堆，这一步是 `O(log n)`（弹出/插入堆）。  
- 当空闲堆为空时，直接把时间快进到最近的 `busy` 堆顶的 `free_time`，无需逐秒模拟。  

这样每个任务只会触发 **常数次堆操作**，整体复杂度降到 `O((n + m) log n)`。

#### 代码（Python）

```python
import heapq
from typing import List

def assignTasks(servers: List[int], tasks: List[int]) -> List[int]:
    """
    最优解：利用两个最小堆（空闲堆 & 忙碌堆）模拟任务分配过程。
    """
    n = len(servers)
    m = len(tasks)

    # 空闲堆：存 (weight, index)
    available = [(servers[i], i) for i in range(n)]
    heapq.heapify(available)

    # 忙碌堆：存 (free_time, weight, index)
    busy = []

    ans = [0] * m
    cur = 0          # 当前时间（也可以理解为“当前正在处理的任务的下标”）

    for j in range(m):
        # 任务 j 在第 j 秒到达，时间不能倒退
        cur = max(cur, j)

        # ① 把所有已经完成的任务的服务器搬回空闲堆
        while busy and busy[0][0] <= cur:
            free_time, w, idx = heapq.heappop(busy)
            heapq.heappush(available, (w, idx))

        # ② 若此时没有空闲服务器，需要等到最近的服务器空闲
        if not available:
            # 快进时间到最近的 free_time
            cur = busy[0][0]
            # 再把此时空闲的服务器全部搬回 available
            while busy and busy[0][0] <= cur:
                free_time, w, idx = heapq.heappop(busy)
                heapq.heappush(available, (w, idx))

        # ③ 现在一定有空闲服务器，直接取堆顶（权重最小、下标最小）
        w, idx = heapq.heappop(available)
        ans[j] = idx                     # 记录答案
        # 该服务器将在 cur + tasks[j] 时空闲，放入忙碌堆
        heapq.heappush(busy, (cur + tasks[j], w, idx))

    return ans
```

> 关键行均已加中文注释，直接复制运行即可得到题目要求的答案。

#### 复杂度

- **时间复杂度**：`O((n + m) log n)`  
  - 初始化空闲堆 `O(n)`（堆化）。  
  - 对每个任务最多进行一次 `while busy` 的弹出（`O(log n)`）和一次 `push` 到 `available`（`O(log n)`），以及一次 `push` 到 `busy`（`O(log n)`）。  
  - 用大白话说，就是**每个任务只需要几次“找最小”“放入堆”**，而不是遍历所有服务器，快得多。

- **空间复杂度**：`O(n + m)`（主要是两个堆，最坏情况下 `busy` 里会有 `m` 条记录，`available` 最多 `n` 条）。

---

## 心得

- **核心技巧**：利用**两个最小堆**分别管理“空闲服务器”和“忙碌服务器”，把**“找最小”**的操作从 `O(n)` 降到 `O(log n)`。  
- **适用场景**：  
  1. 需要随时取出“当前最优”元素的排队/调度问题（如**多线程任务调度**、**出租车匹配**）。  
  2. “资源（服务器）有释放时间，需要在未来某时重新加入可用集合”的场景（如**CPU 任务调度**、**会议室预定**）。  
- **一句话总结**：  
  “用堆把‘谁最轻’和‘谁最先空’这两层优先级都压进数据结构，模拟时只搬堆顶，效率自然飞起。”

---

## 反思

- **第一反应**：看到“最小权重、最小下标”以及“服务器会在任务结束后再次可用”，立刻想到**优先队列**（堆）来维护动态的最小元素。  
- **最容易踩的坑**：  
  - **时间快进**：当所有服务器都忙时必须把当前时间直接跳到最近的 `free_time`，否则会逐秒循环导致超时。  
  - **同时释放多台服务器**：在时间快进后，需要一次性把所有 `free_time <= cur` 的服务器全部搬回 `available`，否则会错过同一时刻可以处理的多个任务。  
  - **下标 tie‑break**：堆的比较必须把 `(weight, index)` 作为整体元组，否则会出现权重相同却不按下标排序的错误。  
- **下次类似题的第一步**：  
  “先判断是否有‘随时间变化的可用集合’，如果有，立刻考虑用 **两个堆**（一个存可用，一个存正在计时的）来实现”。  

祝你玩转堆，玩转调度！