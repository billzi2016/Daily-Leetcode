# #1252. 矩阵中奇数值的单元格 / Cells with Odd Values in a Matrix

> 难度：简单 · 标签：Array、Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/cells-with-odd-values-in-a-matrix/)

---

## 题目（英文原版）

**Description**

There is an m x n matrix that is initialized to all 0's. There is also a 2D array indices where each indices[i] = [ri, ci] represents a 0-indexed location to perform some increment operations on the matrix.
For each location indices[i], do both of the following:
Given m, n, and indices, return the number of odd-valued cells in the matrix after applying the increment to all locations in indices.
Follow up: Could you solve this in O(n + m + indices.length) time with only O(n + m) extra space?

**Examples**

**Example 1:**

```
Input: m = 2, n = 3, indices = [[0,1],[1,1]]
Output: 6
Explanation: Initial matrix = [[0,0,0],[0,0,0]].
After applying first increment it becomes [[1,2,1],[0,1,0]].
The final matrix is [[1,3,1],[1,3,1]], which contains 6 odd numbers.
```

**Example 2:**

```
Input: m = 2, n = 2, indices = [[1,1],[0,0]]
Output: 0
Explanation: Final matrix = [[2,2],[2,2]]. There are no odd numbers in the final matrix.
```

**Constraints**

- 1 <= m, n <= 50
- 1 <= indices.length <= 100
- 0 <= ri < m
- 0 <= ci < n

---

## 题目（中文翻译）

有一个 `m x n` 的矩阵，初始全部为 `0`。另有一个二维数组 `indices`，其中 `indices[i] = [ri, ci]` 表示一个 **0 索引** 的位置，需要对矩阵执行增量操作。

对于每个位置 `indices[i]`，执行以下两步：

1. 将第 `ri` 行（row）的所有单元格的值加 `1`。  
2. 将第 `ci` 列（column）的所有单元格的值加 `1`。

给定 `m`、`n` 和 `indices`，返回对所有 `indices` 中的位置完成增量操作后，矩阵中奇数值（odd-valued）单元格的数量。

**示例 1**  
**输入**: `m = 2, n = 3, indices = [[0,1],[1,1]]`  
**输出**: `6`  
**解释**: 初始矩阵为 `[[0,0,0],[0,0,0]]`。  
第一次增量后矩阵变为 `[[1,2,1],[0,1,0]]`。  
最终矩阵为 `[[1,3,1],[1,3,1]]`，其中包含 `6` 个奇数。

**示例 2**  
**输入**: `m = 2, n = 2, indices = [[1,1],[0,0]]`  
**输出**: `0`  
**解释**: 最终矩阵为 `[[2,2],[2,2]]`，没有奇数。

**约束条件**  

- `1 <= m, n <= 50`
- `1 <= indices.length <= 100`
- `0 <= ri < m`
- `0 <= ci < n`

**进阶**: 能否在 `O(n + m + indices.length)` 时间内，仅使用 `O(n + m)` 额外空间完成求解？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
题目给出一个 `m × n` 的全 0 矩阵，随后会有若干个坐标 `indices[i] = [ri, ci]`。  
每一次操作我们要：

1. 把第 `ri` 行的所有元素 **加 1**；
2. 把第 `ci` 列的所有元素 **加 1**。

最直接的想法就是 **真的把矩阵全部写出来**，每次操作都遍历对应的行和列，逐个加 1，最后再遍历一遍矩阵统计奇数个数。

> **类比**：把矩阵想象成一张电子表格（Excel），每次操作就像在某一行全部加 1、在某一列全部加 1。我们把表格的每个格子都记下来，按步骤修改它们的数值，最后数一数哪些格子是奇数。

**为什么正确**  
因为我们严格按照题目要求对每个格子做了相同次数的加法，所有的加法都是整数，最后的奇偶性自然就是题目要的答案。

**时间/空间复杂度**  
- 对每个坐标，我们要遍历一整行（`n` 个格子）和一整列（`m` 个格子），所以一次操作是 `O(m + n)`。  
- 有 `k = len(indices)` 次操作，总时间是 `O(k·(m+n))`。在最坏情况下 `k≈100，m,n≤50`，仍然可以接受。  
- 我们需要保存整个矩阵，大小为 `m·n`，所以空间是 `O(m·n)`。

> **大白话**：  
> - `O(k·(m+n))` 就像“每次都要把整条街（行）和整条巷（列）走一遍”，次数是 `k`。  
> - `O(m·n)` 就是“把整座城市的每幢楼都记下来”，占的空间随城市面积线性增长。

#### 代码（Python）

```python
def oddCells_bruteforce(m: int, n: int, indices: list[list[int]]) -> int:
    # 1️⃣ 创建 m 行 n 列的全 0 矩阵
    matrix = [[0] * n for _ in range(m)]

    # 2️⃣ 按照每个 (ri, ci) 进行加 1 操作
    for ri, ci in indices:
        # 把第 ri 行的所有元素 +1
        for col in range(n):
            matrix[ri][col] += 1          # 行里每个格子都加 1

        # 把第 ci 列的所有元素 +1
        for row in range(m):
            matrix[row][ci] += 1          # 列里每个格子都加 1

    # 3️⃣ 统计奇数格子的数量
    odd_cnt = 0
    for row in range(m):
        for col in range(n):
            if matrix[row][col] % 2 == 1:   # %2 为 1 表示奇数
                odd_cnt += 1
    return odd_cnt
```

#### 复杂度

- **时间复杂度**：`O(k·(m+n) + m·n)`  
  - 前半段是遍历所有操作并更新行/列，后半段是最终遍历矩阵统计奇数。  
  - 对于本题的约束，这已经足够快，但当 `m、n、k` 变大时会明显慢下来。

- **空间复杂度**：`O(m·n)`  
  - 需要存放整个矩阵，每个格子占用一个整数的空间。  

---

### 2. 最优解

#### 思路  
在暴力解里，我们每次都把整行、整列的所有格子都加 1，实际上 **只关心奇偶性**，而奇偶性只取决于每行被加的次数和每列被加的次数的**奇偶**。

**瓶颈**：  
- 暴力解的时间大部分花在遍历矩阵本身（`m·n`），但我们并不需要真的去修改每个格子，只要知道每行/每列被加了几次即可。

**关键观察**  
- 对于任意格子 `(r, c)`，它最终的数值 = `row_cnt[r] + col_cnt[c]`，其中  
  - `row_cnt[r]` = 第 `r` 行被加的次数（即有多少个 `[r, *]` 出现在 `indices` 中）  
  - `col_cnt[c]` = 第 `c` 列被加的次数（即有多少个 `[* , c]` 出现在 `indices` 中）  

- 只要 `row_cnt[r] + col_cnt[c]` 是奇数，格子就是奇数。  
- 因此我们只需要统计每行、每列的 **奇偶性**（是奇是偶），而不必记录具体的次数。

**如何实现**  
1. 用两个一维数组 `row`（长度 `m`）和 `col`（长度 `n`）分别记录每行、每列被加的次数。  
2. 遍历 `indices`，对对应的 `row[ri]`、`col[ci]` 各加 1。  
3. 统计 `row` 中奇数的行数 `odd_rows`，以及 `col` 中奇数的列数 `odd_cols`。  
4. 最终奇数格子的数量可以直接算出来：  
   - 奇数行 × 偶数列 会产生奇数（因为奇 + 偶 = 奇）  
   - 偶数行 × 奇数列 也会产生奇数（偶 + 奇 = 奇）  
   - 所以 `odd_cells = odd_rows * (n - odd_cols) + (m - odd_rows) * odd_cols`

**类比**：  
把每行看成一本书的章节，每列看成一本书的页码。我们只关心每章节被翻了几次（奇/偶）以及每页码被翻了几次（奇/偶），然后根据“奇+偶=奇”的规则直接算出哪些章节页码组合是奇数。

#### 代码（Python）

```python
def oddCells_optimal(m: int, n: int, indices: list[list[int]]) -> int:
    # 1️⃣ 用一维数组记录每行、每列被加的次数
    row = [0] * m          # row[i] 表示第 i 行被加的次数
    col = [0] * n          # col[j] 表示第 j 列被加的次数

    # 2️⃣ 遍历所有坐标，累加次数
    for ri, ci in indices:
        row[ri] += 1       # 该行被加一次
        col[ci] += 1       # 该列被加一次

    # 3️⃣ 统计奇数行和奇数列的数量
    odd_rows = sum(1 for x in row if x % 2 == 1)   # 行次数为奇数的行数
    odd_cols = sum(1 for x in col if x % 2 == 1)   # 列次数为奇数的列数

    # 4️⃣ 根据奇偶组合直接计算奇数格子个数
    # 奇行 + 偶列 -> 奇数，偶行 + 奇列 -> 奇数
    odd_cells = odd_rows * (n - odd_cols) + (m - odd_rows) * odd_cols
    return odd_cells
```

#### 复杂度

- **时间复杂度**：`O(m + n + k)`  
  - 只遍历一次 `indices`（长度 `k`），再各遍历一次 `row`、`col`（长度分别是 `m`、`n`）。  
  - 与暴力解的 `O(k·(m+n) + m·n)` 相比，线性增长，几乎瞬间完成。

- **空间复杂度**：`O(m + n)`  
  - 只需要两个一维数组来保存行、列的计数，省掉了整个矩阵的存储。  

> 与暴力解对比：时间从“每次遍历整行整列”降到“只遍历一次坐标”，空间从 `m·n` 降到 `m+n`，在数据量大时优势非常明显。

---

## 心得

- **核心技巧**：利用**行列计数 + 奇偶性**来把二维模拟转化为一维计数，避免显式构造矩阵。  
- **适用场景**：  
  1. “矩阵加法后统计奇数/偶数” 类题目（如 LeetCode 1252 – *Cells with Odd Values in a Matrix*）。  
  2. “每次操作影响整行或整列” 的计数问题（如 “Matrix Diagonal Sum” 的行列标记版）。  
  3. “二维网格的状态只和行/列属性有关” 的组合计数问题。  
- **一句话总结**：**把“每格的值”拆成“行的贡献 + 列的贡献”，只统计奇偶即可**。

---

## 反思

- **第一反应**：直接把矩阵写出来，按题目要求一步步加。  
- **最容易踩的坑**：  
  - 忘记同一次操作中，交叉的格子会被加 **两次**（一次来自行，一次来自列），导致计数错误。  
  - 统计奇数时误把 `% 2 == 0` 当作奇数判定。  
  - 边界条件：`m` 或 `n` 为 1 时，行列计数仍然适用，但要确保代码不出现除零或越界。  
- **下次思路**：遇到“对行/列整体操作”时，先问自己 **“每个格子最终值是哪些独立因素之和？”**，如果是行+列的形式，就立刻转向“一维计数+奇偶组合” 的优化思路。