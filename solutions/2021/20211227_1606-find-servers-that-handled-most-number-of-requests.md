# #1606. **找到处理最多请求的服务器** / Find Servers That Handled Most Number of Requests

> 难度：困难 · 标签：Array、Greedy、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/find-servers-that-handled-most-number-of-requests/)

---

## 题目（英文原版）

**Description**

You have k servers numbered from 0 to k-1 that are being used to handle multiple requests simultaneously. Each server has infinite computational capacity but cannot handle more than one request at a time. The requests are assigned to servers according to a specific algorithm:
You are given a strictly increasing array arrival of positive integers, where arrival[i] represents the arrival time of the ith request, and another array load, where load[i] represents the load of the ith request (the time it takes to complete). Your goal is to find the busiest server(s). A server is considered busiest if it handled the most number of requests successfully among all the servers.
Return a list containing the IDs (0-indexed) of the busiest server(s). You may return the IDs in any order.

**Examples**

**Example 1:**

```
Input: k = 3, arrival = [1,2,3,4,5], load = [5,2,3,3,3] 
Output: [1] 
Explanation: 
All of the servers start out available.
The first 3 requests are handled by the first 3 servers in order.
Request 3 comes in. Server 0 is busy, so it's assigned to the next available server, which is 1.
Request 4 comes in. It cannot be handled since all servers are busy, so it is dropped.
Servers 0 and 2 handled one request each, while server 1 handled two requests. Hence server 1 is the busiest server.
```

**Example 2:**

```
Input: k = 3, arrival = [1,2,3,4], load = [1,2,1,2]
Output: [0]
Explanation: 
The first 3 requests are handled by first 3 servers.
Request 3 comes in. It is handled by server 0 since the server is available.
Server 0 handled two requests, while servers 1 and 2 handled one request each. Hence server 0 is the busiest server.
```

**Example 3:**

```
Input: k = 3, arrival = [1,2,3], load = [10,12,11]
Output: [0,1,2]
Explanation: Each server handles a single request, so they are all considered the busiest.
```

**Constraints**

- 1 <= k <= 105
- 1 <= arrival.length, load.length <= 105
- arrival.length == load.length
- 1 <= arrival[i], load[i] <= 109
- arrival is strictly increasing.

---

## 题目（中文翻译）

你有 `k` 台服务器，编号从 `0` 到 `k-1`，用于同时处理多个请求。每台服务器的计算能力是无限的，但一次只能处理一个请求。请求的分配遵循以下算法：

给定一个严格递增的正整数数组 `arrival`，其中 `arrival[i]` 表示第 `i` 个请求的到达时间；另一个数组 `load`，其中 `load[i]` 表示第 `i` 个请求的负载（即完成该请求所需的时间）。你的目标是找出最忙的服务器。若某台服务器成功处理的请求数量在所有服务器中最多，则该服务器被认为是最忙的。

返回一个包含最忙服务器 ID（0 起始）的列表，返回顺序任意。

---

### 示例

**示例 1**

```text
Input: k = 3, arrival = [1,2,3,4,5], load = [5,2,3,3,3] 
Output: [1] 
```

**解释**  
所有服务器最初都是空闲的。  
前 3 个请求分别由编号 `0、1、2` 的服务器按顺序处理。  
第 3 个请求（下标为 3）到达时，服务器 `0` 正在忙碌，于是将该请求分配给下一个空闲的服务器 `1`。  
第 4 个请求到达时，所有服务器均忙碌，该请求被丢弃。  
服务器 `0` 和 `2` 各处理了 1 个请求，服务器 `1` 处理了 2 个请求，因此服务器 `1` 是最忙的。

---

**示例 2**

```text
Input: k = 3, arrival = [1,2,3,4], load = [1,2,1,2]
Output: [0]
```

**解释**  
前 3 个请求分别由编号 `0、1、2` 的服务器处理。  
第 3 个请求（下标为 3）到达时，服务器 `0` 已经空闲，于是由它处理。  
服务器 `0` 处理了 2 个请求，服务器 `1`、`2` 各处理了 1 个请求，因此服务器 `0` 是最忙的。

---

**示例 3**

```text
Input: k = 3, arrival = [1,2,3], load = [10,12,11]
Output: [0,1,2]
```

**解释**  
每台服务器各处理了一个请求，处理数量相同，所以所有服务器都是最忙的。

---

### 约束条件

- `1 <= k <= 10^5`
- `1 <= arrival.length, load.length <= 10^5`
- `arrival.length == load.length`
- `1 <= arrival[i], load[i] <= 10^9`
- `arrival` 为严格递增序列

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每一台服务器的“忙碌状态”都记录下来，然后把每个请求顺序地交给服务器检查。  
- **服务器状态**：用一个长度为 `k` 的数组 `busy_until[i]` 表示第 `i` 台服务器何时会空闲（如果当前时间 < `busy_until[i]`，说明它正忙）。  
- **分配规则**：第 `i` 个请求到达时，先从 `(i % k)` 开始顺时针遍历 `k` 台服务器，找到第一个 `busy_until[server] <= arrival[i]` 的服务器，就把请求交给它；如果全部服务器都忙，则这条请求直接丢弃。  
- **计数**：再用一个数组 `cnt[i]` 记录每台服务器成功处理的请求次数，最后取出最大值对应的下标即可。

> **生活化类比**：把每台服务器想象成一间“自助餐厅”。`busy_until[i]` 就是这间餐厅的“打烊时间”。客人（请求）来了以后，先看自己最喜欢的餐厅（`i % k`），如果这家还在营业，就进去吃；否则顺时针找下一家还有空位的餐厅。找不到就只能离开（请求被丢弃）。

这种做法一定能得到正确答案，因为我们完全按照题目给出的规则逐一模拟了请求的分配过程。

#### 代码（Python）

```python
from typing import List

def busiestServers_bruteforce(k: int, arrival: List[int], load: List[int]) -> List[int]:
    n = len(arrival)
    # 每台服务器何时空闲，初始都在时间 0 前空闲
    busy_until = [0] * k
    # 统计每台服务器处理的请求数
    cnt = [0] * k

    for i in range(n):
        start = arrival[i]
        duration = load[i]
        # 从 (i % k) 开始顺时针寻找可用服务器
        assigned = -1
        for offset in range(k):
            server = (i + offset) % k
            if busy_until[server] <= start:          # 该服务器此时空闲
                assigned = server
                break
        if assigned == -1:          # 所有服务器都忙，丢弃此请求
            continue

        # 分配成功，更新状态和计数
        busy_until[assigned] = start + duration
        cnt[assigned] += 1

    # 找出最大处理次数
    max_cnt = max(cnt)
    return [i for i, c in enumerate(cnt) if c == max_cnt]
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`。最坏情况下每个请求都要遍历 `k` 台服务器寻找空闲的（比如所有服务器都忙），所以总共是请求数 `n` 乘以服务器数 `k`。  
  - **大白话**：如果有 10 万个请求、10 万台服务器，算法要检查 10 万 × 10 万 = 10⁹ 次，这在实际运行时会非常慢。  
- **空间复杂度**：`O(k)`。我们只用了两个长度为 `k` 的数组来记录服务器状态和计数。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要线性遍历 `k` 台服务器去找空闲的那一台。我们需要一种能够 **快速定位最近的可用服务器** 的数据结构。  

两件事需要高效完成：  

1. **释放已完成的请求**  
   - 当新请求到达时，所有在此之前已经结束的请求对应的服务器应该重新加入“可用集合”。  
   - 用 **最小堆**（`heapq`）保存 `(结束时间, 服务器编号)`，堆顶始终是最早结束的任务。只要堆顶的结束时间 `<= 当前到达时间`，就把该服务器弹出堆，放回可用集合。  

2. **寻找下一个可用服务器**  
   - 需要在 **有序集合** 中找到 **不小于 target = i % k** 的最小元素（即顺时针第一个可用服务器）。如果集合里没有大于等于 `target` 的元素，则说明要 **环绕**，取集合中的最小元素。  
   - Python 标准库没有直接的「有序集合」实现，但可以用 **有序列表 + 二分搜索**（`bisect`）来模拟：  
     - `available = sorted list of free server ids`（保持升序）  
     - `bisect_left(available, target)` 能在 `O(log k)` 时间得到第一个不小于 `target` 的位置。  
     - 删除元素时用 `pop(idx)`（均摊 `O(k)`，但在本题的规模下仍然能通过），或者用 `deque` + `set` 进行「懒删」来保持 `O(log k)`，这里为保持思路简洁，直接用列表。  

**整体流程**（伪代码）：

```
available = [0, 1, 2, ..., k-1]   // 有序列表
busy = min-heap                  // (结束时间, server_id)
cnt = [0] * k

for i in range(len(arrival)):
    cur = arrival[i]
    dur = load[i]

    // 1. 释放已经结束的任务
    while busy not empty and busy[0].end_time <= cur:
        end, sid = heap.pop()
        insert sid into available (maintain order)

    if available is empty:
        continue   // 所有服务器都忙，丢弃

    // 2. 找到最近的可用服务器
    target = i % k
    pos = bisect_left(available, target)
    if pos == len(available):   // 环绕
        pos = 0
    sid = available.pop(pos)    // 取出并从可用集合中移除

    // 3. 分配任务
    cnt[sid] += 1
    heap.push( (cur + dur, sid) )
```

> **类比**：  
> - **堆** 就像「厨房计时器」：每次只关注最先会结束的那道菜，先把它端出厨房，让对应的厨师重新空闲。  
> - **有序列表** 像「排队的空座位表」：我们可以快速查到「从第 X 位开始最近的空座位」——如果没有，就回到最前面继续找。

#### 代码（Python）

```python
import heapq
import bisect
from typing import List

def busiestServers(k: int, arrival: List[int], load: List[int]) -> List[int]:
    n = len(arrival)

    # 1. 有序集合：当前空闲的服务器编号（升序）
    #    初始时所有服务器都是空闲的
    available = list(range(k))

    # 2. 最小堆：记录正在处理的请求 (结束时间, server_id)
    busy = []                       # heapq 默认是最小堆

    # 3. 计数数组：每台服务器处理的请求数
    cnt = [0] * k

    for i in range(n):
        cur_time = arrival[i]
        duration = load[i]

        # ---------- 释放已经完成的请求 ----------
        while busy and busy[0][0] <= cur_time:
            end_time, sid = heapq.heappop(busy)
            # 把服务器重新加入有序集合（保持升序）
            bisect.insort(available, sid)   # O(log k)

        # ---------- 没有空闲服务器，直接丢弃 ----------
        if not available:
            continue

        # ---------- 寻找最近的可用服务器 ----------
        target = i % k
        pos = bisect.bisect_left(available, target)   # 第一个 >= target
        if pos == len(available):      # 环绕到列表头部
            pos = 0
        sid = available.pop(pos)       # 取出并从可用集合中删除

        # ---------- 分配请求 ----------
        cnt[sid] += 1
        heapq.heappush(busy, (cur_time + duration, sid))

    # ---------- 找出最忙的服务器 ----------
    max_cnt = max(cnt)
    return [i for i, c in enumerate(cnt) if c == max_cnt]
```

> **代码要点说明**  
> - `bisect.insort(available, sid)`：在有序列表中插入一个元素，保持列表仍然有序，时间是 `O(log k)`（二分定位）+ `O(k)`（移动元素），在本题 `k ≤ 10⁵`，整体仍在可接受范围。  
> - `available.pop(pos)`：弹出第 `pos` 位的服务器，即完成「占用」的动作。  
> - `heapq.heappush` / `heapq.heappop`：分别是把新任务的结束时间压入堆，和取出最早结束的任务，均为 `O(log m)`，其中 `m` 为当前正在处理的请求数（最多 `k`）。  

#### 复杂度  

- **时间复杂度**：`O(n log k)`  
  - 每个请求最多执行一次 `while busy` 循环，弹出一次堆元素（`O(log k)`）。  
  - 在有序集合中插入/查找/删除都使用二分，复杂度 `O(log k)`（插入的实际移动代价在最坏情况下是 `O(k)`，但均摊后仍然是 `O(log k)` 级别，实际通过 LeetCode）。  
  - 因此整体随请求数 `n` 线性增长，乘以对数因子 `log k`，远快于暴力的 `O(n·k)`。  

- **空间复杂度**：`O(k)`  
  - `available`、`busy`、`cnt` 三个结构最多各存 `k` 条记录。  

---

## 心得  

- **核心技巧**：利用 **最小堆** 维护“正在忙碌的服务器”，以及 **有序集合 + 二分** 快速定位“顺时针最近的空闲服务器”。  
- **适用的题型**  
  1. 需要在「时间线」上动态维护「可用资源」的调度类问题（如 **任务调度**、**会议室安排**）。  
  2. 需要在循环数组或环形结构中寻找「下一个满足条件的元素」的场景（如 **循环数组的最近重复元素**、**环形指针的最近空位**）。  
- **一句话总结**：**把“忙碌的服务器”放进堆，让最早释放的先出来；把“空闲的服务器”放进有序集合，用二分快速找下一个可用的编号。**  

---

## 反思  

- **第一反应**：看到「每台服务器只能同时处理一个请求」和「顺时针找下一个可用服务器」这两个规则，就想到要**模拟**整个过程。最直接的想法就是逐台检查——这就是暴力解。  
- **最容易踩的坑**  
  1. **环绕寻找**：当 `bisect_left` 返回的位置等于列表长度时，需要回到列表头部，否则会误判没有可用服务器。  
  2. **请求被丢弃的时机**：一定要在把已经结束的任务全部释放以后，再判断 `available` 是否为空。否则可能误认为还有空闲服务器。  
  3. **大数溢出**：结束时间是 `arrival[i] + load[i]`，两者均可能达到 `10⁹`，相加后仍在 Python 整数范围（无限精度），但在某些语言需要使用 64 位整数。  
- **下次遇到同类题的第一步**：  
  - **先划分两类资源**：正在使用的 → 用堆管理最早释放时间；空闲的 → 用有序结构（或队列）快速定位下一个符合条件的资源。这样可以把“线性搜索”降到对数级别。