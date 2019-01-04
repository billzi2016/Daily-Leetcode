# #223. 矩形面积 / Rectangle Area

> 难度：中等 · 标签：Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/rectangle-area/)

---

## 题目（英文原版）

**Description**

Given the coordinates of two rectilinear rectangles in a 2D plane, return the total area covered by the two rectangles.
The first rectangle is defined by its bottom-left corner (ax1, ay1) and its top-right corner (ax2, ay2).
The second rectangle is defined by its bottom-left corner (bx1, by1) and its top-right corner (bx2, by2).

**Examples**

**Example 1:**

```
Input: ax1 = -3, ay1 = 0, ax2 = 3, ay2 = 4, bx1 = 0, by1 = -1, bx2 = 9, by2 = 2
Output: 45
```

**Example 2:**

```
Input: ax1 = -2, ay1 = -2, ax2 = 2, ay2 = 2, bx1 = -2, by1 = -2, bx2 = 2, by2 = 2
Output: 16
```

**Constraints**

- -104 <= ax1 <= ax2 <= 104
- -104 <= ay1 <= ay2 <= 104
- -104 <= bx1 <= bx2 <= 104
- -104 <= by1 <= by2 <= 104

---

## 题目（中文翻译）

给定平面上两个轴对齐矩形（axis-aligned rectangle）的坐标，返回这两个矩形覆盖的总面积。  
第一个矩形由左下角 (ax1, ay1) 和右上角 (ax2, ay2) 定义。  
第二个矩形由左下角 (bx1, by1) 和右上角 (bx2, by2) 定义。

**示例 1：**  
**示例 2：**  

**约束条件：**

- -10⁴ ≤ ax1 ≤ ax2 ≤ 10⁴  
- -10⁴ ≤ ay1 ≤ ay2 ≤ 10⁴  
- -10⁴ ≤ bx1 ≤ bx2 ≤ 10⁴  
- -10⁴ ≤ by1 ≤ by2 ≤ 10⁴  

**示例：**  

**示例 1:**  
```
Input: ax1 = -3, ay1 = 0, ax2 = 3, ay2 = 4, bx1 = 0, by1 = -1, bx2 = 9, by2 = 2
Output: 45
```

**示例 2:**  
```
Input: ax1 = -2, ay1 = -2, ax2 = 2, ay2 = 2, bx1 = -2, by1 = -2, bx2 = 2, by2 = 2
Output: 16
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两个矩形里所有的“格子”都枚举出来，然后把它们放进一个集合（`set`）中去重，最后集合的大小就是两个矩形的并集面积。

- **数据结构**：这里用到的集合（`set`）可以类比为“一个只能装唯一物品的盒子”。往里面放东西时，如果已经有相同的东西了，盒子会自动把它拒绝，这正好对应了“去重”。  
- **为什么正确**：每个格子（用整数坐标表示的 1×1 小正方形）只会被算一次。所有格子都放进集合后，集合的元素个数正好等于被两个矩形覆盖的总格子数，也就是我们要求的面积。  
- **时间/空间复杂度**：  
  - 时间上要遍历矩形内部的每一个格子，格子数等于矩形的面积，所以是 **O(area₁ + area₂)**。如果两个矩形都很大（比如坐标在 ±10⁴），面积会达到 10⁸ 甚至更高，执行起来会很慢。  
  - 空间上要把所有格子存进集合，同样是 **O(area₁ + area₂)**，最坏情况下需要和遍历的时间一样多的内存。

> **大白话**：`O(n²)` 里，`n` 代表“每条边的长度”。如果把矩形看成棋盘，遍历每个格子相当于把整块棋盘的每一格都检查一遍，耗时会随棋盘面积呈二次增长。

#### 代码（Python）

```python
def computeArea_bruteforce(ax1, ay1, ax2, ay2,
                          bx1, by1, bx2, by2):
    # 用 set 保存所有被覆盖的格子坐标 (x, y)
    covered = set()

    # 第一个矩形：遍历左下角到右上角的每一个整数格子
    for x in range(ax1, ax2):          # 左闭右开，正好对应每个宽度为 1 的格子
        for y in range(ay1, ay2):
            covered.add((x, y))       # 加入集合，重复的格子会自动去重

    # 第二个矩形，同理
    for x in range(bx1, bx2):
        for y in range(by1, by2):
            covered.add((x, y))

    # 集合的大小就是并集面积
    return len(covered)


# ---------- 测试 ----------
print(computeArea_bruteforce(-3, 0, 3, 4, 0, -1, 9, 2))   # 45
print(computeArea_bruteforce(-2, -2, 2, 2, -2, -2, 2, 2)) # 16
```

> 代码每行都加了中文注释，帮助你对照思路。

#### 复杂度

- **时间复杂度**：`O(area₁ + area₂)`  
  - 这里的 `area₁ = (ax2-ax1)*(ay2-ay1)`，`area₂ = (bx2-bx1)*(by2-by1)`。如果矩形很大，时间会线性增长到几亿次循环，实际运行会很慢。
- **空间复杂度**：`O(area₁ + area₂)`  
  - 需要把所有格子坐标存进集合，最坏情况下占用的内存和遍历的格子数一样多。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐格子枚举**——我们把每个格子都当作独立的对象去处理，导致时间和空间都随面积线性增长。实际上，矩形的面积可以直接用宽度 × 高度算出来，不需要逐格子检查。

两个矩形的并集面积 = **矩形 A 的面积 + 矩形 B 的面积 - 重叠部分的面积**。  
所以核心任务是求出**两个矩形的交叉面积**，如果它们不相交，交叉面积就是 0。

求交叉面积的关键在于**找出在 x 方向和 y 方向上都重叠的区间**：

- 在 **x 方向**，左边的边界是 `max(ax1, bx1)`（取两条左边界中更靠右的），右边的边界是 `min(ax2, bx2)`（取两条右边界中更靠左的）。如果左边界大于或等于右边界，说明在 x 方向没有重叠，交叉宽度为 0。
- **y 方向** 同理：`max(ay1, by1)` 为下边界，`min(ay2, by2)` 为上边界。

交叉宽度 `overlap_width = max(0, min(ax2, bx2) - max(ax1, bx1))`  
交叉高度 `overlap_height = max(0, min(ay2, by2) - max(ay1, by1))`  

交叉面积 = `overlap_width * overlap_height`（如果任意一个为 0，面积自然为 0）。

整个过程只用了几次常数时间的比较与加减运算，**不需要遍历任何格子**，因此是最优的 O(1) 解法。

> **类比**：想象两块地的投影在水平和垂直方向上分别投下影子，交叉面积就是两条水平影子重叠的宽度乘以两条垂直影子重叠的高度。只要先算出影子重叠的长度，就能直接得到交叉面积。

#### 代码（Python）

```python
def computeArea(ax1, ay1, ax2, ay2,
                bx1, by1, bx2, by2):
    """
    返回两个轴平行矩形的并集面积
    """
    # 1️⃣ 先算各自的面积
    area_a = (ax2 - ax1) * (ay2 - ay1)   # 矩形 A 的宽 × 高
    area_b = (bx2 - bx1) * (by2 - by1)   # 矩形 B 的宽 × 高

    # 2️⃣ 计算在 x 方向的重叠宽度
    overlap_width = max(0, min(ax2, bx2) - max(ax1, bx1))
    # 3️⃣ 计算在 y 方向的重叠高度
    overlap_height = max(0, min(ay2, by2) - max(ay1, by1))

    # 4️⃣ 重叠面积（若不相交则为 0）
    overlap_area = overlap_width * overlap_height

    # 5️⃣ 并集面积 = 两矩形面积之和 - 重叠面积
    return area_a + area_b - overlap_area


# ---------- 测试 ----------
print(computeArea(-3, 0, 3, 4, 0, -1, 9, 2))   # 45
print(computeArea(-2, -2, 2, 2, -2, -2, 2, 2)) # 16
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做了常数次的加、减、乘、比较，和输入规模无关。  
  - 与暴力解相比，时间从“随面积线性增长”瞬间降到了“永远只需要几步”。
- **空间复杂度**：`O(1)` — 只用了若干个整数变量，未使用额外的容器。

---

## 心得

- **核心技巧**：**利用几何的投影思想求交叉区间**，即在每个维度上分别求重叠长度，再相乘得到交叉面积。  
- **适用的题型**  
  1. 两个或多个 **轴平行矩形** 的并集/交集面积（如 LeetCode 191. Number of 1 Bits 的变形）。  
  2. **线段覆盖** 类问题：求两条线段的交集长度。  
  3. **二维区间相交** 判断：判断两个矩形是否相交（只需要判断 `overlap_width>0 && overlap_height>0`）。
- **一句话总结解题钥匙**：**先算各自面积，再减去“重复计数的交叉面积”。**  

---

## 反思

- **拿到题目第一反应**：先想把两个矩形“每个格子都点出来”，因为最直观的做法就是把所有点收集进集合去重。  
- **最容易踩的坑**  
  - **边界条件**：如果两矩形只在边上相接（例如右边界恰好等于左边界），交叉宽度/高度应为 0，不能出现负数。使用 `max(0, …)` 可以安全处理。  
  - **坐标顺序**：题目保证 `ax1 ≤ ax2`、`by1 ≤ by2`，但如果自行实现时忘记检查，可能导致宽或高为负数。  
  - **整数溢出**：在某些语言里宽度乘以高度可能超过 32 位整数范围，Python 的整数是大整数，不会溢出，但在 C/C++ 中需要使用 `long long`。  
- **下次遇到同类题，第一步该想到**：**先把每个维度的交集长度算出来**（`max(left1, left2)` 与 `min(right1, right2)`），再用这些长度来构造交叉面积或判断是否相交。这样可以直接跳过“逐格子枚举”的低效思路。