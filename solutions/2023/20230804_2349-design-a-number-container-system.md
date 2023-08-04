# #2349. 设计数字容器系统 / Design a Number Container System

> 难度：中等 · 标签：Hash Table、Design、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/design-a-number-container-system/)

---

## 题目（英文原版）

**Description**

Design a number container system that can do the following:
Implement the NumberContainers class:

**Examples**

**Example 1:**

```
Input
["NumberContainers", "find", "change", "change", "change", "change", "find", "change", "find"]
[[], [10], [2, 10], [1, 10], [3, 10], [5, 10], [10], [1, 20], [10]]
Output
[null, -1, null, null, null, null, 1, null, 2]

Explanation
NumberContainers nc = new NumberContainers();
nc.find(10); // There is no index that is filled with number 10. Therefore, we return -1.
nc.change(2, 10); // Your container at index 2 will be filled with number 10.
nc.change(1, 10); // Your container at index 1 will be filled with number 10.
nc.change(3, 10); // Your container at index 3 will be filled with number 10.
nc.change(5, 10); // Your container at index 5 will be filled with number 10.
nc.find(10); // Number 10 is at the indices 1, 2, 3, and 5. Since the smallest index that is filled with 10 is 1, we return 1.
nc.change(1, 20); // Your container at index 1 will be filled with number 20. Note that index 1 was filled with 10 and then replaced with 20. 
nc.find(10); // Number 10 is at the indices 2, 3, and 5. The smallest index that is filled with 10 is 2. Therefore, we return 2.
```

**Constraints**

- 1 <= index, number <= 109
- At most 105 calls will be made in total to change and find.

---

## 题目（中文翻译）

设计一个数字容器系统，使其能够执行以下操作：

**实现 `NumberContainers` 类**  
- `NumberContainers()`：初始化数字容器系统。  
- `void change(int index, int number)`：将下标 `index` 处的数字改为 `number`。如果该下标原本已有数字，则覆盖原有值。  
- `int find(int number)`：返回最小的下标 `index`，使得该下标被填入了 `number`。如果不存在这样的下标，返回 `-1`。

---

### 示例

```json
Input
["NumberContainers", "find", "change", "change", "change", "change", "find", "change", "find"]
[[], [10], [2, 10], [1, 10], [3, 10], [5, 10], [10], [1, 20], [10]]

Output
[null, -1, null, null, null, null, 1, null, 2]
```

**解释**
```java
NumberContainers nc = new NumberContainers();
nc.find(10);          // 还没有下标被填入数字 10，返回 -1。
nc.change(2, 10);     // 将下标 2 处的数字设为 10。
nc.change(1, 10);     // 将下标 1 处的数字设为 10。
nc.change(3, 10);     // 将下标 3 处的数字设为 10。
nc.change(5, 10);     // 将下标 5 处的数字设为 10。
nc.find(10);          // 当前填入数字 10 的下标有 {1,2,3,5}，最小的是 1，返回 1。
nc.change(1, 20);     // 将下标 1 处的数字改为 20，原来的 10 被移除。
nc.find(10);          // 现在填入数字 10 的下标为 {2,3,5}，最小的是 2，返回 2。
```

---

### 约束条件

- `1 <= index, number <= 10^9`
- `change` 与 `find` 的调用总次数不超过 `10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把「容器」想成一张 **大表**，下标 `index` 对应表格中的位置，里面保存的是 `number`。  
- **`change(index, number)`**：把表格第 `index` 格的值改成 `number`。  
- **`find(number)`**：遍历整张表，找出所有等于 `number` 的下标，返回最小的那个；如果没有出现就返回 `-1`。

> **类比**：把表格想象成一本电话号码簿，`index` 是「姓名」的位置，`number` 是「电话号码」。要改号只要把对应位置改掉；要找某个号码就把整本簿子从头到尾翻一遍，看到相同的号码就记下它的页码（下标），最后取最小的页码。

**为什么正确**  
因为我们把所有信息都保存在表格里，`find` 把表格每一格都检查一遍，必然能找到所有等于目标 `number` 的下标，取最小的就是答案。

**复杂度分析**（大白话）  
- `change` 只改动一个格子，时间是 **O(1)**（常数时间），空间不变。  
- `find` 要把整张表遍历一遍，表格长度记作 `N`，所以时间是 **O(N)**。如果表格非常大（题目里 `index` 最大可达 `10^9`），遍历一次几乎是不可能的。  
- 额外空间只用来保存这张表，大小也是 **O(N)**。

> **O(N)** 的含义：如果表格里有 10 万格，`find` 大约要检查 10 万次；如果有 100 万格，就要检查 100 万次，时间会随表格大小线性增长。

#### 代码（Python）

```python
class NumberContainers:
    def __init__(self):
        # 用字典模拟“表格”，只保存出现过的 index，未出现的默认不存在
        self.idx_to_num = {}          # index -> number

    # 把 index 位置的值改成 number
    def change(self, index: int, number: int) -> None:
        self.idx_to_num[index] = number   # 直接覆盖，时间 O(1)

    # 返回最小的 index，使得该位置的数恰好是 number
    def find(self, number: int) -> int:
        min_idx = float('inf')           # 记录目前找到的最小下标
        for idx, val in self.idx_to_num.items():   # 遍历所有已出现的下标
            if val == number:
                if idx < min_idx:
                    min_idx = idx
        return -1 if min_idx == float('inf') else min_idx
```

#### 复杂度

- **时间复杂度**  
  - `change`：`O(1)`（只改一个字典条目）  
  - `find`：`O(N)`，`N` 为当前已经出现过的不同 `index` 数量。  
  - 解释：`find` 需要检查每一个已经存储的下标，数量越多耗时越多。

- **空间复杂度**  
  - `O(N)`，我们把所有出现过的 `index` 和对应的 `number` 都保存在字典里。

> 这种暴力解在实际测试里会超时，因为题目最多会调用 `find`/`change` `10^5` 次，而 `index` 的范围可以非常大，遍历所有下标根本不现实。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于 `find`：每次都要遍历全部下标。  
我们需要一种数据结构，能够 **快速定位**「某个 `number` 所对应的最小 `index`」。  
这正好可以用 **「有序集合」**（Ordered Set）来实现：  
- 对每个 `number`，维护一个**有序集合**，里面装的是所有当前**等于该 `number` 的 `index`**。  
- 有序集合可以在 **O(log k)** 时间内插入、删除，并且能够在 **O(1)**（或 O(log k)）时间直接得到最小元素。

Python 标准库没有直接的「有序集合」实现，但我们可以用 **最小堆（heap）** + **懒删** 的技巧来模拟：

1. **两个哈希表**（字典）  
   - `idx_to_num`：`index → number`（记录每个位置当前的数）  
   - `num_to_heap`：`number → min‑heap`（每个数对应一个最小堆，堆里放所有出现过的 `index`）

2. **`change(index, number)`**  
   - 先查出 `index` 以前对应的旧数 `old`（如果之前没有出现过则为 `None`）。  
   - 把 `idx_to_num[index] = number` 更新。  
   - 把 `index` **压入** `num_to_heap[number]`（因为现在它属于 `number`）。  
   - **不必立即从旧数的堆里删除** `index`，因为堆不支持高效的任意位置删除。我们把这件事留到 `find` 时再处理（懒删）。

3. **`find(number)`**  
   - 取出 `num_to_heap[number]`（如果不存在直接返回 `-1`）。  
   - 不断检查堆顶 `idx` 是否仍然对应 `number`（即 `idx_to_num.get(idx) == number`）。  
       - 如果是，说明堆顶是合法的最小下标，直接返回。  
       - 如果不是，说明这条记录已经被后面的 `change` 移走了，**弹出**堆顶并继续检查下一个。  
   - 当堆空了仍未找到合法下标，返回 `-1`。

> **类比**：  
> - 把每个 `number` 想象成一本「索引簿」，簿子里按页码（`index`）从小到大排好。  
> - 当我们把某页的内容改成别的 `number` 时，只是把这页的号码写在新簿子里，同时旧簿子里这页的记录会「过时」。在查询时，我们先翻到簿子最前面（堆顶），如果这页已经被改走，就把它撕掉（弹出），继续看下一页，直到找到一页仍然属于该簿子。

#### 代码（Python）

```python
import heapq
from collections import defaultdict

class NumberContainers:
    def __init__(self):
        # index -> 当前的 number
        self.idx_to_num = {}

        # number -> min‑heap(保存所有出现过的 index)
        # 使用 defaultdict，第一次访问时会自动创建空列表
        self.num_to_heap = defaultdict(list)

    # 把 index 位置的数改成 number
    def change(self, index: int, number: int) -> None:
        old = self.idx_to_num.get(index)          # 以前的数，可能是 None
        if old == number:                         # 没有实质变化，直接返回
            return

        # ① 更新全局映射
        self.idx_to_num[index] = number

        # ② 把 index 放进新的 number 对应的堆
        heapq.heappush(self.num_to_heap[number], index)
        # 注意：旧的 number 对应的堆里仍然保留 index，
        #       这条「脏数据」会在 find 时被懒删掉

    # 返回最小的 index，使得该位置的数恰好是 number
    def find(self, number: int) -> int:
        heap = self.num_to_heap.get(number)
        if not heap:               # 从未出现过该 number
            return -1

        # 懒删：弹出所有已经不属于该 number 的下标
        while heap:
            idx = heap[0]                         # 堆顶元素（最小 index）
            # 检查这条记录是否仍然有效
            if self.idx_to_num.get(idx) == number:
                return idx                       # 合法且最小，直接返回
            heapq.heappop(heap)                  # 已失效，弹出继续检查

        # 堆全部被弹光，说明没有合法的 index
        return -1
```

#### 复杂度

- **时间复杂度**  
  - `change`：`O(log k)`，其中 `k` 为该 `number` 当前堆的大小（插入堆的代价）。在最坏情况下 `k ≤ N`，但整体上仍然是 **对数级**，远快于线性遍历。  
  - `find`：平均 **O(log k)**。每次可能会弹出若干「脏」元素，但每个元素最多被弹出一次，累计摊销后仍是对数级。  
  - 与暴力解相比，`find` 从 `O(N)` 降到了 `O(log N)`，即使 `N` 达到 `10^5` 也毫无压力。

- **空间复杂度**  
  - `O(N)`，需要保存所有出现过的 `index`（在 `idx_to_num`）以及每个 `number` 对应的堆（总元素数也是 `N`）。  
  - 这里的 `N` 是实际调用 `change` 时出现的不同 `index` 数量，最多 `10^5`，符合题目限制。

> **对数 O(log N) 的含义**：如果有 10 万个下标，`log₂10⁵ ≈ 17`，也就是说一次 `find` 或 `change` 只需要大约十几步操作，而不是十万步。

---

## 心得

- **核心技巧**：**哈希表 + 有序集合（这里用最小堆 + 懒删）**，实现「数 → 下标集合」的快速查询与维护。  
- **适用的题型**  
  1. **按值查最小/最大下标**（如 LeetCode 1825 `Finding the Minimum Possible Integer After at Most K Adjacent Swaps on Digits` 中的类似思路）。  
  2. **需要维护「每个值的出现位置」并快速获取极值**（如 352. `Data Stream as Disjoint Intervals` 的区间合并思路）。  
  3. **需要频繁更新并查询最小/最大元素的设计题**（如 1557. `Minimum Number of Operations to Make Array Sorted`）。  
- **一句话总结解题钥匙**：  
  > 用哈希表把「下标 ↔︎ 数」的对应关系记下来，用有序结构（堆）把「数 → 所有下标」维护成随时可取最小的集合，查询时把「已经失效」的元素懒惰地弹出即可。

---

## 反思

- **拿到题目第一反应**：直接用字典保存 `index → number`，`find` 暴力遍历。  
- **最容易踩的坑**  
  - `index`、`number` 范围高达 `10⁹`，不能用数组直接下标访问。  
  - `find` 需要 **最小** 的下标，不能随便返回任意一个匹配的下标。  
  - 在 `change` 时，旧的 `index` 必须从旧数对应的集合中删除，否则会导致 `find` 误判。直接在堆里删除代价高，用 **懒删** 可以避免。  
- **下次遇到同类题**，第一步应该想到：  
  > “是否可以把每个值的所有出现位置放进一个能够快速取最小（或最大）元素的有序结构？”  
  如果答案是“是”，就立刻上哈希表 + 有序集合（堆、平衡树、SortedList）这条路。