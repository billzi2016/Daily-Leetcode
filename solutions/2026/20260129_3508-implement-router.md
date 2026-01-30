# #3508. 实现路由器 / Implement Router

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Design、Queue、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/implement-router/)

---

## 题目（英文原版）

**Description**

Design a data structure that can efficiently manage data packets in a network router. Each data packet consists of the following attributes:
Implement the Router class:
Router(int memoryLimit): Initializes the Router object with a fixed memory limit.
bool addPacket(int source, int destination, int timestamp): Adds a packet with the given attributes to the router.
int[] forwardPacket(): Forwards the next packet in FIFO (First In First Out) order.
int getCount(int destination, int startTime, int endTime):
Note that queries for addPacket will be made in increasing order of timestamp.

**Examples**

**Example 1:**

```
Input: ["Router", "addPacket", "addPacket", "addPacket", "addPacket", "addPacket", "forwardPacket", "addPacket", "getCount"] [[3], [1, 4, 90], [2, 5, 90], [1, 4, 90], [3, 5, 95], [4, 5, 105], [], [5, 2, 110], [5, 100, 110]]
Output: [null, true, true, false, true, true, [2, 5, 90], true, 1]
Explanation
```

**Example 2:**

```
Input: ["Router", "addPacket", "forwardPacket", "forwardPacket"] [[2], [7, 4, 90], [], []]
Output: [null, true, [7, 4, 90], []]
Explanation
```

**Constraints**

- 2 <= memoryLimit <= 105
- 1 <= source, destination <= 2 * 105
- 1 <= timestamp <= 109
- 1 <= startTime <= endTime <= 109
- At most 105 calls will be made to addPacket, forwardPacket, and getCount methods altogether.
- queries for addPacket will be made in increasing order of timestamp.

---

## 题目（中文翻译）

设计一种数据结构，用于在网络路由器中高效管理数据包。每个数据包包含以下属性：

- **source**：数据包的来源节点  
- **destination**：数据包的目的节点  
- **timestamp**：数据包产生的时间戳

实现 `Router` 类：

```cpp
Router(int memoryLimit)                 // 初始化 Router 对象，设置固定的内存上限
bool addPacket(int source, int destination, int timestamp)   // 将具有给定属性的数据包加入路由器
int[] forwardPacket()                   // 按 FIFO（先进先出）顺序转发下一条数据包，返回该数据包的 [source, destination, timestamp]；若无可转发的数据包返回空数组
int getCount(int destination, int startTime, int endTime)    // 返回在时间区间 [startTime, endTime] 内、目的地为 destination 的数据包数量
```

**注意**：对 `addPacket` 的调用会按照递增的 `timestamp` 顺序出现。

---

### 示例 1

**输入**

```json
["Router", "addPacket", "addPacket", "addPacket", "addPacket", "addPacket", "forwardPacket", "addPacket", "getCount"]
[[3], [1, 4, 90], [2, 5, 90], [1, 4, 90], [3, 5, 95], [4, 5, 105], [], [5, 2, 110], [5, 100, 110]]
```

**输出**

```json
[null, true, true, false, true, true, [2, 5, 90], true, 1]
```

**解释**  
- `Router(3)` 创建一个内存上限为 3 的路由器。  
- `addPacket(1,4,90)` 成功加入，返回 `true`。  
- `addPacket(2,5,90)` 成功加入，返回 `true`。  
- `addPacket(1,4,90)` 因为已经有相同的 `source`、`destination`、`timestamp`，且内存已满，加入失败，返回 `false`。  
- `addPacket(3,5,95)` 成功加入，返回 `true`。  
- `addPacket(4,5,105)` 成功加入，返回 `true`。  
- `forwardPacket()` 按 FIFO 顺序转发最早的 `[2,5,90]`，返回该数组。  
- `addPacket(5,2,110)` 成功加入，返回 `true`。  
- `getCount(5,100,110)` 在时间区间 `[100,110]` 内目的地为 `5` 的数据包共有 1 条，返回 `1`。

---

### 示例 2

**输入**

```json
["Router", "addPacket", "forwardPacket", "forwardPacket"]
[[2], [7, 4, 90], [], []]
```

**输出**

```json
[null, true, [7, 4, 90], []]
```

**解释**  
- `Router(2)` 创建内存上限为 2 的路由器。  
- `addPacket(7,4,90)` 成功加入，返回 `true`。  
- 第一次 `forwardPacket()` 转发并返回 `[7,4,90]`。  
- 第二次 `forwardPacket()` 已无数据包可转发，返回空数组 `[]`。

---

### 约束条件

- `2 <= memoryLimit <= 10^5`
- `1 <= source, destination <= 2 * 10^5`
- `1 <= timestamp <= 10^9`
- `1 <= startTime <= endTime <= 10^9`
- `addPacket`、`forwardPacket`、`getCount` 方法的调用总次数不超过 `10^5` 次。
- 对 `addPacket` 的查询会按递增的 `timestamp` 顺序出现。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把路由器里所有的数据包全部存在一个普通的 **list**（或 Python 的 `list`）里，  
- `addPacket` 时直接把三元组 `[source, destination, timestamp]` `append` 到列表尾部。  
- `forwardPacket` 时把列表最前面的元素 `pop(0)`（相当于把队首弹出），返回它。  
- `getCount` 时遍历整个列表，统计 `destination` 相同且 `timestamp` 落在 `[startTime, endTime]` 区间的包的个数。

> **类比**：想象你有一根装满信件的长管子，想查找某个收件人的信件数量，就只能从头到尾一个一个检查。

**为什么能得到正确答案**  
- 所有操作都直接在真实的“存储”上完成，完全遵守题目对 FIFO、容量限制和查询的要求。  
- `addPacket`、`forwardPacket`、`getCount` 的行为都和题目描述一一对应，因而必然返回正确结果。

**复杂度分析（大白话）**  
- `addPacket`：只需要把元素放到列表尾部，时间大约是 **O(1)**（常数时间），空间随加入的包线性增长 **O(1)**（每次只占一点点额外空间）。  
- `forwardPacket`：把列表第一个元素弹出，`pop(0)` 必须把后面的所有元素往前搬一位，时间是 **O(n)**（n 为当前包的数量），空间不变 **O(1)**。  
- `getCount`：要遍历整个列表，最坏情况下要检查每一个包，时间是 **O(n)**，空间仍是 **O(1)**。  

> **O(n) 是什么意思？**  
> 假设现在路由器里有 10 000 包，`forwardPacket` 或 `getCount` 需要大约 10 000 步才能完成；如果包的数量翻倍到 20 000，所需的步数也会大约翻倍。  

---

#### 代码（Python）

```python
from typing import List

class Router:
    def __init__(self, memoryLimit: int):
        self.limit = memoryLimit          # 最大能存多少包
        self.buf: List[List[int]] = []   # 用普通列表模拟队列
        self.seen = set()                # 用集合防止重复插入

    # 暴力版：直接把包加入列表尾部
    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        key = (source, destination, timestamp)
        # 1) 内存已满 2) 已经有完全相同的包，都不能加入
        if len(self.buf) >= self.limit or key in self.seen:
            return False
        self.buf.append([source, destination, timestamp])
        self.seen.add(key)
        return True

    # 暴力版：弹出列表最前面的元素
    def forwardPacket(self) -> List[int]:
        if not self.buf:                     # 队列为空，返回空列表
            return []
        pkt = self.buf.pop(0)                # O(n) 的移动操作
        self.seen.remove(tuple(pkt))
        return pkt

    # 暴力版：遍历全部包计数
    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        cnt = 0
        for _, dst, ts in self.buf:
            if dst == destination and startTime <= ts <= endTime:
                cnt += 1
        return cnt
```

#### 复杂度

- **时间复杂度**  
  - `addPacket`：O(1)  
  - `forwardPacket`：O(n)（因为要把后面的元素整体前移）  
  - `getCount`：O(n)（要遍历全部包）  

- **空间复杂度**  
  - 额外空间 O(1)（只用了几个变量），但存放的包本身最多占 `memoryLimit` 个，整体是 O(memoryLimit)。

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈有两点：

1. **`forwardPacket` 的 O(n) 移动**  
   - 每次弹出队首都要把后面的所有元素往前搬，这在包很多时会非常慢。

2. **`getCount` 的全表遍历**  
   - 题目要求最多 10⁵ 次查询，如果每次都遍历全部包，整体时间会达到 O(10¹⁰)，明显超时。

我们要把这两个操作都降到 **对数级** 或 **常数级**。

---

#### 2.1 用 **双端队列（deque）** 替代普通 list  

Python 的 `collections.deque` 在两端的插入、弹出都是 **O(1)** 的。  
- `addPacket` → `deque.append`（在右端插入）  
- `forwardPacket` → `deque.popleft`（在左端弹出）  

这样 `forwardPacket` 就不需要搬移元素，时间降为 **O(1)**。

---

#### 2.2 为每个目的地维护 **有序时间戳列表**，配合 **二分查找**  

`getCount` 只需要统计 **某个目的地** 在时间区间 `[startTime, endTime]` 内的包数。  
思路：

- 对每个 `destination`，单独保存一个 **递增的时间戳序列**。  
  - 因为题目保证所有 `addPacket` 调用的 `timestamp` **是递增的**，我们可以直接把新时间戳 `append` 到对应序列的末尾，序列天然有序。  
- 当 `forwardPacket` 把某个包弹出时，说明该包是最早加入队列的，同样也是该目的地时间序列中最早的时间戳。我们只需要把它从序列的 **左端** 删除。  
  - 为了做到 O(1) 删除，我们可以把序列实现为 **list + 一个左指针（offset）**，或者直接使用 `deque`（但二分查找只能在随机访问的列表上进行）。这里选用 **list + offset**，因为二分查找只能在列表上完成。

**查询过程**（二分查找）：

- 对目标目的地的时间戳列表（已去掉前面已经弹出的部分）使用 `bisect_left` 找到 **第一个 ≥ startTime** 的位置 `l`，使用 `bisect_right` 找到 **第一个 > endTime** 的位置 `r`。  
- 区间 `[l, r)` 的长度即为答案，时间复杂度 **O(log k)**（k 为该目的地当前的包数）。

---

#### 2.3 防止重复包

题目示例表明，同样的 `(source, destination, timestamp)` 不能被插入两次。  
我们使用一个 **集合 `seen`** 来记录已经存在的三元组，插入前检查是否已在集合中。

---

#### 2.4 完整数据结构

| 成员 | 作用 | 备注 |
|------|------|------|
| `self.limit` | 最大可容纳的包数 | 只在 `addPacket` 时检查 |
| `self.queue` | `deque`，保存所有包的完整信息（source, destination, timestamp） | 实现 FIFO |
| `self.seen` | `set`，存放已存在的 `(source, destination, timestamp)` | 防止重复 |
| `self.time_map` | `defaultdict(list)`，`destination → [timestamps]`（递增） | 用于二分查找 |
| `self.offset` | `defaultdict(int)`，`destination → 已弹出数量` | 逻辑上相当于把列表左侧的元素“抛弃” |

---

#### 代码（Python）

```python
from collections import deque, defaultdict
from bisect import bisect_left, bisect_right
from typing import List

class Router:
    def __init__(self, memoryLimit: int):
        self.limit = memoryLimit                 # 最大容量
        self.queue = deque()                     # FIFO 队列，保存完整包信息
        self.seen = set()                        # 用于判重
        self.time_map = defaultdict(list)       # destination -> 按加入顺序递增的 timestamp 列表
        self.offset = defaultdict(int)          # destination -> 已经弹出的时间戳数量（逻辑左指针）

    # ------------------------------------------------------------------
    # 添加包
    # ------------------------------------------------------------------
    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        key = (source, destination, timestamp)
        # ① 内存已满 ② 已经存在相同的包 → 直接返回 False
        if len(self.queue) >= self.limit or key in self.seen:
            return False

        # ③ 正常加入
        self.queue.append([source, destination, timestamp])  # O(1)
        self.seen.add(key)                                    # O(1)

        # ④ 对应目的地的时间序列追加（因为 timestamp 单调递增，直接 append 即保持有序）
        self.time_map[destination].append(timestamp)          # O(1)
        return True

    # ------------------------------------------------------------------
    # 转发（弹出）最早进入的包
    # ------------------------------------------------------------------
    def forwardPacket(self) -> List[int]:
        if not self.queue:                     # 队列为空
            return []

        pkt = self.queue.popleft()             # O(1)
        src, dst, ts = pkt
        self.seen.remove((src, dst, ts))       # 把判重集合中对应的记录删掉

        # 对应目的地的时间序列左侧弹出一个时间戳
        # 实际上我们不真的删除列表的第一个元素，而是把 offset 加 1
        self.offset[dst] += 1

        return pkt

    # ------------------------------------------------------------------
    # 统计某个目的地在时间区间 [startTime, endTime] 的包数量
    # ------------------------------------------------------------------
    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        ts_list = self.time_map.get(destination, [])
        if not ts_list:                     # 该目的地根本没有包
            return 0

        left = self.offset[destination]          # 逻辑左指针
        # 二分查找只在 “有效区间” [left, len(ts_list)) 里进行
        l = bisect_left(ts_list, startTime, lo=left)   # 第一个 >= startTime
        r = bisect_right(ts_list, endTime, lo=left)    # 第一个 > endTime
        return r - l                               # 区间长度即为答案
```

#### 复杂度

- **时间复杂度**  
  - `addPacket`：**O(1)** —— 只做常数次集合、队列、列表的 `append`。  
  - `forwardPacket`：**O(1)** —— `deque.popleft` 与 offset 增加都是常数时间。  
  - `getCount`：**O(log k)**，其中 *k* 为该 `destination` 当前剩余的包数（二分查找）。相较于暴力的 O(n) 提升巨大。

- **空间复杂度**  
  - 所有数据结构总共只保存不超过 `memoryLimit` 条包的信息，以及每条包对应的时间戳一次。  
  - 因此整体 **O(memoryLimit)**，符合题目限制。

---

## 心得

- **核心技巧**：  
  1. 用 **双端队列** 实现 FIFO，保证 `forwardPacket` 为 O(1)。  
  2. 对每个查询维度（这里是 `destination`）维护 **有序的辅助结构**（时间戳列表），配合 **二分查找** 快速统计区间数量。  
  3. 利用题目给出的 **时间戳递增** 特性，让插入保持有序，无需额外排序。

- **适用的类似题型**  
  - “设计一个支持 O(1) 入队、出队并能快速查询区间计数的队列”。  
  - “在动态数据流中，要求对某个属性的区间统计，且插入顺序单调”。  
  - “实现带容量限制的缓存，并支持基于属性的快速计数”。

- **一句话总结**：**用 deque 解决 FIFO 的 O(1) 操作，用有序时间戳 + 二分查找把区间计数降到对数级**。

---

## 反思

- **第一反应**：直接用普通列表实现所有操作，代码最直观，却忽视了 `pop(0)` 的高昂代价。  
- **最容易踩的坑**  
  - **忘记判重**：如果不维护 `seen`，相同的包会被多次加入，导致 `addPacket` 返回错误的 `True`。  
  - **删除时间戳时的效率**：若真的在列表左端 `pop(0)`，会把二分查找的优势全部抵消。使用 offset（或 deque）才是真正的 O(1) 删除。  
  - **二分查找的范围**：一定要把已经弹出的部分（`offset`）排除，否则会把已经不在队列里的时间戳计进去。  

- **下次遇到同类题**：第一步先思考 “这道题需要**快速的两端操作**吗？” → 若是，立刻选 `deque`；再检查 “是否有**单调/有序**的属性可以用于二分查找”。这样可以快速定位到最优的数据结构组合。