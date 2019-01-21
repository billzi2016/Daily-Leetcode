# #240. 搜索二维矩阵 II / Search a 2D Matrix II

> 难度：中等 · 标签：Array、Binary Search、Divide and Conquer、Matrix · [LeetCode 链接](https://leetcode.com/problems/search-a-2d-matrix-ii/)

---

## 题目（英文原版）

**Description**

Write an efficient algorithm that searches for a value target in an m x n integer matrix matrix. This matrix has the following properties:

**Examples**

**Example 1:**

```
Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
Output: true
```

**Example 2:**

```
Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
Output: false
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= n, m <= 300
- -109 <= matrix[i][j] <= 109
- All the integers in each row are sorted in ascending order.
- All the integers in each column are sorted in ascending order.
- -109 <= target <= 109

---

## 题目（中文翻译）

编写一个高效的算法，在一个 **m × n** 的整数矩阵（**matrix**）中搜索目标值（**target**）。该矩阵满足以下性质：

- 每一行中的所有整数均按升序排列。
- 每一列中的所有整数亦按升序排列。

**示例 1**  
**输入**: `matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5`  
**输出**: `true`

**示例 2**  
**输入**: `matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20`  
**输出**: `false`

### 约束条件
- `m == matrix.length`
- `n == matrix[i].length`
- `1 ≤ m, n ≤ 300`
- `-10^9 ≤ matrix[i][j] ≤ 10^9`
- `-10^9 ≤ target ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把矩阵当成一本“数字书”，把每一页（每一行）和每一行里的每个数字都翻一遍，看到目标值就返回 `True`，遍历完整个矩阵仍未找到则返回 `False`。  
这里用到的数据结构只有 **列表（list）**，因为 Python 的二维矩阵本质上是「列表的列表」——就像把若干本同样大小的书堆在一起，每本书对应一行。

为什么这个方法一定能得到正确答案？因为题目只要求判断 **是否存在**，只要把所有可能的元素都检查一遍，就不可能漏掉目标值。

#### 代码（Python）

```python
def searchMatrix_brute(matrix, target):
    """
    暴力遍历每一个元素
    :param matrix: List[List[int]]
    :param target: int
    :return: bool
    """
    # 外层遍历每一行
    for i, row in enumerate(matrix):
        # 内层遍历行内每个数
        for j, val in enumerate(row):
            # 找到目标直接返回 True
            if val == target:
                # print(f"在第{i}行第{j}列找到了目标 {target}")
                return True
    # 所有元素都检查完仍未找到
    return False
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  这里的 `m` 是行数，`n` 是列数。意思是「最坏情况下，需要检查矩阵里所有 `m×n` 个格子」，就像要把一本 100 页的字典每一页的每个单词都读一遍。  
- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量（循环计数器），不随矩阵大小增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于「每个格子都要看」。矩阵的两条排序特性其实给了我们方向感：

- 每行从左到右递增  
- 每列从上到下递增  

想象我们站在矩阵的 **右上角**（第一行最后一列），此时：

- 向左走会让数 **变小**（因为同一行左边的数更小）  
- 向下走会让数 **变大**（因为同一列下面的数更大）  

因此我们可以把「比较」的结果转化为「移动」的方向：

1. 若当前数字 **等于** `target`，直接返回 `True`。  
2. 若当前数字 **大于** `target`，说明目标不可能在当前列的更下方（因为下方更大），只能往左走，尝试更小的数。  
3. 若当前数字 **小于** `target`，说明目标不可能在当前行的更左侧（因为左侧更小），只能往下走，尝试更大的数。

每一步都把搜索范围缩小一行或一列，最多走 `m + n` 步就会跑出矩阵边界。这样就把原本的 `m·n` 次检查降到了线性 `m+n`。

> **类比**：把矩阵想象成一座「高低起伏的山脉」，我们站在最高点（右上角），想找特定海拔的点。若当前海拔太高，就往左走（海拔下降），太低就往下走（海拔上升），一步步逼近目标。

#### 代码（Python）

```python
def searchMatrix_opt(matrix, target):
    """
    从右上角开始，利用行列有序的特性进行线性搜索
    :param matrix: List[List[int]]
    :param target: int
    :return: bool
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    # 起始位置：第一行最后一列
    row, col = 0, n - 1

    while row < m and col >= 0:
        cur = matrix[row][col]
        # print(f"检查位置 ({row}, {col})，值为 {cur}")

        if cur == target:          # 找到目标
            return True
        elif cur > target:         # 当前值太大，左移寻找更小的数
            col -= 1
        else:                      # 当前值太小，下移寻找更大的数
            row += 1

    # 走出矩阵边界仍未找到
    return False
```

#### 复杂度  

- **时间复杂度**：`O(m + n)`  
  最多向左走 `n` 步（每列只走一次），向下走 `m` 步（每行只走一次），所以总步数不超过 `m + n`。这比 `m·n` 省了很多，就像在一条直路上找目标，而不是在整个城市里随意跑。  
- **空间复杂度**：`O(1)`  
  只用了几个整型变量 `row、col、cur`，不随矩阵规模增大。

---

## 心得

- **核心技巧**：利用矩阵的“行递增、列递增”特性，**从右上角或左下角** 开始，用“比较后决定向左或向下” 的思路把搜索空间一次削减一行或一列。  
- **适用的题型**  
  1. **Search a 2D Matrix I**（把矩阵看成一维有序数组，用二分查找）  
  2. **Kth Smallest Element in a Sorted Matrix**（同样利用行列有序，用二分或堆）  
  3. **Count Negative Numbers in a Sorted Matrix**（同理，从左下角或右上角计数）  
- **一句话总结**：**“在有序矩阵里，站在右上角，比较后左移或下移，就能线性找到目标。”**

## 反思

- **第一反应**：直接遍历所有元素——最安全但最慢。  
- **最容易踩的坑**  
  - 忘记处理空矩阵或空行的边界（`if not matrix`）。  
  - 把「左移」写成「右移」或「下移」写成「上移」，会导致无限循环或错过目标。  
  - 目标值可能在矩阵的最左下角或最右上角，需要确保循环条件 `row < m and col >= 0` 正确。  
- **下次遇到同类题**：第一步立刻问自己——**“矩阵有没有行/列有序？”** 若有，立刻把指针放在右上角或左下角，准备用“比较后移动” 的线性搜索策略。