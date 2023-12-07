# #2502. **设计内存分配器** / Design Memory Allocator

> 难度：中等 · 标签：Array、Hash Table、Design、Simulation · [LeetCode 链接](https://leetcode.com/problems/design-memory-allocator/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the size of a 0-indexed memory array. All memory units are initially free.
You have a memory allocator with the following functionalities:
Note that:
Implement the Allocator class:

**Examples**

**Example 1:**

```
Input
["Allocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate", "allocate", "freeMemory", "allocate", "freeMemory"]
[[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]]
Output
[null, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]

Explanation
Allocator loc = new Allocator(10); // Initialize a memory array of size 10. All memory units are initially free.
loc.allocate(1, 1); // The leftmost block's first index is 0. The memory array becomes [1,_,_,_,_,_,_,_,_,_]. We return 0.
loc.allocate(1, 2); // The leftmost block's first index is 1. The memory array becomes [1,2,_,_,_,_,_,_,_,_]. We return 1.
loc.allocate(1, 3); // The leftmost block's first index is 2. The memory array becomes [1,2,3,_,_,_,_,_,_,_]. We return 2.
loc.freeMemory(2); // Free all memory units with mID 2. The memory array becomes [1,_, 3,_,_,_,_,_,_,_]. We return 1 since there is only 1 unit with mID 2.
loc.allocate(3, 4); // The leftmost block's first index is 3. The memory array becomes [1,_,3,4,4,4,_,_,_,_]. We return 3.
loc.allocate(1, 1); // The leftmost block's first index is 1. The memory array becomes [1,1,3,4,4,4,_,_,_,_]. We return 1.
loc.allocate(1, 1); // The leftmost block's first index is 6. The memory array becomes [1,1,3,4,4,4,1,_,_,_]. We return 6.
loc.freeMemory(1); // Free all memory units with mID 1. The memory array becomes [_,_,3,4,4,4,_,_,_,_]. We return 3 since there are 3 units with mID 1.
loc.allocate(10, 2); // We can not find any free block with 10 consecutive free memory units, so we return -1.
loc.freeMemory(7); // Free all memory units with mID 7. The memory array remains the same since there is no memory unit with mID 7. We return 0.
```

**Constraints**

- 1 <= n, size, mID <= 1000
- At most 1000 calls will be made to allocate and freeMemory.

---

## 题目（中文翻译）

给定一个整数 `n`，表示一个 0 起始下标的内存数组的大小。最初所有内存单元均为空闲。

请实现一个内存分配器（memory allocator），它支持如下功能：

* `Allocator(int n)`  
  构造函数，初始化大小为 `n` 的内存数组，所有单元均为空闲。

* `int allocate(int size, int mID)`  
  为标识为 `mID` 的进程（process）分配一段连续的 `size` 个内存单元。  
  - 必须从左到右查找，返回能够满足需求的 **最左**（起始下标最小）的连续空闲区间的起始下标。  
  - 若不存在足够大的连续空闲区间，则返回 `-1`。  
  - 分配成功后，这段区间的所有单元均被标记为已占用，并关联到 `mID`。

* `int freeMemory(int mID)`  
  释放所有 **已分配给 `mID` 的内存单元**，并返回本次释放的单元总数。  
  - 释放后，这些单元重新变为 **空闲**（free）。  
  - 若 `mID` 没有对应的已分配内存，则返回 `0`。

> **注意**
> - 同一 `mID` 可能会多次调用 `allocate`，产生不相连的多个区间；`freeMemory` 必须一次性释放该 `mID` 所有区间。
> - `allocate` 与 `freeMemory` 的调用次数均不超过 1000 次。

---

### 示例

```text
Input
["Allocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate", "allocate", "freeMemory", "allocate", "freeMemory"]
[[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]]
Output
[null, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]
```

**解释**  
```java
Allocator loc = new Allocator(10); // 初始化一个大小为 10 的内存数组，所有单元均为空闲。
loc.allocate(1, 1); // 返回 0，分配下标 0 的单元给 mID = 1
loc.allocate(1, 2); // 返回 1，分配下标 1 的单元给 mID = 2
loc.allocate(1, 3); // 返回 2，分配下标 2 的单元给 mID = 3
loc.freeMemory(2);  // 释放 mID = 2 的所有单元，返回 1（下标 1 被释放）
loc.allocate(3, 4); // 返回 3，分配下标 3~5 的 3 个单元给 mID = 4
loc.allocate(1, 1); // 返回 1，分配下标 1 的单元给 mID = 1（因为它是最左的空闲位）
loc.allocate(1, 1); // 返回 6，分配下标 6 的单元给 mID = 1
loc.freeMemory(1);  // 释放 mID = 1 的所有单元（下标 0、1、6），返回 3
loc.allocate(10, 2);// 返回 -1，无法找到长度为 10 的连续空闲区间
loc.freeMemory(7);  // mID = 7 没有分配记录，返回 0
```

---

### 约束

- `1 <= n, size, mID <= 1000`
- `allocate` 与 `freeMemory` 的调用总次数不超过 `1000` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把内存看成一个长度为 `n` 的数组 `mem[0 … n-1]`，  
- **空闲** 用 `0` 表示，  
- **已分配** 用对应的 `mID`（内存块的标识）填入。

> **类比**：把内存想象成一本字典，`0` 就是“未写页”，`mID` 就是“某本书的页码”。  
> 只要遍历这本字典，就能看到每一页是空的还是已经被某本书占用了。

**allocate(size, mID)**  
1. 从左到右扫描 `mem`，找连续的 `size` 个 `0`（空闲）的位置。  
2. 找到后把这段位置全部写成 `mID`，返回这段的左端下标。  
3. 若遍历完都找不到，则返回 `-1`。

**freeMemory(mID)**  
遍历整条内存数组，把所有等于 `mID` 的位置改回 `0`，同时统计改了多少个位置，最后返回这个计数。

> 这种做法“最笨”在于每次 `allocate` 都要 **从头扫描一次**，每次 `freeMemory` 都要 **遍历整条内存**。但是它的实现非常直观，适合刚学会数组的同学。

#### 代码（Python）

```python
class Allocator:
    def __init__(self, n: int):
        """
        初始化长度为 n 的内存数组，全部置为 0（表示空闲）。
        """
        self.mem = [0] * n          # mem[i] == 0 表示空闲，>0 表示被对应的 mID 占用

    def allocate(self, size: int, mID: int) -> int:
        """
        在最左侧找到连续 size 个空闲单元，标记为 mID 并返回起始下标；
        若不存在则返回 -1。
        """
        n = len(self.mem)
        i = 0
        while i <= n - size:            # 只需要遍历到 n - size，后面不可能放下 size 个单元
            # 检查从 i 开始的 size 个位置是否全部为空
            ok = True
            for j in range(i, i + size):
                if self.mem[j] != 0:    # 只要有一个已被占用，就不是连续空闲块
                    ok = False
                    break
            if ok:                       # 找到合适的块
                for j in range(i, i + size):
                    self.mem[j] = mID    # 用 mID 标记这段内存
                return i                # 返回左端下标
            i += 1                       # 否则左移一格继续尝试
        return -1                        # 没有足够大的空闲块

    def freeMemory(self, mID: int) -> int:
        """
        释放所有被 mID 占用的单元，返回实际释放的单元数。
        """
        freed = 0
        for i in range(len(self.mem)):
            if self.mem[i] == mID:       # 找到属于该 mID 的位置
                self.mem[i] = 0          # 置为 0 表示空闲
                freed += 1
        return freed
```

#### 复杂度

- **时间复杂度**  
  - `allocate`：最坏情况下要遍历整条内存并在每个位置检查 `size` 次 → **O(n·size)**。在本题约束 `size ≤ n ≤ 1000`，所以最坏是 O(n²)。  
    - **大白话**：想象你在一排 1000 把椅子里找连续 200 把空椅子，你可能要把每把椅子都检查一遍，还要在每个检查点再看后面 200 把椅子是否都空，算下来就是“平方级”的工作量。  
  - `freeMemory`：需要把整条内存扫一遍 → **O(n)**。  
- **空间复杂度**  
  - 只用了一个长度为 `n` 的数组 → **O(n)**，即和内存大小线性相关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次 `allocate` 都要 **从头线性扫描**，以及 `freeMemory` 每次都遍历整条内存。  
我们可以把“连续空闲块”抽象成 **区间**（左端点、右端点），把所有空闲区间维护在一个有序容器里（这里用 `list`，因为数据量很小）。  
同理，已经分配给某个 `mID` 的区间也要记录下来，这样 `freeMemory` 可以直接拿到这些区间，而不必再次遍历整个内存。

核心思路：

1. **维护空闲区间列表 `free_intervals`**  
   - 初始时只有一个区间 `[0, n-1]`（全部空闲）。  
   - 区间按左端点升序排列，方便“左侧第一个足够大的区间”可以直接找到。  

2. **维护已分配区间的映射 `alloc_map`**  
   - `alloc_map[mID]` → `[(l1, r1), (l2, r2), …]`，记录该 `mID` 占用了哪些区间。  

3. **allocate(size, mID)**  
   - 从 `free_intervals` 依次找第一个长度 ≥ `size` 的区间 `[l, r]`。  
   - 把左侧的 `size` 单元分配给 `mID`，即产生新占用区间 `[l, l+size-1]`。  
   - 更新 `free_intervals`：如果区间被完全用掉，则删除；否则把剩余的右侧部分 `[l+size, r]` 替换回去。  
   - 把新占用区间加入 `alloc_map[mID]`。  
   - 返回起始下标 `l`，若遍历完都找不到则返回 `-1`。  

4. **freeMemory(mID)**  
   - 直接取出 `alloc_map[mID]`（可能是空列表），遍历这些区间，把它们重新插回 `free_intervals`。  
   - 插回时要 **合并相邻或重叠的空闲区间**，防止碎片化。  
   - 统计并返回释放的单元总数（所有区间长度之和），并删除 `alloc_map[mID]` 的记录。  

> **类比**：  
> 把内存想象成一块连续的土地。空闲的土地用若干块“地块”来表示（每块都有左、右边界），已经卖出的土地（分配给某本书）也用地块记录。买地时，只要在左边找一块够大的空地即可；卖地时，直接把对应的地块收回并和相邻的空地拼在一起，形成更大的空地块。

#### 代码（Python）

```python
class Allocator:
    def __init__(self, n: int):
        """
        - free_intervals : 按左端点升序保存所有空闲区间 (l, r)
        - alloc_map      : mID -> 已分配区间列表 [(l, r), ...]
        初始时整个内存都是空的，只有一个区间 [0, n-1]。
        """
        self.free_intervals = [(0, n - 1)]
        self.alloc_map = {}          # {mID: [(l, r), ...]}

    # ---------- 辅助函数 ----------
    def _add_free_interval(self, new_l: int, new_r: int):
        """
        把新空闲区间 (new_l, new_r) 插入 free_intervals，并与相邻区间合并。
        这里采用线性遍历，因为区间数量最多也不会超过 1000。
        """
        merged = []
        placed = False
        for l, r in self.free_intervals:
            if r + 1 < new_l:                 # 当前区间在新区间左侧且不相邻
                merged.append((l, r))
            elif new_r + 1 < l:               # 当前区间在新区间右侧且不相邻
                if not placed:
                    merged.append((new_l, new_r))
                    placed = True
                merged.append((l, r))
            else:                             # 有重叠或相邻，需要合并
                new_l = min(new_l, l)
                new_r = max(new_r, r)
        if not placed:                        # 新区间在最右侧
            merged.append((new_l, new_r))
        self.free_intervals = merged          # 重新赋值为合并后的列表

    # ---------- 接口 ----------
    def allocate(self, size: int, mID: int) -> int:
        """
        在最左侧找到连续 size 个空闲单元，标记为 mID 并返回起始下标；
        若不存在则返回 -1。
        """
        for idx, (l, r) in enumerate(self.free_intervals):
            length = r - l + 1
            if length >= size:                # 找到第一个足够大的空闲区间
                start = l
                end = l + size - 1            # 分配的区间 [start, end]

                # 1) 更新空闲区间列表：把已用掉的左侧部分剔除
                if length == size:            # 区间正好被用完，直接删掉
                    self.free_intervals.pop(idx)
                else:                         # 只用掉左侧 size 单元，保留右侧剩余部分
                    self.free_intervals[idx] = (l + size, r)

                # 2) 记录分配信息
                self.alloc_map.setdefault(mID, []).append((start, end))

                return start                  # 返回左端下标
        return -1                             # 没有足够大的空闲块

    def freeMemory(self, mID: int) -> int:
        """
        释放所有属于 mID 的区间，返回实际释放的单元数。
        """
        if mID not in self.alloc_map:
            return 0                          # 该 mID 从未分配过

        freed = 0
        for l, r in self.alloc_map[mID]:
            self._add_free_interval(l, r)      # 把每个已占用区间重新放回空闲列表并合并
            freed += r - l + 1                 # 统计释放的单元数

        del self.alloc_map[mID]                # 删除该 mID 的记录
        return freed
```

#### 复杂度

- **时间复杂度**  
  - `allocate`：遍历空闲区间列表，最坏情况遍历所有区间 → **O(k)**，其中 `k` 为当前空闲区间的数量。  
    - **大白话**：相当于只检查“几块空地”，而不是每一块地砖。  
  - `freeMemory`：直接拿到该 `mID` 所占的所有区间（数量记为 `t`），每个区间调用一次合并操作，合并本身仍是遍历当前空闲区间列表 → **O(t + k)**。  
- **空间复杂度**  
  - 维护的 `free_intervals` 与 `alloc_map` 共计至多保存所有区间，区间数 ≤ `n`（每个单元最多形成一个区间） → **O(n)**。  
  - 与暴力解相比，额外使用了一个映射表来记录每个 `mID` 的区间，但整体仍是线性级别。

与暴力解相比，**不再需要每次遍历整条内存**，而是只在区间层面操作，实际运行速度会快很多，尤其当 `n` 较大、调用次数较多时优势更明显。

---

## 心得

- **核心技巧**：把连续的空闲单元抽象成 **区间（interval）**，用有序的区间列表管理空闲空间，用哈希表记录每个 `mID` 对应的已占用区间。  
- **适用场景**  
  1. “区间分配/回收”类问题，如 **“设计堆栈式内存分配器”**、**“区间调度”**（LC 735）  
  2. **“合并区间”**、**“区间查询”**（LC 986、LC 715）  
  3. **“预约系统”**、**“会议室安排”**等需要快速找到空闲连续段的场景。  
- **一句话总结解题钥匙**：把“连续的空位”视作一个可合并的 **区间**，用区间而不是单个格子来操作，既能快速定位左侧第一块足够大的空地，又能在释放时高效合并碎片。

---

## 反思

- **第一反应**：直接把内存当成数组，暴力遍历寻找连续空位。因为数组是最直观的抽象，容易写出可运行的代码。  
- **最容易踩的坑**  
  - **边界条件**：`allocate` 时要确保 `i <= n - size`，否则会越界。  
  - **区间合并**：在 `freeMemory` 中忘记把相邻的空闲区间合并，会导致空闲区间列表碎片化，后续 `allocate` 可能找不到本来可以使用的空间。  
  - **重复释放**：同一个 `mID` 可能已经被释放过，若不检查是否存在于 `alloc_map`，会错误地把空闲区间重复加入。  
- **下次遇到同类题**：第一步先思考“是否可以把连续的资源抽象成区间”。如果答案是肯定的，就先建立区间结构（列表/堆/平衡树），再在此基础上实现分配和回收。这样可以避免每次都遍历全部细粒度的元素。