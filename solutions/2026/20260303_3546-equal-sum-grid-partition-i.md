# #3546. 等和网格划分 I / Equal Sum Grid Partition I

> 难度：中等 · 标签：Array、Matrix、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/equal-sum-grid-partition-i/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix grid of positive integers. Your task is to determine if it is possible to make either one horizontal or one vertical cut on the grid such that:
Return true if such a partition exists; otherwise return false.

**Examples**

**Example 1:**

```
Input: grid = [[1,4],[2,3]]
Output: true
Explanation:

A horizontal cut between row 0 and row 1 results in two non-empty sections, each with a sum of 5. Thus, the answer is true .
```

**Example 2:**

```
Input: grid = [[1,3],[2,4]]
Output: false
Explanation:
No horizontal or vertical cut results in two non-empty sections with equal sums. Thus, the answer is false .
```

**Constraints**

- 1 <= m == grid.length <= 105
- 1 <= n == grid[i].length <= 105
- 2 <= m * n <= 105
- 1 <= grid[i][j] <= 105

---

## 题目（中文翻译）

给定一个由正整数构成的 **m × n** 矩阵（matrix）`grid`。请判断是否可以在该矩阵上只进行一次 **水平切割（horizontal cut）** 或一次 **垂直切割（vertical cut）**，使得切割后得到的两个非空子区域（section）的元素和（sum）相等。  

如果存在满足条件的划分，返回 `true`；否则返回 `false`。  

### 示例

**示例 1**  
```text
Input: grid = [[1,4],[2,3]]
Output: true
Explanation:
在第 0 行和第 1 行之间进行一次水平切割（horizontal cut），可得到两个非空部分，分别的元素和均为 5。因此答案为 true。
```

**示例 2**  
```text
Input: grid = [[1,3],[2,4]]
Output: false
Explanation:
无论进行水平切割（horizontal cut）还是垂直切割（vertical cut），都无法得到两个非空部分的元素和相等。因此答案为 false。
```

### 约束条件
- `1 <= m == grid.length <= 10^5`
- `1 <= n == grid[i].length <= 10^5`
- `2 <= m * n <= 10^5`
- `1 <= grid[i][j] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是**枚举所有可能的切割位置**，分别计算切割后上下（或左右）两块的元素和，看它们是否相等。  

- **水平切割**：在第 `r` 行和第 `r+1` 行之间划一条线（`0 ≤ r < m‑1`），上面的部分是第 `0 … r` 行，下面的部分是第 `r+1 … m‑1` 行。  
- **垂直切割**：在第 `c` 列和第 `c+1` 列之间划线（`0 ≤ c < n‑1`），左边是第 `0 … c` 列，右边是第 `c+1 … n‑1` 列。  

要实现这个想法，需要：

1. **遍历所有行**，把每一行的所有元素加起来得到该行的和。  
2. 对每一个可能的水平切割 `r`，把 `0 … r` 行的和相加得到上半部分的总和 `top`，下半部分的总和就是 `total - top`（`total` 为整个矩阵的总和）。如果 `top == total - top`，说明找到了合法的切割，直接返回 `True`。  
3. 同理**遍历所有列**，做同样的检查。  

> **类比**：把矩阵想象成一本厚厚的书，行是书页，列是章节。我们想在某页之间或者某章节之间“撕开”书本，两边的字数（即元素和）要相等。只要把每页（每列）的字数累加起来，随时检查左/上边的字数是否已经占到了一半，就能判断是否可以平分。

**为什么正确**：如果存在一种切割使得两块的和相等，那么必然在遍历到对应的切割位置时，上半/左半的累计和会恰好等于总和的一半。我们检查所有可能的位置，自然不会漏掉。

**时间/空间复杂度**（大白话版）：

- **时间**：我们需要先遍历整个矩阵一次算总和（`m·n` 次加法），随后再分别遍历所有行和所有列（每行/列只加一次），总共也是 `O(m·n)`。如果把“遍历所有切割位置并每次重新求和”写成两层循环，那就是 `O((m+n)·m·n)`，太慢了。这里的暴力实现已经把每次求和的工作提前累计好，避免了重复计算。  
- **空间**：只用几个整数保存累计和和总和，不需要额外的数组，空间是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def equalSumGridPartition(grid: List[List[int]]) -> bool:
    m, n = len(grid), len(grid[0])

    # 1️⃣ 计算整个矩阵的总和
    total = 0
    for i in range(m):
        for j in range(n):
            total += grid[i][j]          # 把每个格子里的数字加进来

    # 2️⃣ 检查所有可能的水平切割
    top_sum = 0                         # 累计上半部分的和
    for r in range(m - 1):              # 最后一行后面不能切
        row_sum = sum(grid[r])          # 这一行的和
        top_sum += row_sum              # 加到上半部分
        if top_sum == total - top_sum:  # 看看上下两块是否相等
            return True

    # 3️⃣ 检查所有可能的垂直切割
    left_sum = 0                        # 累计左半部分的和
    for c in range(n - 1):              # 最后一列后面不能切
        col_sum = 0
        for i in range(m):
            col_sum += grid[i][c]       # 累加第 c 列的每个元素
        left_sum += col_sum
        if left_sum == total - left_sum:
            return True

    # 如果所有切割都不满足条件，返回 False
    return False
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 解释：我们只遍历矩阵两遍（一次算总和，一次算行/列累计），每个格子最多被访问两次，和矩阵大小成正比。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了几个整数变量来保存累计和，没有使用额外随矩阵规模增长的数组。

---  

### 2. 最优解  

#### 思路  
从暴力解出发，**瓶颈**在于我们在检查垂直切割时，需要对每一列重新遍历所有行来求列和，这会导致额外的 `O(m·n)` 工作，虽然整体仍是 `O(m·n)`，但可以进一步把这一步也改成 **一次遍历** 完成。

**优化思路**：

1. **一次遍历算出所有行的前缀和**（累加到 `top_sum`），同时**一次遍历算出所有列的前缀和**（累加到 `left_sum`）。  
2. 为了在同一次遍历中同时得到每一列的和，我们可以**在读取矩阵的过程中把每列的累计和保存在一个长度为 `n` 的数组 `col_prefix`**。这样遍历第 `i` 行时，就把该行每个元素加入对应列的前缀和。  
3. 当遍历完第 `i` 行后，`top_sum` 已经是第 `0…i` 行的总和；`col_prefix[j]` 已经是第 `0…i` 行第 `j` 列的累计和。我们可以立即检查：  
   - 如果 `top_sum == total - top_sum`（水平切割在第 `i` 行下方） → 返回 `True`。  
   - 同时，对于每一列 `j`（`j < n-1`），如果 `col_prefix[j] == total - col_prefix[j]`（垂直切割在第 `j` 列右侧） → 返回 `True`。  
4. 只要在一次遍历结束前找到了满足条件的切割，就可以提前返回。若遍历完仍未找到，则返回 `False`。  

> **类比**：把矩阵想成一块巧克力，每一行是横向的条纹，每一列是纵向的条纹。我们在“吃”巧克力的过程中，边吃边记录已经吃掉的横向和纵向的重量，一旦发现已经吃掉的重量恰好是整块巧克力的一半，就可以把它一刀劈开。

**核心技巧**：**前缀和（Prefix Sum）**。前缀和的思想是：把“前面所有元素的和”保存下来，这样在后面判断“前半部分是否等于后半部分”时，只需要一次比较，而不必每次都重新累加。

#### 代码（Python）

```python
from typing import List

def equalSumGridPartition(grid: List[List[int]]) -> bool:
    m, n = len(grid), len(grid[0])

    # ① 先算出整个矩阵的总和（只遍历一次）
    total = 0
    for row in grid:
        total += sum(row)

    # ② 初始化用于记录每列前缀和的数组
    col_prefix = [0] * n          # col_prefix[j] = 已经遍历到的行中，第 j 列的累计和
    top_sum = 0                   # 已经遍历的行的累计和（用于水平切割）

    # ③ 逐行遍历，同时更新列前缀和
    for i in range(m):
        row_sum = sum(grid[i])    # 第 i 行的总和
        top_sum += row_sum        # 累计到上半部分

        # 检查水平切割（只能在 i 行之后切，i < m-1）
        if i < m - 1 and top_sum == total - top_sum:
            return True

        # 更新每列的前缀和，并检查垂直切割
        for j in range(n):
            col_prefix[j] += grid[i][j]   # 把第 i 行第 j 列的值加进去

        # 检查所有可能的垂直切割（只能在第 j 列右侧切，j < n-1）
        for j in range(n - 1):
            if col_prefix[j] == total - col_prefix[j]:
                return True

    # 没有任何合法切割
    return False
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 解释：我们只遍历矩阵一次（每个格子访问一次），在遍历过程中即完成了行前缀和、列前缀和的更新以及切割检查。  
  - 与暴力解的时间复杂度相同，但**常数因子更小**（没有额外的二次遍历），在大数据量时更快。  

- **空间复杂度**：`O(n)`  
  - 解释：额外使用了一个长度为 `n` 的数组 `col_prefix` 来保存列的累计和。若把 `n` 看作矩阵的列数，这个空间随列数线性增长。相比最原始的“每次重新遍历列”方案，省去了 `O(m·n)` 的临时存储。

---  

## 心得  

- **核心技巧**：前缀和（Prefix Sum）——把“前面已经累计的和”保存下来，后面只需要 O(1) 就能得到子区间的和。  
- **适用题型**：  
  1. “数组/矩阵能否被等分”类（如 `Split Array Largest Sum`、`Equal Sum Partition`）。  
  2. “子数组/子矩阵和等于目标值”类（如 `Subarray Sum Equals K`、`Number of Submatrices That Sum to Target`）。  
- **一句话总结解题钥匙**：**把累计和保存下来，一遍遍历中同步检查是否已经达到整体的一半**。  

---  

## 反思  

- **第一反应**：直接枚举所有切割位置，分别求两块的和——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记切割必须把矩阵分成**非空**两块，切割位置不能在最外侧。  
  - 在检查垂直切割时，若每次都重新遍历整列，会导致时间超限。  
  - 计算总和时使用 `int` 足够，但在某些语言需要注意整数溢出（Python 自动大整数）。  
- **下次类似题的第一步**：先算出**整体总和**，判断是否为偶数（只有偶数才可能平分），然后使用**前缀和**在一次遍历中同步检查水平和垂直的可能性。