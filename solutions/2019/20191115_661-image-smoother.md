# #661. 图像平滑器 / Image Smoother

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/image-smoother/)

---

## 题目（英文原版）

**Description**

An image smoother is a filter of the size 3 x 3 that can be applied to each cell of an image by rounding down the average of the cell and the eight surrounding cells (i.e., the average of the nine cells in the blue smoother). If one or more of the surrounding cells of a cell is not present, we do not consider it in the average (i.e., the average of the four cells in the red smoother).
Given an m x n integer matrix img representing the grayscale of an image, return the image after applying the smoother on each cell of it.

**Examples**

**Example 1:**

```
Input: img = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[0,0,0],[0,0,0],[0,0,0]]
Explanation:
For the points (0,0), (0,2), (2,0), (2,2): floor(3/4) = floor(0.75) = 0
For the points (0,1), (1,0), (1,2), (2,1): floor(5/6) = floor(0.83333333) = 0
For the point (1,1): floor(8/9) = floor(0.88888889) = 0
```

**Example 2:**

```
Input: img = [[100,200,100],[200,50,200],[100,200,100]]
Output: [[137,141,137],[141,138,141],[137,141,137]]
Explanation:
For the points (0,0), (0,2), (2,0), (2,2): floor((100+200+200+50)/4) = floor(137.5) = 137
For the points (0,1), (1,0), (1,2), (2,1): floor((200+200+50+200+100+100)/6) = floor(141.666667) = 141
For the point (1,1): floor((50+200+200+200+200+100+100+100+100)/9) = floor(138.888889) = 138
```

**Constraints**

- m == img.length
- n == img[i].length
- 1 <= m, n <= 200
- 0 <= img[i][j] <= 255

---

## 题目（中文翻译）

描述  
图像平滑器（Image Smoother）是一种 3×3 大小的滤波器，可以对图像的每个像素（cell）进行处理，取该像素及其八个相邻像素的平均值并向下取整（floor），得到平滑后的值（即蓝色平滑器所示的九个像素的平均值）。如果某个像素的相邻像素不存在，则在计算平均值时不计入这些缺失的像素（即红色平滑器所示的四个像素的平均值）。

给定一个 m×n 的整数矩阵 img，表示一幅灰度图像（grayscale），返回对矩阵中每个像素都应用图像平滑器后的新矩阵。

约束条件  
- m == img.length  
- n == img[i].length  
- 1 ≤ m, n ≤ 200  
- 0 ≤ img[i][j] ≤ 255  

示例  
示例 1  
Input: img = [[1,1,1],[1,0,1],[1,1,1]]  
Output: [[0,0,0],[0,0,0],[0,0,0]]  
Explanation:  
对于坐标 (0,0)、(0,2)、(2,0)、(2,2)： floor(3/4) = floor(0.75) = 0  
对于坐标 (0,1)、(1,0)、(1,2)、(2,1)： floor(5/6) = floor(0.83333333) = 0  
对于坐标 (1,1)： floor(8/9) = floor(0.88888889) = 0  

示例 2  
Input: img = [[100,200,100],[200,50,200],[100,200,100]]  
Output: [[137,141,137],[141,138,141],[137,141,137]]  
Explanation:  
对于坐标 (0,0)、(0,2)、(2,0)、(2,2)： floor((100+200+200+50)/4) = floor(137.5) = 137  
对于坐标 (0,1)、(1,0)、(1,2)、(2,1)： floor((200+200+50+200+100+100)/6) = floor(141.666667) = 141  
对于坐标 (1,1)： floor((50+200+200+200+200+100+100+100+100)/9) = floor(138.888889) = 138

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**把每个格子当作中心，遍历它的 8 个相邻格子（以及它自己），把所有出现的格子值加起来，除以出现的格子数量再向下取整**，得到该格子平滑后的值。

- **遍历顺序**：先用两层 `for` 循环遍历矩阵的每个位置 `(i, j)`，再用另外两层 `for` 循环（`dx, dy ∈ {-1,0,1}`）检查它的九宫格。
- **数据结构**：只需要原始矩阵 `img`（相当于一本字典，坐标是“键”，像素值是“页码”），以及一个同尺寸的结果矩阵 `res` 来存放平滑后的值。
- **正确性**：对每个格子我们都完整地统计了它能看到的所有相邻格子（边界格子会少一些），并且按照题目要求用了**向下取整**（`//`），所以得到的结果必然符合题意。

#### 代码（Python）

```python
from typing import List

def imageSmoother_brute(img: List[List[int]]) -> List[List[int]]:
    m, n = len(img), len(img[0])          # 行数、列数
    res = [[0] * n for _ in range(m)]     # 用来保存答案的矩阵

    for i in range(m):
        for j in range(n):
            total = 0      # 累加格子值
            cnt = 0        # 计数出现了多少个格子
            # 检查以 (i, j) 为中心的 3×3 区域
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    x, y = i + dx, j + dy
                    # 边界检查：坐标必须在矩阵内部
                    if 0 <= x < m and 0 <= y < n:
                        total += img[x][y]
                        cnt += 1
            # 向下取整得到平滑后的值
            res[i][j] = total // cnt
    return res
```

#### 复杂度  

- **时间复杂度**：`O(m * n * 9) ≈ O(mn)`  
  对每个格子我们最多检查 9 次（常数），所以整体仍然是矩阵大小的线性时间。可以把 `O(mn)` 想象成“遍历整个图片一次”。  
- **空间复杂度**：`O(m * n)`  
  需要额外的结果矩阵 `res`，大小和原图相同。  

---

### 2. 最优解

#### 思路  

虽然暴力解已经是 `O(mn)`，但它在每次计算九宫格时都要**重复求和**，这在大矩阵（`200 × 200`）下仍会有不少重复工作。我们可以用**前缀和（二维累计和）**把每个子矩阵的和在 `O(1)` 时间内算出来，从而把整体时间降到真正的线性 `O(mn)`，而且只需要一次遍历即可完成。

**前缀和的类比**：  
把矩阵想象成一本“数字书”。前缀和表 `psum` 就像在每一页的左上角写下了“从书的第一页左上角到当前页左上角的所有数字之和”。有了这个信息，要算任意矩形区域的和，只需要四次查表并做加减——就像知道了两块面积后，用加减法得到交叉部分的面积。

**构建前缀和**  

`psum[i+1][j+1]` 表示矩阵左上角 `(0,0)` 到 `(i,j)`（含）的所有元素之和。递推公式：

```
psum[i+1][j+1] = img[i][j] + psum[i][j+1] + psum[i+1][j] - psum[i][j]
```

这里的 `- psum[i][j]` 是为了抵消左上角那块被加了两次的部分。

**利用前缀和求九宫格和**  

对每个格子 `(i,j)`，它的九宫格在原矩阵中的左上角坐标是 `(i-1, j-1)`，右下角坐标是 `(i+1, j+1)`（超出边界的部分直接截断）。设 `r1, c1, r2, c2` 为截断后的四个坐标，则子矩阵和为：

```
sub_sum = psum[r2+1][c2+1] - psum[r1][c2+1] - psum[r2+1][c1] + psum[r1][c1]
```

子矩阵的格子数 `cnt` 直接用 `(r2 - r1 + 1) * (c2 - c1 + 1)` 计算。

这样每个格子只需要 **常数次** 查表和加减，就能得到平滑后的值。

#### 代码（Python）

```python
from typing import List

def imageSmoother_opt(img: List[List[int]]) -> List[List[int]]:
    m, n = len(img), len(img[0])

    # 1️⃣ 建立前缀和矩阵，尺寸为 (m+1) × (n+1) 方便边界处理
    psum = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row_sum = 0                 # 当前行的累计和
        for j in range(n):
            row_sum += img[i][j]    # 累加到当前列
            psum[i + 1][j + 1] = psum[i][j + 1] + row_sum
            # 解释：上面一行的累计和 + 本行到当前位置的累计和

    # 2️⃣ 用前缀和求每个格子的平滑值
    res = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            # 九宫格的左上、右下坐标（注意不要越界）
            r1 = max(0, i - 1)
            c1 = max(0, j - 1)
            r2 = min(m - 1, i + 1)
            c2 = min(n - 1, j + 1)

            # 前缀和求子矩阵和（四次查表 + 三次加减）
            total = (psum[r2 + 1][c2 + 1]
                     - psum[r1][c2 + 1]
                     - psum[r2 + 1][c1]
                     + psum[r1][c1])

            cnt = (r2 - r1 + 1) * (c2 - c1 + 1)   # 实际出现的格子数
            res[i][j] = total // cnt             # 向下取整
    return res
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 构建前缀和遍历一次矩阵 `O(mn)`。  
  - 再次遍历每个格子，利用前缀和常数次查表得到子矩阵和，仍是 `O(mn)`。  
  与暴力解相比，**把每个格子内部的 9 次循环压缩成了 1 次常数操作**，在大数据时更省时。

- **空间复杂度**：`O(m * n)`  
  需要额外的前缀和矩阵 `psum`（比原图大一行一列）以及结果矩阵 `res`。两者都是线性空间。

---

## 心得

- **核心技巧**：二维前缀和（累计和），可以在 `O(1)` 时间内求任意子矩形的元素和。  
- **适用题型**：  
  1. 区域求和类（如 LeetCode 304、矩阵求和）  
  2. 需要快速统计局部窗口（如滑动窗口最大值的二维变形）  
  3. 统计子矩阵满足某种条件的计数问题  
- **一句话总结**：**“把所有前缀和预先算好，后面每次只用四次加减就能得到任意矩形的和”。**

---

## 反思

- **第一反应**：直接把每个格子周围的 8 个邻居遍历一遍，写出双层循环套双层循环的暴力实现。  
- **最容易踩的坑**：  
  - 边界格子没有完整的 3×3 区域，需要**动态裁剪**左上、右下坐标。  
  - 前缀和数组要多开一行一列（`m+1, n+1`），否则在求左上角子矩阵时会出现负索引。  
  - 取整方式必须是向下取整，Python 中 `//` 正好满足要求（注意负数除法的取整规则，但本题数值非负）。  
- **下次遇到同类题**：第一步先想“有没有办法把局部求和的重复工作一次性算好”，这通常指向**前缀和**或**差分数组**等预处理技巧。