# #2319. 判断矩阵是否为 X 矩阵 / Check if Matrix Is X-Matrix

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/check-if-matrix-is-x-matrix/)

---

## 题目（英文原版）

**Description**

A square matrix is said to be an X-Matrix if both of the following conditions hold:
Given a 2D integer array grid of size n x n representing a square matrix, return true if grid is an X-Matrix. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: grid = [[2,0,0,1],[0,3,1,0],[0,5,2,0],[4,0,0,2]]
Output: true
Explanation: Refer to the diagram above. 
An X-Matrix should have the green elements (diagonals) be non-zero and the red elements be 0.
Thus, grid is an X-Matrix.
```

**Example 2:**

```
Input: grid = [[5,7,0],[0,3,1],[0,5,0]]
Output: false
Explanation: Refer to the diagram above.
An X-Matrix should have the green elements (diagonals) be non-zero and the red elements be 0.
Thus, grid is not an X-Matrix.
```

**Constraints**

- n == grid.length == grid[i].length
- 3 <= n <= 100
- 0 <= grid[i][j] <= 105

---

## 题目（中文翻译）

给定一个大小为 `n x n` 的二维整数数组 `grid`，它表示一个方阵（square matrix）。如果该方阵满足以下 **两个** 条件，则称其为 **X 矩阵**（X-Matrix）：

1. 主对角线（从左上到右下）和副对角线（从右上到左下）上的所有元素均为非零（non‑zero）。
2. 其余位置的元素全部为零（0）。

如果 `grid` 是 X 矩阵，返回 `true`；否则返回 `false`。

---

## 示例

### 示例 1  
**输入**  
```text
grid = [[2,0,0,1],
        [0,3,1,0],
        [0,5,2,0],
        [4,0,0,2]]
```  
**输出**  
```text
true
```  
**解释**  
如上图所示，绿色的元素（即两条对角线）均为非零，红色的元素均为 `0`，因此 `grid` 是一个 X 矩阵。

### 示例 2  
**输入**  
```text
grid = [[5,7,0],
        [0,3,1],
        [0,5,0]]
```  
**输出**  
```text
false
```  
**解释**  
如上图所示，绿色的元素（两条对角线）中存在为 `0` 的情况，或者红色的元素不全为 `0`，因此 `grid` 不是 X 矩阵。

---

## 约束条件

- `n == grid.length == grid[i].length`
- `3 <= n <= 100`
- `0 <= grid[i][j] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把矩阵的每个格子都检查一遍，判断它是否满足 **X‑矩阵** 的两个要求：

1. **对角线上的元素必须非零**。  
   - 主对角线：行号 `i` 与列号 `j` 相同，即 `i == j`。  
   - 副对角线：行号 `i` 加列号 `j` 等于 `n‑1`，即 `i == n‑1‑j`。  
   （把矩阵想成一本字典，行号是“章节”，列号是“页码”。只有当章节号等于页码，或者章节号 + 页码恰好等于最后一页的前一页时，这个位置才是“对角线”。）

2. **非对角线的位置必须全是 0**。  

只要遍历所有 `n × n` 个格子，按照上面的规则逐个判断，就能得到答案。  

> **为什么正确**  
> - 对每个格子都做了检查，既不漏掉对角线，也不漏掉非对角线。只要全部满足条件，整个矩阵必然是 X‑矩阵；只要有任意一个格子不满足，答案就一定是 `false`。

> **时间/空间分析**  
> - 我们要遍历每一行的每一列，一共 `n²` 次检查，时间随矩阵大小呈二次增长，用 **O(n²)** 表示。  
>   > 大白话：如果矩阵是 10×10，需要检查 100 次；如果是 100×100，需要检查 10,000 次，检查次数会快速变多。  
> - 只用到几个整型变量（行号、列号、矩阵大小），不需要额外的数组或列表，空间是 **O(1)**，即常数级别。  

#### 代码（Python）

```python
def checkXMatrix(grid):
    """
    判断一个 n×n 的矩阵是否为 X‑Matrix。
    :param grid: List[List[int]]，方阵
    :return: bool
    """
    n = len(grid)                       # 矩阵的维度
    for i in range(n):                  # 遍历每一行
        for j in range(n):              # 遍历每一列
            # 判断 (i, j) 是否在对角线上
            on_main_diag = i == j
            on_anti_diag = i == n - 1 - j
            if on_main_diag or on_anti_diag:
                # 对角线元素必须非零
                if grid[i][j] == 0:
                    return False       # 只要有一个不满足，直接返回 False
            else:
                # 非对角线元素必须为零
                if grid[i][j] != 0:
                    return False
    return True                         # 全部检查完都满足条件
```

#### 复杂度

- **时间复杂度：O(n²)** — 需要检查矩阵中的每一个格子，格子总数正好是 `n` 的平方。  
- **空间复杂度：O(1)** — 只用了常数个变量（`n, i, j`），不随矩阵大小增长。

---

### 2. 最优解

#### 思路  
其实在本题中，**暴力遍历已经是最优**，因为我们必须至少看一次每个格子才能确认它是否满足要求。  
唯一可以改进的地方是 **提前结束**：一旦发现不符合条件的格子，就不必继续遍历剩下的格子，直接返回 `False`。这在实际运行时可以省去很多不必要的比较，尤其是矩阵很大且错误出现在前面时。

核心思路仍然是：

1. 对每个位置 `(i, j)` 判断它是否在对角线上（`i == j` 或 `i == n‑1‑j`）。  
2. 根据是否在对角线上检查值是否为 0 / 非 0。  
3. **一发现错误立即返回**。

下面的代码把 “提前结束” 写得更明显，并加了少量的变量让逻辑更清晰。

#### 代码（Python）

```python
def checkXMatrix(grid):
    n = len(grid)
    # 逐行检查
    for i in range(n):
        # 逐列检查
        for j in range(n):
            # 是否在任一对角线上
            on_diag = (i == j) or (i == n - 1 - j)

            if on_diag:
                # 对角线必须是非零
                if grid[i][j] == 0:
                    return False          # 立即返回，省掉后面的循环
            else:
                # 非对角线必须是零
                if grid[i][j] != 0:
                    return False
    # 所有格子都满足要求
    return True
```

#### 复杂度

- **时间复杂度：O(n²)** — 最坏情况下仍需检查所有格子；但**平均**会更快，因为一旦出现错误就会提前退出。  
- **空间复杂度：O(1)** — 只使用了常数个辅助变量。

---

## 心得

- **核心技巧**：**坐标映射**（通过行列下标判断是否在主/副对角线） + **一次遍历 + 早停**。  
- **适用的题型**：  
  1. 判断矩阵是否满足某种“位置模式”的题目（如对称矩阵、棋盘格等）。  
  2. 检查二维数组中是否满足“行列特定条件”的题目（如全 0 行、全 1 列等）。  
- **解题钥匙**：**把“是否在某集合”抽象为下标关系**，然后逐个验证即可。

## 反思

- **第一反应**：看到“对角线”和“非对角线”的描述，马上想到用下标 `i, j` 的等式来区分两类格子。  
- **最容易踩的坑**：  
  - 忘记 **副对角线** 的判定公式 `i == n - 1 - j`（只写了主对角线会导致错误）。  
  - 对 **边界值**（如 `n = 3`）的格子不仔细检查，尤其是中心格子同时位于两条对角线，只要它是非零即可。  
- **下次思路**：遇到类似“矩阵中某些位置要满足特定数值，其他位置要满足另一数值”的题目，第一步就**写出位置判定的数学表达式**，随后在一次遍历中完成全部检查并**利用提前退出**提升效率。