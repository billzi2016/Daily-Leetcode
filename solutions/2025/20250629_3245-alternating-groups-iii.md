# #3245. 交替组 III / Alternating Groups III

> 难度：困难 · 标签：Array、Binary Indexed Tree · [LeetCode 链接](https://leetcode.com/problems/alternating-groups-iii/)

---

## 题目（英文原版）

**Description**

There are some red and blue tiles arranged circularly. You are given an array of integers colors and a 2D integers array queries.
The color of tile i is represented by colors[i]:
An alternating group is a contiguous subset of tiles in the circle with alternating colors (each tile in the group except the first and last one has a different color from its adjacent tiles in the group).
You have to process queries of two types:
Return an array answer containing the results of the queries of the first type in order.
Note that since colors represents a circle, the first and the last tiles are considered to be next to each other.

**Examples**

**Example 1:**

```
Input: colors = [0,1,1,0,1], queries = [[2,1,0],[1,4]]
Output: [2]
Explanation:

First query:
Change colors[1] to 0.

Second query:
Count of the alternating groups with size 4:
```

**Example 2:**

```
Input: colors = [0,0,1,0,1,1], queries = [[1,3],[2,3,0],[1,5]]
Output: [2,0]
Explanation:

First query:
Count of the alternating groups with size 3:

Second query: colors will not change.
Third query: There is no alternating group with size 5.
```

**Constraints**

- 4 <= colors.length <= 5 * 104
- 0 <= colors[i] <= 1
- 1 <= queries.length <= 5 * 104
- queries[i][0] == 1 or queries[i][0] == 2
- For all i that:
	
queries[i][0] == 1: queries[i].length == 2, 3 <= queries[i][1] <= colors.length - 1
queries[i][0] == 2: queries[i].length == 3, 0 <= queries[i][1] <= colors.length - 1, 0 <= queries[i][2] <= 1
- queries[i][0] == 1: queries[i].length == 2, 3 <= queries[i][1] <= colors.length - 1
- queries[i][0] == 2: queries[i].length == 3, 0 <= queries[i][1] <= colors.length - 1, 0 <= queries[i][2] <= 1

---

## 题目（中文翻译）

存在若干红色和蓝色的瓦片，按环形排列。给定一个整数数组 `colors` 和一个二维整数数组 `queries`。  
- `colors[i]` 表示第 `i` 块瓦片的颜色，`0` 代表蓝色，`1` 代表红色。  
- **交替组（alternating group）** 是指环上连续的一段瓦片，使得组内相邻的两块瓦片颜色互不相同（即组内除首块和末块外的每块瓦片，其颜色都与组内前后相邻的瓦片不同）。  

需要按照 `queries` 中的指令依次处理两类查询：

1. **计数查询** `queries[i] = [1, k]`  
   - 返回环上 **大小恰为 `k` 的交替组的数量**。  
2. **修改查询** `queries[i] = [2, idx, c]`  
   - 将 `colors[idx]` 的颜色修改为 `c`（`c` 为 `0` 或 `1`）。

请返回一个数组 `answer`，其中按出现顺序记录所有计数查询的结果。  
注意：由于 `colors` 表示的是环形结构，首块瓦片和末块瓦片被视为相邻。

---

### 示例

#### 示例 1  
**输入**  
``` 
colors = [0,1,1,0,1], queries = [[2,1,0],[1,4]]
```  
**输出**  
```
[2]
```  
**解释**  

- 第一个查询 `[2,1,0]`：将 `colors[1]` 改为 `0`，此时 `colors` 变为 `[0,0,1,0,1]`。  
- 第二个查询 `[1,4]`：统计大小为 `4` 的交替组的数量，答案为 `2`。

#### 示例 2  
**输入**  
``` 
colors = [0,0,1,0,1,1], queries = [[1,3],[2,3,0],[1,5]]
```  
**输出**  
```
[2,0]
```  
**解释**  

- 第一个查询 `[1,3]`：统计大小为 `3` 的交替组的数量，得到 `2`。  
- 第二个查询 `[2,3,0]`：将 `colors[3]` 改为 `0`，但此时颜色并未发生变化。  
- 第三个查询 `[1,5]`：统计大小为 `5` 的交替组的数量，环中不存在这样的交替组，答案为 `0`。

---

### 约束条件
- `4 <= colors.length <= 5 * 10^4`
- `colors[i]` 只取 `0` 或 `1`
- `1 <= queries.length <= 5 * 10^4`
- `queries[i][0] == 1` 或 `queries[i][0] == 2`
- 当 `queries[i][0] == 1` 时，`queries[i]` 的长度为 `2`，且 `3 <= queries[i][1] <= colors.length - 1`
- 当 `queries[i][0] == 2` 时，`queries[i]` 的长度为 `3`，`0 <= queries[i][1] <= colors.length - 1`，`0 <= queries[i][2] <= 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把整个圆环展开成一条直线**，然后遍历所有长度为 `k` 的连续子数组，检查它们的颜色是否交替。  
具体步骤：

1. 把 `colors` 看成一个长度为 `n` 的普通数组（因为是环，首尾相邻，只要把数组复制一次 `colors*2`，就可以在不越界的情况下检查跨越边界的子数组）。  
2. 对每一个起点 `i (0 ≤ i < n)`，取长度为 `k` 的子数组 `colors[i : i+k]`（在复制后的数组里），判断相邻颜色是否不同。  
3. 若全部相邻颜色不同，就计数 `+1`。  

> **数据结构类比**：把 `colors` 当成一本词典，遍历每一页（起点），检查相邻的两个词（颜色）是否不同，就像在查字典时把相邻的两个词比对。

**为什么正确**：  
只要子数组的每一对相邻颜色都不相等，按照题目定义它就是一个 *alternating group*。把环展开后，所有可能的起点都能被遍历到，所以计数完整。

**时间/空间复杂度**：

- 对每个查询我们都要检查 `n` 个起点，每个起点检查 `k‑1` 对相邻颜色，最坏情况是 `O(n·k)`。  
- 由于 `k` 最多也可能是 `n`，最坏时间复杂度是 `O(n²)`。  
- 只用了原数组的复制，空间 `O(n)`。

> **大白话**：如果把 `n` 想成“1000”，`O(n²)` 就相当于要做 `1000×1000 = 100万` 次比较，查询很多次的话会非常慢。

#### 代码（Python）

```python
def brute_count(colors: list[int], k: int) -> int:
    """暴力统计环上交替子数组的个数，时间 O(n²)"""
    n = len(colors)
    # 为了处理跨越首尾的情况，把数组复制一次
    doubled = colors + colors
    ans = 0
    for start in range(n):                     # 每一个可能的起点
        ok = True
        for i in range(start, start + k - 1):  # 检查相邻两格是否不同
            if doubled[i] == doubled[i + 1]:
                ok = False
                break
        if ok:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  > 这里的 `n²` 表示如果 `n=5·10⁴`，一次查询就要做约 `2.5·10⁹` 次比较，显然不可接受。

- **空间复杂度**：`O(n)`  
  > 只多用了一个长度为 `2n` 的临时数组。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于每次查询都要 **遍历所有起点**。  
我们需要把查询压到 `O(log n)`，并且还能在 **单点修改**（把某块颜色改成 0/1）后快速更新。

关键观察：

1. **交替段的划分**  
   在环上，若相邻两个格子颜色相同，则这两个格子之间是 **“断点”**。所有断点把环划分成若干 **最大交替段**（内部颜色始终交替，段的两端恰好是断点）。  
   例如 `0 1 0 0 1 0` 的断点在第 2、3 位（0‑index），于是得到段 `[0,1]、[0]、[0,1,0]`，长度分别是 `2、1、3`。

2. **段内部的子段计数**  
   对于长度为 `L` 的最大交替段，**任意** 长度为 `k (k≤L)` 的子段都是交替的，且有 `L‑k+1` 种起点。  
   因此整个环中长度恰为 `k` 的交替组数 =  

   \[
   \sum_{L \ge k} (L - k + 1)
   \]

3. **把求和拆成两部分**  

   \[
   \sum_{L \ge k} (L - k + 1)
   = \Bigl(\sum_{L \ge k} (L+1)\Bigr) \;-\; k \cdot \Bigl(\text{cnt}_{L\ge k}\Bigr)
   \]

   只要我们能快速得到  
   - **cnt≥k**：长度 ≥ k 的段的个数  
   - **sum≥k**：这些段的 \((L+1)\) 之和  

   那答案就能在 `O(log n)` 内算出来。

4. **使用「树状数组」(Fenwick Tree / BIT)**  
   - 维护两个 BIT，`bit_cnt` 记录每个长度出现的次数，`bit_sum` 记录 \((L+1)·cnt\)。  
   - BIT 支持「前缀和」查询，利用「总和 - 前缀和(k‑1)」即可得到「≥k」的后缀信息，时间 `O(log n)`。

5. **如何维护「断点集合」**  
   - 断点只有 `0…n‑1` 共 `n` 个位置。我们用另一个 BIT `bit_break`（每个位置 0/1 表示是否是断点）来 **快速定位最近的左/右断点**（前驱、后继）。  
   - BIT 的「第 k 小」查询（二分找最小索引使前缀和≥k）可以在 `O(log n)` 完成，进而得到左/右断点。

6. **单点修改的影响**  
   改变 `colors[pos]` 只会影响两条相邻的边 `(pos‑1,pos)` 与 `(pos,pos+1)`，即最多 **两处断点** 的增删。  
   - **插入断点**：把原来的一个大段 `L_old` 拆成 `L1` 与 `L2`。  
   - **删除断点**：把相邻的两个小段合并成一个大段 `L_new`。  
   对段长度的增删只需要在 `bit_cnt / bit_sum` 中更新相应的值，时间 `O(log n)`。

7. **环上没有断点的特殊情况**  
   当 `bit_break` 中的断点数为 `0`，整个环本身就是一个交替段，长度 `n`。此时长度为 `k` 的交替组数恰好是 `n`（每个起点都可以），而不是 `n‑k+1`。我们单独处理这个情况。

> **类比**：把断点想成“书页的分页符”，每个分页符把一本书分成若干章节。我们关心的是每个章节的页数（长度），以及「所有章节里，页数 ≥ k」的统计信息。Fenwick 树就像一本“快速目录”，能在 `log n` 时间内告诉我们符合条件的章节有多少、总页数是多少。

#### 代码（Python）

```python
from typing import List

# ---------- Fenwick Tree ----------
class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)          # 1-indexed

    def add(self, idx: int, delta: int):
        """在位置 idx（1 ≤ idx ≤ n）上加 delta"""
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx: int) -> int:
        """前缀和，求 [1, idx] 的累计值"""
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx
        return s

    def range_sum(self, l: int, r: int) -> int:
        """求 [l, r] 的和，l、r 均为 1-indexed，且 l ≤ r"""
        return self.sum(r) - self.sum(l - 1)

    # ---------- 第 k 小（顺序统计） ----------
    def kth(self, k: int) -> int:
        """
        返回最小的 idx，使得前缀和 >= k（1 ≤ k ≤ total）。
        若 k 超出范围会返回 n+1。
        """
        idx = 0
        bit_mask = 1 << (self.n.bit_length())   # 最大的 2^p <= n
        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bit_mask >>= 1
        return idx + 1   # 1-indexed

# ---------- 主算法 ----------
class Solution:
    def __init__(self, colors: List[int]):
        self.n = len(colors)
        self.colors = colors[:]                # 工作副本
        self.break_bit = Fenwick(self.n)       # 记录断点 (0/1)
        self.cnt_bit = Fenwick(self.n)         # 记录每种长度出现次数
        self.sum_bit = Fenwick(self.n)         # 记录 (L+1) * 次数

        # 初始断点
        for i in range(self.n):
            if self.colors[i] == self.colors[(i + 1) % self.n]:
                self.break_bit.add(i + 1, 1)    # BIT 使用 1-index

        self._rebuild_segments()               # 根据断点初始化段信息

    # ---------- 辅助：段信息的增删 ----------
    def _add_seg(self, L: int, delta: int):
        """在段长度集合中添加/删除长度 L，delta 为 +1 或 -1"""
        if L == 0:
            return
        self.cnt_bit.add(L, delta)
        self.sum_bit.add(L, delta * (L + 1))

    def _prev_break(self, pos: int) -> int:
        """返回最近的左侧断点位置（0-index），若不存在则返回最右侧的断点（环形）"""
        # pos 为 0-index，BIT 用 1-index
        rank = self.break_bit.sum(pos)                 # ≤ pos 的断点数量
        if rank == 0:                                   # 环形回到最右侧
            total = self.break_bit.sum(self.n)
            return self.break_bit.kth(total) - 1
        else:
            return self.break_bit.kth(rank) - 1

    def _next_break(self, pos: int) -> int:
        """返回最近的右侧断点位置（0-index），若不存在则返回最左侧的断点（环形）"""
        rank = self.break_bit.sum(pos + 1)             # ≤ pos 的断点数量（含 pos）
        total = self.break_bit.sum(self.n)
        if rank == total:                               # 环形回到最左侧
            return self.break_bit.kth(1) - 1
        else:
            return self.break_bit.kth(rank + 1) - 1

    # ---------- 插入 / 删除 断点 ----------
    def _insert_break(self, p: int):
        """在位置 p (0-index) 处插入断点"""
        if self.break_bit.range_sum(p + 1, p + 1) == 1:   # 已经是断点
            return
        # 找到插入前的左、右断点
        left = self._prev_break(p)
        right = self._next_break(p)
        # 原来的大段长度
        L_old = (right - left) % self.n
        # 拆成两段
        L1 = (p - left) % self.n
        L2 = (right - p) % self.n
        # 更新段集合
        self._add_seg(L_old, -1)
        self._add_seg(L1, +1)
        self._add_seg(L2, +1)
        # 最后把断点写入 BIT
        self.break_bit.add(p + 1, 1)

    def _delete_break(self, p: int):
        """删除位置 p (0-index) 处的断点"""
        if self.break_bit.range_sum(p + 1, p + 1) == 0:   # 本来就不是断点
            return
        # 左、右断点（不包括 p 本身）
        left = self._prev_break(p)
        right = self._next_break(p)
        # 被合并的两段长度
        L1 = (p - left) % self.n
        L2 = (right - p) % self.n
        L_new = (right - left) % self.n
        # 更新段集合
        self._add_seg(L1, -1)
        self._add_seg(L2, -1)
        self._add_seg(L_new, +1)
        # 删除断点
        self.break_bit.add(p + 1, -1)

    # ---------- 初始化所有段 ----------
    def _rebuild_segments(self):
        """根据当前的 break_bit，重新统计所有 maximal alternating 段"""
        total_break = self.break_bit.sum(self.n)
        if total_break == 0:                 # 整个环本身是一个交替段
            self._add_seg(self.n, +1)
            return

        # 把所有断点取出来（顺序遍历一次 O(n)）
        breaks = []
        for i in range(self.n):
            if self.break_bit.range_sum(i + 1, i + 1) == 1:
                breaks.append(i)

        m = len(breaks)
        for i in range(m):
            cur = breaks[i]
            nxt = breaks[(i + 1) % m]
            L = (nxt - cur) % self.n          # 长度可能跨越 0 点
            self._add_seg(L, +1)

    # ---------- 查询 ----------
    def query_k(self, k: int) -> int:
        """返回环上长度恰为 k 的交替组数量，时间 O(log n)"""
        if k > self.n:
            return 0
        total_break = self.break_bit.sum(self.n)
        if total_break == 0:                 # 环全交替
            return self.n if k <= self.n else 0

        # cnt_ge = Σ cnt[L] (L ≥ k)
        cnt_lt = self.cnt_bit.sum(k - 1)
        sum_lt = self.sum_bit.sum(k - 1)

        total_cnt = self.cnt_bit.sum(self.n)
        total_sum = self.sum_bit.sum(self.n)

        cnt_ge = total_cnt - cnt_lt
        sum_ge = total_sum - sum_lt

        # 公式： Σ(L+1) - k * cnt
        return sum_ge - k * cnt_ge

    # ---------- 单点修改 ----------
    def update(self, pos: int, new_color: int):
        """把 colors[pos] 改成 new_color，时间 O(log n)"""
        if self.colors[pos] == new_color:
            return

        n = self.n
        # 左边的断点 (pos-1, pos)
        left_edge = (pos - 1) % n
        old_break_left = (self.colors[left_edge] == self.colors[pos])
        new_break_left = (self.colors[left_edge] == new_color)
        if old_break_left != new_break_left:
            if new_break_left:
                self._insert_break(left_edge)
            else:
                self._delete_break(left_edge)

        # 右边的断点 (pos, pos+1)
        right_edge = pos
        old_break_right = (self.colors[pos] == self.colors[(pos + 1) % n])
        new_break_right = (new_color == self.colors[(pos + 1) % n])
        if old_break_right != new_break_right:
            if new_break_right:
                self._insert_break(right_edge)
            else:
                self._delete_break(right_edge)

        # 最后真正修改颜色
        self.colors[pos] = new_color


# ---------- 对外调用 ----------
def alternatingGroupsIII(colors: List[int], queries: List[List[int]]) -> List[int]:
    sol = Solution(colors)
    ans = []
    for q in queries:
        if q[0] == 1:                # 查询类型
            k = q[1]
            ans.append(sol.query_k(k))
        else:                         # 更新类型
            pos, val = q[1], q[2]
            sol.update(pos, val)
    return ans
```

#### 复杂度

- **时间复杂度**  
  - 初始化：遍历一次 `O(n)`。  
  - 每一次查询 (`type 1`)：`O(log n)`（两次 BIT 前缀和）。  
  - 每一次更新 (`type 2`)：至多处理两条边 → 最多两次「插入/删除断点」 → 每次涉及 `O(log n)` 的前驱/后继查找和段长度更新 → 总计 `O(log n)`。  

  与暴力的 `O(n²)` 相比，提升到了对数级，能够轻松应对 `n, queries ≤ 5·10⁴`。

- **空间复杂度**  
  - 三个 BIT 各占 `O(n)`，再加上原数组 `O(n)`，整体 `O(n)`。  

  只用了线性额外空间，符合题目限制。

---

## 心得

- **核心技巧**：把环上的「交替段」抽象为「断点」划分的若干最大段，利用段长度的线性关系转化为「区间计数」问题，再用**树状数组**（Fenwick）完成「区间统计」与「单点更新」的高效操作。  
- **适用场景**：  
  1. 需要统计「满足某种局部约束的子数组」的数量，且约束可以通过「最大合法段」来描述（例如「不含相同相邻元素」）。  
  2. 动态维护「断点」或「分段」信息的题目，如「动态最长递增子段」的变形、环形数组的「连续相同/不同」统计。  
- **一句话总结**：把「交替」转化为「断点划分」的段长度统计，用两棵 BIT 实现「长度≥k」的快速求和。

---

## 反思

- **第一反应**：直接遍历所有起点，检查每段是否交替（暴力）。  
- **最容易踩的坑**  
  1. **环的跨界**：忘记首尾相连导致遗漏跨零点的子段。  
  2. **更新时的双向影响**：改动一个位置会影响左右两条边，必须同时处理，否则段信息会不一致。  
  3. **全部交替的特殊情况**：没有断点时，公式 `Σ(L‑k+1)` 失效，需要单独返回 `n`。  
- **下次类似题的第一步**：先思考「哪些局部不满足条件会把数组切分成独立区间？」（即找断点），再把区间属性转化为可累计的数值，寻找支持「区间统计 + 单点更新」的数据结构（BIT / 线段树）。