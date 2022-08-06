# #1886. 判断矩阵是否可以通过旋转得到 / Determine Whether Matrix Can Be Obtained By Rotation

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/determine-whether-matrix-can-be-obtained-by-rotation/)

---

## 题目（英文原版）

**Description**

Given two n x n binary matrices mat and target, return true if it is possible to make mat equal to target by rotating mat in 90-degree increments, or false otherwise.

**Examples**

**Example 1:**

```
Input: mat = [[0,1],[1,0]], target = [[1,0],[0,1]]
Output: true
Explanation: We can rotate mat 90 degrees clockwise to make mat equal target.
```

**Example 2:**

```
Input: mat = [[0,1],[1,1]], target = [[1,0],[0,1]]
Output: false
Explanation: It is impossible to make mat equal to target by rotating mat.
```

**Example 3:**

```
Input: mat = [[0,0,0],[0,1,0],[1,1,1]], target = [[1,1,1],[0,1,0],[0,0,0]]
Output: true
Explanation: We can rotate mat 90 degrees clockwise two times to make mat equal target.
```

**Constraints**

- n == mat.length == target.length
- n == mat[i].length == target[i].length
- 1 <= n <= 10
- mat[i][j] and target[i][j] are either 0 or 1.

---

## 题目（中文翻译）

**描述**  
给定两个 `n x n` 的二进制矩阵（binary matrix）`mat` 和 `target`，如果可以通过对 `mat` 进行若干次 **90 度（90-degree）** 旋转（顺时针或逆时针均可）使其与 `target` 相等，则返回 `true`，否则返回 `false`。

**示例 1**  
```text
Input: mat = [[0,1],[1,0]], target = [[1,0],[0,1]]
Output: true
Explanation: 我们可以将 `mat` 顺时针旋转 90 度，使其等于 `target`。
```

**示例 2**  
```text
Input: mat = [[0,1],[1,1]], target = [[1,0],[0,1]]
Output: false
Explanation: 无法通过旋转 `mat` 使其等于 `target`。
```

**示例 3**  
```text
Input: mat = [[0,0,0],[0,1,0],[1,1,1]], target = [[1,1,1],[0,1,0],[0,0,0]]
Output: true
Explanation: 我们可以将 `mat` 顺时针旋转两次（每次 90 度），使其等于 `target`。
```

**约束条件**  
- `n == mat.length == target.length`  
- `n == mat[i].length == target[i].length`  
- `1 <= n <= 10`  
- `mat[i][j]` 和 `target[i][j]` 仅为 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把矩阵不断顺时针转 90 度，最多转四次**（因为四次转一圈又回到原来的模样），每一次转完后把得到的矩阵和 `target` 逐个元素比较，如果全部相同就说明可以得到目标。

- **使用的数据结构**：  
  - `list[list[int]]`（二维列表）来存放矩阵。可以把它想象成 Excel 表格，行号是行，列号是列。  
  - “哈希表”在这里不需要，用最朴素的逐元素比较就行。

- **为什么正确**：  
  - 题目只允许 0、90、180、270 度四种旋转方式。遍历这四种情况就一定能覆盖所有可能的结果，只要其中有一次和 `target` 完全相同，就返回 `True`。

- **时间/空间复杂度**：  
  - 每一次旋转需要遍历整个 `n×n` 的矩阵，时间是 `O(n²)`。最多转四次，所以总时间是 `4·O(n²) = O(n²)`（常数 4 在复杂度分析里可以忽略）。  
  - 为了实现旋转我们会新建一个同样大小的矩阵来保存转后的结果，这需要额外的 `n²` 个格子，空间复杂度是 `O(n²)`。  
  - 用大白话说，**时间复杂度 O(n²)** 就是“随着矩阵边长 n 增大，耗时大约会跟 n 的平方成正比”。**空间 O(n²)** 就是“我们额外用了和原矩阵一样多的存储空间”。

#### 代码（Python）

```python
from typing import List

def rotate(mat: List[List[int]]) -> List[List[int]]:
    """顺时针旋转 90 度，返回一个新矩阵。"""
    n = len(mat)
    # 新建一个 n×n 的空矩阵
    new = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            # 位置映射公式：new[i][j] = mat[n-1-j][i]
            new[i][j] = mat[n - 1 - j][i]
    return new

def findRotation(mat: List[List[int]], target: List[List[int]]) -> bool:
    """暴力检查 0、90、180、270 度四种情况是否能匹配 target。"""
    for _ in range(4):                     # 最多尝试四次
        if mat == target:                  # 逐元素比较（list 自带的 == 已经做到这点）
            return True
        mat = rotate(mat)                  # 旋转 90 度，准备下一轮比较
    return False                           # 四次都不相等，返回 False
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 只要遍历矩阵四次，每次 `n²`，常数 4 不算在大 O 里。  
- **空间复杂度**：`O(n²)` — 每次旋转都新建了一个同样大小的矩阵来保存结果。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**时间已经是最优的**（只能遍历矩阵，至少要 `O(n²)`），真正可以改进的地方是**空间**。  
在暴力实现里我们每次旋转都新建一个矩阵，这会占用额外的 `n²` 空间。其实矩阵的原地旋转（不申请新数组）只需要 `O(1)` 的额外空间。

**原地旋转的核心技巧**：

1. **先转置**（把行和列互换），相当于把矩阵沿主对角线翻转。  
   - 位置映射：`mat[i][j] ↔ mat[j][i]`，只需要遍历上三角（`i < j`）即可，避免重复交换。  
2. **再把每一行反转**（左右镜像），相当于把每行的元素顺序倒过来。  

这两步组合起来正好等价于顺时针旋转 90 度。  
- **类比**：想象一张纸先把横竖坐标互换（转置），再把纸左右翻转，就得到顺时针旋转的效果。

我们仍然最多尝试四次（因为四次回到原点），但每次旋转只在原矩阵上就地完成，省掉了额外的 `n²` 空间。

#### 代码（Python）

```python
from typing import List

def rotate_in_place(mat: List[List[int]]) -> None:
    """在原矩阵上就地完成顺时针 90 度旋转，返回 None（直接修改 mat）。"""
    n = len(mat)
    # 1) 转置：交换 mat[i][j] 与 mat[j][i]（只遍历上三角）
    for i in range(n):
        for j in range(i + 1, n):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]   # 交换

    # 2) 反转每一行：把每行的元素左右翻转
    for i in range(n):
        left, right = 0, n - 1
        while left < right:
            mat[i][left], mat[i][right] = mat[i][right], mat[i][left]
            left += 1
            right -= 1

def findRotation(mat: List[List[int]], target: List[List[int]]) -> bool:
    """使用原地旋转，空间 O(1) 检查四种可能。"""
    for _ in range(4):
        if mat == target:
            return True
        rotate_in_place(mat)      # 直接在 mat 上旋转
    return False
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每次原地旋转仍然要遍历整个矩阵两遍（一次转置，一次行反转），四次总共仍是常数倍的 `n²`。  
- **空间复杂度**：`O(1)` — 只用了若干个临时变量（`i, j, left, right`），不随矩阵大小增长。

---

## 心得

- **核心技巧**：原地矩阵旋转（转置 + 行反转）  
- **适用的题型**：  
  1. “判断矩阵是否相等（或相似）”的题目，例如 `Rotate Image`（LeetCode 48）。  
  2. “把图像顺时针/逆时针旋转”类的几何变换题。  
  3. “矩阵对称性”检查，如是否为旋转对称矩阵。  
- **一句话总结**：**只要记住“转置 + 行翻转 = 顺时针 90°”，就能在 O(1) 额外空间内完成矩阵的任意次 90° 旋转**。

---

## 反思

- **第一反应**：先想“把矩阵每次转 90°，比较四次”，也就是暴力枚举。  
- **最容易踩的坑**：  
  - **边界条件**：`n = 1` 时矩阵只有一个元素，四次旋转仍是自己，代码必须能正确处理。  
  - **原地旋转的实现细节**：转置时只能遍历上三角（`i < j`），否则会把已经交换好的元素再换回来。  
  - **比较时的等价性**：直接使用 `mat == target` 在 Python 中会逐行、逐列比较，确保两者是同构的列表。  
- **下次遇到同类题**：第一步先**确定最多需要检查几种状态**（本题是 4 种），随后思考**是否可以在原地完成状态转变**，如果可以就选原地算法，省空间。