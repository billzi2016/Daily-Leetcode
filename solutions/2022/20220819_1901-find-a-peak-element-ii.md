# #1901. 寻找峰值元素 II / Find a Peak Element II

> 难度：中等 · 标签：Array、Binary Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-a-peak-element-ii/)

---

## 题目（英文原版）

**Description**

A peak element in a 2D grid is an element that is strictly greater than all of its adjacent neighbors to the left, right, top, and bottom.
Given a 0-indexed m x n matrix mat where no two adjacent cells are equal, find any peak element mat[i][j] and return the length 2 array [i,j].
You may assume that the entire matrix is surrounded by an outer perimeter with the value -1 in each cell.
You must write an algorithm that runs in O(m log(n)) or O(n log(m)) time.

**Examples**

**Example 1:**

```
Input: mat = [[1,4],[3,2]]
Output: [0,1]
Explanation: Both 3 and 4 are peak elements so [1,0] and [0,1] are both acceptable answers.
```

**Example 2:**

```
Input: mat = [[10,20,15],[21,30,14],[7,16,32]]
Output: [1,1]
Explanation: Both 30 and 32 are peak elements so [1,1] and [2,2] are both acceptable answers.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 500
- 1 <= mat[i][j] <= 105
- No two adjacent cells are equal.

---

## 题目（中文翻译）

一个峰值元素（peak element）在二维网格（2D grid）中指的是它严格大于左、右、上、下四个相邻邻居的元素。  
给定一个下标从 0 开始的 `m × n` 矩阵 `mat`，且任意两个相邻单元格的值都不相等，找出任意一个峰值元素 `mat[i][j]` 并返回长度为 2 的数组 `[i, j]`。  
你可以假设整个矩阵的外围被一圈值为 `-1` 的外部边界（outer perimeter）包围。  
要求你设计的算法时间复杂度为 `O(m log n)` 或 `O(n log m)`。

**示例 1**  
**示例 2**  
**约束条件**

```text
示例 1:
Input: mat = [[1,4],[3,2]]
Output: [0,1]
Explanation: 3 和 4 都是峰值元素，因此 [1,0] 和 [0,1] 都是可接受的答案。

示例 2:
Input: mat = [[10,20,15],[21,30,14],[7,16,32]]
Output: [1,1]
Explanation: 30 和 32 都是峰值元素，因此 [1,1] 和 [2,2] 都是可接受的答案。
```

**约束条件**
- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 500`
- `1 <= mat[i][j] <= 10^5`
- 任意两个相邻单元格的值不相等。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把矩阵的每一个格子都检查一遍，判断它是否比上、下、左、右四个相邻格子都大。如果是，就找到了一个**峰值**，直接返回它的坐标。

- **用到的数据结构**：普通的二维列表 `mat`（相当于一张电子表格），我们只需要遍历它的行和列。  
- **生活化类比**：把矩阵想象成一块高低起伏的地形图，每个格子是一个小山丘。我们把手伸向每个格子，看看它是否是四周都比它低的小山顶。  
- **正确性**：因为题目要求返回**任意**一个峰值，只要遍历到的格子满足“比上下左右都高”，就一定是合法答案。遍历完整个矩阵后，若存在峰值（题目保证一定有），必然能找到。  

#### 代码（Python）

```python
from typing import List

def findPeakElement(mat: List[List[int]]) -> List[int]:
    m, n = len(mat), len(mat[0])          # 行数、列数
    # 四个方向的偏移量，方便统一检查
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(m):
        for j in range(n):
            cur = mat[i][j]
            is_peak = True                # 假设当前格子是峰值
            for dx, dy in dirs:           # 检查四个相邻格子
                x, y = i + dx, j + dy
                # 如果相邻格子在矩阵内部且不小于当前格子，则不是峰值
                if 0 <= x < m and 0 <= y < n and mat[x][y] >= cur:
                    is_peak = False
                    break
            if is_peak:                    # 找到第一个峰值直接返回
                return [i, j]

    # 题目保证一定有峰值，理论上不会走到这里
    return [-1, -1]
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 我们对矩阵的每个格子都检查一次（`m·n` 次），每次检查至多 4 个相邻格子，常数级别的工作，整体就是“矩阵大小乘以一个常数”，即 `O(m·n)`。  
  - 用大白话说，就是如果矩阵有 1000×1000 = 1 000 000 个格子，程序大约会跑 1 000 000 次检查。

- **空间复杂度**：`O(1)`  
  - 只用了几个额外的变量（行列计数、方向数组），和矩阵本身的大小无关，算是常数空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都遍历整张矩阵**。我们需要把搜索范围快速缩小。观察题目：

- 相邻格子的值**不相等**，这保证了在任意方向上如果向更大的方向走，必然可以继续上升，最终会到达一个峰值（类似山坡的最高点）。
- 题目要求 `O(m log n)` 或 `O(n log m)`，提示我们可以使用 **二分搜索** 的思想，把搜索维度压到对数级。

下面以 **列方向的二分** 为例（如果列比行多，时间复杂度就是 `O(m log n)`；如果行比列多，只需要把行、列互换即可）：

1. **选取中间列** `mid = n // 2`。  
2. 在这列中**找到最大值所在的行** `max_row`（遍历该列 O(m)）。  
3. 比较该最大值 `mat[max_row][mid]` 与它的左右相邻格子（如果存在）：

   - 如果它大于左、右两侧的邻居，则它已经是**峰值**（因为左、右不比它高，上下已经不是更大的方向，因为我们已经在该列的最大值了）。
   - 如果左侧邻居更大，则说明**峰值一定在左半边**（因为左侧更高，向左继续上升必然能找到峰值），我们把搜索区间缩小到左半边 **包括** `mid` 列（因为左半边的最大值可能正好在 `mid` 列）。
   - 同理，如果右侧邻居更大，则搜索右半边 **包括** `mid` 列。

4. 重复上述步骤，直到搜索区间只剩一列，返回对应的峰值坐标。

这就是**“在列上做二分，行上线性找最大”**的思路。每一次二分都只遍历 **一列**（O(m)），二分的深度是 `log n`，所以总时间 `O(m log n)`。

> **为什么一定能找到峰值？**  
> 设想我们在某一步把搜索区间限制到左半边，因为左侧相邻格子比当前格子高。左半边的矩阵仍然满足“相邻格子不相等”。在左半边继续二分，最终会收敛到一个格子，它要么是左半边的局部最大（即峰值），要么左侧已经没有更高的格子了（因为已经到达最左列），这时它必然满足四周比它小的条件。

#### 代码（Python）

```python
from typing import List

def findPeakElement(mat: List[List[int]]) -> List[int]:
    m, n = len(mat), len(mat[0])

    # 为了让代码更通用，写一个二分函数，参数可以是按列或按行二分
    def search(left: int, right: int) -> List[int]:
        """
        在列区间 [left, right]（左闭右闭）中二分查找峰值。
        每一次取中间列 mid，在线性扫描该列得到最高的行 max_row。
        """
        while left <= right:
            mid = (left + right) // 2                # 中间列
            # 找到 mid 列中最大的那个元素所在的行
            max_row = 0
            for i in range(1, m):
                if mat[i][mid] > mat[max_row][mid]:
                    max_row = i

            # 取左、右相邻列的值，若越界则视为 -1（题目外层围着 -1）
            left_val  = mat[max_row][mid - 1] if mid - 1 >= 0 else -1
            right_val = mat[max_row][mid + 1] if mid + 1 < n else -1
            cur_val   = mat[max_row][mid]

            # 判断是否为峰值
            if cur_val > left_val and cur_val > right_val:
                return [max_row, mid]                # 找到峰值直接返回

            # 若左侧更大，说明峰值在左半边（包括 mid 列）
            if left_val > cur_val:
                right = mid - 1
            else:   # 右侧更大
                left = mid + 1

        # 理论上不会走到这里，因为一定会在循环中返回
        return [-1, -1]

    # 选择在列上二分（若 n < m，可改为在行上二分，只需把矩阵转置或写另一套）
    return search(0, n - 1)
```

> **代码要点注释**  
> - `left_val`、`right_val` 用 `-1` 填充越界情况，正好对应题目外层围着 `-1` 的假设。  
> - `while left <= right` 循环保证二分能收敛；每一次循环我们只遍历 **一列**（`for i in range(1, m)`），所以时间是 `O(m)`。  
> - `max_row` 的寻找是线性的，但只在当前列进行，不会遍历整张矩阵。

#### 复杂度  

- **时间复杂度**：`O(m log n)`  
  - 每一次二分我们只扫描 **一列**，花费 `O(m)`。二分的深度是 `log₂ n`（把列数不断折半），于是总时间是 `O(m·log n)`。  
  - 用通俗的话说：如果矩阵是 500 行 × 500 列，`log₂ 500 ≈ 9`，我们只需要大约 `500 × 9 = 4500` 次元素比较，远远小于暴力的 250 000 次。

- **空间复杂度**：`O(1)`  
  - 只使用了常数个额外变量（`left, right, mid, max_row` 等），不随矩阵大小增长。

---

## 心得

- **核心技巧**：在满足“相邻不相等”且四周被 `-1` 包围的二维数组中，可以利用 **二分搜索** 把搜索空间指数级压缩。关键在于每次二分只在线性维度（行或列）上寻找局部最大，然后依据左右（或上下）邻居的大小决定搜索方向。  
- **适用的题型**：  
  1. **二维峰值**（本题）  
  2. **单调矩阵的最小/最大查找**（如 LeetCode 240. Search a 2D Matrix II）  
  3. **分治求解的矩阵分割问题**（如寻找矩阵中满足某种单调性质的点）  
- **一句话总结**：把矩阵“一列一列”当作“一维山坡”，在每列找最高点，然后用左右比较决定向哪边继续爬坡——这就是“二分 + 局部最大” 的解题钥匙。

---

## 反思

- **第一反应**：看到“峰值”，自然想到“遍历全部、逐个比较”，于是写出暴力解。  
- **最容易踩的坑**：  
  - 忘记处理边界列的情况（左/右越界时应视为 `-1`）。  
  - 误以为只要在中间列的最大值比左右都大就一定是峰值，忽略了上下方向的比较；其实因为我们已经在该列的**全局最大**，所以上下不可能更大。  
  - 递归或循环的结束条件写错，导致无限循环或遗漏最后一列。  
- **下次遇到同类题**：第一步先思考“能否把二维问题降维到一维”，再找出**单调/局部极值**的性质，利用二分或分治把搜索空间快速缩小。这样往往能把 `O(m·n)` 降到 `O(m log n)` 或 `O(n log m)`。