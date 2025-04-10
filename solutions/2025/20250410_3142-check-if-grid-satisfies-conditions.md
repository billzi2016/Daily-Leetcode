# #3142. 检查网格是否满足条件 / Check if Grid Satisfies Conditions

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/check-if-grid-satisfies-conditions/)

---

## 题目（英文原版）

**Description**

You are given a 2D matrix grid of size m x n. You need to check if each cell grid[i][j] is:
Return true if all the cells satisfy these conditions, otherwise, return false.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,2],[1,0,2]]
Output: true
Explanation:

All the cells in the grid satisfy the conditions.
```

**Example 2:**

```
Input: grid = [[1,1,1],[0,0,0]]
Output: false
Explanation:

All cells in the first row are equal.
```

**Example 3:**

```
Input: grid = [[1],[2],[3]]
Output: false
Explanation:

Cells in the first column have different values.
```

**Constraints**

- 1 <= n, m <= 10
- 0 <= grid[i][j] <= 9

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的二维矩阵 `grid`。请检查是否每个单元格 `grid[i][j]` 同时满足以下两个条件：

1. 同一行（row）中的所有元素互不相同（distinct）。  
2. 同一列（column）中的所有元素相等。

若矩阵中的所有单元格均满足上述条件，返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**输入:** `grid = [[1,0,2],[1,0,2]]`  
**输出:** `true`  
**解释:**  
所有行的元素各不相同，且每一列的元素都相等，满足条件。

### 示例 2
**输入:** `grid = [[1,1,1],[0,0,0]]`  
**输出:** `false`  
**解释:**  
第一行的所有元素相同，违反了“行内元素互不相同”的要求。

### 示例 3
**输入:** `grid = [[1],[2],[3]]`  
**输出:** `false`  
**解释:**  
第一列的元素分别为 1、2、3，不相等，违反了“列内元素相等”的要求。

## 约束条件
- `1 <= n, m <= 10`
- `0 <= grid[i][j] <= 9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的要求可以拆成 **两条** 简单的规则：

1. **同一列的所有单元格必须相等**  
   把每一列想象成一本书的“章节”。章节里每一页（行）都必须写同样的内容，才能算合格。检查时，只要把第一行的值记下来，然后把同一列的其它行逐个对比就行了。

2. **相邻两列的数值必须不同**  
   把每一列的“章节编号”拿出来（也就是该列的值），相邻的章节编号不能相同。因为每列内部已经保证一致，只需要比较每列的**第一行**（或任意一行）的数值即可。

只要这两条规则都满足，答案就是 `True`，否则 `False`。

**为什么暴力解一定正确？**  
- 第一步遍历所有列、所有行，确保每列内部一致；如果有一列不一致，必然违背题目要求，直接返回 `False`。  
- 第二步只比较相邻列的“代表值”（第一行的数），因为已经保证同列内部相同，这一步即可判断相邻列是否相同。

**时间/空间复杂度**（大白话）  
- 我们需要把每个格子都看一遍，格子的总数是 `m × n`（`m` 行、`n` 列），所以时间是 **`O(m·n)`**，意思是“和格子数量成正比”。  
- 只用了常数个额外变量（比如 `prev`、`cur`），不随 `m`、`n` 增长，所以空间是 **`O(1)`**，意思是“几乎不占额外内存”。

#### 代码（Python）

```python
def check_grid(grid):
    """
    判断二维矩阵是否满足：
    1) 每一列的所有元素相等
    2) 相邻列的值不同
    """
    m = len(grid)          # 行数
    n = len(grid[0])       # 列数

    # 1) 检查每列内部是否相等
    for col in range(n):
        # 取该列的第一个元素作为基准
        base = grid[0][col]
        for row in range(1, m):
            if grid[row][col] != base:   # 只要有一个不相等，就不满足条件
                return False

    # 2) 检查相邻列的基准值是否不同
    for col in range(1, n):
        if grid[0][col] == grid[0][col - 1]:   # 前后两列相同 → 失败
            return False

    return True
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  需要遍历矩阵的每一个格子一次。比如 5×5 的矩阵需要检查 25 次。

- **空间复杂度**：`O(1)`  
  只用了常数个变量 `m, n, base, row, col`，不随矩阵大小增长。

---

### 2. 最优解

#### 思路  

从暴力解来看，**唯一的瓶颈**就是我们分别用了两次遍历：

1. 第一次遍历检查每列是否一致（`m·n` 次比较）。  
2. 第二次遍历检查相邻列是否不同（`n‑1` 次比较）。

其实这两件事可以 **合并在一次遍历里** 完成。  
遍历矩阵时，**按列** 依次处理每一列的所有行：

- 当我们在处理第 `col` 列时，顺便把该列的基准值（`grid[0][col]`）和上一列的基准值比较一次。  
- 同时在同一列内部，检查每一行是否与基准相同。

这样只需要一次完整的矩阵遍历，就能同时验证两条规则，时间仍是 `O(m·n)`，但只做一次遍历，代码更简洁，常数因子更小。

**核心技巧**：**一次遍历同时做多件事**。这在很多矩阵/数组题目里都非常有用——只要把所有需要的检查条件写进同一个循环体，就能省去多余的遍历。

#### 代码（Python）

```python
def check_grid(grid):
    """
    一次遍历同时完成：
    1) 每列内部所有元素相等
    2) 相邻列的基准值不同
    """
    m = len(grid)
    n = len(grid[0])

    # prev_val 用来记录前一列的基准值（第一行的数），初始化为 None
    prev_val = None

    for col in range(n):
        # 当前列的基准值（第一行的数）
        cur_val = grid[0][col]

        # ① 检查相邻列是否相同（从第二列开始比较）
        if prev_val is not None and cur_val == prev_val:
            return False
        prev_val = cur_val

        # ② 检查当前列内部是否全相等
        for row in range(1, m):
            if grid[row][col] != cur_val:
                return False

    # 所有检查都通过
    return True
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  只遍历一次矩阵，仍然和格子数量成正比。相比两次遍历的写法，常数因子更小，实际运行更快。

- **空间复杂度**：`O(1)`  
  只用了 `prev_val`、`cur_val`、`row`、`col` 四个额外变量，空间占用不随输入规模变化。

---

## 心得

- **核心技巧**：一次遍历同时完成多项检查（这里是列内部相等 + 相邻列不同）。  
- **适用的题型**  
  1. 检查二维矩阵的行/列属性（如“每行递增且相邻行首元素不同”）。  
  2. 一维数组的连续子段满足多重条件（如“所有子段内部相等且相邻子段不同”）。  
- **解题钥匙**：**把所有条件都写进同一个循环**，避免重复遍历。

---

## 反思

- **第一反应**：把两条规则分开写，两次遍历实现。  
- **最容易踩的坑**  
  - 忽略了 **相邻列必须不同** 这条规则，只检查了列内部相等。  
  - 边界情况：只有一列时，第二条规则自然成立，代码要避免访问 `prev_val` 时产生错误。  
- **下次遇到同类题**：先在脑中把所有检查条件列出来，思考它们是否可以在同一次遍历里完成；如果可以，就把它们写进同一个 `for` 循环，省去不必要的循环层数。