# #3242. Design Neighbor Sum Service / Design Neighbor Sum Service

> 难度：简单 · 标签：Array、Hash Table、Design、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/design-neighbor-sum-service/)

---

## 题目（英文原版）

**Description**

You are given a n x n 2D array grid containing distinct elements in the range [0, n2 - 1].
Implement the NeighborSum class:

**Examples**

**Example 1:**

```
Input:
["NeighborSum", "adjacentSum", "adjacentSum", "diagonalSum", "diagonalSum"]
[[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]], [1], [4], [4], [8]]
Output: [null, 6, 16, 16, 4]
Explanation:
```

**Example 2:**

```
Input:
["NeighborSum", "adjacentSum", "diagonalSum"]
[[[[1, 2, 0, 3], [4, 7, 15, 6], [8, 9, 10, 11], [12, 13, 14, 5]]], [15], [9]]
Output: [null, 23, 45]
Explanation:
```

**Constraints**

- 3 <= n == grid.length == grid[0].length <= 10
- 0 <= grid[i][j] <= n2 - 1
- All grid[i][j] are distinct.
- value in adjacentSum and diagonalSum will be in the range [0, n2 - 1].
- At most 2 * n2 calls will be made to adjacentSum and diagonalSum.

---

## 题目（中文翻译）

你得到一个 `n x n` 的二维数组 `grid`，其中的元素互不相同，且均在区间 `[0, n^2 - 1]` 内。  
请实现 `NeighborSum` 类，提供以下接口：

- `NeighborSum(int[][] grid)`：构造函数，接收上述数组并进行必要的预处理。  
- `int adjacentSum(int value)`：返回 `grid` 中数值为 `value` 的单元格 **上下左右四个方向**（即相邻单元格）的元素之和。如果该方向不存在相邻单元格，则不计入求和。  
- `int diagonalSum(int value)`：返回 `grid` 中数值为 `value` 的单元格 **四个对角方向**（左上、右上、左下、右下）的元素之和。同样地，如果某个方向没有对应的单元格，则不计入求和。

> **说明**  
> - 所有查询的 `value` 必定出现在 `grid` 中。  
> - 题目保证 `adjacentSum` 与 `diagonalSum` 的调用次数总计不超过 `2 * n^2`，因此可以在构造时预先记录每个数值的位置，以实现 `O(1)` 的查询时间。

### 示例

#### 示例 1
```text
Input:
["NeighborSum", "adjacentSum", "adjacentSum", "diagonalSum", "diagonalSum"]
[[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]], [1], [4], [4], [8]]
Output: [null, 6, 16, 16, 4]
Explanation:
- 调用 `new NeighborSum(grid)` 初始化对象，`grid` 如下：
  0 1 2
  3 4 5
  6 7 8
- `adjacentSum(1)` 的相邻单元格为 0、2、4，和为 0+2+4 = **6**。  
- `adjacentSum(4)` 的相邻单元格为 1、3、5、7，和为 1+3+5+7 = **16**。  
- `diagonalSum(4)` 的对角单元格为 0、2、6、8，和为 0+2+6+8 = **16**。  
- `diagonalSum(8)` 的对角单元格为 4，和为 **4**。
```

#### 示例 2
```text
Input:
["NeighborSum", "adjacentSum", "diagonalSum"]
[[[[1, 2, 0, 3], [4, 7, 15, 6], [8, 9, 10, 11], [12, 13, 14, 5]]], [15], [9]]
Output: [null, 23, 45]
Explanation:
- 初始化的 `grid` 为：
  1  2  0  3
  4  7 15  6
  8  9 10 11
 12 13 14  5
- `adjacentSum(15)` 的相邻单元格为 7、6、10，和为 7+6+10 = **23**。  
- `diagonalSum(9)` 的对角单元格为 1、3、13、11，和为 1+3+13+11 = **45**。
```

### 约束条件
- `3 <= n == grid.length == grid[0].length <= 10`
- `0 <= grid[i][j] <= n^2 - 1`
- `grid[i][j]` 均互不相同
- `adjacentSum` 与 `diagonalSum` 的参数 `value` 均在区间 `[0, n^2 - 1]` 内且必定存在于 `grid` 中
- 最多会调用 `adjacentSum` 与 `diagonalSum` 共计 `2 * n^2` 次

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一个 **n×n** 的矩阵 `grid`（`3 ≤ n ≤ 10`），要求实现一个类 `NeighborSum`，它有两类查询：

* `adjacentSum(val)` – 求值 `val` 在矩阵中 **上下左右** 四个相邻格子的和。  
* `diagonalSum(val)` – 求值 `val` 在矩阵中 **左上、右上、左下、右下** 四个对角格子的和。

最直接的做法就是**每次查询时**遍历整个矩阵，找到 `val` 所在的坐标 `(i, j)`，然后根据坐标检查四个方向（或四个对角）的格子是否在矩阵内部，若在就把它们的值累加。

> **类比**：把矩阵想成一张城市地图，`val` 就是我们要找的某栋楼的编号。暴力做法相当于把整座城市的每一栋楼都走一遍，直到找到目标楼，再去查看它的相邻街区。

这种方法 **一定能得到正确答案**，因为我们把所有可能的格子都检查了一遍。

#### 代码（Python）

```python
class NeighborSum:
    def __init__(self, grid):
        """
        :param grid: List[List[int]]   n×n 矩阵，元素互不相同
        """
        self.grid = grid
        self.n = len(grid)

    def _find(self, val):
        """遍历整个矩阵，返回 val 所在的坐标 (i, j)"""
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == val:
                    return i, j
        # 题目保证一定能找到，这里只为代码完整
        raise ValueError("value not found")

    def adjacentSum(self, val):
        i, j = self._find(val)          # 找到目标格子
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # 上下左右四个方向
        s = 0
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.n:   # 越界就不算
                s += self.grid[ni][nj]
        return s

    def diagonalSum(self, val):
        i, j = self._find(val)          # 找到目标格子
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]   # 四个对角方向
        s = 0
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.n:
                s += self.grid[ni][nj]
        return s
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  每次查询都要遍历整个 `n×n` 矩阵（`n ≤ 10`），找一次坐标相当于看 `n²` 格子。大白话：如果矩阵是 10×10，最多要看 100 次，算得很快，但如果矩阵扩大到 1000×1000，工作量就会变成 1 000 000 次，明显不够高效。

- **空间复杂度**：`O(1)`（不计输入矩阵本身）  
  只用了常数级别的额外变量 `i, j, s` 等。

---

### 2. 最优解

#### 思路  

**慢在哪里？**  
暴力解的瓶颈是每次查询都要 **线性扫描** 整个矩阵来定位 `val`，这一步耗时 `O(n²)`。事实上，矩阵的大小固定且 **每个数只出现一次**，我们完全可以在构造函数里把 “数 → 坐标” 的映射提前算好，后面查询时直接取出坐标，时间就降到 `O(1)`。

**一步步推导**  

1. **预处理**：遍历一次矩阵，把每个元素 `grid[i][j]` 与它的坐标 `(i, j)` 存入哈希表（Python 中的 `dict`）。  
   - 哈希表就像一本**字典**，键是单词（这里是数值），值是页码（这里是坐标）。查找时直接“翻到对应页”，时间常数。

2. **查询**：  
   - 通过哈希表 `pos[val]` 直接得到 `(i, j)`。  
   - 然后检查四个方向（或四个对角），同样要做边界判断。因为只检查最多 4 个格子，时间是常数。

**核心数据结构**：**哈希表**（字典）  
- **插入**：遍历一次矩阵，`O(n²)`，一次性完成。  
- **查找**：`O(1)`，因为哈希表的查询时间在均摊意义下是常数。

**类比**：把矩阵看成一座图书馆，所有书都有唯一的编号。暴力解是每次找书都从书架的第一个位置往后翻；最优解则是事先把每本书的编号和所在书架位置记在一本**索引卡**里，需要哪本书直接翻到对应的卡片，就能立刻知道位置。

#### 代码（Python）

```python
class NeighborSum:
    def __init__(self, grid):
        """
        构造函数一次遍历矩阵，建立 “值 → (i, j)” 的映射。
        """
        self.grid = grid
        self.n = len(grid)
        self.pos = {}                         # 哈希表：value -> (i, j)
        for i in range(self.n):
            for j in range(self.n):
                self.pos[grid[i][j]] = (i, j)  # 记录坐标

    def _adjacent(self, i, j):
        """返回 (i, j) 四个正交邻居的坐标列表（已剔除越界）"""
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.n:
                res.append((ni, nj))
        return res

    def _diagonal(self, i, j):
        """返回 (i, j) 四个对角邻居的坐标列表（已剔除越界）"""
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        res = []
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.n:
                res.append((ni, nj))
        return res

    def adjacentSum(self, val):
        """O(1) 时间获取相邻格子之和"""
        i, j = self.pos[val]               # 直接拿到坐标
        s = 0
        for ni, nj in self._adjacent(i, j):
            s += self.grid[ni][nj]
        return s

    def diagonalSum(self, val):
        """O(1) 时间获取对角格子之和"""
        i, j = self.pos[val]
        s = 0
        for ni, nj in self._diagonal(i, j):
            s += self.grid[ni][nj]
        return s
```

#### 复杂度  

- **时间复杂度**  
  - 构造函数：`O(n²)`（只做一次遍历）  
  - 每次查询：`O(1)`，因为只要一次哈希查找 + 最多 4 次常数操作。  
  与暴力解相比，查询速度提升了 **从 `O(n²)` 到 `O(1)`**，在大量查询时优势明显。

- **空间复杂度**：`O(n²)`  
  需要额外存储一个大小为 `n²` 的字典来记录每个数的坐标。因为 `n ≤ 10`，最多也只有 100 条记录，完全可以接受。

---

## 心得

- **核心技巧**：**预处理 + 哈希表**（把“从值到坐标”的映射一次性算好），把查询从线性搜索降到常数时间。  
- **适用场景**：  
  1. **一次构造、 多次查询** 的矩阵/数组问题（如 “矩阵查询” 系列）。  
  2. **值唯一且需要快速定位** 的场景（如 “随机抽取数字的下标”）。  
  3. 需要 **O(1) 查找** 的游戏地图或棋盘类题目。  
- **一句话总结**：先把“在哪里”记下来，后面只管“算什么”，查询立刻变快。

---

## 反思

- **第一反应**：直接遍历矩阵找坐标，写出最直接的实现。  
- **最容易踩的坑**：  
  - 边界检查忘记，导致访问 `grid[-1][j]` 或 `grid[n][j]` 报错。  
  - 误把对角方向写成正交方向，或相反。  
  - 忘记在构造函数里初始化哈希表，导致查询时 `KeyError`。  
- **下次类似题**的第一步：**先思考是否可以一次预处理得到“值 → 位置信息”**，如果可以，就立刻建立哈希表；否则再考虑逐次遍历。