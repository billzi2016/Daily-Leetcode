# #1146. 快照数组 / Snapshot Array

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Design · [LeetCode 链接](https://leetcode.com/problems/snapshot-array/)

---

## 题目（英文原版）

**Description**

Implement a SnapshotArray that supports the following interface:

**Examples**

**Example 1:**

```
Input: ["SnapshotArray","set","snap","set","get"]
[[3],[0,5],[],[0,6],[0,0]]
Output: [null,null,0,null,5]
Explanation: 
SnapshotArray snapshotArr = new SnapshotArray(3); // set the length to be 3
snapshotArr.set(0,5);  // Set array[0] = 5
snapshotArr.snap();  // Take a snapshot, return snap_id = 0
snapshotArr.set(0,6);
snapshotArr.get(0,0);  // Get the value of array[0] with snap_id = 0, return 5
```

**Constraints**

- 1 <= length <= 5 * 104
- 0 <= index < length
- 0 <= val <= 109
- 0 <= snap_id < (the total number of times we call snap())
- At most 5 * 104 calls will be made to set, snap, and get.

---

## 题目（中文翻译）

实现一个 `SnapshotArray`，它支持以下接口：

- `SnapshotArray(length)`：初始化一个长度为 `length` 的数组，所有元素初始值为 `0`。
- `set(index, val)`：将下标为 `index` 的元素设置为 `val`。
- `snap()`：对当前数组拍摄一次快照，并返回该快照的编号 `snap_id`（从 `0` 开始递增）。
- `get(index, snap_id)`：返回在第 `snap_id` 次快照时，数组下标 `index` 的值。

---

**示例 1：**

```text
Input: ["SnapshotArray","set","snap","set","get"]
[[3],[0,5],[],[0,6],[0,0]]
Output: [null,null,0,null,5]
Explanation: 
SnapshotArray snapshotArr = new SnapshotArray(3); // 将数组长度设为 3
snapshotArr.set(0,5);  // 设置 array[0] = 5
snapshotArr.snap();    // 拍摄一次快照，返回 snap_id = 0
snapshotArr.set(0,6);  // 将 array[0] 更新为 6
snapshotArr.get(0,0);  // 获取快照 snap_id = 0 时 array[0] 的值，返回 5
```

---

**约束条件**

- `1 <= length <= 5 * 10^4`
- `0 <= index < length`
- `0 <= val <= 10^9`
- `0 <= snap_id < (snap() 调用的总次数)`
- 最多会有 `5 * 10^4` 次 `set`、`snap` 与 `get` 调用。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次 `snap()` 时的完整数组都保存下来。  
可以想象：

- **数组** 就像一本笔记本，里面记录了每个位置的当前值。  
- **快照** 就像把这本笔记本复印一份，保存为“第 k 次复印”。  
- 当调用 `get(index, snap_id)` 时，只要去第 `snap_id` 份复印本里找第 `index` 行的内容即可。

实现方式：

1. 用一个普通的 Python 列表 `cur` 保存当前数组（长度 `length`，初始全为 `0`）。  
2. 用另一个列表 `snapshots` 保存所有快照。每一次 `snap()`，把 `cur` **整体拷贝**（`cur[:]`）并追加到 `snapshots` 中，返回当前快照的编号 `snap_id`（等于 `snapshots` 的下标）。  
3. `set(index, val)` 直接修改 `cur[index] = val`。  
4. `get(index, snap_id)` 直接返回 `snapshots[snap_id][index]`。

> **为什么正确？**  
> 每一次 `snap()` 都把当时完整的数组状态完整保存下来，后面无论怎么修改 `cur`，已经保存的快照内容都不受影响。因此查询任何历史快照的任意位置，都能得到那一刻的真实值。

#### 代码（Python）

```python
class SnapshotArray:
    def __init__(self, length: int):
        # 当前正在编辑的数组，初始全为 0
        self.cur = [0] * length
        # 用来保存每一次快照的完整数组
        self.snapshots = []          # snapshots[i] 是第 i 次 snap 的数组拷贝
        # 第一次 snap 的 id 从 0 开始计数
        self.snap_cnt = 0

    def set(self, index: int, val: int) -> None:
        # 直接改动当前数组对应位置的值
        self.cur[index] = val

    def snap(self) -> int:
        # 把当前数组完整复制一份保存起来
        self.snapshots.append(self.cur[:])   # [:] 是浅拷贝，得到一个新列表
        snap_id = self.snap_cnt
        self.snap_cnt += 1
        return snap_id

    def get(self, index: int, snap_id: int) -> int:
        # 直接在对应的快照里取值
        return self.snapshots[snap_id][index]
```

#### 复杂度  

- **时间复杂度**  
  - `set`：`O(1)`（直接改动数组）。  
  - `snap`：`O(n)`，因为要把长度为 `n`（即 `length`）的数组整体拷贝一遍。这里的 `O(n)` 可以理解为“和数组长度成正比”。如果数组有 10 000 项，拷贝一次大约要执行 10 000 次复制操作。  
  - `get`：`O(1)`（直接定位到快照列表再取值）。  

- **空间复杂度**  
  - 每一次 `snap` 都保存了一份完整数组，所以最坏情况下会占用 `O(k·n)` 的空间（`k` 为快照次数，`n` 为数组长度）。如果你拍了 5 000 张快照，而每张快照有 10 000 项，那么总共会占用约 5 000 × 10 000 = 50 000 000 个整数的内存，显然会超出题目限制。

> **结论**：虽然思路简单易懂，但在大量快照或较大数组时会导致时间和空间都爆炸，不能通过所有测试。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每一次 `snap` 都要复制整张表。  
其实我们并不需要保存每一次完整的数组，只要记录**每个位置的值在什么时候被改动**即可。  

**核心想法**：对每个下标 `i`，维护一个有序的「快照‑值」列表 `history[i]`，其中每一项是 `(snap_id, val)`，表示「在快照 `snap_id` 时，这个位置的值是 `val`」。

实现细节（一步步推导）：

1. **初始化**  
   - 对每个下标 `i`，先放入 `( -1, 0 )`，表示在任何快照之前默认值是 `0`。  
   - 用 `defaultdict(list)` 或普通 `list` 的列表来保存这些历史记录。  

2. **set(index, val)**  
   - 只记录当前正在进行的快照编号 `cur_snap_id`（即将要产生的下一个 `snap` 的 id），因为这次修改在后面的所有快照中都生效，除非再次被覆盖。  
   - 检查 `history[index]` 的最后一项的 `snap_id` 是否等于 `cur_snap_id`：  
     - 如果相等，说明已经在同一个快照里改过多次，只需要把最后一项的值更新为最新的 `val`（覆盖即可）。  
     - 否则，直接在列表末尾追加 `(cur_snap_id, val)`。  

3. **snap()**  
   - 只需要返回当前的 `snap_id`（从 `0` 开始递增），并把全局计数器 `cur_snap_id` 加 `1`。不需要复制任何数据。  

4. **get(index, snap_id)**  
   - 现在我们要在 `history[index]` 中找到 **最近的**（即 `snap_id` ≤ 给定 `snap_id`）记录。  
   - 因为每个列表是按 `snap_id` **递增**的，典型的做法是 **二分查找**（`bisect_right`），时间是 `O(log m)`，其中 `m` 是该下标的修改次数。  
   - Python 中可以写成：  
     ```python
     import bisect
     pos = bisect.bisect_right(hist, (snap_id, float('inf'))) - 1
     return hist[pos][1]
     ```  
   - 这里 `float('inf')` 只是一种技巧，保证即使有相同的 `snap_id`，也能取到最右侧的那一项。  

> **为什么正确？**  
> - 每一次 `set` 都把「在当前快照号之前的最新值」记录下来。  
> - 对任意 `snap_id`，我们在对应下标的历史列表中查找最近的、`snap_id` 不超过目标的记录，这正是「在该快照时该位置的值」的定义。  
> - 二分查找能够在有序列表中快速定位，保证查询时间对每个下标都是对数级别。

#### 代码（Python）

```python
import bisect
from collections import defaultdict

class SnapshotArray:
    def __init__(self, length: int):
        # 每个下标对应的历史记录列表，初始放入 ( -1, 0 )
        self.hist = defaultdict(list)          # key: index, value: list of (snap_id, val)
        for i in range(length):
            self.hist[i].append((-1, 0))        # 默认值 0，快照号 -1 表示“在任何快照之前”

        self.cur_snap_id = 0    # 下一次 snap() 要返回的 id，也是当前正在写入的 snap_id

    def set(self, index: int, val: int) -> None:
        # 取该下标最近一次的记录
        lst = self.hist[index]
        # 如果最近一次的记录已经是当前 snap_id，则覆盖值
        if lst[-1][0] == self.cur_snap_id:
            lst[-1] = (self.cur_snap_id, val)   # 直接替换
        else:
            # 否则追加一条新记录
            lst.append((self.cur_snap_id, val))

    def snap(self) -> int:
        # 当前 snap_id 作为本次快照的编号返回，然后自增
        snap_id = self.cur_snap_id
        self.cur_snap_id += 1
        return snap_id

    def get(self, index: int, snap_id: int) -> int:
        lst = self.hist[index]
        # 二分查找：找出第一个 snap_id > target 的位置，再往左一步就是 ≤ target 的最大项
        # (snap_id, INF) 保证即使有完全相同的 snap_id，也能取到最右侧那条记录
        pos = bisect.bisect_right(lst, (snap_id, float('inf'))) - 1
        return lst[pos][1]
```

#### 复杂度  

- **时间复杂度**  
  - `set`：`O(1)`（只在列表尾部检查或追加）。  
  - `snap`：`O(1)`（仅返回并递增计数器）。  
  - `get`：`O(log k)`，其中 `k` 是该下标被 `set` 的次数。二分查找的意义可以理解为“把需要检查的次数从线性逐个比对，压缩到只需要对数级的比较”。如果某个位置最多被改动 1 000 次，`log₂1000 ≈ 10`，即最多只要十次比较就能得到答案。  

- **空间复杂度**  
  - 每一次 `set` 至多在对应下标的历史列表里多存一条记录，因此总空间是 `O(total_set_calls)`，即所有 `set` 操作的数量上限（ ≤ 5 × 10⁴），远小于暴力解的 `O(k·n)`。  

> 与暴力解相比，最优解把每次快照的**复制成本**彻底消除，只在真正修改时记录信息，查询时通过二分查找快速定位，时间和空间都在题目限制内。

---

## 心得

- **核心技巧**：对每个元素维护“快照‑值”有序历史（类似“版本化数组”），查询时二分查找最近的版本。  
- **适用场景**  
  1. **SnapshotArray / SnapshotArray 变体**（如 `SnapshotArray`、`SnapshotArrayWithDelete`）。  
  2. **持久化数据结构**（如持久化并查集、持久化线段树）。  
  3. **时间旅行查询**（如「查询某时间点的数组/字符串」）。  
- **一句话总结**：把每次改动记成「在第几次快照时改成了多少」，查询时只要在该位置的改动记录里二分找最近的快照即可。

---

## 反思

- **第一反应**：直接把每次 `snap` 的完整数组保存下来，思路最直观。  
- **最容易踩的坑**  
  - **空间爆炸**：大量快照会导致 `O(k·n)` 的内存，超出限制。  
  - **二分边界**：在 `get` 时如果没有正确处理 “找不到小于等于 snap_id 的记录”，会出现索引错误，需要在列表首部放置 `(-1, 0)` 作为哨兵。  
  - **同一次快照内多次 `set`**：必须覆盖而不是追加，否则会在二分时返回错误的旧值。  
- **下次遇到同类题**：第一步先思考 **“只记录变化点，而不是完整状态”**，然后决定用 **有序列表 + 二分**（或哈希 + 前缀/后缀）来实现快速查询。