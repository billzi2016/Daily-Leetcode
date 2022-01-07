# #1620. 网络质量最高的坐标 / Coordinate With Maximum Network Quality

> 难度：中等 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/coordinate-with-maximum-network-quality/)

---

## 题目（英文原版）

**Description**

You are given an array of network towers towers, where towers[i] = [xi, yi, qi] denotes the ith network tower with location (xi, yi) and quality factor qi. All the coordinates are integral coordinates on the X-Y plane, and the distance between the two coordinates is the Euclidean distance.
You are also given an integer radius where a tower is reachable if the distance is less than or equal to radius. Outside that distance, the signal becomes garbled, and the tower is not reachable.
The signal quality of the ith tower at a coordinate (x, y) is calculated with the formula ⌊qi / (1 + d)⌋, where d is the distance between the tower and the coordinate. The network quality at a coordinate is the sum of the signal qualities from all the reachable towers.
Return the array [cx, cy] representing the integral coordinate (cx, cy) where the network quality is maximum. If there are multiple coordinates with the same network quality, return the lexicographically minimum non-negative coordinate.
Note:

**Examples**

**Example 1:**

```
Input: towers = [[1,2,5],[2,1,7],[3,1,9]], radius = 2
Output: [2,1]
Explanation: At coordinate (2, 1) the total quality is 13.
- Quality of 7 from (2, 1) results in ⌊7 / (1 + sqrt(0)⌋ = ⌊7⌋ = 7
- Quality of 5 from (1, 2) results in ⌊5 / (1 + sqrt(2)⌋ = ⌊2.07⌋ = 2
- Quality of 9 from (3, 1) results in ⌊9 / (1 + sqrt(1)⌋ = ⌊4.5⌋ = 4
No other coordinate has a higher network quality.
```

**Example 2:**

```
Input: towers = [[23,11,21]], radius = 9
Output: [23,11]
Explanation: Since there is only one tower, the network quality is highest right at the tower's location.
```

**Example 3:**

```
Input: towers = [[1,2,13],[2,1,7],[0,1,9]], radius = 2
Output: [1,2]
Explanation: Coordinate (1, 2) has the highest network quality.
```

**Constraints**

- 1 <= towers.length <= 50
- towers[i].length == 3
- 0 <= xi, yi, qi <= 50
- 1 <= radius <= 50

---

## 题目（中文翻译）

**描述**  
给定一个数组 `towers`，其中 `towers[i] = [xi, yi, qi]` 表示第 `i` 个网络塔（tower），其位置为 `(xi, yi)`，质量因子为 `qi`。所有坐标均为平面直角坐标系中的整数坐标，两个坐标之间的距离采用欧几里得距离（Euclidean distance）。

同时给定一个整数 `radius`，当塔与某坐标的距离小于等于 `radius` 时，该塔是可达（reachable）的；超出该距离后信号会失真，塔不可达。

第 `i` 块塔在坐标 `(x, y)` 处的信号质量（signal quality）按公式  

\[
\left\lfloor \frac{qi}{1 + d} \right\rfloor
\]

计算，其中 `d` 为该塔与坐标之间的距离。某坐标的网络质量（network quality）是所有可达塔的信号质量之和。

返回数组 `[cx, cy]`，表示网络质量最大的整数坐标 `(cx, cy)`。若存在多个坐标拥有相同的最大网络质量，返回字典序最小的非负坐标。

**示例 1**  
```text
Input: towers = [[1,2,5],[2,1,7],[3,1,9]], radius = 2
Output: [2,1]
```
**解释**：在坐标 `(2, 1)` 处，总质量为 13。  
- 来自塔 `(2, 1)`（质量因子 7）的质量为 `⌊7 / (1 + sqrt(0))⌋ = ⌊7⌋ = 7`。  
- 来自塔 `(1, 2)`（质量因子 5）的质量为 `⌊5 / (1 + sqrt(2))⌋ = ⌊2.07⌋ = 2`。  
- 来自塔 `(3, 1)`（质量因子 9）的质量为 `⌊9 / (1 + sqrt(1))⌋ = ⌊4.5⌋ = 4`。  
没有其他坐标的网络质量更高。

**示例 2**  
```text
Input: towers = [[23,11,21]], radius = 9
Output: [23,11]
```
**解释**：只有一座塔，网络质量在塔所在位置最高。

**示例 3**  
```text
Input: towers = [[1,2,13],[2,1,7],[0,1,9]], radius = 2
Output: [1,2]
```
**解释**：坐标 `(1, 2)` 具有最高的网络质量。

**约束条件**  
- `1 <= towers.length <= 50`  
- `towers[i].length == 3`  
- `0 <= xi, yi, qi <= 50`  
- `1 <= radius <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

这道题的输入规模非常小：  

- 塔的数量 `n ≤ 50`  
- 每个坐标 `xi, yi` 都在 `[0, 50]` 之间  
- 信号半径 `radius ≤ 50`  

因为所有坐标都是整数，而且范围不大，我们可以把**所有可能的整数坐标**都枚举一遍，逐个计算它们的网络质量，最后挑出质量最高的坐标即可。  

**用到的数据结构**  

- **列表（list）**：存放塔的信息 `towers[i] = [xi, yi, qi]`。  
- **双层循环**：外层遍历所有候选坐标 `(x, y)`，内层遍历所有塔，求每座塔对该坐标的贡献。  
- **数学函数**：`math.sqrt` 计算欧氏距离，`int()`（向下取整）实现公式中的 ⌊ ⌋。  

> 类比：把平面想成一张格子纸，格子上的每个点都是一个“候选点”。我们要把每个格子里的“信号强度”算出来，找出最高的格子。  

**为什么这个方法一定能得到正确答案**  

- 题目要求的坐标必须是整数且 **非负**，所以只要遍历所有非负整数点，就不会漏掉答案。  
- 对每个点，我们按照题目给出的公式，**逐塔累加**，得到的正是该点的网络质量。  
- 只要把所有点的质量都算出来，取最大值（若相同取字典序最小），答案自然出现。  

**时间/空间复杂度的大白话**  

- **时间复杂度**：我们要检查 `X` 个横坐标 × `Y` 个纵坐标，每个坐标再遍历 `n` 座塔。  
  - 这里 `X`、`Y` 最多是 `0 … 50 + radius ≤ 100`，所以最多约 `101 × 101 ≈ 10⁴` 个点。  
  - 每个点最多看 `50` 座塔，算下来大约 `5×10⁵` 次简单运算。  
  - 用大 O 记法写成 `O((M+R)² · n)`，其中 `M` 是最大坐标（≤50），`R` 是半径（≤50），`n` 是塔的数量。  
  - **直观解释**：最多十几万次“小计算”，在电脑里几毫秒就能跑完。  

- **空间复杂度**：只用了几个常数级的变量（循环计数、临时和），与输入规模无关，记作 `O(1)`（常数空间）。  

#### 代码（Python）  

```python
import math
from typing import List

def bestCoordinate(towers: List[List[int]], radius: int) -> List[int]:
    # 1. 计算搜索范围：所有塔的坐标加上半径的上下界
    min_x = min(t[0] for t in towers)
    max_x = max(t[0] for t in towers)
    min_y = min(t[1] for t in towers)
    max_y = max(t[1] for t in towers)

    # 为了不遗漏半径覆盖的区域，向外扩展 radius
    start_x, end_x = max(0, min_x - radius), max_x + radius
    start_y, end_y = max(0, min_y - radius), max_y + radius

    best_quality = -1          # 当前找到的最大质量
    best_coord = [0, 0]        # 对应的坐标

    # 2. 枚举所有整数坐标 (x, y)
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            total = 0  # 该点的累计网络质量

            # 3. 对每座塔，计算它是否在半径内并贡献多少质量
            for tx, ty, q in towers:
                d = math.sqrt((tx - x) ** 2 + (ty - y) ** 2)  # 欧氏距离
                if d <= radius:               # 在可达范围内
                    total += int(q / (1 + d))  # ⌊ qi / (1 + d) ⌋

            # 4. 更新答案：质量更高或质量相同但字典序更小
            if total > best_quality or (total == best_quality and [x, y] < best_coord):
                best_quality = total
                best_coord = [x, y]

    return best_coord
```

> **关键行中文注释**  
> - 第 4‑7 行：先找出所有塔的最左/最右、最上/最下位置，再向四周各扩 `radius`，保证搜索区域完整。  
> - 第 12‑14 行：遍历每个候选点 `(x, y)`。  
> - 第 17‑21 行：对每座塔计算距离 `d`，若 `d ≤ radius`，按公式累加质量。`int()` 自动向下取整。  
> - 第 24‑27 行：如果当前点的质量更大，或相等但坐标更“靠前”（字典序），就更新答案。  

#### 复杂度  

- **时间复杂度**：`O((M+R)² · n)`，约 `O(10⁴·50) = O(5·10⁵)` 次基本运算。  
  - **含义**：即使在最坏情况下（搜索 101×101 个点、50 座塔），也只要几百毫秒就能完成。  
- **空间复杂度**：`O(1)`，只用了若干临时变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  

暴力解已经能在题目给出的约束下轻松 AC，但我们仍可以把搜索范围 **进一步收紧**，让代码更“干净”。  

**慢点在哪？**  
- 暴力解把整个矩形 `[0, max_x+radius] × [0, max_y+radius]` 都遍历了一遍。  
- 实际上，只有**离任意塔不超过 `radius` 的点** 才可能得到正的质量。  
- 只要把搜索框限定在“所有塔的覆盖区的并集”即可，外面的点质量必为 0，根本不需要算。  

**如何收紧搜索框？**  
1. 对每座塔 `(xi, yi)`，它的有效覆盖区域是一个以它为中心、半径为 `radius` 的圆。  
2. 把所有这些圆的 **外接矩形** 合并，即可得到一个**最小的矩形**，只要遍历这个矩形就不会漏掉任何可能的最佳点。  
   - 外接矩形的左下角是 `(max(0, min_x - radius), max(0, min_y - radius))`。  
   - 右上角是 `(max_x + radius, max_y + radius)`。  
   - 这里的 `min_x / max_x`、`min_y / max_y` 是所有塔坐标的最小/最大值。  
3. 只在这个更小的矩形里枚举整数点，计算质量，和暴力解的计算方式完全相同。  

**核心概念：**  
- **边界框（Bounding Box）**：把若干几何形状（这里是圆）外扩到一个矩形，方便离散枚举。  
- **字典序最小**：在 Python 中，列表比较会按元素顺序逐个比较，正好满足“先比较 x 再比较 y”。  

> 类比：把所有塔的信号覆盖范围看成一块“草地”，我们只需要在草地内部找最高点，而不必去草地外的荒原浪费时间。  

#### 代码（Python）  

```python
import math
from typing import List

def bestCoordinate(towers: List[List[int]], radius: int) -> List[int]:
    # 1️⃣ 计算所有塔的最小/最大坐标
    xs = [t[0] for t in towers]
    ys = [t[1] for t in towers]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # 2️⃣ 只遍历覆盖区域的外接矩形（并且保持非负）
    left   = max(0, min_x - radius)
    right  = max_x + radius
    bottom = max(0, min_y - radius)
    top    = max_y + radius

    best_quality = -1
    best_coord = [0, 0]

    # 3️⃣ 枚举矩形内的每个整数点
    for x in range(left, right + 1):
        for y in range(bottom, top + 1):
            total = 0
            # 4️⃣ 逐塔累计质量
            for tx, ty, q in towers:
                d = math.hypot(tx - x, ty - y)   # sqrt((dx)^2 + (dy)^2)
                if d <= radius:
                    total += int(q / (1 + d))
            # 5️⃣ 更新答案（质量更高或相等且字典序更小）
            if total > best_quality or (total == best_quality and [x, y] < best_coord):
                best_quality = total
                best_coord = [x, y]

    return best_coord
```

> **关键行解释**  
> - 第 5‑9 行：收集所有塔的 x、y，求出最左/最右、最下/最上位置。  
> - 第 12‑15 行：构造紧凑的搜索矩形，只要在此范围内遍历即可。  
> - 第 22 行：`math.hypot` 是 `sqrt(dx*dx + dy*dy)` 的简写，更直观。  
> - 第 27‑30 行：同暴力解的更新逻辑，利用列表比较实现字典序判断。  

#### 复杂度  

- **时间复杂度**：仍然是 `O((M+R)² · n)`，但实际遍历的格子数往往比最坏情况更少（因为我们把外部的“荒原”裁掉了）。  
  - 在极端情况下（比如所有塔都集中在左下角），搜索矩形的宽高仍然是 `≈ 2·radius + (max−min)`，与暴力解同阶，只是常数更小。  
- **空间复杂度**：`O(1)`，只用常数级额外变量。  

---

## 心得  

- **核心技巧**：**枚举 + 计算**（利用小输入规模） + **边界框裁剪**（只遍历可能的点）。  
- **此技巧适用的题型**  
  1. “在平面/网格上求最大/最小值”——如 LeetCode 1627 *Graph Connectivity With Threshold* 中的离散搜索。  
  2. “给定若干圆/矩形，求覆盖最多的整数点”——如 1732 *Find the Highest Altitude*（在离散坐标上累加）。  
  3. “小范围枚举 + 直接计算”——如 1452 *Maximum Number of Balls in a Box*（盒子容量小）。  
- **一句话总结解题钥匙**：**把搜索空间压到“所有可能出现最佳解的区域”，然后逐点穷举计算**。  

---

## 反思  

- **第一反应**：看到坐标范围不大，立刻想到“遍历所有整数点”。  
- **最容易踩的坑**  
  - **忘记限制坐标为非负**：题目要求返回非负坐标，搜索时要把左下角限制在 `0`。  
  - **距离判断的精度**：使用 `math.hypot`（或 `sqrt`）得到的浮点数可能出现极小误差，比较时使用 `<= radius` 足够安全。  
  - **字典序比较**：直接 `if total == best_quality and [x, y] < best_coord` 能一次性搞定，别忘了先判断质量相等再比较坐标。  
- **下次遇到同类题的第一步**：先估算**搜索空间大小**，若能在合理范围内完整枚举，就先写暴力版；随后思考如何**利用几何或数值边界**把空间进一步收紧。