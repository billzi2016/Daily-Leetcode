# #3588. 寻找三角形的最大面积 / Find Maximum Area of a Triangle

> 难度：中等 · 标签：Array、Hash Table、Math、Greedy、Geometry、Enumeration · [LeetCode 链接](https://leetcode.com/problems/find-maximum-area-of-a-triangle/)

---

## 题目（英文原版）

**Description**

You are given a 2D array coords of size n x 2, representing the coordinates of n points in an infinite Cartesian plane.
Find twice the maximum area of a triangle with its corners at any three elements from coords, such that at least one side of this triangle is parallel to the x-axis or y-axis. Formally, if the maximum area of such a triangle is A, return 2 * A.
If no such triangle exists, return -1.
Note that a triangle cannot have zero area.

**Examples**

**Example 1:**

```
Input: coords = [[1,1],[1,2],[3,2],[3,3]]
Output: 2
Explanation:

The triangle shown in the image has a base 1 and height 2. Hence its area is 1/2 * base * height = 1 .
```

**Example 2:**

```
Input: coords = [[1,1],[2,2],[3,3]]
Output: -1
Explanation:
The only possible triangle has corners (1, 1) , (2, 2) , and (3, 3) . None of its sides are parallel to the x-axis or the y-axis.
```

**Constraints**

- 1 <= n == coords.length <= 105
- 1 <= coords[i][0], coords[i][1] <= 106
- All coords[i] are unique.

---

## 题目（中文翻译）

**描述**  
给定一个大小为 `n x 2` 的二维数组 `coords`，其中每行表示平面上一个点的坐标。  
求任意选取 `coords` 中的三个点构成的三角形的 **最大面积的两倍**，且该三角形至少有一条边平行于 **x 轴** 或 **y 轴**。形式化地，如果满足条件的最大面积为 `A`，返回 `2 * A`。  
如果不存在满足条件的三角形，返回 `-1`。  
注意，三角形的面积不能为零。

**示例 1**  
```
Input: coords = [[1,1],[1,2],[3,2],[3,3]]
Output: 2
```
**解释**：  
如图所示的三角形的底为 `1`，高为 `2`。因此面积为 `1/2 * 底 * 高 = 1`，返回的值为 `2 * 1 = 2`。

**示例 2**  
```
Input: coords = [[1,1],[2,2],[3,3]]
Output: -1
```
**解释**：  
唯一可能的三角形的三个顶点为 `(1, 1)`、`(2, 2)`、`(3, 3)`，但它的任意一条边都不平行于 **x 轴** 或 **y 轴**，因此返回 `-1`。

**约束条件**  
- `1 <= n == coords.length <= 10^5`  
- `1 <= coords[i][0], coords[i][1] <= 10^6`  
- 所有 `coords[i]` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的三点组合都枚举一遍**，然后判断这三个点能否组成满足“至少有一条边平行于坐标轴”的三角形，若可以就算出它的面积（题目要求返回 `2 * area`，即 `base * height`），最后取最大的那个。

- **数据结构**：我们只需要把坐标保存在一个普通的列表 `coords` 中，遍历时直接取下标即可。  
  - 可以把 “哈希表” 想象成 **一本查字典的工具书**，key 是要找的词，value 是对应的解释。这里我们不需要哈希表，只是把所有点当成“词”，直接遍历。

- **为什么正确**：因为我们枚举了 **所有** 三点组合，必然不会漏掉最优解。只要在每一次枚举中正确判断是否满足平行条件并计算面积，就一定能得到正确答案。

- **复杂度分析**：  
  - 枚举三点的方式是 `C(n,3) ≈ n³ / 6`，所以时间复杂度是 **O(n³)**。  
  - 只用了常数级的额外空间（几个循环变量），空间复杂度是 **O(1)**。  
  - 对于 `n` 最高可达 `10⁵` 的情况下，`n³` 完全不可接受——这就是暴力解的瓶颈。

> **大白话解释**：  
> - `O(n³)` 可以想象成“把 1000 个人每三个人凑一桌，看看每桌的情况”。当人数是 10⁵ 时，桌子数量天文数字，根本不可能坐完。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def maxTriangleArea_bruteforce(coords: List[List[int]]) -> int:
    """
    暴力枚举所有三点组合，返回 2 * 最大面积（或 -1）
    """
    max_twice_area = -1  # 用 -1 表示还没有合法三角形

    # 逐个枚举三点组合，combinations 会自动生成所有不重复的三元组
    for (x1, y1), (x2, y2), (x3, y3) in combinations(coords, 3):
        # 判断是否有一条边水平或垂直
        # 1) (x1,y1)-(x2,y2) 平行于 x 轴：y1 == y2
        # 2) (x1,y1)-(x2,y2) 平行于 y 轴：x1 == x2
        # 其余两条边同理
        parallel = (
            y1 == y2 or x1 == x2 or
            y1 == y3 or x1 == x3 or
            y2 == y3 or x2 == x3
        )
        if not parallel:
            continue          # 这三点不满足题目要求，直接跳过

        # 计算三角形面积的两倍：base * height
        # 只要找出哪条平行边是底（base），另一条坐标的差就是高（height）
        # 为了简单，这里直接用向量叉积公式：| (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1) |
        # 结果正好是 2 * area
        twice_area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        if twice_area == 0:   # 零面积的退化三角形不算
            continue
        max_twice_area = max(max_twice_area, twice_area)

    return max_twice_area
```

#### 复杂度

- **时间复杂度**：`O(n³)` —— 需要遍历所有三点组合，随着 `n` 的增长会非常慢。  
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量，不会随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们把所有三点都枚举了，而实际上只需要关注 **满足平行条件的两点**（它们决定底边），再找一个合适的第三点来形成最大高度。

**关键观察**：

1. **底边一定在同一条水平线（y 相同）或同一条垂直线（x 相同）**。  
   - 把“底边平行于 x 轴”想象成“在同一条水平道路上跑”，只要两辆车（点）在同一条道路（相同的 y）上，它们之间的距离就是底的长度。  
   - 同理，“底边平行于 y 轴”就是在同一根竖直的柱子（相同的 x）上。

2. **在同一条水平线上**，要让底（`base`）尽可能长，只需要取 **最左** 与 **最右** 两个点的 `x` 差值。  
   - 因此，只要知道每条 y 对应的最小 x、最大 x 即可得到该 y 的最大底。

3. **高度（`height`）** 是指第三点到这条底所在的水平线（或垂直线）的垂直距离。  
   - 对于固定的 `y`（水平底），高度只和 **全局最高点的 y** 与 **全局最低点的 y** 有关。取离当前 y 最远的那一个即可得到最大可能的高度。  
   - 同理，固定 `x`（垂直底）时，高度取全局最左或最右的 x 差值。

4. **只要底边长度 > 0 且高度 > 0**，就能组成合法的三角形（面积非零）。  
   - 所以我们只需要遍历所有 **有至少两个点的 y（或 x）**，计算 `base * height`，取最大值。

**实现步骤**：

- 第一步：遍历所有点，收集三类信息  
  - `y -> [x1, x2, …]`（同一水平线上的所有 x）  
  - `x -> [y1, y2, …]`（同一垂直线上的所有 y）  
  - 全局最小/最大 `x` 与 `y`（用于求高度）

- 第二步：对每个 `y`（如果该 y 上的点数 ≥ 2）  
  - `base = max_x_on_y - min_x_on_y`  
  - `height = max(y - global_min_y, global_max_y - y)`  
  - 更新答案 `ans = max(ans, base * height)`

- 第三步：对每个 `x`（如果该 x 上的点数 ≥ 2）同理处理。

- 最后：如果 `ans` 仍为 0，说明没有满足条件的三角形，返回 `-1`；否则返回 `ans`（已经是 `2 * area`）。

**为什么是最优**：

- 只遍历 **一次** 所有点建立哈希表（O(n)），再遍历哈希表的键（每个键对应的点数之和仍是 O(n)），所以整体时间是 **O(n)**。  
- 只保存每条线的最小/最大坐标，空间是 **O(n)**（最坏情况下每个点的 x、y 都不相同，需要各自的键），但相较于 `n = 10⁵` 仍然可以接受。

> **类比**：  
> 把所有点想象成城市的交叉口，`y` 对应“同一条东西向的街道”，我们只关心这条街上最左和最右的交叉口（因为它们能撑起最长的底），而高度则是找离这条街最远的“南北向的街道”。这样只要把每条街的两端记下来，就能瞬间算出最长的“底 * 高”。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maxTriangleArea(coords: List[List[int]]) -> int:
    """
    O(n) 最优解
    返回 2 * 最大面积（若不存在返回 -1）
    """
    if len(coords) < 3:
        return -1

    # 1. 收集信息
    xs_on_y = defaultdict(list)   # y -> 所有在该 y 上的 x
    ys_on_x = defaultdict(list)   # x -> 所有在该 x 上的 y

    min_x = min_y = 10**9
    max_x = max_y = -10**9

    for x, y in coords:
        xs_on_y[y].append(x)
        ys_on_x[x].append(y)

        # 同时更新全局最值，供后面求高度使用
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y

    ans = 0  # 记录最大的 2 * area

    # 2. 处理水平底（同一 y）
    for y, xs in xs_on_y.items():
        if len(xs) < 2:          # 需要至少两点才能构成底
            continue
        base = max(xs) - min(xs)  # 最左和最右的 x 差
        # 高度取离当前 y 最远的全局 y
        height = max(y - min_y, max_y - y)
        if height > 0:            # 必须保证高度不为 0，才能得到非退化三角形
            ans = max(ans, base * height)

    # 3. 处理垂直底（同一 x）
    for x, ys in ys_on_x.items():
        if len(ys) < 2:
            continue
        base = max(ys) - min(ys)  # 最上和最下的 y 差
        height = max(x - min_x, max_x - x)
        if height > 0:
            ans = max(ans, base * height)

    return ans if ans != 0 else -1
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次遍历收集信息是 `O(n)`，随后遍历所有不同的 `y` 与 `x`（它们的数量不超过 `n`）也是线性，整体是线性时间。  
  - 与暴力解的 `O(n³)` 相比，速度提升了 **指数级**，在 `n = 10⁵` 时可以轻松跑完。

- **空间复杂度**：`O(n)`  
  - 需要两个哈希表 `xs_on_y`、`ys_on_x`，最坏情况下每个点都有唯一的 `x` 与 `y`，所以总共存储 `2n` 个整数，仍然是线性空间。  
  - 对于本题的约束（`n ≤ 10⁵`），完全可以接受。

---

## 心得

- **核心技巧**：**利用同一水平/垂直线上点的极值（最左/最右、最高/最低）来快速求最大底和最大高**，并结合全局极值求高度。  
- **适用的题型**：  
  1. “在平面上找满足某种坐标约束的最大/最小几何量”，例如 **最大矩形面积**（两点同 x、两点同 y）。  
  2. “需要用到极值/前缀/后缀信息快速求解”，如 **最大 Manhattan 距离**、**最大面积的矩形**（LeetCode 85）。  
  3. 任何可以把问题拆成“固定一条直线，再找离它最远的点”的几何题目。

- **一句话总结解题钥匙**：  
  > “把所有点按相同的 x 或 y 分组，**只保留每组的最左/最右（或最高/最低）**，再结合全局最值即可在 **O(n)** 内算出最大底 × 高。”

---

## 反思

- **第一反应**：看到“至少有一条边平行于坐标轴”，立刻想到“找相同 x 或相同 y 的点”。于是想到把点按行/列分组，这是突破口。  
- **最容易踩的坑**：  
  - **高度为 0**：即所有点都在同一条水平线或同一条垂直线上，此时只能得到退化三角形，需要返回 `-1`。  
  - **只两点同 x（或 y）但没有第三点**：同样需要检查 `height > 0`。  
  - **全局极值恰好在同一条线上**：比如最高点恰好也在当前的水平线上，这时 `height` 计算会得到 0，需要用 `max(y - min_y, max_y - y)` 正确处理。  
- **下次遇到同类题**，第一步应该：  
  1. **把约束转化为“相同坐标的点构成基线”**，  
  2. **统计每条基线的极值**（最左/最右或最高/最低），  
  3. **利用全局极值求出对应的最大高度**，再做乘积比较。这样思路清晰，代码也自然简洁。