# #1401. **圆与矩形重叠** / Circle and Rectangle Overlapping

> 难度：中等 · 标签：Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/circle-and-rectangle-overlapping/)

---

## 题目（英文原版）

**Description**

You are given a circle represented as (radius, xCenter, yCenter) and an axis-aligned rectangle represented as (x1, y1, x2, y2), where (x1, y1) are the coordinates of the bottom-left corner, and (x2, y2) are the coordinates of the top-right corner of the rectangle.
Return true if the circle and rectangle are overlapped otherwise return false. In other words, check if there is any point (xi, yi) that belongs to the circle and the rectangle at the same time.

**Examples**

**Example 1:**

```
Input: radius = 1, xCenter = 0, yCenter = 0, x1 = 1, y1 = -1, x2 = 3, y2 = 1
Output: true
Explanation: Circle and rectangle share the point (1,0).
```

**Example 2:**

```
Input: radius = 1, xCenter = 1, yCenter = 1, x1 = 1, y1 = -3, x2 = 2, y2 = -1
Output: false
```

**Example 3:**

```
Input: radius = 1, xCenter = 0, yCenter = 0, x1 = -1, y1 = 0, x2 = 0, y2 = 1
Output: true
```

**Constraints**

- 1 <= radius <= 2000
- -104 <= xCenter, yCenter <= 104
- -104 <= x1 < x2 <= 104
- -104 <= y1 < y2 <= 104

---

## 题目（中文翻译）

给定一个圆，用三元组 **(radius, xCenter, yCenter)** 表示，其中 `radius` 为半径，`(xCenter, yCenter)` 为圆心坐标；以及一个轴对齐矩形，用四元组 **(x1, y1, x2, y2)** 表示，其中 `(x1, y1)` 为左下角坐标，`(x2, y2)` 为右上角坐标。  
如果圆和矩形存在重叠则返回 `true`，否则返回 `false`。换句话说，判断是否存在任意点 **(xi, yi)** 同时属于圆和矩形。

**示例 1**  
**输入**: `radius = 1, xCenter = 0, yCenter = 0, x1 = 1, y1 = -1, x2 = 3, y2 = 1`  
**输出**: `true`  
**解释**: 圆和矩形共享点 **(1, 0)**。

**示例 2**  
**输入**: `radius = 1, xCenter = 1, yCenter = 1, x1 = 1, y1 = -3, x2 = 2, y2 = -1`  
**输出**: `false`  

**示例 3**  
**输入**: `radius = 1, xCenter = 0, yCenter = 0, x1 = -1, y1 = 0, x2 = 0, y2 = 1`  
**输出**: `true`  

**约束条件**  
- `1 <= radius <= 2000`  
- `-10^4 <= xCenter, yCenter <= 10^4`  
- `-10^4 <= x1 < x2 <= 10^4`  
- `-10^4 <= y1 < y2 <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把矩形内部的每一个点都“检查一遍”，看它是否落在圆内部。  
- **遍历**：把矩形的左下角 `(x1, y1)` 当作起点，逐行、逐列遍历到右上角 `(x2, y2)`。  
- **判断**：对每个点 `(xi, yi)`，计算它到圆心 `(xCenter, yCenter)` 的欧氏距离  
  \[
  d = \sqrt{(xi-xCenter)^2 + (yi-yCenter)^2}
  \]  
  如果 `d <= radius`，说明这个点同时属于圆和矩形，题目即返回 `True`。  
- **结束**：遍历完所有点仍未找到满足条件的点，则返回 `False`。  

> **类比**：把矩形想成一本书的每一页，遍历每页就像在找一本字典里有没有某个词。这里的“词”是“满足距离条件的点”。  

这种方法之所以 **正确**，是因为我们把矩形里可能的所有点都枚举了，只要有交点一定会被找到。  

**时间/空间复杂度**  
- 时间复杂度：`O( (x2-x1) * (y2-y1) )`。如果矩形宽度为 `w = x2-x1`，高度为 `h = y2-y1`，我们要检查 `w*h` 个点。用大白话说，就是“矩形有多大，就要检查多少次”。  
- 空间复杂度：`O(1)`，只用常数个变量存坐标和距离。

> 注意：LeetCode 的坐标范围可达 `10^4`，所以 `w*h` 最坏可以是 `4·10^8`，这在实际运行中会超时甚至内存炸掉——这就是暴力解的瓶颈。

#### 代码（Python）

```python
import math

def checkOverlap_bruteforce(radius, xCenter, yCenter, x1, y1, x2, y2):
    # 逐行、逐列遍历矩形内部的每一个整数点
    for xi in range(x1, x2 + 1):          # +1 为了把右边界也算进去
        for yi in range(y1, y2 + 1):
            # 计算该点到圆心的距离
            dx = xi - xCenter
            dy = yi - yCenter
            distance = math.sqrt(dx * dx + dy * dy)
            # 如果距离不大于半径，说明该点在圆内
            if distance <= radius:
                return True               # 找到交点，直接返回
    return False                          # 全部点都不在圆内
```

#### 复杂度  

- **时间复杂度**：`O((x2 - x1) * (y2 - y1))`  
  → “矩形的面积有多大，就要检查多少次”。  
- **空间复杂度**：`O(1)`  
  → 只用了常数个临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**遍历所有点是最慢的环节**。我们需要一种只用常数时间就能判断“最近的点”和圆心的距离的方法。  

**关键观察**：  
- 对于任意一个矩形，离圆心最近的点一定在矩形的**内部或边界**上。  
- 这个最近点可以通过“把圆心的坐标**限制（clamp）**到矩形的范围”得到。  
  - “限制”的意思是：如果圆心的 x 坐标在矩形的左右边之间，就保持不变；否则取离它最近的左边或右边的 x 坐标。y 方向同理。  
  - 用生活化的类比：想象你站在圆心的位置，想要走到矩形里最近的点。你只能在水平和垂直方向上“踩到”矩形的边缘，不能跳过。  

**实现步骤**  

1. **求最近点的 x 坐标**  
   ```python
   closestX = min(max(xCenter, x1), x2)
   ```
   - `max(xCenter, x1)`：如果圆心在左边界左侧，就把它“推”到左边界 `x1`；否则保持原样。  
   - `min(..., x2)`：再把它限制到右边界 `x2`，防止超过右侧。  

2. **求最近点的 y 坐标**（同理）  
   ```python
   closestY = min(max(yCenter, y1), y2)
   ```

3. **计算最近点到圆心的距离的平方**（为了避免开根号）  
   ```python
   dx = closestX - xCenter
   dy = closestY - yCenter
   distance_sq = dx * dx + dy * dy
   ```

4. **比较**：如果 `distance_sq <= radius * radius`，说明最近点在圆内部或恰好在圆上，矩形与圆相交；否则不相交。  

> **为什么只看最近点就够？**  
> 因为如果最近点已经在圆外，那么矩形的所有其他点离圆心更远，自然不可能进入圆内。反之，最近点在圆内就已经证明有交点存在。  

#### 代码（Python）

```python
def checkOverlap(radius, xCenter, yCenter, x1, y1, x2, y2):
    """
    判断圆 (radius, xCenter, yCenter) 与轴对齐矩形 (x1, y1, x2, y2) 是否相交
    思路：先找到离圆心最近的矩形点，再比较距离与半径
    """
    # 1. 把圆心的 x 坐标限制到矩形的水平范围内
    #    如果圆心在矩形左边，则取左边界 x1；在右边则取右边界 x2；在中间保持不变
    closestX = min(max(xCenter, x1), x2)

    # 2. 把圆心的 y 坐标限制到矩形的垂直范围内（同理）
    closestY = min(max(yCenter, y1), y2)

    # 3. 计算最近点到圆心的距离的平方（避免使用 sqrt 提高效率）
    dx = closestX - xCenter
    dy = closestY - yCenter
    distance_sq = dx * dx + dy * dy

    # 4. 半径的平方
    radius_sq = radius * radius

    # 5. 若距离平方不大于半径平方，则相交
    return distance_sq <= radius_sq
```

#### 复杂度  

- **时间复杂度**：`O(1)`（常数时间）  
  → 只做了几次算术运算和比较，跟矩形大小毫无关系。相比暴力解的 “遍历所有点”，快了几个数量级。  
- **空间复杂度**：`O(1)`（常数空间）  
  → 只使用了若干临时变量，和输入规模无关。

---

## 心得  

- **核心技巧**：**坐标限制（clamp）** + **最近点距离比较**。  
- **适用的题型**（相似思路）  
  1. 判断点是否在矩形内部（`clamp` 直接判断是否相等）。  
  2. 判断圆与线段是否相交（把线段端点限制到圆的投影上）。  
  3. 判断两个轴对齐矩形是否相交（比较投影区间是否重叠）。  
- **一句话总结解题钥匙**：*只要找到离圆心最近的矩形点，比较它与半径的距离即可。*

---

## 反思  

- **第一反应**：把矩形里所有点枚举一遍检查——这在实际面试中往往会导致超时。  
- **最容易踩的坑**  
  - 忽略矩形完全包围圆心的情况（此时最近点就是圆心本身）。  
  - 只比较 x 方向或 y 方向的距离，而忘记用勾股定理合并两者。  
  - 处理边界时使用 `<=` 而不是 `<`，因为“相切”也算相交。  
- **下次遇到同类题**：第一步先思考“**最近点**”或“**投影**”概念，尝试把几何问题转化为**距离比较**，往往能直接得到 O(1) 解。