# #1637. 最宽垂直区域（两点之间且不包含点） / Widest Vertical Area Between Two Points Containing No Points

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points/)

---

## 题目（英文原版）

**Description**

Given n points on a 2D plane where points[i] = [xi, yi], Return the widest vertical area between two points such that no points are inside the area.
A vertical area is an area of fixed-width extending infinitely along the y-axis (i.e., infinite height). The widest vertical area is the one with the maximum width.
Note that points on the edge of a vertical area are not considered included in the area.

**Examples**

**Example 1:**

```
Input: points = [[8,7],[9,9],[7,4],[9,7]]
Output: 1
Explanation: Both the red and the blue area are optimal.
```

**Example 2:**

```
Input: points = [[3,1],[9,0],[1,0],[1,4],[5,3],[8,8]]
Output: 3
```

**Constraints**

- n == points.length
- 2 <= n <= 105
- points[i].length == 2
- 0 <= xi, yi <= 109

---

## 题目（中文翻译）

给定平面上 **n** 个点，其中 `points[i] = [xi, yi]`，返回两个点之间的 **最宽垂直区域（vertical area）** 的宽度，使得该区域内部不包含任何点。  
垂直区域是指宽度固定、沿 **y** 轴无限延伸（即高度无限）的区域。宽度最大的垂直区域即为答案。  
注意，位于垂直区域边缘的点不算作位于区域内部。

**示例 1**  
**输入**: `points = [[8,7],[9,9],[7,4],[9,7]]`  
**输出**: `1`  
**解释**: 红色和蓝色两块区域的宽度都是最优的。

**示例 2**  
**输入**: `points = [[3,1],[9,0],[1,0],[1,4],[5,3],[8,8]]`  
**输出**: `3`

**约束条件**  
- `n == points.length`  
- `2 <= n <= 10^5`  
- `points[i].length == 2`  
- `0 <= xi, yi <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每两个点的 x 坐标之间的距离都算一遍，找出最大的那段**。  
因为题目要求“垂直区域”，也就是一条宽度固定、在 y 方向无限延伸的带子。只要这条带子左右两侧各有一个点，且带子内部不再出现其他点，它的宽度就是两点的 x 坐标差。

- **使用的数据结构**：我们只需要把所有点的 x 坐标取出来，放进一个普通的列表（list）里。列表就像一排排的抽屉，编号（下标）是顺序，里面装的就是每个点的横坐标。
- **为什么正确**：如果我们枚举所有点对 `(i, j)`，计算 `abs(xi - xj)`，那么一定会遍历到真正的最宽间隔对应的那两个点。因为题目只关心 x 方向的距离，y 完全不影响宽度。
- **时间/空间复杂度**：  
  - 我们要检查 `C(n,2) = n·(n-1)/2` 对点，时间随 `n²` 增长，记作 **O(n²)**。这里的 `O` 可以理解为“数量级”，比如 `n=10⁴` 时，`n²` 就是 1 亿次操作，明显会很慢。  
  - 只用了一个存放 x 坐标的列表，大小是 `n`，所以空间是 **O(n)**。

#### 代码（Python）

```python
from typing import List

def maxWidthOfVerticalArea_bruteforce(points: List[List[int]]) -> int:
    # 把所有 x 坐标抽出来，放进 list_x
    list_x = [p[0] for p in points]          # list_x[i] 对应第 i 个点的 x 坐标

    max_width = 0
    n = len(list_x)
    # 双层循环枚举所有点对 (i, j)
    for i in range(n):
        for j in range(i + 1, n):            # 只枚举一次，避免重复
            width = abs(list_x[i] - list_x[j])
            if width > max_width:
                max_width = width
    return max_width
```

#### 复杂度

- **时间复杂度**：O(n²) — 随着点的数量平方增长，点越多，运算次数会呈指数级增长，实际运行会非常慢。  
- **空间复杂度**：O(n) — 只额外存了一个长度为 n 的列表，用来保存 x 坐标。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈是大量的重复比较**。我们其实不需要比较每一对点，只要知道**相邻点的横坐标差**的最大值即可。原因如下：

1. 把所有点的 x 坐标从小到大排好序（想象把抽屉重新排列，左边的抽屉编号更小）。  
2. 排好序后，任意两点之间的宽度一定等于它们之间 **若干个相邻抽屉的差的累加**。  
3. 要想得到最大的宽度，显然应该挑选 **相邻抽屉之间最大的差**，因为如果我们跨过中间的点再去算宽度，那中间的点会把宽度拆成若干段，而其中必然有一段不比直接相邻的那段大。

所以，**只需要一次排序 + 一次遍历相邻差值**，即可得到答案。

- **核心算法/数据结构**：  
  - **排序**（Sorting）：把所有 x 坐标按从小到大排列。排序可以类比为把一堆乱序的书按照高度从低到高排好，方便后面快速找相邻的两本书。  
  - **遍历相邻差**：一次线性扫描，记录相邻两个坐标的差的最大值。

- **为什么这样更快**：排序的时间复杂度是 O(n log n)，比 O(n²) 大幅降低；遍历一次的时间是 O(n)。整体就是 **O(n log n)**，在 `n ≤ 10⁵` 的限制下完全可以接受。

#### 代码（Python）

```python
from typing import List

def maxWidthOfVerticalArea(points: List[List[int]]) -> int:
    # 1. 把所有 x 坐标提取出来
    xs = [p[0] for p in points]          # xs[i] 是第 i 个点的横坐标

    # 2. 对横坐标进行升序排序
    xs.sort()                            # 排好序后相邻元素的差才是我们关心的

    # 3. 扫描相邻差值，找出最大的那个
    max_width = 0
    for i in range(1, len(xs)):
        # 当前相邻两点的宽度
        cur_gap = xs[i] - xs[i - 1]      # 已经是正数，因为 xs 已经排好序
        if cur_gap > max_width:
            max_width = cur_gap

    return max_width
```

#### 复杂度

- **时间复杂度**：O(n log n) — 主要耗时在排序，`log n` 大约是 17（因为 2¹⁷≈10⁵），所以即使是 10⁵ 条数据也只需要几万次比较，跑得非常快。相较于暴力的 O(n²)，提升巨大。  
- **空间复杂度**：O(n) — 需要额外存储所有 x 坐标的列表，和输入规模相同。Python 的 `sort()` 是原地排序，额外的空间开销很小。

---

## 心得

- **核心技巧**：先把关键维度（这里是 x 坐标）排序，再只比较相邻元素的差值。  
- **适用的题型**：  
  1. “最大相邻差”类题目，如 LeetCode 164（最大间距）  
  2. “区间不重叠”类题目，需要把区间端点排序后线性扫描  
  3. “最近点对”在一维情况下的简化版（只需相邻差）  
- **解题钥匙**：**把问题降维 + 排序**，往往能把 O(n²) 的暴力直接压到 O(n log n) 或 O(n)。

---

## 反思

- **第一反应**：看到“宽度”，自然想到计算两点之间的距离，于是想到遍历所有点对（暴力）。  
- **最容易踩的坑**：  
  - 忽略了 y 坐标根本不影响答案，误把它当作二元比较的维度会导致不必要的复杂度。  
  - 没考虑“点在边缘不算”这一点，实际上只要相邻点的差就是合法的宽度，不需要额外减一。  
  - 对于只有两个点的极端情况，要确保代码仍然返回它们的差。  
- **下次遇到同类题**：第一步就问自己“哪个维度决定答案？”——找到关键维度后，立刻考虑 **排序 + 相邻比较**，往往能快速得到最优解。