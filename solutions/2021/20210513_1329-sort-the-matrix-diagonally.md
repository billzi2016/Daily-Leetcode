# #1329. 对角线排序矩阵 / Sort the Matrix Diagonally

> 难度：中等 · 标签：Array、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/sort-the-matrix-diagonally/)

---

## 题目（英文原版）

**Description**

A matrix diagonal is a diagonal line of cells starting from some cell in either the topmost row or leftmost column and going in the bottom-right direction until reaching the matrix's end. For example, the matrix diagonal starting from mat[2][0], where mat is a 6 x 3 matrix, includes cells mat[2][0], mat[3][1], and mat[4][2].
Given an m x n matrix mat of integers, sort each matrix diagonal in ascending order and return the resulting matrix.

**Examples**

**Example 1:**

```
Input: mat = [[3,3,1,1],[2,2,1,2],[1,1,1,2]]
Output: [[1,1,1,1],[1,2,2,2],[1,2,3,3]]
```

**Example 2:**

```
Input: mat = [[11,25,66,1,69,7],[23,55,17,45,15,52],[75,31,36,44,58,8],[22,27,33,25,68,4],[84,28,14,11,5,50]]
Output: [[5,17,4,1,52,7],[11,11,25,45,8,69],[14,23,25,44,58,15],[22,27,31,36,50,66],[84,28,75,33,55,68]]
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 100
- 1 <= mat[i][j] <= 100

---

## 题目（中文翻译）

矩阵对角线（matrix diagonal）是指从矩阵最上行（topmost row）或最左列（leftmost column）中的某个单元格出发，沿右下方向（bottom‑right direction）一直延伸至矩阵边界的所有单元格构成的一条斜线。例如，在一个 6 × 3 的矩阵 `mat` 中，以 `mat[2][0]` 为起点的矩阵对角线包括单元格 `mat[2][0]、mat[3][1]、mat[4][2]`。

给定一个 `m × n` 的整数矩阵 `mat`，请将每条矩阵对角线按升序（ascending order）排序后返回得到的矩阵。

**示例 1**  
输入: `mat = [[3,3,1,1],[2,2,1,2],[1,1,1,2]]`  
输出: `[[1,1,1,1],[1,2,2,2],[1,2,3,3]]`

**示例 2**  
输入: `mat = [[11,25,66,1,69,7],[23,55,17,45,15,52],[75,31,36,44,58,8],[22,27,33,25,68,4],[84,28,14,11,5,50]]`  
输出: `[[5,17,4,1,52,7],[11,11,25,45,8,69],[14,23,25,44,58,15],[22,27,31,36,50,66],[84,28,75,33,55,68]]`

**约束条件**
- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 100`
- `1 <= mat[i][j] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每条对角线的所有元素全部取出来，排好序后再放回原来的位置**。  
- **数据结构**：我们可以用「列表」来保存一条对角线上的数。把列表想象成「装东西的抽屉」，每条对角线对应一个抽屉，抽屉的编号用 `i - j`（行号减列号）来表示——因为在同一条对角线上，`i - j` 的值都是相等的。  
- **正确性**：把抽屉里的东西全部排序后，再按原来的顺序（左上→右下）放回去，就保证了每条对角线从左上到右下的数是递增的。其它对角线不受影响，因为它们的抽屉（`i - j`）不同。  
- **复杂度**：  
  - 对每条对角线我们都要遍历一次取数、一次排序、一次写回。  
  - 排序的时间是 `O(k log k)`（`k` 为该对角线长度），所有对角线的总长度等于矩阵的元素个数 `m·n`，所以最坏情况下的时间复杂度是 `O(m·n·log(min(m,n)))`。  
  - 需要额外的列表来保存每条对角线的元素，最多同时保存最短那条对角线的长度（不超过 `min(m,n)`），所以空间复杂度是 `O(min(m,n))`。  
  - 用大白话说，`O(m·n·log min(m,n))` 就是「先把所有格子看一遍（`m·n`），再对每条短的对角线做一次‘整理’（`log` 是整理的难度）」，整体会比直接一个个比较慢很多，但仍在可接受范围。

#### 代码（Python）

```python
from typing import List
import collections

def diagonalSort_brute(mat: List[List[int]]) -> List[List[int]]:
    m, n = len(mat), len(mat[0])
    # 用字典把每条对角线的元素收集起来，key = i - j
    diag = collections.defaultdict(list)

    # 1️⃣ 把所有元素放进对应的抽屉
    for i in range(m):
        for j in range(n):
            diag[i - j].append(mat[i][j])

    # 2️⃣ 对每个抽屉里的数进行升序排序
    for d in diag:
        diag[d].sort(reverse=True)   # 逆序存，后面 pop() 更快

    # 3️⃣ 再把排好序的数放回矩阵
    for i in range(m):
        for j in range(n):
            mat[i][j] = diag[i - j].pop()   # 从抽屉的尾部取出最小的

    return mat
```

> **关键行中文注释**  
> - `diag[i - j].append(mat[i][j])`：把坐标 `(i, j)` 的数放进编号为 `i-j` 的抽屉。  
> - `diag[d].sort(reverse=True)`：把抽屉里的数从大到小排好，后面 `pop()` 能直接拿到最小的。  
> - `mat[i][j] = diag[i - j].pop()`：把排好序的最小数写回原位置。

#### 复杂度

- **时间复杂度**：`O(m·n·log min(m,n))`  
  - `m·n` 是遍历所有格子的次数。  
  - 每条对角线最多 `min(m,n)` 个元素，排序的代价是 `log min(m,n)`，所以整体乘在一起。  
- **空间复杂度**：`O(min(m,n))`  
  - 只需要额外存放最短那条对角线的元素（最多 `min(m,n)` 个），其余空间都是常数。

---

### 2. 最优解

#### 思路  

从暴力解出发，慢的地方主要在 **“每条对角线都要单独排序”**，而排序本身已经是最优的 `O(k log k)`（`k` 为该对角线长度），没有进一步改进的余地。  
真正的“最优”在于 **实现方式更简洁、常数更小**，而且 **不需要把所有对角线都一次性收集进内存**。  

**关键观察**  
- 对角线的编号仍然是 `i - j`，这点不变。  
- 如果我们 **从左上角往右下角遍历**，每次取出当前对角线的所有元素，排序后直接写回，就不需要额外的 `pop()` 操作。  

**核心技巧**：**先收集、再排序、再写回**，但把「收集」和「写回」的循环分别写成两个独立的遍历，这样代码更易读，且只需要一次额外的列表（对应单条对角线），空间仍是 `O(min(m,n))`。  

**步骤**  
1. **遍历所有起点**  
   - 对角线只能从 **第一行** 或 **第一列** 的格子开始。  
   - 先遍历第一行的每个列 `j`（起点 `(0, j)`），再遍历第一列的每个行 `i`（起点 `(i, 0)`，`i>0` 防止重复）。  
2. **收集该对角线的元素**  
   - 从起点沿右下方向走 `(i+1, j+1)`，把值放进列表 `vals`。  
3. **排序**  
   - `vals.sort()` 把列表升序。  
4. **写回**  
   - 再次沿同样路径遍历，把排序好的值一个一个写回矩阵。  

这样每条对角线只遍历两遍（收集 + 写回），整体仍是 `O(m·n·log min(m,n))`，但实现更直观，且不需要 `pop()` 的额外开销。

#### 代码（Python）

```python
from typing import List

def diagonalSort(mat: List[List[int]]) -> List[List[int]]:
    m, n = len(mat), len(mat[0])

    # 1️⃣ 处理所有从第一行出发的对角线
    for start_col in range(n):
        i, j = 0, start_col          # 起点 (0, start_col)
        vals = []                    # 用来暂存该对角线的所有数

        # 收集
        while i < m and j < n:
            vals.append(mat[i][j])
            i += 1
            j += 1

        # 排序
        vals.sort()

        # 写回
        i, j = 0, start_col
        for v in vals:
            mat[i][j] = v
            i += 1
            j += 1

    # 2️⃣ 处理所有从第一列（除左上角）出发的对角线
    for start_row in range(1, m):    # 从第2行开始，防止重复左上角那条对角线
        i, j = start_row, 0          # 起点 (start_row, 0)
        vals = []

        # 收集
        while i < m and j < n:
            vals.append(mat[i][j])
            i += 1
            j += 1

        # 排序
        vals.sort()

        # 写回
        i, j = start_row, 0
        for v in vals:
            mat[i][j] = v
            i += 1
            j += 1

    return mat
```

> **关键行中文注释**  
> - `while i < m and j < n:`：沿右下方向遍历，直到超出矩阵边界。  
> - `vals.sort()`：对收集到的数做升序排列。  
> - `for v in vals: mat[i][j] = v`：把排好序的数一个一个写回原矩阵。

#### 复杂度

- **时间复杂度**：`O(m·n·log min(m,n))`  
  - 每条对角线收集一次、排序一次、写回一次。排序是主导耗时，`log min(m,n)` 仍是对角线长度的对数。  
  - 与暴力解的时间复杂度相同，但常数更小（不需要 `pop()`、不需要额外的哈希表查找）。  
- **空间复杂度**：`O(min(m,n))`  
  - 只在遍历一条对角线时临时保存它的元素，最大不超过最短的对角线长度。  

---

## 心得

- **核心技巧**：利用 `i - j`（行列差）把同一条对角线归类，或从矩阵左上边缘的起点逐条遍历。  
- **适用题型**：  
  1. “对角线遍历”类题目（如 LeetCode 498. Diagonal Traverse）  
  2. “按某种规则分组再排序”类题目（如 1329. Sort the Matrix Diagonally 的变体）  
  3. “矩阵中同一属性的元素统一处理”类（如 1672. Richest Customer Wealth 按行/列分组）  
- **一句话总结**：**把同一条对角线的格子看成“一起装箱”，先装好（收集），再把箱子里的东西排好序，最后把箱子搬回原位**。

---

## 反思

- **第一反应**：看到“对角线”就想到“把所有对角线的坐标收集起来”，于是自然想到使用哈希表 `i-j` 作为键。  
- **最容易踩的坑**：  
  - **起点重复**：左上角的对角线既可以从第一行的第 0 列，也可以从第一列的第 0 行开始，必须避免重复遍历。  
  - **边界判断**：遍历时要同时检查行、列是否越界 (`i < m and j < n`)；忘记其中一个会导致 IndexError。  
  - **排序后写回顺序**：如果把收集的列表倒序存放（如 `reverse=True`），写回时必须用 `pop()`；否则直接正序遍历写回即可。  
- **下次第一步**：先确定 **“同类元素的标识”**（这里是 `i - j`），再决定是 **“一次性收集全部再统一处理”**（哈希表）还是 **“逐条遍历、现场处理”**（起点遍历）。这一步能帮助快速定位最合适的实现方式。