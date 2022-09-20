# #1942. 最小未被占用的椅子编号 / The Number of the Smallest Unoccupied Chair

> 难度：中等 · 标签：Array、Hash Table、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/the-number-of-the-smallest-unoccupied-chair/)

---

## 题目（英文原版）

**Description**

There is a party where n friends numbered from 0 to n - 1 are attending. There is an infinite number of chairs in this party that are numbered from 0 to infinity. When a friend arrives at the party, they sit on the unoccupied chair with the smallest number.
When a friend leaves the party, their chair becomes unoccupied at the moment they leave. If another friend arrives at that same moment, they can sit in that chair.
You are given a 0-indexed 2D integer array times where times[i] = [arrivali, leavingi], indicating the arrival and leaving times of the ith friend respectively, and an integer targetFriend. All arrival times are distinct.
Return the chair number that the friend numbered targetFriend will sit on.

**Examples**

**Example 1:**

```
Input: times = [[1,4],[2,3],[4,6]], targetFriend = 1
Output: 1
Explanation: 
- Friend 0 arrives at time 1 and sits on chair 0.
- Friend 1 arrives at time 2 and sits on chair 1.
- Friend 1 leaves at time 3 and chair 1 becomes empty.
- Friend 0 leaves at time 4 and chair 0 becomes empty.
- Friend 2 arrives at time 4 and sits on chair 0.
Since friend 1 sat on chair 1, we return 1.
```

**Example 2:**

```
Input: times = [[3,10],[1,5],[2,6]], targetFriend = 0
Output: 2
Explanation: 
- Friend 1 arrives at time 1 and sits on chair 0.
- Friend 2 arrives at time 2 and sits on chair 1.
- Friend 0 arrives at time 3 and sits on chair 2.
- Friend 1 leaves at time 5 and chair 0 becomes empty.
- Friend 2 leaves at time 6 and chair 1 becomes empty.
- Friend 0 leaves at time 10 and chair 2 becomes empty.
Since friend 0 sat on chair 2, we return 2.
```

**Constraints**

- n == times.length
- 2 <= n <= 104
- times[i].length == 2
- 1 <= arrivali < leavingi <= 105
- 0 <= targetFriend <= n - 1
- Each arrivali time is distinct.

---

## 题目（中文翻译）

描述  
有一个派对，`n` 位朋友编号为 `0` 到 `n - 1` 参加。派对上有无限多的椅子，编号从 `0` 到正无穷。当一位朋友到达派对时，他会坐在**未占用的椅子（unoccupied chair）**中编号最小的那把。  
当一位朋友离开派对时，他的椅子在离开的瞬间变为未占用。如果另一位朋友在同一瞬间到达，他们可以坐在这把椅子上。  

给定一个下标从 `0` 开始的二维整数数组 `times`，其中 `times[i] = [arrivali, leavingi]` 表示第 `i` 位朋友的到达时间和离开时间，另有整数 `targetFriend`。所有的到达时间互不相同。  
返回编号为 `targetFriend` 的朋友最终坐的椅子编号。

示例  

示例 1:  
输入: `times = [[1,4],[2,3],[4,6]]`, `targetFriend = 1`  
输出: `1`  
解释:  
- 朋友 `0` 在时间 `1` 到达，坐在椅子 `0`。  
- 朋友 `1` 在时间 `2` 到达，坐在椅子 `1`。  
- 朋友 `1` 在时间 `3` 离开，椅子 `1` 变为空。  
- 朋友 `0` 在时间 `4` 离开，椅子 `0` 变为空。  
- 朋友 `2` 在时间 `4` 到达，坐在椅子 `0`。  
由于朋友 `1` 坐在椅子 `1`，返回 `1`。

示例 2:  
输入: `times = [[3,10],[1,5],[2,6]]`, `targetFriend = 0`  
输出: `2`  
解释:  
- 朋友 `1` 在时间 `1` 到达，坐在椅子 `0`。  
- 朋友 `2` 在时间 `2` 到达，坐在椅子 `1`。  
- 朋友 `0` 在时间 `3` 到达，坐在椅子 `2`。  
- 朋友 `1` 在时间 `5` 离开，椅子 `0` 变为空。  
- 朋友 `2` 在时间 `6` 离开，椅子 `1` 变为空。  
- 朋友 `0` 在时间 `10` 离开，椅子 `2` 变为空。  
由于朋友 `0` 坐在椅子 `2`，返回 `2`。

约束条件  
- `n == times.length`  
- `2 <= n <= 10^4`  
- `times[i].length == 2`  
- `1 <= arrivali < leavingi <= 10^5`  
- `0 <= targetFriend <= n - 1`  
- 每个 `arrivali` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **模拟** 整个派对的过程：

1. 按照朋友的到达顺序（`times[i][0]`）依次处理每个人。  
2. 当某个朋友到达时，从编号 `0` 开始往上找，看看哪把椅子是空的，找到的第一把就是他坐的椅子。  
3. 当朋友离开时，把对应的椅子标记为“空”。  

> **类比**：把所有椅子想成一本编号从 0 开始的字典，空椅子就是字典里没有被划掉的词条。我们每次都要从头遍历，找第一个没有被划掉的词条。

因为题目保证所有到达时间互不相同，我们只需要在每一次**到达**时检查当前已经离开的朋友并把他们的椅子释放即可（可以用一个简单的列表保存每个人的离开时间和对应的椅子）。

这个方法**一定能得到正确答案**——我们严格按照题目描述的“最小编号空椅子”来分配。

#### 代码（Python）

```python
def smallestChair(times, targetFriend):
    n = len(times)
    # 记录每个人的座位，-1 表示还未坐下
    seat_of = [-1] * n

    # 按到达时间排序，得到处理顺序的朋友下标列表
    order = sorted(range(n), key=lambda i: times[i][0])

    # 用一个列表保存已经坐下的朋友信息： (离开时间, 朋友编号, 椅子编号)
    occupied = []          # 这里用普通 list，后面会遍历检查是否有人离开

    # 用一个布尔数组记录椅子是否被占用，长度随需要动态增长
    occupied_chair = []    # occupied_chair[i] == True 表示椅子 i 已被占用

    for friend in order:
        cur_arrival = times[friend][0]

        # 1️⃣ 先把已经离开的朋友的椅子释放
        new_occupied = []
        for leave, f, chair in occupied:
            if leave <= cur_arrival:          # 已经离开
                occupied_chair[chair] = False   # 这把椅子空出来
            else:
                new_occupied.append((leave, f, chair))
        occupied = new_occupied

        # 2️⃣ 找到最小的空椅子编号
        chair = 0
        while True:
            if chair >= len(occupied_chair):      # 还没有这把椅子，直接扩容
                occupied_chair.append(False)
            if not occupied_chair[chair]:        # 空的，就坐下
                break
            chair += 1

        # 记录坐下信息
        seat_of[friend] = chair
        occupied_chair[chair] = True
        occupied.append((times[friend][1], friend, chair))

        # 如果已经是目标朋友，直接返回答案
        if friend == targetFriend:
            return chair

    return -1   # 理论上不会走到这里
```

> 关键行中文注释已写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环遍历 `n` 位朋友。  
  - 每次寻找最小空椅子时最坏需要从 `0` 扫到当前已经使用的最大椅子编号，最坏情况是 `O(n)`。  
  - 因此总体是 `n * n = n²`。  
  - **大白话**：如果有 10,000 位朋友，最差情况下要检查 10,000 × 10,000 = 1 亿次，运行会比较慢。

- **空间复杂度**：`O(n)`  
  - 需要保存每个人的座位、已占用的椅子状态以及正在进行的离开事件，最多和朋友数量同阶。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于两点：

1. **寻找最小空椅子** 时需要线性扫描。  
2. **释放座位** 时需要遍历所有已占用的朋友。

要把这两件事都变成 **对数时间**（`O(log n)`），我们可以借助 **最小堆（优先队列）**：

- **可用椅子堆** `free`: 存放所有当前空闲的椅子编号，堆顶永远是最小编号。  
- **占用椅子堆** `busy`: 存放正在使用的椅子信息 `(离开时间, 椅子编号)`，堆顶是最早离开的那位朋友。  

处理步骤：

1. **把所有事件按照时间排序**。  
   为了统一处理“离开”和“到达”，我们把每位朋友的到达和离开分别视为两个事件，放进同一个列表 `events`，格式为 `(时间, 类型, 朋友编号)`，其中 `类型 = 0` 表示离开，`1` 表示到达。因为离开和到达可能在同一时刻，**先处理离开**（`type = 0` 排在前）才能让新到的朋友立即坐到刚释放的椅子上。  

2. **遍历事件**：  
   - **离开事件**：弹出 `busy` 堆顶（一定是当前离开的朋友），把对应的椅子编号加入 `free` 堆，这样它立刻成为可用的最小椅子。  
   - **到达事件**：  
     - 若 `free` 不为空，直接取堆顶（最小空椅子）。  
     - 若 `free` 为空，说明所有已有的椅子都被占用，此时需要新开一把椅子，编号就是当前已使用的椅子数量 `next_seat`（从 `0` 开始递增）。  
     - 把 `(离开时间, 椅子编号)` 加入 `busy` 堆，标记这把椅子被占用。  
     - 如果到达的朋友正是 `targetFriend`，立刻返回他坐的椅子编号。

> **类比**：  
> - `busy` 堆像是“正在用餐的桌子”，我们随时知道哪张桌子最早会空出来（堆顶）。  
> - `free` 堆像是“空闲的餐具抽屉”，抽屉里总是按编号从小到大排好，取最上面的就是编号最小的那把椅子。

整个过程每个事件只会做 `O(log n)` 次堆操作，整体 `O(n log n)`。

#### 代码（Python）

```python
import heapq
from typing import List

def smallestChair(times: List[List[int]], targetFriend: int) -> int:
    n = len(times)

    # 1️⃣ 把所有到达 / 离开事件放进同一个列表
    #   (时间, 类型, 朋友编号)   类型 0=离开 1=到达，离开先处理
    events = []
    for i, (arr, leave) in enumerate(times):
        events.append((arr, 1, i))   # 到达
        events.append((leave, 0, i)) # 离开
    events.sort()   # 按时间升序，时间相同则离开在前

    free = []                # 可用椅子最小堆，存椅子编号
    busy = []                # 占用椅子堆，存 (离开时间, 椅子编号)
    next_seat = 0            # 下一个从未使用过的椅子编号
    seat_of = [0] * n        # 记录每个人的椅子，方便离开时使用

    for time, typ, idx in events:
        if typ == 0:                     # ---------- 离开 ----------
            # 从 busy 堆弹出对应的 (离开时间, 椅子编号)
            leave_time, chair = heapq.heappop(busy)
            # 这把椅子现在空了，放进 free 堆
            heapq.heappush(free, chair)
        else:                            # ---------- 到达 ----------
            # 若有空椅子直接取；否则使用全新椅子
            if free:
                chair = heapq.heappop(free)   # 取最小空椅子
            else:
                chair = next_seat
                next_seat += 1                # 新椅子编号递增

            seat_of[idx] = chair               # 记下 idx 的座位

            # 把这把椅子标记为占用，等它离开时再释放
            heapq.heappush(busy, (times[idx][1], chair))

            # 一旦是目标朋友，答案已确定
            if idx == targetFriend:
                return chair

    # 理论上不会走到这里
    return -1
```

> 代码中每一步都有中文注释，直接运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 先把 `2n` 条事件排序，需要 `O(n log n)`。  
  - 之后每条事件只做堆的 `push / pop`，每次都是 `O(log n)`，总共也是 `O(n log n)`。  
  - **对比**：相较于暴力的 `O(n²)`，当 `n` 达到 10⁴ 时，`n log n` 只有几万次操作，几乎瞬间完成。

- **空间复杂度**：`O(n)`  
  - `events`、`busy`、`free`、`seat_of` 三个列表最多各存 `O(n)` 条目，整体线性空间。

---

## 心得

- **核心技巧**：使用 **最小堆**（优先队列）同时维护“已占用的椅子”（按离开时间）和“空闲的椅子”（按编号），实现**即时释放**与**最小编号分配**。
- **适用的题型**  
  1. “会议室安排”类问题（按结束时间释放资源）。  
  2. “最小未使用的正整数”或“最小空闲的编号”类问题。  
  3. “飞机登机口分配”“CPU 任务调度”等需要动态分配最小编号资源的场景。
- **一句话总结解题钥匙**：  
  *“把‘谁先离开’和‘哪个座位号最小’分别放进两个最小堆，事件顺序处理，就能在对数时间内完成分配。”*

---

## 反思

- **第一反应**：直接模拟、每次线性扫描最小空椅子。虽然直观，却忽视了规模会导致超时。
- **最容易踩的坑**  
  - **离开和到达同一时刻**：必须先处理离开事件，否则新来的朋友会错过刚释放的椅子。  
  - **堆中离开的信息对应错误**：离开时一定要弹出对应的 `(离开时间, chair)`，否则会把错误的椅子释放回 `free`。  
  - **新椅子编号的递增**：当 `free` 为空时，需要使用一个全局计数 `next_seat`，不能随意取 `len(busy)`，因为 `busy` 包含已离开的元素。
- **下次类似题的第一步**：  
  “把所有时间点抽象成事件，按时间顺序遍历；遇到需要‘最小/最大’的资源时，先考虑用堆来维护。”