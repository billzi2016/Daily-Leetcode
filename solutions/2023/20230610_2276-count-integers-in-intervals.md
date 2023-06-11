# #2276. **区间内整数计数** / Count Integers in Intervals

> 难度：困难 · 标签：Design、Segment Tree、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/count-integers-in-intervals/)

---

## 题目（英文原版）

**Description**

Given an empty set of intervals, implement a data structure that can:
Implement the CountIntervals class:
Note that an interval [left, right] denotes all the integers x where left <= x <= right.

**Examples**

**Example 1:**

```
Input
["CountIntervals", "add", "add", "count", "add", "count"]
[[], [2, 3], [7, 10], [], [5, 8], []]
Output
[null, null, null, 6, null, 8]

Explanation
CountIntervals countIntervals = new CountIntervals(); // initialize the object with an empty set of intervals. 
countIntervals.add(2, 3);  // add [2, 3] to the set of intervals.
countIntervals.add(7, 10); // add [7, 10] to the set of intervals.
countIntervals.count();    // return 6
                           // the integers 2 and 3 are present in the interval [2, 3].
                           // the integers 7, 8, 9, and 10 are present in the interval [7, 10].
countIntervals.add(5, 8);  // add [5, 8] to the set of intervals.
countIntervals.count();    // return 8
                           // the integers 2 and 3 are present in the interval [2, 3].
                           // the integers 5 and 6 are present in the interval [5, 8].
                           // the integers 7 and 8 are present in the intervals [5, 8] and [7, 10].
                           // the integers 9 and 10 are present in the interval [7, 10].
```

**Constraints**

- 1 <= left <= right <= 109
- At most 105 calls in total will be made to add and count.
- At least one call will be made to count.

---

## 题目（中文翻译）

给定一个空的区间集合，实现一个数据结构，使其能够支持以下操作：

- `add(left, right)`：将区间 `[left, right]`（包含左端点 `left` 与右端点 `right`）加入集合中。  
- `count()`：返回集合中所有区间所覆盖的 **不同整数** 的数量，即至少被一个区间包含的整数个数。

> 注意：区间 `[left, right]` 表示所有满足 `left ≤ x ≤ right` 的整数 `x`。

### 示例

**示例 1：**

```text
Input
["CountIntervals", "add", "add", "count", "add", "count"]
[[], [2, 3], [7, 10], [], [5, 8], []]

Output
[null, null, null, 6, null, 8]
```

**解释**

```java
CountIntervals countIntervals = new CountIntervals(); // 初始化，区间集合为空
countIntervals.add(2, 3);   // 添加区间 [2, 3]
countIntervals.add(7, 10); // 添加区间 [7, 10]
countIntervals.count();    // 当前覆盖的整数为 {2,3,7,8,9,10}，返回 6
countIntervals.add(5, 8);  // 添加区间 [5, 8]，与已有区间产生重叠，实际覆盖的整数为 {2,3,5,6,7,8,9,10}
countIntervals.count();    // 返回 8
```

### 约束条件

- `1 <= left <= right <= 10^9`
- `add` 与 `count` 方法的调用总次数不超过 `10^5`
- 至少会调用一次 `count` 方法

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次 `add(left, right)` **真的把所有整数** `left … right` 逐个记下来。  
我们可以用一个 **哈希集合**（在生活中可以把它想象成一本“字典”，键是整数，值是是否出现过）来保存出现过的整数：

1. `add(l, r)`：遍历 `l … r`，把每个数插入集合。  
2. `count()`：直接返回集合的大小 `len(set)`。

> **为什么这样是对的？**  
> 集合天然去重，只要把所有区间覆盖的整数都放进去，集合的大小就恰好等于“出现过的整数个数”。  

> **时间/空间复杂度**  
> - `add` 需要遍历区间的每个整数，最坏情况是区间长度为 `10^9`，显然不可接受。即 **O(length)**。  
> - `count` 只需要读取集合的大小，**O(1)**。  
> - 集合里要存 **所有出现过的整数**，最坏会占用 `O(total numbers)` 的内存，和题目要求的 `10^5` 次调用相比也会爆炸。  

用大白话解释：如果把 `O(n²)` 想象成“把 `n` 本书的每一页都读两遍”，这里的 `O(length)` 就是“把区间里每个数字都亲自数一遍”，区间太大时根本不可能在合理时间内完成。

#### 代码（Python）

```python
class CountIntervals:
    def __init__(self):
        # 用集合保存出现过的整数，类似“字典”里记录哪些词出现过
        self.seen = set()

    def add(self, left: int, right: int) -> None:
        # 把区间里的每个整数都放进集合
        for x in range(left, right + 1):
            self.seen.add(x)      # 把 x 记下来，重复的会自动去重

    def count(self) -> int:
        # 集合大小就是不同整数的个数
        return len(self.seen)
```

#### 复杂度

- **时间复杂度**：`add` 为 `O(right - left + 1)`，即遍历区间的长度。  
  `count` 为 `O(1)`。  
  当区间非常大时，这种做法会非常慢（相当于“数到一亿”）。
- **空间复杂度**：`O(total distinct numbers)`，最坏需要存所有出现过的整数，内存会很大。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **把每个具体的整数都记下来**，而我们只关心 **区间的总长度**。  
如果我们把所有已经加入的区间 **合并成互不重叠的“非重叠区间集合”**，只需要维护：

1. 这些非重叠区间的 **起点**、**终点**（用 `(l, r)` 表示）。  
2. 当前所有区间覆盖的整数总数 `total_len = Σ (r - l + 1)`。

这样：

- `count()` 只要返回 `total_len`，**O(1)**。  
- `add(l, r)` 只需要把新区间和已有的非重叠区间进行 **合并**，并相应地 **增减** `total_len`。

关键在于 **快速定位** 与 `l, r` 可能重叠的已有区间。这里可以使用 **有序容器**（如二叉搜索树）来维护区间的左端点有序。Python 标准库没有直接的平衡树，但我们可以用 **两个平行的列表** + `bisect`（二分查找）来实现“有序集合”。思路如下：

1. 用 `starts = []` 保存所有非重叠区间的左端点（升序），用 `intervals = []` 保存对应的 `(l, r)`。两者下标保持同步。  
2. 对于 `add(l, r)`：  
   - 用 `bisect_left(starts, l)` 找到第一个左端点 **不小于** `l` 的位置 `i`。  
   - 为了处理左侧可能已经覆盖的区间，需要检查 `i-1`（如果存在）看它的右端点是否 ≥ `l-1`。  
   - 从 `i-1` 开始向右遍历，合并所有与 `[l, r]` 有交集的区间。合并过程：  
     - 把它们的左端点取最小、右端点取最大，得到新的区间 `[new_l, new_r]`。  
     - 从 `total_len` 中 **减去** 被合并区间的长度（因为它们将被新区间取代）。  
     - 同时把这些旧区间从 `starts`、`intervals` 中删除。  
   - 最后把合并后的 `[new_l, new_r]` 插入到正确的位置，**把它的长度加到 `total_len`**。  

这样每次 `add` 只会遍历 **实际被合并的区间数**，而每个区间在整个生命周期里最多被合并一次（被删除后不再出现），所以总体上是 **摊销 O(log N)**（二分查找）加 **O(k)**（被合并的区间数），在最坏情况下 `k` 也是 `log N` 级别，满足题目 10⁵ 次调用的要求。

> **类比**：把已有的非重叠区间想象成“一排排不重叠的书”。我们想往书架里放新的一本书（新区间），先找出它可能碰到的相邻书（二分定位），然后把相邻的、可以合在一起的书合并成一本更大的书，最后把这本新书放回合适的位置。

#### 代码（Python）

```python
import bisect

class CountIntervals:
    def __init__(self):
        # starts[i] 保存第 i 个非重叠区间的左端点，保持升序
        self.starts = []          # List[int]
        # intervals[i] = (l, r) 对应 starts[i]
        self.intervals = []       # List[Tuple[int, int]]
        # 当前所有区间覆盖的整数个数
        self.total_len = 0

    def add(self, left: int, right: int) -> None:
        # 先把新区间的左右端点设为待合并的区间
        new_l, new_r = left, right

        # 1️⃣ 用二分定位：第一个左端点 >= left 的位置
        i = bisect.bisect_left(self.starts, left)

        # 2️⃣ 检查左侧的区间是否与 [left, right] 有交集
        #    需要看 i-1 区间的右端点是否 >= left-1（相邻也算连续）
        if i > 0 and self.intervals[i - 1][1] >= left - 1:
            i -= 1   # 把左侧的可能相交区间也算进来

        # 3️⃣ 从位置 i 开始向右遍历，合并所有与 new 区间相交的区间
        while i < len(self.intervals) and self.intervals[i][0] <= new_r + 1:
            cur_l, cur_r = self.intervals[i]
            # 从总长度中减掉被合并的旧区间的长度
            self.total_len -= (cur_r - cur_l + 1)

            # 更新合并后区间的左右端点
            new_l = min(new_l, cur_l)
            new_r = max(new_r, cur_r)

            # 删除旧区间（因为已经被新区间吞掉了）
            del self.starts[i]
            del self.intervals[i]
            # 注意：删除后 i 指向的仍是下一个未检查的区间，无需 i+=1

        # 4️⃣ 把合并好的新区间插回有序位置
        bisect.insort(self.starts, new_l)          # 把左端点插入保持有序
        # 找到插入后对应的下标（因为可能有相同的左端点）
        pos = bisect.bisect_left(self.starts, new_l)
        self.intervals.insert(pos, (new_l, new_r))

        # 5️⃣ 把新区间的长度加到 total_len
        self.total_len += (new_r - new_l + 1)

    def count(self) -> int:
        # 直接返回累计的长度即可，时间 O(1)
        return self.total_len
```

> **代码要点注释**  
> - `bisect_left` 相当于在有序的“字典”里查找插入位置，时间是 **对数级**。  
> - `while` 循环只会遍历真的“相交”或“相邻”的区间，合并后这些旧区间被删掉，后面再也不会出现。  
> - `total_len` 的增减确保 `count()` 只需要 **O(1)**。

#### 复杂度

- **时间复杂度**  
  - `add`：二分查找 `O(log m)`（`m` 为当前非重叠区间数），加上遍历并删除相交区间 `O(k)`（`k` 为被合并的区间数）。由于每个区间在被合并后就不再出现，整体上 `add` 的摊销复杂度是 **O(log N)**，其中 `N ≤ 10⁵` 为调用次数上限。  
  - `count`：**O(1)**，只读一个整数。  
  与暴力解相比，`add` 从 “遍历区间长度” 下降到 “对数级 + 被合并区间数”，大幅提升性能。

- **空间复杂度**  
  - 只保存 **非重叠区间**，最坏情况每个 `add` 都不相交，最多保存 `O(N)` 个区间。每个区间只占两个整数，空间约为 **O(N)**。  
  - `total_len` 只占一个整数。相比暴力解需要保存所有具体整数，空间降低了几个数量级。

---

## 心得

- **核心技巧**：维护**不重叠区间的有序集合**并在插入时**合并**，同时维护区间总长度。  
- **适用的题型**（类似思路）  
  1. **区间合并**（如 LeetCode 56 Merge Intervals）  
  2. **动态区间查询**（如 LeetCode 715 Range Module）  
  3. **统计被覆盖的整数个数**（本题）  
- **一句话总结**：把“每个整数是否出现”抽象成“区间的长度”，用有序结构合并区间，`count` 只需要读一个累计值。

---

## 反思

- **第一反应**：直接把所有整数记下来，用集合去重。虽然思路最直观，却忽视了数值范围极大（`10⁹`）的限制。  
- **最容易踩的坑**  
  - **区间相邻**：`[2,3]` 与 `[4,5]` 应视为可以合并成 `[2,5]`（因为整数是连续的），所以合并条件是 `cur_l <= new_r + 1`。  
  - **左侧检查**：二分定位后可能还有左侧区间与新区间相交，必须向左回退一次检查。  
  - **删除时的索引**：在循环中删除元素后不要忘记 `i` 仍指向下一个未检查的区间。  
  - **大数溢出**：在 Python 中整数不溢出，但如果用其他语言要注意 `long long`。  
- **下次遇到同类题**：第一步先思考 **“我只需要区间的总长度/总覆盖面积”，而不是每个点”。随后考虑 **有序容器 + 合并** 的方式实现。