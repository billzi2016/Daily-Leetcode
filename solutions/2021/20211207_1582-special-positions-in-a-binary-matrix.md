# #1582. 二进制矩阵中的特殊位置 / Special Positions in a Binary Matrix

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/special-positions-in-a-binary-matrix/)

---

## 题目（英文原版）

**Description**

Given an m x n binary matrix mat, return the number of special positions in mat.
A position (i, j) is called special if mat[i][j] == 1 and all other elements in row i and column j are 0 (rows and columns are 0-indexed).

**Examples**

**Example 1:**

```
Input: mat = [[1,0,0],[0,0,1],[1,0,0]]
Output: 1
Explanation: (1, 2) is a special position because mat[1][2] == 1 and all other elements in row 1 and column 2 are 0.
```

**Example 2:**

```
Input: mat = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
Explanation: (0, 0), (1, 1) and (2, 2) are special positions.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 100
- mat[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 `m x n` 的二进制矩阵（binary matrix）`mat`，返回矩阵中 **特殊位置**（special positions）的数量。  
如果位置 `(i, j)` 满足 `mat[i][j] == 1` 且该行 `i` 的其余元素以及该列 `j` 的其余元素全部为 `0`（行列均采用 0 起始索引），则称其为 **特殊位置**。

**示例 1**  
**输入**：`mat = [[1,0,0],[0,0,1],[1,0,0]]`  
**输出**：`1`  
**解释**：`(1, 2)` 是特殊位置，因为 `mat[1][2] == 1`，且第 1 行和第 2 列的其他元素全部为 `0`。

**示例 2**  
**输入**：`mat = [[1,0,0],[0,1,0],[0,0,1]]`  
**输出**：`3`  
**解释**：`(0, 0)`, `(1, 1)` 和 `(2, 2)` 均为特殊位置。

**约束条件**  
- `m == mat.length`  
- `n == mat[i].length`  
- `1 <= m, n <= 100`  
- `mat[i][j]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：遍历矩阵里的每一个元素 `(i, j)`，  
- 如果 `mat[i][j] == 1`，就检查它所在的 **整行** `i` 和 **整列** `j`，看除了这个位置之外，是否还有别的 `1`。  
- 若整行和整列里除了 `(i, j)` 之外全是 `0`，就把答案加一。

> **数据结构类比**  
> - 矩阵本身就像一本**二维的账本**，行是“同一时间段的记录”，列是“同一类别的记录”。我们要找的特殊位置，就是“只有这一格记了‘1’，其它同一行、同一列的格子全是‘0’”。  
> - 检查行或列时，只需要顺序遍历就行，类似于在账本里翻到对应的那一页，一页页看有没有别的记号。

**为什么正确**  
因为题目要求“行里只有这一格是 1，列里也只有这一格是 1”。只要我们逐个验证每个 `1` 是否满足这两个条件，就一定能找出所有特殊位置，且不会漏掉。

**时间/空间复杂度**  
- 对每个 `1`（最坏情况下矩阵全是 `1`），我们要检查它所在的整行 `n` 个元素和整列 `m` 个元素，时间是 `O(m + n)`。  
- 矩阵里有 `m·n` 个格子，所以总体时间是 `O(m·n·(m + n))`。  
  - 用大白话说，就是“遍历所有格子（`m·n` 次），每次还要再去看一遍它所在的行和列”，所以会慢一点。  
- 只用了原矩阵本身，没有额外的数据结构，空间是 `O(1)`（常数级）。

#### 代码（Python）

```python
from typing import List

def numSpecial_brute(mat: List[List[int]]) -> int:
    m, n = len(mat), len(mat[0])
    ans = 0

    for i in range(m):
        for j in range(n):
            # 只关心值为 1 的格子
            if mat[i][j] != 1:
                continue

            # 检查同一行是否只有这一个 1
            row_ok = True
            for col in range(n):
                if col != j and mat[i][col] == 1:
                    row_ok = False          # 行里还有别的 1，直接否定
                    break

            # 检查同一列是否只有这一个 1
            col_ok = True
            for row in range(m):
                if row != i and mat[row][j] == 1:
                    col_ok = False          # 列里还有别的 1，直接否定
                    break

            # 同时满足行、列条件才算特殊位置
            if row_ok and col_ok:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n·(m + n))`  
  - 解释：遍历每个格子 `m·n` 次，每次最坏要检查一整行 `n` 和一整列 `m`，所以乘在一起就是 `m·n·(m+n)`。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数器和布尔变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历整行整列**。其实我们只需要知道每一行有多少个 `1`，每一列有多少个 `1`，这些信息可以**一次遍历矩阵就算出来**，后面再判断时就只要 O(1) 时间。

**步骤**  

1. **第一次遍历**：用两个一维数组  
   - `row_cnt[i]` 记录第 `i` 行 `1` 的个数。  
   - `col_cnt[j]` 记录第 `j` 列 `1` 的个数。  
   这一步相当于先把“每行每列有多少记号”记在一本**统计表**里（就像把账本里每页的记号总数先算好），时间是 `O(m·n)`，空间是 `O(m + n)`。

2. **第二次遍历**：再次遍历矩阵，遇到 `mat[i][j] == 1` 时，直接检查 `row_cnt[i] == 1` 且 `col_cnt[j] == 1`。如果成立，就说明这格子是唯一的 `1`，即特殊位置。此时不需要再去看整行整列，判断是常数时间 `O(1)`。

这样总时间是两次遍历矩阵，`O(2·m·n) = O(m·n)`，空间多用了两个计数数组 `O(m + n)`，在本题的约束（`m, n ≤ 100`）下完全可以接受。

> **核心数据结构解释**  
> - **数组（list）** 就像一本**一维的目录**，下标是行号或列号，存的值是对应行/列里 `1` 的数量。查一次目录只要 `O(1)`，非常快。  
> - 这里不需要哈希表，因为行号和列号本身就是连续的整数，直接用下标存取最方便。

#### 代码（Python）

```python
from typing import List

def numSpecial(mat: List[List[int]]) -> int:
    m, n = len(mat), len(mat[0])

    # 1. 统计每行、每列的 1 的个数
    row_cnt = [0] * m          # row_cnt[i] = 第 i 行中 1 的数量
    col_cnt = [0] * n          # col_cnt[j] = 第 j 列中 1 的数量

    for i in range(m):
        for j in range(n):
            if mat[i][j] == 1:
                row_cnt[i] += 1
                col_cnt[j] += 1

    # 2. 再次遍历，找出满足条件的特殊位置
    ans = 0
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 1 and row_cnt[i] == 1 and col_cnt[j] == 1:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 解释：只遍历矩阵两遍，每遍都是 `m·n` 次基本操作，整体线性增长，和矩阵大小成正比。比暴力的 `O(m·n·(m+n))` 快很多，尤其当 `m`、`n` 较大时差距明显。  
- **空间复杂度**：`O(m + n)`  
  - 解释：额外用了两条一维数组，分别保存每行、每列的计数。占用的空间随行数和列数线性增长，但相对于矩阵本身仍然是很小的开销。

---

## 心得

- **核心技巧**：使用**行/列计数**（前缀计数的简化版）一次遍历即可得到全局信息，后续判断只需 O(1)。
- **适用的题型**  
  1. “只出现一次的元素”类题目（如矩阵中唯一的 1、唯一的 0）。  
  2. “行列约束”类题目，例如 LeetCode 1461 *Check If a String Is a Valid Sequence from Root to Leaves Path in a Binary Tree*（思路类似的统计路径出现次数）。  
  3. “统计行/列特性”类题目，如 1462 *Course Schedule IV* 中的前置关系计数。
- **一句话总结解题钥匙**：**先把每行每列的 1 的数量统计下来，后面只需要看这个数字是否为 1**。

---

## 反思

- **第一反应**：直接遍历每个 `1`，逐行逐列检查——这是最自然的暴力思路。  
- **最容易踩的坑**  
  - 忘记排除当前格子本身，在检查行/列时要 `col != j`、`row != i`。  
  - 边界情况：矩阵只有一行或一列时，行计数和列计数会重合，需要保证统计和判断逻辑都能覆盖。  
- **下次类似题的第一步**：先思考“是否可以把行/列（或其他维度）的信息预先统计”，把全局信息压缩到 O(m+n) 的数组里，再在遍历时直接利用这些信息完成判断。这样往往能把暴力的 O(m·n·(m+n)) 降到 O(m·n)。