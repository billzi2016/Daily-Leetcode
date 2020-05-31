# #883. **三维形体的投影面积** / Projection Area of 3D Shapes

> 难度：简单 · 标签：Array、Math、Geometry、Matrix · [LeetCode 链接](https://leetcode.com/problems/projection-area-of-3d-shapes/)

---

## 题目（英文原版）

**Description**

You are given an n x n grid where we place some 1 x 1 x 1 cubes that are axis-aligned with the x, y, and z axes.
Each value v = grid[i][j] represents a tower of v cubes placed on top of the cell (i, j).
We view the projection of these cubes onto the xy, yz, and zx planes.
A projection is like a shadow, that maps our 3-dimensional figure to a 2-dimensional plane. We are viewing the "shadow" when looking at the cubes from the top, the front, and the side.
Return the total area of all three projections.

**Examples**

**Example 1:**

```
Input: grid = [[1,2],[3,4]]
Output: 17
Explanation: Here are the three projections ("shadows") of the shape made with each axis-aligned plane.
```

**Example 2:**

```
Input: grid = [[2]]
Output: 5
```

**Example 3:**

```
Input: grid = [[1,0],[0,2]]
Output: 8
```

**Constraints**

- n == grid.length == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] <= 50

---

## 题目（中文翻译）

给定一个 `n × n` 的网格（grid），在网格的每个单元格上放置若干个 `1 × 1 × 1` 的立方体，这些立方体与坐标轴 `x`、`y`、`z` 对齐（axis‑aligned）。  
网格中的每个数值 `v = grid[i][j]` 表示在单元格 `(i, j)` 上堆叠的高度为 `v` 的立方体塔（tower）。

我们观察这些立方体在 **xy 平面**、**yz 平面** 和 **zx 平面** 上的 **投影（projection）**。投影类似于阴影（shadow），它把三维图形映射到二维平面。当从顶部、正面和侧面观察立方体时，看到的就是这些投影。

返回三个投影的面积总和。

---

### 示例

**示例 1**

```text
Input: grid = [[1,2],[3,4]]
Output: 17
Explanation: 下面展示了该形体在每个坐标轴对齐平面上的三个投影（“阴影”）。
```

**示例 2**

```text
Input: grid = [[2]]
Output: 5
```

**示例 3**

```text
Input: grid = [[1,0],[0,2]]
Output: 8
```

---

### 约束条件

- `n == grid.length == grid[i].length`
- `1 <= n <= 50`
- `0 <= grid[i][j] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一块立方体** 都拆出来，逐个判断它在三个方向上（上、前、侧）有没有被“遮挡”。  
- **上视图（xy 平面）**：只要格子里有立方体，这个格子在俯视时一定会出现一个 1×1 的方块（像在地图上画一个点）。
- **前视图（yz 平面）**：从前面往看，某一列（固定 `j`）里最高的那堆立方体会露出它的最前面。低于最高的那堆会被前面的立方体挡住，像排队时后面的人被前面的人遮住了视线。
- **侧视图（zx 平面）**：从侧面往看，某一行（固定 `i`）里最高的那堆立方体会露出它的最左面，同理。

如果我们把每个立方体都拆开来看，**每块立方体** 会贡献：

| 面向 | 是否计入投影面积 |
|------|-----------------|
| 上   | 只要立方体在最上层（即 `grid[i][j] > 0`）就计 1 |
| 前   | 当它是所在列 `j` 中最高的那层（`k == max_{i} grid[i][j]`）时计 1 |
| 侧   | 当它是所在行 `i` 中最高的那层（`k == max_{j} grid[i][j]`）时计 1 |

把所有立方体的贡献加起来，就是三个投影的总面积。

> **类比**：想象你在玩积木，每块积木都可能在三个方向上投下影子。我们把所有积木都搬出来，逐块检查哪一面能看到影子，然后把这些影子面积相加。

这种做法虽然概念最清晰，但实际上要遍历 **每个立方体**，时间会随立方体数量（最高 50×50×50 = 125 000）而增长。对于本题的约束，这仍然能跑完，但不是最优的。

#### 代码（Python）

```python
def projectionArea(grid):
    n = len(grid)                # 网格的行数（也是列数）
    total = 0                    # 最终答案

    # ---------- 上视图 ----------
    # 只要格子里有立方体，就会在俯视图出现一个正方形
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:   # 这里相当于“有东西在这儿”
                total += 1

    # ---------- 前视图 ----------
    # 对每一列 j，找出最高的塔高
    for j in range(n):
        col_max = 0
        for i in range(n):
            col_max = max(col_max, grid[i][j])
        total += col_max          # 最高的那块立方体正面可见

    # ---------- 侧视图 ----------
    # 对每一行 i，找出最高的塔高
    for i in range(n):
        row_max = max(grid[i])    # Python 自带的行最大值
        total += row_max

    return total
```

> **关键行中文注释** 已在代码中给出，帮助你一步步跟踪思路。

#### 复杂度

- **时间复杂度**：`O(n³)`（最坏情况下遍历每个立方体）。  
  这里的 `n³` 可以想象成“立方体的体积”。因为我们把每块小立方体都看了一遍。
- **空间复杂度**：`O(1)`，只用了常数级的额外变量（`total、col_max、row_max`），不随输入大小增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正需要遍历的不是每块小立方体，而是每个格子**（即每个塔的高度）。  
- **上视图**：只要格子里有立方体，就计 1。遍历一次网格即可得到答案。  
- **前视图**：每一列 `j` 只需要知道该列的 **最大高度**，因为最高的那块立方体的前面会投下影子。  
- **侧视图**：每一行 `i` 同理，只需要该行的 **最大高度**。

于是只要 **一次遍历**（或两次遍历）网格，就能同时得到：

- 上视图的面积 `top = Σ (grid[i][j] > 0)`
- 前视图的面积 `front = Σ max_{i} grid[i][j]`（对每列求最大值）
- 侧视图的面积 `side = Σ max_{j} grid[i][j]`（对每行求最大值）

把这三部分相加即为答案。

> **类比**：把每列看成一排楼房，站在街道上只能看到最高的那栋楼的正面；把每行看成一排楼房，站在侧面只能看到最高的那栋楼的侧面。我们不必数每层楼，只要记住每排的最高层即可。

#### 代码（Python）

```python
def projectionArea(grid):
    n = len(grid)
    top = 0                     # 上视图面积
    front = 0                   # 前视图面积（列最大值之和）
    side = 0                    # 侧视图面积（行最大值之和）

    # 同时遍历每一行，统计 top、side，并收集每列的最大值
    col_max = [0] * n           # col_max[j] 保存第 j 列的最高塔

    for i in range(n):
        row_max = 0             # 本行的最高塔（用于 side）
        for j in range(n):
            h = grid[i][j]
            if h > 0:
                top += 1       # 只要有立方体，上视图加一

            row_max = max(row_max, h)   # 行最大值
            col_max[j] = max(col_max[j], h)  # 列最大值

        side += row_max          # 行最大值计入侧视图

    front = sum(col_max)        # 列最大值之和计入前视图
    return top + front + side
```

> 代码里每一行都有中文注释，帮助你把 **“遍历一次”** 的思路对应到具体实现。

#### 复杂度

- **时间复杂度**：`O(n²)`。只遍历了 `n × n` 个格子一次（`n ≤ 50`），相当于“看整个棋盘的每个格子”。这比暴力的 `O(n³)` 快了一个量级。
- **空间复杂度**：`O(n)`，需要一个长度为 `n` 的数组 `col_max` 来存每列的最大值。相较于输入规模，这只是线性额外空间。

---

## 心得

- **核心技巧**：把三维投影问题拆解为**行最大值**、**列最大值**和**是否有立方体**的计数。  
- **适用的题型**  
  1. “矩阵的行/列最大值之和”类题（如 LeetCode 1977 *Number of Ways to Separate Numbers* 的行列统计思路）。  
  2. “从不同方向观察二维/三维结构的可见面积”类题（如 892 *Surface Area of 3D Shapes*）。  
- **一句话总结**：**只要把每行、每列的最高层记下来，投影面积就能一次算完**。

---

## 反思

- **第一反应**：看到“投影”“阴影”会想到把每个小立方体都拆出来，逐块判断可见性——这就是暴力思路。  
- **最容易踩的坑**  
  - 忘记 **上视图** 只需要判断是否大于 0，而不是高度本身。  
  - 对 **前视图/侧视图** 用错了方向：列对应前视图，行对应侧视图，容易写反。  
  - 边界情况：全零矩阵时，上视图为 0，行/列最大值也都为 0，答案应为 0。  
- **下次类似题**：第一步先思考“从某个方向看，哪些格子会被遮挡”。如果只需要最高的那一层，就转化为 **行/列最大值** 的统计问题。这样可以立刻把复杂度降到 `O(n²)`。