# #3276. 网格中选择单元格的最大得分 / Select Cells in Grid With Maximum Score

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Matrix、Bitmask · [LeetCode 链接](https://leetcode.com/problems/select-cells-in-grid-with-maximum-score/)

---

## 题目（英文原版）

**Description**

You are given a 2D matrix grid consisting of positive integers.
You have to select one or more cells from the matrix such that the following conditions are satisfied:
Your score will be the sum of the values of the selected cells.
Return the maximum score you can achieve.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,3],[4,3,2],[1,1,1]]
Output: 8
Explanation:

We can select the cells with values 1, 3, and 4 that are colored above.
```

**Example 2:**

```
Input: grid = [[8,7,6],[8,3,2]]
Output: 15
Explanation:

We can select the cells with values 7 and 8 that are colored above.
```

**Constraints**

- 1 <= grid.length, grid[i].length <= 10
- 1 <= grid[i][j] <= 100

---

## 题目（中文翻译）

给定一个由正整数构成的二维矩阵 `grid`。  
你需要从矩阵中选取一个或多个单元格，使得满足以下条件：

- 选取的单元格满足题目隐含的约束（题目原文未给出具体约束，依据示例可自行推断）。
- 你的得分等于所有被选中单元格的数值之和。

返回你能够获得的最大得分。

**示例 1**  
**输入**: `grid = [[1,2,3],[4,3,2],[1,1,1]]`  
**输出**: `8`  
**解释**:  

我们可以选取数值为 `1、3、4` 的单元格（如上图所示的颜色），其和为 `8`，即为最大得分。

**示例 2**  
**输入**: `grid = [[8,7,6],[8,3,2]]`  
**输出**: `15`  
**解释**:  

我们可以选取数值为 `7` 和 `8` 的单元格（如上图所示的颜色），其和为 `15`，即为最大得分。

**约束条件**

- `1 <= grid.length, grid[i].length <= 10`
- `1 <= grid[i][j] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求**选取若干个格子**，满足：

* 不能有两格在同一行  
* 不能有两格在同一列  

（可以把它想象成在一个棋盘上放“车”，每个车占据唯一的行和列，互不冲突。）  
选中的格子价值之和即为得分，求最大的可能得分。

最直接的想法是**把所有格子列成一个大列表**，然后枚举它的每一种选取方式（即每个格子“选”或“不选”），检查是否满足行、列互不冲突的约束，合法的就把价值相加取最大。

> **数据结构类比**：  
> - 把整个矩阵看成一本“词典”，每个格子是一条“词条”。  
> - 暴力枚举就像把词典的每一页都翻一遍，看看能否挑出一组不冲突的词条。

虽然思路极其简单，但实际会遍历 **2^(m·n)** 种情况（`m` 行、`n` 列），即使 `m,n ≤ 10`，`2^100` 也完全不可接受。

#### 代码（Python）

```python
from itertools import product

def maxScore_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    cells = [(i, j, grid[i][j]) for i in range(m) for j in range(n)]

    best = 0
    # 对每个格子决定选还是不选，使用二进制枚举
    for mask in range(1 << (m * n)):
        rows_used = set()
        cols_used = set()
        cur_sum = 0
        ok = True
        for idx, (i, j, val) in enumerate(cells):
            if mask >> idx & 1:                # 选中第 idx 个格子
                if i in rows_used or j in cols_used:
                    ok = False                 # 行或列冲突，直接放弃
                    break
                rows_used.add(i)
                cols_used.add(j)
                cur_sum += val
        if ok:
            best = max(best, cur_sum)
    return best
```

> **关键行中文注释**  
> - `for mask in range(1 << (m * n)):`：遍历所有 2^(m·n) 种选取组合。  
> - `if i in rows_used or j in cols_used:`：检测是否已有相同行/列被占用。  

#### 复杂度  

- **时间复杂度**：`O(2^{m·n} * (m·n))`  
  - `2^{m·n}` 是所有子集的数量，后面的乘积是检查每个子集时遍历格子的代价。  
  - 用大白话说，就是“把每一页词典的每一种可能组合都翻遍，还要逐页检查是否冲突”。  
- **空间复杂度**：`O(m·n)`  
  - 只保存了行、列集合以及当前遍历的格子列表。  

显然，这种办法只能在极小的矩阵（比如 2×2）上跑通，不能用于正式提交。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**冲突只和行、列是否被占用有关**，而不在乎我们到底选了哪几个具体的格子。  
这提示我们可以用**状态压缩 DP**（即位运算的“位掩码”）来记忆已经占用的行集合。

**核心观察**  

1. 每一列最多只能选 **一格**（否则必然与另一格同列冲突）。  
2. 处理列的顺序是天然的——从左到右逐列考虑。  
3. 当我们处理第 `c` 列时，只需要知道**已经用了哪些行**（用一个 `rows_mask` 表示），不必关心更早前选了哪些列。  

于是我们定义 DP 状态：

```
dp[mask] = 在已经处理完的若干列中，恰好占用了 mask 所表示的行集合时，能够得到的最大得分
```

- `mask` 是一个长度为 `m` 的二进制数，`mask & (1<<i) != 0` 表示第 `i` 行已经被选过。  
- 初始时 `dp[0] = 0`（什么行都没占，用分数 0），其余状态为负无穷。

**转移**  

对于当前列 `c`，我们可以：

* **不选** 任何格子 → `dp_next[mask] = max(dp_next[mask], dp[mask])`  
* **选** 第 `r` 行的格子（前提是该行尚未被占用） →  
  `new_mask = mask | (1 << r)`  
  `dp_next[new_mask] = max(dp_next[new_mask], dp[mask] + grid[r][c])`

遍历完所有列后，答案就是 `max(dp[mask])`（因为可以不必占满所有行）。

**为什么是最优的？**  

- 每一步只考虑**当前列的决定**，而所有之前的决定已经用 `mask` 完全记录。  
- DP 的“最优子结构”保证：若在前 `c` 列得到的最高分是 `dp[mask]`，则加入第 `c+1` 列的任何合法选择，都只能在此基础上加上该列对应的格子价值，得到的分数一定是**所有可能中最大的**。  
- 由于每列最多一次选择，状态数为 `2^m`（`m ≤ 10`），转移每次最多尝试 `m` 行，整体复杂度非常低。

#### 代码（Python）

```python
def maxScore_dp(grid):
    """
    动态规划（位掩码）求最大得分
    约束：每行、每列至多选一个格子
    """
    m, n = len(grid), len(grid[0])
    INF_NEG = -10**9                      # 表示不可能的负无穷

    # dp[mask] 表示已经占用了 mask 所对应的行集合时的最大得分
    dp = [INF_NEG] * (1 << m)
    dp[0] = 0                             # 初始：没有占用任何行，得分 0

    for col in range(n):                  # 按列从左到右遍历
        dp_next = dp[:]                    # 先复制为“不选当前列”的情况
        for mask in range(1 << m):        # 枚举已经占用的行集合
            if dp[mask] == INF_NEG:       # 这个状态不可达，直接跳过
                continue
            # 尝试在本列选第 r 行的格子（前提是该行未被占用）
            for r in range(m):
                if mask >> r & 1:          # 第 r 行已经被占，用不了
                    continue
                new_mask = mask | (1 << r) # 把第 r 行标记为已占用
                cand = dp[mask] + grid[r][col]
                if cand > dp_next[new_mask]:
                    dp_next[new_mask] = cand   # 更新到更大的分数
        dp = dp_next                       # 进入下一列

    # 最终答案是任意合法 mask 的最大值
    return max(dp)
```

**关键行中文注释**  

- `dp = [INF_NEG] * (1 << m)`：创建大小为 `2^m` 的 DP 表，初始为“不可达”。  
- `for col in range(n):`：按列顺序处理，保证后面的决定只依赖前面的状态。  
- `if mask >> r & 1:`：检查第 `r` 行是否已经被占用，若是则跳过。  
- `new_mask = mask | (1 << r)`：把第 `r` 行加入已占用集合。  
- `dp_next[new_mask] = cand`：如果这条新路径的得分更高，就更新。  

#### 复杂度  

- **时间复杂度**：`O(n * 2^m * m)`  
  - `n` 列循环；每列遍历 `2^m` 个行掩码；对每个掩码最多尝试 `m` 行。  
  - 对于 `m ≤ 10`、`n ≤ 10`，最多约 `10 * 1024 * 10 ≈ 1e5` 次操作，几乎瞬间完成。  
  - 与暴力的 `2^{m·n}` 相比，降低了指数层级，实际运行快很多。  

- **空间复杂度**：`O(2^m)`  
  - 只保存当前列的 DP 表（两份交替使用），大小为 `2^m ≤ 1024`，非常小。  

---

## 心得  

- **核心技巧**：**位掩码 DP**（状态压缩动态规划），用二进制记录哪些行已经被占用。  
- **适用题型**：  
  1. “在矩阵/棋盘上选格子，使行列互斥”——如 *Maximum Score of a Grid*、*Maximum Sum of Non‑Adjacent Cells*（行列约束）。  
  2. “给定两组元素，求不冲突的最大匹配”——二分图最大权匹配的规模受限版（`m,n ≤ 20`）。  
  3. “子集选择 + 互斥约束”——如背包类的“每类只能选一个”问题。  

> **一句话总结解题钥匙**：**把“哪些行已经被占”压成一个二进制数，逐列递推，所有合法组合的最优值就能一次算完。**

---

## 反思  

- **第一反应**：直接把所有格子列出来暴力枚举。  
- **最容易踩的坑**  
  1. **忘记“每列只能选一个”**，导致状态转移错误（会出现同列多选的非法解）。  
  2. **位运算写错**：`mask >> r & 1` 与 `(mask & (1 << r))` 的优先级容易混淆。  
  3. **初始值设为负无穷**，否则未覆盖的状态会误导最大值的比较。  
- **下次类似题**：  
  1. 先确认“互斥约束”是行、列还是其它维度。  
  2. 思考能否用 **位掩码** 把互斥信息压缩成状态。  
  3. 按照“自然的顺序”（列、行、时间等）逐步 DP，确保每一步只依赖已经确定的子问题。  

祝你在算法的道路上越走越顺 🚀