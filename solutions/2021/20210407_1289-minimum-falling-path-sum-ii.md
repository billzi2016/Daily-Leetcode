# #1289. 最小下降路径和 II / Minimum Falling Path Sum II

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-falling-path-sum-ii/)

---

## 题目（英文原版）

**Description**

Given an n x n integer matrix grid, return the minimum sum of a falling path with non-zero shifts.
A falling path with non-zero shifts is a choice of exactly one element from each row of grid such that no two elements chosen in adjacent rows are in the same column.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,3],[4,5,6],[7,8,9]]
Output: 13
Explanation: 
The possible falling paths are:
[1,5,9], [1,5,7], [1,6,7], [1,6,8],
[2,4,8], [2,4,9], [2,6,7], [2,6,8],
[3,4,8], [3,4,9], [3,5,7], [3,5,9]
The falling path with the smallest sum is [1,5,7], so the answer is 13.
```

**Example 2:**

```
Input: grid = [[7]]
Output: 7
```

**Constraints**

- n == grid.length == grid[i].length
- 1 <= n <= 200
- -99 <= grid[i][j] <= 99

---

## 题目（中文翻译）

给定一个 **n × n** 的整数矩阵 **grid**，返回满足 **非零位移（non-zero shifts）** 条件的 **下降路径（falling path）** 的最小和。  
**非零位移的下降路径** 是指从矩阵的每一行恰好选取一个元素，且相邻两行选取的元素所在的列不同。

**示例 1**  
**输入**: `grid = [[1,2,3],[4,5,6],[7,8,9]]`  
**输出**: `13`  
**解释**:  
所有可能的下降路径如下所示：  
```
[1,5,9], [1,5,7], [1,6,7], [1,6,8],
[2,4,8], [2,4,9], [2,6,7], [2,6,8],
[3,4,8], [3,4,9], [3,5,7], [3,5,9]
```  
其中和最小的下降路径是 **[1,5,7]**，因此答案为 **13**。

**示例 2**  
**输入**: `grid = [[7]]`  
**输出**: `7`

**约束条件**  
- `n == grid.length == grid[i].length`  
- `1 <= n <= 200`  
- `-99 <= grid[i][j] <= 99`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从第一行开始，依次往下选，每选一行就把当前格子的值加到路径和里**。  
在第 `i` 行选了第 `j` 列以后，下一行（第 `i+1` 行）就只能选 **除第 `j` 列之外的任意一列**，因为相邻两行不能在同一列。  

如果把每一行看成一层楼梯，每层楼有 `n` 个格子，走一条“下坠路径”就像在楼梯上走路，**每一步都要换到别的柱子上**。  
我们可以把每一层的选择记在一个二维数组 `dp[i][j]` 中，表示**走到第 `i` 行第 `j` 列时，已经得到的最小路径和**。  

递推公式：

```
dp[0][j] = grid[0][j]                              # 第一行只能选自己
dp[i][j] = grid[i][j] + min{ dp[i-1][k] | k ≠ j }   # 只能从上一行的不同列转来
```

把所有 `dp[n-1][j]`（最后一行的每一列）取最小值，就是答案。

> **为什么这个方法一定能得到正确答案？**  
> 动态规划的核心是「子问题最优解能推出整体最优解」。这里的子问题是「走到第 `i` 行第 `j` 列的最小路径和」，它只依赖于第 `i-1` 行的状态，且我们遍历了所有合法的前一步（所有 `k ≠ j`），因此一定能找到真正的最小值。

**时间/空间复杂度**  
- 对每一行的每一列 (`n²` 次) 都要遍历上一行的所有除自身外的列 (`n-1` 次)，所以总共是 **`O(n³)`**。  
  大白话：如果 `n=200`，大概要算 200 × 200 × 199 ≈ 8 × 10⁶ 次，这在 Python 里已经有点慢了。  
- 需要保存整张 `dp` 表，大小也是 `n × n`，即 **`O(n²)`** 的额外空间。

#### 代码（Python）

```python
from typing import List

def minFallingPathSum_bruteforce(grid: List[List[int]]) -> int:
    n = len(grid)
    # dp[i][j] 表示走到第 i 行第 j 列的最小路径和
    dp = [[float('inf')] * n for _ in range(n)]

    # 初始化第一行
    for j in range(n):
        dp[0][j] = grid[0][j]          # 只选自己的值

    # 逐行填表
    for i in range(1, n):
        for j in range(n):             # 当前行的列
            # 从上一行的所有不同列转来，取最小值
            min_prev = float('inf')
            for k in range(n):
                if k == j:            # 不能和上一行同列
                    continue
                if dp[i-1][k] < min_prev:
                    min_prev = dp[i-1][k]
            dp[i][j] = grid[i][j] + min_prev

    # 最后一行的最小值就是答案
    return min(dp[n-1])
```

#### 复杂度  

- **时间复杂度：`O(n³)`**  
  - “立方”来源于三层循环：行、当前列、上一行的所有列。  
  - 对于 `n=200`，约 8 百万次比较，已超出题目对 Hard 级别的期望。

- **空间复杂度：`O(n²)`**  
  - 需要保存整个 `dp` 表（`n × n` 个数），相当于一个 `n×n` 的棋盘大小。

---

### 2. 最优解

#### 思路  

从上面的暴力 DP 可以看到，**瓶颈在于每次求 `min{ dp[i-1][k] | k ≠ j }`**，我们要遍历上一行的 `n-1` 个列。  
如果我们能在 **`O(1)`** 时间内得到「上一行除了第 `j` 列之外的最小值」，整体就能降到 `O(n²)`。

**关键观察**  
- 对于一行的所有 `dp` 值，**只需要记住最小的两个**：
  - `first_min`：最小值所在的列 `first_idx`。
  - `second_min`：第二小的值（列不一定不同）。
- 当我们要算 `dp[i][j]` 时：
  - 如果 `j` **不等于** `first_idx`（上一行的最小值所在列），则直接使用 `first_min`。
  - 否则（`j` 与上一行的最小列相同），只能使用 `second_min`，因为必须换列。

这样每一行只需一次遍历（`O(n)`）就能得到 `first_min` 与 `second_min`，随后再一次遍历来计算当前行的 `dp`（同样 `O(n)`），总体是 **`O(n²)`**。

**类比**  
把每一行想成「超市的收银台」——我们想要找最便宜的商品，但有时买家不允许选同一个品牌（列）。只要记住最便宜的两种商品（最小、次小），就能在不看完整个列表的情况下快速决定该买哪一种。

**算法步骤**  

1. **初始化**：`dp = grid[0]`（第一行本身就是路径和）。  
2. **遍历每一行**（从第 2 行到第 n 行）  
   - 在 `dp` 中找到 `first_min`、`first_idx`、`second_min`。  
   - 创建新数组 `new_dp`，对每个列 `j`：  
     - `prev = first_min` 如果 `j != first_idx`，否则 `prev = second_min`。  
     - `new_dp[j] = grid[i][j] + prev`。  
   - 用 `new_dp` 替换 `dp`，继续下一行。  
3. 最后返回 `dp` 中的最小值。

**复杂度分析**  
- 每行我们只遍历两次（一次找最小两值，一次算新 `dp`），都是 `O(n)`，共 `n` 行 → **`O(n²)`**。  
- 只用两条长度为 `n` 的一维数组，**`O(n)`** 额外空间（可以直接在原数组上原地更新）。

#### 代码（Python）

```python
from typing import List

def minFallingPathSum(grid: List[List[int]]) -> int:
    """
    动态规划 + 维护上一行的最小、次小值
    时间 O(n²)  空间 O(n)
    """
    n = len(grid)
    # dp 保存到当前行为止的最小路径和（第一行为起点）
    dp = grid[0][:]                     # 复制一份，防止修改原矩阵

    for i in range(1, n):
        # 1️⃣ 找到上一行的最小值和次小值
        first_min = second_min = float('inf')
        first_idx = -1
        for j, val in enumerate(dp):
            if val < first_min:
                second_min = first_min   # 旧的最小变成次小
                first_min = val
                first_idx = j
            elif val < second_min:
                second_min = val

        # 2️⃣ 依据最小/次小值计算当前行的 dp
        new_dp = [0] * n
        for j in range(n):
            # 如果当前列不是上一行最小值所在列，就可以直接使用 first_min
            prev = first_min if j != first_idx else second_min
            new_dp[j] = grid[i][j] + prev

        dp = new_dp                      # 进入下一轮

    # 3️⃣ 最后一行的最小值即为答案
    return min(dp)
```

#### 复杂度  

- **时间复杂度：`O(n²)`**  
  - 对每一行我们只做两次线性遍历，整体是 `n × 2n = 2n²`，常数因素小。  
  - 与暴力的 `O(n³)` 相比，速度提升约 `n` 倍（例如 `n=200` 时从 8 百万次降到 40 千次）。

- **空间复杂度：`O(n)`**  
  - 只保留当前行的 `dp`（长度 `n`）和新建的 `new_dp`，不需要整张 `n×n` 的表。  
  - 对比暴力的 `O(n²)`，省了大量内存。

---

## 心得  

- **核心技巧**：在 DP 中“**只保留上一层的最小/次小值**”，从而把“遍历所有前驱”降到常数时间。  
- **适用场景**：  
  1. **矩阵/网格 DP**，每一步只能从上一层的**除自身外的任意位置**转移（如本题）。  
  2. **行列约束的最小/最大路径**（例如 “最小上升路径” 需要不同列或行）。  
  3. **分组背包** 中“同组不能选同一件”时，维护组内最小/次小即可。  
- **一句话总结**：**“当转移规则是‘不能和前一步同列（或同组）’，只记前一步的最小和次小，就能实现 O(1) 转移”。**

---

## 反思  

- **第一反应**：直接写 `dp[i][j] = grid[i][j] + min(dp[i-1][k] for k != j)`，把所有合法前驱都遍历一遍。  
- **最容易踩的坑**：  
  - **边界条件**：`n = 1` 时直接返回唯一元素。  
  - **负数**：因为元素可能为负数，初始化最小值时一定要用 `float('inf')`，不能用 `0`。  
  - **同列冲突**：忘记在最小值列上使用次小值，会导致错误的“同列”路径被算进来。  
- **下次遇到类似题**：第一步先**思考转移是否有“排除自身”**的限制，若是，就尝试**维护前一层的最小/次小**，看能否把 `O(n³)` 降到 `O(n²)`。