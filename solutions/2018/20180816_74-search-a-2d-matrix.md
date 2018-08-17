# #74. 搜索二维矩阵 / Search a 2D Matrix

> 难度：中等 · 标签：Array、Binary Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/search-a-2d-matrix/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix matrix with the following two properties:
Given an integer target, return true if target is in matrix or false otherwise.
You must write a solution in O(log(m * n)) time complexity.

**Examples**

**Example 1:**

```
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
```

**Example 2:**

```
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -104 <= matrix[i][j], target <= 104

---

## 题目（中文翻译）

你被给定一个 **m 行 n 列** 的整数矩阵 **matrix**，满足以下两个属性：

- （属性描述在原题中省略，此处保留原文结构）

给定一个整数 **target**，如果 **target** 出现在矩阵中返回 `true`，否则返回 `false`。

要求你的解法时间复杂度为 **O(log(m * n))**。

**示例 1**  

**输入**  
```
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
```
**输出**  
```
true
```

**示例 2**  

**输入**  
```
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
```
**输出**  
```
false
```

**约束条件**  

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把矩阵里的每一个元素都检查一遍，看看有没有等于 `target` 的。  
这相当于把矩阵当成一堆“盒子”，一个盒子装一个数，顺序打开每个盒子查看内容。  
- **使用的数据结构**：二维列表（`list[list[int]]`），在 Python 中就像一个装有若干行的表格，每行又是一个列表。  
- **为什么正确**：因为我们把所有可能的元素都遍历了一遍，只要有等于 `target` 的，必然会在遍历过程中被发现。  

#### 代码（Python）

```python
def searchMatrix_bruteforce(matrix, target):
    # matrix 是一个 m 行 n 列的二维列表
    for row in matrix:                 # 逐行遍历
        for num in row:                # 行内逐个检查
            if num == target:          # 找到目标直接返回 True
                return True
    return False                       # 全部检查完仍未找到，返回 False
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 这里的 `m` 是行数，`n` 是列数。我们最坏情况下要看遍历矩阵里的每一个元素，等价于“把所有盒子都打开”。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（`row`, `num`），不随矩阵大小增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**遍历所有元素是最慢的环节**，因为我们没有利用题目给出的两个重要属性：

1. 每一行从左到右是严格递增的。  
2. 第一行的最后一个数小于第二行的第一个数，第二行的最后一个数小于第三行的第一个数，……  

这两个条件等价于说：**把矩阵“摊平”成一个一维有序数组后，仍然是递增的**。  
因此我们可以把二维坐标 `(i, j)` 映射到一维下标 `k`：

```
k = i * n + j        (n 为每行的列数)
i = k // n           (整除得到行号)
j = k % n            (取余得到列号)
```

这样就可以在 **有序数组** 上使用二分查找（Binary Search），时间复杂度是 `O(log(m*n))`，满足题目要求。

**二分查找的核心思想**：  
- 设定搜索区间 `[left, right]`，初始为整个数组的下标范围 `[0, m*n-1]`。  
- 取中点 `mid = (left + right) // 2`，把 `mid` 映射回矩阵坐标 `(i, j)`，取出对应的数 `mid_val`。  
- 若 `mid_val == target`，直接返回 `True`。  
- 若 `mid_val < target`，说明目标只可能在右半边，`left = mid + 1`。  
- 若 `mid_val > target`，说明目标只可能在左半边，`right = mid - 1`。  
- 循环结束仍未找到，则返回 `False`。

下面用类比帮助理解：  
想象你有一本 **字典**（按字母顺序排好），要找某个单词，你不会从头到尾翻，而是先打开中间的页码，比较首字母决定向左还是向右继续找，这就是二分查找的思路。

#### 代码（Python）

```python
def searchMatrix(matrix, target):
    """
    在满足升序条件的二维矩阵中使用二分查找。
    时间复杂度 O(log(m * n))，空间复杂度 O(1)。
    """
    if not matrix or not matrix[0]:
        return False                     # 空矩阵直接返回 False

    m = len(matrix)                      # 行数
    n = len(matrix[0])                   # 列数
    left, right = 0, m * n - 1           # 一维下标的搜索区间

    while left <= right:
        mid = (left + right) // 2        # 取中点
        i = mid // n                     # 由一维下标得到行号
        j = mid % n                      # 由一维下标得到列号
        mid_val = matrix[i][j]           # 中点对应的矩阵元素

        if mid_val == target:            # 找到了
            return True
        elif mid_val < target:           # 目标在右侧
            left = mid + 1
        else:                            # 目标在左侧
            right = mid - 1

    return False                         # 循环结束仍未命中
```

#### 复杂度  

- **时间复杂度**：`O(log(m * n))`  
  - 每次循环都把搜索区间长度减半，就像把一本字典从 1000 页缩小到 500、250…，最多需要 `log₂(m*n)` 次比较。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`left, right, mid, i, j`），不随矩阵大小增加。

---

## 心得

- 这道题考察的核心技巧是 **把二维有序结构映射成一维有序序列，然后使用二分查找**。  
- 该技巧适用于：  
  1. “Search a 2D Matrix” 系列的变体（如矩阵每行首元素大于前一行末元素）。  
  2. “Kth Smallest Element in a Sorted Matrix”（使用二分或堆）等需要在有序矩阵中快速定位的题目。  
- **一句话总结解题钥匙**：把矩阵摊平成有序数组，二分即可。

---

## 反思

- **第一反应**：看到“矩阵每行递增、行与行之间也递增”，立刻想到可以把它当作一维有序序列来处理。  
- **最容易踩的坑**：  
  - 忘记检查空矩阵或空行导致下标越界。  
  - 在映射坐标时写错 `i = mid // n`、`j = mid % n`（比如把 `n` 写成 `m`）。  
  - 循环条件写成 `left < right` 而不是 `left <= right`，可能漏掉最后一个元素。  
- **下次遇到同类题**，第一步应该问自己：“矩阵是否可以等价为一维有序数组？”如果答案是“是”，立刻考虑二分查找。