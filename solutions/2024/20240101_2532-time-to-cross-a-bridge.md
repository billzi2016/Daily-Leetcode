# #2532. 过桥所需时间 / Time to Cross a Bridge

> 难度：困难 · 标签：Array、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/time-to-cross-a-bridge/)

---

## 题目（英文原版）

**Description**

There are k workers who want to move n boxes from the right (old) warehouse to the left (new) warehouse. You are given the two integers n and k, and a 2D integer array time of size k x 4 where time[i] = [righti, picki, lefti, puti].
The warehouses are separated by a river and connected by a bridge. Initially, all k workers are waiting on the left side of the bridge. To move the boxes, the ith worker can do the following:
The ith worker is less efficient than the jth worker if either condition is met:
The following rules regulate the movement of the workers through the bridge:
Return the elapsed minutes at which the last box reaches the left side of the bridge.

**Examples**

**Example 1:**

```
From 0 to 1 minutes: worker 2 crosses the bridge to the right.
From 1 to 2 minutes: worker 2 picks up a box from the right warehouse.
From 2 to 6 minutes: worker 2 crosses the bridge to the left.
From 6 to 7 minutes: worker 2 puts a box at the left warehouse.
The whole process ends after 7 minutes. We return 6 because the problem asks for the instance of time at which the last worker reaches the left side of the bridge.
```

**Example 2:**

```

```

**Constraints**

- 1 <= n, k <= 104
- time.length == k
- time[i].length == 4
- 1 <= lefti, picki, righti, puti <= 1000

---

## 题目（中文翻译）

描述  
有 k 名工人需要将 n 个箱子从右侧（旧）仓库搬运到左侧（新）仓库。给定整数 n 和 k，及一个大小为 k × 4 的二维整数数组 time，其中 time[i] = [right_i, pick_i, left_i, put_i]。  

仓库之间被一条河隔开，河上有一座桥相连。最初，所有 k 名工人都在桥的左侧等待。为了搬运箱子，第 i 名工人可以按以下顺序执行操作：  

- 右侧 crossing（right_i）  
- 拾取箱子（pick_i）  
- 左侧 crossing（left_i）  
- 放置箱子（put_i）  

第 i 名工人的效率低于第 j 名工人的条件如下（满足任意一条即可）：  

（此处原文缺失）  

以下规则约束工人在桥上的移动：  

（此处原文缺失）  

返回最后一个箱子到达左侧桥口的累计分钟数。

示例 1  
（示例的输入/输出保持原样）

**解释**  
- 从 0 到 1 分钟：工人 2 过桥到右侧。  
- 从 1 到 2 分钟：工人 2 从右侧仓库取箱子。  
- 从 2 到 6 分钟：工人 2 过桥回左侧。  
- 从 6 到 7 分钟：工人 2 把箱子放入左侧仓库。  

整个过程在 7 分钟后结束。我们返回 6 ，因为题目要求返回最后一个工人到达左侧桥口的时间点。  
（已截断）

示例 2  
（示例的输入/输出保持原样）

**解释**  
（此处原文缺失）

约束条件  
- 1 ≤ n, k ≤ 10⁴  
- time.length == k  
- time[i].length == 4  
- 1 ≤ left_i, pick_i, right_i, put_i ≤ 1000

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把整个过程想成“一群人轮流走桥、搬箱子、再走回来”。  
最直接的办法是 **把所有事情顺序写出来**，让每个工人按照下面的步骤一次又一次地执行：

1. 从左岸走到右岸（用 `right[i]` 分钟）  
2. 把箱子从右仓库搬到手里（`pick[i]` 分钟）  
3. 再走回左岸（`left[i]` 分钟）  
4. 把箱子放到左仓库（`put[i]` 分钟）  

把这四个动作接在一起，就是 **一次完整的搬运**，耗时  
`right[i] + pick[i] + left[i] + put[i]`。  

如果我们把 **所有工人** 按照这个顺序 **一个接一个** 完成搬运，直到把 `n` 个箱子全部搬完，就得到答案。

> **类比**：这跟排队买咖啡一样，只有一条队伍（桥），每个人必须等前面的人走完才能轮到自己。

**为什么能得到正确答案？**  
因为我们没有违反题目给出的任何限制：  
- 桥一次只能容纳一个工人；  
- 每个工人必须完整地走、搬、走、放才能算搬完一箱。  

只要把所有合法的动作都按顺序执行，最后的完成时间必然是 **一种** 可行方案的时间。  

**时间/空间复杂度**  
- 需要模拟 **每一次完整搬运**，最坏情况每个箱子都由同一个最慢的工人搬完，模拟次数为 `n`（箱子数）+ `k`（工人初始上桥的次数），每一次都只做常数时间的计算 → **O(n + k)**。  
- 只保存几个计数器和时间变量 → **O(1)** 的额外空间。

> 这里的 “O(n + k)” 用大白话说，就是“随着箱子和工人的数量线性增长”。虽然看起来已经是线性的，但当 `n、k` 都是 10⁴ 时，这个暴力过程仍然会 **频繁让桥空闲**，导致整体耗时远大于实际最优答案。

---

#### 代码（Python）

```python
def findCrossingTime(n: int, k: int, time: list[list[int]]) -> int:
    # 记录已经搬走的箱子数量
    moved = 0
    # 当前时间
    cur = 0
    # 所有工人最初都在左岸，准备第一次过桥
    # 用一个列表模拟“按顺序排队”，这里直接按工人编号顺序
    left_queue = list(range(k))
    # 右岸暂时没有工人
    right_queue = []

    # 为了演示暴力思路，这里把每一次完整搬运都顺序执行
    while moved < n:
        # 取下一个左岸工人（若左岸没有则取右岸）
        if left_queue:
            i = left_queue.pop(0)          # 第 i 个工人
            cur += time[i][0]              # right[i]：左→右
            cur += time[i][1]              # pick[i]：拿箱子
            cur += time[i][2]              # left[i]：右→左
            cur += time[i][3]              # put[i]：放箱子
            moved += 1                     # 完成一箱
            # 完成后工人仍在左岸，继续加入队列等待下次搬运
            left_queue.append(i)
        else:
            # 这里理论上不会出现，因为总有工人在左岸等着
            raise RuntimeError("桥上没人可以过桥")
    return cur
```

> **代码说明**  
- `left_queue.pop(0)` 取出队首工人，模拟“桥空了，最先来的工人上桥”。  
- `time[i][0] … time[i][3]` 分别对应题目中的 `righti, picki, lefti, puti`。  
- 每搬完一箱就把 `moved` 加 1，直到 `moved == n` 为止。  

---

#### 复杂度

- **时间复杂度**：`O(n + k)` → 随着箱子数量线性增长。  
  *大白话*：如果箱子是 10000 个，代码会循环 10000 次，每次做几次加法，时间大概是“几万步”。  
- **空间复杂度**：`O(k)` → 只存放 `k` 个工人的编号。  

> 这套思路虽然能跑通小数据，但在 `n、k` 同时达到上限时会因为桥总是闲置而浪费大量时间。下面我们来找出 **真正的最优方案**。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“一次只能让排在最前面的工人过桥”**，而题目并没有规定必须按编号顺序。  
只要 **桥空了**，我们可以挑选 **任何已经准备好的工人** 过去。  
于是要把 **“谁先准备好”** 和 **“谁效率低”** 两个信息都考虑进去。

**关键观察**  

1. **桥是唯一的资源**，只能一次容纳一个工人。  
2. 当桥空闲时，若左岸和右岸都有工人已经等好（即已经完成前面的动作），我们应该让 **效率更低的工人先过桥**。  
   - “效率低” 的定义：  
     - 如果 `right[i] + left[i]`（只算走桥的时间）更大，则该工人走桥更慢；  
     - 如果走桥时间相同，再比较 `pick[i] + put[i]`（搬箱子的时间）。  
   - 这等价于比较 **总耗时 `right[i] + left[i] + pick[i] + put[i]`**，数值大的工人更低效。  
3. 当只有一侧有工人在等时，显然只能让那侧的工人先过桥。  

因此我们把 **“什么时候可以上桥”** 与 **“效率多少”** 同时放进 **优先队列（最小堆）** 中：

- `left_heap`：左岸等待过桥的工人，堆的键为 `(ready_time, efficiency, worker_id)`。  
- `right_heap`：右岸等待过桥的工人，键同上。  

`ready_time` 表示该工人完成前一步动作后 **已经准备好** 的最早时间。  
`efficiency` 取 **总耗时**（越大越低效），在时间相同的情况下，**效率更低的工人会先被弹出**。

**模拟过程**（事件驱动）：

```
cur = 0                                 # 当前全局时间
moved = 0                               # 已搬走的箱子数
push all workers into left_heap with ready_time=0
while moved < n:
    # 选出下一位可以过桥的工人
    if right_heap and (not left_heap or right_heap[0].ready_time <= left_heap[0].ready_time):
        # 右→左
        ready, eff, i = heapq.heappop(right_heap)
        start = max(cur, ready)          # 等到桥空且工人准备好
        cur = start + left[i]            # 走桥到左岸
        cur += put[i]                    # 放箱子
        moved += 1                       # 完成一箱
        # 这名工人现在在左岸，准备再次去右岸
        heapq.heappush(left_heap, (cur + right[i] + pick[i], eff, i))
    else:
        # 左→右
        ready, eff, i = heapq.heappop(left_heap)
        start = max(cur, ready)
        cur = start + right[i]           # 走桥到右岸
        cur += pick[i]                   # 拿箱子
        # 现在在右岸，等着把箱子搬回左岸
        heapq.heappush(right_heap, (cur + left[i] + put[i], eff, i))
return cur - put[last_worker]   # 题目要求“最后一箱到达左岸的时刻”，即放完箱子的瞬间
```

**核心点解释**  

- **为什么把 `ready_time + crossing + work` 再次压回堆？**  
  当工人完成一次完整的“左→右→左”循环后，他会在左岸再次准备好。下一次上桥的最早时间正好是 **当前时间 + 本次剩余动作时间**（这里我们把右→左的桥和放箱子时间算进 `ready_time`），所以直接把新的 `ready_time` 推回对应的堆即可。

- **为什么使用两个堆而不是一个全局堆？**  
  因为工人只能在自己所在的岸上等待上桥，左岸的工人只能向右走，右岸的只能向左走。两个堆自然区分方向，选取时只比较两边最近的 `ready_time`。

- **为什么效率（总耗时）要放在堆的第二维？**  
  当两名工人在同一时刻都已经准备好时，题目要求“效率更低的先走”。把它设为第二关键字，Python 的 `heapq` 会在 `ready_time` 相等时自动比较 `efficiency`，实现题目要求的调度规则。

#### 代码（Python）

```python
import heapq
from typing import List

def findCrossingTime(n: int, k: int, time: List[List[int]]) -> int:
    """
    模拟桥上搬箱子的过程，返回最后一箱放到左岸的时间点。
    """
    # 拆分四个时间数组，方便阅读
    right = [t[0] for t in time]   # 左→右过桥时间
    pick  = [t[1] for t in time]   # 拿箱子时间
    left  = [t[2] for t in time]   # 右→左过桥时间
    put   = [t[3] for t in time]   # 放箱子时间

    # 效率 = 总耗时，数值越大代表越低效（越慢）
    efficiency = [right[i] + left[i] + pick[i] + put[i] for i in range(k)]

    # 两个小根堆：左岸等待右行、右岸等待左行
    # 堆元素为 (ready_time, efficiency, worker_id)
    left_heap  = [(0, efficiency[i], i) for i in range(k)]
    right_heap = []
    heapq.heapify(left_heap)

    cur_time = 0          # 全局时间指针
    moved   = 0           # 已经成功搬走的箱子数

    while moved < n:
        # 选出下一位可以上桥的工人
        # 若右岸有人且其 ready_time 更早（或相等且更低效），就让右岸工人先走
        if right_heap and (not left_heap or right_heap[0][0] <= left_heap[0][0]):
            ready, eff, idx = heapq.heappop(right_heap)   # 右→左
            start = max(cur_time, ready)                  # 等桥空且工人准备好
            # 走桥到左岸
            cur_time = start + left[idx]
            # 放箱子
            cur_time += put[idx]
            moved += 1                                     # 完成一箱

            # 这名工人现在回到左岸，准备再次去右岸
            # 下一次左→右的最早开始时间 = 当前时间 + 再次走桥 + 拿箱子
            next_ready = cur_time + right[idx] + pick[idx]
            heapq.heappush(left_heap, (next_ready, eff, idx))
        else:
            # 左→右
            ready, eff, idx = heapq.heappop(left_heap)    # 左→右
            start = max(cur_time, ready)
            # 走桥到右岸
            cur_time = start + right[idx]
            # 拿箱子
            cur_time += pick[idx]

            # 现在在右岸，准备把箱子搬回左岸
            # 下一次右→左的最早开始时间 = 当前时间 + 再次走桥 + 放箱子
            next_ready = cur_time + left[idx] + put[idx]
            heapq.heappush(right_heap, (next_ready, eff, idx))

    # cur_time 已经是“最后一次放箱子”结束的时刻
    return cur_time
```

> **代码要点**  
- `ready` 表示该工人 **已经完成前置动作并等在桥口** 的最早时间。  
- `start = max(cur_time, ready)` 确保 **桥只能一次容纳一个工人**，即如果当前时间 `cur_time` 还在进行别人的动作，就得等到 `cur_time`。  
- `next_ready` 把本次 **剩余动作**（走桥 + 拿/放箱子）累加到当前时间，得到下一次 **可以再次上桥** 的时间点，然后重新放进对应的堆。  

#### 复杂度

- **时间复杂度**：`O((n + k) log k)`  
  - 每搬走一箱会弹出一次堆、再插入一次堆（`log k`），共 `n` 次；  
  - 初始把 `k` 名工人放进左堆也是 `k log k`。  
  - 用大白话说，就是“每次操作都像排队找最早的那个人，排队长度最多是工人数 `k`，找人要花点时间（对数级），总共要找 `n` 次”。  
- **空间复杂度**：`O(k)`  
  - 两个堆里最多存放 `k` 条记录，和工人数成正比。

> 与暴力解相比，**把“谁先上桥”从固定顺序改成优先队列**，大幅减少了桥的空闲时间，使整体耗时从线性（但常数很大）降到了 **对数级** 的调度开销。

---

## 心得

- **核心技巧**：**事件驱动的优先队列模拟**（把每个工人的“准备好时间”放进堆，始终取最早且最低效的工人上桥）。  
- **适用场景**  
  1. 需要在 **单一资源**（桥、跑道、机器）上调度多个“作业”，且每个作业在完成前会产生“下次可用时间”。  
  2. “**多机并行**”或“**单机多任务**”的调度问题，例如  
     - “机器加工多批产品”  
     - “单线程处理多条网络请求的排队模型”。  
- **解题钥匙**：把 **时间点** 视为“事件”，用 **最小堆** 按时间顺序弹出，下一个事件产生的时间再压回堆。

---

## 反思

- **第一反应**：看到桥只能一次通行，就想把所有工人排成固定顺序，逐个让他们完成一次搬运。  
- **最容易踩的坑**  
  1. **忽略效率排序**：只按时间先后上桥会导致低效工人占用桥太久，答案会偏大。  
  2. **边界条件**：当左、右两侧的工人“准备好时间”相等时，需要按照“效率更低的先走”来决定；若忘记这个规则会得到错误结果。  
  3. **计数箱子**：箱子数量是通过 **放箱子** 完成时递增的，而不是在**拿箱子**时递增，容易混淆。  
- **下次类似题**的第一步：**把所有状态抽象成 “什么时候可以进行下一个动作”**，并用优先队列管理这些时间点。这样可以自然地得到最早可执行的操作，同时满足题目中对“低效先走”等次序要求。