# #1465. 水平和垂直切割后蛋糕块的最大面积 / Maximum Area of a Piece of Cake After Horizontal and Vertical Cuts

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-area-of-a-piece-of-cake-after-horizontal-and-vertical-cuts/)

---

## 题目（英文原版）

**Description**

You are given a rectangular cake of size h x w and two arrays of integers horizontalCuts and verticalCuts where:
Return the maximum area of a piece of cake after you cut at each horizontal and vertical position provided in the arrays horizontalCuts and verticalCuts. Since the answer can be a large number, return this modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: h = 5, w = 4, horizontalCuts = [1,2,4], verticalCuts = [1,3]
Output: 4 
Explanation: The figure above represents the given rectangular cake. Red lines are the horizontal and vertical cuts. After you cut the cake, the green piece of cake has the maximum area.
```

**Example 2:**

```
Input: h = 5, w = 4, horizontalCuts = [3,1], verticalCuts = [1]
Output: 6
Explanation: The figure above represents the given rectangular cake. Red lines are the horizontal and vertical cuts. After you cut the cake, the green and yellow pieces of cake have the maximum area.
```

**Example 3:**

```
Input: h = 5, w = 4, horizontalCuts = [3], verticalCuts = [3]
Output: 9
```

**Constraints**

- 2 <= h, w <= 109
- 1 <= horizontalCuts.length <= min(h - 1, 105)
- 1 <= verticalCuts.length <= min(w - 1, 105)
- 1 <= horizontalCuts[i] < h
- 1 <= verticalCuts[i] < w
- All the elements in horizontalCuts are distinct.
- All the elements in verticalCuts are distinct.

---

## 题目（中文翻译）

给定一个大小为 `h × w` 的矩形蛋糕，以及两个整数数组 `horizontalCuts`（水平切割） 和 `verticalCuts`（垂直切割），请在数组中提供的每个水平和垂直位置进行切割后，返回蛋糕块的最大面积。由于答案可能很大，请返回该面积对 `10^9 + 7` 取模后的结果。

## 示例

### 示例 1
**输入:** `h = 5, w = 4, horizontalCuts = [1,2,4], verticalCuts = [1,3]`  
**输出:** `4`  
**解释:** 上图展示了给定的矩形蛋糕，红色线段为水平切割和垂直切割的位置。切割完后，绿色的那块蛋糕拥有最大的面积。

### 示例 2
**输入:** `h = 5, w = 4, horizontalCuts = [3,1], verticalCuts = [1]`  
**输出:** `6`  
**解释:** 上图展示了给定的矩形蛋糕，红色线段为水平切割和垂直切割的位置。切割完后，绿色和黄色的两块蛋糕拥有相同的最大面积。

### 示例 3
**输入:** `h = 5, w = 4, horizontalCuts = [3], verticalCuts = [3]`  
**输出:** `9`

## 约束条件
- `2 <= h, w <= 10^9`
- `1 <= horizontalCuts.length <= min(h - 1, 10^5)`
- `1 <= verticalCuts.length <= min(w - 1, 10^5)`
- `1 <= horizontalCuts[i] < h`
- `1 <= verticalCuts[i] < w`
- `horizontalCuts` 中的所有元素互不相同。
- `verticalCuts` 中的所有元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有水平切割点和垂直切割点都列出来，**把蛋糕切成的每一块都算出来**，然后找出面积最大的那块。

- **数据结构**：  
  - `horizontalCuts`、`verticalCuts` 本身就是列表（list），可以把它们看成“切刀的位置”。  
  - 为了方便计算每块蛋糕的上下、左右边界，我们可以把原始的蛋糕边界（0 与 `h`、`w`）也加进去，形成完整的切割序列。把序列想象成一本字典，**键（key）**是切刀的位置，**值（value）**是对应的坐标。  
- **为什么正确**：  
  - 每一次水平切割把蛋糕分成若干横向的条带，每一次垂直切割再把每条带分成若干小块。遍历所有横向条带与所有纵向条带的组合，就能得到所有可能的块。  
- **复杂度分析（大白话）**：  
  - 如果水平切了 `m` 次，垂直切了 `n` 次，那么横向会产生 `m+1` 条带，纵向会产生 `n+1` 条块。我们要把这两组 **两两配对**，所以要做大约 `(m+1)*(n+1)` 次乘法和比较。  
  - 这在最坏情况下相当于 `O(m·n)`，当切割次数达到上限（约 `10^5`）时，计算量会天文级别，根本跑不完。  
  - 额外空间只用了几个临时列表，`O(m+n)`。

#### 代码（Python）

```python
def maxArea_bruteforce(h: int, w: int,
                       horizontalCuts: list[int],
                       verticalCuts: list[int]) -> int:
    MOD = 10**9 + 7

    # 把蛋糕的四条边也当作切割点加入，方便后面计算间距
    # 这里的 0 与 h（或 w）相当于字典的“页码”，指明了最上/左/下/右的边界
    h_cuts = [0] + sorted(horizontalCuts) + [h]
    v_cuts = [0] + sorted(verticalCuts) + [w]

    max_area = 0

    # 遍历每一条横向带（两条相邻水平切割之间的间距）
    for i in range(1, len(h_cuts)):
        height = h_cuts[i] - h_cuts[i - 1]   # 这块的高度
        # 对每一条纵向带（两条相邻垂直切割之间的间距）做同样的遍历
        for j in range(1, len(v_cuts)):
            width = v_cuts[j] - v_cuts[j - 1]   # 这块的宽度
            area = height * width
            if area > max_area:
                max_area = area

    return max_area % MOD
```

> **关键行注释**  
> - `h_cuts = [0] + sorted(horizontalCuts) + [h]`：把“蛋糕的上边缘 0”和“下边缘 h”也算进去，这样相邻两个切割点之间的差就是一块的高度。  
> - 双层 `for` 循环：穷举每一种高度 × 宽度的组合，得到所有块的面积。  

#### 复杂度

- **时间复杂度**：`O(m·n)`（`m = len(horizontalCuts)`，`n = len(verticalCuts)`）  
  - 用大白话来说，就是如果水平切了 1000 次、垂直切了 1000 次，就要算大约 1,000,000 次面积，这在实际运行时会非常慢。
- **空间复杂度**：`O(m + n)`  
  - 只用了两个额外的列表来存放排好序的切割点。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定最大面积的，是两次切割之间的最大间距**（即最大的高度和最大的宽度），而不是所有组合。我们只需要找出：

1. **水平切割中相邻两点的最大间距** → 最大的 `height`。  
2. **垂直切割中相邻两点的最大间距** → 最大的 `width`。

因为所有块都是 `height × width` 的形式，最大的块必然是“最高的那条横向带”乘以“最宽的那条纵向带”。这就把原本的 `O(m·n)` 降到了 `O(m log m + n log n)`（排序）或者 `O(m + n)`（如果已经排好序）。

**关键概念解释**  

- **排序（Sorting）**：把切割点从小到大排好，就像把一本字典的词条按字母顺序排列，找相邻词的距离非常容易。Python 的 `sorted()` 就是把列表“排好序”。  
- **最大间距（Maximum Gap）**：遍历排好序的切割点，计算相邻两点的差值，记录最大的那个差值。把这个过程想象成在数轴上画点，然后用尺子量每两个相邻点之间的距离，找最长的一段。  

**一步步推导**  

1. 把 `0`（蛋糕的起始边）和 `h`（或 `w`）加到切割数组的两端。这样我们就能直接比较“最上/左边缘”和第一个切割点之间的距离、以及“最后一个切割点”和最下/右边缘之间的距离。  
2. 对水平切割数组排序后，遍历一次，计算 `h_cuts[i] - h_cuts[i-1]`（相邻两点的距离），把最大的保存为 `max_h`。同理得到 `max_w`。  
3. 最大块的面积 = `max_h * max_w`，由于面积可能非常大，需要对 `10^9+7` 取模。  

#### 代码（Python）

```python
def maxArea(h: int, w: int,
           horizontalCuts: list[int],
           verticalCuts: list[int]) -> int:
    MOD = 10**9 + 7

    # 1️⃣ 把边界 0 与 h (w) 加进去，形成完整的切割序列
    h_cuts = [0] + sorted(horizontalCuts) + [h]
    v_cuts = [0] + sorted(verticalCuts) + [w]

    # 2️⃣ 找水平切割的最大间距
    max_h = 0
    for i in range(1, len(h_cuts)):
        gap = h_cuts[i] - h_cuts[i - 1]   # 两个相邻切点之间的距离
        if gap > max_h:
            max_h = gap

    # 3️⃣ 找垂直切割的最大间距
    max_w = 0
    for i in range(1, len(v_cuts)):
        gap = v_cuts[i] - v_cuts[i - 1]
        if gap > max_w:
            max_w = gap

    # 4️⃣ 计算最大面积并取模
    return (max_h * max_w) % MOD
```

> **关键行注释**  
> - `h_cuts = [0] + sorted(horizontalCuts) + [h]`：把“上边缘 0”和“下边缘 h”也算进去，这样最大间距可能出现在最边缘到第一刀之间或最后一刀到边缘之间。  
> - `gap = h_cuts[i] - h_cuts[i - 1]`：相邻两个切点之间的距离，就是一块的高度（或宽度）。  
> - 最后一步的 `% MOD`：防止整数溢出，保证答案在题目要求的范围内。

#### 复杂度

- **时间复杂度**：`O(m log m + n log n)`  
  - 这里的 `log` 来自排序。排序一次大约需要 `m·log m`（水平）和 `n·log n`（垂直）次比较。排序后只需要一次线性遍历，时间几乎可以忽略不计。相比暴力解的 `O(m·n)`，速度提升了好几个数量级。  
- **空间复杂度**：`O(m + n)`  
  - 额外存了排好序的两个列表。若在原数组上就地排序，额外空间甚至可以降到 `O(1)`（不计递归栈）。

---

## 心得

- **核心技巧**：**找最大间距**（Maximum Gap） + **排序**。这道题的关键不是枚举所有块，而是发现最大面积只由最大高度和最大宽度决定。  
- **适用的题型**  
  1. “最大子区间长度”类（如 `Maximum Distance Between Two Consecutive Elements`）。  
  2. “划分后最大/最小尺寸”类（如 `Maximum Width of a River`、`Maximum Area of Island` 中的类似思路）。  
- **一句话总结**：**先把切点排好序，只要找出相邻切点的最大距离，面积即是这两个最大距离的乘积**。

---

## 反思

- **第一反应**：想把所有块面积都算一遍，结果发现会超时。  
- **最容易踩的坑**  
  - 忘记把蛋糕的边界 `0` 与 `h`（或 `w`）加入切割数组，导致漏掉边缘到第一刀之间的间距。  
  - 没有对结果取模，导致大数溢出。  
  - 对 `horizontalCuts` 与 `verticalCuts` 的长度取了错误的上限，导致数组越界。  
- **下次遇到同类题**：**第一步**先思考“最大/最小值是否只和相邻元素有关”，如果是，就立即考虑**排序 + 线性扫描**，而不是暴力枚举所有组合。