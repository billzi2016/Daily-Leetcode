# #867. 转置矩阵 / Transpose Matrix

> 难度：简单 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/transpose-matrix/)

---

## 题目（英文原版）

**Description**

Given a 2D integer array matrix, return the transpose of matrix.
The transpose of a matrix is the matrix flipped over its main diagonal, switching the matrix's row and column indices.

**Examples**

**Example 1:**

```
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[1,4,7],[2,5,8],[3,6,9]]
```

**Example 2:**

```
Input: matrix = [[1,2,3],[4,5,6]]
Output: [[1,4],[2,5],[3,6]]
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 105
- -109 <= matrix[i][j] <= 109

---

## 题目（中文翻译）

给定一个二维整数数组 `matrix`，返回 `matrix` 的转置（transpose）。  
矩阵的转置是指沿着其主对角线（main diagonal）翻转矩阵，即交换矩阵的行索引和列索引。

示例 1：

示例 2：

约束条件：
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 10^5
- -10^9 <= matrix[i][j] <= 10^9

示例：
示例 1:
```text
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[1,4,7],[2,5,8],[3,6,9]]
```

示例 2:
```text
Input: matrix = [[1,2,3],[4,5,6]]
Output: [[1,4],[2,5],[3,6]]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每一行的第 i 个元素，搬到第 i 列的第 行**。  
可以把原矩阵想象成一本书的章节（行），每一页（列）上都有文字。转置相当于把“章节号”变成“页码”，把“页码”变成“章节号”。  
实现上，只需要两个循环：

1. 外层遍历列下标 `i`（因为转置后列数等于原矩阵的行数）。  
2. 内层遍历原矩阵的每一行 `row`，把 `row[i]` 收集起来，形成转置后的新行。

这样得到的每一行就是原矩阵的第 i 列。由于我们把所有元素都搬了一遍，结果必然正确。

#### 代码（Python）

```python
def transpose(matrix):
    """
    :param matrix: List[List[int]] 原矩阵，行数为 m，列数为 n
    :return: List[List[int]] 转置后的矩阵，行数为 n，列数为 m
    """
    m = len(matrix)          # 原矩阵的行数
    n = len(matrix[0])       # 原矩阵的列数（题目保证每行长度相同）

    # 用一个外层循环遍历每一列 i（转置后会成为新矩阵的第 i 行）
    result = []              # 用来存放转置后的所有行
    for i in range(n):       # n 次，也就是转置后有 n 行
        new_row = []         # 第 i 行的内容
        for r in range(m):  # 遍历原矩阵的每一行
            new_row.append(matrix[r][i])   # 把原第 r 行第 i 列的元素搬过来
        result.append(new_row)            # 完成第 i 行后放进结果
    return result
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  解释：我们需要访问矩阵中的每一个元素一次。比如 3 × 4 的矩阵有 12 个数，就会做 12 次「搬运」操作。`m` 是行数，`n` 是列数，乘起来就是总元素个数。

- **空间复杂度**：`O(m * n)`  
  解释：转置后得到的新矩阵同样需要存放所有元素，大小和原矩阵一样。因此额外的空间正好是原矩阵元素的个数。

---

### 2. 最优解

#### 思路  
上面的暴力解已经是最优的时间复杂度 `O(m·n)`，因为任何算法都必须看到每个元素才能把它搬到新位置。  
我们可以把实现方式写得更简洁、更「Pythonic」：

- **`zip`**：把多个可迭代对象的第 i 个元素“打包”成一个元组。把矩阵的每一行当作一个可迭代对象，`zip(*matrix)` 就会把第 0 列的所有元素打成一个元组，第 1 列的所有元素打成另一个元组……这正好是转置的结果。  
- **列表推导式**：把每个 `zip` 产生的元组再转成列表，得到最终的二维列表。

这里的核心概念是“解包（*）”。把矩阵的行列表解包后作为 `zip` 的多个参数，相当于让 `zip` 同时遍历所有行，从而一次完成列到行的转换。

#### 代码（Python）

```python
def transpose(matrix):
    """
    使用 zip + 解包，实现一行代码的转置。
    zip(*matrix) 把第 0 列、第 1 列、... 打包成元组。
    再把每个元组转成列表，得到最终的二维列表。
    """
    # zip 返回的是迭代器，每个元素是一个元组，需要转成 list
    return [list(col) for col in zip(*matrix)]
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  解释：`zip` 仍然会遍历所有元素一次，和暴力解一样快，无法再更快了。

- **空间复杂度**：`O(m * n)`  
  解释：同样需要存放转置后的矩阵，空间使用没有变化。  

相比暴力解，**代码行数更少、可读性更高**，而且完全利用了 Python 的内置特性。

---

## 心得

- **核心技巧**：把矩阵的行列互换——转置。常用工具是双层循环或 `zip(*matrix)`。
- **适用的题型**：  
  1. 矩阵转置（本题）。  
  2. 求矩阵的对称矩阵或共轭转置。  
  3. 在图像处理里把图片顺时针/逆时针旋转 90°（需要先转置再翻转）。
- **一句话总结**：`zip(*matrix)` 就是“把所有行的同位元素拉在一起”，是转置的钥匙。

---

## 反思

- **第一反应**：看到“把行变列”，立刻想到两层循环把每个 `matrix[r][c]` 放到 `result[c][r]`。  
- **最容易踩的坑**：  
  - 忘记先读取矩阵的列数 `n`，导致外层循环次数写错。  
  - 对不规则矩阵（行长度不一致）使用 `zip(*matrix)` 会自动截短，需确保输入满足“每行长度相同”。  
- **下次遇到同类题的第一步**：先判断是否可以直接用语言自带的 **解包 + zip**，如果不行再回到最直接的双层循环实现。