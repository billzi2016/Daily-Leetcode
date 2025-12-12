# #3453. 分离正方形 I / Separate Squares I

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/separate-squares-i/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.
Find the minimum y-coordinate value of a horizontal line such that the total area of the squares above the line equals the total area of the squares below the line.
Answers within 10-5 of the actual answer will be accepted.
Note: Squares may overlap. Overlapping areas should be counted multiple times.

**Examples**

**Example 1:**

```
Input: squares = [[0,0,1],[2,2,1]]
Output: 1.00000
Explanation:

Any horizontal line between y = 1 and y = 2 will have 1 square unit above it and 1 square unit below it. The lowest option is 1.
```

**Example 2:**

```
Input: squares = [[0,0,2],[1,1,1]]
Output: 1.16667
Explanation:

The areas are:
Since the areas above and below the line are equal, the output is 7/6 = 1.16667 .
```

**Constraints**

- 1 <= squares.length <= 5 * 104
- squares[i] = [xi, yi, li]
- squares[i].length == 3
- 0 <= xi, yi <= 109
- 1 <= li <= 109
- The total area of all the squares will not exceed 1012.

---

## 题目（中文翻译）

你得到一个二维整数数组 **squares**。`squares[i] = [xi, yi, li]` 表示一个与 x 轴平行的正方形的左下角坐标 `(xi, yi)` 和边长 `li`。  
找出一条水平直线的最小 **y** 坐标，使得该直线上方的所有正方形面积之和等于该直线下方的所有正方形面积之和。  
答案只要在真实值的 `10⁻⁵` 以内即视为正确。  

**注意**：正方形之间可能会重叠，重叠区域应当被多次计入。  

#### 示例  

**示例 1**  
输入：`squares = [[0,0,1],[2,2,1]]`  
输出：`1.00000`  
解释：  
任意位于 `y = 1` 与 `y = 2` 之间的水平直线，上方的面积为 1 单位，下方的面积也为 1 单位。满足条件的最小 **y** 坐标为 1。  

**示例 2**  
输入：`squares = [[0,0,2],[1,1,1]]`  
输出：`1.16667`  
解释：  
计算得到的面积相等时，对应的 **y** 坐标为 `7/6 = 1.16667`。  

#### 约束条件  

- `1 <= squares.length <= 5 * 10⁴`  
- `squares[i] = [xi, yi, li]`  
- `squares[i].length == 3`  
- `0 <= xi, yi <= 10⁹`  
- `1 <= li <= 10⁹`  
- 所有正方形的总面积不超过 `10¹²`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的 y 坐标枚举一遍**，然后逐个计算：

1. 把水平线放在某个 y 值上。  
2. 对每个正方形，判断它在这条线上方占了多少面积（可以是全部、全部不算，或只算一半）。  
3. 把所有正方形的“上方面积”相加，记为 `above`。  
4. `below = total_area - above`（因为题目要求把重叠的面积算多次，所以总面积就是每个正方形的面积之和）。  
5. 检查 `above` 是否等于 `below`，如果相等就找到了答案。

> **类比**：想象我们在一本书的每一页上画一条横线，想知道这条线把书的“内容”均匀分成两半。最笨的办法就是把每一页的每一行都试一遍，看看哪一行最接近平分。

**为什么正确**：只要把所有可能的 y 都遍历到，必然会碰到使 `above = total/2` 的那个 y（或非常接近的 y），因为面积随 y 单调递增——线往上移动，上方面积只能增大。

**时间/空间分析**  

- 假设我们把 y 坐标离散成 `M` 个点（比如每 0.01 一个单位），每个点都要遍历 `N`（正方形数量）次。  
- **时间复杂度** 为 `O(N · M)`。如果 `N = 10⁵`、`M = 10⁶`（为了 1e‑5 精度），时间会爆炸。  
- **空间复杂度** 只需要保存输入数组，`O(N)`。

> **大白话**：`O(N·M)` 就像把 10 万个人每人排队 1 万次，显然跑不完。我们需要更聪明的方法。

---

#### 代码（Python）

```python
def brute_force(squares):
    # 计算总面积（重叠会被多算）
    total = sum(l * l for _, _, l in squares)

    # 取所有可能的 y，步长设得很小（这里仅作示例，实际会超时）
    step = 0.01                     # 为了演示，实际需要 1e-5 级别
    lo = min(y for _, y, _ in squares)
    hi = max(y + l for _, y, l in squares)

    y = lo
    while y <= hi:
        above = 0.0
        for x, bottom, l in squares:
            top = bottom + l
            if y <= bottom:                     # 整个正方形在上方
                above += l * l
            elif y >= top:                      # 整个正方形在下方
                continue
            else:                                # 只算线以上的那一段
                height = top - y
                above += height * l
        if abs(above - total / 2) < 1e-5:
            return y
        y += step
    return -1   # 未找到（理论上不会出现）
```

> **注释**  
> - `step` 越小精度越高，但循环次数会指数级增加。  
> - 这里的 `while` 循环相当于把所有可能的 y “排队” 检查。

#### 复杂度

- **时间复杂度**：`O(N · M)`，其中 `M` 是我们把区间离散成的点数。  
  - 例如 `N = 10⁵`、`M = 10⁶` → `10¹¹` 次操作，根本跑不完。  
- **空间复杂度**：`O(N)`，只存原始输入。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于 **遍历所有 y**。实际上，**面积随 y 单调递增**（线往上走，上方面积只会增加或保持不变），这正好满足 **二分查找**（Binary Search）的条件。

**关键观察**  

- 对于单个正方形 `[(xi, yi), side = li]`，设水平线的 y 为 `h`。  
  - 若 `h ≤ yi`，整块正方形都在水平线上方，贡献面积 `li²`。  
  - 若 `h ≥ yi + li`，整块正方形都在下方，贡献面积 `0`。  
  - 若 `yi < h < yi + li`，只算上方那段的面积：高度 = `(yi + li) - h`，宽度仍是 `li`，面积 = `li * ((yi + li) - h)`。

> **类比**：把每个正方形想象成一块巧克力棒，水平线像一把刀。刀从最底下切起，刀越往上切，切走的巧克力块（上方面积）只会变多，永不减少。

**二分搜索的实现**  

1. **搜索区间**  
   - 最低可能的 y：所有正方形的最小 `yi`（最底部）。  
   - 最高可能的 y：所有正方形的最大 `yi + li`（最高顶部）。  
2. **目标函数** `f(h) = 上方面积 - total/2`  
   - `f(h) < 0` → 线太低，上方面积不足，需要把线抬高。  
   - `f(h) > 0` → 线太高，上方面积过多，需要把线压低。  
3. **二分循环**：  
   - 取中点 `mid = (lo + hi) / 2`，计算 `above(mid)`。  
   - 根据 `above(mid)` 与 `total/2` 的大小关系收缩区间。  
   - 终止条件：区间宽度小于 `1e-6`（保证答案误差 ≤ 1e-5）。  

**计算 `above(h)` 的细节**（时间 `O(N)`）：

```python
def above_area(squares, h):
    area = 0.0
    for _, bottom, l in squares:
        top = bottom + l
        if h <= bottom:                # 整块在上方
            area += l * l
        elif h < top:                  # 部分在上方
            area += l * (top - h)      # height * width
        # else: h >= top → 贡献 0
    return area
```

**复杂度对比**  

- **二分搜索** 需要 `log2((hi-lo)/eps)` 次迭代，`eps≈1e-6`。区间长度最多是 `1e9`（坐标上限），所以迭代次数约为 `log2(1e15) ≈ 50`。  
- 每次迭代遍历所有正方形，时间 `O(N)`.  
- 总时间 `O(N·log(1/eps))`，约 `5·10⁶` 次基本操作，轻松通过限制。  
- 空间仍然只需存输入，`O(N)`。

---

#### 代码（Python）

```python
from typing import List

def separate_squares(squares: List[List[int]]) -> float:
    """
    二分答案，返回使上下面积相等的最小 y 坐标（误差 ≤ 1e-5）。
    """
    # 1. 预处理：总面积、搜索上下界
    total_area = 0.0
    lo = float('inf')
    hi = -float('inf')
    for _, y, l in squares:
        total_area += l * l                # 重叠面积算多次，直接累加
        lo = min(lo, y)                    # 最低可能的水平线
        hi = max(hi, y + l)                # 最高可能的水平线

    target = total_area / 2.0               # 目标上方面积

    # 2. 计算在高度 h 时，上方累计面积的函数
    def above(h: float) -> float:
        area = 0.0
        for _, bottom, l in squares:
            top = bottom + l
            if h <= bottom:                 # 整块在上方
                area += l * l
            elif h < top:                   # 部分在上方
                area += l * (top - h)       # (height above h) * width
            # else: 完全在下方，贡献 0
        return area

    # 3. 二分搜索，精度控制到 1e-6（比要求的 1e-5 更严格）
    eps = 1e-6
    while hi - lo > eps:
        mid = (lo + hi) / 2.0
        if above(mid) < target:             # 上方面积不足，需抬高线
            lo = mid
        else:                               # 上方面积已足，压低线
            hi = mid

    # 返回最小的满足条件的 y，取 hi（此时 hi≈lo，均满足条件）
    return hi
```

> **代码要点**  
> - `above` 每次遍历 `squares`，只做几次浮点运算，效率高。  
> - `while hi - lo > eps` 保证循环次数在 50 左右。  
> - 最后返回 `hi`（或 `lo`），两者相差不到 `1e-6`，满足题目误差要求。

#### 复杂度

- **时间复杂度**：`O(N · log( (max_y - min_y) / 1e-6 ))`  
  - 约等于 `O(N·50)` → 对 `N ≤ 5·10⁴` 完全够快。  
  - 与暴力 `O(N·M)` 相比，**快了几万甚至几百万倍**。  
- **空间复杂度**：`O(N)`，仅保存输入数组和少量临时变量。

---

## 心得

- **核心技巧**：利用面积随水平线位置单调递增的特性，使用 **二分搜索** 在实数范围内快速定位平分点。  
- **相似题型**  
  1. *“寻找中位数的水平切线”*（比如若干矩形的面积平分线）。  
  2. *“在若干区间上求面积相等的垂直线”*（如 `Separate Squares II`、`Minimum Height to Balance`）。  
  3. *“在一维数组中找满足累计和等于目标的阈值”*（前缀和 + 二分）。  
- **一句话总结**：**面积是单调函数 → 用二分把答案逼到 1e‑5 以内**。

---

## 反思

- **第一反应**：直接枚举 y、逐个计算面积，结果显而易见会超时。  
- **最容易踩的坑**  
  - 忘记 **重叠面积要计多次**，误以为需要做集合并。  
  - 计算 **部分覆盖面积** 时写错公式（应是 `l * (top - h)`，而不是 `l * (h - bottom)`）。  
  - 终止条件不够严格，导致误差超过 `1e-5`（需要把精度设为 `1e-6` 或更小）。  
- **下次类似题**：第一步立刻判断 **单调性**（是递增还是递减），随后 **二分答案** 而不是枚举。这样能把时间从指数级压到对数级。