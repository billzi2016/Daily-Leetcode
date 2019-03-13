# #335. 路径交叉 / Self Crossing

> 难度：困难 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/self-crossing/)

---

## 题目（英文原版）

**Description**

You are given an array of integers distance.
You start at the point (0, 0) on an X-Y plane, and you move distance[0] meters to the north, then distance[1] meters to the west, distance[2] meters to the south, distance[3] meters to the east, and so on. In other words, after each move, your direction changes counter-clockwise.
Return true if your path crosses itself or false if it does not.

**Examples**

**Example 1:**

```
Input: distance = [2,1,1,2]
Output: true
Explanation: The path crosses itself at the point (0, 1).
```

**Example 2:**

```
Input: distance = [1,2,3,4]
Output: false
Explanation: The path does not cross itself at any point.
```

**Example 3:**

```
Input: distance = [1,1,1,2,1]
Output: true
Explanation: The path crosses itself at the point (0, 0).
```

**Constraints**

- 1 <= distance.length <= 105
- 1 <= distance[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `distance`。  
你从坐标原点 \((0, 0)\) 开始，在 X‑Y 平面上按以下顺序移动：先向北（north）移动 `distance[0]` 米，然后向西（west）移动 `distance[1]` 米，再向南（south）移动 `distance[2]` 米，接着向东（east）移动 `distance[3]` 米，如此循环。换句话说，每走完一步后，方向按逆时针（counter‑clockwise）方向旋转。  
若路径的某一点与之前走过的路径相交，则返回 `true`；否则返回 `false`。

**示例**  

示例 1  
```
Input: distance = [2,1,1,2]
Output: true
Explanation: 路径在点 (0, 1) 处相交。
```

示例 2  
```
Input: distance = [1,2,3,4]
Output: false
Explanation: 路径在任何位置都没有相交。
```

示例 3  
```
Input: distance = [1,1,1,2,1]
Output: true
Explanation: 路径在点 (0, 0) 处相交。
```

**约束条件**  
- `1 <= distance.length <= 10^5`  
- `1 <= distance[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每一步走的线段都记下来，然后每走完一段就去检查它是否和**之前的任意一段**相交。  
- **数据结构**：我们可以把每条线段用「起点」和「终点」的坐标 `(x1, y1, x2, y2)` 存在一个列表里。列表就像一本「旅行日志」，每翻一页就能看到之前走过的路。  
- **为什么正确**：只要有两条线段相交，说明路径在某个点上交叉了，返回 `True`；如果所有线段两两都不相交，则路径永远不自交，返回 `False`。  
- **复杂度分析**：  
  - 对于第 `i` 条新线段，我们要和前面的 `i‑1` 条线段全部比较一次。于是比较次数大约是 `1 + 2 + … + (n‑1) = n·(n‑1)/2`，这就是 **O(n²)**。  
  - 空间方面我们要保存所有已经走过的线段，最多 `n` 条，故是 **O(n)**。  
  - 用大白话说，`O(n²)` 就像「你要和每个人都握手」——如果有 10,000 步，就要握手 100,000,000 次，明显太慢了。

#### 代码（Python）

```python
from typing import List

def is_self_crossing_bruteforce(distance: List[int]) -> bool:
    # 记录所有走过的线段，格式为 (x1, y1, x2, y2)
    segments = []
    # 当前坐标
    x, y = 0, 0
    # 方向的循环序列：北、西、南、东 …（逆时针）
    dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    for i, d in enumerate(distance):
        dx, dy = dirs[i % 4]          # 取本步的方向向量
        nx, ny = x + dx * d, y + dy * d   # 计算步结束后的新坐标

        # 检查新线段 (x, y) -> (nx, ny) 是否和已有任意线段相交
        for (x1, y1, x2, y2) in segments:
            if intersect(x, y, nx, ny, x1, y1, x2, y2):
                return True

        # 把新线段加入日志
        segments.append((x, y, nx, ny))
        x, y = nx, ny   # 更新当前位置

    return False


def intersect(ax, ay, bx, by, cx, cy, dx, dy) -> bool:
    """
    判断两条线段 (a,b) 与 (c,d) 是否相交。
    这里所有线段都是水平或垂直的，判交可以简化为区间重叠判断。
    """
    # 先把每条线段归一化，使 (x1,y1) 为左/下端点，(x2,y2) 为右/上端点
    if ax > bx or ay > by:  # 水平线段
        ax, bx = bx, ax
    if cx > dx or cy > dy:  # 竖直线段
        cx, dx = dx, cx

    # 横竖相交的情况
    if ax == bx:  # a-b 是竖直线
        if cy == dy:  # c-d 是水平线
            return (cx <= ax <= dx) and (ay <= cy <= by)
    elif ay == by:  # a-b 是水平线
        if cx == dx:  # c-d 是竖直线
            return (ax <= cx <= bx) and (cy <= ay <= dy)

    # 同向（都水平或都竖直）且重叠的情况
    if ax == bx == cx == dx:  # 都是竖直线
        return max(ay, cy) <= min(by, dy)
    if ay == by == cy == dy:  # 都是水平线
        return max(ax, cx) <= min(bx, dx)

    return False
```

> 关键行中文注释已经写在代码里，直接运行即可看到结果（注意 `intersect` 只处理轴对齐的线段，这正好符合题目每一步都是上下左右走的特点）。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每走一步要和之前所有步比较，步数越多，比较次数呈二次增长。  
- **空间复杂度**：`O(n)`  
  - 需要保存每一步的起止坐标，最坏情况下要存 `n` 条线段。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每一步都要遍历全部历史**。其实我们可以发现，路径的自交只能在**最近的几条线段**之间产生，远离的线段已经不可能再相交。  
把路径想象成螺旋式的走法：  

1. **第一种形态**：路径像「向外扩张的正方形」——每一步都比前一步长。此时不可能自交。  
2. **第二种形态**：当第 4 步（`i = 3`）的长度 **不大于** 第 2 步时，会出现第一种自交（第 4 步与第 1 步相交）。  
3. **第三种形态**：以后出现的自交，只会在**相隔 3、4、5 步**的线段之间。也就是说，第 `i` 步只需要和 `i‑3`、`i‑4`、`i‑5` 步比较。

基于这个观察，我们只需要 **常数空间**（只保存最近的 6 条距离）就能判断是否自交。下面把三种可能的交叉情况写成判断式：

| 情形 | 说明 | 判断条件 |
|------|------|----------|
| **Case 1**（第 4 步与第 1 步相交） | `i ≥ 3` 且 `distance[i] ≥ distance[i‑2]` 且 `distance[i‑1] ≤ distance[i‑3]` | `d[i] >= d[i-2] and d[i-1] <= d[i-3]` |
| **Case 2**（第 5 步与第 1 步相交，形成「凹陷」） | `i ≥ 4` 且 `distance[i-1] == distance[i-3]` 且 `distance[i] + distance[i-4] >= distance[i-2]` | `d[i-1] == d[i-3] and d[i] + d[i-4] >= d[i-2]` |
| **Case 3**（第 6 步与第 1 步相交，形成「更复杂的交叉」） | `i ≥ 5` 且 `distance[i-2] >= distance[i-4]` 且 `distance[i] >= distance[i-2] - distance[i-4]` 且 `distance[i-1] >= distance[i-3] - distance[i-5]` 且 `distance[i-1] <= distance[i-3]` | `d[i-2] >= d[i-4] and d[i] >= d[i-2] - d[i-4] and d[i-1] >= d[i-3] - d[i-5] and d[i-1] <= d[i-3]` |

只要出现任意一种情况，就说明路径自交。

> **为什么只需要检查这几种情况？**  
> 想象路径在平面上画出来，方向是北→西→南→东→北…。当我们向北走第 `i` 步时，最有可能相交的只能是**向南的第 `i‑2` 步**（相隔两步），或者**向东的第 `i‑3` 步**（相隔三步），更远的线段要么已经被更靠近的线段遮挡，要么根本不在同一直线上。于是只要把这几条「最近的」线段的长度关系写成不等式，就能完整覆盖所有可能的交叉。

#### 代码（Python）

```python
from typing import List

def is_self_crossing(distance: List[int]) -> bool:
    """
    O(n) 时间、O(1) 空间的最优解。
    只检查最近的 6 条距离，依据上面的三个交叉案例。
    """
    d = distance  # 为了书写更简洁

    for i in range(len(d)):
        # ----- Case 1：第 i 条线段与第 i-3 条相交 -----
        # 需要 i >= 3 才能取到 i-3
        if i >= 3 and d[i] >= d[i-2] and d[i-1] <= d[i-3]:
            return True

        # ----- Case 2：第 i 条线段与第 i-4 条相交（形成凹陷） -----
        # 需要 i >= 4 才能取到 i-4
        if i >= 4 and d[i-1] == d[i-3] and d[i] + d[i-4] >= d[i-2]:
            return True

        # ----- Case 3：第 i 条线段与第 i-5 条相交（更复杂的交叉） -----
        # 需要 i >= 5 才能取到 i-5
        if (i >= 5 and
            d[i-2] >= d[i-4] and
            d[i] >= d[i-2] - d[i-4] and
            d[i-1] >= d[i-3] - d[i-5] and
            d[i-1] <= d[i-3]):
            return True

    return False
```

> 代码里每个 `if` 前都有中文注释，帮助你对照上表快速定位对应的交叉情形。只遍历一次数组，空间只用了几个临时变量，满足 `O(1)` 额外空间。

#### 复杂度

- **时间复杂度**：`O(n)` — 只需要一次线性遍历，`n` 是步数。相比暴力的 `O(n²)`，大幅提升（相当于「只和前面的人握一次手」）。
- **空间复杂度**：`O(1)` — 只用了常数个变量，不随 `n` 增长。相当于「只带了一本小笔记本」而不是记录全部路径。

---

## 心得

- **核心技巧**：把看似几何的「自交」问题转化为**相邻若干段长度的比较**，利用路径的方向规律（逆时针）归纳出固定的几种交叉模式。  
- **适用的题型**：  
  1. **Self Crossing**（本题）  
  2. **Spiral Matrix / Turtle Graphics** 系列——需要根据方向和步长判断是否越界或相交。  
  3. **Robot Bounded In Circle**——判断机器人轨迹是否形成闭环，思路同样是利用方向周期性。  
- **一句话总结解题钥匙**：**“自交只会在最近的 3~5 条线段之间发生，用固定的几条不等式一次遍历全部步长即可”。**

---

## 反思

- **第一反应**：看到“每一步方向逆时针”，立刻想到把路径画在坐标系里，用线段相交检测。于是写出了暴力的 O(n²) 方案。  
- **最容易踩的坑**：  
  - 忘记处理**特殊的凹陷情况**（Case 2），导致在 `[1,1,1,2,1]` 这类输入上错误。  
  - 边界判断不严谨，例如 `i‑5` 时要确保数组长度足够，否则会出现索引错误。  
  - 对于同向（水平‑水平、垂直‑垂直）重叠的情况，需要明确只比较最近的几段，否则会误判。  
- **下次遇到同类题**：第一步先**画图并观察**，找出“最近几条线段”之间的几何关系，再**把关系写成不等式**，最后用一次遍历验证。这样既能保证正确性，又能得到最优的时间/空间表现。