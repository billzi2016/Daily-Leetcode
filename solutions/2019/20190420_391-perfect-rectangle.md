# #391. 完美矩形 / Perfect Rectangle

> 难度：困难 · 标签：Array、Hash Table、Math、Geometry、Line Sweep · [LeetCode 链接](https://leetcode.com/problems/perfect-rectangle/)

---

## 题目（英文原版）

**Description**

Given an array rectangles where rectangles[i] = [xi, yi, ai, bi] represents an axis-aligned rectangle. The bottom-left point of the rectangle is (xi, yi) and the top-right point of it is (ai, bi).
Return true if all the rectangles together form an exact cover of a rectangular region.

**Examples**

**Example 1:**

```
Input: rectangles = [[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]]
Output: true
Explanation: All 5 rectangles together form an exact cover of a rectangular region.
```

**Example 2:**

```
Input: rectangles = [[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]]
Output: false
Explanation: Because there is a gap between the two rectangular regions.
```

**Example 3:**

```
Input: rectangles = [[1,1,3,3],[3,1,4,2],[1,3,2,4],[2,2,4,4]]
Output: false
Explanation: Because two of the rectangles overlap with each other.
```

**Constraints**

- 1 <= rectangles.length <= 2 * 104
- rectangles[i].length == 4
- -105 <= xi < ai <= 105
- -105 <= yi < bi <= 105

---

## 题目（中文翻译）

给定一个数组 `rectangles`，其中 `rectangles[i] = [xi, yi, ai, bi]` 表示一个轴对齐矩形（axis-aligned rectangle）。该矩形的左下角坐标为 `(xi, yi)`，右上角坐标为 `(ai, bi)`。  
如果所有矩形恰好覆盖成一个完整的矩形区域（exact cover of a rectangular region），返回 `true`；否则返回 `false`。

**示例 1**  
**示例 2**  
**示例 3**  

### 示例

#### 示例 1
```text
Input: rectangles = [[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]]
Output: true
Explanation: 所有 5 个矩形恰好组成了一个完整的矩形区域的完全覆盖。
```

#### 示例 2
```text
Input: rectangles = [[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]]
Output: false
Explanation: 两个矩形区域之间存在空隙，因此未形成完整的覆盖。
```

#### 示例 3
```text
Input: rectangles = [[1,1,3,3],[3,1,4,2],[1,3,2,4],[2,2,4,4]]
Output: false
Explanation: 有两个矩形相互重叠，导致覆盖不完整。
```

### 约束条件
- `1 <= rectangles.length <= 2 * 10^4`
- `rectangles[i].length == 4`
- `-10^5 <= xi < ai <= 10^5`
- `-10^5 <= yi < bi <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有矩形两两比较，确认**没有任何重叠**，并且**没有留下空洞**。  
具体可以这样做：

1. **遍历所有矩形**，记录下它们的左下角、右上角坐标，用来算出 **所有矩形的最左下点** 与 **最右上点**（这两个点决定了整个覆盖区域的外边框）。
2. **计算每个矩形的面积**，把所有面积加起来得到 `total_area`。
3. **两两检查是否有重叠**。如果两矩形在 x 方向有交集且在 y 方向也有交集，就说明它们重叠了，直接返回 `False`。
4. **判断是否有空洞**：如果没有重叠，且 `total_area` 正好等于外边框的面积（`(max_x - min_x) * (max_y - min_y)`），则说明矩形们刚好填满了外边框，没有空洞，返回 `True`；否则返回 `False`。

> **类比**：把每个矩形想象成一块拼图，先把所有拼图的边缘找出来（外框），再检查每块拼图之间是否有“压在一起”的情况（重叠），最后确认拼出来的面积恰好和外框面积相等——这就是“没有空洞、没有重叠、正好填满”。

**为什么这个方法正确**  
- 如果出现 **重叠**，必然会导致 `total_area` 大于外框面积，或者我们在第 3 步已经直接检测到并返回 `False`。
- 如果出现 **空洞**（即有未被任何矩形覆盖的区域），则 `total_area` 必然小于外框面积，因为我们只把真实的矩形面积相加。

只要同时满足 **无重叠** 且 **面积相等**，就能保证所有矩形恰好拼成一个完整的大矩形。

#### 代码（Python）

```python
from typing import List

def is_rectangle_cover_bruteforce(rectangles: List[List[int]]) -> bool:
    # ---------- 第一步：找外层矩形的左下角和右上角 ----------
    min_x = min(rect[0] for rect in rectangles)   # 最左的 x
    min_y = min(rect[1] for rect in rectangles)   # 最下的 y
    max_x = max(rect[2] for rect in rectangles)   # 最右的 x
    max_y = max(rect[3] for rect in rectangles)   # 最上的 y

    # ---------- 第二步：累计所有小矩形的面积 ----------
    total_area = 0
    for x1, y1, x2, y2 in rectangles:
        total_area += (x2 - x1) * (y2 - y1)

    # ---------- 第三步：两两检查是否有重叠 ----------
    n = len(rectangles)
    for i in range(n):
        x1, y1, x2, y2 = rectangles[i]
        for j in range(i + 1, n):
            a1, b1, a2, b2 = rectangles[j]
            # 判断在 x、y 两个方向是否都有交集
            if not (x2 <= a1 or a2 <= x1 or y2 <= b1 or b2 <= y1):
                # 只要有一次交集就说明重叠
                return False

    # ---------- 第四步：比较面积 ----------
    outer_area = (max_x - min_x) * (max_y - min_y)
    return total_area == outer_area
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  这里的 `n` 是矩形的数量。最耗时的步骤是两两比较是否重叠，需要遍历 `n*(n-1)/2` 对矩形。用大白话说，就是如果有 10,000 个矩形，就要检查大约 5,000 万次——这在实际中会慢得不耐烦。

- **空间复杂度**：`O(1)`（不计输入本身）  
  只用了几个整数来保存最小/最大坐标和面积，总占用的额外内存几乎是常数级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **两两比较**——`O(n²)` 的时间在 `n` 达到 2·10⁴ 时根本跑不完。  
我们需要一种 **只遍历一次**（或线性遍历）就能判断“是否有重叠、是否有空洞”的方法。

观察下面两点可以帮助我们做到这一点：

1. **面积相等**：如果所有小矩形恰好拼成一个大矩形，所有小矩形的面积之和必然等于外层大矩形的面积（同上一步的第 4 步）。这一步仍然是 `O(n)`，只需要一次遍历即可得到 `total_area` 与外框坐标。

2. **角点出现的次数**：  
   - 在一个完整的大矩形里，**只有四个角**（左下、左上、右下、右上）会出现 **一次**。  
   - 其他所有内部的点（包括小矩形的角点）要么被 **两块** 矩形共享一次（形成内部边），要么被 **四块** 矩形共享一次（形成内部交叉点），因此它们出现的次数一定是 **偶数**（2 次或 4 次）。

   基于这个观察，我们可以把所有小矩形的四个角点放进一个 **哈希集合**（Python 的 `set`），每次遇到一个角点：
   - 如果它不在集合里，就 **加入**（第一次出现）。
   - 如果它已经在集合里，就 **删除**（第二次出现抵消掉）。
   - 这样，所有出现偶数次的点最终都会被删掉，只剩下出现奇数次的点。

   最后，**集合里应该恰好剩下外层大矩形的四个角**，且这四个角必须和我们在第 1 步求出的外框坐标相同。

> **类比**：把每个角点想成一本“借书卡”。第一次出现时我们把卡片放进盒子，第二次出现时我们把卡片从盒子里拿走。真正的“借书卡”只会出现一次的，就是四个外角。若盒子里剩下的卡片不是这四个，说明有“多借”或“少借”，即有重叠或空洞。

**完整的判定条件**（全部满足才返回 `True`）：

- `total_area == outer_area`（面积相等）。
- `corner_set` 中恰好有四个点，且这四个点正好是外框的四个角。

这两个条件一起保证了**没有重叠、没有空洞、恰好覆盖**。

#### 代码（Python）

```python
from typing import List, Tuple

def is_rectangle_cover(rectangles: List[List[int]]) -> bool:
    """
    最优解：一次遍历 + 哈希集合（角点计数）
    """
    # ---------- 1. 统计外框坐标和所有小矩形的面积 ----------
    min_x = min(rect[0] for rect in rectangles)
    min_y = min(rect[1] for rect in rectangles)
    max_x = max(rect[2] for rect in rectangles)
    max_y = max(rect[3] for rect in rectangles)

    total_area = 0
    corners = set()                     # 用来存放出现奇数次的角点

    for x1, y1, x2, y2 in rectangles:
        # 累加面积
        total_area += (x2 - x1) * (y2 - y1)

        # 当前矩形的四个角
        rect_corners: Tuple[Tuple[int, int], ...] = (
            (x1, y1),  # 左下
            (x1, y2),  # 左上
            (x2, y1),  # 右下
            (x2, y2),  # 右上
        )

        # 把每个角加入/删除集合，实现“出现偶数次则消除”
        for pt in rect_corners:
            if pt in corners:
                corners.remove(pt)   # 第二次出现，抵消
            else:
                corners.add(pt)      # 第一次出现，加入

    # ---------- 2. 检查面积 ----------
    outer_area = (max_x - min_x) * (max_y - min_y)
    if total_area != outer_area:
        return False

    # ---------- 3. 检查角点集合 ----------
    expected_corners = {(min_x, min_y), (min_x, max_y),
                        (max_x, min_y), (max_x, max_y)}
    return corners == expected_corners
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需要一次遍历每个矩形，所有操作（面积累加、集合的增删）都是 **常数时间**。用大白话说，就是如果有 20,000 个矩形，只会处理 20,000 次，跑得飞快。

- **空间复杂度**：`O(n)`（最坏情况）  
  集合里最多会存下每个矩形的四个角（如果所有角都不相同），所以空间与矩形数量成线性关系。不过实际情况往往会有很多角相互抵消，集合大小通常很小——只剩下四个外角。

---

## 心得

- **核心技巧**：**面积相等 + 角点出现次数**（即“奇数出现的角点必须恰好是外层矩形的四个角”）。  
- **适用场景**：  
  1. **拼图类几何覆盖**（如 LeetCode 391 Perfect Rectangle、LeetCode 850 Rectangle Area II）  
  2. **判断多个区间是否恰好覆盖一个大区间**（一维版本的相同思路）  
  3. **判断若干线段是否组成闭合多边形**（利用端点出现次数的奇偶性）

- **一句话总结解题钥匙**：  
  > “把所有小矩形的面积加起来，看是否等于外框面积；再把所有角点用‘出现奇偶抵消’的方式筛选，最后只剩四个外角——这两个条件一起就能保证恰好覆盖且不重叠。”

---

## 反思

- **第一反应**：看到“是否恰好覆盖一个矩形”，自然会想到先比较面积，再检查是否有重叠或空洞。最直接的实现往往是两两比较，这就是暴力思路。

- **最容易踩的坑**  
  1. **漏掉负坐标**：题目允许坐标为负数，计算面积时一定要用 `(right - left) * (top - bottom)`，不能直接相乘坐标本身。  
  2. **角点集合的比较**：一定要把外层四个角点写成 **集合** 再比较，否则顺序不同会导致错误。  
  3. **大数溢出**（在 C++/Java 中要注意），在 Python 整数不溢出，但仍要保证使用 `int` 而不是 `float`，否则精度会出错。

- **下次遇到同类题，第一步该想到**：  
  - **“面积相等 + 奇数角点”** 这套“全局 + 局部”判定法。先用面积快速排除大多数不合法情况，再用角点的奇偶特性验证是否真的拼成了一个完整的矩形。这样既省时又稳妥。