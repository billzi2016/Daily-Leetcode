# #3111. 最少矩形覆盖点数 / Minimum Rectangles to Cover Points

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-rectangles-to-cover-points/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array points, where points[i] = [xi, yi]. You are also given an integer w. Your task is to cover all the given points with rectangles.
Each rectangle has its lower end at some point (x1, 0) and its upper end at some point (x2, y2), where x1 <= x2, y2 >= 0, and the condition x2 - x1 <= w must be satisfied for each rectangle.
A point is considered covered by a rectangle if it lies within or on the boundary of the rectangle.
Return an integer denoting the minimum number of rectangles needed so that each point is covered by at least one rectangle.
Note: A point may be covered by more than one rectangle.

**Examples**

**Example 1:**

```
Input: points = [[2,1],[1,0],[1,4],[1,8],[3,5],[4,6]], w = 1
Output: 2
Explanation:
The image above shows one possible placement of rectangles to cover the points:
```

**Example 2:**

```
Input: points = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]], w = 2
Output: 3
Explanation:
The image above shows one possible placement of rectangles to cover the points:
```

**Example 3:**

```
Input: points = [[2,3],[1,2]], w = 0
Output: 2
Explanation:
The image above shows one possible placement of rectangles to cover the points:
```

**Constraints**

- 1 <= points.length <= 105
- points[i].length == 2
- 0 <= xi == points[i][0] <= 109
- 0 <= yi == points[i][1] <= 109
- 0 <= w <= 109
- All pairs (xi, yi) are distinct.

---

## 题目（中文翻译）

你得到一个二维整数数组 `points`，其中 `points[i] = [xi, yi]` 表示第 *i* 个点的坐标。同时给定一个整数 `w`。你的任务是使用矩形（rectangle）覆盖所有给定的点。

每个矩形的下端位于某点 `(x1, 0)`，上端位于某点 `(x2, y2)`，并且满足 `x1 <= x2`、`y2 >= 0`，以及 **宽度约束** `x2 - x1 <= w`。  

如果一个点位于矩形的内部或恰好在矩形的边界上，则认为该点被该矩形覆盖。

返回一个整数，表示至少需要多少个矩形，使得每个点至少被一个矩形覆盖。  
**注意**：一个点可以被多个矩形覆盖。

---

### 示例

**示例 1**  
```text
Input: points = [[2,1],[1,0],[1,4],[1,8],[3,5],[4,6]], w = 1
Output: 2
Explanation:
上图展示了一种可能的矩形放置方式，使得所有点均被覆盖。
```

**示例 2**  
```text
Input: points = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]], w = 2
Output: 3
Explanation:
上图展示了一种可能的矩形放置方式，使得所有点均被覆盖。
```

**示例 3**  
```text
Input: points = [[2,3],[1,2]], w = 0
Output: 2
Explanation:
上图展示了一种可能的矩形放置方式，使得所有点均被覆盖。
```

---

### 约束条件

- `1 <= points.length <= 10^5`
- `points[i].length == 2`
- `0 <= xi == points[i][0] <= 10^9`
- `0 <= yi == points[i][1] <= 10^9`
- `0 <= w <= 10^9`
- 所有点 `(xi, yi)` 均互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个点都单独用一个矩形**，因为题目只要求「每个点至少被一个矩形覆盖」，不要求矩形之间不能重叠。  
实现上可以这样：

1. 维护一个集合 `uncovered` 保存还没有被覆盖的点。  
2. 每次从 `uncovered` 中随便挑一个点 `(x, y)`，把它当作矩形的左下角 `(x, 0)`，再随便选一个合法的右上角 `(x, y)`（只要 `x - x ≤ w`），这相当于只覆盖这一个点。  
3. 把被覆盖的点从 `uncovered` 中删掉，计数 `ans += 1`。  
4. 重复步骤 2~3，直到所有点都被删光。

> **类比**：把每个点想成一本书，暴力解就是每本书都买一个专门的书架，虽然能把所有书都收好，但显然浪费空间。

这个方法一定能得到答案，因为每个点最终都会被某个矩形覆盖，只是可能用了很多不必要的矩形。

#### 代码（Python）

```python
from typing import List, Set, Tuple

def min_rectangles_bruteforce(points: List[List[int]], w: int) -> int:
    # 把点转成 tuple，方便放进 set
    uncovered: Set[Tuple[int, int]] = { (x, y) for x, y in points }
    ans = 0

    while uncovered:
        # 随便挑一个点作为左下角
        x0, y0 = next(iter(uncovered))
        # 只覆盖这个点（最保守的做法），相当于矩形宽度为 0
        # 只要满足 x0 - x0 <= w，显然成立
        uncovered.remove((x0, y0))
        ans += 1          # 用掉了一个矩形

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况每次都要遍历集合找点并删除，集合的 `remove` 平均是 `O(1)`，但我们要进行 `n` 次循环，每次都要从集合里挑点，整体仍是线性遍历 `n` 次，实际是 `O(n)`，但因为这是一种“每点单独一个矩形”的思路，真正的 **最优解** 需要更高效的算法，这里只做概念展示）。  
- **空间复杂度**：`O(n)`，需要存储所有未覆盖的点。

> **大白话**：时间复杂度的 `O(n²)` 可以想成「如果有 1000 个点，程序大概要跑 1000 × 1000 = 100 万次操作」，这在 10⁵ 规模的输入下会非常慢。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键在于如何一次性覆盖尽可能多的点**。  
观察题目：

- 矩形的下边界永远是 `y = 0`，所以只要 `x` 坐标在区间 `[x1, x2]` 且 `x2 - x1 ≤ w`，点就一定能被覆盖，**点的 `y` 完全不影响是否能被同一个矩形覆盖**（提示里已经说了）。
- 因此我们只需要关心 `x` 坐标，把每个点看成“一条竖直的线”。  
- 若把所有 `x` 排序，从左到右扫描，**每次都把左边最小的未覆盖点 `x0` 选进一个新矩形的左端**，然后把 **所有 `x ≤ x0 + w` 的点**都一次性覆盖掉。这样做显然是最省矩形的，因为左端选得越左，能够覆盖的点越多。

这就是经典的**贪心区间覆盖**（类似「给定若干点，最少多少段长度为 `w` 的线段能覆盖所有点」）：

1. 把所有点的 `x` 提取出来并排序。  
2. 用指针 `i` 指向当前未被覆盖的最左点。  
3. 设 `start = xs[i]` 为本次矩形的左端，则右端可以伸到 `start + w`。  
4. 再用指针 `j` 向右移动，直到 `xs[j] > start + w` 为止，`[i, j-1]` 之间的点全部被当前矩形覆盖。  
5. 计数 `ans += 1`，把 `i` 移到 `j`，继续下一轮。

> **类比**：想象你在地上画一条长度为 `w` 的刷子，一次可以刷掉所有在刷子范围内的点。每次把刷子左边贴到最左边未被刷到的点上，就能一次性刷掉最多的点。

#### 代码（Python）

```python
from typing import List

def min_rectangles(points: List[List[int]], w: int) -> int:
    """
    贪心：一次性覆盖尽可能多的 x 坐标
    """
    # 1. 只关心 x 坐标，提取后排序
    xs = sorted(p[0] for p in points)   # 类似把所有点的横坐标排成一本字典

    n = len(xs)
    i = 0          # 当前未覆盖的最左点的下标
    ans = 0        # 需要的矩形数

    while i < n:
        # 2. 以 xs[i] 为左端，右端最多可以到 xs[i] + w
        start = xs[i]
        right_limit = start + w

        # 3. 向右扫描，找到第一个超出区间的点
        j = i
        while j < n and xs[j] <= right_limit:
            j += 1    # 这个点还能被当前矩形覆盖

        # 4. 现在 [i, j) 之间的点全被一个矩形覆盖
        ans += 1
        i = j        # 继续从下一个未覆盖的点开始

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，随后一次线性扫描 `O(n)`，所以整体是 `O(n log n)`。  
  - **含义**：如果有 10⁵ 个点，排序大约需要 10⁵ × log₂10⁵ ≈ 10⁵ × 17 ≈ 1.7 百万次比较，完全可以在一秒内完成。

- **空间复杂度**：`O(n)`（存储排序后的 `xs` 列表）。如果在原地排序并直接遍历 `points`，可以把空间降到 `O(1)`，但对初学者保持 `O(n)` 更易理解。

> 与暴力解相比，时间从可能的 `O(n²)` 降到了 `O(n log n)`，在大数据量下快了几百倍。

---

## 心得

- **核心技巧**：**贪心 + 按 x 排序的区间覆盖**。  
- 这类技巧常用于「最少多少个固定长度的区间能覆盖所有点」的问题，典型的还有：  
  1. **“最少相扑手”**（给定点，最少多少根长度为 `L` 的线段覆盖）  
  2. **“加油站排队”**（每辆车只能在长度为 `w` 的加油站区间内加油）  
- **解题钥匙**：**“一次把左边最远的点尽可能往右覆盖”。**  

---

## 反思

- **第一反应**：看到矩形的宽度限制 `x2 - x1 ≤ w`，立刻想到“固定宽度的区间”，于是把点的 `x` 抽出来，忽略 `y`。  
- **最容易踩的坑**：  
  - 忘记 `y` 完全不影响答案，误把 `y` 也加入排序或判断条件。  
  - `w = 0` 的特殊情况：每个不同的 `x` 必须单独一个矩形，代码仍能正确处理，因为 `right_limit = start + 0`。  
  - 大数值 `xi`（最高 10⁹）不会导致溢出，因为 Python 整数任意大。  
- **下次第一步**：**把所有点的关键维度（这里是 `x`）抽出来排序**，然后思考“怎样一次性覆盖最多的未覆盖元素”。这几乎是所有「最少区间」贪心题的统一思路。