# #3382. 点约束下的最大面积矩形 II / Maximum Area Rectangle With Point Constraints II

> 难度：困难 · 标签：Array、Math、Binary Indexed Tree、Segment Tree、Geometry、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-area-rectangle-with-point-constraints-ii/)

---

## 题目（英文原版）

**Description**

There are n points on an infinite plane. You are given two integer arrays xCoord and yCoord where (xCoord[i], yCoord[i]) represents the coordinates of the ith point.
Your task is to find the maximum area of a rectangle that:
Return the maximum area that you can obtain or -1 if no such rectangle is possible.

**Examples**

**Example 1:**

```
Input: xCoord = [1,1,3,3], yCoord = [1,3,1,3]
Output: 4
Explanation:

We can make a rectangle with these 4 points as corners and there is no other point that lies inside or on the border. Hence, the maximum possible area would be 4.
```

**Example 2:**

```
Input: xCoord = [1,1,3,3,2], yCoord = [1,3,1,3,2]
Output: -1
Explanation:

There is only one rectangle possible is with points [1,1], [1,3], [3,1] and [3,3] but [2,2] will always lie inside it. Hence, returning -1.
```

**Example 3:**

```
Input: xCoord = [1,1,3,3,1,3], yCoord = [1,3,1,3,2,2]
Output: 2
Explanation:

The maximum area rectangle is formed by the points [1,3], [1,2], [3,2], [3,3] , which has an area of 2. Additionally, the points [1,1], [1,2], [3,1], [3,2] also form a valid rectangle with the same area.
```

**Constraints**

- 1 <= xCoord.length == yCoord.length <= 2 * 105
- 0 <= xCoord[i], yCoord[i] <= 8 * 107
- All the given points are unique.

---

## 题目（中文翻译）

**描述**  
平面上有 `n` 个点。给定两个整数数组 `xCoord` 和 `yCoord`，其中 `(xCoord[i], yCoord[i])` 表示第 `i` 个点的坐标。  
你的任务是找到满足以下条件的矩形的最大面积：

- 矩形的四个顶点必须全部是给定的点。
- 矩形内部（不含边界）以及边界上**不能**出现除四个顶点之外的其他给定点。

返回可以得到的最大面积；如果不存在满足条件的矩形，则返回 `-1`。

**示例 1**  
```text
Input: xCoord = [1,1,3,3], yCoord = [1,3,1,3]
Output: 4
Explanation:
我们可以使用这四个点作为矩形的四个角，且没有其他点落在矩形内部或边界上。因此最大可能面积为 4。
```

**示例 2**  
```text
Input: xCoord = [1,1,3,3,2], yCoord = [1,3,1,3,2]
Output: -1
Explanation:
唯一可以形成的矩形是顶点 `[1,1]、[1,3]、[3,1]、[3,3]`，但点 `[2,2]` 必然位于矩形内部，所以不存在合法矩形，返回 -1。
```

**示例 3**  
```text
Input: xCoord = [1,1,3,3,1,3], yCoord = [1,3,1,3,2,2]
Output: 2
Explanation:
最大面积矩形由点 `[1,3]、[1,2]、[3,2]、[3,3]` 构成，面积为 2。另一个同样合法且面积相同的矩形是 `[1,1]、[1,2]、[3,1]、[3,2]`。
```

**约束条件**  

- `1 <= xCoord.length == yCoord.length <= 2 * 10^5`
- `0 <= xCoord[i], yCoord[i] <= 8 * 10^7`
- 所有给出的点均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 可能的矩形都枚举一遍：

1. 任选四个不同的点，检查它们是否可以恰好组成一个矩形的四个顶点。  
   - 矩形的两条对边必须平行于坐标轴，所以四个点的 `x` 必须只有两种取值，`y` 也只能有两种取值。  
2. 只要满足上面的条件，就进一步判断矩形内部（包括边界）是否还有别的点。  
   - 对每个剩余的点，检查它的 `x` 是否在左右两条竖边之间，且 `y` 是否在上下两条横边之间。  

把所有合法的矩形面积算出来，取最大的就是答案；如果根本没有合法矩形，返回 `-1`。

> **生活化类比**：把所有点想成一堆 **信封**，我们先随手挑选四个信封的左上、左下、右上、右下角，看看这四个信封能否拼出一个完整的矩形信封；随后再把所有其它信封一个个塞进去，看它们会不会卡在矩形内部。

> **为什么一定对？**  
> 只要把所有可能的四点组合都检查一遍，肯定不会漏掉任何合法矩形；同理，所有不合法的组合也都会被过滤掉。因此，这种“枚举+验证”必然能得到正确答案。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def maxAreaRectangle(xCoord: List[int], yCoord: List[int]) -> int:
    points = list(zip(xCoord, yCoord))          # 把坐标合成 (x, y) 元组
    n = len(points)
    ans = -1

    # 1）枚举任意 4 个点
    for quad in combinations(range(n), 4):
        xs = {points[i][0] for i in quad}
        ys = {points[i][1] for i in quad}
        # 必须恰好有两种不同的 x 和两种不同的 y 才能组成轴对齐矩形
        if len(xs) != 2 or len(ys) != 2:
            continue

        x1, x2 = sorted(xs)    # 左、右边的 x
        y1, y2 = sorted(ys)    # 下、上边的 y
        area = (x2 - x1) * (y2 - y1)
        if area == 0:          # 面积为 0 说明是线段，不算矩形
            continue

        # 2）检查是否有其它点落在矩形内部或边上
        valid = True
        for i in range(n):
            if i in quad:
                continue
            x, y = points[i]
            if x1 <= x <= x2 and y1 <= y <= y2:   # 落在闭区间说明非法
                valid = False
                break

        if valid:
            ans = max(ans, area)

    return ans
```

> **关键行注释**  
> - `xs = {points[i][0] for i in quad}`：用集合把四个点的 `x` 去重，若数量不是 2 则不可能是矩形。  
> - `if x1 <= x <= x2 and y1 <= y <= y2`：判断一个点是否在矩形的 **闭** 区间内（包括边），只要出现一次就直接否定。

#### 复杂度  

- **时间复杂度**：  
  - 枚举四点组合的数量是 `C(n,4) ≈ n⁴ / 24`，每个组合内部又要遍历其余 `O(n)` 个点检查是否在内部。  
  - 故整体是 **O(n⁵)**（粗略估计），对 `n ≤ 2·10⁵` 完全不可接受。  
  - 用大白话说，`n = 1000` 时就要跑 **10⁵⁰** 次，根本不可能在电脑上跑完。  

- **空间复杂度**：  
  - 只存了原始点列表和若干临时集合，都是 `O(n)`。  

> 暴力解只能用来验证思路或在极小数据上实验，真正的比赛题必须找到更快的算法。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举所有四点** 是最耗时的环节。  
真正需要关注的，是 **如何快速找到两条竖边**（即同一个 `x` 上的两点）并在 **右侧最近的 `x`** 处找到对应的另一条竖边，同时保证矩形内部没有任何点。

下面把整个过程拆成几个关键步骤，逐步推导出最终的 `O(n log n)` 解法。

---

#### 2.1 关键观察  

1. **矩形的四条边必须平行于坐标轴**  
   - 因此每条竖边都是“同一个 `x` 坐标上的两点”，每条横边都是“同一个 `y` 坐标上的两点”。  

2. **如果我们从左往右扫描所有不同的 `x`**，当处理到某个 `x = X` 时，**左侧所有点已经全部出现**，右侧的点还没有出现。  
   - 对于当前 `X`，只要找出 **在同一列（同 `x`）上** 的两点 `(X, y1)`、`(X, y2)`（`y1 < y2`），它们可以作为矩形的左竖边。  

3. **左竖边与右竖边之间不能有其他点**。  
   - 换句话说，在区间 `X_left < x < X_right` 内，**没有任何点的 `y` 落在 `[y1, y2]`**。  
   - 如果我们在扫描过程中维护 **“截至目前（左侧已扫过的点）每个 `y` 最后出现的 `x`”**，那么只要在区间 `(y1, y2)`（不含端点）里**最大的 `x`**仍然是 `X_left`，说明在两条竖边之间没有点出现。  

4. **寻找右竖边**  
   - 对于固定的左竖边 `(X_left, y1)`、`(X_left, y2)`，我们只要在后面的 `x` 中找到 **第一次** 同时出现 `y1` 与 `y2` 的列 `X_right`，并且满足上面的 “区间内部没有点” 条件，就得到一个合法矩形。  

5. **最大面积**  
   - 矩形面积 = `(X_right - X_left) * (y2 - y1)`，显然要让两者差值尽可能大。  
   - 因此在找到合法的右竖边后，只需要计算面积并取最大即可。

---

#### 2.2 数据结构：**线段树（Segment Tree）**  

我们需要快速回答以下两类查询：

| 查询类型 | 说明 |
|----------|------|
| **更新** `update(y, X)` | 当我们扫描到点 `(X, y)` 时，把该 `y` 对应的“最近出现的 `x`”更新为 `X`。 |
| **区间最大值** `query(y1+1, y2-1)` | 给定两个 `y`，查询 **开放区间** `(y1, y2)` 内所有 `y` 的最近出现 `x` 的**最大值**。如果该最大值 ≤ `X_left`，说明在两竖边之间没有点。 |

线段树天然支持 **点更新 + 区间最大查询**，时间复杂度为 `O(log M)`，其中 `M` 是离散化后的 `y` 值个数（最多 `n`）。

> **类比**：把线段树想成一棵“层层汇总的树”。每个叶子保存一个 `y` 对应的最新 `x`，内部节点保存它们子区间的最大 `x`。更新某个 `y` 时，只要把对应的叶子改了，往上走的每个父节点都会自动重新记录子区间的最大值；查询区间最大值时，只需要挑出覆盖该区间的若干节点，取它们保存的最大值即可。

---

#### 2.3 完整算法  

1. **离散化 `y` 坐标**  
   - 由于 `y` 的取值范围可达 `8·10⁷`，直接用数组会浪费太多空间。我们把所有出现的 `y` 排序去重，映射到 `[0, m-1]` 的下标。  

2. **把点按照 `x` 从小到大分组**  
   - 使用 `defaultdict(list)` 把同一 `x` 的所有 `y` 收集在一起，形成 `x -> [y1, y2, …]`。  
   - 对每个 `x`，把对应的 `y` 列表再 **升序排序**，方便后面枚举相邻的两点形成竖边。  

3. **初始化线段树**  
   - 所有叶子初始值设为 `-inf`（这里用 `-1`），表示“至今还没有出现过”。  

4. **从左到右遍历所有不同的 `x`**（记作 `curX`）  

   a. **处理左竖边**  
      - 对当前 `curX` 的 `y` 列表 `Y = [y0, y1, …]`（已升序），枚举所有相邻的两点 `(y_i, y_{i+1})`，它们构成一条可能的左竖边。  
      - 对每对 `(y_low, y_high)`，做一次区间最大查询 `maxX = query(idx_low+1, idx_high-1)`（如果 `y_low+1 > y_high-1`，说明没有中间的 `y`，直接把 `maxX = -1`）。  
      - 若 `maxX <= lastX[(y_low, y_high)]`（后面会解释），说明在这两条竖边之间没有点，可以尝试找右竖边。  

   b. **寻找右竖边**  
      - 我们需要在 **后面的 `x`** 中第一次出现 **同样的两条 `y`**。为此维护一个哈希表 `lastX_pair[(y_low, y_high)]`，记录上一次出现这对 `y` 的 `x`（即左竖边的 `x`）。  
      - 当遍历到新的 `curX`，如果这对 `y` 在哈希表里已有记录 `prevX`，则 `prevX` 是左竖边，`curX` 是右竖边。  
      - 此时再次使用线段树查询区间 `(y_low, y_high)` 的最大 `x`，若 **`maxX <= prevX`**，则说明在两列之间没有点，矩形合法。  
      - 计算面积 `area = (curX - prevX) * (y_high - y_low)`，更新全局最大值 `ans`。  

   c. **更新哈希表 & 线段树**  
      - 对当前列的所有相邻 `y` 对 `(y_low, y_high)`，把 `lastX_pair[(y_low, y_high)] = curX`（表示这对在 `curX` 处出现）。  
      - 对列中每个单独的 `y`，执行 `update(idx_y, curX)`，把该 `y` 的最新出现 `x` 设为 `curX`，为后续的区间查询做准备。  

5. **遍历结束**，如果 `ans` 仍为 `-1`，说明不存在合法矩形；否则返回 `ans`。  

---

#### 2.4 为什么能够保证“内部没有点”  

- **线段树保存的是“截至当前列左侧已出现的点的最新 `x`”。**  
- 当我们准备以 `prevX`（左竖边）和 `curX`（右竖边）形成矩形时，查询区间 `(y_low, y_high)` 得到的 `maxX` 表示 **在这段 `y` 区间里最近出现的点的 `x`**。  
- 如果 `maxX ≤ prevX`，说明在 `prevX` 与 `curX` 之间（即两竖边之间）**没有任何点的 `y` 落在区间内部**。  
- 这正是题目要求的“矩形内部（包括边界）没有其它点”。  

---

#### 2.5 复杂度分析  

| 步骤 | 时间 | 空间 |
|------|------|------|
| 离散化 `y` | `O(n log n)`（排序） | `O(n)` |
| 按 `x` 分组并排序每组 `y` | `O(n log n)`（每组内部排序） | `O(n)` |
| 主循环（遍历每个不同的 `x`） | 每个 `x` 处理其 `k` 个 `y`：<br>• 枚举相邻对 → `O(k)` 次查询/更新 <br>• 每次查询/更新 `O(log n)` | 线段树 `O(n)`，哈希表 `O(n)` |
| **总体** | `O(n log n)`（主循环支配） | `O(n)` |

> **与暴力解对比**：暴力需要 `O(n⁵)`（根本不可跑），而最优解只需要 `O(n log n)`，即使 `n = 2·10⁵` 也能在几秒内完成。

---

#### 代码（Python）

```python
import sys
from collections import defaultdict
from bisect import bisect_left
from typing import List, Tuple

# ---------- 线段树实现（区间最大） ----------
class SegTree:
    def __init__(self, size: int):
        self.N = 1
        while self.N < size:          # 建立完整的二叉树，叶子数为 2 的幂
            self.N <<= 1
        self.data = [-1] * (2 * self.N)   # 初始值设为 -1，表示“还未出现”

    # 点更新：把位置 idx 的值设为 val（只会递增，因为 x 随扫描只增大）
    def update(self, idx: int, val: int) -> None:
        i = idx + self.N
        self.data[i] = val
        i >>= 1
        while i:
            self.data[i] = max(self.data[i << 1], self.data[(i << 1) | 1])
            i >>= 1

    # 区间查询 [l, r]（闭区间），返回最大值；若 l > r 返回 -1
    def query(self, l: int, r: int) -> int:
        if l > r:
            return -1
        l += self.N
        r += self.N
        res = -1
        while l <= r:
            if l & 1:
                res = max(res, self.data[l])
                l += 1
            if not (r & 1):
                res = max(res, self.data[r])
                r -= 1
            l >>= 1
            r >>= 1
        return res

# ---------- 主函数 ----------
def maxAreaRectangle(xCoord: List[int], yCoord: List[int]) -> int:
    points = list(zip(xCoord, yCoord))
    n = len(points)

    # 1) 离散化 y
    ys = sorted({y for _, y in points})
    y_to_idx = {y: i for i, y in enumerate(ys)}
    m = len(ys)                     # 离散化后 y 的种类数

    # 2) 按 x 分组并对每组的 y 排序
    cols = defaultdict(list)       # x -> list of y
    for x, y in points:
        cols[x].append(y)
    sorted_x = sorted(cols.keys())
    for x in sorted_x:
        cols[x].sort()              # 只需要升序，后面枚举相邻两点

    # 3) 初始化线段树和辅助哈希表
    seg = SegTree(m)
    last_pair_x = dict()           # (y_low, y_high) -> 最近一次出现该对的 x（左竖边）
    ans = -1

    # 4) 从左到右扫描每一列
    for curX in sorted_x:
        cur_ys = cols[curX]
        k = len(cur_ys)

        # a) 对当前列的所有相邻 y 对，尝试形成矩形
        for i in range(k - 1):
            y_low = cur_ys[i]
            y_high = cur_ys[i + 1]
            idx_low = y_to_idx[y_low]
            idx_high = y_to_idx[y_high]

            pair = (y_low, y_high)

            # 如果这对 y 以前出现过，则它的上一次出现位置是左竖边
            if pair in last_pair_x:
                leftX = last_pair_x[pair]          # 左竖边所在的 x
                # 检查区间 (y_low, y_high) 是否被其他点“打断”
                max_inside = seg.query(idx_low + 1, idx_high - 1)
                if max_inside <= leftX:            # 区间内部没有点
                    area = (curX - leftX) * (y_high - y_low)
                    if area > ans:
                        ans = area

            # 不论是否已出现，都把当前 x 记录为这对 y 的最新出现位置
            last_pair_x[pair] = curX

        # b) 把本列的每个单独 y 更新到线段树
        for y in cur_ys:
            seg.update(y_to_idx[y], curX)

    return ans

# ---------- 测试 ----------
if __name__ == "__main__":
    # 示例 1
    print(maxAreaRectangle([1,1,3,3], [1,3,1,3]))               # 4
    # 示例 2
    print(maxAreaRectangle([1,1,3,3,2], [1,3,1,3,2]))           # -1
    # 示例 3
    print(maxAreaRectangle([1,1,3,3,1,3], [1,3,1,3,2,2]))       # 2
```

> **代码要点注释**  
> - `SegTree.update` 只会把叶子节点的值设为当前 `x`（单调递增），因此内部节点只需要取子区间的最大值。  
> - `last_pair_x` 记录每一对相邻 `y` 最近出现的 `x`，相当于 “这条竖边上一次出现在哪里”。  
> - `seg.query(idx_low+1, idx_high-1)` 查询 **开放** 区间 `(y_low, y_high)`，若返回的最大 `x` 小于等于左竖边的 `x`，说明两竖边之间没有点。  

---

## 心得  

- **核心技巧**：  
  1. **把二维几何约束转化为“一维区间的最大值”查询**。  
  2. **利用线段树（或 Fenwick 树）在 O(log n) 时间内维护“截至目前每个 y 的最新出现 x”**。  
  3. **用哈希表记录相邻 y 对出现的最近列**，实现左竖边 → 右竖边的快速匹配。  

- **适用的题型**（类似思路）  
  1. “最大空矩形 / 最大空正方形” 类题，需要检查矩形内部是否有点。  
  2. “在平面上找不被其它点遮挡的最大矩形” 这类 **扫线 + 区间查询** 的问题。  
  3. “找两个横坐标之间、纵坐标区间内不存在点的最大距离”——同样可以用 **最近出现的 x** 维护。

- **一句话总结解题钥匙**  
  > **把“内部没有点”转化为“在两列之间对应 y 区间的最大出现列 ≤ 左列”，用线段树实时维护每个 y 的最新列即可。**  

---

## 反思  

- **第一反应**：看到“矩形四角必须是给定点，且内部不能有点”，立刻想到 **枚举四点**，这就是暴力解。  
- **最容易踩的坑**  
  1. **区间是否包含端点**：题目要求“内部或在边上都不允许”，所以在判断是否有点时必须把 `y_low`、`y_high` 以及 `x_left`、`x_right` 都排除在查询区间之外。  
  2. **相邻 y 对的选取**：只有相邻的两点才能形成竖边的上下端点；如果跳过相邻点，可能会漏掉合法矩形或误判。  
  3. **离散化时忘记映射回原始坐标**：面积计算必须使用原始 `x`、`y` 差值，而不是离散化后的下标差。  
  4. **更新顺序**：在处理完当前列的矩形后才更新线段树，否则会把同一列的点错误地计入 “左列之后的内部点”。  

- **下次遇到同类题**，第一步应该想到 **“扫线 + 区间数据结构”**：  
  1. 按照某个方向（这里是 `x`）排序。  
  2. 维护一个能快速回答 “在某个一维区间内的最大/最小/计数” 的结构（线段树 / Fenwick / 有序集合）。  
  3. 用哈希表或额外的映射记录“上一次出现的配对”，实现左右两侧的匹配。  

这样就能把原本指数级的搜索压缩到 `O(n log n)`，轻松应对 2·10⁵ 规模的数据。