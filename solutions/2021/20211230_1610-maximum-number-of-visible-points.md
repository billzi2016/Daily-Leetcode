# #1610. 可见点的最大数量 / Maximum Number of Visible Points

> 难度：困难 · 标签：Array、Math、Geometry、Sliding Window、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-visible-points/)

---

## 题目（英文原版）

**Description**

You are given an array points, an integer angle, and your location, where location = [posx, posy] and points[i] = [xi, yi] both denote integral coordinates on the X-Y plane.
Initially, you are facing directly east from your position. You cannot move from your position, but you can rotate. In other words, posx and posy cannot be changed. Your field of view in degrees is represented by angle, determining how wide you can see from any given view direction. Let d be the amount in degrees that you rotate counterclockwise. Then, your field of view is the inclusive range of angles [d - angle/2, d + angle/2].
Your browser does not support the video tag or this video format.
You can see some set of points if, for each point, the angle formed by the point, your position, and the immediate east direction from your position is in your field of view.
There can be multiple points at one coordinate. There may be points at your location, and you can always see these points regardless of your rotation. Points do not obstruct your vision to other points.
Return the maximum number of points you can see.

**Examples**

**Example 1:**

```
Input: points = [[2,1],[2,2],[3,3]], angle = 90, location = [1,1]
Output: 3
Explanation: The shaded region represents your field of view. All points can be made visible in your field of view, including [3,3] even though [2,2] is in front and in the same line of sight.
```

**Example 2:**

```
Input: points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]
Output: 4
Explanation: All points can be made visible in your field of view, including the one at your location.
```

**Example 3:**

```
Input: points = [[1,0],[2,1]], angle = 13, location = [1,1]
Output: 1
Explanation: You can only see one of the two points, as shown above.
```

**Constraints**

- 1 <= points.length <= 105
- points[i].length == 2
- location.length == 2
- 0 <= angle < 360
- 0 <= posx, posy, xi, yi <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一个点数组 `points`、一个整数 `angle`，以及你的所在位置 `location`，其中 `location = [posx, posy]`，`points[i] = [xi, yi]` 都是平面直角坐标系中的整数坐标。

最初，你面向正东方向（即 X 轴正方向）。你不能移动位置，只能原地旋转，也就是说 `posx` 和 `posy` 固定不变。视野宽度（单位：度）用 `angle` 表示，决定了你在任意观察方向下能够看到的范围。设逆时针旋转的角度为 `d`（度），则你的视野为闭区间 `[d - angle/2, d + angle/2]`。

如果某一点相对于你的位置与正东方向形成的角度落在视野范围内，则该点可见。  
- 同一坐标可能出现多个点。  
- 若有点恰好位于你的位置，无论如何旋转都一定能看到这些点。  
- 点本身不会遮挡视线，即不会影响其他点的可见性。

返回在最佳旋转角度下，你能够看到的点的最大数量。

**示例**  

*示例 1*  
```
Input: points = [[2,1],[2,2],[3,3]], angle = 90, location = [1,1]
Output: 3
Explanation: 阴影区域即为你的视野范围。通过适当旋转，所有点都可以出现在视野内，包括 [3,3]，即使 [2,2] 与其在同一直线上且在前方。
```

*示例 2*  
```
Input: points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]
Output: 4
Explanation: 所有点都可以在视野内被看到，其中包括位于你所在位置的点。
```

*示例 3*  
```
Input: points = [[1,0],[2,1]], angle = 13, location = [1,1]
Output: 1
Explanation: 如上图所示，你只能看到两个点中的一个。
```

**约束条件**  

- `1 <= points.length <= 10^5`
- `points[i].length == 2`
- `location.length == 2`
- `0 <= angle < 360`
- `0 <= posx, posy, xi, yi <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每一种可能的朝向都尝试一次，统计能看到多少点**。  
- 首先把所有点相对于观察者的位置 `(posx, posy)` 转成极坐标角度 `θ`（东向为 0°，逆时针递增）。  
- 由于观察者可以任意旋转 `d` 度，那么视野是 `[d‑angle/2, d+angle/2]`（闭区间）。  
- 暴力做法就是把 `d` 设为 **0°、1°、2°、…、359°**（或者更细的步长），每次遍历所有点，检查它们的角度是否落在该区间内，计数后取最大值。  
- 还有一种等价的写法：**把每个点的角度当作窗口左端**，右端就是左端加上 `angle`，统计窗口内的点数。因为角度是连续的，只要把左端枚举为所有点的角度，就能覆盖所有可能的最佳视野。

> **为什么能工作？**  
> 视野是一个连续的角度区间，只要把区间的左端对齐到任意点的角度，就不会错过“最优”位置——如果最优区间的左端不在任何点上，我们可以把它左移到最近的点上，点的数量不变。

> **大白话的复杂度**：  
> - 枚举 `n` 个左端（每个点一次），每次再遍历 `n` 个点检查是否在区间内 → 大约要做 `n × n` 次比较。  
> - 如果 `n = 10⁵`，这相当于 **一万亿** 次操作，电脑根本跑不完。

#### 代码（Python）

```python
import math
from typing import List

def visiblePoints_bruteforce(points: List[List[int]], angle: int,
                            location: List[int]) -> int:
    # 1️⃣ 统计恰好在观察者位置的点，这些点不受视野影响，直接计入答案
    same = 0
    angles = []                     # 其余点的极角（弧度）
    x0, y0 = location
    for x, y in points:
        if x == x0 and y == y0:     # 与观察者同坐标
            same += 1
        else:
            # 计算相对向量的角度，math.atan2 返回 [-π, π]，转换成 [0, 2π)
            theta = math.atan2(y - y0, x - x0)
            if theta < 0:
                theta += 2 * math.pi
            angles.append(theta)

    # 角度为 0° 时，所有点都可见（题目保证 angle < 360）
    if angle == 360:
        return same + len(angles)

    # 2️⃣ 暴力枚举每个点的角度作为窗口左端
    max_cnt = 0
    half = math.radians(angle) / 2   # 角度转成弧度，方便后面比较
    for base in angles:              # 每个点当作窗口左端
        cnt = 0
        # 窗口的右端 = 左端 + angle（弧度）
        right = base + math.radians(angle)
        for a in angles:
            # 处理环绕 2π 的情况：如果右端超过 2π，就把角度加 2π 再比较
            if base <= a <= right or (right > 2 * math.pi and a + 2 * math.pi <= right):
                cnt += 1
        max_cnt = max(max_cnt, cnt)

    return same + max_cnt
```

> **关键注释**  
> - `math.atan2(dy, dx)` 把向量 `(dx, dy)` 转成角度，就像把指南针指向 **东** 为 0°，**北** 为 90°。  
> - `same` 记录“就在原点”的点，这些点永远能看到。  
> - `half` 只是把角度从度数转换成弧度，方便后面比较。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：如果有 `n` 个点（不算在原点的），我们会对每个点遍历全部点一次。`n²` 就像“排队买票时每个人都要检查每个人的票”，随着点的增多，耗时会呈 **平方** 增长。
- **空间复杂度**：`O(n)`  
  - 只需要存储每个点的角度以及少量额外变量，和点的数量成线性关系。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次窗口左端固定时，都要遍历所有点去计数**。我们可以把所有点的角度排好序，然后用**滑动窗口（双指针）**一次遍历完成全部计数。

**核心观察**  
1. 把每个点的角度排成从小到大的一条直线（圆形展开为线段），**任意一个视野都对应一段连续的角度**。  
2. 为了处理“跨过 0°/360° 的情况”，把已经排好序的角度列表再复制一遍并在每个角度上加 `2π`，形成 `angles + [a+2π for a in angles]`。这样所有可能的连续窗口都可以在这条 **不环绕** 的长数组里找到。  
3. 设窗口左端指针 `i`，右端指针 `j` 向右移动，只要 `angles[j] - angles[i] <= angle`（弧度），窗口就合法。窗口大小 `j-i+1` 就是当前左端能看到的点数。  
4. 当左端 `i` 向右移动时，右端 `j` 不会左移，只会继续往右推进（因为角度是单调递增），于是整体只遍历一次，**线性时间**。

**步骤细化**  
- **步骤 1**：统计同位置点 `same`（同暴力解），并把其它点的角度存入列表 `angles`（弧度）。  
- **步骤 2**：把 `angles` 排序。  
- **步骤 3**：如果 `angle == 360`，直接返回所有点数（因为视野覆盖全圆）。  
- **步骤 4**：把排好序的 `angles` 复制一遍并加 `2π`，得到 `extended = angles + [a + 2π for a in angles]`。  
- **步骤 5**：使用双指针遍历 `extended`（只遍历前 `len(angles)` 个左端），维护右指针 `j` 使得 `extended[j] - extended[i] <= angle_rad`。记录最大窗口大小。  
- **步骤 6**：答案 = `same + max_window`。

> **类比**：  
> 想象一条绳子上挂着彩灯，彩灯的间距对应点的角度。你手里有一个固定长度的灯罩（视野宽度），想把灯罩滑动，使得罩住最多的彩灯。把绳子首尾相连再拉直，就可以一次性把所有可能的“罩住区间”都在直线里找到，这正是我们复制加 `2π` 的作用。

#### 代码（Python）

```python
import math
from typing import List

def visiblePoints(points: List[List[int]], angle: int,
                 location: List[int]) -> int:
    # ---------- 1️⃣ 统计在原点的点 ----------
    same = 0
    angles = []                     # 其余点的极角（弧度）
    x0, y0 = location
    for x, y in points:
        if x == x0 and y == y0:
            same += 1
        else:
            theta = math.atan2(y - y0, x - x0)   # [-π, π]
            if theta < 0:
                theta += 2 * math.pi            # 转成 [0, 2π)
            angles.append(theta)

    # ---------- 2️⃣ 特殊情况：视野覆盖全圆 ----------
    if angle == 360:
        return same + len(angles)

    # ---------- 3️⃣ 角度排序 ----------
    angles.sort()
    n = len(angles)
    if n == 0:                     # 只有同位置的点
        return same

    # ---------- 4️⃣ 复制一遍，处理环绕 ----------
    angle_rad = math.radians(angle)   # 把度数转成弧度，后面比较更直观
    extended = angles + [a + 2 * math.pi for a in angles]

    # ---------- 5️⃣ 双指针滑动窗口 ----------
    max_cnt = 0
    j = 0
    for i in range(n):                 # 只让 i 在原始数组范围内
        # 保证 j 总是向右移动，窗口合法
        while j < i + n and extended[j] - extended[i] <= angle_rad + 1e-9:
            j += 1
        # 窗口内点的数量 = j - i（因为 j 已经指向第一个不合法的元素）
        max_cnt = max(max_cnt, j - i)

    # ---------- 6️⃣ 加上同位置点 ----------
    return same + max_cnt
```

> **代码要点注释**  
> - `1e-9` 是防止浮点数误差导致的“恰好相等”被误判。  
> - `j < i + n` 保证右指针不跨过复制的第二段太远，只需要看最多 `n` 个元素（因为窗口最大不超过全部点数）。  
> - `extended[j] - extended[i] <= angle_rad` 判断当前窗口是否仍在视野范围内。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，滑动窗口一次线性遍历 `O(n)`，两者相加仍是 `O(n log n)`。相比暴力的 `O(n²)`，这就像把 **“遍历所有人”** 换成 **“先排好队再快速检查”**，大幅提升效率。  
- **空间复杂度**：`O(n)`  
  - 需要存储角度数组以及复制后的 `extended`（长度约为 `2n`），与点的数量呈线性关系。

---

## 心得

- **核心技巧**：**极角排序 + 双指针滑动窗口**。先把点的方向统一到一条线（极坐标），再利用“窗口在有序序列中滑动”快速统计最大可见点数。  
- **适用场景**（类似题目）  
  1. “最多点在同一条直线的角度范围内” – 例如 **`Maximum Points Inside a Circle`**（将距离改成角度）。  
  2. “在环形数组中找最长子数组满足和 ≤ K” – 需要复制数组处理环绕，同样用滑动窗口。  
  3. “在平面上找最长的角度区间覆盖的点” – 如 **`Find the K Closest Points to Origin`**（把距离换成角度）。  
- **一句话总结**：把环形问题“摊平”成直线，再用 **有序+窗口** 的思路一次遍历即可得到最优解。

---

## 反思

- **第一反应**：看到“角度、旋转、视野”，自然想到把点转成极坐标，再枚举所有可能的视角。  
- **最容易踩的坑**  
  1. **同位置的点**：它们的角度是未定义的，必须单独计数，否则会漏掉。  
  2. **角度跨 0°/360°**：直接比较会出错，需要把数组复制并加 `2π` 来处理环绕。  
  3. **浮点数误差**：`math.atan2`、`math.radians` 产生的结果可能出现极小的误差，比较时加一个容忍值（如 `1e-9`）防止错判。  
- **下次类似题目第一步**：**把几何信息（距离、角度、方向）统一到一维有序序列**（比如极角、距离），再思考是否可以使用 **双指针/滑动窗口** 在该序列上一次遍历求解。