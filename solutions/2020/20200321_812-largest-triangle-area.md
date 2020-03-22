# #812. 最大三角形面积 / Largest Triangle Area

> 难度：简单 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/largest-triangle-area/)

---

## 题目（英文原版）

**Description**

Given an array of points on the X-Y plane points where points[i] = [xi, yi], return the area of the largest triangle that can be formed by any three different points. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: points = [[0,0],[0,1],[1,0],[0,2],[2,0]]
Output: 2.00000
Explanation: The five points are shown in the above figure. The red triangle is the largest.
```

**Example 2:**

```
Input: points = [[1,0],[0,0],[0,1]]
Output: 0.50000
```

**Constraints**

- 3 <= points.length <= 50
- -50 <= xi, yi <= 50
- All the given points are unique.

---

## 题目（中文翻译）

给定一个平面上点的数组 `points`，其中 `points[i] = [xi, yi]`，返回任意 **三个不同点** 能够组成的 **最大三角形** 的面积。只要答案与实际结果的误差在 `10⁻⁵` 以内即视为正确。

## 示例

### 示例 1
**输入**  
```
points = [[0,0],[0,1],[1,0],[0,2],[2,0]]
```
**输出**  
```
2.00000
```
**解释**  
如上图所示，给出了这五个点。红色的三角形面积最大。

### 示例 2
**输入**  
```
points = [[1,0],[0,0],[0,1]]
```
**输出**  
```
0.50000
```

## 约束条件
- `3 <= points.length <= 50`
- `-50 <= xi, yi <= 50`
- 所有给定的点互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**枚举所有三点组合**，对每一种组合计算它们能组成的三角形面积，取最大的那个。  

- **数据结构**：我们只需要把点保存在一个列表 `points` 中，遍历时用三个下标 `i、j、k` 来指向三点。  
- **生活化类比**：把点想成平面上的小石子，暴力解相当于把每三颗石子都拎起来，拼成一个三角形，然后量一下它的面积，找出最大的那块“石板”。  
- **为什么正确**：只要遍历到所有可能的三点组合，就不可能漏掉答案；面积的计算公式（叉积）是数学上严谨的。  

#### 代码（Python）  

```python
from typing import List
import itertools
import math

def largestTriangleArea(points: List[List[int]]) -> float:
    """
    暴力枚举所有三点组合，返回最大的三角形面积
    """
    max_area = 0.0                     # 用来记录目前找到的最大面积
    # itertools.combinations 会生成所有不重复的三元组 (i, j, k)
    for (x1, y1), (x2, y2), (x3, y3) in itertools.combinations(points, 3):
        # 叉积的绝对值等于两向量构成的平行四边形面积，除以 2 即为三角形面积
        area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0
        max_area = max(max_area, area)   # 更新最大值
    return max_area
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 解释：我们要把 `n`（最多 50）个点两两三两地挑出来，组合数是 `C(n,3) = n·(n-1)·(n-2)/6`，数量级上就是 `n³`。如果把 `n³` 想象成“把 50 块积木每次挑 3 块”，最多会尝试约 20,000 次，计算量在电脑上完全可以接受。  
- **空间复杂度**：`O(1)`（不计输入本身）  
  - 解释：只用了常数个变量来保存临时面积和最大面积，没有额外的随 `n` 增长的数据结构。  

---  

### 2. 最优解  

#### 思路  

虽然暴力已经够快（`n ≤ 50`），但从算法角度我们可以把时间降到 **`O(m²)`**，其中 `m` 是点的**凸包**（外壳）上的点数。原因是：  

1. **三角形的最大面积一定出现在凸包的顶点**。  
   - 类比：想象把所有点用橡皮筋紧紧包住，橡皮筋形成的多边形叫凸包。任何在橡皮筋内部的点，和外面的点组成的三角形都可以“拉伸”到更大的面积，直到顶点落在橡皮筋上。  
2. 于是我们先把点的凸包算出来（**单调链（Monotone Chain）**算法，时间 `O(n log n)`），得到一个顺时针或逆时针排列的点序列。  
3. 对凸包上的点使用 **旋转卡尺（Rotating Calipers）**：固定一个顶点 `i`，在其余点中寻找两条“卡尺”使得面积最大。旋转卡尺的核心是：当 `j` 向前移动时，`k` 只会单调前进，不会回头，从而整体只需要 `O(m²)` 次比较。  

下面一步步解释核心概念：  

- **凸包**：把所有点想成散落的邮票，用一根细绳把所有邮票围住，绳子形成的最紧凑的多边形就是凸包。常用的 **Monotone Chain** 实现方式是先按 `x` 再按 `y` 排序，然后分别从左到右、右到左构造上、下链。  
- **叉积**：两向量的叉积 `| (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1) |` 等于平行四边形面积，除以 2 就是三角形面积。  
- **旋转卡尺**：想象两根可旋转的尺子夹住凸包的三个点，随着其中一个点沿着凸包顺时针移动，另外两个点也会顺时针“追随”，因为面积函数在凸多边形上是单调的，这样我们只需要线性遍历即可。  

#### 代码（Python）  

```python
from typing import List
import math

def cross(o, a, b):
    """
    计算向量 OA 与 OB 的叉积
    o, a, b 为点 (x, y)
    返回值为叉积的有符号值
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points: List[List[int]]) -> List[List[int]]:
    """
    Monotone Chain 求凸包，返回按逆时针顺序排列的顶点列表
    复杂度 O(n log n)（排序主导）
    """
    # 先按 x 再按 y 排序，去重（题目已保证唯一，这一步可省）
    points = sorted(set(map(tuple, points)))
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        # 当加入新点后，最后两个点与新点形成的转向不是左转（即 cross <= 0），说明不是凸的，弹出
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # 去掉重复的起点和终点
    return lower[:-1] + upper[:-1]

def largestTriangleArea(points: List[List[int]]) -> float:
    """
    最优解：先求凸包，再用旋转卡尺在凸包上找最大三角形面积
    时间复杂度 O(m²) ，其中 m 为凸包点数（最坏情况仍是 O(n²)）
    """
    hull = convex_hull(points)          # 1️⃣ 计算凸包
    m = len(hull)
    if m < 3:
        return 0.0

    max_area = 0.0
    # 2️⃣ 旋转卡尺：固定 i，遍历 j、k
    for i in range(m):
        k = (i + 2) % m                 # k 初始为 i+2，保证三点不重合
        for j in range(i + 1, i + m - 1):
            j_mod = j % m                # 将索引映射回环形数组
            # 移动 k，使得面积最大（单调递增）
            while True:
                next_k = (k + 1) % m
                cur = abs(cross(hull[i], hull[j_mod], hull[k]))
                nxt = abs(cross(hull[i], hull[j_mod], hull[next_k]))
                if nxt > cur:
                    k = next_k
                else:
                    break
            # 记录此时的面积（除以 2）
            area = cur / 2.0
            max_area = max(max_area, area)

    return max_area
```

> **代码要点注释**  
> - `cross` 用来计算叉积，正负表示转向（左转/右转），但我们只关心绝对值来求面积。  
> - `convex_hull` 的 `lower`、`upper` 分别是下凸链和上凸链，合在一起即完整的凸包。  
> - 旋转卡尺的核心是 `while` 循环：只要把 `k` 再往前走能让面积更大，就继续前进；一旦不再增大，就停下来，这保证了整体只遍历 `O(m²)` 次。  

#### 复杂度  

- **时间复杂度**：`O(n log n + m²)`  
  - `n log n` 来自排序求凸包。  
  - `m` 是凸包顶点数，最坏情况下 `m = n`，于是整体是 `O(n²)`。与暴力的 `O(n³)` 比，数量级下降了一个阶。  
- **空间复杂度**：`O(n)`  
  - 需要存储排序后的点列表和凸包本身，都是线性空间。  

---  

## 心得  

- **核心技巧**：**凸包 + 旋转卡尺**。  
- **适用的题型**  
  1. “给定点集合，求最大/最小面积/周长的几何图形”——如最大矩形、最小包围圆。  
  2. “在凸多边形上求某种极值”——如找最大距离（直径）或最小宽度。  
  3. “点集合的几何优化”——如求最远点对（旋转卡尺的另一种用法）。  
- **一句话总结**：**先把“外壳”找出来，再在外壳上用卡尺“转动”，可以把原本的三重循环降到二重循环。**  

---  

## 反思  

- **第一反应**：看到“任意三点”，自然想到直接枚举三元组，写出叉积公式求面积。  
- **最容易踩的坑**  
  - **整数溢出**：在某些语言里叉积可能超过 32 位整数范围，但 Python 的整数是大数，不会溢出。  
  - **边界条件**：当所有点共线时，最大面积应为 `0`，需要确保代码不会因为 `m < 3` 而出错。  
  - **循环取模**：旋转卡尺需要在环形数组上移动，忘记 `% m` 会导致索引越界。  
- **下次第一步**：先判断点的规模，如果 `n` 很大，立刻考虑 **先求凸包**，因为最大几何量往往落在凸包上。这样可以把搜索空间大幅缩小，再决定使用哪种具体的优化（卡尺、双指针、动态规划等）。