# #3127. 同色正方形 / Make a Square with the Same Color

> 难度：简单 · 标签：Array、Matrix、Enumeration · [LeetCode 链接](https://leetcode.com/problems/make-a-square-with-the-same-color/)

---

## 题目（英文原版）

**Description**

You are given a 2D matrix grid of size 3 x 3 consisting only of characters 'B' and 'W'. Character 'W' represents the white color, and character 'B' represents the black color.
Your task is to change the color of at most one cell so that the matrix has a 2 x 2 square where all cells are of the same color.
Return true if it is possible to create a 2 x 2 square of the same color, otherwise, return false.

**Examples**

**Example 1:**

```
Input: grid = [["B","W","B"],["B","W","W"],["B","W","B"]]
Output: true
Explanation:
It can be done by changing the color of the grid[0][2] .
```

**Example 2:**

```
Input: grid = [["B","W","B"],["W","B","W"],["B","W","B"]]
Output: false
Explanation:
It cannot be done by changing at most one cell.
```

**Example 3:**

```
Input: grid = [["B","W","B"],["B","W","W"],["B","W","W"]]
Output: true
Explanation:
The grid already contains a 2 x 2 square of the same color.
```

**Constraints**

- grid.length == 3
- grid[i].length == 3
- grid[i][j] is either 'W' or 'B'.

---

## 题目（中文翻译）

你得到一个大小为 3 × 3 的二维矩阵（grid），矩阵中仅包含字符 `'B'`（黑色）和 `'W'`（白色）。  
任务是最多更改一个单元格（cell）的颜色，使得矩阵中出现一个 2 × 2 的正方形（square），且该正方形内的四个单元格颜色全部相同。  

如果可以通过至多一次颜色修改得到这样的 2 × 2 正方形，返回 `true`；否则返回 `false`。

**示例 1**  
```text
Input: grid = [["B","W","B"],["B","W","W"],["B","W","B"]]
Output: true
Explanation:
将 grid[0][2] 的颜色改为 `'W'` 即可形成一个全部相同颜色的 2 × 2 正方形。
```

**示例 2**  
```text
Input: grid = [["B","W","B"],["W","B","W"],["B","W","B"]]
Output: false
Explanation:
即使最多更改一个单元格的颜色，也无法得到全同色的 2 × 2 正方形。
```

**示例 3**  
```text
Input: grid = [["B","W","B"],["B","W","W"],["B","W","W"]]
Output: true
Explanation:
矩阵已经包含一个全部相同颜色的 2 × 2 正方形，无需进行任何修改。
```

**约束条件**  

- `grid.length == 3`
- `grid[i].length == 3`
- `grid[i][j]` 只能是 `'W'` 或 `'B'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目只给了一个固定大小的 **3×3** 矩阵，要求在**至多改动一个格子**后，矩阵里出现一个 **2×2** 的全同色方块。  
最直接的办法就是把所有可能的 **2×2** 小方块全部枚举出来，逐个检查：

1. 先不改动任何格子，统计每个 2×2 方块里 `'B'` 和 `'W'` 的个数。  
2. 如果某个方块已经全是同一种颜色（4 个相同），直接返回 `True`。  
3. 否则，看看方块里最多的颜色出现了几次。如果最多的颜色已经出现 **3 次**，只需要把剩下的那一个格子改成同样的颜色，就可以得到全同色方块。  
4. 如果所有 2×2 方块里 **最多只有 2 个相同颜色**，即使改动一个格子也不可能让它们全部相同，返回 `False`。

> **类比**：把每个 2×2 小方块想象成一本小字典，字典里只有两种单词 `'B'` 和 `'W'`。我们只需要看字典里出现最多的单词有多少次，如果已经出现了 3 次，就只需要补一本（改动一个格子）就可以让字典全是同一个单词。

这种做法一定能得到正确答案，因为我们把**所有可能的 2×2 方块**都检查了一遍，并且对每个方块都考虑了“最多改动一次”的所有情况。

#### 代码（Python）

```python
from typing import List

def can_make_square(grid: List[List[str]]) -> bool:
    # 3x3 矩阵只有左上角 (0,0)、(0,1)、(1,0)、(1,1) 四个 2x2 子矩阵
    for i in range(2):               # 行号 0 或 1
        for j in range(2):           # 列号 0 或 1
            # 取出左上角为 (i,j) 的 2x2 方块的四个格子
            cells = [
                grid[i][j],
                grid[i][j + 1],
                grid[i + 1][j],
                grid[i + 1][j + 1]
            ]
            # 统计 B 与 W 的数量
            cntB = cells.count('B')
            cntW = 4 - cntB            # 因为总共 4 格，剩下的都是 W

            # 已经全相同，直接返回 True
            if cntB == 4 or cntW == 4:
                return True

            # 最多相同颜色出现了 3 次，只需改动剩下的 1 格
            if cntB == 3 or cntW == 3:
                return True

    # 没有任何 2x2 方块满足条件
    return False
```

#### 复杂度

- **时间复杂度**：`O(1)`  
  虽然我们说是“遍历所有 2×2 方块”，但在 3×3 矩阵里最多只有 **4** 个子矩阵，常数级别的操作不随输入规模增长，等价于 O(1)。  
  大白话：不管矩阵多大（这里固定 3×3），我们只检查几次，花的时间几乎不变。

- **空间复杂度**：`O(1)`  
  只用了几个计数变量和临时列表，额外占用的内存不随输入大小变化。

---

### 2. 最优解

#### 思路  

对这道题来说，上面的“暴力”已经是**最优**的做法，因为搜索空间本身只有 4 个 2×2 子矩阵，无法再进一步压缩。  
这里把“最优解”重新表述为**直接判断**的思路，帮助读者把握核心：

1. **观察**：要得到全同色的 2×2 方块，只需要在任意 2×2 子矩阵里出现 **至少 3 个相同颜色**。  
2. **遍历**：仍然遍历四个子矩阵，统计每个子矩阵中 `'B'` 的个数（`cntB`），`'W'` 的个数即 `4 - cntB`。  
3. **判定**：只要 `cntB >= 3` 或 `cntB <= 1`（即 `cntW >= 3`），说明可以通过 ≤1 次翻转得到全同色方块，返回 `True`。  
4. 所有子矩阵都不满足上述条件，则返回 `False`。

核心概念只有**计数**，不需要额外的数据结构。可以把 `cntB` 看成“这块小方块里黑色的票数”，只要票数够多（≥3）或者够少（≤1），就能“只改一票”让所有票统一。

#### 代码（Python）

```python
def can_make_square(grid: List[List[str]]) -> bool:
    # 只要任意 2x2 子矩阵里黑色数量 >=3 或 <=1，就能在至多一次翻转后得到全同色
    for i in range(2):
        for j in range(2):
            cntB = (
                (grid[i][j]   == 'B') +
                (grid[i][j+1] == 'B') +
                (grid[i+1][j] == 'B') +
                (grid[i+1][j+1] == 'B')
            )
            # cntB >= 3 -> 至少有 3 个 B； cntB <= 1 -> 至少有 3 个 W
            if cntB >= 3 or cntB <= 1:
                return True
    return False
```

> **小技巧**：`(grid[x][y] == 'B')` 在 Python 中会得到 `True/False`，在数值运算时会自动转成 `1/0`，于是可以直接相加得到黑色的数量。

#### 复杂度

- **时间复杂度**：`O(1)`  
  同上，只遍历 4 次子矩阵，常数时间。

- **空间复杂度**：`O(1)`  
  只使用了几个整数计数，额外空间不随输入变化。

---

## 心得

- **核心技巧**：**计数 + 常数遍历**  
  只要在每个 2×2 小块里统计一种颜色的出现次数，判断是否 ≥3（或 ≤1）即可决定是否能在 ≤1 次修改后得到全同色方块。

- **适用的题型**  
  1. 检查局部子矩阵是否满足某种“多数”条件（如 LeetCode 1277 “Count Square Submatrices with All Ones”）  
  2. “最多改动 k 次”使局部结构满足要求的题目（如 “Make the Fence Great Again” 中的局部检查）  
  3. 任意固定窗口大小的**滑动窗口计数**问题（如 “Maximum Number of Vowels in a Substring of Given Length”）

- **一句话总结**：只要子矩阵里已有 **3** 个相同颜色，就能用 **1** 次翻转完成全同色——计数即答案。

## 反思

- **第一反应**：看到“3×3、2×2、最多改动一次”，立刻想到**枚举所有 2×2 子矩阵**并**统计颜色**，因为规模太小不必考虑复杂的数据结构。

- **最容易踩的坑**  
  1. 忘记检查已经**全部相同**的情况（直接返回 `True`）。  
  2. 只统计 `'B'` 而不考虑 `'W'`，导致遗漏 `cntB <= 1` 的情形。  
  3. 错误的遍历范围：`i`、`j` 只能到 `1`（因为 2×2 方块左上角的坐标只能是 0 或 1），否则会越界。

- **下次遇到同类题**：第一步先**确定窗口大小**（这里是 2×2），然后**遍历所有窗口**，**统计关键属性**（颜色数、和、最大值等），最后**根据“最多改动 k 次”**的阈值判断可行性。这样思路统一，代码实现也会更简洁。