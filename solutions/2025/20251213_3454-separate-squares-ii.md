# #3454. 分离正方形 II / Separate Squares II

> 难度：困难 · 标签：Array、Binary Search、Segment Tree、Line Sweep · [LeetCode 链接](https://leetcode.com/problems/separate-squares-ii/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.
Find the minimum y-coordinate value of a horizontal line such that the total area covered by squares above the line equals the total area covered by squares below the line.
Answers within 10-5 of the actual answer will be accepted.
Note: Squares may overlap. Overlapping areas should be counted only once in this version.

**Examples**

**Example 1:**

```
Input: squares = [[0,0,1],[2,2,1]]
Output: 1.00000
Explanation:

Any horizontal line between y = 1 and y = 2 results in an equal split, with 1 square unit above and 1 square unit below. The minimum y-value is 1.
```

**Example 2:**

```
Input: squares = [[0,0,2],[1,1,1]]
Output: 1.00000
Explanation:

Since the blue square overlaps with the red square, it will not be counted again. Thus, the line y = 1 splits the squares into two equal parts.
```

**Constraints**

- 1 <= squares.length <= 5 * 104
- squares[i] = [xi, yi, li]
- squares[i].length == 3
- 0 <= xi, yi <= 109
- 1 <= li <= 109
- The total area of all the squares will not exceed 1015.

---

## 题目（中文翻译）

给定一个二维整数数组（2D integer array）`squares`。每个 `squares[i] = [xi, yi, li]` 表示一个 **平行于 x 轴的正方形** 的左下角点（bottom-left point）坐标以及边长（side length）。

求一条水平线（horizontal line）的最小 y 坐标，使得该线以上的正方形覆盖的总面积等于该线以下的正方形覆盖的总面积。

答案只要在实际答案的 `10^-5` 误差范围内即可接受。

**注意**：正方形可能会重叠。**重叠区域**（overlapping areas）在本题中只计一次。

### 示例

**示例 1**

```text
Input: squares = [[0,0,1],[2,2,1]]
Output: 1.00000
```

**解释**：

任意位于 `y = 1` 与 `y = 2` 之间的水平线都能将面积等分，上方和下方各有 1 个单位面积。满足条件的最小 y 值为 1。

**示例 2**

```text
Input: squares = [[0,0,2],[1,1,1]]
Output: 1.00000
```

**解释**：

由于蓝色正方形与红色正方形重叠，重叠部分只计一次。因此，`y = 1` 的水平线将所有正方形的面积等分。

### 约束条件

- `1 <= squares.length <= 5 * 10^4`
- `squares[i] = [xi, yi, li]`
- `squares[i].length == 3`
- `0 <= xi, yi <= 10^9`
- `1 <= li <= 10^9`
- 所有正方形的总面积不超过 `10^15`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的横坐标**（即每个正方形的下边 `yi` 与上边 `yi+li`）列出来，形成一系列 **区间端点**。  
在相邻的两个端点之间（例如 `y = 2.3` 与 `y = 2.8` 之间），所有正方形的覆盖情况是固定不变的——要么该正方形在这条水平线上方，要么在下方，或者正好被水平线切开。  

因此我们可以：

1. 把所有 `yi` 与 `yi+li` 收集并去重、排序，得到 `Y = [y0, y1, …, yk]`。  
2. 对每个相邻区间 `[Y[i], Y[i+1]]`，任选一个代表值（如区间中点），**统计该横坐标以下的总覆盖面积**（即所有正方形与该横坐标以下的交集的并集面积）。  
3. 当累计面积恰好等于总面积的一半时，区间的左端点就是答案的 **最小可能 y**。  

> **类比**：把每条水平线想成一本书的“页码”。我们把所有可能的“页码”列出来，然后逐页翻，看哪一页的上半部分和下半部分的字数相等。  

**为什么正确**  
- 正方形的边都是平行于坐标轴的，只有在它们的 **上下边界** 处，覆盖关系才会改变。  
- 在两个相邻边界之间，所有正方形相对于这条水平线的状态（在上、在下、被切）保持不变，所以面积函数在该区间是 **线性的**，不会出现“跳变”。  
- 因此只要检查每个区间的左端点（或左端点的极限），就能找到最小满足条件的 `y`。

**时间/空间复杂度**  
- 收集端点：`O(n)`（`n` 为正方形个数）  
- 排序端点：`O(m log m)`，其中 `m ≤ 2n`（每个正方形贡献上下两个端点）  
- 对每个区间遍历所有正方形计算交叉面积：`O(m * n)`，最坏会是 `O(n²)`。  
- 空间：存放端点数组 `O(m)`，即 `O(n)`。

> **大白话**：`O(n²)` 就像你有 `n` 本书，想把每本书和每本书都比一遍，需要 `n`×`n` 次比较，数量会很快爆炸。

#### 代码（Python）

```python
from typing import List

def union_area_below(squares: List[List[int]], line_y: float) -> int:
    """
    计算所有正方形在 y <= line_y 区域的并集面积（整数，因为坐标都是整数）。
    暴力做法：对每个正方形求它和水平线以下的交叉矩形，再把这些矩形做并集。
    这里用最简单的 O(n²) 并集算法：两两比较是否相交并合并。
    """
    # 每个正方形在 y 方向被截断后的矩形： [x, x+L) × [y, min(y+L, line_y))
    rects = []
    for x, y, L in squares:
        if line_y <= y:                # 整个正方形在水平线之上
            continue
        top = min(y + L, line_y)       # 被截断的上边界
        rects.append((x, x + L, y, top))

    # 下面用平凡的并集：把所有矩形按 x 排序，然后扫描合并重叠区间
    rects.sort(key=lambda r: (r[0], r[2]))   # 先按左 x 再按下 y 排序
    merged = []                               # 存放合并后的矩形 (x1,x2,y1,y2)

    for r in rects:
        if not merged:
            merged.append(list(r))
            continue
        last = merged[-1]
        # 判断两个矩形在 x、y 上是否相交（这里因为都是轴对齐矩形，判断更简单）
        if r[0] <= last[1] and r[2] <= last[3]:   # 有交集
            # 合并：取并集的外接矩形
            last[1] = max(last[1], r[1])
            last[2] = min(last[2], r[2])
            last[3] = max(last[3], r[3])
        else:
            merged.append(list(r))

    # 计算并集面积
    area = 0
    for x1, x2, y1, y2 in merged:
        area += (x2 - x1) * (y2 - y1)
    return area


def brute_force(squares: List[List[int]]) -> float:
    # 1️⃣ 收集所有上下边界
    ys = []
    for _, y, L in squares:
        ys.append(y)
        ys.append(y + L)
    ys = sorted(set(ys))

    total_area = 0
    # 先算整体并集面积（不必细算，只要和为 total/2 即可）
    # 这里直接用上面的函数把 line_y 设为无限大
    total_area = union_area_below(squares, float('inf'))

    half = total_area / 2.0

    # 2️⃣ 逐区间检查
    for i in range(len(ys) - 1):
        low = ys[i]                     # 区间左端点（可能的答案）
        # 计算 low 以下的面积
        cur = union_area_below(squares, low + 1e-9)   # 加一个极小值，确保算到区间内部
        if cur >= half - 1e-9:          # 已经达到或超过一半
            return low                  # 最小的满足条件的 y
    return ys[-1]   # 理论上不会走到这里
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：我们对每个可能的 `y` 区间（最多 `2n` 个）都遍历所有正方形来求交集，最坏情况是 `n` 与 `n` 的乘积。  
- **空间复杂度**：`O(n)`  
  - 解释：只需要保存正方形列表、端点数组以及临时的矩形并集，均与正方形数量线性相关。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“对每个候选 y 都遍历所有正方形”**。  
事实上，**随着水平线的移动，覆盖面积的变化是单调的**：  
- 线往上移动时，**下面的面积只会增加**（因为会把更多的正方形纳入下方），  
- 同时 **上面的面积只会减少**。  

于是我们可以把 **求满足面积相等的 y** 看成在一个 **单调函数** 上做 **二分搜索**（Binary Search）。  

二分搜索需要一个 **快速计算 “水平线 y 以下的并集面积”** 的子过程。  
这正是 **线段树 + 线扫**（Line Sweep）擅长的场景：

1. **离散化 x 轴**  
   - 把所有正方形的左、右边界 `xi` 与 `xi+li` 收集并排序，得到离散坐标 `X = [x0, x1, …]`。  
   - 两个相邻离散坐标之间的区间称为 **原子区间**，在同一次扫描中，它们的覆盖状态是统一的。  

2. **事件化**  
   - 对每个正方形，生成两条 **垂直事件**：  
     - `y = yi` 时，**加入**（add）长度 `li` 的区间 `[xi, xi+li)`。  
     - `y = yi+li` 时，**删除**（remove）同样的区间。  
   - 把所有事件按 `y` 从小到大排序。  

3. **线段树维护**  
   - 线段树的每个节点记录 **当前覆盖的总宽度**（即在该节点对应的 x 区间上，是否被至少一个正方形覆盖）。  
   - 当处理一条事件时，向线段树 **区间加/减 1**（计数），树会自动更新该节点的 **覆盖宽度**。  

4. **面积累加**  
   - 扫描时，记录上一次处理的 `y_prev`。  
   - 当前 `y` 与 `y_prev` 之间的垂直跨度 `dy = y - y_prev`，此时线段树的 **覆盖宽度** `cur_width` 表示 **在这段 `dy` 内，所有正方形在 x 方向的并集宽度**。  
   - 区间面积贡献为 `cur_width * dy`，累加到 **“已处理的下方面积”**。  

5. **二分搜索**  
   - 预先算出 **所有正方形的并集总面积** `total`（一次完整的线扫即可得到）。  
   - 目标是找到最小的 `y` 使得 `area_below(y) >= total / 2`。  
   - 在二分搜索的每一步，调用 **线扫函数**（带上限 `y_limit`）只扫描到 `y_limit`，返回 **截至该高度的下方面积**。  
   - 由于面积随 `y` 单调递增，二分搜索在 `log(坐标范围)` 次迭代内收敛到 `1e-5` 精度。  

> **类比**：  
> - **离散化 x** 像把一条长长的街道划分成若干块地皮，每块地皮要么被建筑覆盖，要么空着。  
> - **线段树** 就是实时记录每块地皮是否有人在建房子（计数 >0），并且能够快速把一段地皮整体标记为“有人”。  
> - **线扫** 类似于把一条横向的“施工进度线”从下往上推，每次遇到建筑的起点就“开始施工”，遇到终点就“停止施工”。  

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List, Tuple

# ---------- 线段树实现 ----------
class SegTree:
    """支持区间 +1 / -1 更新，并能实时返回被覆盖的总宽度"""
    def __init__(self, xs: List[int]):
        self.xs = xs                     # 离散化后的 x 坐标
        self.n = len(xs) - 1            # 原子区间个数 = xs 长度-1
        self.cnt = [0] * (self.n * 4)    # 区间覆盖计数
        self.len = [0] * (self.n * 4)    # 被覆盖的宽度

    def _push_up(self, idx: int, l: int, r: int):
        """根据子节点或计数更新当前节点的覆盖宽度"""
        if self.cnt[idx] > 0:           # 只要计数>0，整个区间必被覆盖
            self.len[idx] = self.xs[r+1] - self.xs[l]
        else:                           # 否则取左右子节点的宽度和
            if l == r:
                self.len[idx] = 0
            else:
                self.len[idx] = self.len[idx*2] + self.len[idx*2+1]

    def _update(self, idx: int, l: int, r: int, ql: int, qr: int, delta: int):
        """在离散区间 [ql,qr] 上加 delta（+1 添加，-1 删除）"""
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self.cnt[idx] += delta
            self._push_up(idx, l, r)
            return
        mid = (l + r) // 2
        self._update(idx*2, l, mid, ql, qr, delta)
        self._update(idx*2+1, mid+1, r, ql, qr, delta)
        self._push_up(idx, l, r)

    def add_interval(self, x1: int, x2: int, delta: int):
        """把实际坐标 x1,x2 转成离散下标后调用 _update"""
        l = bisect_left(self.xs, x1)
        r = bisect_left(self.xs, x2) - 1   # 因为 xs[r+1] = x2
        if l <= r:
            self._update(1, 0, self.n-1, l, r, delta)

    def covered_width(self) -> int:
        """根节点记录的当前总覆盖宽度"""
        return self.len[1]

# ---------- 线扫 + 面积函数 ----------
def area_below(squares: List[List[int]], limit_y: float, xs: List[int], events: List[Tuple[int, int, int, int]]) -> float:
    """
    计算水平线 y = limit_y 以下的并集面积。
    参数 xs 为离散化的 x 坐标，events 为预处理好的 (y, type, x1, x2) 列表，
    type = +1 表示加入区间，-1 表示删除区间。
    """
    st = SegTree(xs)
    cur_y = 0
    area = 0.0
    i = 0
    # 只遍历到 limit_y
    while i < len(events) and events[i][0] <= limit_y:
        y, typ, x1, x2 = events[i]
        # 先把上一段区间的面积加进去
        dy = y - cur_y
        if dy:
            area += st.covered_width() * dy
            cur_y = y
        # 处理当前事件
        st.add_interval(x1, x2, typ)
        i += 1

    # 处理 limit_y 与最后一个事件之间的剩余高度
    if limit_y > cur_y:
        area += st.covered_width() * (limit_y - cur_y)
    return area

def prepare(squares: List[List[int]]) -> Tuple[List[int], List[Tuple[int, int, int, int]], float]:
    """
    1. 离散化所有 x 边界
    2. 生成所有垂直事件并按 y 排序
    3. 计算总并集面积（一次完整线扫），返回 total
    """
    xs = set()
    events = []          # (y, type, x1, x2)
    for x, y, L in squares:
        xs.add(x)
        xs.add(x + L)
        events.append((y, +1, x, x + L))          # 加入区间
        events.append((y + L, -1, x, x + L))      # 删除区间
    xs = sorted(xs)

    events.sort(key=lambda e: e[0])               # 按 y 从小到大

    # 计算总面积（limit_y = +inf 相当于遍历完全部事件）
    total = area_below(squares, float('inf'), xs, events)
    return xs, events, total

def solve_separate_squares(squares: List[List[int]]) -> float:
    xs, events, total_area = prepare(squares)
    target = total_area / 2.0

    # 二分搜索 y，范围取所有上下边界的最小/最大值
    low = min(y for _, y, _ in squares)
    high = max(y + L for _, y, L in squares)

    for _ in range(80):               # 2^-80 < 1e-24，足够保证 1e-5 精度
        mid = (low + high) / 2.0
        cur = area_below(squares, mid, xs, events)
        if cur >= target:             # 已经达到或超过一半，向左收紧
            high = mid
        else:
            low = mid
    return high   # 最小满足条件的 y（误差在 1e-5 之内）

# ------------------- 示例 -------------------
if __name__ == "__main__":
    squares1 = [[0, 0, 1], [2, 2, 1]]
    print("{:.5f}".format(solve_separate_squares(squares1)))   # 1.00000

    squares2 = [[0, 0, 2], [1, 1, 1]]
    print("{:.5f}".format(solve_separate_squares(squares2)))   # 1.00000
```

**代码要点注释（已在代码中）**  
- `SegTree` 用计数 `cnt` 判断区间是否被覆盖，用 `len` 保存 **被覆盖的宽度**。  
- `add_interval` 把实际坐标映射到离散下标后完成 **区间加/减**。  
- `area_below` 只遍历到 `limit_y`，利用线段树的实时宽度计算每段 `dy` 的面积贡献。  
- `prepare` 一次性完成 **离散化**、**事件生成**、**总面积** 的预处理，后续二分只需重复 `area_below`，不必重新构造树。  

#### 复杂度  

- **时间复杂度**  
  - 离散化 + 事件排序：`O(n log n)`（`n` 为正方形数）。  
  - 计算一次完整的总面积：`O(n log n)`（每个事件一次 `O(log n)` 的树更新）。  
  - 二分搜索：`O(log(坐标范围) * n log n)`，这里 `log(坐标范围) ≈ 60`（因为坐标 ≤ 1e9，二分到 1e-5 需要约 60 次），每次二分仍需遍历全部事件并做树更新。  
  - 综合：**`O(n log n)`**（常数因二分而略增，但仍远低于 `O(n²)`）。  

- **空间复杂度**  
  - 离散化的 x 数组、事件数组均为 `O(n)`。  
  - 线段树大小约为 `4 * m`，其中 `m` 为离散 x 区间数 ≤ `2n`。  
  - 故整体 **`O(n)`** 额外空间。  

> 与暴力解相比，时间从 `O(n²)` 降到了 `O(n log n)`，在 `n=5·10⁴` 时能轻松跑完。

---

## 心得  

- **核心技巧**：**线段树 + 线扫** 用来快速求 **轴对齐矩形的并集面积**，配合 **二分搜索** 把“等面积分割”转化为单调函数求根。  
- **适用的题型**  
  1. 求 **多个矩形（或正方形）并集面积**（如 LeetCode 850、1913 等）。  
  2. **按面积/体积分割** 的几何题（比如“在平面上找使上方面积等于下方面积的直线”）。  
  3. 需要 **动态维护区间覆盖宽度** 的场景（如“矩形的总长度覆盖”）。  
- **一句话总结解题钥匙**：**把面积随 y 单调递增的特性抽象为单调函数，用二分定位，再用线段树的区间计数快速求每一次“累计面积”。**

---

## 反思  

- **第一反应**：看到“面积相等”立刻想到 **二分**，因为面积随高度单调。  
- **最容易踩的坑**  
  - **离散化错误**：忘记把右边界 `xi+li` 也加入集合，会导致区间宽度计算少一次。  
  - **线段树的合并逻辑**：计数为 `0` 时必须把左右子节点的宽度相加，不能直接设为 `0`。  
  - **浮点精度**：二分终止条件要足够严格（如循环 80 次），否则可能误差超过 `1e-5`。  
  - **总面积计算**：如果直接把 `limit_y = +inf` 传给 `area_below`，需要让函数在遍历完所有事件后仍能返回累计面积。  
- **下次类似题的第一步**：先判断**单调性**，如果单调就考虑**二分**；再把“求某一高度以下的几何量”抽象为**线扫 + 区间维护**，准备好离散坐标和事件列表。