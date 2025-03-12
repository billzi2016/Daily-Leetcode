# #3102. 最小化曼哈顿距离 / Minimize Manhattan Distances

> 难度：困难 · 标签：Array、Math、Geometry、Sorting、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/minimize-manhattan-distances/)

---

## 题目（英文原版）

**Description**

You are given an array points representing integer coordinates of some points on a 2D plane, where points[i] = [xi, yi].
The distance between two points is defined as their Manhattan distance.
Return the minimum possible value for maximum distance between any two points by removing exactly one point.

**Examples**

**Example 1:**

```
Input: points = [[3,10],[5,15],[10,2],[4,4]]
Output: 12
Explanation:
The maximum distance after removing each point is the following:
12 is the minimum possible maximum distance between any two points after removing exactly one point.
```

**Example 2:**

```
Input: points = [[1,1],[1,1],[1,1]]
Output: 0
Explanation:
Removing any of the points results in the maximum distance between any two points of 0.
```

**Constraints**

- 3 <= points.length <= 105
- points[i].length == 2
- 1 <= points[i][0], points[i][1] <= 108

---

## 题目（中文翻译）

给定一个数组 **points**，表示平面上若干点的整数坐标，其中 `points[i] = [xi, yi]`。  
两点之间的距离定义为它们的曼哈顿距离（Manhattan distance）。  
移除恰好一个点后，返回任意两点之间的最大距离的最小可能取值。

Example 1:  
Example 2:  
Constraints:

示例 1:  
Input: points = [[3,10],[5,15],[10,2],[4,4]]  
Output: 12  
Explanation:  
移除每个点后对应的最大距离如下所示：  
12 是在恰好移除一个点后，任意两点之间的最大距离的最小可能值。

示例 2:  
Input: points = [[1,1],[1,1],[1,1]]  
Output: 0  
Explanation:  
移除任意一个点后，任意两点之间的最大距离均为 0。

约束条件：  
- 3 <= points.length <= 10^5  
- points[i].length == 2  
- 1 <= points[i][0], points[i][1] <= 10^8

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**要删除的那个点，然后在剩下的点里逐对计算曼哈顿距离，找出最大的那个距离，记为 `cur_max`。对每一个可能被删掉的点都这样做，最后把所有 `cur_max` 中的最小值返回。

- **使用的数据结构**：  
  - **二维列表** `points` 保存所有坐标。  
  - **两层循环**：外层遍历要删除的点 `i`，内层遍历剩余点 `j,k` 计算 `|xj‑xk|+|yj‑yk|`。  
  - 可以把 “所有点的集合” 想象成一本电话簿，暴力做法就是把每个人的号码都两两拨出来比较，显然非常耗时。

- **为什么正确**：  
  - 我们把所有可能的删除方案都尝试了一遍，并且对每种方案都精确算出了剩余点的最大曼哈顿距离。  
  - 只要把所有方案的答案取最小，就一定是全局最优解。

- **复杂度分析**：  
  - 对每个点 `i`（共 `n` 个），我们都要在剩下的 `n‑1` 个点里做两两比较，次数是 `C(n‑1,2) = (n‑1)*(n‑2)/2`。  
  - 所以总的时间复杂度是 **O(n³)**（实际上是 `n * (n‑1) * (n‑2) / 2`，但我们只说 `O(n³)` 方便记忆），这在 `n ≤ 10⁵` 时根本不可接受。  
  - 只用了原始的点列表，没有额外的空间，空间复杂度是 **O(1)**（不计输入本身）。

> **大白话**：`O(n³)` 就像把 1000 本书的每一页都和每一本书的每一页互相比对，根本不可能在一分钟内完成。

---

#### 代码（Python）

```python
from typing import List

def minMaxManhattan_bruteforce(points: List[List[int]]) -> int:
    n = len(points)
    ans = float('inf')
    # 枚举要删除的点 i
    for i in range(n):
        cur_max = 0
        # 在剩余点里两两比较
        for j in range(n):
            if j == i:                     # 被删掉的点直接跳过
                continue
            for k in range(j + 1, n):
                if k == i:
                    continue
                # 曼哈顿距离 = |xj-xk| + |yj-yk|
                d = abs(points[j][0] - points[k][0]) + \
                    abs(points[j][1] - points[k][1])
                cur_max = max(cur_max, d)   # 记录当前方案的最大距离
        ans = min(ans, cur_max)            # 取所有方案的最小值
    return ans
```

> 代码可以直接运行，但在 `n=10⁵` 时会卡死。

#### 复杂度  

- **时间复杂度**：`O(n³)` — 需要遍历三层循环，随着点的数量呈立方增长，实际不可用。  
- **空间复杂度**：`O(1)` — 只用了常数级的临时变量。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“两两比较所有点的距离”**。  
观察曼哈顿距离的特殊结构可以把它压缩成只关心 **四个极值**，从而把 `O(n²)` 的比较降到 `O(1)`。

---

**关键观察 1：曼哈顿距离的四种写法**  

对任意两点 `(xi, yi)`、`(xj, yj)`：

```
|xi-xj| + |yi-yj|
= max( (xi-xj)+(yi-yj),
        (xi-xj)-(yi-yj),
       -(xi-xj)+(yi-yj),
       -(xi-xj)-(yi-yj) )
```

把 `(xi, yi)` 变换为两个新坐标：

```
u_i = xi + yi
v_i = xi - yi
```

则上式等价于  

```
max( |u_i - u_j| , |v_i - v_j| )
```

也就是说，两个点的曼哈顿距离 = **它们在 u 轴上的距离** 与 **在 v 轴上的距离** 的较大者。

---

**关键观察 2：整组点的最大曼哈顿距离**  

设所有点的 `u` 最大值为 `Umax`，最小值为 `Umin`，`v` 最大值为 `Vmax`，最小值为 `Vmin`。  
则整组点的 **最大** 曼哈顿距离就是：

```
max( Umax - Umin , Vmax - Vmin )
```

因为只要挑出在 u 方向最远的两点或在 v 方向最远的两点，它们的距离就已经是全局最大。

---

**关键观察 3：删除一个点只会影响极值**  

当我们删除某个点 `(x, y)`（对应 `u, v`），**只有** 当这个点是当前 `Umax`、`Umin`、`Vmax` 或 `Vmin` 中的 **唯一拥有者** 时，极值才会改变。  
如果它不是极值，或者极值还有其它点共享，那么删除它对最大距离没有影响。

因此，只要我们事先知道每个方向的 **第一大/小** 与 **第二大/小**（以及它们的出现次数），就可以 **在 O(1) 时间** 判断删除任意一点后新的极值是什么，进而得到新的最大曼哈顿距离。

---

**实现步骤**  

1. **预处理**  
   - 遍历一次数组，计算每个点的 `u = x + y`、`v = x - y`，并存入列表。  
   - 同时记录  
     - `Umax`、`Usecond_max`、`Umax_cnt`（最大值、次大值、最大值出现次数）  
     - `Umin`、`Usecond_min`、`Umin_cnt`（最小值、次小值、最小值出现次数）  
     - `Vmax`、`Vsecond_max`、`Vmax_cnt`、`Vmin`、`Vsecond_min`、`Vmin_cnt`  
   - 这一步是 **O(n)**。

2. **枚举删除点**（仍然是 O(n)）  
   - 对每个点的 `u, v`，分别判断它是否是唯一的极值。  
   - 若是唯一极大（或极小），使用对应的次极大（或次极小）代替；否则仍使用原极值。  
   - 计算 `cur = max(new_Umax - new_Umin, new_Vmax - new_Vmin)`。  
   - 更新答案 `ans = min(ans, cur)`。

3. **返回答案**。

---

**为什么是最优**  

- 只遍历了两遍数组，时间复杂度 **O(n)**，在 `n ≤ 10⁵` 时完全可接受。  
- 只用了若干整数变量和两个长度为 `n` 的列表（存 `u`、`v`），空间复杂度 **O(n)**。  
- 通过数学变换把原本需要两两比较的二次关系压缩到四个极值的比较，避免了所有冗余计算。

---

#### 代码（Python）

```python
from typing import List

def minMaxManhattan(points: List[List[int]]) -> int:
    n = len(points)

    # 1️⃣ 计算旋转坐标 u = x + y, v = x - y
    u = [0] * n
    v = [0] * n
    for i, (x, y) in enumerate(points):
        u[i] = x + y
        v[i] = x - y

    # 2️⃣ 统计四个方向的极值及其出现次数
    # 初始化为极端值，后面会被实际数据覆盖
    Umax, Usecond_max = -10**20, -10**20
    Umin, Usecond_min = 10**20, 10**20
    Vmax, Vsecond_max = -10**20, -10**20
    Vmin, Vsecond_min = 10**20, 10**20
    Umax_cnt = Umin_cnt = Vmax_cnt = Vmin_cnt = 0

    for val in u:
        # 最大值 & 次大值
        if val > Umax:
            Usecond_max, Umax = Umax, val
            Umax_cnt = 1
        elif val == Umax:
            Umax_cnt += 1
        elif val > Usecond_max:
            Usecond_max = val

        # 最小值 & 次小值
        if val < Umin:
            Usecond_min, Umin = Umin, val
            Umin_cnt = 1
        elif val == Umin:
            Umin_cnt += 1
        elif val < Usecond_min:
            Usecond_min = val

    for val in v:
        if val > Vmax:
            Vsecond_max, Vmax = Vmax, val
            Vmax_cnt = 1
        elif val == Vmax:
            Vmax_cnt += 1
        elif val > Vsecond_max:
            Vsecond_max = val

        if val < Vmin:
            Vsecond_min, Vmin = Vmin, val
            Vmin_cnt = 1
        elif val == Vmin:
            Vmin_cnt += 1
        elif val < Vsecond_min:
            Vsecond_min = val

    # 3️⃣ 枚举删除每个点，计算新的最大曼哈顿距离
    ans = float('inf')
    for i in range(n):
        # 处理 u 方向的极值
        if u[i] == Umax and Umax_cnt == 1:
            cur_Umax = Usecond_max
        else:
            cur_Umax = Umax

        if u[i] == Umin and Umin_cnt == 1:
            cur_Umin = Usecond_min
        else:
            cur_Umin = Umin

        # 处理 v 方向的极值
        if v[i] == Vmax and Vmax_cnt == 1:
            cur_Vmax = Vsecond_max
        else:
            cur_Vmax = Vmax

        if v[i] == Vmin and Vmin_cnt == 1:
            cur_Vmin = Vsecond_min
        else:
            cur_Vmin = Vmin

        # 该删除方案的最大曼哈顿距离
        cur = max(cur_Umax - cur_Umin, cur_Vmax - cur_Vmin)
        ans = min(ans, cur)

    return ans
```

> 代码已完整注释，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了三次（一次算 `u/v`，一次统计极值，一次枚举删除），每次都是线性操作。  
  - 与暴力解的 `O(n³)` 相比，速度提升了 **n²** 量级（比如 `n=10⁵` 时从天年级降到几毫秒）。

- **空间复杂度**：`O(n)`  
  - 需要保存 `u`、`v` 两个长度为 `n` 的数组。  
  - 只用了若干整数变量，额外空间很小。

---

## 心得  

- **核心技巧**：把曼哈顿距离通过坐标旋转（`u = x + y`、`v = x - y`）转化为 **两条轴的 Chebyshev 距离**，从而只需要关注 **四个极值**（最大/最小的 `u`、`v`）。  
- **适用的题型**：  
  1. “删除若干点后，使最大 Manhattan 距离最小” 系列（如本题）。  
  2. “求一组点的 Manhattan 直径（最大距离）” 或 “求最小包围盒的边长”。  
  3. “在平面上找最大/最小 Manhattan 距离的两点对” 的变体。  
- **一句话总结**：**把 Manhattan 距离拆成两条独立的“一维极值差”，只要维护好极大/极小及其第二极值，就能在 O(n) 内完成所有删点的评估。**

---

## 反思  

- **第一反应**：直接两两比较，写出暴力枚举。  
- **最容易踩的坑**：  
  - 忘记统计极值的出现次数，导致当多个点共享同一个极值时错误地使用次极值。  
  - 边界情况：`n = 3` 时删除后只剩两点，仍然可以使用相同公式；若所有点完全重合，极值差为 0，需要保证次极值也被正确初始化（使用足够小/大的哨兵值）。  
- **下次遇到同类题**：第一步先**思考能否把二维距离压缩到一维极值**，即寻找可以“线性化”或“旋转坐标”的技巧，然后再关注极值的维护。这样往往能把二次甚至三次的暴力直接降到线性。