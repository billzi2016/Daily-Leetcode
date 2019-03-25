# #352. 数据流的非重叠区间 / Data Stream as Disjoint Intervals

> 难度：困难 · 标签：Binary Search、Design、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/data-stream-as-disjoint-intervals/)

---

## 题目（英文原版）

**Description**

Given a data stream input of non-negative integers a1, a2, ..., an, summarize the numbers seen so far as a list of disjoint intervals.
Implement the SummaryRanges class:
Follow up: What if there are lots of merges and the number of disjoint intervals is small compared to the size of the data stream?

**Examples**

**Example 1:**

```
Input
["SummaryRanges", "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals"]
[[], [1], [], [3], [], [7], [], [2], [], [6], []]
Output
[null, null, [[1, 1]], null, [[1, 1], [3, 3]], null, [[1, 1], [3, 3], [7, 7]], null, [[1, 3], [7, 7]], null, [[1, 3], [6, 7]]]

Explanation
SummaryRanges summaryRanges = new SummaryRanges();
summaryRanges.addNum(1);      // arr = [1]
summaryRanges.getIntervals(); // return [[1, 1]]
summaryRanges.addNum(3);      // arr = [1, 3]
summaryRanges.getIntervals(); // return [[1, 1], [3, 3]]
summaryRanges.addNum(7);      // arr = [1, 3, 7]
summaryRanges.getIntervals(); // return [[1, 1], [3, 3], [7, 7]]
summaryRanges.addNum(2);      // arr = [1, 2, 3, 7]
summaryRanges.getIntervals(); // return [[1, 3], [7, 7]]
summaryRanges.addNum(6);      // arr = [1, 2, 3, 6, 7]
summaryRanges.getIntervals(); // return [[1, 3], [6, 7]]
```

**Constraints**

- 0 <= value <= 104
- At most 3 * 104 calls will be made to addNum and getIntervals.
- At most 102 calls will be made to getIntervals.

---

## 题目（中文翻译）

给定一个**非负整数**（non‑negative integer）数据流 `a₁, a₂, ..., aₙ`，需要实时地将已出现的数字汇总为一组**不相交区间**（disjoint intervals）并返回。

实现 `SummaryRanges` 类，使其支持以下操作：

- `SummaryRanges()`：构造函数，初始化数据结构。
- `void addNum(int value)`：向数据流中加入一个新数字 `value`（`0 <= value <= 10⁴`）。
- `int[][] getIntervals()`：返回当前所有不相交区间的列表，区间内部按升序排列，列表本身也按区间左端点升序排列。

**示例 1**

```text
Input
["SummaryRanges", "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals"]
[[], [1], [], [3], [], [7], [], [2], [], [6], []]

Output
[null, null, [[1, 1]], null, [[1, 1], [3, 3]], null, [[1, 1], [3, 3], [7, 7]], null, [[1, 3], [7, 7]], null, [[1, 3], [6, 7]]]
```

**解释**

```java
SummaryRanges summaryRanges = new SummaryRanges();
summaryRanges.addNum(1);      // arr = [1]
summaryRanges.getIntervals(); // 返回 [[1, 1]]
summaryRanges.addNum(3);      // arr = [1, 3]
summaryRanges.getIntervals(); // 返回 [[1, 1], [3, 3]]
summaryRanges.addNum(7);      // arr = [1, 3, 7]
summaryRanges.getIntervals(); // 返回 [[1, 1], [3, 3], [7, 7]]
summaryRanges.addNum(2);      // arr = [1, 2, 3, 7]
summaryRanges.getIntervals(); // 返回 [[1, 3], [7, 7]]
summaryRanges.addNum(6);      // arr = [1, 2, 3, 6, 7]
summaryRanges.getIntervals(); // 返回 [[1, 3], [6, 7]]
```

**约束条件**

- `0 <= value <= 10⁴`
- `addNum` 与 `getIntervals` 的调用总次数不超过 `3 * 10⁴`
- `getIntervals` 的调用次数不超过 `10²`

**进阶**

如果合并操作非常频繁，而不相交区间的数量相对于数据流的规模来说很小，如何优化实现？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有出现过的数字全部记下来**，在需要返回区间时再一次性把它们整理成不相交的区间。

- **保存数据的结构**：用一个 `set`（集合）存所有出现过的整数。集合就像一本“数字字典”，只管记下出现过的词（数字），不管顺序。  
- **合并区间**：`getIntervals` 时，把集合里的数字取出来排序（相当于把字典的词条排好序），然后从左到右扫描，一旦发现相邻的数字（比如 2、3、4）就把它们合并成 `[2,4]`，否则就单独形成 `[x,x]`。

这样做一定能得到正确答案，因为我们没有遗漏任何数字，也没有把本不相邻的数字放进同一个区间。

**时间/空间复杂度**  
- `addNum`：往集合里加一个元素，时间是 **O(1)**（常数时间），因为集合的插入是哈希表实现的，和“往字典里查找词条并写下页码”差不多，几乎不花时间。  
- `getIntervals`：先把集合里的 `n` 个数字排个序，需要 **O(n log n)**，相当于把一堆乱七八糟的纸片（数字）先按大小排好队。随后一次线性扫描合并区间是 **O(n)**，但排序是瓶颈。整体 **O(n log n)**。  
- 空间：我们要把所有出现过的数字都保存下来，最多 `n` 个，故 **O(n)** 的额外空间。

> 大白话：`O(n log n)` 就是“先把 n 件东西排好顺序，再做一次遍历”。`log n` 大约是把东西二分查找需要的次数，比如把 1 万本书找一本，最多只需要查 14 次（因为 2^14≈16384）。

#### 代码（Python）

```python
class SummaryRanges:
    def __init__(self):
        # 用集合保存所有出现过的整数，像一本“数字字典”
        self.nums = set()

    def addNum(self, value: int) -> None:
        # 往集合里加一个数字，时间复杂度 O(1)
        self.nums.add(value)

    def getIntervals(self) -> list[list[int]]:
        # 1️⃣ 把集合里的数字排好序，时间 O(n log n)
        sorted_vals = sorted(self.nums)

        intervals = []                     # 用来存放结果区间
        i = 0
        n = len(sorted_vals)

        # 2️⃣ 一次线性扫描，合并连续的数字，时间 O(n)
        while i < n:
            start = sorted_vals[i]         # 区间左端点
            end = start                    # 区间右端点先和左端点相同

            # 向右扩展，只要下一个数字恰好是当前右端点 + 1，就属于同一个区间
            while i + 1 < n and sorted_vals[i + 1] == end + 1:
                i += 1
                end = sorted_vals[i]

            intervals.append([start, end])
            i += 1

        return intervals
```

#### 复杂度

- **时间复杂度**：`addNum` 为 **O(1)**，`getIntervals` 为 **O(n log n)**。其中 `n` 是已出现的数字个数。排序的 `log n` 表示“把 n 件东西二分查找需要的次数”，实际运行时大约是 14~20 次（当 n≈10⁴ 时）。
- **空间复杂度**：**O(n)**，因为我们把所有出现的数字都保存在集合里。

---

### 2. 最优解

#### 思路  

暴力解的慢点在 **`getIntervals` 每次都要重新排序**。如果我们能在插入新数字时就把区间保持好，那么 `getIntervals` 只需要把已有的区间直接返回即可，时间会降到 **O(m)**，其中 `m` 是当前区间的个数（通常远小于数字个数）。

**关键想法**：维护一个**有序的区间列表**，每次 `addNum` 时在这条有序链上找出**可能受影响的相邻区间**，再根据新数字与它们的关系决定合并、扩展或直接插入一个新区间。

实现步骤：

1. **数据结构**：用 `list` 保存所有区间 `[l, r]`，并且始终保持 `l`（左端点）递增。列表就像一排排整齐的抽屉，抽屉编号（左端点）从小到大。
2. **二分查找定位**：因为区间左端点有序，我们可以用 Python 标准库 `bisect`（二分查找）在 **O(log m)** 时间找到第一个左端点大于 `value` 的位置 `idx`。这一步相当于在排好序的抽屉里快速定位应该放哪一抽屉。
3. **检查左侧区间**：`idx-1`（如果存在）是新数字左边最近的区间，记作 `left = intervals[idx-1]`。如果 `value` 落在 `left` 区间内部（`left[0] ≤ value ≤ left[1]`），说明数字已经被覆盖，直接返回；如果恰好是 `left[1] + 1`，则可以把 `left` 区间右端点向右扩展到 `value`。
4. **检查右侧区间**：`idx`（如果存在）是新数字右边最近的区间，记作 `right = intervals[idx]`。如果 `value` 恰好是 `right[0] - 1`，则可以把 `right` 区间左端点向左收缩到 `value`。
5. **合并左右**：如果第 3 步和第 4 步都触发（即新数字正好桥接了左、右两个区间），则把 `left` 和 `right` 合并成一个更大的区间 `[left[0], right[1]]`，并删除 `right`。
6. **全新区间**：如果既没有左侧也没有右侧可以合并，新数字本身就是一个孤立区间 `[value, value]`，直接在 `idx` 位置插入。

这样，每次 `addNum` 只需要 **一次二分查找 + 常数次区间合并**，即 **O(log m)**。而 `getIntervals` 只需要返回已经维护好的列表，时间 **O(m)**（直接返回引用或拷贝）。

#### 代码（Python）

```python
import bisect

class SummaryRanges:
    def __init__(self):
        # 有序区间列表，始终保持左端点递增
        self.intervals = []   # 每个元素形如 [l, r]

    def addNum(self, value: int) -> None:
        # 1️⃣ 用二分查找定位第一个左端点大于 value 的区间索引
        # bisect_left 会返回 intervals 中第一个 interval[0] >= value 的位置
        idx = bisect.bisect_left(self.intervals, [value, value])

        # ---------- 处理左侧区间 ----------
        left_merge = False   # 是否需要把 value 合并到左侧区间
        if idx > 0:
            left = self.intervals[idx - 1]
            if left[0] <= value <= left[1]:
                # value 已经在左侧区间内部，无需任何操作
                return
            if left[1] + 1 == value:
                left_merge = True   # 可以把左区间右端点扩展到 value

        # ---------- 处理右侧区间 ----------
        right_merge = False
        if idx < len(self.intervals):
            right = self.intervals[idx]
            if right[0] - 1 == value:
                right_merge = True  # 可以把右区间左端点收缩到 value

        # ---------- 根据合并情况更新区间 ----------
        if left_merge and right_merge:
            # 同时桥接左右两段，需要把两段合并成一个更大的区间
            self.intervals[idx - 1][1] = self.intervals[idx][1]   # 扩展左区间右端点
            del self.intervals[idx]                               # 删除右区间
        elif left_merge:
            # 只合并左侧，右端点直接延伸到 value
            self.intervals[idx - 1][1] = value
        elif right_merge:
            # 只合并右侧，左端点直接收缩到 value
            self.intervals[idx][0] = value
        else:
            # 左右都不能合并，新建一个孤立区间插入到正确的位置
            self.intervals.insert(idx, [value, value])

    def getIntervals(self) -> list[list[int]]:
        # 直接返回已有的有序区间列表，时间 O(m)
        # 为防止外部修改，这里返回浅拷贝
        return [interval[:] for interval in self.intervals]
```

#### 复杂度

- **时间复杂度**  
  - `addNum`：二分查找 `O(log m)`，随后最多做几次列表插入/删除，均为 `O(m)` 最坏情况（当要在列表头部插入时，需要移动后面的元素），但因为 **`m`（区间数）通常远小于总数字数**，整体可以视作 **接近 O(log m)**。在 Python 中 `list.insert`/`del` 的实际开销与 `m` 成线性关系，但在题目限制下（`m ≤ 10⁴`）仍然很快。  
  - `getIntervals`：直接返回已有区间，遍历一次即得到结果，时间 **O(m)**。  
  与暴力解相比，`getIntervals` 从 **O(n log n)** 降到了 **O(m)**，`addNum` 仍保持对数级别的效率。

- **空间复杂度**：只保存不相交的区间，最多 `m` 个，每个区间占用常数空间，故 **O(m)**。因为 `m ≤ n`，在最坏情况下仍是 **O(n)**，但实际往往远小于 `n`，尤其是“合并很多、区间很少”的跟进情形。

---

## 心得

- **核心技巧**：**有序维护 + 二分查找**。把“区间左端点递增”视作排好序的抽屉，利用二分快速定位，再局部合并/插入。
- **适用的题型**  
  1. 动态维护不相交区间（如「合并区间」的在线版）。  
  2. 动态维护有序集合并快速查询前驱/后继（如「数据流中的中位数」的平衡树实现）。  
  3. 需要在有序结构上做局部修改的场景（如「搜索旋转数组」的二分定位）。
- **一句话总结解题钥匙**：**把全局排序的成本前置到每次插入时，用二分定位局部更新**。

---

## 反思

- **第一反应**：把所有数字存下来，等到查询时再一次性排序合并——最直观但不够高效。
- **最容易踩的坑**  
  - 忽略 **重复数字**：如果已经在某区间内部再次插入，需要直接返回，不做任何合并。  
  - 边界条件：插入的数字恰好是最左/最右区间的前后邻居，需要正确处理 `idx == 0` 或 `idx == len(intervals)` 的情况。  
  - `getIntervals` 返回引用会导致外部修改内部结构，最好返回拷贝或只读视图。
- **下次遇到同类题**：第一步想到 **“是否可以在插入时保持结构有序？”**，进而使用 **二分查找 + 局部合并** 的思路。这样可以把查询成本从 **O(n log n)** 降到 **O(m)**，大幅提升性能。