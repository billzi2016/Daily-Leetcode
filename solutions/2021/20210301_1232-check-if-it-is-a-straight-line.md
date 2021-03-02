# #1232. 判断是否在同一直线上 / Check If It Is a Straight Line

> 难度：简单 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/check-if-it-is-a-straight-line/)

---

## 题目（英文原版）

**Description**

You are given an array coordinates, coordinates[i] = [x, y], where [x, y] represents the coordinate of a point. Check if these points make a straight line in the XY plane.

**Examples**

**Example 1:**

```
Input: coordinates = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]
Output: true
```

**Example 2:**

```
Input: coordinates = [[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]
Output: false
```

**Constraints**

- 2 <= coordinates.length <= 1000
- coordinates[i].length == 2
- -10^4 <= coordinates[i][0], coordinates[i][1] <= 10^4
- coordinates contains no duplicate point.

---

## 题目（中文翻译）

给定一个数组 `coordinates`，其中 `coordinates[i] = [x, y]` 表示一点的坐标 `[x, y]`。请判断这些点在 XY 平面上是否共线（即是否在同一直线上）。

## 示例

### 示例 1
**输入:** `coordinates = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]`  
**输出:** `true`

### 示例 2
**输入:** `coordinates = [[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]`  
**输出:** `false`

## 约束条件

- `2 <= coordinates.length <= 1000`
- `coordinates[i].length == 2`
- `-10^4 <= coordinates[i][0], coordinates[i][1] <= 10^4`
- `coordinates` 中不存在重复的点。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**只要所有点的斜率都相同，它们就在同一直线上**。  
- **斜率** = (y₂‑y₁) / (x₂‑x₁)。可以把斜率想象成“爬坡的陡度”，如果每段路的陡度都一样，说明整条路是一条直线。  
- 我们先取前两个点 `p0 = (x0, y0)`、`p1 = (x1, y1)`，算出它们的斜率 `k = (y1‑y0)/(x1‑x0)`（注意分母可能为 0，表示竖直线）。  
- 然后遍历剩下的每个点 `pi = (xi, yi)`，把它们和 `p0` 的斜率也算出来，和 `k` 比较。只要有一个不相等，就说明不是直线。  

> **为什么正确？**  
> 两点唯一确定一条直线；如果第三点与前两点的斜率相同，说明它也落在这条直线上。把这个过程对所有点都检查一次，就能确保所有点共线。  

> **时间/空间复杂度**  
> - **时间**：我们要遍历一次坐标数组，算斜率并比较，**O(n)**（n 为点的个数）。  
> - **空间**：只用了常数个额外变量，**O(1)**。  

> **大白话解释 O(n)**：如果有 10 个点，就检查 10 次；如果有 1000 个点，就检查 1000 次，工作量随点的多少线性增长。  

#### 代码（Python）  

```python
from typing import List

def checkStraightLine(coordinates: List[List[int]]) -> bool:
    # 取前两个点
    x0, y0 = coordinates[0]
    x1, y1 = coordinates[1]

    # 计算第一段的斜率，分子和分母分别保存，避免直接除法产生浮点误差
    dx = x1 - x0      # 分母
    dy = y1 - y0      # 分子

    # 对每一个后续点，检查它与第一个点的斜率是否相等
    for i in range(2, len(coordinates)):
        xi, yi = coordinates[i]
        # 两个斜率相等等价于 (yi - y0) / (xi - x0) == dy / dx
        # 为避免除法，交叉相乘后比较： (yi - y0) * dx == (xi - x0) * dy
        if (yi - y0) * dx != (xi - x0) * dy:
            return False        # 只要有一个点不在同一直线上，就返回 False
    return True                 # 全部点都满足条件
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 随着点的数量线性增长，遍历一次即可。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  
上面的“暴力”解已经是 **O(n)**，在本题的约束（n ≤ 1000）下已经很快。  
但我们在实现时仍有细节可以进一步**提升鲁棒性**，尤其是：

1. **除法会产生浮点误差**：如果直接算斜率 `k = dy / dx`，当 `dx` 很大或很小、或者 `dy` 为负数时，可能出现精度丢失。  
2. **竖直线的特殊情况**：`dx = 0` 时，斜率无穷大，直接除法会报错。  

为了解决这两个问题，我们**使用向量的叉积（cross product）**来判断三点是否共线。  
- 把两条向量写成 `(dx1, dy1)` 与 `(dx2, dy2)`，它们的叉积是 `dx1 * dy2 - dy1 * dx2`。  
- 当叉积为 0 时，说明两向量方向相同（或相反），即三点共线。  
- 叉积只涉及整数相乘、相减，不会出现除法和浮点数。

实现步骤：

1. 取前两个点 `p0, p1`，算出基准向量 `v = (dx, dy)`。  
2. 对每个后续点 `pi`，构造向量 `u = (xi - x0, yi - y0)`。  
3. 计算 `dx * (yi - y0) - dy * (xi - x0)`（即 `v × u`），若不为 0 则返回 `False`。  
4. 全部检查通过返回 `True`。  

> **类比**：想象你手里拿两根木棍，一根固定（基准向量），另一根指向新的点。如果把它们放在一起转动，只有当两根木棍完全重合（不产生“扭曲”）时，才说明新点在同一直线上。这个“扭曲程度”正是叉积的数值，0 表示没有扭曲。

#### 代码（Python）  

```python
from typing import List

def checkStraightLine(coordinates: List[List[int]]) -> bool:
    # 取前两个点，构造基准向量
    x0, y0 = coordinates[0]
    x1, y1 = coordinates[1]
    dx = x1 - x0      # 基准向量的 x 分量
    dy = y1 - y0      # 基准向量的 y 分量

    # 逐点检查叉积是否为 0
    for i in range(2, len(coordinates)):
        xi, yi = coordinates[i]
        # 向量 (xi-x0, yi-y0) 与基准向量的叉积
        cross = dx * (yi - y0) - dy * (xi - x0)
        if cross != 0:          # 只要有一次不为 0，就不是同一直线
            return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 仍然只遍历一次点集合。相比暴力解没有增加额外的循环，效率相同。  
- **空间复杂度**：`O(1)` — 只用了常数个整数变量。  

> 与暴力解的对比：  
> - 两者时间相同，但使用叉积避免了除法，**更安全、更不易出错**。  
> - 在实际面试或生产代码中，推荐使用叉积这种“整数版斜率比较”。  

---  

## 心得  

- **核心技巧**：**向量叉积判断共线**（或说“交叉相乘”）。  
- **适用题型**：  
  1. 判断多点是否在同一直线上（本题）。  
  2. 判断三点是否构成直角或平行（利用点积或叉积）。  
  3. 计算多边形的面积（Shoelace formula 也用到了叉积）。  
- **一句话总结**：**“共线 ↔ 叉积为 0”，用整数运算消除斜率除法的陷阱**。  

---  

## 反思  

- **第一反应**：看到“直线”，马上想到斜率公式，想用除法比较。  
- **最容易踩的坑**：  
  - **除以 0**（竖直线）会抛异常。  
  - **浮点数精度误差**导致相等判断失误。  
  - **边界情况**：只有两个点时直接返回 `True`。  
- **下次类似题的第一步**：先把**向量**写出来，想“叉积为 0 吗？”而不是直接算斜率。这样思路更稳健，也更容易写出没有除法的代码。