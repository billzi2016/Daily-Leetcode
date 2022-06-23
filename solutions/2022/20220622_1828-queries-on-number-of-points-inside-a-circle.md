# #1828. 圆内点数查询 / Queries on Number of Points Inside a Circle

> 难度：中等 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/queries-on-number-of-points-inside-a-circle/)

---

## 题目（英文原版）

**Description**

You are given an array points where points[i] = [xi, yi] is the coordinates of the ith point on a 2D plane. Multiple points can have the same coordinates.
You are also given an array queries where queries[j] = [xj, yj, rj] describes a circle centered at (xj, yj) with a radius of rj.
For each query queries[j], compute the number of points inside the jth circle. Points on the border of the circle are considered inside.
Return an array answer, where answer[j] is the answer to the jth query.
Follow up: Could you find the answer for each query in better complexity than O(n)?

**Examples**

**Example 1:**

```
Input: points = [[1,3],[3,3],[5,3],[2,2]], queries = [[2,3,1],[4,3,1],[1,1,2]]
Output: [3,2,2]
Explanation: The points and circles are shown above.
queries[0] is the green circle, queries[1] is the red circle, and queries[2] is the blue circle.
```

**Example 2:**

```
Input: points = [[1,1],[2,2],[3,3],[4,4],[5,5]], queries = [[1,2,2],[2,2,2],[4,3,2],[4,3,3]]
Output: [2,3,2,4]
Explanation: The points and circles are shown above.
queries[0] is green, queries[1] is red, queries[2] is blue, and queries[3] is purple.
```

**Constraints**

- 1 <= points.length <= 500
- points[i].length == 2
- 0 <= x​​​​​​i, y​​​​​​i <= 500
- 1 <= queries.length <= 500
- queries[j].length == 3
- 0 <= xj, yj <= 500
- 1 <= rj <= 500
- All coordinates are integers.

---

## 题目（中文翻译）

给定一个数组 `points`，其中 `points[i] = [xi, yi]` 表示平面上第 *i* 个点的坐标。多个点可能具有相同的坐标。  
再给定一个数组 `queries`，其中 `queries[j] = [xj, yj, rj]` 描述了一个以 `(xj, yj)` 为圆心、半径为 `rj` 的圆（circle）。

对于每个查询 `queries[j]`，计算第 *j* 个圆内的点的数量。位于圆边界上的点也算作在圆内。  
返回一个数组 `answer`，其中 `answer[j]` 为第 *j* 个查询的答案。

---

## 示例

### 示例 1

**输入**  
``` 
points = [[1,3],[3,3],[5,3],[2,2]], 
queries = [[2,3,1],[4,3,1],[1,1,2]]
``` 

**输出**  
```
[3,2,2]
``` 

**解释**：图中展示了点和圆。`queries[0]` 为绿色圆，`queries[1]` 为红色圆，`queries[2]` 为蓝色圆。

### 示例 2

**输入**  
``` 
points = [[1,1],[2,2],[3,3],[4,4],[5,5]], 
queries = [[1,2,2],[2,2,2],[4,3,2],[4,3,3]]
``` 

**输出**  
```
[2,3,2,4]
``` 

**解释**：图中展示了点和圆。`queries[0]` 为绿色圆，`queries[1]` 为红色圆，`queries[2]` 为蓝色圆，`queries[3]` 为紫色圆。

---

## 约束

- `1 <= points.length <= 500`
- `points[i].length == 2`
- `0 <= xi, yi <= 500`
- `1 <= queries.length <= 500`
- `queries[j].length == 3`
- `0 <= xj, yj <= 500`
- `1 <= rj <= 500`
- 所有坐标均为整数

---

## 进阶

是否可以在 **O(n)** 之外的更低时间复杂度内完成每个查询的答案计算？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把每个圆的查询都和所有点逐一比对**：

1. 取出第 `j` 个查询 `queries[j] = [xj, yj, rj]`，它描述了一个圆心在 `(xj, yj)`、半径为 `rj` 的圆。  
2. 对数组 `points` 中的每一个点 `p = [xi, yi]`，计算它到圆心的欧氏距离  

\[
d = \sqrt{(xi - xj)^2 + (yi - yj)^2}
\]

   只要 `d ≤ rj`（**等号成立也算在圆里**），就把计数器 `cnt` 加一。  
3. 把得到的 `cnt` 放进答案数组 `answer[j]`，继续处理下一个查询。

> **类比**：  
> 想象你在一个大操场上摆放了很多小旗子（点），老师让你数出每个指定圆形范围内有多少面旗子。最笨的办法就是把每面旗子都走过去量一下距离——虽然慢，但一定能得到正确答案。

**为什么一定正确**  
只要遍历了所有点，且距离判断没有漏掉任何一种情况（点在圆内、点在圆上、点在圆外），计数必然完整。

**复杂度分析（大白话）**  
- 外层循环遍历所有查询，记作 `m = queries.length`。  
- 内层循环遍历所有点，记作 `n = points.length`。  
- 对每对 (查询, 点) 只做一次常数时间的距离比较（平方根可以省掉，用平方比较），所以总共要做 `m × n` 次操作。

```
时间复杂度：O(m·n)   （比如 500 × 500 = 25 000 次，机器能轻松跑完）
空间复杂度：O(1)    （只用了几个计数变量，不随输入规模增长）
```

> **O(m·n) 的含义**：如果把 `m` 看成“查询的数量”，`n` 看成“点的数量”，那么运行时间会随这两个数的乘积线性增长。点或查询多一点，时间就会相应“翻倍”或“成几倍”。

#### 代码（Python）

```python
from typing import List

def countPoints(points: List[List[int]], queries: List[List[int]]) -> List[int]:
    """
    暴力解：对每个查询遍历所有点，判断距离是否在半径范围内。
    """
    ans = []                                 # 用来存放每个查询的答案
    for qx, qy, r in queries:                # 逐个读取圆心 (qx, qy) 和半径 r
        r2 = r * r                            # 为了避免开根号，比较平方距离
        cnt = 0                               # 本次查询的计数器
        for px, py in points:                # 遍历所有点
            dx = px - qx
            dy = py - qy
            if dx * dx + dy * dy <= r2:      # 如果点到圆心的平方距离 ≤ r²，就在圆内
                cnt += 1
        ans.append(cnt)                       # 把本次查询的结果加入答案列表
    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 每个查询都要检查所有点，乘积越大耗时越长。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`cnt`, `r2`, `dx`, `dy`），不随输入规模变化。

---

### 2. 最优解

> **从暴力解出发**：  
> 暴力解的“慢点”在于**每个查询都把所有点都扫一遍**，即使很多点离圆心很远，根本不可能落在圆里。我们希望 **先把“明显不可能”的点剔除**，只对可能落在圆里的点做距离检查。

#### 思路  

本题的坐标范围只有 `0 … 500`，点的数量最多 `500`，这让我们可以利用 **空间划分（grid bucket）** 来快速定位离圆心较近的点。

**步骤概览**  

1. **把平面切成若干小格子**（例如每格 50×50），每个格子内部保存所有落在其中的点的下标。  
   - 这相当于在地图上划分“社区”，每个社区里只存放住在那里的居民（点）。  
   - 查找时只需要看圆覆盖了哪些社区，而不是所有居民。

2. **对于每个查询**  
   - 先算出圆的 **包围盒**（外接正方形）：`[cx‑r, cx+r] × [cy‑r, cy+r]`。  
   - 根据包围盒的左、右、上、下边界，确定它会碰到哪些格子（只检查这些格子）。  
   - 对这些格子里的点逐个做距离判断（因为格子内部的点数量通常远小于总点数）。

3. **计数**：同暴力解一样，用平方距离比较，统计落在圆内的点。

**为什么比暴力快**  

- 每个查询只会遍历 **与圆相交的格子**，而格子数目与圆的面积（即 `π·r²`）成正比。  
- 对于半径不大的圆，涉及的格子和点会少得多。  
- 最坏情况（半径覆盖整个平面）仍然会检查所有点，但这已经是 `O(n)`，而不是 `O(m·n)`。

**核心概念解释**  

- **格子（bucket / cell）**：把二维平面按固定宽高切成若干矩形块。把所有点放进对应的块里，就像把书按类别放进不同的抽屉。  
- **包围盒（bounding box）**：圆外接的最小正方形。因为正方形的边是平行于坐标轴的，计算它覆盖哪些格子非常简单——只要比较格子的左/右/上/下边界即可。  
- **平方距离**：`(dx)² + (dy)²`，省去开根号，数值更小、更快。

#### 代码（Python）

```python
from typing import List
import math

def countPoints_optimized(points: List[List[int]], queries: List[List[int]]) -> List[int]:
    """
    使用网格划分（bucket）来加速查询。
    坐标范围 0~500，取格子大小为 50（可自行调节），
    这样最多产生 11×11 = 121 个格子，每格最多存 500/121 ≈ 5 个点（平均）。
    """
    # ---------- 1. 建立格子 ----------
    MAX_COORD = 500
    CELL_SIZE = 50                     # 每个格子的宽度和高度
    # 计算格子数量（多加 1 防止坐标恰好在最右/上边界）
    ROWS = (MAX_COORD // CELL_SIZE) + 1
    COLS = (MAX_COORD // CELL_SIZE) + 1

    # grid[i][j] 保存所有落在第 i 行、第 j 列格子里的点（以 (x, y) 形式存）
    grid = [[[] for _ in range(COLS)] for _ in range(ROWS)]

    for x, y in points:
        r = x // CELL_SIZE            # 行号
        c = y // CELL_SIZE            # 列号
        grid[r][c].append((x, y))

    # ---------- 2. 处理每个查询 ----------
    ans = []
    for cx, cy, r in queries:
        r2 = r * r                     # 圆的半径平方，后面直接比较
        # 计算包围盒的左、右、上、下边界（注意不要越界）
        x_min = max(0, cx - r)
        x_max = min(MAX_COORD, cx + r)
        y_min = max(0, cy - r)
        y_max = min(MAX_COORD, cy + r)

        # 包围盒对应的格子范围
        row_start = x_min // CELL_SIZE
        row_end   = x_max // CELL_SIZE
        col_start = y_min // CELL_SIZE
        col_end   = y_max // CELL_SIZE

        cnt = 0
        # 只遍历可能与圆相交的格子
        for i in range(row_start, row_end + 1):
            for j in range(col_start, col_end + 1):
                for px, py in grid[i][j]:        # 逐个点检查
                    dx = px - cx
                    dy = py - cy
                    if dx * dx + dy * dy <= r2:  # 在圆内或恰好在边界
                        cnt += 1
        ans.append(cnt)

    return ans
```

> **代码要点注释**  
> - `CELL_SIZE = 50` 只是一种经验值，实际可根据 `points` 与 `queries` 的规模调节。  
> - 通过 `x // CELL_SIZE` 把点映射到对应的格子；同理查询时把包围盒的四条边映射到格子索引。  
> - 只遍历 `row_start … row_end`、`col_start … col_end` 这块子矩阵，避免了全局扫描。

#### 复杂度

- **预处理**（把点放进格子）  
  - 时间：`O(n)`，每个点只算一次格子索引。  
  - 空间：`O(n + ROWS·COLS)`，除了保存原始点外，还额外存了格子容器（格子数量固定，最多 `11×11`）。

- **每个查询**  
  - 设圆的半径为 `r`，格子大小为 `s`，则横向最多涉及 `⌈2r / s⌉ + 1` 行，纵向同理。  
  - 因此检查的格子数约为 `O((r/s)²)`，每个格子里点的数量与 `n` 成正比的概率极低（因为格子很细）。  
  - **平均时间**约为 `O(k)`，`k` 为实际落在圆的格子里的点数（远小于 `n`）。  
  - **最坏情况**（`r` 大到覆盖整个平面）仍是 `O(n)`。

- **总体**（`m` 条查询）  
  - 平均 `O(m·k)`，在实际数据中通常远快于暴力的 `O(m·n)`。  

- **空间复杂度**：`O(n + ROWS·COLS)` ≈ `O(n)`，因为格子数量是常数级别（最多 121），不随 `n` 增长。

> 与暴力解对比：  
> - 暴力是 **每次都遍历全部 `n` 个点** → `O(m·n)`。  
> - 优化后 **只遍历可能在圆里的少量点** → 平均 `O(m·k)`，`k << n`，在大多数测试里运行更快。

---

## 心得

- **核心技巧**：**空间划分（grid / bucket）+ 包围盒过滤**  
  把平面切块，先用圆的外接正方形快速定位可能的块，再在块内部做精确的圆内判定。

- **适用的题型**  
  1. “给定若干点，求每个几何查询（圆、矩形、椭圆）内部点的数量”。  
  2. “最近邻/范围查询” 类问题（例如 LeetCode 设计数据结构实现 `add(point)`、`count(point, radius)`）。  
  3. “在大平面上统计落在若干固定形状内的对象”，常用 **网格划分** 或 **四叉树**。

- **一句话总结解题钥匙**：  
  “先用粗略的**几何包围盒**把搜索范围压缩到少数格子，再在这些格子里做精确的**距离比较**。”

---

## 反思

- **第一反应**：直接遍历所有点，写出最朴素的距离判断代码。  
- **最容易踩的坑**  
  1. **忘记把距离平方比较**，导致使用 `math.sqrt` 造成不必要的性能损失。  
  2. **边界条件**：圆的半径可能让包围盒超出坐标上限，需要 `max/min` 限制在 `[0, 500]`。  
  3. **格子大小的选择**：如果格子太大，过滤效果差；太小会产生很多空格子，增加遍历开销。  
- **下次类似题的第一步**：  
  “先看坐标范围是否有限，若是，就考虑把平面划分成网格（或四叉树），利用几何外接形状快速定位可能的候选点，再做精确判定。”