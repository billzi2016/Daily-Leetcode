# #3394. 检查网格能否被切割成若干部分 / Check if Grid can be Cut into Sections

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/check-if-grid-can-be-cut-into-sections/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the dimensions of an n x n grid, with the origin at the bottom-left corner of the grid. You are also given a 2D array of coordinates rectangles, where rectangles[i] is in the form [startx, starty, endx, endy], representing a rectangle on the grid. Each rectangle is defined as follows:
Note that the rectangles do not overlap. Your task is to determine if it is possible to make either two horizontal or two vertical cuts on the grid such that:
Return true if such cuts can be made; otherwise, return false.

**Examples**

**Example 1:**

```
Input: n = 5, rectangles = [[1,0,5,2],[0,2,2,4],[3,2,5,3],[0,4,4,5]]
Output: true
Explanation:

The grid is shown in the diagram. We can make horizontal cuts at y = 2 and y = 4 . Hence, output is true.
```

**Example 2:**

```
Input: n = 4, rectangles = [[0,0,1,1],[2,0,3,4],[0,2,2,3],[3,0,4,3]]
Output: true
Explanation:

We can make vertical cuts at x = 2 and x = 3 . Hence, output is true.
```

**Example 3:**

```
Input: n = 4, rectangles = [[0,2,2,4],[1,0,3,2],[2,2,3,4],[3,0,4,2],[3,2,4,4]]
Output: false
Explanation:
We cannot make two horizontal or two vertical cuts that satisfy the conditions. Hence, output is false.
```

**Constraints**

- 3 <= n <= 109
- 3 <= rectangles.length <= 105
- 0 <= rectangles[i][0] < rectangles[i][2] <= n
- 0 <= rectangles[i][1] < rectangles[i][3] <= n
- No two rectangles overlap.

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`，表示一个 `n × n` 的网格（grid），原点位于网格的左下角。另给定一个二维坐标数组 `rectangles`，其中 `rectangles[i]` 形如 `[startx, starty, endx, endy]`，表示网格上的一个矩形（rectangle）。每个矩形的定义如下：

- 左下角坐标为 `(startx, starty)`，右上角坐标为 `(endx, endy)`。
- `0 ≤ startx < endx ≤ n`，`0 ≤ starty < endy ≤ n`。

已知所有矩形互不重叠（no overlap）。你的任务是判断是否可以在网格上做 **两条水平切割**（horizontal cuts）或 **两条垂直切割**（vertical cuts），使得满足题目要求。

- 若可以进行这样的切割，返回 `true`；否则返回 `false`。

---

**示例**

**示例 1**  
``` 
Input: n = 5, rectangles = [[1,0,5,2],[0,2,2,4],[3,2,5,3],[0,4,4,5]]
Output: true
```
**解释**：  
如图所示，我们可以在 `y = 2` 和 `y = 4` 处做两条水平切割。因此答案为 `true`。

**示例 2**  
``` 
Input: n = 4, rectangles = [[0,0,1,1],[2,0,3,4],[0,2,2,3],[3,0,4,3]]
Output: true
```
**解释**：  
我们可以在 `x = 2` 和 `x = 3` 处做两条垂直切割。因此答案为 `true`。

**示例 3**  
``` 
Input: n = 4, rectangles = [[0,2,2,4],[1,0,3,2],[2,2,3,4],[3,0,4,2],[3,2,4,4]]
Output: false
```
**解释**：  
不存在满足条件的两条水平切割或两条垂直切割。因此答案为 `false`。

---

**约束条件**  

- `3 ≤ n ≤ 10^9`
- `3 ≤ rectangles.length ≤ 10^5`
- `0 ≤ rectangles[i][0] < rectangles[i][2] ≤ n`
- `0 ≤ rectangles[i][1] < rectangles[i][3] ≤ n`
- 任意两个矩形均不重叠（No two rectangles overlap）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把 **切线** 想成在网格上画一条不碰任何矩形的直线。  
- **水平切**：在某个 `y = k`（`0 < k < n`）的水平线上，所有矩形的 **纵向投影**（即 `[starty, endy]`）都要么在这条线的上面，要么在下面，不能跨过它。  
- **垂直切**：同理，在 `x = k` 上，所有矩形的 **横向投影**（`[startx, endx]`）都必须完全在左侧或右侧，不能穿过。

如果我们能找到 **两条互不相交的水平切线**（或两条垂直切线），就把整个 `n × n` 的网格划分成 **3 条不相交的条带**，每条条带里装着若干矩形，这就是题目要求的 “可以切”。  

**暴力做法**：  
1. 枚举所有可能的切线位置 `k`（`k` 可以是 1 … n‑1 的整数）。  
2. 对每条候选切线，遍历所有矩形，检查是否有矩形的投影跨过 `k`。  
3. 记录所有合法的切线位置，然后在这些合法位置里挑选任意两条，看它们是否能把网格分成 3 段（即两条切线之间必须有非零距离）。  

**为什么能得到正确答案**：  
只要切线不穿过任何矩形，它们就不会破坏矩形的完整性。两条合法切线自然把区间 `[0, n]` 划分成 3 段，只要这 3 段都非空（长度 > 0），就满足题意。

**时间/空间复杂度**  
- 枚举 `k` 的次数是 `O(n)`（`n` 最大可达 `10^9`），对每个 `k` 又要遍历全部矩形 `m = len(rectangles)`，所以总时间是 `O(n · m)`，在最坏情况下几乎是 **指数级** 的不可接受。  
- 只使用常数级额外空间 `O(1)`（不计输入）。

> **大白话**：`O(n·m)` 就像把一整块大米（`n`）分成很多小袋子（`k`），每袋子里再装上一箱子米（`m`），箱子越多，袋子越多，工作量会爆炸。

---

#### 代码（Python）

```python
def can_cut_bruteforce(n, rectangles):
    # 记录所有可以做水平切的 y 坐标
    good_h = []
    for y in range(1, n):                     # 逐个可能的切线位置
        ok = True
        for sx, sy, ex, ey in rectangles:
            if sy < y < ey:                   # 矩形跨过了 y
                ok = False
                break
        if ok:
            good_h.append(y)

    # 同理记录所有可以做垂直切的 x 坐标
    good_v = []
    for x in range(1, n):
        ok = True
        for sx, sy, ex, ey in rectangles:
            if sx < x < ex:
                ok = False
                break
        if ok:
            good_v.append(x)

    # 检查是否能选出两条合法切线，使它们之间有空隙
    def has_two_cuts(arr):
        # arr 已经是从小到大排好的合法切线坐标
        for i in range(len(arr) - 1):
            if arr[i+1] - arr[i] > 0:          # 两条切线之间有宽度
                # 再找一条在它们右边的切线
                for j in range(i+2, len(arr)):
                    if arr[j] - arr[i+1] > 0:
                        return True
        return False

    return has_two_cuts(good_h) or has_two_cuts(good_v)
```

> 代码里每一行都有中文注释，直接复制即可运行。  

#### 复杂度

- **时间复杂度**：`O(n · m)`  
  - 解释：`n`（最多 10⁹）是切线候选数，`m`（最多 10⁵）是矩形数，两者相乘会导致运行时间极其庞大，实际会超时。  
- **空间复杂度**：`O(m)`（存储合法切线列表，最坏情况每条切线都合法）

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于 **逐个切线去检查所有矩形**。  
实际上我们只需要知道 **哪些坐标上有矩形的投影跨过**，而不必对每个坐标都遍历一次。  

把每个矩形在 **x 方向** 的投影看成一个闭区间 `[startx, endx]`（左闭右开更好理解），同理在 **y 方向** 看成 `[starty, endy]`。  
如果我们把所有区间按照左端点 `start` 排序，就可以一次遍历得到 **所有“空隙”**（即没有任何区间覆盖的坐标段）。  

**关键观察**：  
- 一条合法的切线必须落在 **两个相邻区间之间的空隙** 上。  
- 要把网格划分成 3 条条带，需要 **至少两段空隙**（两条切线之间也必须有宽度）。  

因此问题等价于：  
> 在 x 方向的所有投影区间里，是否存在 **≥2** 个不相交的空隙？  
> 同理检查 y 方向。

**如何快速找空隙**：

1. 把所有 `[l, r]` 按 `l` 升序排列。  
2. 用一个变量 `cur_max` 记录已经遍历过的区间的 **最大右端点**。  
3. 当遍历到第 `i` 个区间时，若 `cur_max == l_i`（前面的区间最右端正好等于当前区间的左端），说明 **在 `cur_max` 这个位置出现了空隙**（宽度为 `l_i - cur_max = 0`，实际上这里是“紧贴”，不算合法切线）。  
   当 `cur_max < l_i` 时，说明 **在 `cur_max` 与 `l_i` 之间有宽度 > 0 的空隙**，这正是一条可以切的线。我们记录一次。  
4. 更新 `cur_max = max(cur_max, r_i)`，继续向后遍历。  

遍历结束后，只要记录的空隙数 `gap_cnt >= 2`，就可以在该方向上完成两条切线。  

因为我们只遍历一次排序好的列表，时间是 `O(m log m)`（排序）+ `O(m)`（一次扫描），空间 `O(m)`（存储区间），这在 `m ≤ 10⁵` 时完全可以接受。

> **类比**：把区间想成 **道路上的施工段**，`cur_max` 是已经修好的最远路段。每当出现一段 **未施工的路**（`cur_max < next_start`），我们就可以在这段空地上“挖一条切线”。要把城市分成 3 区，只需要找到 **两块空地**。

#### 代码（Python）

```python
from typing import List

def can_cut(n: int, rectangles: List[List[int]]) -> bool:
    """
    判断是否能在 n×n 网格上做两条水平切或两条垂直切，使每条切线不穿过任何矩形。
    """
    # 把投影区间分别抽取出来
    xs = [(r[0], r[2]) for r in rectangles]   # (startx, endx)
    ys = [(r[1], r[3]) for r in rectangles]   # (starty, endy)

    def enough_gaps(intervals: List[tuple]) -> bool:
        """
        判断在给定的闭区间列表中，是否存在至少两段空隙。
        intervals 为 (l, r)，左闭右开（l <= x < r）。
        """
        # 按左端点升序排列
        intervals.sort(key=lambda x: x[0])
        cur_max = intervals[0][1]          # 已经覆盖的最右端（不含）
        gap_cnt = 0                         # 已找到的空隙数量

        for l, r in intervals[1:]:
            if cur_max < l:                 # 发现宽度 > 0 的空隙
                gap_cnt += 1
                if gap_cnt >= 2:           # 已经够了，直接返回
                    return True
            # 更新已覆盖的最右端（取最大）
            cur_max = max(cur_max, r)

        return False

    # 检查横向（垂直切）和纵向（水平切）两种可能
    return enough_gaps(xs) or enough_gaps(ys)
```

**代码要点说明**  

| 行号 | 关键含义 | 中文注释 |
|------|----------|----------|
| 4‑5  | 把每个矩形的 `x`、`y` 投影抽成区间 | `xs`、`ys` 分别存储横向/纵向区间 |
| 9‑25 | `enough_gaps`：判断一个方向上是否有 ≥2 个空隙 | 采用 **排序 + 单次扫描** 的贪心 |
| 12   | 按左端点排序，确保从左到右逐段检查 | `intervals.sort(key=lambda x: x[0])` |
| 13   | `cur_max` 记录已覆盖的最右端（不含） | 初始为第一个区间的右端 |
| 16‑19| 若 `cur_max < l`，说明出现宽度 > 0 的空隙 | 记录一次 `gap_cnt`，提前返回 |
| 21   | 更新 `cur_max` 为目前看到的最大右端 | `cur_max = max(cur_max, r)` |
| 27‑28| 主函数返回：横向或纵向任意一种满足即为 True | `or` 逻辑 |

#### 复杂度

- **时间复杂度**：`O(m log m)`  
  - 排序两次（`x`、`y`），每次 `O(m log m)`，后面的线性扫描是 `O(m)`。  
  - 与暴力的 `O(n·m)` 相比，**只和矩形数量有关**，即使 `n` 很大（10⁹）也毫无压力。  
- **空间复杂度**：`O(m)`  
  - 需要存放投影区间的列表，大小与矩形数量线性相关。

---

## 心得  

- **核心技巧**：把二维切割问题转化为“一维区间划分”，利用**排序 + 贪心找空隙**。  
- **适用的题型**  
  1. “能否用若干条直线把平面划分成若干不相交区域” 类似题（如 “切割木块”）。  
  2. “检查是否存在两条不相交的分割线” 的区间版（如 “Maximum Number of Non‑Overlapping Intervals”）。  
  3. “把一维线段划分成若干段，每段必须完整包含若干区间” 的问题（如 “Partition Labels”）。  
- **一句话总结**：**把二维切割降维成一维区间，找足够的空隙即可**。

---

## 反思  

- **第一反应**：直接枚举所有可能的切线位置，逐个检查矩形是否跨过——这看起来最直观，却忽视了 `n` 可能非常大。  
- **最容易踩的坑**  
  1. **坐标范围**：`n` 可达 `10⁹`，不能把每个坐标都遍历一遍。  
  2. **区间端点的闭合方式**：切线不能恰好落在矩形的边界上（因为题目说“切线不能穿过矩形”，但可以贴着边界），这里采用左闭右开的投影表示最安全。  
  3. **空隙必须有正宽度**：`cur_max == l` 时只是两区间相邻，不能作为切线。  
- **下次遇到同类题**：第一步先 **把几何约束投影到一维**，看能否通过**排序+扫描**快速得到“空隙/分割点”。这样既避免大规模枚举，又能得到最优复杂度。