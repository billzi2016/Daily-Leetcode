# #699. 掉落方块 / Falling Squares

> 难度：困难 · 标签：Array、Segment Tree、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/falling-squares/)

---

## 题目（英文原版）

**Description**

There are several squares being dropped onto the X-axis of a 2D plane.
You are given a 2D integer array positions where positions[i] = [lefti, sideLengthi] represents the ith square with a side length of sideLengthi that is dropped with its left edge aligned with X-coordinate lefti.
Each square is dropped one at a time from a height above any landed squares. It then falls downward (negative Y direction) until it either lands on the top side of another square or on the X-axis. A square brushing the left/right side of another square does not count as landing on it. Once it lands, it freezes in place and cannot be moved.
After each square is dropped, you must record the height of the current tallest stack of squares.
Return an integer array ans where ans[i] represents the height described above after dropping the ith square.

**Examples**

**Example 1:**

```
Input: positions = [[1,2],[2,3],[6,1]]
Output: [2,5,5]
Explanation:
After the first drop, the tallest stack is square 1 with a height of 2.
After the second drop, the tallest stack is squares 1 and 2 with a height of 5.
After the third drop, the tallest stack is still squares 1 and 2 with a height of 5.
Thus, we return an answer of [2, 5, 5].
```

**Example 2:**

```
Input: positions = [[100,100],[200,100]]
Output: [100,100]
Explanation:
After the first drop, the tallest stack is square 1 with a height of 100.
After the second drop, the tallest stack is either square 1 or square 2, both with heights of 100.
Thus, we return an answer of [100, 100].
Note that square 2 only brushes the right side of square 1, which does not count as landing on it.
```

**Constraints**

- 1 <= positions.length <= 1000
- 1 <= lefti <= 108
- 1 <= sideLengthi <= 106

---

## 题目（中文翻译）

有若干正方形从二维平面上的 **X 轴 (X-axis)** 上方掉落。  
给定一个二维整数数组 `positions`，其中 `positions[i] = [left_i, sideLength_i]` 表示第 *i* 个正方形的左边缘对齐在 **X 坐标 (X-coordinate)** `left_i`，且该正方形的 **边长 (side length)** 为 `sideLength_i`。  

每个正方形依次从高于已有方块的高度掉落。它会向下（**负 Y 方向 (negative Y direction)**）运动，直到落在另一正方形的顶部或直接落在 **X 轴 (X-axis)** 上。仅当正方形的底面接触到另一正方形的顶部时才视为“落在”它上面，擦碰到左侧或右侧不算。落地后，正方形固定不动，不能再移动。  

在每一次掉落后，需要记录当前所有正方形堆叠的最高高度。返回一个整数数组 `ans`，其中 `ans[i]` 为第 *i* 次掉落后最高堆叠的高度。

**示例 1**  
输入: `positions = [[1,2],[2,3],[6,1]]`  
输出: `[2,5,5]`  
解释:  
- 第一次掉落后，最高堆叠是正方形 1，高度为 **2**。  
- 第二次掉落后，正方形 2 落在正方形 1 的顶部，最高堆叠高度变为 **5**（2+3）。  
- 第三次掉落后，正方形 3 与前两块不相交，最高堆叠仍为 **5**。  
因此返回 `[2,5,5]`。

**示例 2**  
输入: `positions = [[100,100],[200,100]]`  
输出: `[100,100]`  
解释:  
- 第一次掉落后，最高堆叠是正方形 1，高度为 **100**。  
- 第二次掉落后，正方形 2 只擦碰到正方形 1 的右侧，不算落在其上，所以两块的最高高度仍为 **100**。  
因此返回 `[100,100]`。

**约束条件**  
- `1 <= positions.length <= 1000`  
- `1 <= left_i <= 10^8`  
- `1 <= sideLength_i <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次方块落下都**模拟**一遍：

1. **记录每一段 x 轴上已有的高度**。可以把 X 轴离散成很多小区间（每个整数坐标），用一个字典 `height[x]` 表示坐标 `x` 上方的最高点。  
   - 这相当于把 X 轴想象成一本“高度手册”，查某个位置的高度就像查字典，`key` 是坐标，`value` 是当前最高的堆叠高度。

2. 当第 `i` 个方块 `[left, side]` 落下时，它会占据区间 `[left, left+side)`（左闭右开）。它会**坐在这段区间里已有的最高高度之上**，于是我们遍历这段区间，找出 `max(height[x])`（如果这段区间还没有任何方块，则最高高度为 0），再加上自己的 `side`（方块的厚度），得到它落地后的顶部高度 `cur_h`。

3. 把这段区间的每个坐标的高度都更新为 `cur_h`（因为方块占满了这段），并把全局最高高度 `ans_i` 记录下来。

> **为什么正确**  
> 方块只能在 **完全重叠** 的区间上落在别的方块上（左、右侧只相邻不算），所以它的底部必然与它覆盖区间内所有已有方块的最高面齐平。遍历区间取最大高度，正好模拟了这个过程。

#### 代码（Python）

```python
from typing import List

def fallingSquares(positions: List[List[int]]) -> List[int]:
    # 用字典模拟离散的 X 轴高度表，key 为整数坐标，value 为该坐标上方的最高高度
    height = {}
    res = []            # 记录每一步的全局最高
    cur_max = 0         # 当前最高高度

    for left, side in positions:
        right = left + side          # 方块右端（不包含）
        # 1️⃣ 找到落地后方块的顶部高度
        base = 0                     # 区间内已有的最高面
        for x in range(left, right):
            base = max(base, height.get(x, 0))
        cur_h = base + side          # 方块落地后的顶部

        # 2️⃣ 用新高度更新区间
        for x in range(left, right):
            height[x] = cur_h

        # 3️⃣ 更新全局最高并加入答案
        cur_max = max(cur_max, cur_h)
        res.append(cur_max)

    return res
```

> **关键行注释**  
> - `height.get(x, 0)`: 如果这个坐标之前从未被占用，默认高度为 0（相当于在地面上）。  
> - `range(left, right)`: 左闭右开，确保只遍历方块实际占据的整数坐标。  
> - `cur_max = max(cur_max, cur_h)`: 每次只保留最高的那根塔。

#### 复杂度

- **时间复杂度**：`O(n * L)`，其中 `n = len(positions)`，`L` 为方块的边长（在最坏情况下等于 `right-left`），相当于 `O(n^2)`。  
  - 大白话：每放一块，都要把它占的每个坐标检查一遍；如果有 1000 块，每块平均占 1000 个坐标，就要检查约 1,000,000 次。

- **空间复杂度**：`O(W)`，`W` 为所有方块占据的不同坐标数，最坏情况下等于所有区间的并集大小。  
  - 对于本题的约束（`left` 最大到 10⁸），如果直接使用字典会占用很多内存，但因为 `n ≤ 1000`，实际占用的坐标数仍在可接受范围。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐坐标遍历**：当方块跨度很大时（`sideLength` 可达 10⁶），`range(left, right)` 会遍历上百万次，导致运行慢。

我们需要一种**区间查询/更新**的数据结构，使得：

- **查询**：在区间 `[L, R)` 内求最大高度 → `O(log N)`  
- **更新**：把区间 `[L, R)` 的所有点的高度设为同一个值 → `O(log N)`

这正是**线段树（Segment Tree）**或**树状数组（Fenwick Tree）**的典型任务。不过这里的“设为同一个值”是**区间赋值**，而我们只需要维护**区间最大值**，因此 **线段树 + 懒惰标记**（Lazy Propagation）最合适。

另外，`left` 的取值范围很大（1~10⁸），直接在这么大的坐标上建树会浪费空间。**坐标压缩**（Coordinate Compression）可以把真实坐标映射到 `[0, m-1]` 的小整数序列：

1. 把所有出现的左端点 `left` 和右端点 `left+side` 收集进数组 `coords`。  
2. 对 `coords` 排序并去重，得到有序的离散坐标列表。  
3. 用字典 `idx[x]` 把每个真实坐标映射到离散后的下标。  

这样，原本可能是 10⁸ 的坐标，压缩后最多只有 `2 * n`（因为每个方块产生左、右两个端点）个不同坐标，最多 2000，完全可以在内存里建线段树。

**整体流程**：

| 步骤 | 解释 |
|------|------|
| **坐标收集 & 压缩** | 把所有左、右端点离散化，得到下标 `l = idx[left]`、`r = idx[right]` |
| **区间查询** | 在线段树上查询 `[l, r-1]`（因为右端点是开区间）上的最大高度 `base` |
| **计算新高度** | `cur_h = base + side` |
| **区间更新** | 把 `[l, r-1]` 区间的所有节点的值更新为 `cur_h`（覆盖） |
| **记录全局最高** | 与前一步的 `max_height` 取最大，加入答案列表 |

下面我们一步步实现 **线段树 + 懒惰标记**，并用类比帮助理解：

- **线段树**可以想象成一本“区间手册”，每本手册记录一段连续坐标的最高高度。查询时，手册会把大段的记录合并（类似把几本子手册的最高值取最大），从而快速得到任意子区间的最高值。  
- **懒惰标记**就像在手册的封面贴了一张“待更新”的便签，真正的更新会在需要时再往下传播，避免每次都把所有子区间都改一遍。

#### 代码（Python）

```python
from typing import List
import bisect

class SegmentTree:
    """支持区间最大值查询和区间赋值的线段树（带懒惰标记）"""
    def __init__(self, n: int):
        self.N = n                         # 离散坐标的数量
        self.size = 1
        while self.size < n:               # 扩展到 2 的幂，便于实现
            self.size <<= 1
        self.tree = [0] * (2 * self.size)  # 存最大值
        self.lazy = [0] * (2 * self.size)  # 懒惰标记，0 表示“无待更新”

    def _push(self, node: int):
        """把 node 的懒惰标记向下传播到子节点"""
        if self.lazy[node]:
            # 子节点直接覆盖为 lazy[node]（因为本题只会把区间整体提升到更高的值）
            self.tree[node << 1] = self.lazy[node]
            self.tree[node << 1 | 1] = self.lazy[node]
            self.lazy[node << 1] = self.lazy[node]
            self.lazy[node << 1 | 1] = self.lazy[node]
            self.lazy[node] = 0            # 清除当前节点的标记

    def _range_update(self, l: int, r: int, val: int, node: int, node_l: int, node_r: int):
        """把区间 [l, r]（闭区间）更新为 val"""
        if r < node_l or node_r < l:       # 完全不相交
            return
        if l <= node_l and node_r <= r:    # 完全覆盖
            self.tree[node] = val
            self.lazy[node] = val
            return
        # 部分覆盖，需要向下递归
        self._push(node)                   # 先把旧的懒标记下发
        mid = (node_l + node_r) >> 1
        self._range_update(l, r, val, node << 1, node_l, mid)
        self._range_update(l, r, val, node << 1 | 1, mid + 1, node_r)
        self.tree[node] = max(self.tree[node << 1], self.tree[node << 1 | 1])

    def range_update(self, l: int, r: int, val: int):
        """外部调用的简化接口（l、r 为离散坐标下标，闭区间）"""
        self._range_update(l, r, val, 1, 0, self.size - 1)

    def _range_query(self, l: int, r: int, node: int, node_l: int, node_r: int) -> int:
        """查询区间 [l, r]（闭区间）里的最大值"""
        if r < node_l or node_r < l:
            return 0                     # 不相交返回 0（因为高度非负）
        if l <= node_l and node_r <= r:
            return self.tree[node]
        self._push(node)                 # 先把懒标记下发，保证子树信息是最新的
        mid = (node_l + node_r) >> 1
        left_max = self._range_query(l, r, node << 1, node_l, mid)
        right_max = self._range_query(l, r, node << 1 | 1, mid + 1, node_r)
        return max(left_max, right_max)

    def range_query(self, l: int, r: int) -> int:
        return self._range_query(l, r, 1, 0, self.size - 1)


def fallingSquares(positions: List[List[int]]) -> List[int]:
    # 1️⃣ 收集所有端点并坐标压缩
    coords = []
    for left, side in positions:
        coords.append(left)
        coords.append(left + side)          # 右端点（开区间）
    coords = sorted(set(coords))
    # 映射：真实坐标 -> 离散下标
    idx = {x: i for i, x in enumerate(coords)}

    # 2️⃣ 建立线段树（区间数量 = len(coords) - 1，实际区间是相邻坐标之间的段）
    seg = SegmentTree(len(coords))

    res = []
    cur_max = 0
    for left, side in positions:
        l = idx[left]
        r = idx[left + side] - 1          # 因为线段树使用闭区间，右端点减 1
        # 3️⃣ 查询当前区间的最高面
        base = seg.range_query(l, r)
        cur_h = base + side                # 落地后的顶部高度
        # 4️⃣ 把区间更新为新高度
        seg.range_update(l, r, cur_h)
        # 5️⃣ 更新全局最高并记录答案
        cur_max = max(cur_max, cur_h)
        res.append(cur_max)

    return res
```

> **代码要点注释**  
> - `coords` 中存放的是所有左、右端点，压缩后 `len(coords) ≤ 2·n`，足够小。  
> - `SegmentTree` 的 `size` 向上取到最近的 2 的幂，方便使用 **完全二叉树** 的数组表示法。  
> - `range_update` 与 `range_query` 都是 **闭区间**（`[l, r]`），所以在调用时把右端点的离散下标减 1。  
> - 懒惰标记的意义在于：一次更新可能覆盖很多叶子节点，我们只在后续查询或更细的更新时才真正把它们展开。

#### 复杂度

- **时间复杂度**：`O(n log m)`，其中 `n = len(positions)`，`m = len(coords) ≤ 2n`。  
  - 大白话：每放一块，只需要在树上**查一次**和**改一次**，每次操作都只需要“爬”树的高度（大约 `log₂ m` 次），对 1000 块来说大约几千次运算，十分快。

- **空间复杂度**：`O(m)`，主要是线段树的两个数组 `tree`、`lazy`，大小约为 `4·m`（因为完整二叉树需要 4 倍左右的空间）。  
  - 对于本题 `m ≤ 2000`，只需要几千个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**坐标压缩 + 区间最大查询/更新（线段树）**。  
- **适用的题型**  
  1. “柱状图/线段覆盖”类问题，如 LeetCode 850 *Rectangle Area II*。  
  2. “区间加法/最大值”类，如 LeetCode 699 *Falling Squares*（本题）或 1850 *Minimum Adjacent Swaps to Reach the Kth Smallest Number*（需要区间查询）。  
  3. “离散化 + 线段树” 常见于大坐标范围但元素数量有限的几何或区间问题。

- **一句话总结**：把大坐标压成小整数，再用线段树在“区间”上快速取最大、批量赋值，即可在 O(log n) 里完成每块方块的落地高度计算。

---

## 反思

- **第一反应**：直接把每个坐标的高度存到数组里，遍历区间求最大——这就是暴力解。  
- **最容易踩的坑**  
  1. **坐标范围太大**：直接用 `list` 长度为 10⁸ 会爆内存，需要坐标压缩。  
  2. **左闭右开 vs 左闭右闭**：题目说“左边缘对齐”，右端点不算在方块内部，处理时要注意把右端点减 1（或在查询/更新时使用开区间）。  
  3. **懒惰标记的覆盖**：这里的更新是把区间整体提升到更高的值，直接覆盖即可；如果是“取最大”更新，需要把 `lazy` 取 `max` 而不是直接赋值。  
- **下次遇到同类题**：第一步先**坐标压缩**，把所有涉及的端点离散化；随后判断是否需要**区间查询/更新**，如果是，就准备**线段树**或**树状数组**来完成 O(log n) 的操作。这样即可把“看似 O(n²)”的问题降到 “O(n log n)”。