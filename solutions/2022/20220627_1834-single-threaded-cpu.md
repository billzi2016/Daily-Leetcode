# #1834. 单线程 CPU / Single-Threaded CPU

> 难度：中等 · 标签：Array、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/single-threaded-cpu/)

---

## 题目（英文原版）

**Description**

You are given n​​​​​​ tasks labeled from 0 to n - 1 represented by a 2D integer array tasks, where tasks[i] = [enqueueTimei, processingTimei] means that the i​​​​​​th​​​​ task will be available to process at enqueueTimei and will take processingTimei to finish processing.
You have a single-threaded CPU that can process at most one task at a time and will act in the following way:
Return the order in which the CPU will process the tasks.

**Examples**

**Example 1:**

```
Input: tasks = [[1,2],[2,4],[3,2],[4,1]]
Output: [0,2,3,1]
Explanation: The events go as follows: 
- At time = 1, task 0 is available to process. Available tasks = {0}.
- Also at time = 1, the idle CPU starts processing task 0. Available tasks = {}.
- At time = 2, task 1 is available to process. Available tasks = {1}.
- At time = 3, task 2 is available to process. Available tasks = {1, 2}.
- Also at time = 3, the CPU finishes task 0 and starts processing task 2 as it is the shortest. Available tasks = {1}.
- At time = 4, task 3 is available to process. Available tasks = {1, 3}.
- At time = 5, the CPU finishes task 2 and starts processing task 3 as it is the shortest. Available tasks = {1}.
- At time = 6, the CPU finishes task 3 and starts processing task 1. Available tasks = {}.
- At time = 10, the CPU finishes task 1 and becomes idle.
```

**Example 2:**

```
Input: tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
Output: [4,3,2,0,1]
Explanation: The events go as follows:
- At time = 7, all the tasks become available. Available tasks = {0,1,2,3,4}.
- Also at time = 7, the idle CPU starts processing task 4. Available tasks = {0,1,2,3}.
- At time = 9, the CPU finishes task 4 and starts processing task 3. Available tasks = {0,1,2}.
- At time = 13, the CPU finishes task 3 and starts processing task 2. Available tasks = {0,1}.
- At time = 18, the CPU finishes task 2 and starts processing task 0. Available tasks = {1}.
- At time = 28, the CPU finishes task 0 and starts processing task 1. Available tasks = {}.
- At time = 40, the CPU finishes task 1 and becomes idle.
```

**Constraints**

- tasks.length == n
- 1 <= n <= 105
- 1 <= enqueueTimei, processingTimei <= 109

---

## 题目（中文翻译）

给定 `n` 个任务，编号为 `0` 到 `n-1`，用二维整数数组 `tasks` 表示，其中 `tasks[i] = [enqueueTimeᵢ, processingTimeᵢ]` 表示第 `i` 个**任务（task）**将在 `enqueueTimeᵢ` 时可被处理，且需要 `processingTimeᵢ` 的时间才能完成。  

你只有一颗单线程 CPU（single‑threaded CPU），一次最多只能处理一个任务，CPU 的工作方式如下：

1. 当 CPU 空闲且没有可处理的任务时，它会等待，直到下一个任务进入队列。  
2. 当有一个或多个任务可用时，CPU 会从这些任务中挑选 **处理时间（processingTime）最短** 的任务执行。  
3. 如果多个可用任务的处理时间相同，则选择 **编号最小** 的任务。  
4. 任务一旦开始执行，就会一直执行到完成，期间不会被中断。  

返回 CPU 处理完所有任务的 **执行顺序**（即任务的编号序列）。  

---

## 示例  

### 示例 1  
**输入**  
```text
tasks = [[1,2],[2,4],[3,2],[4,1]]
```  

**输出**  
```text
[0,2,3,1]
```  

**解释**  
事件的时间线如下：  

- `time = 1` 时，任务 `0` 可用。可用任务集合 = `{0}`。  
- 同时，空闲的 CPU 开始处理任务 `0`。可用任务集合 = `{}`。  
- `time = 2` 时，任务 `1` 可用。可用任务集合 = `{1}`。  
- `time = 3` 时，任务 `2` 可用。可用任务集合 = `{1, 2}`。  
- 同时，CPU 完成任务 `0`，此时挑选处理时间最短的任务 `2`（`processingTime = 2`）并开始执行。可用任务集合 = `{1}`。  
- `time = 4` 时，任务 `3` 可用。可用任务集合 = `{1, 3}`。  
- CPU 完成任务 `2`，此时处理时间最短的是任务 `3`（`processingTime = 1`），开始执行。可用任务集合 = `{1}`。  
- CPU 依次完成剩余任务 `3`、`1`，得到最终顺序 `[0,2,3,1]`。  

### 示例 2  
**输入**  
```text
tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
```  

**输出**  
```text
[4,3,2,0,1]
```  

**解释**  
事件的时间线如下：  

- `time = 7` 时，所有任务同时可用。可用任务集合 = `{0,1,2,3,4}`。  
- 空闲的 CPU 立即挑选处理时间最短的任务 `4`（`processingTime = 2`）并开始执行。可用任务集合 = `{0,1,2,3}`。  
- `time = 9` 时，CPU 完成任务 `4`，此时处理时间最短的是任务 `3`（`processingTime = 4`），开始执行。可用任务集合 = `{0,1,2}`。  
- `time = 13` 时，CPU 完成任务 `3`，接下来挑选任务 `2`（`processingTime = 5`），以此类推，最终得到执行顺序 `[4,3,2,0,1]`。  

---

## 约束条件  

- `tasks.length == n`  
- `1 <= n <= 10⁵`  
- `1 <= enqueueTimeᵢ, processingTimeᵢ <= 10⁹`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把时间线从 **1** 开始，一秒一秒往后走，**每一时刻** 都去检查哪些任务已经出现（`enqueueTime ≤ 当前时间`），再从这些可选任务里挑出 **处理时间最短** 的那个（如果处理时间相同，就挑下标最小的），交给 CPU 执行。  

- **数据结构**：我们只需要一个普通的 Python 列表来保存所有任务。遍历列表找可执行任务时，就像在字典里找词一样——只不过这里没有现成的“查词本”，只能线性扫描。  
- **为什么正确**：题目本身规定 CPU 每次都要从「当前已经出现且未被处理」的任务中挑最短的，那我们只要严格按这个规则模拟，就一定得到正确的执行顺序。  
- **复杂度的“大白话”**：  
  - **时间复杂度 O(n²)**：假设有 `n` 个任务。我们每走一步时间，都要遍历全部 `n` 个任务去找可执行的；而时间本身最多也要走 `n` 步（因为每走一步都会完成至少一个任务），于是大约会做 `n × n` 次工作。  
  - **空间复杂度 O(1)**：只用了常数级的额外变量（比如当前时间、答案列表），不随 `n` 增长。

#### 代码（Python）

```python
from typing import List

def getOrder_bruteforce(tasks: List[List[int]]) -> List[int]:
    n = len(tasks)
    # 为每个任务记录它的原始下标，方便返回结果
    indexed = [(i, t[0], t[1]) for i, t in enumerate(tasks)]  # (index, enqueue, process)

    cur_time = 0          # CPU 当前的时间指针
    completed = 0         # 已经完成的任务数
    ans = []              # 记录执行顺序

    while completed < n:
        # 1）找出所有已经到达且还没被处理的任务
        candidates = []
        for idx, enq, proc in indexed:
            if enq <= cur_time and idx not in ans:   # 这里用 ans 判断是否已处理
                candidates.append((proc, idx, enq))   # (处理时间, 下标, 入队时间)

        if not candidates:          # 没有可执行任务 → CPU 必须等到下一个任务出现
            # 找到所有未处理任务中最早的 enqueueTime
            next_time = min(enq for idx, enq, proc in indexed if idx not in ans)
            cur_time = max(cur_time, next_time)
            continue

        # 2）从候选集合里挑出处理时间最短、下标最小的任务
        # Python 的元组比较会先比较第一个元素，再比较第二个，以此类推
        proc, idx, _ = min(candidates)

        # 3）执行该任务
        ans.append(idx)
        cur_time += proc          # CPU 忙碌的时间往后推进
        completed += 1

    return ans
```

> **代码说明**  
> - 第 4 行把每个任务和它的原始下标绑在一起，后面挑选时可以直接得到下标。  
> - `candidates` 用来收集当前时刻所有可以执行的任务；`min(candidates)` 会自动实现「处理时间最短、下标最小」的规则。  
> - 当 `candidates` 为空时，说明 CPU 处于空闲，需要跳到下一个任务的 `enqueueTime`（这一步是暴力解的瓶颈所在）。

#### 复杂度

- **时间复杂度**：**O(n²)**  
  - 每完成一个任务（共 `n` 次），我们都要遍历全部 `n` 条任务去找可执行的，所以大约 `n × n` 次比较。  
- **空间复杂度**：**O(1)**（不计输出数组）  
  - 只用了几个整数变量和一个临时的 `candidates` 列表（最多 `n` 大小），不随 `n` 的增长而出现额外的递归栈或哈希表等。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**每一次都要遍历全部任务**。我们可以把任务提前**排序**，让 CPU 按时间顺序“看到”任务；同时，用**最小堆（priority queue）**只保留已经出现但还未处理的任务，这样每次挑选最短任务只需要 `O(log k)`（`k` 为堆的大小），而不必遍历全部 `n` 条。

**一步步的优化过程**：

1. **先把任务按照 `enqueueTime` 排序**  
   - 想象把所有任务排成一条队伍，排好序后我们只需要顺序走过这条队伍，就能知道下一个“什么时候会有新任务出现”。  
2. **维护一个最小堆**  
   - 堆里放的是 **已经到达且还没处理的任务**，堆的比较键是 `(processingTime, index)`。  
   - 这相当于把“已出现的任务”装进一个“随时可以抽最短的抽屉”，抽屉最上面的就是处理时间最短、下标最小的任务。  
   - **类比**：堆就像一本“按页码排好序的字典”，查找最小的那一页（最短任务）只需要几步，而不必从头到尾翻。  
3. **模拟 CPU 的工作**  
   - 用一个指针 `i` 遍历已经排好序的任务列表。  
   - **把所有 enqueueTime ≤ 当前时间的任务都压进堆**（相当于它们已经“排队”等待”。）  
   - **如果堆非空**，弹出堆顶任务执行，时间前进 `processingTime`。  
   - **如果堆空**，说明此时没有任务可做，CPU 必须“等”，直接把时间跳到下一个任务的 `enqueueTime`（即 `tasks[i][0]`）。  
   - 重复上述过程，直到所有任务都被处理完。

**核心算法**：排序 + 最小堆（优先队列）  
- 排序的时间复杂度是 `O(n log n)`。  
- 堆的每次 `push` / `pop` 都是 `O(log n)`，而整个过程最多会 `push` `n` 次、`pop` `n` 次，仍是 `O(n log n)`。

#### 代码（Python）

```python
import heapq
from typing import List

def getOrder(tasks: List[List[int]]) -> List[int]:
    n = len(tasks)
    # 1) 把任务和原始下标绑在一起，按 enqueueTime 排序
    #    每个元素形如 (enqueueTime, processingTime, index)
    indexed = [(enq, proc, i) for i, (enq, proc) in enumerate(tasks)]
    indexed.sort(key=lambda x: x[0])          # 按出现时间升序

    ans = []          # 记录执行顺序
    min_heap = []     # 堆中存 (processingTime, index)
    time = 0          # CPU 当前时间指针
    i = 0             # 遍历 sorted tasks 的指针

    while len(ans) < n:
        # 2) 把所有已经到达的任务加入堆
        while i < n and indexed[i][0] <= time:
            enq, proc, idx = indexed[i]
            heapq.heappush(min_heap, (proc, idx))   # 处理时间相同会自动比较下标
            i += 1

        if min_heap:
            # 3) 堆非空 → 取出处理时间最短、下标最小的任务
            proc, idx = heapq.heappop(min_heap)
            ans.append(idx)          # 记录执行顺序
            time += proc             # CPU 忙碌到 time + proc
        else:
            # 4) 堆空 → CPU 空闲，直接跳到下一个任务的出现时间
            #    这里一定有未处理的任务，因为 while 循环条件保证 ans 还未满
            time = indexed[i][0]

    return ans
```

> **代码说明**  
> - 第 4 行把每个任务包装成三元组 `(enqueue, process, index)`，随后 `sort` 让我们可以**一次遍历**得到“下一个要出现的任务”。  
> - `while i < n and indexed[i][0] <= time:` 负责把**所有已到达**的任务一次性压进堆，避免每次只压一个导致多余的循环。  
> - `heapq.heappush` / `heapq.heappop` 实现最小堆，堆的比较键是 `(proc, idx)`，自然满足“处理时间最短、下标最小”。  
> - 当堆为空时，`time = indexed[i][0]` 直接把时间快进到下一个任务的出现时刻，省去逐秒等待的无效循环。

#### 复杂度

- **时间复杂度**：**O(n log n)**  
  - 排序一次 `O(n log n)`。  
  - 每个任务最多一次 `push`、一次 `pop`，每次操作 `O(log n)`，共 `2n` 次，仍是 `O(n log n)`。  
  - 与暴力解的 `O(n²)` 相比，规模稍大的 `10⁵` 级数据也能轻松跑完。  

- **空间复杂度**：**O(n)**  
  - 需要存放排序后的任务列表（`O(n)`）和堆（最坏情况下同时存 `n` 条已到达但未处理的任务），以及答案数组 `ans`（`O(n)`）。  
  - 相比暴力解的常数空间，这里多用了线性空间，但仍在题目允许的范围内。

---

## 心得

- **核心技巧**：**使用最小堆维护已到达任务的优先顺序**，配合**先按 enqueueTime 排序**的预处理。  
- **适用的题型**（类似思路）  
  1. *LeetCode 1834. 单线程 CPU*（本题）  
  2. *LeetCode 218. 天际线问题*（利用堆维护当前最高建筑）  
  3. *LeetCode 621. 任务调度器*（堆帮助挑选最少间隔的任务）  
- **一句话总结解题钥匙**：**先把“何时会出现任务”排好序，再用最小堆随时挑出“当前最短的任务”。**

---

## 反思

- **第一反应**：看到“CPU 每次选最短任务”，立刻想到**优先队列**（堆），但最初会忽视任务出现时间的限制，导致直接把所有任务都放进堆，这会违背题目要求。  
- **最容易踩的坑**  
  1. **忘记在堆里同时保存任务下标**，导致无法按照 “处理时间相同取下标最小” 的规则。  
  2. **CPU 空闲时未正确跳时间**，如果只把时间加 `1` 而不是直接跳到下一个 `enqueueTime`，会导致时间循环 `O(maxTime)`，超时。  
  3. **边界条件**：所有任务的 `enqueueTime` 都相同，或者只有一个任务时，算法仍需正常工作。  
- **下次遇到同类题的第一步**：  
  - **把所有事件（任务出现）按时间排序**，随后**用堆维护当前可选的最佳对象**。这样可以把“时间线模拟”和“最佳选择”两件事分离，代码更清晰、效率更高。