# #2536. 子矩阵加一 / Increment Submatrices by One

> 难度：中等 · 标签：Array、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/increment-submatrices-by-one/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n, indicating that we initially have an n x n 0-indexed integer matrix mat filled with zeroes.
You are also given a 2D integer array query. For each query[i] = [row1i, col1i, row2i, col2i], you should do the following operation:
Return the matrix mat after performing every query.

**Examples**

**Example 1:**

```
Input: n = 3, queries = [[1,1,2,2],[0,0,1,1]]
Output: [[1,1,0],[1,2,1],[0,1,1]]
Explanation: The diagram above shows the initial matrix, the matrix after the first query, and the matrix after the second query.
- In the first query, we add 1 to every element in the submatrix with the top left corner (1, 1) and bottom right corner (2, 2).
- In the second query, we add 1 to every element in the submatrix with the top left corner (0, 0) and bottom right corner (1, 1).
```

**Example 2:**

```
Input: n = 2, queries = [[0,0,1,1]]
Output: [[1,1],[1,1]]
Explanation: The diagram above shows the initial matrix and the matrix after the first query.
- In the first query we add 1 to every element in the matrix.
```

**Constraints**

- 1 <= n <= 500
- 1 <= queries.length <= 104
- 0 <= row1i <= row2i < n
- 0 <= col1i <= col2i < n

---

## 题目（中文翻译）

给定一个正整数 `n`，表示我们最初有一个 `n × n`、下标从 `0` 开始、所有元素均为 `0` 的整数矩阵 `mat`。  

同时给定一个二维整数数组 `queries`。对于每个 `queries[i] = [row1_i, col1_i, row2_i, col2_i]`，需要执行以下操作：将左上角坐标为 `(row1_i, col1_i)`、右下角坐标为 `(row2_i, col2_i)` 的子矩阵（submatrix）中的每个元素加 `1`。  

在执行完所有查询后返回矩阵 `mat`。

**示例 1**  
```
Input: n = 3, queries = [[1,1,2,2],[0,0,1,1]]
Output: [[1,1,0],[1,2,1],[0,1,1]]
```
解释：上图分别展示了初始矩阵、第一次查询后的矩阵以及第二次查询后的矩阵。  
- 第一次查询中，我们将左上角为 `(1, 1)`、右下角为 `(2, 2)` 的子矩阵（submatrix）中的每个元素加 `1`。  
- 第二次查询中，我们将左上角为 `(0, 0)`、右下角为 `(1, 1)` 的子矩阵中的每个元素加 `1`。  

**示例 2**  
```
Input: n = 2, queries = [[0,0,1,1]]
Output: [[1,1],[1,1]]
```
解释：上图展示了初始矩阵以及第一次查询后的矩阵。  
- 第一次查询中，我们将矩阵中的所有元素加 `1`。  

**约束条件**  
- `1 <= n <= 500`  
- `1 <= queries.length <= 10^4`  
- `0 <= row1_i <= row2_i < n`  
- `0 <= col1_i <= col2_i < n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每一次查询的子矩阵都遍历一遍，把对应的格子加 1。  
可以把矩阵想象成一张 **Excel 表**，每次查询就像在表格里画一个矩形，然后把这个矩形里的每个格子都手动 +1。  

- **使用的数据结构**：普通的二维列表 `mat[n][n]`。  
- **正确性**：因为我们对每一次查询都把对应范围的每个元素都加了 1，所有查询结束后 `mat` 中的每个格子恰好等于它被覆盖的次数。  

#### 代码（Python）

```python
def incrementSubmatrices_bruteforce(n: int, queries: list[list[int]]) -> list[list[int]]:
    # 初始化 n×n 的全零矩阵
    mat = [[0] * n for _ in range(n)]

    # 对每一条查询，遍历子矩阵的每一个坐标并加一
    for row1, col1, row2, col2 in queries:
        for r in range(row1, row2 + 1):          # 行号从 row1 到 row2（含）
            for c in range(col1, col2 + 1):      # 列号从 col1 到 col2（含）
                mat[r][c] += 1                   # 对该格子加一
    return mat
```

#### 复杂度  

- **时间复杂度**：`O(Q * n²)`（最坏情况下每条查询的子矩阵可能是整个矩阵，`Q` 为查询条数）。  
  - 大白话：如果 `n=500`，`Q=10⁴`，理论上会进行 500·500·10⁴ ≈ 2.5×10⁹ 次加法，明显会超时。  
- **空间复杂度**：`O(n²)`，只需要保存最终的矩阵 `mat`。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每一次查询都要遍历子矩阵的所有格子**。  
我们可以把 “遍历所有格子” 的工作 **延后**，先只在每行的“边界”上做标记，等所有查询结束后再一次性把标记展开为真实的数值，这就是 **差分数组 + 前缀和** 的思想。

**关键观察**  
- 对一行来说，给区间 `[l, r]` 加 1 等价于：
  - 在位置 `l` 加 1（表示从这里开始要累计 +1），
  - 在位置 `r+1` 减 1（表示在这里停止累计 +1）。
- 当我们把所有查询的标记都加完后，对每一行做一次前缀和（从左到右累加），就会得到该行每个格子的真实值。

**实现步骤**  

1. **准备差分矩阵** `diff`，大小仍然是 `n × (n+1)`（多一列是为了处理 `r+1` 的减法，不越界）。  
2. **对每条查询** `[row1, col1, row2, col2]`  
   - 对行 `row1 … row2`（包括两端），在 `diff[row][col1]` 加 1，`diff[row][col2+1]` 减 1。  
   - 这一步只修改两列，时间是 `O(row2‑row1+1)`。  
3. **把差分矩阵恢复为结果矩阵**  
   - 对每一行 `r`，从左到右累计：`diff[r][c] += diff[r][c-1]`。  
   - 累计完后，前 `n` 列就是答案矩阵的第 `r` 行。  

**为什么对每行单独做差分就够了？**  
因为每一次查询的子矩阵是由若干连续的行组成的，对每行来说，它只关心自己所在列区间的增量。把每行的增量独立记录，然后再统一累计，就等价于在二维空间里一次性加 1。

#### 代码（Python）

```python
def incrementSubmatrices_optimal(n: int, queries: list[list[int]]) -> list[list[int]]:
    # 1. 差分矩阵，extra column 用来处理右边界的 -1
    diff = [[0] * (n + 1) for _ in range(n)]

    # 2. 对每条查询在对应的行上做差分标记
    for row1, col1, row2, col2 in queries:
        for r in range(row1, row2 + 1):          # 只遍历受影响的行
            diff[r][col1] += 1                    # 区间左端 +1
            diff[r][col2 + 1] -= 1                # 区间右端的下一格 -1（不会越界，因为多了一列）

    # 3. 把差分展开为真实值（前缀和），并写回到结果矩阵
    res = [[0] * n for _ in range(n)]
    for r in range(n):
        cur = 0                                 # 累计和变量
        for c in range(n):
            cur += diff[r][c]                   # 前缀和 = 前一个累计 + 本行差分
            res[r][c] = cur                     # 该格子的最终值
    return res
```

#### 复杂度  

- **时间复杂度**：`O(Q * H + n²)`，其中 `H` 是每条查询涉及的行数（`row2‑row1+1`）。  
  - 在最坏情况下，每条查询可能覆盖所有行，`H = n`，于是时间为 `O(Q·n + n²)`。  
  - 对于本题的约束 `n ≤ 500，Q ≤ 10⁴`，这大约是 `5·10⁶ + 2.5·10⁵` 次操作，完全可以在一秒左右跑完。  
- **空间复杂度**：`O(n²)`（`diff` 与返回的矩阵各占 `n×(n+1)` 和 `n×n`），只比暴力多了一个常数列。

---

## 心得

- **核心技巧**：**二维差分 + 行前缀和**（本质上是把二维区间加法拆解成多次一维区间加法）。  
- **适用的题型**  
  1. “子矩阵加值” 类问题（如 LeetCode 307、308）。  
  2. “二维区间查询/更新” 的离线处理（如矩阵翻转、涂色等）。  
- **一句话总结**：**把每一次“大面积”更新拆成“每行两点标记”，最后一次性累计**。

---

## 反思

- **第一反应**：看到“对每个子矩阵全部加 1”，自然想到直接遍历全部格子（暴力解）。  
- **最容易踩的坑**  
  - 忘记在 `col2+1` 位置做减法，会导致后面的格子累计过多。  
  - 差分矩阵的列数需要比原矩阵多一列，否则 `col2+1` 会越界。  
  - 当 `col2` 已经是最右侧时，`col2+1` 正好落在额外的第 `n` 列，这列在最终答案中不需要保留。  
- **下次遇到同类题**：第一步先问自己 **“能否把二维更新拆成多次一维更新？”**，如果能，就立刻考虑差分+前缀和的思路。