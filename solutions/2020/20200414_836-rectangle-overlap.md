# #836. 矩形重叠 / Rectangle Overlap

> 难度：简单 · 标签：Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/rectangle-overlap/)

---

## 题目（英文原版）

**Description**

An axis-aligned rectangle is represented as a list [x1, y1, x2, y2], where (x1, y1) is the coordinate of its bottom-left corner, and (x2, y2) is the coordinate of its top-right corner. Its top and bottom edges are parallel to the X-axis, and its left and right edges are parallel to the Y-axis.
Two rectangles overlap if the area of their intersection is positive. To be clear, two rectangles that only touch at the corner or edges do not overlap.
Given two axis-aligned rectangles rec1 and rec2, return true if they overlap, otherwise return false.

**Examples**

**Example 1:**

```
Input: rec1 = [0,0,2,2], rec2 = [1,1,3,3]
Output: true
```

**Example 2:**

```
Input: rec1 = [0,0,1,1], rec2 = [1,0,2,1]
Output: false
```

**Example 3:**

```
Input: rec1 = [0,0,1,1], rec2 = [2,2,3,3]
Output: false
```

**Constraints**

- rec1.length == 4
- rec2.length == 4
- -109 <= rec1[i], rec2[i] <= 109
- rec1 and rec2 represent a valid rectangle with a non-zero area.

---

## 题目（中文翻译）

一个轴对齐矩形（axis-aligned rectangle）用列表 `[x1, y1, x2, y2]` 表示，其中 `(x1, y1)` 为左下角坐标，`(x2, y2)` 为右上角坐标。矩形的上、下边平行于 X 轴，左、右边平行于 Y 轴。  

当两个矩形的交集面积大于 0 时，它们被认为是重叠的。需要注意，若两个矩形仅在边缘或角点相触，则 **不算** 重叠。  

给定两个轴对齐矩形 `rec1` 和 `rec2`，如果它们重叠返回 `true`，否则返回 `false`。

## 示例

### 示例 1
**输入:** `rec1 = [0,0,2,2]`, `rec2 = [1,1,3,3]`  
**输出:** `true`

### 示例 2
**输入:** `rec1 = [0,0,1,1]`, `rec2 = [1,0,2,1]`  
**输出:** `false`

### 示例 3
**输入:** `rec1 = [0,0,1,1]`, `rec2 = [2,2,3,3]`  
**输出:** `false`

## 约束条件

- `rec1.length == 4`
- `rec2.length == 4`
- `-10^9 <= rec1[i], rec2[i] <= 10^9`
- `rec1` 和 `rec2` 表示面积非零的合法矩形

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直观的想法是把两个矩形的每一个**整数网格点**都枚举出来，看看有没有点同时落在两个矩形内部。  
- **数据结构**：我们可以把每个矩形内部的点装进一个 `set`（集合），就像把词装进字典里，词是点坐标，字典的“页码”是`True`，可以快速判断一个点是否出现过。  
- **为什么正确**：如果两个矩形真的有正面积的交集，那么必然会有至少一个点同时属于两个集合，遍历完后只要发现这样的点就说明相交。  
- **复杂度分析**：  
  - 假设第一个矩形宽为 `w1 = x2 - x1`，高为 `h1 = y2 - y1`，点的总数是 `w1 * h1`（这里我们把坐标都当成整数），第二个矩形同理。最坏情况下我们要遍历两者所有点，所以时间复杂度大约是 **O(w1·h1 + w2·h2)**。如果把矩形的宽高都记成 `n`，则近似为 **O(n²)**，也就是“平方级”，意思是随着矩形边长增长，耗时会呈二次方增长。  
  - 需要额外的集合来保存点，空间复杂度同样是 **O(w1·h1 + w2·h2)**，即“和输入一样多的空间”。  

> 这里的暴力解其实在实际面试里几乎不可接受，因为坐标范围可以很大（甚至到 `10⁹`），根本不可能把所有点都列举出来。但它帮助我们先从最容易理解的角度确认“只要有共同点就算相交”。

#### 代码（Python）

```python
def isRectangleOverlap_brute(rec1, rec2):
    # 把矩形 1 的所有整数点放进集合
    points = set()
    x1, y1, x2, y2 = rec1
    for x in range(x1, x2):          # 右边界不包括在内，防止只碰边的情况
        for y in range(y1, y2):
            points.add((x, y))

    # 遍历矩形 2 的每个点，看看是否已经在集合里
    a1, b1, a2, b2 = rec2
    for x in range(a1, a2):
        for y in range(b1, b2):
            if (x, y) in points:    # 找到共同点，说明有正面积交集
                return True
    return False                     # 没有任何共同点
```

#### 复杂度  

- **时间复杂度**：`O(w1·h1 + w2·h2)` → 在最坏情况下约为 `O(n²)`，表示随矩形边长平方增长。  
- **空间复杂度**：`O(w1·h1 + w2·h2)` → 需要存储所有点的集合，同样随面积线性增长。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，真正的“瓶颈”在于我们**枚举了所有点**。实际上我们根本不需要逐点检查，只要比较两条**投影区间**（在 X 轴和 Y 轴上的投影）是否有交集即可。  

- **投影区间**：把矩形看成两根 **数轴上的线段**。  
  - 在 X 方向，矩形 1 投影为 `[x1, x2)`，矩形 2 为 `[a1, a2)`。  
  - 在 Y 方向，同理为 `[y1, y2)` 与 `[b1, b2)`。  
- **相交条件**：如果这两根线段在 **任意一个方向** 完全不重叠（即左边的右端点 ≤ 右边的左端点），那么矩形一定不相交。反之，只有当 X 方向和 Y 方向的投影 **都** 有正长度的交集时，矩形才会有正面积的交集。  
- **为什么不包括等号**：题目说明“只碰边或角算不相交”，所以我们使用 **半开区间** `[left, right)`，左闭右开；当右端点等于左端点时，交集长度为 0，代表仅仅相触，不算重叠。  

> 类比：想象两块木板分别放在水平和垂直的轨道上。如果在水平轨道上它们的投影没有重叠（即一块木板完全在另一块左边或右边），那无论垂直方向怎么摆，它们也不可能相交。  

#### 代码（Python）

```python
def isRectangleOverlap(rec1, rec2):
    """
    判断两个轴对齐矩形是否有正面积交集。
    思路：分别检查 X、Y 方向的投影是否都有交集。
    """
    x1, y1, x2, y2 = rec1
    a1, b1, a2, b2 = rec2

    # 若在 X 方向上不重叠，直接返回 False
    # x2 <= a1  表示 rec1 完全在 rec2 的左侧（或仅在左边缘相触）
    # a2 <= x1  表示 rec2 完全在 rec1 的左侧
    if x2 <= a1 or a2 <= x1:
        return False

    # 若在 Y 方向上不重叠，直接返回 False
    if y2 <= b1 or b2 <= y1:
        return False

    # 两个方向都有交集，说明有正面积的重叠
    return True
```

#### 复杂度  

- **时间复杂度**：`O(1)` → 只做了几次常数次的比较，不随输入大小变化。相较于暴力解的 `O(n²)`，提升巨大。  
- **空间复杂度**：`O(1)` → 只用了若干个临时变量，额外空间几乎为零。  

---

## 心得  

- **核心技巧**：把几何相交问题转化为**一维区间交集**的判断。  
- **适用题型**：  
  1. 判断两个线段是否相交（LeetCode 793）  
  2. 判断两个圆是否相交（可把圆投影到 X/Y 轴上做区间比较）  
  3. 多个矩形是否有公共区域（同理使用区间交集的思想）  
- **解题钥匙**：**“投影 + 区间不相交即整体不相交”**。

## 反思  

- **第一反应**：直接想到把所有点枚举出来检查是否有公共点。  
- **最容易踩的坑**：忘记题目要求“仅相触不算相交”，导致使用 `<=` 而不是 `<`，从而把边界相接的情况误判为相交。  
- **下次第一步**：先把二维几何问题抽象成“一维投影”，检查每个方向的区间是否有正交集。这样既能避免细节错误，又能立刻得到最优的 `O(1)` 解法。