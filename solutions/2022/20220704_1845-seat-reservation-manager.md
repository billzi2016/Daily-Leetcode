# #1845. 座位预订管理器 / Seat Reservation Manager

> 难度：中等 · 标签：Design、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/seat-reservation-manager/)

---

## 题目（英文原版）

**Description**

Design a system that manages the reservation state of n seats that are numbered from 1 to n.
Implement the SeatManager class:

**Examples**

**Example 1:**

```
Input
["SeatManager", "reserve", "reserve", "unreserve", "reserve", "reserve", "reserve", "reserve", "unreserve"]
[[5], [], [], [2], [], [], [], [], [5]]
Output
[null, 1, 2, null, 2, 3, 4, 5, null]

Explanation
SeatManager seatManager = new SeatManager(5); // Initializes a SeatManager with 5 seats.
seatManager.reserve();    // All seats are available, so return the lowest numbered seat, which is 1.
seatManager.reserve();    // The available seats are [2,3,4,5], so return the lowest of them, which is 2.
seatManager.unreserve(2); // Unreserve seat 2, so now the available seats are [2,3,4,5].
seatManager.reserve();    // The available seats are [2,3,4,5], so return the lowest of them, which is 2.
seatManager.reserve();    // The available seats are [3,4,5], so return the lowest of them, which is 3.
seatManager.reserve();    // The available seats are [4,5], so return the lowest of them, which is 4.
seatManager.reserve();    // The only available seat is seat 5, so return 5.
seatManager.unreserve(5); // Unreserve seat 5, so now the available seats are [5].
```

**Constraints**

- 1 <= n <= 105
- 1 <= seatNumber <= n
- For each call to reserve, it is guaranteed that there will be at least one unreserved seat.
- For each call to unreserve, it is guaranteed that seatNumber will be reserved.
- At most 105 calls in total will be made to reserve and unreserve.

---

## 题目（中文翻译）

设计一个系统来管理编号从 **1** 到 **n** 的 **n** 个座位的预订状态。

实现 `SeatManager` 类：

```text
SeatManager(int n)      // 初始化一个拥有 n 个座位的 SeatManager
int reserve()           // 预订一个座位，返回当前可用的编号最小的座位号
void unreserve(int seatNumber) // 取消对 seatNumber 的预订，使其重新可用
```

**示例 1：**

```json
Input
["SeatManager", "reserve", "reserve", "unreserve", "reserve", "reserve", "reserve", "reserve", "unreserve"]
[[5], [], [], [2], [], [], [], [], [5]]

Output
[null, 1, 2, null, 2, 3, 4, 5, null]
```

**解释**  
```java
SeatManager seatManager = new SeatManager(5); // 初始化一个拥有 5 个座位的 SeatManager。
seatManager.reserve();    // 此时所有座位均可用，返回编号最小的座位 1。
seatManager.reserve();    // 返回编号最小的未被预订的座位 2。
seatManager.unreserve(2); // 取消对座位 2 的预订，使其重新可用。
seatManager.reserve();    // 再次预订，返回编号最小的可用座位 2。
seatManager.reserve();    // 返回 3。
seatManager.reserve();    // 返回 4。
seatManager.reserve();    // 返回 5。
seatManager.unreserve(5); // 取消对座位 5 的预订。
```

**约束条件**

- `1 <= n <= 10^5`
- `1 <= seatNumber <= n`
- 对每一次 `reserve` 调用，保证至少有一个未被预订的座位。
- 对每一次 `unreserve` 调用，保证 `seatNumber` 当前已被预订。
- `reserve` 和 `unreserve` 的调用总次数不超过 `10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个座位的使用情况记在一个长度为 `n` 的数组里，`True` 表示已被占用，`False` 表示空闲。  
- **数据结构**：`list[bool]`，相当于我们在纸上画了 `n` 把椅子，勾掉的表示有人坐了，空的表示还能坐。  
- **reserve**（预订）时，从座位 1 开始顺序检查，找到第一个 `False` 就返回它的编号，并把它标记为 `True`。  
- **unreserve**（取消预订）时，只需要把对应下标的位置改回 `False` 即可。

这种做法**一定能得到正确答案**，因为我们遍历了所有座位，必然能找到当前最小的空座。

#### 代码（Python）

```python
class SeatManager:
    def __init__(self, n: int):
        # 用一个布尔数组记录座位是否被占用，全部初始化为 False（未占用）
        self.n = n
        self.taken = [False] * (n + 1)   # 1-indexed，省去下标转换

    def reserve(self) -> int:
        """
        线性扫描找到最小的未被占用的座位编号
        """
        for seat in range(1, self.n + 1):
            if not self.taken[seat]:      # 发现空座位
                self.taken[seat] = True   # 标记为已占用
                return seat
        # 根据题目保证，这里永远不会执行到

    def unreserve(self, seatNumber: int) -> None:
        """
        直接把对应位置改回 False，即可取消预订
        """
        self.taken[seatNumber] = False
```

#### 复杂度  

- **时间复杂度**  
  - `reserve`：最坏情况下要检查所有 `n` 把座位，**O(n)**。可以把 O(n) 想象成“最多要走 n 步”。  
  - `unreserve`：直接定位下标，**O(1)**（常数时间）。  

- **空间复杂度**  
  - 只用了一个长度为 `n+1` 的布尔数组，**O(n)** 的额外空间。  

> 这套方案在 `n` 很小或者调用次数很少时还能接受，但当 `n` 达到 10⁵、操作次数也达 10⁵ 时，`reserve` 的线性扫描会导致超时。

---

### 2. 最优解

#### 思路  

从暴力解可以看到瓶颈在 **每次预订都要遍历整个座位表**。我们需要一种数据结构，能够：

1. **快速取出当前最小的空座位**（类似“取字典里最小的键”），
2. **快速把座位号重新放回可用集合**（相当于“把词重新装进字典”），
3. 同时保持 **合理的空间使用**。

这正好符合 **最小堆（Min‑Heap）** 的特性：

- 堆是一棵近似完全二叉树，根节点始终是所有元素中的最小值。  
- 取出最小值（`heappop`）和插入新值（`heappush`）的时间都是 **O(log n)**，即“最多走几层树的高度”，而高度约为 `log₂ n`，远远小于 `n`。  
- Python 标准库 `heapq` 已经实现了最小堆，只需要把座位号当作整数放进去即可。

实现细节：

1. **初始化**：把 `1 … n` 全部压入堆，堆顶自然是 `1`（最小的空座位）。  
2. **reserve**：`heappop` 堆顶即得到当前最小的可用座位号。  
3. **unreserve**：把被释放的座位号重新 `heappush` 进堆，让它重新参与“最小座位”竞争。

> 这里的堆相当于一个 **“随时能拿到最小编号的空座位盒子”**，每次取出或放入都很快。

#### 代码（Python）

```python
import heapq

class SeatManager:
    def __init__(self, n: int):
        """
        初始化时把所有座位编号放进最小堆。
        heapq 实现的是最小堆，根节点总是最小值。
        """
        self.available = list(range(1, n + 1))   # 1, 2, ..., n
        heapq.heapify(self.available)           # O(n) 把列表变成堆

    def reserve(self) -> int:
        """
        取出堆顶（最小的空座位），时间复杂度 O(log n)
        """
        seat = heapq.heappop(self.available)    # 弹出最小座位号
        return seat

    def unreserve(self, seatNumber: int) -> None:
        """
        把释放的座位号重新放进堆，时间复杂度 O(log n)
        """
        heapq.heappush(self.available, seatNumber)
```

#### 复杂度  

- **时间复杂度**  
  - `reserve`：`heappop` 为 **O(log n)**，即“只需走树的高度”。  
  - `unreserve`：`heappush` 也是 **O(log n)**。  
  与暴力解的 **O(n)** 相比，提升巨大，尤其在 `n` 很大时几乎是“瞬间完成”。  

- **空间复杂度**  
  - 堆中最多存放所有空座位，最坏情况是全部座位空闲，仍是 **O(n)**。  
  - 与暴力解的空间相同，但不需要额外的布尔数组，实际常数更小。

---

## 心得

- **核心技巧**：使用最小堆（优先队列）维护「可用座位集合」，实现「随时取最小」和「快速归还」两种操作。  
- **适用的题型**  
  1. “获取最小/最大未使用编号” 类问题，如 **Design Phone Directory**、**Find Smallest Missing Positive**（需要快速找缺失的最小正整数）。  
  2. “动态调度资源” 场景，如 **Task Scheduler**（按优先级取任务）。  
- **一句话总结解题钥匙**：**把「空座位」抽象成一个「最小堆」，每次取最小、归还即插入，即可在对数时间内完成预订和取消。**

## 反思

- **第一反应**：直接用数组遍历寻找最小空位，想到“把所有座位都记下来”。  
- **最容易踩的坑**  
  - 忽视 `reserve` 的线性扫描会导致超时。  
  - 在手写堆实现时容易忘记「堆化」的过程，导致堆属性被破坏。  
  - `unreserve` 必须保证不会出现重复的座位号进入堆，否则后续 `reserve` 可能返回已经被占用的座位。  
- **下次遇到同类题的第一步**：问自己「我需要快速获取当前最小（或最大）可用元素吗？」如果答案是「是」，立刻想到 **堆 / 有序集合**，把问题抽象为「取最小/最大」+「插入」的组合。