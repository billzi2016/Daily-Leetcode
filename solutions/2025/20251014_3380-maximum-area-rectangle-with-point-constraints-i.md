# #3380. 点约束下的最大面积矩形 I / Maximum Area Rectangle With Point Constraints I

> 难度：中等 · 标签：Array、Math、Binary Indexed Tree、Segment Tree、Geometry、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-area-rectangle-with-point-constraints-i/)

---

## 题目（英文原版）

**Description**

You are given an array points where points[i] = [xi, yi] represents the coordinates of a point on an infinite plane.
Your task is to find the maximum area of a rectangle that:
Return the maximum area that you can obtain or -1 if no such rectangle is possible.

**Examples**

**Example 1:**

```
Input: points = [[1,1],[1,3],[3,1],[3,3]]
Output: 4
Explanation:

We can make a rectangle with these 4 points as corners and there is no other point that lies inside or on the border . Hence, the maximum possible area would be 4.
```

**Example 2:**

```
Input: points = [[1,1],[1,3],[3,1],[3,3],[2,2]]
Output: -1
Explanation:

There is only one rectangle possible is with points [1,1], [1,3], [3,1] and [3,3] but [2,2] will always lie inside it. Hence, returning -1.
```

**Example 3:**

```
Input: points = [[1,1],[1,3],[3,1],[3,3],[1,2],[3,2]]
Output: 2
Explanation:

The maximum area rectangle is formed by the points [1,3], [1,2], [3,2], [3,3] , which has an area of 2. Additionally, the points [1,1], [1,2], [3,1], [3,2] also form a valid rectangle with the same area.
```

**Constraints**

- 1 <= points.length <= 10
- points[i].length == 2
- 0 <= xi, yi <= 100
- All the given points are unique.

---

## 题目（中文翻译）

你得到一个数组 `points`，其中 `points[i] = [xi, yi]` 表示无限平面上一个点的坐标。请你找到满足以下条件的矩形的最大面积：

- 矩形的四个顶点必须全部取自 `points`；
- 矩形的内部以及边界上**不能**再出现其他给定的点。

返回能够得到的最大面积，如果不存在满足条件的矩形则返回 `-1`。

---

### 示例

**示例 1**  
**输入**: `points = [[1,1],[1,3],[3,1],[3,3]]`  
**输出**: `4`  
**解释**:  

我们可以使用这四个点作为矩形的四个角，且没有其他点落在矩形内部或边界上。因此，能够得到的最大面积为 `4`。

---

**示例 2**  
**输入**: `points = [[1,1],[1,3],[3,1],[3,3],[2,2]]`  
**输出**: `-1`  
**解释**:  

唯一可能的矩形是由点 `[1,1]、[1,3]、[3,1]、[3,3]` 构成，但点 `[2,2]` 必然位于该矩形内部。由于不存在符合要求的矩形，返回 `-1`。

---

**示例 3**  
**输入**: `points = [[1,1],[1,3],[3,1],[3,3],[1,2],[3,2]]`  
**输出**: `2`  
**解释**:  

最大面积矩形可以由点 `[1,3]、[1,2]、[3,2]、[3,3]` 形成，面积为 `2`。另外，点 `[1,1]、[1,2]、[3,1]、[3,2]` 也能构成面积相同的合法矩形。

---

### 约束条件

- `1 <= points.length <= 10`
- `points[i].length == 2`
- `0 <= xi, yi <= 100`
- 所有给出的点均互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有点两两配对，看看它们能否成为矩形的**对角线**。  
- 已知两个对角点 \((x_1,y_1)\) 与 \((x_2,y_2)\)（且 \(x_1\neq x_2,\;y_1\neq y_2\)），矩形的另外两个顶点只能是 \((x_1,y_2)\) 与 \((x_2,y_1)\)。  
- 为了快速判断这两个点是否真的在输入里，我们可以把所有点放进一个 **哈希集合**（就像把所有单词放进词典，查找某个单词是否存在只需要看它的“页码”是否在字典里）。  

找到了四个角之后，还必须确认 **没有其他点落在矩形的内部或边上**。这一步只能把所有点再遍历一遍，逐个判断它们的坐标是否满足  

\[
x_{\min} \le x \le x_{\max}\ \text{且}\ y_{\min} \le y \le y_{\max}
\]

如果除了四个角之外还有点满足上式，就说明这不是合法矩形。

把所有可能的对角线都枚举完，记录下合法矩形的最大面积即可。

> **为什么能得到正确答案**  
> - 任意合法矩形的两条对角线必然出现在点集中，枚举所有点对一定会遍历到它。  
> - 只要四个角全在集合里且内部没有额外点，这个矩形就满足题目要求。  

#### 代码（Python）

```python
from typing import List, Tuple

def maxAreaRectangle(points: List[List[int]]) -> int:
    # 把点装进集合，查询 O(1)
    point_set = { (x, y) for x, y in points }

    max_area = -1
    n = len(points)

    # 枚举所有点对，作为对角线的两端
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # 对角线必须是“斜的”，即 x、y 都不相等
            if x1 == x2 or y1 == y2:
                continue

            # 另外两条边的端点必须也在点集中
            if (x1, y2) not in point_set or (x2, y1) not in point_set:
                continue

            # 计算矩形左下、右上坐标，方便后面检查点是否在内部
            xl, xr = sorted((x1, x2))
            yb, yt = sorted((y1, y2))

            # 检查是否有其他点落在矩形内部或边上
            valid = True
            for px, py in points:
                # 跳过四个角本身
                if (px, py) in {(x1, y1), (x2, y2), (x1, y2), (x2, y1)}:
                    continue
                if xl <= px <= xr and yb <= py <= yt:
                    valid = False
                    break

            if valid:
                area = (xr - xl) * (yt - yb)
                max_area = max(max_area, area)

    return max_area
```

#### 复杂度

- **时间复杂度**：\(O(n^3)\)。  
  - 两层循环枚举点对是 \(O(n^2)\)。  
  - 对每个候选矩形要再遍历全部点检查内部是否有多余点，导致再乘一个 \(n\)。  
  - 用大白话说，如果点有 10 个，最坏要检查 10 × 10 × 10 = 1000 次操作，仍然在可以接受的范围。

- **空间复杂度**：\(O(n)\)。  
  - 只用了一个集合存放所有点，大小随输入点数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有点来判断内部是否有多余点**。  
我们可以把“检查矩形内部是否有点”这一步提前做成 **常数时间查询**，这样整体就降到 \(O(n^2)\)。

思路分两步：

1. **建立二维前缀和（2‑D Prefix Sum）**  
   - 题目坐标范围只有 \(0\sim100\)，可以把平面划成一个 101 × 101 的网格。  
   - `grid[x][y] = 1` 表示坐标 \((x,y)\) 上有点，否者为 0。  
   - 前缀和 `ps[i+1][j+1]` 表示左上角 \((0,0)\) 到 \((i,j)\)（含）之间点的数量。  
   - 有了前缀和，**任意矩形**内部（包括边界）的点数可以用四个加减操作在 **O(1)** 时间算出来。  
   - 前缀和的构造本身是 \(O(X\*Y)\)，这里的 \(X,Y\le 101\)，可以视作常数。

2. **枚举对角线并利用前缀和快速验证**  
   - 同样枚举所有点对 \((x_1,y_1),(x_2,y_2)\) 作为对角线（仍是 \(O(n^2)\)）。  
   - 先检查另外两角是否在集合里（哈希表 O(1)）。  
   - 通过前缀和求出矩形内部点的总数 `cnt`。  
   - 合法矩形必须恰好有 **4** 个点（就是四个角），于是只要 `cnt == 4` 就可以接受。  

这样，每个候选矩形的检查只用了常数时间，整体复杂度从 \(O(n^3)\) 降到了 \(O(n^2)\)。

> **核心数据结构解释**  
> - **哈希集合**：类似字典，存放所有点，查找某个坐标是否出现只要看它的“页码”是否在字典里，时间是常数。  
> - **二维前缀和**：想象在格子里累加点的数量，`ps[i][j]` 就是左上角子矩形的点总数。要得到任意矩形 \([x1,x2]\times[y1,y2]\) 的点数，只需要四次加减（类似求区间和的技巧），所以查询是 O(1)。

#### 代码（Python）

```python
from typing import List, Tuple

def maxAreaRectangle(points: List[List[int]]) -> int:
    # ---------- 1. 建立哈希集合 ----------
    point_set = {(x, y) for x, y in points}

    # ---------- 2. 建立 0~100 的网格 ----------
    MAXC = 101                     # 坐标上限 + 1
    grid = [[0] * MAXC for _ in range(MAXC)]
    for x, y in points:
        grid[x][y] = 1

    # ---------- 3. 计算二维前缀和 ----------
    # ps[i+1][j+1] = grid[0..i][0..j] 里的点数
    ps = [[0] * (MAXC + 1) for _ in range(MAXC + 1)]
    for i in range(MAXC):
        row_sum = 0
        for j in range(MAXC):
            row_sum += grid[i][j]          # 当前行的累计
            ps[i + 1][j + 1] = ps[i][j + 1] + row_sum

    # ---------- 4. 辅助函数：返回闭区间矩形内点的数量 ----------
    def rect_cnt(x1: int, y1: int, x2: int, y2: int) -> int:
        # 确保左下、右上顺序
        xl, xr = sorted((x1, x2))
        yb, yt = sorted((y1, y2))
        # 前缀和公式
        return (ps[xr + 1][yt + 1] - ps[xl][yt + 1]
                - ps[xr + 1][yb] + ps[xl][yb])

    max_area = -1
    n = len(points)

    # ---------- 5. 枚举所有对角线 ----------
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # 对角线必须是斜的
            if x1 == x2 or y1 == y2:
                continue

            # 另外两个角必须存在
            if (x1, y2) not in point_set or (x2, y1) not in point_set:
                continue

            # 使用前缀和检查内部点数
            if rect_cnt(x1, y1, x2, y2) != 4:   # 多于四个点或少于四个点
                continue

            area = abs(x2 - x1) * abs(y2 - y1)
            max_area = max(max_area, area)

    return max_area
```

#### 复杂度

- **时间复杂度**：\(O(n^2 + C^2)\)，其中 \(n\) 为点的个数，\(C=101\) 为坐标上限。  
  - 前缀和的构造是 \(O(C^2)\)（≈10⁴），可以视为常数。  
  - 主循环枚举所有点对是 \(O(n^2)\)。  
  - 与暴力解的 \(O(n^3)\) 相比，省掉了每次遍历所有点的那一层，提升显著。  

- **空间复杂度**：\(O(C^2)\) 用于存放网格和前缀和（约 10 KB），再加上哈希集合的 \(O(n)\)。整体仍然非常小。

---

## 心得

- **核心技巧**：把“矩形内部点数查询”转化为 **二维前缀和**，实现 **常数时间** 判定。  
- **适用的题型**：  
  1. “给定点集合，求满足某种几何约束的最大/最小面积/周长” 类题目。  
  2. “平面上有若干障碍点，求不包含障碍的最大子矩形” 这类网格 DP / 前缀和题。  
  3. “统计满足某种范围条件的点的数量”——常用前缀和或 BIT/线段树实现快速查询。  
- **一句话总结**：**把范围计数预处理为 O(1) 查询，是几何离散化题目的通用钥匙。**

---

## 反思

- **第一反应**：直接枚举对角线，然后逐点检查是否有点落在矩形内部。  
- **最容易踩的坑**：  
  - 忘记排除四个角本身导致误判内部有点。  
  - 对坐标顺序没有统一处理（左下 vs 右上），导致前缀和查询范围错误。  
  - 当矩形的宽或高为 0（两点在同一直线上）时，应该直接舍弃。  
- **下次类似题的第一步**：**先思考能否把“范围内点的计数”预处理成常数时间查询**（前缀和、树状数组或线段树），再在此基础上做枚举或动态规划。这样往往能把指数级/三次方的暴力降到二次方或更低。