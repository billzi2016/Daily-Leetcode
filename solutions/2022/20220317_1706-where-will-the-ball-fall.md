# #1706. 球会掉落到哪里 / Where Will the Ball Fall

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/where-will-the-ball-fall/)

---

## 题目（英文原版）

**Description**

You have a 2-D grid of size m x n representing a box, and you have n balls. The box is open on the top and bottom sides.
Each cell in the box has a diagonal board spanning two corners of the cell that can redirect a ball to the right or to the left.
We drop one ball at the top of each column of the box. Each ball can get stuck in the box or fall out of the bottom. A ball gets stuck if it hits a "V" shaped pattern between two boards or if a board redirects the ball into either wall of the box.
Return an array answer of size n where answer[i] is the column that the ball falls out of at the bottom after dropping the ball from the ith column at the top, or -1 if the ball gets stuck in the box.

**Examples**

**Example 1:**

```
Input: grid = [[1,1,1,-1,-1],[1,1,1,-1,-1],[-1,-1,-1,1,1],[1,1,1,1,-1],[-1,-1,-1,-1,-1]]
Output: [1,-1,-1,-1,-1]
Explanation: This example is shown in the photo.
Ball b0 is dropped at column 0 and falls out of the box at column 1.
Ball b1 is dropped at column 1 and will get stuck in the box between column 2 and 3 and row 1.
Ball b2 is dropped at column 2 and will get stuck on the box between column 2 and 3 and row 0.
Ball b3 is dropped at column 3 and will get stuck on the box between column 2 and 3 and row 0.
Ball b4 is dropped at column 4 and will get stuck on the box between column 2 and 3 and row 1.
```

**Example 2:**

```
Input: grid = [[-1]]
Output: [-1]
Explanation: The ball gets stuck against the left wall.
```

**Example 3:**

```
Input: grid = [[1,1,1,1,1,1],[-1,-1,-1,-1,-1,-1],[1,1,1,1,1,1],[-1,-1,-1,-1,-1,-1]]
Output: [0,1,2,3,4,-1]
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- grid[i][j] is 1 or -1.

---

## 题目（中文翻译）

你有一个大小为 `m x n` 的二维网格（2-D grid）表示一个盒子（box），并且有 `n` 个球。盒子的上下两侧是打开的。  
网格中的每个单元格（cell）都有一块对角板（diagonal board），它跨越单元格的两个角，可以将球向右或向左重定向。  

我们在盒子每一列的顶部各投下一颗球。每颗球要么卡在盒子里，要么从底部掉出。  
球会卡住的情况有两种：

1. 球撞到了两个相邻对角板形成的 “V” 形（V-shaped）模式。  
2. 对角板把球导向盒子的左墙或右墙。

返回一个大小为 `n` 的数组 `answer`，其中 `answer[i]` 是第 `i` 列顶部投下的球最终从底部掉出的列索引；如果球卡住，则为 `-1`。

### 示例

#### 示例 1
**输入**  
```text
grid = [[1,1,1,-1,-1],
        [1,1,1,-1,-1],
        [-1,-1,-1,1,1],
        [1,1,1,1,-1],
        [-1,-1,-1,-1,-1]]
```
**输出**  
```text
[1,-1,-1,-1,-1]
```
**解释**  
如图所示：  
- 球 `b0` 从第 0 列投下，最终从第 1 列掉出。  
- 球 `b1` 从第 1 列投下，会在第 1 行第 2~3 列之间的 “V” 形处卡住。  
- 球 `b2` 从第 2 列投下，会在第 1 行第 2~3 列之间的 “V” 形处卡住。  
- 球 `b3` 从第 3 列投下，会在第 0 行第 3~4 列之间的 “V” 形处卡住。  
- 球 `b4` 从第 4 列投下，会在第 0 行第 4~5 列之间的 “V” 形处卡住。  

#### 示例 2
**输入**  
```text
grid = [[-1]]
```
**输出**  
```text
[-1]
```
**解释**  
球被导向左墙而卡住。

#### 示例 3
**输入**  
```text
grid = [[1,1,1,1,1,1],
        [-1,-1,-1,-1,-1,-1],
        [1,1,1,1,1,1],
        [-1,-1,-1,-1,-1,-1]]
```
**输出**  
```text
[0,1,2,3,4,-1]
```

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 100`
- `grid[i][j]` 只能是 `1` 或 `-1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每一颗球想成一只小球，从箱子的**顶部**某一列掉下来，沿着每个格子的斜板向左或向右滑动，直到到达底部或者卡住。  

- **数据结构**：我们直接把输入的 `grid` 当成二维数组（矩阵）来用。二维数组就像一张**电子表格**，行号 `i` 是从上到下的层数，列号 `j` 是从左到右的位置。  
- **模拟过程**：从第 `0` 行开始，检查当前格子里的斜板方向  
  - `grid[i][j] == 1` 表示斜板把球往右推（\ /），球会向右移动到 `j+1`，并下落到下一行 `i+1`。  
  - `grid[i][j] == -1` 表示斜板把球往左推（/ \），球会向左移动到 `j-1`，并下落到下一行 `i+1`。  
- **卡住的情况**  
  1. 球要往右走，但是已经在最右边的列（`j == n-1`），会撞墙。  
  2. 球要往左走，但是已经在最左边的列（`j == 0`），会撞墙。  
  3. 当前格子向右，而右边格子向左（形成 “V”），或者当前格子向左而左边格子向右（形成倒 “V”），球会卡在两块板之间。  

只要把上面的规则一步一步执行下来，就能得到每颗球最终掉出的列号，或者 `-1`（表示卡住）。

#### 代码（Python）

```python
from typing import List

def findBall(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])          # 行数、列数
    answer = [-1] * n                       # 预先准备答案数组

    # 把每一列的球都单独模拟一次
    for start_col in range(n):
        col = start_col                      # 球当前所在的列
        for row in range(m):
            direction = grid[row][col]       # 当前格子的斜板方向

            # 计算球要去的下一个列号
            next_col = col + direction

            # ① 越界 → 撞墙
            if next_col < 0 or next_col >= n:
                col = -1                      # 标记卡住
                break

            # ② “V” 形卡住：当前格子向右，但右边格子向左；或相反
            if grid[row][next_col] != direction:
                col = -1
                break

            # ③ 正常移动到下一行的 next_col
            col = next_col

        # 循环结束后，col 若仍是合法列号，则说明掉到底部
        answer[start_col] = col if col != -1 else -1

    return answer
```

> **关键注释**  
> - `direction` 只能是 `1`（右）或 `-1`（左），所以 `col + direction` 就是球要去的下一个列。  
> - `grid[row][next_col] != direction` 用来检测 **V** 形卡住的情况：如果相邻两个格子的方向不一致，球就会卡住。  

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - 解释：我们对每一列（共 `n` 列）都遍历最多 `m` 行，所以总共最多做 `m × n` 步操作。把 `O(m·n)` 想象成“如果箱子有 10 行 10 列，需要检查 100 次”。  
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 解释：除了输入的 `grid` 和返回的 `answer`，我们只用了几个整数变量 (`row`, `col`, `direction`)，占用常数级别的空间。  

---

### 2. 最优解

#### 思路  

上面的直觉解已经是 **线性** 的 `O(m·n)`，在本题的约束（`m, n ≤ 100`）下已经很快了。  
但是我们可以把 **模拟过程** 看成一种**动态规划**：  
- 若已知球进入某个格子 `(i, j)` 时会最终掉到哪一列（或卡住），则可以直接把这个结果写到格子 `(i-1, j')` 上，省掉后面的重复模拟。  
- 具体做法是从 **底部向上** 逐行计算，每个格子保存“从这里掉下来会到达的列号”。  

这样做的好处是：每个格子只被访问一次，时间仍是 `O(m·n)`，但我们把**每颗球的完整路径**合并到一次遍历里，代码更简洁，且易于解释 “从下往上推导”。  

**核心概念——“从下往上”**  
- 底层行 `m-1` 的每个格子如果不卡住，直接把它对应的列号写进去（因为已经是最后一层）。  
- 对于上面的行 `i`，看它的斜板方向 `grid[i][j]`：  
  - 若向右（`1`），检查右边格子 `j+1` 是否也向右且不越界。若满足，则当前格子掉出的列 = 右边格子记录的列。  
  - 若向左（`-1`），检查左边格子 `j-1` 是否也向左且不越界。若满足，则当前格子掉出的列 = 左边格子记录的列。  
  - 否则，这里卡住，记录为 `-1`。  

最终，第一行（第 `0` 行）每个格子记录的就是从对应列顶部掉下来的结果。

#### 代码（Python）

```python
from typing import List

def findBall(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])
    # dp[i][j] 表示从格子 (i, j) 开始往下，最终会掉到哪一列（-1 表示卡住）
    dp = [[-1] * n for _ in range(m)]

    # 初始化最底层：只要不越界且不形成 V，就直接是自己的列号
    for j in range(n):
        dp[m - 1][j] = j  # 最后一行不需要检查 V，因为已经到底

    # 自底向上遍历每一行（除最底层外）
    for i in range(m - 2, -1, -1):
        for j in range(n):
            direction = grid[i][j]
            next_j = j + direction          # 球要去的下一列

            # 越界直接卡住
            if next_j < 0 or next_j >= n:
                dp[i][j] = -1
                continue

            # 检查相邻格子的方向是否一致（防止 V 形卡住）
            if grid[i][next_j] != direction:
                dp[i][j] = -1
                continue

            # 若相邻格子已经算出了结果，则沿用
            dp[i][j] = dp[i + 1][next_j]

    # 第一行的 dp 即为答案
    return dp[0]
```

> **关键注释**  
> - `dp[i][j]` 把“从这里掉下来会去哪个列”这个信息**缓存**下来，后面再需要时直接查表。  
> - `grid[i][next_j] != direction` 正是检测 **V** 形卡住的条件：两块相邻的斜板方向不一致，球会卡在中间。  
> - 最底层直接把列号写进去，因为已经没有更下一行可检查，球只能直接掉出。  

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - 解释：我们只遍历一次二维表的每个格子（`m × n` 次），每次只做常数时间的检查。相较于直觉解，这里**不再对每一列重复走完整条路径**，而是一次遍历完成所有列的答案。  
- **空间复杂度**：`O(m * n)`（也可以改写成 `O(n)`）  
  - 解释：我们用了一个同样大小的 `dp` 表来保存每格的结果。如果只保留当前行和下一行的结果，也可以把空间压缩到 `O(n)`，但对本题来说 `O(m·n)` 已经足够小（最多 10,000 个整数）。  

---

## 心得

- **核心技巧**：**从下往上动态规划**（或“自底向上”） + **状态缓存**（把每个格子的结果记下来）。  
- **适用的题型**  
  1. 需要沿着固定方向“滑动”或“流动”，且每一步的结果只取决于下一步的状态（例如「摆动的球」类题目、迷宫的单向流动）。  
  2. 类似的 LeetCode 题目有  
     - *“Falling Squares”*（模拟方块下落，使用区间合并）  
     - *“Candy Crush”*（自底向上消除）  
- **一句话总结解题钥匙**：**把每一步的结果缓存起来，逆向推导即可一次遍历得到所有答案**。

---

## 反思

- **第一反应**：直接把每颗球从上到下“走一遍”。这在代码实现上最直观，但会产生很多重复的子路径。  
- **最容易踩的坑**  
  1. **越界**：向左时 `j-1`、向右时 `j+1` 必须先检查是否在 `[0, n-1]` 范围内，否则会数组索引错误。  
  2. **V 形卡住**：相邻两个格子方向不一致时必须立刻判定卡住，不能继续往下。  
  3. **底部行的处理**：底行没有下一行，需要单独把列号写进去，否则会误把 `-1` 当作答案。  
- **下次遇到同类题**：第一步先**思考状态转移**——“从当前格子往下会得到什么”，然后决定是**正向模拟**还是**逆向 DP**，看哪种方式可以把重复计算省掉。这样往往能把时间从指数/平方级降到线性级。