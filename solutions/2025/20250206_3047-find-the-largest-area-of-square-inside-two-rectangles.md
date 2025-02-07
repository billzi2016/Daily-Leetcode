# #3047. 求两个矩形内部的最大正方形面积 / Find the Largest Area of Square Inside Two Rectangles

> 难度：中等 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/find-the-largest-area-of-square-inside-two-rectangles/)

---

## 题目（英文原版）

**Description**

There exist n rectangles in a 2D plane with edges parallel to the x and y axis. You are given two 2D integer arrays bottomLeft and topRight where bottomLeft[i] = [a_i, b_i] and topRight[i] = [c_i, d_i] represent the bottom-left and top-right coordinates of the ith rectangle, respectively.
You need to find the maximum area of a square that can fit inside the intersecting region of at least two rectangles. Return 0 if such a square does not exist.
Input: bottomLeft = [[1,1],[2,2],[3,1]], topRight = [[3,3],[4,4],[6,6]]
Output: 1
Explanation:
A square with side length 1 can fit inside either the intersecting region of rectangles 0 and 1 or the intersecting region of rectangles 1 and 2. Hence the maximum area is 1. It can be shown that a square with a greater side length can not fit inside any intersecting region of two rectangles.
Input: bottomLeft = [[1,1],[1,3],[1,5]], topRight = [[5,5],[5,7],[5,9]]
Output: 4
Explanation:
A square with side length 2 can fit inside either the intersecting region of rectangles 0 and 1 or the intersecting region of rectangles 1 and 2. Hence the maximum area is 2 * 2 = 4. It can be shown that a square with a greater side length can not fit inside any intersecting region of two rectangles.
Input: bottomLeft = [[1,1],[2,2],[1,2]], topRight = [[3,3],[4,4],[3,4]]
Output: 1
Explanation:
A square with side length 1 can fit inside the intersecting region of any two rectangles. Also, no larger square can, so the maximum area is 1. Note that the region can be formed by the intersection of more than 2 rectangles.
Input: bottomLeft = [[1,1],[3,3],[3,1]], topRight = [[2,2],[4,4],[4,2]]
Output: 0
Explanation:
No pair of rectangles intersect, hence, the answer is 0.

**Constraints**

- n == bottomLeft.length == topRight.length
- 2 <= n <= 103
- bottomLeft[i].length == topRight[i].length == 2
- 1 <= bottomLeft[i][0], bottomLeft[i][1] <= 107
- 1 <= topRight[i][0], topRight[i][1] <= 107
- bottomLeft[i][0] < topRight[i][0]
- bottomLeft[i][1] < topRight[i][1]

---

## 题目（中文翻译）

存在 n 个矩形，均位于二维平面上且四边平行于坐标轴。给定两个二维整数数组 `bottomLeft` 和 `topRight`，其中 `bottomLeft[i] = [a_i, b_i]` 与 `topRight[i] = [c_i, d_i]` 分别表示第 i 个矩形的左下角（bottom‑left）坐标和右上角（top‑right）坐标。  

要求求出可以放入 **至少两个矩形的交叉区域（intersecting region）** 内的正方形（square）的最大面积。如果不存在这样的正方形，返回 0。  

## 示例  

### 示例 1  
**输入**  
```
bottomLeft = [[1,1],[2,2],[3,1]], 
topRight = [[3,3],[4,4],[6,6]]
```  
**输出**  
```
1
```  
**解释**  
边长为 1 的正方形可以放入矩形 0 与矩形 1 的交叉区域，或者矩形 1 与矩形 2 的交叉区域。因此最大面积为 1。可以证明，边长更大的正方形无法放入任意两个矩形的交叉区域。  

### 示例 2  
**输入**  
```
bottomLeft = [[1,1],[1,3],[1,5]], 
topRight = [[5,5],[5,7],[5,9]]
```  
**输出**  
```
4
```  
**解释**  
边长为 2 的正方形可以放入矩形 0 与矩形 1 的交叉区域，或矩形 1 与矩形 2 的交叉区域。因此最大面积为 \(2 \times 2 = 4\)。可以证明，边长更大的正方形无法放入任意两个矩形的交叉区域。  

### 示例 3  
**输入**  
```
bottomLeft = [[1,1],[2,2],[1,2]], 
topRight = [[3,3],[4,4],[3,4]]
```  
**输出**  
```
1
```  
**解释**  
边长为 1 的正方形可以放入任意两矩形的交叉区域。更大的正方形都无法放入，因此最大面积为 1。注意，交叉区域可以由超过 2 个矩形的交集形成。  

### 示例 4  
**输入**  
```
bottomLeft = [[1,1],[3,3],[3,1]], 
topRight = [[2,2],[4,4],[4,2]]
```  
**输出**  
```
0
```  
**解释**  
不存在任意两矩形相交的情况，故答案为 0。  

## 约束条件  

- `n == bottomLeft.length == topRight.length`  
- `2 <= n <= 10^3`  
- `bottomLeft[i].length == topRight[i].length == 2`  
- `1 <= bottomLeft[i][0], bottomLeft[i][1] <= 10^7`  
- `1 <= topRight[i][0], topRight[i][1] <= 10^7`  
- `bottomLeft[i][0] < topRight[i][0]`  
- `bottomLeft[i][1] < topRight[i][1]`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们要找 **至少两** 个矩形的交集里能放下的最大正方形面积。  
最直接的办法就是：

1. 把所有矩形两两配对（`i < j`），因为题目只要求“至少两”，配对已经足够。  
2. 对每一对矩形，先判断它们是否相交。  
   - 两个轴对齐的矩形 **不相交** 的情况很容易记：  
     - 第一个矩形的左边界在第二个矩形的右边界右侧（`x1_left > x2_right`），或者  
     - 第一个矩形的右边界在第二个矩形的左边界左侧（`x1_right < x2_left`），  
     - 同理检查 **y** 方向。  
   - 如果没有上述情况，说明它们有交集。  
3. 交集本身也是一个矩形，求它的左下角和右上角坐标：
   - 左下角的 **x** 坐标 = 两个矩形左边界的 **最大值**（因为交集的左边要往右推）  
   - 左下角的 **y** 坐标 = 两个矩形下边界的 **最大值**  
   - 右上角的 **x** 坐标 = 两个矩形右边界的 **最小值**（因为交集的右边要往左收）  
   - 右上角的 **y** 坐标 = 两个矩形上边界的 **最小值**  
4. 交集矩形的宽度 = `right_x - left_x`，高度 = `top_y - bottom_y`。  
   正方形的边长只能不超过宽度和高度的 **较小者**，即 `side = min(width, height)`。  
5. 把所有配对得到的 `side` 取最大值，答案就是 `max_side²`（面积）。

> **类比**：把每个矩形想成一本书的封面，两个封面重叠的部分就是它们的“公共页面”。我们要找的正方形，就像在这块公共页面上画一个最大的正方形。

#### 代码（Python）

```python
from typing import List

def largestSquareArea(bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
    n = len(bottomLeft)
    max_side = 0                     # 记录能放下的最大正方形边长

    # 双层循环遍历所有矩形对 (i, j)
    for i in range(n):
        x1_left, y1_bottom = bottomLeft[i]
        x1_right, y1_top   = topRight[i]

        for j in range(i + 1, n):
            x2_left, y2_bottom = bottomLeft[j]
            x2_right, y2_top   = topRight[j]

            # ---- 判断是否相交 ----
            # 如果在 x 方向上没有交集，或者在 y 方向上没有交集，则跳过
            if x1_left > x2_right or x2_left > x1_right:
                continue
            if y1_bottom > y2_top or y2_bottom > y1_top:
                continue

            # ---- 计算交集矩形的四条边 ----
            inter_left   = max(x1_left,  x2_left)   # 左边界取较大的
            inter_bottom = max(y1_bottom, y2_bottom)# 下边界取较大的
            inter_right  = min(x1_right, x2_right) # 右边界取较小的
            inter_top    = min(y1_top,   y2_top)   # 上边界取较小的

            width  = inter_right - inter_left
            height = inter_top   - inter_bottom

            # 交集可能退化成线段或点，此时宽或高为 0，直接跳过
            if width <= 0 or height <= 0:
                continue

            # 能放进去的正方形边长 = 宽高的较小值
            side = min(width, height)
            max_side = max(max_side, side)

    # 面积 = 边长的平方
    return max_side * max_side
```

> 代码中的每一行都配有中文注释，帮助初学者快速对照思路。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们要检查每一对矩形，配对的数量是 `C(n,2) = n·(n-1)/2`，大约是 `n²/2`，所以时间随 `n` 的平方增长。对 1000 个矩形来说，大约只有 500,000 次循环，完全可以接受。

- **空间复杂度**：`O(1)`  
  只用了常数级的额外变量（`max_side`、临时坐标等），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

在本题的约束下（`n ≤ 10³`），**暴力枚举所有配对已经是最优的**。  
为什么？

- **下界**：我们必须至少检查两两矩形的交集，因为答案可能来源于任意两矩形的交集。没有额外的结构（如排序后一次扫过）能保证在不检查某对的情况下仍然得到全局最大值。  
- **上界**：一次配对的计算只涉及常数次比较与加减运算，时间是 `O(1)`。因此整体 `O(n²)` 已经是最紧凑的可能。

不过，为了让思路更“优化”，我们可以在暴力循环里加入**提前剪枝**，进一步降低常数：

1. **宽高提前估计**：如果当前已知的 `max_side` 已经很大，而两矩形的水平或垂直间距（`min(x1_right, x2_right) - max(x1_left, x2_left)`）小于 `max_side`，则这对矩形不可能再产生更大的正方形，直接跳过。  
2. **使用整数坐标的特性**：所有坐标都是整数，正方形的边长也一定是整数，这让我们可以把 `max_side` 当作整数比较，避免浮点运算。

下面给出加入剪枝的实现，逻辑与上面的暴力解相同，只是更快一些。

#### 代码（Python）

```python
from typing import List

def largestSquareAreaOptimized(bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
    n = len(bottomLeft)
    max_side = 0

    for i in range(n):
        x1_l, y1_b = bottomLeft[i]
        x1_r, y1_t = topRight[i]

        for j in range(i + 1, n):
            x2_l, y2_b = bottomLeft[j]
            x2_r, y2_t = topRight[j]

            # 先做快速不相交检查（与暴力版相同）
            if x1_l > x2_r or x2_l > x1_r:
                continue
            if y1_b > y2_t or y2_b > y1_t:
                continue

            # 计算交集宽高
            inter_left   = max(x1_l, x2_l)
            inter_bottom = max(y1_b, y2_b)
            inter_right  = min(x1_r, x2_r)
            inter_top    = min(y1_t, y2_t)

            width  = inter_right - inter_left
            height = inter_top   - inter_bottom

            if width <= 0 or height <= 0:
                continue

            # 剪枝：如果宽高的较小值已经不超过当前 max_side，则不可能更新答案
            possible_side = min(width, height)
            if possible_side <= max_side:
                continue

            max_side = possible_side

    return max_side * max_side
```

#### 复杂度

- **时间复杂度**：`O(n²)`（与暴力解相同的渐进上界）  
  解释：仍然需要遍历所有配对，只是通过剪枝可以在实际运行时省掉一部分不必要的计算，常数更小。

- **空间复杂度**：`O(1)`  
  只使用了固定数量的临时变量。

---

## 心得

- **核心技巧**：**矩形交集的几何计算** + **正方形边长取宽高最小值**。  
- **适用的类似题型**：  
  1. “求两个矩形交集的面积”  
  2. “在若干矩形的公共区域里放置最大的圆/正方形”  
  3. “判断任意两条线段是否相交并求交点”  
- **解题钥匙**：**把二维几何问题转化为四个一维比较（max / min）**，再用 **`min(width, height)`** 得到正方形的最大可能边长。

---

## 反思

- **第一反应**：先想到 “两两配对，求交集”，因为题目本身要求“至少两”，配对是最自然的枚举方式。  
- **最容易踩的坑**：  
  - 忘记检查交集是否退化成 **线段或点**（宽或高为 0），这会导致 `side = 0` 但仍被计入最大值。  
  - 坐标的比较方向写反了，例如把 `x1_left > x2_right` 当成 “相交”。  
  - 对 **大数**（坐标可达 `10⁷`）使用 **浮点数**，可能产生精度误差，直接用整数比较更安全。  
- **下次遇到同类题**：第一步先 **写出“是否相交 + 交集坐标”** 的通用公式，随后根据题目需求（面积、周长、能否放置某形状）再进行后续计算。这样可以把复杂的几何问题拆解成若干简单的 **max / min** 操作。