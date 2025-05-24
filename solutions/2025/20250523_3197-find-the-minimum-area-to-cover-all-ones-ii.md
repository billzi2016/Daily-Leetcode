# #3197. 覆盖所有 1 的最小面积 II / Find the Minimum Area to Cover All Ones II

> 难度：困难 · 标签：Array、Matrix、Enumeration · [LeetCode 链接](https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/)

---

## 题目（英文原版）

**Description**

You are given a 2D binary array grid. You need to find 3 non-overlapping rectangles having non-zero areas with horizontal and vertical sides such that all the 1's in grid lie inside these rectangles.
Return the minimum possible sum of the area of these rectangles.
Note that the rectangles are allowed to touch.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,1],[1,1,1]]
Output: 5
Explanation:
```

**Example 2:**

```
Input: grid = [[1,0,1,0],[0,1,0,1]]
Output: 5
Explanation:
```

**Constraints**

- 1 <= grid.length, grid[i].length <= 30
- grid[i][j] is either 0 or 1.
- The input is generated such that there are at least three 1's in grid.

---

## 题目（中文翻译）

给定一个二维二进制数组 `grid`。你需要找到 **3** 个相互不重叠、面积非零且边平行于坐标轴的矩形（rectangle），使得 `grid` 中所有的 `1` 都位于这些矩形内部。返回这些矩形面积之和的最小可能值。注意，矩形之间可以相互接触。

示例 1:
```
Input: grid = [[1,0,1],[1,1,1]]
Output: 5
Explanation:
```

示例 2:
```
Input: grid = [[1,0,1,0],[0,1,0,1]]
Output: 5
Explanation:
```

约束条件：
- `1 <= grid.length, grid[i].length <= 30`
- `grid[i][j]` 仅为 `0` 或 `1`
- 输入保证 `grid` 中至少存在三个 `1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有 1 的位置枚举出来，然后穷举三条不相交的矩形**，检查它们是否把所有的 1 包含进去，最后取面积最小的一组。  

- **数据结构**：我们可以把每个矩形用四个整数 `(r1, c1, r2, c2)` 表示，分别是左上角和右下角的行、列下标。  
  - 这有点像在地图上画一个 **矩形框**，左上角是框的左上角，右下角是框的右下角。  
- **为什么正确**：只要枚举到所有可能的三条矩形组合，必然会出现最优解（因为它本身就是一种组合）。  
- **复杂度分析**：  
  - 设网格大小为 `m × n ( ≤ 30 )`。  
  - 单条矩形的左上角有 `m·n` 种可能，右下角也有 `m·n` 种可能（但必须在左上右下的右下方），所以一条矩形大约有 `O(m² n²)` 种。  
  - 三条矩形的组合就是 `O((m² n²)³) = O(m⁶ n⁶)`，这在最坏情况下相当于 `30¹² ≈ 5.3×10¹⁷` 次枚举，根本不可算。  
  - 空间上只需要保存几条矩形的坐标，几乎为 `O(1)`。  

> **大白话**：  
> `O(m² n²)` 可以理解为“把每一格都当成左上角，再把每一格当成右下角”，相当于把整个棋盘的每一对角落都挑出来。  
> 当我们再把这种“挑角落”操作做三次，就像在找三块拼图的所有可能摆法，数量会爆炸到天文数字。

#### 代码（Python）

```python
# 这段代码仅用于说明暴力思路，实际运行会超时
def minArea_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    ones = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]

    best = float('inf')
    # 枚举第一条矩形
    for r1 in range(m):
        for c1 in range(n):
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    rect1 = (r1, c1, r2, c2)
                    # 枚举第二条矩形（与第一条不相交）
                    for r1b in range(m):
                        for c1b in range(n):
                            for r2b in range(r1b, m):
                                for c2b in range(c1b, n):
                                    if not disjoint(rect1, (r1b, c1b, r2b, c2b)):
                                        continue
                                    rect2 = (r1b, c1b, r2b, c2b)
                                    # 枚举第三条矩形（与前两条均不相交）
                                    for r1c in range(m):
                                        for c1c in range(n):
                                            for r2c in range(r1c, m):
                                                for c2c in range(c1c, n):
                                                    rect3 = (r1c, c1c, r2c, c2c)
                                                    if (disjoint(rect1, rect3) and
                                                        disjoint(rect2, rect3)):
                                                        if covers_all([rect1, rect2, rect3], ones):
                                                            area = area_rect(rect1) + \
                                                                   area_rect(rect2) + \
                                                                   area_rect(rect3)
                                                            best = min(best, area)
    return best
```

> **注意**：上述代码只是演示思路，`disjoint` 用来判断两矩形是否相交，`covers_all` 用来判断所有的 `1` 是否都在这三条矩形内部。实际提交必然 TLE。

#### 复杂度  

- **时间复杂度**：`O(m⁶ n⁶)`，在本题约等于 `5×10¹⁷` 次操作，根本不可接受。  
- **空间复杂度**：`O(1)`（只保存常数条矩形），但这并不能抵消时间上的灾难。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于 **“枚举三条矩形的所有组合”**。  
我们需要把搜索空间压缩到 **只枚举分割线**，因为**不相交且只能水平/垂直放置的矩形**，其相对位置只能通过几条直线来划分。

下面一步步推导：

1. **先考虑 1 条矩形**  
   - 对于任意子矩形区域 `[r1..r2] × [c1..c2]`，只要里面有 1，最小覆盖矩形就是这些 1 的外接矩形。  
   - 用四个变量记录子区域里 1 的最小行、最大行、最小列、最大列，面积 = `(maxR-minR+1)*(maxC-minC+1)`。  
   - 记作 `f1[r1][c1][r2][c2]`（**单矩形最小面积**）。

2. **再考虑 2 条矩形**  
   - 两条不相交矩形要么**水平切**（在某行 `split` 上把区域分成上下两块），要么**垂直切**（在某列 `split` 上把区域分成左右两块）。  
   - 因此 `f2`（**两矩形最小面积**）可以通过在子区域内部尝试所有可能的水平/垂直切分，取 `f1` 的和的最小值：  

     ```
     f2[region] = min(
         f1[top] + f1[bottom]   (对所有水平切分),
         f1[left] + f1[right]   (对所有垂直切分)
     )
     ```

3. **三条矩形的情况**  
   三条矩形的形状其实只有以下几种（允许矩形相邻但不能重叠）：

   - **三条水平带**：用两条水平切分线把整个网格切成三块。  
   - **三条垂直带**：用两条垂直切分线把整个网格切成三块。  
   - **先竖后横**：先用一条垂直切分线把网格划分为左、右两块，左块用 **1 条矩形** 覆盖，右块再用 **2 条矩形**（水平切分）覆盖。左/右角色可以互换。  
   - **先横后竖**：先用一条水平切分线把网格划分为上、下两块，上块 1 条矩形，下块 2 条矩形（垂直切分），同样可以互换。

   只要把上面四类情况全部枚举一次，就一定能得到最优解。

4. **预处理**  
   - 网格最大只有 `30 × 30`，子矩形的数量 `≈ (30·31/2)² ≈ 5×10⁴`，完全可以 **枚举所有子矩形** 并计算 `f1`、`f2`。  
   - 计算 `f1` 时直接遍历子矩形内部找 1 的外接框，最坏情况是 `5×10⁴ × 30×30 ≈ 4.5×10⁷` 次基本操作，足够快（几百毫秒）。  
   - 计算 `f2` 时，对每个子矩形尝试所有水平/垂直切分，切分次数至多 `30+30`，总复杂度约 `5×10⁴ × 60 ≈ 3×10⁶`，同样轻松。

5. **最终答案**  
   - 按照上面四类枚举方式，用已经算好的 `f1`、`f2` 直接求和，取最小值即为答案。

> **核心概念解释**  
> - **前缀和**：这里我们没有用到前缀和来统计 1 的个数，因为只需要判断“是否有 1”，直接遍历即可，代码更直观。  
> - **外接矩形**：想象把所有的 1 用橡皮筋拉紧，橡皮筋形成的最小矩形就是外接矩形。  
> - **切分线**：把棋盘想象成纸，画一条直线把纸剪开，左边/右边（或上面/下面）就是两个不相交的区域。

#### 代码（Python）

```python
from typing import List

INF = 10 ** 9

def minArea(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # --------------------------------------------------------------
    # 1. 计算 f1：任意子矩形里，用 1 条矩形覆盖的最小面积
    # --------------------------------------------------------------
    # f1[(r1,c1,r2,c2)] = 最小外接矩形面积，若子矩形里没有 1，则为 0
    f1 = {}
    for r1 in range(m):
        for c1 in range(n):
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    min_r, max_r = m, -1
                    min_c, max_c = n, -1
                    # 扫描子矩形，找出 1 的边界
                    for i in range(r1, r2 + 1):
                        for j in range(c1, c2 + 1):
                            if grid[i][j] == 1:
                                if i < min_r: min_r = i
                                if i > max_r: max_r = i
                                if j < min_c: min_c = j
                                if j > max_c: max_c = j
                    if max_r == -1:                     # 没有 1
                        area = 0
                    else:
                        area = (max_r - min_r + 1) * (max_c - min_c + 1)
                    f1[(r1, c1, r2, c2)] = area

    # --------------------------------------------------------------
    # 2. 计算 f2：任意子矩形里，用 2 条矩形覆盖的最小面积
    # --------------------------------------------------------------
    f2 = {}
    for r1 in range(m):
        for c1 in range(n):
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    best = INF
                    # 水平切分
                    for split in range(r1, r2):
                        top = f1[(r1, c1, split, c2)]
                        bottom = f1[(split + 1, c1, r2, c2)]
                        best = min(best, top + bottom)
                    # 垂直切分
                    for split in range(c1, c2):
                        left = f1[(r1, c1, r2, split)]
                        right = f1[(r1, split + 1, r2, c2)]
                        best = min(best, left + right)
                    # 若子矩形本身没有 1，则直接 0（两矩形也可以不出现）
                    if best == INF:
                        best = 0
                    f2[(r1, c1, r2, c2)] = best

    # --------------------------------------------------------------
    # 3. 枚举三条矩形的四种布局，求最小总面积
    # --------------------------------------------------------------
    ans = INF

    # 3.1 三条垂直带（两条竖向切分线）
    for c_mid1 in range(n):
        for c_mid2 in range(c_mid1 + 1, n - 1):
            a = f1[(0, 0, m - 1, c_mid1)]
            b = f1[(0, c_mid1 + 1, m - 1, c_mid2)]
            c = f1[(0, c_mid2 + 1, m - 1, n - 1)]
            ans = min(ans, a + b + c)

    # 3.2 三条水平带（两条横向切分线）
    for r_mid1 in range(m):
        for r_mid2 in range(r_mid1 + 1, m - 1):
            a = f1[(0, 0, r_mid1, n - 1)]
            b = f1[(r_mid1 + 1, 0, r_mid2, n - 1)]
            c = f1[(r_mid2 + 1, 0, m - 1, n - 1)]
            ans = min(ans, a + b + c)

    # 3.3 先竖后横：左侧 1 矩形 + 右侧 2 矩形（水平切分）
    for col in range(n - 1):
        left_one = f1[(0, 0, m - 1, col)]
        right_two = f2[(0, col + 1, m - 1, n - 1)]
        ans = min(ans, left_one + right_two)

        left_two = f2[(0, 0, m - 1, col)]
        right_one = f1[(0, col + 1, m - 1, n - 1)]
        ans = min(ans, left_two + right_one)

    # 3.4 先横后竖：上方 1 矩形 + 下方 2 矩形（垂直切分）
    for row in range(m - 1):
        top_one = f1[(0, 0, row, n - 1)]
        bottom_two = f2[(row + 1, 0, m - 1, n - 1)]
        ans = min(ans, top_one + bottom_two)

        top_two = f2[(0, 0, row, n - 1)]
        bottom_one = f1[(row + 1, 0, m - 1, n - 1)]
        ans = min(ans, top_two + bottom_one)

    return ans
```

> **代码要点解释**  
> 1. `f1[(r1,c1,r2,c2)]` 用 **字典** 存储，键是四元组，读取时 O(1)。  
> 2. 计算 `f1` 时直接遍历子矩形，找到 1 的最外层行、列，即外接矩形。  
> 3. 计算 `f2` 时只需要尝试 **所有可能的切分线**，把子矩形分成两块，分别使用 `f1`，取最小和。  
> 4. 最后四段枚举对应四种“划分方式”，每一次都只做 O(1) 次查表相加，整体时间主要耗在预处理 `f1/f2`，约几千万次基本操作，轻松跑完。

#### 复杂度  

- **时间复杂度**  
  - 计算 `f1`：`O(m² n² * m n)` ≈ `O(m³ n³)`，在最坏 `30³·30³ = 4.5×10⁷` 次。  
  - 计算 `f2`：对每个子矩形尝试最多 `m+n` 条切分线，故 `O(m² n² (m+n))` ≈ `3×10⁶` 次。  
  - 最终枚举四种布局：`O(m + n + m² + n²)`，可以忽略。  
  - **总体**：约 `5×10⁷` 次基本操作，远低于 1 秒的限制。  

- **空间复杂度**  
  - `f1`、`f2` 各保存 `O(m² n²)` 个整数，约 `5×10⁴` 个，几 MB 级别。  
  - 额外使用常数级别的变量，整体 `O(m² n²)`。

> **意义**：  
> - `O(m³ n³)` 中的 “³” 其实是因为网格非常小（≤30），所以即使是立方级别也能接受。  
> - 与暴力解的 `O(m⁶ n⁶)` 相比，次数从天文级降到了几千万级，真正可以跑在实际机器上。

---

## 心得  

- **核心技巧**：把“3 条不相交矩形”转化为**划分线**的枚举，利用**子问题 DP**（`f1`、`f2`）把局部最优合并成全局最优。  
- **适用的题型**  
  1. “用 k 条矩形/线段覆盖所有 1”，如 *Find Minimum Area to Cover All Ones I*（k=2）。  
  2. “把矩阵划分为若干块，使每块满足某种属性”，比如 “分割数组使每块和相等”。  
  3. “在小尺寸网格上求最优划分”，如 “最小代价分割棋盘”。  
- **一句话总结**：**先求出任意子区域用一条矩形的最小面积，再通过切分线递推得到两条、三条矩形的最小面积**。

---

## 反思  

- **第一反应**：直接想把所有可能的三条矩形枚举，结果发现时间爆炸。  
- **最容易踩的坑**  
  1. **忘记矩形可以相邻**：相邻不算重叠，切分线可以放在两矩形之间的边界上。  
  2. **子区域没有 1 时的处理**：面积应为 0，否则会把不存在的矩形计入总和。  
  3. **边界条件**：切分线的循环范围必须保证左/上区域非空，否则会产生非法索引。  
- **下次类似题的第一步**：**先思考如何用“一条切分线”把问题拆成更小的子问题**，再利用 DP/前缀和把子问题的最优解保存起来，最后合并。这样可以把指数级搜索压到多项式级。