# #149. 直线上最多的点数 / Max Points on a Line

> 难度：困难 · 标签：Array、Hash Table、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/max-points-on-a-line/)

---

## 题目（英文原版）

**Description**

Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.

**Examples**

**Example 1:**

```
Input: points = [[1,1],[2,2],[3,3]]
Output: 3
```

**Example 2:**

```
Input: points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
Output: 4
```

**Constraints**

- 1 <= points.length <= 300
- points[i].length == 2
- -104 <= xi, yi <= 104
- All the points are unique.

---

## 题目（中文翻译）

给定一个点的数组（array），其中 `points[i] = [xi, yi]` 表示 X‑Y 平面（X‑Y plane）上的一个点（point），返回位于同一直线（straight line）上的点的最大数量（maximum number）。

## 示例

### 示例 1
**输入:** `points = [[1,1],[2,2],[3,3]]`  
**输出:** `3`

### 示例 2
**输入:** `points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]`  
**输出:** `4`

## 约束条件
- `1 <= points.length <= 300`
- `points[i].length == 2`
- `-10^4 <= xi, yi <= 10^4`
- 所有点均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**任取两点**，它们唯一决定一条直线。随后把所有其余点一个一个地检查，看看是否也在这条直线上。  

- **数据结构**：我们只需要 **数组**（存放点）和 **计数器**（统计同一直线上的点数）。  
- **生活化类比**：把每条直线想象成一根绳子，先用两颗珠子（两点）把绳子拉直，然后把其它珠子一个一个放到绳子上，能放上的就是共线的。  
- **为什么正确**：任意两点一定能唯一确定一条直线；如果所有点都在这条直线上，那么这条直线必然会被我们枚举到。遍历所有可能的两点组合，必然能找到包含最多点的那条直线。  

**时间/空间复杂度**  
- 外层两层循环遍历「所有点对」是 `O(n²)`（n 为点的数量）。  
- 对每一条直线，我们再遍历一次全部点来计数，时间是 `O(n)`。  
- 综合下来总共是 `O(n³)`，也就是**立方级别**的时间——如果 n=300，最坏会执行 27,000,000 次基本操作，已经比较慢了。  
- 只用了几个计数器和临时变量，空间是 `O(1)`（常数级），几乎不占额外内存。

#### 代码（Python）  

```python
from typing import List

def max_points_brute(points: List[List[int]]) -> int:
    """暴力解：枚举每条直线，统计其上点的个数"""
    n = len(points)
    if n <= 2:                     # 0、1、2 个点必然在同一直线上
        return n

    # 判断三点 (x1,y1)、(x2,y2)、(x3,y3) 是否共线的公式：
    # (y2 - y1)*(x3 - x1) == (y3 - y1)*(x2 - x1)
    def collinear(p1, p2, p3) -> bool:
        return (p2[1] - p1[1]) * (p3[0] - p1[0]) == \
               (p3[1] - p1[1]) * (p2[0] - p1[0])

    ans = 0
    # 枚举所有点对 (i, j)，i < j
    for i in range(n):
        for j in range(i + 1, n):
            cnt = 2                 # 这条直线至少包含 i、j 两点
            for k in range(n):
                if k == i or k == j:
                    continue
                if collinear(points[i], points[j], points[k]):
                    cnt += 1        # 第 k 点也在同一直线上
            ans = max(ans, cnt)     # 维护最大值
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 立方级别。可以把它想成「三层循环」：先挑两颗珠子，再把所有珠子逐个放上去。  
- **空间复杂度**：`O(1)` —— 只用了少量计数器，和输入规模无关。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈** 在于每次都要遍历全部点来计数。我们可以把计数的工作 **提前**，在一次遍历里就完成。  

**核心想法**：对每一个点 `i`，把它当作「锚点」；计算它与其它每一点 `j` 的斜率（倾斜程度），相同斜率的点必然在同一直线上。于是只要统计「同一斜率出现了多少次」即可得到以 `i` 为起点的最大共线点数。  

- **为什么这样更快**：对每个锚点，我们只需要一次 `O(n)` 的遍历来建立斜率映射，然后再取最大计数。整个过程是 `n` 次 `O(n)`，即 `O(n²)`。不再需要第三层循环。  
- **需要的工具**：  
  1. **哈希表（字典）**：把斜率当作「键」存进去，出现次数当作「值」。字典就像一本**查字典**，词（斜率）对应的页码（计数）告诉我们这条直线上有多少点。  
  2. **斜率的标准化**：直接用浮点数会产生精度误差。我们把斜率写成最简分数 `dy/gcd, dx/gcd`（分子/分母），并统一处理符号，使 `(-1,2)` 与 `(1,-2)` 视为同一斜率。  
  3. **特殊情况**：  
     - **垂直线**（dx = 0）没有斜率，用一个单独的计数 `vertical` 记录。  
     - **重合点**（同一点出现多次）在本题中不存在（题目保证点唯一），但在更通用的实现里会用 `overlap` 计数。  

**类比**：想象你站在一座高塔上（锚点），向四面八方发射激光束。每一束激光对应一种斜率。所有在同一束激光上的点都在同一直线上。我们只需要找出哪束激光射中了最多的点。

#### 代码（Python）  

```python
from typing import List
from math import gcd

def max_points(points: List[List[int]]) -> int:
    """最优解：以每个点为锚点，利用哈希表统计斜率出现次数"""
    n = len(points)
    if n <= 2:                     # 0、1、2 个点必然共线
        return n

    ans = 0
    for i in range(n):
        slopes = {}                # key: (dy, dx) 的最简分数，value: 出现次数
        vertical = 0               # 记录垂直线（dx == 0）的点数
        # overlap = 0              # 本题不需要，但若出现相同点可用

        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            dx = xj - xi
            dy = yj - yi

            if dx == 0 and dy == 0:
                # 重合点（本题不会出现），如果出现则计数 overlap
                # overlap += 1
                continue

            if dx == 0:            # 垂直线
                vertical += 1
                continue

            # 把斜率化成最简分数，保证分母为正
            g = gcd(dy, dx)
            dy //= g
            dx //= g
            if dx < 0:            # 让分母保持正数，统一符号
                dy = -dy
                dx = -dx

            key = (dy, dx)
            slopes[key] = slopes.get(key, 0) + 1

        # 当前锚点能形成的最大共线点数（加上锚点本身）
        local_max = vertical
        if slopes:
            local_max = max(local_max, max(slopes.values()))
        ans = max(ans, local_max + 1)   # +1 是把锚点 itself 加进去

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环：外层遍历每个锚点 `n` 次，内层遍历它后面的点 `≈ n/2` 次。整体相当于「遍历所有点对」一次，比暴力的三层循环快了一个量级。  
- **空间复杂度**：`O(n)` —— 对每个锚点我们都要维护一个哈希表，最坏情况下会存储 `n-1` 条不同的斜率。随着锚点的移动，这个表会被重新创建，所以最大额外空间是线性级别。  

---

## 心得  

- **核心技巧**：**以点为锚点，统计斜率的出现次数**（哈希表 + 斜率标准化）。  
- **适用的题型**：  
  1. **共线点/共面点** 类似题目（如 “Max Points on a Line”）。  
  2. **同一斜率的子数组**（如 “Longest Arithmetic Subsequence”）。  
  3. **点对之间的相对关系**（如 “Number of Boomerangs”）。  
- **一句话总结解题钥匙**：**把几何问题转化为“斜率相等的计数”，用哈希表快速汇总**。

---

## 反思  

- **第一反应**：看到“直线”就想到两点唯一确定直线，于是想到枚举所有点对。  
- **最容易踩的坑**：  
  - 直接使用浮点数比较斜率会出现精度误差，导致同一条直线被误判为不同。  
  - 竖直线的斜率是无穷大，需要单独计数。  
  - 负数斜率的符号统一（分母为正）是必须的，否则 `(1, -2)` 与 `(-1, 2)` 会被误当成两条不同直线。  
- **下次类似题的第一步**：**先把几何关系抽象成“比例相等”或“差值相等”，找出可以用哈希表计数的特征（斜率、差值、方向向量）**。这样就能快速从暴力枚举跳到 `O(n²)` 的高效解。