# #3148. **网格中的最大差值得分** / Maximum Difference Score in a Grid

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-score-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix grid consisting of positive integers. You can move from a cell in the matrix to any other cell that is either to the bottom or to the right (not necessarily adjacent). The score of a move from a cell with the value c1 to a cell with the value c2 is c2 - c1.
You can start at any cell, and you have to make at least one move.
Return the maximum total score you can achieve.

**Examples**

**Example 1:**

```
Input: grid = [[9,5,7,3],[8,9,6,1],[6,7,14,3],[2,5,3,1]]
Output: 9
Explanation: We start at the cell (0, 1) , and we perform the following moves: - Move from the cell (0, 1) to (2, 1) with a score of 7 - 5 = 2 . - Move from the cell (2, 1) to (2, 2) with a score of 14 - 7 = 7 . The total score is 2 + 7 = 9 .
```

**Example 2:**

```
Input: grid = [[4,3,2],[3,2,1]]
Output: -1
Explanation: We start at the cell (0, 0) , and we perform one move: (0, 0) to (0, 1) . The score is 3 - 4 = -1 .
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 2 <= m, n <= 1000
- 4 <= m * n <= 105
- 1 <= grid[i][j] <= 105

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的矩阵（matrix）`grid`，其中所有元素均为正整数。你可以从矩阵中的任意单元格（cell）移动到同一列更下方或同一行更右侧的任意单元格（不要求相邻）。一次移动的得分定义为目标单元格的值 `c2` 减去起始单元格的值 `c1`，即 `c2 - c1`。  
你可以从任意单元格开始，且必须至少进行一次移动。返回能够获得的最大总得分（total score）。

**示例 1**

```text
Input: grid = [[9,5,7,3],[8,9,6,1],[6,7,14,3],[2,5,3,1]]
Output: 9
Explanation: 我们从单元格 (0, 1) 开始，依次执行以下移动：
- 从 (0, 1) 移动到 (2, 1)，得分为 7 - 5 = 2。
- 从 (2, 1) 移动到 (2, 2)，得分为 14 - 7 = 7。
总得分为 2 + 7 = 9。
```

**示例 2**

```text
Input: grid = [[4,3,2],[3,2,1]]
Output: -1
Explanation: 我们从单元格 (0, 0) 开始，只进行一次移动：从 (0, 0) 到 (0, 1)。得分为 3 - 4 = -1。
```

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `2 <= m, n <= 1000`
- `4 <= m * n <= 10^5`
- `1 <= grid[i][j] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一个格子都当作**起点**，然后把它能到达的所有格子（只能向下或向右）都枚举一遍，计算一次移动的得分 `c2 - c1`，把这些得分加起来得到整条路径的总分，最后取最大的那个。

> **数据结构类比**  
> - **二维数组** `grid` 就像一本带有坐标的表格，每个格子里放着一个数字。  
> - 暴力遍历时我们要把这本表格的每一页（每个格子）都当成“起点”，然后翻到它后面所有可能的页（满足只向下或向右的格子），这一步类似“查字典”时把每个词的所有后续词都列出来。

为什么能得到正确答案？因为题目要求**任意起点**、**任意合法路径**，只要我们把所有合法路径的得分都算一遍，最大值必然在其中。

**时间复杂度**  
- 对每个格子 `O(m·n)`，我们都要向下遍历至最底行、向右遍历至最右列，最坏情况是遍历 `O(m·n)` 个终点。  
- 所以总共是 `O((m·n)²)`，即 **平方级**。如果把 `m·n` 看成 `N`，则是 `O(N²)`。这在 `m,n ≤ 1000`（即 `N ≤ 10⁶`）时根本跑不完。

**空间复杂度**  
- 只用了原来的 `grid`，再加几个常数变量，**O(1)** 额外空间。

#### 代码（Python）

```python
from typing import List

def maxScore_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    best = -10**9                     # 记录全局最大得分，初始设很小
    for i in range(m):
        for j in range(n):            # (i, j) 作为起点
            start_val = grid[i][j]
            # 向下遍历
            for x in range(i + 1, m):
                diff = grid[x][j] - start_val
                best = max(best, diff)            # 只走一步的得分
                # 再继续往右走（多步路径）
                cur = diff
                for y in range(j + 1, n):
                    cur += grid[x][y] - grid[x][y-1]   # 每一步右移的增量
                    best = max(best, cur)
            # 向右遍历（只走右，不走下）
            cur = 0
            for y in range(j + 1, n):
                cur += grid[i][y] - grid[i][y-1]
                best = max(best, cur)
    return best
```

> **关键行注释**  
> - `best = -10**9`：因为得分可能为负数，先把答案设成一个很小的数。  
> - `diff = grid[x][j] - start_val`：从起点直接跳到同列的下方格子，只算一次得分。  
> - `cur += grid[x][y] - grid[x][y-1]`：当我们在同一行继续向右移动时，每一步的得分都是“右边格子值 - 左边格子值”。把这些增量累计起来，就得到从起点经过若干格子的总得分。

#### 复杂度

- **时间复杂度**：`O((m·n)²)`，即平方级。可以想象成把 `N = m·n` 个格子两两配对，数量是 `N²`，所以会非常慢。  
- **空间复杂度**：`O(1)`，只用了常数级额外空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于我们把每一条路径都枚举了一遍。其实，题目给了一个非常重要的提示：

> **任意合法路径的总得分 = 终点格子的值 - 起点格子的值**  

因为向下或向右的每一步得分都是 “后一个格子值 - 前一个格子值”，把所有步骤相加后，内部的值会相互抵消，只剩下 **终点** 减 **起点**。  
这意味着我们只需要找一对格子 `(start, end)`，满足 `end` 能够从 `start` 到达（即 `end` 在 `start` 的右下方向），并且让 `grid[end] - grid[start]` 最大即可。

**如何快速找出这样的配对？**  

遍历矩阵时，维护“当前格子左上方（包括同一行左侧和同一列上方）能够到达的最小值”。记作 `min_sofar[i][j]`。  
- 当我们来到格子 `(i, j)` 时，所有能够作为它起点的格子都已经遍历过（因为只能往右或往下），它们的最小值就是 `min_sofar[i][j]`。  
- 那么以 `(i, j)` 为终点的最佳得分就是 `grid[i][j] - min_sofar[i][j]`。  
- 同时，`min_sofar[i][j]` 需要更新为 `min(grid[i][j], min_sofar[i-1][j], min_sofar[i][j-1])`，因为以后更右下的格子也可以把当前格子当作起点。

这样只需要一次遍历矩阵，就能在 **O(m·n)** 时间内得到答案。

> **核心算法：动态规划**  
> - “状态” 是 `min_sofar[i][j]`（到达 `(i, j)` 前的最小格子值）。  
> - “状态转移” 只依赖于上方和左方两个已经算好的状态。  
> - 这正是**动态规划**的典型写法：把大问题拆成小子问题，逐步合并。

> **类比**  
> 想象你在山谷里行走，只能往东或往南。你想找一条从低处到高处的路径，使高度差最大。遍历时，你把每个位置的**最低海拔**记下来，后面每到一个新位置，只要看“当前海拔 - 之前记的最低海拔”，差值就是从最低点走到这里的最大爬升。

#### 代码（Python）

```python
from typing import List

def maxScore(grid: List[List[int]]) -> int:
    """
    返回在只能向下或向右移动的前提下，任意起点、任意终点的最大总得分。
    """
    m, n = len(grid), len(grid[0])

    # min_val[i][j] 表示 (i, j) 左上（包括本格）能够到达的最小格子值
    min_val = [[0] * n for _ in range(m)]

    # 初始化左上角
    min_val[0][0] = grid[0][0]

    # 第一行只能从左边来到
    for j in range(1, n):
        min_val[0][j] = min(min_val[0][j-1], grid[0][j])

    # 第一列只能从上边来到
    for i in range(1, m):
        min_val[i][0] = min(min_val[i-1][0], grid[i][0])

    ans = -10**9                     # 全局最大得分，先设成很小的数

    # 从左上到右下遍历（跳过 (0,0) 因为必须至少移动一次）
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue            # 起点不能自己当终点，必须移动

            # 取到达 (i,j) 前的最小格子值（不包括自己）
            best_start = min(
                min_val[i-1][j] if i > 0 else 10**9,
                min_val[i][j-1] if j > 0 else 10**9
            )
            # 以 (i,j) 为终点的得分
            cur_score = grid[i][j] - best_start
            ans = max(ans, cur_score)

            # 更新 min_val，让后面的格子能够使用
            min_val[i][j] = min(grid[i][j], best_start)

    return ans
```

> **关键行解释**  
> - `best_start = min(min_val[i-1][j] if i > 0 else INF, min_val[i][j-1] if j > 0 else INF)`  
>   取上方或左方已经记录的最小值；如果当前位置在第一行/列，另一侧不存在，用一个很大的数 `INF` 代替，保证不会误选。  
> - `cur_score = grid[i][j] - best_start`  
>   正是“终点值 - 能到达的最小起点值”。这一步把所有可能的起点一次性考虑完。  
> - `min_val[i][j] = min(grid[i][j], best_start)`  
>   更新到达当前格子后，整体可见的最小值，以供右下方继续使用。

#### 复杂度

- **时间复杂度**：`O(m·n)`。我们只遍历矩阵一次，每个格子做 `O(1)` 的常数操作。相比暴力的 `O((m·n)²)`，快了几乎 **指数级**（把 `N²` 降到 `N`）。  
- **空间复杂度**：`O(m·n)` 用来保存 `min_val`。如果想进一步节省空间，可以把它压缩成两行或一行滚动数组，空间可降到 `O(n)`，但对初学者保持二维数组更直观。

---

## 心得

- **核心技巧**：把路径得分化简为 “终点值 - 起点值”，进而只需要维护“左上方的最小值”。这是一种**单调性**的思想，常见于“最大差值”类问题。  
- **适用的题型**  
  1. **数组最大差值**：如 “Maximum Difference Between Two Elements” 只允许后面的元素减前面的元素。  
  2. **二维网格最大升高**：如 “Best Time to Buy and Sell Stock II” 的二维版本。  
  3. **单调栈/单调队列**：在需要“左侧最近更小/更大元素”时，也会用到类似的“维护最小值”思路。  
- **一句话总结解题钥匙**：**把累加的每一步差值抵消掉，只关心起点最小、终点最大**。

---

## 反思

- **第一反应**：看到“只能向右或向下”，自然想到 DFS/回溯或 DP，进而想把所有路径枚举。  
- **最容易踩的坑**  
  1. **必须至少移动一次**：不能把同一个格子当作路径（得分 0），所以答案可能是负数。  
  2. **起点必须在终点的左上方**：如果误把右上或左下的格子当作起点，会导致非法路径。  
  3. **边界初始化**：第一行/列的 `min_val` 只能来自唯一的方向，忘记处理会导致 `IndexError`。  
- **下次类似题的第一步**：先思考“路径累计的得分会不会出现抵消”，如果可以化简为“终点值 - 起点值”，就立刻转向**维护极值（最小/最大）**的动态规划或单调结构，而不是枚举所有路径。