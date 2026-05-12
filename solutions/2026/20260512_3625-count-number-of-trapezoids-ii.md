# #3625. 计数梯形的数量 II / Count Number of Trapezoids II

> 难度：困难 · 标签：Array、Hash Table、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/count-number-of-trapezoids-ii/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array points where points[i] = [xi, yi] represents the coordinates of the ith point on the Cartesian plane.
Return the number of unique trapezoids that can be formed by choosing any four distinct points from points.
A trapezoid is a convex quadrilateral with at least one pair of parallel sides. Two lines are parallel if and only if they have the same slope.

**Examples**

**Example 1:**

```
Input: points = [[-3,2],[3,0],[2,3],[3,2],[2,-3]]
Output: 2
Explanation:

There are two distinct ways to pick four points that form a trapezoid:
```

**Example 2:**

```
Input: points = [[0,0],[1,0],[0,1],[2,1]]
Output: 1
Explanation:

There is only one trapezoid which can be formed.
```

**Constraints**

- 4 <= points.length <= 500
- –1000 <= xi, yi <= 1000
- All points are pairwise distinct.

---

## 题目（中文翻译）

给定一个二维整数数组 `points`，其中 `points[i] = [xi, yi]` 表示第 *i* 个点在笛卡尔坐标系中的坐标。  
返回从 `points` 中任选 **四个互不相同的点** 所能构成的 **不同梯形（trapezoid）** 的数量。

梯形（trapezoid）是指 **凸四边形（convex quadrilateral）**，且至少有一对 **平行边（parallel sides）**。两条直线当且仅当它们的 **斜率（slope）** 相同才平行。

---

### 示例 1
**输入**  
``` 
points = [[-3,2],[3,0],[2,3],[3,2],[2,-3]]
```  
**输出**  
```
2
```  
**解释**  

存在两种不同的点的选取方式可以组成梯形：

---

### 示例 2
**输入**  
``` 
points = [[0,0],[1,0],[0,1],[2,1]]
```  
**输出**  
```
1
```  
**解释**  

只能形成一种梯形。

---

### 约束条件
- `4 <= points.length <= 500`
- `-1000 <= xi, yi <= 1000`
- 所有点两两不同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有点的四个组合枚举出来**，检查这四个点能否组成一个梯形。  
具体步骤：

1. 用 `itertools.combinations(points, 4)` 生成所有不重复的四点集合（相当于从点的集合里抽 4 张卡）。
2. 对每一组点，枚举它们的 6 条可能的连线，计算每条线的斜率 `dy/dx`（如果 `dx = 0`，斜率记为 `inf`，即垂直线）。  
   - 斜率的意义可以类比为“这条路和水平线的倾斜程度”。  
3. 判断这 4 条线是否形成**凸四边形**（即没有自相交），并且至少有一对平行的边（斜率相同）。  
   - 两条线平行 ⇔ 斜率相同，这就像字典里查单词：键（斜率）相同的条目就是平行的线。  

只要满足以上条件，就计数 +1。

> **为什么正确？**  
> 枚举了所有可能的四点组合，且每一种组合都完整地检查了“是否是梯形”。因此没有遗漏，也不会误计。

#### 代码（Python）

```python
import itertools
from math import gcd

def slope(p1, p2):
    """返回两点之间的斜率，用 (dy, dx) 的最简整数表示。
       垂直线返回 (1, 0)；水平线返回 (0, 1)。
    """
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]
    if dx == 0:               # 垂直
        return (1, 0)
    if dy == 0:               # 水平
        return (0, 1)
    g = gcd(dy, dx)
    dy //= g
    dx //= g
    # 统一符号：让 dx 为正数，保证唯一表示
    if dx < 0:
        dy, dx = -dy, -dx
    return (dy, dx)

def is_convex_quad(pts):
    """判断四个点是否构成凸四边形（不自交、没有三点共线）。"""
    # 先把点按极角排序，得到逆时针顺序的四边形
    cx = sum(p[0] for p in pts) / 4
    cy = sum(p[1] for p in pts) / 4
    pts = sorted(pts, key=lambda p: (p[0] - cx, p[1] - cy))
    # 计算每条边的叉积，全部同号则为凸
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    signs = []
    for i in range(4):
        c = cross(pts[i], pts[(i + 1) % 4], pts[(i + 2) % 4])
        if c == 0:               # 三点共线，退化
            return False
        signs.append(c > 0)
    return all(signs) or not any(signs)

def brute_count_trapezoids(points):
    """暴力 O(n^4) 解法，返回梯形数量。"""
    ans = 0
    for quad in itertools.combinations(points, 4):
        if not is_convex_quad(quad):
            continue
        # 计算四条边的斜率（不需要区分顺序，只要能找出相同的即可）
        slopes = []
        for i in range(4):
            for j in range(i + 1, 4):
                slopes.append(slope(quad[i], quad[j]))
        # 判断是否至少有一对相同的斜率（即平行边）
        # 用集合计数出现次数
        cnt = {}
        for s in slopes:
            cnt[s] = cnt.get(s, 0) + 1
        if any(v >= 2 for v in cnt.values()):
            ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n⁴)`  
  - 解释：我们遍历所有 `C(n,4) ≈ n⁴/24` 种四点组合，每种组合内部做常数次的几何检查。  
  - 对于 `n = 500`（题目上限），`n⁴` 已经是 **6.25×10¹⁰**，根本跑不完。  
- **空间复杂度**：`O(1)`（只用常数级的临时变量）。  

> **大白话**：`O(n⁴)` 就像让 500 个人每两两组成队，再每支队再两两配对，组合数量会爆炸，根本不现实。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于**枚举所有四点组合**。我们需要把问题拆解为 **只看“平行的两条边”**，而不是整条四边形。  

**关键观察**  

1. **梯形的定义**：只要有 **一对平行的边**，其余两边不需要平行。  
2. 对于一条平行边（我们称为“底”），只要找另一条 **不共享端点**、斜率相同的线段，就能形成 **至少一种梯形**（可能会出现平行四边形的情况，需要后面再处理）。  

因此我们可以：

- 把 **所有点对**（即所有可能的线段）按照它们的 **斜率** 分组。斜率用最简分数 `(dy, dx)` 表示，`dy/dx` 的约分可以用 `gcd` 完成。  
  - 类比：把所有“道路”按“倾斜程度”放进不同的抽屉。  
- 对于同一个斜率抽屉里有 `k` 条线段，任意挑两条 **不相交** 的线段就能当作梯形的两条平行底。  
  - 直接挑两条的组合数是 `C(k,2)`（从 `k` 条线段里挑两条）。  
  - 但如果两条线段 **共用一个端点**，它们根本不是两条独立的底，不能算梯形，需要剔除。  

**如何剔除共点的组合**  

在同一斜率抽屉里，统计每个点出现了多少次（即有多少条线段以该点为端点并且斜率相同）。记为 `cnt[p]`。  
- 对于某个点 `p`，从它的 `cnt[p]` 条线段中挑两条会产生 `C(cnt[p],2)` 组非法组合。  
- 把所有点的非法组合累加后从 `C(k,2)` 中减去，即得到 **合法的平行底对数**。  

**仍然会多算什么？**  

当四个点构成 **平行四边形** 时，它的两对对边都平行。按照上面的统计方式：

- 对于斜率 `s1`，这对平行四边形会贡献一次合法底对。  
- 对于另一条斜率 `s2`，它又会再贡献一次。  

于是 **每个平行四边形被算了两次**，但题目只要求算一次（只要“至少有一对平行边”）。  

**解决办法：计数所有平行四边形并减去一次**  

- 平行四边形的判定可以用 **对角线的中点相同** 的特性：如果两条线段的中点相同，则它们是同一个四边形的两条对角线，且必然是平行四边形。  
- 对所有点对 (i < j) 计算中点 `(xi + xj, yi + yj)`（用整数和避免浮点），放进哈希表 `mid_cnt`。  
- 对于同一个中点出现了 `c` 次，说明有 `C(c,2)` 对不同的对角线，它们恰好构成 `C(c,2)` 个平行四边形。  

最终答案  

```
答案 = Σ_over_slopes [ C(k,2) - Σ_over_points_in_this_slope C(cnt[p],2) ] 
      - Σ_over_midpoints C(c,2)
```

这整个过程只遍历 **所有点对**（约 `n²/2`），因此时间是 `O(n²)`，空间同样是 `O(n²)`（用于哈希表）。

#### 代码（Python）

```python
from math import gcd
from collections import defaultdict

def normalized_slope(p1, p2):
    """返回两点的最简斜率 (dy, dx) ，统一 dx>0 的表示方式。"""
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]
    if dx == 0:               # 垂直线统一为 (1,0)
        return (1, 0)
    if dy == 0:               # 水平线统一为 (0,1)
        return (0, 1)
    g = gcd(dy, dx)
    dy //= g
    dx //= g
    # 让 dx 为正，保证唯一性（比如 (-1, -2) -> (1,2)）
    if dx < 0:
        dy, dx = -dy, -dx
    return (dy, dx)

def count_trapezoids(points):
    n = len(points)
    # 1️⃣ 统计每条斜率的所有线段以及每条线段对应的端点出现次数
    slope_to_segments = defaultdict(list)   # slope -> list of (i, j)
    point_cnt_in_slope = defaultdict(lambda: defaultdict(int))
    for i in range(n):
        for j in range(i + 1, n):
            s = normalized_slope(points[i], points[j])
            slope_to_segments[s].append((i, j))
            point_cnt_in_slope[s][i] += 1
            point_cnt_in_slope[s][j] += 1

    # 2️⃣ 计算“合法的平行底对数” —— 不共享端点的两条线段
    total_parallel_pairs = 0
    for s, segs in slope_to_segments.items():
        k = len(segs)                     # 该斜率下的线段总数
        if k < 2:
            continue
        # 所有两两组合 C(k,2)
        pairs = k * (k - 1) // 2
        # 减去共点的非法组合
        for cnt in point_cnt_in_slope[s].values():
            if cnt >= 2:
                pairs -= cnt * (cnt - 1) // 2
        total_parallel_pairs += pairs

    # 3️⃣ 统计平行四边形的个数（对角线中点相同）
    mid_cnt = defaultdict(int)           # (x_sum, y_sum) -> 出现次数
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            # 用坐标和代替中点，避免出现小数
            mid = (xi + xj, yi + yj)
            mid_cnt[mid] += 1

    parallelogram = 0
    for c in mid_cnt.values():
        if c >= 2:
            parallelogram += c * (c - 1) // 2   # C(c,2)

    # 4️⃣ 最终答案：合法底对数 - 多算的平行四边形
    return total_parallel_pairs - parallelogram
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：我们遍历所有点对两次（一次算斜率，一次算中点），每次都是 `n·(n-1)/2`，即约 `n²/2` 次操作。  
  - 与暴力的 `O(n⁴)` 相比，**从十亿级别直接降到几万级别**，轻松跑完 `n = 500`。  

- **空间复杂度**：`O(n²)`  
  - 需要存储每条线段的斜率分组以及中点计数。对 `n = 500` 而言，大约是 `125,000` 条记录，完全可以放进内存。  

> **对比**：暴力是“把每个人的所有可能组合都列出来”，最优解是“只关心每两个人之间的关系（斜率 / 中点）”，大幅削减了不必要的枚举。

---

## 心得  

- **核心技巧**：**把几何问题转化为“离散的哈希计数”**。  
  - 斜率归一化 + 哈希表 → 快速找到所有平行的线段。  
  - 对角线中点相同 → 快速统计平行四边形。  

- **该技巧适用的题型**  
  1. “统计满足某种相同属性的点对”——如 **共线点对**、**等距点对**。  
  2. “利用中点/向量/斜率唯一标识特定图形”——如 **矩形计数**、**等腰三角形计数**。  
  3. “把几何关系抽象成离散的键值对”——如 **点对间的曼哈顿距离相等** 等。  

- **一句话总结解题钥匙**  
  > **把“平行”或“等长”等连续的几何关系离散化为哈希键，然后用组合数学快速计数**。

---

## 反思  

- **第一反应**：看到“梯形”立刻想到枚举四点并逐个判定。  
- **最容易踩的坑**  
  1. **斜率的归一化**：如果不把 `(2,4)` 与 `(1,2)` 统一，会把本来平行的线段分到不同的桶里，导致计数错误。  
  2. **共点线段的剔除**：仅靠 `C(k,2)` 会把共享端点的组合也算进去，需要额外减去。  
  3. **平行四边形的双计**：忘记对平行四边形做一次补偿，会把答案高出一倍。  
  4. **中点的表示**：使用浮点会产生精度误差，采用整数坐标和 `(x1+x2, y1+y2)` 才安全。  

- **下次遇到同类题**  
  - **第一步**：把几何关系（平行、相等、垂直等）抽象成**离散的键**（斜率、向量、长度、坐标和等），并用哈希表统计出现次数。  
  - **第二步**：用**组合公式** `C(cnt,2)` 计算可能的配对数，再逐一排除因共点或其他约束导致的非法配对。  
  - **第三步**：检查是否有**重复计数的结构**（如平行四边形、矩形），找出唯一的特征（如对角线中点）再做一次补偿。