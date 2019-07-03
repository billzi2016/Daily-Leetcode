# #478. 生成圆内随机点 / Generate Random Point in a Circle

> 难度：中等 · 标签：Math、Geometry、Rejection Sampling、Randomized · [LeetCode 链接](https://leetcode.com/problems/generate-random-point-in-a-circle/)

---

## 题目（英文原版）

**Description**

Given the radius and the position of the center of a circle, implement the function randPoint which generates a uniform random point inside the circle.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input
["Solution", "randPoint", "randPoint", "randPoint"]
[[1.0, 0.0, 0.0], [], [], []]
Output
[null, [-0.02493, -0.38077], [0.82314, 0.38945], [0.36572, 0.17248]]

Explanation
Solution solution = new Solution(1.0, 0.0, 0.0);
solution.randPoint(); // return [-0.02493, -0.38077]
solution.randPoint(); // return [0.82314, 0.38945]
solution.randPoint(); // return [0.36572, 0.17248]
```

**Constraints**

- 0 < radius <= 108
- -107 <= x_center, y_center <= 107
- At most 3 * 104 calls will be made to randPoint.

---

## 题目（中文翻译）

给定圆的半径（radius）和圆心（center）的位置，实现函数 `randPoint`，使其能够在圆内生成均匀分布的随机点（random point）。

**实现 `Solution` 类：**

**示例 1：**

**Input**  
```json
["Solution", "randPoint", "randPoint", "randPoint"]
[[1.0, 0.0, 0.0], [], [], []]
```

**Output**  
```json
[null, [-0.02493, -0.38077], [0.82314, 0.38945], [0.36572, 0.17248]]
```

**Explanation**  
```java
Solution solution = new Solution(1.0, 0.0, 0.0);
solution.randPoint(); // 返回 [-0.02493, -0.38077]
solution.randPoint(); // 返回 [0.82314, 0.38945]
solution.randPoint(); // 返回 [0.36572, 0.17248]
```

**约束条件**  
- `0 < radius <= 10^8`  
- `-10^7 <= x_center, y_center <= 10^7`  
- 最多会调用 `randPoint` `3 * 10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法是先在**外接正方形**里随机挑一个点，然后检查它是否落在圆内。  
- **外接正方形**的边长等于圆的直径 `2 * radius`，中心和圆心相同。  
- 随机生成的 `x`、`y` 坐标可以看成“在字典里查词”，字典的 **key** 是坐标，**value** 是是否在圆内。我们只需要判断 ` (x‑x_center)² + (y‑y_center)² ≤ radius² `，如果成立就返回，否则再来一次——这一步叫**拒绝采样（rejection sampling）**。  

这样做一定能得到均匀分布的点，因为每一次的随机坐标都是在同一个正方形里等概率产生的，只有把不合法的点“扔掉”。  

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float):
        self.r = radius                 # 圆的半径
        self.xc = x_center              # 圆心的 x 坐标
        self.yc = y_center              # 圆心的 y 坐标
        self.r_sq = radius * radius     # 预先算好的 r²，后面会反复用到

    def randPoint(self) -> List[float]:
        while True:                     # 不断尝试，直到采到合法点
            # 在外接正方形里随机取点，范围是 [xc‑r, xc+r] × [yc‑r, yc+r]
            x = random.uniform(self.xc - self.r, self.xc + self.r)
            y = random.uniform(self.yc - self.r, self.yc + self.r)

            # 判断是否在圆内：欧氏距离的平方 ≤ r²
            if (x - self.xc) ** 2 + (y - self.yc) ** 2 <= self.r_sq:
                return [x, y]          # 合法，直接返回
```

#### 复杂度  

- **时间复杂度**：`O(1)`（期望）。  
  - 解释：一次循环的概率是 **圆面积 / 正方形面积 = πr² / (2r)² = π/4 ≈ 0.785**，也就是说平均只需要约 `1 / 0.785 ≈ 1.27` 次循环就能得到合法点。虽然最坏情况（一直不满足）理论上是无限次，但在实际随机环境下几乎不会出现。  
- **空间复杂度**：`O(1)`。只用了常数个变量，和输入规模无关。

---

### 2. 最优解

#### 思路  
上面的暴力解的“慢点”在于**可能会多次循环**——每次都要生成两个随机数并做一次判定。我们可以直接**在圆内部生成点**，这样一次就能得到合法坐标，避免拒绝采样的循环。

**核心技巧：极坐标 + 开方**  

1. **角度** `θ`：在圆里，任意方向出现的概率应该相同。于是我们可以在 `[0, 2π)` 区间均匀取一个角度，用 `random.random() * 2 * math.pi` 实现。  
2. **半径** `ρ`：如果直接在 `[0, r]` 里均匀取半径，离圆心近的区域会产生的点更少，因为面积是 `πρ²`，而不是线性增长。要让每一个**面积元素**出现的概率相同，需要在 **面积** 上均匀取点。  
   - 设 `u` 为 `[0, 1)` 的均匀随机数，取 `ρ = sqrt(u) * r`。  
   - 为什么要开根号？因为面积对应的是 `ρ²`，如果 `u = (ρ/r)²`，则 `ρ = r * sqrt(u)`，这样 `ρ` 的分布正好让每个面积块出现概率相等。  

得到极坐标 `(ρ, θ)` 后，用三角函数转回笛卡尔坐标：

```
x = x_center + ρ * cos(θ)
y = y_center + ρ * sin(θ)
```

这样一次就能得到圆内的均匀点，**不需要循环**。

#### 代码（Python）

```python
import random
import math
from typing import List

class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float):
        self.r = radius
        self.xc = x_center
        self.yc = y_center

    def randPoint(self) -> List[float]:
        # 1. 随机角度，均匀分布在 [0, 2π)
        theta = random.random() * 2 * math.pi

        # 2. 随机半径，先在 [0,1) 均匀取 u，再开根号得到 ρ
        u = random.random()
        rho = self.r * math.sqrt(u)   # 开根号是关键

        # 3. 极坐标转笛卡尔坐标，加上圆心偏移
        x = self.xc + rho * math.cos(theta)
        y = self.yc + rho * math.sin(theta)

        return [x, y]
```

#### 复杂度  

- **时间复杂度**：`O(1)`（确定性）。  
  - 解释：只做了固定次数的随机数生成、一次开根号、一次三角函数运算，和点的数量无关。比起可能需要多次循环的暴力解，这里永远只需要“一次”。  
- **空间复杂度**：`O(1)`。只用了常数个局部变量。

---

## 心得

- **核心技巧**：把“均匀采样”从**面积**层面转化为**极坐标**，并用 `sqrt` 把线性均匀的随机数映射到半径上。  
- **适用的题型**  
  1. “在圆/球内均匀随机点” 类题（如 3D 球体随机点）。  
  2. “在矩形/多边形内均匀随机点” 时，也常先做**拒绝采样**或**切分面积**的思路。  
  3. “随机生成满足某分布的数值” 时，需要把 **均匀分布** 通过**逆变换采样**映射到目标分布。  
- **一句话总结解题钥匙**：**先把均匀性放到面积（或体积）上，再用合适的坐标变换一次搞定**。

---

## 反思

- **第一反应**：直接在外接正方形里随机取点，然后判断是否在圆内（即暴力的拒绝采样）。这思路最直观，也容易写对。  
- **最容易踩的坑**  
  - 忘记把 `radius` 的平方用于判断，会导致点分布不均。  
  - 使用 `random.randint`（离散）而不是 `random.random`（连续）会让点分布出现格子状的偏差。  
  - 在极坐标法里忘记对半径做 `sqrt`，会导致点集中在圆心附近。  
- **下次遇到同类题**：第一步先思考**“我想让每一块面积出现的概率相同吗？”**，如果是，就立刻考虑**极坐标 + 逆变换**（开根号）或**直接在几何体内部采样**，而不是先在外层盒子里随机再过滤。