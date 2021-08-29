# #1453. 最大数量的飞镖落在圆形飞镖盘内 / Maximum Number of Darts Inside of a Circular Dartboard

> 难度：困难 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/)

---

## 题目（英文原版）

**Description**

Alice is throwing n darts on a very large wall. You are given an array darts where darts[i] = [xi, yi] is the position of the ith dart that Alice threw on the wall.
Bob knows the positions of the n darts on the wall. He wants to place a dartboard of radius r on the wall so that the maximum number of darts that Alice throws lie on the dartboard.
Given the integer r, return the maximum number of darts that can lie on the dartboard.

**Examples**

**Example 1:**

```
Input: darts = [[-2,0],[2,0],[0,2],[0,-2]], r = 2
Output: 4
Explanation: Circle dartboard with center in (0,0) and radius = 2 contain all points.
```

**Example 2:**

```
Input: darts = [[-3,0],[3,0],[2,6],[5,4],[0,9],[7,8]], r = 5
Output: 5
Explanation: Circle dartboard with center in (0,4) and radius = 5 contain all points except the point (7,8).
```

**Constraints**

- 1 <= darts.length <= 100
- darts[i].length == 2
- -104 <= xi, yi <= 104
- All the darts are unique
- 1 <= r <= 5000

---

## 题目（中文翻译）

**描述**  
Alice 在一面非常大的墙上投掷了 `n` 支飞镖。给定一个数组 `darts`，其中 `darts[i] = [x_i, y_i]` 表示第 `i` 支飞镖在墙上的坐标。  
Bob 已经知道这 `n` 支飞镖的所有位置，他想在墙上放置一个半径为 `r` 的圆形飞镖盘（dartboard），使得落在飞镖盘内的飞镖数量尽可能多。  
给定整数 `r`，返回可以落在飞镖盘上的最大飞镖数。

**示例 1**  

**示例 2**  

**约束条件**  
- `1 <= darts.length <= 100`  
- `darts[i].length == 2`  
- `-10^4 <= x_i, y_i <= 10^4`  
- 所有的飞镖位置互不相同  
- `1 <= r <= 5000`

**示例**  

**示例 1**  
```text
Input: darts = [[-2,0],[2,0],[0,2],[0,-2]], r = 2
Output: 4
Explanation: 以中心 `(0,0)`、半径 `2` 的圆形飞镖盘包含了所有点。
```

**示例 2**  
```text
Input: darts = [[-3,0],[3,0],[2,6],[5,4],[0,9],[7,8]], r = 5
Output: 5
Explanation: 以中心 `(0,4)`、半径 `5` 的圆形飞镖盘包含了除点 `(7,8)` 之外的所有点。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的圆都枚举一遍**，然后统计每个圆里有多少飞镖。  
圆的半径 `r` 已经固定了，只要确定圆心 `(cx, cy)` 就唯一确定一个圆。  
我们可以这样做：

1. **任选两个飞镖** `A(x1, y1)`、`B(x2, y2)`。  
   - 如果这两个点的距离 `d` 大于 `2r`，说明半径为 `r` 的圆根本容不下它们，直接跳过。  
   - 否则，以 `A`、`B` 为圆上两点，半径为 `r` 的圆有 **0、1 或 2** 个（就像用绳子（长度 `2r`）把两根钉子系在墙上，绳子可以在墙面上形成两种不同的圆）。我们把这 0/1/2 个圆心算出来。  

2. 对每一个得到的圆心，**遍历所有飞镖**，统计有多少飞镖在圆的内部（包括边界）。  
3. 记录出现的最大值，即为答案。

> **类比**：  
> - “哈希表像查字典”，这里的 **圆心** 就像字典的 **key**，对应的 **“圆里包含的飞镖数量”** 就是 **value**。我们把每个可能的 key（圆心）都算一遍，找出最大的 value。

**为什么正确**：  
- 题目提示：*如果存在最优解，必然可以把圆移动到让两点恰好在圆的边界上*。因此只要枚举所有点对产生的圆心，就一定会包含最优圆心。  

#### 代码（Python）

```python
import math
from typing import List

def maxDartsInsideCircle(darts: List[List[int]], r: int) -> int:
    # 计算两点距离的平方，避免每次开根号
    def dist2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    n = len(darts)
    if n == 1:                     # 只有一个点，显然答案是 1
        return 1

    r2 = r * r                     # 半径的平方，后面比较用
    best = 1                       # 至少能放下一个

    # 把所有点对枚举一遍
    for i in range(n):
        for j in range(i + 1, n):
            p, q = darts[i], darts[j]
            d2 = dist2(p, q)       # 两点距离的平方

            # 两点距离大于直径，半径 r 的圆不可能同时容下它们
            if d2 > (2 * r) ** 2:
                continue

            # ---------- 计算圆心 ----------
            # 中点
            mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
            # 两点连线的斜率向量 (dx, dy)
            dx, dy = q[0] - p[0], q[1] - p[1]
            # 直线垂直方向的单位向量
            # 长度为 d = sqrt(d2)
            d = math.sqrt(d2)
            ux, uy = -dy / d, dx / d   # 旋转 90° 并归一化

            # 两个可能的圆心距离中点的距离
            # 根据勾股定理： (r)^2 = (d/2)^2 + h^2 => h = sqrt(r^2 - (d/2)^2)
            h = math.sqrt(r2 - (d / 2) ** 2)

            # 圆心1、2
            centers = [
                (mx + ux * h, my + uy * h),
                (mx - ux * h, my - uy * h)
            ]

            # ---------- 统计每个圆心能包含多少点 ----------
            for cx, cy in centers:
                cnt = 0
                for x, y in darts:
                    if (x - cx) ** 2 + (y - cy) ** 2 <= r2 + 1e-7:
                        cnt += 1
                best = max(best, cnt)

    return best
```

> **关键行解释**  
> - `if d2 > (2 * r) ** 2:`：两点间距大于直径时直接剪枝。  
> - `ux, uy = -dy / d, dx / d`：把连线向量旋转 90° 并归一化，得到垂直方向的单位向量。  
> - `h = math.sqrt(r2 - (d / 2) ** 2)`：几何公式，求出圆心到连线中点的距离。  
> - `if (x - cx) ** 2 + (y - cy) ** 2 <= r2 + 1e-7:`：判断点是否在圆内（加上极小的误差容忍）。

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环遍历所有点对，数量是 `C(n,2) = n·(n-1)/2 ≈ n²/2`。  
  - 对每个圆心我们再次遍历全部 `n` 个点统计。  
  - 所以整体是 `≈ n² × n = n³`。  
  - **大白话**：如果有 100 个飞镖，最坏情况下要检查 `100³ = 1,000,000` 次，这在电脑里跑得很快。

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（几个坐标、计数器），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历所有点去统计**，导致 `O(n³)`。  
我们可以把统计过程 **合并到一次遍历**，把问题转化为 **角度区间重叠**，从而把复杂度降到 `O(n² log n)`。

核心想法：

1. **固定一个飞镖 `P`**，把它当作圆的 **“参考点”**。  
   圆心必须在以 `P` 为圆心、半径为 `r` 的圆上（因为 `P` 必须落在圆内）。我们把这些可能的圆心看成 **一个圆周**。

2. 对于另一飞镖 `Q`（`Q != P`），如果 `|PQ| > 2r`，根本不可能和 `P` 同时在同一个半径 `r` 的圆里，直接忽略。  
   否则，**所有能同时容下 `P` 与 `Q` 的圆心**，在上面那条圆周上会形成一个 **弧段**。  
   - 把向量 `PQ` 的方向记为角度 `θ = atan2(Qy-Py, Qx-Px)`。  
   - 以 `θ` 为中心，左右各展开 `α = acos(d / (2r))`（这里 `d = |PQ|`），得到区间 `[θ-α, θ+α]`。  
   - 圆心落在这个角度区间内，就能把 `P` 与 `Q` 同时包含。

3. 对固定的 `P`，我们得到 **`n-1` 个角度区间**（每个其他点对应一个区间）。  
   现在问题变成：**在一个圆周上，最多有多少个区间相交**？  
   这正是“区间最大重叠数”问题，可以用 **角度扫描（Sweep）**解决：  
   - 把每个区间的左端点记为 `+1`（进入），右端点记为 `-1`（离开）。  
   - 将所有端点按角度排序（需要把跨越 `2π` 的区间拆开或复制一遍），顺序遍历，维护当前的重叠计数，最大值即为以 `P` 为参考点时能容下的最多飞镖数。  

4. 对每个 `P` 重复步骤 2~3，取所有 `P` 的最大值即为答案。

> **类比**：  
> - 把圆心想象成 **“在转盘上的指针”**。每个其它飞镖 `Q` 给指针划出一个 “可以接受的角度区间”。我们要找出指针在转动时，最多同时落在多少个区间里——这正是 **“找最多重叠的区间”**。

#### 代码（Python）

```python
import math
from typing import List

def maxDartsInsideCircle(darts: List[List[int]], r: int) -> int:
    n = len(darts)
    if n <= 2:                     # 两个点以下必然全在同一个圆里
        return n

    r2 = r * r                     # 半径平方，后面距离比较用
    ans = 1                        # 至少能放下一个

    for i in range(n):
        # 以 darts[i] 为参考点 P
        angles = []                # 保存所有区间的端点（角度, 进入/离开）

        xi, yi = darts[i]

        for j in range(n):
            if i == j:
                continue
            xj, yj = darts[j]
            dx, dy = xj - xi, yj - yi
            d2 = dx * dx + dy * dy

            # 两点距离大于直径，根本不可能同在一个半径 r 的圆里
            if d2 > (2 * r) ** 2:
                continue

            d = math.sqrt(d2)                      # |PQ|
            base = math.atan2(dy, dx)              # 向量 PQ 的方向角 θ
            # 计算可以让圆心同时覆盖 P、Q 的角度偏移 α
            # 根据余弦定理：cos α = d / (2r)
            alpha = math.acos(d / (2.0 * r))

            start = base - alpha
            end   = base + alpha

            # 为了统一处理跨 0/2π 的情况，把角度规范到 [0, 2π) 再复制一遍
            # 这里我们把所有角度都平移到 [0, 2π) 区间
            # 若 start < 0，或 end >= 2π，后面会统一加 2π 复制
            angles.append((start, 1))   # 进入区间
            angles.append((end, -1))    # 离开区间

        # 归一化到 [0, 2π) 并复制一遍，以处理环形跨界
        norm = []
        for ang, typ in angles:
            # 把角度搬到 [0, 2π)
            a = ang % (2 * math.pi)
            norm.append((a, typ))
            # 复制一遍，+2π，方便后面线性扫描
            norm.append((a + 2 * math.pi, typ))

        # 按角度排序，若角度相同，先进入后离开（确保计数正确）
        norm.sort(key=lambda x: (x[0], -x[1]))

        cur = 1                     # 圆心一定在 P 的圆上，算上 P 本身
        for ang, typ in norm:
            cur += typ
            ans = max(ans, cur)

    return ans
```

> **关键行解释**  
> - `alpha = math.acos(d / (2.0 * r))`：几何公式，求出 **“圆心相对于点 P 的允许偏移角度”**。  
> - `ang % (2 * math.pi)`：把角度统一到 `[0, 2π)`，方便后面处理环形。  
> - `norm.append((a + 2 * math.pi, typ))`：把所有角度再平移一圈复制一遍，避免在 `0` 与 `2π` 交界处漏算重叠。  
> - `cur = 1`：默认圆心已经包含参考点 `P` 本身。  

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 外层遍历每个参考点 `P`，共 `n` 次。  
  - 对每个 `P`，我们最多生成 `2·(n-1)` 个区间端点（每个其它点最多产生 2 条端点），随后进行一次排序，排序复杂度是 `O(m log m)`，这里 `m ≤ 2·(n-1) = O(n)`。  
  - 因此每个 `P` 的工作量是 `O(n log n)`，整体是 `O(n² log n)`。  
  - **大白话**：如果有 100 个飞镖，大约要做 `100² ≈ 10,000` 次排序，每次排序的元素不多，跑得非常快。

- **空间复杂度**：`O(n)`  
  - 对每个参考点我们保存的角度列表长度最多是 `2·(n-1)`，随 `n` 线性增长。  

---

## 心得

- **核心技巧**：把几何约束转化为 **角度区间重叠**，利用 **扫描线（Sweep）** 求最大重叠数。  
- **适用题型**（类似思路）  
  1. **“在平面上放置固定半径的圆，使得包含点的数量最多”**（本题的变形）。  
  2. **“给定若干线段，求一条垂直线能穿过最多的线段”**（转化为一维区间重叠）。  
  3. **“在平面上放置固定长度的线段，使得覆盖最多的点”**（也可转化为角度区间问题）。  

- **一句话总结解题钥匙**：  
  *“固定一个点，把所有能和它同在圆里的点对应成角度区间，求最大区间重叠即可”。*

---

## 反思

- **第一反应**：看到“圆的半径固定，找最优圆心”，立刻想到**枚举两点求圆心**的暴力法。  
- **最容易踩的坑**  
  1. **数值误差**：`acos` 的参数可能因浮点误差略大于 1，导致 `ValueError`。要先 `min(1, max(-1, d/(2r)))` 或加上容忍 `1e-9`。  
  2. **跨 0/2π 的区间**：直接在 `[0, 2π)` 排序会把跨界的区间割断，需要复制一圈或特殊处理。  
  3. **特殊情况**：点数只有 1 或 2 时直接返回 `n`，避免后面角度计算除以零等异常。  

- **下次遇到同类题**：  
  *“先把几何约束转成角度/距离的区间，然后用区间重叠/滑动窗口求最大覆盖”。*  

祝你在几何与算法的世界里玩得开心 🚀