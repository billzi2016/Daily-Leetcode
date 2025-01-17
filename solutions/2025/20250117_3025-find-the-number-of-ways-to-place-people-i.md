# #3025. 寻找放置人物的方案数 I / Find the Number of Ways to Place People I

> 难度：中等 · 标签：Array、Math、Geometry、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-ways-to-place-people-i/)

---

## 题目（英文原版）

**Description**

You are given a 2D array points of size n x 2 representing integer coordinates of some points on a 2D plane, where points[i] = [xi, yi].
Count the number of pairs of points (A, B), where
Return the count.

**Examples**

**Example 1:**

```
Input: points = [[1,1],[2,2],[3,3]]
Output: 0
Explanation:

There is no way to choose A and B so A is on the upper left side of B .
```

**Example 2:**

```
Input: points = [[6,2],[4,4],[2,6]]
Output: 2
Explanation:
```

**Example 3:**

```
Input: points = [[3,1],[1,3],[1,1]]
Output: 2
Explanation:
```

**Constraints**

- 2 <= n <= 50
- points[i].length == 2
- 0 <= points[i][0], points[i][1] <= 50
- All points[i] are distinct.

---

## 题目（中文翻译）

给定一个大小为 `n × 2` 的二维数组 `points`，其中 `points[i] = [xi, yi]` 表示平面上第 `i` 个点的整数坐标。  
统计满足以下条件的点对 `(A, B)` 的数量：

- `A` 位于 `B` 的左上方，即 `A.x < B.x` 且 `A.y > B.y`。

返回该计数。

**示例 1**

```text
Input: points = [[1,1],[2,2],[3,3]]
Output: 0
Explanation:
不存在任意一对点满足 A 在 B 的左上方。
```

**示例 2**

```text
Input: points = [[6,2],[4,4],[2,6]]
Output: 2
Explanation:
满足条件的点对有 ( [4,4] , [6,2] ) 与 ( [2,6] , [4,4] )，共 2 对。
```

**示例 3**

```text
Input: points = [[3,1],[1,3],[1,1]]
Output: 2
Explanation:
满足条件的点对有 ( [1,3] , [3,1] ) 与 ( [1,3] , [1,1] )，共 2 对。
```

**约束条件**

- `2 ≤ n ≤ 50`
- `points[i].length == 2`
- `0 ≤ points[i][0], points[i][1] ≤ 50`
- 所有 `points[i]` 均互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **枚举所有点对**，检查它们是否满足题目要求。  
- **点对的方向**：点 `A = (x1, y1)` 必须在点 `B = (x2, y2)` 的左上方，也就是 `x1 < x2` 且 `y1 > y2`。可以把它想象成在地图上，`A` 在 `B` 的左边且更靠上。  
- **矩形内部没有其它点**：把 `A` 当作左上角、`B` 当作右下角画一个矩形，要求矩形内部（包括边界）只能出现这两个点，不能有第三个点。这里的“矩形内部”指的是所有满足 `x1 ≤ x ≤ x2` 且 `y2 ≤ y ≤ y1` 的整数坐标点。  

验证这两个条件后，如果都满足，就把这对点计入答案。  
因为 `n ≤ 50`，直接三层循环也能跑完（`O(n³)`），但我们先写最朴素的 **两层循环 + 线性遍历所有其余点** 的版本，时间复杂度是 `O(n³)`。

> **类比**：把每个点想成一本书的书签。我们要找两本书的书签，使得左边的书签在右边书签的左上方，并且这两个书签之间的所有页面（矩形区域）里没有其他书签。

#### 代码（Python）

```python
from typing import List

def countPairs_bruteforce(points: List[List[int]]) -> int:
    n = len(points)
    ans = 0

    # 把每个点拆成 (x, y) 方便使用
    pts = [(p[0], p[1]) for p in points]

    # 枚举所有有序点对 (i, j)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(n):
            if i == j:
                continue
            x2, y2 = pts[j]

            # 方向条件：A 必须在 B 的左上方
            if not (x1 < x2 and y1 > y2):
                continue

            # 检查矩形内部是否还有其它点
            valid = True
            for k in range(n):
                if k == i or k == j:
                    continue
                x, y = pts[k]
                # 判断点 k 是否落在以 (x1,y1) 为左上、(x2,y2) 为右下的矩形里
                if x1 <= x <= x2 and y2 <= y <= y1:
                    valid = False      # 发现第 3 个点，直接否定
                    break

            if valid:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举点对是 `O(n²)`，内部再遍历所有其余点检查是否在矩形里是 `O(n)`，于是总体是 `n²·n = n³`。  
  - 对于 `n = 50`，`50³ = 125,000` 次基本运算，完全可以接受，只是不是最优的思路。

- **空间复杂度**：`O(1)`（不计输入数组）  
  - 只用了常数级别的额外变量 `ans、valid、x1、y1…`，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次检查矩形内部时都要遍历所有点，导致 `O(n³)`。  
我们可以把“矩形里有多少点”这类**二维计数**问题预处理成 **前缀和**（又叫二维累计和），这样一次查询就能在 `O(1)` 时间得到矩形内点的数量。

**关键点 1：坐标范围有限**  
- 题目给出 `0 ≤ xi, yi ≤ 50`，坐标只在 `0~50` 的小格子里。我们可以建立一个大小为 `51 × 51` 的网格 `grid[x][y]`，如果某个坐标有点就标记为 `1`，否则为 `0`。

**关键点 2：二维前缀和**  
- 前缀和 `pref[i][j]` 表示左上角 `(0,0)` 到 `(i-1, j-1)`（左闭右开的矩形）里点的总数。  
- 构造公式：  
  ```python
  pref[i+1][j+1] = pref[i][j+1] + pref[i+1][j] - pref[i][j] + grid[i][j]
  ```
- 有了前缀和，任意矩形 `(x1, y1)`（左上）到 `(x2, y2)`（右下）的点数可以用 **四次减法** 快速得到：
  ```python
  cnt = pref[x2+1][y2+1] - pref[x1][y2+1] - pref[x2+1][y1] + pref[x1][y1]
  ```

**关键点 3：枚举点对 + O(1) 检查**  
- 仍然枚举所有有序点对 `(A, B)`，先检查方向 `xA < xB` 且 `yA > yB`（这一步是 `O(1)`）。  
- 接着用前缀和查询矩形 `[xA, xB] × [yB, yA]` 内的点数 `cnt`。如果 `cnt == 2`，说明矩形里只有 A、B 两个点，符合要求。  

这样时间复杂度降到 **`O(n² + C²)`**，其中 `C = 51` 是坐标上限，`C²` 用于构建前缀和。对于本题，`n² = 2500`，远小于暴力的 `125,000`。

> **类比**：把坐标平面想成一张表格，前缀和就像在表格左上角放了一个“统计机器人”。每次想知道某块区域里有多少点，只要让机器人报告四个角的累计数量，马上就能算出答案，省掉遍历所有点的麻烦。

#### 代码（Python）

```python
from typing import List

def countPairs_optimal(points: List[List[int]]) -> int:
    MAXC = 51                     # 坐标上限 + 1
    # 1. 把点映射到网格
    grid = [[0] * MAXC for _ in range(MAXC)]
    for x, y in points:
        grid[x][y] = 1            # 有点的格子记为 1

    # 2. 构造二维前缀和
    pref = [[0] * (MAXC + 1) for _ in range(MAXC + 1)]
    for i in range(MAXC):
        for j in range(MAXC):
            pref[i + 1][j + 1] = (
                pref[i][j + 1] + pref[i + 1][j] - pref[i][j] + grid[i][j]
            )

    # 3. 枚举点对并用前缀和快速判断
    ans = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(n):
            if i == j:
                continue
            x2, y2 = points[j]

            # 必须是左上 / 右下 关系
            if not (x1 < x2 and y1 > y2):
                continue

            # 统计矩形 [x1, x2] × [y2, y1] 内的点数
            cnt = (
                pref[x2 + 1][y1 + 1]
                - pref[x1][y1 + 1]
                - pref[x2 + 1][y2]
                + pref[x1][y2]
            )
            # 只要矩形里恰好有 A、B 两点，就合法
            if cnt == 2:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² + C²)`  
  - 构建网格 `O(C²)`（`C = 51`），构造前缀和同样 `O(C²)`。  
  - 主循环枚举所有有序点对 `O(n²)`，每对只做常数次前缀和查询。  
  - 对比暴力的 `O(n³)`，这里把内部的线性遍历去掉了，速度提升明显。

- **空间复杂度**：`O(C²)`  
  - 需要保存 `grid`（`51×51`）和 `pref`（`52×52`）两个二维数组，大小固定，不随 `n` 增长。

---

## 心得

- **核心技巧**：**二维前缀和**（2‑D prefix sum）把“矩形内点的数量”查询从线性降到常数。  
- **适用场景**：  
  1. 判断任意子矩形是否满足某种计数条件（如 “是否全为 0”）。  
  2. 统计二维网格中某区域的和或数量（如 LeetCode 2408 “设计一个数组求和查询系统” 的二维版本）。  
  3. “子矩形无其他点” 类似的几何约束题（如 “Number of Corner Rectangles”）。  
- **一句话总结**：**把点离散到固定大小的网格，利用前缀和一次查询即得矩形内部点数**。

---

## 反思

- **第一反应**：看到“上左 / 下右”以及“矩形内部没有其它点”，自然想到枚举点对后遍历其余点检查——这就是暴力解。  
- **最容易踩的坑**：  
  - **坐标边界**：前缀和的索引要小心左闭右开与闭区间的对应关系，容易越界。  
  - **点的顺序**：必须确保 `x1 < x2` 且 `y1 > y2`，否则矩形定义会倒置导致查询错误。  
  - **计数准确性**：矩形内部点数应恰好等于 `2`（只含 A、B），不能等于 `1`（遗漏自己）或更大。  
- **下次思路**：遇到“矩形/子区间里点/数的多少”这类问题，第一步就想到 **离散化 + 前缀和**，把线性检查转化为常数查询。这样既能保证正确性，又能快速得到最优解。