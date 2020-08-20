# #963. 最小面积矩形 II / Minimum Area Rectangle II

> 难度：中等 · 标签：Array、Hash Table、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/minimum-area-rectangle-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of points in the X-Y plane points where points[i] = [xi, yi].
Return the minimum area of any rectangle formed from these points, with sides not necessarily parallel to the X and Y axes. If there is not any such rectangle, return 0.
Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: points = [[1,2],[2,1],[1,0],[0,1]]
Output: 2.00000
Explanation: The minimum area rectangle occurs at [1,2],[2,1],[1,0],[0,1], with an area of 2.
```

**Example 2:**

```
Input: points = [[0,1],[2,1],[1,1],[1,0],[2,0]]
Output: 1.00000
Explanation: The minimum area rectangle occurs at [1,0],[1,1],[2,1],[2,0], with an area of 1.
```

**Example 3:**

```
Input: points = [[0,3],[1,2],[3,1],[1,3],[2,1]]
Output: 0
Explanation: There is no possible rectangle to form from these points.
```

**Constraints**

- 1 <= points.length <= 50
- points[i].length == 2
- 0 <= xi, yi <= 4 * 104
- All the given points are unique.

---

## 题目（中文翻译）

给定一个二维平面上的点数组 **points**，其中 `points[i] = [xi, yi]` 表示第 *i* 个点的坐标。  
返回由这些点构成的任意矩形（rectangle）的最小面积，矩形的四条边不要求平行于 X 轴或 Y 轴。如果不存在这样的矩形，返回 `0`。  
答案相对误差在 `10^-5` 以内均视为正确。

**示例 1**  
输入: `points = [[1,2],[2,1],[1,0],[0,1]]`  
输出: `2.00000`  
解释: 最小面积矩形由点 `[1,2]、[2,1]、[1,0]、[0,1]` 构成，面积为 `2`。

**示例 2**  
输入: `points = [[0,1],[2,1],[1,1],[1,0],[2,0]]`  
输出: `1.00000`  
解释: 最小面积矩形由点 `[1,0]、[1,1]、[2,1]、[2,0]` 构成，面积为 `1`。

**示例 3**  
输入: `points = [[0,3],[1,2],[3,1],[1,3],[2,1]]`  
输出: `0`  
解释: 这些点无法组成任何矩形。

**约束条件**

- `1 <= points.length <= 50`
- `points[i].length == 2`
- `0 <= xi, yi <= 4 * 10^4`
- 所有给定的点均互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有点的**四元组**（4 个点）枚举出来，逐个判断这 4 个点能否组成一个矩形，再算出它的面积取最小值。  
判断矩形的条件可以用向量的**垂直**来表达：  
- 设四个点为 A、B、C、D（任意顺序），如果把它们两两配成两条相邻的边（如 AB、BC、CD、DA），则相邻两条边的向量点积应为 0（因为垂直）。  
- 同时，四条边的长度必须两两相等（AB=CD，BC=DA），这样才能保证是矩形而不是平行四边形。

**数据结构**  
- 直接用 Python 的 `list` 保存点坐标，遍历时用 `itertools.combinations` 生成所有四元组。  
- 判断垂直时用向量的点积公式 `x1*x2 + y1*y2`，这就像查字典一样：把两个向量的“x 分量”相乘再加上“y 分量”相乘，结果为 0 说明它们互相垂直。

**为什么正确**  
枚举所有可能的 4 点组合，必然不会错过任何合法矩形；只要我们的判定条件（两条相邻边垂直且对应边相等）成立，就一定是矩形。

**复杂度**  
- 设点的数量为 `n`（最多 50），四元组的数量是 `C(n,4) = n·(n-1)·(n-2)·(n-3)/24`，数量级约为 `O(n⁴)`。  
- 每个四元组内部做常数次向量运算，空间只用存点本身，`O(1)`。

> 大白话解释：如果你把 50 只小鸡排成一行，每只小鸡要和后面的 49、48、…、1 只小鸡分别配对，最后再把 4 只小鸡凑一块检查，工作量会像 **四次方** 那么大，几乎不可接受。

#### 代码（Python）

```python
from itertools import combinations
from math import hypot

def minAreaFreeRect_bruteforce(points):
    # 把点列表转成元组，方便哈希（后面会用到）
    pts = [tuple(p) for p in points]
    min_area = float('inf')

    # 依次枚举所有四元组
    for quad in combinations(pts, 4):
        # 先把四个点全排列一次，尝试找出一种顺序使得相邻边垂直
        # 为了代码简洁，这里直接检查所有 3 种可能的对角线划分
        a, b, c, d = quad
        # 计算四条可能的边向量
        vec = {
            (a, b): (b[0]-a[0], b[1]-a[1]),
            (b, c): (c[0]-b[0], c[1]-b[1]),
            (c, d): (d[0]-c[0], d[1]-c[1]),
            (d, a): (a[0]-d[0], a[1]-d[1]),
            (a, c): (c[0]-a[0], c[1]-a[1]),   # 对角线
            (b, d): (d[0]-b[0], d[1]-b[1]),
        }

        # 检查四边是否能形成矩形（两条相邻边垂直且对应边相等）
        # 这里遍历四种旋转方式
        for order in [(a,b,c,d), (a,c,b,d), (a,b,d,c)]:
            p1, p2, p3, p4 = order
            v1 = vec[(p1, p2)]
            v2 = vec[(p2, p3)]
            v3 = vec[(p3, p4)]
            v4 = vec[(p4, p1)]

            # 垂直：向量点积为 0
            if v1[0]*v2[0] + v1[1]*v2[1] != 0:   # 不是直角
                continue
            # 对边相等
            if v1[0]**2 + v1[1]**2 != v3[0]**2 + v3[1]**2:   # AB != CD
                continue
            if v2[0]**2 + v2[1]**2 != v4[0]**2 + v4[1]**2:   # BC != DA
                continue

            # 计算面积 = |AB| * |BC|
            area = hypot(*v1) * hypot(*v2)
            min_area = min(min_area, area)

    return 0 if min_area == float('inf') else min_area
```

#### 复杂度

- **时间复杂度**：`O(n⁴)`  
  解释：我们把所有 4 点组合都遍历了一遍，点的数量越多，工作量会呈四次方增长。

- **空间复杂度**：`O(1)`（不计输入存储）  
  解释：只用了常数个临时变量来保存向量和面积。

---

### 2. 最优解

#### 思路  

**从暴力解出发**，我们发现瓶颈在于“枚举四元组”。  
实际上，矩形的 **两条对角线** 有两个关键特性：

1. **长度相等**（对角线是矩形的两条相同的线段）。  
2. **中点相同**（对角线的交点就是矩形的中心）。

只要我们找到两条满足这两个条件的线段，它们的四端点必定能组成一个矩形。于是可以把**点对**（即每条可能的线段）作为基本单位来处理，而不是四元组。

**核心算法**：  
- 对所有点对 `(i, j)`（`i < j`）计算  
  - 中点 `mid = ((xi + xj) / 2, (yi + yj) / 2)`  
  - 对角线的平方长度 `dist = (xi - xj)² + (yi - yj)²`  
- 用哈希表把「相同中点且相同长度」的点对放到同一个桶里。  
  - 这一步类似把“查字典”，`key = (mid_x, mid_y, dist)`，`value` 是所有拥有这个 key 的点对列表。  
- 对每个桶内的点对两两组合，计算对应矩形的面积。  
  - 已知四个顶点 A、B、C、D（假设 AB、CD 为一条对角线，AC、BD 为另一条），矩形的面积等于两条相邻边的长度乘积。  
  - 取任意一条对角线的两个端点（如 A、C），它们与另一条对角线的端点（如 B、D）形成两个向量 `AB` 与 `AD`。面积可以用 **向量叉积的绝对值** 来得到：`area = |AB × AD|`（因为 `|AB × AD| = |AB| * |AD| * sinθ`，而在矩形中 `θ = 90°`，所以等于 `|AB|*|AD|`）。  
  - 实际上，用向量叉积可以直接得到面积，即 `area = abs((xB-xA)*(yD-yA) - (yB-yA)*(xD-xA))`。

**为什么快**  
- 点对的数量是 `C(n,2) = n·(n-1)/2`，约为 `O(n²)`，比 `O(n⁴)` 少了很多。  
- 只在同一个 bucket（中点+长度相同）内部做两两组合，通常每个 bucket 里的点对很少，整体仍保持 `O(n²)` 的规模。

**类比**  
把每条线段想象成“一张票”，票面上写着它的“中心位置”和“长度”。我们把所有写着相同信息的票放进同一个抽屉（哈希表的 bucket），抽屉里有两张票就能拼成一张矩形的“拼图”。只要遍历抽屉，就能找到所有可能的矩形。

#### 代码（Python）

```python
from collections import defaultdict
from math import inf

def minAreaFreeRect(points):
    """
    最优解：利用对角线的「相同中点 + 相同长度」特性。
    """
    pts = [tuple(p) for p in points]
    # key -> list of point pairs (i, j)
    # key 为 (mid_x*2, mid_y*2, dist) 为了保持整数（避免浮点误差）
    buckets = defaultdict(list)

    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            # 中点乘以 2（保持整数），因为 (x1+x2)/2 可能是小数
            mid_x2 = x1 + x2          # = 2 * midpoint.x
            mid_y2 = y1 + y2          # = 2 * midpoint.y
            # 对角线的平方距离
            dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
            buckets[(mid_x2, mid_y2, dist)].append((i, j))

    min_area = inf

    # 在每个 bucket 中，两条对角线即可构成矩形
    for key, pairs in buckets.items():
        if len(pairs) < 2:   # 少于两条对角线不可能成矩形
            continue
        # 两两组合
        for a in range(len(pairs)):
            i1, j1 = pairs[a]
            for b in range(a + 1, len(pairs)):
                i2, j2 = pairs[b]

                # 取四个不同的点（如果有重复说明是同一条线段，跳过）
                pts_set = {i1, j1, i2, j2}
                if len(pts_set) != 4:
                    continue

                # 任选一个点作为左下角，这里取 i1
                ax, ay = pts[i1]
                bx, by = pts[i2]
                dx, dy = pts[j2]

                # 向量 AB 与 AD
                vec1 = (bx - ax, by - ay)   # AB
                vec2 = (dx - ax, dy - ay)   # AD

                # 叉积的绝对值即为矩形面积
                area = abs(vec1[0] * vec2[1] - vec1[1] * vec2[0])
                if area < min_area:
                    min_area = area

    return 0 if min_area == inf else min_area
```

> **代码要点注释**  
- `mid_x2, mid_y2` 用 “两倍的中点坐标” 代替真实的中点，避免浮点数比较带来的误差。  
- `dist` 用平方距离代替真实距离，同样是为了保持整数且不影响比较。  
- `defaultdict(list)` 相当于一本“字典”，把相同 `key` 的所有点对收集在一起。  
- 叉积公式 `x1*y2 - y1*x2` 就像计算两条向量围成的平行四边形面积，矩形是其中一种特殊情况。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 枚举所有点对需要 `n·(n-1)/2 ≈ n²/2` 次。  
  - 对每个 bucket 的两两组合总和仍然是 `O(n²)`（因为每条对角线只能出现在唯一的 bucket 中）。  
  - 与暴力的 `O(n⁴)` 相比，提升了一个量级，能够轻松跑完 50 个点的全部情况。

- **空间复杂度**：`O(n²)`  
  - 哈希表里存放所有点对（约 `n²/2` 条），每条点对只占用常数空间。  
  - 与时间复杂度相匹配，是必需的额外空间。

---

## 心得

- **核心技巧**：利用矩形对角线“中点相同、长度相等”的几何特性，把四点问题转化为两条线段的配对问题。  
- **适用的题型**：  
  1. “任意方向的矩形”或“平行四边形”相关的最小/最大面积/周长问题。  
  2. “找出满足特定几何关系的点对”类题目，如 **Maximum Size Rectangle**、**Largest Triangle Area**。  
  3. “利用哈希把几何特征归类”的问题，如 **Valid Square**、**Number of Boomerangs**。  
- **一句话总结解题钥匙**：**把“矩形”拆成“两个相同的对角线”，用哈希把同类对角线聚在一起，配对即得矩形。**

---

## 反思

- **第一反应**：看到“矩形不一定平行于坐标轴”，立刻想到几何特性——对角线必相等且交于同一点。  
- **最容易踩的坑**  
  1. **浮点误差**：直接用中点的真实坐标 `(x1+x2)/2` 进行哈希会因为 0.5 等小数导致相同的中点被划分到不同的 bucket。解决办法是把中点乘以 2 保存整数。  
  2. **重复点对**：同一条对角线可能被不同的两条点对表示，需要在配对时检查四个点是否互不相同。  
  3. **面积为 0 的退化矩形**：四点共线时叉积为 0，记得在最终答案中返回 `0`（题目要求没有矩形返回 0）。  
- **下次遇到同类题**，第一步应该**寻找可以唯一描述几何形状的特征**（如中点、斜率、长度），并用**哈希表把相同特征的元素归类**，再在同一类内部做组合搜索。这样往往能把指数级的枚举降到多项式级。