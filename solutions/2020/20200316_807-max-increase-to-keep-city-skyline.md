# #807. 最大增高以保持城市天际线 / Max Increase to Keep City Skyline

> 难度：中等 · 标签：Array、Greedy、Matrix · [LeetCode 链接](https://leetcode.com/problems/max-increase-to-keep-city-skyline/)

---

## 题目（英文原版）

**Description**

There is a city composed of n x n blocks, where each block contains a single building shaped like a vertical square prism. You are given a 0-indexed n x n integer matrix grid where grid[r][c] represents the height of the building located in the block at row r and column c.
A city's skyline is the outer contour formed by all the building when viewing the side of the city from a distance. The skyline from each cardinal direction north, east, south, and west may be different.
We are allowed to increase the height of any number of buildings by any amount (the amount can be different per building). The height of a 0-height building can also be increased. However, increasing the height of a building should not affect the city's skyline from any cardinal direction.
Return the maximum total sum that the height of the buildings can be increased by without changing the city's skyline from any cardinal direction.

**Examples**

**Example 1:**

```
Input: grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]
Output: 35
Explanation: The building heights are shown in the center of the above image.
The skylines when viewed from each cardinal direction are drawn in red.
The grid after increasing the height of buildings without affecting skylines is:
gridNew = [ [8, 4, 8, 7],
            [7, 4, 7, 7],
            [9, 4, 8, 7],
            [3, 3, 3, 3] ]
```

**Example 2:**

```
Input: grid = [[0,0,0],[0,0,0],[0,0,0]]
Output: 0
Explanation: Increasing the height of any building will result in the skyline changing.
```

**Constraints**

- n == grid.length
- n == grid[r].length
- 2 <= n <= 50
- 0 <= grid[r][c] <= 100

---

## 题目（中文翻译）

给定一个由 `n × n` 块组成的城市，每块对应一座竖直的正方体建筑。你得到一个 **0 索引** 的 `n × n` 整数矩阵 `grid`，其中 `grid[r][c]` 表示位于第 `r` 行第 `c` 列的建筑高度。

城市的 **天际线**（skyline）是从远处侧面观察城市时，所有建筑形成的外部轮廓。四个基准方向——北、东、南、西——各自的天际线可能不同。

我们可以对任意数量的建筑增加任意高度（每座建筑增加的高度可以不同），包括原本高度为 `0` 的建筑。但增加高度后 **不能改变** 任意基准方向的天际线。

返回在不改变任何方向天际线的前提下，建筑高度总共能够增加的 **最大和**。

---

### 示例 1

**输入**

```text
grid = [[3,0,8,4],
        [2,4,5,7],
        [9,2,6,3],
        [0,3,1,0]]
```

**输出**

```
35
```

**解释**  
图中中心展示了原始的建筑高度。四个方向的天际线用红色描绘。  
在不影响天际线的前提下，增高后的矩阵为：

```text
gridNew = [[8,4,8,7],
           [7,4,7,7],
           [9,4,8,7],
           [3,3,3,3]]
```

---

### 示例 2

**输入**

```text
grid = [[0,0,0],
        [0,0,0],
        [0,0,0]]
```

**输出**

```
0
```

**解释**  
对任意建筑增加高度都会改变天际线，因此最大增高和为 `0`。

---

### 约束条件

- `n == grid.length`
- `n == grid[r].length`
- `2 ≤ n ≤ 50`
- `0 ≤ grid[r][c] ≤ 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的要求是：**在不改变城市四个方向（北、东、南、西）的天际线的前提下，把建筑物的高度尽可能往上调**，求所有调高的总和的最大值。

先把问题拆成最直接的想法：

1. **先算出四个方向的天际线**  
   - 从**北**看（即从上往下看），每一列的最高建筑决定了北向天际线。  
   - 从**西**看（即从左往右看），每一行的最高建筑决定了西向天际线。  
   - **东**向天际线其实和西向相同，只是顺序相反，数值不变。  
   - **南**向天际线和北向相同，只是顺序相反，数值不变。  

   用数组 `row_max[i]` 保存第 `i` 行的最高楼，用 `col_max[j]` 保存第 `j` 列的最高楼。  
   这里的数组可以类比成 **字典**（哈希表）——我们把“行号/列号”当作 **key**，最高高度当作 **value**，随时可以“查字典”得到对应的最高值。

2. **对每一栋建筑，计算它能增加的最大高度**  
   - 这栋建筑所在的行最高值 `row_max[i]` 决定了**从西/东方向**它最多能有多高。  
   - 所在的列最高值 `col_max[j]` 决定了**从北/南方向**它最多能有多高。  
   - 为了不破坏任意方向的天际线，这两个限制中**更小的那个**才是安全的上限。  

   所以，**可以把这栋建筑调到的最高高度** = `min(row_max[i], col_max[j])`。  
   已有的高度是 `grid[i][j]`，因此**本次可以增加的高度** = `min(row_max[i], col_max[j]) - grid[i][j]`（如果是负数就说明已经达到了上限，取 0）。

3. **把所有建筑的可增加量相加**，得到答案。

> 这就是最直接、最“笨拙”的办法：先把所有限制算出来，然后逐个检查、累计。

#### 代码（Python）

```python
from typing import List

def maxIncreaseKeepingSkyline(grid: List[List[int]]) -> int:
    n = len(grid)                     # n 行 n 列，n ≤ 50，完全可以遍历

    # 1️⃣ 计算每行、每列的最高楼（相当于查字典）
    row_max = [max(row) for row in grid]                # 行最大值列表
    col_max = [max(grid[i][j] for i in range(n)) for j in range(n)]  # 列最大值列表

    # 2️⃣ 累加每栋建筑可以增加的高度
    total_increase = 0
    for i in range(n):
        for j in range(n):
            # 该位置能达到的最高高度 = 行最高 与 列最高 中的较小值
            allowed_height = min(row_max[i], col_max[j])
            # 实际可以增加的量（若已达上限则为 0）
            increase = allowed_height - grid[i][j]
            if increase > 0:
                total_increase += increase

    return total_increase
```

#### 复杂度

- **时间复杂度：O(n²)**  
  - 解释：我们遍历了 `n` 行 `n` 列两次（一次算行/列最大值，一次累计增加量），总共是 `n × n` 次基本操作。  
  - 对于 `n = 50`，最多只是 2500 次循环，几乎可以忽略不计。

- **空间复杂度：O(n)**  
  - 解释：我们额外用了两个长度为 `n` 的列表 `row_max`、`col_max` 来存行列最大值，和原始矩阵无关，只占用线性空间。

---

### 2. 最优解

#### 思路  

在上面的**暴力解**中，已经是最简洁的做法了。  
所谓“最优”，指的是**在时间和空间上都做到最好的**。  
这里的关键点是：

1. **瓶颈在哪里？**  
   - 暴力解已经是 O(n²) 的遍历，没有多余的嵌套循环或指数级搜索。  
   - 由于输入本身是一个 `n × n` 的矩阵，任何解法都必须至少读取所有元素一次，即 **Ω(n²)**（下界）时间是不可避免的。  

2. **有没有可以进一步压缩空间的余地？**  
   - 我们使用了两组 `row_max`、`col_max`，各占 O(n) 空间。  
   - 其实我们可以在一次遍历中 **同步计算行最大值和列最大值**，再在第二次遍历中直接使用，这样仍是 O(n) 空间，已经是最小可能（除非直接在原矩阵上修改，但那会破坏原始数据，阅读性下降）。  

因此，**最优解**就在于**明确两次遍历的意义**，并且用 **简洁的 Python 表达式** 把步骤写得更直观。

下面给出稍作优化的实现：

- 第一次遍历：一次性得到 `row_max` 与 `col_max`（利用 `zip(*grid)` 把列转成行，省去手写双层循环）。
- 第二次遍历：直接累计增加量。

#### 代码（Python）

```python
from typing import List

def maxIncreaseKeepingSkyline(grid: List[List[int]]) -> int:
    # 1️⃣ 一次性算出行最大值和列最大值
    row_max = [max(row) for row in grid]          # 每行最高
    col_max = [max(col) for col in zip(*grid)]    # 每列最高，zip(*grid) 把列“转置”为行

    # 2️⃣ 累加所有建筑可以提升的高度
    total = 0
    for i, row in enumerate(grid):
        for j, height in enumerate(row):
            # 该位置的安全上限 = 行最高 与 列最高 中的较小者
            total += min(row_max[i], col_max[j]) - height

    return total
```

> **关键点解释**  
> - `zip(*grid)`：把矩阵的列“打包”成元组序列，等价于转置矩阵，方便一次性求列最大值。可以把它想象成“把每列的建筑排成一排”，再找最高的那栋。  
> - `enumerate`：在遍历时同时得到下标 `i、j`，对应行号和列号，省去手写计数器。

#### 复杂度

- **时间复杂度：O(n²)**  
  - 仍然需要遍历整个矩阵两遍（一次算最大值，一次累计），这已经是理论下界，无法再快。

- **空间复杂度：O(n)**  
  - 只存了两条长度为 `n` 的列表 `row_max`、`col_max`，已经是最小可能的额外空间。

---

## 心得

- **核心技巧**：**利用行/列的最大值构造约束**，再对每个单元格取 `min(row_max, col_max)`。本质上是**取交集的上限**，保证四个方向的天际线不变。  
- **适用的题型**  
  1. **矩阵约束类**：如 “矩阵中的最大值保持不变的增量” 类题目。  
  2. **行/列独立约束**：比如 “使每行每列的和相等的最小增量” 之类的问题。  
  3. **不改变极值的修改**：如 “在不改变数组最大值的前提下增大元素”。  
- **一句话总结**：**“行列最高限定，取最小上限，累加差值”。**

---

## 反思

- **第一反应**：看到“天际线不变”，马上想到“每行/列的最高建筑是天际线的关键”。于是就想到先算行最高、列最高，再限制每个位置的高度。  
- **最容易踩的坑**  
  1. **忘记取最小值**：只用行最高或列最高会导致某方向的天际线被抬高。  
  2. **负数增量**：`min(row_max, col_max) - grid[i][j]` 可能为负，直接相加会导致答案错误（应该视作 0）。在实现时使用 `max(0, ...)` 或直接相信 `min` 永远 ≥ 原值（因为原值本身 ≤ 行/列最大值）。  
  3. **边界情况**：全零矩阵或全部已经是行/列最大值的矩阵，增量应为 0。代码要能正确返回 0。  
- **下次遇到同类题**：第一步想到 **“先把每个约束的极值算出来”，再 **“对每个元素取所有约束的最小上限”。** 这一步几乎是通用的思考模板。