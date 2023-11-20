# #2482. 行列中 1 与 0 的差值 / Difference Between Ones and Zeros in Row and Column

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/difference-between-ones-and-zeros-in-row-and-column/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n binary matrix grid.
A 0-indexed m x n difference matrix diff is created with the following procedure:
Return the difference matrix diff.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,1],[1,0,1],[0,0,1]]
Output: [[0,0,4],[0,0,4],[-2,-2,2]]
Explanation:
- diff[0][0] = onesRow0 + onesCol0 - zerosRow0 - zerosCol0 = 2 + 1 - 1 - 2 = 0 
- diff[0][1] = onesRow0 + onesCol1 - zerosRow0 - zerosCol1 = 2 + 1 - 1 - 2 = 0 
- diff[0][2] = onesRow0 + onesCol2 - zerosRow0 - zerosCol2 = 2 + 3 - 1 - 0 = 4 
- diff[1][0] = onesRow1 + onesCol0 - zerosRow1 - zerosCol0 = 2 + 1 - 1 - 2 = 0 
- diff[1][1] = onesRow1 + onesCol1 - zerosRow1 - zerosCol1 = 2 + 1 - 1 - 2 = 0 
- diff[1][2] = onesRow1 + onesCol2 - zerosRow1 - zerosCol2 = 2 + 3 - 1 - 0 = 4 
- diff[2][0] = onesRow2 + onesCol0 - zerosRow2 - zerosCol0 = 1 + 1 - 2 - 2 = -2
- diff[2][1] = onesRow2 + onesCol1 - zerosRow2 - zerosCol1 = 1 + 1 - 2 - 2 = -2
- diff[2][2] = onesRow2 + onesCol2 - zerosRow2 - zerosCol2 = 1 + 3 - 2 - 0 = 2
```

**Example 2:**

```
Input: grid = [[1,1,1],[1,1,1]]
Output: [[5,5,5],[5,5,5]]
Explanation:
- diff[0][0] = onesRow0 + onesCol0 - zerosRow0 - zerosCol0 = 3 + 2 - 0 - 0 = 5
- diff[0][1] = onesRow0 + onesCol1 - zerosRow0 - zerosCol1 = 3 + 2 - 0 - 0 = 5
- diff[0][2] = onesRow0 + onesCol2 - zerosRow0 - zerosCol2 = 3 + 2 - 0 - 0 = 5
- diff[1][0] = onesRow1 + onesCol0 - zerosRow1 - zerosCol0 = 3 + 2 - 0 - 0 = 5
- diff[1][1] = onesRow1 + onesCol1 - zerosRow1 - zerosCol1 = 3 + 2 - 0 - 0 = 5
- diff[1][2] = onesRow1 + onesCol2 - zerosRow1 - zerosCol2 = 3 + 2 - 0 - 0 = 5
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个下标从 0 开始的 **m × n** 二进制矩阵（binary matrix）`grid`。  
构造一个下标从 0 开始的 **m × n** 差值矩阵（difference matrix）`diff`，其计算方式如下：

- 对于每个单元格 `(i, j)`，  
  `diff[i][j] = onesRow_i + onesCol_j - zerosRow_i - zerosCol_j`  

  其中  
  * `onesRow_i` 为第 `i` 行中 `1` 的个数，`zerosRow_i` 为第 `i` 行中 `0` 的个数；  
  * `onesCol_j` 为第 `j` 列中 `1` 的个数，`zerosCol_j` 为第 `j` 列中 `0` 的个数。  

返回构造得到的差值矩阵 `diff`。

## 示例

### 示例 1
**输入**
```json
grid = [[0,1,1],[1,0,1],[0,0,1]]
```
**输出**
```json
[[0,0,4],[0,0,4],[-2,-2,2]]
```
**解释**
- `diff[0][0] = onesRow0 + onesCol0 - zerosRow0 - zerosCol0 = 2 + 1 - 1 - 2 = 0`  
- `diff[0][1] = onesRow0 + onesCol1 - zerosRow0 - zerosCol1 = 2 + 1 - 1 - 2 = 0`  
- `diff[0][2] = onesRow0 + onesCol2 - zerosRow0 - zerosCol2 = 2 + 3 - 1 - 0 = 4`  
- `diff[1][0] = onesRow1 + onesCol0 - zerosRow1 - zerosCol0 = 2 + 1 - 1 - 2 = 0`  
- `...`（后续已截断）

### 示例 2
**输入**
```json
grid = [[1,1,1],[1,1,1]]
```
**输出**
```json
[[5,5,5],[5,5,5]]
```
**解释**
- `diff[0][0] = onesRow0 + onesCol0 - zerosRow0 - zerosCol0 = 3 + 2 - 0 - 0 = 5`  
- `diff[0][1] = onesRow0 + onesCol1 - zerosRow0 - zerosCol1 = 3 + 2 - 0 - 0 = 5`  
- `diff[0][2] = onesRow0 + onesCol2 - zerosRow0 - zerosCol2 = 3 + 2 - 0 - 0 = 5`  
- `diff[1][0] = onesRow1 + onesCol0 - zerosRow1 - zerosCol0 = 3 + 2 - 0 - 0 = 5`  
- `...`（后续已截断）

## 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 10^5`
- `1 ≤ m × n ≤ 10^5`
- `grid[i][j]` 仅为 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求把每个位置 `(i, j)` 的 **行** 中 1 的个数、**列** 中 1 的个数、以及对应的 0 的个数全部算出来，然后套公式  

```
diff[i][j] = (onesRow[i] + onesCol[j]) - (zerosRow[i] + zerosCol[j])
```

最直接的想法是：  
- **遍历每一个格子** `(i, j)`。  
- 为了得到 `onesRow[i]`，我们 **从左到右扫一遍第 i 行**，把所有 1 加起来。  
- 为了得到 `onesCol[j]`，我们 **从上到下扫一遍第 j 列**，把所有 1 加起来。  
- `zerosRow[i] = n - onesRow[i]`（因为每行恰好有 `n` 个格子），`zerosCol[j] = m - onesCol[j]` 同理。  

> **类比**：把行看成一本书的章节，把列看成一本书的页码。要知道某章节有多少个“好评”（1），只能逐页翻阅；要知道某页码有多少个“好评”，只能逐章节查找。  

只要把每一行、每一列都遍历一次，就能得到对应的计数，从而算出 `diff[i][j]`。

#### 代码（Python）

```python
from typing import List

def diffMatrix_bruteforce(grid: List[List[int]]) -> List[List[int]]:
    m, n = len(grid), len(grid[0])
    diff = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            # 统计第 i 行的 1 的个数（暴力遍历整行）
            ones_row = 0
            for col in range(n):
                if grid[i][col] == 1:
                    ones_row += 1

            # 统计第 j 列的 1 的个数（暴力遍历整列）
            ones_col = 0
            for row in range(m):
                if grid[row][j] == 1:
                    ones_col += 1

            zeros_row = n - ones_row          # 行中 0 的个数
            zeros_col = m - ones_col          # 列中 0 的个数

            diff[i][j] = (ones_row + ones_col) - (zeros_row + zeros_col)
    return diff
```

> **关键行中文注释**  
> - `for col in range(n):` → “遍历第 i 行的每一列”。  
> - `for row in range(m):` → “遍历第 j 列的每一行”。  

#### 复杂度  

- **时间复杂度**：`O(m * n * (m + n))`  
  - 对每个格子 `(i, j)`（共 `m·n` 个）我们都要再遍历一遍整行 `O(n)` 和整列 `O(m)`，于是总共是 `m·n·(m+n)`。  
  - **大白话**：如果矩阵是 100×100，暴力解大约要做 100·100·(100+100)=2,000,000 次基本操作，远大于直接一次遍历的 10,000 次。

- **空间复杂度**：`O(m·n)` 用于存放结果矩阵 `diff`，额外的临时变量只占常数空间 `O(1)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：  
- 对每个格子都重复统计同一行或同一列的 1 的个数。  
- 实际上，同一行的 `onesRow[i]` 在该行的所有格子里是 **完全相同** 的；同一列的 `onesCol[j]` 也是如此。  

**优化思路**：把每一行、每一列的 1 的个数 **提前算好并保存下来**，后面再直接查表即可。  
这一步只需要 **一次** 遍历整个矩阵，时间 `O(m·n)`，空间 `O(m+n)`（分别存行计数和列计数）。  

有了 `onesRow[i]` 与 `onesCol[j]`，我们还能直接算出对应的 0 的个数：

```
zerosRow[i] = n - onesRow[i]      # 行长是 n
zerosCol[j] = m - onesCol[j]      # 列长是 m
```

把公式代入：

```
diff[i][j] = (onesRow[i] + onesCol[j]) - ( (n - onesRow[i]) + (m - onesCol[j]) )
           = 2 * onesRow[i] + 2 * onesCol[j] - n - m
```

**关键点**：

1. **一次遍历** 统计行、列的 1 的个数（相当于把“查字典”提前做好，行号/列号是 key，1 的个数是 value）。  
2. 再次遍历矩阵，用已知的 `onesRow`、`onesCol` 直接算出 `diff[i][j]`，不再需要再遍历行或列。  

> **类比**：把每行的“好评数”记在一本小册子里（行册），把每列的“好评数”记在另一册子里（列册），以后查某行或某列的好评数，只需要翻开对应页码，一眼就能看到。

#### 代码（Python）

```python
from typing import List

def diffMatrix_optimal(grid: List[List[int]]) -> List[List[int]]:
    """
    计算差值矩阵 diff，时间 O(m*n)，空间 O(m+n)
    """
    m, n = len(grid), len(grid[0])

    # 1️⃣ 统计每行、每列的 1 的个数
    ones_row = [0] * m          # 行计数数组，索引 i 对应第 i 行的 1 的数量
    ones_col = [0] * n          # 列计数数组，索引 j 对应第 j 列的 1 的数量

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:    # 遇到 1 就把对应行、列的计数加一
                ones_row[i] += 1
                ones_col[j] += 1

    # 2️⃣ 根据公式直接算 diff
    diff = [[0] * n for _ in range(m)]
    # 预先算好一个常数项，省去每次循环的重复计算
    const = -n - m                # - (行长度) - (列长度)

    for i in range(m):
        for j in range(n):
            # 2 * onesRow[i] + 2 * onesCol[j] + const
            diff[i][j] = 2 * ones_row[i] + 2 * ones_col[j] + const

    return diff
```

> **关键行中文注释**  
> - `ones_row = [0] * m` → “准备一个长度为 m 的数组，用来存每行的 1 的数量”。  
> - `if grid[i][j] == 1:` → “发现一个 1，就把它所在的行和列的计数都加一”。  
> - `const = -n - m` → “把公式里不变的 `-n - m` 提前算好，后面每次只需要加上去”。  

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 第一次遍历一次矩阵统计行列计数，第二次遍历一次矩阵填入结果，总共两遍 `m·n`，和矩阵大小成线性关系。  
  - 与暴力解相比，省掉了每格子额外的 `O(m+n)`，速度提升了数百倍。

- **空间复杂度**：`O(m + n)`（不计结果矩阵）  
  - 只用了两个一维数组分别保存行计数和列计数，长度分别是 `m`、`n`。  
  - **大白话**：如果矩阵有 1000 行 1000 列，我们只需要额外存 2000 个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**预处理**（把会被重复使用的信息提前算好并保存），相当于把“查字典”提前做好。  
- **适用场景**：  
  1. 需要多次查询同一行/列/子数组统计信息的矩阵题（如 “行列和” 之类）。  
  2. “前缀和” 或 “后缀和” 需要在 O(1) 时间内得到区间和的场景。  
  3. “统计每行/列出现次数” 这类需要 O(1) 查询的计数题。  

> **解题钥匙**：**一次遍历把所有重复计算的子结果保存下来，后面直接查表**。

---

## 反思

- **第一反应**：直接对每个格子去遍历整行整列，写出最直接的公式实现。  
- **最容易踩的坑**：  
  - 忘记 **0 的个数** 其实可以用行/列长度减去 1 的个数直接得到，避免二次遍历。  
  - 当 `m` 或 `n` 非常大时，暴力遍历会导致超时，需要及时想到“重复子问题的缓存”。  
  - 结果矩阵的大小本身已经是 `O(m·n)`，所以不能再额外使用 `O(m·n)` 的临时结构（如每格子再存一整行或整列的计数）。  

- **下次遇到同类题**：  
  1. 先 **列出需要的统计量**（行/列/子矩阵的和、个数等）。  
  2. 思考 **这些统计量在矩阵中会被多少次重复使用**。  
  3. 若使用次数 > 1，就 **预先一次遍历把它们保存**，后面直接查表。  

这样就能把看似 “二次方” 的暴力思路，轻松压缩到线性时间。祝你编码愉快！