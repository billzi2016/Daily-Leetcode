# #85. 最大矩形 / Maximal Rectangle

> 难度：困难 · 标签：Array、Dynamic Programming、Stack、Matrix、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/maximal-rectangle/)

---

## 题目（英文原版）

**Description**

Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

**Examples**

**Example 1:**

```
Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 6
Explanation: The maximal rectangle is shown in the above picture.
```

**Example 2:**

```
Input: matrix = [["0"]]
Output: 0
```

**Example 3:**

```
Input: matrix = [["1"]]
Output: 1
```

**Constraints**

- rows == matrix.length
- cols == matrix[i].length
- 1 <= row, cols <= 200
- matrix[i][j] is '0' or '1'.

---

## 题目（中文翻译）

给定一个 `rows x cols` 的二进制矩阵（binary matrix），矩阵仅由字符 `'0'` 和 `'1'` 组成，求只包含 `'1'` 的最大矩形的面积并返回该面积。

## 示例

### 示例 1
**输入**  
```json
matrix = [["1","0","1","0","0"],
          ["1","0","1","1","1"],
          ["1","1","1","1","1"],
          ["1","0","0","1","0"]]
```
**输出**  
```
6
```
**解释**  
最大矩形如上图所示。

### 示例 2
**输入**  
```json
matrix = [["0"]]
```
**输出**  
```
0
```

### 示例 3
**输入**  
```json
matrix = [["1"]]
```
**输出**  
```
1
```

## 约束条件

- `rows == matrix.length`
- `cols == matrix[i].length`
- `1 <= rows, cols <= 200`
- `matrix[i][j]` 为字符 `'0'` 或 `'1'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把矩阵里每一个可能的左上角 `(r1, c1)` 以及每一个可能的右下角 `(r2, c2)` 都枚举一遍，然后检查这个子矩形里是否全是 `'1'`。如果全是 `'1'`，就计算它的面积 ` (r2‑r1+1) * (c2‑c1+1)`，取最大值即可。

- **用到的数据结构**：只需要二维列表（matrix）本身。把每个子矩形看成一本书的章节，左上角是章节的起始页，右下角是结束页；我们要逐页检查章节内容是否全是“好”，如果是，就记下章节长度（面积）。
- **为什么正确**：因为我们把所有可能的矩形都遍历了一遍，必然不会漏掉最大那一个。只要判断条件（全为 `'1'`）成立，就一定是合法矩形。

#### 代码（Python）

```python
def maximalRectangle_bruteforce(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    max_area = 0

    # 枚举左上角
    for r1 in range(rows):
        for c1 in range(cols):
            # 只从 '1' 开始尝试，因为左上角若是 '0' 必不可能是全 1 的矩形
            if matrix[r1][c1] == '0':
                continue
            # 枚举右下角
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    # 检查子矩形是否全是 '1'
                    all_one = True
                    for i in range(r1, r2 + 1):
                        for j in range(c1, c2 + 1):
                            if matrix[i][j] == '0':
                                all_one = False
                                break
                        if not all_one:
                            break
                    if all_one:
                        area = (r2 - r1 + 1) * (c2 - c1 + 1)
                        max_area = max(max_area, area)
    return max_area
```

#### 复杂度  

- **时间复杂度**：`O(rows² * cols²)`  
  解释：我们有四层循环分别遍历行列的起点和终点，最坏情况下每一次都要检查子矩形内部的每个格子，所以整体是二次方的二次方，类似“把矩阵的每一块都翻遍”。  
- **空间复杂度**：`O(1)`（不使用额外的随矩阵大小增长的存储空间，只用了几个计数变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复检查**：同一行/列的元素会被多次遍历。我们需要把“检查子矩形是否全为 1”这一步做得更快。

观察矩阵的每一行，**把它当成直方图的底部**，即可把二维问题转化为求**最大矩形面积的直方图**问题：

1. 对每一列 `j` 维护一个 `height[j]`，表示从当前行往上连续的 `'1'` 的数量（就像柱子的高度）。  
   - 当 `matrix[i][j] == '1'` 时，`height[j] += 1`。  
   - 当 `matrix[i][j] == '0'` 时，`height[j] = 0`（因为柱子被截断了）。  
   这一步相当于“把每一行看成地面，往上堆砖”。  

2. 对每一行得到的 `height` 数组，求 **该直方图的最大矩形面积**。  
   - 这一步可以用 **单调栈**（monotonic stack）在 `O(cols)` 时间完成。  
   - 栈中保存的是柱子下标，且对应的高度是 **递增** 的。每当出现一个比栈顶更低的柱子时，就说明栈顶柱子右边的最大宽度已经确定，可以弹出计算面积。

把两步结合起来：遍历所有行 → 更新 `height` → 用单调栈求最大矩形 → 记录全局最大即可。

> **单调栈的类比**：想象你在排队买咖啡，身高从低到高站成一列（单调递增）。当有个更矮的人进来时，所有比他高的前面的人都必须离开队伍（弹出），因为他们的“右边界”已经被这个更矮的人挡住了。弹出时可以算出每个人可以“占据的宽度”。

#### 代码（Python）

```python
def maximalRectangle(matrix):
    """
    通过把每一行当作直方图底部，使用单调栈在 O(rows * cols) 时间求解。
    """
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    # heights[j] 表示第 j 列连续 1 的高度
    heights = [0] * (cols + 1)          # 多加一个哨兵 0，方便统一弹栈逻辑
    max_area = 0

    for i in range(rows):
        for j in range(cols):
            # 更新高度：如果是 1，累加；如果是 0，重新计数为 0
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0

        # 单调递增栈，保存柱子的下标
        stack = []
        for j in range(cols + 1):       # 多遍历一次哨兵位
            # 当前柱子比栈顶柱子低时，弹出栈顶计算面积
            while stack and heights[j] < heights[stack[-1]]:
                h = heights[stack.pop()]          # 被弹出的柱子高度
                # 左边界是栈顶元素（弹出后新的栈顶），如果栈空说明左边界是 -1
                left = stack[-1] if stack else -1
                width = j - left - 1               # 宽度 = 当前下标 - 左边界 - 1
                max_area = max(max_area, h * width)
            stack.append(j)           # 当前柱子入栈，保持递增

    return max_area
```

#### 复杂度  

- **时间复杂度**：`O(rows * cols)`  
  解释：外层遍历每一行 `rows` 次，内部两步（更新 `heights` 与单调栈求最大矩形）都是线性遍历 `cols`，所以总工作量相当于“把矩阵每个格子看一次”。比暴力的 `O(n⁴)` 快了好几个数量级。  
- **空间复杂度**：`O(cols)`  
  解释：我们额外用了 `heights` 数组和单调栈，大小与列数成正比。相比于矩阵本身的存储，这是一块“可忽略不计”的额外空间。

---

## 心得

- **核心技巧**：把二维最大矩形问题转化为**直方图最大矩形**，再使用**单调栈**在一次遍历里完成求解。  
- **适用的题型**：  
  1. `Largest Rectangle in Histogram`（单调栈的直接版）。  
  2. `Maximal Square`（同样可以把每行的连续 1 长度看成高度，只是计算方式略有不同）。  
  3. `Number of Submatrices With All Ones`（需要在每行上做前缀和或栈的变形）。  
- **一句话总结**：**把二维问题压平为一维直方图，用单调栈一次遍历找最大面积**。

---

## 反思

- **第一反应**：看到“矩阵、全为 1 的矩形”，自然想到暴力枚举所有子矩形。  
- **最容易踩的坑**：  
  - 忘记在 `heights` 末尾加一个哨兵 `0`，导致最后的递增柱子无法弹出，遗漏最大面积。  
  - 计算宽度时的边界处理：弹出后左边界是栈顶元素（如果栈空则是 `-1`），宽度公式必须是 `j - left - 1`，容易写成 `j - left` 出错。  
  - 输入是字符 `'0'`/`'1'`，不要把它们当成整数比较，否则会出错。  
- **下次第一步**：先把每一行的连续 1 高度累加成 `heights`，再想到“这不就是直方图最大矩形吗？”立即联想到单调栈求解。这样可以把搜索空间从四次方直接压到线性。