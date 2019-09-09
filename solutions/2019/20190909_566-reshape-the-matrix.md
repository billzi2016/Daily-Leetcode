# #566. 矩阵重塑 / Reshape the Matrix

> 难度：简单 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/reshape-the-matrix/)

---

## 题目（英文原版）

**Description**

In MATLAB, there is a handy function called reshape which can reshape an m x n matrix into a new one with a different size r x c keeping its original data.
You are given an m x n matrix mat and two integers r and c representing the number of rows and the number of columns of the wanted reshaped matrix.
The reshaped matrix should be filled with all the elements of the original matrix in the same row-traversing order as they were.
If the reshape operation with given parameters is possible and legal, output the new reshaped matrix; Otherwise, output the original matrix.

**Examples**

**Example 1:**

```
Input: mat = [[1,2],[3,4]], r = 1, c = 4
Output: [[1,2,3,4]]
```

**Example 2:**

```
Input: mat = [[1,2],[3,4]], r = 2, c = 4
Output: [[1,2],[3,4]]
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 100
- -1000 <= mat[i][j] <= 1000
- 1 <= r, c <= 300

---

## 题目（中文翻译）

在 MATLAB 中，有一个非常便利的函数 **reshape**，它可以将一个 *m × n* 矩阵重新排列成大小为 *r × c* 的新矩阵，同时保持原始数据的顺序不变。  
给定一个 *m × n* 矩阵 `mat`，以及两个整数 `r` 和 `c`，分别表示期望得到的重塑后矩阵的行数和列数。  
重塑后的矩阵应按照原矩阵的**行遍历顺序**（row‑traversing order）依次填充所有元素。  
如果使用给定的参数能够合法地完成重塑操作，则输出新的重塑矩阵；否则，输出原矩阵。

**示例 1**  
**示例 2**  
**约束条件**：

- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 100`
- `-1000 <= mat[i][j] <= 1000`
- `1 <= r, c <= 300`

---

#### 示例

**示例 1**  
输入: `mat = [[1,2],[3,4]], r = 1, c = 4`  
输出: `[[1,2,3,4]]`

**示例 2**  
输入: `mat = [[1,2],[3,4]], r = 2, c = 4`  
输出: `[[1,2],[3,4]]`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是 **把原矩阵的所有元素一个一个读出来，顺序放进新的矩阵**。  
可以把这一步想象成：

- **把原矩阵的每一行当成一本书的章节**，先读完第一章的所有页（即第一行的所有元素），再读第二章，依次类推。  
- **把这些页码写到新书的页面上**，新书的页面数是 `r × c`，我们仍然按顺序填满每一页。

实现时只需要两层循环遍历原矩阵，把每个元素放到新矩阵对应的位置。  
位置的映射可以用「一维索引 → 二维坐标」的公式：

```
k = 已经放进去的元素个数（从 0 开始计数）
新矩阵的行号 = k // c          （除法取整，相当于“第几行”）
新矩阵的列号 = k %  c          （取余，相当于“第几列”）
```

为什么这样做是对的？因为我们严格保持了「行遍历顺序」——先填满一行，再填下一行，正好和原矩阵的遍历顺序一致。

#### 代码（Python）

```python
from typing import List

def matrixReshape(mat: List[List[int]], r: int, c: int) -> List[List[int]]:
    m, n = len(mat), len(mat[0])          # 原矩阵的行数和列数
    total = m * n                         # 元素总数

    # 如果元素总数不匹配，直接返回原矩阵
    if total != r * c:
        return mat

    # 先准备一个 r 行 c 列的空矩阵
    reshaped = [[0] * c for _ in range(r)]

    k = 0                                 # 已经放进去的元素个数
    for i in range(m):
        for j in range(n):
            # 计算新矩阵的行列坐标
            new_row = k // c
            new_col = k % c
            reshaped[new_row][new_col] = mat[i][j]   # 把元素搬过去
            k += 1

    return reshaped
```

#### 复杂度  

- **时间复杂度：** `O(m·n)`  
  解释：我们要遍历原矩阵的每一个元素一次，`m·n` 就是矩阵的大小。  
  “`O(m·n)`” 的含义可以理解为「工作量随矩阵元素个数线性增长」，元素多两倍，时间也大约会翻倍。

- **空间复杂度：** `O(r·c)`（即 `O(m·n)`）  
  解释：需要额外创建一个和答案等大的新矩阵来存放结果，大小正好是 `r·c`。  
  如果不能 reshape（直接返回原矩阵），则不占额外空间。

---

### 2. 最优解  

#### 思路  
从上面的暴力解可以看到，核心工作只有 **一次遍历**，已经是线性时间 `O(m·n)`，没有多余的嵌套循环。因此在时间上已经达到了最优。  
唯一可以改进的地方是 **空间**：如果题目允许 **原地修改**（在原矩阵上直接重新组织），可以省去额外的 `O(r·c)` 空间。但 LeetCode 要求返回一个新矩阵（或原矩阵），所以我们仍需要一个结果容器。

下面给出一种更简洁的实现思路：

1. **先把所有元素拉平成一维列表**（相当于把书的所有章节的页码放进一本长卷轴）。  
2. **再按照 `c` 为步长切片**，直接生成每一行。  
3. 这一步利用 Python 的列表切片特性，代码非常短。

核心概念仍是「一维索引 ↔ 二维坐标」，只不过把手动的 `//`、`%` 运算交给了切片操作。

#### 代码（Python）

```python
from typing import List

def matrixReshape(mat: List[List[int]], r: int, c: int) -> List[List[int]]:
    m, n = len(mat), len(mat[0])
    total = m * n
    if total != r * c:            # 不能 reshape，直接返回原矩阵
        return mat

    # 1️⃣ 把矩阵拉平成一维列表
    flat = [num for row in mat for num in row]   # 嵌套列表推导式

    # 2️⃣ 按每 c 个元素切成一行，组成 r 行的结果矩阵
    reshaped = [flat[i * c:(i + 1) * c] for i in range(r)]

    return reshaped
```

> **代码解释**  
> - `flat = [num for row in mat for num in row]`  
>   相当于「先遍历每一行 `row`，再遍历行里的每个数字 `num`，把它们依次放进 `flat` 列表」；这一步的时间仍是 `O(m·n)`。  
> - `flat[i * c:(i + 1) * c]` 用切片一次性取出第 `i` 行需要的 `c` 个元素，省去了手动算行列坐标的过程。

#### 复杂度  

- **时间复杂度：** `O(m·n)`  
  与暴力解相同，只是代码更紧凑。我们仍然只遍历一次原矩阵的所有元素。

- **空间复杂度：** `O(m·n)`  
  需要额外的 `flat` 列表（长度 `m·n`）以及最终的 `reshaped` 矩阵。若把 `flat` 看作临时缓冲区，整体仍是 `O(r·c)`。

---

## 心得  

- **核心技巧**：一维索引 ↔ 二维坐标的映射（除法取整 `//` 与取余 `%`），以及利用列表推导式和切片实现「拉平‑切片」的思路。  
- **适用的题型**：  
  1. **矩阵展平/重塑**（如本题、LeetCode 566. Reshape the Matrix）。  
  2. **图像/像素的线性化**（如把二维图片转成一维数组进行卷积）。  
  3. **把二维坐标映射到一维数组的缓存**（常见于实现自定义哈希表、位图等）。  
- **一句话总结解题钥匙**：**把二维位置转成“一条直线”上的下标，用除法/取余或切片把它们重新拼回所需的形状**。

## 反思  

- **第一反应**：先检查元素总数是否匹配，若不匹配直接返回原矩阵；否则想办法把元素按顺序搬过去。  
- **最容易踩的坑**：  
  - 忘记检查 `m·n` 是否等于 `r·c`，导致下标越界。  
  - 在手动计算新坐标时，除法和取余写反了（`new_row = k % c`、`new_col = k // c`）会导致行列颠倒。  
  - 对空矩阵或只有一行/一列的特殊情况不做额外处理，代码仍然能正常工作。  
- **下次遇到同类题**，第一步应想到 **“先把所有元素拉平成一维，再按目标宽度切块”**，或者直接用 **“除法+取余”** 把一维下标映射到新矩阵的行列。这样既直观又易于实现。