# #2249. 圆内格点计数 / Count Lattice Points Inside a Circle

> 难度：中等 · 标签：Array、Hash Table、Math、Geometry、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-lattice-points-inside-a-circle/)

---

## 题目（英文原版）

**Description**

Given a 2D integer array circles where circles[i] = [xi, yi, ri] represents the center (xi, yi) and radius ri of the ith circle drawn on a grid, return the number of lattice points that are present inside at least one circle.
Note:

**Examples**

**Example 1:**

```
Input: circles = [[2,2,1]]
Output: 5
Explanation:
The figure above shows the given circle.
The lattice points present inside the circle are (1, 2), (2, 1), (2, 2), (2, 3), and (3, 2) and are shown in green.
Other points such as (1, 1) and (1, 3), which are shown in red, are not considered inside the circle.
Hence, the number of lattice points present inside at least one circle is 5.
```

**Example 2:**

```
Input: circles = [[2,2,2],[3,4,1]]
Output: 16
Explanation:
The figure above shows the given circles.
There are exactly 16 lattice points which are present inside at least one circle. 
Some of them are (0, 2), (2, 0), (2, 4), (3, 2), and (4, 4).
```

**Constraints**

- 1 <= circles.length <= 200
- circles[i].length == 3
- 1 <= xi, yi <= 100
- 1 <= ri <= min(xi, yi)

---

## 题目（中文翻译）

给定一个二维整数数组 `circles`，其中 `circles[i] = [xi, yi, ri]` 表示第 *i* 个圆（circle）的中心 `(xi, yi)` 和半径 `ri`，求至少被一个圆覆盖的格点（lattice point）的数量。

---

## 示例

### 示例 1
**输入:** `circles = [[2,2,1]]`  
**输出:** `5`  
**解释:**  
上图展示了给定的圆。圆内的格点为 `(1, 2)`, `(2, 1)`, `(2, 2)`, `(2, 3)`, `(3, 2)`，在图中用绿色标出。  
而 `(1, 1)`、`(1, 3)` 等点（图中红色）不算在圆内。  
因此，至少被一个圆覆盖的格点数量为 **5**。

### 示例 2
**输入:** `circles = [[2,2,2],[3,4,1]]`  
**输出:** `16`  
**解释:**  
上图展示了两个圆。恰好有 16 个格点位于至少一个圆内部，例如 `(0, 2)`, `(2, 0)`, `(2, 4)`, `(3, 2)`, `(4, 4)` 等。

---

## 约束条件

- `1 <= circles.length <= 200`
- `circles[i].length == 3`
- `1 <= xi, yi <= 100`
- `1 <= ri <= min(xi, yi)`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把**所有可能的格点**（即整数坐标点）都枚举一遍，然后逐个检查它们是否落在**任意一个圆**内部。  

- **枚举范围**：题目给出的坐标 `xi, yi ≤ 100`，半径 `ri ≤ min(xi, yi)`，所以最左、最右、最上、最下的格点不会超过 `0 … 200`（因为最左可能是 `xi - ri`，最右可能是 `xi + ri`）。我们可以把整个平面当成一个 0~200 的网格，遍历所有 `(x, y)`。
- **判断是否在圆内**：一个格点 `(x, y)` 在圆心 `(xc, yc)`、半径 `r` 的圆里，当且仅当  
  \[
  (x - xc)^2 + (y - yc)^2 \le r^2
  \]  
  这就像“查字典”——把 `(x - xc)^2 + (y - yc)^2` 当作“键”，`r^2` 当作“页码”，只要键不大于页码，就说明在字典里（即在圆内）。
- **去重**：同一个格点可能被多个圆覆盖。我们可以把已经找到的格点放进**哈希表**（在 Python 里用 `set`），相当于记下这本字典已经翻到哪一页，避免重复计数。

为什么这个方法一定对？因为我们把所有可能的格点都检查了一遍，凡是满足圆的判定式的点必然被记录下来，且不遗漏。

**复杂度直观解释**：  
- **时间复杂度**：我们遍历了大约 `201 × 201 ≈ 4·10⁴` 个格点，对每个格点最多要检查 200 个圆。于是最坏情况是 `4·10⁴ × 200 = 8·10⁶` 次基本运算。用大 O 记作 `O(范围 × 圆的个数)`，即 `O( (max_coord)² · n )`，这里 `max_coord ≈ 200`，`n ≤ 200`。可以把它想象成“把一张 200×200 的棋盘的每格都检查一次，再对每格看 200 次”。
- **空间复杂度**：我们只用一个 `set` 存放格点坐标，最多不超过所有格点的数量，即 `O((max_coord)²)`，约 `4·10⁴` 个元素。相当于在纸上记下最多 4 万个格子的“是否被圆覆盖”。

#### 代码（Python）

```python
from typing import List, Set, Tuple

def countLatticePoints_bruteforce(circles: List[List[int]]) -> int:
    # 1. 计算所有格点的搜索范围
    # 由于 xi, yi <= 100, ri <= xi,yi, 最左/右/上/下不会超过 0~200
    min_x, max_x = 0, 200
    min_y, max_y = 0, 200

    inside: Set[Tuple[int, int]] = set()          # 哈希表，存放已确认在圆内的格点

    # 2. 枚举每一个格点
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # 3. 检查它是否落在任意一个圆里
            for xc, yc, r in circles:
                # 判定式：距离平方 <= 半径平方
                if (x - xc) ** 2 + (y - yc) ** 2 <= r ** 2:
                    inside.add((x, y))           # 加入集合，自动去重
                    break                        # 已经在某圆内，无需继续检查其他圆

    # 4. 集合大小即为答案
    return len(inside)
```

#### 复杂度

- **时间复杂度**：`O((max_coord)² · n)` ≈ `O(200²·200) = O(8·10⁶)`。  
  *含义*：把整个 200×200 的棋盘每格都检查一次，每格最多看 200 次圆，算起来大概几百万次运算，电脑几毫秒就能跑完。
- **空间复杂度**：`O((max_coord)²)` ≈ `O(4·10⁴)`。  
  *含义*：最多记下四万条格点坐标，放在集合里，占用的内存和棋盘大小成正比。

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于我们把所有格点（包括很多根本不可能落在圆里的点）都遍历了一遍。实际上，**每个圆只会覆盖它的外接正方形内部的格点**，而外面的格点肯定不需要检查。我们可以利用这一点大幅削减搜索空间。

**优化步骤**：

1. **只在圆的外接正方形里枚举**  
   对于圆心 `(xc, yc)`、半径 `r`，格点的 `x` 只能在 `[xc - r, xc + r]` 之间。于是我们把 `x` 的循环范围直接收窄到这段，而不是 0~200。

2. **利用圆的对称性，计算 y 的取值范围**  
   给定一个 `x`，横向距离 `dx = x - xc` 已知，圆内的点满足  
   \[
   dx^2 + dy^2 \le r^2 \quad\Longrightarrow\quad dy^2 \le r^2 - dx^2
   \]  
   于是 `dy` 的最大整数值是 `⌊√(r² - dx²)⌋`（向下取整），对应的 `y` 只能在 `[yc - dy, yc + dy]`。这一步相当于“先算出这根竖线能伸多高”，只在这根竖线上枚举格点。

3. **同样用集合去重**  
   多个圆仍可能重叠，使用 `set` 记录已经统计过的格点即可。

这样做的好处是：**每个格点只会被它所在的圆实际覆盖的区域枚举一次**，而不是遍历整个大棋盘。时间复杂度降到 **所有圆内部格点的总数**，在最坏情况下仍然是 `O(π·r²·n)`，但常数更小，实际运行会快很多。

> **核心概念——前缀平方根**  
> 计算 `dy = int(math.isqrt(r*r - dx*dx))` 时用到了整数开方 `isqrt`，它相当于把“平方根再向下取整”这件事交给计算机一次性完成，避免了浮点数误差。

#### 代码（Python）

```python
import math
from typing import List, Set, Tuple

def countLatticePoints_opt(circles: List[List[int]]) -> int:
    inside: Set[Tuple[int, int]] = set()   # 用来去重

    for xc, yc, r in circles:
        # 只在外接正方形的 x 范围遍历
        for x in range(xc - r, xc + r + 1):
            dx = x - xc
            # 计算对应的最大 dy（向下取整的整数平方根）
            dy = int(math.isqrt(r * r - dx * dx))
            # 在 y 范围内全部加入集合
            for y in range(yc - dy, yc + dy + 1):
                inside.add((x, y))

    return len(inside)
```

**代码要点注释**：

- `math.isqrt`：返回非负整数的整数平方根，等价于 `int(math.sqrt(...))` 但不会产生浮点误差。
- `range(xc - r, xc + r + 1)`：左闭右开区间，确保把外接正方形的边界格点全部包含进去。
- `inside.add((x, y))`：集合自动去重，即使同一点被多个圆覆盖也只计一次。

#### 复杂度  

- **时间复杂度**：`O( Σ_{i=1}^{n} (π·ri²) )`，即所有圆内部格点的总数。  
  *含义*：我们只遍历真正可能出现的格点，数量大约等于圆的面积（π·r²）乘以圆的个数。相较于暴力的 `O(200²·n)`，这里的常数更小，实际运行更快。
- **空间复杂度**：`O( Σ_{i=1}^{n} (π·ri²) )`，因为集合里存的正是这些格点。  
  *含义*：最坏情况下所有圆不重叠，集合大小等于所有圆内部格点的总数。

---

## 心得  

- **核心技巧**：**利用几何约束把搜索空间收紧**（外接正方形 + 纵向最大偏移），并用 **哈希表去重**。  
- **适用场景**：  
  1. **点在圆/椭圆/扇形内部**的计数问题。  
  2. **网格上求满足距离约束的点集合**（如“曼哈顿距离 ≤ k 的格点”）。  
  3. **多形状覆盖计数**（如多个矩形、菱形的覆盖点数）。  
- **一句话总结解题钥匙**：**“先把范围收窄到必然可能的区域，再用集合防止重复”。**

---

## 反思  

- **第一反应**：直接把整个坐标平面遍历一遍，然后对每个点检查所有圆。  
- **最容易踩的坑**：  
  - **边界遗漏**：`range` 的左闭右开要记得 `+1`，否则最右/上边界的格点会被漏掉。  
  - **整数平方根误差**：使用 `math.isqrt` 而不是 `math.sqrt` 转 `int`，防止 `sqrt(9)` 变成 `2.999999…` 导致 `dy` 少算 1。  
  - **集合去重**：忘记使用集合会导致同一点被多次计数，答案会偏大。  
- **下次类似题的第一步**：**先算出每个几何体的最小包围盒**（外接矩形/正方形），只在这些盒子内部遍历；随后**用数学关系（如勾股定理）进一步限制第二维的取值范围**。这样可以把暴力的 “全局遍历” 变成 “局部精准遍历”。