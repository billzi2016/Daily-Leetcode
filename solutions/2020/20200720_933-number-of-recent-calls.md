# #933. 最近的调用次数 / Number of Recent Calls

> 难度：简单 · 标签：Design、Queue、Data Stream · [LeetCode 链接](https://leetcode.com/problems/number-of-recent-calls/)

---

## 题目（英文原版）

**Description**

You have a RecentCounter class which counts the number of recent requests within a certain time frame.
Implement the RecentCounter class:
It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.

**Examples**

**Example 1:**

```
Input
["RecentCounter", "ping", "ping", "ping", "ping"]
[[], [1], [100], [3001], [3002]]
Output
[null, 1, 2, 3, 3]

Explanation
RecentCounter recentCounter = new RecentCounter();
recentCounter.ping(1);     // requests = [1], range is [-2999,1], return 1
recentCounter.ping(100);   // requests = [1, 100], range is [-2900,100], return 2
recentCounter.ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3
```

**Constraints**

- 1 <= t <= 109
- Each test case will call ping with strictly increasing values of t.
- At most 104 calls will be made to ping.

---

## 题目（中文翻译）

你需要实现一个 `RecentCounter` 类，用于统计在特定时间窗口内的最近请求数量。

实现 `RecentCounter` 类，使其满足以下要求：

- 每次调用 `ping(t)` 时，`t` 均严格大于上一次调用的 `t`（保证时间递增）。
- `ping(t)` 返回最近 **3000 毫秒**（包括 `t` 本身）内的请求次数，即统计所有满足 `t - 3000 <= requestTime <= t` 的请求。

### 示例

```json
Input
["RecentCounter", "ping", "ping", "ping", "ping"]
[[], [1], [100], [3001], [3002]]
Output
[null, 1, 2, 3, 3]
```

**解释**

```java
RecentCounter recentCounter = new RecentCounter();
recentCounter.ping(1);     // requests = [1]，范围为 [-2999, 1]，返回 1
recentCounter.ping(100);   // requests = [1, 100]，范围为 [-2900, 100]，返回 2
recentCounter.ping(3001);  // requests = [1, 100, 3001]，范围为 [1, 3001]，返回 3
recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002]，范围为 [2, 3002]，返回 3
```

### 约束条件

- `1 <= t <= 10^9`
- 每个测试用例中的 `ping` 调用的 `t` 值严格递增。
- 最多会调用 `ping` `10^4` 次。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们需要实现一个 `RecentCounter`，它的 `ping(t)` 方法返回「最近 3000 毫秒」内（即 `[t‑3000, t]` 区间）所有请求的数量。  

最直接的想法是：  
1. 用一个普通的 **列表**（list）把每一次 `ping` 的时间 `t` 都记下来。  
2. 当有新的 `ping(t)` 时，遍历整个列表，统计有多少时间落在 `[t‑3000, t]` 区间。  

> **类比**：列表就像一本顺序排列的日记本，记下每一次打电话的时间。要统计最近三秒的通话次数，就得把整本日记一本一本翻，看看哪些日期在这三秒内。

**为什么正确**  
因为我们把所有请求的时间都完整保存了，遍历时只要检查每个时间是否在合法区间，就一定能得到正确的计数。

#### 代码（Python）

```python
from typing import List

class RecentCounter:
    def __init__(self):
        # 用一个列表保存所有 ping 的时间戳
        self.history: List[int] = []

    def ping(self, t: int) -> int:
        # 把当前时间加入列表
        self.history.append(t)

        # 统计落在 [t-3000, t] 区间的时间个数
        cnt = 0
        for time in self.history:
            if t - 3000 <= time <= t:   # 区间判断
                cnt += 1
        return cnt
```

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n` 是已经调用 `ping` 的次数。每一次 `ping` 都要遍历所有历史记录，最坏情况下会看 `n` 次。  
  > 大白话：如果已经打了 1000 次电话，第 1001 次查询要看 1000 条记录，时间会随记录数线性增长。

- **空间复杂度**：`O(n)`，因为我们把每一次的时间戳都存到了列表里，列表长度等于调用次数。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都遍历全部历史记录**，这会导致时间随调用次数线性增长。  
观察题目有两个关键点可以帮助我们优化：

1. **时间戳严格递增**  
   每一次 `ping(t)` 的 `t` 都比上一次大，这意味着旧的请求永远不会再出现新的 “最近 3000ms” 区间之外的情况。

2. **只关心最近 3000ms 内的请求**  
   超出这个区间的时间点再也不会对后面的答案产生影响，可以直接丢弃。

基于这两点，我们可以使用 **队列（Queue）** 来维护「只剩下最近 3000ms 的时间戳」：

- 队列的左端（`front`）保存最早的请求时间。  
- 当新 `t` 来了，先把 `t` 加入队列尾部。  
- 然后不断检查队列头部的时间是否小于 `t‑3000`，如果是，就把它弹出（`popleft`），因为它已经不再是“最近 3000ms”内的请求。  
- 最终队列里剩下的元素个数就是答案。

> **类比**：想象你在排队买咖啡，店里只允许最近三秒进入的顾客排队。每当有新顾客进来，你把他放到队尾，然后把已经等了超过三秒的顾客赶走。队列里剩下的就是还能买咖啡的人数。

Python 标准库的 `collections.deque` 正好提供了 **两端都能 O(1) 进行插入和删除** 的队列。

#### 代码（Python）

```python
from collections import deque
from typing import Deque

class RecentCounter:
    def __init__(self):
        # 用双端队列保存最近 3000ms 以内的时间戳
        self.q: Deque[int] = deque()

    def ping(self, t: int) -> int:
        # 1. 把当前时间加入队列尾部
        self.q.append(t)

        # 2. 删除所有早于 t-3000 的时间点
        #    队列头部最早的时间如果已经超出窗口，就弹出
        while self.q and self.q[0] < t - 3000:
            self.q.popleft()   # O(1) 删除最左侧元素

        # 3. 队列当前的长度就是最近 3000ms 内的请求数
        return len(self.q)
```

#### 复杂度  

- **时间复杂度**：`O(1)` 均摊（amortized）。每一次 `ping` 只会把当前时间加入一次，并且每个时间戳最多被弹出一次。整体来看，`n` 次调用总共只做了 `O(n)` 次入队和出队操作，摊到每次就是常数时间。  
  > 与暴力解对比：不再随历史记录增长而线性变慢。

- **空间复杂度**：`O(k)`，其中 `k` 是任意时刻窗口内的请求数，最坏情况下 `k ≤ 3001`（因为时间戳是整数且递增，最多每毫秒出现一次）。在题目限制 `最多 10⁴ 次调用` 的前提下，空间最多是 `O(10⁴)`，远小于保存全部历史记录的 `O(n)`。

---

## 心得  

- **核心技巧**：利用「单调递增」的特性，用**队列**维护滑动窗口（最近 3000ms）中的元素。  
- **适用场景**：  
  1. 「滑动窗口计数」类问题，如统计最近 `k` 秒内的请求数。  
  2. 「最近 `k` 次」类查询，例如最近 `k` 条聊天记录。  
  3. 「窗口最大值/最小值」问题（配合单调队列）。  
- **一句话总结**：**只保留窗口内的元素，过期的立即丢弃，用队列实现 O(1) 的滑动窗口。**

---

## 反思  

- **第一反应**：看到“最近 3000ms”就想到遍历全部记录，直接统计。  
- **最容易踩的坑**：  
  - 忘记在弹出元素时使用 `< t-3000`（而不是 `<=`），否则会把恰好在左边界的合法请求误删。  
  - 没有利用时间递增的性质，导致实现复杂度更高。  
- **下次遇到同类题**：第一步想到「把时间戳放进队列」，然后「循环弹出队首直到满足窗口条件」，这样就能直接得到答案。