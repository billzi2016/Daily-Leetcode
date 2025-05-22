# #3195. 覆盖所有 1 的最小矩形面积 I / Find the Minimum Area to Cover All Ones I

> 难度：中等 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-i/)

---

## 题目（英文原版）

**Description**

You are given a 2D binary array grid. Find a rectangle with horizontal and vertical sides with the smallest area, such that all the 1's in grid lie inside this rectangle.
Return the minimum possible area of the rectangle.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,0],[1,0,1]]
Output: 6
Explanation:

The smallest rectangle has a height of 2 and a width of 3, so it has an area of 2 * 3 = 6 .
```

**Example 2:**

```
Input: grid = [[1,0],[0,0]]
Output: 1
Explanation:

The smallest rectangle has both height and width 1, so its area is 1 * 1 = 1 .
```

**Constraints**

- 1 <= grid.length, grid[i].length <= 1000
- grid[i][j] is either 0 or 1.
- The input is generated such that there is at least one 1 in grid.

---

## 题目（中文翻译）

给定一个二维二进制数组（2D binary array）`grid`。请找到一个水平和垂直边的矩形（rectangle），使得 `grid` 中所有的 `1` 都位于该矩形内部，并且该矩形的面积最小。返回可能的最小面积。

## 示例

### 示例 1
**输入:** `grid = [[0,1,0],[1,0,1]]`  
**输出:** `6`  
**解释:**  
最小的矩形高度为 `2`，宽度为 `3`，因此面积为 `2 * 3 = 6`。

### 示例 2
**输入:** `grid = [[1,0],[0,0]]`  
**输出:** `1`  
**解释:**  
最小的矩形高度和宽度均为 `1`，所以面积为 `1 * 1 = 1`。

## 约束条件
- `1 <= grid.length, grid[i].length <= 1000`
- `grid[i][j]` 只能是 `0` 或 `1`
- 输入保证至少存在一个 `1` 在 `grid` 中

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的矩形**，然后检查每个矩形里是否把所有 `1` 都包含进去，最后挑出面积最小的那一个。  
- **矩形的表示**：用左上角 `(top, left)` 与右下角 `(bottom, right)` 四个坐标来描述。  
- **判断矩形是否合法**：遍历矩形内部的每个格子，若发现有 `1` 落在矩形外部，就说明这个矩形不符合要求。  
- **为什么能得到正确答案**：因为我们把所有合法矩形都穷举了一遍，最小的那个必然会被找到。  

> 类比：想象你在一张地图上找一块最小的纸，要求纸能把所有标记的点（`1`）都覆盖住。暴力法相当于把所有可能的纸的尺寸和位置都尝试一遍，再挑最小的那块。

#### 代码（Python）  

```python
def minArea_bruteforce(grid):
    m, n = len(grid), len(grid[0])

    # 先统计所有 1 的坐标，方便后面检查
    ones = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]

    # 初始化答案为一个很大的数
    best = m * n

    # 枚举左上角 (top, left)
    for top in range(m):
        for left in range(n):
            # 枚举右下角 (bottom, right)
            for bottom in range(top, m):
                for right in range(left, n):
                    # 判断当前矩形是否包含所有的 1
                    ok = True
                    for x, y in ones:
                        if not (top <= x <= bottom and left <= y <= right):
                            ok = False
                            break
                    if ok:
                        area = (bottom - top + 1) * (right - left + 1)
                        best = min(best, area)   # 记录最小面积
    return best
```

> 关键点说明  
> - 第 4 行把所有 `1` 的坐标提前保存，后面判断矩形是否合法时只需要遍历这些坐标，避免每次都遍历整张矩阵。  
> - 四层循环分别枚举矩形的上下、左右边界，穷尽所有可能。  
> - `top <= x <= bottom and left <= y <= right` 用来判断一个 `1` 是否在当前矩形内部。  

#### 复杂度  

- **时间复杂度**：`O(m² * n² * k)`，其中 `k` 是 `1` 的个数。  
  - 四层循环分别遍历 `m`、`n`、`m`、`n`，最坏情况下会产生 `m²·n²` 种矩形。  
  - 对每个矩形我们都要检查所有 `1`（数量记为 `k`），所以整体是 `m²·n²·k`。  
  - 用大白话说，这相当于“把每一块可能的纸都搬到每一个 `1` 前面检查”，当矩阵稍大时几乎不可能跑完。  

- **空间复杂度**：`O(k)`，用于存放所有 `1` 的坐标。除了这点额外空间，算法本身只用常数级变量。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于枚举所有矩形**。实际上我们并不需要枚举，只要找到所有 `1` 所在的**最外层边界**即可：  

- 最左边出现 `1` 的列号 → `min_col`  
- 最右边出现 `1` 的列号 → `max_col`  
- 最上边出现 `1` 的行号 → ``min_row``  
- 最下边出现 `1` 的行号 → `max_row`  

这四个边界决定了唯一的最小矩形。只要一次遍历矩阵，实时更新这四个极值，就能得到答案。  

> 类比：把所有的 `1` 想象成散布在平面上的小石子。要用最小的纸把它们全部包住，只要把纸的左、右、上、下边缘分别贴到最左、最右、最上、最下的石子上即可。  

**为什么正确**：  
- 任意合法矩形的左边界一定不小于 `min_col`，右边界不大于 `max_col`，同理行方向也是如此。  
- 因此把四条边都紧贴到极限位置得到的矩形，面积最小且必定包含所有 `1`。  

#### 代码（Python）  

```python
def minArea(grid):
    """
    返回覆盖所有 1 的最小矩形面积
    """
    rows, cols = len(grid), len(grid[0])

    # 初始化四个边界为“无穷大/无穷小”，方便后面取极值
    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    # 一次遍历整个矩阵
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:               # 只关心值为 1 的格子
                # 更新四个边界
                if i < min_row:
                    min_row = i                # 更靠上的行
                if i > max_row:
                    max_row = i                # 更靠下的行
                if j < min_col:
                    min_col = j                # 更靠左的列
                if j > max_col:
                    max_col = j                # 更靠右的列

    # 计算宽度和高度（+1 因为坐标是从 0 开始的，边界本身也算在内）
    height = max_row - min_row + 1
    width  = max_col - min_col + 1
    return height * width
```

> 关键行解释  
> - 第 7‑8 行把四个极值初始化为 “不可能的值”，这样第一次遇到 `1` 时一定会被更新。  
> - 第 12‑19 行是**唯一的遍历**，每发现一个 `1` 就立即比较并更新对应的最小/最大行/列。  
> - 第 23‑24 行把行、列的跨度转化为矩形的高度和宽度，记得要加 1，因为坐标本身也占用一个格子。  

#### 复杂度  

- **时间复杂度**：`O(m * n)`。我们只遍历了一遍矩阵，每个格子检查一次。用大白话说，就是“把所有格子都走一遍”，即使是 1000×1000 的矩阵也只需要 100 万次操作，完全可以接受。  

- **空间复杂度**：`O(1)`。只用了四个整数来记录边界，和矩阵大小无关，属于常数级别的额外空间。  

---

## 心得  

- **核心技巧**：**一次遍历求极值**（最小/最大行列），把“找边界”这件事抽象为维护四个变量。  
- **适用的题型**  
  1. “最小矩形覆盖所有特定元素”类（如本题、LeetCode 295 `Find Median of Two Sorted Arrays` 的边界思路）。  
  2. “在二维平面上找最小/最大范围”类（如 “最大岛屿面积” 的边界剪枝）。  
  3. “统计矩形内部元素”类（如 “二维前缀和” 的范围查询，先求边界再利用前缀和快速求和）。  
- **一句话总结**：只要能把所有目标点的**上下左右四个极限**找出来，最小覆盖矩形就呼之欲出。  

---

## 反思  

- **第一反应**：看到“矩形”“最小面积”，本能想到枚举所有矩形（暴力）——这在面试里常常是最安全的起点。  
- **最容易踩的坑**  
  1. **忘记加 1**：计算宽度/高度时，`max - min` 只得到跨度，需要再加上格子本身的宽度。  
  2. **边界初始化错误**：如果把 `min_row` 初始化为 `0`，而矩阵第一行全是 `0`，会导致错误的最小行。正确做法是用 “不可能的极值” 如 `rows`、`-1`。  
  3. **没有考虑只有一个 `1` 的情况**：此时 `min_row == max_row`、`min_col == max_col`，仍然要返回 `1` 而不是 `0`。  
- **下次类似题的第一步**：先思考“是否只需要极值信息”，如果答案是肯定的，就直接写一次遍历的代码；否则再考虑更复杂的枚举或动态规划。