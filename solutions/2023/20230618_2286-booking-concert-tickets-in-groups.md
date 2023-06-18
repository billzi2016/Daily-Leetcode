# #2286. 团体预订演唱会门票 / Booking Concert Tickets in Groups

> 难度：困难 · 标签：Binary Search、Design、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/booking-concert-tickets-in-groups/)

---

## 题目（英文原版）

**Description**

A concert hall has n rows numbered from 0 to n - 1, each with m seats, numbered from 0 to m - 1. You need to design a ticketing system that can allocate seats in the following cases:
Note that the spectators are very picky. Hence:
Implement the BookMyShow class:

**Examples**

**Example 1:**

```
Input
["BookMyShow", "gather", "gather", "scatter", "scatter"]
[[2, 5], [4, 0], [2, 0], [5, 1], [5, 1]]
Output
[null, [0, 0], [], true, false]

Explanation
BookMyShow bms = new BookMyShow(2, 5); // There are 2 rows with 5 seats each 
bms.gather(4, 0); // return [0, 0]
                  // The group books seats [0, 3] of row 0. 
bms.gather(2, 0); // return []
                  // There is only 1 seat left in row 0,
                  // so it is not possible to book 2 consecutive seats. 
bms.scatter(5, 1); // return True
                   // The group books seat 4 of row 0 and seats [0, 3] of row 1. 
bms.scatter(5, 1); // return False
                   // There is only one seat left in the hall.
```

**Constraints**

- 1 <= n <= 5 * 104
- 1 <= m, k <= 109
- 0 <= maxRow <= n - 1
- At most 5 * 104 calls in total will be made to gather and scatter.

---

## 题目（中文翻译）

**描述**  
演唱会厅有 `n` 行（rows），编号为 `0` 到 `n - 1`，每行有 `m` 个座位（seats），编号为 `0` 到 `m - 1`。需要设计一个票务系统，使得可以在以下两种情况下为观众分配座位，且观众对座位的要求非常挑剔：

* **gather(k, maxRow)**  
  - 在编号不超过 `maxRow` 的所有行中，寻找**同一行内连续的 `k` 个空座位**。  
  - 如果存在，则把这 `k` 个座位全部预订，返回一个长度为 `2` 的数组 `[row, seatIndex]`，其中 `row` 为预订的行号，`seatIndex` 为该行中最左侧被预订座位的编号。  
  - 如果不存在满足条件的连续座位，则返回空数组 `[]`。  

* **scatter(k, maxRow)**  
  - 在编号不超过 `maxRow` 的所有行中，**任意分配 `k` 个空座位**（不要求连续，也可以跨行）。  
  - 如果能够成功预订 `k` 张票，则返回 `true`，否则返回 `false`。  

实现 `BookMyShow` 类，使其能够高效处理上述两类请求。

**类定义**  

```java
class BookMyShow {
    public BookMyShow(int n, int m) { ... }   // 初始化 n 行、每行 m 个座位
    public int[] gather(int k, int maxRow) { ... }   // 见上描述
    public boolean scatter(int k, int maxRow) { ... } // 见上描述
}
```

**示例**  

```text
输入
["BookMyShow", "gather", "gather", "scatter", "scatter"]
[[2, 5], [4, 0], [2, 0], [5, 1], [5, 1]]

输出
[null, [0, 0], [], true, false]

解释
BookMyShow bms = new BookMyShow(2, 5); // 有 2 行，每行 5 个座位
bms.gather(4, 0); // 返回 [0, 0]，在第 0 行预订座位 [0, 3]
bms.gather(2, 0); // 返回 []，第 0 行剩余座位不足 2 个连续座位
bms.scatter(5, 1); // 返回 true，成功在第 0 行剩余的 1 个座位和第 1 行的前 4 个座位完成预订
bms.scatter(5, 1); // 返回 false，剩余可用座位不足 5 个
```

**约束条件**  

- `1 <= n <= 5 * 10^4`
- `1 <= m, k <= 10^9`
- `0 <= maxRow <= n - 1`
- 对 `gather` 与 `scatter` 的调用总次数不超过 `5 * 10^4`  

请实现满足上述约束的高效算法。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每个座位都记下来，用一个二维数组 `seats[n][m]` 表示是否已被占用。  
- **`gather(k, maxRow)`**：从第 `0` 行开始逐行扫描，找到第一行中连续 `k` 个空座位且行号 ≤ `maxRow`，把这些座位标记为已占用，返回起始位置 `(row, seat)`。如果遍历完都找不到，就返回空列表 `[]`。  
- **`scatter(k, maxRow)`**：同样从第 `0` 行开始逐行扫描，只要还有空位，就把它们一个一个占用，直到占满 `k` 个座位或所有行都已经超过 `maxRow`。如果成功占满 `k`，返回 `True`，否则返回 `False`。  

> **类比**：把每一排座位想象成一本字典的每一页，`seats[row][col] = 0/1` 就像字典里每个词是否已经划线标记。要找连续的 `k` 个空词，就得一页一页、一个字一个字往后看。

这种办法 **一定能得到正确答案**，因为我们把所有座位的状态都精确记录了，遍历时不遗漏任何可能的安排。

#### 代码（Python）  

```python
class BookMyShow:
    def __init__(self, n: int, m: int):
        # n 行，每行 m 坐席，0 表示空，1 表示已占
        self.n, self.m = n, m
        self.seats = [[0] * m for _ in range(n)]

    def gather(self, k: int, maxRow: int):
        """在 ≤ maxRow 的范围内寻找同一排的 k 个连续空座位"""
        for r in range(maxRow + 1):
            cnt = 0                     # 当前连续空座位计数
            for c in range(self.m):
                if self.seats[r][c] == 0:
                    cnt += 1
                    if cnt == k:       # 找到 k 个连续空位
                        start = c - k + 1
                        for i in range(start, start + k):
                            self.seats[r][i] = 1   # 标记已占
                        return [r, start]
                else:
                    cnt = 0             # 被占的座位把连续计数清零
        return []                     # 没有满足条件的安排

    def scatter(self, k: int, maxRow: int):
        """在 ≤ maxRow 的范围内任意座位占满 k 张票"""
        for r in range(maxRow + 1):
            for c in range(self.m):
                if self.seats[r][c] == 0:
                    self.seats[r][c] = 1
                    k -= 1
                    if k == 0:
                        return True
        return False                  # 座位不够
```

#### 复杂度  

- **时间复杂度**  
  - `gather`：最坏需要遍历所有行的所有座位 → **O(n·m)**。  
  - `scatter`：同理，需要遍历到第 `maxRow` 行的每个座位 → **O(n·m)**。  
  - 这里的 `O(n·m)` 只是一种“大概的说法”，相当于“如果把所有座位都检查一遍，花的时间就是这么多”。  
- **空间复杂度**  
  - 需要保存一个 `n × m` 的二维数组 → **O(n·m)**，相当于“每个座位都占用一个小格子”。  

显然，这种暴力做法在 `n、m` 都可能很大的情况下（题目里 `n ≤ 5·10⁴, m ≤ 10⁹`）会直接 **TLE / MLE**，所以我们必须改进。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，真正的“瓶颈”在于 **频繁地遍历每一排的每一个座位**。  
我们只需要知道每一排 **还有多少空座位**，以及 **该排最左边的空座位位置**，就可以在 **O(log n)** 或 **O(log n·log m)** 的时间内完成查询和更新。  

下面一步步推导出可行的优化方案：

1. **记录每排剩余座位数**  
   - 用一个长度为 `n` 的数组 `remain[row]` 表示第 `row` 行还有多少空座位。  
   - `scatter` 只需要判断从第 `0` 行到 `maxRow` 行的剩余座位总和是否 ≥ `k`，如果够，就可以直接“把座位往后填”。  

2. **记录每排最左侧空座位的列号**  
   - 用另一个长度为 `n` 的数组 `first[row]` 表示第 `row` 行最左边仍然空着的座位下标（从 `0` 开始）。  
   - `gather` 只需要在 `0 … maxRow` 之间找第一行满足 `first[row] + k ≤ m` 的行。  

3. **快速查询区间信息**  
   - 我们需要 **区间求和**（`scatter`）和 **区间最大值**（`gather`）两种操作。  
   - 这正好可以用 **线段树（Segment Tree）** 或 **树状数组（Binary Indexed Tree, BIT）** 来实现。  
   - BIT 天然支持前缀和（求区间和），但不直接支持区间最大值；而线段树可以在同一棵树里同时维护 **最大值** 和 **总和** 两个属性。  

4. **选用数据结构**  
   - 为了代码简洁且一次构造即可完成两种查询，我们使用 **线段树**。  
   - 每个节点保存两个信息：  
     - `total`：该区间内所有行的剩余座位总和（用于 `scatter`）。  
     - `max_first`：该区间内 `first[row]` 的最大值（用于 `gather`，因为我们要找“最左侧的空位最靠前的行”）。  

5. **操作细节**  
   - **初始化**：每行的剩余座位数是 `m`，最左空位是 `0`。构建线段树的时间是 `O(n)`。  
   - **gather(k, maxRow)**：  
     1. 在 `[0, maxRow]` 区间查询 `max_first`，如果 **最大值** > `m - k`，说明没有一行能容纳 `k` 个连续座位，直接返回 `[]`。  
     2. 否则在该区间**二分查找**（或递归下沉）找到最左侧满足 `first[row] + k ≤ m` 的行 `r`。  
     3. 记录起始列 `c = first[r]`，随后把 `first[r] += k`、`remain[r] -= k`，并在树上更新这两个值。  
   - **scatter(k, maxRow)**：  
     1. 查询 `[0, maxRow]` 区间的 `total`，如果小于 `k`，直接返回 `False`。  
     2. 否则从第 `0` 行开始，**逐行**把座位填满：  
        - 若当前行 `remain[row] ≤ k`，则整行用完，`k -= remain[row]`，`first[row] = m`（表示已满），`remain[row] = 0`。  
        - 否则只占用 `k` 个座位，`first[row] += k`、`remain[row] -= k`，`k = 0`。  
        - 每次修改后在树上更新对应行的 `total` 与 `max_first`。  
     3. 循环结束后返回 `True`。  
   - 由于每次 **只会在树上更新** O(log n) 次（每行最多一次），整体时间复杂度是 `O(log n)`（`gather`）或 `O(log n + rows_used·log n)`（`scatter`），而 `rows_used` 在最坏情况下是 `maxRow+1`，但每次调用的 `k` 只会遍历 **被真正占用的行**，总的调用次数不超过 `5·10⁴`，所以能够通过时间限制。  

> **类比**：线段树就像一本分层目录的“索引”。最底层是每一排的座位信息，上层把若干排的总和、最大空位“压缩”起来，查询时只需要看几层目录，而不必逐个翻页。

#### 代码（Python）  

```python
class SegmentTreeNode:
    """线段树的节点，维护区间 [l, r] 的两种信息"""
    __slots__ = ('l', 'r', 'left', 'right', 'total', 'max_first')
    def __init__(self, l: int, r: int):
        self.l, self.r = l, r          # 区间左右端点（闭区间）
        self.left = self.right = None  # 子节点
        self.total = 0                 # 该区间所有行的剩余座位数之和
        self.max_first = 0             # 该区间所有行的 first[row] 的最大值


class BookMyShow:
    def __init__(self, n: int, m: int):
        self.n, self.m = n, m
        # 初始时每行都有 m 个空座位，first = 0
        self.root = self._build(0, n - 1)

    # ---------- 建树 ----------
    def _build(self, l: int, r: int) -> SegmentTreeNode:
        node = SegmentTreeNode(l, r)
        if l == r:                     # 叶子节点对应一行
            node.total = self.m        # 该行剩余座位数
            node.max_first = 0        # 最左空位列号
            return node
        mid = (l + r) // 2
        node.left = self._build(l, mid)
        node.right = self._build(mid + 1, r)
        self._push_up(node)
        return node

    # ---------- 合并子节点信息 ----------
    def _push_up(self, node: SegmentTreeNode):
        node.total = node.left.total + node.right.total
        node.max_first = max(node.left.max_first, node.right.max_first)

    # ---------- 单点更新 ----------
    def _update(self, node: SegmentTreeNode, idx: int, new_total: int, new_first: int):
        """把第 idx 行的 total 与 first 更新为新值"""
        if node.l == node.r:           # 到达叶子
            node.total = new_total
            node.max_first = new_first
            return
        if idx <= node.left.r:
            self._update(node.left, idx, new_total, new_first)
        else:
            self._update(node.right, idx, new_total, new_first)
        self._push_up(node)

    # ---------- 区间查询：总剩余座位 ----------
    def _query_total(self, node: SegmentTreeNode, ql: int, qr: int) -> int:
        if ql <= node.l and node.r <= qr:
            return node.total
        ans = 0
        if ql <= node.left.r:
            ans += self._query_total(node.left, ql, qr)
        if qr >= node.right.l:
            ans += self._query_total(node.right, ql, qr)
        return ans

    # ---------- 区间查询：max_first ----------
    def _query_max_first(self, node: SegmentTreeNode, ql: int, qr: int) -> int:
        if ql <= node.l and node.r <= qr:
            return node.max_first
        res = -1
        if ql <= node.left.r:
            res = max(res, self._query_max_first(node.left, ql, qr))
        if qr >= node.right.l:
            res = max(res, self._query_max_first(node.right, ql, qr))
        return res

    # ---------- 在区间 [0, maxRow] 内找第一行能够容纳 k 连续座位 ----------
    def _find_row_for_gather(self, node: SegmentTreeNode, maxRow: int, k: int) -> int:
        """
        返回最左侧满足 first[row] + k <= m 的行号。
        前置条件：在 [0, maxRow] 区间内必定存在这样的一行。
        """
        if node.l > maxRow:          # 完全在查询范围之外
            return -1
        if node.l == node.r:         # 叶子，直接返回行号
            return node.l
        # 先检查左子树，因为我们要求最左的行
        if node.left.l <= maxRow:
            # 若左子树的 max_first 已经满足条件，则继续向左搜索
            if node.left.max_first + k <= self.m:
                return self._find_row_for_gather(node.left, maxRow, k)
        # 否则只能去右子树（注意仍然受 maxRow 限制）
        return self._find_row_for_gather(node.right, maxRow, k)

    # ---------- 公共接口 ----------
    def gather(self, k: int, maxRow: int):
        """
        在第 0~maxRow 行中寻找同一排连续 k 个空座位。
        成功返回 [row, startSeat]，否则返回 []。
        """
        # 1. 判断是否有行的 first + k <= m
        if self._query_max_first(self.root, 0, maxRow) + k > self.m:
            return []                     # 没有满足条件的行

        # 2. 找到最左的那一行
        row = self._find_row_for_gather(self.root, maxRow, k)

        # 3. 读取该行当前的 first 与 total（这里直接用查询得到的值）
        # 为了简化实现，我们在更新时把最新的值存下来
        # 这里重新查询一次获取最新的 total/first（实际可在更新时维护）
        cur_first = self._query_max_first(self.root, row, row)   # 其实是该行的 first
        cur_total = self._query_total(self.root, row, row)       # 该行剩余座位数

        start = cur_first
        # 4. 更新该行信息
        new_first = cur_first + k
        new_total = cur_total - k
        self._update(self.root, row, new_total, new_first)
        return [row, start]

    def scatter(self, k: int, maxRow: int) -> bool:
        """
        在第 0~maxRow 行中任意座位占满 k 张票。
        成功返回 True，座位不足返回 False。
        """
        # 1. 检查区间总剩余座位是否足够
        if self._query_total(self.root, 0, maxRow) < k:
            return False

        # 2. 按行依次占位，直到 k 为 0
        row = 0
        while k > 0:
            # 只关注在 maxRow 范围内的行
            if row > maxRow:
                break
            # 查询当前行的剩余座位数
            cur_total = self._query_total(self.root, row, row)
            if cur_total == 0:          # 已满，直接跳到下一行
                row += 1
                continue
            # 本行可以使用的座位数
            use = min(k, cur_total)

            # 读取该行的 first（最左空位列号）
            cur_first = self._query_max_first(self.root, row, row)

            # 更新该行状态
            new_first = cur_first + use
            new_total = cur_total - use
            self._update(self.root, row, new_total, new_first)

            k -= use
            if new_total == 0:          # 本行已满，继续下一行
                row += 1
        return True
```

> **代码说明**  
> - `SegmentTreeNode` 用 `__slots__` 节约内存，避免每个节点都有 `__dict__`。  
> - `max_first` 存的是 **该行最左空位的列号**，而不是最大空位数，查询时取最大值即可快速判断是否存在能容纳 `k` 连续座位的行。  
> - `gather` 里先检查 `max_first + k > m`，如果不满足则直接返回 `[]`，避免不必要的递归。  
> - `scatter` 采用 “按行消耗” 的方式，最多遍历 `maxRow+1` 行，但每次遍历只做 **O(log n)** 的查询/更新，总体仍在可接受范围。  

#### 复杂度  

- **时间复杂度**  
  - `gather`：查询 `max_first` 为 `O(log n)`，随后在树上二分寻找满足条件的行也为 `O(log n)`，最后一次点更新 `O(log n)`。整体 **O(log n)**。  
    - **含义**：即使有 5·10⁴ 行，最多只需要“看几层目录”，而不必逐行检查。  
  - `scatter`：首先一次区间求和 `O(log n)`，随后最多遍历被占用的行数（每行一次更新），每次更新 `O(log n)`。最坏情况下遍历 `maxRow+1` 行，但总的调用次数受题目限制，实际运行仍在 **O(log n · rows_used)**，可以视为 **接近 O(log n)**。  
- **空间复杂度**  
  - 线段树使用约 `4·n` 个节点，每个节点只保存两个整数 → **O(n)**。  
  - 额外的递归栈深度最多 `log₂ n`，可以忽略不计。  

与暴力解相比，时间从 **遍历所有座位 O(n·m)** 降到了 **只看几层树 O(log n)**，空间也从 `n·m`（根本不可行）降到 `O(n)`，完美满足题目大数据范围。

---  

## 心得  

- **核心技巧**：利用线段树（或同类的区间数据结构）同时维护**区间最大值**和**区间和**，从而在 `O(log n)` 时间内完成“能否一次性安排”以及“实际安排后状态更新”。  
- **适用题型**  
  1. **区间预约 / 资源分配**（例如酒店预订、停车位管理）  
  2. **区间查询与修改**（如区间最大子段和、区间最小值查询）  
  3. **动态库存管理**（如电商库存的快速扣减）  
- **一句话总结**：把每一排的“剩余座位数”和“最左空位位置”装进线段树，用树的层级“索引”代替逐行遍历，才能在海量座位中瞬间定位。

---  

## 反思  

- **第一反应**：看到 “最左行、最左座位” 的要求，我第一时间想到 **逐行扫描**，因为这样最容易满足“最小行号、最小座位号”。  
- **最容易踩的坑**  
  1. **溢出**：`m` 和 `k` 可达 `10⁹`，直接相加可能超过 32 位整数，需要使用 Python 的大整数或在 C++ 中使用 `long long`。  
  2. **边界条件**：`maxRow` 可能等于 `n‑1`，查询区间时一定要闭区间且防止越界。  
  3. **更新同步**：`total` 与 `max_first` 必须在同一次点更新中保持一致，否则后续查询会出现不匹配的错误。  
  4. **散布（scatter）时的行跳过**：如果某行已经满了，一定要立刻跳到下一行，否则会陷入死循环。  
- **下次思路**：遇到“在序号最小的对象上完成连续/任意分配”时，第一步就考虑 **维护每个对象的剩余容量**，并用 **支持区间最大/和的结构**（线段树或 BIT）来快速定位和判断，而不是直接遍历。这样可以把时间从线性提升到对数级。