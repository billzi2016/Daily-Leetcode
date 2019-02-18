# #304. 二维区域和查询 - 不可变 / Range Sum Query 2D - Immutable

> 难度：中等 · 标签：Array、Design、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/range-sum-query-2d-immutable/)

---

## 题目（英文原版）

**Description**

Given a 2D matrix matrix, handle multiple queries of the following type:
Implement the NumMatrix class:
You must design an algorithm where sumRegion works on O(1) time complexity.

**Examples**

**Example 1:**

```
Input
["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
Output
[null, 8, 11, 12]

Explanation
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- -104 <= matrix[i][j] <= 104
- 0 <= row1 <= row2 < m
- 0 <= col1 <= col2 < n
- At most 104 calls will be made to sumRegion.

---

## 题目（中文翻译）

给定一个二维矩阵 **matrix**，需要处理多次以下类型的查询：

实现 **NumMatrix** 类：

- 设计一种算法，使得 `sumRegion` 的时间复杂度为 **O(1)**。

**Example 1**

**Constraints**

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 200`
- `-10^4 <= matrix[i][j] <= 10^4`
- `0 <= row1 <= row2 < m`
- `0 <= col1 <= col2 < n`
- 最多会调用 `sumRegion` `10^4` 次

**示例：**

```json
Input
["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]

Output
[null, 8, 11, 12]
```

**Explanation**

```java
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2],
                                     [5, 6, 3, 2, 1],
                                     [1, 2, 0, 1, 5],
                                     [4, 1, 0, 1, 7],
                                     [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // 返回 8（即红色矩形的和）
numMatrix.sumRegion(1, 1, 2, 2); // 返回 11（即绿色矩形的和）
numMatrix.sumRegion(1, 2, 2, 4); // 返回 12（即蓝色矩形的和）
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是**每次查询**时，遍历矩阵中指定的子矩形的所有格子，把它们的值相加后返回。  
- 用到的数据结构只有原始的二维列表 `matrix`，就像一本普通的表格，想要查某个区域的总和只能一个格子一个格子地数。  
- 这种方法一定能得到正确答案，因为我们把要求的所有数都加了进去，没有遗漏也没有多加。  

> **为什么正确**  
> 题目只要求返回指定左上角 `(row1, col1)` 与右下角 `(row2, col2)` 所围成的矩形内所有元素的和。暴力遍历恰好把这些位置全部遍历一遍并相加，等价于数学定义的求和。

#### 代码（Python）

```python
class NumMatrix:
    def __init__(self, matrix):
        """
        直接把矩阵保存下来，后面查询时直接使用。
        """
        self.matrix = matrix
        self.m = len(matrix)          # 行数
        self.n = len(matrix[0]) if matrix else 0   # 列数

    def sumRegion(self, row1, col1, row2, col2):
        """
        暴力遍历子矩形的每一个元素并求和。
        """
        total = 0
        for r in range(row1, row2 + 1):          # 行从 row1 到 row2（含）
            for c in range(col1, col2 + 1):      # 列从 col1 到 col2（含）
                total += self.matrix[r][c]       # 把当前格子的值加进去
        return total
```

#### 复杂度

- **时间复杂度**：`O((row2‑row1+1) * (col2‑col1+1))`  
  直白的解释就是：如果查询的矩形有 `a` 行、`b` 列，就要看 `a*b` 个格子。最坏情况下（查询整个矩阵），就是 `O(m·n)`，相当于“遍历整张表”。  
- **空间复杂度**：`O(1)`（不计保存原矩阵的空间）  
  只用了几个临时变量 `total, r, c`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次查询都要 **重新遍历** 那片区域。若有上万次查询，这种重复工作会非常浪费。  
我们可以把“遍历一次”这件事提前到 **构造函数** 里完成，只要在查询时能够 **直接算出** 子矩形的和，就能把查询时间降到 `O(1)`。

实现思路——**二维前缀和（2‑D Prefix Sum）**，也叫**累计和矩阵**。  

1. **构造累计和矩阵 `pre`**  
   - `pre[i][j]` 表示原矩阵左上角 `(0,0)` 到 `(i‑1, j‑1)`（不含 `i,j`）所有元素的总和。  
   - 这相当于把原矩阵的每一行、每一列都先“累加”，就像把一本字典的每一页都把前面的页码加进去，查询时只需要看几页的累计值。  
   - 递推公式（图示）：

```
pre[i][j] = pre[i-1][j]          # 上面那一行的累计
          + pre[i][j-1]          # 左边那一列的累计
          - pre[i-1][j-1]        # 左上角重复加了两次，要减掉
          + matrix[i-1][j-1]     # 加上本格子的原始值
```

   - 为了避免边界检查，把 `pre` 的大小设为 `(m+1) × (n+1)`，第一行第一列全部为 `0`，这样 `i-1`、`j-1` 永远合法。

2. **利用累计和求子矩形和**  
   - 想要左上 `(row1, col1)`、右下 `(row2, col2)` 的矩形和，只需要四块累计值相减相加：

```
sum = pre[row2+1][col2+1]          # 整个大矩形的累计
    - pre[row1][col2+1]            # 去掉上方多余的部分
    - pre[row2+1][col1]            # 去掉左侧多余的部分
    + pre[row1][col1]              # 左上角被减了两次，补回来
```

   - 这一步只用了常数次数组访问，**时间是 O(1)**。

#### 代码（Python）

```python
class NumMatrix:
    def __init__(self, matrix):
        """
        预处理：构造二维前缀和矩阵 pre。
        pre 的尺寸比原矩阵多一行一列，第一行第一列全部为 0，方便边界计算。
        """
        if not matrix or not matrix[0]:
            # 空矩阵的情况，直接记为 None，后面查询直接返回 0
            self.pre = None
            return

        m, n = len(matrix), len(matrix[0])
        # 创建 (m+1) x (n+1) 的全 0 矩阵
        self.pre = [[0] * (n + 1) for _ in range(m + 1)]

        # 填充 pre，按照递推公式
        for i in range(1, m + 1):          # i 对应原矩阵的第 i-1 行
            row_sum = 0                    # 用来累计当前行的前缀和，省去一次列的访问
            for j in range(1, n + 1):      # j 对应原矩阵的第 j-1 列
                row_sum += matrix[i - 1][j - 1]          # 当前行从左到右累加
                self.pre[i][j] = self.pre[i - 1][j] + row_sum
                # 解释：pre[i-1][j] 为上一行同列的累计，row_sum 为本行到 j 列的累计

    def sumRegion(self, row1, col1, row2, col2):
        """
        使用前缀和矩阵在 O(1) 时间内返回子矩形的元素和。
        """
        if self.pre is None:
            return 0

        # 注意坐标要向右下移动一格，因为 pre 多了一层 0 边界
        r1, c1, r2, c2 = row1 + 1, col1 + 1, row2 + 1, col2 + 1

        total = (self.pre[r2][c2]          # 大矩形的累计和
                 - self.pre[r1 - 1][c2]    # 去掉上方多余的部分
                 - self.pre[r2][c1 - 1]    # 去掉左侧多余的部分
                 + self.pre[r1 - 1][c1 - 1])  # 补回左上角被减两次的部分
        return total
```

#### 复杂度

- **时间复杂度**  
  - 构造阶段：`O(m·n)`，遍历整个矩阵一次把前缀和算完。  
  - 查询 `sumRegion`：`O(1)`，只做了几次数组下标访问和加减运算。  
  与暴力解相比，查询从 **线性** 降到了 **常数**，在大量查询时优势非常明显。  

- **空间复杂度**：`O(m·n)`  
  需要额外存一张同样规模（略大一行一列）的累计和矩阵。可以把它想象成在原表格旁边再贴了一张“每行每列的累计和”表，查询时直接查表。

---

## 心得

- **核心技巧**：二维前缀和（累计和矩阵），把一次遍历的工作提前到构造阶段，使后续查询成为常数时间操作。  
- **适用题型**  
  1. “Range Sum Query 2D – Immutable”（本题）  
  2. “Range Sum Query – Immutable” 的一维版本（前缀和）  
  3. “Submatrix Sum Equals K” 中需要快速求子矩阵和的场景（也会用到前缀和）  
- **一句话总结**：**把“把所有数加起来”这件事提前做一次，以后只要几次减法就能直接得到答案**。

---

## 反思

- **第一反应**：看到“多次查询子矩形和”，立刻想到“遍历每次的子矩形”。这就是暴力解。  
- **最容易踩的坑**  
  - **边界处理**：前缀和矩阵多出一行一列，查询时坐标要加 1（或减 1）否则会越界或算错。  
  - **负数**：矩阵里可能有负数，不能把 `max`、`min` 之类的优化思路套进去，前缀和对负数同样适用。  
  - **空矩阵**：虽然题目保证至少有 1 行 1 列，但在写通用代码时仍需防止 `matrix == []` 的情况。  
- **下次遇到同类题**：第一步先思考“能否把一次性计算的工作搬到构造函数里”，如果答案是“可以”，就尝试构建 **前缀和**（或 **单调栈**、**哈希表** 等适合的结构）来实现 `O(1)` 或 `O(log n)` 的查询。